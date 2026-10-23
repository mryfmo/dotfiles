---
format: 2
task_id: dotfiles-T133-agmsg-hardening-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - home/dot_agents/skills/agmsg/scripts/storage.sh
  - home/dot_agents/skills/agmsg/scripts/drivers/**
  - tests/unit/test_agmsg_hardening.py
  - .orchestration/dotfiles-T133-agmsg-hardening-a01/**
after: [dotfiles-T133-worker-write-boundary-slice4-a01]
owner_of:
  - dotfiles-T133-worker-write-boundary-a01
  - dotfiles-T133-worker-write-boundary-slice1-a01
---

# AGMSG-TASK dotfiles-T133-agmsg-hardening-a01 — owner of agmsg store-driver validation and plugin authorization (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51). The a01 record of the worker-write-boundary lineage already carries a section `## Owned by dotfiles-T133-agmsg-hardening-a01 (a task to be written; upstream agmsg)` with the rows text-security:5cbbc03:2 (store-plugin trust: `storage.sh:208-228` selects and sources a writable, store-selected driver) and its widening; a04 line 594 and slice 1's row "agmsg store driver and plugin selection" name this task. The dispatch text is authored later from an upstream-agmsg brief; this stub is never dispatched. The agmsg scripts live under the user's skills directory, so the final allowed_files follow the upstream layout at dispatch time.

## Scope

Validate the store driver name against a closed allowlist before `storage.sh` sources it; authorize plugins only from a trusted, non-writable location; refuse a writable store-selected driver path; one rejection test per route. The static plugin and trusted-plugin denies that P1-15 renders reduce the exposure meanwhile and are recorded as the compensating control.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
