# OSS Readiness — Product & Engineering RFC

## Mission
An offline, safe-by-default repository health inspector with verifiable evidence and useful remediation. A file-presence checklist is an entry point, not a quality/security badge. Reviewer demo: scan a real Python or JS project, show why each finding passed/failed, reject symlinks outside root, and export deterministic JSON in a CI Action.

## Wide view and differentiation
Maintainers need to understand reproducibility, contributor access, trustworthy releases, license clarity, and security practices. Most simple repository checkers can be fooled by empty files or placeholders. Stand out by *evidence-backed* rules, explainable failures, safe filesystem handling and low setup cost. Use OpenSSF best practices as a reference without asserting certification.

## Primary adopter
Solo or small-team OSS maintainer before accepting outside contributors or publishing v1.0. Wants actionable local and CI checks, not vanity rankings. A CI workflow should fail only for clearly defined missing requirements.

## Scope
Offline metadata and minimally bounded file content inspection; README/license/contribution/security/CI/test/release checks with evidence paths. Deterministic JSON, shell-friendly output and stable codes. No arbitrary external commands or network calls. No finding can guarantee code security, legal compliance or grant eligibility.

## Proposed architecture
Root path -> trust-boundary-aware file resolver -> bounded catalog of rule probes -> Finding(id, result, evidence, remedy, limitations) -> stable JSON/console reporters -> CI gate. Rules must be independent and versioned, with optional ecosystem profiles added only after real fixtures. Avoid executing scripts from target repositories; do not invoke package managers as part of assessment.

## Security and quality principles
Never follow symlinks outside root; ignore paths that are links when evaluating evidence. Bound recursion and count when locating test files. Exclude generated/binary/vendor directories. Do not print hostile filenames unescaped in console. A present workflow file does not mean CI passed. Test with adversarial filenames, empty files, symlinks and nested dummy projects.

## Roadmap
**P0 (initial PR):** symlink containment, bounded safe test file discovery, reliable CI evidence, edge-case tests, explicit caveats.
**P1:** structured rule findings and fix guidance; modular Python/JS/Go/Rust/Java profiles with positive and negative fixtures.
**P2:** SARIF/JSON schema, GitHub Action output, public quality examples, checked limited OpenSSF baseline mapping and self-audit without false badge claims.
**P3:** SBOM/release-readiness probes, benchmarks on large projects, versioned signed releases, independent developer feedback.

## Acceptance and review gate
Safe to run on attacker-controlled repo in a low-permission environment: no command execution, network or out-of-root traversal; fixed maximum work; tests on Python 3.10/3.12; CI permission minimal; CLI stable exit codes. Use test project fixtures; report limitations at every score.

## Adoption evidence
Real third-party Action consumers, independently filed issues, reproducible project diagnostics, fixes to ecosystem-specific false positives and meaningful upstream contributions, never automated star/download/PR boosting.

## Integration
Run the scanner in the other three new repos *only after* independently validating its findings. Do not award positive scores just because these repos contain a few template files.

## Open design decisions
Should the 0–100 score remain prominent at all? Which portable evidence checks matter? How to avoid training users to maximize score rather than actual maintainability? Prefer evidence and remediation over a single score.
