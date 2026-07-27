# run_biblical_tests.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Role:** Biblical Empirical Suite runner — Tests 03-09 only

---

## What It Is

The isolated biblical test runner. Executes only the Biblical Empirical Suite (Tests 03 through 09) without running the JAX Field Theory tests. Useful when you want to verify the biblical side of the framework independently of the physics computations.

---

## Why Separate Runners for Each Suite?

The two suites test fundamentally different things:
- **JAX Field Theory:** Tests physical mathematics — PDE stability, cosmology, information theory
- **Biblical Empirical:** Tests historical patterns in biblical data — complexity, scaling, constraint satisfaction

Separating the runners allows:
- Independent verification of each suite
- Running only the biblical tests on machines without GPU acceleration (the JAX tests benefit more from GPU)
- Debugging biblical test issues without re-running the full field theory suite
- Presenting the biblical evidence separately for audiences more interested in that context

---

## Output

Running `run_biblical_tests.ipynb` produces:
- PASS/FAIL console output for Tests 03-09
- Individual result JSON files (test03_results.json through test09_results.json)
- `test_suite_summary.json` for the biblical suite
- Total runtime: approximately 2.5 seconds

---

## Interpretation

The biblical empirical tests are the most surprising results in the collection for many audiences. Physicists expect the chi-field PDE to be stable — that's what well-formed field theories do. But finding Spearman ρ = 1.0 across 2,500 years of biblical history, or finding that the biblical strategy uniquely satisfies six simultaneous constraints, is unexpected by almost any prior.

Having a standalone runner for these tests makes them accessible to audiences who want to start from the historical evidence rather than the physics. Run `run_biblical_tests.ipynb`, see 7/7 PASSED, read the individual test reports, engage with what that means — without needing to understand Lagrangian mechanics first.

The suite is designed to be modular. The runner respects that design.
