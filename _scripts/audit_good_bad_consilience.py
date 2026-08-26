#!/usr/bin/env python3
"""Audit good/bad coherence consilience across Lane 4 atoms."""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATOMS = ROOT / "_ledger" / "atoms"
OUT_MD = ROOT / "_ledger" / "LANE4_GOOD_BAD_CONSILIENCE_AUDIT.md"
OUT_CSV = ROOT / "_ledger" / "LANE4_GOOD_BAD_CONSILIENCE_AUDIT.csv"

TERMS = {
    "good": ["good", "goodness", "virtue", "fruit", "love", "righteous", "alignment", "coherence", "truth", "restoration", "grace"],
    "bad": ["bad", "vice", "sin", "corruption", "decoherence", "collapse", "misalignment", "judgment", "bondage", "propagation"],
}

MOTIFS = {
    "standard_exposure": ["standard", "comparison", "expos", "judgment", "light", "ledger", "measurement"],
    "coherence_alignment": ["coherence", "alignment", "truth", "good", "virtue", "righteous"],
    "decoherence_corruption": ["decoherence", "misalignment", "corruption", "sin", "vice", "collapse"],
    "restoration": ["restoration", "grace", "atonement", "reset", "fruit", "repair"],
    "propagation": ["propagation", "epidemiology", "addiction", "bondage", "spread"],
}


def load_atoms():
    for path in sorted(ATOMS.glob("*.json")):
        yield json.loads(path.read_text(encoding="utf-8"))


def text_of(atom):
    def flatten(value):
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            return " ".join(flatten(v) for v in value)
        if isinstance(value, dict):
            return " ".join(flatten(v) for v in value.values())
        return "" if value is None else str(value)

    fields = [
        atom.get("atom_id", ""),
        atom.get("title", ""),
        atom.get("claim", ""),
        flatten(atom.get("definitions", [])),
        flatten(atom.get("bridges", [])),
        flatten(atom.get("negative_guards", [])),
        flatten(atom.get("kill_conditions", [])),
    ]
    return " ".join(fields).lower()


def hits(text, words):
    return sorted({w for w in words if w in text})


def row_for(atom):
    text = text_of(atom)
    good_hits = hits(text, TERMS["good"])
    bad_hits = hits(text, TERMS["bad"])
    if not good_hits and not bad_hits:
        return None
    motif_hits = [name for name, words in MOTIFS.items() if hits(text, words)]
    polarity = "mixed_good_bad" if good_hits and bad_hits else ("good_alignment" if good_hits else "bad_degradation")
    return {
        "atom_id": atom["atom_id"],
        "title": atom["title"],
        "domain": atom.get("domain", ""),
        "lane": atom.get("lane", ""),
        "claim_class": atom.get("claim_class", ""),
        "mode_classification": atom.get("mode_classification", ""),
        "proof_label": atom.get("proof_label", ""),
        "status": atom.get("current_status", ""),
        "polarity": polarity,
        "motifs": "; ".join(motif_hits),
        "good_terms": "; ".join(good_hits),
        "bad_terms": "; ".join(bad_hits),
    }


def consilience_grade(rows):
    motif_domains = defaultdict(set)
    for row in rows:
        for motif in filter(None, row["motifs"].split("; ")):
            motif_domains[motif].add(row["domain"])
    strongest = max((len(v) for v in motif_domains.values()), default=0)
    if strongest >= 4:
        return "CONSILIENCE_CANDIDATE_STRONG"
    if strongest >= 2:
        return "CONSILIENCE_CANDIDATE"
    return "PATTERN_CANDIDATE"


def main():
    rows = [r for atom in load_atoms() if (r := row_for(atom))]
    rows.sort(key=lambda r: (r["domain"], r["atom_id"]))

    fieldnames = [
        "atom_id", "title", "domain", "lane", "claim_class", "mode_classification",
        "proof_label", "status", "polarity", "motifs", "good_terms", "bad_terms",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    by_domain = Counter(r["domain"] for r in rows)
    by_label = Counter(r["proof_label"] for r in rows)
    by_mode = Counter(r["mode_classification"] for r in rows)
    by_polarity = Counter(r["polarity"] for r in rows)
    motif_domains = defaultdict(set)
    motif_rows = defaultdict(list)
    for r in rows:
        for motif in filter(None, r["motifs"].split("; ")):
            motif_domains[motif].add(r["domain"])
            motif_rows[motif].append(r["atom_id"])

    lines = [
        "# Lane 4 Good/Bad Consilience Audit",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Verdict",
        "",
        f"Audit classification: `{consilience_grade(rows)}`",
        "",
        "This is not a formal proof that goodness, righteousness, coherence, and God are identical.",
        "It is a ledger-backed finding that the good/bad grammar appears across multiple independently named lanes and should be treated as consilience candidate material, not dismissed as a mere science hedge.",
        "",
        "## Counts",
        "",
        f"- Matching atoms: **{len(rows)}**",
        f"- Domains touched: **{len(by_domain)}**",
        "",
        "Polarity:",
        *[f"- `{k}`: {v}" for k, v in sorted(by_polarity.items())],
        "",
        "Proof labels:",
        *[f"- `{k}`: {v}" for k, v in sorted(by_label.items())],
        "",
        "Mode classifications:",
        *[f"- `{k}`: {v}" for k, v in sorted(by_mode.items())],
        "",
        "## Motif Coverage",
        "",
        "| Motif | Domains | Atom count |",
        "|---|---:|---:|",
    ]
    for motif in sorted(motif_domains):
        lines.append(f"| `{motif}` | {len(motif_domains[motif])} | {len(motif_rows[motif])} |")

    lines += [
        "",
        "## Structural Thesis Under Test",
        "",
        "```text",
        "good / righteousness / truth / coherence / fruit",
        "  -> alignment with a truth-bearing standard",
        "",
        "bad / sin / corruption / decoherence / vice",
        "  -> misalignment, degradation, collapse, or parasitic propagation",
        "",
        "judgment / measurement / light / ledger",
        "  -> exposure of alignment or misalignment",
        "",
        "grace / restoration / atonement / fruit",
        "  -> repair, reset, reintegration, or restored coherence",
        "```",
        "",
        "## Negative Guard",
        "",
        "```text",
        "Do not call this Lean-proved theology.",
        "Do not call every row formal isomorphism.",
        "Do not treat science-language resemblance as automatic canon.",
        "Do not hide the theological implication either: repeated independent convergence is consilience candidate evidence.",
        "```",
        "",
        "## Rows",
        "",
        "| Atom | Title | Polarity | Motifs | Label |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| `{r['atom_id']}` | {r['title']} | `{r['polarity']}` | {r['motifs']} | `{r['proof_label']}` |")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT_MD)
    print(OUT_CSV)
    print(f"matching_atoms={len(rows)}")
    print(f"classification={consilience_grade(rows)}")


if __name__ == "__main__":
    main()
