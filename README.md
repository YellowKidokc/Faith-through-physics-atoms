# Faith Through Physics — Atom System
## The canonical node specification for the Theophysics framework
## David Lowe | POF 2828 | July 23, 2026
## Built by: Claude Opus, GPT Codex, Kimi | Adversarially reviewed

---

## GOVERNING RULES

**Artifacts enter where they belong.
Claims rise only as far as their burden requires.
Truth descends as far as people require.**

Proposed node connections can now be pressure-tested through the provider-neutral
[Adversarial Review Gate](_docs/ADVERSARIAL_REVIEW_GATE.md). Its GUI and CLI
block opposed wires while reserving every acceptance decision for a human. The
same rail can generate proposed plain-language math translation nodes without
promoting the source claim.

Canonical terminology is indexed by the
[Canonical Definition Registry](_docs/CANONICAL_DEFINITION_REGISTRY.md). Each
definition and its evidence remain independent atoms; resolver matches are only
proposals and inherit required source citations when rendered.

Long-running paper series use the
[Living Atlas Resolution](_docs/LIVING_ATLAS_RESOLUTION.md) rule:
later work may change a claim's current standing, but it never rewrites the
historical state of the paper where the claim first appeared.

Evidence is component-aware by contract. The
[Evidence Coverage Method](_docs/EVIDENCE_COVERAGE_METHOD.md) separates
evidence strength from evidence coverage, so a source can strongly support one
part of a claim while remaining silent on another.

Publication is human-gated by design:
[Canonical Publication Gate](_docs/CANONICAL_PUBLICATION_GATE.md) keeps
authoring source, frozen canonical publication, and living Atlas state separate.

Ascendant, Descendant, and Meeting projections are documented in
[_docs/ASCENDANT_DESCENDANT_MEETING.md](_docs/ASCENDANT_DESCENDANT_MEETING.md).
They render as additional views over the same atom and Atlas objects.

Whole-page explanation is a separate aggregation call:
[_docs/PAGE_AGGREGATION_API.md](_docs/PAGE_AGGREGATION_API.md). It consumes
claim/evidence/receipt outputs and produces repeatable map summaries without
creating new claims or evidence.

Build hardening rules for Marker 12, conflict states, pre-admission gates, Phi,
and reproducibility boundaries are recorded in
[_docs/BUILD_SPEC_HARDENING.md](_docs/BUILD_SPEC_HARDENING.md).

---

## CRITICAL DISTINCTIONS

### 1. Claim identity is independent of canonical status
A claim is a claim whether it is draft, proposed, challenged, 
supported, falsified, or deprecated. Canonical means the framework 
currently accepts it — it does not confer claimhood.

### 2. Only claims are claims. Everything else orbits.
Papers, evidence, translations, articles, and results are NOT claims.
They are nodes AROUND claims. The claim is the sun.

### 3. Every node carries a coherence direction
Every atom is either building coherence or documenting decoherence.
This is the fundamental binary that sits between God and the 
Master Equation. χ measures the ratio between them.

---

## THE CORE DNA (every node has this)

```jsonld
{
  "@id": "unique permanent URL",
  "nodeID": "tp:DOMAIN/STAGE/ID",
  "name": "human-readable title",
  "nodeType": "CLAIM | EVIDENCE | BRIDGE | KILL | PAPER | 
               OBJECTION | TRANSLATION | APPLICATION | 
               ARTICLE | REACH | RESULT | RAW",
  "coherenceDirection": "coherence | decoherence | neutral | mixed",
  "domainType": "physics | theology | education | etc",
  "workbenchStage": "00_inbox_working | 01_canonical | etc",
  "epistemicStatus": "draft | proposed | challenged | supported |
                      verified | weakened | falsified | deprecated | 
                      superseded",
  "status": "active | archived",
  "author": [],
  "dateCreated": "ISO date",
  "dateModified": "ISO date",
  "edges": [
    {
      "type": "dependsOn | feedsInto | bridgesTo | challenges | 
              expands | forksFrom | descendsTo",
      "target": "@id of target node",
      "grade": "structural_identity | structural_isomorphism | 
               structural_analogy | metaphorical",
      "propagates": true | false,
      "failureScope": "global | bridge_peers | dependents | local",
      "descentInvariant": {
        "claimMeaningPreserved": true | false | "unreviewed",
        "confidencePreserved": true | false | "unreviewed",
        "boundariesPreserved": true | false | "unreviewed",
        "killConditionPreserved": true | false | "not_applicable",
        "addedPremises": [],
        "applicationLeap": "none | disclosed | unsupported",
        "reviewStatus": "unreviewed | machine_checked | human_reviewed"
      }
    }
  ]
}
```

---

## CLAIM NODES (the primary atoms)

Claims are the ONLY nodes that carry claimID. A claim is a claim 
at every stage of its life — draft through falsified.

```jsonld
{
  "nodeType": "CLAIM",
  "claimID": "tp:EDU/C0042",
  "claimKind": "axiom | definition | theorem | empirical | 
                prediction | interpretation | application",
  "canonicalStatus": "noncanonical | candidate | canonical | rejected",
  "statementTechnical": "formal version",
  "statementPlain": "everyday version",
  "axiomRoot": "@id of root claim",
  "mathematicalForm": "equation if applicable",
  "falsificationCondition": "what would break this",
  "verificationStatus": "informal | machine-verified | falsified",
  "kernelChecked": false,
  "challengeStatus": "unchallenged | challenged-open | 
                      challenged-survived | falsified",
  "claimBurden": {
    "class": "pastoral | textual | theological | historical | 
              empirical | statistical | mathematical | 
              isomorphism | causal | application",
    "requiredSupport": ["list of what this claim class demands"],
    "supportStatus": "complete | incomplete | blocked"
  }
}
```

### Key properties:
- **claimID** stays with the claim forever, regardless of status
- **canonicalStatus** tracks framework acceptance separately
- **workbenchStage** tracks where humans are working on it
- **claimKind** includes prediction and application as subtypes
  (because predictions and applications can be independently 
  true or false)
- **claimBurden** auto-generates from claimKind — each kind 
  has a minimum support contract

### Claim-burden table:

| Claim Kind | Minimum Support Required |
|-----------|------------------------|
| Pastoral exhortation | Scripture/theological grounding |
| Textual biblical | Exact passage, translation note |
| Theological interpretation | Scripture refs, interpretive premises |
| Historical | Primary/secondary sources, date qualification |
| Empirical | Observation, source data, method, uncertainty |
| Statistical | Dataset, inclusion rule, denominator, calculation |
| Mathematical | Definitions, derivation/proof, boundary conditions |
| Isomorphism | Mapping, invariants, bidirectional test, boundaries |
| Causal | Competing explanations, distinguishing evidence |
| Application | Source claims, added premises, boundary, kill condition |

---

## SUPPORTING NODES (orbit claims)

These nodes do NOT get claimID. They reference claims via edges.

### EVIDENCE NODE
```
sourceType, sourceRef, dataPoints, relevantClaim,
citationStatus (verified | unverified | retracted)
Does NOT require statementTechnical/statementPlain.
```

### BRIDGE NODE  
```
sourceDomain, targetDomain, bridgeGrade, mappingProof,
bidirectionalTest, boundaryConditions, masterEquationLink
Connects claims in TWO different domains.
```

### KILL NODE
```
killCondition, attemptDescription, outcome, targetClaim,
counterArgument, boundaryDiscovered
failureType: root_claim | mapping | boundary | measurement |
             empirical_instance | interpretation | application
```

### PAPER NODE
```
abstract, coreClaimRef, scope, argumentChain, everydayBridge
Composite node — assembles truth held in claim nodes.
NOT source of truth. NOT endpoint.
```

### OBJECTION NODE
```
objection, strength, response, status, targetClaim
Steelmanned — strongest form, not strawmen.
```

### TRANSLATION NODE
```
plainStatement, analogy, soWhat, sourceClaim, readingLevel
Meaning-preserving restatement ONLY.
Does NOT include practical application (that's APPLICATION).
```

### APPLICATION NODE
```
derivedFrom (source claim + theological/domain premises),
applicationDomain, inferenceStatement, boundaryConditions,
falsificationCondition, addedPremises, status
NEW inferential leap — can be WRONG even when source claim is RIGHT.
Must disclose added premises.
```

### ARTICLE NODE
```
seriesID, narrativeArc, humanAnchor, claimRefs, bridgeRefs,
readingLevel, crossRefs
```

### REACH NODE
```
format, sourceArticle, impactStatement, actionItems,
legalWarning
```

### RESULT NODE
```
predictionRef, outcome, data, accuracy, revisionTrigger
Confirmed → strengthens upstream. Failed → triggers revision.
```

---

## THE COHERENCE COORDINATE

Every atom carries `coherenceDirection`:

- **coherence** — this node builds, preserves, or documents 
  order, signal, alignment, grace, truth, love, faith, logos
- **decoherence** — this node documents, analyzes, or describes 
  disorder, noise, drift, entropy, deception, captivity, doubt
- **neutral** — system/infrastructure node (template, index)
- **mixed** — contains both (e.g., a paper comparing coherent 
  and decoherent states)

This is NOT a moral judgment on the node. A KILL node documenting 
a failed attack is tagged "coherence" (the claim survived). An 
EVIDENCE node documenting civilizational decay is tagged 
"decoherence" (it describes entropy). The tag describes what 
the content is ABOUT, not whether the content is good or bad.

The Master Equation measures χ — the ratio of coherence to 
decoherence. This tag lets the graph compute coherence density 
across any domain, stage, or slice of the framework.

---

## FOUR ROUTE PROFILES

### Route A: Pastoral / Everyday
```
theological grounding → everyday → article → audience
```
No paper required. Claims within still carry their burden.

### Route B: Explanatory Article
```
canonical refs → evidence → everyday → article → audience
```
Article is primary. Claims get linked support nodes.

### Route C: Framework Argument
```
canonical → paradigm → synthesis → hypothesis → evidence →
falsification → objections → everyday → article → audience → 
fulfilled
```
Paper added when scope warrants.

### Route D: Formal Paper
```
canonical → proof/method → evidence → falsification → paper →
objections → translation → application → article → audience → 
fulfilled
```
Paper is composite rendering, not source of truth.

---

## FIVE COORDINATES (per atom)

1. **What is it?** → nodeType
2. **Epistemic state?** → epistemicStatus + canonicalStatus
3. **Where does it apply?** → domainType + boundaries
4. **For whom?** → audienceLevel
5. **How derived?** → edges + provenance + descentInvariants

Four views generated:
- **Canon view** → claims, proofs, provenance
- **Workbench view** → 14 folders for human production
- **Graph view** → dependencies, bridges, propagation
- **Public view** → descent renderings, reader modes

---

## DESCENT RULE

Pushing up is optional. Pushing down is never optional.

Descent is complete ONLY when:
1. At least one path reaches an ordinary-person artifact
2. Every edge on that path has a reviewed Descent Invariant
3. Any application is a separate node with disclosed premises
4. The reader can trace back to the exact source claim

---

## FALSIFICATION PROPAGATION (scoped)

| Failure Type | Scope |
|-------------|-------|
| Root claim false | Global |
| Mapping invalid | Bridge peers flagged |
| Boundary exceeded | Dependents flagged |
| Measurement invalid | Local |
| Empirical failure | Dependents flagged |
| Interpretation overreach | Local |
| Application failure | Application node only |

---

## THE HIERARCHY

```
GOD
  ↓
COHERENCE ←→ DECOHERENCE  (the fundamental binary)
  ↓
MASTER EQUATION  (χ measures the ratio)
  ↓
TEN LAWS  (ten expressions of the binary)
  ↓
DOMAINS  (infinite projections)
  ↓
14-STAGE ARC  (the ripening process)
  ↓
ATOMS  (self-describing, self-connecting nodes)
```

---

_Faith Through Physics | POF 2828_
_"The Word became flesh and dwelt among us." — John 1:14_
_Truth always flows down._
