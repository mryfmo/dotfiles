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

- `~/Workspace/dotfiles/.git/config.lock` exists as a read-only, zero-byte file (mtime 06:01 JST), and no process holds it. It looks like a stub the sandbox's bubblewrap leaves on disk when it protects `.git/config` for linked worktrees.
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
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T44: the Claude Code sandbox sets network.allowAllUnixSockets: true so the herdr control plane works from sandboxed Bash on Linux; file and network isolation are unchanged (operator 2026-09-29, from T39 live E2E leg 1)."
5ab13bbc-7eb0-41cf-a99c-9aa95b8a51b3
```

## Effects

None outside the repository working tree. The settings take effect when the operator next runs `make update`.

cost: 0 subagent dispatches; orchestrating-session token/cost figures n/a.

## Revision 2 (orchestrator status=revise 03:06:10Z; amendment r2; task_rev 825fdc0a…6e09 verified)

The operator decided on 2026-10-01 to **remove the socket relaxation and keep the uv cache write**. Before switching, worker-c had finished T43 (merged as c5dd169). Commits:
- **663ddbd** merges origin/main b9d15b5 into `fix/sandbox-unix-sockets` (clean auto-merge).
- **dcb8839** is the fix.

There was no force push. PR #215 head is `dcb8839081d3911ceff85577f57c37aaea9efa26` (all CI checks pass, nix skipped; mergeStateStatus CLEAN). The PR is retitled "fix(agents): let the Claude sandbox write the uv cache; keep Unix sockets closed on Linux", and its body is rewritten for revision 2.

1. **Removed** `sandbox.network.allowAllUnixSockets` from:
   - `home/dot_agents/agent-config.yaml`: the key and its 5-line comment. A 3-line comment now records why the allow-all switch stays off, phrased without the key name so the grep below stays empty.
   - the generator passthrough in `scripts/generate-agent-configs.py` `render_claude_sandbox`;
   - the validator's boolean check in `scripts/validate-agent-assets.py` `validate_claude_sandbox`;
   - the rendered `home/.chezmoitemplates/claude-settings-managed.json` (regenerated; only that key changed);
   - the two tests that asserted it: the generator test's `assertNotIn` / `assertIs` lines, and the validator test `test_claude_sandbox_allow_all_unix_sockets_must_be_boolean`.
2. **Kept** `allowUnixSockets: [~/.config/herdr/herdr.sock]` with its macOS-only comment, and `filesystem.extra_allow_write: [~/.cache/uv]` together with its generator rendering, validator check and tests. The generator test still asserts `allowWrite == ["/root-a", "~/.cache/uv"]`.
3. **README "Claude Code sandbox" section:**
   - The `allowAllUnixSockets` sentence is replaced. It now says that Linux and WSL2 ignore `allowUnixSockets` (seccomp cannot inspect socket paths), so `herdr`, `agmsg-dispatch`, `herdr-agents` and `gh` (keyring over D-Bus) run through the normal unsandboxed retry prompt on Linux.
   - It also says `allowAllUnixSockets` is deliberately not used, because with a `docker`-group user or a reachable `systemd --user` bus it turns the auto-approved sandbox into an escape, and links code.claude.com/docs/en/sandboxing#security-limitations.
   - The "Operator-visible effect" paragraph had said "Local Unix sockets, including herdr and the `gh` keyring, are reachable". I corrected it, because that would otherwise be false: on Linux such commands fail inside the sandbox and go through the unsandboxed retry prompt.
4. **For the record** (amendment r2 item 3): the round-1 review accepted the relaxation without weighing docker.sock as an escape, and the security-profile review was not run. Removal narrows the boundary, so no separate review is needed for r2.

**Checks** (verbatim in the r2 validation section, every exit captured directly):
- base-ok after the merge, exit 0.
- `grep -n allowAllUnixSockets` over the manifest, generator, validator and template: **no output, exit=1**. The same over both test files: exit=1.
- Rendered sandbox `network`/`filesystem`:
  - network: `allowUnixSockets` [herdr.sock] and `allowedDomains` [the five GitHub hosts], with no allow-all key;
  - filesystem: `allowWrite` lists the 4 agmsg roots plus `~/.cache/uv`.
- `make render-check`: up to date, exit 0.
- `make unit-test`: 634 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: ok, exit 0.
- `gh pr checks 215`: in the validation file.

**Notes**
- The Understand-Anything hook fired after the commits. I did not act on it.
- `allowedDomains` and `failIfUnavailable` are untouched.
- **Effect** (after the operator's next `make update`): sandboxed Bash gains write access to `~/.cache/uv`. Unix sockets on Linux stay blocked inside the sandbox, which is the status quo before T44.
- **CompactionDB (main checkout):** **911e61c8-e962-4648-84d9-0598702cfa49** supersedes the r1 decision `5ab13bbc-7eb0-41cf-a99c-9aa95b8a51b3`, which says `allowAllUnixSockets: true`. Please drop or ignore 5ab13bbc at consolidation.

[memory:decision] T44 r2: the Claude Code sandbox does not set network.allowAllUnixSockets (with a docker-group user or a reachable systemd --user bus it makes the auto-approved sandbox an escape); on Linux herdr, agmsg-dispatch, herdr-agents and gh use the unsandboxed retry prompt; filesystem.extra_allow_write [~/.cache/uv] stays (operator decision 2026-10-01). Supersedes the T44 r1 decision.

cost (revision 2): 0 subagent dispatches; about 20k context tokens consumed this round (session budget counter; no per-task figure exposed).
