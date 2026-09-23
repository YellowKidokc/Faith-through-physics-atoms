from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

RUN = Path(r"C:\Users\David\Documents\faiththruphysics.com\60_EXCHANGE\REALITY_200\20260903T202716Z")
SOURCE = RUN / "REALITY_200_CANDIDATES.json"
TARGET = RUN / "SORTED_REALITY_BUCKETS"

BUCKETS = {
    "01_LOGIC_MATHEMATICS_AND_FORMAL_STRUCTURE": {
        "logic and inference", "mathematics and formal structure"
    },
    "02_METAPHYSICS_EPISTEMOLOGY_AND_SCIENTIFIC_METHOD": {
        "metaphysics and ontology", "epistemology and philosophy of science"
    },
    "03_PHYSICS_COSMOLOGY_THERMODYNAMICS_AND_INFORMATION": {
        "fundamental physics", "cosmology and spacetime",
        "thermodynamics and statistical mechanics", "information and computation"
    },
    "04_CHEMISTRY_LIFE_EVOLUTION_AND_EARTH_SYSTEMS": {
        "chemistry and complex systems", "biology and evolution", "ecology and Earth systems"
    },
    "05_MIND_CONSCIOUSNESS_PSYCHOLOGY_LANGUAGE_AND_MEANING": {
        "neuroscience and cognition", "consciousness and philosophy of mind",
        "psychology and human development", "language, meaning, and communication"
    },
    "06_SOCIAL_SYSTEMS_HISTORY_AND_CIVILIZATION": {
        "social systems, economics, and institutions", "history and human civilization"
    },
    "07_ETHICS_MORALITY_AND_VALUE": {"ethics and moral philosophy"},
    "08_THEOLOGY_AND_PHILOSOPHY_OF_RELIGION": {"theology and philosophy of religion"},
    "09_CROSS_DOMAIN_LIMITS_INTEGRATION_AND_OPEN_QUESTIONS": {
        "cross-domain limits, integration, and open questions"
    },
}


def slug(text: str, limit: int = 72) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")
    return value[:limit].rstrip("-") or "untitled"


def bucket_for(domain: str) -> str:
    matches = [bucket for bucket, domains in BUCKETS.items() if domain in domains]
    if len(matches) != 1:
        raise ValueError(f"Domain has {len(matches)} buckets: {domain}")
    return matches[0]


def architecture_card(item: dict) -> str:
    assumptions = "; ".join(item["minimal_assumptions"]) or "None stated"
    dependencies = ", ".join(item["depends_on_ids"]) or "None stated in this independent batch"
    return f"""---
reality_id: "{item['id']}"
status: "CANDIDATE_DRAFT_NOT_ADMITTED"
domain: "{item['domain']}"
claim_mode: "{item['claim_mode']}"
epistemic_status: "{item['epistemic_status']}"
confidence_0_to_100: {item['confidence_0_to_100']}
source: "DeepSeek Reality 200 independent discovery run"
---

# {item['id']} — {item['statement']}

## Sixty-second architecture card

| Field | Answer |
|---|---|
| What system is being described? | {item['domain']} |
| What must this system keep true? | {item['statement']} |
| What is inside scope? | The proposition as bounded below |
| What is outside scope? | {item['scope_boundary']} |
| Main building blocks | {assumptions} |
| Governing invariants | Claim mode: {item['claim_mode']}; status: {item['epistemic_status']} |
| Strongest rival architecture | {item['strongest_rival']} |
| Highest architecture test passed | API-generated candidate only; no independent test attached |
| Largest open seam | {item['defeat_or_revision_condition']} |

## Candidate statement

{item['statement']}

## Epistemic classification

- **Mode:** {item['claim_mode']}
- **Status:** {item['epistemic_status']}
- **API confidence:** {item['confidence_0_to_100']}/100
- **Dependencies named by API:** {dependencies}

## Minimal assumptions

""" + "\n".join(f"- {a}" for a in item["minimal_assumptions"]) + f"""

## Strongest support

{item['strongest_support']}

## Strongest rival

{item['strongest_rival']}

## Defeat or revision condition

{item['defeat_or_revision_condition']}

## Why fundamental

{item['why_fundamental']}

## Integration boundary

This record preserves an independently generated API candidate. It has not been compared with the Faith Through Physics axiom corpus, admitted into canon, or independently verified merely because it appears in this folder.
"""


def main() -> None:
    packet = json.loads(SOURCE.read_text(encoding="utf-8"))
    items = packet["items"]
    if len(items) != 200 or len({item["id"] for item in items}) != 200:
        raise RuntimeError("Expected exactly 200 unique Reality records")
    TARGET.mkdir(parents=True, exist_ok=True)
    for bucket in BUCKETS:
        folder = TARGET / bucket
        folder.mkdir(exist_ok=True)
        for old in folder.glob("*.md"):
            old.unlink()

    rows = []
    by_bucket = defaultdict(list)
    for item in items:
        bucket = bucket_for(item["domain"])
        filename = f"{item['id']}_{slug(item['statement'])}.md"
        path = TARGET / bucket / filename
        text = architecture_card(item)
        path.write_text(text, encoding="utf-8")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        row = {
            "id": item["id"], "statement": item["statement"], "bucket": bucket,
            "domain": item["domain"], "claim_mode": item["claim_mode"],
            "epistemic_status": item["epistemic_status"],
            "confidence_0_to_100": item["confidence_0_to_100"],
            "file": filename, "path": str(path), "sha256": digest,
        }
        rows.append(row)
        by_bucket[bucket].append(row)

    with (TARGET / "REALITY_200_SORTED_MANIFEST.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

    lines = [
        "# Reality 200 — Independent Candidate Index", "",
        "These 200 records were generated without supplying the Faith Through Physics axiom corpus. They remain API candidates, not admitted truths. Each linked note includes the automatic sixty-second architecture card.", ""
    ]
    for bucket in BUCKETS:
        lines += [f"## {bucket}", "", f"**Count:** {len(by_bucket[bucket])}", "",
                  "| ID | Candidate | Mode | Status | Confidence |", "|---|---|---|---|---:|"]
        for row in by_bucket[bucket]:
            link = f"[[{bucket}/{row['file']}|{row['id']}]]"
            statement = str(row["statement"]).replace("|", "/")
            lines.append(f"| {link} | {statement} | {row['claim_mode']} | {row['epistemic_status']} | {row['confidence_0_to_100']} |")
        lines.append("")
    (TARGET / "00_REALITY_200_MASTER_INDEX.md").write_text("\n".join(lines), encoding="utf-8")

    counts = Counter(row["bucket"] for row in rows)
    (TARGET / "SORTING_RECEIPT.md").write_text(
        "# Reality 200 Sorting Receipt\n\n"
        f"- Source: `{SOURCE}`\n"
        f"- Independent candidates read: **{len(items)}**\n"
        f"- Individual architecture-card notes written: **{len(rows)}**\n"
        f"- Missing or duplicate IDs: **{200 - len(set(row['id'] for row in rows))}**\n"
        "- Comparison against Theophysics axioms performed: **No**\n\n"
        + "\n".join(f"- **{bucket}:** {counts[bucket]}" for bucket in BUCKETS) + "\n",
        encoding="utf-8",
    )
    print(f"SORTED={len(rows)} BUCKETS={len(counts)} TARGET={TARGET}")


if __name__ == "__main__":
    main()
