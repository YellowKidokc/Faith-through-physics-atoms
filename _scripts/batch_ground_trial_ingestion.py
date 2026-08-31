#!/usr/bin/env python3
"""Provenance-pinned Ground Trial adapter for the existing claim pipeline."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path

STATUS = "CANDIDATE_DRAFT — NOT ADMITTED"
DEFAULT_LEDGER = Path(r"Z:\__New\Theophysics.new\notes\THE_GROUND_TRIAL\06_CLAIM_ATOMS\00_MASTER_CLAIM_LEDGER.md")
DEFAULT_CHAIN = Path(r"Z:\__New\Theophysics.new\___AXIOM\01_CANON\18_THE_AXIOM_CHAIN\___CANONICAL\SEQUENTIAL_PRE_v2.3_BACKUP\_AXIOM_CHAIN_MASTER_v2.3_SEALED.md")
INDEX_NAMED_CHAIN = Path(r"Z:\__New\Theophysics.new\___AXIOM\01_CANON\18_THE_AXIOM_CHAIN\AXIOM_CHAIN_MASTER_v2.3_SEALED.md")


def load_pipeline():
    path = Path(__file__).with_name("claim_pipeline_service.py")
    spec = importlib.util.spec_from_file_location("claim_pipeline_service", path)
    module = importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module)
    return module


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def text_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def headings_by_line(lines: list[str]) -> list[str]:
    current = "(document root)"; result = []
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match: current = match.group(2)
        result.append(current)
    return result


def source_ref(path: Path, source_hash: str, heading: str, start: int, end: int, quotation: str) -> dict:
    return {"path_or_uri":str(path.resolve()),"source_hash":source_hash,"heading":heading,"line_start":start,"line_end":end,"quotation":quotation,"quotation_hash":text_hash(quotation)}


def infer_type(label: str) -> str:
    upper = label.upper()
    if "BR" in upper or "IDENTIFICATION" in upper: return "bridge"
    if "T/" in upper or upper.startswith("T"): return "theological"
    if "E" in upper or "HY_EVIDENCE" in upper: return "empirical"
    if "D" in upper or "LN" in upper or "AX_SCAFFOLD" in upper: return "mathematical"
    return "universal"


def proposal(identifier: str, claim: str, plain: str, claim_type: str, source: dict, open_items: list[str], incomplete: str | None = None) -> dict:
    value = {"source_object_id":identifier,"status":STATUS,"operation":"new_claim","claim":claim.strip(),"plain_language":plain.strip(),"claim_type":claim_type,"defeat_condition":"Human review finds the quotation was split incorrectly, stripped of a necessary qualifier, or assigned a burden not licensed by its source.","present_evidence":[],"open_items":open_items,"source":source,"canonical_promotion_requested":False,"canonical_language_enabled":True,"candidate_version":"0.1.0"}
    if incomplete: value["discovery_incomplete_reason"] = incomplete
    return value


def parse_ledger(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines(); headings = headings_by_line(lines); digest = file_hash(path); rows = []
    pattern = re.compile(r"^\|\s*(GT-[A-Z0-9-]+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$")
    for index, line in enumerate(lines, 1):
        match = pattern.match(line)
        if not match: continue
        identifier, claim, classification, boundary = match.groups()
        rows.append(proposal(identifier, claim, claim, infer_type(classification), source_ref(path,digest,headings[index-1],index,index,claim), [boundary]))
    return rows


def chain_entries(path: Path) -> list[tuple[int,int,str]]:
    lines = path.read_text(encoding="utf-8").splitlines(); entries=[]; in_fence=False; start=None; buffer=[]
    id_start = re.compile(r"^\s*([A-Z][A-Z0-9]*\d+(?:\.\d+)?[a-z]?)\s+.+")
    for number, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            if start is not None: entries.append((start, number-1, "\n".join(buffer))); start=None; buffer=[]
            in_fence = not in_fence; continue
        if not in_fence: continue
        if id_start.match(line):
            if start is not None: entries.append((start, number-1, "\n".join(buffer)))
            start=number; buffer=[line]
        elif start is not None and (line.startswith(" ") or line.strip()): buffer.append(line)
    if start is not None: entries.append((start,len(lines),"\n".join(buffer)))
    return entries


def parse_chain(path: Path) -> list[dict]:
    lines=path.read_text(encoding="utf-8").splitlines(); headings=headings_by_line(lines); digest=file_hash(path); rows=[]
    first = re.compile(r"^\s*([A-Z][A-Z0-9]*\d+(?:\.\d+)?[a-z]?)\s+(.+?)(?:\s+[←â].*)?$")
    ruleable = re.compile(r"\b(is|are|exists|enables|requires|required|cannot|preserved|derives|entails|equals|=|≠)\b", re.I)
    for start,end,quote in chain_entries(path):
        match=first.match(quote.splitlines()[0])
        if not match: continue
        identifier,title=match.groups(); title=re.split(r"\s+(?:←|â†)",title,1)[0].strip()
        reason = None if ruleable.search(title) else "The sealed chain supplies a catalog label or bundled entry, not a confidently separable truth-apt proposition; human wording/splitting is required."
        rows.append(proposal(identifier,title,title,infer_type(quote),source_ref(path,digest,headings[start-1],start,end,quote),["Preserve the sealed grade, dependencies, repairs, and rivals as separately addressable fields."],reason))
    return rows


def unique_proposals(values: list[dict]) -> list[dict]:
    chosen: dict[tuple[str,str],dict] = {}; order=[]
    for value in values:
        key=(value["source"]["source_hash"],value["source_object_id"])
        if key not in chosen: chosen[key]=value; order.append(key); continue
        old=chosen[key]; old_quote=old["source"]["quotation"]; new_quote=value["source"]["quotation"]
        old_score=("←" in old_quote or "â†" in old_quote,len(old_quote)); new_score=("←" in new_quote or "â†" in new_quote,len(new_quote))
        if new_score > old_score: chosen[key]=value
    return [chosen[key] for key in order]


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--ledger",default=str(DEFAULT_LEDGER)); parser.add_argument("--chain",default=str(DEFAULT_CHAIN)); parser.add_argument("--output-root",required=True); parser.add_argument("--provider",choices=("mock","deepseek"),default="mock"); parser.add_argument("--model",default="deepseek-chat"); parser.add_argument("--limit",type=int); args=parser.parse_args()
    ledger=Path(args.ledger).resolve(); chain=Path(args.chain).resolve()
    if not ledger.is_file() or not chain.is_file(): raise SystemExit("ledger and sealed chain must both exist")
    values=unique_proposals(parse_ledger(ledger)+parse_chain(chain)); values=values[:args.limit] if args.limit else values
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"); run=Path(args.output_root).resolve()/"_batch_ingestion"/stamp; proposals=run/"proposals"; receipts=run/"receipts"; split=run/"human_split_queue"
    for folder in (proposals,receipts,split): folder.mkdir(parents=True,exist_ok=True)
    pipeline=load_pipeline(); pipeline.RUNS=receipts; results=[]
    for value in values:
        safe=re.sub(r"[^A-Za-z0-9_.-]+","-",value["source_object_id"]); proposal_path=proposals/f"{safe}.proposal.json"; proposal_path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        receipt=pipeline.review(value,args.provider,args.model)
        split_path=None
        if receipt["final_status"]=="BLOCKED" and receipt["stages"][0]["status"]=="DISCOVERY_INCOMPLETE":
            queued={"status":STATUS,"reason":receipt["stages"][0]["output"]["open_questions"],"proposal_path":str(proposal_path),"source":value["source"],"human_action":"SPLIT or restate without overwriting the source, then submit a new candidate version.","canonical_admission_performed":False}
            split_path=split/f"{safe}.split.json"; split_path.write_text(json.dumps(queued,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        results.append({"id":value["source_object_id"],"proposal":str(proposal_path),"receipt":receipt["receipt_path"],"status":receipt["final_status"],"split_queue":str(split_path) if split_path else None})
    manifest={"batch_version":"ground-trial-source-ingestion/1.0.0","status":STATUS,"created_at":datetime.now(timezone.utc).isoformat(),"provider":args.provider,"sources":[{"role":"ground_trial_ledger","path":str(ledger),"sha256":file_hash(ledger)},{"role":"sealed_sequential_chain","path":str(chain),"sha256":file_hash(chain),"index_named_path":str(INDEX_NAMED_CHAIN),"index_named_path_exists":INDEX_NAMED_CHAIN.exists(),"pointer_drift":"OPEN" if not INDEX_NAMED_CHAIN.exists() else None}],"counts":{"submitted":len(results),"pass":sum(x["status"]=="PASS" for x in results),"human_split_queue":sum(x["split_queue"] is not None for x in results)},"results":results,"canonical_admission_performed":False}
    path=run/"BATCH_MANIFEST.json"; path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({**manifest,"manifest_path":str(path)},ensure_ascii=False,indent=2)); return 0


if __name__=="__main__": raise SystemExit(main())
