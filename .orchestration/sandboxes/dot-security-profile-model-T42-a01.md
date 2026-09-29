# T42 sandbox record

- No container or VM isolation was used. All git work happened in
  `.claude/worktrees/worker-c` on `fix/security-profile-model` from
  origin/main 8f1061f, which was clean before the switch.
- The only generated file was produced by `uv run --with pyyaml
  scripts/generate-agent-configs.py`. No `~/.codex/**` writes, no
  `make update`/`chezmoi apply`, no local Bats, no force push, no merge.
- Network: `git push` of the task branch, `gh pr create` and `gh pr checks`.
- Writes outside the worktree were limited to the listed `.orchestration`
  artifacts and the CompactionDB `memory add`.
