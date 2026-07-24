# 20_everyday_canon
> What is the simplest faithful statement?

**Branch:** public  ·  **Glyph:** `truth`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `rendered-view`

## Required fields
- `plainStatement`
- `confidence`
- `scope`
- `uncertainty`
- `boundaries`
- `whatWouldChangeIt`

## Allowed incoming edges
- `renders <- 02_claim_atoms.statementPlain`

## Allowed outgoing edges
- `feedsInto -> 21, 22, 23, 24, 26`

## Completion condition
Descent invariant reviewed and all four flags true.

## Propagation behavior
Inherits from the atom. Never originates falsification.

## NLP / classifier operations
Verify meaning, confidence, boundaries and failure condition survived translation. Flag any added premise.

## Validation rules
GENERATED, NOT HAND-AUTHORED. This is a canonical expression, not a loose summary. If it adds advice, that advice becomes a 24_application node.

## Public rendering
Default public view.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
