---
task: dotfiles-T128-orchestrator-tools-a04
head: 3e5cad37118dfed6836eb3b1e52541198b43b7d7
pr: 336
base: d25c3df87a92eb8123bbfbb8306d4d4318dddc99
started: 2026-10-13T09:38:23Z
finished: 2026-10-13T09:39:25Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Reject malformed ledger rows before using the record — scripts/regime-counters.sh:130-132

```text
The acceptance-record parser does not enforce the documented ledger-row grammar, so malformed records alter S1 classification instead of being ignored. The remaining reviewed behavior appears consistent with the stated requirements.

Review comment:

- [P2] Reject malformed ledger rows before using the record — scripts/regime-counters.sh:130-132
  When an acceptance record has a `ledger` array containing non-objects, missing/non-string `id` values, or invalid `class` values, this check still accepts the record, suppresses the Bot-title fallback, and may count malformed rows under `class=invalid`. The applicable task contract requires every row to contain a string `id` and a `[a-z0-9-]` class, otherwise the record must be ignored (`.orchestration/dotfiles-T128-orchestrator-tools-a04/task.md#L111`). Validate all ledger entries while loading the record and fall back when any entry is malformed.
The acceptance-record parser does not enforce the documented ledger-row grammar, so malformed records alter S1 classification instead of being ignored. The remaining reviewed behavior appears consistent with the stated requirements.

Review comment:

- [P2] Reject malformed ledger rows before using the record — scripts/regime-counters.sh:130-132
  When an acceptance record has a `ledger` array containing non-objects, missing/non-string `id` values, or invalid `class` values, this check still accepts the record, suppresses the Bot-title fallback, and may count malformed rows under `class=invalid`. The applicable task contract requires every row to contain a string `id` and a `[a-z0-9-]` class, otherwise the record must be ignored (`.orchestration/dotfiles-T128-orchestrator-tools-a04/task.md#L111`). Validate all ledger entries while loading the record and fall back when any entry is malformed.
```
