# Sandbox: dotfiles-T114-canonical-clone-reconcile-a01

- Isolation: dedicated linked worktree `.claude/worktrees/worker-c` (manifest worker_worktree), branch `fix/canonical-clone-reconcile` created with `git switch -c ... --no-track origin/main`; shared `.git/config` untouched.
- All edits and validations ran inside the Claude sandbox. Out-of-sandbox actions through the permission gate: `git push origin fix/canonical-clone-reconcile` (failed: no SSH identity), `gh auth status` (not logged in), `ssh-add -l` (no identities), the `ls ~/.config/gh` existence probe, and writing these artifacts to the main checkout plus the agmsg-dispatch PONG.
- Sandbox-caused deviations: commit signing disabled per command (`-c commit.gpgsign=false`, `GIT_CONFIG_*` env for tests) because `~/.ssh/id_ed25519*` is read-denied; `MISE_STATE_DIR=$TMPDIR/mise-state` for the prettier check; pypi.org/files.pythonhosted.org and registry.npmjs.org/nodejs.org declared as allowed_domains for uv and mise.
- A scratch detached checkout of origin/main was created under the session scratchpad for the failure baseline and removed with `git worktree remove --force` (no prune).
- Canonical clone `~/.local/share/chezmoi`: read-only probes only (the boundary check's `git -C` calls).
