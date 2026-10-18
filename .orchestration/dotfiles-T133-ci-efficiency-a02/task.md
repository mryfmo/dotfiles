---
format: 2
task_id: dotfiles-T133-ci-efficiency-a02
kind: code
security: true
allowed_files:
  - .github/workflows/test.yaml
  - .github/workflows/remote.yaml
  - .github/workflows/private-bootstrap.yaml
  - .github/workflows/agent-assets.yml
  - .github/flakes.yaml
  - scripts/orchestrator/ci-rerun.sh
  - tests/unit/test_workflow_orchestration_skip.py
  - tests/unit/test_ci_rerun.py
  - tests/unit/test_workflow_security.py
  - .orchestration/dotfiles-T133-ci-efficiency-a02/**
after: []
reset_of: [dotfiles-T133-ci-efficiency-a01]
threat_table:
  - control: ".github/workflows/test.yaml (PR concurrency and in-job macOS decisions; home and install changes retain macOS coverage; every required context still reports)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise"
  - control: ".github/workflows/remote.yaml (PR concurrency, extraction of the optional private job, and the public bootstrap path decision including .chezmoiroot and vendor/)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed"
  - control: ".github/workflows/private-bootstrap.yaml (the extracted private job runs on main pushes, schedule and dispatch; its decision remains identical to the public job's)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script"
  - control: ".github/workflows/agent-assets.yml (PR concurrency cancels superseded runs and preserves main runs)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run"
  - control: ".github/flakes.yaml (production signatures are validated with the production matching engine, measured positive samples and real-failure negative samples)"
    disposition: "closed: tests/unit/test_ci_rerun.py::test_the_production_flake_registry_matches_its_samples_and_no_real_failure"
  - control: "scripts/orchestrator/ci-rerun.sh (numeric run ids, current PR head verification, signature classification of every failure conclusion, and persistent atomic reservations per run precede any rerun)"
    disposition: "residual: fake gh tests verify refusal and reservation ordering; unreadable API state prevents reruns, and a final head recheck narrows the unavoidable race between a read and the rerun request"
  - control: "tests/unit/test_workflow_orchestration_skip.py (existing workflow readers, real git fixture repositories, required-context assertions and the added home and install Markdown cases)"
    disposition: "residual: temporary repositories exercise the actual decision scripts; final-head GitHub checks verify the seven required contexts and event behavior"
  - control: "tests/unit/test_ci_rerun.py (fake gh records all arguments and controls PR heads, job conclusions, logs, failures and concurrent calls; the production registry test reads the checked-in data)"
    disposition: "residual: fixtures exercise ordering and refusal without live reruns; registry mutation checks detect invalid and overly broad production expressions"
  - control: "tests/unit/test_workflow_security.py (only the private-bootstrap permissions expectation is added)"
    disposition: "residual: the exact permissions and pinned-action assertions stay intact; the final audit verifies that the sole change is the added expectation"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-ci-efficiency-a02/** (report.md, validation.md, sandbox.md, learning.md, autoskill.md, measure.md and worker review evidence)"
    disposition: "residual: records distinguish inherited measurements from new outputs; red and green evidence, final-head feedback counts and sandbox commands are checked by the audit"
  - control: "the task-file copy on the branch .orchestration/dotfiles-T133-ci-efficiency-a02/task.md replaces .orchestration/dotfiles-T133-ci-efficiency-a01/task.md in the next push"
    disposition: "residual: the orchestrator owns predecessor-copy removal; the new copy is byte-identical to the dispatched a02 text, and its own sha256 is checked against the TASK and RESULT at acceptance"
  - control: task metadata
    disposition: "residual: the canonical dispatched file passes task-consistency checks C1 to C10 and C7b before dispatch and acceptance; byte comparison binds the branch copy to that file"
  - control: metadata separators
    disposition: "residual: the front matter is read as the first YAML document, and whole-file byte comparison covers separators and body as well as metadata"
  - control: in-process effects
    disposition: "residual: workflow decisions retain required check reporting; the helper writes only per-run reservations and the TSV ledger before its sole GitHub write, gh run rerun --failed; tests use fake gh"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: event and ref inputs stay quoted, actions stay pinned, permissions stay read-only, and API or parser failures prevent reruns; the existing YAML reader is reused without dependency or interpreter changes"
  - control: new or renamed scripts
    disposition: "residual: the PR introduces one rerun script and one extracted workflow, both declared in allowed_files and listed in the RESULT; additional scripts are outside this task"
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges PR 409 only through gh pr merge --squash --match-head-commit after Orchestrator Playbook step 10's final-head evidence and gate"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, so CI, the feedback sweep, local review, task-level audit and security review are refreshed before the gate"
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; ordinary removal refuses a dirty worktree, and any forced removal requires an acceptance record naming discarded state"
premises:
  - claim: none of the three workflows has a concurrency block today
    command: /usr/bin/grep -c '^concurrency:' .github/workflows/test.yaml .github/workflows/remote.yaml .github/workflows/agent-assets.yml
    output: |-
      .github/workflows/test.yaml:0
      .github/workflows/remote.yaml:0
      .github/workflows/agent-assets.yml:0
  - claim: remote.yaml runs both bootstrap jobs on pull_request today
    command: sed -n 3,9p .github/workflows/remote.yaml
    output: |-
      on:
        push:
          branches: [main]
        pull_request:
          branches: [main]
        workflow_dispatch:
        schedule:
  - claim: the required-contexts test pins the seven required check names, so item 2 cannot remove or rename a required job
    command: /usr/bin/grep -c 'def test_the_required_contexts_are_the_workflows_jobs' tests/unit/test_workflow_orchestration_skip.py
    output: |-
      1
  - claim: the ruleset requires exactly seven status checks, none of them private-bootstrap
    command: gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]|length'
    output: |-
      7
---

# AGMSG-TASK dotfiles-T133-ci-efficiency-a02 — INV-6 reset of dotfiles-T133-ci-efficiency-a01, CI efficiency (plan 024 P1-3, F5)

This redesign is written by a review-profile context other than the author of a01 under plan 006 INV-6 (S2). The audit of `27613c0c1ea978de1f0250a4a254de07fa543e98` returned `Verdict: incorrect`. The orchestrator records a01 as reset by this task before dispatch and retains its history and counts.

PR #409 continues on the same branch, `tools/ci-efficiency-a01`, under this task. The next push replaces `.orchestration/dotfiles-T133-ci-efficiency-a01/task.md` with this text's byte-identical copy at `.orchestration/dotfiles-T133-ci-efficiency-a02/task.md`. The orchestrator owns removal of the predecessor copy as reset bookkeeping. The worker's edit boundary is `allowed_files`.

The four premises preserve a01's baseline observations verbatim. They describe the state before the existing PR changes. The a01 report records the parked-PR work as completed; those actions are not repeated. The existing measurement of 30 completed pull-request runs per workflow remains the measurement baseline. The a02 `measure.md` identifies its source and measurement date and retains the tables, measured failure lines and Q4 decision.

## Goal

A pull request's newest head receives CI coverage appropriate to its changed files, superseded runs are cancelled, and all seven required contexts continue reporting. Main pushes retain the full matrix. The optional private bootstrap runs on main, schedule and dispatch. The rerun helper refuses superseded PR heads and reruns a run at most once only after every failed, timed-out or cancelled job matches a measured flake signature.

## Files

1. `.github/workflows/test.yaml`, `.github/workflows/remote.yaml` and `.github/workflows/agent-assets.yml` retain the same top-level concurrency block in block style. Its `group` is `${{ github.workflow }}-${{ github.event_name == 'pull_request' && format('pr-{0}', github.event.pull_request.number) || format('main-{0}', github.sha) }}` and its `cancel-in-progress` is `${{ github.event_name == 'pull_request' }}`. A newer PR head cancels its superseded run. Main pushes have a group per commit, and schedule and dispatch runs are never grouped with a PR. `tests/unit/test_workflow_orchestration_skip.py::test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run` checks the exact expressions in all three files.

2. `private-bootstrap` moves from `remote.yaml` to `.github/workflows/private-bootstrap.yaml`, named `Private bootstrap`, with push to `main`, the existing `0 0 * * 5` schedule and `workflow_dispatch` as its only triggers. The job remains byte-identical to the original job except for the bootstrap decision and skip message specified in item 3. Its matrix, secret conditions, isolated HOME, full action SHAs and `permissions: contents: read` remain intact. `remote.yaml` retains `public-bootstrap` as its only job. `tests/unit/test_workflow_orchestration_skip.py::test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script` checks the triggers, job placement and shared decision script.

3. The public and private bootstrap jobs use identical decision scripts. On a pull request, the existing `--no-renames` changed-file list runs the bootstrap when it is empty or contains a path matching `^(setup\.sh$|install/|home/|scripts/lib/|scripts/update-agent-assets\.sh$|scripts/gh-auth\.sh$|tests/install/|\.github/workflows/remote\.yaml$|\.github/workflows/private-bootstrap\.yaml$|\.chezmoiroot$|vendor/)`. Other PR diffs set `should_run=false`. Push, schedule and dispatch retain `should_run=true`. The `.chezmoiroot` and `vendor/` entries cover the source-root selection and vendored bootstrap assets. `test.yaml` retains its existing relevance decision and applies the macOS-only PR decision specified in item 10. Skip messages report `unrelated` or `os-independent on macos-14`. No job gains a job-level `if` or `needs`. Heavy unit-test steps retain `steps.decide.outputs.should_test == 'true'` as their only condition, and bootstrap steps retain their existing decision and secret conditions. `tests/unit/test_workflow_orchestration_skip.py::test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed` covers `scripts/x.py`, `home/x`, `install/x.sh`, `.chezmoiroot`, `vendor/`, `.orchestration/`, an empty diff and a push.

4. `.github/flakes.yaml` remains a list of `{id, job, log_regex, note}`. Each entry comes from a measured failed run whose matching line and successful retry are recorded in `measure.md`. The existing measurement supports `snapcraft-assertion-timeout` and contains no Homebrew tap flake. No unobserved Homebrew signature or generic timeout signature is added. `scripts/orchestrator/ci-rerun.sh <run-id>` remains Bash with English shdoc comments, `set -euo pipefail`, numeric argument validation, `jq` and the existing YAML-loading mechanism. It reads `gh run view <run-id> --json jobs,status,conclusion,headSha,event`, obtains each candidate job's logs, and matches its name and log against the same signature's `job` and `log_regex` using extended regular expressions. Items 7, 8 and 11 define freshness, candidate conclusions and reservation ordering. Every matched job receives one `<utc>\t<run-id>\t<headSha>\t<job>\t<signature id>` row in `.orchestration/validation/ci-reruns.tsv` before `gh run rerun <run-id> --failed`. Success exits 0; API, parser or rerun errors exit 1; usage errors or no candidate failed jobs exit 2; an unmatched job exits 3 with `real failure: <job>`; an already reserved or recorded run exits 4. API failures retain the existing normalization to exit 1. `tests/unit/test_ci_rerun.py::test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature` retains its matched, mixed-real-failure, ledger-content and repeated-call assertions. `tests/unit/test_ci_rerun.py::test_a_failing_gh_exits_1_never_with_the_scripts_own_codes` remains green.

5. `tests/unit/test_workflow_orchestration_skip.py` reads the extracted workflow through its `PRIVATE` constant. `test_the_required_contexts_are_the_workflows_jobs`, `test_no_required_contexts_job_has_a_job_level_if_or_needs`, `test_both_bootstrap_jobs_decide_with_the_same_script`, the heavy-step condition assertions and existing decision tests retain their coverage. The concurrency, trigger and path-decision tests named in items 1 to 3 remain green. The macOS test named in item 10 retains Python-and-documentation, Ubuntu, shell-change and main-push cases. Fixture lines count against the test cap.

6. `tests/unit/test_workflow_security.py` gains only `"private-bootstrap.yaml": {"contents": "read"}` in `EXPECTED_PERMISSIONS`. Every other assertion and line in that module remains unchanged. Its exact-permissions test passes with the extracted workflow, and `tests/unit/test_workflow_orchestration_skip.py::test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script` verifies the placement of the workflow that requires this expectation.

7. The superseded-head P2 is fixed in `ci-rerun.sh`. A pull-request run's associated PR and current head are read through `gh`; the current PR head must equal the run's `headSha`. Missing or ambiguous PR association, missing SHA or an unreadable response exits 1 without a rerun. A mismatch exits 3 with `superseded: run <run-id>` and never calls `gh run rerun`. The comparison occurs before reservation and is repeated immediately before the rerun request. A reservation already written remains reserved if the final comparison refuses the run. `tests/unit/test_ci_rerun.py::test_ci_rerun_refuses_a_superseded_pull_request_head` is red against `27613c0c` and green after the fix. Its fake `gh` covers an already superseded run, a current run, unavailable PR-head evidence and a head that advances during log inspection. Every refusal asserts zero rerun calls.

8. The failure-classification P2 is fixed in `ci-rerun.sh`. Jobs with conclusions `failure`, `timed_out` and `cancelled` all require a matching signature before the run can be rerun. A timeout or cancellation is never authorized by its conclusion alone. Missing logs provide no signature match and prevent the rerun. Matched timeout and cancellation jobs receive their own ledger rows. `tests/unit/test_ci_rerun.py::test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs` is red against `27613c0c` and green after the fix. It covers a matched failure mixed with an unmatched timed-out job, the corresponding cancelled case, runs containing only an unmatched timeout or cancellation, and signature-matched cases. Unmatched cases exit 3, identify the job, write no reservation or ledger rows and make zero rerun calls.

9. The production-registry P2 is fixed by `tests/unit/test_ci_rerun.py::test_the_production_flake_registry_matches_its_samples_and_no_real_failure`. This test loads the checked-in `.github/flakes.yaml` rather than the separate fake-registry fixture. Every signature has a measured sample job and log line keyed by its id. Both expressions compile with the production extended-regex engine and match that signature's own sample. No signature matches the recorded samples of real failures; negative logs are also checked with job names that satisfy the signature's job expression so a job-name mismatch cannot hide an overly broad log expression. Samples include the measured `test_validate_agent_assets` failure and a test assertion failure. The red evidence uses temporary-checkout mutations of the production registry with an invalid expression and an overly broad `.*` expression; the new test rejects each mutation. The green evidence restores the measured production registry and passes. An added signature requires its own positive sample and the same negative checks.

10. The macOS Markdown P2 is fixed in `test.yaml`. The OS-independent pattern is `^(scripts/.*\.py$|tests/unit/.*\.py$|docs/|plans/|\.orchestration/|[^/]+\.md$|ruff\.toml$|\.prettierignore$)`. The Markdown alternative accepts root-level Markdown; Markdown under `home/` or `install/` keeps macOS running. The extra skip applies only to `OS=macos-14` on a pull request whose every relevant path matches the pattern. `tests/unit/test_workflow_orchestration_skip.py::test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise` gains separate `home/.../SKILL.md` and `install/.../README.md` cases, each expecting `should_test=true`. Those cases are red against `27613c0c` and green after the fix. Root Markdown and documentation cases still skip macOS, and corresponding Ubuntu and main-push cases still run.

11. The reservation P2 is fixed in `ci-rerun.sh`. The checkout-wide `ci-reruns.lock` is replaced by persistent per-run directories under `.orchestration/validation/ci-reruns.lock.d/`. After classification and freshness checks, atomic `mkdir .orchestration/validation/ci-reruns.lock.d/<run-id>` reserves that run before ledger rows and the rerun request. The reservation remains after success, failure or interruption. A pre-existing reservation or TSV entry exits 4 without another rerun. Unrelated run ids do not contend for a shared lock, and an abandoned reservation blocks only its own run. `tests/unit/test_ci_rerun.py::test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs` is red against `27613c0c` and green after the fix. It covers concurrent calls for the same run, overlapping calls for distinct eligible runs, and an abandoned reservation with no TSV row. `tests/unit/test_ci_rerun.py::test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice` is updated to assert that both the per-run directory and every ledger row exist when fake `gh` receives the rerun request, and that a failed request retains them and prevents another attempt.

12. The evidence-count P3 is corrected in the a02 report and RESULT and in the orchestrator's acceptance record. The saved feedback JSON for `27613c0c` contains nine check runs in `checks` and one commit status represented by an item with `source: status`; seven required contexts succeeded. The unsupported `CI 13/13` claim is removed. The a02 RESULT states the final-head feedback JSON's actual check-run and commit-status counts separately and reports the seven required contexts separately. `tests/unit/test_workflow_orchestration_skip.py::test_the_required_contexts_are_the_workflows_jobs` continues pinning those seven names. The validation record pastes the JSON count calculation and required-name comparison; historical counts are identified with their historical head.

## Out of scope

Caching remains a follow-up. The inherited measurement records no qualifying test-workflow fetch or install step and identifies the public-bootstrap step for further investigation before caching. Its proposed cache key and fresh-bootstrap caveats remain in `measure.md`.

Unit-test parallelism, the Makefile, `macos.yaml`, `ubuntu.yaml`, `docs.yml`, ruleset changes, the `regime` CI job and self-hosted runners remain outside this task. Changes to other PRs and new branches are outside this reset. Historical a01 evidence remains unchanged apart from the orchestrator-owned replacement of its branch task copy. Validation uses fake `gh` for reruns and does not rerun live GitHub jobs.

## Check

`make unit-test` and `make format` run with their complete outputs and exit statuses pasted in `.orchestration/dotfiles-T133-ci-efficiency-a02/validation.md`. `shellcheck scripts/orchestrator/ci-rerun.sh` and `shfmt -d scripts/orchestrator/ci-rerun.sh` are clean. `uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security tests.unit.test_ci_rerun -v` is green.

The validation file contains the red-then-green evidence for all five P2 fixes. Behavioral regressions are demonstrated against `27613c0c`; the production-registry test demonstrates red results for the invalid and broad registry mutations and a green result for the restored production file. Recorded failures preserve the test command's actual exit status. Pre-existing whole-tree failures are identified with a comparison against the unchanged base and are never reported as passing checks. Bats tests run only in GitHub Actions.

After each push, `gh run list --branch tools/ci-efficiency-a01 --json name,event,conclusion,headSha` and `gh pr checks 409 --required` provide head-specific evidence that all seven required contexts reported successfully and no private-bootstrap workflow ran on the pull request. The final-head feedback JSON supplies the separate check-run and commit-status counts.

`git diff --numstat origin/main...HEAD` is pasted with totals of at most 330 changed lines outside `tests/`, `.orchestration/` and the moved private-bootstrap job, and at most 500 changed lines under `tests/`. Changed lines mean additions plus deletions, including test fixtures. These caps raise a01's limits by 80 lines outside tests and 150 lines under tests. The extracted private-bootstrap file and the original job's removed lines are counted separately, with both counts pasted; unrelated changes receive no move exemption.

The canonical task file passes `scripts/orchestrator/task-consistency-check.py`, including C1 to C10 and C7b. The branch task copy is compared byte for byte with the dispatched a02 text, and its SHA-256 is recorded.

## Completion

One branch, `tools/ci-efficiency-a01`, carries the work, and PR #409 continues under this task. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-ci-efficiency-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-ci-efficiency-a02/task.md>` in the RESULT. The orchestrator writes the follow-up owner task before recording any advisory disposition. The five P2 fixes specified here remain required work.

The worker writes `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, `measure.md` and worker review evidence under `.orchestration/dotfiles-T133-ci-efficiency-a02/`. Records distinguish inherited evidence from validations executed for this task. A Codex seat writes these paths relative to its own worktree and states that placement in the RESULT.

This task is `security: true` because workflow decisions governing required checks are a trust boundary. The orchestrator runs the task-level audit and a separate security-profile review on the final head before the gate. Integration follows agmsg-orchestration Orchestrator Playbook step 10, including the final-head feedback sweep, dispositions, audit, acceptance record and gate. A changed head receives refreshed evidence before integration.

No `@codex review` comment is posted. The automatic-review state and any bounded-wait outcome are recorded against the relevant head. Every `gh` write and `git` write runs as a single command, with no chained local mutation. The RESULT names the final head, base, branch, changed files, new script and workflow, every Bot thread and proposed disposition, test selectors, red and green evidence, cap totals, feedback-derived check counts, task-copy hash and evidence paths.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-ci-efficiency-a02.md: OK
premises: the a01's four, outputs pasted at write time (2026-10-18 13:3x JST)
redesigned by the codex review profile (headless, read-only) at 2026-10-18T06:52Z as the INV-6 reset of a01; checked and dispatched by the orchestrator
```

Implementation tests and live CI were not run in this read-only redesign; the final head still requires the Check, task-level audit and security review.