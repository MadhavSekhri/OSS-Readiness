import tempfile
import unittest
from pathlib import Path
from oss_readiness.audit import audit
from oss_readiness.cli import main
from contextlib import redirect_stdout
from io import StringIO


class TestAudit(unittest.TestCase):
    def test_empty_repo_scores_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            result = audit(directory)
            self.assertEqual(result["score"], 0)
            self.assertEqual(result["max_score"], 100)

    def test_real_docs_and_tests_increase_score(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("README", encoding="utf-8")
            (root / "LICENSE").write_text("MIT", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_app.py").write_text("assert True", encoding="utf-8")
            self.assertEqual(audit(root)["score"], 40)

    def test_empty_files_or_directories_do_not_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").touch()
            (root / "tests").mkdir()
            (root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            self.assertEqual(audit(root)["score"], 0)

    def test_any_named_workflow_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ci = root / ".github" / "workflows"
            ci.mkdir(parents=True)
            (ci / "test-python.yaml").write_text("name: test", encoding="utf-8")
            self.assertEqual(audit(root)["score"], 15)

    def test_cli_threshold_controls_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("README", encoding="utf-8")
            sink = StringIO()
            with redirect_stdout(sink):
                self.assertEqual(main([str(root), "--min-score", "15"]), 0)
                self.assertEqual(main([str(root), "--min-score", "20"]), 1)

    def test_nonexistent_path_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                audit(Path(directory) / "missing")


if __name__ == "__main__":
    unittest.main()
