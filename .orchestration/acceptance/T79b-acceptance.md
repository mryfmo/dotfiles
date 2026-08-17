# T79b acceptance

- task: T79b (kept-core qualifier audit, PR #137 P1 review finding)
- decision: accepted
- date: 2026-08-17
- reviewer: claude-deep-dot (orchestrator)

## Adversarial review

- All 8 claimed repairs re-derived directly from the full diff (small
  enough for exhaustive reading, not sampling): repository-scoped
  activation (the P1), repository-mutating-work object, reporting
  omissions, full sampled-spot-check wording, explicit Crit-gate
  non-delegation, every-`.orchestration`-file duty, upgrade-session
  chore commit, CompactionDB opt-in scope on decision verification.
- 25/25 tightened clauses audited per validation table; core at 1,411
  chars ≈ 353 est. tok (≤360 ceiling), no moved detail regrown, skill
  and codex AGENTS.md untouched.
- Gates re-run orchestrator-side: 336 unit tests OK,
  validate-agent-assets ok.
- Own-review lesson recorded: presence-checking clauses is insufficient;
  kept-core wording must be diffed against pre-edit qualifiers.

## Effects

effects=none. Rule propagates via symlink; no deployment needed.

cost: n/a (worker-reported)
