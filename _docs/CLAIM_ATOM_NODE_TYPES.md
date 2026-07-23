# FAITH THROUGH PHYSICS — ATOM NODE TYPES
## What each stage produces and how they connect
## Claude Opus + GPT Codex corrections | July 23, 2026

---

## CRITICAL DISTINCTION (from GPT Codex)

**Paper, evidence, translation, article, and result nodes are NOT claims.
They are nodes AROUND claims. Only 01_canonical produces actual claims.
Everything else orbits, supports, attacks, translates, or confirms claims.**

This keeps the graph clean. The claim is the sun. Everything else orbits.

---

## THE CORE DNA (every node has this)

Every atom, regardless of type, carries:

```jsonld
{
  "@id": "unique permanent URL",
  "nodeID": "tp:DOMAIN/STAGE/ID",
  "name": "human-readable title",
  "nodeType": "one of the types below",
  "domainType": "physics | theology | education | etc",
  "stage": "01_canonical | 06_falsification | etc",
  "status": "draft | active | verified | falsified | deprecated",
  "author": "David Lowe + AI collaborator",
  "dateCreated": "ISO date",
  "dateModified": "ISO date",
  "edges": [
    {
      "type": "dependsOn | feedsInto | bridgesTo | challenges | expands | forksFrom",
      "target": "@id of target node",
      "grade": "structural_identity | structural_isomorphism | structural_analogy | metaphorical",
      "propagates": true | false
    }
  ]
}
```

### Key changes from v1 (per GPT Codex review):
1. Every node gets **nodeID**. Only actual claim nodes (01_canonical) get **claimID**.
2. Edges are **typed objects** with grade and propagation flag — not just flat arrays.
3. Bridge-grade propagation belongs ON THE EDGE, not on the node.
4. **statementTechnical** and **statementPlain** only required on nodes that make statements (claims, paradigms, translations, articles). Evidence and result nodes don't need them.
5. Evidence nodes get **citationStatus** (verified | unverified | retracted).

The shared DNA means ANY node can connect to ANY other node
across stages and across domains. The connection types are
what change.

---

## THE NODE TYPES BY STAGE

### 00_inbox_working → RAW NODE
The rawest form. Barely structured.

```
Fields: source, date, rough_domain, raw_text
Connects: nowhere yet — orphan until classified
Purpose: capture before it's lost
```

NOT a real atom yet. It becomes one when it gets classified
and moves to a stage.

---

### 01_canonical → CLAIM NODE ⭐ (the primary atom)

This is the core unit. THE ONLY NODE TYPE THAT IS A CLAIM.
Everything else orbits claims. Only claim nodes get claimID.

```
Fields: claimID (tp:DOMAIN/L#/C#), 
        statementTechnical, statementPlain, axiomRoot,
        claimClass (floor-axiom | definition | theorem |
        bridge | empirical-anchor | prediction | boundary),
        derivationChain, mathematicalForm,
        falsificationCondition, verificationStatus,
        kernelChecked (Lean 4), challengeStatus
Connects TO: other claims via edges (type: dependsOn)
Connects FROM: everything else points back here
```

Example: "Time-translation symmetry in the moral domain
implies a conserved current via Noether's theorem."

---

### 02_paradigm → PARADIGM NODE

What this claim breaks about old thinking.

```
Fields: oldParadigm, breakStatement, newParadigm,
        historicalPrecedent, claimRef (points to 01)
Connects TO: the claim it reframes (01_canonical)
Connects FROM: articles, everyday (they USE the reframe)
```

Example: "Education is not a policy problem. It's a
physics problem — Shannon channel with noise > signal."

---

### 03_synthesis → BRIDGE NODE

Cross-domain connection. The isomorphisms.

```
Fields: sourceDomain, targetDomain, bridgeGrade
        (structural_identity | structural_isomorphism |
        structural_analogy | metaphorical),
        mappingProof, bidirectionalTest,
        boundaryConditions, masterEquationLink,
        claimRef (points to 01 in BOTH domains)
Connects TO: claims in TWO different domains
Connects FROM: papers, articles that USE the bridge
Edge rule: identity/isomorphism PROPAGATE falsification
           analogy/metaphorical DO NOT propagate
```

Example: "Shannon channel capacity ↔ education
transmission fidelity — structural identity, same equation."

---

### 04_hypothesis → PREDICTION NODE

Testable prediction derived from a claim.

```
Fields: prediction, predictedMagnitude, testMethod,
        confidenceLevel, derivedFrom (points to 01),
        timeframe (testable_now | future | mathematical)
Connects TO: the claim it predicts FROM (01_canonical)
Connects FROM: fulfilled nodes (13) that report results
```

Example: "Systems retaining a Logos should show measurably
higher transmission fidelity — testable via Amish vs public."

---

### 05_evidence → EVIDENCE NODE

External data supporting or challenging a claim.
NOT a claim itself — a node AROUND a claim.

```
Fields: sourceType (academic | LLM | wiki | dataset |
        competing_framework), sourceRef, dataPoints,
        relevantClaim (points to 01 or 04),
        conclusionSeparate (boolean — source notes vs conclusions),
        citationStatus (verified | unverified | retracted)
Connects TO: claims or predictions it supports/challenges
Connects FROM: papers, articles that cite it
Note: does NOT require statementTechnical/statementPlain
```

Example: "NAEP 8th grade math: 35% → 28% proficiency.
Source: National Assessment of Educational Progress."

---

### 06_falsification → KILL NODE

What would destroy a claim, and whether we tried.

```
Fields: killCondition, attemptDescription, outcome
        (survived | weakened | boundary_found | falsified),
        targetClaim (points to 01), counterArgument,
        boundaryDiscovered
Connects TO: the claim it attacks (01_canonical)
Connects FROM: objections (08), fulfilled (13)
Edge rule: if outcome=falsified, propagates
           upstream-falsified to all dependents
```

Example: "Kill attempt: 'Amish succeed from isolation,
not Logos.' Outcome: survived — secular communes show
high attrition despite isolation."

---

### 07_paper → PAPER NODE

Formal treatment combining multiple nodes.

```
Fields: abstract, coreClaimRef (points to 01), scope,
        definitions, priorWork, argumentChain,
        evidenceRefs (points to 05), falsificationRefs
        (points to 06), objectionRefs (points to 08),
        everydayBridge (points to 09),
        template (doctoral template sections 1-13)
Connects TO: claims, evidence, falsification, objections
             it synthesizes
Connects FROM: articles, audience that descend from it
```

The paper is a COMPOSITE node — it doesn't hold original
truth. It assembles and argues truth held in claim nodes.

---

### 08_objections → OBJECTION NODE

Steelmanned pushback.

```
Fields: objection, objectionSource, strength
        (serious | moderate | common_misunderstanding),
        response, status (answered | unresolved | partial),
        targetClaim (points to 01 or 07)
Connects TO: the claim or paper it pushes against
Connects FROM: fulfilled (13) if the objection was tested
```

---

### 09_everyday → TRANSLATION NODE

Plain language version.

```
Fields: plainStatement, practicalApplication,
        analogy, soWhat, sourceClaim (points to 01),
        readingLevel (grade_8 | grade_10 | grade_12)
Connects TO: the claim it translates (01_canonical)
Connects FROM: worldcheck (10), articles (11)
```

---

### 10_worldcheck → CHECK NODE

Pressure test of the everyday version.

```
Fields: reactionsSummary, mainstreamFraming,
        simplificationAudit, factCheckResult,
        sourceTranslation (points to 09)
Connects TO: the everyday node it tested (09)
Connects FROM: articles (11) that incorporate feedback
```

---

### 11_articles → ARTICLE NODE

Narrative treatment.

```
Fields: seriesID (GTQ | CNS | CDT | DRV | LP | standalone),
        seriesNumber, narrativeArc, humanAnchor,
        crossRefs (points to articles in other domains),
        readingLevel, claimRefs (points to 01 nodes used),
        bridgeRefs (points to 03 nodes used)
Connects TO: claims and bridges it narrates
Connects FROM: audience (12) versions derived from it
```

---

### 12_audience → REACH NODE

SEO, social, toolkit, action guide.

```
Fields: format (social_post | video_script | infographic |
        one_pager | toolkit | podcast_outline | SEO_page),
        sourceArticle (points to 11 or 09),
        impactStatement, actionItems,
        legalWarning (boolean for toolkit nodes)
Connects TO: the article or everyday version it derives from
Connects FROM: fulfilled (13) tracking real-world impact
```

---

### 13_fulfilled → RESULT NODE

What happened.

```
Fields: predictionRef (points to 04), outcome
        (confirmed | partial | failed | pending),
        data, accuracy, revisionTrigger,
        realWorldOutcome
Connects TO: the prediction it resolves (04)
Connects BACK TO: canonical (01) to strengthen or revise
Edge rule: confirmed → strengthens upstream claim
           failed → triggers new 00_inbox_working entry
```

---

## THE CONNECTION MAP

```
                    RAW (00)
                      ↓ classifies into
                  CLAIM (01) ←←←←←←←←←←← RESULT (13)
                  ↙  ↓  ↘                    ↑
          PARADIGM  BRIDGE  PREDICTION ———→ RESULT
            (02)    (03)      (04)           (13)
                      ↓        ↓
                   EVIDENCE  EVIDENCE
                     (05)     (05)
                      ↓
                   KILL (06)
                      ↓
                   PAPER (07)
                      ↓
                   OBJECTION (08)
                      ↓
                   TRANSLATION (09)
                      ↓
                   CHECK (10)
                      ↓
                   ARTICLE (11)
                      ↓
                   REACH (12)
                      ↓
                   RESULT (13) ———→ back to CLAIM (01)
```

Everything flows down. Results flow back up. The cycle.

---

## HOW THE GRAPH GROWS ORGANICALLY

1. You write a CLAIM atom in education/01_canonical/
2. The claim declares its axiomRoot and domainType
3. An AI scans all atoms, finds economics has a claim
   with the SAME axiomRoot
4. A BRIDGE atom gets proposed: "these two claims share
   a structural root — investigate"
5. You verify: is it identity, isomorphism, or just analogy?
6. If identity/isomorphism: the bridge PROPAGATES — 
   kill one side, the other side feels it
7. The graph just grew a connection nobody planned

That's the organic growth. The atoms find each other
through shared roots. The AI is the matchmaker.
The human verifies the grade.

---

## WHAT GOES IN THE REPO

Each atom is TWO files in its stage folder:

```
education/01_canonical/
  ├── A042-L9-C1.jsonld    ← the machine-readable atom
  └── A042-L9-C1.html      ← the rendered pill (generated)
```

The .jsonld is source of truth. The .html is generated FROM it.
Never edit the HTML directly — edit the atom, regenerate.

The builder script takes your input → writes .jsonld → 
generates .html pill. One command, both files.
