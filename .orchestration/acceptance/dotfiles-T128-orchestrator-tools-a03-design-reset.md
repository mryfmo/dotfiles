---
task_id: dotfiles-T128-orchestrator-tools-a03
status: reset
redesign_task: dotfiles-T128-orchestrator-tools-a04
design_sha256: d0a26050132a32ddc8d3b397b31f3a815bdaed1a55867daa4d81551f15e14fd7
redesign_source: dotfiles-T128-orchestrator-tools-redesign-a02
reason: INV-6-second-revise-pre-empted; threads-4255494133-4255494139-4255494137; local-review-0d19947-finding-1; plan-016-G
---

# Reset record: dotfiles-T128-orchestrator-tools-a03 → a04 (INV-6 pre-empted at the second revise, 2026-10-13 07:xxZ; plan 016 option G′)

- **Trigger:** Codex Bot review 5499708109 (06:40:11Z) on PR #336's second update-branch head `0d199475` (scripts byte-identical to the accepted `ba4d4762`): threads 4255494133 and 4255494139 (`bus-read.sh:51`: closers unbound to the task's endpoints; `closed-historical` missing from the status set) and 4255494137 (`three-repeat.sh:41`: a default-limited memory count printed as the total); the orchestrator's local review of the same head (C-32, `.orchestration/validation/dotfiles-T128-orchestrator-tools-a03-local-review-0d19947.md`): `dispatch.sh:187` validates the record destination after the send. All four are real; a code fix would be a03's second revise.

```text
task=dotfiles-T128-orchestrator-tools-a03 tasks=2 amendments=1 questions=0 results=2 withdrawn=0 revises=1 first_result_head=c8fb09b00bc3e79fdce2f23617c3e6aadaa55e5e bot_p1_heads_after_result=0 audits=unknown wall=2026-10-13T04:25:32Z..2026-10-13T05:36:13Z (1:10) source=live
detail: pr=336 authors=claude-deep-dot tasks=01a13382-2e60-70e0-89e1-ce855fd087b9,01a133b0-b870-7f97-81b1-ad0052979186 results=01a133a7-7d28-7b06-84a5-8080a9b00d38,01a133c2-e4c8-7a25-8472-27a0e11015dd questions=- withdrawn=- bot_heads=- source=live
```

- **Decision:** plan 016 option G′ (operator, 07:16Z): guards first (the local review before the audit, no boundary while a PR awaits its merge, a02 item 6 as the owner of the final head's residual P2, on main before the findings), then the fix under them on the same PR by the same worker.
- **Redesign:** `dotfiles-T128-orchestrator-tools-redesign-a02` on the review seat: a04 = a03 (as on `main`, `ef3b2646…`) + the stop gate's closing rule for bus-read.sh with its history-row grammar table and two tests, the body search and the stated or raised memory cap for three-repeat.sh with its table and test, the record-destination check for dispatch.sh with its test, the four tests in item 2, the Completion clause (one revise round; residual P2 owned by a02 item 6; no boundary until the merge). Confirmed by the Codex half on the same hash.
- **Worker:** `claude-standard-dot-a003` holds at `ba4d4762` (ACCEPTANCE `accepted` 05:36:59Z; the acceptance of a03 stands withdrawn by this reset: its head is not merged); its commits stay; a04 asks for the four fixes, their tests, the a04 task copy and evidence.
- **Anchor:** message 917: `2026-10-13T07:51:23Z: AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-redesign-a02 round=5 status=ready_for_review verdict=accept design_sha256=d0a26050132a32ddc8d3b397b31f3a815bdaed1a55867daa4d81551f15e14fd7 receipt=.orchestration/validation/dotfiles-T128-orchestrator-tools-redesign-a02.md receipt_sha256=6603acd4e28385eefbcf09f359164d5d63b18de96f2258b88ad3a18655f454af`
- **Records (S5):** M-20261012-33 (C-32). Dispatch after the boundary commit that lands a04, a02's change and this record.
