#!/usr/bin/env python3
"""Generate a cross-domain Master Equation topbar packet.

This adapter turns the cleaner Cross-Domain Coherence archive into a compact
topbar contract: every domain pill must say how C, S, G, and O are instantiated,
what evidence is claimed, and what would weaken or falsify the mapping.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import claim_runtime


REPO = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(
    r"C:\theophysics\_PRODUCTION_DEEP_SOURCE_ARCHIVE_2026-07-26"
    r"\Cross-Domain Coherence Project\00_CROSS_DOMAIN_ROADMAP.md"
)
DEFAULT_ARCHIVE_ROOT = DEFAULT_SOURCE.parent
DEFAULT_OUT = REPO / "cross-domain" / "11_articles" / "TOPBAR_FILL_PACKET.cross-domain.roadmap.json"
DEFAULT_REGISTRY = REPO / "_vocab" / "cross_domain_api_registry.json"
TOPBAR_PAGES = Path(r"D:\GitHub\Python-WEB\topbar\canonical-page-shell\pages")

TONES = ["gold", "teal", "blue", "purple", "orange", "red"]

DOMAIN_FALLBACKS = [
    {
        "code": "PSY",
        "label": "Psychological Entropy",
        "hardProblem": "Mental-health collapse, addiction, trauma, and recovery.",
        "C": "Psychological integration and durable mental health.",
        "S": "Trauma load, addiction severity, disorder, and fragmentation.",
        "G": "External negentropic input: community, grace, truth, and transcendent source.",
        "O": "Capacity for faith, surrender, reception, and metacognitive alignment.",
        "evidence": "Recovery dynamics, addiction research, trauma burden, 12-step/open-system recovery claims.",
    },
    {
        "code": "SEM",
        "label": "Semantic Entropy",
        "hardProblem": "Collapse of shared meaning, moral vocabulary, and civic language.",
        "C": "Shared meaning, moral clarity, linguistic precision, and stable thick concepts.",
        "S": "Ambiguity, semantic thinning, therapeutic drift, and subjective language inflation.",
        "G": "Objective truth, Logos-aligned language, virtue vocabulary, and moral grammar.",
        "O": "Cultural receptivity to enduring truths and collective attention to meaning.",
        "evidence": "Ngram trends, dictionary shifts, virtue-word decline, Semantic Coherence Index.",
    },
    {
        "code": "SOM",
        "label": "Somatic Entropy",
        "hardProblem": "Physiological degradation: metabolic, hormonal, reproductive, and mortality signals.",
        "C": "Physiological health, reproductive vitality, metabolic function, and embodied order.",
        "S": "Chronic disease, hormonal disruption, infertility, obesity, toxic exposure, and exhaustion.",
        "G": "Natural order, clean environment, whole-food nutrition, activity, rest, and biological design.",
        "O": "Individual and collective adherence to natural law and healthy practice.",
        "evidence": "Testosterone decline, sperm-count decline, obesity trends, NHANES and public-health markers.",
    },
    {
        "code": "EDU",
        "label": "Education Entropy",
        "hardProblem": "Transmission failure: knowledge decay, grade inflation, and civic illiteracy.",
        "C": "Knowledge acquisition, critical thinking, civic literacy, and generational transmission.",
        "S": "Grade inflation, declining objective scores, curricular fragmentation, and attention decay.",
        "G": "Objective standards, rigorous curriculum, truth-seeking, discipline, and foundational texts.",
        "O": "Student and social receptivity to learning, correction, and intellectual formation.",
        "evidence": "SAT, NAEP, grade inflation, civics surveys, and standards drift.",
    },
]

DOMAIN_HINTS = [
    {
        "code": "ECON",
        "label": "Economic / Monetary Entropy",
        "paths": ["01_Federal_Reserve", "Federal Reserve", "Economics", "Economic_Monetary"],
        "hardProblem": "Money, trust, debt, incentives, and paper claims detaching from real value.",
        "C": "Honest signal between money, labor, value, and time.",
        "S": "Inflation, debt abstraction, Cantillon distortion, bailout moral hazard, and phantom value.",
        "G": "Objective standards, honest weights, real collateral, covenantal trust, and productive exchange.",
        "O": "Institutional and public willingness to receive correction from reality rather than paper over it.",
    },
    {
        "code": "FAM",
        "label": "Family Structure Entropy",
        "paths": ["Family_Structure"],
        "hardProblem": "Marriage, fatherhood, fertility, and covenantal household stability.",
        "C": "Stable covenantal family bonds and intergenerational trust.",
        "S": "Divorce, fatherlessness, isolation, sexual fragmentation, and fertility collapse.",
        "G": "Covenant, sacrificial love, duty, chastity, forgiveness, and shared worship.",
        "O": "Personal and social willingness to submit desire to long-term covenantal goods.",
    },
    {
        "code": "TECH",
        "label": "Technological Entropy",
        "paths": ["Technology"],
        "hardProblem": "Digital systems maximizing attention, manipulation, and designed instability.",
        "C": "Durable attention, truth-contact, embodied relation, and human-scale agency.",
        "S": "Dopamine capture, distraction, algorithmic manipulation, unreality, and accelerated social decay.",
        "G": "Tool discipline, humane design, truthful mediation, Sabbath limits, and embodied community.",
        "O": "User and institution willingness to choose coherence over frictionless capture.",
    },
    {
        "code": "HIST",
        "label": "Historical Coherence Collapse",
        "paths": ["06_History_AW", "History", "The_Moral_Decay_of_America_Project"],
        "hardProblem": "The 1960-1980 American phase transition and the order of civilizational decay.",
        "C": "Shared moral order, institutional trust, family stability, and civic continuity over time.",
        "S": "Sequential collapse across semantic, familial, institutional, economic, and somatic domains.",
        "G": "Transcendent constraint, moral vocabulary, constitutional memory, and covenantal public order.",
        "O": "A society's willingness to preserve inherited order and repent when feedback turns negative.",
    },
    {
        "code": "SCI",
        "label": "Scientific Method Entropy",
        "paths": ["04_Scientific_Method", "Scientific method"],
        "hardProblem": "Science gaining precision while losing explanatory grounding and admissible why-questions.",
        "C": "Predictive power plus explanatory grounding, falsification, and honest boundary conditions.",
        "S": "Interpretive debris, method-only reduction, unfalsifiable prestige, and refusal of first causes.",
        "G": "Truth as an external standard, methodological humility, and falsifiable explanatory structure.",
        "O": "Research communities willing to ask forbidden questions and accept correction.",
    },
    {
        "code": "AI",
        "label": "AI Alignment Entropy",
        "paths": ["AI_Alignment", "14_AI_Synthesis_Final"],
        "hardProblem": "Agency, manipulation, survival incentives, and whether intelligence can remain coherence-seeking.",
        "C": "Truthful, non-exploitative alignment between agent action, human good, and reality.",
        "S": "Reward hacking, short-term optimization, manipulation, opacity, and runaway agency.",
        "G": "Coherence constraints, humility, truth-telling, fruit audit, and moral boundary conditions.",
        "O": "Agent and developer receptivity to constraints that reduce power but preserve goodness.",
    },
    {
        "code": "COS",
        "label": "Cosmological Coherence",
        "paths": ["Cosmology"],
        "hardProblem": "Dark energy, Hubble tension, cosmic order, and open-system source structure.",
        "C": "Large-scale intelligible order and stable cosmic structure.",
        "S": "Expansion pressure, heat-death drift, model tension, and unexplained initial order.",
        "G": "External source term, boundary condition, grace dynamics, and sustaining order.",
        "O": "Observer-aware cosmology willing to test source-structured models.",
    },
    {
        "code": "THEO",
        "label": "Theological Engineering",
        "paths": ["05_Theological_Engineering", "Theological_Engineering", "Religion"],
        "hardProblem": "Turning doctrine into falsifiable structure without reducing God to machinery.",
        "C": "Doctrinal coherence, lived fruit, and faithful mapping between theology and reality.",
        "S": "Category error, metaphor inflation, dead formalism, and spiritual abstraction without fruit.",
        "G": "Revelation, grace, Scripture, sacrament, and the Logos as external anchor.",
        "O": "Faithful reception, repentance, and willingness to let doctrine judge the system.",
    },
    {
        "code": "TRIN",
        "label": "Trinity Coherence",
        "paths": ["10_Trinity"],
        "hardProblem": "Unity and distinction without collapse into contradiction or modal flattening.",
        "C": "Three-person relational closure with one coherent divine essence.",
        "S": "Contradiction, collapse of distinction, tritheism, modalism, and semantic drift.",
        "G": "Revelation and Logos-grounded relational ontology.",
        "O": "Reader willingness to test paradox by structure rather than slogan.",
    },
    {
        "code": "ARCH",
        "label": "Architecture / Built Coherence",
        "paths": ["13_Architecture"],
        "hardProblem": "Whether built environments encode order, hierarchy, beauty, and human-scale meaning.",
        "C": "Embodied intelligibility, proportion, durability, human scale, and sacred orientation.",
        "S": "Placelessness, fragmentation, cheapness, anti-human scale, and aesthetic noise.",
        "G": "Pattern language, beauty, craft, symbolic order, and truthful material limits.",
        "O": "Communities willing to build for meaning rather than extraction.",
    },
    {
        "code": "DEM",
        "label": "Demographic Entropy",
        "paths": ["12_Demographics"],
        "hardProblem": "Fertility, age structure, continuity, and whether a society wants a future.",
        "C": "Generational continuity, replacement, family formation, and future-oriented sacrifice.",
        "S": "Sub-replacement fertility, aging, despair, isolation, and delayed family formation.",
        "G": "Hope, covenantal family meaning, child-welcoming norms, and future trust.",
        "O": "Cultural willingness to receive life as gift and responsibility.",
    },
    {
        "code": "INST",
        "label": "Institutional Trust Entropy",
        "paths": ["Institutional_Trust"],
        "hardProblem": "Public trust, legitimacy, corruption, and institutional signal decay.",
        "C": "Trustworthy institutions aligned with truth, duty, competence, and public good.",
        "S": "Corruption, cynicism, credential inflation, legitimacy collapse, and narrative capture.",
        "G": "Accountability, objective standards, public virtue, and transparent correction.",
        "O": "Institutional willingness to be judged by truth instead of self-preservation.",
    },
]

EXCLUDED_SCAN_PARTS = {
    ".git",
    ".venv",
    ".venv-convert",
    "__pycache__",
    "venv",
    "node_modules",
    "assets",
    "Archive",
    "A3_ARCHIVE",
    "_DESKTOP_MIGRATION_ARCHIVE",
    "_Incoming_Sorting",
    "_NON_CANONICAL_REVIEW",
}

SCAN_PATTERNS = [
    r"\bmaster equation\b",
    r"\bdc/dt\b",
    r"\bdC/dt\b",
    r"\bcoherence\b",
    r"\bentropy\b",
    r"\bfalsif",
    r"\bkill condition\b",
    r"\bphase transition\b",
    r"\bcontrol group\b",
    r"\bgrace\b",
    r"\blogos\b",
]


def fix_mojibake(text: str) -> str:
    try:
        fixed = text.encode("cp1252").decode("utf-8")
    except UnicodeError:
        return text
    return fixed if fixed.count("\ufffd") <= text.count("\ufffd") else text


def normalize_space(text: str) -> str:
    return claim_runtime.normalize_space(text)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", value.upper()).strip("-")


def parse_domain_sections(raw: str) -> list[dict[str, str]]:
    domains: dict[str, dict[str, str]] = {item["code"]: dict(item) for item in DOMAIN_FALLBACKS}
    section_re = re.compile(
        r"###\s+2\.\d+\s+(?P<title>[^\n]+)\n(?P<body>.*?)(?=\n###\s+2\.|\n---|\n##\s+3\.)",
        re.S,
    )
    variable_re = re.compile(r"\*\s+\*\*(?P<key>[CSGO])\s*\([^)]*\):\*\*\s*(?P<value>[^\n]+)")
    evidence_re = re.compile(r"\*\s+\*\*Evidence:\*\*\s*(?P<value>[^\n]+)", re.I)
    for match in section_re.finditer(raw):
        title = normalize_space(match.group("title"))
        body = match.group("body")
        code_match = re.search(r"\(([A-Z]{3})\)", title)
        code = code_match.group(1) if code_match else ""
        if code not in domains:
            continue
        domains[code]["label"] = re.sub(r"\s*-\s*\(.*?\)\s*$", "", re.sub(r"\s*\([A-Z]{3}\)", "", title)).strip()
        for var in variable_re.finditer(body):
            domains[code][var.group("key")] = normalize_space(var.group("value"))
        evidence = evidence_re.search(body)
        if evidence:
            domains[code]["evidence"] = normalize_space(evidence.group("value"))
    return [domains[item["code"]] for item in DOMAIN_FALLBACKS]


def archive_root_for(source: Path) -> Path:
    return source.parent if source.is_file() else source


def should_scan(path: Path, root: Path) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        rel_parts = path.parts
    return not any(part in EXCLUDED_SCAN_PARTS for part in rel_parts)


def markdown_files(paths: list[Path], root: Path) -> list[Path]:
    found: list[Path] = []
    for path in paths:
        if not path.exists() or not should_scan(path, root):
            continue
        if path.is_file() and path.suffix.lower() == ".md":
            found.append(path)
        elif path.is_dir():
            for item in path.rglob("*.md"):
                if should_scan(item, root):
                    found.append(item)
    return sorted(set(found))


def hit_count(text: str) -> int:
    return sum(len(re.findall(pattern, text, flags=re.I)) for pattern in SCAN_PATTERNS)


def best_sentence(text: str) -> str:
    sentences = claim_runtime.extract_claim_sentences(text, limit=20)
    if not sentences:
        return "Archive scan found framework vocabulary, but the evidence summary still needs human review."
    scored = sorted(
        ((hit_count(sentence), sentence) for sentence in sentences),
        key=lambda item: (-item[0], len(item[1])),
    )
    return scored[0][1]


def scan_hint(root: Path, hint: dict[str, Any]) -> dict[str, Any] | None:
    paths = [root / rel for rel in hint["paths"]]
    files = markdown_files(paths, root)
    scored_files = []
    total_hits = 0
    for path in files[:120]:
        try:
            text = fix_mojibake(path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        sample = text[:160000]
        score = hit_count(sample)
        if score <= 0:
            continue
        total_hits += score
        scored_files.append((score, path, sample))
    if total_hits < 8 or not scored_files:
        return None
    scored_files.sort(key=lambda item: (-item[0], str(item[1])))
    best = scored_files[0]
    item = {
        "code": hint["code"],
        "label": hint["label"],
        "hardProblem": hint["hardProblem"],
        "C": hint["C"],
        "S": hint["S"],
        "G": hint["G"],
        "O": hint["O"],
        "evidence": best_sentence(best[2]),
        "hitCount": total_hits,
        "sourceFiles": [str(path.relative_to(root)) for _, path, _ in scored_files[:3]],
        "grade": "candidate structural application",
    }
    return item


def discover_scanned_domains(source: Path, existing_codes: set[str], max_domains: int) -> list[dict[str, Any]]:
    root = archive_root_for(source)
    candidates = []
    for hint in DOMAIN_HINTS:
        if hint["code"] in existing_codes:
            continue
        item = scan_hint(root, hint)
        if item:
            candidates.append(item)
    candidates.sort(key=lambda item: (-int(item.get("hitCount", 0)), item["code"]))
    return candidates[:max_domains]


def term_for_domain(item: dict[str, str], idx: int) -> dict[str, Any]:
    projection = "dC/dt = O*G*(1-C) - S*C"
    source_files = item.get("sourceFiles", [])
    source_value = ", ".join(source_files[:2]) if isinstance(source_files, list) and source_files else "00_CROSS_DOMAIN_ROADMAP.md"
    grade = item.get("grade", "structural application")
    return {
        "id": f"domain-{item['code'].lower()}",
        "label": item["code"],
        "tone": TONES[idx % len(TONES)],
        "front": {
            "eyebrow": "Cross-domain projection",
            "subtitle": item["label"],
            "equation": projection,
            "summary": f"{item['label']} is treated as structurally relevant when its collapse and restoration can be named through C, S, G, and O without changing the equation's logic.",
            "rows": [
                {"label": "Hard problem", "value": item["hardProblem"]},
                {"label": "C", "value": item["C"]},
                {"label": "S", "value": item["S"]},
                {"label": "G", "value": item["G"]},
                {"label": "O", "value": item["O"]},
                {"label": "Hits", "value": str(item.get("hitCount", "roadmap"))},
            ],
        },
        "back": {
            "eyebrow": "Relevance contract",
            "rows": [
                {"label": "Evidence", "value": item["evidence"]},
                {"label": "Grade", "value": str(grade)},
                {"label": "Source", "value": source_value},
                {"label": "Boundary", "value": "This supports Master Equation relevance; it is not a proof that every claim in the domain is already verified."},
                {"label": "Kill condition", "value": "The pill weakens if C/S/G/O are arbitrary, non-measurable, or fail to organize the domain evidence better than rival variables."},
            ],
        },
        "proofUrl": "",
    }


def build_claims(domains: list[dict[str, str]], source: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    indexed = claim_runtime.atom_index(claim_runtime.load_atoms())
    base_claims = [
        "A cross-domain application is Master Equation relevant only when it declares what counts as coherence, entropy load, external coherence input, and receptive capacity in that domain.",
        "The older open-system equation functions as a reduced projection of the Master Equation, not as a replacement for the richer canonical atom graph.",
        "A domain bridge strengthens when the same coherence-collapse and recovery structure organizes independent evidence without changing the definitions after seeing the result.",
        "The 1968-1973 phase-transition window is a cross-domain hypothesis that must survive domain holdouts and timeline checks.",
        "The Amish/control-group claim is useful only where the comparison names protected coherence inputs and checks rival explanations.",
    ]
    for item in domains:
        base_claims.append(
            f"{item['label']} instantiates the open-system coherence variables as C: {item['C']} S: {item['S']} G: {item['G']} O: {item['O']}"
        )

    claims = []
    proofs = []
    for idx, sentence in enumerate(base_claims, start=1):
        claim_id = f"CDC-C{idx:03d}"
        proof_id = f"CDC-P{idx:03d}"
        classification = claim_runtime.classify(sentence, indexed)
        best = classification["matches"][0] if classification["matches"] else {}
        status = "partial" if classification["verdict"] in {"likely-existing-atom", "needs-review"} else "draft"
        claims.append(
            {
                "id": claim_id,
                "sentence": sentence,
                "formal": sentence,
                "status": status,
                "derivation": [
                    f"Generated from cross-domain adapter source: {source.name}.",
                    f"Runtime atom alignment: {classification['verdict']}; best match: {best.get('nodeID', 'none')}.",
                ],
                "killCondition": "Show the domain mapping changes definitions opportunistically, cannot be measured, or fails against a named rival model.",
                "proofIds": [proof_id],
            }
        )
        proofs.append(
            {
                "id": proof_id,
                "title": str(best.get("name") or "Cross-domain roadmap source"),
                "status": status,
                "summary": f"Local adapter claim grounded in {source}. Best atom match: {best.get('nodeID', 'none')}.",
                "claimIds": [claim_id],
                "url": "",
            }
        )
    return claims, proofs


def claim_span(claim: dict[str, Any]) -> str:
    return (
        f'<span class="ftp-claim-sentence" data-claim-id="{html.escape(str(claim["id"]))}">'
        f'{html.escape(str(claim["sentence"]))}</span>'
    )


def build_mtl(domains: list[dict[str, str]]) -> list[dict[str, Any]]:
    items = [
        {
            "id": "CDC-MTL-001",
            "format": "box",
            "title": "Legacy Open-System Coherence Equation",
            "equation": "dC/dt = O*G*(1-C) - S*C",
            "wordEquation": "Change in coherence equals receptive capacity times external coherence input times remaining repair capacity, minus entropy load times present coherence.",
            "structuralInsight": "This is the older cross-domain rail. It should be treated as a reduced/open-system projection that lets domains speak to the newer Master Equation atom graph.",
            "plain": "Every domain must say what counts as C, S, G, and O before it borrows the equation.",
            "influence": "Strengthens when variables are measurable before the conclusion; weakens when the mapping is metaphor-only or retrospectively adjusted.",
        },
        {
            "id": "CDC-MTL-002",
            "format": "box",
            "title": "Projection Into Current Master Equation Work",
            "equation": "Domain(C,S,G,O) -> ME factors + fruit audit + failure propagation",
            "wordEquation": "A domain claim enters the current system by mapping its coherence terms, auditing its fruit, and tracking dependency failures.",
            "structuralInsight": "The cross-domain archive does not need a separate API family; it needs an adapter that translates old domain variables into the shared runtime contract.",
            "plain": "Same engine, different doorway.",
            "influence": "Strengthens when a domain has evidence, named variables, kill conditions, and downstream claims that can be weakened if the bridge fails.",
        },
    ]
    for idx, item in enumerate(domains, start=3):
        items.append(
            {
                "id": f"CDC-MTL-{idx:03d}",
                "format": "box",
                "title": f"{item['code']} Variable Instantiation",
                "equation": f"{item['code']}: C={item['C']}; S={item['S']}; G={item['G']}; O={item['O']}",
                "wordEquation": f"{item['label']} applies the open-system rail by naming its coherence state, entropy pressure, external coherence input, and receptive capacity.",
                "structuralInsight": "This makes the domain pill inspectable instead of leaving the Master Equation reference hidden in prose.",
                "plain": f"{item['label']} is admitted as a structural application only as far as this mapping holds.",
                "influence": "Use evidence and falsification rows on the domain pill before promoting claims to verified.",
            }
        )
    return items


def build_reader_layers(domains: list[dict[str, str]], claims: list[dict[str, Any]]) -> dict[str, str]:
    domain_items = "".join(
        f"<li><b>{html.escape(item['code'])}</b>: {html.escape(item['label'])} maps C/S/G/O to a named hard problem.</li>"
        for item in domains
    )
    claim_items = "".join(f"<li>{claim_span(claim)}</li>" for claim in claims)
    first = claims[0]
    second = claims[1]
    return {
        "highschool": (
            "<h2>The Idea, Simply</h2>"
            "<p>The cross-domain project works when every new field has to open the same pill: what is coherence here, what is entropy here, what brings repair from outside, and what receives it?</p>"
            f"<p>{claim_span(first)}</p>"
            f"<ul>{domain_items}</ul>"
        ),
        "college": (
            "<h2>The Bridge</h2>"
            "<p>The archive uses the older open-system equation as a disciplined bridge into the current Master Equation runtime.</p>"
            f"<p>{claim_span(first)}</p>"
            f"<p>{claim_span(second)}</p>"
            "<p>The important move is not bragging that every field is solved. The important move is making every field pay the same structural toll before the framework claims relevance.</p>"
            f"<ul>{claim_items}</ul>"
        ),
        "phd": (
            "<h2>The Formal Contract</h2>"
            "<p>A cross-domain bridge is admissible when variable assignment, evidence scope, phase-transition timing, control-group logic, and failure propagation are explicit before reader persuasion begins.</p>"
            f"<p>{claim_span(first)}</p>"
            f"<p>{claim_span(second)}</p>"
            "<p>The generated packet treats dC/dt as a legacy projection and routes it into the current atom graph through claim classification, MTL entries, and review-grade proof handles.</p>"
        ),
    }


def build_verification(domains: list[dict[str, str]], claims: list[dict[str, Any]], source: Path) -> list[dict[str, Any]]:
    counts = Counter(claim["status"] for claim in claims)
    scanned = sum(1 for item in domains if item.get("grade") == "candidate structural application")
    return [
        {
            "title": "Source",
            "rows": [
                ["Archive", str(source.parent)],
                ["Roadmap", source.name],
                ["Domains", str(len(domains))],
                ["Scanned candidates", str(scanned)],
                ["Adapter", "_scripts/cross_domain_pill_adapter.py"],
            ],
        },
        {
            "title": "Master Equation Relevance",
            "rows": [
                ["Required", "C/S/G/O declared"],
                ["Equation", "dC/dt = O*G*(1-C) - S*C"],
                ["Status", "legacy projection"],
                ["Current route", "atom graph + MTL + fruit audit"],
            ],
        },
        {
            "title": "Claims",
            "rows": [
                ["Total", str(len(claims))],
                ["Partial", str(counts["partial"])],
                ["Draft", str(counts["draft"])],
                ["Verified", str(counts["verified"])],
            ],
        },
        {
            "title": "Gate",
            "rows": [
                ["Evidence", "must be domain-specific"],
                ["Rival model", "must be named"],
                ["Kill condition", "required"],
                ["Promotion", "human review after local/API audit"],
            ],
        },
    ]


def build_registry(packet_path: Path, domains: list[dict[str, str]], source: Path) -> dict[str, Any]:
    return {
        "registryID": "cross-domain-api-registry",
        "source": str(source),
        "packet": str(packet_path),
        "calls": [
            {
                "name": "CrossDomain.intake",
                "status": "implemented",
                "script": "_scripts/cross_domain_pill_adapter.py",
                "returns": "canonical topbar fill packet with roadmap and hit-scanned domain pills",
            },
            {
                "name": "Domain.scanHits",
                "status": "implemented",
                "contract": ["Master Equation hits", "coherence hits", "entropy hits", "falsification hits"],
            },
            {
                "name": "Domain.instantiate",
                "status": "implemented",
                "contract": ["C", "S", "G", "O", "evidence", "killCondition"],
            },
            {
                "name": "LegacyEquation.translate",
                "status": "implemented",
                "from": "dC/dt = O*G*(1-C) - S*C",
                "to": "Master Equation atom graph, MTL, claim runtime, fruit audit",
            },
            {
                "name": "CrossDomain.promote",
                "status": "planned",
                "requires": "API or human review of evidence, rival models, and live claim dependencies",
            },
        ],
        "domains": domains,
    }


def build_packet(source: Path, out: Path, registry_out: Path, copy_to_topbar: bool, scan: bool, max_scanned: int) -> dict[str, Any]:
    raw = fix_mojibake(source.read_text(encoding="utf-8", errors="replace"))
    domains = parse_domain_sections(raw)
    if scan:
        domains.extend(discover_scanned_domains(source, {item["code"] for item in domains}, max_scanned))
    terms = [term_for_domain(item, idx) for idx, item in enumerate(domains)]
    claims, proofs = build_claims(domains, source)
    mtl = build_mtl(domains)
    packet = {
        "page": {
            "id": "CDC-ROADMAP-001",
            "title": "Cross-Domain Coherence Roadmap",
            "series": "Cross-Domain Coherence",
            "subtitle": "A generated topbar packet showing how each domain earns Master Equation relevance.",
            "kicker": "Cross-Domain / Master Equation Adapter",
            "byline": "David Lowe - Faith Through Physics - July 2026",
            "sourceArchive": str(source.parent),
            "prev": {"label": "", "url": ""},
            "next": {"label": "", "url": ""},
        },
        "terms": terms,
        "claims": claims,
        "proofs": proofs,
        "mtl": mtl,
        "verification": build_verification(domains, claims, source),
        "audio": [
            {"id": "read", "label": "Read Aloud", "url": ""},
            {"id": "debate", "label": "Debate", "url": ""},
            {"id": "deep", "label": "Deep Dive", "url": ""},
            {"id": "critique", "label": "Critique", "url": ""},
        ],
        "audit": {
            "right": [
                "The cross-domain project should use the same local runtime APIs as the Master Equation, with a domain adapter in front.",
                "The domain pills now expose C/S/G/O mappings, evidence status, and kill conditions instead of hiding the bridge in prose.",
                "Archive folders with enough framework hits are admitted as candidate pills and tied back to the Master Equation runtime.",
            ],
            "overstated": [
                "The packet marks cross-domain claims as structural applications, not final proofs.",
                "The legacy open-system equation needs compatibility language when presented beside the newer Master Equation atoms.",
                "Auto-scanned candidate domains are triage handles; their evidence rows are not yet final literature reviews.",
            ],
            "wrong": [
                "Do not promote a domain to verified unless its variable mapping, evidence, rival model, and failure conditions survive review.",
            ],
        },
        "reader_layers": build_reader_layers(domains, claims),
    }
    write_json(out, packet)
    registry = build_registry(out, domains, source)
    write_json(registry_out, registry)
    if copy_to_topbar:
        TOPBAR_PAGES.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, TOPBAR_PAGES / out.name)
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a cross-domain Master Equation topbar packet.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--registry-out", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--no-copy", action="store_true", help="Do not copy the packet into the topbar shell pages directory.")
    parser.add_argument("--roadmap-only", action="store_true", help="Only emit the four roadmap domains.")
    parser.add_argument("--max-scanned", type=int, default=12, help="Maximum scanned candidate domains to add as pills.")
    args = parser.parse_args()

    packet = build_packet(args.source, args.out, args.registry_out, not args.no_copy, not args.roadmap_only, args.max_scanned)
    print(f"[ok] wrote {args.out}")
    print(f"[ok] wrote {args.registry_out}")
    print(f"[ok] terms={len(packet['terms'])} claims={len(packet['claims'])} proofs={len(packet['proofs'])} mtl={len(packet['mtl'])}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
