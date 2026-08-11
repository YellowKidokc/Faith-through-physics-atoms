namespace Theophysics

/-!
# Totalized Negation Kernel

This file formalizes the abstract persistence-limit schema:

> Any operation that requires an enabling good, then destroys the support it
> requires without adequate regeneration or substitution, cannot remain
> indefinitely operational.

The theorem is intentionally conditional. Lean checks the dependency shape; it
does not prove that logic, politics, or physics automatically satisfy the
domain premises. Those premises are exposed through `TotalizationBundle`.

This kernel proves a persistence limit, not guaranteed historical victory.
-/

namespace TotalizedNegationKernel

universe u v

structure NegationWorld where
  Operation : Type u
  Good : Type v
  Requires : Operation -> Good -> Prop
  Negates : Operation -> Good -> Prop
  ReachesSupport : Operation -> Good -> Prop
  Available : Good -> Prop
  Regenerated : Good -> Prop
  Substituted : Good -> Prop

def EffectiveSupport (W : NegationWorld) (g : W.Good) : Prop :=
  W.Available g \/ W.Regenerated g \/ W.Substituted g

def IndefinitelyOperational (W : NegationWorld) (a : W.Operation) : Prop :=
  forall g : W.Good, W.Requires a g -> EffectiveSupport W g

structure TotalizationBundle (W : NegationWorld) where
  support_eliminated_without_replacement :
    forall a g,
      W.Negates a g ->
      W.ReachesSupport a g ->
      Not (W.Regenerated g) ->
      Not (W.Substituted g) ->
      Not (W.Available g)

theorem totalized_negation_uninhabitable
    (W : NegationWorld)
    (B : TotalizationBundle W)
    (a : W.Operation)
    (g : W.Good)
    (hReq : W.Requires a g)
    (hNeg : W.Negates a g)
    (hReach : W.ReachesSupport a g)
    (hNoRegen : Not (W.Regenerated g))
    (hNoSub : Not (W.Substituted g)) :
    Not (IndefinitelyOperational W a) := by
  intro hSustain
  have hSupport : EffectiveSupport W g := hSustain g hReq
  have hNoAvail : Not (W.Available g) :=
    B.support_eliminated_without_replacement
      a g hNeg hReach hNoRegen hNoSub
  cases hSupport with
  | inl hAvail =>
      exact hNoAvail hAvail
  | inr hOther =>
      cases hOther with
      | inl hRegen =>
          exact hNoRegen hRegen
      | inr hSub =>
          exact hNoSub hSub

/-! ## Premise controls -/

inductive OneOp where
  | op
deriving DecidableEq, Repr

inductive OneGood where
  | good
deriving DecidableEq, Repr

def regeneratedWorld : NegationWorld where
  Operation := OneOp
  Good := OneGood
  Requires := fun _ _ => True
  Negates := fun _ _ => True
  ReachesSupport := fun _ _ => True
  Available := fun _ => False
  Regenerated := fun _ => True
  Substituted := fun _ => False

theorem regeneration_allows_effective_support :
    EffectiveSupport regeneratedWorld OneGood.good := by
  exact Or.inr (Or.inl trivial)

theorem regenerated_operation_can_be_indefinitely_operational :
    IndefinitelyOperational regeneratedWorld OneOp.op := by
  intro _g _hReq
  exact Or.inr (Or.inl trivial)

def selectiveNegationWorld : NegationWorld where
  Operation := OneOp
  Good := OneGood
  Requires := fun _ _ => True
  Negates := fun _ _ => True
  ReachesSupport := fun _ _ => False
  Available := fun _ => True
  Regenerated := fun _ => False
  Substituted := fun _ => False

theorem selective_negation_can_remain_operational :
    IndefinitelyOperational selectiveNegationWorld OneOp.op := by
  intro _g _hReq
  exact Or.inl trivial

def noRequirementWorld : NegationWorld where
  Operation := OneOp
  Good := OneGood
  Requires := fun _ _ => False
  Negates := fun _ _ => True
  ReachesSupport := fun _ _ => True
  Available := fun _ => False
  Regenerated := fun _ => False
  Substituted := fun _ => False

theorem no_requirement_world_is_vacuously_operational :
    IndefinitelyOperational noRequirementWorld OneOp.op := by
  intro g hReq
  cases hReq

def totalizedCollapseWorld : NegationWorld where
  Operation := OneOp
  Good := OneGood
  Requires := fun _ _ => True
  Negates := fun _ _ => True
  ReachesSupport := fun _ _ => True
  Available := fun _ => False
  Regenerated := fun _ => False
  Substituted := fun _ => False

def totalizedCollapseBundle : TotalizationBundle totalizedCollapseWorld where
  support_eliminated_without_replacement := by
    intro _a _g _hNeg _hReach _hNoRegen _hNoSub
    intro hAvail
    exact hAvail

theorem totalized_collapse_world_not_operational :
    Not (IndefinitelyOperational totalizedCollapseWorld OneOp.op) := by
  exact totalized_negation_uninhabitable
    totalizedCollapseWorld
    totalizedCollapseBundle
    OneOp.op
    OneGood.good
    trivial
    trivial
    trivial
    (by intro h; exact h)
    (by intro h; exact h)

end TotalizedNegationKernel

end Theophysics
