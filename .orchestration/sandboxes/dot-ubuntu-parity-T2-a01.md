# dot-ubuntu-parity-T2-a01 sandbox

No OpenSandbox was used. This task ran directly in the operator's registered
git worktree for this work, as instructed by the task's 環境注意 section
(no live-container isolation was requested or needed for shell-script and
Python-config edits plus `mise`/`uv`/`unittest` runs).

- Worktree: `/home/moriya/Workspace/worktrees/chezmoi-ubuntu-parity`
- Branch: `feat/ubuntu-parity` (pre-existing, created at worktree setup)
- Base: `main` at the point this worktree was created (see `git log --oneline main..HEAD` in Validation for the 6 commits added on top)
- No `chezmoi apply`, no push, no PR, no writes under `$HOME`, no
  network-affecting commands beyond `mise install`/`mise lock` scoped to
  this repo's own `home/dot_mise` config dir.
