# ROSETTA STONE - NODE-TO-CHAIN CONNECTOR

## What This Does
Takes individual truth-nodes (from blind extraction) and maps each one to its place in the axiomatic chain. No labels imposed — the node finds its home or gets flagged as floating.

## The Schema
`chain_schema.json` contains:
- **chain**: 20 steps (God creates → Christ is convergence point)
- **proof_stack**: 25 formal steps with kill conditions
- **derivative_families**: 9 declared variable families with modes and status
- **keeper_deck**: 18 strict keeper axioms with anchors

## The Pipeline

There are two valid implementations:

- `chain_to_node_audit.py`: deterministic local connector. It scores nodes against the declared schema with lexical/alias structural matching, then emits connected/floating/gap reports. This is the default infrastructure pass because it is reproducible and does not need an API key.
- `run_rosetta_connector.py`: model-backed connector. It asks a model to classify each node against the chain, proof stack, and derivative families, preserving prompts and receipts.

Both implementations are routing tools only. Neither proves, admits, canonizes, promotes, or edits any node.

### Input
A set of extracted nodes, each with:
```json
{"node_id": "N001", "text": "the claim text", "source": "which paper"}
```

### Stage 1: Chain Matching
For each node, API call with embedded schema:
```
System: You are a structural classifier. Given a truth-node and a 20-step axiomatic chain, determine which chain step (if any) this node supports, contradicts, or extends. If it doesn't map to any step, say FLOATING.

Schema: [chain from chain_schema.json]

Node: [node text]

Respond JSON only:
{
  "node_id": "...",
  "chain_step": 1-20 or null,
  "relationship": "supports | contradicts | extends | floating",
  "confidence": 0.0-1.0,
  "reason": "one sentence"
}
```

### Stage 2: Proof Stack Matching
Same node, now against the 25-step formal proof stack:
```
{
  "node_id": "...",
  "proof_step_id": "P1" | "A2.1" | "CROSS" | null,
  "role": "direct_support | premise | evidence | counterargument | background | floating",
  "confidence": 0.0-1.0
}
```

### Stage 3: Family Matching
Same node, against the 9 declared derivative families:
```
{
  "node_id": "...",
  "family_symbol": "G" | "L" | "J" | ... | null,
  "mode": "which specific mode if applicable" | null,
  "relationship": "supports | extends | contradicts | floating"
}
```

### Stage 4: Assembly
After all nodes are classified:

**Connected nodes**: have at least one chain_step OR proof_step OR family match
**Floating nodes**: matched nothing — either the chain is incomplete or the node doesn't belong

Output:
```json
{
  "total_nodes": 1011,
  "connected": 847,
  "floating": 164,
  "chain_coverage": {
    "step_1": ["N001", "N045", "N789"],
    "step_2": ["N012", "N034"],
    ...
    "step_20": ["N999"]
  },
  "floating_nodes": [
    {"node_id": "N055", "text": "...", "nearest_step": 7, "distance": "low"}
  ]
}
```

### Stage 5: Gap Analysis
- Which chain steps have NO supporting nodes? → gap in evidence
- Which chain steps have MANY supporting nodes? → well-supported
- Which floating nodes cluster together? → possible missing chain step
- Which floating nodes contradict a chain step? → possible chain weakness

## API Configuration
- Model: deepseek-chat or claude-sonnet (whichever is on the rail)
- Temperature: 0
- JSON mode enforced
- Each node classified independently (no bleed)
- Schema embedded in every call (it's small enough)

## Output Location
`D:\GitHub\Faith-through-physics-atoms\_proposals\rosetta_stone_v0_1\`

## The Key Insight
The nodes do not get told what to be. They are compared against an explicitly
declared reference and may map, contradict, qualify, or float. The result is a
reviewable routing record, not a proof that the reference chain is correct.
