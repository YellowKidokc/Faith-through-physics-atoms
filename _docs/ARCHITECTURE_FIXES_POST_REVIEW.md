# ARCHITECTURE FIXES — Response to GPT Adversarial Review
## Claude Opus | July 23, 2026

---

## Summary: 8 breaks identified, 7 valid, all fixable

GPT's adversarial review identified real structural issues.
None of them require scrapping the architecture. All of them 
require making implicit design decisions EXPLICIT and adding 
two missing concepts: the Descent Invariant and the Application 
node type.

---

## Fix 1: Stage numbers are sort order, not execution order

ADD to v11 spec:

"The 14 stages are numbered for filesystem sort order, not 
execution order. Evidence (05) can arrive before hypothesis (04). 
Objections (08) can arrive before paper (07). The ONLY ordering 
constraint is the descent rule: stages below entry point must 
eventually be populated. Content enters wherever it naturally 
sits and can fill upper stages in any order."

Status: WORDING FIX. Add to spec.

---

## Fix 2: Descent Invariant (meaning preservation)

ADD new edge property to atom schema:

```jsonld
{
  "edges": [
    {
      "type": "descendsTo",
      "target": "tp:education/09/001",
      "transformationType": "translation | narrative | application | excerpt",
      "descentInvariant": {
        "claimMeaningPreserved": true,
        "confidencePreserved": true,
        "boundariesPreserved": true,
        "killConditionPreserved": true,
        "addedPremises": [],
        "omittedMaterial": [],
        "applicationLeap": "none | disclosed | unsupported",
        "reviewStatus": "unreviewed | machine_checked | human_reviewed | disputed"
      }
    }
  ]
}
```

The descent rule becomes: "A claim is descent-complete only when 
at least one path reaches an everyday artifact AND every edge on 
that path has a reviewed Descent Invariant AND any added 
application is represented as a separate node."

Status: SCHEMA ADDITION. Add to atom spec.

---

## Fix 3: Application node type (separate from translation)

ADD new node type:

```
Stage 09 splits into two operations:
  09_everyday = TRANSLATION (meaning-preserving restatement)
  NEW: APPLICATION (inferential leap to practical advice)

APPLICATION node:
  nodeType: "application"
  derivedFrom: [source claim, theological premise, domain premise]
  applicationDomain: "marriage | education | church | policy | personal"
  inferenceStatement: "the exact bridge from claim to action"
  boundaryConditions: "where the application holds and doesn't"
  falsificationCondition: "what would show the application is wrong"
  addedPremises: ["list of premises not in the source claim"]
  status: "proposed | reviewed | verified | rejected"
```

This prevents a valid equation from smuggling in unsupported 
advice. The application declares its added premises so they 
can be challenged independently.

Status: NEW NODE TYPE. Add to atom spec and folder template.

---

## Fix 4: Completion computed per claim, not per folder

CLARIFY in spec:

"Folder-level status (empty/wip/done) is the HUMAN view — a 
quick glance at domain health. Claim-level completion is the 
MACHINE view — computed by the graph scanner from atom state.

The status scanner reports BOTH:
- Folder status: which stages have any content
- Claim coverage: which claims have completed descent paths

A domain is not descent-complete because folders are populated.
A domain is descent-complete when every canonical claim has at 
least one reviewed path to an everyday artifact."

Status: SCANNER ENHANCEMENT. Modify status_scan.py to check 
per-claim coverage once atoms exist.

---

## Fix 5: Falsification propagation scoping

REFINE edge propagation rules:

```
failureType: 
  root_claim          -> propagate globally
  mapping_invalid     -> propagate to bridge peers
  boundary_exceeded   -> flag dependents for review (not falsify)
  measurement_invalid -> flag local only
  empirical_failure   -> flag dependents for review
  interpretation      -> flag local only
  application_failure -> flag application node only

propagationScope:
  global       -> all dependents falsified
  bridge_peers -> connected domains flagged for review
  dependents   -> downstream nodes flagged for review  
  local        -> only this node affected
```

"Only a root-level logical contradiction propagates globally. 
Most empirical failures flag dependents for review, not auto-
falsification."

Status: SCHEMA REFINEMENT. Update atom edge rules.

---

## Fix 6: Theological companion references canonical, doesn't redefine

ADD to _theological/ README template:

"This folder contains MAPPINGS from canonical theological claims 
to this domain. It does NOT independently define doctrine.

Canonical theological claims live in:
  theology/01_canonical/
  scripture/01_canonical/
  trinity/01_canonical/

This folder answers: 'How does canonical theology bear on THIS 
domain?' It must not independently redefine the theology.

Every scripture.md, doctrine.md, and christ-type.md should 
REFERENCE canonical theological atoms, not restate them."

Status: README UPDATE. Modify template.

---

## Fix 7: Parallel discovery relabeled as experimental design

REWRITE the final section of WHY_THIS_STRUCTURE.md:

Change "The Parallel Discovery Hypothesis" to 
"Experimental Design: Cross-Domain Process Similarity"

Add: "Cross-domain process similarities are partly guaranteed 
by the shared template. They cannot support the framework 
unless the similarity is defined before inspection, measured 
independently of the shared template, and compared against a 
null model. The structure may help reveal evidence. It is not 
itself evidence."

Status: WORDING FIX. Already partially done.

---

## Fix 8: Five-coordinate system as explicit atom dimensions

CLARIFY in atom schema:

Every atom explicitly declares five independent coordinates:

```
coordinate_1_type: "what is it" 
  -> nodeType field (claim, evidence, bridge, kill, paper, 
     objection, translation, application, article, reach, result)

coordinate_2_state: "epistemic state"
  -> status field (captured, classified, proposed, active, 
     verified, weakened, falsified, deprecated, superseded)

coordinate_3_domain: "where does it apply"
  -> domainType + optional subdomain + boundaryConditions

coordinate_4_audience: "for whom is it rendered"
  -> NEW: audienceLevel field (technical_specialist, doctoral, 
     informed_adult, everyday, child, pastor, parent, policymaker)

coordinate_5_provenance: "how was it derived"
  -> edges with typed connections, bridge grades, confidence, 
     Descent Invariants
```

The folders are the WORKBENCH VIEW — one materialized projection 
of coordinates 1 and 2. The graph is the CANON VIEW — projection 
of coordinates 3 and 5. The website is the PUBLIC VIEW — projection 
of coordinate 4.

"Four views, one data layer. The folders remain valuable as human 
workbench. They become a generated view, not the definition of 
what an artifact is."

Status: SCHEMA CLARIFICATION. Atom schema already has most of 
these as fields. Add audienceLevel. Make the five-coordinate 
framing explicit in the spec.

---

## What GPT Got Wrong

One thing: his claim that the 14-stage arc "cannot be the ontology 
of the system." 

We never said it was. The arc is the WORKBENCH — the human 
production view. The ontology is the atom graph. The folders 
organize labor. The atoms define identity, provenance, and 
relationships. We said this explicitly in the paper: "folders = 
lifecycle, atoms = relationships."

His five-coordinate system is a better DESCRIPTION of what the 
atoms already carry. It's not a replacement for the folder 
structure. It's a refinement of the atom schema. Both are needed.

---

## Net Assessment

GPT's review makes the architecture approximately 30% stronger 
(his own estimate). The Descent Invariant is the biggest win — 
it closes the gap between "file exists" and "meaning survived." 
The Application node type is the second biggest win — it audits 
the most important inferential leap in the ministry.

None of the fixes require restructuring. All of them require 
making implicit decisions explicit and adding two concepts to 
the atom schema.

The architecture survives. It gets better.

---
*Faith Through Physics | POF 2828*
