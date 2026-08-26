# Lagrangian Side-by-Side Report

Generated: `2026-06-24T10:28:54`

This harness does **not** decide whether the framework is true.
It checks whether each candidate behaves like a disciplined formal model under the same test bench.

## Plain-English Variables

- `chi` / `chi_bar`: coherence weight. Higher means the system can carry ordered motion.
- `S_entropy` / `S_v1`: entropy drag. Higher means more disorder pressure.
- `W`: resistance or grace leak. Higher means the system resists alignment.
- `chi10`: upward source term. Think coherence support, grace support, or Christ-source term.
- `Gamma9`: downward sink term. Think decoherence drain, adversary sink, or collapse pressure.
- `xdot` / `Fdot` / `Fsum_dot`: activity term. Motion through the system.
- `V`: stored potential cost. What the system has to carry or overcome.

## Same Regimes For Every Model

- **balanced**: `K=1`, `chi=1`, `chi_bar=1`, `xdot=2`, `Fsum_dot=3`, `S_entropy=1`, `S_v1=4`, `W=1/5`, `Fdot=2`, `V=1`, `chi10=3`, `Gamma9=1`
- **resistance_drag**: `K=1`, `chi=1`, `chi_bar=1`, `xdot=2`, `Fsum_dot=3`, `S_entropy=1`, `S_v1=4`, `W=4/5`, `Fdot=2`, `V=1`, `chi10=3`, `Gamma9=1`
- **source_rich**: `K=1`, `chi=1`, `chi_bar=1`, `xdot=2`, `Fsum_dot=3`, `S_entropy=1`, `S_v1=4`, `W=1/5`, `Fdot=2`, `V=1`, `chi10=6`, `Gamma9=1`
- **sink_heavy**: `K=1`, `chi=1`, `chi_bar=1`, `xdot=2`, `Fsum_dot=3`, `S_entropy=1`, `S_v1=4`, `W=1/5`, `Fdot=2`, `V=1`, `chi10=3`, `Gamma9=6`
- **entropy_heavy**: `K=1`, `chi=1`, `chi_bar=1`, `xdot=2`, `Fsum_dot=3`, `S_entropy=6`, `S_v1=12`, `W=1/5`, `Fdot=2`, `V=1`, `chi10=3`, `Gamma9=1`

## Model Scorecards

### LLC v1 (historical compression form)

- Summary: Single compression form: substrate-scaled coherence minus entropy penalty.
- Expression: `Fsum_dot**2*K*chi - K*S_v1*chi`
- Reduction note: Historical baseline only; useful for correspondence checks against v2-style limits.
- What helps: Higher total motion-through-order (Fsum_dot^2) helps the score.
- What hurts: Higher entropy penalty hurts the score.
- Grace leak handle: No explicit free-will resistance term in this historical form.

**Dimension checks**
- `PASS` v1 bracket compatibility: expected `action_density`, observed `action_density | action_density`

**Response signs**
- `S_entropy` -> `n/a`
- `S_v1` -> `-K*chi`
- `W` -> `n/a`
- `chi10` -> `n/a`
- `Gamma9` -> `n/a`

**Euler-Lagrange**
- equation: `2*K*(chi(t)*Derivative(Fsum(t), (t, 2)) + Derivative(Fsum(t), t)*Derivative(chi(t), t))`
- solved acceleration: `-Derivative(Fsum(t), t)*Derivative(chi(t), t)/chi(t)`

**Regime values**
- `balanced` -> `5.00000000000000`
- `resistance_drag` -> `5.00000000000000`
- `source_rich` -> `5.00000000000000`
- `sink_heavy` -> `5.00000000000000`
- `entropy_heavy` -> `-3.00000000000000`

**Regime deltas vs balanced**
- `resistance_drag` delta -> `0`
- `source_rich` delta -> `0`
- `sink_heavy` delta -> `0`
- `entropy_heavy` delta -> `-8.00000000000000`

### Spirit Lagrangian

- Summary: Coherence-weighted activity minus entropy drag.
- Expression: `-S_entropy*chi + chi*xdot**2`
- Reduction note: This is the simplest live candidate for direct symbolic checks.
- What helps: Activity helps if coherence weight is present.
- What hurts: Entropy directly drags the value down.
- Grace leak handle: No explicit resistance term; leak is seen mainly through entropy drag.

**Dimension checks**
- `PASS` spirit add/subtract compatibility: expected `action_density`, observed `action_density | action_density`

**Response signs**
- `S_entropy` -> `-chi`
- `S_v1` -> `n/a`
- `W` -> `n/a`
- `chi10` -> `n/a`
- `Gamma9` -> `n/a`

**Euler-Lagrange**
- equation: `2*chi(t)*Derivative(x(t), (t, 2)) + 2*Derivative(chi(t), t)*Derivative(x(t), t)`
- solved acceleration: `-Derivative(chi(t), t)*Derivative(x(t), t)/chi(t)`

**Regime values**
- `balanced` -> `3.00000000000000`
- `resistance_drag` -> `3.00000000000000`
- `source_rich` -> `3.00000000000000`
- `sink_heavy` -> `3.00000000000000`
- `entropy_heavy` -> `-2.00000000000000`

**Regime deltas vs balanced**
- `resistance_drag` delta -> `0`
- `source_rich` delta -> `0`
- `sink_heavy` delta -> `0`
- `entropy_heavy` delta -> `-5.00000000000000`

### Anti-Lagrangian

- Summary: Sign-inverted contrast model: anti-coherence or collapse-seeking behavior.
- Expression: `S_entropy*chi - chi*xdot**2`
- Reduction note: Should be exactly the negative of the Spirit Lagrangian.
- What helps: Entropy helps this model instead of hurting it.
- What hurts: Ordered activity hurts this model instead of helping it.
- Grace leak handle: Useful as a contrast model for systems that appear to reward collapse.

**Dimension checks**
- `PASS` anti add/subtract compatibility: expected `action_density`, observed `action_density | action_density`

**Response signs**
- `S_entropy` -> `chi`
- `S_v1` -> `n/a`
- `W` -> `n/a`
- `chi10` -> `n/a`
- `Gamma9` -> `n/a`

**Euler-Lagrange**
- equation: `-2*chi(t)*Derivative(x(t), (t, 2)) - 2*Derivative(chi(t), t)*Derivative(x(t), t)`
- solved acceleration: `-Derivative(chi(t), t)*Derivative(x(t), t)/chi(t)`

**Regime values**
- `balanced` -> `-3.00000000000000`
- `resistance_drag` -> `-3.00000000000000`
- `source_rich` -> `-3.00000000000000`
- `sink_heavy` -> `-3.00000000000000`
- `entropy_heavy` -> `2.00000000000000`

**Regime deltas vs balanced**
- `resistance_drag` delta -> `0`
- `source_rich` delta -> `0`
- `sink_heavy` delta -> `0`
- `entropy_heavy` delta -> `5.00000000000000`

### LLC v2 (canonical wrapper form)

- Summary: Substrate wrapper around eight internally dual channels, plus upward source and downward sink.
- Expression: `8*Fdot**2*K*W**2*chi_bar - 16*Fdot**2*K*W*chi_bar + 8*Fdot**2*K*chi_bar - Gamma9*K - 8*K*V + K*chi10`
- Reduction note: Best current candidate for testing resistance, source, and sink behavior side by side.
- What helps: Higher coherent channel activity and stronger chi10 source raise the value.
- What hurts: Resistance W, large native potential cost, and Gamma9 sink lower the value.
- Grace leak handle: Explicit: as W rises, the useful kinetic term shrinks by (1-W)^2.

**Dimension checks**
- `PASS` v2 channel term compatibility: expected `action_density`, observed `action_density + action_density + action_density | action_density`
- `PASS` v2 source/sink compatibility: expected `action_density`, observed `action_density + action_density + action_density + action_density | action_density | action_density`

**Response signs**
- `S_entropy` -> `n/a`
- `S_v1` -> `n/a`
- `W` -> `16*Fdot**2*K*chi_bar*(W - 1)`
- `chi10` -> `K`
- `Gamma9` -> `-K`

**Euler-Lagrange**
- not run: No single time-dependent generalized coordinate declared for this model.

**Regime values**
- `balanced` -> `14.4800000000000`
- `resistance_drag` -> `-4.72000000000000`
- `source_rich` -> `17.4800000000000`
- `sink_heavy` -> `9.48000000000000`
- `entropy_heavy` -> `14.4800000000000`

**Regime deltas vs balanced**
- `resistance_drag` delta -> `-19.2000000000000`
- `source_rich` delta -> `3.00000000000000`
- `sink_heavy` delta -> `-5.00000000000000`
- `entropy_heavy` delta -> `0`

## Cross-Model Checks

- **anti_vs_spirit** `PASS`: Anti-Lagrangian should equal the negative of Spirit.
  - result: `0`
- **llc_v2_zero_resistance_limit** `PASS`: Canonical v2 with W=0 and no source/sink should reduce to a pure channel core.
  - result: `8*(Fdot**2*chi_bar - V)`
- **llc_v1_core_reference** `PASS`: Historical v1 core for side-by-side correspondence reference.
  - result: `chi*(Fsum_dot**2 - S_v1)`
- **resistance_penalty_sign** `PASS`: In v2, increasing W should hurt the active kinetic contribution.
  - result: `16*Fdot**2*K*chi_bar*(W - 1)`
- **source_sink_direction** `PASS`: In v2, chi10 should help and Gamma9 should hurt.
  - result: `{"dL/dchi10": "K", "dL/dGamma9": "-K"}`
- **historical_vs_canonical_note** `PASS`: v1 and v2 are not algebraically identical, but should be judged under the same regimes.
  - result: `v1 uses Fsum_dot=Fsum_dot; v2 uses per-channel activity=Fdot, resistance=W, and source/sink terms.`

## Preregistered Predictions

These are the parts that matter if you want the process to be hard to contest later:
claim first, rule first, result second.

### P1 Resistance Penalty

- Claim: Increasing resistance W should reduce canonical LLC v2 under the same regime.
- Why: The v2 kinetic contribution is suppressed by (1-W)^2, so usable coherence should fall as W rises.
- Test: Compare balanced vs resistance_drag using the same canonical v2 parameters.
- Failure: If resistance_drag is greater than or equal to balanced, the grace-leak story is weak.
- Result: `balanced=14.4800000000000, resistance_drag=-4.72000000000000`
- Verdict: `PASS`

### P2 Source-Sink Asymmetry

- Claim: Adding chi10 is not equivalent to merely reducing Gamma9.
- Why: The framework treats source and sink as different structural roles, not one reversible slider.
- Test: Compare delta(source_rich - balanced) against the magnitude of delta(sink_heavy - balanced).
- Failure: If the magnitudes match exactly across the shared regime, the asymmetry claim is not supported here.
- Result: `source_delta=3.00000000000000, sink_delta=-5.00000000000000`
- Verdict: `PASS`

### P3 Spirit-Anti Discriminator

- Claim: Spirit and Anti should separate the same regimes in opposite directions.
- Why: Anti is the exact sign inversion of Spirit, so coherent and collapse-seeking behavior should split cleanly.
- Test: Compare balanced and entropy_heavy outputs for Spirit vs Anti under identical inputs.
- Failure: If the sign split disappears, the contrast-pair story weakens.
- Result: `spirit_balanced=3.00000000000000, anti_balanced=-3.00000000000000, spirit_entropy=-2.00000000000000, anti_entropy=2.00000000000000`
- Verdict: `PASS`

### P4 Collapse Threshold

- Claim: There should exist a resistance boundary where canonical v2 flips from positive to negative.
- Why: If resistance is truly load-bearing, enough of it should push the system across a qualitative boundary.
- Test: Solve LLC v2 = 0 for W under the shared balanced regime.
- Failure: If no root exists in the physical interval W in [0,1], the threshold claim weakens for this setup.
- Result: `roots_in_[0,1]=[0.566987298107781]`
- Verdict: `PASS`

### P5 Conserved Coherence Candidate (algebraic-invariant-only)

- Claim: The framework should eventually expose a symmetry-backed conserved composite quantity.
- Why: If the action structure is real, Noether-style reasoning should identify an invariant or quasi-invariant composite. For now we only claim exact algebraic invariants under constrained transforms.
- Test: Check whether paired source/sink shifts cancel exactly and whether the action reduces to a repeated channel core plus net source-sink gap.
- Failure: If those exact symmetry residues fail, the Noether program loses its footing before dynamics even enter.
- Result: `current prerequisite core=8*(Fdot**2*chi_bar - V); paired_shift_delta_L=0; net_gap=-Gamma9 + chi10`
- Verdict: `PASS`

### P7 Wrong-Control Rejection

- Claim: Deliberately wrong variants should fail at least one of the basic behavioral checks that the canonical model passes.
- Why: If the canonical placement of source, sink, and resistance really matters, bad rewrites should break predictably.
- Test: Run the same regimes and W sweep across wrong-control variants and see whether they lose monotonic resistance loss, source/sink structure, or both.
- Failure: If wrong-control variants pass the same gauntlet cleanly, the canonical architecture is not carrying enough unique structure.
- Result: `canonical_curvature=16.0000000000000; rejected_controls=['gamma9_added', 'chi10_subtracted', 'resistance_ignored', 'source_sink_swapped']`
- Verdict: `PASS`

### P10 Grace-Leak Nonlinearity

- Claim: Resistance-like leakage should curve the loss profile rather than act like a simple straight-line penalty.
- Why: The canonical term uses (1-W)^2, so the response should be nonlinear even before later interpretation enters.
- Test: Measure the midpoint second difference across the canonical W sweep; a nonzero value marks curvature.
- Failure: If the midpoint second difference is zero, the curve is acting linearly under the sampled sweep.
- Result: `canonical_midpoint_second_difference=16.0000000000000`
- Verdict: `PASS`

## Wrong-Control Gauntlet

This section tests whether the canonical structure actually matters by running obviously wrong rewrites under the same bench.

### canonical_v2

- balanced: `14.4800000000000`
- resistance_drag: `-4.72000000000000`
- source_rich: `17.4800000000000`
- sink_heavy: `9.48000000000000`
- resistance penalty preserved: `True`
- source/sink asymmetry preserved: `True`
- source helps: `True`
- sink hurts: `True`
- monotonic W-loss: `True`
- midpoint second difference: `16.0000000000000`
- W sweep: W=0 -> 26.000000, W=1/10 -> 19.920000, W=1/5 -> 14.480000, W=3/10 -> 9.680000, W=2/5 -> 5.520000, W=1/2 -> 2.000000, W=3/5 -> -0.880000, W=7/10 -> -3.120000, W=4/5 -> -4.720000, W=9/10 -> -5.680000, W=1 -> -6.000000

### gamma9_added

- balanced: `16.4800000000000`
- resistance_drag: `-2.72000000000000`
- source_rich: `19.4800000000000`
- sink_heavy: `21.4800000000000`
- resistance penalty preserved: `True`
- source/sink asymmetry preserved: `True`
- source helps: `True`
- sink hurts: `False`
- monotonic W-loss: `True`
- midpoint second difference: `16.0000000000000`
- W sweep: W=0 -> 28.000000, W=1/10 -> 21.920000, W=1/5 -> 16.480000, W=3/10 -> 11.680000, W=2/5 -> 7.520000, W=1/2 -> 4.000000, W=3/5 -> 1.120000, W=7/10 -> -1.120000, W=4/5 -> -2.720000, W=9/10 -> -3.680000, W=1 -> -4.000000

### chi10_subtracted

- balanced: `8.48000000000000`
- resistance_drag: `-10.7200000000000`
- source_rich: `5.48000000000000`
- sink_heavy: `3.48000000000000`
- resistance penalty preserved: `True`
- source/sink asymmetry preserved: `True`
- source helps: `False`
- sink hurts: `True`
- monotonic W-loss: `True`
- midpoint second difference: `16.0000000000000`
- W sweep: W=0 -> 20.000000, W=1/10 -> 13.920000, W=1/5 -> 8.480000, W=3/10 -> 3.680000, W=2/5 -> -0.480000, W=1/2 -> -4.000000, W=3/5 -> -6.880000, W=7/10 -> -9.120000, W=4/5 -> -10.720000, W=9/10 -> -11.680000, W=1 -> -12.000000

### linear_resistance

- balanced: `19.6000000000000`
- resistance_drag: `0.400000000000000`
- source_rich: `22.6000000000000`
- sink_heavy: `14.6000000000000`
- resistance penalty preserved: `True`
- source/sink asymmetry preserved: `True`
- source helps: `True`
- sink hurts: `True`
- monotonic W-loss: `True`
- midpoint second difference: `0`
- W sweep: W=0 -> 26.000000, W=1/10 -> 22.800000, W=1/5 -> 19.600000, W=3/10 -> 16.400000, W=2/5 -> 13.200000, W=1/2 -> 10.000000, W=3/5 -> 6.800000, W=7/10 -> 3.600000, W=4/5 -> 0.400000, W=9/10 -> -2.800000, W=1 -> -6.000000

### resistance_ignored

- balanced: `26.0000000000000`
- resistance_drag: `26.0000000000000`
- source_rich: `29.0000000000000`
- sink_heavy: `21.0000000000000`
- resistance penalty preserved: `False`
- source/sink asymmetry preserved: `True`
- source helps: `True`
- sink hurts: `True`
- monotonic W-loss: `True`
- midpoint second difference: `0`
- W sweep: W=0 -> 26.000000, W=1/10 -> 26.000000, W=1/5 -> 26.000000, W=3/10 -> 26.000000, W=2/5 -> 26.000000, W=1/2 -> 26.000000, W=3/5 -> 26.000000, W=7/10 -> 26.000000, W=4/5 -> 26.000000, W=9/10 -> 26.000000, W=1 -> 26.000000

### source_sink_swapped

- balanced: `10.4800000000000`
- resistance_drag: `-8.72000000000000`
- source_rich: `7.48000000000000`
- sink_heavy: `15.4800000000000`
- resistance penalty preserved: `True`
- source/sink asymmetry preserved: `True`
- source helps: `False`
- sink hurts: `False`
- monotonic W-loss: `True`
- midpoint second difference: `16.0000000000000`
- W sweep: W=0 -> 22.000000, W=1/10 -> 15.920000, W=1/5 -> 10.480000, W=3/10 -> 5.680000, W=2/5 -> 1.520000, W=1/2 -> -2.000000, W=3/5 -> -4.880000, W=7/10 -> -7.120000, W=4/5 -> -8.720000, W=9/10 -> -9.680000, W=1 -> -10.000000

### all_additive

- balanced: `39.1200000000000`
- resistance_drag: `34.3200000000000`
- source_rich: `42.1200000000000`
- sink_heavy: `34.1200000000000`
- resistance penalty preserved: `True`
- source/sink asymmetry preserved: `True`
- source helps: `True`
- sink hurts: `True`
- monotonic W-loss: `True`
- midpoint second difference: `4.00000000000000`
- W sweep: W=0 -> 42.000000, W=1/10 -> 40.480000, W=1/5 -> 39.120000, W=3/10 -> 37.920000, W=2/5 -> 36.880000, W=1/2 -> 36.000000, W=3/5 -> 35.280000, W=7/10 -> 34.720000, W=4/5 -> 34.320000, W=9/10 -> 34.080000, W=1 -> 34.000000

Rejected controls:

- `gamma9_added`
- `chi10_subtracted`
- `resistance_ignored`
- `source_sink_swapped`

## Invariant Search

These are algebraic invariants or symmetry residues under constrained transformations. They are not yet claimed as full Noether conserved quantities.

### paired_source_sink_shift

- Transform: `chi10 -> chi10 + delta, Gamma9 -> Gamma9 + delta`
- Description: n/a
- Result: `0`
- Verdict: `PASS`

### source_gap_generator

- Description: If dL/dchi10 + dL/dGamma9 = 0, equal source/sink shifts cancel exactly.
- Result: `0`
- Verdict: `PASS`

### net_source_sink_gap

- Description: The source/sink contribution enters only through chi10 - Gamma9.
- Result: `-Gamma9 + chi10`
- Verdict: `PASS`

### per_channel_core

- Description: The channel stack separates into repeated copies of one shared channel core.
- Result: `Fdot**2*chi_bar*(W - 1)**2 - V`
- Verdict: `PASS`

### recovered_channel_sum

- Description: Removing the source-sink gap from the K-normalized action leaves the repeated channel stack.
- Result: `8*Fdot**2*chi_bar*(W - 1)**2 - 8*V`
- Verdict: `PASS`

## Variation Audit

This section is the direct answer to the entropy-coupling question.

### bare_spirit_varied_by_x

- Lagrangian: `-S(t)*chi(t) + chi(t)*Derivative(x(t), t)**2`
- Equation: `2*chi(t)*Derivative(x(t), (t, 2)) + 2*Derivative(chi(t), t)*Derivative(x(t), t)`
- Solved form: `-Derivative(chi(t), t)*Derivative(x(t), t)/chi(t)`
- Entropy enters directly: `False`

### entropy_coupled_spirit_varied_by_x

- Lagrangian: `-S(t)*chi(t)*x(t) + chi(t)*Derivative(x(t), t)**2`
- Equation: `S(t)*chi(t) + 2*chi(t)*Derivative(x(t), (t, 2)) + 2*Derivative(chi(t), t)*Derivative(x(t), t)`
- Solved form: `-S(t)/2 - Derivative(chi(t), t)*Derivative(x(t), t)/chi(t)`
- Entropy enters directly: `True`

### chi_as_dynamical_field

- Lagrangian: `-S(t)*chi(t) + Derivative(chi(t), t)**2/2`
- Equation: `S(t) + Derivative(chi(t), (t, 2))`
- Solved form: `-S(t)`
- Entropy enters directly: `True`

### rayleigh_extension_on_bare_spirit

- Lagrangian: `-S(t)*chi(t) + chi(t)*Derivative(x(t), t)**2`
- Rayleigh term: `gamma*Derivative(x(t), t)**2/2`
- Equation: `gamma*Derivative(x(t), t) + 2*chi(t)*Derivative(x(t), (t, 2)) + 2*Derivative(chi(t), t)*Derivative(x(t), t)`
- Solved form: `(-gamma - 2*Derivative(chi(t), t))*Derivative(x(t), t)/(2*chi(t))`
- Entropy enters directly: `False`

## Read This Like A Normal Person

- If a model cannot translate into SymPy cleanly, it is not ready.
- If terms being added together do not share the same dimension class, it is not ready.
- If the anti-model is not exactly the negative of the spirit model, the contrast claim is weak.
- If resistance `W` does not reduce the useful part of v2, the grace-leak story is weak.
- If `chi10` does not help and `Gamma9` does not hurt, the source/sink story is weak.
- If the Euler-Lagrange equation closes cleanly, the model is at least mechanically well-formed.
- If the Euler-Lagrange equation does **not** produce the theological relation you hoped for, that is still useful: it tells you what is not yet derived.
- If predictions are written before tuning and stored with the report, the process becomes much harder to contest later.
