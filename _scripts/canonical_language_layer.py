#!/usr/bin/env python3
"""Candidate-only canonical language resolution for claim_pipeline_service.

This module cannot admit records. Its signed-admission helper is usable only when
explicitly called with a complete event and is not called by review or bootstrap.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

STATUS = "CANDIDATE_DRAFT — NOT ADMITTED"
REGISTRY_NAMES = (
    "DEFINITION_REGISTRY", "SYMBOL_NOTATION_REGISTRY", "AXIOM_REGISTRY",
    "TRUTH_KERNEL_REGISTRY", "FORMAL_OBJECT_REGISTRY", "BRIDGE_REGISTRY",
    "PROJECTION_REGISTRY",
)
TRUTH_MODES = {
    "DECLARED", "DEFINED", "DERIVED", "CONDITIONALLY_ENTAILED",
    "EMPIRICALLY_SUPPORTED", "HISTORICALLY_SUPPORTED",
    "PHILOSOPHICALLY_ARGUED", "THEOLOGICALLY_IDENTIFIED",
    "BRIDGE_DEPENDENT", "OPEN",
}
SIGNED_ADMISSION_FIELDS = {
    "event_type", "actor", "date", "rationale", "source_hashes",
    "candidate_hash", "unresolved_fields", "downstream_impact",
    "signed_admission_receipt", "registry_id", "object_id", "version",
}


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def empty_registry(name: str) -> dict:
    if name not in REGISTRY_NAMES: raise ValueError(f"unknown registry {name}")
    return {"schema_version":"canonical-language-registry/1.0.0","registry_id":name,"registry_version":"0.1.0","status":STATUS,"active_versions":{},"admitted_objects":{},"proposed_objects":[],"human_ruling_required":True}


def object_key(record: dict) -> str:
    for key in ("definition_id","symbol_id","axiom_id","truth_id","formal_object_id","bridge_id","projection_id"):
        if record.get(key): return str(record[key])
    raise ValueError("record has no governed object id")


def validate_registry(registry: dict) -> list[str]:
    errors=[]
    if registry.get("registry_id") not in REGISTRY_NAMES: errors.append("unknown registry_id")
    if registry.get("status") != STATUS: errors.append("registry must remain candidate-only")
    if registry.get("human_ruling_required") is not True: errors.append("human ruling must be required")
    admitted=registry.get("admitted_objects",{}); active=registry.get("active_versions",{})
    if not isinstance(admitted,dict) or not isinstance(active,dict): errors.append("admitted_objects and active_versions must be objects")
    for oid,version in active.items():
        if f"{oid}@{version}" not in admitted: errors.append(f"active pointer lacks admitted immutable object: {oid}@{version}")
    return errors


def propose_revision(registry: dict, record: dict) -> dict:
    errors=validate_registry(registry)
    if errors: raise ValueError("; ".join(errors))
    result=copy.deepcopy(registry); oid=object_key(record); version=str(record.get("version", ""))
    if not version: raise ValueError("version is required")
    key=f"{oid}@{version}"
    if key in result["admitted_objects"]: raise ValueError("admitted versions are immutable and cannot be overwritten")
    if any(object_key(item)==oid and str(item.get("version"))==version for item in result["proposed_objects"]): raise ValueError("proposed version already exists")
    active=result["active_versions"].get(oid)
    if active and not record.get("supersedes"): raise ValueError("revision of an active object must name supersedes")
    candidate=copy.deepcopy(record); candidate["status"]=STATUS; candidate["human_ruling_required"]=True; candidate["candidate_hash"]=sha(record)
    result["proposed_objects"].append(candidate)
    return result


def apply_signed_admission(registry: dict, record: dict, event: dict) -> dict:
    missing=sorted(SIGNED_ADMISSION_FIELDS-set(event))
    if missing or event.get("event_type")!="SIGNED_HUMAN_ADMISSION" or not event.get("signed_admission_receipt"):
        raise ValueError("complete distinct signed admission event required" + (": "+", ".join(missing) if missing else ""))
    oid=object_key(record); version=str(record["version"])
    if event["registry_id"]!=registry["registry_id"] or event["object_id"]!=oid or str(event["version"])!=version: raise ValueError("admission event target mismatch")
    expected_hash=record.get("candidate_hash") or sha(record)
    if event["candidate_hash"]!=expected_hash: raise ValueError("candidate hash mismatch")
    result=copy.deepcopy(registry); key=f"{oid}@{version}"
    if key in result["admitted_objects"]: raise ValueError("admitted version already exists")
    admitted=copy.deepcopy(record); admitted["status"]="ADMITTED"; admitted["admission_event_hash"]=sha(event)
    result["admitted_objects"][key]=admitted; result["active_versions"][oid]=version
    return result


def next_version(current: str | None) -> str:
    if not current: return "0.1.0"
    parts=[int(x) for x in current.split(".")]
    if len(parts)!=3: raise ValueError("semantic version required")
    return f"{parts[0]}.{parts[1]+1}.0"


def normalized_glyph(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def detect_symbol_conflicts(candidate: dict, records: list[dict]) -> list[dict]:
    conflicts=[]; glyph=normalized_glyph(candidate.get("glyph","")); meaning=str(candidate.get("meaning","")).strip().casefold()
    for old in records:
        if normalized_glyph(old.get("glyph",""))==glyph and glyph:
            incompatible=[field for field in ("meaning","type_signature","domain","codomain","units") if old.get(field) and candidate.get(field) and old[field]!=candidate[field]]
            if incompatible: conflicts.append({"kind":"INCOMPATIBLE_SYMBOL_REUSE","against":f"{old.get('symbol_id')}@{old.get('version')}","fields":incompatible})
        if meaning and str(old.get("meaning","")).strip().casefold()==meaning and normalized_glyph(old.get("glyph",""))!=glyph:
            conflicts.append({"kind":"MULTIPLE_SYMBOLS_ONE_OBJECT","against":f"{old.get('symbol_id')}@{old.get('version')}","glyphs":[old.get("glyph"),candidate.get("glyph")]})
    missing=[field for field in ("type_signature","domain","codomain") if not candidate.get(field)]
    if missing: conflicts.append({"kind":"OPEN_MISSING_TYPE_INFORMATION","fields":missing})
    if candidate.get("register")=="bridge" and candidate.get("glyph")=="=": conflicts.append({"kind":"BRIDGE_WRITTEN_AS_LITERAL_EQUALITY"})
    return conflicts


def truth_mode_for(capsule: dict, classification: dict) -> str:
    intent=str(capsule.get("warrant_intent",capsule.get("claim_type",""))).upper(); register=str(classification.get("register","")).lower()
    if capsule.get("source_object_id")=="A0" or capsule.get("claim")=="The Triune God is.": return "DECLARED"
    if "DEFINITION" in intent: return "DEFINED"
    if "COUNTERMODEL" in intent or register=="mathematics": return "CONDITIONALLY_ENTAILED"
    if register=="empirical": return "EMPIRICALLY_SUPPORTED"
    if register=="history": return "HISTORICALLY_SUPPORTED"
    if register=="theology": return "THEOLOGICALLY_IDENTIFIED"
    if register=="bridge": return "BRIDGE_DEPENDENT"
    if register in {"domain-neutral","normative","unresolved"}: return "PHILOSOPHICALLY_ARGUED"
    return "OPEN"


def build_truth_kernel(capsule: dict, classification: dict, definitions: list[str], symbols: list[str]) -> dict:
    proposition=capsule["claim"].strip(); mode=truth_mode_for(capsule,classification); premises=list(capsule.get("premise_set",capsule.get("depends_on",[])))
    entailment="NOT_TESTED"
    if mode=="CONDITIONALLY_ENTAILED": entailment="CONDITIONAL_ONLY — PREMISES NOT PROVED"
    if proposition=="The Triune God is.": entailment="DECLARED THEOLOGICAL STARTING POINT — NOT LEAN-PROVED"
    return {"truth_id":capsule.get("truth_id") or f"TRUTH-{capsule.get('source_object_id','UNASSIGNED')}","version":capsule.get("candidate_version","0.1.0"),"exact_proposition":proposition,"premise_set":premises,"definitions_used":definitions,"symbols_used":symbols,"domain":classification.get("register","unresolved"),"scope":capsule.get("scope",[]),"truth_mode":mode,"negation":capsule.get("negation") or f"It is not the case that: {proposition}","countermodels":capsule.get("countermodels",[]),"what_survives_countermodels":capsule.get("what_survives_countermodels",[]),"entailment_status":entailment,"irrevocability_condition":"Formally irrevocable only within the declared premise set and inference rules when its negation is inconsistent with them.","overturn_requires":capsule.get("overturn_requires",["Revise a premise, inference rule, scope, source interpretation, or show a valid countermodel."]),"representation_invariance":capsule.get("representation_invariance","OPEN"),"why_closure":classification.get("why_outcome","WHY_OPEN"),"formal_receipts":capsule.get("formal_receipts",[]),"empirical_or_historical_limits":capsule.get("empirical_or_historical_limits",[]),"bridge_dependencies":capsule.get("bridge_dependencies",[]),"open_fields":capsule.get("open_items",[]),"human_truth_ruling":None,"status":STATUS,"human_ruling_required":True}


def dependency_impact(changed_id: str, objects: list[dict]) -> dict:
    reverse={}
    for item in objects:
        oid=item.get("id") or item.get("truth_id") or object_key(item)
        for dep in item.get("dependencies",item.get("premise_set",[])): reverse.setdefault(dep,[]).append(oid)
    direct=sorted(set(reverse.get(changed_id,[]))); all_down=[]; queue=list(direct)
    while queue:
        node=queue.pop(0)
        if node in all_down: continue
        all_down.append(node); queue.extend(reverse.get(node,[]))
    return {"changed_object":changed_id,"direct_dependents":direct,"all_downstream":all_down,"required_action":"FLAG_FOR_HUMAN_REVIEW","automatic_source_rewrite":False,"cross_register_rule":"Explicit permitted edge required; bridge edges never transfer proof."}


def analyze_candidate(capsule: dict, classification: dict, registry_bundle: dict | None = None) -> dict:
    bundle=registry_bundle or {}; definitions=[]; definition_conflicts=[]
    claim=capsule["claim"]
    for record in bundle.get("definitions",[]):
        terms=[record.get("canonical_term"),*record.get("aliases",[])]
        if any(term and re.search(rf"\b{re.escape(term)}\b",claim,re.I) for term in terms): definitions.append(f"{record['definition_id']}@{record['version']}")
        for forbidden in record.get("forbidden_equivalences",[]):
            if forbidden and forbidden.casefold() in claim.casefold(): definition_conflicts.append({"definition":f"{record['definition_id']}@{record['version']}","forbidden_equivalence":forbidden})
    symbols=[]; symbol_conflicts=[]
    for record in bundle.get("symbols",[]):
        if record.get("glyph") and record["glyph"] in claim: symbols.append(f"{record['symbol_id']}@{record['version']}")
        symbol_conflicts.extend(detect_symbol_conflicts(record,[x for x in bundle.get("symbols",[]) if x is not record]))
    truth=build_truth_kernel(capsule,classification,definitions,symbols)
    bridge={"propagates_proof":False,"status":STATUS,"violations":[]}
    if classification.get("register")=="bridge":
        if re.search(r"\b(is|equals|identical to)\b|=",claim,re.I): bridge["violations"].append("POSSIBLE_LITERAL_IDENTITY_REQUIRES_EXPLICIT_BRIDGE_MAPPING")
        bridge["rule"]="A BRIDGE NEVER PROPAGATES AS PROOF."
    graph=bundle.get("dependency_objects",[]); changed=capsule.get("source_object_id") or truth["truth_id"]
    impact=dependency_impact(changed,graph) if graph else {"changed_object":changed,"direct_dependents":[],"all_downstream":[],"required_action":"FLAG_FOR_HUMAN_REVIEW","automatic_source_rewrite":False}
    operation="new_version" if capsule.get("supersedes") else "new_claim"
    return {"schema_version":"canonical-language-analysis/1.0.0","status":STATUS,"definition_resolution":{"matches":definitions,"conflicts":definition_conflicts},"symbol_resolution":{"matches":symbols,"conflicts":symbol_conflicts},"truth_kernel":truth,"bridge_analysis":bridge,"dependency_impact":impact,"proposed_version_operation":operation,"projection_impact":{"current_projections_may_become_stale":bool(impact.get("all_downstream")),"source_papers_changed":False,"regeneration_requires_admitted_active_versions":True},"human_ruling_required":True,"canonical_admission_performed":False}


def projection_record(projection_id: str, source_objects: list[dict], registry_versions: dict, generator_version: str, unresolved: list[str]) -> dict:
    return {"projection_id":projection_id,"version":"0.1.0","status":STATUS,"source_objects":[{"id":x["id"],"version":x["version"],"source_hash":x["source_hash"]} for x in source_objects],"registry_versions":registry_versions,"generation_time":datetime.now(timezone.utc).isoformat(),"generator_version":generator_version,"currency":"STALE" if unresolved else "CANDIDATE_CURRENT","unresolved_fields":unresolved,"admission_status":"NOT_ADMITTED","independent_source_of_truth":False,"human_ruling_required":True}
