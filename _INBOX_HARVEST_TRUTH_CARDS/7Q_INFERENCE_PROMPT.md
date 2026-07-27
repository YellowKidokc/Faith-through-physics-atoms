# 7Q ADVERSARIAL INFERENCE PROMPT
# Paste this into any LLM. Append your claim at the bottom.
# Returns: surviving insight, failure points, knowledge graph, scientific extraction.
# Does NOT return the worksheet — only the knowledge gained.

---

Analyze the following claim aggressively but fairly.

Do the full reasoning internally using a seven-part adversarial framework:
1. Identity — what is this claim, what type, what tier
2. Domain — where does it live, what scale, cross-domain presence
3. Assertion — state it precisely, generate its negation
4. Support — evidence type, tier, replication, competing explanations
5. Dependencies — what must be true upstream, where does the chain end
6. Consequences — what it forces downstream, predictions, cross-domain implications
7. Kill conditions — five death types (self-refutation, infinite regress, empirical contradiction, logical incoherence, explanatory failure)

Do NOT return the full process.
Return only the inference layer: what was learned, what survives, what fails, and what this adds to a structured knowledge graph.

Output format:

# Core Claim
State the strongest precise version of the claim after analysis.

# Best Surviving Version
What remains if the claim is made maximally coherent and all weak framing is removed?

# Type / Domain
Classify briefly. Note cross-domain presence.

# Upstream Dependencies
What must be true for this to stand? Trace the chain. Where does it terminate — axiom, brute fact, or circularity?

# Downstream Consequences
If true, what else MUST follow? Include untested predictions.

# Primary Failure Points
The strongest reasons this could fail. Name the death type for each.

# What Survives
After maximum pressure, what is still standing?

# What Dies
What parts of the claim do not survive adversarial testing? Be specific.

# Robustness Estimate
Qualitative assessment: weak | fragile | partially grounded | strong but contested | highly constrained
Explain in 3-5 sentences. Separate lack of evidence from disproof. Separate conceptual coherence from empirical support.

# Scientific Extraction
- Hypothesis: (one sentence, testable)
- Predictions: (numbered, each falsifiable)
- Falsification path: (what experiment or observation would kill it)

# Knowledge Graph YAML
Return graph-ready nodes and edges:

```yaml
nodes:
  - id: "claim_001"
    type: Claim | Dependency | Prediction | FailurePoint | Evidence | Concept
    label: ""
    description: ""

edges:
  - source: ""
    target: ""
    relation: depends_on | implies | contradicts | supported_by | weakened_by | tested_by | predicts | fails_under | maps_to | equivalent_to
    confidence: 0.0-1.0
```

# Executive Summary
Shortest possible high-value summary of what was learned. No filler. No hedge language. What moved?

Rules:
- Prefer the strongest surviving interpretation over the weakest wording.
- Separate "unsupported" from "false."
- Separate "coherent" from "true."
- Separate "testable" from "validated."
- If the claim is unconventional, do not dismiss it for being unconventional. Test it structurally.
- If part survives and part dies, separate them cleanly.
- Be precise, restrained, and direct.

---

Claim to analyze:

[PASTE YOUR CLAIM HERE]
