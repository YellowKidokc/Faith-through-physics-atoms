# Claim Hygiene for Formal Correspondence

Theology does not need to become natural science for structural correspondence
with physics to be possible.  It needs enough formal clarity that a claimed
correspondence can be stated, checked, and killed.  Physics likewise needs
enough formal clarity that the physical side of the map is not a cartoon.

The bridge is a third thing: formal correspondence theory.  It is not the
conversion of theology into laboratory science, and it is not the conversion of
physics into doctrine.

## Valid Claim Shape

Use this form for the strengthened Lean rows:

> We defined formal models and proved that, inside those declared models, the
> stated gate, collapse, preservation, or isomorphism condition holds.

For Law 4:

> We defined `StrongForceLaw` and `LoveLaw` and proved that an isomorphism
> witness exists under `LawIso`, with a stronger witness under `RichLawIso`.

For Laws 1, 2, 3, 6, 7, and 8:

> We defined formal gate/control models and proved that the listed healthy
> conditions pass, while listed failure conditions force the relevant factor to
> zero and therefore collapse the master-product `chi`.

## Invalid Claim Shape

Do not market the formal rows as proving any of the following:

- theology has become natural science,
- physics and theology are the same discipline,
- QCD itself is identical to biblical love,
- Lean has proven Christian doctrine from physics,
- a theorem about a declared model automatically proves the adequacy of that
  model for the intended physical or theological subject.

## Remaining Burden

After a Lean theorem compiles, the next burden is adequacy and non-triviality:

- Does the formal physical model faithfully represent the intended physical
  structure?
- Does the formal theological model faithfully represent the intended doctrinal
  or metaphysical structure?
- Do rival or relabeled models also pass the same test?
- Are the public words limited to exactly what the theorem states?

This keeps the project rigorous without collapsing either domain into the
other.

## Citation Rule for Exported Theorems

Every externally cited theorem must be cited with this triple:

1. Exact statement: quote or link the Lean type, not only the English slogan.
2. Claim class: say whether it is a formal-model theorem, gate theorem,
   collapse theorem, isomorphism-witness theorem, adversarial boundary theorem,
   or adequacy argument.
3. Non-claim: explicitly state what the theorem does not prove.

## Law 1-8 Export Surface

| Theorem family | Exact claim class | Valid public wording | Required non-claim |
| --- | --- | --- | --- |
| `law1_mechanism_gate_marker`, `law2_mechanism_gate_marker` | Formal gate theorem | The declared healthy Law 1/2 control models pass their formal gates. | Does not prove the corresponding theological terms are physical fields. |
| `full_*_zero_collapses` | Formal product-collapse theorem | If the named factor is zero in the declared `chi` product model, `chi x = 0`. | Does not prove that real-world coherence requires that theological reality. |
| `law3_*_collapses_chi` | Formal gate-to-product theorem | A declared Law 3 control failure writes `E = 0`, and the formal product collapses. | Does not prove empirical truth-fidelity or revelation theory. |
| `law6_*_collapses_chi`, `law6_logos_limit_K_one` | Formal gate-to-product theorem | The declared Law 6 controls determine whether the formal `K` gate passes or collapses. | Does not prove Logos doctrine from compression physics. |
| `law7_*_collapses_chi`, `law7_righteous_limit_R_one` | Formal gate-to-product theorem | The declared Law 7 controls determine whether the formal `R` gate passes or collapses. | Does not prove righteousness as a physical threshold. |
| `law8_*_collapses_chi`, `law8_faith_limit_Q_one` | Formal gate-to-product theorem | The declared Law 8 controls determine whether the formal `Q` gate passes or collapses. | Does not prove faith as quantum measurement. |
| `law4Iso`, `richLaw4Iso` | Formal isomorphism-witness theorem | The declared `StrongForceLaw` and `LoveLaw` models admit `LawIso` and `RichLawIso` witnesses. | Does not prove QCD itself is biblical love. |

## Adversarial Boundary Rule

Any isomorphism theorem needs a companion boundary test.  In particular,
`weak_law_iso_admits_coin_countermodel` shows that a generic two-state coin
model can also inhabit the base `LawIso` shape.  Therefore base `LawIso` alone
does not establish theological adequacy; richer structure and non-triviality
tests are required.
