#!/usr/bin/env python3
"""Audit staged axiom-domain atoms against the Lean attack-surface rules.

The axiom domain can contain definitions, lemmas, theorems, equations, bridge
claims, evidence nodes, and open problems. The Lean axiom bundle cannot. This
script separates the staged atoms into formal roles before transfer so the
public/API layer does not call every foundation-domain node an axiom.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
DEFAULT_STAGING = Path(r"C:\theophysics\ATOMS_STAGING\axioms\01_canonical")
DEFAULT_REPORT = REPO / "_runtime" / "lean_axiom_bundle_audit.json"
DEFAULT_REGISTRY = REPO / "_vocab" / "lean_axiom_bundle_registry.json"

MINIMUM_BUNDLE = [
    ("AB1", "Reality exists."),
    ("AB2", "Distinction is possible."),
    ("AB3", "Relation is possible."),
    ("AB4", "Information/intelligibility is possible."),
    ("AB5", "Agents can act."),
    ("AB6", "Actions can preserve or degrade relation/coherence."),
    ("AB7", "Degradation without restoration cannot be called moral good."),
    ("AB8", "Restoration requires a source or operation not reducible to unrepaired damage itself."),
    ("AB9", "Justice requires damage/cost to be truthfully accounted for."),
    ("AB10", "Mercy requires restoration without falsifying justice."),
    ("AB11", "Grace is non-coercive restorative input."),
    ("AB12", "Coherence is the integrated state where truth, relation, justice, mercy, and restoration do not contradict."),
]

PUBLIC_STATUS = [
    "CANON",
    "LEAN_SUPPORTED",
    "RUNTIME_SUPPORTED",
    "STRONG_BUT_NEEDS_SOURCING",
    "USEFUL_BUT_UNVERIFIED",
    "SPECULATIVE",
    "OPEN_BRIDGE",
    "CONTRADICTED",
    "QUARANTINE",
]

DEPENDENCY_LABELS = [
    "NONE",
    "USES_PRIMITIVE",
    "USES_DEFINITION",
    "USES_BRIDGE_ASSUMPTION",
    "USES_THEOLOGICAL_IDENTIFICATION",
    "USES_EMPIRICAL_EVIDENCE",
    "USES_OPEN_CONJECTURE",
]

LEAN_FILE_ORDER = [
    "Theophysics/AxiomBundle.lean",
    "Theophysics/CoreDefinitions.lean",
    "Theophysics/BasicLemmas.lean",
    "Theophysics/MoralCoherence.lean",
    "Theophysics/ConsequenceAndCost.lean",
    "Theophysics/JusticeMercy.lean",
    "Theophysics/GraceRestoration.lean",
    "Theophysics/LawFamilyStructures.lean",
    "Theophysics/MasterEquationStructure.lean",
    "Theophysics/BridgeClaims.lean",
    "Theophysics/PublicClaimStatus.lean",
]

CLAIM_TYPE_TO_LEAN_ROLE = {
    "Primitive": "possible axiom / structure field",
    "Definition": "Lean def / structure / inductive",
    "FrameworkCommitment": "explicit bundle field or guarded bridge",
    "Equation": "def or theorem depending on role",
    "Property": "theorem or field depending on dependency status",
    "BoundaryCondition": "hypothesis / theorem context",
    "ObservableDomain": "metadata or runtime/test object",
    "Theorem": "proof target",
    "Lemma": "proof target",
    "BridgePrinciple": "explicit assumption or metadata",
    "Identification": "metadata / guarded theological bridge",
    "EvidenceNode": "outside Lean kernel",
    "Prediction": "outside Lean kernel, runtime/test object",
    "Protocol": "outside Lean kernel",
    "FalsificationCriterion": "outside Lean kernel or metadata",
    "MetaClaim": "documentation / metadata",
    "OpenProblem": "theorem stub with no false proof",
    "ClosureClaim": "only after dependencies close",
    "CapstoneTerminalClaim": "guarded theorem/bridge; no global uniqueness overclaim",
}

FIRST_THEOREM_TARGETS = [
    "T1 distinct classes remain distinct; canonical markers are not silently interchangeable.",
    "T2 alignedWithDestruction a -> degrades a s; alignedWithGood a -> preserves a s.",
    "T3 degraded + unrestored -> not alignedWithGood.",
    "T4 destructive alignment + unrestored -> not alignedWithGood.",
    "T5 zero factor/gate collapses the product model.",
    "T6 one nonzero factor is not sufficient for full coherence if other gates are missing.",
    "T7 selected transitions require named gates/relations.",
    "T8 invalid substitutions violate declared role constraints.",
    "T9 selected transitions are irreversible under declared stage rules.",
    "T10 mercy/restoration preserves truthful accounting instead of deleting the record.",
]

GUARDRAILS = [
    "Lean proves selected structural conditionals under stated assumptions; it does not prove God, Jesus, or Christianity from nothing.",
    "The Lagrangian-to-product-form bridge remains conditional until its open problem is closed.",
    "Fixed-point existence/stability may be local or conditional; do not claim global uniqueness unless proved.",
    "Python/Colab/runtime evidence supports tests and empirical fit; it does not become Lean proof automatically.",
    "Theological identifications require explicit bridge assumptions and must not enter the proof kernel silently.",
]

TRUE_PRIMITIVE = {
    ("axiom", "primitive"),
    ("axiom", "ontological_primitive"),
    ("operator", "ontological_primitive"),
    ("proposition", "primitive"),
    ("proposition", "primordial"),
}

LEAN_DEFINITION_CLASSES = {
    "definition",
    "unit",
    "operator",
    "scope_condition",
    "boundary_condition",
}

DERIVED_CLASSES = {
    "lemma",
    "theorem",
    "equation",
    "closure",
    "constraint",
    "proposition",
    "invariant",
    "terminus",
}

BRIDGE_CLASSES = {
    "bridge",
    "identity",
    "meta_claim",
}

EMPIRICAL_CLASSES = {
    "evidence",
    "prediction",
    "falsification",
    "expansion",
    "protocol",
}

OPEN_CLASSES = {
    "open_problem",
    "cosmology_term",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def atom_id(atom: dict[str, Any], path: Path) -> str:
    return str(atom.get("claimID") or atom.get("nodeID") or path.stem)


def role_for(atom: dict[str, Any]) -> str:
    claim_class = str(atom.get("claimClass") or "")
    source_status = str(atom.get("sourceStatus") or "")
    key = (claim_class, source_status)
    if key in TRUE_PRIMITIVE:
        return "primitive_assumption_candidate"
    if claim_class in LEAN_DEFINITION_CLASSES or source_status in {"definition", "scale_definition", "framework_bound_definition"}:
        return "definition"
    if claim_class in DERIVED_CLASSES or source_status in {"theorem", "equation", "logical_necessity", "corollary"}:
        return "derived_chain"
    if claim_class in BRIDGE_CLASSES or source_status in {"bridge", "identification", "meta_axiom", "stance", "framework_commitment"}:
        return "bridge_or_identification"
    if claim_class in EMPIRICAL_CLASSES or source_status in {"evidence", "prediction", "falsification", "experimental"}:
        return "empirical_or_runtime"
    if claim_class in OPEN_CLASSES or source_status in {"open_problem", "hypothesis", "hypothesis_prediction"}:
        return "open_conjecture"
    return "needs_human_classification"


def bundle_dependency_for(role: str) -> str:
    return {
        "primitive_assumption_candidate": "USES_PRIMITIVE",
        "definition": "USES_DEFINITION",
        "derived_chain": "USES_PRIMITIVE",
        "bridge_or_identification": "USES_THEOLOGICAL_IDENTIFICATION",
        "empirical_or_runtime": "USES_EMPIRICAL_EVIDENCE",
        "open_conjecture": "USES_OPEN_CONJECTURE",
        "needs_human_classification": "USES_OPEN_CONJECTURE",
    }.get(role, "USES_OPEN_CONJECTURE")


def public_status_for(role: str) -> str:
    return {
        "primitive_assumption_candidate": "STRONG_BUT_NEEDS_SOURCING",
        "definition": "CANON",
        "derived_chain": "LEAN_SUPPORTED",
        "bridge_or_identification": "OPEN_BRIDGE",
        "empirical_or_runtime": "RUNTIME_SUPPORTED",
        "open_conjecture": "SPECULATIVE",
        "needs_human_classification": "QUARANTINE",
    }.get(role, "QUARANTINE")


def compact_atom(atom: dict[str, Any], path: Path) -> dict[str, Any]:
    role = role_for(atom)
    return {
        "file": str(path),
        "id": atom_id(atom, path),
        "nodeID": atom.get("nodeID"),
        "name": atom.get("name"),
        "claimClass": atom.get("claimClass"),
        "sourceStatus": atom.get("sourceStatus"),
        "classification": atom.get("classification"),
        "role": role,
        "publicClaimStatus": public_status_for(role),
        "assumption_bundle_dependency": bundle_dependency_for(role),
        "edgeCount": len(atom.get("edges", [])),
        "sourceFile": atom.get("sourceFile"),
    }


def audit(staging: Path) -> dict[str, Any]:
    atoms = []
    for path in sorted(staging.glob("*.jsonld")):
        try:
            atom = read_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            atoms.append({"file": str(path), "role": "unreadable", "error": str(exc)})
            continue
        atoms.append(compact_atom(atom, path))

    by_role: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for atom in atoms:
        by_role[str(atom["role"])].append(atom)

    class_counts = Counter(str(atom.get("claimClass")) for atom in atoms)
    role_counts = Counter(str(atom["role"]) for atom in atoms)
    source_counts = Counter(str(atom.get("sourceStatus")) for atom in atoms)
    bundle_candidates = by_role["primitive_assumption_candidate"]

    warnings = []
    if len(bundle_candidates) > len(MINIMUM_BUNDLE):
        warnings.append(
            f"{len(bundle_candidates)} primitive candidates found for a {len(MINIMUM_BUNDLE)} item minimum bundle; David must ratify the front bundle."
        )
    if by_role["bridge_or_identification"]:
        warnings.append("Bridge/theological identification atoms are present and must not be treated as Lean primitives.")
    if by_role["needs_human_classification"]:
        warnings.append("Some atoms need human classification before promotion.")

    return {
        "source": str(staging),
        "totalAtoms": len(atoms),
        "claimClassCounts": dict(class_counts),
        "sourceStatusCounts": dict(source_counts),
        "roleCounts": dict(role_counts),
        "minimumBundleDraft": [{"id": key, "statement": value} for key, value in MINIMUM_BUNDLE],
        "publicStatuses": PUBLIC_STATUS,
        "dependencyLabels": DEPENDENCY_LABELS,
        "warnings": warnings,
        "roles": {role: items for role, items in sorted(by_role.items())},
    }


def registry_from_report(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "registryID": "lean-axiom-bundle-attack-surface",
        "purpose": "Keep the formal attack surface explicit: assumptions, definitions, derived theorems, bridges, empirical claims, and open conjectures are separate.",
        "starterLeanFile": "lean/Theophysics/AxiomBundle.lean",
        "recommendedFileOrder": LEAN_FILE_ORDER,
        "claimTypeToLeanRole": CLAIM_TYPE_TO_LEAN_ROLE,
        "firstTheoremTargets": FIRST_THEOREM_TARGETS,
        "guardrails": GUARDRAILS,
        "minimumBundleDraft": report["minimumBundleDraft"],
        "publicStatuses": PUBLIC_STATUS,
        "dependencyLabels": DEPENDENCY_LABELS,
        "roleCounts": report["roleCounts"],
        "rules": [
            "Only primitive_assumption_candidate atoms may be considered for the Lean front bundle.",
            "Definitions are controlled vocabulary, not discoveries.",
            "Derived-chain atoms must point back to assumptions/definitions and cannot be primitives.",
            "Bridge/theological identification atoms must be labeled OPEN_BRIDGE unless separately formalized.",
            "Empirical/runtime atoms may support the public case but do not enter the Lean kernel as axioms.",
            "Open conjectures stay speculative until repaired, sourced, or formally derived.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit staged axiom atoms for Lean bundle roles.")
    parser.add_argument("--staging", type=Path, default=DEFAULT_STAGING)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()

    report = audit(args.staging)
    write_json(args.report, report)
    write_json(args.registry, registry_from_report(report))
    print(f"[ok] wrote {args.report}")
    print(f"[ok] wrote {args.registry}")
    print(f"[ok] atoms={report['totalAtoms']}")
    for role, count in sorted(report["roleCounts"].items()):
        print(f"[ok] {role}={count}")
    for warning in report["warnings"]:
        print(f"[warn] {warning}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
