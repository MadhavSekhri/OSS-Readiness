# OSS Readiness

A local CLI to review whether an open-source repository has basic contributor-facing documents and development infrastructure.

**Status:** early prototype. This tool is a **file-presence checklist**, not a security audit, popularity metric, quality certification, or eligibility determination for AI-credit programs.

## Install

    python -m pip install -e .

## Usage

    oss-readiness .
    oss-readiness . --json
    oss-readiness . --min-score 75

This checks README, LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, .gitignore, CI, tests, and issue/PR templates. The result is a weighted 0–100 checklist score. The tool verifies that files are nonempty, test directories contain test-named files, and CI/issue-template directories contain supported files. That still does not guarantee their quality or that CI runs successfully. `--min-score` makes it usable as a local development gate (exit code 1 if below threshold); the score is not evidence of grant eligibility. The CLI does not access the network, require a token, or modify a repository.

## Structured findings and SARIF output (P1)

Export actionable missing-evidence warnings to a SARIF 2.1.0-compatible report:

    oss-readiness . --format sarif > oss-readiness.sarif
    oss-readiness . --format json --min-score 75

Each missing check produces a stable rule ID such as OSS-SECURITY and a
remediation recommendation. The SARIF document contains no absolute
workspace path or fictional source locations. The --json flag remains
compatible with the reusable GitHub Action. See
[reporting guidance](docs/SARIF_REPORTING.md).

## Use as a GitHub Action

Other repositories can run this checklist automatically:

```yaml
name: OSS documentation check
on: [push, pull_request]
permissions:
  contents: read
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - uses: MadhavSekhri/OSS-Readiness@main
        with:
          path: .
          min-score: '75'
```

A failing score exits with status 1; the Action also exposes a numeric `score` output. Pin the Action to a reviewed commit SHA or versioned release in production. A high checklist score measures document and CI-file presence, **not code security, maintainer quality, adoption, or AI-credit eligibility**.

## Tests

    python -m unittest discover -s tests -v

## Contribute

See CONTRIBUTING.md, SECURITY.md and CODE_OF_CONDUCT.md. Contributions should improve accuracy or explain project health more usefully, rather than chasing arbitrary scores.

## License

MIT; see LICENSE.

## Architecture and security

This is an actively developed prototype, not a certification or completed production service. Review the [product design and acceptance gates](docs/PRODUCT_PLAN.md), [threat model](docs/THREAT_MODEL.md), and [implementation contract](docs/EVIDENCE_MODEL.md) before depending on it. Changes are proposed through draft pull requests with automated tests and security-focused code review.
