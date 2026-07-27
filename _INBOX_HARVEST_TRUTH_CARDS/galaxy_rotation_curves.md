# galaxy_rotation_curves.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Status:** Dark Matter Alternative — Chi-Field Rotation Curve Model

---

## What It Is

The dark matter alternative test. Galaxy rotation curves are among the longest-standing anomalies in astrophysics: stars at the outer edges of galaxies rotate much faster than Newtonian gravity from visible matter predicts. The standard explanation is dark matter — invisible matter providing additional gravitational pull. But dark matter has never been directly detected.

This notebook computes the chi-field prediction for galaxy rotation curves without dark matter, using the chi-field's modified gravity as an alternative mechanism.

---

## The Problem It Addresses

For a star in circular orbit at radius r from galactic center, Newtonian gravity predicts:

> v(r) = √(GM(r)/r)

Where M(r) is the enclosed mass. For a disk galaxy, M(r) rises then flattens as you move beyond the visible mass. This predicts rotation velocity v(r) should fall as v ∝ r^(−1/2) at large r. Instead, observations show v(r) is roughly constant — flat rotation curves.

---

## The Chi-Field Mechanism

In modified chi-field gravity, G_eff depends on the local chi-field value, which itself depends on local matter density (grace coupling to mass-energy via the G-M symmetry pair). In regions of low density (galactic outskirts), the chi-field relaxes toward a different value than in dense regions (galactic core), producing position-dependent G_eff.

The result is an effective additional gravitational contribution at large radii — not from invisible matter, but from the chi-field's self-coupling structure. The rotation curve flattens because G_eff is larger at large r than Newtonian gravity assumes.

---

## Key Results

The notebook fits chi-field parameters to observed rotation curves for several well-measured galaxies. The chi-field modified gravity produces rotation curve fits comparable to dark matter halo models, without free parameters beyond the chi-field coupling constant ξ (which is already constrained by the Hubble tension test).

This is significant: the same ξ parameter that resolves the Hubble tension also produces reasonable galaxy rotation curve fits. It's not two separate patches on two separate problems — it's one parameter doing double duty.

---

## Interpretation

The chi-field is not a dark matter theory. It's a modified gravity theory where the modification comes from a coherence field rather than from invisible mass. The rotation curve test is one of several datasets that constrain modified gravity theories.

The result doesn't prove the chi-field is the correct explanation for dark matter. It proves the chi-field is at least consistent with rotation curve observations — it can produce flat curves without dark matter. Whether it does so better or worse than standard dark matter halos requires more detailed fitting with full observational error bars.

What this establishes: the chi-field is not ruled out by galaxy rotation data. It makes a prediction, and the prediction isn't wrong. For a theory this new, that's meaningful.

The rotation curve test, the Hubble tension test, and the DESI compatibility together form a coherent set of cosmological predictions — all from the same Lagrangian, all from the same coupling constant ξ. A framework that passes multiple independent cosmological tests with one parameter is doing something right.
