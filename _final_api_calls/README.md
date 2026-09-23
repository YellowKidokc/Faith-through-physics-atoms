# FINAL API CALLS AND CANONIZATION STACK

This folder is the ordered reconstruction package for the claim-to-candidate
system. It contains one epistemic pipeline and a perpendicular runtime system.
Folder order is a reading order, not a claim that every numbered document is an
API stage.

> **CANDIDATE SYSTEM — NO AUTOMATIC ADMISSION.** Discovery, classification,
> translation, storage, and review may propose records. Only a separate human
> ruling may admit one.

## Axis A — epistemic processing

```text
SOURCE
  -> 01 label-blind structural discovery
  -> 02 question and burden resolution
  -> 03 native object expansion
  -> controlled classification and testing
  -> 06 translation / isomorphism, only after native warrant
  -> human candidate ruling
  -> separate admission event
```

Classification is forbidden during the protected discovery portion of `01`.
The model-created groupings in `01` are descriptive emergent organizations, not
controlled domain, register, proof, truth, or canon classifications. In `02`,
Q14 is the final forward question and is the earliest point at which controlled
role classification may be proposed. `03` assigns the native object layer only
after the burden is known. `06` runs only after both native objects have been
opened and classified under their own burdens.

## Axis B — execution, storage, and review

```text
CAPTURE -> EXECUTE -> STORE -> VALIDATE -> REVIEW -> PRESENT -> HUMAN RULE
```

`07–12` implement or specify this runtime axis. SQL, Ollama, build briefs, and
icons are not epistemic stages and must never be inserted into Axis A as though
they establish truth.

## Ordered document roles

| # | Role | Document |
|---|---|---|
| 00 | EXECUTION | Three-call operational wrapper |
| 01 | PIPELINE | Nondiscriminatory discovery; executable embedded call |
| 01A | PIPELINE | Label-blind guiding-question extraction; executable, answers and classifications prohibited |
| 02 | PIPELINE | Question-to-burden and answer-resolution router |
| 03 | SCHEMA / PIPELINE | Current v1.1 four-object expansion canon |
| 04 | GOVERNING | Unified end-to-end methodology |
| 05 | GOVERNING | Master orchestrator and overlap resolver |
| 06 | PIPELINE | Translation and isomorphism firewall |
| 07 | IMPLEMENTATION | Canonical Content OS architecture |
| 08/08A | SCHEMA | SQLite contract and executable schema |
| 09 | UI/RUNTIME | AI review and canon-session layer |
| 10 | IMPLEMENTATION | Kimi build handoff |
| 11 | IMPLEMENTATION | Codex/Claude vertical-slice build prompt |
| 12 | UI/RUNTIME | Proposed node icon semantics |

The former `03` v0.1 file is preserved in `_superseded_source_versions/`; it
was not deleted. The v1.1 four-object edition is the active reference in this
stack.

## What is executable today

- `01_NONDISCRIMINATORY_DISCOVERY.md` contains the executable
  `final_api_python` block and produces a source-bound JSON receipt plus an
  optional plain-English projection.
- `01A_LABEL_BLIND_QUESTION_EXTRACTOR.md` contains an executable listening pass
  that emits only ordered, source-bound guiding questions. It generates no
  answers or classifications.
- `00` describes the existing three-call service and its schemas under
  `_scripts/` and `_schema/`.
- `02–06` are currently governing specifications, not yet five independently
  executable embedded API calls.
- `07–12` are implementation/runtime contracts, not truth-producing calls.

Therefore a successful `01` receipt proves that discovery ran. It does not by
itself prove that burden routing, object expansion, controlled classification,
translation, HTML population, human review, or admission occurred.

## Run the implemented discovery call

```powershell
python .\_final_api_calls\run_embedded_markdown.py `
  .\_final_api_calls\01_NONDISCRIMINATORY_DISCOVERY.md `
  --source "C:\path\to\paper.md" `
  --provider mock
```

Use `--provider deepseek` only when the credential is already configured. The
launcher and receipts never print it.

See `13_END_TO_END_STACK_AUDIT_2026-09-01.md` for the current consistency and
implementation audit.
