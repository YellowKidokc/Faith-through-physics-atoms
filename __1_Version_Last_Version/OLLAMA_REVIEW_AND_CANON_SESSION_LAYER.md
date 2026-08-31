# OLLAMA REVIEW AND CANON SESSION LAYER
## Notebook handoff for AI collaborators and implementers
## Status: partly present, partly specified; not yet one finished end-to-end service

## The short version

Ollama is the local reasoning layer that helps the Canonical Content OS notice trouble early and prepare the next human canonization session. It does not decide truth, rewrite accepted canon, certify Lean, or promote anything. It reads staged candidates and the graph around them, performs only the review jobs assigned to it, and writes bounded receipts: objections, conflicts, missing evidence, possible duplicates, affected dependents, stale story bindings, and recommended next tests.

> **Deterministic code establishes mechanical facts. Ollama performs scoped semantic review. Humans adjudicate canon.**

Ollama is not the canonizer. It is the local, inexpensive first reviewer and agenda builder.

## What exists now

- Ollama is installed and its local API is responding at `http://127.0.0.1:11434`.
- Models observed on 2026-08-25: `qwen3:4b-instruct`, `gemma4:latest`, `llama3.2:3b`, and `nomic-embed-text:latest`.
- TextGO already contains an Ollama provider and can serve as the capture/popup client.
- `_scripts/adversarial_review.py` already implements a provider-neutral adversarial gate for proposed relationships.
- That gate has deterministic-offline and OpenAI-compatible paths, fails to `uncertain`, writes receipts, lets `oppose` block a proposal, and never promotes it.
- Receipts are stored in `_proposals/adversarial-reviews.jsonl`.
- The current rubric checks epistemology, ontology, logic, and falsification.
- Existing atoms, proposals, ledgers, schemas, validators, and `canon_guard` material must be extended rather than replaced.

Not yet present as one completed runtime:

- a watcher connecting filesystem/Git changes to all review jobs;
- complete content-hash and upstream-dependency invalidation;
- every contradiction represented as a first-class conflict node;
- full impact tracing for stories, papers, equations, and frozen publications;
- an automatically generated canon-session agenda;
- a finished local API joining TextGO, the graph, receipts, Ollama, and human adjudication.

Any AI describing this layer must preserve that distinction.

## The mechanism

### 1. Capture is permissive

Selected text, a typed claim, harvested statement, correction, or amendment enters as an immutable candidate with an ID, timestamp, source, and content hash. Entry is default-yes because it is reversible. It may be incomplete, contradictory, or wrong; its status must say so.

Rejection requires a located reason: the failed contract, triggering evidence, and smallest condition that would resolve it. A bare `FAIL` is insufficient.

### 2. Deterministic checks run first

Code—not an LLM—settles mechanical facts:

- schema validity;
- identity and duplicate IDs;
- source existence and hashes;
- version-transition rules;
- missing dependencies and dependency/status ceilings;
- ungraded bridge propagation;
- frozen-record protection;
- Lean receipt existence and hash match, without impersonating Lean;
- rebuildability of the derived SQLite projection.

Results are authoritative only for the exact checks performed.

### 3. Ollama receives a bounded review packet

The runtime sends the candidate, relevant canonical neighbors, dependencies, evidence contract, negative controls, kill conditions, existing objections, and one reviewer rubric. It should not dump the whole corpus into every prompt.

Named review roles may include:

- adversarial: strongest reason the candidate or edge should fail;
- contradiction: incompatible claims or definitions;
- evidence: whether evidence supports the stated burden and grade;
- bridge: preserved properties, category errors, and propagation permission;
- provenance: suspicious attribution not caught deterministically;
- story-binding: prose spans made stale;
- impact: downstream items affected;
- duplicate: semantic merge candidates, never an automatic merge.

The model may propose a conclusion. It may not silently edit the candidate to make it pass.

### 4. Every review produces a receipt

At minimum:

- candidate ID and content hash;
- reviewer role;
- provider, model, and model version/digest where available;
- prompt/policy hash;
- checks attempted and graph-neighborhood references;
- verdict: `pass`, `oppose`, `uncertain`, or `error`;
- located objections and evidence;
- required tests or smallest repair;
- advisory confidence;
- timestamp, receipt hash, and resulting gate state.

An Ollama `PASS` means only that this reviewer found no defeating problem under this packet and rubric. It does not mean proved, replicated, theologically established, or canonical.

### 5. Conflicts remain visible

Divergence is not itself failure. Undetected divergence is.

Incompatible records create or update a conflict record with both sides, versions, hashes, dependency blast radius, receipts, and unresolved status. It remains searchable and appears on the next agenda. It is not hidden in an archive or resolved by model preference.

### 6. Review is event-driven

Re-review triggers on meaningful invalidation:

- candidate content changes;
- a governing definition, axiom, equation, or dependency changes;
- source hash or provenance changes;
- bridge grade or propagation permission changes;
- a prior objection is answered;
- a deliberate model/policy refresh campaign runs;
- a human launches a full audit sweep.

Unchanged items are not repeatedly reviewed on a timer.

### 7. The output is a canon-session agenda

The main product is not a stream of popups. It is the prepared agenda for David and the AI crew:

- candidates changed since the last session;
- conflicts opened, closed, or widened;
- high-blast-radius changes;
- status/dependency ceiling violations;
- stale story and paper bindings;
- frozen publications with superseded upstream claims;
- failed deterministic checks;
- adversarial objections and required tests;
- items ready for adjudication;
- unresolved items ranked by consequence, not arrival time.

### 8. Human promotion is separate

The reviewer process must not possess the credential or code path used for canonical promotion. Human choices are explicit: promote, return, accept with exception, keep unresolved, or reject with a located reason. Accepted canon is immutable at that version; corrections create successors and supersession links.

## Component boundaries

- **TextGO:** capture and display through a narrow local API. Canon logic stays out of TextGO.
- **Canonical Content OS service:** identity, staging, contracts, deterministic validation, graph traversal, receipts, agendas, and authenticated human promotion.
- **Ollama:** replaceable local semantic reviewer behind a provider adapter.
- **JSON-LD/Git:** authoritative records and history.
- **SQLite:** derived, searchable, and rebuildable.
- **Lean/formal tools:** separate verifiers whose real outputs and axiom footprints become receipts. Ollama may route but cannot impersonate them.
- **Cloud models:** optional escalation reviewers for high-burden cases.

## Verification contracts are data, not executable atoms

Atoms remain inert and auditable. A `verification_contract` may declare required checks, competent reviewer classes, staleness triggers, and receipt hashes. The runtime executes it. Atoms contain no executable reviewer code or credentials.

## Failure behavior

- Ollama unavailable: preserve candidate, mark review pending, continue deterministic checks.
- Malformed output: write an error receipt; never coerce to PASS.
- Timeout: `uncertain`, not approval.
- Conflicting reviewers: preserve both and open adjudication.
- Missing context: name it and request the smallest additional packet.
- Hallucinated source: block that assertion until provenance exists.
- AI opposition: may block promotion, but the proposal stays visible and recoverable.
- AI pass: remains awaiting human.

## Intended mature form

The mature layer captures proposals, tracks versioned dependencies, attacks new claims, detects drift, measures blast radius, and prepares canonization agendas. Ollama supplies affordable semantic attention across the long tail. Stronger cloud reviewers and formal systems are invoked only where burden and consequence justify them. Nothing is silently rejected, rewritten, or promoted.

> **Cheap to enter. Deterministic where possible. Adversarial by default. Expensive to promote. Impossible to reject without a reason. Impossible to canonize without a human act.**

## First implementation slice

1. TextGO sends one selected statement to `POST /candidate`.
2. The service assigns identity/hash and writes an immutable fixture candidate.
3. Deterministic validation writes receipts.
4. Ollama runs one bounded adversarial review.
5. A changed dependency opens one conflict or stale-binding agenda item.
6. `GET /agenda` shows receipts and blast radius.
7. A separate authenticated human action promotes or returns the fixture.
8. SQLite is deleted and rebuilt from JSON-LD, events, and receipts.
9. A negative control proves AI PASS cannot reach the promotion writer.

Only then enable filesystem watching, broader roles, and live-canon integration.
