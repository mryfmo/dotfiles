# T31 sandbox record

- No container or VM isolation was used. Git work used the dedicated worker
  worktree `.claude/worktrees/worker-c` on branch `feat/mosh-and-asset-bumps`,
  created from `origin/main` (dd44b86).
- **No host installs**: no apt/brew/sudo runs; mosh installs are proven by CI
  public-bootstrap (Ubuntu `apt-get install`; macOS runs `brew info` under
  `CI=true`).
- The single live network-touching step was the pins-only
  `bump_release_asset_pins` run in the worktree. It made read-only GitHub API,
  crates.io, and awscli.amazonaws.com HEAD requests, and wrote repo files only
  through `generate-agent-configs.py --set-asset`.
- Unit tests use fake `gh`/`curl`/`uv` with a fixed `UPGRADE_RELEASE_NOW`. The
  mutation baseline ran against a `git archive origin/main` export in the
  scratchpad.
- No `make apply`/`chezmoi apply` was run. The local Bats suite was not run
  (repo policy); the updated `dependencies.bats` runs in CI.
- Revision 2: the branch was rebased onto `origin/main` (6846ab5) as the rev2
  dispatch instructed, and republished with `git push --force-with-lease` to
  the worker's own `feat/mosh-and-asset-bumps` branch. This conflicts with the
  task's "no force push" rule and is flagged in the report. The wrapper
  re-render test ran `chezmoi execute-template` against an empty temp HOME
  (no chezmoi config) with env seams; no apply was run.
