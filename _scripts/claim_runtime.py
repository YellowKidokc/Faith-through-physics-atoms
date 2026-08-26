#!/usr/bin/env python3
"""Live claim intake and framework graph export.

This is the thin runtime layer David described:

1. Pull claim-like sentences from a paper or topbar packet.
2. Classify each sentence against the existing atom graph.
3. Append stable records to a live JSONL ledger.
4. Export the underlying nodes as JSON, Mermaid, or a simple HTML mind map.

No external API is required. This is the local reference implementation the
API layer can call later.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ATOM_DIRS = [
    REPO / "axioms" / "01_canonical",
    REPO / "master-equation" / "01_canonical",
]
RUNTIME = REPO / "_runtime"
LEDGER = RUNTIME / "live_claim_ledger.jsonl"
GRAPH_JSON = RUNTIME / "framework_graph.json"
GRAPH_MMD = RUNTIME / "framework_mindmap.mmd"
GRAPH_HTML = RUNTIME / "framework_mindmap.html"

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "because", "but", "by",
    "can", "for", "from", "has", "have", "if", "in", "into", "is", "it",
    "its", "not", "of", "on", "or", "rather", "so", "than", "that", "the",
    "their", "then", "there", "this", "to", "under", "when", "where", "with",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def strip_html(text: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"</(h[1-6]|p|li|div|section|article)>", ". ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def words(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", text.lower())
        if token not in STOPWORDS
    }


def stable_id(prefix: str, text: str) -> str:
    digest = hashlib.sha1(normalize_space(text).lower().encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def atom_paths() -> list[Path]:
    paths: list[Path] = []
    for directory in ATOM_DIRS:
        if directory.exists():
            paths.extend(sorted(directory.glob("*.jsonld")))
    return paths


def load_atoms() -> list[dict[str, Any]]:
    atoms = []
    for path in atom_paths():
        try:
            atom = read_json(path)
        except json.JSONDecodeError:
            continue
        atom["_path"] = str(path.relative_to(REPO))
        atoms.append(atom)
    return atoms


def atom_text(atom: dict[str, Any]) -> str:
    parts = [
        atom.get("name", ""),
        atom.get("statementPlain", ""),
        atom.get("statementTechnical", ""),
        atom.get("mathematicalForm", ""),
        " ".join(atom.get("tags", [])),
        " ".join(atom.get("keywords", [])),
    ]
    return " ".join(str(part) for part in parts if part)


def atom_index(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    indexed = []
    for atom in atoms:
        bag = words(atom_text(atom))
        indexed.append({"atom": atom, "words": bag})
    return indexed


def load_source(path: Path) -> tuple[str, dict[str, Any] | None]:
    if path.suffix.lower() == ".json":
        packet = read_json(path)
        chunks = []
        page = packet.get("page", {})
        if isinstance(page, dict):
            chunks.extend(str(page.get(key, "")) for key in ("title", "subtitle", "kicker"))
        for claim in packet.get("claims", []):
            if isinstance(claim, dict):
                chunks.extend(
                    str(claim.get(key, ""))
                    for key in ("sentence", "formal", "killCondition")
                )
                chunks.extend(str(step) for step in claim.get("derivation", []))
        for proof in packet.get("proofs", []):
            if isinstance(proof, dict):
                chunks.extend(str(proof.get(key, "")) for key in ("title", "summary"))
        for unit in packet.get("mtl", []):
            if isinstance(unit, dict):
                chunks.extend(
                    str(unit.get(key, ""))
                    for key in ("title", "equation", "wordEquation", "structuralInsight", "plain", "influence")
                )
        for term in packet.get("terms", []):
            if isinstance(term, dict):
                chunks.extend(str(term.get(key, "")) for key in ("label",))
                front = term.get("front", {})
                back = term.get("back", {})
                if isinstance(front, dict):
                    chunks.extend(str(front.get(key, "")) for key in ("subtitle", "equation", "summary"))
                if isinstance(back, dict):
                    chunks.extend(str(back.get(key, "")) for key in ("eyebrow",))
        layers = packet.get("reader_layers", {})
        if isinstance(layers, dict):
            chunks.extend(strip_html(str(value)) for value in layers.values())
        text = " ".join(chunks) if chunks else json.dumps(packet, ensure_ascii=False)
        return text, packet
    return read_text(path), None


def extract_claim_sentences(text: str, limit: int = 80) -> list[str]:
    text = strip_html(text)
    pieces = re.split(r"(?<=[.!?])\s+", normalize_space(text))
    claims = []
    claim_markers = re.compile(
        r"\b(is|are|must|cannot|requires?|implies|therefore|because|means|proves?|shows?|collapses?|depends?|predicts?)\b",
        re.I,
    )
    for piece in pieces:
        sentence = normalize_space(piece)
        sentence = re.sub(r"^(The Idea, Simply|The Argument|The Formal Statement)\s+", "", sentence).strip()
        if len(sentence) < 45 or len(sentence) > 420:
            continue
        if claim_markers.search(sentence):
            claims.append(sentence)
        if len(claims) >= limit:
            break
    return list(dict.fromkeys(claims))


def classify(sentence: str, indexed_atoms: list[dict[str, Any]], top_n: int = 5) -> dict[str, Any]:
    sw = words(sentence)
    scored = []
    for row in indexed_atoms:
        aw = row["words"]
        overlap = sw & aw
        if not overlap:
            continue
        denom = max(1, min(len(sw), len(aw)))
        score = len(overlap) / denom
        atom = row["atom"]
        scored.append(
            {
                "nodeID": atom.get("nodeID"),
                "claimID": atom.get("claimID"),
                "name": atom.get("name"),
                "domainType": atom.get("domainType"),
                "claimClass": atom.get("claimClass"),
                "status": atom.get("status"),
                "score": round(score, 3),
                "overlap": sorted(overlap)[:20],
                "path": atom.get("_path"),
            }
        )
    scored.sort(key=lambda item: (-item["score"], str(item.get("nodeID"))))
    best = scored[:top_n]
    if not best:
        verdict = "unmapped-candidate"
    elif best[0]["score"] >= 0.45:
        verdict = "likely-existing-atom"
    elif best[0]["score"] >= 0.25:
        verdict = "needs-review"
    else:
        verdict = "weak-match"
    return {"verdict": verdict, "matches": best}


def existing_ledger_ids() -> set[str]:
    if not LEDGER.exists():
        return set()
    ids = set()
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("runtimeClaimID"):
            ids.add(record["runtimeClaimID"])
    return ids


def intake(path: Path, limit: int = 80) -> list[dict[str, Any]]:
    text, packet = load_source(path)
    atoms = load_atoms()
    indexed = atom_index(atoms)
    source_atoms = []
    if packet and isinstance(packet.get("page"), dict):
        source_atoms = [str(x) for x in packet["page"].get("sourceAtoms", [])]

    seen = existing_ledger_ids()
    records = []
    now = datetime.now(timezone.utc).isoformat()
    for sentence in extract_claim_sentences(text, limit=limit):
        rid = stable_id("RTC", sentence)
        result = classify(sentence, indexed)
        record = {
            "runtimeClaimID": rid,
            "createdAt": now,
            "source": str(path),
            "sentence": sentence,
            "classification": result["verdict"],
            "sourceAtoms": source_atoms,
            "matches": result["matches"],
            "status": "logged" if result["verdict"] != "unmapped-candidate" else "candidate",
        }
        records.append(record)

    RUNTIME.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as fh:
        for record in records:
            if record["runtimeClaimID"] in seen:
                continue
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            seen.add(record["runtimeClaimID"])
    return records


def graph_from_atoms() -> dict[str, Any]:
    atoms = load_atoms()
    nodes = []
    edges = []
    for atom in atoms:
        node_id = atom.get("nodeID") or atom.get("@id") or atom.get("claimID")
        if not node_id:
            continue
        nodes.append(
            {
                "id": node_id,
                "label": atom.get("name") or node_id,
                "domainType": atom.get("domainType", ""),
                "claimClass": atom.get("claimClass", ""),
                "status": atom.get("status", ""),
                "path": atom.get("_path", ""),
            }
        )
        for edge in atom.get("edges", []):
            if isinstance(edge, dict) and edge.get("target"):
                edges.append(
                    {
                        "source": node_id,
                        "target": edge.get("target"),
                        "type": edge.get("type", "edge"),
                        "propagates": bool(edge.get("propagates")),
                    }
                )
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "nodes": nodes,
        "edges": edges,
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges),
            "byDomain": dict(Counter(node["domainType"] for node in nodes)),
            "byClass": dict(Counter(node["claimClass"] for node in nodes)),
            "byStatus": dict(Counter(node["status"] for node in nodes)),
        },
    }


def mermaid_mindmap(graph: dict[str, Any]) -> str:
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph["nodes"]:
        by_domain[node.get("domainType") or "unclassified"].append(node)

    lines = ["mindmap", "  root((Theophysics Atom Graph))"]
    for domain in sorted(by_domain):
        lines.append(f"    {safe_mmd(domain)}")
        by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for node in by_domain[domain]:
            by_class[node.get("claimClass") or "claim"].append(node)
        for claim_class in sorted(by_class):
            lines.append(f"      {safe_mmd(claim_class)}")
            for node in sorted(by_class[claim_class], key=lambda item: str(item["label"]))[:24]:
                label = str(node["label"])
                if len(label) > 70:
                    label = label[:67] + "..."
                lines.append(f"        {safe_mmd(label)}")
    return "\n".join(lines) + "\n"


def safe_mmd(text: str) -> str:
    cleaned = re.sub(r"[\r\n\t]+", " ", str(text)).strip()
    cleaned = cleaned.replace("(", "[").replace(")", "]").replace(":", " -")
    return cleaned or "unnamed"


def html_mindmap(graph: dict[str, Any]) -> str:
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph["nodes"]:
        by_domain[node.get("domainType") or "unclassified"].append(node)
    sections = []
    for domain in sorted(by_domain):
        class_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for node in by_domain[domain]:
            class_groups[node.get("claimClass") or "claim"].append(node)
        body = []
        for claim_class in sorted(class_groups):
            items = "\n".join(
                f"<li><b>{html.escape(str(node['label']))}</b><small>{html.escape(str(node['status']))} · {html.escape(str(node['id']))}</small></li>"
                for node in sorted(class_groups[claim_class], key=lambda item: str(item["label"]))
            )
            body.append(f"<details open><summary>{html.escape(claim_class)} ({len(class_groups[claim_class])})</summary><ul>{items}</ul></details>")
        sections.append(f"<details open><summary>{html.escape(domain)} ({len(by_domain[domain])})</summary>{''.join(body)}</details>")
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Theophysics Atom Mind Map</title>
<style>
body {{ margin: 0; font: 15px/1.45 system-ui, Segoe UI, sans-serif; background: #101418; color: #edf2f7; }}
main {{ max-width: 1180px; margin: 0 auto; padding: 28px; }}
h1 {{ font-size: 26px; margin: 0 0 6px; }}
p {{ color: #aebdcc; margin: 0 0 18px; }}
details {{ margin: 8px 0; border-left: 2px solid #3caea3; padding-left: 12px; }}
summary {{ cursor: pointer; font-weight: 700; color: #f6d365; }}
ul {{ margin: 8px 0 14px; padding-left: 22px; }}
li {{ margin: 6px 0; }}
small {{ display: block; color: #91a4b7; }}
</style>
<main>
<h1>Theophysics Atom Mind Map</h1>
<p>{graph["counts"]["nodes"]} nodes · {graph["counts"]["edges"]} edges · generated {html.escape(graph["generatedAt"])}</p>
{''.join(sections)}
</main>
</html>
"""


def export_graph() -> dict[str, Path]:
    graph = graph_from_atoms()
    write_text(GRAPH_JSON, json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    write_text(GRAPH_MMD, mermaid_mindmap(graph))
    write_text(GRAPH_HTML, html_mindmap(graph))
    return {"json": GRAPH_JSON, "mermaid": GRAPH_MMD, "html": GRAPH_HTML}


def main() -> int:
    parser = argparse.ArgumentParser(description="Live claim ledger and framework mind-map runtime.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_intake = sub.add_parser("intake", help="Extract, classify, and log claims from a source file.")
    p_intake.add_argument("source", type=Path)
    p_intake.add_argument("--limit", type=int, default=80)

    sub.add_parser("graph", help="Export framework graph JSON, Mermaid, and HTML mind map.")

    args = parser.parse_args()
    if args.command == "intake":
        records = intake(args.source, limit=args.limit)
        counts = Counter(record["classification"] for record in records)
        print(f"[ok] inspected={len(records)} ledger={LEDGER}")
        for key, value in sorted(counts.items()):
            print(f"[ok] {key}={value}")
        return 0

    if args.command == "graph":
        outputs = export_graph()
        for kind, path in outputs.items():
            print(f"[ok] {kind}={path}")
        return 0

    return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
