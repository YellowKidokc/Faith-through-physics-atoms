# Coverage Against Excel Theorem Inventory

Source workbook: `Theophysics_Lean4_Addendum_Updated (1) (2).xlsx`

This table compares the `LEAN_DERIVATION_CHAIN` sheet against theorem/definition declarations present in this repo by exact declaration name.

## Summary

- Excel numbered theorem rows checked: `171`
- Exact-name rows implemented: `171`
- Exact-name rows not found: `0`
- `implemented-adversarial`: `63`
- `implemented-core`: `98`
- `implemented-excel-spine`: `10`

Note: the workbook dashboard may count additional rows beyond the visible `LEAN_DERIVATION_CHAIN`; this file reports only the numbered rows available in that sheet.

## Table

| # | Layer | Excel file | Declaration | Type | Repo file(s) | Status |
|---:|---|---|---|---|---|---|
| 1 | 0 — Core | Core.lean | `C0_ne_C1` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 2 | 0 — Core | Core.lean | `C1_ne_C0` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 3 | 0 — Core | Core.lean | `coupling_modification_irreversible` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 4 | 0 — Core | Core.lean | `Q_zero_collapses_chi` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 5 | 0 — Core | Core.lean | `Q_nonzero_not_sufficient_for_positive_chi` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 6 | 1 — Stage | StageMachine.lean | `reaches_localization_from_pre` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 7 | 1 — Stage | StageMachine.lean | `reaches_redistribution_from_pre` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 8 | 1 — Stage | StageMachine.lean | `no_stage_step_back_to_pre_from_localization` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 9 | 1 — Stage | StageMachine.lean | `no_stage_step_back_to_release_from_confirmation` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 10 | 1 — Stage | StageMachine.lean | `no_stage_step_back_to_confirmation_from_redistribution` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 11 | 2 — Mapping | Mapping.lean | `map_physics_sequence_is_theology_sequence` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 12 | 2 — Mapping | Mapping.lean | `localization_maps_to_incarnation` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 13 | 2 — Mapping | Mapping.lean | `confirmation_maps_to_resurrection` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 14 | 3 — Bridge | BridgeMatrix.lean | `canonicalRows_all_valid` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 15 | 3 — Bridge | BridgeMatrix.lean | `grace_swapped_with_faith_invalid` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 16 | 3 — Bridge | BridgeMatrix.lean | `entropy_swapped_with_grace_invalid` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 17 | 3 — Bridge | BridgeMatrix.lean | `compression_swapped_with_communion_invalid` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 18 | 3 — Bridge | BridgeMatrix.lean | `coherence_swapped_with_consequence_lock_invalid` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 19 | 3 — Bridge | BridgeMatrix.lean | `wrong_physical_for_grace_invalid` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 20 | 3 — Bridge | BridgeMatrix.lean | `arbitrary_grace_clone_matches_G` | BOUNDARY | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 21 | 3 — Bridge | BridgeMatrix.lean | `arbitrary_faith_clone_does_not_match_G` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 22 | 3 — Bridge | BridgeMatrix.lean | `full_G_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 23 | 3 — Bridge | BridgeMatrix.lean | `full_M_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 24 | 3 — Bridge | BridgeMatrix.lean | `full_E_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 25 | 3 — Bridge | BridgeMatrix.lean | `full_S_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 26 | 3 — Bridge | BridgeMatrix.lean | `full_T_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 27 | 3 — Bridge | BridgeMatrix.lean | `full_K_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 28 | 3 — Bridge | BridgeMatrix.lean | `full_R_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 29 | 3 — Bridge | BridgeMatrix.lean | `full_Q_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 30 | 3 — Bridge | BridgeMatrix.lean | `full_F_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 31 | 3 — Bridge | BridgeMatrix.lean | `full_C_zero_collapses` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 32 | 3 — Bridge | BridgeMatrix.lean | `full_Q_nonzero_not_sufficient` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 33 | 3 — Bridge | BridgeMatrix.lean | `full_R_gate_required` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 34 | 3 — Bridge | BridgeMatrix.lean | `all_ones_live` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 35 | 4 — Invariance | MasterEquationInvariance.lean | `canonical_substitution_row_valid` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 36 | 4 — Invariance | MasterEquationInvariance.lean | `canonical_substitution_preserves_signature` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 37 | 4 — Invariance | MasterEquationInvariance.lean | `master_equation_invariant_under_canonical_substitution` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 38 | 4 — Invariance | MasterEquationInvariance.lean | `G_zero_still_collapses_after_substitution` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 39 | 4 — Invariance | MasterEquationInvariance.lean | `Q_zero_still_collapses_after_substitution` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 40 | 4 — Invariance | MasterEquationInvariance.lean | `product_only_does_not_detect_grace_faith_swap` | BOUNDARY | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 41 | 4 — Invariance | MasterEquationInvariance.lean | `signature_layer_rejects_grace_faith_swap` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 42 | 4 — Invariance | MasterEquationInvariance.lean | `master_invariance_requires_signature_discipline` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 43 | 5 — Law 3 (EM/Truth) | FieldBridgeControls.lean | `law3_truth_limit_E_one` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 44 | 5 — Law 3 (EM/Truth) | FieldBridgeControls.lean | `law3_command_bypass_forces_E_zero` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 45 | 5 — Law 3 (EM/Truth) | FieldBridgeControls.lean | `law3_phase_inversion_forces_E_zero` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 46 | 5 — Law 3 (EM/Truth) | FieldBridgeControls.lean | `law3_command_bypass_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 47 | 5 — Law 3 (EM/Truth) | FieldBridgeControls.lean | `law3_phase_inversion_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 48 | 5 — Law 6 (Info/Logos) | FieldBridgeControls.lean | `law6_logos_limit_K_one` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 49 | 5 — Law 6 (Info/Logos) | FieldBridgeControls.lean | `law6_relation_bypass_forces_K_zero` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 50 | 5 — Law 6 (Info/Logos) | FieldBridgeControls.lean | `law6_bandwidth_closed_forces_K_zero` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 51 | 5 — Law 6 (Info/Logos) | FieldBridgeControls.lean | `law6_distortion_dominates_forces_K_zero` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 52 | 5 — Law 6 (Info/Logos) | FieldBridgeControls.lean | `law6_bandwidth_collapse_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 53 | 5 — Law 7 (Rel/Frame) | FieldBridgeControls.lean | `law7_righteous_limit_R_one` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 54 | 5 — Law 7 (Rel/Frame) | FieldBridgeControls.lean | `law7_relation_bypass_forces_R_zero` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 55 | 5 — Law 7 (Rel/Frame) | FieldBridgeControls.lean | `law7_metric_absent_forces_R_zero` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 56 | 5 — Law 7 (Rel/Frame) | FieldBridgeControls.lean | `law7_frame_lock_forces_R_zero` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 57 | 5 — Law 7 (Rel/Frame) | FieldBridgeControls.lean | `law7_relation_bypass_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 58 | 5 — Law 7 (Rel/Frame) | FieldBridgeControls.lean | `law7_frame_lock_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 59 | 5 — Law 8 (QM/Faith) | FieldBridgeControls.lean | `law8_faith_limit_Q_one` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 60 | 5 — Law 8 (QM/Faith) | FieldBridgeControls.lean | `law8_command_bypass_forces_Q_zero` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 61 | 5 — Law 8 (QM/Faith) | FieldBridgeControls.lean | `law8_missing_eigenbasis_forces_Q_zero` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 62 | 5 — Law 8 (QM/Faith) | FieldBridgeControls.lean | `law8_control_refusal_forces_Q_zero` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 63 | 5 — Law 8 (QM/Faith) | FieldBridgeControls.lean | `law8_command_bypass_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 64 | 5 — Law 8 (QM/Faith) | FieldBridgeControls.lean | `law8_control_refusal_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 65 | 6 — Score | BridgeScoreDiscipline.lean | `binaryGate_zero` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 66 | 6 — Score | BridgeScoreDiscipline.lean | `binaryGate_positive` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 67 | 6 — Score | BridgeScoreDiscipline.lean | `binaryGate_zero_or_one` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 68 | 6 — Score | BridgeScoreDiscipline.lean | `law3_unbacked_amplitude_still_has_zero_truth_fidelity` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 69 | 6 — Score | BridgeScoreDiscipline.lean | `law3_command_bypass_zeroes_source_backed_fidelity` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 70 | 6 — Score | BridgeScoreDiscipline.lean | `law7_healthy_score_passes_R_gate` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 71 | 6 — Score | BridgeScoreDiscipline.lean | `law7_frame_locked_score_fails_R_gate` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 72 | 6 — Score | BridgeScoreDiscipline.lean | `law7_relation_bypass_score_fails_R_gate` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 73 | 6 — Score | BridgeScoreDiscipline.lean | `law7_final_R_is_binary` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 78 | 7 — Iso | IsomorphismTest.lean | `law4Iso` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 79 | 7 — Iso | IsomorphismTest.lean | `strongForceCoinIso` | BOUNDARY | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 80 | 7 — Iso | IsomorphismTest.lean | `richLaw4Iso` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 81 | 7 — Iso | IsomorphismTest.lean | `no_rich_iso_to_natural_coin` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 82 | 7 — Iso | IsomorphismTest.lean | `richRelabeledCoinIso` | BOUNDARY | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 83 | 7 — Iso | IsomorphismTest.lean | `faith_candidate_not_right_inverse` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 84 | 7 — Iso | IsomorphismTest.lean | `em_candidate_not_right_inverse` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 85 | 7 — Iso | IsomorphismTest.lean | `inverted_mapping_does_not_preserve_value` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 86 | 7 — Iso | IsomorphismTest.lean | `no_law4_iso_uses_inverted_mapping` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 87 | 7 — Iso | IsomorphismTest.lean | `misaligned_collapse_rule_invalid` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 88 | 8 — Maxwell | MaxwellTrinity.lean | `full_quaternion_product_has_coupling_invariant` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 89 | 8 — Maxwell | MaxwellTrinity.lean | `vector_only_product_lacks_coupling_invariant` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 90 | 8 — Maxwell | MaxwellTrinity.lean | `full_scalar_vector_split_reconstructs_quaternion_product` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 91 | 8 — Maxwell | MaxwellTrinity.lean | `same_dot_cross_but_different_quaternion_product` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 92 | 8 — Maxwell | MaxwellTrinity.lean | `quaternionEM_valid` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 93 | 8 — Maxwell | MaxwellTrinity.lean | `trinityRelational_valid` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 94 | 8 — Maxwell | MaxwellTrinity.lean | `quaternionTrinityIso` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 95 | 8 — Maxwell | MaxwellTrinity.lean | `heavisideVectorEM_invalid` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 96 | 8 — Maxwell | MaxwellTrinity.lean | `modalism_invalid` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 97 | 8 — Maxwell | MaxwellTrinity.lean | `staticSingleFieldEM_invalid` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 98 | 8 — Maxwell | MaxwellTrinity.lean | `arbitraryThreePartSystem_invalid` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 99 | 8 — Maxwell | MaxwellTrinity.lean | `relabeledRoleSystem_invalid` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 112 | 9 — J/M | JusticeMercyOperator.lean | `justice_and_mercy_share_common_components` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 113 | 9 — J/M | JusticeMercyOperator.lean | `justice_and_mercy_differ_by_cost_bearer` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 118 | 9 — J/M | JusticeMercyOperator.lean | `cross_satisfies_convergence` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 119 | 9 — J/M | JusticeMercyOperator.lean | `offender_payment_fails_mercy_condition` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 120 | 9 — J/M | JusticeMercyOperator.lean | `human_third_party_fails_authority_and_capacity` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 121 | 9 — J/M | JusticeMercyOperator.lean | `coerced_third_party_fails_voluntariness` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 122 | 9 — J/M | JusticeMercyOperator.lean | `waived_debt_fails_justice_condition` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 123 | 9 — J/M | JusticeMercyOperator.lean | `shared_cost_fails_mercy_condition` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 124 | 9 — J/M | JusticeMercyOperator.lean | `cross_unique_convergence_configuration` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 125 | 9 — J/M | JusticeMercyOperator.lean | `cross_is_unique_solution` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 126 | 10 — Polarity | PolarityDiscipline.lean | `two_destructive_signs_have_positive_raw_product` | PROVED | Final_Lean4_From_Excel.lean, Theophysics_Core.lean | `implemented-core` |
| 127 | 10 — Polarity | PolarityDiscipline.lean | `two_destructive_signs_do_not_pass_coherence_gate` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 128 | 10 — Polarity | PolarityDiscipline.lean | `below_accountability_maps_to_neutral_even_with_bad_signal` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 129 | 10 — Polarity | PolarityDiscipline.lean | `below_accountability_has_zero_culpability` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 130 | 10 — Polarity | PolarityDiscipline.lean | `destructive_strict_M_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 131 | 10 — Polarity | PolarityDiscipline.lean | `neutral_accountability_aware_M_does_not_zero_M` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 132 | 10 — Polarity | PolarityDiscipline.lean | `destructive_accountability_aware_M_collapses_chi` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 133 | 11 — Sign | SignConversionDiscipline.lean | `raw_two_negatives_multiply_positive` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 134 | 11 — Sign | SignConversionDiscipline.lean | `burden_two_negatives_stay_negative` | REJECTION | Final_Lean4_From_Excel.lean | `implemented-excel-spine` |
| 135 | 11 — Sign | SignConversionDiscipline.lean | `burden_negative_positive_stays_negative` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 136 | 11 — Sign | SignConversionDiscipline.lean | `christic_conversion_turns_negative_burden_positive` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 137 | 11 — Sign | SignConversionDiscipline.lean | `christic_conversion_turns_neutral_burden_positive` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 138 | 11 — Sign | SignConversionDiscipline.lean | `two_negative_burdens_require_conversion_for_positive` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 139 | 11 — Sign | SignConversionDiscipline.lean | `two_negative_burdens_without_conversion_not_positive` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 140 | 11 — Sign | SignConversionDiscipline.lean | `negative_burden_gate_zero` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 141 | 11 — Sign | SignConversionDiscipline.lean | `converted_negative_burden_gate_one` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 142 | 12 — C_op | ChristOperatorDiscipline.lean | `C_op_converts_negative_to_positive` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 143 | 12 — C_op | ChristOperatorDiscipline.lean | `C_op_converts_neutral_to_positive` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 144 | 12 — C_op | ChristOperatorDiscipline.lean | `C_op_keeps_positive_positive` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 145 | 12 — C_op | ChristOperatorDiscipline.lean | `C_op_preserves_record_mark` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 146 | 12 — C_op | ChristOperatorDiscipline.lean | `C_op_preserves_source_state` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 147 | 12 — C_op | ChristOperatorDiscipline.lean | `C_op_preserves_negative_history_even_after_positive_output` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 148 | 12 — C_op | ChristOperatorDiscipline.lean | `visible_projection_conflates_negative_and_neutral_conversion` | BOUNDARY | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 149 | 12 — C_op | ChristOperatorDiscipline.lean | `lifted_outputs_preserve_distinct_source_signs` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 150 | 12 — C_op | ChristOperatorDiscipline.lean | `visible_restoration_does_not_imply_erasure` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 151 | 12 — C_op | ChristOperatorDiscipline.lean | `chi_via_COp_converts_two_negative_burdens` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 152 | 12 — C_op | ChristOperatorDiscipline.lean | `chi_via_COp_is_not_plain_scalar_self_multiplication` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 153 | 13 — Mission | MissionReturnOperator.lean | `incarnation_preserves_substrate_identity` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 154 | 13 — Mission | MissionReturnOperator.lean | `cross_preserves_substrate_identity` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 155 | 13 — Mission | MissionReturnOperator.lean | `resurrection_preserves_substrate_identity` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 156 | 13 — Mission | MissionReturnOperator.lean | `incarnation_is_finite_compression` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 157 | 13 — Mission | MissionReturnOperator.lean | `resurrection_returns_to_infinite_resolution` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 158 | 13 — Mission | MissionReturnOperator.lean | `cross_has_entropy_and_death_contact` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 161 | 13 — Mission | MissionReturnOperator.lean | `resurrection_is_not_identical_to_preincarnate_visible_record` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 162 | 13 — Mission | MissionReturnOperator.lean | `resurrection_same_substrate_richer_expression` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 165 | 13 — Mission | MissionReturnOperator.lean | `mission_COp_is_not_repair_only` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 166 | 14 — Memory | MemoryPersistenceDiscipline.lean | `christ_coherent_memory_retained` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 167 | 14 — Memory | MemoryPersistenceDiscipline.lean | `incoherent_recorded_memory_not_retained` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 170 | 14 — Memory | MemoryPersistenceDiscipline.lean | `recorded_and_christ_coherent_forces_retention` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 171 | 14 — Memory | MemoryPersistenceDiscipline.lean | `incoherent_recorded_memory_fails_only_final_retention` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 172 | 14 — Memory | MemoryPersistenceDiscipline.lean | `living_memory_is_not_final_identity_memory` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 173 | 14 — Memory | MemoryPersistenceDiscipline.lean | `reoriented_incoherent_memory_becomes_retained` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 177 | 14 — Memory | MemoryPersistenceDiscipline.lean | `heaven_is_coherent_and_eternal` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 180 | 14 — Memory | MemoryPersistenceDiscipline.lean | `direct_discoherent_christ_entry_into_heaven_fails` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 181 | 14 — Memory | MemoryPersistenceDiscipline.lean | `transformed_discoherent_christ_entry_into_heaven_passes` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 182 | 14 — Memory | MemoryPersistenceDiscipline.lean | `transformed_unrecorded_discoherent_entry_still_fails` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 183 | 14 — Memory | MemoryPersistenceDiscipline.lean | `valid_giving_life_to_christ` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 184 | 14 — Memory | MemoryPersistenceDiscipline.lean | `resisting_without_grace_not_valid_conversion` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 187 | 14 — Memory | MemoryPersistenceDiscipline.lean | `unrecorded_negative_conversion_still_has_no_identity_trace` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 188 | 15 — Lattice | DependencyLattice.lean | `fall_has_parallel_death_and_judgment` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 189 | 15 — Lattice | DependencyLattice.lean | `fall_has_parallel_promise_not_death_then_promise` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 190 | 15 — Lattice | DependencyLattice.lean | `no_death_strictly_before_judgment` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 191 | 15 — Lattice | DependencyLattice.lean | `fall_as_covenant_rupture_requires_image_and_covenant` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 192 | 15 — Lattice | DependencyLattice.lean | `energy_and_momentum_are_noether_siblings` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 193 | 15 — Lattice | DependencyLattice.lean | `no_energy_parent_of_momentum` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 194 | 15 — Lattice | DependencyLattice.lean | `bound_state_requires_excitation_and_coupling` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 198 | 15 — Lattice | DependencyLattice.lean | `glorification_requires_both_for_this_lattice` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 199 | 15 — Lattice | DependencyLattice.lean | `narrative_and_dependency_orders_diverge_at_justification_union` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 203 | 16 — HitRate | HitRateDiscipline.lean | `closedEightOfTen_attempt_count` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 204 | 16 — HitRate | HitRateDiscipline.lean | `closedEightOfTen_hit_count` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 205 | 16 — HitRate | HitRateDiscipline.lean | `closedEightOfTen_denominator_closed` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 206 | 16 — HitRate | HitRateDiscipline.lean | `closedEightOfTen_can_claim_80_percent` | PROVED | Theophysics_Core.lean | `implemented-core` |
| 207 | 16 — HitRate | HitRateDiscipline.lean | `closedEightOfTen_cannot_claim_90_percent` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 208 | 16 — HitRate | HitRateDiscipline.lean | `hiddenDenominator_blocks_anomaly_claim` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 209 | 16 — HitRate | HitRateDiscipline.lean | `failed_attempt_counts_in_denominator` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
| 210 | 16 — HitRate | HitRateDiscipline.lean | `partial_attempt_does_not_count_as_hit` | REJECTION | Theophysics_Adversarial.lean | `implemented-adversarial` |
