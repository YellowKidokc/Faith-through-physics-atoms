# Axiom Pill Mind Map Spec

Purpose: render individual axiom atoms as a readable map without flattening the
entire axiom spine into one chain.

Each axiom pill is one inspectable node. The map shows local dependencies,
claim type, evidence burden, risk, Lean role, and kill condition.

## Axiom Pill Slots

| Slot | Source Field |
|---|---|
| Axiom ID | `axiomRegistry.axiomID` |
| Old ID | `axiomRegistry.oldID` |
| Title | `name` |
| Claim class | `claimClass` |
| Plain statement | `statementPlain` |
| Technical statement | `statementTechnical` |
| Mathematical form | `mathematicalForm` |
| Logical force | `axiomRegistry.logicalForce` |
| Lean role | `axiomRegistry.leanKind` + `axiomRegistry.kernelRole` |
| Risk | `axiomRegistry.riskLevel` |
| Module | `axiomRegistry.moduleID` + `axiomRegistry.moduleTitle` |
| Dependencies | `edges[type=dependsOn]` |
| Kill condition | `falsificationCondition` |
| Propagation test | `axiomRegistry.propagationTest` |
| Eliminated worldview | `axiomRegistry.worldviewsEliminated` |

## Axiom Claim Types

| Type | Meaning | Evidence Burden |
|---|---|---|
| `floor_axiom` | Declared floor commitment | State premise and boundary |
| `definition` | Term-setting node | Check consistency and no drift |
| `theorem` | Derived node | Show derivation or formal receipt |
| `mathematical` | Formal/math structure | Derivation, type check, or proof |
| `empirical_anchor` | Claim touches observable data | Dataset/method/source |
| `prediction` | Future or testable expectation | Date, metric, falsifier |
| `bridge` | Cross-domain mapping | Bridge grade and boundary |
| `boundary` | Limit or guardrail | Explain what it blocks |

## Mind Map Rule

The map should not say "188 axioms are all equally foundational."

It should say:

1. Here is an individual axiom atom.
2. Here is what kind of thing it is.
3. Here is what it depends on.
4. Here is what depends on it.
5. Here is what would break it.
6. Here is whether it is Lean-ready, risky, provisional, or floor-level.

## Visual Grouping

Use module clusters first:

- `M01` Information Ground
- `M02` Coherence / Master Equation
- `M03+` as present in registry

Then color by claim class:

- floor axiom: dark indigo
- definition: teal
- theorem: amber
- mathematical: blue
- empirical/prediction: green
- bridge/boundary: rose

Risk should be visible as a small badge, not as a hidden field.
