# ATLAS Lean Reference Readout

Created: 2026-07-20 06:49:15

Source path:

```text
D:\GitHub\atlas-lean
```

Note: `MOVED_TO.md` says this repo was moved to `G:\GitHub\atlas-lean` on 2026-07-10. The D-drive copy still exists and was inspected.

## What It Is

ATLAS is an autoformalized Lean 4 textbook mathematics library. It is useful as a proof-pattern/reference corpus, not as Theophysics canon evidence.

## Local Counts

- Lean files excluding `.lake` and `.git`: 2654
- Book/domain folders: 26
- `report.json` files: 26
- `targets.yaml` files: 26
- Pinned toolchain: Lean 4 v4.29.0
- Mathlib revision from lakefile: 8a178386ffc0f5fef0b77738bb5449d50efeea95

## Book / Domain Folders
- AlgebraicCombinatorics
- AlgebraicGeometryI
- AlgebraicTopologyI
- AlgebraNotes
- AnAlgorithmistsToolkit
- ArithmeticGeometry
- BooleanFunctions
- Buildings
- CombinatorialOptimization
- ComplexVariables
- DifferentialAnalysis
- DifferentialGeometry
- EllipticCurves
- FourierAnalysis
- GeometryOfManifolds
- HighDimensionalStatistics
- IntroductionToFunctionalAnalysis
- IntroductionToPartialDifferentialEquations
- LieGroups
- NumberTheoryI
- ProbabilisticMethodsInCombinatorics
- ProjectionTheory
- RealAnalysis
- TensorCategories
- TheoryOfComputation
- TheoryOfProbability

## Why It Helps Us

1. It gives Lean project layout examples: `lakefile.toml`, `lean-toolchain`, top-level import file, domain folders, generated code folders.
2. It gives proof-review categories we should imitate: faithfulness, proof integrity, code quality, dependency-chain risk.
3. It includes `targets.yaml` and `report.json`, which are close to what our Excel/Lean/Colab crosswalk should become.
4. It supports the idea of separating theorem statement quality from proof completion. A faithful statement with `sorry` is not the same as a proved theorem.
5. It can help a Lean specialist find idioms, imports, helper lemmas, and mathlib patterns.

## Guardrail

Do not copy ATLAS wholesale into the Theophysics canon. Use it as an external reference. It is machine-generated, ongoing, and contains some sorry-backed declarations according to its own reports.

## Copied Reference Files

- H:\Desktop 2\LEAN 4\GPT\QUARANTINE\ATLAS_REFERENCE\ATLAS_README.md
- H:\Desktop 2\LEAN 4\GPT\QUARANTINE\ATLAS_REFERENCE\atlas_lakefile.toml
- H:\Desktop 2\LEAN 4\GPT\QUARANTINE\ATLAS_REFERENCE\atlas_lean-toolchain
- H:\Desktop 2\LEAN 4\GPT\QUARANTINE\ATLAS_REFERENCE\MOVED_TO.md

## Best Use For The Lean Specialist GPT

Ask it to use ATLAS as reference for package organization, proof-review metadata, dependency reports, and idiomatic Lean/mathlib patterns. Do not ask it to treat ATLAS as evidence that Theophysics claims are true.
