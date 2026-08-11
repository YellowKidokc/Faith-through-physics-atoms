"""Turn a claim equation into a reviewable, plain-language translation node."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from adversarial_review import CompatibleClient, REPO

IDENTIFIER = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z][A-Za-z0-9_]*(?:_[A-Za-z0-9]+)?)(?![A-Za-z0-9_])")
OPERATORS = [("<=>", " exactly when "), ("=>", " leads to "), (">=", " at least "),
             ("<=", " at most "), ("!=", " differs from "), ("=", " equals "),
             (" + ", " plus "), (" - ", " minus "), (" * ", " times "), ("/", " per ")]


def find_claim(claim_id: str) -> tuple[Path, dict[str, Any]]:
    for path in REPO.rglob("*.jsonld"):
        if any(p in {"_vocab", "_protocol"} for p in path.parts):
            continue
        atom = json.loads(path.read_text(encoding="utf-8"))
        if claim_id in {atom.get("claimID"), atom.get("nodeID"), atom.get("@id")}:
            return path, atom
    raise ValueError(f"claim not found: {claim_id}")


def glossary_for(equation: str, supplied: dict[str, str] | None = None) -> dict[str, str]:
    supplied = supplied or {}
    identifiers = dict.fromkeys(IDENTIFIER.findall(equation))
    return {symbol: supplied.get(symbol, symbol.replace("_", " ")) for symbol in identifiers}


def word_equation(equation: str, glossary: dict[str, str]) -> str:
    text = IDENTIFIER.sub(lambda m: glossary.get(m.group(1), m.group(1)), equation)
    for operator, words in OPERATORS:
        text = text.replace(operator, words)
    return " ".join(text.split())


def local_translation(equation: str, glossary: dict[str, str]) -> dict[str, Any]:
    words = word_equation(equation, glossary)
    return {
        "symbolGlossary": glossary,
        "wordEquation": words,
        "explanations": [
            {"level": "plain", "text": f"Read the structure as: {words}."},
            {"level": "structural", "text": "Each operator states how the neighboring quantities relate; grouping and implication order must be preserved."},
        ],
        "analogies": [],
        "warnings": ["Symbol names were translated mechanically. Supply a glossary or use model review before publication."],
    }


def translation_prompt(equation: str, context: str, glossary: dict[str, str]) -> str:
    return f"""Translate the mathematical structure below without changing or solving it.
Return JSON only with: symbolGlossary (object; each value 1-2 words), wordEquation
(same ordering/grouping/operators as the equation), explanations (array of objects with
level and text; use plain, structural, and technical only as complexity requires), analogies
(one or two objects with title, text, and limits), warnings (array). Never add a theological,
causal, empirical, or uniqueness conclusion not entailed by the math. Explicitly explain
fractions, grouping, min/max, conditions, implications, and boundary assumptions when present.
Equation: {equation}
Known glossary: {json.dumps(glossary)}
Claim context: {context}"""


def normalize(raw: dict[str, Any], equation: str, glossary: dict[str, str]) -> dict[str, Any]:
    merged = {**glossary, **{str(k): str(v) for k, v in (raw.get("symbolGlossary") or {}).items()}}
    explanations = raw.get("explanations") or []
    return {"equation": equation, "equationMarkdown": f"$$\n{equation}\n$$",
            "symbolGlossary": merged, "wordEquation": str(raw.get("wordEquation") or word_equation(equation, merged)),
            "explanations": explanations[:3], "analogies": (raw.get("analogies") or [])[:2],
            "warnings": list(raw.get("warnings") or [])}


def translate(claim: dict[str, Any], provider: str = "local", endpoint: str = "", model: str = "",
              api_key: str = "", supplied_glossary: dict[str, str] | None = None) -> dict[str, Any]:
    equation = str(claim.get("mathematicalForm") or claim.get("mathFormNormal") or "").strip()
    if not equation:
        raise ValueError("claim has no mathematicalForm or mathFormNormal")
    glossary = glossary_for(equation, supplied_glossary)
    if provider == "compatible":
        if not endpoint or not model:
            raise ValueError("compatible provider requires endpoint and model")
        raw = CompatibleClient(endpoint, model, api_key).review(translation_prompt(
            equation, str(claim.get("statementTechnical") or ""), glossary))
    else:
        raw = local_translation(equation, glossary)
    return normalize(raw, equation, glossary)


def build_node(source: dict[str, Any], result: dict[str, Any], provider: str, model: str) -> dict[str, Any]:
    source_id = str(source.get("claimID") or source.get("nodeID") or source.get("@id"))
    digest = hashlib.sha256((source_id + result["equation"]).encode()).hexdigest()[:12]
    now = datetime.now(timezone.utc).isoformat()
    return {"@context": source.get("@context", ["https://faiththruphysics.com/vocab/context.jsonld"]),
            "@id": f"https://faiththruphysics.com/translations/math/{digest}",
            "nodeID": f"tp:translation/math/{digest}", "name": f"Math translation — {source.get('name', source_id)}",
            "nodeType": "translation", "domainType": source.get("domainType"), "stage": "09_everyday",
            "status": "proposed", "audienceLevel": "everyday", "dateCreated": now, "dateModified": now,
            "sourceClaim": source_id, "translationKind": "mathematical_structure", **result,
            "edges": [{"type": "dependsOn", "target": source_id, "propagates": False, "status": "proposed"}],
            "generationReceipt": {"provider": provider, "model": model or "deterministic-local-v1",
                                  "reviewStatus": "unreviewed", "generatedAt": now}}


def write_node(source_path: Path, node: dict[str, Any]) -> Path:
    domain_root = source_path
    while domain_root.parent != REPO and domain_root.parent != domain_root:
        domain_root = domain_root.parent
    folder = domain_root / "09_everyday"; folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{node['nodeID'].split('/')[-1]}-math-translation.jsonld"
    path.write_text(json.dumps(node, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def render_fragment(node: dict[str, Any]) -> str:
    explanations = "".join(f"<h3>{html.escape(str(x.get('level','Explanation')).title())}</h3><p>{html.escape(str(x.get('text','')))}</p>" for x in node["explanations"])
    analogies = "".join(f"<h3>{html.escape(str(x.get('title','Analogy')))}</h3><p>{html.escape(str(x.get('text','')))}</p><p><em>Limit: {html.escape(str(x.get('limits','')))}</em></p>" for x in node["analogies"])
    return f'<article class="math-translation"><div class="equation" style="text-align:center;font-size:2em;margin:1.5em">{html.escape(node["equation"])}</div><div class="word-equation" style="text-align:center;font-size:1.35em">{html.escape(node["wordEquation"])}</div>{explanations}{analogies}</article>'


def main() -> None:
    p = argparse.ArgumentParser(description="Generate a draft math translation node")
    p.add_argument("--claim-id", required=True); p.add_argument("--provider", choices=("local", "compatible"), default="local")
    p.add_argument("--endpoint", default=os.getenv("MATH_TRANSLATION_API_URL", "")); p.add_argument("--model", default=os.getenv("MATH_TRANSLATION_MODEL", ""))
    p.add_argument("--api-key", default=os.getenv("MATH_TRANSLATION_API_KEY", "")); p.add_argument("--glossary", help="JSON object of symbol-to-words")
    p.add_argument("--write", action="store_true"); p.add_argument("--html", action="store_true")
    args = p.parse_args(); path, claim = find_claim(args.claim_id)
    result = translate(claim, args.provider, args.endpoint, args.model, args.api_key, json.loads(args.glossary) if args.glossary else None)
    node = build_node(claim, result, args.provider, args.model)
    if args.write:
        output = write_node(path, node); print(output.relative_to(REPO))
        if args.html: output.with_suffix(".html").write_text(render_fragment(node), encoding="utf-8")
    else: print(json.dumps(node, indent=2, ensure_ascii=False))


if __name__ == "__main__": main()
