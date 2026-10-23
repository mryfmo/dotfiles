---
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice2-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - scripts/generate-agent-configs.py
  - home/.chezmoitemplates/claude-worker-settings.json
  - home/.chezmoitemplates/claude-managed-settings.json
  - home/dot_claude-worker/modify_private_settings.json
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_claude_worker_settings.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice2-a01/**
after: [dotfiles-T133-worker-write-boundary-slice1-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice2-a01 — P1-15 slice 2: startup screening and the worker/admin outputs (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat so that slice 1 can name this task as the owner of the obligations it defers (C-51). The dispatch text is authored by `author-loop.sh` from the allocation brief (`.agents/worklog/orchestrator-glue/a04-allocation-r1.md`, slice 2) after slice 1 merges; this stub is never dispatched.

## Scope (from the allocation table)

Register both generated outputs (worker and admin settings) in the same change as their preparation consumer. Implement the single preflight: the S01-S23 startup-source inventory, executable-file contents, S11 discard/regenerate, every launch route, narrow interpreter consumption and the runtime-name classes. The guard and the guarded tracked settings already exist (slice 1). Existing unguarded main-local settings refuse unchanged; accepting those installations waits for slice 3 and the deployment. Administrative content is generated but has no installation target yet. Launcher changes are extracted selectively from the preserved a03 draft (`tools/worker-write-boundary-a01`); documentation and ignore assertions wait for slice 4. No live dependents are released.

## Obligations owned for slice 1

Design 5.14 item 1 (startup enforcement, configuration reloads, races and live refusal), the launch-route regressions of the S11 and executable-file contracts that slice 1 only declares, and the foreign-root refusal identifier (this task's dispatched id replaces a04's).

## Intermediate condition after merge (E2)

`make render-check`, `make validate-agent-assets`, the five E1 modules plus the complete `tests.unit.test_claude_worker_settings` pass; required GitHub CI green; final-head review, audit and security evidence fresh.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
