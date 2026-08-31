#!/usr/bin/env python3
"""Local David-OS claim capsule and gated DeepSeek review service.

Writes review receipts only. It never promotes, overwrites, or mutates canon.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
APP = REPO / "_runtime" / "claim_capsule_app"
RUNS = APP / "runs"
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"


def load_canonical_language_layer():
    path = Path(__file__).with_name("canonical_language_layer.py")
    spec = importlib.util.spec_from_file_location("canonical_language_layer", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def extract_json(text: str) -> dict:
    clean = text.strip()
    clean = re.sub(r"^```(?:json)?\s*", "", clean)
    clean = re.sub(r"\s*```$", "", clean)
    try:
        value = json.loads(clean)
    except json.JSONDecodeError:
        start, end = clean.find("{"), clean.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Reviewer did not return a JSON object")
        value = json.loads(clean[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Reviewer output must be a JSON object")
    return value


def load_deepseek_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    candidates = [
        REPO / "keys.txt",
        REPO / ".env.local",
        REPO / ".env",
        Path(r"D:\GitHub\GOLD\Faith-through-physics-atoms\.env"),
    ]
    for path in candidates:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip().startswith("DEEPSEEK_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("DeepSeek is not configured. Set DEEPSEEK_API_KEY or place it in an ignored repo keys.txt/.env.local file.")


def call_deepseek(system: str, payload: dict, model: str) -> dict:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False, indent=2)},
        ],
        "temperature": 0.1,
        "max_tokens": 7500,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        DEEPSEEK_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {load_deepseek_key()}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"DeepSeek HTTP {exc.code}") from exc
    return extract_json(result["choices"][0]["message"]["content"])


DISCOVERY_PROMPT = """You are Stage 1 of the Faith Through Physics claim pipeline.
Inspect the raw expression without assigning a discipline, claim class, theology label, evidence grade, IC grade, or canonical status. Classifications are outputs of a later stage, never inputs here. Expose dependency structure rather than paraphrasing. Preserve uncertainty and alternatives. Do not split a sentence merely because it has an explanatory, definitional, limiting, or boundary clause; split only when the source contains two assertions with independently reviewable truth conditions. Respect any source-pinned decomposition guidance in the capsule without treating it as a truth verdict. Return JSON only with exactly: schema_version='claim-discovery/1.0.0', stage='NON_DISCRIMINATORY_DISCOVERY', status (DISCOVERY_COMPLETE, DISCOVERY_INCOMPLETE, or BLOCKED), raw_expression, referent, and string arrays identities, distinctions, relations, operations, dependencies, constraints, invariants, collapse_conditions, consequences, countermodels, open_questions, prohibited_outputs. prohibited_outputs must name classifications deliberately withheld. Do not smuggle the proposed answer into a dependency. Be compact: each array may contain at most 12 items, each item at most 30 words; raw_expression and referent at most 80 words each. Finish the complete JSON object and do not include commentary."""

CLASSIFICATION_PROMPT = """You are Stage 2 of the Faith Through Physics claim pipeline. You may classify only the hash-pinned Stage 1 discovery and the source_governance record carried in the capsule. Do not add facts. Source metadata is a classification boundary: if it supplies allowed claim species or warrant classes, preserve them exactly; if you believe they are wrong, return RETURN_TO_DISCOVERY and explain the conflict in new_fact_exception. Never silently strengthen a source marked primitive or stance into a formal proof, metaphysical necessity, empirical result, or a cross-domain bridge. A notation or representation is not by itself a formal warrant. Keep formal, empirical, historical, philosophical, theological, and bridge warrants distinct. Return JSON only with exactly: schema_version='claim-classification/1.0.0', stage='CLASSIFICATION_AND_BURDEN_ROUTING', status, discovery_receipt_hash, object_type (CLAIM/EVIDENCE/PROOF/PROCESS), register, claim_species, native_anatomy array, warrant_class, lifecycle='candidate', why_outcome (WHY_CLOSED/WHY_OPEN/WHY_FAILED/NOT_APPLICABLE), burdens array, unresolved array, new_fact_exception string or null. status must be exactly CLASSIFICATION_COMPLETE, RETURN_TO_DISCOVERY, or BLOCKED; never use aliases such as CLASSIFIED. Classification never promotes or canonizes."""

RECONCILIATION_PROMPT = """You are Stage 3 of the Faith Through Physics claim pipeline. Reconcile the raw capsule, hash-pinned discovery, hash-pinned classification, and source_governance record with graph and translation discipline. Keep Native -> Bridge -> Identification as three distinct rails. Do not create a bridge merely because a claim has philosophical, theological, or physical language. When source_governance.bridge_permitted is false, bridge_statement must be null. A bridge may be proposed only when a source-pinned source and target mapping are supplied; it must be one-directional unless both directions are demonstrated, must list lost structure, and never propagates proof. Return JSON only with exactly: schema_version='claim-reconciliation/1.0.0', stage='RECONCILIATION_TRANSLATION_AND_FIT', status, discovery_receipt_hash, classification_receipt_hash, recommended_operation (new_claim/amend/new_version/supersede/add_evidence/hold_open), graph_fit, native_statement, bridge_statement string or null, identification_statement string or null, safe_public_wording, preserved array, lost array, downstream_effects array, publication_eligibility (ELIGIBLE_FOR_HUMAN_REVIEW/NOT_ELIGIBLE/EXCEPTION_HUMAN_REVIEW), human_ruling_required=true. status must be exactly RECONCILIATION_COMPLETE, RETURN_TO_CLASSIFICATION, or BLOCKED; never use aliases such as RECONCILED. Never canonize."""


def require_fields(value: dict, fields: list[str], stage: str) -> None:
    missing = [field for field in fields if field not in value]
    if missing:
        raise ValueError(f"{stage} missing required fields: {', '.join(missing)}")


def mock_discovery(capsule: dict) -> dict:
    claim = capsule["claim"].strip()
    return {"schema_version":"claim-discovery/1.0.0","stage":"NON_DISCRIMINATORY_DISCOVERY","status":"DISCOVERY_COMPLETE","raw_expression":claim,"referent":claim,"identities":["The asserted referent must remain identifiable across restatements."],"distinctions":["The assertion must be distinguishable from its negation and nearby alternatives."],"relations":[],"operations":[],"dependencies":["Terms require stable definitions."],"constraints":[capsule.get("defeat_condition") or "A defeat condition remains open."],"invariants":["Meaning preserved between the exact and plain-language statements."],"collapse_conditions":["The assertion collapses if its stated defeat condition is met."],"consequences":[],"countermodels":["The exact negation remains a live comparison until discriminated."],"open_questions":capsule.get("open_items", []),"prohibited_outputs":["No discipline, warrant, grade, bridge, or canonical status assigned in Stage 1."]}


def incomplete_discovery(capsule: dict, reason: str) -> dict:
    claim = capsule["claim"].strip()
    return {"schema_version":"claim-discovery/1.0.0","stage":"NON_DISCRIMINATORY_DISCOVERY","status":"DISCOVERY_INCOMPLETE","raw_expression":claim,"referent":claim,"identities":[],"distinctions":[],"relations":[],"operations":[],"dependencies":[],"constraints":[],"invariants":[],"collapse_conditions":[],"consequences":[],"countermodels":[],"open_questions":[reason],"prohibited_outputs":["No classification, warrant, bridge, proof, or canonical status may be assigned until a human split resolves the source bundle."]}


def mock_classification(capsule: dict, discovery: dict, discovery_hash: str) -> dict:
    species = capsule.get("claim_type", "other")
    register = {"mathematical":"mathematics","empirical":"empirical","historical":"history","theological":"theology","bridge":"bridge","normative":"normative","universal":"domain-neutral","everyday_translation":"translation"}.get(species,"unresolved")
    warrant = {"mathematical":"D/C","empirical":"E","historical":"H","theological":"T","bridge":"BR/A","normative":"P/T"}.get(species,"O")
    object_type = capsule.get("object_type_hint", "CLAIM")
    if object_type not in {"CLAIM", "EVIDENCE", "PROOF", "PROCESS"}: object_type = "CLAIM"
    governance = capsule.get("source_governance") or {}
    allowed_species = governance.get("allowed_claim_species") or []
    allowed_warrants = governance.get("allowed_warrant_classes") or []
    if allowed_species:
        species = allowed_species[0]
    if allowed_warrants:
        warrant = allowed_warrants[0]
    return {"schema_version":"claim-classification/1.0.0","stage":"CLASSIFICATION_AND_BURDEN_ROUTING","status":"CLASSIFICATION_COMPLETE","discovery_receipt_hash":discovery_hash,"object_type":object_type,"register":register,"claim_species":species,"native_anatomy":[],"warrant_class":warrant,"lifecycle":"candidate","why_outcome":"WHY_OPEN","burdens":["Complete the native anatomy and attach discriminating support."],"unresolved":discovery.get("open_questions", []),"new_fact_exception":None}


def mock_reconciliation(capsule: dict, discovery: dict, classification: dict, dh: str, ch: str) -> dict:
    governance = capsule.get("source_governance") or {}
    is_bridge = classification["register"] == "bridge" and governance.get("bridge_permitted", False)
    return {"schema_version":"claim-reconciliation/1.0.0","stage":"RECONCILIATION_TRANSLATION_AND_FIT","status":"RECONCILIATION_COMPLETE","discovery_receipt_hash":dh,"classification_receipt_hash":ch,"recommended_operation":capsule.get("operation","new_claim"),"graph_fit":"Candidate only; semantic graph matching is pending.","native_statement":capsule["claim"],"bridge_statement":capsule["claim"] if is_bridge else None,"identification_statement":None,"safe_public_wording":capsule.get("plain_language",capsule["claim"]),"preserved":["Exact claim wording and declared warrant boundary."],"lost":(["Full source and target structure have not been tested."] if is_bridge else []),"downstream_effects":[],"publication_eligibility":"ELIGIBLE_FOR_HUMAN_REVIEW","human_ruling_required":True}


def apply_source_governance_guard(capsule: dict, classification: dict) -> dict:
    """Fail closed when a source-pinned classification boundary was silently exceeded."""
    governance = capsule.get("source_governance") or {}
    allowed_species = set(governance.get("allowed_claim_species") or [])
    allowed_warrants = set(governance.get("allowed_warrant_classes") or [])
    violations = []
    if allowed_species and classification.get("claim_species") not in allowed_species:
        violations.append(f"claim_species={classification.get('claim_species')!r} is outside source-pinned allowed values")
    if allowed_warrants and classification.get("warrant_class") not in allowed_warrants:
        violations.append(f"warrant_class={classification.get('warrant_class')!r} is outside source-pinned allowed values")
    if violations:
        classification = dict(classification)
        classification["status"] = "RETURN_TO_DISCOVERY"
        classification["new_fact_exception"] = "SOURCE_GOVERNANCE_BLOCK: " + "; ".join(violations)
        classification["unresolved"] = list(classification.get("unresolved") or []) + [classification["new_fact_exception"]]
    return classification


def apply_bridge_guard(capsule: dict, reconciliation: dict) -> dict:
    """Do not allow an unpinned or prohibited bridge to pass into a review-ready projection."""
    governance = capsule.get("source_governance") or {}
    bridge = reconciliation.get("bridge_statement")
    if bridge and not governance.get("bridge_permitted", False):
        reconciliation = dict(reconciliation)
        reconciliation["status"] = "RETURN_TO_CLASSIFICATION"
        reconciliation["publication_eligibility"] = "NOT_ELIGIBLE"
        reconciliation["downstream_effects"] = list(reconciliation.get("downstream_effects") or []) + [
            "SOURCE_GOVERNANCE_BLOCK: bridge was emitted without a source-pinned mapping."
        ]
    return reconciliation


def load_source_document(capsule: dict) -> dict | None:
    source = capsule.get("source") or {}
    raw_path = source.get("path_or_uri")
    if not raw_path:
        return None
    path = Path(raw_path).resolve()
    allowed_roots = [REPO.resolve(), Path(r"Z:\__New\Theophysics.new").resolve()]
    if not any(path == root or root in path.parents for root in allowed_roots):
        raise ValueError("Source path is outside the allowed repository and Obsidian vault roots")
    if not path.is_file():
        raise ValueError(f"Source file does not exist: {path}")
    raw = path.read_bytes()
    actual_hash = "sha256:" + hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    declared_hash = source.get("source_hash")
    if declared_hash and declared_hash.lower().replace("sha256:", "") != actual_hash.replace("sha256:", ""):
        raise ValueError("Source hash does not match the current file")
    content = text
    line_start, line_end = source.get("line_start"), source.get("line_end")
    if line_start is not None or line_end is not None:
        if not isinstance(line_start, int) or not isinstance(line_end, int) or line_start < 1 or line_end < line_start:
            raise ValueError("Source excerpt requires valid one-based line_start and line_end")
        lines = text.splitlines()
        if line_end > len(lines):
            raise ValueError("Source excerpt line range exceeds the source file")
        content = "\n".join(lines[line_start - 1 : line_end])
        declared_quote = source.get("quotation")
        if declared_quote is not None and declared_quote not in content:
            raise ValueError("Pinned source quotation is not present in the declared line range")
        quote_hash = source.get("quotation_hash")
        if quote_hash and digest_text(declared_quote or content) != quote_hash:
            raise ValueError("Pinned source quotation hash does not match")
    return {"path": str(path), "sha256": actual_hash, "heading": source.get("heading"), "line_start": line_start, "line_end": line_end, "quotation": source.get("quotation"), "quotation_hash": source.get("quotation_hash"), "content": content}


def digest_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def review(capsule: dict, provider: str, model: str) -> dict:
    require_fields(capsule, ["claim", "plain_language", "claim_type", "operation", "defeat_condition"], "capsule")
    if capsule.get("canonical_promotion_requested") not in (None, False):
        raise ValueError("This service never accepts canonical promotion requests")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    stages = []
    source_document = load_source_document(capsule)
    discovery_input = {"capsule": capsule}
    if source_document:
        discovery_input["source_document"] = source_document
        discovery_input["instruction"] = "Treat the source as a possible bundle. Do not force one epistemic ruling across independent assertions; return DISCOVERY_INCOMPLETE when decomposition is required."
    if capsule.get("decomposition_guidance"):
        discovery_input["decomposition_guidance"] = capsule["decomposition_guidance"]
    incomplete_reason = capsule.get("discovery_incomplete_reason")
    discovery = incomplete_discovery(capsule, incomplete_reason) if incomplete_reason else call_deepseek(DISCOVERY_PROMPT, discovery_input, model) if provider == "deepseek" else mock_discovery(capsule)
    require_fields(discovery, ["status", "raw_expression", "referent", "prohibited_outputs"], "discovery")
    dh = sha(discovery); stages.append({"name":"discovery","status":discovery["status"],"hash":dh,"output":discovery})
    if discovery["status"] != "DISCOVERY_COMPLETE":
        return finish(run_id, provider, model, capsule, stages, "BLOCKED")
    classification_input = {"capsule":capsule,"source_reference":({"path":source_document["path"],"sha256":source_document["sha256"]} if source_document else None),"discovery":discovery,"discovery_receipt_hash":dh}
    classification = call_deepseek(CLASSIFICATION_PROMPT, classification_input, model) if provider == "deepseek" else mock_classification(capsule, discovery, dh)
    classification = apply_source_governance_guard(capsule, classification)
    require_fields(classification, ["status", "discovery_receipt_hash", "object_type", "register", "warrant_class"], "classification")
    if classification["discovery_receipt_hash"] != dh:
        raise ValueError("Classification did not preserve the discovery receipt hash")
    ch = sha(classification); stages.append({"name":"classification","status":classification["status"],"hash":ch,"output":classification})
    if classification["status"] != "CLASSIFICATION_COMPLETE":
        return finish(run_id, provider, model, capsule, stages, "BLOCKED")
    language_resolution = None
    if capsule.get("canonical_language_enabled"):
        language_resolution = load_canonical_language_layer().analyze_candidate(capsule, classification, capsule.get("canonical_language_registry_bundle"))
    rec_input = {"capsule":capsule,"discovery":discovery,"classification":classification,"canonical_language_resolution":language_resolution,"discovery_receipt_hash":dh,"classification_receipt_hash":ch}
    reconciliation = call_deepseek(RECONCILIATION_PROMPT, rec_input, model) if provider == "deepseek" else mock_reconciliation(capsule, discovery, classification, dh, ch)
    reconciliation = apply_bridge_guard(capsule, reconciliation)
    require_fields(reconciliation, ["status", "discovery_receipt_hash", "classification_receipt_hash", "human_ruling_required"], "reconciliation")
    if reconciliation["discovery_receipt_hash"] != dh or reconciliation["classification_receipt_hash"] != ch:
        raise ValueError("Reconciliation did not preserve upstream receipt hashes")
    rh = sha(reconciliation); stages.append({"name":"reconciliation","status":reconciliation["status"],"hash":rh,"output":reconciliation})
    status = "PASS" if reconciliation["status"] == "RECONCILIATION_COMPLETE" else "BLOCKED"
    return finish(run_id, provider, model, capsule, stages, status, language_resolution)


def finish(run_id: str, provider: str, model: str, capsule: dict, stages: list[dict], status: str, canonical_language_resolution: dict | None = None) -> dict:
    receipt = {"receipt_version":"claim-pipeline-receipt/1.0.0","run_id":run_id,"created_at":datetime.now(timezone.utc).isoformat(),"provider":provider,"model":model,"capsule_hash":sha(capsule),"stages":stages,"final_status":status,"canonical_promotion_performed":False}
    if canonical_language_resolution is not None:
        receipt["canonical_language_resolution"] = canonical_language_resolution
        receipt["canonical_language_resolution_hash"] = sha(canonical_language_resolution)
    RUNS.mkdir(parents=True, exist_ok=True)
    path = RUNS / f"{run_id}.json"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt["receipt_path"] = str(path)
    return receipt


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP), **kwargs)

    def send_json(self, status: int, value: dict) -> None:
        data = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/health":
            candidates = [
                REPO / "keys.txt",
                REPO / ".env.local",
                REPO / ".env",
                Path(r"D:\GitHub\GOLD\Faith-through-physics-atoms\.env"),
            ]
            configured = bool(os.environ.get("DEEPSEEK_API_KEY")) or any(
                path.is_file()
                and any(line.strip().startswith("DEEPSEEK_API_KEY=") for line in path.read_text(encoding="utf-8", errors="replace").splitlines())
                for path in candidates
            )
            self.send_json(200, {"status":"ok","service":"claim-pipeline","deepseek_configured":configured,"canonical_promotion_enabled":False}); return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/review":
            self.send_json(404, {"error":"not found"}); return
        try:
            length = int(self.headers.get("Content-Length", "0")); body = json.loads(self.rfile.read(length).decode("utf-8"))
            provider = body.pop("provider", "deepseek"); model = body.pop("model", "deepseek-chat")
            if provider not in {"deepseek", "mock"}: raise ValueError("provider must be deepseek or mock")
            self.send_json(200, review(body, provider, model))
        except Exception as exc:
            self.send_json(400, {"error":str(exc),"canonical_promotion_performed":False})


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--host", default="127.0.0.1"); parser.add_argument("--port", type=int, default=8787); parser.add_argument("--review-json"); parser.add_argument("--output-dir"); parser.add_argument("--provider", choices=["deepseek","mock"], default="deepseek"); parser.add_argument("--model", default="deepseek-chat"); args = parser.parse_args()
    global RUNS
    if args.output_dir:
        RUNS = Path(args.output_dir).resolve()
    if args.review_json:
        capsule = json.loads(Path(args.review_json).read_text(encoding="utf-8")); print(json.dumps(review(capsule,args.provider,args.model),ensure_ascii=False,indent=2)); return
    APP.mkdir(parents=True, exist_ok=True); print(f"Claim capsule: http://{args.host}:{args.port}"); ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()


if __name__ == "__main__": main()
