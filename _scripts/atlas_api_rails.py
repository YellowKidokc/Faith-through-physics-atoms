#!/usr/bin/env python3
"""Atlas API Rails v1.

Deterministic rail between a semantic/API classification packet and the Atlas registry.
It DOES NOT infer semantics. It validates structure, emits stable beacons, computes
safe graph/count projections, and combines child records into Series/Global records.

Usage:
  python _scripts/atlas_api_rails.py emit candidate.json --out _runtime/atlas-beacons
  python _scripts/atlas_api_rails.py combine record1.json record2.json \
      --resolution series --semantic-code SER.MASTER --label "Master Equation Series" \
      --out _runtime/atlas-beacons
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

VECTOR_ORDER = ("G", "M", "E", "S", "T", "K", "R", "Q", "F", "C")
TIE_ORDER = ("E", "C", "G", "K", "M", "T", "R", "F", "S", "Q")
MARKERS = tuple(f"{i:02d}" for i in range(1, 16))
MEETING_STATES = {
    "CONVERGED", "PRESSURE", "PRESSURE_DISCOVERY",
    "PREDICTED_NOT_OBSERVED", "UNRESOLVED", "CONTRADICTED"
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, dict):
        raise ValueError(f"{path}: top level must be an object")
    return obj


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def vector_string(vector: Dict[str, int]) -> str:
    return "".join(f"{k}{vector[k]}" for k in VECTOR_ORDER)


def expected_hash(vector: Dict[str, int]) -> str:
    ranked = sorted(VECTOR_ORDER, key=lambda k: (-vector[k], TIE_ORDER.index(k)))
    pairs = [(ranked[i], ranked[-1 - i]) for i in range(5)]
    return "".join(f"[{a}·{b}]" for a, b in pairs)


def validate_packet(packet: Dict[str, Any]) -> None:
    require(packet.get("protocol_version") == "ATLAS_API_RAILS_1.0",
            "protocol_version must equal ATLAS_API_RAILS_1.0")

    source = packet.get("source") or {}
    require(bool(source.get("document_id")), "source.document_id required")
    require(bool(re.fullmatch(r"[0-9a-fA-F]{64}", str(source.get("sha256", "")))), "source.sha256 must be 64 hex chars")
    require(isinstance(source.get("spans"), list), "source.spans must be a list")

    identity = packet.get("identity") or {}
    for key in ("uuid", "semantic_code", "human_label", "resolution"):
        require(identity.get(key) not in (None, ""), f"identity.{key} required")
    require(identity["resolution"] in {"local", "paper", "series", "global"}, "invalid identity.resolution")

    nabla = packet.get("nabla") or {}
    vector = nabla.get("vector") or {}
    require(tuple(vector.keys()) == VECTOR_ORDER, f"nabla.vector must use exact order: {' '.join(VECTOR_ORDER)}")
    for key in VECTOR_ORDER:
        require(vector[key] in (0, 3), f"nabla.vector.{key} must be 0 or 3")
    require(nabla.get("hash") == expected_hash(vector),
            f"nabla.hash mismatch; expected {expected_hash(vector)}")

    periodic = packet.get("periodic15") or {}
    missing = [m for m in MARKERS if m not in periodic]
    require(not missing, f"periodic15 missing markers: {missing}")

    stack = packet.get("atom_stack") or {}
    for key in ("atoms", "components", "claims", "evidence", "tests", "edges"):
        require(isinstance(stack.get(key), list), f"atom_stack.{key} must be a list")

    audit = packet.get("audit") or {}
    require(audit.get("admission_state") in {"candidate", "admitted"}, "audit.admission_state must be candidate or admitted")

    orientation = stack.get("orientation") or {}
    meeting = orientation.get("meeting_state")
    if meeting is not None:
        require(meeting in MEETING_STATES, f"unknown meeting_state: {meeting}")


def edge_endpoints(edge: Dict[str, Any]) -> tuple[str | None, str | None]:
    src = edge.get("source") or edge.get("from") or edge.get("source_id")
    dst = edge.get("target") or edge.get("to") or edge.get("target_id")
    return src, dst


def compute_local(packet: Dict[str, Any]) -> Dict[str, Any]:
    stack = packet["atom_stack"]
    edges = stack.get("edges", [])
    nodes = set()
    for bucket in ("atoms", "components", "claims", "evidence", "tests", "arguments", "bridges", "open_items"):
        for obj in stack.get(bucket, []) or []:
            oid = obj.get("id") or obj.get("atom_id") or obj.get("claim_id") or obj.get("component_id")
            if oid:
                nodes.add(str(oid))
    degree = Counter()
    for edge in edges:
        src, dst = edge_endpoints(edge)
        if src:
            degree[str(src)] += 1
            nodes.add(str(src))
        if dst:
            degree[str(dst)] += 1
            nodes.add(str(dst))

    identity_code = packet["identity"]["semantic_code"]
    primary_degree = degree.get(identity_code, 0)
    if primary_degree == 0 and len(packet["atom_stack"].get("atoms", [])) == 1:
        atom = packet["atom_stack"]["atoms"][0]
        atom_id = atom.get("id") or atom.get("atom_id")
        if atom_id:
            primary_degree = degree.get(str(atom_id), 0)

    return {
        "computed_at": now_iso(),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "claim_count": len(stack.get("claims", [])),
        "component_count": len(stack.get("components", [])),
        "evidence_count": len(stack.get("evidence", [])),
        "test_count": len(stack.get("tests", [])),
        "bridge_count": len(stack.get("bridges", [])),
        "open_item_count": len(stack.get("open_items", [])),
        "primary_graph_degree": primary_degree,
        "degree_by_node": dict(sorted(degree.items())),
        "note": "Counts/topology are deterministic projections. They do not promote standing or grades."
    }


def beacon_payloads(packet: Dict[str, Any], computed: Dict[str, Any]) -> Dict[str, Any]:
    stack = packet["atom_stack"]
    return {
        "01_identity": packet["identity"],
        "02_source": packet["source"],
        "03_nabla": packet["nabla"],
        "04_periodic15": packet["periodic15"],
        "05_atom_stack": {
            "atoms": stack.get("atoms", []),
            "components": stack.get("components", []),
            "claims": stack.get("claims", []),
            "arguments": stack.get("arguments", [])
        },
        "06_dependency": {"edges": stack.get("edges", []), "computed": computed},
        "07_warrant": {
            "evidence": stack.get("evidence", []),
            "tests": stack.get("tests", []),
            "open_items": stack.get("open_items", [])
        },
        "08_dynamics": stack.get("dynamics", {}),
        "09_orientation": stack.get("orientation", {}),
        "10_bridges": {"bridges": stack.get("bridges", [])},
        "11_reality_mirror": stack.get("reality_mirror", {}),
        "12_audit": packet.get("audit", {}),
        "13_computed": computed
    }


def emit(packet: Dict[str, Any], out_root: Path) -> Path:
    validate_packet(packet)
    computed = compute_local(packet)
    run_id = packet.get("audit", {}).get("run_id") or f"RUN-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    safe_code = re.sub(r"[^A-Za-z0-9._-]+", "_", packet["identity"]["semantic_code"])
    run_dir = out_root / f"{run_id}__{safe_code}"
    beacons_dir = run_dir / "beacons"

    beacons = beacon_payloads(packet, computed)
    manifest_entries = []
    for name, payload in beacons.items():
        path = beacons_dir / f"{name}.json"
        save_json(path, payload)
        manifest_entries.append({"beacon": name, "path": str(path.relative_to(run_dir)), "sha256": sha256_text(canonical_json(payload))})

    combined = dict(packet)
    combined["computed"] = computed
    combined["beacon_manifest"] = manifest_entries
    combined_path = run_dir / "combined.atlas-record.json"
    save_json(combined_path, combined)

    manifest = {
        "protocol": "ATLAS_API_RAILS_1.0",
        "run_id": run_id,
        "object": packet["identity"],
        "created_at": now_iso(),
        "admission_state": packet["audit"]["admission_state"],
        "beacons": manifest_entries,
        "combined": {
            "path": combined_path.name,
            "sha256": sha256_text(canonical_json(combined))
        }
    }
    save_json(run_dir / "00_manifest.json", manifest)
    return combined_path


def flatten(values: Iterable[Any]) -> List[Any]:
    out: List[Any] = []
    for value in values:
        if isinstance(value, list):
            out.extend(value)
        elif value not in (None, ""):
            out.append(value)
    return out


def aggregate_periodic(children: List[Dict[str, Any]], resolution: str, semantic_code: str) -> Dict[str, Any]:
    ps = [c.get("periodic15", {}) for c in children]
    native_domains = sorted(set(map(str, flatten(p.get("03", []) for p in ps))))
    bridged_domains = sorted(set(map(str, flatten(p.get("04", []) for p in ps))))
    claim_families = Counter(map(str, flatten(p.get("06") for p in ps)))
    functions = Counter(map(str, flatten(p.get("07") for p in ps)))
    disputes = Counter(map(str, flatten(p.get("11") for p in ps)))
    alerts = sorted(set(map(str, flatten(p.get("15") for p in ps))))
    total_runs = 0
    total_degree = 0
    for p in ps:
        try:
            total_runs += int(p.get("13", 0) or 0)
        except (TypeError, ValueError):
            pass
        try:
            total_degree += int(p.get("14", 0) or 0)
        except (TypeError, ValueError):
            pass

    object_type = "SERIES" if resolution == "series" else "GLOBAL_PROJECT"
    return {
        "01": semantic_code,
        "02": "AGGREGATED_JURISDICTION",
        "03": native_domains,
        "04": bridged_domains,
        "05": object_type,
        "06": {"distribution": dict(claim_families)},
        "07": {"distribution": dict(functions)},
        "08": {"child_record_count": len(children), "provenance": "child_records"},
        "09": "AGGREGATED_UNADJUDICATED",
        "10": "UNRESOLVED_REQUIRES_DECLARED_AGGREGATION_RULE",
        "11": {"distribution": dict(disputes)},
        "12": "UNKNOWN_REQUIRES_GRADE_REGISTRY_AGGREGATION",
        "13": total_runs,
        "14": total_degree,
        "15": alerts or ["NONE_REPORTED"]
    }


def combine(paths: List[Path], resolution: str, semantic_code: str, label: str, out_root: Path) -> Path:
    require(resolution in {"series", "global"}, "combine resolution must be series or global")
    children = [load_json(p) for p in paths]
    require(children, "at least one child record required")
    for child in children:
        validate_packet(child)

    child_hashes = [sha256_text(canonical_json(c)) for c in children]
    agg_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, resolution + ":" + semantic_code + ":" + "|".join(child_hashes)))
    periodic = aggregate_periodic(children, resolution, semantic_code)

    record = {
        "protocol_version": "ATLAS_API_RAILS_1.0",
        "source": {
            "document_id": semantic_code,
            "sha256": sha256_text("|".join(child_hashes)),
            "title": label,
            "spans": []
        },
        "identity": {
            "uuid": agg_uuid,
            "semantic_code": semantic_code,
            "human_label": label,
            "resolution": resolution
        },
        "nabla": {
            "filing": "AGGREGATE/" + semantic_code,
            "vector": {k: 0 for k in VECTOR_ORDER},
            "hash": expected_hash({k: 0 for k in VECTOR_ORDER}),
            "confidence": {},
            "review_flags": ["AGGREGATE_NABLA_REQUIRES_SEMANTIC_ADJUDICATION"]
        },
        "periodic15": periodic,
        "atom_stack": {
            "atoms": flatten(c.get("atom_stack", {}).get("atoms", []) for c in children),
            "components": flatten(c.get("atom_stack", {}).get("components", []) for c in children),
            "claims": flatten(c.get("atom_stack", {}).get("claims", []) for c in children),
            "evidence": flatten(c.get("atom_stack", {}).get("evidence", []) for c in children),
            "tests": flatten(c.get("atom_stack", {}).get("tests", []) for c in children),
            "edges": flatten(c.get("atom_stack", {}).get("edges", []) for c in children),
            "arguments": flatten(c.get("atom_stack", {}).get("arguments", []) for c in children),
            "bridges": flatten(c.get("atom_stack", {}).get("bridges", []) for c in children),
            "open_items": flatten(c.get("atom_stack", {}).get("open_items", []) for c in children),
            "dynamics": {"status": "REQUIRES_DECLARED_AGGREGATION_RULE"},
            "orientation": {"meeting_state": "UNRESOLVED", "status": "REQUIRES_AGGREGATION_OR_PHI"},
            "reality_mirror": {"status": "REQUIRES_AGGREGATION"}
        },
        "audit": {
            "origin": "python_aggregate",
            "admission_state": "candidate",
            "model": None,
            "prompt_version": None,
            "run_id": None,
            "confidence": None,
            "review_flags": [
                "AGGREGATE_RECORD_DOES_NOT_INHERIT_CHILD_STANDING_AUTOMATICALLY",
                "AGGREGATE_NABLA_REQUIRES_SEMANTIC_ADJUDICATION"
            ]
        },
        "children": [{"semantic_code": c["identity"]["semantic_code"], "sha256": h} for c, h in zip(children, child_hashes)]
    }
    return emit(record, out_root)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Atlas API Rails: validate, beacon, combine")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_emit = sub.add_parser("emit", help="Validate one API packet and emit deterministic beacons")
    p_emit.add_argument("packet", type=Path)
    p_emit.add_argument("--out", type=Path, default=Path("_runtime/atlas-beacons"))

    p_combine = sub.add_parser("combine", help="Combine emitted/local Atlas records conservatively")
    p_combine.add_argument("records", nargs="+", type=Path)
    p_combine.add_argument("--resolution", required=True, choices=["series", "global"])
    p_combine.add_argument("--semantic-code", required=True)
    p_combine.add_argument("--label", required=True)
    p_combine.add_argument("--out", type=Path, default=Path("_runtime/atlas-beacons"))

    args = parser.parse_args(argv)
    try:
        if args.cmd == "emit":
            packet = load_json(args.packet)
            out = emit(packet, args.out)
        else:
            out = combine(args.records, args.resolution, args.semantic_code, args.label, args.out)
        print(out)
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
