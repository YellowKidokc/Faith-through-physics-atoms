# Unified Node Stack Receipt — 2026-08-18

## Gate statement

All files in this proposal are **Candidate**. No source atom was edited. No generated node is canon. `kernelChecked` remains `false`; `propagates_evidence` and `propagates_falsification` remain `false`; David alone can promote anything.

No live API call was made from the sandbox. The generalized-question pass is represented as `not_run`, and all sample facets are deterministic source projections.

## Proposal files

| File | Purpose |
|---|---|
| `UNIFIED_NODE_STACK_STANDARD.md` | Human standard for the one-node/many-facet stack |
| `unified_node_stack.schema.json` | JSON Schema draft 2020-12 contract |
| `unified_node_api_chain.yaml` | Ordered API/facet-runner contract |

The read-only probe harness, generated example envelopes, and local run manifest are intentionally not committed in this review diff. The local test results are recorded below; the harness can be added in a follow-up implementation PR after the contract shape is approved.

## Architecture tested

The tested envelope separates:

1. `node_core` — operational object kind and truth-bearing flag;
2. `question_pass` — API 1, the generalized non-claim question pre-pass;
3. `classification` — API 2, the unified one-axiom classification layer;
4. `facets` — sparse layer-specific outputs;
5. `governance` — candidate-only gates;
6. `provenance` — adapter and source hashes;
7. `native` — original record, preserved rather than rewritten.

## Representative records projected

| Source record | Node kind | Facets exercised |
|---|---:|---|
| `TL-01-004-law-04-strong-force-yukawa-agape.jsonld` | claim | Ten Laws, Master Equation, Fruits |
| `TL-01-009-law-09-weak-force-fermi-conservation.jsonld` | claim | Ten Laws, Master Equation |
| `ME-01-060-full-master-equation.jsonld` | equation | Master Equation |
| `ME-EQ-009-fruits-phase-transition.jsonld` | equation | Master Equation, Fruits |
| `ME-EQ-010-fruit-vector.jsonld` | equation | Master Equation, Fruits |
| `AX-111-gcp-correlation.jsonld` | evidence | Evidence, Trinity/Watcher boundary stub |
| `AX-112-pear-lab-results.jsonld` | evidence | Evidence, Trinity/Watcher boundary stub |

## Run result

Local prototype command:

```bash
python3 _proposals/rosetta_stone_v0_1/build_unified_node_examples.py --root .
```

Result:

- source records read: **7**
- unified nodes written: **7**
- duplicate node IDs: **0**
- JSON Schema validation errors: **0**
- source atoms modified: **0**
- live API used: **false**

Additional local checks:

```bash
python3 -m py_compile _proposals/rosetta_stone_v0_1/build_unified_node_examples.py
python3 -m json.tool _proposals/rosetta_stone_v0_1/unified_node_stack.schema.json
```

Both passed.

## Boundary checks

- The Rosetta connector spec from PR #16 was not edited.
- Existing source atoms remain read-only inputs.
- `question_pass.status` is `not_run` in every example.
- Every example has `proof_label: NOT_ESTABLISHED` because no new verification was run.
- Law 4 keeps the native `MAPPED` grade while separately carrying the operator-supplied derivation-chain status.
- Law 4 Fruits preserve the Tier 1/Tier 2 split: Love/Joy/Peace are marked `tier1_derived`; the remaining six are marked `tier2_correspondence`.
- The full Master Equation example preserves the historical source expression and carries a C/C_W boundary note instead of silently resolving the open χ/C ruling.
- GCP/PEAR examples are evidence nodes with `replication_status: disputed` and `do_not_promote: true`.
- Trinity/Watcher is present only as a boundary stub on consciousness evidence; no Trinity, personhood, Phi, or Watcher component was asserted from those source atoms.

## Known limits

1. This is a source-projection probe, not a document scorer.
2. The seven examples do not yet exercise a real paper node, protocol node, objection node, translation node, result node, or question node.
3. API 1 and API 2 payloads are specified but not executed here.
4. The current Trinity folder contains stage scaffolding, not a concrete canonical atom to project.
5. Applied-domain examples are schema-supported but not yet populated from a concrete source atom.
6. The operator-supplied statement that Laws 4, 5, and 9 derivation chains are complete is carried as an open-item-backed candidate note; receipts still need to be ingested into this repo.

## Review questions for David

1. Keep evidence atoms as `node_kind: evidence`, or keep them as claims with an evidence facet?
2. Should the outer claim type for Ten Laws atoms be `BRIDGE`, `IDENTIFICATION`, or component-only with no single outer type?
3. Should document-level Fruits scoring use the five-step depth scale here or the simpler tile scale?
4. Should API 1 and API 2 remain two separate local calls, or become one batched call that writes two separate receipts?
5. Should this stack land as a separate PR after PR #16, or be folded into PR #16 before merge?
