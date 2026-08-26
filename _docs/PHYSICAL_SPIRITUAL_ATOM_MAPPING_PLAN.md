# Physical / Spiritual Atom Mapping Plan

Purpose: make the support concepts thorough enough to become both machine-readable atoms and future mind-map nodes without overpromoting a bridge claim.

This document is a build plan, not canon promotion. It should guide later atom creation, validation, graph rendering, and paper synthesis.

## Core Decision

Every cross-domain term should be split into three inspectable things:

1. **Physical atom**  
   The standard physics concept: definition, domain, equations, manifestations, limits.

2. **Spiritual atom**  
   The theological, moral, or lived concept: definition, scriptural/theological anchors, manifestations, limits.

3. **Bridge atom or bridge edge**  
   The proposed mapping between them: claim grade, what is preserved, what is not preserved, what would break it.

Do not collapse all three into one atom. If the bridge fails, the physical definition and the spiritual definition may still remain valid.

## Why This Matters

The Master Equation can only be trusted if its supporting vocabulary is accountable.

The equation is not just ten variables multiplied together. It is a graph of:

- definitions
- assumptions
- physical mechanisms
- spiritual correspondences
- bridge grades
- dependencies
- negative guards
- kill conditions
- receipts

That graph later becomes the mind map.

## Atom Classes Needed

Use these as preferred `claimClass` / `nodeType` meanings when creating JSON-LD atoms or Lane 4 atoms.

| Class | Meaning | Example |
|---|---|---|
| `physical_definition` | Standard physics concept | equilibrium, flux, conservation |
| `spiritual_definition` | Theological/moral/lived concept | peace, grace, moral cost |
| `master_equation_factor` | Existing ME slot | G, M, E, S_eff, T, K, R, Q, F, C |
| `bridge_candidate` | Cross-domain mapping not yet proven | equilibrium -> peace |
| `boundary_guard` | What the claim must not say | conservation != direct proof of moral conservation |
| `manifestation_index` | Where the concept appears | buildings, fields, fluids, phase states |
| `paper_seed` | Writing unit produced from atom cluster | Peace Is Not Nothing Happening |
| `mindmap_cluster` | Visual group / graph region | State-Boundary-Balance-Limit |

If the current schema only allows broader names, preserve these as tags, keywords, or classification fields until the schema is intentionally extended.

## Edge Types Needed

Use typed edges so the graph can show the difference between support, bridge, analogy, and proof.

| Edge Type | Meaning | Propagates Falsification? |
|---|---|---|
| `definesPhysicalTerm` | A definition atom names a physical concept | No |
| `definesSpiritualTerm` | A definition atom names a spiritual concept | No |
| `manifestsIn` | Concept appears in a physical/lived domain | No |
| `explainsWhyThere` | Mechanism explains manifestation | No |
| `supportsMasterEquationRole` | Concept clarifies an ME factor/operator/boundary | Sometimes |
| `mapsToCandidate` | Candidate cross-domain bridge | No |
| `mapsToFormal` | Explicit formal bridge with maps/guards | Yes only if grade allows |
| `guardsAgainst` | Blocks overclaim or category error | No |
| `requiresReceipt` | Needs Lean, dataset, source, or derivation | No |
| `feedsPaper` | Atom cluster can generate a paper | No |
| `feedsMindMap` | Atom cluster should render as a visual graph | No |

## Bridge Grades

Use existing bridge-grade discipline:

| Grade | Meaning | Allowed Language |
|---|---|---|
| `metaphorical` | Useful image only | "illustrates" |
| `structural_analogy` | Similar pattern, not formal | "resembles", "parallels" |
| `candidate_correspondence` | Testable mapping candidate | "candidate bridge", "structural correspondence" |
| `formal_correspondence` | Explicit map and boundaries exist | "formal correspondence" |
| `structural_isomorphism` | Maps, inverses, preservation/reflection, guards passed | "isomorphism" |
| `structural_identity` | Same formal structure under disciplined interpretation | Use rarely; requires strongest receipts |

Default grade for the General physics support vocabulary should be `candidate_correspondence` or lower until formal gates are passed.

## Required Fields For Each Physical Atom

Each physical atom should answer:

- What is the term?
- What is the standard physics definition?
- What equations or formal constraints are involved?
- Where does it manifest physically?
- Why does it manifest there?
- What domain limits apply?
- What would be a misuse of the term?
- Which Master Equation role does it support?
- What source artifact did it come from?

## Required Fields For Each Spiritual Atom

Each spiritual atom should answer:

- What is the term?
- What is the theological/moral/lived definition?
- Where does it manifest in human or spiritual life?
- What scriptural, doctrinal, or philosophical anchors apply?
- What are the boundaries of the term?
- What would be a misuse of the term?
- Which Master Equation role does it support?
- What source artifact did it come from?

## Required Fields For Each Bridge Atom

Each bridge atom should answer:

- Which physical atom is being mapped?
- Which spiritual atom is being mapped?
- What property is claimed to be preserved?
- What property is explicitly not claimed?
- What is the bridge grade?
- What would break or demote the bridge?
- What evidence is present?
- What receipt is still owed?
- Does falsification propagate?

## Master Equation Role Vocabulary

Use these roles to connect support atoms to the Master Equation without forcing every term into a factor slot.

| Role | Meaning |
|---|---|
| `state_variable` | Describes current condition of chi or a component |
| `factor_slot` | Directly clarifies G/M/E/S_eff/T/K/R/Q/F/C |
| `operator` | Acts on or transforms the system |
| `boundary_condition` | Describes what may enter, leave, or constrain the system |
| `conservation_constraint` | Tracks what cannot disappear without accounting |
| `equilibrium_target` | Defines stable/high-coherence condition |
| `failure_mode` | Defines collapse, disorder, noise, distortion, or instability |
| `actualization_gate` | Describes transition from potential to actuality |
| `measurement_condition` | Describes observation, visibility, or detection |
| `limit_condition` | Defines impossibility or range of validity |
| `paper_cluster` | Organizes atoms for writing output |
| `mindmap_cluster` | Organizes atoms for visual graph output |

## First Candidate Inventory: General Physics Layer

These are the first support atoms to create or reconcile. They are the grammar layer behind the Master Equation.

| Physical Atom | Spiritual Atom Candidate | ME Role | Bridge Grade Now | Paper/Mindmap Cluster |
|---|---|---|---|---|
| state | condition / spiritual state | `state_variable` | `candidate_correspondence` | State and Identity |
| table | enumerated possibility / discernment | `mindmap_cluster` | `structural_analogy` | Possibility Space |
| conservation | moral accounting / cost | `conservation_constraint` | `candidate_correspondence` | Cost and Consequence |
| flux | transfer / giving / leakage | `boundary_condition` | `candidate_correspondence` | Boundary Transfer |
| energy flux | active transfer / grace input caution | `boundary_condition` | `structural_analogy` | Boundary Transfer |
| equilibrium | peace / rightly ordered relation | `equilibrium_target` | `candidate_correspondence` | Peace and Stability |
| superposition | unresolved potential / choice | `actualization_gate` | `candidate_correspondence` | Potential to Actual |
| random motion | hidden aggregate order / disorder | `failure_mode` | `structural_analogy` | Noise and Disorder |
| noise | confusion / unresolved signal | `failure_mode` | `structural_analogy` | Noise and Disorder |
| speed limit | creaturely limit / impossible task | `limit_condition` | `candidate_correspondence` | Limit and Law |

## Link To Existing Master Equation Atoms

The current master-equation atoms already include factor slots such as:

- `ME-01-020` G - External Negentropy Influx
- `ME-01-021` M - Alignment Cosine
- `ME-01-022` E - Signal Propagation Fidelity
- `ME-01-023` S_eff - Effective Entropy Factor
- `ME-01-024` T - Temporal Integration
- `ME-01-025` K - Information Compression Ratio
- `ME-01-026` R - Phase Transition Indicator
- `ME-01-027` Q - Superposition Measure
- `ME-01-028` F - Non-Local Correlation Strength
- `ME-01-029` C - Total Integration Measure
- `ME-01-060` Full Master Equation

The support atoms should not replace these. They should attach to them.

Examples:

- `superposition` supports `ME-01-027` as a physical/definition source for Q.
- `flux` supports `ME-01-020` as boundary-language for external influx.
- `noise` supports `ME-01-022` and `ME-01-023` as signal and entropy distortion language.
- `equilibrium` supports the interpretation of high `chi` as stable coherence.
- `speed limit` supports impossible-transition and range-of-validity guards.
- `conservation` guards grace/non-unitarity language so it does not become "energy from nowhere."

## Mind Map Design

Future visual maps should not show one flat cloud of terms. Use layers:

1. **Master Equation center**  
   `chi_total` and ten factor atoms.

2. **Physical grammar ring**  
   state, conservation, flux, equilibrium, superposition, noise, speed limit.

3. **Spiritual meaning ring**  
   condition, cost, transfer, peace, potential, confusion, creaturely limit.

4. **Bridge ring**  
   candidate edges with grades and kill conditions.

5. **Output ring**  
   papers, everyday translations, evidence receipts, objections, falsification tests.

Every visual node should show:

- title
- class
- domain
- status
- bridge grade if applicable
- kill condition badge
- source artifact link

## What Is Really Needed Before Generation

Before generating new atoms, run an audit:

1. Confirm whether a matching atom already exists in `master-equation`, `physics`, `theology`, `_ledger/atoms`, or axiom JSON-LD files.
2. If it exists, add edges or a bridge atom rather than duplicate it.
3. If it does not exist, create a draft physical atom and draft spiritual atom.
4. Create bridge atoms only after both sides have stable definitions.
5. Keep all initial bridge grades at `candidate_correspondence` or lower.
6. Attach source artifacts and negative guards.
7. Render a dry-run mind map before promotion.

## Overclaim Guards

Apply these guards to every generated bridge:

- A physical definition does not prove a spiritual identity.
- A spiritual meaning does not define the physics term.
- A bridge grade belongs on the mapping, not on either source atom.
- A mind map is a visualization, not evidence.
- A compiled proof only proves the formal statement under its premises.
- A receipt never silently promotes canon status.

## Suggested Build Sequence

1. Create or reconcile physical definition atoms for the General layer.
2. Create or reconcile spiritual definition atoms for the matching meaning layer.
3. Create bridge-candidate atoms with strict guards.
4. Link bridge candidates to existing Master Equation factor atoms.
5. Render a dry-run mind map from the graph.
6. Review bridge grades manually.
7. Only then consider promotion or public paper generation.

## First Paper Cluster

Start with equilibrium because it is strong and clean:

- physical atom: equilibrium
- spiritual atom: peace / rightly ordered relation
- bridge atom: equilibrium-to-peace candidate correspondence
- ME role: `equilibrium_target`
- paper seed: `Peace Is Not Nothing Happening`
- guard: this is not a proof that spiritual peace reduces to mechanics

Compressed line:

> A stable system is not one without forces; it is one whose forces have found their truthful relation.

