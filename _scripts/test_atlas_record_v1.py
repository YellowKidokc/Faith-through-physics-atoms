import unittest

from _scripts.build_atlas_record_v1 import DEFAULT_ATOM, build_record


class AtlasRecordV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = build_record(DEFAULT_ATOM)

    def test_periodic_bridge_marker_contains_admitted_targets_only(self) -> None:
        self.assertEqual(
            self.record["periodic15"]["marker_4_bridged_domains"],
            ["tp:bridges/master-equation/economics/trilemma-cost-bearing"],
        )
        standings = {bridge["target"]: bridge["standing"] for bridge in self.record["bridges"]}
        self.assertEqual(standings["tp:theology/01/001"], "Candidate")

    def test_unknown_native_grade_is_not_fabricated(self) -> None:
        self.assertEqual(self.record["periodic15"]["marker_10_native_grade"], "NOT_ESTABLISHED")
        self.assertEqual(self.record["periodic15"]["marker_12_evidence_grade"], "UNKNOWN")
        projection = self.record["computed"]["grade_projection"]
        self.assertEqual(projection["status"], "UNKNOWN")

    def test_exact_source_components_are_addressable(self) -> None:
        component_ids = {
            component["component_id"]
            for component in self.record["atom_stack"]["components"]
            if component["type"] == "claim_component"
        }
        self.assertEqual(
            component_ids,
            {
                "tp:ME/L5/C1.algebraic-trilemma",
                "tp:ME/L5/C1.external-cost-bearer",
                "tp:ME/L5/C1.historical-instantiation",
            },
        )

    def test_claim_mode_and_source_hash_are_preserved(self) -> None:
        self.assertEqual(self.record["atom_stack"]["claims"][0]["mode"], "FORMAL_DERIVATION")
        self.assertEqual(self.record["atom_stack"]["claims"][0]["mode_native"], "formal_derivation")
        self.assertRegex(self.record["source"]["content_hash"], r"^sha256:[0-9a-f]{64}$")

    def test_reality_mirror_is_not_periodic_marker_16(self) -> None:
        self.assertNotIn("reality_mirror", self.record["periodic15"])
        self.assertEqual(self.record["reality_mirror"]["class"], "F")

    def test_atom_stack_is_the_local_canonical_unit(self) -> None:
        stack = self.record["atom_stack"]
        self.assertEqual(stack["atom"]["atom_id"], self.record["id"]["atom_id"])
        self.assertEqual(stack["dependencies"], stack["upstream"])
        self.assertTrue(stack["warrant"]["evidence_receipt_ids"])


if __name__ == "__main__":
    unittest.main()
