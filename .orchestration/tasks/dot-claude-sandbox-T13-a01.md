# AGMSG-TASK dot-claude-sandbox-T13-a01: manage the Claude Code Bash sandbox in the shared manifest, symmetric with the Codex workspace-write sandbox (plan part F)

Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/melodic-conjuring-sifakis.md` §F.
Repo (your worktree): `/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10`, branch `feat/claude-sandbox-manifest` created with `git switch -c feat/claude-sandbox-manifest origin/main` once the T10 branch is pushed and the tree is clean. You are `claude-standard-dot-a003`.

## Problem (verified 2026-09-25)

- Codex workers run under `sandbox_mode = workspace-write`, `network_access = false`, with the agmsg store dirs as extra `writable_roots` — all rendered from `codex.sandbox_workspace_write` in `home/dot_agents/agent-config.yaml` and checked by `validate-agent-assets.py`.
- Claude Code has an equivalent native sandbox (`sandbox` key in settings.json; bubblewrap + socat on Linux), but the manifest, `generate-agent-configs.py`, the managed template `home/.chezmoitemplates/claude-settings-managed.json`, the validator, the installers and `make doctor` know nothing about it. Since `worker_kind` became `claude`, the worker's write confinement was silently lost, and every Bash call prompts because nothing is sandboxed.
- Host facts: `/usr/bin/bwrap` present, `socat` missing, Ubuntu 24.04.5 with `kernel.apparmor_restrict_unprivileged_userns = 1` and no bwrap AppArmor profile → the sandbox cannot start on this host until the installer provides the prerequisites.

Official reference (read it first): https://code.claude.com/docs/en/sandboxing and https://code.claude.com/docs/en/settings. Key facts already extracted: defaults write-allow = cwd + session `$TMPDIR` + `permissions.additionalDirectories`; `autoAllowBashIfSandboxed` (default true) skips the bare-Bash prompt in manual/auto modes but **not** in plan mode; `deny` rules and content-scoped `ask` rules still apply; `filesystem.disabled`, `network.tlsTerminate`, `credentials.*mask*` are user/managed-scope only (our managed template *is* the user settings file, so that is fine); filesystem/network arrays merge across scopes; Linux needs `bubblewrap` and `socat`, and Ubuntu 24.04+ needs an AppArmor profile allowing bwrap user namespaces; subagent Bash is sandboxed when the parent is.

## Required design

1. **Manifest** `home/dot_agents/agent-config.yaml`: add `claude.sandbox` with
   - `enabled: true`, `failIfUnavailable: true` (a Claude session must not silently run unconfined; the installer guarantees prerequisites), `autoAllowBashIfSandboxed: true`, `allowUnsandboxedCommands: true` (the escape hatch stays visible through the normal prompt), `excludedCommands: []` (populate only from E2E evidence, with a comment per entry).
   - `filesystem.allowWrite`: the same agmsg store paths as `codex.sandbox_workspace_write.writable_roots` — render them from that single list, do not duplicate values — plus `~/.claude/projects` (orchestrator memory) and `~/.config/herdr/herdr-agents.log` only if E2E shows a hook/command needs it (justify in a comment).
   - `network.allowedDomains`: GitHub hosts needed by `gh` and https git (`github.com`, `api.github.com`, `uploads.github.com`, `objects.githubusercontent.com`, `codeload.github.com`). Nothing else unless E2E proves a need; record each addition.
   - Comment block (English) stating the symmetry with the Codex sandbox and that `make upgrade`/installers are operator-run outside Claude sessions.
2. **Generator** `scripts/generate-agent-configs.py`: render `sandbox` into `home/.chezmoitemplates/claude-settings-managed.json`; regenerate the template; keep the JSON key order stable.
3. **Validator** `scripts/validate-agent-assets.py`: `validate_claude_settings` requires `sandbox.enabled == true`, `failIfUnavailable == true`, `autoAllowBashIfSandboxed == true`, and `filesystem.allowWrite ⊇ codex.sandbox_workspace_write.writable_roots` (reuse the existing writable-roots helper around L349); `network.allowedDomains` must be non-empty and contain only hostnames (no schemes/paths). Add the corresponding unit tests in `tests/unit/test_validate_agent_assets.py` (positive + one negative per rule).
4. **Installer** `install/ubuntu/common/dependencies.sh`: add `bubblewrap` and `socat`. Add the AppArmor profile step for bwrap exactly as the sandboxing doc describes for Ubuntu 24.04+ (profile file under `/etc/apparmor.d/`, reload), idempotent, shdoc-documented, in the same style as the surrounding installers. macOS needs nothing (seatbelt). Do **not** run it on this host (sudo is denied to agents); the operator applies it via `make update`. Add/extend the bats coverage the repo uses for installers (CI runs it; no local bats).
5. **Doctor**: extend the doctor/health check (find it: `grep -rn "doctor" Makefile scripts | head`) to report `bwrap`, `socat`, the AppArmor profile presence and the `apparmor_restrict_unprivileged_userns` sysctl as WARN/OK lines; unit test in `tests/unit/test_runtime_health.py` following its fixture style.
6. **Docs**: README section "Claude Code sandbox" (what is confined, why nested worktrees under `.claude/worktrees/` stay writable, plan-mode caveat, how to inspect denials); one line in `home/dot_agents/README.md` policy list; `home/dot_config/claude/rules` needs no change unless a rule states something now false — check `model-selection.md`/`agmsg-orchestration.md` and report.
7. **Live E2E** (required; paste verbatim): the settings only take effect after the operator runs `make update`, which you must not run. So do the E2E against a **temporary HOME**: `HOME=<scratch>` with a minimal `~/.claude/settings.json` containing exactly the rendered `sandbox` block, `claude -p` with express-profile args from `~/.agents/model-profiles.env` in a scratch git repo, and show (a) `echo x > /tmp/outside-probe` under that session's sandbox fails while a write inside cwd succeeds, (b) `gh api user -q .login` works (network allowlist), (c) `git -C <scratch> ls-remote https://github.com/mryfmo/dotfiles.git HEAD` works, (d) `ssh -T git@github.com` behaviour (expected: blocked or unsandboxed fallback — record which, this decides whether the push remote should be https for agents), (e) `herdr pane list` (unix socket) — record whether it works sandboxed; if not, propose the minimal `excludedCommands` entry with the reason. If `failIfUnavailable` makes the temp-HOME session refuse to start because socat/AppArmor are missing on this host, record that verbatim as the expected pre-installer behaviour and run the rest with a second temp settings file that sets `failIfUnavailable: false` and `allowUnsandboxedCommands: true`, stating clearly which results came from an unsandboxed fallback.
8. **Commit / PR**: conventional commits (`feat(agents): manage the Claude Code sandbox from the shared manifest`, `feat(install): install bubblewrap/socat and the bwrap AppArmor profile on Ubuntu`, …). Push `feat/claude-sandbox-manifest`, open the PR (English; problem, design, E2E table; end with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`), `gh pr checks --watch`, paste the final table.

## allowed_files

`home/dot_agents/agent-config.yaml`, `scripts/generate-agent-configs.py`, `home/.chezmoitemplates/claude-settings-managed.json` (regenerated only), `scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_runtime_health.py`, `install/ubuntu/common/dependencies.sh` (+ a new `install/ubuntu/common/bwrap_apparmor.sh` and its thin chezmoi wrapper under `home/.chezmoiscripts/` if the repo pattern requires one — name them in the report), the doctor script you identify, the bats file(s) covering installers/doctor, `README.md`, `home/dot_agents/README.md`, and the five artefact files. Anything else → `blocked` with the reason.

## forbidden_actions

`sudo`; installing packages on this host; `make update`; `make upgrade`; `chezmoi apply` against the real HOME; editing `~/.claude/settings.json`; merging the PR; local bats; force-push; ad-hoc `--model` flags.

## effects

`scratch-home-e2e` (reverse: `rm -rf <scratchpad>/claude-sandbox-e2e-*`).

## Artefacts (in `/home/moriya/Workspace/dotfiles`)

report `.orchestration/reports/dot-claude-sandbox-T13-a01.md` (design table, E2E results, open questions such as the ssh push decision, PR URL, `[memory:decision]`: "Claude Code sandbox is rendered from claude.sandbox in agent-config.yaml, symmetric with codex.sandbox_workspace_write; agmsg writable roots come from one manifest list"), validation, sandbox, learning, autoskill (same basename). `contextdb_cli.py memory add` from the main checkout; paste command and output.

## Done signal

`AGMSG-RESULT v1 task_id=dot-claude-sandbox-T13-a01 status=ready_for_review|blocked pr=<n> effects=scratch-home-e2e report=... validation=... sandbox=... learning=... autoskill=...` via `send.sh dotfiles claude-standard-dot-a003 claude-remediation-dot "<message>"`. max_turns=45.
