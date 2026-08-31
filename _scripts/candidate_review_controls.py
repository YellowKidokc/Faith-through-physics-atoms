#!/usr/bin/env python3
"""Fail-closed candidate review, immutable Kimi intake, and human ruling controls."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

STATUS = "CANDIDATE_DRAFT — NOT ADMITTED"
DECISIONS = {"APPROVE CANDIDATE", "REVISE", "SPLIT", "HOLD OPEN", "WITHDRAW", "REJECT"}
REQUIRED_ADMISSION = {"actor", "date", "rationale", "source_hashes", "candidate_hash", "unresolved_fields", "downstream_impact", "signed_admission_receipt"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def validate_packet(packet: dict) -> list[str]:
    errors: list[str] = []
    if packet.get("status") != STATUS:
        errors.append("exact candidate status stamp is required")
    if packet.get("lifecycle") != "candidate" or packet.get("canonical_admission") is not False or packet.get("admission_event") is not None:
        errors.append("candidate/admission state is contradictory")
    if packet.get("id") == "A0" and packet.get("review_card", {}).get("exact_claim") != "The Triune God is.":
        errors.append("A0 wording changed")
    card = packet.get("review_card")
    required = {"exact_claim", "plain_language_meaning", "object_type_and_register", "warrant", "dependencies", "supporting_material", "defeat_conditions", "open_matters", "automated_review_results", "kimi_exact_criticism", "proposed_response", "human_decision"}
    if not isinstance(card, dict) or required - set(card):
        errors.append("review card is incomplete")
    kimi = packet.get("kimi_review", {})
    if kimi.get("affected") and kimi.get("state") != "ADJUDICATED" and not kimi.get("finalization_blocked"):
        errors.append("Kimi-affected candidate must remain blocked until adjudicated")
    decision = packet.get("candidate_approval")
    if decision is not None and decision.get("decision") not in DECISIONS:
        errors.append("invalid candidate decision")
    return errors


def validate_run(root: Path) -> dict:
    results = []
    for path in sorted((root / "_candidate_packets").glob("*.candidate.json")):
        errors = validate_packet(read_json(path))
        results.append({"path": str(path), "status": "PASS" if not errors else "BLOCKED", "errors": errors})
    if not results:
        results.append({"path": str(root / "_candidate_packets"), "status": "BLOCKED", "errors": ["no candidate packets found"]})
    receipt = {"status": "PASS" if all(x["status"] == "PASS" for x in results) else "BLOCKED", "checked_at": now(), "results": results, "canonical_admission_performed": False}
    folder = root / "_receipts"; folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"VALIDATION_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt["receipt_path"] = str(path)
    return receipt


def import_kimi(root: Path, source: Path) -> dict:
    raw = source.read_bytes()
    source_hash = digest(raw)
    intake = root / "_kimi_intake"
    preserved = intake / "preserved_sources"
    ledgers = intake / "objection_ledgers"
    receipts = intake / "receipts"
    for folder in (preserved, ledgers, receipts):
        folder.mkdir(parents=True, exist_ok=True)
    stored = preserved / f"{source_hash.split(':')[1]}__{source.name}"
    if stored.exists() and stored.read_bytes() != raw:
        raise ValueError("immutable Kimi source collision")
    if not stored.exists():
        shutil.copyfile(source, stored)
    objection_id = "KIMI-" + source_hash.split(":")[1][:12].upper() + "-UNMAPPED-001"
    ledger = {
        "schema_version": "kimi-objection-ledger/1.0.0", "status": STATUS,
        "source": {"original_path": str(source.resolve()), "preserved_path": str(stored), "sha256": source_hash, "immutable": True},
        "objections": [{"objection_id": objection_id, "exact_wording": raw.decode("utf-8", errors="replace"), "mapping_status": "OPEN — UNMAPPED", "candidate_links": [], "proposed_responses": [], "david_ruling": None}],
        "canonical_admission_performed": False,
    }
    ledger_path = ledgers / f"{source_hash.split(':')[1]}.objections.json"
    if not ledger_path.exists():
        ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"event": "KIMI_IMMUTABLE_INTAKE", "created_at": now(), "source_sha256": source_hash, "preserved_path": str(stored), "ledger_path": str(ledger_path), "canonical_admission_performed": False}
    receipt_path = receipts / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{source_hash.split(':')[1][:12]}.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt["receipt_path"] = str(receipt_path)
    return receipt


def rule_candidate(root: Path, candidate_id: str, decision: str, actor: str, rationale: str) -> dict:
    if decision not in DECISIONS:
        raise ValueError("decision must be one of: " + ", ".join(sorted(DECISIONS)))
    packet_path = root / "_candidate_packets" / f"{candidate_id}.candidate.json"
    packet = read_json(packet_path)
    errors = validate_packet(packet)
    if errors:
        raise ValueError("packet validation failed: " + "; ".join(errors))
    if packet["kimi_review"]["affected"] and packet["kimi_review"]["state"] != "ADJUDICATED":
        raise ValueError("candidate is blocked pending Kimi adjudication")
    event = {"event_type": "CANDIDATE_HUMAN_RULING", "status": STATUS, "candidate_id": candidate_id, "candidate_version": packet["candidate_version"], "decision": decision, "actor": actor, "date": now(), "rationale": rationale, "canonical_admission_performed": False}
    folder = root / "_human_rulings"; folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{candidate_id}.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.candidate-ruling.json"
    path.write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    event["ruling_path"] = str(path)
    return event


def map_objection(root: Path, ledger_path: Path, objection_id: str, candidate_id: str, candidate_version: str) -> dict:
    ledger = read_json(ledger_path)
    objection = next((item for item in ledger.get("objections", []) if item.get("objection_id") == objection_id), None)
    if objection is None: raise ValueError("objection id not found")
    packet_path = root / "_candidate_packets" / f"{candidate_id}.candidate.json"
    packet = read_json(packet_path)
    if packet.get("candidate_version") != candidate_version: raise ValueError("candidate version does not match packet")
    link = {"candidate_id": candidate_id, "candidate_version": candidate_version}
    if link not in objection["candidate_links"]: objection["candidate_links"].append(link)
    objection["mapping_status"] = "MAPPED — PENDING ADJUDICATION"
    packet["kimi_review"] = {"state":"PENDING_ADJUDICATION","affected":True,"objection_ids":sorted(set(packet.get("kimi_review", {}).get("objection_ids", []) + [objection_id])),"finalization_blocked":True}
    if objection["exact_wording"] not in packet["review_card"]["kimi_exact_criticism"]: packet["review_card"]["kimi_exact_criticism"].append(objection["exact_wording"])
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status":STATUS,"objection_id":objection_id,"candidate":link,"finalization_blocked":True,"canonical_admission_performed":False}


def adjudicate_objection(root: Path, ledger_path: Path, objection_id: str, candidate_id: str, response: str, ruling: str, actor: str) -> dict:
    if ruling not in DECISIONS: raise ValueError("Kimi ruling must use a candidate decision")
    ledger = read_json(ledger_path); objection = next((item for item in ledger.get("objections", []) if item.get("objection_id") == objection_id), None)
    if objection is None: raise ValueError("objection id not found")
    if not any(link.get("candidate_id") == candidate_id for link in objection.get("candidate_links", [])): raise ValueError("objection is not linked to candidate")
    response_event = {"candidate_id":candidate_id,"response":response,"actor":actor,"date":now()}; objection["proposed_responses"].append(response_event)
    objection["david_ruling"] = {"candidate_id":candidate_id,"decision":ruling,"actor":actor,"date":now()}; objection["mapping_status"] = "ADJUDICATED"
    packet_path = root / "_candidate_packets" / f"{candidate_id}.candidate.json"; packet = read_json(packet_path)
    packet["review_card"]["proposed_response"].append(response_event); packet["kimi_review"]["state"] = "ADJUDICATED"; packet["kimi_review"]["finalization_blocked"] = False
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status":STATUS,"objection_id":objection_id,"candidate_id":candidate_id,"kimi_state":"ADJUDICATED","canonical_admission_performed":False}


def validate_admission_event(value: dict) -> list[str]:
    errors = sorted(REQUIRED_ADMISSION - set(value))
    if value.get("event_type") != "SIGNED_HUMAN_ADMISSION": errors.append("event_type")
    if value.get("decision") != "ADMIT": errors.append("decision")
    if not value.get("signed_admission_receipt"): errors.append("signed_admission_receipt")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate"); check.add_argument("--root", required=True)
    intake = sub.add_parser("import-kimi"); intake.add_argument("--root", required=True); intake.add_argument("--source", required=True)
    ruling = sub.add_parser("rule-candidate"); ruling.add_argument("--root", required=True); ruling.add_argument("--candidate", required=True); ruling.add_argument("--decision", required=True); ruling.add_argument("--actor", required=True); ruling.add_argument("--rationale", required=True)
    mapping = sub.add_parser("map-kimi"); mapping.add_argument("--root", required=True); mapping.add_argument("--ledger", required=True); mapping.add_argument("--objection", required=True); mapping.add_argument("--candidate", required=True); mapping.add_argument("--version", required=True)
    adjudicate = sub.add_parser("adjudicate-kimi"); adjudicate.add_argument("--root", required=True); adjudicate.add_argument("--ledger", required=True); adjudicate.add_argument("--objection", required=True); adjudicate.add_argument("--candidate", required=True); adjudicate.add_argument("--response", required=True); adjudicate.add_argument("--ruling", required=True); adjudicate.add_argument("--actor", required=True)
    args = parser.parse_args(); root = Path(args.root).resolve()
    if args.command == "validate": result = validate_run(root)
    elif args.command == "import-kimi": result = import_kimi(root, Path(args.source).resolve())
    elif args.command == "rule-candidate": result = rule_candidate(root, args.candidate, args.decision, args.actor, args.rationale)
    elif args.command == "map-kimi": result = map_objection(root, Path(args.ledger).resolve(), args.objection, args.candidate, args.version)
    else: result = adjudicate_objection(root, Path(args.ledger).resolve(), args.objection, args.candidate, args.response, args.ruling, args.actor)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if result.get("status") != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
