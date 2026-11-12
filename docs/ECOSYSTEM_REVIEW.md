# Ecosystem review and positioning

Review date: 2026-11-12.

## Existing projects
- OpenSSF Scorecard: https://scorecard.dev/ — automated security risk checks and scores for source repositories.
- OpenSSF Best Practices Badge: https://openssf.org/projects/best-practices-badge/ — verified/self-reported project practice criteria and maturity.
- OpenSSF Scorecard description: https://openssf.org/projects/scorecard/ — risk-focused checks and adoption guidance.

## The gap to address
Do **not** duplicate security scanning or invent a competitor 'security score'. Build an **offline evidence-and-remediation checker for contributor onboarding**: does the repository provide usable documentation, real test files, an actual workflow, issue/PR templates, and a reproducible local development path? State exactly which files are evidence and what has *not* been checked.

## Reviewer demo
Scan synthetic repositories with valid docs, empty placeholders, symlinks to external files and huge test directories. Stable JSON shows specific evidence paths; the CLI exits nonzero on a documented score gate. Show that a high score is not an OpenSSF badge.

## Future work
Add ecosystem-specific profiles and rule explanations, clearly identified unchecked risks, bounded metadata scanning, optional SARIF reports, an explanation of why test detection may yield false negatives, and compatibility with Scorecard rather than replacing it.

## Measure real usefulness
A third-party repository adopts the Action and fixes legitimate gaps, reports false positives and contributes a valid cross-language rule. Do not optimize for a vanity headline metric.
