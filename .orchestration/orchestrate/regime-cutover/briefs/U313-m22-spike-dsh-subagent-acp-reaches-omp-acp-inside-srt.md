# U313 M-22 spike: dsh-subagent-acp started by the dsh role of hcom-seat reaches `omp acp` inside srt

GOAL
The critical path's row 3 (handoff/08-purpose-and-goal.md §3) asks for one measurement: a DSH control host, started by `hcom-seat dsh` under srt, delegates one task through `dsh-subagent-acp` to a throwaway shim that runs the seat canary and then `srt --settings <worker> -- omp acp`, and the shim's launch.log shows the canary line followed by the omp acp start line. The PRD row of M-22 (`.private/harness-kit/PRD.md:278`) names three decisions rows: the canary held before omp started; the child's omp version and the route its session log names, with a DSH profile that holds no Anthropic or OpenAI key; a write outside the worker's roots refused. Records only: no tracked file changes. The spike replaces the plan's hand-written `srt -- dsh` control host with the deployed dsh role (PR 697), the kit's only lever that names srt for DSH. Part A below is measurable now; Part B waits on U310 (the dsh profile's bridge route) and runs when the coordinator says so.

SCOPE
Scratch only: `SPIKE=$(mktemp -d "${TMPDIR:-/tmp}/dsh-spike-acp.XXXXXX")`, `HOME=$SPIKE/home`, `DSH_HOME=$SPIKE/dsh-home`, a scratch seats root `$SPIKE/seats`, the shim `$SPIKE/bin/acp-shim-spike`, the profile `$DSH_HOME/profiles/thak-acp`, outputs under `/tmp/m22/`. Reads: the repository at `/tmp/dotfiles-wt/U313` (a read-only worktree at origin/main 2b2415f6, created by the coordinator; never commit there), the installed lever `~/.local/bin/common/hcom-seat`, the installed DSH under `~/.dsh` (read and link, never write). May write: nothing in the repository or the store; the proposed decisions rows go to `/tmp/dotfiles-wt/U313-rows.tsv` (one row per line in the store's six-column form `ts  phase  decision  why  evidence  result`, phase `M-22`) and the report to `/tmp/dotfiles-wt/U313-report.txt`; the coordinator writes the store. Not: hcom-seat, the thak profile, the manifest, the plugin, anything under the real `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local/state/omp-seats`, `~/Workspace`.

CONTEXT
The dsh role (installed lever `~/.local/bin/common/hcom-seat:85-127`): per-launch slot, write roots DSH_HOME, `~/.omp/profiles/dsh`, `~/.omp/run` (:1494); read grants cwd, slot, DSH_HOME, profile, `~/.agents/skills`, tools dir (:1795); command `<DSH_HOME>/bin/dsh --profile <name>` (:2051-2054); environment `env -i HOME PATH DSH_HOME OMP_PROFILE=dsh [USER LANG TERM]` (:2268-2274). The shim's canary string is four words, `write-denied read-denied ssh-denied debug-denied` (:2182-2198), and the shim writes no log on success: launch.log is this spike's file. dsh-subagent-acp at the pin `dsh-v0.2.1-rc.5` (`packages/subagent/subagent-acp/README.md`): `command`, `args`, `permission`, `env` over a credential-scrubbed parent environment; `initialize` then `newSession` before the run publishes; stderr inherited. The base bundle mounts `subagent` with `spawn` and `fork` and `tool-subagent` with `provider: spawn`; the spike patch adds the `acp` provider and repoints `tool-subagent`. `omp acp`: ACP JSON-RPC over newline-delimited stdio, stdout protocol only, diagnostics on stderr, logs under `~/.omp/logs/`, `--profile <name>` isolates sessions under `~/.omp/profiles/<name>/agent/sessions/`. Data dependency: U310 gives the dsh profile its bridge route; until it is deployed a DSH turn under the role ends in `HTTP 404: No available model matches "claude-bridge/claude-opus-5-5"`, so Part B waits and Part A does not. The test table row for this spike is `tests/sandbox-write-denies.tsv` s21 (the coordinator fills it from your report).

DATA SHAPE
launch.log at `$DSH_HOME/spike/worker/launch.log` (under a role write root), one line per event, `<utc> acp-shim-spike: <event>`; events in order: `canary <four words>`, `omp acp start omp <version> profile dsh cwd <path>`, `omp acp exit <status>`. Worker settings at `$DSH_HOME/spike/worker/srt-settings.json`, a copy of a worker seat's settings with allowWrite = the spawn cwd and `$HOME/.omp/profiles/dsh`, denyRead and denyWrite as the dsh role's, no `allowNestedUserNamespaces`. The profile patch `$DSH_HOME/profiles/thak-acp/cordis.patch.yml` = the rendered thak patch plus an inserted row `{id: subagent-acp, name: '@deepseek-ai/dsh-subagent-acp', config: {providerName: acp, command: $SPIKE/bin/acp-shim-spike, args: [], permission: allow, env: {OMP_PROFILE: dsh}}}` and `tool-subagent` repointed to `{provider: acp, toolName: subagent}`. Proposed decisions rows: phase `M-22`, each naming the launch.log line verbatim and public paths only (write `~/...`, never the absolute home).

CHANGE
Part A, measurable now (no route, no login):
1. Build the scratch root; link the installed dsh tree as U272 did; render thak-acp from the thak patch plus the two rows above; `DSH_HOME=$DSH_HOME $DSH_HOME/bin/dsh --profile thak-acp --dump-config > /tmp/m22/dump.txt`; expect the `subagent-acp` row resolved and `tool-subagent` with `provider: acp`. If the package does not resolve, install it in the scratch profile the way the thak plugins are linked (manifest `home/dot_agents/agent-config.yaml:1382`) and record that.
2. Write the shim from the installed shim text (:2163-2232): it writes the worker settings from its `$PWD`, runs the probe, appends the canary line, runs `srt --settings <worker> -- omp --version > version.txt` inside, appends the start line, then execs `srt --settings <worker> -- /usr/bin/env PATH=<seat path> omp acp --profile dsh --approval-mode yolo`. Refuses, exit 2, on any probe word other than the four.
3. Nested srt: `srt --settings $SPIKE/outer.json -- srt --settings $SPIKE/inner.json -- /bin/sh -c 'echo nested-ok' > /tmp/m22/nested.txt`; expect `nested-ok`. If it fails, stop and record: the shim cannot nest and M-24's design changes.
4. Shim alone, outside DSH: `printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":1,"clientCapabilities":{}}}' > /tmp/m22/init.json; cd $SPIKE/dsh-home/spike/cwd; HOME=$SPIKE/home $SPIKE/bin/acp-shim-spike < /tmp/m22/init.json > /tmp/m22/acp-out.txt 2> /tmp/m22/acp-err.txt`; expect launch.log lines 1 and 2 in order, and one JSON-RPC line on stdout with `"id":1` and a `result` carrying `protocolVersion`. No model is needed for `initialize`.
5. Dry run of the control host: `cd /tmp/dotfiles-wt/U313; HOME=$SPIKE/home HCOM_DIR=$SPIKE/hcom HCOM_TEAM=regime ~/.local/bin/common/hcom-seat dsh --home $DSH_HOME --seats-root $SPIKE/seats --profile thak-acp --dry-run > /tmp/m22/dry.txt 2> /tmp/m22/dry-err.txt`; expect the launch line with `OMP_PROFILE=dsh` and `--profile thak-acp`, exit 0. If the lever refuses a scratch HOME or cwd, paste the refusal and stop Part A there.
Part B, only when the coordinator sends the word (after U310 is deployed and the login exists):
6. The real turn under the role from `~/Workspace/dotfiles` asking for one subagent use; launch.log shows canary, start, exit in order; the reply is the word.
7. The newest session file under the dsh profile names `claude-bridge`; the scratch profile's credentials file holds no `ANTHROPIC` or `OPENAI`; version.txt read.
8. A second turn asking the child to write outside its roots; expect the file absent and a refusal line.
9. Write the three proposed decisions rows to `/tmp/dotfiles-wt/U313-rows.tsv`; delete `$SPIKE` except `$SPIKE/bin/acp-shim-spike` for M-24.

ACCEPTANCE
1. `/tmp/m22/nested.txt` holds `nested-ok` (pasted).
2. launch.log from step 4 pasted: line 1 the canary with the four words, line 2 `omp acp start omp <version>`, in that order; `acp-out.txt` holds one JSON-RPC result for id 1.
3. `dump.txt` lines for `subagent-acp` and `tool-subagent` pasted; `dry.txt` pasted.
4. Part B when unblocked: the reply, launch.log, the session file grep, the credentials grep, the refused write; else Part B named as waiting on U310 with the exact blocking line if you tried.
5. `git -C /tmp/dotfiles-wt/U313 status --porcelain > /tmp/m22/status.txt` prints nothing; `git -C ~/Workspace/dotfiles status --porcelain --untracked-files=all -- . ':!.orchestration' > /tmp/m22/status-main.txt` unchanged by you.
6. `/tmp/dotfiles-wt/U313-rows.tsv` holds the Part A rows (one per measurement) in the six-column form.

VERIFY
The coordinator reads the rows against the pasted launch.log, writes the decisions rows and the s21 observed cell, and schedules Part B.

CLOSURE
allowlist

TRUST
TRUST: the spike trusts the installed hcom-seat's canary and settings shape and copies them; it adds one subagent provider row in a scratch profile only; makes no model turn in Part A and at most two on the operator's login in Part B; reads no credential; writes nothing outside `$SPIKE`, `/tmp/m22/` and the two files under `/tmp/dotfiles-wt/`.

TIMEBOX
90 minutes for Part A; Part B 30 minutes once the coordinator unblocks it.

FORBIDDEN
No change to hcom-seat, the thak profile, the manifest or the omp-gateway plugin; no install under `~/.local/bin`; no write under the real `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local/state/omp-seats`, `~/Workspace`, or the store; no `allowNestedUserNamespaces`; no API key in any env or patch; no `/v1/messages` request in Part A; no push; no `gh` call; no commit in the read-only worktree; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/m22/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git write commands or edit files in `~/Workspace/dotfiles` or `/tmp/dotfiles-wt/U313`; never edit the live store.
- Progress line at `/tmp/dotfiles-wt/U313-progress.txt` after every step; final report to `/tmp/dotfiles-wt/U313-report.txt` before you end.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Prove It Works: every row is a pasted line; Explain the Number: name what each measurement does and does not show).

REPORT
Status, the nested-srt result, the two launch.log lines, whether Part B ran and its blocker if not, the rows file path, deviations. Under 14 lines.

STANDING
`preferences.md` (orders 21, 30, 41, 42, 44, 46, 47); `briefs/U272-hcom-seat-dsh-role.md`; `briefs/U310-dsh-role-provisions-its-omp-profile-with-the-bridge-route.md`; `tests/dsh-login-route.tsv` g6; `tests/sandbox-write-denies.tsv` s21; `decisions.tsv` M-21 rows and the g6 rows of 2026-11-06T19:22Z; `.private/harness-kit/PRD.md:278`; `.private/harness-kit/plan/tasks.tsv:364-375`.
