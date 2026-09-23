# Canon Store

Append-only, git-backed single source of truth for the unified workbench.

- `sources/` — original untouched papers and transcripts.
- `papers/` — aggregated per-paper JSON records.
- `runs/` — one folder per pipeline execution.
- `atoms/` — canonical atoms grouped by admission status.
- `predicates/` — truth predicates (true but not canon).
- `prompts/` — versioned prompt library.
- `templates/` — HTML/JSON publishing templates.

Do not edit files in place. Every change appends a new record or version.
