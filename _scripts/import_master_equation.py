r"""Build Master Equation atoms from the axiom registry and formal layer notes.

Generates:

  - _vocab/master_equation_registry.json
  - master-equation/01_canonical/ME-01-010-*.jsonld and later

The importer depends on _vocab/axiom_registry.json, which is produced by
_scripts/import_master_axioms.py.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
AXIOM_REGISTRY = REPO / "_vocab" / "axiom_registry.json"
OUT_DIR = REPO / "master-equation" / "01_canonical"
REGISTRY_PATH = REPO / "_vocab" / "master_equation_registry.json"

FORMAL_LAYER = REPO / "_INBOX_HARVEST_TRUTH_CARDS" / "01_FORMAL_LAYER_Definition10.md"
BRIDGE_LAYER = REPO / "_INBOX_HARVEST_TRUTH_CARDS" / "02_PHYSICAL_THEOLOGICAL_LAYER_TenFactorTable.md"
VERIFICATION_REPORT = REPO / "_INBOX_HARVEST_TRUTH_CARDS" / "VERIFIED_SECTION_BY_SECTION_REPORT.md"

FACTOR_ROWS = [
    {
        "id": "ME-01-020",
        "symbol": "G",
        "name": "External Negentropy Influx",
        "domain": "R>=0",
        "definition": "External negentropy influx rate.",
        "plain": "Coherence cannot be self-sufficient in a closed system; it needs an outside influx.",
        "axiom": "AX-059",
        "tags": ["grace", "entropy", "coherence"],
    },
    {
        "id": "ME-01-021",
        "symbol": "M",
        "name": "Alignment Cosine",
        "domain": "[-1, 1]",
        "definition": "Alignment cosine between system state vector and reference vector.",
        "plain": "A system couples most strongly when it is aligned with its reference.",
        "axiom": "AX-067",
        "tags": ["symmetry", "coherence"],
    },
    {
        "id": "ME-01-022",
        "symbol": "E",
        "name": "Signal Propagation Fidelity",
        "domain": "R>=0",
        "definition": "Signal propagation fidelity, structurally matching channel capacity.",
        "plain": "Truth transmission depends on whether signal survives noise.",
        "axiom": "AX-003",
        "tags": ["information", "signal-noise", "truth"],
    },
    {
        "id": "ME-01-023",
        "symbol": "S_eff",
        "name": "Effective Entropy Factor",
        "domain": "(0, 1]",
        "definition": "S_eff = exp(-eta * S_prod), or rationally 1/(1 + S_prod), so raw entropy production reduces coherence contribution.",
        "plain": "Entropy does not feed coherence directly; it enters as the thing that lowers the contribution.",
        "axiom": "AX-092",
        "tags": ["entropy", "decoherence"],
    },
    {
        "id": "ME-01-024",
        "symbol": "T",
        "name": "Temporal Integration",
        "domain": "R>0",
        "definition": "Temporal integration parameter.",
        "plain": "Time turns possibility into accumulated consequence.",
        "axiom": "AX-097",
        "tags": ["phase-transition"],
    },
    {
        "id": "ME-01-025",
        "symbol": "K",
        "name": "Information Compression Ratio",
        "domain": "R>=0",
        "definition": "Information compression ratio grounded in Kolmogorov complexity.",
        "plain": "Ordered meaning compresses; random noise does not.",
        "axiom": "AX-029",
        "tags": ["information", "logos", "coherence"],
    },
    {
        "id": "ME-01-026",
        "symbol": "R",
        "name": "Phase Transition Indicator",
        "domain": "{0, 1}",
        "definition": "Phase transition indicator for irreversible state change.",
        "plain": "Some thresholds do not merely change degree; they change state.",
        "axiom": "AX-062",
        "tags": ["phase-transition"],
    },
    {
        "id": "ME-01-027",
        "symbol": "Q",
        "name": "Superposition Measure",
        "domain": "[0, 1]",
        "definition": "Measure of unresolved state space before selection or collapse.",
        "plain": "Open possibility remains unresolved until actualization.",
        "axiom": "AX-045",
        "tags": ["observer", "faith"],
    },
    {
        "id": "ME-01-028",
        "symbol": "F",
        "name": "Non-Local Correlation Strength",
        "domain": "[0, 1]",
        "definition": "Non-local correlation strength, including entanglement or relational bond.",
        "plain": "Related systems are no longer fully independent.",
        "axiom": "AX-080",
        "tags": ["faith", "covenant", "coherence"],
    },
    {
        "id": "ME-01-029",
        "symbol": "C",
        "name": "Total Integration Measure",
        "domain": "[0, 1]",
        "definition": "Total integration or local global-coherence measure inside the product.",
        "plain": "C is the local integrator inside the product; chi is the output after integration.",
        "axiom": "AX-017",
        "tags": ["coherence", "logos"],
    },
]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:80]


def load_axiom_items() -> dict[str, dict[str, Any]]:
    data = json.loads(AXIOM_REGISTRY.read_text(encoding="utf-8"))
    return {item["axiomID"]: item for item in data["items"]}


def base_atom(atom_id: str, name: str, claim_class: str, status: str = "captured") -> dict[str, Any]:
    return {
        "@context": [
            "https://schema.org",
            "https://faiththruphysics.com/vocab/context.jsonld",
        ],
        "@type": "Claim",
        "@id": f"https://faiththruphysics.com/claims/master-equation/01/{atom_id}",
        "nodeID": f"tp:master-equation/01/{atom_id}",
        "claimID": f"tp:ME/{atom_id}",
        "nodeType": "claim",
        "name": name,
        "author": [
            {"@type": "Person", "name": "David Lowe"},
            {"@type": "SoftwareApplication", "name": "GPT (OpenAI)", "tp:role": "ai-collaborator"},
            {"@type": "SoftwareApplication", "name": "Claude (Anthropic)", "tp:role": "ai-collaborator"},
        ],
        "aiContributionDeclared": True,
        "dateCreated": "2026-07-28",
        "dateModified": date.today().isoformat(),
        "version": "0.1.0",
        "claimClass": claim_class,
        "domainType": "master-equation",
        "stage": "01_canonical",
        "status": status,
        "audienceLevel": "informed_adult",
        "paradigmRelation": "reframes",
        "evidenceType": "formal_derivation",
        "kernelChecked": False,
        "challengeStatus": "unchallenged",
        "axiomRoot": "https://faiththruphysics.com/claims/axioms/01/AX-135",
    }


def depends_on(target: str, note: str) -> dict[str, Any]:
    return {"type": "dependsOn", "target": target, "propagates": True, "note": note}


def ax_target(ax_id: str) -> str:
    return f"tp:axioms/01/{ax_id}"


def write_atom(atom: dict[str, Any]) -> str:
    atom_id = atom["nodeID"].split("/")[-1]
    filename = f"{atom_id}-{slugify(atom['name'])}.jsonld"
    (OUT_DIR / filename).write_text(json.dumps(atom, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f"master-equation/01_canonical/{filename}"


def axiom_claim(ax: dict[str, Any], atom_id: str) -> dict[str, Any]:
    atom = base_atom(atom_id, ax["title"], ax["claimClass"], status="captured")
    atom["statementTechnical"] = ax["title"]
    atom["statementPlain"] = ax["title"]
    atom["edges"] = [depends_on(ax_target(ax["axiomID"]), "Source registry row imported from Master Axiom.")]
    atom["keywords"] = [ax["axiomID"], ax.get("oldID", ""), ax.get("newType", "")]
    atom["tags"] = ["logos", "coherence", "equation"]
    atom["verificationStatus"] = "registry-import"
    atom["sourceReference"] = AXIOM_REGISTRY.as_posix()
    atom["masterEquationRole"] = {
        "sourceAxiomID": ax["axiomID"],
        "sourceOldID": ax.get("oldID", ""),
        "sourceRow": ax.get("sourceRow"),
        "sourceType": ax.get("newType", ""),
    }
    return atom


def main() -> int:
    if not AXIOM_REGISTRY.exists():
        raise SystemExit("Run _scripts/import_master_axioms.py first.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("ME-01-0[1-9][0-9]-*.jsonld"):
        if old.name.startswith(("ME-01-001-", "ME-01-002-")):
            continue
        old.unlink()

    axioms = load_axiom_items()
    written: list[dict[str, Any]] = []

    # Central integration claim from AX-135.
    ax135 = axioms["AX-135"]
    core = base_atom("ME-01-010", "Master Equation Integration", "theorem", status="captured")
    core["statementTechnical"] = (
        "All fundamental dynamics integrate into a single unified framework under chi, "
        "with formal factor slots and dependency constraints tracked as first-class atoms."
    )
    core["statementPlain"] = (
        "The Master Equation is the framework's integration center: the place where the "
        "ten factor rails become one computable coherence structure."
    )
    core["mathematicalForm"] = "chi_total = integral(G * M * E * S_eff * T * K * R * Q * F * C) d^3x dt"
    core["mathFormNormal"] = "chi = product([G,M,E,S_eff,T,K,R,Q,F,C]) integrated over region and time"
    core["edges"] = [
        depends_on(ax_target("AX-135"), "Axiom registry source: Master Equation Integration."),
        depends_on(ax_target("AX-012"), "Earlier Master Equation first form."),
        depends_on(ax_target("AX-021"), "Master coherence equation."),
    ]
    core["tags"] = ["logos", "coherence", "equation"]
    core["keywords"] = ["master-equation", "chi", "ten-factors", "integration"]
    core["verificationStatus"] = "registry-import"
    core["falsificationCondition"] = "Show the ten laws are inconsistent with each other, or that the master equation is overconstrained or internally contradictory."
    core["sourceReference"] = "; ".join([str(FORMAL_LAYER), str(BRIDGE_LAYER), str(AXIOM_REGISTRY)])
    path = write_atom(core)
    written.append({"id": "ME-01-010", "title": core["name"], "path": path, "role": "integration"})

    # Ten formal factor atoms.
    factor_ids = []
    for factor in FACTOR_ROWS:
        atom = base_atom(factor["id"], f"{factor['symbol']} - {factor['name']}", "definition", status="captured")
        atom["statementTechnical"] = factor["definition"]
        atom["statementPlain"] = factor["plain"]
        atom["mathematicalForm"] = f"{factor['symbol']} in {factor['domain']}"
        atom["edges"] = [
            depends_on("tp:master-equation/01/ME-01-010", "Factor slot belongs to the Master Equation integration atom."),
            depends_on(ax_target(factor["axiom"]), f"Factor is grounded by {factor['axiom']} in the axiom spine."),
        ]
        atom["tags"] = factor["tags"]
        atom["keywords"] = ["master-equation-factor", factor["symbol"], factor["domain"]]
        atom["verificationStatus"] = "formal-layer-import"
        atom["sourceReference"] = str(FORMAL_LAYER)
        atom["masterEquationFactor"] = factor
        path = write_atom(atom)
        factor_ids.append(factor["id"])
        written.append({"id": factor["id"], "title": atom["name"], "path": path, "role": "factor"})

    # Law I-X rows from AX-136 through AX-145.
    law_ids = []
    for n, ax_id in enumerate([f"AX-{i:03d}" for i in range(136, 146)], start=40):
        ax = axioms[ax_id]
        atom = axiom_claim(ax, f"ME-01-{n:03d}")
        atom["name"] = ax["title"]
        atom["statementTechnical"] = f"{ax['title']} is a Master Equation law definition imported from the axiom spine."
        atom["statementPlain"] = f"{ax['title']} names one law rail inside the Master Equation."
        atom["edges"].insert(0, depends_on("tp:master-equation/01/ME-01-010", "Law belongs to the Master Equation integration atom."))
        atom["sourceReference"] = "; ".join([str(BRIDGE_LAYER), str(AXIOM_REGISTRY)])
        atom["masterEquationRole"]["role"] = "law"
        path = write_atom(atom)
        law_ids.append(atom["nodeID"].split("/")[-1])
        written.append({"id": atom["nodeID"].split("/")[-1], "title": atom["name"], "path": path, "role": "law"})

    # Full equation from AX-146.
    ax146 = axioms["AX-146"]
    full = axiom_claim(ax146, "ME-01-060")
    full["statementTechnical"] = "The corrected full Master Equation multiplies the ten formal factors, using S_eff rather than raw S_prod, and integrates the product over region and time."
    full["statementPlain"] = "The full equation says coherence is not a sum of nice things. It is a product, so any required channel collapsing matters to the whole."
    full["mathematicalForm"] = "chi_total = integral_{t0}^{t1} integral_Omega G*M*E*S_eff*T*K*R*Q*F*C d^3x dt"
    full["mathFormNormal"] = "chi_total = integrate(product(ten_factor_slots), space, time)"
    full["edges"] = [
        depends_on("tp:master-equation/01/ME-01-010", "Full equation instantiates the integration claim."),
        *[depends_on(f"tp:master-equation/01/{fid}", "Full equation uses this formal factor slot.") for fid in factor_ids],
        depends_on(ax_target("AX-146"), "Axiom registry source: Full Master Equation."),
    ]
    full["sourceReference"] = str(FORMAL_LAYER)
    full["tags"] = ["logos", "coherence", "equation", "proof"]
    path = write_atom(full)
    written.append({"id": "ME-01-060", "title": full["name"], "path": path, "role": "full-equation"})

    # Verification-kernel interpretation.
    kernel = base_atom("ME-01-061", "Product-Collapse Kernel Boundary", "theorem", status="captured")
    kernel["statementTechnical"] = (
        "The verified Lean kernel proves the general product-collapse architecture: "
        "under the declared algebraic interface, product collapse is equivalent to at least one zero factor, "
        "and chi inherits zero collapse through the MasterState packaging."
    )
    kernel["statementPlain"] = (
        "The machine proof verifies the skeleton: in this architecture, one dead required channel kills the product, "
        "and a live product requires all required channels to stay nonzero."
    )
    kernel["mathematicalForm"] = "listProd xs = zero iff zero in xs; chi_zero_if_any_factor_zero"
    kernel["edges"] = [
        depends_on("tp:master-equation/01/ME-01-060", "Kernel verifies the product-collapse architecture used by the full equation."),
        depends_on(ax_target("AX-132"), "Falsification criterion for chi-field architecture."),
    ]
    kernel["tags"] = ["proof", "kill-condition", "coherence"]
    kernel["keywords"] = ["Lean", "zero-collapse", "product architecture", "no-zero-divisors"]
    kernel["verificationStatus"] = "lean4-section-report"
    kernel["kernelChecked"] = True
    kernel["status"] = "captured"
    kernel["sourceReference"] = str(VERIFICATION_REPORT)
    path = write_atom(kernel)
    written.append({"id": "ME-01-061", "title": kernel["name"], "path": path, "role": "verification-boundary"})

    # Theorem that the laws derive from chi from AX-147.
    ax147 = axioms["AX-147"]
    derivation = axiom_claim(ax147, "ME-01-062")
    derivation["statementTechnical"] = "All ten laws are represented as derivative rails of the chi architecture, with symmetry pairs 1<->8, 2<->9, 3<->10, 4<->7, and 5<->6 recorded as a theorem-level claim."
    derivation["statementPlain"] = "The ten laws are not loose decorations around the equation; they are claimed to be rails derived from chi."
    derivation["edges"] = [
        depends_on("tp:master-equation/01/ME-01-010", "Derivation theorem depends on the integration atom."),
        depends_on("tp:master-equation/01/ME-01-060", "Derivation theorem depends on the full equation atom."),
        *[depends_on(f"tp:master-equation/01/{lid}", "Derivation theorem depends on this law rail.") for lid in law_ids],
        depends_on(ax_target("AX-147"), "Axiom registry source: Laws Derive From Chi."),
    ]
    derivation["sourceReference"] = str(AXIOM_REGISTRY)
    derivation["tags"] = ["logos", "coherence", "proof"]
    path = write_atom(derivation)
    written.append({"id": "ME-01-062", "title": derivation["name"], "path": path, "role": "derivation-theorem"})

    registry = {
        "generatedAt": date.today().isoformat(),
        "sourceAxiomRegistry": str(AXIOM_REGISTRY),
        "sourceDocuments": [str(FORMAL_LAYER), str(BRIDGE_LAYER), str(VERIFICATION_REPORT)],
        "totalAtoms": len(written),
        "factorCount": len(factor_ids),
        "lawCount": len(law_ids),
        "atoms": written,
        "formalNoDriftRules": [
            "Ten factors only: G, M, E, S_eff, T, K, R, Q, F, C.",
            "S enters as S_eff, not raw S_prod.",
            "C is a factor; chi is the integrated output.",
            "Teaching laws must reduce to the formal factor layer.",
        ],
    }
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(written)} Master Equation atoms")
    print(f"Wrote registry to {REGISTRY_PATH}")
    print(f"Factors: {len(factor_ids)}; Laws: {len(law_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
