# Universal Address Spec v1.0

**Status:** candidate specification  
**Date:** 2026-09-22  
**POF:** 2828 — Faith-through-physics-atoms  
**Companions:** [`DEFINITION_REGISTRY_v1.0.md`](DEFINITION_REGISTRY_v1.0.md), [`DEFINITION_PILLS_SEED_v0.1.md`](DEFINITION_PILLS_SEED_v0.1.md)

## 1. Purpose

This spec defines a single addressing scheme that can **pinpoint any unit — a word, sentence, claim, proof, definition, equation, table, or figure — inside any paper, in any version, forever**.

The address has three layers:

- **IDENTITY** — the `uuid`. Minted once at first ingestion, immutable, never reused. This is what the rest of the system references.
- **LOCATOR** — the `section_path` and character `offsets`. The lasers: fast, precise, version-bound.
- **ANCHOR** — the exact text, prefix/suffix fingerprint, and `sha256(exact)`. The memory: verifies the locator and re-acquires the target if the document drifts.

A unit is a persistent identity. Each place it appears is an **occurrence**, and each occurrence has its own locator + anchor inside a specific document version.

## 2. Address object schema

```json
{
  "uuid":        "8f14e45f-ceea-5d1a-9f3f-230c4b09cbe7",
  "handle":      "MEQ/GRACE/§3.1.4",
  "target_type": "claim",
  "locator": {
    "section_path": [3, 1, 4],
    "offsets":      [1247, 1389]
  },
  "anchor": {
    "exact":   "The wrapper is outside the product, not a tenth ingredient.",
    "prefix":  "...therefore the governing form must satisfy",
    "suffix":  "; this is what makes the veto property structural...",
    "sha256":  "a667b7b0e2e8e6c5b0d6e4f3a2b1c9d8e7f6a5b4c3d2e1f0a1b2c3d4e5f6a7b8"
  },
  "source": {
    "doc_uuid":   "doc-019f-4a2c-8e7b-...",
    "doc_sha256": "b8f7a6e5d4c3b2a1..."
  }
}
```

### Field reference

| Field | Layer | Required | Description |
|-------|-------|----------|-------------|
| `uuid` | identity | yes | Minted once at ingestion. Immutable. Never reused. The only stable reference. |
| `handle` | identity | no | Human-readable label, MEQ-style. Convenience only; may change. |
| `target_type` | identity | yes | `word \| sentence \| claim \| proof \| definition \| equation \| table \| figure`. Other types may be added by schema amendment. |
| `locator.section_path` | locator | yes | Array of zero-based indices: `[3,1,4]` = section 3, subsection 1, unit 4. The lasers. |
| `locator.offsets` | locator | yes | `[start, end]` character offsets within that document version. |
| `anchor.exact` | anchor | yes | The target text, verbatim. |
| `anchor.prefix` | anchor | yes | ~40 characters before `exact`, for drift recovery. |
| `anchor.suffix` | anchor | yes | ~40 characters after `exact`, for drift recovery. |
| `anchor.sha256` | anchor | yes | `sha256(anchor.exact)`. One hash, one target. |
| `source.doc_uuid` | source | yes | The document's permanent identity. |
| `source.doc_sha256` | source | yes | The document version hash. Binds the locator to an exact version. |

## 3. The three rules

### R1 — IDENTITY vs OCCURRENCE

The same unit in two different papers is **one `uuid`, two occurrences**.

- Identity is deduplicated by `sha256(exact)` across the corpus.
- Occurrence is per-document-version and carries its own `locator` and `source.doc_sha256`.

### R2 — RESOLUTION WATERFALL

Resolve an address in this order, stopping at the first success:

1. **Lasers first** — use `section_path` + `offsets` to find the text in the current document version.
2. **Verify anchor** — hash the text at those offsets and compare to `anchor.sha256`.
3. **If drifted** — use `anchor.exact` + `prefix`/`suffix` as a fingerprint to re-acquire the target in the current version.
4. **If found** — update the occurrence's `locator` (`section_path`, `offsets`). The `uuid` is untouched. Mark status `re-aimed`.
5. **If NOT found** — mark the occurrence `moved` (found elsewhere with a forward pointer) or `lost` (unrecoverable). Never silently repoint.

> Canon principle: edges do not silently retarget.

### R3 — MINT AT INGESTION

Wild papers carry no UUIDs. The pipeline mints an identity, anchors it, and grid-maps every extracted unit on entry.

- Ingestion creates the identity + first occurrence.
- Any later edit produces a new `doc_sha256` and triggers re-anchoring of occurrences; the identity `uuid` persists.

## 4. Status vocabulary

Every occurrence carries a resolution status. The vocabulary is exhaustive; there is no silent state.

| Status | Meaning |
|--------|---------|
| `resolved` | Lasers hit the target and `sha256(exact)` verified. |
| `re-aimed` | Drift was detected; the target was re-acquired by anchor fingerprint and the lasers were updated. |
| `moved` | The content exists elsewhere in the document; a forward pointer to the new occurrence is supplied. |
| `lost` | The anchor is unrecoverable in the current version. The `uuid` stays resolvable to its last-known-good address + history. |

## 5. Resolution waterfall (detailed)

```
┌─────────────────┐
│  given address  │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ 1. lasers (section_path  │
│    + offsets)            │
└────────┬─────────────────┘
         │ hit?
         ▼ yes
┌──────────────────────────┐
│ 2. verify sha256(exact)  │
└────────┬─────────────────┘
         │ match?
         ▼ yes
      resolved
         │ no
         ▼
┌──────────────────────────┐
│ 3. fingerprint re-acquire│
│    exact + prefix/suffix │
└────────┬─────────────────┘
         │ found?
         ▼ yes
   re-aimed (update lasers)
         │ no
         ▼
   moved ──► forward pointer
     or
   lost ──► last-known-good + history
```

## 6. Target types

The minimal required vocabulary:

- `word` — a single term or symbol.
- `sentence` — a grammatical sentence.
- `claim` — an assertion that can be graded.
- `proof` — an inferential step or argument block.
- `definition` — a definition atom (links to the definition registry).
- `equation` — a mathematical expression.
- `table` — tabular data.
- `figure` — image, diagram, or chart.

New target types are added by schema amendment and must include a canonical example before acceptance.

## 7. File layout

```
_runtime/
  addresses/
    <doc_uuid>/
      <doc_sha256>.jsonl    # one occurrence per line
  address_index.jsonld      # generated map: uuid -> latest occurrence

canon/
  atoms/
    <uuid>.jsonld           # identity record: the unit's canonical atom

_definitions/
  registry/
    DEF-0142.yaml           # definition registry row (uuid, term, status)
  atoms/
    DEF-0142.jsonld         # definition full record
```

Each line in a per-document address file is an occurrence. The identity atom lives with the rest of the project's atom store (canon or `_definitions`).

## 8. Integration with existing systems

- **Definition registry** — a definition's `uuid` is its identity. The registry row in `_definitions/registry/DEF-XXXX.yaml` stores the identity; the full record stores occurrences and anchors.
- **Claim atoms** — replace ad-hoc `sourceReference` strings (file paths, workbook rows) with a proper `address` object. The claim atom's `uuid` is its identity; every cited source location is an occurrence.
- **FIS lossless address** — the existing "small handle → fat record" pattern on file rows is the same idea applied at file granularity. This spec extends it to sub-document units.
- **`_runtime/anchor_lines/`** — the runtime's existing anchor output becomes a legacy source of `anchor.exact` / `prefix` / `suffix` candidates. New ingestion should emit occurrences in the v1.0 address format.
- **Web Annotation / Xanadu** — see Prior Art below. This spec is the project's convergence of those models with immutable minted identity.

## 9. Prior art

- **Ted Nelson, Xanadu "tumblers" (1960s)** — decimal tree addresses (`top-level.x.sub-level`) that locate content in a hierarchical document. The `section_path` in this spec is a direct descendant of the tumbler idea.
- **W3C Web Annotation Data Model** — defines `exact` / `prefix` / `suffix` selectors for anchoring text. The anchor layer of this spec is aligned with that standard.

This spec = **tumblers + Web Annotation selectors + minted identity**.

## 10. Migration from current references

Current claim atoms use `sourceReference` with local file paths and workbook coordinates. Migration to v1.0:

1. For every cited source location, mint an identity `uuid` (or reuse one if `sha256(exact)` already exists in the corpus).
2. Create an occurrence in `_runtime/addresses/<doc_uuid>/<doc_sha256>.jsonl`.
3. Replace `sourceReference` with an `address` object containing `uuid`, `locator`, `anchor`, and `source`.
4. Keep the old `sourceReference` as `legacySourceReference` until all consumers are upgraded.

## 11. Edge cases

- **Empty or whitespace-only exact** — rejected at ingestion. An address must point to non-empty semantic text.
- **Duplicate `sha256(exact)` in the same document** — treated as separate occurrences only if `locator` differs; otherwise deduplicated.
- **Document split or merge** — produces new `doc_uuid`s. Occurrences in the old document are marked `moved` with forward pointers to the new document occurrences.
- **Character encoding changes** — offsets are always UTF-8 character counts. A change in encoding without content change does not alter `doc_sha256`, but consumers must normalize before applying offsets.

## 12. References

- [`DEFINITION_REGISTRY_v1.0.md`](DEFINITION_REGISTRY_v1.0.md)
- [`DEFINITION_PILLS_SEED_v0.1.md`](DEFINITION_PILLS_SEED_v0.1.md)
- [`_docs/CANONICAL_DEFINITION_REGISTRY.md`](../../_docs/CANONICAL_DEFINITION_REGISTRY.md)
- [`_schema/definition_record_v1.schema.json`](../../_schema/definition_record_v1.schema.json)
- [`_scripts/definition_resolver.py`](../../_scripts/definition_resolver.py)
- [`_runtime/anchor_lines/`](../../_runtime/anchor_lines/)
