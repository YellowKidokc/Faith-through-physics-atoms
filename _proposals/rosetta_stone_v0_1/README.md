# Rosetta Stone Connector v0.1

This proposal rail compares completed **blind semantic nodes** with a declared
axiomatic chain, proof stack, and derivative-family inventory. It comes after
semantic extraction, not before it.

## What it does

The proposal now has two connector modes:

1. `chain_to_node_audit.py` - local deterministic connector. No API key. Reads a folder of node JSON files and writes connected/floating/gap reports. It evaluates chain, proof-stack, and derivative-family matches independently so one strong proof match does not hide a chain match.
2. `run_rosetta_connector.py` - model-backed receipt rail. Writes prompts and API receipts for chain/proof/family comparisons.
3. `compare_connector_runs.py` - compares the two mapping outputs, marking agreement and disagreement without turning either into a verdict.

For every node, the model-backed rail runs three independent, receipt-backed comparisons:

1. `chain`: nearest declared chain step or `floating`.
2. `proof_stack`: declared formal-record role or `floating`.
3. `derivative_families`: declared family relation or `floating`.

It writes the exact prompt, response, node source receipt, source hash, schema
hash, timestamp, model, and an aggregate coverage report.

## What it does not do

- It does not edit source nodes.
- It does not decide whether any statement is true, proven, admitted, or canon.
- It does not write to `CLAIM_REGISTRY.sqlite`.
- A map match is not evidence that a chain step is valid.

`floating` and `contradicts` are intended results, not errors. They make missing
steps, tensions, and chain limits visible.

The deterministic connector is a broad, explainable candidate generator. Its
lexical links are **not** semantic confirmation. The model-backed connector is
also a comparison result, not proof. The comparator makes agreement and
disagreement reviewable.

## Smoke test

Deterministic full blind-node connection map:

```powershell
python .\chain_to_node_audit.py `
  --schema .\chain_schema.json `
  --nodes "\\192.168.2.50\h_hp\Desktop\AXIOM\FULL_CORPUS_BLIND_RUN_20260814\SEMANTIC_NODES" `
  --output-dir .\runs\deterministic_audit
```

This writes:

- `connection_map.json`
- `connection_map.csv`
- `connected_nodes.json`
- `floating_nodes.json`
- `gap_analysis.json`
- `RUN_MANIFEST.json`
- `RUN_REPORT.md`
- a run-local snapshot of `chain_to_node_audit.py`

Model-backed one-node smoke test:

```powershell
python .\run_rosetta_connector.py `
  "\\192.168.2.50\h_hp\Desktop\AXIOM\FULL_CORPUS_BLIND_RUN_20260814\SEMANTIC_NODES\receipts" `
  --output-dir .\runs\api_smoke_test `
  --limit 1
```

Use `--dry-run` to verify all input parsing, prompt production, and output
layout without calling the model. Do not run the entire 1,011-node corpus until
the smoke-test receipts and mapping behavior have been reviewed.

Compare completed runs:

```powershell
python .\compare_connector_runs.py `
  --deterministic-map .\runs\deterministic_audit\connection_map.json `
  --api-receipts .\runs\api_smoke_test\receipts `
  --output-dir .\runs\comparison
```
