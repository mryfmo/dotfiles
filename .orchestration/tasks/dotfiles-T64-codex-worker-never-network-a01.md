# AGMSG-TASK dotfiles-T64-codex-worker-never-network-a01

Drafted 2026-10-03 by the orchestrator seat from the approved correction plan (Phase 1, dotfiles-T64). Worker: `claude-standard-dot-a005` in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`. Depends on dotfiles-T63 (merged as c6de5156: the forbidden execpolicy exists before the prompt-free seat).

## Objective

Principle 1 and the operator decision "never + network on": a Codex worker seat launched by `herdr-agents` never prompts; operations outside the sandbox are auto-denied; GitHub reachability moves inside the sandbox instead of through an operator escalation (which no longer exists under `never`). Interactive Codex sessions keep the base config (`approval_policy = "on-request"`, `network_access = false`).

1. `home/dot_local/bin/common/executable_herdr-agents`: in both Codex worker launch paths — `write_spawn_options` (around line 391, the `--add-worker` spawn options; it validates `^--[a-z][a-z0-9-]*$` flag/value pairs, so use the long form) and `start_worker_agent` `worker_args=` (around line 1153) — append `--ask-for-approval never`, and add `-c sandbox_workspace_write.network_access=true` beside the existing `-c sandbox_workspace_write.writable_roots=…` (1154-1155; `write_spawn_options` already emits `--config:` lines at ~406). Update the usage text (line 84 area) and the header comment that describes the worker launch.
2. `tests/unit/test_herdr_agents.py`: update the argv pins that end with `--sandbox workspace-write --profile …` (around lines 1358, 1457, 1473, 1489, 1507, 2099, 2463, 2781, 2824, 4705, 4849, 4985, 5009; grep for the exact strings) and the spawn-options assertions; add one assertion that both `--ask-for-approval: never` and the `network_access=true` config line appear in the spawn options file.
3. `README.md` (Codex worker paragraph around lines 600-625) and `home/dot_agents/skills/agmsg-orchestration/SKILL.md:46` (the sentence saying a GitHub fetch/push is an escalation only the operator answers): the worker seat runs with `--ask-for-approval never` and in-sandbox network; there is no escalation prompt for workers; an action outside the sandbox or forbidden by execpolicy fails and the worker reports `AGMSG-PONG v1 status=blocked`. Note the trade-off: Codex `network_access` is boolean (no domain allowlist like Claude's `allowedDomains`). State that the PermissionRequest hook (permgate) is dead for the worker seat under `never` and live for interactive sessions.

VERIFY (record in the validation file with sources/outputs; use a scratch git repo, never the live seat): (a) `codex -a never --sandbox workspace-write -c sandbox_workspace_write.network_access=true` (express profile args from `~/.agents/model-profiles.env`) runs `git fetch` and `gh pr view` without any prompt; (b) a write outside the writable roots comes back to the model as a failure, not a prompt; (c) a command forbidden by the T63 rules is refused under `never` with the justification text; (d) the PermissionRequest hook does not fire under `never` (observe permgate's decisions log `~/.local/state/permgate/decisions.jsonl` count before/after, or the hook's absence in Codex's own log). Cite the Codex 0.160.0 docs/source lines for `--ask-for-approval never` semantics.

[memory:decision] dotfiles-T64 (operator 2026-10-03): herdr-agents launches Codex worker seats with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`; a worker never prompts, out-of-sandbox and execpolicy-forbidden actions fail and are reported as blocked PONGs; interactive Codex sessions keep on-request and network off.

## Repo / branch

- Work ONLY in the worker-c worktree. `git fetch origin`; `git switch -c chore/codex-worker-never-network origin/main` (c6de5156 or later). Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`
- `README.md` (the Codex worker paragraph), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (line 46 sentence)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T64-codex-worker-never-network-a01.md` (main checkout)

## Forbidden actions

- Changing the base `approval_policy` or `network_access` in `agent-config.yaml`/templates/profiles; touching the audit lane (`--audit`), permgate, or the rules file; editing `~/.codex`; `make update`/`make apply`; `herdr-agents --restart-worker` on the live pair; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -c 'ask-for-approval never' home/dot_local/bin/common/executable_herdr-agents     # expect 2
grep -n 'network_access=true' home/dot_local/bin/common/executable_herdr-agents
uv run python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md
mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents; shellcheck home/dot_local/bin/common/executable_herdr-agents
# VERIFY (a)-(d) transcripts from the scratch repo
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings with a fix commit and repeat; if the Bot enumerates spellings of an already-covered class, propose `not-applicable` in the report instead of another commit; record `bot: none` if nothing arrives. Do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, VERIFY results with sources.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.
