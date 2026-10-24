# U25 agmsg: `make update` stops bootstrapping it and removes the hooks it installed — brief

GOAL
After this unit lands and the operator runs `make update` once, no Claude Code session in the repository checkout receives the agmsg SessionStart, SessionEnd or Stop hooks any more (the "AGMSG terminal … AGMSG monitor mode: invoke the Monitor tool" directive disappears), the coordinator's agmsg identity `claude-deep-dot` has left the team `dotfiles-conformance`, and `make update` never re-registers either. The agmsg tooling, allow rule, writable roots, validators, docs and tests stay for U26 and U27; this unit only turns the live wiring off and makes that the steady state. E1 of plan 025 (W9) begins here; the `openai-codex` route drop stays in U21 behind its own gate.

SCOPE
One branch `feat/agmsg-bootstrap-off` from the current `origin/main`. May write: `Makefile` (the `update` recipe line that calls `agmsg-bootstrap`, and the `agmsg-bootstrap` target), `home/dot_local/bin/common/executable_herdr-agents` (the `--bootstrap-agmsg` entry point and `bootstrap_agmsg`; add the retire path), `tests/unit/test_herdr_agents.py`, `README.md` (the Lifecycle lines that describe the agmsg bootstrap step, and the one sentence in "agmsg" that says `make update` seats the orchestrator identity). Nothing else: no change to `agent-config.yaml`, the settings template, validators, `agmsg-dispatch`, the skills or the rules.

CONTEXT (every fact with its source)
1. What runs today: `Makefile:124` `$(MAKE) agmsg-bootstrap` at the end of `update`; `Makefile:161-166` the target runs `home/dot_local/bin/common/executable_herdr-agents --bootstrap-agmsg "$(CURDIR)"`. `bootstrap_agmsg` (`executable_herdr-agents:1407-1436`) calls `~/.agents/skills/agmsg/scripts/delivery.sh set both claude-code <workdir>` when `<workdir>/.claude/settings.local.json` has no SessionStart hook containing `agmsg/scripts/session-start.sh`, then runs the agmsg doctor. The hooks live in the checkout's `.claude/settings.local.json` (lines 20-48 today: SessionStart `session-start.sh`, SessionEnd `session-end.sh`, Stop `check-inbox.sh`, plus an allow rule for `inbox.sh dotfiles-conformance *` at line 6), never in `~/.claude/settings.json`. The directive text itself comes from the deployed upstream skill (`~/.agents/skills/agmsg/scripts/session-start.sh`), so a dotfiles change alone does not silence it; the hooks must be removed from the live file.
2. The off path already exists in the same skill and is what `herdr-agents --remove-worker` uses (`executable_herdr-agents:1993-2002`): `delivery.sh set off <type> <project>` removes the hooks (`delivery.sh:278`, modes `monitor|turn|both|off`), then `leave.sh <team> <name>` drops the identity. The team today holds exactly one member, `claude-deep-dot` (`team.sh dotfiles-conformance`, 2026-10-24T00:2xZ); the six worker identities were retired at X9 (pilot-facts). The team name and the identity come from the agmsg config under `~/.agents/skills/agmsg/teams/dotfiles-conformance/`; read how `bootstrap_agmsg` or `herdr-agents` resolves them rather than hard-coding `claude-deep-dot`.
3. Decision trail: plan 025 §W9 E1-E3 (agmsg removed after X); pilot-facts X9 "parked: drop agmsg-bootstrap from make update at E1"; the inventory of 2026-10-24 (decisions.tsv D-024-142): 41 test files, `executable_herdr-agents` 214 hits, README sections, so the removal is sliced: U25 (this), U26 tooling, U27 docs and skill files.
4. `make update` runs in the operator's terminal outside Claude sessions; it must stay non-interactive (Makefile comment above `update`). The retire step must be idempotent: a second `make update` finds no hooks and no identity and prints one line saying so.
5. Tests: `tests/unit/test_herdr_agents.py` drives `herdr-agents` with fakes (read how it fakes `delivery.sh`, `leave.sh` and the settings file for `--bootstrap-agmsg` and `--remove-worker`, and reuse that pattern). The bats tests are never run locally (AGENTS.md Test Policy).

ACCEPTANCE
1. `Makefile`: `update` no longer calls `agmsg-bootstrap`; it calls a new target `agmsg-retire` that runs `executable_herdr-agents --retire-agmsg "$(CURDIR)"`; the old `agmsg-bootstrap` target is removed (nothing else in the tree calls it: confirm with grep and paste).
2. `herdr-agents --retire-agmsg <workdir>`: refuses `$HOME` as workdir like the bootstrap did; when the checkout's `.claude/settings.local.json` carries any hook whose command contains `agmsg/scripts/`, runs `delivery.sh set off claude-code <workdir>` and verifies afterwards that no such hook remains (fail with a message naming the file if one does); when the agmsg identity for this checkout is still a team member, runs `leave.sh <team> <name>`; prints one line per action taken and one line `agmsg already retired for <workdir>` when nothing was needed; exit 0 in both cases; missing `delivery.sh` is reported and skipped like the bootstrap does today. The `inbox.sh` allow rule in the local settings is left to `delivery.sh set off` if it removes it, and otherwise reported in the output (do not edit the settings file by hand).
3. Tests in `tests/unit/test_herdr_agents.py`: first run removes hooks and leaves (fake calls asserted in order), second run prints the already-retired line and calls nothing, a hook that survives `set off` fails the command, `$HOME` is refused; the old bootstrap tests are deleted with the function.
4. `README.md`: the Lifecycle sentence that said `make update` bootstraps agmsg now says it retires it and why (E1); the "agmsg" section keeps its history but its first paragraph says the regime is retired and points at hcom.
5. `make unit-test` and `make validate-agent-assets` green (paste the summary lines); CI green.
6. Dry run on this host without touching the live file (STANDING 4): copy the checkout's `.claude/settings.local.json` into a scratch `HOME=$TMPDIR/u25-home` layout with fake `delivery.sh` and `leave.sh`, run the new entry point against it, paste the output of the first and the second run.
7. PR body: `Program-Unit: regime-cutover/U25`, the facts above, the footer (STANDING 14). The operator handout row (two extra columns, STANDING 5): `make -C ~/.local/share/chezmoi update`, expected `agmsg retired` lines on the first run; then a new Claude Code session in `~/Workspace/dotfiles` shows no "AGMSG monitor mode" directive; `team.sh dotfiles-conformance` prints `0 member(s)` or "Team not found"; dry-run column: `operator-only: live settings and team`.

VERIFY
The commands above with pasted output. Network: `api.github.com`, `github.com` only.

TIMEBOX
2 hours.

FORBIDDEN
No edit to the checkout's live `.claude/settings.local.json`, `~/.claude`, `~/.agents/skills/agmsg/db` or `teams` (the old bus history is evidence; U27 archives it); no deletion of `agmsg-dispatch`, the skills, rules, validators or writable roots (U26/U27); no edits outside SCOPE; no merge, rebase, force-push or PR close.

REPORT
Shape per STANDING 12, under 200 words: status, branch, head sha, PR link, CI state, the dry-run outputs, the test summary lines, the handout rows, deviations, follow-ups. Then the RESULT line per the hcom-worker skill, with the `bus-history.sh` row as proof of delivery.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` before any command (its line 20 is this unit's regime: you are the omp worker seat).
