# Lean 4 Is Not Enough

Lean 4 matters here. It gives one kind of rigor:

- theorem structure
- symbolic dependency
- explicit assumptions
- proof traceability

That is real value.

But Lean 4 does not answer every question this framework needs answered.

It does not, by itself, tell us:

- whether a proposed action is a good comparative model
- whether a bad control fails under the same regime
- whether a source term behaves differently from a sink term in a shared bench
- whether a resistance term acts linearly or nonlinearly in sampled behavior
- whether a prediction was written down before later interpretation

That is why the current verification stack has more than one layer.

## The Verification Stack

### 1. Formal Proof Layer

This is where Lean 4 belongs.

Questions answered here:

- is the theorem internally stated correctly
- do conclusions follow from declared assumptions
- can the proof object be checked mechanically

What this layer does **not** establish by itself:

- that the chosen model is the right model
- that a theological interpretation is historically true
- that a comparison claim beats rival formulations

### 2. Symbolic Translation Layer

This is where the Python harness starts helping.

Questions answered here:

- can the candidate equations be represented cleanly in SymPy
- do the basic derivatives exist and simplify cleanly
- do comparison variants remain formally well-formed

If a model cannot survive this layer, it is not ready for stronger claims.

### 3. Shared-Regime Comparison Layer

This is the fairness layer.

All candidate models are run on the same bench with the same regime settings.

That matters because it removes one common objection:

`you tuned your preferred model differently from the alternatives`

The current lab compares:

- historical LLC v1
- Spirit
- Anti
- canonical LLC v2
- deliberately wrong controls

## What The Current Python Layer Already Shows

### Resistance is load-bearing

Canonical v2 does not treat resistance as a harmless offset.

It gates usable channel contribution through `(1-W)^2`.

Current shared-bench result:

- balanced: `14.48`
- resistance drag: `-4.72`

### There is a computed collapse threshold

Under the current balanced regime, canonical v2 crosses zero at:

`W ~= 0.566987298107781`

That is a real numerical boundary produced by the current form.

### Source and sink are not mirror operations

The current test bench produces:

- source-rich delta: `+3`
- sink-heavy delta: `-5`

That means adding source is not the same thing as merely removing sink.

### Wrong controls fail

This matters a lot.

The current gauntlet rejects:

- `gamma9_added`
- `chi10_subtracted`
- `resistance_ignored`
- `source_sink_swapped`

That means the canonical placement is doing real structural work.

### The harness also catches negative results

The variation audit showed that the bare Spirit form does not automatically
derive every hoped-for entropy relation without extra coupling or a different
choice of varied field.

That is a feature, not a flaw.

A serious verification layer must surface what is **not** yet derived.

## What To Say On The Website

Short version:

Lean 4 checks proof structure.
The Python lab checks model behavior.
Neither one is enough by itself.
Together they form a stronger verification path.

Longer version:

The proof layer verifies what follows from stated assumptions.
The comparison layer verifies whether the chosen equations behave distinctly,
survive shared-regime testing, reject wrong controls, and produce registered
predictions before later interpretation.

That is why this project uses more than one verification method.

## Suggested Site Copy

### Header

Lean 4 and Beyond

### Subhead

Formal proof is one layer of rigor. Comparative symbolic testing is another.
We use both because neither one, alone, is enough.

### Body

Lean 4 verifies theorem structure inside an explicit proof environment.
The Python comparison lab verifies whether candidate equations translate
cleanly, survive shared-regime testing, reject wrong controls, and produce
timestamped predictions before later interpretation.

The goal is not to pretend one tool proves everything.
The goal is to stack independent forms of verification until the weak parts are
visible and the surviving parts are harder to dismiss.

## Next Layer After This

The next step is not louder claims.

It is more comparison:

- trajectory simulations
- benchmark rival models
- empirical side-by-side datasets
- public timestamped prediction updates
