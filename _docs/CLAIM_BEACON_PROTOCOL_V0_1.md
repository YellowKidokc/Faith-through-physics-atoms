# Claim Beacon Protocol v0.1

Claim Beacon Protocol lets claim atoms publish portable discovery metadata without replacing the station architecture or bloating each atom with every bridge proof. A beacon lives inside the JSON-LD claim atom under `claimBeacon`; bridge records, shared protocol records, proof records, manifests, proposals, and HTML are linked artifacts.

## Separation rule

```text
Claim atom = one precise assertion and its own test contract
Bridge atom = how two or more domains connect
Shared protocol records = rules every bridge must obey
Evidence / proof / test records = receipts for specific claims or bridges
```

Claim atoms carry their identity, statement, evidence needs, kill conditions, dependencies, and pointers to bridge/proof/policy records. They do not embed full bridge mappings, pivot ontologies, conflict matrices, commutativity tests, or benchmark reports.

## Beacon block in claim atoms

Every public claim atom SHOULD expose:

- `permanentID`: stable claim identity, normally `claimID`.
- `canonicalURL`: public URL for the atom or claim page.
- `version` and `provenance`: version, repository path, Git commit, modified date, authors, and source references when known.
- `priorVersions`: superseded versions or migration notes.
- `have`: support, derivations, data, or concise capabilities the claim itself offers.
- `need`: evidence, definitions, dependencies, or source records the claim requires.
- `breakIf`: explicit falsification or failure conditions.
- `claimType`, `domain`, `masterEquationVariables`, `tags`, and local `bridgeGrade` summary.
- `bridgeRefs`, `ontologyRefs`, and `policyRefs`: links to bridge atoms and shared protocol records.
- `proposalFeed`: public or local proposal stream for candidate relationships.

## Bridge record format

Bridge atoms use the existing `nodeType: bridge` schema and carry source domain, target domain, mapping table, grade, preserved relations, reverse mapping, boundary conditions, commutativity tests, conflict matrix reference, invariant monitors, proof links, and validation receipt. The reusable schema is `_protocol/claim-beacon/v0.1/bridge-record.schema.json`.

## Shared protocol records

- Pivot ontology: `_protocol/claim-beacon/v0.1/pivot-ontology.jsonld`.
- Conflict matrix: `_protocol/claim-beacon/v0.1/conflict-matrix.jsonld`.
- Bridge schema: `_protocol/claim-beacon/v0.1/bridge-record.schema.json`.
- Invariant monitor schema: `_protocol/claim-beacon/v0.1/invariant-monitor.schema.json`.

## Discovery manifest

`/.well-known/claim-beacons.json` lists public claim atom records, bridge records, and shared protocol records. Other repositories can fetch the manifest, then read JSON-LD claim beacons and linked bridge/protocol artifacts independently.

## Candidate relationship proposal

A proposal record uses `ClaimBeaconProposal` and includes:

- `sourceAtom` and `targetAtom`.
- `proposedEdgeType`.
- `matchReason`.
- `confidence`.
- `status`: `proposed`, `accepted`, `rejected`, or `superseded`.
- `validationReceipt`: method, validator, timestamp, Git commit, acceptance fields, bridge grade, and falsification-propagation flag.

Matchmakers write proposals only. They MUST NOT create accepted edges automatically.

## Validation and propagation rules

1. A human or verification station must accept and grade an edge before it becomes part of the atom graph.
2. Only accepted `structural_identity` or `structural_isomorphism` edges may propagate falsification.
3. `structural_analogy`, `metaphorical`, and `ungraded` edges never propagate falsification.
4. Git provenance, atom paths, and prior versions must be preserved in beacons and validation receipts.
5. Falsification propagation is computed from accepted edges; proposal feeds are advisory only.

## Local scripts

Use `_scripts/claim_beacon.py`:

```bash
python _scripts/claim_beacon.py manifest
python _scripts/claim_beacon.py propose
python _scripts/claim_beacon.py render
python _scripts/claim_beacon.py all
```

The v0.1 matchmaker compares `have`, `need`, and `breakIf` with deterministic keyword overlap and writes JSON Lines proposals to `_proposals/claim-relationships.jsonl`.
