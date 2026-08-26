# 02_claim_atoms
> What exactly is being claimed?

**Branch:** capture  ·  **Glyph:** `claim`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `claim`
- `bridge`
- `application`

## Required fields
- `claimID`
- `nodeType`
- `statementTechnical`
- `statementPlain`
- `claimClass`
- `domainType`
- `status`
- `evidenceType`
- `falsificationCondition`
- `glyphs`
- `tags`
- `axiomRoot`

## Allowed incoming edges
- `feedsInto <- 01_middle_seed`

## Allowed outgoing edges
- `dependsOn`
- `bridgesTo`
- `descendsTo`
- `challenges`
- `expands`

## Completion condition
Atom validates clean and carries both canonical expressions.

## Propagation behavior
SOURCE OF TRUTH. Falsification originates and propagates from here per bridgeGrade.

## NLP / classifier operations
Emit mathFormNormal. Propose candidate bridges (ungraded, propagates=false). Never assign a grade.

## Validation rules
python _scripts/validate_atoms.py must return 0 errors. Only claim nodes carry claimID.

## Public rendering
The atom renders BOTH canon folders. Neither is hand-authored.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
