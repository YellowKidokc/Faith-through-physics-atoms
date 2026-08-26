# CoherenceAlgebra.lean

**Category:** LEAN4 Formal Proof — Foundation Layer  
**Location:** LEAN4/GOOD_LEAN/CoherenceAlgebra.lean  
**Role:** The algebraic bedrock. Everything else imports this.

---

## What It Is

CoherenceAlgebra.lean is the foundation of the entire formal proof system. It defines the abstract algebraic structure — `CoherenceAlgebra α` — that all other theorems are built on. If you want to understand why the Theophysics framework is formally rigorous, this is where you start.

It does three things:

1. **Defines the CoherenceAlgebra typeclass** — a commutative monoid with zero, a no-zero-divisors law, and the critical guarantee that zero ≠ one. This is the mathematical cage that makes the chi-product work.

2. **Proves the list product zero theorem** — if any single element in a list product equals zero, the entire product is zero. Fully proved. No `sorry`. This is the formal backbone of "one broken law kills the whole system."

3. **Defines the dual-layer structure** — each law is a `DualLaw` with a physical projection and a spiritual projection. The system product is computed across both simultaneously.

---

## Key Theorems

**`list_prod_zero_iff`** — the crown jewel of this file. It proves, completely and rigorously, that `listProd xs = zero ↔ ∃ x ∈ xs, x = zero`. Any zero anywhere kills everything. This is proved by structural induction over the list using `no_zero_divisors` and `mul_zero`. No sorry statements. Fully verified by Lean.

**`spiritual_restoration_is_external`** — if an internal operator maps zero to zero (sign conservation), it cannot be the thing that maps zero to one (restoration). The restoring operator must be external to the system's closure. This is the formal version of "you can't save yourself."

**`observation_required`** — an actualized state requires an observer. Stated as an axiom at the foundation level, which is honest: this is a framework commitment, not a deduction.

---

## The Critical Design Choice

The `zero_mul` axiom is defined as `mul zero a = a` rather than `mul zero a = zero`. This is intentional — it reflects the asymmetry between Grace (which can restore from zero) and ordinary multiplication (which propagates zero). The `mul_zero` direction (right multiply) gives `mul a zero = zero`, which is the veto property. This asymmetry is the formal signature of Law 1 (Grace) versus Law 9 (Sin).

---

## Why It Matters

Every other `.lean` file in the project — GraceOperator, MasterEquation, JusticeMercy, Thermodynamics, all of them — imports CoherenceAlgebra and inherits its guarantees. The `no_zero_divisors` property is what gives the zero-collapse theorems their teeth. The `zero_ne_one` axiom is what makes restoration meaningful: if zero and one were the same, grace would be a no-op.

This file is small (under 100 lines) and does exactly what a foundation layer should do: state the minimum axioms needed, prove the structural consequences, and get out of the way.
