#!/usr/bin/env python3
"""Meta claim extractor for canon assemblies.

Reads a large assembled canon markdown file, splits it into W#.# works, asks the
configured LLM to extract and classify claims, and writes a complete runtime log.

This script does not edit source documents and does not promote claims. It only
creates review artifacts under _runtime/meta_claim_extractor/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
RUNTIME = REPO / "_runtime" / "meta_claim_extractor"

DEFAULT_INPUT = Path(r"C:\theophysics\OPUS\CANON_ASSEMBLY\CANON_ASSEMBLED.md")

DEFENSE_CLASSES = {
    "ROOT",
    "AXIOM",
    "CLOSURE",
    "DERIVATION",
    "ADMISSION",
    "RHETORIC",
    "UNCLASSIFIED",
}

FRAMEWORK_LANES = {
    "physics",
    "master_equation",
    "ten_laws",
    "trinity",
    "axioms",
    "consciousness",
    "morality",
    "crown",
    "story",
    "meta",
    "other",
}

PHYSICS_CLAIM_TYPES = {
    "not_physics",
    "established_physics",
    "physics_model",
    "mathematical_formalism",
    "simulation_runtime",
    "empirical_prediction",
    "bridge_mapping",
    "theological_interpretation",
    "story_rendering",
}

EVIDENCE_LANES = {
    "none_needed",
    "lean_formal",
    "math_derivation",
    "python_runtime",
    "empirical_dataset",
    "historical_source",
    "scripture_theology",
    "philosophical_argument",
    "adversarial_review",
    "story_quality",
    "mixed",
}

FRAMEWORK_GLYPHS = {
    "physics": "physics",
    "master_equation": "master-equation",
    "ten_laws": "law",
    "trinity": "theology",
    "axioms": "axiom",
    "consciousness": "consciousness",
    "morality": "ethics",
    "crown": "cross",
    "story": "render-html",
    "meta": "mesh",
    "other": "claim",
}

PHYSICS_TYPE_GLYPHS = {
    "established_physics": "physics",
    "physics_model": "equation",
    "mathematical_formalism": "equation",
    "simulation_runtime": "python-verified",
    "empirical_prediction": "prediction",
    "bridge_mapping": "isomorphism",
    "theological_interpretation": "theology",
    "story_rendering": "render-html",
    "not_physics": "claim",
}

DEFENSE_GLYPHS = {
    "ROOT": "truth",
    "AXIOM": "axiom",
    "CLOSURE": "boundary",
    "DERIVATION": "proof",
    "ADMISSION": "doubt",
    "RHETORIC": "render-html",
    "UNCLASSIFIED": "claim",
}

EVIDENCE_GLYPHS = {
    "none_needed": "truth",
    "lean_formal": "lean4",
    "math_derivation": "equation",
    "python_runtime": "python-verified",
    "empirical_dataset": "evidence",
    "historical_source": "source-term",
    "scripture_theology": "theology",
    "philosophical_argument": "logos",
    "adversarial_review": "ai-validated",
    "story_quality": "render-html",
    "mixed": "binder",
}

ACTION_GLYPHS = {
    "keep": "canonical",
    "fix": "draft",
    "strengthen": "coherence",
    "demote": "boundary",
    "cut": "kill-condition",
    "quarantine": "deception",
    "needs_review": "doubt",
}

SYSTEM_PROMPT = """You are the Faith Through Physics canon meta-layer.

Task:
Extract explicit and implied claims from one work in the assembled canon.
Classify each claim honestly under the Defense Grid.

Defense Grid labels:
- ROOT: declared starting premise or root commitment.
- AXIOM: assumed formal rule or floor principle.
- CLOSURE: a claim that closes by self-reference, contradiction, or unavoidable entailment.
- DERIVATION: a claim derived from named premises, axioms, receipts, or earlier nodes.
- ADMISSION: a concession, limit, open problem, correction, kill condition, or "not proved" boundary.
- RHETORIC: story-layer, illustration, punchline, analogy, or public-facing speech that must not be treated as proof.
- UNCLASSIFIED: use only when the work is too unclear to classify.

Rules:
- Be conservative. Do not upgrade rhetoric into derivation.
- "Almost closure" is not a category.
- If a claim depends on a bridge, name the bridge and its weakness.
- Mark downhill layer claims, physics-overreach, invented precision, or proof inflation as risks.
- Keep file paths and source IDs exact.
- Return valid JSON only. No markdown fences.

JSON schema:
{
  "work_id": "W4.1",
  "title": "short title",
  "turn": "TURN 4 - GOD DEEPER",
  "source_path": "path if present, else empty string",
  "overall_status": "reviewed|needs_review|quarantine|empty",
  "summary": "brief review summary",
  "claims": [
    {
      "claim_id": "W4.1-C001",
      "claim_text": "one precise claim",
      "framework_lane": "physics|master_equation|ten_laws|trinity|axioms|consciousness|morality|crown|story|meta|other",
      "physics_claim_type": "not_physics|established_physics|physics_model|mathematical_formalism|simulation_runtime|empirical_prediction|bridge_mapping|theological_interpretation|story_rendering",
      "defense_class": "ROOT|AXIOM|CLOSURE|DERIVATION|ADMISSION|RHETORIC|UNCLASSIFIED",
      "claim_level": "formal|bridge|theological|physics|moral|story|editorial|meta",
      "evidence_lane": "none_needed|lean_formal|math_derivation|python_runtime|empirical_dataset|historical_source|scripture_theology|philosophical_argument|adversarial_review|story_quality|mixed",
      "evidence_needed": ["specific evidence this exact claim requires"],
      "evidence_present": ["specific evidence present in this work"],
      "evidence_gap": ["specific missing evidence"],
      "support": ["quoted or paraphrased support from this work"],
      "dependencies": ["A2", "W3.2", "Lean receipt", "none named"],
      "risks": ["specific risk or empty"],
      "kill_condition": "specific condition that would break this exact claim, or empty",
      "required_concession": "sentence to add before attack, or empty",
      "recommended_action": "keep|fix|strengthen|demote|cut|quarantine",
      "glyphs": ["semantic glyph ids if obvious; extractor will normalize if omitted"],
      "confidence": 0.0
    }
  ],
  "fixes": [
    {
      "severity": "P0|P1|P2|P3",
      "target": "phrase, section, or claim_id",
      "problem": "what is wrong",
      "repair": "specific repair"
    }
  ],
  "log_notes": ["anything the next pass must know"]
}
"""


def load_env() -> None:
    env_path = REPO / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and not os.environ.get(key):
            os.environ[key] = value


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def trim(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    head_len = max_chars * 2 // 3
    tail_len = max_chars - head_len
    return text[:head_len] + "\n\n[...TRUNCATED FOR META CLAIM REVIEW...]\n\n" + text[-tail_len:]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "untitled"


def extract_json(text: str) -> dict[str, Any]:
    clean = text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?\s*", "", clean)
        clean = re.sub(r"\s*```$", "", clean)
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        start, end = clean.find("{"), clean.rfind("}")
        if start >= 0 and end > start:
            return json.loads(clean[start : end + 1])
        raise


def normalize_choice(value: Any, allowed: set[str], default: str, uppercase: bool = False) -> str:
    raw = str(value or "").strip()
    candidate = raw.upper() if uppercase else raw.lower()
    return candidate if candidate in allowed else default


def unique(values: list[str]) -> list[str]:
    seen = set()
    out = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def glyph_path(glyph_id: str) -> str:
    return f"theophysics_glyphs/svg/{glyph_id}.svg"


def claim_glyphs(claim: dict[str, Any]) -> list[str]:
    action = normalize_choice(claim.get("recommended_action"), set(ACTION_GLYPHS), "needs_review")
    values = [
        FRAMEWORK_GLYPHS.get(claim["framework_lane"], "claim"),
        PHYSICS_TYPE_GLYPHS.get(claim["physics_claim_type"], "claim"),
        DEFENSE_GLYPHS.get(claim["defense_class"], "claim"),
        EVIDENCE_GLYPHS.get(claim["evidence_lane"], "binder"),
        ACTION_GLYPHS.get(action, "doubt"),
    ]
    if claim.get("kill_condition"):
        values.append("kill-condition")
    return unique(values)


def attach_classification_bundle(claim: dict[str, Any]) -> None:
    claim["framework_lane"] = normalize_choice(claim.get("framework_lane"), FRAMEWORK_LANES, "other")
    claim["physics_claim_type"] = normalize_choice(claim.get("physics_claim_type"), PHYSICS_CLAIM_TYPES, "not_physics")
    claim["defense_class"] = normalize_choice(claim.get("defense_class"), DEFENSE_CLASSES, "UNCLASSIFIED", uppercase=True)
    claim["evidence_lane"] = normalize_choice(claim.get("evidence_lane"), EVIDENCE_LANES, "mixed")
    claim["recommended_action"] = normalize_choice(
        claim.get("recommended_action"),
        set(ACTION_GLYPHS),
        "needs_review",
    )
    glyphs = claim_glyphs(claim)
    claim["glyphs"] = glyphs
    claim["glyph_paths"] = [glyph_path(item) for item in glyphs]
    claim["classification_bundle"] = {
        "framework_lane": claim["framework_lane"],
        "physics_claim_type": claim["physics_claim_type"],
        "defense_class": claim["defense_class"],
        "claim_level": claim.get("claim_level", "meta"),
        "evidence_lane": claim["evidence_lane"],
        "recommended_action": claim["recommended_action"],
        "glyphs": glyphs,
    }


def split_works(text: str) -> list[dict[str, str]]:
    turn = ""
    work_turn = ""
    pieces: list[dict[str, str]] = []
    pattern = re.compile(r"(?m)^(## TURN \d+[^\n]*|### W\d+\.\d+[^\n]*)")
    matches = list(pattern.finditer(text))
    work_start: re.Match[str] | None = None

    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        if heading.startswith("## TURN"):
            if work_start is not None:
                pieces.append(make_work(work_turn, work_start.group(1), text[work_start.start() : match.start()]))
                work_start = None
            turn = heading.replace("—", "-").replace("â€”", "-")
            continue
        if not heading.startswith("### W"):
            continue
        if work_start is not None:
            end = match.start()
            pieces.append(make_work(work_turn, work_start.group(1), text[work_start.start() : end]))
        work_start = match
        work_turn = turn

    if work_start is not None:
        pieces.append(make_work(turn, work_start.group(1), text[work_start.start() :]))

    return pieces


def make_work(turn: str, heading: str, body: str) -> dict[str, str]:
    cleaned_heading = heading.replace("—", "-").replace("â€”", "-").strip("# ")
    id_match = re.search(r"\b(W\d+\.\d+)\b", cleaned_heading)
    work_id = id_match.group(1) if id_match else "W?.?"
    title = re.sub(r"^W\d+\.\d+\s*[-:]*\s*", "", cleaned_heading).strip() or work_id
    source_match = re.search(r"\*\*Source:\*\*\s*`([^`]+)`", body)
    return {
        "work_id": work_id,
        "title": title,
        "turn": turn,
        "source_path": source_match.group(1) if source_match else "",
        "body": body.strip(),
    }


def provider_config(args: argparse.Namespace) -> dict[str, str]:
    endpoint = args.endpoint or os.environ.get("META_CLAIM_ENDPOINT", "")
    model = args.model or os.environ.get("META_CLAIM_MODEL", "")
    api_key = args.api_key or os.environ.get("META_CLAIM_API_KEY", "")

    if not endpoint and os.environ.get("DEEPSEEK_API_KEY"):
        endpoint = "https://api.deepseek.com/v1/chat/completions"
        model = model or "deepseek-chat"
        api_key = os.environ["DEEPSEEK_API_KEY"]
    if not endpoint and os.environ.get("OPENAI_API_KEY"):
        endpoint = "https://api.openai.com/v1/chat/completions"
        model = model or "gpt-4o"
        api_key = os.environ["OPENAI_API_KEY"]
    if not endpoint:
        raise SystemExit("No API key found. Set DEEPSEEK_API_KEY in .env or environment.")
    if not model:
        raise SystemExit("No model selected.")
    return {"endpoint": endpoint, "model": model, "api_key": api_key}


def call_api(prompt: str, cfg: dict[str, str], timeout: int, max_tokens: int) -> str:
    body = {
        "model": cfg["model"],
        "temperature": 0.1,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    if "deepseek.com" in cfg["endpoint"]:
        body["response_format"] = {"type": "json_object"}

    headers = {"Content-Type": "application/json"}
    if cfg["api_key"]:
        headers["Authorization"] = f"Bearer {cfg['api_key']}"
    req = urllib.request.Request(
        cfg["endpoint"],
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {error_body[:500]}") from exc

    return payload["choices"][0]["message"]["content"]


def make_prompt(work: dict[str, str], max_chars: int, max_claims: int) -> str:
    body = trim(work["body"], max_chars)
    return f"""Review this canon work and extract the top load-bearing claims.

Work id: {work["work_id"]}
Title: {work["title"]}
Turn: {work["turn"]}
Source path: {work["source_path"]}
Body SHA256: {sha256_text(work["body"])}

Remember:
- The goal is a meta-layer claim ledger.
- Do not rewrite the work.
- Pull out claims, classify defense class, name concessions, and log risks.
- Return at most {max_claims} claims.
- Prefer load-bearing claims, concessions, kill conditions, and overclaim risks.
- Do not list repeated restatements as separate claims.
- Every claim must have a specific framework_lane.
- If a claim touches physics, classify its physics_claim_type precisely.
- Evidence must match the claim type. Do not use general enthusiasm as evidence.
- Established physics needs recognized physics support.
- Mathematical formalism needs derivation or formal proof.
- Simulation/runtime claims need executable receipts.
- Empirical predictions need datasets, methods, dates, and falsification criteria.
- Bridge mappings need grade and boundary.
- Theological interpretations need theology/scripture/tradition or stated premise.
- Story renderings need story-quality review, not proof status.
- Keep each support item under 18 words.
- Keep each risk, dependency, and concession short.

Work:
---
{body}
---"""


def normalize_result(work: dict[str, str], data: dict[str, Any]) -> dict[str, Any]:
    data.setdefault("work_id", work["work_id"])
    data.setdefault("title", work["title"])
    data.setdefault("turn", work["turn"])
    data.setdefault("source_path", work["source_path"])
    data.setdefault("overall_status", "needs_review")
    data.setdefault("summary", "")
    data.setdefault("claims", [])
    data.setdefault("fixes", [])
    data.setdefault("log_notes", [])

    for index, claim in enumerate(data["claims"], start=1):
        if not claim.get("claim_id"):
            claim["claim_id"] = f"{work['work_id']}-C{index:03d}"
        claim.setdefault("claim_level", "meta")
        claim.setdefault("evidence_needed", [])
        claim.setdefault("evidence_present", [])
        claim.setdefault("evidence_gap", [])
        claim.setdefault("support", [])
        claim.setdefault("dependencies", [])
        claim.setdefault("risks", [])
        claim.setdefault("kill_condition", "")
        claim.setdefault("required_concession", "")
        claim.setdefault("confidence", 0.0)
        attach_classification_bundle(claim)
    return data


def write_outputs(run_dir: Path, results: list[dict[str, Any]], events: list[dict[str, Any]]) -> None:
    claims = []
    for result in results:
        for claim in result.get("claims", []):
            row = {
                "work_id": result["work_id"],
                "work_title": result["title"],
                "turn": result["turn"],
                "source_path": result.get("source_path", ""),
            }
            row.update(claim)
            claims.append(row)

    (run_dir / "meta_claims.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (run_dir / "meta_claims.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in claims),
        encoding="utf-8",
    )
    (run_dir / "run_log.jsonl").write_text(
        "".join(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n" for event in events),
        encoding="utf-8",
    )

    counts: dict[str, int] = {}
    framework_counts: dict[str, int] = {}
    evidence_counts: dict[str, int] = {}
    glyph_counts: dict[str, int] = {}
    for claim in claims:
        key = claim.get("defense_class", "UNCLASSIFIED")
        counts[key] = counts.get(key, 0) + 1
        framework = claim.get("framework_lane", "other")
        framework_counts[framework] = framework_counts.get(framework, 0) + 1
        evidence = claim.get("evidence_lane", "mixed")
        evidence_counts[evidence] = evidence_counts.get(evidence, 0) + 1
        for glyph_id in claim.get("glyphs", []):
            glyph_counts[glyph_id] = glyph_counts.get(glyph_id, 0) + 1

    lines = [
        "# Meta Claim Extraction Report",
        "",
        f"Generated: {now()}",
        f"Works reviewed: {len(results)}",
        f"Claims extracted: {len(claims)}",
        "",
        "## Defense Class Counts",
        "",
    ]
    lines += [f"- `{key}`: {counts[key]}" for key in sorted(counts)]
    lines += ["", "## Framework Lane Counts", ""]
    lines += [f"- `{key}`: {framework_counts[key]}" for key in sorted(framework_counts)]
    lines += ["", "## Evidence Lane Counts", ""]
    lines += [f"- `{key}`: {evidence_counts[key]}" for key in sorted(evidence_counts)]
    lines += ["", "## Glyph Counts", ""]
    lines += [f"- `{key}`: {glyph_counts[key]}" for key in sorted(glyph_counts)]
    lines += ["", "## Work Summaries", ""]
    for result in results:
        lines.append(f"### {result['work_id']} - {result['title']}")
        lines.append(f"- Status: `{result.get('overall_status', 'needs_review')}`")
        lines.append(f"- Claims: {len(result.get('claims', []))}")
        if result.get("summary"):
            lines.append(f"- Summary: {result['summary']}")
        for fix in result.get("fixes", []):
            lines.append(f"- {fix.get('severity', 'P2')} fix: {fix.get('target', '')} - {fix.get('repair', '')}")
        lines.append("")
    (run_dir / "META_CLAIM_REVIEW.md").write_text("\n".join(lines), encoding="utf-8")


def run(args: argparse.Namespace) -> None:
    load_env()
    input_path = Path(args.input).resolve()
    text = input_path.read_text(encoding="utf-8", errors="replace")
    works = split_works(text)
    if args.turn:
        works = [work for work in works if work["turn"].lower().startswith(f"## turn {args.turn}".lower())]
    if args.work:
        wanted = {item.strip().upper() for item in args.work.split(",") if item.strip()}
        works = [work for work in works if work["work_id"].upper() in wanted]
    if args.start_at:
        start = args.start_at.upper()
        works = [work for work in works if work["work_id"].upper() >= start]
    if args.limit:
        works = works[: args.limit]
    if not works:
        raise SystemExit("No works matched.")

    if args.plan:
        for work in works:
            print(f"{work['work_id']}\t{work['turn']}\t{work['title']}")
        return

    cfg = provider_config(args)
    rid = args.run_id or run_id()
    run_dir = RUNTIME / rid
    raw_dir = run_dir / "raw_responses"
    raw_dir.mkdir(parents=True, exist_ok=True)

    events: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []

    for offset, work in enumerate(works, start=1):
        event = {
            "timestamp": now(),
            "event": "work_started",
            "run_id": rid,
            "work_id": work["work_id"],
            "title": work["title"],
            "turn": work["turn"],
            "source_path": work["source_path"],
            "body_sha256": sha256_text(work["body"]),
            "provider_endpoint": cfg["endpoint"].split("/v1")[0],
            "model": cfg["model"],
        }
        events.append(event)
        print(f"[{offset}/{len(works)}] {work['work_id']} - {work['title']}")

        prompt = make_prompt(work, args.max_chars, args.max_claims)
        try:
            raw = call_api(prompt, cfg, args.timeout, args.max_tokens)
            (raw_dir / f"{work['work_id']}.raw.txt").write_text(raw, encoding="utf-8")
            parsed = normalize_result(work, extract_json(raw))
            (run_dir / f"{work['work_id']}.json").write_text(json.dumps(parsed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            results.append(parsed)
            events.append({**event, "event": "work_completed", "claim_count": len(parsed.get("claims", []))})
        except Exception as exc:
            error = {"work_id": work["work_id"], "title": work["title"], "error": str(exc)}
            (run_dir / f"{work['work_id']}.error.json").write_text(json.dumps(error, indent=2) + "\n", encoding="utf-8")
            events.append({**event, "event": "work_failed", "error": str(exc)})
            if not args.keep_going:
                write_outputs(run_dir, results, events)
                raise
        if args.sleep:
            time.sleep(args.sleep)

    write_outputs(run_dir, results, events)
    print(run_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Defense Grid claims from canon assembly.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Assembled canon markdown file.")
    parser.add_argument("--turn", type=int, help="Only process one turn number.")
    parser.add_argument("--work", help="Comma-separated work IDs, e.g. W4.1,W4.2.")
    parser.add_argument("--start-at", help="Start at work ID, e.g. W4.1.")
    parser.add_argument("--limit", type=int, help="Limit number of works.")
    parser.add_argument("--plan", action="store_true", help="List selected works without API calls.")
    parser.add_argument("--run-id", help="Optional run folder name.")
    parser.add_argument("--max-chars", type=int, default=28000)
    parser.add_argument("--max-claims", type=int, default=18)
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--keep-going", action="store_true")
    parser.add_argument("--endpoint", help="Override API endpoint.")
    parser.add_argument("--model", help="Override model.")
    parser.add_argument("--api-key", help="Override API key. Prefer environment/.env.")
    args = parser.parse_args()
    try:
        run(args)
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        raise SystemExit(130)


if __name__ == "__main__":
    main()
