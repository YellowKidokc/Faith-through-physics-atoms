---
type: template
id: 7Q-KERNEL
title: "The 7 Questions — Universal Kernel"
created: 2026-03-23
updated: 2026-03-23
author: David Lowe | POF 2828
status: canonical
purpose: "The invariant engine behind every 7Q template. Domain-agnostic. Direction-agnostic."
usage: "Load this kernel, select a domain plugin, run forward (classify) or reverse (prove)."
version: "1.0"
parent_of:
  - 7Q_FORWARD_CLASSIFIER.md
  - 7Q_REVERSE_PROOF.md
  - 7Q_EVIDENCE_PROTOCOL.md
  - 7Q_NEW_SCIENTIFIC_METHOD.md
  - 7Q_INFERENCE_PROMPT.md
  - 7Q_PHYSICS_TEMPLATE.md
---

# The 7 Questions — Universal Kernel v1.0

> The structure inside the structure.
> Seven questions. Two directions. Every domain.
> The form never changes. The vocabulary does.

---

## Architecture

```
┌──────────────────────────────────────┐
│          7Q UNIVERSAL KERNEL         │
│  (this document — never changes)     │
│                                      │
│  Q0  Posture                         │
│  Q1  Identity    ← domain.entities   │
│  Q2  Location    ← domain.subdomains │
│  Q3  Assertion   ← domain.claim_types│
│  Q4  Evidence    ← domain.evidence   │
│  Q5  Dependency  ← domain.prereqs    │
│  Q6  Consequence ← domain.predictions│
│  Q7  Falsification ← domain.kills   │
│                                      │
│  Direction: FORWARD or REVERSE       │
│  Evidence: PS × CF (always)          │
│  Death types: 5 (always)             │
└──────────────────────────────────────┘
         │
         ├── domain: physics
         ├── domain: biology
         ├── domain: theology
         ├── domain: economics
         ├── domain: consciousness
         ├── domain: information_theory
         ├── domain: moral_philosophy
         ├── domain: history
         └── domain: theophysics (composite)
```

---

## Two Directions, Same Engine

| Forward (Classify) | Reverse (Prove) |
|---|---|
| Q1 → Q2 → Q3 → Q4 → Q5 → Q6 → Q7 | Q7 → Q6 → Q5 → Q4 → Q3 → Q2 → Q1 |
| Name it → Locate it → State it → Support it → Ground it → Force it → Kill it | Try to kill it → What survives forces → What it stands on → Evidence confirms → Claim is conclusion → Domain is earned → Identity is earned |
| Start with identity | Start with destruction |
| End with death warrant | End with what's left standing |

---

## Q0: Posture (Precondition — Not a step)

Before any question is asked, the inquirer declares:

```yaml
posture:
  worldview: ""              # What do you already believe about reality?
  epistemology: ""           # What counts as knowledge for you?
  priors: []                 # What assumptions are you carrying in?
  off_ramp: ""               # What would make you abandon this?
  # Q0 is not optional. Hidden priors corrupt every question downstream.
```

> The inquirer cannot be the ground of inquiry. Arrive with humility, not the answer.

---

## Q1: What is it? (Identity)

What you're looking at. What kind of thing it is. How stable it is.

```yaml
# ═══ INVARIANT FIELDS (every domain) ═══
id: ""                        # Unique identifier
title: ""
summary: ""                   # One sentence

entity_type: ""
  # UNIVERSAL OPTIONS:
  # axiom | hypothesis | theory | claim | postulate        (epistemic)
  # observation | evidence | evidence_bundle                (observational)
  # definition | equation | law | mechanism | principle     (formal)
  # ← domain plugin adds domain-specific entity types here

axiom_class: ""               # primitive | derived | boundary | disputed
status: ""                    # draft | candidate | provisional | stable | canonical | deprecated
origin:
  author: ""
  source_class: ""            # original | peer_review | scripture | historical | speculative
  reliability: null           # 0-5

# ═══ DOMAIN EXTENSION SLOT ═══
# domain_plugin.q1: {}        # Loaded from selected domain
```

---

## Q2: Where does it live? (Location)

What domain. What scale. Does it exist somewhere else.

```yaml
# ═══ INVARIANT FIELDS ═══
domain: ""                    # Selected from domain list
subdomain: ""                 # ← domain plugin provides options
scale: ""                     # quantum | micro | meso | macro | cosmic | meta | multi_scale

# ═══ CROSS-DOMAIN (the power move) ═══
cross_domain:
  maps_to: {}                 # domain_name: "description of mapping"
  isomorphism_status: ""      # ISO-confirmed | ISO-parallel | ISO-analogy | domain-bound
  isomorphism_target: ""      # What it maps to in the other domain

# ═══ DOMAIN EXTENSION SLOT ═══
# domain_plugin.q2: {}
```

**Cross-domain is where universality lives.** If a pattern appears in physics AND theology with the same mathematical structure, it's not a metaphor. It's a structural isomorphism. If it only appears in one domain, it might be local.

---

## Q3: What is it claiming? (Assertion)

State it precisely. Generate its negation. Remove all hedge language.

```yaml
# ═══ INVARIANT FIELDS ═══
claim:
  statement: ""               # The precise claim, no hedging
  negation: ""                # The strongest opposite claim
  boundary: ""                # What is NOT being claimed

claim_type: ""
  # UNIVERSAL OPTIONS:
  # descriptive | causal | ontological | predictive | mathematical
  # mechanistic | normative | constitutive | correlational | existential
  # ← domain plugin adds domain-specific claim types

precision_level: ""           # vague | basic | detailed | mathematical | precise
certainty_type: ""            # proven | derived | well_supported | tentative | speculative | unknown
scope: ""                     # universal | domain_specific | local | conditional

# ═══ DOMAIN EXTENSION SLOT ═══
# domain_plugin.q3: {}
```

**Precision is where most claims fail.** A vague claim can't be tested. A precise claim can be killed. Precision is not optional — it's what makes the system scientific.

---

## Q4: What supports it? (Evidence)

Three channels. They multiply. You can't compensate for zero in one by maxing another.

```yaml
# ═══ THREE-CHANNEL EVIDENCE (INVARIANT — never changes) ═══

# CHANNEL 1: PHENOMENON STRENGTH (PS) — What do we observe?
phenomenon_strength:
  score: null                 # 0.00 — 1.00
  reproducibility:            # weight: 0.40
    status: ""                # replicated | partial | unreplicated | not_applicable
    independent_replications: 0
  effect_size:                # weight: 0.30
    magnitude: ""             # negligible | small | medium | large | overwhelming
    sigma: null
  measurement_quality:        # weight: 0.30
    instrument_type: ""
    blinding: ""              # double_blind | single_blind | open | not_applicable
    systematic_bias_risk: ""  # low | moderate | high

# CHANNEL 2: EXPLANATORY DEPTH (ED) — Why does it happen?
explanatory_depth:
  score: null                 # 0.00 — 1.00
  mechanism:                  # weight: 0.40
    described: false
    formalized: false
    mechanism_type: ""        # ← domain plugin provides options
  constraints:                # weight: 0.30
    conservation_laws_respected: ""
    boundary_conditions_met: ""
    counterexamples: ""       # none_found | addressed | unaddressed
  scope:                      # weight: 0.30
    domains_explained: 0
    novel_predictions: 0

# CHANNEL 3: EXPERIENTIAL COHERENCE (EC) — Does it hold in lived reality?
experiential_coherence:
  score: null                 # 0.00 — 1.00
  consistency:                # weight: 0.25 — internal contradictions?
    self_contradictions: 0
  stability:                  # weight: 0.25 — how long has it held?
    time_tested: ""
    trend: ""                 # strengthening | stable | weakening
  transformation:             # weight: 0.25 — does it change behavior?
    measurable_behavior_change: false
  pattern:                    # weight: 0.25 — independent discovery?
    independent_discoverers: 0
    cross_cultural_presence: false

# ═══ THE FORMULAS (INVARIANT) ═══
# PS = reproducibility×0.40 + effect_size×0.30 + measurement_quality×0.30
# ED = mechanism×0.40 + constraints×0.30 + scope×0.30
# EC = consistency×0.25 + stability×0.25 + transformation×0.25 + pattern×0.25
# CF = (0.5 + 0.5×ED) × (0.5 + 0.5×EC)
# E_final = PS × CF
#
# CAPS:
# ED < 0.3 → E_final capped at 0.50 (WHY-PENALTY)
# EC < 0.1 → flag NO_LIVED_VALIDITY

# ═══ FIVE EVIDENCE GATES (INVARIANT) ═══
gates:
  E1_identity: ""             # What format? (paper, dataset, testimony, etc.)
  E2_type: ""                 # What epistemic class? (experimental, mathematical, etc.)
  E3_strength: ""             # How convincing by its own standards?
  E4_linkage: ""              # How does it connect to the claim?
  E5_vulnerabilities: []      # What flags? (WHY-PENALTY, CIRCULAR, SMALL_N, etc.)

# ═══ DOMAIN EXTENSION SLOT ═══
# domain_plugin.q4: {}        # Domain-specific evidence types, datasets, methods
```

> Three channels multiply. Unexplained evidence is incomplete evidence.
> Unlived evidence is untested evidence. Both reduce the score mathematically.

---

## Q5: What does it depend on? (Dependency)

Trace the chain. Where does it terminate?

```yaml
# ═══ INVARIANT FIELDS ═══
depends_on: []                # Titles or IDs of upstream dependencies
assumptions: []               # Unstated but required assumptions
boundary_conditions: []       # Required boundary conditions

# ═══ DEPENDENCY CHAIN ═══
derivation:
  derived_from: []            # What this was derived FROM
  leads_to: []                # What this derivation PRODUCES
  method: ""                  # deductive | inductive | abductive | constructive | by_contradiction

# ═══ TERMINUS TYPE (where does the chain end?) ═══
terminus: ""
  # axiom          — stable foundation, accepted without proof
  # brute_fact     — irreducible, no further explanation available
  # empirical      — grounded in observation, testable
  # circular       — PROBLEM: chain loops back to itself
  # infinite       — PROBLEM: chain never terminates

weakest_dependency: ""        # The single most vulnerable upstream link

# ═══ DOMAIN EXTENSION SLOT ═══
# domain_plugin.q5: {}        # Domain-specific prerequisite knowledge
```

**Terminus type is where most hidden problems live.** If the chain is circular or infinite, the claim has no foundation. If the chain ends at a brute fact, say so honestly.

---

## Q6: What does it force? (Consequence)

If this is true, what MUST follow? Not what you hope. What it forces.

```yaml
# ═══ INVARIANT FIELDS ═══
enables: []                   # What this makes possible
implies: []                   # What logically follows
predicts: []                  # What this predicts will be observed

# ═══ TESTABLE PREDICTIONS (INVARIANT STRUCTURE) ═══
testable_predictions:
  - prediction: ""
    prediction_type: ""       # retrodictive | predictive | structural | explanatory
    test_method: ""
    expected_result: ""
    current_status: ""        # untested | confirmed | disconfirmed | ambiguous

# ═══ CROSS-DOMAIN FORCING ═══
forces_in_other_domains: []   # What becomes true in other domains if this is true
cannot_avoid: []              # Consequences that follow whether you like them or not

# ═══ COMPETING MODELS ═══
competing_models:
  exclusive_to_this_claim: false
  competitors:
    - theory: ""
      explains_same_evidence: ""  # fully | partially | weakly
      what_it_misses: ""
      decisive_test: ""

# ═══ DOMAIN EXTENSION SLOT ═══
# domain_plugin.q6: {}
```

**Claims with no testable consequences are not scientific.** Claims whose consequences are identical to a competitor's are not distinctive. Both are failure modes.

---

## Q7: What would kill it? (Falsification)

Five ways anything can die. These are universal. They apply to physics, theology, biology, economics, history — everywhere.

```yaml
# ═══ THE FIVE DEATH TYPES (INVARIANT — UNIVERSAL) ═══
death_tests:
  self_refutation:            # The claim, if true, proves itself false
    live: false
    description: ""
    survived: false
  infinite_regress:           # The justification chain never terminates
    live: false
    description: ""
    survived: false
  empirical_contradiction:    # Observable facts contradict the claim
    live: false
    description: ""
    survived: false
  logical_incoherence:        # The claim is internally contradictory (A and not-A)
    live: false
    description: ""
    survived: false
  explanatory_failure:        # A competitor explains the same evidence better
    live: false
    description: ""
    survived: false

# ═══ KILL CONDITIONS ═══
kill_conditions: []           # Specific conditions that would destroy this
branch_status: ""             # dead | survives | problematic | terminal

# ═══ CASCADE ANALYSIS ═══
collapse_if_false: []         # What else falls if this falls
collapse_scope: ""            # local | domain | framework
total_damage: ""              # minimal | moderate | severe | catastrophic

# ═══ ROBUSTNESS ═══
proof_status: ""              # open | argued | derived | tested | survived_adversary
robustness: ""                # weak | fragile | grounded | strong | constrained
robustness_note: ""           # 2-3 sentence assessment

# ═══ DOMAIN EXTENSION SLOT ═══
# domain_plugin.q7: {}        # Domain-specific kill conditions
```

> Every object carries its own death warrant. That's what makes this scientific, not taxonomic.

---

## Failure Catalogue (Universal)

Every claim fails in one of these ways. Domain doesn't matter.

| # | Failure Type | Where Detected | What It Looks Like |
|---|---|---|---|
| 1 | **Vague claim** | Q3 | Can't be tested because it can't be stated precisely |
| 2 | **No negation** | Q3 | If you can't state what would be false, the claim is empty |
| 3 | **Zero ED** | Q4 | Describes THAT but never explains WHY |
| 4 | **Zero EC** | Q4 | Lives only in theory, never in reality |
| 5 | **Circular dependency** | Q5 | A depends on B depends on A |
| 6 | **Infinite regress** | Q5/Q7 | Justification chain never bottoms out |
| 7 | **No predictions** | Q6 | If true, nothing follows — unfalsifiable |
| 8 | **Generic predictions** | Q6 | Predictions are the same as competitor's |
| 9 | **Self-refutation** | Q7 | The claim destroys itself |
| 10 | **Empirical contradiction** | Q7 | Reality says no |
| 11 | **Logical incoherence** | Q7 | Claims A and not-A |
| 12 | **Explanatory failure** | Q7 | A simpler model does the same job |
| 13 | **Hidden priors** | Q0 | Unstated assumptions corrupt analysis |
| 14 | **Confirmation bias** | Q4/E5 | Only supporting evidence sought |
| 15 | **Selection bias** | Q4/E5 | Evidence cherry-picked |
| 16 | **P-hacking** | Q4/E5 | Statistical significance gamed |
| 17 | **Single source** | Q4/E5 | One lab, one dataset, one author |
| 18 | **Survivorship bias** | Q4/E5 | Failures not counted |
| 19 | **Domain isolation** | Q2 | Pattern appears nowhere else — may be local artifact |
| 20 | **False isomorphism** | Q2 | Surface similarity, different structure underneath |

---

## Domain Plugin Interface

Every domain plugin provides these extension fields. The kernel loads them into the `domain_plugin.*` slots above.

```yaml
# ═══ DOMAIN PLUGIN SCHEMA ═══
domain_plugin:
  name: ""                    # e.g. "physics", "biology", "theology"
  version: ""

  q1:                         # Identity extensions
    entity_types: []          # Domain-specific entity types
    subtypes: {}              # Further classification

  q2:                         # Location extensions
    subdomains: []            # Available subdomains
    scales: []                # Available scales
    regimes: []               # Available regimes (if applicable)

  q3:                         # Assertion extensions
    claim_types: []           # Domain-specific claim types
    formal_fields: {}         # Domain-specific formal fields (equations, units, etc.)

  q4:                         # Evidence extensions
    evidence_types: []        # Domain-specific evidence types
    datasets: {}              # Known datasets
    methods: []               # Common experimental methods

  q5:                         # Dependency extensions
    prerequisite_knowledge: {}# What domain knowledge is required
    foundational_theories: [] # Base theories the domain rests on

  q6:                         # Consequence extensions
    prediction_types: []      # Domain-specific prediction categories
    consequence_fields: {}    # Domain-specific consequence tracking

  q7:                         # Falsification extensions
    kill_types: []            # Domain-specific kill conditions
    cascade_map: {}           # Domain-specific cascade relationships
```

---

## Truth Score Integration

```yaml
# How 7Q feeds into the Truth Score (T)
truth_score_contribution:
  S: { from: "Q7 — kill conditions survived" }
  E: { from: "Q4 — E_final = PS × CF" }
  L: { from: "Q3 precision + Q4 explanatory depth" }
  D: { from: "Q5 — dependency chain depth" }
  P: { from: "Q6 — predictions generated" }
  C: { from: "Q2 — cross-domain coherence" }

  T: null                     # (S + E + L + D + P + C) / 6
  T_enhanced: null            # T × (0.6 + 0.4 × 7Q_composite)

  confidence_class: ""
    # ESTABLISHED       — T >= 0.85
    # WELL_SUPPORTED    — T >= 0.65
    # TENTATIVE         — T >= 0.40
    # SPECULATIVE       — T >= 0.15
    # UNSUPPORTED       — T < 0.15
```

---

## The Core Principle

Seven questions forward: **classify** anything.
Seven questions reversed: **prove** anything.
Same engine. Two directions. Every domain.

The form never changes. The vocabulary does.
The mechanism is hidden. The user sees only the questions.

> A claim survives iff it is:
> (1) sincerely stated (Q0),
> (2) precisely defined (Q1, Q3),
> (3) connected to other truths (Q2, Q6),
> (4) evidentially grounded with explanatory depth (Q4, Q5), and
> (5) robust against all five death types (Q7).
>
> This applies to God, gravity, goodness, governance, genetics, and grief.
> The questions are the same. The answers are domain-specific.
> That's the whole system.

---

*David Lowe | POF 2828 | Theophysics*
*7Q Universal Kernel v1.0 | March 23, 2026*
*"The structure inside the structure."*
