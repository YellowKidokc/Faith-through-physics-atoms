# Prediction Registry v1

This page is the short human-readable registry for the current Theophysics
Lagrangian test bench.

It sits between two mistakes:

1. saying the framework is already proven
2. pretending the formal work means nothing until every later layer is done

The right claim is smaller and stronger:

The current equations generate testable behavior under a shared comparison
regime, and those behaviors can be frozen before later interpretation.

## What This Registry Is For

- record predictions before later tuning
- state the test rule before the result
- make failure visible
- separate formal structure from theological interpretation
- give the Lean 4 layer a neighboring verification layer rather than treating
  any one tool as sufficient by itself

## Boundary Statement

This registry does not prove Theophysics true.

It records what the present model family does under explicit conditions.

A pass means:

`the model behaved as claimed under the tested regime`

A failure means:

`the wording, derivation, or equation form must be revised, downgraded, or rejected`

## Current Registered Results

### P1 - Resistance Penalty

- Claim: increasing `W` should reduce the usable canonical coherence score
- Why it matters: resistance is supposed to be load-bearing, not decorative
- Test rule: compare `balanced` against `resistance_drag`
- Current result: `14.48 -> -4.72`
- Status: `PASS`

### P2 - Source / Sink Asymmetry

- Claim: adding `chi10` is not equivalent to merely reducing `Gamma9`
- Why it matters: source and sink are structurally different operations
- Test rule: compare source-rich and sink-heavy deltas from the same baseline
- Current result: `+3` vs `-5`
- Status: `PASS`

### P3 - Spirit / Anti Contrast Pair

- Claim: Spirit and Anti should classify the same regime in opposite directions
- Why it matters: the contrast pair should be exact, not rhetorical
- Test rule: run identical regimes through both forms
- Current result: balanced `3` vs `-3`; entropy-heavy `-2` vs `2`
- Status: `PASS`

### P4 - Collapse Threshold

- Claim: there should be a resistance boundary where canonical v2 flips from
  positive to negative
- Why it matters: this is the strongest current numerical prediction
- Test rule: solve canonical v2 for `L = 0` under the shared balanced regime
- Current result: `W ~= 0.566987298107781`
- Status: `PASS`

### P5 - Conserved Coherence Candidate

- Claim: if the action structure is meaningful, some symmetry-backed invariant
  should appear
- Why it matters: this is the doorway toward a real conservation argument
- Test rule: first require exact algebraic invariants under constrained
  transforms before claiming any full Noether result
- Current result:
  - paired source/sink shift leaves `L` unchanged
  - source/sink enters as `chi10 - Gamma9`
  - repeated channel core is recoverable exactly
- Status: `PASS`, but only at the `algebraic-invariant` level

### P7 - Wrong-Control Rejection

- Claim: bad rewrites should fail under the same bench the canonical model
  survives
- Why it matters: if wrong controls also pass, the architecture is not doing
  real work
- Test rule: run canonical and deliberately wrong variants through the same
  regimes and `W` sweep
- Current rejected controls:
  - `gamma9_added`
  - `chi10_subtracted`
  - `resistance_ignored`
  - `source_sink_swapped`
- Status: `PASS`

### P10 - Grace-Leak Nonlinearity

- Claim: resistance should produce curved loss, not simple linear degradation
- Why it matters: `(1-W)^2` should show up in behavior, not only in notation
- Test rule: measure curvature across the `W` sweep
- Current result: midpoint second difference `16`
- Status: `PASS`

## What We Learned From The Variation Audit

This part matters because it keeps us honest.

The current harness did **not** magically derive every hoped-for theological
statement from the simplest Spirit form.

What it actually showed:

- the bare Spirit form is formally well-shaped
- but bare variation with respect to `x(t)` does **not** insert entropy
  directly into the equation of motion
- entropy enters directly only when:
  - entropy is coupled to the varied coordinate
  - `chi` is treated as the varied field
  - or extra dissipative structure is introduced

That is not a defeat.

That is exactly the kind of negative result a serious verification layer should
surface.

## Why This Belongs Next To Lean 4

Lean 4 checks formal proof structure inside the theorem environment.

This lab checks different questions:

- do the candidate equations translate cleanly into a symbolic engine
- do the added terms share compatible dimension classes
- do side-by-side variants behave differently for principled reasons
- do wrong controls fail
- do predictions survive being written before later interpretation

Lean 4 is not enough by itself.
Python is not enough by itself.
The website is not enough by itself.

Together they start to form a verification stack:

1. conceptual claim
2. equation form
3. symbolic translation
4. side-by-side comparison
5. wrong-control rejection
6. preregistered prediction
7. timestamped artifact trail
8. later empirical comparison

That stack is the real point.

## Next Additions

- trajectory simulations for source-rich stability claims
- empirical comparisons against known benchmark models
- plots for the resistance threshold and nonlinear loss curve
- a cleaner Noether program with explicit scope limits
- a site-facing summary block for the Lean 4 section
