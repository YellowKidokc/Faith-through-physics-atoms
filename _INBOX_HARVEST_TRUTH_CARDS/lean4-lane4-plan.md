# Lean 4 Lane 4 Plan

## Objective

Convert the Theophysics canon into a typed formal skeleton before attempting proofs.

This lane is not the theological proof lane, and it is not the empirical validation lane. It is the structural integrity lane.

## Rule

Do not encode all 190/191 nodes as Lean axioms.

Only true primitives may become candidate axioms. Definitions become definitions. Theorems become proof targets. Equations become typed formal objects or propositions. Identifications and bridge claims require explicit bridge assumptions. Predictions, protocols, evidence nodes, and falsification criteria stay outside the proof kernel.

## Phase 1 - Typed Canon

Output files:

- `typed-canon-reclassification.csv`
- `typed-canon-reclassification.json`
- `typed-canon-summary.md`

Checks:

- Every node has one claim type.
- Every node has one logical-force label.
- Every dependency is explicit.
- Duplicate IDs are collapsed or flagged.

## Phase 2 - Graph Hygiene

Lean or script checks:

- Missing dependency IDs.
- Circular dependencies.
- Nodes with no upstream where they are not primitive.
- Nodes with no downstream where they are not terminal, evidence, prediction, or protocol.
- Theorems depending directly on predictions or evidence nodes.
- Identifications used as derivations without bridge guards.

## Phase 3 - Formalizable Chains

Start with short chains:

1. A1.1 Existence -> A1.2 Distinction -> A1.3 Information Primacy.
2. A1.2 + D1.1 -> D1.2 Bit Definition.
3. D3.1 -> P3.1 Coherence Non-Negativity, if the measure is typed nonnegative.
4. P3.2 -> T3.1 Coherence Cannot Self-Increase, only after separating micro-coherence conservation from macro-coherence/entropy behavior.
5. D8.1 Sign Operator -> T8.1 Sign Invariance, if the sign-state algebra is encoded.
6. D9.1 Grace Operator -> P9.1 Grace Idempotence, if G-hat is modeled as a projection-like operator.

## Phase 4 - Bridge Guarding

All bridge claims get explicit labels:

- formal derivation
- metaphysical inference
- structural analogy
- theological identification
- empirical hypothesis

No bridge claim may be used as a theorem premise unless a named bridge assumption is explicitly imported.

## Phase 5 - Report Back

Generate:

- proof-ready chains
- partially formalizable chains
- outside-kernel claims
- high-risk bridge claims
- contradiction/cycle risks
- missing definitions

## Bottom Line

Lean 4 can help make the skeleton honest. It cannot verify broad theological or empirical reality until those claims are translated into precise formal objects. The first win is not proving Theophysics. The first win is preventing Theophysics from accidentally treating every powerful sentence as an axiom.
