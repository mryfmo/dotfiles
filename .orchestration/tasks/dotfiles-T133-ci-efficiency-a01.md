---
format: 2
task_id: dotfiles-T133-ci-efficiency-a01
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
  - .orchestration/dotfiles-T133-ci-efficiency-a01/**
after: []
threat_table:
  - control: "the PR edits .github/workflows/test.yaml in two places (item 1: the concurrency block; item 3: the decide step's should_test becomes false on macos-14 when the diff is OS-independent; the job still reports success or failure, no job-level if or needs, every heavy step keeps its decision)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise"
  - control: "the PR edits .github/workflows/remote.yaml in three places (item 1: the concurrency block; item 2: the private-bootstrap job leaves this file; item 3: the public-bootstrap decide step skips when no bootstrap path changed; the job still reports)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed"
  - control: "the PR adds .github/workflows/private-bootstrap.yaml (item 2: the private-bootstrap job moved byte for byte except its triggers, which are push to main, schedule and workflow_dispatch, never pull_request; it is not a required check)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script"
  - control: "the PR edits .github/workflows/agent-assets.yml in one place (item 1: the concurrency block)"
    disposition: "closed: tests/unit/test_workflow_orchestration_skip.py::test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run"
  - control: ".github/flakes.yaml (new; data: known flake signatures, each an id, a job name pattern, a log regular expression and a note)"
    disposition: "closed: tests/unit/test_ci_rerun.py::test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature"
  - control: "the PR adds scripts/orchestrator/ci-rerun.sh (item 4: reads a run's failed jobs and their logs through gh, matches them against the flake file, reruns the failed jobs once and records the rerun; a non-matching failure exits 3 without a rerun)"
    disposition: "closed: tests/unit/test_ci_rerun.py::test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature"
  - control: "tests/unit/test_workflow_orchestration_skip.py (the existing workflow reader and decision tests adapted to the moved job and the two new decisions)"
    disposition: "residual: the tests run the decide scripts with real git on temporary repositories as today; the required-contexts and no-job-level-if tests keep their assertions"
  - control: "tests/unit/test_ci_rerun.py (new; a fake gh on PATH answers run, job and log queries from fixtures and records every argv)"
    disposition: "residual: fakes only; no live GitHub"
  - control: "the PR edits tests/unit/test_workflow_security.py in one line (Amendment 1: EXPECTED_PERMISSIONS gains the row private-bootstrap.yaml: contents read; every other assertion of the module unchanged)"
    disposition: "residual: one expected value for the moved workflow; the audit reads the diff against the current file"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-ci-efficiency-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-ci-efficiency-a01/ (report.md, validation.md, sandbox.md, learning.md, the item 0 measurement table)"
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the workflows change only which steps run and which runs are cancelled; the seven required contexts keep reporting success or failure in every event; ci-rerun.sh's one write is gh run rerun --failed, recorded in .orchestration/validation/ci-reruns.tsv"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: the workflow files are the change under review, read against the GitHub Actions documentation for concurrency and required checks (plan 024 5.9); every action stays pinned to its full sha and the permissions blocks are untouched (tests/unit/test_workflow_security.py keeps passing with Amendment 1's one expected row); no interpreter file changes"
  - control: new or renamed scripts
    disposition: "residual: 1 new script under scripts/orchestrator and 1 new workflow, both named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
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

# AGMSG-TASK dotfiles-T133-ci-efficiency-a01 — CI for many concurrent PRs (plan 024 P1-3, F5: concurrency, private-bootstrap off pull requests, in-job skips, flake signatures)

Written 2026-10-18 by the orchestrator seat from plan 024 (wave P-W0, `024-todo.md` row P1-3, `024-design-quality.md` 5.9 Q1 to Q9 and 5.10 M9, `024-design-programs.md` item (11)). Seat: claude-standard-dot-a011 (worker-d). Four seats pushing at once saturate the five macOS runners (10 jobs and 3 macOS per PR head today, median wall time 10 minutes, macOS queue up to 26 minutes); the seven required checks stay, main's push keeps the full matrix, and a PR runs only its newest head.

## Item 0 (first): finish the parked PRs and measure

(a) Your worktree holds `tools/make-update-followups-a01` (PR #405, draft) with the untracked evidence directory `.orchestration/dotfiles-T132-make-update-followups-a01/`: commit it on that branch, push, `gh pr ready 405`, and `gh pr ready 402` (PR #402's evidence is already in its tree). When #405's required checks are green and the Bot's review of its head is in (the wait of Worker Playbook step 15, run in the background while you work on item 1), send the `AGMSG-RESULT` for `dotfiles-T132-make-update-followups-a01` as its task text says, with the evidence paths in that PR. (b) Measure before changing anything: for the last 30 completed `test.yaml` and `remote.yaml` runs on pull requests, `gh api 'repos/mryfmo/dotfiles/actions/runs?per_page=30&event=pull_request' --jq` the `created_at`, `run_started_at`, `updated_at` of each run and `gh api repos/mryfmo/dotfiles/actions/runs/<id>/jobs --jq` each job's `started_at`, `completed_at` and each step's duration; paste a table (per workflow: run wall-time median, queued median, per-job median, the three longest steps) into `.orchestration/dotfiles-T133-ci-efficiency-a01/measure.md`. From it decide Q4: a fetch or install step with median over 60 seconds gets `actions/cache` in a follow-up task (name the step and the key you would use; do not add the cache in this PR), otherwise record "no cache". Then `git switch -c tools/ci-efficiency-a01 --no-track origin/main`.

## Goal

A pull request's CI runs once per newest head, exercises the bootstrap and the macOS matrix only when the diff can affect them, and leaves the non-required private bootstrap to main and the schedule; a known flake is rerun once by a script that records it, and never a real failure.

## Files

1. Concurrency (Q1) in `test.yaml`, `remote.yaml` and `agent-assets.yml`, the same block in each: `concurrency: { group: ${{ github.workflow }}-${{ github.event_name == 'pull_request' && format('pr-{0}', github.event.pull_request.number) || format('main-{0}', github.sha) }}, cancel-in-progress: ${{ github.event_name == 'pull_request' }} }` written in block style; a PR's superseded head is cancelled, a main push runs to completion per commit (so a red main names its commit), schedule and dispatch runs are never grouped with a PR.
2. `private-bootstrap` leaves `remote.yaml` for the new `.github/workflows/private-bootstrap.yaml` (Q2), the job text byte for byte, the workflow `name: Private bootstrap`, `on: push: branches: [main]`, `schedule` (the same cron) and `workflow_dispatch`, the same `permissions: contents: read`, the same pinned actions; its decide step stays as it is (the test that both bootstrap jobs decide with the same script now reads the two files). `remote.yaml` keeps `public-bootstrap` as the only job; nothing else in it changes beyond items 1 and 3.
3. In-job skips (Q3). `public-bootstrap`'s decide step (both files share the script, so edit it identically in `private-bootstrap.yaml`) sets `should_run=false` on a pull request whose changed files (the existing `--no-renames` diff) contain no path matching `^(setup\.sh$|install/|home/|scripts/lib/|scripts/update-agent-assets\.sh$|scripts/gh-auth\.sh$|tests/install/|\.github/workflows/remote\.yaml$|\.github/workflows/private-bootstrap\.yaml$|\.chezmoiroot$|vendor/)` (Amendment 2 adds the last two: chezmoi reads `.chezmoiroot` and the bootstrap installs vendored assets); an empty diff still runs; push, schedule and dispatch still run. `test.yaml`'s decide step keeps `should_test` as computed today and, only when `OS` is `macos-14` and the event is a pull request, sets it to `false` when every relevant changed file matches `^(scripts/.*\.py$|tests/unit/.*\.py$|docs/|plans/|\.orchestration/|.*\.md$|ruff\.toml$|\.prettierignore$)` (a shell, install, home, bats, Makefile or workflow change keeps macOS running); the skip step's message names the reason (`unrelated` or `os-independent on macos-14`). No step or job gains a job-level `if` or `needs`; every heavy step keeps `steps.decide.outputs.should_test == 'true'` as its only condition (the existing test asserts this).
4. `.github/flakes.yaml` (new): a list of `{id, job, log_regex, note}` seeded with the macOS Homebrew tap warning and the network timeout patterns you find in the measured failed runs of item 0 (paste the matching log lines in measure.md; an empty list is valid when none is found). `scripts/orchestrator/ci-rerun.sh <run-id>` (new, bash, shdoc, `set -euo pipefail`, `jq`): `gh run view <run-id> --json jobs,status,conclusion,headSha,event`; for each job with `conclusion: failure`, `gh run view <run-id> --job <job-id> --log-failed`; a job matches when its name matches a signature's `job` and its log matches `log_regex`; when every failed job matches, reserve the run first (Amendment 2: an atomic `mkdir .orchestration/validation/ci-reruns.lock.d/<run-id>` and the `<utc>\t<run-id>\t<headSha>\t<job>\t<signature id>` rows appended to `.orchestration/validation/ci-reruns.tsv` before the rerun), then `gh run rerun <run-id> --failed` once; a failed rerun exits 1 and keeps the reservation, so a crash or a concurrent call never reruns twice; exit 0 on success; when any failed job matches nothing, exit 3 with `real failure: <job>` and no rerun; a run already listed in the TSV is never rerun again (exit 4). Tests in `tests/unit/test_ci_rerun.py` with a fake gh: `test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature` (match → one rerun and one TSV row per job; one non-matching job → exit 3 and no rerun; a second call on the same run → exit 4 and no rerun).
5. `tests/unit/test_workflow_orchestration_skip.py`: the module constants gain the private-bootstrap workflow; `test_the_required_contexts_are_the_workflows_jobs`, `test_no_required_contexts_job_has_a_job_level_if_or_needs` (now reading private-bootstrap from its file), `test_both_bootstrap_jobs_decide_with_the_same_script` (two files) and the existing decision tests keep passing; new: `test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run` (reads the concurrency blocks: the group expression and `cancel-in-progress` exactly as item 1), `test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script` (the `on:` keys of the new file; no `pull_request`), `test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed` (temporary repositories: a `scripts/x.py` change skips, a `home/x` change runs, an `install/x.sh` change runs, an `.orchestration/` change skips, an empty diff runs, push runs), `test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise` (`OS=macos-14` with a `.py` and `.md` diff gives `should_test=false`; the same diff with `OS=ubuntu-24.04` gives true; a `home/x.sh` diff gives true on both). Fixture lines count against the test cap.

## Out of scope

Caching (Q4, decided in item 0, implemented in a follow-up), unit-test parallelism, the Makefile, `macos.yaml`, `ubuntu.yaml`, `docs.yml`, the ruleset (the operator's), the `regime` CI job (P1-11), self-hosted runners (plan 024 5.8 S3 rejects them).

## Check

`make unit-test`, `make format`, `shellcheck` and `shfmt -d` on `ci-rerun.sh` clean, `uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security tests.unit.test_ci_rerun -v` green, and, after the push, `gh run list --branch tools/ci-efficiency-a01 --json name,event,conclusion` showing the seven required contexts reported on the head and no `private-bootstrap` run on the pull request, all pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 250 changed lines outside `tests/`, `.orchestration/` and the moved private-bootstrap job (count that file's lines separately and paste both), 350 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after item 0. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-ci-efficiency-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T133-ci-efficiency-a01/task.md>` in the RESULT. This task is `security: true` (CI that decides required checks is a trust boundary): the orchestrator runs the task-level audit and a second review on the `security` profile on the final head before the gate (plan 024 5.11 Q-A).

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-ci-efficiency-a01.md: OK
premises 1 to 4: outputs pasted at write time (2026-10-18 13:3x JST)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-ci-efficiency-a01.md
```

## Amendment 1 (round 1, 2026-10-18T04:34Z)

a011's question PONG (04:29:22Z): `tests/unit/test_workflow_security.py` pins the exact top-level permissions of every workflow file (`EXPECTED_PERMISSIONS`, lines 8 to 15), so the new `private-bootstrap.yaml` of item 2 fails `test_workflows_have_exact_top_level_permissions` until one row is added. Authorized: the file joins `allowed_files` with its row; the one added line is `"private-bootstrap.yaml": {"contents": "read"}` in that mapping; nothing else in the module changes. The decision is the orchestrator's by default (an `allowed_files` touch point grep found after dispatch; no operator round).

## Amendment 2 (round 1, 2026-10-18T05:46Z) and the orchestrator's revise round 1

a011's RESULT (05:44:40Z, PR #409 at 7779e78b): the Bot's review 5561618690 left two P2 on this PR's own change, both small and within `allowed_files` (the Completion clause's revise case, C-50): 4305896433, the bootstrap path gate misses `.chezmoiroot` and `vendor/`; 4305896435, `ci-rerun.sh` records the rerun after calling it, so a crash or a concurrent call can rerun twice. Authorized as the orchestrator's revise round 1 (INV-6 revises 0 to 1): item 3's pattern gains `\.chezmoiroot$|vendor/` in both bootstrap workflows with two cases in `test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed`; item 4 reserves the run (an atomic `mkdir` lock directory under the validation directory and the TSV rows) before `gh run rerun`, a failed rerun exits 1 keeping the reservation, with one test `test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice` (red on 7779e78b: a fake gh whose rerun fails leaves no row there and a second call reruns again). INV-6: amendments 2 (the first added a touch point, this one answers the Bot's first review), revises 1; a further amendment or revise on this task is a hold and a re-plan. `check=tests/unit/test_workflow_orchestration_skip.py::test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed` and `check=tests/unit/test_ci_rerun.py::test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice`. Copy this text as task.md, push once as single commands, wait for CI and the automatic review (no `@codex review` comment), then RESULT with `previous_head=7779e78b529b87aa52638a20456393f48407d409` in `.orchestration/<task>/revise.yaml`.
