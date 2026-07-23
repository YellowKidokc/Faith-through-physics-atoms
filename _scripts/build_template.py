"""
FAITH THROUGH PHYSICS — Template Builder
Creates the master domain template with all 14 stage folders.
Each folder gets a README with AI instructions and checklist.

Usage: python build_template.py
Output: C:\theophysics\CANONICAL\_template\
"""
import os

base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_template')

stages = [
    ('00_inbox_working',  'Raw thinking, voice dumps, unsorted',           'EXPLORE',    'raw'),
    ('01_canonical',      'Locked truth, proven claims',                   'CLAIM',      'claim'),
    ('02_paradigm',       'What this breaks, new mental model',            'REFRAME',    'paradigm'),
    ('03_synthesis',      'How it connects to other domains',              'CONNECT',    'bridge'),
    ('04_hypothesis',     'If true, then THIS must follow',                'PREDICT',    'prediction'),
    ('05_evidence',       'External research, LLM, wiki, data',           'COMPARE',    'evidence'),
    ('06_falsification',  'Kill conditions, what would break it',          'TEST',       'kill'),
    ('07_paper',          'Formal doctoral-level treatment',               'PROVE',      'paper'),
    ('08_objections',     'Strongest pushback, steelmanned',               'DEFEND',     'objection'),
    ('09_everyday',       'Plain language Monday morning version',         'TRANSLATE',  'translation'),
    ('10_worldcheck',     'Everyday version pressure-tested',              'VERIFY',     'check'),
    ('11_articles',       'Narrative story form, readable',                'TELL',       'article'),
    ('12_audience',       'SEO, social, widest reach, toolkits',           'REACH',      'reach'),
    ('13_fulfilled',      'Did it hold, what happened',                    'CONFIRM',    'result'),
]

checklists = {
    '00': [
        'Raw content deposited with date and source',
        'AI session attribution noted',
        'Domain identified for routing',
    ],
    '01': [
        'Formal claim stated in one sentence',
        'claimID assigned (tp:DOMAIN/L#/C#)',
        'statementTechnical written',
        'statementPlain written (descent rule: MANDATORY)',
        'Derivation chain documented',
        'Mathematical formalization present',
        'Axiom dependencies mapped (edges with dependsOn)',
        'falsificationCondition defined',
        'No contradiction with other canonical claims',
        'David has approved',
    ],
    '02': [
        'Old paradigm documented (what people currently believe)',
        'Explicit break statement written (what changes)',
        'New mental model described (how to think now)',
        'Historical precedent identified',
        'claimRef edge points to 01_canonical node',
    ],
    '03': [
        'Cross-domain mapping is formal (not analogy)',
        'bridgeGrade assigned: identity | isomorphism | analogy | metaphorical',
        'Structural correspondence proved',
        'Bidirectional prediction tested',
        'Boundary conditions documented',
        'Master Equation connection shown',
        'Edges connect claims in BOTH domains',
        'Propagation flag set correctly on edges',
    ],
    '04': [
        'Prediction is specific and measurable',
        'Magnitude predicted (not just direction)',
        'Test methodology proposed',
        'Confidence level stated',
        'derivedFrom edge points to 01_canonical claim',
        'Timeframe set: testable_now | future | mathematical',
    ],
    '05': [
        'External sources gathered',
        'citationStatus set: verified | unverified | retracted',
        'Competing frameworks documented',
        'LLM consensus checked (what AI says unprompted)',
        'Raw data preserved',
        'Source notes separated from conclusions',
        'relevantClaim edge points to claim or prediction',
    ],
    '06': [
        'Kill condition stated explicitly',
        'At least one kill attempt documented',
        'Strongest counter-argument steelmanned (/EAST)',
        'Boundary conditions identified',
        'Failure modes listed',
        'Outcome recorded: survived | weakened | boundary_found | falsified',
        'If falsified: propagation triggered to all dependents',
    ],
    '07': [
        'Follows doctoral template (13 sections)',
        'Abstract: problem, claim, method, result, limitation',
        'Core claim referenced (edge to 01_canonical)',
        'Scope explicitly states what is NOT covered',
        'Argument chain complete with no gaps',
        'Evidence referenced (edges to 05_evidence nodes)',
        'Falsification referenced (edges to 06 nodes)',
        'Citations identified and accessible',
        'EVERYDAY BRIDGE section at end (MANDATORY — links to 09)',
    ],
    '08': [
        'Objections steelmanned (strongest form, not strawmen)',
        'Point-by-point responses written',
        'Unresolved items documented honestly',
        'Source attribution for each objection',
        'targetClaim edge points to claim or paper',
    ],
    '09': [
        'Non-expert can understand this (no jargon test)',
        'Practical application stated (Monday morning)',
        'Analogy or metaphor provided',
        'So-what question answered',
        'sourceClaim edge points to 01_canonical',
        'THIS IS THE FLOOR — if canonical, this stage is MANDATORY',
    ],
    '10': [
        'Real-world reactions gathered or simulated',
        'Simplification audit done (anything lost?)',
        'Cultural framing differences noted',
        'Fact-check passed',
        'sourceTranslation edge points to 09_everyday node',
    ],
    '11': [
        'Above high school reading level, below PhD',
        'Narrative structure present (human anchor, story arc)',
        'Cross-references to related articles in other domains',
        'Reading level verified',
        'claimRefs edges point to claims used in narrative',
    ],
    '12': [
        'Impact assessment written (how does this change lives)',
        'No barrier to entry (accessible to anyone)',
        'Audience can ACT on this (not just read)',
        'Formatted for sharing (platform-appropriate)',
        'Legal/medical/financial warnings if toolkit content',
        'sourceArticle edge points to 11 or 09',
    ],
    '13': [
        'Results documented with actual data',
        'Prediction accuracy assessed',
        'Failed predictions logged (intellectual honesty)',
        'Revision triggers identified',
        'predictionRef edge points to 04_hypothesis',
        'If confirmed: strengthens upstream 01_canonical',
        'If failed: triggers new 00_inbox_working entry',
    ],
}

# NLP and API hooks per stage
nlp_hooks = {
    '00': 'NLP: auto-classify domain from raw text. API: none.',
    '01': 'NLP: extract formal claim statement. API: Lean 4 verification check.',
    '02': 'NLP: compare old vs new paradigm framing. API: none.',
    '03': 'NLP: detect shared equation structures across domains. API: graph query for shared axiom roots.',
    '04': 'NLP: extract testable prediction sentence. API: none.',
    '05': 'NLP: source credibility scoring. API: web search for competing frameworks, LLM consensus check.',
    '06': 'NLP: steelman strength scoring. API: none.',
    '07': 'NLP: reading level assessment (Flesch-Kincaid). API: citation verification.',
    '08': 'NLP: objection severity classification. API: none.',
    '09': 'NLP: jargon detection (flag any framework-specific terms). API: readability scoring.',
    '10': 'NLP: sentiment analysis on real-world reactions. API: web search for mainstream framing.',
    '11': 'NLP: narrative arc detection. API: cross-reference validation.',
    '12': 'NLP: SEO keyword extraction. API: social media formatting.',
    '13': 'NLP: outcome classification (confirmed/partial/failed). API: data validation.',
}

os.makedirs(base, exist_ok=True)

for folder, desc, verb, node_type in stages:
    path = os.path.join(base, folder)
    os.makedirs(path, exist_ok=True)
    prefix = folder[:2]
    items = checklists.get(prefix, [])
    hooks = nlp_hooks.get(prefix, '')
    readme_path = os.path.join(path, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f'# {folder}\n')
        f.write(f'## {desc}\n\n')
        f.write(f'**Action:** {verb}  \n')
        f.write(f'**Node type:** {node_type}  \n')
        f.write(f'**Status:** EMPTY  \n\n')
        f.write('---\n\n')
        f.write('## AI Checklist\n\n')
        for item in items:
            f.write(f'- [ ] {item}\n')
        f.write(f'\n---\n\n')
        f.write(f'## NLP / API Hooks\n\n')
        f.write(f'{hooks}\n\n')
        f.write('---\n\n')
        f.write(f'## Files\n\n')
        f.write(f'Place .jsonld atoms and their generated .html pills here.\n')
        f.write(f'The .jsonld is source of truth. Never edit .html directly.\n\n')
        f.write('---\n')
        f.write('*Faith Through Physics | POF 2828 | Domain Architecture v11*\n')

# Create _theological companion folder
theo_path = os.path.join(base, '_theological')
os.makedirs(theo_path, exist_ok=True)

theo_readme = os.path.join(theo_path, 'README.md')
with open(theo_readme, 'w', encoding='utf-8') as f:
    f.write('# _theological\n')
    f.write('## The root system underneath this domain\n\n')
    f.write('This is NOT a stage in the 14-stage arc.\n')
    f.write('This is the COMPANION — the theological grounding\n')
    f.write('that runs underneath every stage.\n\n')
    f.write('The arc is the ripening process.\n')
    f.write('This folder is the root system.\n\n')
    f.write('---\n\n')
    f.write('## Contents\n\n')
    f.write('- **scripture.md** — relevant Scripture passages for this domain\n')
    f.write('- **doctrine.md** — theological tradition and doctrinal grounding\n')
    f.write('- **bridge.md** — how the theology maps to this domain\'s claims\n')
    f.write('- **christ-type.md** — Jesus as pattern in this domain\'s vocabulary\n\n')
    f.write('---\n\n')
    f.write('## AI Checklist\n\n')
    f.write('- [ ] At least one Scripture passage identified for this domain\n')
    f.write('- [ ] Christ-type written (Jesus in this domain\'s language)\n')
    f.write('- [ ] Theological bridge connects to 01_canonical claims\n')
    f.write('- [ ] An everyday person can see Jesus in this domain\n\n')
    f.write('---\n\n')
    f.write('## Why This Exists\n\n')
    f.write('Every domain reaches back to Jesus. This folder is where\n')
    f.write('that connection is documented. Not as a stage that content\n')
    f.write('passes through, but as the ground everything grows from.\n\n')
    f.write('The physicist reading physics/ finds Jesus here.\n')
    f.write('The economist reading economics/ finds Jesus here.\n')
    f.write('The parent reading education/ finds Jesus here.\n\n')
    f.write('All nodes reach back.\n\n')
    f.write('---\n')
    f.write('*Faith Through Physics | POF 2828*\n')

# Create the four template files
for fname, header, prompt in [
    ('scripture.md', 'Scripture Passages', 'List relevant Scripture passages for this domain.\nInclude book, chapter, verse, and a brief note on relevance.'),
    ('doctrine.md', 'Doctrinal Grounding', 'What theological tradition or doctrine grounds this domain?\nHow has the church historically understood this topic?'),
    ('bridge.md', 'Theological Bridge', 'How does the theology map to the canonical claims in this domain?\nWhat is the structural connection between Scripture and the equations?'),
    ('christ-type.md', 'Christ as Pattern', 'How does Jesus appear in this domain\'s vocabulary?\nWhat is the "Jesus story" for this field?\n\nExample for education: Jesus picked fishermen — untrained,\nlow-status, high-transmission-fidelity.\n\nExample for economics: Jesus and the rich young ruler —\nattachment vs source-coupled provision.\n\nWrite the Christ-type for THIS domain.'),
]:
    fpath = os.path.join(theo_path, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(f'# {header}\n\n')
        f.write(f'{prompt}\n\n')
        f.write('---\n')
        f.write('*Faith Through Physics | POF 2828*\n')

# Create desktop.ini for folder icons (Windows)
# These use standard Windows icon indices for visual status
for folder, desc, verb, node_type in stages:
    path = os.path.join(base, folder)
    ini_path = os.path.join(path, 'desktop.ini')
    with open(ini_path, 'w', encoding='utf-8') as f:
        f.write('[.ShellClassInfo]\n')
        f.write(f'InfoTip={desc}\n')
        # Icon index 4 = empty folder icon (will be customized later)
        f.write('IconResource=%SystemRoot%\\system32\\shell32.dll,4\n')

print(f'DONE: Template built at {base}')
print(f'  14 stage folders with README checklists')
print(f'  _theological companion folder with 4 files')
print(f'  NLP/API hooks in each README')
print(f'  desktop.ini for folder icons')
