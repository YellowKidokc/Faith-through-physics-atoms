# Lean Canonical Ledger Summary

This ledger deduplicates the full 47-file Lean scan by theorem/declaration name and assigns one canonical owner per name.

## Counts

- **ledger_version**: LEAN_CANONICAL_LEDGER_20260709
- **raw_declaration_rows_unique_names**: 884
- **raw_declaration_instances_full_scan**: 2318
- **kind_counts_unique_names**: {'inductive': 44, 'def': 216, 'structure': 41, 'theorem': 583}
- **proof_strength_counts_unique_names**: {'DECLARATION_OR_UNKNOWN': 399, 'TRIVIAL_TRUE': 85, 'SIMPLIFICATION': 81, 'DEFINITIONAL_RFL': 157, 'WRAPPER_OR_IMPORTED': 110, 'SUBSTANTIVE_OR_CASE_PROOF': 26, 'FINITE_DECIDABLE': 26}
- **public_count_buckets**: {'SCAFFOLDING_NOT_PUBLIC_COUNT': 301, 'CANONICAL_THEOREM_DEDUPED_PENDING_COMPILE': 228, 'LOW_CONTENT_TRUE_NOT_PUBLIC_COUNT': 85, 'UNIQUE_THEOREM_PENDING_COMPILE': 270}
- **canonical_theorem_count_pending_compile**: 498
- **low_content_true_excluded**: 85
- **scaffolding_excluded**: 301
- **missing_original_names_total**: 171
- **missing_original_names_found_in_full_scan**: 171
- **missing_original_names_still_missing**: 0
- **compile_status_note**: No Lean build was run in this pass; compile status remains pending.

## Public Count Discipline

Do not publish the raw 1,567-style declaration count as the proof count. The public-facing number should come from `canonical_theorem_count_pending_compile` only after the relevant canonical roots compile.

## Load-Bearing Controls

- `heavisideVectorEM_invalid` — theophysics-lean-main\theophysics-lean-main\Theophysics_Adversarial.lean:453 — WRAPPER_OR_IMPORTED — CANONICAL_THEOREM_DEDUPED_PENDING_COMPILE
- `heaviside_passes_if_coupling_guard_removed` — theophysics-lean-main\theophysics-lean-main\Theophysics_Core.lean:234 — TRIVIAL_TRUE — LOW_CONTENT_TRUE_NOT_PUBLIC_COUNT
- `modalism_invalid` — theophysics-lean-main\theophysics-lean-main\Theophysics_Adversarial.lean:457 — WRAPPER_OR_IMPORTED — CANONICAL_THEOREM_DEDUPED_PENDING_COMPILE
- `modalism_passes_if_distinctness_guard_removed` — theophysics-lean-main\theophysics-lean-main\Theophysics_Core.lean:235 — TRIVIAL_TRUE — LOW_CONTENT_TRUE_NOT_PUBLIC_COUNT
- `relabeledRoleSystem_invalid` — theophysics-lean-main\theophysics-lean-main\Theophysics_Adversarial.lean:469 — WRAPPER_OR_IMPORTED — CANONICAL_THEOREM_DEDUPED_PENDING_COMPILE
- `relabeled_roles_pass_if_profile_guard_removed` — theophysics-lean-main\theophysics-lean-main\Theophysics_Core.lean:237 — TRIVIAL_TRUE — LOW_CONTENT_TRUE_NOT_PUBLIC_COUNT
- `static_single_field_passes_if_dynamic_guard_removed` — theophysics-lean-main\theophysics-lean-main\Theophysics_Core.lean:236 — TRIVIAL_TRUE — LOW_CONTENT_TRUE_NOT_PUBLIC_COUNT

## Generated Artifacts

- `LEAN_CANONICAL_LEDGER.csv`
- `LEAN_CANONICAL_LEDGER.summary.json`
- `lean-load-bearing-controls-ledger.csv`
- `lean-missing-names-full-scan-resolution.csv`
