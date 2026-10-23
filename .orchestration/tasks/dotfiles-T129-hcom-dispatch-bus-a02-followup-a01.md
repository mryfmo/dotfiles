---
format: 2
task_id: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - scripts/orchestrator/bus-history.sh
  - scripts/orchestrator/dispatch.sh
  - tests/unit/test_hcom_dispatch.py
  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01/**
after: [dotfiles-T129-hcom-dispatch-bus-a02]
---

# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 — owner of the hcom-dispatch bus a02 residual rows (owner stub)

Owner stub written 2026-10-22T05:35Z by the orchestrator seat (plan 023 PR C stage 1, D-024-79/81). Owns the residual rows of the a02 threat table (fixture-integrity and metadata automation, the same-UID file-tool residual of design 5.14 item 0 for the private tool directory, the deferred launcher half listed in a01). Never dispatched as a stub; authored after a02 merges from the advisory rows of its acceptance record.

## Owned rows

- Owned requirement (D-024-83, M-20261022-01, C-133, 2026-10-22T06:38Z): the dispatcher's pre-send refuses a `status=revise` line when `scripts/regime-counters.sh <task>` prints an S2 line for the task and the line carries no `waiver=D-024-NN` id; one failing-test selector is named when this stub becomes a text.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
