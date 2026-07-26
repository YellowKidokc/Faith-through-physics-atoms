# Adversarial Review Gate

The gate sits between automatic relationship discovery and human acceptance.
It is intentionally asymmetric: an adversarial `oppose` verdict blocks a wire,
while `pass` and `uncertain` remain `awaiting_human`. The tool never edits an
atom and never promotes a proposal to accepted status.

## GUI

```bash
python _scripts/claim_beacon.py propose
python _scripts/adversarial_gui.py
```

Open <http://127.0.0.1:8787>. The GUI shows source and target nodes as a wire,
the deterministic match, the newest review receipt, and its gate state.

## CLI and automation

The offline reviewer is conservative and useful in hooks or scheduled jobs:

```bash
python _scripts/adversarial_review.py
python _scripts/adversarial_review.py --proposal-id cbp-example
```

It blocks explicit falsified/retracted/rejected/contradictory material. When it
cannot prove a contradiction, it reports uncertainty rather than manufacturing
a pass.

Any service exposing an OpenAI-compatible chat-completions API can supply the
adversarial model. This keeps the framework independent of a particular vendor
or orchestration tool (including n8n):

```bash
export ADVERSARY_API_URL=https://provider.example/v1/chat/completions
export ADVERSARY_MODEL=review-model
export ADVERSARY_API_KEY=secret
python _scripts/adversarial_review.py --provider compatible
```

For the GUI, configure only `ADVERSARY_API_KEY` in the server environment; the
endpoint and model are entered in the page. Keys are never returned to or
stored by the browser. n8n can either execute the CLI or POST JSON to
`/api/review` with `proposalID`, `provider`, `endpoint`, and `model`.

Receipts are written to `_proposals/adversarial-reviews.jsonl`, one latest
receipt per proposal. They assess only four categories, enough structure to
make decisions without pretending to encode all philosophy:

1. **Epistemology** — whether evidence bears the claimed confidence.
2. **Ontology** — whether the mapped entities/categories are commensurable.
3. **Logic** — whether direction, scope, and boundaries survive the mapping.
4. **Falsification** — whether kill conditions contradict or defeat the wire.

Operational rule: only a separate, authenticated human workflow may turn a
proposal into an accepted edge. It must refuse any proposal whose latest
receipt has `gateStatus: blocked`.

## Math translation layer

The same GUI includes a translation workspace. Give it a claim ID and,
preferably, a small symbol glossary such as `{"J":"justice","M":"mercy"}`.
It produces three visually and semantically separate layers:

1. The original equation, centered and enlarged.
2. A word-equation that preserves the equation's ordering and operators.
3. Up to three explanations and two explicitly bounded analogies.

Previewing does not write anything. **Save draft node** creates a proposed,
unreviewed `translation` node in the domain's `09_everyday` folder, plus an HTML
fragment. It never changes the source claim or silently treats generated prose
as canonical.

The CLI supports the same workflow:

```bash
python _scripts/math_translation.py --claim-id tp:ME/L5/C1 \
  --glossary '{"J":"justice","M":"mercy","W":"free will"}'
python _scripts/math_translation.py --claim-id tp:ME/L5/C1 \
  --provider compatible --write --html
```

For model generation, configure `MATH_TRANSLATION_API_URL`,
`MATH_TRANSLATION_MODEL`, and `MATH_TRANSLATION_API_KEY`. An n8n HTTP Request
node can POST to `/api/math/translate` with `claimID`, `glossary`, `provider`,
`endpoint`, `model`, and `write`. Keep `write: false` until a preview has been
inspected. The prompt specifically forbids adding theological, causal,
empirical, or uniqueness conclusions that the equation itself does not entail.
