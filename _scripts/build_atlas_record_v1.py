#!/usr/bin/env python3
"""Build AtlasRecord v1 gold slices from the existing atom layer.

This script deliberately adapts existing records instead of inventing a new
classification engine. Missing external subsystems are recorded in `unmapped`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ATOM = ROOT / "_ledger" / "atoms" / "tp-lane4-master-equation-me-01-001-trilemma-impossibility.json"
DEFAULT_OUT = ROOT / "gold" / "master-equation" / "atlas-record-v1.master-equation.trilemma.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:16]


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_source_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.exists():
        return path
    candidate = ROOT / "master-equation" / "01_canonical" / path.name
    return candidate if candidate.exists() else path


def normalized_claim_mode(source: dict[str, Any], atom: dict[str, Any]) -> str:
    native = source.get("evidenceType") or source.get("verificationStatus") or atom.get("claim_class", "")
    return {
        "formal_derivation": "FORMAL_DERIVATION",
        "theorem": "FORMAL_DERIVATION",
        "empirical_event": "EMPIRICAL_EVENT",
        "axiom": "AXIOM",
        "pre_assumption": "PRE_ASSUMPTION",
    }.get(str(native).lower(), "UNKNOWN")


def component(atom: dict[str, Any], kind: str, label: str, content: Any, index: int, criteria: list[str]) -> dict[str, Any]:
    atom_id = atom["atom_id"]
    suffix = kind.replace("_", "-")
    return {
        "component_id": f"{atom_id}.{suffix}.{index:02d}",
        "type": kind,
        "label": label,
        "content": content,
        "meta_criteria_ids": criteria,
        "standing": atom.get("current_status", "candidate"),
        "source_span_ids": ["source-span:primary-jsonld"],
    }


def build_components(atom: dict[str, Any], source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": f"{atom['atom_id']}.claim.01",
            "type": "claim",
            "label": "Claim",
            "content": atom["claim"],
            "meta_criteria_ids": ["dependency", "evidence", "coherence", "provenance", "translation"],
            "standing": atom.get("current_status", "candidate"),
            "source_span_ids": ["source-span:primary-jsonld"],
        }
    ]
    for source_component in source.get("claimComponents", []):
        rows.append({
            "component_id": source_component.get("componentID", ""),
            "type": "claim_component",
            "label": source_component.get("predicate", "Claim Component"),
            "content": source_component.get("predicate", ""),
            "meta_criteria_ids": ["dependency", "evidence", "falsifiability", "provenance"],
            "standing": source_component.get("status", "UNKNOWN"),
            "source_span_ids": ["source-span:claim-components"],
        })
    mappings = [
        ("assumption", "assumptions", ["dependency", "coherence", "provenance"]),
        ("definition", "definitions", ["coherence", "translation", "provenance"]),
        ("equation", "equations", ["formal", "falsifiability", "dependency", "provenance"]),
        ("dependency", "dependencies", ["dependency", "blast_radius", "coherence"]),
        ("negative_guard", "negative_guards", ["falsifiability", "coherence", "blast_radius"]),
        ("kill_condition", "kill_conditions", ["falsifiability", "blast_radius", "evidence"]),
        ("bridge", "bridges", ["cross_domain", "translation", "provenance", "independence"]),
    ]
    for kind, field, criteria in mappings:
        for index, value in enumerate(atom.get(field, []), 1):
            rows.append(component(atom, kind, kind.replace("_", " ").title(), value, index, criteria))
    return rows


def build_record(atom_path: Path) -> dict[str, Any]:
    atom = load_json(atom_path)
    raw_source_paths = [str(p) for p in atom.get("source_artifacts", [])]
    resolved_sources = [resolve_source_path(path) for path in raw_source_paths]
    source_path = next((path for path in resolved_sources if path.exists()), None)
    source = load_json(source_path) if source_path else {}
    atlas = ROOT / "_atlas"
    coverage = [r for r in load_jsonl(atlas / "evidence-coverage.jsonl") if r.get("claim_id") == atom.get("source_claim_id")]
    projections = [r for r in load_jsonl(atlas / "projections.jsonl") if r.get("claim_id") == atom.get("source_claim_id")]
    gates = [r for r in load_jsonl(atlas / "preadmission-gates.jsonl") if r.get("atom_id") in {atom.get("source_claim_id"), atom.get("atom_id")}]

    atom_rel = atom_path.relative_to(ROOT).as_posix()
    source_paths = [
        path.relative_to(ROOT).as_posix() if path.exists() and path.is_relative_to(ROOT) else str(path).replace("\\", "/")
        for path in resolved_sources
    ]
    aliases = [x for x in [atom.get("original_jsonld_id"), atom.get("original_node_id")] if x]

    components = build_components(atom, source)
    grade_registry = load_json(atlas / "grade-registry.json")
    native_grade = atom.get("proof_label", "UNKNOWN")
    grade_rule = grade_registry.get("mode_to_atlas", {}).get(native_grade)
    normalized_grade = grade_rule.get("atlas_grade", "UNKNOWN") if grade_rule else "UNKNOWN"
    source_edges = {edge.get("target"): edge for edge in source.get("edges", [])}
    admitted_bridge_targets = [
        target for target in atom.get("bridges", [])
        if source_edges.get(target, {}).get("status") == "accepted"
    ]
    open_component_ids = [
        row.get("componentID", "")
        for row in source.get("claimComponents", [])
        if row.get("status") in {"open", "contested", "unverified"}
    ]
    component_types = sorted({row["type"] for row in components})
    evidence = []
    anchors = []
    for row in coverage:
        for idx, support in enumerate(row.get("supports", []), 1):
            evidence_id = row.get("evidence_id", row.get("coverage_id", "evidence"))
            component_id = support.get("claim_component", "")
            evidence.append({
                "evidence_id": evidence_id if len(row.get("supports", [])) == 1 else f"{evidence_id}.{idx:02d}",
                "claim_id": row["claim_id"],
                "component_id": component_id,
                "relation": support.get("relation", "supports"),
                "strength": support.get("strength", "UNKNOWN"),
                "coverage": float(row.get("coverage", 0)),
                "statement": support.get("note", row.get("method_note", "")),
                "source": row.get("source_artifact", ""),
                "does_not_show": row.get("unaddressed", []),
            })
            anchors.append({
                "anchor_id": f"anchor:{digest(evidence_id + component_id)}",
                "class": "coverage_receipt",
                "status": "Candidate",
                "target_id": component_id,
                "limitations": row.get("method_note", ""),
            })

    tests = []
    for idx, condition in enumerate(atom.get("kill_conditions", []), 1):
        tests.append({
            "test_id": f"{atom['atom_id']}.kill.{idx:02d}",
            "claim_id": atom.get("source_claim_id", atom["atom_id"]),
            "type": "kill_condition",
            "condition": condition,
            "status": "untested",
            "blast_radius": "component_and_downstream_dependencies",
        })
    for projection in projections:
        for idx, condition in enumerate(projection.get("kill_conditions", []), 1):
            tests.append({
                "test_id": f"{projection['projection_id']}.kill.{idx:02d}",
                "claim_id": projection["claim_id"],
                "type": "projection_kill_condition",
                "condition": condition,
                "status": projection.get("result", "declared"),
                "blast_radius": "projection_path",
            })

    edges = []
    for idx, dep in enumerate(atom.get("dependencies", []), 1):
        edges.append({
            "edge_id": f"edge:{digest(atom['atom_id'] + 'depends' + dep)}",
            "from": atom["atom_id"],
            "relation": "dependsOn",
            "to": dep,
            "status": "declared_by_atom",
            "source": atom_rel,
        })
    for idx, bridge in enumerate(atom.get("bridges", []), 1):
        source_edge = source_edges.get(bridge, {})
        edges.append({
            "edge_id": f"edge:{digest(atom['atom_id'] + 'bridge' + bridge)}",
            "from": atom["atom_id"],
            "relation": "bridgesTo",
            "to": bridge,
            "status": source_edge.get("status", "declared_by_atom"),
            "source": atom_rel,
        })
    for projection in projections:
        for edge in projection.get("edges", []):
            edges.append({
                "edge_id": f"edge:{digest(projection['projection_id'] + json.dumps(edge, sort_keys=True))}",
                "from": edge.get("from", ""),
                "relation": edge.get("relation_type", ""),
                "to": edge.get("to", ""),
                "status": projection.get("result", "declared"),
                "source": projection["projection_id"],
            })

    bridges = [
        {
            "bridge_id": f"bridge:{digest(atom['atom_id'] + bridge)}",
            "target": bridge,
            "mapping_type": source_edges.get(bridge, {}).get("grade", atom.get("bridge_grade", "declared_bridge")),
            "standing": "Admitted" if source_edges.get(bridge, {}).get("status") == "accepted" else "Candidate",
            "forbidden": "Bridge declaration must not promote native grade without independent warrant.",
        }
        for bridge in atom.get("bridges", [])
    ]

    ascent = next((p for p in projections if p.get("mode") == "ascendant"), {})
    descent = next((p for p in projections if p.get("mode") == "descendant"), {})
    meeting = next((p for p in projections if p.get("mode") == "meeting"), {})

    admitted = any(g.get("admission_status") == "admitted" for g in gates)
    candidate_or_admitted = "Admitted" if admitted else "Candidate"
    admission_receipts = []
    for gate in gates:
        human_audit = gate.get("human_audit", {})
        if isinstance(human_audit, dict) and human_audit:
            admission_receipts.append({
                "system": "human audit",
                "status": "filled" if human_audit.get("status") else "partially_filled",
                "owned_fields": ["audit.candidate_or_admitted"],
                "notes": f"Pre-admission gate origin={gate.get('origin', 'UNKNOWN')}; human_audit={json.dumps(human_audit, sort_keys=True)}",
            })
    claims = [
        {
            "claim_id": atom.get("source_claim_id", atom["atom_id"]),
            "text": atom["claim"],
            "formal_restatement": source.get("statementTechnical", "; ".join(atom.get("equations", []))),
            "mode": normalized_claim_mode(source, atom),
            "mode_native": source.get("evidenceType", atom.get("claim_class", "")),
            "standing": atom.get("current_status", ""),
            "native_grade": native_grade,
            "source_span_ids": ["source-span:primary-jsonld", "source-span:technical-statement"],
            "notes": "Native grade preserved; meta score must remain computed separately.",
        }
    ]

    return {
        "schema_version": "atlas-record/v1",
        "id": {
            "record_id": "atlas-record:master-equation:trilemma-impossibility",
            "atom_id": atom["atom_id"],
            "source_claim_id": atom.get("source_claim_id", ""),
            "stable_uid": atom.get("atom_uid", ""),
            "aliases": aliases,
        },
        "source": {
            "kind": "lane4_atom_json",
            "title": atom["title"],
            "content_hash": file_hash(source_path) if source_path else "UNKNOWN",
            "paths": [atom_rel] + source_paths,
            "source_spans": [
                {
                    "span_id": "source-span:technical-statement",
                    "path": source_paths[0] if source_paths else atom_rel,
                    "selector": "/statementTechnical",
                    "quote": source.get("statementTechnical", atom["claim"]),
                },
                {
                    "span_id": "source-span:primary-jsonld",
                    "path": source_paths[0] if source_paths else atom_rel,
                    "selector": "/statementPlain",
                    "quote": source.get("statementPlain", atom["claim"]),
                },
                {
                    "span_id": "source-span:claim-components",
                    "path": source_paths[0] if source_paths else atom_rel,
                    "selector": "/claimComponents",
                    "quote": json.dumps(source.get("claimComponents", []), ensure_ascii=False),
                },
                {
                    "span_id": "source-span:mathematical-form",
                    "path": source_paths[0] if source_paths else atom_rel,
                    "selector": "/mathematicalForm",
                    "quote": source.get("mathematicalForm", "; ".join(atom.get("equations", []))),
                },
            ],
            "provenance": [
                {
                    "timestamp": event.get("timestamp", ""),
                    "event_type": event.get("event_type", ""),
                    "result": event.get("result", ""),
                    "limits": event.get("limits", ""),
                    "reviewer": event.get("reviewer", ""),
                }
                for event in atom.get("ledger", [])
            ],
        },
        "nabla": {
            "classification": "artifact:atom/lane4; domain:master-equation; role:technical-canonical-claim",
            "semantic_address": "nabla://faith-through-physics/master-equation/01-canonical/ME-01-001-trilemma-impossibility#tp:ME/L5/C1",
            "routing_hints": [
                "open lane4 atom first",
                "open canonical JSON-LD source",
                "load Atlas evidence coverage for tp:ME/L5/C1",
                "load Atlas ascent/descent projections for tp:ME/L5/C1"
            ],
            "deterministic_status": "candidate",
            "notes": "Nabla canonical service was not available locally; this is a deterministic address derived from existing repository paths and ids.",
        },
        "periodic15": {
            "marker_1_scope": "paper/local",
            "marker_2_home_domain": atom.get("domain", ""),
            "marker_3_native_domains": [atom.get("domain", "")],
            "marker_4_bridged_domains": admitted_bridge_targets,
            "marker_5_object_type": "Equation / Model",
            "marker_6_claim_family": "Quantity / Measurement",
            "marker_7_function_kind": "Derivation",
            "marker_8_source_kind": "lane4_atom_json",
            "marker_9_standing": atom.get("current_status", ""),
            "marker_10_native_grade": native_grade,
            "marker_11_modality": atom.get("mode_classification", ""),
            "marker_12_evidence_grade": normalized_grade,
            "marker_13_dispute": "open:" + ",".join(open_component_ids) if open_component_ids else "none_declared",
            "marker_14_publication_state": f"source:{source.get('stage', 'UNKNOWN')}/{source.get('status', 'UNKNOWN')};lane4:{atom.get('current_status', 'UNKNOWN')}",
            "marker_15_component_state": ",".join(component_types),
        },
        "atom_stack": {
            "atom": {
                "atom_id": atom["atom_id"],
                "title": atom["title"],
                "object_type": "Equation / Model",
                "standing": atom.get("current_status", "UNKNOWN"),
                "native_grade": native_grade,
            },
            "components": components,
            "claims": claims,
            "upstream": list(atom.get("dependencies", [])),
            "downstream": [],
            "dependencies": list(atom.get("dependencies", [])),
            "arguments": [],
            "warrant": {
                "evidence_receipt_ids": [row["evidence_id"] for row in evidence],
                "proof_test_ids": [row["test_id"] for row in tests if row["type"] != "kill_condition"],
                "counterevidence_ids": [],
                "kill_condition_ids": [row["test_id"] for row in tests if "kill_condition" in row["type"]],
            },
            "tests": tests,
            "dynamics": {
                "ascent": ascent,
                "translation": {
                    "status": "partial",
                    "preserved": ["closed-system trilemma invariant"],
                    "lost": ["historical instantiation is not established by algebra alone"],
                    "introduced": [],
                    "forbidden": ["do not turn theological bridge into propagated evidence"]
                },
                "descent": descent,
                "meeting_state": meeting.get("result", "UNRESOLVED"),
            },
        },
        "evidence_receipts": evidence,
        "edges": edges,
        "bridges": bridges,
        "anchors": anchors,
        "reality_mirror": {
            "class": "F",
            "status": "Candidate",
            "rule": "Reality Mirror tests whether the claim reaches a constraint the system did not manufacture; it is not Marker 16.",
            "anchor_ids": [row["anchor_id"] for row in anchors],
        },
        "meta_argument": {
            "status": "not_run",
            "engine": "YellowKidokc/the-meta-argument",
            "input_profile": "formal_claim_adapter_required",
            "variables": {},
            "refusal_states": ["INSUFFICIENTLY_DEFINED"],
            "veto": "UNKNOWN",
            "confidence": "UNKNOWN",
            "dependencies": [],
        },
        "computed": {
            "graph_signature": {
                "declared_dependency_count": len(atom.get("dependencies", [])),
                "declared_bridge_count": len(atom.get("bridges", [])),
                "evidence_receipt_count": len(evidence),
                "kill_condition_count": len(tests),
            },
            "grade_projection": {
                "registry": "_atlas/grade-registry.json",
                "native_grade": native_grade,
                "normalized_grade": normalized_grade,
                "status": "computed" if grade_rule else "UNKNOWN",
            },
            "load_bearing": gates[0].get("computed_load_bearing", "UNKNOWN") if gates else "UNKNOWN",
            "blast_radius": list(atom.get("dependencies", [])),
        },
        "audit": {
            "candidate_or_admitted": candidate_or_admitted,
            "subsystem_receipts": [
                {
                    "system": "Nabla",
                    "status": "partially_filled",
                    "owned_fields": ["nabla"],
                    "notes": "Semantic address derived from repo path/id; external Nabla classifier not run.",
                },
                {
                    "system": "Argument Compiler",
                    "status": "not_run",
                    "owned_fields": ["claims", "components", "evidence", "tests", "edges"],
                    "notes": "Remote repo inspected: its draft model covers sources, claims, evidence, citations, and edges, but it does not yet provide a runnable extraction pipeline or complete Atlas adapter.",
                },
                {
                    "system": "The Meta-Argument",
                    "status": "not_run",
                    "owned_fields": ["computed.meta_scores", "computed.deterministic_audit"],
                    "notes": "Remote repo inspected: its engine scores atomic historical/action cases. It was not run because this formal claim does not satisfy that case contract without a typed adapter.",
                },
                {
                    "system": "Atlas",
                    "status": "filled",
                    "owned_fields": ["periodic15", "dynamics", "bridges", "anchors", "computed.graph_signature"],
                    "notes": "Filled from _atlas registries and Lane 4 atom layer.",
                },
                {
                    "system": "AXIOM-REACT",
                    "status": "external_missing",
                    "owned_fields": ["rendering"],
                    "notes": "React app is local but not modified by this builder; consume this JSON as UI input.",
                }
            ] + admission_receipts,
            "warnings": [
                "Historical instantiation remains open and must not be inferred from algebra.",
                "Bridge declaration must not promote native grade without independent warrant.",
                "Marker 4 contains admitted bridge targets only; candidate bridges remain in bridges[].",
                f"Graph admission is {candidate_or_admitted}; Lane 4 lifecycle remains {atom.get('current_status', 'UNKNOWN')}. These are separate states.",
                "Meta score is not native grade.",
                "Reality Mirror is metadata, not Marker 16."
            ],
        },
        "unresolved": [
            {
                "field_or_requirement": "Marker 12 normalized evidence grade",
                "reason": f"Native grade {native_grade!r} is not present in the C0-C6 grade registry." if not grade_rule else "Mapped by grade registry.",
                "next_step": "Assign or import a ratified C0-C6 native grade before projecting an Atlas grade." if not grade_rule else "No action required.",
            },
            {
                "field_or_requirement": "Nabla v6 vector, pairing hash, and per-dimension confidence",
                "reason": "No source-owned Nabla packet for this exact Master Equation atom was found; only a deterministic repository address can be derived safely.",
                "next_step": "Run the Nabla classifier and attach its source packet without replacing the canonical artifact paths or spans.",
            },
            {
                "field_or_requirement": "Argument Compiler native extraction",
                "reason": "The remote draft schema has Source, Citation, Evidence, Claim, ArgumentEdge, and ArgumentGraph, but no implemented source extraction receipt, component model, warrant/objection model, or byte-preserving source-span contract.",
                "next_step": "Implement a typed export adapter in argument-compiler; replace the current Lane 4 adaptation only after its output preserves exact locators and source hashes.",
            },
            {
                "field_or_requirement": "The Meta-Argument deterministic scoring",
                "reason": "The remote case schema is real but requires actor/action/target/cost-bearer historical-case fields. The Master Equation formal claim cannot be inserted without fabricating those values.",
                "next_step": "Add a formal-claim adapter or a separate typed case profile, then run the existing engine to fill variables, direction, veto, confidence, dependencies, and refusal states.",
            },
            {
                "field_or_requirement": "AXIOM-REACT render integration",
                "reason": "No React import route has been wired yet.",
                "next_step": "Add AXIOM-REACT data loader for gold/master-equation/atlas-record-v1.master-equation.trilemma.json.",
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atom", type=Path, default=DEFAULT_ATOM)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    record = build_record(args.atom)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
