# Walkthrough: What This Lean 4 Repo Shows

This is the informal walkthrough for family, friends, reviewers, and anyone who wants to understand what is actually sitting inside the Lean 4 code.

The simplest way to say it is this:

This repo does not merely describe a framework. It gives Lean 4 a set of formal definitions and then asks Lean to check whether the claimed structural consequences follow from those definitions.

Lean is not impressed by vibes. Lean does not care who wrote the file, where they went to school, or whether the idea sounds beautiful. If a theorem does not follow, Lean rejects it. If a false statement is intentionally placed in the adversarial file, Lean is expected to reject it.

That is why the project is split into a positive side and an adversarial side.

## The two halves

There are two main jobs happening here.

First, the positive side says: given these definitions, these structures really do follow.

Second, the adversarial side says: given these same definitions, these false positives, shortcuts, swaps, and malformed structures are rejected.

That second part matters. A system that only proves what it likes is too easy to fool. The adversarial file is where we ask, for example:

- Can coercive order count as full coherence?
- Can passive entropy be treated as active evil?
- Can a closed system self-restore without external input?
- Can a random gap count as a structured fracture?
- Can separation alone count as the Fall?
- Can a high-signal claim still be deception if freedom is missing?
- Can modalism, static single-field structure, or arbitrary three-part structure pass the same structural gate as the richer relational form?
- Can eight out of ten be honestly reported as ninety percent?

The answer to those, in the current formal definitions, is no.

## The core product structure

At the center is a multiplicative chi structure:

```text
chi = G * M * E * S * T * K * R * Q * F * C
```

The important formal point is that this is a product, not a sum.

That means a zero channel collapses the product. Lean checks this for the channels. For example, if `Q = 0`, then `chi = 0`. If `G = 0`, then `chi = 0`. The same zero-collapse discipline is repeated across the ten-factor structure.

That is one of the load-bearing ideas: coherence is not treated as a pile of points where enough strong channels can hide one dead channel. A collapsed gate remains collapsed.

## Coupling and irreversibility

The project begins with a small coupling-state model:

```text
C0
C1
```

Lean proves these states are distinct. It also proves the transition is one-way in the model: the system can transition from the first state to the second, but there is no constructor that transitions backward into the original state.

That is a formal skeleton for irreversible structural change.

## Signature discipline

A major source of false positives in symbolic systems is swapping labels while pretending the structure stayed the same.

So the Lean code gives factors signatures. A factor is not only a name. It has a domain, mechanism, and tendency.

This lets the system reject bad swaps. For example:

- Grace and faith cannot simply be treated as the same signature.
- Entropy and grace cannot simply be swapped.
- Compression and communion cannot simply be swapped.

That does not mean Lean has proved the full theological content of those words. It means the formal signatures assigned to those roles are not interchangeable inside this model.

That is the right kind of claim: narrow, deterministic, and checkable.

## Coherence is not mere order

One of the newer files distinguishes full coherence from mere order.

That matters because an oppressive or coercive system can be highly ordered while still failing coherence. Lean checks this distinction.

So the formal system is not saying:

```text
order = good
```

It is saying something more disciplined:

```text
coherence requires the right kind of order, not mere control
```

The adversarial side then rejects the false move where coercive order is treated as full coherence.

## Passive entropy is not active evil

Another important distinction is between passive decay and active discoherence.

The project does not collapse thermodynamic entropy into moral evil. Lean encodes passive entropy as not being the same thing as active, chosen, relational discoherence.

That is one of the most important guardrails in the whole project.

The structure can say decay is a real slope without saying physics itself is morally evil.

## Restoration requires openness, input, cost, and memory

The coherence layer also formalizes restoration.

A system does not self-restore in the closed case. Restoration requires:

- an open boundary,
- external input,
- paid repair cost,
- information or memory preservation.

Lean checks those implications from the restoration model.

This is one of the cleanest bridges between the thermodynamic intuition and the theological language, because it keeps the claim structural. Restoration is not free. Repair is not magic inside the closed system. Something has to enter, pay, preserve, and restore.

## Fracture: not a God-of-the-gaps move

The fracture file distinguishes a random gap from a structured scar.

A random gap is not enough. Local indeterminacy alone is not enough. A real fracture, in this model, requires a structured mismatch: global coherence plus local rupture plus a scar signature.

That gives the project a more disciplined form:

```text
not every mystery counts
not every gap counts
not every unknown counts
```

Only the specifically defined structured fracture passes.

## Fall structure

The Fall file is conservative on purpose.

It does not try to prove every historical, biological, or theological detail. It formalizes a structural spine:

- pre-Fall coherence is not the Fall,
- separation alone is not the Fall,
- coupling without entanglement is not the Fall,
- full Fall activation requires the defined structural conditions,
- sustained post-Fall life requires the grace-floor condition in the model.

That is the right shape for Lean: exact structural gates, not sweeping narrative claims.

## Chi Evaluator

The chi evaluator file is the formal skeleton underneath the claim-evaluation engine.

It defines ten channels:

```text
G, M, E, S_eff, T, K, R, Q, F, C
```

Each channel has positive signal and negative/corrupting signal. The effective score is:

```text
vPos * (100 - vNeg)
```

Then the static chi score is the product of the effective channel scores.

Lean checks that if any effective channel is zero, the full product collapses.

It also checks a high-signal deception pattern. This is important because a claim can look strong in one channel, especially signal or rhetoric, while failing freedom, compression, or time pressure.

So the evaluator is not merely asking:

```text
Does this sound true?
```

It asks:

```text
Does it remain coherent across channels and under pressure?
```

## Fruit and pressure

The evaluator includes pressure-gradient logic. A weak claim that improves under pressure is different from a strong-looking claim that decays under pressure.

It also includes Fruit and anti-Fruit outputs. In this model, a claim's lived output matters. A coercive output can be marked as anti-Fruit-dominant, while a peaceful output can be Fruit-dominant.

Again, Lean is not reading hearts here. It is checking the deterministic structure we gave it.

## Maxwell / Trinity structure controls

This section is easy to misunderstand, so it is worth saying clearly.

The Lean code does not prove the Trinity from Maxwell's equations.

What it does is narrower:

It defines certain structural gates and then rejects specific inadequate substitutes.

For example, the adversarial file rejects:

- vector-only product as lacking the coupling invariant,
- Heaviside-vector-only structure as invalid for the richer gate,
- modalism as invalid for the relational structure,
- static single-field structure as invalid,
- arbitrary three-part systems as invalid,
- relabeled role systems as invalid.

That is a meaningful formal result because it blocks cheap lookalikes. It says, in effect, that not every three-part thing, not every relabeling, and not every flattened model passes the same structural test.

## Justice and mercy controls

The justice/mercy section encodes narrow failure modes.

It rejects cases like:

- offender payment pretending to be mercy,
- an unauthorized or incapable third party,
- coerced third-party payment,
- waived debt pretending justice was satisfied,
- shared cost failing the mercy condition.

That is a formal structure for distinguishing different payment/mercy/justice cases.

## Memory and identity

The memory layer guards against a cheap version of restoration where history simply disappears.

The model requires retained memory/identity structure. It rejects:

- incoherent recorded memory as final retained memory,
- living memory as identical to final identity memory,
- direct discoherent entry into heaven,
- transformed but unrecorded discoherent entry,
- resisting without grace as valid conversion,
- unrecorded negative conversion as preserving identity trace.

The point is not to prove all metaphysics of memory. The point is that within this formal model, restoration does not mean erasure.

## Hit-rate honesty

The hit-rate section is a simple but important honesty gate.

If there are eight hits out of ten closed attempts, the system can claim eighty percent. It cannot claim ninety percent.

It also blocks hidden denominator games, ignored failed attempts, and partial attempts counted as full hits.

That matters because any public-facing framework needs denominator discipline. If the math is going to claim success, the denominator has to be honest.

## Why the adversarial file matters

The adversarial file is not a side issue. It is where the project earns trust.

It shows that the formalism has teeth. It can say no.

It rejects things the project should reject:

- false positives,
- label swaps,
- coercion,
- hidden denominators,
- bad structural analogies,
- malformed restoration claims,
- shallow imitations of richer structures.

That is why this is stronger than a normal essay. The reader can inspect the code and run the build.

## What a successful build means

When `lake build` succeeds, it means Lean accepted the definitions and proofs in this repo under the pinned Lean version.

It means the formal claims in the files type-check.

It means the positive theorems compile.

It means the adversarial file also compiles, including the intentional rejection checks.

## Caveats and scope

These caveats are not apologies. They are boundaries.

Lean verifies formal consequences from definitions. It does not independently verify that the definitions perfectly capture reality.

Lean does not prove Christianity, the Trinity, historical resurrection, moral theology, physics, or metaphysics in their full real-world content.

Lean does prove that, inside this formal structure, certain consequences follow and certain malformed alternatives are rejected.

The Maxwell/Trinity controls do not prove the Trinity. They reject specific inadequate structures such as modalism, arbitrary three-part systems, static single-field flattening, and relabeled-role substitutes.

The thermodynamics/coherence controls do not prove grace as a person. They formalize that restoration, in the model, requires openness, input, cost, and preservation.

The chi evaluator is not a truth oracle. It is a deterministic coherence diagnostic skeleton.

The empirical and historical claims around the larger project still require evidence, interpretation, and public review.

That is the line: the repo verifies the formal structure. The surrounding project argues why that structure matters.
