# T44 sandbox record

- This worker session now runs inside the Claude Code Bash sandbox, the T39
  settings live since `make update`. Pure file edits and the targeted unit
  test runs happened inside it.
- Anything needing the uv cache, `gh` (keyring socket), `git push`, or git
  metadata writes, plus the main-checkout `.orchestration` artifacts, ran
  outside the sandbox through the normal permission prompt. None of it was
  escalated agent-to-agent.
- The `.git/config.lock` stub (see report) was left in place and reported to
  the orchestrator. The worktree HEAD was repaired with a per-worktree
  `git symbolic-ref`.
- No `make update`/`chezmoi apply`, no local Bats, no force push, no merge.
  No `.ua/**`, hooks, settings (other than the generated template) or
  permgate changes.

## Revision 2

- worker-c switched from `feat/orchestration-rules-T43` (merged as c5dd169) to `fix/sandbox-unix-sockets` (c2c1f62, matching origin). 663ddbd merges origin/main and dcb8839 is the fix; pushed without `-u`.
- Unsandboxed for the stated limits: the generator write and make targets (uv cache; unit-test socket test), `git push`, `gh`, and the main-checkout CompactionDB entry and artifact appends. No `make update` and no `chezmoi apply`.
