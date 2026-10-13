---
task: dotfiles-T128-orchestrator-tools-a02
head: 9ad0c15090d8047917e3d9206a0651acc6912771
pr: 346
base: 73f56c159094baae810605848ff040e31dae44e7
started: 2026-10-13T15:41:31Z
finished: 2026-10-13T15:43:15Z
findings: 4
engine: codex review --base main (profile review, read-only)
---

- [P1] Do not auto-dismiss all CI failures — scripts/orchestrator/fill_sweep.py:23-24
- [P1] Require hashes for tab-delimited TASK messages — scripts/orchestrator/dispatch.sh:80-80
- [P2] Handle deleted orchestration files in boundary PRs — scripts/orchestrator/boundary.sh:41-44
- [P2] Preserve deleted files when fast-forwarding — scripts/orchestrator/ff-main.sh:35-38

```text
The change permits unhashed TASK dispatches, can automatically dismiss genuine CI failures, and breaks documented boundary and fast-forward workflows for deleted files. These behavioral defects should be fixed before merging.

Full review comments:

- [P1] Require hashes for tab-delimited TASK messages — scripts/orchestrator/dispatch.sh:80-80
  When an `AGMSG-TASK` uses the newly accepted tab separator, this check accepts it, but the later `[[ ${line} == "AGMSG-TASK "* ]]` test does not recognize it. A tab-delimited TASK can therefore be sent without `task_file=` or `task_sha256=`, bypassing the integrity check; determine the message kind from the parsed tokens instead of matching a literal space.

- [P1] Do not auto-dismiss all CI failures — scripts/orchestrator/fill_sweep.py:23-24
  When the sweep contains a real warning/failure annotation or failed commit status, these blanket rules label it as a runner notice or non-finding and produce a valid-looking `not-applicable` disposition. That lets the zero-gap audit precondition pass without investigating broken CI; only recognized neutral events should be filled automatically, while other annotations and unsuccessful statuses must remain gaps for explicit disposition.

- [P2] Preserve deleted files when fast-forwarding — scripts/orchestrator/ff-main.sh:35-38
  When a local tracked file has been deleted, `git diff --name-only` includes its path but `mv` immediately fails because the source no longer exists. Thus `ff-main.sh` cannot fast-forward while preserving this ordinary local edit, despite its documented guarantee; represent deletions separately or only move paths that currently exist before restoring the tracked state.

- [P2] Handle deleted orchestration files in boundary PRs — scripts/orchestrator/boundary.sh:41-44
  When the boundary includes a deleted `.orchestration` file, `git status` lists the path but this loop attempts to copy the now-missing source and exits before creating the PR. Since `git add -A` is intended to record deletions, the copy stage must distinguish deleted paths and remove them from the temporary worktree instead.
The change permits unhashed TASK dispatches, can automatically dismiss genuine CI failures, and breaks documented boundary and fast-forward workflows for deleted files. These behavioral defects should be fixed before merging.

Full review comments:

- [P1] Require hashes for tab-delimited TASK messages — scripts/orchestrator/dispatch.sh:80-80
  When an `AGMSG-TASK` uses the newly accepted tab separator, this check accepts it, but the later `[[ ${line} == "AGMSG-TASK "* ]]` test does not recognize it. A tab-delimited TASK can therefore be sent without `task_file=` or `task_sha256=`, bypassing the integrity check; determine the message kind from the parsed tokens instead of matching a literal space.

- [P1] Do not auto-dismiss all CI failures — scripts/orchestrator/fill_sweep.py:23-24
  When the sweep contains a real warning/failure annotation or failed commit status, these blanket rules label it as a runner notice or non-finding and produce a valid-looking `not-applicable` disposition. That lets the zero-gap audit precondition pass without investigating broken CI; only recognized neutral events should be filled automatically, while other annotations and unsuccessful statuses must remain gaps for explicit disposition.

- [P2] Preserve deleted files when fast-forwarding — scripts/orchestrator/ff-main.sh:35-38
  When a local tracked file has been deleted, `git diff --name-only` includes its path but `mv` immediately fails because the source no longer exists. Thus `ff-main.sh` cannot fast-forward while preserving this ordinary local edit, despite its documented guarantee; represent deletions separately or only move paths that currently exist before restoring the tracked state.

- [P2] Handle deleted orchestration files in boundary PRs — scripts/orchestrator/boundary.sh:41-44
  When the boundary includes a deleted `.orchestration` file, `git status` lists the path but this loop attempts to copy the now-missing source and exits before creating the PR. Since `git add -A` is intended to record deletions, the copy stage must distinguish deleted paths and remove them from the temporary worktree instead.
```
