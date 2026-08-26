# 30_real_world_verdict
> What actually happened?

**Branch:** verdict  ·  **Glyph:** `justice`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `result`

## Required fields
- `formal_verdict`
- `empirical_verdict`
- `bridge_verdict`
- `translation_verdict`
- `application_verdict`

## Allowed incoming edges
- `resolves <- 13_hypothesis, 15_falsification, 24_application, 25_worldcheck`

## Allowed outgoing edges
- `feedsInto -> 31_revision_return`

## Completion condition
All five verdict types recorded or explicitly marked pending.

## Propagation behavior
Typed per verdict. ONE SUCCESS CANNOT SILENTLY STAND IN FOR EVERY VERDICT TYPE.

## NLP / classifier operations
Detect a single verdict being reported as overall success.

## Validation rules
Shared by both branches. Neither branch may declare its own success.

## Public rendering
Verdict card, all five types shown.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
