# OSS Readiness — Threat Model

Assets: user filesystem, developer CI credentials, scanning availability, trustworthiness of reported evidence.
Trust boundary: arbitrary repository directory tree -> scanner -> CI stdout / report.

| Threat | Failure | Mitigation |
|---|---|---|
| External symlink | scanner counts private/outside-root files | never follow symlinks for evidence or traversal |
| Huge test tree | resource exhaustion | bounded candidates/depth; ignore generated vendor directories |
| Project code execution | malicious repo takes over CI runner | metadata-only probes; never run project scripts or package managers |
| Control-character filenames | log manipulation | escape or omit untrusted paths in console |
| Empty placeholder files | inflated score | nonempty checks with documented limits |
| Misleading certification | users mistake score for security | every output explicitly disclaims quality/security/eligibility |
| Excessive permissions | unnecessary repository write access | Action consumer uses contents:read |
| Secret content reading | scanner captures sensitive files | no read of arbitrary file bodies in P0 |

Exit criteria: synthetic malicious filesystem fixtures, no network or execution, predictable time and memory, explicit failure remedies.
