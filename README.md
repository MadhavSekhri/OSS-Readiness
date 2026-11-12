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
