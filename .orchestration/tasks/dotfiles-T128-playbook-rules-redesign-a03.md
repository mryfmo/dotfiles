---
format: 2
task_id: dotfiles-T128-playbook-rules-redesign-a03
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-playbook-rules-redesign-a03 — write the successor task file `dotfiles-T128-playbook-rules-a04` (plan 010 option D, the operator's choice)

Drafted 2026-10-12 by the orchestrator seat. The Codex Bot's fourth round on PR #328 (head `fe34f7db`) found four more things in items 1 and 3 only: 4249303433 (P1: the class slug comes from a review title and is substituted into shell commands), 4249303413 (P1: the `history.sh` read is default-limited to 20 rows), 4249303426 (P2: the silence clock never resets after one event), 4249303398 (P2: a correction's status can be landed for one mechanism and pending for another). Root cause M-20261012-21 / C-23: operational procedure written as rule prose. The operator chose plan 010 option D: items 1 and 3 become the obligation plus the script that performs it with its landing condition; everything operational moves to T718's scripts. The change is task text, so a03 is withdrawn (INV-6 pre-empted) and the redesign is yours. The worker `claude-standard-dot-a003` holds and continues under a04 on PR #328.

## Inputs

- `.orchestration/tasks/dotfiles-T128-playbook-rules-a03.md`, the four threads (quoted in `.orchestration/learning/mistakes/M-20261012-21.md`; `gh api repos/mryfmo/dotfiles/pulls/328/comments --jq '.[]|select(.id==4249303433 or .id==4249303413 or .id==4249303426 or .id==4249303398)|.body'`), C-23, plan 010, T718's task file (`.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md`: `three-repeat.sh`, `bus-read.sh`, `dispatch.sh`), the SKILL on `main`.

## What the successor says (everything else verbatim from a03)

1. Front matter: `task_id: dotfiles-T128-playbook-rules-a04`, `reset_of: [dotfiles-T128-playbook-rules-a01, dotfiles-T128-playbook-rules-a02, dotfiles-T128-playbook-rules-a03]`, the a04 evidence directory in `allowed_files` (a03's no longer), copy rows for the a01 to a04 task copies (C3), `design_review.receipt` round 22.
2. Item 1 (step 6) becomes exactly: "Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker; a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a complete bus read, never from a default-limited one. A seat silent for thirty minutes since its latest bus event for the task (INV-10's figure) gets a bus read, then a PING; a longer silent wait is never the answer. Once plan 007 T718 lands, `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the complete read and the silence check; until then the orchestrator runs `history.sh <team> --limit 1000` and pastes."
3. Item 3 (the three-repeat procedure) becomes exactly: "When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line; until then the orchestrator runs them by hand with a validated slug. Once `dotfiles-T128-gate-evidence-a02` lands, the gate refuses the action without the line; until then the orchestrator refuses it by rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record."
4. Items 2, 4, 5, 6, 7, 8 unchanged (item 7's token tests follow the new sentences; the step-6 fixture changes with item 1).
5. The heading carries the reset; the intro names the three S1 cycles, plan 010 option D and the a03 head `fe34f7db`; the worker's commits stay; one Completion clause (PR #328 stays, the orchestrator's `update-branch` already moved it to `e12872cd`).
6. Nothing else changes: not the premises (re-paste premise 1 with `/usr/bin/grep -n` from a worktree at `origin/main` `e0e2fe62`, per C-18).

## Stop condition

`task-consistency-check.py` C1 to C9 pass on a04 (state what you re-derived: the four copy rows, C7, C9 for every quoted sentence); the differences from a03 are exactly items 1 to 5; items 1 and 3 contain no command text beyond the two named interim commands, no limit, no grammar other than the slug's, and every mechanism they name carries "once … lands" or exists on `origin/main`.

## Output

Write `.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md` and the receipt `.orchestration/validation/dotfiles-T128-playbook-rules-redesign-a03.md` (header; diff summary; checks; the successor's sha256), then `AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-redesign-a03 status=ready_for_review verdict=accept design_sha256=<sha256 of the a04 file> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing any other tracked file; branches; PRs.
