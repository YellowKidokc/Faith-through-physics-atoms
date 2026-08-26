# Topbar Fill Packet System

This is the bridge between Faith Through Physics Atoms and the canonical website top bar.

Use it when an atom, article, paper, axiom, or master-equation note needs to become a canonical HTML page.

## The Plain Rule

The atoms repo owns truth.

The topbar builder owns presentation.

The fill packet is the handoff between them.

An AI may fill or improve the packet. It must not hand-edit the top bar, footer, CSS, renderer, dialog, proof drawer, audio dock, or canonical shell markers.

## What To Hand Another AI

Give the AI these items:

1. The source markdown, atom JSON-LD, paper, or article text
2. This document
3. `_template/11_articles/TOPBAR_FILL_PACKET.template.json`
4. The instruction: "Fill the packet only. Do not make a full HTML page."

The AI returns one completed JSON packet.

## Where Everything Goes

| Source material | Packet field | Notes |
|---|---|---|
| Page identity | `page` | Title, subtitle, series, byline, previous/next |
| Atom IDs / claim IDs | `page.sourceAtoms` | Keep traceability back to this repo |
| Glossary / domain terms | `terms[]` | These become topbar term pills and term dialog cards |
| Load-bearing claims | `claims[]` | Use exact visible sentences where possible |
| Formal support | `proofs[]` | Link each proof to claim IDs |
| Master equation / equations | `mtl[]` | Math Translation Layer records |
| Reading layers | `reader_layers` | High school, college, PhD content blocks |
| Top panel stats | `verification[]` | Four compact cards works best |
| Audio links | `audio[]` | Four slots; blank URL means safely disabled |
| Honest critique | `audit` | right, overstated, wrong |

## Copy-Paste Boundary

The packet is JSON only.

Do not paste:

- `<!DOCTYPE html>`
- `<html>`, `<head>`, or `<body>`
- topbar HTML
- footer HTML
- CSS
- JavaScript
- duplicate audio dock markup
- canonical marker comments

Do paste:

- headings
- paragraphs
- lists
- tables
- claim spans
- short inline HTML needed inside `reader_layers`

For `reader_layers`, paste only the inside of the layer. The builder supplies the actual wrapper.

Good:

```json
"college": "<h2>The Argument</h2><p>Article text...</p>"
```

Not good:

```json
"college": "<section class=\"ftp-reader-layer\" data-reader-layer=\"college\">...</section>"
```

## Claim Sentence Rule

Every important assertion gets a stable ID.

The exact public sentence goes in `claims[].sentence`.

The same sentence should appear in the article content wrapped like this:

```html
<span class="ftp-claim-sentence" data-claim-id="MEQ-C001">The exact claim sentence appears here.</span>
```

If the claim is not ready, mark it `draft`. Do not call something verified just because it sounds strong.

## MTL Rule

Every important equation needs a Math Translation Layer entry.

Use `format: "inline"` when the equation is simple.

Use `format: "box"` when the structure matters, especially for:

- product collapse
- minus signs / opposition
- boundary behavior
- one-way arrows
- conservation
- integrals / accumulation

## Three AI Call Mapping

If using the 3-call topbar fill pipeline:

| Call | Fills |
|---|---|
| Call 1: Topbar + Terms + Verification | `terms[]`, `verification[]`, part of `page` |
| Call 2: Claims + Proofs + MTL | `claims[]`, `proofs[]`, `mtl[]` |
| Call 3: Adversarial Audit | `audit.right`, `audit.overstated`, `audit.wrong` |

The final human/AI pass fills or revises `reader_layers`.

## Review Checklist

Before building:

- `page.id` is unique
- `page.sourceAtoms` lists the source atom IDs
- every claim has `sentence`, `formal`, `status`, `derivation`, `killCondition`
- every proof links to at least one claim
- every claim proof ID exists in `proofs[]`
- every important equation appears in `mtl[]`
- highschool, college, and phd reader layers are filled
- audio has four slots, even if URLs are blank
- audit has right, overstated, and wrong arrays

After building:

- validate the JSON
- build the HTML
- validate the built HTML
- visually check that the top bar appears once
- visually check that audio is either present once or safely absent
- visually check that claim clicks and MTL/proof panels work

## Build Command

Copy the filled packet to:

```text
D:\GitHub\Python-WEB\topbar\canonical-page-shell\pages\
```

Then run:

```powershell
cd D:\GitHub\Python-WEB\topbar\canonical-page-shell
node validate-page.js pages\YOUR_PACKET.json
node build-page.js pages\YOUR_PACKET.json --out dist\YOUR_PAGE.html --validate
```

If validation fails, fix the packet. Do not fix the shell.

## Name Recommendation

Use this filename pattern:

```text
TOPBAR_FILL_PACKET.<domain>.<slug>.json
```

Examples:

```text
TOPBAR_FILL_PACKET.master-equation.master-equation.json
TOPBAR_FILL_PACKET.axioms.axiom-001.json
TOPBAR_FILL_PACKET.evolution.inverse-solver.json
```

This is the part David fills, or another AI fills, before the topbar builder turns it into a page.
