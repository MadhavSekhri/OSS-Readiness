"""Deterministic checklist for open-source repository file presence."""
from pathlib import Path

CHECKS = (
    ("readme", 15, ("README.md", "README.rst", "README"), "Document purpose and usage"),
    ("license", 15, ("LICENSE", "LICENSE.md", "COPYING"), "Provide a recognized OSS license"),
    ("contributing", 10, ("CONTRIBUTING.md", ".github/CONTRIBUTING.md"), "Explain how to contribute"),
    ("security", 10, ("SECURITY.md", ".github/SECURITY.md"), "Provide a security disclosure policy"),
    ("conduct", 5, ("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"), "Set community expectations"),
    ("changelog", 5, ("CHANGELOG.md", "CHANGES.md"), "Track user-visible changes"),
    ("gitignore", 5, (".gitignore",), "Exclude generated files and secrets"),
    ("ci", 15, (".github/workflows/ci.yml", ".github/workflows/ci.yaml", ".gitlab-ci.yml"), "Run CI checks"),
    ("tests", 10, ("tests", "test"), "Include automated tests"),
    ("issue_template", 5, (".github/ISSUE_TEMPLATE",), "Guide issue reporting"),
    ("pull_request_template", 5, (".github/pull_request_template.md", "PULL_REQUEST_TEMPLATE.md"), "Guide PRs"),
)


def audit(path: str | Path):
    base = Path(path).resolve()
    if not base.is_dir():
        raise ValueError("path must be a local directory")
    checks = []
    score = 0
    total = 0
    for ident, weight, candidates, guidance in CHECKS:
        present = any((base / candidate).exists() for candidate in candidates)
        checks.append({"id": ident, "points": weight, "passed": present, "guidance": guidance})
        total += weight
        if present:
            score += weight
    return {
        "path": str(base),
        "score": score,
        "max_score": total,
        "checks": checks,
        "caveat": "File-presence checklist only; not grant eligibility, quality assurance or security certification.",
    }
