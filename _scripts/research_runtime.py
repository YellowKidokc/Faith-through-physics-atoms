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
ANCHOR_DIR = RUNTIME / "anchor_lines"

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
    ("Text.anchor_lines", "implemented", "_scripts/research_runtime.py anchor"),
    ("Text.anchor_folder", "implemented", "_scripts/research_runtime.py anchor-folder"),
    ("Text.anchor_prompt", "implemented", "_scripts/research_runtime.py anchor --include-prompt"),
]

ANCHOR_MARKERS = {
    "mechanism": (
        "because", "therefore", "requires", "depends", "costs", "pays", "absorbs",
        "transfers", "closes", "opens", "holds", "carries", "repairs", "decays",
        "source", "signal", "ledger", "floor", "inside", "outside", "channel",
        "coherence", "entropy", "grace", "choice", "damage", "receiver",
    ),
    "punch": (
        "not", "never", "cannot", "can't", "isn't", "doesn't", "only", "whole",
        "everything", "nothing", "always", "forever", "inside", "outside",
    ),
}


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


def anchor_source_text(path: Path) -> str:
    text, _packet = claim_runtime.load_source(path)
    text = re.split(r"\n\s*## \[DRAWER REGISTER\b|\n\s*## WORLDVIEW SESSION\b", text, maxsplit=1)[0]
    kept = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            continue
        if stripped.startswith("*Failures this chapter:"):
            continue
        kept.append(line)
    return normalize(claim_runtime.strip_html("\n".join(kept)))


def sentences(text: str) -> list[str]:
    cleaned = normalize(claim_runtime.strip_html(text))
    pieces = re.split(r"(?<=[.!?])\s+", cleaned)
    result = []
    for piece in pieces:
        sentence = normalize(piece.strip(" -\t\r\n"))
        if not 20 <= len(sentence) <= 320:
            continue
        if sentence.startswith(">") or sentence.startswith("**"):
            continue
        if re.match(r"^(Simulation|Physics|Math|Story function|Theophysics bridge|Theology|Claim strength|Kill condition|Reader takeaway):", sentence):
            continue
        result.append(sentence)
    return result


def section_blocks(text: str) -> list[dict[str, str]]:
    lines = claim_runtime.strip_html(text).splitlines()
    blocks: list[dict[str, str]] = []
    title = "Document"
    buffer: list[str] = []
    for line in lines:
        heading = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if heading:
            if normalize("\n".join(buffer)):
                blocks.append({"title": title, "text": "\n".join(buffer)})
            title = heading.group(2).strip()
            buffer = []
        else:
            buffer.append(line)
    if normalize("\n".join(buffer)):
        blocks.append({"title": title, "text": "\n".join(buffer)})
    if not blocks:
        blocks.append({"title": "Document", "text": text})
    return blocks


def sentence_score(sentence: str) -> float:
    low = sentence.lower()
    score = 0.0
    length = len(sentence)
    if 55 <= length <= 180:
        score += 2.0
    elif 35 <= length <= 230:
        score += 1.0
    score += 0.45 * len(contains_any(low, ANCHOR_MARKERS["mechanism"]))
    score += 0.35 * len(contains_any(low, ANCHOR_MARKERS["punch"]))
    if re.search(r"\bnot\b.+\bbut\b|\bnot\b.+\bbecause\b|\bcannot\b.+\bwithout\b", low):
        score += 2.0
    if re.search(r"\b(the|a) (ledger|signal|floor|chain|source|crowd|equation|receiver|template)\b", low):
        score += 1.2
    if re.search(r"^the (first|second|third) said that\b", low):
        score -= 1.5
    if re.search(r"\" \"", sentence):
        score -= 1.0
    if sentence.endswith("?"):
        score -= 0.6
    if "," in sentence and length > 210:
        score -= 0.8
    return score


def strongest_sentence(text: str) -> str:
    candidates = sentences(text)
    if not candidates:
        return ""
    return max(candidates, key=sentence_score)


def mechanism_plain(text: str) -> str:
    candidate_sentences = sentences(text)
    if not candidate_sentences:
        return ""
    scored = sorted(candidate_sentences, key=sentence_score, reverse=True)[:5]
    mechanism = scored[0]
    if len(mechanism) > 220:
        mechanism = mechanism[:217].rstrip(",;: ") + "..."
    return mechanism


def clean_anchor(sentence: str) -> str:
    anchor = normalize(sentence)
    anchor = re.sub(r"^(And|But|So|Then|Because)\s+", "", anchor, flags=re.I)
    anchor = re.sub(r"^The (first|second|third) said that\s+", "", anchor, flags=re.I)
    anchor = re.sub(r"^VESSEL:\s*", "", anchor, flags=re.I)
    anchor = re.sub(r"\s*[-–—]\s*", " - ", anchor)
    if len(anchor) > 185:
        parts = re.split(r";|, and |, but | because ", anchor, maxsplit=1, flags=re.I)
        if parts and 35 <= len(parts[0]) <= 185:
            anchor = parts[0]
    return anchor.rstrip(".") + "."


def anchor_alternates(anchor: str) -> dict[str, str]:
    base = clean_anchor(anchor)
    low = base.lower()
    plain = base
    poetic = base
    brutal = base
    if "inside" in low and "outside" in low:
        poetic = "What cannot close from inside must be crossed from outside."
        brutal = "Inside cannot pay an outside-sized bill."
    elif "ledger" in low or "debt" in low or "paid" in low or "bill" in low:
        poetic = "Mercy does not erase the ledger; it finds the payer."
        brutal = "Unpaid forgiveness is just hidden debt."
    elif "signal" in low or "receiver" in low or "channel" in low or "pipe" in low:
        poetic = "The signal can be perfect and still arrive bent."
        brutal = "A clean signal cannot save a closed receiver."
    elif "floor" in low or "substrate" in low or "source" in low:
        poetic = "The floor holds because the source keeps arriving."
        brutal = "The floor is not self-sustaining."
    elif "choice" in low or "choose" in low:
        poetic = "A free choice becomes real by leaving a mark."
        brutal = "You cannot un-choose."
    elif "breaking" in low or "building" in low or "decay" in low:
        poetic = "Building has to pay every cycle; decay only has to wait."
        brutal = "Breaking is cheaper than building."
    return {"plain": plain, "poetic": poetic, "brutal": brutal}


def anchor_prompt(section_title: str, text: str) -> str:
    excerpt = normalize(claim_runtime.strip_html(text))
    if len(excerpt) > 4500:
        excerpt = excerpt[:4500].rstrip() + "..."
    return f"""You are doing a literary compression pass for a Theophysics chapter or section.

Input section title: {section_title}

Task:
1. Identify the load-bearing mechanism in plain English.
2. Find the strongest sentence already present.
3. Write one better anchor sentence only if the existing sentence is not already stronger.
4. Provide three alternates: plain, poetic, brutal.
5. Recommend keep existing / replace with new / add near ending.

Rules:
- Do not summarize blandly.
- Preserve the mechanism.
- Keep the sentence quotable from memory.
- Do not make it generic inspirational language.
- Do not overclaim beyond the section.
- The result should feel like the sentence the section was trying to earn.

Section:
{excerpt}
"""


def compress_section(title: str, text: str, include_prompt: bool = False) -> dict[str, Any]:
    strongest = strongest_sentence(text)
    mechanism = mechanism_plain(text)
    anchor = clean_anchor(strongest or mechanism)
    alternates = anchor_alternates(anchor)
    recommendation = "keep existing"
    if strongest and alternates["brutal"] != anchor and sentence_score(alternates["brutal"]) >= sentence_score(strongest):
        recommendation = "add near ending"
    result: dict[str, Any] = {
        "sectionTitle": title,
        "loadBearingMechanism": mechanism,
        "strongestSentenceAlreadyPresent": strongest,
        "recommendedAnchorSentence": anchor,
        "alternates": alternates,
        "recommendation": recommendation,
    }
    if include_prompt:
        result["modelPrompt"] = anchor_prompt(title, text)
    return result


def anchor_report(path: Path, include_prompt: bool = False, max_sections: int = 80) -> dict[str, Any]:
    text = anchor_source_text(path)
    blocks = section_blocks(text)[:max_sections]
    sections = [compress_section(block["title"], block["text"], include_prompt=include_prompt) for block in blocks]
    doc_anchor = compress_section(path.stem, text, include_prompt=False)
    output = {
        "runtime": "theophysics-research-runtime",
        "api": "Text.anchor_lines",
        "version": "0.1.0",
        "generatedAt": now(),
        "source": str(path),
        "documentAnchor": doc_anchor,
        "sections": sections,
    }
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", path.stem).strip("-").lower() or "source"
    out_json = ANCHOR_DIR / f"{slug}.anchors.json"
    out_md = ANCHOR_DIR / f"{slug}.anchors.md"
    claim_runtime.write_text(out_json, json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    claim_runtime.write_text(out_md, anchor_markdown(output))
    output["_jsonPath"] = str(out_json)
    output["_markdownPath"] = str(out_md)
    return output


def anchor_markdown(output: dict[str, Any]) -> str:
    lines = [
        f"# Anchor Lines - {Path(output['source']).name}",
        "",
        f"Generated: {output['generatedAt']}",
        "",
        "## Document Anchor",
        "",
        output["documentAnchor"]["recommendedAnchorSentence"],
        "",
        "## Sections",
        "",
    ]
    for section in output["sections"]:
        lines += [
            f"### {section['sectionTitle']}",
            "",
            f"- Mechanism: {section['loadBearingMechanism']}",
            f"- Existing: {section['strongestSentenceAlreadyPresent']}",
            f"- Anchor: {section['recommendedAnchorSentence']}",
            f"- Plain: {section['alternates']['plain']}",
            f"- Poetic: {section['alternates']['poetic']}",
            f"- Brutal: {section['alternates']['brutal']}",
            f"- Recommendation: {section['recommendation']}",
            "",
        ]
    return "\n".join(lines)


def anchor_folder(folder: Path, pattern: str = "*.md", include_prompt: bool = False, limit: int = 200) -> dict[str, Any]:
    files = sorted(path for path in folder.glob(pattern) if path.is_file())[:limit]
    reports = [anchor_report(path, include_prompt=include_prompt) for path in files]
    index = {
        "runtime": "theophysics-research-runtime",
        "api": "Text.anchor_folder",
        "generatedAt": now(),
        "folder": str(folder),
        "pattern": pattern,
        "count": len(reports),
        "reports": [
            {
                "source": report["source"],
                "json": report["_jsonPath"],
                "markdown": report["_markdownPath"],
                "documentAnchor": report["documentAnchor"]["recommendedAnchorSentence"],
            }
            for report in reports
        ],
    }
    out = ANCHOR_DIR / "anchor_index.json"
    claim_runtime.write_text(out, json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    index["_path"] = str(out)
    return index


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

    p_anchor = sub.add_parser("anchor", help="Build anchor-line compression report for a source file.")
    p_anchor.add_argument("source", type=Path)
    p_anchor.add_argument("--include-prompt", action="store_true", help="Include model-call prompt payloads in JSON output.")
    p_anchor.add_argument("--max-sections", type=int, default=80)

    p_anchor_folder = sub.add_parser("anchor-folder", help="Build anchor-line reports for every matching file in a folder.")
    p_anchor_folder.add_argument("folder", type=Path)
    p_anchor_folder.add_argument("--pattern", default="*.md")
    p_anchor_folder.add_argument("--include-prompt", action="store_true", help="Include model-call prompt payloads in JSON output.")
    p_anchor_folder.add_argument("--limit", type=int, default=200)

    p_failure = sub.add_parser("failure", help="Show blast radius for a claim/node id.")
    p_failure.add_argument("claim_id")

    sub.add_parser("registry", help="Write runtime API registry.")

    args = parser.parse_args()
    if args.command == "manifest":
        result = manifest(args.source, limit=args.limit)
        print(f"[ok] manifest={result['_path']}")
        print(f"[ok] claims={len(result['claimIDs'])} lowest={result['survivalVector']['lowestCoordinate']}")
        return 0
    if args.command == "anchor":
        result = anchor_report(args.source, include_prompt=args.include_prompt, max_sections=args.max_sections)
        print(f"[ok] json={result['_jsonPath']}")
        print(f"[ok] markdown={result['_markdownPath']}")
        print(f"[ok] sections={len(result['sections'])}")
        return 0
    if args.command == "anchor-folder":
        result = anchor_folder(args.folder, pattern=args.pattern, include_prompt=args.include_prompt, limit=args.limit)
        print(f"[ok] index={result['_path']}")
        print(f"[ok] reports={result['count']}")
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
