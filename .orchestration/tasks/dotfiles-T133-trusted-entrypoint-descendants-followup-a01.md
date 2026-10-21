---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-descendants-followup-a01
kind: code
security: true
allowed_files:
  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
  - home/dot_claude/hooks/executable_project-map-reload.sh
  - home/dot_agents/skills/agmsg/scripts/**
  - scripts/format-staged.sh
  - tests/unit/test_trusted_descendants.py
  - .orchestration/dotfiles-T133-trusted-entrypoint-descendants-followup-a01/**
after: [dotfiles-T133-trusted-entrypoint-binding-a01]
owner_of:
  - dotfiles-T133-worker-write-boundary-slice1-a01
  - dotfiles-T133-worker-write-boundary-slice2-a01
  - dotfiles-T133-worker-write-boundary-slice3-a01
  - dotfiles-T133-worker-write-boundary-slice4-a01
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-descendants-followup-a01 — owner of the descendant execution binding (guard, delivery, formatter, map)

Written 2026-10-21 by the orchestrator seat before the first owner disposition of the P1-15 slices (C-51: the owner task exists before the first advisory row), per re-plan v2 J1 and the allocation draft `.agents/worklog/orchestrator-glue/a04-allocation-r1.md` section 3. `dotfiles-T133-trusted-entrypoint-binding-a01` excludes this work at its line 19 ("Complete guard, delivery and formatter/map descendant binding is outside this split"), so a04's Out of scope and the slice texts name this task instead.

## Scope

Bind the execution of the four descendant families to their declared interpreters, inputs and configuration, with a rejection test per family, after binding-a01 has landed the trusted entrypoint:

1. **Guard**: the installed orchestrator-only guard, its interpreter and the fixed project payload chain (ContextDB hooks, the stop gate, state and attachment operations) and the inputs they consume.
2. **Delivery**: the fixed agmsg delivery operations (session-start, session-end, check-inbox, identities) and the descendants they reach, their executable identities and configuration inputs. Store-driver and plugin authorization stay with the agmsg-hardening owner.
3. **Formatter**: the formatter script and the Ruff/Prettier/Node chain, its configuration selection, executable availability and rejection tests.
4. **Map**: the project-map reload hook and the terminal-browser/runtime descendants, their selected inputs and configuration, and rejection tests.

Out of scope: the legacy PermissionRequest command, its structural validator and isolated execution (binding-a01); version pins (pins-a01); the slices' own routing and screening (their residual rows stay residual for the implemented portion and name this task for the deferred binding).

## Owned rows

The slice records' rows that name this task as owner are read from `## Owned by dotfiles-T133-trusted-entrypoint-descendants-followup-a01` in `.orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice{1,2,3,4}-a01.md`. Deployment that needs complete binding (new guard/delivery/formatter/map descendant execution) waits for this task; the Phase-A deployment of P1-15 keeps the recorded existing-binding allowance and its compensating controls.

## Check and Completion

Dispatched only after binding-a01 merges; the dispatch amendment fixes allowed_files to the files the four families actually execute (listed above as the expected set), adds one threat row per allowed_files entry and per family, and names the rejection test selectors. RESULT lists each family's binding, its test and the deployment check that releases the dependents.

## Checks (pasted by the orchestrator before each send)

```text
(empty until dispatch)
```
