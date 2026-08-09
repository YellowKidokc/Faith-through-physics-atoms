"""Canonical Definition Registry resolver and validator.

Discovery emits review proposals only. It never edits atoms, accepts an edge,
or promotes a definition. Definition proposals use the same adversarial receipt
feed and human-only acceptance rule as Claim Beacon proposals.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "_definitions" / "registry.jsonld"
PROPOSALS = REPO / "_proposals" / "definition-links.jsonl"
MARKER_RE = re.compile(r"\[\[def:([a-z0-9][a-z0-9/-]*)\]\]", re.I)
SCAN_SUFFIXES = {".md", ".html", ".jsonld"}
SINGLE_LETTER_UNSAFE = {"G", "M", "E", "S", "T", "K", "R", "Q", "F", "C"}


@dataclass(frozen=True)
class Match:
    definition_id: str
    matched: str
    method: str
    confidence: float
    status: str = "proposed"
    reason: str = ""


def load_registry(repo: Path = REPO) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    registry_path = repo / "_definitions" / "registry.jsonld"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    atoms = {}
    for item in registry["definitions"]:
        atom_path = registry_path.parent / item["atom"]
        atom = json.loads(atom_path.read_text(encoding="utf-8"))
        atoms[item["permanentDefinitionID"]] = atom
    return registry, atoms


def boundary_pattern(value: str) -> re.Pattern[str]:
    return re.compile(r"(?<![\w-])" + re.escape(value) + r"(?![\w-])", re.I)


def resolve_text(text: str, atoms: dict[str, dict[str, Any]]) -> list[Match]:
    found: dict[tuple[str, str, str], Match] = {}
    marker_spans = []
    for marker in MARKER_RE.finditer(text):
        marker_spans.append(marker.span())
        definition_id = "tp:def:" + marker.group(1).lower()
        if definition_id in atoms:
            match = Match(definition_id, marker.group(0), "explicit-marker", .99,
                          reason="Valid permanent ID named by an explicit definition marker.")
            found[(match.definition_id, match.matched.lower(), match.method)] = match
        else:
            match = Match(definition_id, marker.group(0), "explicit-marker", .99, "unresolved",
                          "Explicit marker does not exist in the registry.")
            found[(match.definition_id, match.matched.lower(), match.method)] = match
    scrubbed = MARKER_RE.sub(" ", text)
    term_owners: dict[str, list[str]] = {}
    for did, atom in atoms.items():
        for term in [atom["preferredTerm"], *atom.get("aliases", [])]:
            term_owners.setdefault(term.casefold(), []).append(did)
    for term, owners in term_owners.items():
        if boundary_pattern(term).search(scrubbed):
            if len(owners) > 1:
                for did in owners:
                    m = Match(did, term, "alias", .45, "unresolved", "Alias belongs to multiple definitions.")
                    found[(did, term, "alias")] = m
            else:
                did = owners[0]
                method = "preferred-term" if term == atoms[did]["preferredTerm"].casefold() else "alias"
                score = .9 if method == "preferred-term" else .78
                m = Match(did, term, method, score, reason="Boundary-safe canonical term match.")
                found[(did, term, method)] = m
    for did, atom in atoms.items():
        for spec in atom.get("associatedSymbols", []):
            symbol = spec["symbol"]
            if not boundary_pattern(symbol).search(scrubbed):
                continue
            # Single-letter variables are never connected by symbol alone. Context
            # is recorded for a reviewer, but explicit markers remain the safe path.
            if len(symbol) == 1 or symbol.upper() in SINGLE_LETTER_UNSAFE:
                m = Match(did, symbol, "symbol", .3, "unresolved",
                          "Single-letter symbol requires explicit marker or human resolution of namespace, equation position, domain, terminology, and existing edges.")
            else:
                m = Match(did, symbol, "symbol", .65, reason="Namespaced multi-character symbol match.")
            found[(did, symbol, "symbol")] = m
    return sorted(found.values(), key=lambda x: (x.definition_id, x.method, x.matched))


def proposal(path: Path, match: Match, repo: Path = REPO) -> dict[str, Any]:
    rel = path.relative_to(repo).as_posix()
    stable = f"{rel}|{match.definition_id}|{match.matched}|{match.method}"
    return {"protocol": "DefinitionLinkProposal", "protocolVersion": "1.0.0",
            "proposalID": "dlp-" + hashlib.sha256(stable.encode()).hexdigest()[:16],
            "sourceAtom": rel, "targetAtom": match.definition_id,
            "proposedEdgeType": "dependsOnDefinition", "matchReason": match.reason,
            "matchedText": match.matched, "matchMethod": match.method,
            "confidence": match.confidence, "status": match.status,
            "validationReceipt": {"validator": "_scripts/definition_resolver.py resolve",
                "method": "definition-resolver-v1", "createdAt": datetime.now(timezone.utc).isoformat(),
                "acceptedBy": None, "acceptedAt": None, "adversarialGateStatus": "pending",
                "humanReviewRequired": True}}


def scan(repo: Path = REPO) -> list[dict[str, Any]]:
    _, atoms = load_registry(repo)
    output = []
    ignored = {".git", "__pycache__", "_definitions", "_proposals"}
    for path in sorted(repo.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES or ignored.intersection(path.parts):
            continue
        for match in resolve_text(path.read_text(encoding="utf-8"), atoms):
            output.append(proposal(path, match, repo))
    return output


def write_proposals(repo: Path = REPO) -> list[dict[str, Any]]:
    rows = scan(repo)
    target = repo / "_proposals" / "definition-links.jsonl"
    target.parent.mkdir(exist_ok=True)
    target.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    return rows


def validate(repo: Path = REPO) -> list[str]:
    errors = []
    registry_path = repo / "_definitions" / "registry.jsonld"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    atoms = {}
    for entry in registry.get("definitions", []):
        atom_path = registry_path.parent / entry.get("atom", "")
        if not atom_path.is_file():
            errors.append(f"{entry.get('permanentDefinitionID')}: missing registry atom {entry.get('atom')}")
            continue
        atoms[entry["permanentDefinitionID"]] = json.loads(atom_path.read_text(encoding="utf-8"))
    ids = [x["permanentDefinitionID"] for x in registry["definitions"]]
    if len(ids) != len(set(ids)): errors.append("duplicate permanent definition ID in registry")
    seen_aliases: dict[str, str] = {}
    known_nodes = set(ids)
    for path in repo.rglob("*.jsonld"):
        try: data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError: continue
        known_nodes.update(str(data[k]) for k in ("nodeID", "claimID", "@id") if data.get(k))
    for entry in registry["definitions"]:
        did = entry["permanentDefinitionID"]
        if did not in atoms: continue
        atom = atoms[did]
        if atom.get("permanentDefinitionID") != did or atom.get("claimID") != did:
            errors.append(f"{did}: registry/atom permanent ID mismatch")
        if entry.get("canonicalStatus") != atom.get("canonicalStatus"):
            errors.append(f"{did}: registry/atom canonical status mismatch")
        source, policy = atom.get("source", {}), atom.get("citationPolicy", {})
        if policy.get("required") and not (source.get("exactShortQuotation") and source.get("authoritativeSourceURL")):
            errors.append(f"{did}: required citation lacks quote or link")
        if policy.get("inheritToDependents") not in (True, False) or (policy.get("inheritToDependents") and not policy.get("required")):
            errors.append(f"{did}: invalid citation inheritance")
        for alias in [atom.get("preferredTerm", ""), *atom.get("aliases", [])]:
            key = alias.casefold()
            if key in seen_aliases and seen_aliases[key] != did: errors.append(f"ambiguous alias '{alias}': {seen_aliases[key]} and {did}")
            seen_aliases[key] = did
        for edge in atom.get("edges", []):
            if edge.get("target") not in known_nodes: errors.append(f"{did}: broken edge {edge.get('target')}")
    return errors


def render(source: Path, output: Path, repo: Path = REPO) -> None:
    _, atoms = load_registry(repo)
    raw = source.read_text(encoding="utf-8")
    matches = [m for m in resolve_text(raw, atoms) if m.status == "proposed"]
    citations = []
    for did in dict.fromkeys(m.definition_id for m in matches):
        atom = atoms[did]
        if atom["citationPolicy"]["required"] and atom["citationPolicy"]["inheritToDependents"]:
            src = atom["source"]
            citations.append(f'<li id="{html.escape(did)}"><a href="{html.escape(src["authoritativeSourceURL"])}">{html.escape(atom["preferredTerm"])}</a>: “{html.escape(src["exactShortQuotation"])}” — {html.escape(src["sourceName"])}</li>')
    body = html.escape(raw).replace("\n", "<br>\n")
    output.write_text(f'<!doctype html><html><body><article>{body}</article><section class="definition-citations"><h2>Definition sources</h2><ol>{"".join(citations)}</ol></section></body></html>\n', encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("resolve"); sub.add_parser("validate")
    render_p = sub.add_parser("render"); render_p.add_argument("source", type=Path); render_p.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.command == "resolve": print(f"wrote {len(write_proposals())} proposals")
    elif args.command == "validate":
        errors = validate(); print("\n".join(errors) if errors else "definition registry valid")
        raise SystemExit(bool(errors))
    else: render(args.source, args.output)


if __name__ == "__main__": main()
