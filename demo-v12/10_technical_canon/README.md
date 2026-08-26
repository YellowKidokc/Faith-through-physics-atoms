# 10_technical_canon
> What is the most precise defensible statement?

**Branch:** technical  ·  **Glyph:** `canonical`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `rendered-view`

## Required fields
- `definitions`
- `variables`
- `units`
- `assumptions`
- `scope`
- `uncertainty`
- `dependencies`
- `revisionCondition`

## Allowed incoming edges
- `renders <- 02_claim_atoms.statementTechnical`

## Allowed outgoing edges
- `feedsInto -> 11, 12, 13, 17`

## Completion condition
Statement locked and versioned in the ledger.

## Propagation behavior
Inherits from the atom. Never originates falsification.

## NLP / classifier operations
Check every variable is defined and every assumption is stated. Flag undefined symbols.

## Validation rules
GENERATED, NOT HAND-AUTHORED. Regenerating must produce an identical file. Canonical means current-approved, not unquestionable.

## Public rendering
Technical layer of the public page.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
