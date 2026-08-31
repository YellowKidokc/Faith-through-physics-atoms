# THE THREE-CALL CLAIM PIPELINE — IMPLEMENTATION v1.0

**Date:** 2026-08-25  
**Status:** IMPLEMENTED LOCALLY; deterministic vertical slice verified; live DeepSeek call awaits an attached private key  
**Authority boundary:** Review produces candidate receipts. It never performs canonical promotion.

## Governing sequence

```text
CAPSULE
  -> CALL 1: NON-DISCRIMINATORY DISCOVERY
  -> hard gate: DISCOVERY_COMPLETE
  -> CALL 2: CLASSIFICATION AND BURDEN ROUTING
  -> hard gate: CLASSIFICATION_COMPLETE
  -> CALL 3: RECONCILIATION, TRANSLATION, AND GRAPH FIT
  -> human review eligibility
  -> separate explicit human canonization action
```

The operating rule is:

> Call 1 discovers without naming. Call 2 names without promoting. Call 3 connects without laundering. A human rules admission.

## Call 1 — non-discriminatory discovery

Call 1 sees the raw capsule. It is prohibited from assigning a discipline, object class, proof class, evidence grade, IC grade, bridge grade, theological identification, or canonical standing. It exposes:

- referent;
- identities and distinctions;
- relations and operations;
- dependencies and constraints;
- invariants and collapse conditions;
- consequences and countermodels;
- open questions.

It must return `DISCOVERY_COMPLETE` before Call 2 can run.

## Call 2 — classification and burden routing

Call 2 sees the capsule and the hash-pinned Call 1 output. It assigns the four-object type, register, claim species, native anatomy, warrant class, lifecycle, WHY outcome, burdens, and unresolved items. It may not invent facts missing from discovery. When another fact is necessary, it returns `RETURN_TO_DISCOVERY` with a named exception.

It must return `CLASSIFICATION_COMPLETE` before Call 3 can run.

## Call 3 — reconciliation, translation, and fit

Call 3 sees the capsule and both hash-pinned upstream outputs. It recommends new claim, amendment, new version, supersession, added evidence, or hold-open. It keeps three rails visible:

```text
NATIVE STATEMENT -> BRIDGE STATEMENT -> IDENTIFICATION STATEMENT
```

It records preserved and lost structure, safe public wording, downstream effects, graph fit, and publication eligibility. Eligibility means eligible for human review, never automatically canonical.

## Implemented artifacts

- `_schema/claim_capsule_v1.schema.json`
- `_schema/claim_discovery_output_v1.schema.json`
- `_schema/claim_classification_output_v1.schema.json`
- `_schema/claim_reconciliation_output_v1.schema.json`
- `_schema/claim_pipeline_receipt_v1.schema.json`
- `_scripts/claim_pipeline_service.py`
- `_scripts/test_claim_pipeline_service.py`
- `_runtime/claim_capsule_app/index.html`
- `RUN_CLAIM_CAPSULE.ps1`

## Run

From the repository root:

```powershell
.\RUN_CLAIM_CAPSULE.ps1
```

The editor opens at `http://127.0.0.1:8787`. Select **Test machinery without DeepSeek** to verify the gates without an external call. With `DEEPSEEK_API_KEY` available to the process or stored in an ignored root `keys.txt`, `.env.local`, or `.env`, leave the test box unchecked to run the three live DeepSeek calls.

## Verified behavior

- JSON syntax verified for all five claim-pipeline schemas.
- Python modules compile.
- Three unit tests pass.
- The local HTTP health endpoint responds.
- A mock capsule runs discovery, classification, and reconciliation in order.
- A receipt is written under `_runtime/claim_capsule_app/runs/`.
- An incomplete discovery prevents classification.
- A canonical-promotion request is rejected.
- The receipt declares `canonical_promotion_performed: false`.

## Honest boundary

The deterministic orchestration and local browser flow are verified. A live DeepSeek response has not yet been verified in this implementation because no usable DeepSeek credential was discoverable in the current environment or the repository's established private-key locations. No key was printed or copied.
