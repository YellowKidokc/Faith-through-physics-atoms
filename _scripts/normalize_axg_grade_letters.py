#!/usr/bin/env python3
"""Normalize existing AXG grade letters and rebuild the aggregate leaderboard."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def letter(score):
    return "A" if score>=93 else "A-" if score>=90 else "B+" if score>=87 else "B" if score>=83 else "B-" if score>=80 else "C+" if score>=77 else "C" if score>=73 else "C-" if score>=70 else "D" if score>=60 else "F"

def main():
    p=argparse.ArgumentParser();p.add_argument("--review-dir",required=True);a=p.parse_args();root=Path(a.review_dir).resolve();rows=[]
    for path in sorted((root/"json").glob("AXG-P*.grade-thread.json")):
        obj=json.loads(path.read_text(encoding="utf-8"));r=obj["review"];g=r["writing_grade"];score=int(g["total_score"]);new=letter(score)
        if g.get("letter")!=new:
            g.setdefault("api_reported_letter",g.get("letter"));g["letter"]=new;g["letter_normalized_by_validator"]=True
            path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        md_path=root/(path.name.replace(".grade-thread.json",".GRADE_AND_THREAD.md"));text=md_path.read_text(encoding="utf-8")
        text=re.sub(r'(?m)^writing_grade: ".*"$',f'writing_grade: "{new}"',text);text=re.sub(r'(?m)^## Writing grade: .* — \d+/100$',f'## Writing grade: {new} — {score}/100',text);md_path.write_text(text,encoding="utf-8")
        counts={s:sum(1 for t in r["paragraph_trace"] if t["thread_status"]==s) for s in ["ADVANCES","HOLDS","REPEATS","DRIFTS","BREAKS"]}
        rows.append({"paper_id":r["paper_id"],"title":md_path.stem,"score":score,"letter":new,"readiness":r["epistemic_readiness"]["status"],"paragraphs":len(r["paragraph_trace"]),**counts})
    summary={"summary_version":"axg-grade-summary/1.0.1","normalization_rule":"Letter derived deterministically from the ruled numeric thresholds.","papers":rows,"canonical_promotion_performed":False}
    (root/"GRADE_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    ordered=sorted(rows,key=lambda x:x["score"],reverse=True);avg=round(sum(x["score"] for x in rows)/len(rows),1)
    md=["---",'title: "AX-GND Draft Grades and Continuous-Thread Summary"','status: "REVIEW LAYER — NOT CANON"',f'average_score: {avg}',"canonical_promotion_performed: false","---","","# AX-GND Draft Grades and Continuous-Thread Summary","","> Writing grades measure draft construction, not truth. Epistemic readiness measures readiness for the next discovery pass, not admission.","","| Rank | Paper | Score | Grade | Epistemic readiness | Advance | Hold | Repeat | Drift | Break |","|---:|---|---:|---:|---|---:|---:|---:|---:|---:|"]
    for i,x in enumerate(ordered,1):md.append(f"| {i} | [[{x['title']}|{x['paper_id']}]] | {x['score']} | {x['letter']} | {x['readiness']} | {x['ADVANCES']} | {x['HOLDS']} | {x['REPEATS']} | {x['DRIFTS']} | {x['BREAKS']} |")
    totals={s:sum(x[s] for x in rows) for s in ["ADVANCES","HOLDS","REPEATS","DRIFTS","BREAKS"]}
    md.extend(["","## Corpus-level result","",f"- Average writing score: **{avg}/100**",f"- Paragraphs advancing the thread: **{totals['ADVANCES']}**",f"- Paragraphs holding position: **{totals['HOLDS']}**",f"- Paragraphs repeating: **{totals['REPEATS']}**",f"- Paragraphs drifting: **{totals['DRIFTS']}**",f"- Thread breaks: **{totals['BREAKS']}**","","## Next rewrite order","","Start with the lowest scores and the highest concentration of HOLD or REPEAT paragraphs. Apply proposed hinge lines only after checking that they preserve the actual warrant.",""])
    (root/"00_GRADE_AND_THREAD_SUMMARY.md").write_text("\n".join(md),encoding="utf-8")
    print(json.dumps({"papers":len(rows),"average":avg,"summary":str(root/'00_GRADE_AND_THREAD_SUMMARY.md')},indent=2))
if __name__=="__main__":main()
