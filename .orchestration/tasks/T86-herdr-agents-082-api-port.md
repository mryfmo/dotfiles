# T86 — Port herdr-agents to the herdr 0.8.2 CLI API

## Objective

`home/dot_local/bin/common/executable_herdr-agents` still calls the pre-0.8 herdr
CLI (`herdr agent start <name> --cwd --workspace --split right --env … --no-focus`).
herdr 0.8.2 removed those flags: `agent start` now requires
`--kind <kind> --pane <existing-pane-id>` and starts the agent in a pane that is
already at its interactive shell prompt. As a result both full mode and
`--attach` fail with `unknown option: --cwd`, and the Codex worker pane cannot be
(re)created through the launcher. Port the script to the current official API,
following the documented herdr agent-automation pattern, and fix two adjacent
defects found during the outage review (agent-name casing, hardcoded Codex
profile default).

Reference for the official pattern (herdr docs, agent-automation):

```bash
split=$(herdr pane split "$pane_id" --direction right --no-focus)
pane=$(printf '%s\n' "$split" | jq -r '.result.pane.pane_id')
herdr agent start <name> --kind codex --pane "$pane" -- <agent args>
```

## Required changes

1. **API port.** Audit every `herdr` invocation in the script against the 0.8.2
   CLI (`herdr <cmd> --help`) and replace all removed/renamed flags. At minimum
   the Codex/Claude agent launch paths must become: create/locate the pane
   (`herdr pane split … --no-focus --cwd …` or reuse the current pane), capture
   the pane id from the JSON response (never predict ids), then
   `herdr agent start <name> --kind <codex|claude> --pane <id> -- <args>`.
2. **Shell-readiness guard.** `agent start` requires the target pane to be at
   its interactive shell prompt. A pane freshly created by `pane split` can
   still be initializing zsh; injecting at that moment leaves bracketed-paste
   garbage in the line editor (observed live: `zsh: bad pattern: [200~codex`,
   then `agent start` times out). Before each `agent start` into a
   newly-created pane, wait for shell readiness (e.g. `herdr pane wait-output`
   for the prompt, and/or `herdr pane process-info` showing the shell as the
   foreground process, with a bounded timeout), and retry `agent start` once on
   timeout. Document the race in a comment.
3. **Agent-name casing.** 0.8.2 enforces `^[a-z][a-z0-9_-]{0,31}$`.
   `codex-worker-${workspace_id}` produced `codex-worker-w1F` and was rejected
   (`invalid_agent_name`, observed live). Lowercase the derived name and
   validate it against the pattern before use.
4. **Codex profile default from the manifest.** The Codex worker profile
   default is currently the hardcoded string `standard`. Per the model-selection
   policy, interactive model choices live only in
   `home/dot_agents/agent-config.yaml`, rendered to
   `~/.agents/model-profiles.env`. Resolve the default as:
   `HERDR_AGENTS_CODEX_PROFILE` env override if set, else
   `MODEL_PROFILE_INTERACTIVE` sourced from `~/.agents/model-profiles.env`,
   else `standard` as the last-resort fallback. Keep the shdoc `@arg`
   documentation in sync.
5. **Tests.** Update `tests/unit/test_herdr_agents.py`: the fake `herdr` CLI
   must emulate the 0.8.2 contract (reject the removed flags, require
   `--kind`/`--pane`, enforce the agent-name pattern), plus add coverage for
   the lowercase-name derivation, the readiness wait/retry path, and the
   profile-default resolution order (env override > model-profiles.env >
   standard). `make unit-test` (`uv run python -m unittest discover -s
tests/unit -v`) must pass.
6. **Comment policy.** All shell comments in English, shdoc-compatible
   (`@file`, `@brief`, `@description`, `@arg`, `@option`, `@example`).

## Live E2E verification (required before RESULT)

Pane-lifecycle changes are accepted only with live end-to-end verification
covering both a fresh workspace and an existing-workspace repair/attach
(same scope as T18):

- Fresh: run the ported script against a scratch directory and verify a
  two-pane workspace (claude + codex) comes up with named agents registered
  (`herdr agent list`).
- Repair/attach: rerun against the same workspace (and exercise `--attach`
  semantics) and verify idempotency — no duplicate panes/agents.
- Launch E2E test-subject agents ONLY with the express profile arguments from
  `~/.agents/model-profiles.env` (`MODEL_PROFILE_EXPRESS_CLAUDE_ARGS`,
  `MODEL_PROFILE_EXPRESS_CODEX_ARGS` /
  `HERDR_AGENTS_CODEX_PROFILE=express`); ad-hoc `--model` flags are forbidden.
- Tear the E2E workspace down afterwards (close panes/workspace; if the E2E
  bootstrap joined agmsg teams, `leave.sh` them) and record the cleanup in the
  validation file.
- Do NOT touch the live `dotfiles` workspace (w1F) or its panes.

## Git workflow

- Branch from up-to-date `origin/main`: `fix/herdr-agents-herdr-082-api`.
- The worktree carries unrelated dirty files (`home/dot_mise/config.toml`,
  `home/dot_mise/mise.lock`). NEVER stage or commit them. Stage by explicit
  pathspec only (the two allowed source files + nothing else); verify with
  `git status` before committing that only intended paths are staged.
- Conventional Commit message and English PR title/description. After pushing,
  watch GitHub Actions (`gh pr checks --watch`); fix failures and re-push until
  green. Do not merge the PR — the orchestrator merges at acceptance.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`
- `.orchestration/reports/T86-herdr-agents-082-api-port.md`
- `.orchestration/validation/T86-herdr-agents-082-api-port.md`
- `.orchestration/sandboxes/T86-herdr-agents-082-api-port.md`
- `.orchestration/learning/T86-herdr-agents-082-api-port.md`
- `.orchestration/autoskill/runs/T86-herdr-agents-082-api-port.md`
- `.agents/worklog/codex/**` (worklog per protocol)

## Forbidden actions

- Committing or staging `home/dot_mise/*` or any path outside allowed files.
- Dependency changes; editing `~/.agents/skills/agmsg/**` or any installed
  skill; editing `.claude/**`, `.codex/**`, `Makefile`, CI workflows.
- Running `bats` locally (CI-only per repo policy). `make unit-test`,
  `shellcheck`, `bash -n` are allowed and expected locally.
- Merging the PR; force-pushing; touching the live w1F workspace panes.

## Validation commands (record output in the validation file)

```bash
bash -n home/dot_local/bin/common/executable_herdr-agents
shellcheck home/dot_local/bin/common/executable_herdr-agents
make unit-test
gh pr checks <pr> # final state
```

## Durable facts to record (CompactionDB opted-in repo)

Run `python3 .claude/hooks/contextdb_cli.py memory add` before completion and
include the exact commands in the report:

- [memory:decision] herdr-agents targets the herdr 0.8.2 agent API: pane split
  (JSON id capture) + shell-readiness wait + `agent start --kind --pane`;
  agent names are lowercased and validated against `^[a-z][a-z0-9_-]{0,31}$`.
- [memory:decision] The Codex worker pane profile default is resolved from
  `MODEL_PROFILE_INTERACTIVE` in `~/.agents/model-profiles.env` (env override
  `HERDR_AGENTS_CODEX_PROFILE` wins; `standard` is the last-resort fallback),
  keeping model selection single-sourced in agent-config.yaml.

## Expected result

`AGMSG-RESULT v1 task_id=T86 status=ready_for_review` with all artifact paths,
a `cost:` line in the report, and the PR number + CI state in the report.

max_turns=40
