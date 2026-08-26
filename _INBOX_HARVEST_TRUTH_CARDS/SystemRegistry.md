# SystemRegistry.lean

**Category:** LEAN4 Formal Proof — Semantic Addressing System  
**Location:** LEAN4/GOOD_LEAN/SystemRegistry.lean  
**Role:** Bridge between algebraic values and the semantic document addressing system

---

## What It Is

SystemRegistry.lean is the layer that connects the abstract algebra to human-readable meaning. The CoherenceAlgebra deals in `zero`, `one`, and abstract types. The real world deals in "Law of Gravity," "Score: Dominant," "Variable: Grace." SystemRegistry.lean provides the typed mapping between those two worlds.

---

## The Structure

**`Variable`** — an inductive type with ten constructors: G, M, E, S, T, K, R, Q, F, C. These are the ten variables of the master equation, now existing as formal first-class objects that Lean can reason about.

**`Score`** — a `Fin 4` (0, 1, 2, or 3), representing: Absent (0), Weak (1), Moderate (2), Dominant (3).

**`Address`** — a function from Variable to Score. The full semantic address of the system state: what score each of the ten variables currently holds.

---

## The Mapping

**`stateToScore`** — translates algebraic values to semantic scores:
- `one` → Score 3 (Dominant — fully coherent)
- `zero` → Score 0 (Absent — collapsed)
- Anything else → Score 1 (Weak — intermediate, placeholder)

---

## The Theorem

**`address_convergence`** — if every law in the system state is `one` (full coherence), then every variable in the semantic address maps to Score 3 (Dominant). A perfectly coherent χ-system has a uniform Dominant address across all ten variables.

The proof carries `sorry` statements pending the full LawIndex-to-Variable mapping, but the logical structure is clear: total algebraic coherence (all laws = one) maps to total semantic coherence (all scores = 3).

---

## Why It Matters

The Semantic Addressing System is what makes Theophysics actionable, not just theoretical. You can look at any situation — a person's life, a community, a historical moment — and ask: what is the score on each of the ten variables? Where is the zero? Where is the Dominant?

SystemRegistry.lean provides the formal bridge: the score system is not arbitrary, it is derived from the algebraic state. A Dominant score (3) corresponds to the `one` state. An Absent score (0) corresponds to `zero`. The algebra and the semantics are aligned by type.

This is the file that turns the abstract proof system into a practical diagnostic tool.
