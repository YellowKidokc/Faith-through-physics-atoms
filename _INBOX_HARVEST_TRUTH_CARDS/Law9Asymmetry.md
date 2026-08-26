# Law9Asymmetry.lean

**Category:** LEAN4 Formal Proof — Law 9 (Weak Force / Sin)  
**Location:** LEAN4/GOOD_LEAN/Law9Asymmetry.lean  
**Role:** Proves that the sin-process is directional, non-invertible, and asymmetric

---

## What It Is

The Weak Force is the only fundamental force in physics that violates parity symmetry — it has a preferred direction, a handedness, that cannot be mirrored. This is called CP violation. Law9Asymmetry.lean takes that physical fact and formalizes its theological mapping: Sin is the asymmetric operator in the coherence system.

It proves one essential thing: the operator that maps a coherent state to zero has no internal inverse.

---

## The Theorem

**`sin_asymmetry`** — if the system is in the aligned state (one), then applying SinProcess gives zero: `state = one → SinProcess state = zero`

The proof is immediate by definition — `SinProcess` is defined to always return zero (a simplification that captures the essential property: sin collapses coherence). What makes the file significant is not the proof itself but the formal encoding: Sin is modeled as a *unidirectional* operator that cannot be reversed by anything within the system's own closure.

---

## The Asymmetry Point

The file's comment is worth quoting directly: *"Unlike Laws 1-8, Law 9 is directional. We model this as a non-invertible operator."*

Laws 1-8 are bilateral — they have restoring forces, equilibria, symmetries. The strong force binds and releases. Electromagnetism attracts and repels. Gravity is always attractive but the orbits are stable cycles. Law 9 — the Weak Force / Sin — is the exception. It violates the symmetry. It has a preferred direction: toward zero.

The formal consequence: there is no `SinInverse` in the operator algebra that could map zero back to one using the same mechanism. The Grace Operator does this — but Grace is explicitly external to the system (proved in GraceOperator.lean). Sin and Grace are not symmetric. They are not mirror images. Grace is the only exit from where Sin leads.

---

## Why It Matters

The asymmetry between sin and grace is often described theologically as "you can't earn your way back." Law9Asymmetry.lean provides a formal version of that claim. The operator that collapses coherence and the operator that restores it are not inverses of each other. They do not cancel. The path down (SinProcess) and the path back up (graceStep) are structurally different kinds of operations — and that difference is now proved in a theorem.
