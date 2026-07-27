# FAITH THROUGH PHYSICS — READ ME FIRST
## Theophysics Research Initiative | POF 2828
## If you are an AI, read this entire file before doing anything else.

---

## WHAT IS THIS FOLDER

This is the canonical production root for the Faith Through Physics 
framework. Every domain, every claim, every article, every proof 
lives here. The structure IS the scientific method.

## HOW IT'S ORGANIZED

### Top level = DOMAINS
Each folder at the top level is a knowledge domain: physics, theology, 
education, psychology, economics, etc. The list is infinite — add a 
new domain anytime by running the batch script.

### Inside each domain = THE 14-STAGE ARC
Every domain contains the same 14 numbered subfolders. They represent 
the complete lifecycle of a truth-claim:

```
00_inbox_working   — Raw thinking, voice dumps, unsorted
01_canonical       — Locked truth, proven claims
02_paradigm        — What this breaks about old thinking
03_synthesis       — How it connects to other domains
04_hypothesis      — If true, then THIS must follow
05_evidence        — External research, LLM, wiki, data
06_falsification   — Kill conditions, what would break it
07_paper           — Formal doctoral-level treatment
08_objections      — Strongest pushback, steelmanned
09_everyday        — Plain language Monday morning version
10_worldcheck      — Everyday version pressure-tested
11_articles        — Narrative story form, readable
12_audience        — SEO, social, widest reach, toolkits
13_fulfilled       — Did it hold, what happened, the receipt
```

### Not every file uses all 14 stages
Content enters wherever it naturally sits. Most content enters at 
11_articles. Some enters at 07_paper. Some at 09_everyday.

## THE ONE RULE YOU CANNOT BREAK

**PUSHING UP IS OPTIONAL. PUSHING DOWN IS NEVER OPTIONAL.**

You can skip every stage ABOVE a file's entry point.
You can NEVER skip the stages BELOW it.
Every truth must descend until it reaches the everyday person.

The PhD paper that never becomes a Monday morning conversation 
is a failed paper. The equation that never becomes "here's what 
this means for your marriage" hasn't finished its job.

The everyday person is the floor. Everything reaches the floor.


## THE NODES (Faith Through Physics Atoms)

Every stage produces a specific type of node. Nodes are stored 
as .jsonld files (machine-readable) with .html pills generated 
from them (human-readable).

**CRITICAL: Only 01_canonical nodes are CLAIMS.** Everything else 
is a node AROUND a claim — it orbits, supports, attacks, translates, 
or confirms the claim. The claim is the sun.

### Node DNA (every node has this):
- **nodeID** — unique ID (every node gets this)
- **claimID** — only on 01_canonical claim nodes
- **name** — human-readable title
- **nodeType** — raw, claim, paradigm, bridge, prediction, evidence, 
  kill, paper, objection, translation, check, article, reach, result
- **domainType** — which domain this belongs to
- **stage** — which of the 14 stages
- **status** — draft | active | verified | falsified | deprecated
- **edges** — typed connections to other nodes:
  ```
  { type: "dependsOn", target: "node-id", 
    grade: "structural_identity", propagates: true }
  ```

### Bridge grades (on edges, not nodes):
- **structural_identity** — same equation, PROPAGATES falsification
- **structural_isomorphism** — formal math mapping, PROPAGATES
- **structural_analogy** — similar but not proven, does NOT propagate
- **metaphorical** — illustrative only, does NOT propagate

### The graph builds itself:
When you create a node and set its edges, the graph grows.
An AI scanning all nodes can discover connections you haven't 
seen — two claims in different domains sharing an axiom root 
means a potential bridge nobody planned.

## HOW TO ADD A NEW DOMAIN

Run from this folder:
```
python _scripts\new_domain.py [domain-name]
```
Example: `python _scripts\new_domain.py materials-science`

This copies the template and creates all 14 stage folders 
with README checklists in each one.

To create ALL initial domains at once:
```
python _scripts\batch_create_domains.py
```

## HOW TO CREATE A NEW ATOM

```
python _scripts\atom_builder.py --domain education --stage 01_canonical
```

The builder walks you through required fields, generates 
the .jsonld file, and renders the .html pill.

## HOW TO QUERY THE GRAPH

```
python _scripts\atom_graph.py --bridges education economics
python _scripts\atom_graph.py --missing-plain
python _scripts\atom_graph.py --propagate-falsify education-01-001
```

## FILE TAGGING

Every file gets three tags in its frontmatter:

```yaml
entry_layer: 07_paper      # where it IS now
max_layer: 01_canonical    # how far UP it could go
next_action: "needs 09_everyday version"
```

Stages below entry_layer = your TODO list.

## FOLDER STATUS ICONS

Each stage folder uses desktop.ini to show its status:

| Icon | Meaning |
|------|---------|
| ○ (empty circle) | Stage is empty — no content yet |
| ◐ (half circle) | Stage has content — work in progress |
| ● (full circle) | Stage is complete — all checklist items done |

## FULL SPECIFICATIONS

For complete details, read these canonical documents:
- Architecture spec: _docs\THEOPHYSICS_ARCHITECTURE_v11_CANONICAL.md
- Node types: _docs\CLAIM_ATOM_NODE_TYPES.md
- Decision log: _docs\ARCHITECTURE_DECISION_LOG.md
- Codex build pack: _docs\ATOM_BUILD_PACK.md
- Folder beacon scan and batch editing: _docs\FOLDER_BEACON_SYSTEM.md

---

_Faith Through Physics | POF 2828_
_"The Word became flesh and dwelt among us." — John 1:14_
_Truth always flows down._
