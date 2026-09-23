# Claim Atom Canon v1.1 — SQL Schema

## Files

- `claim_atom_canon_v1_1_sqlite.sql` — additive SQLite target schema.
- Governing source: `THE_CLAIM_ATOM_EXPANSION_CANON_v1_1_FOUR_OBJECT_LAYERS_FULL.md`.

## Safety boundary

This schema has not been applied to `_canon/index.sqlite`. The existing database
remains untouched. The SQL is a target contract for a new database or a later
human-approved migration.

## Central design decisions

1. `atoms` stores immutable family identity only.
2. `atom_versions` stores versioned statements and the five independent axes.
3. Each atom has exactly one primary object type: CLAIM, EVIDENCE, PROOF, or
   PROCESS.
4. Type-specific burdens live in four extension families.
5. `edges` and `edge_versions` are first-class; specialized payload tables carry
   evidence, proof, process, and bridge semantics.
6. Candidate and admitted graph membership are separate rows requiring rulings.
7. Corrections never overwrite sealed history and include downstream impact and
   restoration paths.
8. Legacy IDs and `legacy_proof_label` are preserved. The new
   `one_axiom_classification` field is independent and never overwrites it.
9. OPEN questions, countermodels, kill conditions, failed claims, and negative
   results remain queryable first-class records.
10. JSON columns hold variable domain-specific payloads; identities,
    relationships, versions, receipts, and governance remain relational.

## Suggested validation command

Use Python's built-in SQLite driver without creating a persistent file:

```powershell
@'
import sqlite3, pathlib
sql = pathlib.Path(r"D:\GitHub\Faith-through-physics-atoms\__1_Version_Last_Version\claim_atom_canon_v1_1_sqlite.sql").read_text(encoding="utf-8")
db = sqlite3.connect(":memory:")
db.executescript(sql)
print("schema ok")
'@ | python -
```

## Migration order

Do not perform a repository-wide rewrite directly. Use:

```text
INVENTORY + HASH
→ LEGACY FIELD MAP
→ STAGED NEW DATABASE
→ REFERENCE VALIDATION
→ CANDIDATE GRAPH IMPORT
→ HUMAN REVIEW
→ ADMITTED MEMBERSHIP RULINGS
→ DETERMINISTIC PROJECTION REBUILD
```

The old database remains the rollback source until migration receipts, row
counts, hashes, unresolved-field reports, and human approval are complete.

## Important non-goals

- Schema conformance does not establish truth.
- A stored proof receipt does not establish a physical interpretation.
- A bridge row does not propagate proof into another register.
- An AI-created candidate cannot enter `ADMITTED` without a human ruling.
- The resolver may map an address but cannot manufacture authority.

