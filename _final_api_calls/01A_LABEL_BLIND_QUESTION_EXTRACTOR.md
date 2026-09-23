---
title: "Final API Call 01A - Label-Blind Guiding Question Extractor"
version: "1.0.1"
status: "CANDIDATE_DRAFT — NOT ADMITTED"
authority: "question_extraction_only"
canonical_admission: false
---

# Final API Call 01A — Label-Blind Guiding Question Extractor

## Purpose

Listen to a source before classification and recover the ordered questions that
the source leads a careful reader to ask. This stage does not answer, classify,
grade, canonize, or identify a preferred conclusion.

## Withheld from the model

- filename and folder;
- document title and frontmatter;
- named Markdown headings;
- inherited tags and classifications;
- canon status and preferred taxonomy.

Section boundaries become `SECTION_001`, `SECTION_002`, and so on. Source text
inside each section remains unchanged so every question can be rebound to exact
source cues.

## Output contract

Return one JSON object containing an ordered `guiding_questions` array. Every
question must contain:

- `id`;
- `question`;
- `exact_source_cues`;
- `why_reader_is_led_to_ask`;
- `source_section`;
- `line_start`;
- `line_end`.

The runner verifies exact cues against the neutralized source and replaces model
line estimates with deterministic source coordinates.

## Prohibited behavior

- Do not answer any question.
- Do not assign domains, disciplines, registers, object types, claim species,
  axiom types, proof classes, warrants, grades, or canon status.
- Do not turn assertions into leading questions that contain their answer.
- Do not manufacture questions merely because a topic word appears.
- Do not produce a complete summary or claim inventory.

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


SYSTEM_PROMPT = """You are a label-blind question extractor. Read the supplied source as a careful first-time reader and recover only the ordered questions the text is trying to make that reader ask. Listen; do not answer. Do not summarize the paper, extract a claim ledger, or classify anything. Do not assign a domain, discipline, register, object type, claim species, axiom type, proof class, warrant, grade, theology label, or canon status. Do not smuggle an answer into a leading question. Prefer a small sequence of load-bearing questions over many topical questions. Preserve the paper's progression: question -> tension -> deeper question. Every question must be genuinely implied by exact source language. Return JSON only with exactly: schema_version='guiding-questions/1.0.1'; stage='LABEL_BLIND_QUESTION_EXTRACTION'; status (QUESTIONS_COMPLETE, QUESTIONS_INCOMPLETE, or BLOCKED); guiding_questions array; prohibited_outputs array. Each guiding question must contain exactly: id, question, exact_source_cues array, why_reader_is_led_to_ask, source_section, line_start, line_end. Return 4 to 12 guiding questions unless the source supports fewer. exact_source_cues must contain one or two short verbatim quotations from the supplied source. Questions must end with a question mark. Do not include answers, summaries, observations, or non-question pressure statements anywhere in the output."""


FRONTMATTER = re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
HEADING = re.compile(r"^(#{1,6})\s+.*$", re.MULTILINE)
FORBIDDEN_KEYS = {
    "answer", "short_answer", "answer_status", "domain", "discipline", "register",
    "object_type", "claim_species", "axiom_type", "proof_class", "warrant",
    "evidence_grade", "bridge_grade", "theological_identification",
    "canonical_status", "admission_status",
}


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
    return "\n".join(lines).strip() + "\n", {
        "named_headings_replaced": section,
        "frontmatter_withheld": True,
        "filename_withheld": True,
        "folder_withheld": True,
        "html_comments_withheld": True,
    }


def all_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from all_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_keys(child)


def bind_question(item: dict, neutral: str) -> None:
    cues = item.get("exact_source_cues")
    if not isinstance(cues, list) or not 1 <= len(cues) <= 2:
        raise ValueError("Each question requires one or two exact source cues")
    positions = []
    for cue_index, cue in enumerate(cues):
        if not isinstance(cue, str) or not cue.strip():
            raise ValueError("Source cues must be non-empty strings")
        position = neutral.find(cue)
        if position < 0:
            position = neutral.lower().find(cue.lower())
            if position >= 0:
                cues[cue_index] = neutral[position:position + len(cue)]
            else:
                raise ValueError(f"Question cue was not an exact source quotation: {cue!r}")
        positions.append((position, position + len(cue)))
    start = min(position[0] for position in positions)
    end = max(position[1] for position in positions)
    item["line_start"] = neutral.count("\n", 0, start) + 1
    item["line_end"] = neutral.count("\n", 0, end) + 1
    preceding = neutral[:start].splitlines()
    item["source_section"] = next(
        (line for line in reversed(preceding) if re.fullmatch(r"SECTION_\d{3}", line)),
        "SECTION_000",
    )


def validate(output: dict, neutral: str) -> None:
    if set(output) != {
        "schema_version", "stage", "status", "guiding_questions",
        "prohibited_outputs",
    }:
        raise ValueError("Question output has missing or additional top-level fields")
    if output["schema_version"] != "guiding-questions/1.0.1":
        raise ValueError("Wrong question schema version")
    if output["stage"] != "LABEL_BLIND_QUESTION_EXTRACTION":
        raise ValueError("Wrong question extraction stage")
    questions = output["guiding_questions"]
    if output["status"] == "QUESTIONS_COMPLETE" and not questions:
        raise ValueError("Empty question list cannot be complete")
    if not isinstance(questions, list) or len(questions) > 12:
        raise ValueError("Question list must contain at most 12 items")
    leaked = sorted(FORBIDDEN_KEYS & set(all_keys(output)))
    if leaked:
        raise ValueError("Question stage leaked prohibited fields: " + ", ".join(leaked))
    expected_item_keys = {
        "id", "question", "exact_source_cues", "why_reader_is_led_to_ask",
        "source_section", "line_start", "line_end",
    }
    for index, item in enumerate(questions, 1):
        if set(item) != expected_item_keys:
            raise ValueError(f"Question {index} has missing or additional fields")
        item["id"] = f"Q{index:03d}"
        if not isinstance(item["question"], str) or not item["question"].strip().endswith("?"):
            raise ValueError("Every extracted question must end with a question mark")
        bind_question(item, neutral)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--provider", choices=["mock", "deepseek"], default="mock")
    parser.add_argument("--model", default="deepseek-chat")
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    raw = source.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    neutral, withheld = neutralize_markdown(text)

    if args.provider == "deepseek":
        output = pipeline.call_deepseek(SYSTEM_PROMPT, {"source": neutral}, args.model)
    else:
        first = next((line for line in neutral.splitlines() if line and not line.startswith("SECTION_")), "")
        output = {
            "schema_version": "guiding-questions/1.0.1",
            "stage": "LABEL_BLIND_QUESTION_EXTRACTION",
            "status": "QUESTIONS_INCOMPLETE",
            "guiding_questions": [],
            "prohibited_outputs": [f"Mock mode produced no answers or classifications; source began: {first[:80]}"],
        }
    validate(output, neutral)

    receipt = {
        "receipt_version": "final-api-question-extraction/1.0.0",
        "status": "CANDIDATE_DRAFT — NOT ADMITTED",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "call": "01A_LABEL_BLIND_QUESTION_EXTRACTOR",
        "provider": args.provider,
        "model": args.model,
        "blind_input": {"neutral_sha256": digest(neutral.encode("utf-8")), **withheld},
        "question_extraction": output,
        "post_extraction_source_binding": {"path": str(source), "source_hash": digest(raw)},
        "answers_generated": False,
        "classification_performed": False,
        "source_modified": False,
        "canonical_admission_performed": False,
        "human_ruling_required": True,
    }
    out_dir = Path(args.output_dir).resolve() if args.output_dir else REPO / "_runtime" / "final_api_calls"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = out_dir / f"{stamp}__01A_label_blind_questions.json"
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "question_count": len(output["guiding_questions"]),
        "receipt": str(out),
        "answers_generated": False,
        "classification_performed": False,
        "source_modified": False,
        "canonical_admission_performed": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Run

```powershell
python .\_final_api_calls\run_embedded_markdown.py `
  .\_final_api_calls\01A_LABEL_BLIND_QUESTION_EXTRACTOR.md `
  --source "C:\path\to\paper.md" `
  --provider deepseek `
  --output-dir "C:\path\to\60_EXCHANGE\CANDIDATE_JSON\QUESTION_TEST"
```

## Boundary

A successful receipt establishes only that guiding questions were extracted and
bound to source cues. It does not establish that the questions are answered,
that any source assertion is true, or that any object has been classified or
admitted.
