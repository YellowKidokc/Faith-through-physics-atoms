# THE VOCABULARY
## The one place every classification in Faith Through Physics is declared
## POF 2828 | fills the slot atoms already reference: /vocab/context.jsonld

Every atom in this repo declares `@context` pointing here. Until now that
URL resolved to nothing. This is that file — the controlled vocabulary the
whole framework reads from.

**The rule: nothing is classified anywhere else.** A domain, a tag, a node
type, a glyph, a verification method — it is declared HERE and referenced
everywhere. If a classifier invents a category, the category is wrong or
the vocabulary is incomplete. Those are the only two options.

---

## THE SIX AXES

Every atom is located by six independent coordinates. Five are from the
GPT review (`GOVERNING_RULES_FINAL.md`); the sixth is the lexical layer
that was missing and without which nothing can be matched automatically.

| # | Axis | Question | Field |
|---|------|----------|-------|
| 1 | Type | What is it? | `nodeType` |
| 2 | State | What is its epistemic state? | `status` |
| 3 | Domain | Where does it apply? | `domainType` |
| 4 | Audience | For whom is it rendered? | `audienceLevel` |
| 5 | Provenance | How was it derived? | `edges[]`, `evidenceType`, `verifiedBy` |
| 6 | **Lexical** | **What is it ABOUT?** | **`tags[]`, `keywords[]`, `glyphs[]`, `mathFormNormal`** |

Axis 6 is the matching engine. Axes 1–5 describe an atom. Axis 6 lets
atoms FIND each other. Without it every edge must be hand-authored.

---

## AXIS 1 — nodeType (what is it)

Only `claim` is a claim. Everything else orbits claims.

| Glyph | nodeType | Stage | What it is |
|---|---|---|---|
| ◌ | `raw` | 00 | Captured, unclassified. Orphan until typed. |
| ◆ | `claim` | 01 | **THE atom.** Only type that gets a `claimID`. |
| ⊘ | `paradigm` | 02 | What this breaks about old thinking. |
| ≅ | `bridge` | 03 | Cross-domain mapping. Carries a grade. |
| ⧖ | `prediction` | 04 | Testable, timestamped forecast. |
| E | `evidence` | 05 | External data. Not a claim. |
| ⛔ | `kill` | 06 | Kill condition + attempt + outcome. |
| ▤ | `paper` | 07 | Composite. Assembles truth, doesn't hold it. |
| ⚔ | `objection` | 08 | Steelmanned pushback + response. |
| ☖ | `translation` | 09 | Meaning-preserving restatement. |
| ⊙ | `check` | 10 | Pressure test of the translation. |
| ✍ | `article` | 11 | Narrative treatment. |
| ⌘ | `reach` | 12 | SEO, social, toolkit, one-pager. |
| ⟡ | `result` | 13 | What happened. Closes a prediction. |
| ↦ | `application` | — | **Inferential leap to advice.** Declares added premises. |

`application` is NOT a stage folder — it is a node type that can attach
anywhere below a claim. Translation preserves meaning; application adds
premises. They are separate operations and must be separate nodes.

---

## AXIS 2 — status (epistemic state)

| Glyph | status | Meaning |
|---|---|---|
| ◌ | `captured` | Exists, unprocessed |
| ◇ | `classified` | Typed and filed, not asserted |
| ❖ | `proposed` | Asserted, unsupported |
| ● | `active` | Supported, in use |
| ◆ | `verified` | Burden met for its claimClass |
| ⊢ | `kernel_verified` | Machine-checked in Lean 4 |
| ⊝ | `weakened` | Survived a kill attempt with damage |
| ⊗ | `falsified` | Kill condition fired |
| ⊠ | `deprecated` | Withdrawn |
| ⇄ | `superseded` | Replaced; pointer to successor required |

---

## AXIS 3 — domainType (where it applies)

Root layer sits above domains. Every domain gets a glyph so a type
signature reads at a glance. Six existed; the rest are assigned here.

### Root layer (above all domains)
| Glyph | domain | Note |
|---|---|---|
| ☉ | `god` | The source. Not a domain — the ground. |
| ⟁ | `trinity` | Triadic structure |
| Μ | `master-equation` | χ, the ten variables |
| Α | `axioms` | 22 public / 188 technical |
| ℒ | `ten-laws` | The ten, with symmetry pairs |
| ✝ | `scripture` | Canonical text |
| Θ | `theology` | Canonical doctrine |

### Domains
| Glyph | domain | Glyph | domain |
|---|---|---|---|
| Φ | `physics` | ψ | `consciousness` |
| ℹ | `information-theory` | β | `biology` |
| ⚖ | `ethics` | ⊛ | `cosmology` |
| ⚕ | `pharmacology` | ⚗ | `addiction-science` |
| ⌬ | `chemistry` | ☣ | `epidemiology` |
| ✿ | `ecology` | ♒ | `fluid-dynamics` |
| ⚙ | `control-theory` | ⟐ | `mathematics` |
| ⇉ | `network-science` | ♫ | `music-theory` |
| ⚿ | `cryptography` | ✎ | `education` |
| ⌛ | `history` | ☗ | `economics` |
| ☯ | `psychology` | ✚ | `christian-life` |
| ⟦AI⟧ | `ai-alignment` | ⚑ | `politics` |
| ⚓ | `law` | ⌂ | `sociology` |
| ⚛ | `quantum` | ⊞ | `linguistics` |
| ⚘ | `agriculture` | ⚒ | `engineering` |
| ☤ | `medicine` | ✇ | `technology` |
| ⚔ | `military-history` | ☰ | `philosophy` |
| ⚜ | `art` | ⌖ | `statistics` |

**Adding a domain:** add the row here first, then run
`_scripts/new_domain.py`. A domain folder without a vocabulary row is
invisible to the classifier and will be back-filled with guesses.

---

## AXIS 4 — audienceLevel (for whom)

| Glyph | audienceLevel | Reading target |
|---|---|---|
| ⊢ | `specialist` | Domain expert, formal notation assumed |
| ▤ | `doctoral` | Academic, full derivation expected |
| ◈ | `informed_adult` | Curious layperson, math explained |
| ✚ | `pastor` | Teaching-oriented, doctrine-forward |
| ⌂ | `parent` | Applied, home and family framing |
| ⚑ | `policymaker` | Decision-relevant, consequence-forward |
| ☖ | `everyday` | Monday-morning plain language |
| ✎ | `child` | Grade 4–8 |

The push-down rule in vocabulary terms: **a claim is not descent-complete
until at least one reviewed path reaches `everyday`.**

---

## AXIS 5 — provenance (how it was derived)

### evidenceType — the missing controlled vocabulary
Answers "does it have mathematics, is it logical, is it measured."

| Glyph | evidenceType | What backs the claim |
|---|---|---|
| ⟐ | `formal_derivation` | Proof from stated axioms |
| ⊢ | `machine_verified` | Lean 4 kernel-checked |
| ∫ | `mathematical_model` | Equation with defined terms |
| ⌖ | `statistical` | Dataset, denominator, reproducible calc |
| E | `empirical` | Defined observation + method |
| ⧗ | `historical` | Primary or credible secondary source |
| ✝ | `textual` | Exact passage + translation note |
| Θ | `interpretive` | Stated interpretive premises |
| ≈ | `analogical` | Resemblance only — **never propagates** |
| ◊p | `personal` | Author disclosure, testimony |

### verifiedBy — who or what checked it
| Glyph | method | | Glyph | method |
|---|---|---|---|---|
| ⊢ | `lean4` | | ω | `wolfram` |
| π | `python` | | ⑦ | `seven_question` |
| AI | `ai_review` | | ⌥ | `human_review` |
| NLP | `nlp_pass` | | F | `facts_card` |

### edge types + bridge grades (unchanged from the atom spec, indexed here)

| Glyph | edge type | Meaning |
|---|---|---|
| ↓ | `dependsOn` | Needs the target to stand |
| → | `feedsInto` | Contributes to the target |
| ≅ | `bridgesTo` | Cross-domain mapping — carries a grade |
| ⚔ | `challenges` | Attacks the target |
| ⇧ | `expands` | Extends the target's scope |
| ⑂ | `forksFrom` | Divergent variant |
| ↦ | `descendsTo` | Toward a broader audience — carries a Descent Invariant |

| Glyph | bridge grade | Propagates falsification? |
|---|---|---|
| ≡ | `structural_identity` | **YES** — same equation, renamed variables |
| ≅ | `structural_isomorphism` | **YES** — shared logical architecture |
| ≈ | `structural_analogy` | no — resemblance, flagged for review |
| ~ | `metaphorical` | no — illustrative only |

### paradigmRelation — what a claim does to prior thinking
| Glyph | value | Meaning |
|---|---|---|
| ⊘ | `breaks` | Prior frame is wrong, not incomplete |
| ⇧ | `extends` | Prior frame holds, scope widens |
| ⟲ | `reframes` | Same facts, different organizing principle |
| ✓ | `confirms` | Independently re-derives prior result |
| ⊙ | `orthogonal` | Prior frame neither helped nor hurt |

---

## AXIS 6 — THE LEXICAL LAYER (the matching engine)

This is what was missing. Axes 1–5 describe an atom; this axis lets atoms
find each other. Four fields, in order of matching strength:

### 1. `mathFormNormal` — strongest signal
The equation rewritten in canonical form with **role names, not domain
names**, so the same structure matches across domains.

```
Trilemma  raw: "J = T_A/D, M = 1 - T_B/D, T_A = T_B => J = 1 - M"
        normal: "a = x/d ; b = 1 - y/d ; x = y => a = 1 - b"
```
Any two atoms whose `mathFormNormal` matches are **candidate structural
identities** — the strongest bridge grade — regardless of domain. This is
the field that makes cross-domain matching computable instead of intuitive.

### 2. `glyphs[]` — the type signature (exactly 5 slots, positional)
Compact machine+human readable declaration prefixing a canonical block.
**Slots are positional and fixed:**

| Slot | Axis | Enum source |
|---|---|---|
| 1 | `status` | vocab.json → status |
| 2 | `nodeType` | vocab.json → nodeType |
| 3 | `scope` | domains_and_tags.json → root_layer + domainType |
| 4 | `evidenceType` | vocab.json → evidenceType |
| 5 | `primaryTag` | domains_and_tags.json → tags |

```
◆ ⟐ Μ ⊢ ⚖   = verified · proof · master-equation · lean-checked · justice
◇ ❖ ✎ ⌖ ☉   = draft · claim · education · statistical · truth
```

**`audienceLevel` and `verifiedBy` are metadata, not signature slots.** They
carry glyphs for display only and never occupy a positional slot. Five slots
is a hard constraint — if a sixth is needed, the atom is doing two jobs and
should be split.

Because slots are positional, cross-axis glyph reuse is unambiguous (`⊢` in
slot 1 = kernel_verified, in slot 4 = machine_verified). **Within-axis reuse
is illegal** unless the terms are declared members of one compression class
(see `compressions.json`).

### 3. `tags[]` — controlled, cross-domain concept anchors
Tags are the **concept vocabulary** — drawn from the theological/physical
term set. They are the layer that connects a physics atom to a theology
atom when the math hasn't been normalized yet. Controlled, not free.

| Glyph | tag | Glyph | tag | Glyph | tag |
|---|---|---|---|---|---|
| ✦ | `grace` | ⬒ | `sin` | ☉ | `truth` |
| ◒ | `deception` | ⚖ | `justice` | ♡ | `mercy` |
| ✝ | `cross` | ⟡ | `resurrection` | ⟠ | `faith` |
| ◌ | `doubt` | λ | `logos` | ✺ | `coherence` |
| ✣ | `decoherence` | ⇥ | `source-term` | ⛔ | `kill-condition` |
| ∩ | `covenant` | ⊕ | `atonement` | ↺ | `repentance` |
| ⇧ | `sanctification` | ⊙ | `witness` | ∴ | `entropy` |
| □ | `boundary` | ✺ | `glory` | ⟲ | `invariant` |
| ⊘ | `broken-symmetry` | ≔ | `definition` | χ | `variable` |
| ∫ | `equation` | ⟐ | `proof` | ≅ | `isomorphism` |

Add tags freely — but add them HERE, with a glyph, or the classifier
can't emit them.

### 4. `keywords[]` — free text, lowest strength
Uncontrolled. Feeds embedding similarity and full-text search only.
Never used to justify a bridge on its own.

---

## HOW MATCHING WORKS

```
1. mathFormNormal identical      -> candidate: structural_identity
2. mathFormNormal isomorphic     -> candidate: structural_isomorphism
3. shared axiomRoot              -> candidate: dependsOn or sibling
4. tag overlap >= 2 across domains -> candidate: bridge, grade UNKNOWN
5. keyword/embedding similarity  -> candidate: review only
```

**The machine proposes. The human grades.** A candidate edge is written
with `grade: "ungraded"` and `propagates: false` until a human assigns
the grade. Only identity and isomorphism propagate falsification, so an
ungraded edge can never silently kill a claim.

This is the engine behind "the atoms find each other." Without Axis 6 the
graph only contains edges someone typed by hand.
