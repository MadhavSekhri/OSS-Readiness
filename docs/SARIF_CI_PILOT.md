# Export repository readiness findings from CI

Copy this workflow into `.github/workflows/oss-readiness.yml` in the repository you want to check. It produces a SARIF artifact for every successful evaluation, including evaluations below the chosen score. It uses read-only repository permissions.

```yaml
name: OSS readiness
on: [push, pull_request]
permissions:
  contents: read
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
        with:
          persist-credentials: false
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0
        with:
          python-version: '3.12'
      - name: Install reviewed revision
        run: python -m pip install 'OSS-Readiness @ git+https://github.com/MadhavSekhri/OSS-Readiness@7feb7bb73305f8db39a7ab959ea5f145f76ed'
      - name: Generate report
        shell: bash
        run: |
          status=0
          oss-readiness . --format sarif --min-score 0 > oss-readiness.sarif.tmp || status=$?
          if [[ "$status" == 0 || "$status" == 1 ]] && [[ -s oss-readiness.sarif.tmp ]]; then
            mv oss-readiness.sarif.tmp oss-readiness.sarif
          fi
          exit "$status"
      - name: Upload report
        if: ${{ !cancelled() && hashFiles('oss-readiness.sarif') != '' }}
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4.6.2
        with:
          name: oss-readiness.sarif
          path: oss-readiness.sarif
          retention-days: 7
          if-no-files-found: error
```

Start with an advisory run at a minimum score of 0. Download the artifact from the run and inspect `runs[0].results`. Pick one finding that matters to your contributors, address it in a PR, and check that its rule ID disappears. For example, if the repository lacks a security policy, add the project's real vulnerability-reporting instructions and check for the disappearance of `OSS-SECURITY`.

You can set a team-approved score above 0 later. A below-threshold result will fail the job while keeping the report available. These findings cover contributor-facing repository files and development infrastructure.
