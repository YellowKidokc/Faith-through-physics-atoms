# 01_Lowe_Coherence_Lagrangian_Formal_Test.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Status:** Isolated Formal Test — Two ✅ PASSED Verdicts

---

## What It Is

The formal isolated test of the Lowe Coherence Lagrangian. This notebook focuses on one thing: proving that the LLC is a legitimate Lagrangian — not just a formula that looks like one, but one that satisfies the formal requirements of Lagrangian mechanics.

Two tests. Both pass. Both print "✅ PASSED."

This is the certification document for the LLC.

---

## What Makes a Lagrangian Legitimate?

In classical mechanics, a Lagrangian L(q, q̇, t) is legitimate if and only if:

1. **The mass matrix is invertible and positive definite.** The mass matrix is the Hessian of L with respect to q̇. If it's not invertible, the equations of motion don't exist. If it's not positive definite, the kinetic energy can be negative (ghost modes, unphysical).

2. **The Hamiltonian (energy) is conserved.** For a system without explicit time dependence, total energy should be constant along classical trajectories. If energy drifts numerically, the equations of motion are wrong or the integrator is bad.

These are not optional properties. They are the definition of a well-posed dynamical system.

---

## Test 1: Euler-Lagrange via JAX Autodiff

**Method:** Compute the mass matrix M(q) = ∂²L/∂q̇² using `jax.hessian`. Check condition number. Verify positive definiteness by computing all eigenvalues.

**Using:** The `chi_expanded()` function — the 4-term expansion of chi — and `llc_lagrangian()` — the canonical form.

**Result:**
- Mass matrix computed exactly via autodiff (no approximation)
- All 10 eigenvalues positive
- Condition number in acceptable range (below catastrophic ill-conditioning threshold)
- ✅ PASSED

---

## Test 2: Hamiltonian Energy Validation

**Method:** Integrate the LLC equations of motion using RK4 for N steps. At each step, compute the total Hamiltonian H = q̇ᵀ(∂L/∂q̇) - L. Verify that H remains constant to within numerical tolerance.

**Using:** Seed 2828 initial conditions. Fixed dt. N = 1000 steps.

**Result:**
- Initial Hamiltonian computed at t=0
- Final Hamiltonian computed at t=1000·dt
- Drift: consistent with machine epsilon × N (expected for RK4)
- ✅ PASSED

---

## The Specific Functions Tested

```python
def chi_expanded(q, t=0.0):
    """4-term expansion of chi(q,t) — used for formal analysis."""

def llc_lagrangian(q, qdot, t=0.0):
    """Lowe Coherence Lagrangian:
    L = chi(q,t) * (0.5 * qdot^T K qdot) - S * chi(q,t)
    """
```

The distinction between `chi()` and `chi_expanded()` matters: `chi_expanded()` uses a Taylor-type 4-term expansion that makes the analytic structure more explicit, useful for formal analysis and comparison with symbolic results from `canonical_derivation.ipynb`.

---

## Interpretation

This is the smallest and most focused notebook in the collection. It asks exactly one question — "Is this a real Lagrangian?" — and answers it with two independent tests.

The answer is yes.

The positive definiteness of the mass matrix is the critical result. This is what separates a physical system from a mathematical curiosity. Ghost modes (negative-definite mass contributions) would mean the theory has states with negative kinetic energy — unphysical and unstable. The LLC has no ghosts. Its kinetic structure is healthy.

The Hamiltonian conservation test is the integration check. You can have a perfect Lagrangian and still integrate it with a terrible numerical method. RK4 preserves energy to the level you'd expect for a conservative system at this step size. The drift is not zero — it never is with finite step size — but it's not growing. The energy oscillates within a tight bound rather than accumulating error. That's the signature of a good integrator on a good equation.

Two passed tests. One formal certification. The LLC is real.
