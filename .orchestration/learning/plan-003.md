# Plan 003 learning triage

## Observations

- Chezmoi v2.70.5 exposes the documented two-column status contract directly in `chezmoi status --help`: column 1 compares last-written and actual state, while column 2 compares actual and target state.
- A CI bootstrap can enforce HOME isolation without a new framework by requiring `HOME` to be under the native `RUNNER_TEMP` path before apply.
- Public PR correctness requires both executing checkout `setup.sh` and pointing chezmoi initialization at the checkout; checking only the script body would still allow managed state from `main`.
- Crit receipt enum fields are strict: `review_outcome` must be exactly `approved` or `addressed`.
- Executing `shell -c "$(fetch_url ...)"` masks a failed fetch behind the outer shell command; capture installer text in a checked assignment before execution.
- Debian package lookup distinguishes exit 1 (not installed) from exit 2 (fatal); only exit 1 should enter the missing-package set.
- Bootstrap safety claims must separate source/config mutations from destination-target mutations and must not imply transactionality for `chezmoi apply`.
- A green PR rollup is insufficient evidence: inspect exact-head workflow runs and
  check suites because a workflow may fail before creating any check run.
- Job-level expressions cannot use every runner context; initialize isolated HOME
  in a runner step through `RUNNER_TEMP` and `GITHUB_ENV`.
- Composed shell templates need subshell isolation when included scripts declare
  identical readonly globals.

## Reuse decision

- Candidate only; no reusable rule was promoted or written to project learn files because this task forbids `.agents/worklog` source changes and the orchestrator owns promotion decisions.
- Suggested destinations if promoted: bootstrap CI guidance/tests for checkout source locality and Crit evidence receipt examples.
- Additional candidate destinations: installer-download safety guidance, Debian package-state helpers, and bootstrap target-boundary test conventions.
