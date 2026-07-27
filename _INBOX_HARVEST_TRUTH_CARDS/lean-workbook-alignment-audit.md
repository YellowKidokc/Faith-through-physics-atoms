# Lean Workbook Alignment Audit

Working source hub: `H:\Desktop 2\LEAN 4\Google CoLab Python`

## Workbook Base

- Base workbook: `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4.xlsx`

- `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4.xlsx`
  - `Sheet1`: 1 rows x 1 cols
  - `LEAN_DERIVATION_CHAIN`: 291 rows x 8 cols
  - `GAUNTLET_ARCHITECTURE`: 133 rows x 12 cols
- `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4.backup-20260701.xlsx`
  - `Sheet1`: 1 rows x 1 cols
  - `LEAN_DERIVATION_CHAIN`: 232 rows x 8 cols
  - `GAUNTLET_ARCHITECTURE`: 133 rows x 12 cols
- `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4_backup_before_location_audit.xlsx`
  - `Sheet1`: 1 rows x 1 cols
  - `LEAN_DERIVATION_CHAIN`: 291 rows x 8 cols
  - `GAUNTLET_ARCHITECTURE`: 133 rows x 12 cols
- `H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Faith-Thru-Physics-Lean-4--main\Faith-Thru-Physics-Lean-4--main\docs\Theophysics_Lean4_Addendum_Updated (1).xlsx`
  - `DASHBOARD`: 84 rows x 7 cols
  - `LEAN_DERIVATION_CHAIN`: 232 rows x 8 cols
  - `GAUNTLET_ARCHITECTURE`: 133 rows x 12 cols
  - `EXCEL_ADD_LIST`: 43 rows x 10 cols
  - `LANE4_DOSSIER`: 9 rows x 10 cols
  - `EMPIRICAL_TESTS`: 8 rows x 10 cols
  - `LOGIC_TANGENTS`: 9 rows x 10 cols
  - `INFRA_PUBLICATION`: 12 rows x 10 cols
  - `OPEN_PROBLEMS_GUARDS`: 7 rows x 10 cols
  - `FALSE_POSITIVE_QUEUE`: 11 rows x 10 cols

## Lean Inventory

- Lean theorem/lemma declarations found in extracted hub: **1567**
- Workbook rows in `LEAN_DERIVATION_CHAIN`: **270**
- Lean declarations not yet represented by exact theorem name in workbook: **756**
- Embedded workbook `EXCEL_ADD_LIST` rows found: **42**
- Embedded workbook `FALSE_POSITIVE_QUEUE` rows found: **10**
- Embedded workbook `OPEN_PROBLEMS_GUARDS` rows found: **6**

## Proof Strength Counts

- `DECLARATION_OR_UNKNOWN`: 281
- `DEFINITIONAL_RFL`: 451
- `FINITE_DECIDABLE`: 58
- `SIMPLIFICATION`: 189
- `SUBSTANTIVE_OR_CASE_PROOF`: 43
- `TRIVIAL_TRUE`: 352
- `WRAPPER_OR_IMPORTED`: 193

## Immediate Risks

- Workbook rows with `True`/trivial/not-found risk: **122**
- Flagship names with `True := by trivial` or broad English claims need rewording or stronger Lean statements before public citation.
- The workbook should gain evidence-ladder fields: `Defined`, `Formal`, `NegativeTest`, `Symbolic`, `Numerical`, `Stability`, `NullModel`, `Empirical`, `Prospective`, `Replication`.
- The structural-equivalence template adds claim classes `C0-C7`; every workbook row should receive exactly one primary class.
- The new staging CSV uses the five required sentences: defined, formally proven, numerically demonstrated, empirically observed, and interpretation proposed.

## Next Build

1. Add missing Lean declarations to a staging sheet, not directly into the canonical workbook.
2. Add `Proof_Strength` and `Public_Claim_Risk` columns.
3. For every `TRIVIAL_TRUE` flagship row, either downgrade the English claim or replace the theorem with a substantive statement.
4. Add a five-sentence evidence split per claim: what was defined, proven, numerically demonstrated, empirically observed, and interpreted.
5. Only after this audit, generate a clean workbook copy for repo testing.
