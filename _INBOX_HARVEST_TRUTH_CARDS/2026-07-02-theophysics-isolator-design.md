# Design Spec: Theophysics Isolator — Neutral Core + Adjudication Protocol

**Date:** 2026-07-02  
**Project:** `dharma-mirror-lean` (Lean 4)  
**Goal:** Add a neutral formal isolator proving that bounded endogenous restoration cannot reach perfect coherence under positive decay, and pair it with an adjudication protocol that assigns proof obligations to Christian, Buddhist, and materialist interpretations without presupposing any of them.

---

## 1. Purpose

The prior audit showed that:

- The abstract coherence skeleton is portable across Christian and Buddhist frameworks.
- A full 10-law structural isomorphism fails because the algebraic roles (especially the decay/source slots) do not align under locked theological labels.
- Existing empirical notebooks demonstrate compatibility with scalar-field/modified-gravity machinery but do not prove uniqueness.

The next step is a **constraint-based** test, not a curve-fit-based test. This design builds a neutral mathematical isolator in Lean 4 and a written protocol for how worldviews must engage it.

The central formal question:

> Can a coherence system with positive decay reach perfect coherence using only a bounded source that is a function of its own internal state?

The expected neutral answer: **No.** Perfect coherence requires an unbounded or external source contribution.

Theological interpretations are then layered on as **interpretation modules**, not as axioms of the core proof.

---

## 2. Deliverables

1. `Isolator.lean` — neutral core theorem module.
2. `ChristianInterpretation.lean` — optional interpretation placeholder.
3. `BuddhistInterpretation.lean` — optional interpretation placeholder.
4. `MaterialistInterpretation.lean` — optional interpretation placeholder.
5. `docs/isolator_protocol.md` — adjudication protocol.

Build command remains `lake build` from the existing project root.

---

## 3. Architecture

```text
dharma-mirror-lean/
├── lakefile.toml
├── DharmaMirror.lean              (existing abstract CoherenceSystem)
├── Isolator.lean                  (new — neutral RestorationFramework + theorems)
├── ChristianInterpretation.lean   (new — optional)
├── BuddhistInterpretation.lean    (new — optional)
├── MaterialistInterpretation.lean (new — optional)
└── docs/
    └── isolator_protocol.md       (new)
```

The neutral core must compile without importing any interpretation module. Interpretation modules may import the neutral core, not the reverse.

---

## 4. Neutral Core Definitions (`Isolator.lean`)

### 4.1 RestorationFramework

A structure extending the existing `CoherenceSystem` idea:

```lean
structure RestorationFramework where
  State    : Type          -- system state space
  c        : State → ℝ     -- coherence scalar, expected in [0, 1]
  sigma    : State → ℝ     -- source term
  delta    : State → ℝ     -- decay term
  omega    : State → ℝ     -- openness / coupling term
  deriv    : State → ℝ     -- dc/dt = omega * sigma * (1 - c) - delta * c
```

The dynamics are intentionally simple. They generalize the prior `rate` definition.

### 4.2 EndogenousSource

```lean
class EndogenousSource (F : RestorationFramework) where
  -- sigma is determined entirely by the system’s own state.
  -- No restriction on which state variables may enter.
  is_internal : ∃ (f : F.State → ℝ), ∀ s, F.sigma s = f s
```

This class is structurally trivial; its purpose is to classify the source conceptually. The isolator’s mathematical force comes from `BoundedEffectiveSource` paired with `PositiveDecay`.

### 4.3 BoundedEffectiveSource

Because the dynamics use the product `omega * sigma`, the relevant bound is on the effective source term:

```lean
def effective_source (F : RestorationFramework) (s : F.State) : ℝ :=
  F.omega s * F.sigma s

class BoundedEffectiveSource (F : RestorationFramework) where
  K_eff       : ℝ
  K_eff_nonneg : 0 ≤ K_eff
  bound       : ∀ s, effective_source F s ≤ K_eff
```

`K_eff` may depend on the framework instance but must be finite and independent of the state.

### 4.4 PositiveDecay

```lean
class PositiveDecay (F : RestorationFramework) where
  pos : ∀ s, 0 < F.delta s
```

### 4.5 ExogenousSource

```lean
class ExogenousSource (F : RestorationFramework) where
  -- The source includes a contribution not computable from the system state.
  -- It may be a constant, a function of external parameters, or an unbounded limit.
  contribution : ∀ s, F.sigma s = f_internal s + sigma_ext
```

The key property is that `sigma_ext` is not forced to zero by internal decay.

### 4.6 FaithIsCoupling

```lean
class FaithIsCoupling (F : RestorationFramework) where
  -- omega scales the rate at which source is received but does not itself add source.
  -- Formally: at fixed internal state aside from omega, sigma is constant in omega.
  no_source_from_faith : ∀ s s',  (state_except_omega s = state_except_omega s') → F.sigma s = F.sigma s'
```

The exact Lean encoding of `state_except_omega` will be resolved during implementation; the intent is an independence condition.

---

## 5. Theorems to Prove

### 5.1 Core Isolator (Bound Form)

```lean
theorem bounded_endogenous_equilibrium_bound
  (F : RestorationFramework)
  [EndogenousSource F]
  [BoundedEffectiveSource F]
  [PositiveDecay F]
  (s : F.State)
  (equilibrium : F.deriv s = 0)
  (omega_pos : 0 < F.omega s)
  (delta_min : ℝ)
  (delta_min_pos : 0 < delta_min)
  (delta_lower : delta_min ≤ F.delta s)
  (in_range : 0 ≤ F.c s ∧ F.c s ≤ 1)
  : F.c s ≤ K_eff / (K_eff + delta_min)
```

where `K_eff` is the bound from `BoundedEffectiveSource`.

**Proof sketch:** At equilibrium,

```text
omega * sigma * (1 - c) = delta * c
```

Let `lambda = omega * sigma`. Then:

```text
c = lambda / (lambda + delta)
  ≤ K_eff / (K_eff + delta_min)
```

The inequality uses `lambda ≤ K_eff`, `delta ≥ delta_min > 0`, and the fact that `x ↦ x / (x + d)` is increasing in `x` for `x ≥ 0` when `d > 0`.

Because `K_eff / (K_eff + delta_min) < 1`, the equilibrium coherence is bounded strictly away from 1.

### 5.2 Perfect-Coherence Impossibility Corollary

```lean
theorem bounded_endogenous_cannot_perfect
  (F : RestorationFramework)
  [EndogenousSource F]
  [BoundedEffectiveSource F]
  [PositiveDecay F]
  (s : F.State)
  (equilibrium : F.deriv s = 0)
  (omega_pos : 0 < F.omega s)
  (delta_min_pos : 0 < delta_min)
  (in_range : 0 ≤ F.c s ∧ F.c s ≤ 1)
  : F.c s < 1
```

This follows immediately from the bound theorem.

### 5.3 Unbounded / External Source Limit Theorem

```lean
theorem unbounded_source_perfect_attractor
  (F : RestorationFramework)
  [PositiveDecay F]
  : ∀ ε > 0, ∃ (Λ₀ : ℝ), ∀ Λ ≥ Λ₀,
    let F' := F with source := F.sigma + Λ in
    equilibrium_coherence F' > 1 - ε
```

This is a limit theorem, not a claim of finite-time reachability. It matches the prior result in `DharmaMirror.lean`.

### 5.4 Faith Is Coupling, Not Source

```lean
theorem faith_coupling_not_source
  (F : RestorationFramework)
  [EndogenousSource F]
  [BoundedEffectiveSource F]
  [PositiveDecay F]
  (s : F.State)
  (equilibrium : F.deriv s = 0)
  : increasing F.omega s cannot raise F.c s above the bound set by the effective source and decay
```

Formalized as: for a fixed effective source bound and decay, equilibrium coherence is monotonically increasing in `omega` but bounded above by `K_eff / (K_eff + delta_min)`.

---

## 6. Interpretation Placeholders

These modules are optional in the first implementation pass. They must import only the neutral core.

### 6.1 ChristianInterpretation.lean

Maps:

- `sigma` → grace (external, unbounded in the limit)
- `delta` → sin / entropy / decay
- `omega` → faith / openness
- `c` → coherence / communion

Proof obligation: show that grace is exogenous and non-coercive.

Non-coercive grace means the received contribution `omega * sigma → 0` as openness/faith `omega → 0`. The source `sigma` may remain available, but it is not coercively received by a closed system. This preserves the distinction: grace is the source, faith is the coupling.

### 6.2 BuddhistInterpretation.lean

Maps:

- `sigma` → wisdom / compassion / skillful means
- `delta` → craving / ignorance / attachment
- `omega` → meditative openness / insight
- `c` → liberation / awakening

Proof obligation: specify the strongest source model Buddhism adopts:

1. Bounded endogenous source
2. Unbounded endogenous source
3. Exogenous / nondual ground
4. Not representable by scalar coherence

Then prove what follows. If (1), the isolator theorem says perfect coherence is impossible. If (2) or (3), the model converges toward the Christian structure. If (4), the framework is incommensurable and the debate shifts to whether scalar coherence is the right measure.

### 6.3 MaterialistInterpretation.lean

Maps:

- `sigma` → self-organization / local entropy reduction / information processing
- `delta` → entropy / dissipation
- `omega` → coupling to available free energy
- `c` → organized complexity

Proof obligation: show that self-organization can sustain or increase coherence without an external source injection, or accept that local organization is always paid for by global dissipation.

---

## 7. Protocol Document (`docs/isolator_protocol.md`)

### 7.1 Plain-Language Statement of the Formal Result

Under positive decay, any coherence dynamics whose effective source `omega * sigma` is both (a) a function only of the system’s internal state and (b) bounded above by a finite constant `K_eff`, cannot reach perfect coherence. The equilibrium coherence is bounded strictly below 1.

Perfect coherence is only approachable in the limit if the source is unbounded or includes a contribution from outside the system state.

### 7.2 What Counts as Endogenous Restoration

A source is endogenous if:

- It is computable from the system’s own state variables.
- It does not invoke a term that persists independently when the internal state decays to zero.

Examples: self-organization, learning, practice, insight, internal information reconfiguration.

### 7.3 What Counts as Exogenous Restoration

A source is exogenous if:

- It includes a contribution not determined by the system state.
- It remains available even when the internal state would otherwise decay to incoherence.

Examples: external input, uncreated ground, infinite source, grace, nondual ground modeled as external to the finite self.

### 7.4 Adjudication Rules

1. **No relabeling without identifiability.** A worldview may not claim its source is exogenous merely by giving it a theological name. It must show that the source term in its model satisfies the formal exogeneity condition.
2. **Curve-fitting is not a proof obligation.** Demonstrating that a model fits data does not discharge the obligation to classify its source as endogenous or exogenous.
3. **Internal inconsistency is decisive.** If a worldview claims endogenous liberation and also claims perfect coherence, it must either bound its source and accept `c* < 1`, or admit an unbounded/external source and converge toward the exogenous-restoration class.
4. **Incommensurability is allowed but costly.** A worldview may reject the scalar coherence framework entirely, but then it cannot use the isolator’s conclusions and must defend its own measurement framework.

### 7.5 Worldview Proof Obligations

| Worldview | Obligation |
|-----------|-----------|
| Christian | Show that grace functions as an exogenous, non-coercive source. Show that faith is coupling, not production of grace. |
| Buddhist | Specify the source model: bounded endogenous, unbounded endogenous, exogenous/nondual, or non-scalar. Then prove the consequences. |
| Materialist | Show that self-organization can overcome positive decay without external source injection, or accept the bound. |

---

## 8. Testing and Verification

- `lake build` must succeed with all new files.
- Include at least two concrete examples in `Isolator.lean` or a companion test file:
  1. Linear bounded effective source: `omega(c) * sigma(c) = k_eff * c` with `k_eff < delta_min` ⇒ equilibrium `c* < 1`.
  2. Constant exogenous source: `sigma = Lambda` with `Lambda → ∞` ⇒ equilibrium `c* → 1`.
- Verify that the neutral core compiles independently of interpretation modules.
- Verify that interpretation modules compile only by importing the neutral core.

---

## 9. Risks and Limitations

1. **Triviality of `EndogenousSource`.** Because any `sigma : State → ℝ` is a function of state, the class is trivial unless paired with `BoundedEffectiveSource`. The presentation must make clear that the isolator’s force comes from bounded effective source + positive decay, not from the endogenous label alone.
2. **Defining boundedness carefully.** `K` must be finite and state-independent. Unbounded functions that grow with state can mimic exogenous behavior and must be classified separately.
3. **Avoiding question-begging.** The neutral core must not import theological language. Interpretation modules are the only place Christian/Buddhist/materialist terms appear.
4. **Scope of perfect coherence.** The theorem concerns scalar coherence in `[0, 1]`. Worldviews that reject this metric may sidestep the isolator; the protocol addresses this by requiring them to defend their alternative metric.

---

## 10. Success Criteria

- `Isolator.lean` compiles and contains the bound theorem, the impossibility corollary, the unbounded-source limit theorem, and the faith-is-coupling theorem.
- The protocol document is written and contains adjudication rules for all three worldviews.
- Interpretation placeholders exist and demonstrate how each worldview inherits its proof obligation.
- No theological axiom appears in the neutral core.

---

*Spec approved for implementation planning.*
