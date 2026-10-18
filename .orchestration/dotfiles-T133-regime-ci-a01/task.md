---
format: 2
task_id: dotfiles-T133-regime-ci-a01
kind: code
security: true
allowed_files:
  - .github/workflows/regime.yml
  - scripts/orchestrator/regime-ci.py
  - tests/unit/test_regime_ci.py
  - .orchestration/dotfiles-T133-regime-ci-a01/**
after: []
threat_table:
  - control: "the PR adds .github/workflows/regime.yml (one job on pull_request, pinned action shas, the regime-ci run on the PR head; an optional check until the operator makes it required)"
    disposition: "closed: tests/unit/test_regime_ci.py::test_the_regime_workflow_pins_its_actions_runs_on_the_pr_head_and_cancels_superseded_runs"
  - control: "the PR adds scripts/orchestrator/regime-ci.py (reads PR-controlled task copies, precheck.json and result.txt as data with yaml.safe_load and json, runs the tracked task-consistency checker on the copy as a subprocess, executes nothing the PR controls, one violation per line, exit 1)"
    disposition: "closed: tests/unit/test_regime_ci.py::test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr"
  - control: "tests/unit/test_regime_ci.py (temporary repositories with a task copy, precheck.json and result.txt; one fixture per rule; the workflow-shape test)"
    disposition: "residual: fixtures are temporary repositories built by the test; the audit reads each case and its assertion"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-regime-ci-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-regime-ci-a01/ (report.md, validation.md, sandbox.md, learning.md)"
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: regime-ci.py writes nothing and runs only git read commands and the tracked checker; the workflow runs it in a fresh runner on the PR head; no secret is read"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: the workflow pins actions/checkout and astral-sh/setup-uv by sha (the shas the other workflows use), runs on ubuntu-24.04 with uv run --no-project --with pyyaml python -I; a PR cannot change the workflow that checks it without that change appearing in its own diff, which the audit reads"
  - control: new or renamed scripts
    disposition: "residual: one new script, regime-ci.py, named here; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: none of the three new files exists on origin/main
    command: git ls-files .github/workflows/regime.yml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py | wc -l
    output: |-
      0
  - claim: the other workflows pin actions/checkout and astral-sh/setup-uv by sha, the shas regime.yml reuses
    command: "/usr/bin/grep -h 'uses: actions/checkout@\\|uses: astral-sh/setup-uv@' .github/workflows/*.yaml | sed 's/^[- ]*//' | sort -u"
    output: |-
      uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
      uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
  - claim: the task-consistency checker on main documents eleven checks (C1 to C10 and C7b), the unit rules regime-ci runs as a subprocess; C11 to C15 arrive with PR #417 and need no change here
    command: /usr/bin/grep -c '^C[0-9]*b\? ' scripts/orchestrator/task-consistency-check.py
    output: |-
      11
  - claim: the result.txt convention (plan 024 programs (4)) is not on main yet, so the precheck rule applies only when .orchestration/<task>/precheck.json exists in the PR
    command: /usr/bin/grep -c 'result.txt' scripts/orchestrator/result-precheck.sh 2>/dev/null || echo absent-on-main
    output: |-
      absent-on-main
  - claim: the ruleset's seven required contexts do not include regime, so the job starts optional (its promotion is the operator's ruleset step through P1-14's ruleset-request.sh)
    command: gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]|map(select(.=="regime"))|length'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T133-regime-ci-a01 — the regime CI job (plan 024 P1-11; programs item (6))

Written 2026-10-18 by the orchestrator seat from plan 024 (`024-todo.md` row P1-11, `024-design-programs.md` item (6), `024-design-mechanism.md` verdict conditions (1) and (5)). The job checks on GitHub what the verdict otherwise checks at acceptance: the task copy, the precheck binding, the allowed files, the caps and the threat-table unit rules. It starts as an optional check; making it required is the operator's ruleset step. Seat: a Claude seat (CI YAML and a Python script are no seat's execution boundary).

## Goal

Every pull request that carries a task copy (`.orchestration/<task>/task.md`) is checked by one GitHub job, `regime`, that fails with one line per violation and passes records-only pull requests with a "no target" line. The checks execute nothing the pull request controls.

## Files

1. `.github/workflows/regime.yml` (new): `on: pull_request` (opened, synchronize, reopened, ready_for_review); `concurrency: { group: regime-pr-${{ github.event.pull_request.number }}, cancel-in-progress: true }`; one job `regime` on `ubuntu-24.04` with `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1` (`fetch-depth: 0`, `ref: ${{ github.event.pull_request.head.sha }}`), `astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7`, and the step `uv run --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base origin/${{ github.base_ref }} --head ${{ github.event.pull_request.head.sha }}`. The design's `github.sha` is the merge commit on `pull_request` events, so the head is the PR head sha (a design correction, stated in report.md). The job name is `regime`, the context name the ruleset will take.
2. `scripts/orchestrator/regime-ci.py --base <ref> --head <sha> [--root <checkout>]` (new, Python, `python -I`, PyYAML through `uv run --no-project --with pyyaml`, the standard library otherwise, shdoc-style module docstring in English). It lists `git diff --name-only <base>...<head>` and the task directories whose `task.md` is in that list or exists at `<head>`; with none, and when every changed path is under `.orchestration/` or the head branch name starts with `orchestration/`, it prints `regime-ci: no target (records-only)` and exits 0. For each task `<t>` it checks: (a) the copy `.orchestration/<t>/task.md` passes the tracked checker, run as `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <root> <copy>` from the checkout at `<head>` (its lines are reported verbatim, prefixed `regime-ci: <t>: checker:`); (b) when `.orchestration/tasks/<t>.md` exists at `<head>`, the copy is byte-identical to it, else when `.orchestration/<t>/result.txt` exists, the copy's sha256 equals its `task_copy=` token, else the line `regime-ci: <t>: task copy unverifiable (no dispatched text at head, no result.txt)` is a warning, not a failure; (c) when `.orchestration/<t>/precheck.json` exists, its `head` equals `<head>` and its sha256 equals the `precheck=` token of `result.txt`, each mismatch a violation; when it does not exist, one warning line `regime-ci: <t>: precheck absent` (the failure form arrives with `PRECHECK_REQUIRED`, a later task); (d) every changed path matches an `allowed_files` entry of the copy's front matter (an entry ending in `/**` matches its prefix, other globs through `fnmatch` with `*` not crossing `/`, a plain entry exactly), each stray path a violation; (e) the caps: the copy's `## Check` section is parsed for `at most <n> changed lines outside <paths>` and `<m> under tests/` (backticked paths allowed; the defaults are `tests/` and `.orchestration/`), and `git diff --numstat <base>...<head>` additions plus deletions are compared, each exceeded cap a violation, a copy without a cap sentence a warning; (f) the threat-table unit rules are the checker's C4 and C7b (already covered by (a); no second implementation). Output: one line per finding on stdout in the form `regime-ci: <t>: <rule>: <detail>`, warnings prefixed `regime-ci: warning:`; exit 1 when any violation exists, else 0 with a final `regime-ci: ok <n> task(s)` line. The script reads files with `open` and `yaml.safe_load`/`json.load`, runs only `git` read commands and the tracked checker, and never evaluates, sources or executes any PR content.
3. Tests `tests/unit/test_regime_ci.py`: `test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr` (a temporary repository with a base commit holding the dispatched text and a head commit holding a consistent copy, precheck.json and result.txt: exit 0 and the ok line; then one subtest per rule, each changing one thing: a byte-different copy, a precheck head mismatch, a precheck sha mismatch, a changed path outside allowed_files, a cap exceeded by one line, a missing threat row for an entry; each subtest asserts exactly one violation line naming that rule and exit 1), `test_regime_ci_passes_a_records_only_pr_with_no_target` (changed paths all under `.orchestration/`, no task copy: the no-target line, exit 0), `test_regime_ci_warns_without_precheck_and_without_dispatched_text` (the two warning lines, exit 0), and `test_the_regime_workflow_pins_its_actions_runs_on_the_pr_head_and_cancels_superseded_runs` (parses `regime.yml` with yaml.safe_load: the two `uses:` values equal the pinned shas of premise 2, the run step names `github.event.pull_request.head.sha`, the concurrency group names the PR number with `cancel-in-progress: true`, the job id is `regime`). Fixture lines count against the test cap.
4. `report.md` states the design correction (head sha instead of `github.sha`), the two warning forms and when each becomes a failure (the dispatched text lands on main at boundaries; `PRECHECK_REQUIRED` flips after the four merge-base confirmations), and the operator's promotion step (`ruleset-request.sh` after P1-14 adds `regime` to the required contexts).

## Out of scope

Making `regime` a required check (the operator's ruleset step), `scripts/orchestrator/task-consistency-check.py` (P1-12, PR #417), `result-precheck.sh` and `result.txt` (P1-5, PR #411), `dispatch.sh` (P1-5, P1-6), `verdict.sh` (P1-4a), any other workflow file (F5, PR #409), the private-bootstrap workflow.

## Check

`make format`, `uv run python -m unittest tests.unit.test_regime_ci -v` green, `uv run --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base origin/main --head HEAD` run once on your own branch with its output pasted (your own task copy is its target; the precheck warning is expected until PR #411 merges), all pasted in `.orchestration/dotfiles-T133-regime-ci-a01/validation.md`, with `git diff --numstat origin/main...HEAD`: at most 300 changed lines outside `tests/` and `.orchestration/`, 450 under `tests/`. The job's own run on your PR is pasted from `gh run view` (its conclusion on the final head; a failure on your own PR is a finding to fix, since the PR must pass its own check).

## Completion

One PR from a fresh branch off `origin/main`. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-regime-ci-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T133-regime-ci-a01/task.md>` in the RESULT; the RESULT also carries `precheck=` when `scripts/orchestrator/result-precheck.sh` has merged (PR #411), else `precheck=pending-411`. `security: true`: the orchestrator runs the task-level audit and the security-profile review on the final head. No `@codex review` comment; single commands for every gh and git write; a classifier denial is a blocked PONG. Until P1-14 lands, any string containing the words gh pr merge or gh pr create is written with the file-edit tool, never in a Bash heredoc or echo.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-regime-ci-a01.md: OK
premises 1 to 5: outputs pasted at write time (2026-10-18 22:0x JST)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-regime-ci-a01.md
```
