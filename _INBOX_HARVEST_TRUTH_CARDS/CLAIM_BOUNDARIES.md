# Claim Boundaries

This file prevents claim drift.

## Lean Verified

Lean verifies that the definitions and theorems in this repository compile and
type-check.

The current package verifies:

- a toy substrate/coupling-state skeleton;
- stage and mapping structures;
- rejection-first tests for several false positives;
- a quaternion scalar-vector coupling distinction;
- a triadic gate that accepts the intended formal candidates and rejects named
  controls.

## Internally Canonical

Internally canonical means:

- stable enough to preserve;
- consistent with the current Theophysics framework;
- useful as a build target for future formalization;
- not disposable scratch work.

It does not mean:

- peer-reviewed;
- externally endorsed by Lean maintainers;
- a proof of the full theological or physical claim;
- immune from revision after specification review.

## Awaiting External Review

The project is waiting for external Lean-community review. Until those emails
come back, public language should say:

```text
Lean-build verified and internally canonical; external Lean review pending.
```

Do not say:

```text
Lean experts have approved this.
```

## Open Failure Modes

The strongest open failure mode is specification drift: Lean can prove theorems
about definitions that are too weak or too convenient.

The next strongest failure mode is false-positive leakage: a system unrelated to
the intended claim might satisfy the same gate.

Both are productive failure modes. They tell the next Lean pass exactly where to
tighten the formal structure.

