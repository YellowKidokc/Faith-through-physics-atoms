# KIMI Compilation — DG v0.2 Claim-Level Pass Report

**Scope:** Claim-level Unified Derivation Grammar v0.2 protocol pass over the A/B/C HTML compilation.

**Date:** 2026-08-01

## Summary

- **Total claim rows extracted:** 543

### Counts by `dg6_state`
- coherent: 276
- coherent_partial: 261
- defective: 6

### Counts by `dg7_admissible`
- needs_review: 261
- partial: 6
- yes: 276

### Counts by `dg8_closure_pass`
- yes: 543

### Counts by `recommended_atom_action`
- create_bridge_atom: 297
- create_claim_atom: 152
- create_gap_atom: 88
- create_objection_atom: 6

## Flagged Rows (defective or create_objection_atom)

| row_id | reason |
| --- | --- |
| KIMI-fall-redemption-B-001 | Register gap / defective B-section. |
| KIMI-fall-redemption-B-002 | Register gap / defective B-section. |
| KIMI-fall-redemption-B-003 | Register gap / defective B-section. |
| KIMI-spiritual-terms-B-001 | Register gap / defective B-section. |
| KIMI-spiritual-terms-B-002 | Register gap / defective B-section. |
| KIMI-spiritual-terms-B-003 | Register gap / defective B-section. |

## Notes

- This pass is **pre-pill**. Many structural DG columns (dg1–dg5) were assigned using register-level heuristics; rows marked `needs_review` or `partial` should be reviewed before atom promotion.
- Compound paragraphs were split into independent sentence-level claims where possible; list items and table rows were kept as single claim rows.
- Theology names are treated as instantiations, not DG-core content, per v0.2 section 6.
- Proof labels use the v0.2 schema codes (D, S, L, M, H, E, BR, T, C, PM, PH).