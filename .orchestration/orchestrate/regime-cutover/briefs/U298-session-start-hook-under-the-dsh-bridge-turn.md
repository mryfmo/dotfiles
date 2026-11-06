# U298 the SessionStart hook under a DSH bridge turn: measured absent, claimed present

GOAL
Row `d22` of `tests/dsh-workflow-turn.tsv` (rewritten by U290 from the kit's own sources) expects that a DSH turn through the claude-bridge route runs the kit's SessionStart hook group once: `tests/unit/test_dsh_hook_coverage.py:126-132` states that at dsh-v0.2.1-rc.5 the bridge runs `SessionStart/*` alone (PreToolUse/Bash, PostToolUse/Write|Edit and PermissionRequest/* uncovered, M-15), and `home/dot_local/bin/common/executable_agent-session-staleness:189-203` writes one `<sha256 of session_id>.epoch` file under `~/.local/state/agent-staleness` per session. On the deployed laptop (2026-11-06T15:14Z, after the omp-gateway profile link was deployed) the turn `DSH_HOME=$HOME/.dsh ~/.dsh/bin/dsh --profile thak 'Reply with the single word pong.'` answered `pong` with status 0 and the epoch file count stayed 18 before and after. Either the coverage table's claim is wrong (the bridge runs no kit hook at rc.5, and the table and M-15 should say so), or the hook is configured but does not fire for a bridge session (a kit gap in how the bridge child inherits the Claude settings), or the hook fires and writes elsewhere (then the row's expectation names the wrong directory). This unit measures which, with evidence, and fixes the one that is wrong.

SCOPE
A new branch `fix/session-start-hook-under-bridge` from `origin/main` (your tree is `/tmp/dotfiles-wt/U298`). May write, depending on the finding: `tests/unit/test_dsh_hook_coverage.py` and the coverage table it reads (if the claim is wrong), `home/dot_dsh/plugins/omp-gateway/*` or the bridge configuration the kit deploys (if the bridge should pass the hook settings and does not), `home/dot_local/bin/common/executable_agent-session-staleness` and its tests (if the hook writes elsewhere or refuses silently), `docs/` where the hook coverage is documented, and the body `../U298-pr-body.md`. Not: the thak profile rows, the DSH pin, the Claude settings on this host.

CONTEXT
Read the coverage test and its table whole, the staleness hook (how it finds the session id, where it writes, when it is silent), the bridge plugin's session start path (`home/dot_dsh/plugins/omp-gateway/*.mjs`: what it sends to omp's `auth-gateway stdio`, and whether a Claude Code session with the user's settings is what runs underneath; `docs/pi-claude-bridge.md`), and the omp bridge route's hook behaviour as the pinned omp documents it. Measurement is read-only against the deployed kit except for the one turn you run (which writes DSH's own logs under `~/.dsh` and, if the hook fires, one epoch file): run the d22 command once with `CLAUDE_DEBUG` or the hook's own verbose switch if it has one, list `~/.local/state/agent-staleness` before and after, and read the DSH session log for the turn (`~/.dsh/...`) for any hook or settings line. If the hook needs a settings file the bridge child never reads, show the path it would read (the staleness hook's registration lives in `~/.claude/settings.json`; the bridge child's `CLAUDE_CONFIG_DIR` may point elsewhere: find it).

DATA SHAPE
One finding row in the body: cause (table claim, bridge configuration, or hook location), the evidence (the files and lines read, the measured listing before and after, the log lines), and the fix that follows from it. The coverage table stays the single statement of which kit hooks run under the bridge; whatever the finding, it ends true.

CHANGE
1. Measure per CONTEXT and write the finding row first (`../U298-finding.md`, within 25 minutes), then fix the one wrong thing.
2. Tests for the fix: if the table changes, the coverage test's expectation changes with it and names the measurement; if the bridge changes, a test pins that the hook settings reach the child; if the hook changes, its tests pin the new path or the refusal message.
3. Re-run the d22 command once after the fix is deployable only if the fix is in a file the turn reads from the worktree (else state that the proof is the coordinator's after deploy).
4. The body: Summary (the row, the measurement, the cause), Contract, Threat table, Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_dsh_hook_coverage <the module of the changed file>` OK (paste the count).
2. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `make shellcheck` exit 0 if a shell file changed; `make render-check` exit 0 if a rendered file changed.
3. The finding row pasted with its evidence.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. After the merge and deploy the coordinator re-runs the d22 row.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the coverage test as the statement to make true and the one DSH turn as the measurement; it writes nothing under `~/.claude`, `~/.omp` or `~/.agents`, reads no credential and makes no request beyond the one turn's own route.

TIMEBOX
60 minutes, the first 25 for the finding.

FORBIDDEN
No edit of `~/.claude/settings.json` or any host file; no second DSH turn beyond the one measurement and the one re-run; no `/v1/messages` request of your own; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u298/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U298` and the coordinator fetches it by path.
- Progress line at `../U298-progress.txt` every ten minutes at most; the finding within 25 minutes. Final report to `../U298-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes; Prove It Works: the deployed kit is the artifact).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the finding row in one line, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `tests/dsh-workflow-turn.tsv` row d22; `tests/changes-u290.md`; plan item M-15.
