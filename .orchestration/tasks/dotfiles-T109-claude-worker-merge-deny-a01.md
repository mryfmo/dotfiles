# AGMSG-TASK dotfiles-T109-claude-worker-merge-deny-a01

Drafted 2026-10-06 by the orchestrator seat; step 2 of decision A (`.orchestration/validation/github-auth-design-2026-10-05.md` §16) after T108 (#293) deployed. Kind: Claude permission policy for worker seats (the worker worktree's `.claude/settings.local.json`) written by `herdr-agents`, plus tests and docs. This is Claude's own execution boundary, so it is routed to a Codex seat (routing rule); a Claude seat would refuse it as self-modification.

## Objective

1. `home/dot_local/bin/common/executable_herdr-agents`: when a Claude worker is seated (the pair worker in the manifest `worker_worktree`, a `--restart-worker` re-seat, and `--add-worker --kind claude`), after `ensure_worker_delivery` has written the agmsg hooks, merge into `<worktree>/.claude/settings.local.json` a `permissions.deny` list containing exactly `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`. Idempotent with `jq`: keep every other key (`hooks`, existing `permissions.allow`), add the four entries once, never remove other deny entries, never touch the main checkout's or the user-level settings (the orchestrator must merge). One shdoc function, one call site per seat path.
2. `tests/unit/test_herdr_agents.py`: the file gains the four entries on first seat, stays byte-identical on a second seat, keeps unrelated keys, and is not written for a Codex worker (Codex seats are covered by the execpolicy from T108).
3. README (GitHub section, the sentence "Claude worker seats have no such denial yet") and SKILL step 10.5 ("Claude seats get their deny rules in a separate task"): state that `herdr-agents` writes the four deny rules into a Claude worker seat's worktree settings, that deny rules hold over allow rules and nested subcommands in every permission mode (code.claude.com permissions), and that prefix rules do not catch a method flag placed after the path, so the integration gate stays the authority. Docs test tokens follow.

Forbidden: the manifest `claude.permissions` block, the rendered user-level settings template, `modify_private_settings.json`, permgate, Codex execpolicy, the main checkout's `.claude/settings*.json`; `make update`/`apply`; thread resolution; local bats.

[memory:decision] dotfiles-T109 (orchestrator 2026-10-06, decision A step 2): `herdr-agents` gives every Claude worker seat the four merge/auto-merge deny rules in its worktree's `.claude/settings.local.json`; the user-level settings stay untouched so the orchestrator can merge.

## Repo / branch

worker-e; `git fetch origin`; `git switch -c feat/claude-worker-merge-deny --no-track origin/main` (main at c467314e or later); verify task_rev against the main checkout's task file; otherwise PONG blocked.

## Allowed files

`home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`, `README.md` (the one sentence), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (step 10.5 sentence), `tests/unit/test_agmsg_orchestration_docs.py`. Artifacts in your worktree at `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T109-claude-worker-merge-deny-a01.md` plus `.orchestration/validation/dotfiles-T109-claude-worker-merge-deny-a01-worker-crit.json` and `-worker-review-receipt.md`; the orchestrator copies them into the main checkout.

## Validation commands (paste verbatim output, whole)

```
bash -n home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
shellcheck home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
uv run --no-project python -m unittest tests.unit.test_herdr_agents tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English, attribution footer), CI green, Bot wait per the SKILL, artifacts, `cost: n/a`; say in the report that the orchestrator records the decision (Codex seat); `AGMSG-RESULT v1 task_id=dotfiles-T109` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. max_turns=15.

### PONG decision 1 (orchestrator, 2026-10-06 05:56Z) — the worklog write is not required

`.agents/worklog/**` is read-only in your sandbox and is not an expected artifact of this task. Do what T101 and T102 did: keep your plan and todo inside your report (`.orchestration/reports/dotfiles-T109-claude-worker-merge-deny-a01.md`) and record "worklog fallback in the report" in the sandbox record. Not a blocker; proceed with the objective.
