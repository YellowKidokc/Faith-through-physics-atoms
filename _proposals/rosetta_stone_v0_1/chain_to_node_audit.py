#!/usr/bin/env python3
"""Deterministic chain-to-node connector.

This tool maps extracted semantic nodes to a declared chain schema. It does not
extract nodes, call a model, change source files, or grant truth/canon status.
It produces a connection map, floating-node report, and gap analysis.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_FLOAT_THRESHOLD = 0.18
DEFAULT_STRONG_THRESHOLD = 0.34

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "from",
    "has", "have", "if", "in", "into", "is", "it", "its", "no", "not",
    "of", "on", "or", "rather", "that", "the", "their", "then", "there",
    "this", "to", "with", "without", "who", "when", "where", "which",
    "while", "will", "within",
}

ALIASES = {
    "exist": {"exist", "exists", "existence", "being", "something", "nonempty"},
    "create": {"create", "creates", "creation", "created", "creator", "sustain", "sustains"},
    "distinction": {"distinction", "distinguish", "distinguishable", "difference", "different", "state", "states"},
    "information": {"information", "signal", "code", "distinction", "bits", "shannon", "record", "data"},
    "truth": {"truth", "true", "truthful", "falsify", "falsification", "provenance", "record", "ledger"},
    "value": {"value", "good", "better", "worse", "preserve", "preservation", "damage"},
    "moral": {"moral", "morality", "right", "wrong", "ought", "sin", "debt", "justice", "mercy"},
    "agency": {"agency", "agent", "choice", "choose", "will", "voluntary", "responsibility"},
    "law": {"law", "laws", "rule", "rules", "boundary", "limit", "limits", "time", "consequence", "consequences"},
    "entropy": {"entropy", "decay", "dissipation", "vulnerability", "drift", "finite", "closed", "isolated"},
    "adversarial": {"adversarial", "enemy", "exploit", "amplify", "attractor", "incoherence", "anti"},
    "grace": {"grace", "repair", "restore", "restoration", "external", "source", "input", "coherence"},
    "cross": {"cross", "christ", "cost", "payer", "atonement", "justice", "mercy", "convergence"},
    "coherence": {"coherence", "coherent", "chi", "integrate", "integration", "restore", "alignment"},
    "observer": {"observer", "observation", "actualization", "actualize", "watcher", "selection"},
    "substrate": {"substrate", "carrier", "ground", "source", "support"},
}


@dataclass(frozen=True)
class Node:
    node_id: str
    text: str
    source_file: str
    trace_id: str | None
    raw: dict[str, Any]


@dataclass(frozen=True)
class Reference:
    ref_id: str
    ref_type: str
    label: str
    text: str
    raw: dict[str, Any]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_token(token: str) -> str:
    token = token.lower().strip("_-")
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 4 and token.endswith("ing"):
        return token[:-3]
    if len(token) > 3 and token.endswith("ed"):
        return token[:-2]
    if len(token) > 3 and token.endswith("s"):
        return token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    raw = re.findall(r"[A-Za-z0-9_]+", text.lower())
    return [normalize_token(tok) for tok in raw if len(tok) > 1 and tok not in STOPWORDS]


def expand_tokens(tokens: Iterable[str]) -> Counter[str]:
    counts: Counter[str] = Counter(tokens)
    token_set = set(counts)
    for canonical, variants in ALIASES.items():
        normalized_variants = {normalize_token(v) for v in variants}
        if token_set & normalized_variants:
            counts[canonical] += 2
            for variant in normalized_variants:
                counts[variant] += 1
    return counts


def text_from_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return " ".join(text_from_value(item) for item in value)
    if isinstance(value, dict):
        return " ".join(text_from_value(item) for item in value.values())
    return str(value)


def node_text(payload: dict[str, Any]) -> str:
    fields = [
        "coherent_statement",
        "plain_statement",
        "statement",
        "text",
        "claim",
        "scope_text",
        "source_quotes",
        "formal_expressions",
        "definition_attempts",
        "open_textual_questions",
    ]
    return " ".join(text_from_value(payload.get(field)) for field in fields).strip()


def iter_node_payloads(path: Path) -> Iterable[tuple[dict[str, Any], str | None]]:
    payload = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item, item.get("trace_id")
        return
    if not isinstance(payload, dict):
        return

    trace_id = payload.get("trace_id") or payload.get("result", {}).get("trace_id")
    containers: list[Any] = []
    if isinstance(payload.get("result"), dict):
        containers.append(payload["result"].get("semantic_nodes"))
        containers.append(payload["result"].get("nodes"))
    containers.extend([payload.get("semantic_nodes"), payload.get("nodes")])

    emitted = False
    for container in containers:
        if isinstance(container, list):
            for item in container:
                if isinstance(item, dict):
                    emitted = True
                    yield item, trace_id or item.get("trace_id")

    if not emitted and payload.get("node_id"):
        yield payload, trace_id or payload.get("trace_id")


def load_nodes(node_dir: Path) -> list[Node]:
    nodes: list[Node] = []
    seen: set[tuple[str, str]] = set()
    for path in sorted(node_dir.rglob("*.json")):
        try:
            for payload, trace_id in iter_node_payloads(path):
                node_id = str(payload.get("node_id", "")).strip()
                if not node_id:
                    continue
                key = (node_id, str(path))
                if key in seen:
                    continue
                text = node_text(payload)
                if not text:
                    continue
                seen.add(key)
                nodes.append(Node(node_id=node_id, text=text, source_file=str(path), trace_id=trace_id, raw=payload))
        except json.JSONDecodeError:
            continue
    return nodes


def load_schema(schema_path: Path) -> dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8", errors="replace"))


def build_references(schema: dict[str, Any]) -> list[Reference]:
    refs: list[Reference] = []
    for item in schema.get("chain", []):
        step = item.get("step")
        label = f"Step {step}: {item.get('axiom', '')}"
        text = " ".join([text_from_value(item.get("axiom")), text_from_value(item.get("layer")), text_from_value(item.get("follows_from"))])
        refs.append(Reference(f"chain:{step}", "chain", label, text, item))
    for item in schema.get("proof_stack", []):
        ref_id = str(item.get("id", ""))
        label = f"{ref_id}: {item.get('name', '')}"
        text = " ".join([
            text_from_value(item.get("id")),
            text_from_value(item.get("name")),
            text_from_value(item.get("type")),
            text_from_value(item.get("statement")),
            text_from_value(item.get("kill_condition")),
        ])
        refs.append(Reference(f"proof:{ref_id}", "proof_stack", label, text, item))
    for item in schema.get("derivative_families", []):
        symbol = str(item.get("symbol", ""))
        label = f"{symbol}: {item.get('family', '')}"
        text = " ".join([
            text_from_value(item.get("symbol")),
            text_from_value(item.get("family")),
            text_from_value(item.get("status")),
            text_from_value(item.get("modes")),
            text_from_value(item.get("kill_condition")),
        ])
        refs.append(Reference(f"family:{symbol}", "derivative_family", label, text, item))
    return refs


def cosine(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    common = set(left) & set(right)
    dot = sum(left[tok] * right[tok] for tok in common)
    left_norm = math.sqrt(sum(v * v for v in left.values()))
    right_norm = math.sqrt(sum(v * v for v in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return dot / (left_norm * right_norm)


def score_node(node: Node, references: list[Reference]) -> list[dict[str, Any]]:
    node_counts = expand_tokens(tokenize(node.text))
    scored: list[dict[str, Any]] = []
    for ref in references:
        ref_counts = expand_tokens(tokenize(ref.text))
        common = sorted((set(node_counts) & set(ref_counts)), key=lambda tok: (node_counts[tok] + ref_counts[tok], tok), reverse=True)
        score = cosine(node_counts, ref_counts)
        scored.append({
            "ref_id": ref.ref_id,
            "ref_type": ref.ref_type,
            "label": ref.label,
            "score": round(score, 4),
            "shared_terms": common[:12],
        })
    return sorted(scored, key=lambda row: (row["score"], len(row["shared_terms"])), reverse=True)


def relationship_for(node: Node, best: dict[str, Any], threshold: float) -> str:
    text = node.text.lower()
    if best["score"] < threshold:
        return "floating"
    contradiction_markers = ("defeat", "challenge", "contradict", "falsify", "kill condition", "objection", "could be defeated")
    boundary_markers = ("separate claim", "not automatically", "until independently supported", "boundary", "open question")
    if any(marker in text for marker in contradiction_markers):
        return "counter_or_kill_condition"
    if any(marker in text for marker in boundary_markers):
        return "boundary_or_qualification"
    return "supports_or_elaborates"


def best_by_type(ranked: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    best: dict[str, dict[str, Any]] = {}
    for row in ranked:
        best.setdefault(row["ref_type"], row)
    return best


def connect(nodes: list[Node], references: list[Reference], threshold: float, strong_threshold: float) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_ref: dict[str, list[dict[str, Any]]] = defaultdict(list)
    floating: list[dict[str, Any]] = []
    weak: list[dict[str, Any]] = []

    for node in nodes:
        ranked = score_node(node, references)
        best = ranked[0] if ranked else {"score": 0, "ref_id": None, "label": "", "ref_type": "", "shared_terms": []}
        second = ranked[1] if len(ranked) > 1 else None
        typed_best = best_by_type(ranked)
        typed_matches: dict[str, dict[str, Any]] = {}
        connected = False
        has_weak = False
        has_strong = False
        for ref_type in ("chain", "proof_stack", "derivative_family"):
            type_best = typed_best.get(ref_type, {"score": 0, "ref_id": None, "label": "", "ref_type": ref_type, "shared_terms": []})
            type_relationship = relationship_for(node, type_best, threshold)
            type_connected = type_relationship != "floating"
            type_confidence = "floating"
            if type_connected:
                type_confidence = "strong" if type_best["score"] >= strong_threshold else "weak"
                connected = True
                has_weak = has_weak or type_confidence == "weak"
                has_strong = has_strong or type_confidence == "strong"
            typed_matches[ref_type] = {
                "connected": type_connected,
                "relationship": type_relationship,
                "confidence": type_confidence,
                "ref_id": type_best["ref_id"],
                "label": type_best["label"],
                "score": type_best["score"],
                "shared_terms": type_best["shared_terms"],
            }
        relationship = "floating"
        confidence = "floating"
        if connected:
            relationship = "multi_axis_connection"
            confidence = "strong" if has_strong else "weak"
        row = {
            "node_id": node.node_id,
            "trace_id": node.trace_id,
            "source_file": node.source_file,
            "connected": connected,
            "relationship": relationship,
            "confidence": confidence,
            "best_ref_id": best["ref_id"],
            "best_ref_type": best["ref_type"],
            "best_label": best["label"],
            "score": best["score"],
            "shared_terms": best["shared_terms"],
            "second_ref_id": second["ref_id"] if second else None,
            "second_score": second["score"] if second else None,
            "chain_ref_id": typed_matches["chain"]["ref_id"],
            "chain_score": typed_matches["chain"]["score"],
            "chain_relationship": typed_matches["chain"]["relationship"],
            "chain_confidence": typed_matches["chain"]["confidence"],
            "proof_ref_id": typed_matches["proof_stack"]["ref_id"],
            "proof_score": typed_matches["proof_stack"]["score"],
            "proof_relationship": typed_matches["proof_stack"]["relationship"],
            "proof_confidence": typed_matches["proof_stack"]["confidence"],
            "family_ref_id": typed_matches["derivative_family"]["ref_id"],
            "family_score": typed_matches["derivative_family"]["score"],
            "family_relationship": typed_matches["derivative_family"]["relationship"],
            "family_confidence": typed_matches["derivative_family"]["confidence"],
            "axis_matches": typed_matches,
            "statement": node.raw.get("coherent_statement") or node.raw.get("plain_statement") or node.text[:500],
        }
        rows.append(row)
        if connected:
            for axis in typed_matches.values():
                if axis["connected"]:
                    by_ref[str(axis["ref_id"])].append(row)
            if has_weak:
                weak.append(row)
        else:
            floating.append(row)

    expected_by_type: dict[str, list[str]] = defaultdict(list)
    for ref in references:
        expected_by_type[ref.ref_type].append(ref.ref_id)
    gaps = {
        ref_type: [ref_id for ref_id in ref_ids if ref_id not in by_ref]
        for ref_type, ref_ids in expected_by_type.items()
    }
    coverage = {
        ref_id: {
            "count": len(items),
            "strong": sum(1 for item in items if item["confidence"] == "strong"),
            "weak": sum(1 for item in items if item["confidence"] == "weak"),
            "top_nodes": [
                {"node_id": item["node_id"], "score": item["score"], "relationship": item["relationship"]}
                for item in sorted(items, key=lambda row: row["score"], reverse=True)[:10]
            ],
        }
        for ref_id, items in sorted(by_ref.items())
    }
    summary = {
        "node_count": len(nodes),
        "reference_count": len(references),
        "connected_count": len(rows) - len(floating),
        "floating_count": len(floating),
        "weak_connected_count": len(weak),
        "strong_connected_count": sum(1 for row in rows if row["confidence"] == "strong"),
        "relationship_counts": dict(Counter(row["relationship"] for row in rows)),
        "confidence_counts": dict(Counter(row["confidence"] for row in rows)),
        "gaps": gaps,
        "coverage": coverage,
        "floating_nodes": sorted(floating, key=lambda row: row["score"], reverse=True),
        "weak_connections": sorted(weak, key=lambda row: row["score"]),
    }
    return rows, summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "node_id", "trace_id", "connected", "relationship", "confidence",
        "best_ref_id", "best_ref_type", "best_label", "score", "second_ref_id",
        "second_score", "chain_ref_id", "chain_score", "chain_relationship",
        "chain_confidence", "proof_ref_id", "proof_score", "proof_relationship",
        "proof_confidence", "family_ref_id", "family_score", "family_relationship",
        "family_confidence", "shared_terms", "source_file", "statement",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            clean = dict(row)
            clean["shared_terms"] = ";".join(row.get("shared_terms") or [])
            writer.writerow(clean)


def write_markdown(path: Path, manifest: dict[str, Any], summary: dict[str, Any]) -> None:
    gap_lines: list[str] = []
    for ref_type, gaps in summary["gaps"].items():
        gap_lines.append(f"- `{ref_type}` gaps: `{len(gaps)}`")
        if gaps:
            gap_lines.append(f"  - {', '.join(f'`{gap}`' for gap in gaps[:30])}")
            if len(gaps) > 30:
                gap_lines.append(f"  - ... {len(gaps) - 30} more")

    floating_lines = [
        f"- `{row['node_id']}` -> nearest `{row['best_ref_id']}` score `{row['score']}`: {str(row['statement'])[:180]}"
        for row in summary["floating_nodes"][:25]
    ]
    weak_lines = [
        f"- `{row['node_id']}` -> `{row['best_ref_id']}` score `{row['score']}`: {str(row['statement'])[:180]}"
        for row in summary["weak_connections"][:25]
    ]

    body = [
        "# Chain-To-Node Audit Report",
        "",
        f"- Generated: `{manifest['generated_at']}`",
        f"- Schema: `{manifest['schema_path']}`",
        f"- Node folder: `{manifest['node_folder']}`",
        f"- Nodes read: `{summary['node_count']}`",
        f"- References read: `{summary['reference_count']}`",
        f"- Connected: `{summary['connected_count']}`",
        f"- Floating: `{summary['floating_count']}`",
        f"- Strong connected: `{summary['strong_connected_count']}`",
        f"- Weak connected: `{summary['weak_connected_count']}`",
        "",
        "Boundary: this is structural routing only. It does not prove, admit, canonize, promote, or edit any source node.",
        "",
        "## Gap Summary",
        "",
        *gap_lines,
        "",
        "## Top Floating Nodes",
        "",
        *(floating_lines or ["- None"]),
        "",
        "## Weak Connections To Review",
        "",
        *(weak_lines or ["- None"]),
        "",
        "## Output Files",
        "",
        "- `connection_map.json`",
        "- `connection_map.csv`",
        "- `connected_nodes.json`",
        "- `floating_nodes.json`",
        "- `gap_analysis.json`",
        "- `RUN_MANIFEST.json`",
    ]
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Connect extracted node JSON to chain_schema.json.")
    parser.add_argument("--schema", required=True, help="Path to chain_schema.json")
    parser.add_argument("--nodes", required=True, help="Folder containing node JSON files")
    parser.add_argument("--output-dir", required=True, help="Folder for connection reports")
    parser.add_argument("--float-threshold", type=float, default=DEFAULT_FLOAT_THRESHOLD)
    parser.add_argument("--strong-threshold", type=float, default=DEFAULT_STRONG_THRESHOLD)
    args = parser.parse_args()

    schema_path = Path(args.schema).resolve()
    node_folder = Path(args.nodes).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    schema = load_schema(schema_path)
    references = build_references(schema)
    nodes = load_nodes(node_folder)
    if not nodes:
        raise SystemExit(f"No node payloads found under {node_folder}")

    rows, summary = connect(nodes, references, args.float_threshold, args.strong_threshold)
    manifest = {
        "generated_at": now(),
        "tool": "chain_to_node_audit.py",
        "tool_version": "0.1.1",
        "schema_path": str(schema_path),
        "schema_sha256": file_sha256(schema_path),
        "node_folder": str(node_folder),
        "output_dir": str(output_dir),
        "float_threshold": args.float_threshold,
        "strong_threshold": args.strong_threshold,
        "boundary": "Structural routing only. No source node is changed; no connection is proof, admission, canonization, or a truth verdict.",
    }

    connected = [row for row in rows if row["connected"]]
    floating = [row for row in rows if not row["connected"]]
    gap_analysis = {
        "generated_at": manifest["generated_at"],
        "gaps": summary["gaps"],
        "coverage": summary["coverage"],
        "summary": {key: value for key, value in summary.items() if key not in {"coverage", "floating_nodes", "weak_connections"}},
    }

    (output_dir / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    (output_dir / "connection_map.json").write_text(json.dumps(rows, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_csv(output_dir / "connection_map.csv", rows)
    (output_dir / "connected_nodes.json").write_text(json.dumps(connected, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    (output_dir / "floating_nodes.json").write_text(json.dumps(floating, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    (output_dir / "gap_analysis.json").write_text(json.dumps(gap_analysis, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(output_dir / "RUN_REPORT.md", manifest, summary)

    # Snapshot the tool into the run folder so old runs remain reproducible.
    tool_source = Path(__file__).read_text(encoding="utf-8")
    (output_dir / "chain_to_node_audit.py").write_text(tool_source, encoding="utf-8")

    print(json.dumps({
        "output_dir": str(output_dir),
        "nodes": summary["node_count"],
        "connected": summary["connected_count"],
        "floating": summary["floating_count"],
        "gaps": {key: len(value) for key, value in summary["gaps"].items()},
    }, indent=2))


if __name__ == "__main__":
    main()
