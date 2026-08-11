# T40 acceptance

status: accepted
task_id: T40-understand-anything-search-first
reviewed_by: claude-deep-dot (orchestrator)
date: 2026-08-12

## Independent verification

- Branch `feat/understand-anything-search-first`: exactly two commits with the
  specified messages; diff vs main touches only the 11 intended files.
- Search-first guidance present and correctly worded in the Claude rule,
  Codex AGENTS.md section (Japanese), and the regenerated express-explorer
  prompt (freshness check is satisfiable read-only via `.git/HEAD`).
- `.ua` commit contains exactly the five intended files plus `.gitignore`
  (adds `intermediate/`, `tmp/`, `diff-overlay.json`); `config.json` now has
  `"autoUpdate": true`, enabling the plugin's SessionStart/PostToolUse
  freshness hooks.
- Orchestrator re-ran `validate-agent-assets` (ok) and the generator
  (idempotent — no diff) on a clean worktree of the branch; the new
  `knowledge-graph.json` validator token is enforced.

next_action: orchestrator pushes, opens the PR, and merges on green per the
operator's standing approval for this workstream.
