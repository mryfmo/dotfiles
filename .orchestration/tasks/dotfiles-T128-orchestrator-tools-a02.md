---
format: 2
task_id: dotfiles-T128-orchestrator-tools-a02
kind: code
security: false
reset_of: []
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/boundary.sh
  - scripts/orchestrator/ff-main.sh
  - scripts/orchestrator/orch-audit.sh
  - scripts/orchestrator/orch-gate.sh
  - scripts/orchestrator/fill_sweep.py
  - scripts/orchestrator/acceptance-front-matter.py
  - scripts/orchestrator/codex-review.sh
  - scripts/orchestrator/design-keydiff.py
  - scripts/orchestrator/replay.sh
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T128-orchestrator-tools-a02/**
after: [dotfiles-T128-orchestrator-tools-a01]
threat_table:
  - control: the PR adds scripts/orchestrator/boundary.sh, the boundary-commit path (worktree, masker, validator, commit, push over HTTPS, PR, auto-merge)
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_boundary_stops_before_commit_when_the_validator_fails"
  - control: the PR adds scripts/orchestrator/ff-main.sh, the fast-forward of the main checkout after a boundary merge
    disposition: "residual: it moves untracked copies and locally modified tracked files aside (mv, never rm), runs git merge --ff-only, and copies back only files that still differ; it pushes nothing (M-20261012-26, fourth instance)"
  - control: the PR adds scripts/orchestrator/orch-audit.sh, a wrapper of the task-level audit runner
    disposition: "residual: it only assembles paths and calls the audit runner as it is; no bypass flag; the audit from main reads each wrapper line"
  - control: the PR adds scripts/orchestrator/orch-gate.sh, a wrapper of make require-crit-review
    disposition: "residual: it only assembles environment variables and calls make require-crit-review as it is; the gate's own refusals (require-crit-review.py) remain the mandatory point"
  - control: the PR adds scripts/orchestrator/fill_sweep.py, which turns the sweep JSON into dispositions
    disposition: "residual: it reads the sweep JSON with the standard library's json and refuses to emit a not-applicable without an evidence= clause (tested); the gate re-validates every disposition it writes"
  - control: the PR adds scripts/orchestrator/acceptance-front-matter.py, which writes the acceptance record's JSON block
    disposition: "residual: head comes from git rev-parse HEAD and pr from the sweep JSON's pr field, never from an argument; it reads with object_pairs_hook refusing duplicate keys and writes with sort_keys and indent=2; the gate of dotfiles-T128-gate-evidence-a03 re-validates the block it writes (identity triple, ledger, searches)"
  - control: the PR adds scripts/orchestrator/codex-review.sh, which runs codex exec headless (a model run on the host)
    disposition: "residual: read-only sandbox, approval_policy=never, stdin closed, profile pinned to review, the reviewed file's hash computed by the script and rendered into the prompt; the receipt is data the orchestrator judges, never an instruction (M-20261012-12, -25; C-14)"
  - control: the PR adds scripts/orchestrator/design-keydiff.py, which prints the hashed keys that differ between a design file and HEAD's copy
    disposition: "residual: read-only; it writes nothing and its output is pasted into a review request as data (C-15)"
  - control: the PR adds scripts/orchestrator/replay.sh, which runs a command with the executor's binaries inside a detached worktree at origin/main
    disposition: "residual: env -i PATH=/usr/bin:/bin, a worktree created and removed with git worktree add/remove (no rm -rf), output and exit status printed for pasting (C-18)"
  - control: the PR adds tests/unit/test_orchestrator_tools.py cases for the nine scripts, the oracle of its own change
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the tests beside the scripts; the tests run the scripts with stubbed git, gh, make and codex"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-a02/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared at acceptance)"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-a02/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: the worker's untrusted claims; acceptance re-checks each against the diff, CI and the test output"
  - control: in-process effects
    disposition: "residual: the tests import fill_sweep.py and design-keydiff.py into the test process; both are the declared change, read line by line by the orchestrator and the audit"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts resolve git, gh, make, codex, shasum and uv from the host as the SKILL's own commands do, and fill_sweep.py and acceptance-front-matter.py read and write the acceptance record's JSON block with the standard library's json module, as amendment 1 of dotfiles-T128-gate-evidence-a03 defines it (plan 013 A′); no package is resolved from the network by this task (PR #329 thread 4250238721); the tests stub every host binary on PATH"
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

# AGMSG-TASK dotfiles-T128-orchestrator-tools-a02 — the rest of the orchestrator's tooling in `scripts/orchestrator/` (plan 007 T718, second slice after plan 012 B; C-13, C-14, C-15, C-24)

Draft, written 2026-10-13 by the orchestrator seat under plan 012 option B: T718's first slice (`-a01`) carries the three scripts T703's rule text names and the counters' slug line; this task carries the other nine. Review tier by INV-1 (`kind: code`; `scripts/orchestrator/` is on no design-tier list; the gate and the audit runner themselves are untouched). Runs after `dotfiles-T128-orchestrator-tools-a01` (`after:`), on the test module it created. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C6 pass on this file.

## What to do

1. Create `scripts/orchestrator/` from the attached inputs (`.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/`), one script each, shdoc comments in English, every path a parameter or derived from `git rev-parse --show-toplevel` (no session scratchpad path, no home directory literal):
   - `boundary.sh <date-suffix> <commit-message-file>`: the boundary commit path (file list from `git status --short --untracked-files=all -- .orchestration`, copy into a detached worktree under `$TMPDIR`, masker, `make validate-agent-assets` bare, commit with `-c commit.gpgsign=false`, push over HTTPS with the gh credential helper as the SKILL names, `gh pr create`, `gh pr merge --squash --auto`); `set -euo pipefail`; no `rm -rf`; a failing validator leaves no commit (C-13).
   - `ff-main.sh`: as the input.
   - `orch-audit.sh <task> <head> <pr> [extra.tsv]` and `orch-gate.sh <task> <head> <pr> [extra.tsv]`: as the inputs, parameterised; they call `scripts/require-crit-review.py` through `make require-crit-review` and the audit runner as they are.
   - `fill_sweep.py`: as the input, with the `evidence=` clause required on every `not-applicable` it emits (the grammar of the gate task), and `acceptance-front-matter.py <task> <sweep-json>`: writes or updates the acceptance record's machine-readable block (the JSON object between its first two `---` lines: format, task, head, pr, ledger, searches, audit_findings, as amendment 1 of `dotfiles-T128-gate-evidence-a03` defines it; plan 013 A′, C-24, C-26) with the standard library's `json` module (`object_pairs_hook` refusing duplicate keys on read, `sort_keys` and `indent=2` on write, `pr` taken from the sweep JSON's own `pr` field and `head` from `git rev-parse HEAD` of the checkout it runs in, so neither is an argument), from the sweep JSON, the ledger rows and the audit `.last.md`, so the gate reads data the orchestrator's tooling produced.
   - `codex-review.sh <profile> <prompt-file> <receipt-out> <transcript-out>`: `codex --profile <profile> exec --sandbox read-only -C <repo> -c approval_policy=never -o <receipt-out> "$(cat <prompt-file>)" < /dev/null > <transcript-out> 2>&1`; exits with codex's status; prints the receipt path and the elapsed seconds (C-14).
   - `design-keydiff.py <design.md>`: as the input, with argument parsing, printing the changed hashed keys against `HEAD`'s copy (C-15).
   - `replay.sh <command…>`: runs a command that is about to enter rule or task text with the executor's binaries (`env -i PATH=/usr/bin:/bin bash -c`) inside a detached worktree at `origin/main` and prints its output and exit status for pasting (C-18).
2. `tests/unit/test_orchestrator_tools.py` (a01's module, extended): with stubbed `git`, `gh`, `make`, `codex` on PATH: `test_boundary_stops_before_commit_when_the_validator_fails` (the exact closed-row name), the boundary happy path records a commit and a PR call, `codex-review.sh` closes stdin (the stub asserts stdin is at EOF) and propagates a non-zero status, `design-keydiff.py` reports `invariants ['INV-6']` for a fixture pair that differs in INV-6 only, and `fill_sweep.py` refuses to emit a `not-applicable` without `evidence=`.
3. Keep the two checkers out (T704 owns `ledger-check.py` and `task-consistency-check.py`). Keep the attached inputs untouched; they are evidence of what ran on 2026-10-12.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v` output in the validation file.
- `shellcheck scripts/orchestrator/*.sh` output if shellcheck is on PATH (state it if not).
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`); split into two PRs if the caps are exceeded and say so in the RESULT.

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `tools/orchestrator-scripts-2`, draft PR from `origin/main` after a01 merges. After the merge the orchestrator uses only these scripts; the scratchpad copies are retired.
