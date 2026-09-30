# T44 report: allow all Unix sockets (and the uv cache) in the Claude sandbox (dot-sandbox-unix-sockets-T44-a01)

- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 49f69bc1ec6878221d9dfac666610279be04cf2eaa00db310cfd1facdab783dc (sha256 verified against the main-checkout file and the `origin/main:` blob at f45cf73)
- branch: `fix/sandbox-unix-sockets` from origin/main f45cf73
- commit: c2c1f62
- PR: https://github.com/mryfmo/dotfiles/pull/215 (head c2c1f62; CI 12/12 pass incl. the CodeRabbit status check, nix skipped; MERGEABLE; origin/main has since gained one .orchestration-only commit c6241bb, not merged in so CI did not rerun)

## Changes

1. **`home/dot_agents/agent-config.yaml` `claude.sandbox`:**
   - `network.allowAllUnixSockets: true`, with a comment:
     - Linux/WSL2 ignore `allowUnixSockets`, and the seccomp filter otherwise blocks every Unix socket.
     - The herdr control-plane socket (herdr, agmsg-dispatch, herdr-agents) and the keyring D-Bus socket `gh` reads its token through must be reachable from sandboxed Bash.
     - File and network isolation are unchanged.

     `allowUnixSockets` (herdr socket, macOS) stays.
   - New `filesystem.extra_allow_write: [~/.cache/uv]`. Its comment names the uv cache and calls it a filesystem relaxation limited to that directory (items 7 and 8).
   - Scope note: the allowed-files line limits this file to "the sandbox.network block only". Item 8 explicitly requires the new `claude.sandbox.filesystem.extra_allow_write` list, so it also sits in the sandbox block, as a sibling of `network`. No other key was touched.
2. **`scripts/generate-agent-configs.py` `render_claude_sandbox`:** `network.allowAllUnixSockets` is rendered only when present (boolean passthrough). `filesystem.allowWrite` = Codex writable roots followed by `sandbox.filesystem.extra_allow_write` (default `[]`). The generator does not fail when either key is absent.
3. **`scripts/validate-agent-assets.py` `validate_claude_sandbox`:** if present, `allowAllUnixSockets` must be a boolean. allowWrite entries beyond the Codex roots must be absolute or `~/` paths without `*?[]{}`.
4. **`home/.chezmoitemplates/claude-settings-managed.json`:** regenerated; `--check` ok. The rendered block is `network.allowAllUnixSockets: true`, plus `~/.cache/uv` after the 4 agmsg roots.
5. **Tests:**
   - `test_claude_sandbox_allow_all_unix_sockets_must_be_boolean`: accepts true and false, rejects `"true"`.
   - `test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs`: accepts `~/.cache/uv`, rejects relative, `~cache`, a glob and a non-string.
   - `test_claude_sandbox_renders_optional_socket_and_extra_write_keys` (generator): renders correctly with the keys absent and with them present.
6. **README "Claude Code sandbox" section only:**
   - allowWrite now also covers `extra_allow_write` (`~/.cache/uv`).
   - A new sentence says `allowAllUnixSockets` is `true`, so on Linux all local Unix sockets are allowed for the herdr control plane and the `gh` keyring D-Bus socket, while file and network isolation stay in force.
   - The operator-visible effect now names the uv cache and the reachable Unix sockets.
   - The PR-feedback and generator paragraphs (touched by the still-open T43 PR #214) were not edited.
7. **Checks:** `make unit-test` 613 OK; `make validate-agent-assets` ok; `uv run --with pyyaml scripts/generate-agent-configs.py --check` ok. `make render-check` does not exist on this base yet (it lands with T43 #214).

`allowedDomains` and `failIfUnavailable` are untouched.

## Shared-repo hazard found and reported (PONG at start of T44)

- `/home/moriya/Workspace/dotfiles/.git/config.lock` exists as a read-only, zero-byte file (mtime 06:01 JST), and no process holds it. It looks like a stub the sandbox's bubblewrap leaves on disk when it protects `.git/config` for linked worktrees.
- It blocks every git config write in the shared repo, sandboxed or not.
- My sandboxed `git switch -c fix/sandbox-unix-sockets origin/main` half-applied: the branch ref, index and tree moved, but HEAD and the tracking config did not.
- I repaired only this worktree's HEAD with `git symbolic-ref HEAD refs/heads/fix/sandbox-unix-sockets`, a per-worktree file with no config write. T43's 1843dd1 was untouched throughout.
- I did not delete the lock. Every later git command in T44 ran outside the sandbox, and the push used `git push origin HEAD` without `-u`, so no config write was needed.

## Notes

- Commands that needed the network, the uv cache or git config ran outside the sandbox through the normal permission prompt: make targets, `uv run`, `gh`, `git push`, and edits in the main checkout's `.orchestration`.
- The understand-anything auto-update hook fired after the commit. I did not act on it, per the task note and the T43 rule: hook fired; not acted on.

[memory:decision] T44: the Claude Code sandbox sets
`network.allowAllUnixSockets: true` so the herdr control plane works from
sandboxed Bash on Linux; file and network isolation are unchanged
(operator 2026-09-29, from T39 live E2E leg 1).

## CompactionDB (main checkout)

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T44: the Claude Code sandbox sets network.allowAllUnixSockets: true so the herdr control plane works from sandboxed Bash on Linux; file and network isolation are unchanged (operator 2026-09-29, from T39 live E2E leg 1)."
5ab13bbc-7eb0-41cf-a99c-9aa95b8a51b3
```

## Effects

None outside the repository working tree. The settings take effect when the operator next runs `make update`.

cost: 0 subagent dispatches; orchestrating-session token/cost figures n/a.
