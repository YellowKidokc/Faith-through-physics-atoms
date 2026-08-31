#!/usr/bin/env python3
"""Claim-capsule conversion engine: JSON <-> Markdown, both directions.

JSON is authority. Markdown is the human surface and the AI authoring surface.

Why both directions:
  export  (json -> md)  humans read and edit capsules as prose
  import  (md -> json)  an AI (or a human) authors markdown; this validates it
                        against claim_capsule_v1 and writes the staged JSON

Nothing here promotes anything. Import hard-forces:
    lifecycle = "staged"
    canonical_promotion_requested = false
and refuses to set decision.confirmed_by_human unless a human passes --confirm
at the terminal. Machine-authored capsules therefore always land unconfirmed.

Safety rules (same shape as canon_to_obsidian.py):
  - --dry-run is the default; nothing is written without --apply
  - generated markdown carries `capsule_generated: true`. Any markdown lacking
    that key is never overwritten by export.
  - export never writes into the JSON store; import never writes markdown.
  - import refuses to overwrite an existing .capsule.json unless --overwrite.

Usage:
    python capsule_convert.py export --root D:/_AXIOM_WORK --apply
    python capsule_convert.py import --root D:/_AXIOM_WORK --apply
    python capsule_convert.py validate --root D:/_AXIOM_WORK
    python capsule_convert.py template --out NEW_PAPER.capsule.md

File pairing convention:
    <paper>.md               the paper
    <paper>.capsule.json     the machine capsule (authority)
    <paper>.capsule.md       the human/AI surface (derived, rebuildable)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "claim-capsule/1.0.0"
MARKER_KEY = "capsule_generated"

OPERATIONS = ["new_claim", "amend", "new_version", "supersede", "add_evidence"]
CLAIM_TYPES = [
    "mathematical", "empirical", "historical", "theological",
    "bridge", "universal", "normative", "everyday_translation", "other",
]
VERSION_INTENTS = [
    "patch_nonsemantic", "minor_scope_or_support",
    "major_proposition_change", "not_applicable",
]
SELECTED_BY = ["human", "system_suggestion"]

# operation -> requires target_id
NEEDS_TARGET = {"amend", "new_version", "supersede", "add_evidence"}

# claim_type -> required keys inside type_extension
TYPE_EXTENSION_REQUIRED: dict[str, list[str]] = {
    "mathematical": ["definitions", "premises", "derivation", "countermodels", "receipt"],
    "empirical": ["dataset", "method", "denominator", "uncertainty", "replication"],
    "historical": ["primary_sources", "dates", "corroboration"],
    "theological": ["scripture", "doctrine", "interpretive_premises"],
    "bridge": ["source_definition", "target_definition", "mapping", "preserved", "lost", "negative_controls"],
    "universal": ["search_domain", "counterexample_test"],
    "normative": ["moral_standard", "normative_premises"],
    "everyday_translation": ["source_claim", "descent_preservation_check"],
    "other": [],
}

SCALAR_KEYS = [
    "schema_version", "capsule_id", "canonical_uuid", "operation", "target_id",
    "claim_type", "version_intent", "lifecycle", "canonical_promotion_requested",
]
PROSE_SECTIONS = {
    "Claim": "claim",
    "Plain language": "plain_language",
    "Defeat condition": "defeat_condition",
}
LIST_SECTIONS = {
    "Present evidence": "present_evidence",
    "Open items": "open_items",
}


# --------------------------------------------------------------------------
# tiny frontmatter reader/writer
#
# Deliberately NOT YAML. The subset is: `key: value`, one per line, where value
# is a JSON scalar or a single-line JSON array. That keeps the parser exact and
# removes the PyYAML dependency, at the cost of forbidding block lists. Every
# value this project needs round-trips through json.loads/json.dumps.
# --------------------------------------------------------------------------

def _fm_encode(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _fm_decode(raw: str) -> Any:
    raw = raw.strip()
    if raw == "":
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw  # bare unquoted string, tolerated on input


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    fm: dict[str, Any] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = _fm_decode(val)
    return fm, "\n".join(lines[end + 1:])


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def bullets(block: str) -> list[str]:
    out = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("- "):
            out.append(s[2:].strip())
        elif s.startswith("-") and len(s) > 1:
            out.append(s[1:].strip())
    return [b for b in out if b]


def kv_bullets(block: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in bullets(block):
        if ":" in item:
            k, _, v = item.partition(":")
            out[k.strip().strip("*`")] = v.strip()
    return out


# --------------------------------------------------------------------------
# validation (claim_capsule_v1, implemented directly — no jsonschema dep)
# --------------------------------------------------------------------------

def validate_capsule(cap: dict[str, Any]) -> list[str]:
    errs: list[str] = []

    def need(key: str) -> Any:
        if key not in cap or cap[key] in (None, "", [], {}):
            errs.append(f"missing required field: {key}")
            return None
        return cap[key]

    if cap.get("schema_version") != SCHEMA_VERSION:
        errs.append(f"schema_version must be {SCHEMA_VERSION!r}, got {cap.get('schema_version')!r}")

    op = need("operation")
    if op is not None and op not in OPERATIONS:
        errs.append(f"operation {op!r} not in {OPERATIONS}")
    if op in NEEDS_TARGET and not cap.get("target_id"):
        errs.append(f"operation {op!r} requires target_id")

    for key in ("claim", "plain_language", "defeat_condition"):
        v = need(key)
        if v is not None and not isinstance(v, str):
            errs.append(f"{key} must be a string")

    ct = need("claim_type")
    if ct is not None and ct not in CLAIM_TYPES:
        errs.append(f"claim_type {ct!r} not in {CLAIM_TYPES}")

    for key in ("present_evidence", "open_items"):
        if key not in cap:
            errs.append(f"missing required field: {key}")
        elif not isinstance(cap[key], list):
            errs.append(f"{key} must be a list")

    dec = cap.get("decision")
    if not isinstance(dec, dict):
        errs.append("missing required field: decision")
    else:
        if dec.get("selected_by") not in SELECTED_BY:
            errs.append(f"decision.selected_by must be one of {SELECTED_BY}")
        if not isinstance(dec.get("confirmed_by_human"), bool):
            errs.append("decision.confirmed_by_human must be true or false")

    vi = cap.get("version_intent")
    if vi is not None and vi not in VERSION_INTENTS:
        errs.append(f"version_intent {vi!r} not in {VERSION_INTENTS}")

    if cap.get("lifecycle") != "staged":
        errs.append('lifecycle must be "staged"')
    if cap.get("canonical_promotion_requested") is not False:
        errs.append("canonical_promotion_requested must be false")

    if ct in TYPE_EXTENSION_REQUIRED:
        ext = cap.get("type_extension") or {}
        if not isinstance(ext, dict):
            errs.append("type_extension must be an object")
        else:
            for key in TYPE_EXTENSION_REQUIRED[ct]:
                if key not in ext or not str(ext[key]).strip():
                    errs.append(f"claim_type {ct!r} requires type_extension.{key}")

    src = cap.get("source")
    if src is not None:
        if not isinstance(src, dict):
            errs.append("source must be an object")
        else:
            h = src.get("source_hash")
            if h is not None:
                bare = h[7:] if h.startswith("sha256:") else h
                if len(bare) != 64 or any(c not in "0123456789abcdefABCDEF" for c in bare):
                    errs.append("source.source_hash must be 64 hex chars, optionally 'sha256:' prefixed")
    return errs


# --------------------------------------------------------------------------
# export: json -> markdown
# --------------------------------------------------------------------------

def capsule_to_markdown(cap: dict[str, Any], json_name: str) -> str:
    dec = cap.get("decision") or {}
    src = cap.get("source") or {}
    ext = cap.get("type_extension") or {}

    fm: list[str] = ["---", f"{MARKER_KEY}: true", f"capsule_source: {_fm_encode(json_name)}"]
    for key in SCALAR_KEYS:
        fm.append(f"{key}: {_fm_encode(cap.get(key))}")
    fm.append(f"aliases: {_fm_encode(cap.get('aliases', []))}")
    fm.append(f"decision.selected_by: {_fm_encode(dec.get('selected_by'))}")
    fm.append(f"decision.confirmed_by_human: {_fm_encode(dec.get('confirmed_by_human'))}")
    fm.append(f"decision.selection_reason: {_fm_encode(dec.get('selection_reason'))}")
    fm.append(f"source.path_or_uri: {_fm_encode(src.get('path_or_uri'))}")
    fm.append(f"source.source_hash: {_fm_encode(src.get('source_hash'))}")
    fm.append(f"source.source_span: {_fm_encode(src.get('source_span'))}")
    fm.append(f"generated_utc: {_fm_encode(datetime.now(timezone.utc).isoformat())}")
    fm.append("---")

    parts = ["\n".join(fm), ""]
    parts.append(f"# {cap.get('capsule_id') or 'Claim capsule'}")
    parts.append("")
    parts.append("> Derived view. The JSON is authority. Edit here, then run "
                 "`capsule_convert.py import --apply` to write it back.")
    parts.append("")
    for heading, key in PROSE_SECTIONS.items():
        parts.append(f"## {heading}")
        parts.append("")
        parts.append(str(cap.get(key, "")).strip())
        parts.append("")
    for heading, key in LIST_SECTIONS.items():
        parts.append(f"## {heading}")
        parts.append("")
        items = cap.get(key) or []
        parts.extend(f"- {item}" for item in items) if items else parts.append("- (none)")
        parts.append("")
    parts.append("## Type extension")
    parts.append("")
    if ext:
        parts.extend(f"- {k}: {v}" for k, v in ext.items())
    else:
        parts.append("- (none)")
    parts.append("")
    return "\n".join(parts)


# --------------------------------------------------------------------------
# import: markdown -> json
# --------------------------------------------------------------------------

def markdown_to_capsule(text: str) -> dict[str, Any]:
    fm, body = split_frontmatter(text)
    sec = split_sections(body)

    cap: dict[str, Any] = {"schema_version": SCHEMA_VERSION}
    for key in SCALAR_KEYS:
        if key == "schema_version":
            continue
        cap[key] = fm.get(key)
    cap["aliases"] = fm.get("aliases") or []

    for heading, key in PROSE_SECTIONS.items():
        cap[key] = (sec.get(heading) or "").strip()
    for heading, key in LIST_SECTIONS.items():
        items = bullets(sec.get(heading, ""))
        cap[key] = [i for i in items if i.lower() != "(none)"]

    ext = kv_bullets(sec.get("Type extension", ""))
    cap["type_extension"] = {k: v for k, v in ext.items() if v.lower() != "(none)"}

    cap["decision"] = {
        "selected_by": fm.get("decision.selected_by") or "system_suggestion",
        "confirmed_by_human": bool(fm.get("decision.confirmed_by_human")),
        "selection_reason": fm.get("decision.selection_reason"),
    }
    cap["source"] = {
        "path_or_uri": fm.get("source.path_or_uri"),
        "source_hash": fm.get("source.source_hash"),
        "source_span": fm.get("source.source_span"),
    }

    # hard-forced. Nothing authored downstream can promote itself.
    cap["lifecycle"] = "staged"
    cap["canonical_promotion_requested"] = False
    if not cap.get("version_intent"):
        cap["version_intent"] = "not_applicable"
    return cap


TEMPLATE = """---
capsule_generated: false
capsule_id: "PAPER-ID-PRIMARY"
canonical_uuid: null
operation: "new_claim"
target_id: null
claim_type: "universal"
version_intent: "not_applicable"
lifecycle: "staged"
canonical_promotion_requested: false
aliases: []
decision.selected_by: "system_suggestion"
decision.confirmed_by_human: false
decision.selection_reason: "Primary-atom extraction, first pass."
source.path_or_uri: "Z:/__New/Theophysics.new/___AXIOM/.../PAPER.md"
source.source_hash: null
source.source_span: null
---

# PAPER-ID-PRIMARY

## Claim

One sentence. The paper's single overall claim, not its sub-claims.

## Plain language

The same claim with no jargon.

## Defeat condition

What observation or argument would kill this. Must be checkable.

## Present evidence

- What the paper actually offers in support.

## Open items

- What is asserted but not established.

## Type extension

- search_domain: (required for claim_type universal)
- counterexample_test: (required for claim_type universal)
"""


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def find_capsules(root: Path, suffix: str) -> list[Path]:
    return sorted(p for p in root.rglob(f"*{suffix}") if "99_ARCHIVE" not in p.parts)


def cmd_export(args) -> int:
    root = Path(args.root)
    files = find_capsules(root, ".capsule.json")
    if not files:
        print(f"no .capsule.json files under {root}")
        return 0
    written = skipped = failed = 0
    for jf in files:
        mf = jf.with_suffix("")           # strip .json  -> *.capsule
        mf = mf.with_suffix(".capsule.md") if not str(mf).endswith(".capsule") else Path(str(mf) + ".md")
        try:
            cap = json.loads(jf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"FAIL  {jf.name}: bad JSON: {e}")
            failed += 1
            continue
        if mf.exists():
            fm, _ = split_frontmatter(mf.read_text(encoding="utf-8"))
            if fm.get(MARKER_KEY) is not True:
                print(f"SKIP  {mf.name}: hand-written (no {MARKER_KEY}: true)")
                skipped += 1
                continue
        md = capsule_to_markdown(cap, jf.name)
        if args.apply:
            mf.write_text(md, encoding="utf-8")
            print(f"WROTE {mf}")
        else:
            print(f"WOULD WRITE {mf}  ({len(md)} bytes)")
        written += 1
    print(f"\nexport: {written} written, {skipped} skipped, {failed} failed"
          f"{'' if args.apply else '  [dry run — pass --apply to write]'}")
    return 1 if failed else 0


def cmd_import(args) -> int:
    root = Path(args.root)
    files = find_capsules(root, ".capsule.md")
    if not files:
        print(f"no .capsule.md files under {root}")
        return 0
    written = rejected = skipped = 0
    for mf in files:
        cap = markdown_to_capsule(mf.read_text(encoding="utf-8"))
        if args.confirm:
            cap["decision"]["confirmed_by_human"] = True
            cap["decision"]["selected_by"] = "human"
        else:
            cap["decision"]["confirmed_by_human"] = False
        errs = validate_capsule(cap)
        if errs:
            rejected += 1
            print(f"REJECT {mf.name}")
            for e in errs:
                print(f"       - {e}")
            continue
        jf = Path(str(mf)[: -len(".md")] + ".json")
        if jf.exists() and not args.overwrite:
            print(f"SKIP   {jf.name}: exists (pass --overwrite to replace)")
            skipped += 1
            continue
        if args.apply:
            jf.write_text(json.dumps(cap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"STAGED {jf}")
        else:
            print(f"WOULD STAGE {jf}")
        written += 1
    print(f"\nimport: {written} staged, {skipped} skipped, {rejected} rejected"
          f"{'' if args.apply else '  [dry run — pass --apply to write]'}")
    return 1 if rejected else 0


def cmd_validate(args) -> int:
    root = Path(args.root)
    files = find_capsules(root, ".capsule.json")
    bad = 0
    for jf in files:
        try:
            cap = json.loads(jf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"FAIL {jf.name}: bad JSON: {e}")
            bad += 1
            continue
        errs = validate_capsule(cap)
        if errs:
            bad += 1
            print(f"FAIL {jf.name}")
            for e in errs:
                print(f"     - {e}")
        else:
            print(f"OK   {jf.name}")
    print(f"\nvalidate: {len(files) - bad}/{len(files)} pass")
    return 1 if bad else 0


def cmd_template(args) -> int:
    out = Path(args.out)
    if out.exists():
        print(f"refusing to overwrite {out}")
        return 1
    out.write_text(TEMPLATE, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Claim-capsule JSON <-> Markdown conversion engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("export", help="json -> markdown")
    p.add_argument("--root", required=True)
    p.add_argument("--apply", action="store_true")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("import", help="markdown -> staged json")
    p.add_argument("--root", required=True)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--confirm", action="store_true",
                   help="human ratification: sets decision.confirmed_by_human true")
    p.set_defaults(func=cmd_import)

    p = sub.add_parser("validate", help="check every capsule against claim_capsule_v1")
    p.add_argument("--root", required=True)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("template", help="emit a blank authoring template")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_template)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
