# 13_hypothesis
> What should happen if the technical claim is true?

**Branch:** technical  ·  **Glyph:** `prediction`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `prediction`

## Required fields
- `prediction`
- `predictedMagnitude`
- `decisionThreshold`
- `method`
- `baseline`
- `alternatives`
- `confidenceBeforeTesting`
- `resultStatus`

## Allowed incoming edges
- `dependsOn <- 10_technical_canon`

## Allowed outgoing edges
- `feedsInto -> 30_real_world_verdict`

## Completion condition
Prospective prediction registered BEFORE the result is known.

## Propagation behavior
Failed prediction flags dependents for review; does not auto-falsify the root claim.

## NLP / classifier operations
Detect retrospective predictions. Flag anything registered after the outcome was available.

## Validation rules
Technical branch only. The public branch links to these nodes rather than duplicating them.

## Public rendering
Prediction card with status.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
