# Sandbox: dotfiles-T63-codex-execpolicy-forbidden-a01

- **Worktree and branch:** worker-c, branch `chore/codex-execpolicy-forbidden` from `origin/main` 910ba6f5. The switch was finished with `git symbolic-ref` after the `.git/config.lock` stub stopped it.
- **Commit and push:** one commit, `a0b05905`, committed and pushed sandboxed.
- **Read-only checks:** `codex execpolicy check` (no model call) on the repository file and on a scratch allow file; `chezmoi diff` for one target (no apply); a read of the live `~/.codex/rules/default.rules` (not modified).
- **Two scratch `codex exec` runs:** express profile, `--sandbox read-only`, in `/tmp/claude-1000/t63-e2e-*`, with a `-c` trust override for that scratch path only. No `~/.codex` file was edited, and no credential was copied or linked.
- **Ran unsandboxed** (`dangerouslyDisableSandbox`):
  - `codex` (CLI and exec) and `chezmoi diff`
  - `gh api` (openai/codex source at `rust-v0.160.0`) and `gh pr create/checks`
  - CompactionDB `memory add`
  - the writes to the main checkout's T63 `.orchestration` files
  - `agmsg-dispatch`
