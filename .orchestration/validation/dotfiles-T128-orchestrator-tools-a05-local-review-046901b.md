---
task: dotfiles-T128-orchestrator-tools-a05
head: 046901bcdc92301fac2f81b0ea4f9ca802e1a695
pr: 346
base: df044557655bfd1031faa3b0ad90ca1e1f7f0260
started: 2026-10-13T22:22:45Z
finished: 2026-10-13T22:23:33Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P1] Handle deleted orchestration files in boundary commits — scripts/orchestrator/boundary.sh:41-44
- [P1] Preserve locally deleted tracked files during fast-forward — scripts/orchestrator/ff-main.sh:35-37

```text
Two new repository-management scripts fail on tracked-file deletions, preventing normal boundary commits and fast-forwards while preserving local changes. These are functional regressions in their core workflows.

Full review comments:

- [P1] Preserve locally deleted tracked files during fast-forward — scripts/orchestrator/ff-main.sh:35-37
  When a tracked file is locally deleted, `git diff --name-only` includes it, but this unconditional `mv` fails because the path no longer exists. The script therefore cannot fast-forward while preserving this valid local edit, contrary to the required behavior for locally modified tracked paths in [task.md:123](.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md#L123). Record deleted paths separately, restore the checkout for the merge, and delete those paths again afterward.

- [P1] Handle deleted orchestration files in boundary commits — scripts/orchestrator/boundary.sh:41-44
  If a tracked `.orchestration` file was deleted, `git status` includes its path but `cp` immediately fails because the source no longer exists. Boundary PR creation is therefore blocked for deletions, and simply skipping the copy would also leave the file present in the new worktree. The boundary workflow specified in [task.md:122](.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md#L122) should explicitly remove deleted paths from the temporary worktree.
Two new repository-management scripts fail on tracked-file deletions, preventing normal boundary commits and fast-forwards while preserving local changes. These are functional regressions in their core workflows.

Full review comments:

- [P1] Preserve locally deleted tracked files during fast-forward — scripts/orchestrator/ff-main.sh:35-37
  When a tracked file is locally deleted, `git diff --name-only` includes it, but this unconditional `mv` fails because the path no longer exists. The script therefore cannot fast-forward while preserving this valid local edit, contrary to the required behavior for locally modified tracked paths in [task.md:123](.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md#L123). Record deleted paths separately, restore the checkout for the merge, and delete those paths again afterward.

- [P1] Handle deleted orchestration files in boundary commits — scripts/orchestrator/boundary.sh:41-44
  If a tracked `.orchestration` file was deleted, `git status` includes its path but `cp` immediately fails because the source no longer exists. Boundary PR creation is therefore blocked for deletions, and simply skipping the copy would also leave the file present in the new worktree. The boundary workflow specified in [task.md:122](.orchestration/dotfiles-T128-orchestrator-tools-a05/task.md#L122) should explicitly remove deleted paths from the temporary worktree.
```
