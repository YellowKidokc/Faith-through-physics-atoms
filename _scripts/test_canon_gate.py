import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import canon_gate as cg


class CanonGateTests(unittest.TestCase):
    def test_sidecar_is_default_and_promotion_requires_flag(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "paper.md"
            source.write_text("# Paper\n\nClaim text.", encoding="utf-8")
            with patch.object(cg, "REPO", root), patch.object(cg, "SIDECARS", root / "_atlas" / "canon-sidecars"), patch.object(cg, "CANON", root / "_canon"), patch.object(cg, "REGISTRY", root / "_atlas" / "canonical-publications.jsonl"):
                record = cg.build_record(source, "PAPER-001-v1")
                sidecar = cg.write_sidecar(record)
                self.assertTrue(sidecar.exists())
                self.assertFalse((root / "_canon").exists())
                data = json.loads(sidecar.read_text(encoding="utf-8"))
                self.assertEqual("sidecar", data["publication_snapshot"]["canonGate"]["status"])
                self.assertIn("atlas_projection", data)

    def test_accept_canon_writes_frozen_html_json_and_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "paper.md"
            source.write_text("# Paper\n\nClaim text.", encoding="utf-8")
            with patch.object(cg, "REPO", root), patch.object(cg, "SIDECARS", root / "_atlas" / "canon-sidecars"), patch.object(cg, "CANON", root / "_canon"), patch.object(cg, "REGISTRY", root / "_atlas" / "canonical-publications.jsonl"):
                html_path, json_path = cg.promote(source, cg.build_record(source, "PAPER-001-v1"))
                self.assertTrue(html_path.exists())
                self.assertTrue(json_path.exists())
                self.assertIn("promoted", cg.REGISTRY.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
