# AtlasRecord v1 Adapter Audit

Audit date: 2026-08-11

Specimen: `tp:ME/L5/C1`, the Master Equation trilemma claim.

## Repositories Inspected

- `YellowKidokc/Faith-through-physics-atoms`, branch `OBS-Plugin-Final-Claude`
- `YellowKidokc/argument-compiler`, branch `main`
- `YellowKidokc/the-meta-argument`, branch `OBS-Plugin-Final-Claude`
- local `D:/GitHub/AXIOM-REACT`

The remote repos were inspected without physically merging or cloning them into this repository.

## Argument Compiler Mapping

| Compiler field | AtlasRecord v1 target | Result |
| --- | --- | --- |
| `Source.id/type/title/url/metadata` | `source` | Partial: no content hash or exact span contract |
| `Citation.source_id/locator/url/timestamp` | `source.source_spans`, evidence source | Partial: locator is optional and quote text is not required |
| `Evidence.id/text/citation/confidence` | `evidence_receipts[]` | Partial: no component target, relation strength, coverage, or negative scope |
| `Claim.id/text/status/qualifier/evidence_ids` | `atom_stack.claims[]` | Partial: status taxonomy needs an adapter to Nabla claim modes and Atlas standing |
| `ArgumentEdge.source_id/target_id/relation` | `edges[]` | Direct for supports/attacks/elaborates/depends_on after relation normalization |
| warrants, rebuttals, objections | `atom_stack.warrant`, components, edges, tests | Unmapped: described in README but absent from the draft data model |
| source extraction receipt | `source.provenance`, `audit.subsystem_receipts` | Unmapped: no implemented extraction pipeline in the current repo state |

Argument Compiler must not replace exact source text with a summary. Its adapter is acceptable only when the artifact hash, locator, and quoted span remain reproducible.

## The Meta-Argument Mapping

The repo does have JSON schemas. `schemas/case.schema.json` is a real Draft 2020-12 atomic-case contract, and `schemas/score.schema.json` is its score envelope.

| Meta-Argument field | AtlasRecord v1 target | Result |
| --- | --- | --- |
| `case_id` | `id.record_id` or audit case id | Direct |
| `variables.G/M/E/S/T/K/R/Q/F` | `computed.meta_scores` | Direct after a valid case is constructed |
| answer `UNKNOWN` | deterministic audit | Direct and preserved |
| answer `NOT_APPLICABLE` | deterministic audit | Direct and excluded from scoring by engine rule |
| `refusal_states` | audit warnings/refusal result | Direct |
| `ontological_dependencies` | computed dependencies | Direct |
| score `direction/confidence` | deterministic audit | Direct |
| engine veto and structural significance | deterministic audit/meta scores | Available from engine output, though not fully constrained by `score.schema.json` |
| actor/action/target/cost bearers/beneficiaries | no honest mapping for this formal claim | Unmapped without a formal-claim adapter |
| native C0-C6 grade | `periodic15.marker_10_native_grade` | Unmapped: not emitted by current score schema |
| Atlas A-D/- projection | `periodic15.marker_12_evidence_grade` | Must be computed by Atlas grade registry, not by Meta-Argument |
| H/P/A lane envelope and convergence | `audit` | Unmapped in current public schemas |

The Master Equation claim must not be disguised as a historical action case. A typed `formal_claim` input profile is the smallest honest adapter.

## Master Equation Corrections Applied

- Exact JSON-LD selectors now identify technical statement, plain statement, mathematical form, and claim components.
- `atom_stack` is now first-class and owns local components, claims, dependencies, arguments, warrant, tests, and Ascent/Translation/Descent dynamics.
- Reality Mirror is a separate top-level block rather than a pseudo-marker inside `periodic15`.
- The canonical source file receives a SHA-256 content hash.
- Nabla claim mode is normalized to `FORMAL_DERIVATION`, while the native `formal_derivation` label is retained.
- Marker 4 contains only the accepted economics bridge.
- The proposed theology bridge remains a Candidate and cannot propagate grade.
- Marker 12 is computed through the grade registry. It remains `UNKNOWN` because native `NOT_ESTABLISHED` is not a ratified C0-C6 grade.
- Candidate/Admitted standing comes from the pre-admission gate, including origin and human-audit receipt.

## Still Unmapped

1. Nabla v6 vector, pairing hash, and per-dimension confidence for this exact atom.
2. Argument Compiler native extraction and source-preservation receipt.
3. A formal-claim input adapter for The Meta-Argument.
4. Meta-Argument native grade, normalized grade handoff, and H/P/A convergence envelope.
5. AXIOM-REACT rendering route for this shared record.

These gaps are also emitted inside the gold specimen's `unresolved[]` array so they travel with the record.
