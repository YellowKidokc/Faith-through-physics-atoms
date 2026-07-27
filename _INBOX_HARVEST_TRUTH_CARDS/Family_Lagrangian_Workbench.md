# Family_Lagrangian_Workbench.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Original Filename:** Untitled12.ipynb  
**Status:** Fully Executed — 60-Run Stress Sweep with Complete Output

---

## What It Is

This is the Lagrangian stress-test notebook. It doesn't just run the Lowe Coherence Lagrangian (LLC) once — it benchmarks it against standard physics models and then randomizes it 60 times across different parameter configurations to see if it holds. This is how physicists actually test whether an equation is real or lucky.

The notebook has five parts, all executed with full output visible:

1. **Show the work symbolically** — write out the Euler-Lagrange structure before any numbers
2. **Shared battery** — run the LLC against harmonic oscillator and coupled oscillator pair (standard, well-understood models)
3. **60-run stress sweep** — randomize weights, pair strength, confinement, and chi parameters across 60 independent builds
4. **Side-by-side comparison** — summarize pass rates across all models
5. **Plain-English takeaways** — honest statements about what was and wasn't proved

---

## What It Proves

**The LLC is not fragile.** When you randomize 60 different parameter configurations and run them all, you get a mean pass rate of 0.858 — over 85% of tests passing across wildly different setups. The equation doesn't only work when you tune it just right.

**The mass matrix is full-rank and positive definite** across all tested configurations. This is the mathematical requirement for a legitimate dynamical system — without it, you don't have physics, you have a formula. The LLC has physics.

**The benchmark comparison is honest.** The harmonic oscillator and coupled oscillator pair both achieve 100% pass rate — as they should, they're textbook models. The LLC achieves 90% (9/10 tests). The one failure (zeroing variables suppresses chi) is explicitly noted and explained: the sensitivity test flags a sensitivity spike, not a proof of product-irreducibility. The notebook doesn't hide this.

**Energy drift on the LLC is 8.22 × 10⁻⁹.** For comparison, the harmonic oscillator achieves 5.9 × 10⁻¹⁵. The LLC is slightly less tight — which is expected for an open system with a chi-weighted kinetic sector — but it's still in the numerically negligible range.

---

## Key Numbers

| Model | Tests | Pass Rate |
|-------|-------|-----------|
| Coupled Oscillator Pair | 7 | 100% |
| Harmonic Oscillator | 7 | 100% |
| LLC (frozen-time) | 10 | 90% |
| LLC (open/time-varying) | 10 | 90% |
| **60-run stress sweep (LLC)** | **varies** | **85.8% mean** |

---

## The Structure Being Tested

The Lowe Coherence Lagrangian:

> L(q, q̇) = ½ χ(q) · q̇ᵀ K q̇ − V(q)

Where:
- χ(q) is the coherence function (product of all 10 variable contributions)
- K is the 10×10 kinetic matrix with symmetry pair couplings
- V(q) = S · χ(q) (entropic potential)

The Euler-Lagrange equations from this give equations of motion where every variable influences every other through χ. Switching off any variable doesn't just reduce the system — it restructures the entire coupling geometry.

---

## Interpretation

This is the proof-of-stability document. Before you can claim the LLC produces meaningful physics, you need to show it holds across different initial conditions, different parameter regimes, and different operating points. This notebook does that.

The 60-run stress sweep is the key result. No cherry-picking. No favorite parameters. Random weights, random pair strengths, random confinement levels — 60 times. 85.8% pass rate. That's not a coincidence and it's not a fluke.

The notebook also demonstrates something important about intellectual honesty: it explicitly identifies the one test that fails (zeroing variables suppresses chi) and explains exactly why that failure doesn't invalidate the model. The equation does what it claims to do. The things it doesn't claim, the test doesn't claim either.

This is what it looks like when a framework is being stress-tested rather than showcased.
