# Chi Properties — Physics Mirror Scan & Isomorphic Event Candidates
## Generated 2026-08-10 from ME-01-050 properties against known physics

---

## PROPERTY-BY-PROPERTY PHYSICS MIRRORS

### 1. Multiplicative Product Structure (not additive)

| Physics Process | Mirror Grade | Sameness Level | Notes |
|---|---|---|---|
| **Reliability engineering** | EXACT | L5 | R_system = prod R_i. Any R_i = 0 kills system. Identical math, identical veto. |
| **Feynman amplitudes** | EXACT | L5 | Total amplitude = product of vertex amplitudes. Forbidden vertex = 0 kills the path. |
| **Independent probability** | EXACT | L4 | P(all) = prod P_i. Any impossible event zeros joint. |
| **Transfer matrices (stat mech)** | STRONG | L4 | Z = Tr(prod T_i). Singular matrix collapses the trace. |
| **Signal chain gain** | EXACT | L5 | Total gain = prod G_i. Zero gain at any stage = no output. |
| **Survival analysis** | STRONG | L4 | S(t) = prod S_i(t). Any lethal event zeros survival. |

ISO-CHI-001: Reliability R = prod R_i maps one-for-one onto chi = prod X_i. Lean target: EventIso preserving step, invariant, cost, veto.

### 2. Veto Property (any zero collapses the whole)

| Physics Process | Mirror Grade | Sameness Level | Notes |
|---|---|---|---|
| **Series circuit** | EXACT | L5 | Open switch kills current through entire circuit. |
| **Enzyme cascade** | EXACT | L5 | Missing enzyme halts entire downstream chain. |
| **Nuclear criticality** | STRONG | L4 | k_eff below 1 at any stage, chain dies. |
| **Supply chain** | EXACT | L5 | Missing component halts production line. |
| **AND gate** | EXACT | L7 | Output = prod inputs. Any 0 = 0 output. Boolean product IS the veto. |

ISO-CHI-002: AND gate maps onto veto. Already Lean-proved (listProd_eq_zero_iff). Boolean bridge is one def away.

### 3. Bounded [0,1], Non-negative, Continuous

| Physics Process | Mirror Grade | Sameness Level | Notes |
|---|---|---|---|
| **Order parameters** | EXACT | L5 | Magnetization M in [0,1]. Superconducting |psi| in [0,1]. |
| **Quantum fidelity** | EXACT | L4 | F(rho,sigma) in [0,1]. How close two states are. |
| **Correlation functions** | STRONG | L3 | Normalized autocorrelation absolute value in [0,1]. |

ISO-CHI-003: Order parameter phase transition maps onto chi. Both bounded, both collapse to zero, both have critical thresholds. Sameness L6.

### 4. Dimensionless Ratios (fraction of capacity)

| Physics Process | Mirror Grade | Sameness Level | Notes |
|---|---|---|---|
| **Thermodynamic efficiency** | EXACT | L4 | eta = W_out/Q_in in [0,1]. Fraction of available energy. |
| **Shannon utilization** | EXACT | L5 | Rate/capacity in [0,1]. This IS Level 0 of chi. |
| **Quantum gate fidelity** | STRONG | L4 | F = |<psi_ideal|psi_actual>|^2 in [0,1]. |
| **Solar cell fill factor** | EXACT | L4 | FF = P_max/(V_oc x I_sc) in [0,1]. |

Key finding: fraction-of-capacity is the standard form of any normalized performance metric. Not a Theophysics invention.

### 5. Wrapper (operator, not factor)

| Physics Process | Mirror Grade | Sameness Level | Notes |
|---|---|---|---|
| **Hamiltonian** | STRONG | L4 | H collects energy terms; H is not T or V. |
| **Trace in QM** | EXACT | L5 | Tr(rho A) wraps the product; not a factor in it. |
| **Partition function Z** | STRONG | L4 | Z wraps microstates. Z is not a microstate. |
| **Normalization** | EXACT | L5 | <psi|psi>=1 constrains the whole, not a component. |
| **Functor** | EXACT | L5 | Maps between categories; not an object in either. Same type-level distinction as C_W. |

ISO-CHI-004: Z wraps microstates into thermo; C_W wraps factors into coherence. Neither is a member of what it wraps. Sameness L4.

### 6. Snapshot vs Dynamics (Level 1 vs Level 2)

| Physics Process | Mirror Grade | Sameness Level | Notes |
|---|---|---|---|
| **Config space vs phase space** | EXACT | L5 | Where vs which-way. Same split. |
| **PES vs equations of motion** | EXACT | L5 | Landscape vs movement on landscape. |
| **Free energy vs Langevin** | EXACT | L6 | F(x) landscape + dx/dt = -nabla F + noise maps onto chi landscape + dX/dt = W nabla chi + eta. |

ISO-CHI-005 (HIGHEST PRIORITY): Langevin maps onto chi Level 2.
- Mobility mu = will W
- Landscape V = chi
- Thermal noise xi = grace eta
- BREAK: noise is random; grace is directed. The break IS the theological claim. Two theorems from one structure.
- Sameness L6 with named defect.

### 7. Gradient Ascent

| Physics Process | Mirror Grade | Sameness Level | Notes |
|---|---|---|---|
| **Gradient descent (ML)** | EXACT (sign-flipped) | L5 | theta - alpha nabla L vs X + W nabla chi. Same dynamics, opposite sign. |
| **Chemotaxis** | EXACT | L5 | Bacteria swim up concentration gradients. |
| **Free fall** | STRONG | L4 | Follow the landscape. Sign convention differs. |

### 8. Measurement Instrument (not salvation)

Category distinction, not structural isomorphism. Chi is thermometer, not heater. Reads the walk; does not set the latch.

### 9. Free Will in the Derivative

| Physics Process | Mirror Grade | Sameness Level | Notes |
|---|---|---|---|
| **Velocity vs position** | EXACT | L7 | Can't see direction from a photograph. Will is velocity. |
| **Momentum generates translation** | STRONG | L5 | Same role in Hamiltonian mechanics. |
| **Current vs charge** | EXACT | L5 | Charge = snapshot. Current = derivative. Sleeping saint = capacitor. |

---

## ISOMORPHIC EVENT CANDIDATES SUMMARY

| ID | Physics Mirror | Chi Property | Level | Lean |
|---|---|---|---|---|
| ISO-CHI-001 | Series reliability | Product structure | L5 | TARGET |
| ISO-CHI-002 | AND gate | Veto | L7 | PARTIAL (exists) |
| ISO-CHI-003 | Order parameter | Bounded + collapse | L6 | TARGET |
| ISO-CHI-004 | Partition function Z | Wrapper | L4 | TARGET |
| ISO-CHI-005 | Langevin dynamics | Gradient + source | L6 (defect) | TARGET: prove iso AND break |
| ISO-CHI-006 | Gradient descent | Gradient ascent | L5 | TARGET |
| ISO-CHI-007 | Current vs charge | Will in derivative | L5 | TARGET |

## NAMED BREAKS (where iso fails and why the failure matters)

1. Langevin noise is random; grace is directed. The break IS the content.
2. Gradient descent minimizes (human-designed loss); chi ascends (Logos-given landscape). Break points at the designer.
3. Order parameters don't choose alignment; chi carries free will in six of nine registers. Break is where agency enters.
4. Reliability has no grace term. Failed component stays failed unless repaired from outside. The repair IS grace, but in engineering it's designed in. In chi it comes from outside. Break is the open-system claim.
