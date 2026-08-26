# Theophysics Typed Canon - Lane 4 First Pass

Generated: 2026-07-04T13:13:04

## Purpose

This is the first-pass typed canon for Lean 4 preparation. It does not treat every node as an axiom. It separates primitives, definitions, framework commitments, equations, theorems, bridge claims, empirical nodes, predictions, protocols, meta-claims, and closure claims.

## Counts by New Type

- Definition: 38
- Primitive: 33
- Theorem: 27
- Property: 15
- Equation: 12
- BoundaryCondition: 9
- ObservableDomain: 9
- FrameworkCommitment: 8
- EvidenceNode: 6
- Protocol: 5
- UniversalPrinciple: 4
- Hypothesis: 4
- FalsificationCriterion: 3
- MetaClaim: 3
- CapstoneTerminalClaim: 3
- BridgePrinciple: 3
- OpenProblem: 2
- Prediction: 2
- Corollary: 2
- ClosureClaim: 1
- Identification: 1
- Operator: 1

## Counts by Risk Level

- high: 19
- low: 71
- medium: 70
- medium-high: 31

## Manual Cleanups Applied

- EXP5.1 and EXP5.2 classified as EvidenceNode.
- PERSONHOOD classified as OpenProblem / axiomatic gap.
- P3 classified as Primitive / primordial stage.
- LAMBDA classified as CapstoneTerminalClaim.
- Duplicate A1.1 collapsed by keeping the fuller claim.

## Lean 4 Rule

Only true primitives should become Lean axioms. Definitions become definitions. Theorems become proof targets. Predictions, protocols, and evidence nodes stay outside the proof kernel as metadata or test objects. Bridge identifications and theological identifications require explicit assumptions and should not be silently used as formal derivations.

## Files

- typed-canon-reclassification.csv
- typed-canon-reclassification.json
- TheophysicsCanon.lean
- lean4-lane4-plan.md
