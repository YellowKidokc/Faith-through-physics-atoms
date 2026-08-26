#!/usr/bin/env python3
"""Convert BLUE static HTML pages into canonical topbar fill packets."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

import claim_runtime


REPO = Path(__file__).resolve().parents[1]
DEFAULT_BLUE = Path(r"C:\theophysics\_BLUE_PAGES_INTAKE_2026-07-28\BLUE")

TONES = ["gold", "teal", "blue", "purple", "orange", "red"]


def fix_mojibake(text: str) -> str:
    try:
        fixed = text.encode("cp1252").decode("utf-8")
    except UnicodeError:
        return text
    return fixed if fixed.count("�") <= text.count("�") else text


def strip_tags(text: str) -> str:
    return claim_runtime.normalize_space(claim_runtime.strip_html(text))


def first_match(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    return strip_tags(match.group(1)) if match else default


def slug_to_page_id(slug: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", slug.upper()).strip("-")


def table_terms(raw: str) -> list[dict[str, str]]:
    table = re.search(r"<table\b.*?</table>", raw, flags=re.I | re.S)
    if not table:
        return []
    rows = re.findall(r"<tr\b.*?</tr>", table.group(0), flags=re.I | re.S)
    terms = []
    for row in rows[1:]:
        cells = re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", row, flags=re.I | re.S)
        if len(cells) < 3:
            continue
        terms.append(
            {
                "factor": strip_tags(cells[0]),
                "physics": strip_tags(cells[1]),
                "spiritual": strip_tags(cells[2]),
                "eponym": strip_tags(cells[3]) if len(cells) > 3 else "",
            }
        )
    return terms


def build_terms(raw: str) -> list[dict[str, Any]]:
    terms = []
    seen = set()
    for idx, item in enumerate(table_terms(raw)):
        label = item["spiritual"] or item["factor"]
        term_id = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
        if not term_id or term_id in seen:
            continue
        seen.add(term_id)
        terms.append(
            {
                "id": term_id,
                "label": label,
                "tone": TONES[idx % len(TONES)],
                "front": {
                    "eyebrow": "Blue page term",
                    "subtitle": item["physics"],
                    "equation": item["factor"],
                    "summary": f"{label} is the spiritual reading attached to {item['physics']} in this blue-page draft.",
                    "rows": [
                        {"label": "Factor", "value": item["factor"]},
                        {"label": "Eponym", "value": item["eponym"]},
                    ],
                },
                "back": {
                    "eyebrow": "Review",
                    "rows": [
                        {"label": "Source", "value": "BLUE page static HTML intake."},
                        {"label": "Risk", "value": "Generated from existing page structure; canonical atom alignment still needs review."},
                    ],
                },
                "proofUrl": "",
            }
        )

    if not terms:
        for idx, label in enumerate(["Coherence", "Grace", "Master Equation"]):
            term_id = label.lower().replace(" ", "-")
            terms.append(
                {
                    "id": term_id,
                    "label": label,
                    "tone": TONES[idx],
                    "front": {
                        "eyebrow": "Blue page term",
                        "subtitle": "",
                        "equation": "",
                        "summary": f"{label} appears as a load-bearing term in this page.",
                        "rows": [{"label": "Source", "value": "Extracted from page text."}],
                    },
                    "back": {"eyebrow": "Review", "rows": [{"label": "Status", "value": "Needs atom alignment."}]},
                    "proofUrl": "",
                }
            )
    return terms


def equation_blocks(raw: str) -> list[dict[str, str]]:
    blocks = []
    for block in re.findall(r'<div class="eq"\b.*?</div>\s*</div>|<div class="eq"\b.*?</div>', raw, flags=re.I | re.S):
        formula = first_match(r'<div class="formula"\b[^>]*>(.*?)</div>', block)
        reading = first_match(r'<div class="reading"\b[^>]*>(.*?)</div>', block)
        if formula:
            blocks.append({"formula": formula, "reading": reading})
    return blocks


def build_mtl(raw: str, page_id: str) -> list[dict[str, Any]]:
    items = []
    for idx, eq in enumerate(equation_blocks(raw), start=1):
        items.append(
            {
                "id": f"{page_id}-MTL-{idx:03d}",
                "format": "box",
                "title": "Equation" if idx == 1 else f"Equation {idx}",
                "equation": eq["formula"],
                "wordEquation": eq["reading"],
                "structuralInsight": "Imported from the blue-page equation block so the canonical MTL drawer can render it.",
                "plain": eq["reading"] or "This equation needs a plain-language translation.",
                "influence": "Needs canonical review against atom dependencies and current Master Equation notation.",
            }
        )
    return items or [
        {
            "id": f"{page_id}-MTL-001",
            "format": "box",
            "title": "Math Translation",
            "equation": "",
            "wordEquation": "",
            "structuralInsight": "No explicit equation block found.",
            "plain": "No explicit equation block found.",
            "influence": "Add MTL entries during review.",
        }
    ]


def build_claims(text: str, page_id: str, limit: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    indexed = claim_runtime.atom_index(claim_runtime.load_atoms())
    sentences = claim_runtime.extract_claim_sentences(text, limit=limit)
    claims = []
    proofs = []
    for idx, sentence in enumerate(sentences, start=1):
        claim_id = f"{page_id}-C{idx:03d}"
        proof_id = f"{page_id}-P{idx:03d}"
        classification = claim_runtime.classify(sentence, indexed)
        best = classification["matches"][0] if classification["matches"] else {}
        status = "partial" if classification["verdict"] == "likely-existing-atom" else "draft"
        claims.append(
            {
                "id": claim_id,
                "sentence": sentence,
                "formal": str(best.get("name") or sentence),
                "status": status,
                "derivation": [
                    f"Runtime classification: {classification['verdict']}.",
                    f"Best atom match: {best.get('nodeID', 'none')}.",
                ],
                "killCondition": "Show the sentence is not supported by the matched atom, or that it overstates the blue-page source.",
                "proofIds": [proof_id],
            }
        )
        proofs.append(
            {
                "id": proof_id,
                "title": str(best.get("name") or "Blue page source evidence"),
                "status": status,
                "summary": f"Source sentence imported from BLUE page. Best match: {best.get('nodeID', 'none')}.",
                "claimIds": [claim_id],
                "url": "",
            }
        )
    return claims, proofs


def claim_html(claims: list[dict[str, Any]]) -> str:
    lis = []
    for claim in claims:
        lis.append(
            f'<li><span class="ftp-claim-sentence" data-claim-id="{html.escape(claim["id"])}">'
            f'{html.escape(claim["sentence"])}</span></li>'
        )
    return "<ul>" + "".join(lis) + "</ul>" if lis else ""


def build_packet(source: Path, out: Path, limit: int) -> dict[str, Any]:
    raw = fix_mojibake(source.read_text(encoding="utf-8", errors="replace"))
    text = strip_tags(raw)
    slug = source.stem
    page_id = slug_to_page_id(f"BLUE-{slug}")
    title = first_match(r"<h1\b[^>]*>(.*?)</h1>", raw, source.stem.replace("-", " ").title())
    subtitle = first_match(r'<div class="sub"\b[^>]*>(.*?)</div>', raw)
    kicker = first_match(r'<div class="kicker"\b[^>]*>(.*?)</div>', raw, "BLUE intake")
    claims, proofs = build_claims(text, page_id, limit)
    mtl = build_mtl(raw, page_id)
    terms = build_terms(raw)
    status_counts = Counter(claim["status"] for claim in claims)

    packet = {
        "page": {
            "id": page_id,
            "title": title,
            "series": "BLUE Intake",
            "subtitle": subtitle,
            "kicker": kicker,
            "byline": "David Lowe · Faith Through Physics · July 2026",
            "prev": {"label": "", "url": ""},
            "next": {"label": "", "url": ""},
        },
        "terms": terms,
        "claims": claims,
        "proofs": proofs,
        "mtl": mtl,
        "verification": [
            {"title": "Page Contract", "rows": [["Source", str(source)], ["Terms", str(len(terms))], ["Claims", str(len(claims))], ["MTL", str(len(mtl))]]},
            {"title": "Claims", "rows": [["Partial", str(status_counts["partial"])], ["Draft", str(status_counts["draft"])], ["Runtime", "local classification"], ["Review", "required"]]},
            {"title": "Pills", "rows": [["Terms", "enabled"], ["Proof drawer", "enabled"], ["MTL drawer", "enabled"], ["Audio", "empty"]]},
        ],
        "audio": [
            {"id": "read", "label": "Read Aloud", "url": ""},
            {"id": "debate", "label": "Debate", "url": ""},
            {"id": "deep", "label": "Deep Dive", "url": ""},
            {"id": "critique", "label": "Critique", "url": ""},
        ],
        "audit": {
            "right": ["The static blue page can be represented in the canonical topbar shell with active terms, claims, proofs, and MTL data."],
            "overstated": ["Runtime classification is lexical/local and still needs canonical review."],
            "wrong": ["No external API review has been applied to this converted packet yet."],
        },
        "reader_layers": {
            "highschool": f"<h2>The Idea, Simply</h2><p>{html.escape(subtitle or title)}</p>{claim_html(claims[:5])}",
            "college": f"<h2>The BLUE Page, Wired</h2><p>This version keeps the page readable, but moves its terms, claims, proofs, and equations into the canonical topbar data layer.</p>{claim_html(claims)}",
            "phd": f"<h2>Runtime Structure</h2><p>Converted from static BLUE HTML into a topbar fill packet. Claims are runtime-classified against the atom graph and should be reviewed before promotion.</p>{claim_html(claims)}",
        },
    }
    claim_runtime.write_text(out, json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a BLUE static HTML page to a canonical topbar packet.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--limit", type=int, default=24)
    args = parser.parse_args()

    out = args.out or (REPO / "blue-pages" / "11_articles" / f"TOPBAR_FILL_PACKET.blue.{args.source.stem}.json")
    packet = build_packet(args.source, out, args.limit)
    print(f"[ok] wrote {out}")
    print(f"[ok] terms={len(packet['terms'])} claims={len(packet['claims'])} proofs={len(packet['proofs'])} mtl={len(packet['mtl'])}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
