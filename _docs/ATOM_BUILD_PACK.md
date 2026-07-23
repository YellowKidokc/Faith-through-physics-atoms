# CODEX BUILD PACK: CLAIM ATOM SYSTEM
## Task: Build the atom builder, renderer, and graph connector
## From: David Lowe + Claude Opus | July 23, 2026
## For: Codex CLI agent

---

## WHAT YOU'RE BUILDING

Three tools that work together:

1. **atom_builder.py** — Interactive CLI that walks you through 
   creating a claim atom. Outputs .jsonld file.
2. **atom_renderer.py** — Reads .jsonld, generates collapsible 
   HTML pill. Outputs .html file next to the .jsonld.
3. **atom_graph.py** — Reads ALL .jsonld files across all domains,
   builds in-memory graph, answers connection queries.

All three live at: C:\theophysics\scripts\atoms\

---

## REFERENCE FILES (read these first)

- Architecture spec: C:\theophysics\_CANON\THEOPHYSICS_ARCHITECTURE_v11_CANONICAL.md
- Node type taxonomy: C:\theophysics\_CANON\CLAIM_ATOM_NODE_TYPES.md
- Existing atom standard: \\192.168.2.50\h_hp\Desktop\Files\claim-atom-standard-1.0\
- Existing vocab: \\192.168.2.50\h_hp\Desktop\Files\claim-atom-standard-1.0\tp-standard\vocab\context.jsonld
- Example atom: \\192.168.2.50\h_hp\Desktop\Files\claim-atom-standard-1.0\tp-standard\claims\A042\L9\C1.jsonld

---

## TOOL 1: atom_builder.py

Interactive Python CLI. No dependencies beyond stdlib + json.

### Usage:
```
python atom_builder.py --domain education --stage 01_canonical
python atom_builder.py --domain physics --stage 03_synthesis
python atom_builder.py --domain christian-life --stage 09_everyday
```

### Flow:
1. Accept --domain and --stage as args
2. Determine node type from stage (see NODE_TYPES below)
3. Prompt for required fields based on node type
4. Prompt for optional fields
5. Auto-generate:
   - @id (URL pattern: faiththruphysics.com/claims/DOMAIN/STAGE/ID)
   - claimID (tp:DOMAIN/STAGE/ID)
   - dateCreated (today)
   - dateModified (today)
6. Write .jsonld to C:\theophysics\PRODUCTION\[domain]\[stage]\[id].jsonld
7. Call atom_renderer.py to generate .html pill next to it
8. Print summary: what was created, where it lives, what it connects to

### Node type determines required fields:


```
NODE_TYPES = {
    "00_inbox_working": {
        "type": "raw",
        "required": ["source", "rough_domain", "raw_text"],
        "optional": ["tags"]
    },
    "01_canonical": {
        "type": "claim",
        "note": "ONLY node type that gets claimID. Everything else gets nodeID only.",
        "required": [
            "claimID",  # tp:DOMAIN/L#/C# — unique to claim nodes
            "statementTechnical", "statementPlain",
            "claimClass",  # floor-axiom|definition|theorem|bridge|empirical-anchor|prediction|boundary
            "domainType", "falsificationCondition"
        ],
        "optional": [
            "axiomRoot", "edges", "derivationChain",
            "mathematicalForm", "verificationStatus",
            "kernelChecked", "challengeStatus"
        ]
    },
    "02_paradigm": {
        "type": "paradigm",
        "required": ["oldParadigm", "breakStatement", "newParadigm", "claimRef"],
        "optional": ["historicalPrecedent"]
    },
    "03_synthesis": {
        "type": "bridge",
        "required": [
            "sourceDomain", "targetDomain", "bridgeGrade",
            # structural_identity|structural_isomorphism|structural_analogy|metaphorical
            "mappingProof", "claimRef"
        ],
        "optional": ["bidirectionalTest", "boundaryConditions", "masterEquationLink"]
    },
    "04_hypothesis": {
        "type": "prediction",
        "required": ["prediction", "derivedFrom", "testMethod"],
        "optional": ["predictedMagnitude", "confidenceLevel", "timeframe"]
    },
    "05_evidence": {
        "type": "evidence",
        "note": "NOT a claim. Node around a claim. No statementTechnical/Plain required.",
        "required": ["sourceType", "sourceRef", "relevantClaim", "citationStatus"],
        # sourceType: academic|LLM|wiki|dataset|competing_framework
        # citationStatus: verified|unverified|retracted
        "optional": ["dataPoints", "conclusionSeparate"]
    },
    "06_falsification": {
        "type": "kill",
        "required": ["killCondition", "targetClaim", "outcome"],
        # outcome: survived|weakened|boundary_found|falsified
        "optional": ["attemptDescription", "counterArgument", "boundaryDiscovered"]
    },
    "07_paper": {
        "type": "paper",
        "required": ["abstract", "coreClaimRef", "scope", "argumentChain", "everydayBridge"],
        "optional": ["definitions", "priorWork", "evidenceRefs", "falsificationRefs", "objectionRefs"]
    },
    "08_objections": {
        "type": "objection",
        "required": ["objection", "strength", "response", "targetClaim"],
        # strength: serious|moderate|common_misunderstanding
        "optional": ["objectionSource", "status"]
        # status: answered|unresolved|partial
    },
    "09_everyday": {
        "type": "translation",
        "required": ["plainStatement", "soWhat", "sourceClaim"],
        "optional": ["practicalApplication", "analogy", "readingLevel"]
    },
    "10_worldcheck": {
        "type": "check",
        "required": ["sourceTranslation", "factCheckResult"],
        "optional": ["reactionsSummary", "mainstreamFraming", "simplificationAudit"]
    },
    "11_articles": {
        "type": "article",
        "required": ["seriesID", "narrativeArc", "claimRefs"],
        "optional": ["seriesNumber", "humanAnchor", "crossRefs", "readingLevel", "bridgeRefs"]
    },
    "12_audience": {
        "type": "reach",
        "required": ["format", "sourceArticle", "impactStatement"],
        # format: social_post|video_script|infographic|one_pager|toolkit|podcast_outline|SEO_page
        "optional": ["actionItems", "legalWarning"]
    },
    "13_fulfilled": {
        "type": "result",
        "required": ["predictionRef", "outcome", "data"],
        # outcome: confirmed|partial|failed|pending
        "optional": ["accuracy", "revisionTrigger", "realWorldOutcome"]
    }
}
```

### ID Generation:
- Pattern: [DOMAIN]-[STAGE_NUM]-[AUTO_INCREMENT].jsonld
- Example: education-01-001.jsonld, physics-03-012.jsonld
- Script scans existing files in the target folder to find next number

### Connection prompts:
When building a node, the builder should prompt:
- "What claim does this depend on?" → shows list of existing 01_canonical atoms
- "What domain does this bridge to?" → shows list of existing domains
- "What prediction does this fulfill?" → shows list of existing 04_hypothesis atoms

This makes connections EASY — pick from a list, don't type URLs.

---

## TOOL 2: atom_renderer.py

Reads .jsonld, outputs .html pill (collapsible block).

### Usage:
```
python atom_renderer.py education-01-001.jsonld
python atom_renderer.py --all education  # renders all atoms in a domain
python atom_renderer.py --all            # renders everything
```


### HTML Pill Template:

The pill renders as a collapsible block. Cathedral aesthetic 
(dark bg, gold accents). Closed state shows one line. 
Open state shows all fields.

```html
<div class="atom-pill" data-atom-id="education-01-001" 
     data-domain="education" data-stage="01_canonical"
     data-status="verified">
  
  <!-- CLOSED STATE (always visible) -->
  <div class="pill-header" onclick="togglePill(this)">
    <span class="pill-badge">CLAIM</span>
    <span class="pill-status verified">VERIFIED</span>
    <span class="pill-title">Law 9 Moral Conservation — Claim 1</span>
    <span class="pill-toggle">▶</span>
  </div>
  
  <!-- OPEN STATE (hidden until clicked) -->
  <div class="pill-body" style="display:none;">
    
    <div class="pill-section">
      <h4>Technical Statement</h4>
      <p class="technical">Time-translation symmetry preserved 
      in the moral domain implies...</p>
    </div>
    
    <div class="pill-section">
      <h4>Plain Language</h4>
      <p class="plain">If the moral laws don't change over time, 
      then something moral is conserved...</p>
    </div>
    
    <div class="pill-section">
      <h4>Kill Condition</h4>
      <p class="kill">Exhibit a moral-domain transformation that 
      preserves the Lagrangian but yields no conserved current...</p>
    </div>
    
    <div class="pill-section">
      <h4>Dependencies</h4>
      <ul class="deps">
        <!-- auto-populated from dependsOn field -->
      </ul>
    </div>
    
    <div class="pill-section">
      <h4>Verification</h4>
      <p>Status: <span class="verified">machine-verified</span> 
      | System: Lean 4 | Kernel: checked</p>
    </div>
    
    <div class="pill-meta">
      Domain: education | Stage: 01_canonical | Class: theorem
      | Created: 2026-02-14 | Modified: 2026-07-22
    </div>
    
  </div>
</div>
```

### CSS (cathedral aesthetic):
- Background: #0a0a0a
- Gold accents: #d4af37
- Status badges: green=verified, yellow=draft, red=falsified, 
  blue=machine-verified, gray=pending
- Font: system sans-serif, 14px body, 12px meta
- Pill border-left: 3px solid colored by node type
  (gold=claim, blue=bridge, green=translation, red=kill, 
   purple=paper, orange=prediction)
- Transition: smooth slide-down on open

---

## TOOL 3: atom_graph.py

Reads all .jsonld files, builds connection graph, answers queries.

### Usage:
```
python atom_graph.py --scan                    # build graph from all atoms
python atom_graph.py --connections education    # show all connections for a domain
python atom_graph.py --bridges education economics  # find bridges between two domains
python atom_graph.py --roots                   # show all axiom roots and what depends on them
python atom_graph.py --orphans                 # find atoms with no connections
python atom_graph.py --missing-plain           # find atoms without statementPlain (unfinished descent)
python atom_graph.py --propagate-falsify ID    # simulate: if this atom is falsified, what breaks?
python atom_graph.py --stats                   # summary: atoms per domain, per stage, connection density
```

### Graph structure:
- Nodes: every .jsonld file
- Edges: dependsOn, feedsInto, bridgesTo, challenges, expands, forksFrom
- Edge weights: bridgeGrade determines propagation
  - structural_identity: propagates fully
  - structural_isomorphism: propagates fully
  - structural_analogy: does NOT propagate
  - metaphorical: does NOT propagate

### Output format:
- Console: human-readable summary
- JSON: --json flag outputs machine-readable graph
- DOT: --dot flag outputs Graphviz DOT for visualization

### The key queries for AI hop-in:

```
# "How does education connect to economics?"
python atom_graph.py --bridges education economics

Output:
  BRIDGE: education-03-001 ↔ economics-03-004
    Type: structural_identity
    Shared root: fiat_inflation_equation
    Grade: PROPAGATES (if one falls, other is flagged)

  BRIDGE: education-03-002 ↔ economics-01-007  
    Type: structural_analogy
    Shared concept: Goodhart's Law
    Grade: ILLUSTRATIVE (does not propagate)
```

```
# "What has unfinished descent?"
python atom_graph.py --missing-plain

Output:
  physics-01-003: statementPlain is EMPTY
  master-equation-01-001: statementPlain is EMPTY
  consciousness-04-002: no 09_everyday node found
  
  Total: 47 atoms missing plain versions
  Unfinished descent: 23% of canonical claims
```

```
# "If I falsify this claim, what breaks?"
python atom_graph.py --propagate-falsify education-01-001

Output:
  DIRECT dependents (would be flagged upstream-falsified):
    education-04-001 (prediction)
    education-07-001 (paper)
    education-03-001 (bridge to economics)
  
  CROSS-DOMAIN propagation (via structural_identity bridges):
    economics-01-007 (shares fiat inflation root)
  
  SAFE (analogy bridges, do not propagate):
    psychology-03-005 (analogy only)
  
  Total impact: 4 atoms flagged, 1 cross-domain, 1 safe
```

---

## PRODUCTION PATH

All atoms live inside the domain folder structure:

```
C:\theophysics\PRODUCTION\
├── education\
│   ├── 01_canonical\
│   │   ├── education-01-001.jsonld    ← atom
│   │   ├── education-01-001.html      ← rendered pill
│   │   └── README.md                  ← stage checklist
│   ├── 03_synthesis\
│   │   ├── education-03-001.jsonld
│   │   └── education-03-001.html
│   └── ...
├── economics\
│   ├── 01_canonical\
│   │   ├── economics-01-001.jsonld
│   │   └── economics-01-001.html
│   └── ...
```

The graph scanner walks C:\theophysics\PRODUCTION\ recursively,
finds all .jsonld files, and builds the graph from their edges.

---

## BUILD ORDER

1. atom_builder.py first (you need atoms before you can render or graph them)
2. atom_renderer.py second (generates pills from atoms)
3. atom_graph.py third (needs a population of atoms to be useful)

---

## DEPENDENCIES

- Python 3.10+
- json (stdlib)
- os, glob, pathlib (stdlib)
- argparse (stdlib)
- NO external packages for builder and renderer
- Optional for graph: networkx (pip install networkx) for advanced graph ops
- Optional for graph: graphviz (pip install graphviz) for DOT output

---

## THE RULE

The atom is source of truth. The HTML pill is generated.
Never edit HTML directly. Edit the .jsonld, regenerate.

The atom carries its own meaning. The folder gives it context.
The graph gives it connections. The pill gives it a face.

---

_Theophysics Research Initiative | POF 2828_
_Claim Atom Standard 1.0 + Domain Architecture v11_
