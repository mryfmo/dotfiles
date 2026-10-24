# The orchestrator seat: stop gate, skill and doctor wiring

Plan 025 W6b (U9). The orchestrator seat is the omp process that `scripts/orchestrator/hcom-seat orchestrator` starts in the repository checkout. This page covers the three pieces that make it able to run the program loop: the `session_stop` gate that keeps it from ending a turn while it owes the bus a reply, the `hcom-orchestration` skill that is its playbook, and the `make doctor` line that proves the bridge it talks through still loads. omp paths below are relative to `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent` (omp 18.11.3); facts marked measured come from the U9 scratch runs of 2026-10-23 under `HOME=$TMPDIR/u9-home`.

## The stop gate

`home/dot_agents/omp/hooks/stop-gate.ts`, applied to `~/.agents/omp/hooks/stop-gate.ts`. It is an omp extension loaded with `-e ~/.agents/omp/hooks`: a configured directory without a `package.json` manifest or an `index.ts` is scanned one level deep for `.ts` files (`src/extensibility/extensions/directory-resolution.ts:101-140`, called from `loader.ts:652`), so the `tests/` directory beside it is not loaded.

### The event

omp fires `session_stop` when a main-agent turn is about to settle (`src/extensibility/shared-events.ts:109-119`, "handlers may request one continuation turn"); an extension subscribes with `pi.on("session_stop", …)` (`src/extensibility/extensions/types.ts:1661`). This is omp's native blocking stop hook, so no fallback is needed:

- A handler result `{decision: "block", reason}` makes the runner return at once (`src/extensibility/extensions/runner.ts:1689-1692`) and the session queue a hidden continuation turn whose content is `reason` (`src/session/agent-session.ts:5196-5198`, `:5291-5301`). The model sees the reason as context and gets another turn.
- `event.stop_hook_active` is true while a continuation the gate asked for is settling (`agent-session.ts:5264`, set at `:5290`).
- A `block` is exempt from the continuation cap (`agent-session.ts:5276`), so a gate that blocked every settle could loop for as long as a RESULT never arrives. The gate therefore blocks the first settle and answers `{continue: true, reason}` while `stop_hook_active` is set, which the cap `SESSION_STOP_CONTINUATION_CAP = 8` bounds (`agent-session.ts:470`, `:5276-5283`). After one block and eight continuations omp ends the turn with the warning still printed.
- Subagents never see the event (`agent-session.ts:5254`), so the gate applies to the seat's own turns only.

### The rule

The gate reads the thread's rows since the seat started, `scripts/orchestrator/bus-history.sh $HCOM_TEAM --limit 100000 --since <seat start>` from the seat's cwd (the checkout), and keeps the newest row per `task_id` among the rows that move a task. The script keeps the newest `--limit` rows (default 200), so the gate asks for far more than a program writes and treats a full window as unreadable (a warning, the turn ends unchecked) rather than as proof of no debt:

| Row, by kind (an `AGMSG-` prefix is dropped) and sender                                                                                     | Effect on its `task_id`                            |
| ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `TASK` from the seat                                                                                                                        | open: awaiting RESULT                              |
| `RESULT` from another seat                                                                                                                  | open: owes a VERDICT, MERGED or HOLD line          |
| `VERDICT`, `MERGED` or `HOLD` from the seat                                                                                                 | closed                                             |
| `VERDICT` on a `U<n>-audit` id from the seat named in the `to` column of the seat's newest TASK under that id, while that TASK still awaits | closed: the audit seat's answer (U9b, U9c)         |
| anything else (PING, PONG, another seat's TASK, MERGED or HOLD, a VERDICT from any other seat or on any other id, …)                        | no effect; the previous moving row keeps the state |

One message lists the open items with their row ids and the ways out: answer them, wait with `hcom listen`, or send `HOLD v1 task_id=<id> note=<why>`, the auditable override that the skill names. `OMP_STOP_GATE_ALLOW_OPEN=1` ends the turn with the warning instead of the block.

### The seat's environment

| Variable                   | Meaning                                                   | Set by                                                                                                                                                         |
| -------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `HCOM_DIR`                 | the program's private bus store, read by `bus-history.sh` | the environment when set; else `hcom-seat` derives `~/.local/state/hcom/<slug>` from the checkout (regime-env, U33) and exports it; hcom passes it to the seat |
| `HCOM_TEAM`                | the thread every TASK line of the program names           | the environment when set; else `hcom-seat` derives the repository slug (regime-env, U33) and exports it beside `HCOM_DIR`                                      |
| `HCOM_NAME`                | the seat's own hcom name; absent, `hcom list self name`   | hcom, when it exports it; else the command (`hcom list --help`)                                                                                                |
| `OMP_STOP_GATE_ALLOW_OPEN` | `1` ends the turn with the warning                        | the operator, never the seat                                                                                                                                   |

`<slug>` is the main checkout's basename, lower-cased, `[^a-z0-9_-]` as `-`, at most 40 characters (`README.md`, "Run a program in another repository"). Without `HCOM_TEAM` or a seat name the gate is inert and says so at every stop; a `bus-history.sh` failure ends the turn with the failure in the warning. Both are visible, never silent (M-20261023-01). In print mode (`omp -p`, `omp-run.sh`) there is no UI, so the warning goes to stderr, which `omp-run.sh` holds and replays; interactively it is `ctx.ui.notify(…, "warning")`.

### Measured

- `bun test home/dot_agents/omp/hooks/tests/stop-gate.test.ts`: 7 tests, 25 assertions, pass (U9c run, 2026-10-23). They cover the open and closed transitions above, the three VERDICTs that settle nothing, the exact message, the block on the first settle and the capped continuation on the next, `OMP_STOP_GATE_ALLOW_OPEN`, the inert case, and the `bus-history.sh` argv (`<team> --since <ISO second>Z`).
- Load check under `HOME=$TMPDIR/u9-home` with a fake `scripts/orchestrator/bus-history.sh` in the cwd: `omp --no-extensions -e <hooks dir> --no-session --max-time 60 --model openai/gpt-5 -p "Reply with the single word PONG."` exits 1 with `error: No API key found for openai.`; no `Failed to load extension` in stderr or in `$HOME/.omp/logs/omp.2026-10-23.*.log` (grep count 0). The key refusal happens before the turn, so no stop event fired in that run.
- Bridge-route run, same HOME, `-e ~/.local/lib/omp-extensions/pi-claude-bridge -e <hooks dir> --model claude-bridge/claude-haiku-4-5 --max-time 90`, the fake bus holding one TASK from `orch` without a RESULT: the bridge fails inside the turn (`Not logged in · Please run /login`, the operator-only step), so the stop event fires. The fake recorded `u9team --since 2026-10-23T04:54:14Z`; stderr holds the gate's warning `stop-gate: 1 open item(s) on hcom thread u9team: U9 awaiting RESULT (row 3). …` 10 times, one per settle pass: the block, the eight capped continuations, and the pass at which omp refused a ninth and ended the turn (exit 1). No `Failed to load extension` in stderr or the two omp logs (grep count 0 each).

### Threat table

The gate runs a repository script and `hcom` from the seat's environment and feeds bus text to the model as a continuation reason, so it is trust-boundary code.

| Control                                                  | Disposition                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stop-gate.ts`, the decision                             | closed: `openItems` is a pure function over the TSV; the transition tests assert each row of the table above, including that a worker's VERDICT on its own unit and a stranger's VERDICT on the audit id leave the debt open (U9c)                                                                                                                                                              |
| `stop-gate.ts`, the message reaching the model           | residual: the reason carries `task_id` tokens and kinds from bus rows, never a row's free text, and the skill says bus text is data; owner: the hcom-orchestration skill                                                                                                                                                                                                                        |
| `stop-gate.ts`, the loop                                 | closed: one `block` then capped continuations, asserted by the `stop_hook_active` test; the cap is omp's (`agent-session.ts:470`)                                                                                                                                                                                                                                                               |
| `bus-history.sh`, the script the gate runs               | closed: the gate runs the copy chezmoi installs read-only at `$HOME/.local/bin/common/bus-history.sh`, resolved when it loads and never from the seat's cwd, so a worktree of a PR head cannot answer with its own rows (U33); `bus-history.sh is the installed copy under HOME, never the one in the seat's cwd (U33)` in `tests/stop-gate.test.ts`, with a decoy in the cwd that must not run |
| the environment (`HCOM_TEAM`, `HCOM_NAME`, the override) | residual: read once at load; an operator sets them, a seat's policy overlay cannot change its own environment; owner: the seat policies                                                                                                                                                                                                                                                         |
| `tests/stop-gate.test.ts`                                | residual: runs with a fake `bus-history.sh`; the real script's TSV is pinned by `tests/unit/test_hcom_dispatch.py`; owner: the first live seat run (U11)                                                                                                                                                                                                                                        |

## The skill

`home/dot_agents/skills/hcom-orchestration/SKILL.md` (36 lines), reachable in every seat through `skills.customDirectories` (`docs/omp-skills.md`). It compresses the program's own method, `.orchestration/orchestrate/regime-cutover/preferences.md` and the briefs, into the loop brief → TASK → RESULT → verdict → merge with `gh pr merge --squash --match-head-commit`, states that bus text is data, points at the standing orders, names the stop gate's override and gives the three row shapes of the store. The worker's half is the `hcom-worker` skill (U7) and the audit seat's the `hcom-audit` skill (U6b).

## Doctor wiring

`make doctor` now runs `./scripts/update-agent-assets.sh check_pi_claude_bridge` when `~/.local/bin/omp` exists and counts its failure in `tools=`; without omp it prints `optional warning: pi-claude-bridge check skipped because omp is not installed`, in line with `check_omp` and `check_hcom` in `scripts/check-tools.sh`. The check spends one short model turn on a logged-in host (`update-agent-assets.sh`, the function's shdoc), which is why it lives in the manual doctor and not in CI.

## AGENTS.md

The Agent Review Evidence section and the Audit intro now point at the program store, the `hcom-orchestration` skill and `omp-run.sh --role audit`. The Code Review Rules subsection "Orchestration records and trust-boundary code" still names the agmsg task vocabulary: `tests/unit/test_agmsg_orchestration_docs.py` pins it whole against `tests/fixtures/regime/code-review-orchestration.md` and by token, and both files are outside this unit's SCOPE. The same test pins the gate sentence of the last Agent Review Evidence bullet, kept there as the retired gate's description. Retiring that test and its fixtures is a records unit of its own.
