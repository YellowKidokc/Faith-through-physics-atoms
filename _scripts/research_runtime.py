#!/usr/bin/env python3
"""Theophysics Research Runtime.

Universal local API layer for papers, stories, atoms, and topbar packets.
It keeps the prose readable while generating the hidden structure underneath:
claim logging, nothing-hidden checks, term typing, survival vector, and failure
propagation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import claim_runtime


REPO = Path(__file__).resolve().parents[1]
RUNTIME = REPO / "_runtime"
REGISTRY_PATH = REPO / "_vocab" / "research_runtime_registry.json"

HIDDEN_CHECKS = {
    "source": ("energy", "order", "information", "authority", "source", "input", "grace", "external"),
    "payer": ("cost", "pay", "paid", "payer", "burden", "debt", "sacrifice", "price"),
    "observer": ("observe", "observer", "measure", "verify", "witness", "interpret", "actualize"),
    "standard": ("standard", "success", "good", "truth", "target", "criterion", "measure"),
    "boundary": ("boundary", "closed system", "open system", "inside", "outside", "scope", "domain"),
    "scale": ("individual", "family", "community", "institution", "nation", "civilization", "cosmic", "scale"),
    "time": ("now", "later", "time", "future", "long-run", "generation", "asymptotic", "horizon"),
}

TERM_TYPES = {
    "G": "source",
    "grace": "source",
    "M": "measure",
    "meaning": "value judgment",
    "E": "variable",
    "entropy": "variable",
    "S_eff": "state",
    "self": "receiver",
    "T": "boundary condition",
    "time": "boundary condition",
    "K": "measure",
    "knowledge": "measure",
    "R": "relation",
    "relation": "relation",
    "Q": "state",
    "quantum": "state",
    "F": "operator",
    "faith": "operator",
    "C": "integrator",
    "Christ": "integrator",
    "observer": "observer",
    "boundary": "boundary condition",
    "justice": "value judgment",
    "mercy": "value judgment",
}

SURVIVAL_DIMENSIONS = {
    "grounding": ("primitive", "assumption", "axiom", "definition", "given"),
    "typeSafety": ("type", "operator", "variable", "observer", "boundary", "bridge"),
    "hiddenDependencyCompleteness": tuple(HIDDEN_CHECKS.keys()),
    "derivationDepth": ("derive", "therefore", "proof", "because", "implies", "follows"),
    "discriminability": ("blind", "match", "wrong parent", "confusion", "scrambling", "rival basis"),
    "countermodelSurvival": ("countermodel", "rival", "alternative", "explains better", "cannot explain"),
    "falsifiability": ("kill condition", "falsification", "would fail", "disprove", "failure"),
    "reproducibility": ("rerun", "script", "data source", "commit", "version", "reproduce"),
    "bidirectionality": ("bidirectional", "reverse", "forward", "prediction", "constraint"),
    "semanticFidelity": ("checksum", "translation", "formal", "public", "meaning"),
    "failureContainment": ("blast radius", "survive if false", "dependents", "fallback"),
    "provenanceIndependence": ("provenance", "witness", "independent", "prompt", "model", "human", "ai"),
}

REGISTERED_APIS = [
    ("Claim.register", "implemented", "_scripts/claim_runtime.py intake"),
    ("Claim.status", "implemented", "_scripts/claim_runtime.py intake"),
    ("Claim.dependencies", "implemented", "_scripts/claim_runtime.py graph"),
    ("Claim.kill_condition", "implemented", "atom falsificationCondition fields"),
    ("Claim.render", "implemented", "_scripts/build_topbar_packet.py"),
    ("Corpus.semantic_address", "registered", "pending semantic-address adapter"),
    ("Ledger.cost_and_consent", "registered", "pending Crown ledger adapter"),
    ("HIDDEN_SOURCE", "implemented", "_scripts/research_runtime.py manifest"),
    ("HIDDEN_PAYER", "implemented", "_scripts/research_runtime.py manifest"),
    ("HIDDEN_OBSERVER", "implemented", "_scripts/research_runtime.py manifest"),
    ("HIDDEN_STANDARD", "implemented", "_scripts/research_runtime.py manifest"),
    ("HIDDEN_BOUNDARY", "implemented", "_scripts/research_runtime.py manifest"),
    ("HIDDEN_SCALE", "implemented", "_scripts/research_runtime.py manifest"),
    ("HIDDEN_TIME", "implemented", "_scripts/research_runtime.py manifest"),
    ("TYPECHECK", "implemented", "_scripts/research_runtime.py manifest"),
    ("FAILURE_PROPAGATION", "implemented", "_scripts/research_runtime.py failure"),
    ("SURVIVAL_VECTOR", "implemented", "_scripts/research_runtime.py manifest"),
    ("BIDIRECTIONALITY", "registered", "requires mapping corpus"),
    ("BASIS_CHALLENGE", "registered", "requires benchmark corpus and rival bases"),
    ("DOMAIN_HOLDOUT", "registered", "requires preregistered holdout workflow"),
    ("BLIND_MATCH", "registered", "requires evaluator set or model panel"),
    ("ASSUMPTION_SWAP", "registered", "requires model-specific parameters"),
    ("SEMANTIC_CHECKSUM", "registered", "requires multi-layer source surfaces"),
    ("WITNESS_PANEL", "registered", "requires independent model calls"),
    ("PREDICTION_ESCROW", "registered", "requires timestamp/commit policy"),
    ("SCALE_SCAN", "registered", "requires claim-specific scales"),
    ("COUNTERMODEL", "registered", "requires rival model generator"),
    ("MISUSE_AUDIT", "implemented", "_scripts/research_runtime.py manifest"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def contains_any(text: str, markers: tuple[str, ...]) -> list[str]:
    low = text.lower()
    return [marker for marker in markers if re.search(r"\b" + re.escape(marker.lower()) + r"\b", low)]


def source_text(path: Path) -> str:
    text, _packet = claim_runtime.load_source(path)
    return normalize(claim_runtime.strip_html(text))


def nothing_hidden(text: str) -> dict[str, Any]:
    checks = {}
    for key, markers in HIDDEN_CHECKS.items():
        hits = contains_any(text, markers)
        checks[key] = {
            "status": "named" if hits else "missing",
            "markers": hits[:8],
            "question": {
                "source": "Where do energy, order, information, or authority enter?",
                "payer": "Who bears the cost?",
                "observer": "Who measures, verifies, interprets, or actualizes?",
                "standard": "What defines success, goodness, truth, or the target state?",
                "boundary": "What is inside the system, and what is outside?",
                "scale": "Is the claim local, global, individual, institutional, or cosmic?",
                "time": "Does the result hold now, later, asymptotically, or briefly?",
            }[key],
        }
    missing = [key for key, value in checks.items() if value["status"] == "missing"]
    return {
        "status": "nothing-hidden-pass" if not missing else "needs-review",
        "missing": missing,
        "checks": checks,
    }


def typecheck(text: str) -> dict[str, Any]:
    hits = []
    for term, typ in TERM_TYPES.items():
        pattern = r"(?<![A-Za-z0-9_])" + re.escape(term) + r"(?![A-Za-z0-9_])"
        if re.search(pattern, text, flags=re.I):
            hits.append({"term": term, "type": typ})
    by_term: dict[str, set[str]] = defaultdict(set)
    for hit in hits:
        by_term[hit["term"].lower()].add(hit["type"])
    silent_shifts = [
        {"term": term, "types": sorted(types)}
        for term, types in by_term.items()
        if len(types) > 1
    ]
    return {
        "terms": hits,
        "silentTypeShiftFlags": silent_shifts,
        "status": "typecheck-pass" if not silent_shifts else "needs-review",
    }


def survival_vector(text: str, hidden: dict[str, Any], type_result: dict[str, Any], claim_records: list[dict[str, Any]]) -> dict[str, Any]:
    vector = {}
    for dimension, markers in SURVIVAL_DIMENSIONS.items():
        if dimension == "hiddenDependencyCompleteness":
            named = 7 - len(hidden["missing"])
            score = 3 if named == 7 else 2 if named >= 5 else 1 if named >= 3 else 0
            evidence = [k for k, v in hidden["checks"].items() if v["status"] == "named"]
        elif dimension == "typeSafety":
            score = 2 if type_result["terms"] else 0
            if type_result["silentTypeShiftFlags"]:
                score = 1
            evidence = [hit["term"] for hit in type_result["terms"][:8]]
        else:
            hits = contains_any(text, markers)
            score = 2 if len(hits) >= 2 else 1 if hits else 0
            evidence = hits[:8]
        vector[dimension] = {
            "score": score,
            "meaning": ["absent", "named", "implemented", "independently-tested"][score],
            "evidence": evidence,
        }

    if claim_records:
        mapped = sum(1 for record in claim_records if record["classification"] in {"likely-existing-atom", "needs-review"})
        vector["grounding"]["score"] = max(vector["grounding"]["score"], 2 if mapped else 1)
        vector["grounding"]["meaning"] = ["absent", "named", "implemented", "independently-tested"][vector["grounding"]["score"]]
        vector["grounding"]["evidence"].append(f"{mapped}/{len(claim_records)} claims mapped or reviewable")

    lowest = min(vector.items(), key=lambda item: item[1]["score"])
    return {"scale": "0 absent, 1 named, 2 implemented, 3 independently tested", "lowestCoordinate": lowest[0], "dimensions": vector}


def misuse_audit(text: str) -> dict[str, Any]:
    risks = {
        "score_actions_not_souls": ("soul", "person is", "people are", "rank people", "score people"),
        "coercive_use": ("government", "coerce", "force compliance", "mandatory", "punish dissent"),
        "victim_cost_hidden": ("forgive and forget", "move on", "no cost", "without cost", "conceal"),
        "authority_capture": ("leader", "source", "cost-bearer", "submit to me", "unquestioned"),
        "insult_language": ("decoherent person", "decoherent people", "less coherent", "inferior"),
    }
    rows = []
    for risk, markers in risks.items():
        hits = contains_any(text, markers)
        rows.append({"risk": risk, "status": "flagged" if hits else "not-detected", "markers": hits})
    return {
        "boundary": "Score claims, actions, and systems; do not score souls.",
        "flags": [row for row in rows if row["status"] == "flagged"],
        "checks": rows,
    }


def manifest(path: Path, limit: int = 80) -> dict[str, Any]:
    text = source_text(path)
    claim_records = claim_runtime.intake(path, limit=limit)
    hidden = nothing_hidden(text)
    types = typecheck(text)
    survival = survival_vector(text, hidden, types, claim_records)
    misuse = misuse_audit(text)
    output = {
        "runtime": "theophysics-research-runtime",
        "version": "0.1.0",
        "generatedAt": now(),
        "source": str(path),
        "oneSentence": claim_records[0]["sentence"] if claim_records else "",
        "claimIDs": [record["runtimeClaimID"] for record in claim_records],
        "claimSummary": dict(Counter(record["classification"] for record in claim_records)),
        "hiddenDependencies": hidden,
        "types": types,
        "survivalVector": survival,
        "misuseAudit": misuse,
        "registeredButNotRun": [
            name for name, status, _target in REGISTERED_APIS if status == "registered"
        ],
    }
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", path.stem).strip("-").lower() or "source"
    out = RUNTIME / f"runtime_manifest.{slug}.json"
    claim_runtime.write_text(out, json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    output["_path"] = str(out)
    return output


def graph_index() -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    graph = claim_runtime.graph_from_atoms()
    nodes = {node["id"]: node for node in graph["nodes"]}
    reverse: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph["edges"]:
        reverse[edge["target"]].append(edge)
    return nodes, reverse


def failure_propagation(claim_id: str) -> dict[str, Any]:
    nodes, reverse = graph_index()
    direct = reverse.get(claim_id, [])
    visited = {claim_id}
    queue = deque((edge["source"], 1) for edge in direct)
    indirect = []
    while queue:
        node_id, depth = queue.popleft()
        if node_id in visited:
            continue
        visited.add(node_id)
        if depth > 1:
            indirect.append(node_id)
        for edge in reverse.get(node_id, []):
            queue.append((edge["source"], depth + 1))
    independent_count = max(0, len(nodes) - len(visited))
    return {
        "claimID": claim_id,
        "directDependentsInvalidated": [edge["source"] for edge in direct],
        "indirectDependentsWeakened": indirect,
        "claimsRequiringReview": sorted(set(edge["source"] for edge in direct) | set(indirect)),
        "independentClaimsUnaffectedCount": independent_count,
        "fallback": "Lower downstream claims to review/captured unless they name an independent rederivation artifact.",
    }


def write_registry() -> dict[str, Any]:
    registry = {
        "generatedAt": now(),
        "runtime": "theophysics-research-runtime",
        "apis": [
            {"name": name, "status": status, "target": target}
            for name, status, target in REGISTERED_APIS
        ],
    }
    claim_runtime.write_text(REGISTRY_PATH, json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
    return registry


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Theophysics Research Runtime services.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_manifest = sub.add_parser("manifest", help="Build runtime manifest for a source file.")
    p_manifest.add_argument("source", type=Path)
    p_manifest.add_argument("--limit", type=int, default=80)

    p_failure = sub.add_parser("failure", help="Show blast radius for a claim/node id.")
    p_failure.add_argument("claim_id")

    sub.add_parser("registry", help="Write runtime API registry.")

    args = parser.parse_args()
    if args.command == "manifest":
        result = manifest(args.source, limit=args.limit)
        print(f"[ok] manifest={result['_path']}")
        print(f"[ok] claims={len(result['claimIDs'])} lowest={result['survivalVector']['lowestCoordinate']}")
        return 0
    if args.command == "failure":
        print(json.dumps(failure_propagation(args.claim_id), ensure_ascii=False, indent=2))
        return 0
    if args.command == "registry":
        result = write_registry()
        print(f"[ok] registry={REGISTRY_PATH}")
        print(f"[ok] apis={len(result['apis'])}")
        return 0
    return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
