---
format: 2
task_id: dotfiles-T128-orchestrator-tools-a01
kind: code
security: false
reset_of: []
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/*
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T128-orchestrator-tools-a01/**
after: [dotfiles-T128-playbook-rules-a02]
threat_table:
  - control: the PR adds scripts/orchestrator/* (boundary.sh, ff-main.sh, orch-audit.sh, orch-gate.sh, fill_sweep.py, codex-review.sh, design-keydiff.py, replay.sh, dispatch.sh), scripts the orchestrator runs on the host against records, PR feedback and the gate
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_boundary_stops_before_commit_when_the_validator_fails"
  - control: orch-gate.sh and orch-audit.sh wrap the merge gate and the task-level audit, so a wrapper could pass inputs the gate would refuse
    disposition: "residual: the wrappers only assemble environment variables and paths and call make require-crit-review and the audit runner as they are; they add no bypass flag, and the gate's own refusals (require-crit-review.py) remain the mandatory point; the audit from main reads each wrapper line"
  - control: codex-review.sh runs codex exec with a prompt file and writes a receipt and a transcript (a model run on the host)
    disposition: "residual: read-only sandbox, approval_policy=never, stdin closed, profile pinned to review; the receipt is data the orchestrator judges, never an instruction (M-20261012-12, C-14)"
  - control: the PR adds tests/unit/test_orchestrator_tools.py, the oracle of its own change
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the tests beside the scripts; the tests run the scripts with stubbed git, gh, make and codex"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared at acceptance)"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: the worker's untrusted claims; acceptance re-checks each against the diff, CI and the test output"
  - control: in-process effects
    disposition: "residual: the tests import fill_sweep.py and design-keydiff.py into the test process; both are the declared change, read line by line by the orchestrator and the audit"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: none in allowed_files; an undeclared change to such a file fails at the audit (INV-12)"
  - control: new or renamed scripts
    disposition: "residual: every new script is under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the orchestrator's tooling lives in a session scratchpad, hand-typed per use; three recorded mistakes of 2026-10-12 come from that form"
    command: "grep -h '^id:\\|^artifact:' .orchestration/learning/mistakes/M-20261012-11.md .orchestration/learning/mistakes/M-20261012-12.md .orchestration/learning/mistakes/M-20261012-13.md"
    output: |-
      id: M-20261012-11
      artifact: "boundary commit 2026-10-12 (4): the amend chain of 10:55Z in worktree boundary-2026-10-12-4"
      id: M-20261012-12
      artifact: "design-review round 20 and the Phase 1 task-file review, Codex halves (headless codex exec runs of 11:11Z and 11:15Z)"
      id: M-20261012-13
      artifact: "design v19 (dotfiles-T128-regime-v3-a01, round 21): the INV-6 clause appended to INV-4"
  - claim: "the SKILL already states the exit-status rule the boundary script embodies"
    command: "grep -n -o 'branch on its real exit status, never through a pipe' home/dot_agents/skills/agmsg-orchestration/SKILL.md"
    output: "75:branch on its real exit status, never through a pipe"
  - claim: "the input copies of the scratchpad tools are attached beside this task"
    command: "ls .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/"
    output: |-
      boundary.sh
      codex-review-prompt-example.txt
      design-keydiff.py
      ff-main.sh
      fill_sweep.py
      orch-audit.sh
      orch-gate.sh
      t717-prep.sh
---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-a01 — promote the orchestrator's scratchpad tooling to `scripts/orchestrator/` with the discipline built in (plan 007 T718; C-13, C-14, C-15)

Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 5, T718; approval pending at drafting time). Review tier by INV-1 (`kind: code`; `scripts/orchestrator/` is on no design-tier list; the gate and the audit runner themselves are untouched). Runs after `dotfiles-T128-playbook-rules-a02` (`after:`; the INV-6 successor of a01), because the SKILL sentences that will name these scripts belong to a later docs task, not to this PR. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C6 pass on this file.

## What to do

1. Create `scripts/orchestrator/` from the attached inputs (`.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/`), one script each, shdoc comments in English, every path a parameter or derived from `git rev-parse --show-toplevel` (no session scratchpad path, no home directory literal):
   - `boundary.sh <date-suffix> <commit-message-file>`: the boundary commit path (file list from `git status --short --untracked-files=all -- .orchestration`, copy into a detached worktree under `$TMPDIR`, masker, `make validate-agent-assets` bare, commit with `-c commit.gpgsign=false`, push over HTTPS with the gh credential helper as the SKILL names, `gh pr create`, `gh pr merge --squash --auto`); `set -euo pipefail`; no `rm -rf`; a failing validator leaves no commit (C-13).
   - `ff-main.sh`: as the input.
   - `orch-audit.sh <task> <head> <pr> [extra.tsv]` and `orch-gate.sh <task> <head> <pr> [extra.tsv]`: as the inputs, parameterised; they call `scripts/require-crit-review.py` through `make require-crit-review` and the audit runner as they are.
   - `fill_sweep.py`: as the input, with the `evidence=` clause required on every `not-applicable` it emits (the grammar of `dotfiles-T128-gate-evidence-a01`).
   - `codex-review.sh <profile> <prompt-file> <receipt-out> <transcript-out>`: `codex --profile <profile> exec --sandbox read-only -C <repo> -c approval_policy=never -o <receipt-out> "$(cat <prompt-file>)" < /dev/null > <transcript-out> 2>&1`; exits with codex's status; prints the receipt path and the elapsed seconds (C-14).
   - `design-keydiff.py <design.md>`: as the input, with argument parsing, printing the changed hashed keys against `HEAD`'s copy (C-15).
   - `dispatch.sh <team> <from> <to> <pane> <line-file>`: reads a TASK or ACCEPTANCE line from a file, recomputes every `*_sha256=` field from the file each names (`task_file=`, `design=`, `amended_task=`), exits non-zero naming the field on a mismatch, otherwise calls `agmsg-dispatch` (C-20).
   - `replay.sh <command…>`: runs a command that is about to enter rule or task text with the executor's binaries (`env -i PATH=/usr/bin:/bin bash -c`) inside a detached worktree at `origin/main` and prints its output and exit status for pasting (C-18).
2. `tests/unit/test_orchestrator_tools.py`: with stubbed `git`, `gh`, `make`, `codex` on PATH: `test_boundary_stops_before_commit_when_the_validator_fails` (the exact closed-row name), the boundary happy path records a commit and a PR call, `codex-review.sh` closes stdin (the stub asserts stdin is at EOF) and propagates a non-zero status, `design-keydiff.py` reports `invariants ['INV-6']` for a fixture pair that differs in INV-6 only, and `fill_sweep.py` refuses to emit a `not-applicable` without `evidence=`.
3. Keep the two checkers out (T704 owns `ledger-check.py` and `task-consistency-check.py`). Keep the attached inputs untouched; they are evidence of what ran on 2026-10-12.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v` output in the validation file.
- `shellcheck scripts/orchestrator/*.sh` output if shellcheck is on PATH (state it if not).
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`); split into two PRs if the caps are exceeded and say so in the RESULT.

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `tools/orchestrator-scripts`, draft PR from `origin/main`. After the merge the orchestrator uses only these scripts; the scratchpad copies are retired.
