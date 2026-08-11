import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import page_aggregate as pa


class PageAggregateTests(unittest.TestCase):
    def test_aggregation_is_independent_from_extraction_and_includes_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "_atlas").mkdir()
            (root / "_ledger").mkdir()
            (root / "_runtime").mkdir()
            (root / "_atlas" / "view-definitions.json").write_text(json.dumps({
                "version": "test",
                "maps": {
                    "meeting_map": {"question": "Does evidence meet prediction?", "include_edges": ["meeting"], "layout": "two_column"},
                    "coverage_map": {"question": "What is missing?", "include_edges": ["supports"], "layout": "grid"},
                },
            }), encoding="utf-8")
            (root / "_atlas" / "open-items.jsonl").write_text("", encoding="utf-8")
            (root / "_atlas" / "relations.jsonl").write_text("", encoding="utf-8")
            (root / "_atlas" / "evidence-coverage.jsonl").write_text(
                json.dumps({"evidence_id": "E1", "claim_id": "C1", "coverage": 1, "supports": []}) + "\n",
                encoding="utf-8",
            )
            (root / "_atlas" / "projections.jsonl").write_text(
                json.dumps({"projection_id": "M1", "claim_id": "C1", "mode": "meeting", "title": "M", "result": "contradicted"}) + "\n",
                encoding="utf-8",
            )
            (root / "_ledger" / "LANE4_GLOBAL_CLAIM_LEDGER.jsonl").write_text(
                json.dumps({"atom_id": "L1", "proof_label": "PYTHON_RUNTIME_SUPPORTED", "current_status": "active_candidate"}) + "\n",
                encoding="utf-8",
            )
            source = root / "page.html"
            source.write_text("<html>C1</html>", encoding="utf-8")

            with patch.object(pa, "REPO", root):
                result = pa.aggregate_page(source, root)
            self.assertEqual("CONTRADICTED", next(m["status"] for m in result["maps"] if m["map_id"] == "meeting_map"))
            self.assertTrue(any(r["receipt_type"] == "lane4" for r in result["receipts"]))
            self.assertTrue(any(r["receipt_type"] == "python" for r in result["receipts"]))
            self.assertTrue(any(r["receipt_type"] == "colab" for r in result["receipts"]))


if __name__ == "__main__":
    unittest.main()
