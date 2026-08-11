# Build Spec Hardening

This file records corrections that prevent false confidence in the map/API
layer.

## Marker 12

Marker 12, Evidence Grade, is computed.

It must be treated as:

`Yes (derived from native via grade_registry)`

Computed fields 12, 13, 14, and 15 are never fabricated. Marker 12 may be
projected only from admitted native evidence coverage and `grade_registry`
rules.

## Grade Registry

`C0` retired overclaims map to `-` with `alert_state: SUPERSEDED`. They do not
receive active grade `D`. Grade `D` is reserved for active overclaims still in
the evaluative conversation.

Method convergence examples must use the actual scale. A `C5 / C5 / C2` result
is a dispute to inspect; do not normalize it to `C4`.

## Meeting State

Meeting states are:

- `CONVERGED`
- `PRESSURE`
- `PREDICTED_NOT_OBSERVED`
- `UNRESOLVED`
- `CONTRADICTED`

`CONTRADICTED` means descent predicts X while ascent finds not-X with admitted
high warrant. It requires suspension review for the affected bridge or claim.

## Reproducibility vs Independent Validation

Reproducibility means same inputs produce same outputs. It proves the process is
deterministic.

Independent validation requires different rubric, different schema, or
adversarially chosen inputs producing a convergent result. Only independent
validation upgrades standing.

## Load-Bearing Pre-Admission Gate

Any atom with `computed_load_bearing = true` and
`origin = ai_inference_unverified` is blocked from candidate graph admission
until it has a formal receipt or human audit entry.

## Open Item / Resolution Beacon

Open Item and Resolution Beacon are the same stored object type. The UI may
display either label depending on context.

## Conflict Resolution

Every later resolution edge may carry `warrant_strength` and
`scope_limitation`. The Atlas computes the strongest warranted state. If two
equal-strength admitted edges contradict under overlapping scope, the open item
enters `DISPUTED` and awaits audit.

## Phi Operation Procedure

1. Select source and target atom sets.
2. Normalize components, equations, assumptions, and negative guards.
3. Compute candidate similarity over declared components and equations.
4. Inject negative controls from unrelated domains or known failed bridges.
5. Compute directionality by checking whether source assumptions preserve target
   predicates without adding forbidden structure.
6. Run ablation by removing each assumed correspondence.
7. Mark `ablation_result = survived` only if the bridge still preserves the
   declared invariant under ablation.
8. Emit a bridge candidate, never an accepted bridge.
9. Require adversarial review and human acceptance before propagation.
