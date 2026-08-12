"""Drift regression tests — one per defect fixed on 2026-08-12.

These three tests pin the fixes for the three drift defects found during
the v0.5 freeze-candidate alignment review. If any of them fails, a fixed
defect has regressed. Do not weaken these tests to make them pass; fix the
data instead.

Defect 1 — grade registry drifted from the v0.5 freeze bridge
    (C3 was B/SUPPORTED, C5 was A/STRONG; freeze bridge says
    C3 = C/PROVISIONAL, C5 = B+/ESTABLISHED). Marker 12 is computed from
    this registry, so any drift here mis-grades every atom at birth.

Defect 2 — a non-canonical sixth meeting state ("converged_partial")
    appeared in _atlas/projections.jsonl. The meeting contract has exactly
    five states, enumerated in _atlas/view-definitions.json
    (meeting_map.meeting_states). That file is the single source of truth;
    this test reads the enum from there rather than duplicating it.

Defect 3 — ME-C1's statementPlain asserted as settled ("exactly one
    historical instantiation") what its own claimComponents mark open.
    Contract: any claim atom carrying an open component must carry a
    boundary marker in statementPlain — the plain rendering may not be
    more confident than the graph it renders.

Stdlib only, consistent with the repo's no-third-party-dependency policy.
Run: python -m unittest discover -s _scripts -p "test_*.py"
"""
import glob
import json
import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The v0.5 freeze-candidate grade bridge
# (unified_architecture_weave_v0.5_FREEZE_CANDIDATE.md, 2026-08-11).
FREEZE_GRADE_BRIDGE = {
    "C0": {"atlas_grade": "-", "alert_state": "SUPERSEDED"},
    "C1": {"atlas_grade": "-", "alert_state": "OPEN"},
    "C2": {"atlas_grade": "C", "alert_state": "CANDIDATE"},
    "C3": {"atlas_grade": "C", "alert_state": "PROVISIONAL"},
    "C4": {"atlas_grade": "B", "alert_state": "SUPPORTED"},
    "C5": {"atlas_grade": "B+", "alert_state": "ESTABLISHED"},
    "C6": {"atlas_grade": "A", "alert_state": "CANON"},
}

# Tokens that mark an honesty boundary in plain-language renderings.
# A statementPlain touching an open component must contain at least one.
BOUNDARY_TOKENS = (
    "open",
    "separate claim",
    "does not establish",
    "not establish",
    "not proven",
    "unproven",
    "remains",
    "not yet",
    "owed",
)


def _atom_paths():
    for path in glob.glob(os.path.join(REPO, "**", "*.jsonld"), recursive=True):
        if "_vocab" in path or "_protocol" in path:
            continue
        yield path


class DriftRegressionTests(unittest.TestCase):
    def test_grade_registry_matches_freeze_bridge(self):
        """Defect 1: _atlas/grade-registry.json must equal the v0.5 freeze
        grade bridge for every C-mode (grade letter and alert state)."""
        with open(os.path.join(REPO, "_atlas", "grade-registry.json"),
                  encoding="utf-8") as fh:
            registry = json.load(fh)
        mapping = registry["mode_to_atlas"]
        self.assertEqual(
            set(mapping), set(FREEZE_GRADE_BRIDGE),
            "grade registry C-mode keys drifted from the freeze bridge",
        )
        for mode, expected in FREEZE_GRADE_BRIDGE.items():
            self.assertEqual(
                mapping[mode]["atlas_grade"], expected["atlas_grade"],
                f"{mode} atlas_grade drifted from freeze bridge",
            )
            self.assertEqual(
                mapping[mode]["alert_state"], expected["alert_state"],
                f"{mode} alert_state drifted from freeze bridge",
            )

    def test_meeting_states_are_canonical(self):
        """Defect 2: every meeting-mode projection must use one of the five
        canonical meeting states enumerated in view-definitions.json."""
        with open(os.path.join(REPO, "_atlas", "view-definitions.json"),
                  encoding="utf-8") as fh:
            views = json.load(fh)
        canonical = set(views["maps"]["meeting_map"]["meeting_states"])
        self.assertEqual(
            canonical,
            {"CONVERGED", "PRESSURE", "PREDICTED_NOT_OBSERVED",
             "UNRESOLVED", "CONTRADICTED"},
            "meeting_states enum in view-definitions.json changed; "
            "update this test only via an architecture amendment",
        )
        path = os.path.join(REPO, "_atlas", "projections.jsonl")
        with open(path, encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                proj = json.loads(line)
                if proj.get("mode") != "meeting":
                    continue
                self.assertIn(
                    proj.get("result"), canonical,
                    f"projections.jsonl line {lineno}: meeting result "
                    f"{proj.get('result')!r} is not a canonical meeting state",
                )
                if "meeting_state" in proj:
                    self.assertIn(
                        proj["meeting_state"], canonical,
                        f"projections.jsonl line {lineno}: meeting_state "
                        f"{proj['meeting_state']!r} is not canonical",
                    )

    def test_plain_statement_honors_open_components(self):
        """Defect 3: a claim atom with any open claimComponent must carry a
        boundary marker in statementPlain, in both the .jsonld source and
        its generated .html pill if one exists."""
        checked = 0
        for path in _atom_paths():
            with open(path, encoding="utf-8") as fh:
                try:
                    atom = json.load(fh)
                except Exception:
                    continue
            components = atom.get("claimComponents") or []
            if not any(c.get("status") == "open" for c in components):
                continue
            checked += 1
            plain = (atom.get("statementPlain") or "").lower()
            self.assertTrue(
                any(token in plain for token in BOUNDARY_TOKENS),
                f"{os.path.basename(path)}: statementPlain asserts without a "
                f"boundary marker while carrying an open component",
            )
            pill = path[:-len(".jsonld")] + ".html"
            if os.path.exists(pill):
                with open(pill, encoding="utf-8") as fh:
                    pill_text = fh.read().lower()
                self.assertTrue(
                    any(token in pill_text for token in BOUNDARY_TOKENS),
                    f"{os.path.basename(pill)}: pill out of sync — no "
                    f"boundary marker while the atom carries an open component",
                )
        self.assertGreater(
            checked, 0,
            "no claim atoms with open components found; test is vacuous",
        )


if __name__ == "__main__":
    unittest.main()
