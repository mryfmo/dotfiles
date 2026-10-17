---
format: 2
task_id: dotfiles-T129-doctor-sleep-disabled-a01
kind: code
security: false
allowed_files:
  - Makefile
  - scripts/check-sleep.sh
  - tests/unit/test_check_sleep.py
  - tests/unit/test_runtime_health.py
  - .orchestration/dotfiles-T129-doctor-sleep-disabled-a01/**
after: [dotfiles-T129-assets-omp-hcom-a01]
threat_table:
  - control: "the PR edits Makefile in one place (the doctor target runs the new sleep check after the tools check and folds its status into tool_status)"
    disposition: "residual: one line in the existing recipe; make doctor's exit status already aggregates its checks; the diff is read by the audit against the current target"
  - control: "the PR adds scripts/check-sleep.sh (reads pmset -g on macOS, warns on Linux, executes nothing else)"
    disposition: "closed: tests/unit/test_check_sleep.py::test_check_sleep_fails_unless_sleepdisabled_is_1_on_macos_and_warns_on_linux"
  - control: "the PR adds tests/unit/test_check_sleep.py (a stub pmset on PATH and a stub uname; red before the script exists)"
    disposition: "residual: stubs written by the test into a temporary directory; the audit reads each case against item 1"
  - control: "the PR edits tests/unit/test_runtime_health.py only in its three make-doctor fixtures (one shutil.copy of the new sleep script beside the existing check-tools copy in each; no assertion changes; Amendment 1)"
    disposition: "residual: three fixture lines; the file is also PR #388's, so this PR merges after #388 and rebases; the audit reads the diff against the current file"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-doctor-sleep-disabled-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-doctor-sleep-disabled-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the test runs the script as a subprocess with stub pmset and uname on PATH; the script reads pmset -g and writes nothing"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; make doctor runs where it runs today; the script is bash with shellcheck in CI"
  - control: new or renamed scripts
    disposition: "residual: 1 new script under scripts, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: the doctor target on origin/main runs check-tools.sh and check-agent-runtime.py and no sleep check, so item 1 adds one script and one recipe line
    command: git show origin/main:Makefile | sed -n '/^doctor:/,/^$/p' | /usr/bin/grep -cE 'check-tools|check-agent-runtime|pmset|check-sleep'
    output: |-
      2
---

# AGMSG-TASK dotfiles-T129-doctor-sleep-disabled-a01 — make doctor fails on a Mac that may sleep (plan 023 PR F, the item the monitor named)

Written 2026-10-17 by the orchestrator seat from the overnight monitor's consolidated correction of 22:40 JST (item 2, under the operator's 21:49 JST directive): an orchestrator Mac that sleeps overnight stalls every seat, so `make doctor` must say so. A separate small task rather than an F4 amendment (F4's cap has 11 lines left), to a seat the orchestrator names in the TASK line; `scripts/check-tools.sh` is PR #388's file, so the check is its own script.

## Goal

`make doctor` fails on macOS unless `pmset -g` reports `SleepDisabled 1`, and only warns on Linux.

## Files

1. `scripts/check-sleep.sh` (new, bash, shdoc comments): on `uname -s` = `Darwin`, runs `pmset -g`, finds the `SleepDisabled` line and exits 1 with `sleep check: SleepDisabled is <value>; run: sudo pmset -a disablesleep 1` unless the value is `1`; a missing line or a failing `pmset` exits 1 with the reason; on any other OS prints `sleep check: skipped (not macOS)` and exits 0. The `doctor` target in `Makefile` runs it after `./scripts/check-tools.sh` and folds its status into `tool_status` the same way.
2. `tests/unit/test_check_sleep.py` (new): `test_check_sleep_fails_unless_sleepdisabled_is_1_on_macos_and_warns_on_linux` runs the script with a stub `uname` and a stub `pmset` on PATH: `SleepDisabled 1` exits 0; `SleepDisabled 0` exits 1 naming the value and the pmset command; no line exits 1; a Linux `uname` exits 0 with the skipped line; red before the script exists.

## Out of scope

Changing the sleep setting (the operator's `sudo pmset -a disablesleep 1` or `caffeinate`); any other doctor check.

## Check

`uv run python -m unittest tests/unit/test_check_sleep.py -v` green, `shellcheck scripts/check-sleep.sh` and `shfmt -d scripts/check-sleep.sh` clean, `make doctor` run once on the worker's Mac with its output pasted (its exit status reported as is), with `git diff --numstat origin/main...HEAD`: at most 60 changed lines outside `tests/` and `.orchestration/`, 200 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main`. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-doctor-sleep-disabled-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T129-doctor-sleep-disabled-a01/task.md>` in the RESULT.

## Amendment 1 (round 1, 2026-10-17T14:1xZ)

a005's question (PONG 14:08:04Z): PR #394 (draft, head 550ebb14) fails CI's four test jobs on three existing tests of `tests/unit/test_runtime_health.py` (lines 1280 to 1360) that build a temporary repository from the Makefile, `scripts/check-tools.sh` and a stub runtime check and run `make doctor` there, so the new recipe line finds no `./scripts/check-sleep.sh` (exit 127). Option A, a005's default, is adopted: `tests/unit/test_runtime_health.py` joins `allowed_files` for one `shutil.copy` of the sleep script beside the existing check-tools copy in each of the three fixtures (three lines, one commit, no assertion change); option B (a guard that skips a missing script) is refused because a missing check would pass silently. The file is also PR #388's, so `after:` names that task: the PR merges after #388 and rebases onto main first (the monitor's finish order places it after #392). Ready the PR after the push as the Completion clause says.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-doctor-sleep-disabled-a01.md: OK
premise 1: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-doctor-sleep-disabled-a01.md
```
