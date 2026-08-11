import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fis_folder_beacon_patch import load_patches, patch_beacons
from fis_folder_beacon_scan import scan
from folder_beacon import BeaconError, dump_front_matter, parse_front_matter


BEACON = """---
fis_schema: "folder-beacon.v2"
folder_id: "FLD-1"
folder: "site\\\\bgl"
name: "bgl"
short_name: "BGL"
folder_class: "page_series"
status: "active"
contains: ["article_html"]
provides: ["html_pages"]
needs: ["audio_assets"]
looking_for: ["audio matching BGL"]
search_tokens: ["bgl", "loser"]
allowed_actions: ["index"]
forbidden_actions: ["delete"]
batch_tags: ["site-data", "page-series"]
---
# Notes

Keep this body exactly.
"""


class FolderBeaconTests(unittest.TestCase):
    def test_round_trip_preserves_markdown_body(self):
        data, body = parse_front_matter(BEACON)
        rendered = dump_front_matter(data, body)
        self.assertEqual(body, parse_front_matter(rendered)[1])

    def test_rejects_front_matter_that_is_not_at_top(self):
        with self.assertRaises(BeaconError):
            parse_front_matter("intro\n" + BEACON)

    def test_scanner_indexes_only_valid_beacons(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "ok").mkdir()
            (root / "bad").mkdir()
            (root / "ok" / ".fisnote").write_text(BEACON, encoding="utf-8")
            (root / "bad" / ".fisnote").write_text("---\nfis_schema: old\n---\n", encoding="utf-8")
            result = scan([root])
            self.assertEqual(1, len(result["folders"]))
            self.assertEqual(1, len(result["errors"]))
            self.assertEqual("BGL", result["folders"][0]["short_name"])

    def test_batch_patch_selects_and_preserves_body(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".fisnote"
            path.write_text(BEACON, encoding="utf-8")
            patches = [
                {"op": "add_unique", "selector": {"batch_tags": ["site-data"]}, "field": "allowed_actions", "value": "beaker_scan"},
                {"op": "set", "selector": {"folder_class": "asset_audio"}, "field": "short_name", "value": "NO"},
            ]
            report = patch_beacons([Path(directory)], patches)
            self.assertEqual(1, len(report["changed"]))
            data, body = parse_front_matter(path.read_text(encoding="utf-8"))
            self.assertIn("beaker_scan", data["allowed_actions"])
            self.assertEqual("BGL", data["short_name"])
            self.assertEqual(parse_front_matter(BEACON)[1], body)

    def test_dry_run_reports_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".fisnote"
            path.write_text(BEACON, encoding="utf-8")
            report = patch_beacons([Path(directory)], [{"op": "append_tag", "selector": {}, "value": "new"}], True)
            self.assertEqual(1, len(report["changed"]))
            self.assertEqual(BEACON, path.read_text(encoding="utf-8"))

    def test_patch_file_requires_explicit_selector(self):
        with tempfile.TemporaryDirectory() as directory:
            patch_file = Path(directory) / "patches.jsonl"
            patch_file.write_text(json.dumps({"op": "append_tag", "value": "new"}) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires an explicit selector"):
                load_patches(patch_file)

    def test_explicit_empty_selector_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            patch_file = Path(directory) / "patches.jsonl"
            patch = {"op": "append_tag", "selector": {}, "value": "new"}
            patch_file.write_text(json.dumps(patch) + "\n", encoding="utf-8")
            self.assertEqual([patch], load_patches(patch_file))

    def test_programmatic_patch_requires_explicit_selector(self):
        with self.assertRaisesRegex(ValueError, "requires an explicit selector"):
            patch_beacons([], [{"op": "append_tag", "value": "new"}])


if __name__ == "__main__":
    unittest.main()
