#!/usr/bin/env python3
"""Private canonical action node runner.

Turns copied axiom markdown files into canonical derivation-node reviews.
Provider defaults to DeepSeek because this pass is meant to run there first.

This script writes only local runtime artifacts. It does not modify source axioms.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


SYSTEM_PROMPT = """You are auditing Theophysics axiom documents into Canonical Action Nodes.

Be strict, useful, and conservative. Do not flatter. Do not upgrade theology into physics or bridge claims into proof.

Return valid JSON only. No markdown fences.

Schema:
{
  "source_id": string,
  "title": string,
  "canonical_node": {
    "axiom": string,
    "definitions": [string],
    "derivation": [string],
    "action": string,
    "boundary": [string],
    "test": [string]
  },
  "dg_protocol": {
    "dg1_dependencies": [string],
    "dg2_new_capability": string,
    "dg3_preserved_floor": string,
    "dg4_collapse_if_removed": string,
    "dg5_translation_registers": [string],
    "dg6_state": "coherent|defective|ruptured|unknown",
    "dg7_admissible": "yes|no|partial|needs_review",
    "dg8_closure_pass": "yes|no|unclear"
  },
  "classification": {
    "claim_class": string,
    "proof_label": string,
    "grade": "A|B|C|D|E|F",
    "recommended_atom_action": string
  },
  "risk": {
    "overstatement_risks": [string],
    "kill_conditions": [string],
    "lean_target": string
  },
  "plain_summary": string
}

Allowed proof_label values:
LEAN_FORMAL_PROOF, LEAN_CONDITIONAL_PROOF, LEAN_GUARDRAIL_SUPPORTED,
PYTHON_RUNTIME_SUPPORTED, COLAB_REPRODUCIBLE, SYMBOLIC_SUPPORTED,
HISTORICALLY_SUPPORTED, ABDUCTIVELY_FAVORED, BRIDGE_DECLARED,
ISOMORPHIC_EVENT_CANDIDATE, COUNTERMODEL_FOUND, NOT_ESTABLISHED,
RERUN_OWED, QUARANTINE, NARRATIVE_ANCHOR.

Prefer NOT_ESTABLISHED unless the document itself names a stronger verified artifact.
"""


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "untitled"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def trim_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    head = text[: max_chars // 2]
    tail = text[-max_chars // 2 :]
    return head + "\n\n[...TRUNCATED FOR API REVIEW...]\n\n" + tail


def extract_json(text: str) -> dict:
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


TRANSLATE = str.maketrans(
    {
        "\u2014": " - ",
        "\u2013": " - ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00ac": "not ",
        "\u2205": "empty-set",
        "\u2208": "in",
        "\u2209": "not-in",
        "\u222a": "union",
        "\u2234": "therefore",
        "\u2192": "->",
        "\u21d2": "=>",
        "\u03c7": "chi",
        "\u03a9": "Omega",
        "\u03a6": "Phi",
        "\u03c6": "phi",
        "\u00b7": "*",
    }
)


def ascii_clean(value):
    """Keep outputs stable in Windows tools and CSV consumers."""
    if isinstance(value, str):
        cleaned = value.translate(TRANSLATE)
        return cleaned.encode("ascii", errors="replace").decode("ascii").replace("?", "")
    if isinstance(value, list):
        return [ascii_clean(v) for v in value]
    if isinstance(value, dict):
        return {ascii_clean(k): ascii_clean(v) for k, v in value.items()}
    return value


def call_deepseek(prompt: str, model: str, max_tokens: int, temperature: float) -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        raise SystemExit("DEEPSEEK_API_KEY is not set.")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as res:
            data = json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as ex:
        body = ex.read().decode("utf-8", errors="replace")
        raise SystemExit(f"DeepSeek HTTP {ex.code}: {body}") from ex
    return data["choices"][0]["message"]["content"]


def call_openai_responses(prompt: str, model: str, max_tokens: int) -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise SystemExit("OPENAI_API_KEY is not set.")
    payload = {
        "model": model,
        "input": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "max_output_tokens": max_tokens,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as res:
            data = json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as ex:
        body = ex.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenAI HTTP {ex.code}: {body}") from ex
    if "output_text" in data:
        return data["output_text"]
    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                parts.append(content.get("text", ""))
    return "\n".join(parts).strip()


def make_prompt(path: Path, text: str, max_chars: int) -> str:
    source_id = path.stem
    return f"""Convert this axiom document into a Canonical Action Node and DG protocol row.

Source file: {path.name}
Source id: {source_id}
SHA256: {digest_text(text)}

Use the node idea:
- Axiom: irreducible rule/truth/intent
- Definitions: fixed terms preventing drift
- Derivation: logical steps
- Action: what the system should do
- Boundary: what it does not do
- Test: how fidelity is checked

Then run DG1-DG8:
DG1 dependency, DG2 new capability, DG3 preservation, DG4 collapse, DG5 translation, DG6 state, DG7 admissibility, DG8 closure.

Document:
---
{trim_text(text, max_chars)}
---"""


def flatten_list(value) -> str:
    if isinstance(value, list):
        return " | ".join(str(v) for v in value)
    return "" if value is None else str(value)


def run(args: argparse.Namespace) -> None:
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_dir = output_dir / "json"
    json_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.glob("*.md"))
    if args.start:
        files = [p for p in files if p.name >= args.start]
    if args.limit:
        files = files[: args.limit]
    if not files:
        raise SystemExit(f"No markdown files found in {input_dir}")

    rows = []
    for idx, path in enumerate(files, start=1):
        out_path = json_dir / f"{path.stem}.canonical-node.json"
        if out_path.exists() and not args.force:
            obj = json.loads(out_path.read_text(encoding="utf-8"))
        else:
            text = read_text(path)
            prompt = make_prompt(path, text, args.max_chars)
            if args.dry_run:
                obj = {
                    "source_id": path.stem,
                    "title": path.stem,
                    "canonical_node": {
                        "axiom": "",
                        "definitions": [],
                        "derivation": [],
                        "action": "",
                        "boundary": ["dry run only"],
                        "test": [],
                    },
                    "dg_protocol": {
                        "dg1_dependencies": [],
                        "dg2_new_capability": "",
                        "dg3_preserved_floor": "",
                        "dg4_collapse_if_removed": "",
                        "dg5_translation_registers": [],
                        "dg6_state": "unknown",
                        "dg7_admissible": "needs_review",
                        "dg8_closure_pass": "unclear",
                    },
                    "classification": {
                        "claim_class": "dry_run",
                        "proof_label": "NOT_ESTABLISHED",
                        "grade": "E",
                        "recommended_atom_action": "keep_in_inbox",
                    },
                    "risk": {
                        "overstatement_risks": [],
                        "kill_conditions": [],
                        "lean_target": "",
                    },
                    "plain_summary": "Dry run only.",
                }
            else:
                if args.provider == "deepseek":
                    raw = call_deepseek(prompt, args.model, args.max_tokens, args.temperature)
                elif args.provider == "openai":
                    raw = call_openai_responses(prompt, args.model, args.max_tokens)
                else:
                    raise SystemExit(f"Unsupported provider: {args.provider}")
                obj = extract_json(raw)
                obj = ascii_clean(obj)
                time.sleep(args.sleep)
            obj["_runner"] = {
                "provider": args.provider,
                "model": args.model,
                "source_file": str(path),
                "output_file": str(out_path),
            }
            out_path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        dg = obj.get("dg_protocol", {})
        cls = obj.get("classification", {})
        node = obj.get("canonical_node", {})
        risk = obj.get("risk", {})
        rows.append(
            {
                "source_file": path.name,
                "source_id": obj.get("source_id", path.stem),
                "title": obj.get("title", path.stem),
                "axiom": node.get("axiom", ""),
                "definitions": flatten_list(node.get("definitions", [])),
                "action": node.get("action", ""),
                "boundary": flatten_list(node.get("boundary", [])),
                "test": flatten_list(node.get("test", [])),
                "dg1_dependencies": flatten_list(dg.get("dg1_dependencies", [])),
                "dg2_new_capability": dg.get("dg2_new_capability", ""),
                "dg3_preserved_floor": dg.get("dg3_preserved_floor", ""),
                "dg4_collapse_if_removed": dg.get("dg4_collapse_if_removed", ""),
                "dg5_translation_registers": flatten_list(dg.get("dg5_translation_registers", [])),
                "dg6_state": dg.get("dg6_state", ""),
                "dg7_admissible": dg.get("dg7_admissible", ""),
                "dg8_closure_pass": dg.get("dg8_closure_pass", ""),
                "claim_class": cls.get("claim_class", ""),
                "proof_label": cls.get("proof_label", ""),
                "grade": cls.get("grade", ""),
                "recommended_atom_action": cls.get("recommended_atom_action", ""),
                "overstatement_risks": flatten_list(risk.get("overstatement_risks", [])),
                "kill_conditions": flatten_list(risk.get("kill_conditions", [])),
                "lean_target": risk.get("lean_target", ""),
                "plain_summary": obj.get("plain_summary", ""),
            }
        )
        print(f"[{idx}/{len(files)}] {path.name} -> {out_path.name}", flush=True)

    csv_path = output_dir / "canonical_node_rows.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    report = [
        "# Canonical Node API Run",
        "",
        f"Provider: `{args.provider}`",
        f"Model: `{args.model}`",
        f"Files processed: `{len(rows)}`",
        f"CSV: `{csv_path}`",
        "",
        "Boundary: API review is classification and extraction, not proof.",
    ]
    (output_dir / "RUN_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--provider", choices=["deepseek", "openai"], default="deepseek")
    parser.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL") or "deepseek-chat")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--start", default="")
    parser.add_argument("--max-chars", type=int, default=22000)
    parser.add_argument("--max-tokens", type=int, default=3000)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted.")
