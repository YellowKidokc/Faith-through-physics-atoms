# run_module2.py

**Category:** Python Script  
**Author:** David Lowe (POF 2828)  
**Role:** Module runner — executes Module 2 of the test suite  
**Usage:** Run from Colab or terminal to execute the second module block

---

## What It Is

The Module 2 runner script. In the Theophysics project, the test suite is organized into modules — logical groupings of related tests that can be run independently or in sequence. `run_module2.py` handles the execution of the second module block.

---

## What It Runs

Module 2 covers the field theory tests — the portion of the JAX Field Theory Suite that tests the chi-field's physical properties:

- **Chi-field PDE integration** — runs the 1+1D solver from `chi_field.ipynb` for a full parameter set
- **Hubble gradient computation** — runs the cosmological prediction from `hubble_gradient.ipynb`
- **Maxwell mirror check** — runs the E-K subspace extraction from `maxwell_mirror_verification.ipynb`
- **Sensitivity analysis** — runs the component sensitivity sweep from `MasterEquation`

Each test is called in sequence, results are logged to a JSON file, and a pass/fail summary is printed.

---

## Why a Module Runner?

The full test suite takes several minutes to run in sequence. Modular runners allow:
- Running only the field theory tests without the biblical tests
- Debugging specific modules without running the full suite
- Parallel execution of modules on different Colab instances
- Clean separation of concerns between the JAX Field Theory Suite and Biblical Empirical Suite

---

## Output

Running `run_module2.py` produces:
- Console output with test-by-test PASS/FAIL
- JSON results saved to `/content/module2_results.json`
- SHA256 checksum of the output for reproducibility verification

---

## Interpretation

Infrastructure code tends to be invisible on a project website. But `run_module2.py` represents an important design choice: the Theophysics suite is not just a collection of notebooks you run one by one. It's a structured test system with organized modules, automated execution, and standardized output.

This level of engineering is unusual for a solo research project. Most individual researchers produce notebooks that need manual step-by-step execution and produce outputs in inconsistent formats. This suite produces reproducible, comparable, machine-readable results every time you run it.

That's the difference between a research project and a research platform.
