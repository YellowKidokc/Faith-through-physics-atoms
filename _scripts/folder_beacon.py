"""Shared, dependency-free support for ``.fisnote`` folder beacons.

The intentionally small YAML reader supports the beacon vocabulary: mappings,
scalars, and scalar lists.  It does not attempt to be a general YAML parser.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SCHEMA = "folder-beacon.v2"
INDEX_SCHEMA = "folder-beacon-index.v1"
REQUIRED_FIELDS = (
    "fis_schema", "folder_id", "folder", "name", "short_name",
    "folder_class", "status", "contains", "provides", "needs",
    "looking_for", "search_tokens", "allowed_actions",
    "forbidden_actions", "batch_tags",
)
LIST_FIELDS = set(REQUIRED_FIELDS[7:]) | {"aliases", "page_ids", "slugs"}
FRONT_MATTER_END = re.compile(r"(?m)^---[ \t]*\r?$", re.MULTILINE)


class BeaconError(ValueError):
    """A malformed or unsupported beacon."""


def _scalar(text: str) -> Any:
    text = text.strip()
    if not text:
        return ""
    if text.startswith("["):
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            raise BeaconError(f"invalid inline list: {text}") from exc
        if not isinstance(value, list):
            raise BeaconError("only inline scalar lists are supported")
        return value
    if text[0:1] in {'"', "'"}:
        if text[0] == '"':
            try:
                return json.loads(text)
            except json.JSONDecodeError as exc:
                raise BeaconError(f"invalid quoted scalar: {text}") from exc
        if len(text) < 2 or not text.endswith("'"):
            raise BeaconError(f"invalid quoted scalar: {text}")
        return text[1:-1].replace("''", "'")
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    try:
        return float(text) if any(c in text for c in ".eE") else int(text)
    except ValueError:
        return text


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Return beacon data and the body, rejecting nested/complex YAML."""
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise BeaconError("missing YAML front matter at byte zero")
    data: dict[str, Any] = {}
    current_list: str | None = None
    end = None
    for index, raw in enumerate(lines[1:], 1):
        line = raw.rstrip("\r\n")
        if line.strip() == "---":
            end = index
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list is None:
                raise BeaconError(f"list item without field on line {index + 1}")
            data[current_list].append(_scalar(line[4:]))
            continue
        if line[:1].isspace() or ":" not in line:
            raise BeaconError(f"unsupported YAML on line {index + 1}")
        key, value = line.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key):
            raise BeaconError(f"invalid field name on line {index + 1}")
        if key in data:
            raise BeaconError(f"duplicate field {key!r}")
        if value.strip():
            data[key] = _scalar(value)
            current_list = None
        else:
            data[key] = []
            current_list = key
    if end is None:
        raise BeaconError("unterminated YAML front matter")
    return data, "".join(lines[end + 1:])


def read_beacon(path: Path, max_bytes: int | None = None) -> tuple[dict[str, Any], str]:
    """Read a beacon, optionally enforcing a fast-read byte ceiling."""
    if max_bytes is None:
        return parse_front_matter(path.read_text(encoding="utf-8"))
    with path.open("rb") as stream:
        chunk = stream.read(max_bytes)
    text = chunk.decode("utf-8-sig")
    try:
        return parse_front_matter(text)
    except BeaconError as exc:
        if "unterminated" in str(exc) and path.stat().st_size > max_bytes:
            raise BeaconError(f"front matter exceeds {max_bytes} byte scan limit") from exc
        raise


def validate_beacon(data: dict[str, Any]) -> list[str]:
    errors = [f"missing required field: {key}" for key in REQUIRED_FIELDS if key not in data]
    if data.get("fis_schema") != SCHEMA:
        errors.append(f"fis_schema must be {SCHEMA!r}")
    for key in LIST_FIELDS:
        if key in data and not isinstance(data[key], list):
            errors.append(f"{key} must be a list")
    return errors


def _quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def dump_front_matter(data: dict[str, Any], body: str) -> str:
    """Serialize supported values and retain the Markdown body byte-for-byte."""
    output = ["---\n"]
    for key, value in data.items():
        if isinstance(value, list):
            output.append(f"{key}:\n")
            output.extend(f"  - {_quoted(str(item))}\n" for item in value)
        elif isinstance(value, str):
            output.append(f"{key}: {_quoted(value)}\n")
        elif value is None:
            output.append(f"{key}: null\n")
        elif isinstance(value, bool):
            output.append(f"{key}: {str(value).lower()}\n")
        elif isinstance(value, (int, float)):
            output.append(f"{key}: {value}\n")
        else:
            raise BeaconError(f"unsupported value for {key!r}")
    output.append("---\n")
    output.append(body)
    return "".join(output)


def discover(root: Path) -> list[Path]:
    return sorted(root.rglob(".fisnote"), key=lambda path: path.as_posix().lower())
