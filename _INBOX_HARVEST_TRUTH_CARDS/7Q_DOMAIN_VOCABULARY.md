---
title: "7Q Domain Vocabulary — All Domains"
type: template
id: 7Q-DOMAIN-VOCAB
created: 2026-03-23
author: David Lowe | POF 2828
status: canonical
purpose: "Every domain's vocabulary that loads into the 7Q skeleton. Pick a domain, get the words."
---

# 7Q Domain Vocabulary

> The skeleton never changes. When someone picks a domain, these words load into each Q slot.
> This is the domain layer that sits on top of the universal mechanism.

---

## How This Works

```
7Q KERNEL (invariant)
    │
    ├── Q1: entity_types      ← domain provides the vocabulary
    ├── Q2: subdomains, scales ← domain provides the list
    ├── Q3: claim_types        ← domain provides what assertions look like
    ├── Q4: evidence_types     ← domain provides what counts as evidence
    ├── Q5: dependency_types   ← domain provides what the floor is made of
    ├── Q6: prediction_types   ← domain provides what "testable" means
    └── Q7: kill_conditions    ← domain provides specific death modes
```

The five universal death types (self-refutation, infinite regress, empirical contradiction, logical incoherence, explanatory failure) are ALWAYS present. Domain kills ADD to them.

---

## PHYSICS

```yaml
domain: physics
label: "Physics"

q1_entity_types:
  - axiom | law | hypothesis | theory | observation
  - claim | mechanism | definition | equation
  - evidence | operator | field | symmetry | conservation_law

q1_extras:
  formalism: equation | inequality | operator | field_equation | lagrangian | hamiltonian | lindblad | conservation
  physics_type: classical | quantum | relativistic | thermodynamic | information_theoretic | unified
  master_eq_variable: G | M | E | S | T | K | R | Q | F | C
  symmetry_pair: G↔T | M↔F | E↔C | S↔R | T↔K

q2_subdomains:
  - mechanics | electromagnetism | thermodynamics
  - quantum_mechanics | general_relativity | cosmology
  - information_theory | consciousness_physics
  - statistical_mechanics | field_theory | particle_physics

q2_scales: quantum | microscopic | mesoscopic | macroscopic | cosmological | multi_scale
q2_regimes: linear | nonlinear | perturbative | non_perturbative | equilibrium | non_equilibrium | critical

q3_claim_types:
  - descriptive | causal | ontological | predictive
  - mathematical | mechanistic | conservation | symmetry_claim | boundary_condition

q3_extras:
  coherence_prediction: increases | decreases | maintains
  entropy_relation: opposes | generates | neutral | coupled
  grace_dependence: required | enhancing | independent
  consciousness_role: fundamental | emergent | participatory | observer

q4_evidence_types: empirical | experimental | observational | mathematical | logical | computational | inferential
q4_tiers:
  tier_1: "Replicated, peer-reviewed, σ > 3"
  tier_2: "Contested but published"
  tier_3: "Speculative, unreplicated, analogical"

q5_dependency_floor:
  - "Axioms (A1.1–A12.1 in Theophysics)"
  - "Ten Laws (L01–L10)"
  - "Standard physics: GR, QFT, QM, thermodynamics"
  - "Mathematical axioms: ZFC, calculus"

q6_prediction_types: confirmed | untested | decisive | failed
q6_decisive_examples:
  - "Accelerator result"
  - "Telescope survey"
  - "Gravitational wave detection"
  - "Satellite measurement (Cassini, Euclid, JWST)"

q7_domain_kills:
  - ghost_modes: "Negative-norm states in field theory"
  - unitarity_violation: "S-matrix not unitary"
  - causality_violation: "Superluminal signals"
  - renormalization_failure: "Infinities can't be absorbed"
  - fine_tuning: "Parameters require 10⁻¹²⁰ precision"
  - solar_system_constraints: "Violates Cassini/lunar laser bounds"
  - bbn_violation: "Changes primordial element abundances"
  - cmb_inconsistency: "Conflicts with Planck data"
  - dimensional_mismatch: "Units don't work"
  - energy_condition_violation: "Negative energy density without mechanism"
```

---

## BIOLOGY

```yaml
domain: biology
label: "Biology"

q1_entity_types:
  - species | gene | protein | pathway | organism
  - mechanism | observation | theory | hypothesis
  - model | phenotype | genotype | trait

q1_extras:
  biological_level: molecular | cellular | tissue | organ | organism | population | ecosystem
  inheritance: genetic | epigenetic | cultural | none

q2_subdomains:
  - molecular_biology | genetics | genomics | proteomics
  - cell_biology | developmental_biology | neuroscience
  - evolutionary_biology | ecology | microbiology
  - systems_biology | bioinformatics | paleontology

q2_scales: molecular | cellular | tissue | organism | population | ecosystem | planetary
q2_regimes: in_vitro | in_vivo | in_silico | field_observation

q3_claim_types:
  - descriptive | causal | mechanistic | predictive
  - evolutionary | functional | structural | correlational

q3_extras:
  selection_type: natural | artificial | sexual | neutral_drift
  fitness_relation: increases | decreases | neutral

q4_evidence_types: experimental | observational | genetic | fossil | computational | comparative | clinical
q4_tiers:
  tier_1: "Replicated RCT, genome-wide significance (p < 5×10⁻⁸)"
  tier_2: "Single study, candidate gene, observational"
  tier_3: "Case report, in silico only, analogical"

q5_dependency_floor:
  - "Central dogma (DNA → RNA → protein)"
  - "Cell theory"
  - "Evolutionary theory (natural selection + drift)"
  - "Laws of thermodynamics (applied to living systems)"
  - "Chemistry: bonding, energetics, pH"

q6_prediction_types: confirmed | untested | decisive | failed
q6_decisive_examples:
  - "Gene knockout phenotype"
  - "Clinical trial outcome"
  - "Fossil prediction in specific strata"
  - "Ecological intervention result"

q7_domain_kills:
  - thermodynamic_violation: "System creates order without energy input"
  - phylogenetic_contradiction: "Clade placement impossible in any tree"
  - central_dogma_violation: "Information flows backward without known mechanism"
  - replication_failure: "Key experiment cannot be replicated"
  - extinction_of_model: "Model organism shows no predicted effect"
  - sample_size: "n < 10 for population-level claim"
  - confounding: "Uncontrolled variable explains the result"
```

---

## THEOLOGY

```yaml
domain: theology
label: "Theology"

q1_entity_types:
  - doctrine | dogma | claim | argument | narrative
  - exegesis | hermeneutic | tradition | creed
  - prophecy | revelation | testimony | axiom

q1_extras:
  tradition: catholic | protestant | orthodox | jewish | islamic | philosophical | theophysics
  authority_source: scripture | magisterium | consensus | reason | experience

q2_subdomains:
  - systematic_theology | biblical_theology | historical_theology
  - moral_theology | philosophical_theology | apologetics
  - christology | pneumatology | eschatology | soteriology
  - ecclesiology | theological_anthropology

q2_scales: personal | communal | ecclesial | civilizational | cosmic | eternal
q2_regimes: pre_fall | post_fall | redeemed | eschatological

q3_claim_types:
  - doctrinal | exegetical | historical | philosophical
  - moral | experiential | prophetic | constitutive

q3_extras:
  revelation_type: general | special | natural | propositional
  grace_relation: prevenient | justifying | sanctifying | glorifying

q4_evidence_types: scriptural | historical | philosophical | experiential | testimonial | logical | archaeological
q4_tiers:
  tier_1: "Direct scripture, ecumenical council, creedal"
  tier_2: "Church father consensus, strong philosophical argument"
  tier_3: "Private revelation, single testimony, speculative theology"

q5_dependency_floor:
  - "God exists (axiom or argued)"
  - "Scripture is authoritative (to what degree?)"
  - "Logic applies to theological claims"
  - "Historical events are recoverable"
  - "Human testimony is sometimes reliable"

q6_prediction_types: confirmed | untested | eschatological | retroactive
q6_decisive_examples:
  - "Archaeological discovery confirming/denying historical claim"
  - "Manuscript discovery changing textual basis"
  - "Cross-cultural convergence of independent testimony"
  - "Prophetic fulfillment (with pre-dating verified)"

q7_domain_kills:
  - internal_contradiction: "Two doctrines contradict within same system"
  - historical_falsification: "Key event didn't happen (e.g., no Exodus)"
  - textual_corruption: "Source text is demonstrably fabricated"
  - problem_of_evil: "Theodicy fails for this specific claim"
  - competing_revelation: "Another tradition has stronger claim on same truth"
  - moral_failure: "Doctrine produces consistent moral atrocity"
  - hermeneutic_collapse: "No stable reading of the source text possible"
```

---

## CONSCIOUSNESS

```yaml
domain: consciousness
label: "Consciousness Studies"

q1_entity_types:
  - theory | model | phenomenon | mechanism | observation
  - qualia | experience | report | correlation | claim

q1_extras:
  consciousness_theory: IIT | GWT | HOT | panpsychism | functionalism | theophysics_chi
  hard_problem_stance: dissolves | solves | accepts | reframes

q2_subdomains:
  - philosophy_of_mind | neuroscience | phenomenology
  - psychophysics | quantum_consciousness | artificial_consciousness
  - contemplative_science | neurophenomenology

q2_scales: neural | cognitive | experiential | collective | cosmic
q2_regimes: waking | dreaming | meditative | anesthetized | psychedelic | pathological

q3_claim_types:
  - phenomenological | mechanistic | correlational | constitutive
  - predictive | ontological | functional | eliminative

q3_extras:
  explanatory_gap: acknowledged | claimed_bridged | denied
  zombie_argument: relevant | irrelevant | dissolved

q4_evidence_types: neuroimaging | behavioral | psychophysical | phenomenological | computational | clinical
q4_tiers:
  tier_1: "Replicated fMRI/EEG, clinical study, large n"
  tier_2: "Single study, philosophical argument, small n"
  tier_3: "Anecdotal, introspective report, thought experiment"

q5_dependency_floor:
  - "Consciousness exists (hard to deny without contradiction)"
  - "Neural correlates are real (empirically established)"
  - "First-person reports have some reliability"
  - "Physical laws apply to brains"

q6_decisive_examples:
  - "Anesthesia prediction: specific neural signature"
  - "AI consciousness test: behavioral markers"
  - "PEAR/GCP replication at 5σ"
  - "NDE study with verified veridical perception"

q7_domain_kills:
  - explanatory_gap: "Cannot bridge subjective experience and neural activity"
  - epiphenomenalism: "Consciousness has no causal power (unfalsifiable)"
  - neural_correlation_failure: "Predicted correlate not found"
  - zombie_possibility: "Functional duplicate without experience possible in principle"
  - measurement_problem: "Cannot measure consciousness without relying on report"
  - artificial_consciousness_test: "AI passes all tests but we can't verify experience"
```

---

## INFORMATION THEORY

```yaml
domain: information_theory
label: "Information Theory"

q1_entity_types:
  - theorem | bound | channel | code | protocol
  - measure | entropy | capacity | algorithm | definition

q2_subdomains:
  - classical_information | quantum_information | algorithmic_information
  - coding_theory | cryptography | network_information_theory
  - semantic_information | biological_information

q2_scales: bit | message | channel | network | universal
q2_regimes: noiseless | noisy | quantum | classical | distributed

q3_claim_types:
  - mathematical | bound | capacity | optimality | impossibility | protocol

q4_evidence_types: mathematical_proof | computational | experimental | information_theoretic
q4_tiers:
  tier_1: "Formal proof, replicated computation"
  tier_2: "Numerical evidence, conjectured bound"
  tier_3: "Heuristic argument, analogy"

q5_dependency_floor:
  - "Shannon entropy definition"
  - "Probability theory"
  - "Kolmogorov axioms"
  - "For quantum: Hilbert space formalism"

q7_domain_kills:
  - capacity_exceeded: "Channel capacity claim violated by counterexample"
  - entropy_violation: "Claimed compression below Shannon limit"
  - no_free_lunch: "Claimed universal advantage without trade-off"
  - complexity_mismatch: "Algorithm claimed efficient but provably not"
```

---

## ECONOMICS

```yaml
domain: economics
label: "Economics"

q1_entity_types:
  - theory | model | policy | mechanism | observation
  - market | institution | agent | equilibrium | claim

q2_subdomains:
  - microeconomics | macroeconomics | behavioral_economics
  - game_theory | development_economics | monetary_theory
  - political_economy | econometrics | financial_economics

q2_scales: individual | firm | market | national | global
q2_regimes: equilibrium | disequilibrium | crisis | transition

q3_claim_types:
  - causal | predictive | normative | descriptive | mechanistic | correlational

q4_evidence_types: econometric | experimental | natural_experiment | historical | survey | simulation
q4_tiers:
  tier_1: "RCT, natural experiment with strong instrument"
  tier_2: "Observational with controls, quasi-experimental"
  tier_3: "Case study, simulation only, theoretical"

q5_dependency_floor:
  - "Agents respond to incentives"
  - "Scarcity exists"
  - "Markets clear (or don't — specify)"
  - "Rational choice (or bounded — specify)"

q7_domain_kills:
  - natural_experiment_contradiction: "Policy tested, opposite result"
  - lucas_critique: "Model breaks when agents learn the model"
  - external_validity_failure: "Works in lab, fails in field"
  - endogeneity: "Claimed cause is actually effect"
  - goodhart_law: "Measure becomes target, ceases to be good measure"
```

---

## MORAL PHILOSOPHY

```yaml
domain: moral_philosophy
label: "Moral Philosophy"

q1_entity_types:
  - principle | virtue | duty | right | claim
  - theory | dilemma | intuition | argument | framework

q2_subdomains:
  - metaethics | normative_ethics | applied_ethics
  - virtue_ethics | deontology | consequentialism
  - moral_psychology | political_philosophy | bioethics

q2_scales: personal | interpersonal | institutional | societal | universal
q2_regimes: ideal | non_ideal | emergency | everyday

q3_claim_types:
  - normative | metaethical | applied | descriptive | constitutive

q3_extras:
  moral_realism: realist | anti_realist | constructivist | error_theory
  universalizability: universal | contextual | relative

q4_evidence_types: philosophical_argument | intuition_pump | empirical_moral_psychology | historical | testimonial | cross_cultural
q4_tiers:
  tier_1: "Valid argument from shared premises, cross-cultural convergence"
  tier_2: "Strong intuition, historical precedent"
  tier_3: "Single tradition, contested premises"

q5_dependency_floor:
  - "Moral claims can be true or false (or specify anti-realism)"
  - "Humans have agency"
  - "Suffering matters (or argue otherwise)"
  - "Consistency is required"

q7_domain_kills:
  - reductio_ad_absurdum: "Principle leads to monstrous conclusion"
  - moral_intuition_override: "Almost everyone finds this wrong"
  - demandingness: "Principle requires impossible sacrifice"
  - moral_luck: "Principle makes moral worth depend on chance"
  - is_ought_gap: "Derives ought from is without bridge"
  - cultural_imperialism: "Universal claim can't survive contact with other traditions"
```

---

## HISTORY

```yaml
domain: history
label: "History"

q1_entity_types:
  - event | process | institution | person | period
  - narrative | cause | consequence | source | claim

q2_subdomains:
  - political_history | social_history | economic_history
  - intellectual_history | military_history | cultural_history
  - historiography | world_history | microhistory

q2_scales: individual | local | regional | national | civilizational | global
q2_regimes: ancient | medieval | early_modern | modern | contemporary

q3_claim_types:
  - causal | descriptive | comparative | counterfactual | periodization | narrative

q4_evidence_types: primary_source | secondary_source | archaeological | numismatic | epigraphic | oral_tradition | archival
q4_tiers:
  tier_1: "Multiple independent primary sources, archaeological confirmation"
  tier_2: "Single primary source, strong secondary consensus"
  tier_3: "Oral tradition only, heavily contested, no material evidence"

q5_dependency_floor:
  - "Sources are sometimes reliable"
  - "Past events are recoverable (to some degree)"
  - "Causation in human affairs is possible to argue"
  - "Anachronism must be avoided"

q7_domain_kills:
  - source_fabrication: "Key source is forged or fabricated"
  - archaeological_contradiction: "Material evidence contradicts narrative"
  - anachronism: "Claim imposes modern categories on past"
  - selection_bias: "Only favorable sources cited"
  - unfalsifiable_narrative: "Story explains everything, predicts nothing"
  - presentism: "Past judged entirely by present values"
```

---

## THEOPHYSICS (Composite Domain)

```yaml
domain: theophysics
label: "Theophysics (composite)"
inherits: [physics, theology, consciousness, information_theory]

q1_extras:
  master_equation: "χ = ∭(G·M·E·S·T·K·R·Q·F·C) dx dy dt"
  ten_laws: L01–L10
  five_symmetry_pairs: "G↔T, S↔F, E↔K, M↔Q, R↔C"
  chi_field: "Self-grounding informational substrate"

q2_subdomains:
  - "All physics subdomains"
  - "All theology subdomains"
  - "All consciousness subdomains"
  - "All information theory subdomains"
  - "moral_physics (unique to theophysics)"

q3_extras:
  iso_requirement: "All cross-domain claims must specify ISO status"
  grace_source_term: "J_grace = β_G·Φ(x)·f_reg(χ)/(S_local+ε)"
  modified_uncertainty: "Δx·Δp ≥ ℏ(1-C)/2"

q7_domain_kills:
  all_physics_kills: "Inherited"
  all_theology_kills: "Inherited"
  trinity_inconsistency: "Mathematical trinity mapping contradicts Nicene formulation"
  chi_field_redundancy: "ΛCDM explains all data without χ"
  grace_unfalsifiable: "Grace source term cannot be measured in principle"
  consciousness_epiphenomenal: "χ-field has no observable coupling to matter"
  ten_laws_arbitrary: "No derivation for why these ten and not others"
```

---

## Adding a New Domain

To add a domain, fill this template:

```yaml
domain: [name]
label: "[Display Name]"

q1_entity_types: [list]
q1_extras: {field: options}

q2_subdomains: [list]
q2_scales: [list]
q2_regimes: [list]

q3_claim_types: [list]
q3_extras: {field: options}

q4_evidence_types: [list]
q4_tiers:
  tier_1: "[definition]"
  tier_2: "[definition]"
  tier_3: "[definition]"

q5_dependency_floor: [list of bedrock assumptions]

q6_prediction_types: [list]
q6_decisive_examples: [list]

q7_domain_kills:
  [kill_name]: "[description]"
```

The five universal death types are inherited automatically. Domain kills add to them.

---

*David Lowe · POF 2828 · Theophysics*
*"Same skeleton. Different words."*
