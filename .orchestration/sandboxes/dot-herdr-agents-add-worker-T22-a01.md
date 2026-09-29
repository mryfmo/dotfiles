# T22 sandbox record

## Revision 4

- **Git.** All git work ran in the dedicated worktree `.claude/worktrees/worker-c`, on `feat/herdr-agents-worker-seat`. There is no container or VM isolation. The one stash was tagged (`t22-wip-rebase`), applied by sha, and dropped by tag.
- **Tests.** All herdr and agmsg behaviour was exercised through the unit-test fake harness in temp HOMEs, with fake `herdr`, `identities/join/team/delivery/spawn/despawn/leave.sh`. Real git ran only inside test temp repos.
- **Real system, read-only only:** `spawn.sh`, `lib/spawn-options.sh` and type manifests; `herdr agent start --help` / `workspace create --help`; `identities.sh` for the main checkout and worker-c.
- **Excluded:** no real herdr pane or workspace command, no `join`/`leave`/`delivery` against the `dotfiles` team, no `make update`/`chezmoi apply`, no local bats, no merge, and no force push.
