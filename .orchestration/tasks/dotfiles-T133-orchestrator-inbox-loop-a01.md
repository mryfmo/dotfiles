---
format: 2
task_id: dotfiles-T133-orchestrator-inbox-loop-a01
kind: code
security: false
dispatch_status: frozen-superseded-by-phase-2
allowed_files:
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T133-orchestrator-inbox-loop-a01/**
after: []
---

# AGMSG-TASK dotfiles-T133-orchestrator-inbox-loop-a01 — the SessionStart directive schedules the inbox wakeup when the Monitor tool is absent (owner stub)

Owner stub written 2026-10-22T03:55Z by the orchestrator seat (D-024-77, D-024-78). The `agmsg-orchestration:` directive that `herdr-agents --attach` prints at SessionStart tells the orchestrator to invoke the Monitor tool; its fallback sentence ("If the generic Monitor tool is unavailable … switch to turn delivery or run manual inbox checks") is replaced by an instruction to call the ScheduleWakeup tool with a fixed prompt (read the agmsg inbox with inbox.sh and act on every RESULT, PONG and question; pace 10 minutes while a RESULT or chain is pending, 20 to 30 minutes otherwise) and to re-arm it on every wakeup until the session ends. One red-then-green fixture in tests/unit/test_herdr_agents.py on the printed directive text. The SKILL sentence is the operator's (proposal-skill-readme-sentences.md). Never dispatched as a stub. Frozen 2026-10-22T03:58Z (D-024-79): superseded by phase 2 (hcom bus and omp), not authored unless the cutover slips.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
