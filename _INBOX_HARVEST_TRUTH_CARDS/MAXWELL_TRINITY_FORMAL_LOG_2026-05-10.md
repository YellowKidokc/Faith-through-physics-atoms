# Maxwell / Trinity Lean 4 Formal Log

POF 2828 + Codex  
Date: 2026-05-10  
Status: first rejection-first Lean pass completed

## File Added

- `ResurrectionFormal/MaxwellTrinity.lean`
- Imported from `ResurrectionFormal.lean`

## Build Result

Command:

```text
lake build
```

Final result:

```text
Build completed successfully (9 jobs).
```

## What Was Formalized

The file defines a small structural gate called `ValidTriadic`.

A system passes only if it has:

1. canonical source / mediator / actualizer role profiles;
2. a scalar-vector coupling invariant derived from full quaternion
   multiplication;
3. a full dynamic-field marker;
4. relational distinctness;
5. mutual necessity.

This intentionally tests the proposed Maxwell/Trinity structure as a
triadic relational architecture, not as a full historical or physical proof of
Maxwell's quaternion equations.

## Rejection-First Tests

The following controls are proven invalid:

1. `heavisideVectorEM_invalid`
   - Heaviside/vector EM fails because vector-only dot/cross data lacks the
     scalar-vector coupling invariant required by full quaternion
     multiplication.

2. `modalism_invalid`
   - Modalism fails because relational distinctness is false.

3. `staticSingleFieldEM_invalid`
   - A static/single-field EM case fails because it is not the full dynamic
     field structure.

4. `arbitraryThreePartSystem_invalid`
   - An arbitrary three-part system fails because it lacks canonical role
     profiles.

5. `relabeledRoleSystem_invalid`
   - Semantic relabeling fails because role labels alone do not supply the
     required profiles.

## Positive Test

After the controls, Lean accepts:

- `quaternionEM_valid`
- `trinityRelational_valid`
- `quaternionTrinityIso`

This proves that the two encoded candidate systems satisfy the same triadic
gate and admit a role-preserving isomorphism under the current specification.

## Wrong-Role Control

Lean also proves that a cyclic role swap fails:

- `cyclicRoleMap_not_source_preserving`
- `cyclicRoleMap_not_profile_preserving`

This blocks the simple semantic game where the same three labels are rotated
into the wrong structural positions.

## Load-Bearing Constraint Audit

The following theorems show which guards are doing real work:

1. `heaviside_passes_if_coupling_guard_removed`
   - If the scalar-vector coupling guard is removed, Heaviside passes.

2. `modalism_passes_if_distinctness_guard_removed`
   - If relational distinctness is removed, modalism passes.

3. `static_single_field_passes_if_dynamic_guard_removed`
   - If the dynamic-field guard is removed, the static case passes.

4. `relabeled_roles_pass_if_profile_guard_removed`
   - If role profiles are removed, relabeling passes.

5. `arbitrary_three_part_passes_bare_gate`
   - If the gate is reduced to "has three parts," arbitrary systems pass.

This is the strongest part of the current pass. It shows the controls are not
decorative; the failure conditions are load-bearing.

## Quaternion Algebra Sanity Check

A small Hamilton-quaternion structure was added as a guardrail around the phrase
"non-decomposable."

Lean proves:

1. `full_scalar_vector_split_reconstructs_quaternion_product`
   - If the full scalar/vector split data is retained, the quaternion product
     can be reconstructed exactly.

2. `vector_only_data_does_not_determine_full_product`
   - If only vector-side data is retained, two quaternions with the same vector
     part but different scalar parts can produce different products.

3. `same_vector_only_data_for_different_scalar_inputs`
   - Two different scalar inputs can produce identical vector-only dot/cross
     data.

4. `scalar_vector_coupling_differs_for_same_vector_only_data`
   - Those same inputs differ in scalar-vector coupling.

5. `same_dot_cross_but_different_quaternion_product`
   - Lean verifies the combined adversarial result: identical vector dot/cross
     data, different full quaternion product.

6. `vector_only_dot_cross_not_enough_for_quaternion_product`
   - There exists a concrete counterexample showing vector-only dot/cross data
     does not determine the full quaternion product.

This matters because the strongest honest version is not:

```text
The quaternion product cannot be decomposed in any sense.
```

The stronger and more precise version is:

```text
The full quaternion product requires scalar-vector coupling data. A vector-only
or over-separated reading can lose that coupling.
```

That target is now directly formalized inside the `ValidTriadic` structure.
The old abstract `ProductInvariant.unified` marker has been replaced by the
proposition-valued field `couplingInvariant`.

## Mistake Log

First build failed because `TriadicSystem` derived `Repr` even though it
contains a function field:

```text
failed to synthesize instance of type class
Repr (TriadicRole -> OperationProfile)
```

Fix:

- removed `deriving Repr` from `TriadicSystem`;
- rebuild succeeded.

No proof failures occurred after that correction.

## Honest Boundary

What Lean proved:

```text
Given these structural definitions, the intended quaternion/Trinity candidates
pass the triadic gate, while the five adversarial controls fail.
```

What Lean did not prove:

```text
Maxwell's historical quaternion equations really instantiate this abstraction.
```

```text
The quaternion product is mathematically non-decomposable in every sense.
```

```text
The theological interpretation is uniquely forced by the formal structure.
```

Those are specification-review questions. The current pass now encodes the
quaternion theorem directly into the triadic validity gate instead of using the
marker `ProductInvariant.unified`.

## Current Assessment

This is substantially stronger than the Law 4 two-state test because the false
positive controls are explicit and because each rejected case fails for a
specific stated invariant.

But it is not yet the final proof to send as a headline claim. It is the first
clean formal gate plus a real scalar-vector coupling theorem. Heaviside now
fails because vector-only separated operations cannot preserve the formalized
coupling invariant, not because it is tagged as decomposed.
