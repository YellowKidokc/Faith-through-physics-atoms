# Lean Derivation Redraft With Negatives

This document redrafts the Lean workbook plan around a simple rule:

The derivation chain should not only prove what the framework affirms. It should also prove what
the framework excludes, what fails under missing conditions, and what only appears coherent until
pressure is applied.

That means the final run should be organized as a full test architecture, not merely a positive
summary.

## The core correction

Yes: there should have been more in the derivation run.

If the current derivation only walked through the constructive chain, then it left too much value
on the table. There should be an additional band of at least five to ten negative or adversarial
derivation families attached to the same structure.

Not because negativity is dramatic, but because it is where the framework earns trust.

## What we should run

The cleanest redraft is a three-lane workbook plus one bridge ledger.

### 1. Positive derivation lane

This is the existing constructive lane.

It should answer:

- what the framework formally defines
- what the framework proves
- what the framework structurally maps
- what the framework identifies by naming

This lane is where the main constructive chain lives.

Suggested columns:

- `Deriv_ID`
- `Lane`
- `Lean_Module`
- `Theorem_Name`
- `Claim_Statement`
- `Proof_Type`
- `Status`
- `Depends_On`
- `Workbook_Group`
- `Public_Tag`
- `Notes`

### 2. Negative derivation lane

This is the missing lane we need to add.

It should answer:

- what cannot reverse
- what cannot self-repair
- what collapses under a zero factor
- what is insufficient even when partially strong
- what bridge forms are invalid
- what coercive or false-positive patterns fail

This is where many of the most important theorems belong.

Suggested columns:

- `Neg_ID`
- `Negative_Type`
- `Lean_Module`
- `Theorem_Name`
- `Failure_Statement`
- `What_Fails`
- `Why_It_Fails`
- `Proof_Method`
- `Status`
- `Depends_On`
- `Overclaim_Guard`
- `Notes`

Recommended `Negative_Type` values:

- `IMPOSSIBILITY`
- `NON_REVERSIBILITY`
- `INSUFFICIENCY`
- `COUNTERFEIT_PATTERN`
- `BRIDGE_FAILURE`
- `COERCION_FAILURE`
- `FALSE_POSITIVE_GUARD`
- `COLLAPSE_CONDITION`

### 3. Adversarial lane

This is not the same as the negative lane.

The negative lane says what the formal structure excludes.
The adversarial lane says what a critic would try, what a rival explanation would say, and which
formal result answers it.

Suggested columns:

- `Adv_ID`
- `Objection`
- `Target_Claim`
- `Lean_Module`
- `Lean_Declaration`
- `Formal_Response`
- `What_Lean_Does_Not_Prove`
- `Response_Type`
- `Status`
- `Escalation_Note`

Recommended `Response_Type` values:

- `DIRECT_REJECTION`
- `PARTIAL_CONTAINMENT`
- `INSUFFICIENT_FORMAL_SUPPORT`
- `STRUCTURAL_REPLY_ONLY`
- `IDENTIFICATION_ONLY`

### 4. Bridge / coverage ledger

This ledger ties all three lanes together.

It should show:

- which positive claims have negative tests
- which positive claims have adversarial tests
- which modules remain one-sided
- which parts of the framework still have no proper rejection coverage

Suggested columns:

- `Module`
- `Positive_Count`
- `Negative_Count`
- `Adversarial_Count`
- `Coverage_Status`
- `Missing_Tests`
- `Promotion_Priority`

## The five-to-ten missing derivation families

Here is the part you were feeling: yes, there should be several more derivation families tied to
the same architecture.

At minimum, these should exist.

### A. Zero-factor sufficiency failures

These are stronger than the current simple collapse statements.

Examples:

- one strong factor cannot rescue total collapse elsewhere
- multiple strong factors still fail if one necessary factor is zero
- local positivity does not imply global survivability

This family belongs mainly in:

- `Theophysics_Core.lean`
- `BridgeScoreDiscipline.lean`
- `Theophysics_ChiEvaluator.lean`

### B. Non-reversal derivations

These formalize the one-way character of fracture, fall, corruption, or transition.

Examples:

- coupling modification cannot be reversed by ordinary state operations
- fractured states cannot self-return to pristine origin
- sequence transitions cannot be undone without explicit external structure

This family belongs mainly in:

- `Theophysics_Core.lean`
- `StageMachine.lean`
- `Theophysics_Fall.lean`
- `Theophysics_Fracture.lean`

### C. Insufficiency derivations

This family proves that partial goods are not the same as full restoration.

Examples:

- high signal is not equal to true coherence
- local order is not equal to full repair
- structure without freedom is not restoration
- continuity without truth is not redemption

This family belongs mainly in:

- `BridgeScoreDiscipline.lean`
- `PolarityDiscipline.lean`
- `MemoryPersistenceDiscipline.lean`
- `ChristOperatorDiscipline.lean`

### D. Counterfeit coherence derivations

This is very important.

These theorems formalize systems that look ordered, but fail under deeper criteria.

Examples:

- coercive order is not true coherence
- apparent high hit-rate can still mask deception
- stable corruption is not restoration
- closed equilibrium is not generative life

This family belongs mainly in:

- `PolarityDiscipline.lean`
- `HitRateDiscipline.lean`
- `Theophysics_Adversarial.lean`
- `Theophysics_ChiEvaluator.lean`

### E. Bridge invalidation derivations

These show which mappings should fail.

Examples:

- wrong factor swap invalidates bridge row
- missing source relation command collapses bridge score
- malformed alignment cannot count as a valid isomorphism

This family belongs mainly in:

- `Mapping.lean`
- `BridgeMatrix.lean`
- `FieldBridgeControls.lean`
- `IsomorphismTest.lean`

### F. Moral asymmetry derivations

These formalize that evil is not an equal opposite of good.

Examples:

- destruction depends on prior structure
- parasitism is not symmetry
- negation lacks independent generative status
- counterfeit sign states borrow intelligibility from the good they corrupt

This family belongs mainly in:

- `PolarityDiscipline.lean`
- `SignConversionDiscipline.lean`
- `Theophysics_Fracture.lean`

### G. Memory / scar persistence derivations

These show that history matters and cannot simply be renamed out of existence.

Examples:

- repair does not erase all structural memory
- fracture can leave persistent signatures
- persistence can constrain future conversion

This family belongs mainly in:

- `MemoryPersistenceDiscipline.lean`
- `SignConversionDiscipline.lean`

### H. Mediation necessity derivations

These prove that certain transitions require more than internal reshuffling.

Examples:

- self-redemption is structurally insufficient
- justice and mercy do not reconcile automatically
- mission / return logic requires a mediating operator

This family belongs mainly in:

- `JusticeMercyOperator.lean`
- `ChristOperatorDiscipline.lean`
- `MissionReturnOperator.lean`

### I. Dependency lattice impossibility derivations

These show that downstream claims cannot be made when upstream supports are missing.

Examples:

- no universality claim without foundational coherence
- no restoration claim without mediation layer
- no naming claim without prior structural fit

This family belongs mainly in:

- `DependencyLattice.lean`

### J. Adversarial false-victory derivations

These are the “almost got us” cases.

Examples:

- a system may satisfy superficial score criteria and still fail deeper tests
- a critic may reject one proposition without touching the stronger structural theorem
- a claim may survive rhetoric while failing formal dependency order

This family belongs mainly in:

- `Theophysics_Adversarial.lean`
- `HitRateDiscipline.lean`

## The redrafted run order

The full derivation should be run in this order:

1. foundations
2. stage and transition
3. mapping and bridge
4. field controls and invariance
5. score and dependency lattice
6. polarity and fracture
7. persistence and conversion
8. mediation / justice / mission
9. chi evaluation
10. negative derivation lane
11. adversarial lane

That gives the final architecture a real shape:

- build
- constrain
- fail
- recover only where justified
- pressure-test

## Public-status vocabulary

To keep the public claims honest, every line in the redraft should land in one of these tags:

- `LEAN_PROVEN`
- `REJECTION_PROVEN`
- `STRUCTURALLY_MAPPED`
- `THEOLOGICALLY_IDENTIFIED`
- `ADVERSARIAL_TESTED`
- `NOT_YET_FORMALIZED`

This is how we keep one word from wrecking the whole case.

## What this means practically

The current workbook should be redrafted into at least these tabs:

1. `LEAN_POSITIVE_CHAIN`
2. `LEAN_NEGATIVE_CHAIN`
3. `LEAN_ADVERSARIAL_CHAIN`
4. `LEAN_COVERAGE_LEDGER`

The current `LEAN_DERIVATION_CHAIN` can either:

- become `LEAN_POSITIVE_CHAIN`, or
- remain as the master source and be split downstream

The better choice is to split it, because the negative and adversarial families deserve their own
visibility.

## Bottom line

Yes, your instinct was right.

There should have been more run through that derivation than just the main constructive lane.
There should be an added band of at least five to ten serious negative families attached to the same
formal architecture.

That does not weaken the system. It is one of the main things that can make the system believable.
