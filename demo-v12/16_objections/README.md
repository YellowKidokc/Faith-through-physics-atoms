# 16_objections
> What is the strongest opposing case?

**Branch:** technical  ·  **Glyph:** `doubt`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `objection`

## Required fields
- `objection`
- `objectionSource`
- `strength`
- `response`
- `status`
- `targetClaim`

## Allowed incoming edges
- `challenges -> claim or paper`

## Allowed outgoing edges
- `feedsInto -> papers/`

## Completion condition
At least one serious-strength objection, steelmanned and attributed.

## Propagation behavior
Unresolved objections do not falsify but must remain visible.

## NLP / classifier operations
Score objection strength. Flag strawmen. A weak objection filed here is a defect.

## Validation rules
Objections develop throughout the branch, not after the paper is written. Unresolved points stay adjacent to responses.

## Public rendering
War-room section with unresolved items marked.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
