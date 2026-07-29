#!/usr/bin/env python3
"""Probe DeepSeek's Math Translation Layer output for one non-canon document."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
KEYS = Path(r"C:\theophysics\_scripts\keys.txt")
CANON_REFERENCE = HERE / "canon" / "crown-knowledge-atom-no-drift.md"
OUT_DIR = ROOT / "_runtime" / "canon_guard" / "mtl_probe"


def load_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    if KEYS.exists():
        for line in KEYS.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip().startswith("DEEPSEEK_API_KEY="):
                return line.partition("=")[2].strip()
    raise SystemExit("DEEPSEEK_API_KEY not found in environment or keys.txt")


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
                    "You are a Math Translation Layer specialist for Faith Through Physics. "
                    "Explain equations in clear layered language, preserve canonical drift warnings, "
                    "and never promote an inbox document to canon."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""


def build_prompt(source_path: Path, max_chars: int) -> str:
    source_text = source_path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    canon = CANON_REFERENCE.read_text(encoding="utf-8", errors="replace")
    rel = source_path.relative_to(ROOT).as_posix()
    return f"""# Math Translation Layer Probe

You are reviewing one non-canon inbox document.

Do not rewrite the document.
Do not promote it to canon.
Do not silently repair equations.

Use the current Crown no-drift rule when judging equations.

## Current Crown Reference

```text
{canon}
```

## Source File

```text
{rel}
```

## Source Text

```markdown
{source_text}
```

## Task

Create a Math Translation Layer output for this document.

Return Markdown with:

1. `# MTL Probe Report`
2. `## Non-Canon Status`
3. `## Equations Detected`
4. `## MTL Entries`
   - For each equation or formal structure:
     - `id`
     - exact source line or phrase
     - math layer: what the symbols are doing
     - plain-language layer
     - theological / philosophical layer, if present
     - canonical status: current, old/drift, uncertain, or historical-only
     - topbar pill candidate: yes/no and why
5. `## Canon Drift Warnings`
6. `## What To Keep`
7. `## What To Delete Or Archive`
8. `## Overall Verdict`

Important:

- If the source uses `G*M*E*S*T*K*R*Q*F*C`, flag it as old/drift unless the text clearly labels it historical.
- Current Crown form is `chi(W) = C_W[ triple_integral (G*M*E*S*T*K*R*Q*F) dx dy dt ]`.
- Explain whether the MTL is useful for topbar pills.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a DeepSeek MTL probe on one source file.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--model", default="deepseek-chat")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--max-tokens", type=int, default=7000)
    parser.add_argument("--max-input-chars", type=int, default=18000)
    args = parser.parse_args()

    source = Path(args.input).resolve()
    if not source.is_file():
        raise SystemExit(f"Input file not found: {source}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    label = source.stem.replace(" ", "_")
    prompt_path = OUT_DIR / f"{label}_{stamp}.prompt.md"
    output_path = OUT_DIR / f"{label}_{stamp}.mtl.md"

    prompt = build_prompt(source, args.max_input_chars)
    prompt_path.write_text(prompt, encoding="utf-8")
    output = call_deepseek(args.model, args.temperature, args.max_tokens, prompt)
    output_path.write_text(output.strip() + "\n", encoding="utf-8")

    print(f"MTL probe written: {output_path}")
    print(f"Prompt snapshot written: {prompt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

