# 23_public_evidence
> What receipts can an ordinary person inspect?

**Branch:** public  ·  **Glyph:** `witness`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `evidence`

## Required fields
- `accessibleWitness`
- `sourceTrail`
- `linkToTechnicalEvidence`

## Allowed incoming edges
- `descendsTo <- 14_evidence`

## Allowed outgoing edges
- `feedsInto -> 26_audience`

## Completion condition
Every public receipt links upward to the complete technical evidence.

## Propagation behavior
Inherits. Never originates.

## NLP / classifier operations
Verify each receipt is actually inspectable by a non-specialist.

## Validation rules
Evidence is simplified in PRESENTATION, never strengthened in CONCLUSION. Public case is not a replacement for the technical ledger.

## Public rendering
Receipts, each with a link up.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
