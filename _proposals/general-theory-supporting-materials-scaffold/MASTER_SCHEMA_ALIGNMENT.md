# Master Schema Alignment

Status: proposal alignment note

This note records how the master invariant, physics atom schema, worldview schema, and physics-numbers bridge rules should govern the General Theory Supporting Materials scaffold before any proposed atom is promoted into a canonical rail.

## Source Files Reviewed

- `MASTER_INVARIANT.md`
- `PHYSICS_ATOM_SCHEMA.md`
- `PHYSICS_NUMBERS_BRIDGE.md`
- `SCHEMA.md`

Duplicate copies were present for `MASTER_INVARIANT.md` and `PHYSICS_NUMBERS_BRIDGE.md`; the duplicate contents matched exactly. Use the non-duplicate names as the working source references unless a later dated file explicitly supersedes them.

## Master Invariant

The governing invariant is:

`NO_SILENT_TRUTH_PROPAGATION`

Nothing becomes true in another rail merely because it is present, validated, useful, elegant, analogous, or theologically attractive in its source rail.

Every promotion or bridge must preserve the separation between:

- claim
- evidence
- inference
- truth status

This means a physics atom can be strong physics without becoming a theological claim. A theological atom can be faithful theology without becoming a physics claim. A mathematics atom can provide structure without proving metaphysical identity.

## Rail Structure

The atom system recognizes six major rails:

- Scripture
- Physics
- Worldview / Philosophy
- History
- Mathematics
- Theophysics

The General Theory scaffold should use these as route labels, not as proof labels. A rail says where a claim belongs for evaluation. It does not certify that the claim is true.

## Lifecycle

The lifecycle states should remain explicit:

- `extracted_not_ratified`
- `ratified`
- `validated`
- `bridged`
- `integrated`
- `disputed`
- `deprecated`

For the current scaffold, new atoms should default to `extracted_not_ratified` unless there is a separate validation receipt. Bridge atoms should not be marked `integrated` merely because their two source atoms are attractive or coherent.

## Physics Atom Chain

The physics schema uses a controlled chain:

1. Physics source
2. Physics claim atom
3. Physics validation record
4. Bridge / correspondence
5. Theophysics claim atom

The important rule is that physics atoms do not point directly into Theophysics as proof. The bridge layer is where comparison, mapping, analogy, dependency, or correspondence is tested.

For the General Theory scaffold, each physical atom should eventually carry:

- source material
- claim text
- domain / regime
- quantities and units
- assumptions
- measurement protocol
- validation status
- failure modes
- relation to equations or invariants

## Worldview Layer

Worldview commitments should be treated as real ledger objects. These are not throwaway opinions; they are constitutive premises, constraints, denials, interpretive commitments, or metaphysical load-bearing assumptions.

The key guardrail is:

Do not eliminate a worldview because it lacks an explicit Theophysics category. Eliminate it only when it constitutively denies something Theophysics requires.

For the scaffold, worldview atoms should identify:

- what the commitment asserts
- what it denies
- what kind of evidence it accepts
- where it constrains interpretation
- whether it is compatible, incompatible, or underdetermined relative to Theophysics

## Physics-Numbers Bridge Rules

The bridge schema requires a two-hop path:

1. Physics claim -> mathematical structure
2. Mathematical structure -> Numbers-in-God property

The God-side grounding is a separate bridge. The bridge should not skip from physics directly to God by rhetoric, resonance, or verbal similarity.

Each physics-numbers bridge must preserve:

- the reality / representation distinction
- shared predicate precision
- rival explanations
- negative controls
- kill conditions
- separated evidence status
- separated truth status

## Bridge Grades

Bridge candidates should be graded rather than flattened:

- `formal_structural`
- `operational`
- `dependency`
- `convergence`
- `verbal`

`verbal` bridges are rejected as bridges. They may be retained only as weak prompts for future analysis.

## Initial Bridge Predicate Families

The bridge schema identifies eight initial bridge candidates:

- invariant
- generative
- order-giving / constraint
- foundational / mathematical dependency
- intelligible
- objective
- unified / compression
- rational / rule-governed derivability

It also marks evaluation / judging as an experimental ninth candidate, not yet promoted.

## High-Risk Bridge Terms

The bridge schema warns against leading with these terms in physics-to-God claims:

- necessary
- eternal
- immutable
- self-existent
- infinite
- perfect
- immaterial
- non-local
- transcendent

These may be theologically meaningful, but they are high-risk bridge labels because physics usually does not establish them directly. In this scaffold they should require stronger bridge records, rival explanations, and explicit scope limits.

## Consequences For The Current Scaffold

The existing `general_theory_atoms.v0.1.json` file should be treated as a draft vocabulary scaffold, not as canonical atom ingestion.

Before promotion, each atom should be normalized into the repo-compatible shape:

- keep physical, spiritual, mathematical, worldview, and bridge atoms as separate objects
- add `claim`, `evidence`, `inference`, and `truth_status` fields
- add lifecycle status
- add rail
- add source receipts
- add explicit failure / kill conditions
- add `reality_or_representation` for any physics-numbers bridge
- add bridge grade for bridge atoms
- separate God-grounding bridge from physics-numbers bridge
- preserve original draft payload as source data

## Recommended Import Posture

The import route should be:

1. Load exports as source artifacts.
2. Normalize their atom type and rail.
3. Preserve original data without treating it as canonical truth.
4. Attach receipts to each candidate atom.
5. Apply master invariant checks.
6. Validate schema shape.
7. Write into a draft/proposal area first.
8. Promote only after explicit review.

This gives the project the breadth David wants while keeping the evidential accounting clean enough that later critics cannot honestly say the framework is merely sliding between physics, mathematics, and theology without declaring where the claim changed rails.
