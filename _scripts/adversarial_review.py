"""Adversarial gate for proposed Claim Beacon relationships.

The gate is deliberately provider-neutral: an OpenAI-compatible endpoint can be
used, or a deterministic local reviewer can be selected for offline work.  A
review can block a proposal, but it can never accept one; acceptance remains a
separate human decision.
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
PROPOSALS = REPO / "_proposals" / "claim-relationships.jsonl"
REVIEWS = REPO / "_proposals" / "adversarial-reviews.jsonl"
ALLOWED_VERDICTS = {"pass", "oppose", "uncertain"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def atoms_by_id() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in REPO.rglob("*.jsonld"):
        if any(part in {"_vocab", "_protocol"} for part in path.parts):
            continue
        atom = json.loads(path.read_text(encoding="utf-8"))
        for key in ("claimID", "nodeID", "@id"):
            if atom.get(key):
                result[str(atom[key])] = atom
    return result


def review_prompt(proposal: dict[str, Any], source: dict[str, Any], target: dict[str, Any]) -> str:
    packet = {
        "proposal": proposal,
        "source": source,
        "target": target,
        "rubric": {
            "epistemology": "Does the evidence justify the proposed relation and confidence?",
            "ontology": "Are the entities and categories actually comparable?",
            "logic": "Does the inference preserve direction, scope, and boundary conditions?",
            "falsification": "Do either claim's kill conditions contradict or defeat the link?",
        },
    }
    return (
        "Act as a hostile but fair reviewer. Look for the strongest reason this proposed graph "
        "edge must not connect. Return JSON only with keys verdict (pass|oppose|uncertain), "
        "summary, objections (array), requiredTests (array), and confidence (0..1). "
        "Use oppose when a stated contradiction, failed invariant, category error, or unsupported "
        "inferential leap defeats the edge. Uncertainty must not be reported as pass.\n\n"
        + json.dumps(packet, ensure_ascii=False)
    )


@dataclass
class CompatibleClient:
    endpoint: str
    model: str
    api_key: str = ""
    timeout: int = 60

    def review(self, prompt: str) -> dict[str, Any]:
        body = json.dumps({
            "model": self.model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": prompt}],
        }).encode()
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(self.endpoint, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            payload = json.load(response)
        content = payload["choices"][0]["message"]["content"]
        return json.loads(content) if isinstance(content, str) else content


def local_review(proposal: dict[str, Any], source: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    """Conservative offline gate: contradictions block; missing proof stays uncertain."""
    text = json.dumps([proposal, source, target], ensure_ascii=False).lower()
    opposing = [term for term in ("falsified", "retracted", "contradiction", "rejected") if term in text]
    if opposing:
        verdict, summary = "oppose", f"Blocking state found: {', '.join(opposing)}."
    else:
        verdict, summary = "uncertain", "No deterministic contradiction found; model or human review is still required."
    return {"verdict": verdict, "summary": summary, "objections": opposing,
            "requiredTests": ["human review of mapping and boundary conditions"], "confidence": 1.0 if opposing else 0.35}


def normalize(result: dict[str, Any]) -> dict[str, Any]:
    verdict = str(result.get("verdict", "uncertain")).lower()
    if verdict not in ALLOWED_VERDICTS:
        verdict = "uncertain"
    return {"verdict": verdict, "summary": str(result.get("summary", "No summary supplied.")),
            "objections": list(result.get("objections") or []),
            "requiredTests": list(result.get("requiredTests") or []),
            "confidence": max(0.0, min(1.0, float(result.get("confidence", 0))))}


def run_reviews(provider: str = "local", proposal_id: str | None = None,
                endpoint: str = "", model: str = "", api_key: str = "") -> list[dict[str, Any]]:
    atoms = atoms_by_id()
    proposals = [p for p in load_jsonl(PROPOSALS) if not proposal_id or p.get("proposalID") == proposal_id]
    output = []
    client = CompatibleClient(endpoint, model, api_key) if provider == "compatible" else None
    for proposal in proposals:
        source = atoms.get(str(proposal.get("sourceAtom")), {})
        target = atoms.get(str(proposal.get("targetAtom")), {})
        try:
            raw = client.review(review_prompt(proposal, source, target)) if client else local_review(proposal, source, target)
            result, error = normalize(raw), None
        except (ValueError, KeyError, urllib.error.URLError, TimeoutError) as exc:
            result, error = normalize({"verdict": "uncertain", "summary": "Reviewer failed closed."}), str(exc)
        receipt = {"proposalID": proposal.get("proposalID"), "reviewedAt": datetime.now(timezone.utc).isoformat(),
                   "provider": provider, "model": model or "deterministic-local-v1", **result,
                   "gateStatus": "blocked" if result["verdict"] == "oppose" else "awaiting_human",
                   "error": error}
        output.append(receipt)
    if output:
        prior = {r.get("proposalID"): r for r in load_jsonl(REVIEWS)}
        prior.update({r["proposalID"]: r for r in output})
        REVIEWS.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in prior.values()), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Adversarially review proposed graph edges")
    parser.add_argument("--provider", choices=("local", "compatible"), default=os.getenv("ADVERSARY_PROVIDER", "local"))
    parser.add_argument("--proposal-id")
    parser.add_argument("--endpoint", default=os.getenv("ADVERSARY_API_URL", ""))
    parser.add_argument("--model", default=os.getenv("ADVERSARY_MODEL", ""))
    parser.add_argument("--api-key", default=os.getenv("ADVERSARY_API_KEY", ""))
    args = parser.parse_args()
    if args.provider == "compatible" and not (args.endpoint and args.model):
        parser.error("compatible provider requires --endpoint and --model")
    print(json.dumps(run_reviews(args.provider, args.proposal_id, args.endpoint, args.model, args.api_key), indent=2))


if __name__ == "__main__":
    main()
