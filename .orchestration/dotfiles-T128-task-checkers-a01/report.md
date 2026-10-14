---
task_id: dotfiles-T128-task-checkers-a01
seat: claude-standard-dot-a002
branch: regime/task-checkers
base: 28eec93c9a78e6a56d1f5f60ded675f521edb96f
code_commit: 612931f3
pr: 352
task_sha256: a309b3944b2dec9be6117499a98d7cc4bd7bd0026706f99525df1221fd226efb
---

# Report: dotfiles-T128-task-checkers-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `regime/task-checkers` from `origin/main` `28eec93c` (PR #350 merged), PR #352.
- Task file: amendment 2, sha256 `a309b394…`, copied byte-identical to `.orchestration/dotfiles-T128-task-checkers-a01/task.md` (validation §1). The attached inputs are untouched.
- Round 1 was dispatched at 04:14:57Z. Two questions followed:
  - 04:18Z: `test_regime_rule_sections_are_pinned_whole` pins the SKILL's invariants section against `tests/fixtures/regime/invariants.md`. This led to amendment 1, which adds that fixture.
  - 05:08Z: the macOS CI failure, and the Bot's four P1 threads, three of which change what a check means. This led to the answer to push the CI fix, then amendment 2 (05:36:34Z) for the fixes.

## Commits

| Commit | What |
|---|---|
| `c3b617a4` | Items 1 to 6 with amendment 1 |
| `63433cf1` | Task copy and first evidence; the Bot's one review was of this head |
| `1ca0d5d1` | CI fix, tests only: the stub `git` goes first inside `uv run` |
| `612931f3` | Amendment 2: the Bot's four P1 threads |
| this commit | Task copy at `a309b394` and this evidence |

## What landed

| Item | File | What it does |
|---|---|---|
| 1 | `scripts/orchestrator/task-consistency-check.py` | C1 to C10 and C7b of the input, in its order and with its messages, with one alignment (amendment 2, thread 4266930635): C4 counts an entry as named only where a row's control goes on with its end, a space, `/`, `"`, `'`, `(`, `)`, `,` or a glob character. `--root` (default `git -C <first file's directory> rev-parse --show-toplevel`; exit 2 when that fails) is where the design path resolves (C6) and the cwd of every `git` probe (C8 to C10). The docstring names each check in one line. |
| 2 | `scripts/orchestrator/ledger-check.py` | The input's rows, findings and gaps, with its output and exit, plus the gate's two counts (amendment 2): a Codex Bot `review` body with a `![P<n> Badge]` token, keyed `pullrequestreview-<id>` (thread 4266930617), and audit lines matching the gate's `AUDIT_FINDING` regex verbatim (4266930623). |
| 3 | `scripts/orchestrator/orch-audit.sh` | The ledger check runs on every audit: `check` defaults to `$(cd -- "$(dirname -- "$0")" && pwd)/ledger-check.py`, resolved before the script's `cd` to the checkout root. An explicit `--ledger-check` must still be tracked (exit 2, refusal text unchanged), and a gap still exits 3 before codex runs. |
| 4 | `tests/unit/test_task_checkers.py` (new), `tests/unit/test_orchestrator_tools.py`, `tests/unit/test_agmsg_orchestration_docs.py` | The cases item 4 names; see below. |
| 5 | `tests/fixtures/lessons/` (4 files) | Copies from `origin/main` (validation §7); no home path. |
| 6 | `home/dot_agents/skills/agmsg-orchestration/SKILL.md` and `tests/fixtures/regime/invariants.md` | The line-73 and line-71 sentences, verbatim, in both files (amendment 1). |

Notes on meaning:

- Against the input, run from the worktree over every task file:
  - The 86 format-2 files differ by exactly four added C4 lines, the amendment-2 rule (validation §6).
  - The other 309 files raise the same exception as the input.
- On the ten historical files, the amended checker's sets equal premise 1, so item 4's table is unchanged.
  - The four added C4 lines fall in three files whose sets already held C4: process-rules-a02, regime-counters-a01 and regime-counters-a02.
  - Each entry is named only in a disposition, never in a control. The amended rule reads the control text, and validation §6 pastes each disposition excerpt.
- C9 maps the `task-consistency-check C<n>` form to the probe `scripts/task-consistency-check.py`, the input's string. The script lands at `scripts/orchestrator/`, so that form never finds it on `origin/main`. I kept the string as the task's meaning; it is a T705 candidate (learning 4).
- `ledger-check.py` keeps the input's behaviour on missing arguments, a traceback with exit 1. `orch-audit.sh` reads that as an incomplete ledger, so it fails closed.

## Tests

The Check command: 94 tests OK (validation §3). The checker cases:

- **`..._detects_the_ten_historical_files`:** the amended checker's sets, which equal premise 1.
- **`..._passes_a_complete_task_file`:** `OK` under a temporary `--root`. Then a changed design receipt gives C6, so the design resolves under `--root` (mutation M7).
- **`..._reaches_every_other_check`:** item 4's six checks, plus one entry beyond its text, C2's other-directory branch (mutation M3).
- **`..._c4_names_an_entry_only_at_a_path_boundary`** (amendment 2): `scripts/foo.py.bak` leaves `scripts/foo.py` to C4. The end, a space, `/`, `)`, `"`, `,` and `*` each name it, one case each.
- **`test_ledger_check_reports_the_gaps_of_the_pre_fix_record`:** `findings 36; gaps 36`. The a05 fixtures hold no badged review body and no bulleted line.
- **`test_ledger_check_passes_a_complete_record`:** `gaps 0`, then one `GAP` line. Its audit lines are `[P0]` and `[P3]`.
- **`test_ledger_check_counts_what_the_gate_counts`** (amendment 2): a badged Codex review body and a `- [P1]` line give `findings 2` and two `GAP` lines. An unbadged Bot review and another author's badged review are not findings.
- **`test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap`:** exit 3 before codex, with the sweep and ledger checks really run through a `.python-version` shim. An untracked `--ledger-check` is still refused with exit 2.
- **The two docs tests:** assert the new sentences and the absence of the superseded ones.

Mutation pass: 27 mutations, 27 caught (validation §8), covering:

- each check and both exits;
- `--root`;
- the ledger parts and the three pre-fix forms of amendment 2 (F1 to F3);
- a dot taken as a C4 boundary (F4);
- the three `orch-audit.sh` behaviours;
- both SKILL sentences.

## Replay and caps

- Replay: 15 `OK` of 86 format-2 files with either grep (validation §5). This task's own file, at amendment 2, is `OK` from the main checkout.
- Caps (validation §9; amendment 2 lets the 200-line practice cap yield within INV-2's 500):
  - outside `tests/` and `.orchestration/`: 4 files, 194 added + 10 deleted = 204 changed lines;
  - under `tests/`: 752 added lines (cap 1000);
  - 12 files outside `.orchestration/`.

## CI and the Bot

- **The Bot:** one review, at `gh pr ready` (04:52:25Z), of `63433cf1`. It raised four P1 threads, each `fixed:612931f3` (the table in validation §10). The Security Review finished with no comment. The fix heads got no new Bot wait, by the task's once-at-open rule.
- **CI on `c3b617a4` and `63433cf1`:** `test (macos-14, client)` failed two checker tests. `uv run` puts its base interpreter's `bin` before the caller's PATH, and on the macOS runner a real `git` sits there.
  - This is inferred from the local PATH listing and from the failure pattern; it was not reproduced, because the reproduction command was denied (sandbox record).
  - `1ca0d5d1` sets the stub first inside `uv run`, and its CI is 13 of 13 green.
- **CI on the final head:** in the RESULT.

## Not done, or outside scope

- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
