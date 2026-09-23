# FOR KIMI — CANONICAL CONTENT OS BUILD BRIEF

Companion mechanism specification: `OLLAMA_REVIEW_AND_CANON_SESSION_LAYER.md`. The main output of the continuous local-review layer is the next canon-session agenda, not automatic canonization. Ollama is a replaceable semantic reviewer; deterministic checks and human promotion remain separate authorities.

David's intended system is a claim-centered canonicalization workbench, not a folder form and not an AI auto-publisher.

## Popup decision — use TextGO

The desktop front end already exists at `D:\GitHub\TextGO` and https://github.com/YellowKidokc/TextGO. It is a Tauri/Svelte selection-popup tool with hotkey/double-click/drag-selection triggers, interactive toolbar mode, custom icons, and extensible actions. The Canonical Content OS should extend TextGO rather than introduce a second popup application.

Primary interaction: select a sentence, let TextGO display Claim/Evidence/Definition/Math/Story/Bridge actions, and open the selected semantic workbench. A configurable global shortcut opens an empty workbench. A `/claim` typed command is optional and must be explicit; do not create a passive global keylogger or trigger on the ordinary word “claim.”

The current local TextGO worktree contains uncommitted changes, including Sidecar Wizard work. Preserve and integrate with them; never reset or overwrite them.

## The experience David wants

David types `claim`, `evidence`, `math`, `definition`, `story`, or another semantic command. A small GUI opens and searches the live graph before asking him to choose whether he is creating a new item, amending an existing item, creating a new version, superseding an old one, or attaching support. The system remembers his common route and may preselect it, but must show the operation before saving.

The top of every item is one short Truth Capsule. The complete specification expands underneath only as needed for that item's type and burden. A mathematical claim receives formal obligations; a historical claim receives source obligations; a story receives truth bindings to claims and definitions rather than pretending the story is itself proof.

Closing an item stages a candidate revision. Deterministic checks and configured AI reviewers run automatically, sign receipts limited to the checks they performed, and return passes, warnings, exceptions, or blocks. They never silently edit accepted canon or promote a candidate. David/human adjudication remains the final promotion event.

Once accepted, typed dependency edges drive updates:

- generated views rebuild automatically;
- mathematical and definitional replacements are proposed deterministically and verified;
- authored stories are not blind-rewritten—they are marked stale at the bound paragraph/span and offered a revision;
- frozen publications retain their historical text and receive successor/current-state links;
- conflicts, ambiguous identity, invalid schema, or missing provenance go to reversible quarantine.

## Key architectural decisions

1. JSON-LD/Git is canonical source.
2. SQLite is the initial live index and is rebuildable—not a second canon.
3. Event/outbox records every close, review, promotion, propagation, and quarantine action.
4. Claim is the central truth-bearing node; other nodes orbit it.
5. Node type, lifecycle stage, operational state, and epistemic grade remain separate axes.
6. Existing `_icons` remain lifecycle/status icons. Add semantic node-type icons separately.
7. Human-readable IDs use stable prefixes such as `CLM-ME-0001`; version is separate.
8. AI signatures state model/tool version, input hash, policy/prompt hash, checks performed, verdict, and exceptions.
9. Automatic review is default; automatic canon promotion is forbidden.
10. Preserve before quarantine; never silently discard.

## First vertical slice

Build one complete route before generalizing:

```text
type claim
 -> semantic search
 -> new/amend/version/supersede selection
 -> Truth Capsule
 -> stage candidate
 -> deterministic validation
 -> one adversarial AI receipt
 -> human approval
 -> write canonical JSON-LD
 -> update SQLite projection
 -> rebuild HTML pill
 -> show audit receipt
```

Use `CLM-ME-0001` or a fixture, not a live canonical claim, until the full loop passes.

Full design: `_docs/CANONICAL_CONTENT_OS_V0_1.md`.
