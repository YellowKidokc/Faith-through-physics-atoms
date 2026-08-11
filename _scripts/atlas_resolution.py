"""Living Atlas resolution utilities.

Papers remain historical snapshots. Claims are living epistemic objects whose
current state can be changed by later accepted graph relations.
"""
from __future__ import annotations

import html
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
OPEN_ITEMS = REPO / "_atlas" / "open-items.jsonl"
RELATIONS = REPO / "_atlas" / "relations.jsonl"
EVIDENCE_COVERAGE = REPO / "_atlas" / "evidence-coverage.jsonl"

INVERSES = {
    "establishes": "established by",
    "supports": "supported by",
    "partially_supports": "partially supported by",
    "consistent_with": "has consistency evidence from",
    "contextualizes": "contextualized by",
    "contradicts": "contradicted by",
    "partially_contradicts": "partially contradicted by",
    "is_silent": "not addressed by",
    "qualifies": "qualified by",
    "supersedes": "superseded by",
    "resolves": "resolved by",
    "depends_on": "required by",
    "dependsOn": "required by",
    "extends": "extended by",
    "falsifies": "falsified by",
}

STATE_BY_RELATION = {
    "establishes": "established",
    "resolves": "resolved",
    "qualifies": "qualified",
    "supersedes": "superseded",
    "contradicts": "contested",
    "partially_contradicts": "partially_contested",
    "falsifies": "falsified",
    "supports": "supported",
    "partially_supports": "partially_supported",
}


@dataclass
class Atlas:
    forward: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    backward: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    open_items_by_atom: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    evidence_by_claim: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    atoms: dict[str, dict[str, Any]] = field(default_factory=dict)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: invalid JSON on line {number}: {exc}") from exc
    return rows


def atom_key(path: Path, atom: dict[str, Any]) -> str:
    return str(atom.get("claimID") or atom.get("nodeID") or atom.get("@id") or path.relative_to(REPO).as_posix())


def load_claim_atoms(root: Path = REPO) -> dict[str, dict[str, Any]]:
    atoms: dict[str, dict[str, Any]] = {}
    for path in root.rglob("*.jsonld"):
        if any(part in {"_vocab", "_protocol"} for part in path.parts):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("nodeType") == "claim" or data.get("claimID"):
            data["_path"] = path.relative_to(root).as_posix()
            atoms[atom_key(path, data)] = data
    return atoms


def normalize_relation(row: dict[str, Any]) -> dict[str, Any]:
    relation = dict(row)
    relation.setdefault("relation", relation.get("type") or relation.get("edgeType"))
    relation.setdefault("sourceAtom", relation.get("source") or relation.get("from"))
    relation.setdefault("targetAtom", relation.get("target") or relation.get("to"))
    relation.setdefault("status", "accepted")
    return relation


def relations_from_atoms(atoms: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for source_id, atom in atoms.items():
        for edge in atom.get("edges", []):
            if edge.get("status") != "accepted":
                continue
            target = edge.get("target")
            relation = edge.get("relation") or edge.get("type")
            if not target or not relation:
                continue
            rows.append({
                "sourceAtom": source_id,
                "targetAtom": target,
                "relation": relation,
                "status": "accepted",
                "scope": edge.get("scope"),
                "source": atom.get("_path"),
            })
    return rows


def relations_from_open_items(open_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in open_items:
        for resolution in item.get("resolved_by") or []:
            source = resolution.get("atom_id")
            relation = resolution.get("relation", "resolves")
            targets = resolution.get("targets") or item.get("affects") or []
            if source and not targets and item.get("opened_by", {}).get("atom_id"):
                targets = [item["opened_by"]["atom_id"]]
            for target in targets:
                rows.append({
                    "sourceAtom": source,
                    "targetAtom": target,
                    "relation": relation,
                    "status": "accepted",
                    "scope": resolution.get("scope"),
                    "paper_id": resolution.get("paper_id"),
                    "issue_id": item.get("issue_id"),
                })
    return rows


def build_atlas(root: Path = REPO) -> Atlas:
    atoms = load_claim_atoms(root)
    open_items = load_jsonl(root / "_atlas" / "open-items.jsonl")
    evidence_rows = load_jsonl(root / "_atlas" / "evidence-coverage.jsonl")
    relation_rows = [normalize_relation(r) for r in load_jsonl(root / "_atlas" / "relations.jsonl")]
    relation_rows.extend(relations_from_atoms(atoms))
    relation_rows.extend(relations_from_open_items(open_items))

    atlas = Atlas(atoms=atoms)
    for relation in relation_rows:
        if relation.get("status") not in {"accepted", "verified"}:
            continue
        source, target = relation.get("sourceAtom"), relation.get("targetAtom")
        if not source or not target:
            continue
        atlas.forward.setdefault(str(source), []).append(relation)
        atlas.backward.setdefault(str(target), []).append(relation)

    for item in open_items:
        affected = set(str(a) for a in item.get("affects", []))
        opened_atom = item.get("opened_by", {}).get("atom_id")
        if opened_atom:
            affected.add(str(opened_atom))
        for atom_id in sorted(affected):
            atlas.open_items_by_atom.setdefault(atom_id, []).append(item)
    for row in evidence_rows:
        claim_id = row.get("claim_id") or row.get("claimID")
        if claim_id:
            atlas.evidence_by_claim.setdefault(str(claim_id), []).append(row)
    return atlas


def component_coverage(item: dict[str, Any]) -> dict[str, Any] | None:
    components = item.get("components") or []
    if not components:
        return None
    resolved = [c for c in components if c.get("status") in {"resolved", "verified", "supported"}]
    return {
        "resolved": len(resolved),
        "total": len(components),
        "status": "resolved" if len(resolved) == len(components) else "partially_resolved" if resolved else "open",
        "components": components,
    }


def current_status(atom_id: str, atom: dict[str, Any], atlas: Atlas) -> str:
    items = atlas.open_items_by_atom.get(atom_id, [])
    if items:
        coverages = [component_coverage(i) for i in items]
        if any(c and c["status"] == "partially_resolved" for c in coverages):
            return "partially_resolved"
        if all(i.get("status") == "resolved" for i in items):
            return "resolved"
        if any(i.get("status") in {"contested", "blocked"} for i in items):
            return "contested"
        return "open"
    for relation in atlas.backward.get(atom_id, []):
        state = STATE_BY_RELATION.get(str(relation.get("relation")))
        if state:
            return state
    return str(atom.get("currentAtlasStatus") or atom.get("status") or atom.get("canonicalStatus") or "unknown")


def original_status(atom: dict[str, Any]) -> str:
    paper_state = atom.get("paperState") or atom.get("publicationState") or {}
    if isinstance(paper_state, dict):
        return str(paper_state.get("statusAtPublication") or paper_state.get("status") or atom.get("status") or "unknown")
    return str(paper_state or atom.get("status") or "unknown")


def _li(text: str) -> str:
    return f"<li>{html.escape(text)}</li>"


def render_relation(relation: dict[str, Any], inverse: bool = False) -> str:
    source = str(relation.get("sourceAtom", "unknown"))
    target = str(relation.get("targetAtom", "unknown"))
    rel = str(relation.get("relation", "relates"))
    label = INVERSES.get(rel, f"{rel} by") if inverse else rel
    other = source if inverse else target
    scope = relation.get("scope")
    suffix = f" - {scope}" if scope else ""
    issue = f" ({relation.get('issue_id')})" if relation.get("issue_id") else ""
    return _li(f"{label}: {other}{suffix}{issue}")


def render_open_item(item: dict[str, Any]) -> str:
    title = str(item.get("issue_id", "open-item"))
    question = str(item.get("question", ""))
    status = str(item.get("status", "open"))
    coverage = component_coverage(item)
    parts = [f"<article class=\"open-item\"><h4>{html.escape(title)}</h4>",
             f"<p><strong>Status:</strong> {html.escape(status)}</p>"]
    if question:
        parts.append(f"<p>{html.escape(question)}</p>")
    if coverage:
        parts.append(f"<p><strong>Coverage:</strong> {coverage['resolved']}/{coverage['total']} components ({html.escape(coverage['status'])})</p>")
        parts.append("<ul>")
        for component in coverage["components"]:
            label = component.get("component_id") or component.get("id") or "component"
            parts.append(_li(f"{label}: {component.get('status', 'open')} - {component.get('question', '')}"))
        parts.append("</ul>")
    parts.append("</article>")
    return "".join(parts)


def claim_components(atom: dict[str, Any]) -> list[dict[str, Any]]:
    raw = atom.get("claimComponents") or atom.get("components") or []
    components = []
    for index, component in enumerate(raw, 1):
        if isinstance(component, dict):
            component_id = component.get("componentID") or component.get("component_id") or component.get("id")
            components.append({
                "componentID": str(component_id or f"component-{index}"),
                "predicate": str(component.get("predicate") or component.get("question") or component_id or f"component-{index}"),
                "status": str(component.get("status", "declared")),
            })
        else:
            components.append({"componentID": f"component-{index}", "predicate": str(component), "status": "declared"})
    return components


def evidence_component_status(atom: dict[str, Any], evidence_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    components = claim_components(atom)
    by_component = {component["componentID"]: {**component, "evidence": []} for component in components}
    for row in evidence_rows:
        for support in row.get("supports", []):
            component_id = str(support.get("claim_component", ""))
            if component_id not in by_component:
                by_component[component_id] = {"componentID": component_id, "predicate": component_id, "status": "undeclared", "evidence": []}
            by_component[component_id]["evidence"].append({
                "evidence_id": row.get("evidence_id"),
                "relation": support.get("relation"),
                "strength": support.get("strength"),
                "coverage": row.get("coverage"),
                "note": support.get("note"),
            })
        for component_id in row.get("unaddressed", []):
            component_id = str(component_id)
            if component_id not in by_component:
                by_component[component_id] = {"componentID": component_id, "predicate": component_id, "status": "undeclared", "evidence": []}
    return list(by_component.values())


def render_evidence_coverage(atom_id: str, atom: dict[str, Any], atlas: Atlas) -> str:
    evidence_rows = atlas.evidence_by_claim.get(atom_id, [])
    components = evidence_component_status(atom, evidence_rows)
    if not evidence_rows and not components:
        return ""

    row_html = []
    for component in components:
        evidence = component.get("evidence", [])
        if evidence:
            evidence_text = "; ".join(
                f"{e.get('evidence_id')}: {e.get('relation')} ({e.get('strength')}, coverage {e.get('coverage')})"
                for e in evidence
            )
        else:
            evidence_text = "UNSUPPORTED COMPONENT - no admitted evidence"
        row_html.append(
            "<tr>"
            f"<td>{html.escape(str(component['componentID']))}</td>"
            f"<td>{html.escape(str(component['predicate']))}</td>"
            f"<td>{html.escape(evidence_text)}</td>"
            "</tr>"
        )

    evidence_items = []
    for row in evidence_rows:
        unaddressed = ", ".join(str(x) for x in row.get("unaddressed", [])) or "none declared"
        evidence_items.append(_li(
            f"{row.get('evidence_id')}: coverage {row.get('coverage')} - unaddressed: {unaddressed}. {row.get('method_note', '')}"
        ))

    return f"""
      <h4>Evidence Coverage</h4>
      <p><strong>Rule:</strong> Evidence strength is not evidence coverage. Evidence only propagates over the portion it actually supports.</p>
      <table class="evidence-coverage">
        <thead><tr><th>Component</th><th>Predicate</th><th>Admitted evidence</th></tr></thead>
        <tbody>{''.join(row_html)}</tbody>
      </table>
      <ul>{''.join(evidence_items) or '<li>No evidence coverage records admitted.</li>'}</ul>
"""


def render_resolution_section(atom_id: str, atom: dict[str, Any], atlas: Atlas) -> str:
    forward = atlas.forward.get(atom_id, [])
    backward = atlas.backward.get(atom_id, [])
    open_items = atlas.open_items_by_atom.get(atom_id, [])
    if not forward and not backward and not open_items and not atom.get("paperState") and not atom.get("publicationState"):
        return ""

    forward_html = "".join(render_relation(r) for r in forward) or "<li>None recorded</li>"
    backward_html = "".join(render_relation(r, inverse=True) for r in backward) or "<li>None recorded</li>"
    open_html = "".join(render_open_item(i) for i in open_items) or "<p>No open items recorded for this atom.</p>"
    evidence_html = render_evidence_coverage(atom_id, atom, atlas)
    return f"""
  <section class="atlas-resolution atlas-mode-current" data-principle="retroactive-resolution-non-retroactive-history">
    <style>
      .atlas-resolution .atlas-toggle button {{ margin-right: .5rem; }}
      .atlas-resolution.atlas-mode-original .current-state {{ display: none; }}
      .atlas-resolution.atlas-mode-current .paper-state {{ display: none; }}
    </style>
    <h2>Living Atlas Status</h2>
    <p><strong>Rule:</strong> Later work may change current standing, but it never rewrites the paper's historical state.</p>
    <div class="atlas-toggle" role="group" aria-label="State view">
      <button type="button" data-view="original" onclick="this.closest('.atlas-resolution').className='atlas-resolution atlas-mode-original'">Original Paper State</button>
      <button type="button" data-view="current" onclick="this.closest('.atlas-resolution').className='atlas-resolution atlas-mode-current'">Current Atlas State</button>
    </div>
    <section class="paper-state">
      <h3>At Publication</h3>
      <p><strong>Status then:</strong> {html.escape(original_status(atom))}</p>
    </section>
    <section class="current-state">
      <h3>Current Atlas State</h3>
      <p><strong>Status now:</strong> {html.escape(current_status(atom_id, atom, atlas))}</p>
      <h4>Forward Resolution</h4>
      <ul>{forward_html}</ul>
      <h4>Backward Resolution</h4>
      <ul>{backward_html}</ul>
      <h4>Open Items</h4>
      {open_html}
      {evidence_html}
    </section>
  </section>
"""
