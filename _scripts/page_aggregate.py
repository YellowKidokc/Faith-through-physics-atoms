"""Aggregate one page into repeatable Atlas map summaries.

This is intentionally independent from claim/evidence extraction. It consumes
already-admitted graph, coverage, receipt, and view-definition records.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import atlas_resolution

REPO = Path(__file__).resolve().parents[1]
VIEW_DEFINITIONS = REPO / "_atlas" / "view-definitions.json"
LANE4_LEDGER = REPO / "_ledger" / "LANE4_GLOBAL_CLAIM_LEDGER.jsonl"


def load_view_definitions(root: Path = REPO) -> dict[str, Any]:
    return json.loads((root / "_atlas" / "view-definitions.json").read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def lane4_receipts(root: Path = REPO) -> list[dict[str, Any]]:
    rows = load_jsonl(root / "_ledger" / "LANE4_GLOBAL_CLAIM_LEDGER.jsonl")
    receipts = []
    for row in rows:
        receipts.append({
            "receipt_type": "lane4",
            "atom_id": row.get("atom_id"),
            "proof_label": row.get("proof_label"),
            "current_status": row.get("current_status"),
            "limits": "Lane 4/Python/Colab receipts are evidence-bearing receipts, not automatic canon promotion.",
        })
    return receipts


def runtime_receipts(root: Path = REPO) -> list[dict[str, Any]]:
    receipts = []
    for path in sorted((root / "_runtime").rglob("*")) if (root / "_runtime").exists() else []:
        if path.is_file():
            kind = "lean" if "lean" in path.as_posix().lower() else "runtime"
            receipts.append({
                "receipt_type": kind,
                "path": path.relative_to(root).as_posix(),
                "limits": "Runtime receipt supports execution/proof discipline only within its stated assumptions.",
            })
    receipts.append({
        "receipt_type": "python",
        "path": "_scripts/test*.py",
        "limits": "Python tests support implementation behavior; they do not prove theological or empirical claims.",
    })
    receipts.append({
        "receipt_type": "colab",
        "path": "external_colab_receipt_pending",
        "limits": "Colab receipt slot is reserved; no Colab execution receipt is admitted until attached.",
    })
    return receipts


def meeting_state(projections: list[dict[str, Any]]) -> str:
    states = {str(p.get("result", "")).lower() for p in projections if p.get("mode") == "meeting"}
    if any("contradict" in s for s in states):
        return "CONTRADICTED"
    if any("converged" in s for s in states):
        return "CONVERGED"
    if any("partial" in s for s in states):
        return "UNRESOLVED"
    return "UNRESOLVED"


def aggregate_page(source: Path, root: Path = REPO) -> dict[str, Any]:
    atlas = atlas_resolution.build_atlas(root)
    views = load_view_definitions(root)
    source_rel = source.resolve().relative_to(root.resolve()).as_posix()
    related_atoms = {
        atom_id: atom for atom_id, atom in atlas.atoms.items()
        if atom.get("_path") == source_rel or atom_id in source.read_text(encoding="utf-8", errors="replace")
    }
    if not related_atoms and source.suffix.lower() == ".html":
        related_atoms = {atom_id: atom for atom_id, atom in atlas.atoms.items() if atom_id in source.read_text(encoding="utf-8", errors="replace")}

    projections = [p for rows in atlas.projections_by_claim.values() for p in rows]
    evidence_rows = [e for rows in atlas.evidence_by_claim.values() for e in rows]
    map_summaries = []
    for key, view in views["maps"].items():
        map_summaries.append({
            "map_id": key,
            "question": view["question"],
            "layout": view["layout"],
            "include_edges": view["include_edges"],
            "status": meeting_state(projections) if key == "meeting_map" else "defined",
        })

    warnings = []
    if not related_atoms:
        warnings.append("No direct claim atom was matched to this page; aggregation used global Atlas context only.")
    if meeting_state(projections) == "CONTRADICTED":
        warnings.append("Meeting Map contains CONTRADICTED state; bridge or claim suspension review is required.")

    return {
        "page_id": source.stem,
        "source": source_rel,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": f"Aggregated {len(related_atoms)} directly related claim atoms, {len(evidence_rows)} evidence coverage records, and {len(projections)} projection records into {len(map_summaries)} map views.",
        "maps": map_summaries,
        "receipts": lane4_receipts(root) + runtime_receipts(root),
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate a page into repeatable Atlas map summaries")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = aggregate_page(args.source.resolve())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
