# Architecture: dotfiles at 8c3cfec2 (U434, feat/router-profile-acp-subagent, PR 757)

## Product and principals

- **The repository** is a dotfiles kit with the regime-cutover seat levers: `hcom-seat` launches each agent seat (orchestrator, worker, dsh, router) inside srt 0.0.81 with settings it renders; `acp-broker` runs outside every seat, started by the router launch, and starts omp workers, each in a sibling srt sandbox, for the Router.
- **The operator** runs `hcom-seat` from a terminal, outside every seat. hcom-seat and the broker run unsandboxed as the operator.
- **The Router** (the dsh superagent of the router row) runs inside srt and reads GitHub-authored input; it is the lowest-trust principal on this change. It writes its own seat directory and state slot, is denied the broker directory `<state slot>/broker` for write, and reaches the broker only through the socket there.
- **Workers** are `omp acp` processes under settings the broker renders: their task slot (a clone the broker made), the shared Claude Code directory, their omp profile and `~/.omp/run`; `allowUnixSockets` empty.
- **Protected resources**: the checkout and its git state, the seats root, other seats' slots, the operator's Claude Code state, the credential stores, the private tool directory `~/.local/state/hcom-seat`, the manifest pins.

## The change under review (5b99f2c3..8c3cfec2, 13 paths, +317 -24)

- **The Router's subagent route** (home/dot_dsh/profiles/router/cordis.patch.yml:31-35, :49-60, rendered by scripts/generate-agent-configs.py:2538-2542, :2549-2564): `tool-subagent` on the `acp` provider with `maxDepth: provider-managed`, and the `subagent-acp` insert whose command is `~/.local/bin/common/acp-seat` with args `--socket $ACP_BROKER_SOCK --name router`, `permission: allow`, `env: {}`.
- **The client's defaults** (scripts/orchestrator/acp-seat:143-164): `--repo` defaults to the process cwd, `--ref` to `HEAD`; `--socket` and `--name` required; the same header checks before anything is sent (:265-276).
- **The socket's name** (scripts/orchestrator/hcom-seat:3287-3292): the router row adds `ACP_BROKER_SOCK=<state slot>/broker/sock` to dsh's `env -i` list; the dsh row adds none.
- The acp-seat and hcom-seat pins (agent-config.yaml:912, :942) and digests (generated-agent-outputs.json:436, :478), one README line (:151), four test modules. acp-broker, acp-relay.py and seat-settings-render.sh are unchanged.

## Trust boundaries the hunt reads

- **Router to broker**: the header and the ACP stream are all that cross; the broker judges the header (acp-broker:1306-1330) and reads the repository only inside the Router's own sandbox (:1810-1828).
- **Router to worker**: the worker's grants are the broker's; `permission: allow` answers the worker's requests on a stream the Router already controlled.
- **Depth**: a worker cannot reach the broker (its `allowUnixSockets` is empty), so the route does not recurse.
- **Environment**: one path, no credential, on the router row alone.
- **Pin-then-run and rendering**: the two changed levers equal their pins and their copies; the committed router patch reads as the renderer's output.

## Entry surfaces and paths

- The Router's subagent tool call (a model action steered by GitHub input), which spawns acp-seat in the request's cwd.
- The Router's connection to the broker socket (the ACP-SEAT header, then the stream), carried from earlier runs' broker units.
- The router profile deployed to `~/.dsh/profiles/router`, and the levers beside the manifest.

## Prior coverage

- Base: run-75 (a65bc8ed; its code units are 5b99f2c3's). 228 units at this head: 112 covered, 22 candidate, 94 out_of_scope. Changed-source units: 73; each unit citing a line U434 changed has a parent re-check at this head, and run-75's nine U344b units were re-read.
- run-74's three records sync 56 units are restored: this head's .orchestration equals 7375902b's.
- No same-source confirmed record exists to exclude: run-75's findings.json is empty and its 22 leads are unvalidated candidates.
- The full code architecture of the levers is in run-73's to run-75's `architecture.md`; this file names what U434 adds.

## Companion selection

- `AI-AND-LLM.md`: a model-driven subagent tool that spawns workers through a privileged broker (sub-agent trust, tool permissions).
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: the local IPC between the Router, acp-seat and the broker.
- `SUPPLY-CHAIN-AND-RELEASE.md`: the pinned levers, their copies and the generated profile.
- Not selected: no browser, cloud, tenant, native code, wire protocol to a shared service or HTTP flow is in the change.
