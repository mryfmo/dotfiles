# T13 agmsg orchestration rule file — ACCEPTED

**Verdict: ACCEPT** — commit `c4f80cf` on branch `rule/agmsg-orchestration` (not pushed)

Date: 2026-07-17 (Asia/Tokyo). Reviewer: orchestrator-fable5 (claude-code).

## What was delivered

1. `home/dot_config/claude/rules/agmsg-orchestration.md` (16 lines, 14 rules):
   delegation regime (Claude orchestrates; one resident codex worker executes,
   sequential tasks, adversarial multi-lens acceptance review, crit guard is
   orchestrator-only), delivery/liveness (delivery mode `both` + persistent
   Monitor on watch.sh + actas-claim session lock; completion detected only by
   AGMSG-RESULT arrival; codex `notify`/`agent-turn-complete` as out-of-band
   option), identity/registration convention (unique per physical agent,
   cwd-derived suffix, pre-join collision scan, no `$HOME` registrations,
   explicit nudge delivery, `AGMSG_STORAGE_PATH` separation).
2. `home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl` — wires the rule
   into the official `~/.claude/rules/*.md` load path.
3. Defect fix found during review: `symlink_ponytail.md.tmpl` had a dead
   `home/home/...` target; corrected and verified.

## Official grounding (sources)

- Claude Code hooks (SessionStart `additionalContext`, Stop):
  https://code.claude.com/docs/en/hooks.md
- Rules/memory load paths (`~/.claude/rules/*.md`):
  https://code.claude.com/docs/en/memory.md
- Monitor tool (sanctioned long-running watch):
  https://code.claude.com/docs/en/tools-reference.md
- External-process limits (Channels/MCP only; no direct injection API):
  https://code.claude.com/docs/en/channels.md
- Codex `notify` (`agent-turn-complete`):
  https://developers.openai.com/codex/config-advanced

## Acceptance evidence

- Independent verification: `git show --stat HEAD` = exactly the 3 intended
  files, 18(+)/1(−); message matches the authorized Conventional Commit.
- crit guard: `make require-crit-review` passed with `AGENT_REVIEWED=1
REVIEW_EVIDENCE=.agents/worklog/claude/T13-crit-review-receipt.md`
  (crit-data evidence: `.agents/worklog/claude/T13-crit-review.json`,
  resolved record `r_70bb67`).
- Deployment: `chezmoi apply` created
  `~/.claude/rules/agmsg-orchestration.md` → repo source (verified resolving),
  and repaired `~/.claude/rules/ponytail.md`.
- Live validation this session: delivery `both` + Monitor delivered
  AGMSG-RESULT between turns (23:04:13Z, 23:05:47Z, 23:09:36Z events).

## Residual items (operator decisions)

- Push / PR for branch `rule/agmsg-orchestration`: not done (operator did not
  request push).
- `ai-ops-platform` team still holds `$HOME` registrations
  (`orchestrator-fable5`, `codex-gpt56sol-high`) contrary to the new rule —
  pending operator decision.
