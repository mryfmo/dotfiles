# AGMSG-TASK dotfiles-T62-claude-auto-deny-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 1, dotfiles-T62). Runs in parallel with T64/T65; allowed files are disjoint. Worker: the identity named in the dispatch, in its own worktree under `.claude/worktrees/`.

## Objective

Principle 2: "plan approval only" is implemented by user-level settings. `~/.claude/settings.json` is chezmoi-rendered from `home/dot_agents/agent-config.yaml` through `scripts/generate-agent-configs.py render_claude_settings` (397-470) into `home/.chezmoitemplates/claude-settings-managed.json` and merged by `home/dot_claude/modify_private_settings.json`. Operator decisions: `defaultMode: auto`; publish-class commands move from `ask` to `deny`; the `Bash(git push:*)` ask is removed because `main` is protected by the GitHub ruleset and both roles push branches legitimately.

1. `home/dot_agents/agent-config.yaml`: line ~170 `defaultMode: plan` → `auto`; move `gh release:*`, `npm publish:*`, `uv publish:*`, `terraform apply:*`, `kubectl apply:*` from `ask` (~192-198) into `deny` (~181-191), keeping the existing deny entries; delete `Bash(git push:*)` from `ask`. Add a one-line comment above `defaultMode` stating why it is user-level (`auto` is not honoured in project settings) and that the Stop gate (T65) and the deny list are the boundaries.
2. Regenerate `home/.chezmoitemplates/claude-settings-managed.json` (`make render-check` must pass). If `ask` becomes empty, either keep `"ask": []` or render it conditionally like `allow` (line ~420): one line, worker's choice, say which.
3. Tests: `tests/unit/test_generate_agent_configs.py` (fixture ~82 and any `defaultMode`/`ask` assertions), `tests/unit/test_claude_settings_merge.py` only if its real-template test (~399) breaks.

VERIFY (record with sources): (a) `"auto"` is a valid `permissions.defaultMode` in the schema the template declares (`https://json.schemastore.org/claude-code-settings.json`) and in Claude Code 2.1.x docs; (b) `defaultMode: auto` is honoured only from user/managed settings, not project settings (the reason it lives here); (c) whether explicit `ask` rules still prompt under `auto` (either answer leaves this change correct; record it).

[memory:decision] dotfiles-T62 (operator 2026-10-03): Claude's user-level permissions (chezmoi-rendered `~/.claude/settings.json`) use `defaultMode: auto`; publish-class commands (gh release, npm/uv publish, terraform/kubectl apply) are denied rather than asked; the `git push` ask is removed because the GitHub ruleset protects main and branch pushes are legitimate for both roles.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c chore/claude-auto-deny origin/main`. Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the `claude.permissions` block and the one comment only)
- `home/.chezmoitemplates/claude-settings-managed.json` (regenerated)
- `scripts/generate-agent-configs.py` (only the one-line `ask` conditional, if chosen)
- `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_claude_settings_merge.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T62-claude-auto-deny-a01.md` (main checkout)

## Forbidden actions

- hooks or sandbox changes; `.claude/settings.local.json`; `home/dot_local/bin/**`; `scripts/*.sh`; `README.md`; `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge 2>&1 | tail -3
jq '.permissions.defaultMode, .permissions.ask, .permissions.deny' home/.chezmoitemplates/claude-settings-managed.json
make unit-test
make validate-agent-assets
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot review of that head; fix P0/P1 inline findings with a fix commit and repeat; if the Bot enumerates spellings of an already-covered class, propose `not-applicable` in the report; record `bot: none` if nothing arrives. Do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, VERIFY results with sources.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## PONG decision 1 (2026-10-03T22:59Z, status=blocked: auto-mode classifier "Self-Modification")

The Claude worker (a006) was refused both `Edit` calls on `home/dot_agents/agent-config.yaml` by the Claude Code auto-mode classifier (reason: Self-Modification), which treats a Claude agent editing the source of Claude's own permission policy as self-modification and forbids reaching the same outcome through another tool. The worker correctly stopped without a diff. VERIFY (a)(b)(c) are done and recorded in its report (notably: `auto` is the built-in starting mode since Claude Code 2.1.283, and a project-level `auto` would disable the user-level value).

- Decision: a Claude seat cannot carry this task by design; T62 is withdrawn from a006 (released for other work) and will be re-dispatched to a **Codex** worker (`herdr-agents --add-worker <worktree> --kind codex`) after dotfiles-T64 is merged and the operator's `make update` has deployed the launcher that starts Codex workers with `--ask-for-approval never` and in-sandbox network, so the worker can push its PR without an escalation prompt. The task text above stays valid; the worker identity and worktree come from the new dispatch.
- Constraint recorded for the correction plan: tasks that edit Claude's permission policy source (manifest `claude.permissions`, the rendered settings template, the merge script) go to Codex workers or the operator, never to a Claude seat in auto mode.
- Follow-up noted by the worker: `README.md:392-393` cites `Bash(git push:*)` as an ask example; fold the README fix into T69 (docs) rather than widening T62.

## Re-dispatch to a Codex worker (orchestrator, 2026-10-04)

- Worker: the Codex seat re-seated in `.claude/worktrees/worker-e` with `herdr-agents --add-worker .claude/worktrees/worker-e --kind codex` (identity named in the dispatch line). The launcher now starts Codex workers with `--ask-for-approval never` and in-sandbox network (T64, deployed 2026-10-04), so `git push`/`gh pr create` need no prompt; anything the sandbox refuses is a blocked PONG, never an escalation.
- Branch from `origin/main` (f2b5c115 or later). `defaultMode: plan` → `auto`; publish-class `ask` entries → `deny`; `Bash(git push:*)` removed from `ask` (the `main` ruleset is the real guard). Everything else in the task text stands; T88's routing rule is why a Claude seat may not do this.
- After merge the orchestrator runs `make update` in the canonical clone; Claude seats then start in `auto`, and the permission prompts the operator has been answering stop.
