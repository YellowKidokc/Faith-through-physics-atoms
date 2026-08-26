# CODEX CODE

Date: 2026-05-02

## Purpose

This package contains the Codex Lean 4 work for the narrow Master Equation
product test only.

It does not attempt to prove theology.
It proves formal product behavior.

## Main Deliverables

- `CorrectedEntropyKernel.lean`
  Standalone Lean kernel proving the abstract entropy-attenuation structure.

- `TheophysicsProductionKernel.lean`
  Existing production kernel preserved for comparison.

- `narrow_product_test/`
  Small Mathlib-backed Lean project for the concrete product test using
  `S_eff = exp(-η S_prod)`.

## Narrow Product Test

The Mathlib project tests two versions:

### Version A

Raw alignment factor:

`M ∈ [-1,1]`

Local product:

`χ_local = G * M * E * S_eff * T * K * R * Q * F * C`

Lean proves:

- `S_eff > 0`
- `S_eff ≤ 1` when `η > 0` and `S_prod ≥ 0`
- `S_eff` decreases as `S_prod` increases
- `R = 0 -> χ_local = 0`
- zero in any multiplicative factor except `S_eff` forces `χ_local = 0`
- `χ_local > 0` only with the added sign condition `M > 0`
- monotonicity in `G` and antitonicity in `S_prod` require `M ≥ 0`

It also includes explicit counterexamples showing what fails when `M < 0`.

### Version B

Effective alignment factor:

`M_eff = (1 + M) / 2`

Local product:

`χ_local = G * M_eff * E * S_eff * T * K * R * Q * F * C`

Lean proves the same structural facts more cleanly because every multiplicative
factor is nonnegative under the stated bounds.

## Key Lean File

- `narrow_product_test/NarrowProductTest/Basic.lean`

This is the main concrete proof file for the A/B comparison.

## Verification

These checks passed:

- `lake env lean NarrowProductTest/Basic.lean`
- `lake env lean NarrowProductTest.lean`

## Recommendation

Version B is the cleaner formalization target for the Master Equation product
layer because it removes the sign-instability caused by raw signed `M`.
