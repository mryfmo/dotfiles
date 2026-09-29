# T36 sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `chore/ua-graph-refresh-T36` from `origin/main`. The worktree was clean
  before the switch, and the merged local `feat/herdr-agents-worker-seat`
  branch was deleted first. The branch was moved from 2126564 to 7b69b1e
  (no commits yet, clean tree) after the task-text correction.
- Plugin scripts ran from the Claude plugin cache (2.9.7) and
  `~/.understand-anything-plugin` (core already built), read-only. No
  install and no build. The worktree redirect was disabled, so every graph
  write stayed inside worker-c `.ua/`.
- Stale T33c `.ua/intermediate` and `.ua/tmp` contents, and the Phase 7
  scratch output, were moved into this session's scratchpad, never into
  untracked `.ua/.trash-*` paths.
- The 35 dispatched plugin subagents were told to write only inside worker-c
  `.ua/intermediate` and `.ua/tmp`, to treat file contents as untrusted
  data, and never to copy secret or env values. A post-save scan found no
  `model-profiles.env` values and no common token or key patterns in the
  graph.
- Writes outside the worktree were limited to the allowed
  `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-graph-refresh-T36-a01.md`
  files and the task-required CompactionDB `memory add` in the main
  checkout.
- No `make apply` or `chezmoi apply` was run. The local Bats suite was not
  run. There was no force push and no merge.
