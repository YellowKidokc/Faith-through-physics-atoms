#!/usr/bin/env python3
"""Run deterministic Crown Canon Guard, then ask DeepSeek for semantic triage.

The model reviews findings only. It does not modify source files.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
ROOT = PACKAGE.parent
GUARD = HERE / "canon_guard.py"
MANIFEST = HERE / "crown-canon-manifest.toml"
CANON_REFERENCE = HERE / "canon" / "crown-knowledge-atom-no-drift.md"
KEYS = Path(r"C:\theophysics\_scripts\keys.txt")
OUT_DIR = ROOT / "_runtime" / "canon_guard"


def load_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    if KEYS.exists():
        for line in KEYS.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip().startswith("DEEPSEEK_API_KEY="):
                return line.partition("=")[2].strip()
    raise SystemExit("DEEPSEEK_API_KEY not found in environment or keys.txt")


def run_guard() -> tuple[Path, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUT_DIR / "crown-canon-report.json"
    review_packet = OUT_DIR / "crown-canon-review-packet.json"
    cmd = [
        sys.executable,
        str(GUARD),
        str(ROOT),
        "-m",
        str(MANIFEST),
        "--format",
        "json",
        "-o",
        str(report_path),
        "--review-packet",
        str(review_packet),
    ]
    result = subprocess.run(cmd)
    if result.returncode not in {0, 2}:
        raise SystemExit(f"Canon Guard failed with exit code {result.returncode}")
    return report_path, review_packet


def compact_findings(report: dict[str, Any], max_per_code: int) -> dict[str, Any]:
    findings = report.get("findings", [])
    counts = Counter(f["code"] for f in findings)
    severity_counts = Counter(f["severity"] for f in findings)
    samples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for finding in findings:
        bucket = samples[finding["code"]]
        if len(bucket) < max_per_code:
            bucket.append({
                "severity": finding.get("severity"),
                "path": finding.get("path"),
                "line": finding.get("line"),
                "message": finding.get("message"),
                "canonical_id": finding.get("canonical_id"),
            })
    return {
        "summary": report.get("summary", {}),
        "counts_by_code": dict(sorted(counts.items())),
        "counts_by_severity": dict(sorted(severity_counts.items())),
        "samples_by_code": dict(samples),
    }


def call_deepseek(model: str, temperature: float, max_tokens: int, prompt: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "openai", "--quiet"], check=False)
        from openai import OpenAI

    client = OpenAI(api_key=load_key(), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a conservative canon audit reviewer for Faith Through Physics. "
                    "You do not rewrite canon. You classify deterministic guard findings into "
                    "true drift, likely false positive, acceptable view-layer difference, or "
                    "needs David ratification. Keep equations exact and do not invent authority."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""


def build_prompt(report: dict[str, Any], max_per_code: int) -> str:
    reference = CANON_REFERENCE.read_text(encoding="utf-8", errors="replace")
    compact = compact_findings(report, max_per_code)
    return f"""# Crown Canon Semantic Review Request

Review this deterministic Canon Guard report.

The guard is intentionally conservative. Your job is to triage, not to rewrite.

## Canon Reference

```text
{reference}
```

## Deterministic Guard Summary

```json
{json.dumps(compact, indent=2, ensure_ascii=False)}
```

## Required Output

Return Markdown with these sections:

1. Executive verdict
2. Top true-drift findings, ordered by priority
3. Likely false positives or view-layer exceptions
4. Exact files/rules David should ratify before fixes
5. Safe deterministic fixes that could be added later
6. Things not to auto-fix
7. Recommended next command or next review packet

Rules:

- Do not say the old equation is fixed unless the report proves it.
- Distinguish atom-canon status from page/view status.
- Treat C-as-tenth-factor drift as high priority unless the file is clearly documenting legacy history.
- Treat legacy verification fields as migration warnings unless they create contradiction.
- Keep the current Crown rule visible: chi(W) = C_W[triple_integral(G*M*E*S*T*K*R*Q*F) dx dy dt].
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Crown Canon Guard plus DeepSeek semantic triage.")
    parser.add_argument("--model", default="deepseek-chat")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--max-tokens", type=int, default=6000)
    parser.add_argument("--max-per-code", type=int, default=8)
    parser.add_argument("--skip-guard", action="store_true")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUT_DIR / "crown-canon-report.json"
    if not args.skip_guard or not report_path.exists():
        report_path, _ = run_guard()

    report = json.loads(report_path.read_text(encoding="utf-8", errors="replace"))
    prompt = build_prompt(report, args.max_per_code)
    prompt_path = OUT_DIR / "deepseek-crown-review.prompt.md"
    review_path = OUT_DIR / "deepseek-crown-review.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    review = call_deepseek(args.model, args.temperature, args.max_tokens, prompt)
    review_path.write_text(review.strip() + "\n", encoding="utf-8")

    print(f"DeepSeek Crown review written: {review_path}")
    print(f"Prompt snapshot written: {prompt_path}")
    print(f"Guard report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

