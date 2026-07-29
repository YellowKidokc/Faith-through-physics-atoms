import re
from dataclasses import dataclass, asdict
from html import escape
from pathlib import Path

from .scanner import FENCE, RAW_END, RAW_START, VisibleHTMLParser, infer_context


@dataclass
class LinkProposal:
    file: str; line: int; column: int; term: str; canonId: str; targetURL: str
    context: str; alreadyLinked: bool; suggestedLink: str; risk: str; needsApproval: bool

    def to_dict(self): return asdict(self)


def _markdown_link(term): return f"{term['term']} [[{term['pillLabel']}:{term['canonId'].split('/')[-1]}]]"


def autolink_markdown(path, terms, first_use="section", apply=False):
    source = Path(path).read_text(encoding="utf-8"); lines = source.splitlines(keepends=True)
    seen, proposals, fenced, raw = set(), [], False, False
    for i, line in enumerate(lines):
        if FENCE.match(line): fenced = not fenced; continue
        if RAW_START.search(line): raw = True
        if re.match(r"^#{1,6}\s", line):
            if first_use == "section": seen.clear()
            continue
        if fenced or raw or line.lstrip().startswith(">"):
            if RAW_END.search(line): raw = False
            continue
        context = infer_context(path, lines)
        for term in terms:
            key = term["canonId"]
            if key in seen or context in term.get("blockedContexts", []): continue
            flags = 0 if term.get("caseSensitive") else re.I
            names = [term["term"], *term.get("aliases", [])]
            match = re.search(r"(?<![\w[])\b(?:"+"|".join(map(re.escape, names))+r")\b(?![^[]*\]\])", line, flags)
            if not match: continue
            already = "[[" in line[max(0, match.end()):match.end()+40] or "](" in line[match.end():match.end()+80]
            suggestion = _markdown_link(term)
            proposals.append(LinkProposal(str(path), i+1, match.start()+1, match.group(), key, term["proofURL"], context,
                already, suggestion, "low" if not term.get("requiresHumanApproval") else "medium", term.get("requiresHumanApproval", False)))
            seen.add(key)
            if apply and not already and not term.get("requiresHumanApproval"):
                lines[i] = line[:match.start()] + match.group() + " [[" + term["pillLabel"] + ":" + key.split("/")[-1] + "]]" + line[match.end():]
            break
        if RAW_END.search(line): raw = False
    if apply and "".join(lines) != source: Path(path).write_text("".join(lines), encoding="utf-8")
    return proposals


def html_pill(term):
    return (f'<a class="canon-pill" href="{escape(term["proofURL"])}" data-canon-id="{escape(term["canonId"])}" '
            f'title="{escape(term["tooltip"])}">{escape(term["display"])}</a>')


def autolink_html(path, terms):
    """Propose links for visible DOM text nodes; HTML mutation remains disabled."""
    parser = VisibleHTMLParser()
    parser.feed(Path(path).read_text(encoding="utf-8", errors="replace"))
    seen, proposals = set(), []
    for (line, col), text in parser.parts:
        for term in terms:
            if term["canonId"] in seen: continue
            flags = 0 if term.get("caseSensitive") else re.I
            names = [term["term"], *term.get("aliases", [])]
            match = re.search(r"\b(?:"+"|".join(map(re.escape, names))+r")\b", text, flags)
            if not match: continue
            proposals.append(LinkProposal(str(path), line, col+match.start()+1, match.group(), term["canonId"],
                term["proofURL"], "html", False, html_pill(term),
                "low" if not term.get("requiresHumanApproval") else "medium", term.get("requiresHumanApproval", False)))
            seen.add(term["canonId"])
    return proposals
