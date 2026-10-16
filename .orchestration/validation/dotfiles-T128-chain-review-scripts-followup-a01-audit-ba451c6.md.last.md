- [P2] high implementation scripts/orchestrator/local-review.sh:96 `read -r -a` breaks valid `env -S` quoting: `--require "/opt/review modules/init.js"` becomes three arguments containing literal quotes instead of two. A read-only comparison with native `env -S` reproduced this. Valid launchers can fail before reviewing; the test covers only unquoted arguments.
- [P2] high orchestration .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a01.md:88 The known quoting defect is marked `not-applicable` because a subsequent task will fix it. That defers rather than fixes or refutes it, contrary to the integration rule. The recorded waiver concerns INV-6 counts. Although the owner task exists locally, this disposition’s `git show origin/main:…` evidence command fails because that file has not landed there.
- [P3] high evidence .orchestration/dotfiles-T128-chain-review-scripts-followup-a01/sandbox.md:4 The committed count is 19, but rows 1–17 plus acknowledged calls 5a, 8b and 11a total 20, matching the supplied final sandbox record. The committed machine-readable evidence understates the count by one.

INV-2: holds .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a01.md:70 — 3 source/test files, 100 changed production lines and 170 test additions satisfy the named caps.

Both premises hold at the original branch base, and the committed task copy matches the dispatched hash. After `gh` failed, the GitHub connector confirmed final-head CI success; all 11 relevant tests passed within the 1,122-test suite. [CI evidence](https://github.com/mryfmo/dotfiles/actions/runs/38843542821/job/116788814618).

Orchestration findings: 1

📝 まとめ: Audited [PR #364](https://github.com/mryfmo/dotfiles/pull/364) at `ba451c66`; found three issues and modified nothing.
Not rerun: local suites, mutation harness, real reviewer or merge gate; quoted `env -S` launchers remain affected.
Verdict: incorrect