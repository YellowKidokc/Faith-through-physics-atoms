# Formal Specification

This document states the public-facing mathematical contract for the current Master Equation formalization.

It is intentionally conservative. Anything not encoded in Lean is marked as interpretation, assumption, or test-layer behavior.

## 1. Factor Architecture

The local product layer has ten named slots:

```text
G, M, E, S_eff, T, K, R, Q, F, C
```

where:

- `G` is the generative / source factor.
- `M` is the alignment factor.
- `E` is the embodiment / expression factor.
- `S_eff` is entropy attenuation, not raw entropy production.
- `T` is temporal fidelity.
- `K` is covenant / constraint fidelity.
- `R` is a binary renewal gate.
- `Q` is quality / wisdom / discernment.
- `F` is faith / active trust.
- `C` is coherence / justice-mercy / canonical constraint.

The local output is:

```text
chi_local = G * M * E * S_eff(S_prod) * T * K * R * Q * F * C
```

`chi_local` is an output, not an additional factor.

## 2. Entropy Attenuation

Raw entropy production is not multiplied directly into coherence. Instead, it enters through a positive attenuation function:

```text
S_eff(S_prod) > 0
```

and when entropy production increases, effective coherence contribution does not increase:

```text
S_prod_1 <= S_prod_2  =>  S_eff(S_prod_2) <= S_eff(S_prod_1)
```

The concrete narrow test uses:

```text
S_eff(S_prod) = exp(-eta * S_prod)
```

with:

```text
eta > 0
S_prod >= 0
```

## 3. Product Collapse

The core product theorem is:

```text
product(xs) = 0  iff  at least one required factor is 0
```

For the local product:

```text
R = 0 => chi_local = 0
```

and any zero multiplicative factor collapses the product.

## 4. Raw Alignment Versus Effective Alignment

Two versions are tracked.

Version A:

```text
M in [-1, 1]
chi_local = G * M * E * S_eff * T * K * R * Q * F * C
```

This is expressive but sign-unstable. Lean proves counterexamples where negative `M` makes positivity and monotonicity claims fail.

Version B:

```text
M_eff = (1 + M) / 2
M in [-1, 1]
M_eff in [0, 1]
chi_local = G * M_eff * E * S_eff * T * K * R * Q * F * C
```

This is the recommended canonical product layer because it preserves the expected nonnegative-factor interpretation.

## 5. Grace Operator

Grace is formalized as a regime-level reset:

```text
grace(constructive) = constructive
grace(destructive) = constructive
```

Lean proves:

```text
grace(grace(r)) = grace(r)
```

and:

```text
grace is not invertible as a total regime map
```

This is a structural claim about the operator. The theological meaning is interpretation layered on top of the formal model.

## 6. Justice-Mercy / Coherence Operator

A zero-preserving coherence operator `C_op` satisfies:

```text
C_op(0) = 0
```

Lean proves that such an internal operator cannot rescue an already-zero product.

This keeps the model honest: if grace is meant to reset a destructive regime, it is not smuggled in as ordinary multiplication inside the collapsed product.

## 7. Physical-Spiritual Correspondence

The repo does not assume that two law models are isomorphic.

A valid isomorphism must provide:

```text
toFun
invFun
left_inverse
right_inverse
preserves_value
preserves_collapse
```

So the canonical claim is not:

```text
these two domains are automatically the same
```

but:

```text
if you claim equivalence, here is the formal proof obligation
```

## 8. Lagrangian Status

The canonical Lagrangian should be treated as a model specification until its assumptions, fields, symmetries, variation principle, and derived equations are encoded.

The current repo can safely publish:

```text
formal product architecture
entropy attenuation behavior
operator/reset structure
proof obligations for isomorphism
Python numerical mirrors
```

It should not yet claim:

```text
Lean has proven the full physical Lagrangian
Lean has proven a Noether theorem for commandments
Lean has proven empirical truth
```
