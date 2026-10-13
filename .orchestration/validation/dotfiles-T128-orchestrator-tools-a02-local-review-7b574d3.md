---
task: dotfiles-T128-orchestrator-tools-a02
head: 7b574d323c4ec30d5982755bc6f9fe627264de5f
pr: 346
base: 73f56c159094baae810605848ff040e31dae44e7
started: 2026-10-13T16:15:00Z
finished: 2026-10-13T16:16:08Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve deletions in boundary commits — scripts/orchestrator/boundary.sh:41-44

```text
The boundary automation cannot create a boundary PR containing deleted files and mishandles renames, so a supported class of orchestration changes fails or produces the wrong commit.

Review comment:

- [P2] Preserve deletions in boundary commits — scripts/orchestrator/boundary.sh:41-44
  When a `.orchestration` file is deleted, `git status` still lists its path, but this unconditional `cp` fails because the source no longer exists; for a rename, only the new path is copied and the old path remains in the worktree, producing a duplicate instead of a deletion. Handle deleted/renamed status entries explicitly (prefer a NUL-delimited status format) so boundary PRs reproduce the complete change. The boundary threat row is marked closed only by a validator-failure test, which does not cover this behavior ([task.md:28-30](.orchestration/dotfiles-T128-orchestrator-tools-a02/task.md#L28-L30)).
The boundary automation cannot create a boundary PR containing deleted files and mishandles renames, so a supported class of orchestration changes fails or produces the wrong commit.

Review comment:

- [P2] Preserve deletions in boundary commits — scripts/orchestrator/boundary.sh:41-44
  When a `.orchestration` file is deleted, `git status` still lists its path, but this unconditional `cp` fails because the source no longer exists; for a rename, only the new path is copied and the old path remains in the worktree, producing a duplicate instead of a deletion. Handle deleted/renamed status entries explicitly (prefer a NUL-delimited status format) so boundary PRs reproduce the complete change. The boundary threat row is marked closed only by a validator-failure test, which does not cover this behavior ([task.md:28-30](.orchestration/dotfiles-T128-orchestrator-tools-a02/task.md#L28-L30)).
```
