#!/usr/bin/env python3
"""Build an HTML mind map for individual axiom atoms."""
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
AXIOMS = REPO / "axioms" / "01_canonical"
OUT = REPO / "_runtime" / "axiom_mindmap" / "axiom_mindmap.html"
MODE_CLASSIFICATION = REPO / "_docs" / "AXIOMS_PART1_MODE_CLASSIFICATION.md"
GLYPH_REL = "../../theophysics_glyphs/svg"


CLASS_COLORS = {
    "floor_axiom": "#4338ca",
    "definition": "#0f766e",
    "theorem": "#b45309",
    "mathematical": "#2563eb",
    "empirical_anchor": "#15803d",
    "empirical": "#15803d",
    "prediction": "#16a34a",
    "bridge": "#be123c",
    "boundary": "#be123c",
}

MODE_COLORS = {
    "AX_CORE": "#111827",
    "AX_DERIVED": "#7c2d12",
    "AX_SCAFFOLD": "#0369a1",
    "FW_EXTENDED": "#6d28d9",
    "HY_EVIDENCE": "#15803d",
    "DROP_DUPLICATE": "#991b1b",
    "UNCLASSIFIED": "#64748b",
}

MODE_GLYPHS = {
    "AX_CORE": "axiom",
    "AX_DERIVED": "proof",
    "AX_SCAFFOLD": "definition",
    "FW_EXTENDED": "mesh",
    "HY_EVIDENCE": "evidence",
    "DROP_DUPLICATE": "boundary",
    "UNCLASSIFIED": "claim",
}

CLASS_GLYPHS = {
    "floor_axiom": "axiom",
    "definition": "definition",
    "theorem": "proof",
    "mathematical": "equation",
    "empirical_anchor": "evidence",
    "empirical": "evidence",
    "prediction": "prediction",
    "bridge": "isomorphism",
    "boundary": "boundary",
}


def e(value: Any) -> str:
    return html.escape(str(value or ""))


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", value)


def glyph(name: str, label: str, css_class: str = "glyph") -> str:
    return f'<img class="{css_class}" src="{GLYPH_REL}/{e(name)}.svg" alt="{e(label)}" loading="lazy">'


def glyph_for_atom(atom: dict[str, Any]) -> str:
    name = MODE_GLYPHS.get(atom["mode"]) or CLASS_GLYPHS.get(atom["claimClass"], "claim")
    label = atom["mode"] if atom["mode"] != "UNCLASSIFIED" else atom["claimClass"]
    return glyph(name, label)


def load_axioms() -> list[dict[str, Any]]:
    classifications = load_mode_classification()
    atoms = []
    for path in sorted(AXIOMS.glob("*.jsonld")):
        data = json.loads(path.read_text(encoding="utf-8"))
        reg = data.get("axiomRegistry", {})
        edges = data.get("edges", [])
        atom_id = reg.get("axiomID") or data.get("nodeID") or path.stem
        mode_key = reg.get("oldID") or atom_id
        mode = classifications.get(mode_key) or classifications.get(atom_id) or {}
        atoms.append(
            {
                "path": path,
                "id": atom_id,
                "old": reg.get("oldID", ""),
                "name": data.get("name", atom_id),
                "claimClass": data.get("claimClass", "unclassified"),
                "plain": data.get("statementPlain", ""),
                "technical": data.get("statementTechnical", ""),
                "math": data.get("mathematicalForm", ""),
                "logicalForce": reg.get("logicalForce", ""),
                "leanKind": reg.get("leanKind", ""),
                "kernelRole": reg.get("kernelRole", ""),
                "risk": reg.get("riskLevel", "unknown"),
                "module": reg.get("moduleID", "M??"),
                "moduleTitle": reg.get("moduleTitle", "Unsorted"),
                "treeLevel": reg.get("treeLevel", ""),
                "spineRole": reg.get("spineRole", ""),
                "worldviews": reg.get("worldviewsEliminated", ""),
                "propagation": reg.get("propagationTest", ""),
                "kill": data.get("falsificationCondition", ""),
                "depends": [edge.get("target", "") for edge in edges if edge.get("type") == "dependsOn"],
                "nodeID": data.get("nodeID", ""),
                "mode": mode.get("mode", "UNCLASSIFIED"),
                "modeDecision": mode.get("decision", ""),
                "modeAnchor": mode.get("anchor", ""),
                "modeStatus": mode.get("status", ""),
                "modeWhy": mode.get("why", ""),
            }
        )
    return atoms


def load_mode_classification() -> dict[str, dict[str, str]]:
    if not MODE_CLASSIFICATION.exists():
        return {}
    current = ""
    out: dict[str, dict[str, str]] = {}
    section_re = re.compile(r"^##\s+(AX_CORE|AX_DERIVED|AX_SCAFFOLD|FW_EXTENDED|HY_EVIDENCE|DROP_DUPLICATE)\b")
    row_re = re.compile(r"^-\s+`([^`]+)`\s+\|\s+(.*?)\s+\|\s+decision=`([^`]+)`\s+\|\s+anchor=`([^`]+)`.*?status=`([^`]+)`\s+\|\s+why=(.*)$")
    for line in MODE_CLASSIFICATION.read_text(encoding="utf-8", errors="replace").splitlines():
        section = section_re.match(line)
        if section:
            current = section.group(1)
            continue
        row = row_re.match(line)
        if not current or not row:
            continue
        raw_id = row.group(1).strip()
        title = row.group(2).strip()
        item = {
            "mode": current,
            "title": title,
            "decision": row.group(3).strip(),
            "anchor": row.group(4).strip(),
            "status": row.group(5).strip(),
            "why": row.group(6).strip(),
        }
        if raw_id not in out or item["mode"] != "DROP_DUPLICATE":
            out[raw_id] = item
        ax_match = re.search(r"\b(AX-\d+[A-Za-z]?)\b", title)
        if ax_match:
            ax_id = ax_match.group(1)
            if ax_id not in out or item["mode"] != "DROP_DUPLICATE":
                out[ax_id] = item
        old_id_match = re.match(r"([A-Z]+[0-9]+(?:\.[0-9]+)?)\s+", title)
        if old_id_match:
            old_id = old_id_match.group(1)
            if old_id not in out or item["mode"] != "DROP_DUPLICATE":
                out[old_id] = item
    return out


def target_to_axiom_id(target: str) -> str:
    match = re.search(r"(AX-\d+[A-Za-z]?)", target or "")
    return match.group(1) if match else target


def build_html(atoms: list[dict[str, Any]]) -> str:
    by_module: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    reverse: dict[str, list[str]] = defaultdict(list)
    for atom in atoms:
        by_module[(atom["module"], atom["moduleTitle"])].append(atom)
        for dep in atom["depends"]:
            reverse[target_to_axiom_id(dep)].append(atom["id"])

    cards = []
    for (module, title), items in sorted(by_module.items()):
        cards.append(f'<section class="module" id="{e(safe_id(module))}">')
        cards.append(f'<h2><span>{e(module)}</span>{e(title)}</h2>')
        cards.append('<div class="grid">')
        for atom in items:
            color = MODE_COLORS.get(atom["mode"], CLASS_COLORS.get(atom["claimClass"], "#64748b"))
            deps = [target_to_axiom_id(dep) for dep in atom["depends"]]
            dependents = reverse.get(atom["id"], [])
            cards.append(
                f"""
<article class="card" data-class="{e(atom['claimClass'])}" data-mode="{e(atom['mode'])}" data-risk="{e(atom['risk'])}" data-module="{e(module)}" style="--accent:{color}">
  <button class="card-head" type="button" aria-expanded="false">
    {glyph_for_atom(atom)}
    <span class="id">{e(atom['id'])}</span>
    <span class="title">{e(atom['name'])}</span>
    <span class="badge">{e(atom['mode'])}</span>
    <span class="risk">{e(atom['risk'])}</span>
  </button>
  <div class="card-body">
    <p class="plain">{e(atom['plain'])}</p>
    <dl>
      <dt>Old ID</dt><dd>{e(atom['old']) or "None"}</dd>
      <dt>{glyph(MODE_GLYPHS.get(atom['mode'], 'claim'), 'Mode', 'row-glyph')} Mode</dt><dd>{e(atom['mode'])}</dd>
      <dt>Decision</dt><dd>{e(atom['modeDecision']) or "None"}</dd>
      <dt>Anchor</dt><dd>{e(atom['modeAnchor']) or "None"}</dd>
      <dt>Mode Status</dt><dd>{e(atom['modeStatus']) or "None"}</dd>
      <dt>Mode Why</dt><dd>{e(atom['modeWhy']) or "None"}</dd>
      <dt>{glyph(CLASS_GLYPHS.get(atom['claimClass'], 'claim'), 'Claim Class', 'row-glyph')} Claim Class</dt><dd>{e(atom['claimClass'])}</dd>
      <dt>Tree Level</dt><dd>{e(atom['treeLevel']) or "None"}</dd>
      <dt>Logical Force</dt><dd>{e(atom['logicalForce']) or "None"}</dd>
      <dt>{glyph('lean4', 'Lean Role', 'row-glyph')} Lean Role</dt><dd>{e(atom['leanKind'])} / {e(atom['kernelRole'])}</dd>
      <dt>{glyph('equation', 'Math Form', 'row-glyph')} Math Form</dt><dd>{e(atom['math']) or "None"}</dd>
      <dt>Depends On</dt><dd>{e(", ".join(deps) if deps else "None")}</dd>
      <dt>Used By</dt><dd>{e(", ".join(dependents[:12]) if dependents else "None")}</dd>
      <dt>{glyph('kill-condition', 'Kill Condition', 'row-glyph')} Kill Condition</dt><dd>{e(atom['kill']) or "None declared"}</dd>
      <dt>Propagation</dt><dd>{e(atom['propagation']) or "None declared"}</dd>
      <dt>Worldviews</dt><dd>{e(atom['worldviews']) or "None declared"}</dd>
    </dl>
  </div>
</article>"""
            )
        cards.append("</div></section>")

    total = len(atoms)
    classes = defaultdict(int)
    modes = defaultdict(int)
    risks = defaultdict(int)
    for atom in atoms:
        classes[atom["claimClass"]] += 1
        modes[atom["mode"]] += 1
        risks[atom["risk"]] += 1
    mode_chips = "".join(f'<button data-filter-mode="{e(k)}">{glyph(MODE_GLYPHS.get(k, "claim"), k, "mini-glyph")}{e(k)} <b>{v}</b></button>' for k, v in sorted(modes.items()))
    class_chips = "".join(f'<button data-filter-class="{e(k)}">{glyph(CLASS_GLYPHS.get(k, "claim"), k, "mini-glyph")}{e(k)} <b>{v}</b></button>' for k, v in sorted(classes.items()))
    risk_chips = "".join(f'<button data-filter-risk="{e(k)}">{e(k)} <b>{v}</b></button>' for k, v in sorted(risks.items()))

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Theophysics Axiom Mind Map</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Inter, Segoe UI, Arial, sans-serif; background:#f8fafc; color:#172033; }}
header {{ position:sticky; top:0; z-index:5; background:rgba(255,255,255,.94); border-bottom:1px solid #dbe3ee; padding:18px 24px 14px; backdrop-filter: blur(10px); }}
h1 {{ margin:0 0 6px; font-size:24px; letter-spacing:0; }}
.sub {{ margin:0; color:#526274; font-size:14px; max-width:920px; }}
.toolbar {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; align-items:center; }}
.toolbar input {{ min-width:260px; flex:1; padding:10px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:14px; }}
.toolbar button {{ border:1px solid #cbd5e1; background:#fff; border-radius:6px; padding:8px 10px; cursor:pointer; color:#203047; display:inline-flex; align-items:center; gap:6px; }}
.toolbar button.active {{ border-color:#111827; background:#111827; color:#fff; }}
.glyph {{ width:24px; height:24px; object-fit:contain; flex:0 0 auto; }}
.mini-glyph {{ width:16px; height:16px; object-fit:contain; flex:0 0 auto; }}
.row-glyph {{ width:16px; height:16px; object-fit:contain; vertical-align:-3px; margin-right:4px; }}
.toolbar button.active img {{ filter:brightness(0) invert(1); }}
main {{ padding:22px 24px 48px; }}
.legend {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:10px; margin-bottom:22px; }}
.legend div {{ background:#fff; border:1px solid #dbe3ee; border-radius:8px; padding:10px 12px; }}
.legend strong {{ display:flex; align-items:center; gap:6px; font-size:13px; margin-bottom:6px; }}
.module {{ margin:0 0 26px; }}
.module h2 {{ display:flex; gap:10px; align-items:baseline; font-size:18px; margin:0 0 12px; }}
.module h2 span {{ font-size:13px; color:#fff; background:#172033; border-radius:5px; padding:3px 7px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(310px,1fr)); gap:12px; }}
.card {{ background:#fff; border:1px solid #dbe3ee; border-left:6px solid var(--accent); border-radius:8px; overflow:hidden; box-shadow:0 1px 2px rgba(15,23,42,.05); }}
.card[hidden] {{ display:none; }}
.card-head {{ width:100%; display:grid; grid-template-columns:auto auto minmax(0,1fr) auto auto; gap:8px; align-items:center; text-align:left; background:#fff; border:0; padding:12px; cursor:pointer; }}
.id {{ font-weight:800; color:var(--accent); font-size:13px; }}
.title {{ font-weight:700; min-width:0; overflow-wrap:anywhere; }}
.badge,.risk {{ font-size:11px; border-radius:999px; padding:4px 7px; background:#edf2f7; color:#334155; white-space:nowrap; }}
.risk {{ background:#fff7ed; color:#9a3412; }}
.card-body {{ display:none; border-top:1px solid #e2e8f0; padding:12px; }}
.card.open .card-body {{ display:block; }}
.plain {{ margin:0 0 12px; font-size:14px; line-height:1.45; }}
dl {{ margin:0; display:grid; grid-template-columns:105px 1fr; gap:7px 10px; font-size:13px; }}
dt {{ font-weight:800; color:#475569; }}
dd {{ margin:0; overflow-wrap:anywhere; color:#1f2937; }}
@media (max-width: 640px) {{
  header, main {{ padding-left:14px; padding-right:14px; }}
  .card-head {{ grid-template-columns:auto auto 1fr; }}
  .badge,.risk {{ justify-self:start; }}
  dl {{ grid-template-columns:1fr; }}
  dt {{ margin-top:8px; }}
}}
</style>
</head>
<body>
<header>
  <h1>Theophysics Axiom Mind Map</h1>
  <p class="sub">Individual axiom pills mapped by module, class, risk, dependency, Lean role, and kill condition. This is not one giant chain; it is a field of inspectable axiom atoms.</p>
  <div class="toolbar">
    <input id="search" placeholder="Search axioms, statements, IDs, kill conditions..." aria-label="Search axioms">
    <button id="all" class="active">All <b>{total}</b></button>
    {mode_chips}
    {class_chips}
    {risk_chips}
  </div>
</header>
<main>
  <section class="legend">
    <div><strong>{glyph('claim', 'Claim Class', 'mini-glyph')} Claim Class</strong> What kind of axiom atom this is.</div>
    <div><strong>{glyph('axiom', 'Mode', 'mini-glyph')} Mode</strong> Whether it is strict core, derived, scaffold, framework, evidence, or duplicate.</div>
    <div><strong>{glyph('lean4', 'Lean Role', 'mini-glyph')} Lean Role</strong> Whether it is a candidate axiom, theorem, definition, or model field.</div>
    <div><strong>{glyph('kill-condition', 'Kill Condition', 'mini-glyph')} Kill Condition</strong> What would break this exact axiom atom.</div>
    <div><strong>{glyph('mesh', 'Dependencies', 'mini-glyph')} Dependencies</strong> Local links only; no forced whole-chain flattening.</div>
  </section>
  {''.join(cards)}
</main>
<script>
const cards = [...document.querySelectorAll('.card')];
const search = document.querySelector('#search');
let classFilter = '';
let modeFilter = '';
let riskFilter = '';
function applyFilters() {{
  const q = search.value.trim().toLowerCase();
  cards.forEach(card => {{
    const text = card.innerText.toLowerCase();
    const okText = !q || text.includes(q);
    const okClass = !classFilter || card.dataset.class === classFilter;
    const okMode = !modeFilter || card.dataset.mode === modeFilter;
    const okRisk = !riskFilter || card.dataset.risk === riskFilter;
    card.hidden = !(okText && okClass && okMode && okRisk);
  }});
}}
document.querySelectorAll('[data-filter-mode]').forEach(btn => btn.addEventListener('click', () => {{
  modeFilter = modeFilter === btn.dataset.filterMode ? '' : btn.dataset.filterMode;
  classFilter = ''; riskFilter = '';
  document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
  if (modeFilter) btn.classList.add('active'); else document.querySelector('#all').classList.add('active');
  applyFilters();
}}));
document.querySelectorAll('[data-filter-class]').forEach(btn => btn.addEventListener('click', () => {{
  classFilter = classFilter === btn.dataset.filterClass ? '' : btn.dataset.filterClass;
  modeFilter = ''; riskFilter = '';
  document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
  if (classFilter) btn.classList.add('active'); else document.querySelector('#all').classList.add('active');
  applyFilters();
}}));
document.querySelectorAll('[data-filter-risk]').forEach(btn => btn.addEventListener('click', () => {{
  riskFilter = riskFilter === btn.dataset.filterRisk ? '' : btn.dataset.filterRisk;
  modeFilter = ''; classFilter = '';
  document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
  if (riskFilter) btn.classList.add('active'); else document.querySelector('#all').classList.add('active');
  applyFilters();
}}));
document.querySelector('#all').addEventListener('click', () => {{
  modeFilter = ''; classFilter = ''; riskFilter = ''; search.value = '';
  document.querySelectorAll('.toolbar button').forEach(b => b.classList.remove('active'));
  document.querySelector('#all').classList.add('active');
  applyFilters();
}});
search.addEventListener('input', applyFilters);
cards.forEach(card => card.querySelector('.card-head').addEventListener('click', () => {{
  card.classList.toggle('open');
  card.querySelector('.card-head').setAttribute('aria-expanded', card.classList.contains('open'));
}}));
</script>
</body>
</html>
"""


def main() -> None:
    atoms = load_axioms()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_html(atoms), encoding="utf-8")
    print(OUT)
    print(f"axiom atoms: {len(atoms)}")


if __name__ == "__main__":
    main()
