# Learning triage: dotfiles-T64-codex-worker-never-network-a01

Candidates only; nothing is promoted.

1. **`codex exec` forces `approval_policy = never`.** It does so even with `-a on-request` and with `on-request` in `config.toml` (rollout `turn_context`). An exec run cannot show the effect of an approval flag. Use `codex debug prompt-input` with the same flags to check how the interactive config resolves.
2. **`codex exec --json` hides code-mode tool calls.** It does not emit `command_execution` items for the model's code-mode `exec` tool calls. The rollout under `~/.codex/sessions/` is the authoritative record of every call and its output. Read it before trusting, or distrusting, the model's summary.
3. **`codex sandbox` is a model-free probe** of a sandbox policy: `codex sandbox -c sandbox_mode=… -c sandbox_workspace_write.…=… -- <cmd>`. Pair it with `codex execpolicy check` for rules.
4. **This corrects T63 learning 2.** A scratch project `.codex/rules/` trusted per invocation does load under `--sandbox workspace-write`: run1 refused `rm -rf` and `sudo` with the scratch rules' justifications.
5. **Codex protects `.git` under a writable root.** It is read-only, so `git fetch` in a plain main clone fails on `.git/FETCH_HEAD`. A linked worktree with the herdr git-metadata roots fetches.
6. **Host-dependent tests.** The regime-boundary tests' `pgrep -f 'crit _serve'` reads the host process table. Unsandboxed runs fail while other seats' crit servers are up. A test-side `pgrep` stub would remove the dependency.
7. **Self-matching `pgrep`.** A `pgrep -f '<pattern>'` probe placed in the same shell command as the tests makes that shell's own argv match. Use a `[c]`-style bracket pattern or a separate command.
