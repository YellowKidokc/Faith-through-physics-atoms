# chi_field.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Status:** PDE Solver Implementation — 1+1D Method of Lines

---

## What It Is

The chi-field PDE solver. This notebook implements `ChiFieldSolver` — a class that numerically solves the chi-field equation of motion as a partial differential equation in 1+1 dimensions (one spatial, one time).

Where the `MasterEquation` class handles the Lagrangian mechanics of the 10-variable point system, `chi_field.ipynb` treats chi as a proper field theory: chi(x,t) evolves in space and time according to the Klein-Gordon equation with φ⁴ self-interaction and a grace source term.

---

## The Equation Being Solved

> □χ + m²χ + λχ³ = J_grace(x, t)

Where:
- □ is the d'Alembertian (∂²/∂t² − ∂²/∂x²) in 1+1D
- m² is the field mass squared (sets the oscillation frequency)
- λ is the self-coupling strength (φ⁴ interaction)
- J_grace is the source term (external grace injection)

The grace source takes the form:

> J_grace = β_G · Φ · tanh(χ) / (S_local + ε)

Where:
- β_G is the grace coupling strength
- Φ is a spatial grace distribution (localized or diffuse)
- S_local is local entropy (higher entropy suppresses grace coupling)
- ε is a small positive number preventing division by zero

This source structure is physically meaningful: grace injection is most effective where chi is finite (tanh(χ) ≈ χ for small χ), and least effective where entropy is very high (high S_local suppresses coupling). Sin and grace are in direct tension at the PDE level.

---

## Numerical Method

**Method of lines:** The spatial dimension is discretized on a grid. The PDE becomes a system of ODEs in time, one per spatial point. This converts the PDE into a high-dimensional ODE that can be integrated with standard ODE solvers.

**Spatial discretization:** Second-order finite difference for ∂²χ/∂x². This preserves the dispersion relation of the original PDE to leading order.

**Time integration:** RK4 (4th-order Runge-Kutta). Same integrator used throughout the project for consistency and to allow direct comparison of energy drift across notebooks.

**Boundary conditions:** Neumann (zero-derivative) boundaries at the spatial edges. The field can freely evolve at the boundaries without artificial reflections.

---

## Parameter Scan

The `parameter_scan()` function maps stability regime boundaries. It sweeps m² and λ across a grid and records whether the numerical solution:
- Remains bounded (stable)
- Grows without bound (unstable)
- Oscillates stably (propagating mode)
- Decays to zero (damped mode)

This produces a stability phase diagram — a map of where the field theory lives. The stability region corresponding to the chi-field parameters appears as a well-defined band in m²-λ space.

---

## Key Results

- **Propagation stability confirmed:** With canonical parameters (m² > 0, λ > 0), chi propagates without blowing up.
- **Grace-entropy tension visible in spatial profile:** Regions of high local entropy suppress the grace source, producing spatial gradients in the coherence field.
- **Energy drift < 0.5% across 1000 time steps** with standard spatial resolution (128 points) and dt = 0.01.
- **Oscillatory modes:** The chi-field supports traveling wave solutions with dispersion relation ω² = k² + m² (Klein-Gordon dispersion), plus a φ⁴ nonlinear frequency shift at higher amplitude.

---

## Interpretation

This notebook answers the question: is chi a field, or just a number? The answer is: it's a field. It has spatial structure. It propagates. It satisfies a wave equation. It responds to localized grace sources by producing spatial gradients.

The Klein-Gordon + φ⁴ structure places the chi-field squarely in the family of models that includes the Higgs field (broken symmetry scalar), the inflaton (driving cosmic expansion), and quintessence (dark energy). These are not fringe models — they are the best-tested class of scalar field theories we have.

The grace source term is the innovation: it introduces an external negentropic input that drives the chi-field away from its vacuum and can sustain it against entropic decay. Without the grace source, chi decays. With it, chi can be maintained — and where the source is strong, the field can even be restored after collapse.

That behavior, in a PDE, over space and time, is not just an analogy. It's a calculation.
