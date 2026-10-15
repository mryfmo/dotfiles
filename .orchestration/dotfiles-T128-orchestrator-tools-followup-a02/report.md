---
task_id: dotfiles-T128-orchestrator-tools-followup-a02
seat: claude-standard-dot-a002
branch: tools/orchestrator-tools-followup-a02
base: 907522c2
code_commit: bf0fe7ab
fix_commit: afe7f1eb
round2_commit: a07f0df4
pr: 368
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
| `audit:e9404a6:2`, `audit:39c186a:2` (P3) | evidence-command-null-url | For an item whose `url` is JSON null, the evidence command is `jq --argjson s <source> --argjson c <check> '.items[] \| select(.source == $s and .check == $c)' <sweep>`: each value is its JSON literal, shell-quoted with `shlex.quote` (the Bot's P1, thread `4280648512`, fixed in `afe7f1eb`: the check is an external status context, and interpolated into the single-quoted program a `'` in it ended the argument and ran the rest as shell code). Only the disposition string changes; no other field of the item is touched, so the gate's comparison of the masked bodies sees the same items. | `test_fill_sweep_selects_a_null_url_status_by_source_and_check`: a null-url status whose check is ``Code'Rabbit" $(touch pwned); touch pwned`` gets a `jq --argjson` command, and the command, replayed with `bash -c` and the real `jq`, prints the item and creates no `pwned` file. |

Each fix reverted alone fails its test, and the file was restored afterwards (validation §6: 5 mutants, 5 caught; the fourth drops the null-url branch's `shlex.quote`, the fifth the url form's).

Readings, declared:

- **The null-url branch is generic:** it keys on `url is None`, not on `source == "status"`, so any null-url item gets a command that selects it. Two null-url items share the empty fragment and already take the `item#<n>` path with `jq '.items[<n>]'`, which still wins.
- **The url form (round 2):** a status's url is its external `target_url`, which `pr-feedback.py` copies, so it is not a link the sweep builds. Round 1 left `select(.url == "<url>")` interpolating it; the audit of `cfebc1f` raised that as a P2 and the orchestrator sent it back as revise round 2 (C-50). `a07f0df4` passes it the same way: `jq --argjson u <url> '.items[] \| select(.url == $u)' <sweep>`, the url's JSON literal shell-quoted. Test: `test_fill_sweep_quotes_the_url_form_evidence` (a status url holding a quote and a `$(touch pwned)` payload, replayed with `bash -c`: the item is shown and no file is created); the expected string of `test_fill_sweep_refuses_a_not_applicable_without_evidence` changes to the new form.

## Tests

The Check: 52 tests OK, the four new ones named (validation §5); `shellcheck` clean; `ruff check` and `ruff format --check` clean.

## Caps

Validation §7: outside `tests/` and `.orchestration/`, 2 files, 14 added + 6 deleted = 20 changed lines (cap 200); under `tests/`, 92 added lines (cap 1000).

## CI and the Bot

- **The Bot:** PR #368 was opened as a draft and marked ready at 08:14:42Z. The Bot reviewed `3657d672` at 08:18:10Z (review `5530116843`) with one inline P1, thread `4280648512` on `fill_sweep.py:79`, "Shell-quote status contexts in evidence commands". The one fix round: `afe7f1eb`, with the test above extended to that input. No other thread.
- **Round 2:** no new Bot wait, per the revise message.
- **CI:** in the RESULT for the final head.

## Not done, or outside scope

- Nothing outside the three files. The other 32 ids of the owner section are closed in the record, per the task intro.
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
