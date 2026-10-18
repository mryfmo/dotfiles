---
task_id: dotfiles-T129-audit-inherit-replan-json-followup-a01
seat: claude-standard-dot-a011
branch: tools/audit-inherit-replan-json-followup-a01
base: 741e24272fd64b6a36c0d6725c53265de1c94982 (PR #390's head; the PR's base is main)
code_commit: d3891c0b (the test commit 598ca1f9 and the fix d3891c0b)
pr: not yet (gh pr create waits for the orchestrator's PING, as the dispatch note says)
task_sha256: 1f6b90f40470d02455fbd2424a01b1e9cb40a03c0b5f5f7f135d645295dbf3bb
---

# Report: dotfiles-T129-audit-inherit-replan-json-followup-a01

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The task text's re-plan names `codex-standard-dot-a010`, but the dispatch went to this seat, which follows the dispatch.
- Task file: dispatched 2026-10-18T06:27:55Z at `1f6b90f4…`, copied byte-identical to `task.md`. The task-consistency check passes, and premises 1 to 3 re-run unchanged (validation §1, §1a and §2). The record's owned rows at dispatch are `local:741e242:2` only (§3), which is R2.
- Branch: `git fetch origin tools/audit-inherit-replan-json`, then `git switch -c tools/audit-inherit-replan-json-followup-a01 741e242…`, each a single command. The PR's diff against main is F1 plus this re-plan, so its task-level audit is the first that covers F1.

## What changed

1. **R1, `scripts/orchestrator/chain-integrate.sh` (the local review P1 of 741e242, class `unbound-evidence`)**: inside the existing inheritance condition, after the two patch-ids are computed, the head must also be the tree a clean merge of its parents writes: `"${git}" -C "${main}" merge-tree --write-tree "${head}^1" "${head}^2"` must print a non-empty tree equal to `rev-parse "${head}^{tree}"`. Otherwise `old` is emptied and the head gets a fresh audit, through `orch-audit.sh` as before. A conflict (merge-tree exits 1) or a git without `--write-tree` empties `tree`, so it fails closed. The header sentence says so. 6 added and 1 removed lines.
2. **R2, `scripts/orchestrator/ledger-check.py` (owned row `local:741e242:2`)**: an audit summary whose first line is `inherited-from: <sha7>` yields `audit:<that sha7>:<n>`; otherwise the sha7 comes from the file name as before. The module docstring says so. 7 added and 3 removed lines.
3. **Tests**:
   - `tests/unit/test_chain_glue.py::test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree`. The fixture puts a file of two identical blocks (`L L L M L L L`) on main, and the audited PR head inserts `NEW` after the first `M`.
     - (a) A clean merge of a moved main inherits: no `orch-audit.sh` call, and the inherited summary exists.
     - (b) A merge that moves `NEW` to the second block has the same patch-id, which the test asserts, yet gets a fresh audit: one `orch-audit.sh` call and no inherited file. That case is red on `598ca1f9`.
   - `tests/unit/test_task_checkers.py::test_ledger_check_reads_inherited_audit_ids_from_the_marker`: an inherited summary named for `1234567` whose marker names `abcdef0`, with one `[P1]`. A record holding `audit:1234567:1` gives `GAP audit:abcdef0:1`, and a record holding `audit:abcdef0:1` passes. Red on `598ca1f9`.

## The Check

- The re-plan's command `uv run python -m unittest tests.unit.test_chain_glue tests.unit.test_task_checkers tests.unit.test_orchestrator_tools -v`: 80 tests green at the head (validation §5). Red on `598ca1f9` for exactly the two new tests.
- The a01 Check command (`test_chain_glue`, `test_require_crit_review`, `test_regime_counters`, `test_orchestrator_tools`), validation §6a:
  - Inside the sandbox, 201 tests, with 136 failures in `test_require_crit_review`. At `741e242` the same command runs 200 tests with the same 136 failures, the same tests by name.
  - The cause is this machine's global git config (SSH commit signing that cannot read `~/.ssh` in the sandbox). With `GIT_CONFIG_GLOBAL=/dev/null`, a failing test passes alone, and the whole command is green (§6a). CI is the authority.
- shellcheck and `shfmt -i 4 -sr -d` are clean on `chain-integrate.sh`; `ruff format --check` and `ruff check` are clean on the changed Python files (§6).
- Caps (§7): against `741e242`, 17 changed lines outside `tests/` and `.orchestration/` (cap 60) and 58 under `tests/` (cap 120). Against `origin/main`, 113 and 366 (the a01 caps 200 and 1000).

## Declared

- Worker review P2, outside R1/R2: F1's audit link from the merge's first parent to the audited head is the 7-character short sha in the file name (`chain-integrate.sh:183-185`). A deliberately hostile worker could grind a commit with a colliding prefix and inherit another head's audit; it cannot happen by accident. Proposed owner: `dotfiles-T129-audit-inherit-replan-json-followup-a02`. Fix direction: bind the full sha.
- Worker review P3: `ledger-check.py` prints the findings of an inherited summary twice when its parent's summary is also passed. Only the printed totals are affected; the exit code is right and the gate uses a set. Same proposed owner.
- R1 compares against a local `git merge-tree`. On GitHub's real update-branch merge `741e242` it reproduces the head's tree (premise 3), so the honest case still inherits. A rename or criss-cross case where GitHub's merge differs would only cost a fresh audit.

## Review, hook, cost

- Worker-side independent review: one round on `d3891c0b` by a fresh read-only subagent, `Verdict: correct`, with the two declared findings above. It confirmed fail-closed behaviour on a conflict, an older git, a non-merge head and an octopus merge, liveness on 741e242, and agreement of R2 with the gate's marker parsing. Files: `dotfiles-T129-audit-inherit-replan-json-followup-a01-worker-crit.json` and receipt `dotfiles-T129-audit-inherit-replan-json-followup-a01-worker-review-receipt.md`.
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
- CompactionDB: one decision added in this worktree's store before completion, id `707e4cfa-db8f-43aa-8a42-d32d32972aa6` (validation §9).
