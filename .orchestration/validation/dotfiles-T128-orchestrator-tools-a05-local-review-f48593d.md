---
task: dotfiles-T128-orchestrator-tools-a05
head: f48593d6e89e31cbbcdd785ffcf1e6b71ffe34b3
pr: 350
base: 7d58d6cd1d98463f582e40f1bf0eb7bdeb4c6f4e
started: 2026-10-14T00:41:47Z
finished: 2026-10-14T00:43:14Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Align the gate invocation with the declared trust-boundary control — scripts/orchestrator/orch-gate.sh:66-67
- [P2] Restore the review worktree when setup fails — scripts/orchestrator/orch-gate.sh:55-59

```text
The gate wrapper diverges from its reviewed trust-boundary specification and can leave the shared review worktree corrupted when evidence setup fails. Both issues should be addressed before merging.

Full review comments:

- [P1] Align the gate invocation with the declared trust-boundary control — scripts/orchestrator/orch-gate.sh:66-67
  This bypasses `make require-crit-review` and directly executes the Python guard, while the task’s trust-boundary row explicitly says this wrapper “calls make require-crit-review as it is.” That leaves the implemented control materially different from the reviewed threat table, which repository policy requires reporting and reconciling for trust-boundary code; either amend the task/control before landing or restore the declared invocation. See `.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md:37-38`.

- [P2] Restore the review worktree when setup fails — scripts/orchestrator/orch-gate.sh:55-59
  Once checkout of the PR head succeeds, any failure in `mkdir` or `cp` exits immediately under `set -e`, skipping the cleanup and checkout at lines 69–70. A permissions, disk-space, or interrupted-copy failure therefore leaves the shared review worktree detached at the PR head with partially copied evidence, causing later audits or gates to run from unexpected state; install a cleanup trap immediately after the checkout so restoration occurs on every exit path.
The gate wrapper diverges from its reviewed trust-boundary specification and can leave the shared review worktree corrupted when evidence setup fails. Both issues should be addressed before merging.

Full review comments:

- [P1] Align the gate invocation with the declared trust-boundary control — scripts/orchestrator/orch-gate.sh:66-67
  This bypasses `make require-crit-review` and directly executes the Python guard, while the task’s trust-boundary row explicitly says this wrapper “calls make require-crit-review as it is.” That leaves the implemented control materially different from the reviewed threat table, which repository policy requires reporting and reconciling for trust-boundary code; either amend the task/control before landing or restore the declared invocation. See `.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md:37-38`.

- [P2] Restore the review worktree when setup fails — scripts/orchestrator/orch-gate.sh:55-59
  Once checkout of the PR head succeeds, any failure in `mkdir` or `cp` exits immediately under `set -e`, skipping the cleanup and checkout at lines 69–70. A permissions, disk-space, or interrupted-copy failure therefore leaves the shared review worktree detached at the PR head with partially copied evidence, causing later audits or gates to run from unexpected state; install a cleanup trap immediately after the checkout so restoration occurs on every exit path.
```
