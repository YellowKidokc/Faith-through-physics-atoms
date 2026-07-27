# Proof Walkthrough

This walkthrough explains what the proof package is doing in plain language.

It is written for readers who may not know Lean yet but want to understand exactly where the claims are checked.

## 1. The Core Product Claim

File:

```text
TheophysicsProductionKernel.lean
```

The core theorem is:

```lean
theorem listProd_eq_zero_iff (xs : List α) :
    listProd xs = A.zero ↔ A.zero ∈ xs
```

Plain English:

```text
A finite product is zero exactly when at least one factor is zero.
```

This is the formal backbone of the collapse claim. It does not depend on numerical examples, floating point arithmetic, or hand-picked data.

## 2. The No-Rescue Operator Claim

File:

```text
TheophysicsProductionKernel.lean
```

The operator structure is:

```lean
structure CoherenceOperator (α : Type u) [A : CoherenceAlgebra α] where
  apply : α → α
  preserves_zero : apply A.zero = A.zero
```

Plain English:

```text
If an internal coherence operator preserves zero, it cannot turn a collapsed product back into coherence.
```

The Lean theorem:

```lean
theorem zero_if_any_factor_zero ...
```

says that once the product is zero, applying a zero-preserving operator still gives zero.

This matters because it keeps grace from being hidden inside ordinary multiplication. Grace is modeled separately as a regime reset.

## 3. Grace As Reset

File:

```text
TheophysicsProductionKernel.lean
```

Grace is encoded as:

```lean
def grace : Regime → Regime
  | Regime.constructive => Regime.constructive
  | Regime.destructive  => Regime.constructive
```

Lean proves:

```lean
theorem grace_idempotent
```

Plain English:

```text
Applying grace once or twice has the same result.
```

Lean also proves:

```lean
theorem grace_not_invertible
```

Plain English:

```text
Grace cannot be reversed into the original destructive/constructive history by a total inverse function.
```

## 4. The Isomorphism Burden

File:

```text
TheophysicsProductionKernel.lean
```

The structure:

```lean
structure LawIso ...
```

requires:

```text
map forward
map backward
left inverse
right inverse
value preservation
collapse preservation
```

Plain English:

```text
If someone claims a physical law model and a spiritual law model are structurally equivalent, they have to provide the maps and prove preservation. The repo does not assume that equivalence for free.
```

This is important for credibility. It makes the claim falsifiable and checkable.

## 5. Corrected Entropy

File:

```text
CorrectedEntropyKernel.lean
```

The corrected local product uses:

```text
S_eff(S_prod)
```

instead of multiplying raw entropy production directly.

Lean tracks the required behavior:

```text
S_eff is positive
S_eff decreases as S_prod increases
R = false collapses local chi
zero in a required factor collapses local chi
positive factors yield positive local chi
```

This is the formal reason to say:

```text
entropy enters through attenuation, not as raw entropy multiplication
```

## 6. Narrow Product Test

File:

```text
narrow_product_test/NarrowProductTest/Basic.lean
```

This is the Mathlib-backed concrete test using:

```text
S_eff = exp(-eta * S_prod)
```

It compares two alignment models.

Version A:

```text
M in [-1, 1]
chi_local = G * M * E * S_eff * T * K * R * Q * F * C
```

Lean proves this can become sign-unstable when `M < 0`.

Version B:

```text
M_eff = (1 + M) / 2
chi_local = G * M_eff * E * S_eff * T * K * R * Q * F * C
```

Lean proves this version behaves cleanly under the expected nonnegative-factor assumptions.

## 7. What The Repo Can Honestly Claim

Safe public claim:

```text
The repository formally verifies structural properties of the Master Equation product architecture in Lean 4, with Python and Colab mirrors for numerical exploration.
```

Do not claim yet:

```text
Lean has proven the full physical Lagrangian.
Lean has proven empirical truth.
Lean has proven all spiritual interpretations.
```

The package is stronger because it is honest about that boundary.
