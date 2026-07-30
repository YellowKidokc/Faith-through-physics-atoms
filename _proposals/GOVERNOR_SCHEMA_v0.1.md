# GOVERNOR SCHEMA v0.1 — Meta-Layer Node Class and Routing Rule
**POF 2828 | 2026-07-30 | Fable | Status: PROPOSAL — satisfies the bootstrap-review
requirement ("explicit schema/routing design before governor becomes a node type")**
**Reference implementation: _scripts/governor_route.py (self-tested, all four gates fire)**
**Test fixture: _scripts/governor_test_manifest.json**

## 1. What a governor is
A governor is a node that constrains TRAVERSAL, not content. Claims are suns;
orbits support or attack them; governors are the sky both move under. A governor
never asserts anything about the world — it asserts what may be CITED, at what
LABEL, across which EDGES.

## 2. Node shape (JSON-LD additions)
```json
{
  "nodeID": "GOV-G02",
  "nodeType": "governor",
  "governorClass": "label-gate | overclaim-filter | grade-rules |
                    trust-boundary | criteria | controls",
  "scope": ["unification"],
  "ruleset": { },
  "status": "active",
  "edges": [ {"type": "governs", "target": "domain:unification",
              "grade": "structural_identity", "propagates": true} ]
}
```
Rules: governors carry NO claimID, are never counted as claims, and are the only
nodeType permitted a "governs" edge. A domain with zero active governors is
UNROUTABLE by policy (fail-closed, not fail-open).

## 3. The routing rule (the sequence proven by hand on 2026-07-30)
```
query
 -> resolve governors for target domain(s)        [fail-closed if none]
 -> G02 overclaim filter on candidate atom text    [BLOCKED: not reproducible]
 -> G06 completeness: claims must carry kill conds [MALFORMED: not citable]
 -> G01 label check                                [MALFORMED if unlabeled]
 -> G03 edge-grade check                           [MALFORMED if ungraded]
 -> G04 status admission:
      active/verified   -> ADMITTED   (citable)
      conditional/open  -> CONDITIONAL (nameable as open work only)
      falsified/deprecated/quarantined -> BLOCKED
 -> assemble answer from ADMITTED only
 -> stamp: labels present + router version + rule line
```
WRITTEN ≠ RUN lives here: everything stays in the graph; admission status alone
decides what an answer may contain. Nothing is deleted to stay dormant.

## 4. Integration map (invention already done piecemeal — this integrates)
| Existing organ | Becomes |
|---|---|
| canon_guard (UNIFICATION 34) | drift entries appended to G02 ruleset |
| OVERCLAIM_WARNINGS.csv (27) | merged into G02 ruleset |
| coherence scorer (35) | POST-admission ranking only — never admission |
| quarantine policy (99) | terminal status; router treats as BLOCKED |
| warrant labels (governance) | G01 ruleset |
| bridge grades (09 policy) | G03 ruleset |

## 5. What v0.1 does not do (honest scope)
- No semantic understanding: G02 is substring matching; the NLP stack (SBERT/
  DeBERTa) is the planned upgrade, same slot, same sequence.
- No transitive propagation yet: propagate-falsify remains atom_graph.py's job;
  v0.2 should call it after G03.
- No per-query scope resolution beyond domain tags.

## 6. Adoption gate
David reviews this file + runs the self-test. If ruled in: governorClass enters
the schema, six GOV atoms are minted for unification, and the API pill runner
(25) calls governor_route before assembly. Until ruled: this stays a proposal
and the manual pass remains the procedure.
