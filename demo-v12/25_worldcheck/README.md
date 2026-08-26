# 25_worldcheck
> Does the plain claim survive contact with people and reality?

**Branch:** public  ·  **Glyph:** `seven-question`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `check`

## Required fields
- `comprehensionResult`
- `confidencePreserved`
- `naturalObjections`
- `applicationOutcome`
- `contradictingPublicFacts`

## Allowed incoming edges
- `tests <- 20_everyday_canon, 24_application`

## Allowed outgoing edges
- `feedsInto -> 30_real_world_verdict, 26_audience`

## Completion condition
Tested with real people outside the project.

## Propagation behavior
Translation failure triggers a rewrite, not a falsification of the claim.

## NLP / classifier operations
Run 7Q. Compare reader-reported meaning against statementPlain.

## Validation rules
This is the pressure test of the PUBLIC branch, not the final scientific verdict.

## Public rendering
Optional; results inform the audience layer.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
