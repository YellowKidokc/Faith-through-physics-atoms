#!/usr/bin/env python3
"""Compare deterministic candidate routing with receipt-backed API mappings.

Agreement means only that two methods selected the same declared reference for a
node and stage. It is not a truth, proof, or canon result.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def api_reference(stage: str, result: dict[str, Any]) -> str | None:
    if stage == "chain" and result.get("chain_step") is not None:
        return f"chain:{result['chain_step']}"
    if stage == "proof_stack" and result.get("proof_step_id"):
        return f"proof:{result['proof_step_id']}"
    if stage == "derivative_families" and result.get("family_symbol"):
        return f"family:{result['family_symbol']}"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Rosetta deterministic and API connector runs.")
    parser.add_argument("--deterministic-map", required=True, help="connection_map.json from chain_to_node_audit.py")
    parser.add_argument("--api-receipts", required=True, help="receipts folder from run_rosetta_connector.py")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    deterministic_path = Path(args.deterministic_map).resolve()
    api_dir = Path(args.api_receipts).resolve()
    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)

    deterministic = {
        row["node_id"]: row
        for row in json.loads(deterministic_path.read_text(encoding="utf-8"))
    }
    api_rows: list[dict[str, Any]] = []
    for path in sorted(api_dir.glob("*.json")):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        stage = receipt.get("stage")
        node_id = receipt.get("node_id")
        result = receipt.get("result", {})
        if stage and node_id:
            api_rows.append({
                "node_id": node_id,
                "stage": stage,
                "api_reference": api_reference(stage, result),
                "api_relationship": result.get("relationship", result.get("role")),
                "api_confidence": result.get("confidence"),
                "receipt": str(path),
            })

    comparisons: list[dict[str, Any]] = []
    for api in api_rows:
        candidate = deterministic.get(api["node_id"])
        deterministic_field = {
            "chain": "chain_ref_id",
            "proof_stack": "proof_ref_id",
            "derivative_families": "family_ref_id",
        }[api["stage"]]
        deterministic_score_field = {
            "chain": "chain_score",
            "proof_stack": "proof_score",
            "derivative_families": "family_score",
        }[api["stage"]]
        deterministic_ref = candidate.get(deterministic_field) if candidate else None
        if not candidate:
            outcome = "missing_deterministic_node"
        elif not api["api_reference"]:
            outcome = "api_floating"
        elif not deterministic_ref:
            outcome = "missing_deterministic_stage_candidate"
        elif deterministic_ref == api["api_reference"]:
            outcome = "same_candidate"
        else:
            outcome = "different_candidate"
        comparisons.append({
            **api,
            "deterministic_reference": deterministic_ref,
            "deterministic_relationship": candidate.get("relationship") if candidate else None,
            "deterministic_confidence": candidate.get("confidence") if candidate else None,
            "deterministic_score": candidate.get(deterministic_score_field) if candidate else None,
            "outcome": outcome,
        })

    report = {
        "generated_at": now(),
        "boundary": "Comparison only. Agreement is not proof, admission, canonization, or a truth verdict.",
        "deterministic_map": str(deterministic_path),
        "api_receipts": str(api_dir),
        "deterministic_nodes": len(deterministic),
        "api_stage_results": len(comparisons),
        "outcomes": dict(Counter(row["outcome"] for row in comparisons)),
        "comparisons": comparisons,
    }
    (output / "CONNECTOR_COMPARISON.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Rosetta Connector Comparison",
        "",
        f"- Deterministic nodes available: `{len(deterministic)}`",
        f"- API stage results compared: `{len(comparisons)}`",
        f"- Outcomes: `{report['outcomes']}`",
        "",
        "Agreement means two routing methods selected the same declared reference. It is not proof or a verdict.",
        "",
        "## Results",
        "",
    ]
    for row in comparisons:
        lines.append(f"- `{row['node_id']}` / `{row['stage']}`: `{row['outcome']}`; deterministic `{row['deterministic_reference']}`, API `{row['api_reference']}`")
    (output / "COMPARISON_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "outcomes": report["outcomes"]}, indent=2))


if __name__ == "__main__":
    main()
