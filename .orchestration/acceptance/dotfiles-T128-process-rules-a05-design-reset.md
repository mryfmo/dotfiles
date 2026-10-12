---
task_id: dotfiles-T128-process-rules-a05
status: reset
redesign_task: dotfiles-T128-process-rules-a06
design_sha256: 90fb32c26f4b1f70aebf44e7cee898e75dd7e273304def9bfaa2d7dff165f9aa
redesign_source: dotfiles-T128-process-rules-redesign-a05
reason: INV-6-questions
---

# Reset record: dotfiles-T128-process-rules-a05 → a06 (INV-6, 2026-10-12 00:34Z)

- **Trigger:** INV-6's question count: two `AGMSG-PONG status=question` on a05 (603 at 23:42Z, 621 at 00:34Z); and the second question asked for a `threat_table` row (`tests/fixtures/regime/*.md`, the expected half of item 10's whole-section oracle; Bot P1 4243885108 on `be0afe7e`), which, added, would be amendment 2. Counters at the stop (`scripts/regime-counters.sh dotfiles-T128-process-rules-a05`, pasted below once run): amendments 1, questions 2, results 1.
- **Cause:** the orchestrator wrote item 10 (amendment 1) without the oracle row for the fixtures, although A7's text received the same row at 00:27Z; the Bot found it on the first head that carried the fixtures. Class `threat-table-missing` (with 4240566259): 2.
- **Redesign:** `dotfiles-T128-process-rules-redesign-a05` on the review seat (dispatched 00:37Z) produces a06 = a05 (`71ca5df0…`) plus the fifth threat-table row (the Bot's remedy text), `reset_of` a05, History, First commit and Completion from `be0afe7e`. The worker's item 10 commit `07b2160b` (five fixtures, `test_regime_rule_sections_are_pinned_whole`) stays on the branch; a06 adds one commit (the task copy and evidence).
- **Worker:** `claude-standard-dot-a003` holds at `be0afe7e` (ACCEPTANCE `under_review`, 00:37Z).
- **Anchor:** RESULT 628 at 00:40:18Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a05 round=2 status=ready_for_review verdict=accept design_sha256=c45a1000651933ad8bf418ba809c5c4f7a4fdd703f358e24a1dc6cff03718d5d receipt=none`.
- **Counters at the stop (00:36Z, `scripts/regime-counters.sh dotfiles-T128-process-rules-a05`, pasted; the second line is the script's S2 line):**
  `task=dotfiles-T128-process-rules-a05 tasks=2 amendments=1 questions=2 results=1 withdrawn=0 revises=0 first_result_head=4af89390945b2f85edd3ef0617600e32fc5056fd bot_p1_heads_after_result=1 audits=unknown wall=2026-10-11T23:32:05Z..2026-10-12T00:00:08Z (0:28) source=live`
  `S2: questions 2 >= 2 source=live`
- **Anchor after a06 amendment 1:** RESULT 634 at 00:56:56Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a05 round=3 status=ready_for_review verdict=accept design_sha256=90fb32c26f4b1f70aebf44e7cee898e75dd7e273304def9bfaa2d7dff165f9aa receipt=none` (round 2 on `c45a1000…` superseded).
