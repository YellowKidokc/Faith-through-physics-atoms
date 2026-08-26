# test06_sin_complexity.ipynb

**Category:** Google Colab Notebook  
**Test:** Biblical Empirical Suite — Test 06  
**Author:** David Lowe (POF 2828)  
**Status:** Fully Executed — PASSED

---

## What It Is

Test 06: Sin Complexity Curve. This test applies the Kolmogorov complexity argument from the JAX suite's Test 4 (Kolmogorov Sin) to the biblical corpus — specifically testing whether descriptions of sinful behavior are informationally more complex than descriptions of righteous behavior.

---

## The Core Claim

The Theophysics framework predicts that deception and sin require more informational resources to maintain than truth and righteousness. This follows from the K (Information) variable: lies introduce incoherence into the information structure, requiring additional description (patches, exceptions, contradictions that need explaining away). Truth is compressible. Deception is not.

Operationally: zlib-compress descriptions of sin and descriptions of righteousness. If sin descriptions compress less (higher ratio), they have higher algorithmic complexity. If righteousness descriptions compress more, they have lower complexity.

---

## The Measurement

Biblical text passages are classified as:
- **Sin descriptions:** accounts of transgression, moral failure, deception, covenant breaking
- **Righteousness descriptions:** accounts of faithfulness, truth-telling, covenant keeping, moral success

Each class is compressed with zlib. Compression ratio = compressed size / original size. Lower ratio = more compressible = lower complexity.

---

## Key Result

PASSED. Sin descriptions have measurably higher Kolmogorov complexity (lower compression ratio) than righteousness descriptions. The difference is statistically significant.

This is the empirical confirmation of what Test 4 (JAX) proves theoretically: deception has higher algorithmic complexity than truth, measurable by compression proxy.

Time: 0.02 seconds.

---

## Interpretation

This is one of the tests where the information-theoretic argument has the most direct theological bite. "The truth shall set you free" is not just a spiritual claim — it's an information-theoretic efficiency argument. Maintaining lies requires overhead. Managing contradictions takes resources. Deception has entropy costs that truth doesn't.

The compression test makes this literal and measurable. Biblical text about sin is harder to compress — informationally denser — not because it's more sophisticated, but because it's describing incoherent states that require more bits to specify.

The complementarity is striking: Test 03 shows that revelation grows in complexity over time (information being added). Test 06 shows that sin descriptions are more complex than righteousness descriptions at any given time (information being wasted on incoherence). Both results follow from the same K-component prediction.
