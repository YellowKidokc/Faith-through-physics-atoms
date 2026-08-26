# 12_technical_synthesis
> What formal structures connect across domains?

**Branch:** technical  ·  **Glyph:** `isomorphism`

<!-- GENERATED FILE - do not hand-edit.
     Source: _vocab/stage_contracts*.json
     Regenerate: python _scripts/write_stage_contracts.py -->

## Permitted node types
- `bridge`

## Required fields
- `sourceDomain`
- `targetDomain`
- `bridgeGrade`
- `mathFormNormal`
- `substitutionMap`
- `preservedOperations`
- `inverseMapping`
- `boundaryConditions`

## Allowed incoming edges
- `dependsOn <- 10_technical_canon`

## Allowed outgoing edges
- `bridgesTo -> other domains`
- `feedsInto -> papers/`

## Completion condition
Mapping stated, bidirectional test run, grade assigned by a human.

## Propagation behavior
identity/isomorphism PROPAGATE. analogy/metaphorical DO NOT. ungraded never propagates.

## NLP / classifier operations
Match mathFormNormal across the corpus. Propose candidates as ungraded. GRADING IS HUMAN-ONLY.

## Validation rules
Analogy, correspondence, isomorphism and identity remain distinct. No grade above analogy without equations, variable correspondence, boundaries and a novel prediction.

## Public rendering
Cross-domain section with the grade shown.

---

## Folder state
The icon on this folder reflects its state automatically:
`gray` empty · `amber` working · `green` done (`_STATUS.done`) · `red` failed (`_STATUS.failed`)

Run `python _scripts/set_folder_icons.py` after changing content.
