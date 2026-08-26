# Theophysics Research Runtime

Universal API contract for every claim, paper, model, story, and instrument.

## Rule

The public artifact stays readable.

The runtime keeps the underlying structure live: claims, dependencies, hidden
assumptions, type boundaries, kill conditions, survival vector, misuse risks,
and failure propagation.

## Implemented Local Calls

```text
Claim.register()
Claim.status()
Claim.dependencies()
Claim.kill_condition()
Claim.render(formal | bridge | public)
HIDDEN_SOURCE()
HIDDEN_PAYER()
HIDDEN_OBSERVER()
HIDDEN_STANDARD()
HIDDEN_BOUNDARY()
HIDDEN_SCALE()
HIDDEN_TIME()
TYPECHECK()
SURVIVAL_VECTOR()
MISUSE_AUDIT()
FAILURE_PROPAGATION()
```

## Registered Future Calls

```text
Corpus.semantic_address()
Ledger.cost_and_consent()
BIDIRECTIONALITY()
BASIS_CHALLENGE()
DOMAIN_HOLDOUT()
BLIND_MATCH()
ASSUMPTION_SWAP()
SEMANTIC_CHECKSUM()
WITNESS_PANEL()
PREDICTION_ESCROW()
SCALE_SCAN()
COUNTERMODEL()
```

These remain registered until the needed data, rival models, or independent
witness protocol exists.

## Commands

```powershell
python _scripts\claim_runtime.py intake path\to\paper.md
python _scripts\claim_runtime.py graph
python _scripts\research_runtime.py registry
python _scripts\research_runtime.py manifest path\to\paper-or-packet.json
python _scripts\research_runtime.py failure tp:master-equation/01/ME-01-060
```

## Artifact Manifest

Every generated manifest carries:

```yaml
paper_id:
one_sentence:
claim_ids:
claim_summary:
hidden_dependencies:
types:
survival_vector:
misuse_audit:
registered_but_not_run:
```

The runtime should not average the Survival Vector into a flattering score.
It publishes the vector and names the lowest coordinate.

## Public Boundary

Score claims, actions, systems, and arguments.

Do not score souls.
