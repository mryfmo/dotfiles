# Acceptance: dot-ua-refresh-T5-a01

status: accepted (blocked outcome, closed without graph changes)
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator)
cost: n/a

## Findings

- `.ua/meta.json` base (13079e4) disagrees with the graph/fingerprints hash (d91b835, #147). The two "re-pin graph baseline" commits (5021c76, fdfa5f0) advanced meta without regenerating the graph; the plugin's guard correctly refuses that base.
- Retry from the graph's own hash d91b835 prepared successfully and selected FULL_UPDATE (743 structurally changed files of 1393, 733 candidates, 10 deletions). Task policy forbids `/understand --full`; worker stopped correctly with `.ua` untouched.
- Decision needed from the operator: authorize a full rebuild (token-heavy; run via a Codex worker or a cheaper profile, never in the interactive deep session), or leave the graph stale and stop re-pinning meta by hand.

## Integration

No repository change. Worktree `.claude/worktrees/ua-refresh` removed.
