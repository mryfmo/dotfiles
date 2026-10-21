# Acceptance: dotfiles-T128-chain-glue-finish-a02

Reset of `dotfiles-T128-chain-glue-finish-a01` (PR #378; D-024-63), anchored by `dotfiles-T128-chain-glue-finish-a01-design-reset.md` (review a011, RESULT 2994). Text sha256 ddb8c53f4bb98a9cd3dc1dfd75d4b65c09b4e548dc1ae9908f0d59bc661bd369 (64 lines; the two R1 lint lines of chain-finish.sh and one fixture; caps 40/120 for the reset's own commits). Dispatched 2026-10-21T10:04Z to claude-standard-dot-a008 (worker-f, wJ:p3) as bus 2996 (read 10:03:19Z), round 1, continuing PR #378's branch `tools/chain-glue-finish` from b09c88c6; overlap_ok=378 (own PR) and 396 (the stale duplicate of #412's branch, ledger class close). Counters before the send (C-126): a01 TASKs=1 revises=4 RESULTs=5 questions=0; a02 all 0.

## Counters (INV-6)

amendments=0 revises=0 questions=0 at dispatch.
- 2026-10-21T21:18Z: a008 RESULT 2999 (status=blocked, regime-only: the a02 text was not on main; head 0e01e270, this reset 4/15 lines, PR-wide 178/290, both red-then-green pairs recorded, 42 tests OK, all required checks green) and PONG 3000 (done). Its note: the selector class in the text was wrong (`ChainGlueTest` -> `ChainIntegrateTest`). Amendment 1 (three selector references, nothing else; 68 lines; sha 3590ab4e5beedbbdb639253a8072776965c3b7c937b92e65117396cf0109e8f0) sent as ACCEPTANCE 3001 (status=revise, round 2, records-only: task.md and result.txt task_copy). The first boundary-29 run was stopped before its push so the amended bytes, not ddb8c53f, reach main; boundary 29 re-run. Counters: amendments=1 revises=1 questions=0.

