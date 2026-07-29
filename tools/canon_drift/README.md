# Canon Drift

`canon-drift` is a conservative, auditable scanner for retired Master Equation forms,
encoding damage, emoji, HTML render drift, and optional canon links. It never delegates
rewriting to a model. Exact registry-approved matches can be applied; fuzzy and protected
matches remain proposals or human rulings.

Run from the repository root:

```bash
PYTHONPATH=tools/canon_drift python -m canon_drift scan path/to/documents
PYTHONPATH=tools/canon_drift python -m canon_drift report path/to/documents
PYTHONPATH=tools/canon_drift python -m canon_drift fix path/to/documents --dry-run --patch review.patch
PYTHONPATH=tools/canon_drift python -m canon_drift fix path/to/documents --apply --threshold 0.95
PYTHONPATH=tools/canon_drift python -m canon_drift html-scan path/to/site
PYTHONPATH=tools/canon_drift python -m canon_drift weekly path/to/documents --markdown --html --json-report
PYTHONPATH=tools/canon_drift python -m canon_drift autolink path/to/documents --dry-run
```

`weekly` writes JSON, Markdown, and unified-patch artifacts. `fix --apply` applies only
low-risk `safeAutoFix` entries at or above the threshold; story and raw fragment matches
remain protected. HTML mutation is deliberately disabled in v0.1: HTML is parsed by text
node and all changes remain reviewable findings.
