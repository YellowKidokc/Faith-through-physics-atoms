# Seven-Question Dossier Protocol

## Purpose

Turn a dossier from a narrative research page into a structured investigative object.

Core rule:

`Dossier = Structured Answer Set to One Core Question`

The dossier is therefore not primarily:

- summary
- evidence
- discussion

It is primarily:

- identity
- domain
- claim
- evidence
- dependencies
- consequences
- falsification

## Investigative Spine

Every dossier should answer these seven in order:

1. `Q1 Identity`
2. `Q2 Domain`
3. `Q3 Claim`
4. `Q4 Evidence`
5. `Q5 Dependencies`
6. `Q6 Consequences`
7. `Q7 Falsification`

This is the dossier protocol.

## Q1 Identity

Question:

`What exactly are we investigating?`

Required fields:

```yaml
identity:
  uuid:
  dossier_id:
  title:
  subject:
  entity_type:
  axiom_class:
  notation:
```

Function:

- establishes the target
- prevents ambiguity
- fixes naming and identity drift

## Q2 Domain

Question:

`Where does this object live?`

Required fields:

```yaml
domain:
  primary_domain:
  subdomain:
  scale:
  regime:
  cross_domains:
    theology:
    consciousness:
    information:
```

Function:

- establishes context
- prevents domain confusion
- supports graph placement

## Q3 Claim

Question:

`What exactly is being asserted?`

Required fields:

```yaml
claim:
  claim_type:
  precision_level:
  statement:
  mathematical_form:
  scope:
```

Function:

- defines the core assertion
- prevents vague claim drift
- anchors downstream evidence and falsification

## Q4 Evidence

Question:

`What supports this claim?`

Required fields:

```yaml
evidence:
  - id:
    type:
    source:
    description:
    replication_status:
```

Evidence categories:

- experimental
- observational
- mathematical
- logical
- historical
- scriptural
- computational

Function:

- keeps evidence separate from interpretation
- forces atomic support objects

## Q5 Dependencies

Question:

`What must already be true for this to stand?`

Required fields:

```yaml
dependencies:
  axioms: []
  laws: []
  required_theories: []
  assumptions: []
```

Function:

- reveals hidden assumptions
- shows load-bearing structure

## Q6 Consequences

Question:

`If true, what follows?`

Required fields:

```yaml
consequences:
  predictions:
    - description:
      test_method:
  theoretical_implications:
  framework_implications:
```

Function:

- converts claims into tests
- makes framework consequences explicit

## Q7 Falsification

Question:

`How does this die?`

Required fields:

```yaml
falsification:
  conditions:
    - description:
  death_condition:
```

Function:

- acts as the death warrant
- prevents non-scientific closure

## Forward Mode

Normal dossier flow:

`Identity -> Domain -> Claim -> Evidence -> Dependencies -> Consequences -> Falsification`

## Reverse Mode

Reverse dossier flow:

`Falsification -> Consequences -> Evidence -> Claim`

Use reverse mode when the work begins from:

- adversarial review
- destruction manual
- kill-switch design
- contradiction hunt

## Page Rendering

The dossier protocol is the investigation spine, not the visible page skeleton.

Recommended page rendering can still use:

1. Hero
2. FACTS
3. Media
4. Body
5. Evidence
6. Related
7. Structure
8. Footer

But the page should be backed by `Q1-Q7`, not by arbitrary article ordering.

## Graph Consequences

Every dossier should become a graph object with edges like:

- `depends_on`
- `supports`
- `predicts`
- `contradicts`
- `falsifies`

## Dossier Types

Likely extensible dossier families:

- theory dossier
- axiom dossier
- experiment dossier
- entity dossier
- controversy dossier
- application dossier
- worldview dossier

## Why This Is Stronger

Most dossiers mix:

- evidence
- analysis
- rhetoric
- opinion

This protocol forces separation and makes every dossier:

- deterministic
- machine-navigable
- comparable
- difficult to manipulate rhetorically
