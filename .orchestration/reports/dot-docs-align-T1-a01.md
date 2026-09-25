# dot-docs-align-T1-a01 report

status: ready_for_review

cost: n/a

## Result

- [memory:decision] README lifecycle, Crit, and Herdr command descriptions now match the current implementation and unit assertions, including GitHub extension convergence, CompactionDB sync, final agmsg bootstrap, authoritative Linux Crit handling, and pane-split/agent-start command separation.
- The agent asset updater's shdoc header now covers its actual marketplace, plugin, GitHub extension, pinned release, CompactionDB, and Herdr integration duties; no shell logic changed.
- The parity-policy numbering is sequential.
- [memory:decision] The development image now uses Ubuntu 24.04 without apt Bats. Because Noble owns UID/GID 1000 by default, the Dockerfile reuses/renames that account when requested IDs collide and precreates a user-owned workdir before `USER`; unoccupied IDs retain the add path.

## Files changed for this task

- `README.md`
- `Dockerfile`
- `scripts/update-agent-assets.sh` (file-header comment only)
- `home/dot_agents/README.md`

The pre-existing `dot-herdr-sheldon-T1-a01` worktree changes were preserved.

## CompactionDB

Command:

`python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-docs-align-T1-a01: lifecycle and Herdr documentation now mirrors the actual gh-extension/CompactionDB/agmsg and pane-split/agent-start flows; the Dockerfile uses Ubuntu 24.04, removes apt Bats, reuses the base image default UID/GID 1000 by renaming that account, and precreates a user-owned workdir.'`

Decision ID: `b0c22d42-c6a6-40d0-a705-7ed1927cdc7b`

## Side effects

No persistent side effects outside the repository. All task-created Docker containers, images, and layers in `adh-test` were removed; final counts were zero.
