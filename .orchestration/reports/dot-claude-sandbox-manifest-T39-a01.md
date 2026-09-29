# T39 report: Claude Code sandbox from the shared manifest (dot-claude-sandbox-manifest-T39-a01)

- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 15bf3dcbe2ba38f6b28582d1693272f035fea5a18c581a6dcd84d5de1c9fdcc0 (sha256 verified against the main-checkout file and the `origin/main:` blob at d2f19ec)
- branch: `feat/claude-sandbox-manifest-r2` from origin/main d2f19ec. worker-c was clean and detached at d2f19ec after T38.
- PR: https://github.com/mryfmo/dotfiles/pull/211 (head 271e8ef = 2815528 + merge of origin/main 83b8567, which adds only .orchestration files; no force push; MERGEABLE; CI 14/14 pass including the three bats `test` jobs, nix skipped)
- `feat/claude-sandbox-manifest` / #179 were not touched and not closed.

## Commits

1. **841e12b** `feat(agents): carry PR #179 (Claude Code sandbox from the manifest) onto main`
   - `git merge --squash origin/pr/179` (b729f54).
   - The three superseded AppArmor files were un-staged and deleted *before* this commit: `install/ubuntu/common/bwrap_apparmor.sh`, `home/.chezmoiscripts/ubuntu/run_once_before_51-setup-bwrap-apparmor.sh.tmpl` and `tests/install/ubuntu/common/bwrap_apparmor.bats`. So no commit ever contains them. This follows the forbidden-actions rule "creating or keeping" them.
   - Conflicts:
     - `agent-config.yaml` header: main's lines kept, plus the PR's continuation "The Claude sandbox allowWrite list is rendered from the same entries."
     - `dependencies.bats`: count set to 18.
     - `check-tools.sh`: main's `check_agmsg` and "AppArmor" section kept, plus a presence-only `check_claude_sandbox` under "Claude Code sandbox" after "AppArmor". It reports bwrap and socat on PATH, WARNs when missing, and has no sysctl or profile logic.
     - `test_runtime_health.py`: main's `APPARMOR_USERNS_SYSCTL` fixture unchanged, and the PR's sysctl/profile fixture removed. The sandbox test is presence-only: missing socat warns, both present gives `warnings=0`, and Darwin is not applicable. `bwrap`/`socat` stay in the doctor fixture's fake command list.
     - README: the PR's section placed before `### agmsg`, next to its original position after "Agent review and permission assets".
   - The managed settings were regenerated with `uv run --with pyyaml scripts/generate-agent-configs.py`, never hand-edited. `allowWrite` lists all four Codex roots, including `agmsg/ext-tools`.
   - 609 tests OK; validate ok.
2. **2815528** `feat(agents): stage the Claude sandbox defaults and allow the herdr socket`
   - `failIfUnavailable: false` (two-stage comment).
   - New `network.allowUnixSockets: [~/.config/herdr/herdr.sock]`, with a comment on the macOS-only scope and the messaging-socket gap.
   - The generator renders `allowUnixSockets`.
   - `validate_claude_sandbox`: `failIfUnavailable` must be a boolean (it was "must be true", which would have rejected the approved value), and `allowUnixSockets` entries must be absolute or `~/` paths without `*?[]{}`. New test `test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs` rejects six bad entries.
   - README section rewrite (see below). Parity item 9 now matches the validator; it previously said "fail closed when unavailable".
   - 610 tests OK; validate ok; render check ok; shellcheck and shfmt (repo flags) clean.

## Final sandbox block (rendered)

`enabled: true`, `failIfUnavailable: false`, `autoAllowBashIfSandboxed: true`,
`allowUnsandboxedCommands: true`, `excludedCommands: []`,
`filesystem.allowWrite` = the four `{{ .chezmoi.homeDir }}/.agents/skills/agmsg/{db,teams,run,ext-tools}`,
`network.allowedDomains` = github.com, api.github.com, uploads.github.com, objects.githubusercontent.com, codeload.github.com,
`network.allowUnixSockets` = `~/.config/herdr/herdr.sock`. The verbatim JSON is in the validation file. No other key was added or altered.

## allowUnixSockets: documented schema and gaps

From the settings reference (verbatim excerpts in the validation file):
- The key is `sandbox.network.allowUnixSockets`, typed as an array of strings, each a socket path.
- The documented example uses a `~/` path (`"~/.ssh/agent-socket"`). No env-var expansion is documented; `~/` expansion is documented for the filesystem path lists.
- **Platform gap:** "Claude Code ignores this list on Linux and WSL2, where the seccomp filter can't inspect socket paths; use `allowAllUnixSockets` there instead." On this Ubuntu host the herdr entry therefore has no effect; it only applies on macOS.
  - When the optional seccomp filter is present on Linux, sandboxed commands cannot open any Unix socket unless `allowAllUnixSockets` is true. That key is not in the approved list, so it was not added.
  - In practice a sandboxed `herdr`/agmsg-dispatch call on Linux may fail and fall back to an unsandboxed retry behind a prompt (`allowUnsandboxedCommands: true`).
  - When the filter is missing, sockets are not blocked.
  - Decision needed later: `allowAllUnixSockets` or `excludedCommands` for herdr, after live E2E.
- **Messaging-socket gap:** `CLAUDE_CODE_MESSAGING_SOCKET` is a per-process path set at runtime (this session: `/run/user/1000/cc-socks/<pid>.sock`). The schema has no env-var or glob form for it, and our validator rejects globs, so only the herdr socket was added. The task's `[memory:decision]` text, recorded verbatim, says "herdr/Claude unix sockets allowed". In fact only the herdr socket is listed.

## README

- The "### Claude Code sandbox" section says `failIfUnavailable` is `false` for the first stage and adds the `allowUnixSockets` sentence.
- The `/etc/apparmor.d/bwrap` paragraph is replaced by a pointer to main's bwrap-userns paragraph ("Agent review and permission assets") and the doctor wording.
- The `claude --settings '{"sandbox": {"failIfUnavailable": false}}'` workaround is removed, since that is now the default.
- New paragraph: "Operator-visible effect: after the next `make update`, Claude Code Bash commands run confined to the working directory, the session `$TMPDIR`, and `allowWrite`. Network hosts other than the listed GitHub domains prompt. A command that fails inside the sandbox may be retried unsandboxed after a normal permission prompt. Missing `bwrap` or `socat` only warns while `failIfUnavailable` is `false`."

## Notes

- The understand-anything auto-update hook fired after each commit. I did not act on it: `.ua/**` is forbidden.
- No `sudo`, `make update`, `chezmoi apply` or local bats was run. The bats count change (18) is validated by CI.

[memory:decision] T39: the Claude Code sandbox is rendered from
`claude.sandbox` in agent-config.yaml (enabled, failIfUnavailable=false for
the first stage, autoAllowBashIfSandboxed, allowUnsandboxedCommands,
allowWrite mirrored from the Codex writable roots, GitHub-only
allowedDomains, herdr/Claude unix sockets allowed) with bubblewrap+socat as
Ubuntu prerequisites and a presence-only doctor check; PR #179's own
`/etc/apparmor.d/bwrap` profile is dropped in favour of main's bwrap-userns
(T30). Flipping failIfUnavailable to true waits for live E2E (operator
2026-09-29).

[memory:failure] T39: `sandbox.network.allowUnixSockets` is macOS-only (ignored on Linux/WSL2) and cannot express the per-process Claude messaging socket; on Linux only `allowAllUnixSockets` opens Unix sockets under the seccomp filter.

## CompactionDB (main checkout)

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T39: the Claude Code sandbox is rendered from claude.sandbox in agent-config.yaml (enabled, failIfUnavailable=false for the first stage, autoAllowBashIfSandboxed, allowUnsandboxedCommands, allowWrite mirrored from the Codex writable roots, GitHub-only allowedDomains, herdr/Claude unix sockets allowed) with bubblewrap+socat as Ubuntu prerequisites and a presence-only doctor check; PR #179's own /etc/apparmor.d/bwrap profile is dropped in favour of main's bwrap-userns (T30). Flipping failIfUnavailable to true waits for live E2E (operator 2026-09-29)."
41736f91-68ac-4412-9874-9960402043ad
```

## Effects

None outside the repository working tree. The settings take effect only when the operator next runs `make update`.

cost: 0 subagent dispatches; orchestrating-session token/cost figures n/a.
