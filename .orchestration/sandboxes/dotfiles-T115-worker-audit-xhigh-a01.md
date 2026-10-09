# Sandbox: dotfiles-T115-worker-audit-xhigh-a01

- Isolation: dedicated git worktree `.claude/worktrees/worker-d`, seat `claude-standard-dot-a002` (Claude Code, `standard` profile), branch `chore/worker-audit-xhigh` from `origin/main` 52e56c89 with `--no-track`; shared `.git/config` untouched.
- Sandboxed commands: every edit, regeneration, validation and unit test ran inside the Claude Code sandbox.
- Sandbox-caused deviations:
  - `uv run --with pyyaml` could not reach pypi.org (network denied, validation attempt 1); re-run with `UV_OFFLINE=1`, pyyaml 6.0.3 from the local uv cache (attempt 2). No `allowed_domains` widening.
  - `mise x node npm:prettier` failed writing `~/.local/state/mise/trusted-configs`; the installed prettier 3.9.9 binary ran directly with mise node 26.10.0 on PATH.
  - Commit signing reads `~/.ssh/id_ed25519.pub`, which is read-denied; the branch commit was made with `-c commit.gpgsign=false` (unsigned, as T114's), and the squash merge makes the commit on `main`.
- Outside the sandbox through the permission gate (Worker Playbook step 4): `git push` (the task's HTTPS + `gh auth git-credential` form), `gh pr create`, `gh pr checks` / `gh api` for the CI and Bot wait, writing and masking these artifacts at their main-checkout paths, the main-checkout CompactionDB `memory add`, and `agmsg-dispatch`.
- No `make update`, `make upgrade`, canonical-clone access, `herdr-agents` invocation, thread resolution or hand edit of a generated file.
