#!/usr/bin/env python3
"""Compile all canonical-node JSON results into one markdown report."""
import json, os, glob, sys

sys.stdout.reconfigure(encoding='utf-8')

BATCHES = [
    'D:/GitHub/Faith-through-physics-atoms/_runtime/full-audit-batch1/json',
    'D:/GitHub/Faith-through-physics-atoms/_runtime/full-audit-batch2/json',
    'D:/GitHub/Faith-through-physics-atoms/_runtime/full-audit-batch3/json',
    'D:/GitHub/Faith-through-physics-atoms/_runtime/me-audit/json',
    'D:/GitHub/Faith-through-physics-atoms/_runtime/deepseek-meta-audit/json',
]

rows = []
seen = set()
for b in BATCHES:
    for f in sorted(glob.glob(os.path.join(b, '*.json'))):
        try:
            d = json.load(open(f, encoding='utf-8'))
            key = d.get('source_id', os.path.basename(f))
            if key in seen:
                continue
            seen.add(key)
            cls = d.get('classification', {})
            risk = d.get('risk', {})
            dg = d.get('dg_protocol', {})
            node = d.get('canonical_node', {})
            rows.append({
                'source_id': key,
                'title': d.get('title', '?'),
                'grade': cls.get('grade', '?'),
                'proof': cls.get('proof_label', '?'),
                'action': cls.get('recommended_atom_action', '?'),
                'claim_class': cls.get('claim_class', '?'),
                'state': dg.get('dg6_state', '?'),
                'admissible': dg.get('dg7_admissible', '?'),
                'closure': dg.get('dg8_closure_pass', '?'),
                'axiom': node.get('axiom', ''),
                'boundary': node.get('boundary', []),
                'test': node.get('test', []),
                'risks': risk.get('overstatement_risks', []),
                'kills': risk.get('kill_conditions', []),
                'lean_target': risk.get('lean_target', ''),
                'summary': d.get('plain_summary', ''),
            })
        except Exception:
            pass

rows.sort(key=lambda r: r['grade'])

OUT = 'D:/GitHub/Faith-through-physics-atoms/_runtime/FULL_AUDIT_REPORT.md'

with open(OUT, 'w', encoding='utf-8') as md:
    md.write('# Theophysics Canonical Node Audit Report\n')
    md.write(f'## {len(rows)} atoms processed | Generated 2026-08-10\n\n')
    md.write('---\n\n')

    # Summary table
    grades = {}
    for r in rows:
        grades[r['grade']] = grades.get(r['grade'], 0) + 1
    md.write('## Grade Summary\n\n')
    md.write('| Grade | Count |\n|---|---|\n')
    for g in sorted(grades.keys()):
        md.write(f'| {g} | {grades[g]} |\n')
    md.write(f'| **Total** | **{len(rows)}** |\n\n')

    # Full table
    md.write('## All Atoms by Grade\n\n')
    md.write('| Grade | Proof Label | State | Source | Title | Action |\n')
    md.write('|---|---|---|---|---|---|\n')
    for r in rows:
        title = r['title'][:55].replace('|', '//')
        md.write(f"| {r['grade']} | {r['proof']} | {r['state']} | {r['source_id'][:40]} | {title} | {r['action'][:25]} |\n")

    md.write('\n---\n\n')

    # Per-atom detail
    md.write('## Per-Atom Detail\n\n')
    for r in rows:
        md.write(f"### {r['title']}\n")
        md.write(f"**Source:** `{r['source_id']}`\n\n")
        md.write(f"**Grade:** {r['grade']} | **Proof:** {r['proof']} | **Class:** {r['claim_class']}\n\n")
        md.write(f"**State:** {r['state']} | **Admissible:** {r['admissible']} | **Closure:** {r['closure']}\n\n")
        if r['axiom']:
            md.write(f"**Axiom:** {r['axiom'][:200]}\n\n")
        if r['summary']:
            md.write(f"**Summary:** {r['summary'][:300]}\n\n")
        if r['risks']:
            risks = r['risks'] if isinstance(r['risks'], list) else [r['risks']]
            md.write('**Overstatement Risks:**\n')
            for risk in risks[:3]:
                md.write(f'- {str(risk)[:150]}\n')
            md.write('\n')
        if r['kills']:
            kills = r['kills'] if isinstance(r['kills'], list) else [r['kills']]
            md.write('**Kill Conditions:**\n')
            for k in kills[:3]:
                md.write(f'- {str(k)[:150]}\n')
            md.write('\n')
        if r['lean_target']:
            md.write(f"**Lean Target:** {r['lean_target'][:200]}\n\n")
        md.write('---\n\n')

print(f'Wrote {len(rows)} atoms to {OUT}')
