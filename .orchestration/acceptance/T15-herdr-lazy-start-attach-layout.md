# T15 herdr lazy start + claude-triggered layout — ACCEPTED (merged & deployed)

**Verdict: ACCEPT** — PR #75 squash-merged as `cab6de14`; deployed via chezmoi.

Date: 2026-07-17 (Asia/Tokyo). Reviewer: orchestrator-fable5 (claude-code).
PR: https://github.com/mryfmo/dotfiles/pull/75

## Delivered behavior

1. `herdr` (Ghostty, no args) → `herdr-session` attaches to a single plain
   terminal; no pre-built layout.
2. Starting Claude Code in any herdr pane fires the official Claude
   SessionStart hook → `herdr-agents --attach`: no-op outside herdr (env
   check before any command requirement); inside herdr it renames the pane,
   adds the yazi files pane (0.8 split → 20% far right) and the
   `codex-worker-<workspace>` agent (lands middle → 40/40/20 per T10).
   Idempotent on rerun/resume; per-workspace, so new herdr workspaces get the
   same behavior.
3. Full mode (`prefix+alt+a` / `herdr-agents DIR`) unchanged; its Claude now
   carries `HERDR_AGENTS_LAYOUT=managed` and the attach hook no-ops on that
   sentinel — deterministic guard against the pane-duplication race
   (Codex bot P2 finding, verified PLAUSIBLE, fixed in `2de91223`).

## Review & verification chain

- Orchestrator code review of the full diff (4 files) including the settings
  modifier: baseline `claude-settings-managed.json` has `hooks.SessionStart`
  (list) so the appended hook is not vacuous; merge takes the managed side
  wholesale → exactly one hook per render (double-render diff empty, proven).
- Independent execution verification T15-V1: unittest 32/32 (33 after race
  gate), full suite 149→150 OK, validator exit 0, shellcheck/bash -n clean,
  HERDR-env no-op proof exit 0. Initially reported a FALSE PASS on the
  validator item (wrapper echo masked exit=2); rejected, worker acknowledged
  in a Correction section and re-ran honestly. Lesson: always cross-check
  summaries against raw logs; `; echo exit=$?` hides the real exit status.
- crit guard passed (`AGENT_REVIEWED=1`, receipt
  `.agents/worklog/claude/T15-crit-review-receipt.md`, record `r_6294d6`).
- CI: two full green rounds (initial + race-gate head). One bot finding,
  fixed, replied, thread resolved (GraphQL verified). Squash merge per repo
  convention; branch deleted; local main synced (`cab6de1`).
- Deployment: `chezmoi apply` — `~/.claude/settings.json` now contains the
  attach hook (grep=1) and `~/.local/bin/common/herdr-session` no longer
  references herdr-agents (grep=0).

## Operator verification steps (live UX)

Current herdr session was intentionally left untouched. To see the new
behavior: quit herdr, launch `herdr` in Ghostty → one plain terminal; run
`claude` → 3-pane claude|codex|files layout; `herdr workspace` add → same
lazy behavior per workspace.
