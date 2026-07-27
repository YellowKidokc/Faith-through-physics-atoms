# Lean 4 Theorem Count Canon

Date: 2026-07-01

## Safe current readout

The old public-facing number `319` should not be treated as canonical.

The cleaner audited numbers are:

- `305` theorem declarations in the prior root package before the new negative inventory module
- `~330` theorem declarations after adding `Theophysics_NegativeInventory.lean`

## What changed

A new module, `Theophysics_NegativeInventory.lean`, was added to the package and compiled clean with the rest of the Lean corpus.

That module adds a first major tranche of the negative-chain families, including:

- per-factor insufficiency
- dependency-lattice rejection
- sign/conversion rejection
- resurrection false-positive rejection

This means the package is no longer just a positive-formalization stack. It now contains a more serious severe-testing layer.

## What is safe to say right now

The safest current wording is:

> The prior audited root package contained 305 theorem declarations, and the current package is now at roughly 330 after the addition of the negative-inventory module. A final canonical recount should still be run before any public-facing fixed number is used.

## What should not be said

Do not keep using `319` as though it is settled unless the source of that number is reconciled and re-counted.

## Why this matters

The whole point of this framework is that it invites inspection. If the theorem count is stated publicly, it should be a number that survives a direct reviewer count.

## Next cleanup step

Before Templeton or any formal public packet:

1. Run one final theorem-declaration recount across the exact package boundary being claimed.
2. Freeze the counting rule.
3. Record the final number in one canonical ledger only.

## FROZEN RECOUNT — 2026-07-01 (this is the canonical number)

**Counting rule (frozen):** lines matching `^\s*(theorem|lemma)\s+<identifier>` in the
root-level `.lean` files of `D:\GitHub\Faith-Thru-Physics-Lean-4-` (the compiled package),
excluding `lakefile.lean`, the `EVIDENCE\` copies, and all subfolder duplicates.

| File | Theorems |
|---|---|
| Final_Lean4_From_Excel.lean | 38 |
| Theophysics_Adversarial.lean | 78 |
| Theophysics_ChiEvaluator.lean | 23 |
| Theophysics_Coherence.lean | 13 |
| Theophysics_Core.lean | 132 |
| Theophysics_Fall.lean | 11 |
| Theophysics_Fracture.lean | 10 |
| Theophysics_NegativeInventory.lean | 21 |
| **TOTAL (root package)** | **326** |

Whole package builds with exit 0, zero sorry, zero axiom declarations.

**Separate count, separate claim:** `D:\GitHub\theophysics-lean\Theophysics_Canonization.lean`
(the Mathlib-based canonization module) compiled clean on 2026-07-01 — 35 theorems, zero
sorry, zero axioms. If cited together with the root package, say "326 + 35 across two
packages", never a single merged number, because they are different toolchain targets
(Std-only vs Mathlib).

**Public-facing wording:** "326 machine-checked theorems in the core package, zero
unresolved proofs" — retire 319 and 305 everywhere.

