#!/usr/bin/env python3
"""Build a Lean project, write a receipt, and optionally attach it to Lane 4."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import lane4_ledger


ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "_runtime" / "lean_receipts"
FORBIDDEN = {
    "sorry": re.compile(r"\bsorry\b"),
    "admit": re.compile(r"\badmit\b"),
    "axiom": re.compile(r"^\s*axiom\b", re.MULTILINE),
    "unsafe": re.compile(r"\bunsafe\b"),
    "trivial_true": re.compile(r"theorem\s+\S+[\s\S]{0,240}:\s*True\s*:=\s*(?:by\s*)?trivial"),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "lean-receipt"


def run_build(project: Path, command: list[str]) -> dict:
    started = now()
    proc = subprocess.run(
        command,
        cwd=project,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "started": started,
        "command": command,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def scan_lean_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    matches = {}
    for name, pattern in FORBIDDEN.items():
        hits = []
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            hits.append({"line": line, "text": match.group(0)[:160]})
        if hits:
            matches[name] = hits
    return {
        "path": str(path),
        "exists": path.exists(),
        "forbiddenMatches": matches,
        "ok": not matches,
    }


def write_receipt(
    *,
    title: str,
    project: Path,
    lean_file: Path,
    atom: str,
    build: dict,
    scan: dict,
    meaning: str,
    limits: str,
) -> tuple[Path, Path]:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{slug(title)}-{stamp}"
    md_path = RECEIPTS / f"{stem}.md"
    json_path = RECEIPTS / f"{stem}.json"
    status = "pass" if build["ok"] and scan["ok"] else "fail"
    payload = {
        "generatedAt": now(),
        "title": title,
        "status": status,
        "project": str(project),
        "leanFile": str(lean_file),
        "atom": atom,
        "build": build,
        "scan": scan,
        "meaning": meaning,
        "limits": limits,
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        f"# {title}",
        "",
        f"Generated: {payload['generatedAt']}",
        f"Status: **{status}**",
        "",
        "## Lean Artifact",
        "",
        f"`{lean_file}`",
        "",
        "## Project",
        "",
        f"`{project}`",
        "",
        "## Build",
        "",
        f"Command: `{' '.join(build['command'])}`",
        f"Return code: `{build['returncode']}`",
        "",
        "```text",
        build["stdout"] or build["stderr"] or "No build output.",
        "```",
        "",
        "## Integrity Scan",
        "",
        "Scanned for `sorry`, `admit`, top-level `axiom`, `unsafe`, and fake `theorem ... : True := trivial`.",
        "",
        f"Result: {'no forbidden matches' if scan['ok'] else 'forbidden matches found'}",
        "",
        "## Meaning",
        "",
        meaning,
        "",
        "## Limits",
        "",
        limits,
        "",
        "## Lane 4 Atom",
        "",
        f"`{atom}`",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path, json_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Lean and record a Lane 4 receipt.")
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--lean-file", required=True, type=Path)
    parser.add_argument("--atom", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--meaning", required=True)
    parser.add_argument("--limits", required=True)
    parser.add_argument("--reviewer", default="Codex")
    parser.add_argument("--build-command", nargs="+", default=["lake", "build"])
    parser.add_argument("--skip-attach", action="store_true")
    args = parser.parse_args()

    project = args.project.resolve()
    lean_file = args.lean_file.resolve()
    if not project.is_dir():
        raise SystemExit(f"project folder not found: {project}")
    if not lean_file.is_file():
        raise SystemExit(f"Lean file not found: {lean_file}")

    build = run_build(project, args.build_command)
    scan = scan_lean_file(lean_file)
    md_path, json_path = write_receipt(
        title=args.title,
        project=project,
        lean_file=lean_file,
        atom=args.atom,
        build=build,
        scan=scan,
        meaning=args.meaning,
        limits=args.limits,
    )

    attached = False
    if build["ok"] and scan["ok"] and not args.skip_attach:
        atom = lane4_ledger.get_atom(args.atom)
        lane4_ledger.append_event(
            atom,
            {
                "event_type": "test_run",
                "lane": "Lean4",
                "result": "pass",
                "artifact_path": str(md_path),
                "meaning": args.meaning,
                "limits": args.limits,
                "reviewer": args.reviewer,
            },
        )
        lane4_ledger.rebuild()
        attached = True

    print(str(md_path))
    print(str(json_path))
    print(f"build_ok={build['ok']}")
    print(f"scan_ok={scan['ok']}")
    print(f"attached={attached}")
    return 0 if build["ok"] and scan["ok"] else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
