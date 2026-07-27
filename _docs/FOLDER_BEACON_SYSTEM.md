# Folder Beacon System

Folder Beacon v2 makes each `.fisnote` a cheap, explicit routing record. Its
machine-readable YAML front matter answers what a folder contains, provides,
needs, seeks, and permits. Markdown after the closing delimiter remains for
human notes.

## Minimum beacon

```yaml
---
fis_schema: "folder-beacon.v2"
folder_id: "FLD-20260726-8259cf57"
folder: "GitHub\\faiththruphysics-site-data\\be-glad-youre-a-loser"
name: "be-glad-youre-a-loser"
short_name: "BGL"
folder_class: "page_series"
status: "active"
contains: ["article_html", "series_index_html"]
provides: ["html_pages", "series_navigation"]
needs: ["article_markdown", "audio_assets"]
looking_for: ["audio matching BGL"]
search_tokens: ["bgl", "be glad", "loser"]
allowed_actions: ["index", "beaker_scan", "link_assets"]
forbidden_actions: ["delete", "rename_public_html_without_approval"]
batch_tags: ["site-data", "page-series", "bgl"]
---
```

The compact parser is deliberately dependency-free and accepts top-level
scalar fields and scalar lists (inline JSON-style or block-style). It rejects
nested mappings instead of guessing their meaning.

## Fast scan

```bash
python _scripts/fis_folder_beacon_scan.py ROOT [ROOT ...] \
  --output folder_beacon_index.json
```

The scanner finds `.fisnote` files, reads at most 64 KiB from each by default,
validates every required v2 field, and writes `folder-beacon-index.v1`. Invalid
or oversized beacons appear in the output's `errors` collection and produce a
nonzero exit code. Change the ceiling with `--max-bytes`.

## Safe batch patches

Create a JSONL file with one operation per line:

```jsonl
{"op":"add_unique","selector":{"batch_tags":["site-data"]},"field":"allowed_actions","value":"beaker_scan"}
{"op":"add_unique","selector":{"folder_class":"asset_audio"},"field":"provides","value":"audio_assets"}
{"op":"set","selector":{"folder":"GitHub\\faiththruphysics-site-data\\be-glad-youre-a-loser"},"field":"short_name","value":"BGL"}
```

Preview and apply it with:

```bash
python _scripts/fis_folder_beacon_patch.py changes.jsonl ROOT --dry-run
python _scripts/fis_folder_beacon_patch.py changes.jsonl ROOT
```

Supported operations are `set`, `add_unique`, `remove_value`,
`replace_value` (using `old_value` and `value`), `append_tag`, and
`mark_needs_review`. A list-valued selector requires all listed values.

The editor changes YAML only, writes each file through an atomic temporary
file, never moves or deletes folders, and emits a changed/skipped/error report.
Successful non-dry runs append hashes and applied operation numbers to
`folder_beacon_patch_ledger.jsonl`, providing an auditable backup ledger.
