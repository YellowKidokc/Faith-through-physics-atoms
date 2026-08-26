# AXIOM → ROSETTA ADAPTER STANDARD v0.1

Status: **candidate proposal**  
Scope: `axioms/01_canonical/*.jsonld` → Rosetta Stone connector input  
Boundary: adapter/routing only. This standard does **not** edit source atoms, prove claims, admit candidates, canonize results, or change Rosetta Stone v0.1.

## 1. Fixed Center

The fixed center is the existing Rosetta Stone connector:

- `ROSETTA_STONE_CONNECTOR_SPEC.md`
- `chain_schema.json`
- `chain_to_node_audit.py`
- `run_rosetta_connector.py`
- `compare_connector_runs.py`

This proposal adds a standardized way to turn the existing axiom atom records into the node envelopes those rails already know how to route.

It deliberately does **not** replace the axiom JSON-LD records. The source atom remains the source of truth. The adapter emits a reviewable projection.

## 2. The Rule

> Do not rewrite axioms to fit Rosetta. Project each axiom into Rosetta's input shape, preserve its native identity, and let the connector route it.

Each source atom produces one standardized envelope:

```text
axioms/01_canonical/AX-025-coherence-cannot-self-increase.jsonld
  -> AX-025.rosetta.json
  -> deterministic connector nodes/
  -> model-backed connector receipts/*.nodes.json
```

The envelope is simultaneously:

1. a **claim atom projection** — preserves claim, evidence, proof-link, verdict separation;
2. a **Rosetta input node** — carries `node_id`, `coherent_statement`, `plain_statement`, `formal_expressions`, and `scope_text`;
3. an **API-call payload** — can be embedded in markdown/HTML or sent directly to the model-backed rail;
4. a **receipt-bearing candidate** — carries source hash, source path, governance flags, and adapter provenance.

## 3. Non-Negotiables

1. **Source atoms are read-only.** The adapter never edits `axioms/01_canonical/*.jsonld`.
2. **No single-label flattening.** A claim gets separate axes for claim type, derivation role, claim species, proof label, truth status, and bridge status.
3. **Candidate-only output.** Every generated envelope has `candidate_or_admitted: "Candidate"`.
4. **No evidence/falsification propagation by default.** Both propagation flags are `false`.
5. **Sparse storage.** Optional bridge, mirror, and compression fields appear only when there is real signal or an explicit not-run/candidate state worth recording.
6. **Routing is not proof.** A chain/proof/family match is a comparison result only.
7. **Exact-ID hints are not semantic matches.** The adapter may note that `BC2` exists in the proof stack, but the connector still decides routing.

## 4. Standard Envelope

Schema file: `axiom_rosetta_node.schema.json`

Minimum public shape:

```json
{
  "schema_version": "rosetta-axiom-node/v0.1",
  "node_id": "AX-025",
  "atom_id": "tp:axioms/01/AX-025",
  "claim_id": "tp:AXIOMS/T3.1",
  "canonical_uri": "https://faiththruphysics.com/claims/axioms/01/AX-025",
  "title": "Coherence Cannot Self-Increase",
  "claim": "Macro-coherence ... cannot self-increase.",
  "coherent_statement": "Macro-coherence ... cannot self-increase.",
  "plain_statement": "Macro-coherence ... cannot self-increase.",
  "formal_expressions": ["dC_macro/dt ≤ 0 (closed system, no external input)"],
  "scope_text": "Q3 | Q3-K (Coherence theorem — 2nd Law analog) | M03 | Coherence Engine",
  "dependencies": ["tp:axioms/01/AX-023", "tp:axioms/01/AX-024"],
  "kill_conditions": ["Show a closed system spontaneously increasing coherence."],
  "truth_unit": {
    "claim": "Macro-coherence ... cannot self-increase.",
    "question": "Type 1 (Does X hold?)",
    "evidence": [],
    "proof_link": null,
    "verdict": "not_evaluated_registry_import"
  },
  "classification": {
    "native_claim_class": "theorem",
    "native_new_type": "Theorem",
    "unified_claim_type": "THEOREM",
    "unified_claim_type_status": "adapter_candidate",
    "derivation_role": "derived_result",
    "claim_species": ["logical", "mathematical"],
    "domain": "Ontological",
    "stage": "01_canonical",
    "proof_label": "NOT_ESTABLISHED",
    "truth_status": {
      "ontic": "unknown",
      "epistemic": "insufficient"
    }
  },
  "rosetta_targets": {
    "exact_id_hints": {
      "proof_step_ids": ["T3.1"],
      "chain_steps": [],
      "keeper_deck_ids": ["T3.1"]
    },
    "routing_status": "unrouted",
    "chain_step": null,
    "proof_step_id": null,
    "family_symbol": null
  },
  "mirror_search": {
    "required": true,
    "status": "not_run",
    "question": "What human-independent process has the same relational structure?"
  },
  "source": {
    "path": "axioms/01_canonical/AX-025-coherence-cannot-self-increase.jsonld",
    "sha256": "...",
    "stage": "01_canonical",
    "source_reference": "...",
    "workbook": {}
  },
  "governance": {
    "candidate_or_admitted": "Candidate",
    "kernelChecked": false,
    "propagates_evidence": false,
    "propagates_falsification": false,
    "boundary": "Adapter projection and Rosetta routing only."
  },
  "native": {
    "claimClass": "theorem",
    "axiomRegistry": {},
    "edges": []
  },
  "series_carry_forward": {
    "claim_fingerprint": "sha256:...",
    "fingerprint_basis": "node_id + title + normalized claim + question + domain + species + dependencies + kill_conditions"
  }
}
```

The actual schema allows the `native` record to preserve source fields without forcing those fields into the connector prompt.

## 5. Field Mapping

| Standard field | Source field | Rule |
|---|---|---|
| `node_id` | `axiomRegistry.axiomID` | fallback: filename stem |
| `atom_id` | `nodeID` | preserve exact repo ID |
| `claim_id` | `claimID` | preserve exact public claim ID |
| `canonical_uri` | `@id` | preserve URL |
| `title` | `name` | no rewrite |
| `claim` | `statementTechnical` | fallback: `statementPlain` |
| `coherent_statement` | `statementTechnical` | Rosetta compatibility |
| `plain_statement` | `statementPlain` | Rosetta compatibility |
| `formal_expressions` | `mathematicalForm` | array; omit when absent |
| `scope_text` | `treeLevel`, `treeBranch`, `moduleID`, `moduleTitle` | deterministic join with ` \| ` |
| `dependencies` | `edges[type=dependsOn].target` | sorted unique list |
| `kill_conditions` | `falsificationCondition` | array; no paraphrase |
| `question` | `axiomRegistry.questionType` | may be `null` |
| `domain` | `axiomRegistry.domain` → `domainType` | preserve native domain |
| `proof_label` | `verificationStatus`, `kernelChecked` | current corpus maps to `NOT_ESTABLISHED` |
| `source.sha256` | file bytes | adapter-computed |
| `claim_fingerprint` | normalized claim identity material | adapter-computed |

## 6. Multi-Axis Classification

The old atom vocabulary and the newer unified classification schema answer different questions. Keep both.

### 6.1 Native axes — preserved, not reinterpreted

- `native_claim_class` ← `claimClass`
- `native_new_type` ← `axiomRegistry.newType`
- `kernelRole` and `spineRole` remain inside `native.axiomRegistry`

### 6.2 Unified claim type — adapter candidate

`unified_claim_type` uses the 15-type classification vocabulary:

`AXIOM`, `DEFINITION`, `BOUNDARY`, `LEMMA`, `THEOREM`, `COROLLARY`, `MODEL`, `HYPOTHESIS`, `PREDICTION`, `PROTOCOL`, `EVIDENCE`, `BRIDGE`, `IDENTIFICATION`, `OPEN`, `CLOSURE`

For this adapter, the result is always marked:

```json
"unified_claim_type_status": "adapter_candidate"
```

That prevents a mechanical mapping from becoming a canon ruling.

### 6.3 Primitive handling

Existing `Primitive` / `floor_axiom` records are **not** silently called `AXIOM`.

They map to:

```json
{
  "unified_claim_type": "HYPOTHESIS",
  "derivation_role": "candidate_primitive",
  "claim_species": ["metaphysical_ontological"]
}
```

Reason: under the newer one-axiom discipline, only the God/ground claim receives `AXIOM`. Existing primitives remain native registry primitives, while the standardized layer treats their primitive status as testable through kernel-compression bridges.

This does not demote the source record. It marks the adapter projection honestly.

## 7. Truth Unit Rule

Every envelope carries the minimum truth-bearing object:

```json
{
  "truth_unit": {
    "claim": "what is asserted",
    "question": "what question this answers",
    "evidence": [],
    "proof_link": null,
    "verdict": "not_evaluated_registry_import"
  }
}
```

The current axiom JSON-LD corpus does not carry separate evidence objects or proof-link records. Therefore the adapter must not invent them. It records the empty evidence array and null proof link.

The presence of a falsification condition is stored under `kill_conditions`; it is not treated as evidence.

## 8. Mirror Search Rule

Every envelope starts mirror search as required but not run:

```json
"mirror_search": {
  "required": true,
  "status": "not_run",
  "question": "What human-independent process has the same relational structure?"
}
```

Later rails may add candidate domains, mappings, differences, stop reasons, and bridge grades. The adapter does not force a mirror.

## 9. Bridge Rule

Only native bridge records receive `bridge_evaluation` at adaptation time:

```json
"bridge_evaluation": {
  "bridge_type": "cross_domain",
  "status": "declared_not_tested",
  "bridge_grade": "B0",
  "failure_condition": "..."
}
```

`B0` means declared/shared-vocabulary level only. It does not mean the bridge is false; it means no preservation tests have been run in this adapter pass.

## 10. Kernel-Compression Rule

Candidate primitives receive a `compression_bridge` stub:

```json
"compression_bridge": {
  "bridge_type": "kernel_compression",
  "source_node": "AX-167",
  "source_claim": "Information Primitive",
  "target_kernel": ["tp:axioms/01/AX-001", "tp:axioms/01/AX-002"],
  "proposed_derivation": null,
  "compression_grade": "K0",
  "status": "candidate",
  "demotion_if_successful": "primitive -> derived",
  "failure_condition": "..."
}
```

This makes the primitive question explicit:

> Can this node be generated from earlier nodes without assuming itself?

If a later formal bridge reaches `K4` or `K5`, that is a separate review event. The adapter does not demote anything.

## 11. Exact-ID Rosetta Hints

The adapter may populate exact-ID hints from `chain_schema.json`:

- `proof_step_ids` when `axiomRegistry.oldID` exactly equals a proof-stack ID
- `chain_steps` when the old ID appears in a chain layer label
- `keeper_deck_ids` when the old ID exactly equals a keeper-deck ID

These are routing hints only. They are not semantic matches, and the connector still performs chain/proof/family comparison independently.

## 12. Output Layout

```text
_proposals/rosetta_stone_v0_1/
  axiom_to_rosetta_node.py
  axiom_rosetta_node.schema.json
  AXIOM_ROSETTA_ADAPTER_STANDARD.md

runs/axiom_adapter/
  nodes/
    AX-001.rosetta.json
    AX-002.rosetta.json
    ...
  receipts/
    axioms_01_canonical.nodes.json
  ADAPTER_REPORT.json
```

Use `nodes/` for the deterministic connector. Use `receipts/axioms_01_canonical.nodes.json` for the model-backed connector.

## 13. Commands

From `_proposals/rosetta_stone_v0_1/`:

```powershell
python .\axiom_to_rosetta_node.py `
  --atoms-dir ..\..\axioms\01_canonical `
  --output-dir .\runs\axiom_adapter
```

Deterministic connector:

```powershell
python .\chain_to_node_audit.py `
  --schema .\chain_schema.json `
  --nodes .\runs\axiom_adapter\nodes `
  --output-dir .\runs\axiom_deterministic
```

Model-backed connector, dry run first:

```powershell
python .\run_rosetta_connector.py `
  .\runs\axiom_adapter\receipts `
  --output-dir .\runs\axiom_api_smoke `
  --limit 1 `
  --dry-run
```

Then compare the deterministic and model-backed runs with the existing comparator.

## 14. Acceptance Tests

A clean adapter run must show:

1. every `AX-*.jsonld` source file produces exactly one envelope;
2. no duplicate `node_id` values;
3. no source file is modified;
4. every envelope validates against `axiom_rosetta_node.schema.json`;
5. every envelope remains `Candidate`;
6. both propagation flags remain `false`;
7. `chain_to_node_audit.py` can read the emitted `nodes/` folder;
8. `run_rosetta_connector.py --dry-run` can read the emitted `receipts/*.nodes.json` batch;
9. the report includes source count, node count, class counts, exact-ID hint counts, and validation errors;
10. no Rosetta route is represented as proof, admission, canonization, or truth.

## 15. What Changes Later

This adapter standardizes the **axiom lane** only.

Later lanes can reuse the same envelope pattern for:

- master equation records
- Ten Laws records
- evidence records
- paper Telescope records
- bridge registry records
- worldview axioms

Each lane should get its own adapter, but not its own incompatible envelope.
