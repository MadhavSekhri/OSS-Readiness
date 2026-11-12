"""CLI for local OSS project documentation checklist."""
import argparse
import json
from .audit import audit
from .report import findings_from_audit, to_sarif


def main(argv=None):
    parser = argparse.ArgumentParser(prog="oss-readiness", description="Offline OSS hygiene audit")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", help="Print JSON diagnostics")
    parser.add_argument("--min-score", type=int, default=0,
                        help="Fail with exit code 1 if score is below N (0-100)")
    parser.add_argument("--format", choices=("text", "json", "sarif"), default="text",
                        help="Console, JSON, or SARIF 2.1.0 output")
    args = parser.parse_args(argv)
    if not 0 <= args.min_score <= 100:
        parser.error("--min-score must be from 0 to 100")
    try:
        result = audit(args.path)
    except ValueError as exc:
        parser.exit(2, f"error: {exc}\n")
    result["meets_threshold"] = result["score"] >= args.min_score
    fmt = "json" if args.json else args.format
    if fmt == "json":
        result["findings"] = findings_from_audit(result)
        print(json.dumps(result, indent=2))
    elif fmt == "sarif":
        print(json.dumps(to_sarif(result), indent=2))
    else:
        print(f"OSS hygiene: {result['score']}/{result['max_score']} points")
        for item in result["checks"]:
            print(f"{'PASS' if item['passed'] else 'MISSING'} {item['id']}: {item['guidance']}")
        print(result["caveat"])
    return 0 if result["meets_threshold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
