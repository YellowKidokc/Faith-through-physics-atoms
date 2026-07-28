"""Build a fast JSON index from Folder Beacon v2 ``.fisnote`` files."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from folder_beacon import INDEX_SCHEMA, discover, read_beacon, validate_beacon

INDEX_FIELDS = (
    "folder_id", "folder", "name", "short_name", "display_name",
    "folder_class", "status", "contains", "provides", "needs",
    "looking_for", "search_tokens", "allowed_actions", "forbidden_actions",
    "batch_tags", "page_ids", "slugs",
)


def scan(roots: list[Path], max_bytes: int = 65536) -> dict:
    folders, errors = [], []
    for root in roots:
        for path in discover(root):
            try:
                beacon, _ = read_beacon(path, max_bytes=max_bytes)
                problems = validate_beacon(beacon)
                if problems:
                    raise ValueError("; ".join(problems))
                record = {key: beacon[key] for key in INDEX_FIELDS if key in beacon}
                record["path"] = str(path.parent.resolve())
                folders.append(record)
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append({"file": str(path), "error": str(exc)})
    folders.sort(key=lambda item: (item["path"].lower(), item["folder_id"]))
    return {
        "schema": INDEX_SCHEMA,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "roots": [str(root.resolve()) for root in roots],
        "folders": folders,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="*", type=Path, default=[Path.cwd()])
    parser.add_argument("-o", "--output", type=Path, default=Path("folder_beacon_index.json"))
    parser.add_argument("--max-bytes", type=int, default=65536)
    args = parser.parse_args()
    result = scan(args.roots, args.max_bytes)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"indexed {len(result['folders'])}; errors {len(result['errors'])}; wrote {args.output}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
