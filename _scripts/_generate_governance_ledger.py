#!/usr/bin/env python3
"""No-cost governance ledger for all pre-v2.3 canonical source notes.

Reads every Markdown source note, auto-extracts source_governance using the
same logic as the claim pipeline driver, and writes a human-reviewable ledger.
No DeepSeek calls. No candidate batches. No source mutation.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Reuse the extraction logic from the demo driver so the ledger and the batch
# runner never drift.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _run_candidate_batch_demo import (
    SOURCE_DIR,
    VAULT,
    build_source_governance,
    extract_section,
)

OUTPUT_ROOT = VAULT / "__CANDIDATE_DRAFTS_NOT_ADMITTED" / f"governance_ledger_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
LEDGER_PATH = OUTPUT_ROOT / "governance_ledger.md"
JSON_PATH = OUTPUT_ROOT / "governance_ledger.json"


def governance_issues(path: Path, gov: dict) -> list[tuple[str, str]]:
    """Return (severity, message) tuples for missing or unusual metadata.

    Severities:
      - info: structural curiosity (em-dash, multiple clauses)
      - review: mapping/metadata gap that needs a human decision
      - split: likely bundled assertion; create separate capsules
      - block: broken dependency or missing required field
    """
    issues: list[tuple[str, str]] = []
    required = ["declared_mode", "declared_status", "atlas_type", "domain"]
    for field in required:
        if not gov.get(field):
            issues.append(("block", f"missing {field.replace('declared_', '')}"))

    if gov.get("declared_status") and not gov.get("allowed_claim_species"):
        issues.append(("review", f"unmapped status '{gov['declared_status']}'"))

    text = path.read_text(encoding="utf-8", errors="replace")
    statement = extract_section(text, "Statement") or ""

    # Structural flags (informational, not necessarily bundles).
    has_emdash = "\u2014" in statement or "--" in statement
    if has_emdash:
        issues.append(("info", "statement contains em-dash; review structure before single-capsule run"))

    sentences = [s.strip() for s in re.split(r"[.!?]\s+", statement) if s.strip()]
    if len(sentences) > 1:
        issues.append(("info", f"statement has {len(sentences)} clauses; review before single-capsule run"))
        # Stronger split signal: two independent sentences with different subjects.
        first_words = [s.split()[0].lower() for s in sentences if s.split()]
        if len(set(first_words)) > 1:
            issues.append(("split", "possible bundle: clauses have different leading subjects"))

    if gov.get("bridge_permitted"):
        depends = gov.get("depends_on", [])
        if len(depends) < 2:
            issues.append(("review", "bridge permitted but fewer than 2 dependencies; mapping may be incomplete"))

    return issues


def format_flags(issues: list[tuple[str, str]]) -> str:
    if not issues:
        return "ok"
    return "; ".join(f"[{sev}] {msg}" for sev, msg in issues)


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    source_files = sorted(
        [
            p for p in SOURCE_DIR.glob("*.md")
            if p.name.lower() != "index.md" and not p.name.startswith("_")
        ],
        key=lambda p: p.name,
    )

    records: list[tuple[Path, dict, list[tuple[str, str]]]] = []
    all_ids: set[str] = set()
    for path in source_files:
        gov = build_source_governance(path)
        issues = governance_issues(path, gov)
        records.append((path, gov, issues))
        if gov.get("declared_id"):
            all_ids.add(gov["declared_id"])

    # Second pass: check dependency targets exist.
    for path, gov, issues in records:
        for dep in gov.get("depends_on", []):
            if dep and dep not in all_ids:
                issues.append(("block", f"dependency '{dep}' not found in scanned sources"))

    # Summary counters.
    total = len(records)
    flagged = [(p, g, i) for p, g, i in records if i]
    info_count = sum(1 for _, _, i in records for sev, _ in i if sev == "info")
    review_count = sum(1 for _, _, i in records for sev, _ in i if sev == "review")
    split_count = sum(1 for _, _, i in records for sev, _ in i if sev == "split")
    block_count = sum(1 for _, _, i in records for sev, _ in i if sev == "block")

    lines = [
        "# Governance ledger — pre-v2.3 canonical source notes",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Source directory: `{SOURCE_DIR}`",
        f"Records scanned: {total}",
        "",
        "This ledger is read-only. It does not create candidate batches or call DeepSeek.",
        "",
        "## Summary",
        "",
        f"- Total records: {total}",
        f"- Records with any flag: {len(flagged)}",
        f"- `[info]` structural notes: {info_count}",
        f"- `[review]` mapping/metadata decisions needed: {review_count}",
        f"- `[split]` likely bundled assertions: {split_count}",
        f"- `[block]` broken or missing required metadata: {block_count}",
        "",
        "## Legend",
        "",
        "- `[info]` — curiosity; does not block a single-capsule run.",
        "- `[review]` — mapping/metadata needs a human decision before DeepSeek run.",
        "- `[split]` — source probably bundles independent assertions; create separate capsules.",
        "- `[block]` — missing required field or dangling dependency; must fix before run.",
        "",
        "| # | ID | Mode | Status | Atlas type | Domain | Depends on | Claim species | Warrant class | Bridge | Flags |",
        "|---|----|------|--------|------------|--------|------------|---------------|---------------|--------|-------|",
    ]

    json_records = []
    for i, (path, gov, issues) in enumerate(records, 1):
        depends = ", ".join(gov.get("depends_on", [])) or "none"
        species = ", ".join(gov.get("allowed_claim_species", [])) or "OPEN"
        warrant = ", ".join(gov.get("allowed_warrant_classes", [])) or "OPEN"
        bridge = "yes" if gov.get("bridge_permitted") else "no"
        flags = format_flags(issues)
        lines.append(
            f"| {i} | `{gov.get('declared_id') or 'N/A'}` | `{gov.get('declared_mode') or 'N/A'}` | "
            f"`{gov.get('declared_status') or 'N/A'}` | {gov.get('atlas_type') or 'N/A'} | "
            f"{gov.get('domain') or 'N/A'} | {depends} | {species} | {warrant} | {bridge} | {flags} |"
        )
        json_records.append({
            "index": i,
            "source": str(path),
            "declared_id": gov.get("declared_id"),
            "declared_mode": gov.get("declared_mode"),
            "declared_status": gov.get("declared_status"),
            "atlas_type": gov.get("atlas_type"),
            "domain": gov.get("domain"),
            "depends_on": gov.get("depends_on", []),
            "allowed_claim_species": gov.get("allowed_claim_species", []),
            "allowed_warrant_classes": gov.get("allowed_warrant_classes", []),
            "bridge_permitted": gov.get("bridge_permitted", False),
            "bridge_limits": gov.get("bridge_limits", {}),
            "defeat_conditions": gov.get("defeat_conditions", []),
            "limitations": gov.get("limitations", []),
            "issues": [{"severity": sev, "message": msg} for sev, msg in issues],
        })

    lines.extend([
        "",
        "## Flagged records requiring review",
        "",
        f"Count: {len(flagged)}",
        "",
    ])

    if not flagged:
        lines.append("No flags raised.")
    else:
        for path, gov, issues in flagged:
            rel = path.relative_to(VAULT)
            lines.extend([
                f"### `{gov.get('declared_id') or path.name}`",
                "",
                f"- **Source:** `{rel}`",
                f"- **Mode:** `{gov.get('declared_mode') or 'N/A'}`",
                f"- **Status:** `{gov.get('declared_status') or 'N/A'}`",
                f"- **Atlas type:** {gov.get('atlas_type') or 'N/A'}",
                f"- **Domain:** {gov.get('domain') or 'N/A'}",
                f"- **Depends on:** {', '.join(gov.get('depends_on', [])) or 'none'}",
                f"- **Derived species:** {', '.join(gov.get('allowed_claim_species', [])) or 'OPEN'}",
                f"- **Derived warrant:** {', '.join(gov.get('allowed_warrant_classes', [])) or 'OPEN'}",
                f"- **Bridge permitted:** {gov.get('bridge_permitted', False)}",
                "",
                "**Flags:**",
            ])
            for sev, msg in issues:
                lines.append(f"- **[{sev}]** {msg}")
            lines.append("")

    lines.extend([
        "",
        "## Next steps",
        "",
        "1. Review `[block]` and `[split]` records first.",
        "2. Resolve `[review]` mapping decisions (e.g., corollary treatment, bridge mappings).",
        "3. Use `[info]` flags to spot-check statement structure; most can be ignored.",
        "4. Compare ledger-derived species/warrant with Kimi's entries.",
        "5. Run DeepSeek only on records whose governance is confirmed.",
    ])

    LEDGER_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    JSON_PATH.write_text(json.dumps(json_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Ledger written: {LEDGER_PATH}")
    print(f"JSON written: {JSON_PATH}")
    print(f"Records scanned: {total}")
    print(f"Flagged records: {len(flagged)}")
    print(f"  info: {info_count}, review: {review_count}, split: {split_count}, block: {block_count}")


if __name__ == "__main__":
    main()
