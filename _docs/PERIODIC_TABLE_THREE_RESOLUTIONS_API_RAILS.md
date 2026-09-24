# Periodic Table at Three Resolutions — API Rails v1

## Purpose

This is the deterministic rail beneath the semantic/API lane.

```text
SOURCE DOCUMENT
    ↓
semantic/API interpreter
    ↓
ATLAS_API_RAILS_1.0 packet
    ↓
_scripts/atlas_api_rails.py
    ↓
beacons + combined Atlas record
    ↓
Local → Series → Global projections
```

The semantic/API lane proposes meaning. Python does not invent semantics. Python validates the packet, checks Nabla order/hash, preserves source spans, computes safe graph/count fields, writes beacons, and combines child records conservatively.

## Registry

Canonical view registry:

`_atlas/periodic-table-three-resolutions.json`

Stored resolutions:

1. `local`
2. `series`
3. `global`

Cross-Series `Φ` is a comparison operation between Series records, not a fourth stored resolution.

## Core rule

**Classify once → store canonical objects/typed edges → compute/project many ways.**

Do not call the API again merely to decide whether a canonical edge belongs on the Proof Map, Dependency Map, Blast Radius Map, Evolution Map, Dispute Map, or Reality-Mirror view. Those are deterministic projections when the primitive objects/edges already exist.

## Required API output

The API should return one JSON object matching:

`_schema/atlas_api_classification.schema.json`

Minimum blocks:

```text
protocol_version
source
identity
nabla
periodic15
atom_stack
audit
```

`atom_stack` contains the local canonical material:

```text
atoms
components
claims
evidence
tests
edges
arguments
dynamics
orientation
bridges
reality_mirror
open_items
```

## Emit one local record

```bash
python _scripts/atlas_api_rails.py emit candidate.json \
  --out _runtime/atlas-beacons
```

The rail writes a run directory containing:

```text
00_manifest.json
beacons/
  01_identity.json
  02_source.json
  03_nabla.json
  04_periodic15.json
  05_atom_stack.json
  06_dependency.json
  07_warrant.json
  08_dynamics.json
  09_orientation.json
  10_bridges.json
  11_reality_mirror.json
  12_audit.json
  13_computed.json
combined.atlas-record.json
```

Each beacon has a deterministic SHA-256 entry in `00_manifest.json`. The combined record contains the same canonical material plus computed fields and the beacon manifest.

## Combine into Series

```bash
python _scripts/atlas_api_rails.py combine \
  child-a.json child-b.json child-c.json \
  --resolution series \
  --semantic-code SER.MASTER_EQUATION \
  --label "Master Equation Series" \
  --out _runtime/atlas-beacons
```

The combiner:

- preserves all child atom-stack objects;
- unions native/admitted bridged domains;
- computes counts/runs/connectivity conservatively;
- emits a Series Periodic-15 projection;
- does **not** inherit child standing automatically;
- does **not** fabricate Marker 12;
- does **not** infer aggregate Nabla semantics;
- flags fields that require semantic/adjudicative aggregation.

## Combine into Global

Use the same command with:

```text
--resolution global
```

Global is still the same Periodic-15 grammar with richer aggregation. Global diagnostics such as Φ registry, anomaly register, topology, anchor coverage, and bottlenecks are projections over the same canonical graph.

## API ownership vs Python ownership

### Semantic/API lane may propose

- domain
- object type
- claim family
- function kind
- source meaning
- Nabla dimensions
- claim/evidence semantics
- dependency meaning
- Dynamics answers
- bridge candidates
- Reality-Mirror candidates

### Python rail owns

- required-field/schema checks
- source/hash preservation
- exact Nabla vector order
- Nabla semantic hash verification
- stable beacon filenames
- beacon hashes
- counts
- graph degree from typed edges
- child record aggregation
- deterministic projection membership
- run manifests

### Python rail must not

- promote semantic candidates to truth
- turn lexical absence into ontological absence
- invent an external anchor
- admit a bridge
- fabricate native/normalized grades
- infer aggregate standing without a declared rule
- silently collapse Candidate and Admitted graphs

## Candidate / Admitted

`audit.admission_state` is required:

```text
candidate
admitted
```

API-originated semantic extraction normally begins as `candidate`. The rail may compute against Candidate data for sandbox analysis, but canonical production propagation is governed by the applicable admission gate.

## Reproducibility lane

A second model/NLP system should receive the same source spans, registries, decision rules, and required output schema. It emits a separate `ATLAS_API_RAILS_1.0` packet. Compare the two packets only after both commit independently.

Agreement target is canonical objects + typed graph structure, not identical generated prose.

## Naming

Every object uses:

```text
Permanent UUID
Semantic Code
Human Label
```

The UUID is opaque. The semantic code is stable and registry-backed. The human label may change.

## Status

This rail is intentionally conservative. It is an integration spine, not a semantic engine. It is designed so DeepSeek, another LLM/NLP system, or a human gold lane can all produce the same packet shape and run down the same deterministic Python rails.
