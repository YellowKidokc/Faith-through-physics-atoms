# PAPERS
## Composites. Not domains, not stages.

A **claim** has exactly one domain. That is its address.
A **paper** spans many domains. It has no address — it has parts.

That is why papers live here and not inside a domain folder. A paper that
is 70% education, 20% information-theory and 10% economics cannot sit in
`education/` without lying about the other 30%.

## The rule

> **A paper points at claims. It never contains them.**

Every paper's `paper.yaml` lists its claims by `claimID`. Falsify a claim
in any domain and every paper carrying it is affected automatically. That
is what makes cherry-picking impossible — the structure knows what depends
on what.

## Layout

```
papers/
  <paper-slug>/
    paper.yaml        machine-readable index (paper-spec compatible)
    manuscript.md     the prose, with the 3-sentence header on top
    figures/
    runnable/         scripts a reader can execute
```

No stage folders in here. Stages are how a **claim** ripens. A paper is an
**output** — it does not ripen, the claims under it do.

## paper.yaml

Conforms to the paper-spec standard (CC-BY-4.0) so the claims validate
against an external open schema, plus Theophysics extensions:

```yaml
spec_version: "0.1.0"
meta:
  title: ""
  authors: []
  aiContributionDeclared: true      # tp extension
claims:                              # by claimID, across domains
  - id: "tp:education/transmission-failure"
    status: supported
acceptance:
  - claim_id: ""
    criterion: ""
    falsification: ""                # required, never omitted
dependencies:
  - reference: ""
    relationship: "extends|contradicts|builds_on"
    critical: true                   # critical=true propagates
limitations:
  - description: ""
    severity: "major|minor"
    addressable: true

# Theophysics extensions
tp_composition: {education: 0.7, information-theory: 0.2, economics: 0.1}
tp_bridge_grades: {}                 # per cross-domain claim
tp_descent_complete: false           # has it reached audienceLevel=everyday
tp_compliance: 0                     # of 10, per REIMAGINED_DOCTORAL_PAPER.md
```

## Entry points

- **Humans** enter at `00_TITLES.md` — every title A-Z, links to papers and claims.
- **AI collaborators** enter at `README_AI_START_HERE.md`, which points here and to the domains.
- **Either route converges on the same claims.** A paper is a valid entry
  because its `hasPart` traverses down into the domains.

## Not every seed deserves a paper

Every factual claim deserves enough rigor to state it honestly. Only claims
that complete the technical branch become paper candidates.
