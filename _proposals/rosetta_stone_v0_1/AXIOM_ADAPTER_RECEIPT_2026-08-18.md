# AXIOM → ROSETTA ADAPTER RECEIPT

Date: 2026-08-18  
Status: candidate proposal / local verification only  
Boundary: adapter projection and structural routing only. No source atom was edited; no result is proof, admission, canonization, promotion, or a truth verdict.

## Files Added

- `_proposals/rosetta_stone_v0_1/AXIOM_ROSETTA_ADAPTER_STANDARD.md`
- `_proposals/rosetta_stone_v0_1/axiom_rosetta_node.schema.json`
- `_proposals/rosetta_stone_v0_1/axiom_to_rosetta_node.py`
- `_proposals/rosetta_stone_v0_1/AXIOM_ADAPTER_RECEIPT_2026-08-18.md`

No existing Rosetta Stone v0.1 file was changed.

## Source Corpus

- Source folder: `axioms/01_canonical/`
- Source records read: `191`
- Source records modified: `0`

## Adapter Result

- Envelopes emitted: `191`
- Duplicate `node_id` values: `0`
- Adapter validation errors: `0`
- JSON Schema validation errors: `0`

## Native Claim Classes Read

| Native class | Count |
|---|---:|
| `theorem` | 51 |
| `floor_axiom` | 45 |
| `definition` | 38 |
| `empirical_anchor` | 18 |
| `mathematical` | 13 |
| `boundary` | 9 |
| `prediction` | 8 |
| `empirical` | 5 |
| `bridge` | 3 |
| `theological_interpretation` | 1 |

## Adapter-Candidate Unified Types

These are mechanical adapter candidates, not canon classifications.

| Unified type | Count |
|---|---:|
| `HYPOTHESIS` | 41 |
| `DEFINITION` | 38 |
| `THEOREM` | 27 |
| `BOUNDARY` | 18 |
| `CLOSURE` | 15 |
| `LEMMA` | 15 |
| `MODEL` | 13 |
| `PROTOCOL` | 8 |
| `EVIDENCE` | 6 |
| `BRIDGE` | 3 |
| `COROLLARY` | 2 |
| `OPEN` | 2 |
| `PREDICTION` | 2 |
| `IDENTIFICATION` | 1 |

## Exact-ID Hint Counts

Exact-ID hints are routing hints only, not semantic matches.

| Hint type | Count |
|---|---:|
| Keeper-deck exact ID | 13 |
| Proof-stack exact ID | 10 |
| Chain-layer exact ID | 5 |

## Compatibility Tests

### JSON Schema

All `191` generated envelopes validate against:

- `axiom_rosetta_node.schema.json`

Result: **PASS**

### Deterministic Connector

Command shape:

```powershell
python .\chain_to_node_audit.py `
  --schema .\chain_schema.json `
  --nodes .\runs\axiom_adapter\nodes `
  --output-dir .\runs\axiom_deterministic
```

Sandbox result:

- Nodes read: `191`
- References read: `54`
- Connected: `166`
- Floating: `25`
- Chain gaps: `3` (`chain:6`, `chain:13`, `chain:15`)
- Proof-stack gaps: `4` (`proof:P1`, `proof:VAL1`, `proof:CROSS`, `proof:NC1`)
- Derivative-family gaps: `1` (`family:R`)

Result: **PASS — connector accepted all emitted nodes**

### Model-Backed Connector Dry Run

Command shape:

```powershell
python .\run_rosetta_connector.py `
  .\runs\axiom_adapter\receipts `
  --output-dir .\runs\axiom_api_smoke `
  --limit 1 `
  --dry-run
```

Sandbox result:

- Nodes loaded: `1` under `--limit 1`
- Mapping attempts: `3`
- Statuses: `dry_run: 3`

Result: **PASS — batch receipt format accepted**

No live API call was made in the sandbox.

## Review Notes

1. Existing `Primitive` / `floor_axiom` records are preserved natively but projected as `HYPOTHESIS` + `candidate_primitive` under the newer one-axiom discipline.
2. `unified_claim_type_status` is always `adapter_candidate`, so mechanical mapping cannot become a canon ruling.
3. `truth_unit.evidence` remains empty and `truth_unit.proof_link` remains null when the source atom does not carry those objects.
4. Candidate primitives receive `compression_bridge` stubs at `K0`; this creates review surface without demoting any source atom.
5. Native bridge records receive `bridge_evaluation` stubs at `B0`; this means declared/not tested, not rejected.
6. The deterministic connector's floating nodes and weak matches are review outputs, not failures.

## Open Items

- OI candidate: decide whether the standardized envelope should remain proposal-local under `_proposals/rosetta_stone_v0_1/` or graduate into `_schema/` after review.
- OI candidate: decide whether `Primitive` should remain mapped to `HYPOTHESIS + candidate_primitive`, or whether the unified schema should add a separate `PRIMITIVE` claim axis.
- OI candidate: run the model-backed connector live only after reviewing the deterministic output and dry-run receipts on David's machine.
