# Atom Rail Import Notes

Status: inspection note, not import.

Source files inspected:

- `atoms_export.json`
- `atoms_insert.sql`
- `ingest_atoms.py`

These files are treated as source artifacts for the D-drive atom repository. They are not a separate project identity and should not define the canonical namespace.

## What This Rail Is

The files use a Python rail that builds atoms from CSV catalogs and writes them to a PostgreSQL table.

It is not the same as the Lane 4 append-only ledger rail, but it is compatible as an upstream or staging source.

The database table shape is:

```sql
CREATE TABLE IF NOT EXISTS atoms (
    id              SERIAL PRIMARY KEY,
    atom_id         TEXT UNIQUE NOT NULL,
    atom_type       TEXT NOT NULL,
    rail            TEXT NOT NULL,
    label           TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'extracted_not_ratified',
    data            JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

The rail can:

- dry-run atom generation
- export JSON
- export SQL
- initialize the Postgres table
- insert through `psycopg2`
- insert through `psql` CLI fallback

## Counts Observed

`atoms_export.json` contains 147 atoms:

| Atom Type | Count |
|---|---:|
| `physics_claim` | 41 |
| `theophysics_claim` | 56 |
| `mathematical_claim` | 42 |
| `physics_numbers_bridge` | 8 |

## Rail Mapping In Script

The script maps atom types to rails internally:

| Atom Type | Rail |
|---|---|
| `physics_claim` | `physics` |
| `worldview_commitment` | `worldview` |
| `bible_claim` | `scripture` |
| `theophysics_claim` | `theophysics` |
| `mathematical_claim` | `mathematics` |
| `historical_claim` | `history` |
| `bridge` | `bridge` |
| `physics_numbers_bridge` | `bridge` |

Note: the exported JSON does not include a top-level `rail` field. The rail is inferred from `atom_type` during SQL export or database insertion.

## Important Guardrail

Every exported atom is marked:

```text
status = extracted_not_ratified
```

That is the right status.

These atoms are staged, not canon.

## Strong Part

The eight `physics_numbers_bridge` atoms are disciplined. They include:

- shared predicate
- mathematical form
- physics bearer
- numbers bearer
- bridge grade
- kill condition
- falsifier
- negative controls
- rival explanations
- evidence separation
- God-grounding bridge requirement

This is the pattern the General Theory scaffold should imitate.

Especially important:

```text
God-side grounding is a separate bridge.
```

That prevents a physics-to-math bridge from silently becoming a proof of God.

## Mismatch With Lane 4 Ledger

The Postgres atom format is not identical to `_schema/lane4_atom.schema.json`.

Main differences:

- The source export uses `claim_id`; Lane 4 uses deterministic `atom_id` plus `atom_uid`.
- The source export stores rich data inside JSONB `data`; Lane 4 expands fields like assumptions, definitions, equations, bridges, dependencies, negative guards, kill conditions, and ledger events.
- The source export has no append-only per-atom event ledger.
- The source export infers `rail`; Lane 4 stores `lane`.
- The source export statuses are staging statuses; Lane 4 statuses interact with proof labels and rerun status.

## Recommended Adapter

Create a Python adapter rail:

```text
atoms_export.json
  -> normalize rails
  -> add source_artifacts
  -> map atom_type to claim_class/lane
  -> preserve original atom as source_data
  -> add negative guards
  -> add proof_label = NOT_ESTABLISHED unless evidence status demands lower/other label
  -> create draft Lane 4 candidate atoms
  -> validate
  -> render preview mind map
```

Do not import directly.

## Proposed Mapping To Lane 4 Candidate Fields

| Source Field | Lane 4 Candidate Field |
|---|---|
| `claim_id` / `bridge_id` | `source_claim_id` |
| `label` | `title` |
| `claim.proposition` | `claim` |
| `atom_type` | `claim_class` |
| inferred rail | `lane` |
| `truth_conditions` | `definitions` or `assumptions` |
| `disconfirmation_conditions` | `kill_conditions` |
| `source_anchors` | `source_artifacts` plus source metadata |
| `negative_guards` / `negative_controls` | `negative_guards` |
| `mathematical_form` | `equations` |
| bridge object | `bridges` |
| full source atom | `classification_bundle.source_atom` |

## Relation To General Theory Scaffold

The export proves the Python rails pattern already exists:

```text
catalog CSVs -> Python builder -> atom JSON -> SQL/DB/API rail
```

The General Theory scaffold should use the same style:

```text
general_theory_atoms.v0.1.json
  -> Python proposal validator
  -> duplicate/reconciliation check
  -> preview graph/mind map
  -> optional Lane 4 import
```

## Next Practical Step

Build `_scripts/ingest_general_theory_proposal.py` or similar with these modes:

```text
--dry-run
--validate
--export-json
--export-sql
--preview-mindmap
--lane4-candidates
```

Keep database insertion and Lane 4 import separate.

The database is good for browsing/querying.
The Lane 4 ledger is good for proof/status governance.
