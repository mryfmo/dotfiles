---
task_id: dotfiles-T128-task-checkers-a01
seat: claude-standard-dot-a002
branch: regime/task-checkers
base: 28eec93c9a78e6a56d1f5f60ded675f521edb96f
code_commit: c3b617a4
pr: 352
task_sha256: cd00812f4a3cd64d841d5a96c7720e33be904e9cabb2cf70d31ccad8580b6a2d
---

# Report: dotfiles-T128-task-checkers-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `regime/task-checkers` from `origin/main` `28eec93c` (PR #350 merged), PR #352.
- Task file: amendment 1, sha256 `cd00812f…`, copied byte-identical to `.orchestration/dotfiles-T128-task-checkers-a01/task.md` (validation §1). The attached inputs are untouched (their hashes match the task text).
- Round 1 dispatched at 04:14:57Z. At 04:18Z I asked (`AGMSG-PONG status=question`): `test_regime_rule_sections_are_pinned_whole` compares the SKILL's invariants section with `tests/fixtures/regime/invariants.md` byte for byte, so item 6 could not pass outside `allowed_files`. Amendment 1 (04:35:53Z) added the fixture; nothing was pushed before it.

## What landed (`c3b617a4`)

| Item | File | What it does |
|---|---|---|
| 1 | `scripts/orchestrator/task-consistency-check.py` | C1 to C10 and C7b of the input, in the input's order and with its messages. `--root` (default `git -C <first file's directory> rev-parse --show-toplevel`; exit 2 when that fails) is where the design path resolves (C6) and the cwd of every `git` probe (C8 to C10). Docstring names each check in one line. |
| 2 | `scripts/orchestrator/ledger-check.py` | The input's rows, findings and gaps, with its output and exit. |
| 3 | `scripts/orchestrator/orch-audit.sh` | The ledger check runs on every audit: `check` defaults to `$(cd -- "$(dirname -- "$0")" && pwd)/ledger-check.py`, resolved before the script's `cd` to the checkout root, so a relative `$0` still names the sibling. An explicit `--ledger-check <script>` must still be tracked (exit 2, the refusal text unchanged); a gap still exits 3 with "the ledger is incomplete" before codex runs. The `@description` and `@option` lines say so. |
| 4 | `tests/unit/test_task_checkers.py` (new), `tests/unit/test_orchestrator_tools.py`, `tests/unit/test_agmsg_orchestration_docs.py` | The cases item 4 names; see below. |
| 5 | `tests/fixtures/lessons/` (4 files) | Copies from `origin/main`: the ten front matters, each after a `# <task_id>` line; the record and the audit `.last.md` byte-identical; the sweep as the same object on one line (validation §7). No home path. |
| 6 | `home/dot_agents/skills/agmsg-orchestration/SKILL.md` and `tests/fixtures/regime/invariants.md` | The line-73 and line-71 sentences, verbatim as item 6 gives them, in both files (amendment 1). Nothing else changes. |

Choices inside "unchanged in meaning":

- The port's only behaviour change is where it resolves: the design path and the `git` cwd come from `--root` instead of the current directory. On every task file of the worktree, run from the worktree, the port prints what the input prints: all 86 format-2 files give the same lines, and the other 309 raise the same exception (validation §6; outputs are sorted, because C9 and C10 walk Python sets in either version).
- C9 maps the `task-consistency-check C<n>` form to the probe `scripts/task-consistency-check.py`, the input's string. The script lands at `scripts/orchestrator/`, so that form never finds it on `origin/main`. I kept the string because the task forbids a change of meaning; it is a T705 candidate (learning 4). None of the six cases or the ten files reaches that form.
- `ledger-check.py` keeps the input's behaviour on missing arguments (a Python traceback, exit 1), which `orch-audit.sh` reads as an incomplete ledger: it fails closed.

## Tests

The Check command: 92 tests OK (validation §3).

- `test_task_consistency_check_detects_the_ten_historical_files`: the ten files of item 5a under `--root` the repository; the failing check ids per file equal premise 1 exactly.
- `test_task_consistency_check_passes_a_complete_task_file`: `OK` under a temporary `--root`, the stub answering present and found, and a body naming `REVIEW_EVIDENCE` so the C8 probe runs. Beyond item 4's text: the same file is checked again after the design's receipt changes, and C6 appears. This shows the design resolves under `--root`, not the cwd, and it catches mutation M7.
- `test_task_consistency_check_reaches_every_other_check`: the six files item 4 names (C1, C5, C7b, C8, C9, C10, each at most 5 lines). Beyond item 4's text: one more entry, C2's other branch (an `allowed_files` entry under another task's directory). The ten reach only C2's missing-own-directory branch, and mutation M3 survived without it.
- `test_ledger_check_reports_the_gaps_of_the_pre_fix_record`: `ledger rows 0; findings 36; gaps 36`, 36 `GAP` lines, exit 1.
- `test_ledger_check_passes_a_complete_record`: 4 rows, `gaps 0`, exit 0; one row removed gives one `GAP` line, exit 1. The audit's lines are `[P0]` and `[P3]`, the two ends of the class, so mutation L3 is caught.
- `test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap`: with no `--ledger-check`, a record missing one of two ids exits 3 before codex runs. The sweep check and the ledger check really run: the `uv` stub executes a `.python-version` shim that runs python. Beyond item 4's text: two closing lines show that an untracked `--ledger-check` override is still refused with exit 2 (mutation A3).
- `test_rule_changes_travel_as_task_amendments` and `test_threat_table_rows_have_a_fixed_unit`: the assertions move to the new sentences, and each superseded sentence is asserted absent. The second test's existing stale string stays.

Mutation pass: 23 mutations, 23 caught (validation §8), covering each check, both exits, `--root`, the ledger parts, the three `orch-audit.sh` behaviours and both SKILL sentences.

## Replay and caps

- Replay (validation §5): 15 `OK` of 86 format-2 files in `.orchestration/tasks/`, with the Check's `grep` (a ugrep wrapper in this shell) and with `/usr/bin/grep` alike. This task's own file is not under the worktree's `.orchestration/tasks/` (it is not on `origin/main`); checked from the main checkout it is `OK`.
- Caps (validation §9): outside `tests/` and `.orchestration/`, 4 files with 188 added + 10 deleted = 198 changed lines (cap 200). Under `tests/`, 725 added lines (cap 1000). 12 files outside `.orchestration/`. Nothing was shortened under `tests/`. To fit the 200, the scripts were tightened before the first commit: long literals assigned to names, one `git()` helper, and one `print` with `sep` in place of loops. Every message is kept.

## Bot, CI and not done

- CI and the Bot round on PR #352: validation §10 and the RESULT.
- The full `tests/unit` discover is left to CI.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
