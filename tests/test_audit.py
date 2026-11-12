import tempfile
import unittest
from pathlib import Path
from oss_readiness.audit import audit


class TestAudit(unittest.TestCase):
    def test_empty_repo_scores_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            result = audit(directory)
            self.assertEqual(result["score"], 0)
            self.assertEqual(result["max_score"], 100)

    def test_expected_files_increase_score(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("README")
            (root / "LICENSE").write_text("MIT")
            (root / "tests").mkdir()
            self.assertEqual(audit(root)["score"], 40)

    def test_nonexistent_path_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                audit(Path(directory) / "missing")


if __name__ == "__main__":
    unittest.main()
