# Mothership Design Summary

## Thin faces, fat bodies

Papers keep small, version-controllable address maps (the face).  Each address
contains a `uuid`, `locator`, `anchor`, and `source` — enough to resolve and
verify a unit, but not its full semantic body.

The mothership stores the fat bodies in a central, sha256-keyed store.  Address
maps reference bodies by `sha256(anchor.exact)`.  A thin face can point to a
large, richly-annotated canonical atom without bloating the paper.

## Hash dedupe

Identities are deduplicated by exact body text hash.  Two addresses whose
`anchor.exact` hashes to the same value share one identity UUID and one body.
Occurrences still record per-document locators, preserving provenance.

## Divergence flagging

The identity store enforces one term → one sha256.  If the same term appears
with a different body, a `Divergence` is raised and recorded.  Divergences are
exposed in the nightly report for human review; they block canon promotion.

## Resolution waterfall

`resolve_address()` implements the spec order:

1. Lasers: `section_path` + `offsets`
2. Verify `sha256(exact)`
3. Fingerprint re-acquire with `exact` + `prefix`/`suffix`
4. Mark `re-aimed`, `moved`, or `lost` — never silently repoint

## Canon engine

`CanonEngine` runs a small, versioned rule set:

- required fields present
- anchor verifies against body sha256
- no divergences
- source cited
- non-empty anchor text

Each rule returns pass/fail and the receipt carries a rule version and
timestamp.

## Delta fast path

`compute_touched_addresses()` diffs old vs new document text, finds changed
character ranges, and returns addresses whose anchor window (exact expanded by
prefix/suffix) intersects a changed range.  No paper re-read, no external
dependencies.
