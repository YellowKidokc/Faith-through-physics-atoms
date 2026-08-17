#!/usr/bin/env python3
"""Axiom JSON-LD -> Rosetta Stone node adapter.

This is a projection layer only. It reads existing axiom atoms, writes
standardized Rosetta input envelopes, and never edits source atoms or promotes
any claim. The output is compatible with both Rosetta connector rails:

- nodes/: one JSON envelope per atom for chain_to_node_audit.py
- receipts/: one *.nodes.json batch receipt for run_rosetta_connector.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ADAPTER_VERSION = "axiom-rosetta-adapter/0.1.0"
NODE_SCHEMA_VERSION = "rosetta-axiom-node/v0.1"

REQUIRED_NODE_FIELDS = (
    "schema_version",
    "node_id",
    "atom_id",
    "claim_id",
    "title",
    "claim",
    "coherent_statement",
    "plain_statement",
    "formal_expressions",
    "scope_text",
    "truth_unit",
    "classification",
    "source",
    "governance",
)

CLAIM_CLASS_MAP = {
    "floor_axiom": ("HYPOTHESIS", "candidate_primitive", ["metaphysical_ontological"]),
    "theorem": ("THEOREM", "derived_result", ["logical", "mathematical"]),
    "definition": ("DEFINITION", "vocabulary", ["definitional"]),
    "empirical_anchor": ("EVIDENCE", "empirical_anchor", ["empirical_generalization"]),
    "empirical": ("EVIDENCE", "empirical_record", ["empirical_generalization"]),
    "mathematical": ("MODEL", "mathematical_model", ["mathematical"]),
    "boundary": ("BOUNDARY", "constraint", ["modal", "metaphysical_ontological"]),
    "prediction": ("PREDICTION", "prospective_test", ["empirical_generalization", "causal"]),
    "bridge": ("BRIDGE", "cross_domain_mapping", ["bridge_correspondence"]),
    "theological_interpretation": ("IDENTIFICATION", "theological_identification", ["theological", "interpretive"]),
}

NEW_TYPE_MAP = {
    "Definition": ("DEFINITION", "vocabulary", ["definitional"]),
    "Primitive": ("HYPOTHESIS", "candidate_primitive", ["metaphysical_ontological"]),
    "Theorem": ("THEOREM", "derived_result", ["logical", "mathematical"]),
    "Property": ("LEMMA", "derived_property", ["logical"]),
    "Equation": ("MODEL", "equation", ["mathematical"]),
    "BoundaryCondition": ("BOUNDARY", "constraint", ["modal"]),
    "ObservableDomain": ("BOUNDARY", "observable_domain", ["empirical_generalization"]),
    "FrameworkCommitment": ("CLOSURE", "framework_commitment", ["metaphysical_ontological"]),
    "EvidenceNode": ("EVIDENCE", "evidence_record", ["empirical_generalization"]),
    "Protocol": ("PROTOCOL", "procedure", ["causal"]),
    "Hypothesis": ("HYPOTHESIS", "proposed_untested", ["metaphysical_ontological"]),
    "UniversalPrinciple": ("HYPOTHESIS", "candidate_universal", ["universal", "metaphysical_ontological"]),
    "FalsificationCriterion": ("PROTOCOL", "falsification_test", ["empirical_generalization"]),
    "CapstoneTerminalClaim": ("CLOSURE", "terminal_claim", ["metaphysical_ontological"]),
    "BridgePrinciple": ("BRIDGE", "cross_domain_mapping", ["bridge_correspondence"]),
    "MetaClaim": ("CLOSURE", "meta_claim", ["metaphysical_ontological"]),
    "OpenProblem": ("OPEN", "open_problem", ["metaphysical_ontological"]),
    "Corollary": ("COROLLARY", "direct_consequence", ["logical"]),
    "Prediction": ("PREDICTION", "prospective_test", ["empirical_generalization"]),
    "Identification": ("IDENTIFICATION", "theological_identification", ["theological", "interpretive"]),
    "Operator": ("MODEL", "operator", ["mathematical"]),
    "ClosureClaim": ("CLOSURE", "closure_claim", ["metaphysical_ontological"]),
}

PROOF_LABEL_BY_STATUS = {
    "registry-import": "NOT_ESTABLISHED",
    "informal": "NOT_ESTABLISHED",
    "machine-verified": "PYTHON_RUNTIME_SUPPORTED",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return " ".join(clean_text(item) for item in value if clean_text(item))
    if isinstance(value, dict):
        return " ".join(clean_text(item) for item in value.values() if clean_text(item))
    return " ".join(str(value).split())


def as_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def atom_sort_key(path: Path) -> tuple[int, str]:
    match = re.match(r"AX-(\d+)", path.name)
    return (int(match.group(1)) if match else 999999, path.name)


def atom_id_from_file(path: Path, atom: dict[str, Any]) -> str:
    registry_id = clean_text(atom.get("axiomRegistry", {}).get("axiomID"))
    if registry_id:
        return registry_id
    node_id = clean_text(atom.get("nodeID"))
    if node_id:
        return node_id.rsplit("/", 1)[-1]
    return path.stem


def dependency_targets(atom: dict[str, Any]) -> list[str]:
    deps: list[str] = []
    for edge in as_list(atom.get("edges")):
        if isinstance(edge, dict) and edge.get("type") == "dependsOn" and edge.get("target"):
            deps.append(clean_text(edge.get("target")))
    return sorted(dict.fromkeys(dep for dep in deps if dep))


def infer_claim_species(unified_type: str, fallback: list[str]) -> list[str]:
    by_type = {
        "DEFINITION": ["definitional"],
        "LEMMA": ["logical"],
        "THEOREM": ["logical", "mathematical"],
        "COROLLARY": ["logical"],
        "MODEL": ["mathematical"],
        "HYPOTHESIS": ["metaphysical_ontological"],
        "PREDICTION": ["empirical_generalization"],
        "PROTOCOL": ["causal"],
        "EVIDENCE": ["empirical_generalization"],
        "BRIDGE": ["bridge_correspondence"],
        "IDENTIFICATION": ["theological", "interpretive"],
        "OPEN": ["metaphysical_ontological"],
        "CLOSURE": ["metaphysical_ontological"],
    }
    return sorted(dict.fromkeys(by_type.get(unified_type, fallback)))


def proof_label_for(atom: dict[str, Any]) -> str:
    if atom.get("kernelChecked") is True:
        return "LEAN_GUARDRAIL_SUPPORTED"
    status = clean_text(atom.get("verificationStatus"))
    return PROOF_LABEL_BY_STATUS.get(status, "NOT_ESTABLISHED")


def reference_hints(old_id: str, schema: dict[str, Any]) -> dict[str, Any]:
    """Return exact-ID Rosetta reference hints only; no semantic routing here."""
    if not old_id:
        return {"proof_step_ids": [], "chain_steps": [], "keeper_deck_ids": []}
    proof_ids = [
        clean_text(item.get("id"))
        for item in schema.get("proof_stack", [])
        if clean_text(item.get("id")) == old_id
    ]
    chain_steps = []
    for item in schema.get("chain", []):
        layer = clean_text(item.get("layer"))
        if old_id and old_id in layer:
            chain_steps.append(item.get("step"))
    keeper_ids = [
        clean_text(item.get("id"))
        for item in schema.get("keeper_deck", [])
        if clean_text(item.get("id")) == old_id
    ]
    return {
        "proof_step_ids": sorted(dict.fromkeys(proof_ids)),
        "chain_steps": chain_steps,
        "keeper_deck_ids": sorted(dict.fromkeys(keeper_ids)),
    }


def fingerprint_basis(node_id: str, title: str, claim: str, question: str, domain: str, species: list[str], deps: list[str], kill: list[str]) -> str:
    material = {
        "node_id": node_id,
        "title": title,
        "claim": claim,
        "question": question,
        "domain": domain,
        "claim_species": species,
        "dependencies": deps,
        "kill_conditions": kill,
    }
    return json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_node(path: Path, atom: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    registry = atom.get("axiomRegistry", {}) if isinstance(atom.get("axiomRegistry"), dict) else {}
    node_id = atom_id_from_file(path, atom)
    title = clean_text(atom.get("name")) or node_id
    technical = clean_text(atom.get("statementTechnical")) or clean_text(atom.get("statementPlain"))
    plain = clean_text(atom.get("statementPlain")) or technical
    formal = [clean_text(atom.get("mathematicalForm"))] if clean_text(atom.get("mathematicalForm")) else []
    question = clean_text(registry.get("questionType"))
    domain = clean_text(registry.get("domain")) or clean_text(atom.get("domainType"))
    native_class = clean_text(atom.get("claimClass")) or "unclassified"
    new_type = clean_text(registry.get("newType"))
    mapped = NEW_TYPE_MAP.get(new_type) or CLAIM_CLASS_MAP.get(native_class) or ("OPEN", "unmapped_native_role", ["metaphysical_ontological"])
    unified_type, derivation_role, species_fallback = mapped
    species = infer_claim_species(unified_type, species_fallback)
    deps = dependency_targets(atom)
    kill = [clean_text(atom.get("falsificationCondition"))] if clean_text(atom.get("falsificationCondition")) else []
    source_path = path.as_posix()
    source_hash = sha256_bytes(path.read_bytes())
    scope_parts = [
        clean_text(registry.get("treeLevel")),
        clean_text(registry.get("treeBranch")),
        clean_text(registry.get("moduleID")),
        clean_text(registry.get("moduleTitle")),
    ]
    scope_text = " | ".join(part for part in scope_parts if part and part != "—")
    status = clean_text(atom.get("status")) or "unknown"
    proof_label = proof_label_for(atom)
    hints = reference_hints(clean_text(registry.get("oldID")), schema)
    basis = fingerprint_basis(node_id, title, technical, question, domain, species, deps, kill)

    node: dict[str, Any] = {
        "schema_version": NODE_SCHEMA_VERSION,
        "node_id": node_id,
        "trace_id": node_id,
        "atom_id": clean_text(atom.get("nodeID")) or f"tp:axioms/01/{node_id}",
        "claim_id": clean_text(atom.get("claimID")) or None,
        "canonical_uri": clean_text(atom.get("@id")) or None,
        "title": title,
        "claim": technical,
        "coherent_statement": technical,
        "plain_statement": plain,
        "formal_expressions": formal,
        "scope_text": scope_text,
        "dependencies": deps,
        "kill_conditions": kill,
        "truth_unit": {
            "claim": technical,
            "question": question or None,
            "evidence": [],
            "proof_link": None,
            "verdict": "not_evaluated_registry_import",
        },
        "classification": {
            "native_claim_class": native_class,
            "native_new_type": new_type or None,
            "unified_claim_type": unified_type,
            "unified_claim_type_status": "adapter_candidate",
            "derivation_role": derivation_role,
            "claim_species": species,
            "domain": domain or None,
            "stage": clean_text(atom.get("stage")) or None,
            "proof_label": proof_label,
            "truth_status": {
                "ontic": "unknown",
                "epistemic": "insufficient",
            },
        },
        "rosetta_targets": {
            "exact_id_hints": hints,
            "routing_status": "unrouted",
            "chain_step": None,
            "proof_step_id": None,
            "family_symbol": None,
        },
        "mirror_search": {
            "required": True,
            "status": "not_run",
            "question": "What human-independent process has the same relational structure?",
        },
        "source": {
            "path": source_path,
            "sha256": source_hash,
            "stage": clean_text(atom.get("stage")) or None,
            "source_reference": clean_text(atom.get("sourceReference")) or None,
            "workbook": atom.get("sourceWorkbook") or None,
        },
        "governance": {
            "candidate_or_admitted": "Candidate",
            "kernelChecked": bool(atom.get("kernelChecked", False)),
            "propagates_evidence": False,
            "propagates_falsification": False,
            "boundary": "Adapter projection and Rosetta routing only. No source atom is edited; no match is proof, admission, canonization, or a truth verdict.",
        },
        "native": {
            "nodeType": clean_text(atom.get("nodeType")) or None,
            "domainType": clean_text(atom.get("domainType")) or None,
            "status": status,
            "challengeStatus": clean_text(atom.get("challengeStatus")) or None,
            "tags": as_list(atom.get("tags")),
            "keywords": as_list(atom.get("keywords")),
            "axiomRegistry": registry,
            "edges": as_list(atom.get("edges")),
        },
        "series_carry_forward": {
            "claim_fingerprint": f"sha256:{sha256_text(basis)}",
            "fingerprint_basis": "node_id + title + normalized claim + question + domain + species + dependencies + kill_conditions",
        },
    }

    if native_class == "bridge" or new_type == "BridgePrinciple":
        node["bridge_evaluation"] = {
            "bridge_type": "cross_domain",
            "status": "declared_not_tested",
            "bridge_grade": "B0",
            "failure_condition": kill[0] if kill else None,
        }

    if derivation_role == "candidate_primitive" or clean_text(registry.get("kernelRole")) == "candidateAxiom":
        node["compression_bridge"] = {
            "bridge_type": "kernel_compression",
            "source_node": node_id,
            "source_claim": title,
            "target_kernel": deps,
            "proposed_derivation": None,
            "compression_grade": "K0",
            "status": "candidate",
            "demotion_if_successful": "primitive -> derived",
            "failure_condition": kill[0] if kill else None,
        }

    return node


def validate_node(node: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_NODE_FIELDS:
        if field not in node:
            errors.append(f"missing required field: {field}")
    if not node.get("node_id"):
        errors.append("node_id is empty")
    if not node.get("claim"):
        errors.append("claim is empty")
    if node.get("schema_version") != NODE_SCHEMA_VERSION:
        errors.append(f"schema_version must be {NODE_SCHEMA_VERSION}")
    governance = node.get("governance", {})
    if governance.get("candidate_or_admitted") != "Candidate":
        errors.append("governance.candidate_or_admitted must remain Candidate")
    if governance.get("propagates_evidence") is not False:
        errors.append("governance.propagates_evidence must be false")
    if governance.get("propagates_falsification") is not False:
        errors.append("governance.propagates_falsification must be false")
    return errors


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Project axiom JSON-LD atoms into Rosetta Stone node envelopes.")
    parser.add_argument("--atoms-dir", default=str(ROOT.parents[1] / "axioms" / "01_canonical"), help="Folder containing AX-*.jsonld source atoms")
    parser.add_argument("--output-dir", required=True, help="Adapter output folder")
    parser.add_argument("--chain-schema", default=str(ROOT / "chain_schema.json"), help="Rosetta chain_schema.json for exact-ID hints")
    args = parser.parse_args()

    atoms_dir = Path(args.atoms_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    chain_schema_path = Path(args.chain_schema).resolve()
    schema = load_json(chain_schema_path)
    atom_paths = sorted(atoms_dir.glob("AX-*.jsonld"), key=atom_sort_key)
    if not atom_paths:
        raise SystemExit(f"No AX-*.jsonld atoms found under {atoms_dir}")

    nodes: list[dict[str, Any]] = []
    errors: dict[str, list[str]] = {}
    class_counts: Counter[str] = Counter()
    native_counts: Counter[str] = Counter()
    hint_counts: Counter[str] = Counter()
    seen_node_ids: set[str] = set()

    nodes_dir = output_dir / "nodes"
    receipts_dir = output_dir / "receipts"
    nodes_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir(parents=True, exist_ok=True)

    for path in atom_paths:
        atom = load_json(path)
        node = build_node(path, atom, schema)
        node_errors = validate_node(node)
        if node["node_id"] in seen_node_ids:
            node_errors.append(f"duplicate node_id: {node['node_id']}")
        seen_node_ids.add(node["node_id"])
        if node_errors:
            errors[str(path)] = node_errors
        nodes.append(node)
        class_counts[node["classification"]["unified_claim_type"]] += 1
        native_counts[node["classification"]["native_claim_class"]] += 1
        hints = node["rosetta_targets"]["exact_id_hints"]
        if hints["proof_step_ids"]:
            hint_counts["proof_step_exact_id"] += 1
        if hints["chain_steps"]:
            hint_counts["chain_layer_exact_id"] += 1
        if hints["keeper_deck_ids"]:
            hint_counts["keeper_deck_exact_id"] += 1
        write_json(nodes_dir / f"{node['node_id']}.rosetta.json", node)

    batch = {
        "trace_id": "axioms/01_canonical",
        "adapter": {
            "adapter_version": ADAPTER_VERSION,
            "generated_at": utc_now(),
            "source_dir": str(atoms_dir),
            "source_count": len(atom_paths),
            "node_count": len(nodes),
            "chain_schema": str(chain_schema_path),
            "chain_schema_sha256": sha256_bytes(chain_schema_path.read_bytes()),
            "boundary": "Adapter projection only. Source atoms are unchanged; all outputs are candidate routing inputs, not proof, admission, canonization, or truth verdicts.",
        },
        "result": {"semantic_nodes": nodes},
    }
    write_json(receipts_dir / "axioms_01_canonical.nodes.json", batch)

    report = {
        "adapter_version": ADAPTER_VERSION,
        "generated_at": utc_now(),
        "source_dir": str(atoms_dir),
        "output_dir": str(output_dir),
        "source_count": len(atom_paths),
        "node_count": len(nodes),
        "duplicate_node_ids": len(atom_paths) - len(seen_node_ids),
        "unified_claim_type_counts": dict(sorted(class_counts.items())),
        "native_claim_class_counts": dict(sorted(native_counts.items())),
        "exact_id_hint_counts": dict(sorted(hint_counts.items())),
        "validation_errors": errors,
        "outputs": {
            "deterministic_connector_nodes": str(nodes_dir),
            "model_connector_batch": str(receipts_dir / "axioms_01_canonical.nodes.json"),
        },
    }
    write_json(output_dir / "ADAPTER_REPORT.json", report)
    print(json.dumps({"output_dir": str(output_dir), "nodes": len(nodes), "validation_errors": len(errors)}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
