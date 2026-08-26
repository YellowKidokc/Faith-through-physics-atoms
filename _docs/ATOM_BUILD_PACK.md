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


---

## NEW NODE TYPES (v2.1 — Public Descent Layer)

Added: 2026-07-24 by Claude Opus + GPT correction
v2.0 atomized delivery formats (SEO, social, FAQ, glossary, etc).
GPT correctly identified this as container proliferation, not knowledge
structure. v2.1 collapses those back into reach.format variants and
adds only the genuinely missing types: question, series, audienceProfile.

Rule: atomize the descent PROCESS, not the delivery FORMAT.

---

### QUESTION NODE (genuinely new)

The public starts with questions, not claims. This is the entry point
for the entire public descent chain.

```
NODE_TYPES["question"] = {
    "type": "question",
    "required": [
        "question",              # the actual question a person asks
        "askedBy",               # audience type: skeptic, parent, student, pastor, etc
        "questionContext",       # public_debate|personal_crisis|academic_inquiry|pastoral_care|
                                 # family_conversation|online_comment|classroom|self_study
        "sourceClaims"           # edges to claim atoms that answer this question
    ],
    "optional": [
        "timeBudget",            # how long the person has: 60_seconds, 5_minutes, 30_minutes
        "priorKnowledge",        # none|low|moderate|high
        "audienceProfileRef",    # edge to reusable audience profile
        "urgency"                # casual|important|crisis
    ]
}
```

### SERIES NODE (genuinely new)

Defines article order for breadcrumb generation and series navigation.
Breadcrumbs are computed from this — no separate authoring.

```
NODE_TYPES["series"] = {
    "type": "series",
    "required": [
        "seriesID",              # gtq|mda|convergence|three-gates|logos-papers
        "seriesName",            # human-readable full name
        "articleOrder"           # ordered list of edges to article atoms
    ],
    "optional": [
        "entryPoint",            # edge to article new readers start at
        "description",
        "totalReadingTime",      # estimated minutes for full series
        "prerequisiteSeries",    # edge to series atom: "read MDA before GTQ"
        "status",                # in_progress|complete|paused
        "seriesThesis"           # one sentence: what the whole series argues
    ]
}
```

### AUDIENCE PROFILE (reusable object, not a node)

Not a separate atom. A reusable configuration stored in _vocab/audiences/
and referenced by ID from question, translation, reach, and article nodes.

```
AUDIENCE_PROFILE = {
    "audienceID":           # truck-driver-skeptic, grieving-mother, physics-phd, etc
    "priorKnowledge":       # none|low|moderate|high
    "primaryQuestion":      # what they most need answered
    "stakes":               # personal|academic|professional|spiritual|political
    "trustedEvidence":      # historical|empirical|personal|scriptural|mathematical
    "likelyMisconceptions": # what they probably believe that's wrong
    "vocabularyKnown":      # terms they already understand
    "timeBudget":           # 60_seconds|5_minutes|30_minutes|unlimited
}
```

### REACH NODE (expanded, replaces 7 media-specific types)

One node type, many formats. Format is a field, not a type.

```
NODE_TYPES["reach"] = {
    "type": "reach",
    "required": [
        "reachFormat",           # seo_page|faq|glossary_entry|tiktok_script|twitter_thread|
                                 # instagram_caption|linkedin_post|youtube_script|podcast_outline|
                                 # substack_post|infographic|one_pager|toolkit|debate_card|
                                 # visual|carousel|reel|story
        "sourceNodes",           # edges to article/translation/claim atoms this renders
        "impactStatement"        # one sentence: what this changes for the audience
    ],
    "optional": [
        "audienceProfileRef",    # edge to audience profile
        "questionRef",           # edge to question atom this answers
        "actionItems",
        "legalWarning",
        "hook",                  # for social formats: first line / first 3 seconds
        "coreMessage",           # for social formats: one sentence takeaway
        "duration",              # for video/audio: seconds
        "hashtags",
        "callToAction",
        "visualType",            # for visual renders: diagram|chart|infographic|3d_render|etc
        "altText",               # for visuals: accessibility
        "filePath",              # for visuals: path to rendered file
        "renderScript",          # for visuals: path to generator script
        "keywords",              # for SEO: primary search terms
        "metaTitle",             # for SEO: max 60 chars
        "metaDescription",       # for SEO: max 155 chars
        "searchIntent",          # for SEO: informational|navigational|transactional|comparison
        "structuredDataType"     # for SEO: Article|FAQPage|HowTo|ClaimReview
    ]
}
```

### PUBLIC DESCENT COMPLETION RULE (from GPT)

A claim has reached people only when:
1. A real question receives a faithful answer
2. An inspectable receipt exists (plain evidence, plain limits)
3. A bounded application exists where appropriate
4. A comprehension check confirms the audience preserved meaning
5. A traceable route back to rigor exists

### WHAT THE OLD v2.0 TYPES BECAME

| v2.0 type    | v2.1 home                                    |
|-------------|----------------------------------------------|
| seo         | reach node with reachFormat: seo_page        |
| social      | reach node with reachFormat: tiktok_script etc|
| faq         | reach node with reachFormat: faq             |
| glossary    | reach node with reachFormat: glossary_entry  |
| testimony   | result node with evidenceType: personal      |
| visual      | reach node with reachFormat: visual          |
| debate_move | objection + application node pair            |
| breadcrumb  | computed from series node + article edges     |

---

## UPDATED ROUTE PROFILES (v2.1)

### Route A: Pastoral / Everyday (unchanged)
```
theological grounding → translation → article → reach → result
```

### Route B: Explanatory Article (unchanged)
```
canonical refs → evidence → translation → article → reach → result
```

### Route C: Framework Argument (unchanged)
```
canonical → paradigm → synthesis → hypothesis → evidence →
falsification → objections → translation → article → reach → result
```

### Route D: Formal Paper (unchanged)
```
canonical → proof → evidence → falsification → paper →
objections → translation → application → article → reach → result
```

### Route E: Public Ministry (v2.1)
```
question → claim → translation → article → reach(faq + glossary_entry +
tiktok_script + seo_page) → result
```
Question node is the entry. Reach node handles all formats.

### Route F: Debate Arsenal (v2.1)
```
question → claim → objection + application → reach(debate_card +
tiktok_script) → result
```
Three Gates is the prototype.

### Route G: Series Publication (v2.1)
```
series → article[] → reach(seo_page)[] → breadcrumbs auto-generated
```

---

## BREADCRUMB GENERATION (computed, not authored)

1. Find current article atom
2. Read its seriesID
3. Find series atom with that seriesID
4. Read articleOrder to get prev/next
5. Render: [Series Name] > [Article N of M] | ← Prev | Next →

Additionally:
- upwardLink: article → paper edge → "Go deeper →"
- downwardLink: article → translation edge → "Simpler version →"
- parallelLinks: claim with multiple translations at different
  readingLevels → reading level switcher

---

## PUBLIC DESCENT SPINE (from GPT, v2.1)

The public equivalent of the doctoral rigor chain:

```
QUESTION (what does the person need answered?)
   ↓
AUDIENCE CONTEXT (who are they, what do they trust?)
   ↓
FAITHFUL TRANSLATION (meaning + confidence + boundaries preserved)
   ↓
LIVED RELEVANCE (where this appears in ordinary life)
   ↓
INSPECTABLE RECEIPT (plain evidence + plain limits)
   ↓
APPLICATION (if appropriate — with disclosed premises)
   ↓
COMPREHENSION CHECK (did meaning survive descent?)
   ↓
PUBLIC RENDERINGS (reach nodes in various formats)
   ↓
REAL-WORLD RESULT (what actually happened)
```

Node mapping:
- QUESTION → question node
- AUDIENCE CONTEXT → audienceProfile object
- FAITHFUL TRANSLATION → translation node with descentInvariant
- LIVED RELEVANCE → article node (humanAnchor, soWhat, feltProblem)
- INSPECTABLE RECEIPT → evidence node rendered plain (plainFinding, plainLimit)
- APPLICATION → application node (addedPremises disclosed)
- COMPREHENSION CHECK → check node
- PUBLIC RENDERINGS → reach nodes (one per format)
- REAL-WORLD RESULT → result node

---

_End of v2.1 additions._

---

## ARCHIVED v2.0 SPECS (kept for reference, superseded by v2.1)

The following node types from v2.0 have been collapsed into existing
types per the mapping table above. Specs preserved below for any
tooling that referenced them during the v2.0 window.

<!--  ARCHIVED v2.0 SPECS START (everything below is superseded by v2.1)
TESTIMONY NODE (now result with evidenceType: personal)
        "platform",              # where the testimony came from
        "date",
        "permission",            # true|false — do we have permission to publish
        "followUp",              # edge to result atom if tracked
        "anonymized"             # true if identifying details removed
    ]
}
```

### VISUAL NODE
```
NODE_TYPES["visual"] = {
    "type": "visual",
    "required": [
        "visualType",            # diagram|chart|infographic|3d_render|timeline|comparison|process_flow|equation_visual|glyph
        "sourceClaim",           # edge to claim atom
        "altText",               # accessibility description
        "filePath"               # relative path to the image/render file
    ],
    "optional": [
        "dataSource",            # edge to evidence atom
        "readingLevel",          # which audience this visual targets
        "printable",             # true if suitable for PDF/print
        "animationSteps",        # list of steps for animated visuals
        "renderScript",          # path to the Python/matplotlib script that generates it
        "dimensions"             # width x height
    ]
}
```

### DEBATE_MOVE NODE
```
NODE_TYPES["debate_move"] = {
    "type": "debate_move",
    "required": [
        "moveName",              # e.g. "Gate 1: Is There Truth?"
        "trigger",               # what the opponent says that activates this
        "response",              # what you say back
        "structure",             # WHY it works — the logical mechanism
        "sourceClaim"            # edge to claim atom
    ],
    "optional": [
        "selfRefutationProof",   # if the denial is self-refuting, the formal proof
        "commonCounters",        # list of expected pushback
        "videoScript",           # edge to social atom (tiktok script)
        "difficulty",            # beginner|intermediate|advanced
        "fieldTested",           # true if used in actual debate
        "winRate"                # if tracked — what % of the time this lands
    ]
}
```

### SERIES NODE
```
NODE_TYPES["series"] = {
    "type": "series",
    "required": [
        "seriesID",              # gtq|mda|convergence|three-gates|logos-papers|etc
        "seriesName",            # human-readable full name
        "articleOrder"           # ordered list of edges to article atoms
    ],
    "optional": [
        "entryPoint",            # edge to the article new readers should start at
        "description",
        "totalReadingTime",      # estimated minutes for the whole series
        "prerequisiteSeries",    # edge to series atom — "read MDA before GTQ"
        "status",                # in_progress|complete|paused
        "seriesThesis"           # one sentence — what the whole series argues
    ]
}
```

---

## UPDATED ROUTE PROFILES

### Route E: Public Ministry
```
claim → translation → article → faq + glossary + social + seo → testimony
```
No paper required. Claims still carry their burden.

### Route F: Debate Arsenal
```
claim → objection → debate_move → social (tiktok scripts) → testimony
```
The Three Gates is the prototype for this route.

### Route G: Series Publication
```
series → article [] → seo [] → social [] → breadcrumbs auto-generated
```
Series atom defines order. Breadcrumbs render from the graph.

---

## BREADCRUMB GENERATION (not a separate atom)

Breadcrumbs are COMPUTED from existing atoms, not authored:

1. Find the current article atom
2. Read its seriesID
3. Find the series atom with that seriesID
4. Read articleOrder to get prev/next
5. Render: [Series Name] > [Article N of M] | ← Prev | Next →

Additionally:
- upwardLink: if article has edge to paper atom, render "Go deeper →"
- downwardLink: if article has edge to translation atom, render "Simpler version →"
- parallelLinks: if claim has multiple translation atoms at different readingLevels, render reading level switcher

All computed. No authoring required.
ARCHIVED v2.0 SPECS END -->
