# Evidence Coverage Method

Evidence strength is not evidence coverage.

Coverage means how much of a declared claim's content an evidence object
actually bears on. It is not the probability that the claim is true.

Allowed evidence-component relations:

- `establishes`
- `supports`
- `partially_supports`
- `consistent_with`
- `contextualizes`
- `qualifies`
- `contradicts`
- `partially_contradicts`
- `is_silent`

Evidence records live in `_atlas/evidence-coverage.jsonl`. Each row points to a
claim, one evidence object, the components it bears on, relation strength, and
any unaddressed components.

Canonical rule:

**Evidence only propagates over the portion it actually supports.**

This keeps a source from being rendered as `MATCH` or `NO MATCH` when it really
supports only part of the proposition.

## Test Cycles

`TC-001` is the Master Equation canonical document. It stresses technical canon,
explicit proof state, bridge boundaries, and promotion rules.

`TC-002` is Why Grace Has an Equation. It stresses narrative exposition and the
need to prevent rhetorical confidence from becoming evidential standing.
