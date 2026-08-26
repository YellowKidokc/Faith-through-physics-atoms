# Appendix B: Mathematical Derivation

## The Hubble Gradient Function H₀(z)

**DT-004: The Hubble Gradient** **Status:** Core derivation — load-bearing for the paper's testability

---

## B.1 The Physical Argument

The main paper argues that the Hubble tension arises because measurements at different redshifts use "rulers" calibrated in different thermodynamic reference frames. This appendix formalizes that argument into an explicit, testable function.

The key physical variable is the **structure fraction** f_s(z) — the fraction of the universe's baryonic matter that exists in gravitationally collapsed, thermodynamically structured systems (atoms, molecules, stars, galaxies) at redshift z.

At z ~ 1100 (CMB epoch): f_s ≈ 0. The universe is thermal plasma. No structure exists. All measurement scales are thermally defined.

At z ~ 0 (today): f_s ≈ 1. The universe is fully structured. Measurement scales are defined by atomic transitions, stellar physics, and gravitational dynamics.

The "ruler" used to measure expansion is a weighted average of thermal and structural length scales, with the weight determined by f_s(z).

---

## B.2 The Functional Form

### Definition

The effective Hubble parameter as measured at redshift z is:

```
H₀(z) = H_thermal + ΔH · f_s(z)
```

Where:

- H_thermal = 67.4 km/s/Mpc (the value measured in the thermal reference frame; Planck 2018)
- H_local = 73.5 km/s/Mpc (the value measured in the structural reference frame; SH0ES)
- ΔH = H_local - H_thermal = 6.1 km/s/Mpc
- f_s(z) = structure fraction at redshift z

### Structure Fraction

The structure fraction follows a generalized logistic (sigmoidal) function:

```
f_s(z) = 1 / (1 + (z / z_t)^α)
```

Where:

- z_t = transition redshift (where structure formation is approximately half-complete)
- α = steepness parameter (how rapidly the transition occurs)

### Complete Equation

```
H₀(z) = 67.4 + 6.1 / (1 + (z / z_t)^α)       [Eq. B.1]
```

**Free parameters:** 2 (z_t and α) **Fixed parameters:** 2 (H_thermal = 67.4, H_local = 73.5; both observed)

---

## B.3 Parameter Constraints

### From Structure Formation Simulations

The parameters z_t and α are NOT free in the usual sense — they are constrained by independent observations and simulations of cosmic structure formation:

**Transition redshift z_t:** Cosmological simulations (Illustris-TNG, EAGLE, FLAMINGO) show that the stellar mass density of the universe reaches approximately half its present-day value at z ≈ 1.0–2.0. The cosmic star formation rate peaks at z ≈ 1.5–2.5 (the "cosmic noon"). This constrains z_t to the range 1.0–2.5.

**Steepness α:** The steepness of the structure formation transition is determined by the physics of gravitational collapse, cooling, and feedback. Simulations suggest a relatively gradual transition, consistent with α ≈ 1.5–2.5. A very steep transition (α > 4) would imply a sudden phase change in structure formation, which is not observed.

### Independent Calibration Test

**Critical point:** The parameters z_t and α should NOT be fitted to Hubble data. They should be derived from structure formation data (stellar mass density, star formation rate, galaxy luminosity functions) and then TESTED against Hubble measurements. If the structure-formation-derived values produce the correct H₀ gradient, that is a genuine prediction. If they must be tuned to fit Hubble data but don't match structure formation, the thermodynamic interpretation fails.

This is the difference between a prediction and a fit.

---

## B.4 Numerical Predictions

### Using z_t = 1.5, α = 2.0 (central values from structure formation)

|Redshift z|f_s(z)|H₀(z) predicted|Measurement context|
|---|---|---|---|
|0|1.000|73.5|Local distance ladder|
|0.1|0.996|73.5|Nearby SNe|
|0.3|0.962|73.3|Intermediate SNe|
|0.5|0.900|72.9|BAO (model-dependent*)|
|1.0|0.692|71.6|JWST distance ladder|
|1.5|0.500|70.5|JWST high-z|
|2.0|0.360|69.6|JWST high-z|
|3.0|0.200|68.6|JWST deep fields|
|5.0|0.083|67.9|Early galaxy surveys|
|10.0|0.023|67.5|Pre-reionization|
|1100|~0|67.4|CMB|

*Note on BAO: Baryon Acoustic Oscillation measurements at z ~ 0.5 do not directly measure H₀ in the same way the distance ladder does. BAO measures the angular diameter distance and sound horizon scale. The inferred H₀ depends on the assumed cosmological model. If ΛCDM (which assumes constant H₀) is used to interpret BAO, the result will be pulled toward the CMB value by construction. BAO values in the 68–70 range may reflect the ΛCDM assumption rather than an independent gradient measurement. Only model-independent distance ladder measurements at various redshifts can directly test the gradient prediction.

### Using z_t = 1.0, α = 2.0 (lower bound)

|Redshift z|f_s(z)|H₀(z) predicted|
|---|---|---|
|0.5|0.800|72.3|
|1.0|0.500|70.5|
|1.5|0.308|69.3|
|2.0|0.200|68.6|
|3.0|0.100|68.0|

### Using z_t = 2.5, α = 1.5 (upper bound)

|Redshift z|f_s(z)|H₀(z) predicted|
|---|---|---|
|0.5|0.964|73.3|
|1.0|0.849|72.6|
|1.5|0.720|71.8|
|2.0|0.598|71.0|
|3.0|0.399|69.8|

---

## B.5 Testable Predictions with Error Bands

The parameter ranges z_t ∈ [1.0, 2.5] and α ∈ [1.5, 2.5] define a prediction band for H₀(z):

|Redshift z|H₀ Prediction Band (km/s/Mpc)|
|---|---|
|0|73.5 (fixed by observation)|
|0.5|72.3 – 73.3|
|1.0|70.5 – 72.6|
|1.5|69.3 – 71.8|
|2.0|68.6 – 71.0|
|3.0|68.0 – 69.8|
|5.0|67.6 – 68.5|
|10.0|67.4 – 67.8|

**Key prediction:** At z > 3, H₀ should be below 70 km/s/Mpc regardless of parameter choice. This is the sharpest falsification target.

---

## B.6 Relationship to Standard Cosmology

### What changes

In standard ΛCDM, the Hubble parameter H(z) varies with redshift according to the Friedmann equation:

```
H(z) = H₀ · √(Ω_m(1+z)³ + Ω_Λ)
```

Here H₀ is a single constant. The variation of H(z) with z is due to the changing matter-energy density, not the changing measurement frame.

In the emergent distance framework, the Friedmann equation remains valid as a description of the emergent geometry. The additional claim is that the constant H₀ in the Friedmann equation is itself frame-dependent: its measured value depends on the thermodynamic state of the measurement apparatus available at redshift z.

### What stays the same

All predictions of GR and ΛCDM remain valid within each reference frame. The emergent framework does not modify gravity, add particles, or change the energy content of the universe. It adds a single interpretive layer: the recognition that the "constant" H₀ is measured with epoch-dependent rulers.

### Mathematical relationship

The standard Friedmann H(z) and the gradient H₀(z) are related by:

```
H_measured(z) = H₀(z) · √(Ω_m(1+z)³ + Ω_Λ) / H₀(z=0)
```

Where the ratio H₀(z)/H₀(z=0) acts as a redshift-dependent calibration correction. At z = 0, this ratio is 1 and standard cosmology is recovered exactly.

---

## B.7 Kill Conditions (Mathematical)

The functional form H₀(z) = 67.4 + 6.1/(1 + (z/z_t)^α) is falsified if:

**KC-B1:** The best-fit z_t from Hubble data falls outside [0.5, 5.0]. This would indicate the transition is not associated with structure formation.

**KC-B2:** The best-fit α from Hubble data falls outside [0.5, 4.0]. This would indicate the transition shape is not consistent with known structure formation physics.

**KC-B3:** H₀ measured at z > 3 exceeds 70 km/s/Mpc. No parameter combination within the allowed range produces H₀ > 70 at z > 3.

**KC-B4:** The best-fit z_t and α from Hubble data are inconsistent (> 3σ) with the same parameters derived from structure formation data (stellar mass density, cosmic star formation rate). This would indicate the gradient exists but is not caused by structure formation — requiring a different mechanism.

**KC-B5:** Direct distance ladder measurements at z > 1 (not BAO, not model-dependent) show H₀ > 72. This would indicate no convergence toward the CMB value.

---

## B.8 What This Appendix Does NOT Do

This derivation provides a functional form and testable predictions. It does NOT:

1. Derive the thermodynamic reference frame interpretation from first principles (this requires a microscopic theory of emergent geometry)
2. Prove that structure formation is the correct variable (it could be information density, entropy, or something else correlated with structure)
3. Replace ΛCDM (the standard model is recovered as a special case)
4. Claim certainty about z_t and α (these are predictions to be tested, not established facts)

The derivation is complete enough to test. It is not complete enough to replace the standard model. That distinction matters.

---

## References

Madau, P. & Dickinson, M. (2014). Cosmic Star-Formation History. ARA&A, 52, 415–486. DOI: 10.1146/annurev-astro-081811-125615

Pillepich, A. et al. (2018). Simulating galaxy formation with the IllustrisTNG model. MNRAS, 473(3), 4077–4106. DOI: 10.1093/mnras/stx2656

Planck Collaboration. (2020). Planck 2018 results. VI. Cosmological parameters. A&A, 641, A6. DOI: 10.1051/0004-6361/201833910

Riess, A. G. et al. (2022). A Comprehensive Measurement of the Local Value of the Hubble Constant. ApJL, 934(1), L7. DOI: 10.3847/2041-8213/ac5c5b

Schaye, J. et al. (2015). The EAGLE simulations of galaxy formation. MNRAS, 446(1), 521–554. DOI: 10.1093/mnras/stu2058

---

_"The difference between a hypothesis and a prediction is an equation."_