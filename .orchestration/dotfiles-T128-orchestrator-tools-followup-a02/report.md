---
task_id: dotfiles-T128-orchestrator-tools-followup-a02
seat: claude-standard-dot-a002
branch: tools/orchestrator-tools-followup-a02
base: 907522c2
code_commit: bf0fe7ab
task_sha256: 5fab7eb8076bb83f23f094cbbcd3be5e8881dd3b6ece707a4db14a96c119b3bb
---

# Report: dotfiles-T128-orchestrator-tools-followup-a02

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/orchestrator-tools-followup-a02` from `origin/main` `907522c2`. The PR #365 and #366 branches stay in the worktree untouched.
- Task file: sha256 `5fab7eb8…`, copied byte-identical; the task-consistency check passes on the dispatched file; the four attached inputs hash to the values the task intro names (validation §1). Dispatched 08:06:21Z. All three premises replay equal (§2). No question and no amendment.

## The owned rows and what each changed

Read from the attached copy of the record (validation §3): four ids, three defects, in the task's order.

| Row | Class | Change | Test |
|---|---|---|---|
| `audit:2e77a33:1` (P1) | pathspec-globbing | `boundary.sh` passes each deleted name to `git rm` as `":(literal)${f}"`, so a `*`, `?` or `[` in it is a character, not a pattern. `--ignore-unmatch` and `--` stay. | `test_boundary_deletes_a_name_with_glob_characters_literally`: origin holds `a*.md`, `ab.md`, `[x].md`, `x.md`; the first and third are deleted; the boundary commit deletes exactly those two, and `ab.md` and `x.md` stay in its tree. |
| `audit:2e77a33:2` (P1) | collision-key-order | `fill_sweep.py` builds the collision set from `cids`, the fragments after the `discussion_r` strip, which is the key the lookup uses. The raw fragment `key` stays only for the GAP line, as before. | `test_fill_sweep_sees_a_collision_after_the_discussion_r_strip`: a review fragment `discussion_r123` and a status fragment `123` with one TSV row `123`: both items print `shared-key 123 item#<n>`, both stay gaps and the sweep is not written; rows `item#0` and `item#1` then fill them. |
| `audit:e9404a6:2`, `audit:39c186a:2` (P3) | evidence-command-null-url | For an item whose `url` is JSON null, the evidence command is `jq '.items[] \| select(.source == "<source>" and .check == "<check>")' <sweep>`, both values written as JSON literals. Only the disposition string changes; no other field of the item is touched, so the gate's comparison of the masked bodies sees the same items. | `test_fill_sweep_selects_a_null_url_status_by_source_and_check`: a null-url CodeRabbit status gets that exact command, and the command, replayed with the real `jq`, prints the item. |

Each fix reverted alone fails its test, and the file was restored afterwards (validation §6: 3 mutants, 3 caught).

Readings, declared:

- **The null-url branch is generic:** it keys on `url is None`, not on `source == "status"`, so any null-url item gets a command that selects it. Two null-url items share the empty fragment and already take the `item#<n>` path with `jq '.items[<n>]'`, which still wins.
- **Quoting:** the new command, like the url form before it, sits in single quotes, so a `'` inside a check name would break the replay. No row names that, so it is unchanged.

## Tests

The Check: 51 tests OK, the three new ones named (validation §5); `shellcheck` clean; `ruff check` and `ruff format --check` clean.

## Caps

Validation §7: outside `tests/` and `.orchestration/`, 2 files, 11 added + 5 deleted = 16 changed lines (cap 200); under `tests/`, 67 added lines (cap 1000).

## CI and the Bot

In the RESULT (the post-ready calls are planned in sandbox.md, so no evidence update moves the head after the Bot's review).

## Not done, or outside scope

- Nothing outside the three files. The other 32 ids of the owner section are closed in the record, per the task intro.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
