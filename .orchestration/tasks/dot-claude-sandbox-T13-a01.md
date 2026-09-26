---
task_id: dot-claude-sandbox-T13-a01
revision: 3
---
# AGMSG-TASK dot-claude-sandbox-T13-a01 (revision 3): unattended Claude workers through THIS environment's permission architecture — sandbox (PR #179) + `--permission-prompts none` + role-aware permgate policy, symmetric with Codex `workspace-write`/`approval_policy`

Revision 3 replaces revision 2 entirely (revision 2 designed a Claude-only `dontAsk` settings file and ignored permgate; discarded).

## Facts — official Claude Code docs (quoted by URL in the acceptance record)
- `--permission-mode` on the CLI overrides `permissions.defaultMode` from every settings file (permission-modes.md). Plan mode never exits without a human unless a `PermissionRequest` hook allows `ExitPlanMode` (hooks-guide.md).
- `--permission-prompts none` (headless.md): "Anything that would prompt is denied unless a `PermissionRequest` hook allows it, Claude is told that nobody can approve the request and not to retry it, and the run continues"; `AskUserQuestion` is removed.
- `PermissionRequest` hook output: `hookSpecificOutput.decision.behavior: allow|deny`, `reason`, `updatedInput`, `updatedPermissions` (hooks.md).
- `sandbox.autoAllowBashIfSandboxed` (default true) runs sandboxed Bash without a prompt in any mode; `excludedCommands` bypass the sandbox but still go through permission rules; `ask` rules always prompt (sandboxing.md, permissions.md).
- `--settings <file>` sits directly under managed settings in precedence (settings.md). Not needed by this design.

## Facts — this environment (file:line in `.orchestration/acceptance/dot-claude-sandbox-T13-a01.md`, "environment map")
- permgate (`home/dot_local/bin/common/executable_permgate`) is the single `PermissionRequest` decision point for Claude and Codex: deny_patterns → cli layer → allow_patterns (bounded commands only: no shell control/expansion characters) → LLM classifier in shadow. Silence = native prompt. Policy `home/dot_agents/permgate-policy.yaml` (schema_version 2). Live host: 113 decisions, all `fallthrough ask`; deterministic allow set = 9 read-only patterns, deny = `rm -rf /`. No role distinction; no role env reaches panes.
- Managed Claude settings: `defaultMode: plan`, deny + ask lists, no `allow`, no `sandbox`. Codex: `approval_policy = "on-request"`, `sandbox_mode = "workspace-write"`, `network_access = false`, agmsg `writable_roots`. herdr-agents launches Claude workers with profile args only; Codex workers with `--sandbox workspace-write --profile <p>`.
- Result: Claude workers inherit plan mode and every write/Bash waits for a human; Codex workers prompted too (268/370 historical fallthroughs were `apply_patch`) and were approved by the operator. Neither kind is unattended today.

## Design (documented mechanisms only; manifest is the single source; validator enforces)
1. **Sandbox** — revision 1 items 1–8 as implemented in PR #179 (rebase onto origin/main ≥ fed6d80; resolve `check-tools.sh` conflicts with T17). Sandboxed Bash runs prompt-free for every Claude session; the residue (excluded `gh`, `git push` over ssh, `ask` rules) reaches permgate.
2. **Worker launch (herdr-agents, rendered from `claude.worker` in `agent-config.yaml`)**: every Claude worker pane gets `--permission-mode acceptEdits --permission-prompts none` before the profile args, and env `HERDR_AGENTS_ROLE=worker` (the same variable T21 keys its guardrails on); the orchestrator pane gets `HERDR_AGENTS_ROLE=orchestrator` and keeps `plan` + human prompts. `acceptEdits` is the Claude analogue of Codex `workspace-write` (edits inside the worktree need no decision); `none` makes every remaining prompt a permgate decision with deny as the fail-closed default. No `--settings` file, no `dontAsk`, no `bypassPermissions`/`auto` for workers.
3. **Codex worker symmetry**: Codex workers launch with `--ask-for-approval never` (documented `approval_policy` value) in addition to `--sandbox workspace-write --profile`; sandbox denials return to the model as failures, no human prompt. Rendered from `codex.worker` in the manifest; the interactive Codex profiles keep `on-request`.
4. **permgate role-aware policy (schema_version 3)**: `roles.worker.allow_patterns` — deterministic, bounded patterns for the worker playbook: `git add|commit|switch|rebase|status|diff|log|fetch`, `git push origin <branch>`, `git push --force-with-lease=<ref>:<sha> origin <branch>`, `gh pr create|view|diff|checks|comment|edit`, `gh api repos/*/pulls/*`, `gh api repos/*/issues/*/comments`, `uv run …`, `python3 …`, `make test|validate|…` (enumerate from the Makefile), `shellcheck`, `shfmt`, `~/.agents/skills/agmsg/scripts/*.sh`. `roles.worker.deny_patterns` — every forbidden action from `home/dot_config/claude/rules/agmsg-orchestration.md` and the task contracts: `make upgrade|update`, `chezmoi apply`, `gh pr merge`, `gh auth *`, `codex login`, `git push --force` without `--force-with-lease`, `sudo`, `rm -rf` outside the worktree. `roles.orchestrator` = today's policy unchanged. Role comes from `HERDR_AGENTS_ROLE` in the hook's environment; missing role → today's behaviour. Classifier stays shadow for both providers (validator rule unchanged). Because workers will chain commands, the report must measure how many worker commands the bounded-command rule would reject on the recorded decisions log and propose the documented mitigation (single commands per call in the worker playbook, not a looser matcher).
5. **Validator**: `claude.worker`/`codex.worker` present and rendered into the herdr-agents argv; worker mode ∈ {acceptEdits, default}; `--permission-prompts none` present; `HERDR_AGENTS_ROLE` set for both panes; permgate policy schema 3 with `roles.worker` deny ⊇ the forbidden-action list (one source list in the manifest renders both the rule text and the deny patterns); `sandbox.enabled` (item 1); both providers still `llm_enabled: false`.
6. **Tests**: `test_herdr_agents.py` argv/env for claude and codex workers; `test_permgate.py` role resolution, worker allow/deny goldens, missing-role fallback, shadow unchanged; generator/validator tests; `lifecycle.bats` greps (CI only).
7. **E2E (scratch HOME, verbatim)**: (a) `claude -p --permission-mode acceptEdits --permission-prompts none` with `HERDR_AGENTS_ROLE=worker` and the rendered policy: an allowed `git status` runs, a denied `make upgrade` is refused with permgate's reason and no prompt, an unmatched chained command is denied (fail-closed) and the run continues; (b) sandbox present/absent outcome per revision 1 item 7; (c) Codex: `codex exec --ask-for-approval never --sandbox workspace-write` in the scratch repo runs an in-workspace edit and fails a network call without prompting (skip with the exact error if Codex is not logged in — operator item).
8. **Docs**: README "Unattended workers" section (Claude flags, Codex flags, permgate roles, what still prompts for the orchestrator, how to read `~/.local/state/permgate/decisions.jsonl`); `home/dot_agents/README.md` policy line; `agmsg-orchestration.md` rule: workers issue one command per Bash call.
9. **Security review**: permgate policy changes require the `security`-profile Codex audit before merge (model-selection.md); Codex is not logged in on this host — the PR waits for that audit or an explicit operator waiver recorded in the acceptance file.

Repo/identity/worktree: assigned at dispatch after PR #184 merges (overlaps T19 on `agent-config.yaml`, validator, `check-tools.sh`, herdr-agents). Branch `feat/claude-sandbox-manifest` (existing PR #179) rebased; new commits on top.

## allowed_files
Revision 1 list plus: `home/dot_local/bin/common/executable_permgate`, `home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_herdr-agents`, `home/.chezmoitemplates/codex-config-managed.toml` (only if `codex.worker` needs rendering there), `home/dot_config/claude/rules/agmsg-orchestration.md` (+ Codex mirror), `tests/unit/test_permgate.py`, `tests/unit/test_herdr_agents.py`, `tests/unit/test_generate_agent_configs.py`, `tests/install/common/lifecycle.bats`.

## forbidden_actions
Revision 1 list; additionally: enabling `llm_enabled` for any provider; adding `bypassPermissions`/`auto`/`dontAsk` anywhere; loosening the bounded-command rule; editing `~/.local/state/permgate/*`.

## Revision history
- r1 (09-25 07:47Z): sandbox manifest (PR #179).
- r2 (09-26 03:3xZ): Claude-only `dontAsk` settings file — discarded (ignored permgate).
- r3 (09-26 04:0xZ): environment-integrated design: sandbox + `--permission-prompts none` + role-aware permgate + Codex `never`; grounded in official docs and the environment map.

---
# Revision 1 text (items 1–8 remain binding)

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
