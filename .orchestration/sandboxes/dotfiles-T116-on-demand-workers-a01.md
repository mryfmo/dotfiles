# Sandbox: dotfiles-T116-on-demand-workers-a01

- Isolation: worktree `.claude/worktrees/worker-c` (seat), branch `feat/on-demand-workers` from `origin/main` 02d65ca7 with `git switch -c … --no-track`; shared `.git/config` untouched.
- All edits, shellcheck and unit tests ran inside the Claude sandbox, with commit signing disabled per command (`GIT_CONFIG_*` env, `-c commit.gpgsign=false`) because `~/.ssh` is read-denied; uv with pypi.org/files.pythonhosted.org and mise with registry.npmjs.org/nodejs.org declared; `MISE_STATE_DIR=$TMPDIR/mise-state` for prettier.
- About 30 add-worker tests cannot run in this sandbox (their spawn path's `mktemp` lands in a write-denied `/var/folders`); they fail identically on origin/main here and pass in CI.
- A scratch detached checkout of origin/main under the session scratchpad served the failure baseline and was removed with `git worktree remove --force` (no prune).
- Out-of-sandbox through the permission gate: HTTPS `git push` with the T114 command, `gh pr create/edit/checks/api/run view`, the CompactionDB `memory add`, writing and masking the artifacts in the main checkout, `agmsg-dispatch` (excludedCommands).
- No herdr-agents mode ran against the live Herdr server.
