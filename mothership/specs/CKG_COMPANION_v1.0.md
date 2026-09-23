# CKG Companion v1.0 — Mothership Publication Spec

**Status:** candidate specification  
**Date:** 2026-09-22  
**POF:** 2828 — Faith-through-physics-atoms  
**Companion type:** `axiom_companion`

## 1. Purpose

A **CKG companion** is a machine-readable review wrapper produced by the Claim-Knowledge-Grade (CKG) pipeline for a paper, chapter, or major claim.  It carries a structured front-matter face, a section-by-section scorecard (S01–S10), and the original article body.

The mothership **publishes** companions into `mothership/companions/` so that the curator can ingest them alongside pills and address maps.  Publication is a one-way, additive transform: the source file is never modified.

## 2. File format

A companion is a Markdown file with YAML front matter followed by a Markdown body.

### 2.1 Front matter

Front matter MUST be valid YAML.  It MAY be presented in either of two equivalent forms:

1. **Bare YAML front matter** — delimited by `---` at the very top of the file.
2. **Fenced YAML block** — wrapped in ` ```yaml ` / ` ``` ` (legacy CKG export format).

The publisher accepts both forms and rewrites the normalized copy as bare YAML front matter.

### 2.2 Body

The body MUST contain:

- A `## SCORECARD` table mapping sections S01–S10.
- Section headings `## S01 · ...` through `## S10 · ...`.
- The original article text after the scorecard sections.

The publisher does not rewrite the body except to preserve it verbatim.

## 3. Required front-matter fields

| Field | Type | Description |
|-------|------|-------------|
| `paper_uuid` | string | Stable identifier for the paper.  Minted as UUIDv5 if absent. |
| `title` | string | Human-readable title. |
| `clean_title` | string | Title slug used for filenames and display. |
| `status` | string | One of the status vocabulary values (§4). |
| `type` | string | Companion type, e.g. `axiom_companion`, `claim_companion`. |
| `one_sentence_finding` | string | Compressed central claim. |
| `claim_ids` | list[string] | Stable claim identifiers referenced by the companion. |
| `score_total` | int | Total score. |
| `score_ceiling` | int | Maximum possible score. |
| `score_class` | string | Class label, e.g. `CANDIDATE`. |
| `build_next` | string | Curator-facing recommendation for the next build action. |
| `s01_pos`..`s10_pos` | int | Positive points per section. |
| `s01_neg`..`s10_neg` | int | Negative points per section. |
| `s01_net`..`s10_net` | int | Net points per section. |
| `s01_ceiling`..`s10_ceiling` | int | Per-section ceiling. |

Optional but recommended fields: `paper_id`, `original_title`, `canon_status`, `semantic_status`, `template_version`, `taxonomy_ref`, `source_file`, `source_sha256`, `captured_at`, `chapter`, `content_type`, `reader_category`, `domain_primary`, `domain_secondary`, `domain_tertiary`, `tags`, `framework_keys`, `governing_question`, `topic_keys`, `paper_rating`, `evidence_status`, `formal_status`, `lean_receipts`, `human_review`, `chains_loadbearing`, `chains_honesty`, `integrity_bonus`, `gated`, `semantic_provider`, `semantic_model`, `run_id`, `processed_date`.

## 4. Status vocabulary

Companions use the following status values:

| Status | Meaning |
|--------|---------|
| `CANDIDATE_DRAFT` | Initial AI-analyzed companion awaiting review. |
| `CANDIDATE` | Passed basic validation, ready for curator queue. |
| `REVIEW_PENDING` | Queued for human or adversarial review. |
| `UNDER_REVIEW` | Active review in progress. |
| `ACCEPTED` | Companion and its claims accepted into canon track. |
| `REJECTED` | Companion failed review; retained for audit. |
| `RETIRED` | Superseded by a newer companion. |

## 5. Claim ID conventions

Claim IDs SHOULD follow the pattern `<paper_id>-C<nnn>` (for example, `temporal_direction_breakthrough-C001`).  Hidden premises may use `<paper_id>-HP<nnn>`.

Each `claim_id` in `claim_ids` SHOULD have a stable UUID.  The publisher mints a UUIDv5 from the claim ID (project namespace `faiththruphysics.com`) and stores it in the `claim_uuids` map if the source file does not already provide one.

## 6. Relationship to pills, addresses, and mothership

| Artifact | Relationship |
|----------|--------------|
| **Pills** | A companion is a fat review wrapper; its claims are extracted as pills. |
| **Address maps** | The companion's `paper_uuid` links to paper address maps. |
| **Mothership** | The mothership reads `companions/index.json`, pulls companions by `paper_uuid`, and feeds them to the curator as candidate bodies. |
| **Curator** | The curator uses `build_next`, `score_class`, and claim UUIDs to rank proposals. |

## 7. Normalized filename

Published companions are named:

```
<paper_uuid>_<clean_title_slug>.md
```

The `clean_title` is lowercased, non-alphanumeric characters are replaced with underscores, and consecutive underscores collapse to one.  Leading/trailing underscores are stripped.

Example: `16166191_temporal_direction_insight.md`

## 8. `companions/index.json`

The publisher maintains an atomic index of published companions.  Each entry contains:

```json
{
  "paper_uuid": "16166191",
  "title": "The Temporal Direction Insight",
  "status": "CANDIDATE_DRAFT",
  "path": "companions/16166191_temporal_direction_insight.md",
  "source_file": "/mnt/data/TEMPORAL_DIRECTION_BREAKTHROUGH.md",
  "claim_ids": ["temporal_direction_breakthrough-C001", ...]
}
```

The index is written atomically (write temp + rename) so concurrent publisher runs cannot corrupt it.

## 9. Short example

```yaml
---
type: axiom_companion
title: "The Temporal Direction Insight"
paper_id: "temporal_direction_breakthrough"
paper_uuid: "16166191"
clean_title: "The Temporal Direction Insight"
status: CANDIDATE_DRAFT
one_sentence_finding: "Unification of General Relativity and Quantum Mechanics requires a zero-width boundary operator (L)..."
claim_ids:
  - "temporal_direction_breakthrough-C001"
  - "temporal_direction_breakthrough-C002"
  - "temporal_direction_breakthrough-C003"
score_total: 71
score_ceiling: 100
score_class: CANDIDATE
build_next: "Focus on formalizing the Bool -> Hilbert bridge..."
s01_pos: 9
s01_neg: 0
s01_net: 9
s01_ceiling: 10
# ... s02..s10 omitted for brevity
---

## SCORECARD

| § | Section | Pos | Neg | Net | Ceiling | Chain |
|---|---------|-----|-----|-----|---------|-------|
| S01 | Classification & Routing | 9 | 0 | 9 | 10 | — |
| ... | ... | ... | ... | ... | ... | ... |

## S01 · Classification & Routing
...

## S02 · Claim Definition
...
```
