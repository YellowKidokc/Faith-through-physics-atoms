# 15_falsification
> How can this claim lose?

**Branch:** technical  ·  **Glyph:** `kill-condition`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `kill`

## Required fields
- `killCondition`
- `attemptDescription`
- `outcome`
- `targetClaim`
- `failureType`
- `propagationScope`

## Allowed incoming edges
- `challenges -> 10_technical_canon`

## Allowed outgoing edges
- `feedsInto -> 30_real_world_verdict`

## Completion condition
Kill condition typed to the claim class and at least one attempt recorded.

## Propagation behavior
Per failureType: root_claim=global, mapping_invalid=bridge peers, boundary_exceeded=dependents, measurement/interpretation=local, application_failure=application node only.

## NLP / classifier operations
Check the kill condition is typed correctly for the claimClass and is actually reachable.

## Validation rules
FAILED TESTS REMAIN PERMANENTLY VISIBLE. Deleting a failed attempt is a governance breach.

## Public rendering
Kill conditions shown with the claim, not hidden.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
