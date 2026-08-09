# Meta Claim Extractor

The meta claim extractor reads a canon assembly file, splits it by `W#.#` works,
runs the configured API, and writes a full claim/defense-grid review under:

`_runtime/meta_claim_extractor/<run-id>/`

It does not edit source files and does not promote claims.

The extractor follows the claim/evidence lane contract in
`_docs/CLAIM_EVIDENCE_LANE_FRAMEWORK.md`.

## Classification + Glyph API Rail

Every extracted claim row now carries a normalized `classification_bundle`.
This is the API rail that keeps the pill, ledger, graph, and HTML views aligned.

```json
{
  "classification_bundle": {
    "framework_lane": "physics",
    "physics_claim_type": "theological_interpretation",
    "defense_class": "RHETORIC",
    "claim_level": "theological",
    "evidence_lane": "scripture_theology",
    "recommended_action": "demote",
    "glyphs": ["physics", "theology", "render-html", "boundary"]
  },
  "glyph_paths": [
    "theophysics_glyphs/svg/physics.svg",
    "theophysics_glyphs/svg/theology.svg"
  ]
}
```

These glyphs are semantic tags, not proof labels. They tell the renderer what
kind of claim it is, where it belongs, what evidence lane it needs, and what
warning/action posture it carries.

The review report also includes framework lane, evidence lane, and glyph counts
so each API run can be audited at a glance.

## Preview the selected works

```powershell
powershell -ExecutionPolicy Bypass -File _scripts\RUN_META_CLAIM_EXTRACTOR.ps1 -Plan
```

## Run one work first

```powershell
powershell -ExecutionPolicy Bypass -File _scripts\RUN_META_CLAIM_EXTRACTOR.ps1 -Work W4.1
```

## Run one turn

```powershell
powershell -ExecutionPolicy Bypass -File _scripts\RUN_META_CLAIM_EXTRACTOR.ps1 -Turn 4 -KeepGoing
```

## Run the raw half of the assembly

```powershell
python _scripts\meta_claim_extractor.py --input "C:\theophysics\OPUS\CANON_ASSEMBLY\CANON_ASSEMBLED.md" --start-at W4.1 --keep-going
```

## Output files

- `meta_claims.json` - full parsed results.
- `meta_claims.jsonl` - one claim per line, including classification bundle and glyph paths.
- `run_log.jsonl` - every work start, completion, or failure.
- `META_CLAIM_REVIEW.md` - human-readable review sheet.
- `raw_responses/` - exact API responses, for auditability.
