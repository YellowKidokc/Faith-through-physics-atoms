namespace Theophysics

/-!
# Truth Substrate Kernel

This file proves a narrow semantic dependency kernel.

It does not prove that Jesus is the truth, that a speaker is identical with
truth, or that any historical/theological identification claim is true.

It separates raw utterance from assertion:

* an `Utterance` is uninterpreted expression;
* an `Assertion` is an utterance carrying truth-apt content;
* a `Lie` is an assertion whose content does not hold in the substrate;
* a `Certificate` is a witness that an assertion's content holds.

The kernel proves that lies can exist inside a truth substrate, but cannot
certify themselves as true. It also proves that abolishing truth-aptness
abolishes assertion, not raw utterance.
-/

namespace TruthSubstrateKernel

universe u

structure World (P : Type u) where
  TruthApt : P -> Prop
  Holds : P -> Prop

structure Utterance (P : Type u) where
  raw : P

structure Assertion {P : Type u} (W : World P) where
  utterance : Utterance P
  truthApt : W.TruthApt utterance.raw

def Assertion.content {P : Type u} {W : World P} (a : Assertion W) : P :=
  a.utterance.raw

def TruthConditionsAvailable {P : Type u} (W : World P) : Prop :=
  exists p : P, W.TruthApt p

def Lie {P : Type u} (W : World P) (a : Assertion W) : Prop :=
  Not (W.Holds a.content)

structure Certificate {P : Type u} (W : World P) (a : Assertion W) where
  witness : W.Holds a.content

/-! ## Basic construction -/

theorem truthApt_content_yields_assertion
    {P : Type u}
    (W : World P)
    (p : P)
    (h : W.TruthApt p) :
    exists a : Assertion W, a.content = p := by
  refine ⟨{ utterance := { raw := p }, truthApt := h }, ?_⟩
  rfl

theorem truth_substrate_model_exists :
    exists W : World Bool, TruthConditionsAvailable W := by
  refine ⟨{ TruthApt := fun _ => True, Holds := fun b => b = true }, ?_⟩
  exact ⟨true, trivial⟩

theorem lie_hosting_model_exists :
    exists W : World Bool, exists a : Assertion W, Lie W a := by
  let W : World Bool :=
    { TruthApt := fun _ => True, Holds := fun b => b = true }
  let a : Assertion W := { utterance := { raw := false }, truthApt := trivial }
  refine ⟨W, a, ?_⟩
  intro h
  cases h

/-! ## Certification boundary -/

theorem certified_assertion_holds
    {P : Type u}
    (W : World P)
    (a : Assertion W)
    (c : Certificate W a) :
    W.Holds a.content :=
  c.witness

theorem lie_is_not_certifiable
    {P : Type u}
    (W : World P)
    (a : Assertion W)
    (hLie : Lie W a) :
    Not (exists _c : Certificate W a, True) := by
  intro h
  rcases h with ⟨c, _⟩
  exact hLie c.witness

theorem lie_requires_truth_conditions
    {P : Type u}
    (W : World P) :
    (exists a : Assertion W, Lie W a) ->
      TruthConditionsAvailable W := by
  intro h
  rcases h with ⟨a, _hLie⟩
  exact ⟨a.content, a.truthApt⟩

theorem no_truth_conditions_no_assertion
    {P : Type u}
    (W : World P)
    (hNoTruthApt : Not (TruthConditionsAvailable W)) :
    Not (exists _a : Assertion W, True) := by
  intro h
  rcases h with ⟨a, _⟩
  exact hNoTruthApt ⟨a.content, a.truthApt⟩

/-! ## Denial controls -/

inductive DenialClaim where
  | target
  | notTarget
deriving DecidableEq, Repr

def trueDenialWorld : World DenialClaim where
  TruthApt := fun _ => True
  Holds := fun p => p = DenialClaim.notTarget

def falseDenialWorld : World DenialClaim where
  TruthApt := fun _ => True
  Holds := fun p => p = DenialClaim.target

def denialAssertion (W : World DenialClaim)
    (h : W.TruthApt DenialClaim.notTarget) : Assertion W :=
  { utterance := { raw := DenialClaim.notTarget }, truthApt := h }

theorem true_denial_is_certifiable :
    exists a : Assertion trueDenialWorld, Certificate trueDenialWorld a := by
  let a : Assertion trueDenialWorld := denialAssertion trueDenialWorld trivial
  refine ⟨a, ?_⟩
  exact { witness := rfl }

theorem false_denial_is_a_lie :
    exists a : Assertion falseDenialWorld, Lie falseDenialWorld a := by
  let a : Assertion falseDenialWorld := denialAssertion falseDenialWorld trivial
  refine ⟨a, ?_⟩
  intro h
  contradiction

/-! ## Raw utterance control -/

def truthAptlessWorld : World Bool where
  TruthApt := fun _ => False
  Holds := fun _ => False

theorem truthAptless_world_has_raw_utterance :
    exists u : Utterance Bool, u.raw = true := by
  exact ⟨{ raw := true }, rfl⟩

theorem truthAptless_world_has_no_assertion :
    Not (exists _a : Assertion truthAptlessWorld, True) := by
  apply no_truth_conditions_no_assertion
  intro h
  rcases h with ⟨_p, hApt⟩
  exact hApt

end TruthSubstrateKernel

end Theophysics
