#!/usr/bin/env python3
"""Draft cohesive proposed papers from validated AX-GND extraction packets."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("claim_pipeline_service", HERE / "claim_pipeline_service.py")
service = importlib.util.module_from_spec(spec); spec.loader.exec_module(service)

SYSTEM = """You are drafting one proposed extraction paper from David Lowe's Part Zero — The Ground.

This is extraction, not invention. Preserve David's direct voice, Christian premise, technical distinctions, and human meaning. Do not flatten theology into generic spirituality. Do not present a disclosed premise as a scientific conclusion. Do not promote a bridge into proof. Do not invent quotations, citations, equations, facts, or source claims.

Use meaning before mechanism. Build a cohesive paper rather than an outline. The opening must create a question the paper actually pays. Make each component visible, but do not paste ledger language mechanically. State the strongest rival fairly. Put the weakest inferential seam in the open. Return to the opening in the ending.

Return valid JSON only with exactly:
{
  "paper_id": string,
  "title": string,
  "status": "PROPOSED_EXTRACTION_DRAFT",
  "source_component_ids": [string],
  "central_thesis": string,
  "opening_promise": string,
  "strongest_rival": string,
  "warrant_boundaries": [string],
  "body_markdown": string,
  "ending_line": string,
  "open_questions": [string],
  "canonical_promotion_performed": false
}

Write 900-1400 words in body_markdown. Use section headings sparingly. Include a clearly labeled 'What this paper does not establish' section. Do not call anything proved unless the supplied source explicitly provides a proof receipt. Complete the JSON."""


def excerpts(lines: list[str], components: list[dict], radius: int = 18) -> str:
    ranges = []
    for c in components:
        n = int(c["source_line_start"]) - 1
        ranges.append((max(0,n-radius),min(len(lines),n+radius+1)))
    ranges.sort(); merged=[]
    for start,end in ranges:
        if merged and start <= merged[-1][1] + 3: merged[-1]=(merged[-1][0],max(merged[-1][1],end))
        else: merged.append((start,end))
    return "\n\n[...SOURCE CONTEXT BREAK...]\n\n".join("\n".join(f"{i+1}: {lines[i]}" for i in range(start,end)) for start,end in merged)


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+","_",value).strip("_").upper()


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--source",required=True); parser.add_argument("--catalog",required=True); parser.add_argument("--output-dir",required=True); parser.add_argument("--model",default="deepseek-chat"); parser.add_argument("--start-family"); parser.add_argument("--limit",type=int); args=parser.parse_args()
    source=Path(args.source).resolve(); envelope=json.loads(Path(args.catalog).read_text(encoding="utf-8")); catalog=envelope["catalog"]; output=Path(args.output_dir).resolve(); output.mkdir(parents=True,exist_ok=True); json_dir=output/"json"; json_dir.mkdir(exist_ok=True)
    lines=source.read_text(encoding="utf-8",errors="replace").splitlines(); by_id={c["component_id"]:c for c in catalog["components"]}; families=catalog["paper_families"]
    if args.start_family: families=[f for f in families if f["family_id"]>=args.start_family]
    if args.limit: families=families[:args.limit]
    for index,family in enumerate(families,1):
        components=[by_id[cid] for cid in family["component_ids"]]
        payload={"source":{"path":str(source),"sha256":envelope["source_hash"]},"family":family,"components":components,"source_context":excerpts(lines,components)}
        print(f"[{index}/{len(families)}] {family['family_id']} {family['working_title']}",flush=True)
        draft=service.call_deepseek(SYSTEM + "\n\nIdentity lock: copy paper_id and source_component_ids exactly from the supplied family. Do not add, remove, rename, reorder, or reinterpret an ID.",payload,args.model)
        service.require_fields(draft,["paper_id","title","status","source_component_ids","central_thesis","opening_promise","strongest_rival","warrant_boundaries","body_markdown","ending_line","open_questions","canonical_promotion_performed"],family["family_id"])
        base=f"{family['family_id']}_{safe_name(family['working_title'])}"
        (json_dir/f"{base}.candidate.json").write_text(json.dumps(draft,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        if draft["paper_id"] != family["family_id"] or sorted(draft["source_component_ids"]) != sorted(family["component_ids"]): raise SystemExit(f"{family['family_id']} did not preserve component identity; candidate retained")
        if draft["canonical_promotion_performed"] is not False: raise SystemExit("Draft attempted canonical promotion")
        result={"draft_receipt_version":"axg-paper-draft/1.0.0","provider":"deepseek","model":args.model,"catalog_hash":envelope["catalog_hash"],"canonical_promotion_performed":False,"draft":draft}
        (json_dir/f"{base}.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        md=["---",f'title: "{draft["title"]}"',f'paper_id: "{draft["paper_id"]}"','status: "PROPOSED EXTRACTION DRAFT — NOT CANON"',f'component_catalog_hash: "{envelope["catalog_hash"]}"',"canonical_promotion_performed: false","---","",f"# {draft['title']}","","> [!warning] Proposed extraction draft","> This working paper was extracted from Part Zero and requires human review, classification, and reconciliation before any admission.","",draft["body_markdown"].strip(),"","## Carrying line","",f"> **{draft['ending_line']}**","","## Draft receipt","",f"- Components: {', '.join(draft['source_component_ids'])}",f"- Central thesis: {draft['central_thesis']}",f"- Strongest rival: {draft['strongest_rival']}","- Canonical promotion performed: false",""]
        (output/f"{base}.md").write_text("\n".join(md),encoding="utf-8")
        time.sleep(0.4)
    print(json.dumps({"drafted":len(families),"output":str(output)},indent=2),flush=True)


if __name__=="__main__": main()
