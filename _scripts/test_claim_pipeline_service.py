import importlib.util
import tempfile
import unittest
import json
from pathlib import Path

MODULE = Path(__file__).with_name("claim_pipeline_service.py")
spec = importlib.util.spec_from_file_location("claim_pipeline_service", MODULE)
service = importlib.util.module_from_spec(spec); spec.loader.exec_module(service)

CONTROLS = Path(__file__).with_name("candidate_review_controls.py")
controls_spec = importlib.util.spec_from_file_location("candidate_review_controls", CONTROLS)
controls = importlib.util.module_from_spec(controls_spec); controls_spec.loader.exec_module(controls)


class ClaimPipelineTests(unittest.TestCase):
    def capsule(self):
        return {"operation":"new_claim","claim":"A separation can be made.","plain_language":"A distinction is possible.","claim_type":"universal","defeat_condition":"A coherent denial that makes no distinction.","present_evidence":[],"open_items":["Whether a performer is co-primitive."],"canonical_promotion_requested":False}

    def test_mock_runs_all_three_stages_without_promotion(self):
        old = service.RUNS
        with tempfile.TemporaryDirectory() as tmp:
            service.RUNS = Path(tmp)
            receipt = service.review(self.capsule(), "mock", "mock-deterministic")
            self.assertEqual(receipt["final_status"], "PASS")
            self.assertEqual(len(receipt["stages"]), 3)
            self.assertFalse(receipt["canonical_promotion_performed"])
            self.assertTrue(Path(receipt["receipt_path"]).is_file())
        service.RUNS = old

    def test_promotion_request_is_rejected(self):
        capsule = self.capsule(); capsule["canonical_promotion_requested"] = True
        with self.assertRaisesRegex(ValueError, "never accepts canonical promotion"):
            service.review(capsule, "mock", "mock")

    def test_stage_two_cannot_run_after_incomplete_discovery(self):
        original = service.mock_discovery
        service.mock_discovery = lambda capsule: {**original(capsule), "status":"DISCOVERY_INCOMPLETE"}
        old = service.RUNS
        with tempfile.TemporaryDirectory() as tmp:
            service.RUNS = Path(tmp)
            receipt = service.review(self.capsule(), "mock", "mock")
            self.assertEqual(len(receipt["stages"]), 1)
            self.assertEqual(receipt["final_status"], "BLOCKED")
        service.RUNS = old; service.mock_discovery = original

    def test_contradictory_candidate_status_is_rejected(self):
        packet = {"status":controls.STATUS,"id":"X","lifecycle":"candidate","canonical_admission":True,"admission_event":None,"review_card":{},"kimi_review":{}}
        self.assertIn("candidate/admission state is contradictory", controls.validate_packet(packet))

    def test_incomplete_record_cannot_look_canonical(self):
        packet = {"status":controls.STATUS,"id":"X","lifecycle":"candidate","canonical_admission":False,"admission_event":None,"review_card":{},"kimi_review":{}}
        self.assertIn("review card is incomplete", controls.validate_packet(packet))

    def test_candidate_approval_is_not_admission(self):
        self.assertNotIn("ADMIT", controls.DECISIONS)
        self.assertTrue(controls.validate_admission_event({}))

    def test_kimi_source_is_immutable_through_intake_and_ruling(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "kimi.txt"; source.write_text("Exact criticism.", encoding="utf-8")
            receipt = controls.import_kimi(root, source)
            preserved = Path(receipt["preserved_path"])
            before = preserved.read_bytes()
            ledger = json.loads(Path(receipt["ledger_path"]).read_text(encoding="utf-8"))
            ledger["objections"][0]["david_ruling"] = {"decision":"HOLD OPEN"}
            Path(receipt["ledger_path"]).write_text(json.dumps(ledger), encoding="utf-8")
            self.assertEqual(before, preserved.read_bytes())
            self.assertEqual(controls.digest(before), receipt["source_sha256"])

    def test_receipt_stage_hash_chain_is_recomputable(self):
        old = service.RUNS
        with tempfile.TemporaryDirectory() as tmp:
            service.RUNS = Path(tmp); receipt = service.review(self.capsule(), "mock", "mock")
            for stage in receipt["stages"]:
                self.assertEqual(stage["hash"], service.sha(stage["output"]))
            self.assertEqual(receipt["stages"][1]["output"]["discovery_receipt_hash"], receipt["stages"][0]["hash"])
            self.assertEqual(receipt["stages"][2]["output"]["classification_receipt_hash"], receipt["stages"][1]["hash"])
        service.RUNS = old

    def test_source_governance_blocks_silent_warrant_upgrade(self):
        capsule = self.capsule()
        capsule["source_governance"] = {
            "allowed_claim_species": ["FRAMEWORK_STANCE"],
            "allowed_warrant_classes": ["PHILOSOPHICAL"],
            "bridge_permitted": False,
        }
        classification = {
            "status": "CLASSIFICATION_COMPLETE",
            "claim_species": "METAPHYSICAL_NECESSITY",
            "warrant_class": "FORMAL",
            "unresolved": [],
        }
        guarded = service.apply_source_governance_guard(capsule, classification)
        self.assertEqual(guarded["status"], "RETURN_TO_DISCOVERY")
        self.assertIn("SOURCE_GOVERNANCE_BLOCK", guarded["new_fact_exception"])

    def test_source_governance_blocks_invented_bridge(self):
        capsule = self.capsule()
        capsule["source_governance"] = {"bridge_permitted": False}
        reconciliation = {
            "status": "RECONCILIATION_COMPLETE",
            "publication_eligibility": "ELIGIBLE_FOR_HUMAN_REVIEW",
            "bridge_statement": "An invented bridge.",
            "downstream_effects": [],
        }
        guarded = service.apply_bridge_guard(capsule, reconciliation)
        self.assertEqual(guarded["status"], "RETURN_TO_CLASSIFICATION")
        self.assertEqual(guarded["publication_eligibility"], "NOT_ELIGIBLE")


if __name__ == "__main__": unittest.main()
