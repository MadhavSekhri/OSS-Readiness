"""Reports contain evidence-based remediations and SARIF 2.1.0 structure."""
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from oss_readiness.audit import audit
from oss_readiness.cli import main
from oss_readiness.report import findings_from_audit, to_sarif


class ReportTests(unittest.TestCase):
    def test_sarif_for_empty_repo(self):
        with tempfile.TemporaryDirectory() as directory:
            report = audit(directory)
            sarif = to_sarif(report)
            self.assertEqual(sarif["version"], "2.1.0")
            run = sarif["runs"][0]
            self.assertEqual(run["tool"]["driver"]["name"], "OSS Readiness")
            self.assertEqual(len(run["results"]), len(report["checks"]))
            self.assertTrue(all("locations" not in r for r in run["results"]))
            self.assertTrue(all("ruleId" in r and "message" in r for r in run["results"]))
            self.assertEqual(run["properties"]["score"], 0)

    def test_passed_evidence_removes_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "README.md").write_text("Nonempty documentation", encoding="utf-8")
            results = findings_from_audit(audit(directory))
            self.assertNotIn("OSS-README", [x["rule_id"] for x in results])
            self.assertIn("OSS-LICENSE", [x["rule_id"] for x in results])

    def test_cli_sarif_and_threshold_exit_status(self):
        with tempfile.TemporaryDirectory() as directory:
            with redirect_stdout(StringIO()) as stream:
                status = main([directory, "--format", "sarif", "--min-score", "1"])
            self.assertEqual(status, 1)
            sarif = json.loads(stream.getvalue())
            self.assertEqual(sarif["runs"][0]["properties"]["score"], 0)
            with redirect_stdout(StringIO()) as stream:
                status = main([directory, "--json"])
            self.assertEqual(status, 0)
            report = json.loads(stream.getvalue())
            self.assertIn("findings", report)

    def test_no_absolute_workspace_path_in_sarif(self):
        with tempfile.TemporaryDirectory() as directory:
            data = json.dumps(to_sarif(audit(directory)))
            self.assertNotIn(directory, data)


if __name__ == "__main__":
    unittest.main()
