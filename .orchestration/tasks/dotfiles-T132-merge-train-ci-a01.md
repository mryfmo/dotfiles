---
format: 2
task_id: dotfiles-T132-merge-train-ci-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - .github/workflows/test.yaml
  - .github/workflows/remote.yaml
  - .github/workflows/agent-assets.yml
  - scripts/run_unit_test.sh
  - Makefile
  - tests/unit/test_workflow_orchestration_skip.py
  - .orchestration/dotfiles-T132-merge-train-ci-a01/**
after: []
threat_table:
  - control: "the PR edits .github/workflows/test.yaml in four places (the train/** push trigger, the concurrency block, the decide step's range for a train push, nothing else in the job)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_the_unit_test_decision_judges_a_train_push_against_main"
  - control: "the PR edits .github/workflows/remote.yaml in three places (the train/** push trigger, the concurrency block, the one decide script both bootstrap jobs share: the bootstrap path list and the train range)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_a_pull_request_skips_the_bootstrap_when_no_bootstrap_path_changed"
  - control: "the PR edits .github/workflows/agent-assets.yml in four places (the train/** push trigger, the concurrency block, fetch-depth 0 on the checkout, a decide step with a step-level if on the three heavy steps; the job keeps no job-level if or needs)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_no_required_contexts_job_has_a_job_level_if_or_needs"
  - control: the PR edits scripts/run_unit_test.sh only in its four bats invocations (the --jobs argument)
    disposition: "residual: the job count is read from getconf _NPROCESSORS_ONLN and overridden by BATS_JOBS, a positive integer the script checks; no test path, filter or HOME handling changes; bats is CI-only here (Test Policy), so the first green run of test (ubuntu-24.04, client) and test (macos-14, client) on the PR is the evidence the RESULT names"
  - control: the PR edits Makefile only in the unit-test target (VERIFY 3)
    disposition: "residual: one recipe line; the target still exits nonzero when any module fails (xargs exits 123) and the module list comes from git ls-files, never from a glob of the working tree"
  - control: the PR edits tests/unit/test_workflow_orchestration_skip.py only in its constants and the decision cases
    disposition: "residual: REQUIRED_CONTEXTS stays byte-identical to the ruleset's seven contexts (premise 2); the structural tests (no job-level if or needs, every heavy step gated, the reader failing closed) stay byte-identical; the new cases run the decide scripts against a temporary repository as the existing ones do"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T132-merge-train-ci-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T132-merge-train-ci-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the unit tests run the decide scripts with bash in a temporary clone under the test's TemporaryDirectory with a fake GITHUB_OUTPUT file, as the module's existing cases do; nothing reads the host's checkout, and no test runs bats or a workflow"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: the three workflow files are the trust boundary (CI that decides the seven required checks): every decide step runs under set -euo pipefail inside its own job, computes its range from origin/main fetched in the step and from github.sha, never from a PR-controlled file; every skip is a step-level if on steps.decide.outputs, so a required job always reports; the push trigger is the literal train/** branch filter and no paths: filter is added at workflow level; cancel-in-progress is true only when github.event_name is pull_request and the group for a push is the sha, so no push run of main or of a train is cancelled or superseded"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script (decide steps inside existing workflow jobs, flags in an existing runner); any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main; this PR's own CI runs on its pull_request event as today, the train trigger it adds fires only after it is on main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: none of the three workflows on origin/main has a train/ trigger or a concurrency block
    command: for f in test.yaml remote.yaml agent-assets.yml; do git show origin/main:.github/workflows/$f | /usr/bin/grep -c -E 'train/|^concurrency:' || true; done | paste -sd' ' -
    output: |-
      0 0 0
  - claim: the README's ruleset payload lists seven required contexts (validate; test and public-bootstrap for ubuntu-24.04 server and client and macos-14 client), the set tests/unit/test_workflow_orchestration_skip.py pins as REQUIRED_CONTEXTS
    command: git show origin/main:README.md | /usr/bin/grep -c '"context":'
    output: |-
      7
  - claim: the test workflow already installs GNU parallel on both runners (brew and apt lines), which bats --jobs requires
    command: git show origin/main:.github/workflows/test.yaml | /usr/bin/grep -c -E 'install .*parallel'
    output: |-
      2
  - claim: the runner has no --jobs today and the Python unit tests run through the Makefile's unittest discover, not through scripts/run_unit_test.sh
    command: a=$(git show origin/main:scripts/run_unit_test.sh | /usr/bin/grep -c -- '--jobs' || true); b=$(git show origin/main:Makefile | /usr/bin/grep -c 'unittest discover'); echo "$a $b"
    output: |-
      0 1
---

# AGMSG-TASK dotfiles-T132-merge-train-ci-a01 — CI for the merge train: train/** runs, in-job bootstrap skip, PR cancellation, parallel tests

Written 2026-10-18 by the orchestrator seat from the operator's specification of 08:1x JST (decision `D-train-strict-off`, decisions.tsv, in the working tree until the next boundary commit). The train builder is the sibling task `dotfiles-T132-merge-train-builder-a01` (file-disjoint; it runs live only after this PR is on main). The ruleset's seven required checks (premise 2) fail open on a skipped job, so every skip in this task is a step-level `if` inside the job (SKILL line 78: "no required job carries a job-level `if` or a `needs`"; `grep -c` 1 on `origin/main`, pasted in the NOTES), as `test.yaml` and `remote.yaml` already do.

## Goal

A push to a `train/**` branch runs the three required-check workflows once on the train tip, each job deciding inside itself from `origin/main...<tip>` whether its paths changed; the bootstrap jobs skip (inside the job, reporting success) when neither the PR nor the train tip touches a bootstrap path; a new push to a PR cancels that PR's running workflows; the bats suites run with `--jobs`.

## Files

1. `.github/workflows/test.yaml`: (a) `on.push.branches: [main, "train/**"]`; (b) a top-level `concurrency:` block, `group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.sha }}` and `cancel-in-progress: ${{ github.event_name == 'pull_request' }}` (a push run's group is its sha: never queued behind, never superseded); (c) the decide step takes the train case before the `BEFORE_SHA` case: when `github.ref` starts with `refs/heads/train/` (pass `REF: ${{ github.ref }}` in the step's `env`), `git fetch --no-tags origin main` and `diff_range="origin/main...${HEAD_SHA}"`; the path regex and the `should_test` outputs are unchanged. Nothing else in the job changes; the `continue-on-error` canary stays.
2. `.github/workflows/remote.yaml`: (a) and (b) as item 1; (c) the one decide script both bootstrap jobs share (the test `test_both_bootstrap_jobs_decide_with_the_same_script` pins the two scripts equal): a `pull_request` event and a `train/` push both diff `origin/main...${HEAD_SHA}` (the fetch as today); every other event keeps `should_run=true`; `should_run=true` only when the diff lists a bootstrap path: `^(setup\.sh$|install/|home/|scripts/lib/|scripts/update-agent-assets\.sh$|scripts/gh-auth\.sh$|tests/install/|\.github/workflows/remote\.yaml$)` (the operator's list plus the workflow itself); an empty diff still runs. The skip-notice step's text says which range was compared and that no bootstrap path changed. The step-level `if` form on the bootstrap steps stays as it is.
3. `.github/workflows/agent-assets.yml`: (a) and (b) as item 1; (c) `fetch-depth: 0` on the checkout (the decide needs the merge base); (d) a step `Decide whether the diff needs the asset validation` with `id: decide`, after the checkout and before `Setup uv`, in the remote.yaml form: `pull_request` and a `train/` push diff `origin/main...${HEAD_SHA}`, every other event is `should_run=true`, and the path regex is `^(home/|scripts/validate-agent-assets\.py$|scripts/update-agent-assets\.sh$|scripts/require-crit-review\.py$|\.coderabbit\.yaml$|\.github/workflows/agent-assets\.yml$)` (the files `scripts/validate-agent-assets.py` reads: `ROOT / "home/..."` at lines 92 to 375 and the token checks at lines 1004 to 1230; VERIFY 1); a notice step for the skip; `if: ${{ steps.decide.outputs.should_run == 'true' }}` on `Setup uv`, `Validate agent assets` and `Parse CodeRabbit config`; the two scheduled steps keep their own `if` and-ed with the decision. No job-level `if` or `needs`.
4. `scripts/run_unit_test.sh`: each of the four `bats` invocations (the three suites and the files test, not the `--count` call) gets `--jobs "${BATS_JOBS:-$(getconf _NPROCESSORS_ONLN)}"`; the value is checked once in `main` (`[[ ${BATS_JOBS:-1} =~ ^[1-9][0-9]*$ ]]`). GNU parallel is installed on both runners (premise 3); bats prints `requires GNU parallel` and fails otherwise, which is the desired loud failure. The shdoc header gains one sentence on `BATS_JOBS`.
5. `Makefile` (VERIFY 3, default in scope): the `unit-test` recipe becomes `git ls-files -z 'tests/unit/test_*.py' | xargs -0 -n 1 -P "$$(getconf _NPROCESSORS_ONLN)" uv run python -m unittest -v`; `xargs` exits 123 when a module fails, so `make unit-test` still fails; output lines of modules interleave, each test line still carries its module.
6. `tests/unit/test_workflow_orchestration_skip.py`: `DECIDING_JOBS` gains `(AGENT_ASSETS, "validate", ASSET_DECISION, "steps.decide.outputs.should_run == 'true'")`, `UNGATED_STEPS` the new decision and notice names (and `Setup uv` is gated, so it is not added); `test_every_event_but_pull_request_bootstraps` becomes `test_every_event_but_pull_request_and_a_train_push_bootstraps`; `test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff` becomes `test_a_pull_request_skips_the_bootstrap_when_no_bootstrap_path_changed` (cases: `.orchestration/x` false, `scripts/orchestrator/x.sh` false, `README.md` false, `install/x.sh` true, `home/x` true, `setup.sh` true, empty diff true, a rename out of `home/` true); new `test_the_unit_test_decision_judges_a_train_push_against_main` (`REF=refs/heads/train/20261018-1`, `EVENT_NAME=push`, a train clone two commits ahead of origin/main whose first commit touches `scripts/x.sh`: `should_test=true`; the same with both commits under `.orchestration/`: false) and `test_the_asset_validation_decision_skips_an_unrelated_diff` for item 3. `REQUIRED_CONTEXTS` and the structural tests stay byte-identical.

## Out of scope

The train builder and its tests (the sibling task); any gate or `scripts/orchestrator/**` change; the ruleset payload in the README (the seven contexts do not change; strict up-to-date is the user's admin switch); `macos.yaml`, `ubuntu.yaml` and `docs.yml` (not required checks); Codecov settings; the bats modules themselves (a test that fails only under `--jobs` is reported in the RESULT with its name and fixed in a follow-up, never by removing `--jobs` from one suite without the orchestrator's answer).

## Check

Pasted in the validation file: `make render-check` (exit 0; the standing check), `shellcheck -x scripts/run_unit_test.sh` (CI's form, `test.yaml` step "Run ShellCheck") and `mise x shfmt@3.14.1 -- shfmt -i 4 -sr -d scripts/run_unit_test.sh` (CI's form) both clean, `uv run python -m unittest tests/unit/test_workflow_orchestration_skip.py tests/unit/test_workflow_security.py -v` green, `make unit-test` green through the new recipe, `uv run --with pyyaml python -c 'import yaml,sys; [yaml.safe_load(open(p)) for p in sys.argv[1:]]' .github/workflows/test.yaml .github/workflows/remote.yaml .github/workflows/agent-assets.yml` (parses), and `git diff --numstat origin/main...HEAD`. Bats is not run locally (Test Policy): the PR's own CI runs the suites with `--jobs` on the three `test` jobs, and the RESULT names those runs and their durations beside the previous run of `origin/main`. Caps: under 200 changed lines (added plus deleted) outside `tests/` and `.orchestration/` (plan 021 step 7.2) and under 1000 added under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main`; under the merge-gate policy the worker opens its PR with the plain draft create form itself (`gh pr create --draft --head <branch>`). `dotfiles-T129-pstack-asset-a01` names `.github/workflows/agent-assets.yml` in its `allowed_files` and has no dispatch line yet (its record of 2026-10-17T10:22Z); the Parallelism rule holds, so it is not dispatched while this PR is open, or this task waits for its merge (the orchestrator decides before dispatch, VERIFY 2). No in-flight PR touches a workflow file, `scripts/run_unit_test.sh`, `Makefile` or `tests/unit/test_workflow_orchestration_skip.py` (`git diff --name-only origin/main...origin/<branch>` of #393, #378, #375, #390 and #400 on 2026-10-18, pasted in the NOTES). A textual conflict is a `PONG status=blocked`, never a hand merge. The Completion clause of `.orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md` applies as written, with `dotfiles-T132-merge-train-ci-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears, before the PR's dispositions, C-51) and `task_copy=<sha256 of .orchestration/dotfiles-T132-merge-train-ci-a01/task.md>` in the RESULT, which also names the three `test` runs with `--jobs` and whether any bats test failed only in parallel.

## VERIFY (the orchestrator closes each before dispatch; a closed item becomes Amendment 1 text, an open one a decided default)

- VERIFY 1: the complete set of files `scripts/validate-agent-assets.py` reads (item 3's regex). Default: the regex of item 3; the worker greps `ROOT /` and the literal path strings in the validator before writing it and widens the regex when a path falls outside, naming the addition in report.md.
- VERIFY 2: whether `dotfiles-T129-pstack-asset-a01` is dispatched before this task (its PR would overlap on `agent-assets.yml`). Default: this task first; pstack rebases.
- VERIFY 3: whether the Python unit tests are in scope (the operator's "parallel unit tests in scripts/run_unit_test.sh": that script runs only bats; the Python suite runs through `make unit-test`, premise 4). Default: in scope through the Makefile recipe of item 5, `Makefile` in `allowed_files`. If the orchestrator says no, item 5 and the Makefile rows are struck and the cap falls to 150.
- VERIFY 4: `bats --jobs` under bashcov on the Ubuntu jobs (`ruby scripts/run_bashcov_unit_test.rb -- scripts/run_unit_test.sh`): parallel bats processes write one xtrace stream, so the coverage upload may become partial or the run may fail. Default: `--jobs` on every run; if the bashcov run fails or Codecov reports a drop, the RESULT says so and the orchestrator decides between `BATS_JOBS=1` on the bashcov step and dropping bashcov (a follow-up either way).
- VERIFY 5: whether any bats module shares a fixed path outside `BATS_TEST_TMPDIR` (a parallel run would race). Default: none; a failure that appears only under `--jobs` is reported by name (Out of scope).
- VERIFY 6: the GitHub expression `${{ github.event_name == 'pull_request' }}` is accepted as `cancel-in-progress` (a boolean expression; docs.github.com "Using concurrency"). Default: as written; the worker pastes the first run's concurrency behaviour (a second push to the PR cancels the first run) in report.md.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T132-merge-train-ci-a01.md: <pending>
premise 1: <pending>
premise 2: <pending>
premise 3: <pending>
premise 4: <pending>
masked <n> match(es) in .orchestration/tasks/dotfiles-T132-merge-train-ci-a01.md
```
