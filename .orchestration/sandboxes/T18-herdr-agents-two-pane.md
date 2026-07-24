# T18 sandbox record

- OpenSandbox: not available in this worker environment.
- Fallback isolation: dedicated git worktree `/Users/mryfmo/Workspace/dotfiles-t18` created from `main` on branch `feat/herdr-file-viewer-popup`.
- Main worktree product files were not edited; only these orchestration artifacts were written there.
- Forbidden actions were not performed: no dependency definition changes, no `home/dot_mise/*` or `home/dot_config/herdr/*` edits, no `chezmoi apply`, no live Herdr mutation, no local Bats, and no git push.
- A pytest runner was installed only into the isolated worktree's ignored `.venv`; no project manifest or lockfile changed.
