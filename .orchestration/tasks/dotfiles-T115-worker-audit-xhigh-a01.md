# AGMSG-TASK dotfiles-T115-worker-audit-xhigh-a01

Drafted 2026-10-09 by the orchestrator seat (`claude-deep-dot`, w4:p1). Operator directive 2026-10-09 (chat): the constellation becomes orchestrator `deep` = Fable 5.1 high (unchanged), worker `standard` = Opus 5.5 **xhigh**, auditor `audit` = gpt-6-astra **xhigh**; it supersedes the 2026-10-04 directive (T96) that set both to high. Kind: two manifest values, their rendered outputs, the validator pin, one README paragraph, two test fixtures; no permission, sandbox or hook block; Claude seat allowed. Dispatched to the added worker `claude-standard-dot-a002` (worker-d), in parallel with T114 (worker-c), whose files are disjoint from this task's.

Orchestrator probes before tasking (2026-10-09, both answered `ok`): `codex exec --sandbox read-only -c model='"gpt-6-astra"' -c model_reasoning_effort='"xhigh"' 'Reply with exactly: ok'` under the ChatGPT login (8,419 tokens), and `claude -p --model claude-opus-5-5 --effort xhigh 'Reply with exactly: ok'`.

## Objective

1. `home/dot_agents/agent-config.yaml`: `model_profiles.standard.claude.effort: xhigh` (was high); `model_profiles.audit.codex.model_reasoning_effort: xhigh` (was high). Nothing else in the manifest changes (`standard.codex` stays gpt-6.1-sol high; `security` stays gpt-6-astra high; `deep`, `review`, `express` untouched). Update the `audit` comment line to say xhigh.
2. Regenerate the rendered outputs with `uv run --no-project --with pyyaml scripts/generate-agent-configs.py`; the expected diff is `home/dot_agents/model-profiles.env` (`MODEL_PROFILE_STANDARD_CLAUDE_ARGS` gains `--effort xhigh`) and `home/dot_codex/modify_private_audit.config.toml` (`model_reasoning_effort = "xhigh"` inside `MANAGED`). `home/.chezmoitemplates/claude-settings-managed.json` (`effortLevel` from `interactive_profile: deep`) and `codex-config-managed.toml` (the standard codex baseline) must not change; if they do, stop and report.
3. `scripts/validate-agent-assets.py` lines 743–752: the audit pin becomes `("model_reasoning_effort", "xhigh")` and its comment `# Operator pin (2026-10-09, T115): the auditor is codex gpt-6-astra xhigh, read-only.` The security pin (lines 734–742) stays high.
4. `tests/unit/test_validate_agent_assets.py` line 352: the sample manifest's audit codex `model_reasoning_effort` becomes `"xhigh"`; any other assertion that pins the audit effort or the standard Claude effort follows (grep the tests first and list what you changed). `tests/unit/test_herdr_agents.py` lines 4016/4024 are a self-contained fixture string and are not in scope.
5. `README.md`, the "three-role constellation" paragraph (line 297 onwards): the worker sentence says `standard` profile (Claude `claude-opus-5-5` at xhigh effort, or Codex `gpt-6.1-sol` at high) and the auditor sentence says `gpt-6-astra`, xhigh reasoning effort, read-only sandbox. Add one sentence after the API-key sentence: `Both xhigh settings answered under the ChatGPT login (probe 2026-10-09).` No other README change (T114 edits line 1284 concurrently).

Forbidden: anything else; `make update`; `make upgrade`; touching `~/.local/share/chezmoi`; `herdr-agents` invocations; thread resolution; hand edits to generated files (regenerate them).

[memory:decision] dotfiles-T115 (orchestrator 2026-10-09): the constellation is orchestrator deep = claude-fable-5-1 high, worker standard = claude-opus-5-5 xhigh (codex gpt-6.1-sol high), auditor audit = gpt-6-astra xhigh read-only; both xhigh values answered under the ChatGPT login on 2026-10-09; this supersedes the 2026-10-04 high/high pin (T96).

## Repo / branch

worker-d (`.claude/worktrees/worker-d`, seated by `herdr-agents --add-worker`); `git fetch origin`; `git switch -c chore/worker-audit-xhigh --no-track origin/main`. T114 (PR #304, worker-c) is in flight on `scripts/check-regime-boundary.sh`, `tests/unit/test_herdr_agents.py`, the SKILL, `.gitignore` and README line 1284; do not touch those. When #304 merges before this PR, the orchestrator runs `gh pr update-branch`.

## Allowed files

`home/dot_agents/agent-config.yaml`, `home/dot_agents/model-profiles.env` (generated), `home/dot_codex/modify_private_audit.config.toml` (generated), `scripts/validate-agent-assets.py` (the audit pin and its comment only), `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_generate_agent_configs.py` (only if an assertion pins the changed values), `README.md` (the constellation paragraph only). Artifacts at `.orchestration/{reports,validation,sandboxes,learning}/dotfiles-T115-worker-audit-xhigh-a01.md`, `.orchestration/autoskill/runs/dotfiles-T115-worker-audit-xhigh-a01.md` (not-used record), worker-side review evidence `.orchestration/validation/dotfiles-T115-worker-audit-xhigh-a01-worker-crit.json` and `-worker-review-receipt.md`, all in the main checkout through the permission gate, masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`.

## Push

`~/.config/git/config` rewrites HTTPS pushes to SSH (`url.git@github.com:.pushInsteadOf`) and the SSH agent is empty, so push as T114 did: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles chore/worker-audit-xhigh`; `gh pr create --base main --head chore/worker-audit-xhigh …` works with the keyring login. No config file changes.

## Validation commands (paste verbatim output, whole)

```
uv run --no-project --with pyyaml scripts/generate-agent-configs.py; echo "rc=$?"
git status --short; git diff --stat
make render-check; echo "rc=$?"
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_generate_agent_configs 2>&1 | tail -3
grep -n 'effort' home/dot_agents/model-profiles.env
grep -o 'model_reasoning_effort = \\"[a-z]*\\"' home/dot_codex/modify_private_audit.config.toml
mise x node npm:prettier -- prettier --check README.md 2>&1 | tail -2
gh pr checks <pr>
```

`make unit-test` (the whole suite) is CI's job; run it locally only if time allows and say so either way.

## Completion

PR to `main` (English title `chore(profiles): worker opus-5-5 xhigh, auditor gpt-6-astra xhigh`, English body naming the operator directive and the two probes; attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line (`uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '...'`, main checkout through the permission gate as T114 did), then `AGMSG-RESULT v1 task_id=dotfiles-T115-worker-audit-xhigh-a01` via `agmsg-dispatch dotfiles-conformance claude-standard-dot-a002 claude-deep-dot w4:p1 "<single line>"`. max_turns=10.

## Amendment 1 (orchestrator, 2026-10-09) — the project-map agent body follows the standard profile

The generator's `render_claude_project_map_agent()` borrows `model_profiles.standard.claude`, so the regeneration also rewrites `home/dot_claude/agents/project-map.md` (`effort: high` → `xhigh`). That is the intended consequence of the directive (the project-map subagent runs at the worker tier's effort), not a stray change: `home/dot_claude/agents/project-map.md` (generated) is added to the allowed files, and so is `tests/unit/test_generate_agent_configs.py` if one of its assertions pins that agent's effort (T111 added model/effort assertions there; update only that value). The two must-not-change files stay as stated. Continue from the held tree: regenerate, run the validation commands, push, PR.

## Revise round 1 (orchestrator, 2026-10-09) — Bot 4224982389 is right; one README sentence

The task's sentence was wrong: the Claude probe ran under the Anthropic (Claude Code) login, not the ChatGPT login. Replace `Both xhigh settings answered under the ChatGPT login (probe 2026-10-09).` with `Both xhigh settings answered on 2026-10-09: the Codex audit probe under the ChatGPT login, the Claude worker probe under the Anthropic login.` Nothing else changes. Prettier on README, push over HTTPS as before, CI, Bot wait on the final diff head, `AGMSG-RESULT v1 … round=1` naming the thread as `fixed:<sha>`. The orchestrator corrects the "under the ChatGPT login" wording of the decision memory at consolidation; no new `memory add` is needed from you.
