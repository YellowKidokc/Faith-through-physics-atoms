# Claim Layer Truth Capsule Specification

Status: draft standard
Scope: all claim-bearing rails

This document defines the shared claim-layer architecture for the atom system. It generalizes the physics claim atom discipline across physics, mathematics, history, worldview, Scripture, theology, Theophysics, bridge, and policy/normative claims.

## Core Rule

A claim is an assertion of a proposition: something presented as true, false, possible, necessary, obligatory, meaningful, or otherwise answerable to a standard of evaluation.

Questions, commands, sources, datasets, evidence records, visualizations, and mind maps are not claims by themselves. They can contain, support, attack, or display claims.

## Four Objects Must Stay Separate

Every claim-bearing atom must separate:

- `claim`
- `evidence`
- `inference`
- `truth_status`

Do not collapse these into one confidence score.

Supported does not mean true.
Unsupported does not mean false.
Valid argument form does not mean true premises.
True conclusion does not mean the argument was valid.

## Claim Parsing Comes First

Before retrieving evidence, parse the claim.

Recommended parse object:

```json
{
  "proposition": "",
  "domain": "",
  "quantifier": "all | some | one | usually | probably",
  "modality": "actual | possible | necessary | impossible | obligatory | permitted | forbidden",
  "temporal_boundary": "",
  "geographic_or_context_boundary": "",
  "claim_species": []
}
```

The system must then define:

```json
{
  "truth_conditions": "",
  "disconfirmation_conditions": ""
}
```

These are set before evidence retrieval so the current evidence does not secretly define the standard.

## Multi-Axis Claim Classification

Do not use a single `claim_type` field as if one label can describe the whole claim.

Use multiple axes:

- domain
- quantifier
- modality
- scope boundary
- claim species
- inference type
- evidence type
- status lifecycle

Suggested `claim_species` values:

- `definitional`
- `logical`
- `mathematical`
- `singular_factual`
- `empirical_generalization`
- `statistical_probabilistic`
- `causal`
- `historical`
- `existential`
- `universal`
- `modal`
- `interpretive`
- `normative_value`
- `policy_prescriptive`
- `metaphysical_ontological`
- `theological`
- `bridge_correspondence`

A single claim can carry multiple species.

Example:

```json
{
  "claim_species": [
    "empirical_generalization",
    "causal",
    "statistical_probabilistic"
  ]
}
```

## Evaluation Depends On Claim Class

Different claim classes require different evaluation standards.

| Claim Species | Primary Evaluation Standard |
|---|---|
| `definitional` | meaning, usage, stipulated definition, conceptual coherence |
| `logical` | formal derivation |
| `mathematical` | mathematical proof |
| `singular_factual` | observation, record, testimony, artifact |
| `empirical_generalization` | repeated observation or experiment |
| `statistical_probabilistic` | statistical inference, uncertainty, denominator, model assumptions |
| `causal` | controls, interventions, causal models, counterfactual analysis |
| `historical` | documents, artifacts, testimony, independent corroboration |
| `existential` | one authenticated instance within the relevant domain |
| `universal` | derivation or broad support; defeated by one valid counterexample |
| `modal` | logical, metaphysical, or domain-specific modal analysis |
| `interpretive` | text, context, authorial intent, tradition, comparative reading |
| `normative_value` | facts plus explicit value or moral standard |
| `policy_prescriptive` | facts, predicted consequences, feasibility, explicit objective |
| `metaphysical_ontological` | coherence, explanatory power, entailments, alternatives, defeaters |
| `theological` | Scripture, doctrine, tradition, reason, theological coherence |
| `bridge_correspondence` | explicit mapping, preserved properties, boundary conditions, negative controls |

## Ontic And Epistemic Status

Every claim-bearing atom should carry two statuses:

```json
{
  "truth_status": {
    "ontic": "true | false | unknown",
    "epistemic": ""
  }
}
```

`ontic` asks whether the claim is actually true.

`epistemic` asks what the available evidence justifies.

Recommended epistemic values:

- `unsupported`
- `some_support`
- `supported`
- `strongly_supported`
- `demonstrated_or_established`
- `evidence_against`
- `refuted`
- `formally_derived`
- `experimentally_established`
- `measurement_reported`
- `observationally_supported`
- `model_dependent`
- `contested`
- `insufficient`
- `no_evidence`

Use domain-specific values when needed, but do not erase the ontic/epistemic distinction.

## Inference Object

Evidence does not speak without an inference relation.

```json
{
  "inference": {
    "inference_type": "deductive | inductive | abductive | analogical | statistical | causal | transcendental | interpretive | theological",
    "inference_description": "",
    "strength": "demonstrative | very_strong | strong | moderate | weak | speculative",
    "known_gaps": ""
  }
}
```

## Evidence Object

Evidence records must say what the evidence actually shows, not what the project hopes it implies.

```json
{
  "evidence": {
    "evidence_status": "",
    "evidence_summary": "",
    "supporting_evidence": [],
    "contrary_evidence": [],
    "key_sources": [],
    "replication_or_corroboration_status": null
  }
}
```

Evidence can support the claim, weaken the claim, support only a premise, or support only a model that contains the claim. These are not the same.

## Structural Asymmetries

Universal claims:

- Many confirmations can support a strict universal.
- One genuine counterexample can defeat it.

Existential claims:

- One authenticated instance can establish the claim.
- Failure to find an instance does not refute it unless the search domain is bounded and sufficiently exhaustive.

Model-dependent claims:

- Evidence for the model is not automatically evidence for the claim independently.
- If the model changes, the claim must be re-evaluated.

Interpretive claims:

- Evidence for a text, equation, or formalism is not automatically evidence for one interpretation of it.

Normative claims:

- A normative conclusion requires a normative premise, standard, or bridge.
- Descriptive facts alone do not silently produce an ought.

Bridge claims:

- A bridge is its own claim.
- Structural analogy is not evidence by itself.
- Propagation requires a separately validated bridge.

## Required Default Flags

All claim-bearing atoms default to:

```json
{
  "propagates_evidence": false,
  "propagates_falsification": false
}
```

No atom upgrades or downgrades another atom's status unless a validated bridge explicitly permits the transfer and names the scope of that transfer.

## Minimal Claim Atom Shape

```json
{
  "atom_type": "claim",
  "claim_id": "",
  "label": "",
  "claim_species": [],
  "claim": {
    "proposition": "",
    "domain": "",
    "quantifier": "",
    "modality": "",
    "temporal_boundary": "",
    "geographic_or_context_boundary": ""
  },
  "truth_conditions": "",
  "disconfirmation_conditions": "",
  "evidence": {
    "evidence_status": "insufficient",
    "evidence_summary": "",
    "supporting_evidence": [],
    "contrary_evidence": [],
    "key_sources": []
  },
  "inference": {
    "inference_type": "",
    "inference_description": "",
    "strength": "",
    "known_gaps": ""
  },
  "truth_status": {
    "ontic": "unknown",
    "epistemic": "insufficient"
  },
  "negative_guards": [],
  "dependencies": [],
  "unresolved_questions": [],
  "propagates_evidence": false,
  "propagates_falsification": false,
  "status": "extracted_not_ratified"
}
```

## Relationship To Physics Claim Schema

The physics claim atom schema is a domain-specific specialization of this general claim layer.

Physics adds:

- physics-specific claim types
- measurement provenance
- replication status
- consensus status
- historical status
- physics proof labels
- source anchors for papers, textbooks, datasets, reviews, and measurements

The general claim layer remains the shared backbone.

## Relationship To Theophysics

This specification does not prove Theophysics claims.

It gives Theophysics a cleaner claim engine:

1. parse the claim
2. declare truth and disconfirmation conditions
3. collect evidence
4. evaluate inference
5. separate ontic and epistemic status
6. connect across rails only through bridge atoms

That protects the project from two opposite errors:

- dismissing a true claim just because it is currently under-evidenced
- promoting an attractive claim just because its evidence feels convergent

## Import Rule For Existing Drafts

Existing definition scaffolds should not be treated as canonical claim atoms.

They should be promoted by this path:

```text
definition scaffold
  -> parsed claim candidate
  -> truth/disconfirmation conditions
  -> evidence record
  -> inference record
  -> ontic/epistemic status
  -> bridge record if cross-rail
  -> canon review
```

No stage silently promotes the next stage.
