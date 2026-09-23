# Definition Registry v1.0

**Status:** candidate specification  
**Date:** 2026-09-22  
**Companion:** [`DEFINITION_PILLS_SEED_v0.1.md`](DEFINITION_PILLS_SEED_v0.1.md) — the pill principle applied one level up.

## 1. Purpose

This document defines the **canonical definition registry** for the Faith Through Physics / Theophysics project. It turns every term into a **thin handle + fat store** pill:

- The **registry row** is a small, greppable, version-controlled file that gives an API or AI worker everything needed to *resolve* a definition.
- The **full record** (the atom) lives elsewhere and carries the 100–200-field body: source spans, usage sites, dispute notes, definition-lane Q&A, grading history, receipts, and rulings.
- The **UUID** is the immutable join key. Terms may change; meanings may split; the UUID never moves.

The registry is a **resolver table**, not the source of truth. If a registry row ever disagrees with its full record, the full record wins and the row regenerates.

## 2. Registry row schema

Each row is one YAML file in `_definitions/registry/`.

```yaml
---
# _definitions/registry/DEF-0142.yaml  — a registry row (a pill)
definition_id: DEF-0142
uuid: 8f14e45f-ceea-5d1a-9f3f-230c4b09cbe7   # minted ONCE, immutable, never reused
term: coherence
plain: parts working together without fighting   # one line, display only
status: candidate            # candidate | canonized | retired
full_record: _definitions/atoms/DEF-0142.jsonld
sha256: a667b7b0e2e8e6c5b0d6e4f3a2b1c9d8e7f6a5b4c3d2e1f0a1b2c3d4e5f6a7b8  # hash of full record
---
```

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `definition_id` | yes | Human-readable permanent ID, prefixed `DEF-`. Stable across versions. |
| `uuid` | yes | Immutable UUID (v4 or v5 in project namespace). Minted once, never reused, never reassigned. |
| `term` | yes | Canonical term. May be renamed in place only if meaning is unchanged; if meaning splits, mint a new row. |
| `plain` | yes | One-line, Monday-morning definition. Display/cache only. Projection of `exact_definition` in the full record. |
| `status` | yes | `candidate`, `canonized`, or `retired`. |
| `full_record` | yes | Relative path from repo root to the JSON-LD atom that owns the body. |
| `sha256` | yes | SHA-256 of the full record file. Drift detection. |

## 3. Full record (the atom)

The full record is a JSON-LD file validated by [`_schema/definition_record_v1.schema.json`](../../_schema/definition_record_v1.schema.json). It contains the substantive definition data:

- `definition_id` and `uuid` (mirrors the registry row)
- `canonical_term`, `aliases`, `forbidden_equivalences`
- `exact_definition` (technical), `plain_definition`, `scope`
- `source` with exact short quotations, authoritative URLs, source hashes
- `citation_policy` (`required`, `inheritToDependents`)
- `dependencies`, `supersedes`
- `definition_lane` fields: ordinary definition, disciplinary definition, disputes, Theophysics use
- `grading_history`, `receipts`, `adversarial_gate_status`, `human_ruling`

The full record is the **source of truth**. Every field in the registry row is a cache of some slice of the full record.

## 4. State machine

```
      extraction / minting
              │
              ▼
        ┌──────────┐
        │ candidate │  ← provisional everywhere
        └────┬──────┘
             │ human PR gate approves
             ▼
        ┌──────────┐
        │ canonized │  ← safe to cite as settled
        └────┬──────┘
             │ human PR gate retires / falsifies / supersedes
             ▼
        ┌──────────┐
        │  retired  │  ← still resolvable; never deleted
        └──────────┘
```

- **candidate** — the definition has been extracted and has a UUID, but it has not passed the review gate. Papers may reference it, but must render it as provisional.
- **canonized** — the review gate has accepted the definition. It becomes a stable citation target.
- **retired** — the definition was falsified, superseded, or withdrawn. The UUID still resolves to its corpse so the ledger stays inspectable. A retired row is never reassigned to a new term.

Status changes are **one-line edits** in the registry row. Because every consumer resolves through the UUID and reads status from the registry, the change propagates on the next run without touching the full record or any citing paper.

## 5. Minting rules

1. **UUIDs are minted at birth.** When a definition is first extracted from a paper, the pipeline generates a UUID and writes the candidate row before the full record is complete.
2. **UUIDs are immutable.** The same UUID follows the definition through candidate → canonized → retired.
3. **UUIDs are never reused.** Even if a definition is retired, its UUID stays attached to that corpse. A new sense of an old term gets a new UUID and a new row.
4. **Definition IDs are sequential.** `DEF-0001`, `DEF-0002`, etc. The ID is a display handle; the UUID is the join key.
5. **One row per meaning.** If the term "coherence" later splits into two senses, there are two rows (`DEF-0142` and `DEF-0234`) with two UUIDs. The original term field may be disambiguated (`coherence (constraint sense)`, `coherence (informational sense)`).

## 6. Lifecycle flow

### 6.1 Extraction
A paper or source runs through `_scripts/definition_resolver.py` or an equivalent API pipeline. Candidate definitions are minted with UUIDs and written to the **canonization inbox** (`_proposals/definition-links.jsonl` and `_definitions/atoms/*.jsonld` drafts).

### 6.2 Registry write
A thin row is created automatically in `_definitions/registry/DEF-XXXX.yaml`. Face visible, body pending.

### 6.3 Canonization
The definition lane review opens the full record:

1. Ordinary-language definition
2. Disciplinary definition
3. Disputes and objections
4. Theophysics use and classification

Grading history and receipts accumulate in the full record only.

### 6.4 Ruling
The PR gate (human review) flips `status: candidate → canonized`. Until then, every paper referencing the UUID renders it as provisional. The flip is one line in one file.

### 6.5 Reference
Papers, claims, and bridges cite the UUID. Meaning survives renames. Splits become new rows. Drift is detectable by `sha256` mismatch.

## 7. Guards

### 7.1 Registry rows are a cache, not a source
If `plain` in the row disagrees with `plain_definition` or `exact_definition` in the full record, the full record wins and the row regenerates. The resolver regenerates `_definitions/registry.jsonld` from the row folder; no consumer should treat the JSON-LD as primary.

### 7.2 UUIDs are never reused
Retired UUIDs remain in `_definitions/registry/` with `status: retired`. The full record remains in `_definitions/atoms/`. Deletion is forbidden; the ledger must stay inspectable.

### 7.3 Status is the single gate
A consumer decides whether to trust a definition by reading `status` from the registry row. It does not infer authority from file location, term popularity, or citation count.

## 8. File layout

```
_definitions/
  registry/
    DEF-0001.yaml          # thin rows (this spec)
    DEF-0002.yaml
    DEF-0142.yaml
  atoms/
    DEF-0001.jsonld        # fat full records
    DEF-0002.jsonld
    DEF-0142.jsonld
  evidence/
    goedel-sep.jsonld      # source/evidence nodes
  registry.jsonld          # generated resolver aggregate (cache)
_proposals/
  definition-links.jsonl   # extracted link proposals
_scripts/
  definition_resolver.py   # resolve, validate, render
_schema/
  definition_record_v1.schema.json   # full record schema
```

## 9. Validation

`_scripts/definition_resolver.py validate` (or its v1.0 successor) enforces:

1. Every row has a unique `definition_id` and a unique `uuid`.
2. Every `full_record` path exists and parses as valid JSON-LD against `_schema/definition_record_v1.schema.json`.
3. `sha256` in the row matches the hash of the full record file.
4. `status` in the row matches `canonicalStatus` / status in the full record.
5. `term` and `plain` in the row match the projected fields in the full record.
6. No alias is owned by more than one canonized or candidate definition.
7. Retired UUIDs are still present in `_definitions/registry/` and `_definitions/atoms/`.

## 10. Integration with existing work

- **`_definitions/registry.jsonld`** becomes a generated aggregate. The YAML row folder is the master; the JSON-LD is the machine-readable cache consumed by `_scripts/definition_resolver.py`.
- **`_schema/definition_record_v1.schema.json`** already describes the full record. v1.0 extends its `status` enum to `candidate | canonized | retired` and adds `uuid` as a required field.
- **`_scripts/definition_resolver.py`** already resolves `[[def:...]]` markers and validates registry/atom consistency. It is extended to read YAML rows, regenerate `registry.jsonld`, and verify `sha256`.
- **Theophysics_Tagger / `canonical_186_sources.txt`** are definition registries that grew up without UUIDs. v1.0 migrates them by minting one row per tag/source and attaching a UUID; the old string IDs become `aliases` or `legacy_id` fields inside the full record.
- **FIS lossless address** on file rows is the same pattern: a small handle pointing at a fat record. The registry applies that pattern to definitions.
- **Definition pills** (`DEFINITION_PILLS_SEED_v0.1.md`) supply the `plain` text and the `is-not` guard. A pill becomes a registry row when it is promoted from seed to canonical candidate.

## 11. Migration from current registry

The existing `_definitions/registry.jsonld` has three entries (`tp:def:terminus-sui`, `tp:def:goedel-incompleteness`, `tp:def:master-equation/grace`). Migration to v1.0:

1. Mint a UUID for each existing definition.
2. Create `_definitions/registry/DEF-XXXX.yaml` for each, mapping the old `permanentDefinitionID` into the full record as a legacy alias.
3. Move or copy the existing atoms in `_definitions/atoms/` to the v1.0 full-record schema.
4. Generate `_definitions/registry.jsonld` from the rows.
5. Update `_scripts/definition_resolver.py` to consume the generated JSON-LD while keeping `[[def:...]]` marker behavior unchanged.

## 12. References

- [`DEFINITION_PILLS_SEED_v0.1.md`](DEFINITION_PILLS_SEED_v0.1.md)
- [`_docs/CANONICAL_DEFINITION_REGISTRY.md`](../../_docs/CANONICAL_DEFINITION_REGISTRY.md)
- [`_schema/definition_record_v1.schema.json`](../../_schema/definition_record_v1.schema.json)
- [`_scripts/definition_resolver.py`](../../_scripts/definition_resolver.py)
- [`_definitions/registry.jsonld`](../../_definitions/registry.jsonld)
