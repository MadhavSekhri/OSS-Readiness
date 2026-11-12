"""CLI for local OSS project checklist."""
import argparse
import json
from .audit import audit


def main(argv=None):
    parser = argparse.ArgumentParser(prog="oss-readiness", description="Offline OSS hygiene audit")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit(args.path)
    except ValueError as exc:
        parser.exit(2, f"error: {exc}\n")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"OSS hygiene: {result['score']}/{result['max_score']} points")
        for item in result["checks"]:
            print(f"{'PASS' if item['passed'] else 'MISSING'} {item['id']}: {item['guidance']}")
        print(result["caveat"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
