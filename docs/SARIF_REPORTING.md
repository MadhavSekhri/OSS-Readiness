# P1: Evidence-based SARIF reports

Run oss-readiness . --format sarif > report.sarif to produce SARIF 2.1.0.
Run oss-readiness . --format json to include structured remediation findings.
Default terminal and the legacy --json flag stay backward-compatible.

Stable rule identifiers use the OSS- prefix, for example OSS-README,
OSS-SECURITY, OSS-ISSUE-TEMPLATE, and OSS-CI.

Missing evidence produces a warning, a plain-language remediation and
a rule ID. A passed check produces no warning. Missing files do not
have a meaningful source code location, so the SARIF output intentionally
does not fabricate regions or artifact locations.

The output never includes an absolute repository path, target file body,
or secret. The tool executes no project code and makes no network call.

Passing results are only basic repository hygiene. They do not prove
security posture, license validity, CI success, software quality,
OpenSSF certification, or AI-credit eligibility.

The --min-score threshold continues to control exit code independently
of reporting format: zero for meeting it, one for falling below it.
