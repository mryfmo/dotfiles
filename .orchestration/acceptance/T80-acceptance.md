# T80 acceptance

- task: T80 (codex AGENTS.md two-tiering, PLAN-pi-pivot Phase 6)
- decision: accepted
- date: 2026-08-17
- reviewer: claude-deep-dot (orchestrator)

## Adversarial review

- 143-clause mapping walked against the actual diff; the entire worklog
  lifecycle (paths, naming, headings, frontmatter schema, index format,
  done-rename, owner rules) spot-verified present in the skill's new
  "Codex worker worklogs" section — zero substance loss.
- Refutation attempt on the key risk — "a plain non-agmsg Codex session
  loses the worklog schema" — rejected: the always-on file keeps the
  binding duties (keep plan/todo current, never commit, one active todo
  per owner) plus an explicit read pointer to the skill section, and the
  same file's Understand-Anything section documents that skills live in
  `~/.agents/skills`, so discovery is closed.
- 3 duplicate-of rows verified as true duplicates with canonical copies.
- Gates re-run orchestrator-side: 336 unit tests OK,
  validate-agent-assets ok.
- Effect: 2,773.51 -> 1,852.90 est. tok (-33.19%) on every Codex session.

## Effects

effects=none. Orchestrator performed targeted skill deployment at
acceptance (same asymmetry-window closure as T79).

cost: n/a (worker-reported)
