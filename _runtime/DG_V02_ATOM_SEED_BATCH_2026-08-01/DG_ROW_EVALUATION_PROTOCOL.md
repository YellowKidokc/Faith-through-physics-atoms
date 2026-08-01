# DG v0.2 Row Evaluation Protocol

Date: 2026-08-01

Purpose:

Use DG v0.2 as a repeatable row/API test for claims before they become pills.

This is the working filter:

```text
Every claim must pass through dependency, new capability, preservation, collapse, translation, dynamics, admissibility, and closure before its status can rise.
```

## The Row Questions

| Gate | Question | Pass Meaning | Failure Meaning |
|---|---|---|---|
| DG1 Dependency | What must already exist for this claim to make sense? | Dependencies are named | The claim floats |
| DG2 Minimal Capability | What new capability appears? | The claim adds an irreducible operation or distinction | The claim is only a restatement |
| DG3 Preservation | What lower structure is preserved? | The claim keeps the floor it stands on | The claim destroys what it needs |
| DG4 Collapse | What fails if this claim is removed? | Necessity is visible | The claim may be decorative |
| DG5 Translation | How does it move across registers? | Structure survives translation | It is analogy or wordplay |
| DG6 Dynamics | Is it coherent, defective, or ruptured? | State is classified | Status is vague |
| DG7 Admissibility | Does it pass dependency + novelty + preservation? | It can become a candidate atom | It stays in inbox/review |
| DG8 Closure | Does it deny what it uses? | No self-defeat detected | It is inadmissible or needs repair |

## Row Output Fields

Use these columns for API rows, spreadsheet rows, or Kimi handoff rows.

```csv
row_id,source_file,claim_text,dg1_dependencies,dg2_new_capability,dg3_preserved_floor,dg4_collapse_if_removed,dg5_translation_registers,dg6_state,dg7_admissible,dg8_closure_pass,proof_label,grade,recommended_atom_action,notes
```

## Recommended Values

### dg6_state

- coherent
- defective
- ruptured
- unknown

### dg7_admissible

- yes
- no
- partial
- needs_review

### dg8_closure_pass

- yes
- no
- unclear

### proof_label

Use Lane 4 labels:

- LEAN_FORMAL_PROOF
- LEAN_CONDITIONAL_PROOF
- LEAN_GUARDRAIL_SUPPORTED
- PYTHON_RUNTIME_SUPPORTED
- COLAB_REPRODUCIBLE
- SYMBOLIC_SUPPORTED
- HISTORICALLY_SUPPORTED
- ABDUCTIVELY_FAVORED
- BRIDGE_DECLARED
- ISOMORPHIC_EVENT_CANDIDATE
- COUNTERMODEL_FOUND
- NOT_ESTABLISHED
- RERUN_OWED
- QUARANTINE
- NARRATIVE_ANCHOR

### grade

- A - established inside its register
- B - strong model or argument
- C - valid bridge / correspondence
- D - speculative but useful
- E - weak / underdeveloped
- F - rejected / retired

### recommended_atom_action

- create_claim_atom
- create_bridge_atom
- create_objection_atom
- attach_evidence
- attach_lean_receipt
- demote
- quarantine
- keep_in_inbox
- merge_with_existing

## The DG2 Test

DG2 is the row-killer.

Ask:

> What can this claim now do that the prior layer could not do?

If the answer is only:

- say it with prettier words
- repeat the same claim
- add a theological name without adding structure
- add a physics term without adding mechanism
- turn an analogy into a conclusion

then the row fails DG2.

It can stay as a note, story line, or rhetorical phrase. It should not become a load-bearing atom.

## Pill Rule

No pill should be generated as if it were strong until the row says:

- dependencies named
- new capability named
- preserved floor named
- collapse condition named
- translation grade named
- state named
- closure checked
- proof label assigned

The pill can still be made early, but it should visually carry the right status:

- candidate
- bridge
- open
- under review
- Lean target
- verified
- demoted

## Plain Speech

DG asks every claim:

```text
What do you need?
What do you add?
What do you preserve?
What breaks without you?
Where can you translate?
Are you healthy, damaged, or failed?
Are you admissible?
Do you contradict yourself?
```

That is the whole filter.

