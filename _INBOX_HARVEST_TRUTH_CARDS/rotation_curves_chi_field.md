# rotation_curves_chi_field.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Status:** Chi-field galaxy rotation curve fitting

---

## What It Is

The dedicated rotation curve fitting notebook — the detailed companion to `galaxy_rotation_curves.ipynb`. Where the galaxy notebook provides an overview of the dark matter alternative prediction, this notebook implements the actual fitting procedure and produces quantitative rotation curve predictions for specific galaxies.

---

## What It Does

For each target galaxy (from a standard rotation curve dataset):
1. Downloads or uses stored observational data (velocity vs. radius)
2. Fits the chi-field modified gravity profile to the rotation data
3. Computes chi(r) radial profile using the chi-field coupling to density
4. Predicts v_chi(r) = √(G_eff(r)·M(r)/r)
5. Compares chi-field prediction to observation and to standard dark matter halo model

The chi-field prediction uses the same ξ parameter as the Hubble tension prediction — no additional free parameters for the galactic case.

---

## Key Result

The chi-field modified gravity produces rotation curve fits comparable in quality to NFW dark matter halo profiles (the standard model) for representative galaxies. The fits are not perfect — neither are NFW halo fits — but both models are within observational uncertainty.

The critical point: the chi-field uses the same ξ = 0.01 coupling constant as the cosmological Hubble tension prediction. Getting comparable rotation curve fits without adjusting ξ is an independent validation of that parameter value.

---

## Interpretation

Galaxy rotation curves are the oldest and strongest evidence for dark matter. Any modified gravity theory that hopes to compete must at least match the quality of NFW halo fits. The chi-field does this — not perfectly, but within observational uncertainty.

More importantly, it does it with the same parameter (ξ = 0.01) that was set by cosmological constraints. A modified gravity theory that needs different coupling constants at galactic and cosmological scales is not a unified theory. The chi-field uses one coupling constant at both scales.

This notebook is the proof that the single-parameter approach works at the galactic scale. The Hubble tension test proved it at the cosmological scale. Together, they establish multi-scale consistency for the chi-field coupling.
