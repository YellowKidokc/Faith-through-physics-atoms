---
type: template
id: 7Q-EVIDENCE-PROTOCOL
title: "The 7Q Evidence Protocol — Comprehensive Classification"
created: 2026-03-21
updated: 2026-03-21
author: David Lowe | POF 2828
status: canonical
purpose: "Rigorously classify, weigh, and audit any evidence claim"
usage: "Apply to any paper, claim, or evidence bundle entering the system"
schema:
  name: "THEOPHYSICS_EVIDENCE_PROTOCOL"
  version: "1.0"
  last_updated: 2026-03-21
---

# The 7Q Evidence Protocol — Comprehensive Classification v1.0

> Evidence without explanation is incomplete. Explanation without evidence is speculation.
> This template classifies evidence across three channels, five gates, and twelve
> philosophical dimensions. Every score is traceable. Every gap is named.

---

## §1 — Philosophical Classification

Before evaluating evidence, classify the claim it supports. This determines
which evidence types are appropriate and which are irrelevant.

```yaml
# ═══ ONTOLOGICAL STATUS ═══
# What kind of thing is being claimed?
ontological_status: ""
  # foundational     — claims about what exists at bedrock level
  # derived          — depends on other claims being true first
  # structural       — claims about the architecture of reality
  # processual       — claims about how things change over time
  # relational       — claims about how things connect
  # dispositional    — claims about what things CAN do (not what they ARE)

# ═══ EPISTEMOLOGICAL MODE ═══
# How do we know this? What justification type?
epistemological_mode: ""
  # deductive        — follows necessarily from premises (math, logic)
  # inductive        — generalized from specific observed cases
  # abductive        — inference to best explanation
  # transcendental   — conditions for possibility (what MUST be true for X to be possible)
  # empirical        — grounded in direct measurement or observation
  # testimonial      — based on witness/historical testimony
  # revelatory       — based on claimed divine revelation (scripture)
  # computational    — based on simulation, numerical verification
  # phenomenological — based on first-person lived experience

# ═══ INQUIRY TYPE ═══
# What is the claim doing?
inquiry_type: ""
  # causal           — X causes Y
  # descriptive      — X is like this
  # predictive       — if X then Y
  # normative        — X ought to be
  # mechanistic      — X works by doing Y
  # constitutive     — X is partially constituted by Y
  # correlational    — X and Y co-occur
  # existential      — X exists (or doesn't)

# ═══ SCOPE ═══
scope: ""
  # universal        — applies everywhere, always
  # domain_specific  — applies within one field
  # local            — applies to a specific case or situation
  # conditional      — applies only under stated conditions

# ═══ CROSS-DOMAIN CLASSIFICATION ═══
cross_domain_status: ""
  # ISO-CONFIRMED    — same equations/structure holds in both domains (formally verified)
  # ISO-PARALLEL     — qualitative structural match, math mapping not demonstrated
  # ISO-ANALOGY      — surface similarity, different structure underneath
  # DOMAIN-BOUND     — no cross-domain presence claimed
  # BRIDGE           — explicitly claims connection between two or more domains

# ═══ EVIDENCE BURDEN ═══
# What SHOULD support this kind of claim?
evidence_burden:
  requires_mathematical_proof: false
  requires_empirical_data: false
  requires_historical_documentation: false
  requires_scriptural_support: false
  requires_computational_verification: false
  requires_peer_review: false
  requires_replication: false
  requires_cross_domain_confirmation: false
```

---

## §2 — Three-Channel Evidence Protocol

Every piece of evidence is scored across three independent channels.
They MULTIPLY, not add. You can't compensate for zero in one channel
by maxing another.

```yaml
# ═══════════════════════════════════════════════
# CHANNEL 1: PHENOMENON STRENGTH (PS)
# What do we observe? How reliable is the observation?
# ═══════════════════════════════════════════════
phenomenon_strength:
  score: null                       # 0.00 — 1.00

  # ── Reproducibility (weight: 0.40) ──
  reproducibility:
    score: null
    status: ""                      # replicated | partial | unreplicated | not_applicable | in_principle
    independent_replications: 0     # Count of independent teams/labs
    replication_rate: null           # Fraction of attempts that succeed
    notes: ""

  # ── Effect Size (weight: 0.30) ──
  effect_size:
    score: null
    magnitude: ""                   # negligible | small | medium | large | overwhelming
    sigma: null                     # Statistical significance (e.g. 6.35)
    p_value: null
    confidence_interval: ""         # e.g. "95% CI: [0.12, 0.38]"
    n_trials: null                  # Sample size
    notes: ""

  # ── Measurement Quality (weight: 0.30) ──
  measurement_quality:
    score: null
    instrument_type: ""             # e.g. "LIGO interferometer", "Google Ngram", "FBI UCR"
    calibration_status: ""          # calibrated | uncalibrated | self-calibrating
    systematic_bias_risk: ""        # low | moderate | high
    blinding: ""                    # double_blind | single_blind | open | not_applicable
    data_source_independence: ""    # independent | correlated | same_source
    notes: ""

  # ── PS Formula ──
  # PS = reproducibility × 0.40 + effect_size × 0.30 + measurement_quality × 0.30

# ═══════════════════════════════════════════════
# CHANNEL 2: EXPLANATORY DEPTH (ED)
# WHY does this happen? What mechanism explains it?
# ═══════════════════════════════════════════════
explanatory_depth:
  score: null                       # 0.00 — 1.00

  # ── Mechanism Clarity (weight: 0.40) ──
  mechanism:
    score: null
    described: false                # Is a mechanism proposed?
    formalized: false               # Is the mechanism mathematically formalized?
    causal_chain_length: 0          # How many causal steps from input to output?
    mechanism_type: ""              # physical | mathematical | logical | biological | social | theological | computational
    notes: ""

  # ── Constraint Consistency (weight: 0.30) ──
  constraints:
    score: null
    conservation_laws_respected: "" # yes | no | not_applicable
    symmetry_preserved: ""          # yes | no | not_applicable
    boundary_conditions_met: ""     # yes | no | partial
    dimensional_consistency: ""     # yes | no | not_applicable
    counterexample_handling: ""     # none_found | addressed | unaddressed
    notes: ""

  # ── Explanatory Scope (weight: 0.30) ──
  scope:
    score: null
    domains_explained: 0            # How many domains does the mechanism cover?
    special_cases_handled: 0        # Edge cases the explanation covers
    novel_predictions: 0            # Predictions the mechanism generates beyond the data
    notes: ""

  # ── ED Formula ──
  # ED = mechanism × 0.40 + constraints × 0.30 + scope × 0.30
  #
  # WHY-PENALTY: If ED < 0.3, evidence is capped at 50% maximum.
  # Unexplained phenomena are INCOMPLETE evidence, not full evidence.

  why_penalty_active: false
  why_penalty_note: ""              # e.g. "Mechanism not proposed — evidence capped"

# ═══════════════════════════════════════════════
# CHANNEL 3: EXPERIENTIAL COHERENCE (EC)
# Does this hold up in lived reality? Across time?
# ═══════════════════════════════════════════════
experiential_coherence:
  score: null                       # 0.00 — 1.00

  # ── Internal Consistency (weight: 0.25) ──
  consistency:
    score: null
    self_contradictions: 0          # Count of internal contradictions
    notes: ""

  # ── Longitudinal Stability (weight: 0.25) ──
  stability:
    score: null
    time_tested: ""                 # e.g. "100 years", "2000 years", "since 2015"
    trend: ""                       # strengthening | stable | weakening | oscillating
    notes: ""

  # ── Behavioral Transformation (weight: 0.25) ──
  transformation:
    score: null
    measurable_behavior_change: false  # Does this evidence show real-world behavioral impact?
    examples: []                    # e.g. ["75% alcohol drop", "50% crime reduction"]
    notes: ""

  # ── Intersubjective Pattern (weight: 0.25) ──
  pattern:
    score: null
    independent_discoverers: 0      # How many people independently found this?
    cross_cultural_presence: false   # Does the pattern appear across cultures?
    cross_disciplinary_citations: 0  # How many fields cite this independently?
    notes: ""

  # ── EC Formula ──
  # EC = consistency × 0.25 + stability × 0.25 + transformation × 0.25 + pattern × 0.25
```
---

## §3 — Completeness Factor & Evidence Score

```yaml
# ═══════════════════════════════════════════════
# COMPLETENESS FACTOR (CF)
# Combines ED and EC to penalize unexplained or untested evidence
# ═══════════════════════════════════════════════
completeness_factor:
  formula: "CF = (0.5 + 0.5 × ED) × (0.5 + 0.5 × EC)"
  value: null                       # 0.25 (worst) to 1.00 (perfect)
  # Note: If ED=0 and EC=0 → CF=0.25 → evidence capped at 25% of PS
  # Note: If ED=1 and EC=1 → CF=1.00 → evidence equals full PS

# ═══════════════════════════════════════════════
# FINAL EVIDENCE SCORE (E_final)
# ═══════════════════════════════════════════════
evidence_final:
  formula: "E_final = PS × CF"
  value: null
  # Caps applied:
  # If ED < 0.3 → E_final capped at 0.50 (why-penalty)
  # If EC < 0.1 → flag "NO LIVED VALIDITY"
  caps_active: []                   # e.g. ["why_penalty", "no_lived_validity"]
```

---

## §4 — Five Evidence Gates

Sequential gates from raw evidence to vulnerability assessment.
Each gate must pass before the next is meaningful.

```yaml
# ═══════════════════════════════════════════════
# GATE 1: IDENTITY (E1)
# What format is this evidence in?
# ═══════════════════════════════════════════════
gate_1_identity:
  format: ""
    # peer_reviewed_paper | preprint | dataset | computational_output
    # historical_record | scriptural_text | personal_testimony
    # journalistic_report | government_data | corporate_data
    # ai_generated | mixed
  publication_status: ""            # published | preprint | unpublished | oral_tradition
  date: ""
  source_url: ""
  doi: ""
  access_level: ""                  # open_access | paywalled | restricted | classified

# ═══════════════════════════════════════════════
# GATE 2: TYPE (E2)
# What epistemic class does this evidence belong to?
# ═══════════════════════════════════════════════
gate_2_type:
  epistemic_class: ""
    # experimental   — controlled experiment with variables
    # observational  — measured but not controlled
    # mathematical   — formal proof or derivation
    # logical        — deductive argument
    # historical     — documented past event
    # scriptural     — biblical or religious text
    # testimonial    — personal witness account
    # computational  — simulation or numerical result
    # meta_analytic  — synthesis of multiple studies
  weight_in_chain: ""               # primary | supporting | corroborating | suggestive | decorative

# ═══════════════════════════════════════════════
# GATE 3: STRENGTH (E3)
# How strong is this evidence by its own standards?
# ═══════════════════════════════════════════════
gate_3_strength:
  strength_class: ""
    # conclusive      — would convince a hostile expert
    # strong          — would convince a neutral expert
    # moderate        — would shift a neutral expert's credence
    # suggestive      — worth investigating but not sufficient alone
    # weak            — anecdotal or poorly controlled
    # contested       — significant methodological disputes
  key_metric: ""                    # e.g. "6.35σ", "p < 0.001", "n=2.5M"
  methodological_concerns: []       # List specific concerns

# ═══════════════════════════════════════════════
# GATE 4: LINKAGE (E4)
# How does this evidence connect to the claim?
# ═══════════════════════════════════════════════
gate_4_linkage:
  connection_type: ""
    # direct_test     — designed to test this specific claim
    # indirect_test   — tests a consequence of the claim
    # analogy         — similar pattern in another domain
    # necessary       — logically required for claim to hold
    # sufficient      — alone would establish the claim
    # corroborating   — consistent but not decisive
  causal_direction: ""              # cause_to_effect | effect_to_cause | bidirectional | correlation_only
  alternative_explanations: []      # What else could explain this evidence?
  exclusion_of_alternatives: ""     # none | partial | comprehensive

# ═══════════════════════════════════════════════
# GATE 5: VULNERABILITIES (E5)
# What's wrong or missing?
# ═══════════════════════════════════════════════
gate_5_vulnerabilities:
  vulnerability_flags: []
    # WHY-PENALTY          — mechanism not proposed (ED near zero)
    # NO_LIVED_VALIDITY    — no experiential coherence markers
    # UNFALSIFIABLE        — no kill conditions named
    # UNGROUNDED           — assumptions not declared
    # UNDEFINED            — claim type not classified
    # SELECTION_BIAS       — evidence cherry-picked
    # SURVIVORSHIP_BIAS    — failures not counted
    # CONFIRMATION_BIAS    — only supporting evidence sought
    # P-HACKING            — statistical significance gamed
    # SMALL_N              — sample too small for universal claim
    # SINGLE_SOURCE        — one lab, one dataset, one author
    # UNREPLICATED         — no independent replication
    # CIRCULAR             — evidence assumes what it proves
    # COMPETING_MODEL      — equally supported by rival theory
  critical_gap: ""                  # The single biggest gap
  recommended_action: ""            # What would strengthen this evidence most
```

---

## §5 — Competing Models Assessment

```yaml
# ═══════════════════════════════════════════════
# COULD THIS EVIDENCE SUPPORT A DIFFERENT CLAIM?
# ═══════════════════════════════════════════════
competing_models:
  exclusive_to_this_claim: false    # Does this evidence ONLY support this claim?
  competing_theories:
    - theory: ""                    # Name of competing model
      explains_same_evidence: ""    # fully | partially | weakly
      what_it_misses: ""            # What this competitor can't explain
      decisive_test: ""             # What experiment would distinguish them
  uniqueness_assessment: ""
    # exclusive       — no other model predicts this
    # discriminating  — this model predicts it better than alternatives
    # ambiguous       — multiple models predict this equally
    # generic         — almost any model could produce this
```

---

## §6 — Evidence Chain Audit

```yaml
# ═══════════════════════════════════════════════
# FULL AUDIT TRAIL
# What was detected, why it scored this way, what's missing
# ═══════════════════════════════════════════════
audit:
  per_channel_summary:
    ps: ""                          # One sentence: what PS found
    ed: ""                          # One sentence: what ED found
    ec: ""                          # One sentence: what EC found
  strengths: []                     # Which channels scored high and why
  weaknesses: []                    # Which channels scored low and why
  gaps: []                          # Which channels scored zero
  overall_narrative: ""             # 2-3 sentence plain language assessment

# ═══════════════════════════════════════════════
# INDEPENDENCE CHECK
# Are the evidence sources truly independent?
# ═══════════════════════════════════════════════
independence:
  sources_truly_independent: false
  shared_confounders: []            # e.g. "All four civilizations share Roman lineage"
  shared_methodology: []            # e.g. "All use same Ngram dataset"
  shared_author: false              # Same researcher collected all evidence?
  independence_score: null          # 0-1 (1 = fully independent lines)

# ═══════════════════════════════════════════════
# THEORY RESONANCE (what established theories map to this?)
# ═══════════════════════════════════════════════
theory_resonance:
  - theory: ""
    mapping: ""                     # STRUCTURAL | ANALOGICAL | NOMINAL
    free_predictions: ""            # What predictions come for free if this mapping holds?
    upgrade_path: ""                # What would need to be shown to upgrade to STRUCTURAL?
  - theory: ""
    mapping: ""
    free_predictions: ""
    upgrade_path: ""
```

---

## §7 — S/E/L/D/P/C Derivation (Truth Score Inputs)

```yaml
# ═══════════════════════════════════════════════
# HOW THIS EVIDENCE FEEDS INTO THE TRUTH SCORE
# ═══════════════════════════════════════════════
truth_score_contribution:
  S: { value: null, source: "Q7 falsifiability — kill conditions" }
  E: { value: null, source: "Q4 E_final = PS × CF" }
  L: { value: null, source: "mean(Q3 assertion precision, Q4 ED)" }
  D: { value: null, source: "Q5 dependency chain depth" }
  P: { value: null, source: "Q6 predictions generated" }
  C: { value: null, source: "Q2 cross-domain coherence" }

  T: null                           # (S + E + L + D + P + C) / 6
  T_enhanced: null                  # T × (0.6 + 0.4 × 7Q_composite)

  confidence_class: ""
    # ESTABLISHED       — T ≥ 0.85
    # WELL_SUPPORTED    — T ≥ 0.65
    # TENTATIVE         — T ≥ 0.40
    # SPECULATIVE       — T ≥ 0.15
    # UNSUPPORTED       — T < 0.15
```

---

## §8 — Quick Reference Card

| Dimension | What It Asks | Score Range | Key Metric |
|-----------|-------------|-------------|------------|
| **PS** | What do we observe? | 0-1 | Reproducibility × Effect × Quality |
| **ED** | Why does it happen? | 0-1 | Mechanism × Constraints × Scope |
| **EC** | Does it hold in life? | 0-1 | Consistency × Stability × Transformation × Pattern |
| **CF** | How complete? | 0.25-1.0 | (0.5+0.5×ED)(0.5+0.5×EC) |
| **E_final** | Total evidence | 0-1 | PS × CF |
| **E1** | Format? | categorical | What kind of document |
| **E2** | Type? | categorical | What epistemic class |
| **E3** | Strength? | categorical | How convincing by its own standards |
| **E4** | Connection? | categorical | How it links to the claim |
| **E5** | Vulnerabilities? | flags | What's wrong or missing |

### Caps
- ED < 0.3 → E_final capped at 0.50 (why-penalty)
- EC < 0.1 → flag NO_LIVED_VALIDITY
- Q7 < 0.3 → T capped at 0.60
- Q6 < 0.3 → T capped at 0.70

### The Core Principle
> Three channels multiply. You can't cheat by maxing one.
> Unexplained evidence is incomplete evidence.
> Unlived evidence is untested evidence.
> Both reduce the final score mathematically, not judgmentally.

---

*David Lowe · POF 2828 · Theophysics*
*7Q Evidence Protocol v1.0 · March 21, 2026*
*"The method does not guarantee truth. It guarantees transparency."*