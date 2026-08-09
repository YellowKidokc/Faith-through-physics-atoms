# Claim Evidence Lane Framework

Purpose: keep claims, evidence, story, and proof status separate on API rails.

The pill must not treat all sentences the same. A claim has a type, and each
type has a matching evidence burden.

## Core Separation

| Slot | Meaning | Can Prove? |
|---|---|---|
| Claim | The exact assertion being made | No, it is the thing evaluated |
| Evidence | The support matched to that assertion | Sometimes, by lane |
| Story | Human-readable rendering | No, it carries meaning and memory |
| Beacon | Permanent ID and receipt trail | No, it preserves identity |
| Defense class | What kind of argumentative support it has | Classifies the burden |
| Kill condition | What would break this exact claim | Governs falsification |

## Framework Lanes

Use one primary lane per claim:

| Lane | Use When |
|---|---|
| `physics` | Claim is directly about physical theory, measurement, or accepted science |
| `master_equation` | Claim routes through chi, the product form, variables, or equation mechanics |
| `ten_laws` | Claim routes through one or more law rails |
| `trinity` | Claim routes through Father/Son/Spirit, perichoresis, or triadic grounding |
| `axioms` | Claim routes through floor commitments, definitions, or axiom spine |
| `consciousness` | Claim concerns observer, witness, recursion, self-reference, Phi, or mind |
| `morality` | Claim concerns good, evil, obligation, guilt, repair, justice, mercy |
| `crown` | Claim concerns truth/fracture/grace/cost/Cross resolution |
| `story` | Claim is primarily a public/narrative rendering |
| `meta` | Claim is about the method, canon, ledger, or proof discipline |
| `other` | Temporary catch-all; should be reduced by later passes |

## Physics Claim Types

If a claim touches physics, classify it precisely.

| Type | Allowed Evidence |
|---|---|
| `established_physics` | Textbook/peer-reviewed physics, standard equations, recognized results |
| `physics_model` | Defined model assumptions, equations, scope limits, comparison to known physics |
| `mathematical_formalism` | Derivation, proof, Lean receipt, algebra, typed definitions |
| `simulation_runtime` | Code, inputs, outputs, reproducible run receipt |
| `empirical_prediction` | Dataset, method, date, metric, expected result, kill condition |
| `bridge_mapping` | Bridge grade, mapping table, boundary, non-propagation rule if weak |
| `theological_interpretation` | Theology/scripture/tradition plus explicit bridge boundary |
| `story_rendering` | Story rail review; never counted as physics proof |
| `not_physics` | Claim does not make a physics assertion |

## Evidence Lanes

| Evidence Lane | Matches |
|---|---|
| `lean_formal` | Formalized theorem/model claims |
| `math_derivation` | Hand derivation or symbolic proof |
| `python_runtime` | Simulations, scoring, data processing |
| `empirical_dataset` | Measurements, surveys, historical data, cosmology releases |
| `historical_source` | Historical or tradition claims |
| `scripture_theology` | Christian theological claims |
| `philosophical_argument` | Grounding, self-reference, metaphysical arguments |
| `adversarial_review` | Objections, steelman, model critique, Kimi/Codex review |
| `story_quality` | Narrative readability, punch, clarity, audience fit |
| `none_needed` | Declared root or story line that is not offered as proof |
| `mixed` | Temporary; should be split if the claim becomes canonical |

## Defense Classes

| Defense Class | Meaning |
|---|---|
| `ROOT` | Declared starting premise. Not derived. |
| `AXIOM` | Rule/floor assumption inside the system. |
| `CLOSURE` | Denial entangles itself or collapses the claim. |
| `DERIVATION` | Follows from named premises, receipts, or earlier nodes. |
| `ADMISSION` | Open problem, limit, concession, kill condition, or owed work. |
| `RHETORIC` | Story, analogy, image, speech line. Useful, but not proof. |
| `UNCLASSIFIED` | Temporary; requires review. |

## Pill Rule

Each pill should render:

1. Claim text.
2. Framework lane.
3. Physics claim type, if relevant.
4. Defense class.
5. Evidence needed.
6. Evidence present.
7. Evidence gap.
8. Kill condition.
9. Story rendering, kept separate.
10. Beacon and log receipt.

The pill may be beautiful, but the rails must stay strict.
