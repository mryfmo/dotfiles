# U25d agmsg retire targets the registered projects, not the clone it runs in — brief

GOAL
`make update` (run in the canonical chezmoi clone) retires agmsg in every checkout where the agmsg hooks were registered, so the workspace checkout `~/Workspace/dotfiles` loses its SessionStart/SessionEnd/Stop agmsg hooks and its `claude-deep-dot` identity without anyone running the retire by hand there. U25 landed the mechanism (`herdr-agents --retire-agmsg [DIR]`, `make agmsg-retire`), but O1 step 7 showed it acts on `$(CURDIR)` only, which is the chezmoi clone (D-024-145): the clone had nothing to retire and the workspace kept everything.

SCOPE
One branch `fix/agmsg-retire-registered-projects` from `origin/main`. May write: `home/dot_local/bin/common/executable_herdr-agents` (the retire path only), `Makefile` (the `agmsg-retire` target), `tests/unit/test_herdr_agents.py`, `README.md` (the two sentences U25 wrote). Nothing else.

CONTEXT
- Measured (D-024-145, 2026-10-24T03:21Z): after `make update`, `~/.local/share/chezmoi/.claude/settings.local.json` is clean, `~/Workspace/dotfiles/.claude/settings.local.json` still carries the three hooks (sha256 4e2bc4de6f6851ee) and the `inbox.sh` allow rule, and `team.sh dotfiles-conformance` still lists `claude-deep-dot`.
- Where the registrations live: the agmsg team store `~/.agents/skills/agmsg/teams/<team>/` (roster and placement records) names each identity's project path; `identities.sh <project> <type>` resolves identities for a project (`executable_herdr-agents:311-325` uses it with `AGMSG_RESOLVE_PROJECT=0`). The hooks sit in `<project>/.claude/settings.local.json`. Read the agmsg skill's scripts (`~/.agents/skills/agmsg/scripts/identities.sh`, `delivery.sh status`, `team.sh`) to find the listing that yields every registered project path for this host; cite the lines.
- The retire of one project is U25's code: `delivery.sh set off claude-code <project>` then `leave.sh <team> <name>`, idempotent, with the post-check that no `agmsg/scripts/` hook remains.

ACCEPTANCE
1. `herdr-agents --retire-agmsg` without a DIR retires every project the team store registers for this host (each printed with its result) and then the clone it runs in; with a DIR it retires that one project as today. `make agmsg-retire` calls the no-DIR form.
2. A project whose `.claude/settings.local.json` is missing or has no agmsg hook is reported and skipped; an identity whose team no longer exists is reported and skipped; exit 0 when nothing was needed, exit 1 when a hook survives `set off`.
3. Tests: a scratch team store with two registered projects (one with hooks, one without) and fake `delivery.sh`, `leave.sh`, `identities.sh`; the hooked project is retired, the other skipped, the order and argv asserted; the DIR form unchanged.
4. `make unit-test`, `make validate-agent-assets` green; CI green; PR body `Program-Unit: regime-cutover/U25d` (regime-ci accepts `U[0-9]+` only: use `Program-Unit: regime-cutover/U25`, the parent, as the fix rounds did), the footer.

TIMEBOX
90 minutes.

FORBIDDEN
No edit to any live `.claude/settings.local.json` or team store (tests use scratch copies); no edits outside SCOPE; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line per the hcom-worker skill.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (line 20).
