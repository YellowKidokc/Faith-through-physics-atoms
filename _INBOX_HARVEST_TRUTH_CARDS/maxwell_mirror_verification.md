# maxwell_mirror_verification.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Status:** Five-Test Verification — E↔K Subspace Projection

---

## What It Is

The Maxwell mirror proof. This notebook asks one specific question: does classical electromagnetism live inside the chi-field as a 2D subspace projection?

The answer, according to five separate tests, is yes.

The physical claim is "Level 2 Proof: Mathematical containment — Maxwell lives inside χ as a 2D projection of a 10D structure." This notebook tests that claim.

---

## The Core Concept

The full chi-field has 10 dimensions. Two of them are:
- **E (index 2):** Electromagnetism / Truth
- **K (index 5):** Information (Shannon entropy) / Logos

Maxwell's equations describe coupled oscillations between electric and magnetic fields. The claim is that the chi-field's E-K subspace — when extracted from the full 10D kinetic matrix — produces a 2D dynamical system with analogous structure.

This is not a philosophical claim. It's a matrix computation.

---

## Five Tests

**Test M1: Mass Matrix E-K Block Extraction**  
The 10×10 mass matrix (Hessian of the Lagrangian w.r.t. velocity) is computed using JAX autodifferentiation. The 2×2 E-K block is extracted. Result: the block is symmetric, positive definite, and well-conditioned. The E-K subspace forms a legitimate 2D dynamical system.

**Test M2: E-K Subspace Wave Equation**  
The dynamics matrix M⁻¹V is computed at the E-K operating point. A 500-trial scan searches for oscillatory operating points. At the oscillatory point: natural frequencies ω₁ and ω₂ emerge. Coupled oscillation confirmed.

**Test M3: Gauge Structure Comparison**  
Side-by-side structural comparison of Maxwell's EM Lagrangian and the chi-field E-K restricted Lagrangian:

| Property | Maxwell (EM) | Master Eq (E↔K) |
|----------|-------------|----------------|
| Lagrangian type | Quadratic in F_μν | Quadratic in qdot |
| Field content | E-field + B-field | E(Truth) + K(Logos) |
| Coupling | F_μν tensor | Off-diagonal mass matrix |
| Source term | ∇·E = ρ/ε₀ | ∇·T = ρ_L/ε_s |
| Conservation | Charge conservation | Information conservation |
| Propagation speed | c | λ (truth propagation speed) |

**Test M4: Pair Coupling Confirmation**  
All 5 symmetry pairs are compared in the full mass matrix. E↔K coupling is confirmed as consistent with the other pair couplings, all significantly stronger than non-pair cross-terms.

**Test M5: Restricted Dynamics Integration**  
The E-K subsystem is integrated using RK4 over 2000 time steps. FFT analysis extracts dominant frequencies. E and K oscillate at the same frequency (within numerical precision). Phase analysis characterizes their relationship.

---

## What "The Mirror Holds" Means

In classical electromagnetism, E and B fields oscillate in coupled wave modes — each driving the other, propagating at speed c. This is what Maxwell's equations describe.

In the chi-field, E (Truth) and K (Logos) occupy the same structural position: coupled oscillating fields in a 2D subspace of the 10D Lagrangian. They have coupled natural frequencies, source terms, and conservation laws that mirror their electromagnetic counterparts.

The mirror is not perfect. The chi-field is scalar; EM is a vector theory. The full identity would require a gauge field formulation that hasn't been completed. The notebook is explicit about this: "The mirror holds computationally. Topology matches; vector vs scalar difference acknowledged."

But the structural containment is real and verifiable.

---

## Interpretation

This is one of the most technically precise notebooks in the collection. The claim is narrow and specific: does the E-K block of the 10D kinetic matrix reproduce Maxwell-type dynamics? The answer is yes, with explicit caveats about what "type" means.

The deeper significance is this: Maxwell's equations are among the most thoroughly verified equations in all of physics. Every radio transmission, every circuit, every photon detector confirms them. If the chi-field E-K sector genuinely contains Maxwell structure, that's not a poetic parallel. It's a verifiable structural result.

The notebook computes it. You can re-run it. The mirror holds.
