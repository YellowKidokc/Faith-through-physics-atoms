---
type: template
id: 7Q-FORWARD
title: "The 7 Questions — Universal Classifier (Forward)"
created: 2026-03-12
updated: 2026-03-15
author: David Lowe | POF 2828
status: canonical
purpose: Classify any scientific object in any domain
usage: Apply forward to decompose and categorize
schema:
  name: "THEOPHYSICS_7Q_CLASSIFIER"
  version: "2.0"
  last_updated: 2026-03-15
  changelog:
    - date: 2026-03-15
      change: "v2.0 — Added 13 structural fields from GPT review + Opus additions: schema version, UUID standard, source authority, math object type, derivation chains, evidence classification, temporal context, debate tracking, computational links, navigation priority, change log, AI permissions, kill conditions. Added stability layer, prediction classification, collapse severity, entity subtyping, graph node ID, definition dependencies."
---

# The 7 Questions — Universal Classifier (Forward) v2.0

> For anything in the system — law, axiom, hypothesis, theory, observation, mechanism, biological claim, physics claim, moral claim — ask these seven in order. Every object carries its own death warrant (Q7). That's what makes the system scientific rather than taxonomic.

---

## Q1: What is it? (Identity)

Classifies the object itself — what it is, how stable it is, who authored it, and what math it contains.

```yaml
# ── CORE IDENTITY ──
id: ""                              # Unique ID: PREFIX-DOMAIN-SEQUENCE (e.g. TP-LAW-007, TP-AX-004, TP-NOTE-10231)
title: ""
summary: ""                         # One-sentence description

# ── ENTITY TYPE (subtyped for reasoning engines) ──
entity_type:
  epistemic: ""                     # axiom | hypothesis | theory | claim | postulate
  observational: ""                 # observation | evidence | evidence_bundle
  formal: ""                        # definition | equation | law | mechanism | operator | conservation_law
  # Legacy flat field (for backward compatibility):
  # entity_type: axiom | law | hypothesis | theory | observation | claim | mechanism | definition | equation | evidence

axiom_class: ""                     # primitive | derived | boundary | disputed

# ── STABILITY (how mature is this in the system) ──
status: ""                          # draft | candidate | provisional | stable | canonical | deprecated
last_reviewed: ""                   # YYYY-MM-DD — prevents stagnation

# ── SOURCE AUTHORITY ──
origin:
  author: "David Lowe"
  institution: "Theophysics Research Initiative"
  source_class: ""                  # theophysics_original | scripture | peer_review | historical | commentary | speculative | anonymous
  reliability_score: null           # 0-5 (5 = highest, e.g. scripture=5, speculative=1)

# ── MATHEMATICAL OBJECT (if applicable) ──
math_object:
  type: ""                          # equation | theorem | axiom | identity | operator | tensor | function | inequality | lagrangian | hamiltonian
  symbols: []                       # e.g. [χ, Λ, Ω, G, C]
  notation: ""                      # LaTeX or symbolic representation
  formalism: ""                     # equation | inequality | operator | field_equation | lagrangian | hamiltonian | lindblad | conservation

# ── GRAPH IDENTITY ──
graph_node: ""                      # e.g. TP_NODE_00214 — for Neo4j, NetworkX, knowledge graphs

# ── NAVIGATION ──
navigation:
  importance: null                  # 1-5 (5 = critical hub note)
  hub_note: false                   # true if this is a central navigation node

# ── AI GOVERNANCE ──
ai_permissions:
  edit_metadata: true
  edit_body: false
  suggest_changes: true
  auto_classify: true               # Allow AI to auto-fill fields
```

---

## Q2: What domain is it in? (Location)

Locates it in science/framework space and tracks cross-domain mappings.

```yaml
# ── DOMAIN ──
domain: ""                          # physics | biology | chemistry | consciousness | theology | moral | mathematics | information
subdomain: ""                       # e.g. quantum_mechanics, thermodynamics, christology, ethics
scale: ""                           # quantum | microscopic | cellular | organism | human | planetary | cosmological | metaphysical | multi_scale
regime: ""                          # linear | nonlinear | perturbative | non_perturbative | equilibrium | non_equilibrium | critical

# ── CROSS-DOMAIN MAPPING ──
also_maps_to:
  physics: ""                       # e.g. "entropy as sin decay"
  theology: ""                      # e.g. "grace as negentropy"
  consciousness: ""                 # e.g. "observer collapse"
  biology: ""                       # e.g. "coherence in neural systems"
  moral: ""                         # e.g. "entropy as sin"
  information: ""                   # e.g. "Shannon limit correspondence"
  mathematics: ""                   # e.g. "group symmetry breaking"

isomorphism_status: ""              # ISO-confirmed | ISO-parallel | ISO-analogy
isomorphism_target: ""              # What it maps to in the other domain

# ── TEMPORAL CONTEXT (when relevant) ──
temporal_scope:
  period: ""                        # e.g. "Second Temple Era", "Post-Resurrection", "Modern Physics"
  start: ""                         # Year or date (negative for BCE)
  end: ""                           # Year or date
```

---

## Q3: What is it claiming? (Assertion)

Classifies the claim type, strength, and framework-specific predictions.

```yaml
# ── CLAIM CLASSIFICATION ──
claim_type: ""                      # descriptive | causal | ontological | predictive | mathematical | mechanistic | normative | conservation | symmetry_claim | boundary_condition
question_type: ""                   # "Type 1: Does X hold?" | "Type 2: What is X?" | "Type 3: What grounds X?" | "Type 4: What must X be?"
precision_level: ""                 # vague | basic | detailed | mathematical | precise
certainty_type: ""                  # proven | derived | well_supported | tentative | speculative | unknown
scope: ""                           # universal | domain_specific | local | specialized

# ── MATHEMATICAL FORM (if applicable) ──
mathematical_form: ""               # The equation or formal statement (LaTeX)
units: ""                           # Physical units if applicable
dimensionality: ""                  # Dimensional analysis
symmetry_claimed: ""                # What symmetry is asserted
conservation_claimed: ""            # What is conserved

# ── THEOPHYSICS-SPECIFIC ──
coherence_prediction: ""            # increases | decreases | maintains | oscillates | none
entropy_relation: ""                # opposes | generates | neutral | coupled
grace_dependence: ""                # required | enhancing | independent | none
consciousness_role: ""              # fundamental | emergent | participatory | observer | none

# ── MASTER EQUATION LINK ──
master_eq_variable: ""              # G | M | E | S | T | K | R | Q | F | C | none
symmetry_pair: ""                   # G-Q | M-F | E-C | S-R | T-K | none
ten_laws_mapping: []                # Which of the Ten Laws does this relate to [1-10]
```

---

## Q4: What supports it? (Evidence)

Classifies evidence type, strength, independence, and experimental data.

```yaml
# ── EVIDENCE CLASSIFICATION ──
evidence_type: ""                   # empirical | experimental | observational | mathematical | logical | scriptural | historical | inferential
evidence_tier: ""                   # tier_1 | tier_2 | tier_3
sources: []
replication_status: ""              # replicated | partial | unreplicated | not_applicable

# ── EVIDENCE TYPE BREAKDOWN ──
evidence_types_present:
  mathematical: false
  scriptural: false
  historical: false
  empirical: false
  philosophical: false
  computational: false

# ── INDEPENDENCE (critical for strength assessment) ──
independent_lines: 0                # Number of independent lines of evidence (3 independent > 1 strong)

# ── EXPERIMENTAL DATA (if applicable) ──
experimental_data:
  dataset: ""                       # e.g. "PEAR-LAB", "GCP", "PROP-COSMOS"
  n_trials: null
  sigma: null                       # Statistical significance
  p_value: null
  effect_size: null

# ── MATHEMATICAL PROOF (if applicable) ──
mathematical_proof:
  method: ""                        # direct | contradiction | induction | construction | existence | uniqueness
  completeness: ""                  # complete | partial | sketch | conjectured
  verified_by: ""

# ── COMPUTATIONAL EVIDENCE ──
computational_tests:
  scripts: []                       # e.g. ["scripts/simulation_entropy.py"]
  datasets: []                      # e.g. ["datasets/gr_data.csv"]
  results: []                       # e.g. ["Mass matrix rank 8/10, energy drift < 1e-6"]
  platform: ""                      # e.g. "JAX/Colab", "Wolfram", "Python"

# ── THEOPHYSICS EXPERIMENTAL CORRELATIONS ──
PEAR_LAB: { trials: null, sigma: null, relevant: false }
GCP: { replicas: null, sigma: null, relevant: false }
PROP_COSMOS: { correlations: null, sigma: null, relevant: false }
```

---

## Q5: What does it depend on? (Dependency)

Classifies upstream structure — what must already be true for this to work.

```yaml
# ── DEPENDENCIES ──
depends_on: []                      # General dependencies (titles or UUIDs)
axiom_dependencies: []              # By axiom ID: [A1.1, A2.3]
law_dependencies: []                # By law number: [1, 5, 8]
definition_dependencies: []         # By definition ID: [Entropy_Definition, Coherence_Definition]
assumptions: []                     # Unstated but required assumptions
boundary_conditions: []             # BCs required: [BC1, BC4, BC7]

# ── DERIVATION CHAIN ──
derivation:
  derived_from: []                  # What this was derived FROM: [AX_001_EXISTENCE, LAW_01_GRACE]
  leads_to: []                      # What this derivation PRODUCES: [ME_CHI_PRIMARY]
  method: ""                        # deductive | inductive | abductive | constructive | by_contradiction

# ── PHYSICS REQUIREMENTS ──
requires_physics:
  classical_mechanics: false
  quantum_mechanics: false
  general_relativity: false
  thermodynamics: false
  information_theory: false
  consciousness_axiom: false

# ── Q0-Q12 POSITION ──
ontological_question: ""            # Which Q in the chain this depends on
preceding_survivors: []             # What must have survived before this

# ── MASTER EQUATION REQUIREMENTS ──
master_equation_required: false
LLC_required: false
ten_laws_required: []               # Which laws must hold
chi_nonzero_required: false
```

---

## Q6: What does it affect or force? (Consequence)

Classifies downstream consequences — what becomes true if this is right.

```yaml
# ── DOWNSTREAM EFFECTS ──
enables: []                         # What this makes possible
implies: []                         # What logically follows
predicts: []                        # What this predicts will be observed
related_questions: []               # Related Q-level questions
related_papers: []                  # Related Logos Papers: [P01, P06]
graph_edges_out: []                 # Outgoing graph connections

# ── PREDICTION CLASSIFICATION ──
testable_predictions:
  - prediction: ""
    prediction_type: ""             # retrodictive | predictive | structural | explanatory
    test_method: ""
    expected_result: ""
    current_status: ""              # untested | confirmed | disconfirmed | ambiguous

# ── THEOPHYSICS CONSEQUENCES ──
forces_in_framework: []             # What other axioms/laws/claims are forced true
coherence_implications: ""
entropy_implications: ""
grace_implications: ""
consciousness_implications: ""
moral_implications: ""

# ── CHAIN FORCING ──
forces_next_question: ""            # Links to next Q in chain
forces_next_axiom: ""
forces_next_paper: ""
```

---

## Q7: What would kill it? (Falsification)

Classifies death conditions, collapse severity, and kill chains.

```yaml
# ── FALSIFICATION ──
falsification: []                   # List of conditions that would destroy this
death_condition: ""                 # self_refutation | infinite_regress | empirical_contradiction | logical_incoherence | unsupported | circular
branch_status: ""                   # dead | survives | problematic | terminal
collapse_if_false: []               # What else falls if this falls
proof_status: ""                    # open | argued | derived | tested | survived_adversary

# ── COLLAPSE SEVERITY ──
collapse_scope: ""                  # local | domain | framework
total_framework_damage: ""          # minimal | moderate | severe | catastrophic

# ── SPECIFIC KILL CONDITIONS ──
kill_conditions:
  - ""                              # e.g. "Observation X falsifies Law 7"
  - ""                              # e.g. "Entropy reversal without external input"

experimental_kill:
  - experiment: ""
    result_that_kills: ""
    current_status: ""

mathematical_kill:
  - condition: ""
    would_invalidate: ""

theoretical_kill:
  - if_true: ""                     # e.g. "if consciousness is fully emergent"
    then_dies: ""

# ── MASTER EQUATION KILL ──
master_equation_kill:
  - if_variable_X_is: ""
    then: ""

# ── CASCADE FAILURE ──
cascade_failure: []                 # Everything that falls if this falls

# ── DEBATE TRACKING ──
debate:
  contested_by: []                  # Who/what contests this claim
  defense_notes: []                 # How the contest was answered
  resolution: ""                    # unresolved | resolved_in_favor | resolved_against | ongoing

# ── CHANGE LOG ──
change_log:
  - date: ""
    change: ""
```

---

## Page Flow (Forward — Classify)

1. **Name** the object → identity, stability, source, math type
2. **Locate** it in domain space → cross-domain mapping, temporal context
3. **State** what it claims → type, strength, framework predictions
4. **Show** what supports it → evidence types, independence, experimental data, computational tests
5. **Trace** what it depends on → derivation chain, definitions, BCs, Q-level position
6. **Map** what it forces downstream → predictions (classified), consequences, chain forcing
7. **Define** what kills it → death conditions, collapse severity, debate status, kill chains

> Forward: identity → location → assertion → evidence → dependency → consequence → death condition

---

## Reverse Flow (Prove — 7Q Elimination)

7. Start with what would kill it → define death conditions
6. Map what it forces → trace consequences
5. Trace dependencies → find weakest upstream link
4. Show evidence → evaluate independent lines
3. State the claim precisely → remove ambiguity
2. Locate the domain → check cross-domain survival
1. Name what survived → the thing that couldn't be killed is the thing that's true

> Reverse: death condition → consequence → dependency → evidence → assertion → location → identity of survivor

---

## Plain English

For anything in the system, ask:

1. What is this thing? Who made it? How stable is it? Does it have math?
2. Where does it belong? Does it cross domains? When does it apply?
3. What exactly is it saying? How strong is the claim?
4. Why should anyone believe it? How many independent lines of evidence? Any experiments?
5. What must already be true for it to work? What definitions does it need?
6. What becomes true if it is right? What predictions does it make?
7. What would prove it wrong? How much collapses if it dies? Who contests it?

**That is the classifier.**

---

## Compact YAML (Copy-Paste Template)

```yaml
# === Q1: IDENTITY ===
id: ""
title: ""
summary: ""
entity_type: { epistemic: "", observational: "", formal: "" }
axiom_class: ""
status: ""
last_reviewed: ""
origin: { author: "David Lowe", source_class: "", reliability_score: null }
math_object: { type: "", symbols: [], notation: "" }
graph_node: ""
navigation: { importance: null, hub_note: false }
ai_permissions: { edit_metadata: true, edit_body: false, suggest_changes: true }

# === Q2: DOMAIN ===
domain: ""
subdomain: ""
scale: ""
regime: ""
also_maps_to: {}
isomorphism_status: ""
temporal_scope: { period: "", start: "", end: "" }

# === Q3: CLAIM ===
claim_type: ""
question_type: ""
precision_level: ""
certainty_type: ""
scope: ""
mathematical_form: ""
coherence_prediction: ""
master_eq_variable: ""
symmetry_pair: ""
ten_laws_mapping: []

# === Q4: EVIDENCE ===
evidence_type: ""
evidence_tier: ""
sources: []
independent_lines: 0
replication_status: ""
evidence_types_present: { mathematical: false, scriptural: false, historical: false, empirical: false, philosophical: false, computational: false }
experimental_data: {}
computational_tests: { scripts: [], datasets: [], results: [] }
PEAR_LAB: { trials: null, sigma: null, relevant: false }
GCP: { replicas: null, sigma: null, relevant: false }

# === Q5: DEPENDENCY ===
depends_on: []
axiom_dependencies: []
law_dependencies: []
definition_dependencies: []
derivation: { derived_from: [], leads_to: [], method: "" }
ontological_question: ""
master_equation_required: false

# === Q6: CONSEQUENCE ===
enables: []
implies: []
predicts: []
testable_predictions: []
forces_next_question: ""
forces_in_framework: []

# === Q7: FALSIFICATION ===
falsification: []
death_condition: ""
branch_status: ""
collapse_scope: ""
total_framework_damage: ""
kill_conditions: []
cascade_failure: []
debate: { contested_by: [], defense_notes: [], resolution: "" }
change_log: []
```

---

*Version 2.0 — Enhanced March 15, 2026*
*Added: schema versioning, UUID standard, source authority, math object typing, derivation chains, evidence classification, temporal context, debate tracking, computational links, navigation priority, change log, AI permissions, kill conditions, collapse severity, entity subtyping, graph node ID, prediction classification, definition dependencies, compact template.*
*David Lowe + Opus — POF 2828*
