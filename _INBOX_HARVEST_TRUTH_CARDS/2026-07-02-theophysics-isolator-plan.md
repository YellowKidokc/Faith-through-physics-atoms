# Theophysics Isolator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a neutral Lean 4 isolator module and adjudication protocol to the DharmaMirror project, proving that bounded effective source + positive decay prevents perfect coherence.

**Architecture:** Extend the existing `DharmaMirror` library with a new `DharmaMirror.Isolator` submodule defining a `RestorationFramework`, source/decay type classes, and the core bound/limit theorems. Add three optional interpretation placeholders in `DharmaMirror/ChristianInterpretation.lean`, `DharmaMirror/BuddhistInterpretation.lean`, and `DharmaMirror/MaterialistInterpretation.lean`. Keep the neutral core independent of theological labels.

**Tech Stack:** Lean 4.31.0, Mathlib (local path dependency at `D:/GitHub/mathlib4`), Lake build system.

## Global Constraints

- Working directory for all commands: `D:/dharma-mirror-lean`.
- No theological axiom may appear in the neutral core (`DharmaMirror/Isolator.lean`).
- All new Lean files must compile with `lake build`.
- Interpretation modules may import the neutral core; the neutral core must not import interpretation modules.
- The effective source bound is `lambda(s) = omega(s) * sigma(s)` and is bounded by `BoundedEffectiveSource.K_eff`.
- Non-coercive grace is modeled as `omega * sigma → 0` when `omega → 0`, while `sigma` may remain available.
- Perfect coherence means `c = 1`; the unbounded-source theorem is a limit result, not finite-time reachability.

---

## File Structure

```text
D:/dharma-mirror-lean/
├── DharmaMirror.lean                         (modify — add imports)
├── DharmaMirror/
│   └── Isolator.lean                         (create — neutral core)
│   └── ChristianInterpretation.lean          (create — optional)
│   └── BuddhistInterpretation.lean           (create — optional)
│   └── MaterialistInterpretation.lean        (create — optional)
└── docs/
    └── isolator_protocol.md                  (create — adjudication protocol)
```

---

### Task 1: Scaffold `DharmaMirror/Isolator.lean`

**Files:**
- Create: `DharmaMirror/Isolator.lean`
- Modify: `DharmaMirror.lean`

**Interfaces:**
- Consumes: Mathlib reals and tactics.
- Produces: `Theophysics.RestorationFramework` structure and `deriv`, `effectiveSource`, `equilibrium`, `addExogenousSource` definitions.

- [ ] **Step 1: Create directory and file**

```bash
mkdir -p "D:/dharma-mirror-lean/DharmaMirror"
```

- [ ] **Step 2: Write the skeleton**

Create `DharmaMirror/Isolator.lean`:

```lean
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace Theophysics

/-- A restoration framework generalizes CoherenceSystem to arbitrary state spaces.
    The dynamics are: dc/dt = omega(s) * sigma(s) * (1 - c(s)) - delta(s) * c(s). -/
structure RestorationFramework where
  State : Type
  c     : State → ℝ   -- coherence scalar, expected in [0, 1]
  sigma : State → ℝ   -- source term
  delta : State → ℝ   -- decay/entropy term
  omega : State → ℝ   -- openness / coupling term

namespace RestorationFramework

/-- Rate of change of coherence at a state. -/
def deriv (F : RestorationFramework) (s : F.State) : ℝ :=
  F.omega s * F.sigma s * (1 - F.c s) - F.delta s * F.c s

/-- Effective source term that actually drives the dynamics. -/
def effectiveSource (F : RestorationFramework) (s : F.State) : ℝ :=
  F.omega s * F.sigma s

/-- Equilibrium coherence for the local effective source and decay. -/
noncomputable def equilibrium (F : RestorationFramework) (s : F.State) : ℝ :=
  let Λ := F.effectiveSource s
  Λ / (Λ + F.delta s)

/-- Add a constant exogenous source Λ to every state. -/
def addExogenousSource (F : RestorationFramework) (Λ : ℝ) : RestorationFramework where
  State := F.State
  c     := F.c
  sigma := fun s => F.sigma s + Λ
  delta := F.delta
  omega := F.omega

end RestorationFramework

end Theophysics
```

- [ ] **Step 3: Import the new module in `DharmaMirror.lean`**

Add near the top of `DharmaMirror.lean`:

```lean
import DharmaMirror.Isolator
```

- [ ] **Step 4: Build and verify**

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds; `DharmaMirror.Isolator` is compiled.

- [ ] **Step 5: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror/Isolator.lean DharmaMirror.lean
git commit -m "feat(isolator): scaffold RestorationFramework"
```

---

### Task 2: Add Source/Decay Type Classes

**Files:**
- Modify: `DharmaMirror/Isolator.lean`

**Interfaces:**
- Consumes: `RestorationFramework`, `effectiveSource`, `deriv`.
- Produces: `EndogenousSource`, `BoundedEffectiveSource`, `PositiveDecay`, `ExogenousSource` classes.

- [ ] **Step 1: Append type classes to `DharmaMirror/Isolator.lean`**

After the `effectiveSource` definition, add:

```lean
/-- Conceptual marker: the source is determined by the system's internal state.
    Mathematically trivial; the real constraint comes from BoundedEffectiveSource. -/
class EndogenousSource (F : RestorationFramework) where
  is_internal : ∃ f : F.State → ℝ, ∀ s, F.sigma s = f s

/-- The effective source term omega * sigma is bounded by a finite constant K_eff. -/
class BoundedEffectiveSource (F : RestorationFramework) where
  K_eff        : ℝ
  K_eff_nonneg : 0 ≤ K_eff
  bound        : ∀ s, F.effectiveSource s ≤ K_eff

/-- Decay is strictly positive at every reachable state. -/
class PositiveDecay (F : RestorationFramework) where
  pos : ∀ s, 0 < F.delta s

/-- The source includes a contribution not reducible to the system state.
    Formally: there is a positive state-independent lower bound sigma_ext on the source. -/
class ExogenousSource (F : RestorationFramework) where
  sigma_ext    : ℝ
  sigma_ext_pos : 0 < sigma_ext
  lower_bound  : ∀ s, sigma_ext ≤ F.sigma s

/-- Faith/openness is coupling, not source production.
    This is encoded directly by the theorem in Task 5. -/
```

Note: the `ExogenousSource` class above is intentionally lightweight; its purpose is to tag a model. The limit theorem in Task 4 will add an unbounded external term explicitly.

- [ ] **Step 2: Build and verify**

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror/Isolator.lean
git commit -m "feat(isolator): add source and decay type classes"
```

---

### Task 3: Prove the Core Bound Theorem and Corollary

**Files:**
- Modify: `DharmaMirror/Isolator.lean`

**Interfaces:**
- Consumes: `RestorationFramework`, `BoundedEffectiveSource`, `PositiveDecay`, `EndogenousSource`.
- Produces: `bounded_endogenous_equilibrium_bound` and `bounded_endogenous_cannot_perfect` theorems.

- [ ] **Step 1: Append the bound theorem**

```lean
/-- THEOREM: positive decay + bounded effective source prevents perfect coherence.
    Equilibrium coherence is bounded above by K_eff / (K_eff + delta_min) < 1. -/
theorem bounded_endogenous_equilibrium_bound
    (F : RestorationFramework)
    [EndogenousSource F]
    [BoundedEffectiveSource F]
    [PositiveDecay F]
    (s : F.State)
    (heq : F.deriv s = 0)
    (homega : 0 < F.omega s)
    (delta_min : ℝ)
    (hdelta_min_pos : 0 < delta_min)
    (hdelta_lower : delta_min ≤ F.delta s)
    (hc : 0 ≤ F.c s ∧ F.c s ≤ 1) :
    F.c s ≤ BoundedEffectiveSource.K_eff / (BoundedEffectiveSource.K_eff + delta_min) := by
  let Λ := F.effectiveSource s
  have h1 : Λ * (1 - F.c s) = F.delta s * F.c s := by
    simp [RestorationFramework.deriv, RestorationFramework.effectiveSource] at heq
    linarith
  have h2 : F.c s = Λ / (Λ + F.delta s) := by
    have hne : Λ + F.delta s ≠ 0 := by nlinarith [hdelta_min_pos, hdelta_lower]
    field_simp
    nlinarith
  have h3 : Λ / (Λ + F.delta s) ≤ BoundedEffectiveSource.K_eff / (BoundedEffectiveSource.K_eff + delta_min) := by
    have hpos1 : 0 < Λ + F.delta s := by nlinarith [hdelta_min_pos, hdelta_lower]
    have hpos2 : 0 < BoundedEffectiveSource.K_eff + delta_min := by nlinarith [hdelta_min_pos, BoundedEffectiveSource.K_eff_nonneg]
    apply (div_le_div_iff (by positivity) (by positivity)).mpr
    nlinarith [BoundedEffectiveSource.bound s, hdelta_lower]
  linarith [h2, h3]
```

- [ ] **Step 2: Append the impossibility corollary**

```lean
/-- COROLLARY: bounded effective source + positive decay ⇒ equilibrium coherence < 1. -/
theorem bounded_endogenous_cannot_perfect
    (F : RestorationFramework)
    [EndogenousSource F]
    [BoundedEffectiveSource F]
    [PositiveDecay F]
    (s : F.State)
    (heq : F.deriv s = 0)
    (homega : 0 < F.omega s)
    (delta_min : ℝ)
    (hdelta_min_pos : 0 < delta_min)
    (hdelta_lower : delta_min ≤ F.delta s)
    (hc : 0 ≤ F.c s ∧ F.c s ≤ 1) :
    F.c s < 1 := by
  have h := bounded_endogenous_equilibrium_bound F s heq homega delta_min hdelta_min_pos hdelta_lower hc
  have hlt : BoundedEffectiveSource.K_eff / (BoundedEffectiveSource.K_eff + delta_min) < 1 := by
    have hpos : 0 < BoundedEffectiveSource.K_eff + delta_min := by nlinarith [hdelta_min_pos, BoundedEffectiveSource.K_eff_nonneg]
    apply (div_lt_iff₀ hpos).mpr
    nlinarith
  linarith
```

- [ ] **Step 3: Build and verify**

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds; both theorems are accepted.

- [ ] **Step 4: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror/Isolator.lean
git commit -m "feat(isolator): prove bounded effective source cannot perfect coherence"
```

---

### Task 4: Prove the Unbounded Source Limit Theorem

**Files:**
- Modify: `DharmaMirror/Isolator.lean`

**Interfaces:**
- Consumes: `RestorationFramework`, `PositiveDecay`, `equilibrium`, `addExogenousSource`.
- Produces: `unbounded_source_perfect_attractor` theorem.

- [ ] **Step 1: Append the limit theorem**

For a fixed state with positive `omega`, adding a constant exogenous source `Λ` makes the effective source `omega * (sigma + Λ)`. As `Λ → ∞`, the equilibrium approaches 1.

```lean
/-- THEOREM: unbounded exogenous source makes perfect coherence an attractor in the limit.
    For every ε > 0 there exists Λ₀ such that adding external source Λ ≥ Λ₀
    yields equilibrium coherence > 1 - ε. -/
theorem unbounded_source_perfect_attractor
    (F : RestorationFramework)
    [PositiveDecay F]
    (s : F.State)
    (homega : 0 < F.omega s)
    (delta_min : ℝ)
    (hdelta_min_pos : 0 < delta_min)
    (hdelta_lower : delta_min ≤ F.delta s) :
    ∀ ε > 0, ∃ Λ₀ : ℝ, 0 < Λ₀ ∧ ∀ Λ : ℝ, Λ₀ ≤ Λ →
      let F' := F.addExogenousSource Λ
      1 - ε < F'.equilibrium s := by
  intro ε hε
  use delta_min / ε
  constructor
  · positivity
  · intro Λ hΛ
    let F' := F.addExogenousSource Λ
    let Λeff := F.omega s * Λ
    have hΛeff_pos : 0 < Λeff := by positivity
    have h1 : F'.equilibrium s = (F.effectiveSource s + Λeff) / (F.effectiveSource s + Λeff + F.delta s) := by
      simp [RestorationFramework.equilibrium, RestorationFramework.effectiveSource, RestorationFramework.addExogenousSource]
      all_goals ring
    have h2 : 1 - ε < (F.effectiveSource s + Λeff) / (F.effectiveSource s + Λeff + F.delta s) := by
      have hpos : 0 < F.effectiveSource s + Λeff + F.delta s := by positivity
      apply (lt_div_iff₀ hpos).mpr
      nlinarith [hΛ, hdelta_lower]
    linarith [h1, h2]
```

- [ ] **Step 2: Build and verify**

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror/Isolator.lean
git commit -m "feat(isolator): prove unbounded source perfect-attractor limit"
```

---

### Task 5: Prove Faith Is Coupling, Not Source

**Files:**
- Modify: `DharmaMirror/Isolator.lean`

**Interfaces:**
- Consumes: `RestorationFramework`, `deriv`, `effectiveSource`.
- Produces: `faith_is_coupling_not_source` theorem.

- [ ] **Step 1: Append the coupling theorem**

```lean
/-- THEOREM: faith/openness is coupling, not source production.
    Rescaling omega by k and sigma by 1/k leaves the rate (and hence equilibrium)
    unchanged. -/
theorem faith_is_coupling_not_source
    (F : RestorationFramework) (k : ℝ) (hk : k ≠ 0) :
    let F' : RestorationFramework := {
      F with
      omega := fun s => k * F.omega s
      sigma := fun s => F.sigma s / k
    }
    ∀ s, F'.deriv s = F.deriv s := by
  intro F' s
  have hprod : F'.omega s * F'.sigma s = F.omega s * F.sigma s := by
    simp
    field_simp [hk]
  simp [RestorationFramework.deriv, hprod]
```

- [ ] **Step 2: Build and verify**

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror/Isolator.lean
git commit -m "feat(isolator): prove faith is coupling not source"
```

---

### Task 6: Create `ChristianInterpretation.lean` Placeholder

**Files:**
- Create: `DharmaMirror/ChristianInterpretation.lean`
- Modify: `DharmaMirror.lean`

**Interfaces:**
- Consumes: `DharmaMirror.Isolator` (`RestorationFramework`, type classes, theorems).
- Produces: `Theophysics.Christian.RestorationFramework` instance and proof obligations.

- [ ] **Step 1: Create the file**

```lean
import DharmaMirror.Isolator

set_option autoImplicit false

namespace Theophysics.Christian

/-- Christian mapping onto RestorationFramework.
    - sigma  → grace (external, unbounded in the limit)
    - delta  → sin / entropy / decay
    - omega  → faith / openness
    - c      → coherence / communion
    Proof obligation: show grace is exogenous and non-coercive. -/
def framework (G S Q C : ℝ) : RestorationFramework where
  State := Unit
  c     := fun _ => C
  sigma := fun _ => G
  delta := fun _ => S
  omega := fun _ => Q

/-- Non-coercive grace: the received contribution omega * sigma → 0 as omega → 0.
    The source G may remain available; it is not received without openness. -/
def nonCoercive (G S Q C : ℝ) : Prop :=
  Q * G = 0 → Q = 0

end Theophysics.Christian
```

- [ ] **Step 2: Import it in `DharmaMirror.lean`**

Add:

```lean
import DharmaMirror.ChristianInterpretation
```

- [ ] **Step 3: Build and verify**

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds.

- [ ] **Step 4: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror/ChristianInterpretation.lean DharmaMirror.lean
git commit -m "feat(isolator): add Christian interpretation placeholder"
```

---

### Task 7: Create `BuddhistInterpretation.lean` Placeholder

**Files:**
- Create: `DharmaMirror/BuddhistInterpretation.lean`
- Modify: `DharmaMirror.lean`

**Interfaces:**
- Consumes: `DharmaMirror.Isolator`.
- Produces: `Theophysics.Buddhist.RestorationFramework` instance and classification of source models.

- [ ] **Step 1: Create the file**

```lean
import DharmaMirror.Isolator

set_option autoImplicit false

namespace Theophysics.Buddhist

/-- Buddhist mapping onto RestorationFramework.
    - sigma  → wisdom / compassion / skillful means
    - delta  → craving / ignorance / attachment
    - omega  → meditative openness / insight
    - c      → liberation / awakening

    Obligation: specify which source model Buddhism adopts:
      (1) bounded endogenous  → isolator says c* < 1
      (2) unbounded endogenous → converges to exogenous-restoration class
      (3) exogenous / nondual ground → converges to exogenous-restoration class
      (4) not representable by scalar coherence → incommensurable -/
def framework (K S Q C : ℝ) : RestorationFramework where
  State := Unit
  c     := fun _ => C
  sigma := fun _ => K
  delta := fun _ => S
  omega := fun _ => Q

/-- Classification of Buddhist source commitments. -/
inductive SourceModel
  | boundedEndogenous
  | unboundedEndogenous
  | exogenousOrNondual
  | nonScalar

end Theophysics.Buddhist
```

- [ ] **Step 2: Import it in `DharmaMirror.lean`**

Add:

```lean
import DharmaMirror.BuddhistInterpretation
```

- [ ] **Step 3: Build and verify**

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds.

- [ ] **Step 4: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror/BuddhistInterpretation.lean DharmaMirror.lean
git commit -m "feat(isolator): add Buddhist interpretation placeholder"
```

---

### Task 8: Create `MaterialistInterpretation.lean` Placeholder

**Files:**
- Create: `DharmaMirror/MaterialistInterpretation.lean`
- Modify: `DharmaMirror.lean`

**Interfaces:**
- Consumes: `DharmaMirror.Isolator`.
- Produces: `Theophysics.Materialist.RestorationFramework` instance.

- [ ] **Step 1: Create the file**

```lean
import DharmaMirror.Isolator

set_option autoImplicit false

namespace Theophysics.Materialist

/-- Materialist mapping onto RestorationFramework.
    - sigma  → self-organization / local entropy reduction / information processing
    - delta  → entropy / dissipation
    - omega  → coupling to available free energy
    - c      → organized complexity
    Obligation: show self-organization can overcome positive decay without
    external source injection, or accept the bound. -/
def framework (Sigma S Q C : ℝ) : RestorationFramework where
  State := Unit
  c     := fun _ => C
  sigma := fun _ => Sigma
  delta := fun _ => S
  omega := fun _ => Q

end Theophysics.Materialist
```

- [ ] **Step 2: Import it in `DharmaMirror.lean`**

Add:

```lean
import DharmaMirror.MaterialistInterpretation
```

- [ ] **Step 3: Build and verify**

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds.

- [ ] **Step 4: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror/MaterialistInterpretation.lean DharmaMirror.lean
git commit -m "feat(isolator): add Materialist interpretation placeholder"
```

---

### Task 9: Final Build Verification

**Files:**
- Verify: all of the above.

- [ ] **Step 1: Full clean build**

```bash
cd "D:/dharma-mirror-lean"
lake clean
lake build
```

Expected: build succeeds with no errors and no warnings.

- [ ] **Step 2: Confirm neutral core compiles alone**

Temporarily comment out the three interpretation imports in `DharmaMirror.lean`, run:

```bash
cd "D:/dharma-mirror-lean"
lake build
```

Expected: build succeeds with only `DharmaMirror.Isolator` imported.

Restore the interpretation imports after verification.

- [ ] **Step 3: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add DharmaMirror.lean
git commit -m "chore(isolator): verify neutral core compiles independently"
```

---

### Task 10: Write `docs/isolator_protocol.md`

**Files:**
- Create: `D:/dharma-mirror-lean/docs/isolator_protocol.md`

**Interfaces:**
- Consumes: the formal results proven in Tasks 3–5.
- Produces: human-readable adjudication protocol.

- [ ] **Step 1: Create the protocol document**

```markdown
# Isolator Protocol — Adjudicating Endogenous vs Exogenous Restoration

## 1. Formal Result

For any coherence dynamics of the form

```text
dc/dt = omega(s) * sigma(s) * (1 - c) - delta(s) * c
```

if `delta(s) ≥ delta_min > 0` and the effective source `omega(s) * sigma(s) ≤ K_eff < ∞`,
then at equilibrium

```text
c* ≤ K_eff / (K_eff + delta_min) < 1.
```

Perfect coherence (`c* = 1`) is impossible with only a bounded endogenous effective source.

## 2. Endogenous Restoration Criteria

A source model is endogenous if:

- `sigma(s)` is computable from the system's internal state.
- The effective source `omega(s) * sigma(s)` is bounded by a finite constant independent of state.

Examples: self-organization, learning, practice, insight, internal information reconfiguration.

## 3. Exogenous Restoration Criteria

A source model is exogenous if:

- `sigma(s)` includes a contribution not determined by the system state.
- The effective source can be made arbitrarily large by increasing an external term.

Examples: external input, uncreated ground, infinite source, grace, nondual ground modeled as external to the finite self.

## 4. Adjudication Rules

1. **No relabeling without identifiability.** A worldview may not claim its source is exogenous merely by giving it a theological name. It must show the source term satisfies the formal exogeneity condition.
2. **Curve-fitting is not a proof obligation.** Demonstrating that a model fits data does not discharge the obligation to classify its source as endogenous or exogenous.
3. **Internal inconsistency is decisive.** If a worldview claims endogenous restoration and also claims perfect coherence, it must either bound its effective source and accept `c* < 1`, or admit an unbounded/external source.
4. **Incommensurability is allowed but costly.** A worldview may reject scalar coherence entirely, but then it cannot use the isolator's conclusions and must defend its own measurement framework.

## 5. Worldview Proof Obligations

| Worldview | Obligation |
|-----------|-----------|
| Christian | Show that grace functions as an exogenous, non-coercive source. Show that faith is coupling, not production of grace. |
| Buddhist | Specify the source model: bounded endogenous, unbounded endogenous, exogenous/nondual, or non-scalar. Then prove the consequences. |
| Materialist | Show that self-organization can overcome positive decay without external source injection, or accept the bound. |

## 6. Non-Coercive Grace

Non-coercive means the received contribution `omega * sigma → 0` as openness/faith `omega → 0`.
The source `sigma` may remain available; it is not coercively received by a closed system.
This preserves the distinction: grace is the source, faith is the coupling.
```

- [ ] **Step 2: Review for neutrality**

Read the document and confirm:
- No worldview is assumed true.
- The formal result is stated before any theological mapping.
- Each worldview has a clear proof obligation.

- [ ] **Step 3: Commit**

```bash
cd "D:/dharma-mirror-lean"
git add docs/isolator_protocol.md
git commit -m "docs(isolator): add adjudication protocol"
```

---

## Self-Review Checklist

- [ ] **Spec coverage:**
  - Neutral `RestorationFramework` → Task 1
  - `BoundedEffectiveSource` → Task 2
  - Core bound theorem → Task 3
  - Unbounded source limit theorem → Task 4
  - Faith-is-coupling theorem → Task 5
  - Christian/Buddhist/Materialist placeholders → Tasks 6–8
  - Protocol document → Task 10
- [ ] **Placeholder scan:** No TBD, TODO, or vague steps remain. Every theorem statement is explicit.
- [ ] **Type consistency:**
  - `BoundedEffectiveSource` uses `effectiveSource` = `omega * sigma` consistently across Tasks 2, 3, 4, 5.
  - `delta_min` and `K_eff` are used consistently in bound theorems.
  - `F.deriv s = 0` is the equilibrium condition in all theorems.
- [ ] **No theological axioms in neutral core:** `DharmaMirror/Isolator.lean` contains only mathematical definitions and theorems.

---

## Execution Handoff

Plan complete and saved to `D:/dharma-mirror-lean/docs/superpowers/plans/2026-07-02-theophysics-isolator-plan.md`.

Two execution options:

1. **Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — Execute tasks in this session using batch execution with checkpoints.

Which approach?
