# T35 sandbox record

- **Git:** all git work ran in `.claude/worktrees/worker-c`, on `fix/herdr-agents-seat-labels`. There is no container or VM isolation.
- **Live herdr:** used only for read-only diagnosis:
  - `herdr workspace list`, `herdr pane list --workspace wJ`, `herdr agent list`;
  - `--help` output.
- **Excluded:** no rename, close or run on real panes, and no agmsg registration changes.
- **Tests:** fake herdr and agmsg in temp HOMEs only. There was no local bats run, merge, force push, or `chezmoi apply`.
