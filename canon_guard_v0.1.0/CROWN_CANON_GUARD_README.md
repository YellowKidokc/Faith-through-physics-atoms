# Crown Canon Guard

This layer checks the atoms repo against the current Crown / Master Equation
no-drift rules.

It does not decide canon by itself.

It does not silently rewrite equations.

It tells us where atoms, registries, packets, or README files still disagree
with the current Crown posture.

## Run

From PowerShell:

```powershell
D:\GitHub\Faith-through-physics-atoms\canon_guard_v0.1.0\RUN_CROWN_CANON_GUARD.ps1
```

## Run With DeepSeek Semantic Review

This runs the deterministic guard first, then sends a compact bounded report to
DeepSeek for triage:

```powershell
D:\GitHub\Faith-through-physics-atoms\canon_guard_v0.1.0\RUN_DEEPSEEK_CROWN_REVIEW.ps1
```

DeepSeek writes:

```text
D:\GitHub\Faith-through-physics-atoms\_runtime\canon_guard\deepseek-crown-review.md
```

Reports are written to:

```text
D:\GitHub\Faith-through-physics-atoms\_runtime\canon_guard\crown-canon-report.txt
D:\GitHub\Faith-through-physics-atoms\_runtime\canon_guard\crown-canon-report.json
D:\GitHub\Faith-through-physics-atoms\_runtime\canon_guard\crown-canon-review-packet.json
```

## What It Checks Now

- old Master Equation products that still include `C` as a tenth factor
- registry language that says `factorCount: 10`
- atom/view status drift such as `"status": "partial"`
- legacy verification fields such as `verificationStatus`, `kernelChecked`, and `challengeStatus`
- old v11 / 14-stage README language
- bare "does not prove theology" hedge language that omits the consilience posture

## Repair Rule

This version is report-first.

Equation changes should be ratified before replacement. The tool can later gain
exact safe fixes for approved text replacements, but it should not infer a new
equation from a fuzzy match.

The DeepSeek review is advisory. It can classify drift and recommend priorities,
but it does not modify files and does not ratify canon.
