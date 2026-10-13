---
format: 2
task_id: dotfiles-T128-orchestrator-tools-a03-amend-review-a1
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-a03-amend-review-a1 — confirm amendment 1 of `dotfiles-T128-orchestrator-tools-a03` (review seat half; Codex headless runs the same check)

Drafted 2026-10-13 05:1xZ by the orchestrator seat. The Codex Bot's thread 4254893065 (P2) on the a03 head `c8fb09b0` says a line without `task_id=` is sent and, with a record, skips the association check, and that the threat table has no row for this malformed-identity path. The code fix is the worker's revise (sent 05:0xZ); the row is task text. Amended file: `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a03.md`, sha256 `ef3b264693a4d8a91b688b06f46d3fb44ec2e90578ad3a18258b69c29b1fcb34`; the pre-amendment copy is on `main` (``1da9594c`, sha256 b7348b8a…`).

## What changed (amendment 1)

- Threat table: one row after the two dispatch.sh rows for a line whose `task_id=` is missing, empty or repeated (or recorded against a record), closed by `test_dispatch_refuses_a_line_without_a_task_id`.
- Item 2 names that test among the closed-row names.
- An "Amendment 1" section at the end. Nothing else.

## Stop condition

1. The diff of the task file against its copy on `main` contains only what the list above says.
2. For each behaviour the amendment adds or changes in a script or a procedure, name the threat row that covers it; a new effect on a gate input (an acceptance record, a sweep JSON, an audit receipt), on the bus or on the host has its own row with a closing test, added by this amendment (C-28, M-20261012-29). An amendment that adds behaviour without its row is `revise`.
3. Each closed row's named test closes its risk and the test names appear verbatim in the task's test item; the wording agrees with the rule sentences and the sibling tasks it cites.
4. The file passes C1 to C10 and C7b (the orchestrator pasted OK) and `amend-sweep.sh` for the superseded terms (pasted); `reset_of`, the copy rows and the evidence directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-orchestrator-tools-a03-amend-review-a1.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-orchestrator-tools-a03: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-a03-amend-review-a1 verdict=confirm|revise amended_task_sha256=ef3b264693a4d8a91b688b06f46d3fb44ec2e90578ad3a18258b69c29b1fcb34 validation=<path>`.
