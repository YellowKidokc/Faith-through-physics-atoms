# Lean 4 Setup Guide

This guide is for readers who want to verify the Lean proofs themselves.

Lean is not installed like an ordinary one-version program. The normal route is to install **elan**, the Lean version manager. Then this repo's `lean-toolchain` file tells elan which Lean version to use.

Official install page:

```text
https://lean-lang.org/install/manual
```

## Fast Path On Windows

Open PowerShell in the repo folder and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_lean4_windows.ps1
```

Then close and reopen PowerShell so the PATH refreshes.

After that, run:

```powershell
.\VERIFY_ALL_WINDOWS.bat
```

## Manual Windows Install

1. Install Git for Windows if you do not already have it.
2. Install elan:

```powershell
curl -O --location https://raw.githubusercontent.com/leanprover/elan/master/elan-init.ps1
powershell -ExecutionPolicy Bypass -File .\elan-init.ps1
Remove-Item .\elan-init.ps1
```

3. Close and reopen PowerShell.
4. Confirm Lean and Lake are visible:

```powershell
lean --version
lake --version
```

5. In this repo folder, run:

```powershell
lean TheophysicsProductionKernel.lean
lean CorrectedEntropyKernel.lean
```

6. For the Mathlib-backed proof test:

```powershell
cd narrow_product_test
lake exe cache get
lake env lean NarrowProductTest/Basic.lean
lake env lean NarrowProductTest.lean
```

## VS Code

Lean is easiest to inspect in VS Code with the official Lean 4 extension.

If VS Code is installed and available as `code`, run:

```powershell
code --install-extension leanprover.lean4
code .
```

Open a `.lean` file. If the Lean Infoview appears and the file has no red errors, Lean is checking the proof.

## What Counts As Verified

A Lean file has passed when the command exits without errors:

```powershell
lean SomeFile.lean
```

or, inside a Lake project:

```powershell
lake env lean SomeFile.lean
```

For this repo, the public verification target is:

```text
TheophysicsProductionKernel.lean
CorrectedEntropyKernel.lean
narrow_product_test/NarrowProductTest/Basic.lean
```

## Common Problems

### `lean is not recognized`

Close and reopen PowerShell. If it still fails, elan is not on PATH.

Try:

```powershell
$env:Path += ";$env:USERPROFILE\.elan\bin"
lean --version
```

### `git is not recognized`

Install Git for Windows:

```text
https://git-scm.com/download/win
```

Then reopen PowerShell.

### Mathlib download is slow

The first Mathlib-backed run may take time. This is normal. The command:

```powershell
lake exe cache get
```

downloads prebuilt Mathlib artifacts when available.

## Why Lean Matters Here

The Python files demonstrate behavior. Lean checks proof obligations.

So the right public claim is:

```text
Python shows examples and counterexamples.
Lean verifies the formal structural claims.
```
