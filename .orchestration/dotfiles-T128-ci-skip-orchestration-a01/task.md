---
format: 2
task_id: dotfiles-T128-ci-skip-orchestration-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - .github/workflows/remote.yaml
  - .github/workflows/test.yaml
  - tests/unit/test_workflow_orchestration_skip.py
invariants:
  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside its jobs, as test.yaml's changes job does), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
threat_table:
  - control: the PR edits the workflow files themselves
    disposition: "residual: a pull_request workflow is PR-controlled (design R8); compensating control: V1c's regime job refuses workflow edits outside a design-tier task, operator routing of workflow changes, the design-tier audit; tests/unit/test_workflow_security.py pins SHAs, permissions and persist-credentials"
  - control: the decision step misclassifies a diff as .orchestration-only
    disposition: "closed: the classification is one git diff --name-only over the merge-base range with a single grep for a path outside .orchestration/; tests: a mixed diff, a pure .orchestration diff, a renamed file, a deleted file"
  - control: a required job is skipped (a job-level if, or needs on a job that failed or was skipped)
    disposition: "closed: GitHub reports a skipped job as Success even for a required check (fail-open: actions docs, control-jobs-with-conditions and workflow-syntax jobs.needs), so no required job carries a job-level if or a needs; each bootstrap job, and test.yaml's test job, decides in its own first step and gates its heavy steps on that step's output; test asserts no job-level if and no needs on any required context's job"
  - control: the decision step itself fails (git fetch, a script error)
    disposition: "closed: an in-job decision step that fails fails the required context (fail-closed) instead of skipping it; test asserts the decision step has no continue-on-error and that every heavy step's if reads its output"
  - control: push and schedule events have no PR range
    disposition: "closed: should_run is true for every event but pull_request; test asserts it"
after: []
premises:
  - claim: "the seven required checks are validate, test (3 legs) and public-bootstrap (3 legs); a required check skipped at the workflow level stays pending and blocks the merge, while a job skipped by a job-level if or by needs on a failed or skipped job reports Success even when required (fail-open), so each required job decides inside itself with a step that fails closed"
    command: "gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type==\"required_status_checks\")|.parameters.required_status_checks[].context]|join(\"; \")'; sed -n 1,12p .github/workflows/test.yaml"
    output: |-
      validate; test (ubuntu-24.04, server); test (ubuntu-24.04, client); test (macos-14, client); public-bootstrap (ubuntu-24.04, server); public-bootstrap (ubuntu-24.04, client); public-bootstrap (macos-14, client)
      name: Unit test
      
      on:
        # Required checks must always report a final status for PRs into `main`.
        # Do not add workflow-level path or branch filters here: GitHub can leave
        # skipped required checks in a pending state and block merges.
        # Keep this workflow unconditional and decide inside jobs whether the full
        # test matrix is necessary for the current diff.
        push:
          branches: [main]
        pull_request:
          branches: [main]
  - claim: "boundary PR 316 (.orchestration files only) ran the three public-bootstrap legs on each of its six heads, 7 to 9 minutes per leg on the final head c264c7d1 plus queue time; an .orchestration-only PR needs none of them"
    command: "gh api repos/mryfmo/dotfiles/commits/c264c7d1/check-runs --paginate --jq '.check_runs[]|select(.name|startswith(\"public-bootstrap\"))|[.name,.started_at,.completed_at]|@tsv'; gh api repos/mryfmo/dotfiles/pulls/316/commits --paginate --jq 'length'"
    output: |-
      public-bootstrap (macos-14, client)	2026-10-10T23:51:13Z	2026-10-10T23:58:20Z
      public-bootstrap (ubuntu-24.04, client)	2026-10-10T23:51:09Z	2026-10-11T00:00:07Z
      public-bootstrap (ubuntu-24.04, server)	2026-10-10T23:51:09Z	2026-10-10T23:58:50Z
      6
---

# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-a01 — plan 006 A201: an .orchestration-only PR runs no bootstrap or test matrix

Phase A5 (design tier: workflows); dispatched in Phase A, no dependency on V0. Claude seat, `.claude/worktrees/worker-f` or whichever is free, branch `feat/ci-skip-orchestration` from `origin/main`. Implements INV-2's CI clause (design v16, unchanged sentence).

## What to build

1. `.github/workflows/remote.yaml`: each of `public-bootstrap` and `private-bootstrap` computes `should_run` in its own first step (no separate `changes` job and no `needs`: a job that `needs` a failed or skipped job is skipped and a skipped required job reports Success) for the event: on `pull_request` from the base-to-head diff (`false` only when every changed path is under `.orchestration/`), and on `push`, `schedule` and `workflow_dispatch` always `true` (those events have no PR range to judge and must keep bootstrapping `main`). `public-bootstrap` and `private-bootstrap` keep their job names and matrix; every heavy step carries a step-level `if: steps.decide.outputs.should_run == 'true'` (never a job-level `if` or a `needs`, which turn a failed decision into a passing required check; never an early-exit step, which cannot skip later steps), so the job completes with success and reports its context on an `.orchestration`-only PR. `test.yaml`'s `test` job already gates its heavy steps but through `needs: changes` (fail-open today, on main): it takes the same in-job decision step and drops the `needs`; the `changes` job goes when nothing needs it; a `main-tests` job, when present (V0 is parked and A5 precedes it, so the test must not require the job), takes the same in-job decision with step-level `if`s. The steps keep the pins `tests/unit/test_workflow_security.py` asserts (action SHAs, `permissions`, `persist-credentials: false`); `agent-assets.yml` is cheap and unchanged.
2. `tests/unit/test_workflow_orchestration_skip.py`: YAML-level checks that every required context's job has no job-level `if` and no `needs`, that each carries the decision step without `continue-on-error`, that each heavy step of `public-bootstrap`, `private-bootstrap` and, when the job exists, `main-tests` carries the `should_run` (or `should_test`) step-level `if`, that the decision yields `true` for `push`, `schedule` and `workflow_dispatch`, and that the context names equal a named constant `REQUIRED_CONTEXTS` that copies premise 1's seven contexts (a unit test cannot read the ruleset; the constant is what changes when the ruleset changes); each fails when its rule is removed. `tests/unit/test_workflow_security.py` must keep passing.
3. Validation: YAML-parse the workflows; the module under `make unit-test`; after the merge the orchestrator pastes `gh pr checks` timings of the next `.orchestration`-only PR into the acceptance record (A201's completion condition: ≤ 10 minutes with every required check reported).

## Amendment 1 (orchestrator, 2026-10-11 05:50Z, after the worker's PONG with the GitHub doc evidence)

The `changes`-job pattern was fail-open: a failed `changes` job skips the jobs that `need` it and a skipped required job reports Success. The threat table gains the two rows above (a missing row, added once); items 1 and 2 and premise 1 are reworded to the in-job decision step; `test.yaml`'s `test` job is fixed the same way in this PR because it carries the same fail-open `needs` on `main` and is in `allowed_files`. No other change.

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-ci-skip-orchestration-a01/task.md`; evidence beside it. Phase A5 of plan 006; dormant contracts are withdrawn from the pattern, so this PR carries its tests directly.

## Completion

Draft PR within 30 minutes, `gh pr ready` before the Bot wait, CI, Bot wait (`@codex review` if nothing in 10 minutes), artifacts, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=8. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.
