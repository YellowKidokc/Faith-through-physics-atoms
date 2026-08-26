# Canonical Map

Generated: 2026-02-19
Vault root: `O:/_Theophysics_v3`

## Why this exists
This map translates skill-level canonical categories into the folders and files that actually exist in this vault.
It is designed for many-to-many resolution so Ring 2 linking works without restructuring 34k+ files.

## Scope and safety rules
Included live roots:
- `O:/_Theophysics_v3/00_AXIOMS`
- `O:/_Theophysics_v3/00_Canonical`
- `O:/_Theophysics_v3/99_MATH_APPENDIX`
- `O:/_Theophysics_v3/99_TAG_NOTES`
- `O:/_Theophysics_v3/MASTER_EQ_CONSOLIDATED/00_TOP_CANONICAL_MASTER_EQ/PASS_20260217_201732`

Excluded from canonical resolution by default:
- Any path containing `/_ARCHIVE/`
- Any path containing `/ZZZ_FOLDER_REVIEW/`
- Any path containing `/999 codex delete/`
- Any path containing `/__David/`

## Translation table
| Skill Expects | Actually Lives In (Primary) | Also Resolve In (Secondary) |
|---|---|---|
| `Axioms/` | `00_AXIOMS` (`^[0-9]+_A...`) | `99_MATH_APPENDIX/Per_Axiom`, `MASTER_EQ.../06_CANONICAL_CHAIN` |
| `Definitions/` | `00_AXIOMS` (`^[0-9]+_D...`) | `99_TAG_NOTES` (`Lexicon`, `Glossary`, `08_CONCEPTS/Types/D_Definition.md`), `MASTER_EQ.../05_TERMS_AND_GLOSSARY` |
| `Equations/` | `00_AXIOMS` (`^[0-9]+_E...`) | `99_MATH_APPENDIX/Equations`, `99_MATH_APPENDIX/Per_Axiom/*_Math.md`, `MASTER_EQ.../01_CORE_EQUATION`, `00_Canonical/TH_Physics`, `00_Canonical/TH_Mathematics` |
| `Evidence/` | `00_AXIOMS` (`EV`, `EXP`, `PRED`, `FALS`, `PROT`) | `00_Canonical/TH_Consciousness`, `00_Canonical/TH_Historical_Docs`, `00_Canonical/TH_Neuroscience_Moral`, `99_TAG_NOTES/PEAR.md` |
| `Laws/` | `00_AXIOMS` (`D19.1` to `D19.10`) | `99_MATH_APPENDIX/Per_Axiom/D19.*_Math.md`, `MASTER_EQ.../02_LAWS`, `99_TAG_NOTES/08_CONCEPTS/*Laws*.md` |
| `Proofs/` | `00_AXIOMS` (`T`, `LN`, `BC`, `F` prefixes) | `99_MATH_APPENDIX/Per_Axiom/*_Math.md`, `MASTER_EQ.../04_VALIDATION_AND_PROOFS` |
| `Variables/` | `00_AXIOMS` variable-definition notes (chi/phi/grace/logos/rho/gamma terms) | `99_TAG_NOTES/08_CONCEPTS/Reference/*chi*`, `MASTER_EQ.../00_OVERVIEW/04 MASTER EQUATION SYMBOL DICTIONARY V1.md`, `MASTER_EQ.../00_OVERVIEW/Equation Index.md` |

## Current evidence snapshot
- `00_AXIOMS`: 200 markdown files
- `00_Canonical` (TH_* + docs): 591 markdown files
- `99_MATH_APPENDIX`: 180 markdown files
- `99_TAG_NOTES`: 304 markdown files
- `MASTER_EQ PASS_20260217_201732`: 785 markdown files

Pattern counts in `00_AXIOMS`:
- Axioms (`A*`): 33
- Definitions (`D*`): 33
- Equations (`E*`): 12
- Evidence-style (`EV/EXP/PRED/FALS/PROT`): 17
- Ten Laws (`D19.*`): 10
- Proof-style (`T/LN/BC/F`): 43

## Canonical exemplars
Axioms:
- `00_AXIOMS/001_A1.1_Existence.md`
- `00_AXIOMS/017_A3.2_Coherence-Measure.md`
- `00_AXIOMS/068_A8.2_Sign-Conservation.md`

Definitions:
- `00_AXIOMS/010_D2.1_Logos-Field-Definition.md`
- `00_AXIOMS/136_D19.1_Law-I-Definition.md`
- `99_TAG_NOTES/Lexicon.md`

Equations:
- `00_AXIOMS/012_E2.1_Master-Equation-First-Form.md`
- `99_MATH_APPENDIX/Equations/Formal_Definition.md`
- `MASTER_EQ_CONSOLIDATED/00_TOP_CANONICAL_MASTER_EQ/PASS_20260217_201732/01_CORE_EQUATION`

Evidence:
- `00_AXIOMS/112_EV15.3_PEAR-Lab-Results.md`
- `00_AXIOMS/111_EV15.2_GCP-Correlation.md`
- `00_AXIOMS/113_EV15.4_Social-Coherence-5.7-Sigma.md`

Laws:
- `00_AXIOMS/136_D19.1_Law-I-Definition.md`
- `00_AXIOMS/145_D19.10_Law-X-Definition.md`
- `MASTER_EQ_CONSOLIDATED/00_TOP_CANONICAL_MASTER_EQ/PASS_20260217_201732/02_LAWS`

Proofs:
- `00_AXIOMS/069_T8.1_Plausibility-Through-Compression.md`
- `00_AXIOMS/015_LN2.1_Information-Anchor-Necessity.md`
- `MASTER_EQ_CONSOLIDATED/00_TOP_CANONICAL_MASTER_EQ/PASS_20260217_201732/04_VALIDATION_AND_PROOFS`

Variables:
- `00_AXIOMS/011_D2.2_Chi-Field-Properties.md`
- `00_AXIOMS/048_D6.1_Collapse-Rate-Gamma.md`
- `00_AXIOMS/174_BRIDGE-PHI-CHI_Individual-Phi-To-Social-Chi.md`

## Known gaps to fill
- `01_CANONICAL/` does not exist as a live folder in this vault.
- Dedicated canonical `PROP-COSMOS` evidence note is not yet present in the canonical roots above.
  Current references exist in:
  - `00_SYSTEM/Glossary/Prop Cosmos.md`
  - `04_THEOPYHISCS/THREE TRUTHS/propcosmos.md`

## Resolution order for Ring 2
1. Resolve against the mapped Primary path for the category.
2. If no direct match, search mapped Secondary paths.
3. If still unresolved, emit an Ungrounded Claim warning and include the missing category.
4. Never auto-resolve from excluded paths.

## Path format for automation
All map consumers should normalize to vault-relative forward-slash paths.
Example: `00_AXIOMS/136_D19.1_Law-I-Definition.md`
## Related Theories

- [LOGOS V3 Revision 4 Long Lossless Bundle](LOGOS_V3_REV4_LONG_LOSSLESS_20260217_114247.md)
- [LOGOS V3 Revision 4 Long Lossless Bundle](LOGOS_V3_REV4_LONG_LOSSLESS_20260217_114353.md)
- [LOGOS V3 Revision 4 Long Lossless Bundle](LOGOS_V3_REV4_LONG_LOSSLESS_20260217_114658.md)
- [LOGOS V3 Revision 4 Long Lossless Bundle](LOGOS_V3_REV4_LONG_LOSSLESS_20260217_115124.md)
- [LOGOS V3 Revision 4 Long Lossless Bundle](LOGOS_V3_REV4_LONG_LOSSLESS_20260217_115124.md)
