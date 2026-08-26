namespace Theophysics

/--
`World` is the typed domain of discourse for the first no-smuggling Lean pass.

It intentionally says very little: there are agents, actions, and states, plus
predicates for coherence, degradation, preservation, restoration, and alignment.
The theological identifications stay outside this proof kernel.
-/
structure World where
  Agent : Type
  Action : Type
  State : Type
  acts : Agent -> Action -> Prop
  coherent : State -> Prop
  degraded : State -> Prop
  preserves : Action -> State -> Prop
  degrades : Action -> State -> Prop
  restores : Action -> State -> Prop
  alignedWithGood : Action -> Prop
  alignedWithDestruction : Action -> Prop

/--
The visible attack surface for the first formal chain.

Downstream theorem files should accept an `AxiomBundle W` instead of declaring
fresh hidden assumptions.
-/
structure AxiomBundle (W : World) where
  destructive_degrades :
    forall a s, W.alignedWithDestruction a -> W.degrades a s
  good_preserves :
    forall a s, W.alignedWithGood a -> W.preserves a s
  degraded_unrestored_not_good :
    forall a s, W.degrades a s -> Not (W.restores a s) -> Not (W.alignedWithGood a)

/--
If an action is structurally destructive and no restoration is present, then it
cannot be aligned with good under the explicit bundle assumptions.
-/
theorem destructive_unrestored_not_good
    (W : World) (A : AxiomBundle W) :
    forall a s,
      W.alignedWithDestruction a ->
      Not (W.restores a s) ->
      Not (W.alignedWithGood a) := by
  intro a s hDestructive hNotRestored hGood
  have hDegrades := A.destructive_degrades a s hDestructive
  exact A.degraded_unrestored_not_good a s hDegrades hNotRestored hGood

end Theophysics
