# Lane 4 Atom Ledger Build Report

## What was built

Lane 4 now has a standard-library Python ledger CLI, a strict JSON Schema, nine
seed atoms, per-atom append-only event arrays, and deterministic JSONL, CSV, and
Markdown projections. The per-atom JSON files are the source of truth; global
files are rebuilt projections and should not be hand-edited.

## File locations

- `_scripts/lane4_ledger.py` — CLI and validation policy.
- `_schema/lane4_atom.schema.json` — atom and event contract.
- `_ledger/atoms/*.json` — individual atom records and their event histories.
- `_ledger/LANE4_GLOBAL_CLAIM_LEDGER.jsonl` — machine event stream.
- `_ledger/LANE4_GLOBAL_CLAIM_LEDGER.csv` — spreadsheet projection.
- `_ledger/LANE4_LATEST_STATUS.md` — current human-readable rollup.
- `_scripts/test_lane4_ledger.py` — identity, rerun, and append-only tests.

## Atom identities

The readable ID is `tp:lane4/<domain>/<source-claim-id-or-title-slug>`.
Punctuation, case, and whitespace are normalized deterministically. Users do not
choose UUIDs. The immutable `atom_uid` is a SHA-256 digest of domain, lane,
optional source claim ID, title, and claim content. Lookup accepts either ID.
Renaming an artifact therefore does not change claim identity.

Event IDs are SHA-256 digests of canonical, sorted event JSON. An identical
event cannot be appended twice.

## Movement tracking

Run:

```bash
python _scripts/lane4_ledger.py move-file --old PATH --new PATH
```

The old path must already attach to an atom. The command records both paths,
before/after SHA-256 values (when readable), and `same_content`; it refuses to
create an unattached movement receipt. It does not move the file itself, making
the evidence operation explicit and safe for drives, mirrors, and archives.

## Validation

```bash
python _scripts/lane4_ledger.py validate
```

Validation rejects missing assumptions, source artifacts, or current status;
unknown proof labels; Lean-proof labels on historical claims; formal-proof
labels from Python/Colab lanes; unproved bridge theorems; formal isomorphism
below C5; old Master Equation records without `RERUN_OWED`; and duplicate event
IDs. Old Master Equation content is automatically initialized as `RERUN_OWED`.
The canonical v3 equation string is held in the CLI so rerun policy is
deterministic.

The governing rule is intentionally asymmetric: compilation or execution never
silently promotes an atom. Attach a receipt, then separately review and edit the
claim status under canon governance. Nothing is called proved unless its lane
proves that kind of claim.

## Ingesting and attaching results

Ingest JSON/JSON-LD or a text/Markdown claim:

```bash
python _scripts/lane4_ledger.py ingest path/to/claim.json
```

Attach a Lean receipt:

```bash
python _scripts/lane4_ledger.py attach-run \
  --atom tp:lane4/master-equation/cw-wrapper-not-tenth-factor \
  --lane Lean4 --result pass --artifact path/to/lean-receipt.md \
  --meaning "Guardrail theorem compiled." \
  --limits "Does not prove Master Equation dynamics." --reviewer Codex
```

For Python or Colab, use the same command with `--lane Python` or
`--lane Colab`. The proof label remains separately governed; a runtime receipt
cannot turn itself into formal proof.

Refresh outputs with `export-csv`, `make-report`, or `status`; all three rebuild
the projections. `status` also prints the report.

## Still missing

- The external `O:`, `H:`, and `D:` sources were not present in this checkout,
  so their receipts have not been ingested or independently verified.
- Canon promotion remains an intentional reviewed edit rather than an automatic
  CLI action. A later workflow may add signed reviewer approvals.
- JSON Schema validation uses the checked-in schema as an interoperability
  contract; the CLI's dependency-free validator enforces the critical canon
  rules without requiring a third-party `jsonschema` package.
- File watching is not automatic. Movement is recorded through the explicit
  command so ambiguous renames never manufacture provenance.
