# 24_application
> What might someone do differently?

**Branch:** public  ·  **Glyph:** `sanctification`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `application`

## Required fields
- `sourceClaim`
- `intendedPerson`
- `desiredOutcome`
- `addedPremises`
- `contextAssumptions`
- `risks`
- `alternatives`
- `stopCondition`
- `professionalBoundaries`

## Allowed incoming edges
- `dependsOn <- 20_everyday_canon`

## Allowed outgoing edges
- `feedsInto -> 25_worldcheck, 30_real_world_verdict`

## Completion condition
Added premises listed explicitly so they can be attacked independently.

## Propagation behavior
APPLICATION FAILURE ATTACKS THE APPLICATION MAPPING FIRST, never automatically the source claim.

## NLP / classifier operations
Extract every premise not present in the source claim. An unlisted added premise is a defect.

## Validation rules
Application is a separate operation from translation because it ADDS PREMISES. A valid claim must never smuggle in unsupported advice.

## Public rendering
Clearly marked as application, with premises visible.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
