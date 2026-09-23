from __future__ import annotations

import csv
import hashlib
import html
import json
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_information_object_standard"

CATEGORIES = [
    ("01", "Term / Definition", "Defines a term without pretending the definition proves a world-claim."),
    ("02", "Claim", "Stores one independently gradable assertion."),
    ("03", "Evidence", "Records what supports or challenges a claim, how it bears, and its limitations."),
    ("04", "MTL / Equation", "Stores a formal object, its symbols, assumptions, derivation status, and plain-language translation."),
    ("05", "Physics Event", "Records an empirical physical event or phenomenon with measurable conditions."),
    ("06", "Isomorphism", "Records a proposed structure-preserving mapping and the tests it must pass."),
    ("07", "Analogy / Metaphor", "Records a non-propagating comparison that aids understanding but does not prove identity."),
    ("08", "Trinity Pattern", "Records a proposed triadic structure with an explicit theological-identification boundary."),
    ("09", "Axiom", "Records an irreducible starting commitment and its scope."),
    ("10", "Law Mapping", "Connects a physical law to a spiritual principle without hiding bridge assumptions."),
    ("11", "Operator", "Records a transformation rule, input and output types, invariants, and failure conditions."),
    ("12", "Falsification / Kill Condition", "States what would weaken, bound, or destroy a target claim."),
    ("13", "Audit", "Records a reproducible inspection, its scope, tools, results, and unresolved gaps."),
    ("14", "Source Atom", "Preserves source language, provenance, location, and hash before interpretation."),
    ("15", "Media", "Connects audio, images, video, and transcripts to the objects they represent."),
    ("16", "Reviewer State", "Records a reviewer judgment without mutating the underlying object or admitting it to canon."),
]

SELECTIONS = {
    "02_OBJECT_CATEGORY_ATLAS": [
        "_docs/THEOPHYSICS_ARCHITECTURE_v11_CANONICAL.md",
    ],
    "03_WORKFLOW_STAGE_TYPES": [
        "_docs/CLAIM_ATOM_NODE_TYPES.md",
        "_template/CLAIM_ATOM_EXPANSION_AI_INTAKE_TEMPLATE_v1_1.md",
    ],
    "04_MACHINE_SCHEMAS": ["_schema/*.json"],
    "05_VOCABULARY": [
        "_vocab/context.jsonld",
        "_vocab/vocab.json",
        "_vocab/domains_and_tags.json",
        "_vocab/layers.json",
        "_vocab/stage_contracts.json",
        "_vocab/stage_contracts_public.json",
        "_vocab/stage_contracts_technical.json",
        "claim-atom-standard-1.0/tp-standard/vocab/context.jsonld",
    ],
    "06_EXAMPLES": [
        "demo-v12/_DOMAIN.json",
        "demo-v12/02_claim_atoms/demo-claim.jsonld",
        "claim-atom-standard-1.0/tp-standard/claims/A042/L9/*.jsonld",
        "claim-atom-standard-1.0/tp-standard/papers/*.jsonld",
        "_definitions/atoms/*.jsonld",
        "_definitions/evidence/*.jsonld",
    ],
    "07_DATABASE_AND_GOVERNANCE": [
        "_final_api_calls/03_THE_CLAIM_ATOM_EXPANSION_CANON_v1_1_FOUR_OBJECT_LAYERS_FULL.md",
        "_final_api_calls/04_THE_UNIFIED_GRAMMAR_METHODOLOGY_v1.md",
        "_final_api_calls/05_THE_TOTAL_DISCOVERY_CLASSIFICATION_TRANSLATION_SYSTEM_v1_0.md",
        "_final_api_calls/06_THE_TRANSLATION_AND_ISOMORPHISM_GRAMMAR_v1_0.md",
        "_final_api_calls/07_CANONICAL_CONTENT_OS_V0_1.md",
        "_final_api_calls/08_CLAIM_ATOM_SQL_SCHEMA_README.md",
        "_final_api_calls/08A_claim_atom_canon_v1_1_sqlite.sql",
        "_final_api_calls/13_END_TO_END_STACK_AUDIT_2026-09-01.md",
        "_final_api_calls/14_HTML_QUESTION_STAGE_AND_CANONICAL_HOME_CROSSWALK_2026-09-01.md",
        "_final_api_calls/SUPRA_INFRAQUE_RADICAL_EPISTEMIC_SCHEMA_v1.md",
    ],
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def selected_files():
    seen = set()
    for section, patterns in SELECTIONS.items():
        for pattern in patterns:
            matches = sorted(ROOT.glob(pattern))
            for source in matches:
                if source.is_file() and source.resolve() not in seen:
                    seen.add(source.resolve())
                    yield section, source


def build_html(manifest: list[dict], json_results: list[dict]) -> str:
    nav = "".join(
        f'<a href="#cat-{n}"><span>{n}</span>{html.escape(name)}</a>'
        for n, name, _ in CATEGORIES
    )
    cards = "".join(
        f'''<section id="cat-{n}" class="card">
        <div class="eyebrow">OBJECT CATEGORY / {n}</div>
        <h2>{html.escape(name)}</h2>
        <span class="badge">PROPOSED GOVERNANCE</span>
        <p>{html.escape(desc)}</p>
        <div class="rule"><b>Required discipline</b><br>Preserve source provenance, distinguish object type from workflow stage, attach edges explicitly, and never infer canon admission from rendering or location.</div>
        </section>'''
        for n, name, desc in CATEGORIES
    )
    valid = sum(1 for row in json_results if row["status"] == "valid")
    invalid = sum(1 for row in json_results if row["status"] == "invalid")
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Faith Through Physics — Information Object Standard</title>
<style>
:root{{--bg:#07111f;--panel:#0d1a2b;--line:#25364a;--text:#e8eef7;--muted:#9eb0c6;--gold:#d9b66f;--cyan:#63d4d5}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,Segoe UI,sans-serif}}
.layout{{display:grid;grid-template-columns:300px 1fr;min-height:100vh}} aside{{position:sticky;top:0;height:100vh;padding:30px 22px;border-right:1px solid var(--line);overflow:auto;background:#091525}}
aside h1{{font:700 22px Georgia,serif;margin:0 0 6px}} aside p{{color:var(--muted);font-size:13px}} nav{{display:grid;gap:5px;margin-top:22px}} nav a{{color:var(--muted);text-decoration:none;padding:8px 10px;border-radius:6px}} nav a:hover{{background:#14243a;color:white}} nav span{{color:var(--gold);display:inline-block;width:34px}}
main{{max-width:1100px;padding:54px 7vw 100px}} .hero{{padding-bottom:38px;border-bottom:1px solid var(--line)}} h1,h2{{font-family:Georgia,serif}} .hero h1{{font-size:42px;margin:.15em 0}} .hero p{{color:var(--muted);max-width:850px}} .stats{{display:flex;gap:12px;flex-wrap:wrap}} .stat,.badge{{border:1px solid var(--line);border-radius:999px;padding:5px 11px;color:var(--gold);font-size:12px}}
.card{{padding:42px 0;border-bottom:1px solid var(--line)}} .card h2{{font-size:32px;margin:4px 0 6px}} .eyebrow{{color:var(--gold);font-size:12px;letter-spacing:.12em}} .rule{{background:#102a34;border-left:3px solid var(--cyan);padding:18px;margin-top:22px;color:#c8e3e5}} .boundary{{margin-top:30px;padding:22px;border:1px solid #70424a;background:#25151b}}
code{{color:#a9e8e8}} @media(max-width:800px){{.layout{{display:block}}aside{{position:relative;height:auto}}}}
</style></head><body><div class="layout"><aside><h1>Information Object Standard</h1><p>Faith Through Physics · compiled standards workbench</p><nav>{nav}</nav></aside><main>
<header class="hero"><div class="eyebrow">FORMAL INFORMATION ARCHITECTURE</div><h1>One envelope. Many object types. Explicit epistemic boundaries.</h1>
<p>This atlas separates an object's <b>type</b> from its workflow <b>stage</b>. A claim is not evidence; evidence is not proof; a Lean receipt is not an empirical bridge; and a rendered page is not canon admission.</p>
<div class="stats"><span class="stat">{len(CATEGORIES)} object categories</span><span class="stat">{len(manifest)} preserved source files</span><span class="stat">{valid} valid JSON documents</span><span class="stat">{invalid} invalid JSON documents</span></div>
<div class="boundary"><b>Status: candidate standard.</b> This compilation preserves and compares existing designs. It does not silently supersede them or admit any object to canon.</div></header>
{cards}
</main></div></body></html>'''


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    for name in ["01_DEFAULT_CORE", *SELECTIONS.keys(), "08_HTML", "99_MANIFEST"]:
        (OUT / name).mkdir(parents=True, exist_ok=True)

    manifest = []
    by_hash = defaultdict(list)
    json_results = []
    for section, source in selected_files():
        relative = source.relative_to(ROOT)
        destination = OUT / section / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        digest = sha256(source)
        by_hash[digest].append(relative.as_posix())
        manifest.append({
            "section": section,
            "source_path": str(source),
            "source_relative": relative.as_posix(),
            "copied_relative": destination.relative_to(OUT).as_posix(),
            "bytes": source.stat().st_size,
            "sha256": digest,
        })
        if source.suffix.lower() in {".json", ".jsonld"}:
            try:
                json.loads(source.read_text(encoding="utf-8-sig"))
                status, error = "valid", ""
            except Exception as exc:
                status, error = "invalid", str(exc)
            json_results.append({"source_relative": relative.as_posix(), "status": status, "error": error})

    default_core = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://faiththruphysics.com/schema/information-object-envelope/v0.1-candidate",
        "title": "Faith Through Physics Universal Information Object Envelope",
        "description": "Candidate minimum shared envelope. Type-specific schemas extend this record.",
        "type": "object",
        "required": ["@id", "nodeID", "nodeType", "name", "status", "version", "provenance", "edges"],
        "properties": {
            "@context": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
            "@id": {"type": "string", "format": "uri"},
            "nodeID": {"type": "string"},
            "nodeType": {"type": "string"},
            "name": {"type": "string", "minLength": 1},
            "status": {"type": "string"},
            "version": {"type": "string"},
            "stage": {"type": "string"},
            "statementTechnical": {"type": "string"},
            "statementPlain": {"type": "string"},
            "provenance": {"type": "object", "required": ["sourcePath", "sha256"], "properties": {"sourcePath": {"type": "string"}, "sha256": {"type": "string", "pattern": "^[A-Fa-f0-9]{64}$"}}},
            "edges": {"type": "array", "items": {"type": "object", "required": ["type", "target"], "properties": {"type": {"type": "string"}, "target": {"type": "string"}, "grade": {"type": "string"}, "propagates": {"type": "boolean"}}}},
            "verification": {"type": "object"},
            "falsification": {"type": "object"}
        },
        "additionalProperties": True,
        "x-governance-status": "CANDIDATE_DRAFT_NOT_ADMITTED"
    }
    (OUT / "01_DEFAULT_CORE" / "universal-information-object-envelope.candidate.schema.json").write_text(json.dumps(default_core, indent=2), encoding="utf-8")

    # Preserve the malformed source exactly in 04_MACHINE_SCHEMAS, but also
    # provide an explicitly named repair candidate for review and testing.
    broken_definition = ROOT / "_schema" / "definition_atom.schema.json"
    broken_text = broken_definition.read_text(encoding="utf-8-sig")
    old_fragment = '"inheritToDependents": {"type": "boolean"}, "additionalProperties": false},'
    new_fragment = '"inheritToDependents": {"type": "boolean"}}, "additionalProperties": false},'
    if old_fragment not in broken_text:
        raise RuntimeError("Expected definition-atom repair fragment was not found; source changed")
    repaired_text = broken_text.replace(old_fragment, new_fragment, 1)
    json.loads(repaired_text)
    (OUT / "01_DEFAULT_CORE" / "definition_atom.repaired-candidate.schema.json").write_text(repaired_text, encoding="utf-8")
    readme = """# Faith Through Physics Information Object Standard — Candidate Workbench

This packet compiles the existing default and expanded information-object systems without changing or deleting their source files.

## Architectural ruling

1. **Universal envelope:** stable identity, type, status, version, provenance, and typed edges.
2. **Object category:** what the record is—claim, evidence, equation, source atom, audit, media, and so forth.
3. **Workflow stage:** where the object currently sits—inbox, canonical-claim candidate, synthesis, falsification, publication, or review.
4. **Type-specific payload:** fields required only for that category.
5. **Review state:** a separate judgment record; it must not silently mutate the reviewed object.

The default envelope should remain small. Expanded schemas supply specialized fields. JSON-LD is the machine authority; HTML is a generated human view; Markdown is the editable explanatory companion.

## Non-claims

- Copying a record here does not canonize it.
- A formal receipt proves only the encoded statement under its assumptions.
- Evidence supports or challenges a claim; it is not itself the claim.
- An isomorphism record must state its mapping, invariants, inverse/bijection requirements where applicable, boundary conditions, and kill test.

## Rebuild

Run `_scripts/build_information_object_standard.py`. The build recreates this folder from selected repository sources and writes hashes and validation results under `99_MANIFEST`.
"""
    (OUT / "00_README.md").write_text(readme, encoding="utf-8")
    (OUT / "01_DEFAULT_CORE" / "object-categories.candidate.json").write_text(json.dumps([{"order": n, "name": name, "purpose": desc, "status": "proposed"} for n, name, desc in CATEGORIES], indent=2), encoding="utf-8")
    (OUT / "08_HTML" / "information-object-standard-atlas.html").write_text(build_html(manifest, json_results), encoding="utf-8")

    with (OUT / "99_MANIFEST" / "files.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=manifest[0].keys())
        writer.writeheader(); writer.writerows(manifest)
    duplicates = [{"sha256": digest, "count": len(paths), "paths": paths} for digest, paths in by_hash.items() if len(paths) > 1]
    (OUT / "99_MANIFEST" / "duplicate-groups.json").write_text(json.dumps(duplicates, indent=2), encoding="utf-8")
    (OUT / "99_MANIFEST" / "json-validation.json").write_text(json.dumps(json_results, indent=2), encoding="utf-8")
    receipt = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(ROOT),
        "output_root": str(OUT),
        "source_file_count": len(manifest),
        "duplicate_group_count": len(duplicates),
        "json_valid": sum(1 for x in json_results if x["status"] == "valid"),
        "json_invalid": sum(1 for x in json_results if x["status"] == "invalid"),
        "status": "CANDIDATE_COMPILATION_NOT_CANON_ADMISSION",
    }
    (OUT / "99_MANIFEST" / "build-receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
