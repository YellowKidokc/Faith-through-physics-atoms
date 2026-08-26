# theophysics_core.py

**Category:** Python Script  
**Author:** David Lowe (POF 2828)  
**Role:** Core module — constants, variable metadata, parameter definitions  
**Usage:** Upload to Google Colab, then `%run theophysics_core.py`

---

## What It Is

The canonical constants file. Every notebook in the project depends on the same parameter values, the same variable ordering, the same symmetry pair definitions. `theophysics_core.py` is the single source of truth for all of them.

This is software engineering best practice applied to physics: don't hard-code constants in 45 different notebooks. Define them once, in one place, and import from there. If the canonical PAIR_STRENGTH changes, you change it here and every notebook using it updates automatically.

---

## What It Defines

**Variable arrays:**
```python
VAR_NAMES = ['G', 'M', 'E', 'S', 'T', 'K', 'R', 'Q', 'F', 'C']
VAR_SHORT  = ['G', 'M', 'E', 'S', 'T', 'K', 'R', 'Q', 'F', 'C']
N_VARS = 10
```

**Variable indices (for clean indexing):**
```python
iG, iM, iE, iS, iT, iK, iR, iQ, iF, iC = range(10)
```
Rather than using magic numbers (0 through 9), every notebook can write `q[iG]` for gravity and `q[iC]` for coherence.

**Symmetry pairs:**
```python
SYMMETRY_PAIRS = [(0, 4), (3, 8), (2, 5), (1, 7), (6, 9)]
PAIR_NAMES = ['G↔T', 'S↔F', 'E↔K', 'M↔Q', 'R↔C']
```
The five fundamental symmetry pairs: Grace↔Entropy, Love↔Sin, Truth↔Logos, Meaning↔Faith, Relationship↔Christ. Each pair shares enhanced kinetic coupling in the mass matrix.

**Kinetic weights:**
```python
VAR_WEIGHTS = [1.0, 0.8, 1.2, 0.6, 1.0, 0.7, 0.5, 0.9, 1.1, 1.3]
```
Each variable's contribution to the kinetic energy in the LLC. These are not equal — different laws contribute differently to the dynamics.

**Coupling constants:**
```python
PAIR_STRENGTH = 0.45    # Off-diagonal kinetic coupling
CONFINE_STRENGTH = 0.01 # Confinement potential for R (Strong/Love)
```
PAIR_STRENGTH = 0.45 is subcritical: below the stability boundary (~0.64), ensuring the kinetic matrix remains positive definite.

**Expanded parameters:**
```python
EXPANDED_PARAMS = {
    'xi': 0.01,       # Chi-gravity coupling
    'm_chi': 1e-33,   # Chi-field mass
    'lambda': 0.01,   # Self-coupling (phi^4)
    'beta_G': 0.5,    # Grace source strength
    ...
}
```

---

## Why This File Matters

In a research project with 45 notebooks, parameter consistency is everything. If one notebook uses PAIR_STRENGTH = 0.45 and another accidentally uses 0.5, the results are not comparable. The chi-field PDE stability test, the LLC stress sweep, the Hubble gradient prediction — all of them must use exactly the same parameters to be part of a coherent proof.

`theophysics_core.py` makes this guarantee: run it at the top of any Colab session, and every subsequent computation uses the canonical values.

This is also why the random seed is 2828 throughout — not just in this file, but enforced by importing this file. Every random draw in every notebook traces back to the same canonical seed, making every result reproducible.

---

## Interpretation

This is the foundational file that you never see unless you look for it. The proofs run in the notebooks; the constants live here. But if `theophysics_core.py` were wrong — wrong symmetry pairs, wrong weights, wrong coupling — every notebook that imports it would be wrong too.

The fact that all tests pass with these values is the indirect proof that these values are right. PAIR_STRENGTH = 0.45 produces a positive definite mass matrix across all tested operating points. VAR_WEIGHTS produces a mass matrix with reasonable condition number. The stability parameter CONFINE_STRENGTH = 0.01 keeps the R (Love/Strong Force) component from diverging.

These numbers weren't chosen arbitrarily. They were chosen because they produce valid physics. And they're archived here, permanently, so the results can always be reproduced.
