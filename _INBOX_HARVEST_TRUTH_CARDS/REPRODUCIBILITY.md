# Reproducibility

## Requirement

Install Lean through `elan`:

- https://github.com/leanprover/elan

The repo pins the Lean version in `lean-toolchain`.

## Build command

From the repository root:

```bash
lake build
```

Expected result:

```text
Build completed successfully
```

You may see Lean `info` messages from `#check_failure` in `Theophysics_Adversarial.lean`. That is expected. Those lines intentionally ask Lean to reject false statements.

You may also see linter warnings in older scaffold files. Warnings are not proof failures. A failed build is different: it stops with an error.

## Why this is reproducible

The repo includes:

- `lean-toolchain` for the Lean version.
- `lakefile.lean` for the Lake package.
- the Lean source files.

No private desktop paths are required for the build.
