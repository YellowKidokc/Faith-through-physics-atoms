# Quote Packet Guard

This folder now contains the Terminus Sui quote guard.

## What it protects

If a document uses Terminus Sui, five-limit, five-theorem, or five-impossibility language, it must carry the source quote packet. The outside sources own their theorems. Theophysics owns the synthesis.

The enforced rule is:

`TERMINUS_SUI_QUOTE_PACKET`

## Where the code lives

- Main guard code: `canon_guard/canon_guard.py`
- Rule manifest: `canon_guard/canon-manifest.toml`
- Easy launcher: `RUN_CANON_GUARD.ps1`

## How to run

From this folder:

```powershell
.\RUN_CANON_GUARD.ps1 -ProjectRoot "C:\path\to\theophysics"
```

For JSON output:

```powershell
.\RUN_CANON_GUARD.ps1 -ProjectRoot "C:\path\to\theophysics" -Output "canon-report.json"
```

## Required quote anchors

The manifest currently requires anchors for:

- Godel incompleteness: `Any consistent formal system`
- Godel consistency-from-outside: `Consistency will never be intrinsic to the system`
- Tarski internal truth: `Any theory extending first-order arithmetic`
- Turing halting: `There exists no Turing machine deciding the halting problem`
- Thermodynamic entropy: `entropy can never decrease`
- Landauer reset cost: `kT ln 2`

If those anchors are missing, Canon Guard reports an error instead of letting AI blur source authority and Theophysics interpretation.
