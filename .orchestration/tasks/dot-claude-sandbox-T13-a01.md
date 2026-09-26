---
task_id: dot-claude-sandbox-T13-a01
revision: 2
---
# AGMSG-TASK dot-claude-sandbox-T13-a01 (revision 2): Claude worker autonomy = sandbox (PR #179) + a manifest-rendered worker permission profile, symmetric with the Codex `approval_policy`/`sandbox_mode`

## Revision 2 — why (verified 2026-09-26 03:3xZ)
Claude workers are launched by `herdr-agents` with profile args only (`--model … --effort …`); the applied `~/.claude/settings.json` has `permissions.defaultMode: plan` and no `sandbox`. Every worker therefore starts in plan mode and every edit/Bash waits for a human at the pane — the reason resident Claude workers stall (worker-c: edits made, never committed, no RESULT for 4 h). Codex workers have the symmetric controls rendered from the manifest (`approval_policy = "on-request"`, `sandbox_mode = "workspace-write"`, agmsg `writable_roots`); Claude has none. PR #179 (revision 1, head b729f54, 16 commits behind main) delivers the sandbox half only.

Documented facts (https://code.claude.com/docs/en/permission-modes, /permissions, /settings, /sandboxing, /hooks-guide; Claude Code 2.1.282 installed, `--settings` needs ≥ 2.1.248):
- `--permission-mode` values: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. `dontAsk` never prompts: actions matched by `permissions.allow` run, everything else is denied without a prompt. `bypassPermissions` is refused as root and is out of policy here (model strength never justifies wider permissions).
- Precedence: managed > CLI (`--settings <file>`, flags) > `.claude/settings.local.json` > `.claude/settings.json` > user. Project/local files cannot set `auto`/`bypassPermissions`; CLI can set any mode.
- `sandbox.autoAllowBashIfSandboxed` (default true) auto-runs sandboxed Bash regardless of mode; `excludedCommands` bypass the sandbox but still go through permission rules; Go CLIs (`gh`) and ssh `git push` need `excludedCommands` or `enableWeakerNetworkIsolation`, plus `allowRead` for `~/.ssh` if ssh is used.
- Rule syntax: `Bash(git commit *)`, `Bash(gh pr *)`, `Edit(//abs/path/**)`; deny rules always win; a PreToolUse hook `allow` exits plan mode (not used here — deterministic rules only).

## Revision 2 deliverables (in addition to revision 1 items 1–8, which stay as implemented in #179)
9. **Worker permission profile in the manifest**: `claude.worker` in `home/dot_agents/agent-config.yaml`: `permission_mode: dontAsk`; `allow` rules covering exactly the worker playbook actions (git add/commit/switch/rebase/push within its worktree, `git push --force-with-lease`, `gh pr create|view|diff|checks|comment|api` read/write on PRs, `uv run`, `python3`, `make <test/validate targets>`, `shellcheck`, `shfmt`, `~/.agents/skills/agmsg/scripts/*.sh`, `Edit(//<worktree>/**)` via `additionalDirectories`/cwd); `deny` rules for the forbidden actions in the agmsg-orchestration rules (`make upgrade`, `make update`, `chezmoi apply`, `gh pr merge`, `gh auth *`, `git push --force` without lease, `sudo`, `codex login`, `rm -rf` outside the worktree). Comment block states the symmetry with `codex.approval_policy`/`sandbox_workspace_write` and that the orchestrator session keeps `plan`.
10. **Rendering**: `scripts/generate-agent-configs.py` renders `home/dot_claude/worker.settings.json` (chezmoi → `~/.claude/worker.settings.json`) containing `permissions.{defaultMode,allow,deny}` and the `sandbox` block from item 1; keep the managed orchestrator settings unchanged.
11. **Launch**: `herdr-agents` passes `-- --settings ~/.claude/worker.settings.json --permission-mode dontAsk <profile args>` for every claude worker (full mode, `--attach` repair, and the future `--add-worker`); README herdr-agents section documents it; unit tests in `tests/unit/test_herdr_agents.py` assert the argv.
12. **Validator**: `validate-agent-assets.py` requires `claude.worker.permission_mode ∈ {dontAsk, acceptEdits}`, forbids `bypassPermissions`/`auto`, requires every forbidden action in `home/dot_config/claude/rules/agmsg-orchestration.md` to have a deny rule (parse the rule file's forbidden list or keep one source list in the manifest that renders both), and requires `sandbox.enabled` (item 3). Tests.
13. **E2E (scratch HOME, verbatim)**: with the rendered worker settings and a scratch worktree: (a) `claude -p --permission-mode dontAsk --settings <file> "run: git status"` completes without a prompt; (b) a denied action (`make upgrade`) is refused without a prompt and the refusal text is captured; (c) sandboxed Bash runs when bwrap+socat are present, or `failIfUnavailable` aborts with the documented message when not (record which happened on this host; `socat` is absent here and the AppArmor step is installer-owned).
14. **Rebase** `feat/claude-sandbox-manifest` onto origin/main (≥ 5e40ff9) before starting; resolve conflicts with T17's `check-tools.sh` changes; run the full unit suite.

Repo/identity/worktree: assigned at dispatch (lane freed after T19 or T16). Overlaps T19 on `agent-config.yaml`, `validate-agent-assets.py`, `check-tools.sh`, `executable_herdr-agents`: dispatch only after PR #184 is merged.

## Revision history
- r1 (09-25 07:47Z): sandbox manifest (PR #179).
- r2 (09-26 03:3xZ): worker permission profile + launch flags + validator + E2E; rebase.

---
# Revision 1 text (kept for reference; items 1–8 remain binding)

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
