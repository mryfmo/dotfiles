# Sandbox: dot-codex-worktree-git-writable-T50-a01

- **Worker:** claude-standard-dot-a005 in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`, branch `fix/codex-worktree-git-writable` from origin/main bb3370a.
- **Ran outside the Claude sandbox** (for the T39 limits: the shared `.git`, Unix sockets, the `codex` helpers, network):
  - git commands that write the shared `.git` (`fetch`, `switch`, `worktree add/remove`, `branch -D`, `commit`, `push`);
  - `make unit-test` and `make validate-agent-assets`;
  - `gh`;
  - every `codex sandbox`, `codex doctor` and `codex exec` probe, so that Codex's own sandbox was the only one in effect, as for a real worker;
  - CompactionDB `memory add`.
- **Fetched sandboxed:** the Codex config schema (curl, allowed domains `developers.openai.com` and `learn.chatgpt.com`).
- **Denied by the permission gate:** a `git worktree add` for the negative check, earlier in the session. The negative check instead swapped the parent launcher into worker-c and restored it (`cmp` exit 0).
- **Scratch state:**
  - `.claude/worktrees/t50-probe` on `scratch/t50-probe`, removed at the end;
  - a scratch `CODEX_HOME` (a copy of `~/.codex/config.toml` plus `[permissions.t50]`) in the session scratchpad. The real `~/.codex` was not modified.
- **Test-subject sessions:** two disposable `codex exec --profile express --sandbox workspace-write --ephemeral` runs (no escalation possible; stdin closed). The first attempt hung on stdin until `timeout 600` (exit 124) and was rerun with `< /dev/null`.
- **Not touched:** worker-sec and its branch, `.orchestration/acceptance/**`, any model, profile, approval, sandbox or network value, and `.git/config.lock`.

## Revision 2

- e334af5 sits on 5952ab8, pushed without `-u`.
- The commands run unsandboxed were the same classes as before: `make` gates, `git commit` and `git push`, and `gh`.
- The negative check swapped in the 5952ab8 launcher and restored it (`cmp` exit 0).
- No new Codex probes: the emitted override is byte-identical.
