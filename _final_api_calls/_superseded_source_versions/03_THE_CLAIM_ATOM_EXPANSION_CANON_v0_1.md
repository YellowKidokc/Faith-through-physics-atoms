# THE CLAIM ATOM EXPANSION CANON v0.1
## How a claim opens, how isomorphism is found, how the universal grammar emerges
## Drafted 2026-08-25 | Sits under THE UNIFIED GRAMMAR METHODOLOGY v1.0 | Matches repo structure: Faith-through-physics-atoms

---

## 1. THE ATOM

The atom is the unit of the corpus: one claim record, carrying the minimal unified record of the methodology (§6). One atom = one assertion, one hash, one state, one grade.

**Address scheme** (as deployed in the repo):

```text
claims / A042 / L9 / C1
        atom   layer  componentnow we're going to go to the expansion rule right 
```

- **Atom (A###):** the claim's immutable identity. Never reused, never deleted.
- **Layer (L#):** the DG layer the claim operates at — what it depends on, what it adds.
- **Component (C#):** the decomposed sub-claims of a bundled statement (Blind Reconstruction §4.1). A bundle of three claims is C1, C2, C3 — graded separately, because components may fail independently.

**Dual format, one source:** every component exists as `.jsonld` (machine-readable, linked data) and `.html` (human-readable), generated deterministically from the same canonical object. The projection is never a second truth store.

**Every atom carries:** the claim/evidence/proof spine (object type), plus the five axes — lifecycle state, proof class, register, IC grade, WHY-closure outcome.

---

## 2. THE EXPANSION RULE

A claim "opens" along its register. Each register has a native expansion template — the anatomy of what must be true for that kind of claim to hold. Opening an atom means producing its register-native sub-atoms, each of which is itself an atom with its own address.

### History claim → the transmission chain (Blind Reconstruction §4.7)

```text
EVENT → POSSIBLE OBSERVERS → WITNESS → TESTIMONY → TRANSMISSION
→ DOCUMENT → PRESERVATION → CORROBORATION → INTERPRETATION → PRESENT CLAIM
```

Each link is a sub-atom. At every link, record where information could be preserved, lost, changed, added, selectively reported, or independently confirmed. A historical claim is exactly as strong as its weakest preserved link — and the chain shows *which* link.

### Physics claim → the measurement anatomy

```text
QUANTITY → UNITS → DYNAMICS → PROTOCOL → INSTRUMENT → DATA → CONTROLS → FIT → CLAIM
```

Sub-atoms carry units, error bars, the protocol, and the negative controls. A physics claim without units and protocol does not open — it returns `DISCOVERY_INCOMPLETE`.

### Math claim → the formal anatomy

```text
DEFINITION → AXIOM USE → LEMMA → DERIVATION → THEOREM STATEMENT → RECEIPT
```

The receipt sub-atom carries the class: NOT_ATTEMPTED / SPECIFICATION_ONLY / … / BUILT_ZERO_SORRY. The theorem proves exactly what its statement says — the Books lesson is enforced by the address structure: the *specification* and the *proof* are different sub-atoms.

### Theological claim → the proclamation anatomy

```text
SOURCE → WITNESS TRADITION → PROCLAMATION → REGISTER → CONFESSION CLASS → SCOPE
```

Theological atoms are declared as theological (class S or C). They are never laundered into class T or E by expansion. Expansion clarifies what the claim *is*; it never upgrades what the claim *proves*.

### Bridge claim → the mapping anatomy

```text
SOURCE REGISTER → TARGET REGISTER → MAPPING → PRESERVED → LOST → GRADE → COUNTERMODELS → NEXT TEST
```

A bridge atom that cannot name its lost structure does not open. The loss field is mandatory.

---

## 3. THE ISOMORPHISM RULE

When two atoms — from any two registers — are both fully opened, their **invariant signatures** can be compared without names (BFP-DG §8):

```text
IDENTITIES · DISTINCTIONS · RELATIONS · OPERATIONS · DEPENDENCIES
· CONSTRAINTS · INVARIANTS · COLLAPSE CONDITIONS · CONSEQUENCES
```

If the signatures match, an isomorphism **candidate** is born:

1. **Discovery, not assertion.** The match is found by comparing opened structures, never declared from vocabulary resemblance.
2. **Grading.** The candidate receives IC-0 through IC-5. Only IC-4 (shared dependency graph and capability classes) or IC-5 (plus collapse and translation behavior) supports a serious structural-convergence claim.
3. **The pressure test.** Remove the labels. Permute the pairings. Construct the strongest rival mapping. Measure whether the preferred mapping has a real advantage.
4. **The Why-Gate.** The isomorphism must face: why does this correspondence exist? WHY_CLOSED (with level), WHY_FAILED, or WHY_OPEN — and WHY_OPEN is preserved, not resolved.
5. **The bridge record.** A surviving isomorphism is stored as a bridge atom (class BR) naming preserved structure, lost structure, grade, countermodels, and the next discriminating test. It propagates as a bridge — never as a proof.

---

## 4. THE UNIVERSAL GRAMMAR

The universal grammar is not a document someone writes. It is the **emergent structure** of the admitted graph:

```text
UNIVERSAL GRAMMAR = the set of all admitted atoms
                  + all confirmed isomorphisms (IC-4/5, WHY-gated)
                  + the typed dependency edges between them
                  viewed whole.
```

It is built bottom-up from verified expansions, never top-down from imposed categories. That is why it will work if anything does: every node in it earned its place through the pipeline, every isomorphism survived the pressure test, and every gap is marked OPEN rather than filled with preference. The grammar is what remains when everything that could not survive scrutiny has been honestly removed — and everything that survived is still wearing its grade.

---

## 5. THE RECURSION AND THE FLOOR

Atoms contain atoms. Expansion continues downward until it reaches one of three termini:

- **PRIMITIVE** — the Mark: distinction itself. The floor of the grammar. No further opening is possible.
- **EMPIRICAL INPUT** — a measurement the framework does not derive. Recorded as INDEPENDENT_EMPIRICAL_INPUT.
- **OPEN** — an honest unresolved terminus. Preserved with its rivals and its next test.

No expansion may terminate in a label borrowed from the answer. That is the whole discipline in one sentence.

---

## 6. THE GUARDS (non-negotiable, inherited)

- Analogy is never promoted to identity.
- A bridge never propagates as proof.
- A specification is never reported as a theorem.
- A selection criterion is never written after the pattern is seen.
- No automated run canonizes; the human rules admission.
- Corrections print where claims printed; nothing is silently edited or deleted.
- The resolver resolves references; it never creates authority.
- The guard tool enforces format; it never grades truth.

---

## 7. THE ONE-SENTENCE VERSION

**Every claim is an atom; every atom opens along its register into sub-atoms; when two opened structures match without names, an isomorphism is born, graded, and gated — and the universal grammar is simply everything that survives.**
