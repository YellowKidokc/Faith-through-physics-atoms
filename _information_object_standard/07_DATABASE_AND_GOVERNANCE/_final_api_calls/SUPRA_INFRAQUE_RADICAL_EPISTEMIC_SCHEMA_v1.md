# SUPRA INFRAQUE
## Radical Epistemic Storage Schema — Version 1

**Purpose:** Replace a file-centered archive with an ontology-first, question-driven epistemic graph capable of representing the full Theophysics corpus without collapsing theology into physics, treating mathematics as empirical proof, or hiding assumptions inside classifications.

**Status:** Proposed governing architecture. This document defines what the system must preserve. The neutral inquiry canon should be derived from these required information slots only after this architecture is accepted.

---

## 1. The Radical Redesign in One Sentence

The file is no longer the unit of knowledge: the system stores independently identifiable **questions, statements, axioms, constitutive disclosures, definitions, derivations, bridges, evidence units, countermodels, predictions, protocols, tests, results, and interpretations**, while files remain immutable provenance containers that may contain any number of those objects.

This separation is essential because:

- one file may contain many logically different claims;
- one claim may occur across many files;
- a sentence may function as a definition in one argument and a premise in another;
- a mathematical expression may formalize a claim without establishing that the claim describes nature;
- an empirical result may support a model without proving its metaphysical interpretation;
- an axiom may be progressively unpacked without additional axioms being silently introduced;
- a bridge between domains is itself a claim requiring justification and testing.

The existing file-intelligence design remains useful, but only as the **physical and provenance layer** beneath the epistemic graph.

---

## 2. Governing Commitments

### 2.1 Ontology before classification

The system first asks what kind of thing a record is and what it asserts. It does not begin by forcing the record into a scientific, theological, mathematical, or philosophical verdict.

### 2.2 Questions before inferred answers

Neutral questions define the information slots. They must not contain the answer they are supposed to discover. A question may specify a contrast, test, or required distinction; it may not presuppose the preferred conclusion.

### 2.3 Classification is multidimensional

No single label can represent both what a statement **does** and what it is **about**. Logical role and ontological domain are independent axes. Additional axes record warrant, status, relation to A0, ontological mode, and testability.

### 2.4 Unpacking is not addition

For the Theophysics corpus, **A0 is one content-rich Triune axiom**. Trinity, Being, Truth, Goodness, Love, relational distinction, and the positive fruits are not to be stored as independent axioms merely because exposition discusses them separately. They are constitutive disclosures or semantic unpackings of the one axiom unless an argument explicitly posits another independent primitive.

### 2.5 A bridge is a claim

No transition from theology to ontology, ontology to information, information to mathematics, mathematics to physics, or physics to consciousness is automatic. Each cross-domain transition must be stored as a bridge dossier with its mapping, preserved structure, assumptions, loss, direction, and tests.

### 2.6 Evidence is not interpretation

Observations, measurements, quotations, datasets, and formal results are stored separately from what an author believes they mean. Competing interpretations may cite the same evidence unit.

### 2.7 Good and privation are not forced into symmetry

The schema must be capable of representing the thesis that truth is prior to falsehood, life to death, and good to corruption. Negative states may be classified as privative, parasitic, corruptive, or derivative rather than as co-original positive substances. This is a representational capability, not a database-imposed conclusion.

### 2.8 Append, assess, supersede—do not silently overwrite

Historical classifications and assessments remain visible. Corrections create new versions or superseding records so that the development of the theory can be audited.

---

## 3. The Architecture: Six Interlocking Planes

| Plane | Stores | Governing question |
|---|---|---|
| Provenance | artifacts, versions, spans, authors, dates, hashes | Where exactly did this come from? |
| Inquiry | neutral questions, runs, responses, leakage checks | What was asked, under what framing, and what appeared? |
| Semantic | statements and other epistemic objects | What exactly is being said or represented? |
| Inferential | typed relationships and warrants | How does one object depend on or affect another? |
| Evaluation | evidence, formalization, bridges, tests, objections | What licenses, limits, tests, or defeats it? |
| Governance | versions, statuses, conflicts, decisions, audit trail | Who changed what, why, and with what authority? |

These are logical planes, not necessarily separate databases. PostgreSQL can implement the authoritative store; a graph projection can support traversal and visualization; vector indexes can assist retrieval but must never become the source of truth.

---

## 4. Core Record: The Epistemic Object

Every meaningful unit receives a stable object identity independent of its filename and wording.

### 4.1 Required core fields

| Field | Meaning |
|---|---|
| `object_id` | Immutable machine identity, preferably UUID/ULID |
| `human_code` | Stable readable code such as `A0`, `Q-014`, `CLM-208`, `BR-031` |
| `object_type` | Primary logical object type |
| `canonical_text` | Smallest complete statement or definition |
| `scope` | Universe, framework, model, population, time, or conditions covered |
| `modality` | Necessary, possible, actual, probable, conditional, normative, interrogative |
| `polarity` | Affirmed, denied, suspended, alternative |
| `owner_framework` | Framework in which the object is defined |
| `status` | Draft, proposed, active, contested, supported, defeated, superseded, retired |
| `created_by` / `created_at` | Authorship and time |
| `version` | Semantic version of this object |

### 4.2 Object types

The initial controlled vocabulary should include:

| Family | Types |
|---|---|
| Foundations | `AXIOM`, `CONSTITUTIVE_DISCLOSURE`, `PRIMITIVE`, `DEFINITION`, `DISTINCTION` |
| Inquiry | `QUESTION`, `QUESTION_FAMILY`, `RESPONSE`, `OBSERVATION` |
| Reasoning | `CLAIM`, `PREMISE`, `LEMMA`, `THEOREM`, `COROLLARY`, `DERIVATION`, `INFERENCE_RULE` |
| Representation | `MODEL`, `FORMAL_EXPRESSION`, `ANALOGY`, `METAPHOR`, `INTERPRETATION` |
| Connection | `BRIDGE`, `TRANSLATION`, `CORRESPONDENCE`, `IDENTITY_CLAIM` |
| Evaluation | `EVIDENCE_UNIT`, `PREDICTION`, `PROTOCOL`, `TEST`, `RESULT`, `FALSIFIER`, `DEFEATER` |
| Critique | `OBJECTION`, `COUNTEREXAMPLE`, `COUNTERMODEL`, `ALTERNATIVE_EXPLANATION`, `LIMITATION` |
| Synthesis | `LAW`, `PRINCIPLE`, `SYNTHESIS`, `APPLICATION` |

The primary type answers “what does this record do?” Secondary logical-role tags are allowed, but one primary type is mandatory in each argument context.

---

## 5. Multiaxial Classification

Classification is stored as assignments, not hard-coded columns, so one object can carry multiple domains and can be reassessed without mutation.

### 5.1 Independent axes

| Axis | Example terms |
|---|---|
| Logical role | definition, axiom, theorem, model, bridge, prediction, interpretation |
| Ontological domain | mathematical, physical, informational, theological, consciousness, moral, cosmological, relational, ontological, epistemic |
| Relation to A0 | constitutive of, disclosed by, derived from, compatible with, independent of, opposed to, unassessed |
| Ontological mode | positive-prior, dependent-positive, relational, privative, corruptive, operational, representational, formal-only, empirical-candidate |
| Warrant type | axiomatic, deductive, abductive, inductive, testimonial, revelatory, phenomenological, empirical, pragmatic, analogical |
| Formal status | unformalized, notation-only, defined, derived, proven-relative-to-premises, simulated, dimensionally checked |
| Empirical status | non-empirical, operationalizable, predicted, protocol-ready, tested, replicated, disconfirmed, underdetermined |
| Epistemic status | stipulated, inferred, observed, interpreted, contested, provisionally accepted, rejected |
| Bridge strength | metaphorical, heuristic, structural analogy, homomorphism, isomorphism, causal proposal, identity claim |

Each assignment records classifier, date, confidence, rationale, and source. Conflicting assignments may coexist until adjudicated.

### 5.2 Primary and secondary domains

Dual classification is expected. For example, a statement may have:

- primary logical role: `BRIDGE`;
- primary domain: `INFORMATIONAL`;
- secondary domains: `THEOLOGICAL`, `PHYSICAL`;
- warrant: `ABDUCTIVE`;
- empirical status: `OPERATIONALIZABLE`;
- bridge strength: `CAUSAL_PROPOSAL`.

The system must never convert these independent facts into one opaque label.

---

## 6. A0 and Constitutive Disclosure

### 6.1 Required representation

`A0` is stored as one `AXIOM` object. Its irreducible content is represented through `CONSTITUTIVE_DISCLOSURE` objects attached by typed relationships.

Illustrative structure:

| Object | Type | Relation |
|---|---|---|
| A0 | AXIOM | root declaration of the Triune God |
| Trinity | CONSTITUTIVE_DISCLOSURE | `CONSTITUTIVE_OF A0` |
| Being / “I AM” | CONSTITUTIVE_DISCLOSURE | `CONSTITUTIVE_OF A0` |
| Truth | CONSTITUTIVE_DISCLOSURE | `CONSTITUTIVE_OF A0` |
| Goodness | CONSTITUTIVE_DISCLOSURE | `CONSTITUTIVE_OF A0` |
| Love | CONSTITUTIVE_DISCLOSURE | `CONSTITUTIVE_OF A0` |
| Relational distinction without division | CONSTITUTIVE_DISCLOSURE | `CONSTITUTIVE_OF A0` |
| Positive fruits or dispositional expressions | CONSTITUTIVE_DISCLOSURE or DERIVED EXPRESSION, as argued | linked with explicit warrant |

This allows the corpus to say more about A0 over time without pretending that A0 began semantically empty. It also permits audit of which contents are claimed as constitutive and which are genuinely derived.

### 6.2 Mandatory A0 audit fields

Every proposed disclosure must answer:

- Is this constitutive, definitional, entailed, inferred, analogical, or merely associated?
- Could A0 remain numerically the same axiom if this content were denied?
- Is the disclosure textually declared, logically required, traditionally received, or introduced by the present model?
- What later derivations depend on it?
- Does moving it into or out of A0 change the theory’s conclusions?

These questions do not decide the theology. They prevent semantic smuggling and semantic amputation alike.

---

## 7. Typed Relations: The Inference Graph

Objects connect through typed, versioned edges. An edge is never “just a link”; it states a relationship and therefore requires its own provenance and warrant.

### 7.1 Initial edge vocabulary

| Relation group | Edge types |
|---|---|
| Constitution | `CONSTITUTIVE_OF`, `DISCLOSES`, `DEFINES`, `HAS_PART`, `INSTANTIATES` |
| Inference | `DEPENDS_ON`, `DERIVED_FROM`, `ENTAILS`, `IMPLIES`, `COROLLARY_OF`, `USES_RULE` |
| Evidence | `SUPPORTS`, `WEAKENS`, `CONTRADICTS`, `UNDERDETERMINES`, `EXPLAINS`, `PREDICTS` |
| Testing | `TESTS`, `FALSIFIES_IF`, `CONFIRMS_IF`, `IMPLEMENTS_PROTOCOL`, `PRODUCES_RESULT` |
| Bridging | `MAPS_FROM`, `MAPS_TO`, `PRESERVES`, `LOSES`, `TRANSLATES`, `CORRESPONDS_TO` |
| Critique | `OBJECTS_TO`, `COUNTEREXAMPLE_TO`, `COUNTERMODEL_TO`, `DEFEATS`, `LIMITS` |
| Governance | `DUPLICATES`, `REFINES`, `SUPERSEDES`, `RETRACTS`, `CONFLICTS_WITH` |

### 7.2 Edge requirements

Every consequential edge records:

- source and target object versions;
- direction;
- relation type;
- whether it claims necessity, sufficiency, probability, compatibility, or analogy;
- stated warrant;
- supporting source spans;
- assumptions required;
- confidence and status;
- defeat conditions.

The **derivation subgraph** must be acyclic. Other relations may form cycles, but cycles cannot masquerade as proofs.

---

## 8. Provenance Plane

The prior file schema becomes the foundation for traceability.

### 8.1 Core records

| Record | Function |
|---|---|
| `artifact` | Stable identity for a document, transcript, dataset, image, codebase, or recording |
| `artifact_version` | Immutable byte-level version with hash, date, author, and origin |
| `source_span` | Exact page, line, paragraph, timestamp, cell, or byte-range locator |
| `object_occurrence` | Links an epistemic object to one or more source spans |
| `agent_run` | Human or AI extraction, classification, transformation, or evaluation event |

The filename is metadata, never identity. File renaming cannot alter epistemic objects. Every quotation and evidence claim must resolve to a source span whenever the medium permits it.

---

## 9. Inquiry Plane

The inquiry layer records not only answers but how the answer was elicited.

### 9.1 Question definition

A `QUESTION` record includes:

- canonical neutral wording;
- question family;
- target information slot;
- allowed answer shape;
- forbidden presuppositions;
- known framing risks;
- domain scope;
- whether the question operates above, within, or below the target system;
- follow-up triggers;
- adjudication rule.

### 9.2 Inquiry runs

Each run stores:

- exact question version and order;
- context supplied before the question;
- model or human respondent;
- temperature/settings where applicable;
- blinded or unblinded condition;
- response verbatim;
- extracted candidate objects;
- leakage, leading-language, and anchoring assessments;
- reproducibility receipts.

This makes it possible to compare framed and unframed inquiry without treating either result as automatically authoritative.

### 9.3 Three inquiry levels

| Level | Function |
|---|---|
| Supra-systemic | asks what must be true for the system, distinction, inquiry, or meaning to be possible |
| Intra-systemic | asks what the proposed system claims and how its parts relate |
| Infra-systemic | asks what observable, formal, experiential, or behavioral consequences occur within implementations |

The method may therefore be named **Methodus Veritatis Supra Infraque** (“the method of truth above and below”), with **Supra Infraque** as its operational name.

---

## 10. Evidence Plane

Evidence must be atomized enough that two interpretations can refer to the same observation without duplicating or rewriting it.

### 10.1 Evidence unit

Required fields include:

- exact content or observation;
- source span and custody;
- evidence kind;
- collection method;
- sample, population, apparatus, or textual corpus;
- uncertainty and known limitations;
- independence from other evidence units;
- replication status;
- direction of evidential effect;
- claims it bears on;
- interpretations applied to it.

### 10.2 Evidence kinds

The system must distinguish at least:

- empirical measurement;
- phenomenological report;
- historical/documentary evidence;
- textual/scriptural evidence;
- formal proof relative to premises;
- simulation output;
- testimony;
- case study;
- conceptual entailment;
- absence or failed prediction.

This avoids scientism and category inflation simultaneously: testimonial or revelatory warrant is not deleted, while it is also not mislabeled as laboratory replication.

---

## 11. Formalization Plane

Mathematical notation is stored separately from the proposition it expresses.

A formal expression records:

- symbols and typed definitions;
- units and dimensions where applicable;
- domain and codomain;
- assumptions and boundary conditions;
- derivation or proof artifact;
- computability and implementation status;
- sensitivity to parameter choices;
- semantic interpretation;
- claim(s) formalized;
- whether the expression is definitional, descriptive, predictive, or merely illustrative.

Formal validity establishes what follows from premises and rules. It does not by itself establish that the premises describe physical reality or that one metaphysical interpretation is uniquely correct.

---

## 12. Bridge Dossiers

The bridge layer is mandatory for every cross-register transition.

### 12.1 Bridge record

Each bridge must store:

| Field | Requirement |
|---|---|
| Source register | The originating vocabulary/domain |
| Target register | The receiving vocabulary/domain |
| Mapping rule | Exact correspondence or transformation |
| Preserved structure | Relations, order, symmetry, quantity, causality, or meaning retained |
| Lost structure | What the mapping omits or distorts |
| Directionality | One-way, two-way, reversible, or non-reversible |
| Strength | Metaphor through identity claim |
| Assumptions | Background premises needed |
| Alternatives | Rival mappings or interpretations |
| Discriminators | Findings that favor this bridge over rivals |
| Defeat conditions | What would break the bridge |
| Validation status | Proposed, formalized, tested, supported, defeated |

### 12.2 Bridge rule

Reusing the same word across two domains does not create a bridge. A bridge exists only when the mapping and its preservation claim are explicit.

Examples requiring dossiers include:

- Logos → information;
- coherence → moral goodness;
- grace → recovery operator;
- relational Trinity → relational ontology;
- consciousness measure → personhood;
- mathematical invariant → physical law;
- physical behavior → theological interpretation.

---

## 13. Testing and Defeat

A claim may be meaningful without being empirically testable, but its mode of evaluation must be explicit.

### 13.1 Test chain

`CLAIM → PREDICTION → OPERATIONALIZATION → PROTOCOL → TEST RUN → RESULT → INTERPRETATION → ASSESSMENT`

Each stage is a separate object. This prevents a theoretical prediction from being reported as an observed result or an observed result from being reported as a unique interpretation.

### 13.2 Defeat conditions

Every load-bearing object must declare the relevant forms of defeat:

- logical contradiction;
- countermodel;
- failed entailment;
- empirical falsifier;
- unsuccessful replication;
- superior alternative explanation;
- category error;
- bridge failure;
- source/provenance failure;
- scope violation;
- semantic equivocation.

“Not applicable” is acceptable only with a reason.

---

## 14. Assessment and Disagreement

Assessments are append-only records containing assessor, criteria, rationale, confidence, scope, and date. They do not overwrite the object assessed.

The system must support:

- multiple confidence estimates;
- theological, philosophical, formal, and empirical reviews by different standards;
- minority and dissenting assessments;
- declared worldview or framework assumptions;
- conflicts awaiting adjudication;
- explicit decisions with reasons;
- later reversal without loss of history.

The database must not settle truth by vote. It records arguments, evidence, and assessments so judgments can be audited.

---

## 15. Minimal Relational Implementation

The following normalized tables are sufficient for a first implementation:

| Table | Purpose |
|---|---|
| `artifacts` | stable source identities |
| `artifact_versions` | immutable source versions and hashes |
| `source_spans` | precise source locators |
| `epistemic_objects` | universal typed object registry |
| `object_versions` | canonical text and scoped semantic versions |
| `object_occurrences` | object-to-source-span links |
| `relation_types` | controlled edge vocabulary |
| `relations` | versioned, warranted edges |
| `classification_axes` | independent dimensions |
| `classification_terms` | controlled values within axes |
| `classification_assignments` | multivalued, assessed classifications |
| `question_definitions` | neutral question specifications |
| `inquiry_runs` | exact contexts, respondents, settings, and receipts |
| `question_responses` | verbatim answers and extracted candidates |
| `evidence_units` | atomic observations and evidentiary records |
| `evidence_links` | claim-direction-strength relationships |
| `formal_expressions` | math, types, units, premises, semantics |
| `proof_artifacts` | derivations, checks, countermodels |
| `bridge_dossiers` | cross-domain mappings and limitations |
| `bridge_tests` | invariance, discrimination, and failure checks |
| `protocols` | reproducible test definitions |
| `test_runs` | execution circumstances and receipts |
| `test_results` | raw and processed outcomes |
| `assessments` | append-only judgments |
| `conflict_sets` | explicit incompatible alternatives |
| `change_events` | audit trail and supersession decisions |

Use JSONB only for genuinely extensible secondary metadata. Identities, types, relations, statuses, provenance, and critical evaluation fields must remain queryable and constrained.

---

## 16. Validation Rules

The first implementation should reject or flag:

1. a claim with no canonical text or scope;
2. an evidence citation with no retrievable source locator;
3. a derivation cycle;
4. a cross-domain edge lacking a bridge dossier;
5. a theorem lacking explicit premises;
6. an empirical conclusion supported only by notation;
7. a “proven” status without a declared proof system or protocol;
8. a question whose wording contains its expected answer;
9. a result record that contains interpretation but no raw observation link;
10. a constitutive disclosure treated as an independent axiom without adjudication;
11. a new A0 disclosure with no semantic-addition audit;
12. a classification that combines logical role and domain into one untraceable label;
13. a negative ontological state assumed co-original merely because it has a positive noun;
14. an assessment that overwrites dissent or prior status;
15. a bridge based only on lexical similarity.

---

## 17. Migration from the Existing Corpus

Migration should proceed in this order:

### Phase 1 — Freeze and register sources

Hash every artifact version. Preserve filenames and existing codes as aliases. Do not reorganize content during registration.

### Phase 2 — Extract without adjudicating

Segment documents into candidate questions, declarations, definitions, claims, equations, bridges, evidence units, predictions, objections, and limitations. Retain verbatim spans.

### Phase 3 — Normalize objects

Merge true duplicates while preserving occurrences. Split compound claims. Assign stable readable codes independent of file order.

### Phase 4 — Reconstruct A0

Register A0 once. Classify its candidate content as constitutive disclosure, definition, entailment, inference, or later association. Record disagreements rather than resolving them through import order.

### Phase 5 — Build the dependency graph

Add explicit edges, then identify unsupported transitions, circular derivations, hidden premises, and load-bearing bridges.

### Phase 6 — Attach evaluation

Connect evidence, formal expressions, tests, countermodels, limitations, and defeat conditions.

### Phase 7 — Run neutral inquiry

Only after the slots and validation rules are frozen should the unbiased question canon be finalized and executed. This prevents the desired answer from redesigning the questions after the fact.

---

## 18. The Question-Derivation Contract

The next document—the neutral inquiry canon—must be generated from the schema, not from the preferred conclusions.

For every required field or validation rule, the canon must contain one or more questions that can populate or test it. Questions will therefore be organized into these families:

1. identity and individuation;
2. logical role;
3. domain and scope;
4. modality and necessity;
5. semantic content and hidden assumptions;
6. constitution versus derivation;
7. dependency and inference;
8. positive priority, dependence, and privation;
9. formalization and mathematical status;
10. bridge legitimacy;
11. evidence and provenance;
12. operationalization and testing;
13. alternatives, countermodels, and defeat;
14. interpretation and underdetermination;
15. coherence across supra-, intra-, and infra-systemic levels;
16. A0-specific semantic integrity;
17. reproducibility and framing sensitivity.

Each question must specify:

- the slot it populates;
- why the slot is necessary;
- neutral canonical wording;
- prohibited leading variants;
- admissible response forms;
- follow-up questions triggered by each response type;
- how disagreement is recorded;
- whether the question is universal or Theophysics-specific.

This contract ensures that “what the questions reveal” remains distinguishable from what the framework hoped they would reveal.

---

## 19. Decisions Required Before Version 1 Is Frozen

Only five architectural decisions remain:

1. **A0 disclosure boundary:** Which properties are asserted as strictly constitutive, and which are derived expressions?
2. **Canonical codes:** Whether readable identifiers follow families such as `AX`, `DSC`, `Q`, `CLM`, `BR`, `EVD`, and `TST`.
3. **Bridge threshold:** Which cross-domain relations require a full dossier versus a lighter translation record?
4. **Assessment vocabulary:** Whether “supported,” “established,” and “proven” receive domain-specific definitions.
5. **Question freeze procedure:** How blind, adversarial, and repeated runs are versioned before results are reviewed.

These are governance decisions. They should be made explicitly rather than embedded in software defaults.

---

## 20. Acceptance Criteria

The redesign is successful if it can represent all of the following without contradiction or loss:

- one Triune A0 with many inseparable disclosures but no accidental axiom multiplication;
- a question asked before a claim exists, and the later claim it reveals;
- the same statement serving different logical roles in different arguments;
- dual or multiple ontological domains;
- a theological claim evaluated as theological without being dismissed for not being physics;
- a physical claim denied empirical status until operationalized and tested;
- a mathematical result valid relative to premises without metaphysical overreach;
- good as positive-prior and evil as a proposed privation, while retaining room for rival models;
- several interpretations of one evidence unit;
- a bridge that succeeds structurally but fails as an identity claim;
- uncertainty, objection, defeat, correction, and supersession without erasing history;
- exact reconstruction of why any conclusion was reached.

---

## Conclusion

The radical change is not a larger taxonomy. It is a change in what counts as a stored thing.

Files store expressions. The epistemic graph stores the objects expressed, the questions that elicited them, the relations claimed among them, and the warrants and tests by which they may be judged. This architecture can honor the theological content of the theory, submit every bridge to disciplined examination, and prevent either scientific or theological vocabulary from receiving an automatic verdict.

Once this architecture is accepted, the next proper step is to produce the **Supra Infraque Neutral Inquiry Canon** directly from Section 18 and use it first on A0 and its proposed constitutive disclosures.
