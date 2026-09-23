# HTML Question Stage and Canonical-Home Crosswalk

**Audit date:** 2026-09-01  
**Status:** design and field-routing audit; no admission event  
**HTML inspected:** `D:/GitHub/nerve/source/html/atoms/atom-builder.html`  
**Question summary inspected:** `C:/Users/David/.codex/attachments/a8b7fa59-d954-4212-ae20-5c8d009a4a85/pasted-text.txt`

## Finding

The supplied question summary captures the builder's governing questions and most major field families, but it is **not literally every question or field in the HTML**. The live HTML also contains detailed register-native questions, the Math panel, the non-warrant Narrative panel, bridge tests, and several exact receipt and validation fields.

The system becomes coherent when the questions are divided into five moments:

1. **PRESERVE — before discovery:** source identity only; no interpretation.
2. **DISCOVER — before categories:** Q0–Q13 and B0–B8; inherited labels hidden.
3. **CLASSIFY — category gate:** Q14, followed by controlled object type, register, claim class, and burden.
4. **OPEN / TEST / TRANSLATE — after categories:** the appropriate Claim, Evidence, Proof, Process, or Bridge anatomy.
5. **RULE — governance:** candidate review and a separate signed admission event.

The HTML currently presents Address before Object Type, which is safe, but then asks Object Type before it runs the protected neutral question sequence. Therefore the HTML is a **post-discovery builder**, not the blind-discovery interface itself. Blind discovery must feed it; the builder must not be used as Call 1.

## Governing sequence

```text
SOURCE BYTES
→ PRESERVATION RECORD
→ Q0–Q13 FORWARD DISCOVERY
→ B0–B8 REVERSE RECONSTRUCTION
→ CONVERGENCE / WHY-CLOSURE
→ Q14 EMERGENT ROLE CLASSIFICATION
→ OBJECT TYPE + REGISTER + BURDEN
→ REGISTER-NATIVE OPENING
→ TRUTH SPACE / COUNTERMODELS / TESTS
→ RECONCILIATION
→ BRIDGE / TRANSLATION (only when required)
→ CANDIDATE PACKET
→ HUMAN RULING
→ SEPARATE SIGNED ADMISSION EVENT
```

## Crosswalk

| HTML question or field family | When asked | Neutral/canonical question source | Canonical answer home | Rule |
|---|---|---|---|---|
| Atom Family, UUID | PRESERVE | identity/provenance rail, not discovery | `atoms`; `atom_versions` | Identity does not certify truth. |
| Layer, Component | PRESERVE initially; REVIEW after classification | address resolver | `atom_addresses` | May be proposed early, but final placement is reviewed after classification. |
| Record Version, Version Operation, Prior Atom@Version, Change Rationale | PRESERVE | version/provenance rail | `atom_versions.prior_atom_version_id`; correction/version records | Never silently overwrite. |
| Source URI, Source Span, Raw Statement, Author/Witness | PRESERVE | source pinning before Q0 | `source_objects`; `source_spans`; `atom_version_sources`; `atom_versions.raw_statement` | Exact source survives every later pass. |
| AI Contribution/provider/model/role/receipt/detail | PRESERVE | provenance rail | `atom_version_sources.ai_contribution_declared`; `receipts`; metadata | AI participation must be explicit. |
| Exact expression / technical statement | DISCOVER Q0 | Q0 Exact Expression | `atom_versions.statement_technical`; `atom_items` | No register or inherited label supplied to the blind pass. |
| Plain equivalent | DISCOVER Q0/Q9 | exact expression + representation ladder | `atom_versions.statement_plain` | Plain form may not strengthen the technical form. |
| Referent | DISCOVER Q1 | Q1 Referent | `atom_items(item_kind='referent')`; claim anatomy JSON | Ask before naming its domain. |
| Identity and distinction | DISCOVER Q2 | Q2 Identity and Distinction | `claim_extensions.identity_conditions_json`; `atom_items` | Preserve equality, difference, and individuation conditions. |
| Dependencies / dependency floor | DISCOVER Q3 | Q3 Dependency Floor | candidate dependency items, later typed into `edges`/`edge_versions` | Discovery proposes dependencies; classification determines their edge type and warrant. |
| Variation and invariance | DISCOVER Q4 | Q4 Variation and Invariance | `invariant_signatures`; `atom_items` | Do not call it an isomorphism yet. |
| Capability and operation | DISCOVER Q5 | Q5 Capability and Operation | `atom_items`; later Claim/Process/Bridge anatomy | Describe behavior before assigning object type. |
| Transition | DISCOVER Q6 | Q6 Transition | `atom_items`; later process/proof steps if warranted | A temporal or logical transition is not yet a causal classification. |
| Constraint, scope, quantifiers, boundary conditions | DISCOVER Q7 | Q7 Constraint and Domain | `atom_versions.scope_text`; `claim_extensions.quantifiers_json`; `boundary_conditions_json` | The discovery answer stays label-free; controlled domain/register is assigned later. |
| Consequence and license | DISCOVER Q8 | Q8 Consequence and License | candidate consequence items; later typed proof/dependency edges | “Follows from” requires an inference license after classification. |
| Representation ladder | DISCOVER Q9 | Q9 Representation Ladder | `atom_items`; technical/plain/formal fields | Track what each rendering preserves and adds. |
| Preservation and loss | DISCOVER Q10 | Q10 Preservation and Loss | `invariant_signatures`; bridge payload only if a bridge is later classified | Lost structure is mandatory before a bridge grade. |
| True-world profile | DISCOVER Q11 | Q11 True-World Profile | `claim_extensions.truth_conditions_json` | State what would be so if the assertion holds. |
| False-world profile / exact negation / strongest rival | DISCOVER Q12 | Q12 False-World and Rival Profile | `claim_extensions.exact_negations_json`; `countermodels` | Countermodels are preserved even if the preferred claim survives. |
| Discrimination / next deciding observation | DISCOVER Q13 | Q13 Discrimination | `kill_conditions`; `open_items`; evidence discrimination fields | This is still pre-category structural discovery. |
| Emergent grouping | DISCOVER output only | Call 1 descriptive grouping | `atom_versions.emergent_labels_json` | Descriptive organization only; not controlled classification. |
| Emergent role classification | CATEGORY GATE | Q14 | controlled classification proposal / review record | Earliest point at which controlled labels may be proposed. |
| Object Type: Claim/Evidence/Proof/Process | CLASSIFY | Four-Object Law after Q14 | `atoms.object_type` | Exactly one primary type; bundled content is split. |
| Register | CLASSIFY | actual burden revealed by discovery | `atom_versions.register_code` | Burden, not file location, determines register. |
| Claim Class | CLASSIFY | role in framework | controlled term + atom version/item | Separate from status, lifecycle, and proof class. |
| Status | CLASSIFY/REVIEW | current candidate assessment | controlled status field/item | Must not mean admitted. |
| Lifecycle | RUNTIME/REVIEW | operational state | `atom_versions.lifecycle_state`; `graph_memberships` | Candidate lifecycle is distinct from epistemic warrant. |
| Proof Class | OPEN/TEST | only for proof-relevant objects | `atom_versions.proof_class`; `proof_extensions.receipt_class` | A build result never upgrades physical or theological truth. |
| IC Grade | TRANSLATE/TEST | only after explicit mapping and loss audit | `atom_versions.ic_grade`; `bridge_edge_payloads`; `bridge_tests` | Never inferred from vocabulary resemblance. |
| WHY Closure | CONVERGENCE/WHY GATE | why-closure questions | `atom_versions.why_outcome`; `why_gate_records` | OPEN is a valid result. |
| Terminus, justification, exact OPEN question, next test | CONVERGENCE/WHY GATE | why-closure and terminus tests | `atom_versions.terminus_type`; `open_items`; `kill_conditions` | A desired theological label cannot serve as closure. |
| dependsOn, defines, interprets, expands, forksFrom, instantiates, challenges | OPEN/RECONCILE | typed relationship review | `edges`; `edge_versions` | Relationship is not automatically inference. |
| bridgesTo | TRANSLATE only | native → bridge → identification sequence | bridge edge/payload and bridge atom | Never ask or assert during blind discovery. |
| supersedes, corrects | GOVERNANCE | correction/version review | `corrections`; `correction_impacts`; edge history | Prior claim remains visible. |
| Blast radius | REVIEW | load-bearing graph analysis | `correction_impacts`; dependency graph receipt | Propagate only through licensed load-bearing edges. |
| Kill condition | OPEN/TEST | Q13 plus native burden | `kill_conditions` | Prefer preregistration; absence remains visible. |
| Interpretation boundary | OPEN/TEST | burden-native limitation | `formalization_boundary`; proof/bridge/evidence limitations | Mandatory for proof and bridges. |
| Correction ledger | GOVERNANCE | post-test correction | `corrections`; `correction_impacts` | Additive history, never silent rewrite. |
| Claim register-native anatomy | POST-CATEGORY OPENING | selected by register after Q14 | `claim_extensions.register_anatomy_json`; typed child items | History, physics, math, theology, etc. receive different burdens. |
| Evidence Source / Custody / Protocol / Conditions / Raw Record | POST-CATEGORY EVIDENCE | Evidence anatomy | `source_objects`; `custody_events`; `evidence_extensions` | Evidence is preserved observation, not a claim that “supports.” |
| Derived Artifacts / information removed or added / reversibility | POST-CATEGORY EVIDENCE | Evidence anatomy | `derived_artifacts` | Derived output never masquerades as raw record. |
| Controls | POST-CATEGORY EVIDENCE | Evidence anatomy | `evidence_controls` | Missing controls become explicit limitations. |
| Independence Map | POST-CATEGORY EVIDENCE | Evidence anatomy | `independence_clusters`; `evidence_independence` | Copied reports are not independent convergence. |
| Discrimination Statement | POST-CATEGORY EVIDENCE | Evidence anatomy | `evidence_extensions.discrimination_statement`; evidence edge payload | Must name target claim and rival. |
| Proof Premises / hidden premise check | POST-CATEGORY PROOF | Proof anatomy | `proof_premises`; `proof_assumptions` | Every premise is typed and linked. |
| Inference Rules / Derivation Steps | POST-CATEGORY PROOF | Proof anatomy | `proof_steps` | Each arrow names its license. |
| Exact Conclusion / plain rendering / conclusion atom | POST-CATEGORY PROOF | Proof anatomy | `proof_extensions.formal_statement`; `conclusion_atom_version_id` | Conclusion is a separate claim atom and says no more than proved. |
| Assumption sensitivity | POST-CATEGORY PROOF | Proof anatomy | `proof_assumptions.sensitivity` | Identify load-bearing assumptions and what changes if removed. |
| Proof Receipt / what checked / what not proved | POST-CATEGORY PROOF | Proof anatomy | `receipts`; `proof_extensions.what_checked_json`; `what_not_proved_json` | Source hash and toolchain must match the theorem actually built. |
| Process Purpose / Inputs / Preconditions / Steps | POST-CATEGORY PROCESS | Process anatomy | `process_extensions`; `process_steps` | Specification is distinct from execution. |
| Process Decision Points / human choices | POST-CATEGORY PROCESS | Process anatomy | `process_steps.decision_actor_type`; process metadata | Subjective choices cannot hide inside deterministic-looking steps. |
| Process Outputs | POST-CATEGORY PROCESS | Process anatomy | `process_extensions.outputs_json` | Explicitly distinguish proposals, evidence, receipts, projections, and mutations. |
| Discriminating Power / cannot distinguish | POST-CATEGORY PROCESS | Process anatomy | `process_extensions.discriminating_power`; `cannot_distinguish` | A schema validator does not determine truth. |
| Failure Modes / detection / safe halt / recovery | POST-CATEGORY PROCESS | Process anatomy | `process_failure_modes` | False-success modes are first-class. |
| Process Version / Run Receipt | POST-CATEGORY PROCESS | Process anatomy | `process_extensions.process_version`; `process_runs` | A successful run establishes only its bounded output. |
| Bridge source/target registers and objects | TRANSLATE | Translation Grammar | `bridge_edge_payloads` | Both sides remain independently warranted. |
| Explicit mapping / preserved / lost / boundary | TRANSLATE | Translation Grammar | `bridge_edge_payloads`; `invariant_signatures` | Loss and boundary are mandatory. |
| Reverse map / commutativity / rival / grade | TRANSLATE/TEST | Translation Grammar | `bridge_tests`; `bridge_rivals`; IC grade | A one-way map is not an isomorphism. |
| Equation / term-by-term / Master Equation socket / behavior at limits | POST-CATEGORY MATH DISPLAY | Math panel and formal anatomy | claim items/formal record; no dedicated normalized SQL columns yet | These fields need a governed JSON extension or dedicated schema before they can be called canonical fields. |
| Narrative hook/excerpt/source/span/predicate/boundary | PRESENTATION ONLY | Narrative panel | projection/presentation record, source span | Narrative may illustrate or motivate; it may not support, falsify, test, or prove. |
| Proposed reviewer / date / handoff / unresolved fields | HUMAN REVIEW PREPARATION | candidate packet | candidate ruling packet / `open_items` | Preparing a ruling is not admission. |
| Human decision, actor, rationale | HUMAN RULING | review event | `rulings` | Allowed candidate decisions remain separate from admission. |
| Signed admission event | SEPARATE ADMISSION | admission schema | admitted `graph_memberships` plus signed ruling/event and hashes | The builder must never create this automatically. |

## Alignment problems found

1. **The attachment is a strong summary, not an exhaustive HTML inventory.** It omits many register-native subquestions and exact field labels.
2. **The HTML is post-discovery.** Its Object-Type Law and register chooser occur before any embedded Q0–Q14 run. That is acceptable only if Call 1 has already run and its immutable output is supplied separately.
3. **Address placement is partly provisional.** Atom family/UUID are preservation identity; Layer/Component may require review after classification.
4. **Status and Claim Class are shown beside the five independent axes but are not themselves two of those five axes.** The UI language should say “independent classification dimensions,” not imply that all seven are the named five.
5. **Math display fields lack a fully normalized canonical SQL home.** Until one is added, store them as governed `atom_items` or versioned extension JSON, not only inside HTML/localStorage.
6. **Narrative fields are correctly non-warrant-bearing.** Keep them outside canonical warrant calculations.
7. **Human-review fields prepare a candidate ruling; admission remains a separate signed event.**

## Final answer

Yes: each meaningful question can have one declared epistemic moment and one canonical answer home. But the correct architecture is not “the HTML asks everything in order.” It is:

- the neutral API asks the pre-category questions;
- Q14 opens the classification gate;
- the HTML builder asks the post-category, burden-native questions;
- JSON/SQLite stores the governed answer;
- HTML and Markdown display it;
- David rules separately;
- admission is a distinct signed event.

