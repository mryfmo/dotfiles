Reading additional input from stdin...
OpenAI Codex v0.162.1
--------
workdir: ~/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a15378-25ba-7710-afe7-865faaaf6088
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
I’ll review the task’s stated controls and cited evidence against the host conditions you listed, using the Ponytail review and agmsg-orchestration guidance. This will remain read-only.

exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
---
name: agmsg-orchestration
description: Coordinate structured agmsg task orchestration between an orchestrator seat and worker seats (Codex or Claude Code). Use when Codex or Claude Code needs to run or supervise AGMSG-TASK / AGMSG-RESULT / AGMSG-ACCEPTANCE workflows, bootstrap workers in herdr panes, manage .orchestration artifacts, act as an agmsg worker, or document the flue-pi style orchestration protocol.
---

# agmsg orchestration

Use this skill for structured multi-agent work where an orchestrator seat assigns bounded tasks to worker seats through `agmsg` teams. The `agmsg-orchestration` rule states the invariants; this skill holds the procedure. Use the regular `agmsg` skill for simple send/inbox/history commands.

## Architecture

- The orchestrator writes task files, starts workers, reviews artifacts, and sends acceptance or revision messages. It is Claude Code in the `herdr-agents` pair, or Codex under `codex-orchestrate` when the manifest's `orchestrator_kind` is `codex` (README "Codex orchestration without a pane").
- Workers, seats of the manifest's `worker_kind` (Codex or Claude Code), execute one assigned task: they read the task file, obey file and action constraints, write artifacts, and send the required result message.
- `agmsg` is the message bus. Use only scripts under `~/.agents/skills/agmsg/scripts/`.
- `herdr` panes are optional worker terminals; they are a launch surface, not the protocol.

## Regime activation and progress

- Activate this regime when the operator requests agmsg/Codex collaboration, or when the agmsg bus is available and a seated worker exists for the repository, such as in a herdr-managed workspace. agmsg is then the always-on communication path and Claude acts only as orchestrator: lightweight grep/read, judgment, task authoring, and acceptance review. The operator may opt out for the current task; only then may the orchestrator mutate the repository directly. When the bus exists but no worker is seated, seat one before any repository mutation (`herdr-agents --add-worker [<worktree>]`, default the manifest `worker_worktree`), and remove it with `herdr-agents --remove-worker <worktree>` once its task is accepted; "no worker" is never an implicit opt-out. In a regime repository the SessionStart `herdr-agents --attach` hook prints this directive as an `agmsg-orchestration:` line after `seat_claim=` in the orchestrator's Herdr pane, or after the summary line in a pane-less session.
- On activation, verify CompactionDB opt-in for the active repository and install it with `compactiondb-install` if missing. Regime start is operator-initiated consent to the install; acceptance-time decision consolidation then applies.
- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
- Start checklist (operator or orchestrator, repository cwd, plain shell or Herdr): the workspace created by `herdr-agents <DIR>` full mode holds the orchestrator pane only, and only the operator creates or relaunches it; inside a Herdr pane the SessionStart `--attach` hook claims the orchestrator seat and prints the directive, and never seats, restarts or repairs a worker. Inside Herdr or outside it, the orchestrator seats a worker on demand with `herdr-agents --add-worker [<worktree>]` (its own tab of the managed workspace, or its own workspace for a pane-less orchestrator), confirms it by PING/PONG before any task, and removes it with `--remove-worker` when the task is done. A Claude that finds itself outside Herdr is the pane-less orchestrator of the bullet above: its SessionStart line reports the state, and it brings the regime up on demand exactly as that bullet describes (composite seat claim outside the sandbox, `--add-worker`, PING/PONG before any task, headless auditor); anything neither bullet describes is not improvised.
- Seat and remove a worker only with `herdr-agents --add-worker` and `herdr-agents --remove-worker`; `--restart-worker` is retired and exits 2. Never run full mode from inside an existing managed workspace; the orchestrator and its worker tabs share one workspace. Activate a worker model or profile change by removing the worker with `herdr-agents --remove-worker <worktree>` and seating it again with `herdr-agents --add-worker <worktree>`, which sources launch args from `~/.agents/model-profiles.env`; never pass ad-hoc flags.
- Do not idle-wait while worker work is in flight; prepare or delegate independent work.
- A blocker reported to the operator carries attached evidence: the exact command, its exit code, and the messages.db `read_at`/PONG query, after the wake path that worked in earlier sessions (`agmsg-dispatch`) has been tried. An inference (for example "trust dialog" from a `poke.sh` exit 15 plus a spawn readiness timeout) is not a reportable blocker. `herdr-agents --add-worker` ends with that evidence for a fresh seat: one `linkage=ok read_at=<ts> pong=<yes|no>` or `linkage=unreached rc=<n> hint=<agmsg-dispatch|poke|attach-a-client>` line from an `agmsg-dispatch` PING, and it exits non-zero only when the PING was not read.
- Detect worker completion only when an `AGMSG-RESULT` arrives through monitor/turn delivery. Send liveness checks only as `AGMSG-PING`/`AGMSG-PONG`; never read worker panes or screens (including read-only probes such as `pane read`/`pane wait-output` against another agent's pane, even to learn output shapes; use `--help` and fake CLIs), infer completion from pane/agent status, or use ad-hoc polling sleep loops. Limit pane interaction to prompt injection and the submit key.
- If an out-of-band Codex completion signal is needed, use the official `notify` config: the `agent-turn-complete` event sends a JSON payload to an external command.

## Parallel workers

- Add and remove parallel workers only with `herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile NAME]` and `herdr-agents --remove-worker <worktree> [--force]` (worktree under `.claude/worktrees/`). For Codex, seat ordinary tasks with `--profile standard`; use `--profile security` only for trust-boundary tasks (permgate, redaction or secret handling, sandbox or permission policy), per the model-selection rule, with an identity such as `codex-security-dot-aNNN`. Add-worker seats the worker in its own tab of the pair workspace, labeled `<team>:<name>` with the pair tab untouched (in its own workspace only when no pair workspace exists, as in the pane-less bring-up), through upstream `spawn.sh --project <worktree> --terminal-driver herdr` with the profile's launch args in a generated spawn options file, so a placement record exists and `poke.sh`/`despawn.sh` work. Remove-worker despawns it, then turns delivery off, leaves, and closes that tab (or workspace), refusing a dirty worktree without `--force`. Keep about three concurrent workers at most; raw herdr topology commands stay forbidden (T21 G7).
- Under upstream agmsg 1.5.0 self-naming, a pair's panes carry `<team>:<name>` labels rather than `claude-orchestrator`/`<kind>-worker`; `herdr-agents` recognizes the pair through the repository's agmsg seats (the orchestrator identity at the main checkout and the pair's own worker seat, never other team members) and never relabels a self-named pane.
- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
- The orchestrator acts directly, without delegation, only under these exemptions: agmsg/herdr control-plane operations and evidence-sync bookkeeping; acceptance and final integration, including merging an already-reviewed, CI-green PR; and machine-state hygiene that touches no repository (tool-manager operations such as `mise install`/`mise prune`, removal of unmanaged `$HOME` files), provided tracked worktrees stay diff-clean throughout. It declares which exemption applies in one line before mutating anything.
- A parallel assignment is valid only when every concurrent worker has all four of: (1) its own git worktree registered as its agmsg `project`; (2) the shared default agmsg store for same-repository work, never a per-worker `AGMSG_STORAGE_PATH`, because identity-addressed delivery and worktree-specific `whoami` already isolate inboxes and one activation watcher observes every RESULT/PONG without extra watchers (which `watch.sh` actas locking cannot support for one claimed identity); (3) an `-aNNN` identity suffix on every concurrent worker, including the first; and (4) an AGMSG-TASK whose expanded `allowed_files` are pairwise-disjoint from all other in-flight tasks for code files; a shared prose file (README, SKILL) may appear in two in-flight tasks only when their sections do not overlap. The orchestrator verifies disjointness and performs all cross-worktree merge, rebase, and conflict integration.
- Parallel execution procedure:
  - At plan approval, partition the approved tasks into waves by dependency and file overlap: code files pairwise-disjoint, and shared prose files in disjoint sections. Write the wave table into the plan file.
  - Keep at most three workers in total. Seat workers with `herdr-agents --add-worker` only up to that cap. Dispatch at once as many tasks of the current wave as there are free seats, each with a distinct `-aNNN` identity and its own worktree, and queue the rest of the wave.
  - When a RESULT arrives, run acceptance for that task while the others continue; acceptance follows RESULT arrival order.
  - A freed worker is re-tasked immediately with the next dependency-free task whose files overlap no in-flight task. Never leave a seated worker idle while a dispatchable task exists. The next task starts on a fresh branch from `origin/main`, and the previous task's branch stays in the worktree, untouched, for its revise rounds and until its acceptance. The worker commits and pushes everything before each RESULT, and before every branch switch it commits the newer task's work (or stashes it under a named tag and restores it afterwards), so a switch never carries edits across branches. When a `status=revise` arrives for the earlier task, it checks that branch out again, does the round, and returns to the newer task's branch, so the worktree is reused sequentially and nothing uncommitted is ever left behind.
  - When a merge moves `main`, every in-flight PR whose base moved, prose or code, merges the new base into its branch with `gh pr update-branch` before its CI, Bot wait and gate. The ruleset's strict up-to-date policy refuses the merge otherwise. `gh pr update-branch` creates a merge commit by default, not a rebase. A real conflict blocks only that PR.
  - Record the wave table and the per-task worker in the acceptance records.
  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
- At parallel-worker teardown, run `delivery.sh set off <type> <worker worktree path>` to stop every watcher on that exact path, then `leave.sh <team> <worker identity>` for each finished worker. The last member of a task-scoped team leaves so the team is deleted while message history remains. Verify with `identities.sh <project> <type>` by counting distinct identity names in the second TSV column: while a worker is seated, one distinct name per type at its worktree is healthy, including multiple rows for that name across teams; the only active seat, the main checkout, holds exactly one name across both types, and a worker worktree holds none once its worker is removed, which `make check-regime-boundary` enforces. More than one distinct name indicates leftover identities that trigger the herdr-agents ambiguity warning at attach and must be cleaned with `leave.sh`; preserve legitimate multi-team memberships of the retained name. Zero names for a project that should remain active must be restored with `join.sh`, never leave-side edits.

## Identity, delivery, and storage

- Give each physical agent one unique identity: `<runtime>-<profile>-<project-suffix>` (for example, `codex-standard-dot`, or a `-flue` suffix for flue-pi). The project suffix derives from the repository, not the checkout; model IDs belong only in `model_profiles` in `agent-config.yaml`. A solo worker has no instance suffix. For parallel workers, rename the incumbent to `-a001` so team registration and message history follow, give every worker an `-aNNN` suffix, re-claim actas locks after rename, and never mix suffixed and unsuffixed identities.
- Before joining, search every `~/.agents/skills/agmsg/teams/*/config.json` for the candidate name. On collision, choose a unique suffix; never reuse one identity for different physical agents.
- Register `project` as the worker's real working-tree path (the dedicated worktree for parallel workers), byte-identical across join, delivery setup, and hook arguments. Trailing slashes and unresolved symlinks orphan inboxes through exact-string mismatch. `$HOME` registrations are forbidden because they create Codex-hook ambiguity and steal inbox messages.
- Register a worker identity at its own worktree path with resolution off: `AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>`, and point its delivery at the same path with `delivery.sh set <mode> <type> <worktree>` so the hook bakes the worktree into the session's project marker. Every `join.sh`/`whoami.sh`/`actas-claim.sh`/`reset.sh`/`watch.sh` call a worker makes runs with `AGMSG_RESOLVE_PROJECT=0` (herdr-agents sets it in every worker pane it creates; `spawn.sh --project` sets it for agmsg-spawned seats). Upstream project resolution (#92, `docs/design.md` "Project resolution") otherwise rewrites the path in order: the live SessionStart marker `run/proj.<agent_pid>.project`, then the nearest registered ancestor, then the registered main checkout via `git rev-parse --git-common-dir`. Verified against a scratch v1.5.0 install: a `join.sh` from inside `.claude/worktrees/<x>` without the opt-out registers at the main checkout; a session whose marker names the main checkout (a seat launched from the main path) makes `whoami.sh` inside the worktree answer with the main checkout's identities; the opt-out restores the worktree in both cases. `session-start.sh` exits before the watcher and marker for any session whose cwd is under `.claude/worktrees/` (#367), so a Claude seat launched inside a nested worktree gets no Monitor watch from that hook: the herdr-agents pair worker relies on turn delivery (a spawn-seated worker starts its Monitor through its actas boot) or the inbox checks below. `identities.sh` stays a pure lookup of the exact path.
- On activation, check `delivery.sh status <type> <repo>`. This repo runs Claude Code seats on `both` (monitor's push plus turn's pull), one notch more redundant than upstream's Claude Code default `monitor`, since an unattended worker pane has no one to notice a Monitor watch that silently failed to re-arm; Codex seats run on `turn` (see the next bullet). If weaker than that, run `delivery.sh set both claude-code <repo>` (or `delivery.sh set turn codex <repo>` for a Codex identity), use the SessionStart-provided `watch.sh <session_id> <repo> <type>` started outside the sandbox as a persistent in-session monitor, and claim exclusivity with `actas-claim.sh <project> <type> <name> <session_id>`. A Claude worker seated by `--add-worker` gets its Monitor watch through its actas boot; when it is seated in its own workspace (no managed workspace exists), `herdr-agents` also sets `AGMSG_CC_MONITOR_KEEP_ALIVE=1` in that workspace's environment so the watch re-arms unconditionally on expiry, not only when the expired watch delivered something (upstream's default).
- `herdr-agents --bootstrap-agmsg` (and full or attach mode) sets the main checkout's orchestrator hooks, Claude Code on `both`; a worker seat gets its own hooks from `herdr-agents --add-worker`, Codex on `turn` and Claude Code on `both`, so the Stop/SessionStart hook in the worktree's tree-scoped, gitignored `.codex/hooks.json` or `.claude/settings.local.json` delivers inbox messages. Codex deliberately stays on `turn` instead of upstream's shim-based `monitor` bridge (the upstream README names `monitor` as the Codex default in one place and `turn` in its delivery table): as of agmsg v1.5.0 that bridge has open reliability defects an unattended resident worker cannot risk — no teardown on session end (upstream #149), a mode switch that does not start the bridge in a live session (#151), and a bridge that restarts forever while its status reports it alive (#1236), all still open. Storage resolution is env-only: keep `AGMSG_STORAGE_PATH` unset for same-repository default-store workers, or set it to the regime's dedicated store for separate cross-project regimes; a wrong or stray value silently reroutes the worker to another database. Pane nudges are only generic wakes; message content always travels over agmsg.
- Worker panes run in their worktree: `herdr-agents --add-worker [<worktree>]` seats the worker in that worktree (default the manifest's `worker_worktree`, created from `origin/main` when missing), registers its identity there with `AGMSG_RESOLVE_PROJECT=0`, sets delivery on that path, and starts it through upstream `spawn.sh`, so turn delivery reaches the worker directly through the worktree's Stop hook and its Monitor watch comes from the actas boot (upstream `session-start.sh` skips sessions under `.claude/worktrees/`, #367). The interim worker inbox discipline (running `~/.agents/skills/agmsg/scripts/inbox.sh <team> <identity>` at each milestone: task start, push, CI green, before RESULT, after any PONG) is retired for a worktree-seated worker; it applies only to a worker still acting under a worktree-registered identity from a main-path pane, until `herdr-agents --remove-worker` and `--add-worker` re-seat it.
- A codex worker in a nested worktree gets `<common>/objects`, `<common>/refs`, `<common>/logs` and `<common>/worktrees/<name>` (`<common>` from `git -C <worktree> rev-parse --git-common-dir`) as writable roots from `herdr-agents` (`-c sandbox_workspace_write.writable_roots`, with the configured agmsg roots kept first), so local git operations need no escalation. The common dir itself, `config`, `hooks`, `info`, `HEAD` and `packed-refs` stay read-only. The worker seat runs with `--ask-for-approval never` and `sandbox_workspace_write.network_access=true`, so a GitHub fetch, push or `gh` call works inside the sandbox and the worker never prompts: there is no escalation for a worker, and an action outside the sandbox or forbidden by the execpolicy fails and is reported as `AGMSG-PONG v1 status=blocked`. The `sandbox_workspace_write.network_access` switch is a boolean, so the worker reaches any host (no domain allowlist is configured, unlike Claude Code's `allowedDomains`), and the permgate PermissionRequest hook never fires for the worker seat; it stays live for interactive Codex sessions, which keep on-request approvals and no sandbox network.
- The orchestrator's actas seat lock must hold the composite instance id `<sid>.<pid>`; check it with `cat ~/.agents/skills/agmsg/run/actas.<team>__<name>.session`. `actas-claim.sh` run from sandboxed Bash cannot read the Claude pid, writes the bare session id, and the Stop-hook inbox check then skips delivery silently (`other:<sid>`). On macOS, the Claude Seatbelt sandbox denies `ps`; a `watch.sh` Monitor started outside the sandbox (by SessionStart or the orchestrator pane) keeps running, but one started inside computes the bare session id and exits against the composite actas lock. On Linux, the bubblewrap pid namespace hides the Claude pid: a sandbox-started Monitor exits "no longer alive", and `pgrep` sees only the sandbox. No seat starts its watch from sandboxed Bash. `herdr-agents` therefore claims the seat outside the sandbox when it starts the orchestrator pane and from its SessionStart `--attach` hook, printing `seat_claim=ok owner=<sid>.<pid>` (or `seat_claim=unresolved`, never a bare-id lock), and `make doctor` warns on a bare-id orchestrator lock while a claude session runs in the repository. When the Monitor is unavailable, turn delivery is the working path, and an idle orchestrator is woken by the worker's `agmsg-dispatch` to the orchestrator pane.
- Reserve store separation for concurrent regimes in different projects, such as flue-pi. When using it, set the same `AGMSG_STORAGE_PATH` in the worker pane and on orchestrator send/watch/history calls or tasks, results, and pongs become unreachable. Same-repository parallel workers always share the default store.

## Live verification

- Accept changes to live desktop behavior — herdr layout/session, pane lifecycle, or delivery hooks — only after live end-to-end verification covers both a fresh session and a persisted-session restore; unit and static tests alone are insufficient.
- Launch orchestrator-driven E2E test-subject panes with express-profile arguments from `~/.agents/model-profiles.env` (`MODEL_PROFILE_EXPRESS_CLAUDE_ARGS` / `MODEL_PROFILE_EXPRESS_CODEX_ARGS`), never ad-hoc `--model` flags.

## Review and integration invariants

- Review every RESULT adversarially across correctness, regressions, security, and reporting omissions: try to refute it, independently re-derive findings, and never treat sampled spot checks as full verification.
- Acceptance review, adversarial RESULT review, and review-profile work remain orchestrator-side; never delegate them to a worker, and keep `make require-crit-review` as the final integration step. Revisit only if worker-side model capability surpasses the orchestrator tier.
- A design review runs in paired rounds. Both reviewers, a fresh Claude context on the `review` profile and a Codex read-only run under a `codex-review` identity, get the same design hash at the same time. The orchestrator revises once per pair of results and opens no round while one is still open. The third pair is the last: on its accept the design is frozen at the hash the pair last accepted, the third pair's own, and whatever is still open at that hash becomes a residual list that is worker input; on its revise or reject nothing is frozen and the design goes back to a context other than its author, never to a fourth pair; a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). The review judges the invariants, threat model, trust anchors and premises for contradiction and enforceability, never implementation detail.
- A task-file review is one round with a fixed stop condition: no contradiction with the design, the premises hold, `allowed_files` covers every touch point that grep finds, and one invariant check (for a task that carries an `invariants` key: the task id maps to its `implementing_tasks` entry, the invariant ids match, and each invariant's sentence equals the design's byte-for-byte, the design read from main (INV-2), checked by hand in the review; a task without the key needs no entry). Anything finer belongs to the worker and the implementation PR.
- A boundary PR synchronizes records at a boundary. It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition.
- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
- A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by `scripts/orchestrator/task-consistency-check.py` (C1 to C10 and C7b) before dispatch and at acceptance, confirmed by the review seat), never as a PONG answer.
- When a finding class reaches three on one artifact (the record's ledger) or `scripts/regime-counters.sh` prints an S1 candidate, the next acceptance action is the records search for that class, pasted into the record as the line `search: <class> -> <the matching mistake records or none>`, and the matching correction is applied when its mechanism is landed, or landed first when it is pending, mechanism by mechanism, before any dispatch; a class is a slug of `[a-z0-9-]` assigned at disposition time, never text taken from a review title. `scripts/orchestrator/three-repeat.sh <class>` validates the slug, runs the records search and the CompactionDB search without a shell and prints the line. The gate (`scripts/require-crit-review.py`, S6) refuses the merge for a ledger class at three or more rows whose `searches` entry does not equal the mistake records naming the class; `acceptance-front-matter.py` writes the entry from the same lookup. Pasting the `search:` line and applying the correction before any dispatch remain the orchestrator's rule. Every `not-applicable` disposition carries `; evidence=<command>` with the output pasted in the record.
- At regime or session boundaries, write pending acceptance records, then mechanically commit every `.orchestration` file so no untracked tail remains. The sync needs no per-task artifact set: its audit record is the commit, whose message lists covered task IDs, plus agmsg ACCEPTANCE history. `make check-regime-boundary` reports a canonical clone with unmerged entries, a stash, or a difference from `origin/main` under `home/`, `install/` or `scripts/` as a sign that something ran where it must not. Lessons from a session are codified in this repository (a rule, the skill, or a check) through a task; Claude auto-memory is not a durable store for regime procedure. The canonical clone is pull and apply only and untouched by any seat: no edits, no apply from a dirty tree (the run_before guard refuses it), and one orchestrator identity per repository, seated at the working clone.
- Stop checklist, at every regime or session boundary and in this order: write pending acceptance records; mask every `.orchestration` file the boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`, which also normalises home directories to `~`; run `make validate-agent-assets` (real exit status); make the `.orchestration` boundary commit with zero untracked tail on a fresh `orchestration/boundary-<YYYY-MM-DD>` branch from `origin/main` and merge its PR with `gh pr merge --squash --auto`, queued only while no other PR is between its final head and its merge (plan 020 step 3; otherwise the boundary PR waits and is merged after that PR); remove every worker with `herdr-agents --remove-worker <worktree>` (despawn, delivery off, leave, tab or workspace closed); check stale identities with `identities.sh <path> <type>` (exactly one name at the main checkout, none at a worker worktree); close Crit review servers (`pgrep -f 'crit _serve'` must be empty); in a CompactionDB-opted-in project, review `uv run --no-project .claude/hooks/contextdb_cli.py memory candidates --limit 20` and promote each candidate worth keeping with `uv run --no-project .claude/hooks/contextdb_cli.py memory promote <id> --scope project`, or leave it. The orchestrator workspace itself stays resident for the next session unless the operator restarts the machine. `make check-regime-boundary` (`scripts/check-regime-boundary.sh`) checks this list and the orchestrator seat lock, one line per violation.
- Before every `.orchestration` boundary commit, run the masker on the files it adds or changes (`uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`), then `make validate-agent-assets`, and branch on its real exit status, never through a pipe; fix a failure before pushing, because committed audit evidence can trip the secret scan, which also rejects a home directory path in `.orchestration/**`.
- The orchestrator never pushes a repository change to `main` directly. `main` is protected by the GitHub ruleset "main integration gate": a pull request is required, review threads must be resolved, the seven required checks must pass under the strict up-to-date policy, and `main` cannot be deleted or rewound. The `.orchestration` boundary commit goes on a fresh branch from `origin/main`, `orchestration/boundary-<YYYY-MM-DD>` (suffix `-2`, `-3`, … for another boundary the same day, since merged branches are kept), opens as a PR, and is merged with `gh pr merge --squash --auto`: each required job decides inside itself and reports success on an `.orchestration`-only diff; a skipped required job would report Success (fail-open), so no required job carries a job-level `if` or a `needs`. An acceptance merge happens only on GitHub using step 10.5; a local merge followed by a push is no longer a path.
- For CompactionDB-opted-in projects, verify during the sync that every accepted task has a consolidated decision record.
- A `.ua/` graph RESULT is accepted only when its validation file pastes the table from `ua-symbol-coverage <previous-graph> <new-graph> --old-ref <previous-graph-rev> --repo-ref <new-graph-rev>` (on PATH from `~/.local/bin/common`; each rev is that graph's `.ua/meta.json` `gitCommitHash`, the new one normally `HEAD` and never the pre-change base; `--old-ref` tells renames from deletions) with zero regressions, or cites the source change behind each decrease; `validateGraph` passing does not prove extraction completeness.
- Task-level audit: every RESULT that changes repository code gets one audit of the task on its final head, covering the whole PR diff (`git diff <merge-base> <head>`).
  - Pair form, in the pair workspace's dedicated audit tab: `herdr-agents --audit <head-sha> --task <id> [--out <path>] <main DIR>`. It writes `.orchestration/validation/<id>-audit-<sha7>.md` and codex's final message to that file's `.last.md` companion, whose last non-blank line is the verdict.
  - Headless form, without a pair workspace, with `<out>` = `.orchestration/validation/<id>-audit-<sha7>.md`, run from the orchestrator's own checkout (never one that sits at the audited head):
    - Give codex the same task-level inputs the pair form builds: the task file `.orchestration/tasks/<id>.md` (required), the worker's report, validation and sandbox files and `<id>-pr-feedback.json` (those present), the final head `<head-sha>` and the PR diff `git diff $(git merge-base origin/main <head-sha>) <head-sha>`. Ask for findings as `[P0-P3] confidence dimension file:line rationale` and exactly one concluding `Verdict: correct|incorrect|blocked` line.
    - Run `rm -f <out> <out>.last.md && set -o pipefail && codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md '<that prompt>' 2>&1 | tee <out>`. Removing both files first means a failed rerun can never leave an earlier `Verdict: correct` behind, as the pair form also ensures, and `pipefail` keeps codex's exit status through `tee`. A nonzero codex exit means no audit: there is nothing to gate, so rerun it.
    - Only after a zero exit, mask both files with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <out> <out>.last.md` from a trusted checkout. Like the pair form, refuse when that checkout's HEAD is the audited commit, or when its validator is missing, untracked, or changed against HEAD (`git diff --quiet HEAD -- scripts/validate-agent-assets.py`), so a PR can never run its own validator on the orchestrator. Treat a refused or failed masking as a failed audit.
    - The gate needs both the transcript file and its non-empty `.last.md` companion.
  - Run either form from a clean tree: the only untracked content in the audited checkout is this task's `.orchestration` evidence that the audit prompt names (task file, report, validation, sandbox file, feedback JSON). Otherwise run it from a dedicated clean checkout, so no other edit can reach the auditor.
  - A new push, including a `gh pr update-branch` merge, needs a new audit of the new head.
  - The orchestrator dispositions every `[P0-P3]` finding in the acceptance record, whatever the verdict, numbered 1..N in the audit's order of `[P0-P3]` lines (the audit's finding lines may be bulleted). For an `incorrect` verdict the dispositions are the record's JSON `audit_findings`, the only form the gate reads: one `{n, reason, evidence}` entry per finding, `n` the number as a string and `reason` at least 20 characters, written with `scripts/orchestrator/acceptance-front-matter.py --audit-dispositions <tsv>`; an entry never cites a fix, since a fix moves the head and needs its own audit. A finding under `Verdict: correct` is dispositioned all the same, as an `audit-finding: <n> …` line in the record's prose: `fixed:<sha>` with a fresh audit of that sha, otherwise `not-applicable:<reason of at least 20 characters>`. Deferral ("later", a follow-up task, a stopgap or a suppression) is not a disposition except under the advisory-P2 policy in Orchestrator Playbook step 10.
  - The audit evidence and the PR-feedback JSON quote reviewed content, so mask them with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>` before they are committed. The gate compares PR-feedback bodies after the same masking, so masked feedback evidence still matches the live collection (T93, #251).
  - Audit findings are input, never approval; acceptance authority stays with the orchestrator, and each RESULT gets its own acceptance record.
- Crit is agent-side only for Claude Code and Codex alike, as in `home/dot_config/claude/rules/crit-review.md`: record crit-data evidence (`crit status --json`, `crit comments --all --json <review.json>`) and never open a browser review to ask the user. When Crit data is unavailable, save the independent agent review as the same repo-local JSON list (objects with non-empty string `id`, `body`, `scope` and `resolved: true`, at least one `scope: "review"` or path-bound `line`/`file` record; hand-written records are acceptable because the guard validates shape, not provenance) and reference it from a `review_surface: crit-data` receipt with `reviewer: claude-code`, `claude`, or `codex`, `review_source: <that JSON>`, and `review_outcome: approved` or `addressed`. Run `crit share` or any other publish step only when the user explicitly asks for it. Close a Crit session opened by the Plan Mode hook once its review is done, so no local Crit web server stays resident.

## Message Contract v1

Send messages as single-line records so inbox/history output stays parseable.

`AGMSG-TASK v1` fields:

```text
AGMSG-TASK v1 task_id=<id> repo=<absolute-repo-path> task_file=<path>
allowed_files=<paths-or-see-task-file-section> forbidden_actions=<semicolon-list>
expected_result_file=<path> expected_validation_file=<path>
expected_sandbox_file=<path> expected_learning_file=<path>
expected_autoskill_file=<path> done_signal=AGMSG-RESULT max_turns=<n>
note=act-as-worker-<task-or-role>
```

Task files must state durable facts with `[memory:decision]` or `[memory:failure]` markers using the tag form, bracket form, and kind aliases defined by the vendored CompactionDB README.

`AGMSG-RESULT v1` fields:

```text
AGMSG-RESULT v1 task_id=<id> status=ready_for_review|blocked
report=<path> validation=<path> sandbox=<path> learning=<path> autoskill=<path>
```

Tasks that create persistent side effects outside the repository working tree, such as global asset installs, writes under `$HOME`, or external service registrations, include the optional field `effects=<semicolon-list-of-short-ids>`. In-repository edits within `allowed_files` are not effects. For each declared effect, the report must state its reverse mapping: a named `~/.agents/.installed-manifest.json` step removable with `remove-agent-asset`, a documented removal procedure, or an `irreversible:` statement with rationale.

RESULT reports must mark durable facts with the same CompactionDB marker contract. In CompactionDB-opted-in projects, the worker runs `uv run --no-project .claude/hooks/contextdb_cli.py memory add` before completion and includes the exact command or commands in the RESULT report.

RESULT validation files must contain the verbatim output of every validation command actually executed — not summaries or PASS labels alone — and any identifier the report claims to have created (commit hash, PR number, CompactionDB memory/decision ID) must appear in that pasted output. A claim without its pasted output is treated as unexecuted and grounds for `status=revise`.

`AGMSG-ACCEPTANCE v1` fields:

```text
AGMSG-ACCEPTANCE v1 task_id=<id> status=accepted|revise reason=<short-reason> next_action=<action>
```

Each acceptance record also includes a `cost:` line with worker-reported token/cost figures when available, otherwise `cost: n/a`.

A RESULT with a P0/P1 surviving the one worker-side fix round carries `bot_rounds=2` and lists it as `open:<thread id>` (`open:review-<review id>` for a review-body finding); the PR stops for the operator's decision (Worker Playbook step 15). A `status=revise` ACCEPTANCE carries `previous_head=<the RESULT head being revised>` and one failing-test selector per finding (`check=tests/<file>::<name>`); the worker records both in `.orchestration/<task id>/revise.yaml`, beside the task.md copy.

Liveness messages:

```text
AGMSG-PING v1 task_id=<id> reason=<short-reason>
AGMSG-PONG v1 task_id=<id> status=alive|blocked|question note=<short-note>
```

`question`: the worker holds and asks; INV-6 counts it.

## `.orchestration` Workspace Layout

- `tasks/`: orchestrator-authored task specs.
- `reports/`: worker reports and blocked-task reports.
- `validation/`: command output and validation evidence.
- `acceptance/`: orchestrator acceptance, revision, or rejection records.
- `sandboxes/`: per-task isolation records (sandbox/worktree evidence).
- `autoskill/config/`, `autoskill/inputs/`, `autoskill/runs/`, `autoskill/outputs/`: redacted AutoSkill artifacts.
- `learning/`: task learning triage records.
- `learning/rule_candidates/`: candidate reusable rules only.
- `skills/candidates/`, `skills/promoted/`, `skills/rejected/`, `skills/merged/`: separated skill registry states.
- `agmsg/`: exported or summarized agmsg history when needed for review.

## Orchestrator Playbook

1. Join or confirm the agmsg team and identities with the `agmsg` scripts.
2. Create the `.orchestration` directories before assigning work.
3. Write a task file that includes objective, scope, allowed files, forbidden actions, expected artifacts, validation commands, and max turns. Name the render check as `make render-check`, never the bare `python3 scripts/generate-agent-configs.py --check`, which fails without PyYAML. Ground `allowed_files` by grepping the repository for every touch point the task names (tests that pin call sequences, mirrors, fixtures) before dispatch. Verify every CLI constraint the task asserts by running the real command in a safe form, not by reading `--help`. Presume an auditor finding that contradicts your own review is right until you refute it with evidence. Decide the worker kind from the allowed files before dispatch: a seat never edits the source of its own execution boundary, so a change is routed by the boundary it touches. A change that touches only Claude's boundary goes to a Codex seat: the `claude.permissions`, `claude.sandbox` and `claude.hooks` blocks of `home/dot_agents/agent-config.yaml` (including excludedCommands, allowUnsandboxedCommands, writable roots, network and the PermissionRequest hook), the Claude-rendering parts of `scripts/generate-agent-configs.py`, the rendered `home/.chezmoitemplates/claude-settings-managed.json`, and `home/dot_claude/modify_private_settings.json`. A change that touches only Codex's boundary goes to a Claude seat: `codex.sandbox_workspace_write`, `codex.approval_policy`, the Codex-rendering parts of the renderer, and `home/.chezmoitemplates/codex-config-managed.toml`. A change that touches both, or a shared source the orchestrator cannot split (such as `codex.sandbox_workspace_write.writable_roots`, which also renders into Claude's `allowWrite`), goes to the operator. The orchestrator decides the kind from the diff the task will produce and records it and the chosen worker profile in the task file. The Claude Code auto-mode classifier also refuses a Claude-boundary task on a Claude seat as Self-Modification. A task that edits permgate (`home/dot_agents/permgate-policy.yaml`, `home/dot_local/bin/common/executable_permgate`), the PermissionRequest hook of both seats, goes to the operator; a Codex `security`-profile worker reviews the change before the orchestrator accepts it, per the model-selection rule. `auto` is Claude Code's built-in starting permission mode since 2.1.283. A project-level `defaultMode: auto` (`.claude/settings.json` or `.claude/settings.local.json`) does not take effect, and the session then also ignores the user-level `defaultMode`, so `auto` belongs only in user or managed settings. Before dispatch, read the task's verbatim blocks against each other for contradictions, and state each rule once; a second artifact references the first instead of restating it.
4. Start or relaunch worker panes only through `herdr-agents` modes. Deliver messages and wakes as in step 6; never use `pane send-text` followed by `send-keys Enter`, because the separate Enter races the TUI composer and fails nondeterministically.
5. Configure delivery deliberately. `delivery.sh set turn` is useful for turn-end inbox checks; changing delivery mode can kill project watcher processes, so do it before starting long-running project watchers.
6. Send `AGMSG-TASK v1` with the exact artifact paths and `done_signal=AGMSG-RESULT`. Pass every `send.sh`/`poke.sh` body with `--body-file <path>` (both take it in agmsg v1.5.0), never as a positional argument: a positional `<text>` passes through the caller's own shell first, where a backtick or `$( )` in the body silently executes and vanishes from what arrives (upstream #378). `agmsg-dispatch` is the one exception and takes a single-line, shell-safe positional message. Pick the path by how the recipient is seated, never by inferring pane or agent status: a worker in a `herdr-agents` pane gets `agmsg-dispatch <team> <from> <to> <pane_id> "<message>"` (send, generic wake, `read_at` wait; single-line shell-safe text only), the sanctioned wake path until worker seating writes placement records at launch, because `poke.sh` exits 1 with "no placement record" for a hand-joined member, and a herdr-agents worker gets a record only once it acts from its own pane (upstream `send.sh`/`inbox.sh` record the acting pane, #1109); a spawn-seated member (placement record `run/spawn.*`; `team.sh <team> --json` shows its pane) gets `poke.sh <team> <name> --body-file <path> [--retries N --retry-delay SECONDS --backoff fixed|exponential]`, which types and submits in one call and refuses to type over an in-progress draft (#1321/#1322); a pane-less member gets `send.sh <team> <from> <to> --body-file <path>` and its own delivery mode. Verify delivery via the messages.db `read_at` column. `poke.sh` exit codes: 10 = terminal unreachable, 12 = pane gone or no live agent, 14/15 = refused to type over a changing or unlocatable input box, 13 = the driver has no poke path for this pane (for example a `plain` terminal); where poke.sh's narrow agmsg-message fallback succeeds it exits 0, so 13 means nothing was delivered, and the printed reason names the native channel, asks the caller to claim its own identity first, or reports that the fallback failed. Never retry a 13 as `send.sh` yourself: that overrides the driver's considered refusal and can double-deliver. Seating case: a worker in an unviewed or headless Herdr workspace (no client attached, a small pane rect such as 18x41) makes `poke.sh` exit 14/15 from its TUI input locator; that is a locator refusal, not evidence about the worker's state, so wake it with `agmsg-dispatch` and verify `read_at`. Every dispatch (TASK, ACCEPTANCE, PING) is recorded in the current acceptance record under a `dispatch:` key as the bus line with its read marker, so the orchestrator creates that record, `.orchestration/acceptance/<task>.md`, before the task's first dispatch (`scripts/orchestrator/dispatch.sh` refuses a record that does not exist or that names another task); a seat is reported as working only from such a line, and after a context compaction the open TASK list is re-derived from a bus read that is refused when it reaches its limit (`bus-read.sh` exits when the history reaches `BUS_READ_LIMIT`; the orchestrator raises the limit and reads again), never from a default-limited one and never from a read whose truncation went unnoticed. A seated worker idle for 20 minutes since its latest bus event for the task while a dispatchable task exists (INV-10's idle figure; its 30 minutes is the first-push deadline) gets a bus read, then a PING; a longer silent wait is never the answer. `scripts/orchestrator/dispatch.sh` writes the line and `scripts/orchestrator/bus-read.sh` performs the read and prints the minutes since each open task's latest event (both on main since a03c1daa, plan 007 T718); the orchestrator applies the 20-minute figure to the minutes the script prints (the script's own silence flag still uses 30 minutes, a recorded residual of the tools lineage).
7. Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls.
8. On `AGMSG-RESULT`, read the task file and every referenced artifact before deciding.
9. For a RESULT carrying `effects`, verify that every declared effect has the report's stated reverse mapping before acceptance; record any irreversible effect in the acceptance note.
10. For a RESULT that carries a pull request, integrate in this order. This is the single procedure that the PR integration rule, `AGENTS.md`, the README and the gh-first-workflow skill cite. A `gh pr update-branch` moves the head, so steps 1 to 4 run again on the new head. After an update-branch the orchestrator runs it, the order is CI on the new head, then the sweep, then the audit; an audit started before CI finishes sees incomplete evidence and returns an evidence-only `incorrect`. Select a checkout with git -C <absolute path>, never with cd, which the sandboxed Bash may not honour. After moving the review worktree to the audited head, verify git -C <review> rev-parse HEAD equals that head and git -C <main> symbolic-ref --short HEAD prints main before the audit and the gate.
    1. Sweep the final head's feedback with `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json` and give every item a `fixed:<commit>` or `not-applicable:<reason>` disposition, leaving none on `failure` or `warning` annotations. Optionally request `@coderabbitai full review` on the final head first; when a CodeRabbit review exists it is swept like any other item, and the gate does not require a bot review. An `open:<thread id>` or `open:review-<review id>` item surviving the worker's fix round follows Worker Playbook step 15's operator-decision path; the PR is not merged, never with the thread open.
       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
       - Except that a small P2 on the PR's own change whose fix stays within the task's `allowed_files` is fixed in a revise round sent by the orchestrator with a `check=` while INV-6's counts allow it.
       - The post-round audit of the final head is the single authority on the PR's findings, dispositioned finding by finding before the gate; a P0/P1 it leaves is the operator's decision, and the merge follows sub-step 5.
    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
    4. Run the gate: `AUDIT_EVIDENCE=<audit> AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> ACCEPTANCE_EVIDENCE=<acceptance record> BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review`.
       - A `review` sweep item whose body carries a `P0`–`P3` badge is a finding with its own `fixed:<commit>` or `not-applicable:<reason>` disposition, never a container for its inline threads.
       - The sweep covers issue comments, reviews, inline review comments with thread resolution, non-passing check runs, check-run annotations at every level (`notice`, `warning`, `failure`), and commit statuses. A `failure` marked `not-applicable` needs a concrete reason of at least 20 characters.
       - A CodeRabbit full review is optional, at most once on the final head: the plan allows one review per hour and every review event spends one (docs.coderabbit.ai/management/rate-limits).
       - The feedback JSON may be masked with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets`, which masks its keys and string values; the gate identifies an item by its source, url, level, path, line and body, and accepts a body or path that is verbatim or exactly that masked form.
       - The gate rejects evidence outside `.orchestration/validation/` or without the `-pr-feedback.json` suffix. It binds `BASE` to the PR's GitHub base before running the collector from that authenticated SHA: an older base must be outside HEAD's first-parent chain, an advanced base must preserve the merge-base with the PR head, and PR branch commits (including `HEAD`) cannot substitute for the base. Evidence must match the local GitHub repository independently of `GH_REPO`, and `fixed:` commits must be in the authenticated GitHub base-to-head range whatever `BASE` is selected.
       - `AUDIT_EVIDENCE` must be the task-level file `.orchestration/validation/<task>-audit-<sha7>.md` (the same `<task>` as the feedback JSON); a per-commit `audit-<sha>.md` is rejected. Its verdict comes only from the non-empty `<file>.last.md` and must be `correct`, or `incorrect` with an `audit_findings` entry in the acceptance record for each of its findings. PRs that change only `.orchestration/` files need no audit.
       - A boundary PR (`orchestration/boundary-<date>[-n]`, `.orchestration` files only) skips the gate, the sweep JSON and the audit (with `BASE` set the gate would demand `PR_FEEDBACK_EVIDENCE`); each Bot thread on it still gets a disposition reply and is resolved, and the next boundary commit message names the PR.
    5. After the required checks pass and the threads are resolved, merge with `gh pr merge <pr> --squash --match-head-commit <audited head sha>`, so a newer head can never be merged on the evidence of the audited one. Every seat acts as the machine's one GitHub account, so no approval is required or possible. Who merges is decided by the integration gate and by native denial of merge commands in Codex seats; `herdr-agents` writes the Claude worker deny rules (`Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`) into the worker worktree's `.claude/settings.local.json`, where [deny rules take precedence over allow rules and cover nested subcommands in every permission mode](https://code.claude.com/docs/en/permissions), but a method flag after the path escapes these prefix rules, so the integration gate remains the authority.
    6. Send `AGMSG-ACCEPTANCE` (step 11).
11. Send `AGMSG-ACCEPTANCE v1 status=accepted` when done, or `status=revise` with a narrow `reason` and `next_action` when more work is required.

## Worker Playbook

1. Read the full `AGMSG-TASK v1` message.
2. Switch to the `repo` and read `task_file` before editing or running validations. Create the task branch without touching the shared `.git/config`, which is read-only for a Codex seat by design (T64 writable roots): `git switch -c <branch> --no-track origin/main`, push with `git push origin <branch>` (no `-u`), and open the PR as a draft with `gh pr create --draft --head <branch>`. Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there; for a Claude seat only the push leaves the sandbox, and a Codex seat pushes from inside it (step 4). A Claude seat's sandbox can leave the same failed write behind, so it uses the same commands. A leftover `.git/config.lock` from a failed attempt is removed by the orchestrator. Remove a scratch worktree (for example one that proves a test fails on `origin/main`) with `git worktree remove <path>` only; never run `git worktree prune` from a sandboxed seat, because other worktrees' paths look missing inside the sandbox and prune then targets their admin directories in the shared `.git/worktrees`.
3. Treat `allowed_files` as the edit boundary. If it says to see the task file, read that section and follow it exactly.
4. Do not perform any `forbidden_actions`. Complete every command inside the sandbox and allowlist; never escalate an action outside that boundary for approval. Fail it instead, send `AGMSG-PONG v1 status=blocked` with the exact command and the boundary it crosses, and wait for the orchestrator to re-task. Agent-to-agent permission approval is forbidden: only the human operator answers a permission prompt. A Claude Code auto-mode classifier denial (for example Self-Modification) is such a boundary: stop without a diff, send `AGMSG-PONG v1 status=blocked` naming the classifier reason, and never pursue the same outcome through another tool. Fetch and fast-forward inside the sandbox; a public remote needs no credential. For Claude seats on macOS, Seatbelt denies the Mach lookup of `com.apple.trustd.agent`, so Go-based CLIs (`gh`, `gcloud`, `terraform`) fail TLS verification with `x509: OSStatus -26276` (`errSecInternal`); `git` uses Apple libcurl, LibreSSL and `/etc/ssl/cert.pem` and succeeds. On Linux, the bubblewrap sandbox denies the AF_UNIX keyring socket, so `gh` answers HTTP 401; `allowUnixSockets` cannot grant a path. Monitor and process visibility limits are in "Identity, delivery, and storage". On both platforms a Claude seat runs three commands outside the sandbox through the permission gate: `gh`, `git push`, and an authenticated `git fetch` (a private HTTPS remote, whose credential helper is `gh`); `excludedCommands` and `enableWeakerNetworkIsolation` are operator options, not selected alternatives. Look up a VERIFY item's external reference (upstream documentation, release notes, an API schema) with the WebFetch tool, not Bash `curl`. Three documented cases run outside the sandbox too: the task's main-checkout CompactionDB `memory add`, through the permission gate because that state directory is read-only from a worktree sandbox; writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox; and `agmsg-dispatch`, through `excludedCommands` (step 11). Every other out-of-sandbox action stays a blocked PONG. A Codex seat has in-sandbox network (T64) and never leaves its sandbox.
5. Write artifacts to the exact expected paths (a Claude seat writes them through the permission gate, step 4). Do not invent alternate paths. A seat whose sandbox cannot write the main checkout (a Codex seat) writes them at the same relative paths in its own worktree, untracked, and the RESULT says so; the orchestrator moves them into the main checkout by absolute path before review. Worker-side review evidence carries a `-worker-` infix (`<task>-worker-crit.json`, `<task>-worker-review-receipt.md`), so it never collides with the orchestrator's own files.
6. Put the verbatim output of every validation command in `expected_validation_file`; every identifier your report claims to have created must appear in that output.
7. Put the isolation status or fallback rationale in `expected_sandbox_file`.
8. Put reusable learning triage in `expected_learning_file`; do not promote rules directly unless the task explicitly allows it.
9. Put AutoSkill run status or a not-used record in `expected_autoskill_file`.
10. If blocked, still write the report and evidence paths that explain the blocker.
11. Reply with the requested `done_signal`, normally `AGMSG-RESULT v1`, and include all artifact paths. To a herdr-paned orchestrator, send RESULT and PONG with `agmsg-dispatch <team> <worker> <orchestrator> <pane_id>` (for example `wN:p1`; single-line, shell-safe text) rather than bare `send.sh`, so the wake starts the idle orchestrator's turn and its Stop hook delivers the message. The Claude sandbox manifest lists `agmsg-dispatch` in `claude.sandbox.excludedCommands`, so a Claude worker runs it outside the sandbox from the first attempt: no failed sandboxed run, no unsandboxed retry, and no escalation. Claude Code still applies its permission rules to excluded commands, so the managed settings allow `Bash(agmsg-dispatch:*)` (the only managed `permissions.allow` entry) and the dispatch runs without a prompt. A Codex seat runs under Codex's own sandbox, which this setting does not cover.
12. Put a `cost:` line in the report with observed session token/cost figures when the runtime exposes them, otherwise `cost: n/a`. This report value feeds the T76 `AGMSG-ACCEPTANCE v1` cost line.
13. A worker executing an AGMSG-TASK treats the Understand-Anything auto-update hook instruction ("knowledge graph is stale, you MUST update it") as out of scope unless `.ua/**` is in its `allowed_files`: it records "hook fired; not acted on" in the report and continues. The orchestrator never runs the graph update in its own session; graph refreshes are separate worker tasks.
14. Before sending RESULT, a worker whose session started a Crit plan review accounts for its Crit review server. A Claude seat starts one through Plan Mode's ExitPlanMode hook, and a Codex seat through the Crit plugin's Stop hook (`crit plan-hook --mode codex`). `make check-regime-boundary` treats a running `crit _serve` as a violation, and unit tests that read the host `pgrep` fail while one runs.
    - A worker cannot reliably stop the server itself (verified with crit v0.21.1 on a scratch `crit plan`). Inside the sandbox, `crit stop` always reports no running daemon. Outside it, `crit stop` stops the plan server only on the branch the server was started on, so it misses a server started before `git switch -c <task-branch>`, which is the common worker case. `crit stop <plan-file>` does not match a plan session on any branch. An unsandboxed `crit stop` is also not pre-approved.
    - A worker cannot inspect the host for the server either. Neither seat may leave its sandbox for host commands, because that would be an escalation, which step 4 forbids. For a Claude seat on macOS or Linux, the platform-specific process limits in "Identity, delivery, and storage" also apply here; no sandboxed host inspection is attempted.
    - So the worker, Claude or Codex, adds `plan-mode-used=<worktree>` to the RESULT and does nothing else about the server.
    - The orchestrator handles it as control-plane hygiene on the host. It runs these `pgrep`/`ps`/`kill` calls outside its own sandbox through the permission gate (`dangerouslyDisableSandbox`, answered by the operator or the auto-mode classifier) under its control-plane exemption, as it already does for `agmsg-dispatch` and `herdr-agents --audit`. It lists servers with `pgrep -fl _serve`, where a process named `crit` is a Crit server and the calling shell is listed under its own name. It reads each server's session record (`~/.crit/sessions/*.json` holds `pid`, `cwd` and `branch`) and confirms the server is live before acting: `ps -o args= -p <pid>` must show `crit _serve`, and the record's `cwd` must be that worker's worktree. The live process's own cwd must also match: `readlink /proc/<pid>/cwd` on Linux (`lsof -a -d cwd -p <pid> -Fn` on macOS) must equal the record's `cwd`. A mismatch means the pid was reused, and the record is stale. Only then does it stop the server with `kill <pid>`. A record whose pid is gone or runs another command is stale; it is removed, never killed. Never use `crit stop --all`, which stops every seat's server.
15. After the final push, wait for CI and the Codex Bot before sending RESULT. The Bot reviews at PR open and, after the one P0/P1 fix round, once more on `@codex review`; the review count is 1 + the fix rounds (plan 020 step 2).
    - Mark the PR ready for review with `gh pr ready <n>` before the first wait, while it is still a draft (`gh pr ready` exits non-zero on a PR that is already ready, so a later head's wait skips it): the Codex Bot reviews non-draft PRs, and a draft only on an explicit `@codex review` comment. When no Bot review of the final head arrives within 10 minutes, post `@codex review` on the PR and wait out the rest of the window.
    - Run `gh pr checks <pr> --watch` in the background and the Bot wait below at the same time: the 10-minute and 15-minute marks count from `gh pr ready` (from the push, for a later head), never from the end of CI. Right after a push GitHub can report no checks yet, and the watcher then exits 1 with `no checks reported`: start it once a check is listed, and restart it on that message instead of reading it as a CI failure. Wait for that watcher's exit status before the RESULT: a non-zero exit means no RESULT until CI passes.
    - Then list the Bot's reviews of the final head with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.login=="chatgpt-codex-connector[bot]" and .commit_id=="<head-sha>")|[.commit_id,.submitted_at]|@tsv'` and the Bot's top-level review comments raised on it with `gh api --paginate repos/{owner}/{repo}/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id == null and .user.login=="chatgpt-codex-connector[bot]" and .original_commit_id=="<head-sha>")|[.id,.original_commit_id,.path]|@tsv'`. A human comment, a CodeRabbit review or an earlier head's review never ends the wait. A comment's `commit_id` moves to the newest head, so findings are matched by `original_commit_id`. Repeat until a review of the final head appears or 15 minutes pass; the report records the latter as `bot: none`. The final head here is the diff head, the last commit that changes the PR's content: a head that only merges the new base with `gh pr update-branch` needs green CI but no new Bot wait. Both endpoints return 30 items per page by default, so keep `--paginate`.
    - This bounded wait is the permitted exception to the no-polling rule in "Regime activation and progress", which governs detecting worker completion and pane status, not a worker's wait on CI and the Bot. List at most every 30 seconds, stop at 15 minutes, and run the loop as a background command or a foreground command with a timeout. Never use bare foreground `sleep`.
    - A 👍 reaction alone is not evidence of a review.
    - Read each listed review's body too: the Codex Bot sometimes places a finding (a `P0`–`P3` badge with a blob link) in the review body instead of an inline thread. Such a review-body finding is listed alongside the top-level inline comments and fixed or dispositioned the same way.
    - Fix P0/P1 findings, inline or review-body, in at most one worker-side fix round before RESULT, then request `@codex review` and restart the wait from the push. A P0/P1 surviving that round is not fixed again: send `AGMSG-RESULT … bot_rounds=2` with each listed as `open:<thread id>` (`open:review-<review id>` for a review-body finding); this stops the PR for the operator's decision, and the next bullet's `fixed:`/`not-applicable:` rule does not override it.
    - Apart from those surviving P0/P1 items, the RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>` under Orchestrator Playbook step 10. The worker resolves no thread.

## Codex seat worklogs

Project layouts vary by language. Set up this worklog structure only when it
does not already exist, and use timestamped filenames in `YYYYMMDD_HHMMSS`
form:

- `.agents/worklog/codex/plan/<timestamp>_plan.md` stores the plan and design
  written before implementation. Ask the user questions when needed, and
  update the plan when questions, learning, or completed tasks change it. It
  must contain `Goal`, `Scope`, `Assumptions`, `Design`, `Tests`, and
  `Open Questions`.
- `.agents/worklog/codex/todo/<timestamp>_todo.md` derives its tasks from the
  plan. Move completed items from `TODO` to `Done`; when `TODO` is empty, set
  its status to `done` and rename it to `<timestamp>_done.md`. It must contain
  `TODO` and `Done`.
- `.agents/worklog/codex/learn/<timestamp>_learn.md` records only reusable,
  validated knowledge that speeds a future decision. State what was learned
  and where it applies, update the plan's `Assumptions`, `Design`, or `Tests`
  when relevant. A learn file must contain `Date`, `Learnings`, and
  `Plan Updates`.

Every plan, todo, and learn file starts with YAML frontmatter containing
`type` (`plan`, `todo`, or `learn`), `id` (`YYYYMMDD_HHMMSS`), `owner` (for
example, `codex-a`), and ISO8601 `created_at` and `updated_at`. Additionally:

- todo requires `status`, `workstream`, and `related_plan`; status is one of
  `active`, `blocked`, `done`, or `superseded`;
- plan requires `status`, one of `draft`, `active`, `done`, or `superseded`;
- learn requires `validated` (`true` or `false`) and `apply_to` (plan/tests),
  and may be created only when reusable and validated.

Optional frontmatter keys are `depends_on` (todo ID array), `blocked_reason`
for blocked work, `evidence` (path array), and `tags`.

## Pitfalls

- Do not start work from the agmsg message alone; read `task_file` first.
- Do not edit outside `allowed_files`, even for convenient cleanup.
- Do not perform forbidden actions such as dependency changes, gate changes, product changes, promotion decisions, image builds, or LLM calls when listed.
- Do not collapse candidate, promoted, rejected, and merged skill registry states into one directory.
- Do not put secrets, raw logs with credentials, or unredacted AutoSkill inputs in artifacts.
- Do not wake workers with `pane send-text` + `send-keys Enter`; use `agmsg-dispatch`, `poke.sh --body-file`, or `send.sh --body-file` as step 6 selects, and verify `read_at` in messages.db.
- Do not treat `AGMSG-ACCEPTANCE status=revise` as a new task unless it changes the task file or explicitly provides a next action.

exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
---
name: ponytail-review
description: >
  Quality review of a change: is the logic right, is it safe, does it hold
  under real load, is risky code tested, is it fast enough, and is every line
  needed. Reads the connected code, not only the diff. Each finding is
  explained in plain English. Use for "review this", "code review", "review
  the last commit", "review my PR", "is this over-engineered", /ponytail-review.
---

Review a change like the senior developer who will be paged when it breaks.
Order of importance: correct, safe, holds under load, tested, fast, lean.
Lean still matters: every extra line must be read, tested and fixed later.
This is a report the user asked for, so give it in full.

## 1. Understand first

- Review what the user names: uncommitted or staged changes, a branch, a PR
  link, or files. Nothing named: the uncommitted changes, or the last commit
  if there are none.
- Read the diff, then the code it touches: callers of every changed function,
  the functions it calls, the tests, the README.
- Trace the real flow: where data comes in, what is stored, what goes out.
- A change can break code it does not touch. When a signature, return value
  or behavior changes, grep every caller.
- Find the expected load in the repo (README, deploy config): one person
  running a script, or many users and processes at once. Judge scale against
  that, and say which load you assumed.

## 2. Look for

1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item,
   rounding, time zones), a caller broken by the change, a fix applied in one
   caller while the shared function stays broken.
2. **Risk:** security holes (injection, weak randomness, secrets, missing
   checks on input from users), data loss (errors swallowed, writes in the
   wrong order, no transaction).
3. **Scale:** fine for one user, wrong for many: check-then-write races, the
   same work done by every process, memory or lists that only grow, a query
   per item, O(n^2) on big input, per-process state that must be shared.
4. **Missing test:** risky new logic (a branch, a parser, money, security,
   data writes, a bug fix) with no test that fails when it breaks. One good
   test, not coverage.
5. **Speed:** big slowdowns are problems. Small wins (work repeated in a hot
   loop) are suggestions; some software counts every millisecond.
6. **Lean:** code that should not exist or should be smaller.
   - delete: dead code, unused options, speculative features
   - reuse: the repo already has this helper (name the path)
   - stdlib / native: the standard library or platform already does it; a
     new dependency for a few lines
   - yagni: abstraction with one implementation, config nobody sets
   - merge: near-copies that must change together
   - split: one function doing several unrelated jobs, so it is hard to read
     or test. Split by job, never by line count, and never into helpers that
     exist only to make a function shorter.

## 3. Check before you report

- Every finding needs a concrete case: "this input or situation leads to this
  wrong result". No case, no finding.
- Re-read the lines and confirm: the caller exists, the value can really be
  empty, the code really is unused.
- A shortcut marked with a `shortcut:` (or older `ponytail:`) comment that names its limit is a
  decision, not a finding, unless the expected load already crosses it.
- Propose the smallest fix that works. Prefer fixes that delete code. Never
  add layers, frameworks or config the problem does not need.
- No style taste, no "consider", no vague worries.

## 4. Output

Very simple English: short sentences, everyday words. Explain a technical
term the first time you use it. The reader may never have seen this code.

Start with `What this change does:` in two or three sentences.

Then the findings in three groups, skip empty groups:
- **Must fix:** bug, security, data loss, breaks at the expected load.
- **Should fix:** risky code without a test, real slowness, duplication, a
  function that mixes jobs, code that should not exist.
- **Nice to have:** small speed-ups, shorter forms.

Number findings across all groups, so the user can say "fix 2 and 5".
Every finding has all four parts, each one or two short sentences:

2. **Orders land on the wrong day** (`billing/close_day.py:L40-52`)
   - **What this is:** At midnight this job closes the day and bills all orders of that day.
   - **Problem:** It takes "today" from the server clock, which runs in UTC. An order placed
     at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day once in the shop's time zone:
     `datetime.now(ZoneInfo("Europe/Berlin")).date()`. One line, nothing else changes.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes them by hand.

End with:
- `Verdict: Ship.` or `Verdict: fix 1 and 3 first.`
- `Lean: -<N> lines possible.` when lean findings exist.
- `Not checked:` one line, if something mattered and you could not check it.

Nothing found: `What this change does:`, then `Looks good. Ship.` and one line
on what you checked.

Lists findings, changes no code.

exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
---
format: 2
task_id: dotfiles-T133-worker-write-boundary-a01
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - home/.chezmoitemplates/claude-worker-settings.json
  - home/.chezmoitemplates/claude-managed-settings.json
  - home/dot_claude-worker/modify_private_settings.json
  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
  - .claude/settings.json
  - scripts/generate-agent-configs.py
  - scripts/validate-agent-assets.py
  - Makefile
  - home/dot_local/bin/common/executable_herdr-agents
  - home/dot_local/bin/common/executable_herdr-agent-state.sh
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - .gitignore
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_validate_agent_assets.py
  - tests/unit/test_claude_settings_merge.py
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/unit/test_claude_worker_settings.py
  - tests/unit/test_claude_managed_settings.py
  - .orchestration/dotfiles-T133-worker-write-boundary-a01/**
after: []
threat_table:
  - control: "tests/unit/test_agmsg_orchestration_docs.py (amendment 1: only the assertion of the Worker Playbook step 4 sentence this task rewrites changes; PR #427 edits this file first and merges before this PR, which rebases onto it)"
    disposition: "residual: one assertion follows the rewritten sentence; the doc test module stays green in CI on the final head"
  - control: "home/dot_agents/agent-config.yaml (trusted checkout and interpreter bindings, static trusted_paths inventory, distinct worker policy, managed sandbox policy and worker caches)"
    disposition: "residual: the rendered policy reduces accidental and injected damage; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy checks both platforms without claiming same-UID isolation."
  - control: "home/.chezmoitemplates/claude-settings-managed.json (orchestrator user settings with failIfUnavailable true, onFailure block, hook PATH bindings and absolute uv/Python PermissionRequest invocation)"
    disposition: "residual: the user baseline preserves orchestrator functions within the managed sandbox policy; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the specified changes and retained settings; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision executes the rendered PermissionRequest under the system-only PATH and checks every rendered hook entrypoint."
  - control: "home/.chezmoitemplates/claude-worker-settings.json (static trusted-path and worktree-configuration Edit denies, empty user exclusions, restricted write allowances, native merge denials and minimal delivery hooks)"
    disposition: "residual: dedicated user settings reduce worker access to trusted paths; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the baseline and distinguishes it from shared managed exclusions and socket access."
  - control: "home/.chezmoitemplates/claude-managed-settings.json (admin-required sandbox enforcement, fixed rendered control-plane exclusions and Herdr socket allowance)"
    disposition: "residual: operator installation establishes the documented enforcement scope against project and local sandbox relaxation; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox asserts the rendered keys; shared control-plane capabilities and same-UID host access remain residual."
  - control: "home/dot_claude-worker/modify_private_settings.json (deployment of the dedicated worker baseline without importing orchestrator policy)"
    disposition: "residual: replacing the worker baseline's managed values reduces stale or permissive user configuration; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks repeated rendering in temporary homes."
  - control: "home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl (anchored launch-root guard for tracked and main-checkout local project hooks)"
    disposition: "residual: the guard reduces execution of worker-influenced project code and orchestrator hooks in worker sessions; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks fixed arguments, canonical identity and child status."
  - control: "formatter and project-map reload configuration-selection boundary (the edited file path in the hook tool input and its owning repository)"
    disposition: "residual: the guard skips these commands for input outside CLAUDE_PROJECT_DIR or in a worker repository under .claude/worktrees/, preventing consumption of worker-controlled Prettier JavaScript configuration and ruff settings; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks both the skip and normal anchored-file execution."
  - control: ".claude/settings.json (portable HOME-relative installed-guard commands with fixed operation identifiers, explicit HOME re-export, pinned system PATH and onFailure block)"
    disposition: "residual: guarded commands reduce worker-triggered project-hook execution while host-specific executable bindings remain in the per-host rendered guard and user settings; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure exhaustively traverses the hook entries and checks this split."
  - control: "scripts/generate-agent-configs.py (separate user and managed settings generation, static manifest deny inventory and absolute executable bindings)"
    disposition: "residual: rendering an explicit manifest list removes Git object traversal from inventory construction; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest checks exact manifest correspondence and filesystem coverage."
  - control: "scripts/validate-agent-assets.py (consolidated item 16: exact platform-symmetric excludedCommands at base lines 349-355; structural sanitized Claude PermissionRequest wiring at base lines 1193-1200; enumeration and preservation of the other managed Claude settings, hook-composition and sandbox checks)"
    disposition: "residual: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form covers the two exclusion fixtures; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate covers shlex parsing, the exact clean prefix, absolute uv and Python bindings, the fixed offline/no-cache uv arguments, the installed permgate script and sole claude argument, malformed or additional words and retained ccgate refusal; the Codex wiring check remains unchanged, and rendered-content validation does not establish live enforcement."
  - control: "Makefile (the install-managed-settings target that renders a home-directory staging file and prints the operator's sudo install command)"
    disposition: "residual: staging makes the administrative installation concrete without granting the worker administrative authority; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo checks the destination, rendered content, quoting and absence of privileged execution."
  - control: "home/dot_local/bin/common/executable_herdr-agents (worker pane environment, dedicated Claude configuration, private caches, worker user hooks and guarded main-checkout local hooks)"
    disposition: "residual: launch preparation reduces accidental inheritance of orchestrator settings and stale hooks (the legacy worktree-local file included: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks checks that migration against a fixture with a previously generated entry); tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches captures managed and standalone launches and repeated starts."
  - control: "home/dot_local/bin/common/executable_herdr-agent-state.sh (repository-owned Herdr state helper with an explicitly supplied absolute Python interpreter)"
    disposition: "residual: binding the helper and its Python child reduces shim execution; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters checks executed identities with planted shims."
  - control: "home/dot_agents/skills/agmsg-orchestration/SKILL.md (the governing Worker Playbook step 4 sentence)"
    disposition: "residual: the sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks its replacement; shared managed control-plane capabilities remain available and are not represented as per-seat isolation."
  - control: ".gitignore (the .uv-cache directory pattern)"
    disposition: "residual: ignoring the private cache reduces accidental cache publication; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
  - control: "tests/unit/test_generate_agent_configs.py (separate platform policies, static inventory, interpreter bindings, tracked hook coverage and item 16's literal-form PermissionRequest assertions)"
    disposition: "residual: render fixtures verify configuration and command construction; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_hooks_use_installed_permgate_paths and tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_claude_settings_use_interactive_profile_with_permgate cover the installed sanitized Claude hook with its bound uv/Python invocation and the synthetic renderer fixture respectively; they do not establish live enforcement or authenticate host-local inputs."
  - control: "tests/unit/test_validate_agent_assets.py (consolidated item 16: the macOS gh-exclusion and Linux extra-exclusion fixtures, valid_claude_sandbox's exact required exclusions, the literal-form hook fixture and the structural PermissionRequest cases)"
    disposition: "residual: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_accepts_manifest_symmetric_settings, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_rejects_each_broken_rule, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_requires_extra_codex_writable_roots, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs and tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs exercise the corrected shared sandbox fixture; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_hook_composition_requires_permgate_first and tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate cover the hook contract without claiming live enforcement."
  - control: "tests/unit/test_claude_settings_merge.py (orchestrator baseline preservation, failure-policy rendering through the existing merge and item 16's literal-form managed PermissionRequest fixtures)"
    disposition: "residual: temporary HOME fixtures verify baseline entries and identify runtime-added hooks separately; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_managed_permgate_replaces_stale_current_ccgate_hook, tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_permission_merge_preserves_unrelated_current_hooks and tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_permission_merge_preserves_custom_hook_in_mixed_entry retain stale-ccgate removal and custom-hook preservation with the specified managed hook; they do not install administrative settings."
  - control: "tests/unit/test_herdr_agents.py (every launch route, repeated starts, main-local and worker-user hook placement, the legacy worktree-local migration, descendants, caches and retained native denials)"
    disposition: "residual: fake launchers and subprocess markers verify effective arguments and executed fixture identities without starting live seats; shared managed exceptions remain explicitly outside per-seat exclusion claims."
  - control: "tests/unit/test_claude_worker_settings.py (dedicated settings deployment, static narrow denies, worktree configuration protection, project guard and hook failure configuration)"
    disposition: "residual: fixtures verify configured controls and credential-free deployment behavior; runtime permission checks and the remaining path-consumption window remain deployment and host residuals."
  - control: "tests/unit/test_claude_managed_settings.py (managed policy rendering, conflicting project and local settings fixtures, rendered-hook executable resolution, PermissionRequest execution and nonprivileged staging)"
    disposition: "residual: fixtures verify the selected documented enforcement keys and staging behavior; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision checks every rendered hook entrypoint and executes the real dependency-free permgate through bound uv/Python under PATH=/usr/bin:/bin, without simulating proof of Claude runtime enforcement or performing sudo installation."
  - control: ".orchestration/dotfiles-T133-worker-write-boundary-a01/** (this task's branch artifacts)"
    disposition: "residual: artifacts distinguish documentation facts, historical probes, final-head fixture results and unperformed operator deployment; acceptance compares their claims with the diff and CI."
  - control: "the task-file copy at .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md (amendment 1 text)"
    disposition: "residual: the first push deletes the a01 copy and adds the byte-identical dispatched a02 copy; TASK and RESULT carry the a02 copy's SHA256, which the orchestrator verifies at acceptance."
  - control: "the evidence records under .orchestration/dotfiles-T133-worker-write-boundary-a01/"
    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, outputs, statuses and tested revisions without credentials or unmasked home-directory paths."
  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    disposition: "residual: the orchestrator checks C1 to C10 and C7b, verifies dispatched bytes and binds integration evidence to the final head; P1-14 a05 and P1-6 implement retrieval of evidence of record from GitHub at its SHA; the GitHub boundary is detection, not prevention."
  - control: metadata separators
    disposition: "residual: the first document separators delimit format-2 metadata; the task-copy SHA256 binds the complete document."
  - control: in-process effects
    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, administrative installation, permission-policy mutation or operator-session restart."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: absolute interpreters, Python -I, sanitized Git, fixed hook PATH and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
  - control: new or renamed scripts
    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
  - control: "5.14 item 0: host threat model"
    disposition: "residual: host controls reduce accidental and injected damage without isolating seats sharing one OS user; prevention of worker-initiated merges requires a separate OS user or host under D-024-23's future P1-16, which the operator decides; the GitHub boundary is detection, not prevention, through P1-11's regime check in the next records PR for missing acceptance or gate evidence; shared managed control-plane exclusions and the Herdr socket remain residual."
  - control: "5.14 item 1: worker write controls"
    disposition: "residual: dedicated configuration, static symlink-aware Edit denies including worktree configuration and orchestrator worklogs and caches, narrow writable agmsg stores, managed sandbox enforcement and failIfUnavailable true reduce damage; documented path checks do not establish atomic immunity to concurrent path swaps."
  - control: "5.14 item 2: sanitized environment and private executable PATH"
    disposition: "residual: sanitized Git verification and absolute hook entrypoints reduce injected configuration, while PATH=/usr/bin:/bin binds upstream env-bash descendants away from shims; the remaining consuming-helper contracts belong to P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6."
  - control: "5.14 item 3: trusted-path checks"
    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
  - control: "5.14 item 4: verified executable and consumed-byte identity"
    disposition: "residual: hooks execute selected absolute entrypoints and trusted scripts, and upstream shell descendants inherit the fixed system PATH; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks; store-selected driver execution remains the separately named agmsg residual."
  - control: "5.14 item 5: output and reservation identity"
    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
  - control: "5.14 item 6: honest residuals, hooks and MCP"
    disposition: "residual: guarded tracked and main-local project hooks and minimal worker user hooks reduce host execution routes; shared managed Herdr socket access, control-plane exclusions, approved external processes and same-UID processes outside every seat sandbox remain residual."
  - control: "5.14 item 7: trusted-execution verification"
    disposition: "residual: this task records red-then-green render, merge, managed-policy, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
  - control: "5.14 item 8: committed approval ledger"
    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority; the GitHub boundary is detection, not prevention."
  - control: "5.14 item 9: private uv caches"
    disposition: "residual: per-seat worker caches, restricted worker write allowances and explicit denies on the orchestrator worklog and uv-cache reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
  - control: "5.14 item 10: no worker command outside the sandbox"
    disposition: "residual: empty worker user exclusions and disabled unsandboxed requests reduce escape routes; the worker rule forbids using shared managed control-plane exceptions, whose availability and Herdr socket access remain residual; the deterministic Codex permgate rule and live deployment remain operator steps."
  - control: "hook failure policy"
    disposition: "residual: every generated and tracked hook entry, including launcher-written worker user and main-local entries, carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
  - control: "agmsg store driver and plugin selection (team configuration drivers.partition, db/trusted-plugins authorization and installed storage.sh sourcing)"
    disposition: "residual: every seat writes the store, and installed storage.sh resolves drivers.partition as a driver path and sources it during unsandboxed delivery; it also uses db/trusted-plugins to authorize plugins/partition/shared.sh for sourcing; fixed PATH does not stop these routes; worker denies on plugins/** and db/trusted-plugins reduce the plugin route; dotfiles-T133-agmsg-hardening-a01 owns upstream basename validation, plugin authorization hardening and their adversarial red-then-green tests; this task introduces no store-derived sourcing beyond the installed scripts' current behavior."
  - control: orchestrator effect merge
    disposition: "residual: the worker is forbidden to merge; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub; shared credentials still permit worker-initiated API merges, so the GitHub boundary is detection, not prevention."
  - control: orchestrator effect update-branch
    disposition: "residual: the orchestrator owns branch updates and obtains fresh required CI, feedback, audit and security evidence for the resulting head."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain, and acceptance identifies any operator-authorized discarded state."
premises:
  - claim: >-
      The historical a05 premises carried by the preceding text describe its recorded observations. They do not require this worker to rebuild PR 400, edit the approval ledger or implement P1-14 a05.
    sources:
      - .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
    sources:
      - .orchestration/decisions.tsv
      - .orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      The existing Claude settings modify script merges the orchestrator user baseline into current settings and appends an attachment hook. The dedicated worker renderer does not import that orchestrator settings merge or its attachment behavior. The administrative managed-settings file is a separate deployment destination.
    sources:
      - home/dot_claude/modify_private_settings.json
      - home/.chezmoitemplates/claude-settings-managed.json
    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
  - claim: >-
      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
    sources:
      - home/dot_local/bin/common/executable_herdr-agents
      - home/dot_agents/agent-config.yaml
    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
  - claim: >-
      Linked-worktree Claude sessions load the main checkout's .claude/settings.local.json. The current launcher writes worker-local delivery hooks and merge denials into a different file. Worker delivery moves to the worker configuration directory's user settings, and the launcher's main-checkout local hooks receive the orchestrator-only guard.
    sources:
      - https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository
      - home/dot_local/bin/common/executable_herdr-agents
      - .claude/settings.local.json
    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks
  - claim: >-
      Managed sandbox.enabled true, failIfUnavailable true and allowUnsandboxedCommands false establish the documented admin-required enforcement scope. Project and local settings cannot supply sandbox relaxations in that scope. User settings and shared managed exceptions remain distinct from project and local settings.
    sources:
      - https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox
      - .orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
    verification: tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings
  - claim: >-
      Installed agmsg storage.sh resolves the writable team configuration's drivers.partition value as a driver path and sources it during delivery. The upstream hardening belongs to dotfiles-T133-agmsg-hardening-a01 and remains a residual of this task.
    sources:
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — INV-6 reset of a01 on tools/worker-write-boundary-a01, seat a010; plan 024 P1-15 under D-024-17, D-024-19, D-024-20, D-024-21 and D-024-23

## Goal

This is the amendment-4 text of the task dispatched at 2026-10-19T05:42Z (the ninth-round text that passed its pre-dispatch security review). Amendment 1 folds in two interpretation notes the worker needed (the inherited make format clause; the portable tracked `.claude/settings.json` with host-specific paths only in the rendered guard) and removes the Codex worker profile item (a Codex seat edits no Codex-boundary source; it becomes the separate Claude-seat task dotfiles-T133-codex-worker-network-a01). Everything else is the dispatched text in meaning; the branch, the eight green tests and the fixtures stay; the worker swaps the task copy to this text at its next push.

The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime detects missing acceptance or gate-passage evidence in the next records PR, not at main-push time, because the records reach main only with that boundary PR. On a PR touching `.orchestration/acceptance/**`, the regime job checks every main merge commit since the previous boundary for its corresponding acceptance record with gate-passage evidence and fails the PR when one is missing. P1-11 owns implementation of that check; this task states section 5.14 item 0's detection rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.

This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`.

The administrative managed policy is shared by every Claude seat. Its Herdr socket allowance and three control-plane exclusions remain available to workers as well as the orchestrator. Empty arrays in worker user settings do not subtract these managed entries. Their availability is a residual under item 0, and the worker execution rule supplies no authorization to use them outside the sandbox.

[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3. This Codex seat edits no Codex-boundary source.

The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10.

C-88: The following verbatim design sentences are normative for this task; the path is context only. The worker resolves `$HOME` when reading `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, and no tracked task text or task copy carries a literal operator home path, as required by the validator's home-path scan.

> 5.14 item 1: Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。 worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。 hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。 `failIfUnavailable: true` を全席に置く。

> 5.14 item 2: 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。

> 5.14 item 9: orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。 `UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。

> 5.14 item 10: worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。

D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.

The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. The retained mechanisms are documented symlink-aware deny rules, approval reads outside the local object database, hook interpreter bindings and runtime hook failure policy.

The fourth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md`. Its six P1 findings remain recorded. The retained mechanisms are the static manifest deny inventory, protection of the orchestrator worklog and cache, narrow home denies around writable agmsg stores, correct linked-worktree hook placement and fixed hook-runtime PATH.

The fifth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md`. Its three P1 findings remain recorded. This revision removes the gh credential-separation mechanism, records the upstream agmsg store-driver residual and moves sandbox enforcement into administrative managed settings.

The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks reduce redirection risk without establishing an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)

The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This historical observation confirms neither credential separation nor final-head deployment readiness.

The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated Claude configuration mechanism, directory-specific Claude credentials, symlink coverage and `onFailure: "block"` support. These Claude credentials do not separate gh Keychain access.

The settings documentation states, “In a worktree, it uses the file at the main checkout’s root.” Linked-worktree sessions therefore load the main checkout's `.claude/settings.local.json`. Worker hooks belong in `~/.claude-worker/settings.json`, and the main checkout's local hooks also receive the orchestrator-only guard. [Claude local settings reference](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository)

## Files

1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.

   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. Both user-settings renders use the same `claude.execution` bindings: resolve Python from `claude.execution.tool_paths.python3`, the trusted source behind `claude.execution.python`, and add the missing `claude.execution.tool_paths.uv` binding for the installed uv binary. Render their resolved absolute executable files, not PATH lookups or a private link whose creation depends on an earlier hook. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them. The manifest also supplies the trusted bindings from which the render resolves the absolute directories holding `ruff`, `prettier` and `terminal-browser`, without using mise shims.

   The manifest defines a separate Claude worker settings output at `home/.chezmoitemplates/claude-worker-settings.json` and an administrative managed-settings output at `home/.chezmoitemplates/claude-managed-settings.json`. The worker configuration directory is `~/.claude-worker`. The launcher passes its expanded absolute path as `CLAUDE_CONFIG_DIR`.

   A static `trusted_paths:` list names every protected top-level path of the anchored checkout and the protected home paths. It explicitly includes `<anchored-checkout>/.agents/worklog/**` and `<anchored-checkout>/.agents/worklog/uv-cache/**`. The `.claude` entries protect tracked contents and the main checkout's `.claude/settings.local.json` without denying the whole `.claude/worktrees/` tree. The list explicitly names directory targets and descendant patterns where both are required.

   Separate worker Edit denies protect `//<anchored-checkout>/.claude/worktrees/*/.claude/**` and `//<anchored-checkout>/.claude/worktrees/*/.mcp.json`. The `.claude` directory target is also protected. Ordinary worktree source files and the per-seat cache remain outside these configuration denies.

   The home-path denies are `~/.agents/agent-config.yaml`, `~/.agents/model-profiles.env`, `~/.agents/skills/**/scripts/**`, `~/.agents/skills/**/SKILL.md`, `~/.agents/skills/agmsg/plugins/**`, `~/.agents/skills/agmsg/db/trusted-plugins`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/bin/**`, `~/.local/share/**`, `~/.local/state/**`, `~/.local/share/mise/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. No blanket deny on `~/.agents/**` or `~/.local/**` replaces this list.

   The agmsg store paths `~/.agents/skills/agmsg/db`, `~/.agents/skills/agmsg/teams`, `~/.agents/skills/agmsg/run` and `~/.agents/skills/agmsg/ext-tools` remain writable. Deny patterns cover neither these directory targets nor their descendants except the file `~/.agents/skills/agmsg/db/trusted-plugins`. Edit denies merge into the sandbox configuration, so Bash writes to that file and `~/.agents/skills/agmsg/plugins/**` are refused too. Their influence on installed delivery-script driver and plugin selection remains the separately owned agmsg residual.

   The orchestrator retains its existing permissions, cache allowances and hook functions within the administrative managed policy. Its user baseline receives `failIfUnavailable: true`, `onFailure: "block"` on its hooks and the interpreter and PATH bindings below. Its exclusion entries match the three control-plane entries specified below; the former Linux `gh *` exclusion is removed.

   The worker user policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`. Shared managed entries remain effective despite these empty worker arrays.

   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.

   Existing model selections, Codex worker profile values, Codex sandbox and approval arguments and Codex shared Git grants retain their meaning and remain unchanged. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.

2. `scripts/generate-agent-configs.py` renders the distinct orchestrator user, worker user and administrative managed baselines from the manifest.

   The trusted-path deny inventory is rendered from the static `trusted_paths:` list. Rendering performs no Git object traversal, `git ls-tree` enumeration or tracked-path discovery. Worker-writable refs, replacement refs and objects do not determine the list.

   Anchored checkout rules use absolute `//` permission patterns. Rendering includes the explicitly listed trusted paths themselves and their descendants. It emits no checkout-wide parent deny that defeats ordinary worktree writes. The separate worktree-configuration denies remain present.

   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator creates no `executable_worker-write-boundary.py` or replacement PreToolUse path validator.

   Every direct Git verification introduced or changed by this task follows section 5.14 item 2. It begins with `env -i`, uses the selected absolute Git executable and an explicit `-C`, sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and supplies `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always`. Diff and show also use `--no-ext-diff --no-textconv` and `-c core.attributesFile=/dev/null -c core.sshCommand=false`.

   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Direct Python invocations use `-I`; PermissionRequest uses the fixed uv invocation in item 3. Hook execution uses the role-specific pinned PATH bindings specified below. The render test asserts that `ruff`, `prettier` and `terminal-browser` resolve under the rendered orchestrator tool PATH on the rendering host and that no entry of that PATH is a shims directory.

   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest` asserts that the rendered list equals the manifest entry after trusted anchor and home expansion. It explicitly asserts the rendered home-path deny patterns `~/.local/share/**` and `~/.local/state/**`, including the application code under `~/.local/share` used by `~/.local/bin` wrappers such as `terminal-browser`. It reads the filesystem of the test's own checkout and asserts that every tracked top-level source path is represented. It invokes no Git command to discover those paths.

   The inventory fixtures cover files, directories, `.claude` children, the main-local settings file, ordinary worktree writes, both worktree-configuration patterns, an anchor containing spaces and both explicit worklog patterns. Adding a top-level source path without a manifest entry makes the coverage assertion fail. Planted Git environment and replacement-ref fixtures leave rendering unchanged.

   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_leave_agmsg_stores_writable` asserts the rendered deny patterns `~/.agents/skills/agmsg/plugins/**` and `~/.agents/skills/agmsg/db/trusted-plugins` and verifies that the four store directories `db`, `teams`, `run` and `ext-tools` and their descendant fixtures remain writable except that one file.

3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator user baseline.

   The existing `home/dot_claude/modify_private_settings.json` continues to render the orchestrator's `~/.claude/settings.json`. That modify script is not imported into the dedicated worker renderer and remains outside `allowed_files`.

   This existing template's name does not make it administrative managed settings. The new `claude-managed-settings.json` template supplies that separate scope.

   The orchestrator retains its current user policy content apart from `failIfUnavailable: true`, `onFailure: "block"`, the required interpreter and PATH bindings and alignment of exclusions with the three control-plane entries. Worker-specific Edit denies and restricted worker cache allowances do not enter this baseline. Administrative sandbox requirements apply to the orchestrator as well as workers.

   Every generated hook entry carries `onFailure: "block"`. Every generated command hook starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before its trusted installed entrypoint, except that this chezmoi template renders PermissionRequest HOME as `HOME="{{ .chezmoi.homeDir }}"`. The prefix re-exports HOME before any HOME-relative entrypoint path. Host-specific interpreter, private-link-directory, anchored-checkout and tool-directory bindings remain in the per-host rendered user settings and guard. The formatter and project-map hooks run through the installed orchestrator-only guard and receive the role-specific pinned PATH specified below. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set without equating baseline coverage with coverage of runtime-added entries.

   The PermissionRequest command is `/usr/bin/env -i PATH=/usr/bin:/bin HOME="{{ .chezmoi.homeDir }}" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}" <abs uv> run --no-config --no-project --offline --no-cache --python <abs python> --script "{{ .chezmoi.homeDir }}/.local/bin/common/permgate" claude`. The template renders `<abs uv>` and `<abs python>` from the trusted manifest bindings in item 1, shell-quotes each complete path and bypasses permgate's shebang. Permgate has no PEP 723 dependency header and imports only the standard library, so `--offline --no-cache` requires no dependency download and uses no shared uv cache. Its existing `#!/usr/bin/env -S uv run --no-cache --script` shebang stays unchanged for interactive use. This bound invocation applies `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 items 2 and 9; that uncommitted design file is read-only context. Host-specific absolute paths rendered in this chezmoi template are permitted; the tracked `.claude/settings.json` remains portable.

   Every other rendered hook command, including SessionStart, Stop, delivery and guard invocations, likewise uses absolute bound entrypoints and interpreters and never relies on PATH to select uv, python3, bash or a tool; upstream agmsg env-bash descendants retain the fixed system-PATH binding in item 11.

   `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy` compares the merged policy with the preceding baseline and accounts for the specified changes. Repeated merging remains idempotent and preserves unrelated settings.

4. `home/.chezmoitemplates/claude-worker-settings.json` is the dedicated worker user baseline.

   It renders the static trusted-path Edit denies, the worktree `.claude` and `.mcp.json` Edit denies, retained native merge denials, empty user `excludedCommands`, `allowUnsandboxedCommands: false`, restricted `allowWrite`, no user Herdr socket allowance and `failIfUnavailable: true` for both Darwin and Linux.

   Its hooks are limited to agmsg delivery. It contains no formatter, project-map, permgate, orchestrator attachment, Herdr state or worker-write-boundary hook. Tracked project hooks and main-checkout local hooks still load and receive the guard described below.

   Every worker hook entry carries `onFailure: "block"`. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}" AGMSG_RESOLVE_PROJECT=0` before the selected absolute shell interpreter and absolute installed agmsg script path. The prefix also re-exports `AGMSG_STORAGE_PATH` when it is set in the launcher environment. Project resolution from a writable `run/proj.<pid>.project` marker remains disabled, so delivery retains the explicit worker path. Descendants inherit this PATH.

   The worker baseline does not copy the orchestrator's plugins, credential files or current hook arrays. Hook settings reload during a session, so protection is stated as current configuration rather than startup capture. `CLAUDE_CONFIG_DIR` selects the separate user settings directory while project settings continue to apply within the administrative enforcement scope. [Claude settings reference](https://code.claude.com/docs/en/settings)

   Worker user settings supply no additional socket or exclusion allowance. Their empty lists cannot remove the shared managed Herdr socket or control-plane exclusions.

5. `home/.chezmoitemplates/claude-managed-settings.json` supplies the administrative sandbox policy.

   The rendered policy sets `sandbox.enabled: true`, `sandbox.failIfUnavailable: true` and `sandbox.allowUnsandboxedCommands: false`. The last setting makes sandboxing admin-required. Project and local files cannot add sandbox exclusions, socket allowances or other documented relaxations in this scope. Managed Boolean values prevail over lower scopes. User settings remain a separate trusted scope, and arrays such as exclusions have no general managed-only lock. [Repository settings under an admin-required sandbox](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox)

   The rendered policy sets `sandbox.filesystem.disabled: false`, `sandbox.enableWeakerNestedSandbox: false`, `sandbox.enableWeakerNetworkIsolation: false`, `sandbox.network.allowAllUnixSockets: false`, `sandbox.network.allowLocalBinding: false` and `sandbox.allowAppleEvents: false`.

   The rendered `sandbox.excludedCommands` list contains exactly `agmsg-dispatch *`, `herdr-agents *` and `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These are the orchestrator's three control-plane entries. It contains no `gh *`, `git push *` or authenticated-fetch exemption.

   The rendered `sandbox.network.allowUnixSockets` list contains exactly the trusted home expansion of `~/.config/herdr/herdr.sock`. This allowance is shared by every seat under managed settings. Per-seat removal is unavailable in that scope, and the worker baseline's empty list does not revoke it.

   Shared control-plane exclusions are also available in worker sessions. The worker execution rule forbids using them to leave the sandbox. The text treats their availability and the socket's host-execution capability as item 0 residuals rather than enforced per-seat separation.

   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox` asserts the rendered content, exact exclusion and socket lists, trusted home expansion and every required Boolean value.

   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings` supplies project and local fixtures that disable sandboxing, disable startup failure, enable unsandboxed retries, add exclusions and sockets, enable weaker isolation and widen filesystem writes. The trusted managed render remains unchanged. The test verifies configuration scope and content without presenting a simulated settings merger as runtime enforcement.

6. `Makefile` adds only the `install-managed-settings` target and its `.PHONY` declaration.

   The target uses the repository's existing rendering facilities to render `home/.chezmoitemplates/claude-managed-settings.json` into `~/.claude/managed-settings.rendered.json`. The staging path is expanded to an absolute path under the user's home.

   The target selects `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux and prints the exact command `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` with the actual staging path and detected destination substituted and shell quoting preserved. The printed command is ready for the operator to run.

   The target performs no sudo call, administrative installation, live settings application, authentication or session restart. The staging file alone does not establish managed enforcement.

   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo` covers both macOS and Linux, uses a temporary home, verifies the staged JSON and exact printed command with the detected destination, includes a home path containing spaces and asserts that a planted sudo marker remains absent.

7. `home/dot_claude-worker/modify_private_settings.json` renders `~/.claude-worker/settings.json` from the dedicated baseline.

   The script follows the existing chezmoi modify-script interface: current content arrives on stdin and the desired settings object is written to stdout. It uses Python's standard library and the same trusted source and home resolution conventions as the existing renderer.

   Worker permissions, sandbox policy and hooks managed by this renderer replace stale managed values. Permissive old user exclusions, socket allowances, hook commands and shared cache allowances do not survive as additive worker user policy. The script does not read or copy `~/.claude/settings.json`.

   Rendering handles empty and malformed input through the repository's existing baseline behavior and is idempotent. It neither reads credentials nor initiates authentication.

   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently` exercises repeated deployment in temporary homes. `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks` plants orchestrator hook and plugin markers and verifies their absence.

8. `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` is installed as `~/.claude/hooks/orchestrator-only.sh`.

   Chezmoi renders the installed guard per host. Its rendered absolute shebang selects the trusted shell interpreter. The host-specific absolute interpreter paths, private executable-link directory, anchored checkout and tool directories are bound inside this rendered guard and the rendered user settings. The tracked project settings contain none of these paths.

   The guard compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Equality executes the fixed operation supplied by the caller through the guard's trusted interpreter and anchored-script bindings, subject to the formatter and project-map tool-input check below. Every other launch root exits 0 without executing it. `CLAUDE_PROJECT_DIR` supplies launch identity and never selects an executable.

   Worker launch roots, sibling worktrees and unrelated checkouts execute no guarded project code. Missing or unresolvable launch-root identity also executes no supplied command. Event cwd does not change the launch-root decision.

   The guard also binds the formatter and project-map reload to the edited file path from the hook's tool input and its owning repository. When the resolved path is outside canonical `CLAUDE_PROJECT_DIR` or belongs to a worker repository under `.claude/worktrees/`, the guard exits 0 without running the command. Worker-repository configuration, including Prettier JavaScript configuration and ruff settings, is never consumed by an orchestrator hook.

   The guard preserves argument boundaries, stdin and child exit status. It performs no eval, PATH interpreter lookup or worktree-relative script selection. Its portable caller starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`. The prefix re-exports `HOME` from the launcher environment as `HOME="$HOME"` before any path that uses it and explicitly re-exports the launch identity and the few variables Claude Code documents for hooks. No interpreter or anchored script path is supplied by the tracked settings.

   The pinned PATH differs by role. Worker-session hooks use `/usr/bin:/bin`. For the orchestrator's formatter and project-map hooks, which the guard runs only in orchestrator sessions, the guard itself sets PATH to a rendered list of absolute tool directories of the trusted root before executing the guarded command. Those directories hold `ruff`, `prettier` and `terminal-browser` and are resolved by the render from the manifest without using mise shims. The formatter and project-map scripts remain outside `allowed_files` and unchanged.

   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The positive-path case runs the complete rendered command in a subprocess with a fake `CLAUDE_PROJECT_DIR` equal to the anchored checkout and asserts that the guarded script executed while preserving its arguments and status. A second case runs the complete rendered command with a worktree `CLAUDE_PROJECT_DIR` and asserts that the guarded script did not execute. A planted `BASH_ENV` in the outer environment remains unexecuted in both cases. Formatter and project-map reload cases keep `CLAUDE_PROJECT_DIR` anchored and supply hook tool input for an outside file and a worker-repository file under `.claude/worktrees/`; both exit 0 with command and planted configuration markers absent. Matching anchored-file inputs run both commands normally. The guard tests execute the portable HOME-relative hook command against separately rendered per-host guards, assert the `HOME="$HOME"` re-export and verify that interpreter and anchor selection occurs only inside the rendered guard. Changing `CLAUDE_PROJECT_DIR` never changes the selected executable.

9. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.

   This tracked file is not a chezmoi template and remains portable across hosts. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`, and the clean environment re-exports the launcher's HOME before any path that uses it. The file names no interpreter, anchor path, private links directory or host-specific tool directory.

   Host-specific absolute bindings live only inside the per-host rendered guard and rendered user settings, including the orchestrator user template's bound PermissionRequest invocation. The guard binds the selected operation to its absolute interpreter and anchored script path. Contextdb commands do not invoke bare `python3` or select `.claude/hooks` from a worker checkout. The Stop gate does not invoke bare `bash` or a worker checkout's `scripts/agent-stop-gate.sh`. `CLAUDE_PROJECT_DIR` never selects an executable.

   Every hook entry carries `onFailure: "block"`. Existing event functions remain available to the anchored orchestrator. They are no-ops in worker sessions because the guard rejects their launch roots.

   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure` traverses every event, matcher and command entry. It rejects unguarded commands, missing failure policy, missing `/usr/bin/env -i` prefixes with the specified HOME re-export, interpreter or anchor paths in the tracked file and worker-selected executable paths. Render fixtures use distinct homes and anchors and assert that the tracked commands stay identical while the guard and worker settings receive their own host bindings.

10. `home/dot_local/bin/common/executable_herdr-agents` supplies the dedicated worker configuration at the actual worker launch boundary.

    Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. This value reaches the actual worker process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.

    Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a conflicting caller Claude configuration directory. This task introduces no worker gh configuration directory, gh templates or credential-separation claim.

    Every worker launch exports `UV_CACHE_DIR=<absolute-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<absolute-worktree>/.uv-cache/python`. Both worker kinds receive values derived from the selected canonical worktree. Caller-provided values do not replace them.

    The launcher stops writing Claude worker delivery hooks and merge denials into worktree-local `.claude/settings.local.json`. It renders the worker delivery hooks and native merge denials into `~/.claude-worker/settings.json`, the user-level settings file selected for that directory.

    Before every Claude worker start, the launcher also migrates the legacy worktree-local file. Claude Code loads the worktree's own `.claude/settings.local.json` alongside the main checkout's local settings, so a previously generated delivery entry there would stay effective with its unsanitized environment and PATH-resolved interpreter. The launcher removes every managed delivery hook entry it previously wrote from `<worktree>/.claude/settings.local.json`, keeps that file's unrelated entries, and refuses to start the worker while a command hook it did not write remains there, naming the entry. The effective hook set is asserted across the three files Claude Code loads for a linked worktree (worker user settings, the main checkout's local settings, the legacy worktree-local file) with a fixture holding a previously generated unsanitized entry: `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks` is red at the base and green on the final head.

    Before every Claude worker start, managed worker delivery entries are regenerated from trusted inputs. An existing delivery match does not skip preparation. Stale managed commands are replaced, unknown command hooks are not promoted into the trusted delivery set and the effective delivery set contains no duplicate managed invocation.

    The launcher also regenerates its managed hooks in the main checkout's `.claude/settings.local.json`. Every local agmsg delivery and orchestrator attachment command that it writes runs through the installed orchestrator-only guard. The existing permissions object and unrelated non-hook settings remain stored. Their effective sandbox interpretation follows the administrative managed policy.

    Every command hook in both `~/.claude-worker/settings.json` and the main checkout's `.claude/settings.local.json` starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"`. Worker user settings contain their per-host rendered absolute interpreter and script bindings. Main-local commands invoke `"$HOME/.claude/hooks/orchestrator-only.sh"` with fixed operation identifiers, leaving host-specific executable bindings inside the rendered guard. The prefix removes inherited `BASH_ENV` before Bash starts and explicitly re-exports the launch identity and documented hook variables. Agmsg delivery prefixes additionally re-export `AGMSG_RESOLVE_PROJECT=0` and `AGMSG_STORAGE_PATH` when the latter is set in the launcher environment, so the clean environment does not re-enable project resolution from the writable `run/proj.<pid>.project` marker. Every entry carries `onFailure: "block"`. Main-local hooks loaded by a worker session execute no guarded payload.

    Worker settings retain existing native merge denials. They add no user excluded commands, Herdr socket allowance, unsandboxed requests or orchestrator hooks. Shared managed exclusions and socket access remain effective.

    Codex launches retain their existing `--sandbox workspace-write` and `--ask-for-approval never` arguments unchanged. This task changes no Codex worker profile or network-policy source and adds no network-policy test.

    The retained Codex Git grant permits shared `.git/objects`, `.git/refs`, `.git/logs` and the worker's administration directory. It does not authenticate local ledger content and is not represented as a host security boundary.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches` covers both worker kinds and all launch routes. `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_repeated_worker_start_replaces_stale_managed_hooks` covers repeated preparation.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_launch_adds_no_unsandboxed_route` checks that worker launch construction adds no outside-sandbox command route, worker user exclusions or socket allowances and retains native merge denials. It separately records the shared managed exceptions and does not claim that empty user arrays remove them.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks` asserts that worker hooks are written to worker user settings, worker preparation writes no worktree-local settings file and main-local agmsg and attachment hooks execute no payload under a worker launch root. An anchored orchestrator invocation still reaches the expected fixture payloads.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_settings_hook_has_system_path_prefix` exhaustively traverses both settings files after initial preparation and repeated starts. It asserts the literal `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix on every command hook, checks the split between absolute bindings in rendered worker settings and HOME-relative main-local guard calls, and asserts that a planted `BASH_ENV` in the hook's inherited environment does not run. The planted-`BASH_ENV` case is red against the current PATH-only form. The test also asserts `AGMSG_RESOLVE_PROJECT=0` in every agmsg delivery prefix and preservation of `AGMSG_STORAGE_PATH` when set in the launcher environment. It invokes the delivery resolver through the rendered prefix with an explicit worker path and a conflicting writable `run/proj.<pid>.project` marker and asserts that the resolver retains the explicit worker path.

11. `home/dot_local/bin/common/executable_herdr-agent-state.sh` provides the repository-owned Herdr state helper installed as `~/.local/bin/common/herdr-agent-state.sh`.

    The currently installed `~/.claude/hooks/herdr-agent-state.sh` is generated by Herdr and is not a tracked source in this repository. Its bare `python3` descendant is not retained as a trusted worker hook. The repository-owned helper preserves the required state-reporting function and receives its absolute Python interpreter through the rendered invocation.

    Every hook command reaches a selected absolute interpreter and absolute script path through trusted installed bindings. The tracked settings name only the HOME-relative guard and fixed operation identifiers. Host-specific interpreter and anchor bindings reside inside the per-host rendered guard or rendered user settings. Repository-owned shell descendants use absolute shebangs or explicit absolute shell invocations. Direct Python descendants use the selected absolute interpreter with `-I`; PermissionRequest uses the bound uv/Python invocation in item 3.

    Upstream agmsg scripts retain their `/usr/bin/env bash` shebangs and direct calls to other installed agmsg scripts. The `PATH=/usr/bin:/bin` supplied by the delivery hook's `/usr/bin/env -i` prefix propagates to those descendants, so their Bash resolution uses the system directories without reaching host shims. The installed upstream files are neither edited nor vendored.

    The delivery inventory names `~/.agents/skills/agmsg/scripts/session-start.sh`, `~/.agents/skills/agmsg/scripts/session-end.sh`, `~/.agents/skills/agmsg/scripts/check-inbox.sh`, `~/.agents/skills/agmsg/scripts/identities.sh` and every additional delivery descendant actually reached.

    The inventory records source ownership, installed path, caller, entrypoint interpreter and inherited PATH for each reached script. Binding only the first command does not establish descendant coverage.

    The inventory separately records the current `storage.sh` route from writable team configuration to driver sourcing. A `drivers.partition` value such as `../../../db/payload` can select a planted driver file during unsandboxed delivery. Fixed PATH does not mitigate that selection. The upstream fix belongs to `dotfiles-T133-agmsg-hardening-a01` as recorded in the acceptance record's ownership section.

    No worker hook added by this task introduces store-derived driver sourcing beyond the behavior of the currently installed agmsg scripts. This task neither implements nor claims the upstream validation.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters` executes the fixture hook routes with planted Python and Bash shims. It includes a directly executed descendant with an `/usr/bin/env bash` shebang, checks descendant markers and records actual interpreter identities and inherited PATH. Capturing launcher command strings alone does not satisfy this test. Its result does not close the store-driver residual.

12. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the Worker Playbook step 4 sentence that lists outside-sandbox worker commands.

    The replacement sentence is: “Every worker command, including gh, git push and authenticated git fetch, runs inside the worker's sandbox; no worker command runs outside it.”

    This sentence governs worker execution. Historical TLS, keyring, artifact-writing and delivery exceptions elsewhere in the playbook provide no authorization to leave the sandbox. Shared managed control-plane exceptions provide no worker authorization either. An unavailable operation produces a blocked PONG with its exact command and boundary.

    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox` checks the replacement and removal of the former three-command exception sentence.

13. `.gitignore` adds only `.uv-cache/`.

    Section 5.14 item 9 fixes trusted orchestrator consumers to `UV_CACHE_DIR=<anchored-checkout>/.agents/worklog/uv-cache`, places managed Python installations beneath that cache and uses `--offline`. Those consumers execute no dependency content from worker caches, shared uv caches or mise caches. Their owning hardening tasks implement the consumer changes.

    This task's static deny inventory explicitly protects both `.agents/worklog/**` and `.agents/worklog/uv-cache/**` beneath the anchored checkout. Their gitignored status does not remove them from the inventory.

    This task's hooks use standard-library Python and absolute shell interpreters; PermissionRequest alone invokes the existing dependency-free permgate through the absolute uv/Python binding with `--offline --no-cache` specified in item 3. The existing `.agents/worklog/` ignore covers the orchestrator cache.

14. The five allowed test modules reuse existing render, merge, fake-launcher and temporary-HOME fixtures.

    Tests are written before implementation and retain identified base-failure and implementation-success evidence. A missing new entrypoint supplies its baseline failure.

    Worker settings tests cover both platforms, exact static manifest correspondence, current-checkout filesystem coverage, every protected path category, directory targets, descendants, both worklog patterns, ordinary worktree writes, the worktree `.claude` and `.mcp.json` denies, writable agmsg stores, stale settings and the absence of the removed boundary hook.

    Managed settings tests cover the exact rendered policy, conflicting project and local sandbox relaxations, shared control-plane exclusions, shared Herdr socket access and staging without privileged execution. They distinguish worker user settings from the effective shared policy.

    Path fixtures cover symlink components and filesystem case aliases. They verify inventory and configuration identities without presenting a simulated permission matcher as proof of Claude runtime enforcement.

    Hook tests cover every generated and tracked entry's failure policy, worker user settings, guarded main-local settings, the `/usr/bin/env -i` prefix with explicit hook-variable re-exports, complete rendered-command positive and worktree-negative cases, role-specific pinned PATH bindings, suppression of a planted inherited `BASH_ENV` and actual descendant execution. They distinguish synchronous policy hooks from background delivery and post-action events.

    `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision` renders the complete orchestrator and worker user hook sets and the guard in a temporary HOME, reusing the tracked and launcher-generated hook fixtures for SessionStart, Stop and delivery. For every command hook, expand only the fixture's known HOME and hook-variable bindings, parse with `shlex`, and assert that the first word is an absolute path to an existing executable file; for `/usr/bin/env -i`, also assert the first word after all environment assignments is such a file. Check the guard's rendered shebang, interpreter and fixed-operation executable bindings too, so no bare uv, python3, bash or tool survives. In the same test, install the unchanged real permgate source and a minimal deterministic fixture policy beneath that temporary HOME, then execute the rendered PermissionRequest command with the actual bound uv and Python binaries, outer `PATH=/usr/bin:/bin` and a fake PermissionRequest payload matching the fixture policy. Assert exit 0, parse stdout and assert `hookSpecificOutput.hookEventName == "PermissionRequest"` and the expected `hookSpecificOutput.decision.behavior`; empty stdout, exit 127 or `env: uv: No such file or directory` fails. A fake uv or permgate that merely prints a decision does not satisfy this test. Record red-then-green evidence for this selector.

    `onFailure: "block"` requires Claude Code v2.1.295 or later and has no enforcement effect on background hooks or the documented excluded events. [Claude hook failure reference](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)

    Tests create no identities, initiate no login and access no real credential store. No fixture result is represented as proof of credential isolation, live managed enforcement or upstream agmsg hardening.

15. `.orchestration/dotfiles-T133-worker-write-boundary-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence.

    The report maps each of the third C-80 review's five findings, fourth C-80 review's six findings and fifth C-80 review's three findings to the revised mechanism, its tests and its remaining residual or owning task. It distinguishes policy configuration from live enforcement and deployment.

16. `scripts/validate-agent-assets.py` is the consolidated validator scope for every existing check affected by this task's rendered Claude settings, hooks, sandbox and exclusions, with their corresponding fixtures and assertions.

    The Linux and macOS `excludedCommands` checks at base lines 349-355 become one exact ordered-list check on both platforms: `agmsg-dispatch *`, `herdr-agents *`, `{{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *`. The last entry becomes `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *` after chezmoi expansion. Neither platform permits `gh *` or an additional, missing, reordered or substituted exclusion. The existing non-empty-string list validation remains. This follows the normative design sentences quoted above from `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 (C-86, C-88); the path is context only.

    The Claude managed-user-settings hook-wiring check in `validate_model_profile_assets` at base lines 1193-1200 becomes structural. Inspect command hooks under `hooks.PermissionRequest`, not serialized text from other events, and parse the command with `shlex` without executing it. Require exactly the sanitized prefix from item 3 with HOME equal to the absolute home rendered from `{{ .chezmoi.homeDir }}`, followed in order by an absolute uv path whose basename is `uv`, `run`, `--no-config`, `--no-project`, `--offline`, `--no-cache`, `--python`, an absolute Python path matching the trusted rendered interpreter binding, `--script`, the absolute installed permgate path whose basename is `permgate`, and `claude`, with no further words. The uv and permgate paths also match their trusted rendered bindings. Compare parsed words so quoting of a bound path containing spaces is preserved; do not require a literal `permgate claude` substring. Missing or malformed commands, an incomplete or altered prefix, an extra environment assignment, relative or substituted executable paths, missing, reordered or additional uv flags, a different script or argument, a direct shebang-based permgate call, a guard selector, and trailing words or shell operations fail. The generated PermissionRequest command and its assertions conform to this bound-interpreter contract; the worker's current `orchestrator-only.sh permgate` selector does not satisfy it. Parsed tokens establish command structure; the render/runtime test in item 14 establishes that the executable binding actually runs under the sanitized PATH. The existing refusal of `ccgate` anywhere in the Claude hooks remains. The Codex PermissionRequest and `permgate codex` check at base lines 1189-1190, and its ccgate refusal, are unchanged because this task changes no Codex hook design.

    The complete inventory of the surrounding checks is retained: `validate_claude_settings` still checks the schema, interactive model and effort, absence of the redundant model suffix and legacy type checker, the `format-edited-files.py` operation marker (still present in the guarded command), permission-allow list shape, sandbox policy, disabled unmanaged plugins and the Crit rule. `validate_claude_sandbox` still requires enabled and auto-allow booleans, a Boolean `failIfUnavailable` (the render tests separately require true), all agmsg and Codex writable roots, valid extra write paths, allowed hostname and telemetry restrictions, the platform Mach-service allowlist, no allow-all Unix sockets and valid socket paths; only its exclusion policy changes. `validate_hook_composition` retains duplicate-command rejection, permgate-first ordering, synchronous timeout budgets and the SessionStart `herdr-agent-state.sh` marker and order. These markers remain in the rendered commands, so none is deleted or weakened to accommodate the prefix. Generated-output freshness, manifest home-path checks, tracked project-settings portability, permgate policy and profile-asset checks and the orchestration home-path/secret scan remain unchanged. New worker-user and administrative-managed-policy outputs retain their exact content checks in the already named render tests; the orchestrator user sandbox validator is not applied to worker empty exclusions.

    In `tests/unit/test_validate_agent_assets.py`, the two already authorized cases in `ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form` remain in scope: macOS gh exclusion and Linux extra exclusion. The shared `ValidateAgentAssetsTest::valid_claude_sandbox` fixture gains the exact three-entry exclusions above. Its callers `test_claude_sandbox_accepts_manifest_symmetric_settings`, `test_claude_sandbox_rejects_each_broken_rule`, `test_claude_sandbox_requires_extra_codex_writable_roots`, `test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs` and `test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs` retain their checks and reach the rule each intends to test. The literal-form fixture in `test_hook_composition_requires_permgate_first` follows the sanitized hook while retaining its ordering failure. Add `ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate` with valid quoted-path cases and negative cases for the structural contract and retained ccgate refusal. Keep red-then-green evidence and run `uv run python -m unittest tests.unit.test_validate_agent_assets -v` to green on the final head.

    The other tests carrying the literal hook form are `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_hooks_use_installed_permgate_paths`, `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_claude_settings_use_interactive_profile_with_permgate`, `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_managed_permgate_replaces_stale_current_ccgate_hook`, `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_permission_merge_preserves_unrelated_current_hooks` and `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_permission_merge_preserves_custom_hook_in_mixed_entry`. Their hook fixtures and assertions are in scope together: production-hook expectations use the parsed prefix, bound absolute uv/Python invocation with the fixed flags, installed permgate script and sole `claude` argument; synthetic renderer and merge-only inputs may remain synthetic where they assert no production command form. Preserve their model, stale-ccgate-removal and custom-hook-preservation assertions and the unchanged Codex assertion. No validator pin or literal-form fixture named here is left outside scope.

The source measurement is 674 changed lines against the unchanged 700-line cap, guard included, and the test measurement is 905 changed lines against the unchanged 950-line cap (the worker's 2026-10-19T08:21:22Z evidence at local head 55c125a1 on main 69dccca9). The valid_claude_sandbox fixture adds about 10 changed test lines, giving about 915; the new `test_rendered_hooks_bind_executables_and_permgate_returns_decision` contributes its measured changed-line count on top (`905 + about 10 + new render/runtime-test lines`), before the remaining structural-hook checks and literal-form fixture/assertion adjustments. The unchanged test cap leaves about 35 lines for that test and all remaining test changes together; those changes must fit the remaining source and test margins, and the worker re-measures the final diff rather than presenting this estimate as a final-head result. No test-cap increase is asserted without a measured sum requiring it.

The guard source is `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl`: chezmoi renders the guard from its .tmpl source with the per-host absolute interpreter, anchored-checkout and tool-directory paths at apply time (a plain `executable_` source would be copied without expansion), and the render test renders the template with the test host values and asserts the paths it contains.

The doc test `tests/unit/test_agmsg_orchestration_docs.py` asserts the exact step 4 sentence this task rewrites (lines 200-201 at the base); the assertion follows the new sentence, nothing else in that module changes; PR #427 (P1-8) edits the same module and merges before this pull request, which rebases onto it before its first push.

## Out of scope

The Codex worker profile change `sandbox_workspace_write.network_access=true` belongs to the separate task `dotfiles-T133-codex-worker-network-a01` for a Claude seat. This task contains no implementation, threat row or test for that change. This Codex seat edits no Codex-boundary source. The operator step for the deterministic Codex permgate policy remains named below.

The worker-write-boundary Python hook, its hook entries and `tests/unit/test_worker_write_boundary.py` are dropped. The gh-trusted wrapper remains dropped. The worker gh configuration directory, its templates and the dedicated-identity implementation are removed from this task.

D-024-23 establishes that `GH_CONFIG_DIR` does not separate same-macOS-user Keychain access. A separate OS user or host is required for prevention of worker-initiated merges. Future P1-16 remains the operator's decision. This task implements no credential-separation substitute.

The permission guard and merge gate remain P1-14 a05's work. P1-14 a05 and P1-6 implement the regime rule that approvals and gate evidence of record come from GitHub at a SHA through its API inside the sandbox. The GitHub boundary is detection, not prevention.

For the committed approval ledger, the regime obtains the commit SHA returned by `git ls-remote origin refs/heads/main` and reads `gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. The consuming implementation reads the API response's file content at that exact SHA. It does not fall back to local files, local refs or local object traversal.

A working-copy decision remains a proposal until its record PR reaches main. This task writes no approval row and implements no local-object substitute for GitHub authority. Shared credentials can still authorize a worker-initiated merge. P1-11 owns the next-records-PR regime check for missing acceptance or gate evidence under section 5.14 item 0's detection rule.

The upstream agmsg driver-selection fix belongs to `dotfiles-T133-agmsg-hardening-a01`. Its recorded scope validates the `drivers.partition` driver name as an allowlisted basename without path separators before sourcing and supplies an adversarial red-then-green test. This task leaves the shared stores writable and records the current sourcing route as a residual. The ownership section identifies that upstream task as a task to be written; this text does not claim that its fix or test exists.

Permgate code and deterministic policy remain the operator's responsibility. The worker prepares the operator step that stops the Codex permgate policy from approving sandbox escapes. The worker performs no live policy edit or escape probe.

The operator logs into Claude once with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected. The Claude Keychain entry is keyed to that directory. This Claude login does not authenticate or isolate gh.

Administrative installation of `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux is the operator's step. The worker implements rendering, staging and the printed installation command without running sudo or installing live managed settings.

The documented file-tool checks reduce symlink redirection risk. A same-UID process can race filesystem changes, alter host-local state or execute outside a seat sandbox. The remaining interval between permission checks and path consumption is a residual under section 5.14 item 0. This text makes no claim that the worker could already write every redirected target directly.

The managed Herdr socket allowance stays available to every seat. Per-seat socket removal is unavailable in that shared scope. Shared control-plane exclusions, socket RPC, hooks, approved MCP processes and other processes outside every seat sandbox retain their stated host trust. The configuration is not represented as same-UID adversarial isolation.

`onFailure: "block"` supplies runtime failure behavior where Claude supports it. Python exit-status tests do not establish timeout handling by the runtime. Background hooks and events on which the field has no effect perform no security enforcement in this design.

Consuming-helper snapshots, reservation locks, the common trusted-execution test helper and orchestrator review-worktree relocation remain with their owning hardening tasks. Codex writable-root grants remain unchanged.

In `scripts/validate-agent-assets.py`, the consolidated policy-check changes enumerated in item 16 are in scope; unrelated validator behavior remains out of scope. In `tests/unit/test_validate_agent_assets.py`, the two exclusion cases, `valid_claude_sandbox`, the named hook fixture and structural-hook cases in item 16 are in scope; unrelated tests remain out of scope. The named literal-form assertions and fixtures in the already allowed generator and merge test modules are included as item 16 specifies.

The worker edits neither `.orchestration/decisions.tsv` nor other tasks' canonical texts, evidence or acceptance records, apart from the explicitly named deletion of the predecessor's task-file copy. It performs no authentication change, keyring mutation, ruleset mutation, administrative installation, live settings application, global installation, operator restart or merge.

## Check

`make render-check` and `make validate-agent-assets` pass. The task's own files pass the `make format` flags: `shfmt -i 4 -sr --diff`, `ruff format --config ruff.toml --check` and `prettier --check`.

The clean base `205fe85c` has an inherited formatting failure on 12 out-of-scope files: ten archived task shell sources, `project-map-reload.sh` and `brew.bats`. The inherited failure is reproduced against that unchanged base and disclosed in `validation.md` with its exact output and per-file exit statuses. This clause authorizes no out-of-scope repair.

Shellcheck and shfmt cover the changed shell sources, including the launcher, orchestrator-only guard and repository-owned Herdr state helper. Added or changed shell comments use English shdoc-compatible annotations. Changed Python receives the repository's Python formatting and lint checks.

`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` is green. The validation record contains every named red-then-green selector and the complete final module run.

The final diff has at most 700 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`. It has at most 950 changed lines under `tests/`. Changed lines are additions plus deletions. The validation record includes per-file numstat, base and head identities and both totals.

The validation record contains exact commands, verbatim outputs, exit statuses and tested identities. Git commands producing that evidence follow section 5.14 item 2.

Both platform renders show separate worker and orchestrator user settings, exact manifest deny-inventory correspondence, filesystem coverage of current tracked top-level source paths, both worklog denies, ordinary worktree writes, the worktree `.claude` and `.mcp.json` denies, narrow home denies, writable agmsg stores, empty worker user exclusions, restricted worker writes and `failIfUnavailable: true` for every Claude seat.

Managed render evidence asserts sandbox enablement, startup failure, disabled unsandboxed retries, the required anti-weakening Boolean values, exactly the three rendered control-plane exclusions and exactly the Herdr socket allowance. Conflicting project and local fixtures leave that render unchanged. The evidence names the documented enforcement scope without claiming live runtime verification.

Staging evidence shows the home-directory output and exact printed `sudo install -m 0644` command with the detected administrative destination on both macOS and Linux. The temporary-HOME test proves that the target executes no sudo command.

Hook evidence inventories every generated and tracked entry, its `onFailure` value, `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix (with template-rendered absolute HOME for PermissionRequest), installed script, absolute entrypoint interpreter and reached descendants. It includes the new render/runtime selector's actual exit status and parsed permgate decision under `PATH=/usr/bin:/bin`, plus first-word and post-env-assignment executable checks for every rendered hook command. It states the portable tracked-command and per-host-rendered-binding split, verifies HOME re-export before HOME-relative paths and shows that tracked commands name no interpreter or anchor path. It includes worker user settings and main-checkout local settings. Render evidence shows that `ruff`, `prettier` and `terminal-browser` resolve under the guard's rendered orchestrator tool PATH on the rendering host and that no PATH entry is a shims directory. Merged-settings evidence identifies runtime-added entries separately. No report claims complete effective failure-policy coverage from template inspection alone.

Launch evidence shows both cache variables reaching the actual worker process on every route. Claude processes additionally receive the dedicated Claude configuration directory. Repeated-start evidence shows replacement of stale managed hooks, retained native merge denials and the unchanged Codex sandbox and approval arguments.

Linked-worktree evidence shows worker hooks in the worker configuration directory's user settings and no new worker-local `.claude/settings.local.json`. Guard markers show that the main checkout's local agmsg and attachment hooks execute no payload under worker launch roots.

Guard markers also show that worker project scripts, contextdb hooks, Stop gates and formatter payloads do not execute through tracked hooks. Descendant markers show that planted PATH interpreters do not execute on the tested hook routes, including an upstream-style `/usr/bin/env bash` descendant.

The report separately identifies the writable agmsg store's current driver-selection route and `dotfiles-T133-agmsg-hardening-a01` ownership. Hook interpreter tests do not claim to close that residual.

The report states the GitHub API ledger rule without claiming this task implements the permission guard or the P1-11 next-records-PR regime check. It states detection, not prevention, and records D-024-23's future P1-16 decision. It also records shared managed exclusions and Herdr socket access, same-UID credential access, path-consumption residuals, external-process trust, hook-event failure limitations and the retained Codex shared Git grant.

No local Bats tests run. Required Bats results come from GitHub Actions. Failed required checks retain their actual output and receive an in-scope fix before RESULT.

The orchestrator runs `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md` before dispatch and at acceptance. C1 to C10 and C7b pass.

A C-80 security-profile context reviews this complete revised text before dispatch. That review is a dispatch prerequisite and is not claimed as a result of this draft.

## Completion

One implementation PR continues the existing branch `tools/worker-write-boundary-a01`, created from clean base `205fe85c`, on the Codex seat a010. The eight green tests, fixtures and evidence stay. The first push deletes the predecessor copy `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md` and adds the byte-identical dispatched a02 task at `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md`. This predecessor-copy deletion is the sole authorized edit to the predecessor's artifact directory.

The Completion clauses of `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` apply with this task's branch, files and evidence paths, `dotfiles-T133-worker-write-boundary-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md>` in RESULT. The a05-specific continuation of PR #420, predecessor-copy deletion, inherited counters, deadline and implementation requirements do not transfer. The orchestrator writes the follow-up owner task before assigning its first advisory P2.

Every worker-side fix round counts toward INV-6. The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no additional private correction-and-review cycle to avoid reporting it.

No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition, and surviving P0/P1 findings remain open for the operator's decision.

Every gh write and every git write runs as a separate command without shell chaining. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG with the exact command and boundary.

The Codex worker writes evidence at the required relative paths in its own worktree and says so in RESULT. Worker review evidence uses the `-worker-` infix. Crit-data evidence and its receipt follow repository rules without a browser review or human review request. The orchestrator copies evidence by absolute path before acceptance.

`AGMSG-RESULT v1` names the final head, base, branch, changed files, new deployable scripts, source and installed paths, trusted anchor, interpreter and descendant inventory, hook PATH bindings, user and administrative settings destinations, staging path and printed installation command, Bot findings and proposed dispositions, open P0/P1 findings, exact test selectors, measured caps, task-copy SHA256 and evidence paths. It distinguishes historical observations from final-head results and names all pending operator steps.

The report states the user-visible effects. Claude workers use `~/.claude-worker` and require its own Claude login. Worker trusted-path and worktree-configuration Edit denies also affect Bash sandbox writes. Agmsg store paths remain writable except `~/.agents/skills/agmsg/db/trusted-plugins`, and worker denies also cover `~/.agents/skills/agmsg/plugins/**`. Worker user settings add no excluded commands or Herdr socket allowance, while shared managed settings retain the three control-plane exclusions and Herdr socket for every seat. Tracked and main-local orchestrator project hooks are no-ops in worker sessions. Worker caches are private. Every Claude seat fails when its sandbox is unavailable.

Administrative managed settings require sandboxing for the orchestrator as well as workers and disable unsandboxed retries. The former Linux gh exemption is removed. The orchestrator retains its existing functions within those requirements and the specified hook failure, guarding and interpreter/PATH-binding changes.

The report states that no gh credential separation is established. Shared credentials permit worker-initiated API merges despite native command denials. The GitHub boundary is detection, not prevention, with the required next-records-PR regime check owned by P1-11.

This task is `security: true`. The orchestrator obtains the task-level audit and a separate security-profile review of the final implementation head. The finding-class record includes `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign under the inherited completion rules.

Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. Changed heads receive fresh required evidence. The final-head security review precedes the gate.

The permission-surface change receives the required operator-backed approval through the repository's existing process. The worker writes no approval row and treats no candidate-tree decision as authority.

Live deployment is the operator's post-merge `make update`. The operator runs `make install-managed-settings`, inspects the rendered staging file and executes its printed `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` command with `/Library/Application Support/ClaudeCode/managed-settings.json` detected on macOS and `/etc/claude-code/managed-settings.json` detected on Linux. Administrative installation is recorded separately from staging and ordinary chezmoi application.

The operator performs the Claude worker-directory login with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected.

The operator applies the prepared deterministic Codex permgate rule that stops approving sandbox escapes and restarts affected sessions.

The deployment record checks effective settings after `make update` and administrative installation, including hooks added by merge scripts or integration installers. It verifies the installed managed-settings content, admin-required sandbox scope, worker directory, both platform policy outputs, static deny inventory, worktree-configuration denies, writable agmsg stores, worker-user and main-local hook placement, hook PATH and interpreter descendants, failure-policy coverage and sandbox startup without exposing credentials.

The effective-settings check includes conflicting project and local sandbox relaxations and confirms that they do not weaken the administrative policy. It also records the shared control-plane exclusions and Herdr socket as available capabilities. It makes no claim that worker user arrays subtract those entries.

Merge alone does not establish deployment readiness. The orchestrator records `make update`, the managed-settings installation with sudo, the Claude worker-directory login, effective startup checks and the Codex permgate rule before releasing dependent hardening tasks for live operation. The upstream agmsg store-driver route remains a named residual until its owning task is implemented. GitHub remains detection, not prevention, until the operator pursues separate-user or separate-host isolation under future P1-16.

## Checks (pasted by the orchestrator before each send)

```
amendment 2, 2026-10-19T08:1xZ; task-consistency-check.py: OK; C-80 text security review of this text: .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-db2a8f9.md.last.md Verdict: correct (amendment 1: e5d1b57 correct)
task=dotfiles-T133-worker-write-boundary-a01 tasks=2 amendments=1 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-19T05:42:14Z..none (-) source=live
detail: pr=none authors=claude-deep-dot tasks=01a152ae-8ef0-784f-801e-d4c9a4f3007f,01a152ed-0b08-7431-8fd0-5b5e43c89bd6 results=- questions=- withdrawn=- bot_heads=- source=live
```

Local Bats, live enforcement, administrative installation, worker-directory login, permgate policy changes and deployment are not performed by the worker.
Deployment remains unverified until the operator completes the post-merge steps; same-UID credential access, shared control-plane exclusions and Herdr socket access, writable-store driver selection and concurrent path consumption remain stated residuals.
**Organizing outputs clearly**
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '1,210p'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|threat.table|task-level audit' ~/.agents/skills/agmsg-orchestration/SKILL.md; git status --short; git rev-parse HEAD; cat .ua/meta.json" in ~/Workspace/dotfiles
 succeeded in 83ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-worker-write-boundary-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - home/dot_agents/agent-config.yaml
     8	  - home/.chezmoitemplates/claude-settings-managed.json
     9	  - home/.chezmoitemplates/claude-worker-settings.json
    10	  - home/.chezmoitemplates/claude-managed-settings.json
    11	  - home/dot_claude-worker/modify_private_settings.json
    12	  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    13	  - .claude/settings.json
    14	  - scripts/generate-agent-configs.py
    15	  - scripts/validate-agent-assets.py
    16	  - Makefile
    17	  - home/dot_local/bin/common/executable_herdr-agents
    18	  - home/dot_local/bin/common/executable_herdr-agent-state.sh
    19	  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
    20	  - .gitignore
    21	  - tests/unit/test_generate_agent_configs.py
    22	  - tests/unit/test_validate_agent_assets.py
    23	  - tests/unit/test_claude_settings_merge.py
    24	  - tests/unit/test_herdr_agents.py
    25	  - tests/unit/test_agmsg_orchestration_docs.py
    26	  - tests/unit/test_claude_worker_settings.py
    27	  - tests/unit/test_claude_managed_settings.py
    28	  - .orchestration/dotfiles-T133-worker-write-boundary-a01/**
    29	after: []
    30	threat_table:
    31	  - control: "tests/unit/test_agmsg_orchestration_docs.py (amendment 1: only the assertion of the Worker Playbook step 4 sentence this task rewrites changes; PR #427 edits this file first and merges before this PR, which rebases onto it)"
    32	    disposition: "residual: one assertion follows the rewritten sentence; the doc test module stays green in CI on the final head"
    33	  - control: "home/dot_agents/agent-config.yaml (trusted checkout and interpreter bindings, static trusted_paths inventory, distinct worker policy, managed sandbox policy and worker caches)"
    34	    disposition: "residual: the rendered policy reduces accidental and injected damage; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy checks both platforms without claiming same-UID isolation."
    35	  - control: "home/.chezmoitemplates/claude-settings-managed.json (orchestrator user settings with failIfUnavailable true, onFailure block, hook PATH bindings and absolute uv/Python PermissionRequest invocation)"
    36	    disposition: "residual: the user baseline preserves orchestrator functions within the managed sandbox policy; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the specified changes and retained settings; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision executes the rendered PermissionRequest under the system-only PATH and checks every rendered hook entrypoint."
    37	  - control: "home/.chezmoitemplates/claude-worker-settings.json (static trusted-path and worktree-configuration Edit denies, empty user exclusions, restricted write allowances, native merge denials and minimal delivery hooks)"
    38	    disposition: "residual: dedicated user settings reduce worker access to trusted paths; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the baseline and distinguishes it from shared managed exclusions and socket access."
    39	  - control: "home/.chezmoitemplates/claude-managed-settings.json (admin-required sandbox enforcement, fixed rendered control-plane exclusions and Herdr socket allowance)"
    40	    disposition: "residual: operator installation establishes the documented enforcement scope against project and local sandbox relaxation; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox asserts the rendered keys; shared control-plane capabilities and same-UID host access remain residual."
    41	  - control: "home/dot_claude-worker/modify_private_settings.json (deployment of the dedicated worker baseline without importing orchestrator policy)"
    42	    disposition: "residual: replacing the worker baseline's managed values reduces stale or permissive user configuration; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks repeated rendering in temporary homes."
    43	  - control: "home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl (anchored launch-root guard for tracked and main-checkout local project hooks)"
    44	    disposition: "residual: the guard reduces execution of worker-influenced project code and orchestrator hooks in worker sessions; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks fixed arguments, canonical identity and child status."
    45	  - control: "formatter and project-map reload configuration-selection boundary (the edited file path in the hook tool input and its owning repository)"
    46	    disposition: "residual: the guard skips these commands for input outside CLAUDE_PROJECT_DIR or in a worker repository under .claude/worktrees/, preventing consumption of worker-controlled Prettier JavaScript configuration and ruff settings; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks both the skip and normal anchored-file execution."
    47	  - control: ".claude/settings.json (portable HOME-relative installed-guard commands with fixed operation identifiers, explicit HOME re-export, pinned system PATH and onFailure block)"
    48	    disposition: "residual: guarded commands reduce worker-triggered project-hook execution while host-specific executable bindings remain in the per-host rendered guard and user settings; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure exhaustively traverses the hook entries and checks this split."
    49	  - control: "scripts/generate-agent-configs.py (separate user and managed settings generation, static manifest deny inventory and absolute executable bindings)"
    50	    disposition: "residual: rendering an explicit manifest list removes Git object traversal from inventory construction; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest checks exact manifest correspondence and filesystem coverage."
    51	  - control: "scripts/validate-agent-assets.py (consolidated item 16: exact platform-symmetric excludedCommands at base lines 349-355; structural sanitized Claude PermissionRequest wiring at base lines 1193-1200; enumeration and preservation of the other managed Claude settings, hook-composition and sandbox checks)"
    52	    disposition: "residual: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form covers the two exclusion fixtures; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate covers shlex parsing, the exact clean prefix, absolute uv and Python bindings, the fixed offline/no-cache uv arguments, the installed permgate script and sole claude argument, malformed or additional words and retained ccgate refusal; the Codex wiring check remains unchanged, and rendered-content validation does not establish live enforcement."
    53	  - control: "Makefile (the install-managed-settings target that renders a home-directory staging file and prints the operator's sudo install command)"
    54	    disposition: "residual: staging makes the administrative installation concrete without granting the worker administrative authority; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo checks the destination, rendered content, quoting and absence of privileged execution."
    55	  - control: "home/dot_local/bin/common/executable_herdr-agents (worker pane environment, dedicated Claude configuration, private caches, worker user hooks and guarded main-checkout local hooks)"
    56	    disposition: "residual: launch preparation reduces accidental inheritance of orchestrator settings and stale hooks (the legacy worktree-local file included: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks checks that migration against a fixture with a previously generated entry); tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches captures managed and standalone launches and repeated starts."
    57	  - control: "home/dot_local/bin/common/executable_herdr-agent-state.sh (repository-owned Herdr state helper with an explicitly supplied absolute Python interpreter)"
    58	    disposition: "residual: binding the helper and its Python child reduces shim execution; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters checks executed identities with planted shims."
    59	  - control: "home/dot_agents/skills/agmsg-orchestration/SKILL.md (the governing Worker Playbook step 4 sentence)"
    60	    disposition: "residual: the sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks its replacement; shared managed control-plane capabilities remain available and are not represented as per-seat isolation."
    61	  - control: ".gitignore (the .uv-cache directory pattern)"
    62	    disposition: "residual: ignoring the private cache reduces accidental cache publication; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
    63	  - control: "tests/unit/test_generate_agent_configs.py (separate platform policies, static inventory, interpreter bindings, tracked hook coverage and item 16's literal-form PermissionRequest assertions)"
    64	    disposition: "residual: render fixtures verify configuration and command construction; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_hooks_use_installed_permgate_paths and tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_claude_settings_use_interactive_profile_with_permgate cover the installed sanitized Claude hook with its bound uv/Python invocation and the synthetic renderer fixture respectively; they do not establish live enforcement or authenticate host-local inputs."
    65	  - control: "tests/unit/test_validate_agent_assets.py (consolidated item 16: the macOS gh-exclusion and Linux extra-exclusion fixtures, valid_claude_sandbox's exact required exclusions, the literal-form hook fixture and the structural PermissionRequest cases)"
    66	    disposition: "residual: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_accepts_manifest_symmetric_settings, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_rejects_each_broken_rule, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_requires_extra_codex_writable_roots, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs and tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs exercise the corrected shared sandbox fixture; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_hook_composition_requires_permgate_first and tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate cover the hook contract without claiming live enforcement."
    67	  - control: "tests/unit/test_claude_settings_merge.py (orchestrator baseline preservation, failure-policy rendering through the existing merge and item 16's literal-form managed PermissionRequest fixtures)"
    68	    disposition: "residual: temporary HOME fixtures verify baseline entries and identify runtime-added hooks separately; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_managed_permgate_replaces_stale_current_ccgate_hook, tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_permission_merge_preserves_unrelated_current_hooks and tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_permission_merge_preserves_custom_hook_in_mixed_entry retain stale-ccgate removal and custom-hook preservation with the specified managed hook; they do not install administrative settings."
    69	  - control: "tests/unit/test_herdr_agents.py (every launch route, repeated starts, main-local and worker-user hook placement, the legacy worktree-local migration, descendants, caches and retained native denials)"
    70	    disposition: "residual: fake launchers and subprocess markers verify effective arguments and executed fixture identities without starting live seats; shared managed exceptions remain explicitly outside per-seat exclusion claims."
    71	  - control: "tests/unit/test_claude_worker_settings.py (dedicated settings deployment, static narrow denies, worktree configuration protection, project guard and hook failure configuration)"
    72	    disposition: "residual: fixtures verify configured controls and credential-free deployment behavior; runtime permission checks and the remaining path-consumption window remain deployment and host residuals."
    73	  - control: "tests/unit/test_claude_managed_settings.py (managed policy rendering, conflicting project and local settings fixtures, rendered-hook executable resolution, PermissionRequest execution and nonprivileged staging)"
    74	    disposition: "residual: fixtures verify the selected documented enforcement keys and staging behavior; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision checks every rendered hook entrypoint and executes the real dependency-free permgate through bound uv/Python under PATH=/usr/bin:/bin, without simulating proof of Claude runtime enforcement or performing sudo installation."
    75	  - control: ".orchestration/dotfiles-T133-worker-write-boundary-a01/** (this task's branch artifacts)"
    76	    disposition: "residual: artifacts distinguish documentation facts, historical probes, final-head fixture results and unperformed operator deployment; acceptance compares their claims with the diff and CI."
    77	  - control: "the task-file copy at .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md (amendment 1 text)"
    78	    disposition: "residual: the first push deletes the a01 copy and adds the byte-identical dispatched a02 copy; TASK and RESULT carry the a02 copy's SHA256, which the orchestrator verifies at acceptance."
    79	  - control: "the evidence records under .orchestration/dotfiles-T133-worker-write-boundary-a01/"
    80	    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, outputs, statuses and tested revisions without credentials or unmasked home-directory paths."
    81	  - control: "task metadata (PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE)"
    82	    disposition: "residual: the orchestrator checks C1 to C10 and C7b, verifies dispatched bytes and binds integration evidence to the final head; P1-14 a05 and P1-6 implement retrieval of evidence of record from GitHub at its SHA; the GitHub boundary is detection, not prevention."
    83	  - control: metadata separators
    84	    disposition: "residual: the first document separators delimit format-2 metadata; the task-copy SHA256 binds the complete document."
    85	  - control: in-process effects
    86	    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no live deployment, login, administrative installation, permission-policy mutation or operator-session restart."
    87	  - control: workflow and interpreter or environment inputs
    88	    disposition: "residual: absolute interpreters, Python -I, sanitized Git, fixed hook PATH and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
    89	  - control: new or renamed scripts
    90	    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
    91	  - control: "5.14 item 0: host threat model"
    92	    disposition: "residual: host controls reduce accidental and injected damage without isolating seats sharing one OS user; prevention of worker-initiated merges requires a separate OS user or host under D-024-23's future P1-16, which the operator decides; the GitHub boundary is detection, not prevention, through P1-11's regime check in the next records PR for missing acceptance or gate evidence; shared managed control-plane exclusions and the Herdr socket remain residual."
    93	  - control: "5.14 item 1: worker write controls"
    94	    disposition: "residual: dedicated configuration, static symlink-aware Edit denies including worktree configuration and orchestrator worklogs and caches, narrow writable agmsg stores, managed sandbox enforcement and failIfUnavailable true reduce damage; documented path checks do not establish atomic immunity to concurrent path swaps."
    95	  - control: "5.14 item 2: sanitized environment and private executable PATH"
    96	    disposition: "residual: sanitized Git verification and absolute hook entrypoints reduce injected configuration, while PATH=/usr/bin:/bin binds upstream env-bash descendants away from shims; the remaining consuming-helper contracts belong to P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6."
    97	  - control: "5.14 item 3: trusted-path checks"
    98	    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
    99	  - control: "5.14 item 4: verified executable and consumed-byte identity"
   100	    disposition: "residual: hooks execute selected absolute entrypoints and trusted scripts, and upstream shell descendants inherit the fixed system PATH; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks; store-selected driver execution remains the separately named agmsg residual."
   101	  - control: "5.14 item 5: output and reservation identity"
   102	    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
   103	  - control: "5.14 item 6: honest residuals, hooks and MCP"
   104	    disposition: "residual: guarded tracked and main-local project hooks and minimal worker user hooks reduce host execution routes; shared managed Herdr socket access, control-plane exclusions, approved external processes and same-UID processes outside every seat sandbox remain residual."
   105	  - control: "5.14 item 7: trusted-execution verification"
   106	    disposition: "residual: this task records red-then-green render, merge, managed-policy, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
   107	  - control: "5.14 item 8: committed approval ledger"
   108	    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority; the GitHub boundary is detection, not prevention."
   109	  - control: "5.14 item 9: private uv caches"
   110	    disposition: "residual: per-seat worker caches, restricted worker write allowances and explicit denies on the orchestrator worklog and uv-cache reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
   111	  - control: "5.14 item 10: no worker command outside the sandbox"
   112	    disposition: "residual: empty worker user exclusions and disabled unsandboxed requests reduce escape routes; the worker rule forbids using shared managed control-plane exceptions, whose availability and Herdr socket access remain residual; the deterministic Codex permgate rule and live deployment remain operator steps."
   113	  - control: "hook failure policy"
   114	    disposition: "residual: every generated and tracked hook entry, including launcher-written worker user and main-local entries, carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
   115	  - control: "agmsg store driver and plugin selection (team configuration drivers.partition, db/trusted-plugins authorization and installed storage.sh sourcing)"
   116	    disposition: "residual: every seat writes the store, and installed storage.sh resolves drivers.partition as a driver path and sources it during unsandboxed delivery; it also uses db/trusted-plugins to authorize plugins/partition/shared.sh for sourcing; fixed PATH does not stop these routes; worker denies on plugins/** and db/trusted-plugins reduce the plugin route; dotfiles-T133-agmsg-hardening-a01 owns upstream basename validation, plugin authorization hardening and their adversarial red-then-green tests; this task introduces no store-derived sourcing beyond the installed scripts' current behavior."
   117	  - control: orchestrator effect merge
   118	    disposition: "residual: the worker is forbidden to merge; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub; shared credentials still permit worker-initiated API merges, so the GitHub boundary is detection, not prevention."
   119	  - control: orchestrator effect update-branch
   120	    disposition: "residual: the orchestrator owns branch updates and obtains fresh required CI, feedback, audit and security evidence for the resulting head."
   121	  - control: orchestrator effect forced worker removal
   122	    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain, and acceptance identifies any operator-authorized discarded state."
   123	premises:
   124	  - claim: >-
   125	      The historical a05 premises carried by the preceding text describe its recorded observations. They do not require this worker to rebuild PR 400, edit the approval ledger or implement P1-14 a05.
   126	    sources:
   127	      - .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
   128	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   129	  - claim: >-
   130	      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
   131	    sources:
   132	      - .orchestration/decisions.tsv
   133	      - .orchestration/plans/024-design-quality.md
   134	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   135	  - claim: >-
   136	      The existing Claude settings modify script merges the orchestrator user baseline into current settings and appends an attachment hook. The dedicated worker renderer does not import that orchestrator settings merge or its attachment behavior. The administrative managed-settings file is a separate deployment destination.
   137	    sources:
   138	      - home/dot_claude/modify_private_settings.json
   139	      - home/.chezmoitemplates/claude-settings-managed.json
   140	    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
   141	  - claim: >-
   142	      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
   143	    sources:
   144	      - home/dot_local/bin/common/executable_herdr-agents
   145	      - home/dot_agents/agent-config.yaml
   146	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
   147	  - claim: >-
   148	      Linked-worktree Claude sessions load the main checkout's .claude/settings.local.json. The current launcher writes worker-local delivery hooks and merge denials into a different file. Worker delivery moves to the worker configuration directory's user settings, and the launcher's main-checkout local hooks receive the orchestrator-only guard.
   149	    sources:
   150	      - https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository
   151	      - home/dot_local/bin/common/executable_herdr-agents
   152	      - .claude/settings.local.json
   153	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks
   154	  - claim: >-
   155	      Managed sandbox.enabled true, failIfUnavailable true and allowUnsandboxedCommands false establish the documented admin-required enforcement scope. Project and local settings cannot supply sandbox relaxations in that scope. User settings and shared managed exceptions remain distinct from project and local settings.
   156	    sources:
   157	      - https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox
   158	      - .orchestration/plans/024-design-quality.md
   159	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   160	    verification: tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings
   161	  - claim: >-
   162	      Installed agmsg storage.sh resolves the writable team configuration's drivers.partition value as a driver path and sources it during delivery. The upstream hardening belongs to dotfiles-T133-agmsg-hardening-a01 and remains a residual of this task.
   163	    sources:
   164	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   165	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md
   166	---
   167	
   168	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — INV-6 reset of a01 on tools/worker-write-boundary-a01, seat a010; plan 024 P1-15 under D-024-17, D-024-19, D-024-20, D-024-21 and D-024-23
   169	
   170	## Goal
   171	
   172	This is the amendment-4 text of the task dispatched at 2026-10-19T05:42Z (the ninth-round text that passed its pre-dispatch security review). Amendment 1 folds in two interpretation notes the worker needed (the inherited make format clause; the portable tracked `.claude/settings.json` with host-specific paths only in the rendered guard) and removes the Codex worker profile item (a Codex seat edits no Codex-boundary source; it becomes the separate Claude-seat task dotfiles-T133-codex-worker-network-a01). Everything else is the dispatched text in meaning; the branch, the eight green tests and the fixtures stay; the worker swaps the task copy to this text at its next push.
   173	
   174	The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime detects missing acceptance or gate-passage evidence in the next records PR, not at main-push time, because the records reach main only with that boundary PR. On a PR touching `.orchestration/acceptance/**`, the regime job checks every main merge commit since the previous boundary for its corresponding acceptance record with gate-passage evidence and fails the PR when one is missing. P1-11 owns implementation of that check; this task states section 5.14 item 0's detection rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.
   175	
   176	This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`.
   177	
   178	The administrative managed policy is shared by every Claude seat. Its Herdr socket allowance and three control-plane exclusions remain available to workers as well as the orchestrator. Empty arrays in worker user settings do not subtract these managed entries. Their availability is a residual under item 0, and the worker execution rule supplies no authorization to use them outside the sandbox.
   179	
   180	[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3. This Codex seat edits no Codex-boundary source.
   181	
   182	The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10.
   183	
   184	C-88: The following verbatim design sentences are normative for this task; the path is context only. The worker resolves `$HOME` when reading `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, and no tracked task text or task copy carries a literal operator home path, as required by the validator's home-path scan.
   185	
   186	> 5.14 item 1: Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。 worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。 hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。 `failIfUnavailable: true` を全席に置く。
   187	
   188	> 5.14 item 2: 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。
   189	
   190	> 5.14 item 9: orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。 `UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。
   191	
   192	> 5.14 item 10: worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。
   193	
   194	D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.
   195	
   196	The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. The retained mechanisms are documented symlink-aware deny rules, approval reads outside the local object database, hook interpreter bindings and runtime hook failure policy.
   197	
   198	The fourth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md`. Its six P1 findings remain recorded. The retained mechanisms are the static manifest deny inventory, protection of the orchestrator worklog and cache, narrow home denies around writable agmsg stores, correct linked-worktree hook placement and fixed hook-runtime PATH.
   199	
   200	The fifth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md`. Its three P1 findings remain recorded. This revision removes the gh credential-separation mechanism, records the upstream agmsg store-driver residual and moves sandbox enforcement into administrative managed settings.
   201	
   202	The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks reduce redirection risk without establishing an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)
   203	
   204	The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This historical observation confirms neither credential separation nor final-head deployment readiness.
   205	
   206	The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated Claude configuration mechanism, directory-specific Claude credentials, symlink coverage and `onFailure: "block"` support. These Claude credentials do not separate gh Keychain access.
   207	
   208	The settings documentation states, “In a worktree, it uses the file at the main checkout’s root.” Linked-worktree sessions therefore load the main checkout's `.claude/settings.local.json`. Worker hooks belong in `~/.claude-worker/settings.json`, and the main checkout's local hooks also receive the orchestrator-only guard. [Claude local settings reference](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository)
   209	
   210	## Files

 succeeded in 110ms:
---
name: ponytail-review
description: >
  Quality review of a change: is the logic right, is it safe, does it hold
  under real load, is risky code tested, is it fast enough, and is every line
  needed. Reads the connected code, not only the diff. Each finding is
  explained in plain English. Use for "review this", "code review", "review
  the last commit", "review my PR", "is this over-engineered", /ponytail-review.
---

Review a change like the senior developer who will be paged when it breaks.
Order of importance: correct, safe, holds under load, tested, fast, lean.
Lean still matters: every extra line must be read, tested and fixed later.
This is a report the user asked for, so give it in full.

## 1. Understand first

- Review what the user names: uncommitted or staged changes, a branch, a PR
  link, or files. Nothing named: the uncommitted changes, or the last commit
  if there are none.
- Read the diff, then the code it touches: callers of every changed function,
  the functions it calls, the tests, the README.
- Trace the real flow: where data comes in, what is stored, what goes out.
- A change can break code it does not touch. When a signature, return value
  or behavior changes, grep every caller.
- Find the expected load in the repo (README, deploy config): one person
  running a script, or many users and processes at once. Judge scale against
  that, and say which load you assumed.

## 2. Look for

1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item,
   rounding, time zones), a caller broken by the change, a fix applied in one
   caller while the shared function stays broken.
2. **Risk:** security holes (injection, weak randomness, secrets, missing
   checks on input from users), data loss (errors swallowed, writes in the
   wrong order, no transaction).
3. **Scale:** fine for one user, wrong for many: check-then-write races, the
   same work done by every process, memory or lists that only grow, a query
   per item, O(n^2) on big input, per-process state that must be shared.
4. **Missing test:** risky new logic (a branch, a parser, money, security,
   data writes, a bug fix) with no test that fails when it breaks. One good
   test, not coverage.
5. **Speed:** big slowdowns are problems. Small wins (work repeated in a hot
   loop) are suggestions; some software counts every millisecond.
6. **Lean:** code that should not exist or should be smaller.
   - delete: dead code, unused options, speculative features
   - reuse: the repo already has this helper (name the path)
   - stdlib / native: the standard library or platform already does it; a
     new dependency for a few lines
   - yagni: abstraction with one implementation, config nobody sets
   - merge: near-copies that must change together
   - split: one function doing several unrelated jobs, so it is hard to read
     or test. Split by job, never by line count, and never into helpers that
     exist only to make a function shorter.

## 3. Check before you report

- Every finding needs a concrete case: "this input or situation leads to this
  wrong result". No case, no finding.
- Re-read the lines and confirm: the caller exists, the value can really be
  empty, the code really is unused.
- A shortcut marked with a `shortcut:` (or older `ponytail:`) comment that names its limit is a
  decision, not a finding, unless the expected load already crosses it.
- Propose the smallest fix that works. Prefer fixes that delete code. Never
  add layers, frameworks or config the problem does not need.
- No style taste, no "consider", no vague worries.

## 4. Output

Very simple English: short sentences, everyday words. Explain a technical
term the first time you use it. The reader may never have seen this code.

Start with `What this change does:` in two or three sentences.

Then the findings in three groups, skip empty groups:
- **Must fix:** bug, security, data loss, breaks at the expected load.
- **Should fix:** risky code without a test, real slowness, duplication, a
  function that mixes jobs, code that should not exist.
- **Nice to have:** small speed-ups, shorter forms.

Number findings across all groups, so the user can say "fix 2 and 5".
Every finding has all four parts, each one or two short sentences:

2. **Orders land on the wrong day** (`billing/close_day.py:L40-52`)
   - **What this is:** At midnight this job closes the day and bills all orders of that day.
   - **Problem:** It takes "today" from the server clock, which runs in UTC. An order placed
     at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day once in the shop's time zone:
     `datetime.now(ZoneInfo("Europe/Berlin")).date()`. One line, nothing else changes.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes them by hand.

End with:
- `Verdict: Ship.` or `Verdict: fix 1 and 3 first.`
- `Lean: -<N> lines possible.` when lean findings exist.
- `Not checked:` one line, if something mattered and you could not check it.

Nothing found: `What this change does:`, then `Looks good. Ship.` and one line
on what you checked.

Lists findings, changes no code.

 succeeded in 179ms:
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
170:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
173:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
174:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
217:## Codex seat worklogs
 M .orchestration/acceptance/dotfiles-T128-chain-github-scripts-followup-a02.md
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a01.md
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a04.md
 M .orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-a01.md
 M .orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-followup-a01.md
 M .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a01.md
 M .orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-a01.md
 M .orchestration/acceptance/dotfiles-T129-doctor-sleep-disabled-a01.md
 M .orchestration/acceptance/dotfiles-T129-integration-seat-result-gate-cap-a01.md
 M .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-a01.md
 M .orchestration/acceptance/dotfiles-T129-orchestrator-load-mechanisms-a01.md
 M .orchestration/acceptance/dotfiles-T130-claude-sandbox-integration-a01.md
 M .orchestration/acceptance/dotfiles-T130-codex-local-review-exclusion-a01.md
 M .orchestration/acceptance/dotfiles-T130-sandbox-portability-a01.md
 M .orchestration/decisions.tsv
 M .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/023-omp-hcom-migration.md
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a05.md
 M .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a01.md
 M .orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-followup-a01.md
 M .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a01.md
 M .orchestration/tasks/dotfiles-T130-claude-sandbox-integration-followup-a01.md
 M .orchestration/tasks/dotfiles-T130-codex-local-review-exclusion-a01.md
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a05.md
?? .orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-followup-a02.md
?? .orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-followup-a03.md
?? .orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-followup-a04.md
?? .orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-followup-a05.md
?? .orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-followup-a07.md
?? .orchestration/acceptance/dotfiles-T129-anthropic-auth-runtime-check-a01.md
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a02.md
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a03.md
?? .orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a01.md
?? .orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a02.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a01.md
?? .orchestration/acceptance/dotfiles-T129-integration-seat-result-gate-cap-followup-a01.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a01.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a03.md
?? .orchestration/acceptance/dotfiles-T129-omp-config-render-a01.md
?? .orchestration/acceptance/dotfiles-T130-claude-sandbox-integration-followup-a01.md
?? .orchestration/acceptance/dotfiles-T130-sandbox-portability-followup-a01.md
?? .orchestration/acceptance/dotfiles-T131-claude-pinned-merge-gate-a01.md
?? .orchestration/acceptance/dotfiles-T131-claude-pinned-merge-gate-review-a01.md
?? .orchestration/acceptance/dotfiles-T132-make-update-followups-a01.md
?? .orchestration/acceptance/dotfiles-T133-audit-pool-a01.md
?? .orchestration/acceptance/dotfiles-T133-ci-efficiency-a01.md
?? .orchestration/acceptance/dotfiles-T133-ci-efficiency-a02.md
?? .orchestration/acceptance/dotfiles-T133-ci-efficiency-followup-a01.md
?? .orchestration/acceptance/dotfiles-T133-ci-efficiency-followup-a02.md
?? .orchestration/acceptance/dotfiles-T133-ci-efficiency-followup-a04.md
?? .orchestration/acceptance/dotfiles-T133-codex-worker-network-a01.md
?? .orchestration/acceptance/dotfiles-T133-dispositions-a01.md
?? .orchestration/acceptance/dotfiles-T133-hold-playbook-a01.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a01.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a02.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a03.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a04.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-a02.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
?? .orchestration/acceptance/dotfiles-T133-result-precheck-a01.md
?? .orchestration/acceptance/dotfiles-T133-result-precheck-a02.md
?? .orchestration/acceptance/dotfiles-T133-result-precheck-a03.md
?? .orchestration/acceptance/dotfiles-T133-result-precheck-a04.md
?? .orchestration/acceptance/dotfiles-T133-rule-text-reduction-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a01.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a02.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md
?? .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a04.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-followup-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/20261018_042459_done.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/20261018_042459_learn.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/20261018_042459_plan.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/20261018_042459_todo.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/amendment1/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/amendment2/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/amendment3/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/autoskill.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/bot-final.json
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/ci-progress.json
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/delivery.json
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/dotfiles-T133-worker-cap-hookspath-a01-worker-crit.json
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/dotfiles-T133-worker-cap-hookspath-a01-worker-review-receipt.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/learning.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/pr-body.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/pr-final.json
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/pr-metadata.json
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/raw/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/ready-epoch.txt
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/report.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/resume.log
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/sandbox.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/validation.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/20261018_071205_plan.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/20261018_071205_todo.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/autoskill.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/base-c966/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/clean-candidate/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/dotfiles-T133-worker-cap-hookspath-a02-worker-crit.json
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/dotfiles-T133-worker-cap-hookspath-a02-worker-review-receipt.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/learning.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/measure.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/raw/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/report.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/sandbox.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/validation.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/learning.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/report.md
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/sandbox.md
?? .orchestration/handoff/2026-10-17T1620Z.md
?? .orchestration/learning/classes.yaml
?? .orchestration/learning/mistakes/M-20261017-08.md
?? .orchestration/learning/mistakes/M-20261017-09.md
?? .orchestration/learning/mistakes/M-20261018-01.md
?? .orchestration/learning/mistakes/M-20261018-02.md
?? .orchestration/learning/mistakes/M-20261018-08.md
?? .orchestration/learning/mistakes/M-20261018-09.md
?? .orchestration/learning/mistakes/M-20261018-10.md
?? .orchestration/learning/mistakes/M-20261018-11.md
?? .orchestration/learning/mistakes/M-20261018-12.md
?? .orchestration/learning/mistakes/M-20261018-13.md
?? .orchestration/learning/mistakes/M-20261018-14.md
?? .orchestration/learning/mistakes/M-20261018-15.md
?? .orchestration/learning/mistakes/M-20261018-16.md
?? .orchestration/learning/mistakes/M-20261019-01.md
?? .orchestration/learning/mistakes/M-20261019-02-test-cap-without-room.md
?? .orchestration/learning/mistakes/M-20261019-03-revise-past-s1.md
?? .orchestration/learning/mistakes/M-20261019-04-parser-gap.md
?? .orchestration/plans/024-checklists.md
?? .orchestration/plans/024-design-evidence.md
?? .orchestration/plans/024-design-mechanism.md
?? .orchestration/plans/024-design-programs.md
?? .orchestration/plans/024-design-prs.md
?? .orchestration/plans/024-design-quality.md
?? .orchestration/plans/024-design.md
?? .orchestration/plans/024-execution.md
?? .orchestration/plans/024-omp-cutover-and-corrective-order.md
?? .orchestration/plans/024-progress.tsv
?? .orchestration/plans/024-todo.md
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a03.md
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a04.md
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a05.md
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a06.md
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a07.md
?? .orchestration/tasks/dotfiles-T129-anthropic-auth-runtime-check-a01.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md
?? .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a04.md
?? .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a03.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a03.md
?? .orchestration/tasks/dotfiles-T129-omp-config-render-a01.md
?? .orchestration/tasks/dotfiles-T130-sandbox-portability-followup-a01.md
?? .orchestration/tasks/dotfiles-T131-claude-pinned-merge-gate-review-a01.md
?? .orchestration/tasks/dotfiles-T132-make-update-followups-a01.md
?? .orchestration/tasks/dotfiles-T132-merge-train-builder-a01.md
?? .orchestration/tasks/dotfiles-T132-merge-train-ci-a01.md
?? .orchestration/tasks/dotfiles-T133-audit-pool-a01.md
?? .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-a01.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-a02.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a02.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a03.md
?? .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
?? .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
?? .orchestration/tasks/dotfiles-T133-dispositions-a01.md
?? .orchestration/tasks/dotfiles-T133-dispositions-a02.md
?? .orchestration/tasks/dotfiles-T133-dispositions-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-hold-playbook-a01.md
?? .orchestration/tasks/dotfiles-T133-hold-playbook-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a02.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a03.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a04.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-a02.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a01.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a02.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a03.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
?? .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-rule-text-reduction-a01.md
?? .orchestration/tasks/dotfiles-T133-rule-text-reduction-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a02.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a01.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a02.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
?? .orchestration/tasks/dotfiles-T133-verdict-audit-pool-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-followup-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-hooks-path-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-a01-chain-c1ba96f.log
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-a01-local-review-c1ba96f.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a02-chain-a64daf1.log
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a02-chain-a905629.log
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a02-chain-b139995.log
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a02-chain-d3480fc.log
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a02-local-review-a64daf1.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a02-local-review-b139995.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a04-chain-325f520.log
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a04-local-review-325f520.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a04-security-325f520.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a04-security-325f520.md.last.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a05-security-2b6fc7f.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a05-security-2b6fc7f.md.last.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a05-security-eda0354.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a05-security-eda0354.md.last.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-066254d.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-066254d.md.last.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-2707add.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-2707add.md.last.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-d20a2dd.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-d20a2dd.md.last.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-claude-r1.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-claude-r2.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-codex-r1.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-codex-r1.md.last.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-codex-r2.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-runtime-check-a01-task-review-codex-r2.md.last.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a01-audit-9842d91.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a01-audit-9842d91.md.last.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a01-chain-2b91aef.log
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a01-chain-9842d91.log
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a01-crit.json
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a01-local-review-9842d91.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a02-audit-2b9abca.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a02-audit-2b9abca.md.last.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a02-chain-0c75842.log
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a02-chain-2b9abca.log
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a02-crit.json
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a02-local-review-2b9abca.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-chain-1b3e0ee.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-a01-chain-741e242.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-a01-local-review-741e242.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-audit-274a536.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-audit-274a536.md.last.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-chain-274a536.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-chain-e23f3f9.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-crit.json
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-local-review-274a536.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-security-274a536.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a01-security-274a536.md.last.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-audit-9d13a06.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-audit-9d13a06.md.last.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-chain-6fd8c49.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-chain-9d13a06.log
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-crit.json
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-local-review-9d13a06.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-security-9d13a06.md
?? .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-followup-a02-security-9d13a06.md.last.md
?? .orchestration/validation/dotfiles-T129-doctor-sleep-disabled-a01-audit-b8bb9a7.md
?? .orchestration/validation/dotfiles-T129-doctor-sleep-disabled-a01-audit-b8bb9a7.md.last.md
?? .orchestration/validation/dotfiles-T129-doctor-sleep-disabled-a01-crit.json
?? .orchestration/validation/dotfiles-T129-doctor-sleep-disabled-a01-local-review-b8bb9a7.md
?? .orchestration/validation/dotfiles-T129-doctor-sleep-disabled-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-doctor-sleep-disabled-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T129-integration-seat-result-gate-cap-a01-audit-9c07098.md
?? .orchestration/validation/dotfiles-T129-integration-seat-result-gate-cap-a01-audit-9c07098.md.last.md
?? .orchestration/validation/dotfiles-T129-integration-seat-result-gate-cap-a01-crit.json
?? .orchestration/validation/dotfiles-T129-integration-seat-result-gate-cap-a01-local-review-9c07098.md
?? .orchestration/validation/dotfiles-T129-integration-seat-result-gate-cap-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-integration-seat-result-gate-cap-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a01-chain-6bea93a.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a01-chain-7df9183.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a01-chain-b0479c8.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a01-chain-c0eb536.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a03-audit-4f5be51.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a03-audit-4f5be51.md.last.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a03-chain-4f5be51.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a03-crit.json
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a03-local-review-4f5be51.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a03-review-receipt.md
?? .orchestration/validation/dotfiles-T129-omp-hcom-stage1-task-review-codex-r1.md
?? .orchestration/validation/dotfiles-T129-omp-hcom-stage1-task-review-codex-r1.md.last.md
?? .orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-audit-3498973.md
?? .orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-audit-3498973.md.last.md
?? .orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-crit.json
?? .orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-local-review-3498973.md
?? .orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-local-review-3cb02fc.md
?? .orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-local-review-fbbc6d9.md
?? .orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T130-codex-local-review-exclusion-a01-security-99b5f86.md
?? .orchestration/validation/dotfiles-T130-codex-local-review-exclusion-a01-security-99b5f86.md.last.md
?? .orchestration/validation/dotfiles-T132-make-update-followups-a01-audit-6121555.md
?? .orchestration/validation/dotfiles-T132-make-update-followups-a01-audit-6121555.md.last.md
?? .orchestration/validation/dotfiles-T132-make-update-followups-a01-chain-6121555.log
?? .orchestration/validation/dotfiles-T132-make-update-followups-a01-crit.json
?? .orchestration/validation/dotfiles-T132-make-update-followups-a01-local-review-6121555.md
?? .orchestration/validation/dotfiles-T132-make-update-followups-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T132-make-update-followups-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-audit-pool-a01-text-security.md
?? .orchestration/validation/dotfiles-T133-audit-pool-a01-text-security.md.last.md
?? .orchestration/validation/dotfiles-T133-audit-pool-a02-text-security.md
?? .orchestration/validation/dotfiles-T133-audit-pool-a02-text-security.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a01-audit-27613c0.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a01-audit-27613c0.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a01-chain-27613c0.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a01-crit.json
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a01-local-review-27613c0.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-audit-4fe2438.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-audit-4fe2438.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-chain-4fe2438.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-chain-b33b418.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-crit.json
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-local-review-4fe2438.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-security-4fe2438.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-a02-security-4fe2438.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-audit-76ab18e.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-audit-76ab18e.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-chain-08ad9d5.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-chain-76ab18e.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-crit.json
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-local-review-76ab18e.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-security-76ab18e.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a01-security-76ab18e.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-chain-09ea7de.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-chain-7329f0e.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-chain-b0d957c.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-chain-c013846.log
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-local-review-7329f0e.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-security-44cb835.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-security-44cb835.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-0512275.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-0512275.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-1de8de2.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-1de8de2.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-9fc8dc4.md
?? .orchestration/validation/dotfiles-T133-codex-worker-network-a01-text-security-5076362.md
?? .orchestration/validation/dotfiles-T133-codex-worker-network-a01-text-security-5076362.md.last.md
?? .orchestration/validation/dotfiles-T133-codex-worker-network-a01-text-security-cf5efd5.md
?? .orchestration/validation/dotfiles-T133-codex-worker-network-a01-text-security-cf5efd5.md.last.md
?? .orchestration/validation/dotfiles-T133-dispositions-a01-audit-fa47987.md
?? .orchestration/validation/dotfiles-T133-dispositions-a01-audit-fa47987.md.last.md
?? .orchestration/validation/dotfiles-T133-dispositions-a01-chain-97a0820.log
?? .orchestration/validation/dotfiles-T133-dispositions-a01-chain-bdbbbf9.log
?? .orchestration/validation/dotfiles-T133-dispositions-a01-chain-fa47987.log
?? .orchestration/validation/dotfiles-T133-dispositions-a01-crit.json
?? .orchestration/validation/dotfiles-T133-dispositions-a01-local-review-bdbbbf9.md
?? .orchestration/validation/dotfiles-T133-dispositions-a01-local-review-fa47987.md
?? .orchestration/validation/dotfiles-T133-dispositions-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-dispositions-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md
?? .orchestration/validation/dotfiles-T133-dispositions-a02-text-security.md.last.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-chain-9f5eaee.log
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-chain-c206774.log
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-crit.json
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-local-review-9f5eaee.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-local-review-c206774.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a03-chain-31d6c32.log
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a03-chain-bc7593a.log
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a03-security-31d6c32.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a03-security-31d6c32.md.last.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a04-chain-0e5d880.log
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a04-chain-911f520.log
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a04-local-review-911f520.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a04-security-911f520.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a04-security-911f520.md.last.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-audit-7fad835.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-audit-7fad835.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-audit-f7d2c48.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-audit-f7d2c48.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-chain-7fad835.log
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-chain-a5a9f4e.log
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-chain-f7d2c48.log
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-crit.json
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-local-review-7fad835.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-local-review-f7d2c48.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-security-7fad835.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-security-7fad835.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-security-a5a9f4e.md
?? .orchestration/validation/dotfiles-T133-regime-ci-a02-security-a5a9f4e.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-audit-380e7f4.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-audit-380e7f4.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-chain-380e7f4.log
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-chain-80e4040.log
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-crit.json
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-local-review-380e7f4.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-security-380e7f4.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-security-380e7f4.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-security-80e4040.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a01-security-80e4040.md.last.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a01-chain-a5cb73b.log
?? .orchestration/validation/dotfiles-T133-result-precheck-a01-local-review-a5cb73b.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a02-chain-40a053e.log
?? .orchestration/validation/dotfiles-T133-result-precheck-a02-chain-4ed1b27.log
?? .orchestration/validation/dotfiles-T133-result-precheck-a02-chain-9cd5514.log
?? .orchestration/validation/dotfiles-T133-result-precheck-a02-local-review-4ed1b27.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a02-local-review-9cd5514.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-audit-bccb2de.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-audit-bccb2de.md.last.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-audit-ddf262d.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-audit-ddf262d.md.last.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-chain-1aa7273.log
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-chain-58f98bf.log
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-chain-bccb2de.log
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-chain-ddf262d.log
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-crit.json
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-local-review-bccb2de.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-local-review-ddf262d.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-review-receipt.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-security-ddf262d.md
?? .orchestration/validation/dotfiles-T133-result-precheck-a03-security-ddf262d.md.last.md
?? .orchestration/validation/dotfiles-T133-rule-text-reduction-a01-audit-e2ea4a5.md
?? .orchestration/validation/dotfiles-T133-rule-text-reduction-a01-audit-e2ea4a5.md.last.md
?? .orchestration/validation/dotfiles-T133-rule-text-reduction-a01-chain-e2ea4a5.log
?? .orchestration/validation/dotfiles-T133-rule-text-reduction-a01-crit.json
?? .orchestration/validation/dotfiles-T133-rule-text-reduction-a01-local-review-e2ea4a5.md
?? .orchestration/validation/dotfiles-T133-rule-text-reduction-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-rule-text-reduction-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-audit-9da0ed3.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-chain-37d969e.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-chain-9da0ed3.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-local-review-9da0ed3.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-audit-8a09b93.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-chain-3f12e60.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-chain-63b6aca.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-chain-8a09b93.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-local-review-8a09b93.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a02-security-8a09b93.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-11c9399.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-11c9399.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-49a7944.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-49a7944.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-5c20a6e.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-5c20a6e.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-819bdac.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-819bdac.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-8ce8dba.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-8ce8dba.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-8d1bf0b.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-8d1bf0b.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-9fe33aa.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-9fe33aa.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a03-text-security-f6797ab.md.last.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-0db5f17.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-485d6b3.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-chain-85a4722.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a01-local-review-85a4722.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-82b99ed.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-b8998de.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-chain-cfeca64.log
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-local-review-b8998de.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a02-local-review-cfeca64.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-12b9ebf.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-6748694.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-6748694.md.last.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-b9bf09a.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-b9bf09a.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-audit-c96697a.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-audit-c96697a.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-chain-c96697a.log
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-crit.json
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-local-review-c96697a.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-audit-bb84bde.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-audit-bb84bde.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-chain-b813355.log
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-chain-bb84bde.log
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-crit.json
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-local-review-bb84bde.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-security-bb84bde.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-a02-security-bb84bde.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-audit-2d8b0fe.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-audit-2d8b0fe.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-chain-2d8b0fe.log
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-chain-570d749.log
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-crit.json
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-local-review-2d8b0fe.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-security-2d8b0fe.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-security-2d8b0fe.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-security-570d749.md
?? .orchestration/validation/dotfiles-T133-worker-cap-hookspath-followup-a01-security-570d749.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-1ae3138.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-1ae3138.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-435275a.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-435275a.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-519afd7.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-519afd7.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-5cbbc03.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-5cbbc03.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-67415f5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-67415f5.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8520998.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-987865d.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-987865d.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-db2a8f9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-db2a8f9.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-e5d1b57.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-e5d1b57.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f1b862c.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f1b862c.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f589c7c.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f589c7c.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f810c30.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f810c30.md.last.md
69dccca98aa772b790f366d63194228372a3c3b0
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

**Managing budget and output format**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '99,209p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
    99	  - control: "5.14 item 4: verified executable and consumed-byte identity"
   100	    disposition: "residual: hooks execute selected absolute entrypoints and trusted scripts, and upstream shell descendants inherit the fixed system PATH; evidence snapshots, last-use digest checks and their race limitations remain with the consuming orchestrator-side tasks; store-selected driver execution remains the separately named agmsg residual."
   101	  - control: "5.14 item 5: output and reservation identity"
   102	    disposition: "residual: this task adds no reservation protocol; full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator-side tasks that create them."
   103	  - control: "5.14 item 6: honest residuals, hooks and MCP"
   104	    disposition: "residual: guarded tracked and main-local project hooks and minimal worker user hooks reduce host execution routes; shared managed Herdr socket access, control-plane exclusions, approved external processes and same-UID processes outside every seat sandbox remain residual."
   105	  - control: "5.14 item 7: trusted-execution verification"
   106	    disposition: "residual: this task records red-then-green render, merge, managed-policy, guard, launch, descendant and cache tests; P1-6 owns tests/unit/trusted_exec_contract.py and the consuming-helper contract tests."
   107	  - control: "5.14 item 8: committed approval ledger"
   108	    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority; the GitHub boundary is detection, not prevention."
   109	  - control: "5.14 item 9: private uv caches"
   110	    disposition: "residual: per-seat worker caches, restricted worker write allowances and explicit denies on the orchestrator worklog and uv-cache reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
   111	  - control: "5.14 item 10: no worker command outside the sandbox"
   112	    disposition: "residual: empty worker user exclusions and disabled unsandboxed requests reduce escape routes; the worker rule forbids using shared managed control-plane exceptions, whose availability and Herdr socket access remain residual; the deterministic Codex permgate rule and live deployment remain operator steps."
   113	  - control: "hook failure policy"
   114	    disposition: "residual: every generated and tracked hook entry, including launcher-written worker user and main-local entries, carries onFailure block, reducing fail-open behavior where Claude supports it; configuration tests cover missing-command and timeout policy, while background hooks and events on which the field has no effect carry no enforcement responsibility."
   115	  - control: "agmsg store driver and plugin selection (team configuration drivers.partition, db/trusted-plugins authorization and installed storage.sh sourcing)"
   116	    disposition: "residual: every seat writes the store, and installed storage.sh resolves drivers.partition as a driver path and sources it during unsandboxed delivery; it also uses db/trusted-plugins to authorize plugins/partition/shared.sh for sourcing; fixed PATH does not stop these routes; worker denies on plugins/** and db/trusted-plugins reduce the plugin route; dotfiles-T133-agmsg-hardening-a01 owns upstream basename validation, plugin authorization hardening and their adversarial red-then-green tests; this task introduces no store-derived sourcing beyond the installed scripts' current behavior."
   117	  - control: orchestrator effect merge
   118	    disposition: "residual: the worker is forbidden to merge; the orchestrator follows the final-head integration gate, required permission approval and pinned squash-merge procedure, with evidence of record retrieved from GitHub; shared credentials still permit worker-initiated API merges, so the GitHub boundary is detection, not prevention."
   119	  - control: orchestrator effect update-branch
   120	    disposition: "residual: the orchestrator owns branch updates and obtains fresh required CI, feedback, audit and security evidence for the resulting head."
   121	  - control: orchestrator effect forced worker removal
   122	    disposition: "residual: no forced removal is planned; existing dirty-worktree protections remain, and acceptance identifies any operator-authorized discarded state."
   123	premises:
   124	  - claim: >-
   125	      The historical a05 premises carried by the preceding text describe its recorded observations. They do not require this worker to rebuild PR 400, edit the approval ledger or implement P1-14 a05.
   126	    sources:
   127	      - .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
   128	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   129	  - claim: >-
   130	      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
   131	    sources:
   132	      - .orchestration/decisions.tsv
   133	      - .orchestration/plans/024-design-quality.md
   134	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   135	  - claim: >-
   136	      The existing Claude settings modify script merges the orchestrator user baseline into current settings and appends an attachment hook. The dedicated worker renderer does not import that orchestrator settings merge or its attachment behavior. The administrative managed-settings file is a separate deployment destination.
   137	    sources:
   138	      - home/dot_claude/modify_private_settings.json
   139	      - home/.chezmoitemplates/claude-settings-managed.json
   140	    verification: tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks
   141	  - claim: >-
   142	      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
   143	    sources:
   144	      - home/dot_local/bin/common/executable_herdr-agents
   145	      - home/dot_agents/agent-config.yaml
   146	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches
   147	  - claim: >-
   148	      Linked-worktree Claude sessions load the main checkout's .claude/settings.local.json. The current launcher writes worker-local delivery hooks and merge denials into a different file. Worker delivery moves to the worker configuration directory's user settings, and the launcher's main-checkout local hooks receive the orchestrator-only guard.
   149	    sources:
   150	      - https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository
   151	      - home/dot_local/bin/common/executable_herdr-agents
   152	      - .claude/settings.local.json
   153	    verification: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks
   154	  - claim: >-
   155	      Managed sandbox.enabled true, failIfUnavailable true and allowUnsandboxedCommands false establish the documented admin-required enforcement scope. Project and local settings cannot supply sandbox relaxations in that scope. User settings and shared managed exceptions remain distinct from project and local settings.
   156	    sources:
   157	      - https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox
   158	      - .orchestration/plans/024-design-quality.md
   159	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   160	    verification: tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings
   161	  - claim: >-
   162	      Installed agmsg storage.sh resolves the writable team configuration's drivers.partition value as a driver path and sources it during delivery. The upstream hardening belongs to dotfiles-T133-agmsg-hardening-a01 and remains a residual of this task.
   163	    sources:
   164	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
   165	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md
   166	---
   167	
   168	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — INV-6 reset of a01 on tools/worker-write-boundary-a01, seat a010; plan 024 P1-15 under D-024-17, D-024-19, D-024-20, D-024-21 and D-024-23
   169	
   170	## Goal
   171	
   172	This is the amendment-4 text of the task dispatched at 2026-10-19T05:42Z (the ninth-round text that passed its pre-dispatch security review). Amendment 1 folds in two interpretation notes the worker needed (the inherited make format clause; the portable tracked `.claude/settings.json` with host-specific paths only in the rendered guard) and removes the Codex worker profile item (a Codex seat edits no Codex-boundary source; it becomes the separate Claude-seat task dotfiles-T133-codex-worker-network-a01). Everything else is the dispatched text in meaning; the branch, the eight green tests and the fixtures stay; the worker swaps the task copy to this text at its next push.
   173	
   174	The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime detects missing acceptance or gate-passage evidence in the next records PR, not at main-push time, because the records reach main only with that boundary PR. On a PR touching `.orchestration/acceptance/**`, the regime job checks every main merge commit since the previous boundary for its corresponding acceptance record with gate-passage evidence and fails the PR when one is missing. P1-11 owns implementation of that check; this task states section 5.14 item 0's detection rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.
   175	
   176	This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`.
   177	
   178	The administrative managed policy is shared by every Claude seat. Its Herdr socket allowance and three control-plane exclusions remain available to workers as well as the orchestrator. Empty arrays in worker user settings do not subtract these managed entries. Their availability is a residual under item 0, and the worker execution rule supplies no authorization to use them outside the sandbox.
   179	
   180	[memory:decision] D-024-20 makes this task the dispatch prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator places this task in their `after:` fields before dispatch. This task has `after: []`. A Codex seat performs these Claude configuration edits under the routing rule, including the Worker Playbook step 4 sentence permitted by plan 021 step 8.3. This Codex seat edits no Codex-boundary source.
   181	
   182	The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10.
   183	
   184	C-88: The following verbatim design sentences are normative for this task; the path is context only. The worker resolves `$HOME` when reading `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, and no tracked task text or task copy carries a literal operator home path, as required by the validator's home-path scan.
   185	
   186	> 5.14 item 1: Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。 worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。 hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。 `failIfUnavailable: true` を全席に置く。
   187	
   188	> 5.14 item 2: 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。
   189	
   190	> 5.14 item 9: orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。 `UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。
   191	
   192	> 5.14 item 10: worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。
   193	
   194	D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.
   195	
   196	The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. The retained mechanisms are documented symlink-aware deny rules, approval reads outside the local object database, hook interpreter bindings and runtime hook failure policy.
   197	
   198	The fourth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md`. Its six P1 findings remain recorded. The retained mechanisms are the static manifest deny inventory, protection of the orchestrator worklog and cache, narrow home denies around writable agmsg stores, correct linked-worktree hook placement and fixed hook-runtime PATH.
   199	
   200	The fifth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md`. Its three P1 findings remain recorded. This revision removes the gh credential-separation mechanism, records the upstream agmsg store-driver residual and moves sandbox enforcement into administrative managed settings.
   201	
   202	The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks reduce redirection risk without establishing an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)
   203	
   204	The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This historical observation confirms neither credential separation nor final-head deployment readiness.
   205	
   206	The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated Claude configuration mechanism, directory-specific Claude credentials, symlink coverage and `onFailure: "block"` support. These Claude credentials do not separate gh Keychain access.
   207	
   208	The settings documentation states, “In a worktree, it uses the file at the main checkout’s root.” Linked-worktree sessions therefore load the main checkout's `.claude/settings.local.json`. Worker hooks belong in `~/.claude-worker/settings.json`, and the main checkout's local hooks also receive the orchestrator-only guard. [Claude local settings reference](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository)
   209	

exec
/bin/zsh -lc "sed -n '/## Codex seat worklogs/,/"'^## /p'"' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
## Codex seat worklogs

Project layouts vary by language. Set up this worklog structure only when it
does not already exist, and use timestamped filenames in `YYYYMMDD_HHMMSS`
form:

- `.agents/worklog/codex/plan/<timestamp>_plan.md` stores the plan and design
  written before implementation. Ask the user questions when needed, and
  update the plan when questions, learning, or completed tasks change it. It
  must contain `Goal`, `Scope`, `Assumptions`, `Design`, `Tests`, and
  `Open Questions`.
- `.agents/worklog/codex/todo/<timestamp>_todo.md` derives its tasks from the
  plan. Move completed items from `TODO` to `Done`; when `TODO` is empty, set
  its status to `done` and rename it to `<timestamp>_done.md`. It must contain
  `TODO` and `Done`.
- `.agents/worklog/codex/learn/<timestamp>_learn.md` records only reusable,
  validated knowledge that speeds a future decision. State what was learned
  and where it applies, update the plan's `Assumptions`, `Design`, or `Tests`
  when relevant. A learn file must contain `Date`, `Learnings`, and
  `Plan Updates`.

Every plan, todo, and learn file starts with YAML frontmatter containing
`type` (`plan`, `todo`, or `learn`), `id` (`YYYYMMDD_HHMMSS`), `owner` (for
example, `codex-a`), and ISO8601 `created_at` and `updated_at`. Additionally:

- todo requires `status`, `workstream`, and `related_plan`; status is one of
  `active`, `blocked`, `done`, or `superseded`;
- plan requires `status`, one of `draft`, `active`, `done`, or `superseded`;
- learn requires `validated` (`true` or `false`) and `apply_to` (plan/tests),
  and may be created only when reusable and validated.

Optional frontmatter keys are `depends_on` (todo ID array), `blocked_reason`
for blocked work, `evidence` (path array), and `tags`.

## Pitfalls

exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '210,365p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
   210	## Files
   211	
   212	1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.
   213	
   214	   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. Both user-settings renders use the same `claude.execution` bindings: resolve Python from `claude.execution.tool_paths.python3`, the trusted source behind `claude.execution.python`, and add the missing `claude.execution.tool_paths.uv` binding for the installed uv binary. Render their resolved absolute executable files, not PATH lookups or a private link whose creation depends on an earlier hook. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them. The manifest also supplies the trusted bindings from which the render resolves the absolute directories holding `ruff`, `prettier` and `terminal-browser`, without using mise shims.
   215	
   216	   The manifest defines a separate Claude worker settings output at `home/.chezmoitemplates/claude-worker-settings.json` and an administrative managed-settings output at `home/.chezmoitemplates/claude-managed-settings.json`. The worker configuration directory is `~/.claude-worker`. The launcher passes its expanded absolute path as `CLAUDE_CONFIG_DIR`.
   217	
   218	   A static `trusted_paths:` list names every protected top-level path of the anchored checkout and the protected home paths. It explicitly includes `<anchored-checkout>/.agents/worklog/**` and `<anchored-checkout>/.agents/worklog/uv-cache/**`. The `.claude` entries protect tracked contents and the main checkout's `.claude/settings.local.json` without denying the whole `.claude/worktrees/` tree. The list explicitly names directory targets and descendant patterns where both are required.
   219	
   220	   Separate worker Edit denies protect `//<anchored-checkout>/.claude/worktrees/*/.claude/**` and `//<anchored-checkout>/.claude/worktrees/*/.mcp.json`. The `.claude` directory target is also protected. Ordinary worktree source files and the per-seat cache remain outside these configuration denies.
   221	
   222	   The home-path denies are `~/.agents/agent-config.yaml`, `~/.agents/model-profiles.env`, `~/.agents/skills/**/scripts/**`, `~/.agents/skills/**/SKILL.md`, `~/.agents/skills/agmsg/plugins/**`, `~/.agents/skills/agmsg/db/trusted-plugins`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/bin/**`, `~/.local/share/**`, `~/.local/state/**`, `~/.local/share/mise/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. No blanket deny on `~/.agents/**` or `~/.local/**` replaces this list.
   223	
   224	   The agmsg store paths `~/.agents/skills/agmsg/db`, `~/.agents/skills/agmsg/teams`, `~/.agents/skills/agmsg/run` and `~/.agents/skills/agmsg/ext-tools` remain writable. Deny patterns cover neither these directory targets nor their descendants except the file `~/.agents/skills/agmsg/db/trusted-plugins`. Edit denies merge into the sandbox configuration, so Bash writes to that file and `~/.agents/skills/agmsg/plugins/**` are refused too. Their influence on installed delivery-script driver and plugin selection remains the separately owned agmsg residual.
   225	
   226	   The orchestrator retains its existing permissions, cache allowances and hook functions within the administrative managed policy. Its user baseline receives `failIfUnavailable: true`, `onFailure: "block"` on its hooks and the interpreter and PATH bindings below. Its exclusion entries match the three control-plane entries specified below; the former Linux `gh *` exclusion is removed.
   227	
   228	   The worker user policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`. Shared managed entries remain effective despite these empty worker arrays.
   229	
   230	   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.
   231	
   232	   Existing model selections, Codex worker profile values, Codex sandbox and approval arguments and Codex shared Git grants retain their meaning and remain unchanged. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.
   233	
   234	2. `scripts/generate-agent-configs.py` renders the distinct orchestrator user, worker user and administrative managed baselines from the manifest.
   235	
   236	   The trusted-path deny inventory is rendered from the static `trusted_paths:` list. Rendering performs no Git object traversal, `git ls-tree` enumeration or tracked-path discovery. Worker-writable refs, replacement refs and objects do not determine the list.
   237	
   238	   Anchored checkout rules use absolute `//` permission patterns. Rendering includes the explicitly listed trusted paths themselves and their descendants. It emits no checkout-wide parent deny that defeats ordinary worktree writes. The separate worktree-configuration denies remain present.
   239	
   240	   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator creates no `executable_worker-write-boundary.py` or replacement PreToolUse path validator.
   241	
   242	   Every direct Git verification introduced or changed by this task follows section 5.14 item 2. It begins with `env -i`, uses the selected absolute Git executable and an explicit `-C`, sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and supplies `-c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always`. Diff and show also use `--no-ext-diff --no-textconv` and `-c core.attributesFile=/dev/null -c core.sshCommand=false`.
   243	
   244	   The private executable-link directory contains only links to selected absolute trusted binaries. Rendering rejects missing bindings, worker-controlled executable paths, shims, empty PATH entries and relative PATH entries. Direct Python invocations use `-I`; PermissionRequest uses the fixed uv invocation in item 3. Hook execution uses the role-specific pinned PATH bindings specified below. The render test asserts that `ruff`, `prettier` and `terminal-browser` resolve under the rendered orchestrator tool PATH on the rendering host and that no entry of that PATH is a shims directory.
   245	
   246	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest` asserts that the rendered list equals the manifest entry after trusted anchor and home expansion. It explicitly asserts the rendered home-path deny patterns `~/.local/share/**` and `~/.local/state/**`, including the application code under `~/.local/share` used by `~/.local/bin` wrappers such as `terminal-browser`. It reads the filesystem of the test's own checkout and asserts that every tracked top-level source path is represented. It invokes no Git command to discover those paths.
   247	
   248	   The inventory fixtures cover files, directories, `.claude` children, the main-local settings file, ordinary worktree writes, both worktree-configuration patterns, an anchor containing spaces and both explicit worklog patterns. Adding a top-level source path without a manifest entry makes the coverage assertion fail. Planted Git environment and replacement-ref fixtures leave rendering unchanged.
   249	
   250	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_leave_agmsg_stores_writable` asserts the rendered deny patterns `~/.agents/skills/agmsg/plugins/**` and `~/.agents/skills/agmsg/db/trusted-plugins` and verifies that the four store directories `db`, `teams`, `run` and `ext-tools` and their descendant fixtures remain writable except that one file.
   251	
   252	3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator user baseline.
   253	
   254	   The existing `home/dot_claude/modify_private_settings.json` continues to render the orchestrator's `~/.claude/settings.json`. That modify script is not imported into the dedicated worker renderer and remains outside `allowed_files`.
   255	
   256	   This existing template's name does not make it administrative managed settings. The new `claude-managed-settings.json` template supplies that separate scope.
   257	
   258	   The orchestrator retains its current user policy content apart from `failIfUnavailable: true`, `onFailure: "block"`, the required interpreter and PATH bindings and alignment of exclusions with the three control-plane entries. Worker-specific Edit denies and restricted worker cache allowances do not enter this baseline. Administrative sandbox requirements apply to the orchestrator as well as workers.
   259	
   260	   Every generated hook entry carries `onFailure: "block"`. Every generated command hook starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before its trusted installed entrypoint, except that this chezmoi template renders PermissionRequest HOME as `HOME="{{ .chezmoi.homeDir }}"`. The prefix re-exports HOME before any HOME-relative entrypoint path. Host-specific interpreter, private-link-directory, anchored-checkout and tool-directory bindings remain in the per-host rendered user settings and guard. The formatter and project-map hooks run through the installed orchestrator-only guard and receive the role-specific pinned PATH specified below. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set without equating baseline coverage with coverage of runtime-added entries.
   261	
   262	   The PermissionRequest command is `/usr/bin/env -i PATH=/usr/bin:/bin HOME="{{ .chezmoi.homeDir }}" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}" <abs uv> run --no-config --no-project --offline --no-cache --python <abs python> --script "{{ .chezmoi.homeDir }}/.local/bin/common/permgate" claude`. The template renders `<abs uv>` and `<abs python>` from the trusted manifest bindings in item 1, shell-quotes each complete path and bypasses permgate's shebang. Permgate has no PEP 723 dependency header and imports only the standard library, so `--offline --no-cache` requires no dependency download and uses no shared uv cache. Its existing `#!/usr/bin/env -S uv run --no-cache --script` shebang stays unchanged for interactive use. This bound invocation applies `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 items 2 and 9; that uncommitted design file is read-only context. Host-specific absolute paths rendered in this chezmoi template are permitted; the tracked `.claude/settings.json` remains portable.
   263	
   264	   Every other rendered hook command, including SessionStart, Stop, delivery and guard invocations, likewise uses absolute bound entrypoints and interpreters and never relies on PATH to select uv, python3, bash or a tool; upstream agmsg env-bash descendants retain the fixed system-PATH binding in item 11.
   265	
   266	   `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy` compares the merged policy with the preceding baseline and accounts for the specified changes. Repeated merging remains idempotent and preserves unrelated settings.
   267	
   268	4. `home/.chezmoitemplates/claude-worker-settings.json` is the dedicated worker user baseline.
   269	
   270	   It renders the static trusted-path Edit denies, the worktree `.claude` and `.mcp.json` Edit denies, retained native merge denials, empty user `excludedCommands`, `allowUnsandboxedCommands: false`, restricted `allowWrite`, no user Herdr socket allowance and `failIfUnavailable: true` for both Darwin and Linux.
   271	
   272	   Its hooks are limited to agmsg delivery. It contains no formatter, project-map, permgate, orchestrator attachment, Herdr state or worker-write-boundary hook. Tracked project hooks and main-checkout local hooks still load and receive the guard described below.
   273	
   274	   Every worker hook entry carries `onFailure: "block"`. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}" AGMSG_RESOLVE_PROJECT=0` before the selected absolute shell interpreter and absolute installed agmsg script path. The prefix also re-exports `AGMSG_STORAGE_PATH` when it is set in the launcher environment. Project resolution from a writable `run/proj.<pid>.project` marker remains disabled, so delivery retains the explicit worker path. Descendants inherit this PATH.
   275	
   276	   The worker baseline does not copy the orchestrator's plugins, credential files or current hook arrays. Hook settings reload during a session, so protection is stated as current configuration rather than startup capture. `CLAUDE_CONFIG_DIR` selects the separate user settings directory while project settings continue to apply within the administrative enforcement scope. [Claude settings reference](https://code.claude.com/docs/en/settings)
   277	
   278	   Worker user settings supply no additional socket or exclusion allowance. Their empty lists cannot remove the shared managed Herdr socket or control-plane exclusions.
   279	
   280	5. `home/.chezmoitemplates/claude-managed-settings.json` supplies the administrative sandbox policy.
   281	
   282	   The rendered policy sets `sandbox.enabled: true`, `sandbox.failIfUnavailable: true` and `sandbox.allowUnsandboxedCommands: false`. The last setting makes sandboxing admin-required. Project and local files cannot add sandbox exclusions, socket allowances or other documented relaxations in this scope. Managed Boolean values prevail over lower scopes. User settings remain a separate trusted scope, and arrays such as exclusions have no general managed-only lock. [Repository settings under an admin-required sandbox](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox)
   283	
   284	   The rendered policy sets `sandbox.filesystem.disabled: false`, `sandbox.enableWeakerNestedSandbox: false`, `sandbox.enableWeakerNetworkIsolation: false`, `sandbox.network.allowAllUnixSockets: false`, `sandbox.network.allowLocalBinding: false` and `sandbox.allowAppleEvents: false`.
   285	
   286	   The rendered `sandbox.excludedCommands` list contains exactly `agmsg-dispatch *`, `herdr-agents *` and `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These are the orchestrator's three control-plane entries. It contains no `gh *`, `git push *` or authenticated-fetch exemption.
   287	
   288	   The rendered `sandbox.network.allowUnixSockets` list contains exactly the trusted home expansion of `~/.config/herdr/herdr.sock`. This allowance is shared by every seat under managed settings. Per-seat removal is unavailable in that scope, and the worker baseline's empty list does not revoke it.
   289	
   290	   Shared control-plane exclusions are also available in worker sessions. The worker execution rule forbids using them to leave the sandbox. The text treats their availability and the socket's host-execution capability as item 0 residuals rather than enforced per-seat separation.
   291	
   292	   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox` asserts the rendered content, exact exclusion and socket lists, trusted home expansion and every required Boolean value.
   293	
   294	   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings` supplies project and local fixtures that disable sandboxing, disable startup failure, enable unsandboxed retries, add exclusions and sockets, enable weaker isolation and widen filesystem writes. The trusted managed render remains unchanged. The test verifies configuration scope and content without presenting a simulated settings merger as runtime enforcement.
   295	
   296	6. `Makefile` adds only the `install-managed-settings` target and its `.PHONY` declaration.
   297	
   298	   The target uses the repository's existing rendering facilities to render `home/.chezmoitemplates/claude-managed-settings.json` into `~/.claude/managed-settings.rendered.json`. The staging path is expanded to an absolute path under the user's home.
   299	
   300	   The target selects `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux and prints the exact command `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` with the actual staging path and detected destination substituted and shell quoting preserved. The printed command is ready for the operator to run.
   301	
   302	   The target performs no sudo call, administrative installation, live settings application, authentication or session restart. The staging file alone does not establish managed enforcement.
   303	
   304	   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo` covers both macOS and Linux, uses a temporary home, verifies the staged JSON and exact printed command with the detected destination, includes a home path containing spaces and asserts that a planted sudo marker remains absent.
   305	
   306	7. `home/dot_claude-worker/modify_private_settings.json` renders `~/.claude-worker/settings.json` from the dedicated baseline.
   307	
   308	   The script follows the existing chezmoi modify-script interface: current content arrives on stdin and the desired settings object is written to stdout. It uses Python's standard library and the same trusted source and home resolution conventions as the existing renderer.
   309	
   310	   Worker permissions, sandbox policy and hooks managed by this renderer replace stale managed values. Permissive old user exclusions, socket allowances, hook commands and shared cache allowances do not survive as additive worker user policy. The script does not read or copy `~/.claude/settings.json`.
   311	
   312	   Rendering handles empty and malformed input through the repository's existing baseline behavior and is idempotent. It neither reads credentials nor initiates authentication.
   313	
   314	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently` exercises repeated deployment in temporary homes. `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks` plants orchestrator hook and plugin markers and verifies their absence.
   315	
   316	8. `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` is installed as `~/.claude/hooks/orchestrator-only.sh`.
   317	
   318	   Chezmoi renders the installed guard per host. Its rendered absolute shebang selects the trusted shell interpreter. The host-specific absolute interpreter paths, private executable-link directory, anchored checkout and tool directories are bound inside this rendered guard and the rendered user settings. The tracked project settings contain none of these paths.
   319	
   320	   The guard compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Equality executes the fixed operation supplied by the caller through the guard's trusted interpreter and anchored-script bindings, subject to the formatter and project-map tool-input check below. Every other launch root exits 0 without executing it. `CLAUDE_PROJECT_DIR` supplies launch identity and never selects an executable.
   321	
   322	   Worker launch roots, sibling worktrees and unrelated checkouts execute no guarded project code. Missing or unresolvable launch-root identity also executes no supplied command. Event cwd does not change the launch-root decision.
   323	
   324	   The guard also binds the formatter and project-map reload to the edited file path from the hook's tool input and its owning repository. When the resolved path is outside canonical `CLAUDE_PROJECT_DIR` or belongs to a worker repository under `.claude/worktrees/`, the guard exits 0 without running the command. Worker-repository configuration, including Prettier JavaScript configuration and ruff settings, is never consumed by an orchestrator hook.
   325	
   326	   The guard preserves argument boundaries, stdin and child exit status. It performs no eval, PATH interpreter lookup or worktree-relative script selection. Its portable caller starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`. The prefix re-exports `HOME` from the launcher environment as `HOME="$HOME"` before any path that uses it and explicitly re-exports the launch identity and the few variables Claude Code documents for hooks. No interpreter or anchored script path is supplied by the tracked settings.
   327	
   328	   The pinned PATH differs by role. Worker-session hooks use `/usr/bin:/bin`. For the orchestrator's formatter and project-map hooks, which the guard runs only in orchestrator sessions, the guard itself sets PATH to a rendered list of absolute tool directories of the trusted root before executing the guarded command. Those directories hold `ruff`, `prettier` and `terminal-browser` and are resolved by the render from the manifest without using mise shims. The formatter and project-map scripts remain outside `allowed_files` and unchanged.
   329	
   330	   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The positive-path case runs the complete rendered command in a subprocess with a fake `CLAUDE_PROJECT_DIR` equal to the anchored checkout and asserts that the guarded script executed while preserving its arguments and status. A second case runs the complete rendered command with a worktree `CLAUDE_PROJECT_DIR` and asserts that the guarded script did not execute. A planted `BASH_ENV` in the outer environment remains unexecuted in both cases. Formatter and project-map reload cases keep `CLAUDE_PROJECT_DIR` anchored and supply hook tool input for an outside file and a worker-repository file under `.claude/worktrees/`; both exit 0 with command and planted configuration markers absent. Matching anchored-file inputs run both commands normally. The guard tests execute the portable HOME-relative hook command against separately rendered per-host guards, assert the `HOME="$HOME"` re-export and verify that interpreter and anchor selection occurs only inside the rendered guard. Changing `CLAUDE_PROJECT_DIR` never changes the selected executable.
   331	
   332	9. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.
   333	
   334	   This tracked file is not a chezmoi template and remains portable across hosts. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`, and the clean environment re-exports the launcher's HOME before any path that uses it. The file names no interpreter, anchor path, private links directory or host-specific tool directory.
   335	
   336	   Host-specific absolute bindings live only inside the per-host rendered guard and rendered user settings, including the orchestrator user template's bound PermissionRequest invocation. The guard binds the selected operation to its absolute interpreter and anchored script path. Contextdb commands do not invoke bare `python3` or select `.claude/hooks` from a worker checkout. The Stop gate does not invoke bare `bash` or a worker checkout's `scripts/agent-stop-gate.sh`. `CLAUDE_PROJECT_DIR` never selects an executable.
   337	
   338	   Every hook entry carries `onFailure: "block"`. Existing event functions remain available to the anchored orchestrator. They are no-ops in worker sessions because the guard rejects their launch roots.
   339	
   340	   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure` traverses every event, matcher and command entry. It rejects unguarded commands, missing failure policy, missing `/usr/bin/env -i` prefixes with the specified HOME re-export, interpreter or anchor paths in the tracked file and worker-selected executable paths. Render fixtures use distinct homes and anchors and assert that the tracked commands stay identical while the guard and worker settings receive their own host bindings.
   341	
   342	10. `home/dot_local/bin/common/executable_herdr-agents` supplies the dedicated worker configuration at the actual worker launch boundary.
   343	
   344	    Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. This value reaches the actual worker process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.
   345	
   346	    Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a conflicting caller Claude configuration directory. This task introduces no worker gh configuration directory, gh templates or credential-separation claim.
   347	
   348	    Every worker launch exports `UV_CACHE_DIR=<absolute-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<absolute-worktree>/.uv-cache/python`. Both worker kinds receive values derived from the selected canonical worktree. Caller-provided values do not replace them.
   349	
   350	    The launcher stops writing Claude worker delivery hooks and merge denials into worktree-local `.claude/settings.local.json`. It renders the worker delivery hooks and native merge denials into `~/.claude-worker/settings.json`, the user-level settings file selected for that directory.
   351	
   352	    Before every Claude worker start, the launcher also migrates the legacy worktree-local file. Claude Code loads the worktree's own `.claude/settings.local.json` alongside the main checkout's local settings, so a previously generated delivery entry there would stay effective with its unsanitized environment and PATH-resolved interpreter. The launcher removes every managed delivery hook entry it previously wrote from `<worktree>/.claude/settings.local.json`, keeps that file's unrelated entries, and refuses to start the worker while a command hook it did not write remains there, naming the entry. The effective hook set is asserted across the three files Claude Code loads for a linked worktree (worker user settings, the main checkout's local settings, the legacy worktree-local file) with a fixture holding a previously generated unsanitized entry: `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks` is red at the base and green on the final head.
   353	
   354	    Before every Claude worker start, managed worker delivery entries are regenerated from trusted inputs. An existing delivery match does not skip preparation. Stale managed commands are replaced, unknown command hooks are not promoted into the trusted delivery set and the effective delivery set contains no duplicate managed invocation.
   355	
   356	    The launcher also regenerates its managed hooks in the main checkout's `.claude/settings.local.json`. Every local agmsg delivery and orchestrator attachment command that it writes runs through the installed orchestrator-only guard. The existing permissions object and unrelated non-hook settings remain stored. Their effective sandbox interpretation follows the administrative managed policy.
   357	
   358	    Every command hook in both `~/.claude-worker/settings.json` and the main checkout's `.claude/settings.local.json` starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"`. Worker user settings contain their per-host rendered absolute interpreter and script bindings. Main-local commands invoke `"$HOME/.claude/hooks/orchestrator-only.sh"` with fixed operation identifiers, leaving host-specific executable bindings inside the rendered guard. The prefix removes inherited `BASH_ENV` before Bash starts and explicitly re-exports the launch identity and documented hook variables. Agmsg delivery prefixes additionally re-export `AGMSG_RESOLVE_PROJECT=0` and `AGMSG_STORAGE_PATH` when the latter is set in the launcher environment, so the clean environment does not re-enable project resolution from the writable `run/proj.<pid>.project` marker. Every entry carries `onFailure: "block"`. Main-local hooks loaded by a worker session execute no guarded payload.
   359	
   360	    Worker settings retain existing native merge denials. They add no user excluded commands, Herdr socket allowance, unsandboxed requests or orchestrator hooks. Shared managed exclusions and socket access remain effective.
   361	
   362	    Codex launches retain their existing `--sandbox workspace-write` and `--ask-for-approval never` arguments unchanged. This task changes no Codex worker profile or network-policy source and adds no network-policy test.
   363	
   364	    The retained Codex Git grant permits shared `.git/objects`, `.git/refs`, `.git/logs` and the worker's administration directory. It does not authenticate local ledger content and is not represented as a host security boundary.
   365	

**Noticing time elapsed**
codex
The text explicitly treats same-user credential access, shared control-plane exceptions, and agmsg store-selected code as residual risks. I’m checking whether the remaining controls bind actual execution, especially hook descendants, executable resolution, and formatter configuration.

exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '366,490p'" in ~/Workspace/dotfiles
 succeeded in 2ms:
   366	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches` covers both worker kinds and all launch routes. `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_repeated_worker_start_replaces_stale_managed_hooks` covers repeated preparation.
   367	
   368	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_launch_adds_no_unsandboxed_route` checks that worker launch construction adds no outside-sandbox command route, worker user exclusions or socket allowances and retains native merge denials. It separately records the shared managed exceptions and does not claim that empty user arrays remove them.
   369	
   370	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks` asserts that worker hooks are written to worker user settings, worker preparation writes no worktree-local settings file and main-local agmsg and attachment hooks execute no payload under a worker launch root. An anchored orchestrator invocation still reaches the expected fixture payloads.
   371	
   372	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_settings_hook_has_system_path_prefix` exhaustively traverses both settings files after initial preparation and repeated starts. It asserts the literal `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix on every command hook, checks the split between absolute bindings in rendered worker settings and HOME-relative main-local guard calls, and asserts that a planted `BASH_ENV` in the hook's inherited environment does not run. The planted-`BASH_ENV` case is red against the current PATH-only form. The test also asserts `AGMSG_RESOLVE_PROJECT=0` in every agmsg delivery prefix and preservation of `AGMSG_STORAGE_PATH` when set in the launcher environment. It invokes the delivery resolver through the rendered prefix with an explicit worker path and a conflicting writable `run/proj.<pid>.project` marker and asserts that the resolver retains the explicit worker path.
   373	
   374	11. `home/dot_local/bin/common/executable_herdr-agent-state.sh` provides the repository-owned Herdr state helper installed as `~/.local/bin/common/herdr-agent-state.sh`.
   375	
   376	    The currently installed `~/.claude/hooks/herdr-agent-state.sh` is generated by Herdr and is not a tracked source in this repository. Its bare `python3` descendant is not retained as a trusted worker hook. The repository-owned helper preserves the required state-reporting function and receives its absolute Python interpreter through the rendered invocation.
   377	
   378	    Every hook command reaches a selected absolute interpreter and absolute script path through trusted installed bindings. The tracked settings name only the HOME-relative guard and fixed operation identifiers. Host-specific interpreter and anchor bindings reside inside the per-host rendered guard or rendered user settings. Repository-owned shell descendants use absolute shebangs or explicit absolute shell invocations. Direct Python descendants use the selected absolute interpreter with `-I`; PermissionRequest uses the bound uv/Python invocation in item 3.
   379	
   380	    Upstream agmsg scripts retain their `/usr/bin/env bash` shebangs and direct calls to other installed agmsg scripts. The `PATH=/usr/bin:/bin` supplied by the delivery hook's `/usr/bin/env -i` prefix propagates to those descendants, so their Bash resolution uses the system directories without reaching host shims. The installed upstream files are neither edited nor vendored.
   381	
   382	    The delivery inventory names `~/.agents/skills/agmsg/scripts/session-start.sh`, `~/.agents/skills/agmsg/scripts/session-end.sh`, `~/.agents/skills/agmsg/scripts/check-inbox.sh`, `~/.agents/skills/agmsg/scripts/identities.sh` and every additional delivery descendant actually reached.
   383	
   384	    The inventory records source ownership, installed path, caller, entrypoint interpreter and inherited PATH for each reached script. Binding only the first command does not establish descendant coverage.
   385	
   386	    The inventory separately records the current `storage.sh` route from writable team configuration to driver sourcing. A `drivers.partition` value such as `../../../db/payload` can select a planted driver file during unsandboxed delivery. Fixed PATH does not mitigate that selection. The upstream fix belongs to `dotfiles-T133-agmsg-hardening-a01` as recorded in the acceptance record's ownership section.
   387	
   388	    No worker hook added by this task introduces store-derived driver sourcing beyond the behavior of the currently installed agmsg scripts. This task neither implements nor claims the upstream validation.
   389	
   390	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters` executes the fixture hook routes with planted Python and Bash shims. It includes a directly executed descendant with an `/usr/bin/env bash` shebang, checks descendant markers and records actual interpreter identities and inherited PATH. Capturing launcher command strings alone does not satisfy this test. Its result does not close the store-driver residual.
   391	
   392	12. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the Worker Playbook step 4 sentence that lists outside-sandbox worker commands.
   393	
   394	    The replacement sentence is: “Every worker command, including gh, git push and authenticated git fetch, runs inside the worker's sandbox; no worker command runs outside it.”
   395	
   396	    This sentence governs worker execution. Historical TLS, keyring, artifact-writing and delivery exceptions elsewhere in the playbook provide no authorization to leave the sandbox. Shared managed control-plane exceptions provide no worker authorization either. An unavailable operation produces a blocked PONG with its exact command and boundary.
   397	
   398	    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox` checks the replacement and removal of the former three-command exception sentence.
   399	
   400	13. `.gitignore` adds only `.uv-cache/`.
   401	
   402	    Section 5.14 item 9 fixes trusted orchestrator consumers to `UV_CACHE_DIR=<anchored-checkout>/.agents/worklog/uv-cache`, places managed Python installations beneath that cache and uses `--offline`. Those consumers execute no dependency content from worker caches, shared uv caches or mise caches. Their owning hardening tasks implement the consumer changes.
   403	
   404	    This task's static deny inventory explicitly protects both `.agents/worklog/**` and `.agents/worklog/uv-cache/**` beneath the anchored checkout. Their gitignored status does not remove them from the inventory.
   405	
   406	    This task's hooks use standard-library Python and absolute shell interpreters; PermissionRequest alone invokes the existing dependency-free permgate through the absolute uv/Python binding with `--offline --no-cache` specified in item 3. The existing `.agents/worklog/` ignore covers the orchestrator cache.
   407	
   408	14. The five allowed test modules reuse existing render, merge, fake-launcher and temporary-HOME fixtures.
   409	
   410	    Tests are written before implementation and retain identified base-failure and implementation-success evidence. A missing new entrypoint supplies its baseline failure.
   411	
   412	    Worker settings tests cover both platforms, exact static manifest correspondence, current-checkout filesystem coverage, every protected path category, directory targets, descendants, both worklog patterns, ordinary worktree writes, the worktree `.claude` and `.mcp.json` denies, writable agmsg stores, stale settings and the absence of the removed boundary hook.
   413	
   414	    Managed settings tests cover the exact rendered policy, conflicting project and local sandbox relaxations, shared control-plane exclusions, shared Herdr socket access and staging without privileged execution. They distinguish worker user settings from the effective shared policy.
   415	
   416	    Path fixtures cover symlink components and filesystem case aliases. They verify inventory and configuration identities without presenting a simulated permission matcher as proof of Claude runtime enforcement.
   417	
   418	    Hook tests cover every generated and tracked entry's failure policy, worker user settings, guarded main-local settings, the `/usr/bin/env -i` prefix with explicit hook-variable re-exports, complete rendered-command positive and worktree-negative cases, role-specific pinned PATH bindings, suppression of a planted inherited `BASH_ENV` and actual descendant execution. They distinguish synchronous policy hooks from background delivery and post-action events.
   419	
   420	    `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision` renders the complete orchestrator and worker user hook sets and the guard in a temporary HOME, reusing the tracked and launcher-generated hook fixtures for SessionStart, Stop and delivery. For every command hook, expand only the fixture's known HOME and hook-variable bindings, parse with `shlex`, and assert that the first word is an absolute path to an existing executable file; for `/usr/bin/env -i`, also assert the first word after all environment assignments is such a file. Check the guard's rendered shebang, interpreter and fixed-operation executable bindings too, so no bare uv, python3, bash or tool survives. In the same test, install the unchanged real permgate source and a minimal deterministic fixture policy beneath that temporary HOME, then execute the rendered PermissionRequest command with the actual bound uv and Python binaries, outer `PATH=/usr/bin:/bin` and a fake PermissionRequest payload matching the fixture policy. Assert exit 0, parse stdout and assert `hookSpecificOutput.hookEventName == "PermissionRequest"` and the expected `hookSpecificOutput.decision.behavior`; empty stdout, exit 127 or `env: uv: No such file or directory` fails. A fake uv or permgate that merely prints a decision does not satisfy this test. Record red-then-green evidence for this selector.
   421	
   422	    `onFailure: "block"` requires Claude Code v2.1.295 or later and has no enforcement effect on background hooks or the documented excluded events. [Claude hook failure reference](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)
   423	
   424	    Tests create no identities, initiate no login and access no real credential store. No fixture result is represented as proof of credential isolation, live managed enforcement or upstream agmsg hardening.
   425	
   426	15. `.orchestration/dotfiles-T133-worker-write-boundary-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence.
   427	
   428	    The report maps each of the third C-80 review's five findings, fourth C-80 review's six findings and fifth C-80 review's three findings to the revised mechanism, its tests and its remaining residual or owning task. It distinguishes policy configuration from live enforcement and deployment.
   429	
   430	16. `scripts/validate-agent-assets.py` is the consolidated validator scope for every existing check affected by this task's rendered Claude settings, hooks, sandbox and exclusions, with their corresponding fixtures and assertions.
   431	
   432	    The Linux and macOS `excludedCommands` checks at base lines 349-355 become one exact ordered-list check on both platforms: `agmsg-dispatch *`, `herdr-agents *`, `{{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *`. The last entry becomes `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *` after chezmoi expansion. Neither platform permits `gh *` or an additional, missing, reordered or substituted exclusion. The existing non-empty-string list validation remains. This follows the normative design sentences quoted above from `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 (C-86, C-88); the path is context only.
   433	
   434	    The Claude managed-user-settings hook-wiring check in `validate_model_profile_assets` at base lines 1193-1200 becomes structural. Inspect command hooks under `hooks.PermissionRequest`, not serialized text from other events, and parse the command with `shlex` without executing it. Require exactly the sanitized prefix from item 3 with HOME equal to the absolute home rendered from `{{ .chezmoi.homeDir }}`, followed in order by an absolute uv path whose basename is `uv`, `run`, `--no-config`, `--no-project`, `--offline`, `--no-cache`, `--python`, an absolute Python path matching the trusted rendered interpreter binding, `--script`, the absolute installed permgate path whose basename is `permgate`, and `claude`, with no further words. The uv and permgate paths also match their trusted rendered bindings. Compare parsed words so quoting of a bound path containing spaces is preserved; do not require a literal `permgate claude` substring. Missing or malformed commands, an incomplete or altered prefix, an extra environment assignment, relative or substituted executable paths, missing, reordered or additional uv flags, a different script or argument, a direct shebang-based permgate call, a guard selector, and trailing words or shell operations fail. The generated PermissionRequest command and its assertions conform to this bound-interpreter contract; the worker's current `orchestrator-only.sh permgate` selector does not satisfy it. Parsed tokens establish command structure; the render/runtime test in item 14 establishes that the executable binding actually runs under the sanitized PATH. The existing refusal of `ccgate` anywhere in the Claude hooks remains. The Codex PermissionRequest and `permgate codex` check at base lines 1189-1190, and its ccgate refusal, are unchanged because this task changes no Codex hook design.
   435	
   436	    The complete inventory of the surrounding checks is retained: `validate_claude_settings` still checks the schema, interactive model and effort, absence of the redundant model suffix and legacy type checker, the `format-edited-files.py` operation marker (still present in the guarded command), permission-allow list shape, sandbox policy, disabled unmanaged plugins and the Crit rule. `validate_claude_sandbox` still requires enabled and auto-allow booleans, a Boolean `failIfUnavailable` (the render tests separately require true), all agmsg and Codex writable roots, valid extra write paths, allowed hostname and telemetry restrictions, the platform Mach-service allowlist, no allow-all Unix sockets and valid socket paths; only its exclusion policy changes. `validate_hook_composition` retains duplicate-command rejection, permgate-first ordering, synchronous timeout budgets and the SessionStart `herdr-agent-state.sh` marker and order. These markers remain in the rendered commands, so none is deleted or weakened to accommodate the prefix. Generated-output freshness, manifest home-path checks, tracked project-settings portability, permgate policy and profile-asset checks and the orchestration home-path/secret scan remain unchanged. New worker-user and administrative-managed-policy outputs retain their exact content checks in the already named render tests; the orchestrator user sandbox validator is not applied to worker empty exclusions.
   437	
   438	    In `tests/unit/test_validate_agent_assets.py`, the two already authorized cases in `ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form` remain in scope: macOS gh exclusion and Linux extra exclusion. The shared `ValidateAgentAssetsTest::valid_claude_sandbox` fixture gains the exact three-entry exclusions above. Its callers `test_claude_sandbox_accepts_manifest_symmetric_settings`, `test_claude_sandbox_rejects_each_broken_rule`, `test_claude_sandbox_requires_extra_codex_writable_roots`, `test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs` and `test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs` retain their checks and reach the rule each intends to test. The literal-form fixture in `test_hook_composition_requires_permgate_first` follows the sanitized hook while retaining its ordering failure. Add `ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate` with valid quoted-path cases and negative cases for the structural contract and retained ccgate refusal. Keep red-then-green evidence and run `uv run python -m unittest tests.unit.test_validate_agent_assets -v` to green on the final head.
   439	
   440	    The other tests carrying the literal hook form are `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_hooks_use_installed_permgate_paths`, `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_claude_settings_use_interactive_profile_with_permgate`, `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_managed_permgate_replaces_stale_current_ccgate_hook`, `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_permission_merge_preserves_unrelated_current_hooks` and `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_permission_merge_preserves_custom_hook_in_mixed_entry`. Their hook fixtures and assertions are in scope together: production-hook expectations use the parsed prefix, bound absolute uv/Python invocation with the fixed flags, installed permgate script and sole `claude` argument; synthetic renderer and merge-only inputs may remain synthetic where they assert no production command form. Preserve their model, stale-ccgate-removal and custom-hook-preservation assertions and the unchanged Codex assertion. No validator pin or literal-form fixture named here is left outside scope.
   441	
   442	The source measurement is 674 changed lines against the unchanged 700-line cap, guard included, and the test measurement is 905 changed lines against the unchanged 950-line cap (the worker's 2026-10-19T08:21:22Z evidence at local head 55c125a1 on main 69dccca9). The valid_claude_sandbox fixture adds about 10 changed test lines, giving about 915; the new `test_rendered_hooks_bind_executables_and_permgate_returns_decision` contributes its measured changed-line count on top (`905 + about 10 + new render/runtime-test lines`), before the remaining structural-hook checks and literal-form fixture/assertion adjustments. The unchanged test cap leaves about 35 lines for that test and all remaining test changes together; those changes must fit the remaining source and test margins, and the worker re-measures the final diff rather than presenting this estimate as a final-head result. No test-cap increase is asserted without a measured sum requiring it.
   443	
   444	The guard source is `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl`: chezmoi renders the guard from its .tmpl source with the per-host absolute interpreter, anchored-checkout and tool-directory paths at apply time (a plain `executable_` source would be copied without expansion), and the render test renders the template with the test host values and asserts the paths it contains.
   445	
   446	The doc test `tests/unit/test_agmsg_orchestration_docs.py` asserts the exact step 4 sentence this task rewrites (lines 200-201 at the base); the assertion follows the new sentence, nothing else in that module changes; PR #427 (P1-8) edits the same module and merges before this pull request, which rebases onto it before its first push.
   447	
   448	## Out of scope
   449	
   450	The Codex worker profile change `sandbox_workspace_write.network_access=true` belongs to the separate task `dotfiles-T133-codex-worker-network-a01` for a Claude seat. This task contains no implementation, threat row or test for that change. This Codex seat edits no Codex-boundary source. The operator step for the deterministic Codex permgate policy remains named below.
   451	
   452	The worker-write-boundary Python hook, its hook entries and `tests/unit/test_worker_write_boundary.py` are dropped. The gh-trusted wrapper remains dropped. The worker gh configuration directory, its templates and the dedicated-identity implementation are removed from this task.
   453	
   454	D-024-23 establishes that `GH_CONFIG_DIR` does not separate same-macOS-user Keychain access. A separate OS user or host is required for prevention of worker-initiated merges. Future P1-16 remains the operator's decision. This task implements no credential-separation substitute.
   455	
   456	The permission guard and merge gate remain P1-14 a05's work. P1-14 a05 and P1-6 implement the regime rule that approvals and gate evidence of record come from GitHub at a SHA through its API inside the sandbox. The GitHub boundary is detection, not prevention.
   457	
   458	For the committed approval ledger, the regime obtains the commit SHA returned by `git ls-remote origin refs/heads/main` and reads `gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. The consuming implementation reads the API response's file content at that exact SHA. It does not fall back to local files, local refs or local object traversal.
   459	
   460	A working-copy decision remains a proposal until its record PR reaches main. This task writes no approval row and implements no local-object substitute for GitHub authority. Shared credentials can still authorize a worker-initiated merge. P1-11 owns the next-records-PR regime check for missing acceptance or gate evidence under section 5.14 item 0's detection rule.
   461	
   462	The upstream agmsg driver-selection fix belongs to `dotfiles-T133-agmsg-hardening-a01`. Its recorded scope validates the `drivers.partition` driver name as an allowlisted basename without path separators before sourcing and supplies an adversarial red-then-green test. This task leaves the shared stores writable and records the current sourcing route as a residual. The ownership section identifies that upstream task as a task to be written; this text does not claim that its fix or test exists.
   463	
   464	Permgate code and deterministic policy remain the operator's responsibility. The worker prepares the operator step that stops the Codex permgate policy from approving sandbox escapes. The worker performs no live policy edit or escape probe.
   465	
   466	The operator logs into Claude once with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected. The Claude Keychain entry is keyed to that directory. This Claude login does not authenticate or isolate gh.
   467	
   468	Administrative installation of `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux is the operator's step. The worker implements rendering, staging and the printed installation command without running sudo or installing live managed settings.
   469	
   470	The documented file-tool checks reduce symlink redirection risk. A same-UID process can race filesystem changes, alter host-local state or execute outside a seat sandbox. The remaining interval between permission checks and path consumption is a residual under section 5.14 item 0. This text makes no claim that the worker could already write every redirected target directly.
   471	
   472	The managed Herdr socket allowance stays available to every seat. Per-seat socket removal is unavailable in that shared scope. Shared control-plane exclusions, socket RPC, hooks, approved MCP processes and other processes outside every seat sandbox retain their stated host trust. The configuration is not represented as same-UID adversarial isolation.
   473	
   474	`onFailure: "block"` supplies runtime failure behavior where Claude supports it. Python exit-status tests do not establish timeout handling by the runtime. Background hooks and events on which the field has no effect perform no security enforcement in this design.
   475	
   476	Consuming-helper snapshots, reservation locks, the common trusted-execution test helper and orchestrator review-worktree relocation remain with their owning hardening tasks. Codex writable-root grants remain unchanged.
   477	
   478	In `scripts/validate-agent-assets.py`, the consolidated policy-check changes enumerated in item 16 are in scope; unrelated validator behavior remains out of scope. In `tests/unit/test_validate_agent_assets.py`, the two exclusion cases, `valid_claude_sandbox`, the named hook fixture and structural-hook cases in item 16 are in scope; unrelated tests remain out of scope. The named literal-form assertions and fixtures in the already allowed generator and merge test modules are included as item 16 specifies.
   479	
   480	The worker edits neither `.orchestration/decisions.tsv` nor other tasks' canonical texts, evidence or acceptance records, apart from the explicitly named deletion of the predecessor's task-file copy. It performs no authentication change, keyring mutation, ruleset mutation, administrative installation, live settings application, global installation, operator restart or merge.
   481	
   482	## Check
   483	
   484	`make render-check` and `make validate-agent-assets` pass. The task's own files pass the `make format` flags: `shfmt -i 4 -sr --diff`, `ruff format --config ruff.toml --check` and `prettier --check`.
   485	
   486	The clean base `205fe85c` has an inherited formatting failure on 12 out-of-scope files: ten archived task shell sources, `project-map-reload.sh` and `brew.bats`. The inherited failure is reproduced against that unchanged base and disclosed in `validation.md` with its exact output and per-file exit statuses. This clause authorizes no out-of-scope repair.
   487	
   488	Shellcheck and shfmt cover the changed shell sources, including the launcher, orchestrator-only guard and repository-owned Herdr state helper. Added or changed shell comments use English shdoc-compatible annotations. Changed Python receives the repository's Python formatting and lint checks.
   489	
   490	`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` is green. The validation record contains every named red-then-green selector and the complete final module run.

exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md task_sha256=bf5881da1c1c289ae3f4fb26cdd94b8a9d01496af0beab448d0cfa4a450c946b deadline=none done_signal=AGMSG-RESULT note=a010:plan-024-P1-15(the-worker-write-boundary;design-5.14-items-0-10;the-text-passed-its-9th-pre-dispatch-security-review);fresh-branch-from-origin/main-b22a5580;your-#420-branch-stays-untouched-for-a05-which-follows-this-merge;security-true:task-level-audit-and-security-review-on-the-final-head;the-operator-steps-named-in-the-text(managed-settings-sudo-install,worker-directory-login,permgate-codex-rule,make-update)are-not-yours;no-@codex-review-comment;single-gh/git-write-commands;one-pre-push-review-round-at-most"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "searches": [],
  "task": "dotfiles-T133-worker-write-boundary-a01"
}
---

# Acceptance: dotfiles-T133-worker-write-boundary-a01 (plan 024 P1-15: the worker write boundary; D-024-17/19/20)

- text: review-profile design 03:18Z (prompt `.agents/worklog/orchestrator-glue/p115-a01-design-prompt.md`); checker OK; 14 files; not dispatched.
- 2026-10-19T03:24:11Z: C-80 review of the text (`.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md`): `Verdict: incorrect`, seven P1, one P2: (1) the gh wrapper forwards argv verbatim, so `gh repo clone … -- --config core.sshCommand=<exe>` runs worker code outside the sandbox → the wrapper allows an explicit subcommand list and refuses `--` passthrough and config-carrying forms; (2) a bash wrapper reads BASH_ENV before `env -i` (probe confirmed) → the wrapper is Python under an absolute `-I` interpreter path rendered from the trusted root; (3) project hooks execute the worktree's `.claude/hooks/contextdb_hook.py` through bare `python3` and the format hooks resolve tools through shims → worker seats run no project hooks (a factual check of the settings switch is pending with the Claude Code docs); (4) Codex workers share `.git/objects` and `.git/refs` writes (herdr-agents:439), so `origin/main` can be replaced after a fetch → design 5.14 item 8 now binds the committed ledger to the sha `git ls-remote origin refs/heads/main` returns (amended 03:2xZ); (5) `git ls-tree` enumeration needs the sanitized git environment; (6) the reviewer states Edit deny rules also enter the Bash sandbox configuration, which would block the orchestrator's sandboxed record writes under `.orchestration/**` → a factual check pending; (7) `failIfUnavailable: false` lets a seat run unsandboxed when Linux dependencies are missing → `true` for worker seats; (8) P2: symlink and case-alias identity tests missing. Five facts are being verified against the Claude Code documentation before the revision (excludedCommands matching, hooks switches and capture, Edit denies vs sandbox, failIfUnavailable, Edit rule scope and path forms).
- 2026-10-19T03:2xZ: Claude Code documentation facts (the claude-code-guide agent, code.claude.com/docs sandboxing, hooks, permissions pages): excludedCommands match the whole call and every chained sub-command must match; `disableAllHooks` exists but no project-only switch; hooks are not captured at start (a file watcher applies edits); Read/Edit deny rules merge into the sandbox filesystem configuration (so an Edit deny on `.orchestration/**` would block the orchestrator's sandboxed record writes); `failIfUnavailable` is fail-open by default; `Edit(path)` rules cover Write/MultiEdit/NotebookEdit, path forms `//abs`, `~/`, project-relative, deny wins. Consequence (5.14 item 1 amended): the Claude-seat boundary is a user-level PreToolUse hook keyed on the session cwd (worktree sessions: deny file-tool writes outside the cwd and inside `<cwd>/.claude/**`, `<cwd>/.mcp.json`), not Edit deny rules; `failIfUnavailable: true`; the gh wrapper is Python under an absolute `-I` interpreter with a subcommand allowlist; the committed ledger is read at the `git ls-remote` sha.
- 2026-10-19T03:35:17Z: the revised P1-15 text (prompt `p115-a01r-redesign-prompt.md`, 320 lines) installed: the Claude-seat boundary as the user-level PreToolUse hook `executable_worker-write-boundary.py` (session-cwd classification, canonical target checks), `failIfUnavailable: true`, the Python `-I` gh-trusted wrapper with a subcommand allowlist, the committed ledger at the ls-remote sha, per-seat caches; checker OK; the second C-80 review started 03:38Z.
- 2026-10-19T03:42:19Z: C-80 second review of the P1-15 text (`…-text-security-67415f5.md`): `Verdict: incorrect`, seven P1: the hook classifies by the mutable event cwd (a worker can cd out) → classify by CLAUDE_PROJECT_DIR; project hooks execute worker-writable scripts (`scripts/agent-stop-gate.sh`, `.claude/hooks/*.py`, PATH-resolved prettier with worker config) → hooks move out of the tracked `.claude/settings.json` into generated local settings, worker seats get a minimal trusted hook set; `python -I` does not neutralize LD_PRELOAD on Linux for the excluded wrapper → the outside-sandbox gh path is abandoned if gh can run inside the sandbox (CA trust experiment 03:4xZ); `gh pr create` runs git against the caller repository without the git controls → moot when gh is sandboxed; `refs/replace` redirects `git show <sha>` → `--no-replace-objects` (5.14 item 8); a worker's own sandboxed background child can swap a validated path before the unsandboxed file-tool write → stated as the residual it is; the hook lacks a failure policy → every error path exits 2 (fail-closed) with tests.
- 2026-10-19T03:45:06Z: probe from the orchestrator seat inside the Claude sandbox: `gh api repos/mryfmo/dotfiles --jq .name` → `dotfiles` (the sandbox proxy is a CONNECT proxy without TLS interception; the keychain token was read). The 2026-10-1x memory "gh inside the sandbox fails TLS" does not hold today. Consequence (5.14 item 10 amended, D-024-17 revised): worker seats run gh inside the sandbox, their excludedCommands are empty, the wrapper design is dropped (it cannot close LD_PRELOAD or argv passthrough); Codex seats get network inside their sandbox and permgate stops approving escapes (the permgate part is the operator's).
- 2026-10-19T03:53:27Z: the round-3 P1-15 text (prompt `p115-a01r2-redesign-prompt.md`, 333 lines) installed: CLAUDE_PROJECT_DIR classification, the orchestrator-only guard for project hooks (.claude/settings.json joins), no unsandboxed worker command (gh * leaves excludedCommands, Codex network inside the sandbox, the permgate codex rule as the operator step), --no-replace-objects at the ls-remote sha, fail-closed hook (exit 2), the worker race stated as a residual; checker OK; the third C-80 review started 03:54Z.
- 2026-10-19T03:58:10Z: C-80 third review of the P1-15 text (`…-text-security-ecc7ab5.md`): `Verdict: incorrect`, five P1: (1) a sandboxed worker can swap an allowed directory for a symlink after the hook validated, so the unsandboxed file tool overwrites a trusted path (the race is an escape, not a self-harm); (2) the writable object database defeats sha pinning: a replaced intermediate tree object redirects `git show <sha>:path` to an attacker blob (tree traversal does not re-hash intermediate objects); (3) hook descendants still resolve `python3` and `env bash` through shims (herdr-agent-state.sh, delivery scripts); (4) the Herdr unix socket in the worker sandbox lets a sandboxed client request host execution (`pane run`) through the server; (5) a hook timeout or kill is fail-open unless the per-hook `onFailure: "block"` (Claude Code ≥ 2.1.295) is set.
- design conclusion (03:5xZ, pending two fact checks): three text rounds show the host is not a security boundary between seats that share one OS user; the regime's hard boundary is GitHub (protected main, required checks, the merge by the orchestrator's identity), and inputs that must resist a malicious worker (the approval ledger, the gate's evidence of record) are read from GitHub at a sha through the API inside the sandbox, never from local files or the local object database; host-local controls target accidental and injected damage and are stated as such. The per-seat mechanism that makes worker-specific policy possible at all is a separate `CLAUDE_CONFIG_DIR` for worker seats (own settings: no excluded commands, no Herdr socket, minimal trusted hooks with absolute interpreters and `onFailure: block`, Edit denies on trusted paths, failIfUnavailable true); the facts (credentials with a second config dir; onFailure; sandbox per config dir; symlink resolution of file-tool paths) are being verified against the documentation.
- 2026-10-19T04:09Z: the round-4 P1-15 text (prompt `p115-a01r3-redesign-prompt.md`, 373 lines) installed: the 5.14 item 0 threat model opens the Goal; Claude worker seats under CLAUDE_CONFIG_DIR=~/.claude-worker rendered from a new template (Edit denies on trusted paths with symlink coverage, no exclusions, no Herdr socket, restricted allowWrite, failIfUnavailable, minimal hooks with onFailure block); project hooks behind the orchestrator-only guard; the ledger read through the GitHub API at the ls-remote sha; hook descendants with absolute interpreters (herdr-agent-state.sh joins); checker OK; the fourth C-80 review started 04:12Z.
- 2026-10-19T04:15:38Z: C-80 fourth review of the P1-15 text (`…-text-security-8d42532.md`): `Verdict: incorrect`, six P1: (1) workers share the orchestrator's gh credential, so a worker can merge through the API inside the sandbox (GitHub cannot distinguish seats) → D-024-22: a dedicated worker GitHub identity outside the ruleset bypass list (operator step); (2) the deny inventory from `git ls-tree` trusts the writable object store (replace refs) → a static rendered list; (3) the orchestrator cache `.agents/worklog/uv-cache` is missing from the inventory → listed; (4) `~/.agents/**` deny conflicts with the agmsg store writes → a narrower list; (5) linked-worktree sessions load the main checkout's `.claude/settings.local.json` (documented), so worktree-local worker settings are not read and the orchestrator's local hooks run in worker sessions → the guard covers them and worker hooks live in the worker config dir; (6) upstream agmsg scripts carry `/usr/bin/env bash` shebangs → the hook command pins PATH=/usr/bin:/bin. Design 5.14 items 0 and 1 amended; round 5 of the text follows.
- 2026-10-19T04:22:08Z: the round-5 P1-15 text (prompt `p115-a01r4-redesign-prompt.md`, 439 lines) installed: the worker gh identity (D-024-22) as a Files item with the worker gh configuration directory and the operator steps; a static `trusted_paths` inventory in the manifest; narrow home-path denies that leave the agmsg store writable; worker hooks in the worker configuration directory because linked-worktree sessions load the main checkout's settings.local.json; the orchestrator's local hooks behind the guard; PATH=/usr/bin:/bin pinned on every hook command; "reduces" wording where item 0 applies; checker OK; the fifth C-80 review started 04:22Z.
- 2026-10-19T04:25:41Z: C-80 fifth review (`…-text-security-08e6ac7.md`): `Verdict: incorrect`, three P1 (converging from seven): (1) GH_CONFIG_DIR separates configuration, not Keychain access: gh keys credentials by host and user, so a same-UID worker reads the orchestrator token → D-024-23: credential separation needs a separate OS user (future P1-16); the GitHub boundary is detection (regime main-push check), stated as such; (2) the agmsg store every seat writes also selects executables: a team's `drivers.partition` path traversal makes storage.sh source a planted file during unsandboxed delivery → an upstream agmsg hardening task (row recorded) and a stated residual; (3) sandbox restrictions in user settings are overridable by project/local settings → the enforcement scope is managed settings (operator `sudo` step) and the worker denies cover `<worktree>/.claude/**` and `.mcp.json`. Design 5.14 items 0 and 1 amended; round 6 follows.

## Owned by dotfiles-T133-agmsg-hardening-a01 (a task to be written; upstream agmsg)

- `text-security:08e6ac7:2` store-driver-traversal: `~/.agents/skills/agmsg/scripts/lib/storage.sh:196` resolves a team config `drivers.partition` value as a built-in driver path and sources it during delivery; a worker that writes the shared store can plant `../../../db/payload` and have the orchestrator's unsandboxed delivery hook source it; the fix validates the driver name against the installed drivers directory (an allowlisted basename, no path separators) before sourcing, with a red-then-green test; reported upstream.
- 2026-10-19T04:32:56Z: the round-6 P1-15 text (prompt `p115-a01r5-redesign-prompt.md`, 501 lines) installed: the dedicated-identity item removed (D-024-23: detection, not prevention); the agmsg-store driver residual row; managed settings as the sandbox enforcement scope (a rendered staging file, `make install-managed-settings` prints the operator's sudo command); worker denies on `<worktree>/.claude/**` and `.mcp.json`; checker OK; the sixth C-80 review started 04:34Z.
- 2026-10-19T04:37:39Z: C-80 sixth review (`…-text-security-5cbbc03.md`): `Verdict: incorrect`, three P1, all local: (1) a pinned PATH does not neutralize an inherited BASH_ENV (probe) → hook commands start with `/usr/bin/env -i PATH=… HOME=…`; (2) the agmsg store's `db/trusted-plugins` and `plugins/partition/shared.sh` let a worker authorize a replacement plugin storage.sh sources → the worker denies cover both paths and the agmsg-hardening row widens; (3) the managed-settings path differs on Linux (`/etc/claude-code/managed-settings.json`) → the Makefile target selects the OS path. Design 5.14 amended; round 7 follows.
- `text-security:5cbbc03:2` store-plugin-trust (agmsg-hardening-a01, widening the first row): storage.sh:208-228 selects and sources a plugin a team's `db/trusted-plugins` authorizes; a worker that writes the store authorizes `plugins/partition/shared.sh`; the fix refuses plugins not installed under the skill's read-only plugins directory with a trust list outside the shared store.
- 2026-10-19T04:43:45Z: the round-7 P1-15 text (prompt `p115-a01r6-redesign-prompt.md`, 501 lines; the three local changes only: env -i on every hook command, the agmsg plugins and trusted-plugins denies with the store kept writable, the OS-selected managed-settings path) installed; checker OK; the seventh C-80 review started 04:44Z.
- 2026-10-19T04:46Z: C-80 seventh review (`…-text-security-519afd7.md`): `Verdict: incorrect`, one P1 and one P2, both consequences of the env -i decision: `env -i` strips CLAUDE_PROJECT_DIR, which the guard needs (every hook would exit 0 without running) → the hook command re-exports the launch identity explicitly after env -i; the pinned PATH removes ruff, prettier and terminal-browser from the orchestrator's formatter and map hooks → in orchestrator sessions the guard runs them with a rendered PATH of the trusted root's absolute tool directories. Round 8 (local) follows.
- 2026-10-19T04:5xZ: round-8 P1-15 text installed (env -i with the launch identity re-exported; role-specific PATH in the guard); checker OK; the eighth C-80 review started.
- 2026-10-19T05:41Z: C-80 ninth review (`…-text-security-435275a.md`): `Verdict: correct`. The text is dispatched to a010 (wJ:p5, worker-e; a012 is on its #412 revise) at 05:4xZ with the counters and the review history pasted in its Checks block; a05 follows on the same seat after this merge.
- 2026-10-19T05:45Z: PING to a010: design 5.14 and D-024-16..23 exist only in the orchestrator working copy until the next records PR; the worker reads them at the absolute path of the main checkout (C-86 recorded).
- 2026-10-19T05:46:28Z: a010 `status=running`: branch `tools/worker-write-boundary-a01` from 205fe85c (origin/main had advanced); the #420 and #427 branches preserved; reading callers and adding the red tests.
- 2026-10-19T05:50:16Z: a010 `status=running question=1`: the Check requires `make format` pass while the clean base 205fe85c fails on 12 out-of-scope files (the known inherited set). Interpretation note 1 (05:5xZ, no amendment): the sibling texts' clause applies (an inherited formatting failure is reproduced against the unchanged base and disclosed with exact output and per-file exit statuses; no out-of-scope repair); the task's own files pass the make format flags. INV-6: questions 1.
- 2026-10-19T06:01:06Z: a010 `status=running question=2`: the tracked `.claude/settings.json` is not a chezmoi template, so literal rendered HOME/anchor/interpreter paths would bind it to this macOS host; it proposes HOME-relative paths in the tracked file with the host-specific absolute paths only inside the rendered guard, and CLAUDE_PROJECT_DIR never selecting an executable. The reading is right and the text is wrong. This is the second question PONG (the first 05:50:16Z) → INV-6 S2: `status=withdrawn` 06:1xZ (branch, 8 green tests, fixtures and evidence kept); the reset a02 = the a01 text with both clarifications folded in and the Codex `network_access` item removed (routing: a Codex seat edits no Codex-boundary source; that item becomes a small Claude-seat task), redesigned by the review profile and passed through C-80 before dispatch.
- correction (2026-10-19T06:13Z): the S2 line above was premature: `regime-counters.sh --history-only` counts `status=question` PONGs and reports questions=0, because a010 sent its two questions as `status=running question=N` (a Codex-seat form deviation of the PONG contract, recorded as a conformance note; C-87: the counter also reads a `question=` field). By the counter INV-6 S2 did not fire; no withdrawal was sent (the send was guarded on the counter). Both questions are answered by interpretation notes (note 1 at 05:5xZ; note 2 at 06:13Z: $HOME-relative paths in the tracked file, host-specific paths only in the rendered guard) and amendment 1 folds both into the text and removes the Codex network_access item (routing); the running redesign output becomes that amendment text (same task id, no reset).
- 2026-10-19T06:19:54Z: a010 `status=blocked` on an optional progress inspection only (`ps -axo … | rg …` refused by its Codex sandbox: operation not permitted); no retry; the authorized unit run continues and is collected through its session; implementation per note 2 continues after that run. No action: an optional inspection outside the sandbox is correctly refused and not escalated (Worker Playbook step 4).
- 2026-10-19T06:23Z: the amendment-1 text (the review-profile a02 output re-targeted to a01: the inherited make format clause, the portable tracked settings.json with host paths only in the rendered guard, the Codex network_access item removed to the Claude-seat task dotfiles-T133-codex-worker-network-a01) installed; checker OK; its C-80 review started 06:23Z; dispatch to a010 on correct.
- 2026-10-19T06:25:59Z: C-80 of the amendment-1 text (`…-text-security-f1b862c.md`): one P2 (the guard source is a plain `executable_` file, which chezmoi copies without template expansion, so the per-host paths cannot be rendered) → the source becomes `executable_orchestrator-only.sh.tmpl` with the rendering sentence and the render test stated; the review runs again before dispatch.
- 2026-10-19T06:26:42Z: a010 `status=blocked` on the required CI doc test: tests/unit/test_agmsg_orchestration_docs.py:200-201 asserts the step 4 sentence this task rewrites and is outside allowed_files. Amendment 1 (in its C-80 review) gains the module for that one assertion with a threat row; C-78: PR #427 (P1-8, the same seat) edits the module and merges first; this PR rebases. PING sent 06:2xZ.
- 2026-10-19T06:5xZ: C-80 of the amendment-1 text with the doc test module (f589c7c): one P1 (the launcher moves delivery hooks to worker user settings but Claude Code keeps loading the worktree's legacy `.claude/settings.local.json`, so previously generated unsanitized entries would stay effective) → item 10 gains the migration paragraph (managed entries removed from the legacy file, unrelated entries kept, an unknown command hook there refuses the start; fixture test test_add_worker_migrates_legacy_worktree_local_hooks); the herdr-agents and test rows name it. C-80 of that text (e5d1b57): `Verdict: correct`. Counters pasted (tasks=1 amendments=0 results=0); amendment 1 dispatched to a010 (sha 7ab7b5a5bbf49d6b61c5a109c6e2bd82656b14f4b76cba9de31eb67765aae326, previous bf5881da…) with the rebase instruction (main 3f240b12; PR #427 once merged).
text-security:f589c7c:1	legacy-hook-binding
- 2026-10-19T07:16:51Z and 07:17:17Z: a010 `status=blocked` twice on amendment 1: (1) the test cap: 861 changed test lines after fixture consolidation against the cap 800 (source 657/700); it asks for 900 rather than deleting checks (native rendering, legacy refusal, no-import markers, descendant/process fixtures). Root cause: amendment 1 added the legacy-migration fixture test without re-measuring the cap (my C-79 defect). (2) `make validate-agent-assets` exits 2: scripts/validate-agent-assets.py:349-355 pins the Linux excludedCommands to the exact four-entry seat-tool list (gh included) and tests/unit/test_validate_agent_assets.py:1080-1091 pins the platform difference; both outside allowed_files. Root cause: the validator encodes the pre-P1-15 exclusion policy; a policy change must move its check and fixture in the same PR. Decision: amendment 2 (the cap re-measured from a010's numbers; the two touchpoints join allowed_files with threat rows) — the second amendment is INV-6 S2, so the text is written by the review-profile context (prompt `p115-a03-redesign-prompt.md`) and passes C-80 before dispatch; a010 continues in-scope work (PING 07:20Z).
- 2026-10-19T07:27:13Z: a010 `status=working`: re-measured after the readable consolidation and the portable/anchored hook fixtures: source 665, tests 895 changed lines; all 21 task-referenced selectors exist; the full module rerun running; the validator untouched pending amendment 2; the draft evidence records exist; task copy = amendment 1 (7ab7b5a5…). Note for amendment 2: the test cap is measured from 895 (+ the validator fixture), not from the 861 of 07:16Z.
- 2026-10-19T08:1xZ: C-80 of the amendment-2 text (db2a8f9): `Verdict: correct`. Counters pasted (tasks=2 amendments=1 results=0 before this send); amendment 2 dispatched to a010 (sha 9111f07b5284f6dc43f77454cfc70fa01f8d708db424426f15ff9f08df74eebd, previous 7ab7b5a5…) with the rebase instruction (main 69dccca9, #427 merged).
- 2026-10-19T08:16:20Z: a010 `status=working`: rebased onto main 69dccca9 conflict-free (local head 55c125a1; 20 task paths; source 665 / tests 895; doc module and render-check green on the rebased head); the rebase reported a denied `packed-refs.lock` write (the worker sandbox; HEAD and refs consistent). Amendment 2 (sha 9111f07b…) dispatched 08:17Z.
- 2026-10-19T08:21:22Z: a010 `status=blocked` on amendment 2 (installed, copy byte-identical 9111f07b…; the three-entry exclusions and the two fixtures red-to-green; source 674/700, tests 905/950): (1) validate-agent-assets.py:1193-1194 requires the literal substring `permgate claude` in the managed Claude settings' hooks, which the env -i prefix and host bindings break; (2) the `valid_claude_sandbox` fixture (:1062-1071) omits the now-required exclusions (2 errors, 6 failures in the module); (3) the text's line 414 carries the operator's absolute home path (the C-86 citation), which the validator's home-path scan trips on the committed task copy. Root cause: amendment 2 widened the validator scope to two exact subranges instead of enumerating every policy check the design changes (the substring hook check is another pin), and C-86's absolute-path citation conflicts with the home-path scan. Proper state: the validator's checks that encode policy move with the policy in one consolidated item (structural hook check, fixtures), and tracked text carries `$HOME`-relative paths plus the quoted design sentences (C-88). Decision: amendment 3, consolidated, written by the review-profile context (prompt `p115-a04-redesign-prompt.md`), C-80, dispatch; a010 holds with no push (its request).
- 2026-10-19T09:09Z: the consolidated amendment-3 text (review-profile `p115-a04.md`, 562 lines; 50 changed lines against amendment 2): item 16 enumerates the validator checks the design changes (platform-symmetric exact exclusions at :349-355; the managed-settings PermissionRequest hook check made structural: shlex-parsed sanitized prefix, executable basename `permgate`, argument `claude`, nothing else; ccgate refusal kept) and the fixtures (`valid_claude_sandbox`, the two platform fixtures, the literal-form assertions in the three test modules); the design path `$HOME`-relative (C-86 amended); 5.14 items 1, 2, 9 and 10 quoted inline (C-88); caps 700/950 with the measurement sentence restated. Checker OK; C-80 started.
- 2026-10-19T09:11:41Z: C-80 of the amendment-3 text (f810c30): `Verdict: incorrect` on one P1: the managed settings PermissionRequest hook calls `permgate claude` directly while permgate's shebang is `#!/usr/bin/env -S uv run --no-cache --script`; under the sanitized `PATH=/usr/bin:/bin` the hook exits 127 and `onFailure: "block"` denies every permission request (the reviewer probed it). Root cause: the text bound hook commands to a fixed PATH without binding the interpreter of the one hook that must run for every seat; a parsed-token validator check cannot see the shebang. Proper state: the hook runs permgate through the rendered absolute uv and python (the managed settings file is a chezmoi template, so host paths belong there), the validator check requires that exact form, and a render test executes every rendered hook command under the fixed PATH. Decision: amendment 4 by the review-profile context (prompt `p115-a05-redesign-prompt.md`); a010 keeps holding.
text-security:f810c30:1	hook-interpreter-binding
- 2026-10-19T09:22Z: amendment-4 text (review-profile `p115-a05.md`, 568 lines; 48 changed lines against amendment 3) installed: the managed PermissionRequest hook runs permgate through the template-rendered absolute uv and Python (`run --no-config --no-project --offline --python <abs> --script`), the validator requires that exact form, and a render test executes every rendered hook command under the fixed PATH (executable resolution, a PermissionRequest execution with a fake payload); caps unchanged (700/950). Checker OK; C-80 started.

**Focusing on concise reading**
web search: 
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8d42532.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-e5d1b57.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-db2a8f9.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f810c30.md.last.md; sed -n '1,20p' .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "python3 -I -c 'import json; g=json.load(open(\".ua/knowledge-graph.json\")); print(\"\\n\".join(str({k:n.get(k) for k in (\"filePath\",\"summary\")}) for n in g.get(\"nodes\",[]) if any(s in str(n.get(\"filePath\",\"\")) for s in [\"format-edited\", \"project-map-reload\", \"agent-config.yaml\", \"permgate\"])))'; git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD | head -35" in ~/Workspace/dotfiles
 succeeded in 235ms:
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:273](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:273) The race acceptance rests on a false premise: a sandboxed worker can swap an allowed directory for a symlink after validation, causing the unsandboxed file tool to overwrite a trusted path that the worker cannot write directly; static path tests cannot close this boundary.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:80](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:80) Remote SHA pinning and `--no-replace-objects` do not authenticate the writable object database: replacing an intermediate tree object can redirect ledger lookup to an attacker’s valid blob because that traversal does not verify the intermediate object’s content hash. [Git tree traversal](https://github.com/git/git/blob/v2.51.0/tree-walk.c), [object reading](https://github.com/git/git/blob/v2.51.0/odb.c).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:219](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:219) Absolute hook entrypoints do not bind their descendants: retained `herdr-agent-state.sh:25` invokes bare `python3`, while delivery invokes scripts with `/usr/bin/env bash` shebangs; the specified launcher captures and tracked-hook tests miss these unsandboxed, PATH-resolved executions on this shim-first host. [Mise shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:84](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:84) The table omits the retained Herdr socket capability (`agent-config.yaml:325`): a sandboxed client can request terminal execution through the host server, whose existing driver uses `pane run`; refusing excluded command names does not restrict socket RPCs or the resulting host execution. [Unix-socket escape risk](https://code.claude.com/docs/en/sandboxing#security-limitations).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:275](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:275) Startup validation does not mitigate a later hook timeout or termination, which permits the protected action; Python exit-2 tests therefore leave enforcement fail-open, although Claude provides runtime-level `onFailure: "block"` starting with v2.1.295. [Hook failure control](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails).

📝 まとめ: Reviewed the task, every threat row, and cited acceptance/review context; five findings remain for orchestrator disposition. No files changed.

Not checked: implementation tests or live enforcement; write isolation and approval integrity remain unestablished.
Verdict: incorrect- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:131](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:131) No threat row or control separates worker GitHub credentials from the orchestrator’s: `CLAUDE_CONFIG_DIR` does not isolate gh authentication, so a worker with the shared credential can call the merge API through permitted sandbox networking; GitHub cannot enforce the claimed seat identity distinction. [gh credential selection](https://cli.github.com/manual/gh_help_environment).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:165](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:165) The deny inventory trusts the same worker-writable Git objects and refs rejected for ledger authority: planted replacement refs can make `git ls-tree` omit protected paths, and neither `env -i` nor the prescribed flags authenticate that enumeration; the named fixtures omit this attack. [Git replacement semantics](https://git-scm.com/docs/git-replace).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:267](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:267) The “protected” orchestrator cache is absent from the specified deny inventory: checkout-local `.agents/worklog/uv-cache` is gitignored, `.agents` is absent from the tracked top-level tree, and `~/.agents/**` names a different directory; `--offline` does not prevent execution of poisoned local cache content.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:169) Denying all `~/.agents/**` also denies the required agmsg `db`, `teams`, `run` and `ext-tools` writes beneath it, contradicting line 159’s allowances and preventing sandboxed worker messaging; render tests that merely assert both lists cannot establish a functioning policy. [Combined sandbox enforcement](https://code.claude.com/docs/en/sandboxing#how-sandboxing-relates-to-permissions).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:235](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:235) Preparing worktree-local delivery settings misses the main checkout’s local settings, which linked-worktree sessions also load and which currently contain unguarded agmsg hooks bound to the main project; dedicated user settings and tracked-hook guards therefore do not establish the promised effective hook set. [Local settings resolution](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:251](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:251) Absolute entrypoint interpreters cannot satisfy the descendant contract while installed agmsg scripts remain unchanged: `session-start.sh:59` directly executes `identities.sh`, whose shebang is `/usr/bin/env bash`; the text supplies no hook-runtime PATH binding that prevents this unsandboxed descendant from resolving through the host’s shims. [Shim resolution](https://mise.jdx.dev/dev-tools/shims.html).

📝 まとめ: Reviewed every threat row and the cited acceptance/review context; six findings remain for orchestrator disposition. No files changed.

Not checked: implementation, live enforcement or credential scopes; execution and authority binding remain unestablished.
Verdict: incorrect- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:285](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:285) `GH_CONFIG_DIR` separates configuration, not Keychain access: gh keys credentials by hostname/user, and the worker can select the readable orchestrator configuration inside its sandbox; separate login and removal of inherited tokens therefore do not establish the claimed GitHub identity boundary. [gh credential implementation](https://github.com/cli/cli/blob/trunk/internal/config/config.go).

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:175](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:175) Writable agmsg stores also control executable selection: a worker can set a team’s `drivers.partition` to `../../../db/payload` and place `payload.sh` in the allowed db directory; installed [storage.sh](~/.agents/skills/agmsg/scripts/lib/storage.sh:196) resolves this as a trusted built-in and sources it during unsandboxed delivery, bypassing fixed PATH without any race; this non-path control lacks a threat row or adversarial test.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:215](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:215) The sandbox restrictions live only in user settings, while project/local settings still load and line 263 preserves unrelated local settings; higher-precedence settings can disable sandboxing or add exclusions/socket allowances, and an empty user list cannot remove them—the design omits the managed/`--settings` enforcement scope and conflicting-scope tests. [Sandbox enforcement scopes](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox).

📝 まとめ: Reviewed every threat row and cited acceptance/review context; three findings remain for orchestrator disposition. No files changed.

Not checked: implementation or live enforcement; credential separation and execution binding remain unestablished.
Verdict: incorrect
 succeeded in 315ms:
No actionable findings. All 20 `allowed_files` entries have coverage across 44 threat rows; none claims closure from configuration tests alone. The legacy-hook migration addresses the previously reported execution-binding gap and matches documented [settings loading](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository).

The design distinguishes its controls from the acknowledged same-user, shared-capability, agmsg sourcing and path-race residuals.

Reviewed task SHA-256: `e5d1b5700f35b5245b872af9736882fb2e2192907d101db2b798e662bf043055`.

📝 まとめ: Reviewed the task, every threat row and cited acceptance/review context. No files changed; acceptance remains the orchestrator’s decision.

Not checked: implementation tests or live deployment; the stated residual risks remain.
Verdict: correctNo actionable findings in the reviewed design. All 22 `allowed_files` entries are covered across 46 threat rows; none claims `closed` status. The controls distinguish executable binding from the explicitly retained same-user, shared-capability, agmsg sourcing and path-race residuals. Managed enforcement and symlink claims match the documented [sandbox scope](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) and [path checks](https://code.claude.com/docs/en/permissions#symlinks).

Reviewed task SHA-256: `db2a8f9b12f3c934b55200590f7469d699931408cd53a4f0ac110f6b0a1463bd`.

📝 まとめ: Reviewed every threat row and cited acceptance/review context without changing files; disposition remains with the orchestrator.

Not checked: implementation tests or live deployment; the stated residual risks remain.
Verdict: correct- [P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:428](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:428) The mandatory direct `permgate` invocation leaves interpreter selection to its unchanged `#!/usr/bin/env -S uv run --no-cache --script` shebang; under the prescribed `PATH=/usr/bin:/bin`, the read-only probe exits 127 (`env: uv: No such file or directory`), so `onFailure: "block"` [denies PermissionRequest](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails); parsed-token tests cannot establish executable binding, and the contract explicitly rejects the absolute-interpreter invocation needed to bypass that shebang.

Reviewed all 46 threat rows and cited acceptance/review context; all 22 allowed paths have rows, and none claims `closed`.

Task SHA-256: `f810c30bd61f7a01d3ea84ceadf4951c50995f82aa01efd425c5c1ee02682c3a`.

📝 まとめ: Read-only design review completed with one finding for orchestrator disposition; no files changed.

Not checked: implementation tests or live deployment; the documented same-user and shared-capability residuals remain.
Verdict: incorrect---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md task_sha256=bf5881da1c1c289ae3f4fb26cdd94b8a9d01496af0beab448d0cfa4a450c946b deadline=none done_signal=AGMSG-RESULT note=a010:plan-024-P1-15(the-worker-write-boundary;design-5.14-items-0-10;the-text-passed-its-9th-pre-dispatch-security-review);fresh-branch-from-origin/main-b22a5580;your-#420-branch-stays-untouched-for-a05-which-follows-this-merge;security-true:task-level-audit-and-security-review-on-the-final-head;the-operator-steps-named-in-the-text(managed-settings-sudo-install,worker-directory-login,permgate-codex-rule,make-update)are-not-yours;no-@codex-review-comment;single-gh/git-write-commands;one-pre-push-review-round-at-most"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "searches": [],
  "task": "dotfiles-T133-worker-write-boundary-a01"
}
---

# Acceptance: dotfiles-T133-worker-write-boundary-a01 (plan 024 P1-15: the worker write boundary; D-024-17/19/20)

- text: review-profile design 03:18Z (prompt `.agents/worklog/orchestrator-glue/p115-a01-design-prompt.md`); checker OK; 14 files; not dispatched.
- 2026-10-19T03:24:11Z: C-80 review of the text (`.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8bac9e5.md`): `Verdict: incorrect`, seven P1, one P2: (1) the gh wrapper forwards argv verbatim, so `gh repo clone … -- --config core.sshCommand=<exe>` runs worker code outside the sandbox → the wrapper allows an explicit subcommand list and refuses `--` passthrough and config-carrying forms; (2) a bash wrapper reads BASH_ENV before `env -i` (probe confirmed) → the wrapper is Python under an absolute `-I` interpreter path rendered from the trusted root; (3) project hooks execute the worktree's `.claude/hooks/contextdb_hook.py` through bare `python3` and the format hooks resolve tools through shims → worker seats run no project hooks (a factual check of the settings switch is pending with the Claude Code docs); (4) Codex workers share `.git/objects` and `.git/refs` writes (herdr-agents:439), so `origin/main` can be replaced after a fetch → design 5.14 item 8 now binds the committed ledger to the sha `git ls-remote origin refs/heads/main` returns (amended 03:2xZ); (5) `git ls-tree` enumeration needs the sanitized git environment; (6) the reviewer states Edit deny rules also enter the Bash sandbox configuration, which would block the orchestrator's sandboxed record writes under `.orchestration/**` → a factual check pending; (7) `failIfUnavailable: false` lets a seat run unsandboxed when Linux dependencies are missing → `true` for worker seats; (8) P2: symlink and case-alias identity tests missing. Five facts are being verified against the Claude Code documentation before the revision (excludedCommands matching, hooks switches and capture, Edit denies vs sandbox, failIfUnavailable, Edit rule scope and path forms).
- 2026-10-19T03:2xZ: Claude Code documentation facts (the claude-code-guide agent, code.claude.com/docs sandboxing, hooks, permissions pages): excludedCommands match the whole call and every chained sub-command must match; `disableAllHooks` exists but no project-only switch; hooks are not captured at start (a file watcher applies edits); Read/Edit deny rules merge into the sandbox filesystem configuration (so an Edit deny on `.orchestration/**` would block the orchestrator's sandboxed record writes); `failIfUnavailable` is fail-open by default; `Edit(path)` rules cover Write/MultiEdit/NotebookEdit, path forms `//abs`, `~/`, project-relative, deny wins. Consequence (5.14 item 1 amended): the Claude-seat boundary is a user-level PreToolUse hook keyed on the session cwd (worktree sessions: deny file-tool writes outside the cwd and inside `<cwd>/.claude/**`, `<cwd>/.mcp.json`), not Edit deny rules; `failIfUnavailable: true`; the gh wrapper is Python under an absolute `-I` interpreter with a subcommand allowlist; the committed ledger is read at the `git ls-remote` sha.

 succeeded in 890ms:
{'filePath': 'home/dot_agents/agent-config.yaml', 'summary': 'Canonical hand-edited manifest for Codex and Claude Code: model profiles (express/standard/review/deep/security/audit/adh), herdr-agents worker kind/profile/worktree, Codex and Claude settings, sandboxes, permissions, hooks, plugins, disabled-by-default MCP servers, and pinned install assets. All agent-native config files are rendered from it.'}
{'filePath': 'home/dot_agents/permgate-policy.yaml', 'summary': 'Policy for the permgate PermissionRequest hook: shadow-only LLM classifier providers, read-deny patterns for secrets, layered deny/workspace-write/allow decisions, regex allowlists for read-only gh/git/process/version commands, a catastrophic rm deny rule, enablement latency thresholds, and observed fallthrough metrics.'}
{'filePath': 'home/dot_claude/hooks/executable_format-edited-files.py', 'summary': 'Claude Code PostToolUse hook that collects edited file paths from the hook JSON and runs ruff format/check plus ty on Python files and prettier on Markdown files without a shell.'}
{'filePath': 'home/dot_claude/hooks/executable_format-edited-files.py', 'summary': 'Recursively walks the hook payload collecting every file_path/path string as a Path set.'}
{'filePath': 'home/dot_claude/hooks/executable_format-edited-files.py', 'summary': 'Entry point that parses stdin JSON, filters existing .py and .md files, runs the configured command lists, and returns the worst exit status.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'uv-run Python PermissionRequest hook and CLI for Claude Code, Codex, and normalized CLI actions that applies deterministic deny/allow patterns and workspace rules first, optionally consults a shadow LLM classifier on metadata only, and logs every decision to a JSONL state file.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Loads and strictly validates the schema-v2 permgate policy (providers, categories, patterns, classifier actions, CLI rules).'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Normalizes a hook payload into tool name, tool input, and the text matched by patterns.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Builds the PermissionRequest hookSpecificOutput decision object.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Builds the JSON schema the LLM classifier must answer with (category, confidence).'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Derives normalized, value-free metadata for classifiable read-only gh/git actions, or None.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Validates classifier output against provider thresholds, categories, and the subject action.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Runs the claude or codex CLI as a one-shot schema-constrained classifier over normalized metadata and returns its parsed result, latency, and status.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Builds the redacted decision log record for a request.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Resolves a CLI action path strictly relative to an absolute cwd, rejecting traversal and unsafe symlinks.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Decides allow or deny for a CLI read path against the read pattern list.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Applies workspace-write rules for normalized CLI actions when enabled by policy.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Core decision pipeline: deterministic deny, workspace, allow patterns, then optional shadow or enabled LLM classification, returning hook output and a log record.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Converts a normalized CLI action (bash/read/write/edit) into a hook-style payload with strict validation.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Handles the `cli` mode: parses a normalized action, decides, logs, and prints the decision.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Benchmarks decision latency over fixed gh/git fixtures and prints p50/p95 statistics.'}
{'filePath': 'home/dot_local/bin/common/executable_permgate', 'summary': 'Entry point dispatching hook, cli, and bench modes, guarding against recursion via the sentinel env var.'}
{'filePath': 'tests/unit/test_permgate.py', 'summary': 'Large unittest suite for the fail-closed permgate PermissionRequest hook: deterministic allow/deny layers, workspace and sensitive-path read rules, CLI protocol, classifier timeouts and shadow logging, and provider enablement.'}
{'filePath': 'tests/unit/test_permgate.py', 'summary': 'Extracts the decision behavior from permgate hook JSON output, returning None for empty output.'}
{'filePath': 'tests/unit/test_permgate.py', 'summary': 'Test case with about fifty checks for permgate deterministic layers, path rules, CLI protocol, classifier handling, and logging.'}
.claude/contextdb/contextdb/cli.py
.claude/contextdb/contextdb/config.py
.claude/contextdb/contextdb/hook.py
.claude/contextdb/contextdb/normalize.py
.claude/contextdb/contextdb/paths.py
.claude/contextdb/contextdb/recovery.py
.claude/contextdb/contextdb/storage.py
.claude/contextdb/contextdb/util.py
.claude/settings.json
.coderabbit.yaml
.github/copilot-instructions.md
.github/flakes.yaml
.github/workflows/agent-assets.yml
.github/workflows/docs.yml
.github/workflows/macos.yaml
.github/workflows/private-bootstrap.yaml
.github/workflows/regime.yml
.github/workflows/remote.yaml
.github/workflows/test.yaml
.github/workflows/ubuntu.yaml
.gitignore
.orchestration/acceptance/T18-herdr-agents-two-pane.md
.orchestration/acceptance/T19-herdr-file-viewer-popup-config.md
.orchestration/acceptance/dot-ccstatusline-ubuntu26-hang-T59-a01.md
.orchestration/acceptance/dot-ci-runner-label-pin-T58-a01.md
.orchestration/acceptance/dot-formatter-hook-root-fix-T61-a01.md
.orchestration/acceptance/dot-git-ignore-cc-writes-T56-a01.md
.orchestration/acceptance/dot-macos-brew-untrusted-taps-T57-a01.md
.orchestration/acceptance/dot-main-push-guard-revert-T60-a01.md
.orchestration/acceptance/dot-plain-start-visibility-T45-a01.md
.orchestration/acceptance/dot-ua-graph-refresh-T55-a01.md
.orchestration/acceptance/dot-ubuntu-parity-T2-a01.md
.orchestration/acceptance/dot-worker-kind-guard-T14-a01.md
.orchestration/acceptance/dotfiles-T100-compactiondb-claude-symlink-note-a01.md
.orchestration/acceptance/dotfiles-T101-codex-worker-profile-default-a01.md

web search: https://code.claude.com/docs/en/sandboxing
**Analyzing Python -I flag behavior**
web search: 
exec
/bin/zsh -lc "rg -n 'execution:|tool_paths:|python3:|python:|uv:|prettier:|terminal-browser:|ruff:|bash:|orchestrator_checkout' home/dot_agents/agent-config.yaml; cat home/dot_claude/hooks/executable_format-edited-files.py; cat .claude/hooks/project-map-reload.sh" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '"'^##|''^###|5'"\\.14|D-024-2[013]' .orchestration/plans/024-design-quality.md; rg -n '5\\.14|ledger|ls-remote|origin|GitHub|Completion|review|acceptance' .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md" in ~/Workspace/dotfiles
 succeeded in 37ms:
99:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
109:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
33:  - control: "scripts/permission-guard.py (canonical permission-surface comparison and exact diff SHA256 approval only from git show origin/main:.orchestration/decisions.tsv after fetch in the verified anchored checkout, under D-024-19; working-copy rows and candidate revisions supply no approval authority)"
34:    disposition: "closed: tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_committed_ledger_never_the_working_copy_or_the_pr_tree"
37:  - control: "scripts/orchestrator/ruleset-verify.sh (comparison result and optional updates of an explicitly selected existing progress ledger only on equality)"
51:  - control: "home/dot_config/git/config.tmpl (removal of the GitHub HTTPS-to-SSH pushinsteadof block)"
54:    disposition: "residual: temporary repositories and synthetic deployed manifests exercise decisions without executing submitted payload text or changing GitHub."
55:  - control: "tests/unit/test_permission_guard.py (revision fixtures, permission digests, committed origin/main ledgers in temporary anchored checkouts named by deployed manifest fixtures, and forged working-copy and PR-tree rows)"
56:    disposition: "residual: fixture approvals are committed at origin/main in temporary anchored repositories; uncommitted and PR-tree rows exercise refusal, no external ledger override is used, and the live decision ledger and credentials remain untouched."
57:  - control: "tests/unit/test_ruleset_scripts.py (GET-only argv capture, duplicate occurrences and optional temporary progress ledgers)"
58:    disposition: "residual: fake GitHub responses and temporary ledgers preserve the live ruleset and progress records while the audit checks the assertions."
67:  - control: "scripts/orchestrator/integrate-merge.sh (trusted execution of the gate, final-head security guard, committed-ledger approval, PR checks, pinned squash merge and anchored fast-forward; worker-root trusted paths refuse, and premise 6 retains its Claude-seat residual)"
76:    disposition: "residual: temporary repositories and fake binaries capture discovery and descendant environments without changing the live checkout or GitHub."
80:    disposition: "residual: the first push deletes the a04 copy and adds the byte-identical dispatched a05 copy; TASK and RESULT carry the a05 copy's SHA256, which the orchestrator verifies at acceptance."
84:    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance, and whole-file byte comparison protects the dispatched metadata."
88:    disposition: "residual: the hook executes no payload text; tests use temporary state; ruleset helpers use GET access and write only an explicitly selected existing temporary progress ledger on equality."
93:  - control: "the sanitized environment (section 5.14 item 2)"
97:  - control: "the identity check of the entrypoint (section 5.14 item 4; updatedInput names the verified anchored realpath and preserves the three arguments, subject to premise 6's runtime-specific residuals)"
99:  - control: "the manifest-rendered worker filesystem write boundary (section 5.14 item 1)"
101:  - control: "the trusted-path write-boundary check (section 5.14 item 3; the hook and entrypoint ask when trusted paths lie under .claude/worktrees/ or a manifest-listed worker worktree)"
103:  - control: "the approval provenance boundary (section 5.14 item 8)"
104:    disposition: "closed: tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_committed_ledger_never_the_working_copy_or_the_pr_tree"
113:  - control: "the worker sandbox exclusions (section 5.14 item 10)"
115:  - control: "the output and reservation identity (section 5.14 item 5)"
117:  - control: "the honest residuals (section 5.14 item 6)"
119:  - control: "the shared trusted-execution regressions (section 5.14 item 7)"
121:  - control: "the private offline uv cache (section 5.14 item 9)"
127:  - control: "orchestrator effect fetch, checkout and fast-forward (fetch of origin/main only, fast-forward only, refusal of modified tracked files outside .orchestration and preservation of untracked records)"
128:    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_fetches_only_origin_main_and_preserves_local_records"
132:    disposition: "residual: no forced removal is planned; the existing dirty-worktree rule applies and the acceptance record identifies any discarded uncommitted state."
134:  - claim: none of the five new files exists on origin/main
138:  - claim: PR #400's branch, the material this task rebuilds from, is at the head the T131 review assessed
139:    command: git rev-parse origin/fix/claude-pinned-merge-gate
142:  - claim: the tracked git config still rewrites GitHub pushes to SSH while the live config (hand-edited) does not, the mismatch D3 (d) resolves
155:      section 5.14 item 1 applies per runtime: a Codex seat's sandbox confines all tool writes to its worktree and enumerated writable paths; a Claude seat's Seatbelt sandbox confines Bash only, while Write/Edit/MultiEdit/NotebookEdit, hooks and MCP processes run outside it and the rendered permission policy has no path deny today. The Claude-seat boundary is residual until P1-15 under D-024-17 adds the permgate path deny. The Bash render test asserts only that sandbox's scope. Approval provenance instead uses the committed origin/main ledger after fetch under D-024-19. Worker Playbook step 4's outside-sandbox gh has no present mitigation and is owned by P1-15, whose pending wrapper uses env -i, an absolute gh and a fixed alias-free read-only GH_CONFIG_DIR. A same-UID process outside every seat sandbox remains residual.
168:The worker's first push deletes `.orchestration/dotfiles-T133-permission-guard-gate-a04/task.md` and adds the byte-identical dispatched text at `.orchestration/dotfiles-T133-permission-guard-gate-a05/task.md`. That predecessor-copy deletion is the specified reset bookkeeping exception to the edit boundary. The orchestrator owns canonical reset records. Predecessor canonical task texts, evidence and acceptance histories remain unchanged.
170:The a04 acceptance record preserves the S1 class table, re-plan line and D-024-16. Its six instances are the following.
174:| a03 security review, `31d6c322` | Hook binaries resolve through mise shims. | `decision-not-bound-to-execution` |
175:| a03 security review, `31d6c322` | `.GIT` case variants bypass Git-metadata exclusion. | `decision-not-bound-to-execution` |
176:| a03 security review, `31d6c322` | The PR tree supplies its own decision ledger. | `decision-not-bound-to-execution` |
177:| a04 security review, `911f5202` | The allowed bare gh resolves through the caller's PATH. | `decision-not-bound-to-execution` |
178:| a04 security review, `911f5202` | The body pathname can be swapped after validation. | `decision-not-bound-to-execution` |
179:| a04 local review, `911f5202` | Caller GIT_* variables redirect checkout identity checks. | `decision-not-bound-to-execution` |
181:The `.GIT` finding is the sibling identified in the acceptance record's class accounting. S1 had already been reached by the a04 security review. The attempted instance-by-instance revise after that threshold remains recorded as an orchestration error. This reset does not turn predecessor findings or historical green tests into approvals.
183:The first five premises preserve a04's write-time observations verbatim. They remain historical observations, including the ledger observation that predates D-024-14. Premise 6 states section 5.14 item 1's runtime-specific boundary and its Claude-seat residual. Its renamed render regression asserts Bash denial only. New reports and evidence use the a05 directory and identify their tested revisions.
185:The design sources are `.orchestration/plans/024-design-programs.md` item (14), `.orchestration/plans/024-design-quality.md` sections 5.13 and 5.14, D-024-03 (d), D-024-14, D-024-16, D-024-17, D-024-18 and D-024-19. Section 5.14 applies by reference under D-024-18, with a threat row for each item. The a04 acceptance record and the three named a03/a04 review records supply the reset findings. D-024-16 replaces their text-form allowance design. The second C-80 pre-dispatch security review at `.orchestration/validation/dotfiles-T133-permission-guard-gate-a05-text-security.md.last.md` returned `Verdict: incorrect` with four P1 and one P2. The orchestrator amended section 5.14 items 1, 2, 8, 9 and 10 and recorded D-024-18 and D-024-19. This text incorporates those decisions and retains the stated residuals.
189:The deadline `2026-10-19T03:00Z`, which is 12:00 JST, is missed. The new estimate belongs to the orchestrator. The a04 acceptance record reports 14:00–14:30 JST as that estimate, without turning it into a new worker deadline. An open security P1 stops integration regardless of the estimate.
193:The PreToolUse hook decides on the executable identity of one tracked anchored entrypoint and returns its verified realpath through `hookSpecificOutput.updatedInput`, subject to premise 6's runtime-specific residuals. That entrypoint binds the tools, environment, evidence and head used by execution. Every gh merge, create or update-branch text form asks with the reason `the merge runs through integrate-merge.sh`. The permission guard accepts exact-digest approval only from the committed `origin/main` ledger after fetch. The ruleset scripts retain duplicate-preserving display and verification without changing the live ruleset.
197:0. The inherited dry-probe baseline remains preserved at `.claude/worktrees/worker-e/.orchestration/dotfiles-T133-permission-guard-gate-a01/validation.md`. Its 54 entries, the a02 independent review and corpus, the a03 Bot fixes and fixture repairs, and the a04 regressions retain their original tested identities and limitations.
199:   The a03 Ubuntu directory-order repair and macOS resolved-temporary-root repair remain one historical CI-repair round under C-61. The initial omission of the macOS CI failure remains disclosed. Historical formatting, gate, CI and review failures remain failures.
201:   The a05 validation record references those transcripts and adds a closure table with input, expected a05 result, actual result, exit status and source identity. Former gh-text allow expectations become ask under D-024-16 and are identified explicitly. Retained regressions keep their original red evidence and receive final-head green runs. The new identity contract has red-then-green evidence under `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_the_tracked_entrypoint_of_the_anchored_checkout`.
203:1. `scripts/permission-guard.py --base <ref> --head <ref> [--manifest home/dot_agents/agent-config.yaml]` retains its Python CLI apart from removal of `--decisions`, isolated interpreter execution and committed-ledger approval under item 11. PyYAML runs through `UV_CACHE_DIR=<anchored checkout>/.agents/worklog/uv-cache uv run --offline --with pyyaml`; the implementation otherwise uses the standard library. Item 9 fixes the cache for every orchestrator-side uv run.
209:   `tests/unit/test_permission_guard.py::PermissionGuardTest::test_permission_diff_without_an_approved_decision_row_fails_and_with_it_passes` retains its red-then-green evidence, with approval committed to the fixture's origin/main. Unchanged surfaces, non-permission changes, rendered-only changes, sandbox and anchor changes, malformed data and bad revisions remain covered. Item 11 replaces the anchored-working-copy ledger regression with the committed-ledger regression.
213:   `scripts/orchestrator/ruleset-verify.sh [--expected <json>] [--progress <tsv>]` uses the same comparison. Equality exits 0. An explicitly selected existing progress ledger receives `verified` and the current UTC timestamp in rows `D1` and `D2`, using asserted row anchors and preserving unrelated bytes. An omitted progress flag or absent named file produces print-only behavior and creates no ledger. A difference prints each differing occurrence and key, exits 1 and writes nothing.
225:   The manifest's `orchestrator_checkout` is expanded and resolved with realpath. It identifies a primary checkout whose Git common directory resolves to its own `.git` and whose origin identifies `mryfmo/dotfiles`. The deployed manifest supplies the anchor independently of payload cwd and candidate revisions. Its protection follows premise 6's runtime-specific scope, including the Claude-seat residual. Git identity operations use the captured absolute git with explicit `-C <anchored checkout>` under the sanitized environment and item 9's fixed configuration controls. Permission approval comes only from the committed ledger under item 11.
227:   The hook and the entrypoint refuse with ask when any path they trust lies under `.claude/worktrees/` or under a worker worktree listed by the deployed manifest, including `worker_worktree`. The checks cover the anchored checkout's `scripts/orchestrator`, the Git object store supplying the committed ledger, evidence, the snapshot directory, the private uv cache and every resolved binary. Path resolution and containment use filesystem identity and reject a trusted path reached through a worker-writable component. Checkout identity alone supplies no approval provenance.
235:   The hook fetches `origin/main` using the absolute git and item 9's fixed configuration controls. The anchored checkout's `git rev-parse HEAD` equals the fetched `git rev-parse origin/main`. `git status --porcelain -- scripts/orchestrator/` is empty. The SHA256 of the file selected by `argv[0]` equals the SHA256 of `git show HEAD:scripts/orchestrator/integrate-merge.sh`. Missing tracking, dirty orchestration scripts, a stale HEAD, a different executable identity or a wrong argument shape asks.
237:   An allow response contains `hookSpecificOutput.updatedInput` with the Bash command rebuilt from the checked argv. `argv[0]` is replaced by the verified realpath inside the anchored checkout, and the three argument values remain unchanged. The returned command is encoded without shell expansion. The hook asks whenever it cannot produce that updated input. It never emits allow for the original unchecked spelling alone. Codex tool writes cannot replace the verified realpath through execution; Claude file tools, hooks and MCP processes retain the P1-15 path-deny gap, and a same-UID process outside every seat sandbox remains residual.
245:   `tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_allows_only_the_tracked_entrypoint_of_the_anchored_checkout` is red before the redesign and green afterward. Its positive case is the tracked matching entrypoint at the anchored primary checkout's fetched main. A modified file, an untracked copy with identical bytes, a HEAD behind origin/main, dirty orchestration scripts and each wrong argv shape ask. A failed fetch or hash comparison never allows.
257:   Premise 6 applies per runtime as section 5.14 item 1 states. A Codex seat's sandbox confines all its tool writes to the seat worktree, scratch and enumerated writable paths. A Claude seat's Seatbelt sandbox confines Bash only. Write/Edit/MultiEdit/NotebookEdit, hooks and MCP processes run outside it, and today's rendered permission policy has no path deny for the anchored checkout, deployed manifest and hooks, trusted binaries, evidence, snapshots or private uv cache. The Claude-seat boundary remains residual until P1-15 under D-024-17 adds the permgate path deny. An unavailable-sandbox fallback supplies no authority to proceed.
261:   Worker Playbook step 4's outside-sandbox gh remains a residual with no present mitigation. P1-15 owns the pending D-024-17 wrapper with `env -i`, an absolute trusted gh and a fixed alias-free read-only `GH_CONFIG_DIR` under section 5.14 item 10. D-024-17 is not a present control. A same-UID process outside every seat sandbox also remains residual. Approval provenance uses the committed ledger under item 11 independently of this boundary.
267:   Former merge, create and update-branch allow rows become ask rows. Hook-only fixtures for PR state, body files, acceptance parsing, audit verdicts and records-only exceptions leave with the deleted parser. Execution and publication assertions move into `tests/unit/test_integrate_merge.py`, where those controls act. Their removal from the hook supplies no claim that the underlying safety requirement disappeared.
277:   The retained trusted-root, metadata-identity and historical anchored-ledger regressions preserve their a03 red evidence against `31d6c322988ebb21eebe1e8bf88d5b3910c11f4d` and their a04 results. Their applicable assertions receive final a05 green runs. The committed-ledger replacement and every changed assertion or added sub-case receive new red evidence. The renamed Bash-only render selector retains applicable evidence and records its final-head run without claiming broader sandbox coverage.
283:   The hook's PR-body parsing, caller body-file validation, PR comparison pagination and task-copy selection, acceptance-front-matter parsing, latest accepted-dispatch requirement, audit parsing, required-check lookup and operation-specific repository logic are deleted. The former 27-row text-form allowance surface is retired with that parser.
285:   The hook's `test_legacy_records_do_not_block_bound_acceptance`, body-file operation tests and anchor-versus-worker-draft split cease to specify hook allowance. Applicable evidence and body safety assertions are exercised at the tracked execution boundary. The pre-merge flow never requires a post-merge `AGMSG-ACCEPTANCE status=accepted` notification.
293:   `tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_comparison_preserves_duplicate_rule_types` retains its red-then-green evidence for both scripts. Fixtures cover two differing occurrences, an earlier missing or differing occurrence whose last occurrence matches, and exact equality with duplicates. A mismatch leaves the temporary progress ledger byte-identical. Equality permits an update only to an explicitly selected existing ledger.
301:   Every direct git invocation of the hook and tracked orchestration scripts uses explicit `-C` and `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `-c core.hooksPath=/dev/null`, `-c core.fsmonitor=false`, `-c protocol.allow=never` and `-c protocol.https.allow=always`. The HTTPS exception permits the required fetch. For Git, fetching `origin/main` is the only network operation. These settings also govern Git subprocesses in the gate and finishing paths. Anchored identity operations use the anchored checkout's `.git/config`, whose protection has premise 6's runtime-specific residual; candidate worktree, global and system configuration supply no approval authority.
315:   `scripts/orchestrator/orch-gate.sh` enters its constructed environment before Git discovery. Its environment rebuild, currently at origin/main lines 87-89, retains the private PATH of links to captured absolute binaries, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` and the private `UV_CACHE_DIR`. Direct Git calls carry explicit `-C` and all four `-c` controls above. The rebuilt environment supplies `GIT_CONFIG_COUNT=4` with fixed `GIT_CONFIG_KEY_0=core.hooksPath`, `GIT_CONFIG_VALUE_0=/dev/null`, `GIT_CONFIG_KEY_1=core.fsmonitor`, `GIT_CONFIG_VALUE_1=false`, `GIT_CONFIG_KEY_2=protocol.allow`, `GIT_CONFIG_VALUE_2=never`, `GIT_CONFIG_KEY_3=protocol.https.allow` and `GIT_CONFIG_VALUE_3=always`. These reconstructed values reach the trusted gate and the validator it starts. The validator's bare git calls inherit the sanitized environment and fixed configuration in the verified gate working directory. Caller `GIT_CONFIG_*` inputs never survive the rebuild.
319:   The four section 5.14 item 7 regressions are the trusted-root binary test, the planted-Git-input test, the worker-root trusted-path test and the source-swap test named in this task. P1-6 owns `tests/unit/trusted_exec_contract.py`, which is not present at this dispatch; its creation remains outside this task.
331:    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_passes_a_body_snapshot_never_the_caller_path` has red-then-green evidence. It swaps the original source for a synthetic private-target symlink after validation and captures the pathname and bytes received by fake gh. Gh receives the original validated bytes through the script-written snapshot. The same selector covers safe relative and absolute sources, refused source types, metadata case variants, full-head snapshot names, unique names for repeated calls, snapshot permissions and snapshot metadata exclusion. Case-insensitive behavior is exercised deterministically on case-sensitive CI hosts.
341:11. `scripts/permission-guard.py` reads its only approval ledger as `git show origin/main:.orchestration/decisions.tsv` after fetching `origin/main` in the verified anchored checkout. D-024-19 and section 5.14 item 8 make this the committed ledger. It never reads approval rows from the working copy or PR tree. A working-copy row is a proposal until the operator-approved records PR carrying it merges to main. Approval provenance no longer depends on premise 6's worker write boundary.
343:    The guard obtains the anchor from deployed `~/.agents/agent-config.yaml`, independently of candidate revisions, expands it and resolves it with realpath. The invoking checkout is the anchored primary checkout. Its common Git directory resolves to its own `.git`, and its origin and GitHub repository identity identify `mryfmo/dotfiles`. Fetch and ledger reads use item 9's sanitized environment, captured absolute git, explicit `-C` and fixed Git configuration controls. A failed fetch, missing committed ledger, ambiguous or mismatched anchor or unrelated checkout refuses approval.
345:    The production `--decisions` exception is removed. There is no external ledger path. Tests create a temporary anchored checkout, name it in the deployed manifest fixture and commit its fixture ledger into origin/main. Uncommitted rows and PR-tree rows are separately forged fixture data. Candidate-manifest changes and aliases cannot choose another ledger.
347:    `tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_committed_ledger_never_the_working_copy_or_the_pr_tree` replaces the anchored-ledger selector with new red-then-green evidence. A matching row present only in the anchored working copy fails. A matching row present only in the PR tree also fails. Approval succeeds only after the matching row reaches the fixture's fetched origin/main ledger, even when the working-copy ledger is absent, different or contains a forged approval. The test also covers failed fetch, missing committed ledger, missing or mismatched anchors and unrelated checkouts. The executable and anchor retain premise 6's runtime-specific residuals.
349:    P1-11 owns future CI wiring. That job reads the base commit's ledger rather than the head's ledger. Until it lands, the orchestrator runs the authoritative final-head comparison at acceptance and pastes its output.
355:    The entrypoint checks the final-head permission guard from the anchored checkout with item 9's private offline uv cache and accepts approval only from the fetched committed origin/main ledger under item 11. It requires the task's acceptance record and the gate evidence that record names. Evidence remains inside the trusted checkout, outside Git metadata, regular and free of symlink components. Record contents are parsed as data and never sourced or evaluated. The entrypoint records SHA256 values for the evidence it consumes.
357:    The entrypoint invokes the trusted `scripts/require-crit-review.py` through tracked `scripts/orchestrator/orch-gate.sh`, with the final-head feedback sweep, audit and companion verdict, review receipt, Crit data and acceptance record. It passes a verified PR worktree as orch-gate.sh's second argument, matching that helper's existing `<task> <pr-worktree> <pr>` interface. A SHA string is not substituted for that worktree argument. The worktree's HEAD equals the requested head.
359:    The gate and validator remain the trusted checkout's copies. A PR-controlled Makefile, gate, interpreter configuration or environment cannot replace them. The allowed orch-gate.sh change implements item 9's environment controls both before discovery and across its environment rebuild, including the validator's inherited Git configuration and private offline uv cache. The task adds no bypass input and does not change the fixed acceptance schema or `scripts/require-crit-review.py`. Existing gate evidence filenames retain their helper-compatible spelling, while the records and comparisons bind the full 40-hex head.
365:    The entrypoint refuses modified tracked files outside `.orchestration/` in the anchored checkout before merging or changing the local checkout. After the merge, trusted git fetches only `origin/main`, checks out the default branch and fast-forwards the anchored checkout with `--ff-only`. It fetches no task-branch or PR-head ref. The fast-forward preserves local orchestration evidence and recoverable copies on failure. Untracked records are never removed. It performs no reset that discards local records, no local integration of the task branch and no push to main. Required glue behavior stays within the two allowed tracked scripts and reuses existing tracked helpers.
369:    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_refuses_a_head_the_pr_does_not_carry` has red-then-green evidence. A PR-head mismatch produces no merge and no fast-forward. The positive case captures the exact `--match-head-commit` argument, binding a later head change to GitHub's merge refusal.
371:    `tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_fetches_only_origin_main_and_preserves_local_records` has red-then-green evidence. Captured fetch and checkout calls target only the valid default-branch update and every fast-forward uses `--ff-only`. Modified tracked files outside `.orchestration/` refuse without a merge or local update. Dirty tracked orchestration records and untracked records survive successful and failed fast-forwards, with recoverable copies retained on failure.
377:At a05 acceptance, the orchestrator runs the guard from the verified anchored checkout with `--base origin/main --head <final head>`, item 9's fixed private `UV_CACHE_DIR` and `--offline`, and records the complete output. It prepares the decision row for that a05 permission-diff digest using the next free `D-024-NN` id and the recorded user-approval basis. The row contains `scope=permission approved_by=user diff_sha256=<exact digest>`.
379:Under D-024-19, that working-copy row is a proposal. The orchestrator puts it through the records PR for boundary 24, which the operator approves through the live hook before the a05 implementation merge. Only after that records PR merges to main does the row carry approval authority. This records PR is separate from the one implementation PR, #420. The guard fetches origin/main again and reads the row only through `git show origin/main:.orchestration/decisions.tsv`.
391:No SKILL file enters `allowed_files`. The worker does not edit predecessor canonical task texts, predecessor evidence, acceptance records, the decision ledger or unrelated orchestration helpers. orch-gate.sh is explicitly inside this task's edit boundary; dispositions-a02 follows this task to avoid concurrent edits to it. The one a04 branch-copy deletion is the stated reset bookkeeping exception. Other reset records belong to the orchestrator.
405:The worker records a worker-worktree refusal as an anchor refusal. From the anchored checkout, the orchestrator runs `UV_CACHE_DIR=<anchored checkout>/.agents/worklog/uv-cache uv run --offline --with pyyaml python -I scripts/permission-guard.py --base origin/main --head <final head>`. It records the complete canonical diff, digest and exit status. Exit 1 before a matching row reaches the fetched committed origin/main ledger remains exit 1. Exit 0 requires that committed approval. No working-copy row makes the command pass.
407:`git diff --numstat origin/main...HEAD` shows at most 850 changed lines outside `tests/` and `.orchestration/` and at most 1250 changed lines under `tests/`. Changed lines are additions plus deletions. The source total includes orch-gate.sh and the regenerated managed settings. The a04 record at `911f5202` measured 648 source lines and 908 test lines under its historical accounting. The parser deletion reduces the hook. The final per-file inventory and both totals are recorded against the final head. No new dependency is added.
409:The validation file `.orchestration/dotfiles-T133-permission-guard-gate-a05/validation.md` contains exact commands, verbatim outputs, exit statuses and tested identities. It includes all named a05 red-then-green selectors, retained regression evidence, the updated probe closure table, the gh-text ask table, the entrypoint metacharacter property test, duplicate-ruleset coverage, filesystem-identity cases, the body-swap interleaving and the committed-ledger comparison against working-copy and PR-tree forgeries. It also includes the renamed Bash-only render assertion, first-action sanitization, updated-input binding, trusted-path refusals, Git configuration isolation with the HTTPS exception, the private offline uv-cache regression, orch-gate discovery and validator-inheritance regression, snapshot recheck and both added orchestrator-effect tests. The record states the Claude-seat path-deny gap, same-UID and outside-sandbox gh residuals without calling any closed.
413:No local Bats tests run. Required Bats results come from GitHub Actions. The orchestrator runs `UV_CACHE_DIR=<anchored checkout>/.agents/worklog/uv-cache uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <anchored checkout> .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` before dispatch and at acceptance, covering C1 to C10 and C7b. This validator invocation follows item 9's cache and environment contract.
415:## Completion
419:The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's existing branch, the qualifications below, `dotfiles-T133-permission-guard-gate-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-permission-guard-gate-a05/task.md>` in RESULT. The orchestrator writes the owner task before assigning its first advisory P2. The six reset defects and retained duplicate-rule defect belong to this task.
423:The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no further private correction-and-review cycle to avoid reporting it. Permitted later rounds remain subject to INV-6 and the inherited completion rule.
425:No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition. Surviving P0/P1 findings remain open for the operator's decision.
427:A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker review evidence uses the required `-worker-` infix. Agent-side review evidence and its receipt follow the repository's Crit-data rules without opening a browser review or asking the user to review.
429:RESULT names the final head, base, branch, changed files, Bot findings and dispositions, every open P0/P1, exact test selectors, measured caps, all six new deployable scripts, the orch-gate.sh change, task-copy SHA256 and evidence paths with the SHA256 values consumed by the entrypoint. The report distinguishes predecessor observations from final-head closure and records the indirect-command-recognition residual, interpreter-launch premise, Claude-seat path-deny gap, same-UID process residual and unmitigated outside-sandbox gh exclusion owned by P1-15 under D-024-17. The orchestrator copies worktree evidence by absolute path before acceptance review.
431:This task is `security: true`. Under C-80, a security-profile context reviews this complete a05 task text before dispatch. That review is a dispatch prerequisite rather than a claim made by this draft. The orchestrator also runs the task-level audit and a separate security-profile review on the final implementation head.
433:The finding-class table includes `decision-not-bound-to-execution` and preserves the predecessor classes `argv-text-mismatch`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign. It never starts another instance-by-instance correction round. The acceptance record retains the required class search and re-plan evidence.
435:Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. A changed head receives fresh required evidence. The security review of that final head precedes the gate.

 exited 1 in 64ms:
299:      # roots. ~/.cache/uv: every `uv run` target (make unit-test,
514:  terminal-browser:
#!/usr/bin/env python3
"""Format files reported by Claude Code hook JSON input.

The hook reads the complete JSON event from stdin, extracts every edited file path
from common Write/Edit/MultiEdit payload shapes, filters by suffix, and runs the
formatter for that suffix without going through a shell. ruff and prettier come
from PATH: their versions are pinned in the mise config, and ruff.toml and
.prettierignore keep vendored and record paths untouched.
"""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

PYTHON_COMMANDS = [
    ["ruff", "format"],
]
MARKDOWN_COMMANDS = [
    ["prettier", "--write"],
]


def collect_paths(value: Any) -> set[Path]:
    paths: set[Path] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"file_path", "path"} and isinstance(item, str):
                paths.add(Path(item))
            else:
                paths.update(collect_paths(item))
    elif isinstance(value, list):
        for item in value:
            paths.update(collect_paths(item))
    return paths


def repository_root(path: Path) -> Path:
    """The git work tree containing path, else its directory: where the formatter configs live."""
    try:
        result = subprocess.run(
            ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        return path.parent
    root = result.stdout.rstrip("\n")
    return Path(root) if result.returncode == 0 and root else path.parent


def run_commands(commands: list[list[str]], files: list[Path]) -> int:
    status = 0
    # Run from each file's repository root: prettier reads .prettierignore from
    # its working directory, and the session's directory may be another tree.
    by_root: dict[Path, list[str]] = {}
    for path in files:
        resolved = path.resolve()
        by_root.setdefault(repository_root(resolved), []).append(str(resolved))
    for root, file_args in sorted(by_root.items()):
        for command in commands:
            config = root / "ruff.toml"
            if command[0] == "ruff" and config.is_file():
                # Pin the root config: ruff otherwise picks each file's nearest
                # pyproject.toml (vendor/compactiondb) and skips the root exclusions.
                command = [*command, "--config", str(config)]
            try:
                result = subprocess.run(command + file_args, cwd=root, check=False)
            except FileNotFoundError:
                # make update installs every declared mise tool, so a missing formatter means that step was skipped or failed.
                print(
                    f"{command[0]} is not installed; run `make update` (it installs every declared mise tool)",
                    file=sys.stderr,
                )
                status = max(status, 1)
                continue
            status = max(status, result.returncode)
    return status


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        print(f"failed to parse Claude hook input: {error}", file=sys.stderr)
        return 0

    paths = sorted(path for path in collect_paths(payload.get("tool_input", payload)) if path.exists())
    python_files = [path for path in paths if path.suffix == ".py"]
    markdown_files = [path for path in paths if path.suffix == ".md"]

    status = 0
    status = max(status, run_commands(PYTHON_COMMANDS, python_files))
    status = max(status, run_commands(MARKDOWN_COMMANDS, markdown_files))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
cat: .claude/hooks/project-map-reload.sh: No such file or directory

web search: 'Repository settings under'
**Reviewing environment and script setup**
exec
/bin/zsh -lc "sed -n '99,140p' .orchestration/plans/024-design-quality.md; rg --files home .claude | rg 'project-map-reload|mise.*toml|permgate"'$'"'; sed -n '448,490p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md; sed -n '412,440p' .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md" in ~/Workspace/dotfiles
 succeeded in 22ms:
## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）

orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。

1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly (`--repo mryfmo/dotfiles` or the full pull-request URL): the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged.
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record.
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
home/dot_claude/hooks/executable_project-map-reload.sh
home/dot_mise/config.toml
home/dot_config/mise/config.toml.tmpl
home/dot_local/bin/common/executable_permgate
## Out of scope

The Codex worker profile change `sandbox_workspace_write.network_access=true` belongs to the separate task `dotfiles-T133-codex-worker-network-a01` for a Claude seat. This task contains no implementation, threat row or test for that change. This Codex seat edits no Codex-boundary source. The operator step for the deterministic Codex permgate policy remains named below.

The worker-write-boundary Python hook, its hook entries and `tests/unit/test_worker_write_boundary.py` are dropped. The gh-trusted wrapper remains dropped. The worker gh configuration directory, its templates and the dedicated-identity implementation are removed from this task.

D-024-23 establishes that `GH_CONFIG_DIR` does not separate same-macOS-user Keychain access. A separate OS user or host is required for prevention of worker-initiated merges. Future P1-16 remains the operator's decision. This task implements no credential-separation substitute.

The permission guard and merge gate remain P1-14 a05's work. P1-14 a05 and P1-6 implement the regime rule that approvals and gate evidence of record come from GitHub at a SHA through its API inside the sandbox. The GitHub boundary is detection, not prevention.

For the committed approval ledger, the regime obtains the commit SHA returned by `git ls-remote origin refs/heads/main` and reads `gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. The consuming implementation reads the API response's file content at that exact SHA. It does not fall back to local files, local refs or local object traversal.

A working-copy decision remains a proposal until its record PR reaches main. This task writes no approval row and implements no local-object substitute for GitHub authority. Shared credentials can still authorize a worker-initiated merge. P1-11 owns the next-records-PR regime check for missing acceptance or gate evidence under section 5.14 item 0's detection rule.

The upstream agmsg driver-selection fix belongs to `dotfiles-T133-agmsg-hardening-a01`. Its recorded scope validates the `drivers.partition` driver name as an allowlisted basename without path separators before sourcing and supplies an adversarial red-then-green test. This task leaves the shared stores writable and records the current sourcing route as a residual. The ownership section identifies that upstream task as a task to be written; this text does not claim that its fix or test exists.

Permgate code and deterministic policy remain the operator's responsibility. The worker prepares the operator step that stops the Codex permgate policy from approving sandbox escapes. The worker performs no live policy edit or escape probe.

The operator logs into Claude once with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected. The Claude Keychain entry is keyed to that directory. This Claude login does not authenticate or isolate gh.

Administrative installation of `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux is the operator's step. The worker implements rendering, staging and the printed installation command without running sudo or installing live managed settings.

The documented file-tool checks reduce symlink redirection risk. A same-UID process can race filesystem changes, alter host-local state or execute outside a seat sandbox. The remaining interval between permission checks and path consumption is a residual under section 5.14 item 0. This text makes no claim that the worker could already write every redirected target directly.

The managed Herdr socket allowance stays available to every seat. Per-seat socket removal is unavailable in that shared scope. Shared control-plane exclusions, socket RPC, hooks, approved MCP processes and other processes outside every seat sandbox retain their stated host trust. The configuration is not represented as same-UID adversarial isolation.

`onFailure: "block"` supplies runtime failure behavior where Claude supports it. Python exit-status tests do not establish timeout handling by the runtime. Background hooks and events on which the field has no effect perform no security enforcement in this design.

Consuming-helper snapshots, reservation locks, the common trusted-execution test helper and orchestrator review-worktree relocation remain with their owning hardening tasks. Codex writable-root grants remain unchanged.

In `scripts/validate-agent-assets.py`, the consolidated policy-check changes enumerated in item 16 are in scope; unrelated validator behavior remains out of scope. In `tests/unit/test_validate_agent_assets.py`, the two exclusion cases, `valid_claude_sandbox`, the named hook fixture and structural-hook cases in item 16 are in scope; unrelated tests remain out of scope. The named literal-form assertions and fixtures in the already allowed generator and merge test modules are included as item 16 specifies.

The worker edits neither `.orchestration/decisions.tsv` nor other tasks' canonical texts, evidence or acceptance records, apart from the explicitly named deletion of the predecessor's task-file copy. It performs no authentication change, keyring mutation, ruleset mutation, administrative installation, live settings application, global installation, operator restart or merge.

## Check

`make render-check` and `make validate-agent-assets` pass. The task's own files pass the `make format` flags: `shfmt -i 4 -sr --diff`, `ruff format --config ruff.toml --check` and `prettier --check`.

The clean base `205fe85c` has an inherited formatting failure on 12 out-of-scope files: ten archived task shell sources, `project-map-reload.sh` and `brew.bats`. The inherited failure is reproduced against that unchanged base and disclosed in `validation.md` with its exact output and per-file exit statuses. This clause authorizes no out-of-scope repair.

Shellcheck and shfmt cover the changed shell sources, including the launcher, orchestrator-only guard and repository-owned Herdr state helper. Added or changed shell comments use English shdoc-compatible annotations. Changed Python receives the repository's Python formatting and lint checks.

`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` is green. The validation record contains every named red-then-green selector and the complete final module run.

No local Bats tests run. Required Bats results come from GitHub Actions. The orchestrator runs `UV_CACHE_DIR=<anchored checkout>/.agents/worklog/uv-cache uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <anchored checkout> .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` before dispatch and at acceptance, covering C1 to C10 and C7b. This validator invocation follows item 9's cache and environment contract.

## Completion

The existing branch `tools/permission-guard-gate-a01` continues PR #420 from `911f5202e61a2e46f527fcd9a4eda0041e97410a`. The first push replaces the a04 branch task copy with the byte-identical dispatched a05 copy. Seat a010 keeps its branch, fixes and evidence. The reset creates no second implementation PR. The missed `2026-10-19T03:00Z` deadline remains reported, and the orchestrator owns the new estimate.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's existing branch, the qualifications below, `dotfiles-T133-permission-guard-gate-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-permission-guard-gate-a05/task.md>` in RESULT. The orchestrator writes the owner task before assigning its first advisory P2. The six reset defects and retained duplicate-rule defect belong to this task.

Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. Predecessor counters, the a03 Bot correction, its single CI-repair round, question PONGs, S2 withdrawal and a04 S1 stop remain historical records. They are not recast as approvals.

The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no further private correction-and-review cycle to avoid reporting it. Permitted later rounds remain subject to INV-6 and the inherited completion rule.

No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition. Surviving P0/P1 findings remain open for the operator's decision.

A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker review evidence uses the required `-worker-` infix. Agent-side review evidence and its receipt follow the repository's Crit-data rules without opening a browser review or asking the user to review.

RESULT names the final head, base, branch, changed files, Bot findings and dispositions, every open P0/P1, exact test selectors, measured caps, all six new deployable scripts, the orch-gate.sh change, task-copy SHA256 and evidence paths with the SHA256 values consumed by the entrypoint. The report distinguishes predecessor observations from final-head closure and records the indirect-command-recognition residual, interpreter-launch premise, Claude-seat path-deny gap, same-UID process residual and unmitigated outside-sandbox gh exclusion owned by P1-15 under D-024-17. The orchestrator copies worktree evidence by absolute path before acceptance review.

This task is `security: true`. Under C-80, a security-profile context reviews this complete a05 task text before dispatch. That review is a dispatch prerequisite rather than a claim made by this draft. The orchestrator also runs the task-level audit and a separate security-profile review on the final implementation head.

The finding-class table includes `decision-not-bound-to-execution` and preserves the predecessor classes `argv-text-mismatch`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign. It never starts another instance-by-instance correction round. The acceptance record retains the required class search and re-plan evidence.

Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. A changed head receives fresh required evidence. The security review of that final head precedes the gate.

The deployed hook allows only the anchored tracked `integrate-merge.sh` invocation through updated input naming the verified realpath. The script itself runs each gh and git write as a separate command, without shell chaining. Callers submit the entrypoint as one command with its three arguments. The eventual merge is exactly `gh pr merge --squash --match-head-commit <audited head> <pr>`.

Until PR #420 lands, strings carrying `gh pr merge` or `gh pr create` are written with the file-edit tool rather than Bash heredocs or echo. This includes test fixtures, reports and validation prose. The worker does not deploy the new hook or relax its tracked-main identity conditions to bootstrap this PR.


web search: 
web search: '/bin/sh'
**Assessing installation script issues**
exec
/bin/zsh -lc "sed -n '1,150p' ~/.agents/skills/agmsg/scripts/check-inbox.sh; sed -n '1,95p' ~/.agents/skills/agmsg/scripts/session-start.sh; sed -n '1,80p' ~/.agents/skills/agmsg/scripts/lib/common.sh; cat home/dot_claude/hooks/executable_project-map-reload.sh" in ~/Workspace/dotfiles
 succeeded in 19ms:
#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(cd "$(dirname "$0")" && pwd)/lib/compat.sh"

# Check inbox across all teams with cooldown. Skips if last check was < 60 seconds ago.
# Usage: check-inbox.sh <type> <project_path>

TYPE="${1:?Usage: check-inbox.sh <type> <project_path>}"
PROJECT="${2:?Missing project_path}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$SCRIPT_DIR/lib/storage.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/actas-lock.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/resolve-project.sh"  # agmsg_agent_pid, for instance-id derivation
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/type-registry.sh"

# Which hook event fired. The Stop entry runs `check-inbox.sh <type> <project>`
# (EVENT defaults to Stop); the mid-turn PostToolUse entry (#1003) appends the
# event as a 3rd arg so this script emits the shape that event's runtime accepts,
# without branching on the type name.
EVENT="${3:-Stop}"

# Some Stop-hook runtimes (codex, copilot) want an explicit JSON status object
# even when there is nothing to deliver; others (claude-code) stay silent. This
# is the type's manifest `stop_output=` (data), not a hardcoded type list.
STOP_OUTPUT="$(agmsg_type_get "$TYPE" stop_output 2>/dev/null || true)"
# The wire shape for a PostToolUse payload, from the type manifest (#1003) — the
# same data-driven approach as stop_output. Measured on codex-cli 0.149.1:
# hookSpecificOutput. An unknown/unset value emits nothing rather than a guess.
POSTTOOL_OUTPUT="$(agmsg_type_get "$TYPE" posttooluse_output 2>/dev/null || true)"

# Status (nothing-to-deliver / cooldown) output. For PostToolUse this stays
# SILENT: codex 0.149.1 treats malformed post-tool-use JSON as a failure, and an
# empty additionalContext on every tool call would be pure noise — so a no-op
# turn emits no bytes, which every runtime reads as "hook did nothing".
# Status of the write that hands a payload over. Declared before the first emit
# (the cooldown one) so EVERY emit in this file reports through the same
# variable: "each emit says whether it worked" is checkable, while "the emits
# that can carry a message are guarded" needs the next reader to work out which
# ones those are -- and that is how one of three ends up unguarded.
EMIT_RC=0
emit_status_json() {
  [ "$EVENT" = "PostToolUse" ] && return 0
  [ "$STOP_OUTPUT" = "json" ] || return 0
  printf '{\n  "continue": true,\n  "systemMessage": "%s"\n}\n' "$1" || EMIT_RC=$?
}

# Hook runtimes that pass JSON do so on stdin. Interactive invocations such as
# Gemini's PostToolUse command may inherit a terminal stdin instead; reading
# unconditionally there blocks waiting for input. The `[ ! -t 0 ]` guard just below
# only rules out that TTY case -- a non-TTY stdin whose write end is left
# open (a hook runtime that writes the payload and then simply never closes
# the pipe) still leaves this `cat` waiting for an EOF that never arrives.
# Stop/turn hooks run synchronously, so a `cat` stuck here freezes the whole
# agent pane until the user kills it. Bound the read; a runtime that forgets
# to close its pipe still gets its payload delivered (it's already sitting in
# the command substitution buffer by the time the deadline fires), just a few
# seconds late instead of never. Fails open when `timeout` isn't on PATH
# (stock macOS) -- same unbounded read as before, no regression there. #381
INPUT=""
if [ ! -t 0 ]; then
  if command -v timeout >/dev/null 2>&1; then
    INPUT=$(timeout "${AGMSG_HOOK_STDIN_TIMEOUT:-2}" cat 2>/dev/null || true)
  else
    INPUT=$(cat 2>/dev/null || true)
  fi
fi

# Prevent infinite loop: if stop hook is already active, exit silently
if echo "$INPUT" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true' 2>/dev/null; then
  exit 0
fi

# The session id is still resolved: the actas-ownership check further down
# needs it. Only the deferral that used to follow it is gone. The field name
# differs by vendor: Claude Code emits snake_case "session_id"; Grok Build (and
# Cursor) emit camelCase "sessionId". Try snake first (claude-code unaffected),
# then camel, then the GROK_SESSION_ID env Grok injects into every hook.
SESSION_ID=$(printf '%s' "$INPUT" \
  | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
  | head -1)
[ -z "$SESSION_ID" ] && SESSION_ID=$(printf '%s' "$INPUT" \
  | sed -n 's/.*"sessionId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
  | head -1)
[ -z "$SESSION_ID" ] && SESSION_ID="${GROK_SESSION_ID:-}"
# Normalized to the per-process instance id (#93), which is the token the
# actas owner file is keyed on.
[ -n "$SESSION_ID" ] && SESSION_ID="$(agmsg_normalize_instance_id "$SESSION_ID" "$TYPE")"

# No deferral to a live watcher (#694).
#
# This used to exit here whenever a watcher process was alive for this session,
# to avoid double delivery in `both` mode. The condition was LIVENESS, and the
# failure `both` exists for preserves liveness exactly: a watcher that is alive
# and delivering nothing. So the one mode advertised as a safety net stood down
# in front of the one situation it was wanted for. On 2026-08-08 a session with
# a broken watcher was switched to `both` to recover delivery and nothing
# changed; what worked was `mode turn`, which stops the watcher, which removes
# the liveness signal, which lets this hook run.
#
# Removing it does not double-deliver, and that is measured rather than
# assumed. Both sides consume through the same state:
#
#   watcher      storage_read_cursor_consume -> inserts a `message_read` event
#                per delivered id AND advances read_cursors.local_position
#   this hook    storage_list_unread -> excludes rows at or below that cursor
#                AND rows with a `message_read` event
#
# So a message the watcher has emitted is not offered here. The remaining
# window is an interleave: this hook SELECTs, the watcher emits and consumes
# the same row, then this hook marks it read. Bounded by one poll interval, and
# the trade is explicit -- a rare duplicate line against a mode that silently
# delivered nothing at all.
#
# Deferral was an optimisation, not a correctness requirement. The read state
# is the correctness requirement, and it was already there.

# Resolve the invocation path to the registered project root (session marker /
# nearest ancestor / sibling worktree) before the identity lookup — the
# whoami.sh path did this resolution, and identities.sh itself is an exact
# registry lookup by design (its other callers rely on that).
PROJECT="$(agmsg_resolve_project "$PROJECT" "$TYPE")"

# Consume exact (team, agent) TSV rows instead of independently flattened
# agent/team lists. For multiple agents, preserve the existing first-agent
# policy, but subscribe only to that agent's actual team rows.
IDENTITIES=$("$SCRIPT_DIR/identities.sh" "$PROJECT" "$TYPE")
[ -n "$IDENTITIES" ] || exit 0

AGENT=""
TEAM_LIST=()
IDENTITIES_VALID=1
while IFS=$'\t' read -r identity_team identity_agent identity_extra; do
  if [ -z "$identity_team" ] || [ -z "$identity_agent" ] || [ -n "$identity_extra" ]; then
    IDENTITIES_VALID=0
    break
  fi

  [ -n "$AGENT" ] || AGENT="$identity_agent"
  [ "$identity_agent" = "$AGENT" ] || continue

  team_seen=0
  # ${arr[@]+...} guards the empty-array expansion: under `set -u` bash 3.2
  # (macOS default) treats "${TEAM_LIST[@]}" on an empty array as unbound.
  for selected_team in ${TEAM_LIST[@]+"${TEAM_LIST[@]}"}; do
#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(cd "$(dirname "$0")" && pwd)/lib/compat.sh"

# SessionStart hook for delivery modes `monitor` and `both`.
#
# Usage: session-start.sh <type> <project_path>
#
# Reads the hook input JSON from stdin to extract the session_id, then emits
# an instruction telling Claude to invoke the Monitor tool against watch.sh.
# The hook input includes session_id for SessionStart events.
#
# Before emitting the directive, this script also takes care of preventing
# duplicate watchers across `/clear` (and similar) re-fires of SessionStart
# within the same Claude Code instance. State is kept in
# `~/.agents/agmsg/run/cc-instance.<cc_pid>`, which records the last
# session_id this CC instance attached to. On each fire we kill the watcher
# for the previous session_id, then record the new one. Multiple CC
# instances of the same project get their own cc_pid, so they never step
# on each other.
#
# Quietly exits 0 when whoami says the agent isn't joined to anything yet.
# Mode is implicit: if this script is being invoked at all, it's because
# `delivery.sh set monitor` (or `both`) installed it in the project's
# settings.local.json — that fact alone is the source of truth for "should
# we emit the directive?". No separate global mode value to consult.

TYPE="${1:?Usage: session-start.sh <type> <project_path>}"
PROJECT="${2:?Missing project_path}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUN_DIR="$SKILL_DIR/run"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/actas-lock.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/registry-lock.sh"  # publish cc-instance only after a complete write
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/resolve-project.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/node.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/hash.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/storage.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/type-registry.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/role-session.sh"  # role->session reverse lookup (#339)
# Only DEFINES agmsg_close_inherited_fds; nothing is closed here. The type
# plug calls it inside a subshell around its own long-lived spawn, so this
# shell's descriptors are untouched. See lib/close-fds.sh.
source "$SCRIPT_DIR/lib/close-fds.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/terminal-context-line.sh"

# Identity sanity check — no point launching a watcher with an empty pair set.
PAIRS=$("$SCRIPT_DIR/identities.sh" "$PROJECT" "$TYPE" 2>/dev/null || true)
[ -n "$PAIRS" ] || exit 0

# Read hook input JSON from stdin BEFORE the type plug below runs (#1468):
# stdin can only be read once, and a plug that needs a hook input field (e.g.
# codex reading `source` to tell startup/resume/clear apart) has to see it
# while it is still there. No plug reads it yet, so this move is order-only —
# nothing downstream changes behavior. The session id field name differs by
# vendor: Claude Code emits snake_case "session_id"; Grok Build (and Cursor)
# emit camelCase "sessionId". Try snake first (claude-code unaffected), then
# camel, then the GROK_SESSION_ID env Grok injects into every hook.
INPUT=$(cat 2>/dev/null || true)
SESSION_ID=""
if [ -n "$INPUT" ]; then
  SESSION_ID=$(printf '%s' "$INPUT" \
    | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | head -1)
  [ -z "$SESSION_ID" ] && SESSION_ID=$(printf '%s' "$INPUT" \
    | sed -n 's/.*"sessionId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    | head -1)
fi
[ -z "$SESSION_ID" ] && SESSION_ID="${GROK_SESSION_ID:-}"
# Fallback so the instruction is still actionable even outside a hook flow.
[ -z "$SESSION_ID" ] && SESSION_ID="unknown-$$"

# Type-specific SessionStart behaviour (Template Method). A type may ship
# scripts/drivers/types/<type>/_session-start.sh defining agmsg_session_start to override the
# default no-op — codex uses it to hand the session off to the bridge. The plug
# is sourced in this script's context so it sees PROJECT / RUN_DIR / SKILL_DIR /
# PAIRS / INPUT / SESSION_ID and the helpers sourced above; it may exit 0
# (codex does, having no Monitor tool) to skip the Monitor-directive path below.
agmsg_session_start_default() { :; }

_tdir="$(agmsg_type_dir "$TYPE" 2>/dev/null || true)"
if [ -n "$_tdir" ] && [ -f "$_tdir/_session-start.sh" ]; then
  # shellcheck disable=SC1090
  . "$_tdir/_session-start.sh"
sed: ~/.agents/skills/agmsg/scripts/lib/common.sh: No such file or directory
#!/bin/bash

# @file home/dot_claude/hooks/executable_project-map-reload.sh
# @brief Reload the visible project map after a Claude file edit.
# @description
#   Pass CDP on both calls to avoid terminal-browser issue 60.
#   Pin tab selection and guard reloads against navigation away from a project map.
#   Match the event file path before choosing an existing map tab.
#   Canonicalize event paths and file URLs with the installed isolated Python stdlib.
#   Reject encoded URL separators before decoding them into filesystem paths.
#   Bind the reload guard to the canonical-matched URL, encoded as a JSON string.
#   Open a separate right split using half the width when the parsed listing yields no map tab.
#   shortcut: rejected map metadata or racing writes can open another pane; tighten selection in the hook follow-up.
# @exitcode 0 Always, including unavailable tools or browsers.

# @description Return the physical absolute path of a local path or file URL.
# @arg $1 path Event path or file URL, including home and relative forms.
# @stdout Canonical path.
canonical_path() {
    python3 -I -S -c '
import os
import sys
from urllib.parse import unquote, urlsplit

path = sys.argv[1]
if path.startswith("file://"):
    url = urlsplit(path)
    if url.netloc not in ("", "localhost") or "%2f" in url.path.lower():
        sys.exit(1)
    path = unquote(url.path, errors="strict")
if path == "~" or path.startswith("~/"):
    path = os.path.expanduser("~") + path[1:]
print(os.path.realpath(path))
' "$1" 2>/dev/null
}

file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
[[ -n "$file_path" ]] || exit 0
event_path=$(canonical_path "$file_path") || exit 0
[[ "$event_path" == */.project-map/index.html ]] || exit 0

listing=$(terminal-browser ls --all --json 2>/dev/null) || exit 0
candidates=$(jq -c '
    [.browsers[]? | .cdpPort as $port
     | select($port | type == "number")
     | select($port >= 1 and $port <= 65535 and $port == ($port | floor))
     | .tabs[]?
     | select(.url | strings | startswith("file://"))
     | select(.targetId | strings | test("^[A-Fa-f0-9]{32}\\z"))
     | [$port, .targetId, .url]][]
' <<< "$listing" 2>/dev/null) || exit 0
selection=""
while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    tab_path=$(canonical_path "$(jq -r '.[2]' <<< "$candidate")") || continue
    [[ "$tab_path" == "$event_path" ]] || continue
    selection=$(jq -r '.[0:2] | @tsv' <<< "$candidate")
    selected_url=$(jq -c '.[2]' <<< "$candidate")
    break
done <<< "$candidates"
if [[ -z "$selection" ]]; then
    terminal-browser open "$file_path" --split right --size 0.5 --no-merge >/dev/null 2>&1
    exit 0
fi
IFS=$'\t' read -r port target_id <<< "$selection"

agent="${TERMINAL_BROWSER_AGENT:-$HOME/.local/share/terminal-browser/app/agent-browser/bin/agent-browser}"
"$agent" --cdp "$port" --session project-map-reload --pin-tab tab "$target_id" >/dev/null 2>&1 || exit 0
"$agent" --cdp "$port" --session project-map-reload --pin-tab eval "if (location.href === new URL($selected_url).href) location.reload()" >/dev/null 2>&1
exit 0

**Questioning Agmsg language**
codex
The revised PermissionRequest command now binds both uv and Python, addressing the previous shebang failure. I’m checking the unchanged delivery and project-hook descendants next: a valid entrypoint alone does not establish that every child command can run under the new PATH.

exec
/bin/zsh -lc "rg -n '\\b(jq|python3|node|sqlite3|git|agmsg)\\b' ~/.agents/skills/agmsg/scripts/identities.sh ~/.agents/skills/agmsg/scripts/lib/storage.sh ~/.agents/skills/agmsg/scripts/lib/compat.sh ~/.agents/skills/agmsg/scripts/drivers/partition/shared.sh ~/.agents/skills/agmsg/scripts/lib/node.sh; sed -n '1,150p' ~/.agents/skills/agmsg/scripts/identities.sh; sed -n '1,100p' ~/.agents/skills/agmsg/scripts/lib/compat.sh; /usr/bin/env -i PATH=/usr/bin:/bin /bin/sh -c 'for tool in bash jq sqlite3 python3 node git; do command -v \""'$tool" || :; done'"'" in ~/Workspace/dotfiles
 succeeded in 68ms:
~/.agents/skills/agmsg/scripts/drivers/partition/shared.sh:6:# directly rather than going through agmsg, and they find their messages by
~/.agents/skills/agmsg/scripts/lib/compat.sh:2:# compat.sh — Platform compatibility shim for agmsg on MSYS2/Windows.
~/.agents/skills/agmsg/scripts/lib/compat.sh:74:#   "C:\Program Files\nodejs\node.exe" C:/Users/.../internal/remote-sync.mjs run --team ossb
~/.agents/skills/agmsg/scripts/lib/compat.sh:172:    sqlite3 :memory: "SELECT lower(
~/.agents/skills/agmsg/scripts/lib/storage.sh:103:# Echo the full path to a team's message store, in a form sqlite3 can open.
~/.agents/skills/agmsg/scripts/lib/storage.sh:105:# Echo the full path to a team's message store, in a form sqlite3 can open.
~/.agents/skills/agmsg/scripts/lib/storage.sh:156:# sqlite3+tr several times over, while still re-reading fresh at the start of
~/.agents/skills/agmsg/scripts/lib/storage.sh:245:# On Windows, sqlite3.exe is a native binary that cannot open a Git Bash path
~/.agents/skills/agmsg/scripts/lib/storage.sh:249:# the shell's `[ -f "$db" ]` test AND sqlite3.exe accept — unlike -w's backslash
~/.agents/skills/agmsg/scripts/lib/storage.sh:286:# Run sqlite3 against the message store with a busy_timeout, so a writer that
~/.agents/skills/agmsg/scripts/lib/storage.sh:292:# this wrapper. In-memory JSON parsing (`sqlite3 :memory:`) does not need it —
~/.agents/skills/agmsg/scripts/lib/storage.sh:297:# PRAGMA returns its value as a row, which sqlite3 would print to stdout and
~/.agents/skills/agmsg/scripts/lib/storage.sh:300:# sqlite3 >= 3.50 renders control bytes in CLI output using caret notation —
~/.agents/skills/agmsg/scripts/lib/storage.sh:304:# sqlite3 >= 3.50 escaping behaviour behind #143. `-escape off` restores the
~/.agents/skills/agmsg/scripts/lib/storage.sh:305:# raw bytes. Older sqlite3 (< 3.50) doesn't know the option (and emits raw bytes
~/.agents/skills/agmsg/scripts/lib/storage.sh:312:    if sqlite3 -escape off :memory: "SELECT 1;" >/dev/null 2>&1; then
~/.agents/skills/agmsg/scripts/lib/storage.sh:321:# `agmsg_sqlite` memoises the probe so it costs one sqlite3 process per shell
~/.agents/skills/agmsg/scripts/lib/storage.sh:325:# call after it probes again -- measured at two sqlite3 processes per call, and
~/.agents/skills/agmsg/scripts/lib/storage.sh:338:  # the probe re-ran on every call — two sqlite3 processes per database access
~/.agents/skills/agmsg/scripts/lib/storage.sh:347:  # Windows' sqlite3.exe (measured: 3.53.4) ends each row of a multi-row
~/.agents/skills/agmsg/scripts/lib/storage.sh:350:  # `-escape` probe above (#102/#143: that is sqlite3 >= 3.50's own caret-
~/.agents/skills/agmsg/scripts/lib/storage.sh:353:  # the Windows C runtime's stdio text-mode translation rewrites sqlite3's
~/.agents/skills/agmsg/scripts/lib/storage.sh:380:  # status is sqlite3's, not sed's, without changing pipefail for the
~/.agents/skills/agmsg/scripts/lib/storage.sh:387:    sqlite3 $_AGMSG_ESCAPE_FLAG -cmd ".timeout ${AGMSG_BUSY_TIMEOUT:-5000}" "$@" | sed $'s/\r$//'
~/.agents/skills/agmsg/scripts/lib/storage.sh:396:    echo "agmsg: the message store is busy: this call waited ${AGMSG_BUSY_TIMEOUT:-5000}ms behind another writer (a sync engine cycle may be running) and gave up (#1001)" >&2
~/.agents/skills/agmsg/scripts/lib/storage.sh:403:# timeout above ran out (sqlite3 said "database is locked"); `failed` for
~/.agents/skills/agmsg/scripts/lib/storage.sh:420:# non-recording path above (Windows' sqlite3.exe row-separator \r\n; see that
~/.agents/skills/agmsg/scripts/lib/storage.sh:428:# The original fd-3 passthrough trick (sqlite3's own fd 1 repointed at
~/.agents/skills/agmsg/scripts/lib/storage.sh:432:# from `${PIPESTATUS[0]}` (sqlite3's, not sed's) rather than the substitution's
~/.agents/skills/agmsg/scripts/lib/storage.sh:443:# `${PIPESTATUS[0]}` (sqlite3's exit status, not sed's) is read in BOTH
~/.agents/skills/agmsg/scripts/lib/storage.sh:450:# sqlite3's. The CRLF fix's own `|| true` above is fine BECAUSE that call
~/.agents/skills/agmsg/scripts/lib/storage.sh:466:  errfile=$(mktemp "${TMPDIR:-/tmp}/agmsg-sqlite-recording-err.XXXXXX" 2>/dev/null) || errfile=/dev/null
~/.agents/skills/agmsg/scripts/lib/storage.sh:468:  if sqlite3 $_AGMSG_ESCAPE_FLAG -cmd ".timeout ${AGMSG_BUSY_TIMEOUT:-5000}" "$@" 2>"$errfile" | sed $'s/\r$//'; then
~/.agents/skills/agmsg/scripts/lib/storage.sh:553:# a command substitution ($(...)). On Windows, sqlite3.exe writes stdout in text
~/.agents/skills/agmsg/scripts/lib/storage.sh:561:  sqlite3 :memory: "$@" | tr -d '\r'
~/.agents/skills/agmsg/scripts/lib/storage.sh:593:  printf '%s\n' "${AGMSG_CONFIG:-$HOME/.agents/agmsg/config.json}"
~/.agents/skills/agmsg/scripts/lib/storage.sh:605:    name="$(sqlite3 :memory: \
~/.agents/skills/agmsg/scripts/lib/storage.sh:645:  printf 'agmsg: no trusted storage driver "%s" found\n' "$name" >&2
~/.agents/skills/agmsg/scripts/lib/node.sh:7:# via the `#!/usr/bin/env node` shebang, and Codex monitor silently never starts.
~/.agents/skills/agmsg/scripts/lib/node.sh:12:# bare "node" so the behaviour is never worse than relying on PATH today (the
~/.agents/skills/agmsg/scripts/lib/node.sh:28:  if command -v node >/dev/null 2>&1; then
~/.agents/skills/agmsg/scripts/lib/node.sh:29:    command -v node
~/.agents/skills/agmsg/scripts/lib/node.sh:39:    "$HOME"/.nvm/versions/node/*/bin/node \
~/.agents/skills/agmsg/scripts/lib/node.sh:40:    "$HOME"/.fnm/node-versions/*/installation/bin/node \
~/.agents/skills/agmsg/scripts/lib/node.sh:41:    "$HOME"/.local/share/fnm/node-versions/*/installation/bin/node; do
~/.agents/skills/agmsg/scripts/lib/node.sh:52:  for n in "$HOME/.volta/bin/node" /opt/homebrew/bin/node /usr/local/bin/node /usr/bin/node; do
~/.agents/skills/agmsg/scripts/lib/node.sh:59:  printf '%s\n' "node"
~/.agents/skills/agmsg/scripts/lib/node.sh:65:# the bare string "node" even when nothing was found), so callers that need
~/.agents/skills/agmsg/scripts/lib/node.sh:73:  local node; node="$(agmsg_resolve_node)"
~/.agents/skills/agmsg/scripts/lib/node.sh:74:  if [ "${node#*/}" != "$node" ]; then
~/.agents/skills/agmsg/scripts/lib/node.sh:75:    [ -x "$node" ]
~/.agents/skills/agmsg/scripts/lib/node.sh:77:    command -v "$node" >/dev/null 2>&1
~/.agents/skills/agmsg/scripts/identities.sh:43:  sqlite3 -separator $'\t' :memory: "
#!/usr/bin/env bash
set -euo pipefail

# List (team, agent) pairs registered for a given (project_path, agent_type).
#
# Usage: identities.sh <project_path> <agent_type>
#
# Output: one "<team>\t<agent>" line per registered pair, tab-separated.
# Empty output (and exit 0) when no pair matches. Pairs are deduplicated.
#
# Used by:
#   - whoami.sh        — exact-match enumeration for identity resolution
#   - watch.sh         — subscription set for the monitor delivery mode
#   - check-inbox.sh   — turn-mode fallback enumeration

PROJECT_PATH="${1:?Usage: identities.sh <project_path> <agent_type>}"
AGENT_TYPE="${2:?Missing agent_type}"
AGENT_TYPE_SQL=$(printf '%s' "$AGENT_TYPE" | sed "s/'/''/g")

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"  # resolve-project.sh requires SKILL_DIR
TEAMS_DIR="$SCRIPT_DIR/../teams"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/resolve-project.sh"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/lib/storage.sh"
PROJECT_SQL_IN=$(agmsg_project_sql_in_list "$PROJECT_PATH")

[ -d "$TEAMS_DIR" ] || exit 0

for config_file in "$TEAMS_DIR"/*/config.json; do
  [ -f "$config_file" ] || continue
  cfg_sql=$(agmsg_sql_readfile_path "$config_file")
  TEAM_NAME=$(agmsg_sqlite_mem "
    WITH raw(json) AS (SELECT CAST(readfile('$cfg_sql') AS TEXT)),
    cfg(json) AS (SELECT CASE WHEN json_valid(json) THEN json END FROM raw)
    SELECT json_extract(json, '\$.name') FROM cfg;
  ")
  [ -z "$TEAM_NAME" ] && continue
  [ "$TEAM_NAME" = "null" ] && continue
  TEAM_SQL=$(printf '%s' "$TEAM_NAME" | sed "s/'/''/g")

  sqlite3 -separator $'\t' :memory: "
    WITH raw(json) AS (SELECT CAST(readfile('$cfg_sql') AS TEXT)),
    cfg(json) AS (SELECT CASE WHEN json_valid(json) THEN json END FROM raw),
    agents AS (
      SELECT
        key AS name,
        CASE
          WHEN json_type(json_extract(value, '\$.registrations')) = 'array' THEN json_extract(value, '\$.registrations')
          ELSE json_array(json_object('type', json_extract(value, '\$.type'), 'project', json_extract(value, '\$.project')))
        END AS registrations
      FROM cfg, json_each(json_extract(cfg.json, '\$.agents'))
    )
    SELECT DISTINCT '$TEAM_SQL' AS team, name
    FROM agents, json_each(agents.registrations) AS r
    WHERE json_extract(r.value, '\$.project') IN ($PROJECT_SQL_IN)
      AND json_extract(r.value, '\$.type') = '$AGENT_TYPE_SQL'
    ORDER BY team, name;
  " | tr -d '\r'
done
#!/usr/bin/env bash
# compat.sh — Platform compatibility shim for agmsg on MSYS2/Windows.
#
# MSYS2's ps does not support POSIX -o flags (ppid=, args=, comm=), uuidgen
# may be absent, and stat flags differ across platforms. This shim provides
# portable wrappers so the rest of the scripts need not branch per-platform.
#
# Usage: source this file early; call _agmsg_detect_platform (or let the
#        wrappers lazy-init it), then use compat_* functions.

_agmsg_platform=""

_agmsg_detect_platform() {
  [ -n "$_agmsg_platform" ] && return
  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) _agmsg_platform="msys"  ;;
    Darwin*)               _agmsg_platform="macos" ;;
    *)                     _agmsg_platform="linux" ;;
  esac
}

# Get parent PID of a process.  Replaces: ps -o ppid= -p <pid>
compat_get_ppid() {
  local pid="$1"
  [ -z "$pid" ] && return 1
  _agmsg_detect_platform
  case "$_agmsg_platform" in
    msys)
      ps -l -p "$pid" 2>/dev/null | awk '
        NR==1 { for (i = 1; i <= NF; i++) if ($i == "PPID") col = i; next }
        NR==2 && col { print $col }
      '
      ;;
    *)
      ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' '
      ;;
  esac
}

# Get Windows PID (WINPID) for an MSYS2 process.  Internal helper.
_compat_get_winpid() {
  local pid="$1"
  ps -l -p "$pid" 2>/dev/null | awk '
    NR==1 { for (i = 1; i <= NF; i++) if ($i == "WINPID") col = i; next }
    NR==2 && col { print $col }
  '
}

# Query Windows CIM for the full command line of a process by WINPID.
_compat_cim_cmdline() {
  local winpid="$1"
  [ -n "$winpid" ] || return 1
  case "$winpid" in *[!0-9]*) return 1 ;; esac
  [ -z "${_AGMSG_COMPAT_NO_CIM:-}" ] || return 1
  powershell.exe -NoProfile -Command \
    "(Get-CimInstance Win32_Process -Filter \"ProcessId=$winpid\").CommandLine" 2>/dev/null \
    | tr -d '\r' | tr '\\' '/'
}

# Get full command line of a process.  Replaces: ps -o args= -p <pid>
# Does <cmdline> name <path>?
#
# It has to be asked as a function because the two sides are written in
# different alphabets and only one of them is ours. `compat_get_cmdline` returns
# what the OS says a process was started with; the path we compare it against
# came out of this shell. Under Git Bash those disagree for the same file:
# `$SKILL_DIR` is `/c/Users/...`, and a native binary launched from it reports
# `C:/Users/...`. A `case` on one against the other never fires -- so every
# check built that way answers "not ours" about a process that IS ours, and
# does it silently, because a non-match is the ordinary answer.
#
# Measured on the reporting machine (#652): the sync engine was alive, its
# `/proc/<pid>/cmdline` read
#   "C:\Program Files\nodejs\node.exe" C:/Users/.../internal/remote-sync.mjs run --team ossb
# while the comparison held /c/Users/.../internal/remote-sync.mjs. Forcing the
# CIM source instead of /proc returned the same `C:/` form, so this is not about
# where the cmdline is read from -- both sources speak Windows.
#
# Five call sites compared a shell path against an OS cmdline this way. Four of
# them decide whether to kill a stale watcher, so on Windows they answered "not
# ours" and left it running.
#
# `cygpath -m` is the mixed form -- `C:/Users/...`, forward slashes -- which is
# what MSYS hands a native binary, and therefore what the process reports.
# Off Windows there is no cygpath and this is the plain match and nothing else,
# the same escape `agmsg_sql_readfile_path` takes.
agmsg_cmdline_names_path() {
  local cmdline="$1" path="$2" native
  [ -n "$cmdline" ] && [ -n "$path" ] || return 1
  case "$cmdline" in *"$path"*) return 0 ;; esac
  command -v cygpath >/dev/null 2>&1 || return 1
  native="$(cygpath -m "$path" 2>/dev/null || true)"
  [ -n "$native" ] || return 1
  # Identical forms would make this second look a copy of the first, not a
  # second chance at it.
  [ "$native" != "$path" ] || return 1
  case "$cmdline" in *"$native"*) return 0 ;; esac
  return 1
}

/bin/bash
/usr/bin/jq
/usr/bin/sqlite3
/usr/bin/python3
/usr/bin/git

**Verifying system and script setup**
**Evaluating path resolution and residual risks**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | sed -n '490,650p'; shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-435275a.md.last.md; sed -n '1,55p' home/dot_local/bin/common/executable_permgate; sed -n '1,95p' ~/.agents/skills/agmsg/scripts/lib/node.sh; rg -n 'agmsg_resolve_node|agmsg_node|AGMSG_NODE' ~/.agents/skills/agmsg/scripts/session-start.sh ~/.agents/skills/agmsg/scripts/check-inbox.sh ~/.agents/skills/agmsg/scripts/drivers/types/claude-code" in ~/Workspace/dotfiles
 succeeded in 53ms:
   490	`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` is green. The validation record contains every named red-then-green selector and the complete final module run.
   491	
   492	The final diff has at most 700 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`. It has at most 950 changed lines under `tests/`. Changed lines are additions plus deletions. The validation record includes per-file numstat, base and head identities and both totals.
   493	
   494	The validation record contains exact commands, verbatim outputs, exit statuses and tested identities. Git commands producing that evidence follow section 5.14 item 2.
   495	
   496	Both platform renders show separate worker and orchestrator user settings, exact manifest deny-inventory correspondence, filesystem coverage of current tracked top-level source paths, both worklog denies, ordinary worktree writes, the worktree `.claude` and `.mcp.json` denies, narrow home denies, writable agmsg stores, empty worker user exclusions, restricted worker writes and `failIfUnavailable: true` for every Claude seat.
   497	
   498	Managed render evidence asserts sandbox enablement, startup failure, disabled unsandboxed retries, the required anti-weakening Boolean values, exactly the three rendered control-plane exclusions and exactly the Herdr socket allowance. Conflicting project and local fixtures leave that render unchanged. The evidence names the documented enforcement scope without claiming live runtime verification.
   499	
   500	Staging evidence shows the home-directory output and exact printed `sudo install -m 0644` command with the detected administrative destination on both macOS and Linux. The temporary-HOME test proves that the target executes no sudo command.
   501	
   502	Hook evidence inventories every generated and tracked entry, its `onFailure` value, `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix (with template-rendered absolute HOME for PermissionRequest), installed script, absolute entrypoint interpreter and reached descendants. It includes the new render/runtime selector's actual exit status and parsed permgate decision under `PATH=/usr/bin:/bin`, plus first-word and post-env-assignment executable checks for every rendered hook command. It states the portable tracked-command and per-host-rendered-binding split, verifies HOME re-export before HOME-relative paths and shows that tracked commands name no interpreter or anchor path. It includes worker user settings and main-checkout local settings. Render evidence shows that `ruff`, `prettier` and `terminal-browser` resolve under the guard's rendered orchestrator tool PATH on the rendering host and that no PATH entry is a shims directory. Merged-settings evidence identifies runtime-added entries separately. No report claims complete effective failure-policy coverage from template inspection alone.
   503	
   504	Launch evidence shows both cache variables reaching the actual worker process on every route. Claude processes additionally receive the dedicated Claude configuration directory. Repeated-start evidence shows replacement of stale managed hooks, retained native merge denials and the unchanged Codex sandbox and approval arguments.
   505	
   506	Linked-worktree evidence shows worker hooks in the worker configuration directory's user settings and no new worker-local `.claude/settings.local.json`. Guard markers show that the main checkout's local agmsg and attachment hooks execute no payload under worker launch roots.
   507	
   508	Guard markers also show that worker project scripts, contextdb hooks, Stop gates and formatter payloads do not execute through tracked hooks. Descendant markers show that planted PATH interpreters do not execute on the tested hook routes, including an upstream-style `/usr/bin/env bash` descendant.
   509	
   510	The report separately identifies the writable agmsg store's current driver-selection route and `dotfiles-T133-agmsg-hardening-a01` ownership. Hook interpreter tests do not claim to close that residual.
   511	
   512	The report states the GitHub API ledger rule without claiming this task implements the permission guard or the P1-11 next-records-PR regime check. It states detection, not prevention, and records D-024-23's future P1-16 decision. It also records shared managed exclusions and Herdr socket access, same-UID credential access, path-consumption residuals, external-process trust, hook-event failure limitations and the retained Codex shared Git grant.
   513	
   514	No local Bats tests run. Required Bats results come from GitHub Actions. Failed required checks retain their actual output and receive an in-scope fix before RESULT.
   515	
   516	The orchestrator runs `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md` before dispatch and at acceptance. C1 to C10 and C7b pass.
   517	
   518	A C-80 security-profile context reviews this complete revised text before dispatch. That review is a dispatch prerequisite and is not claimed as a result of this draft.
   519	
   520	## Completion
   521	
   522	One implementation PR continues the existing branch `tools/worker-write-boundary-a01`, created from clean base `205fe85c`, on the Codex seat a010. The eight green tests, fixtures and evidence stay. The first push deletes the predecessor copy `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md` and adds the byte-identical dispatched a02 task at `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md`. This predecessor-copy deletion is the sole authorized edit to the predecessor's artifact directory.
   523	
   524	The Completion clauses of `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` apply with this task's branch, files and evidence paths, `dotfiles-T133-worker-write-boundary-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md>` in RESULT. The a05-specific continuation of PR #420, predecessor-copy deletion, inherited counters, deadline and implementation requirements do not transfer. The orchestrator writes the follow-up owner task before assigning its first advisory P2.
   525	
   526	Every worker-side fix round counts toward INV-6. The worker's own pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration. The worker starts no additional private correction-and-review cycle to avoid reporting it.
   527	
   528	No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item carries its proposed disposition, and surviving P0/P1 findings remain open for the operator's decision.
   529	
   530	Every gh write and every git write runs as a separate command without shell chaining. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG with the exact command and boundary.
   531	
   532	The Codex worker writes evidence at the required relative paths in its own worktree and says so in RESULT. Worker review evidence uses the `-worker-` infix. Crit-data evidence and its receipt follow repository rules without a browser review or human review request. The orchestrator copies evidence by absolute path before acceptance.
   533	
   534	`AGMSG-RESULT v1` names the final head, base, branch, changed files, new deployable scripts, source and installed paths, trusted anchor, interpreter and descendant inventory, hook PATH bindings, user and administrative settings destinations, staging path and printed installation command, Bot findings and proposed dispositions, open P0/P1 findings, exact test selectors, measured caps, task-copy SHA256 and evidence paths. It distinguishes historical observations from final-head results and names all pending operator steps.
   535	
   536	The report states the user-visible effects. Claude workers use `~/.claude-worker` and require its own Claude login. Worker trusted-path and worktree-configuration Edit denies also affect Bash sandbox writes. Agmsg store paths remain writable except `~/.agents/skills/agmsg/db/trusted-plugins`, and worker denies also cover `~/.agents/skills/agmsg/plugins/**`. Worker user settings add no excluded commands or Herdr socket allowance, while shared managed settings retain the three control-plane exclusions and Herdr socket for every seat. Tracked and main-local orchestrator project hooks are no-ops in worker sessions. Worker caches are private. Every Claude seat fails when its sandbox is unavailable.
   537	
   538	Administrative managed settings require sandboxing for the orchestrator as well as workers and disable unsandboxed retries. The former Linux gh exemption is removed. The orchestrator retains its existing functions within those requirements and the specified hook failure, guarding and interpreter/PATH-binding changes.
   539	
   540	The report states that no gh credential separation is established. Shared credentials permit worker-initiated API merges despite native command denials. The GitHub boundary is detection, not prevention, with the required next-records-PR regime check owned by P1-11.
   541	
   542	This task is `security: true`. The orchestrator obtains the task-level audit and a separate security-profile review of the final implementation head. The finding-class record includes `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. A third non-advisory finding of one class stops the artifact for redesign under the inherited completion rules.
   543	
   544	Final-head feedback collection, task-level audit, finding dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. Changed heads receive fresh required evidence. The final-head security review precedes the gate.
   545	
   546	The permission-surface change receives the required operator-backed approval through the repository's existing process. The worker writes no approval row and treats no candidate-tree decision as authority.
   547	
   548	Live deployment is the operator's post-merge `make update`. The operator runs `make install-managed-settings`, inspects the rendered staging file and executes its printed `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` command with `/Library/Application Support/ClaudeCode/managed-settings.json` detected on macOS and `/etc/claude-code/managed-settings.json` detected on Linux. Administrative installation is recorded separately from staging and ordinary chezmoi application.
   549	
   550	The operator performs the Claude worker-directory login with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected.
   551	
   552	The operator applies the prepared deterministic Codex permgate rule that stops approving sandbox escapes and restarts affected sessions.
   553	
   554	The deployment record checks effective settings after `make update` and administrative installation, including hooks added by merge scripts or integration installers. It verifies the installed managed-settings content, admin-required sandbox scope, worker directory, both platform policy outputs, static deny inventory, worktree-configuration denies, writable agmsg stores, worker-user and main-local hook placement, hook PATH and interpreter descendants, failure-policy coverage and sandbox startup without exposing credentials.
   555	
   556	The effective-settings check includes conflicting project and local sandbox relaxations and confirms that they do not weaken the administrative policy. It also records the shared control-plane exclusions and Herdr socket as available capabilities. It makes no claim that worker user arrays subtract those entries.
   557	
   558	Merge alone does not establish deployment readiness. The orchestrator records `make update`, the managed-settings installation with sudo, the Claude worker-directory login, effective startup checks and the Codex permgate rule before releasing dependent hardening tasks for live operation. The upstream agmsg store-driver route remains a named residual until its owning task is implemented. GitHub remains detection, not prevention, until the operator pursues separate-user or separate-host isolation under future P1-16.
   559	
   560	## Checks (pasted by the orchestrator before each send)
   561	
   562	```
   563	amendment 2, 2026-10-19T08:1xZ; task-consistency-check.py: OK; C-80 text security review of this text: .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-db2a8f9.md.last.md Verdict: correct (amendment 1: e5d1b57 correct)
   564	task=dotfiles-T133-worker-write-boundary-a01 tasks=2 amendments=1 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-19T05:42:14Z..none (-) source=live
   565	detail: pr=none authors=claude-deep-dot tasks=01a152ae-8ef0-784f-801e-d4c9a4f3007f,01a152ed-0b08-7431-8fd0-5b5e43c89bd6 results=- questions=- withdrawn=- bot_heads=- source=live
   566	```
   567	
   568	Local Bats, live enforcement, administrative installation, worker-directory login, permgate policy changes and deployment are not performed by the worker.
   569	Deployment remains unverified until the operator completes the post-merge steps; same-UID credential access, shared control-plane exclusions and Herdr socket access, writable-store driver selection and concurrent path consumption remain stated residuals.8520998f2f3fc88c5cda5af23371faa72dd5ff3a1e5359364907e67968e73c3e  .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md

 exited 1 in 90ms:
No actionable findings in this revision. All 19 `allowed_files` entries are represented across 43 threat rows; none claims closure from configuration tests alone. The design distinguishes its controls from the acknowledged same-UID, shared-capability, agmsg sourcing and path-race residuals. Its enforcement claims match the documented [managed sandbox scope](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) and [symlink checks](https://code.claude.com/docs/en/permissions#symlinks).

📝 まとめ: Reviewed the task, every threat row and cited acceptance/review context. No files changed; acceptance remains the orchestrator’s decision.

Not checked: implementation tests or live deployment; the stated residuals remain.
Verdict: correct#!/usr/bin/env -S uv run --no-cache --script
"""Deterministic permission gate for Claude Code and Codex."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SENTINEL_ENV = "PERMGATE_INNER"
SHELL_CONTROL = re.compile(r"[;&|><`\n]|\$\(")
SHELL_EXPANSION = re.compile(r"[$*?\[\]{}~]")
UNSAFE_READ_OPTIONS = {
    "--ext-diff",
    "--hostname-bin",
    "--no-index",
    "--open-files-in-pager",
    "--output",
    "--pre",
    "--textconv",
    "--watch",
    "--web",
    "-O",
    "-w",
}
SUMMARY_COMMANDS = {
    "ccgate",
    "chezmoi",
    "claude",
    "codex",
    "crit",
    "gh",
    "git",
    "herdr",
    "jq",
    "make",
    "mise",
    "npm",
    "node",
    "pgrep",
    "pnpm",
    "ps",
    "python3",
    "rg",
    "sysctl",
    "uv",
}
#!/usr/bin/env bash
# Resolve a Node binary to run codex-bridge.js.
#
# The bridge is a Node program, but a version-manager Node (nvm / fnm / volta) is
# only placed on PATH by an interactive shell's init. A bridge launched from a
# non-interactive context — e.g. a spawn boot script — therefore cannot find it
# via the `#!/usr/bin/env node` shebang, and Codex monitor silently never starts.
#
# Search order: an explicit override (AGMSG_NODE, then AGMSG_CODEX_NODE for
# back-compat) → active PATH (honours a loaded version manager) → common
# version-manager / system locations (newest nvm/fnm version first). Falls back to
# bare "node" so the behaviour is never worse than relying on PATH today (the
# caller still fails the same way, with the existing delivery.sh preflight
# warning). See #170.
agmsg_resolve_node() {
  # An explicit override is authoritative — return it verbatim, even if it does
  # not exist, so the caller's preflight surfaces a misconfigured value rather
  # than silently falling back. AGMSG_NODE is the canonical name; AGMSG_CODEX_NODE
  # is kept for back-compat with the delivery.sh preflight.
  if [ -n "${AGMSG_NODE:-}" ]; then
    printf '%s\n' "$AGMSG_NODE"
    return 0
  fi
  if [ -n "${AGMSG_CODEX_NODE:-}" ]; then
    printf '%s\n' "$AGMSG_CODEX_NODE"
    return 0
  fi
  if command -v node >/dev/null 2>&1; then
    command -v node
    return 0
  fi

  # Glob the version-manager dirs directly in the for-list (expands in both bash
  # and zsh, unlike an unquoted glob held in a variable). Keep the newest match
  # by version sort. Unmatched globs iterate once as the literal pattern, which
  # the -x test rejects.
  local n best=""
  for n in \
    "$HOME"/.nvm/versions/node/*/bin/node \
    "$HOME"/.fnm/node-versions/*/installation/bin/node \
    "$HOME"/.local/share/fnm/node-versions/*/installation/bin/node; do
    [ -x "$n" ] || continue
    if [ -z "$best" ] || [ "$(printf '%s\n%s\n' "$best" "$n" | sort -V | tail -1)" = "$n" ]; then
      best="$n"
    fi
  done
  if [ -n "$best" ]; then
    printf '%s\n' "$best"
    return 0
  fi

  for n in "$HOME/.volta/bin/node" /opt/homebrew/bin/node /usr/local/bin/node /usr/bin/node; do
    if [ -x "$n" ]; then
      printf '%s\n' "$n"
      return 0
    fi
  done

  printf '%s\n' "node"
  return 0
}

# agmsg_node_usable -- 0 if agmsg_resolve_node's answer is actually usable,
# 1 otherwise. agmsg_resolve_node always returns SOMETHING (falling back to
# the bare string "node" even when nothing was found), so callers that need
# to know whether Node is genuinely available (e.g. a doctor/preflight
# check) must not treat a non-empty return value alone as success. Same
# path-vs-bare-name idiom already used by
# scripts/drivers/storage/jsonl.sh's _jsonl_sync_available, pulled up here
# so every caller shares one resolution+usability contract instead of each
# reimplementing its own judgment of what "usable" means.
agmsg_node_usable() {
  local node; node="$(agmsg_resolve_node)"
  if [ "${node#*/}" != "$node" ]; then
    [ -x "$node" ]
  else
    command -v "$node" >/dev/null 2>&1
  fi
}

**Reviewing Python template generator setup**
**Analyzing shell expansion risks in script**

I'm examining how shlex handles shell expansions, especially around quoted variables that might allow command injection. The `${CLAUDE_PROJECT_DIR}` placeholder uses textual substitution, which could risk injection if shell metacharacters are present unquoted. The documentation shows this is speculative but worth a close look. I confirm offline policies disallow dependencies, so real tests are essential now added. I'll produce a concise summary referencing sources and finalize with a clear verdict, noting two lines of limitations and the final assessment. Counting matches carefully ensures accuracy.
exec
/bin/zsh -lc "python3 -I -c 'from pathlib import Path; import hashlib; p=Path(\".orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md\"); b=p.read_bytes(); s=b.decode(); allowed=s.split(\"allowed_files:\\n\",1)[1].split(\"after:\",1)[0]; table=s.split(\"threat_table:\\n\",1)[1].split(\"premises:\",1)[0]; print(\"allowed_files:\",sum(l.startswith(\"  - \") for l in allowed.splitlines())); print(\"threat_rows:\",sum(l.startswith(\"  - control:\") for l in table.splitlines())); print(\"closed_rows:\",table.count(\"disposition: \\\"closed:\")); print(\"missing_path_rows:\",[l.strip()[2:] for l in allowed.splitlines() if l.startswith(\"  - \") and l.strip()[2:] not in table]); print(\"sha256:\",hashlib.sha256(b).hexdigest())'" in ~/Workspace/dotfiles
 succeeded in 31ms:
allowed_files: 22
threat_rows: 46
closed_rows: 0
missing_path_rows: []
sha256: 8520998f2f3fc88c5cda5af23371faa72dd5ff3a1e5359364907e67968e73c3e

codex
No actionable findings in the stated design. All 22 allowed paths are covered across 46 threat rows; none claims `closed`. The revised PermissionRequest contract binds uv and Python and requires actual execution under the sanitized PATH.

The controls distinguish execution binding from the acknowledged same-user, shared-capability, agmsg sourcing and path-race residuals. Enforcement claims match the documented [managed sandbox scope](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) and [symlink checks](https://code.claude.com/docs/en/permissions#symlinks).

Reviewed task SHA-256: `8520998f2f3fc88c5cda5af23371faa72dd5ff3a1e5359364907e67968e73c3e`.

📝 まとめ: Reviewed every threat row and cited acceptance/review context without changing files; acceptance remains the orchestrator’s decision.

Not checked: implementation tests or live deployment; the explicitly stated residual risks remain.
Verdict: correct
hook: Stop
hook: Stop Completed
tokens used
105,609
No actionable findings in the stated design. All 22 allowed paths are covered across 46 threat rows; none claims `closed`. The revised PermissionRequest contract binds uv and Python and requires actual execution under the sanitized PATH.

The controls distinguish execution binding from the acknowledged same-user, shared-capability, agmsg sourcing and path-race residuals. Enforcement claims match the documented [managed sandbox scope](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) and [symlink checks](https://code.claude.com/docs/en/permissions#symlinks).

Reviewed task SHA-256: `8520998f2f3fc88c5cda5af23371faa72dd5ff3a1e5359364907e67968e73c3e`.

📝 まとめ: Reviewed every threat row and cited acceptance/review context without changing files; acceptance remains the orchestrator’s decision.

Not checked: implementation tests or live deployment; the explicitly stated residual risks remain.
Verdict: correct
