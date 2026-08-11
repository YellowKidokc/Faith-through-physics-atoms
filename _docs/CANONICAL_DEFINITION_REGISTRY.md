# Canonical Definition Registry and Resolver

The registry is an index, not a giant atom. `_definitions/registry.jsonld`
maps each permanent `tp:def:...` ID to one independently versioned definition
atom. Source/evidence records are separate nodes under `_definitions/evidence`.
The Terminus Sui atom is the first canonical reference implementation, migrated
from PR #8 without changing its human-accepted status; fixture definitions stay
`candidate` until a human explicitly approves promotion.

## Provenance and worldview definitions

Every atom separates `source.sourceStatement` (what the source states) from
`source.frameworkInference` and `frameworkClassification` (what David
Lowe/Theophysics inferred, derived, or classified). In particular, use:

> The proposition was sourced from the Stanford Encyclopedia of Philosophy and
> classified as an axiom by Theophysics after applying its axiom test.

Do not say Stanford classified a proposition as an axiom unless its text does.
A worldview atom may link to independent sources, its governing truth priority,
foundational propositions, separately classified axiom atoms and test receipts,
objections, alternatives, and consequences. Those provenance-preserving links
must retain proposal/accepted status independently.

## Resolve, validate, and render

```bash
python _scripts/definition_resolver.py validate
python _scripts/definition_resolver.py resolve
python _scripts/adversarial_review.py --proposal-id dlp-...
python _scripts/definition_resolver.py render paper.md paper.html
```

The resolver scans Markdown, HTML, and JSON-LD. Exact markers such as
`[[def:terminus-sui]]`, `[[def:goedel-incompleteness]]`, and
`[[def:master-equation/grace]]` produce high-confidence proposals when valid.
Preferred terms and aliases are boundary matched. Ambiguous aliases become
unresolved proposals.

Single-letter variables—including G, M, E, S, T, K, R, Q, F, and C—are never
connected by symbol alone. Their proposals remain unresolved unless a reviewer
can establish namespace, equation position, surrounding terminology, document
domain, explicit marker, or existing claim edges. Explicit markers are the
safest disambiguation.

All output begins as `proposed` or `unresolved`; the resolver never writes an
atom. The adversarial gate may oppose a link but cannot accept it. Human review
is always required, and existing accepted edges are untouched.

When a human-accepted definition link's citation policy has `required: true`
and `inheritToDependents: true`, the renderer emits a linked definition-source
list containing the exact short quotation and attribution. A resolver match by
itself never inherits a citation: the proposal must have `status: accepted`, a
non-empty `acceptedBy` and `acceptedAt` receipt, and a non-blocked adversarial
gate. This satisfies the `quote_or_link` policy without treating the paper as
the source of truth.

Validation rejects duplicate permanent IDs, missing registry atoms, ID/status
mismatches, broken atom edges, required citations lacking a quote or URL,
invalid inheritance, and aliases owned by multiple definitions.
