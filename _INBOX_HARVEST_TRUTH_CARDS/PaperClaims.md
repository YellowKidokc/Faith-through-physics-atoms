# Paper Claim Matrix

This file tracks which claims from the draft are formal, assumed, empirical, or
currently only conceptual.

| Draft claim | Lean status | Notes |
| --- | --- | --- |
| `C0` and `C1` are distinct coupling architectures | proved | See `C0_ne_C1` and `C1_ne_C0`. |
| `C0 -> C1` is irreversible | proved relative to definition | True for the current one-way `CouplingStep`; stronger notions need formalization. |
| `Q = 0` collapses the master equation | proved in toy model | Current `chi` is over `Nat`, not real-valued fields or integrals. |
| The stage sequence reaches redistribution from pre-localization | proved in toy model | See `reaches_redistribution_from_pre`; this proves ordering only. |
| Individual reverse stage steps are absent | proved relative to definition | Current stage machine is one-way by construction. |
| The named physics operation sequence maps to the named theology sequence | proved in toy model | See `map_physics_sequence_is_theology_sequence`; this checks explicit order mapping, not categorical isomorphism. |
| Law 4 strong-force/love abstraction is isomorphic | proved relative to enriched toy definition | See `law4Iso` and `richLaw4Iso`; `RichLawIso` blocks the natural coin false positive, but a deliberately relabeled coin still passes, so semantic grounding remains external to Lean. |
| `Q ≠ 0` is sufficient for live coupling | not proved | Needs a positivity model and assumptions for all other factors. |
| Ten-factor physical/theological bridge matrix is internally consistent | proved relative to encoded signatures | See `BridgeMatrix.canonicalRows_all_valid`; targeted semantic swaps fail, but unvetted clones with assigned matching signatures still pass. |
| Full ten-factor toy product collapses when any slot is zero | proved in toy model | See `BridgeMatrix.full_*_zero_collapses`; still over `Nat`, not real-valued fields or integrals. |
| `tau_lock = 33 years` | conjecture / open | Needs a derivation or should remain an explicit free parameter. |
| Incarnation maps to localization | conceptual | Needs operation-preservation definitions. |
| Crucifixion maps to release / cost payment | conceptual | Needs energy-accounting formalism. |
| Resurrection maps to vacuum confirmation | conceptual | Needs a formal retained-property model. |
| Pentecost maps to coupling redistribution | empirical / conceptual | Needs observable definitions and historical test protocol. |
