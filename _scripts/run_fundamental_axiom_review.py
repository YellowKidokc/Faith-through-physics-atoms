#!/usr/bin/env python3
"""Validate and review fundamental-axiom candidates without admitting them."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

STATUS_STAMP = "CANDIDATE_DRAFT — NOT ADMITTED"
EXACT_A0 = "The Triune God is."


def load_pipeline():
    path = Path(__file__).with_name("claim_pipeline_service.py")
    spec = importlib.util.spec_from_file_location("claim_pipeline_service", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def validate_manifest(data: dict) -> list[str]:
    errors: list[str] = []
    rows = data.get("candidates")
    if not isinstance(rows, list) or not rows:
        return ["candidates must be a nonempty array"]
    ids = [row.get("id") for row in rows]
    if any(not isinstance(item, str) or not item.strip() for item in ids):
        errors.append("every candidate requires a nonempty string id")
    if len(ids) != len(set(ids)):
        errors.append("candidate ids must be unique")
    known = set(ids)
    root = data.get("root_id")
    if root not in known:
        errors.append("root_id must identify a candidate")
    required = {"id", "title", "statement", "plain_language", "claim_type", "warrant_intent", "depends_on", "defeat_condition", "open_items"}
    for row in rows:
        missing = sorted(required - set(row))
        if missing:
            errors.append(f"{row.get('id', '<unknown>')}: missing {', '.join(missing)}")
        for dep in row.get("depends_on", []):
            if dep not in known:
                errors.append(f"{row.get('id')}: unknown dependency {dep}")
        if row.get("id") == root and row.get("depends_on"):
            errors.append(f"{root}: governing root may not have incoming dependencies")
    graph = {row["id"]: list(row.get("depends_on", [])) for row in rows if row.get("id") in known}
    visiting, visited = set(), set()
    def walk(node: str):
        if node in visiting:
            errors.append(f"dependency cycle detected at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, []):
            walk(dep)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        walk(node)
    if data.get("status") != "CANDIDATE_DRAFT_NOT_ADMITTED":
        errors.append("manifest status must remain CANDIDATE_DRAFT_NOT_ADMITTED")
    root_rows = [row for row in rows if row.get("id") == "A0"]
    if len(root_rows) != 1 or root_rows[0].get("statement") != EXACT_A0:
        errors.append(f"A0 must exist exactly once and remain exactly: {EXACT_A0}")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--provider", choices=("mock", "deepseek"), default="mock")
    parser.add_argument("--model", default="deepseek-chat")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    output = Path(args.output_dir).resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = validate_manifest(data)
    if errors:
        print(json.dumps({"status": "BLOCKED", "errors": errors}, indent=2))
        return 2

    pipeline = load_pipeline()
    definition_ids = {"D-EXISTENCE":"DEF-EXISTENCE", "D-DISTINCTION":"DEF-DISTINCTION", "D-RELATION":"DEF-RELATION"}
    language_bundle = {
        "definitions": [
            {"definition_id":definition_ids[row["id"]], "version":row.get("version", "0.1.0"), "canonical_term":row["title"].replace(" Definition", ""), "aliases":[], "forbidden_equivalences":[]}
            for row in data["candidates"] if row["id"] in definition_ids
        ],
        "symbols": [],
        "dependency_objects": [{"id":row["id"], "dependencies":row["depends_on"]} for row in data["candidates"]],
    }
    receipt_dir = output / "_receipts"
    packet_dir = output / "_candidate_packets"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    packet_dir.mkdir(parents=True, exist_ok=True)
    pipeline.RUNS = receipt_dir
    results = []
    for row in data["candidates"]:
        capsule = {
            "operation": "new_claim",
            "claim": row["statement"],
            "plain_language": row["plain_language"],
            "claim_type": row["claim_type"],
            "defeat_condition": row["defeat_condition"],
            "present_evidence": [],
            "open_items": row["open_items"],
            "canonical_promotion_requested": False,
            "canonical_language_enabled": True,
            "source_object_id": row["id"],
            "candidate_version": row.get("version", "0.1.0"),
            "depends_on": row["depends_on"],
            "warrant_intent": row["warrant_intent"],
            "canonical_language_registry_bundle": language_bundle,
        }
        receipt = pipeline.review(capsule, args.provider, args.model)
        packet = {
            "packet_version": "fundamental-axiom-candidate/1.1.0",
            "status": STATUS_STAMP,
            "id": row["id"],
            "candidate_version": row.get("version", "0.1.0"),
            "title": row["title"],
            "declared_warrant_intent": row["warrant_intent"],
            "depends_on": row["depends_on"],
            "lifecycle": "candidate",
            "admission_event": None,
            "canonical_admission": False,
            "review_card": {
                "exact_claim": row["statement"],
                "plain_language_meaning": row["plain_language"],
                "object_type_and_register": {
                    "declared_claim_type": row["claim_type"],
                    "declared_warrant_intent": row["warrant_intent"],
                    "automated_object_type": receipt["stages"][1]["output"].get("object_type") if len(receipt["stages"]) > 1 else None,
                    "automated_register": receipt["stages"][1]["output"].get("register") if len(receipt["stages"]) > 1 else None,
                },
                "warrant": row["warrant_intent"],
                "dependencies": row["depends_on"],
                "supporting_material": row.get("supporting_material", []),
                "defeat_conditions": [row["defeat_condition"]],
                "open_matters": row["open_items"],
                "countermodels_and_objections": row.get("countermodels_and_objections", []),
                "automated_review_results": {
                    "provider": receipt["provider"],
                    "model": receipt["model"],
                    "final_status": receipt["final_status"],
                    "receipt_path": receipt["receipt_path"],
                },
                "kimi_exact_criticism": [],
                "proposed_response": [],
                "human_decision": None,
                "canonical_language": receipt.get("canonical_language_resolution"),
            },
            "kimi_review": {
                "state": "NOT_SUPPLIED",
                "affected": False,
                "objection_ids": [],
                "finalization_blocked": False,
            },
            "candidate_approval": None,
            "review_receipt": receipt,
        }
        packet_bytes = json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        packet["candidate_packet_hash"] = "sha256:" + hashlib.sha256(packet_bytes).hexdigest()
        path = packet_dir / f"{row['id']}.candidate.json"
        path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        results.append({"id": row["id"], "status": receipt["final_status"], "packet": str(path)})

    summary = {
        "run_version": "fundamental-axiom-review/1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "provider": args.provider,
        "manifest": str(manifest_path),
        "manifest_sha256": "sha256:" + hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "deterministic_validation": "PASS",
        "results": results,
        "canonical_promotion_performed": False,
        "human_ruling_required": True,
    }
    summary_path = receipt_dir / "RUN_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if all(row["status"] == "PASS" for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
