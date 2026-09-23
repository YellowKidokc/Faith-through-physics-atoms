from __future__ import annotations

import json
import argparse
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"D:\GitHub\Faith-through-physics-atoms")
OUT = Path(r"C:\Users\David\Documents\faiththruphysics.com\60_EXCHANGE\REALITY_200")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

DOMAINS = [
    "logic and inference",
    "mathematics and formal structure",
    "metaphysics and ontology",
    "epistemology and philosophy of science",
    "fundamental physics",
    "cosmology and spacetime",
    "thermodynamics and statistical mechanics",
    "information and computation",
    "chemistry and complex systems",
    "biology and evolution",
    "ecology and Earth systems",
    "neuroscience and cognition",
    "consciousness and philosophy of mind",
    "psychology and human development",
    "language, meaning, and communication",
    "social systems, economics, and institutions",
    "ethics and moral philosophy",
    "history and human civilization",
    "theology and philosophy of religion",
    "cross-domain limits, integration, and open questions",
]

SYSTEM = """You are constructing a rigorous, plural-domain candidate map of reality as responsibly understood today. Do not produce inspirational slogans. Distinguish mathematical truth, empirical finding, philosophical inference, definition, theological doctrine, bridge hypothesis, and open conjecture. Do not award certainty merely because a proposition is culturally familiar. Do not suppress a major truth-candidate merely because it is theological, but never label theology as empirical or formally proved. Prefer high-level claims that organize many lower-level facts. Preserve serious disagreement. State the smallest assumptions you can. Return valid JSON only."""


def load_key() -> str:
    key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    candidates = [
        REPO / "keys.txt",
        REPO / ".env.local",
        REPO / ".env",
        Path(r"D:\GitHub\GOLD\Faith-through-physics-atoms\.env"),
    ]
    for path in candidates:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = re.match(r"\s*DEEPSEEK_API_KEY\s*=\s*['\"]?([^'\"\s]+)", line)
            if match:
                return match.group(1)
    raise SystemExit(
        "DEEPSEEK_API_KEY was not found. Set it in the process environment or an ignored "
        "repository-root keys.txt, .env.local, or .env file. No API call was made."
    )


def prompt(domain: str, start: int) -> str:
    return f"""Generate exactly 10 candidate high-level truths for this domain: {domain}.

These are entries {start:03d} through {start + 9:03d} of a 200-entry cross-domain map. Select claims for explanatory reach and foundational importance, not novelty or agreement with any particular worldview.

Return one JSON object with exactly:
{{
  "domain": "{domain}",
  "items": [
    {{
      "id": "R-{start:03d}",
      "statement": "one precise sentence",
      "domain": "{domain}",
      "claim_mode": "FORMAL|EMPIRICAL|PHILOSOPHICAL|THEOLOGICAL|BRIDGE|DEFINITION|OPEN_CONJECTURE",
      "epistemic_status": "ESTABLISHED|STRONG_CONSENSUS|CONTESTED|TRADITION_DEPENDENT|OPEN",
      "confidence_0_to_100": 0,
      "minimal_assumptions": ["..."],
      "scope_boundary": "what this does not establish",
      "strongest_support": "short description of the strongest support",
      "strongest_rival": "strongest serious alternative or objection",
      "defeat_or_revision_condition": "what would defeat or materially revise it",
      "why_fundamental": "why many other claims depend on it",
      "depends_on_ids": []
    }}
  ]
}}

Use sequential IDs. Exactly 10 items. No Markdown. Do not cite invented sources. Keep every field concise enough that the complete map remains usable."""


def call_api(key: str, user_prompt: str) -> dict:
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "max_tokens": 8000,
    }).encode("utf-8")
    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            envelope = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"DeepSeek HTTP {exc.code}: {detail}") from exc
    content = envelope["choices"][0]["message"]["content"]
    return {"envelope": envelope, "parsed": json.loads(content)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", type=Path, help="Resume an existing timestamped run directory")
    args = parser.parse_args()
    key = load_key()
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = args.resume if args.resume else OUT / stamp
    run_dir.mkdir(parents=True, exist_ok=True)
    all_items = []
    receipts = []
    for batch, domain in enumerate(DOMAINS):
        start = batch * 10 + 1
        raw_path = run_dir / f"batch_{batch + 1:02d}.response.json"
        if raw_path.exists():
            envelope = json.loads(raw_path.read_text(encoding="utf-8"))
            parsed = json.loads(envelope["choices"][0]["message"]["content"])
            result = {"envelope": envelope, "parsed": parsed}
            source = "checkpoint"
        else:
            result = call_api(key, prompt(domain, start))
            source = "api"
        parsed = result["parsed"]
        items = parsed.get("items", [])
        expected_ids = [f"R-{i:03d}" for i in range(start, start + 10)]
        actual_ids = [item.get("id") for item in items]
        if len(items) != 10 or actual_ids != expected_ids:
            raise RuntimeError(f"Batch {batch + 1} failed ID/count validation: {actual_ids}")
        if source == "api":
            raw_path.write_text(json.dumps(result["envelope"], ensure_ascii=False, indent=2), encoding="utf-8")
        all_items.extend(items)
        receipts.append({"batch": batch + 1, "domain": domain, "ids": expected_ids, "response": str(raw_path)})
        print(f"Completed {batch + 1:02d}/20 ({source}): {domain}", flush=True)
        if source == "api":
            time.sleep(0.5)
    if len(all_items) != 200 or len({item["id"] for item in all_items}) != 200:
        raise RuntimeError("Merged result did not contain exactly 200 unique IDs")
    packet = {
        "schema_version": "reality-candidates/1.0.0",
        "status": "CANDIDATE_DRAFT_NOT_ADMITTED",
        "created_utc": stamp,
        "provider": "DeepSeek",
        "model": MODEL,
        "question": "What are the 200 most important high-level truths or truth-candidates needed to describe reality as responsibly understood today?",
        "items": all_items,
    }
    (run_dir / "REALITY_200_CANDIDATES.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "RUN_RECEIPT.json").write_text(json.dumps(receipts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"COMPLETE: {run_dir}")


if __name__ == "__main__":
    main()
