# Paper Graph Overlay Architecture

Date: 2026-07-28  
Prepared by: Codex  
Purpose: define how papers, pills, glyphs, claims, evidence, and graph nodes stay connected without flattening the paper into a database.

## Core Idea

The paper remains readable as a paper.

The graph lives under it.

```text
paper sentence
-> claim anchor
-> atom node
-> glyph tags
-> evidence / bridge / kill-condition nodes
-> 3D graph position
-> popup / pill / paper return link
```

The public reader sees a clean page.

The framework reader can reveal the skeleton underneath.

## What Each Layer Does

### 1. Paper Layer

The paper keeps normal prose, but key sentences get anchor spans:

```html
<span
  class="ftp-claim-sentence"
  data-claim-id="TRUTH-C001"
  data-atom-id="tp:lane4/crown-canon/crown-truth-series-001"
  data-glyphs="truth,judgment,coherence"
>
  Truth is ontological.
</span>
```

This lets the sentence remain readable while giving the graph an exact line to point at.

### 2. Pill Layer

Title pills summarize the load-bearing structures:

```text
Truth
Logos
Math
Law
Good/Bad
Lean
Fruit
Master Equation
```

Each pill is not just decoration. It is a portal into:

```text
claim atoms
supporting evidence
glyphs
proof labels
kill conditions
open review status
```

### 3. Glyph Layer

Glyphs are semantic tags, not just icons.

Example:

```text
truth glyph -> truth-standard / exposure / Logos
coherence glyph -> alignment / integration / fruit
sin glyph -> misalignment / corruption / decoherence
grace glyph -> restoration / external repair / reset
```

The glyph lets the reader see the structural role before reading the whole explanation.

### 4. Atom Layer

Every important claim points to one or more atoms:

```text
claim atom
evidence atom
bridge atom
isomorphic-event atom
consilience atom
Lean receipt atom
runtime receipt atom
```

The atom decides the status:

```text
LEAN_FORMAL_PROOF
BRIDGE_DECLARED
CONSILIENCE_CANDIDATE
ISOMORPHIC_EVENT_CANDIDATE
RERUN_OWED
NOT_ESTABLISHED
```

The paper does not get to overrule the atom.

### 5. Graph Layer

The graph treats papers as first-class nodes.

```text
paper node
  -> section nodes
  -> paragraph nodes
  -> sentence/claim anchors
  -> atom nodes
  -> glyph nodes
  -> proof/evidence nodes
```

In 3D:

```text
papers = large document nodes
claims = bright small nodes attached to paper surface
glyphs = semantic hubs
evidence = support nodes
kill conditions = red boundary nodes
Lean/runtime receipts = verification nodes
```

Clicking the paper node opens the paper.

Clicking the small claim dot opens the popup.

Clicking the atom link opens the full ledger record.

## Popup Contract

Every clickable dot should have a compact popup:

```json
{
  "anchorID": "TRUTH-C001",
  "sentence": "Truth is ontological.",
  "atomID": "tp:lane4/crown-canon/crown-truth-series-001",
  "glyphs": ["truth", "logos", "coherence"],
  "proofLabel": "BRIDGE_DECLARED",
  "modeClassification": "CONSILIENCE_CANDIDATE",
  "plainMeaning": "The paper claims truth-bearing correspondence is prior to science, morality, and repair.",
  "supports": ["tp:lane4/logos/logos-god-terminal-ground-001"],
  "warnings": ["Not Lean proof.", "Theological conclusion remains conditional."],
  "killConditions": ["Show stable science/accountability/repair without truth-bearing correspondence."]
}
```

## Manifest Shape

Each paper should generate a `.graph-manifest.json` file:

```json
{
  "paperID": "CROWN:TRUTH-SERIES-001",
  "title": "The Truth Series",
  "htmlPath": "C:/theophysics/CROWN_CORE/02_CROWN_CANON/THE_SERIES/00_INDEX.md",
  "paperAtomID": "tp:lane4/crown-canon/crown-truth-series-001",
  "anchors": [
    {
      "anchorID": "TRUTH-C001",
      "selector": "[data-claim-id='TRUTH-C001']",
      "text": "Truth is ontological.",
      "atomIDs": ["tp:lane4/crown-canon/crown-truth-series-001"],
      "glyphIDs": ["glyph:truth", "glyph:logos"],
      "edgeTypes": ["claims", "dependsOn", "expresses"],
      "popup": {
        "proofLabel": "BRIDGE_DECLARED",
        "modeClassification": "CONSILIENCE_CANDIDATE",
        "warnings": ["Not Lean proof."]
      }
    }
  ]
}
```

## Edge Types

Use named edges so the graph is not just visual noise:

```text
paperContains -> paper to section/paragraph/anchor
claims -> anchor to claim atom
supports -> evidence to claim
dependsOn -> claim to upstream atom
bridgesTo -> cross-domain bridge
isomorphicWith -> isomorphic-event candidate
expressesGlyph -> claim/anchor to glyph
verifiedBy -> claim to Lean/runtime receipt
weakenedBy -> claim to kill condition
rendersAs -> atom/anchor to pill
opensPaper -> graph node to HTML/markdown paper
```

## Implementation Path

1. Keep papers as clean HTML/Markdown.
2. Add `data-claim-id`, `data-atom-id`, and `data-glyphs` attributes to key sentences.
3. Generate a graph manifest per paper.
4. Merge paper manifests with `framework_graph.json`.
5. Render a 3D graph where document nodes, claim nodes, glyph nodes, and evidence nodes are visible.
6. On click, show a popup for small nodes or open the paper for document nodes.
7. Never let visual edges change proof labels. The ledger remains the authority.

## Canon Rule

```text
The paper is the readable face.
The atom is the authority.
The glyph is the semantic shorthand.
The pill is the reader doorway.
The graph is the underlying skeleton.
```

That means nothing good gets lost in the paper, and nothing unsupported gets promoted by the graph.
