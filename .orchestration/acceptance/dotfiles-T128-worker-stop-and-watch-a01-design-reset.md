---
task_id: dotfiles-T128-worker-stop-and-watch-a01
status: reset
redesign_task: dotfiles-T128-worker-stop-and-watch-a02
design_sha256: 1de19e51b9e23edff9bfc21a64e92a6755ddf247d12c3cf98456bb7629e3878e
redesign_source: dotfiles-T128-worker-stop-and-watch-redesign-a01
reason: INV-6-revises
---

# Reset record: dotfiles-T128-worker-stop-and-watch-a01 → a02 (INV-6, 2026-10-12 02:50Z)

- **Trigger:** after RESULT 664 and the revise-round RESULT 666, three of the four open Bot P2 threads on `e924c5df` need text changes (4244248703, 4244248706, 4244272551); the RESULT carrying them would be revises 2, INV-6's threshold. Counters at the stop (02:24Z paste in the a01 record, plus RESULT 666): tasks 2, amendments 1, questions 1, results 2, revises 1, Bot P0/P1 heads after the first RESULT 0.
- **Cause:** the fix-round-1 widening of the worker's class count (plan S1, `class-count-scope`) consumed the revise round on its own reversal; the three remaining P2s are small wording and contract gaps the Bot found on the revise head (one of them, 4244248703, is the residual wording of the narrowing; 4244248706 is a Message Contract field outside A7's items; 4244272551 restates INV-6's audit source the way a05's bullet had stopped doing).
- **Redesign:** `dotfiles-T128-worker-stop-and-watch-redesign-a01` on the review seat (02:49Z): a02 = A7 (`b0b84598…`) + the three text changes + the contract `head=` token with `tests/fixtures/regime/message-contract.md` in `allowed_files` and the fixture row + a02 bookkeeping + the 4244248692 criterion sentence; checker C1 to C6 before sending; the review seat's `verdict=accept design_sha256=<hash>` is the anchor.
- **Worker:** `claude-standard-dot-a003` holds at `e924c5df` (ACCEPTANCE `under_review`, 02:49Z).
- **Anchor:** RESULT 673 at 02:55:00Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-worker-stop-and-watch-redesign-a01 round=2 status=ready_for_review verdict=accept design_sha256=af519f0f6b250de6a91fceee8bc480721a8316c01be47b904d577bf0042baa8e receipt=none`.
- **Anchor after a02 amendment 1 (plan 008 R2):** RESULT 684 at 04:53:50Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-worker-stop-and-watch-redesign-a01 round=4 status=ready_for_review verdict=accept design_sha256=1de19e51b9e23edff9bfc21a64e92a6755ddf247d12c3cf98456bb7629e3878e receipt=none` (round 3 on `3c308690…` was `revise`: the introduction's 4244248692 sentence still claimed a human-only gate; replaced with the review seat's text; RESULT 673 on `af519f0f…` is the superseded anchor).
