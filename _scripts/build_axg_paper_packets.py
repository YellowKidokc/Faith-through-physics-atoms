#!/usr/bin/env python3
"""Build source-grounded proposed paper packets from the AX-GND component catalog."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_line(line: str) -> str:
    line = re.sub(r"^\s*>\s?", "", line).strip()
    line = re.sub(r"^#{1,6}\s+", "", line)
    return line


def source_excerpt(lines: list[str], line_number: int, radius: int = 5) -> str:
    start = max(0, line_number - 1 - radius)
    end = min(len(lines), line_number + radius)
    return "\n".join(lines[start:end]).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    source = Path(args.source).resolve(); catalog_path = Path(args.catalog).resolve(); output = Path(args.output_dir).resolve()
    text = source.read_text(encoding="utf-8", errors="replace"); lines = text.splitlines()
    envelope = json.loads(catalog_path.read_text(encoding="utf-8")); catalog = envelope["catalog"]
    by_id = {c["component_id"]: c for c in catalog["components"]}
    output.mkdir(parents=True, exist_ok=True); papers = output / "papers"; papers.mkdir(exist_ok=True)

    validation = []
    for component in catalog["components"]:
        anchor = component["verbatim_anchor"]
        exact = anchor in text
        n = int(component["source_line_start"])
        actual = clean_line(lines[n - 1]) if 1 <= n <= len(lines) else ""
        validation.append({"component_id":component["component_id"],"declared_line":n,"line_in_range":1 <= n <= len(lines),"declared_anchor":anchor,"anchor_exact_match":exact,"actual_source_line":actual})
    validation_doc = {"validation_version":"axg-component-validation/1.0.0","source_path":str(source),"source_sha256":"sha256:"+sha_text(text),"catalog_path":str(catalog_path),"catalog_hash":envelope["catalog_hash"],"exact_anchor_count":sum(1 for x in validation if x["anchor_exact_match"]),"component_count":len(validation),"rule":"The API receipt remains unchanged. Draft packets cite actual numbered source lines; nonmatching API anchors are not treated as quotations.","components":validation}
    (output / "AX-GND_v2.component-catalog.validation.json").write_text(json.dumps(validation_doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    index_rows = []
    for family in catalog["paper_families"]:
        comps = [by_id[cid] for cid in family["component_ids"]]
        filename = f"{family['family_id']}_{re.sub(r'[^A-Za-z0-9]+','_',family['working_title']).strip('_').upper()}.md"
        body = ["---",f'title: "{family["working_title"]}"',f'paper_id: "{family["family_id"]}"','status: "PROPOSED EXTRACTION PAPER — NOT CANON"',f'source: "{source}"',f'source_sha256: "sha256:{sha_text(text)}"',f'component_catalog_hash: "{envelope["catalog_hash"]}"',"canonical_promotion_performed: false","---","",f"# {family['working_title']}","","> [!warning] Working extraction paper","> This paper is a source-grounded decomposition of Part Zero. It is not yet classified, graded, reconciled, or canonical.","","## The question", "",family["central_question"],"","## Opening promise", "",family["opening_debt"],"","## Component spine",""]
        for c in comps:
            v = next(x for x in validation if x["component_id"] == c["component_id"])
            body.extend([f"### {c['component_id']} — {c['plain_assertion']}","",f"**Exact assertion:** {c['exact_assertion']}","",f"**Source:** line {c['source_line_start']}, `{c['source_heading']}`", "",f"**Actual source line:** {v['actual_source_line'] or '[blank or structural line; inspect surrounding excerpt]' }", "",f"**Dependencies:** {', '.join(c['depends_on']) or 'OPEN'}", "",f"**Must remain separate from:** {', '.join(c['must_not_be_bundled_with']) or 'none named'}", "",f"**Rival or negation:** {c['negation_or_rival']}", "",f"**Defeat or narrowing condition:** {c['defeat_or_narrowing_condition']}", "",f"**Open:** {'; '.join(c['open_questions']) or 'none named'}", "","#### Source context","","```text",source_excerpt(lines,int(c["source_line_start"])),"```",""])
        body.extend(["## Closing debt","",family["closing_debt"],"","## Current boundary","","This extraction preserves what Part Zero says and exposes where its assertions separate. It does not yet decide the warrant, truth, grade, bridge strength, or admission status of any component.",""])
        (papers / filename).write_text("\n".join(body),encoding="utf-8")
        index_rows.append((family["family_id"],family["working_title"],len(comps),filename))

    idx = ["---",'title: "AX-GND v2 Decomposition — Working Index"','status: "PROPOSED — NOT CANON"',f'source_sha256: "sha256:{sha_text(text)}"',f'catalog_hash: "{envelope["catalog_hash"]}"',"---","","# AX-GND v2 Decomposition","","> Part Zero remains whole. These papers expose its internal joints without changing the canonical source.","","| Paper | Working title | Components | File |","|---|---|---:|---|"]
    for fid,title,count,filename in index_rows:
        idx.append(f"| {fid} | {title} | {count} | [[papers/{filename[:-3]}]] |")
    idx.extend(["","## Validation","",f"- Components: {len(validation)}",f"- Source line numbers in range: {sum(1 for x in validation if x['line_in_range'])}",f"- Exact API anchors: {sum(1 for x in validation if x['anchor_exact_match'])}",f"- Non-exact API anchors retained only in the immutable receipt: {sum(1 for x in validation if not x['anchor_exact_match'])}","","The proposed papers use numbered source context rather than treating a paraphrased API anchor as a quotation.",""])
    (output / "00_INDEX.md").write_text("\n".join(idx),encoding="utf-8")
    print(json.dumps({"papers":len(index_rows),"components":len(validation),"exact_anchors":sum(1 for x in validation if x["anchor_exact_match"]),"output":str(output)},indent=2))


if __name__ == "__main__": main()
