# Faith Through Physics Graph Viewer Structure

Date: 2026-07-28  
Prepared by: Codex  
Purpose: structural design for the graph/paper/pill viewer before frontend polish.

## Product Name

Visible umbrella:

```text
Faith Through Physics
```

Working page title:

```text
Faith Through Physics Atlas
```

Subtitle:

```text
Papers, claims, glyphs, proofs, and consilience maps in one living graph.
```

## Core Principle

The app should not feel like a landing page.

It should open directly into the working reader/graph experience.

```text
left: paper / selected node detail
center: graph canvas
right: inspector / popup card / filters
top: graph mode, node type, search, proof-status controls
```

## Main Layout

```text
+-------------------------------------------------------------------+
| Faith Through Physics      Search...      Graph Mode    Filters    |
+---------------+---------------------------------------+-----------+
| Paper Index   |                                       | Inspector |
| /Pills        |            Graph Canvas               | /Popup    |
| /Glyphs       |            2D or 3D                   | /Receipts |
|               |                                       |           |
+---------------+---------------------------------------+-----------+
| Status strip: selected graph / node count / warnings / receipts     |
+-------------------------------------------------------------------+
```

## Top Bar

Required controls:

```text
Brand: Faith Through Physics
Global search
Graph mode selector
Node type selector
Proof-status filter
Open paper button
Export/share button
```

Graph mode selector:

```text
Knowledge Graph
Dependency Graph
Proof Graph
Evidence Graph
Semantic Graph
Isomorphic Graph
Consilience Graph
Contradiction Graph
Narrative Graph
Reader Path
```

Node type selector:

```text
Papers
Claims
Evidence
Proof Receipts
Kill Conditions
Glyphs
Pills
Domains
Equations
Lean
Python / Colab
Story Anchors
```

Proof-status filter:

```text
All
Lean Formal
Lean Conditional
Runtime Supported
Bridge Declared
Consilience Candidate
Isomorphic Candidate
Rerun Owed
Not Established
Quarantine
```

## Left Panel

The left panel is the navigation spine.

Tabs:

```text
Papers
Pills
Glyphs
Domains
Saved Views
```

Paper list item:

```text
Title
Domain
Status badge
Claim count
Warning count
```

Pill list item:

```text
Pill name
Short meaning
Linked atom count
Proof-status mix
```

Glyph list item:

```text
Glyph symbol
Semantic meaning
Mapped laws / variables / claims
```

## Center Graph Canvas

The graph canvas should support:

```text
2D force graph
3D force graph
fit to selection
highlight neighborhood
pin / unpin node
expand / collapse edges
show edge labels
show only selected graph mode
```

Node visual language:

```text
Paper node: larger document tile / sheet marker
Claim node: small bright dot
Evidence node: square or receipt marker
Proof node: shield/check marker
Kill condition: red boundary marker
Glyph node: symbol marker
Pill node: rounded tag marker
Domain node: cluster hub
```

Edge visual language:

```text
claims: solid
supports: green
dependsOn: blue
contradicts: red
weakens: orange
isomorphicWith: purple
consilientWith: gold
verifiedBy: check/green
rerunOwedBy: dashed red
expressesGlyph: faint dotted
appearsInPaper: gray
```

## Right Inspector

The right panel is the popup card made persistent.

Card sections:

```text
Header
Plain meaning
Proof label
Mode classification
Source paper / sentence
Linked atoms
Glyphs
Evidence
Kill conditions
Warnings
Receipts
Open in paper
Open ledger record
```

Compact popup card fields:

```json
{
  "title": "Truth is ontological",
  "kind": "claim",
  "proofLabel": "BRIDGE_DECLARED",
  "modeClassification": "CONSILIENCE_CANDIDATE",
  "plainMeaning": "Truth-bearing correspondence is prior to science, morality, and repair.",
  "glyphs": ["truth", "logos", "coherence"],
  "warnings": ["Not Lean proof", "Theological conclusion conditional"],
  "actions": ["Open paper", "Open atom", "Show neighborhood"]
}
```

## Paper Reader Mode

When a paper opens, it should still feel like reading.

Paper view contains:

```text
Title
Pills under/near title
Readable article body
Claim dots beside key sentences
Glyph chips inline or in margin
Status strip per section
```

Interaction:

```text
click title pill -> pill popup
click claim dot -> claim card
click glyph -> glyph card
click proof badge -> receipt card
click graph button -> show selected sentence in graph
```

## Data Inputs

The viewer should read:

```text
framework_graph.json
paper.graph-manifest.json files
Lane 4 atom JSON
live_claim_ledger.jsonl
glyph registry
topbar fill packets
anchor_lines manifests
```

Minimum manifest contract:

```json
{
  "paperID": "CROWN:TRUTH-SERIES-001",
  "title": "The Truth Series",
  "paperAtomID": "tp:lane4/crown-canon/crown-truth-series-001",
  "htmlPath": "C:/theophysics/CROWN_CORE/02_CROWN_CANON/THE_SERIES/00_INDEX.md",
  "pills": ["Truth", "Logos", "Math", "Law", "Good/Bad"],
  "anchors": [
    {
      "anchorID": "TRUTH-C001",
      "text": "Truth is ontological.",
      "atomIDs": ["tp:lane4/crown-canon/crown-truth-series-001"],
      "glyphIDs": ["glyph:truth", "glyph:logos"],
      "proofLabel": "BRIDGE_DECLARED",
      "modeClassification": "CONSILIENCE_CANDIDATE"
    }
  ]
}
```

## Built-In Views

Start with these saved views:

```text
Master Equation
Truth Series
Good / Bad Consilience
Logos Grounding
Lean Receipts
Rerun Owed
Isomorphic Events
Fruit Audit
Narrative Anchors
```

## What I Would Tell David

Build one reusable shell.

Do not hand-design every paper.

The shell should ingest manifests and render the same controls every time.

The first version only needs to prove the workflow:

```text
open paper
see title pills
click claim dot
open popup
jump to graph
click graph node
return to paper
```

Once that loop works, Kimmy can make it beautiful.

## Non-Negotiable Guardrail

The graph must never silently promote a claim.

```text
visual connection != proof
edge type matters
proof label comes from the atom ledger
paper language cannot outrun ledger status
```

## Suggested MVP

MVP 1:

```text
Static HTML app
2D graph
paper reader
claim popups
title pills
right inspector
local JSON manifests
```

MVP 2:

```text
3D graph mode
glyph registry cards
saved views
proof receipt timeline
filterable edge types
```

MVP 3:

```text
automatic paper annotation
live claim intake
graph export
reviewer comments
canon promotion queue
```
