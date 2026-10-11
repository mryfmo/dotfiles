---
reviewed_at: 2026-10-11T07:31:44Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4
task: dotfiles-T128-ci-skip-redesign-a01
reset_of: dotfiles-T128-ci-skip-orchestration-a01
source: .orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md@8e9c23daf670ab73dc26603cfbc4001fd3bbbd560829a46fa3a163c21f6c76a7
a02_expected_sha256: 2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
verdict: redesign
---

# Redesign: the successor task file dotfiles-T128-ci-skip-orchestration-a02

The block below is the whole a02 file, derived from a01 at 8e9c23da by a script that applied each edit exactly once and asserted it, then parsed the front matter with PyYAML: task_id and reset_of (item 1); the "required job is skipped" and "decision step itself fails" rows keep their tests and now name the fail-closed reader (item 2, first half); the reader row with its four mutations and the design-on-main row, inserted after the decision-step row (items 2 and 3); item 2 of "What to build" gains the fail-closed rule, Validation the four mutations, Amendment 1 becomes History, the first-commit path is the a02 directory with the a01 directory kept, the heading, first paragraph and Completion continue PR #320 from dc4e6c37 (item 4). The table has 7 rows; the INV-2 sentence, allowed_files, premises and items 1 and 3's other text are byte for byte a01's. Written to a file with a trailing newline, the block hashes to a02_expected_sha256 above; the outer fence is four backticks and the file carries no fence.

Four points where the text departs from the TASK's wording, each for a reason the orchestrator should weigh before writing the file:

1. after: stays []. The TASK asked for after: [orchestration/boundary-2026-10-11-2], but V1's schema types after as task ids that must be accepted before dispatch, INV-10's dispatchability reads the same list, and that name is a branch; the a02 task.md copy would fail V1's validation once the regime job binds. The boundary dependency is carried in the design-on-main row and in Completion instead.
2. The design-on-main row needs a map entry for a02. INV-2's sentence compares the task id with implementing_tasks and remaps only an id ending in -contract-a01; v16 maps dotfiles-T128-ci-skip-orchestration-a01 alone, so a boundary PR carrying v16 unchanged leaves a02 unmapped and the row false. The row therefore says the design on main names a02 beside a01 (a hashed-key change with its pair of reviews; the INV-2 sentence itself unchanged, so a02's sentence stays byte-equal). The same gap applies to dotfiles-T128-regime-counters-a02 (INV-6), outside this task.
3. The fail-closed rule covers job names as well as job and step keys (the TASK's item 2 named the job and step mappings). A scan of the PR-head workflows under jobs: found every job name, job key, step item and step key already in the plain form, so the rule rejects nothing real; a quoted job name would otherwise still read as the job.
4. Completion drops "Draft PR within 30 minutes": PR #320 exists and stays the PR; the update-branch step after the boundary merge and before the final audit is added there.

Premises: unchanged from a01 and not re-run (gh is unreachable from this seat; the second audit reports both holding against live GitHub data). The "fail-open today, on main" clause of item 1 still holds: main's test.yaml at b896d9bc carries needs: changes on the test job.

````markdown
---
format: 2
task_id: dotfiles-T128-ci-skip-orchestration-a02
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
    disposition: "closed: GitHub reports a skipped job as Success even for a required check (fail-open: actions docs, control-jobs-with-conditions and workflow-syntax jobs.needs), so no required job carries a job-level if or a needs; each bootstrap job, and test.yaml's test job, decides in its own first step and gates its heavy steps on that step's output; test asserts no job-level if and no needs on any required context's job, read by the fail-closed reader of the row below (an unsupported key form fails the test instead of reading as absent)"
  - control: the decision step itself fails (git fetch, a script error)
    disposition: "closed: an in-job decision step that fails fails the required context (fail-closed) instead of skipping it; test asserts the decision step has no continue-on-error and that every heavy step's if reads its output, read by the same fail-closed reader"
  - control: the hand-written workflow reader misses a valid YAML form (quoted, escaped or spaced keys, flow mappings)
    disposition: "closed: the reader fails closed: inside jobs:, a job name, a job key or a step key that is not the plain form name: (lower-case letters, digits, _ and -, the colon immediately after; no quotes, no escapes, no flow mapping; comments and blank lines aside) raises and fails every structural test, so an unsupported form can never read as no if; tests: if : false, \"\\x69f\": false, continue-on-error : true and a step written as the flow mapping { if: false } each fail the structural tests (a real YAML parser replaces the reader only if the test environment gains one; this task adds no dependency)"
  - control: the task's invariant sentence and map entry are not on main at dispatch (INV-2)
    disposition: "closed: the design that names this task id in implementing_tasks (dotfiles-T128-ci-skip-orchestration-a02: [INV-2] beside a01's entry; a hashed-key change with its pair of design reviews, the INV-2 sentence unchanged) lands on main through the boundary PR orchestration/boundary-2026-10-11-2 before this PR's final audit; this PR takes that main with gh pr update-branch and merges only from a head audited on it; test: none (the acceptance record pastes git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md | sha256sum and the map line)"
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
````
