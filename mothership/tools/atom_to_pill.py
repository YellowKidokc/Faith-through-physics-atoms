"""Convert JSON-LD atoms into YAML pills.

A pill is a thin face + fat veins representation of an atom.  The face carries
the fields needed for grepping, display, and curator passes; the veins carry
everything else unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


PROJECT_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "faiththruphysics.com")
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".pytest_cache"}


def _first(data: dict[str, Any], keys: tuple[str, ...]) -> Any:
    """Return the first matching key's value, or None."""
    for key in keys:
        if key in data:
            return data[key]
    return None


def _infer_target_type(data: dict[str, Any]) -> str | None:
    """Infer a target_type from JSON-LD type fields."""
    raw = _first(data, ("target_type", "claimKind", "nodeType", "@type", "domainType"))
    if not raw:
        return None

    if isinstance(raw, list):
        candidates = raw
    else:
        candidates = [raw]

    type_map = {
        "claim": "claim",
        "definition": "definition",
        "axiom": "axiom",
        "proof": "proof",
        "sentence": "sentence",
        "equation": "equation",
        "table": "table",
        "figure": "figure",
        "word": "word",
    }

    for candidate in candidates:
        if not isinstance(candidate, str):
            continue
        lower = candidate.lower()
        for key, value in type_map.items():
            if key in lower:
                return value
        # Allow prefixed types like tp:ClaimAtom.
        for key, value in type_map.items():
            if key in lower.replace("atom", "").replace("node", ""):
                return value
    return None


def _stable_uuid(data: dict[str, Any], relative_path: str) -> tuple[str, bool]:
    """Return (uuid, was_minted).

    Uses an existing uuid if present.  Otherwise mints a deterministic UUIDv5
    from the project namespace and the atom's nodeID / claimID / @id / path.
    """
    existing = _first(data, ("uuid", "@uuid"))
    if existing and isinstance(existing, str) and existing.strip():
        return existing.strip(), False

    identifier = _first(data, ("nodeID", "claimID", "@id", "id"))
    if identifier and isinstance(identifier, str) and identifier.strip():
        seed = identifier.strip()
    else:
        seed = relative_path
    return str(uuid.uuid5(PROJECT_NAMESPACE, seed)), True


def _extract_face(data: dict[str, Any], relative_path: str) -> tuple[dict[str, Any], list[str]]:
    """Build the pill face and return (face, errors)."""
    errors: list[str] = []
    face_uuid, was_minted = _stable_uuid(data, relative_path)

    face: dict[str, Any] = {
        "uuid": face_uuid,
        "node_id": _first(data, ("nodeID", "@id", "id")),
        "claim_id": data.get("claimID"),
        "name": data.get("name"),
        "term": _first(data, ("term", "canonical_term", "preferredTerm", "name")),
        "plain": _first(
            data,
            (
                "plain",
                "plainDefinition",
                "statementPlain",
                "plain_definition",
                "statementTechnical",
                "exact_definition",
            ),
        ),
        "status": _first(data, ("status", "canonicalStatus", "intendedStatus")),
        "target_type": _infer_target_type(data),
    }

    # Add source information if present.
    source = _first(data, ("source", "sourceReference"))
    if isinstance(source, dict):
        face["source"] = {
            "doc_uuid": source.get("doc_uuid") or source.get("documentUUID"),
            "doc_sha256": source.get("doc_sha256") or source.get("documentSHA256"),
        }

    # Remove None values for a cleaner face.
    face = {k: v for k, v in face.items() if v is not None}
    return face, errors


def _build_veins(data: dict[str, Any], face: dict[str, Any]) -> dict[str, Any]:
    """Return the remaining JSON-LD content after removing face fields."""
    face_keys = {
        "uuid",
        "nodeID",
        "@id",
        "claimID",
        "name",
        "term",
        "canonical_term",
        "preferredTerm",
        "plain",
        "plainDefinition",
        "statementPlain",
        "plain_definition",
        "statementTechnical",
        "exact_definition",
        "status",
        "canonicalStatus",
        "intendedStatus",
        "target_type",
        "claimKind",
        "nodeType",
        "@type",
        "domainType",
    }
    veins = {k: v for k, v in data.items() if k not in face_keys}
    return veins


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def convert_atom(
    source_path: Path,
    input_root: Path,
    output_root: Path,
) -> tuple[Path | None, bool, list[str]]:
    """Convert one JSON-LD atom to a YAML pill.

    Returns (output_path, uuid_was_minted, errors).
    """
    errors: list[str] = []
    try:
        text = source_path.read_text(encoding="utf-8")
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, False, [f"JSON decode error in {source_path}: {exc}"]
    except OSError as exc:
        return None, False, [f"Read error for {source_path}: {exc}"]

    if not isinstance(data, dict):
        return None, False, [f"Top-level JSON is not an object: {source_path}"]

    relative_path = str(source_path.relative_to(input_root).as_posix())
    face, face_errors = _extract_face(data, relative_path)
    errors.extend(face_errors)
    uuid_was_minted = face.get("uuid") and "uuid" not in data

    veins = _build_veins(data, face)

    pill = {
        "face": face,
        "veins": veins,
        "_metadata": {
            "source_path": relative_path,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "sha256": _sha256_file(source_path),
        },
    }

    relative_stem = source_path.relative_to(input_root).with_suffix("")
    output_path = output_root / relative_stem.with_suffix(".pill.yaml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(pill, fh, sort_keys=False, allow_unicode=True)

    return output_path, bool(uuid_was_minted), errors


def run_conversion(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Run the full conversion and return a summary."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir_resolved = output_dir.resolve()

    pills_created = 0
    uuids_minted = 0
    errors: list[str] = []

    for source_path in sorted(input_dir.rglob("*.jsonld")):
        # Skip output directory if it lives under input_dir.
        if output_dir_resolved in source_path.resolve().parents or source_path.resolve() == output_dir_resolved:
            continue
        # Skip forbidden directories.
        if any(part in SKIP_DIRS for part in source_path.parts):
            continue

        output_path, was_minted, errs = convert_atom(source_path, input_dir, output_dir)
        if errs:
            errors.extend(errs)
            continue
        if output_path is not None:
            pills_created += 1
            if was_minted:
                uuids_minted += 1

    return {
        "pills_created": pills_created,
        "uuids_minted": uuids_minted,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert JSON-LD atoms to YAML pills.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent,
        help="Root directory to scan for .jsonld files (default: repo root).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("mothership/pills"),
        help="Directory to write .pill.yaml files (default: mothership/pills).",
    )
    args = parser.parse_args(argv)

    summary = run_conversion(args.input_dir.resolve(), args.output_dir.resolve())
    print(json.dumps(summary, indent=2))
    return 0 if not summary["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
