#!/usr/bin/env python3
"""Project one passing claim-pipeline receipt into a governed Canonization candidate record."""
from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import jsonschema


NAMESPACE = uuid.UUID("8c12b5bb-445e-4d87-b789-5f9e19aac32c")


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def stage(receipt: dict, name: str) -> dict:
    return next(item for item in receipt["stages"] if item["name"] == name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--source-hash", required=True)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    receipt_bytes = args.receipt.read_bytes()
    receipt = json.loads(receipt_bytes)
    if receipt.get("final_status") != "PASS":
        raise SystemExit("Only a PASS pipeline receipt can become an importable candidate record.")
    if receipt.get("canonical_promotion_performed") is not False:
        raise SystemExit("Receipt violated the no-promotion boundary.")

    discovery_stage = stage(receipt, "discovery")
    classification_stage = stage(receipt, "classification")
    reconciliation_stage = stage(receipt, "reconciliation")
    discovery = discovery_stage["output"]
    classification = classification_stage["output"]
    reconciliation = reconciliation_stage["output"]
    capsule = receipt.get("capsule") or {}
    statement = reconciliation.get("native_statement") or discovery["raw_expression"]

    source_hash = args.source_hash
    if not source_hash.startswith("sha256:"):
        source_hash = "sha256:" + source_hash
    record_id = str(uuid.uuid5(NAMESPACE, source_hash + "|" + statement))
    atom_id = str(uuid.uuid5(uuid.UUID(record_id), "native-claim"))
    now = datetime.now(timezone.utc).isoformat()

    record = {
        "schemaVersion": "1.0.0",
        "recordId": record_id,
        "statusLabel": "CANDIDATE_DRAFT  NOT ADMITTED",
        "workflowState": "Candidate",
        "source": {
            "sourceId": str(args.source),
            "contentHash": source_hash,
            "coordinates": {"path": str(args.source), "discoveryReceipt": str(args.receipt)},
            "title": args.source.stem,
        },
        "created": {"at": now, "by": "pipeline-receipt-adapter"},
        "updated": {"at": now, "by": "pipeline-receipt-adapter"},
        "protectedBlindDiscovery": {
            "immutable": True,
            "recordedAt": receipt["created_at"],
            "inputPolicy": "SOURCE_CONTENT_ONLY_NO_INHERITED_METADATA",
            "result": discovery,
        },
        "recoveredObjects": [{
            "id": atom_id,
            "kind": classification.get("object_type", "CLAIM"),
            "statement": statement,
            "supportStatus": "candidate_unverified",
            "sourceCoordinates": {"sourceId": str(args.source)},
        }],
        "claims": [{
            "id": atom_id,
            "kind": classification.get("claim_species", "CLAIM"),
            "statement": statement,
            "supportStatus": classification.get("why_outcome", "WHY_OPEN"),
            "sourceCoordinates": {"sourceId": str(args.source)},
        }],
        "blindClassification": [{
            "objectId": atom_id,
            "labels": [
                classification.get("object_type", ""),
                classification.get("register", ""),
                classification.get("claim_species", ""),
                classification.get("warrant_class", ""),
                classification.get("why_outcome", ""),
            ],
            "burdens": classification.get("burdens", []),
            "unresolved": classification.get("unresolved", []),
        }],
        "comparison": {"pipelineClassification": classification},
        "reconciliationProposal": reconciliation,
        "countermodels": [
            {"id": str(uuid.uuid5(uuid.UUID(record_id), f"countermodel-{index}")), "kind": "COUNTERMODEL", "statement": value}
            for index, value in enumerate(discovery.get("countermodels", []), 1)
        ],
        "openGaps": [
            {"id": str(uuid.uuid5(uuid.UUID(record_id), f"gap-{index}")), "kind": "OPEN_GAP", "statement": value}
            for index, value in enumerate(classification.get("unresolved", []), 1)
        ],
        "admissionEventReference": None,
        "provenance": [{
            "actor": "deepseek-chat",
            "action": "three-call candidate pipeline",
            "receipt": str(args.receipt),
            "humanRulingRequired": True,
        }],
        "hashes": {
            "source": source_hash,
            "capsule": receipt["capsule_hash"],
            "discovery": discovery_stage["hash"],
            "classification": classification_stage["hash"],
            "reconciliation": reconciliation_stage["hash"],
            "pipelineReceipt": sha256_bytes(receipt_bytes),
        },
    }
    record["blindClassification"][0]["labels"] = [
        label for label in record["blindClassification"][0]["labels"] if label
    ]

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    jsonschema.validate(record, schema, format_checker=jsonschema.FormatChecker())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "VALID_CANDIDATE_RECORD",
        "record_id": record_id,
        "output": str(args.output),
        "workflow_state": "Candidate",
        "admission_performed": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
