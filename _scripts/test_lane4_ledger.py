import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lane4_ledger as ledger


class Lane4LedgerTests(unittest.TestCase):
    def test_identity_is_deterministic_and_semantic(self):
        data = {"title": "Wrapper Zero Veto", "claim": "C_W is an operator.", "domain": "master-equation", "lane": "Lean4", "assumptions": ["C_W is defined."]}
        first = ledger.normalize_atom(data)
        second = ledger.normalize_atom(data)
        self.assertEqual(first["atom_id"], "tp:lane4/master-equation/wrapper-zero-veto")
        self.assertEqual(first["atom_uid"], second["atom_uid"])

    def test_old_master_equation_is_rerun_owed(self):
        atom = ledger.normalize_atom({"title": "Old Master Equation result", "claim": "A v2 output.", "domain": "master-equation", "assumptions": ["v2 inputs"]})
        self.assertEqual(atom["rerun_status"], "RERUN_OWED")
        self.assertEqual(atom["proof_label"], "RERUN_OWED")

    def test_event_is_append_only_and_deduplicated(self):
        atom = ledger.normalize_atom({"title": "A", "claim": "B", "domain": "test", "assumptions": ["C"], "source_artifacts": ["receipt"]})
        with tempfile.TemporaryDirectory() as temp, patch.object(ledger, "ATOMS", Path(temp)):
            event = {"timestamp": "2026-07-28T00:00:00+00:00", "event_type": "test_run", "result": "pass"}
            ledger.append_event(atom, event)
            with self.assertRaises(SystemExit): ledger.append_event(atom, event)


if __name__ == "__main__":
    unittest.main()
