#!/usr/bin/env python3
"""Demo batch: create source-pinned capsules, run claim pipeline, write projections.

Preserves all source files. Outputs are marked CANDIDATE_DRAFT — NOT ADMITTED.
No admission events. No active pointers. No source mutation.

This version automatically extracts source_governance from each source file's
YAML frontmatter and canonical sections so that mode, status, dependencies,
defeat conditions, limitations, and bridge limits travel with the capsule.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Windows consoles default to cp1252; force UTF-8 so source text with diacritics prints cleanly.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

PIPELINE_SCRIPT = Path(__file__).resolve().parent / "claim_pipeline_service.py"
VAULT = Path(r"Z:\__New\Theophysics.new")
SOURCE_DIR = VAULT / "___AXIOM" / "06_AXIOM_CHAIN" / "___CANONICAL" / "SEQUENTIAL_PRE_v2.3_BACKUP"
OUTPUT_ROOT = VAULT / "__CANDIDATE_DRAFTS_NOT_ADMITTED" / f"batch_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
DEFAULT_PROVIDER = "deepseek"
DEFAULT_MODEL = "deepseek-chat"

# Minimal source inventory.  Per-source overrides are supported; anything not
# overridden is extracted automatically from the source note.
SOURCES = [
    {
        "id": "0001_A1.1_A1_1_Existence",
        "filename": "0001_A1_1_Existence.md",
        "claim_type": "philosophical",
        "operation": "new_claim",
        "line_start": 45,
        "line_end": 47,
        "heading": "Statement",
    },
    {
        "id": "0004_A2.2_A2_2_Self_Grounding",
        "filename": "0004_A2.2_A2_2_Self-Grounding.md",
        "claim_type": "philosophical",
        "operation": "new_claim",
        "line_start": 45,
        "line_end": 47,
        "heading": "Statement",
        "decomposition_guidance": "The second clause states the proposed boundary of the same self-grounding stance. Keep it with the stance unless a distinct truth condition is identified.",
    },
    {
        "id": "0010_BC2_BC2_Grace_External_To_System",
        "filename": "0010_BC2_BC2_Grace_External_To_System.md",
        "claim_type": "theological",
        "operation": "new_claim",
        "line_start": 45,
        "line_end": 47,
        "heading": "Statement",
        "discovery_incomplete_reason": "The pinned source sentence bundles theological identification, a conditional boundary statement, and a proposed bridge. Split before classification.",
    },
]


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def digest_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_frontmatter(text: str) -> dict:
    """Parse the first YAML-ish --- block found anywhere in the source note."""
    match = re.search(r"---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        result[key] = value
    return result


def extract_section(text: str, heading: str) -> str | None:
    """Return the body under a `## Heading` until the next `## `, `---`, semantic tag block, or end of file."""
    pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)\n*(?=\n##\s+|\n---\s*\n|\n%%---|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None


def parse_list_section(text: str | None) -> list[str]:
    """Parse a `- item` list, falling back to one item per non-empty line."""
    if not text:
        return []
    items = [line.strip().lstrip("- ").strip() for line in text.splitlines() if line.strip().startswith("- ")]
    if items:
        return items
    return [line.strip() for line in text.splitlines() if line.strip()]


STATUS_TO_SPECIES_WARRANT: dict[str, tuple[list[str], list[str]]] = {
    # Core primitives and stances
    "primitive": (["FRAMEWORK_PRIMITIVE"], ["PHILOSOPHICAL"]),
    "stance": (["FRAMEWORK_STANCE"], ["PHILOSOPHICAL"]),
    "ontological_primitive": (["FRAMEWORK_PRIMITIVE"], ["PHILOSOPHICAL"]),

    # Cross-domain bridges (declared explicitly)
    "bridge": (["BRIDGE"], ["BRIDGE"]),

    # Boundary conditions and identifications
    "boundary": (["BOUNDARY_CONDITION"], ["CONDITIONAL"]),
    "identification": (["IDENTIFICATION"], ["THEOLOGICAL"]),

    # Axiomatic gaps and open markers
    "axiomatic_gap": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "open_problem": (["OPEN_PROBLEM"], ["OPEN"]),

    # Definitions and equations
    "definition": (["DEFINITION"], ["DEFINITIONAL"]),
    "equation": (["EQUATION"], ["MATHEMATICAL"]),
    "scale_definition": (["DEFINITION"], ["DEFINITIONAL"]),

    # Framework extensions
    "logical_necessity": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "property": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "framework_commitment": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "invariant": (["FRAMEWORK_EXTENSION"], ["MATHEMATICAL"]),
    "meta_axiom": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "stage": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "terminal_axiom": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "universal": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "closure_axiom": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "completion": (["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]),
    "fruit": (["FRAMEWORK_EXTENSION"], ["NORMATIVE"]),

    # Theorems and derived results
    "theorem": (["FRAMEWORK_THEOREM"], ["MATHEMATICAL_CONDITIONAL"]),
    "derived": (["FRAMEWORK_THEOREM"], ["MATHEMATICAL_CONDITIONAL"]),
    "master_theorem": (["FRAMEWORK_THEOREM"], ["MATHEMATICAL_CONDITIONAL"]),
    "optimality_theorem": (["FRAMEWORK_THEOREM"], ["MATHEMATICAL_CONDITIONAL"]),
    "uniqueness_theorem": (["FRAMEWORK_THEOREM"], ["MATHEMATICAL_CONDITIONAL"]),
    "corollary": (["COROLLARY"], ["CONDITIONAL"]),

    # Empirical / hypothesis register
    "hypothesis": (["HYPOTHESIS"], ["EMPIRICAL"]),
    "protocol": (["PROTOCOL"], ["EMPIRICAL"]),
    "prediction": (["PREDICTION"], ["EMPIRICAL"]),
    "falsification": (["FALSIFICATION"], ["EMPIRICAL"]),
    "experiment": (["EXPERIMENT"], ["EMPIRICAL"]),
    "experimental": (["EXPERIMENT"], ["EMPIRICAL"]),
    "evidence": (["EVIDENCE"], ["EMPIRICAL"]),
    "evidence_contested": (["EVIDENCE"], ["EMPIRICAL"]),
}


def derive_species_and_warrant(frontmatter: dict) -> tuple[list[str], list[str]]:
    """Map declared metadata to the allowed claim species and warrant classes.

    This mapping is intentionally conservative: it never promotes a source
    marked primitive/stance/boundary into a formal proof, empirical result,
    or cross-domain bridge.
    """
    status = (frontmatter.get("status") or "").lower()
    mode = (frontmatter.get("mode") or "").upper()
    atlas_type = (frontmatter.get("atlas_type") or "").lower()
    domain = (frontmatter.get("domain") or "").lower()

    # Cross-domain bridges from atlas type.
    if atlas_type == "bridge":
        return ["BRIDGE"], ["BRIDGE"]

    # Boundary conditions in the Divine domain get a theological warrant,
    # but they remain boundary conditions, not proofs.
    if status == "boundary" and domain in {"divine", "theology"}:
        return ["BOUNDARY_CONDITION"], ["THEOLOGICAL"]

    # Explicit status mapping.
    if status in STATUS_TO_SPECIES_WARRANT:
        return STATUS_TO_SPECIES_WARRANT[status]

    # Mode-level fallbacks for statuses not explicitly mapped.
    if mode == "HY_EVIDENCE":
        return ["HYPOTHESIS"], ["EMPIRICAL"]
    if mode == "FW_EXTENDED":
        return ["FRAMEWORK_EXTENSION"], ["PHILOSOPHICAL"]
    if mode == "AX_DERIVED":
        return ["DERIVED"], ["CONDITIONAL"]

    # Unknown/unmapped metadata: leave species/warrant open so the guard does
    # not silently force a wrong classification.
    return [], []


def bridge_limits(frontmatter: dict) -> dict:
    """Return bridge governance based on the declared atlas type and status."""
    atlas_type = (frontmatter.get("atlas_type") or "").lower()
    status = (frontmatter.get("status") or "").lower()
    permitted = atlas_type == "bridge" or status == "bridge"
    return {
        "permitted": permitted,
        "requires_explicit_source_target_mapping": True,
        "never_propagates_proof": True,
    }


def parse_dependencies(depends_on: str | None) -> list[str]:
    """Normalize the frontmatter depends_on field into a list of IDs.

    Handles both comma-separated IDs and prose forms such as
    'depends on anchor: D3.3 (Interaction Lagrangian)'.
    """
    if not depends_on:
        return []
    raw = depends_on.strip()
    if raw in {"∅ (foundational)", "∅ (core root)", "∅", "none", "None"}:
        return []

    # If the value is a prose anchor reference, extract the leading ID.
    ids: list[str] = []
    for segment in raw.split(","):
        segment = segment.strip()
        if not segment:
            continue
        # Strip common prefix noise.
        segment = re.sub(r"^(?:depends on anchor:\s*)", "", segment, flags=re.IGNORECASE)
        # Capture the leading ID token (e.g. D3.3, T3.1, A1.1, etc.).
        match = re.match(r"([A-Za-z0-9._\-]+)", segment)
        if match:
            ids.append(match.group(1))
    return ids


def build_source_governance(source_path: Path) -> dict:
    """Extract mode, status, dependencies, defeat conditions, limitations,
    and bridge limits from the source note's canonical text.
    """
    text = source_path.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    species, warrants = derive_species_and_warrant(fm)
    bridge = bridge_limits(fm)

    defeat_text = extract_section(text, "Defeat Conditions")
    limitations_text = extract_section(text, "Limitations (from workbook)")

    return {
        "declared_id": fm.get("id"),
        "declared_mode": fm.get("mode"),
        "declared_status": fm.get("status"),
        "atlas_type": fm.get("atlas_type"),
        "domain": fm.get("domain"),
        "anchor": fm.get("anchor"),
        "depends_on": parse_dependencies(fm.get("depends_on")),
        "defeat_conditions": parse_list_section(defeat_text),
        "limitations": parse_list_section(limitations_text),
        "allowed_claim_species": species,
        "allowed_warrant_classes": warrants,
        "bridge_permitted": bridge["permitted"],
        "bridge_limits": bridge,
    }


def auto_claim_and_defeat(source_path: Path, line_start: int, line_end: int) -> tuple[str, str]:
    """Fallback claim/defeat extraction from the Statement and Defeat Conditions sections.

    Prefers the clean Statement body; the pinned line span is only a fallback.
    """
    text = source_path.read_text(encoding="utf-8", errors="replace")
    statement = extract_section(text, "Statement")
    if statement:
        claim = statement.strip()
    else:
        lines = text.splitlines()
        claim = "\n".join(lines[line_start - 1 : line_end]).strip()

    defeat_text = extract_section(text, "Defeat Conditions")
    if defeat_text:
        defeat = "; ".join(parse_list_section(defeat_text))
    else:
        defeat = "OPEN — no independently specified defeat condition."
    return claim, defeat


def build_capsule(spec: dict, source_path: Path) -> dict:
    source_hash = sha256_file(source_path)
    text = source_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    line_start = spec["line_start"]
    line_end = spec["line_end"]
    quoted = "\n".join(lines[line_start - 1 : line_end])

    claim = spec.get("claim")
    plain_language = spec.get("plain_language")
    defeat_condition = spec.get("defeat_condition")
    if claim is None or plain_language is None or defeat_condition is None:
        auto_claim, auto_defeat = auto_claim_and_defeat(source_path, line_start, line_end)
        if claim is None:
            claim = auto_claim
        if plain_language is None:
            plain_language = auto_claim
        if defeat_condition is None:
            defeat_condition = auto_defeat

    capsule = {
        "schema_version": "claim-capsule/1.0.0",
        "candidate_label": "CANDIDATE_DRAFT — NOT ADMITTED",
        "claim": claim,
        "plain_language": plain_language,
        "claim_type": spec["claim_type"],
        "operation": spec["operation"],
        "defeat_condition": defeat_condition,
        "canonical_promotion_requested": False,
        "source": {
            "path_or_uri": str(source_path),
            "source_hash": source_hash,
            "heading": spec["heading"],
            "line_start": line_start,
            "line_end": line_end,
            "quotation": quoted,
            "quotation_hash": digest_text(quoted),
        },
        "source_governance": spec.get("source_governance") or build_source_governance(source_path),
    }
    if "discovery_incomplete_reason" in spec:
        capsule["discovery_incomplete_reason"] = spec["discovery_incomplete_reason"]
    if "decomposition_guidance" in spec:
        capsule["decomposition_guidance"] = spec["decomposition_guidance"]
    return capsule


def run_pipeline(capsule: dict, provider: str, model: str) -> Path:
    source_name = Path(capsule["source"]["path_or_uri"]).name.replace(".md", "")
    capsule_path = OUTPUT_ROOT / "capsules" / f"{source_name}.capsule.json"
    capsule_path.parent.mkdir(parents=True, exist_ok=True)
    capsule_path.write_text(json.dumps(capsule, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(PIPELINE_SCRIPT), "--review-json", str(capsule_path), "--output-dir", str(OUTPUT_ROOT / "receipts"), "--provider", provider, "--model", model],
        capture_output=True,
        timeout=300,
    )
    def decode_console(value: bytes) -> str:
        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            return value.decode("cp1252", errors="replace")

    stdout = decode_console(result.stdout)
    stderr = decode_console(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed: {stderr}")
    return json.loads(stdout)


def projection_path(receipt: dict) -> Path:
    run_id = receipt["run_id"]
    return OUTPUT_ROOT / "projections" / f"{run_id}.projection.md"


def display_statement(value: object) -> str:
    """Render structured stage output without leaking Python dictionaries into Markdown."""
    if isinstance(value, dict):
        return str(value.get("text") or value.get("statement") or value.get("claim") or "N/A")
    return str(value or "N/A")


def write_projection(receipt: dict, capsule: dict) -> Path:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "projections").mkdir(parents=True, exist_ok=True)

    disc = next((s for s in receipt["stages"] if s["name"] == "discovery"), {})
    clas = next((s for s in receipt["stages"] if s["name"] == "classification"), {})
    rec = next((s for s in receipt["stages"] if s["name"] == "reconciliation"), {})

    disc_out = disc.get("output", {})
    clas_out = clas.get("output", {})
    rec_out = rec.get("output", {})

    gov = capsule.get("source_governance", {})

    lines = [
        f"# {capsule['candidate_label']}",
        "",
        f"**Source:** `{capsule['source']['path_or_uri']}`",
        f"**Source hash:** {capsule['source']['source_hash']}",
        f"**Line span:** {capsule['source']['line_start']}\u2013{capsule['source']['line_end']}",
        f"**Heading:** {capsule['source']['heading']}",
        f"**Pipeline run:** {receipt['run_id']}",
        f"**Final status:** {receipt['final_status']}",
        "",
        "## Claim",
        "",
        f"> {capsule['claim']}",
        "",
        "## Plain language",
        "",
        capsule["plain_language"],
        "",
        "## Source quotation",
        "",
        "```markdown",
        capsule["source"]["quotation"],
        "```",
        "",
        "## Source governance (auto-extracted)",
        "",
        f"- **declared_mode:** {gov.get('declared_mode') or 'N/A'}",
        f"- **declared_status:** {gov.get('declared_status') or 'N/A'}",
        f"- **atlas_type:** {gov.get('atlas_type') or 'N/A'}",
        f"- **domain:** {gov.get('domain') or 'N/A'}",
        f"- **depends_on:** {', '.join(gov.get('depends_on', [])) or 'none'}",
        f"- **bridge_permitted:** {gov.get('bridge_permitted', False)}",
        "",
        "### Defeat conditions",
    ]
    for item in gov.get("defeat_conditions", []):
        lines.append(f"- {item}")
    if not gov.get("defeat_conditions"):
        lines.append("_None extracted_")

    lines.extend(["", "### Limitations"])
    for item in gov.get("limitations", []):
        lines.append(f"- {item}")
    if not gov.get("limitations"):
        lines.append("_None extracted_")

    lines.extend([
        "",
        "---",
        "",
        "## Stage 1 \u2014 NON_DISCRIMINATORY_DISCOVERY",
        "",
        f"- **status:** {disc_out.get('status', 'N/A')}",
        f"- **raw_expression:** {disc_out.get('raw_expression', 'N/A')}",
        f"- **referent:** {disc_out.get('referent', 'N/A')}",
        "",
        "### Distinctions",
    ])
    for item in disc_out.get("distinctions", []):
        lines.append(f"- {item}")
    lines.extend(["", "### Dependencies"])
    for item in disc_out.get("dependencies", []):
        lines.append(f"- {item}")
    lines.extend(["", "### Countermodels"])
    for item in disc_out.get("countermodels", []):
        lines.append(f"- {item}")
    lines.extend(["", "### Open questions"])
    for item in disc_out.get("open_questions", []):
        lines.append(f"- {item}")
    lines.extend(["", "### Prohibited outputs withheld"])
    for item in disc_out.get("prohibited_outputs", []):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "---",
        "",
        "## Stage 2 \u2014 CLASSIFICATION_AND_BURDEN_ROUTING",
        "",
        f"- **status:** {clas_out.get('status', 'N/A')}",
        f"- **object_type:** {clas_out.get('object_type', 'N/A')}",
        f"- **register:** {clas_out.get('register', 'N/A')}",
        f"- **claim_species:** {clas_out.get('claim_species', 'N/A')}",
        f"- **warrant_class:** {clas_out.get('warrant_class', 'N/A')}",
        f"- **why_outcome:** {clas_out.get('why_outcome', 'N/A')}",
        "",
        "### Burdens",
    ])
    for item in clas_out.get("burdens", []):
        lines.append(f"- {item}")
    lines.extend(["", "### Unresolved"])
    for item in clas_out.get("unresolved", []):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "---",
        "",
        "## Stage 3 \u2014 RECONCILIATION_TRANSLATION_AND_FIT",
        "",
        f"- **status:** {rec_out.get('status', 'N/A')}",
        f"- **recommended_operation:** {rec_out.get('recommended_operation', 'N/A')}",
        f"- **publication_eligibility:** {rec_out.get('publication_eligibility', 'N/A')}",
        f"- **human_ruling_required:** {rec_out.get('human_ruling_required', 'N/A')}",
        "",
        "### Native statement",
        display_statement(rec_out.get("native_statement")),
        "",
        "### Bridge statement",
        f"{rec_out.get('bridge_statement') or '_None \u2014 not a bridge claim_'}",
        "",
        "### Identification statement",
        f"{rec_out.get('identification_statement') or '_None \u2014 no identification claimed_'}",
        "",
        "### Preserved structure",
    ])
    for item in rec_out.get("preserved", []):
        lines.append(f"- {item}")
    lines.extend(["", "### Lost structure"])
    for item in rec_out.get("lost", []) or ["_No lost structure reported_"]:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "---",
        "",
        "## Defeat condition",
        "",
        capsule["defeat_condition"],
        "",
        "---",
        "",
        "## Review queue action",
        "",
        "David records one of: APPROVE CANDIDATE | REVISE | SPLIT | HOLD OPEN | WITHDRAW | REJECT",
        "",
        f"- Receipt JSON: `{receipt.get('receipt_path', 'N/A')}`",
    ])

    path = projection_path(receipt)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_queue(receipts_capsules: list[tuple[dict, dict, Path]]) -> Path:
    path = OUTPUT_ROOT / "queue.md"
    lines = [
        f"# Review queue \u2014 {datetime.now(timezone.utc).isoformat()}",
        "",
        "**Status:** All entries are `CANDIDATE_DRAFT \u2014 NOT ADMITTED`. No source files were edited. No admission events occurred.",
        "",
        "| # | Source note | Line span | Claim (one-line) | Pipeline status | Projection |",
        "|---|-------------|-----------|------------------|-----------------|------------|",
    ]
    for i, (receipt, capsule, proj_path) in enumerate(receipts_capsules, 1):
        rel_source = str(Path(capsule["source"]["path_or_uri"]).relative_to(VAULT))
        rel_proj = str(proj_path.relative_to(VAULT))
        lines.append(
            f"| {i} | `{rel_source}` | {capsule['source']['line_start']}\u2013{capsule['source']['line_end']} | {capsule['claim'][:60]}{'...' if len(capsule['claim']) > 60 else ''} | {receipt['final_status']} | [{proj_path.name}]({rel_proj}) |"
        )
    lines.extend([
        "",
        "## Human ruling legend",
        "",
        "- **APPROVE CANDIDATE** \u2014 approve this candidate packet only; it does not admit anything into canon.",
        "- **REVISE** \u2014 candidate needs modification and re-run.",
        "- **SPLIT** \u2014 source contains multiple assertions; create separate capsules.",
        "- **HOLD OPEN** \u2014 keep as candidate pending further evidence.",
        "- **WITHDRAW** \u2014 remove from active candidate set.",
        "- **REJECT** \u2014 candidate is not admissible.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run claim pipeline demo batch with auto-extracted source_governance.")
    parser.add_argument("--provider", choices=["deepseek", "mock"], default=DEFAULT_PROVIDER)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    receipts_capsules = []

    for spec in SOURCES:
        source_path = SOURCE_DIR / spec["filename"]
        if not source_path.is_file():
            print(f"SKIP: source not found {source_path}")
            continue

        capsule = build_capsule(spec, source_path)
        print(f"Processing {spec['id']}...")
        print(f"  source_governance: {json.dumps(capsule.get('source_governance'), ensure_ascii=False)}")
        receipt = run_pipeline(capsule, args.provider, args.model)
        proj_path = write_projection(receipt, capsule)
        receipts_capsules.append((receipt, capsule, proj_path))
        print(f"  -> receipt: {receipt.get('receipt_path')}")
        print(f"  -> projection: {proj_path}")

    queue_path = write_queue(receipts_capsules)
    print(f"\nQueue written: {queue_path}")
    print(f"Output root: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
