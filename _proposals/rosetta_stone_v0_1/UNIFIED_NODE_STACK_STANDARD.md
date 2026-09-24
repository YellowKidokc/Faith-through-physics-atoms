# Unified Node Stack Standard v0.1

Date: 2026-08-18  
Status: Draft proposal — candidate-only  
Scope: one stable node identity with many attached classification/scoring facets

## 1. Purpose

This standard extends the Rosetta axiom adapter into a general **one-node, many-layer** stack.

The goal is not to flatten every object into a claim. The goal is to let one persistent node carry only the layers that actually apply to it:

- a generalized-question pre-pass;
- unified classification;
- Rosetta/axiom routing;
- Master Equation variables and equations;
- Ten Laws and spiritual-family structure;
- Fruits of the Spirit scoring;
- evidence receipts;
- Trinity / Watcher / consciousness structure;
- applied-domain mappings;
- non-claim satellites such as papers, protocols, objections, translations, and results.

A law atom, equation atom, evidence atom, paper, protocol, and bridge should all be addressable through the same outer envelope without pretending they all carry the same truth burden.

## 2. Frozen rule: node identity is not claim status

Every node gets a stable `node_id` and a `node_core.node_kind`. Only the node core answers **what kind of object this is**.

`node_core.truth_bearing` separates:

- **truth-bearing nodes** — claims, equations treated as mathematical claims, empirical evidence claims, and bridge claims; from
- **non-truth-bearing nodes** — questions, protocols, papers, translations, objections, audience renderings, and result records.

A non-truth-bearing node can still be load-bearing operationally. It must not silently acquire claim force because a classifier attached useful facets to it.

## 3. API order

The API chain is deliberately two-stage first, then facet-specific.

### API 1 — generalized-question pass

Runs before classification. It does not determine truth, canon, proof, or bridge grade.

It asks the four domain-neutral questions already present in the master schema:

1. `q1_before` — What must exist before this?
2. `q2_capability` — What can this do that nothing before it could?
3. `q3_collapse` — What breaks if this is removed?
4. `q4_translation` — What does this look like in another domain?

The output is candidate text plus source spans/confidence where available. It becomes `question_pass`, and it feeds API 2.

### API 2 — unified classification pass

Classifies the object produced by API 1 and the source record. It may propose:

- `claim_type`
- `proof_class`
- `proof_label`
- `display_grade`
- `domains`
- `primary_domain`
- `epistemic_layer`
- `blast_radius`
- `primary_law`
- `bridge_grade` where a bridge is actually present

Classification is still only classification. It cannot promote the node.

### API 3+ — facet scorers/connectors

After classification, specialized scorers attach only relevant facets:

- Rosetta/axiom connector
- Master Equation facet scorer
- Ten Laws scorer
- Fruits scorer
- Evidence scorer
- Trinity/Watcher/consciousness scorer
- Applied-domain scorer
- Non-claim object linker

Facet scorers may be run in parallel after API 2, but receipts must preserve which scorer produced which facet.

## 4. Core envelope

The outer envelope is `atlas-unified-node/v0.1`:

```json
{
  "schema_version": "atlas-unified-node/v0.1",
  "node_id": "",
  "node_core": {
    "title": "",
    "node_kind": "claim | evidence | equation | bridge | question | protocol | paper | translation | objection | result | audience | container",
    "truth_bearing": false,
    "canonical_uri": null,
    "primary_claim": null
  },
  "question_pass": {
    "status": "not_run",
    "generalized_questions": []
  },
  "classification": {},
  "facets": {},
  "governance": {},
  "provenance": {},
  "native": {}
}
```

`facets` is sparse: omit a facet when it has not been run or does not apply. An empty object is not a score. `status: not_run` inside a facet is an explicit processing state, not absence.

## 5. Claim and non-claim separation

The unified schema uses `node_kind` for the object's operational role and `classification.claim_type` for the one-axiom claim vocabulary.

Examples:

- `AX-112` has `node_kind: evidence` and may classify as `EVIDENCE`.
- `ME-EQ-009` has `node_kind: equation` and may classify as `MODEL` unless a stronger formal status is separately established.
- `TL-01-004` has `node_kind: claim` and may classify as `BRIDGE`/`IDENTIFICATION` depending on the component being classified.
- A paper or HTML page has `node_kind: paper`; it can carry document-level facet scores without becoming a claim.
- A question from API 1 can be emitted as `node_kind: question`, `truth_bearing: false`.

For multi-component claims, the node keeps one identity and may list component-level classifications inside a facet or `native.claimComponents`. Do not collapse a supported physics component and an open theological bridge component into one inherited truth status.

## 6. Facet contracts

### 6.1 `axiom_rosetta`

Carries the PR-16 Rosetta projection when the node is an axiom or axiom-like claim:

- source Rosetta node reference;
- exact-ID and lexical routing targets;
- truth unit;
- mirror-search status;
- bridge evaluation and compression stubs where applicable.

This facet routes. It does not prove, admit, canonize, or rewrite the native axiom.

### 6.2 `master_equation`

Records Master Equation engagement:

- `chi_variables` using the current schema vocabulary: `G`, `M`, `E`, `S_eff`, `T`, `K`, `R`, `Q`, `F`, `C_W`;
- `primary_law`;
- equation references and normal forms;
- optional `chi_score` only when a scorer actually ran.

The schema preserves the canonical C/C_W firewall: `C_W` is the coherence wrapper. A retired ten-factor product or raw-C shape must be carried as native history or an open ruling, not silently normalized into canon.

### 6.3 `ten_laws`

Records law-level structure:

- engaged laws `L01`-`L10`;
- spiritual-family terms;
- derived terms, correspondence terms, and anti-terms;
- phase forms;
- equations;
- derivation-chain status;
- source node references.

Derivation status must preserve the native canon vocabulary. It must not convert `MAPPED`, `LOCKED`, or `DERIVED` into C0-C6 or proof labels unless David rules that mapping.

### 6.4 `fruits`

Records observable Fruit structure when present:

- English and Greek term;
- equation;
- anti-fruit;
- phase form;
- depth: `mentioned`, `explained`, `equation_present`, `derived`, `evidence_linked`;
- source spans or source node references.

The Law 4 two-tier ruling must remain visible. Love, Peace, and Joy may carry Tier-1 derived status only where the source actually carries that claim; the remaining six remain structural correspondences unless separately promoted by David.

### 6.5 `evidence`

Evidence items get explicit empirical metadata:

- source/dataset;
- citation or artifact path;
- sigma level and p-value where actually stated;
- replication status;
- supported/related claim references;
- contradiction or dispute notes;
- evidence-layer marker.

An evidence facet does not make the supported claim true. `propagates_evidence` remains `false` unless a later human-gated verification rule says otherwise.

### 6.6 `trinity_watcher`

Reserved for consciousness/Watcher structure:

- measurement problem;
- von Neumann chain;
- personhood bridge;
- Phi/integration measure;
- mirror search;
- Watcher/observer role;
- Trinity structural mapping.

This is a cross-cutting classification domain, not a blanket L4 promotion. Each component keeps its own epistemic layer and bridge status.

### 6.7 `applied_domains`

Records applied patterns across:

- psychology
- economics
- education
- history
- semantic entropy
- somatic
- other

Each item names the relevant law, Master Equation variable, claimed pattern, supporting evidence references, and a conservative strength marker.

### 6.8 `non_claim_objects`

Links satellites without promoting them:

- protocols
- papers
- translations
- objections
- results
- audience renderings
- containers
- questions

Each satellite needs a relation (`describes`, `tests`, `objects_to`, `renders`, `reports_result_of`, `contains`, etc.) and must remain non-truth-bearing unless separately emitted as a claim node.

## 7. Scoring rule

There are two different uses of facets:

1. **source projection** — what the source record itself declares;
2. **document scoring** — what an external scorer finds in a paper, article, or object.

Every scored facet must set `facet_mode` to one of these. Do not mix them.

For example, `ME-EQ-010` projects the nine-term fruit vector as source structure. That does **not** mean nine fruits were observed in a target document. A document scorer must create its own `facet_mode: document_score` result.

## 8. Governance and gates

All generated unified nodes enter as candidates.

Required defaults:

```json
{
  "candidate_or_admitted": "Candidate",
  "kernelChecked": false,
  "propagates_evidence": false,
  "propagates_falsification": false,
  "human_gate_required": true,
  "no_truth_promotion_from_routing": true,
  "no_truth_promotion_from_scoring": true
}
```

Do not set:

- `kernelChecked: true` unless a named kernel actually checked the object;
- `propagates_evidence: true` or `propagates_falsification: true` by default;
- `canonicalStatus: canon`;
- `proof_label: LEAN_FULL_VERIFIED` without an actual Lean receipt.

API routing, facet scoring, and document classification never promote a node to canon.

## 9. Sparse storage rule

Store only what exists:

- omit facets that were not run;
- omit optional scores that were not computed;
- use `null` for an applicable but unknown scalar;
- use `status: not_run` only when a runner is expected later;
- preserve native fields under `native` rather than duplicating them into speculative normalized fields.

This keeps the envelope useful for both tiny question nodes and large claim nodes.

## 10. Relationship to PR #16

PR #16 standardizes **axioms into Rosetta node envelopes**. This proposal stacks above it and standardizes **the wider object/facet envelope**.

PR #16 remains the axiom connector layer. This layer may reference a Rosetta node produced by PR #16, but it does not alter the fixed Rosetta connector spec.

## 11. Current test scope

A local read-only probe prototype projected representative existing records into the unified envelope (harness omitted from this review diff to keep the proposal small):

- `TL-01-004` — Law 4, spiritual-family and Fruits structure;
- `TL-01-009` — Law 9, conservation structure and open components;
- `ME-01-060` — full Master Equation;
- `ME-EQ-009` — Fruits phase-transition equation;
- `ME-EQ-010` — nine-term Fruit vector;
- `AX-111` — GCP evidence;
- `AX-112` — PEAR evidence.

The Trinity folder currently has stage scaffolding rather than a concrete canonical atom, so the `trinity_watcher` facet is schema-reserved and not force-filled.

## 12. Acceptance tests

A valid implementation must show that:

1. every generated node validates against `unified_node_stack.schema.json`;
2. native source records are read-only;
3. all outputs are candidates;
4. all propagation flags are false;
5. node kind and claim type remain separate;
6. source projections and document scores are labeled separately;
7. sparse facets stay sparse;
8. API 1 output is stored before API 2 output;
9. facet outputs identify their scorer;
10. no generated node claims canon, kernel verification, or live API execution that did not happen.

## 13. Open rulings for David

1. Should `TL` law atoms keep `BRIDGE` as the outer unified claim type while component classifications carry the supported/open split?
2. Should document-level Fruits scoring use the six-step depth scale in §6.4, or the simpler `0/1/2` scale used by the HTML tiles?
3. Should evidence nodes like AX-111/AX-112 remain `node_kind: evidence`, or should they stay `node_kind: claim` with an evidence facet?
4. Should applied-domain scores live on the evidence node, the paper node, or both with different `facet_mode` values?
5. Is the proposed two-stage API order the right contract for local DeepSeek runs, or should API 1 and API 2 be one batched call with two separately stored outputs?
