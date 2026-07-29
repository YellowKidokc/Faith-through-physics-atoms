# Baseline Consolidation Prompt

Target branch:
`codex/set-up-api-for-adversarial-testing-g9m82n`

GitHub URL:
`https://github.com/YellowKidokc/Faith-through-physics-atoms/tree/codex/set-up-api-for-adversarial-testing-g9m82n`

## Goal

Consolidate the repository down to the baseline structure instead of keeping many repeated domain/template sets.

The linked branch baseline currently contains only these top-level directories:

```text
.well-known
_docs
_proposals
_protocol
_scripts
_template
_vocab
master-equation
```

The current local checkout contains many additional top-level domain/scaffold folders, including:

```text
addiction-science
ai-alignment
axioms
biology
christian-life
consciousness
control-theory
cosmology
cryptography
demo-v12
ecology
economics
education
epidemiology
fluid-dynamics
history
information-theory
lean
music-theory
network-science
papers
pharmacology
physics
psychology
scripture
ten-laws
theology
trinity
```

Many of these are repeated copies of the same 14-stage domain scaffold. The job is to reduce the repo to the baseline while preserving any real content that should survive.

## Important Safety Rule

Do not blindly delete folders just because they look duplicated.

First classify every non-baseline top-level folder as one of:

```text
KEEP_IN_BASELINE
MIGRATE_CONTENT_THEN_REMOVE
ARCHIVE_ONLY
REMOVE_EMPTY_SCAFFOLD
NEEDS_HUMAN_REVIEW
```

Only remove a folder automatically if it is scaffold-only or already represented in the baseline.

## What "Baseline" Means Here

Baseline should mean:

```text
system/docs/scripts/protocol/vocab/template + master-equation
```

The Master Equation is the governing layer. It stays.

The repeated domain folders should not stay at top level unless they contain canonical content that has no baseline home yet.

## Package/Set Consolidation

This repository should not have many competing package roots.

Current package scan found no top-level `package.json` and no top-level `pyproject.toml`.

One untracked package-like folder exists locally:

```text
canon_guard_v0.1.0/canon_guard/pyproject.toml
```

Decision needed:

1. If `canon_guard_v0.1.0` is active runtime code, move or merge it into the baseline runtime/script area.
2. If it is an export/package artifact, archive it outside the repo or under `_archive/`.
3. Do not introduce a second package-management baseline unless the repo deliberately becomes a Python package.

Preferred baseline:

```text
_scripts/
_runtime/
_docs/
_protocol/
_vocab/
_template/
master-equation/
```

Do not create several independent package roots unless there is a clear reason.

## Consolidation Procedure

1. Start from a clean branch based on:

```text
origin/codex/set-up-api-for-adversarial-testing-g9m82n
```

2. Inventory all top-level folders.

3. Treat these as baseline keepers:

```text
.well-known
_docs
_proposals
_protocol
_scripts
_template
_vocab
master-equation
```

4. For every other top-level folder, count real content:

```text
markdown files
json/jsonld files
lean files
python files
html files
csv/jsonl data
non-template README content
```

5. Detect scaffold-only folders by looking for:

```text
00_inbox_working
01_canonical
02_paradigm
03_synthesis
04_hypothesis
05_evidence
06_falsification
07_paper
08_objections
09_everyday
10_worldcheck
11_articles
12_audience
13_fulfilled
_theological
```

If the folder only contains default `README.md`, `.fisnote`, `desktop.ini`, and empty stage folders, mark it:

```text
REMOVE_EMPTY_SCAFFOLD
```

6. If a folder has real files but is just a domain copy, migrate the real files to an appropriate baseline location:

```text
master-equation/      -> master equation laws, factors, coherence, Lean-related ME notes
_docs/                -> architecture, process, reviews, handoff docs
_protocol/            -> schemas, workflows, claim protocols
_vocab/               -> dictionaries, law names, controlled vocabulary
_proposals/           -> candidate bridges, adversarial review inputs/outputs
_archive/             -> old exports or non-current material
```

7. Create a manifest before deleting or moving anything:

```text
_docs/BASELINE_CONSOLIDATION_MANIFEST_20260729.md
```

The manifest must include:

```text
folder
classification
file count
content count
action
destination
reason
```

8. Apply the consolidation.

9. Run validation:

```text
git status --short
python _scripts/test_adversarial_review.py
python _scripts/adversarial_review.py --help
python _scripts/adversarial_gui.py --help
```

If tests are not runnable, record the exact failure in the manifest.

## Expected End State

The branch should end with one coherent baseline:

```text
.well-known/
_docs/
_proposals/
_protocol/
_scripts/
_template/
_vocab/
master-equation/
```

Optional, only if justified:

```text
_archive/
_runtime/
```

Do not leave old scaffold domains at top level unless they contain active canonical content and are intentionally part of the baseline.

## Special Warning About Current Worktree

The current local working tree may already be dirty, with many tracked deletions and local untracked files.

Do not run destructive cleanup commands against that dirty worktree.

Use a fresh clone or a fresh worktree for this consolidation:

```text
git worktree add ../ftp-baseline-consolidation origin/codex/set-up-api-for-adversarial-testing-g9m82n
```

Then perform the consolidation there.

## Human-Readable Summary

We are not trying to keep ten different sets of the same framework.

We want:

```text
one baseline
one Master Equation authority
one script/runtime area
one vocabulary/protocol layer
one place for current proposals/reviews
no duplicated empty domain scaffolds
no accidental deletion of real content
```

