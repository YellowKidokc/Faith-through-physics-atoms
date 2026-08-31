#!/usr/bin/env python3
"""Continue Stage 1 by decomposing a bundled source into neutral components."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("claim_pipeline_service", HERE / "claim_pipeline_service.py")
service = importlib.util.module_from_spec(spec); spec.loader.exec_module(service)

SYSTEM = """You are continuing Stage 1 of the Faith Through Physics claim pipeline after a bundled paper returned DISCOVERY_INCOMPLETE.

Decompose the source into the smallest assertions that can receive one epistemic ruling without forcing that ruling onto another assertion. This is dependency exposure, not paraphrase and not classification.

You may arrange components into coherent future paper families, but you must not assign disciplines, object types, warrant classes, evidence grades, IC grades, bridge grades, truth rulings, or canonical status. Preserve the author's disclosed Christian premise as content without treating it as either proved or disproved. Separate an assertion from its interpretation, application, model, analogy, and identification whenever they could fail independently.

Return valid JSON only with exactly:
- schema_version = claim-component-catalog/1.0.0
- stage = NON_DISCRIMINATORY_COMPONENT_DISCOVERY
- status = COMPONENT_DISCOVERY_COMPLETE, COMPONENT_DISCOVERY_INCOMPLETE, or BLOCKED
- source {path, sha256}
- decomposition_rule
- paper_families: array of {family_id, working_title, central_question, component_ids, opening_debt, closing_debt}
- components: array of {component_id, exact_assertion, plain_assertion, source_heading, source_line_start, verbatim_anchor, depends_on, must_not_be_bundled_with, negation_or_rival, defeat_or_narrowing_condition, open_questions}
- unresolved_boundaries array
- prohibited_outputs array

Use 8-10 paper families and 20-24 top-level components. Component IDs must be AXG-C001, AXG-C002, and so on. Family IDs must be AXG-P01, AXG-P02, and so on. Every component must appear in exactly one family. Source lines and anchors must be grounded in the supplied numbered source. Keep anchors under 18 words. Keep every string under 24 words. Use at most two dependencies, two non-bundling references, and one open question per component. This is a top-level joint catalog; later recursion may open each component further. Finish the complete JSON object."""


def numbered(text: str) -> str:
    return "\n".join(f"{i}: {line}" for i, line in enumerate(text.splitlines(), 1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--discovery-receipt", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="deepseek-chat")
    args = parser.parse_args()

    source = Path(args.source).resolve(); receipt_path = Path(args.discovery_receipt).resolve(); output = Path(args.output_dir).resolve()
    text = source.read_text(encoding="utf-8", errors="replace")
    source_hash = "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    discovery = receipt["stages"][0]
    if discovery["status"] != "DISCOVERY_INCOMPLETE":
        raise SystemExit("Component discovery requires a DISCOVERY_INCOMPLETE upstream receipt")
    payload = {
        "source": {"path": str(source), "sha256": source_hash, "numbered_content": numbered(text)},
        "upstream_discovery": {"receipt_path": str(receipt_path), "receipt_hash": service.sha(receipt), "output": discovery["output"]},
    }
    catalog = service.call_deepseek(SYSTEM, payload, args.model)
    required = ["schema_version","stage","status","source","decomposition_rule","paper_families","components","unresolved_boundaries","prohibited_outputs"]
    service.require_fields(catalog, required, "component catalog")
    if catalog["source"]["sha256"] != source_hash:
        raise SystemExit("Component catalog did not preserve the source hash")
    component_ids = [item["component_id"] for item in catalog["components"]]
    assigned = [cid for family in catalog["paper_families"] for cid in family["component_ids"]]
    if len(component_ids) != len(set(component_ids)):
        raise SystemExit("Duplicate component IDs returned")
    if sorted(component_ids) != sorted(assigned) or len(assigned) != len(set(assigned)):
        raise SystemExit("Every component must appear in exactly one paper family")
    envelope = {
        "receipt_version": "claim-component-discovery-receipt/1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "provider": "deepseek",
        "model": args.model,
        "source_hash": source_hash,
        "upstream_receipt_hash": service.sha(receipt),
        "catalog_hash": service.sha(catalog),
        "canonical_promotion_performed": False,
        "catalog": catalog,
    }
    output.mkdir(parents=True, exist_ok=True)
    path = output / "AX-GND_v2.component-catalog.deepseek.json"
    path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": catalog["status"], "families": len(catalog["paper_families"]), "components": len(catalog["components"]), "path": str(path), "catalog_hash": envelope["catalog_hash"]}, indent=2))


if __name__ == "__main__": main()
