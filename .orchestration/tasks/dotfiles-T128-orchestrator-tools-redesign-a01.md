---
format: 2
task_id: dotfiles-T128-orchestrator-tools-redesign-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-redesign-a01 — write the successor task file `dotfiles-T128-orchestrator-tools-a03` (INV-6 reset of `-a01`; `-a02` is the second slice, not this lineage)

Drafted 2026-10-13 04:1xZ by the orchestrator seat. On PR #336 the Codex Bot's review of the amendment-1 head `5ec05d8d` (thread 4254494999, P1, `task.md:21`): "Fresh functionality added by amendment 1 makes `dispatch.sh` parse a caller-selected acceptance record, inspect untrusted bus output, and rewrite that record after sending, but the dispatch rows here cover only hash verification and malformed message lines … add a dedicated row covering that input and mutation path." The row is task text; a01 already carries amendment 1 (`91eb1ebe…`) and one question, so a second amendment is INV-6's reset: counters at 04:14Z `tasks=2 amendments=1 questions=1 results=2 withdrawn=0 revises=1`. The worker proposes the row and the test that closes it exists in the head (`test_dispatch_records_the_sent_line_with_its_read_marker`).

## Inputs

- `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md` at amendment 1 (sha256 `91eb1ebe246f76e138ce8f3bf108adff844f5acf303bcfecc2b7bc62eb0130ee`, on `main` `4470b0c8`), the thread (`gh api repos/mryfmo/dotfiles/pulls/comments/4254494999 --jq .body`), the worker's RESULT of 04:13:13Z (bus), the design on `main` (INV-6, INV-12), C-26 (threat rows derived from the diff).

## What the successor says (everything else verbatim from a01 amendment 1)

1. Front matter: `task_id: dotfiles-T128-orchestrator-tools-a03`, `reset_of: [dotfiles-T128-orchestrator-tools-a01]`, the a03 evidence directory in `allowed_files` (a01's no longer), copy rows for the a01 and a03 task copies (C3), `design_review.receipt` round 22, `after: []`. The id note: `-a02` is T718's second slice (the other nine scripts), not a predecessor; say so in the intro.
2. Threat table: one new row after the two dispatch.sh rows: "dispatch.sh, given an acceptance record path, reads that record's JSON block, reads the bus marker through history.sh, and rewrites the record's `dispatch` list after the send (a gate input mutated by the orchestrator's tooling)" with `closed: tests/unit/test_orchestrator_tools.py::test_dispatch_records_the_sent_line_with_its_read_marker` and, in the same row's sentence, the controls the script keeps: the path is an argument the orchestrator passes, the block is read with `object_pairs_hook` (a duplicate key refuses), only the `dispatch` list changes, the file is written whole with `sort_keys` and `indent=2`, and the gate re-validates the block.
3. Item 2 names that test among the closed-row names if it does not already.
4. The heading carries the reset; the intro names thread 4254494999, the amendment-1 head `5ec05d8d`, the INV-6 trigger, and that the worker's commits (`2dddff84`, `0a5ae302`, `374fc171`, `b80b03ee`, `77e75595`, `5ec05d8d`) stay; one Completion clause (PR #336 stays; the worker adds the a03 task copy and evidence, no other change expected).
5. Nothing else changes: not items 1, 3, 4, not the premises (replay at `origin/main` `4470b0c8` per C-18), not the environment row. Keep the "Amendment 1" section as history under the a03 heading.

## Stop condition

`task-consistency-check.py` C1 to C10 and C7b pass on a03 (state what you re-derived: the two copy rows, C4 for the new row, C7); `amend-sweep.sh` for `orchestrator-tools-a01/` (outside the copy rows and the history section) finds nothing; the differences from a01 amendment 1 are exactly items 1 to 4; the new row's test name exists in the head `5ec05d8d` (`git show 5ec05d8d:tests/unit/test_orchestrator_tools.py | grep -n test_dispatch_records_the_sent_line_with_its_read_marker`).

## Output

Write `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a03.md` and the receipt `.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a01.md` (header; diff summary; checks; the successor's sha256), then `AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-redesign-a01 status=ready_for_review verdict=accept design_sha256=<sha256 of the a03 file> receipt=<path> receipt_sha256=<sha256>` via the bus. Forbidden: any other tracked file, branches, commits, pushes, PRs. The Codex half reviews a03 on the same hash.

## Round 2 (orchestrator, 2026-10-13 04:2xZ)

Your a03 (`b7348b8a…`) is accepted by this seat. The Codex half asked about one thing outside items 1 to 4: the checker-range phrases "C1 to C6" (item 5's "nothing else changes") that you updated to "C1 to C10 and C7b" at line 39 and in the preserved history paragraph. They are right, as they were in a04 (brief item 7 there); the brief now allows them: 6. the checker-range phrases read "C1 to C10 and C7b" wherever a01 said "C1 to C6", including the history paragraph (bookkeeping). No rewrite: the Codex half re-runs on the same hash with this brief.
