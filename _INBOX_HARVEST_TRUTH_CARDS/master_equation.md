# master_equation.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Role:** Core Computational Engine  
**Status:** Modular Class Definition — Imports from config.py

---

## What It Is

The engine room. `master_equation.ipynb` defines the `MasterEquation` class — the core computational object that all other notebooks import, instantiate, and test. It is not a proof notebook by itself; it is the machine that the proofs run on.

Think of it as the physics library for Theophysics. Where `theophysics_core.py` defines constants and variable metadata, `MasterEquation` defines the full computation — chi, energy, integration, sensitivity, gradients, component control.

---

## MasterEquation Class — What It Does

**Core field computation:**
- `chi(q, t)` — evaluates the coherence field for a given variable state and time
- `chi_with_breakdown(q, t)` — returns chi plus per-component contributions
- `chi_4term(q, t)` — 4-term expansion of chi for analytical work

**Lagrangian mechanics:**
- `lagrangian(q, qdot, t)` — evaluates the Lowe Coherence Lagrangian
- `equations_of_motion(q, qdot, t)` — computes accelerations via Euler-Lagrange
- `energy(q, qdot, t)` — total energy (kinetic + potential)
- `mass_matrix(q, t)` — 10×10 Hessian of kinetic energy (required to be positive definite)

**Numerical integration:**
- `integrate_rk4(q0, qdot0, t_span, n_steps)` — 4th-order Runge-Kutta integrator for time evolution

**Autodifferentiation (JAX):**
- `gradient_chi(q, t)` — gradient of chi with respect to all 10 variables
- `hessian_chi(q, t)` — full 10×10 Hessian of chi

**Analysis tools:**
- `sensitivity_sweep(q_base, variable_index, n_points)` — scans the effect of varying one variable while holding others fixed
- `component_report(q, t)` — print table of all 10 component contributions

**Component control:**
- `disable_component(index)` — set a component's contribution to zero
- `enable_component(index)` — restore a component
- `(these are the tools used in the Veto Property test)`

---

## The Architecture Decision

The choice to use JAX (rather than numpy or PyTorch) was deliberate. JAX provides:

1. **`jax.grad`** — automatic differentiation for exact gradients
2. **`jax.hessian`** — exact second derivatives for the mass matrix
3. **`jax.jacfwd`** — Jacobian computation for the Euler-Lagrange equations
4. **`jit` compilation** — GPU/TPU acceleration when available in Colab
5. **`float64` precision** — essential for energy drift measurements at 10⁻⁹ level

The mass matrix computation in particular benefits from JAX autodiff: rather than approximating the Hessian numerically, it is computed exactly. This is what allows energy conservation to be verified to 9 decimal places.

---

## Configuration

The class imports from `config.py` (or `config.ipynb` in the notebook version):
- `VAR_WEIGHTS = [1.0, 0.8, 1.2, 0.6, 1.0, 0.7, 0.5, 0.9, 1.1, 1.3]`
- `SYMMETRY_PAIRS = [(0,4), (3,8), (2,5), (1,7), (6,9)]`
- `PAIR_STRENGTH = 0.45`
- `CONFINE_STRENGTH = 0.01`
- Random seed: `2828`

These values are not arbitrary — PAIR_STRENGTH = 0.45 is specifically chosen to be subcritical (below the 0.64 stability boundary), ensuring the kinetic matrix remains positive definite across operating points.

---

## Interpretation

This notebook is the foundation. If you want to understand any test result in the collection, you eventually come back here. The MasterEquation class is what makes the framework reproducible: same inputs, same code, same outputs. Every time.

The architecture is clean enough that each method can be tested independently. `chi()` doesn't require `integrate_rk4()` to work. `mass_matrix()` doesn't require `sensitivity_sweep()`. This modularity is what allows the stress tests in `Family_Lagrangian_Workbench.ipynb` to isolate specific behaviors and the Wolfram Gauntlet to test specific sub-components.

A framework that can be tested at the component level is a framework that can be trusted at the system level.
