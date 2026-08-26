# 26_audience
> How does the claim reach the person who needs it?

**Branch:** public  ·  **Glyph:** `logos`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `reach`

## Required fields
- `format`
- `sourceRef`
- `audienceLevel`

## Allowed incoming edges
- `descendsTo <- 20, 21, 22, 23, 25`

## Allowed outgoing edges
- `feedsInto -> 30_real_world_verdict`

## Completion condition
At least one artifact reaches audienceLevel=everyday.

## Propagation behavior
None.

## NLP / classifier operations
Check reading level matches declared audienceLevel.

## Validation rules
The published story is NOT the raw seed with better prose. It carries the corrections earned by the full process.

## Public rendering
Published.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
