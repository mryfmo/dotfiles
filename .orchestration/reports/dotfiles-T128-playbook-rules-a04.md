# Report: dotfiles-T128-playbook-rules-a04

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `regime/playbook-rules`, PR #328. a04 is a03's reset under plan 010 option D (`reset_of: [a01, a02, a03]`).
- Before any edit, the branch was fast-forwarded from the worker's `fe34f7db` to the orchestrator's update-branch head `e12872cd`. `fe34f7db` is an ancestor, so nothing was rebased (validation §1).
- Task file sha256 `e64ee691…` matches the TASK's `task_sha256`. It is copied byte-identical in `ff2e7156` to `.orchestration/dotfiles-T128-playbook-rules-a04/task.md`. The a01, a02 and a03 copies are unchanged since `1083a8c1`, `4486dbdd` and `196d73ca` (§1).

## Commit `beee078a`: items 1 and 3 as obligation, script and landing condition

Both sentences were spliced into the SKILL from the task's quoted spans, not retyped, and every quoted span of items 1 to 6 is present verbatim (§3).

| Item | Now | Test |
|---|---|---|
| 1 (step 6) | the dispatch line "as the bus line with its read marker"; the open TASK list "re-derived from a complete bus read, never from a default-limited one"; "A seat silent for thirty minutes since its latest bus event for the task (INV-10's figure) gets a bus read, then a PING"; once T718 lands, `dispatch.sh` and `bus-read.sh`, until then `history.sh <team> --limit 1000` | `test_dispatches_are_recorded_from_the_bus`: one token per sentence; `assertNotIn` for "expected duration", "the bus line `history.sh <team>` prints" and "no bus event from its seat since" |
| 3 (three-repeat) | the records search pasted as `search: <class> -> <…>`; corrections applied mechanism by mechanism; a class is an `[a-z0-9-]` slug assigned at disposition time, never review-title text; once T718 lands, `three-repeat.sh <class>` runs both searches without a shell; once `gate-evidence-a02` lands, the gate refuses without the line | `test_three_repeats_start_with_a_pasted_correction_search`: one token per sentence; `assertNotIn` adds `memory search <class slug>` (the unquoted interpolation) to the earlier stale forms |

Items 2, 4, 5, 6, 7 and 8 are unchanged, as the task says.

## A premise worth knowing: `history.sh <team> --limit 1000`

Item 1's interim command reads the complete history: 778 rows, against 20 by default, the same count as the positional `history.sh <team> '' 1000` (§2). It does so by accident, though. `history.sh`'s usage is `<team> [agent_id] [limit]`, so `--limit` lands in the agent slot. `storage_history` skips a dash-led agent and then reads `--limit --limit 1000`, taking the second `--limit` as the limit value; a non-numeric limit becomes -1, which means no limit (§2 quotes both scripts). So the sentence's obligation, a complete read, holds, but `1000` is not the limit that applies. I wrote it verbatim, and T718's `bus-read.sh` is meant to replace it. If the orchestrator wants the interim form to be literal, the positional `history.sh <team> '' 1000` reads the same rows by design, and changing it is an amendment.

## Declared fixture changes (INV-12)

- `tests/fixtures/regime/orchestrator-step-6.md`: item 1 (`beee078a`).
- `tests/fixtures/regime/invariants.md`: item 3 (`beee078a`).
- `code-review-orchestration.md` was regenerated and is unchanged (§7).

## Results

- Docs module 47 OK (§4). `test_pr_feedback.py` OK, ruff clean (§5).
- 20 mutants, 20 failures (§6): 1c and 1e put back a03's item-1 wording, 3d a03's whole bullet, 3f a03's "without the paste".
- Size (§7): 6 files outside `.orchestration/`; 7 added lines outside `tests/`; 113 under `tests/` (caps 500 and 1000).
- Premises (§2): `main` moved only under `.orchestration/` since the merge-base; `scripts/orchestrator/` does not exist on `main`, so T718 has not landed; `regime/gate-evidence` is open.

## Bot threads from a03's head `fe34f7db`

| Thread | Disposition |
|---|---|
| 4249303413 (P1, default-limited read) | `fixed:beee078a`: "a complete bus read, never … a default-limited one" |
| 4249303433 (P1, review title into a shell) | `fixed:beee078a`: a class is an `[a-z0-9-]` slug assigned at disposition time; `three-repeat.sh` runs without a shell; the command with `<class slug>` is gone |
| 4249303426 (P2, clock stopped by one early PONG) | `fixed:beee078a`: "since its latest bus event for the task" |
| 4249303398 (P2, partial correction status) | `fixed:beee078a`: "applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism" |

The earlier threads stand as the a03 report tables them. 4248319926 is answered by the update-branch already taken (`e12872cd`). The worker resolves no thread.

## CI and the Codex Bot on the a04 head `2276a365` (main-checkout copy)

- CI: all 12 check runs on `2276a365` are `completed success`, and the watcher exited 0 (validation §9).
- Bot: no review within 10 minutes of the push, so `@codex review` was posted at 15:59:59Z. Review 5493270947 of `2276a365` arrived at 16:03:26Z with one P1 and no P2. Counts: Bot reviews on PR #328 = 5 (`9b2c02a1`, `375bae0f`, `c4e0bb72`, `fe34f7db`, `2276a365`); worker P0/P1 fix rounds = 0.

| Thread | Finding | Verified premise (§9) | Proposed handling |
|---|---|---|---|
| 4250028600 | P1, SKILL.md:74 (item 3): the two trigger paths use different class formats. `scripts/regime-counters.sh` prints its S1 candidate as the first three words of a review title, while the rule says a class is an `[a-z0-9-]` slug assigned at disposition time, so "the records search for that class" has no defined input when the counter path fires | `regime-counters.sh:147` prints `S1: candidate class=<title words>`; `tests/unit/test_regime_counters.py:451` expects `class=reject skipped contract` | `open:4250028600`: not fixable here. The fix is either the script (forbidden: edit-scripts; `scripts/regime-counters.sh` is outside `allowed_files`) or the sentence (an amendment). Two options for the orchestrator: (a) make the counter emit, or resolve its candidate to, the ledger's assigned slug (a T718 or regime-counters task); (b) say in the sentence that a counter candidate is mapped to its ledger slug before the search |

## Not done, or outside scope

- `tests/unit/test_regime_counters.py` and `test_require_crit_review.py` were not run locally (PyPI is unreachable from the sandbox); neither reads the changed files.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `a3ae0494-87a7-437c-b39a-2a08ecfcd170` (§8), with the `history.sh --limit` mechanism above.

cost: n/a

## Revise round 1 with amendment 1 (ACCEPTANCE of 13:57:09Z; task file sha256 `c5dbc2c3…`)

The orchestrator's line lifted the operator's 10:36Z stop and superseded TASK 935. The branch fast-forwarded to the remote head `7771082f`, merged `origin/main` (`4e7a9b3a`) in `87bce51e`, and the task copy now matches the amended file byte for byte (validation §10). `e6602ca1` puts the amended sentences of items 1, 4 and 5 in the SKILL verbatim, as the task file quotes them (§10 checks all three):

| Thread | Finding | Disposition |
|---|---|---|
| 4257278283 (P1) | the invariant check compared ids only | `fixed:e6602ca1`. Each invariant's sentence equals the design's byte for byte, the design read from main (INV-2), by hand until a checker lands. Test: `test_task_file_review_is_one_round_with_a_fixed_stop_condition` (P4) |
| 4257278271 (P2) | step 6 used thirty minutes as INV-10's figure | `fixed:e6602ca1`. A seated worker idle for 20 minutes (INV-10's idle figure; 30 minutes is the first-push deadline). The orchestrator applies it to the minutes `bus-read.sh` prints. Test: `test_dispatches_are_recorded_from_the_bus` (P2) |
| 4257278276 (P2) | the row unit had no rule for a wildcard entry | `fixed:e6602ca1`. One row per concrete changed file under an executed or applied wildcard entry; a data wildcard keeps one row. Test: `test_threat_table_rows_have_a_fixed_unit` (P3) |
| local review of `7771082f`, finding 1 | "a complete bus read", which the merged script does not do | `fixed:e6602ca1`. The read is refused when it reaches its limit, and the orchestrator raises `BUS_READ_LIMIT` and reads again. Test: `test_dispatches_are_recorded_from_the_bus` (P1) |

- Declared fixture changes (INV-12): `tests/fixtures/regime/invariants.md` (the task-file-review and threat-table bullets) and `tests/fixtures/regime/orchestrator-step-6.md` (step 6). `test_regime_rule_sections_are_pinned_whole` fails on a changed fixture (P5).
- The `test_dispatches_are_recorded_from_the_bus` stale list also refuses `complete bus read` and `silent for thirty minutes`.
- Results (§10): 47 docs tests OK; Prettier and ruff clean; 5 mutants, 5 failures. Size: 6 files outside `.orchestration/`; added lines outside and under `tests/`: 7 and 127.
- The orchestrator's line says the Bot reviews on PR open only now, so there is no Bot wait; the pushed head's CI is in the RESULT and in the main-checkout copy.

## CI on the revise head `65a3d71b` (main-checkout copy only)

- Pushed at 2026-10-13T14:04:00Z. CI: all 13 checks pass (validation §11). There is no Bot wait, per the orchestrator's line of 13:57:09Z.
