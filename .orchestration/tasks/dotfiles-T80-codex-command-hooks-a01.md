# AGMSG-TASK dotfiles-T80-codex-command-hooks-a01

Drafted 2026-10-05 by the orchestrator seat from the approved correction plan (Phase 5, dotfiles-T80). Depends on T71 (merged 65915b93). Shares `scripts/generate-agent-configs.py` with T90 (in flight on the Codex security seat), so dispatch only after T90 merges or when the orchestrator confirms T90's generator change has landed.

## Objective

Principle 7 (CompactionDB captures Codex lifecycle too) needs the generator to render generic Codex command hooks, so that T82 can declare PreCompact/PostCompact/SessionEnd hooks in the manifest without touching the renderer again.

1. **Manifest shape (no manifest change in this task):** `codex.hooks.command_hooks` is a list of `{event, command, timeout, status_message}` mappings. `codex.hooks.permission_request` keeps its current shape and rendering; `codex.hooks.state` is untouched.
2. **Generator** (`scripts/generate-agent-configs.py`, the Codex renderer around the `[[hooks.PermissionRequest]]` block): render each `command_hooks` entry as

   ```toml
   [[hooks.<Event>]]
   matcher = "*"

   [[hooks.<Event>.hooks]]
   type = "command"
   command = "<command>"
   timeout = <timeout>
   statusMessage = "<status_message>"
   ```

   in manifest order, after the PermissionRequest block and before `[hooks.state]`. Entries for the same event each get their own `[[hooks.<Event>]]` table (Codex merges arrays). Reuse `quote_toml`/`quote_toml_key`; no new helper unless the PermissionRequest block is refactored to share the same emitter (preferred: one small function used by both).
3. **Validator** (`scripts/validate-agent-assets.py`, `validate_codex_config` or the Codex hooks check next to it): `event` must be one of the Codex hook events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PermissionRequest`, `Stop`, `SubagentStop`, `PreCompact`, `PostCompact`, `SessionEnd`, `Notification`); `command` non-empty string; `timeout` positive int; `status_message` string. VERIFY the event list against the official Codex hooks reference (paste the source URL and the list in the validation file); drop any name the reference does not have. The rendered template must contain exactly the tables the manifest declares (count check), so a stray hand edit fails validation.
4. **Tests:** `tests/unit/test_generate_agent_configs.py` renders a fixture with PreCompact, PostCompact and SessionEnd entries and asserts the exact TOML; a fixture with an empty/missing `command_hooks` renders no extra table; `tests/unit/test_validate_agent_assets.py` rejects an unknown event, a missing command and a non-integer timeout, and accepts the three-hook fixture.
5. `make render-check` stays clean (the manifest declares no `command_hooks` yet, so the rendered templates are byte-identical).

Forbidden: `home/dot_agents/agent-config.yaml`; `home/.chezmoitemplates/codex-config-managed.toml` (must not change); Claude-side rendering; `permission_request` behaviour; permgate.

[memory:decision] dotfiles-T80 (operator 2026-10-03): the Codex renderer emits generic `[[hooks.<Event>]]` command hooks from `codex.hooks.command_hooks` in the manifest, validated against the official Codex hook event list, so lifecycle hooks (PreCompact/PostCompact/SessionEnd for CompactionDB) are declared in the manifest, never hand-written into the rendered TOML.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/codex-command-hooks --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T80-codex-command-hooks-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
make validate-agent-assets
uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets 2>&1 | tail -3
make unit-test 2>&1 | tail -3
git ls-files -z "*.py" | xargs -0 mise x ruff -- ruff format --config ruff.toml --check
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, the VERIFY source.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T80` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=30.
