# Broad Lean Corpus Build and Rich Isomorphism Status v0

## Status

Date checked: 2026-07-20

Package:

```text
H:\Desktop 2\LEAN 4\GPT\IN\D_GitHub_Faith_Thru_Physics_Lean_4
```

Toolchain:

```text
leanprover/lean4:v4.31.0
```

Full build command:

```text
lake build
```

Final result:

```text
Build completed successfully (17 jobs).
```

The first full build attempt hit a local Lean standard-library private `.olean` read issue. After targeted module builds populated the cache, the full `lake build` completed successfully.

## Proof-Escape Scan

Source scan:

```text
rg -n "\b(sorry|admit|axiom|unsafe)\b|^(theorem|lemma|def|structure|inductive)\b" -g "*.lean" .
```

The scan did not find active `sorry`, `admit`, `axiom`, or `unsafe` proof escapes in the main source files checked.

Important note: build output includes text like `have this := sorry` from Lean's `#check_failure` diagnostics. These are expected failure checks in `Theophysics_Adversarial.lean`, not active proof holes.

## Build Layers Confirmed Locally

Targeted builds were run and passed:

```text
lake build Theophysics_Core
lake build Theophysics_Adversarial
lake build Theophysics_Coherence Theophysics_Fracture Theophysics_Fall Theophysics_ChiEvaluator Theophysics_NegativeInventory
lake build
```

The final full build passed.

## Rich Isomorphism Status

The broader corpus contains the richer isomorphism/signature layer that the earlier small seed package does not contain.

Confirmed in corpus docs/source:

```text
RichLawIso
richLaw4Iso
no_rich_iso_to_natural_coin
richRelabeledCoinIso
BridgeMatrix / signature discipline
MasterEquationInvariance
wrong-swap rejection rows
```

The core idea:

```text
The first equation-shape isomorphism was too weak.
The upgraded layer requires more than same variables or same two-state shape.
It tests role preservation, transition preservation, signature discipline,
gate behavior, and adversarial wrong-swap failures.
```

## Safe Claim

Safe public wording:

```text
The framework does not rely merely on equation-shape analogy. The broader Lean
corpus includes a richer structural testing layer: signature discipline,
role/transition preservation, gate tests, and adversarial wrong-swap checks.
The intended mappings pass inside the encoded model while selected false
mappings fail.
```

## Boundary

Still do not overclaim:

```text
Lean verifies the encoded structure.
Lean does not independently prove that every human label is domain-faithful.
Physics, theology, history, and source-grounding still carry that burden.
```

## Relationship to the Small Seed Build

Small seed package:

```text
H:\Desktop 2\LEAN 4\GPT\AXIOM_BUNDLE\minimal_no_sorry_package_draft
```

Seed status:

```text
4 front-loaded assumptions
17 no-sorry starter theorems
concrete toy model
continuous-string theorem
build passed
```

Broad corpus package:

```text
H:\Desktop 2\LEAN 4\GPT\IN\D_GitHub_Faith_Thru_Physics_Lean_4
```

Broad status:

```text
full local build passed
rich isomorphism/signature/adversarial layers present
reported corpus docs claim 287 theorems / zero sorry / zero admit
```

These should remain two separate build layers for now:

```text
Seed kernel = clean compressed assumption spine.
Broad corpus = richer formal archive and adversarial proof surface.
```

Do not dump the broad corpus into the seed package until the theorem inventory is normalized and wrapper/trivial rows are separated from substantive theorem rows.
