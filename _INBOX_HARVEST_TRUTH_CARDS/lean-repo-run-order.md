# Lean Repo Run Order

This is the recommended order for the first real Lean test. I did not run these builds yet.

## 1. Smallest Proof Pulse

Path:

`H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Lean-4-Proofs-main\Lean-4-Proofs-main\theophysics-lean-verification-package\narrow_product_test`

Why first:

- It has its own `lakefile.toml`.
- It has its own `lean-toolchain`.
- It only contains 2 Lean files under that root.
- It is the cleanest first signal before touching the larger proof forests.

Later command:

```powershell
.\RUN_LATER_LEAN_TESTS.ps1 -Target narrow
```

## 2. Theophysics Lean Main

Path:

`H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\theophysics-lean-main\theophysics-lean-main`

Why second:

- It has both `lakefile.lean` and `lean-toolchain`.
- It looks like a real project root.
- It contains 14 Lean files under that root.

Later command:

```powershell
.\RUN_LATER_LEAN_TESTS.ps1 -Target theophysics-main
```

## 3. Faith Thru Physics Lean Main

Path:

`H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Faith-Thru-Physics-Lean-4--main\Faith-Thru-Physics-Lean-4--main`

Why third:

- It has both `lakefile.lean` and `lean-toolchain`.
- It contains 24 Lean files under that root.
- It also contains repeated evidence folders, so duplicate theorem names need canonical handling.

Later command:

```powershell
.\RUN_LATER_LEAN_TESTS.ps1 -Target faith-main
```

## 4. Verification Package Scripts

Path:

`H:\Desktop 2\LEAN 4\Google CoLab Python\_EXTRACTED_REPOS\Lean-4-Proofs-main\Lean-4-Proofs-main\theophysics-lean-verification-package`

Why separate:

- It has a `lean-toolchain` but no root lakefile at that folder.
- It includes Windows runner scripts:
  - `RUN_LEAN_PRODUCTION_KERNEL.bat`
  - `VERIFY_ALL_WINDOWS.bat`

Use this after the lake roots are understood.

## Current Readiness Verdict

- Static scan found **0 real `sorry` or `admit` code holes** after comments were ignored.
- There are **3 proper lake roots** ready for later testing.
- There are **408 duplicate theorem names**, mostly from copied evidence/module folders, so the workbook should cite canonical owner files rather than every duplicate.
- The main risk is not compilation; it is public claim wording for `True`/`by trivial`/definitional theorems.
