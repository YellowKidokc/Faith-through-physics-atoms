# Lean Proof Readiness Packet
This is a static readiness packet. It does not run `lake build` and does not compile the proofs.
## Snapshot
- **central_hub**: H:\Desktop 2\LEAN 4\Google CoLab Python
- **extracted_repos**: H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS
- **lean_files**: 47
- **declarations**: 2113
- **run_roots**: 5
- **lake_roots**: 3
- **signals**: {'rfl': 60, 'check_failure': 308, 'by_trivial': 604, 'decide': 82, 'simp': 267, 'true_statement': 352, 'set_option': 1}
- **severity**: {'REVIEW': 718, 'HIGH_CLAIM_RISK': 956}
- **duplicate_theorem_names**: 408
- **files_with_sorry_or_admit**: 0
- **files_with_claim_risk**: 7

## Recommended Run Order
1. `H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Faith-Thru-Physics-Lean-4--main\Faith-Thru-Physics-Lean-4--main`
   - Later command: `lake build`
2. `H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Lean-4-Proofs-main\Lean-4-Proofs-main\theophysics-lean-verification-package\narrow_product_test`
   - Later command: `lake build`
3. `H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\theophysics-lean-main\theophysics-lean-main`
   - Later command: `lake build`
4. `H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Faith-Thru-Physics-Lean-4--main\Faith-Thru-Physics-Lean-4--main\BUILD_CONFIG`
   - Later action: Run lake build later from this folder.
5. `H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Lean-4-Proofs-main\Lean-4-Proofs-main\theophysics-lean-verification-package`
   - Later action: Use included script or run individual Lean files later.
   - Runner scripts: `H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Lean-4-Proofs-main\Lean-4-Proofs-main\theophysics-lean-verification-package\RUN_LEAN_PRODUCTION_KERNEL.bat | H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Lean-4-Proofs-main\Lean-4-Proofs-main\theophysics-lean-verification-package\VERIFY_ALL_WINDOWS.bat`

## What To Fix Before Making Public Claims
- Anything marked `BLOCKER` needs a direct proof or a deliberate explanation before the proof run.
- Anything marked `HIGH_CLAIM_RISK` may still compile, but should not be described as a strong theorem without the five-sentence evidence separation.
- Duplicate theorem names are not automatically wrong, but they need canonical ownership so the workbook cites the correct one.

## Generated Files
- `lean-static-readiness-report.csv`
- `lean-proof-placeholder-queue.csv`
- `lean-duplicate-theorem-names.csv`
- `lean-canonical-owner-queue.csv`
- `lean-run-roots.csv`
- `lean-import-map.csv`
- `lean-proof-readiness-summary.json`
