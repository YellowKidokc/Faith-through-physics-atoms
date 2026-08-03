"""Story Processing Rail — API-driven paragraph-level refinement.

Three passes:
  1. PUNCH    — flag paragraphs missing an unmistakable sentence; suggest one
  2. JARGON   — score jargon density; suggest plain-language swaps
  3. CITATION — thread historical/theological citations (Fathers, Scripture, ancients)

Usage:
  python story_rail.py punch  path/to/chapter.md [--apply]
  python story_rail.py jargon path/to/chapter.md [--apply]
  python story_rail.py cite   path/to/chapter.md [--apply]
  python story_rail.py all    path/to/chapter.md

Outputs a .story-review.json sidecar. With --apply, writes a new .refined.md.

Provider-neutral: set STORY_RAIL_ENDPOINT, STORY_RAIL_MODEL, STORY_RAIL_API_KEY.
Defaults to Anthropic API if ANTHROPIC_API_KEY is set.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]


def load_env():
    """Load .env from repo root if it exists. One place for all keys."""
    env_path = REPO / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                val = val.strip()
                if val and not os.getenv(key.strip()):
                    os.environ[key.strip()] = val


load_env()


# ── Config ──────────────────────────────────────────────────────────

def get_config() -> dict[str, str]:
    """Resolve API config. Priority: STORY_RAIL_* > DEEPSEEK_* > ANTHROPIC_* > OPENAI_*.
    Default engine is DeepSeek — cheapest and fast enough for paragraph scoring."""
    endpoint = os.getenv("STORY_RAIL_ENDPOINT", "")
    model = os.getenv("STORY_RAIL_MODEL", "")
    api_key = os.getenv("STORY_RAIL_API_KEY", "")
    # DeepSeek first — default engine for story rail
    if not endpoint:
        ak = os.getenv("DEEPSEEK_API_KEY", "")
        if ak:
            endpoint = "https://api.deepseek.com/v1/chat/completions"
            model = model or "deepseek-chat"
            api_key = ak
    if not endpoint:
        ak = os.getenv("ANTHROPIC_API_KEY", "")
        if ak:
            endpoint = "https://api.anthropic.com/v1/messages"
            model = model or "claude-sonnet-4-6"
            api_key = ak
    if not endpoint:
        ak = os.getenv("OPENAI_API_KEY", "")
        if ak:
            endpoint = "https://api.openai.com/v1/chat/completions"
            model = model or "gpt-4o"
            api_key = ak
    return {"endpoint": endpoint, "model": model, "api_key": api_key}


def get_thinking_config() -> dict[str, str]:
    """Config specifically for DeepSeek R1 thinking mode — used for jargon pass."""
    ak = os.getenv("DEEPSEEK_API_KEY", "")
    if ak:
        return {
            "endpoint": "https://api.deepseek.com/v1/chat/completions",
            "model": "deepseek-reasoner",
            "api_key": ak,
        }
    # Fallback to standard config if no DeepSeek key
    return get_config()


def is_anthropic(endpoint: str) -> bool:
    return "anthropic.com" in endpoint


def is_deepseek(endpoint: str) -> bool:
    return "deepseek.com" in endpoint


# ── API Call ────────────────────────────────────────────────────────

def call_api(prompt: str, system: str, cfg: dict[str, str], timeout: int = 90) -> str:
    """Send a prompt to the configured LLM endpoint. Returns raw text response."""
    if is_anthropic(cfg["endpoint"]):
        body = json.dumps({
            "model": cfg["model"],
            "max_tokens": 4096,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }).encode()
        headers = {
            "Content-Type": "application/json",
            "x-api-key": cfg["api_key"],
            "anthropic-version": "2023-06-01",
        }
    else:
        body = json.dumps({
            "model": cfg["model"],
            "temperature": 0.3,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }).encode()
        headers = {"Content-Type": "application/json"}
        if cfg["api_key"]:
            headers["Authorization"] = f"Bearer {cfg['api_key']}"

    req = urllib.request.Request(cfg["endpoint"], data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.load(resp)

    if is_anthropic(cfg["endpoint"]):
        return payload["content"][0]["text"]
    else:
        return payload["choices"][0]["message"]["content"]


# ── Paragraph Splitter ──────────────────────────────────────────────

def split_paragraphs(text: str) -> list[dict[str, Any]]:
    """Split markdown into paragraphs, preserving headers and structure."""
    blocks = []
    current = []
    for line in text.split("\n"):
        if line.strip() == "" and current:
            blocks.append("\n".join(current))
            current = []
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current))

    result = []
    for i, block in enumerate(blocks):
        stripped = block.strip()
        is_header = stripped.startswith("#")
        is_meta = stripped.startswith("---") or stripped.startswith(">") or stripped.startswith("*[")
        is_prose = not is_header and not is_meta and len(stripped) > 40
        result.append({
            "index": i,
            "text": block,
            "type": "header" if is_header else "meta" if is_meta else "prose" if is_prose else "short",
        })
    return result


# ── Pass 1: PUNCH ───────────────────────────────────────────────────

PUNCH_SYSTEM = """You are a prose editor for a narrative that retells the Bible through information theory and physics simulation. The voice is literary, precise, and theological without being preachy.

Your job: evaluate whether this paragraph contains an UNMISTAKABLE SENTENCE — a line compressed enough that a reader cannot skim past it. Examples from this series:
- "The sacrifice IS the repair."
- "Contact is the mechanism. Not will."
- "The clean thing was becoming broken so the broken things could become clean."

Respond in JSON only:
{
  "has_punch": true/false,
  "existing_punch": "the sentence if it exists, or null",
  "suggested_punch": "a candidate sentence if missing, or null",
  "confidence": 0.0-1.0,
  "note": "brief explanation"
}"""

def run_punch(paragraphs: list[dict], cfg: dict[str, str]) -> list[dict]:
    results = []
    prose = [p for p in paragraphs if p["type"] == "prose"]
    for p in prose:
        try:
            raw = call_api(p["text"], PUNCH_SYSTEM, cfg)
            clean = re.sub(r"```json\s*|```", "", raw).strip()
            result = json.loads(clean)
        except Exception as e:
            result = {"has_punch": None, "error": str(e)}
        result["paragraph_index"] = p["index"]
        result["first_words"] = p["text"][:80]
        results.append(result)
    return results


# ── Pass 2: JARGON (two modes) ──────────────────────────────────────

JARGON_STRIP_SYSTEM = """You are a clarity editor for a STORY that bridges physics, theology, and information theory. The target reader is intelligent but not academic — think a smart churchgoer or a curious engineer.

MODE: STRIP — replace jargon with plain language. The best lines in this series translate technical concepts into physical metaphors: "You can't fix the floor while you're standing on it" is better than "internal agents cannot repair the substrate they operate on."

Think step by step about WHY each term is jargon and whether it carries meaning that the plain version would lose. Only strip jargon that can be replaced without losing structural meaning.

Respond in JSON only:
{
  "jargon_score": 0-10 (0=plain English, 10=academic paper),
  "flagged_terms": [{"term": "composition field", "suggestion": "the overlap between them", "safe_to_strip": true}],
  "rewrite": "full paragraph rewritten at jargon_score <= 3, or null if already clean",
  "note": "brief explanation"
}"""

JARGON_DEFINE_SYSTEM = """You are a clarity editor for a THEOPHYSICS technical document that bridges physics, theology, and information theory. The target reader is intelligent and willing to learn terminology, but shouldn't have to guess.

MODE: DEFINE — keep the jargon but make sure every technical term is defined on first use or has enough context that a reader can follow. Don't dumb it down. Make it learnable.

Think step by step about which terms a non-specialist would stumble on and what minimal definition would unstick them.

Respond in JSON only:
{
  "jargon_score": 0-10 (0=plain English, 10=academic paper),
  "undefined_terms": [{"term": "composition field", "definition": "the overlap zone where two agents' output mixes and waste becomes usable material", "insert_after": "the sentence where it first appears"}],
  "note": "brief explanation"
}"""

def run_jargon(paragraphs: list[dict], cfg: dict[str, str], mode: str = "strip") -> list[dict]:
    """Run jargon pass. mode='strip' for stories, mode='define' for theophysics docs."""
    system = JARGON_STRIP_SYSTEM if mode == "strip" else JARGON_DEFINE_SYSTEM
    # Use thinking model for jargon — it reasons better about what's load-bearing
    thinking_cfg = get_thinking_config()
    use_cfg = thinking_cfg if thinking_cfg["endpoint"] else cfg
    results = []
    prose = [p for p in paragraphs if p["type"] == "prose"]
    for p in prose:
        try:
            raw = call_api(p["text"], system, use_cfg)
            clean = re.sub(r"```json\s*|```", "", raw).strip()
            result = json.loads(clean)
            result["jargon_mode"] = mode
        except Exception as e:
            result = {"jargon_score": None, "jargon_mode": mode, "error": str(e)}
        result["paragraph_index"] = p["index"]
        result["first_words"] = p["text"][:80]
        results.append(result)
    return results


# ── Pass 3: CITATION ────────────────────────────────────────────────

CITATION_SYSTEM = """You are a theological and historical citation advisor for a narrative that retells Scripture through physics and information theory. The author wants citations woven into the text — not modern academic papers, but the historical thinkers who reached each idea first.

Priority sources (use these before anyone modern):
- Church Fathers: Augustine, Aquinas, Boethius, Athanasius, Gregory of Nyssa, Basil, Irenaeus, Origen
- Scripture: chapter and verse, woven naturally not as footnotes
- Ancient philosophers: Aristotle, Plato (where they anticipate the point)
- Reformation: Luther, Calvin, Pascal (where relevant)
- Scientists who were also theologians: Newton, Maxwell, Faraday, Leibniz

Your job: identify where in this paragraph a historical citation would strengthen the argument or connect it to tradition. Do NOT cite modern academics unless the idea has no ancient precedent.

Respond in JSON only:
{
  "citations_suggested": [
    {
      "after_sentence": "the sentence this citation follows",
      "citation": "Augustine, Confessions VII.10 — 'I entered and saw with my soul's eye...'",
      "reason": "Augustine describes the same contact-mechanism: seeing truth by proximity, not by effort"
    }
  ],
  "scripture_threads": [
    {
      "verse": "John 1:14",
      "connection": "The Word became flesh — the crossing from outside into the system"
    }
  ],
  "no_citation_needed": true/false,
  "note": "brief explanation"
}"""

def run_citation(paragraphs: list[dict], cfg: dict[str, str]) -> list[dict]:
    results = []
    prose = [p for p in paragraphs if p["type"] == "prose"]
    for p in prose:
        try:
            raw = call_api(p["text"], CITATION_SYSTEM, cfg)
            clean = re.sub(r"```json\s*|```", "", raw).strip()
            result = json.loads(clean)
        except Exception as e:
            result = {"citations_suggested": [], "error": str(e)}
        result["paragraph_index"] = p["index"]
        result["first_words"] = p["text"][:80]
        results.append(result)
    return results


# ── Runner ──────────────────────────────────────────────────────────

PASSES = {
    "punch": run_punch,
    "jargon": run_jargon,
    "cite": run_citation,
}


def process_chapter(path: Path, passes: list[str], cfg: dict[str, str],
                    jargon_mode: str = "strip") -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    paragraphs = split_paragraphs(text)
    review = {
        "source": str(path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": cfg["model"],
        "paragraph_count": len(paragraphs),
        "prose_count": sum(1 for p in paragraphs if p["type"] == "prose"),
        "jargon_mode": jargon_mode,
    }
    for pass_name in passes:
        fn = PASSES[pass_name]
        print(f"  Running {pass_name} pass ({review['prose_count']} paragraphs)...", flush=True)
        if pass_name == "jargon":
            review[pass_name] = fn(paragraphs, cfg, mode=jargon_mode)
        else:
            review[pass_name] = fn(paragraphs, cfg)
        done = len(review[pass_name])
        print(f"    {pass_name}: {done} paragraphs processed", flush=True)
    return review


def main() -> None:
    parser = argparse.ArgumentParser(description="Story Processing Rail — paragraph-level API refinement")
    parser.add_argument("pass_name", choices=["punch", "jargon", "cite", "all"])
    parser.add_argument("chapter", type=Path)
    parser.add_argument("--apply", action="store_true", help="Write .refined.md with suggestions applied")
    parser.add_argument("--jargon-mode", choices=["strip", "define"], default="strip",
                        help="strip=replace jargon (stories), define=keep but define (theophysics)")
    args = parser.parse_args()

    cfg = get_config()
    if not cfg["endpoint"]:
        print("ERROR: Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or STORY_RAIL_ENDPOINT/MODEL/API_KEY")
        sys.exit(1)

    if not args.chapter.exists():
        print(f"ERROR: File not found: {args.chapter}")
        sys.exit(1)

    passes = list(PASSES.keys()) if args.pass_name == "all" else [args.pass_name]
    print(f"Story Rail — {args.chapter.name}")
    print(f"  Passes: {', '.join(passes)}")
    print(f"  Model:  {cfg['model']}")
    print(f"  Jargon: {args.jargon_mode}")
    print()

    review = process_chapter(args.chapter, passes, cfg, jargon_mode=args.jargon_mode)

    # Write sidecar review JSON
    out_path = args.chapter.with_suffix(".story-review.json")
    out_path.write_text(json.dumps(review, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReview written: {out_path}")

    # Summary stats
    if "punch" in review:
        missing = sum(1 for r in review["punch"] if not r.get("has_punch"))
        print(f"  Punch: {missing}/{len(review['punch'])} paragraphs need an unmistakable sentence")
    if "jargon" in review:
        high = sum(1 for r in review["jargon"] if (r.get("jargon_score") or 0) > 5)
        print(f"  Jargon: {high}/{len(review['jargon'])} paragraphs scored > 5")
    if "cite" in review:
        cites = sum(len(r.get("citations_suggested", [])) for r in review["cite"])
        verses = sum(len(r.get("scripture_threads", [])) for r in review["cite"])
        print(f"  Citation: {cites} historical citations + {verses} Scripture threads suggested")


if __name__ == "__main__":
    main()
