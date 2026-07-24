"""Claim Beacon Protocol v0.1 utilities.

Static, dependency-light tools for publishing claim beacons, generating a
public discovery manifest, rendering compact HTML panels, and proposing local
relationships. Proposals are never accepted automatically.

Usage:
  python _scripts/claim_beacon.py manifest
  python _scripts/claim_beacon.py propose
  python _scripts/claim_beacon.py render
  python _scripts/claim_beacon.py all
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
PUBLIC_BASE = "https://faiththruphysics.com"
CONTEXT = "https://faiththruphysics.com/vocab/context.jsonld"
WELL_KNOWN = REPO / ".well-known" / "claim-beacons.json"
PROPOSALS = REPO / "_proposals" / "claim-relationships.jsonl"
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,}", re.I)
PROPAGATING_GRADES = {"structural_identity", "structural_isomorphism"}
NON_PROPAGATING_GRADES = {"structural_analogy", "metaphorical", "ungraded"}


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()
    except Exception:
        return ""


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def load_atoms() -> list[tuple[Path, dict[str, Any]]]:
    atoms = []
    for path in REPO.rglob("*.jsonld"):
        if "_vocab" in path.parts:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("nodeType") == "claim" or data.get("claimID"):
            atoms.append((path, data))
    return atoms


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v]
    return [str(value)]


def tokens(items: list[str]) -> set[str]:
    out: set[str] = set()
    for item in items:
        out.update(t.lower() for t in TOKEN_RE.findall(item))
    return out


def atom_url(path: Path, atom: dict[str, Any]) -> str:
    return str(atom.get("@id") or f"{PUBLIC_BASE}/{rel(path)}")


def html_url(path: Path) -> str:
    return f"{PUBLIC_BASE}/{rel(path.with_suffix('.html'))}"


def default_beacon(path: Path, atom: dict[str, Any]) -> dict[str, Any]:
    claim_id = atom.get("claimID") or atom.get("nodeID") or rel(path)
    offer = []
    if atom.get("evidenceType"):
        offer.append(f"evidence:{atom['evidenceType']}")
    if atom.get("mathematicalForm") or atom.get("mathFormNormal"):
        offer.append("derivation:mathematical-form")
    for edge in atom.get("edges", []):
        if edge.get("type") == "bridgesTo":
            offer.append(f"mapping:{edge.get('grade', 'ungraded')}:{edge.get('target')}")
    need = [edge.get("target") for edge in atom.get("edges", []) if edge.get("type") == "dependsOn" and edge.get("target")]
    break_if = as_list(atom.get("falsificationCondition"))
    return {
        "protocol": "ClaimBeacon",
        "protocolVersion": "0.1.0",
        "permanentID": claim_id,
        "canonicalURL": atom_url(path, atom),
        "version": atom.get("version", "0.1.0"),
        "provenance": {
            "repo": git("config", "--get", "remote.origin.url") or "local",
            "path": rel(path),
            "gitCommit": git("rev-parse", "HEAD") or "uncommitted",
            "dateModified": atom.get("dateModified"),
            "authors": atom.get("author", []),
        },
        "priorVersions": atom.get("priorVersions", []),
        "claimType": atom.get("claimClass"),
        "domain": atom.get("domainType"),
        "masterEquationVariables": atom.get("masterEquationVariables", []),
        "tags": atom.get("tags", []),
        "bridgeGrade": atom.get("bridgeGrade", "ungraded"),
        "have": sorted(set(offer + as_list(atom.get("keywords")) + as_list(atom.get("tags")))),
        "need": need,
        "breakIf": break_if,
        "acceptedLinks": [e for e in atom.get("edges", []) if e.get("status") == "accepted"],
        "proposalFeed": f"{PUBLIC_BASE}/_proposals/claim-relationships.jsonl",
    }


def beacon_for(path: Path, atom: dict[str, Any]) -> dict[str, Any]:
    beacon = default_beacon(path, atom)
    beacon.update(atom.get("claimBeacon", {}))
    return beacon


def write_manifest() -> None:
    records = []
    for path, atom in load_atoms():
        beacon = beacon_for(path, atom)
        records.append({
            "permanentID": beacon["permanentID"],
            "canonicalURL": beacon["canonicalURL"],
            "atom": f"/{rel(path)}",
            "html": f"/{rel(path.with_suffix('.html'))}",
            "beaconPath": f"/{rel(path)}#claimBeacon",
            "version": beacon.get("version"),
            "domain": beacon.get("domain"),
            "claimType": beacon.get("claimType"),
            "tags": beacon.get("tags", []),
        })
    manifest = {
        "@context": [CONTEXT],
        "protocol": "ClaimBeacon",
        "protocolVersion": "0.1.0",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "records": sorted(records, key=lambda r: r["permanentID"]),
    }
    WELL_KNOWN.parent.mkdir(exist_ok=True)
    WELL_KNOWN.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def confidence(shared: set[str], total: int) -> float:
    if not shared:
        return 0.0
    return round(min(0.95, 0.35 + len(shared) / max(total, 1)), 2)


def write_proposals() -> None:
    atoms = [(p, a, beacon_for(p, a)) for p, a in load_atoms()]
    lines = []
    for sp, _sa, sb in atoms:
        s_have, s_break = tokens(as_list(sb.get("have"))), tokens(as_list(sb.get("breakIf")))
        for tp, _ta, tb in atoms:
            if sp == tp:
                continue
            t_need, t_break = tokens(as_list(tb.get("need"))), tokens(as_list(tb.get("breakIf")))
            have_need = s_have & t_need
            break_break = s_break & t_break
            if not have_need and not break_break:
                continue
            edge_type = "challenges" if break_break else "bridgesTo"
            shared = sorted(have_need or break_break)
            proposal = {
                "protocol": "ClaimBeaconProposal",
                "protocolVersion": "0.1.0",
                "sourceAtom": sb["permanentID"],
                "targetAtom": tb["permanentID"],
                "proposedEdgeType": edge_type,
                "matchReason": f"deterministic keyword overlap: {', '.join(shared[:12])}",
                "confidence": confidence(set(shared), len(s_have | t_need | s_break | t_break)),
                "status": "proposed",
                "validationReceipt": {
                    "validator": "_scripts/claim_beacon.py propose",
                    "method": "deterministic-keyword-v1",
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                    "gitCommit": git("rev-parse", "HEAD") or "uncommitted",
                    "acceptedBy": None,
                    "acceptedAt": None,
                    "bridgeGrade": "ungraded",
                    "propagatesFalsification": False,
                },
            }
            pid = hashlib.sha256(json.dumps(proposal, sort_keys=True).encode()).hexdigest()[:16]
            proposal["proposalID"] = f"cbp-{pid}"
            lines.append(json.dumps(proposal, ensure_ascii=False, sort_keys=True))
    PROPOSALS.parent.mkdir(exist_ok=True)
    PROPOSALS.write_text("\n".join(sorted(set(lines))) + ("\n" if lines else ""), encoding="utf-8")


def render_html() -> None:
    for path, atom in load_atoms():
        b = beacon_for(path, atom)
        def items(vals: Any) -> str:
            vals = as_list(vals)
            return "".join(f"<li>{html.escape(str(v))}</li>" for v in vals) or "<li>None declared</li>"
        accepted = b.get("acceptedLinks", [])
        accepted_html = "".join(f"<li>{html.escape(e.get('type','edge'))}: {html.escape(str(e.get('target','')))} ({html.escape(e.get('grade','ungraded'))})</li>" for e in accepted) or "<li>None accepted</li>"
        doc = f"""<!doctype html>
<html lang=\"en\">
<head><meta charset=\"utf-8\"><title>{html.escape(atom.get('name','Claim atom'))}</title></head>
<body>
<article class=\"claim-atom\" data-atom-id=\"{html.escape(b['permanentID'])}\">
  <h1>{html.escape(atom.get('name','Claim atom'))}</h1>
  <p>{html.escape(atom.get('statementPlain') or atom.get('statementTechnical') or '')}</p>
  <section class=\"claim-beacon\" data-protocol=\"ClaimBeacon\" data-version=\"0.1.0\">
    <h2>Claim Beacon / Receipt</h2>
    <p><strong>Permanent ID:</strong> {html.escape(b['permanentID'])}</p>
    <p><strong>Canonical URL:</strong> <a href=\"{html.escape(b['canonicalURL'])}\">{html.escape(b['canonicalURL'])}</a></p>
    <h3>Offers</h3><ul>{items(b.get('have'))}</ul>
    <h3>Needs</h3><ul>{items(b.get('need'))}</ul>
    <h3>Breaks if</h3><ul>{items(b.get('breakIf'))}</ul>
    <h3>Accepted links</h3><ul>{accepted_html}</ul>
    <h3>Proposed links</h3><p>Review proposal feed: <code>/_proposals/claim-relationships.jsonl</code>. Proposed links are never accepted automatically.</p>
  </section>
</article>
</body>
</html>
"""
        path.with_suffix(".html").write_text(doc, encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["manifest", "propose", "render", "all"])
    args = p.parse_args()
    if args.command in {"manifest", "all"}: write_manifest()
    if args.command in {"propose", "all"}: write_proposals()
    if args.command in {"render", "all"}: render_html()


if __name__ == "__main__":
    main()
