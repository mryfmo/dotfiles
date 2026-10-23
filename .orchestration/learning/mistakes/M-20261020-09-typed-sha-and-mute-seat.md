---
id: M-20261020-09
date: 2026-10-20
classes: [run-not-recall, delivery-gap]
severity: P2
---

# A typed sha in an amendment line, and a worker's blocked PONG that never reached the bus

**What happened.** (1) TASK 2883 (amendment 1 of regime-ci-token-a01) carried `previous_task_sha256=61a9942b4e74bc53d9f0…`, a value the orchestrator typed from memory; the stored TASK 2870 says `61a9942b4e74bc53129a…`. The shell step printed the mismatch and dispatched anyway. (2) codex-standard-dot-a010 wrote `AGMSG-PONG … status=blocked` (the P1-15 runtime-name question) to `runtime-blocked-pong.txt` at 06:05Z after its outbound dispatch died with the Codex daemon restart of 05:21Z; it read every later PING within seconds, so the seat looked alive while P1-15, the critical path, stood still for nine hours. The project-map subagent found the file (C-103: files, not panes).

**What the rules say.** Run, do not recall: every figure in a line is pasted command output. A worker that cannot send reports `status=blocked`, which presumes a working bus; the regime had no file-side fallback.

**Why the rules did not fire.** send-task.sh verified task_sha256 but not previous_task_sha256; the mismatch print was advisory. No mechanism compared a Codex seat's file artefacts with its bus rows.

**Mechanism.** send-task.sh derives previous_task_sha256 from the store and refuses a mismatch (C-121). `codex-outbox-sweep.sh` lists undelivered AGMSG files per seat and runs at milestones (C-120). The a010 PONG was answered from the file (a04 reset text in authoring; a010 commits its draft for a re-seat).
