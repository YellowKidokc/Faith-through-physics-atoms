# Baseline Goldens v1.0

**Status:** candidate specification  
**Date:** 2026-09-22  
**POF:** 2828 — Faith-through-physics-atoms

## Purpose

The baseline goldens are the **ruler-approved standard** that every machine lane is measured against. They serve two roles:

1. **Few-shot examples** for LLM extraction, grading, and canonization prompts.
2. **Test fixtures** that the A/B stack-up harness asserts against.

A golden is not just a “good answer.” It is a *bounded* answer: it shows the field completeness, vocabulary discipline, status honesty, and kill-condition quality the project demands.

## Golden slots

| Slot | Node type | Purpose | Status |
|------|-----------|---------|--------|
| `claim_1` | claim | Strongest load-bearing claim in the corpus. Anchor for claim extraction and grading. | `source_to_pick` |
| `claim_2` | claim | A challenged or partially-supported claim. Teaches that negative status is normal, not an error. | `source_to_pick` |
| `evidence_1` | evidence | Verified citation with a clean, accepted edge. Citation-pattern exemplar. | `source_to_pick` |
| `evidence_2` | evidence | Proposed edge with a contested source. Teaches `proposed` vs `accepted`. | `source_to_pick` |
| `bridge_1` | bridge | Cross-domain mapping with `LOST` status and word-gate filled. Bridge anatomy exemplar. | `source_to_pick` |
| `definition_1` | definition | Registry-resident definition with full anatomy. Layer-0 target pattern. | `source_to_pick` |
| `rule_1` | rule | `RULE-CANON-DEF-001` or equivalent constitution atom. The rules as data. | `source_to_pick` |

## Source selection criteria

Each slot needs a **source pointer** in the form:

```yaml
source:
  paper:  "<paper_uuid or path>"
  node:   "<node_id or uuid>"
  reason: "<one sentence why this slot is the canonical example>"
```

Selection rules:

- The source must exist in the corpus as a resolved address or pill.
- The source must be **human-ruler approved** before it becomes a golden.
- The same source may not fill two slots unless its dual nature is explicitly documented.
- A golden’s `status` field must reflect the actual corpus ruling, not an aspirational one.

## Proposed candidates (pending ruling)

These are starting candidates only. They become goldens only after a ruling PR.

| Slot | Candidate source | Ruling needed |
|------|------------------|---------------|
| `definition_1` | `tp:def:terminus-sui` (or its post-migration `DEF-XXXX` row) | Confirm canonical status and full anatomy. |
| `evidence_1` | `tp:def:goedel-incompleteness` source from Stanford Encyclopedia | Confirm citation is accepted. |
| `rule_1` | `RULE-CANON-DEF-001` from the mothership rule atoms | Confirm rule version and receipt. |
| `claim_1` | `tp:axioms/01/AX-001` — Existence floor axiom | Confirm it is load-bearing and well-graded. |
| `claim_2` | `tp:axioms/01/AX-015` — Information Anchor Necessity | Confirm it is proposed/challenged. |
| `bridge_1` | A cross-domain mapping from the master-equation or unification papers | Identify a concrete example with `LOST` word-gate. |
| `evidence_2` | A contested source edge from `_proposals/definition-links.jsonl` | Identify a proposed-but-not-accepted link. |

## Stack-up harness

The A/B harness runs the **same baseline paper set** down two LLM lanes and diffs each lane against these goldens.

```text
baseline papers  ┐
                 ├─>  deepseek lane  ─┐
                 │                     ├─>  Nabla diff  ──>  winner / second opinion
                 └─>  kimi lane      ─┘
```

### Scoring dimensions

1. **Field completeness** — did the lane emit every required field?
2. **Vocabulary discipline** — did it use the canonical terms from `definitions.yaml` / registry?
3. **Status honesty** — did it mark unsupported edges as `proposed`, never `accepted`?
4. **Kill-condition quality** — are falsifiers concrete, testable, and tied to source text?

### Output

- `mothership/reports/stack_up_<timestamp>.json` with per-slot, per-lane scores.
- The lane with the higher aggregate score becomes the **default lane**.
- The other lane remains available as a **second opinion**.

## Integration

- `mothership/llm_client.py` provides the multi-provider client.
- `mothership/tools/stack_up.py` (future) loads this spec, fetches pills by UUID, and runs the harness.
- `mothership/specs/BASELINE_GOLDENS_v1.0.md` is the source of truth for golden definitions and source selections.

## Files

- `mothership/llm_client.py` — provider-agnostic client.
- `mothership/specs/BASELINE_GOLDENS_v1.0.md` — this document.
- `mothership/reports/` — future stack-up reports.

## Next steps

1. Ruler selects and approves one source per slot.
2. Populate the `source:` block for each slot above.
3. Extract or author the canonical golden response for each slot.
4. Run the stack-up harness on a small baseline paper set.
5. Lock the golden versions and version-stamp this spec.
