# Formalization Plan

## Phase 1: Toy Structural Core

Goal: formalize only the claims that are already crisp.

- Coupling states `C0` and `C1`.
- A transition relation from `C0` to `C1`.
- Irreversibility relative to that relation.
- The multiplicative `Q = 0` gate in the toy master equation.

Status: started.

## Phase 2: Stage Machine

Goal: represent the sequence without pretending the physics is already proved.

- Define stages: localization, stabilization, release, confirmation,
  redistribution.
- Define legal transitions between stages.
- Prove basic reachability and non-reversal facts.

Status: started.

## Phase 3: Mapping Preservation

Goal: test the "candidate isomorphism" language.

- Define a physics-side operation sequence.
- Define a theology-side operation sequence.
- Define a mapping between sequences.
- Prove or refute preservation of order and composition.

Status: started with order mapping; composition preservation is still open.

Law 4 status update: minimal `LawIso` proved the binary abstraction but admitted
a coin false positive. Enriched `RichLawIso` added role and transition
preservation, blocked the natural coin false positive, but still admits a
deliberately relabeled coin. The next task is semantic grounding: connect each
formal role/transition field to source-justified physics/theology claims.

All-factor bridge update: `BridgeMatrix` now encodes the ten canonical factor
rows, validates their physical/spiritual signatures, rejects several targeted
semantic swaps, and rechecks full-product zero collapse for every slot. The
remaining burden is source-grounding and richer equation-level signatures.

## Phase 4: Axioms vs Theorems

Goal: make assumptions impossible to miss.

- Put speculative assumptions in a dedicated namespace or file.
- Keep proved toy claims in separate files.
- Maintain the claim matrix as the public audit trail.

## Phase 5: Empirical Interface

Goal: define test targets without claiming Lean can test history.

- Define candidate coupling-domain observables.
- Separate historical datasets from formal definitions.
- Track what would count as confirmation, disconfirmation, or non-testability.
