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

    def test_evidence_coverage_separates_strength_from_silence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root / "claims" / "claim.jsonld", {
                "nodeType": "claim",
                "claimID": "C1",
                "name": "Grace claim",
                "claimComponents": [
                    {"componentID": "C1.a", "predicate": "external"},
                    {"componentID": "C1.b", "predicate": "restoring"},
                    {"componentID": "C1.c", "predicate": "noncoercive"},
                ],
            })
            (root / "_atlas").mkdir()
            (root / "_atlas" / "open-items.jsonl").write_text("", encoding="utf-8")
            (root / "_atlas" / "relations.jsonl").write_text("", encoding="utf-8")
            (root / "_atlas" / "evidence-coverage.jsonl").write_text(
                json.dumps({
                    "evidence_id": "E7",
                    "claim_id": "C1",
                    "coverage": 0.67,
                    "supports": [
                        {"claim_component": "C1.a", "relation": "supports", "strength": "strong"},
                        {"claim_component": "C1.b", "relation": "supports", "strength": "moderate"},
                    ],
                    "unaddressed": ["C1.c"],
                }) + "\n",
                encoding="utf-8",
            )

            atlas = ar.build_atlas(root)
            html = ar.render_evidence_coverage("C1", atlas.atoms["C1"], atlas)
            self.assertIn("E7: supports (strong, coverage 0.67)", html)
            self.assertIn("E7: supports (moderate, coverage 0.67)", html)
            self.assertIn("UNSUPPORTED COMPONENT - no admitted evidence", html)
            self.assertIn("Evidence strength is not evidence coverage", html)

    def test_projection_renders_ascendant_descendant_and_meeting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root / "claims" / "claim.jsonld", {"nodeType": "claim", "claimID": "C1", "name": "Claim"})
            (root / "_atlas").mkdir()
            (root / "_atlas" / "open-items.jsonl").write_text("", encoding="utf-8")
            (root / "_atlas" / "relations.jsonl").write_text("", encoding="utf-8")
            (root / "_atlas" / "evidence-coverage.jsonl").write_text("", encoding="utf-8")
            rows = [
                {"projection_id": "A1", "claim_id": "C1", "mode": "ascendant", "title": "A", "result": "supported", "path": [{"id": "E1"}, {"id": "C1"}]},
                {"projection_id": "D1", "claim_id": "C1", "mode": "descendant", "title": "D", "result": "partial", "reference": "R", "predictions": [{"prediction_id": "P1", "text": "x", "test": "T1", "result": "found"}]},
                {"projection_id": "M1", "claim_id": "C1", "mode": "meeting", "title": "M", "result": "converged", "local_cell": "I1", "ascent": "yes", "descent": "yes"},
            ]
            (root / "_atlas" / "projections.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
            atlas = ar.build_atlas(root)
            html = ar.render_projections("C1", atlas)
            self.assertIn("Ascendant - A", html)
            self.assertIn("Descendant - D", html)
            self.assertIn("Meeting - M", html)
            self.assertIn("Source -> Atomization", html)

    def test_equal_strength_conflict_marks_current_status_disputed(self):
        atlas = ar.Atlas(backward={"C1": [
            {"sourceAtom": "A", "targetAtom": "C1", "relation": "supports", "warrant_strength": "strong"},
            {"sourceAtom": "B", "targetAtom": "C1", "relation": "contradicts", "warrant_strength": "strong"},
        ]})
        self.assertEqual("disputed", ar.current_status("C1", {"status": "active"}, atlas))


if __name__ == "__main__":
    unittest.main()
