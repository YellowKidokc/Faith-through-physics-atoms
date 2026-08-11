import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import adversarial_review as ar
import definition_resolver as dr


class ResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.atoms = dr.load_registry()

    def test_exact_marker_is_high_confidence_proposal(self):
        matches = dr.resolve_text("Use [[def:terminus-sui]].", self.atoms)
        self.assertEqual(("explicit-marker", .99, "proposed"), (matches[0].method, matches[0].confidence, matches[0].status))

    def test_alias_matches_at_word_boundaries(self):
        matches = dr.resolve_text("It is an end in itself.", self.atoms)
        self.assertTrue(any(m.definition_id == "tp:def:terminus-sui" and m.method == "alias" for m in matches))

    def test_ambiguous_single_letter_symbol_is_unresolved(self):
        matches = dr.resolve_text("G = m/r", self.atoms)
        grace = next(m for m in matches if m.definition_id == "tp:def:master-equation/grace")
        self.assertEqual("unresolved", grace.status)

    def test_missing_citation_is_validation_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "_definitions/atoms").mkdir(parents=True)
            atom = json.loads(json.dumps(self.atoms["tp:def:terminus-sui"]))
            atom["source"]["exactShortQuotation"] = ""; atom["source"]["authoritativeSourceURL"] = ""
            (root / "_definitions/atoms/x.jsonld").write_text(json.dumps(atom))
            registry = {"definitions": [{"permanentDefinitionID": atom["permanentDefinitionID"], "atom": "atoms/x.jsonld", "canonicalStatus": atom["canonicalStatus"]}]}
            (root / "_definitions/registry.jsonld").write_text(json.dumps(registry))
            self.assertTrue(any("required citation" in e for e in dr.validate(root)))

    def test_definition_proposal_stays_awaiting_human(self):
        row = {"proposalID": "d1", "sourceAtom": "paper.md", "targetAtom": "tp:def:terminus-sui", "status": "proposed"}
        with tempfile.TemporaryDirectory() as tmp:
            definitions, claims, reviews = Path(tmp)/"d.jsonl", Path(tmp)/"c.jsonl", Path(tmp)/"r.jsonl"
            definitions.write_text(json.dumps(row) + "\n"); claims.write_text("")
            with patch.object(ar, "PROPOSALS", claims), patch.object(ar, "DEFINITION_PROPOSALS", definitions), patch.object(ar, "REVIEWS", reviews), patch.object(ar, "atoms_by_id", return_value={}):
                receipt = ar.run_reviews(proposal_id="d1")[0]
            self.assertEqual("awaiting_human", receipt["gateStatus"])
            self.assertEqual("proposed", row["status"])

    def test_render_inherits_citation_only_from_human_accepted_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_definitions").mkdir()
            (root / "_proposals").mkdir()
            source = root / "paper.md"
            source.write_text("Master Equation grace", encoding="utf-8")
            # Reuse the registry tree without changing what render loads.
            with patch.object(dr, "load_registry", return_value=({}, self.atoms)):
                dr.render(source, root / "unaccepted.html", root)
                self.assertNotIn("<li", (root / "unaccepted.html").read_text())

                row = {"sourceAtom": "paper.md", "targetAtom": "tp:def:master-equation/grace",
                       "status": "accepted", "validationReceipt": {
                           "acceptedBy": "human-reviewer", "acceptedAt": "2026-08-11T00:00:00Z",
                           "adversarialGateStatus": "awaiting_human"}}
                (root / "_proposals/definition-links.jsonl").write_text(json.dumps(row) + "\n")
                dr.render(source, root / "accepted.html", root)
                self.assertIn("Grace (Master Equation)", (root / "accepted.html").read_text())


if __name__ == "__main__": unittest.main()
