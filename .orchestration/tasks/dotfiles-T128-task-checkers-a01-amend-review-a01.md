---
format: 2
task_id: dotfiles-T128-task-checkers-a01-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-checkers-a01-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-task-checkers-a01` (review seat half; Codex headless runs the same check)

Drafted 2026-10-14 (the TASK line's bus time is the dispatch time) by the orchestrator seat. The worker's question (PONG 04:18:10Z, before any push): `tests/unit/test_agmsg_orchestration_docs.py::test_regime_rule_sections_are_pinned_whole` compares the SKILL's invariants section byte for byte with `tests/fixtures/regime/invariants.md` (its lines 8 and 10 are SKILL lines 71 and 73), so item 6's two sentences fail the Check command unless the fixture changes in the same commit; the fixture was outside `allowed_files`. The task file is not on `main` (it reaches it with the next boundary): the pre-amendment copy is the pair-confirmed version 2e360dfe (seat round 3 and Codex round 3, 01:12Z), kept beside this brief as the comparison base; `git diff --no-index <that copy> <the file>` prints `1 file changed, 10 insertions(+), 2 deletions(-)`. Amended file: `.orchestration/tasks/dotfiles-T128-task-checkers-a01.md`, sha256 `cd00812f4a3cd64d841d5a96c7720e33be904e9cabb2cf70d31ccad8580b6a2d`; the pre-amendment copy is on `main` (`not on main; pre-amendment pair-confirmed copy 2e360dfeea7a659801ed8f6cca47cdc64da17fa80d362cb04c961483f279b8c0`).

## What changed (amendment 1)

1. `allowed_files` gains `tests/fixtures/regime/invariants.md`.
2. One residual threat row for it (a data fixture; its diff is item 6's two sentences verbatim; the audit compares the fixture diff with the SKILL diff).
3. Item 6's last bullet says the fixture changes in the same two sentences, verbatim, in the same commit; the out-of-scope list names any other fixture line.
4. A `## Change of 2026-10-14 (amendment 1 …)` section stating 1 to 3. Nothing else changes; items 1 to 5 stand.

## Stop condition

1. The diff of the task file against its pre-amendment pair-confirmed copy (the orchestrator's scratchpad `t704-before-amend1.md`, sha256 2e360dfeea7a659801ed8f6cca47cdc64da17fa80d362cb04c961483f279b8c0; the file is not on `main` yet) contains only what the list above says.
2. For each behaviour the amendment adds or changes in a script or a procedure, name the threat row that covers it; a new effect on a gate input (an acceptance record, a sweep JSON, an audit receipt), on the bus or on the host has its own row with a closing test, added by this amendment (C-28, M-20261012-29). An amendment that adds behaviour without its row is `revise`.
3. Each closed row's named test closes its risk and the test names appear verbatim in the task's test item; the wording agrees with the rule sentences and the sibling tasks it cites.
4. The file passes C1 to C10 and C7b (the orchestrator pasted OK) and `amend-sweep.sh` for the superseded terms (pasted); `reset_of`, the copy rows and the evidence directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a01.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-task-checkers-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-task-checkers-a01-amend-review-a01 verdict=confirm|revise amended_task_sha256=cd00812f4a3cd64d841d5a96c7720e33be904e9cabb2cf70d31ccad8580b6a2d validation=<path>`.
