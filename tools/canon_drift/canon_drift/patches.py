import difflib
from collections import defaultdict
from pathlib import Path


def proposed_patches(findings, threshold=.80):
    """Return unified diffs; protected and uncertain findings are never rewritten."""
    grouped = defaultdict(list)
    for finding in findings:
        if (finding.proposedPatch and not finding.protected and finding.confidence >= threshold
                and finding.suggestedAction in {"auto_fix", "propose_patch"}):
            grouped[finding.file].append(finding)
    output = []
    for filename, items in grouped.items():
        path = Path(filename); original = path.read_text(encoding="utf-8").splitlines(keepends=True); changed = list(original)
        for finding in sorted(items, key=lambda f: (f.line, f.column), reverse=True):
            index = finding.line - 1
            if 0 <= index < len(changed) and finding.matchedText in changed[index]:
                changed[index] = changed[index].replace(finding.matchedText, finding.proposedPatch, 1)
        diff = difflib.unified_diff(original, changed, fromfile=str(path), tofile=str(path)+".proposed")
        output.extend(diff)
    return "".join(output)


def apply_safe(findings, threshold=.95):
    """Apply only registry-approved auto-fixes and return changed file names."""
    grouped = defaultdict(list)
    for finding in findings:
        if finding.suggestedAction == "auto_fix" and not finding.requiresHumanRuling and not finding.protected and finding.confidence >= threshold:
            grouped[finding.file].append(finding)
    changed_files = []
    for filename, items in grouped.items():
        path = Path(filename); lines = path.read_text(encoding="utf-8").splitlines(keepends=True); changed = False
        for finding in sorted(items, key=lambda f:(f.line, f.column), reverse=True):
            i = finding.line-1
            if 0 <= i < len(lines) and finding.matchedText in lines[i]:
                lines[i] = lines[i].replace(finding.matchedText, finding.proposedPatch, 1); changed = True
        if changed: path.write_text("".join(lines), encoding="utf-8"); changed_files.append(filename)
    return changed_files
