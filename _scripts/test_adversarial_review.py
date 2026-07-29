import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import adversarial_review as ar


class ReviewTests(unittest.TestCase):
    def test_local_review_fails_closed_when_no_contradiction(self):
        result = ar.local_review({"matchReason": "shared axiom"}, {"status": "verified"}, {})
        self.assertEqual("uncertain", result["verdict"])

    def test_local_review_blocks_falsified_material(self):
        result = ar.local_review({}, {"status": "falsified"}, {})
        self.assertEqual("oppose", result["verdict"])

    def test_run_writes_blocking_receipt_without_accepting(self):
        proposal = {"proposalID": "p1", "sourceAtom": "s", "targetAtom": "t", "status": "proposed"}
        with tempfile.TemporaryDirectory() as directory:
            proposals, definitions, reviews = Path(directory) / "p.jsonl", Path(directory) / "d.jsonl", Path(directory) / "r.jsonl"
            proposals.write_text(json.dumps(proposal) + "\n")
            definitions.write_text("")
            with patch.object(ar, "PROPOSALS", proposals), patch.object(ar, "REVIEWS", reviews), \
                 patch.object(ar, "DEFINITION_PROPOSALS", definitions), \
                 patch.object(ar, "atoms_by_id", return_value={"s": {"status": "falsified"}, "t": {}}):
                receipt = ar.run_reviews()[0]
            self.assertEqual("blocked", receipt["gateStatus"])
            self.assertEqual("proposed", proposal["status"])
            self.assertEqual("blocked", json.loads(reviews.read_text())["gateStatus"])


if __name__ == "__main__":
    unittest.main()
