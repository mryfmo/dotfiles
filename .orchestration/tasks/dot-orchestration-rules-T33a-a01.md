# AGMSG-TASK dot-orchestration-rules-T33a-a01

## Objective

Codify five rule-text items that need no operator decision (T33 items 2, 4, 5
plus two lessons from T31/T32). Text only; no tooling changes.

1. **Worker inbox discipline (interim, from `.orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md`).**
   Add to the "Identity, delivery, and storage" section of the SKILL and as a
   bullet in the Claude rule: a worker acting under a worktree-registered
   identity from a main-path pane receives no turn delivery for that identity;
   it runs `~/.agents/skills/agmsg/scripts/inbox.sh <team> <identity>` at each
   milestone (task start, push, CI green, before RESULT, after any PONG), and
   the orchestrator treats revision and PING dispatches as picked up at the
   worker's next inbox check, not as turn notices. Name the root fix (worker
   pane launched inside its own worktree) as the condition that retires this
   rule.
2. **Fail-closed task convention (T33-2).** Worker commands complete inside the
   sandbox and allowlist. An action outside that boundary is not escalated
   for approval: the worker fails it, reports `AGMSG-PONG v1 status=blocked`
   with the exact command and boundary, and the orchestrator re-tasks.
   Agent-to-agent permission approval is forbidden (restate the trust
   boundary).
3. **Batch acceptance (T33-4).** When several RESULTs are pending at once, the
   auditor may pre-screen each changeset (`codex --profile audit review
   --commit <sha>`, visible lane when available) before the orchestrator's
   sequential adversarial review; acceptance authority never moves, and each
   RESULT still gets its own acceptance record.
4. **Crit "no web UI" principle (T33-5).** Make the Codex-side crit guidance
   identical to the Claude rule `home/dot_config/claude/rules/crit-review.md`:
   agent-side crit-data evidence, never a browser review to ask the user;
   `crit share`/publish only on explicit user request; a crit session opened
   by the Plan Mode hook is closed once the review is done (no resident local
   web server). Locate the Codex mirror yourself (`grep -rn -i "crit" home/dot_agents home/dot_codex`);
   if no Codex-side crit text exists, add the clause to the agmsg-orchestration
   SKILL "Review and integration invariants" and say so in the report.
5. **No pane probes.** Extend the existing "never read worker panes or
   screens" bullet (SKILL "Regime activation and progress") with "including
   read-only probes such as `pane read`/`pane wait-output` against another
   agent's pane, even to learn output shapes; use `--help` and fake CLIs".

[memory:decision] T33a: interim worker inbox discipline (inbox.sh at each
milestone for worktree-registered identities from a main-path pane),
fail-closed task convention with PONG blocked instead of approval requests,
auditor pre-screening for batched RESULTs with orchestrator-only acceptance,
Codex crit guidance aligned to the Claude no-web-UI rule, and an explicit ban
on read-only pane probes are codified in the agmsg-orchestration rule and
SKILL (operator 2026-09-28).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c docs/orchestration-rules-T33a origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `home/dot_config/claude/rules/agmsg-orchestration.md`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `home/dot_config/claude/rules/crit-review.md` (only if wording must be shared verbatim)
- the Codex-side crit mirror file you locate under `home/dot_agents/` or `home/dot_codex/` (name it in the report)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-orchestration-rules-T33a-a01.md` (main checkout)

## Forbidden actions

- Any change outside rule/skill text: no scripts, tests, manifests, hooks,
  permissions, `reviews/ADH_Integrated_Plan/`.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs and
   the PR number/head SHA. In the report, quote each added/changed sentence.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
