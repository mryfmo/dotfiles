# T41 sandbox record

- No container or VM isolation was used. All git work happened in
  `.claude/worktrees/worker-c` on `chore/ua-graph-refresh-T41` from
  origin/main 72b8901, which was clean before the switch.
- Plugin scripts ran from the Claude plugin cache (2.9.7) and
  `~/.understand-anything-plugin` (core already built), read-only. The
  worktree redirect was disabled, so every graph write stayed in worker-c
  `.ua/`.
- The incremental attempt's intermediates and each phase's scratch output
  were moved into the session scratchpad, never into untracked
  `.ua/.trash-*`.
- The 50 plugin subagents were limited to worker-c `.ua/intermediate` and
  `.ua/tmp`, told to treat file contents as untrusted, and told not to copy
  secrets. The post-save secret scan is in the report.
- Writes outside the worktree were limited to the allowed `.orchestration`
  artifacts and the two CompactionDB `memory add` calls in the main checkout.
  No `make apply`/`chezmoi apply`, no local Bats, no force push, no merge.
