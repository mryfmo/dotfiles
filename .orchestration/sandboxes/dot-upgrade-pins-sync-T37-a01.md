# T37 sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `chore/upgrade-pins-20260929` from origin/main 33452dc. The worktree was
  clean before the switch.
- The canonical clone `~/.local/share/chezmoi` was used read-only
  (`rev-parse`, `status`, `diff`, `hash-object`). It still has its pending
  modifications, untouched.
- Network use was read-only `gh api` / `gh release view` / `gh release
  download -O -` against aws/aws-cli and tomasz-tomczyk/crit. The downloads
  were piped straight to `sha256sum`, and no binary touched disk.
- `uv run --with pyyaml` used an ephemeral uv environment for the render
  check. No `make update`, `make upgrade`, `mise install` or `chezmoi apply`
  was run. No local Bats, no force push, no merge.
- Writes outside the worktree were limited to the allowed
  `.orchestration/…/dot-upgrade-pins-sync-T37-a01.md` files and the
  task-required CompactionDB `memory add` in the main checkout.
