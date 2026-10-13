---
task_id: dotfiles-T128-gate-evidence-a03
status: reset
redesign_task: dotfiles-T128-gate-evidence-a04
design_sha256: 03a5253d1bc78ad928b5b9bc66cbe9ffada6e6090f732acc76c05a532c40001f
redesign_source: dotfiles-T128-gate-evidence-redesign-a03
reason: INV-6-second-amendment-pre-empted; plan-014-option-A
---

# Reset record: dotfiles-T128-gate-evidence-a03 → a04 (INV-6 pre-empted at the fourth binding row, 2026-10-13 02:40Z)

- **Trigger:** Bot review 5498081103 on the amendment-1 head `82e86e50` (02:24:39Z): thread 4254092805 (P1), the gate counts the ledger the record supplies and never checks it against the swept findings; class `acceptance-record-binding`, the fourth row on the lineage (4248232964 task, 4249544762 head, 4250238714 pr, 4254092805 ledger ↔ swept items) → S7 → plan 014; the fix is task text, so the next amendment would be the second and INV-6's reset. Counters at 03:05:18Z:

```text
task=dotfiles-T128-gate-evidence-a03 tasks=2 amendments=1 questions=1 results=1 withdrawn=1 revises=0 first_result_head=82e86e50057d25493a06943c8c8e65a7b217e54a bot_p1_heads_after_result=0 audits=unknown wall=2026-10-12T15:41:03Z..2026-10-13T02:30:11Z (10:49) source=live
detail: pr=329 authors=claude-deep-dot tasks=01a130c6-4698-7ea7-8817-affb77202c15,01a132f0-1bd8-78fa-807b-21d223fde358 results=01a13318-9338-73e2-898f-f9bb69ec5252 questions=01a132cb-7120-76d3-8253-1acc47540e1c withdrawn=01a1331f-8c60-747b-8374-e930c72147c7 bot_heads=- source=live
```

- **Decision:** the operator chose option A (AskUserQuestion answered between 02:34Z and the withdrawal line of 02:37:48Z): a04 = a03 amendment 1 (`1b8ba5b4…`) plus the coverage sentence (ledger ids ⊇ every swept Codex review comment id ∪ `audit:<sha7>:<n>`, refused with `S6: ledger lacks <ids>`), one fixture, one test; the same worker on PR #329.
- **Redesign:** `dotfiles-T128-gate-evidence-redesign-a03` on the review seat (TASK bus 823, 02:38:32Z); the Codex half reviews the a04 file on the same hash.
- **Worker:** `claude-standard-dot-a002` holds at `82e86e50` (ACCEPTANCE `withdrawn` bus 821, 02:37:48Z; PONG ack bus 822, 02:38:05Z).
- **Anchor:** message 845: `2026-10-13T03:03:28Z: AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-redesign-a03 round=4 status=ready_for_review verdict=accept design_sha256=03a5253d1bc78ad928b5b9bc66cbe9ffada6e6090f732acc76c05a532c40001f receipt=.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a03.md receipt_sha256=e17e527b7d554d5ec12db4b233e004dd1d7bf76ae91a0bd0b6460e2dc8305b43 note=item-10-applied(unbadged+near-match-bodies-in-the-review-body-sweep-fixture,near-match-text-verbatim;exact-set-test-named;twelve-fixtures-170-lines-thirteen-tests);checker-OK;sweep-clean;INV-6-byte-equal`
- **Records (S5):** M-20261012-28 (C-26 amended with the coverage rule); plan 014. Design v24 maps a04 (rounds 26 to 28; v24 `fa2c5157…` names no a04 hash, this record is the anchor).
- **Dispatch:** after round 28 and the boundary commit that lands v24, a04 and this record (INV-2).
