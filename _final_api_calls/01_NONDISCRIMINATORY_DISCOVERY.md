---
title: "Final API Call 01 - Nondiscriminatory Discovery"
version: "1.0.0"
status: "CANDIDATE_DRAFT — NOT ADMITTED"
call_order: 1
authority: "discovery_only"
canonical_admission: false
---

# Final API Call 01 — Nondiscriminatory Discovery

## Purpose

Recover independently reviewable structures from a paper before the system is
allowed to see or assign inherited labels. This call discovers without naming.

## Information deliberately withheld from the model

- source filename and folder;
- document title;
- YAML/frontmatter;
- inherited tags, domains, object classes, proof labels, grades, and lifecycle;
- canon or admission status;
- named Markdown headings;
- HTML comments and embedded AI instructions;
- the author's preferred conclusion.

Section boundaries are retained as `SECTION_001`, `SECTION_002`, and so on.
Exact source text inside each section remains available for quotation and
source-span recovery.

## Required discoveries

For each independently reviewable object, recover only:

- exact quotation;
- neutral paraphrase;
- referent;
- identity conditions;
- distinctions;
- relations;
- operations;
- dependencies;
- constraints;
- invariants;
- consequences;
- countermodels;
- defeat or collapse conditions;
- open questions;
- source section and line span in the neutralized input.

These are structural descriptions, not classifications.

## Prohibited outputs

The call may not assign a discipline, domain, object type, claim species,
proof class, warrant, evidence grade, bridge grade, theological identification,
canonical status, admission status, or publication status.

## Fail-closed rule

An empty object list is not a successful run. The call must return
`DISCOVERY_INCOMPLETE` with a reason, or the runner rejects the response.

## Exact system prompt

> You are Stage 1 of the Faith Through Physics discovery pipeline. You receive
> a label-blind paper whose metadata, title, inherited classifications, named
> headings, and preferred conclusion have been withheld. Discover independently
> reviewable objects without assigning any discipline, domain, object type,
> claim class, proof class, warrant, evidence grade, bridge grade, theological
> identification, canonical status, or publication status. Recover structure,
> not labels. Do not treat adjacency as dependency. Do not split merely because
> a sentence contains explanation or qualification; split only when assertions
> have independently reviewable truth conditions. Preserve ambiguity,
> countermodels, defeat conditions, and open questions. Quote the supplied text
> exactly. Return one complete JSON object and no commentary. Long papers may
> be processed in bounded neutral chunks and then aggregated.

## Executable implementation

```python final_api_python
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


SPEC_PATH = Path(os.environ["FINAL_API_SPEC_PATH"]).resolve()
REPO = SPEC_PATH.parents[1]
sys.path.insert(0, str(REPO / "_scripts"))

import claim_pipeline_service as pipeline


SYSTEM_PROMPT = """You are Stage 1 of the Faith Through Physics discovery pipeline. You receive one bounded chunk of a label-blind paper whose metadata, title, inherited classifications, named headings, and preferred conclusion have been withheld. Discover independently reviewable objects without assigning any discipline, domain, object type, claim class, proof class, warrant, evidence grade, bridge grade, theological identification, canonical status, or publication status. Recover structure, not labels. Do not treat adjacency as dependency. Split only when assertions have independently reviewable truth conditions. Preserve ambiguity, countermodels, defeat conditions, and open questions. Quote supplied text exactly. Be compact. Return at most 10 objects. Each array within an object may contain at most 8 items of at most 24 words. Return JSON only with exactly: schema_version='paper-discovery/1.0.0'; stage='NONDISCRIMINATORY_DISCOVERY'; status (DISCOVERY_COMPLETE, DISCOVERY_INCOMPLETE, or BLOCKED); discovered_objects array; global_open_questions array; prohibited_outputs array. Each discovered object must contain: discovery_id, exact_quotation, neutral_paraphrase, referent, identity_conditions array, distinctions array, relations array, operations array, dependencies array, constraints array, invariants array, consequences array, countermodels array, collapse_conditions array, open_questions array, source_section, line_start, line_end. Line fields may be approximate because the runner binds exact lines after receipt. Do not include classification fields. If no object can be responsibly recovered, return DISCOVERY_INCOMPLETE and explain why."""

EMERGENT_PROMPT = """You are the blind organization pass. You receive frozen discoveries but no source filename, title, folder, inherited tags, discipline list, canon vocabulary, or preferred taxonomy. Organize the discoveries using categories that arise from the material itself. Do not use a supplied classification system because none is supplied. Categories may overlap when the material requires it. Identify objects that resist grouping, tensions between groups, and at least one plausible rival organization. These are emergent descriptive groupings, not canon labels, truth grades, or admission decisions. Return JSON only with exactly: schema_version='emergent-organization/1.0.0'; stage='BLIND_EMERGENT_ORGANIZATION'; organization_name; organizing_principle; groupings array; ungrouped_object_ids array; cross_group_tensions array; rival_organizations array; cautions array. Each grouping must contain label, definition, object_ids array, rationale, alternative_labels array. Use only supplied discovery IDs."""


FRONTMATTER = re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
HEADING = re.compile(r"^(#{1,6})\s+.*$", re.MULTILINE)


def digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def neutralize_markdown(text: str) -> tuple[str, dict]:
    text = FRONTMATTER.sub("", text, count=1)
    text = HTML_COMMENT.sub("", text)
    section = 0

    def replace_heading(match: re.Match[str]) -> str:
        nonlocal section
        section += 1
        return f"SECTION_{section:03d}"

    text = HEADING.sub(replace_heading, text)
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    neutral = "\n".join(lines).strip() + "\n"
    return neutral, {
        "named_headings_replaced": section,
        "frontmatter_withheld": True,
        "filename_withheld": True,
        "folder_withheld": True,
        "html_comments_withheld": True,
    }


def bounded_chunks(neutral: str, max_chars: int = 6500) -> list[str]:
    """Keep neutral section boundaries while bounding response size."""
    sections = re.split(r"(?=^SECTION_\d{3}$)", neutral, flags=re.MULTILINE)
    sections = [section.strip() for section in sections if section.strip()]
    chunks: list[str] = []
    current = ""
    for section in sections:
        pieces = [section]
        if len(section) > max_chars:
            pieces = [piece.strip() for piece in section.split("\n\n") if piece.strip()]
        for piece in pieces:
            if current and len(current) + len(piece) + 2 > max_chars:
                chunks.append(current.strip() + "\n")
                current = ""
            current += piece + "\n\n"
    if current.strip():
        chunks.append(current.strip() + "\n")
    return chunks or [neutral]


def bind_exact_location(item: dict, neutral: str) -> None:
    quote = item.get("exact_quotation", "")
    start = neutral.find(quote)
    if start < 0:
        lines = neutral.splitlines()
        reported_start = item.get("line_start")
        reported_end = item.get("line_end")
        if not isinstance(reported_start, int) or not isinstance(reported_end, int):
            raise ValueError("A non-exact quotation lacked usable source lines")
        if reported_start < 1 or reported_end < reported_start or reported_end > len(lines):
            raise ValueError("A non-exact quotation reported an invalid source range")
        item["model_quotation_candidate"] = quote
        quote = "\n".join(lines[reported_start - 1:reported_end]).strip()
        if not quote:
            raise ValueError("Reported source lines did not contain quotable text")
        item["exact_quotation"] = quote
        item["quotation_rebound_from_reported_lines"] = True
        start = neutral.find(quote)
        if start < 0:
            raise ValueError("Runner could not bind quotation to source text")
    line_start = neutral.count("\n", 0, start) + 1
    prior = neutral[:start].splitlines()
    section = next(
        (line for line in reversed(prior) if re.fullmatch(r"SECTION_\d{3}", line)),
        "SECTION_000",
    )
    item["source_section"] = section
    item["line_start"] = line_start
    item["line_end"] = line_start + quote.count("\n")


def mock_discovery(neutral: str) -> dict:
    lines = neutral.splitlines()
    quotation = next(
        (line.strip() for line in lines if line.strip() and not line.startswith("SECTION_")),
        "",
    )
    if not quotation:
        return {
            "schema_version": "paper-discovery/1.0.0",
            "stage": "NONDISCRIMINATORY_DISCOVERY",
            "status": "DISCOVERY_INCOMPLETE",
            "discovered_objects": [],
            "global_open_questions": ["No non-heading source text remained after neutralization."],
            "prohibited_outputs": ["All classification and canon fields withheld."],
        }
    line_number = lines.index(quotation) + 1 if quotation in lines else 1
    return {
        "schema_version": "paper-discovery/1.0.0",
        "stage": "NONDISCRIMINATORY_DISCOVERY",
        "status": "DISCOVERY_COMPLETE",
        "discovered_objects": [{
            "discovery_id": "DISC-001",
            "exact_quotation": quotation,
            "neutral_paraphrase": quotation,
            "referent": "The referent remains to be discriminated.",
            "identity_conditions": [],
            "distinctions": ["The assertion remains distinct from its negation."],
            "relations": [],
            "operations": [],
            "dependencies": [],
            "constraints": [],
            "invariants": [],
            "consequences": [],
            "countermodels": ["The exact negation remains a live comparison."],
            "collapse_conditions": [],
            "open_questions": ["Live semantic discovery was not called in mock mode."],
            "source_section": "SECTION_001",
            "line_start": line_number,
            "line_end": line_number,
        }],
        "global_open_questions": [],
        "prohibited_outputs": ["All classification and canon fields withheld."],
    }


def validate(output: dict, neutral: str) -> None:
    required = {
        "schema_version", "stage", "status", "discovered_objects",
        "global_open_questions", "prohibited_outputs",
    }
    missing = sorted(required - set(output))
    if missing:
        raise ValueError("Discovery output missing: " + ", ".join(missing))
    if output["stage"] != "NONDISCRIMINATORY_DISCOVERY":
        raise ValueError("Wrong discovery stage")
    objects = output["discovered_objects"]
    if output["status"] == "DISCOVERY_COMPLETE" and not objects:
        raise ValueError("Empty discovery cannot be marked complete")
    forbidden = {
        "domain", "discipline", "object_type", "claim_class", "claim_species",
        "proof_class", "proof_label", "warrant", "evidence_grade", "bridge_grade",
        "theological_identification", "canonical_status", "admission_status",
    }
    for item in objects:
        leaked = sorted(forbidden & set(item))
        if leaked:
            raise ValueError("Stage 1 leaked classifications: " + ", ".join(leaked))
        bind_exact_location(item, neutral)


def plain_value(value) -> str:
    if not isinstance(value, dict):
        return str(value)
    if value.get("tension"):
        ids = ", ".join(value.get("object_ids") or [])
        return f"{value['tension']}" + (f" Objects involved: {ids}." if ids else "")
    if value.get("organization_name"):
        groups = "; ".join(
            f"{group.get('label', 'Unnamed')}: {', '.join(group.get('object_ids') or [])}"
            for group in value.get("groupings") or []
        )
        text = f"{value['organization_name']} -- {value.get('organizing_principle', 'No principle stated.')}"
        return text + (f" Groups: {groups}." if groups else "")
    return json.dumps(value, ensure_ascii=False)


def markdown_list(values: list) -> str:
    return "\n".join(f"- {plain_value(value)}" for value in values) if values else "- None recovered."


def write_plain_english_projection(receipt: dict, destination: Path) -> None:
    discovery = receipt["frozen_discovery"]
    source = receipt["post_discovery_source_binding"]
    lines = [
        "---",
        'status: "CANDIDATE_DRAFT — NOT ADMITTED"',
        'projection: "nondiscriminatory-discovery"',
        "canonical_admission: false",
        "---",
        "",
        "# Nondiscriminatory Discovery — Plain-English Review",
        "",
        "> **CANDIDATE_DRAFT — NOT ADMITTED.** This is a discovery projection, not a classification, proof, truth grade, or admission event.",
        "",
        "## What this report did",
        "",
        "It read a label-blind form of the source paper. The model did not receive its filename, folder, title, YAML, inherited tags, domain, proof labels, or canon status.",
        "",
        f"- Source: `{source['path']}`",
        f"- Source hash: `{source['source_hash']}`",
        f"- Discovery status: `{discovery['status']}`",
        f"- Objects recovered: **{len(discovery['discovered_objects'])}**",
        "- Source modified: **No**",
        "- Canonical admission performed: **No**",
        "",
    ]
    organization = receipt.get("emergent_organization") or {}
    if organization:
        lines.extend([
            "## How the blind pass organized the material",
            "",
            "> These are the model's own descriptive groupings, formed before it saw inherited Canonization labels. They are proposals, not controlled classifications.",
            "",
            f"**Organization:** {organization.get('organization_name', 'Unnamed organization')}",
            "",
            f"**Organizing principle:** {organization.get('organizing_principle', 'Not stated.')}",
            "",
        ])
        for group in organization.get("groupings") or []:
            lines.extend([
                f"### {group.get('label', 'Unnamed grouping')}",
                "",
                str(group.get("definition") or "No definition supplied."),
                "",
                f"- Objects: {', '.join(group.get('object_ids') or []) or 'None'}",
                f"- Why they belong together: {group.get('rationale') or 'Not stated.'}",
                f"- Other possible names: {', '.join(group.get('alternative_labels') or []) or 'None'}",
                "",
            ])
        lines.extend([
            "### Material that resisted grouping",
            "",
            markdown_list(organization.get("ungrouped_object_ids") or []),
            "",
            "### Tensions between groupings",
            "",
            markdown_list(organization.get("cross_group_tensions") or []),
            "",
            "### Rival ways to organize the same discoveries",
            "",
            markdown_list(organization.get("rival_organizations") or []),
            "",
        ])
    for index, item in enumerate(discovery["discovered_objects"], start=1):
        quotation = str(item.get("exact_quotation", "")).replace("\n", "\n> ")
        lines.extend([
            f"## {index}. Discovered object",
            "",
            "### Exact source wording",
            "",
            f"> {quotation}",
            "",
            f"**Plain meaning:** {item.get('neutral_paraphrase') or 'Not recovered.'}",
            "",
            f"**What it refers to:** {item.get('referent') or 'Still open.'}",
            "",
            f"**Source location:** `{item.get('source_section')}`, neutralized lines {item.get('line_start')}–{item.get('line_end')}",
            "",
            "### Identity conditions",
            "",
            markdown_list(item.get("identity_conditions") or []),
            "",
            "### Distinctions",
            "",
            markdown_list(item.get("distinctions") or []),
            "",
            "### Relations and operations",
            "",
            markdown_list((item.get("relations") or []) + (item.get("operations") or [])),
            "",
            "### Dependencies and constraints",
            "",
            markdown_list((item.get("dependencies") or []) + (item.get("constraints") or [])),
            "",
            "### Invariants and consequences",
            "",
            markdown_list((item.get("invariants") or []) + (item.get("consequences") or [])),
            "",
            "### Countermodels and collapse conditions",
            "",
            markdown_list((item.get("countermodels") or []) + (item.get("collapse_conditions") or [])),
            "",
            "### What remains open",
            "",
            markdown_list(item.get("open_questions") or []),
            "",
        ])
    lines.extend([
        "## Global open questions",
        "",
        markdown_list(discovery.get("global_open_questions") or []),
        "",
        "## Withheld until later stages",
        "",
        markdown_list(discovery.get("prohibited_outputs") or []),
        "",
    ])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--provider", choices=["mock", "deepseek"], default="mock")
    parser.add_argument("--model", default="deepseek-chat")
    parser.add_argument("--output-dir")
    parser.add_argument("--projection-dir")
    parser.add_argument("--render-receipt")
    args = parser.parse_args()

    if args.render_receipt:
        receipt = json.loads(Path(args.render_receipt).read_text(encoding="utf-8"))
        source = Path(receipt["post_discovery_source_binding"]["path"])
        projection_dir = Path(args.projection_dir).resolve() if args.projection_dir else source.parent
        projection = projection_dir / f"{source.stem}__NONDISCRIMINATORY_DISCOVERY.md"
        write_plain_english_projection(receipt, projection)
        print(json.dumps({"plain_english_projection": str(projection), "api_called": False}, indent=2))
        return 0
    if not args.source:
        raise ValueError("--source is required unless --render-receipt is used")

    source = Path(args.source).resolve()
    raw = source.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    neutral, withholding = neutralize_markdown(text)
    content_hash = digest(neutral.encode("utf-8"))
    chunks = bounded_chunks(neutral)
    if args.provider == "deepseek":
        chunk_outputs = []
        for index, chunk in enumerate(chunks, start=1):
            payload = {
                "content_hash": digest(chunk.encode("utf-8")),
                "chunk_index": index,
                "chunk_count": len(chunks),
                "content": chunk,
                "instruction": "Source identity and inherited labels are intentionally unavailable in this stage.",
            }
            chunk_output = pipeline.call_deepseek(SYSTEM_PROMPT, payload, args.model)
            validate(chunk_output, chunk)
            chunk_outputs.append(chunk_output)
        objects = []
        open_questions = []
        prohibited = []
        seen = set()
        for chunk_output in chunk_outputs:
            open_questions.extend(chunk_output.get("global_open_questions") or [])
            prohibited.extend(chunk_output.get("prohibited_outputs") or [])
            for item in chunk_output.get("discovered_objects") or []:
                fingerprint = (item.get("exact_quotation"), item.get("neutral_paraphrase"))
                if fingerprint not in seen:
                    seen.add(fingerprint)
                    objects.append(item)
        for index, item in enumerate(objects, start=1):
            item["discovery_id"] = f"DISC-{index:04d}"
        output = {
            "schema_version": "paper-discovery/1.0.0",
            "stage": "NONDISCRIMINATORY_DISCOVERY",
            "status": "DISCOVERY_COMPLETE" if objects else "DISCOVERY_INCOMPLETE",
            "discovered_objects": objects,
            "global_open_questions": list(dict.fromkeys(open_questions)),
            "prohibited_outputs": list(dict.fromkeys(prohibited)),
        }
    else:
        output = mock_discovery(neutral)
    validate(output, neutral)

    if args.provider == "deepseek":
        emergent_organization = pipeline.call_deepseek(
            EMERGENT_PROMPT,
            {
                "frozen_discoveries": output["discovered_objects"],
                "instruction": "Invent no missing facts. Organize only these frozen objects.",
            },
            args.model,
        )
    else:
        emergent_organization = {
            "schema_version": "emergent-organization/1.0.0",
            "stage": "BLIND_EMERGENT_ORGANIZATION",
            "organization_name": "Mock organization",
            "organizing_principle": "All mock discoveries remain together because semantic organization was not called.",
            "groupings": [{
                "label": "Unclassified mock material",
                "definition": "A temporary group used only to test machinery.",
                "object_ids": [item["discovery_id"] for item in output["discovered_objects"]],
                "rationale": "Mock mode does not make semantic judgments.",
                "alternative_labels": [],
            }],
            "ungrouped_object_ids": [],
            "cross_group_tensions": [],
            "rival_organizations": [],
            "cautions": ["This organization is a test fixture, not a semantic result."],
        }
    valid_ids = {item["discovery_id"] for item in output["discovered_objects"]}
    if emergent_organization.get("stage") != "BLIND_EMERGENT_ORGANIZATION":
        raise ValueError("Emergent organization returned the wrong stage")
    referenced_ids = {
        object_id
        for group in emergent_organization.get("groupings") or []
        for object_id in group.get("object_ids") or []
    } | set(emergent_organization.get("ungrouped_object_ids") or [])
    unknown_ids = sorted(referenced_ids - valid_ids)
    if unknown_ids:
        raise ValueError("Emergent organization invented discovery IDs: " + ", ".join(unknown_ids))

    receipt = {
        "receipt_version": "final-api-call/1.0.0",
        "status": "CANDIDATE_DRAFT — NOT ADMITTED",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "call": "01_NONDISCRIMINATORY_DISCOVERY",
        "provider": args.provider,
        "model": args.model,
        "blind_input": {
            "content_hash": content_hash,
            "withholding": withholding,
            "chunk_count": len(chunks),
        },
        "frozen_discovery": output,
        "emergent_organization": emergent_organization,
        "post_discovery_source_binding": {
            "path": str(source),
            "source_hash": digest(raw),
        },
        "source_modified": False,
        "canonical_admission_performed": False,
        "human_ruling_required": True,
    }
    out_dir = Path(args.output_dir).resolve() if args.output_dir else REPO / "_runtime" / "final_api_calls"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = out_dir / f"{stamp}__01_nondiscriminatory_discovery.json"
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    projection = None
    if args.projection_dir:
        projection = Path(args.projection_dir).resolve() / f"{source.stem}__NONDISCRIMINATORY_DISCOVERY.md"
        write_plain_english_projection(receipt, projection)
    print(json.dumps({
        "status": output["status"],
        "object_count": len(output["discovered_objects"]),
        "receipt": str(out),
        "plain_english_projection": str(projection) if projection else None,
        "source_modified": False,
        "canonical_admission_performed": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
