# Acceptance: dot-update-convergence-T1-a01

status: accepted
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator, adversarial review)
cost: n/a

## Independent re-derivation

- Template matcher: herdr 0.9.1 binary string `^(startup|resume|clear|compact|fork)$` confirmed via `strings`; template now matches; `modify_private_settings.json` replace-in-place path keeps it. Idempotency test asserts second merge == first.
- Makefile: `git ls-files -u` branch placed before the dirty check; plain-dirty message unchanged (existing tests still pass).
- herdr-agents: `cut -f 2 | sort -u` on `team\tname` rows; empty input stays empty so the "No identity" branch is unaffected.
- Reran independently in the worktree: `make unit-test` 394 OK, shellcheck OK, `shfmt -i 4 -sr -d` OK, `git diff --check` OK.
- Worker limitations (no pytest; bare shfmt style differs) are accurate and immaterial.

## Integration

Committed on `fix/update-convergence`, pushed, PR opened; CI + bot review pending before merge.

## Revision 1 (CI)

status: revise — Agent assets `validate` job failed: "generated agent configs are stale: home/.chezmoitemplates/claude-settings-managed.json". The template is generated from `home/dot_agents/agent-config.yaml` (parity policy rule 7: never hand-edit generated files). The matcher must change at the source (the SessionStart entry ~line 176-186 whose hook is herdr-agent-state.sh) and be regenerated; all other checks green.

## Revision 1 result

status: accepted — matcher moved to `home/dot_agents/agent-config.yaml`; regenerated template unchanged; validator "agent asset validation ok" and `make unit-test` 394 OK reproduced by orchestrator. Pushed as second commit on PR #170.

## Revision 2 (PR #170 Codex bot review, commit 147ad3e)

- P1 manifest source: already addressed by commit e3ca2b8.
- P2 Makefile:54 — unmerged check must precede the branch/upstream checks (conflicted rebase has empty branch name). Valid; revise.
- P2 herdr-agents:561 — `home/dot_agents/skills/agmsg-orchestration/SKILL.md:30` still says any multi-line identities.sh output is a leftover registration to clean with leave.sh; contradicts the dedupe. Valid; revise.

## Revision 2 result

status: accepted — unmerged check moved first with a feature-branch unit case; SKILL.md identity rule counts distinct names; unit OK, validator OK. Pushed as 1b822f2 on PR #170.
