# Faith Through Physics Information Object Standard — Candidate Workbench

This packet compiles the existing default and expanded information-object systems without changing or deleting their source files.

## Architectural ruling

1. **Universal envelope:** stable identity, type, status, version, provenance, and typed edges.
2. **Object category:** what the record is—claim, evidence, equation, source atom, audit, media, and so forth.
3. **Workflow stage:** where the object currently sits—inbox, canonical-claim candidate, synthesis, falsification, publication, or review.
4. **Type-specific payload:** fields required only for that category.
5. **Review state:** a separate judgment record; it must not silently mutate the reviewed object.

The default envelope should remain small. Expanded schemas supply specialized fields. JSON-LD is the machine authority; HTML is a generated human view; Markdown is the editable explanatory companion.

## Non-claims

- Copying a record here does not canonize it.
- A formal receipt proves only the encoded statement under its assumptions.
- Evidence supports or challenges a claim; it is not itself the claim.
- An isomorphism record must state its mapping, invariants, inverse/bijection requirements where applicable, boundary conditions, and kill test.

## Rebuild

Run `_scripts/build_information_object_standard.py`. The build recreates this folder from selected repository sources and writes hashes and validation results under `99_MANIFEST`.
