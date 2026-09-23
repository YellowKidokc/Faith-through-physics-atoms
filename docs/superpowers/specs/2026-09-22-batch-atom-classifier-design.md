# Batch Atom Classifier — Design Spec

**Date:** 2026-09-22  
**Project:** Faith-through-physics-atoms  
**Topic:** A batch-runnable Python pipeline that classifies atoms one at a time and produces canonization-ready receipts.

---

## 1. Purpose

Provide a repeatable, resumable, one-atom-at-a-time classification loop that:

1. Scans a corpus tree for atoms (`.jsonld`) or pills (`.pill.yaml`).
2. Classifies each item using an LLM against the existing `claim-classification/1.0.0` schema.
3. Writes a versioned classification receipt next to (or under) the source.
4. Optionally feeds the receipt to the mothership canon engine for deterministic pre-review.
5. Can be launched from Windows via a `RUN_CLASSIFY.bat` double-click wrapper.

The pipeline is intentionally conservative: it **proposes**, never **admits**. Every output lands as `candidate`/`proposed` and awaits human ruling before promotion.

---

## 2. Scope

**In scope for first deliverable:**
- Python classifier script: `mothership/tools/classify_atoms.py`
- Windows batch launcher: `mothership/RUN_CLASSIFY.bat`
- JSON receipt output conforming to `claim_classification_output_v1.schema.json`
- Resumable run via a local progress file
- Optional `--canon` flag that runs the mothership `CanonEngine` over the classified atom
- Tests for schema validation, prompt assembly, and resumability

**Out of scope for first deliverable:**
- Automatic GitHub PR creation
- Multi-worker parallelism (kept serial so each atom can be inspected and costs are predictable)
- Full curator integration (the curator can later consume these receipts)

**Starting corpus:** `axioms/01_canonical/` and `mothership/pills/`, because they are already minted/addressed and small enough to iterate on safely.

---

## 3. Inputs and Outputs

### Input
- Source atom tree (default: `mothership/pills`)
- Each source is either a `.jsonld` atom or a `.pill.yaml` pill.
- For `.jsonld`, the classifier reads the full object.
- For `.pill.yaml`, the classifier reads `face` + selected `veins` (term, plain statement, target_type, source).

### Output
- One classification receipt per atom:
  - Path: `<output-dir>/<relative-path>/<stem>.classification.json`
  - Schema: `claim-classification/1.0.0`
  - Required fields mirror `_schema/claim_classification_output_v1.schema.json`
- A run manifest:
  - Path: `<output-dir>/RUN-<timestamp>-manifest.json`
  - Contains: run id, source tree, provider/model, counts, errors, skipped files
- A progress file (only when `--resume` is used):
  - Path: `<output-dir>/progress.json`
  - Contains: set of completed source paths, last run id

---

## 4. Components

### 4.1 `classify_atoms.py`
Main entry point. Responsibilities:
- Parse CLI args (`--input-dir`, `--output-dir`, `--provider`, `--model`, `--resume`, `--canon`, `--limit`).
- Discover source atoms.
- Load progress and skip already-completed items.
- For each atom:
  1. Build classification prompt.
  2. Call `llm_client.complete()` with `json_mode=True`.
  3. Parse and validate JSON against the classification schema.
  4. If `--canon`, run `CanonEngine.evaluate()` and attach a `canon_receipt`.
  5. Write receipt.
  6. Update progress.
- Write manifest at end.

### 4.2 Prompt builder
A dedicated function `build_classification_prompt(atom_text: str, face: dict) -> str` that:
- Injects the schema as the required JSON structure.
- Provides one worked example (from `_runtime/claim_capsule_app/runs/20260831T002220Z-3217ae84.json`).
- Includes the atom text verbatim with instructions to classify only what is present.
- Forbids invented evidence or unsupported canonical status.

### 4.3 Schema validator
Uses `jsonschema` if available; otherwise performs a manual required-fields check so the script has no hard dependency beyond `pyyaml` and the stdlib. The receipt is still written even if validation warns, so the human can inspect malformed outputs.

### 4.4 `RUN_CLASSIFY.bat`
A Windows batch wrapper that:
- Sets `DEEPSEEK_API_KEY` from a local `.env` file if present (`.env` is gitignored).
- Activates the project virtual environment if one exists.
- Runs `python tools/classify_atoms.py --input-dir pills --output-dir _runtime/classifications --provider deepseek --resume`.
- Pauses at the end so the user sees the summary.

### 4.5 Canon bridge
When `--canon` is passed, the script converts the classified atom into the `Identity`/`Occurrence` shape expected by `CanonEngine` and appends the deterministic rule receipt under the key `canon_receipt` in the classification output.

---

## 5. Data Flow

```text
atom tree
   |
   v
classify_atoms.py  ----prompt---->  LLM (DeepSeek / Kimi)
   |                                   |
   |<-------------JSON-----------------+
   |
   v
schema validate  ----(if --canon)-->  CanonEngine
   |                                   |
   v                                   v
classification receipt         canon_receipt
   |
   v
output dir + progress.json + manifest.json
```

---

## 6. Path to Canonization

1. **Discovery / intake** — atom is minted with UUID and address.
2. **Classification** (this pipeline) — atom is typed as `CLAIM`, `EVIDENCE`, `PROOF`, or `PROCESS`; species, register, anatomy, burdens, and WHY-outcome are produced.
3. **Canon pre-review** — `CanonEngine` checks required fields, anchor hash, source citations, and non-empty anchors. Output is `PASS` or `FAIL` with per-rule detail.
4. **Curator proposal** — the weekly curator pass can read the classification receipts and propose edges, definitions, or divergences.
5. **Human ruling** — a PR flips `candidate` → `proposed` → `canonized` (or `retired`). The model never performs this flip.

---

## 7. Combining the Proofs and Claims Layers

The classification schema's `object_type` field tells the system whether an atom is:
- `CLAIM` — a load-bearing assertion.
- `EVIDENCE` — a citation, observation, or source.
- `PROOF` — a deductive or formal support object.
- `PROCESS` — a methodology, rule, or workflow atom.

A complete argument chain is built as **edges** between these objects, not by merging them into one record:
- A `CLAIM` carries `edges` pointing to its supporting `EVIDENCE` and `PROOF` objects.
- Classification assigns the correct `object_type` to each atom so the edge drawer knows which end of a link it is holding.
- The canon engine verifies that every `CLAIM` with `object_type: CLAIM` has at least one cited source (`source_cited` rule) and that its anchors verify.
- The classifier never invents edges; it only labels atoms. Edge proposals are left to the curator pass, which can compare classifications across papers.

---

## 8. Error Handling and Resumability

- **Transient LLM errors** (timeout, rate limit): log error, stop the loop, and write progress so the run can resume.
- **Schema validation failures**: write the receipt with `status: CLASSIFICATION_INCOMPLETE` and include the raw LLM output plus validation errors.
- **Missing API key**: exit immediately with a clear message pointing to `RUN_CLASSIFY.bat` setup.
- **Duplicate source**: if progress file shows the source was already processed, skip by default when `--resume` is set; overwrite only if `--force` is passed.

---

## 9. Testing

- Unit test `build_classification_prompt` ensures required schema fields appear in the prompt.
- Unit test schema validation against a known-good classification receipt.
- Unit test resumability: progress file is read, completed items skipped, failed/incomplete items retried.
- Integration test with `llm_client.complete` mocked to return the known-good receipt; verify output file is written and matches schema.

---

## 10. Files Created

- `mothership/tools/classify_atoms.py`
- `mothership/RUN_CLASSIFY.bat`
- `mothership/tests/test_classify_atoms.py`
- `mothership/specs/BATCH_ATOM_CLASSIFIER_v1.0.md` (user-facing spec)
- This design doc: `docs/superpowers/specs/2026-09-22-batch-atom-classifier-design.md`
