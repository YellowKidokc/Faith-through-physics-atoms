# API Call 15 — Reality 200 Abstract Truths Discovery

**Status:** Candidate discovery only. Nothing produced by this call is admitted into canon.

## Question

What are the 200 most important high-level truths or truth-candidates needed to describe reality as responsibly understood today across the major domains of knowledge?

## Design

The call is divided into twenty domain-balanced batches of ten records. This prevents physics, theology, or fashionable philosophical vocabulary from swallowing the entire list. Every record must distinguish established findings, formal truths, philosophical commitments, theological claims, and open conjectures.

## Required fields

- `id`
- `statement`
- `domain`
- `claim_mode`
- `epistemic_status`
- `confidence_0_to_100`
- `minimal_assumptions`
- `scope_boundary`
- `strongest_support`
- `strongest_rival`
- `defeat_or_revision_condition`
- `why_fundamental`
- `depends_on_ids`

## Governing rule

The API is being asked to produce a candidate map of our best present understanding, not timeless revelation and not automatic canon. A theological proposition may be important enough to include without being mislabeled as an empirical or formally verified result.

## Execution

Run:

```powershell
python "D:\GitHub\Faith-through-physics-atoms\_final_api_calls\run_reality_200.py"
```

The runner reads `DEEPSEEK_API_KEY` from the environment or an ignored `keys.txt`, `.env.local`, or `.env` at the repository root. Outputs are written beneath:

```text
C:\Users\David\Documents\faiththruphysics.com\60_EXCHANGE\REALITY_200
```

