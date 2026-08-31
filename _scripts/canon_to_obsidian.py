#!/usr/bin/env python3
"""Project staged canon candidates into Obsidian notes.

Canon is authoritative; these notes are a derived, rebuildable view — the same
relationship SQLite has to the JSON-LD. Delete the output folder, re-run, and
you get it back.

Why notes rather than an embedded workbench: Obsidian's value is backlinks,
graph, and full-text search. A GUI in an iframe is still a GUI. Atoms as notes
become part of the vault's fabric.

**This does not invent a schema.** It writes the same frontmatter and section
layout already used by `_CANONICAL/01_TERMS/*`, so the Canonization Workbench
plugin, Dataview queries, and human readers all see one format.

Staged candidates land in their own folder, never in `01_TERMS`. A candidate is
not a term. Every generated note carries `admission: not_performed`, because
nothing in this pipeline promotes anything.

Safety rules:

- Writes only inside the output folder.
- Every generated file carries `canon_generated: true`. Any file lacking that
  key is never overwritten, so hand-written notes are safe.
- Never writes into the canon store. One-way projection.

Usage:
    python canon_to_obsidian.py --dry-run
    python canon_to_obsidian.py --apply
    python canon_to_obsidian.py --apply --vault "Z:/__New/Theophysics.new"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

MARKER_KEY = "canon_generated"
MARKER = f"{MARKER_KEY}: true"

DEFAULT_CANON_ROOT = Path(__file__).resolve().parents[1] / "_canon"

# The live vault, per Obsidian's own registry (%APPDATA%/obsidian/obsidian.json).
# Not O:\_Theophysics_v4 — that path is stale in INFRASTRUCTURE.md.
DEFAULT_VAULT = Path("Z:/__New/Theophysics.new")

# Matches the plugin's `canonRoot` setting and the existing folder numbering.
# 01_TERMS holds admitted terms; staged candidates get their own drawer.
DEFAULT_OUT = "_CANONICAL/20_CANDIDATES"

GLYPHS = {
    "claim": "◆", "mathematics": "∫", "definition": "≝", "story": "✍",
    "evidence": "E", "bridge": "≅", "kill": "⛔", "proof": "⊢",
    "paper": "▤", "translation": "☖", "application": "↦",
    "objection": "⚔", "prediction": "⧖", "result": "⟡", "source": "⊡",
}


def load_candidates(canon_root: Path) -> list[dict]:
    folder = canon_root / "candidates"
    if not folder.is_dir():
        return []
    out = []
    for path in sorted(folder.glob("*.json")):
        try:
            out.append(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError) as e:
            print(f"  ! skipping {path.name}: {e}", file=sys.stderr)
    return out


def load_receipts(canon_root: Path) -> dict[str, dict]:
    """Latest receipt per subject. Later lines win — the file is append-only."""
    path = canon_root / "receipts.jsonl"
    receipts: dict[str, dict] = {}
    if not path.is_file():
        return receipts
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("subject_id"):
            receipts[r["subject_id"]] = r
    return receipts


def canon_id(candidate: dict) -> str:
    raw = candidate.get("atom_id") or candidate.get("candidate_id") or "unknown"
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "-", str(raw)).strip("-")
    return cleaned or "unknown"


def yaml_str(value) -> str:
    if value is None:
        return '""'
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def extract(candidate: dict) -> dict:
    """Pull note fields from an opaque payload.

    The engine treats `payload` as opaque. Nerve captures nest detail inside
    it; older records are flat `{"text": ...}`. Both shapes must work.
    """
    payload = candidate.get("payload") or {}
    capsule = payload.get("capsule") or {}
    capture = payload.get("capture") or {}
    statement = (capsule.get("exact_statement") or payload.get("text") or "").strip()
    return {
        "object_type": payload.get("node_type") or "claim",
        "statement": statement,
        "plain": (capsule.get("plain_statement") or "").strip(),
        "capsule": capsule,
        "capture": capture,
    }


def render(candidate: dict, receipt: dict | None) -> str:
    info = extract(candidate)
    capsule = info["capsule"]
    capture = info["capture"]
    cid = canon_id(candidate)
    object_type = info["object_type"]
    glyph = GLYPHS.get(object_type, "◆")

    sha = (candidate.get("content_hash") or "").replace("sha256:", "").upper()
    verdict = (receipt or {}).get("verdict", "")

    out: list[str] = []
    out.append("---")
    out.append(f"canon_id: {cid}")
    out.append(f"term: {yaml_str(info['statement'][:80] or cid)}")
    out.append("aliases: []")
    out.append('version: "0.1.0"')
    # Their vocabulary: a staged item is a candidate, whatever the engine's
    # internal status says. The engine's own value is kept alongside.
    out.append("status: candidate")
    out.append(f"object_type: {object_type}")
    out.append(f"admission: not_performed")
    out.append(f"source_ref: {yaml_str(capture.get('source_window') or '')}")
    out.append(f"source_sha256: {sha}")
    out.append("canon_refs: []")
    out.append("")
    out.append("# --- derived, do not hand-edit ---")
    out.append(f"{MARKER}")
    out.append(f"candidate_id: {yaml_str(candidate.get('candidate_id'))}")
    out.append(f"engine_status: {yaml_str(candidate.get('status'))}")
    if verdict:
        out.append(f"engine_verdict: {yaml_str(verdict)}")
        out.append(f"receipt_id: {yaml_str(receipt.get('receipt_id'))}")
    out.append(f"author: {yaml_str(candidate.get('author'))}")
    out.append(f"created_at: {yaml_str(candidate.get('created_at'))}")
    if capsule.get("species"):
        out.append(f"species: {yaml_str(capsule['species'])}")
    if capsule.get("logical_type"):
        out.append(f"logical_type: {yaml_str(capsule['logical_type'])}")
    out.append(f"tags: [canon, candidate, {object_type}]")
    out.append("---")
    out.append("")

    out.append(f"# {glyph} {cid}")
    out.append("")
    out.append("> [!warning] Staged candidate — not canon")
    out.append("> `admission: not_performed`. Promotion is a separate human act")
    out.append("> performed by the canon engine with its own credential.")
    out.append("")

    heading = "Canonical Definition" if object_type == "definition" else "Statement"
    if info["statement"]:
        out.append(f"## {heading}")
        out.append("")
        out.append(info["statement"])
        out.append("")

    if info["plain"]:
        out.append("## Plain statement")
        out.append("")
        out.append(info["plain"])
        out.append("")

    if object_type == "mathematics":
        out.append("## Formal Mathematics")
        out.append("")
        out.append("_Not yet extracted from the captured text._")
        out.append("")

    defeater = (capsule.get("strongest_defeater") or "").strip()
    gap = (capsule.get("open_gap") or "").strip()
    burden = (capsule.get("evidence_burden") or "").strip()
    disconf = (capsule.get("disconfirmation") or "").strip()

    if defeater or gap:
        out.append("## Adversarial position")
        out.append("")
        if defeater:
            out.append(f"**Strongest defeater** — {defeater}")
            out.append("")
        if gap:
            out.append(f"**Largest open gap** — {gap}")
            out.append("")

    if burden or disconf:
        out.append("## Evidence contract")
        out.append("")
        if burden:
            out.append(f"**Burden** — {burden}")
            out.append("")
        if disconf:
            out.append(f"**Disconfirmation** — {disconf}")
            out.append("")

    depends = candidate.get("depends_on") or []
    if depends:
        out.append("## Depends on")
        out.append("")
        for dep in depends:
            out.append(f"- [[{dep}]]")
        out.append("")

    # Every note in 01_TERMS carries a Boundary section. Keep the habit: say
    # what this record does *not* establish.
    out.append("## Boundary")
    out.append("")
    out.append("This is captured input that passed intake, not established truth.")
    if verdict:
        out.append(f"The deterministic verdict was **{verdict}**, authoritative only")
        out.append("for the checks actually performed — listed below. It is not")
        out.append("review, replication, formal proof, or human acceptance.")
    else:
        out.append("No deterministic receipt is recorded for it yet.")
    out.append("")

    out.append("## Provenance")
    out.append("")
    out.append(f"- Candidate `{candidate.get('candidate_id')}`")
    out.append(f"- Hash `{candidate.get('content_hash')}`")
    if candidate.get("note"):
        out.append(f"- {candidate['note']}")
    if capture.get("client"):
        out.append(f"- Client `{capture['client']}`")
    kinds = [k for k in (capture.get("kinds") or []) if k != "any"]
    if kinds:
        out.append(f"- Recognized as {', '.join(kinds)}")
    if receipt:
        checks = receipt.get("checks_attempted") or []
        out.append(f"- Receipt `{receipt.get('receipt_id')}` "
                   f"by `{receipt.get('tool')}` v{receipt.get('tool_version')}")
        if checks:
            out.append(f"- Checks performed: {', '.join(checks)}")
    out.append("")

    return "\n".join(out)


def render_index(rows: list[tuple[str, dict, dict | None]], out_rel: str) -> str:
    """Index note. Uses Dataview when available, with a static fallback table."""
    lines = ["---", MARKER, "tags: [canon, index]", "---", "",
             "# Staged canon candidates", "",
             "Derived from the canon store. Nothing here is admitted.", "",
             "```dataview",
             "TABLE object_type AS Type, engine_status AS Engine, "
             "engine_verdict AS Verdict, admission AS Admission",
             f'FROM "{out_rel}"',
             "WHERE canon_generated",
             "SORT created_at DESC",
             "```", "",
             "## Static listing", ""]

    if not rows:
        lines.append("_No candidates in the store._")
        return "\n".join(lines) + "\n"

    lines.append("| Candidate | Type | Engine | Verdict | Statement |")
    lines.append("|---|---|---|---|---|")
    for cid, cand, receipt in rows:
        info = extract(cand)
        statement = info["statement"].replace("|", "\\|").replace("\n", " ")
        if len(statement) > 60:
            statement = statement[:60] + "…"
        lines.append(
            f"| [[{cid}]] | {info['object_type']} | {cand.get('status','')} "
            f"| {(receipt or {}).get('verdict','—')} | {statement} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def is_generated(path: Path) -> bool:
    try:
        return MARKER_KEY in path.read_text(encoding="utf-8")[:800]
    except OSError:
        return False


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--canon-root", type=Path,
                    default=Path(os.environ.get("CANON_ROOT", DEFAULT_CANON_ROOT)))
    ap.add_argument("--vault", type=Path, default=DEFAULT_VAULT)
    ap.add_argument("--out", default=DEFAULT_OUT)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--apply", action="store_true", help="actually write files")
    g.add_argument("--dry-run", action="store_true", default=True)
    args = ap.parse_args()

    if not args.canon_root.is_dir():
        print(f"canon root not found: {args.canon_root}", file=sys.stderr)
        return 2
    if not args.vault.is_dir():
        print(f"vault not found: {args.vault}", file=sys.stderr)
        return 2

    vault = args.vault.resolve()
    out_dir = (vault / args.out).resolve()
    if not str(out_dir).startswith(str(vault)):
        print("refusing to write outside the vault", file=sys.stderr)
        return 2

    candidates = load_candidates(args.canon_root)
    receipts = load_receipts(args.canon_root)

    print(f"[{'APPLY' if args.apply else 'DRY RUN'}] "
          f"{len(candidates)} candidate(s) from {args.canon_root}")
    print(f"         -> {out_dir}")
    print()

    rows = [(canon_id(c), c, receipts.get(c.get("candidate_id"))) for c in candidates]
    written = skipped = 0

    if args.apply:
        out_dir.mkdir(parents=True, exist_ok=True)

    for cid, cand, receipt in rows:
        target = out_dir / f"{cid}.md"
        if target.exists() and not is_generated(target):
            print(f"  SKIP  {target.name} — exists and was not generated here")
            skipped += 1
            continue
        body = render(cand, receipt)
        if args.apply:
            target.write_text(body, encoding="utf-8")
        print(f"  write {target.name}  ({len(body)} bytes)")
        written += 1

    index = out_dir / "_CANDIDATES INDEX.md"
    if index.exists() and not is_generated(index):
        print(f"  SKIP  {index.name} — exists and was not generated here")
        skipped += 1
    else:
        body = render_index(rows, args.out)
        if args.apply:
            index.write_text(body, encoding="utf-8")
        print(f"  write {index.name}  ({len(body)} bytes)")
        written += 1

    print()
    print(f"{written} file(s) {'written' if args.apply else 'would be written'}"
          f"{f', {skipped} skipped' if skipped else ''}")
    if not args.apply:
        print("Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
