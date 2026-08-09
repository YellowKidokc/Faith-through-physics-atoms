import re
from html.parser import HTMLParser
from pathlib import Path

from .models import Finding, ScanResult
from .normalize import EMOJI, MOJIBAKE, normalize_equation
from .score import score_candidate


EQUATION_CUE = re.compile(r"(?:χ|chi|\\chi|dchi|L\s*=|E\s*=\s*Energy)", re.I)
FENCE = re.compile(r"^\s*(```|~~~)")
RAW_START = re.compile(r"(?:<!--\s*(?:raw|exact)-fragment:start\s*-->|\[!(?:raw|exact)-fragment\])", re.I)
RAW_END = re.compile(r"<!--\s*(?:raw|exact)-fragment:end\s*-->", re.I)


def infer_context(path, lines):
    joined = " ".join(lines[:40]).lower()
    value = str(path).lower() + " " + joined
    if "raw_fragment" in value or "raw fragment" in value: return "raw_fragment"
    if any(x in value for x in ("11_articles", "story", "dialogue", "character")): return "story"
    if any(x in value for x in ("01_canonical", "canonical", "canon summary")): return "canon"
    if any(x in value for x in ("09_everyday", "12_audience", "public teaching")): return "public"
    return "unknown"


def _encoding_findings(path, line, number, context):
    out = []
    for kind, regex in (("mojibake", MOJIBAKE), ("emoji", EMOJI)):
        for match in regex.finditer(line):
            out.append(Finding(str(path), number, match.start()+1, context, kind, match.group(),
                confidence=1.0, distancePoints=0, suggestedAction="flag_only",
                reason=f"detected {kind}; normalization requires human review"))
    return out


def scan_text(path, registry, scan_code=False, html_context=False):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    base_context = "html" if html_context else infer_context(path, lines)
    findings, fenced, raw = [], False, False
    for number, line in enumerate(lines, 1):
        if not html_context and FENCE.match(line):
            fenced = not fenced
            continue
        if RAW_START.search(line): raw = True
        context = "raw_fragment" if raw else "code" if fenced else base_context
        findings.extend(_encoding_findings(path, line, number, context))
        if (fenced and not scan_code) or (line.lstrip().startswith(">") and not raw):
            if RAW_END.search(line): raw = False
            continue
        if EQUATION_CUE.search(line):
            candidates = []
            for retired in registry.retired:
                # Exact forms may be embedded in prose; fuzzy scoring uses the complete line.
                probe = retired["pattern"] if normalize_equation(retired["pattern"]) in normalize_equation(line) else line.strip()
                scored = score_candidate(probe, retired, context, registry.rules)
                if scored["action"] != "ignore": candidates.append((scored["confidence"], retired, scored, probe))
            if candidates:
                _, retired, scored, probe = max(candidates, key=lambda item: item[0])
                column = max(1, line.lower().find(probe.lower()) + 1)
                replacement = retired.get("replacementText", "")
                proposed = replacement if scored["action"] in {"auto_fix", "propose_patch"} else ""
                findings.append(Finding(str(path), number, column, context, "retired_equation", probe,
                    retired["canonicalReplacement"], scored["confidence"], scored["distance"], scored["action"],
                    proposed, scored["ruling"], scored["reason"], scored["protected"], retired["id"]))
        if RAW_END.search(line): raw = False
    return findings


class VisibleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts = []
        self.special = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style", "code", "pre"}:
            self.skip += 1
            if tag == "script" and any(x in (attrs.get("type", "") + attrs.get("src", "")).lower() for x in ("mathjax", "katex", "math/tex")):
                self.special.append((self.getpos(), "MathJax/KaTeX script requires separate review"))
        if tag == "img" and any(x in (attrs.get("alt", "") + attrs.get("src", "")).lower() for x in ("equation", "chi", "master")):
            self.images.append((self.getpos(), attrs.get("alt", "") or attrs.get("src", "")))

    def handle_endtag(self, tag):
        if tag in {"script", "style", "code", "pre"} and self.skip: self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip(): self.parts.append((self.getpos(), data))


def scan_html(path, registry):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    parser = VisibleHTMLParser(); parser.feed(raw)
    findings = []
    for (line, col), data in parser.parts:
        # Preserve DOM boundaries: scan each visible text node independently.
        for finding in scan_fragment(path, data, line, col, registry): findings.append(finding)
    for (line, col), detail in parser.special + parser.images:
        findings.append(Finding(str(path), line, col+1, "html", "html_render_drift", detail,
            confidence=.75, distancePoints=25, suggestedAction="flag_only",
            reason="rendered equation asset or math script can drift independently"))
    return findings


def scan_fragment(path, text, line, col, registry):
    findings = _encoding_findings(path, text, line, "html")
    if EQUATION_CUE.search(text):
        candidates = []
        for retired in registry.retired:
            probe = retired["pattern"] if normalize_equation(retired["pattern"]) in normalize_equation(text) else text.strip()
            score = score_candidate(probe, retired, "html", registry.rules)
            if score["action"] != "ignore": candidates.append((score["confidence"], retired, score, probe))
        if candidates:
            _, retired, score, probe = max(candidates, key=lambda x:x[0])
            findings.append(Finding(str(path), line, col+1, "html", "retired_equation", probe,
                retired["canonicalReplacement"], score["confidence"], score["distance"], score["action"],
                retired.get("replacementText", ""), True, score["reason"], False, retired["id"]))
    return findings


def iter_documents(target, extensions):
    target = Path(target)
    if target.is_file():
        if target.suffix.lower() in extensions: yield target
    elif target.is_dir():
        for path in sorted(target.rglob("*")):
            if path.is_file() and path.suffix.lower() in extensions and ".git" not in path.parts:
                yield path


def scan_path(target, registry, extensions=None, scan_code=False):
    extensions = extensions or {".md", ".txt", ".html", ".htm"}
    findings, count = [], 0
    for path in iter_documents(target, extensions):
        count += 1
        findings.extend(scan_html(path, registry) if path.suffix.lower() in {".html", ".htm"} else scan_text(path, registry, scan_code))
    return ScanResult(count, findings)
