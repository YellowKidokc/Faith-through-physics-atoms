# Canonical Publication Gate

Lock this distinction before building Ascendant/Descendant templates:

**Markdown source is not canonical publication is not Living Atlas state.**

- Markdown/source files are authoring inputs.
- Canonical HTML/JSON are frozen published snapshots.
- The Atlas registry and graph own living epistemic state.

Canonical promotion must be explicit. Run:

```bash
python _scripts/canon_gate.py path/to/source.md --version-id PAPER-023-v1.4
```

That writes a sidecar only. To freeze canonical HTML/JSON and append the
registry row, rerun with:

```bash
python _scripts/canon_gate.py path/to/source.md --version-id PAPER-023-v1.4 --accept-canon
```

Promotion records two statistic classes:

- frozen publication statistics, which never change
- living Atlas statistics, which can update forever

Later research may update current Atlas standing, but it must not rewrite the
historical publication snapshot.
