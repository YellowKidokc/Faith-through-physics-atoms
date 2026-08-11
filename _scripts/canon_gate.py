"""Human-gated canonical publication helper.

Markdown/source files are authoring inputs. Canonical HTML/JSON are frozen
publication snapshots. The Living Atlas owns current epistemic standing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
CANON = REPO / "_canon"
SIDECARS = REPO / "_atlas" / "canon-sidecars"
REGISTRY = REPO / "_atlas" / "canonical-publications.jsonl"


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonld_claims() -> list[dict[str, Any]]:
    claims = []
    for path in REPO.rglob("*.jsonld"):
        if any(part in {"_vocab", "_protocol"} for part in path.parts):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("nodeType") == "claim" or data.get("claimID"):
            data["_path"] = rel(path)
            claims.append(data)
    return claims


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def publication_stats(source: Path) -> dict[str, Any]:
    text = source.read_text(encoding="utf-8", errors="replace")
    claims = load_jsonld_claims()
    source_rel = rel(source)
    related_claims = [
        c for c in claims
        if c.get("_path") == source_rel or str(c.get("sourceReference", "")).endswith(source.name)
    ]
    return {
        "sourceHash": f"sha256:{sha256(source)}",
        "wordCount": count_words(text),
        "atomCount": len(related_claims),
        "claimCount": sum(1 for c in related_claims if c.get("claimID")),
        "definitionCount": sum(1 for c in related_claims if c.get("claimKind") == "definition" or c.get("claimClass") == "definition"),
        "derivationCount": sum(1 for c in related_claims if c.get("mathematicalForm") or c.get("mathFormNormal")),
        "evidenceObjectCount": text.lower().count("evidence"),
        "proofObjectCount": text.lower().count("proof"),
        "openItemCount": text.lower().count("open"),
        "killConditionCount": text.lower().count("kill") + text.lower().count("falsification"),
        "bridgeCandidateCount": text.lower().count("bridge"),
        "equationCount": text.count("="),
        "domainCount": len({str(c.get("domainType")) for c in related_claims if c.get("domainType")}),
        "nativeDomainCount": len({str(c.get("domainType")) for c in related_claims if c.get("domainType")}),
        "referenceCount": len(re.findall(r"https?://|\[[^\]]+\]\([^\)]+\)", text)),
        "initialInternalGrade": "ungraded",
        "initialExternalGrade": "ungraded",
        "initialConsilienceGrade": "ungraded",
    }


def living_stats() -> dict[str, Any]:
    def jsonl_count(path: Path) -> int:
        if not path.exists():
            return 0
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

    relations_path = REPO / "_atlas" / "relations.jsonl"
    open_items_path = REPO / "_atlas" / "open-items.jsonl"
    evidence_path = REPO / "_atlas" / "evidence-coverage.jsonl"
    relations = []
    if relations_path.exists():
        relations = [json.loads(line) for line in relations_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    open_items = []
    if open_items_path.exists():
        open_items = [json.loads(line) for line in open_items_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    now = datetime.now(timezone.utc).isoformat()
    return {
        "currentStanding": "living_atlas",
        "currentG_I": "ungraded",
        "currentG_E": "ungraded",
        "currentG_C": "ungraded",
        "laterSupportingAtoms": sum(1 for r in relations if r.get("relation") in {"supports", "establishes"}),
        "laterContradictingAtoms": sum(1 for r in relations if r.get("relation") in {"contradicts", "falsifies", "partially_contradicts"}),
        "laterQualifyingAtoms": sum(1 for r in relations if r.get("relation") == "qualifies"),
        "resolvedOpenItems": sum(1 for i in open_items if i.get("status") == "resolved"),
        "stillOpenItems": sum(1 for i in open_items if i.get("status") != "resolved"),
        "supersededClaims": sum(1 for r in relations if r.get("relation") == "supersedes"),
        "currentAdmittedBridges": sum(1 for r in relations if r.get("relation") in {"bridgesTo", "supports"} and r.get("status") in {"accepted", "verified"}),
        "suspendedBridges": 0,
        "externalAnchors": jsonl_count(evidence_path),
        "formalReceipts": 0,
        "leanReceipts": len(list((REPO / "_runtime" / "lean_receipts").glob("*"))) if (REPO / "_runtime" / "lean_receipts").exists() else 0,
        "pythonTestReceipts": 0,
        "totalRuns": 0,
        "upstreamDegree": 0,
        "downstreamDegree": 0,
        "crossDomainDegree": 0,
        "papersReferencingThis": 0,
        "seriesReferencingThis": 0,
        "domainsReached": 0,
        "currentBlastRadius": 0,
        "lastRecalculated": now,
        "lastEvidenceAdded": now if jsonl_count(evidence_path) else None,
        "lastStandingChange": None,
    }


def build_record(source: Path, version_id: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "publicationID": version_id,
        "sourcePath": rel(source),
        "sourceKind": source.suffix.lower().lstrip(".") or "unknown",
        "canonicalDate": now,
        "versionID": version_id,
        "principle": "Markdown source != canonical publication != living epistemic state",
        "frozenPublicationStats": publication_stats(source),
        "livingAtlasStats": living_stats(),
        "canonGate": {
            "status": "sidecar",
            "reviewPrompt": "PROMOTE TO CANONICAL PUBLICATION?",
            "allowedActions": ["review_again", "save_as_sidecar", "promote_to_canon"],
            "warning": "Promotion freezes canonical HTML/JSON snapshots. Later Atlas updates may change current standing but must not rewrite this historical version.",
        },
    }


def write_sidecar(record: dict[str, Any]) -> Path:
    SIDECARS.mkdir(parents=True, exist_ok=True)
    path = SIDECARS / f"{record['publicationID']}.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def promote(source: Path, record: dict[str, Any]) -> tuple[Path, Path]:
    CANON.mkdir(parents=True, exist_ok=True)
    record = json.loads(json.dumps(record))
    record["canonGate"]["status"] = "promoted"
    record["canonGate"]["acceptedAt"] = datetime.now(timezone.utc).isoformat()
    json_path = CANON / f"{record['publicationID']}.canonical.json"
    html_path = CANON / f"{record['publicationID']}.canonical{'.html' if source.suffix.lower() != '.html' else '.html'}"
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if source.suffix.lower() == ".html":
        shutil.copyfile(source, html_path)
    else:
        body = source.read_text(encoding="utf-8", errors="replace")
        html_path.write_text(
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<title>{record['publicationID']}</title></head><body><pre>"
            + body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            + "</pre></body></html>\n",
            encoding="utf-8",
        )
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return html_path, json_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare or promote a canonical publication snapshot")
    parser.add_argument("source", type=Path)
    parser.add_argument("--version-id", required=True)
    parser.add_argument("--accept-canon", action="store_true", help="Required to create canonical HTML/JSON and registry rows")
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.exists():
        parser.error(f"source not found: {source}")
    record = build_record(source, args.version_id)
    if args.accept_canon:
        html_path, json_path = promote(source, record)
        print(json.dumps({"status": "promoted", "html": rel(html_path), "json": rel(json_path)}, indent=2))
    else:
        sidecar = write_sidecar(record)
        print(json.dumps({"status": "sidecar", "sidecar": rel(sidecar), "next": "review_again | save_as_sidecar | rerun with --accept-canon"}, indent=2))


if __name__ == "__main__":
    main()
