---
task_id: dotfiles-T133-ci-efficiency-followup-a01
seat: claude-standard-dot-a011
---

# Learning: dotfiles-T133-ci-efficiency-followup-a01

1. An owned row can need a file the owner task does not list. The two bootstrap workflows must keep byte-identical decide scripts (`test_both_bootstrap_jobs_decide_with_the_same_script`), so a row about `remote.yaml` also needs `private-bootstrap.yaml`. Mechanism: before editing a file that a row names, grep the tests for equality assertions over that file (`decide_script(`, `assertEqual(` on two workflows), and ask with evidence, such as the failing test names, before writing the fix. Here the question and its answer took about two minutes, and row 2 proceeded meanwhile.
2. `git -c core.quotePath=false diff --name-only` still quotes a name that holds `"`, `\` or a control character. Only `-z` gives raw paths. A line-oriented `grep` over the quoted output is fail-open for a path gate, because the bootstrap gets skipped. Mechanism: the new test plants all four characters under `home/`. `test.yaml`'s unit-test decision has the same pattern and is named as an advisory observation for the next owner.
3. A step that writes to `${RUNNER_TEMP}` needs the test harness to export it, or `set -u` fails the step. Mechanism: `run_decision` now runs every decision inside a temporary directory exported as `RUNNER_TEMP`, so later workflow edits that use it are testable without changing the fixture again.
