import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from oss_readiness.audit import audit
from oss_readiness.cli import main


class TestAudit(unittest.TestCase):
    def test_empty_repo_scores_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            result = audit(directory)
            self.assertEqual(result["score"], 0)
            self.assertEqual(result["max_score"], 100)

    def test_nonempty_docs_and_real_test_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("A useful README", encoding="utf-8")
            (root / "LICENSE").write_text("MIT", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_app.py").write_text("assert True", encoding="utf-8")
            report = audit(root)
            self.assertEqual(report["score"], 40)
            found = next(c for c in report["checks"] if c["id"] == "tests")
            self.assertEqual(found["evidence"], ["tests/test_app.py"])

    def test_empty_docs_and_template_folders_do_not_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").touch()
            (root / "tests").mkdir()
            (root / "tests" / "test_app.py").touch()
            (root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            self.assertEqual(audit(root)["score"], 0)

    def test_symlink_to_external_readme_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as external:
            root = Path(directory)
            target = Path(external) / "README.md"
            target.write_text("outside private data", encoding="utf-8")
            (root / "README.md").symlink_to(target)
            result = audit(root)
            check = next(c for c in result["checks"] if c["id"] == "readme")
            self.assertFalse(check["passed"])

    def test_symlinked_workflow_directory_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as external:
            root = Path(directory)
            (root / ".github").mkdir()
            workflows = Path(external) / "workflows"
            workflows.mkdir()
            (workflows / "ci.yml").write_text("name: demo", encoding="utf-8")
            (root / ".github" / "workflows").symlink_to(workflows, target_is_directory=True)
            result = audit(root)
            self.assertFalse(next(c for c in result["checks"] if c["id"] == "ci")["passed"])

    def test_symlinked_test_directory_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as external:
            root = Path(directory)
            tests = Path(external) / "tests"
            tests.mkdir()
            (tests / "test_app.py").write_text("assert True", encoding="utf-8")
            (root / "tests").symlink_to(tests, target_is_directory=True)
            self.assertFalse(next(c for c in audit(root)["checks"] if c["id"] == "tests")["passed"])

    def test_ci_any_workflow_and_js_test(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wf = root / ".github" / "workflows"
            wf.mkdir(parents=True)
            (wf / "unit-tests.yaml").write_text("name: tests", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "thing.spec.ts").write_text("it('runs')", encoding="utf-8")
            report = audit(root)
            self.assertTrue(next(c for c in report["checks"] if c["id"] == "ci")["passed"])
            self.assertEqual(report["score"], 25)

    def test_cli_threshold_controls_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("README", encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(main([str(root), "--min-score", "15"]), 0)
                self.assertEqual(main([str(root), "--min-score", "20"]), 1)

    def test_nonexistent_path_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                audit(Path(directory) / "missing")


if __name__ == "__main__":
    unittest.main()
