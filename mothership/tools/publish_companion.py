"""Publish a CKG companion into the mothership companions folder.

A companion is a Markdown file with YAML front matter plus a section-by-section
scorecard (S01..S10) and the original article body.  This tool validates,
normalizes, mints missing UUIDs, writes the companion to the output directory,
and updates companions/index.json atomically.
"""

from __future__ import annotations

import argparse
import json
import re
import uuid
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


PROJECT_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "faiththruphysics.com")
REQUIRED_FIELDS = (
    "title",
    "clean_title",
    "status",
    "type",
    "one_sentence_finding",
    "claim_ids",
    "score_total",
    "score_ceiling",
    "score_class",
    "build_next",
)
# paper_uuid is conceptually required but is auto-minted if absent.
REQUIRED_SCORE_FIELDS = ("_pos", "_neg", "_net", "_ceiling")
STATUS_VOCABULARY = {
    "CANDIDATE_DRAFT",
    "CANDIDATE",
    "REVIEW_PENDING",
    "UNDER_REVIEW",
    "ACCEPTED",
    "REJECTED",
    "RETIRED",
}


class CompanionValidationError(Exception):
    """Raised when a companion fails validation."""


@dataclass(frozen=True)
class CompanionResult:
    """Result of publishing one companion."""

    output_path: Path
    paper_uuid: str
    title: str
    status: str
    claim_ids: list[str]
    claim_uuids_minted: int
    paper_uuid_minted: bool


def _sluggify(title: str) -> str:
    """Convert a title into a safe filename slug."""
    lower = title.lower()
    lower = re.sub(r"[^a-z0-9]+", "_", lower)
    lower = re.sub(r"_+", "_", lower)
    return lower.strip("_")


def _parse_bare_front_matter(stripped: str) -> tuple[dict[str, Any], str] | None:
    """Parse bare `---` ... `---` YAML front matter if present."""
    if not stripped.startswith("---"):
        return None
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", stripped, re.DOTALL)
    if not match:
        return None
    yaml_text = match.group(1)
    body = stripped[match.end():]
    try:
        front_matter = yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError as exc:
        raise CompanionValidationError(f"Invalid YAML front matter: {exc}") from exc
    if not isinstance(front_matter, dict):
        raise CompanionValidationError("YAML front matter is not a mapping")
    return front_matter, body


def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML front matter and the remaining Markdown body.

    Supports both bare YAML front matter (starts with ---) and the legacy CKG
    fenced YAML block (starts with ```yaml).
    """
    stripped = text.lstrip("\n")

    # Legacy fenced YAML block: ```yaml
    if stripped.startswith("```yaml"):
        end_fence = stripped.find("\n```")
        if end_fence == -1:
            raise CompanionValidationError("Fenced YAML block has no closing ```")
        inner = stripped[len("```yaml"):end_fence].strip()
        body = stripped[end_fence + len("\n```"):].lstrip("\n")

        # The fenced block may itself wrap bare `---` front matter.
        parsed = _parse_bare_front_matter(inner)
        if parsed is not None:
            return parsed[0], body

        try:
            front_matter = yaml.safe_load(inner) or {}
        except yaml.YAMLError as exc:
            raise CompanionValidationError(f"Invalid YAML front matter: {exc}") from exc
        if not isinstance(front_matter, dict):
            raise CompanionValidationError("YAML front matter is not a mapping")
        return front_matter, body

    # Bare YAML front matter.
    parsed = _parse_bare_front_matter(stripped)
    if parsed is not None:
        return parsed

    raise CompanionValidationError("No YAML front matter found")


def _mint_claim_uuids(front_matter: dict[str, Any]) -> tuple[dict[str, str], int]:
    """Return (claim_uuids_map, number_of_newly_minted_uuids).

    Existing claim_uuids are preserved.  Missing UUIDs are minted deterministically
    from each claim_id.
    """
    claim_ids = front_matter.get("claim_ids", [])
    if not isinstance(claim_ids, list):
        raise CompanionValidationError("claim_ids must be a list")

    existing = front_matter.get("claim_uuids") or {}
    if not isinstance(existing, dict):
        existing = {}

    claim_uuids = dict(existing)
    minted = 0
    for claim_id in claim_ids:
        if not isinstance(claim_id, str):
            raise CompanionValidationError(f"claim_id must be a string: {claim_id!r}")
        if not claim_id.strip():
            raise CompanionValidationError("claim_ids cannot contain empty strings")
        if claim_id not in claim_uuids or not claim_uuids[claim_id]:
            claim_uuids[claim_id] = str(uuid.uuid5(PROJECT_NAMESPACE, claim_id))
            minted += 1

    return claim_uuids, minted


def _ensure_paper_uuid(front_matter: dict[str, Any], source_path: Path) -> tuple[str, bool]:
    """Return (paper_uuid, was_minted)."""
    paper_uuid = front_matter.get("paper_uuid")
    if paper_uuid and isinstance(paper_uuid, str) and paper_uuid.strip():
        return paper_uuid.strip(), False

    title = front_matter.get("title") or front_matter.get("clean_title") or source_path.stem
    seed = f"{title}:{source_path.resolve().as_posix()}"
    return str(uuid.uuid5(PROJECT_NAMESPACE, seed)), True


def _validate_front_matter(front_matter: dict[str, Any]) -> list[str]:
    """Return a list of validation errors."""
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in front_matter or front_matter[field] is None:
            errors.append(f"Missing required field: {field}")

    if "status" in front_matter:
        status_upper = str(front_matter["status"]).upper()
        if status_upper not in STATUS_VOCABULARY:
            errors.append(
                f"Invalid status '{front_matter.get('status')}'. "
                f"Must be one of: {sorted(STATUS_VOCABULARY)}"
            )

    claim_ids = front_matter.get("claim_ids")
    if claim_ids is not None and not isinstance(claim_ids, list):
        errors.append("claim_ids must be a list")
    elif isinstance(claim_ids, list) and not claim_ids:
        errors.append("claim_ids must not be empty")

    for section in range(1, 11):
        prefix = f"s{section:02d}"
        for suffix in REQUIRED_SCORE_FIELDS:
            field = f"{prefix}{suffix}"
            if field not in front_matter:
                errors.append(f"Missing score field: {field}")
            elif not isinstance(front_matter[field], int):
                errors.append(f"Score field {field} must be an integer")

    if "score_total" in front_matter and "score_ceiling" in front_matter:
        total = front_matter.get("score_total")
        ceiling = front_matter.get("score_ceiling")
        if isinstance(total, int) and isinstance(ceiling, int) and total > ceiling:
            errors.append("score_total cannot exceed score_ceiling")

    return errors


def _render_companion(front_matter: dict[str, Any], body: str) -> str:
    """Return the normalized companion file contents."""
    yaml_text = yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=True)
    return f"---\n{yaml_text}---\n\n{body}"


def _load_index(index_path: Path) -> list[dict[str, Any]]:
    """Load the companions index, returning an empty list if absent or empty."""
    if not index_path.exists():
        return []
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CompanionValidationError(f"Corrupt companions index: {exc}") from exc
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "companions" in data:
        return list(data["companions"])
    raise CompanionValidationError("companions/index.json must be a list or contain a 'companions' key")


def _write_index(index_path: Path, entries: list[dict[str, Any]]) -> None:
    """Write the index atomically."""
    index_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = index_path.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temp_path.replace(index_path)


def _update_index(
    index_path: Path,
    paper_uuid: str,
    title: str,
    status: str,
    relative_path: Path,
    source_file: str | None,
    claim_ids: list[str],
) -> None:
    """Add or replace an entry in the companions index."""
    entries = _load_index(index_path)
    entries = [e for e in entries if e.get("paper_uuid") != paper_uuid]
    entries.append(
        {
            "paper_uuid": paper_uuid,
            "title": title,
            "status": status,
            "path": str(relative_path.as_posix()),
            "source_file": source_file,
            "claim_ids": claim_ids,
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    _write_index(index_path, entries)


def publish_companion(
    input_path: Path,
    output_dir: Path,
) -> CompanionResult:
    """Publish one CKG companion.

    Raises CompanionValidationError on invalid input.
    """
    try:
        text = input_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CompanionValidationError(f"Cannot read input file: {exc}") from exc

    front_matter, body = _split_front_matter(text)

    validation_errors = _validate_front_matter(front_matter)
    if validation_errors:
        raise CompanionValidationError("; ".join(validation_errors))

    paper_uuid, paper_uuid_minted = _ensure_paper_uuid(front_matter, input_path)
    claim_uuids, claim_uuids_minted = _mint_claim_uuids(front_matter)

    normalized = deepcopy(front_matter)
    normalized["paper_uuid"] = paper_uuid
    normalized["claim_uuids"] = claim_uuids
    if "status" in normalized:
        normalized["status"] = str(normalized["status"]).upper()
    if paper_uuid_minted:
        normalized["_paper_uuid_minted"] = True
    if claim_uuids_minted:
        normalized["_claim_uuids_minted"] = claim_uuids_minted

    clean_title = str(normalized.get("clean_title", normalized.get("title", "companion")))
    filename = f"{paper_uuid}_{_sluggify(clean_title)}.md"
    output_path = output_dir / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(_render_companion(normalized, body), encoding="utf-8")

    index_path = output_dir / "index.json"
    _update_index(
        index_path,
        paper_uuid=paper_uuid,
        title=str(normalized.get("title", "")),
        status=str(normalized.get("status", "")),
        relative_path=output_path.relative_to(output_dir.parent),
        source_file=normalized.get("source_file"),
        claim_ids=list(normalized.get("claim_ids", [])),
    )

    return CompanionResult(
        output_path=output_path,
        paper_uuid=paper_uuid,
        title=str(normalized.get("title", "")),
        status=str(normalized.get("status", "")),
        claim_ids=list(normalized.get("claim_ids", [])),
        claim_uuids_minted=claim_uuids_minted,
        paper_uuid_minted=paper_uuid_minted,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publish a CKG companion to mothership/companions.")
    parser.add_argument("input", type=Path, help="Path to the CKG companion Markdown file.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("companions"),
        help="Directory to write the normalized companion and index.json (default: companions, i.e. mothership/companions when run from the mothership directory).",
    )
    args = parser.parse_args(argv)

    try:
        result = publish_companion(args.input.resolve(), args.output_dir.resolve())
    except CompanionValidationError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"Published: {result.output_path}")
    print(f"  paper_uuid: {result.paper_uuid} ({'minted' if result.paper_uuid_minted else 'existing'})")
    print(f"  title: {result.title}")
    print(f"  status: {result.status}")
    print(f"  claims: {len(result.claim_ids)} ({result.claim_uuids_minted} UUIDs minted)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
