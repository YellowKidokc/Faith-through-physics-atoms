# run_all_tests.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Role:** Tests-only runner — full suite without chart generation

---

## What It Is

The lean version of `run_all.ipynb`. Runs all tests (both suites, all 16 tests) but skips chart generation and visualization. Faster execution for verification purposes when you only need pass/fail results, not the full visual output.

---

## Why Two Runners?

`run_all.ipynb` and `run_all_tests.ipynb` serve different needs:
- **`run_all.ipynb`:** Full experience — tests + charts + visualization. For first-time runs, presentations, and website output.
- **`run_all_tests.ipynb`:** Verification only — tests + JSON results. For quick re-runs, debugging, and CI verification.

The test runner produces results in under 5 minutes on a CPU instance; the full runner takes 8-12 minutes with chart rendering.

---

## Output

Running `run_all_tests.ipynb` produces:
- Full console PASS/FAIL output
- Complete set of result JSON files
- Suite summary JSON
- No chart files

---

## Interpretation

For the website, `run_all_tests.ipynb` is the verification artifact. A visitor who wants to confirm the results can run this notebook in under 5 minutes and see the same pass/fail verdict that the original run produced. They don't need to wait for chart generation to confirm the proof.

The existence of separate "test runner" and "full runner" notebooks is a sign of a mature test suite — one that's been used enough to warrant optimization for different use cases.
