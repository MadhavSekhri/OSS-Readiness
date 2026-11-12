# OSS Readiness

A local CLI to review whether an open-source repository has basic contributor-facing documents and development infrastructure.

**Status:** early prototype. This tool is a **file-presence checklist**, not a security audit, popularity metric, quality certification, or eligibility determination for AI-credit programs.

## Install

    python -m pip install -e .

## Usage

    oss-readiness .
    oss-readiness . --json

This checks README, LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, .gitignore, CI, tests, and issue/PR templates. The result is a weighted 0–100 checklist score. The presence of these files does not guarantee their quality. The CLI does not access the network, require a token, or modify a repository.

## Tests

    python -m unittest discover -s tests -v

## Contribute

See CONTRIBUTING.md, SECURITY.md and CODE_OF_CONDUCT.md. Contributions should improve accuracy or explain project health more usefully, rather than chasing arbitrary scores.

## License

MIT; see LICENSE.
