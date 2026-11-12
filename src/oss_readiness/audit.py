"""Deterministic local OSS repository contributor-readiness checklist.

A useful documentation checklist, NOT a quality, security or grant eligibility score.
"""
from pathlib import Path

CHECKS = (
    ("readme", 15, ("README.md", "README.rst", "README"), "Document purpose and usage"),
    ("license", 15, ("LICENSE", "LICENSE.md", "COPYING"), "Declare an OSS license"),
    ("contributing", 10, ("CONTRIBUTING.md", ".github/CONTRIBUTING.md"), "Explain how to contribute"),
    ("security", 10, ("SECURITY.md", ".github/SECURITY.md"), "Provide a security disclosure policy"),
    ("conduct", 5, ("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"), "Set community expectations"),
    ("changelog", 5, ("CHANGELOG.md", "CHANGES.md"), "Track user-visible changes"),
    ("gitignore", 5, (".gitignore",), "Exclude generated files and secrets"),
    ("ci", 15, (".github/workflows", ".gitlab-ci.yml"), "Run CI checks"),
    ("tests", 10, ("tests", "test"), "Include automated tests"),
    ("issue_template", 5, (".github/ISSUE_TEMPLATE",), "Guide issue reporting"),
    ("pull_request_template", 5, (".github/pull_request_template.md", "PULL_REQUEST_TEMPLATE.md"), "Guide PRs"),
)


def _has_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def _present(base: Path, check: str, candidates: tuple[str, ...]) -> bool:
    if check == "ci":
        workflows = base / ".github" / "workflows"
        if workflows.is_dir() and any(
            _has_file(p) for p in workflows.iterdir() if p.suffix.lower() in {".yml", ".yaml"}
        ):
            return True
        return _has_file(base / ".gitlab-ci.yml")
    if check == "tests":
        return any(
            candidate.is_dir() and any(
                path.is_file() and (
                    "test" in path.stem.lower() or path.name.endswith(".spec.ts")
                ) for path in candidate.rglob("*")
            ) for candidate in (base / relative for relative in candidates)
        )
    if check == "issue_template":
        folder = base / ".github" / "ISSUE_TEMPLATE"
        return folder.is_dir() and any(
            _has_file(p) for p in folder.iterdir()
            if p.suffix.lower() in {".md", ".yml", ".yaml"}
        )
    return any(_has_file(base / candidate) for candidate in candidates)


def audit(path: str | Path):
    base = Path(path).resolve()
    if not base.is_dir():
        raise ValueError("path must be a local directory")
    checks = []
    score = 0
    total = 0
    for ident, weight, candidates, guidance in CHECKS:
        present = _present(base, ident, candidates)
        checks.append({
            "id": ident,
            "points": weight,
            "passed": present,
            "guidance": guidance,
        })
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
