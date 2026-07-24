# T13 agmsg orchestration rule report

## Status

Ready for review.

## Result

- Added `home/dot_config/claude/rules/agmsg-orchestration.md` as the only new rule file.
- Added `home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl` so chezmoi deploys the global Claude rule symlink.
- Corrected `home/dot_claude/rules/symlink_ponytail.md.tmpl` by removing the duplicate `home/` path segment that produced a dead symlink.
- Kept the existing rule style: one `##` heading, terse English bullets, no preamble.
- Covered the orchestrator-only delegation regime, adversarial acceptance, non-idle work, orchestrator-owned Crit guard, delivery monitoring, message-only completion detection, Codex notify signaling, identity uniqueness, repository-scoped registration, session claims, explicit nudges, separated stores, and skill invocation.
- Created `rule/agmsg-orchestration` directly from `main` and left the file untracked and unstaged.

## Scope

No existing rule, dependency, CI configuration, deployed chezmoi target, or pre-existing dirty path was modified.

## Revision

- Added regime-activation checks for `delivery.sh status`, `both` mode, the persistent SessionStart `watch.sh` monitor, and `actas-claim.sh` exclusivity.
- Worker completion is now defined only by AGMSG-RESULT arrival through monitor/turn delivery; pane status and polling sleep loops are explicitly rejected.
- Documented Codex `notify` with the `agent-turn-complete` event as the official optional out-of-band signal.

## Supplemental revision

- Wired the new rule into `~/.claude/rules` through the matching chezmoi symlink template.
- Fixed the reviewed latent Ponytail symlink defect in the only additionally allowed existing file.
