# CANONICAL CONTENT OS v0.1
## Claim-centered authoring, review, propagation, and quarantine
## Status: design specification — not yet implemented

## Governing paragraph

At Faith Through Physics, every truth-bearing assertion begins as one permanently identifiable claim. Mathematics, definitions, evidence, stories, bridges, papers, translations, applications, and results are different node types around claims; none may silently impersonate or rewrite the claim. The authoring interface reveals only the questions required by the selected node type, while the complete record remains expandable and machine-readable. Closing an item triggers schema, provenance, evidence, dependency, adversarial, and descent reviews. Automated reviewers may attach signed receipts, warnings, or exceptions, but canonical promotion remains an explicit human act. Accepted changes propagate to generated views and dependent records according to typed edges; authored material that cannot be safely rewritten is marked stale for review. Anything that violates the contracts is preserved in quarantine rather than discarded or silently admitted.

## 1. The two independent icon axes

The existing `_icons` set answers:

> Where is this item in the lifecycle, and what is its operational state?

The new semantic icon axis answers:

> What kind of item is this?

Do not merge these questions. A claim may be in `14_evidence__working`, but it remains a claim. An evidence node may be `done`, but it never becomes a claim.

Recommended visual composition:

```text
[semantic node icon] + [small lifecycle/status badge]
```

## 2. Permanent identity grammar

Human-readable IDs use a stable type prefix, domain code, and sequence. Version is metadata, not part of the permanent identity.

```text
CLM-ME-0001      canonical claim
MTH-ME-0001      mathematical object or derivation
DEF-ME-0001      canonical definition
STY-ME-0001      story/narrative node
EVD-ME-0001      evidence node
BRG-ME-0001      bridge node
KIL-ME-0001      kill/countermodel node
PRF-ME-0001      formal proof receipt
PAP-ME-0001      paper node
TRN-ME-0001      translation node
APP-ME-0001      application node
OBJ-ME-0001      objection node
PRD-ME-0001      prediction node
RES-ME-0001      result node
SRC-ME-0001      source/provenance node
```

Machine IDs remain globally namespaced:

```text
tp:claim/master-equation/CLM-ME-0001
tp:math/master-equation/MTH-ME-0001
tp:story/master-equation/STY-ME-0001
```

Display form may include a version:

```text
CLM-ME-0001 @ 3.0.0
```

### Version semantics

| Change | Version action |
|---|---|
| Spelling, citation, formatting, metadata; no semantic change | patch: `2.2.0 -> 2.2.1` |
| Scope/support clarification; proposition and truth conditions preserved | minor: `2.2.0 -> 2.3.0` |
| Proposition, definition, mathematics, truth conditions, or conclusion changes materially | major: `2.2.0 -> 3.0.0` |
| Earlier item is no longer controlling | supersede; preserve old snapshot and link successor |
| Correction attaches without replacing history | amend; retain original plus visible amendment |

The resolver proposes the version action. The human confirms it.

## 3. Node families

### 3.1 Claim node — the sun

The claim is the proposition being evaluated. It carries:

- technical and plain statements
- claim species and logical type
- truth and disconfirmation conditions
- dependencies
- evidence contract
- current ontic/epistemic status
- canonical version history

Everything else points to claims.

### 3.2 Mathematical node

Mathematical nodes contain definitions, symbols, equations, premise sets, derivations, countermodels, and formal declarations. They may establish a mathematical claim under premises. They do not establish physical instantiation or theological identification without bridge nodes.

If a canonical symbol or expression changes, generated mathematical views may update automatically. Authored prose is scanned and flagged before rewriting.

### 3.3 Definition/principle node

A definition node owns the canonical first statement of a term or named principle. For example, every rendering of “Wall One” begins from its accepted canonical definition.

Definitions may have:

- exact canonical wording
- permitted plain paraphrases
- prohibited drift
- aliases
- source and attribution policy
- namespace and scope

Stories and papers reference the definition; they do not redefine it locally.

### 3.4 Story node

A story cannot be safely synchronized by blind text replacement. Instead it carries truth bindings:

```json
{
  "usesClaims": ["CLM-ME-0001"],
  "usesDefinitions": ["DEF-ME-0004"],
  "truthBindings": [
    {
      "localSpan": "paragraph:12",
      "sourceID": "CLM-ME-0001",
      "relationship": "narrates",
      "requiredMeaning": "closed-system complement only",
      "lastReviewedAgainst": "2.2.0"
    }
  ]
}
```

When a bound claim changes, the story is not automatically rewritten. It receives `review_required: upstream_semantic_change`, shows the changed source statement, and offers a proposed revision.

### 3.5 Evidence node

Evidence remains separate and declares:

- which claim component it bears on
- relation: establishes/supports/qualifies/contradicts/is silent
- coverage, never disguised as probability
- source provenance and citation state
- independence group
- limitations and what it does not show

### 3.6 Bridge node

A bridge connects independently stable source nodes. It owns the mapping, grade, preserved and unpreserved properties, boundary conditions, negative controls, receipts, and propagation permission.

### 3.7 Rendered/composite nodes

Papers, translations, articles, applications, visuals, and reach formats are traceable renderings or composites. They may state claims, but every load-bearing statement must bind to a canonical claim ID or enter quarantine as an unregistered claim candidate.

## 4. Authoring interaction

Typing a reserved command opens the relevant workbench:

```text
claim        evidence      math          definition
story        bridge        kill          paper
translation application   objection     prediction
result       source
```

### Claim command

```text
1. Enter the statement.
2. Semantic resolver searches existing claims and definitions.
3. Choose: new / amend / new version / supersede / add support.
4. Complete the sixty-second Truth Capsule.
5. Expand only claim-class-specific obligations.
6. Stage and close.
7. Review APIs run and attach receipts/exceptions.
8. Human promotes, returns, or quarantines.
```

The UI may remember prior choices and preselect the likely route, but it always displays the selected operation before saving.

## 5. Truth Capsule — collapsed and expanded

Collapsed top:

```text
ID · exact claim · plain claim · kind · status
support present · strongest defeater · largest open gap
```

Expanded record:

- parsing: domain, quantifier, modality, scope
- logical type and evidence burden
- truth/disconfirmation conditions
- definitions and mathematics
- dependencies and enabled dependents
- evidence contract and observations
- inference
- bridges
- countermodels and objections
- source spans and provenance
- review signatures and exceptions
- versions, amendments, and supersession
- public translations, stories, papers, and applications

## 6. Close-event review pipeline

Closing stages an immutable candidate revision and emits an event. It does not directly overwrite canon.

```text
schema validation
 -> semantic duplicate/identity resolution
 -> definition and equation registry check
 -> claim burden/evidence contract check
 -> dependency and status-ceiling check
 -> adversarial review
 -> bridge/propagation review
 -> descent and story-binding review
 -> provenance/version/hash receipt
 -> human adjudication
```

Review outcomes:

- `PASS`
- `PASS_WITH_WARNINGS`
- `EXCEPTION_REQUIRES_HUMAN`
- `BLOCKED_CONTRACT_FAILURE`
- `QUARANTINED_UNRESOLVED`

## 7. Review signatures

Each reviewer signs only what it checked:

```json
{
  "reviewID": "REV-20260825-0001",
  "itemID": "CLM-ME-0001",
  "candidateHash": "sha256:...",
  "reviewerType": "ai | deterministic | human | lean | solver",
  "provider": "",
  "modelOrTool": "",
  "version": "",
  "promptOrPolicyHash": "sha256:...",
  "checksPerformed": [],
  "verdict": "PASS_WITH_WARNINGS",
  "exceptions": [],
  "timestamp": "",
  "signature": ""
}
```

An AI review is not a Lean receipt, empirical replication, or human canon decision.

## 8. Live database and synchronization

Use three layers:

1. **Canonical source:** versioned JSON-LD and registries in Git. This is authoritative.
2. **Live index:** SQLite first, later a service database if needed. It is derived and rebuildable.
3. **Event/outbox log:** records candidate closure, review results, acceptance, rejection, propagation, and quarantine.

The database never becomes an undocumented second canon.

### Accepted-change propagation

An accepted event computes impact through typed edges:

- generated HTML/JSON/views: rebuild automatically
- exact mathematical references: propose deterministic replacement, verify, then rebuild
- definition renderings: update when they inherit canonical wording
- authored stories/articles: mark stale, show affected spans, propose revisions
- propagating bridges: recompute dependent status ceilings
- non-propagating analogies: informational review only
- frozen publications: never rewrite; attach current Atlas status and successor links

## 9. Quarantine

Preserve and quarantine an item when:

- schema is invalid
- identity is ambiguous or duplicates an existing canonical claim
- referenced source/definition/claim is missing
- semantic change is disguised as a patch
- status exceeds dependency ceiling
- bridge requests propagation without sufficient grade/receipt
- story contains an unbound load-bearing assertion
- review returns a blocking contradiction
- source hash or provenance cannot be reconciled

Quarantine records the reason, proposed repair, source location, hash, and restoration/admission path. Nothing is deleted.

## 10. Minimal implementation sequence

1. Ratify type IDs and semantic icon manifest.
2. Split `claimClass` into logical type and burden/species axes.
3. Implement command palette and schema-driven dynamic forms.
4. Implement candidate staging and event/outbox log.
5. Wire deterministic validators before AI reviewers.
6. Implement review receipts and exception panel.
7. Add SQLite projection and dependency-impact queries.
8. Add generated-view rebuilds.
9. Add story truth bindings and stale-span review.
10. Add human canonical promotion and frozen-publication linkage.
