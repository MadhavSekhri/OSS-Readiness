"""Offline evidence checks for local repository contributor readiness.

This tool does not execute repository scripts, contact GitHub or certify security.
"""
import os
from itertools import islice
from pathlib import Path

MAX_DIRECTORY_EVIDENCE_FILES = 128
MAX_TEST_FILES_SCANNED = 256
MAX_TEST_DEPTH = 5
MAX_TEST_DIRS_SCANNED = 128
IGNORED_DIRS = frozenset({
    ".git", "node_modules", "vendor", "dist", "build", ".venv",
    "venv", "__pycache__", ".tox", ".mypy_cache", "target",
})
CHECKS = (
    ("readme", 15, ("README.md", "README.rst", "README"), "Document purpose and usage"),
    ("license", 15, ("LICENSE", "LICENSE.md", "COPYING"), "Declare an OSS license"),
    ("contributing", 10, ("CONTRIBUTING.md", ".github/CONTRIBUTING.md"), "Explain how to contribute"),
    ("security", 10, ("SECURITY.md", ".github/SECURITY.md"), "Provide a security disclosure policy"),
    ("conduct", 5, ("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"), "Set community expectations"),
    ("changelog", 5, ("CHANGELOG.md", "CHANGES.md"), "Track user-visible changes"),
    ("gitignore", 5, (".gitignore",), "Exclude generated files and secrets"),
    ("ci", 15, (".github/workflows", ".gitlab-ci.yml"), "Include a CI configuration file"),
    ("tests", 10, ("tests", "test"), "Include nonempty automated test files"),
    ("issue_template", 5, (".github/ISSUE_TEMPLATE",), "Guide issue reporting"),
    ("pull_request_template", 5, (".github/pull_request_template.md", "PULL_REQUEST_TEMPLATE.md"), "Guide PRs"),
)


def _within_safe_tree(base: Path, candidate: Path) -> bool:
    """Reject symlinks in every path component, including directory ancestors."""
    try:
        relative = candidate.relative_to(base)
    except ValueError:
        return False
    current = base
    try:
        for component in relative.parts:
            current = current / component
            if current.is_symlink():
                return False
        return True
    except OSError:
        return False


def _safe_file(base: Path, candidate: Path) -> bool:
    try:
        return (
            _within_safe_tree(base, candidate)
            and candidate.is_file()
            and candidate.stat().st_size > 0
        )
    except OSError:
        return False


def _safe_folder(base: Path, candidate: Path) -> bool:
    try:
        return _within_safe_tree(base, candidate) and candidate.is_dir()
    except OSError:
        return False


def _relative(base: Path, file: Path) -> str:
    return file.relative_to(base).as_posix()


def _test_filename(name: str) -> bool:
    lower = name.lower()
    return (
        (lower.startswith("test_") and lower.endswith((".py", ".rs", ".js", ".ts")))
        or lower.endswith(("_test.go", ".test.js", ".test.ts", ".spec.ts", ".spec.js", "_spec.rb"))
        or (name.startswith("Test") and name.endswith(".java"))
    )


def _find_tests(base: Path) -> list[str]:
    """Search only bounded test roots; never follow directory symlinks."""
    evidence = []
    visited_files = 0
    visited_dirs = 0
    for relative_root in ("tests", "test"):
        root = base / relative_root
        if not _safe_folder(base, root):
            continue
        for current_name, directories, filenames in os.walk(root, followlinks=False):
            current = Path(current_name)
            depth = len(current.relative_to(root).parts)
            visited_dirs += 1
            if depth >= MAX_TEST_DEPTH or visited_dirs >= MAX_TEST_DIRS_SCANNED:
                directories[:] = []
            else:
                directories[:] = sorted(
                    directory for directory in directories
                    if directory not in IGNORED_DIRS and
                    _safe_folder(base, current / directory)
                )[:MAX_TEST_DIRS_SCANNED - visited_dirs]
            for filename in sorted(islice(filenames, MAX_TEST_FILES_SCANNED - visited_files)):
                visited_files += 1
                candidate = current / filename
                if _test_filename(filename) and _safe_file(base, candidate):
                    evidence.append(_relative(base, candidate))
                    return evidence
                if visited_files >= MAX_TEST_FILES_SCANNED:
                    return evidence
            if visited_dirs >= MAX_TEST_DIRS_SCANNED:
                return evidence
    return evidence


def _present(base: Path, check: str, candidates: tuple[str, ...]) -> list[str]:
    if check == "tests":
        return _find_tests(base)
    if check == "ci":
        workflows = base / ".github" / "workflows"
        if _safe_folder(base, workflows):
            for candidate in sorted(islice(workflows.iterdir(), MAX_DIRECTORY_EVIDENCE_FILES), key=lambda entry: entry.name):
                if candidate.suffix.lower() in {".yml", ".yaml"} and _safe_file(base, candidate):
                    return [_relative(base, candidate)]
        gitlab = base / ".gitlab-ci.yml"
        return [_relative(base, gitlab)] if _safe_file(base, gitlab) else []
    if check == "issue_template":
        folder = base / ".github" / "ISSUE_TEMPLATE"
        if _safe_folder(base, folder):
            for candidate in sorted(islice(folder.iterdir(), MAX_DIRECTORY_EVIDENCE_FILES), key=lambda entry: entry.name):
                if candidate.suffix.lower() in {".md", ".yml", ".yaml"} and _safe_file(base, candidate):
                    return [_relative(base, candidate)]
        return []
    for filename in candidates:
        candidate = base / filename
        if _safe_file(base, candidate):
            return [_relative(base, candidate)]
    return []


def audit(path: str | Path):
    base = Path(path).resolve()
    if not base.is_dir():
        raise ValueError("path must be a local directory")
    checks = []
    score = 0
    total = 0
    for ident, weight, candidates, guidance in CHECKS:
        evidence = _present(base, ident, candidates)
        passed = bool(evidence)
        checks.append({
            "id": ident,
            "points": weight,
            "passed": passed,
            "guidance": guidance,
            "evidence": evidence,
        })
        total += weight
        if passed:
            score += weight
    return {
        "path": str(base),
        "score": score,
        "max_score": total,
        "checks": checks,
        "caveat": "File-presence evidence only; not security certification, actual CI success, code quality or grant eligibility.",
    }
