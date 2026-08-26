#!/usr/bin/env python3
"""Import the Part 1 axiom mode-classification markdown into Lane 4 atoms."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import lane4_ledger as ledger


REPO = Path(__file__).resolve().parents[1]
SOURCE_CANDIDATES = [
    REPO / "_docs" / "AXIOMS_PART1_MODE_CLASSIFICATION.md",
    Path(r"O:\_Theophysics_v5\00_AXIOMS\_LOSSLESS_SUMMARY\AXIOMS_PART1_MODE_CLASSIFICATION.md"),
]
SOURCE = next((path for path in SOURCE_CANDIDATES if path.is_file()), SOURCE_CANDIDATES[0])
REPORT = ledger.LEDGER / "LANE4_AXIOM_CLASSIFICATION_IMPORT_REPORT.md"

MODE_PROOF_LABEL = {
    "AX_CORE": "NOT_ESTABLISHED",
    "AX_DERIVED": "NOT_ESTABLISHED",
    "AX_SCAFFOLD": "NOT_ESTABLISHED",
    "FW_EXTENDED": "NOT_ESTABLISHED",
    "HY_EVIDENCE": "NOT_ESTABLISHED",
    "DROP_DUPLICATE": "QUARANTINE",
}

MODE_GLYPHS = {
    "AX_CORE": ["axiom", "truth"],
    "AX_DERIVED": ["proof", "axiom"],
    "AX_SCAFFOLD": ["definition", "axiom"],
    "FW_EXTENDED": ["mesh", "domain-tag"],
    "HY_EVIDENCE": ["evidence", "prediction"],
    "DROP_DUPLICATE": ["boundary", "kill-condition"],
}


def parse_attrs(rest: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for key, value in re.findall(r"(\w+)=`([^`]*)`", rest):
        attrs[key] = value
    why = re.search(r"\|\s*why=(.*)$", rest)
    if why:
        attrs["why"] = why.group(1).strip()
    return attrs


def parse_entries(text: str) -> list[dict[str, str]]:
    mode = None
    entries: list[dict[str, str]] = []
    for line in text.splitlines():
        heading = re.match(r"^##\s+(AX_CORE|AX_DERIVED|AX_SCAFFOLD|FW_EXTENDED|HY_EVIDENCE|DROP_DUPLICATE)\b", line)
        if heading:
            mode = heading.group(1)
            continue
        if not mode or not line.startswith("- `"):
            continue
        parts = line.split("|")
        if len(parts) < 2:
            continue
        raw_id = parts[0].strip()[3:-1]
        title = parts[1].strip()
        attrs = parse_attrs("|".join(parts[2:]))
        entries.append({
            "mode": mode,
            "raw_id": raw_id,
            "title": title,
            "decision": attrs.get("decision", ""),
            "anchor": attrs.get("anchor", ""),
            "source_class": attrs.get("class", ""),
            "source_status": attrs.get("status", ""),
            "why": attrs.get("why", ""),
            "line": line,
        })
    return entries


def claim_for(entry: dict[str, str]) -> str:
    return (
        f"{entry['title']} is classified in Part 1 as {entry['mode']} "
        f"with decision {entry['decision'] or 'unspecified'} and anchor "
        f"{entry['anchor'] or 'unspecified'}."
    )


def assumptions_for(entry: dict[str, str]) -> list[str]:
    anchor = entry["anchor"] or "anchor_unspecified"
    if anchor == "UNANCHORED_IN_CURRENT_CHAIN":
        return ["UNANCHORED_IN_CURRENT_CHAIN"]
    return [x.strip() for x in anchor.split(",") if x.strip()] or ["anchor_unspecified"]


def status_for(entry: dict[str, str]) -> str:
    if entry["mode"] == "DROP_DUPLICATE":
        return "quarantined_duplicate"
    if entry["anchor"] == "UNANCHORED_IN_CURRENT_CHAIN":
        return "active_candidate_unanchored"
    return "active_candidate"


def atom_data(entry: dict[str, str]) -> dict:
    source_claim_id = f"AX_PART1:{entry['mode']}:{entry['raw_id']}"
    negative_guards = [
        "Mode classification is not proof.",
        "Do not encode every Part 1 row as a Lean axiom.",
        "Lean status must be checked separately from registry status.",
    ]
    if entry["anchor"] == "UNANCHORED_IN_CURRENT_CHAIN":
        negative_guards.append("Unanchored entry cannot be treated as bedrock until a clean dependency path is supplied.")
    if entry["mode"] == "DROP_DUPLICATE":
        negative_guards.append("Duplicate row should not survive canonical normalization.")

    return {
        "title": entry["title"],
        "claim": claim_for(entry),
        "domain": "axioms",
        "lane": "Classification",
        "source_claim_id": source_claim_id,
        "claim_class": "classification",
        "mode_classification": entry["mode"],
        "assumptions": assumptions_for(entry),
        "definitions": [],
        "equations": [],
        "bridges": [],
        "dependencies": assumptions_for(entry),
        "negative_guards": negative_guards,
        "kill_conditions": [
            "A later canonical dashboard contradicts this mode classification.",
            "A clean dependency audit changes the anchor status.",
        ],
        "proof_label": MODE_PROOF_LABEL[entry["mode"]],
        "glyphs": MODE_GLYPHS[entry["mode"]],
        "glyph_paths": [f"theophysics_glyphs/svg/{glyph_id}.svg" for glyph_id in MODE_GLYPHS[entry["mode"]]],
        "current_status": status_for(entry),
        "rerun_status": "not_applicable",
        "source_artifacts": [str(SOURCE)],
        "source_class": entry["source_class"],
        "source_status": entry["source_status"],
        "classification_decision": entry["decision"],
        "classification_anchor": entry["anchor"],
        "classification_why": entry["why"],
    }


def main() -> int:
    if not SOURCE.is_file():
        raise SystemExit(f"source not found: {SOURCE}")
    text = SOURCE.read_text(encoding="utf-8-sig")
    entries = parse_entries(text)
    created = 0
    skipped = 0
    updated = 0
    by_mode: dict[str, int] = {}
    unanchored = 0

    for entry in entries:
        by_mode[entry["mode"]] = by_mode.get(entry["mode"], 0) + 1
        if entry["anchor"] == "UNANCHORED_IN_CURRENT_CHAIN":
            unanchored += 1
        atom = ledger.normalize_atom(atom_data(entry), SOURCE)
        path = ledger.atom_path(atom["atom_id"])
        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))
            changed = False
            for key in ("glyphs", "glyph_paths"):
                if existing.get(key) != atom.get(key):
                    existing[key] = atom.get(key, [])
                    changed = True
            artifacts = existing.setdefault("source_artifacts", [])
            if str(SOURCE) not in artifacts:
                artifacts.append(str(SOURCE))
                changed = True
            if changed:
                ledger.append_event(existing, {
                    "event_type": "classification_glyphs_attached",
                    "lane": "Classification",
                    "result": "recorded",
                    "artifact_path": str(SOURCE),
                    "meaning": f"Attached Part 1 classification glyphs for {entry['raw_id']} as {entry['mode']}.",
                    "limits": "Glyphs classify and render the atom; they do not prove it.",
                    "reviewer": "Codex",
                })
                updated += 1
            else:
                skipped += 1
            continue
        ledger.append_event(atom, {
            "event_type": "classification_imported",
            "lane": "Classification",
            "result": "recorded",
            "artifact_path": str(SOURCE),
            "meaning": f"Imported Part 1 mode classification row {entry['raw_id']} as {entry['mode']}.",
            "limits": "Classification import is not proof and does not promote the claim to canon.",
            "reviewer": "Codex",
        })
        created += 1

    ledger.rebuild()
    validation_failed = ledger.validate()

    lines = [
        "# Lane 4 Axiom Classification Import Report",
        "",
        f"Source: `{SOURCE}`",
        "",
        f"Rows parsed: **{len(entries)}**",
        f"Atoms created: **{created}**",
        f"Existing atoms enriched with glyphs: **{updated}**",
        f"Atoms skipped because already current: **{skipped}**",
        f"Unanchored entries: **{unanchored}**",
        "",
        "## Mode Counts",
        "",
    ]
    for mode in sorted(by_mode):
        lines.append(f"- `{mode}`: {by_mode[mode]}")
    lines += [
        "",
        "## Guardrail",
        "",
        "```text",
        "This import does not prove any axiom.",
        "It turns the classification rows into trackable Lane 4 atoms with source, mode, anchor, negative guards, and kill conditions.",
        "```",
        "",
        "## Validation",
        "",
        f"Lane 4 validation failed: `{validation_failed}`",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    return 1 if validation_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
