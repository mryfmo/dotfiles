---
task: dotfiles-T128-orchestrator-tools-a04
head: 5b99a7443b255426569724f15822dfb3e248411c
pr: 336
base: d25c3df87a92eb8123bbfbb8306d4d4318dddc99
started: 2026-10-13T08:39:56Z
finished: 2026-10-13T08:41:17Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Bind revise openers to the task's existing endpoints — scripts/orchestrator/bus-read.sh:60-60

```text
The bus reader can incorrectly keep a completed task open when an unrelated endpoint emits a revise acceptance with the same task ID. This violates the documented peer-bound state-transition rule.

Review comment:

- [P2] Bind revise openers to the task's existing endpoints — scripts/orchestrator/bus-read.sh:60-60
  A later `AGMSG-ACCEPTANCE status=revise` from unrelated X→Y endpoints becomes `$o`, so a legitimate RESULT from the original worker to orchestrator no longer closes the task. This contradicts the peer-bound rule that rows between other endpoints neither open nor close a task; the cited test covers only unrelated closers, not unrelated revise openers ([task.md:34-35](.orchestration/dotfiles-T128-orchestrator-tools-a04/task.md#L34-L35)). Select revise openers only when their endpoints match the task's established peer pair.
The bus reader can incorrectly keep a completed task open when an unrelated endpoint emits a revise acceptance with the same task ID. This violates the documented peer-bound state-transition rule.

Review comment:

- [P2] Bind revise openers to the task's existing endpoints — scripts/orchestrator/bus-read.sh:60-60
  A later `AGMSG-ACCEPTANCE status=revise` from unrelated X→Y endpoints becomes `$o`, so a legitimate RESULT from the original worker to orchestrator no longer closes the task. This contradicts the peer-bound rule that rows between other endpoints neither open nor close a task; the cited test covers only unrelated closers, not unrelated revise openers ([task.md:34-35](.orchestration/dotfiles-T128-orchestrator-tools-a04/task.md#L34-L35)). Select revise openers only when their endpoints match the task's established peer pair.
```
