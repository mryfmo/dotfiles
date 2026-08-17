# T79 acceptance

- task: T79 (agmsg-orchestration rule two-tiering, PLAN-pi-pivot Phase 6)
- decision: accepted
- date: 2026-08-17
- reviewer: claude-deep-dot (orchestrator)

## Adversarial review

- Mapping table 87/87 subclauses independently walked against the actual
  diffs; refutation attempts on 10 sampled details (a001 rename, trailing
  slash orphaning, commit-message task-ID audit, pane-nudge genericity,
  express-profile env args, delivery `both` escalation, fresh+restore E2E,
  control-plane enumeration, CompactionDB install-on-activation,
  notify event) all found present in the skill — zero loss confirmed.
- "already present" claims (effects 7a/7b, cost 8) verified at
  SKILL.md:77/87/119.
- Message Contract v1 hash unchanged (pre==post).
- Gates re-run orchestrator-side: 336 unit tests OK, validate-agent-assets
  ok, rule file 1,358 chars ≈ 340 est. tok (target ≤350, before 2,204).
- Deployment finding (orchestrator, not a worker violation):
  `~/.claude/rules/*.md` are symlinks into the repo source, so the slim
  rule propagated immediately, while the skill copies under
  `~/.agents/skills` / `~/.claude/skills` are real files pending
  `chezmoi apply` — asymmetry window closed by orchestrator targeted
  apply at acceptance time.

## Effects

effects=none (repo-only edits; deployment performed orchestrator-side).

cost: n/a (worker-reported)
