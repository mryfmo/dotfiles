---
task_id: dotfiles-T128-gate-evidence-a02
status: reset
redesign_task: dotfiles-T128-gate-evidence-a03
design_sha256: 686806a1b6cff143eef371f518098ac8b926fbe91462c1f8a5ac67d6e07c482e
redesign_source: dotfiles-T128-gate-evidence-redesign-a02
reason: INV-6-amendments; plan-011-option-F
---

# Reset record: dotfiles-T128-gate-evidence-a02 → a03 (INV-6 pre-empted after the second S1 cycle, 2026-10-12 15:25Z)

- **Trigger:** Bot review 5492641317 on the merge head `4e2266aa` (round 4): 4249544748 and 4249544762 (P1), 4249544794 (P2), all edges of the gate's prose parsing of the acceptance record; `acceptance-dispositions` at three (4248232988, 4248697668, 4249544748), the second class at three on T702 → S7; the operator chose plan 011 option F. The fix is task text, so it would be amendment 2 and INV-6's count. Counters at 15:33Z:

```text
task=dotfiles-T128-gate-evidence-a02 tasks=2 amendments=1 questions=0 results=2 withdrawn=1 revises=1 first_result_head=d5d6c9b1b22c32e483f76ed2d313571a487aa16a bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-12T13:17:02Z..2026-10-12T15:17:19Z (2:00) source=live
detail: pr=329 authors=claude-deep-dot tasks=01a13042-6cb0-792f-8474-d9323a0b021d,01a13083-cb10-7000-8584-7468ba07059d results=01a13078-7c88-749e-8060-dd5522825f77,01a130b0-8c18-7cfc-8705-696d841733c6 questions=- withdrawn=01a130b7-c7a8-7bc0-8477-9f23515185a5 bot_heads=- source=live
```

- **Redesign:** `dotfiles-T128-gate-evidence-redesign-a02` on the review seat (TASK 15:26:08Z): a03 = a02 amendment 1 (`241aec12…`) + the a03 front matter and three copy rows, item 2 as the acceptance-record front-matter contract (`yaml.safe_load`, `task`, `head` = HEAD, `pr`, `ledger`, `searches` with recomputed sets, `audit_findings`; `AUDIT_DISPOSITIONS` retired), item 1's audit findings routed through `audit_findings`, fixtures as YAML (six, under 90 lines), item 5 with the three threads, the reset heading and intro; premises 1 to 3 replayed at `origin/main` `e0e2fe62`; C1 to C9 OK (C8 by hand); INV-6 byte-equal.
- **Worker:** `claude-standard-dot-a002` holds at `61d90302` (PR #329 head `4e2266aa`; ACCEPTANCE `withdrawn` 15:25:23Z, PONG ack 15:25:30Z).
- **Anchor:** message at 15:31:07Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-redesign-a02 status=ready_for_review verdict=accept design_sha256=686806a1b6cff143eef371f518098ac8b926fbe91462c1f8a5ac67d6e07c482e receipt=.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a02.md receipt_sha256=19e7b1eb85a8c4b87cea57838351a64f6a25d4152255a003e57039d24e47e5fd` (verified: both sha256 match).
- **Records (S5):** M-20261012-22 (C-24); plan 011. Design v22 maps a03 (round 25).
- **Dispatch:** after round 25 and the boundary commit that lands v22, a03 and this record (INV-2).
