# Master One-Page Buildout Plan

Last updated: 2026-07-09

## Short Answer

The best complete plan is now here:

`D:\GitHub\Python-WEB\workflows\paper-intelligence-topbar-bridge`

This folder should be the working home.

The ideas came from three places:

1. Codex outputs from the local audit pass.
2. `THEOPHYSICS_PAPER_INTELLIGENCE\08_SITE_TOPBAR_MANIFEST_BRIDGE`.
3. The site/source audits comparing the Faith Through Physics repos.

## Best Current Source Pieces

### Best Page Body Candidate

Use the page-quality audit result as the source signal:

- Best formatted page body/template found:
  `D:\GitHub\faiththruphysics-site-v2\convergence-deep\cdt-01-math-is-moral.html`

- Best regular-series pilot:
  `D:\GitHub\faiththruphysics-site-v2-lean-deploy\revolution-of-truth\index.html`

Use the first as the strongest body-style reference.
Use the second as the safest pilot series because it has matched easy/academic assets.

### Best Topbar Candidate

Topbar was structurally solved enough to stop optimizing for it first.

Current strongest known topbar source:

`D:\GitHub\faiththruphysics-site-v2\assets\faith-topbar.js`

and its matching CSS.

### Best Variable Spec

Primary file:

`D:\GitHub\Python-WEB\workflows\paper-intelligence-topbar-bridge\01_specs\topbar-page-variable-master-spec.md`

This is the best current map of what the topbar/page manifest needs.

### Best One-Page Layer Protocol

Source concept:

`C:\Users\David\Documents\Codex\2026-07-08\d-github-david-os-apps-desk\outputs\one-page-reader-layer-marker-spec.md`

This should be copied into this workflow as the canonical one-page marker protocol.

## Core Architecture

Do not make one giant script own everything.

Use a two-input manifest system:

```text
site_inventory.json
    +
paper_metric_manifest.json
    =
one_page_html_manifest.json
```

The site inventory owns:

- page slug
- series order
- previous/next page
- file paths
- topbar presence
- layer source paths
- HTML marker positions

Paper Intelligence owns:

- proof scores
- claim counts
- law/variable activation
- coherence scores
- graph metrics
- reading difficulty
- audit/falsification status

The final page builder reads the merged manifest and inserts or updates one canonical HTML page.

## One-Page Rule

Each article should become one canonical HTML page.

Inside that page, use invisible HTML comments as hard machine boundaries:

```html
<!-- READER-LAYER:01:college:BEGIN -->
<section id="reader-layer-college" data-reader-layer="college" data-layer-order="01">
  ...
</section>
<!-- READER-LAYER:01:college:END -->

<!-- READER-LAYER:02:easy:BEGIN -->
<section id="reader-layer-easy" data-reader-layer="easy" data-layer-order="02" hidden>
  ...
</section>
<!-- READER-LAYER:02:easy:END -->

<!-- READER-LAYER:03:academic:BEGIN -->
<section id="reader-layer-academic" data-reader-layer="academic" data-layer-order="03" hidden>
  ...
</section>
<!-- READER-LAYER:03:academic:END -->
```

The comments are for scripts and Codex.
The `section` attributes are for the browser.

## Reader Layers

Start with these layers:

1. `college`
2. `easy`
3. `academic`
4. `proof`
5. `math`
6. `source`
7. `audit`
8. `falsification`
9. `qa`
10. `metadata`

The visible default is `college`.

## Expanded Topbar / Page Variables To Add

The existing variable list is good, but it should grow. Add these as first-class manifest fields or nested groups.

### Identity

- `canonical_claim_id`
- `claim_family_id`
- `series_generation`
- `page_revision`
- `content_hash`
- `source_hash`
- `manifest_hash`
- `last_verified_at`

### Reader Layer Health

- `college_layer_status`
- `easy_layer_status`
- `academic_layer_status`
- `proof_layer_status`
- `math_layer_status`
- `source_layer_status`
- `audit_layer_status`
- `falsification_layer_status`
- `qa_layer_status`
- `metadata_layer_status`
- `missing_layer_count`
- `stale_layer_count`
- `layer_alignment_score`

### Proof / Claim Health

- `claim_count_total`
- `claim_count_primary`
- `claim_count_supporting`
- `anchored_claim_count`
- `under_supported_claim_count`
- `overclaim_count`
- `falsifiable_claim_count`
- `kill_condition_count`
- `derivation_chain_count`
- `unmapped_derivation_count`
- `proof_gap_count`
- `proof_confidence_label`

### Master Equation / Law Health

- `active_law_count`
- `inactive_law_count`
- `dominant_law`
- `dominant_variable`
- `weakest_variable`
- `variable_balance_score`
- `law_coverage_score`
- `bridge_integrity_score`
- `signature_match_score`
- `swap_rejection_status`

### Evidence / Audit Health

- `source_count`
- `citation_count`
- `primary_source_count`
- `external_validation_count`
- `audit_status`
- `audit_last_run`
- `audit_failure_count`
- `falsification_status`
- `strongest_objection`
- `open_objection_count`
- `resolved_objection_count`

### Reading / UX

- `word_count`
- `estimated_read_minutes`
- `reading_grade`
- `reading_level_label`
- `equation_count`
- `diagram_count`
- `table_count`
- `audio_available`
- `read_aloud_ready`
- `mobile_layout_status`

### Site / Navigation

- `prev_page_id`
- `next_page_id`
- `parent_series_id`
- `collection_id`
- `breadcrumb_path`
- `local_html_path`
- `public_url`
- `asset_base_path`
- `topbar_version`
- `shell_version`

### Graph / Intelligence

- `graph_node_id`
- `graph_cluster`
- `graph_centrality`
- `incoming_link_count`
- `outgoing_link_count`
- `related_claim_ids`
- `related_page_ids`
- `dependency_parent_ids`
- `dependency_child_ids`
- `cross_domain_bridge_count`

This adds more than 50 extra candidate fields. Do not force them all into the visible topbar. The visible topbar should show only the best small subset; the rest belong in the hidden page manifest and proof panel.

## High-Value Claim Seeds To Carry Forward

### The Three-Body Solution

Spec file:

`01_specs\three-body-solution-claim-seed.md`

This is a convergence claim across:

1. Maxwell / Heaviside field coupling.
2. Watcher Problem / terminal observer regress.
3. Justice / Mercy / Free Will optimization.

Shared proof shape:

```text
n = 1 self-defeats
n = 2 deadlocks or collapses a required invariant
n = 3 is the unique minimal fixed point
```

This should become a full claim page or proof-drawer module because the cross-domain proof shape is stronger than any single example.

### The J-Space and the Cathedral

Spec file:

`01_specs\j-space-and-the-cathedral-paper-seed.md`

This is the AI-consciousness / workspace paper seed.

Core framing:

```text
Anthropic found a genuine access-workspace layer.
That does not prove phenomenal consciousness.
It does support the framework's projection/substrate distinction.
Law 6 maps to the visible workspace.
Law 10 predicts the deeper coherence substrate beneath it.
```

This should become either:

- a standalone claim page,
- a proof-drawer module under the consciousness/AI lane,
- or a current-events bridge page that ties Anthropic's J-space result to the framework without overclaiming.

## Build Order

1. Keep `revolution-of-truth` as the pilot.
2. Export `paper_metric_manifest.json` from Paper Intelligence.
3. Build `site_inventory.json` from the site repo.
4. Merge them into `one_page_html_manifest.json`.
5. Insert the reader-layer manifest and invisible layer markers into one pilot page.
6. Add the visible topbar panel from the merged manifest.
7. Run Playwright visual checks on desktop and mobile.
8. Only then apply to the rest of the series.

## Existing Python-WEB Tools To Reuse

These already exist in `D:\GitHub\Python-WEB` and should be reused before adding new machinery:

- `apply_faith_topbar.py` - applies the shared Faith Through Physics topbar assets.
- `audit_v2_layer_coverage.py` - audits v2 pages for layer sources, reader tabs, topbar, audio dock, and MTL hooks.
- `import_reading_layers.py` - imports reading-layer source material.
- `audit_reading_layers.py` - audits `reading_layers` manifests.
- `scan_site_layers.py` - scans site layer presence.
- `extract_site_math_translation_layer.py` - extracts math translation content.
- `topbar_contract.py` - likely the right place to align visible topbar field expectations.
- `theophysics-site-repair\modules\inventory.py` - candidate base for `site_inventory.json`.
- `theophysics-site-repair\modules\inject_reader_modes.py` - candidate base for page-layer insertion.
- `theophysics-site-repair\modules\replace_topbar.py` - candidate base for topbar replacement.

`apply_reader_mode_baseline.py` is referenced in `00_AI_START_HERE.md`, but was not found during the prior pass. Treat it as missing until proven otherwise.

## Guardrails

- Do not let Paper Intelligence edit HTML.
- Do not make the website parse giant Excel files.
- Do not run full-site conversion before the pilot passes.
- Do not hide the original/college page body behind another page.
- Do not delete separate easy/academic source assets; use them as inputs.
- Do not show every metric in the topbar. Most variables should stay in the manifest/proof drawer.

## Next Coding Step

Implement the exporter first:

`export_page_metric_manifest.py`

Then implement the site inventory builder:

`build_site_inventory.py`

Then implement the merger:

`merge_one_page_manifest.py`

The page writer comes last.
