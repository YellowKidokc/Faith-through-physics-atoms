import copy
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE=Path(__file__).with_name("canonical_language_layer.py"); spec=importlib.util.spec_from_file_location("canonical_language_layer",MODULE); layer=importlib.util.module_from_spec(spec); spec.loader.exec_module(layer)

class CanonicalLanguageTests(unittest.TestCase):
    def definition(self,version="1.0.0",supersedes=None):
        return {"definition_id":"DEF-DISTINCTION","canonical_term":"Distinction","version":version,"exact_definition":"A is not B in a stated respect.","aliases":[],"forbidden_equivalences":[],"scope":[],"dependencies":[],"source_hashes":[],"supersedes":supersedes}

    def test_admitted_version_cannot_be_overwritten(self):
        reg=layer.empty_registry("DEFINITION_REGISTRY"); reg["admitted_objects"]["DEF-DISTINCTION@1.0.0"]={}; reg["active_versions"]["DEF-DISTINCTION"]="1.0.0"
        with self.assertRaisesRegex(ValueError,"immutable"): layer.propose_revision(reg,self.definition())

    def test_definition_change_creates_new_version_without_pointer_change(self):
        reg=layer.empty_registry("DEFINITION_REGISTRY"); reg["admitted_objects"]["DEF-DISTINCTION@1.0.0"]={}; reg["active_versions"]["DEF-DISTINCTION"]="1.0.0"
        out=layer.propose_revision(reg,self.definition("1.1.0","DEF-DISTINCTION@1.0.0")); self.assertEqual(out["active_versions"]["DEF-DISTINCTION"],"1.0.0"); self.assertEqual(out["proposed_objects"][0]["version"],"1.1.0")

    def test_incompatible_symbol_reuse_fails_resolution(self):
        old={"symbol_id":"SYM-X1","version":"1.0.0","glyph":"χ","meaning":"field","type_signature":"M→R","domain":"M","codomain":"R","units":"1"}; new={"symbol_id":"SYM-X2","version":"0.1.0","glyph":"χ","meaning":"God","type_signature":"Person","domain":"theology","codomain":"theology","units":None}
        self.assertEqual(layer.detect_symbol_conflicts(new,[old])[0]["kind"],"INCOMPATIBLE_SYMBOL_REUSE")

    def test_missing_type_information_remains_open(self):
        result=layer.detect_symbol_conflicts({"symbol_id":"S","glyph":"x","meaning":"value"},[]); self.assertEqual(result[0]["kind"],"OPEN_MISSING_TYPE_INFORMATION")

    def test_conditional_theorem_does_not_prove_premises(self):
        truth=layer.build_truth_kernel({"claim":"Q follows from P.","claim_type":"mathematical","premise_set":["P"]},{"register":"mathematics","why_outcome":"WHY_OPEN"},[],[]); self.assertIn("PREMISES NOT PROVED",truth["entailment_status"])

    def test_a0_cannot_receive_lean_proved_status(self):
        truth=layer.build_truth_kernel({"claim":"The Triune God is.","source_object_id":"A0","formal_receipts":["lean-pass"]},{"register":"theology","why_outcome":"WHY_OPEN"},[],[]); self.assertEqual(truth["truth_mode"],"DECLARED"); self.assertIn("NOT LEAN-PROVED",truth["entailment_status"])

    def test_bridge_never_transfers_proof(self):
        result=layer.analyze_candidate({"claim":"Formal X = theological Y","source_object_id":"B"},{"register":"bridge","why_outcome":"WHY_OPEN"}); self.assertFalse(result["bridge_analysis"]["propagates_proof"]); self.assertTrue(result["bridge_analysis"]["violations"])

    def test_changed_dependency_flags_downstream(self):
        objects=[{"id":"B","dependencies":["A"]},{"id":"C","dependencies":["B"]}]; impact=layer.dependency_impact("A",objects); self.assertEqual(impact["all_downstream"],["B","C"]); self.assertFalse(impact["automatic_source_rewrite"])

    def test_historical_source_unchanged_by_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"paper.md"; path.write_text("Original historical source.",encoding="utf-8"); before=hashlib.sha256(path.read_bytes()).hexdigest(); layer.analyze_candidate({"claim":"A claim","source_object_id":"X"},{"register":"history","why_outcome":"WHY_OPEN"}); self.assertEqual(before,hashlib.sha256(path.read_bytes()).hexdigest())

    def test_projection_can_be_stale_without_source_change(self):
        record=layer.projection_record("P",[{"id":"A","version":"1.0.0","source_hash":"sha256:x"}],{"D":"1"},"g1",["changed dependency"]); self.assertEqual(record["currency"],"STALE"); self.assertFalse(record["independent_source_of_truth"])

    def test_countermodels_are_preserved_in_truth_kernel(self):
        truth=layer.build_truth_kernel({"claim":"Love forces three.","countermodels":["two-person mutual-love model"],"what_survives_countermodels":["other-directed love requires distinction"]},{"register":"mathematics","why_outcome":"WHY_OPEN"},[],[])
        self.assertEqual(truth["countermodels"],["two-person mutual-love model"]); self.assertEqual(truth["what_survives_countermodels"],["other-directed love requires distinction"])

    def test_candidate_approval_cannot_admit(self):
        reg=layer.propose_revision(layer.empty_registry("DEFINITION_REGISTRY"),self.definition()); self.assertFalse(reg["active_versions"]); self.assertFalse(reg["admitted_objects"])

    def test_only_signed_event_changes_active_pointer(self):
        base=layer.empty_registry("DEFINITION_REGISTRY"); record=self.definition(); proposed=layer.propose_revision(base,record)
        with self.assertRaisesRegex(ValueError,"signed admission"): layer.apply_signed_admission(proposed,proposed["proposed_objects"][0],{})
        candidate=proposed["proposed_objects"][0]; event={"event_type":"SIGNED_HUMAN_ADMISSION","actor":"David","date":"2026-08-29","rationale":"test","source_hashes":[],"candidate_hash":candidate["candidate_hash"],"unresolved_fields":[],"downstream_impact":[],"signed_admission_receipt":"signature:test","registry_id":"DEFINITION_REGISTRY","object_id":"DEF-DISTINCTION","version":"1.0.0"}; admitted=layer.apply_signed_admission(proposed,candidate,event); self.assertEqual(admitted["active_versions"]["DEF-DISTINCTION"],"1.0.0")

if __name__=="__main__": unittest.main()
