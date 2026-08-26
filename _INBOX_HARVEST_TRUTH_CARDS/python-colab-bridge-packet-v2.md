# Python / Colab Bridge Packet v2

Created: 2026-07-09

This packet adds the missing bridge between the Lean proof ledger and the runtime notebooks/scripts.

## What Changed

- Added a variable and parameter registry extracted from the runtime artifacts.
- Added a dimensional audit queue for deciding which symbols need units, ranges, normalization, and source notes.
- Added an ablation/control matrix so every public-facing runtime claim runs beside a null, rival, or broken-control version.

## Counts

```text
Runtime artifacts mapped: 25
Symbols/parameters needing review: 329
Claim families: 10
Run phases: {'Phase 1': 10, 'Phase 2': 9, 'Phase 3': 6}
Public status buckets: {'open_or_conflicted': 5, 'mixed_verified_and_open': 6, 'not_declared': 11, 'claims_verified': 3}
```

## Main Rule

Every runtime result should have four things before it supports a public claim:

1. exact artifact path,
2. variable/unit/range declaration,
3. side-by-side baseline or ablation control,
4. output hash or rerun receipt.

## Use These First

- `python-colab-variable-registry.csv`
- `python-colab-dimensional-audit-queue.csv`
- `python-colab-ablation-matrix.csv`

The safest first public-support candidates are still the Maxwell field-coupling notebooks, because they already contain verified-result language. The risky ones are the open/conflicted galaxy, chi, canonical-derivation, and migration artifacts; those should become objection/repair pages until rerun evidence settles them.
