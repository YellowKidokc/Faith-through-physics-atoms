# run_all.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Role:** Master runner — executes all notebooks in the project

---

## What It Is

The one-button execution notebook. Running all cells in `run_all.ipynb` executes the complete Theophysics test suite — all JAX field theory tests, all biblical empirical tests, all chart generation — in a single Colab session.

This is the artifact that makes the claim "just run it" possible. Anyone with a Google account can open this notebook and reproduce the complete proof.

---

## Execution Sequence

The runner executes in this order:
1. `config.ipynb` / `theophysics_core.py` — load constants
2. `master_equation.ipynb` — initialize the MasterEquation class
3. `chi_field.ipynb` — initialize the ChiFieldSolver
4. JAX Field Theory suite (Tests 1A, 1B, 2A, 2B, 3, 4, 5) — all field theory tests
5. Biblical Empirical suite (Tests 03-09) — all biblical tests
6. `generate_all_charts.ipynb` — produce all visualizations
7. `version_manager.ipynb` — compute checksums and verify reproducibility

Total runtime on a free Colab CPU: approximately 8-12 minutes.
Total runtime on a Colab GPU (T4): approximately 3-5 minutes.

---

## What It Produces

On completion:
- Full console output with pass/fail for every test
- JSON result files for each test
- PNG chart files in `/content/charts/`
- `test_suite_summary.json` with timing and overall pass rate
- SHA256 checksum confirming exact reproducibility

---

## Interpretation

`run_all.ipynb` is the proof that the framework is reproducible by anyone, not just its author. The ability to run the complete proof from a fresh Colab instance, with no prior installation, using only the notebooks in this repository, is the computational equivalent of repeatable experiment protocol.

"Run this and see for yourself" is the most powerful statement in science. `run_all.ipynb` makes that statement possible for the Theophysics framework.
