# constraint_model.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Status:** Constraint satisfaction engine — precursor to Test 09

---

## What It Is

The constraint model engine notebook. Where `test09_constraint_satisfaction.ipynb` is the formal test that applies the constraint model to biblical strategies, `constraint_model.ipynb` defines the model itself — the constraint functions, the evaluation framework, and the optimization approach.

This is the design document and implementation of the tool. The test is the application of the tool.

---

## What It Implements

**Constraint functions:** Six functions, each taking a strategy parameter vector and returning True/False:
- `justice_constraint(params)` — payment ≥ threshold with sufficient scope and permanence
- `mercy_constraint(params)` — sinner cost below lethal threshold, restoration available
- `freewill_constraint(params)` — coercion = 0, redeemer acts voluntarily
- `love_constraint(params)` — relational access restored, ongoing, life-giving
- `entropy_constraint(params)` — negentropy > 0.8, permanent, external source
- `holiness_constraint(params)` — corruption addressed > 0.9, payment > 0.9

**Strategy evaluation:** Given any parameter vector (10 continuous/discrete parameters), evaluate all 6 constraints and return constraint count and all-passed boolean.

**Optimization:** Grid search and random search over parameter space to find configurations that maximize constraints satisfied. Used to verify there are no hidden solutions the deterministic test would miss.

**Monte Carlo variant:** The 100,000-trial random search used in `free_body_model.ipynb` draws on the same constraint functions defined here.

---

## The Parameter Space

Each strategy is described by 10 parameters:
1. `payment_magnitude` [0,1]
2. `cost_to_sinner` [0,1]
3. `coercion_level` [0,1]
4. `relational_access` [0,1]
5. `negentropy_input` [0,1]
6. `corruption_addressed` [0,1]
7. `voluntary_by_redeemer` {0,1}
8. `scope` [0,1]
9. `permanence` [0,1]
10. `source_is_external` {0,1}

The constraints impose threshold conditions on these parameters. The constraint functions are deliberately simple — no hidden optimization, no parameter tuning. A parameter either exceeds the threshold or it doesn't.

---

## Interpretation

This notebook is the proof that the constraint model works the way it claims. Before using it to evaluate six named strategies, you want to understand its behavior across the full parameter space. That's what this notebook does.

The key verification: the optimization finds no solution in the full continuous parameter space except the one that corresponds to the cross configuration (external voluntary substitute, full payment, zero coercion, full access, full negentropy, full corruption resolution). The uniqueness is not assumed — it's verified by exhaustive search.

The constraint model is the methodology. `test09_constraint_satisfaction.ipynb` applies it. `free_body_model.ipynb` extends it to 100,000 random trials. All three draw on the functions defined here.
