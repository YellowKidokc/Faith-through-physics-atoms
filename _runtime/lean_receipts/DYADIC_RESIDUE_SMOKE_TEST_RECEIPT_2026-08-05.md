# Dyadic Residue Smoke Test Receipt

Date: 2026-08-05

Lean project:

`H:\lean_smoke_lake`

File added:

`H:\lean_smoke_lake\LeanSmokeLake\DyadicResidue.lean`

Root import updated:

`H:\lean_smoke_lake\LeanSmokeLake.lean`

Build command:

```powershell
lake build
```

Build result:

```text
Build completed successfully (14 jobs).
```

## Theorem

```lean
theorem dyadic_residue_smoke_test :
    (∃ case0 : SharedBlindSpot,
      dyadicAgrees case0.mia case0.kai
      ∧ ¬ correct case0.truth case0.mia
      ∧ ¬ correct case0.truth case0.kai)
    ∧
    (∃ case0 : SharedBlindSpot, ∃ vessel : Report,
      thirdExposesResidue case0 vessel)
```

## Model

```lean
structure Report where
  value : Bool
```

```lean
def dyadicAgrees (a b : Report) : Prop :=
  a.value = b.value
```

```lean
def correct (truth : Bool) (r : Report) : Prop :=
  r.value = truth
```

```lean
structure SharedBlindSpot where
  truth : Bool
  mia : Report
  kai : Report
  mia_kai_agree : dyadicAgrees mia kai
  mia_wrong : ¬ correct truth mia
  kai_wrong : ¬ correct truth kai
```

```lean
def thirdExposesResidue (case0 : SharedBlindSpot) (vessel : Report) : Prop :=
  correct case0.truth vessel
  ∧ vessel.value ≠ case0.mia.value
  ∧ vessel.value ≠ case0.kai.value
```

## What Was Proved

Lean verified that there exists a shared-blindspot case where:

- Mia and Kai agree with each other;
- Mia and Kai are both wrong relative to the underlying fact;
- an independent third report can expose that residue by matching truth and disagreeing with both reports.

Plain English:

> Agreement is not the same as truth when both observers share the same systematic error.

## What This Improves

This is stronger than the cardinality-only smoke tests because it models an actual dyadic failure pattern:

> both members of the dyad agree on the same false reading.

This maps cleanly to the narrative rule:

> VESSEL should not editorialize; it should log numbers that do not fit Mia and Kai's shared wrong story.

## What This Still Does Not Prove

This does not prove God.

This does not prove the Trinity.

This does not prove that every dyad fails.

This does not prove that dyads cannot reach common knowledge.

This does not prove a general measurement-problem theorem.

It proves an existential counterexample to the idea that dyadic agreement always certifies truth.

## Safe Wording

> Lean verifies a shared-blindspot model: two observers can agree with each other while both are wrong, and a third independent report can expose the residue.

## Unsafe Wording

> Lean proves dyads cannot close.

> Lean proves every measurement requires a third observer.

> Lean proves the Trinity from the measurement problem.

## Next Real Formal Target

A true upgrade would require a Kripke-style or fixed-point verification-chain model:

- agents;
- accessibility/knowledge relation;
- reports;
- ground truth;
- common knowledge;
- residue predicate;
- closure predicate;
- theorem showing a specific class of dyadic systems cannot certify a specific residue while a triadic system can.

That remains a real research project.
