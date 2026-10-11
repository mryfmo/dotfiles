---
format: 2
task_id: dotfiles-T128-ci-skip-orchestration-a02
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
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
    disposition: "closed: GitHub reports a skipped job as Success even for a required check (fail-open: actions docs, control-jobs-with-conditions and workflow-syntax jobs.needs), so no required job carries a job-level if or a needs; each bootstrap job, and test.yaml's test job, decides in its own first step and gates its heavy steps on that step's output; test asserts no job-level if and no needs on any required context's job, read by the fail-closed reader of the row below (an unsupported key form fails the test instead of reading as absent)"
  - control: the decision step itself fails (git fetch, a script error)
    disposition: "closed: an in-job decision step that fails fails the required context (fail-closed) instead of skipping it; test asserts the decision step has no continue-on-error and that every heavy step's if reads its output, read by the same fail-closed reader"
  - control: the hand-written workflow reader misses a valid YAML form (quoted, escaped or spaced keys, flow mappings)
    disposition: "closed: the reader fails closed: inside jobs:, a job name, a job key or a step key that is not the plain form name: (lower-case letters, digits, _ and -, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises and fails every structural test, so an unsupported form can never read as no if; tests: if : false, \"\\x69f\": false, continue-on-error : true and a step written as the flow mapping { if: false } each fail the structural tests (a real YAML parser replaces the reader only if the test environment gains one; this task adds no dependency)"
  - control: the task's invariant sentence and map entry are not on main at dispatch (INV-2)
    disposition: "closed: INV-2 requires the design on main before the implementing TASK is dispatched; the design that names this task id (dotfiles-T128-ci-skip-orchestration-a02: [INV-2]) lands on main through the boundary PR orchestration/boundary-2026-10-11-2, and the TASK the worker acts on is the amendment TASK the orchestrator sends after that merge (the 07:38Z TASK predates it and is superseded; the acceptance record names both); this PR takes that main with gh pr update-branch and merges only after its final audit on that head; test: none (the acceptance record pastes git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sha256sum and the two TASK ids)"
  - control: push and schedule events have no PR range
    disposition: "closed: should_run is true for every event but pull_request; test asserts it"
after: []
reset_of: [dotfiles-T128-ci-skip-orchestration-a01]
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

# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-a02 — plan 006 A201: an .orchestration-only PR runs no bootstrap or test matrix (reset of a01)

Phase A5 (design tier: workflows); the reset successor of `dotfiles-T128-ci-skip-orchestration-a01` under INV-6 (reset record `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01-design-reset.md`). The same Claude seat (`claude-standard-dot-a003`), the same branch `feat/ci-skip-orchestration` and PR #320, continuing from `dc4e6c37`; the implementation on that head stays. Implements INV-2's CI clause (design v16, unchanged sentence).

## What to build

1. `.github/workflows/remote.yaml`: each of `public-bootstrap` and `private-bootstrap` computes `should_run` in its own first step (no separate `changes` job and no `needs`: a job that `needs` a failed or skipped job is skipped and a skipped required job reports Success) for the event: on `pull_request` from the base-to-head diff (`false` only when every changed path is under `.orchestration/`), and on `push`, `schedule` and `workflow_dispatch` always `true` (those events have no PR range to judge and must keep bootstrapping `main`). `public-bootstrap` and `private-bootstrap` keep their job names and matrix; every heavy step carries a step-level `if: steps.decide.outputs.should_run == 'true'` (never a job-level `if` or a `needs`, which turn a failed decision into a passing required check; never an early-exit step, which cannot skip later steps), so the job completes with success and reports its context on an `.orchestration`-only PR. `test.yaml`'s `test` job already gates its heavy steps but through `needs: changes` (fail-open today, on main): it takes the same in-job decision step and drops the `needs`; the `changes` job goes when nothing needs it; a `main-tests` job, when present (V0 is parked and A5 precedes it, so the test must not require the job), takes the same in-job decision with step-level `if`s. The steps keep the pins `tests/unit/test_workflow_security.py` asserts (action SHAs, `permissions`, `persist-credentials: false`); `agent-assets.yml` is cheap and unchanged.
2. `tests/unit/test_workflow_orchestration_skip.py`: YAML-level checks that every required context's job has no job-level `if` and no `needs`, that each carries the decision step without `continue-on-error`, that each heavy step of `public-bootstrap`, `private-bootstrap` and, when the job exists, `main-tests` carries the `should_run` (or `should_test`) step-level `if`, that the decision yields `true` for `push`, `schedule` and `workflow_dispatch`, and that the context names equal a named constant `REQUIRED_CONTEXTS` that copies premise 1's seven contexts (a unit test cannot read the ruleset; the constant is what changes when the ruleset changes); each fails when its rule is removed. The reader fails closed: inside `jobs:`, a job name, a job key or a step key that is not the plain form `name:` (lower-case letters, digits, `_` and `-`, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises, so an unsupported form fails every structural test instead of reading as "no `if`"; the test environment has no YAML parser (`make unit-test` runs bare `uv run python`) and this task adds no dependency. `tests/unit/test_workflow_security.py` must keep passing.
3. Validation: YAML-parse the workflows; the module under `make unit-test`; the four unsupported-form mutations (`if : false`, `"\x69f": false`, `continue-on-error : true`, a step written as `{ if: false }`) each fail the structural tests, pasted into validation.md; after the merge the orchestrator pastes `gh pr checks` timings of the next `.orchestration`-only PR into the acceptance record (A201's completion condition: ≤ 10 minutes with every required check reported).

## History

a01: Amendment 1 (2026-10-11 05:50Z, after the worker's PONG with the GitHub doc evidence) turned the `changes`-job pattern into the in-job fail-closed decision: the two rows on skipped jobs and failed decision steps, items 1 and 2 and premise 1 reworded, `test.yaml`'s `test` job fixed in the same PR. Revise round 1 (`dc4e6c37`) closed rename detection (`--no-renames`) and quoted keys. The audit of `dc4e6c37` found the reader class a second time (spaced and escaped keys, flow mappings) and re-raised the design-on-main prerequisite; this reset closes the reader class as a whole (fail closed on any unsupported form) and the design-on-main prerequisite (the two new rows), and changes nothing else.

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md` (the a01 directory stays as it is); evidence beside it, on the same branch from `dc4e6c37`. Phase A5 of plan 006; dormant contracts are withdrawn from the pattern, so this PR carries its tests directly.

## Completion

PR #320 stays the PR (no new draft); once the boundary PR `orchestration/boundary-2026-10-11-2` is merged, `gh pr update-branch` before the final audit; CI, Bot wait (`@codex review` if nothing in 10 minutes), artifacts, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=8. Forbidden: anything outside `allowed_files`; `make update`; thread resolution.
