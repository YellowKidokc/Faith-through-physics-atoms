# Lean 4 Canonical Ledger Merge Report

- Run ID: `lean4-ledger-merge-20260813-052343`
- Generated: `2026-08-13T05:23:46-05:00`
- Output workbook: `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_MERGED.xlsx`
- Output SHA-256: `dc5136f1b78c43aa6f02fa72884c8fafdc0723b802180584abbe33f1aba553f9`
- Source workbook count: 7
- Duplicate source groups: 2
- Addendum sheets added: 10
- Atom log: `D:\GitHub\Faith-through-physics-atoms\_ledger\atoms\tp-lean4-canonical-ledger.json`

## Source Workbooks

| Path | Exists | Bytes | SHA-256 | Sheets |
|---|---:|---:|---|---:|
| `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_V2.xlsx` | True | 271318 | `280422f68a2b9e60f171ea0e69a7d07a1e1c68a91ffed3f8582db735f158059c` | 15 |
| `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_V2 - Python Colab Audit.xlsx` | True | 271318 | `280422f68a2b9e60f171ea0e69a7d07a1e1c68a91ffed3f8582db735f158059c` | 15 |
| `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_V2.backup_before_python_colab_audit.xlsx` | True | 262743 | `216590142b893d4d4c9ce5227f4ea1231afad87701e84ac28d80665255dc9871` | 14 |
| `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_V2.pre_python_colab_replace.xlsx` | True | 262743 | `216590142b893d4d4c9ce5227f4ea1231afad87701e84ac28d80665255dc9871` | 14 |
| `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4.backup_20260710_041459.xlsx` | True | 213922 | `949cc676b61b644668ddf5b4d6042ba98d4372294a32a9c643e3fe4aab11aa13` | 12 |
| `\\192.168.2.50\h_hp\Desktop\Documents\LEAN 4 Master.xlsx` | True | 320644 | `190a4c3bf3c6bac8acc7b7acd0ccd28e10806993f1c77e89249e412e8d4b306b` | 27 |
| `\\192.168.2.50\h_hp\Desktop 2\Theophysics_Lean4_Addendum_Updated (1).xlsx` | True | 96031 | `263642f0a6280588b7432b38c82f654f2ba424129d6b5da506496e3e2f557347` | 10 |

## Duplicate Groups

- `280422f68a2b9e60f171ea0e69a7d07a1e1c68a91ffed3f8582db735f158059c`
  - `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_V2.xlsx`
  - `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_V2 - Python Colab Audit.xlsx`
- `216590142b893d4d4c9ce5227f4ea1231afad87701e84ac28d80665255dc9871`
  - `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_V2.backup_before_python_colab_audit.xlsx`
  - `\\192.168.2.50\h_hp\Desktop\Master EXCEL\Lean 4 - CANONICAL_LEDGER_V2.pre_python_colab_replace.xlsx`

## Cleanup Recommendation

Keep `LEAN 4 Master.xlsx` and the merged workbook as active review surfaces.
Archive duplicate exact copies only after human review of this report.
Do not delete any source workbook; move retired copies into a dated archive folder with this report as receipt.

## Validation Note

The new control atom `tp:lane4/lean4/canonical-ledger` has assumptions, source
artifacts, current status, one merge event, and unique event IDs.

The existing repo-wide Lane 4 validator currently reports pre-existing atom
issues outside this Lean ledger merge lane, so this run does not rebuild the
global claim ledger CSV/JSONL. The merge is logged in the control atom and
`LEAN4_RUN_LOG.jsonl`.
