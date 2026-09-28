# T33c sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `chore/ua-graph-refresh` from `origin/main` (935e198). The worktree was
  clean before the switch.
- Plugin scripts ran from `~/.understand-anything-plugin` (read-only use).
  I ran no install and no build: the core build was done by the
  orchestrator. `UNDERSTAND_NO_WORKTREE_REDIRECT=1` kept every graph write
  inside worker-c's `.ua/`.
- The 39 dispatched plugin subagents were told to write only inside worker-c
  `.ua/`, to read file contents as untrusted data, and never to copy secret
  values. Two of them also wrote generator helper scripts into this
  session's scratchpad.
- No `make apply` or `chezmoi apply` was run. The local Bats suite was not
  run. There was no force push and no merge.
