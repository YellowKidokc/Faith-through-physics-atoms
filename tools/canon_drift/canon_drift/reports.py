import json
from pathlib import Path

from .models import summarize


def json_report(result):
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False) + "\n"


def markdown_report(result):
    summary = summarize(result)
    lines = ["# Canon drift report", "", "## Summary", ""]
    for key, value in summary.items(): lines.append(f"- **{key}:** {value}")
    lines += ["", "## Findings", ""]
    if not result.findings: lines.append("No findings.")
    for f in result.findings:
        lines += [f"### {f.findingType}: `{f.file}:{f.line}:{f.column}`", "",
            f"- Context: `{f.contextType}`", f"- Confidence: `{f.confidence:.2f}` ({f.distancePoints} points off)",
            f"- Decision: `{f.suggestedAction}`", f"- Human ruling: `{'yes' if f.requiresHumanRuling else 'no'}`",
            f"- Protected: `{'yes' if f.protected else 'no'}`", f"- Match: `{f.matchedText}`", f"- Reason: {f.reason}", ""]
    return "\n".join(lines) + "\n"


def write_reports(result, output_prefix):
    prefix = Path(output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path, md_path = Path(str(prefix)+".json"), Path(str(prefix)+".md")
    json_path.write_text(json_report(result), encoding="utf-8")
    md_path.write_text(markdown_report(result), encoding="utf-8")
    return json_path, md_path
