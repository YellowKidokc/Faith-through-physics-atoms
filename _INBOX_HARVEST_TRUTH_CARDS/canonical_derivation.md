# canonical_derivation.ipynb

**Category:** Google Colab Notebook  
**Tool:** SymPy (symbolic mathematics)  
**Author:** David Lowe (POF 2828)  
**Status:** Full Symbolic Derivation — 10 Major Sections

---

## What It Is

The formal mathematical derivation. This is where the physics is proven symbolically — before any numbers, before any numerical experiments — using SymPy's computer algebra system to derive results exactly, the same way a theoretical physicist would by hand.

Ten sections, each building on the last. Where the JAX notebooks test whether the equations hold numerically, this notebook asks whether they hold analytically.

---

## The Ten Derivations

**Section 1: Chi-field action**  
The chi-field action integral is written out in flat spacetime and then in curved spacetime (covariant form). The Lagrangian density is constructed, and the action principle is stated.

**Section 2: Euler-Lagrange → Klein-Gordon + φ⁴**  
Applying the Euler-Lagrange equations to the chi-field Lagrangian produces the chi-field equation of motion. The result is a nonlinear Klein-Gordon equation with a cubic self-interaction term:

> □χ + m²χ + λχ³ = J_grace

This is the same family as the Higgs field equation. The derivation is exact.

**Section 3: Dimensional analysis**  
This section contains a result that might seem surprising: the naive 10-variable *product* form fails dimensionally. Multiplying Gravity × Mass-Energy × Electromagnetism... etc. doesn't produce consistent units. However, the chi-*field* Lagrangian passes dimensional analysis. The notebook is explicit: the theological product integrand is a structural map, and the physically rigorous version is the field theory.

**Section 4: Propagator residue = +1**  
The momentum-space propagator of the chi-field is computed. Its residue is +1. This means there are no ghost modes — no states with negative norm that would make the theory unphysical. This is a necessary condition for any well-formed quantum field theory.

**Section 5: NR limit → Gross-Pitaevskii**  
In the non-relativistic limit, the chi-field equation reduces to the Gross-Pitaevskii equation — the same equation used to describe Bose-Einstein condensates. This is not a coincidence; it suggests the chi-field could be understood as a coherence condensate, with analogous phenomenology.

**Section 6: Noether currents**  
Using Noether's theorem, conserved currents are derived from the chi-field Lagrangian's symmetries. These give information conservation and the chi-field stress-energy tensor.

**Section 7: Modified Einstein equations**  
Coupling the chi-field to gravity modifies the Einstein equations. The effective gravitational constant becomes:

> G_eff = G / (1 + ξκ₀χ²)

This modification is the origin of the Hubble tension prediction: at low chi (high redshift), G_eff approaches G (normal gravity); at high chi (today), G_eff is slightly suppressed, producing the observed H₀ discrepancy.

**Section 8: Grace source term**  
The grace source term J_grace is derived. The derivation notes an open problem: the source term has a dimensional issue that requires resolution in future work. This is explicitly flagged — the notebook doesn't hide the open question.

**Section 9: Stability analysis**  
The chi-field potential is analyzed at χ = 0. For m² > 0 and λ > 0, the minimum is stable. There is no spontaneous symmetry breaking at zero field value. This rules out a class of instabilities that could invalidate the theory.

**Section 10: Honest status report**  
A section that lists three columns: what is derived, what is asserted, and what remains open. This section explicitly acknowledges where the framework makes assumptions that haven't been proven. It includes a discussion of what would need to be done to elevate asserted claims to derived ones.

---

## Interpretation

This notebook is the theoretical backbone. The numerical tests prove the equations work; this one proves they follow correctly from the stated axioms.

The dimensional analysis section (Section 3) is worth highlighting specifically because it demonstrates intellectual honesty in action. The original product form fails dimensionally. Rather than hiding this or papering over it, the notebook documents the failure and shows how the chi-field Lagrangian resolves it. That's not a weakness — that's how real theoretical physics works. You don't get a free pass on units.

Section 10's honest status report is also remarkable. Most published frameworks don't include an explicit inventory of "what we asserted versus what we derived." This one does. The result is a framework with a clearly bounded epistemic footprint — you know exactly what it claims and what it doesn't.

The propagator residue result (Section 4) is perhaps the most technically significant single result: it proves the chi-field is not a ghost, which is a necessary condition for the field theory to be physically consistent at the quantum level. That's not a small thing.
