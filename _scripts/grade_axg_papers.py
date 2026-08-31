#!/usr/bin/env python3
"""Grade proposed AX-GND papers and produce paragraph-thread hinge audits."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("claim_pipeline_service",HERE/"claim_pipeline_service.py")
service=importlib.util.module_from_spec(spec); spec.loader.exec_module(service)

SYSTEM="""You are the Faith Through Physics writing and argument reviewer. Grade a PROPOSED paper without grading its truth by literary force.

Keep two judgments separate:
1. Writing/argument quality: how well the draft states and carries its declared argument.
2. Epistemic readiness: whether its assertions are sufficiently exposed to enter later discovery/classification. This is not a truth grade and not canonical admission.

Writing score is 0-100. Score eight dimensions 0-10: opening_promise, central_thread, paragraph_hinges, meaning_before_mechanism, argumentative_progression, objection_fairness, ending_payment, voice_and_clarity. total_score must equal round(sum(dimensions)*1.25). Letter: A 93-100, A- 90-92, B+ 87-89, B 83-86, B- 80-82, C+ 77-79, C 73-76, C- 70-72, D 60-69, F below 60.

For each substantive prose paragraph, ask: What can the reader now see that they could not see one paragraph ago? Assign ADVANCES, HOLDS, REPEATS, DRIFTS, or BREAKS. Name the paragraph function. Quote or accurately identify its current final line. Supply a stronger hinge only when useful; never intensify beyond the evidence. Hinge types: Surface to Substrate, Personal to Universal, Mechanism to Meaning, Cause to Reversal, Question to Better Question, Local Result to Larger Consequence, or NONE.

Return valid JSON only with exactly:
{
 "schema_version":"paper-grade-thread-review/1.0.0",
 "paper_id":string,
 "writing_grade":{"total_score":integer,"letter":string,"dimensions":{eight named integer scores},"strengths":[string],"weaknesses":[string]},
 "epistemic_readiness":{"status":"READY_FOR_NEXT_DISCOVERY|NEEDS_DISCOVERY_REVISION|BRIDGE_BOUNDARY_REQUIRED|HOLD_OPEN","reasons":[string],"not_a_truth_grade":true},
 "central_thread":string,
 "opening_debt":string,
 "ending_payment":string,
 "paragraph_trace":[{"paragraph_id":"P01", "opening_words":string,"function":string,"new_seeing":string,"thread_status":"ADVANCES|HOLDS|REPEATS|DRIFTS|BREAKS","hinge_type":string,"current_final_line":string,"better_hinge":string_or_null,"revision_needed":boolean}],
 "strongest_objection":string,
 "rewrite_priorities":[{"priority":integer,"location":string,"action":string,"reason":string}],
 "verdict":string,
 "canonical_promotion_performed":false
}

Ignore YAML, callouts, receipt metadata, lists, and headings when counting substantive paragraphs. Preserve the paper's disclosed Christian frame. Be strict but constructive. Complete the JSON."""


def safe(value:str)->str: return re.sub(r"[^A-Za-z0-9]+","_",value).strip("_").upper()

def letter_for(score:int)->str:
    if score>=93:return "A"
    if score>=90:return "A-"
    if score>=87:return "B+"
    if score>=83:return "B"
    if score>=80:return "B-"
    if score>=77:return "C+"
    if score>=73:return "C"
    if score>=70:return "C-"
    if score>=60:return "D"
    return "F"


def main():
    p=argparse.ArgumentParser(); p.add_argument("--draft-dir",required=True); p.add_argument("--output-dir",required=True); p.add_argument("--model",default="deepseek-chat"); p.add_argument("--start-paper"); p.add_argument("--limit",type=int); a=p.parse_args()
    drafts=sorted(Path(a.draft_dir).resolve().glob("AXG-P*.md")); out=Path(a.output_dir).resolve(); out.mkdir(parents=True,exist_ok=True); json_dir=out/"json"; json_dir.mkdir(exist_ok=True)
    if a.start_paper: drafts=[f for f in drafts if re.match(r"AXG-P\d+",f.name).group(0)>=a.start_paper]
    if a.limit: drafts=drafts[:a.limit]
    rows=[]
    for i,path in enumerate(drafts,1):
        paper_id=re.match(r"AXG-P\d+",path.name).group(0); text=path.read_text(encoding="utf-8",errors="replace")
        print(f"[{i}/{len(drafts)}] grading {paper_id}",flush=True)
        review=service.call_deepseek(SYSTEM,{"paper_id":paper_id,"paper_markdown":text},a.model)
        service.require_fields(review,["schema_version","paper_id","writing_grade","epistemic_readiness","central_thread","opening_debt","ending_payment","paragraph_trace","strongest_objection","rewrite_priorities","verdict","canonical_promotion_performed"],paper_id)
        if review["paper_id"]!=paper_id or review["canonical_promotion_performed"] is not False: raise SystemExit(f"{paper_id} identity or authority failure")
        dims=review["writing_grade"]["dimensions"]; expected=round(sum(int(v) for v in dims.values())*1.25)
        if int(review["writing_grade"]["total_score"])!=expected: review["writing_grade"]["total_score"]=expected; review["writing_grade"]["score_recomputed_by_validator"]=True
        normalized_letter=letter_for(expected)
        if review["writing_grade"].get("letter")!=normalized_letter:
            review["writing_grade"]["api_reported_letter"]=review["writing_grade"].get("letter")
            review["writing_grade"]["letter"]=normalized_letter
            review["writing_grade"]["letter_normalized_by_validator"]=True
        receipt={"review_receipt_version":"paper-grade-thread-review-receipt/1.0.0","provider":"deepseek","model":a.model,"source_draft":str(path),"source_draft_hash":service.sha({"text":text}),"canonical_promotion_performed":False,"review":review}
        base=path.stem
        (json_dir/f"{base}.grade-thread.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        g=review["writing_grade"]; ep=review["epistemic_readiness"]
        md=["---",f'title: "{paper_id} — Grade and Continuous Thread"',f'paper_id: "{paper_id}"','status: "REVIEW RECEIPT — NOT CANON"',f'writing_score: {g["total_score"]}',f'writing_grade: "{g["letter"]}"',f'epistemic_readiness: "{ep["status"]}"',"canonical_promotion_performed: false","---","",f"# {paper_id} — Grade and Continuous Thread","",f"## Writing grade: {g['letter']} — {g['total_score']}/100","","| Dimension | Score / 10 |","|---|---:|"]
        for k,v in g["dimensions"].items(): md.append(f"| {k.replace('_',' ').title()} | {v} |")
        md.extend(["","## Central thread","",review["central_thread"],"","## Opening debt","",review["opening_debt"],"","## Ending payment","",review["ending_payment"],"","## Epistemic readiness","",f"**{ep['status']}** — this is not a truth grade.",""])
        for reason in ep["reasons"]: md.append(f"- {reason}")
        md.extend(["","## Paragraph thread and hinge layer","","| ¶ | Function | Thread | New seeing | Better hinge |","|---|---|---|---|---|"])
        for t in review["paragraph_trace"]:
            hinge=(t.get("better_hinge") or "—").replace("|","\\|").replace("\n"," "); new=t["new_seeing"].replace("|","\\|").replace("\n"," "); md.append(f"| {t['paragraph_id']} | {t['function']} | **{t['thread_status']}** | {new} | {hinge} |")
        md.extend(["","## Strongest objection","",review["strongest_objection"],"","## Rewrite priorities",""])
        for item in sorted(review["rewrite_priorities"],key=lambda x:x["priority"]): md.append(f"{item['priority']}. **{item['location']}** — {item['action']}  \n   {item['reason']}")
        md.extend(["","## Verdict","",review["verdict"],""])
        (out/f"{base}.GRADE_AND_THREAD.md").write_text("\n".join(md),encoding="utf-8")
        counts={s:sum(1 for t in review["paragraph_trace"] if t["thread_status"]==s) for s in ["ADVANCES","HOLDS","REPEATS","DRIFTS","BREAKS"]}
        rows.append({"paper_id":paper_id,"title":path.stem,"score":g["total_score"],"letter":g["letter"],"readiness":ep["status"],"paragraphs":len(review["paragraph_trace"]),**counts})
        time.sleep(.35)
    (out/"GRADE_SUMMARY.json").write_text(json.dumps({"summary_version":"axg-grade-summary/1.0.0","papers":rows,"canonical_promotion_performed":False},indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"graded":len(rows),"output":str(out)},indent=2),flush=True)

if __name__=="__main__": main()
