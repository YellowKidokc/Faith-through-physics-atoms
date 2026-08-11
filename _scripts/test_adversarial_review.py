import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import adversarial_review as ar
import math_translation as mt


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


class MathTranslationTests(unittest.TestCase):
    CLAIM = {"claimID": "tp:test/C1", "name": "Test", "domainType": "mathematics",
             "mathematicalForm": "J = T_A/D, M = 1 - T_B/D"}

    def test_word_equation_preserves_structure(self):
        result = mt.translate(self.CLAIM, supplied_glossary={"J": "justice", "T_A": "paid cost",
                                                             "D": "damage", "M": "mercy", "T_B": "owed cost"})
        self.assertEqual("justice equals paid cost per damage, mercy equals 1 minus owed cost per damage",
                         result["wordEquation"])
        self.assertEqual("$$\nJ = T_A/D, M = 1 - T_B/D\n$$", result["equationMarkdown"])

    def test_generated_node_is_proposed_and_unreviewed(self):
        result = mt.translate(self.CLAIM)
        node = mt.build_node(self.CLAIM, result, "local", "")
        self.assertEqual("translation", node["nodeType"])
        self.assertEqual("proposed", node["status"])
        self.assertEqual("unreviewed", node["generationReceipt"]["reviewStatus"])
        self.assertEqual("dependsOn", node["edges"][0]["type"])

    def test_translation_requires_equation(self):
        with self.assertRaisesRegex(ValueError, "no mathematicalForm"):
            mt.translate({"claimID": "empty"})


if __name__ == "__main__":
    unittest.main()
