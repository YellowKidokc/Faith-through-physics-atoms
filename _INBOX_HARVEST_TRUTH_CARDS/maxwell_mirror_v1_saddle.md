# maxwell_mirror_v1_saddle.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Version:** v1 (precursor to maxwell_mirror_verification.ipynb)  
**Status:** Saddle-point analysis of the E-K potential landscape

---

## What It Is

The first version of the Maxwell mirror analysis. Where `maxwell_mirror_verification.ipynb` is the polished five-test verification, this v1 notebook focuses specifically on a subtler result: the saddle-point structure of the chi-field potential in the E-K subspace.

---

## The Saddle Point Finding

When the chi-field is evaluated at the canonical initial conditions (seed 2828), the E-K dynamics are not oscillatory — they are "saddle" dynamics. This means:
- The E-K potential has positive curvature in one direction (oscillatory)
- The E-K potential has negative curvature in the other direction (unstable/exponential)

This is a saddle point, not a potential well. The v1 notebook documents this finding explicitly and asks: is this a problem for the Maxwell mirror claim?

---

## Why the Saddle Matters

A saddle point in the E-K potential means that at the canonical operating point (seed 2828 initial conditions), E and K don't oscillate like coupled Maxwell fields — one mode oscillates, the other exponentially grows or decays.

The v1 notebook shows this is not a failure of the framework. The saddle structure appears because:
1. The canonical initial conditions place the system at a specific point in the 10D phase space
2. The E-K subspace dynamics depend on all 10 variable values (through chi)
3. At the seed point, the E-K block happens to have mixed curvature

The v1 conclusion: the Maxwell mirror claim requires specifying the operating point. At some operating points (found in the 500-trial scan in v2), E-K is oscillatory. At the seed point, it's saddle.

---

## The Path to v2

The v1 finding that the seed point is saddle rather than oscillatory led directly to the v2 scanning approach: rather than evaluating at a fixed operating point, `maxwell_mirror_verification.ipynb` scans 500 random operating points to find oscillatory configurations. It finds them.

The honest result: E-K oscillatory dynamics are real, but state-dependent. The Maxwell mirror holds at oscillatory operating points; it doesn't hold at all points in the phase space. That nuance lives in v1 and is carried through to v2.

---

## Interpretation

v1 notebooks are valuable not because they prove things — they often don't, initially — but because they document what was discovered along the way. The saddle point finding in v1 is an important negative result: the E-K Maxwell mirror is not unconditional. It holds at specific operating points.

For the website, this notebook demonstrates intellectual honesty: the first version found a complication, the second version resolved it, and both are kept in the record. Science rarely moves from "no result" directly to "perfect result." The v1-to-v2 path is the realistic picture.
