r"""Import key equations as first-class, queryable atoms.

Generates:

  - _vocab/equation_registry.json
  - master-equation/01_canonical/ME-EQ-*.jsonld
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "master-equation" / "01_canonical"
REGISTRY_PATH = REPO / "_vocab" / "equation_registry.json"

FORMAL_LAYER = REPO / "_INBOX_HARVEST_TRUTH_CARDS" / "01_FORMAL_LAYER_Definition10.md"
FRUITS_LAYER = REPO / "_INBOX_HARVEST_TRUTH_CARDS" / "fruits_of_the_spirit_equations.md"
VERIFICATION_REPORT = REPO / "_INBOX_HARVEST_TRUTH_CARDS" / "VERIFIED_SECTION_BY_SECTION_REPORT.md"


EQUATIONS = [
    {
        "id": "ME-EQ-001",
        "name": "Full Master Equation",
        "symbolic": "χ_total = ∫_{t0}^{t1} ∫_Ω G·M·E·S_eff·T·K·R·Q·F·C d^3x dt",
        "normal": "chi_total = integrate(product([G,M,E,S_eff,T,K,R,Q,F,C]), space, time)",
        "plain": "Total coherence is the integrated product of ten required factor slots.",
        "variables": ["G", "M", "E", "S_eff", "T", "K", "R", "Q", "F", "C", "χ_total"],
        "depends": ["tp:master-equation/01/ME-01-060", "tp:axioms/01/AX-146"],
        "tags": ["equation", "coherence", "logos"],
        "source": FORMAL_LAYER,
    },
    {
        "id": "ME-EQ-002",
        "name": "Local Product Form",
        "symbolic": "χ_local(x,t) = G(x,t)·M(x,t)·E(x,t)·S_eff(x,t)·T(x,t)·K(x,t)·R(x,t)·Q(x,t)·F(x,t)·C(x,t)",
        "normal": "chi_local = G*M*E*S_eff*T*K*R*Q*F*C",
        "plain": "At a local slice, coherence is multiplicative rather than additive.",
        "variables": ["G", "M", "E", "S_eff", "T", "K", "R", "Q", "F", "C", "χ_local"],
        "depends": ["tp:master-equation/01/ME-01-010", "tp:master-equation/01/ME-01-060"],
        "tags": ["equation", "coherence"],
        "source": FORMAL_LAYER,
    },
    {
        "id": "ME-EQ-003",
        "name": "Entropy Sign Repair",
        "symbolic": "S_eff(x,t) = exp(-η·S_prod(x,t))",
        "normal": "S_eff = exp(-eta*S_prod); alternative S_eff = 1/(1+S_prod)",
        "plain": "Raw entropy production is converted into an effective factor that decreases coherence.",
        "variables": ["S_eff", "S_prod", "η"],
        "depends": ["tp:master-equation/01/ME-01-023", "tp:axioms/01/AX-092"],
        "tags": ["equation", "entropy", "decoherence"],
        "source": FORMAL_LAYER,
    },
    {
        "id": "ME-EQ-004",
        "name": "Grace Dynamics",
        "symbolic": "dG/dt = G_ext - γG + β·F·C",
        "normal": "dG_dt = G_ext - gamma*G + beta*F*C",
        "plain": "Grace-like coherence influx grows through external source and relational coupling, while decaying under loss.",
        "variables": ["G", "G_ext", "γ", "β", "F", "C"],
        "depends": ["tp:master-equation/01/ME-01-043", "tp:axioms/01/AX-139"],
        "tags": ["equation", "grace", "coherence", "faith"],
        "source": FORMAL_LAYER,
    },
    {
        "id": "ME-EQ-005",
        "name": "Lowe Coherence Lagrangian",
        "symbolic": "L = χ(q,t)(1/2·qdot^T·K·qdot) - S·χ(q,t)",
        "normal": "L = chi(q,t)*(0.5*qdot^T*K*qdot) - S*chi(q,t)",
        "plain": "The Lagrangian treats coherence as weighting kinetic structure while entropy supplies the penalty term.",
        "variables": ["L", "χ", "q", "qdot", "K", "S"],
        "depends": ["tp:master-equation/01/ME-01-040", "tp:axioms/01/AX-136"],
        "tags": ["equation", "coherence", "entropy"],
        "source": REPO / "_INBOX_HARVEST_TRUTH_CARDS" / "01_Lowe_Coherence_Lagrangian_Formal_Test.md",
    },
    {
        "id": "ME-EQ-006",
        "name": "Zero-Collapse Theorem",
        "symbolic": "χ = 0 ⇔ ∃ required factor f_i = 0",
        "normal": "listProd(xs)=zero iff zero in xs",
        "plain": "A required zero channel collapses the product, and product collapse implies a zero channel under the kernel assumptions.",
        "variables": ["χ", "f_i", "zero", "listProd"],
        "depends": ["tp:master-equation/01/ME-01-061", "tp:axioms/01/AX-132"],
        "tags": ["equation", "proof", "kill-condition"],
        "source": VERIFICATION_REPORT,
        "kernelChecked": True,
    },
    {
        "id": "ME-EQ-007",
        "name": "Grace Non-Unitarity",
        "symbolic": "Ĝ†Ĝ ≠ I",
        "normal": "G_hat_dagger*G_hat != I",
        "plain": "Grace is modeled as information-adding transformation, not merely rearrangement of a closed state.",
        "variables": ["Ĝ", "I"],
        "depends": ["tp:master-equation/01/ME-01-048", "tp:axioms/01/AX-074"],
        "tags": ["equation", "grace", "information"],
        "source": FORMAL_LAYER,
    },
    {
        "id": "ME-EQ-008",
        "name": "Sign Conservation",
        "symbolic": "[σ̂, Û] = 0",
        "normal": "commutator(sigma_hat,U_hat)=0",
        "plain": "Self-generated unitary operations preserve the sign state.",
        "variables": ["σ̂", "Û"],
        "depends": ["tp:master-equation/01/ME-01-047", "tp:axioms/01/AX-068"],
        "tags": ["equation", "moral-conservation", "symmetry"],
        "source": FORMAL_LAYER,
    },
    {
        "id": "ME-EQ-009",
        "name": "Fruits Phase Transition",
        "symbolic": "Φ_i(χ) = tanh(β_i(χ - χ_c))",
        "normal": "Phi_i = tanh(beta_i*(chi-chi_c))",
        "plain": "Fruit and anti-fruit outputs appear as bounded phase behavior around a coherence threshold.",
        "variables": ["Φ_i", "χ", "β_i", "χ_c"],
        "depends": ["tp:axioms/01/AX-151"],
        "tags": ["equation", "coherence", "phase-transition"],
        "source": FRUITS_LAYER,
    },
    {
        "id": "ME-EQ-010",
        "name": "Fruit Vector",
        "symbolic": "Φ⃗ = {Love, Joy, Peace, Patience, Kindness, Goodness, Faithfulness, Gentleness, Self-Control}",
        "normal": "Phi_vector = [Love,Joy,Peace,Patience,Kindness,Goodness,Faithfulness,Gentleness,SelfControl]",
        "plain": "The fruits form a nine-dimensional observable output vector.",
        "variables": ["Φ⃗"],
        "depends": ["tp:axioms/01/AX-151", "tp:axioms/01/AX-152", "tp:axioms/01/AX-153", "tp:axioms/01/AX-154", "tp:axioms/01/AX-155", "tp:axioms/01/AX-156", "tp:axioms/01/AX-157", "tp:axioms/01/AX-158", "tp:axioms/01/AX-159", "tp:axioms/01/AX-160"],
        "tags": ["equation", "coherence"],
        "source": FRUITS_LAYER,
    },
]


def slugify(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def atom_for(eq: dict[str, Any]) -> dict[str, Any]:
    atom = {
        "@context": ["https://schema.org", "https://faiththruphysics.com/vocab/context.jsonld"],
        "@type": "Claim",
        "@id": f"https://faiththruphysics.com/claims/master-equation/01/{eq['id']}",
        "nodeID": f"tp:master-equation/01/{eq['id']}",
        "claimID": f"tp:ME/{eq['id']}",
        "nodeType": "claim",
        "name": eq["name"],
        "author": [
            {"@type": "Person", "name": "David Lowe"},
            {"@type": "SoftwareApplication", "name": "GPT (OpenAI)", "tp:role": "ai-collaborator"},
        ],
        "aiContributionDeclared": True,
        "dateCreated": "2026-07-28",
        "dateModified": date.today().isoformat(),
        "version": "0.1.0",
        "claimClass": "mathematical",
        "domainType": "master-equation",
        "stage": "01_canonical",
        "status": "captured",
        "audienceLevel": "informed_adult",
        "paradigmRelation": "reframes",
        "evidenceType": "formal_derivation",
        "statementTechnical": eq["symbolic"],
        "statementPlain": eq["plain"],
        "mathematicalForm": eq["symbolic"],
        "mathFormNormal": eq["normal"],
        "axiomRoot": "https://faiththruphysics.com/claims/axioms/01/AX-135",
        "edges": [
            {
                "type": "dependsOn",
                "target": target,
                "propagates": True,
                "note": "Equation atom dependency.",
            }
            for target in eq["depends"]
        ],
        "tags": eq["tags"],
        "keywords": ["equation", *eq["variables"]],
        "verificationStatus": "equation-registry-import",
        "kernelChecked": bool(eq.get("kernelChecked", False)),
        "challengeStatus": "unchallenged",
        "falsificationCondition": "Show the equation is ill-typed, contradicts its dependency atoms, or fails the verification/empirical burden declared by its source layer.",
        "sourceReference": str(eq["source"]),
        "equationRegistry": {
            "equationID": eq["id"],
            "variables": eq["variables"],
            "normalForm": eq["normal"],
            "source": str(eq["source"]),
        },
    }
    return atom


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("ME-EQ-*.jsonld"):
        old.unlink()

    items = []
    for eq in EQUATIONS:
        atom = atom_for(eq)
        filename = f"{eq['id']}-{slugify(eq['name'])}.jsonld"
        (OUT_DIR / filename).write_text(json.dumps(atom, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        items.append(
            {
                "equationID": eq["id"],
                "name": eq["name"],
                "symbolic": eq["symbolic"],
                "normal": eq["normal"],
                "variables": eq["variables"],
                "atomPath": f"master-equation/01_canonical/{filename}",
                "dependsOn": eq["depends"],
            }
        )

    REGISTRY_PATH.write_text(
        json.dumps(
            {
                "generatedAt": date.today().isoformat(),
                "totalEquations": len(items),
                "items": items,
                "queryContract": {
                    "byID": "_vocab/equation_registry.json.items[].equationID",
                    "byVariable": "_vocab/equation_registry.json.items[].variables",
                    "atomNodeID": "tp:master-equation/01/{equationID}",
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(items)} equation atoms")
    print(f"Wrote registry to {REGISTRY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
