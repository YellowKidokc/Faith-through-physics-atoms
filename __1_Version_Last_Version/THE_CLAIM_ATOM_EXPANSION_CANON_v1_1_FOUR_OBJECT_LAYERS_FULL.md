# THE CLAIM ATOM EXPANSION CANON v1.1 — FOUR-OBJECT FULL EDITION
## The four object layers, their full anatomies, the edges between them, and the grammar they generate
## Expanded 2026-08-25 from v0.1, the v0.2 approval draft, and the v1.0 full expansion
## Repository home: `Faith-through-physics-atoms`

---

## DOCUMENT STATUS AND AUTHORITY

This document fully expands **THE CLAIM ATOM EXPANSION CANON v0.2 — APPROVAL DRAFT** while retaining the register anatomies and implementation detail developed in the v1.0 full expansion. It does not replace the Unified Grammar Methodology. It sits underneath that methodology and specifies what happens when a claim, evidence record, proof, or process enters the pipeline, opens into components, connects to other atoms, receives correction, or becomes part of the admitted graph.

This is a methodological canon, not a mass admission ruling. Its presence in the final-version directory does not retroactively upgrade every record already present in the repository. Existing records retain their identifiers, grades, proof labels, histories, and unresolved fields until a human-approved migration or ruling says otherwise.

The repository currently contains more than one record generation and more than one grading vocabulary. Therefore:

- `A###/L#/C#` is the canonical address form defined by the claim-atom standard and exemplified by `A042/L9/C1–C3`; it must not be falsely imputed to legacy records that have not been migrated.
- IC-0 through IC-5 grades the strength of a proposed cross-register structural correspondence.
- Native C0 through C6 and Atlas `- / C / B / B+ / A` grades belong to a separate evidence-grade projection.
- `structural_identity`, `structural_isomorphism`, `structural_analogy`, `metaphorical`, and `independent` are bridge-grade terms.
- These scales may be cross-referenced by an explicit registry, but they are not interchangeable merely because their labels look similar.

When this document says **must**, it states a canon requirement for a conforming new or migrated record. When it says **may**, it identifies an allowed extension. When it says **currently**, it describes repository state and must be rechecked before being treated as permanent.

---

# PART I — WHY THE ATOM EXISTS

## 1. THE PROBLEM THE ATOM SOLVES

A corpus can contain ten thousand pages and still fail to tell us what has actually been established. A paragraph may contain a definition, an empirical statement, a theological confession, a mathematical consequence, and a bridge between them. If the paragraph is graded as one object, the strongest sentence can hide the weakest, the weakest can unfairly discredit the strongest, and a formal proof of one component can be reported as proof of the whole bundle.

The claim atom prevents that collapse.

An atom is the smallest corpus object that can receive one epistemic ruling without forcing that ruling onto a different assertion. It is not necessarily the shortest grammatical sentence. It is the smallest assertion whose truth conditions, dependencies, evidence, failure conditions, and status can be tracked as one unit.

The atom does four things at once:

1. It preserves exactly what was claimed.
2. It exposes what the claim depends on.
3. It separates what supports the claim from what merely resembles it.
4. It allows failure to propagate only where the dependency graph licenses propagation.

The goal is not to make the corpus small. The goal is to make every load-bearing move visible.

## 2. THE ATOM DEFINED

**One atom = one assertion, one immutable identity, one versioned state, one independently assignable grade.**

An atom may have many sources, many evidential items, many dependencies, many countermodels, and many rendered views. It still contains only one proposition at the level being graded.

An atom is not:

- a whole paper merely renamed as a claim;
- a paragraph whose conjuncts can fail independently;
- an equation without a statement of what the equation is claimed to mean;
- a quotation treated as though quotation proves the quoted content;
- a label such as `theorem`, `physics`, or `Christian` used in place of a truth condition;
- an HTML page treated as a second source of truth;
- an automated score treated as a human admission ruling.

## 3. THE ADDRESS

The canonical claim-component address is:

```text
claims / A042 / L9 / C1
         atom   layer  component
```

### 3.1 Atom identity — `A###`

The atom identifier names the enduring claim family. It is immutable, never reused, and never silently deleted. If the wording changes materially, the old form remains recoverable and the relationship between versions is recorded.

The identifier does not certify truth. `A042` means “this tracked claim family,” not “claim 42 has been admitted.”

### 3.2 Layer — `L#`

The layer states where the claim operates in the dependency stack: what must already be available for the claim to be meaningful, and what new capability the claim adds if granted.

The repository’s vertical vocabulary distinguishes generative, constraint, and expression layers. Current named layers include God, Trinity, Logos/generative kernel, creative decree/boundary conditions, constraint meta-laws, Master Equation/Ten Laws, domains, and claim atoms. A numeric `L#` in an address must resolve through a versioned layer registry. It must not acquire meaning from the number alone.

A layer assignment is not a truth grade. It answers **where does this claim operate?**, not **how well is it supported?**

### 3.3 Component — `C#`

The component identifies one independently gradable assertion extracted from a bundle. If a sentence contains three claims that can fail separately, it opens as C1, C2, and C3. Shared prose may remain in a parent record, but no child inherits another child’s proof status merely by proximity.

For example, a bundled statement may contain:

```text
C1 — a formal conditional
C2 — a proposed physical or moral interpretation of that conditional
C3 — a theological identification of the proposed mechanism
```

A proof of C1 does not prove C2. Support for C2 does not establish C3. The address makes that non-transfer visible.

### 3.4 Child addresses created by expansion

When C1 opens into its native anatomy, its children require stable identities. A conforming implementation may use path segments or typed edge records, but it must preserve all of the following:

```text
parent claim ID
child claim ID
child role in the expansion
ordinal where order matters
source span or derivation origin
content hash
version
```

The visible path may be rendered as, for example:

```text
A042/L9/C1/MEASUREMENT/UNITS
A042/L9/C1/FORMAL/LEMMA-02
A042/L9/C1/BRIDGE/LOST-STRUCTURE
```

These examples are naming guidance, not permission to manufacture addresses outside the active resolver. The resolver maps valid identifiers; it does not create authority.

## 4. DUAL FORMAT, ONE SOURCE

Every conforming component may be projected as:

- `.jsonld` for machine-readable identity, typed relations, validation, and graph use;
- `.html` for human reading, challenge, correction, and public display;
- optional Markdown, tables, cards, diagrams, or API responses for additional views.

All projections are generated deterministically from the same canonical object. The JSON-LD is not true because it is JSON-LD, and the HTML is not authoritative because it is easier to read. Authority belongs to the ruled canonical object and its ledgered version.

A projection must show or link:

- the canonical ID and version;
- the exact claim;
- its register and classification;
- lifecycle and admission state;
- proof or evidence status;
- dependencies;
- countermodels and kill conditions;
- correction history;
- what has and has not been established.

Hand-editing a generated projection creates drift and is prohibited. Correct the canonical object, record the correction, and regenerate the views.

---

# PART II — THE FOUR OBJECT LAYERS

## 5. THE OBJECT-TYPE LAW

Every canonical atom has exactly one primary object type:

| Object type | Function | Governing question |
|---|---|---|
| **CLAIM** | Asserts a proposition | What is being said? |
| **EVIDENCE** | Bears on one or more propositions | What speaks for, against, or between alternatives? |
| **PROOF** | Establishes an exact conclusion under premises | What is derived, by which rules, from what? |
| **PROCESS** | Performs a versioned operation | What procedure generates, transforms, audits, or tests? |

This is an exclusive primary-type rule, not a denial that records can contain sentences. An evidence atom may include a discrimination statement; that does not turn the evidence object into a claim object. A proof atom has a conclusion; that does not make the proof and the conclusion the same object. A process atom states its purpose and outputs; those statements describe the process rather than replacing it with a claim.

When content performs more than one primary function, it must be decomposed. A paper paragraph that reports data, draws an inference, and proposes an interpretation becomes at least one evidence atom, one claim atom, and—if a derivation is asserted—one proof atom, connected by typed edges.

### 5.1 CLAIM — assertion

A claim atom stores one independently gradable proposition. It carries the raw statement, normalized technical and plain forms, exact negations, scope, quantifiers, boundaries, source location, and identity conditions. Its native anatomy is selected by the burden of its register and is expanded in Part IV.

### 5.2 EVIDENCE — discrimination

An evidence atom stores a preserved record whose function is to discriminate among claims or hypotheses. It is not “a claim that supports.” Its authority comes neither from being called evidence nor from having a hash. Its bearing is expressed only through typed evidence edges, each with a discrimination statement and independence assessment.

### 5.3 PROOF — establishment under premises

A proof atom stores an inspectable derivation object: premises, licensed steps, exact conclusion, assumptions, receipt, and interpretation boundary. The proof and the conclusion claim are distinct atoms joined by `proves`; premises are claim atoms joined by `derivedFrom`.

### 5.4 PROCESS — runnable operation

A process atom stores a versioned protocol, gate, grammar, transformation, audit, or pipeline whose function is to do something. It names inputs, steps, outputs, discriminating power, failure modes, and version. A description of a procedure is not evidence that it was run; each execution requires its own receipt or run record.

### 5.5 What is not an object layer

Everything below is an axis, state, subtype, edge, terminus, or record relation rather than a fifth primary object type:

- lifecycle: candidate, admitted, withdrawn, rejected, quarantined, superseded;
- proof class: D, S, L, M, H, E, BR, T, C, PM, PH and applicable receipt classes;
- register: formal, empirical, historical, theological, bridge, and others;
- IC grade and bridge grade;
- WHY-closure outcome;
- `OPEN`, `PRIMITIVE`, and `INDEPENDENT_EMPIRICAL_INPUT` termini;
- correction, which is a first-class governance record operating on atoms without becoming a fifth epistemic object layer.

Axes remain independent. An admitted evidence atom can still have low discriminating power. A `BUILT_ZERO_SORRY` proof can prove a narrow model theorem while its physical interpretation remains open. A process can be canonically admitted as the approved method while no particular run has yet been executed.

## 6. THE FIVE INDEPENDENT AXES

No single status field is allowed to carry all meanings. Every atom records at least five independent axes.

### 6.1 Lifecycle state — where the object is in the process

Typical states include:

```text
RAW → PRESERVED → DECOMPOSED → OPENED → TESTED → CANDIDATE
→ HUMAN_REVIEW → ADMITTED | RETURNED | WITHDRAWN | FALSIFIED
→ SUPERSEDED | DEPRECATED
```

The exact controlled vocabulary belongs to the active schema. Lifecycle does not state truth. An admitted theological confession and an admitted empirical result can share lifecycle state while carrying different warrant classes.

### 6.2 Proof class — what kind of warrant the claim has

At minimum the record must distinguish:

```text
NOT_ATTEMPTED
SPECIFICATION_ONLY
INFORMAL_ARGUMENT
FORMALIZED_NOT_BUILT
BUILT_WITH_ASSUMPTIONS
BUILT_WITH_SORRY
BUILT_ZERO_SORRY
COUNTERMODEL_FOUND
FALSIFIED
```

Repositories may retain more granular legacy labels. No projection may collapse `SPECIFICATION_ONLY` into `THEOREM`, or `BUILT_ZERO_SORRY` into a real-world validation claim.

### 6.3 Register — what kind of assertion is being made

Registers include, but are not limited to:

```text
FORMAL / MATHEMATICAL
EMPIRICAL / PHYSICAL
HISTORICAL
INFORMATIONAL
CONSCIOUSNESS / FIRST-PERSON
MORAL / NORMATIVE
THEOLOGICAL / CONFESSIONAL
BRIDGE / CROSS-REGISTER
INTERPRETIVE
PREDICTIVE
PROTOCOL
```

Registers can interact without becoming identical. A mathematical theorem can constrain a physical model; a physical observation can motivate a theological interpretation; a theological confession can supply a root-conditioned reading. None inherits the warrant native to the other.

### 6.4 IC grade — how much structure a correspondence preserves

IC grades apply to isomorphism candidates and structural convergence claims:

```text
IC-0 — vocabulary proximity only; no demonstrated structural mapping.
IC-1 — one or more local feature correspondences; relations largely unspecified.
IC-2 — multiple explicit relations map, but dependencies or operations are incomplete.
IC-3 — substantial relational and operational correspondence with stated boundaries;
       rival mappings or collapse behavior remain insufficiently discriminated.
IC-4 — shared dependency graph and capability classes are demonstrated under an
       explicit mapping; preserved and lost structure are named; serious candidate.
IC-5 — IC-4 plus matched collapse behavior and translation behavior, with the
       preferred mapping surviving label removal, permutation, rivals, and controls.
```

These are operational definitions for this canon. IC-4 and IC-5 support a serious structural-convergence claim. Neither, by itself, proves that the compared domains are ontologically identical or that a theological identification is true.

### 6.5 WHY-closure outcome — whether the correspondence is explained

Every serious correspondence receives one of:

```text
WHY_CLOSED — an explanation passes the applicable why-ladder levels and the
             non-restatement test; the closure level and explanation type are named.
WHY_FAILED — the offered explanation collapses, restates the correspondence, conflicts
             with evidence, or loses to a stronger rival.
WHY_OPEN   — the correspondence may be real, but its reason is underdetermined;
             rivals and the next discriminating test are retained.
```

`WHY_OPEN` is not a polite synonym for success or failure. It is a positive record of unresolved explanatory structure.

## 7. THE MINIMAL UNIFIED ATOM RECORD

A full record should be capable of expressing the following envelope. Concrete field names may be adapted only through a versioned schema and migration map.

```yaml
identity:
  id:
  object_type: CLAIM | EVIDENCE | PROOF | PROCESS
  parent_id:
  atom_family:
  layer:
  component:
  version:
  content_hash:

provenance:
  raw_statement:
  source_uri:
  source_span:
  source_hash:
  author_or_witness:
  date_received:
  ai_contribution_declared:

claim:
  statement_technical:
  statement_plain:
  exact_negations: []
  scope:
  quantifiers: []
  boundary_conditions: []
  identity_conditions: []

axes:
  lifecycle_state:
  proof_class:
  register:
  ic_grade:
  why_outcome:

discovery:
  referent:
  distinctions: []
  identity_conditions: []
  dependency_floor: []
  operations: []
  constraints: []
  invariants: []
  collapse_conditions: []
  consequences: []
  representation_ladder: []
  formalization_boundary:

truth_space:
  if_true: []
  if_false: []
  false_worlds: []
  countermodels: []

reverse_reconstruction:
  candidate_grounds: []
  inference_steps: []
  unique_recovery: false

evidence:
  support: []
  challenge: []
  negative_controls: []
  independent_inputs: []
  limitations: []

proof:
  specification:
  formal_statement:
  axioms_used: []
  definitions_used: []
  lemmas_used: []
  receipt:
  what_checked: []
  what_not_proved: []

convergence:
  compared_atom_ids: []
  anonymized_signatures: []
  candidate_mapping: []
  rivals: []
  verdict:

why_closure:
  ladder_levels: []
  explanation_types: []
  non_restatement_pass:
  outcome:
  closure_level:
  next_discriminating_test:

classification:
  emergent_labels: []
  inherited_labels: []
  reconciliation_status:

root_pass:
  root_id:
  grounding_verdict:
  added_premises: []

gauntlet:
  countermodels: []
  kill_conditions: []
  preregistration_receipt:
  execution_receipts: []

admission:
  graph: candidate | admitted
  human_ruling: pending
  ruling_actor:
  ruling_date:
  rationale:

dependencies:
  depends_on: []
  supports: []
  challenges: []
  expands: []
  bridges_to: []
  supersedes: []

corrections: []
projections: []
```

The universal envelope is composed with exactly one type extension:

```yaml
claim_extension:     { register_anatomy, truth_conditions, exact_negations }
evidence_extension:  { source, custody, protocol, conditions, raw_record,
                       derived_artifacts, controls, independence_map,
                       discrimination_statement }
proof_extension:     { premises, inference_rules, derivation_steps, conclusion,
                       assumption_register, receipt, interpretation_boundary }
process_extension:   { purpose, inputs, preconditions, steps, decision_points,
                       outputs, discriminating_power, failure_modes, version,
                       run_receipt }
```

An absent value is not permission to guess. Use a declared null, `UNKNOWN`, `NOT_APPLICABLE`, or `OPEN` according to the schema.

---

# PART III — THE GENERAL EXPANSION PROCEDURE

## 8. WHAT IT MEANS FOR A CLAIM TO OPEN

A claim opens when its compressed assertion is decomposed into the conditions that must hold for that kind of claim to be warranted. The register determines the native anatomy. Each necessary condition becomes a child atom or an explicitly typed field when it is not independently assertive.

Opening is not paraphrase. It is dependency exposure.

The general operation is:

```text
PRESERVE → SEGMENT → TYPE → EXPOSE DEPENDENCIES → GENERATE NATIVE CHILDREN
→ DEFINE TRUTH SPACE → ATTACH EVIDENCE → BUILD RIVALS → TEST → RECORD TERMINI
```

### 8.1 Preserve

Store the raw source, exact span, source hash, date, and original identifier. No later clarification may erase what the source actually said.

### 8.2 Segment

Split conjunctions, hidden conditionals, scope changes, equivocations, empirical insertions, and bridge moves. A component boundary is required whenever one part could be true while another is false.

### 8.3 Type

Assign a provisional register only after reading the claim’s actual burden. Questions belong to burdens, not disciplines. A claim found in a physics paper may be historical, mathematical, metaphysical, or theological.

### 8.4 Expose dependencies

Ask what must be defined, observed, accepted, or derived before the claim can hold. Separate formulation dependencies from truth-making dependencies and evidential dependencies.

### 8.5 Generate native children

Instantiate the register template. Each child receives its own state and grade where independent failure is possible.

### 8.6 Define the truth space

State what the world or model looks like if the claim is true, what its exact negations are, and what observations or constructions discriminate among them.

### 8.7 Attach evidence without laundering

Evidence stays in its native class. Testimony remains testimony. A proof remains conditional on its axioms. A structural match remains a bridge. A confession remains theological.

### 8.8 Build the strongest rivals

Do not compare the preferred claim with a caricature. Construct alternatives capable of producing the same observed signature.

### 8.9 Test and preserve the result

Run preregistered tests where possible. Preserve failures, countermodels, null results, and incomplete termini. The output of opening is a more inspectable object, not a guaranteed upgrade.

## 9. COMPLETION CONDITIONS FOR AN OPEN ATOM

An atom is **FULLY_OPENED** only when:

- the raw claim and source are preserved;
- independently falsifiable components are separated;
- the register-native required fields are present;
- dependencies and inference licenses are typed;
- exact negations and countermodels are present;
- evidence and proof boundaries are explicit;
- unresolved fields are marked rather than filled;
- the next discriminating test is named where closure is absent;
- all child references resolve;
- the record passes schema and integrity validation.

`FULLY_OPENED` means structurally complete for evaluation. It does not mean true, admitted, proved, or canonized.

If a required native field is absent, the atom returns:

```text
DISCOVERY_INCOMPLETE
```

with missing fields, reason, and next action.

---

# PART IV — REGISTER-NATIVE EXPANSION TEMPLATES

## 10. HISTORY — THE TRANSMISSION CHAIN

```text
EVENT → POSSIBLE OBSERVERS → WITNESS → TESTIMONY → TRANSMISSION
→ DOCUMENT → PRESERVATION → CORROBORATION → INTERPRETATION → PRESENT CLAIM
```

A historical claim is not one undifferentiated appeal to “the sources.” It is a chain in which each link can preserve, lose, change, add, select, suppress, or independently confirm information.

### 10.1 Event

Record what is alleged to have happened, where, when, to whom, and at what resolution. Separate the event claim from later interpretations of its meaning.

Required questions:

- What event would make the statement true?
- Which parts are directly observable and which are inferred?
- What alternative events could generate the same later report?

### 10.2 Possible observers

Identify who or what could in principle have perceived the event. Distinguish physical presence, access, competence, attention, and opportunity.

### 10.3 Witness

For each claimed witness record identity, proximity, capacity, incentives, dependence on other witnesses, and whether the witness is named, anonymous, collective, hostile, friendly, or reconstructed.

### 10.4 Testimony

Record what the witness is actually reported to have said, in what form, at what time, and with what claimed certainty. Do not replace testimony with the present author’s summary.

### 10.5 Transmission

Map oral, scribal, institutional, liturgical, archival, or digital transmission. Record the number and type of intermediaries, opportunities for contamination, and independent channels.

### 10.6 Document

Record provenance, dating range, authorship status, genre, intended audience, material witnesses, and textual variants. A document’s existence supports a claim about what was recorded; it does not automatically prove the recorded event.

### 10.7 Preservation

Track custody, copying, loss, redaction, translation, canonization, discovery, and restoration. Name gaps.

### 10.8 Corroboration

Separate independent corroboration from repetition of a common source. Record hostile attestation, archaeological fit, documentary convergence, silence, and contradiction without pooling them blindly.

### 10.9 Interpretation

State the inference from preserved record to event claim. Type it as deductive, inductive, abductive, statistical, analogical, or underdetermined.

### 10.10 Present claim

The final child states exactly what the current evidence warrants, at the narrowest defensible scope.

### 10.11 Historical strength rule

The chain is limited by its weakest load-bearing link, but not every weak link destroys every conclusion. The record must state which conclusions survive and which fail if a given link is removed.

## 11. PHYSICS — THE MEASUREMENT ANATOMY

```text
QUANTITY → UNITS → DYNAMICS → PROTOCOL → INSTRUMENT → DATA
→ CONTROLS → ANALYSIS/FIT → CLAIM
```

### 11.1 Quantity

Define the observable or inferred quantity operationally. If the quantity is latent, state how it connects to observations.

### 11.2 Units and scale

Record dimensions, units, scale, normalization, resolution, error model, and dimensional checks. A physical claim that should have units but cannot name them is incomplete.

### 11.3 Dynamics

State the model, governing equation, parameters, initial conditions, boundary conditions, regime of validity, and approximations. Separate a fitted equation from a derived law.

### 11.4 Protocol

Describe sampling, intervention, randomization, calibration, exclusion criteria, preregistration, and stopping rules. Retrospective choices are marked.

### 11.5 Instrument

Record device, calibration state, sensitivity, specificity, noise floor, drift, saturation, preprocessing, and observer/software involvement.

### 11.6 Data

Preserve raw data or a hash-addressed location, transformations, missingness, exclusions, and data lineage. A chart is a projection, not the raw evidence.

### 11.7 Controls

Include negative controls, positive controls, sham conditions, baselines, rival models, leakage checks, and confound tests appropriate to the domain.

### 11.8 Analysis and fit

Record estimator, uncertainty, model comparison, sensitivity analyses, multiple-testing treatment, assumptions, and out-of-sample behavior. Good fit is not automatically identification of the true mechanism.

### 11.9 Physical claim

State the narrow empirical consequence supported by the measurement chain. Metaphysical or theological interpretation, if present, opens separately as a bridge or theological atom.

### 11.10 Physics completion rule

A physics claim missing operational quantity, units where applicable, protocol, instrument/data provenance, uncertainty, and controls returns `DISCOVERY_INCOMPLETE`.

## 12. MATHEMATICS AND FORMAL METHODS — THE FORMAL ANATOMY

```text
DEFINITION → AXIOM USE → INFERENCE RULE → LEMMA → DERIVATION
→ THEOREM STATEMENT → BUILD RECEIPT → INTERPRETATION BOUNDARY
```

### 12.1 Definition

Every defined term is inspected for hidden conclusions. A definition may stipulate a model object; it cannot establish that the object exists in physical reality or corresponds to God.

### 12.2 Axiom use

List explicit axioms, imported library assumptions, typeclass assumptions, classical principles, nonemptiness assumptions, and domain-specific postulates. Distinguish root assumptions from derived propositions.

### 12.3 Inference rule

Name the licensed step. Dependency is not inference: `B depends on A` does not itself show that A entails B.

### 12.4 Lemma

Each lemma states a reusable intermediate proposition and its dependencies. Lemmas that merely unpack definitions are labeled accordingly.

### 12.5 Derivation

Preserve the sequence of licensed steps. For computational proofs, preserve source, toolchain versions, commands, and outputs.

### 12.6 Theorem statement

The theorem atom stores the exact formal proposition. The plain-language rendering must be tested for equivalence and must not add intended interpretation.

### 12.7 Receipt

A gold receipt records at least:

```text
source file
theorem name
repository revision
toolchain and dependency versions
build command
exit code
zero-sorry status
content hash
what was checked
what was not proved
```

### 12.8 Interpretation boundary

If the theorem is claimed to describe physics, consciousness, morality, or theology, that move becomes a separate bridge atom. A passing Bool model establishes a property of that model, not automatically of Hilbert space, the world, or God.

## 13. THEOLOGY — THE PROCLAMATION ANATOMY

```text
SOURCE → TEXTUAL WITNESS → WITNESS TRADITION → PROCLAMATION
→ THEOLOGICAL REGISTER → CONFESSION CLASS → SCOPE → RELATION TO OTHER CLAIMS
```

Theological claims are not treated as embarrassing scientific claims. They are opened faithfully in their native register and judged by appropriate theological, historical, exegetical, philosophical, and confessional burdens.

### 13.1 Source

Name Scripture, creed, council, theological tradition, testimony, revelation claim, or constructive theological argument. Preserve exact citations and textual variants where relevant.

### 13.2 Textual witness

Record the actual passage or bounded excerpt, language and translation issues, literary context, and genre. A keyword match does not establish doctrine.

### 13.3 Witness tradition

Record how communities and interpreters received the source, including major agreements, disagreements, and historical development.

### 13.4 Proclamation

State what is being confessed or taught. Do not disguise proclamation as a neutral measurement claim.

### 13.5 Theological register

Identify whether the claim is scriptural attestation, doctrinal synthesis, metaphysical theology, Christological identification, moral teaching, eschatological prediction, or another controlled subtype.

### 13.6 Confession class

Use the project’s proof-boundary classes, including S or C where applicable, without laundering them into formal theorem or empirical evidence classes.

### 13.7 Scope

State whether the claim is internal to a confessed root, argued as public metaphysics, historically attributed, proposed as interpretation, or asserted universally. Root-conditioned entailment does not prove the root.

### 13.8 Relation to other claims

Record whether scientific, mathematical, historical, or experiential atoms constrain, resonate with, challenge, or leave the theological claim underdetermined.

## 14. BRIDGES — THE MAPPING ANATOMY

```text
SOURCE REGISTER → TARGET REGISTER → SOURCE OBJECT → TARGET OBJECT
→ MAPPING → PRESERVED → LOST → BOUNDARY CONDITIONS → GRADE
→ REVERSE MAPPING → COMMUTATIVITY TESTS → COUNTERMODELS
→ WHY-GATE → NEXT TEST
```

### 14.1 Source and target registers

Name both sides. A bridge cannot hide cross-register movement inside one sentence.

### 14.2 Source and target objects

Identify the exact atoms or structures. “Physics and theology are similar” is not a bridge record.

### 14.3 Mapping

Provide explicit maps between identities, relations, operations, states, or dependency positions. Vocabulary resemblance is insufficient.

### 14.4 Preserved structure

Name what remains invariant under translation: relations, order, composition, capability, dependency, conservation, symmetry, or collapse behavior.

### 14.5 Lost structure

Name what does not transfer. This field is mandatory. A bridge that cannot state its losses has not opened.

### 14.6 Boundary conditions

State where the mapping is expected to hold and where it is not. Local structural correspondence must not be projected globally.

### 14.7 Grade

Record both the bridge-grade vocabulary and, when evaluated, the IC grade. Do not infer one automatically from the other without an approved crosswalk.

### 14.8 Reverse mapping

Test whether the proposed map is invertible, partially invertible, many-to-one, or one-way. If reflection fails, the record cannot be called an isomorphism in the strict sense.

### 14.9 Commutativity and translation tests

Where operations are claimed to correspond, test whether mapping before or after the operation yields the same result. Record failures.

### 14.10 Countermodels and next test

Construct rival mappings and cases that preserve superficial features while breaking the preferred structure. Name the next observation or formal result that would discriminate them.

## 15. OTHER REGISTERS

The five templates above are mandatory cores, not a ban on other registers. Information, consciousness, moral, normative, computational, linguistic, and first-person claims require their own ratified templates. Until ratified, they use the universal envelope plus the closest applicable domain extension, with unresolved burdens marked `OPEN`.

No discipline becomes the master classifier. The burden of the assertion selects the extension.

---

# PART IV-A — THE NON-CLAIM OBJECT ANATOMIES

## 15A. THE EVIDENCE LAYER — THE ANATOMY OF BEARING WITNESS

An evidence atom is a preserved record whose epistemic function is discrimination. It may support, contradict, falsify, or test a claim, but it does none of those things merely by existing. Its bearing is a property of a typed edge evaluated against alternatives.

```text
SOURCE → PROVENANCE/CUSTODY → PROTOCOL → CONDITIONS → RAW RECORD
→ DERIVED ARTIFACTS → CONTROLS → INDEPENDENCE MAP → DISCRIMINATION STATEMENT
```

An evidence atom is **FULLY_OPENED** only when all nine burdens are present or explicitly marked inapplicable with rationale.

### 15A.1 Source

The source sub-atom identifies the originating object: instrument output, physical sample, manuscript, testimony, image, database export, experiment log, observation, or other record. It preserves original bytes where possible, together with URI or physical location, acquisition date, media type, size, and cryptographic hash.

The source is not a summary. If original bytes cannot be retained, the record states why, what surrogate was preserved, and what information may have been lost.

### 15A.2 Provenance and custody

The custody chain records who or what possessed the record, when, and what was done to it. Every transfer and transformation receives an event record linking prior and resulting hashes.

Required fields include:

```text
custodian or system
time interval
transfer method
integrity check
transformation, if any
prior hash
resulting hash
known gap or uncertainty
```

A custody break does not automatically destroy evidential value. It limits what can be claimed from integrity and becomes part of the uncertainty record.

### 15A.3 Protocol

The protocol states how the observation or record was produced. It names sampling, recruitment, apparatus, interview procedure, documentary selection, measurement schedule, calibration, exclusion rules, preregistration, and stopping conditions as applicable.

A hash proves file identity after hashing. It does not prove that the file was generated by a reliable protocol. Evidence without a recoverable protocol is classified according to what it actually is—often testimony, anecdote, or uncontrolled observation—not discarded and not inflated.

### 15A.4 Conditions

Conditions bound the observation. They include time, environment, population, range, scale, context, instrument configuration, observer position, inclusion criteria, and relevant background state.

The evidence edge may not claim beyond those conditions without a separate generalization claim and warrant.

### 15A.5 Raw record

The raw record is the least processed available observation. It is preserved verbatim and immutable. Missing fields, illegible portions, sensor dropouts, uncertain translations, and corrupted segments remain visible.

For testimony, “raw” means the earliest recoverable wording or recording, not the underlying event itself. For a historical document, the raw record is the document witness; the event claim still requires the history anatomy.

### 15A.6 Derived artifacts

Cleaning, OCR, transcription, translation, normalization, aggregation, feature extraction, plotting, fitting, and summarization create derived artifacts. Each artifact records:

- its parent object or objects;
- transformation process and version;
- parameters and operator;
- output hash;
- information removed, merged, inferred, or added;
- reversibility and restoration path;
- validation or review status.

A chart, quotation packet, cleaned table, or model feature is never allowed to masquerade as the raw record.

### 15A.7 Controls

Controls ask what the system reports when the proposed effect should be absent, present at a known level, or produced by a rival mechanism. Depending on the burden, controls may include negative, positive, sham, blank, placebo, calibration, hostile-witness, irrelevant-text, permutation, leakage, synthetic, or holdout controls.

An absent control is not always fatal—for unique historical events, some experimental controls are impossible—but the missing discrimination must be stated. “Evidence without controls is a story” is a warning against causal overclaim, not a rule that testimony ceases to exist.

### 15A.8 Independence map

The independence map prevents correlated records from being counted as independent convergence. It represents shared:

```text
originating source
witness or author
instrument
dataset
selection mechanism
institution or transmission chain
analysis code
assumption
funding or incentive structure
```

Five reports copied from one report are one originating channel with five transmissions. Two instruments sharing the same calibration defect are not fully independent. Independence can be partial and dimension-specific; it is assessed, not assumed.

The map records clusters and common causes. Any combined evidential weight must use the effective independent structure rather than raw record count.

### 15A.9 Discrimination statement

Every evidence-to-claim edge answers:

> **What would this record look like if the target claim were false, and how does the observed record differ from that expectation?**

The statement names at least the target claim, its relevant negation or rival, expected record under each, observed feature, comparison rule, and residual ambiguity.

If the record is equally expected under every live hypothesis, its discrimination weight is zero. It may remain valuable as context, provenance, or a constraint, but it does not count as differential support.

### 15A.10 Evidence edge states

```text
supports     — the record is more expected under the claim than the named rival.
contradicts  — the record is less expected under the claim but does not independently refute it.
falsifies    — the record meets a preregistered kill condition under a valid protocol.
tests        — the record is produced to discriminate but the result may be null or pending.
```

The edge—not the evidence object—carries target-specific direction, discrimination statement, weight or grade, independence adjustment, boundary conditions, and reviewer ruling. The same evidence atom may support one claim, contradict another, and merely test a third.

### 15A.11 Evidence completion and failure states

An evidence atom returns `DISCOVERY_INCOMPLETE` when a required source, protocol, raw record, or discrimination statement is missing. Other candid states include `CUSTODY_GAP`, `CONTROL_LIMITED`, `DEPENDENT_CHANNEL`, `NON_DISCRIMINATING`, `PROTOCOL_DEVIATION`, and `TRANSFORMATION_UNVERIFIED`.

These states describe limitations. They do not authorize deletion.

## 15B. THE PROOF LAYER — THE ANATOMY OF ESTABLISHMENT

A proof atom is not a confident claim and not a screenshot of successful output. It is the complete derivation object connecting named premises to one exact conclusion through licensed steps.

```text
PREMISES → INFERENCE RULES → DERIVATION STEPS → CONCLUSION
→ ASSUMPTION REGISTER → RECEIPT → INTERPRETATION BOUNDARY
```

### 15B.1 Premises

Every premise is named, versioned, and linked to a claim atom. Premises are classified as definitions, axioms, boundary conditions, imported theorems, empirical inputs, root-conditioned assumptions, or temporary hypotheses.

A proof may be deductively valid while one premise remains candidate or false. Therefore the proof’s build status and the premises’ epistemic grades remain separate.

The governing diagnostic is not only “what is the weakest premise?” but “which premise is unacknowledged?” A weak acknowledged premise makes the conclusion conditional. A hidden premise makes the reported proof scope false.

### 15B.2 Inference rules

Every transition names its license: logical rule, algebraic transformation, induction principle, statistical rule, theorem invocation, model assumption, or other valid step. No arrow appears merely because the next sentence sounds plausible.

An inference-rule source may be a formal kernel, cited theorem, declared methodological rule, or explicit abductive warrant. Deductive, inductive, abductive, statistical, and analogical steps must not be mixed without labels.

### 15B.3 Derivation steps

Steps are ordered, inspectable, and individually addressable when they can fail independently. Each step records inputs, rule, output, dependencies, and verification state.

Compression is permitted only when the omitted steps are mechanically reconstructible or linked. “Therefore” is not a receipt.

### 15B.4 Conclusion

The conclusion is a separate claim atom containing the exact statement established under the premises. The proof atom connects to it with `proves`.

The conclusion must preserve quantifiers, types, scopes, model restrictions, and conditions. A plain-language rendering may accompany it but may not add words such as “real,” “physical,” “God,” “consciousness,” or “therefore Christianity” unless those appear in the formal statement with warranted definitions and bridges.

### 15B.5 Assumption register

The assumption register includes:

- all explicit and imported axioms;
- definitions that constrain the result;
- nonemptiness and existence assumptions;
- classical or constructive logic choices;
- boundary and initial conditions;
- idealizations and simplifications;
- model-to-world assumptions;
- root-conditioned theological premises;
- sensitivity: what changes when each assumption is removed or weakened.

The register distinguishes assumptions used for formulation from assumptions used in derivation.

### 15B.6 Receipt

The canonical receipt classes are:

```text
NOT_ATTEMPTED
SPECIFICATION_ONLY
ENCODED_NOT_BUILT
BUILT_WITH_GAPS
BUILT_ZERO_SORRY
COUNTERMODEL_FOUND
FORMALLY_REFUTED_AS_STATED
```

Legacy vocabularies may map to these only through an explicit registry. Existing `proof_label` values remain untouched during proposed classification.

A build receipt records theorem and file names, repository revision, source hash, toolchain and dependency versions, exact command, exit code, warnings, `sorry`/admission count, runtime environment, date, and operator. It also prints:

```text
what_checked:
what_not_proved:
```

A successful build without these boundaries is operational evidence of compilation, not a complete proof receipt.

### 15B.7 Interpretation boundary

Every proof prints what it does not establish. This field is mandatory and travels with every projection of the proof.

Examples:

- A Lean theorem over Boolean predicates does not establish the corresponding property in Hilbert space.
- A theorem about a stipulated moral variable does not establish that morality is a physical conserved quantity.
- Consistency of a theological model does not establish the truth or uniqueness of the theology.
- A finite model witness establishes satisfiability in that model, not metaphysical actuality.
- A derived prediction is not empirical confirmation until evidence bears on it.

If an intended interpretation crosses registers, the interpretation boundary points to the required bridge atom.

### 15B.8 Countermodels as proof outputs

A countermodel is a successful result against an overstrong statement. It records the proposition refuted, construction, assumptions, execution receipt, minimal failing feature, and repair options.

`COUNTERMODEL_FOUND` and `FORMALLY_REFUTED_AS_STATED` never disappear when a weaker successor theorem is admitted. The corpse remains linked to the lesson and correction.

### 15B.9 Proof completion rule

A proof is `FULLY_OPENED` only when premises resolve, every inference license is inspectable, the exact conclusion exists as a claim atom, the assumption register is complete, the receipt matches the source, and the interpretation boundary is printed. This structural state is independent of whether the receipt says `BUILT_ZERO_SORRY` or `COUNTERMODEL_FOUND`.

## 15C. THE PROCESS LAYER — THE ANATOMY OF THE RUNNABLE

A process atom is a versioned method whose function is to transform, generate, test, route, score, validate, or govern. The Unified Grammar pipeline, Why-Closure Gate, blind reconstruction protocol, resolver, guard, migration tool, proof build, and this expansion canon are processes or process specifications.

```text
PURPOSE → INPUTS → PRECONDITIONS → STEPS → DECISION POINTS → OUTPUTS
→ DISCRIMINATING POWER → FAILURE MODES → VERSION → RUN RECEIPT
```

### 15C.1 Purpose

State the single operational capability added by the process. A purpose is bounded: “validate schema conformance” is valid; “determine truth” is not a valid purpose for a format validator.

### 15C.2 Inputs

Name accepted object types, schemas, versions, required fields, and immutable source references. Inputs are hash-pinned when a run must be reproducible.

### 15C.3 Preconditions

State what must already hold: dependency availability, toolchain, permissions, calibration, blinded keys, preregistration, human selection, or candidate-graph isolation.

### 15C.4 Steps

List ordered operations at a resolution sufficient for independent reproduction or audit. Each consequential transformation states what it reads, writes, and preserves.

### 15C.5 Decision points

Human rulings, thresholds, branching logic, exception handling, and stopping conditions are explicit. A process cannot conceal a subjective selection inside an apparently deterministic step.

### 15C.6 Outputs

Specify output object types, schemas, storage destinations, status meanings, hashes, and whether outputs are proposals, evidence, receipts, projections, or canonical mutations.

An output’s type is determined by its function, not by the prestige of the process that created it. AI extraction produces claim candidates; it does not produce admitted claims.

### 15C.7 Discriminating power

State what the process can distinguish and what it cannot. Examples:

- a schema validator distinguishes conforming from nonconforming records, not true from false claims;
- a proof build distinguishes kernel acceptance from rejection of encoded statements, not physical applicability;
- the Why-Gate distinguishes explanatory closure from restatement under its rubric, not divine revelation from non-revelation by itself;
- an evidence protocol may distinguish two named hypotheses while leaving a third unresolved.

### 15C.8 Failure modes

Failure modes are part of the process definition. Include invalid input, unresolved references, stale schema, data leakage, post hoc criteria, non-independent controls, tool failure, partial write, nondeterminism, reviewer override, and false-success states.

Each failure mode names detection, safe halt behavior, artifacts preserved, and recovery path.

### 15C.9 Version

Processes are immutable by version. Material changes to input contract, step order, thresholds, output semantics, or authority create a new version. Old versions remain resolvable so past results can be interpreted.

### 15C.10 Run receipt

A process specification is distinct from a process execution. Every execution records:

```text
process ID and version
input IDs and hashes
configuration and environment
start and end time
operator or agent
step outcomes
warnings and deviations
output IDs and hashes
exit state
what the run establishes
what the run does not establish
```

### 15C.11 Recursive self-application

Methods obey their own grammar. This canon can be treated as a process atom and audited for purpose, inputs, steps, outputs, discrimination, failure modes, and version. Self-application does not prove the method complete; it makes exceptions and authority visible.

## 15D. THE UNIVERSAL SUB-ATOM RULE

The named positions in an anatomy become separate sub-atoms when they make independently contestable assertions or carry independently reusable records. Purely structural fields may remain embedded when they cannot sensibly receive a separate truth or integrity ruling.

The test is:

> Could this part fail, change, be reused, or be corrected while the parent and its other parts remain intact?

If yes, it receives an address or canonical linked identity. If no, it remains a typed field. This prevents both bundled overclaim and meaningless atom explosion.

---

# PART V — BLIND STRUCTURAL DISCOVERY

## 16. THE INVARIANT SIGNATURE

Before two domains are compared, each opened atom is rendered without its inherited names as:

```text
IDENTITIES · DISTINCTIONS · RELATIONS · OPERATIONS · DEPENDENCIES
· CONSTRAINTS · INVARIANTS · COLLAPSE CONDITIONS · CONSEQUENCES
```

### Identities

What objects, states, agents, events, or propositions must remain trackable as the same?

### Distinctions

What differences make the system nontrivial? What collapses if the distinctions disappear?

### Relations

What connects the identities: order, adjacency, dependence, causation, participation, entailment, observation, covenant, composition, or another typed relation?

### Operations

What transformations can occur? Who or what performs them? Are they reversible, compositional, deterministic, stochastic, voluntary, or externally driven?

### Dependencies

What must exist or hold before something else can be formulated, instantiated, observed, or derived?

### Constraints

What possibilities are excluded? Are constraints logical, mathematical, dynamical, empirical, historical, moral, or theological?

### Invariants

What remains stable across permitted transformations?

### Collapse conditions

What failure removes a capability, erases a distinction, makes the system incoherent, or changes its class?

### Consequences

What follows if the structure is granted, and by what inference license?

## 17. THE BLINDNESS REQUIREMENT

The signatures must be compared before preferred domain labels are allowed to guide pairing. A valid blind packet:

- replaces domain-loaded names with neutral tokens;
- preserves arity, direction, order, and type information;
- withholds the desired theological identification;
- includes rival pairings;
- records the selection rule before results are inspected;
- keeps the deblinding key hash-pinned.

Blindness does not make an analysis unbiased by magic. It removes one known route by which vocabulary resemblance and desired conclusions can determine the mapping.

---

# PART VI — HOW AN ISOMORPHISM CANDIDATE IS BORN

## 18. DISCOVERY, NOT ASSERTION

An isomorphism candidate is born only after two fully opened structures display a mapping that preserves enough of their invariant signatures to justify testing. Shared words such as “light,” “information,” “field,” “law,” “relation,” “observer,” or “logos” do not create a candidate by themselves.

The order is:

```text
OPEN A → OPEN B → ANONYMIZE → GENERATE CANDIDATE MAPS
→ SCORE PRESERVATION AND LOSS → BUILD RIVALS → PRESSURE TEST
→ ASSIGN IC GRADE → RUN WHY-GATE → STORE AS BRIDGE OR REJECT
```

## 19. MAPS, PRESERVATION, AND REFLECTION

For a strict isomorphism claim, the bridge must provide maps in both directions and show appropriate preservation and reflection. If only selected relations transfer, the correct label may be homomorphism, embedding, analogy, correspondence, or translation rather than isomorphism.

The name follows the demonstrated structure.

The minimum serious record includes:

- source set or structure;
- target set or structure;
- forward map;
- reverse map or explicit statement that none exists;
- relation/operation preservation tests;
- reflection tests;
- boundary conditions;
- lost structure;
- rival maps;
- collapse tests.

## 20. THE PRESSURE TEST

Every preferred mapping faces four attacks.

### 20.1 Remove the labels

If the match disappears when evocative names are removed, the candidate was lexical rather than structural.

### 20.2 Permute the pairings

Generate alternative pairings subject to the same rules. The preferred mapping must demonstrate an advantage not created by hand-selection.

### 20.3 Construct the strongest rival

The rival should explain the same signature with equal care. A naturalistic, alternative theological, mathematical, historical, or artifact-based account is not weakened to make the preferred bridge look unique.

### 20.4 Measure advantage

Use preregistered criteria: preserved relations, dependency alignment, operational commutativity, collapse prediction, translation stability, complexity penalty, and holdout behavior. A score is evidence about a test, not a probability that the metaphysical conclusion is true.

## 21. UNIQUE RECOVERY AND UNDERDETERMINATION

Minimal convergence occurs when the proposed root is among the structures capable of generating the observed signature.

Unique recovery requires that the reconstruction return only that root under the stated search space and assumptions.

```text
minimal convergence: preferred root ∈ recovered candidate set
unique recovery:      recovered candidate set = {preferred root}
```

If several roots generate the same signature, the correct result is underdetermination. That is not a failed experiment. It identifies what the present structure cannot decide.

## 22. THE WHY-GATE IN FULL

The why-gate asks not merely whether two structures correspond, but why the correspondence exists rather than failing or taking another form.

The ladder is evaluated level by level:

```text
DESCRIPTIVE → MECHANISTIC → STRUCTURAL → BOUNDARY → HISTORICAL
→ GROUNDING → PURPOSIVE
```

Inapplicable levels are marked, not silently skipped.

Answers are typed, for example, as logical necessity, mathematical necessity, definitional consequence, dynamical mechanism, common ancestry, common constraint, selection effect, design claim, grounding claim, purposive explanation, artifact, or coincidence.

The non-restatement test asks: does the explanation add information beyond saying that the structures match? “They correspond because they share a pattern” fails.

Closure always reports its level. Structural closure is not automatically grounding or purposive closure. A Mark-to-God structural bridge may be closed at one level while a specifically Trinitarian identification remains `WHY_OPEN`.

## 23. BIRTH, SURVIVAL, AND STORAGE

An isomorphism candidate can end in one of four ways:

```text
REJECTED — mapping fails or is no better than rivals.
ANALOGY — useful limited resemblance; no identity propagation.
BRIDGE_CANDIDATE — serious preserved structure, still awaiting gate or ruling.
CONFIRMED_STRUCTURAL_BRIDGE — IC-4/5, pressure-tested, WHY-gated, human-admitted.
```

Even the final state propagates as a bridge, never as proof of every statement in the target register.

---

# PART VII — RECURSION, TERMINI, AND THE FLOOR

## 24. ATOMS CONTAIN ATOMS

Every newly exposed child can itself be opened. A theorem child opens into definitions, axioms, lemmas, and receipts. A document child opens into provenance and preservation. A measurement child opens into calibration and uncertainty. A bridge child opens into maps, losses, and rivals.

Recursion stops only when further decomposition would no longer expose an independently meaningful burden or when a valid terminus is reached.

## 25. THE THREE TERMINI

### 25.1 PRIMITIVE

A primitive is a declared floor beyond which the present grammar cannot open without presupposing what it is trying to explain. In the methodology, the Mark—distinction itself—is the limiting example.

A primitive record must state:

- why it is treated as primitive;
- what depends on it;
- what alternative primitives have been considered;
- whether its primitiveness is logical, methodological, model-relative, or theological.

Calling something primitive does not make it self-evidently true.

### 25.2 INDEPENDENT_EMPIRICAL_INPUT

This is a measured or observed input the framework uses but does not derive: a constant, initial condition, dataset, event, or boundary condition.

It retains the full measurement or historical chain. It must not be relabeled as a theoretical consequence simply because the model requires it.

### 25.3 OPEN

An open terminus records an unresolved dependency, missing mechanism, undecided rival, or unperformed test.

It must include:

- the exact open question;
- current candidates;
- evidence bearing on each;
- what has already failed;
- the next discriminating test;
- downstream claims affected by the uncertainty.

OPEN is first-class corpus knowledge.

## 26. THE NO-BORROWED-ANSWER RULE

No expansion may terminate in a label borrowed from the desired conclusion.

Invalid examples:

```text
Why is reality intelligible? → Logos, because Logos means intelligibility.
Why is relation fundamental? → Trinity, because Trinity is relational.
Why does the model restore? → Grace, because grace restores.
```

These may be theological identifications or proposed explanations, but they are not closures until the independent burden, rivals, mapping, and why-gate are satisfied.

---

# PART VIII — DEPENDENCY, FAILURE, AND CORRECTION

## 27. TYPED EDGES

The admitted and candidate graphs use typed edges. Edges are first-class relational records with their own identity, provenance, version, status, warrant metadata, reviewer, and correction history. They do not inherit the authority of either endpoint.

```text
CLAIM    ← supports / contradicts / falsifies / tests — EVIDENCE
CLAIM    ← proves —                                      PROOF
PROOF    — derivedFrom →                                 CLAIM
EVIDENCE — generatedBy →                                 PROCESS
PROOF    — auditedBy →                                   PROCESS
ANY      — dependsOn / defines / interprets / bridgesTo
           / expands / forksFrom / instantiates
           / supersedes / corrects →                     ANY
```

### 27.1 Edge identity and direction

Every edge names source, predicate, target, direction, version, creation actor, creation process, and lifecycle state. Inverse renderings may be generated for navigation, but the canonical direction remains fixed.

### 27.2 Evidence-edge payload

`supports`, `contradicts`, `falsifies`, and `tests` require the target claim version, discrimination statement, compared rival or negation, conditions, independence cluster, weight or grade method, and uncertainty. `falsifies` additionally requires the kill condition and evidence that it was preregistered or a ruling explaining why retrospective falsification is valid.

### 27.3 Proof-edge payload

`derivedFrom` identifies the exact premise role and version. `proves` identifies the exact conclusion statement and carries the proof receipt reference. If the conclusion changes, the proof edge does not silently retarget.

### 27.4 Process-edge payload

`generatedBy` and `auditedBy` name the process version and run receipt. A process specification without an execution receipt cannot be used to claim that an evidence or proof object was actually generated or audited.

### 27.5 Bridge-edge payload

`bridgesTo` requires source and target registers, explicit mapping, preserved structure, lost structure, boundary conditions, bridge grade, IC grade where assigned, WHY outcome, countermodels, and next test. Missing loss information makes the edge incomplete.

### 27.6 General semantic edges

`dependsOn` records load-bearing prerequisite structure. `defines` records semantic stipulation and never evidential support. `interprets` records a meaning assignment without proof transfer. `expands` records parent-child anatomy. `forksFrom` records an alternative development. `instantiates` records a case of a general type. `supersedes` changes current selection while preserving history. `corrects` binds a correction record to its target.

An edge states a relationship, not an inference unless its predicate, payload, and warrant explicitly license that inference. Edge weights never become “percent true.”

## 28. FAILURE PROPAGATION

Failure propagates only along load-bearing dependencies.

- If B deductively depends on A and A is falsified, B becomes upstream-falsified unless an independent derivation is recorded.
- If B is merely motivated by A, falsifying A removes that motivation but may not falsify B.
- If two claims are joined by analogy, falsification does not automatically cross the bridge.
- Bridge propagation is permitted only under the active schema’s approved grades and relation rules.
- An interpretation does not inherit theorem status, and a theorem does not inherit empirical truth from an interpretation.

The graph must make the blast radius inspectable before a ruling is applied.

## 29. THE CORRECTION RECORD — THE CORPUS IMMUNE SYSTEM

A correction is a first-class governance record, not an in-place edit and not a fifth epistemic object layer. It opens as:

```text
ORIGINAL → DEFECT CLASS → DEFECT STATEMENT → EVIDENCE → PROPOSED TEXT OR ACTION
→ DOWNSTREAM INVALIDATION MAP → HUMAN RULING → RESTORATION PATH → RECEIPT
```

### 29.1 Original

The correction points to the exact object or edge version and preserves its bytes, content hash, projections, prior state, and context. The target remains resolvable after correction.

### 29.2 Defect class

```text
LOCAL_DEFINITE_FIX    — spelling, broken reference, formatting, or other bounded repair
SUBSTANTIVE_CORRECTION — meaning, evidence, derivation, scope, or warrant materially changes
WITHDRAWAL             — the author or ruler removes the object from current use
RECLASSIFICATION       — primary content remains, but type, register, grade, or state was wrong
```

The class determines required review and blast-radius handling. A substantive change may never be disguised as a local fix.

### 29.3 Defect statement

State exactly what is wrong, where it occurs, how it was detected, and what remains valid. Avoid global language when the defect is local.

### 29.4 Evidence

Link the evidence atoms, proof receipts, countermodels, process failures, or governance rulings that warrant correction. The correction’s existence does not prove its diagnosis.

### 29.5 Proposed text or action

Provide the replacement object, weakened scope, new grade, withdrawal notice, or reclassification as a staged proposal with hashes and a readable diff. The proposal does not overwrite the target before ruling.

### 29.6 Downstream invalidation map

Traverse typed dependencies and classify each downstream effect:

```text
UNAFFECTED
REVIEW_REQUIRED
WEAKENED
UPSTREAM_FALSIFIED
PROJECTION_REBUILD_REQUIRED
RERUN_OWED
```

Bridge, analogy, interpretation, and motivational edges are evaluated by their actual propagation rules; the system does not invalidate by mere adjacency.

### 29.7 Human ruling

The ruler accepts, rejects, modifies, or defers the correction. The record names actor, authority, date, rationale, dissent or unresolved issue, and effective graph state. Automation may prepare the packet but cannot issue the ruling.

### 29.8 Restoration path

The correction records how to reconstruct the pre-correction state, including object hashes, schema and process versions, projection locations, and ledger events. Restoration does not erase the correction; it creates another ruled state transition.

### 29.9 Receipt and re-entry

The receipt records applied changes, hashes, affected edges, regenerated projections, validation results, and unresolved reruns. Every corrected atom re-enters the Unified Grammar pipeline at Stage 0 with its provenance intact.

Corrections print wherever the corrected claim printed. Nothing is silently edited or deleted. Falsified and withdrawn atoms remain visible with their lessons. Supersession changes current preference, not historical existence. The correction ledger is the corpus’s memory of its mistakes—and therefore part of its credibility.

---

# PART IX — THE UNIVERSAL GRAMMAR

## 30. WHAT THE GRAMMAR IS

The universal grammar is not a master essay imposed on the corpus. It is the emergent structure visible when admitted atoms and admitted bridges are viewed together.

```text
UNIVERSAL GRAMMAR
  = all human-admitted CLAIM, EVIDENCE, PROOF, and PROCESS atoms
  + all human-admitted IC-4/IC-5 structural bridges that passed the WHY-gate
  + all typed dependency, challenge, correction, and expansion edges
  + the complete correction ledger
  + all retained OPEN boundaries necessary to interpret the graph honestly
```

Open records are included as boundaries of present knowledge, not as admitted answers.

## 31. WHY IT MUST EMERGE BOTTOM-UP

If categories are imposed before analysis, every domain is forced to speak the language of the desired synthesis. If the grammar is allowed to emerge after opening, testing, and reconciliation, repeated structures can be discovered without erasing differences.

Bottom-up does not mean assumption-free. It means assumptions are recorded, roots are conditional when necessary, selection rules are fixed before results, and candidate structures remain separable from admitted ones.

## 32. WHAT IT MEANS FOR A PATTERN TO BE UNIVERSAL

A pattern is not universal because it appears in several chosen examples. A serious universality claim requires:

- a defined domain of applicability;
- independent instances;
- stable invariant signature;
- preregistered inclusion and exclusion rules;
- negative cases;
- rival grammars;
- collapse behavior;
- translation tests;
- out-of-sample or holdout performance where possible;
- an explicit statement of exceptions and unknowns.

The grammar expands when new admitted structure survives. It contracts or differentiates when corrections show that a claimed universal was local.

## 33. CHRISTIAN ROOT-CONDITIONED READING

The project may begin from the theological claim that God is Creator and ask whether physics, information, consciousness, moral order, history, revelation, and the person of Christ cohere as aspects and witnesses of one created reality.

That root-conditioned pass is legitimate when declared. It does not turn science into an instrument that stands outside reality and votes God into existence. Nor does it permit a theological answer to be inserted into an empirical blank.

Within the confessed root, distributed convergence can be examined as a claim about created testimony: physical intelligibility, informational order, moral cost, personal consciousness, historical witness, grace, and revelation may converge without becoming one register. Corruption can predict distortion without making every discrepancy disappear. Christ may be proposed as the interpretive center without a structural bridge being mislabeled as an empirical proof.

The atom system makes this constructive theological reading stronger by making its boundaries visible. It allows the corpus to say:

```text
THIS is formally derived.
THIS is empirically measured.
THIS is historically attested.
THIS is theologically confessed.
THIS is a bridge between them.
THIS remains open.
```

Unity is not achieved by erasing those sentences. It is achieved when they can remain distinct and still belong to one inspectable graph.

---

# PART X — THE HUMAN ADMISSION GATE

## 34. CANDIDATE AND ADMITTED GRAPHS

The candidate graph contains extracted claims, proposed expansions, unruled migrations, candidate bridges, model outputs, and AI-generated sidecars. The admitted graph contains only objects that have received an explicit human ruling under the active governance contract.

No automated run canonizes.

Automation may:

- preserve and hash sources;
- propose segmentation;
- instantiate templates;
- detect missing fields;
- validate schema;
- resolve identifiers;
- generate projections;
- run deterministic tests;
- calculate registered scores;
- display dependencies and possible blast radius.

Automation may not:

- declare a claim true;
- convert analogy into identity;
- decide theological orthodoxy;
- upgrade proof class from prose resemblance;
- invent missing evidence;
- resolve an OPEN field by preference;
- move a candidate into canon without a human ruling.

## 35. THE RULING PACKET

A human reviewer should receive:

```text
SELECT — exact atoms and versions under review
ACT — proposed admission, return, correction, weakening, or withdrawal
STAGE — isolated candidate changes
PREVIEW — human-readable claim, evidence, proof, rivals, losses, and blast radius
APPROVE — named ruling with rationale and receipt
```

The ruling packet must show changes against the prior version and must never hide unresolved fields behind a green summary.

---

# PART XI — WORKED EXPANSION EXAMPLES

## 36. EXAMPLE A — OPENING A BUNDLED CROSS-REGISTER CLAIM

Suppose the source says:

> Time-translation symmetry in a moral domain implies a conserved moral current; wrongdoing is therefore irreversible but conserved, and grace is the external term that closes the ledger.

This is not one atom. It contains at least:

```text
C1 FORMAL: Under a defined moral-domain Lagrangian with time-translation symmetry,
           a conserved current follows under the stated Noether conditions.

C2 BRIDGE/INTERPRETIVE: The formal variables adequately map to moral action, debt,
                        irreversibility, and displacement.

C3 THEOLOGICAL: Grace or atonement is correctly identified with the external source
                term required by the model.
```

### C1 opens formally

- Define the state space, action, symmetry, current, differentiability conditions, and moral-domain terms.
- List all axioms and imported mathematical results.
- Prove the theorem or label it specification/informal.
- Record whether the proof establishes a theorem in an abstract model only.

### C2 opens as a bridge

- Source: formal dynamical system.
- Target: moral experience and normative consequence.
- Map each variable and operation.
- State preserved relations.
- State losses: moral agency, intention, guilt, interpersonal meaning, and normativity may not be represented by the formal current.
- Construct rivals: bookkeeping metaphor, psychological displacement model, social-cost model, or no conserved moral quantity.
- Assign IC grade only after tests.

### C3 opens theologically

- Name scriptural and doctrinal sources for grace and atonement.
- State confession class and scope.
- Separate “the model requires an external term” from “the external term is Christ’s atonement.”
- Record the latter as a theological identification bridge unless independently established in its native register.

Possible result:

```text
C1: BUILT_ZERO_SORRY in a stipulated abstract model.
C2: IC-2 or IC-3 structural analogy, WHY_OPEN.
C3: theological confession/interpretation, root-conditioned; not derived by C1.
```

This is not a failure of unification. It is an honest map of where each burden currently stands.

## 37. EXAMPLE B — OPENING A RESURRECTION CLAIM

Suppose the present claim is:

> Jesus rose bodily from the dead.

The history expansion asks:

- What event is alleged?
- Who could have observed the death, burial, empty tomb, appearances, and later effects?
- Which witnesses are independently attested?
- What do the earliest testimonies actually say?
- How did those testimonies reach surviving documents?
- What is the dating, genre, textual preservation, and dependence of those documents?
- Which facts are multiply attested and which depend on one channel?
- What rival event models exist: legend, grief experience, mistaken identity, relocation, conspiracy, visionary experience, mixed explanation?
- Which model best explains the bounded evidence, and what remains underdetermined?

The theological interpretation—“the resurrection is God’s vindication and the center of new creation”—opens separately from the historical event claim while remaining connected to it.

## 38. EXAMPLE C — TESTING A LOGOS/INFORMATION BRIDGE

Suppose two opened structures show:

```text
Structure A: stable distinctions, syntactic relations, transformation rules,
             error-sensitive preservation, interpretable consequence.

Structure B: intelligible distinctions, rational relations, lawful transformation,
             truth-preserving communication, meaning-bearing consequence.
```

A weak response says, “Information is Logos.”

A conforming response:

1. anonymizes the structures;
2. proposes explicit maps;
3. tests whether syntax, semantics, agency, truth, and interpretation are preserved;
4. names losses—Shannon information alone does not supply meaning, truth, intention, or personhood;
5. compares rivals such as mathematical structuralism, emergent semantics, teleosemantics, and theistic Logos ontology;
6. grades the correspondence;
7. asks why the correspondence exists;
8. stores the surviving result as a bridge with `WHY_OPEN` unless grounding is genuinely discriminated.

The bridge may illuminate both domains without pretending that an information equation proves John 1.

---

# PART XII — VALIDATION AND IMPLEMENTATION CONTRACT

## 39. FORMAT VALIDATION

The guard tool checks:

- required fields;
- controlled vocabularies;
- identifier form;
- hash form;
- reference resolution;
- child-parent consistency;
- version consistency;
- required bridge losses;
- required OPEN next tests;
- proof receipt completeness;
- projection determinism.

Passing format validation means the object is well-formed. It does not mean the claim is true.

## 40. SEMANTIC REVIEW

Human or explicitly bounded analytic review checks:

- whether segmentation preserved the source;
- whether the plain statement matches the technical statement;
- whether the register is correct;
- whether dependencies are real;
- whether evidence is appropriately typed;
- whether proof scope is overstated;
- whether countermodels are strong;
- whether bridge losses are honest;
- whether the proposed grade is warranted;
- whether an OPEN field has been prematurely closed.

## 41. MIGRATION CONTRACT

Legacy objects are preserved before migration. A migration must produce:

- source inventory and hashes;
- old-to-new identifier map;
- field-level transformation log;
- explicit assumptions;
- validation output;
- unresolved-field report;
- rollback or restoration path;
- human approval before admitted-graph replacement.

A valid legacy record is not called invalid merely because it lacks every v1.0 field. It is described as valid under its current contract and incomplete under the expanded envelope.

---

# PART XIII — NON-NEGOTIABLE GUARDS

## 42. EPISTEMIC GUARDS

- Analogy is never promoted to identity.
- A bridge never propagates as proof.
- A specification is never reported as a theorem.
- A model theorem is never reported as empirical validation without a validated model-to-world bridge.
- A theological identification is never reported as physically derived.
- A source’s authority is never inferred from the resolver.
- A document’s existence is never treated as proof of every event it records.
- A fitted pattern is never treated as a uniquely identified mechanism without rival comparison.
- `WHY_OPEN` is never silently converted to closure.
- `UNKNOWN` is never replaced by the preferred answer.

## 43. PROCEDURAL GUARDS

- Preserve before decomposition.
- Analyze before classification.
- Register selection criteria before inspecting the target pattern.
- Build the strongest rival, not the easiest rival.
- Retain countermodels and failed claims as first-class receipts.
- Keep candidate and admitted graphs separate.
- Require explicit human admission.
- Correct where the claim printed.
- Never silently delete or rewrite provenance.
- Generate every projection from one canonical object.

## 44. TOOL GUARDS

- The resolver resolves references; it never creates authority.
- The guard enforces format; it never grades truth.
- The scorer applies registered criteria; it never estimates metaphysical probability.
- The proof assistant checks the encoded theorem; it never supplies the intended interpretation.
- The AI proposes structures and flags gaps; it never canonizes.
- The renderer displays state; it never becomes a second truth store.

---

# PART XIV — OPERATING CHECKLIST

## 45. BEFORE OPENING

- [ ] Preserve source and hash.
- [ ] Record exact span.
- [ ] Assign or resolve immutable identity.
- [ ] Separate inherited labels from blind analysis.
- [ ] State the review scope.

## 46. DURING OPENING

- [ ] Split independently failing components.
- [ ] Choose register by burden.
- [ ] Instantiate native template.
- [ ] Record definitions and dependencies.
- [ ] State exact negations.
- [ ] Build true and false worlds.
- [ ] Attach evidence with provenance.
- [ ] Name formalization boundary.
- [ ] Create serious rivals.
- [ ] Record terminus for every branch.

## 47. BEFORE AN ISOMORPHISM CLAIM

- [ ] Both structures are fully opened.
- [ ] Signatures are anonymized.
- [ ] Forward map is explicit.
- [ ] Reverse map or its absence is explicit.
- [ ] Preserved structure is named.
- [ ] Lost structure is named.
- [ ] Boundary conditions are named.
- [ ] Pairings were permuted.
- [ ] Strongest rival was tested.
- [ ] Collapse and translation behavior were tested.
- [ ] IC grade is justified.
- [ ] WHY outcome and level are recorded.
- [ ] Result is stored as bridge, not proof.

## 48. BEFORE ADMISSION

- [ ] Schema and integrity validation pass.
- [ ] Proof receipt is complete where applicable.
- [ ] Evidence limitations are visible.
- [ ] Countermodels and failures remain attached.
- [ ] Dependency blast radius is previewed.
- [ ] Candidate/admitted boundary is visible.
- [ ] Human reviewer issues explicit ruling.
- [ ] Ruling and projections receive hashes/receipts.

---

# PART XV — COMPACT FORMS

## 49. THE EQUATION

```text
ATOM
  = one canonical object of type CLAIM, EVIDENCE, PROOF, or PROCESS
  + immutable identity and provenance
  + type-native expansion
  + independent lifecycle, proof, register, IC, and WHY axes
```

```text
CLAIM    = assertion + truth conditions + register anatomy
EVIDENCE = preserved record + independence map + discrimination statement
PROOF    = premises + licensed derivation + exact conclusion + boundary
PROCESS  = versioned runnable + bounded power + failure modes + run receipt
```

```text
ISOMORPHISM CANDIDATE
  = two fully opened anonymized signatures
  + explicit maps
  + preserved and lost structure
  + boundary conditions
  + rival and permutation tests
  + IC grade
  + WHY-gate outcome
```

```text
UNIVERSAL GRAMMAR
  = admitted atoms
  + admitted serious structural bridges
  + typed edges
  + visible open boundaries
  viewed whole
```

## 50. THE PARAGRAPH VERSION

Every corpus record enters exactly as it was found, receives an immutable identity, and is assigned one primary type: claim, evidence, proof, or process. Claims open according to the burden native to their register; evidence opens into provenance, controls, independence, and discrimination; proofs open into premises, licensed steps, exact conclusions, receipts, and interpretation boundaries; processes open into reproducible operations, bounded discriminating power, failure modes, and run receipts. Typed edges state how these objects bear on one another without transferring authority they do not possess. Fully opened structures may then be compared without names. If an explicit mapping survives rivals, permutation, collapse and translation testing, IC grading, and the WHY-gate, it may enter human review as a structural bridge. Corrections remain first-class records. The universal grammar is the graph visible when all admitted objects, edges, bridges, corrections, and honest open boundaries are viewed together.

## 51. THE ONE-SENTENCE VERSION

**Every record is an atom of one of four kinds—claim, evidence, proof, or process; every atom opens along its native burden into independently accountable sub-atoms; evidence must say what the world would look like if the claim were false, proofs must print what they do not establish, processes must declare what they cannot distinguish, and isomorphisms must survive nameless mapping, loss accounting, rivals, grading, and the Why-Gate—so the universal grammar is simply the human-admitted structure that remains, with every correction and open wound still wearing its proper name.**

---

# APPENDIX A — RELATION TO THE UNIFIED GRAMMAR PIPELINE

```text
STAGE 0  RAW INTAKE              → preserve atom source and hash
STAGE 1  BLIND DISCOVERY         → produce invariant signature
STAGE 2  BLIND RECONSTRUCTION    → produce candidate grounds and inference chain
STAGE 3  CONVERGENCE CHECK       → compare signatures without names
STAGE 4  WHY-CLOSURE GATE        → explain, fail, or preserve open
STAGE 5  EMERGENT CLASSIFICATION → assign labels after analysis
STAGE 6  RECONCILIATION          → compare discovered and inherited roles
STAGE 7  ROOT-CONDITIONED PASS   → test consequences under a declared root
STAGE 8  COUNTERMODEL GAUNTLET   → attack, build, test, and preserve receipts
STAGE 9  ADMISSION & STORAGE     → human ruling into candidate or admitted graph
STAGE 10 GOVERNANCE & CORRECTION → version, correct publicly, and re-enter pipeline
```

# APPENDIX B — CURRENT REPOSITORY COMPATIBILITY NOTE

The current repository contains the claim-atom JSON-LD standard, Lane 4 atoms, Atlas records, bridge schemas, canonical nodes, proofs, papers, legacy records, proposals, runtime outputs, and generated views. This canon supplies the target expansion contract across those families. It does not declare a completed repository-wide migration.

Until migration is ruled complete:

- preserve legacy IDs;
- preserve `proof_label` and existing status fields untouched;
- add new classification axes through explicit versioned fields;
- distinguish current-schema validity from v1.0 completeness;
- generate sidecars or proposals before rewriting canonical objects;
- retain `RERUN_OWED`, `OPEN`, `UNKNOWN`, and other unresolved states;
- require human adjudication before admission or replacement.

# APPENDIX C — FINAL GOVERNING MAXIM

> **Open the claim until every burden has somewhere honest to stand. Compare structures only after their names can no longer do the work. Admit only what survives—and never erase the exact place where survival is still undecided.**
