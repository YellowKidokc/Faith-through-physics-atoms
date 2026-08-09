import json
import tempfile
import unittest
from pathlib import Path

from canon_drift.autolink import autolink_html, autolink_markdown
from canon_drift.models import ScanResult
from canon_drift.patches import apply_safe, proposed_patches
from canon_drift.registry import Registry
from canon_drift.scanner import scan_html, scan_text


ROOT = Path(__file__).resolve().parents[3]


class CanonDriftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.registry = Registry(ROOT)

    def write(self, directory, name, text):
        path = Path(directory) / name; path.write_text(text, encoding="utf-8"); return path

    def test_at_least_ten_registered_old_variants_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            for index, retired in enumerate(self.registry.retired):
                path = self.write(tmp, f"v{index}.md", retired["pattern"] + "\n")
                findings = [f for f in scan_text(path, self.registry) if f.findingType == "retired_equation"]
                self.assertEqual(1, len(findings), retired["pattern"])
                self.assertGreaterEqual(findings[0].confidence, .95)
        self.assertGreaterEqual(len(self.registry.retired), 10)

    def test_unicode_and_latex_normalize_to_registry_form(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "symbols.md", r"$\chi = \prod(G,M,E,S,T,K,R,Q,F)$")
            finding = next(f for f in scan_text(path, self.registry) if f.findingType == "retired_equation")
            self.assertGreaterEqual(finding.confidence, .95)

    def test_code_fence_is_not_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "code.md", "```text\nchi = G/S\n```\n")
            self.assertFalse([f for f in scan_text(path, self.registry) if f.findingType == "retired_equation"])

    def test_raw_fragment_is_protected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "raw.md", "<!-- raw-fragment:start -->\nchi = product(G,M,E,S,T,K,R,Q,F)\n<!-- raw-fragment:end -->\n")
            finding = next(f for f in scan_text(path, self.registry) if f.findingType == "retired_equation")
            self.assertTrue(finding.protected); self.assertNotEqual("auto_fix", finding.suggestedAction)

    def test_mojibake_and_emoji_are_audited(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "encoding.txt", "Broken â€™ text 😀\n")
            kinds = {f.findingType for f in scan_text(path, self.registry)}
            self.assertTrue({"mojibake", "emoji"}.issubset(kinds))

    def test_html_scans_text_nodes_not_attributes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "page.html", '<p title="chi = G/S">chi = G/S</p>')
            findings = [f for f in scan_html(path, self.registry) if f.findingType == "retired_equation"]
            self.assertEqual(1, len(findings)); self.assertEqual("html", findings[0].contextType)

    def test_html_equation_image_and_math_script_are_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "page.html", '<img alt="Master equation" src="old.png"><script type="math/tex">chi=G/S</script>')
            findings = scan_html(path, self.registry)
            self.assertEqual(2, sum(f.findingType == "html_render_drift" for f in findings))

    def test_patch_is_proposed_without_mutating_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "01_canonical.md", "chi = product(G,M,E,S,T,K,R,Q,F)\n")
            original = path.read_text(); findings = scan_text(path, self.registry)
            patch = proposed_patches(findings)
            self.assertIn("chi(X) = C_W", patch); self.assertEqual(original, path.read_text())

    def test_apply_only_changes_safe_exact_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            safe = self.write(tmp, "01_canonical-safe.md", "chi = product(G,M,E,S,T,K,R,Q,F)\n")
            risky = self.write(tmp, "01_canonical-risk.md", "chi = G/S\n")
            findings = scan_text(safe, self.registry) + scan_text(risky, self.registry)
            changed = apply_safe(findings)
            self.assertEqual([str(safe)], changed); self.assertIn("G/S", risky.read_text())

    def test_autolink_first_use_per_section_and_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "01_canonical.md", "# A\nMaster Equation here. Master Equation again.\n# B\nMaster Equation here.\n")
            proposals = autolink_markdown(path, self.registry.autolink_terms, "section", True)
            self.assertEqual(2, sum(p.canonId == "tp:eq/master-equation/v3" for p in proposals))
            self.assertEqual(2, path.read_text().count("[[eq:v3]]"))

    def test_autolink_avoids_quotes_headings_and_fences(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "01_canonical.md", "# Terminus Sui\n> Trinitarian\n```\nLaw 1\n```\nMaster Equation\n")
            proposals = autolink_markdown(path, self.registry.autolink_terms)
            self.assertEqual(["Master Equation"], [p.term for p in proposals])

    def test_html_autolink_is_dom_aware_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "page.html", '<code>Law 1</code><p>Law 1 explains it.</p>')
            proposals = autolink_html(path, self.registry.autolink_terms)
            self.assertEqual(1, len(proposals)); self.assertIn("canon-pill", proposals[0].suggestedLink)

    def test_result_schema_serializes_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "x.md", "chi = G/S\n")
            payload = ScanResult(1, scan_text(path, self.registry)).to_dict()
            finding = payload["findings"][0]
            for key in ("file", "line", "column", "contextType", "findingType", "confidence", "distancePoints", "suggestedAction", "requiresHumanRuling"):
                self.assertIn(key, finding)
            json.dumps(payload)


if __name__ == "__main__": unittest.main()
