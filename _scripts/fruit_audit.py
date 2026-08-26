r"""Score a paper or text against the Fruits of the Spirit diagnostic rubric.

This is a local API-style callable. It does not claim deep semantic judgment;
it returns a transparent first-pass scorecard with evidence snippets.

Usage:
  python _scripts/fruit_audit.py path\to\paper.md
  echo "paper text" | python _scripts/fruit_audit.py -
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


REPO = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO / "_vocab" / "fruit_audit_registry.json"


@dataclass(frozen=True)
class FruitSpec:
    axiom_id: str
    name: str
    symbol: str
    fruit_class: str
    positive_markers: tuple[str, ...]
    negative_name: str
    negative_markers: tuple[str, ...]
    question: str


FRUITS: tuple[FruitSpec, ...] = (
    FruitSpec("AX-152", "Love", "L", "canonical-fruit", ("love", "sacrificial", "neighbor", "other", "service", "communion", "restore", "healing"), "Hatred", ("hate", "hatred", "contempt", "enemy", "dehuman", "revenge", "despise"), "Does the paper preserve the dignity and good of the other?"),
    FruitSpec("AX-153", "Joy", "J", "canonical-fruit", ("joy", "delight", "gratitude", "resilience", "celebrate", "glad"), "Despair", ("despair", "hopeless", "nihil", "meaningless", "fatalism", "despond"), "Does the paper produce durable gladness rather than collapse into despair?"),
    FruitSpec("AX-154", "Peace", "P", "canonical-fruit", ("peace", "reconcile", "harmony", "stability", "equilibrium", "nonviolent", "rest"), "Conflict", ("conflict", "anxiety", "panic", "fear", "threat", "terror", "agitation"), "Does the paper reduce contradiction and disorder rather than amplify conflict?"),
    FruitSpec("AX-155", "Patience", "Pa", "canonical-fruit", ("patience", "long-suffering", "endurance", "delayed", "wait", "slow", "time horizon", "persever"), "Impatience", ("impatient", "impatience", "rush", "instant", "reactionary", "short-term", "impulsive"), "Does the paper honor time, process, and delayed fruit?"),
    FruitSpec("AX-156", "Kindness", "K", "canonical-fruit", ("kindness", "mercy", "generous", "gentle help", "care", "compassion", "hospitality"), "Cruelty", ("cruel", "cruelty", "mock", "punish", "humiliate", "extract", "exploit"), "Does the paper export coherence to others at cost to itself?"),
    FruitSpec("AX-157", "Goodness", "Go", "canonical-fruit", ("goodness", "truth", "integrity", "justice", "right", "honest", "repair", "virtue"), "Corruption", ("corrupt", "corruption", "deceive", "lie", "manipulate", "bribe", "rot", "fraud"), "Does the paper align action with truth and repair?"),
    FruitSpec("AX-158", "Faithfulness", "Fa", "canonical-fruit", ("faithful", "faithfulness", "covenant", "promise", "commitment", "loyal", "steadfast", "trustworthy"), "Betrayal", ("betray", "betrayal", "abandon", "treachery", "unfaithful", "break promise", "disloyal"), "Does the paper keep covenantal consistency across time?"),
    FruitSpec("AX-159", "Gentleness", "Ge", "canonical-fruit", ("gentle", "gentleness", "meek", "calibrated", "humble", "noncoercive", "tender", "restrained"), "Harshness", ("harsh", "harshness", "coerce", "coercive", "dominate", "brutal", "threaten", "violent"), "Does the paper calibrate force to necessity?"),
    FruitSpec("AX-160", "Self-Control", "S", "canonical-fruit", ("self-control", "self_control", "discipline", "restraint", "sober", "temperance", "govern", "regulated"), "Indulgence", ("indulgence", "addiction", "compulsion", "enslaved", "impulse", "uncontrolled", "driven", "obsession"), "Does the paper show governed agency rather than impulse dominance?"),
    FruitSpec("AX-150", "Grace", "G", "companion-fruit", ("grace", "mercy", "gift", "forgive", "forgiveness", "external input", "restore", "unearned"), "Self-Sufficiency", ("self-sufficient", "self saved", "works suffice", "earn salvation", "merit alone", "closed system"), "Does the paper name the source of repair without pretending the closed system saves itself?"),
    FruitSpec("AX-151", "Hope", "H", "companion-fruit", ("hope", "hoped", "hopeful", "promise", "future", "resurrection", "renewal", "not yet"), "Despair", ("despair", "hopeless", "nihil", "meaningless", "fatalism", "despond"), "Does the paper open a durable future rather than merely diagnose collapse?"),
    FruitSpec("AX-066a", "Humility", "Hu", "companion-fruit", ("humility", "humble", "repent", "teachability", "receive", "confess", "listen", "submitted"), "Pride", ("pride", "arrogant", "boast", "dominate", "self-exalt", "unaccountable", "superior"), "Does the paper stay correctable under truth rather than using the framework to exalt itself?"),
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def snippets(text: str, markers: Iterable[str], limit: int = 4) -> list[str]:
    out: list[str] = []
    for marker in markers:
        match = re.search(r"\b" + re.escape(marker.lower()) + r"\b", text.lower())
        if not match:
            continue
        start = match.start()
        left = max(0, start - 80)
        right = min(len(text), start + len(marker) + 100)
        out.append(normalize(text[left:right]))
        if len(out) >= limit:
            break
    return out


def marker_count(text: str, markers: Iterable[str]) -> int:
    low = text.lower()
    total = 0
    for marker in markers:
        total += len(re.findall(r"\b" + re.escape(marker.lower()) + r"\b", low))
    return total


def dependencies_for(axiom_id: str) -> list[str]:
    deps = [
        f"tp:axioms/01/{axiom_id}",
        "tp:axioms/01/AX-151",
        "tp:master-equation/01/ME-EQ-009",
        "tp:master-equation/01/ME-EQ-010",
    ]
    return list(dict.fromkeys(deps))


def score_one(text: str, spec: FruitSpec) -> dict:
    pos = marker_count(text, spec.positive_markers)
    neg = marker_count(text, spec.negative_markers)
    raw = pos - neg
    # Transparent, conservative normalization. 0.5 is neutral.
    score = max(0.0, min(1.0, 0.5 + raw / 10.0))
    if score >= 0.7:
        verdict = "fruit-dominant"
    elif score <= 0.3:
        verdict = "anti-fruit-risk"
    else:
        verdict = "mixed-or-unclear"
    return {
        "fruit": spec.name,
        "symbol": spec.symbol,
        "fruitClass": spec.fruit_class,
        "axiomID": spec.axiom_id,
        "antiFruit": spec.negative_name,
        "question": spec.question,
        "score": round(score, 3),
        "positiveHits": pos,
        "negativeHits": neg,
        "verdict": verdict,
        "positiveEvidence": snippets(text, spec.positive_markers),
        "negativeEvidence": snippets(text, spec.negative_markers),
        "dependsOn": dependencies_for(spec.axiom_id),
    }


def audit(text: str, source: str) -> dict:
    results = [score_one(text, spec) for spec in FRUITS]
    avg = sum(r["score"] for r in results) / len(results)
    minimum = min(r["score"] for r in results)
    collapse = [r["fruit"] for r in results if r["score"] <= 0.3]
    return {
        "auditType": "fruit-of-the-spirit-paper-audit",
        "version": "0.1.0",
        "date": date.today().isoformat(),
        "source": source,
        "modelBoundary": "transparent lexical first pass; use as triage, not final moral judgment",
        "overallFruitScore": round(avg, 3),
        "minimumFruitScore": round(minimum, 3),
        "collapseFlags": collapse,
        "verdict": "passes-first-fruit-gate" if not collapse and avg >= 0.55 else "needs-human-review",
        "results": results,
    }


def write_registry() -> None:
    REGISTRY_PATH.write_text(
        json.dumps(
            {
                "generatedAt": date.today().isoformat(),
                "callable": "_scripts/fruit_audit.py",
                "stdinContract": "Pass '-' as the path and pipe text on stdin.",
                "fileContract": "Pass a local paper path as argv[1].",
                "output": "JSON scorecard with one row per fruit.",
                "boundary": "Canonical Fruits of the Spirit plus companion Theophysics virtues. Duplicate fruit labels found in anti-fruit source lists are intentionally excluded from anti-fruit scoring.",
                "dependsOn": ["tp:axioms/01/AX-151", "tp:master-equation/01/ME-EQ-009", "tp:master-equation/01/ME-EQ-010"],
                "fruits": [
                    {
                        "name": spec.name,
                        "symbol": spec.symbol,
                        "fruitClass": spec.fruit_class,
                        "axiomID": spec.axiom_id,
                        "antiFruit": spec.negative_name,
                        "question": spec.question,
                        "positiveMarkers": list(spec.positive_markers),
                        "negativeMarkers": list(spec.negative_markers),
                    }
                    for spec in FRUITS
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    write_registry()
    if len(sys.argv) < 2:
        print(f"Wrote registry to {REGISTRY_PATH}")
        print("Pass a file path, or '-' to read paper text from stdin.")
        return 0

    source = sys.argv[1]
    if source == "-":
        text = sys.stdin.read()
    else:
        text = Path(source).read_text(encoding="utf-8")
    print(json.dumps(audit(text, source), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
