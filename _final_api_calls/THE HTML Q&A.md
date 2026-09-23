

HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML HTML


Yes. That's a better representation than giving you an architectural essay first.

What you want is essentially a **field-by-field reconstruction of what the builder is interrogating**, grouped by object type. Then when you give me the neutral/non-discriminating questions, we can lay them beside this and determine:

$$
\text{Question}
\rightarrow
\text{information elicited}
\rightarrow
\text{ATOM field}
\rightarrow
\text{gap/duplicate}
$$

From the 19 screenshots, I can start the reconstruction like this.

# 1. CLAIM

## A. Identity / preservation

The system first asks:

| Field                  | Question it is really asking                                         | Expected answer/output                   |
| ---------------------- | -------------------------------------------------------------------- | ---------------------------------------- |
| **Atom Family**        | Which enduring assertion is this?                                    | Immutable `A###` identity                |
| **Layer**              | Where does this assertion operate in the dependency stack?           | `L#`                                     |
| **Component**          | Is this one independently gradable assertion within a larger bundle? | `C#`                                     |
| **UUID**               | Which exact database object is this?                                 | Unique machine identifier                |
| **Record Version**     | Which version of this claim are we evaluating?                       | Semantic version                         |
| **Version Operation**  | Is this new, revised, superseding, etc.?                             | Version relationship                     |
| **Prior Atom@Version** | What earlier state did this come from?                               | Parent version reference                 |
| **Change Rationale**   | Why did the claim change?                                            | Explicit explanation                     |
| **Source URI**         | Where did the assertion originate?                                   | File/URL/source pointer                  |
| **Source Span**        | Exactly where in the source?                                         | Lines/paragraph/chars                    |
| **Raw Statement**      | What exactly was originally claimed?                                 | Immutable verbatim text                  |
| **Author/Witness**     | Who originated the assertion?                                        | Person/source identity                   |
| **AI Contribution**    | Did AI participate?                                                  | yes/no + provider/model/role/run receipt |

The governing idea is:

$$
\boxed{\text{Preserve what was actually said before interpreting it.}}
$$

---

# 2. CLAIM OPENING

Then the system asks:

> **What exactly is this claim saying?**

This is not summarization. It is decomposition.

## Core statement

| Field                                 | Actual question                                                     | Output                      |
| ------------------------------------- | ------------------------------------------------------------------- | --------------------------- |
| **Statement — Technical**             | What is the exact proposition, preserving scope and quantifiers?    | Formal/technical statement  |
| **Statement — Plain**                 | What is the equivalent statement an ordinary reader can understand? | Plain-language equivalent   |
| **Scope**                             | Where does this claim apply?                                        | Domain/range                |
| **Quantifiers & Boundary Conditions** | Is this all, some, conditional, local, model-specific?              | Explicit logical boundaries |

And there is a crucial constraint:

$$
\boxed{\text{Plain statement must be equivalent, not stronger.}}
$$

---

# 3. CLAIM REGISTER

Then ATOM asks:

> **What kind of burden does this assertion carry?**

Not:

> Where did I find it?

The screenshots show register choices approximately:

* Formal / Mathematical
* Empirical / Physical
* Historical
* Informational
* Consciousness / First-person
* Moral / Normative
* Theological / Confessional
* Bridge / Cross-register
* Interpretive
* Predictive
* Protocol

That's important because the **questions change according to the burden of the claim**.

A mathematical theorem shouldn't be interrogated like historical testimony.

An empirical measurement shouldn't be interrogated like theology.

A bridge shouldn't inherit the authority of either endpoint.

---

# 4. CLAIM CLASSIFICATION

Then there are several **independent classifications**, rather than one giant status.

### Status

Where does it stand now?

`draft / proposed / weakened / falsified / deprecated / superseded`

### Claim class

What function does it perform?

`floor-axiom / definition / theorem / bridge / empirical-anchor / prediction / boundary`

### Lifecycle

What has happened to it operationally?

`RAW → PRESERVED → DECOMPOSED → OPENED → TESTED → CANDIDATE → HUMAN_REVIEW → RETURNED / WITHDRAWN / FALSIFIED / SUPERSEDED / DEPRECATED`

### Register

What kind of epistemic burden?

The register list above.

### Proof class

If formal proof is relevant:

`NOT_ATTEMPTED / SPECIFICATION_ONLY / INFORMAL_ARGUMENT / FORMALIZED_NOT_BUILT / BUILT_WITH_ASSUMPTIONS / BUILT_WITH_SORRY / BUILT_ZERO_SORRY / COUNTERMODEL_FOUND / FALSIFIED`

### IC grade

How much structure does a proposed correspondence preserve?

`IC-0 ... IC-5`

### Why-Closure

Has the explanatory question actually closed?

`WHY_OPEN / WHY_CLOSED / WHY_FAILED`

This is one of the strongest parts of what you've built:

$$
\boxed{
\text{Status}
\neq
\text{Proof}
\neq
\text{Register}
\neq
\text{Correspondence Strength}
\neq
\text{Why-Closure}.
}
$$

---

# 5. CLAIM DEPENDENCIES

Now the builder asks:

> **What does this assertion actually depend upon?**

The graph includes typed relationships such as:

`dependsOn`

`defines`

`interprets`

`bridgesTo`

`expands`

`forksFrom`

`instantiates`

`supersedes`

`corrects`

`challenges`

And crucially:

> **A relationship is not automatically an inference.**

So ATOM asks:

| Question                                 | Output                       |
| ---------------------------------------- | ---------------------------- |
| What are the load-bearing prerequisites? | `dependsOn` Atom@Version IDs |
| What does this bridge to?                | Bridge targets               |
| What challenges it?                      | Rival/challenge atoms        |
| What did it fork from?                   | Ancestry                     |
| What does it supersede?                  | Replaced claim               |
| Is it a child expansion?                 | Parent atom                  |
| If this fails, what else actually fails? | **Blast radius**             |

That last field is excellent.

It prevents:

$$
A\text{ fails}\Rightarrow\text{everything vaguely connected to A fails}.
$$

Failure propagates only through licensed, load-bearing dependencies.

---

# 6. CLAIM TRUTH SPACE

Now we're finally asking the adversarial questions.

### Exact negation

> **What exactly would it mean for this claim to be false?**

Output:

$$
\neg C
$$

not merely “someone disagrees.”

### Kill condition

> **What concrete observation/result would falsify it?**

Preferably preregistered.

### Strongest rival

> **What is the best competing explanation?**

Not the easiest straw man.

### Interpretation boundary

> **What does this atom NOT establish?**

This prevents:

$$
\text{analogy}\rightarrow\text{identity}
$$

$$
\text{model consistency}\rightarrow\text{world truth}
$$

$$
\text{Lean theorem}\rightarrow\text{physical confirmation}
$$

etc.

### Correction ledger

> What did we get wrong, and what replaced it?

Importantly, the old claim remains visible.

That gives:

$$
\boxed{\text{correction is additive history, not silent rewriting}.}
$$

---

# 7. CLAIM TERMINUS

Then comes a question I think will be extremely relevant when you give me the neutral questions:

> **When are we actually allowed to stop asking why?**

ATOM currently recognizes:

### `PRIMITIVE`

The present grammar cannot open it further without presupposing what it is trying to explain.

### `INDEPENDENT_EMPIRICAL_INPUT`

The system uses an observed/measured input it does not itself derive.

### `OPEN`

There remains an unresolved dependency, mechanism, rival, or test.

And then it asks:

* Why does expansion stop here?
* If OPEN, what exactly remains unresolved?
* What candidates already exist?
* What has already failed?
* What next discriminating test could settle it?

Plus your **No-Borrowed-Answer Rule**:

> You cannot terminate an explanation merely by naming the desired conclusion.

That's substantial.

---

# 8. EVIDENCE

Evidence gets an entirely different interrogation.

The governing question is:

> **What speaks for, against, or between alternatives?**

The anatomy visible in the screenshots is:

$$
\boxed{
Source
\rightarrow
Provenance/Custody
\rightarrow
Protocol
\rightarrow
Conditions
\rightarrow
RawRecord
\rightarrow
DerivedArtifacts
\rightarrow
Controls
\rightarrow
Independence
\rightarrow
Discrimination
}
$$

### Source

Questions:

* What is the actual originating object?
* Where do the bytes live?
* What's its cryptographic hash?
* Were the original bytes retained?
* If not, what surrogate exists and what may have been lost?

### Provenance & custody

* Who possessed it?
* When?
* What transformations occurred?
* Can integrity be demonstrated?
* Where are the gaps?

### Protocol

* How was this evidence generated?
* Sampling method?
* Instrument?
* Interview procedure?
* Measurement schedule?
* Was it preregistered?
* What were the stopping conditions?
* If no protocol exists, is it actually testimony/anecdote/uncontrolled observation?

### Conditions

* Under what time?
* Environment?
* Population?
* Range?
* Scale?
* Context?
* Instrument configuration?
* Observer position?

### Raw record

> **What is the least-processed observation actually available?**

Preserve:

* missing data;
* illegibility;
* sensor dropout;
* uncertain translation;
* corruption.

### Derived artifacts

* What was generated from the raw record?
* By which process/version/parameters?
* What information was removed?
* What was merged?
* What was inferred?
* What was added?
* Can we reverse the transformation and recover the raw record?

This is an extremely important separation:

$$
\boxed{\text{observation}\neq\text{analysis of observation}.}
$$

### Controls

* What happens when the proposed effect is absent?
* Negative control?
* Positive?
* Sham?
* Blank?
* Permutation?
* Holdout?
* Hostile witness?
* Which controls are impossible?
* What discrimination is lost because they're impossible?

### Independence map

* Do five records really represent five independent observations?
* Shared source?
* Witness?
* Instrument?
* Dataset?
* Analysis code?
* Assumptions?
* Funding?
* Common causal origin?

Output:

$$
\boxed{\text{effective independent evidence structure}}
$$

rather than raw citation count.

### Discrimination statement

This may be the central evidence question:

> **What would this evidence look like if the target claim were false?**

Then:

* target claim;
* strongest rival;
* expected record under falsity;
* actual observed record;
* exact difference carrying evidentiary weight;
* residual ambiguity.

That's excellent.

---

# 9. PROOF

Proof gets another anatomy:

$$
\boxed{
Premises
\rightarrow
InferenceRules
\rightarrow
DerivationSteps
\rightarrow
Conclusion
\rightarrow
AssumptionRegister
\rightarrow
Receipt
\rightarrow
InterpretationBoundary
}
$$

### Premises

* Which Atom IDs?
* What kind of premises?
* Definition?
* Axiom?
* Boundary condition?
* Imported theorem?
* Empirical input?
* Root-conditioned assumption?
* Temporary hypothesis?
* **Which premise did we use without acknowledging it?**

### Inference rules

* What licenses each transition?
* Logical rule?
* Algebraic transformation?
* Induction?
* Theorem invocation?
* Deductive?
* Inductive?
* Abductive?
* Statistical?
* Analogical?

This prevents different inferential strengths from being silently mixed.

### Derivation steps

For each:

$$
input\rightarrow rule\rightarrow output
$$

plus dependencies and verification state.

### Conclusion

* What exactly was established?
* Quantifiers preserved?
* Types preserved?
* Scope preserved?
* Model restrictions preserved?
* Which separate claim atom contains that conclusion?
* Can it be rendered plainly **without adding anything**?

### Assumption register

* Every explicit assumption.
* Every imported assumption.
* What changes when each is removed?
* Which are load-bearing?
* Which belong to formulation?
* Which belong to derivation?

### Receipt

* theorem/file;
* repository revision;
* source hash;
* toolchain;
* dependencies;
* command;
* exit code;
* warnings;
* `sorry/admit` count;
* runtime environment;
* date;
* operator;
* what was actually checked;
* what was **not** proved.

### Interpretation boundary

Again:

> **What does this proof not establish?**

Mandatory.

---

# 10. PROCESS

And finally, Process is not Evidence and not Proof.

It asks:

> **What procedure generates, transforms, audits, or tests?**

Anatomy:

$$
\boxed{
Purpose
\rightarrow
Inputs
\rightarrow
Preconditions
\rightarrow
Steps
\rightarrow
DecisionPoints
\rightarrow
Outputs
\rightarrow
DiscriminatingPower
\rightarrow
FailureModes
\rightarrow
Version
\rightarrow
RunReceipt
}
$$

### Purpose

One bounded capability.

Not “determine truth.”

Something like:

> validate schema conformance.

### Inputs

* accepted object types;
* schemas;
* versions;
* required fields;
* immutable source references;
* hashes where reproducibility matters.

### Preconditions

* dependencies;
* toolchain;
* permissions;
* calibration;
* blinded keys;
* preregistration;
* human selection;
* candidate isolation.

### Steps

Enough detail for independent reproduction.

Each step states:

* reads;
* writes;
* preserves.

### Decision points

Where does judgment enter?

What thresholds exist?

What branches?

What exceptions?

Which decisions require a human?

### Outputs

What object is produced?

Claim candidate?

Evidence?

Receipt?

Projection?

Canonical mutation?

Critically:

$$
\boxed{\text{AI extraction produces candidates, not admitted claims}.}
$$

### Discriminating power

* What can this process distinguish?
* **What can it NOT distinguish?**

This is a field I particularly want to compare against your neutral questions.

### Failure modes

* invalid input;
* unresolved references;
* stale schema;
* leakage;
* post-hoc criteria;
* non-independent controls;
* tool failure;
* partial writes;
* nondeterminism;
* reviewer override;
* false-success state.

Then for every failure:

* detection;
* safe halt;
* preserved artifacts;
* recovery path.

### Version

What materially changed?

### Run receipt

Specification is separated from execution.

A process can exist without ever having been run.

A successful run establishes only what that execution establishes.

---

# 11. HUMAN ADMISSION

And then the whole machine stops.

Automation can:

extract,

segment,

validate,

hash,

propose,

test,

find missing fields,

calculate blast radius.

But it **cannot canonize**.

The final questions are:

* Who should review?
* What should the reviewer consider?
* What remains unresolved?
* What candidate graph is being presented?
* What explicit human ruling was made?

So:

$$
\boxed{
\text{Candidate Graph}
\xrightarrow{\text{Human Ruling}}
\text{Admitted Graph}
}
$$

That's the system I see in your screenshots.

---

## Now give me the non-discriminating questions

Because **that comparison is going to be very revealing**.

I don't want merely to ask:

> “Do we already have this question?”

For each neutral question, I want to map:

$$
Q_i
\rightarrow
\text{what information it extracts}
\rightarrow
\text{which ATOM object it belongs to}
\rightarrow
\text{which exact field(s) receive the answer}
$$

and then classify it as:

$$
\boxed{
\text{EXACT MATCH}
/
\text{PARTIAL MATCH}
/
\text{DUPLICATE}
/
\text{MISSING FROM ATOM}
/
\text{ATOM ASKS SOMETHING STRONGER}
}
$$

And there's another possibility I'm specifically watching for:

$$
\boxed{\text{QUESTION OCCURS TOO LATE}}
$$

because ATOM may contain the right question but ask it **after an interpretation/classification has already biased the object**.

That could be one of the things that broke the original intake.

So yes—**this is now laid out at the level you were asking for. Give me the neutral/non-discriminating questions next, and we'll align them against this exact anatomy rather than redesigning anything yet.**
