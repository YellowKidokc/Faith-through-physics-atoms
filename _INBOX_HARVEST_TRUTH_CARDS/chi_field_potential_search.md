# chi_field_potential_search.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Status:** Parameter scan — Chi-field potential landscape mapping

---

## What It Is

The stability boundary-finder for the chi-field potential. This notebook systematically scans the chi-field's parameter space (m², λ, and coupling constants) to map where stable solutions exist, where instabilities emerge, and where the theory breaks down.

Think of it as the engineering tolerance test: before you claim your theory works at a given parameter set, you should know how far from that parameter set you can move before it stops working.

---

## What It Scans

The chi-field potential takes the form:

> V(χ) = ½m²χ² + ¼λχ⁴

Three scanning dimensions:
1. **m² (mass squared):** From negative (tachyonic) through zero (massless) to positive (massive, stable)
2. **λ (self-coupling):** From zero through subcritical to supercritical
3. **Grace coupling β_G:** How strongly the grace source term drives the field

At each grid point, the notebook:
- Initializes the chi-field solver with those parameters
- Integrates for N time steps
- Checks whether the solution remains bounded or diverges
- Records the outcome: STABLE, OSCILLATORY, DECAYING, UNSTABLE

---

## Key Results

The stability map shows:
- **m² > 0, λ > 0:** Stable potential well. The canonical parameter region.
- **m² < 0, λ > 0:** Mexican hat potential. Spontaneous symmetry breaking — the field rolls off zero to a nonzero vacuum.
- **m² < 0, λ = 0:** Tachyonic instability. Field diverges.
- **m² > 0, λ = 0:** Stable but non-interacting. Standard massive scalar.
- **Large λ:** Stiff potential. Oscillations at high frequency. Numerical stability requires small dt.

The canonical chi-field parameters (m² = 10⁻⁶⁶ kg²·m⁻²·s⁻², λ = 0.01 in natural units) sit well within the stable region, with large margins to the nearest instability.

---

## Interpretation

This notebook answers the most practical stability question: how robust is the chi-field to parameter variation? The answer is: very robust. The stable parameter region is large, and the canonical parameters are deep within it.

This matters because the canonical parameters come from physical matching requirements — they're set by the Hubble tension prediction and the LLC structure, not by hand-tuning for stability. The fact that these physically-motivated parameters happen to sit in the stable region (rather than near a boundary) is evidence of internal consistency.

The potential scan also identifies the conditions under which the chi-field would spontaneously symmetry-break — a feature that might be physically interesting for early-universe cosmology but isn't part of the current canonical model. The notebook documents where those boundaries are.
