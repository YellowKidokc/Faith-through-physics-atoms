"""Harvest CKG companion outputs and convert them into mothership pills.

Each CKG companion is a Markdown file with YAML frontmatter plus a structured
body.  This script extracts the face fields (paper identity, grade, source hash)
and key veins (claims, domains, headings, provider/model) and writes one thin
.pill.yaml per companion into the mothership pills tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


# Deliberately simple Markdown frontmatter parser: we expect `---` fences.
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
# Extract the first level-1 heading as the companion title.
_H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
# Extract a fenced YAML/JSON block under ## Source.
_SOURCE_BLOCK_RE = re.compile(
    r"## Source\s*\n+```(?:ya?ml|json)\s*\n(.*?)\n```",
    re.DOTALL | re.IGNORECASE,
)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _normalize_newlines(text: str) -> str:
    """Convert all line endings to LF for uniform parsing."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter_dict, body)."""
    text = _normalize_newlines(text)
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    try:
        front = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        front = {}
    return front, match.group(2)


def _extract_source_yaml(body: str) -> dict[str, Any]:
    """Look for a fenced YAML/JSON block under ## Source."""
    match = _SOURCE_BLOCK_RE.search(body)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _extract_sections(body: str) -> dict[str, str]:
    """Return a dict of section titles to section bodies.

    Line-based parser so that very large companions don't defeat a single
    regex and so that subtitle-style headings inside the Source block are
    still captured.
    """
    sections: dict[str, str] = {}
    lines = body.splitlines()
    heading_re = re.compile(r"^(#{2,3})\s+(.+)$")

    current_title: str | None = None
    current_lines: list[str] = []
    for line in lines:
        match = heading_re.match(line)
        if match:
            if current_title is not None:
                cleaned = "\n".join(current_lines).strip()
                if cleaned:
                    sections[current_title.strip()] = cleaned
            current_title = match.group(2)
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        cleaned = "\n".join(current_lines).strip()
        if cleaned:
            sections[current_title.strip()] = cleaned

    return sections


def _slugify(name: str) -> str:
    """Make a filesystem-safe slug."""
    name = name.lower().replace(" ", "_").replace("-", "_")
    return re.sub(r"[^a-z0-9_]", "", name)[:80]


def convert_companion(
    source_path: Path,
    input_root: Path,
    output_root: Path,
) -> tuple[Path | None, list[str]]:
    """Convert one CKG companion Markdown file into a YAML pill."""
    errors: list[str] = []

    try:
        text = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"Read error for {source_path}: {exc}"]

    front, body = _parse_frontmatter(text)
    if not front:
        errors.append(f"No frontmatter found in {source_path}; using empty face.")

    paper_uuid = front.get("paper_uuid")
    source_hash = front.get("source_hash")
    source_path_raw = front.get("source_path")
    grade = front.get("grade", "UNSCORED")
    model = front.get("model")
    provider = front.get("provider")

    title_match = _H1_RE.search(body)
    title = title_match.group(1).strip() if title_match else source_path.stem

    source_yaml = _extract_source_yaml(body)
    sections = _extract_sections(body)

    face: dict[str, Any] = {
        "uuid": paper_uuid,
        "name": title,
        "target_type": "paper_companion",
        "status": grade.lower() if isinstance(grade, str) else grade,
    }
    if source_path_raw:
        face["source_path_raw"] = source_path_raw

    source_block: dict[str, Any] = {}
    if paper_uuid:
        source_block["doc_uuid"] = paper_uuid
    if source_hash:
        source_block["doc_sha256"] = source_hash
    if source_block:
        face["source"] = source_block

    # Drop None values for a clean face.
    face = {k: v for k, v in face.items() if v is not None}

    veins: dict[str, Any] = {
        "ckg_frontmatter": front,
        "source_yaml": source_yaml,
        "sections": sections,
    }
    if model:
        veins["model"] = model
    if provider:
        veins["provider"] = provider

    relative_stem = source_path.relative_to(input_root).with_suffix("")
    output_path = output_root / relative_stem.with_suffix(".pill.yaml")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pill = {
        "face": face,
        "veins": veins,
        "_metadata": {
            "source_path": str(source_path.relative_to(input_root).as_posix()),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "sha256": _sha256_file(source_path),
        },
    }

    with output_path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(pill, fh, sort_keys=False, allow_unicode=True)

    return output_path, errors


def run_conversion(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Harvest all CKG companion Markdown files into pills."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir_resolved = output_dir.resolve()

    pills_created = 0
    errors: list[str] = []

    for source_path in sorted(input_dir.rglob("*.md")):
        if output_dir_resolved in source_path.resolve().parents or source_path.resolve() == output_dir_resolved:
            continue

        output_path, errs = convert_companion(source_path, input_dir, output_dir)
        errors.extend(errs)
        if output_path is not None:
            pills_created += 1

    return {
        "pills_created": pills_created,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert CKG companion Markdown outputs into mothership pills."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path(r"\\192.168.2.50\h_hp\Desktop\APIs\APIs\CKG\OUTBOX\01_ALL_PAPERS"),
        help="Directory containing CKG companion .md files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "pills" / "ckg_companions",
        help="Directory to write .pill.yaml files.",
    )
    args = parser.parse_args(argv)

    summary = run_conversion(args.input_dir.resolve(), args.output_dir.resolve())
    print(json.dumps(summary, indent=2))
    return 0 if not summary["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
