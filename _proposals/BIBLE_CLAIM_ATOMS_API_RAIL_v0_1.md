# Bible Claim Atoms API Rail v0.1

Status: proposal
Date: 2026-08-09
Owner: David Lowe / Faith Through Physics
Purpose: define an API extraction rail for Scripture-derived claim atoms without calling Bible statements formal axioms.

## Core Decision

Bible extraction should produce `bible_claim_atom` records.

Do not call these axioms by default. A Bible Claim Atom is a structured Scriptural witness statement: a claim, command, event, promise, warning, or theological proposition extracted from a bounded passage with reference, context, genre, and interpretive warnings.

Formal promotion remains separate. Extraction does not ratify doctrine, prove Theophysics, or canonize a mapping.

## Why This Exists

The atoms system needs a rail that can:

- ingest a Bible passage,
- split it into one-claim-per-atom records,
- preserve reference and translation provenance,
- classify the claim type,
- map substantial claims to Theophysics domains only when warranted,
- mark interpretive risk,
- export rows for Excel / worldcheck / rails,
- keep extracted claims reviewable before promotion.

## API Shape

### Request

```json
{
  "task": "extract_bible_claim_atoms",
  "translation": "KJV",
  "passage_reference": "John 1:1-5",
  "source_text": "In the beginning was the Word...",
  "extraction_profile": "strict",
  "target_domains": ["Logos", "God", "Christology", "Creation", "Information"],
  "theophysics_mapping_allowed": true,
  "output_format": "json"
}
```

### Response

```json
{
  "rail": "bible_claim_atoms_api_rail_v0.1",
  "translation": "KJV",
  "passage_reference": "John 1:1-5",
  "atoms": [
    {
      "atom_type": "bible_claim_atom",
      "source_claim_id": "BIB-JOH-001-001-A",
      "reference": "John 1:1",
      "translation": "KJV",
      "source_text": "In the beginning was the Word, and the Word was with God, and the Word was God.",
      "claim_text": "The Word existed in the beginning, was with God, and was God.",
      "claim_type": "theological_proposition",
      "speaker": "narrator",
      "genre": "gospel_prologue",
      "context": "Opening of John's Gospel; introduces the Logos before creation.",
      "direct_or_inferred": "direct",
      "doctrinal_domains": ["Logos", "God", "Christology", "Trinity"],
      "doctrinal_role": "constitutive",
      "theophysics_mapping": {
        "variable_or_domain": "Logos",
        "relation": "grounds_information_order",
        "mapping_confidence": "high",
        "mapping_status": "proposed"
      },
      "supports": ["Logos as divine", "Logos as pre-creation ground"],
      "constrains": ["Logos cannot be merely created information"],
      "interpretive_warnings": [
        "Translation-sensitive term: Logos/Word",
        "Requires Johannine prologue context"
      ],
      "source_anchor": {
        "book": "John",
        "chapter": 1,
        "verse_start": 1,
        "verse_end": 1
      },
      "status": "extracted_not_ratified",
      "confidence": "high",
      "notes": "Scriptural witness statement, not a formal mathematical axiom."
    }
  ],
  "validation": {
    "one_claim_per_atom": true,
    "unmapped_claims_allowed": true,
    "promotion_performed": false
  }
}
```

## Controlled Vocabulary

### `claim_type`

- `divine_declaration`
- `moral_command`
- `theological_proposition`
- `historical_claim`
- `prophetic_claim`
- `wisdom_principle`
- `anthropological_claim`
- `cosmological_claim`
- `soteriological_claim`
- `covenant_statement`
- `warning_or_judgment`
- `promise`
- `narrative_event`

### `direct_or_inferred`

- `direct`
- `strong_inference`
- `weak_inference`
- `typological`
- `symbolic`
- `poetic`
- `parabolic`
- `disputed`

### `doctrinal_role`

- `constitutive`
- `supporting`
- `illustrative`
- `boundary`
- `negative_control`
- `contextual`

### `status`

- `extracted_not_ratified`
- `reviewed`
- `ratified`
- `rejected`
- `needs_review`

## Extraction Prompt

Use this as the model instruction for the API call:

```text
Extract Bible Claim Atoms from the supplied passage.

Do not call them axioms. Each atom must represent exactly one claim, command, event, promise, warning, or theological proposition.

For each atom return JSON with:
- atom_type = bible_claim_atom
- source_claim_id
- reference
- translation
- source_text
- claim_text
- claim_type
- speaker
- genre
- context
- direct_or_inferred
- doctrinal_domains
- doctrinal_role
- theophysics_mapping
- supports
- constrains
- interpretive_warnings
- source_anchor
- status
- confidence
- notes

Rules:
1. Do not extract isolated phrases without context.
2. Do not force Theophysics mappings.
3. Mark poetic, parabolic, symbolic, typological, or disputed readings clearly.
4. Keep historical narrative distinct from doctrinal proposition.
5. One atom equals one claim.
6. If a verse contains multiple claims, split it into multiple atoms.
7. If the claim depends on interpretation, set status to needs_review.
8. Extraction never promotes the claim to canon.
9. Theophysics mappings are proposed bridges, not proof.
```

## Lane 4 Compatibility

Bible Claim Atoms can be wrapped into the current Lane 4 schema without changing the production schema immediately.

Recommended wrapper fields:

```json
{
  "atom_id": "tp:lane4/scripture/bib-joh-001-001-a",
  "source_claim_id": "BIB-JOH-001-001-A",
  "title": "John 1:1 - The Word was with God and was God",
  "claim": "The Word existed in the beginning, was with God, and was God.",
  "domain": "scripture",
  "lane": "BibleClaimAtoms",
  "claim_class": "bible_claim_atom",
  "mode_classification": "scriptural_witness_statement",
  "assumptions": [
    "The supplied translation text is the extraction source.",
    "The atom records a bounded scriptural witness, not a formal axiom."
  ],
  "definitions": [
    "claim_type: theological_proposition",
    "direct_or_inferred: direct",
    "doctrinal_role: constitutive"
  ],
  "equations": [],
  "bridges": [
    {
      "target": "Logos",
      "relation": "grounds_information_order",
      "grade": "proposed_scriptural_bridge",
      "propagates": false
    }
  ],
  "dependencies": [
    "John 1:1",
    "Johannine prologue context"
  ],
  "negative_guards": [
    "Do not treat extraction as canon ratification.",
    "Do not treat a Theophysics mapping as formal proof.",
    "Do not use isolated phrase extraction without context."
  ],
  "kill_conditions": [
    "Wrong reference or source text.",
    "Claim combines multiple distinct claims that should be split.",
    "Mapping depends on disputed interpretation but is marked direct."
  ],
  "proof_label": "NARRATIVE_ANCHOR",
  "current_status": "extracted_not_ratified",
  "rerun_status": "not_applicable",
  "source_artifacts": [
    "Bible translation source text for John 1:1"
  ],
  "classification_bundle": {
    "atom_type": "bible_claim_atom",
    "translation": "KJV",
    "reference": "John 1:1",
    "claim_type": "theological_proposition",
    "direct_or_inferred": "direct",
    "doctrinal_domains": ["Logos", "God", "Christology", "Trinity"],
    "interpretive_warnings": [
      "Translation-sensitive term: Logos/Word"
    ]
  },
  "ledger": []
}
```

## Validation Rails

Reject or route to `needs_review` if:

- `source_text` is missing.
- `reference` is missing or malformed.
- `claim_text` contains multiple separable claims.
- `claim_type` is not in the controlled vocabulary.
- `direct_or_inferred` is `direct` but the atom is actually typological, symbolic, poetic, or inferred.
- `theophysics_mapping` is present but no substantial relationship is stated.
- `status` is `ratified` at extraction time.
- `proof_label` claims formal proof.

Allow:

- atoms with no Theophysics mapping,
- multiple atoms from one verse,
- one atom spanning multiple verses when the claim is syntactically or contextually inseparable,
- disputed atoms if marked `needs_review`.

## Excel / Sheet Columns

Minimum export columns:

```text
source_claim_id
reference
translation
claim_text
claim_type
speaker
genre
context
direct_or_inferred
doctrinal_domains
doctrinal_role
theophysics_variable_or_domain
relation_to_theophysics
mapping_confidence
status
confidence
interpretive_warnings
source_text
notes
```

## Promotion Rule

Extraction is not promotion.

The API may create `extracted_not_ratified` atoms only. Promotion to `reviewed` or `ratified` requires a separate review event, source check, and canon governance step.

This follows the Lane 4 rule: receipts and execution never silently promote an atom.

## Next Implementation Step

1. Add a dedicated JSON Schema extension or profile for `classification_bundle.atom_type = bible_claim_atom`.
2. Add an extraction script that calls the API and writes candidate JSON files to `scripture/00_inbox_working/bible-claim-atoms/`.
3. Validate candidate files against this proposal before ingesting into Lane 4.
4. Export a spreadsheet projection for review.
5. Only after review, ingest selected atoms with `lane4_ledger.py ingest`.
