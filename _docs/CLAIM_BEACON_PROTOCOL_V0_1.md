# Claim Beacon Protocol v0.1

Claim Beacon Protocol lets claim atoms publish a portable, machine-readable discovery block without replacing the existing station architecture. A beacon lives inside the JSON-LD claim atom under `claimBeacon`; generated manifests, proposals, and HTML are derived artifacts.

## Beacon block

Every public claim atom SHOULD expose:

- `permanentID`: stable claim identity, normally `claimID`.
- `canonicalURL`: public URL for the atom or claim page.
- `version` and `provenance`: version, repository path, Git commit, modified date, authors, and source references when known.
- `priorVersions`: superseded versions or migration notes.
- `have`: support, derivations, data, mappings, keywords, or tags the atom offers.
- `need`: evidence, definitions, dependencies, mappings, or source records it requires.
- `breakIf`: explicit falsification or failure conditions.
- `claimType`, `domain`, `masterEquationVariables`, `tags`, and `bridgeGrade`.
- `acceptedLinks`: human-accepted edges copied from the atom graph.
- `proposalFeed`: public or local proposal stream for candidate relationships.

## Discovery manifest

`/.well-known/claim-beacons.json` lists public atom records and their locations. Other repositories can fetch the manifest, then read each JSON-LD atom's `claimBeacon` block.

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
