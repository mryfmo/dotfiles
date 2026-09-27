# Rule candidate: herdr worker relaunch stays inside the pair workspace

Origin: T24 deployment, 2026-09-27. Operator correction: "スペースをわけるのはオーケストレータとワーカーの対としてはおかしい" (splitting workspaces is wrong for an orchestrator-worker pair).

Observed failure: after `/exit`-ing the worker agent to pick up the new worker
profile, the orchestrator ran `herdr-agents <DIR>` (full mode) from inside its
own pane. Full mode created a duplicate workspace (wG) with its own
orchestrator pane instead of healing the current one, because the exited
worker left `<ws>:p2` as an agentless labeled shell pane. `herdr-agents
--attach` also refused ("panes are ambiguous or include unmanaged panes").
Cleanup required `/exit` prompts to the stray agents plus `herdr workspace
close wG`.

Proposed rule:

1. The orchestrator/worker pair always lives in ONE workspace (README fixed
   two-pane layout). Never run `herdr-agents [DIR]` full mode from inside an
   existing pair workspace.
2. To relaunch a worker in place (e.g. after a `worker_profile` change):
   `herdr agent prompt <ws>:p2 "/exit"`, then
   `herdr agent start claude-worker-<ws> --kind claude --pane <ws>:p2 -- ${MODEL_PROFILE_<PROFILE>_CLAUDE_ARGS}`
   with args sourced from `~/.agents/model-profiles.env` (ad-hoc `--model`
   stays prohibited). Verify the argv echoed by the start result.
3. A stray duplicate workspace is torn down by `/exit`-ing its agents via
   `herdr agent prompt`, then `herdr workspace close <id>`.
4. Tooling gap (follow-up task candidate): add a sanctioned worker-relaunch
   mode to `herdr-agents` (e.g. `--restart-worker`) so this sequence lives in
   the managed tool, per the no-improvisation rule.

[memory:failure] herdr-agents full mode run from inside the pair workspace
spawns a duplicate workspace; relaunch workers in place with `herdr agent
start … --pane <ws>:p2 -- ${MODEL_PROFILE_<PROFILE>_CLAUDE_ARGS}` (2026-09-27,
T24 deployment).

## Addendum (2026-09-27, T26 live E2E)
5. `--restart-worker` gap: after the old worker exits, its herdr agent
   registration can linger briefly and `herdr agent start` fails with
   `agent_name_taken`. Add a bounded wait for the registration to clear (or
   reuse/rename it) before starting; until then, a single retry after ~10s
   recovers. (Part B exit-dialog handling itself verified working live.)
