# Physics Claim Schema Conformance

Status: conformance check

Question: does `general_theory_atoms.v0.1.json` already follow the full Physics Claim Atom schema?

Answer: partially in principle, not yet in full structure.

## Current Draft Shape

The current proposal file contains 30 draft atoms:

- 10 `physical_definition` atoms
- 10 `spiritual_definition` atoms
- 10 `bridge_candidate` atoms

These are vocabulary and mapping scaffold atoms. They are not yet full `physics_claim` atoms.

## What It Already Follows

The draft follows the schema's governing discipline in these ways:

- it separates physical definitions from spiritual definitions
- it puts cross-rail claims in bridge atoms
- it marks the pack as draft proposal, not canon
- it includes misuse guards
- it includes kill conditions
- it avoids direct physical proof of Theophysics
- it treats mind-map rendering as visualization, not evidence
- it avoids using `isomorphism` without the stronger proof gates

## What It Does Not Yet Follow

The physical definition atoms do not yet include the full required `physics_claim` fields:

- `claim_id`
- `claim_types`
- `claim.proposition`
- `claim.quantifier`
- `claim.modality`
- `claim.temporal_boundary`
- `claim.domain`
- `claim.claim_species`
- `truth_conditions`
- `disconfirmation_conditions`
- `evidence`
- `consensus_status`
- `historical_status`
- `inference`
- `truth_status`
- `measurement_provenance` when applicable
- `proof_label`
- `source_anchors`
- `negative_guards`
- `propagates_evidence`
- `propagates_falsification`
- lifecycle `status` using the master status vocabulary

## Correct Interpretation

The current file is not wrong. It is simply one layer earlier than the full physics claim atom schema.

Use it as:

```text
definition scaffold -> claim-layer parse -> physics claim atom candidates -> validation records -> bridge candidates -> Theophysics atoms
```

Do not use it as:

```text
definition scaffold -> canonical physics claims
```

## Required Promotion Rule

Before any `physical_definition` atom becomes a canonical `physics_claim`, it must be expanded into the full schema shape and must explicitly preserve the four-object separation:

- claim
- evidence
- inference
- truth status

It must also default to:

```json
{
  "propagates_evidence": false,
  "propagates_falsification": false,
  "status": "extracted_not_ratified"
}
```

unless an explicit validation record says otherwise.

## Recommended Next Step

Create a converter/validator that reads `general_theory_atoms.v0.1.json` and emits draft `physics_claim` candidates for the physical side only.

The converter should use `_docs/CLAIM_LAYER_TRUTH_CAPSULE_SPEC.md` as the shared claim backbone and then apply the domain-specific physics claim schema on top of it.

The converter should not invent evidence. If sources are missing, it should write:

```json
{
  "evidence_status": "insufficient",
  "evidence_summary": "Definition scaffold created; source validation not yet attached.",
  "key_sources": []
}
```

That way the atom exists, but no evidence or truth status is silently upgraded.
