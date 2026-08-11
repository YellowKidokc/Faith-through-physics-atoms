import json
import tempfile
import unittest
from pathlib import Path

import atlas_resolution as ar


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


class AtlasResolutionTests(unittest.TestCase):
    def test_single_relation_renders_forward_and_inverse_views(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root / "claims" / "old.jsonld", {
                "nodeType": "claim", "claimID": "A003-17", "name": "Old claim", "status": "open",
                "paperState": {"paperID": "P003", "statusAtPublication": "open"},
            })
            write_json(root / "claims" / "new.jsonld", {
                "nodeType": "claim", "claimID": "A073-09", "name": "New claim", "status": "verified",
            })
            (root / "_atlas").mkdir()
            (root / "_atlas" / "relations.jsonl").write_text(
                json.dumps({"sourceAtom": "A073-09", "targetAtom": "A003-17", "relation": "resolves", "status": "accepted"}) + "\n",
                encoding="utf-8",
            )
            (root / "_atlas" / "open-items.jsonl").write_text("", encoding="utf-8")

            atlas = ar.build_atlas(root)
            old_html = ar.render_resolution_section("A003-17", atlas.atoms["A003-17"], atlas)
            new_html = ar.render_resolution_section("A073-09", atlas.atoms["A073-09"], atlas)

            self.assertIn("resolved by: A073-09", old_html)
            self.assertIn("resolves: A003-17", new_html)
            self.assertIn("Status then:</strong> open", old_html)

    def test_component_coverage_prevents_false_full_resolution(self):
        item = {
            "issue_id": "OI-0042",
            "components": [
                {"component_id": "a", "question": "A", "status": "resolved"},
                {"component_id": "b", "question": "B", "status": "resolved"},
                {"component_id": "c", "question": "C", "status": "open"},
            ],
        }
        coverage = ar.component_coverage(item)
        self.assertEqual({"resolved": 2, "total": 3, "status": "partially_resolved"}, {k: coverage[k] for k in ("resolved", "total", "status")})


if __name__ == "__main__":
    unittest.main()
