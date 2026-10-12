---
format: 2
task_id: dotfiles-T128-playbook-rules-redesign-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-playbook-rules-redesign-a01 — write the successor task file `dotfiles-T128-playbook-rules-a02` (INV-6 reset of T703 after two worker questions)

Drafted 2026-10-12 by the orchestrator seat. `dotfiles-T128-playbook-rules-a01` reached INV-6's count (`questions=2`: PONG 12:27:06Z on the Bot's three findings, PONG 12:37:00Z on the amended search command) and is withdrawn to design; the redesign is another context's, yours. The worker `claude-standard-dot-a003` holds its prepared work uncommitted on `regime/playbook-rules` (PR #328, head `9b2c02a1`) and continues under the successor id on the same branch and PR (the a06 → a07 precedent).

## Inputs

- `.orchestration/tasks/dotfiles-T128-playbook-rules-a01.md` (amendment 1, sha256 `a28413fa…`), its acceptance record `.orchestration/acceptance/dotfiles-T128-playbook-rules-a01.md`, the two question PONGs (messages 711 and 719 in `history.sh dotfiles-conformance`), the Bot threads 4247933544, 4247933561, 4247933574 on PR #328, the records M-20261012-14 to 16 and C-16 to C-18, plan 007 Phase 0 (schema with `classes:`, the three-repeat procedure line, the replay-environment clause), and the design v20 (`7a067b19…` on `main`; INV-6's clause).

## What the successor says (everything else verbatim from a01 amendment 1)

1. Front matter: `task_id: dotfiles-T128-playbook-rules-a02`, `reset_of: [dotfiles-T128-playbook-rules-a01]`, the evidence directory `.orchestration/dotfiles-T128-playbook-rules-a02/**` in `allowed_files` (and the a01 directory no longer), a threat-table row for the a01 task copy and one for the a02 copy (C3), `design_review.receipt` round 22.
2. Item 3's search: `grep -rl 'classes:.*<class slug>' .orchestration/learning/mistakes/` (`-rl`; the worker's finding), with one sentence that the `classes:` fields land on `main` through the boundary commit that precedes this dispatch, so the rule is testable from `main`.
3. The heading carries the reset; the intro names both questions and the a01 head `9b2c02a1`; the worker's prepared work (task copy, item 5, tests, fixtures) is kept as it is.
4. Nothing else changes: not items 1, 2, 4 to 8, not the premises (re-paste premise 1's grep output as plain `/usr/bin/grep -n` prints it, from a worktree at `origin/main` `683384ea`, per C-18).

## Stop condition

`task-consistency-check.py` C1 to C7 pass on the successor (the orchestrator's checker; state what you re-derived by hand: C3's two copy rows, C7's eight names); the two differences from a01 amendment 1 are exactly items 1 to 3 above; no sentence of the SKILL or AGENTS.md is restated beyond a01's.

## Output

Write `.orchestration/tasks/dotfiles-T128-playbook-rules-a02.md` (through the permission gate, the main checkout) and the receipt `.orchestration/validation/dotfiles-T128-playbook-rules-redesign-a01.md` (header; the diff summary a01 amendment 1 → a02; the checks; the successor's sha256), then `AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-redesign-a01 status=ready_for_review verdict=accept design_sha256=<sha256 of the a02 file> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing any other tracked file; branches; PRs.
