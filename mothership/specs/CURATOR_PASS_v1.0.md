# CURATOR PASS v1.0 — the corpus asks what to run next

**Status:** candidate specification  
**Date:** 2026-09-22  
**POF:** 2828 — Faith-through-physics-atoms  
**Companions:** [`DEFINITION_REGISTRY_v1.0.md`](../../unification/01_middle_seed/DEFINITION_REGISTRY_v1.0.md), [`UNIVERSAL_ADDRESS_SPEC_v1.0.md`](../../unification/01_middle_seed/UNIVERSAL_ADDRESS_SPEC_v1.0.md)

## 1. Purpose

The Curator Pass is a read-only, corpus-wide planning process that inspects the
current state of all pills, address maps, identities, and tests and proposes
what the next build should do.  It does **not** edit papers, flip statuses, or
mint UUIDs for anything it did not extract from source text.  It only produces
a ranked `build_next` queue of proposals for human review.

The curator closes the loop between:

- the thin **pills** and **address maps** that papers keep,
- the fat **bodies** and **identities** stored in the mothership,
- the **definition registry** that governs terms,
- and the **test/falsification receipts** that guard claims.

## 2. Cadence

- **Nightly cron:** automated hands — fill, pill, validate, resolve addresses,
  update receipts.
- **Curator Pass:** weekly eyes — scan the whole corpus, rank gaps, emit one
  `build_next` queue as a ruling PR.

The curator is intentionally slower than the nightly pipeline because its
output is a proposal set that humans rule on.

## 3. Input

The curator reads, but never writes:

| Input | Source | Purpose |
|-------|--------|---------|
| Pills | `mothership/pills/` or configured `pills_dir` | Tiny, greppable faces of atoms |
| Address maps | `_runtime/addresses/` or configured `address_maps_dir` | Per-document occurrence lists |
| Identity store | `mothership.identity_store.IdentityStore` | Deduplicated bodies + divergences |
| Bodies | `mothership/tests/sample_data/bodies/` or configured `bodies_dir` | Fat text pulled on demand |
| Tests / receipts | Pill `receipts` and `falsificationCondition` fields | Guard status |

Bodies are fetched on demand via the pill's own address (self-API pattern):
read `anchor.sha256`, pull the matching body file, resolve the address.

## 4. Output

A single `build_next` queue: a JSON list of proposal atoms, sorted by priority.
Each proposal has `status: proposed` and a receipt.  The queue is regenerated
from scratch on every curator run; it is a refreshable view, not a persistent
backlog.

The queue is posted as a **ruling PR** for human review.  The PR contains the
queue JSON, a summary, and links to each affected pill/identity.

## 5. Proposal types

| Type | Trigger | Human action |
|------|---------|--------------|
| `extract` | Atom-shaped content with no address or no resolvable body | Mint address + identity from source text |
| `define` | Term in use with no definition registry entry | Open `DISCOVERY_INCOMPLETE` lane; draft definition |
| `link` | Cross-paper support/contradiction with no recorded edge | Draw/reject the proposed edge |
| `cover` | Paper address map exists but has no pills | Run the full ingestion pipeline on the paper |
| `diverge` | Same term mapped to different sha256s with no ruling | Adjudicate meaning split, retirement, or merge |
| `test` | Kill/falsification condition registered but never tested | Run the test and record receipt |
| `meta` | Curator process gap detected by self-inspection | Improve the curator through the same PR gate |

## 6. Proposal object schema

```json
{
  "proposal_id": "PROP-0001",
  "type": "diverge",
  "targets": [
    "8f14e45f-ceea-5d1a-9f3f-230c4b09cbe7",
    "a3f7..."
  ],
  "reason": "Term 'grace-claim' maps to 3 distinct sha256 bodies with no human ruling.",
  "expected_yield": 0.9,
  "priority": 1,
  "status": "proposed",
  "receipt": {
    "curator_version": "2026-09-22.v1",
    "rule_version": "2026-09-22.v1",
    "timestamp": "2026-09-22T12:00:00Z",
    "generator": "CuratorPass"
  }
}
```

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `proposal_id` | yes | Sequential human-readable ID, prefixed `PROP-`. |
| `type` | yes | One of the proposal types above. |
| `targets` | yes | UUIDs or nodeIDs the proposal acts on. |
| `reason` | yes | Human-readable justification. |
| `expected_yield` | yes | 0.0–1.0 float or short string describing payoff. |
| `priority` | yes | Integer; lower is higher priority. |
| `status` | yes | Always `proposed`. |
| `receipt` | yes | Version, rule version, timestamp, generator. |

## 7. Ranking / priority rules

Default priority bands (lower number = higher priority):

1. `diverge` — semantic splits corrupt the ledger if left unresolved.
2. `test` — falsification guards must be exercised.
3. `extract` — missing atoms block downstream linking.
4. `define` — undefined terms block precise grading.
5. `link` — edges are cheap once identities exist.
6. `cover` — backfill for thin papers.
7. `meta` — curator self-improvement is lowest because it is recursive.

Within a band, proposals are sorted by `expected_yield` descending, then by
target count ascending.

## 8. Guards (constitution, one level up)

### C1 — Curator is a process atom
Every run emits a versioned, receipted, reproducible artifact.  The receipt
includes `curator_version`, `rule_version`, `timestamp`, and `generator`.

### C2 — Everything it suggests enters as `status: proposed`
The curator never admits anything.  All proposals await human ruling.

### C3 — Read-only with respect to papers and statuses
- Never edits paper files.
- Never flips `candidate` ↔ `canonized` ↔ `retired`.
- Only mints UUIDs when extracting from actual source text (not done by the
  curator itself; that is the `extract` proposal's human action).

### C4 — Proposals are themselves atoms
Each proposal has a stable `proposal_id`, a receipt, and a retireable status.
They can be ruled on, corrected, or retired through the same gate.

### C5 — Recursive self-application
The curator can propose improvements to the curator process.  These `meta`
proposals pass through the same PR gate as any other proposal.

## 9. Process flow

```
┌─────────────────┐
│  ingest inputs  │  pills, address maps, identity store, bodies
└────────┬────────┘
         ▼
┌─────────────────┐
│  detect gaps    │  extract / define / link / cover / diverge / test / meta
└────────┬────────┘
         ▼
┌─────────────────┐
│  score & rank   │  priority band + expected_yield
└────────┬────────┘
         ▼
┌─────────────────┐
│  emit queue     │  build_next JSON + ruling PR text
└─────────────────┘
```

## 10. Integration

- **Mothership:** the curator reuses `IdentityStore` for divergences and
  deduplication, and `resolve_address()` for on-demand body resolution.
- **Definition Registry:** `define` proposals are triggered when a `definition`
  target's term is not represented by an identity or registry row.
- **Universal Address Spec:** every proposal that touches an address references
  its immutable `uuid`; occurrences stay version-bound.
- **Atom-to-pill converter:** `mothership/tools/atom_to_pill.py` produces the
  pill corpus the curator consumes.

## 11. File layout

```
mothership/
  specs/
    CURATOR_PASS_v1.0.md      # this spec
  mothership/
    curator.py                # CuratorPass implementation
  tools/
    atom_to_pill.py           # JSON-LD -> YAML pill converter
  pills/                      # generated pill corpus
  proposals/
    build_next.json           # generated queue (ruling PR artifact)
```

## 12. References

- [`DEFINITION_REGISTRY_v1.0.md`](../../unification/01_middle_seed/DEFINITION_REGISTRY_v1.0.md)
- [`UNIVERSAL_ADDRESS_SPEC_v1.0.md`](../../unification/01_middle_seed/UNIVERSAL_ADDRESS_SPEC_v1.0.md)
- [`mothership/mothership/curator.py`](../../mothership/mothership/curator.py)
- [`mothership/tools/atom_to_pill.py`](../../mothership/tools/atom_to_pill.py)
