#!/usr/bin/env python3
"""Build a canonical topbar fill packet from the atom registries.

This is the local adapter between the atoms repo and the canonical page shell:
atoms/registries in, TOPBAR_FILL_PACKET JSON out.
"""

from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "master-equation" / "11_articles" / "TOPBAR_FILL_PACKET.master-equation.generated.json"

FACTOR_TERMS = [
    ("G", "Grace", "External coherence injection; the gift that prevents closed-system collapse."),
    ("M", "Meaning", "The semantic load and purpose structure carried by a system."),
    ("E", "Entropy", "The disorder pressure that must be repaired, resisted, or transformed."),
    ("S_eff", "Effective Self", "The ordered agency of the person after entropy and fragmentation are accounted for."),
    ("T", "Time", "The duration and history through which coherence must remain stable."),
    ("K", "Knowledge", "Truth contact, intelligibility, and tested understanding."),
    ("R", "Relation", "Covenantal connection, reciprocity, and non-isolated coherence."),
    ("Q", "Quantum", "The physical substrate where measurement, possibility, and state transition enter."),
    ("F", "Faith", "Trust enacted under incomplete visibility, tested by its fruit."),
    ("C", "Christ", "The Logos-centered integration term that anchors the framework's theological claim."),
]

TONE_CYCLE = ["gold", "teal", "blue", "purple", "orange"]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return text or "item"


def topbar_status(atom_status: str) -> str:
    if atom_status == "verified":
        return "verified"
    if atom_status in {"tested", "partial"}:
        return "partial"
    return "draft"


def load_atom(node_id: str) -> dict[str, Any] | None:
    if not node_id.startswith("tp:master-equation/01/"):
        return None
    atom_id = node_id.rsplit("/", 1)[-1]
    matches = sorted((ROOT / "master-equation" / "01_canonical").glob(f"{atom_id}-*.jsonld"))
    if not matches:
        return None
    return read_json(matches[0])


def sentence_for(atom: dict[str, Any]) -> str:
    plain = str(atom.get("statementPlain", "")).strip()
    if plain:
        return plain if plain.endswith((".", "!", "?")) else plain + "."
    name = str(atom.get("name", "This atom")).strip()
    return f"{name} is captured as a canonical master-equation atom."


def formal_for(atom: dict[str, Any]) -> str:
    return str(atom.get("statementTechnical") or atom.get("mathematicalForm") or sentence_for(atom)).strip()


def build_terms(fruit_registry: dict[str, Any]) -> list[dict[str, Any]]:
    terms: list[dict[str, Any]] = []
    for idx, (symbol, label, summary) in enumerate(FACTOR_TERMS):
        terms.append(
            {
                "id": slugify(label),
                "label": label,
                "tone": TONE_CYCLE[idx % len(TONE_CYCLE)],
                "front": {
                    "eyebrow": "Master Equation factor",
                    "subtitle": f"{symbol} factor",
                    "equation": symbol,
                    "summary": summary,
                    "rows": [
                        {"label": "Role", "value": "Required product factor in the coherence equation."},
                        {"label": "Failure mode", "value": "If the factor collapses to zero, the product model collapses with it."},
                    ],
                },
                "back": {
                    "eyebrow": "Atom linkage",
                    "rows": [
                        {"label": "Source", "value": "master_equation_registry.json and equation atoms."},
                        {"label": "Risk", "value": "Needs domain-specific measurement before being treated as empirical."},
                    ],
                },
                "proofUrl": "",
            }
        )

    fruits = fruit_registry.get("fruits", [])
    canonical = [item for item in fruits if item.get("fruitClass") == "canonical-fruit"]
    companions = [item for item in fruits if item.get("fruitClass") == "companion-fruit"]
    fruit_names = ", ".join(str(item.get("name", "")) for item in fruits)
    fruit_summary = (
        f"The fruit vector audits {len(canonical)} canonical Fruits of the Spirit"
        f" plus {len(companions)} companion Theophysics virtues."
    )
    terms.append(
        {
            "id": "fruit-vector",
            "label": "Fruit Vector",
            "tone": "teal",
            "front": {
                "eyebrow": "Audit term",
                "subtitle": f"{len(fruits)} visible outputs",
                "equation": "Phi_vector",
                "summary": fruit_summary,
                "rows": [
                    {"label": "Fruits", "value": fruit_names},
                    {"label": "Use", "value": "A first-pass triage signal for whether a paper exports coherent fruit."},
                ],
            },
            "back": {
                "eyebrow": "API contract",
                "rows": [
                    {"label": "Callable", "value": str(fruit_registry.get("callable", "_scripts/fruit_audit.py"))},
                    {"label": "Boundary", "value": "This is not final moral judgment; it flags where a human should review."},
                ],
            },
            "proofUrl": "",
        }
    )
    return terms


def build_claims(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claims = []
    for idx, atom in enumerate(atoms, start=1):
        claim_id = f"MEQ-C{idx:03d}"
        proof_id = f"MEQ-P{idx:03d}"
        edges = atom.get("edges", [])
        deps = [str(edge.get("target", "")) for edge in edges if isinstance(edge, dict) and edge.get("target")]
        derivation = [
            f"Imported from atom {atom.get('nodeID', atom.get('claimID', 'unknown'))}.",
            "Dependencies: " + (", ".join(deps[:4]) if deps else "none declared"),
        ]
        claims.append(
            {
                "id": claim_id,
                "sentence": sentence_for(atom),
                "formal": formal_for(atom),
                "status": topbar_status(str(atom.get("status", ""))),
                "derivation": derivation,
                "killCondition": str(atom.get("falsificationCondition", "Show the dependency atoms fail or the claim is over-scoped.")),
                "proofIds": [proof_id],
            }
        )
    return claims


def build_proofs(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    proofs = []
    for idx, atom in enumerate(atoms, start=1):
        proofs.append(
            {
                "id": f"MEQ-P{idx:03d}",
                "title": str(atom.get("name", f"Master Equation Atom {idx}")),
                "status": topbar_status(str(atom.get("status", ""))),
                "summary": str(atom.get("sourceReference") or "Generated from the canonical master-equation atom registry."),
                "claimIds": [f"MEQ-C{idx:03d}"],
                "url": "",
            }
        )
    return proofs


def build_mtl(equation_registry: dict[str, Any]) -> list[dict[str, Any]]:
    mtl = []
    for item in equation_registry.get("items", []):
        eq_id = str(item.get("equationID", "ME-EQ"))
        name = str(item.get("name", eq_id))
        symbolic = str(item.get("symbolic", ""))
        normal = str(item.get("normal", ""))
        variables = [str(v) for v in item.get("variables", [])]
        mtl.append(
            {
                "id": eq_id.replace("ME-EQ-", "MEQ-MTL-"),
                "format": "box",
                "title": name,
                "equation": symbolic,
                "wordEquation": normal,
                "structuralInsight": "This equation is stored as a first-class atom so the topbar can display, query, and audit it rather than burying it in prose.",
                "plain": f"{name} tracks {', '.join(variables[:8]) if variables else 'its declared variables'} inside the Master Equation framework.",
                "influence": "It strengthens when its dependency atoms hold and weakens when a dependency, variable definition, or boundary condition fails.",
            }
        )
    return mtl


def claim_span(claim: dict[str, Any]) -> str:
    return (
        f'<span class="ftp-claim-sentence" data-claim-id="{escape(str(claim["id"]))}">'
        f'{escape(str(claim["sentence"]))}</span>'
    )


def build_reader_layers(claims: list[dict[str, Any]], mtl: list[dict[str, Any]]) -> dict[str, str]:
    first = claims[0] if claims else {"id": "MEQ-C001", "sentence": "The Master Equation is captured as a canonical atom graph."}
    second = claims[1] if len(claims) > 1 else first
    remaining_claims = "".join(f"<li>{claim_span(claim)}</li>" for claim in claims[2:])
    claim_index = f"<ul>{remaining_claims}</ul>" if remaining_claims else ""
    hs = (
        "<h2>The Idea, Simply</h2>"
        "<p>The Master Equation page is now fed by atoms instead of loose notes. The symbols, claims, equations, and fruit audit all come from the same canonical registry.</p>"
        f"<p>{claim_span(first)}</p>"
        "<p>That means the topbar can show definitions, claims, proof links, math translations, and review warnings from one source of truth.</p>"
    )
    college = (
        "<h2>The Argument</h2>"
        "<p>The Master Equation is represented as a computable packet: factor terms become topbar glossary cards, equation atoms become math translation units, and source atoms become claim/proof pairs.</p>"
        f"<p>{claim_span(first)}</p>"
        f"<p>{claim_span(second)}</p>"
        "<p>The fruit audit is also exposed as a callable review layer, so a paper can be judged for visible outputs without confusing first-pass triage with final authority.</p>"
        f"{claim_index}"
    )
    phd = (
        "<h2>The Formal Statement</h2>"
        "<p>This generated topbar packet treats the atom registry as the data layer and the canonical page shell as the rendering layer. Claims preserve dependency edges, kill conditions, and verification status in reduced topbar form.</p>"
        f"<p>{claim_span(first)}</p>"
        f"<p>{claim_span(second)}</p>"
        f"<p>The MTL layer currently exposes {len(mtl)} equation atoms, including product-collapse and fruit-vector equations.</p>"
    )
    return {"highschool": hs, "college": college, "phd": phd}


def build_verification(source_atoms: list[str], claims: list[dict[str, Any]], mtl: list[dict[str, Any]], terms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = {status: sum(1 for claim in claims if claim.get("status") == status) for status in ("verified", "partial", "draft")}
    return [
        {
            "title": "Page Contract",
            "rows": [
                ["Shell", "canonical"],
                ["Packet source", "atom registry adapter"],
                ["Source atoms", str(len(source_atoms))],
                ["Terms", str(len(terms))],
            ],
        },
        {
            "title": "Claims",
            "rows": [
                ["Total", str(len(claims))],
                ["Verified", str(counts["verified"])],
                ["Partial", str(counts["partial"])],
                ["Draft", str(counts["draft"])],
            ],
        },
        {
            "title": "Math Translation",
            "rows": [
                ["Equations", str(len(mtl))],
                ["Plain translations", str(len(mtl))],
                ["Format", "box"],
                ["Source", "_vocab/equation_registry.json"],
            ],
        },
        {
            "title": "API Calls",
            "rows": [
                ["Call 1", "topbar, terms, verification"],
                ["Call 2", "claims, proofs, MTL"],
                ["Call 3", "adversarial audit"],
                ["Fruit audit", "_scripts/fruit_audit.py"],
            ],
        },
    ]


def build_packet(out_path: Path) -> dict[str, Any]:
    equation_registry = read_json(ROOT / "_vocab" / "equation_registry.json")
    fruit_registry = read_json(ROOT / "_vocab" / "fruit_audit_registry.json")

    selected_node_ids = [
        "tp:master-equation/01/ME-01-010",
        "tp:master-equation/01/ME-01-060",
        "tp:master-equation/01/ME-01-061",
        "tp:master-equation/01/ME-EQ-001",
        "tp:master-equation/01/ME-EQ-006",
        "tp:master-equation/01/ME-EQ-009",
        "tp:master-equation/01/ME-EQ-010",
    ]
    atoms = [atom for node_id in selected_node_ids if (atom := load_atom(node_id))]

    terms = build_terms(fruit_registry)
    claims = build_claims(atoms)
    proofs = build_proofs(atoms)
    mtl = build_mtl(equation_registry)
    source_atoms = [str(atom.get("nodeID", "")) for atom in atoms if atom.get("nodeID")]

    packet = {
        "page": {
            "id": "MEQ-GENERATED-001",
            "title": "Master Equation",
            "series": "Canonical Foundations",
            "subtitle": "A generated topbar packet sourced from the axiom, equation, and fruit-audit atoms.",
            "kicker": "Master Equation / Atom Graph",
            "byline": "David Lowe · Faith Through Physics · July 2026",
            "sourceAtoms": source_atoms,
            "prev": {"label": "", "url": ""},
            "next": {"label": "", "url": ""},
        },
        "terms": terms,
        "claims": claims,
        "proofs": proofs,
        "mtl": mtl,
        "verification": build_verification(source_atoms, claims, mtl, terms),
        "audio": [
            {"id": "read", "label": "Read Aloud", "url": ""},
            {"id": "debate", "label": "Debate", "url": ""},
            {"id": "deep", "label": "Deep Dive", "url": ""},
            {"id": "critique", "label": "Critique", "url": ""},
        ],
        "audit": {
            "right": [
                "The packet is generated from canonical atoms, so the topbar is no longer detached from the framework's source of truth.",
                "Equations and fruit audit logic are exposed as callable registry-backed layers rather than prose-only references.",
            ],
            "overstated": [
                "Most imported Master Equation atoms remain captured/draft rather than formally verified.",
                "The fruit audit is lexical first-pass triage until upgraded with semantic model scoring and human review.",
            ],
            "wrong": [
                "No live external API key or hosted audio URLs are embedded in this packet.",
            ],
        },
        "reader_layers": build_reader_layers(claims, mtl),
    }
    write_json(out_path, packet)
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a topbar fill packet from Faith Through Physics atoms.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output TOPBAR_FILL_PACKET JSON path.")
    args = parser.parse_args()
    packet = build_packet(args.out)
    print(f"[ok] wrote {args.out}")
    print(f"[ok] terms={len(packet['terms'])} claims={len(packet['claims'])} proofs={len(packet['proofs'])} mtl={len(packet['mtl'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
