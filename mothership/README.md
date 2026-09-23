# Mothership Prototype

A self-contained proof-of-concept for the Faith Through Physics / Theophysics
"mothership" architecture: papers keep thin address maps, while the mothership
owns the canonical fat bodies.

## Architecture

- **Papers** emit JSONL address maps (`uuid`, `locator`, `anchor`, `source`).
- **Bodies** live in a central store keyed by `sha256(anchor.exact)`.
- **Mothership** scans address maps, pulls bodies, deduplicates identities,
  detects divergences, resolves addresses, and produces nightly reports.
- **CanonEngine** evaluates identities with deterministic rules before they are
  promoted to canon review.
- **Delta fast path** determines which addresses are touched by a document edit
  without re-reading papers.
- **CuratorPass** runs weekly to propose the next build actions: extract,
  define, link, cover, diverge, test, and meta proposals.
- **atom_to_pill** converts existing JSON-LD atoms into the YAML pill format
  consumed by the curator.
- **Companions** are CKG-style paper review wrappers published to
  `mothership/companions/` and consumed by the curator alongside pills and
  address maps.

## Quickstart

```bash
cd mothership
python -m pytest
```

## Modules

| Module | Purpose |
|--------|---------|
| `mothership.address` | `Address` dataclass and `resolve_address()` waterfall |
| `mothership.identity_store` | `IdentityStore`: dedupe by sha256, detect divergences |
| `mothership.mothership` | `Mothership`: scan maps, pull bodies, run nightly pipeline |
| `mothership.canon_engine` | `CanonEngine`: deterministic promotion rules |
| `mothership.delta` | `compute_touched_addresses()`: microsecond diff impact |
| `mothership.curator` | `CuratorPass`: weekly build_next proposal queue |
| `mothership.api` | Callable surface over pills, companions, addresses, and rules |
| `tools/atom_to_pill.py` | JSON-LD atom -> YAML pill converter |
| `tools/publish_companion.py` | CKG companion -> `mothership/companions/` publisher |

## Design principles

- UUIDs are minted once and immutable.
- Identities are deduplicated by `sha256(exact)`.
- Same term + different sha256 = divergence requiring human review.
- Address resolution never silently retargets.
- The mothership never writes back to paper directories.

## Curator Pass

```python
from pathlib import Path
from mothership.curator import CuratorPass
from mothership.identity_store import IdentityStore

curator = CuratorPass(
    pills_dir=Path("mothership/pills"),
    address_maps_dir=Path("tests/sample_data"),
    identity_store=IdentityStore(),
    bodies_dir=Path("tests/sample_data/bodies"),
)
build_next = curator.run()
```

The curator emits a ranked list of proposals (`diverge` > `test` > `extract` >
`define` > `link` > `cover` > `meta`).  Every proposal has `status: proposed`
and a versioned receipt.  See `specs/CURATOR_PASS_v1.0.md` for the full spec.

## Atom-to-Pill Converter

Convert the repo's JSON-LD atoms into YAML pills:

```bash
python mothership/tools/atom_to_pill.py
# or specify directories:
python mothership/tools/atom_to_pill.py --input-dir . --output-dir mothership/pills
```

Output is written to `mothership/pills/` preserving the input directory
structure, with `.pill.yaml` extension.

## Companion Publisher

Publish a CKG-style companion Markdown file into `mothership/companions/`:

```bash
cd mothership
python -m tools.publish_companion /path/to/companion.md
# or specify an output directory:
python -m tools.publish_companion /path/to/companion.md --output-dir companions
```

The publisher validates the front matter, mints missing paper/claim UUIDs,
normalizes the filename, writes the companion, and updates
`companions/index.json` atomically.  The input file is never modified.

See `specs/CKG_COMPANION_v1.0.md` for the full format spec.

## Mothership API

The API layer turns every pill and companion into a callable handle:

```python
from mothership.api import MothershipAPI

api = MothershipAPI()

# fetch a face or a full pill
api.list_pills()
api.get_pill("fabe6192-d3e1-503e-9c00-f286a16deeed")

# fetch a published companion
api.list_companions()
api.get_companion("16166191")

# resolve a universal address against a document
api.resolve_address(address_dict, document_text)

# ask the curator what to run next
api.curator_build_next()

# run the canon engine on a pill
api.canon_evaluate(pill)
```

CLI shortcuts:

```bash
cd mothership
python -m mothership.api status
python -m mothership.api list-pills
python -m mothership.api get-pill <uuid>
python -m mothership.api curator
```

## Specs

- `specs/CURATOR_PASS_v1.0.md`
- `specs/CKG_COMPANION_v1.0.md`
- `specs/BASELINE_GOLDENS_v1.0.md`

## Tests

`tests/test_mothership.py` covers deduplication, divergence detection, the full
resolution waterfall, canon rule pass/fail, the delta fast path, and end-to-end
scanning with sample data.

`tests/test_curator.py` covers each curator proposal type and the read-only
proposal guards.

`tests/test_atom_to_pill.py` covers face extraction, UUID minting, and YAML
output.

`tests/test_publish_companion.py` covers front-matter parsing, validation,
UUID minting, filename normalization, index updates, and rejection of invalid
companions.
