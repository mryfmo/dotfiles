---
format: 2
task_id: dotfiles-T133-herdr-agents-eperm-a01
kind: code
security: false
dispatch_status: frozen-superseded-by-phase-2
allowed_files:
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T133-herdr-agents-eperm-a01/**
after: []
---

# AGMSG-TASK dotfiles-T133-herdr-agents-eperm-a01 — herdr-agents reports the EPERM it meets (owner stub)

Owner stub written 2026-10-22T02:55Z by the orchestrator seat (D-024-72, handoff R8-3). When a Herdr query from a sandbox fails with `PermissionDenied` (Linux Claude sandbox, Codex sandbox), `herdr-agents` currently reports "several Herdr workspaces are labeled …; refusing"; it must print the query's error and exit non-zero instead. One red-then-green fixture in tests/unit/test_herdr_agents.py with a fake `herdr` that answers EPERM. Never dispatched as a stub. Frozen 2026-10-22T03:58Z (D-024-79): superseded by phase 2 (hcom bus and omp), not authored unless the cutover slips.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
