# T44 acceptance

status: accepted (single round)
task_id: T44-marker-extraction-redesign
reviewed_by: claude-deep-dot (orchestrator)
date: 2026-08-12

## Independent verification

- Structure matches the specified design exactly: bracket-only regex +
  `finditer` enumeration, tag-form content sliced to the next marker start,
  explicit spans removed before the heuristic pass, ASCII sentence
  terminators split only before whitespace (with the documented
  over-splitting note).
- Vendor pytest 46/46 (43 existing unchanged + 3 new regression tests).
- Direct functional check with the exact E2E prompt yields precisely two
  explicit project-scoped candidates — (decision, "Use SQLite for all local
  storage. And also") and (constraint, "the E2E2 scratch project must never
  call external networks") — with no heuristic duplicate.
- MANIFEST regenerated; CHANGELOG 2.0.0+dotfiles.2; README documents both
  marker forms and the boundary rule. Worker included its artifacts and crit
  self-review evidence in the same commit (proactive zero-tail).

next_action: orchestrator sweeps this acceptance, pushes, opens the PR,
merges on green, re-syncs ~/.agents/compactiondb, and re-runs the live E2E.
