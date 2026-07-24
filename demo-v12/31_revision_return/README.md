# 31_revision_return
> What changes now?

**Branch:** verdict  ·  **Glyph:** `repentance`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `revision`

## Required fields
- `changeType`
- `affectedClaims`
- `newInboxEntries`

## Allowed incoming edges
- `dependsOn <- 30_real_world_verdict`

## Allowed outgoing edges
- `feedsInto -> 02_claim_atoms (update), 00_inbox_working (new)`

## Completion condition
Every verdict has produced either a canon update or a new inbox entry.

## Propagation behavior
Closes the cycle. Applies the verdict to the atom.

## NLP / classifier operations
Verify no verdict was recorded without a corresponding revision or explicit no-change note.

## Validation rules
Failed mappings may leave the source claim intact. Harmful applications are STOPPED. Unresolved anomalies become new inbox material.

## Public rendering
Changelog.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
