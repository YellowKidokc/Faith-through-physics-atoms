# 01_middle_seed
> Here is what we found and why it might matter

**Branch:** capture  ·  **Glyph:** `binder`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `seed`

## Required fields
- `title`
- `whatWeNoticed`
- `candidateClaim`
- `whyItMatters`
- `whatSupportsIt`
- `whatIsUncertain`
- `nextDirection`

## Allowed incoming edges
- `feedsInto <- 00_inbox_working`

## Allowed outgoing edges
- `feedsInto -> 02_claim_atoms`

## Completion condition
At least one material claim has been extracted into 02_claim_atoms.

## Propagation behavior
none - a seed carries no falsification weight

## NLP / classifier operations
Extract candidate claims. Propose domain + tags + glyph signature. Flag sentences that assert without support.

## Validation rules
Written for an informed adult. Must state what is uncertain. May not present the formal case as complete.

## Public rendering
Optional preview. Mark clearly as unreviewed.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
