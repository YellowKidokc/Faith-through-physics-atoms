# Knowledge Construction Workbook — Integration Contract v1

Template: [Knowledge Construction Workbook](../_templates/KNOWLEDGE_CONSTRUCTION_WORKBOOK.md)

## What it does
An Obsidian-native foldable checklist and reasoning record. The selectable registry is finite **for this version**, not an exhaustive enumeration of every legitimate inference system. Every selected method must carry its own rationale, inputs, actual execution, result, and limits.

## Non-negotiable distinctions
1. Discovery does not justify a claim. Freeze the hypothesis before confirmatory testing.
2. Intake/provenance, formal representation, inference, interpretation, and validation are distinct.
3. Deductive validity means conclusion follows *if premises hold*; soundness additionally requires true premises.
4. Evidence strength is distinct from component coverage; use [Evidence Coverage Method](EVIDENCE_COVERAGE_METHOD.md).
5. Cross-domain resemblance is not automatically isomorphism; demonstrate mapping, bijection, and preserved structure before that label.
6. Independent AI first-pass reviews must document model/version, inputs, disagreements, external checks, and human adjudication. Agreement is not proof.
7. Respect the [Adversarial Review Gate](ADVERSARIAL_REVIEW_GATE.md): an AI pass cannot accept graph edges.
8. Respect the [Canonical Publication Gate](CANONICAL_PUBLICATION_GATE.md): source workbook, frozen publication, and living Atlas status are separate.
9. No silent revision of the original hypothesis. Append new versions.
10. Distinguish logical validity, premise warrant, soundness, empirical support, and overall disposition.

## How to use
Copy the template to a new note, complete Page Zero, Discovery, and Hypothesis; timestamp the original. Work through applicable method options and record exact source/premise IDs. Keep unused options unchecked. Run at least one serious adversarial test and record unresolved objections. Use the FACTS crosswalk to author a readable paper while retaining the full workbook for audit.

## Technical limitations
Obsidian renders `> [!note]-` as a collapsed callout, but folding **does not delete unused content**. YAML frontmatter is machine-readable metadata, while body checkboxes are separate Markdown; they do not synchronize automatically. Obsidian's Properties editor does not support arbitrary nested YAML as editable structured fields. Automatic export of only activated stages requires a separate parser/renderer, **not included** in this change.

## Acceptance checks
- New files only; no existing canon or Atlas state modified.
- Frontmatter parses as YAML.
- Foldable callouts and checkbox menus exist for all 13 sections.
- Hypothesis freeze, evidence coverage, human gate, multi-AI adjudication, and return audit are documented.
- The workbook does not imply automatic truth certification or canon promotion.
