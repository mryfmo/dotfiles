# AGMSG-TASK dot-security-profile-model-T42-a01

## Objective

The `security` Codex profile pins `gpt-daybreak-blue-latest`, which the Codex
CLI rejects under ChatGPT-account login:
`The 'gpt-daybreak-blue-latest' model is not supported when using Codex with a ChatGPT account.`
A security-lane worker seat therefore cannot start (observed 2026-09-29 on
`herdr-agents --add-worker … --kind codex --profile security`). Operator
decision 2026-09-29: the `security` profile uses `gpt-6-astra` with
`model_reasoning_effort: high` (the same model the `audit` profile already
runs under ChatGPT login) until API-key auth is decided separately.

Deliver:

1. `home/dot_agents/agent-config.yaml`: `model_profiles.security.codex.model:
   gpt-6-astra` (keep `high` and the notify hook; keep the Claude half).
   Add a one-line comment that daybreak requires API-key auth.
2. `scripts/validate-agent-assets.py` (~line 743): replace the hard pin
   "must use gpt-daybreak-blue-latest" with a pin on `gpt-6-astra` / `high`
   in the same style as the audit pin below it; message names the operator
   decision date.
3. Regenerate the managed render:
   `uv run --with pyyaml scripts/generate-agent-configs.py` so
   `home/dot_codex/modify_private_security.config.toml` carries
   `model = "gpt-6-astra"`; `--check` passes. Never hand-edit that file.
4. Tests: update `tests/unit/test_generate_agent_configs.py` (~452, 477) and
   `tests/unit/test_validate_agent_assets.py` (~193) to the new model; keep
   the negative case (a wrong security model must fail validation).
5. `make unit-test`, `make validate-agent-assets` green.

[memory:decision] T42: the `security` Codex profile runs `gpt-6-astra` high
under ChatGPT login; `gpt-daybreak-blue-latest` is not usable without API-key
auth, which stays an open operator decision (operator 2026-09-29).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c fix/security-profile-model origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the security codex model line + comment only)
- `scripts/validate-agent-assets.py` (the security pin only)
- `home/dot_codex/modify_private_security.config.toml` (generated only)
- `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-security-profile-model-T42-a01.md` (main checkout)

## Forbidden actions

- Any other profile, model, or effort change; launcher, rule, or skill edits; `~/.codex/**` writes; `make update`/`chezmoi apply`; merging; force push; local bats; writes outside the worktree except the listed paths.

## Validation commands (paste verbatim output)

```
git merge-base --is-ancestor origin/main HEAD && echo base-ok
git diff --stat origin/main
uv run --with pyyaml scripts/generate-agent-configs.py --check
grep -n 'model = ' home/dot_codex/modify_private_security.config.toml
make validate-agent-assets
make unit-test
git grep -n daybreak -- ':!.orchestration' ':!.ua'
gh pr checks <pr-number>
```

## Completion

1. PR to `main` titled `fix(agents): run the security Codex profile on gpt-6-astra under ChatGPT login`, English description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths with verbatim outputs, PR number and head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `send.sh --body-file` for replies. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
