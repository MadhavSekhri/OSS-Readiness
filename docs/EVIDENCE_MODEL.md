# Audit evidence semantics

This tool runs offline. It does not execute target scripts or check whether CI is actually green, a license is legally valid or a vulnerability exists.

## Evidence
JSON output adds an `evidence` array to each check. Each entry is a path relative to the selected repository root. Evidence requires a nonempty regular file; symlinked evidence and directories with symlinked ancestors are rejected. Test discovery searches bounded `test/` and `tests/` directories for common Python, Go, JavaScript, TypeScript, Ruby, Rust and Java test filenames.

## Resource budget
- At most 256 candidate test files and 128 test directories are scanned, to depth 5.
- The scanner ignores known build/vendor/cache directories and does not follow directory symlinks.
- It checks for first matching evidence, rather than trying to inspect every file.
- A repository that hides its only tests after the bounds may receive a false negative; improve the tests or future rule profiles if necessary.

## Limitations
An existing workflow YAML is not proof that GitHub Actions runs or succeeds. An existing license file does not certify OSI compatibility. No file-body quality checks or vulnerability scanning occur in v0.1. The numeric score is a quick hygiene signal, not OpenSSF certification or AI-credit qualification. This is not race-proof against a concurrent attacker mutating the filesystem during scanning.

## Extending
See [Product plan](PRODUCT_PLAN.md) and [Threat model](THREAT_MODEL.md) for ecosystem profiles, SARIF and future remediations.
