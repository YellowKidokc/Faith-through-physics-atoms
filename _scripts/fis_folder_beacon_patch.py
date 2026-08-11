"""Safely apply JSONL batch patches to Folder Beacon v2 front matter."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from folder_beacon import LIST_FIELDS, discover, dump_front_matter, read_beacon, validate_beacon

OPS = {"set", "add_unique", "remove_value", "replace_value", "append_tag", "mark_needs_review"}


def matches(data: dict[str, Any], selector: dict[str, Any]) -> bool:
    for field, expected in selector.items():
        actual = data.get(field)
        if isinstance(expected, list):
            if not isinstance(actual, list) or not all(item in actual for item in expected):
                return False
        elif actual != expected:
            return False
    return True


def apply_operation(data: dict[str, Any], patch: dict[str, Any]) -> bool:
    op = patch.get("op")
    if op not in OPS:
        raise ValueError(f"unsupported operation: {op!r}")
    field = patch.get("field")
    if op == "append_tag":
        field = "batch_tags"
    elif op == "mark_needs_review":
        field, patch = "status", {**patch, "value": "needs_review"}
        op = "set"
    if not isinstance(field, str):
        raise ValueError(f"operation {op!r} requires a field")
    before = copy.deepcopy(data.get(field))
    if op == "set":
        data[field] = patch.get("value")
    elif op in {"add_unique", "append_tag"}:
        values = data.setdefault(field, [])
        if not isinstance(values, list):
            raise ValueError(f"{field} is not a list")
        if patch.get("value") not in values:
            values.append(patch.get("value"))
    elif op == "remove_value":
        if not isinstance(before, list):
            raise ValueError(f"{field} is not a list")
        data[field] = [value for value in before if value != patch.get("value")]
    elif op == "replace_value":
        if not isinstance(before, list):
            raise ValueError(f"{field} is not a list")
        if "old_value" not in patch or "value" not in patch:
            raise ValueError("replace_value requires old_value and value")
        data[field] = [patch["value"] if value == patch["old_value"] else value for value in before]
    if field in LIST_FIELDS and not isinstance(data.get(field), list):
        raise ValueError(f"{field} must remain a list")
    return before != data.get(field)


def load_patches(path: Path) -> list[dict[str, Any]]:
    patches = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            patch = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on patch line {number}: {exc}") from exc
        if "selector" not in patch:
            raise ValueError(f"patch line {number} requires an explicit selector")
        if not isinstance(patch["selector"], dict):
            raise ValueError(f"selector on patch line {number} must be an object")
        patches.append(patch)
    return patches


def patch_beacons(roots: list[Path], patches: list[dict[str, Any]], dry_run: bool = False) -> dict:
    for index, patch in enumerate(patches, 1):
        if "selector" not in patch:
            raise ValueError(f"patch {index} requires an explicit selector")
        if not isinstance(patch["selector"], dict):
            raise ValueError(f"selector for patch {index} must be an object")

    report: dict[str, Any] = {"changed": [], "skipped": [], "errors": []}
    for path in sorted({path for root in roots for path in discover(root)}):
        try:
            original = path.read_text(encoding="utf-8")
            data, body = read_beacon(path)
            problems = validate_beacon(data)
            if problems:
                raise ValueError("; ".join(problems))
            applied = []
            for index, patch in enumerate(patches, 1):
                if matches(data, patch["selector"]) and apply_operation(data, patch):
                    applied.append(index)
            problems = validate_beacon(data)
            if problems:
                raise ValueError("patch produced invalid beacon: " + "; ".join(problems))
            updated = dump_front_matter(data, body)
            if not applied or updated == original:
                report["skipped"].append(str(path))
                continue
            entry = {
                "file": str(path), "operations": applied,
                "before_sha256": hashlib.sha256(original.encode()).hexdigest(),
                "after_sha256": hashlib.sha256(updated.encode()).hexdigest(),
            }
            report["changed"].append(entry)
            if not dry_run:
                temporary = path.with_name(path.name + ".tmp")
                temporary.write_text(updated, encoding="utf-8")
                temporary.replace(path)
        except (OSError, UnicodeError, ValueError) as exc:
            report["errors"].append({"file": str(path), "error": str(exc)})
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("patch_file", type=Path)
    parser.add_argument("roots", nargs="*", type=Path, default=[Path.cwd()])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report", type=Path, default=Path("folder_beacon_patch_report.json"))
    parser.add_argument("--ledger", type=Path, default=Path("folder_beacon_patch_ledger.jsonl"))
    args = parser.parse_args()
    report = patch_beacons(args.roots, load_patches(args.patch_file), args.dry_run)
    report.update({"schema": "folder-beacon-patch-report.v1", "created_at": datetime.now(timezone.utc).isoformat(), "dry_run": args.dry_run})
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not args.dry_run and report["changed"]:
        with args.ledger.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(report, ensure_ascii=False) + "\n")
    print(f"changed {len(report['changed'])}; skipped {len(report['skipped'])}; errors {len(report['errors'])}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
