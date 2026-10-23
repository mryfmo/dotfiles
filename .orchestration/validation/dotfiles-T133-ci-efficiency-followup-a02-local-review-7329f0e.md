---
task: dotfiles-T133-ci-efficiency-followup-a02
head: 7329f0eee8f2780c254cd7283209eddb92cacc07
pr: 424
base: b22a5580d0778e57a66d3f75c76e3c55b88701e1
started: 2026-10-19T04:44:02Z
finished: 2026-10-19T04:46:53Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P1] Use an absolute path for cleanup before PATH is pinned — scripts/orchestrator/ci-rerun.sh:42-42

```text
The new cleanup trap introduces an arbitrary-code-execution path when tool resolution fails before PATH is pinned. Syntax checks passed; filesystem-writing tests were not run in the read-only sandbox.

Review comment:

- [P1] Use an absolute path for cleanup before PATH is pinned — scripts/orchestrator/ci-rerun.sh:42-42
  When invoked from a PR checkout with an empty or `.` PATH entry, a missing or rejected tool causes the loop to exit before PATH is pinned. This trap then resolves `rm` through the inherited PATH, executing a checkout-supplied executable with the operator's privileges and credential access instead of failing closed. Use `/bin/rm` in the trap and extend the planted-tools test to cover tool-resolution failure.
The new cleanup trap introduces an arbitrary-code-execution path when tool resolution fails before PATH is pinned. Syntax checks passed; filesystem-writing tests were not run in the read-only sandbox.

Review comment:

- [P1] Use an absolute path for cleanup before PATH is pinned — scripts/orchestrator/ci-rerun.sh:42-42
  When invoked from a PR checkout with an empty or `.` PATH entry, a missing or rejected tool causes the loop to exit before PATH is pinned. This trap then resolves `rm` through the inherited PATH, executing a checkout-supplied executable with the operator's privileges and credential access instead of failing closed. Use `/bin/rm` in the trap and extend the planted-tools test to cover tool-resolution failure.
```
