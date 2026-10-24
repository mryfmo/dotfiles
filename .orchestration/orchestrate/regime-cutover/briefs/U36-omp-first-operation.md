# U36 omp-first operation: the orchestrator seat is the entry point and keeps the seats alive — brief

GOAL
The operator starts one omp seat and talks to it; the seat makes the other seats exist, runs the program loop, relaunches a seat that died, and comes back by itself when it dies. No Claude Code session is part of the loop. The permission classifier of the Claude Code session, which refused seat launches and `hcom kill` from that session even with matching allow rules (2026-10-24T06:2xZ: `hcom-seat worker --dry-run` passed, `hcom-seat orchestrator` was refused as "Create Unsafe Agents"), is therefore out of the path.

SCOPE
One branch `feat/omp-first-operation` from `origin/main` (after U31 lands; shares `hcom-seat` and the skills). May write: `home/dot_agents/skills/hcom-orchestration/SKILL.md` (a step 0), `home/dot_agents/omp/policies/orchestrator.yml` and `worker.yml` (`task: deny` under `tools.approval`, with the comment naming the stall), `tests/unit/test_omp_seat_policy.py`, a new `scripts/orchestrator/regime-start` lever, a new supervisor definition (choose the host-native one: a `launchd` agent plist under `home/Library/LaunchAgents/` for macOS and a `systemd --user` unit for Linux, both rendered from one manifest entry, or `pueue` if the repo already manages a pueue daemon; cite what exists), `scripts/update-agent-assets.sh` only if the supervisor needs an install step, `README.md` (a section "Start here: the omp seats" at the top of the regime material), `docs/orchestrator-seat.md`, tests. Nothing else.

CONTEXT
- Measured today: the orchestrator seat ran steps 1 to 7 for seven units with no human in the loop (ledger rows 02:28Z to 05:27Z); it died once (06:03Z) after spawning an omp Task subagent on the claude-bridge route (`No API key for provider: claude-bridge`, then every hcom delivery failed with `Extension sendUserMessage failed`); the two worker seats on the same route were unaffected; the host login was valid. The seats are bound to the herdr session: the 07:13 JST herdr restart ended all three (hcom.db events 126-134, `exit:shutdown`), so a supervisor must survive a herdr restart or re-run after it.
- `hcom-seat` refuses a second seat at an existing name only when the directory is not a worktree of this repository; a relaunch at the same `--name` reuses the worktree (README "hcom-seat"), which is what a worker resume needs.
- `audit.yml` already has `task: deny`; `orchestrator.yml` and `worker.yml` have only `eval: deny` under `tools.approval`.
- hcom gives a launched seat `HCOM_LAUNCHED=1`, `HCOM_TAG`, `HCOM_DIR`; the stop gate needs `HCOM_TEAM` (docs/orchestrator-seat.md, environment table). The supervisor must export both for the orchestrator seat it starts.

ACCEPTANCE
1. hcom-orchestration SKILL gains step 0 (the text of O3 STEP 0: list, launch missing roles by name, never a subagent, relaunch a silent seat after 20 minutes with `note=resume from your branch`) and one sentence in the intro: "The operator types instructions into your pane; a Claude Code session is not part of the loop."
2. `orchestrator.yml` and `worker.yml`: `task: deny`; tests assert the row and that a `task` call is refused in a scratch-HOME omp read-back (pattern of U6).
3. `scripts/orchestrator/regime-start [<program>]`: from a checkout, exports the derived `HCOM_DIR`/`HCOM_TEAM` (U33's derivation when it has landed; until then the two values from the Claude settings env or the arguments), launches the orchestrator seat through `hcom-seat orchestrator`, waits for `listening`, prints the pane name and the sentence "type your instruction in the pane `<tab>`; the store is `<path>`", and exits 0; idempotent (an existing listening orchestrator is reported, not duplicated).
4. The supervisor: starts `regime-start` at login and restarts the orchestrator seat when its process exits, with a backoff and a log under `~/.local/state/hcom/<slug>/supervisor.log`; it never restarts a seat the operator stopped on purpose (`hcom kill` writes a marker the supervisor honours, or the supervisor's own `regime-stop` does); documented enable/disable commands; measured once on this host (paste the log lines of one deliberate kill and the relaunch).
5. README "Start here": `make update`; `regime-start`; what to type; where to read progress (`bus-history.sh <team> --limit 20`, the pane); how to stop (`regime-stop`); that the Claude Code session is optional. PR body `Program-Unit: regime-cutover/U36`, threat table (the supervisor runs a seat with the user's rights at login; the `task` deny; `regime-start` inputs), the footer; audit seat.

TIMEBOX
3 hours.

FORBIDDEN
No change to the deny rows beyond `task`; no Claude settings change; no edits outside SCOPE; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 and 21).
