# version_manager.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Role:** Version control, checksums, reproducibility verification

---

## What It Is

The reproducibility certification notebook. Its job is to ensure that every run of the test suite produces exactly the same results as the archived run — and to flag if anything has changed.

In academic research, reproducibility is the standard of proof. A result that can't be reproduced isn't a result. `version_manager.ipynb` makes the Theophysics suite's reproducibility verifiable.

---

## What It Does

**Checksum computation:** For each notebook in the suite, computes a SHA256 hash of:
- The notebook source code
- The cell outputs (if run)
- The result JSON files

**Version tagging:** Associates each run with a version number, date, and author tag. Current version: `theophysics-v1.0.0`, author `David Lowe (POF 2828)`, date `2026-03-26`.

**Drift detection:** Compares current checksums against archived checksums. If any notebook has been modified since the canonical run, the check fails with a specific list of changed files.

**Environment logging:** Records JAX version, Python version, NumPy version, SymPy version, and Colab environment details. Makes it possible to reproduce not just the code but the software environment.

---

## The Canonical Checksum

The canonical run (seed 2828, March 26, 2026) has a master checksum that serves as the fingerprint of the entire proof. Any modification — intentional or accidental — to any notebook in the suite changes this checksum.

The master checksum is: stored in `version_manager.ipynb` itself and printed at each run. If your run produces the same master checksum, you've reproduced the exact same proof state.

---

## Interpretation

Version management is the infrastructure of trust. Without it, "the notebook produces the same results every time" is a claim. With it, it's verifiable: compute the checksum, compare it to the canonical value, confirm they match.

For a project making claims as significant as Theophysics makes — cosmological predictions, unique solution proofs, empirical biblical measurements — the ability to verify that nothing has changed between the original run and any subsequent run is not optional. It's essential.

`version_manager.ipynb` provides that verification. It's the last line of defense against "maybe the code was different then."
