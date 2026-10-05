# AGMSG-TASK dot-ci-runner-label-pin-T58-a01

Drafted 2026-10-02 by the orchestrator seat; operator-approved (queued after T56 and T57). Worker: `claude-standard-dot-a005` in `~/Workspace/dotfiles/.claude/worktrees/worker-c`. Do not start before the AGMSG-TASK dispatch for T58 arrives.

## Objective

GitHub annotates every CI run with "The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026" (8 annotations per PR). The September task `runner-label-pin T18` was never executed. Make the runner choice explicit so the migration cannot change CI behaviour silently, and prove the suite on Ubuntu 26 before the deadline.

1. Replace every `ubuntu-latest` with the explicit label of the image it resolves to today, `ubuntu-24.04`, in `.github/workflows/{test,remote,agent-assets,docs,ubuntu}.yaml` (`runs-on:` and matrix `os:` values, and the `if [ "${OS}" == ... ]` string comparisons that key on the label) and in `scripts/run_unit_test.sh` (the `OS` comparisons). Keep `macos-14` unchanged.
2. Add one non-required canary cell to `test.yaml`'s `test` matrix: `os: ubuntu-26.04` with `continue-on-error: true` for the `client` system only, so a failure is visible in the run but does not block merges. If the `ubuntu-26.04` label is not yet available, record the exact GitHub response in the validation file and leave the canary out (state it in the report).
3. Update the required-check context names that the label change renames: the ruleset payload in `README.md` (`test (ubuntu-latest, server)` → `test (ubuntu-24.04, server)`, likewise `client`, and the two `public-bootstrap (ubuntu-latest, …)` entries), and the fixture names in `tests/unit/test_pr_feedback.py` that mirror them. Note in the report that the operator must re-apply the ruleset payload after merge (the live ruleset, if any, keys on context names).
4. Ground every occurrence with `git grep -n -E 'ubuntu-latest' -- .github scripts tests README.md Makefile` before editing and paste the list; after editing the same grep must return only `README.md` lines inside the migration notice, if you keep one, or nothing.

[memory:decision] T58 (operator 2026-10-02): CI runner labels are explicit (`ubuntu-24.04`, `macos-14`), never `*-latest`; a new OS image is adopted through a non-required canary cell first, then by changing the explicit label.

## Repo / branch

- Work ONLY in the worker-c worktree. `git fetch origin`; `git switch -c chore/ci-runner-label-pin origin/main`. Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `.github/workflows/test.yaml`, `remote.yaml`, `agent-assets.yml`, `docs.yml`, `ubuntu.yaml`
- `scripts/run_unit_test.sh`
- `README.md` (ruleset payload context names only)
- `tests/unit/test_pr_feedback.py` (fixture check names only), `tests/unit/test_workflow_security.py` if it asserts labels
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ci-runner-label-pin-T58-a01.md` (main checkout)

## Forbidden actions

- Any installer, rule, skill, manifest or launcher change; merging; force push; local bats; `make apply`; pushing `main`.

## Validation commands (paste verbatim output)

```
git grep -n -E 'ubuntu-latest' -- .github scripts tests README.md Makefile
git diff origin/main --stat
make unit-test
make validate-agent-assets
gh pr checks <pr-number>      # must show the renamed contexts and the canary cell's result
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green (the canary may be red; it is `continue-on-error`).
2. Artifacts at the exact expected paths; validation with verbatim outputs, PR number and head SHA.
3. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
4. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=25.

## Decisions on the PONG (orchestrator, 2026-10-03 01:35 JST)

1. `tests/unit/test_supply_chain_policy.py` is added to the allowed files. Its `test_nix_inputs_lock_and_ci_use_2605` asserts `"ubuntu-latest" in workflow` as a token check; change that one assertion to the explicit label (`ubuntu-24.04`) and nothing else in the file. The orchestrator's grounding missed it; `make unit-test` must pass.
2. Accepted: in the shell `if [ "${OS}" == ... ]` checks of `test.yaml` and `scripts/run_unit_test.sh`, match the Ubuntu family (`ubuntu-*`) so the `ubuntu-26.04` canary cell takes the Ubuntu branch instead of "not supported". `runs-on:` and matrix `os:` values stay explicit labels. The Codecov upload condition pins `ubuntu-24.04` only, so the canary never uploads coverage.
3. Accepted: `tests/unit/test_pr_feedback.py:130` is GitHub annotation text, not a check context name; leave it unchanged. Only the required-check context names (`test (ubuntu-latest, …)`, `public-bootstrap (ubuntu-latest, …)`) in that file and in the README ruleset payload are renamed.

Everything else in this task is unchanged.
