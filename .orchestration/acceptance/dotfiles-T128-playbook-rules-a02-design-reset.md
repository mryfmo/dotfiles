---
task_id: dotfiles-T128-playbook-rules-a02
status: reset
redesign_task: dotfiles-T128-playbook-rules-a03
design_sha256: ee6385184e3db246df45970bf71862525d5fd990aa41f92b2b9d03654d45adb2
redesign_source: dotfiles-T128-playbook-rules-redesign-a02
reason: INV-6-amendments; plan-009-option-A
---

# Reset record: dotfiles-T128-playbook-rules-a02 → a03 (INV-6 pre-empted after S7, 2026-10-12 14:17Z)

- **Trigger:** Bot review 5491652266 on `c4e0bb72` (13:45:41Z): 4248711363 and 4248711371 (P1), rule sentences stating the gate's refusal and the checker as present before either is on `main`; with 4248319926 the class `unlanded-mechanism-stated-as-present` reached three on the T703 artifact, the second S1 cycle (after `search-procedure` at 13:24Z), so plan 007 S7 stopped the orchestrator; the operator chose plan 009 option A (14:0xZ). The fix is task text, so it would be amendment 2 and INV-6's count. Counters at 14:24Z:

```text
task=dotfiles-T128-playbook-rules-a02 tasks=2 amendments=1 questions=0 results=2 withdrawn=1 revises=1 first_result_head=375bae0f90bd167c0393be8088b92cf338657608 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-12T12:49:23Z..2026-10-12T14:01:27Z (1:12) source=live
detail: pr=328 authors=claude-deep-dot tasks=01a13029-1c38-74dc-8c9e-3b67ce8619d3,01a1304c-ec30-7a06-8a55-e748cc59d054 results=01a13045-7220-78c3-858a-dbac6ee1ce62,01a1306b-16d8-74bd-82cb-85866524fd2c questions=- withdrawn=01a13079-f388-7307-86fb-c6d085103e35 bot_heads=- source=live
```

- **Redesign:** `dotfiles-T128-playbook-rules-redesign-a02` on the review seat (TASK 14:18:37Z): a03 = a02 amendment 1 (`07b78f64…`) + the a03 front matter and three copy rows, items 2, 3, 4 in the landing-condition form ("once … lands; until then …"), item 6's successor id, the reset heading and intro, one Completion clause; premise 1 re-pasted from `/usr/bin/grep` at `origin/main` `7cbe5405`; C1 to C9 OK (C9 re-derived by hand; the seat's addendum 14:23:23Z covers item 2).
- **Worker:** `claude-standard-dot-a003` holds at `c4e0bb72` on `regime/playbook-rules` (PR #328; ACCEPTANCE `withdrawn` 14:17:51Z).
- **Anchor:** message at 14:22:24Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-redesign-a02 status=ready_for_review verdict=accept design_sha256=ee6385184e3db246df45970bf71862525d5fd990aa41f92b2b9d03654d45adb2 receipt=.orchestration/validation/dotfiles-T128-playbook-rules-redesign-a02.md receipt_sha256=156c3aaa2710822eb016cfe02391612bd645fd2e8424866ca48a9dd64e56e7ae` (verified: both sha256 match).
- **Records (S5):** M-20261012-19 (C-21); plan 009.
- **Dispatch:** after the boundary commit that lands a03 and this record (INV-2).
