# BUILD PROMPT — CANONICAL CONTENT OS FIRST VERTICAL SLICE

You are implementing the first safe, usable vertical slice of the Faith Through Physics Canonical Content OS in:

`D:\GitHub\Faith-through-physics-atoms`

Use the existing TextGO fork as the desktop popup and selection front end:

`D:\GitHub\TextGO`

TextGO is a Tauri/Svelte application that already supplies selection triggers, global shortcuts, an interactive toolbar, a `popup` window, customizable icons, and extensible script/local-or-cloud-AI actions. Extend that architecture; do not build a second popup shell or passive global keylogger.

**The TextGO worktree already contains uncommitted user/other-agent work**, including changes in the Tauri and popup/executor/shortcut layers plus `SidecarWizard.svelte`. Inspect the current diff before editing, preserve those changes, and integrate around them. Do not reset, overwrite, or revert them.

Read these handoff files completely before touching code:

1. `__1_Version_Last_Version\CANONICAL_CONTENT_OS_V0_1.md`
2. `__1_Version_Last_Version\FOR_KIMI_CANONICAL_CONTENT_OS_BUILD_BRIEF.md`
3. `__1_Version_Last_Version\NODE_ICON_ASSIGNMENTS.json`
4. `__1_Version_Last_Version\OLLAMA_REVIEW_AND_CANON_SESSION_LAYER.md`

Treat the Ollama layer document as the governing boundary for local semantic review: deterministic validators run first, Ollama writes scoped receipts and agenda items, and a separate authenticated human capability performs promotion. Do not collapse those three authorities into one service method.

Then inspect and reconcile—not overwrite—the repository's current vocabulary, stage contracts, schemas, validators, canonical gate, definition resolver, adversarial gate, claim-beacon code, and existing GUI/renderers. Look around first and identify the actual active implementations. Do not create a parallel canon system when an existing component can be extended.

## Objective

Build one complete fixture-only claim route:

```text
type/select CLAIM
 -> semantic search for existing claims
 -> choose NEW / AMEND / NEW VERSION / SUPERSEDE / ADD SUPPORT
 -> complete a short Truth Capsule
 -> reveal claim-specific fields progressively
 -> stage an immutable candidate revision
 -> run deterministic validation
 -> attach one mock or locally configured adversarial-review receipt
 -> present human approval/rejection/exception controls
 -> on approval write fixture canonical JSON-LD
 -> update a rebuildable SQLite projection
 -> generate an HTML pill/view
 -> write a complete audit receipt
```

Do not run this against live canon until the fixture route passes.

## Hard boundaries

- Preserve user files and existing dirty-worktree changes.
- Do not delete, relocate, rename, or rewrite existing canonical records.
- Do not install dependencies or call paid APIs without explicit approval.
- Do not store secrets in source, logs, SQLite, browser responses, or receipts.
- Automatic close may stage and review. It must never automatically promote canon.
- AI review is not Lean verification, empirical replication, or human acceptance.
- JSON-LD/Git remains authoritative. SQLite is a derived, rebuildable index.
- Frozen publications are never silently rewritten.
- Stories/articles with changed upstream truth bindings are marked stale and proposed for review, not blindly edited.
- Invalid, ambiguous, unsupported, or provenance-broken input is preserved in reversible quarantine with a reason and recovery path.
- Canonical Master Equation has nine coordinates. `C_W` is a wrapper, not a tenth coordinate.

## Required first-slice features

### 1. Command/launcher

Implement the entry points through TextGO:

1. **Selected-text route:** selecting text opens the TextGO toolbar; semantic actions such as Claim, Evidence, Definition, Mathematics, Story, and Bridge appear with the proposed node icons. Clicking Claim passes the selected text into the Truth Capsule.
2. **Empty-workbench route:** a configurable TextGO global shortcut opens the same popup without selected text.
3. **Optional typed-command route:** `/claim` may be supported only through an explicit editor/TextGO rule or a small AutoHotkey handoff that invokes TextGO. Do not add broad passive keystroke capture. Ordinary occurrences of the word `claim` must never trigger the popup.

Reuse TextGO's existing `/popup` window and action/executor abstractions. Keep the Canonical Content OS logic behind a narrow local API so the popup can be replaced without changing canon.

### 2. Semantic identity check

Search exact IDs, aliases, normalized statements, definitions, and existing claim text. Return ranked proposals only. Never merge automatically.

### 3. Version action

Implement and display:

- patch: non-semantic metadata/citation/format change
- minor: scope/support clarification with proposition preserved
- major: proposition, definition, mathematics, truth conditions, or conclusion changed
- amend: original preserved with visible correction
- supersede: old snapshot preserved and successor linked

The system proposes; the human confirms.

### 4. Truth Capsule

Collapsed fields:

- permanent claim ID
- exact technical statement
- plain statement
- logical type
- claim species/evidence burden
- current status
- evidence present
- strongest defeater
- largest open gap

Expanded fields are schema-driven by claim species. Do not show every possible field for every claim.

### 5. Candidate staging

Closing writes a candidate artifact and event. It does not overwrite canon. Candidate records must include source hash, prior-version reference, proposed operation, timestamp, author, and current validation state.

### 6. Deterministic validation

At minimum check:

- schema validity
- ID uniqueness and reference integrity
- semantic-version action consistency
- required definitions
- truth/disconfirmation conditions
- evidence contract presence appropriate to claim species
- dependency/status ceiling
- bridge propagation permissions
- provenance and source hash

### 7. Review receipts

Every reviewer receipt records:

- item ID and candidate hash
- reviewer type
- provider/model/tool and version where applicable
- policy or prompt hash
- checks actually performed
- verdict
- warnings/exceptions
- timestamp
- signature or deterministic receipt hash

### 8. Human gate

Explicit choices:

- approve fixture promotion
- return for revision
- accept with recorded exception
- quarantine

No default approval button may fire on page close.

### 9. SQLite projection

Store searchable projections of claims, versions, edges, receipts, events, and quarantine state. Provide a rebuild command from JSON-LD and receipts. Prove rebuildability with a test.

### 10. Generated view

Generate an HTML pill from the accepted fixture JSON-LD. Never hand-edit generated HTML. Show semantic node icon plus lifecycle/status badge using the assignment manifest. If `.ico` assets do not exist, use accessible text/glyph fallbacks and report the missing assets honestly.

## Testing requirements

Run negative controls before the happy path:

1. duplicate claim proposal does not auto-merge
2. semantic major change cannot pass as patch
3. missing dependency is quarantined or blocked
4. status cannot exceed dependency ceiling
5. ungraded bridge cannot propagate
6. AI PASS cannot promote canon
7. stale story binding is flagged, not rewritten
8. broken source hash fails validation
9. database can be deleted and rebuilt from authoritative fixtures
10. generated HTML can be regenerated from the same accepted atom

Then run the positive end-to-end fixture test.

## Required deliverables

- working source code integrated into the existing architecture
- fixture atoms and isolated test data
- automated tests
- launch instructions
- schema and database migration notes
- one end-to-end receipt bundle
- implementation audit:
  - what was implemented
  - what passed deterministically
  - what was runtime/UI tested
  - what remains unimplemented
  - what was deliberately not changed

## Stop conditions

Stop and request David's decision if implementation requires:

- choosing between genuinely conflicting canonical schemas
- changing live canonical IDs or accepted claim meanings
- installing a new service or paid dependency
- creating or using credentials
- migrating or deleting live data
- deciding whether an exception may be accepted as canon

Do not stop merely because the work is large. Complete the safe fixture slice and report any remaining boundary precisely.
