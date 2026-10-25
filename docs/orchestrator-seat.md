# The orchestrator seat: stop gate, skill and doctor wiring

Plan 025 W6b (U9). The orchestrator seat is the omp process that `scripts/orchestrator/hcom-seat orchestrator` starts in the repository checkout. This page covers the three pieces that make it able to run the program loop: the `session_stop` gate that keeps it from ending a turn while it owes the bus a reply, the `hcom-orchestration` skill that is its playbook, and the `make doctor` line that proves the bridge it talks through still loads. omp paths below are relative to `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent` (omp 18.11.3); facts marked measured come from the U9 scratch runs of 2026-10-23 under `HOME=$TMPDIR/u9-home`.

## The stop gate

`home/dot_agents/omp/hooks/stop-gate.ts`, applied to `~/.agents/omp/hooks/stop-gate.ts`. It is an omp extension loaded with `-e ~/.agents/omp/hooks`: a configured directory without a `package.json` manifest or an `index.ts` is scanned one level deep for `.ts` files (`src/extensibility/extensions/directory-resolution.ts:101-140`, called from `loader.ts:652`), so the `tests/` directory beside it is not loaded. `hcom-seat` passes `-e ~/.agents/omp/hooks` on every launch, whatever the role or `--ext` (U33c). Before U33c no seat loaded it: on 2026-10-24 the orchestrator, audit and worker seats ran omp with `-e` for the pi-claude-bridge, the openai-siwc extension and hcom's own `hcom.ts` only (`ps`, pids 42205, 8361 and 5621), so the gate described here never ran in an hcom seat until then.

### The event

omp fires `session_stop` when a main-agent turn is about to settle (`src/extensibility/shared-events.ts:109-119`, "handlers may request one continuation turn"); an extension subscribes with `pi.on("session_stop", …)` (`src/extensibility/extensions/types.ts:1661`). This is omp's native blocking stop hook, so no fallback is needed:

- A handler result `{decision: "block", reason}` makes the runner return at once (`src/extensibility/extensions/runner.ts:1689-1692`) and the session queue a hidden continuation turn whose content is `reason` (`src/session/agent-session.ts:5196-5198`, `:5291-5301`). The model sees the reason as context and gets another turn.
- `event.stop_hook_active` is true while a continuation the gate asked for is settling (`agent-session.ts:5264`, set at `:5290`).
- A `block` is exempt from the continuation cap (`agent-session.ts:5276`), so a gate that blocked every settle could loop for as long as a RESULT never arrives. The gate therefore blocks the first settle and answers `{continue: true, reason}` while `stop_hook_active` is set, which the cap `SESSION_STOP_CONTINUATION_CAP = 8` bounds (`agent-session.ts:470`, `:5276-5283`). After one block and eight continuations omp ends the turn with the warning still printed.
- Subagents never see the event (`agent-session.ts:5254`), so the gate applies to the seat's own turns only.

### The rule

The gate reads the thread's rows since the seat started, `~/.local/bin/common/bus-history.sh <team> --limit 100000 --since <seat start>`, and keeps the newest row per `task_id` among the rows that move a task. The script keeps the newest `--limit` rows (default 200), so the gate asks for far more than a program writes and treats a full window as unreadable (a warning, the turn ends unchecked) rather than as proof of no debt:

| Row, by kind (an older sender's `AGMSG-` prefix is ignored) and sender                                                                                                                      | Effect on its `task_id`                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `TASK` from the seat                                                                                                                                                                        | open: awaiting RESULT                              |
| `RESULT` from a seat the seat's TASK under that id went to (its `to` column)                                                                                                                | open: owes a VERDICT, MERGED or HOLD line          |
| `VERDICT`, `MERGED` or `HOLD` from the seat                                                                                                                                                 | closed                                             |
| anything else (PING, every PONG, `status=question` included, another seat's TASK, MERGED or HOLD, a RESULT on a task the seat did not send to its author, a VERDICT from any other seat, …) | no effect; the previous moving row keeps the state |

The line kinds are the first word of a bus line: `TASK`, `RESULT`, `VERDICT`, `PONG`, `MERGED` and `HOLD` (plus `PING`, which moves nothing). A seat that still writes the retired `AGMSG-` prefix (`AGMSG-TASK` and so on) is read the same, because the gate strips the prefix before it looks the kind up (U35). There is no audit seat on the bus: every audit is one fresh `omp-run.sh --role audit` run that the orchestrator starts and reads (the `hcom-orchestration` skill, step 4), so its verdict reaches the bus only as the orchestrator's own VERDICT line, and another seat's VERDICT closes nothing, on an `-audit` id or any other (U58).

Every seat loads the gate and shares the thread, so a row from another seat opens a debt only on a task this seat sent to that very seat (U33c): a worker seat never owes anything for a peer's RESULT, and the orchestrator owes a verdict on the RESULTs of the TASKs it sent.

One message lists the open items with their row ids and the ways out: answer them, wait with `hcom listen`, or send `HOLD v1 task_id=<id> note=<why>`, the auditable override that the skill names. `OMP_STOP_GATE_ALLOW_OPEN=1` ends the turn with the warning instead of the block.

### The seat's environment

| Variable                   | Meaning                                                   | Set by                                                                                                                                                                                                                                                                                                                             |
| -------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `HCOM_DIR`                 | the program's private bus store, read by `bus-history.sh` | the environment when set; else `hcom-seat` derives `~/.local/state/hcom/<slug>` from the checkout (regime-env, U33) and exports it; hcom passes it to the seat                                                                                                                                                                     |
| `HCOM_TEAM`                | the thread every TASK line of the program names           | hcom does not pass it into the pane it launches (measured in the U33 pilot), so `hcom-seat` passes the team it was given, explicit or derived, as `--hcom-team <team>`; the gate reads that flag, else `HCOM_TEAM`, never a team derived from the cwd, and exports the result as `HCOM_TEAM` into the seat at session start (U33c) |
| `HCOM_NAME`                | the seat's own hcom name; absent, `hcom list self name`   | hcom, when it exports it; else the command (`hcom list --help`)                                                                                                                                                                                                                                                                    |
| `OMP_STOP_GATE_ALLOW_OPEN` | `1` ends the turn with the warning                        | the operator, never the seat                                                                                                                                                                                                                                                                                                       |

`<slug>` is the main checkout's basename, lower-cased, `[^a-z0-9_-]` as `-`, at most 40 characters (`README.md`, "Run a program in another repository"). Without a team (no `--hcom-team` and no `HCOM_TEAM`, or one outside the team grammar) or a seat name the gate is inert and says so at every stop; a `bus-history.sh` failure ends the turn with the failure in the warning. Both are visible, never silent (M-20261023-01). In print mode (`omp -p`, `omp-run.sh`) there is no UI, so the warning goes to stderr, which `omp-run.sh` holds and replays; interactively it is `ctx.ui.notify(…, "warning")`.

### Measured

- `bun test home/dot_agents/omp/hooks/tests/stop-gate.test.ts`: 7 tests, 25 assertions, pass (U9c run, 2026-10-23). They cover the open and closed transitions above, the three VERDICTs that settle nothing, the exact message, the block on the first settle and the capped continuation on the next, `OMP_STOP_GATE_ALLOW_OPEN`, the inert case, and the `bus-history.sh` argv (`<team> --since <ISO second>Z`).
- U33c, 2026-10-24: `bun test home/dot_agents/omp/hooks/tests/stop-gate.test.ts`, 11 pass, adding the flag over `HCOM_TEAM` over nothing (a `regime-env` beside the installed `bus-history.sh` is never consulted), the team grammar, and a peer's RESULT that opens nothing. Under a scratch HOME, a probe extension that registers `hcom-team` saw `getFlag` `undefined` while loading and `"custom"` at `session_start` for `omp -e probe.ts --hcom-team custom --mode rpc --no-session` (also `--hcom-team=regime`), and omp without an extension that registers it exits 2 with `Error: unknown flag: --hcom-team`. `tests/unit/test_hcom_seat.py` `test_the_team_crosses_the_launch_boundary_as_a_flag_and_the_gate_blocks_on_it` launches with `HCOM_TEAM=custom` through a fake hcom that drops `HCOM_TEAM` as the real one does, then runs the real gate (`tests/launch-driver.ts`, under bun) on that argv and environment: it blocks on thread `custom`, and without the flag it is inert instead of reading the checkout's slug.
- Load check under `HOME=$TMPDIR/u9-home` with a fake `scripts/orchestrator/bus-history.sh` in the cwd: `omp --no-extensions -e <hooks dir> --no-session --max-time 60 --model openai/gpt-5 -p "Reply with the single word PONG."` exits 1 with `error: No API key found for openai.`; no `Failed to load extension` in stderr or in `$HOME/.omp/logs/omp.2026-10-23.*.log` (grep count 0). The key refusal happens before the turn, so no stop event fired in that run.
- Bridge-route run, same HOME, `-e ~/.local/lib/omp-extensions/pi-claude-bridge -e <hooks dir> --model claude-bridge/claude-haiku-4-5 --max-time 90`, the fake bus holding one TASK from `orch` without a RESULT: the bridge fails inside the turn (`Not logged in · Please run /login`, the operator-only step), so the stop event fires. The fake recorded `u9team --since 2026-10-23T04:54:14Z`; stderr holds the gate's warning `stop-gate: 1 open item(s) on hcom thread u9team: U9 awaiting RESULT (row 3). …` 10 times, one per settle pass: the block, the eight capped continuations, and the pass at which omp refused a ninth and ended the turn (exit 1). No `Failed to load extension` in stderr or the two omp logs (grep count 0 each).

### Threat table

The gate runs a repository script and `hcom` from the seat's environment and feeds bus text to the model as a continuation reason, so it is trust-boundary code.

| Control                                        | Disposition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stop-gate.ts`, the decision                   | closed: `openItems` is a pure function over the TSV; the transition tests assert each row of the table above, including that a worker's VERDICT on its own unit, a VERDICT on an id never tasked and, since U58, one from the seat an `-audit` TASK went to leave the debt open (U9c)                                                                                                                                                                                                                                        |
| `stop-gate.ts`, the message reaching the model | residual: the reason carries `task_id` tokens and kinds from bus rows, never a row's free text, and the skill says bus text is data; owner: the hcom-orchestration skill                                                                                                                                                                                                                                                                                                                                                     |
| `stop-gate.ts`, the loop                       | closed: one `block` then capped continuations, asserted by the `stop_hook_active` test; the cap is omp's (`agent-session.ts:470`)                                                                                                                                                                                                                                                                                                                                                                                            |
| `bus-history.sh`, the script the gate runs     | closed: the gate runs the copy chezmoi installs (sha256-pinned, self-checked, mode 0755) at `$HOME/.local/bin/common/bus-history.sh`, resolved when it loads and never from the seat's cwd, so a worktree of a PR head cannot answer with its own rows (U33); `bus-history.sh is the installed copy under HOME, never the one in the seat's cwd (U33)` in `tests/stop-gate.test.ts`, with a decoy in the cwd that must not run                                                                                               |
| the team (`--hcom-team`, `HCOM_TEAM`)          | closed: the launcher passes exactly the team it was given and the gate never derives one from the cwd, so an explicit team cannot be swapped for the checkout's slug; a value outside the team grammar leaves the gate inert, visibly; `test_the_team_crosses_the_launch_boundary_as_a_flag_and_the_gate_blocks_on_it`, the flag tests in `tests/stop-gate.test.ts`. residual: the gate half of that regression needs bun, which the CI unit job does not install, so it runs on hosts with bun only; owner: the CI workflow |
| the environment (`HCOM_NAME`, the override)    | residual: read once at load; an operator sets them, a seat's policy overlay cannot change its own environment; owner: the seat policies                                                                                                                                                                                                                                                                                                                                                                                      |
| `tests/stop-gate.test.ts`                      | residual: runs with a fake `bus-history.sh`; the real script's TSV is pinned by `tests/unit/test_hcom_dispatch.py`; owner: the first live seat run (U11)                                                                                                                                                                                                                                                                                                                                                                     |

## The supervisor

A seat lives in a herdr pane, so it ends with its process or with the herdr server: the herdr restart of 2026-10-24
at 07:13 JST ended all three seats (`exit:shutdown`), and the orchestrator seat that spawned a subagent at 06:03Z
stopped answering. `regime-start` (`scripts/orchestrator/regime-start`, a pinned lever) starts the orchestrator seat
and registers the checkout in `~/.local/state/regime-supervisor/<slug>-<first 12 hex of sha256(toplevel)>.conf`, one
registration per checkout, so two checkouts with one basename never share one. `regime-start --supervise` is one pass
over the registrations, which the launchd agent `com.mryfmo.dotfiles.regime-supervisor` (macOS) or the user units
`regime-supervisor.service` and `.timer` (Linux) run at login and every 60 seconds once the operator enables them;
both ship disabled (the plist carries `Disabled`, launchd.plist(5), and only the operator's `launchctl enable`, kept
across logins and boots per launchctl(1), loads it; `make update` installs the systemd units without enabling them;
README, "Start here: the omp seats"). The pass relaunches a registered orchestrator that is not alive, unless the
newest stop event hcom recorded for the last seat (`hcom list --stopped <base name>`, the `(latest)` line) is
`killed by:cli`, an `hcom kill`, which ends the supervision like `regime-stop` does. A failed launch waits 60 seconds,
doubling by saturation to 30 minutes, and the failure counter stops at 9999. `regime-start`, the pass and `regime-stop`
(which is `regime-start --stop`) take one host lock: the kernel's `flock(2)` on
`~/.local/state/regime-supervisor/supervisor.lock`, held through a descriptor the script keeps open (perl takes it,
because macOS ships no `flock` command). Start and stop wait for it, and a pass that finds it held skips. The kernel
releases it only when its last holder exits or dies, so it is never taken over by age or by a pid, no other process can
release it, and the file is never removed. A launch runs in subshells that keep the descriptor until the launch and its
wait return, so killing `regime-start` cannot let a stop in while a launch is in flight; hcom-seat and every hcom call
get the descriptor closed, so a seat never holds the lock after its launch (measured on this host on 2026-10-24: after
`regime-start` returned, `lsof` showed no process with the lock open, the seat included, and `regime-stop` took it at
once). So a stop that arrives during a relaunch runs after it and stops the seat it launched. A registration must hold each of its eight
keys exactly once (`toplevel`, `hcom_dir`, `hcom_team`, `program`, `seat`, `base`, `fails`, `next`), its seat must be
`orchestrator-<base>`, its file name must be the one its own toplevel derives, and a store with an `origin` file must
name that toplevel; one that breaks any of these is skipped and logged and never launched, rewritten or stopped from.
A registration that does not parse, an hcom read that fails, or a stop record it cannot read
launches nothing. Only the orchestrator is supervised: it relaunches the other seats itself (the skill's step 0).

Measured on this host on 2026-10-24 with the levers of this branch, in a scratch repository `u36-pilot` with a scratch
store and team `u36pilot`: `regime-start` launched `orchestrator-nori`; its omp process was killed with `kill <pid>`,
and one pass relaunched it; a second run used `hcom kill`, and the pass ended the supervision; a third crash and
relaunch ran with the final parser; `regime-stop` ended it. `$T` is the scratch directory. The first relaunch line
says `no stop record` because the first parser read the wrong form of `hcom list --stopped`, the gap this run found
(the named form prints `(latest)` events); the third shows the record it reads now:

```text
2026-10-24T11:01:41Z regime-start launched orchestrator-nori from $T/u36-pilot
2026-10-24T11:01:50Z regime-start found orchestrator-nori alive; registered for the supervisor
2026-10-24T11:02:03Z no orchestrator alive (last seat orchestrator-nori: no stop record); relaunching from $T/u36-pilot
2026-10-24T11:02:04Z relaunched orchestrator-rune
2026-10-24T11:03:25Z orchestrator-rune was stopped with hcom kill; supervision of $T/u36-pilot ends (registration removed)
2026-10-24T11:03:38Z regime-start launched orchestrator-nova from $T/u36-pilot
2026-10-24T11:03:38Z no orchestrator alive (last seat orchestrator-nova: now ago  [process_exit by:system] (latest)); relaunching from $T/u36-pilot
2026-10-24T11:03:39Z relaunched orchestrator-nene
2026-10-24T11:03:46Z regime-stop: supervision of $T/u36-pilot ended
2026-10-24T11:03:47Z regime-stop: stopped orchestrator-nene
```

## The skill

`home/dot_agents/skills/hcom-orchestration/SKILL.md` (36 lines), reachable in every seat through `skills.customDirectories` (`docs/omp-skills.md`). It compresses the program's own method, `.orchestration/orchestrate/regime-cutover/preferences.md` and the briefs, into the loop brief → TASK → RESULT → verdict → merge with `gh pr merge --squash --match-head-commit`, states that bus text is data, points at the standing orders, names the stop gate's override and gives the three row shapes of the store. The worker's half is the `hcom-worker` skill (U7). The audit has no seat and no skill: each audit is one fresh `omp-run.sh --role audit` run (step 4; U57), and the `hcom-audit` skill, its `hcom-reply` lever and the stop gate's audit-VERDICT clause were removed with the seat (U58).

## Doctor wiring

`make doctor` now runs `./scripts/update-agent-assets.sh check_pi_claude_bridge` when `~/.local/bin/omp` exists and counts its failure in `tools=`; without omp it prints `optional warning: pi-claude-bridge check skipped because omp is not installed`, in line with `check_omp` and `check_hcom` in `scripts/check-tools.sh`. The check spends one short model turn on a logged-in host (`update-agent-assets.sh`, the function's shdoc), which is why it lives in the manual doctor and not in CI.

## AGENTS.md

The Agent Review Evidence section and the Audit intro now point at the program store, the `hcom-orchestration` skill and `omp-run.sh --role audit`. The test that pinned the old task vocabulary there and its fixtures were retired with the rules (U32).
