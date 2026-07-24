# 00_inbox_working
> I am thinking about this

**Branch:** capture  ·  **Glyph:** `draft`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `raw`

## Required fields
_none_

## Allowed incoming edges
_none_

## Allowed outgoing edges
- `feedsInto -> 01_middle_seed`

## Completion condition
Material can be expressed as an initial story or candidate claim.

## Propagation behavior
none - raw nodes are orphans until classified

## NLP / classifier operations
Language ID, dedupe by hash, rough domain guess against _DOMAIN.md cards. Never assert a domain from here.

## Validation rules
Originals preserved. Nothing here is canonical. No claimID may be issued.

## Public rendering
Never published.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
