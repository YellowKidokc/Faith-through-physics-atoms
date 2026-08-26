# test_base.py

**Category:** Python Script  
**Author:** David Lowe (POF 2828)  
**Role:** Base class infrastructure for the test suite  
**Usage:** Import in test notebooks — provides shared setup, utilities, constants

---

## What It Is

The test infrastructure foundation. Every test in the Biblical Empirical Suite and the JAX Field Theory Suite builds on a shared set of utilities, constants, and validation helpers. Rather than duplicating this code in 16 different notebooks, `test_base.py` provides it once.

This is the same architectural decision as `theophysics_core.py` for parameters: centralize shared infrastructure, eliminate duplication, ensure consistency.

---

## What It Provides

**PhysicalConstants dataclass:**
The canonical set of physical and framework constants, made available as typed fields:
```python
c = 299792458.0         # Speed of light (m/s)
hbar = 1.054571817e-34  # Reduced Planck constant
G = 6.674e-11           # Gravitational constant
k_B = 1.380649e-23      # Boltzmann constant
H0 = 70.0               # Reference Hubble constant (km/s/Mpc)
xi = 0.01               # Chi-gravity coupling strength
m_s = 1e-33             # Soul field mass (kg)
lambda_coupling = 1e-15 # Chi-gravity vertex coupling
f_critical = 0.35       # Critical faith threshold
```

**Test scaffolding:**
- `setup_jax()` — configures JAX for float64, sets seed 2828, verifies device availability
- `tolerance_check(computed, expected, rtol, atol)` — standardized tolerance comparison with logging
- `spearman_test(x, y)` — Spearman rank correlation with significance
- `compression_complexity(text)` — zlib-based Kolmogorov complexity proxy
- `save_results(test_name, results_dict)` — JSON output to standard path

**Logging:**
- `TestLogger` class that records pass/fail for each assertion, computes suite statistics, and outputs the final scorecard format used in THEOPHYSICS_COMPLETE_COLAB.ipynb

---

## Why a Base Class?

Without `test_base.py`, each of the 16 tests would need to:
1. Independently define PhysicalConstants (risk of inconsistency)
2. Implement its own tolerance comparison (risk of inconsistent thresholds)
3. Implement its own Spearman test (risk of implementation variation)
4. Implement its own result logging (inconsistent output format)
5. Independently set up JAX (risk of different precision settings)

With `test_base.py`, all of these are guaranteed consistent. The `f_critical = 0.35` value appears in every quantum faith test because `test_base.py` says it's 0.35. The tolerance thresholds are the same in every test because `tolerance_check()` defines them once.

This is how you build a test suite that proves something rather than just producing numbers.

---

## Interpretation

`test_base.py` is invisible infrastructure — the kind of code that you only notice when it's absent. When it works, tests run consistently. When it's missing, tests drift apart.

The most important thing `test_base.py` does is enforce consistency across 16 independent tests by 1 author over several months of development. A project that starts each test from scratch will silently diverge — different tolerances, different precision settings, different constant values. A project with a shared base stays coherent.

That coherence is what makes the final scorecard meaningful. When all 16 tests pass against the same tolerance standards, the same constants, and the same infrastructure, "16/16 PASSED" means something real. Without a shared base, it might mean 16 different definitions of "pass."
