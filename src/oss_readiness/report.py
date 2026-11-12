"""SARIF 2.1.0 diagnostics from bounded, offline repository evidence checks.

Missing evidence is a warning about repository hygiene, not a security finding.
"""
REMEDIATIONS = {
    "readme": "Add a nonempty README describing purpose, installation and usage.",
    "license": "Declare an appropriate, reviewed open-source license in LICENSE.",
    "contributing": "Add CONTRIBUTING.md with development and review instructions.",
    "security": "Add SECURITY.md describing a private vulnerability reporting process.",
    "conduct": "Add a code of conduct and a private reporting method.",
    "changelog": "Maintain user-facing release changes in CHANGELOG.md.",
    "gitignore": "Add .gitignore suitable for the language and generated artifacts.",
    "ci": "Add a nonempty CI workflow and independently verify that it runs.",
    "tests": "Add test-named, nonempty automated test files in test/ or tests/.",
    "issue_template": "Provide a meaningful issue template in .github/ISSUE_TEMPLATE/.",
    "pull_request_template": "Provide a useful GitHub pull-request template.",
}

INFORMATION_URI = "https://github.com/MadhavSekhri/OSS-Readiness"
SARIF_SCHEMA = "https://json.schemastore.org/sarif-2.1.0.json"


def rule_id(identifier):
    return "OSS-" + identifier.replace("_", "-").upper()


def findings_from_audit(audit_result):
    """Return actionable, stable IDs for failed evidence checks only."""
    return [
        {
            "rule_id": rule_id(check["id"]),
            "id": check["id"],
            "level": "warning",
            "message": check["guidance"],
            "remediation": REMEDIATIONS[check["id"]],
            "points": check["points"],
        }
        for check in audit_result["checks"] if not check["passed"]
    ]


def to_sarif(audit_result):
    """Produce SARIF for supported code-scanning viewers without false locations."""
    rules = []
    for check in audit_result["checks"]:
        rules.append({
            "id": rule_id(check["id"]),
            "name": check["id"],
            "shortDescription": {"text": check["guidance"]},
            "help": {"text": REMEDIATIONS[check["id"]]},
            "properties": {"tags": ["maintainability", "repository-hygiene"]},
        })
    results = []
    for finding in findings_from_audit(audit_result):
        results.append({
            "ruleId": finding["rule_id"],
            "level": finding["level"],
            "message": {"text": finding["message"] + " " + finding["remediation"]},
            # Missing files have no real source location; do not invent one.
            "properties": {"points": finding["points"]},
        })
    return {
        "$schema": SARIF_SCHEMA,
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {
                "name": "OSS Readiness",
                "informationUri": INFORMATION_URI,
                "semanticVersion": "0.1.0",
                "rules": rules,
            }},
            "results": results,
            "properties": {
                "score": audit_result["score"],
                "maxScore": audit_result["max_score"],
                "caveat": audit_result["caveat"],
            },
        }],
    }
