# GitHub Publishing Plan

Recommended public repo name:

```text
DavidLoweOKC/theophysics-lean-verification
```

That name is clearer than putting this inside a broad existing repo because the public promise is specific:

```text
Lean 4 verification package + Python/Colab mirrors for the Theophysics Master Equation.
```

## Existing DavidLoweOKC Repos

The public GitHub profile currently shows repos including:

```text
theophysics
Master-Equation-COLAB
fruits-truth-engine
theophysics-formal-papers
```

This package could go into `theophysics`, but a dedicated verification repo is easier for readers to trust, clone, and run.

## Best Reader Flow

1. Open the repo.
2. Read `READER_START_HERE.md`.
3. Run `VERIFY_ALL_WINDOWS.bat`.
4. If Lean is missing, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_lean4_windows.ps1
```

5. Reopen PowerShell.
6. Run:

```powershell
.\VERIFY_ALL_WINDOWS.bat
```

## Copy-Paste Path

For readers who do not want the full repo first:

```text
COPY_PASTE_LEAN4.lean
```

can be copied into any Lean 4 environment and checked with:

```powershell
lean COPY_PASTE_LEAN4.lean
```

This file checks the smallest standalone layer:

```text
product collapse
grace idempotence and non-invertibility
fruits gate
zero-preserving justice/mercy operator
```

## What I Need To Publish It

Codex currently does not have write access to `DavidLoweOKC`.

To publish directly, authorize/install the GitHub connector for `DavidLoweOKC`, or create an empty public repo named:

```text
theophysics-lean-verification
```

Then give Codex access and I can populate it.
