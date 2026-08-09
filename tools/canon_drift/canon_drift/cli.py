import argparse
import json
import sys
from pathlib import Path

from .autolink import autolink_html, autolink_markdown
from .patches import apply_safe, proposed_patches
from .registry import Registry
from .reports import json_report, markdown_report, write_reports
from .scanner import iter_documents, scan_path


def parser():
    p = argparse.ArgumentParser(prog="canon-drift", description="Auditable canon drift scanner and conservative codemod")
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("scan", "report", "html-scan"):
        cmd = sub.add_parser(name); cmd.add_argument("path"); cmd.add_argument("--output")
    fix = sub.add_parser("fix"); fix.add_argument("path"); fix.add_argument("--dry-run", action="store_true"); fix.add_argument("--apply", action="store_true"); fix.add_argument("--threshold", type=float, default=.95); fix.add_argument("--patch")
    weekly = sub.add_parser("weekly"); weekly.add_argument("path"); weekly.add_argument("--markdown", action="store_true"); weekly.add_argument("--html", action="store_true"); weekly.add_argument("--json-report", action="store_true"); weekly.add_argument("--output", default="canon-drift-weekly")
    link = sub.add_parser("autolink"); link.add_argument("path"); link.add_argument("--dry-run", action="store_true"); link.add_argument("--apply", action="store_true"); link.add_argument("--first-use", choices=("page", "section"), default="section"); link.add_argument("--html", action="store_true")
    return p


def main(argv=None):
    args = parser().parse_args(argv); registry = Registry()
    if args.command == "autolink":
        proposals = []
        extensions = {".html", ".htm"} if args.html else {".md"}
        for path in iter_documents(args.path, extensions):
            if args.html: proposals.extend(autolink_html(path, registry.autolink_terms))
            else: proposals.extend(autolink_markdown(path, registry.autolink_terms, args.first_use, args.apply))
        print(json.dumps({"dryRun":not args.apply, "proposals":[p.to_dict() for p in proposals]}, indent=2)); return 0
    exts = {".html", ".htm"} if args.command == "html-scan" else None
    if args.command == "weekly" and (args.markdown or args.html):
        exts = set(); exts |= {".md", ".txt"} if args.markdown else set(); exts |= {".html", ".htm"} if args.html else set()
    result = scan_path(args.path, registry, exts)
    if args.command == "scan" or args.command == "html-scan": print(json_report(result), end="")
    elif args.command == "report":
        content = markdown_report(result); Path(args.output).write_text(content, encoding="utf-8") if args.output else print(content, end="")
    elif args.command == "weekly":
        paths = write_reports(result, args.output); patch = proposed_patches(result.findings); Path(args.output+".patch").write_text(patch, encoding="utf-8"); print(json.dumps({"reports":[str(x) for x in paths], "patch":args.output+".patch", **result.to_dict()["summary"]}, indent=2))
    elif args.command == "fix":
        patch = proposed_patches(result.findings, min(args.threshold, .80));
        if args.patch: Path(args.patch).write_text(patch, encoding="utf-8")
        else: print(patch, end="")
        if args.apply: print(json.dumps({"changed":apply_safe(result.findings, args.threshold)}))
    return 0


if __name__ == "__main__": raise SystemExit(main())
