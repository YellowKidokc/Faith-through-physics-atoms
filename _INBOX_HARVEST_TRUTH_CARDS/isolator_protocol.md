# Isolator Protocol — Adjudicating Endogenous vs Exogenous Restoration

## 1. Formal Result

For any coherence dynamics of the form

```text
dc/dt = omega(s) * sigma(s) * (1 - c) - delta(s) * c
```

if `delta(s) ≥ delta_min > 0` and the effective source `omega(s) * sigma(s) ≤ K_eff < ∞`,
then at equilibrium

```text
c* ≤ K_eff / (K_eff + delta_min) < 1.
```

Perfect coherence (`c* = 1`) is impossible with only a bounded endogenous effective source.

See `DharmaMirror/Isolator.lean` for the Lean 4 proofs:

- `bounded_endogenous_equilibrium_bound`
- `bounded_endogenous_cannot_perfect`
- `unbounded_source_perfect_attractor`
- `faith_is_coupling_not_source`

## 2. Endogenous Restoration Criteria

A source model is endogenous if:

- `sigma(s)` is computable from the system's internal state.
- The effective source `omega(s) * sigma(s)` is bounded by a finite constant independent of state.

Examples: self-organization, learning, practice, insight, internal information reconfiguration.

## 3. Exogenous Restoration Criteria

A source model is exogenous if:

- `sigma(s)` includes a contribution not determined by the system state.
- The effective source can be made arbitrarily large by increasing an external term.

Examples: external input, uncreated ground, infinite source, grace, nondual ground modeled as external to the finite self.

## 4. Adjudication Rules

1. **No relabeling without identifiability.** A worldview may not claim its source is exogenous merely by giving it a theological name. It must show the source term satisfies the formal exogeneity condition.
2. **Curve-fitting is not a proof obligation.** Demonstrating that a model fits data does not discharge the obligation to classify its source as endogenous or exogenous.
3. **Internal inconsistency is decisive.** If a worldview claims endogenous restoration and also claims perfect coherence, it must either bound its effective source and accept `c* < 1`, or admit an unbounded/external source.
4. **Incommensurability is allowed but costly.** A worldview may reject scalar coherence entirely, but then it cannot use the isolator's conclusions and must defend its own measurement framework.

## 5. Worldview Proof Obligations

| Worldview | Obligation |
|-----------|-----------|
| Christian | Show that grace functions as an exogenous, non-coercive source. Show that faith is coupling, not production of grace. |
| Buddhist | Specify the source model: bounded endogenous, unbounded endogenous, exogenous/nondual, or non-scalar. Then prove the consequences. |
| Materialist | Show that self-organization can overcome positive decay without external source injection, or accept the bound. |

## 6. Non-Coercive Grace

Non-coercive means the received contribution `omega * sigma → 0` as openness/faith `omega → 0`.
The source `sigma` may remain available; it is not coercively received by a closed system.
This preserves the distinction: grace is the source, faith is the coupling.
