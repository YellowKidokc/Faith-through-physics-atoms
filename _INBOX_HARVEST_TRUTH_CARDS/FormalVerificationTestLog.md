# Formal Verification Test Log

This log records Lean verification runs, adversarial tests, mistakes, and
boundary discoveries. The goal is not to make the work look clean after the
fact; the goal is to preserve the actual path by which the formal claims were
tested, weakened, strengthened, or rejected.

## 2026-05-10 - LawIso / Law 4 Adversarial Pass

### Context

The active question was whether the `LawIso` structure in
`ResurrectionFormal.IsomorphismTest` could support a Law 4 bridge:

- physical side: strong-force confinement/freedom
- theological side: love/agape captivity/liberation

The first version modeled both sides as two-state systems with:

- a zero/one value function
- a collapsed predicate
- a bidirectional map
- value preservation
- collapse preservation

### Positive Result

`law4Iso` compiles.

This proves that the chosen two-state abstractions are isomorphic under the
current `LawIso` definition.

### Adversarial Result

Several targeted wrong candidates fail under the current definition:

- a faith candidate with an extra state fails the right-inverse test
- an electromagnetism candidate with an extra state fails the right-inverse test
- an inverted strong-force/love mapping fails value preservation
- a misaligned collapse predicate fails the `collapsed_value_zero` requirement

### Mistake / Boundary Discovery

The initial interpretation was too strong.

It was tempting to say that `law4Iso` verified the strong-force/love bridge.
That overclaims what the current Lean structure proves.

An adversarial false-positive test was added:

- `CoinState.tails`
- `CoinState.heads`
- same zero/one value pattern
- same collapse pattern

Lean accepted `strongForceCoinIso`.

That means the current `LawIso` definition also admits an unrelated binary
zero/one system. This is not a Lean failure. It is a specification-boundary
finding: the definition is too thin to distinguish a meaningful Law 4 bridge
from any unrelated binary system with the same collapse/value pattern.

### Corrected Claim

Current verified claim:

> The selected binary collapse/freedom abstractions are isomorphic under the
> current `LawIso` definition.

Current rejected / not-yet-supported claim:

> Lean has verified that the strong force and love are structurally isomorphic
> in a domain-rich sense.

### Verification Commands

The project was checked with:

```text
lake build
lake env lean IsomorphismTest.lean
```

The active Lean module path was also scanned for proof escape hatches:

```text
sorry
admit
axiom
unsafe
```

No active proof escape hatches were found in the active Lean module path after
the test.

### Next Required Strengthening

The next formal layer should strengthen the bridge beyond binary value/collapse
matching. Candidate preserved structure:

- transition/regime behavior
- operation roles
- directionality
- domain-specific invariants
- richer state data
- explicit bridge tier classification

Until that strengthening exists, `LawIso` should be described as a minimal
abstraction test, not as a full domain-rich proof.

## 2026-05-10 - RichLawIso / Role and Transition Strengthening

### Context

After the coin false positive, the next test was whether adding more preserved
structure could make the bridge more discriminating.

A stronger `RichLawModel` / `RichLawIso` layer was added with:

- value preservation
- collapse preservation
- regime-role preservation
- forward transition preservation
- reverse transition reflection

A generic `richLawIsoRefl` theorem was also added. It proves that any
`RichLawModel` is isomorphic to itself. This is mathematically expected, but it
also documents the semantic boundary: copied or relabeled structure will pass if
the formal fields are the same.

The added regime roles were:

- `constraining`
- `liberating`
- `randomLow`
- `randomHigh`

### Positive Result

`richLaw4Iso` compiles.

This proves that the enriched strong-force/love abstractions preserve:

- zero/one value
- collapse predicate
- constraining/liberating role
- release-style transition from collapsed/constraining to free/liberating

### Adversarial Result: Natural Coin Blocked

The natural coin model assigns:

- tails -> `randomLow`
- heads -> `randomHigh`

Lean proves `no_rich_iso_to_natural_coin`.

This means the strengthened specification blocks the earlier natural coin false
positive. A merely binary system no longer passes if its roles are encoded as
random rather than constraining/liberating.

### Deeper Boundary Discovery: Relabeled Coin Still Passes

A second coin model was deliberately relabeled:

- tails -> `constraining`
- heads -> `liberating`

Lean accepts `richRelabeledCoinIso`.

This is the deeper specification boundary. Once a human assigns the same
semantic roles and transition shape to the coin model, Lean can verify
preservation of those encoded structures. Lean cannot independently certify
that the labels are faithful to the domain.

The generic `richLawIsoRefl` result confirms the same lesson in abstract form:
formal isomorphism is about preserved structure, not about whether a structure's
human-readable interpretation is warranted.

### Corrected Claim

Current verified claim:

> Under the enriched role/transition abstraction, the strong-force/love models
> are isomorphic, and the natural coin false positive is rejected.

Current not-yet-supported claim:

> Lean has independently verified that the role labels themselves are faithful
> readings of strong-force physics or theological love.

### What Worked

- Minimal `LawIso` found the binary abstraction match.
- Minimal adversarial tests rejected wrong cardinality and wrong mapping cases.
- The coin false positive exposed the first overclaim.
- `RichLawIso` strengthened the test with roles and transitions.
- `RichLawIso` rejected the natural coin model.

### What Did Not Work / Where We Overstated

- The minimal `LawIso` did not distinguish Law 4 from any binary zero/one
  collapse system.
- The enriched `RichLawIso` still depends on human-assigned semantic roles.
- A relabeled coin can pass if given the same role and transition structure.
- Therefore Lean currently verifies preservation of an encoded abstraction, not
  the truth of the domain interpretation.

### Current Boundary

The formal boundary is now clear:

> Lean can verify that a proposed bridge preserves explicitly encoded structure.
> Lean cannot, by itself, verify that the encoded structure is the correct
> scientific or theological interpretation of the source domains.

The next layer must therefore add either:

- richer domain-specific invariants that are harder to relabel trivially, or
- an external audit layer documenting why each encoded role is justified by
  physics/theology sources.

Likely next invariants:

- multi-regime behavior
- non-symmetric interaction structure
- domain-specific operation names
- functional constraints such as monotonicity/antitonicity
- evidence links from prose/source claims to formal fields

### Verification Commands

The project was checked with:

```text
lake build
lake env lean IsomorphismTest.lean
```

The active Lean module path was scanned for:

```text
sorry
admit
axiom
unsafe
```

No active proof escape hatches were found.

## 2026-05-10 - All-Factor Bridge Matrix / Full Equation Pass

### Context

The Law 4 test was generalized across the ten-factor bridge table from
Layer 1 and Layer 2.

The new `ResurrectionFormal.BridgeMatrix` module encodes:

- all ten formal factor slots: `G M E S T K R Q F C`
- their formal signatures
- their physical readings
- their spiritual readings
- canonical physical/spiritual bridge rows
- semantic-swap adversarial rows
- full ten-factor product values

### Positive Result

`canonicalRows_all_valid` compiles.

This proves that the encoded canonical bridge table is internally consistent:
each physical reading and spiritual reading has the same encoded signature as
the formal factor slot it is assigned to.

The full ten-factor product tests also compile:

- each slot collapses the product when set to zero
- `R = 0` collapses the product
- `Q = 1` is not sufficient if another required factor is zero
- all ten factors set to `1` gives product output `1`

### Adversarial Semantic-Swap Results

The following wrong substitutions are rejected by Lean under the encoded
signature table:

- `G` / grace swapped with faith-commitment
- `S` / entropy swapped with grace
- `K` / compression swapped with communion
- `C` / coherence swapped with consequence-lock
- `G` paired with the wrong physical reading, entanglement

These tests show that the bridge matrix is not accepting arbitrary declared
swaps once the signatures are fixed.

### Boundary Discovery: Unvetted Clones Still Pass

The module also includes an explicit unvetted-clone boundary:

- `arbitraryGraceClone` is assigned the same signature as `G`
- Lean accepts that it matches `G`
- `arbitraryFaithClone` is assigned the `Q` signature
- Lean rejects that it matches `G`

This is the same semantic-grounding boundary found in the Law 4 test. Lean can
reject swaps when their encoded signatures differ. Lean cannot determine whether
an externally supplied term deserves the signature a human assigned to it.

### Corrected Claim

Current verified claim:

> The encoded ten-row bridge matrix is internally consistent, rejects several
> targeted semantic swaps, and preserves the full ten-factor zero-collapse
> product behavior.

Current not-yet-supported claim:

> Lean has independently verified that every physical and theological reading
> is the correct domain interpretation of its assigned formal factor.

### What Worked

- The ten canonical rows pass as a complete encoded bridge matrix.
- Several semantic games fail when they change the encoded signature.
- The full equation product behaves as expected across all ten factor slots.
- `Q` nonzero is explicitly shown not to be sufficient by itself.

### What Did Not Work / Where We Overstated

- The bridge matrix verifies internal consistency, not external truth.
- The signatures are currently coarse. They distinguish major mechanism classes
  but do not yet encode detailed equations such as Shannon capacity,
  Kolmogorov complexity, action integrals, or quantum amplitudes.
- A human can still create a relabeled clone and assign it the desired
  signature. Lean will verify the assignment, not the honesty of the assignment.
- Therefore the project still needs a source-grounding layer from prose,
  citations, or detailed equations into each formal signature field.

### Current Boundary

The broad test answers the next question:

> Under the current signature table, all ten bridges are internally coherent and
> multiple wrong swaps are rejected. The remaining open burden is whether the
> signature table itself is domain-faithful.

### Verification Commands

The project was checked with:

```text
lake build
```

The module compiled as part of the project target.
