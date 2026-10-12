---
task_id: dotfiles-T128-gate-evidence-a01
status: reset
redesign_task: dotfiles-T128-gate-evidence-a02
design_sha256: 930f570b9a44114ab68062575b212fdcbd959653cebb1f3f7c710d717f033ddf
redesign_source: dotfiles-T128-gate-evidence-redesign-a01
reason: INV-6-amendments
---

# Reset record: dotfiles-T128-gate-evidence-a01 → a02 (INV-6, 2026-10-12 13:02Z)

- **Trigger:** Bot P1 4248232976 on PR #329 head `5971fffe` (review 5491066199, 13:0xZ): no threat row for the gate's new input `ACCEPTANCE_EVIDENCE`; a missing row is added once as an amendment, and amendment 1 (the row split and the search grammar) was spent, so this would be amendment 2, INV-6's count. The worker asked (PONG question 13:00:25Z, message 725) and held. Counters at 13:08Z:

```text
task=dotfiles-T128-gate-evidence-a01 tasks=2 amendments=1 questions=1 results=0 withdrawn=1 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T11:58:43Z..none (-) source=live
detail: pr=none authors=claude-deep-dot tasks=01a12ffa-b938-700e-8286-8d4a8206fae9,01a1301c-cfc8-7d43-84f5-228ff26106ee results=- questions=01a13033-3240-7d43-8845-fc5d49c09668 withdrawn=01a13035-1e70-7443-8d6a-9fd8cc26a8e4 bot_heads=- source=live
```

- **Redesign:** `dotfiles-T128-gate-evidence-redesign-a01` on the review seat (TASK 13:03:27Z): a02 = a01 amendment 1 (`d1b6fcf3…`) + the a02 front matter and copy rows, the `ACCEPTANCE_EVIDENCE` row closed by `tests/unit/test_require_crit_review.py::test_base_requires_an_acceptance_record_under_acceptance`, the `search:` grammar accepting both grep forms, the 4248232955 disposition sentence, the reset heading and intro, one Completion clause (PR #329 stays); premises 1 to 3 re-pasted from `/usr/bin` tools at `origin/main` `4cf1d4e2`.
- **Worker:** `claude-standard-dot-a002` holds its four in-lane fixes uncommitted on `regime/gate-evidence` (ACCEPTANCE `withdrawn` 13:02:35Z; PONG alive 13:05:13Z).
- **Anchor:** message at 13:07:04Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-redesign-a01 status=ready_for_review verdict=accept design_sha256=930f570b9a44114ab68062575b212fdcbd959653cebb1f3f7c710d717f033ddf receipt=.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a01.md receipt_sha256=f4a10d81a9c89262073375d3e8d81351c255dc949da9ff03e1f40a0a588c84c6` (verified: both sha256 match; C1 to C7 OK; INV-6 byte-equal).
- **Records (S5):** M-20261012-17 (C-19).
- **Dispatch:** after design v21 (the a02 map entry, one pair round) and the boundary commit that lands v21, this record and the successor (INV-2).
