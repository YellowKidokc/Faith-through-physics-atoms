# 14_evidence
> What bears directly on the claim?

**Branch:** technical  ·  **Glyph:** `evidence`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `evidence`

## Required fields
- `sourceType`
- `sourceRef`
- `citationStatus`
- `relevantClaim`
- `conclusionSeparate`

## Allowed incoming edges
- `supports/challenges -> 10_technical_canon or 13_hypothesis`

## Allowed outgoing edges
- `feedsInto -> 17_doctoral_paper`

## Completion condition
Negative evidence, null results and replication status recorded alongside favorable evidence.

## Propagation behavior
Empirical failure flags dependents for review. Local unless the claim is empirical at root.

## NLP / classifier operations
Verify citations resolve. Separate source content from source conclusions.

## Validation rules
LLM and wiki summaries are NOT decisive evidence. They are baseline maps and belong in 22_lived_synthesis unless they point to inspectable sources.

## Public rendering
Evidence ledger, including what cuts against.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
