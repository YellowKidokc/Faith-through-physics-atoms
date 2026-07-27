# solve_master_equation.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Status:** ODE solver for the master equation system

---

## What It Is

The dedicated ODE solver for the master equation. While the `MasterEquation` class includes `integrate_rk4()` as a method, `solve_master_equation.ipynb` provides a fuller, standalone solver environment — with more control over integration parameters, adaptive step sizing, and output formatting.

---

## What It Solves

The system being integrated is the Euler-Lagrange equations derived from the Lowe Coherence Lagrangian:

> M(q)·q̈ + C(q, q̇)·q̇ + ∇V(q) = F_external(t)

Where:
- M(q) is the 10×10 mass matrix (chi-weighted kinetic metric)
- C(q, q̇) is the Coriolis-like term (from chi's dependence on q)
- ∇V(q) is the gradient of the entropic potential
- F_external(t) is external forcing (grace injection over time)

This is a second-order 10-dimensional nonlinear ODE system. Written as a first-order system in (q, q̇), it becomes 20-dimensional.

---

## Solver Features

**Step size control:** Adaptive step size based on energy drift per step. If energy drift exceeds threshold, step is rejected and retried with smaller dt. This ensures accuracy across all operating points, not just the canonical ones.

**Trajectory output:** Full (q(t), q̇(t)) trajectory stored at each time step, with chi(t) computed inline. Output includes:
- Time array
- 10 position trajectories q_i(t)
- 10 velocity trajectories q̇_i(t)
- Chi-field value χ(t)
- Hamiltonian H(t) (energy conservation check)

**Grace profiles:** Selectable grace input time profiles:
- Constant grace
- Exponential decay
- Step function (on/off)
- Sinusoidal modulation
- Custom function

---

## Key Results

For canonical parameters (seed 2828):
- Energy drift per 1000 steps: < 10⁻⁸
- All 10 variable trajectories remain bounded
- Chi-field χ(t) shows expected convergence behavior
- Grace profiles produce the expected "Four Lines" behavior pattern

---

## Interpretation

This is the numerical heart of the time-evolution side of the project. The chi-field PDE solver (`chi_field.ipynb`) handles spatial structure. This solver handles the Lagrangian mechanics time evolution of the 10-variable system.

The adaptivity is the key feature: by adjusting step size to maintain energy conservation, the solver gives trustworthy results even near operating points where the equations are stiff (high curvature in the mass matrix or potential). Stiff ODEs are where naive fixed-step integrators fail; adaptive solvers handle them correctly.

The grace profile selector makes this notebook a tool for exploring different "scenarios" — what happens to the chi-field if grace is constant? If it decays? If it's applied suddenly? The answers appear in the trajectory plots. The Four Lines visualization in `COLAB_MASTER.ipynb` was generated using this solver's output.
