---
format: 2
task_id: dotfiles-T128-gate-evidence-a04-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-gate-evidence-a04-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-gate-evidence-a04` (review seat half; Codex headless runs the same check)

Drafted 2026-10-13 03:2xZ by the orchestrator seat. Worker-c's question of 03:15:27Z on T718 a01 (the agmsg scripts expose a read marker, `history.sh` prints ●/○, never a timestamp; the skill forbids reading the database) showed that a04's `dispatch` key described its entries as ` read_at=<timestamp or unread>` while T718's `dispatch.sh` will write `read_at=read|unread`. One wording change aligns a04 with what will be written; the gate still validates the list only as strings. Amended file: `.orchestration/tasks/dotfiles-T128-gate-evidence-a04.md`, sha256 `be659392a6300bc0fff0ba3c421660352938762d6fccb259075f1c430ae8b3d8`; the pre-amendment copy is on `main` (`948d1f38`, sha256 03a5253d…).

## What changed (amendment 1)

- Item 2, the `dispatch` key: the entry suffix is ` read_at=<marker>`, the marker `read` or `unread` as `history.sh` prints it, recorded by `scripts/orchestrator/dispatch.sh`, never a database read.
- An "Amendment 1" section at the end. Nothing else.

## Stop condition

1. The diff of the task file against its copy on `main` contains only the two changes above.
2. The wording matches T718 a01 amendment 1's item 1 (`.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md` on `main`) and the a04 rule sentence of T703 (step 6: "the bus line with its read marker").
3. The file passes C1 to C10 and C7b (the orchestrator pasted OK); `reset_of`, the copy rows and the a04 directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-gate-evidence-a04-amend-review-a01.md`: the usual header with the file's sha256, findings, one line `Amendment verdict: dotfiles-T128-gate-evidence-a04: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-a04-amend-review-a01 verdict=confirm|revise amended_task_sha256=be659392a6300bc0fff0ba3c421660352938762d6fccb259075f1c430ae8b3d8 validation=<path>`.
