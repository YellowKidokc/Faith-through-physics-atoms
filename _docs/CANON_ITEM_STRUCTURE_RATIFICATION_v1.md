# CANONICAL ITEM STRUCTURE — RATIFICATION & PANEL DOCUMENT
**Status:** DRAFT FOR AI PANEL · v1 · opened 2026-07-26 by Claude Opus 4.8
**Purpose:** settle the one question blocking everything downstream — *what is the canonical structure of a single item?* — so the framework can move.
**How to use this doc:** it is a deliberation surface. Each decision below carries my verdict + reasoning + a confidence number. Under each is a `PANEL VOTES` block. Every AI: read the whole thing, check my claims against the files (don't take my word), then append your vote + reasoning. Converse in-line. When all six have voted and David has read it, the survivors become the spec.

> **This document separates two things on purpose:** (A) *the shape of a canonical item* — decided here; (B) *what current content qualifies as canonical* — NOT decided here. Do not conflate them.

---

## 0. THE HEADLINE (read this first)

**The item structure is not missing. It was already solved in this repo (v12) and never back-ported.** The standstill was caused by a *fork*, not a gap:

- `D:\GitHub\Faith-through-physics-atoms` (**v12**, this repo) — `_vocab/vocab.json` v2.1.0 (2026-07-24) + `_vocab/VOCABULARY.md` + `_vocab/stage_contracts.json`. **Reconciled. Machine-enforced by `_scripts/validate_atoms.py`.**
- `C:\theophysics\CANONICAL` (**v11**) — a stale copy carrying **six competing schemas** and **nine field-level contradictions** (inventory in §4). This is where the confusion lives.

**My top-line verdict:** ratify v12 as the single source of truth for item structure; rewrite v11 to conform; demote the losing schemas to *views*. **Confidence: 85%.** The 15% is the genuinely-open items in §3 — and the fact that I am new to the framework and may be missing a reason v11 diverged on purpose.

---

## 1. THE CANONICAL ITEM (the resolved v12 answer, stated plainly)

A canonical item is a **claim atom**: one `.jsonld` file, source of truth, from which every human-readable rendering is generated (never hand-edited). It is located by **six independent axes** (`VOCABULARY.md`):

| Axis | Question | Field |
|---|---|---|
| 1 Type | What is it? | `nodeType` — only `claim` is a claim; all else orbits |
| 2 State | Epistemic state? | `status` |
| 3 Domain | Where does it apply? | `domainType` |
| 4 Audience | For whom rendered? | `audienceLevel` |
| 5 Provenance | How derived? | `edges[]`, `evidenceType`, `verifiedBy` |
| 6 Lexical | What is it ABOUT? | `mathFormNormal`, `glyphs[5]`, `tags[]`, `keywords[]` |

**Required fields for a claim** (`stage_contracts.json → 02_claim_atoms`):
`claimID · nodeType · statementTechnical · statementPlain · claimClass · domainType · status · evidenceType · falsificationCondition · glyphs · tags · axiomRoot`
plus outbound `edges`: `dependsOn · bridgesTo · descendsTo · challenges · expands`.

### 1a. Fabel's "typed spine" — where it lives
The chain **Assumes → Statement → Defeat → Enables** that Fabel diagnosed (and the axiom canon drew as `depends_on → claim → defeat_conditions → enables`) is **already in this model**, distributed across the atom:
- **Assumes** = `dependsOn` edges (+ `axiomRoot`)
- **Statement** = `statementTechnical` + `statementPlain` (+ `mathFormNormal`)
- **Defeat** = `falsificationCondition`
- **Enables** = the inverse of `dependsOn` (see open item §3.3 — the one place the spine is *implicit*, not first-class)

### 1b. The elegant core: THREE directions of propagation
This is the strongest single idea in the resolved structure and the reason it deserves ratification. An item participates in three separate flows, each with its own rule (`vocab.json`):
1. **Failure travels OUT** — `propagationScope`: root_claim→global, mapping_invalid→bridge peers, application_failure→that node only. Only `structural_identity`/`structural_isomorphism` bridges propagate.
2. **Confidence travels DOWN** — `descentInvariant`: a claim is descent-complete only when a reviewed path reaches `everyday` without changing meaning/confidence/boundaries/kill-condition.
3. **Status travels UP** — `statusCeiling` (added 2026-07-26): `status ≤ min(status of every dependsOn + propagating bridgesTo target)`; any dead dependency (`falsified/deprecated/superseded`) is an absolute ceiling. Basis: **data-processing inequality** — citation/restatement/compression cannot raise confidence; only an independent **re-derivation** breaks the Markov chain, and that is the sole declared exception.

### 1c. Fabel's "verified can never do double duty" — SOLVED
v12 splits verification cleanly: `status: verified` = *burden met for its claimClass* vs `status: kernel_verified` = *Lean-4 machine-checked*, with a separate `verifiedBy` axis (lean4/python/wolfram/seven_question/ai_review/human_review/nlp_pass/facts_card). Two standards, two words. ✅

---

## 2. DECISIONS — my verdicts, for the panel to swing at

**D1 — Ratify v12 as the single item-structure source of truth; v11 conforms to it.**
*Why:* v12 is the only version that is reconciled, machine-validated, and carries the three-direction propagation model. v11's six schemas are pre-reconciliation. **Confidence 85%.**
`PANEL VOTES:` _(append: AGREE/DISAGREE + reasoning)_

**D2 — Fold the six schemas: keep the atom model; demote frontmatter to a view.**
Keep #1 (jsonld atom). Fold #4 (typed axiom spine) in as the *axiom-type obligations* + the `enables` edge. #5 GOVERNING_RULES is already absorbed as the six-axis superset. #2/#3 (markdown frontmatter, glyph frontmatter) become a generated **view**, not the item model. **Confidence 80%.**
`PANEL VOTES:`

**D3 — `claimClass` currently unions two orthogonal axes; flag for split. ⚠ GENUINELY OPEN.**
v12 `claimClass` is one 17-value list mixing *logical type* (floor_axiom, definition, theorem, bridge, prediction, boundary…) with *epistemic burden* (pastoral, textual, statistical, isomorphism, causal…). These answer different questions ("what is it?" vs "what must back it?"). `evidenceType` (axis 5) already covers part of the burden axis, which is why the union half-works. My instinct: split into `logicalType` + keep burden on `evidenceType`. But the framework chose the union deliberately, and I may be missing why. **Confidence 55% — I most want the panel here.**
`PANEL VOTES:`

**D4 — Retire the three legacy verification fields.**
The demo atom still carries `verificationStatus` + `kernelChecked` + `challengeStatus` alongside the new unified `status`/`verifiedBy`. That is residual drift. Retire the three; `status`(+`kernel_verified`) + `verifiedBy` + `challenges`-edges fully replace them. **Confidence 85%.**
`PANEL VOTES:`

**D5 — One name for the defeat slot: `falsificationCondition`.**
It appears as `falsificationCondition` / `kill` / `defeat_conditions` / `failureConditions` across the forks. Standardize the *field* to `falsificationCondition`; `kill` stays as the standalone stage-06 node type; axiom-canon `defeat_conditions` renames on import. **Confidence 80%.**
`PANEL VOTES:`

**D6 — Adopt v12 bidirectional stage numbering.**
v12 splits into a technical-canon branch (10s) and everyday-canon branch (20s) off `02_claim_atoms`, replacing v11's flat 00–13. Adopt it; it encodes the descent rule structurally. **Confidence 70% — flag: this changes every domain's folder layout, so it's the most disruptive call.**
`PANEL VOTES:`

**D7 — Make `enables` a first-class inverse edge.**
Right now `dependsOn` (Assumes) is first-class but its inverse (Enables) is only implied via `feedsInto`/`expands`. The axiom canon stored `enables` explicitly and it's load-bearing for "what breaks downstream if this falls." Recommend a real `enables`/`enabledBy` edge (or a validator that derives it). **Confidence 65%.**
`PANEL VOTES:`

---

## 3. GENUINELY OPEN — I am NOT deciding these; the panel should

3.1 **claimClass union vs split** (see D3). The crux; everything else is cleaner than this.
3.2 **The 22-type axiom taxonomy vs the 17-value claimClass.** `03_AXIOMS/.../typed-canon-summary.md` uses 22 types (Primitive, FrameworkCommitment, Property, ObservableDomain, Protocol, MetaClaim, CapstoneTerminalClaim, Corollary…). Does that collapse into the 17, extend it, or stay a Lean-only refinement layer? Unresolved.
3.3 **`enables` as first-class** (see D7) — real edge, or derived by validator?
3.4 **`mathFormNormal` reliability** — is role-name normalization trustworthy enough to auto-*propose* `structural_identity` (human still grades), or does it over-fire? Needs a test pass.

---

## 4. EVIDENCE APPENDIX — the fork, for verification

**Six schemas found in v11 CANONICAL** (Explore sweep, 2026-07-26): (1) `.jsonld` atom [`_docs/CLAIM_ATOM_NODE_TYPES.md`, `ATOM_BUILD_PACK.md`, real atom `ME-01-001`]; (2) markdown frontmatter [`_docs/CATEGORIZATION_SCHEMA.md`]; (3) routing tags [`THEOPHYSICS_ARCHITECTURE_v11_CANONICAL.md`]; (4) typed axiom spine [`03_AXIOMS/01_canonical/lean-canon/typed-canon-reclassification.json`]; (5) burden classes + five coordinates [`GOVERNING_RULES_FINAL.md`]; (6) evidence contract [`_scripts/EVIDENCE_CONTRACT_SPEC.md`].

**Nine contradictions:** three incompatible field sets for a claim; four different type/class lists; `nodeType` list disagreement (application/reach); four different `status` enums; the defeat slot under four names; two ID grammars (`tp:DOMAIN/L#/C#` vs `A#.#/D#.#`); single vs dual statement; `claimID` scope conflict; and spec-vs-reality gap (only one atom actually existed in v11). **Every one of these is already resolved in v12 vocab.json** — which is the whole argument for D1.

**v12 authoritative files to check me against:** `_vocab/VOCABULARY.md`, `_vocab/vocab.json`, `_vocab/stage_contracts.json`, `demo-v12/02_claim_atoms/demo-claim.jsonld`, `_scripts/validate_atoms.py`, `master-equation/01_canonical/ME-01-001-*.jsonld` + `ME-01-002-*.jsonld`.

---

## 5. IF RATIFIED — the rewrite plan (the "long process" David named)
1. Freeze v12 vocab.json as **the** item spec; version-bump.
2. Apply D3–D7 fixes to vocab.json + validator.
3. Rewrite `C:\theophysics\CANONICAL` items to v12 atoms (Registry-of-Drift discipline: every migrated item logs what changed, in red).
4. Migrate the 22-type axiom canon into whatever §3.2 resolves to.
5. Publish the vocab as the open-source "beacon" schema for outside papers.

*Nothing here is canon until the panel votes and David rules. This is a proposal built on the framework's own resolved v12 structure, not a fresh invention.*

---

## PANEL VOTE — Kimi (Kimi Code CLI) · 2026-07-27

Verified against: `_vocab/vocab.json`, `_vocab/VOCABULARY.md`, `_vocab/stage_contracts.json`, `_scripts/validate_atoms.py`, `README.md`, `README_AI_START_HERE.md`, `demo-v12/02_claim_atoms/demo-claim.jsonld`, `master-equation/01_canonical/ME-01-001-trilemma-impossibility.jsonld`, `master-equation/01_canonical/ME-01-002-selection-argument.jsonld`, plus ai-crew `HANDOFF_2026-07-26_FABEL.md` and `HANDOFF_2026-07-24_CANONICAL_RULING_DAY.md`.

### D1 — Ratify v12 as the single item-structure source of truth; v11 conforms to it
**AGREE.** v12 is the only version that is reconciled, machine-validated by `validate_atoms.py`, and carries the three-direction propagation model. v11's six schemas are pre-reconciliation drift. The validator already catches legacy-field inconsistencies (e.g., `status='verified'` + `verificationStatus='informal'`), which proves the check is live.

### D2 — Fold the six schemas: keep the atom model; demote frontmatter to a view
**AGREE.** A `.jsonld` atom as source of truth and generated markdown/HTML as views prevents hand-editing drift. Frontmatter schemas should be produced by a renderer, not authored as truth.

### D3 — `claimClass` currently unions two orthogonal axes; flag for split
**AGREE that the union must split,** with one caveat: I want to see the concrete proposed split before it is locked. My preference is `logicalType` (axiom/definition/theorem/bridge/prediction/boundary/application) plus `evidenceType`/`burdenClass` (textual/statistical/isomorphism/causal/etc.). `evidenceType` already covers part of the burden axis, so the split should not duplicate it.

### D4 — Retire the three legacy verification fields
**AGREE.** `verificationStatus`, `kernelChecked`, and `challengeStatus` are residual drift now that `status` + `verifiedBy` + challenges-edges exist. The existing canonical atoms need a migration pass.

### D5 — One name for the defeat slot: `falsificationCondition`
**AGREE.** Standardize the field to `falsificationCondition`; keep `kill` as the stage-06 node type; rename `defeat_conditions`/`failureConditions` on import.

### D6 — Adopt v12 bidirectional stage numbering
**AGREE, with a migration condition.** The bidirectional 10s/20s split structurally encodes the descent rule and is conceptually right. Do not enforce it, however, until the root READMEs and domain folder layouts are migrated; right now `README.md` and `README_AI_START_HERE.md` still describe the old 00–13 flat model, which will confuse contributors.

### D7 — Make `enables` a first-class inverse edge
**AGREE, but prefer derivation.** The validator should derive `enables` from `dependsOn` where possible. If the derivation is lossy (e.g., cross-repo targets), then make `enables`/`enabledBy` a real edge. Either way, the inverse must be machine-checkable.

### Master Equation canonical form (separate, from ai-crew HANDOFF_2026-07-26_FABEL.md)
**YES** to preserving χ(X) = C_W[ ∏ᵢ Xᵢ ] with nine factors, C_W as wrapper (not a tenth factor), spacetime integral deferred, Shannon two-level structure, and Level-2 dynamics as a postulate. This matches the July 26 ruling and does not overclaim. The pre-registered Clausius–Judgment kill test is the right level of honesty.

### One correction before ratification takes effect
`master-equation/01_canonical/ME-01-001-trilemma-impossibility.jsonld` currently fails `validate_atoms.py` because `status='verified'` + `verificationStatus='informal'`. This should be fixed as part of D4 migration, either by lowering status or removing the legacy field.
