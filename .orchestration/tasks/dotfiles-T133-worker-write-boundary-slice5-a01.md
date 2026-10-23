---
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice5-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - .claude/settings.json
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice5-a01/**
after: [dotfiles-T133-worker-write-boundary-slice4-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice5-a01 — P1-15 slice 5: activate the tracked hooks on the installed guard (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51) after the third C-80 round of slice 1 (`…-text-security-f4246e9.md.last.md`): switching the tracked hook commands in `.claude/settings.json` to `~/.claude/hooks/orchestrator-only.sh` before that guard is installed removes the stop gate from every session that loads the tracked settings, and `onFailure: block` cannot protect `Stop`. Activation therefore follows provisioning: slice 1 renders the guard template and the migration logic but leaves the tracked commands unchanged; the deployment stage A (`make update`, `make install-managed-settings`, the administrative installation) provisions the guard on the host; this slice switches the tracked references afterwards, with a test that the referenced guard path exists in the rendered deployment inventory before the switch is accepted.

## Scope

`.claude/settings.json`: replace the current tracked hook commands with the fixed guard invocation (exec form, absolute `--manifest` operand, supported `onFailure` block) only for hooks whose guard target the deployment inventory lists as installed; the regression test asserts the inventory check and the unchanged behaviour of hooks without an installed guard.

## Owned for slice 1

The tracked-hook activation and its ordering after stage A (slice 1 row ".claude/settings.json" is out of slice 1's scope and names this task).

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
