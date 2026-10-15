---
format: 2
task_id: dotfiles-T128-task-checkers-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-checkers-review-a01 — confirm the task text of plan 007 T704 (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-14 by the orchestrator seat (round-1 TASK on the bus 00:54:47Z). The reviewed file is `.orchestration/tasks/dotfiles-T128-task-checkers-a01.md` (untracked; its sha256 is the `checkers_sha256` of the TASK line), the first task written in plan 021's step-7 short form (goal in one sentence, files, out of scope, one end-to-end check command, a hand-written threat table: the generator it lands cannot generate its own). Its inputs are the two scratchpad scripts under `.orchestration/tasks/dotfiles-T128-task-checkers-a01-input/` (sha256 in the file's first paragraph). Sources to read first: plan 007 line 127 (T704), plan 021 step 6.2 and its scrutiny rows S6 and S10, plan 020 step 4 (the Completion rules), the design `dotfiles-T128-regime-v3-a01.md` INV-2 (caps) and the two SKILL sentences at lines 71 and 73 of `origin/main` 7d58d6cd. One round, fixed stop condition.

## Stop condition

1. Nothing in the file contradicts plan 007 T704, plan 021 step 6.2 or the design: the two checkers, their tests, the fixtures from the ten historical files and the pre-fix record, the two SKILL sentences; no check changes meaning (the inputs are the specification). The premises hold: re-run the commands of premises 1, 2, 4 and 5 and compare the outputs byte for byte (paste any difference).
2. `allowed_files` covers every touch point the items name and nothing else: `grep -n 'T704' home/dot_agents/skills/agmsg-orchestration/SKILL.md` gives exactly the two sentences of item 6; `grep -n 'T704\|C1 to C6' tests/unit/test_agmsg_orchestration_docs.py` gives exactly the two assertions item 6 names; `grep -n 'ledger-check' scripts/orchestrator/orch-audit.sh` is what item 3 changes; the subprocess pattern item 4 cites exists at `tests/unit/test_orchestrator_tools.py` (`--with`, `pyyaml`). The files are pairwise-disjoint from the in-flight PR #350 (`scripts/orchestrator/acceptance-front-matter.py`, `scripts/orchestrator/orch-gate.sh`, `tests/unit/test_orchestrator_tools.py`) except `tests/unit/test_orchestrator_tools.py`, which is allowed only because `after:` names a05 and dispatch follows #350's merge: confirm both.
3. Each `closed` row's test name appears verbatim in item 4 and that test closes the row's risk; the two quoted sentences of item 6 are byte-for-byte the text of `origin/main` 7d58d6cd (paste the two grep lines); no sentence states an unlanded mechanism as present outside its own landing clause; the Completion clause matches plan 020 step 4 (the Bot's single review, one fix round, a surviving P0/P1 to the operator, P2 advisory under a named owner); the INV-2 counts hold: 11 files outside `.orchestration/` (at most 15), and the line budget under `tests/` (480 front-matter lines plus 31, 1 and 22 of the triple plus the tests) fits 1000.
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-task-checkers-a01.md: OK` from the input checker at 00:5xZ); the brief check listed no count word or time that disagrees with the file's own lists.

## Output

`.orchestration/validation/dotfiles-T128-task-checkers-review-a01.md`: the usual header with both sha256 (this file's and the reviewed file's), findings (`P0`–`P3`, confidence, `file:line`, one line each), and one line `Task-file verdict: dotfiles-T128-task-checkers-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-task-checkers-review-a01 round=1 verdict=confirm|revise checkers_sha256=<sha> validation=<path>`.

## Round 2 (orchestrator, 2026-10-14 01:03Z)

The Codex half's round 1 (receipt `.orchestration/validation/dotfiles-T128-task-checkers-review-a01-codex.md`, 00:58Z, two P1, verdict revise) is applied: (1) premise 1's `output:` held three of the ten lines (a `tee | head -2` in the orchestrator's capture pipeline cut the file: M-20261014-01); the block now holds the ten lines, written by `premise-run.py --write`, which runs each premise's own `command:` and stores its full stdout, and all five premises re-run equal; (2) the one closed SKILL row named one test for two sentences; it is now two rows, one per sentence, closed by `test_rule_changes_travel_as_task_amendments` (line 73) and `test_threat_table_rows_have_a_fixed_unit` (line 71), and item 6 names the test per sentence. Nothing else changed; the input checker prints `OK` on the new hash (the `checkers_sha256` of the round-2 TASK line). Judge round 2 on that hash under the same four stop conditions; a round-1 RESULT on the old hash is superseded.

## Round 3 (orchestrator, after the round-2 RESULTs of 01:06Z)

Round 2: the seat confirmed on ba6a1e02 with one P2 and two P3; the Codex half (receipt `-codex-r2.md`) asked two changes. All five are applied: (1) item 2 no longer extends the ledger check (the JSON-block ids go to the out-of-scope list, for T705), so stop condition 1 holds as written, and its test is now `test_ledger_check_passes_a_complete_record`; (2) the two docs-test names stand in item 4 (its last bullet), so every closed row's test name is in item 4; (3) the Check's replay count says what it counts (15 before this task's own file joined the directory); (4) "200 changed lines (added plus deleted)" per plan 021 step 7.2 and "1000 added lines" per INV-2; (5) the clock times are gone from the draft lines of both files (C-33 rule 4). The input checker prints `OK` and `premise-run.py` prints OK for all five premises on the new hash (the `checkers_sha256` of the round-3 TASK line). Same four stop conditions.
