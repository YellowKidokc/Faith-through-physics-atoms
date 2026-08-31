import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE=Path(__file__).with_name("batch_ground_trial_ingestion.py")
spec=importlib.util.spec_from_file_location("batch_ground_trial_ingestion",MODULE); adapter=importlib.util.module_from_spec(spec); spec.loader.exec_module(adapter)

class BatchIngestionTests(unittest.TestCase):
    def test_ledger_preserves_quote_heading_lines_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"ledger.md"; path.write_text("# Ledger\n| ID | Claim | Class | Boundary |\n|---|---|---|---|\n| GT-C01 | Exact claim. | P | OPEN |\n",encoding="utf-8")
            row=adapter.parse_ledger(path)[0]
            self.assertEqual(row["claim"],"Exact claim."); self.assertEqual(row["source"]["heading"],"Ledger"); self.assertEqual(row["source"]["line_start"],4); self.assertEqual(row["source"]["source_hash"],adapter.file_hash(path)); self.assertEqual(row["source"]["quotation_hash"],adapter.text_hash("Exact claim."))

    def test_terse_chain_label_enters_human_split_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"chain.md"; path.write_text("# Chain\n```\nA1.1 Existence ← ∅ [AX_CORE]\nA1.3 Distinction ENABLES Information ← A1.0\n```\n",encoding="utf-8")
            rows=adapter.parse_chain(path)
            self.assertIn("discovery_incomplete_reason",rows[0]); self.assertNotIn("discovery_incomplete_reason",rows[1]); self.assertEqual(rows[0]["source"]["quotation"],"A1.1 Existence ← ∅ [AX_CORE]")

    def test_repeated_source_id_chooses_richest_occurrence_once(self):
        base={"source_object_id":"A1","source":{"source_hash":"sha256:x","quotation":"A1 Existence","line_start":1}}
        richer={"source_object_id":"A1","source":{"source_hash":"sha256:x","quotation":"A1 Existence ← ∅ [AX_CORE]","line_start":8}}
        result=adapter.unique_proposals([base,richer])
        self.assertEqual(len(result),1); self.assertEqual(result[0]["source"]["line_start"],8)

if __name__=="__main__": unittest.main()
