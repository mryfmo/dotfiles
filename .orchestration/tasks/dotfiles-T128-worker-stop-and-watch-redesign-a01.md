---
format: 2
task_id: dotfiles-T128-worker-stop-and-watch-redesign-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-worker-stop-and-watch-redesign-a01 — the reset redesign of A7 (INV-6: a second revise RESULT would be revises 2)

Drafted 2026-10-12 02:49Z by the orchestrator seat. `dotfiles-T128-worker-stop-and-watch-a01` (PR #323, worker `claude-standard-dot-a003`, head `e924c5df`, CI green, no Codex P0/P1 on any head after the first RESULT) has RESULT 664 and the revise-round RESULT 666; its four open Bot P2 threads need three text changes, and the RESULT that would carry them is revises 2 (INV-6), so A7 resets to a02 by this task. The counters at the stop are in `.orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a01.md`.

## What to produce

The complete text of `dotfiles-T128-worker-stop-and-watch-a02.md`: the A7 file at sha256 `b0b8459834bf11869843ba685d795538523f1fa19adb2c30777586b11bed0b19` (`.orchestration/tasks/dotfiles-T128-worker-stop-and-watch-a01.md`) with exactly these changes:

1. `task_id: dotfiles-T128-worker-stop-and-watch-a02`; `reset_of: [dotfiles-T128-worker-stop-and-watch-a01]`; `allowed_files` gains `tests/fixtures/regime/message-contract.md` and names `.orchestration/dotfiles-T128-worker-stop-and-watch-a02/**` in place of the a01 directory; the fixture row names the three fixtures; the task-copy row names `-a01/task.md and -a02/task.md` and its residual binds the a02 file's hash. (`design_review.receipt` stays round 18.)
2. A7-1 (step 15), thread 4244248703: the listing bullet lists every Codex Bot review body that carries a badge (P0 to P3) and attributes it to the review's `commit_id`; the fix cap and INV-6's head count stay P0/P1 (inline, `review_comment` items); state the sentence and its token.
3. A7-2 (step 7), thread 4244272551: the audit-head component of INV-6 is read as the counters bullet prescribes (the script's `audits=` when it prints one; otherwise the record's pasted reading of INV-6's source or of the interim record the orchestrator used), not by naming an artifact format; state the sentence (it names no file format) and its token.
4. Message Contract v1, thread 4244248706: the RESULT line gains `head=<full sha>` as a mandatory field ("the first RESULT's head is INV-6's baseline"), the fixture `tests/fixtures/regime/message-contract.md` is updated in the same commit, and `test_question_pongs_are_in_the_contract` or a sibling test pins the token `head=<full sha>`; state the line and the token.
5. Thread 4244248692 (a threat row for the forced removal): no row. The introduction states why: the table's unit is a controlled path (every `allowed_files` entry has a row); the forced removal is an orchestrator control-plane action behind the human-only permission gate, prescribed by the SKILL sentence the SKILL row covers, and the orchestrator dispositions the thread with that criterion (input for B0).
6. Title, introduction and one "History" sentence name a02 and this reset. First commit and Completion: from `e924c5df`, copy this file byte-identical to `.orchestration/dotfiles-T128-worker-stop-and-watch-a02/task.md` (the a01 directory stays), one commit for the copy, the three text changes, the three fixtures and the tokens, CI, Bot wait under the cap (a further finding of the `class-count-scope` kind, that the worker's count is narrower than S1's scope, is reported with its class, not fixed), `AGMSG-RESULT v1 task_id=dotfiles-T128-worker-stop-and-watch-a02 … head=<full sha> reset_of=dotfiles-T128-worker-stop-and-watch-a01` listing 4244248703, 4244272551 and 4244248706 as `fixed:<that sha>` and every earlier thread as RESULT 666 listed them.
7. Nothing else changes. Before sending, run `uv run --no-project --with pyyaml python /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/task-consistency-check.py <a scratch copy named dotfiles-T128-worker-stop-and-watch-a02.md>` from the repository root and paste its `OK` line.

## Output

`.orchestration/validation/dotfiles-T128-worker-stop-and-watch-redesign-a01.md` with the usual header and the whole a02 file in one non-empty four-backtick block (plain scalars with a colon-space quoted; `wc -l`, a YAML parse and the checker's `OK` before sending), then `AGMSG-RESULT v1 task_id=dotfiles-T128-worker-stop-and-watch-redesign-a01 status=ready_for_review verdict=redesign receipt=<path> receipt_sha256=<sha256> a02_expected_sha256=<sha256 of the block plus a trailing newline>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator writes the file, runs the checker and asks for the one confirmation (`verdict=accept design_sha256=<hash>`, the reset anchor; the record's `redesign_source` is this task id). max_turns=3. Forbidden: editing tracked files; branches; PRs.
