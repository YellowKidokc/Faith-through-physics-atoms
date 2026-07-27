# generate_all_charts.ipynb

**Category:** Google Colab Notebook  
**Author:** David Lowe (POF 2828)  
**Role:** Master chart generation — all visualizations from one execution

---

## What It Is

The one-stop chart generator. Rather than running 10 different notebooks to produce 10 different visualizations, `generate_all_charts.ipynb` imports all the data and generates the complete visualization suite in one session.

This is the notebook to run when you need publication-ready output.

---

## Charts Generated

**Field theory visualizations:**
- Chi-field 1+1D space-time evolution (colormap: space on x, time on y, chi-value as color)
- Hubble gradient sigmoid H₀(z) with observational data points overlaid
- Galaxy rotation curve comparison (observed vs. chi-field prediction vs. dark matter)
- Maxwell mirror E-K subspace oscillation plot
- Kinetic matrix heatmap with symmetry pair highlights

**Lagrangian mechanics visualizations:**
- Energy conservation plot (Hamiltonian over time — should be flat)
- Mass matrix eigenvalue spectrum
- LLC phase portrait (q vs. q̇ trajectories)
- Sensitivity sweep bars (∂chi/∂q_i for each variable)
- 60-run stress sweep pass rate distribution

**Biblical empirical visualizations:**
- Complexity growth across eras (Test 03) with Spearman ρ annotation
- Grace response curves (Test 04) with exponential fit overlay
- Sin vs. righteousness complexity comparison (Test 06) as box plot
- Community coherence scaling (Test 07) with non-linear fit
- Revelation density S-curve (Test 08) with logistic fit
- Strategy comparison table (Test 09) with force-by-force color coding

**Summary visualization:**
- Final scorecard dashboard (identical to COLAB_MASTER output)

---

## Output Format

All charts are saved to `/content/charts/` in PNG format at 300 DPI — print-quality resolution suitable for academic publication. The directory structure:

```
/content/charts/
  field_theory/
  lagrangian/
  biblical/
  summary/
```

---

## Interpretation

This notebook is the production pipeline. When the research is ready for publication — website, paper, presentation — this is the one to run. It produces every visual in the project, consistently formatted, consistently named, consistently sized.

The decision to have a separate chart-generation notebook (rather than generating charts inline in each test notebook) is another example of clean design: keep the tests clean, keep the visualizations clean, don't intermix them. The tests prove results. The chart generator displays them.

For website integration specifically, the `/content/charts/` output would feed directly into a gallery or interactive display.
