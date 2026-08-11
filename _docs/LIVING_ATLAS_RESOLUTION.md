# Living Atlas Resolution

Canonical rule:

**Retroactive Resolution, Non-Retroactive History**

Later work may change the current standing of an earlier claim, but it may not
alter what the earlier paper historically claimed or knew.

## Storage

Store each accepted relation once in `_atlas/relations.jsonl`.

The renderer computes the inverse view:

| Stored relation | Inverse view |
| --- | --- |
| `supports` | supported by |
| `contradicts` | contradicted by |
| `qualifies` | qualified by |
| `supersedes` | superseded by |
| `resolves` | resolved by |
| `depends_on` / `dependsOn` | required by |
| `extends` | extended by |
| `falsifies` | falsified by |

Unresolved questions live in `_atlas/open-items.jsonl` and keep their own event
history. A paper is a snapshot; the claim graph owns current proof state.

## Rendering

`python _scripts/claim_beacon.py render` adds a Living Atlas Status section to
claim HTML when an atom has paper state, accepted relations, inverse relations,
or open items.

Every rendered claim can show:

- original paper state
- current Atlas state
- forward resolution
- backward resolution
- open item component coverage

Component coverage is deliberately conservative. If later work resolves only
two of three components, the claim renders as `partially_resolved`, not
`resolved`.
