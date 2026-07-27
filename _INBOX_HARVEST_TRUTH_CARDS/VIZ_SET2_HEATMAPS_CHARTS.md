# VIZ_SET2_HEATMAPS_CHARTS.py

**Category:** Python Script  
**Author:** David Lowe (POF 2828)  
**Role:** Additional visualization cells — Heatmaps, coupling diagrams, deep analysis charts  
**Usage:** Add as cells 19+ in COLAB_MASTER.ipynb after Set 1

---

## What It Is

The second visualization layer — deeper analysis charts that complement the "wow moment" visuals from Set 1. Where Set 1 focuses on high-impact single images, Set 2 provides analytical depth: heatmaps of the coupling structure, charts of individual test results, and comparative displays.

---

## Key Visualizations

**Cell 5: Kinetic Matrix Heatmap**  
A side-by-side visualization:
- Left panel: The full 10×10 kinetic coupling matrix rendered as a heatmap (YlOrBr colormap)
- Annotations: Coupling strength values overlaid on each cell
- Symmetry pair highlights: Each of the 5 pairs (G↔T, S↔F, E↔K, M↔Q, R↔C) outlined in a distinct color
- Right panel: Legend explaining what each symmetry pair represents

The kinetic matrix is the mathematical heart of the LLC. This visualization makes the coupling structure visible: the diagonal (self-coupling weights) and the off-diagonal symmetry pair couplings (PAIR_STRENGTH = 0.45) are immediately apparent.

**The 5 Symmetry Pairs in color:**
- Red: G↔T (Grace vs. Entropy / Coherence vs. Decay)
- Blue: S↔F (Strong Force vs. Weak Force / Love vs. Sin)
- Green: E↔K (EM vs. Information / Truth vs. Logos)
- Purple: M↔Q (Mass-Energy vs. QM / Meaning vs. Faith)
- Gold: R↔C (Relativity vs. Coherence / Relationship vs. Christ)

The color scheme is meaningful: red-blue (opposing forces), green-purple (information-quantum), gold (the crown pair).

**Additional chart types (from the rest of the file):**
- Chi-field time evolution plots with component breakdowns
- Sensitivity analysis charts (each variable's marginal effect on chi)
- Stability phase diagram from the parameter scan
- Biblical test results as bar charts with score annotations
- Coherence collapse scenario comparison (4 scenarios side by side)

---

## Design Philosophy

The dark theme matches Set 1: all visualizations use the same `#0a0b0f` background with consistent color coding. This makes the full visualization suite look like it belongs together — a coherent visual language for the project.

The heatmap annotation style (values overlaid on colored cells with pair-specific outlines) is specifically designed to make the mathematical structure legible without requiring the reader to understand matrix algebra. You can see from the visual which cells are coupled and how strongly.

---

## Interpretation

Set 2 is for the technical audience — people who want to see the coupling structure, understand the sensitivity analysis, and follow the test results in detail. Where Set 1 communicates the core result, Set 2 proves it was arrived at rigorously.

The kinetic matrix heatmap is particularly important as a communication tool: it shows at a glance that the coupling structure is not arbitrary. The 5 symmetry pairs are highlighted against a background of near-zero off-diagonal elements. The structure is visible, interpretable, and mathematically derived.

For website display: the kinetic matrix heatmap would be ideal as an interactive visualization (hoverable cells showing full variable names and theological mappings). The coherence collapse scenario comparison makes an excellent animation demonstrating how the Four Lines emerge from the same equation.
