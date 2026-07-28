from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


LEAN_CORPUS = Path(r"\\192.168.2.50\h_hp\Desktop 2\LEAN 4\LEAN4_CORPUS_CLASSIFIED.json")
REPO = Path(r"D:\GitHub\Faith-through-physics-atoms")
PACKET = REPO / "master-equation" / "11_articles" / "TOPBAR_FILL_PACKET.master-equation.generated.json"
TOPBAR_PACKET = Path(r"D:\GitHub\Python-WEB\topbar\canonical-page-shell\pages\TOPBAR_FILL_PACKET.master-equation.generated.json")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    corpus = load_json(LEAN_CORPUS)
    packet = load_json(PACKET)

    classifications = corpus.get("all_classifications", [])
    categories = Counter(item.get("category", "UNKNOWN") for item in classifications if isinstance(item, dict))
    line_total = sum(int(item.get("lines") or 0) for item in classifications if isinstance(item, dict))

    total_files = int(corpus.get("total_files") or len(classifications))
    tier_s_files = corpus.get("tier_S_files", [])
    tier_s_count = len(tier_s_files)
    master_equation_count = int(categories.get("MASTER_EQUATION", 0))
    needs_review_count = len(corpus.get("needs_review", [])) or int(categories.get("NEEDS_REVIEW", 0))
    mathlib_dependency_count = int(categories.get("MATHLIB_DEPENDENCY", 0))

    tier_s_names = [
        str(item if isinstance(item, str) else item.get("filename", "")).strip()
        for item in tier_s_files
    ]
    tier_s_names = [name for name in tier_s_names if name]

    lean_term = {
        "id": "lean-corpus",
        "label": "Lean Corpus",
        "tone": "purple",
        "front": {
            "eyebrow": f"Classified Lean 4 corpus / scan {corpus.get('scan_date', 'unknown')}",
            "subtitle": "Four-number verification pill",
            "equation": f"{total_files} files | {tier_s_count} core | {master_equation_count} ME | {needs_review_count} review",
            "summary": "A compact map of the Lean corpus behind the Master Equation: what exists, what is central, what directly touches the Master Equation, and what still needs review.",
            "rows": [
                {"label": "Files scanned", "value": str(total_files)},
                {"label": "Tier-S/core files", "value": str(tier_s_count)},
                {"label": "Master Equation files", "value": str(master_equation_count)},
                {"label": "Needs review", "value": str(needs_review_count)},
            ],
        },
        "back": {
            "eyebrow": "Corpus detail",
            "rows": [
                {"label": "Lines scanned", "value": f"{line_total:,}"},
                {"label": "Mathlib dependencies", "value": str(mathlib_dependency_count)},
                {"label": "Tier-S names", "value": ", ".join(tier_s_names)},
                {"label": "Source JSON", "value": str(LEAN_CORPUS)},
            ],
        },
        "proofUrl": "",
    }

    terms = [
        term
        for term in packet.get("terms", [])
        if term.get("id") != "lean-corpus"
    ]
    insert_at = next((idx for idx, term in enumerate(terms) if term.get("id") == "fruit-vector"), len(terms))
    terms.insert(insert_at, lean_term)
    packet["terms"] = terms

    verification = []
    for v in packet.get("verification", []):
        if v.get("title") == "Lean Corpus":
            continue
        verification.append(v)
    verification.append({
        "title": "Lean Corpus",
        "rows": [
            ["Scan date", str(corpus.get("scan_date", ""))],
            ["Files scanned", str(total_files)],
            ["Tier-S/core", str(tier_s_count)],
            ["Master Equation", str(master_equation_count)],
            ["Needs review", str(needs_review_count)],
        ],
    })
    packet["verification"] = verification

    audit = packet.setdefault("audit", {"right": [], "overstated": [], "wrong": []})
    right_line = f"Lean corpus pill added from classified scan: {total_files} files, {tier_s_count} Tier-S/core, {master_equation_count} Master Equation, {needs_review_count} needs review."
    over_line = "The Lean corpus pill is a classified coverage map, not a claim that every scanned file is theorem-complete or Master-Equation-specific."
    audit["right"] = [x for x in audit.get("right", []) if "Lean corpus pill added" not in x] + [right_line]
    audit["overstated"] = [x for x in audit.get("overstated", []) if "Lean corpus pill is a classified coverage map" not in x] + [over_line]

    for key, html in packet.get("reader_layers", {}).items():
        if "Lean Corpus Pill" not in html:
            packet["reader_layers"][key] = html + (
                "<h2>Lean Corpus Pill</h2>"
                f"<p>The classified Lean 4 corpus adds a four-number verification pill: "
                f"{total_files} files scanned, {tier_s_count} Tier-S/core files, "
                f"{master_equation_count} Master Equation files, and {needs_review_count} review-needed files. "
                "This is a coverage and classification signal, not a blanket proof label.</p>"
            )

    dump_json(PACKET, packet)
    dump_json(TOPBAR_PACKET, packet)
    print(f"Updated {PACKET}")
    print(f"Copied {TOPBAR_PACKET}")
    print(f"Four numbers: files={total_files}, tier_s={tier_s_count}, master_equation={master_equation_count}, needs_review={needs_review_count}")


if __name__ == "__main__":
    main()
