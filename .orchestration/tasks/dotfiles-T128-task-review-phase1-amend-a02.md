---
format: 2
task_id: dotfiles-T128-task-review-phase1-amend-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-review-phase1-amend-a02 — confirm amendment 1 of `dotfiles-T128-playbook-rules-a02` (review seat half; Codex headless runs the same check)

Drafted 2026-10-12 13:2xZ by the orchestrator seat. The Codex Bot's review 5491172156 of PR #328 head `375bae0f` raised two P2s; 4248319936 says the step-6 sentence "past the task's expected duration" has no computable threshold. The sentence is task text (item 1, verbatim into the SKILL), so it changes by amendment, confirmed by the review seat. One round.

## What changed (amendment 1 of a02)

- `.orchestration/tasks/dotfiles-T128-playbook-rules-a02.md` item 1: the last sentence of the step-6 addition now reads "Thirty minutes of bus silence from a seat after it reads a TASK, an amendment or a revise (the design's first-push threshold, INV-10; a TASK may state another figure as `expected_minutes=`) triggers a bus read, then a PING; a longer silent wait is never the answer." The heading and intro carry the amendment note (and the disposition path for 4248319926: the orchestrator's `gh pr update-branch` brings the `classes:` fields into the PR tree). Nothing else changes.
- Context: the thread text (`gh api repos/mryfmo/dotfiles/pulls/328/comments --jq '.[]|select(.id==4248319936)|.body'`, or the quote in the orchestrator's acceptance record), INV-10 in the design (`.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`: the 30-minute first-push threshold), C-12 (`.orchestration/learning/corrections/C-12.md`, updated with the same figure).

## Stop condition

1. The diff of the task file against its copy on `main` (`7cbe5405`) contains only what the list above says.
2. The new sentence gives a computable trigger (an elapsed time measured from a bus event the orchestrator can read) and does not contradict step 7's `max_turns` tracking or INV-10.
3. The file passes C1 to C7 (the orchestrator pasted OK; re-derive C7 by reading the rows) and `reset_of`, the copy rows and the a02 directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-task-review-phase1-amend-a02.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-playbook-rules-a02: confirm|revise`, then `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-phase1-amend-a02 status=ready_for_review verdicts=dotfiles-T128-playbook-rules-a02:<v> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing tracked files; branches; PRs.

## Round 2 (orchestrator, 2026-10-12 13:25Z)

Your round-1 receipt confirmed; the Codex half asked for one revision, applied once: the trigger now counts from the moment the TASK, amendment or revise entered the bus history (INV-10's clock), with no bus event from its seat since, and carries no override. Item 1's last sentence reads: "Thirty minutes after a TASK, an amendment or a revise enters the bus history with no bus event from its seat since (the clock and the figure of INV-10's first-push rule) trigger a bus read, then a PING; a longer silent wait is never the answer." Confirm the same three stop conditions on the revised file (its whole-file sha256 is in the AGMSG-TASK `task_sha256=` of the amendment line; `git diff HEAD -- .orchestration/tasks/dotfiles-T128-playbook-rules-a02.md`). Receipt: append a "Round 2" section to `.orchestration/validation/dotfiles-T128-task-review-phase1-amend-a02.md`, then `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-phase1-amend-a02 round=2 status=ready_for_review verdicts=dotfiles-T128-playbook-rules-a02:<confirm|revise> receipt=<path> receipt_sha256=<sha256>`.
