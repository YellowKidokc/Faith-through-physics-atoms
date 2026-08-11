# Page Aggregation API

The page aggregation call is independent from claim extraction and evidence
extraction.

Claim/evidence calls produce granular objects. The page aggregation call
consumes the whole page plus already-admitted Atlas records and produces a
coherent, repeatable map summary.

Run:

```bash
python _scripts/page_aggregate.py path/to/page.html --output _atlas/page-aggregations/page.json
```

The output follows `_schema/page_aggregation.schema.json` and includes:

- the ten map definitions from `_atlas/view-definitions.json`
- admitted evidence coverage summaries
- Ascendant / Descendant / Meeting projection state
- Lane 4 receipts
- Python test receipt slot
- Colab receipt slot
- warnings when the page cannot be tied directly to claim atoms

This call does not create claims, accept evidence, promote canon, or infer new
bridges. It is a reader-facing aggregation over existing admitted data.
