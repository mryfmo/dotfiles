---
task_id: dotfiles-T128-task-checkers-followup-a01
seat: claude-standard-dot-a002
branch: tools/task-checkers-followup
base: f0faa33a
code_commit: d99b6458
pr: 365
task_sha256: 506fa2ce4da29aaa64f67c02b5fbaa92eee40fb0fc0c65070aaf0a3b63a69442
---

# Report: dotfiles-T128-task-checkers-followup-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/task-checkers-followup` from `origin/main` `f0faa33a` (after PR #361), PR #365.
- Task file: sha256 `506fa2ce…`, copied byte-identical to `.orchestration/dotfiles-T128-task-checkers-followup-a01/task.md`; the task-consistency check passes on the dispatched file (validation §1).
- Dispatched 04:25:00Z. Both premises replay `present` (§2). No question and no amendment.
  - An alive PONG at 04:26:56Z named the plan and the reading of `audit:c1f60f7:3` before any code.
  - A second alive PONG answered the 04:53:36Z state PING.
- The session restarted once during the test edits. The worktree held every edit, and the three modules then passed (validation §5).

## The owned rows and what each changed

Item 1's rows, read from `origin/main` (validation §3):

| Row | Class | Change | Test |
|---|---|---|---|
| `local:c1f60f7:3` | advisory-p2 | C9 maps `task-consistency-check C<n>` to `scripts/orchestrator/task-consistency-check.py`, now named once as `CHECKER`, where the checker landed. It was `scripts/task-consistency-check.py`. | `test_task_consistency_check_c9_probes_the_landed_checker_path` (new): a docs task quoting `task-consistency-check C4` passes. The stub `git` answers `present` for that path alone and logs the probe. |
| `audit:c1f60f7:1` | ledger-fidelity | `ledger-check.py` counts a `review_comment` only when its `author` is `chatgpt-codex-connector[bot]` (it was any item with `bot` set), as `swept_finding_ids()` in `scripts/require-crit-review.py` does. The docstring says "a Codex Bot review comment". | `test_ledger_check_counts_what_the_gate_counts`: the amendment-2 parity test, which the audit named, gains a Codex Bot inline comment, counted, and a CodeRabbit one, not counted. `findings 3; gaps 3`. |
| `audit:c1f60f7:2` | trusted-checkout | `orch-audit.sh` refuses the ledger check, the default `ledger-check.py` as an override, unless it is tracked (`git ls-files`, the existing refusal text) and unchanged from `HEAD` (`git diff --quiet HEAD`, `<check> differs from HEAD`). This is the validator's pair of checks. The `@description` and `@option` lines say so. | `test_orch_audit_refuses_a_ledger_check_that_differs_from_head` (new). Each case exits 2 before the ledger check and before codex: the default untracked, the default edited after its commit, and an override edited after its commit. |
| `audit:c1f60f7:3` | counter-evidence | No change. The lineage record's own line disposes of it as `not-applicable:fixed in this record before the gate (the counters pasted and the threshold dispositioned above)` (validation §3, line 122). The finding was about that record, names no repository file, and the SKILL already requires the paste. This was stated in the 04:26:56Z PONG, and no amendment followed. | — |

Test edits the rows force, beyond the new cases:

- **The `review_comment` items the tests write:**
  - In `test_ledger_check_passes_a_complete_record` and `test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap`, they now carry the Codex Bot's `author`, as the sweep JSON does. Before, `bot: true` stood for it.
  - The fixture sweep under `tests/fixtures/lessons/` already carries the author, so its count stays 36.
- **The two `orch-audit.sh` tests that reach the ledger check** commit `scripts/orchestrator/ledger-check.py` in their `origin` commit, since an untracked default is now refused.

## Tests

The Check: 103 tests OK across the three modules (validation §5). Mutation pass, 4 mutations, 4 caught (§7):
- C9 back on the old path;
- the ledger counting any bot;
- the `HEAD` comparison removed;
- the default exempted from the tracking check again. This one survived the first pass; the untracked-default case was added for it.

## Caps

Validation §6:

- outside `tests/` and `.orchestration/`: 3 files, 11 added + 6 deleted = 17 changed lines (cap 200);
- under `tests/`: 59 added lines (cap 1000);
- 5 files outside `.orchestration/`.

## CI and the Bot

- **The Bot:** PR #365 was opened as a draft and marked ready (04:57:25Z) after the evidence commit `4cc9d206`. Review 5528296451 at 05:00:08Z, of that head, raised one inline thread, a P2, and its body holds no badge (validation §8). No P0 or P1, so there is no fix round.

  | Thread | Where | Finding | Proposed disposition |
  |---|---|---|---|
  | 4279174373 | `orch-audit.sh:55` | The tracked-and-unchanged check covers the checker file alone, while `python` without `-I` prepends the checker's directory to `sys.path`. An untracked module beside it, such as a `json.py`, would still be imported. Remedy named: run the checker with `-I`, or validate its import directory. | advisory P2, for the lineage's next owner task under the same heading (the Completion's rule); the worker resolves no thread |
- **CI on `4cc9d206`:** 13 of 13 checks pass (validation §8).
- **CI on the final head (this commit, the evidence update):** in the RESULT.

## Not done, or outside scope

- C9 still treats the prose form `C<n> of the task-consistency check` as never present (T704 learning 4). No owned row names it.
- `ledger-check.py` still keys an inline comment on `discussion_r`, where the gate splits on `_r`. Both give the same id for a review-comment URL; no row names it.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
