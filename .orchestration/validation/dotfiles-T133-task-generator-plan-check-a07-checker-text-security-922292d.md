Reading additional input from stdin...
OpenAI Codex v0.163.0
--------
workdir: ~/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a15d90-104f-7913-a2fa-15e67f4645df
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
I’ll review the task, threat table, and cited evidence against the host conditions you listed. I’m using the agmsg-orchestration and Ponytail review guidance; this session is read-only, and I can’t switch its model profile mid-session.
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 6ms:
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

- Add and remove parallel workers only with `herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile NAME]` and `herdr-agents --remove-worker <worktree> [--force]` (worktree under `.claude/worktrees/`). For Codex, seat ordinary tasks with `--profile standard`; use `--profile security` only for trust-boundary tasks (permgate, redaction or secret handling, sandbox or permission policy), per the model-selection rule, with an identity such as `codex-security-dot-aNNN`. Add-worker seats the worker in its own tab of the pair workspace, labeled `<team>:<name>` with the pair tab untouched (in its own workspace only when no pair workspace exists, as in the pane-less bring-up), through upstream `spawn.sh --project <worktree> --terminal-driver herdr` with the profile's launch args in a generated spawn options file, so a placement record exists and `poke.sh`/`despawn.sh` work. Remove-worker despawns it, then turns delivery off, leaves, and closes that tab (or workspace), refusing a dirty worktree without `--force`. Keep at most `worker_cap` workers (4 in the manifest today); raw herdr topology commands stay forbidden (T21 G7).
- Under upstream agmsg 1.5.0 self-naming, a pair's panes carry `<team>:<name>` labels rather than `claude-orchestrator`/`<kind>-worker`; `herdr-agents` recognizes the pair through the repository's agmsg seats (the orchestrator identity at the main checkout and the pair's own worker seat, never other team members) and never relabels a self-named pane.
- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
- The orchestrator acts directly, without delegation, only under these exemptions: agmsg/herdr control-plane operations and evidence-sync bookkeeping; acceptance and final integration, including merging an already-reviewed, CI-green PR; and machine-state hygiene that touches no repository (tool-manager operations such as `mise install`/`mise prune`, removal of unmanaged `$HOME` files), provided tracked worktrees stay diff-clean throughout. It declares which exemption applies in one line before mutating anything.
- A parallel assignment is valid only when every concurrent worker has all four of: (1) its own git worktree registered as its agmsg `project`; (2) the shared default agmsg store for same-repository work, never a per-worker `AGMSG_STORAGE_PATH`, because identity-addressed delivery and worktree-specific `whoami` already isolate inboxes and one activation watcher observes every RESULT/PONG without extra watchers (which `watch.sh` actas locking cannot support for one claimed identity); (3) an `-aNNN` identity suffix on every concurrent worker, including the first; and (4) an AGMSG-TASK whose expanded `allowed_files` are pairwise-disjoint from all other in-flight tasks for code files; a shared prose file (README, SKILL) may appear in two in-flight tasks only when their sections do not overlap. The orchestrator verifies disjointness and performs all cross-worktree merge, rebase, and conflict integration.
- Parallel execution procedure:
  - At plan approval, partition the approved tasks into waves by dependency and file overlap: code files pairwise-disjoint, and shared prose files in disjoint sections. Write the wave table into the plan file.
  - Keep at most `worker_cap` workers in total (4 in the manifest today; `herdr-agents --add-worker` refuses the next seat). Seat workers with `herdr-agents --add-worker` only up to that cap. Dispatch at once as many tasks of the current wave as there are free seats, each with a distinct `-aNNN` identity and its own worktree, and queue the rest of the wave.
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
- Only acceptance decisions and final merge stay orchestrator-side. Seats and scripts handle integration, adversarial RESULT review, review-profile work, gate and records through `verdict.sh`, `audit-pool.sh`, `result-precheck.sh`, `acceptance-front-matter.py` and `dispatch.sh --next`. Pending each mechanism, Delegation's interim exemption permits manual orchestrator execution. Every code-changing RESULT gets one task-level audit of its final head; findings are input, never approval (the "Task-level audit" bullet).
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

Task front matter's optional `requires_decision:` lists decision ids without which the task may not proceed. The task-consistency checker verifies each id exists in `.orchestration/decisions.tsv` with a result other than `pending`.

`AGMSG-RESULT v1` fields:

```text
AGMSG-RESULT v1 task_id=<id> status=ready_for_review|blocked
report=<path> validation=<path> sandbox=<path> learning=<path> autoskill=<path>
```

Before sending, the worker writes the RESULT line's `key=value` pairs to `.orchestration/<task>/result.txt`; `result-precheck.sh` reads that file.

Tasks that create persistent side effects outside the repository working tree, such as global asset installs, writes under `$HOME`, or external service registrations, include the optional field `effects=<semicolon-list-of-short-ids>`. In-repository edits within `allowed_files` are not effects. For each declared effect, the report must state its reverse mapping: a named `~/.agents/.installed-manifest.json` step removable with `remove-agent-asset`, a documented removal procedure, or an `irreversible:` statement with rationale.

The RESULT field `precheck=<sha256 of precheck.json>` is the digest of the precheck evidence already emitted by P1-5.

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

The optional PONG field `context=<percent>` reports the seat's context usage. `dispatch.sh --next` reads it and refuses a seat above its context threshold.

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
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md' in ~/Workspace/dotfiles
 succeeded in 12ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a08.md
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
 M .orchestration/acceptance/dotfiles-T133-result-precheck-a03.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md
 M .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-pins-a01.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07-design-reset.md
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a02-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a03.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/
?? .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01/
?? .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02/
?? .orchestration/learning/mistakes/M-20261021-05-codex-run-inside-the-sandbox-after-compaction.md
?? .orchestration/learning/mistakes/M-20261021-06-dispatch-against-the-texts-own-precondition.md
?? .orchestration/learning/mistakes/M-20261021-07-wrong-owner-id-in-the-chain-line.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T128-task-checkers-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a03-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a03.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-1d72f16.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-audit-08b8add.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-chain-08b8add.log
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-08b8add.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-audit-c439b63.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-audit-c439b63.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-c439b63.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-c439b63.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-chain-28dde0f.log
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-local-review-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-1f17d05.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-text-security-0908b8f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-text-security-0908b8f.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-text-security-70feed4.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-text-security-70feed4.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-audit-f66b27f.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-audit-f66b27f.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-chain-f66b27f.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-local-review-f66b27f.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-audit-c8c712f.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-audit-c8c712f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-chain-2d1d095.log
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-chain-c8c712f.log
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-crit.json
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-local-review-2d1d095.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-local-review-c8c712f.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-security-2d1d095.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-security-2d1d095.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-security-c8c712f.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-security-c8c712f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0b96f40.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0b96f40.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0e9bf3f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0e9bf3f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0f87501.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0f87501.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-3844d93.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-3844d93.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-task-generator-plan-check-a07-checker
     4	kind: code
     5	security: true
     6	design: 5.14 items 0-10
     7	design_review:
     8	  design: .orchestration/plans/024-design-quality.md
     9	allowed_files:
    10	  - scripts/orchestrator/task-consistency-check.py
    11	  - tests/unit/test_task_consistency_c11_c15.py
    12	  - tests/unit/test_task_checkers.py
    13	  - .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/**
    14	after: []
    15	reset_of: [dotfiles-T133-task-generator-plan-check-a06-checker]
    16	retained_predecessor_directories:
    17	  - .orchestration/dotfiles-T133-task-generator-plan-check-a04/
    18	  - .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/
    19	  - .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/
    20	expected_result_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/report.md
    21	expected_validation_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/validation.md
    22	expected_sandbox_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/sandbox.md
    23	expected_learning_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/learning.md
    24	expected_autoskill_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/autoskill.md
    25	expected_measure_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/measure.md
    26	threat_table:
    27	  - {control: "scripts/orchestrator/task-consistency-check.py", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retained defenses and final-head fixtures mitigate checker faults; pre-start and same-UID interference remain."}
    28	  - {control: "tests/unit/test_task_consistency_c11_c15.py", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; real-checker fixtures and deterministic models mitigate regressions; native-platform and live-API coverage remain limited."}
    29	  - {control: "tests/unit/test_task_checkers.py", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; preserve historical expectations and compare the full suite against the merge-base in the same environment."}
    30	  - {control: ".orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/**", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; commit .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/task.md byte-identical to dispatch and all evidence; no credentials or runtime helpers."}
    31	  - {control: "predecessor copy .orchestration/dotfiles-T133-task-generator-plan-check-a04/task.md", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain the entire inventoried directory unchanged from c439b63c; historical evidence grants no approval."}
    32	  - {control: "predecessor copy .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task.md", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain the entire inventoried directory unchanged from c439b63c; historical evidence grants no approval."}
    33	  - {control: "predecessor copy .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain the entire inventoried directory unchanged from c439b63c; historical evidence grants no approval."}
    34	  - {control: "checker-side interpreter selection after startup", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_interpreter_resolution_order"}
    35	  - {control: "gh child environment", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_gh_child_preserves_parent_tokens"}
    36	  - {control: "canonical-main design read", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_uses_canonical_main_only"}
    37	  - {control: "C6 canonical receipt binding and design hash", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
    38	  - {control: "fixture and evidence symlink exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_symlink_to_applied_file_is_finding"}
    39	  - {control: "fixture and evidence case-alias exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_case_alias_to_applied_file_is_finding"}
    40	  - {control: "original Unicode path confinement", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_resolves_original_unicode_path"}
    41	  - {control: "internal directory aliases", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_rejects_internal_directory_alias"}
    42	  - {control: "directory pruning name comparison", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_prunes_with_normalised_directory_names"}
    43	  - {control: "path_entry pipeline identity", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_canonical_path_pipeline_rejects_normalised_collisions"}
    44	  - {control: "path grammar and filesystem identity", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; preserve all grammar, confinement and identity fixtures; filesystem models do not establish native coverage."}
    45	  - {control: "C16 reference and item coverage", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c16_requires_reference_and_all_item_rows"}
    46	  - {control: "C16 item occurrence counting", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_rejects_multi_item_rows"}
    47	  - {control: "C16 resolved-target applicability", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_uses_resolved_literal_alias"}
    48	  - {control: "C15 invariants validation", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_rejects_invariants_without_design"}
    49	  - {control: "C14 probe status", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c14_grep_count_no_match_fails"}
    50	  - {control: "C4 directory scope coverage", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c4_requires_separate_directory_scope_rows"}
    51	  - {control: "C12 CLAUDE instruction coverage", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_requires_concrete_claude_rows"}
    52	  - {control: "C8 canonical binary decoding", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c8_handles_binary_canonical_blobs"}
    53	  - {control: "C12 symlink classification", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_classifies_links_and_checks_missing_alias_prefixes"}
    54	  - {control: "missing-literal directory-symlink prefix validation", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_classifies_links_and_checks_missing_alias_prefixes"}
    55	  - {control: "UV_CACHE_DIR refusal", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_refuses_missing_uv_cache_dir"}
    56	  - {control: "case-aliased symlink target relativisation", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_entry_relativises_case_alias_by_identity"}
    57	  - {control: "task metadata", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; orchestrator verifies reset lineage, scope, caps, prerequisites and dispatched-copy identity before acceptance."}
    58	  - {control: "metadata separators", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; the dispatched digest covers the entire file including separators and populated Checks; quoted evidence stays data."}
    59	  - {control: "in-process effects", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain C14 authorization, fixed vocabulary and non-execution controls; existing negative tests limit probe execution."}
    60	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; design 5.14 items 2, 3, 4 and 9 apply by reference; no workflow or caller changes are authorized."}
    61	  - {control: "new or renamed scripts", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; only the existing production checker changes; no resolver, wrapper, dependency or artifact runtime code."}
    62	  - {control: "orchestrator effect dispatch.sh keeps calling the checker unchanged", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain the unchanged-invocation compatibility fixture; design 5.14 items 2, 4 and 9 apply by reference."}
    63	  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; worker never merges; orchestrator applies Playbook step 10 to the final audited head."}
    64	  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; recompute the merge-base and refresh CI, feedback and audit after every head change."}
    65	  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; none assigned; preserve worker state, PR #440 and withdrawn lineage evidence."}
    66	  - {control: "orchestrator effect PR metadata", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; orchestrator rewrites the English PR description to final measured counts before RESULT."}
    67	  - {control: "5.14 item 0", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 0 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    68	  - {control: "5.14 item 1", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 1 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    69	  - {control: "5.14 item 2", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 2 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    70	  - {control: "5.14 item 3", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 3 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    71	  - {control: "5.14 item 4", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 4 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    72	  - {control: "5.14 item 5", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 5 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    73	  - {control: "5.14 item 6", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 6 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    74	  - {control: "5.14 item 7", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 7 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    75	  - {control: "5.14 item 8", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
    76	  - {control: "5.14 item 9", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 9 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    77	  - {control: "5.14 item 10", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 10 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    78	premises: []
    79	---
    80	
    81	# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a07-checker
    82	
    83	🤖 I read the AGENTS.md for mryfmo/dotfiles.
    84	
    85	## Goal and scope
    86	
    87	[memory:decision] D-024-57 and D-024-58 reset a06 after its second and final mechanism round; a07 is a fix set on the a06 design, preserving its pipeline, C1-C16 and fixtures. No third a06 round is authorized.
    88	Continue PR #440 on `tools/task-generator-plan-check-a05-checker` from `c439b63c65285ec8180dc3e21394c87ef21115b4`; its PR patch is unchanged since `2cb58482`. The orchestrator names a Codex standard-profile seat other than a012 in the TASK line; max_turns=12.
    89	Read the a06 dispatched task and evidence at the continuation head, its acceptance record, and `.orchestration/validation/` audit/local reviews of c439b63c, local review of 21f52c7 and security review of 2cb5848 whole; retain all finding IDs and a04/a05 history.
    90	[memory:failure] The a06 R1 unset-cache fallback was the orchestrator's error, not a design exception; restore item 9. Preserve withdrawn PR #417 lineage and every inventoried predecessor directory unchanged from the continuation head.
    91	Design 5.14 items 0-10 in `.orchestration/plans/024-design-quality.md` apply by reference under D-024-29/30. Retain a06 checker behavior, pipeline, grammar, fixtures and mutation requirements except Items 1-8; this text supersedes its scope, lineage, assignment, dispatch, measurement and completion clauses.
    92	Only the allowed checker, two test files and own evidence may change. Generator, plan checker, templates, workflows, dispatch/resolver implementation, deployment and canonical orchestration records remain outside scope; do not revive the withdrawn three-script implementation.
    93	
    94	## Items
    95	
    96	Each numbered Item has one new fixture in `TaskConsistencyC11C15Test`; selectors are the full closed-row selectors above. Write fixtures before fixes; assert the intended verdict and finding/refusal label, with valid controls.
    97	1. `test_c15_rejects_invariants_without_design`: at :496, refuse supplied invariants without `design_review.design` with fixed label `C15 invariants require design_review.design`; retain canonical assignment-set and byte-equality validation when design is present (audit:c439b63:1, P1).
    98	2. `test_c14_grep_count_no_match_fails`: at :312, preserve grep's status; unmatched `grep -c` returns stdout `0` and status 1, so authorized C14 fails despite matching expected output; matched controls pass (audit:c439b63:2, local:c439b63:2).
    99	3. `test_c4_requires_separate_directory_scope_rows`: at :348, require separate rows for `scripts/` and `scripts/orchestrator/`; one child-directory row cannot cover both; two distinct rows pass (audit:c439b63:3, local:21f52c7:3).
   100	4. `test_c12_requires_concrete_claude_rows`: at :476, classify `CLAUDE.md` and every `CLAUDE*` match as applied instructions; wildcard matches require concrete rows; named controls pass (audit:c439b63:4, local:21f52c7:2).
   101	5. `test_c8_handles_binary_canonical_blobs`: at :225, use a fixed decoding fallback or skip undecodable canonical blobs; C8 traversal reaching `home/.key.txt.age` returns its proper finding or valid verdict, never UnicodeDecodeError (local:c439b63:1).
   102	6. `test_c12_classifies_links_and_checks_missing_alias_prefixes`: at :476/:251, two independently red subcases require a concrete row for an unnamed applied symlink by its own path/name even when its target is non-applied, and reject a missing literal beneath an internal directory alias before returning early; preserve target-based applicability, confinement and valid controls (security:2cb5848:1-2).
   103	7. `test_refuses_missing_uv_cache_dir`: at :138, restore design 5.14 item 9 by removing the unset-cache fallback and refusing absent UV_CACHE_DIR with fixed label `refused: UV_CACHE_DIR absent`; preserve absolute-cache checks and the valid supplied-cache control (audit:c439b63:8).
   104	8. `test_path_entry_relativises_case_alias_by_identity`: at :83, relativise case-aliased symlink targets by filesystem identity rather than case-sensitive `relative_to`; an in-repository alias yields a checker verdict without ValueError; escaping targets still fail (local:c439b63:3).
   105	
   106	## Check
   107	
   108	Run every new fixture against checker revision `c439b63c65285ec8180dc3e21394c87ef21115b4` for its behavioral red and against its fix commit for green; record eight red/green full-SHA pairs, with both Item 6 subcases independently red. Missing dependencies, import errors, zero tests and unrelated refusals are not reds.
   109	Preserve all a06 tests, historical red provenance, negative controls and mutation requirements; rerun both complete checker modules on Python 3.12.15 and 3.15.0. Keep the isolated selector bootstrap, deterministic Unicode/case models, observed native-filesystem limitations and one-file collision control from a06.
   110	Host facts measured before authoring: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`. Run that resolve command and paste its actual output; never guess a binding.
   111	Use a06 Commands with design 5.14 items 2, 3, 4, 7, 9 and 10 by reference, including validation of its provisioned 3.12.15 binding; record actual tool paths, hashes, versions and expanded commands. Each evidence item names its producer: `worker (Codex seat)` or `orchestrator (Claude seat, sandboxed Bash)`.
   112	For each runtime run `<uv_abs> run --no-config --no-project --offline --python <python_abs> --with pyyaml python -I -m unittest discover -s tests/unit -p 'test_task_consistency_c11_c15.py' -v`.
   113	Also run `<uv_abs> run --no-config --no-project --offline --python <python_abs> --with pyyaml python -I -m unittest discover -s tests/unit -p 'test_task_checkers.py' -v`; expand bindings from measured resolution, not guessed paths.
   114	Run `make unit-test` on the RESULT-time merge-base and candidate in the same environment, with the a06 full-suite base-versus-candidate comparison and exact inherited failure multiplicities; all existing a06 tests stay green and no new suite failures are permitted. Never run Bats locally.
   115	Run `ruff check scripts/orchestrator/task-consistency-check.py tests/unit/test_task_consistency_c11_c15.py tests/unit/test_task_checkers.py` and `ruff format --check scripts/orchestrator/task-consistency-check.py tests/unit/test_task_consistency_c11_c15.py tests/unit/test_task_checkers.py`; retain R4 lint and applicable a06 validators.
   116	The complete final diff has at most 550 changed lines outside `tests/` and `.orchestration/`, and at most 1050 under `tests/`.
   117	Measure additions plus deletions using `git diff --numstat <merge-base40> <head40>`.
   118	Compute `<merge-base40>` with `git merge-base origin/main <head40>` at RESULT time (C-123), never the a06 fixed base; today's base is e00de4e0 and inherited counts are 446 source / 709 tests. Caps allow 104 source / 341 test lines of headroom for these fixes and fixtures; recount after update-branch, attribute inherited versus a07 changes, and drop no controls to fit.
   119	Put complete name-only and numstat output, per-file arithmetic and both totals in measure.md and RESULT; the orchestrator rewrites PR #440's English description to those final counts before RESULT. Do not hide runtime code in evidence or change lint baselines.
   120	Retain a06 canonical prerequisite API verification bound to `repos/mryfmo/dotfiles` and `github.com`; before the anchor review the orchestrator fills Checks with PR #435's merged-state observation from the fixed repository/host API, validated pinned main SHA, decoded design SHA-256, exact commands/output and every stage exit. `after: []` does not waive this prerequisite.
   121	C-80 applies: the orchestrator obtains the security-profile text/threat-table review and dispositions its findings before dispatch. Anchor only the completely populated text; dispatch those exact reviewed bytes with no later paste. Record review evidence and task SHA outside the text; previous_sha256 in Checks binds the a06 dispatched bytes, not branch bytes.
   122	
   123	## Completion and evidence
   124	
   125	Worker Playbook step 4 applies: every command stays sandboxed. Push by HTTPS with `git push https://github.com/mryfmo/dotfiles.git HEAD:refs/heads/tools/task-generator-plan-check-a05-checker` without `-u`; on any denial send `AGMSG-PONG v1 status=blocked` with exact command, exit, output and boundary, then wait for re-tasking; no alternative-tool retry or escape.
   126	Do not probe the herdr socket from a Codex sandbox (measured PermissionDenied); retain D-024-36 network limitations as observations, never assume connectivity or treat unavailable live API checks as passing.
   127	Commit task.md (byte-identical dispatched bytes), report.md, validation.md, sandbox.md, learning.md, autoskill.md (status or not-used), measure.md and worker review evidence under this task's allowed directory; verify every required file with `git ls-files`. Keep plan/todo/learn worklogs current and uncommitted; scope C2/C3 must accept retained lineage and reject hidden predecessor edits.
   128	validation.md includes verbatim stdout/stderr/exits for all checks, checker and regression-source hashes, actual runtimes, eight red/green SHA pairs, mutation outcomes and limits; report.md binds finding IDs to selectors and separates inherited evidence from new observations.
   129	Use agent-side Crit data (`crit status --json`, `crit comments --all --json <review.json>`) or the documented independent-review JSON fallback, with resolved records and `-worker-` evidence names. The receipt contains `review_surface: crit-data`, `reviewer: codex`, `review_source: <repo-local JSON>` and `review_outcome: approved` or `addressed`; run `make require-crit-review` and its evidence-bound invocation; no browser, publication or human review request.
   130	The orchestrator records INV-6/S1 counters before revises; repeated finding classes require a recorded re-plan. At most one worker Bot fix-round under Worker Playbook step 15; a surviving P0/P1 stops for the operator, never a private extra round.
   131	Send `AGMSG-RESULT v1 status=ready_for_review` only after required checks and final-head CI/Bot observations; include PR #440, branch, full head, RESULT merge-base, caps 550/1050, changed_non_tests, changed_tests, inherited attribution, eight red/green SHA pairs, task_copy SHA-256, changed-file inventory, all retained directories, selectors, artifacts, proposed feedback dispositions and `cost:` observed or n/a. After the final head is known, write the RESULT key/value record to this task's result.txt before sending.
   132	Fresh applicable CI follows every push, including evidence-only pushes. The worker never merges; after final-head CI/security review the orchestrator follows Playbook step 10 in order: feedback sweep/dispositions, task audit, acceptance, then gate with PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE and ACCEPTANCE_EVIDENCE. Earlier approvals do not authorize this head.
   133	
   134	## Checks
   135	

**Ensuring manageable output size**
exec
/bin/zsh -lc "sed -n '/## Codex seat worklogs/,/"'^## /p'"' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md | head -80; cat .ua/meta.json' in ~/Workspace/dotfiles
 succeeded in 79ms:
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

 succeeded in 109ms:
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

 succeeded in 172ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a08.md
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
 M .orchestration/acceptance/dotfiles-T133-result-precheck-a03.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md
 M .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-pins-a01.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07-design-reset.md
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a02-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a03.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/
?? .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01/
?? .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02/
?? .orchestration/learning/mistakes/M-20261021-05-codex-run-inside-the-sandbox-after-compaction.md
?? .orchestration/learning/mistakes/M-20261021-06-dispatch-against-the-texts-own-precondition.md
?? .orchestration/learning/mistakes/M-20261021-07-wrong-owner-id-in-the-chain-line.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T128-task-checkers-followup-a02.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a03-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a03.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-1d72f16.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-audit-08b8add.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-chain-08b8add.log
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-08b8add.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-audit-c439b63.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-audit-c439b63.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-c439b63.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-c439b63.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-chain-28dde0f.log
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-local-review-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-1f17d05.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-text-security-0908b8f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-text-security-0908b8f.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-text-security-70feed4.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-text-security-70feed4.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-audit-f66b27f.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-audit-f66b27f.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-chain-f66b27f.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-local-review-f66b27f.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-audit-c8c712f.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-audit-c8c712f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-chain-2d1d095.log
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-chain-c8c712f.log
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-crit.json
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-local-review-2d1d095.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-local-review-c8c712f.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-security-2d1d095.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-security-2d1d095.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-security-c8c712f.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-security-c8c712f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0b96f40.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0b96f40.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0e9bf3f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0e9bf3f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0f87501.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0f87501.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-3844d93.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-3844d93.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-task-generator-plan-check-a07-checker
     4	kind: code
     5	security: true
     6	design: 5.14 items 0-10
     7	design_review:
     8	  design: .orchestration/plans/024-design-quality.md
     9	allowed_files:
    10	  - scripts/orchestrator/task-consistency-check.py
    11	  - tests/unit/test_task_consistency_c11_c15.py
    12	  - tests/unit/test_task_checkers.py
    13	  - .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/**
    14	after: []
    15	reset_of: [dotfiles-T133-task-generator-plan-check-a06-checker]
    16	retained_predecessor_directories:
    17	  - .orchestration/dotfiles-T133-task-generator-plan-check-a04/
    18	  - .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/
    19	  - .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/
    20	expected_result_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/report.md
    21	expected_validation_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/validation.md
    22	expected_sandbox_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/sandbox.md
    23	expected_learning_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/learning.md
    24	expected_autoskill_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/autoskill.md
    25	expected_measure_file: .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/measure.md
    26	threat_table:
    27	  - {control: "scripts/orchestrator/task-consistency-check.py", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retained defenses and final-head fixtures mitigate checker faults; pre-start and same-UID interference remain."}
    28	  - {control: "tests/unit/test_task_consistency_c11_c15.py", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; real-checker fixtures and deterministic models mitigate regressions; native-platform and live-API coverage remain limited."}
    29	  - {control: "tests/unit/test_task_checkers.py", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; preserve historical expectations and compare the full suite against the merge-base in the same environment."}
    30	  - {control: ".orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/**", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; commit .orchestration/dotfiles-T133-task-generator-plan-check-a07-checker/task.md byte-identical to dispatch and all evidence; no credentials or runtime helpers."}
    31	  - {control: "predecessor copy .orchestration/dotfiles-T133-task-generator-plan-check-a04/task.md", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain the entire inventoried directory unchanged from c439b63c; historical evidence grants no approval."}
    32	  - {control: "predecessor copy .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task.md", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain the entire inventoried directory unchanged from c439b63c; historical evidence grants no approval."}
    33	  - {control: "predecessor copy .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain the entire inventoried directory unchanged from c439b63c; historical evidence grants no approval."}
    34	  - {control: "checker-side interpreter selection after startup", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_interpreter_resolution_order"}
    35	  - {control: "gh child environment", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_gh_child_preserves_parent_tokens"}
    36	  - {control: "canonical-main design read", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_uses_canonical_main_only"}
    37	  - {control: "C6 canonical receipt binding and design hash", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
    38	  - {control: "fixture and evidence symlink exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_symlink_to_applied_file_is_finding"}
    39	  - {control: "fixture and evidence case-alias exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_case_alias_to_applied_file_is_finding"}
    40	  - {control: "original Unicode path confinement", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_resolves_original_unicode_path"}
    41	  - {control: "internal directory aliases", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_rejects_internal_directory_alias"}
    42	  - {control: "directory pruning name comparison", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_prunes_with_normalised_directory_names"}
    43	  - {control: "path_entry pipeline identity", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_canonical_path_pipeline_rejects_normalised_collisions"}
    44	  - {control: "path grammar and filesystem identity", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; preserve all grammar, confinement and identity fixtures; filesystem models do not establish native coverage."}
    45	  - {control: "C16 reference and item coverage", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c16_requires_reference_and_all_item_rows"}
    46	  - {control: "C16 item occurrence counting", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_rejects_multi_item_rows"}
    47	  - {control: "C16 resolved-target applicability", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_uses_resolved_literal_alias"}
    48	  - {control: "C15 invariants validation", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_rejects_invariants_without_design"}
    49	  - {control: "C14 probe status", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c14_grep_count_no_match_fails"}
    50	  - {control: "C4 directory scope coverage", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c4_requires_separate_directory_scope_rows"}
    51	  - {control: "C12 CLAUDE instruction coverage", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_requires_concrete_claude_rows"}
    52	  - {control: "C8 canonical binary decoding", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c8_handles_binary_canonical_blobs"}
    53	  - {control: "C12 symlink classification", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_classifies_links_and_checks_missing_alias_prefixes"}
    54	  - {control: "missing-literal directory-symlink prefix validation", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_classifies_links_and_checks_missing_alias_prefixes"}
    55	  - {control: "UV_CACHE_DIR refusal", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_refuses_missing_uv_cache_dir"}
    56	  - {control: "case-aliased symlink target relativisation", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_entry_relativises_case_alias_by_identity"}
    57	  - {control: "task metadata", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; orchestrator verifies reset lineage, scope, caps, prerequisites and dispatched-copy identity before acceptance."}
    58	  - {control: "metadata separators", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; the dispatched digest covers the entire file including separators and populated Checks; quoted evidence stays data."}
    59	  - {control: "in-process effects", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain C14 authorization, fixed vocabulary and non-execution controls; existing negative tests limit probe execution."}
    60	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; design 5.14 items 2, 3, 4 and 9 apply by reference; no workflow or caller changes are authorized."}
    61	  - {control: "new or renamed scripts", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; only the existing production checker changes; no resolver, wrapper, dependency or artifact runtime code."}
    62	  - {control: "orchestrator effect dispatch.sh keeps calling the checker unchanged", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; retain the unchanged-invocation compatibility fixture; design 5.14 items 2, 4 and 9 apply by reference."}
    63	  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; worker never merges; orchestrator applies Playbook step 10 to the final audited head."}
    64	  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; recompute the merge-base and refresh CI, feedback and audit after every head change."}
    65	  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; none assigned; preserve worker state, PR #440 and withdrawn lineage evidence."}
    66	  - {control: "orchestrator effect PR metadata", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; orchestrator rewrites the English PR description to final measured counts before RESULT."}
    67	  - {control: "5.14 item 0", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 0 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    68	  - {control: "5.14 item 1", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 1 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    69	  - {control: "5.14 item 2", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 2 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    70	  - {control: "5.14 item 3", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 3 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    71	  - {control: "5.14 item 4", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 4 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    72	  - {control: "5.14 item 5", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 5 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    73	  - {control: "5.14 item 6", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 6 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    74	  - {control: "5.14 item 7", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 7 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    75	  - {control: "5.14 item 8", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
    76	  - {control: "5.14 item 9", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 9 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    77	  - {control: "5.14 item 10", disposition: "residual: dotfiles-T133-task-generator-plan-check-followup-a01; item 10 applies by reference; retained scoped fixtures and final-head audit mitigate regression risk without closing the referenced boundary."}
    78	premises: []
    79	---
    80	
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

**Checking read-only task setup**
exec
/bin/zsh -lc "rg --files .orchestration/validation | rg 'task-generator.*(c439b63|21f52c7|2cb5848)'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '"'^### 5.14|''^### 5.15|''^## Commands|''^## |item 8|trusted|GIT_'"' .orchestration/plans/024-design-quality.md .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md; cat .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md; cat .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "jq -r '.nodes[] | select((.filePath // \"\") | test(\"task-consistency|dispatch|024-design\")) | [.filePath,.summary] | @tsv' .ua/knowledge-graph.json; git rev-parse HEAD; git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD | head -25" in ~/Workspace/dotfiles
 succeeded in 161ms:
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:49:  - {control: "orchestrator effect dispatch.sh keeps calling the checker unchanged", disposition: "residual: The dispatch fixture proves checker compatibility only; dotfiles-T133-loop-limits-a01 owns dispatch.sh and dotfiles-T133-trusted-entrypoint-binding-a01 owns executable binding before checker startup."}
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:55:  - {control: "5.14 item 2: 無害化した環境を最初に", disposition: "residual: Item 2 applies by reference; PATH-selected mise/uv execute first. dotfiles-T133-loop-limits-a01 owns dispatch.sh, dotfiles-T133-trusted-entrypoint-binding-a01 owns executable binding, and dotfiles-T133-ci-efficiency-followup-a04 owns the resolver and private UV_CACHE_DIR."}
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:61:  - {control: "5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:62:  - {control: "5.14 item 9: 私設キャッシュ", disposition: "residual: Item 9 applies by reference; unchanged dispatch selects shared $HOME/.cache/uv, allowing pre-checker poisoning. dotfiles-T133-ci-efficiency-followup-a04 owns the resolver/private cache; dotfiles-T133-loop-limits-a01 and dotfiles-T133-trusted-entrypoint-binding-a01 own parent execution and binding."}
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:81:## Goal and lineage
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:101:## Dispatch prerequisite and design
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:113:## Implementation contract
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:115:1. Retain interpreter selection: landed `scripts/orchestrator/trusted-interpreter.sh` first, supplied `TRUSTED_PYTHON` second, real `sys.executable` with an explicit stderr fallback warning last. Validate the selected interpreter; resolver failure or invalid supplied input refuses rather than falling through. Add no interpreter PATH discovery.
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:119:   Parent PATH-selected mise/uv and shared-cache execution happen before these defenses. Parent hardening belongs to dotfiles-T133-loop-limits-a01, executable binding to dotfiles-T133-trusted-entrypoint-binding-a01, resolver/private UV_CACHE_DIR to dotfiles-T133-ci-efficiency-followup-a04; this slice closes none of those boundaries.
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:147:Retain all other C1–C15 behavior, C11 class selectors, confinement, non-execution and trusted-execution negative controls. Port no dependency on the two deferred scripts.
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:149:## Required regression fixtures
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:190:## Commands
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:203:## Check
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:220:Run the checker on dispatched bytes and record C14's warning without `--premises-sha`; authorized fixtures use their supplied trusted digest. Never invent dispatch authority from branch bytes or add shell support for authoring probes.
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:222:## Completion and evidence
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:241:## Checks (pasted by the orchestrator before each send)
.orchestration/plans/024-design-quality.md:95:### 5.14 残余（凍結後の計測事実、D-024-29）
.orchestration/plans/024-design-quality.md:103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
.orchestration/plans/024-design-quality.md:107:1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19). The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).
.orchestration/plans/024-design-quality.md:108:2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
.orchestration/plans/024-design-quality.md:115:9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
.orchestration/plans/024-design-quality.md:117:7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a06-checker round=1 reset_of=dotfiles-T133-task-generator-plan-check-a05-checker repo=~/Workspace/dotfiles/.claude/worktrees/worker-g task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md task_sha256=90ca0ae9563df4b352dfb26c6b6aa60132386e15ce9ff50bcf998a43097a12e6 deadline=none done_signal=AGMSG-RESULT note=a012:reset-a06(D-024-39:measured-cap-440/700-for-the-canonical-path-pipeline-re-plan;your-uncommitted-draft-is-this-round's-content,plus-amendment-1's-identity-aware-matching-and-path-collision-refusal-with-the-two-file-regression;C-80-73ac933-correct;PR-440-continues-from-06ffefbc;add-the-a06-task-copy-and-records,keep-the-a05-copy;commit-locally-and-PONG-the-head-for-transport;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)"
  ],
  "format": 1,
  "head": "c439b63c65285ec8180dc3e21394c87ef21115b4",
  "ledger": [
    {
      "class": "excluded-command-trusts-sandbox-context",
      "id": "audit:1368f71:401"
    },
    {
      "class": "excluded-command-trusts-sandbox-context",
      "id": "audit:1368f71:402"
    },
    {
      "class": "sources",
      "id": "audit:1368f71:403"
    },
    {
      "class": "hash-binding",
      "id": "audit:1368f71:404"
    },
    {
      "class": "glob-matches-its-negation",
      "id": "audit:1368f71:405"
    },
    {
      "class": "glob-filter",
      "id": "audit:d0ad49f:201"
    },
    {
      "class": "unmasked-evidence",
      "id": "audit:24d7f55:201"
    },
    {
      "class": "evidence-integrity",
      "id": "audit:9da0ed3:1"
    },
    {
      "class": "threat-row-stale",
      "id": "audit:9da0ed3:2"
    },
    {
      "class": "replan-not-patch",
      "id": "audit:9da0ed3:3"
    },
    {
      "class": "dispatch-wiring",
      "id": "audit:9da0ed3:4"
    },
    {
      "class": "spec-gap",
      "id": "audit:9da0ed3:5"
    },
    {
      "class": "glob-classification",
      "id": "audit:9da0ed3:6"
    },
    {
      "class": "glob-intersection",
      "id": "audit:9da0ed3:7"
    },
    {
      "class": "substring-selection",
      "id": "audit:9da0ed3:8"
    },
    {
      "class": "glob-filter",
      "id": "audit:9da0ed3:9"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:10"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:11"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:12"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:13"
    },
    {
      "class": "regex-gap",
      "id": "audit:9da0ed3:14"
    },
    {
      "class": "records-form",
      "id": "audit:9da0ed3:15"
    },
    {
      "class": "spec-gap",
      "id": "audit:8a09b93:1"
    },
    {
      "class": "glob-classification",
      "id": "audit:8a09b93:2"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:3"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:4"
    },
    {
      "class": "glob-classification",
      "id": "audit:8a09b93:5"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:6"
    },
    {
      "class": "parser-gap",
      "id": "audit:8a09b93:7"
    },
    {
      "class": "parser-gap",
      "id": "audit:8a09b93:8"
    },
    {
      "class": "test-coverage",
      "id": "audit:8a09b93:9"
    },
    {
      "class": "selector-grammar",
      "id": "audit:8a09b93:10"
    },
    {
      "class": "evidence-integrity",
      "id": "audit:8a09b93:11"
    },
    {
      "class": "records-form",
      "id": "audit:8a09b93:12"
    },
    {
      "class": "uv-caller-state-interpreter",
      "id": "audit:7a201ea:1"
    },
    {
      "class": "unlanded-mechanism-stated-as-present",
      "id": "audit:7a201ea:2"
    },
    {
      "class": "checker-exit-unchecked",
      "id": "audit:7a201ea:3"
    },
    {
      "class": "tool-environment",
      "id": "audit:7a201ea:4"
    },
    {
      "class": "happy-path-closing-test",
      "id": "audit:7a201ea:5"
    },
    {
      "class": "glob-classification",
      "id": "audit:7a201ea:6"
    },
    {
      "class": "glob-filter",
      "id": "audit:7a201ea:7"
    },
    {
      "class": "spec-without-input-grammar",
      "id": "audit:7a201ea:8"
    },
    {
      "class": "glob-filter",
      "id": "audit:7a201ea:9"
    },
    {
      "class": "input-validation",
      "id": "audit:7a201ea:10"
    },
    {
      "class": "input-validation",
      "id": "audit:7a201ea:11"
    },
    {
      "class": "happy-path-closing-test",
      "id": "audit:7a201ea:12"
    },
    {
      "class": "acceptance-dispositions",
      "id": "audit:7a201ea:13"
    },
    {
      "class": "replan-skipped",
      "id": "audit:7a201ea:14"
    },
    {
      "class": "evidence-dropped",
      "id": "audit:7a201ea:15"
    },
    {
      "class": "input-validation",
      "id": "audit:cedc7f5:301"
    },
    {
      "class": "input-validation",
      "id": "audit:cedc7f5:302"
    },
    {
      "class": "count-grammar",
      "id": "audit:cedc7f5:303"
    },
    {
      "class": "input-validation",
      "id": "audit:06ffefb:301"
    },
    {
      "class": "input-validation",
      "id": "audit:06ffefb:302"
    },
    {
      "class": "cap-without-room",
      "id": "audit:06ffefb:201"
    },
    {
      "class": "environment-contract",
      "id": "audit:b8bf806:101"
    },
    {
      "class": "platform-dependent-detection",
      "id": "audit:b8bf806:102"
    },
    {
      "class": "evidence-integrity",
      "id": "audit:b8bf806:201"
    },
    {
      "class": "approval-binding",
      "id": "audit:b8bf806:301"
    },
    {
      "class": "input-validation",
      "id": "audit:4a49ed9:401"
    },
    {
      "class": "input-validation",
      "id": "audit:5c09a95:201"
    },
    {
      "class": "input-validation",
      "id": "audit:5c09a95:202"
    },
    {
      "class": "cap-without-room",
      "id": "audit:5c09a95:203"
    },
    {
      "class": "input-validation",
      "id": "audit:1779440:201"
    },
    {
      "class": "caller-dependency",
      "id": "audit:21f52c7:501"
    }
  ],
  "pr": 440,
  "replans": {
    "evidence-integrity": {
      "design": "the worker's validation.md carries a `Base:`/`Candidate:` line pair and a named extra set, and the orchestrator runs `result-evidence-check.sh <task> <head40> <pr>` on every RESULT before reading its report (C-113)",
      "implementation": "`.agents/worklog/orchestrator-glue/result-evidence-check.sh` (written 09:56Z; promotion into scripts/orchestrator/ as a task after the pre-send-check pattern)",
      "specification": "a RESULT's claims are checked mechanically before the orchestrator judges them: the validation's full-suite comparison names every candidate-minus-base failure, and the head's CI has concluded green as read by the orchestrator",
      "verification": "the glue refuses b8bf8066 (`extra=6`, `0 test names`) and accepts the round-2 head only when its extra set is empty or named and its CI runs are all green."
    },
    "glob-classification": {
      "design": "classification is a pure function of the key and the declared rows, so a glob, its negation and a directory scope resolve through the same key table",
      "implementation": "the a06 round on PR #440 (task-consistency-check.py +443 lines at b8bf8066, round 2 pending)",
      "specification": "every path the checker classifies (an `allowed_files` entry, a threat-table control, an applied directory, a walked file) goes through one canonical pipeline, `normalise_name` then `path_entry`, and is classified by its one NFC-folded key, never by a substring or by the glob library's own semantics (a06 text item 1, D-024 reset of a05)",
      "verification": "`tests/unit/test_task_consistency_c11_c15.py` holds one red-then-green test per carried row class, read on the Linux CI jobs by the orchestrator, not on the worker's macOS alone."
    },
    "glob-filter": {
      "design": "one path normaliser shared by every check, tested on the grammar's cases",
      "implementation": "the a05-checker slice",
      "specification": "the checker's path semantics (git pathspec vs glob, root files, directory + child, `./` spellings, escaping scopes) are stated as one grammar in the text",
      "verification": "one fixture per grammar case, red at 7a201eab, plus the audit of the slice's head."
    },
    "input-validation": {
      "design": "a single function returns (enumerated, resolved, normalised-for-matching) for every file and directory, and C12, C16, the fixture exemption and the symlink rules consume that triple instead of normalising or resolving in place",
      "implementation": "worker fix round 2 on PR #440 (a012), source cap 400 unchanged",
      "specification": "every path the checker judges goes through one pipeline: the enumerated path is kept for reporting, its real target is resolved for confinement and applicability, and Unicode normalisation applies only to the comparison of names, never to the path that is confined or resolved",
      "verification": "one red-then-green test per finding plus one invariant test, the security-profile review of the new head, the task-level audit."
    },
    "parser-gap": {
      "design": "a parser refuses what it cannot parse (exit 1 with the line) instead of skipping it, so a gap surfaces as a finding, never as a silent pass",
      "implementation": "the a06 round on PR #440 (the same checker change)",
      "specification": "the front matter, the Check sentence's caps (backticked paths, the numstat command in its own sentence, C-107) and the metadata grammar are parsed by one parser each, with the grammar written once in the checker and quoted in the task text",
      "verification": "one fixture per former gap in `tests/unit/test_task_consistency_c11_c15.py`, red before the pipeline and green after, plus the regime-ci fixture grammar of #441 on main."
    },
    "text-defect": {
      "design": "the task template states the cap that way and the checker (this slice, C16 sibling) counts lines up to the Checks heading",
      "implementation": "this slice adds the rule to task-consistency-check.py (one more check, within the caps) or records it as the a06 owner row if the caps do not allow",
      "specification": "a text's line cap is the authored text, and the orchestrator's pasted Checks section is outside it",
      "verification": "a fixture with a long Checks section passes."
    }
  },
  "searches": [
    {
      "class": "evidence-integrity",
      "records": [
        "M-20261020-04-result-claims-against-own-counts.md"
      ]
    },
    {
      "class": "glob-classification",
      "records": []
    },
    {
      "class": "glob-filter",
      "records": []
    },
    {
      "class": "input-validation",
      "records": [
        "M-20261012-32.md"
      ]
    },
    {
      "class": "parser-gap",
      "records": [
        "M-20261019-04-parser-gap.md"
      ]
    }
  ],
  "task": "dotfiles-T133-task-generator-plan-check-a06-checker"
}
---

# Acceptance record: dotfiles-T133-task-generator-plan-check-a06-checker

- 2026-10-20T07:55Z: reset of dotfiles-T133-task-generator-plan-check-a05-checker (D-024-39: the canonical path pipeline re-plan needs a measured cap of 440 source lines; the a05 text's amendments and worker rounds are spent), text written whole by the review profile (`a06-checker-prompt.md`), 237 lines (self cap 260), Checks normalised; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 4a49ed9263e025e84f3ec5a51df553cfc83ab71192a4de016770e42a1f80491b before the Checks paste. C-80 round 1 running. Continues PR #440 from 06ffefbc with a012's uncommitted pipeline draft as the round's content. The a05 findings history is in the a05 record; its rows and re-plan lines are carried below (M-20261019-06).

## Lineage rows carried from dotfiles-T133-task-generator-plan-check-a05-checker

text-security:1368f71:1	excluded-command-trusts-sandbox-context
text-security:1368f71:2	excluded-command-trusts-sandbox-context
text-security:1368f71:3	sources
text-security:1368f71:4	hash-binding
text-security:1368f71:5	glob-matches-its-negation
text-security:cd37b74:0	correct
worker:d0ad49f:1	glob-filter
worker:24d7f55:1	unmasked-evidence
audit:9da0ed3:1	evidence-integrity
audit:9da0ed3:2	threat-row-stale
audit:9da0ed3:3	replan-not-patch
audit:9da0ed3:4	dispatch-wiring
audit:9da0ed3:5	spec-gap
audit:9da0ed3:6	glob-classification
audit:9da0ed3:7	glob-intersection
audit:9da0ed3:8	substring-selection
audit:9da0ed3:9	glob-filter
audit:9da0ed3:10	parser-gap
audit:9da0ed3:11	parser-gap
audit:9da0ed3:12	parser-gap
audit:9da0ed3:13	parser-gap
audit:9da0ed3:14	regex-gap
audit:9da0ed3:15	records-form
audit:8a09b93:1	spec-gap
audit:8a09b93:2	glob-classification
audit:8a09b93:3	glob-filter
audit:8a09b93:4	glob-filter
audit:8a09b93:5	glob-classification
audit:8a09b93:6	glob-filter
audit:8a09b93:7	parser-gap
audit:8a09b93:8	parser-gap
audit:8a09b93:9	test-coverage
audit:8a09b93:10	selector-grammar
audit:8a09b93:11	evidence-integrity
audit:8a09b93:12	records-form
audit:7a201ea:1	uv-caller-state-interpreter
audit:7a201ea:2	unlanded-mechanism-stated-as-present
audit:7a201ea:3	checker-exit-unchecked
audit:7a201ea:4	tool-environment
audit:7a201ea:5	happy-path-closing-test
audit:7a201ea:6	glob-classification
audit:7a201ea:7	glob-filter
audit:7a201ea:8	spec-without-input-grammar
audit:7a201ea:9	glob-filter
audit:7a201ea:10	input-validation
audit:7a201ea:11	input-validation
audit:7a201ea:12	happy-path-closing-test
audit:7a201ea:13	acceptance-dispositions
audit:7a201ea:14	replan-skipped
audit:7a201ea:15	evidence-dropped
security:cedc7f5:1	input-validation
security:cedc7f5:2	input-validation
security:cedc7f5:3	count-grammar
security:06ffefb:1	input-validation
security:06ffefb:2	input-validation
worker:06ffefb:1	cap-without-room
re-plan: text-defect (amendments 1 and 2 of this text; the python-pin text had the same cap collision) — specification: a text's line cap is the authored text, and the orchestrator's pasted Checks section is outside it; design: the task template states the cap that way and the checker (this slice, C16 sibling) counts lines up to the Checks heading; implementation: this slice adds the rule to task-consistency-check.py (one more check, within the caps) or records it as the a06 owner row if the caps do not allow; verification: a fixture with a long Checks section passes.
re-plan: glob-filter (rows audit:9da0ed3:9, audit:8a09b93:3-4, audit:8a09b93:6, audit:7a201ea:7, audit:7a201ea:9 of the a04 lineage; worker:d0ad49f:1) — specification: an allowed_files pathspec is validated for magic (`:(…)`, leading `:`, escapes) after normalisation, never before, and a path whose directory prefix is a symlink outside the worktree is refused before the full-match filter; symlinked directories are never followed; design: validation order fixed as normalise -> magic check -> symlink-prefix confinement -> full-match filter (a012's proposal, no scope or cap change); implementation: a012's repair in the a05 draft with one regression fixture per defect (magic after normalisation; escaping symlink prefix); verification: a012's independent review, the task-level audit of the final head and the security review (security: true).
re-plan: glob-filter (rows across audit:fa71134, audit:7a201ea; classes glob-classification x3, glob-filter x4, parser-gap x6 in this lineage) — specification: the checker's path semantics (git pathspec vs glob, root files, directory + child, `./` spellings, escaping scopes) are stated as one grammar in the text; design: one path normaliser shared by every check, tested on the grammar's cases; implementation: the a05-checker slice; verification: one fixture per grammar case, red at 7a201eab, plus the audit of the slice's head.
re-plan: input-validation (rows security:cedc7f5:1-2, security:06ffefb:1-2) — specification: every path the checker judges goes through one pipeline: the enumerated path is kept for reporting, its real target is resolved for confinement and applicability, and Unicode normalisation applies only to the comparison of names, never to the path that is confined or resolved; design: a single function returns (enumerated, resolved, normalised-for-matching) for every file and directory, and C12, C16, the fixture exemption and the symlink rules consume that triple instead of normalising or resolving in place; implementation: worker fix round 2 on PR #440 (a012), source cap 400 unchanged; verification: one red-then-green test per finding plus one invariant test, the security-profile review of the new head, the task-level audit.
re-plan: glob-classification (rows audit:9da0ed3:6, audit:8a09b93 and audit:7a201ea of the a04/a05 lineage, carried; four rows) — specification: every path the checker classifies (an `allowed_files` entry, a threat-table control, an applied directory, a walked file) goes through one canonical pipeline, `normalise_name` then `path_entry`, and is classified by its one NFC-folded key, never by a substring or by the glob library's own semantics (a06 text item 1, D-024 reset of a05); design: classification is a pure function of the key and the declared rows, so a glob, its negation and a directory scope resolve through the same key table; implementation: the a06 round on PR #440 (task-consistency-check.py +443 lines at b8bf8066, round 2 pending); verification: `tests/unit/test_task_consistency_c11_c15.py` holds one red-then-green test per carried row class, read on the Linux CI jobs by the orchestrator, not on the worker's macOS alone.
re-plan: parser-gap (rows audit:9da0ed3:10-13 and the a05 carried rows; six rows) — specification: the front matter, the Check sentence's caps (backticked paths, the numstat command in its own sentence, C-107) and the metadata grammar are parsed by one parser each, with the grammar written once in the checker and quoted in the task text; design: a parser refuses what it cannot parse (exit 1 with the line) instead of skipping it, so a gap surfaces as a finding, never as a silent pass; implementation: the a06 round on PR #440 (the same checker change); verification: one fixture per former gap in `tests/unit/test_task_consistency_c11_c15.py`, red before the pipeline and green after, plus the regime-ci fixture grammar of #441 on main.
re-plan: evidence-integrity (rows audit:9da0ed3:1, audit:7a201ea:15 (`evidence-dropped`, same cause) and worker:b8bf806:1; three rows of the lineage) — specification: a RESULT's claims are checked mechanically before the orchestrator judges them: the validation's full-suite comparison names every candidate-minus-base failure, and the head's CI has concluded green as read by the orchestrator; design: the worker's validation.md carries a `Base:`/`Candidate:` line pair and a named extra set, and the orchestrator runs `result-evidence-check.sh <task> <head40> <pr>` on every RESULT before reading its report (C-113); implementation: `.agents/worklog/orchestrator-glue/result-evidence-check.sh` (written 09:56Z; promotion into scripts/orchestrator/ as a task after the pre-send-check pattern); verification: the glue refuses b8bf8066 (`extra=6`, `0 test names`) and accepts the round-2 head only when its extra set is empty or named and its CI runs are all green.

## Rows of the a06 round (CI of b8bf8066 as read by the orchestrator; worker evidence)

ci:b8bf806:1	environment-contract
ci:b8bf806:2	platform-dependent-detection
worker:b8bf806:1	evidence-integrity
security:b8bf806:1	approval-binding
- 2026-10-20T08:01Z: C-80 round 1 (`…-text-security-4a49ed9.md`) `Verdict: incorrect`, one P2 (line 133): NFC-based row matching can credit one threat row to two distinct Linux files (`scripts/café.py` and `scripts/cafe<U+0301>.py`) under `scripts/**`; preserving original paths for filesystem operations does not bind the coverage decision to each file; require identity-aware row matching or collision rejection with a two-file regression before closing the pipeline-identity row. Amendment 1 by the review profile; budget 2 of 3 next.
text-security:4a49ed9:1	input-validation
- 2026-10-20T08:05Z: amendment 1 written whole by the review profile (`a06-checker-r2-prompt.md`) and installed: identity-aware matching through the pipeline triple, a named `path collision` refusal when two distinct files normalise to one key, the two-file regression as the pipeline-identity row's selector; Checks normalised; sha256 4a49ed92… -> 73ac9333b6afcdd437ca1d6cc75ca252517c9a13c5c5bad5938b77eab1caf254. C-80 round 2 next (budget 2 of 3).
- 2026-10-20T08:09Z: C-80 round 2 (`…-text-security-73ac933.md`) `Verdict: correct`; Checks pasted; final sha256 90ca0ae9563df4b352dfb26c6b6aa60132386e15ce9ff50bcf998a43097a12e6; AGMSG-TASK round 1 (reset_of a05-checker) dispatched to a012 (worker-g, wJ:p9) via dispatch.sh (`a06-checker-dispatch.txt`); read_at filled by fill-dispatch.py. The text (final bytes) joins the next records PR so regime-ci verifies the a06 copy.
text-security:73ac933:0	correct
- 2026-10-20T08:11Z: records PR #443 (`records/sync-dispatched-texts-27`, head 40b61c66) carries this text at its dispatched bytes (90ca0ae9…) and the pre-send-check text (ebe84d21…); merged by the orchestrator under D-024-40 once CI is green, so regime-ci verifies the a06 copy on #440.
- 2026-10-20T08:21:55Z: records PR #443 merged by the orchestrator (D-024-40, `--match-head-commit 40b61c66`) -> main 1f97c525; the a06 text is on main.
- 2026-10-20T08:12:36Z: a012 PONG `alive`: a06 TASK read and started; the a06 copy (90ca0ae9…) added; the a05 artifacts restored byte-identical to 06ffefbc; the held draft is this round's content.
- 2026-10-20T08:28:13Z/08:30:55Z: a012 PONGs `blocked`: its independent review of the pipeline draft (source 438/440, tests 698/700; hashes 5c09a95a…/2979c99f…) found [P1] checker:440 a trailing-slash directory scope (`scripts/`) loses its directory intent in the comparison key, so descendants are excluded before confinement (a real escaping symlink passes under `scripts/` and fails under `scripts/**`); [P2] checker:387 the C10 extraction regex excludes combining marks, so a raw NFD path is not captured before the shared resolution (NFC passes, NFD escapes). Disposition (2026-10-20T08:32Z, PING `a06-checker-disposition-1.txt`): both are implementation defects of the prescribed pipeline, repaired within this round with one regression each (equivalent directory scopes on an escaping descendant; NFD/NFC C10 paths); caps retained; if the repair exceeds 440 source lines the orchestrator amends the cap with its attribution (text amendment, C-80, records PR under D-024-40) rather than resetting again.
worker:5c09a95:1	input-validation
worker:5c09a95:2	input-validation
- 2026-10-20T08:37:40Z: a012 PONG `blocked` (cap stop as instructed): with both regressions red first (`test_path_grammar_rejects_escaping_scopes` comparing `scripts/*.py`, `scripts/` and `scripts/**` on the escaping descendant; new `test_c10_confines_original_unicode_script_paths` with raw NFD and NFC paths), the repaired source measures 442 changed lines against 440 and tests 700/700. Disposition (2026-10-20T08:39Z): cap amendment 1 of the a06 text by the orchestrator with the attribution (source 450 = 396 at 06ffefbc + 24 pipeline + 22 for the two review repairs, headroom to the next ten; tests 720), C-80 round, records PR (D-024-40), amendment dispatch; no reset.
worker:5c09a95:3	cap-without-room
- 2026-10-20T08:42Z: cap amendment 1 (orchestrator edit of three sentences: 450/720 with the attribution 396 + 24 + 22 = 442): C-80 round 3 (`…-text-security-b9e04cb.md`) `Verdict: correct`; dispatched to a012 as task_sha256 b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af (previous 90ca0ae9563df4b3…; `a06-checker-amend1.txt`); the text joins records PR sync-28.
text-security:b9e04cb:0	correct
- 2026-10-20T08:49:12Z: a012 PONG `blocked`: the two pipeline repairs are independently verified (source 98c0904f/1779440f; 27 new + 10 legacy methods green on 3.15 and 3.12), but its independent review found a P2 the R4 lint correction introduced (checker:476: the applied-directory classifier runs the metadata name normaliser on filesystem names, so an extensionless backslash filename under scripts/** loses its applied prefix and escapes C12); source 444/450, tests 700/720; the amended task copy (b9e04cb9…) in place. Disposition (2026-10-20T08:50Z, PING `a06-checker-disposition-2.txt`): repair within this round as proposed (applied-directory ancestry from the resolved comparison key's PurePosixPath parents, no metadata grammar), one real-CLI regression, lint again, then independent review, gate, commit, PONG the head.
worker:1779440:1	input-validation
- 2026-10-20T09:15:34Z/09:20:18Z: a012 PONGs `working`: full make measured (base 1267 tests 150 fail 128 err; candidate 1295 tests 156 fail 128 err, the only six added failures the RegimeCiTest subcases owned by #441, now merged); clean selected-tree `make validate-agent-assets` exit 0; frozen source 42183ecc / tests 55c31abd; a C3 observation shown pre-existing (byte-identical at 60a6fb2b); all local proofs and the worker gate complete; commit and PONG of the head expected next.
- 2026-10-20T09:23:57Z: a012 PONG `working`: the a06 round committed locally as head b45caa2b (3 code files + 161 retained a05 + 192 a06 artifacts; the a05 copy byte-identical to 06ffefbc), post-commit verified, awaiting transport. Transport at 2026-10-20T09:34Z failed as a non-fast-forward: the remote head is 762a2541, the orchestrator's `gh pr update-branch` merge of 08:38Z (main b8213131 into 06ffefbc); PING `a06-checker-merge-remote.txt` asks a012 to merge it locally (the same step a013 took on #437) and PONG the new head. Correction C-111: no update-branch of a Codex-seat PR while its worker is mid-round; update-branch only when the chain starts.
- 2026-10-20T09:36:35Z: a012 PONG `blocked`: the local merge of 762a2541 done (head b8bf8066, parents b45caa2b and 762a2541); it asks how the canonical copy and the base's 440 cap resolve. Transported by the orchestrator at 2026-10-20T09:38Z (fast-forward); disposition (PING `a06-checker-transport-done.txt`): the copy stays at the dispatched amended bytes b9e04cb9; regime stays red until records PR #444 (the amended text) merges first; RESULT after the orchestrator reads CI.
- 2026-10-20T09:37Z: head b8bf8066 transported to PR #440 by the orchestrator over HTTPS (D-024-36, `${h}:refs/heads/<branch>`); PING to a012: the a06 copy stays at the dispatched amended bytes b9e04cb9, regime-ci stays red until records PR #444 merges, RESULT after CI as read by the orchestrator.
- 2026-10-20T09:44:40Z: records PR #444 merged by the orchestrator (D-024-40: the copy on its head 661783cc hashes to b9e04cb9… = AGMSG-TASK 2805; sweep `records-sync-28-pr-feedback.json` 5 items, no threads, Codex code and security reviews finding-free; `--match-head-commit 661783cc`) -> main 230b3676. #440's regime run 39402133772 re-run: regime.yml checks out the base tip at run time, so no update-branch is needed for the regime; the ruleset's up-to-date rule still needs one, taken after a012's RESULT (C-111).
- 2026-10-20T09:42:16Z: a012 RESULT round 1 `status=ready_for_review` for head b8bf8066 (task_copy b9e04cb9… = the dispatched amended bytes; branch tools/task-generator-plan-check-a05-checker), sent before the head's Unit-test run ended (09:45Z) although the transport PING asked for the RESULT after CI as read by the orchestrator.
- 2026-10-20T09:45Z-09:50Z: CI of b8bf8066 as read by the orchestrator (Unit-test run 39402138504): `FAILED (failures=7)` of 1296 tests on all three Linux jobs (ubuntu-24.04 client and server, ubuntu-26.04 client); macos-14 client success is no evidence (unit tests are skipped for a Python-only diff). Six failures are `tests/unit/test_regime_ci.py` RegimeCiTest cases reading `checker: no verdict (exit 1): refused: UV_CACHE_DIR must be set to an absolute path`; the seventh is the new `test_canonical_path_pipeline_rejects_normalised_collisions` (`0 != 1 : t-a01.md: OK` inside `finding("C12", prefix=…)`). Snippet install, Agent assets and regime (re-run after #444) are green.
- 2026-10-20T09:51Z: diagnosis from the diff (3 code files: task-consistency-check.py +443, test_task_checkers.py, test_task_consistency_c11_c15.py +655): (R1) `scripts/orchestrator/task-consistency-check.py:37-39` exits at import when `UV_CACHE_DIR` is unset or relative, so every caller that sets none (regime-ci.py's checker launch on main, the regime workflow after a merge, the pre-send glue) gets no verdict; the text's line 117 (`retain … the absolute-cache requirement`) was implemented as a caller obligation while line 47 authorizes no caller edit (C-112). (R2) `confined()` lines 73-79 and `path_entry()` lines 83-89 compute the C12 key only after an `exists()`/`samefile()` probe of the real filesystem, normalisation-insensitive on APFS only, so on Linux the non-existent spelling is dropped before the comparison at line 449. (R3) `validation.md:36` reports base 150 vs candidate 156 failures and calls every failure inherited; the six extra are R1.
- 2026-10-20T09:53:51Z: ACCEPTANCE `status=revise round=1 previous_head=b8bf8066` (2827, `440-revise-1.txt`, read 09:53:57Z): R1 proper state = no import-time refusal, `launch()` uses a set absolute `UV_CACHE_DIR` or a private absolute temporary cache (design 5.14 item 9), one red-then-green test; R2 proper state = C12 compares NFC-folded keys of walked entries and declared rows without probing the alternate spelling; R3 = round 2 names the candidate-minus-base failure set; protocol while the Codex seat has no network: local commit, PONG `working head=<sha40>`, orchestrator transport and `ci=green|red:<names>` PING, RESULT only after `ci=green`; a security-review addendum PING for b8bf8066 follows (review started 09:54Z) and the RESULT waits for it; round 2 is the last worker round.
- 2026-10-20T09:56Z: mechanism (M-20261020-04, C-113): `.agents/worklog/orchestrator-glue/result-evidence-check.sh <task> <head40> [<pr>]` refuses a RESULT whose validation.md shows more candidate failures+errors than the base without each extra test named, and a head whose CI runs are not all green; run on b8bf8066: `refuse: candidate adds 6 failure(s)/error(s) over the base; 0 test names appear` (rc 1).
- 2026-10-20T09:54Z-10:00Z: security review of b8bf8066 (`security-review.sh`, base b8213131; `…-security-b8bf806.md` + `.last.md`): `Verdict: incorrect`, one P1 (high confidence) at `task-consistency-check.py:355`: C6/C15 fetch the normalised comparison key (`path_entry()` turns `cafe\u0301.md` into `caf\u00e9.md`; `main_entry()` normalises at line 176) instead of the original design pathname, so a different canonical file can supply the approval and invariants (reproduced read-only with a modeled API; an ASCII negative control produced C6/C15); the threat rows at text lines 32, 33, 39 and 61 stay unproven. Row `security:b8bf806:1 approval-binding`.
- 2026-10-20T10:01Z: addendum PING (2829, `440-security-addendum-1.txt`) to a012: R4 = the P1 above, proper state original spelling for requests and reads, normalisation only for comparisons, one red-then-green test; round 2 is R1+R2+R3+R4; no further addendum; RESULT after the `ci=green` PING.
- 2026-10-20T12:09:47Z: a012 RESULT round 2 `status=ready_for_review` for head 2cb58482 (task_copy b9e04cb9…; validation: exact 278-vs-278 full-suite comparison, candidate-minus-base []; 48/48 mutants killed on 3.15 and 3.12; evidence precheck ok; CI all green as read by the orchestrator). ACCEPTANCE `status=pending-integration round=2` (2835) at 12:10:58Z.
- 2026-10-20T12:19Z-12:38Z: chain on 2cb58482 (CI green; sweep; sandbox-scan 0): local review (`…-local-review-21f52c7.md`) 1 P1 + 2 P2: [P1] task-consistency-check.py:182 the new `gh api` requests (canonical main, design bytes for C6/C15, C8/C9 lookups) run in regime CI through regime-ci.py's minimal environment without `GH_TOKEN`/`GITHUB_TOKEN`; a fresh runner has no gh login, so after this checker lands every task text that references a design gets `no verdict` in the regime check (main's checker makes no API call today; the regime run on 2cb58482 passed because it executed the base's checker); [P2] :476-480 Claude instruction shims are not classified as applied files; [P2] :348-350 overlapping directory scopes need a separate row. The two P2 are advisory rows under dotfiles-T133-task-generator-plan-check-followup-a01 (recorded by the chain). The P1 is a caller-side dependency, not a defect of the changeset: the fix is the regime workflow passing `GH_TOKEN: ${{ github.token }}` and regime-ci.py forwarding it into the checker's environment (the checker already forwards both tokens when present, line 149; `test_gh_child_preserves_parent_tokens`). Disposition as for PR #411's `--premises-sha` dependency: #440 waits for `dotfiles-T133-regime-ci-token-a01` (text authored now, Claude seat), then takes the new base, and its chain (audit, record, gate) runs on that head. Worker rounds stay spent; no third round.

local:21f52c7:1	caller-dependency
local-finding: 21f52c7:1 not-applicable:sequencing dependency on dotfiles-T133-regime-ci-token-a01 (the regime workflow and regime-ci.py supply the token to the checker; #440 merges after it lands and is update-branched); evidence=git show 2cb584823ccf5f22069ea925b252d8cefb020844:scripts/orchestrator/task-consistency-check.py | sed -n 149p


## Owned by dotfiles-T133-task-generator-plan-check-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:21f52c7:2	advisory-p2
local-finding: 21f52c7:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (a792f57b99ca5c605c4188cd23464191dbba26cda750cf2d50ae193375c33b8a)
local:21f52c7:3	advisory-p2
local-finding: 21f52c7:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (a792f57b99ca5c605c4188cd23464191dbba26cda750cf2d50ae193375c33b8a)
local:21f52c7:4	advisory-p2
local-finding: 21f52c7:4 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (R08-F1 of dotfiles-T133-inv6-reset-anchors-review-a01: the a06 text omits the a05 predecessor obligation 'text-defect checker / long-Checks prevention' or an explicit owner disposition; the a05->a06 reset anchor is re-reviewed as one item after this row)

- 2026-10-20T15:00Z: reset-anchor review R08-F1 (a012, `dotfiles-T133-inv6-reset-anchors-review-a01`): the a06 text omits the a05 predecessor obligation 'text-defect checker / long-Checks prevention' or an explicit owner disposition. Disposition: owned by dotfiles-T133-task-generator-plan-check-followup-a01 (row `local:21f52c7:4 advisory-p2`); the a05->a06 reset anchor is re-reviewed as one item after this row.

local:c439b63:2	advisory-p2
local-finding: c439b63:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (a792f57b99ca5c605c4188cd23464191dbba26cda750cf2d50ae193375c33b8a)
local:c439b63:3	advisory-p2
local-finding: c439b63:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (a792f57b99ca5c605c4188cd23464191dbba26cda750cf2d50ae193375c33b8a)

- 2026-10-21T07:50Z: chain on c439b63c (update-branch of fefa1dcc after boundary 27; PR patch-id 3deeac540b9be86c unchanged since 2cb58482): CI 7 required green; local review `…-local-review-c439b63.md` 1 P1 + 2 P2 (the P2 rows above); the chain stopped at local-advisory (exit 11, plan 020 step 4.2: the PR's one round is over, the P1 goes to the operator). Manual continuation under the interim exemption: sweep 8/8 with `440-extra.tsv` (gaps 0), receipt and record block regenerated for c439b63. The P1 and the two P2 of the round-2 security review `…-security-2cb5848.md.last.md` (never dispositioned until now) are dispositioned below as advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01; D-024-57 records the judgement and its default; the audit and the security review of c439b63c follow through the operator's codex route.

local:c439b63:1	advisory-p2
local-finding: c439b63:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225: `main_texts` decodes every canonical blob strictly, so a C8 traversal that reaches home/.key.txt.age aborts with UnicodeDecodeError; the abort is fail-closed (non-zero exit, no false acceptance), so the orchestrator grades it P2 robustness, not P1); evidence=sed -n 225p scripts/orchestrator/task-consistency-check.py at c439b63c prints `yield main_bytes(root, name).decode()` and the reviewer's read-only reproduction is in the local review file
security:2cb5848:1	input-validation
security-finding: 2cb5848:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (task-consistency-check.py:476 C12 classifies only the resolved target, so an unnamed applied symlink to a non-applied target passes a wildcard scope without a concrete threat row; the checker is a pre-dispatch consistency check, the runtime boundary is the worker sandbox, and the orchestrator reads every threat table by hand until the owner task lands); evidence=.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md finding 1
security:2cb5848:2	input-validation
security-finding: 2cb5848:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (task-consistency-check.py:251 the missing-literal shortcut returns before examining directory symlinks, so a missing file beneath an internal directory alias bypasses the internal-alias rejection; same compensating controls as row 1); evidence=.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md finding 2

## Round 2 final head c439b63c: task-level audit 2026-10-21T08:07Z (operator-run `orch-audit.sh`, `…-audit-c439b63.md.last.md`)

**Verdict: incorrect**: one implementation P1, three implementation P2, five orchestration P2. Per D-024-57 an audit P1 resets the lineage: D-024-58, reset to `dotfiles-T133-task-generator-plan-check-a07-checker` by another context, no third round; a012 holds (ACCEPTANCE 2983). The security review of c439b63c is not run (no merge of this head).

audit:c439b63:1	invariants-validation
audit:c439b63:2	probe-status
audit:c439b63:3	scope-rows
audit:c439b63:4	instruction-shim-classification
audit:c439b63:5	sweep-disposition-wording
audit:c439b63:6	counters-evidence
audit:c439b63:7	cap-measurement
audit:c439b63:8	design-conflict
audit:c439b63:9	checks-omission

Row 1 (P1): task-consistency-check.py:496, C15 accepts arbitrary `invariants` when `design_review.design` is omitted, bypassing canonical assignment and byte-equality validation (a07 item). Row 2: :312 the `grep -c` probe always returns status 0 (same defect as local:c439b63:2; a07). Row 3: :348 C4 accepts one `scripts/orchestrator/` row for both `scripts/` and `scripts/orchestrator/` scopes (same class as local:21f52c7:3; a07). Row 4: :476 C12 does not classify `CLAUDE.md` as applied instructions (same class as local:21f52c7:2; a07). Row 5 (orchestration): the GitGuardian issue comment of #440 was dispositioned by the generic issue-comment template; the next sweep carries a specific row (the fixture digest and a commit id are refutable), as 442-extra.tsv already does for #442. Row 6 (orchestration): the revise at line 416 lacked a counters snapshot; snapshot taken 2026-10-21T08:07Z (C-126): a05-checker TASKs=3 revises=2 questions=2 blocked-PONGs=10 (S2, silenced by the a05 design-reset record); a06-checker TASKs=2 (the cap amendment resend) revises=1 RESULTs=2 questions=0 blocked-PONGs=6. Row 7 (orchestration): the auditor's 517/1505 was measured from a base other than the merge-base; the C-123 measurement is `git diff --numstat e00de4e0 c439b63c` = 446 outside tests/ (task-consistency-check.py 419+27) and 709 under tests/ (35+22, 652+0), within 450/720; not-applicable, evidence pasted here. Row 8 (orchestration, real): the R1 revise directed an unset-cache fallback (checker line 138) while frozen design 5.14 item 9 requires refusal when UV_CACHE_DIR is absent; a07 restores the refusal and the record names this conflict as the orchestrator's error. Row 9 (orchestration, real): the dispatched Checks block omitted the prerequisite API observations the text's line 107 requires; a07's Checks are complete before its anchor review.

audit-finding: c439b63:7 not-applicable:measured from the merge-base per C-123, 446/709 within 450/720; evidence=git diff --numstat e00de4e0e4158de19e2c8921e572461e7e9e4ca0 c439b63c65285ec8180dc3e21394c87ef21115b4

---
format: 2
task_id: dotfiles-T133-task-generator-plan-check-followup-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/task-from-plan.py
  - scripts/orchestrator/plan-check.py
  - tests/unit/test_task_from_plan.py
  - tests/unit/test_plan_check.py
  - scripts/orchestrator/task-consistency-check.py
  - tests/unit/test_task_consistency_c11_c15.py
  - .orchestration/dotfiles-T133-task-generator-plan-check-followup-a01/**
after: [dotfiles-T133-task-generator-plan-check-a01, dotfiles-T133-worker-write-boundary-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/task-from-plan.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits scripts/orchestrator/plan-check.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_task_from_plan.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_plan_check.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits scripts/orchestrator/task-consistency-check.py only within the owned rows (item 1; audit:8a09b93:10 the C11 selector grammar, audit:8a09b93:1-3 C15 and C12)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record, each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_task_consistency_c11_c15.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-task-generator-plan-check-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T133-task-generator-plan-check-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the scripts with fakes on PATH in temporary directories; nothing live changes"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run under uv run --no-project python -I"
  - control: new or renamed scripts
    disposition: "residual: none; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises: []
---

# AGMSG-TASK dotfiles-T133-task-generator-plan-check-followup-a01 — the P1-12 lineage's owner task (advisory P2 of PR #417)

Written 2026-10-18 by the orchestrator seat before the first advisory disposition of PR #417 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T133-task-generator-plan-check-followup-a01` in `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a01.md` (plan 020 step 1.2; the a01 record is the lineage record); it is dispatched after PR #417 merges, to a seat the orchestrator names.

## Item 1

Each owned row (any advisory P2 of the local review or the task-level audit of PR #417's final head, and any Bot P2 the orchestrator records under this owner; rows are read from the records at dispatch) gets its fix and one red-then-green test in `tests/unit/test_task_from_plan.py` or `tests/unit/test_plan_check.py`, named in report.md against the row id. Nothing outside the owned rows; `scripts/orchestrator/task-consistency-check.py` and `tests/unit/test_task_consistency_c11_c15.py` join `allowed_files` only by an amendment that names the row needing them.

## Orchestrator note (2026-10-19T04:3xZ): row order and the C11 grammar first

The owned rows are read from `## Owned by dotfiles-T133-task-generator-plan-check-followup-a01` in `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a02.md` (the audit of 8a09b936: twelve rows, and the parser-gap lineage rows audit:9da0ed3:10-13 under the parser-gap re-plan in that record's JSON block). The first push fixes row `audit:8a09b93:10` alone: C11 accepts the pytest node id `tests/<path>::<Class>::<test>` as well as `tests/<path>::<test>`, red against 8a09b936 with the a02 task copy as the fixture; the orchestrator dispatches no text through the merged checker before that push lands on main. The remaining rows follow in the same PR. The design 5.14 trusted-host contract applies to the scripts this task edits as far as they execute anything (they do not).

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a01.md` apply as written, with `dotfiles-T133-task-generator-plan-check-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-task-generator-plan-check-followup-a01/task.md>` in the RESULT.

## Owned from the a06 final head c439b63c (recorded 2026-10-21T07:50Z)

- `task-consistency-check.py:225` strict decode of canonical blobs: C8's traversal of `home/` reaches `home/.key.txt.age` and aborts with UnicodeDecodeError; decode with a fixed fallback or skip undecodable blobs, with a regression that plants a binary canonical file (local:c439b63:1, graded P2 by the orchestrator because the abort fails closed).
- `task-consistency-check.py:310-312` preserve grep's failure status when no lines match (local:c439b63:2).
- `task-consistency-check.py:83` relativise case-aliased symlink targets by filesystem identity, not by case-sensitive `relative_to` (local:c439b63:3).
- `task-consistency-check.py:476` C12 classifies the resolved target only: an unnamed applied symlink to a non-applied target passes a wildcard scope without a concrete threat row (security:2cb5848:1).
- `task-consistency-check.py:251` the missing-literal shortcut returns before directory symlinks are examined, so a missing file beneath an internal directory alias bypasses the internal-alias rejection (security:2cb5848:2).


 succeeded in 171ms:
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-2cb5848.log
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-21f52c7.md
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-audit-c439b63.md.last.md
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-c439b63.md
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-21f52c7.log
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-c439b63.log
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-audit-c439b63.md
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md

 succeeded in 202ms:
home/dot_local/bin/common/executable_agmsg-dispatch	Orchestrator wake path that sends an agmsg message, wakes an idle Herdr worker pane, and polls for the read receipt with one bounded retry, never sending the message body to the terminal.
home/dot_local/bin/common/executable_agmsg-dispatch	Polls the agmsg store for this message's read receipt until the given SECONDS value or the shared deadline.
tests/unit/test_agmsg_dispatch.py	unittest suite driving agmsg-dispatch against isolated SQLite storage and fake herdr/agent CLIs, covering identifier grammar, idle-only wakes, unread retry, shared timeout budget, and wake-failure reporting.
tests/unit/test_agmsg_dispatch.py	Test case running agmsg-dispatch with fake scripts and a temporary SQLite DB to verify wake, retry, and timeout semantics.
e00de4e0e4158de19e2c8921e572461e7e9e4ca0
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

**Managing token budget**
exec
/bin/zsh -lc "sed -n '103,123p' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
 succeeded in 27ms:
## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）

orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。

1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19). The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).
2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder; a `gh api graphql` call binds the repository through fixed query variables (`owner: "mryfmo"`, `name: "dotfiles"` as constants in the script, passed with `-f`/`-F`) and uses only node ids obtained from a query bound by those variables (verdict a04 C-80 round 5, 2026-10-19): the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged. The sha of canonical `main` comes from the fixed repository's API (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`), never from `git ls-remote origin`, whose destination the local remote and URL-rewrite configuration control (P1-12 a04 C-80, 2026-10-19T20:01Z); the content read at that sha comes from `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>`. Every `gh api` call that decides also binds the host with `--hostname github.com` (`GH_HOST` and the hosts configuration select the API host otherwise), a subcommand binds it through the `github.com/mryfmo/dotfiles` form of `--repo`, and a test that exports a hostile `GH_HOST` shows the call still names github.com or refuses (a02 review b2a186e, 2026-10-19T20:36Z).
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

**Reviewing local contract document**
codex
The task inherits controls that a06 explicitly left open, including executable and cache selection before the checker starts. I’m checking whether a07 preserves those limits accurately and whether each “closed” row’s test supports its claim. I won’t update worklogs or review receipts because this review is read-only.
exec
/bin/zsh -lc "sed -n '81,260p' .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-audit-c439b63.md.last.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-c439b63.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-21f52c7.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git show c439b63c65285ec8180dc3e21394c87ef21115b4:.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md | head -80; git ls-tree --name-only c439b63c65285ec8180dc3e21394c87ef21115b4 .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/' in ~/Workspace/dotfiles
 succeeded in 89ms:
## Goal and lineage

This text is the reset after INV-6 S2 and C-61 under D-024-39; the a05 findings history is in `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md`.
The a05 text's two amendments and two worker fix rounds are spent; this reset authorizes its measured pipeline round rather than a third a05 repair.

Amendment 1 addresses C-80 round 1's `text-security:4a49ed9:1 input-validation` row; `previous_sha256: 4a49ed9263e025e84f3ec5a51df553cfc83ab71192a4de016770e42a1f80491b`. Read `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-4a49ed9.md.last.md` whole. Only identity-aware coverage and collision rejection, with their regression, change.

Read the a05 task and acceptance record whole, including the carried a04 audit rows and both `re-plan: glob-filter` decisions. Also read both security reviews whole:

- `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-cedc7f5.md.last.md`
- `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-06ffefb.md.last.md`

[memory:failure] PR #417's a01–a04 lineage was withdrawn after the audit of `7a201eab2e77596c9a7bc421162b2f3fde25f6f7`; the a05 record carries its findings and re-plans. Preserve that history; do not revive the withdrawn three-script implementation.

[memory:decision] Plan 024 P1-12 continues only the checker C11–C16 and its tests. Worker a012 (Codex, worker-g) continues PR #440, branch `tools/task-generator-plan-check-a05-checker`, from `06ffefbc633fe37bcef107385ea96810b2a9a0c5`, with fixed measurement base `60a6fb2b324d0381c4a6e539b37c650105154a7e`; do not start a fresh branch or PR.

The held, uncommitted pipeline draft is input to this round, not verified completion. Preserve the existing R4 lint correction. The a05 report records 32 green checker tests on Python 3.15.0 and 3.12.15 and 28/28 killed mutants; rerun against the new head.

`task-from-plan.py`, `plan-check.py`, templates, workflows, dispatch, resolver implementation, deployment and canonical orchestration records remain outside scope.

## Dispatch prerequisite and design

Boundary PR #435's merged state and design publication remain dispatch prerequisites. The orchestrator, which has network access, obtains canonical main with `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; validate exactly 40 lowercase hexadecimal characters before substituting `<sha40>`.

Read `gh api 'repos/mryfmo/dotfiles/contents/.orchestration/plans/024-design-quality.md?ref=<sha40>' --hostname github.com --jq .content | base64 -d | grep -F 'Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。'`. Require successful exits from every stage and reject missing or malformed content; successful grep alone is insufficient.

Before sending, record #435's merged state from the fixed repository/host API, pinned main SHA, decoded design SHA-256, commands and stage exits in Checks. Local refs, objects, replacement objects, URL rewrites and local digests supply no prerequisite authority. `after: []` does not waive this boundary.

Design 5.14 at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen under D-024-29 and applies by reference under D-024-30; every item 0–10 has its own threat row above. Do not paraphrase or amend the frozen design.

Premises record local provenance only. Re-run applicable probes before dispatch and paste results in Checks; authoring commands do not extend C14's vocabulary or authorize shell execution.

## Implementation contract

1. Retain interpreter selection: landed `scripts/orchestrator/trusted-interpreter.sh` first, supplied `TRUSTED_PYTHON` second, real `sys.executable` with an explicit stderr fallback warning last. Validate the selected interpreter; resolver failure or invalid supplied input refuses rather than falling through. Add no interpreter PATH discovery.

   Neither `TRUSTED_PYTHON` nor `TRUSTED_BIN_DIR` becomes mandatory. Retain checker-side executable binding when dispatch strips both, and the absolute-cache requirement. No dispatch edit or outer environment prefix repairs this slice.

   Parent PATH-selected mise/uv and shared-cache execution happen before these defenses. Parent hardening belongs to dotfiles-T133-loop-limits-a01, executable binding to dotfiles-T133-trusted-entrypoint-binding-a01, resolver/private UV_CACHE_DIR to dotfiles-T133-ci-efficiency-followup-a04; this slice closes none of those boundaries.

2. C14 consumes `(stdout, exit_status, stderr)`; every nonzero status produces a finding even with matching or empty stdout. Keep dispatched-byte digest authorization, warning without authorization, whitespace comparison and fixed read-only vocabulary. Unsupported commands never reach a shell.

3. Preserve parent `GH_TOKEN` and `GITHUB_TOKEN` exactly for `gh` children, testing each independently, both and neither. Forward through the subprocess environment mapping, never argv or printed values. Retain other sanitization and explicit repository/host binding; dispatch forwarding remains unchanged.

4. C15 accepts referenced designs only from canonical GitHub main, including tasks without invariants. Validate the 40-hex SHA from the fixed repository/host API, then read `gh api repos/mryfmo/dotfiles/contents/<path>?ref=<sha40> --hostname github.com`. Local-only designs fail C15; API failures refuse. Preserve assignment-set and byte-equality checks; hostile `GH_HOST`, local Git configuration and local objects supply no authority.

   C6 uses the same pinned canonical bytes as C15. When `design_review.design_sha256` is present, require its exact SHA-256 over decoded API bytes and a matching `design_review.receipt` against the canonical receipt. When absent, retain legacy canonical receipt comparison and emit a C6 warning naming the missing field. Missing canonical bytes or binding, malformed/mismatched hashes and API failures cannot pass; no local receipt or design supplies authority.

5. Commit one canonical `path_entry` pipeline, consumed by every path-bearing check, explicitly C6/C10/C11/C12/C14 and C16 applicability. Keep the original enumerated path for reporting and filesystem operations, resolve that original to its real target for confinement and applicability, and normalize names to NFC only for comparison. Return the pipeline triple `(original enumerated path, resolved target, comparison key)` together; checks must not independently normalize a pathname before resolving it.

   Matching is identity-aware: a threat row or `allowed_files` entry covers a file only through that file's pipeline triple. The comparison key uses NFC, with case folding where the filesystem folds case. If two enumerated files share a key but have distinct filesystem identities (different resolved paths, or the same path with different byte names on a case- and normalisation-sensitive filesystem), refuse both with `path collision: <a> and <b> normalise to the same key` instead of crediting either.

   Apply it to scopes, threat-row path tokens, design paths, selector paths, applied-file classification and C14 file operands. Git refs remain refs. Preserve the grammar:
   - Repository-relative POSIX literal files, trailing-slash directories and globs; root files need no slash. Remove redundant `./` components consistently.
   - Component-local `*`, `?` and bracket classes; whole-component `**` spans zero or more components. Reject Git pathspec magic, exclusions, escapes and absolute paths after lexical cleanup; never interpret them as scope.
   - Parent traversal, including `../../x/*.py`, and escaping symlinks produce confinement findings, never silent skips. Check symlinked directory prefixes before full-match filtering.
   - Directory and child rows remain separate entries; match normalized path tokens to their own entry. Ancestor substrings do not violate C7b, but a row naming two entries does.
   - Enumerate regular files under fixed scope roots, including ignored and untracked files. Do not follow directory symlinks or scan Git administration. Reject internal directory aliases in literal and glob scopes, even with an explicit row; the index grants no exclusion.
   - Directory pruning compares normalized names against normalized scopes while confining the original directory. A decomposed-Unicode directory must not hide applied files or escaping symlinks.
   - Applied files include root `AGENTS.md`, `Makefile` and `.claude/skills/<name>/SKILL.md`; C12 requires concrete rows for applied wildcard matches, using resolved-target classification.
   - Fixture/evidence exemptions require confinement of the original path, real-target identity beneath the corresponding exempt root, and classification consistent with that exemption. Lexical prefixes or normalized aliases alone grant nothing; retain deterministic case-insensitive checks.

6. Retain C16 under D-024-30: a `security: true` orchestrator-side task explicitly references design 5.14 and has exactly one row for each item 0–10. Determine applicability from canonical scope entries and resolved targets, including covering globs and a literal file symlink into `scripts/orchestrator/`. Match item numbers distinctly, count every occurrence, reject omissions, duplicates and multi-item rows, and preserve non-applicable tasks.

7. Retain only the predecessor directory inventoried above, unchanged from `06ffefbc`; its task.md is historical data. Create this reset's own byte-identical dispatched copy and evidence in its allowed directory. Import or delete no earlier lineage directories. Exercise C2/C3 with the retained predecessor and own-copy rows; hidden predecessor edit scopes using `./` still fail C2. The complete changed-file list and reset lineage must pass regime-ci; no deferred disposition of applicable scope failures.

Retain all other C1–C15 behavior, C11 class selectors, confinement, non-execution and trusted-execution negative controls. Port no dependency on the two deferred scripts.

## Required regression fixtures

Keep the 16 a05 contract fixtures below and their historical behavioral reds at `7a201eab`; rerun every selector green on the final head. Valid controls assert the intended behavior, not an unrelated refusal.

| Behavior | Selector |
| --- | --- |
| Interpreter precedence and invalid-input refusal | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_interpreter_resolution_order` |
| Exact unchanged dispatch invocation without stripped variables | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_dispatch_env_i_invocation` |
| Failed C14 probe with matching stdout | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c14_rejects_failed_probe_with_matching_stdout` |
| Tokens preserved only in the intended child environment | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_gh_child_preserves_parent_tokens` |
| C15 canonical repository, host and SHA without invariants | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_uses_canonical_main_only` |
| C6 receipt/hash against the same canonical bytes as C15 | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes` |
| Glob grammar and Git pathspec rejection | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_distinguishes_globs_from_git_pathspecs` |
| Root literals and applied root-file coverage | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_covers_root_files` |
| Separate directory/child rows and combined-row rejection | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_separates_directory_and_child_rows` |
| Equivalent dot spellings | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_normalises_dot_spellings` |
| Traversal, escaping scope and symlink-prefix refusal | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_rejects_escaping_scopes` |
| Exempt symlink cannot hide an applied production file | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_symlink_to_applied_file_is_finding` |
| Deterministic case-alias refusal | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_case_alias_to_applied_file_is_finding` |
| Applied skill instructions, including untracked matches | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_covers_applied_skill_instructions` |
| C16 reference, omissions, duplicates and valid control | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c16_requires_reference_and_all_item_rows` |
| Reset-copy coverage and hidden predecessor scope refusal | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_reset_scope_rejects_hidden_predecessor_artifacts` |

One red-then-green regression per finding of the two security reviews is mandatory, with the finding ID bound to its selector:

| Finding or invariant | Selector |
| --- | --- |
| security:cedc7f5:1 — resolve original Unicode pathname | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_resolves_original_unicode_path` |
| security:cedc7f5:2 — reject internal directory aliases | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_rejects_internal_directory_alias` |
| security:cedc7f5:3 — count every item occurrence; reject combined rows | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_rejects_multi_item_rows` |
| security:06ffefb:1 — normalized pruning cannot hide files or escaping symlinks | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_prunes_with_normalised_directory_names` |
| security:06ffefb:2 — resolved literal alias triggers C16 | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_uses_resolved_literal_alias` |
| Enumerated, resolved and matched identities agree across pipeline consumers | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_canonical_path_pipeline_preserves_identity` |
| text-security:4a49ed9:1 input-validation — distinct-file collision refusal and single-file coverage | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_canonical_path_pipeline_rejects_normalised_collisions` |

Preserve the three cedc7f5 reds and their greens at `06ffefbc`; they stay green. The two 06ffefb findings and pipeline-invariant test must fail behaviorally at `06ffefbc` before the pipeline fix and pass after it. Add valid confined controls; preserve raw-path reporting and demonstrate name normalization never changes the target confined.

The collision regression plants both `scripts/café.py` (precomposed) and `scripts/café.py` (`e` followed by U+0301, decomposed) under `scripts/**`, with one concrete threat row. Where the filesystem keeps them distinct, expect the named collision finding and no coverage credit for either file. Probe and state the observed filesystem behavior; skip only the two-file case with a stated reason where name normalisation aliases them, rather than assuming behavior from APFS/HFS+ or the OS. A separate one-file case expects normal coverage and no collision, and runs even where the two-file case skips. Record the collision regression's behavioral red before its fix and green after it.

The dispatch fixture reproduces `env -i`, PATH/HOME/absolute UV_CACHE_DIR, optional LANG/LC_ALL, exported AGMSG_* and the existing pinned offline uv launch followed by `python -I <checker> --root <root> <task>`. Assert real arguments, environment and verdict; this proves checker compatibility only. Model Unicode/case distinctions deterministically on insensitive hosts and disclose unavailable native coverage.

## Commands

Use validated absolute, non-shim interpreter and uv bindings, isolated Python, offline dependencies and temporary absolute caches. Record tool paths, hashes and versions; do not trust a checkout executable, ambient .venv or caller Python startup state. The host-provisioned 3.12 floor is `$HOME/.local/share/mise/installs/python/3.12.15/bin/python3.12`; validate it before use.

Run each complete checker module with both Python 3.12.15 and the current Python 3.15.0 binding, expanding placeholders and recording the exact commands:

```
<absolute uv> run --no-config --no-project --offline --python <absolute interpreter> --with pyyaml python -I -m unittest discover -s tests/unit -p 'test_task_consistency_c11_c15.py' -v
<absolute uv> run --no-config --no-project --offline --python <absolute interpreter> --with pyyaml python -I -m unittest discover -s tests/unit -p 'test_task_checkers.py' -v
```

For individual selectors, use the recorded isolated bootstrap that inserts only the validated absolute test root; do not depend on importing an uninstalled tests namespace through CWD. An unavailable runtime or dependency is a blocked operation, not a red test.

## Check

Write regressions before fixes. Record checker revision/SHA256, regression-source SHA256, actual interpreter/version, expanded commands, complete stdout/stderr and exits for historical reds and final greens. Import errors, absent dependencies, missing tests, unrelated refusals and zero-test runs are not red proofs.

Run `make unit-test`, required formatting, changed-file R4 lint and relevant validators. Compare inherited failures against the unchanged base in the same environment; preserve their exact multiplicities, never label them green or repair outside scope. Do not run Bats locally; the orchestrator reads final-head GitHub Actions and returns the results before RESULT.

Paste mutation totals as `mutations=<observed> killed=<observed> survived=<observed>` with per-mutation outcomes. Retain the 28 prior controls and independently disable each new pipeline behavior; its named fixture must kill the mutant. Commit no mutants or mutation framework; unexplained survivors block completion.

The complete final diff has at most 450 changed lines outside `tests/` and `.orchestration/`, and at most 720 under `tests/`.
Measure with `git diff --numstat 60a6fb2b...<head40>`, substituting the validated full final head.
All production changes are in the one allowed checker. The cap attribution (amendment 1, 2026-10-20T08:4xZ) is a05's 396 changed source lines at 06ffefbc, plus the pipeline draft's measured +24 = 420, plus the two independent-review repairs measured by the worker at +22 (directory intent kept in the comparison keys; the original C10 path extracted before resolution) = 442, with headroom to 450; the test cap 720 covers the measured 700 plus the two regressions those repairs add; no further cap increase is authorized.

Count additions plus deletions for both source and tests, as regime-ci does. The held draft's tests measured 704 changed lines before and 700 after the repairs the worker made; the two review regressions fit within 720, so no control is dropped to make room.
Paste the complete numstat, `git diff --name-only 60a6fb2b...<head40>`, per-file arithmetic and both totals in measure.md and RESULT. Do not hide runtime code in artifacts, remove defenses or change a lint baseline to fit.

The whole authored file, including its empty Checks block, is at most 260 lines and has exactly four allowed_files entries. The worker never edits the orchestrator's Checks content; a populated dispatch block is separately identified as appended metadata, never silently excluded from a claimed count.

Run the checker on dispatched bytes and record C14's warning without `--premises-sha`; authorized fixtures use their supplied trusted digest. Never invent dispatch authority from branch bytes or add shell support for authoring probes.

## Completion and evidence

Worker Playbook step 4 applies with this host's measured facts: Codex seats run without network since the daemon restart (D-024-36), so the worker commits locally, PONGs the full head, and the orchestrator transports it to PR #440 and reads CI for the worker; every other command runs inside the sandbox, and any refused command is reported as `AGMSG-PONG v1 status=blocked` with exact command, exit, output and boundary.

Do not retry a refusal through another tool, broader permission or sandbox escape. An orchestrator transport or CI read is not worker permission to leave the sandbox. Record unavailable live API validation honestly and retain local fake-API controls.

Commit report.md, validation.md, sandbox.md, learning.md, autoskill.md (status or not-used), measure.md, the byte-identical task.md and worker review evidence under this task's directory before RESULT. Verify with `git ls-files` that no required evidence remains untracked; this overrides generic untracked-artifact handoff. Codex plan/todo/learn worklogs remain uncommitted.

Use agent-side Crit data and a worker receipt in the allowed directory, with resolved records and the receipt's review_surface/reviewer/review_source/review_outcome binding; no browser, publication or human review request. Run `make require-crit-review` with the required evidence. Retain INV-6/S1 lineage accounting; repeated finding classes require a recorded re-plan, not private patch rounds.

The orchestrator transports every new committed head, checks final-head CI and performs Worker Playbook's bounded Bot procedure for the worker, returning exact observations. Fresh applicable CI follows an evidence-only push too. Keep the existing PR's English title/body current through the orchestrator; the worker never merges or edits canonical acceptance, decision or plan records.

Send `AGMSG-RESULT v1 status=ready_for_review` only after required checks pass. Include full head/base, branch, PR #440, task-copy SHA256, changed-file inventory, retained predecessor directory, final numstat/totals, selectors, historical and new red/green counts, mutation outcomes, CI/Bot observations, proposed feedback dispositions and every artifact path. Report `cost:` with observed figures or `n/a`.

After final-head CI and the required security review, the orchestrator follows Orchestrator Playbook step 10: complete feedback sweep, dispositions, task audit, acceptance record and gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE`. Neither a05 review nor previous CI approves this head.

Deferred checks and changes: generator, plan checker, workflows, dispatch/resolver implementation, deployment and local Bats.
Residual risk: unchanged parent execution, shared cache, credentials and same-UID interference remain; checker fixtures establish no host isolation.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T08:39Z before send 2 (amendment 1, the cap) to a012: the measured repair (source 442, tests 700; a012 PONG 08:37:40Z) exceeded 440, so the cap is 450 source / 720 tests with the attribution stated in the Check (396 + 24 + 22 = 442); nothing else changed; previous_sha256 90ca0ae9563df4b352dfb26c6b6aa60132386e15ce9ff50bcf998a43097a12e6; C-80 verdict and pre-send results follow in the AGMSG-TASK note
PR #440 continues on tools/task-generator-plan-check-a05-checker from head 06ffefbc with your uncommitted pipeline draft as this round's content (source cap 450 = 396 + 24 pipeline + 22 review repairs = 442 with headroom; tests 720); the Codex seats have no network (D-024-36): commit locally, PONG the head, the orchestrator transports it and reads CI; the six RegimeCiTest reds stay until #441 merges; task SHA256 in the AGMSG-TASK line, computed over these final bytes
```

 succeeded in 120ms:
Audited [PR #440](https://github.com/mryfmo/dotfiles/pull/440) at `c439b63c65285ec8180dc3e21394c87ef21115b4`. Final-head CI is green; all three Linux jobs executed Python tests. Source hashes, dispatched-copy identity, retained predecessor artifacts, and recorded test totals reconcile.

- [P1] high implementation `scripts/orchestrator/task-consistency-check.py:496` C15 accepts arbitrary `invariants` when `design_review.design` is omitted; a read-only reproduction returned no findings, bypassing canonical assignment and byte-equality validation.
- [P2] high implementation `scripts/orchestrator/task-consistency-check.py:312` The `grep -c` probe always returns status 0; an unmatched pattern produces actual grep status 1 but passes C14 with expected output `0`, violating the failed-probe requirement.
- [P2] high implementation `scripts/orchestrator/task-consistency-check.py:348` C4 accepts one `scripts/orchestrator/` row for both `scripts/` and `scripts/orchestrator/` scopes; reproduced with no findings despite the separate-row requirement. The previously recorded advisory remains.
- [P2] high implementation `scripts/orchestrator/task-consistency-check.py:476` C12 does not classify `CLAUDE.md` as applied instructions; `CLAUDE*` passes without a concrete row despite matching the existing instruction shim. The previously recorded advisory remains.
- [P2] high orchestration `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-pr-feedback.json:70` GitGuardian’s two specific detections are dismissed as “no finding”; the cited evidence merely selects that comment. Both can be specifically refuted—the synthetic-token digest and a Git commit ID—but that analysis is absent from the disposition.
- [P2] high orchestration `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md:416` The record documents a revise action without the required preceding `regime-counters.sh` output or substitute source readings; the complete record contains no such counter evidence, leaving INV-6 accounting unverified.
- [P2] high orchestration `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:212` The prescribed fixed-base measurement now totals **517 production / 1,505 test lines**, exceeding **450 / 720**; retained evidence reports **446 / 720**. Upstream merges explain the difference, but the final-head measurement contract and evidence were not reconciled.
- [P2] high orchestration `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md:416` R1 directs an unset-cache fallback, implemented at checker line 138, while frozen design 5.14 item 9 explicitly requires refusal when `UV_CACHE_DIR` is absent; the record provides no corresponding design exception or reconciled task amendment.
- [P2] high orchestration `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:243` The dispatched Checks block omits the required prerequisite API observations: PR #435 merged state, pinned main SHA, decoded design hash, commands and stage exits; task line 107 explicitly requires these before dispatch.

The task declares no `invariants` map; its only explicitly named invariant is INV-6.

INV-6: violated `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md:416` — required acceptance-time counter evidence is missing.

Orchestration findings: 5

📝 まとめ: 指定 head の監査を完了し、実装4件・オーケストレーション5件を報告しました。変更は行っていません。

Not rerun: full local suites or Bats; findings above remain unresolved.
Verdict: incorrect---
task: dotfiles-T133-task-generator-plan-check-a06-checker
head: c439b63c65285ec8180dc3e21394c87ef21115b4
pr: 440
base: e00de4e0e4158de19e2c8921e572461e7e9e4ca0
started: 2026-10-21T07:28:37Z
finished: 2026-10-21T07:40:21Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83

```text
Read-only reproductions confirmed a baseline-search crash, a case-aliased path crash, and an incorrectly accepted failed probe. The full unit suite and CI were not rerun.

Full review comments:

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
  When C8 checks a new `*_EVIDENCE` name absent from Makefile and scripts, traversal reaches the existing encrypted `home/.key.txt.age`. This strict decode raises `UnicodeDecodeError`, aborting the checker even when the input has its required threat row. Handle binary canonical blobs without crashing so valid tasks can pass and uncovered inputs receive a C8 finding.

- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83
  On case-insensitive filesystems, an in-repository file symlink can resolve through a differently cased checkout root. `confined()` accepts that target via `samefile()`, but C12 subsequently passes it into `path_entry()`, where this case-sensitive `relative_to(root)` raises `ValueError`. Valid tasks consequently receive no verdict. Preserve identity-aware relativization and extend the closed case-alias fixture ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
  With an authorized `--premises-sha`, a `grep -c` premise expecting `0` passes C14 when its pattern matches nothing because this branch always returns status 0. Actual grep returns status 1 for no matches, contradicting the new requirement to reject unsuccessful probes even when stdout matches. Return a nonzero status for zero matches and add that negative control.
Read-only reproductions confirmed a baseline-search crash, a case-aliased path crash, and an incorrectly accepted failed probe. The full unit suite and CI were not rerun.

Full review comments:

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
  When C8 checks a new `*_EVIDENCE` name absent from Makefile and scripts, traversal reaches the existing encrypted `home/.key.txt.age`. This strict decode raises `UnicodeDecodeError`, aborting the checker even when the input has its required threat row. Handle binary canonical blobs without crashing so valid tasks can pass and uncovered inputs receive a C8 finding.

- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83
  On case-insensitive filesystems, an in-repository file symlink can resolve through a differently cased checkout root. `confined()` accepts that target via `samefile()`, but C12 subsequently passes it into `path_entry()`, where this case-sensitive `relative_to(root)` raises `ValueError`. Valid tasks consequently receive no verdict. Preserve identity-aware relativization and extend the closed case-alias fixture ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
  With an authorized `--premises-sha`, a `grep -c` premise expecting `0` passes C14 when its pattern matches nothing because this branch always returns status 0. Actual grep returns status 1 for no matches, contradicting the new requirement to reject unsuccessful probes even when stdout matches. Return a nonzero status for zero matches and add that negative control.
```
---
task: dotfiles-T133-task-generator-plan-check-a06-checker
head: 21f52c79336580d40b7c94bb4254ad2d28c2a791
pr: 440
base: 230b36767eec123f90dcd79edca76993d9bb9de7
started: 2026-10-20T12:28:33Z
finished: 2026-10-20T12:38:11Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350

```text
The new authenticated API dependency breaks the existing regime CI caller, and two coverage gaps allow incomplete threat tables to pass. Targeted read-only probes confirmed these issues; the full test suite was not run.

Full review comments:

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
  After this checker lands on main, `.github/workflows/regime.yml` invokes it through `regime-ci.py` without setting `GH_TOKEN` or `GITHUB_TOKEN`. Fresh runners have no GitHub CLI login, so tasks referencing a design or requiring C8/C9 lookups now fail: unauthenticated `gh api` exits 4, and regime-ci reports `no verdict`. Supply the workflow token alongside this change and cover that caller environment in a regression test.

- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350
  With both `scripts/` and `scripts/orchestrator/task-consistency-check.py` allowed, a table containing only the child file's row passes. This prefix check credits that row to the directory, while the new `hits()` logic correctly credits it only to the child; consequently, nothing requires a row controlling the rest of `scripts/`. Validate coverage against each entry's own row, preserving the one-row-per-entry requirement in [AGENTS.md:78](AGENTS.md#L78).

- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
  For an allowed `*.md` scope, adding a concrete row for `AGENTS.md` makes C12 pass even without a row for the existing `CLAUDE.md`. That file controls Claude's instruction import and recovery behavior, as established by [AGENTS.md:5–6](AGENTS.md#L5-L6), so it is not ordinary documentation. Scoped instruction files such as `vendor/compactiondb/AGENTS.md` are likewise missed. Include these instruction files in applied-file classification so wildcard scopes require concrete threat rows.
The new authenticated API dependency breaks the existing regime CI caller, and two coverage gaps allow incomplete threat tables to pass. Targeted read-only probes confirmed these issues; the full test suite was not run.

Full review comments:

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
  After this checker lands on main, `.github/workflows/regime.yml` invokes it through `regime-ci.py` without setting `GH_TOKEN` or `GITHUB_TOKEN`. Fresh runners have no GitHub CLI login, so tasks referencing a design or requiring C8/C9 lookups now fail: unauthenticated `gh api` exits 4, and regime-ci reports `no verdict`. Supply the workflow token alongside this change and cover that caller environment in a regression test.

- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350
  With both `scripts/` and `scripts/orchestrator/task-consistency-check.py` allowed, a table containing only the child file's row passes. This prefix check credits that row to the directory, while the new `hits()` logic correctly credits it only to the child; consequently, nothing requires a row controlling the rest of `scripts/`. Validate coverage against each entry's own row, preserving the one-row-per-entry requirement in [AGENTS.md:78](AGENTS.md#L78).

- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
  For an allowed `*.md` scope, adding a concrete row for `AGENTS.md` makes C12 pass even without a row for the existing `CLAUDE.md`. That file controls Claude's instruction import and recovery behavior, as established by [AGENTS.md:5–6](AGENTS.md#L5-L6), so it is not ordinary documentation. Scoped instruction files such as `vendor/compactiondb/AGENTS.md` are likewise missed. Include these instruction files in applied-file classification so wildcard scopes require concrete threat rows.
```
Two findings in head `2cb584823ccf5f22069ea925b252d8cefb020844`:

- **P2 · High confidence — `scripts/orchestrator/task-consistency-check.py:476`:** C12 classifies only the resolved target, allowing an unnamed applied symlink such as `scripts/run → tests/fixtures/payload.txt` through a wildcard scope without a concrete threat row, although invoking the link can execute its target.
- **P2 · High confidence — `scripts/orchestrator/task-consistency-check.py:251`:** The missing-literal shortcut returns before examining directory symlinks, so `scripts/link/new.py`, with `link` pointing elsewhere inside the repository, bypasses the claimed rejection of internal directory aliases.

Both reproduced with the checked-in functions and in-memory filesystem models, without writes. The first returned no findings for a `.txt` target; changing its target to an applied `.py` file correctly produced C12. The second returned no findings for a missing file beneath an internal directory alias. These gaps undermine the threat table’s path-identity/classification controls and its **closed** “internal directory aliases” row. Classification should consider both the enumerated applied path and its confined target; prefix validation must precede the missing-file shortcut.

The remaining controls revealed no additional findings: C14 uses digest authorization and fixed operations without shell execution; YAML uses safe loading; canonical reads bind repository, host and validated commit; credentials travel through child environments. Unicode/collision and C16 controls were inspected. Parent execution, shared caches and same-UID interference remain disclosed residual risks.

Source/test hashes and the task-copy hash match their evidence records. No files were changed.

Not rerun: full suites, native filesystem fixtures or live CI; GitHub connectivity failed. The two demonstrated path-validation bypasses remain unresolved.
Verdict: incorrect
 succeeded in 152ms:
---
format: 2
task_id: dotfiles-T133-task-generator-plan-check-a06-checker
kind: code
security: true
design: 5.14 items 2, 3, 8, 9
design_review:
  design: .orchestration/plans/024-design-quality.md
allowed_files:
  - scripts/orchestrator/task-consistency-check.py
  - tests/unit/test_task_consistency_c11_c15.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/**
after: []
reset_of: [dotfiles-T133-task-generator-plan-check-a05-checker]
retained_predecessor_directories:
  - .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/
expected_result_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report.md
expected_validation_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation.md
expected_sandbox_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/sandbox.md
expected_learning_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/learning.md
expected_autoskill_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/autoskill.md
expected_measure_file: .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/measure.md
threat_table:
  - {control: "scripts/orchestrator/task-consistency-check.py", disposition: "residual: Checker defenses start after parent execution; fixtures and final-head audit establish checker behavior, not protection against pre-start execution or concurrent same-UID replacement."}
  - {control: "tests/unit/test_task_consistency_c11_c15.py", disposition: "residual: Temporary repositories exercise the real checker; modeled filesystem semantics and fake API responses establish behavior rather than native platform coverage or live GitHub availability."}
  - {control: "tests/unit/test_task_checkers.py", disposition: "residual: Historical fixtures retain their coverage; changed expectations require an identified contract change and cannot conceal unrelated findings."}
  - {control: ".orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/**", disposition: "residual: Commit the byte-identical .orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md and required evidence before RESULT; artifacts contain no runtime helpers, credentials or approval authority."}
  - {control: "predecessor copy .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task.md", disposition: "residual: Retain this copy and its artifact directory unchanged from 06ffefbc; reset_of records lineage and permits retention, not edits or inherited approval of the new head."}
  - {control: "checker-side interpreter selection after startup", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_interpreter_resolution_order"}
  - {control: "gh child environment", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_gh_child_preserves_parent_tokens"}
  - {control: "canonical-main design read", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_uses_canonical_main_only"}
  - {control: "C6 canonical receipt binding and design hash", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
  - {control: "fixture and evidence symlink exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_symlink_to_applied_file_is_finding"}
  - {control: "fixture and evidence case-alias exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_case_alias_to_applied_file_is_finding"}
  - {control: "original Unicode path confinement", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_resolves_original_unicode_path"}
  - {control: "internal directory aliases", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_rejects_internal_directory_alias"}
  - {control: "directory pruning name comparison", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c12_prunes_with_normalised_directory_names"}
  - {control: "path_entry pipeline identity", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_canonical_path_pipeline_rejects_normalised_collisions"}
  - {control: "path grammar and filesystem identity", disposition: "residual: Each grammar case retains a behavioral fixture; normalized name comparisons never replace confinement of the original path or prevent concurrent same-UID races."}
  - {control: "C16 reference and item coverage", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c16_requires_reference_and_all_item_rows"}
  - {control: "C16 item occurrence counting", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_rejects_multi_item_rows"}
  - {control: "C16 resolved-target applicability", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_security_c16_uses_resolved_literal_alias"}
  - {control: "task metadata", disposition: "residual: The orchestrator verifies reset lineage, the retained-directory inventory, measured caps, canonical dispatch prerequisite and dispatched-copy identity before sending and accepting."}
  - {control: "metadata separators", disposition: "residual: The complete dispatched-file digest covers YAML separators and body; quoted commands and evidence are data rather than execution authority."}
  - {control: "in-process effects", disposition: "residual: C14 retains its fixed read-only vocabulary and dispatched-byte authorization; no shell, arbitrary Python operand or task-supplied executable is introduced."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: No caller or workflow edit is authorized; unchanged parent PATH and shared cache remain exposed. Checker compatibility proves no parent sanitization, and token values never enter evidence or argv."}
  - {control: "new or renamed scripts", disposition: "residual: Only the existing checker changes in production; add no resolver, wrapper, dependency, template or runtime code under artifacts."}
  - {control: "orchestrator effect dispatch.sh keeps calling the checker unchanged", disposition: "residual: The dispatch fixture proves checker compatibility only; dotfiles-T133-loop-limits-a01 owns dispatch.sh and dotfiles-T133-trusted-entrypoint-binding-a01 owns executable binding before checker startup."}
  - {control: "orchestrator effect merge", disposition: "residual: The worker never merges; the orchestrator follows Playbook step 10 and binds integration to the audited head."}
  - {control: "orchestrator effect update-branch", disposition: "residual: A changed head requires refreshed applicable CI, feedback and audit evidence; never reuse a preceding head's approval."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: No forced removal is assigned; preserve worker state, PR #440 and withdrawn lineage evidence."}
  - {control: "5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: Item 0 applies by reference; this slice establishes neither separate OS identities nor credential isolation."}
  - {control: "5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: Item 1 applies by reference; this task uses a Codex sandbox and makes no Claude deployment claim."}
  - {control: "5.14 item 2: 無害化した環境を最初に", disposition: "residual: Item 2 applies by reference; PATH-selected mise/uv execute first. dotfiles-T133-loop-limits-a01 owns dispatch.sh, dotfiles-T133-trusted-entrypoint-binding-a01 owns executable binding, and dotfiles-T133-ci-efficiency-followup-a04 owns the resolver and private UV_CACHE_DIR."}
  - {control: "5.14 item 3: 信頼パスの境界検査", disposition: "residual: Item 3 applies by reference; the canonical path pipeline does not establish host isolation or prevent same-UID replacement."}
  - {control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Item 4 applies by reference; retained consumed-byte and executable-binding checks cannot exclude concurrent same-UID interference."}
  - {control: "5.14 item 5: 出力と予約の同一性", disposition: "residual: Item 5 applies by reference; this read-only checker adds no reservation or integration resource."}
  - {control: "5.14 item 6: 正直な残余", disposition: "residual: Item 6 applies by reference; distinguish fixture observations, inherited evidence, compatibility warnings and unverified deployment."}
  - {control: "5.14 item 7: 検証", disposition: "residual: Item 7 applies by reference; retain negative controls and disclose unavailable platform coverage without claiming it passed."}
  - {control: "5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
  - {control: "5.14 item 9: 私設キャッシュ", disposition: "residual: Item 9 applies by reference; unchanged dispatch selects shared $HOME/.cache/uv, allowing pre-checker poisoning. dotfiles-T133-ci-efficiency-followup-a04 owns the resolver/private cache; dotfiles-T133-loop-limits-a01 and dotfiles-T133-trusted-entrypoint-binding-a01 own parent execution and binding."}
  - {control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Item 10 applies by reference; D-024-36 records this host's network-disabled Codex seats. Orchestrator transport grants the worker no sandbox escape."}
premises:
  - claim: The fixed measurement base resolves to this commit; local object identity supplies no canonical GitHub design authority.
    command: |-
      git rev-parse 60a6fb2b
    output: |-
      60a6fb2b324d0381c4a6e539b37c650105154a7e
  - claim: The inherited continuation head resolves to this commit; the pipeline draft is not part of this head.
    command: |-
      git rev-parse 06ffefbc
    output: |-
      06ffefbc633fe37bcef107385ea96810b2a9a0c5
---

# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a06-checker

🤖 I read the AGENTS.md for mryfmo/dotfiles.

.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/autoskill.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-evidence-integrity.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-batch-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/c3-compatibility-observation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-initial-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-initial-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/crit-status.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/crit-status.stderr
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/current-measure.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-copy-rows-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-copy-rows.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-grammar-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-grammar-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-all-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-artifact-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-artifact-privacy.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-closed-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-code-diff-check.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-code-diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-diff-check.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutation-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-privacy-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-production-r4.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-python-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-r4-lint.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-scope-integrity.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-source-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-static-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-task-table-validation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-tool-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/formatter-tool-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-source-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-base-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-candidate-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-diff-inventory.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-base.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-candidate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-suite-snapshot-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-base.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-candidate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-comparison-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-comparison.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review-repro.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-lint-adjustment-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-lint-adjustment-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/learning.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/legacy-c12-diagnostic.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/legacy-initial-diagnostic.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/lint-adjustment-blocked-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/lint-adjustment-blocker.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/mask-before-new-P2-hold.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/mask-current-evidence.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/measure.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-measure.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-stop.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-repair-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-repair-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-ci-r4-lint.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/post-repair-source-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/pre-green-source-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-r4-lint.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report-before-final-revision.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/required-selectors.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/reset-provenance.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/result-before-final-revision.txt
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-reproduction.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise.yaml
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-blocked-report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-measure.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-replan.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-result.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-closed-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-code-diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-current-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-artifact-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-artifact-privacy.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-format-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-suite-snapshot.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-candidate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-comparison.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical-red312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical-red315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-consolidation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mask2.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutation-preflight.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-observations.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-production-r4.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-python-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-fixture-consolidation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-suite-snapshot.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-unit-candidate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-unit-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-mutation-preflight.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-pre-red-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-production-r4.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-gate-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-reviewed-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-unreviewed-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/sandbox.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets-result.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-initial-preparation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-results.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task-initial-90ca0ae9.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/transport-merge-hold.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/transport-merge-verification.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation-before-final-revision.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-gate-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-evidence.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-receipt.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-reviewed-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-unreviewed-gate.log

exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-audit-c439b63.md.last.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-c439b63.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-21f52c7.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md' in ~/Workspace/dotfiles
 succeeded in 25ms:
Audited [PR #440](https://github.com/mryfmo/dotfiles/pull/440) at `c439b63c65285ec8180dc3e21394c87ef21115b4`. Final-head CI is green; all three Linux jobs executed Python tests. Source hashes, dispatched-copy identity, retained predecessor artifacts, and recorded test totals reconcile.

- [P1] high implementation `scripts/orchestrator/task-consistency-check.py:496` C15 accepts arbitrary `invariants` when `design_review.design` is omitted; a read-only reproduction returned no findings, bypassing canonical assignment and byte-equality validation.
- [P2] high implementation `scripts/orchestrator/task-consistency-check.py:312` The `grep -c` probe always returns status 0; an unmatched pattern produces actual grep status 1 but passes C14 with expected output `0`, violating the failed-probe requirement.
- [P2] high implementation `scripts/orchestrator/task-consistency-check.py:348` C4 accepts one `scripts/orchestrator/` row for both `scripts/` and `scripts/orchestrator/` scopes; reproduced with no findings despite the separate-row requirement. The previously recorded advisory remains.
- [P2] high implementation `scripts/orchestrator/task-consistency-check.py:476` C12 does not classify `CLAUDE.md` as applied instructions; `CLAUDE*` passes without a concrete row despite matching the existing instruction shim. The previously recorded advisory remains.
- [P2] high orchestration `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-pr-feedback.json:70` GitGuardian’s two specific detections are dismissed as “no finding”; the cited evidence merely selects that comment. Both can be specifically refuted—the synthetic-token digest and a Git commit ID—but that analysis is absent from the disposition.
- [P2] high orchestration `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md:416` The record documents a revise action without the required preceding `regime-counters.sh` output or substitute source readings; the complete record contains no such counter evidence, leaving INV-6 accounting unverified.
- [P2] high orchestration `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:212` The prescribed fixed-base measurement now totals **517 production / 1,505 test lines**, exceeding **450 / 720**; retained evidence reports **446 / 720**. Upstream merges explain the difference, but the final-head measurement contract and evidence were not reconciled.
- [P2] high orchestration `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md:416` R1 directs an unset-cache fallback, implemented at checker line 138, while frozen design 5.14 item 9 explicitly requires refusal when `UV_CACHE_DIR` is absent; the record provides no corresponding design exception or reconciled task amendment.
- [P2] high orchestration `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:243` The dispatched Checks block omits the required prerequisite API observations: PR #435 merged state, pinned main SHA, decoded design hash, commands and stage exits; task line 107 explicitly requires these before dispatch.

The task declares no `invariants` map; its only explicitly named invariant is INV-6.

INV-6: violated `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md:416` — required acceptance-time counter evidence is missing.

Orchestration findings: 5

📝 まとめ: 指定 head の監査を完了し、実装4件・オーケストレーション5件を報告しました。変更は行っていません。

Not rerun: full local suites or Bats; findings above remain unresolved.
Verdict: incorrect---
task: dotfiles-T133-task-generator-plan-check-a06-checker
head: c439b63c65285ec8180dc3e21394c87ef21115b4
pr: 440
base: e00de4e0e4158de19e2c8921e572461e7e9e4ca0
started: 2026-10-21T07:28:37Z
finished: 2026-10-21T07:40:21Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83

```text
Read-only reproductions confirmed a baseline-search crash, a case-aliased path crash, and an incorrectly accepted failed probe. The full unit suite and CI were not rerun.

Full review comments:

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
  When C8 checks a new `*_EVIDENCE` name absent from Makefile and scripts, traversal reaches the existing encrypted `home/.key.txt.age`. This strict decode raises `UnicodeDecodeError`, aborting the checker even when the input has its required threat row. Handle binary canonical blobs without crashing so valid tasks can pass and uncovered inputs receive a C8 finding.

- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83
  On case-insensitive filesystems, an in-repository file symlink can resolve through a differently cased checkout root. `confined()` accepts that target via `samefile()`, but C12 subsequently passes it into `path_entry()`, where this case-sensitive `relative_to(root)` raises `ValueError`. Valid tasks consequently receive no verdict. Preserve identity-aware relativization and extend the closed case-alias fixture ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
  With an authorized `--premises-sha`, a `grep -c` premise expecting `0` passes C14 when its pattern matches nothing because this branch always returns status 0. Actual grep returns status 1 for no matches, contradicting the new requirement to reject unsuccessful probes even when stdout matches. Return a nonzero status for zero matches and add that negative control.
Read-only reproductions confirmed a baseline-search crash, a case-aliased path crash, and an incorrectly accepted failed probe. The full unit suite and CI were not rerun.

Full review comments:

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
  When C8 checks a new `*_EVIDENCE` name absent from Makefile and scripts, traversal reaches the existing encrypted `home/.key.txt.age`. This strict decode raises `UnicodeDecodeError`, aborting the checker even when the input has its required threat row. Handle binary canonical blobs without crashing so valid tasks can pass and uncovered inputs receive a C8 finding.

- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83
  On case-insensitive filesystems, an in-repository file symlink can resolve through a differently cased checkout root. `confined()` accepts that target via `samefile()`, but C12 subsequently passes it into `path_entry()`, where this case-sensitive `relative_to(root)` raises `ValueError`. Valid tasks consequently receive no verdict. Preserve identity-aware relativization and extend the closed case-alias fixture ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
  With an authorized `--premises-sha`, a `grep -c` premise expecting `0` passes C14 when its pattern matches nothing because this branch always returns status 0. Actual grep returns status 1 for no matches, contradicting the new requirement to reject unsuccessful probes even when stdout matches. Return a nonzero status for zero matches and add that negative control.
```
---
task: dotfiles-T133-task-generator-plan-check-a06-checker
head: 21f52c79336580d40b7c94bb4254ad2d28c2a791
pr: 440
base: 230b36767eec123f90dcd79edca76993d9bb9de7
started: 2026-10-20T12:28:33Z
finished: 2026-10-20T12:38:11Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350

```text
The new authenticated API dependency breaks the existing regime CI caller, and two coverage gaps allow incomplete threat tables to pass. Targeted read-only probes confirmed these issues; the full test suite was not run.

Full review comments:

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
  After this checker lands on main, `.github/workflows/regime.yml` invokes it through `regime-ci.py` without setting `GH_TOKEN` or `GITHUB_TOKEN`. Fresh runners have no GitHub CLI login, so tasks referencing a design or requiring C8/C9 lookups now fail: unauthenticated `gh api` exits 4, and regime-ci reports `no verdict`. Supply the workflow token alongside this change and cover that caller environment in a regression test.

- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350
  With both `scripts/` and `scripts/orchestrator/task-consistency-check.py` allowed, a table containing only the child file's row passes. This prefix check credits that row to the directory, while the new `hits()` logic correctly credits it only to the child; consequently, nothing requires a row controlling the rest of `scripts/`. Validate coverage against each entry's own row, preserving the one-row-per-entry requirement in [AGENTS.md:78](AGENTS.md#L78).

- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
  For an allowed `*.md` scope, adding a concrete row for `AGENTS.md` makes C12 pass even without a row for the existing `CLAUDE.md`. That file controls Claude's instruction import and recovery behavior, as established by [AGENTS.md:5–6](AGENTS.md#L5-L6), so it is not ordinary documentation. Scoped instruction files such as `vendor/compactiondb/AGENTS.md` are likewise missed. Include these instruction files in applied-file classification so wildcard scopes require concrete threat rows.
The new authenticated API dependency breaks the existing regime CI caller, and two coverage gaps allow incomplete threat tables to pass. Targeted read-only probes confirmed these issues; the full test suite was not run.

Full review comments:

- [P1] Supply authentication for regime CI's new API calls — scripts/orchestrator/task-consistency-check.py:182-182
  After this checker lands on main, `.github/workflows/regime.yml` invokes it through `regime-ci.py` without setting `GH_TOKEN` or `GITHUB_TOKEN`. Fresh runners have no GitHub CLI login, so tasks referencing a design or requiring C8/C9 lookups now fail: unauthenticated `gh api` exits 4, and regime-ci reports `no verdict`. Supply the workflow token alongside this change and cover that caller environment in a regression test.

- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350
  With both `scripts/` and `scripts/orchestrator/task-consistency-check.py` allowed, a table containing only the child file's row passes. This prefix check credits that row to the directory, while the new `hits()` logic correctly credits it only to the child; consequently, nothing requires a row controlling the rest of `scripts/`. Validate coverage against each entry's own row, preserving the one-row-per-entry requirement in [AGENTS.md:78](AGENTS.md#L78).

- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480
  For an allowed `*.md` scope, adding a concrete row for `AGENTS.md` makes C12 pass even without a row for the existing `CLAUDE.md`. That file controls Claude's instruction import and recovery behavior, as established by [AGENTS.md:5–6](AGENTS.md#L5-L6), so it is not ordinary documentation. Scoped instruction files such as `vendor/compactiondb/AGENTS.md` are likewise missed. Include these instruction files in applied-file classification so wildcard scopes require concrete threat rows.
```
Two findings in head `2cb584823ccf5f22069ea925b252d8cefb020844`:

- **P2 · High confidence — `scripts/orchestrator/task-consistency-check.py:476`:** C12 classifies only the resolved target, allowing an unnamed applied symlink such as `scripts/run → tests/fixtures/payload.txt` through a wildcard scope without a concrete threat row, although invoking the link can execute its target.
- **P2 · High confidence — `scripts/orchestrator/task-consistency-check.py:251`:** The missing-literal shortcut returns before examining directory symlinks, so `scripts/link/new.py`, with `link` pointing elsewhere inside the repository, bypasses the claimed rejection of internal directory aliases.

Both reproduced with the checked-in functions and in-memory filesystem models, without writes. The first returned no findings for a `.txt` target; changing its target to an applied `.py` file correctly produced C12. The second returned no findings for a missing file beneath an internal directory alias. These gaps undermine the threat table’s path-identity/classification controls and its **closed** “internal directory aliases” row. Classification should consider both the enumerated applied path and its confined target; prefix validation must precede the missing-file shortcut.

The remaining controls revealed no additional findings: C14 uses digest authorization and fixed operations without shell execution; YAML uses safe loading; canonical reads bind repository, host and validated commit; credentials travel through child environments. Unicode/collision and C16 controls were inspected. Parent execution, shared caches and same-UID interference remain disclosed residual risks.

Source/test hashes and the task-copy hash match their evidence records. No files were changed.

Not rerun: full suites, native filesystem fixtures or live CI; GitHub connectivity failed. The two demonstrated path-validation bypasses remain unresolved.
Verdict: incorrect
**Reviewing inherited tests for shutil usage**
exec
/bin/zsh -lc "git show c439b63c:scripts/orchestrator/task-consistency-check.py | nl -ba | sed -n '1,240p'; git show c439b63c:tests/unit/test_task_consistency_c11_c15.py | rg -n '"'^    def |shutil|trusted|canonical|receipt|mock.patch'"'" in ~/Workspace/dotfiles
 succeeded in 50ms:
     1	"""Read-only cross-field check of a format-2 task file, before dispatch and at acceptance (plan 007 T704).
     2	
     3	`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>] <task.md>...`
     4	reads canonical GitHub design/baseline bytes (C6, C8 to C10) under --root (default: the first file's git
     5	toplevel), prints `<file name>: OK` or `: FAIL` with one `  C<n> ...` line per finding, and exits 1 when any file fails.
     6	C1 task_id equals the file name.
     7	C2 allowed_files covers .orchestration/<task_id>/** and names no other task's .orchestration/<id>/ directory.
     8	C3 when reset_of is non-empty, a threat_table row names every reset_of id's task.md and the task's own.
     9	C4 every allowed_files entry (its path before any glob) is named in a row's control, followed by its end, a space, / " ' ( ) , or a glob.
    10	C5 no residual binds a predecessor's hash ("names the <aNN> file's hash") instead of the task's own.
    11	C6 design_review.receipt is the design file's current design_review.receipt.
    12	C7 one row per non-path control name and per orchestrator effect name (the SKILL row unit).
    13	C7b no row other than a non-path control names two allowed_files entries (one row per entry).
    14	C8 (code tasks) every *_EVIDENCE input the body names and origin/main does not read yet has a threat row.
    15	C9 (docs tasks) a quoted rule sentence naming a script, *_EVIDENCE, a check id or classes: finds it on origin/main or says once/until.
    16	C10 (docs tasks) a quoted rule sentence naming a script on origin/main has no `=` or `[...]` literal absent from the script and its test.
    17	"""
    18	
    19	import argparse
    20	import base64
    21	import fnmatch
    22	import hashlib
    23	import json
    24	import os
    25	import pathlib
    26	import pwd
    27	import re
    28	import shlex
    29	import shutil
    30	import subprocess
    31	import sys
    32	import tempfile
    33	import unicodedata
    34	from functools import cache
    35	from urllib.parse import quote
    36	
    37	CACHE = os.environ.get("UV_CACHE_DIR")
    38	
    39	try:
    40	    import yaml
    41	except ImportError:
    42	    print("needs pyyaml: run with uv run --no-project --with pyyaml")
    43	    sys.exit(2)
    44	
    45	ROW_UNIT = "task metadata|metadata separators|in-process effects|workflow and interpreter or environment inputs|new or renamed scripts|orchestrator effect merge|orchestrator effect update-branch|orchestrator effect forced worker removal"
    46	C7_NAMES = ROW_UNIT.split("|")
    47	NONPATH = ("in-process effects", "task metadata", "metadata separators", "workflow and interpreter")
    48	NONPATH += ("new or renamed scripts", "orchestrator effect")
    49	C9_NAMES = r"(scripts/[\w./-]+|\b[A-Z][A-Z_]{3,}_EVIDENCE\b|task-consistency-check C\d|\bC\d\b of the task-consistency check|\bclasses:)"
    50	CHECKER = "scripts/orchestrator/task-consistency-check.py"  # where `task-consistency-check C<n>` lands
    51	TRUST_ROOT = pathlib.Path(__file__).resolve().parents[2]
    52	HOST_HOME = pathlib.Path(pwd.getpwuid(os.getuid()).pw_dir)
    53	FORMS = ("closed: ", "residual: ", "out-of-scope: ")
    54	APPLIED = (".sh", ".py", ".yaml", ".yml", ".json", ".toml")
    55	APPLIED_DIRS = ("home/", "scripts/", ".githooks/", ".github/")
    56	UNTRUSTED = "C14: not run (no trusted sha)"  # a warning: the file is not the text --premises-sha names (revise 1)
    57	
    58	
    59	def normalise_name(value):
    60	    if not isinstance(value, str):
    61	        return None
    62	    parts = value.split("/")
    63	    if not value or pathlib.PurePosixPath(value).is_absolute() or "\0" in value or ".." in parts or "\\" in value:
    64	        return None
    65	    name = "/".join(p for p in parts if p not in ("", "."))
    66	    if not name or name[0] in ":!":
    67	        return None
    68	    return unicodedata.normalize("NFC", name) + ("/" if value.endswith(("/", "/.")) else "")
    69	
    70	
    71	def confined(root, rel):
    72	    if not root.exists():
    73	        return None
    74	    path = (root / rel).resolve()
    75	    return next(
    76	        ((path, path.relative_to(p)) for p in (path, *path.parents) if p.exists() and os.path.samefile(p, root)), None
    77	    )
    78	
    79	
    80	def path_entry(root, value, fold=os.path.normcase):
    81	    raw = root / value if isinstance(value, pathlib.Path) or normalise_name(value) else None
    82	    found = confined(root, raw) if raw is not None else None
    83	    key = fold(unicodedata.normalize("NFC", raw.relative_to(root).as_posix())) if raw is not None else None
    84	    if key and str(value).endswith(("/", "/.")):
    85	        key += "/"
    86	    return raw, found[0] if found else None, key
    87	
    88	
    89	def front(text):
    90	    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))
    91	
    92	
    93	def trusted(path):
    94	    raw = pathlib.Path(path)
    95	    path = raw.resolve()
    96	    if not raw.is_absolute() or "shims" in raw.parts or "shims" in path.parts:
    97	        sys.exit("refused: absolute non-shim trusted path required")
    98	    manifest = TRUST_ROOT / "home/dot_agents/agent-config.yaml"
    99	    worker = (yaml.safe_load(manifest.read_text()) or {}).get("worker_worktree") if manifest.is_file() else None
   100	    if ".claude/worktrees" in os.path.normpath(path).casefold() or (
   101	        worker and confined(TRUST_ROOT / worker, path) is not None
   102	    ):
   103	        sys.exit("refused: worker-root trusted path")
   104	    if not path.is_file() or not os.access(path, os.X_OK):
   105	        sys.exit("refused: trusted executable must be an absolute regular executable file")
   106	    return path
   107	
   108	
   109	resolver = TRUST_ROOT / "scripts/orchestrator/trusted-interpreter.sh"
   110	if resolver.exists() or resolver.is_symlink():
   111	    command = ["/bin/bash", "--noprofile", "--norc", "-p", str(trusted(resolver))]
   112	    env = {"PATH": "/usr/bin:/bin", "HOME": str(HOST_HOME), "LANG": "C.UTF-8"}
   113	    result = subprocess.run(command, env=env, capture_output=True, text=True, check=False)
   114	    if result.returncode:
   115	        sys.exit("refused: interpreter resolver failed: " + result.stderr)
   116	    selected = result.stdout.strip()
   117	elif "TRUSTED_PYTHON" in os.environ:
   118	    selected = os.environ["TRUSTED_PYTHON"]
   119	else:
   120	    selected = os.path.realpath(sys.executable)
   121	    print("warning: interpreter fallback to real sys.executable", file=sys.stderr)
   122	PYTHON = trusted(selected)
   123	
   124	
   125	@cache
   126	def executable(name):
   127	    supplied = os.environ.get("TRUSTED_BIN_DIR")
   128	    path = pathlib.Path(supplied) / name if supplied is not None else shutil.which(name)
   129	    if not path or (supplied and (not os.path.isabs(supplied) or not path.is_symlink())):
   130	        sys.exit("refused: trusted executable binding missing: " + name)
   131	    return trusted(path)
   132	
   133	
   134	def launch(root, binary, *args):
   135	    binary = trusted(binary)
   136	    if confined(pathlib.Path(root).resolve(), binary) is not None:
   137	        sys.exit("refused: checkout executable binding")
   138	    if CACHE is not None:
   139	        if not os.path.isabs(CACHE):
   140	            sys.exit("refused: UV_CACHE_DIR must be an absolute path")
   141	        os.makedirs(CACHE, exist_ok=True)
   142	    with tempfile.TemporaryDirectory(dir=CACHE, prefix="checker-") as directory:
   143	        env = {"HOME": str(HOST_HOME), "PATH": directory, "LANG": "C.UTF-8", "UV_CACHE_DIR": CACHE or directory}
   144	        env.update(
   145	            v.split("=", 1)
   146	            for v in "GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 GIT_NO_REPLACE_OBJECTS=1".split()
   147	        )
   148	        if args and args[0] == "api":
   149	            env.update({k: os.environ[k] for k in ("GH_TOKEN", "GITHUB_TOKEN") if k in os.environ})
   150	        return subprocess.run(
   151	            [str(binary), *map(str, args)], cwd=root, env=env, capture_output=True, text=True, check=False
   152	        )
   153	
   154	
   155	def git(cwd, *args):
   156	    root = pathlib.Path(cwd).resolve()
   157	    if (root / ".gitmodules").exists() or (root / ".gitmodules").is_symlink():
   158	        sys.exit("refused: .gitmodules")
   159	    flags = ["-C", str(root), f"--git-dir={root / '.git'}", f"--work-tree={root}"]
   160	    for setting in "core.hooksPath=/dev/null core.fsmonitor=false submodule.recurse=false protocol.allow=never protocol.https.allow=always".split():
   161	        flags += ["-c", setting]
   162	    binary = executable("git")
   163	    config = launch(root, binary, *flags, "config", "--show-origin", "--get-regexp", r"^filter\.|^core\.worktree$")
   164	    if config.returncode not in (0, 1) or config.stdout:
   165	        sys.exit("refused: Git configuration: " + config.stdout + config.stderr)
   166	    top = launch(root, binary, *flags, "rev-parse", "--show-toplevel")
   167	    if top.returncode or not os.path.samefile(top.stdout.strip(), root):
   168	        sys.exit("refused: Git toplevel mismatch")
   169	    return launch(root, binary, *flags, *args)
   170	
   171	
   172	@cache
   173	def main_entry(root, name=None):
   174	    if name is None:
   175	        endpoint, args = "git/ref/heads/main", ("--jq", ".object.sha")
   176	    else:
   177	        if not normalise_name(name):
   178	            sys.exit("refused: canonical path")
   179	        name = pathlib.PurePosixPath(name).as_posix()
   180	        endpoint, args = f"contents/{quote(name.rstrip('/'), safe='/')}?ref={main_entry(root)}", ()
   181	    endpoint = "repos/mryfmo/dotfiles/" + endpoint
   182	    result = launch(root, executable("gh"), "api", endpoint, "--hostname", "github.com", *args)
   183	    print("api-input-sha256 " + hashlib.sha256((result.stdout + result.stderr).encode()).hexdigest(), file=sys.stderr)
   184	    if name is None:
   185	        sha = result.stdout.removesuffix("\n")
   186	        if result.returncode or not re.fullmatch(r"[0-9a-f]{40}", sha):
   187	            sys.exit("refused: canonical main SHA unavailable")
   188	        print("canonical-main " + sha, file=sys.stderr)
   189	        return sha
   190	    if result.returncode:
   191	        if "HTTP 404" in result.stderr:
   192	            return None
   193	        sys.exit("refused: canonical contents unavailable")
   194	    try:
   195	        entry = json.loads(result.stdout)
   196	        if not isinstance(entry, (dict, list)):
   197	            raise ValueError()
   198	        return entry
   199	    except ValueError:
   200	        sys.exit("refused: invalid canonical contents response")
   201	
   202	
   203	@cache
   204	def main_bytes(root, name):
   205	    entry = main_entry(root, name)
   206	    if entry is None:
   207	        return None
   208	    try:
   209	        if not isinstance(entry, dict) or entry.get("encoding") != "base64":
   210	            raise ValueError()
   211	        return base64.b64decode("".join(entry["content"].split()), validate=True)
   212	    except (KeyError, AttributeError, TypeError, ValueError):
   213	        sys.exit("refused: invalid canonical file bytes")
   214	
   215	
   216	def main_texts(root, name):
   217	    entry = main_entry(root, name)
   218	    if isinstance(entry, list):
   219	        for child in entry:
   220	            path = child["path"]
   221	            if not normalise_name(path) or not normalise_name(path).startswith(normalise_name(name).rstrip("/") + "/"):
   222	                sys.exit("refused: canonical directory child")
   223	            yield from main_texts(root, path)
   224	    elif entry is not None:
   225	        yield main_bytes(root, name).decode()
   226	
   227	
   228	def main_contains(root, pattern, names, literal=False):
   229	    texts = (text for name in names for text in main_texts(root, name))
   230	    return any(pattern in text if literal else re.search(pattern, text, re.MULTILINE) for text in texts)
   231	
   232	
   233	def match(name, pattern, partial=False, fold=os.path.normcase):
   234	    names = fold(unicodedata.normalize("NFC", name)).split("/")
   235	    parts = fold(normalise_name(pattern) + ("**" if normalise_name(pattern).endswith("/") else "")).split("/")
   236	
   237	    @cache
   238	    def step(i, j):
   239	        if partial and j == len(names):
   240	            return True
6:import shutil
16:UV = str(Path(shutil.which("uv")).resolve())
17:GIT = shutil.which("git")
39:            shutil.copytree(seed, _CACHE.name, dirs_exist_ok=True, symlinks=True)
50:    def setUp(self):
54:        self.repo, self.trust = self.temp / "repo", self.temp / "trusted"
64:        self.canonical = {DESIGN: "---\ndesign_review:\n  receipt: r1\ninvariants:\n  INV-1: exact sentence\n---\n"}
95:        self.put(DESIGN, self.canonical[DESIGN])
100:    def git(self, *args):
105:    def put(self, name, text):
111:    def task(self, allowed=None, extra=(), body="", **updates):
121:    def check(self, digest=False, env=None, prefix=""):
122:        self.data.write_text(json.dumps(self.canonical))
133:    def finding(self, name, **kwargs):
139:    def test_private_cache_when_unset(self):
147:    def test_interpreter_resolution_order(self):
148:        resolver = self.script.with_name("trusted-interpreter.sh")
170:    def test_dispatch_env_i_invocation(self):
171:        self.data.write_text(json.dumps(self.canonical))
198:    def test_c14_rejects_failed_probe_with_matching_stdout(self):
206:    def test_gh_child_preserves_parent_tokens(self):
226:    def test_c15_uses_canonical_main_only(self):
227:        self.canonical.pop(DESIGN)
229:        self.canonical[DESIGN] = "---\ninvariants: {}\n---\n"
246:        self.canonical[".orchestration/learning/mistakes/cafe\u0301.md"] = "classes: fixture\n"
250:    def test_path_grammar_distinguishes_globs_from_git_pathspecs(self):
266:    def test_c6_receipt_uses_canonical_design_bytes(self):
268:        dr = dict(design=DESIGN, receipt="r1", design_sha256=hashlib.sha256(local.encode()).hexdigest())
270:        self.canonical.pop(DESIGN)
272:        self.canonical[DESIGN] = local + "canonical-only bytes\n"
274:        dr["design_sha256"] = hashlib.sha256(self.canonical[DESIGN].encode()).hexdigest()
283:        self.task(design_review={k: v for k, v in dr.items() if k != "receipt"})
285:        self.task(design_review={**dr, "receipt": "forged"})
295:        self.canonical[".orchestration/plans/caf\u00e9.md"] = local
296:        self.canonical[raw] = other
300:        self.canonical.pop(raw)
302:        self.canonical[raw] = other
303:        dr.update(receipt="nfd", design_sha256=hashlib.sha256(other.encode()).hexdigest())
307:    def test_path_grammar_covers_root_files(self):
317:    def test_path_grammar_separates_directory_and_child_rows(self):
328:    def test_path_grammar_normalises_dot_spellings(self):
336:    def test_path_grammar_rejects_escaping_scopes(self):
349:    def test_exempt_symlink_to_applied_file_is_finding(self):
356:    def test_security_c12_prunes_with_normalised_directory_names(self):
375:    def test_security_c16_uses_resolved_literal_alias(self):
386:    def test_canonical_path_pipeline_rejects_normalised_collisions(self):
418:    def test_c10_confines_original_unicode_script_paths(self):
430:    def test_canonical_path_pipeline_preserves_identity(self):
438:        self.canonical[raw[0]] = self.canonical[DESIGN]
447:            design_review=dict(design=raw[0], receipt="r1"),
459:    def test_security_c12_resolves_original_unicode_path(self):
474:    def test_security_c12_rejects_internal_directory_alias(self):
488:    def test_security_c16_rejects_multi_item_rows(self):
500:    def test_exempt_case_alias_to_applied_file_is_finding(self):
511:    def test_c12_classifies_backslash_filenames_from_resolved_ancestry(self):
520:    def test_c12_covers_applied_skill_instructions(self):
525:    def test_c16_requires_reference_and_all_item_rows(self):
551:    def test_reset_scope_rejects_hidden_predecessor_artifacts(self):
561:    def test_retained_c11_c13_and_fixed_probe_controls(self):
583:        self.assertIn("C14: not run (no trusted sha)", out)
588:    def test_checker_rejects_untrusted_bindings_and_git_configuration(self):
621:    def test_isolated_child_and_same_bytes_survive_hostile_startup_inputs(self):
647:        self.assertNotIn("C14: not run (no trusted sha)", out)

**Analyzing design versus implementation issues**
exec
/bin/zsh -lc "git show c439b63c:tests/unit/test_task_consistency_c11_c15.py | sed -n '1,305p'; git show c439b63c:tests/unit/test_task_consistency_c11_c15.py | sed -n '588,665p'; rg -n 'task-consistency|UV_CACHE|mise|env -i|GIT_' scripts/orchestrator/dispatch.sh" in ~/Workspace/dotfiles
 succeeded in 76ms:
"""Exercise the real checker in temporary repositories; API fixtures provide no live authority."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/orchestrator/task-consistency-check.py"
PYTHON = str(Path(sys.executable).resolve())
UV = str(Path(shutil.which("uv")).resolve())
GIT = shutil.which("git")
MAIN = "a" * 40
DESIGN = ".orchestration/plans/design.md"
NAMES = "task metadata|metadata separators|in-process effects|workflow and interpreter or environment inputs|new or renamed scripts|orchestrator effect merge|orchestrator effect update-branch|orchestrator effect forced worker removal".split(
    "|"
)
RESIDUAL = "residual: fixture data and checked boundaries"
REFERENCE = "Design 5.14 applies by reference."
_CACHE = None


def uv(offline=True):
    args = [UV, "run", "--no-config", "--no-project", "--offline"][: 4 + offline]
    return [*args, "--python", PYTHON, "--with", "pyyaml", "python", "-I"]


def fixture_cache():
    global _CACHE
    if _CACHE is None:
        _CACHE = tempfile.TemporaryDirectory(prefix="checker-deps-")
        seed = os.environ.get("UV_CACHE_DIR", "")
        if os.path.isabs(seed) and Path(seed).is_dir():
            shutil.copytree(seed, _CACHE.name, dirs_exist_ok=True, symlinks=True)
        command = [*uv(bool(seed)), "-c", "import yaml"]
        env = {**os.environ, "UV_CACHE_DIR": _CACHE.name, "PATH": os.defpath}
        result = subprocess.run(command, env=env, capture_output=True, text=True, check=False)
        print("fixture-seed", PYTHON, UV, result.returncode, result.stdout, result.stderr, flush=True)
        if result.returncode:
            raise RuntimeError("PyYAML fixture provisioning failed; this is not a behavioral test result")
    return _CACHE.name


class TaskConsistencyC11C15Test(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="checker-case-")
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo, self.trust = self.temp / "repo", self.temp / "trusted"
        self.repo.mkdir()
        self.script = self.trust / "scripts/orchestrator/task-consistency-check.py"
        self.script.parent.mkdir(parents=True)
        self.script.write_bytes(CHECKER.read_bytes())
        self.bin = self.temp / "bin"
        self.bin.mkdir(mode=0o700)
        for name, source in (("git", GIT), ("uv", UV)):
            (self.bin / name).symlink_to(Path(source).resolve())
        self.data, self.calls = self.temp / "api.json", self.temp / "api-calls.jsonl"
        self.canonical = {DESIGN: "---\ndesign_review:\n  receipt: r1\ninvariants:\n  INV-1: exact sentence\n---\n"}
        gh = self.temp / "gh"
        gh.write_text(
            f"#!{PYTHON} -I\nimport sys,json,base64,os,hashlib\nfrom urllib.parse import unquote\n"
            f"data=json.load(open({str(self.data)!r}));a=sys.argv[1:]\n"
            f"with open({str(self.calls)!r},'a') as f: f.write(json.dumps(dict(argv=a,cache=os.environ.get('UV_CACHE_DIR'),tokens={{k:hashlib.sha256(os.environ[k].encode()).hexdigest() for k in ('GH_TOKEN','GITHUB_TOKEN') if k in os.environ}},host=os.environ.get('GH_HOST')))+'\\n')\n"
            "assert a[0]=='api';p=a[1];prefix='repos/mryfmo/dotfiles/'\n"
            f"if p==prefix+'git/ref/heads/main': print({MAIN!r})\n"
            "elif p.startswith(prefix+'contents/'):\n"
            " name=unquote(p[len(prefix+'contents/'):].split('?ref=')[0])\n"
            " if name in data: print(json.dumps(dict(encoding='base64',content=base64.b64encode(data[name].encode()).decode())))\n"
            " else:\n"
            "  children={key[len(name)+1:].split('/')[0] for key in data if key.startswith(name+'/')}\n"
            "  if children: print(json.dumps([dict(path=name+'/'+v) for v in sorted(children)]))\n"
            "  else: print('gh: Not Found (HTTP 404)',file=sys.stderr);sys.exit(1)\n"
            "else: sys.exit(71)\n"
        )
        gh.chmod(0o700)
        (self.bin / "gh").symlink_to(gh)
        self.env = {
            **os.environ,
            "PATH": str(self.bin),
            "UV_CACHE_DIR": fixture_cache(),
            "TRUSTED_PYTHON": PYTHON,
            "TRUSTED_BIN_DIR": str(self.bin),
            "GIT_CONFIG_GLOBAL": "/dev/null",
        }
        self.env.update(dict.fromkeys(("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"), "fixture"))
        self.env.update(dict.fromkeys(("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"), "fixture@example.test"))
        self.git("init", "-q", "-b", "main")
        self.put("scripts/tool.py", "print('tool')\n")
        self.put(DESIGN, self.canonical[DESIGN])
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.task()

    def git(self, *args):
        return subprocess.check_output(
            [GIT, "-c", "commit.gpgsign=false", *args], cwd=self.repo, env=self.env, text=True
        )

    def put(self, name, text):
        p = self.repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def task(self, allowed=None, extra=(), body="", **updates):
        allowed = [*(allowed or ["scripts/tool.py"]), ".orchestration/t-a01/**"]
        rows = [{"control": p, "disposition": RESIDUAL} for p in [*allowed, *NAMES]]
        fm = dict(format=2, task_id="t-a01", kind="code", design_review=dict(design=DESIGN))
        fm.update(allowed_files=allowed, threat_table=rows + list(extra))
        fm.update(updates)
        self.fm = fm
        self.path = self.put(".orchestration/tasks/t-a01.md", "---\n" + json.dumps(fm) + "\n---\n" + body)
        return self.path

    def check(self, digest=False, env=None, prefix=""):
        self.data.write_text(json.dumps(self.canonical))
        args = [str(self.script), "--root", str(self.repo), str(self.path)]
        if digest:
            args[1:1] = ["--premises-sha", hashlib.sha256(self.path.read_bytes()).hexdigest()]
        if prefix:
            prefix += "\nimport sys,runpy;sys.argv.pop(0);runpy.run_path(sys.argv[0],run_name='__main__')"
            args[:0] = ["-c", prefix]
        env = self.env if env is None else env
        result = subprocess.run([*uv(), *args], env=env, cwd=self.repo, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr

    def finding(self, name, **kwargs):
        rc, out = self.check(**kwargs)
        self.assertEqual(rc, 1, out)
        self.assertIn(name + " ", out)
        return out

    def test_private_cache_when_unset(self):
        rc, out = self.check(prefix="import os;os.environ.pop('UV_CACHE_DIR',None)")
        self.assertEqual(rc, 0, out)
        for call in map(json.loads, self.calls.read_text().splitlines()):
            cache = Path(call["cache"])
            self.assertTrue(cache.is_absolute() and not cache.exists())
        self.assertNotEqual(self.check(prefix="import os;os.environ['UV_CACHE_DIR']='relative'")[0], 0)

    def test_interpreter_resolution_order(self):
        resolver = self.script.with_name("trusted-interpreter.sh")
        marker = self.temp / "resolver-ran"
        resolver.write_text(f"#!/bin/bash -p\nprintf called > '{marker}'\nprintf '%s\\n' '{PYTHON}'\n")
        resolver.chmod(0o700)
        env = {**self.env, "TRUSTED_PYTHON": "invalid"}
        self.assertEqual(self.check(env=env)[0], 0)
        self.assertTrue(marker.exists())
        resolver.write_text("#!/bin/bash -p\nexit 19\n")
        self.assertNotEqual(self.check()[0], 0)
        for value in ("relative/python", str(self.repo)):
            resolver.write_text(f"#!/bin/bash -p\nprintf '%s\\n' '{value}'\n")
            self.assertNotEqual(self.check()[0], 0)
        resolver.unlink()
        self.assertEqual(self.check()[0], 0)
        for value in ("relative/python", str(self.temp / "absent"), str(self.repo)):
            self.assertNotEqual(self.check(env={**self.env, "TRUSTED_PYTHON": value})[0], 0)
        env = {k: v for k, v in self.env.items() if k != "TRUSTED_PYTHON"}
        rc, out = self.check(env=env)
        self.assertEqual(rc, 0, out)
        self.assertIn("sys.executable", out)
        self.assertIn("warning", out)

    def test_dispatch_env_i_invocation(self):
        self.data.write_text(json.dumps(self.canonical))
        env = {k: self.env[k] for k in ("PATH", "HOME", "UV_CACHE_DIR")}
        env.update(LANG="C.UTF-8", AGMSG_FIXTURE="retained")
        result = subprocess.run(
            [
                os.path.realpath("/usr/bin/env"),
                "-i",
                *(f"{k}={v}" for k, v in env.items()),
                *uv(),
                str(self.script),
                "--root",
                str(self.repo),
                str(self.path),
            ],
            cwd=self.repo,
            env={},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("t-a01.md: OK", result.stdout)
        self.assertNotIn("TRUSTED_PYTHON", env)
        self.assertNotIn("TRUSTED_BIN_DIR", env)
        for call in map(json.loads, self.calls.read_text().splitlines()):
            self.assertEqual(call["cache"], env["UV_CACHE_DIR"])

    def test_c14_rejects_failed_probe_with_matching_stdout(self):
        for command, output in (("test -e missing", ""), ("test -f scripts", ""), ("git rev-parse no-such-ref", "")):
            with self.subTest(command=command):
                self.task(premises=[dict(command=command, output=output)])
                self.finding("C14", digest=True)
        self.task(premises=[dict(command="test -f scripts/tool.py", output="")])
        self.assertEqual(self.check(digest=True)[0], 0)

    def test_gh_child_preserves_parent_tokens(self):
        trace = self.temp / "launch-boundary.jsonl"
        prefix = (
            "import subprocess,json;_run=subprocess.run\n"
            f"def run(args,**kw):\n with open({str(trace)!r},'a') as stream:stream.write(json.dumps(any(str(a).startswith(tuple(k+'=' for k in ('GH_TOKEN','GITHUB_TOKEN'))) for a in args))+'\\n')\n return _run(args,**kw)\n"
            "subprocess.run=run"
        )
        for names in ((), ("GH_TOKEN",), ("GITHUB_TOKEN",), ("GH_TOKEN", "GITHUB_TOKEN")):
            env = {k: v for k, v in self.env.items() if k not in ("GH_TOKEN", "GITHUB_TOKEN")}
            expected = {k: hashlib.sha256(("synthetic-" + k).encode()).hexdigest() for k in names}
            env.update({k: "synthetic-" + k for k in names})
            self.calls.unlink(missing_ok=True)
            trace.unlink(missing_ok=True)
            self.assertEqual(self.check(env=env, prefix=prefix)[0], 0)
            observed = [json.loads(line) for line in trace.read_text().splitlines()]
            self.assertTrue(observed)
            self.assertFalse(any(observed), "token values entered subprocess argv")
            for call in map(json.loads, self.calls.read_text().splitlines()):
                self.assertEqual(call["tokens"], expected)

    def test_c15_uses_canonical_main_only(self):
        self.canonical.pop(DESIGN)
        self.finding("C15")
        self.canonical[DESIGN] = "---\ninvariants: {}\n---\n"
        env = {
            **self.env,
            "GH_HOST": "attacker.invalid",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "url.https://attacker.invalid/.insteadOf",
            "GIT_CONFIG_VALUE_0": "https://github.com/",
        }
        self.calls.unlink()
        self.assertEqual(self.check(env=env)[0], 0)
        for call in map(json.loads, self.calls.read_text().splitlines()):
            argv = call["argv"]
            self.assertEqual(argv[argv.index("--hostname") + 1], "github.com")
            self.assertTrue(argv[1].startswith("repos/mryfmo/dotfiles/"))
            self.assertIsNone(call["host"])
            if "/contents/" in argv[1]:
                self.assertTrue(argv[1].endswith("?ref=" + MAIN))
        self.canonical[".orchestration/learning/mistakes/cafe\u0301.md"] = "classes: fixture\n"
        self.task(kind="docs", body='"classes: must be present."')
        self.assertEqual(self.check()[0], 0)

    def test_path_grammar_distinguishes_globs_from_git_pathspecs(self):
        for name in ("scripts/a.py", "scripts/nested/b.py", "scripts/x.txt"):
            self.put(name, "fixture\n")
        for pattern in ("scripts/*.py", "scripts/**/?.py", "scripts/[ab].py"):
            self.task(allowed=[pattern])
            out = self.finding("C12")
            if pattern == "scripts/*.py":
                self.assertNotIn("nested/b.py", out)
            if "**" in pattern:
                self.assertIn("nested/b.py", out)
                self.assertIn("scripts/a.py", out)
        invalid = r":(glob)scripts/** :(exclude)scripts/** :!scripts/** /scripts/** ./:!scripts/** scripts/\*.py"
        for pattern in invalid.split():
            self.task(allowed=[pattern])
            self.finding("C12")

    def test_c6_receipt_uses_canonical_design_bytes(self):
        local = (self.repo / DESIGN).read_text()
        dr = dict(design=DESIGN, receipt="r1", design_sha256=hashlib.sha256(local.encode()).hexdigest())
        self.task(design_review=dr)
        self.canonical.pop(DESIGN)
        self.finding("C6")
        self.canonical[DESIGN] = local + "canonical-only bytes\n"
        self.finding("C6")
        dr["design_sha256"] = hashlib.sha256(self.canonical[DESIGN].encode()).hexdigest()
        self.task(design_review=dr)
        self.calls.unlink()
        self.assertEqual(self.check()[0], 0)
        calls = [json.loads(line)["argv"][1] for line in self.calls.read_text().splitlines()]
        self.assertEqual(sum("/contents/" + DESIGN in name for name in calls), 1)
        for value in (None, "bad", "A" * 64, "0" * 64):
            self.task(design_review={**dr, "design_sha256": value})
            self.finding("C6")
        self.task(design_review={k: v for k, v in dr.items() if k != "receipt"})
        self.finding("C6")
        self.task(design_review={**dr, "receipt": "forged"})
        self.finding("C6")
        dr.pop("design_sha256")
        self.task(design_review=dr)
        rc, out = self.check()
        self.assertEqual(rc, 0, out)
        self.assertIn("warning", out)
        self.assertIn("design_sha256", out)
        raw = ".orchestration/plans/cafe\u0301.md"
        other = local.replace("r1", "nfd").replace("invariants:", "implementing_tasks:\n  t-a01: [INV-1]\ninvariants:")
        self.canonical[".orchestration/plans/caf\u00e9.md"] = local
        self.canonical[raw] = other
        dr.update(design=raw, design_sha256=hashlib.sha256(local.encode()).hexdigest())
        self.task(design_review=dr)
        self.assertIn("\n  C15 ", self.finding("C6"))
        self.canonical.pop(raw)
        self.assertIn("\n  C15 ", self.finding("C6"))
        self.canonical[raw] = other
        dr.update(receipt="nfd", design_sha256=hashlib.sha256(other.encode()).hexdigest())
        self.task(design_review=dr, invariants={"INV-1": "exact sentence"})
        self.assertEqual(self.check()[0], 0)
    def test_checker_rejects_untrusted_bindings_and_git_configuration(self):
        marker = self.temp / "ran"
        bad = self.put("git", f"#!/bin/sh\ntouch '{marker}'\n")
        bad.chmod(0o700)
        (self.bin / "git").unlink()
        (self.bin / "git").symlink_to(bad)
        rc, out = self.check()
        self.assertNotEqual(rc, 0, out)
        self.assertIn("checkout executable", out)
        self.assertFalse(marker.exists())
        (self.bin / "git").unlink()
        (self.bin / "git").symlink_to(Path(GIT).resolve())
        shim = self.temp / "shims/python"
        shim.parent.mkdir()
        shim.symlink_to(PYTHON)
        worker = self.put(self.temp / ".claude/worktrees/seat/python", "invalid")
        for path, named in ((shim, "shim"), (worker, "worker-root")):
            rc, out = self.check(env={**self.env, "TRUSTED_PYTHON": str(path)})
            self.assertNotEqual(rc, 0, out)
            self.assertIn(named, out)
        self.env.update(GIT_DIR=str(self.temp), GIT_WORK_TREE=str(self.temp), GIT_CONFIG_PARAMETERS="hostile")
        self.assertEqual(self.check()[0], 0)
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_PARAMETERS"):
            self.env.pop(key)
        self.git("config", "filter.fixture.clean", f"touch '{marker}'")
        rc, out = self.check()
        self.assertNotEqual(rc, 0, out)
        self.assertIn("Git configuration", out)
        self.assertFalse(marker.exists())
        self.git("config", "--unset", "filter.fixture.clean")
        self.put(".gitmodules", "[submodule]\n")
        self.assertIn(".gitmodules", self.check()[1])

    def test_isolated_child_and_same_bytes_survive_hostile_startup_inputs(self):
        marker = self.temp / "startup-ran"
        for name in (".venv/bin/python", "site/usercustomize.py", "site/sitecustomize.py", "site/evil.pth"):
            self.put(name, f"open({str(marker)!r},'w').close()\n")
        self.put("uv.toml", f'cache-dir = "{self.repo / "bad-cache"}"\n')
        env = {
            **self.env,
            "VIRTUAL_ENV": str(self.repo / ".venv"),
            "PYTHONPATH": str(self.repo / "site"),
            "PYTHONUSERBASE": str(self.repo / "site"),
        }
        self.assertEqual(self.check(env=env)[0], 0)
        self.assertFalse(marker.exists())
        self.assertFalse((self.repo / "bad-cache").exists())
        self.assertEqual(uv()[-2:], ["python", "-I"])
        for flag in ("--no-config", "--no-project", "--offline", "--python"):
            self.assertIn(flag, uv())
        self.assertEqual(uv()[uv().index("--python") + 1], PYTHON)
        self.task(premises=[dict(command="test -f scripts/tool.py", output="")])
        prefix = (
            "import pathlib;_read=pathlib.Path.read_bytes\n"
            f"def read(p):\n data=_read(p)\n if str(p)=={str(self.path)!r}:p.write_text('replaced after reading')\n return data\n"
            "pathlib.Path.read_bytes=read"
        )
        rc, out = self.check(digest=True, prefix=prefix)
        self.assertEqual(rc, 0, out)
        self.assertNotIn("C14: not run (no trusted sha)", out)
        self.assertEqual(self.path.read_text(), "replaced after reading")


if __name__ == "__main__":
    unittest.main()
37:#   An AGMSG-TASK line whose `task_file=` fails `task-consistency-check.py`
39:#   with `--no-config`, `--no-project` and a pinned `--python`, from the root, under `env -i` with only
40:#   `PATH`, `HOME` (the script owner's passwd home), `UV_CACHE_DIR` (under it), `LANG`, `LC_ALL` and the `AGMSG_*`
69:# @exitcode 1 A field check failed, the task file fails the task-consistency check, the record is malformed, or the sent line was not recorded.
99:# One allowlisted environment for git and uv: no inherited GIT_DIR, GIT_WORK_TREE or other GIT_*, VIRTUAL_ENV, UV_* or
113:clean=(env -i PATH="${PATH}" HOME="${home}" UV_CACHE_DIR="${home}/.cache/uv")
205:    # The interpreter is named, python3 as mise answers it under env -i at the root, else python3 on PATH, and uv
206:    # runs under env -i with an allowlist, so no VIRTUAL_ENV, CONDA_PREFIX, UV_* or PYTHON* variable reaches it
208:    py="$(cd -- "${root}" && { env -i PATH="${PATH}" HOME="${home}" mise which python3 2> /dev/null || command -v python3; })" || py=
238:        out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" "${tf}" 2>&1)" || {
239:            echo "dispatch: ${tf} fails the task-consistency check" >&2

**Assessing scope for tests**
exec
/bin/zsh -lc "wc -l -c .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md; sed -n '1,160p' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md" in ~/Workspace/dotfiles
 succeeded in 45ms:
     496   41822 .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md
     348   29576 .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
     844   71398 total
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a06-checker round=1 reset_of=dotfiles-T133-task-generator-plan-check-a05-checker repo=~/Workspace/dotfiles/.claude/worktrees/worker-g task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md task_sha256=90ca0ae9563df4b352dfb26c6b6aa60132386e15ce9ff50bcf998a43097a12e6 deadline=none done_signal=AGMSG-RESULT note=a012:reset-a06(D-024-39:measured-cap-440/700-for-the-canonical-path-pipeline-re-plan;your-uncommitted-draft-is-this-round's-content,plus-amendment-1's-identity-aware-matching-and-path-collision-refusal-with-the-two-file-regression;C-80-73ac933-correct;PR-440-continues-from-06ffefbc;add-the-a06-task-copy-and-records,keep-the-a05-copy;commit-locally-and-PONG-the-head-for-transport;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)"
  ],
  "format": 1,
  "head": "c439b63c65285ec8180dc3e21394c87ef21115b4",
  "ledger": [
    {
      "class": "excluded-command-trusts-sandbox-context",
      "id": "audit:1368f71:401"
    },
    {
      "class": "excluded-command-trusts-sandbox-context",
      "id": "audit:1368f71:402"
    },
    {
      "class": "sources",
      "id": "audit:1368f71:403"
    },
    {
      "class": "hash-binding",
      "id": "audit:1368f71:404"
    },
    {
      "class": "glob-matches-its-negation",
      "id": "audit:1368f71:405"
    },
    {
      "class": "glob-filter",
      "id": "audit:d0ad49f:201"
    },
    {
      "class": "unmasked-evidence",
      "id": "audit:24d7f55:201"
    },
    {
      "class": "evidence-integrity",
      "id": "audit:9da0ed3:1"
    },
    {
      "class": "threat-row-stale",
      "id": "audit:9da0ed3:2"
    },
    {
      "class": "replan-not-patch",
      "id": "audit:9da0ed3:3"
    },
    {
      "class": "dispatch-wiring",
      "id": "audit:9da0ed3:4"
    },
    {
      "class": "spec-gap",
      "id": "audit:9da0ed3:5"
    },
    {
      "class": "glob-classification",
      "id": "audit:9da0ed3:6"
    },
    {
      "class": "glob-intersection",
      "id": "audit:9da0ed3:7"
    },
    {
      "class": "substring-selection",
      "id": "audit:9da0ed3:8"
    },
    {
      "class": "glob-filter",
      "id": "audit:9da0ed3:9"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:10"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:11"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:12"
    },
    {
      "class": "parser-gap",
      "id": "audit:9da0ed3:13"
    },
    {
      "class": "regex-gap",
      "id": "audit:9da0ed3:14"
    },
    {
      "class": "records-form",
      "id": "audit:9da0ed3:15"
    },
    {
      "class": "spec-gap",
      "id": "audit:8a09b93:1"
    },
    {
      "class": "glob-classification",
      "id": "audit:8a09b93:2"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:3"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:4"
    },
    {
      "class": "glob-classification",
      "id": "audit:8a09b93:5"
    },
    {
      "class": "glob-filter",
      "id": "audit:8a09b93:6"
    },
    {
      "class": "parser-gap",
      "id": "audit:8a09b93:7"
    },
    {
      "class": "parser-gap",
      "id": "audit:8a09b93:8"
    },
    {
      "class": "test-coverage",
      "id": "audit:8a09b93:9"
    },
    {
      "class": "selector-grammar",
      "id": "audit:8a09b93:10"
    },
    {
      "class": "evidence-integrity",
      "id": "audit:8a09b93:11"
    },
    {
      "class": "records-form",
      "id": "audit:8a09b93:12"
    },
    {
      "class": "uv-caller-state-interpreter",
      "id": "audit:7a201ea:1"
    },
    {
      "class": "unlanded-mechanism-stated-as-present",
      "id": "audit:7a201ea:2"
    },
    {
      "class": "checker-exit-unchecked",
      "id": "audit:7a201ea:3"
    },
    {
      "class": "tool-environment",
      "id": "audit:7a201ea:4"

**Optimizing JSON parsing approach**
exec
/bin/zsh -lc "sed -n '161,415p' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md" in ~/Workspace/dotfiles
 succeeded in 24ms:
    },
    {
      "class": "happy-path-closing-test",
      "id": "audit:7a201ea:5"
    },
    {
      "class": "glob-classification",
      "id": "audit:7a201ea:6"
    },
    {
      "class": "glob-filter",
      "id": "audit:7a201ea:7"
    },
    {
      "class": "spec-without-input-grammar",
      "id": "audit:7a201ea:8"
    },
    {
      "class": "glob-filter",
      "id": "audit:7a201ea:9"
    },
    {
      "class": "input-validation",
      "id": "audit:7a201ea:10"
    },
    {
      "class": "input-validation",
      "id": "audit:7a201ea:11"
    },
    {
      "class": "happy-path-closing-test",
      "id": "audit:7a201ea:12"
    },
    {
      "class": "acceptance-dispositions",
      "id": "audit:7a201ea:13"
    },
    {
      "class": "replan-skipped",
      "id": "audit:7a201ea:14"
    },
    {
      "class": "evidence-dropped",
      "id": "audit:7a201ea:15"
    },
    {
      "class": "input-validation",
      "id": "audit:cedc7f5:301"
    },
    {
      "class": "input-validation",
      "id": "audit:cedc7f5:302"
    },
    {
      "class": "count-grammar",
      "id": "audit:cedc7f5:303"
    },
    {
      "class": "input-validation",
      "id": "audit:06ffefb:301"
    },
    {
      "class": "input-validation",
      "id": "audit:06ffefb:302"
    },
    {
      "class": "cap-without-room",
      "id": "audit:06ffefb:201"
    },
    {
      "class": "environment-contract",
      "id": "audit:b8bf806:101"
    },
    {
      "class": "platform-dependent-detection",
      "id": "audit:b8bf806:102"
    },
    {
      "class": "evidence-integrity",
      "id": "audit:b8bf806:201"
    },
    {
      "class": "approval-binding",
      "id": "audit:b8bf806:301"
    },
    {
      "class": "input-validation",
      "id": "audit:4a49ed9:401"
    },
    {
      "class": "input-validation",
      "id": "audit:5c09a95:201"
    },
    {
      "class": "input-validation",
      "id": "audit:5c09a95:202"
    },
    {
      "class": "cap-without-room",
      "id": "audit:5c09a95:203"
    },
    {
      "class": "input-validation",
      "id": "audit:1779440:201"
    },
    {
      "class": "caller-dependency",
      "id": "audit:21f52c7:501"
    }
  ],
  "pr": 440,
  "replans": {
    "evidence-integrity": {
      "design": "the worker's validation.md carries a `Base:`/`Candidate:` line pair and a named extra set, and the orchestrator runs `result-evidence-check.sh <task> <head40> <pr>` on every RESULT before reading its report (C-113)",
      "implementation": "`.agents/worklog/orchestrator-glue/result-evidence-check.sh` (written 09:56Z; promotion into scripts/orchestrator/ as a task after the pre-send-check pattern)",
      "specification": "a RESULT's claims are checked mechanically before the orchestrator judges them: the validation's full-suite comparison names every candidate-minus-base failure, and the head's CI has concluded green as read by the orchestrator",
      "verification": "the glue refuses b8bf8066 (`extra=6`, `0 test names`) and accepts the round-2 head only when its extra set is empty or named and its CI runs are all green."
    },
    "glob-classification": {
      "design": "classification is a pure function of the key and the declared rows, so a glob, its negation and a directory scope resolve through the same key table",
      "implementation": "the a06 round on PR #440 (task-consistency-check.py +443 lines at b8bf8066, round 2 pending)",
      "specification": "every path the checker classifies (an `allowed_files` entry, a threat-table control, an applied directory, a walked file) goes through one canonical pipeline, `normalise_name` then `path_entry`, and is classified by its one NFC-folded key, never by a substring or by the glob library's own semantics (a06 text item 1, D-024 reset of a05)",
      "verification": "`tests/unit/test_task_consistency_c11_c15.py` holds one red-then-green test per carried row class, read on the Linux CI jobs by the orchestrator, not on the worker's macOS alone."
    },
    "glob-filter": {
      "design": "one path normaliser shared by every check, tested on the grammar's cases",
      "implementation": "the a05-checker slice",
      "specification": "the checker's path semantics (git pathspec vs glob, root files, directory + child, `./` spellings, escaping scopes) are stated as one grammar in the text",
      "verification": "one fixture per grammar case, red at 7a201eab, plus the audit of the slice's head."
    },
    "input-validation": {
      "design": "a single function returns (enumerated, resolved, normalised-for-matching) for every file and directory, and C12, C16, the fixture exemption and the symlink rules consume that triple instead of normalising or resolving in place",
      "implementation": "worker fix round 2 on PR #440 (a012), source cap 400 unchanged",
      "specification": "every path the checker judges goes through one pipeline: the enumerated path is kept for reporting, its real target is resolved for confinement and applicability, and Unicode normalisation applies only to the comparison of names, never to the path that is confined or resolved",
      "verification": "one red-then-green test per finding plus one invariant test, the security-profile review of the new head, the task-level audit."
    },
    "parser-gap": {
      "design": "a parser refuses what it cannot parse (exit 1 with the line) instead of skipping it, so a gap surfaces as a finding, never as a silent pass",
      "implementation": "the a06 round on PR #440 (the same checker change)",
      "specification": "the front matter, the Check sentence's caps (backticked paths, the numstat command in its own sentence, C-107) and the metadata grammar are parsed by one parser each, with the grammar written once in the checker and quoted in the task text",
      "verification": "one fixture per former gap in `tests/unit/test_task_consistency_c11_c15.py`, red before the pipeline and green after, plus the regime-ci fixture grammar of #441 on main."
    },
    "text-defect": {
      "design": "the task template states the cap that way and the checker (this slice, C16 sibling) counts lines up to the Checks heading",
      "implementation": "this slice adds the rule to task-consistency-check.py (one more check, within the caps) or records it as the a06 owner row if the caps do not allow",
      "specification": "a text's line cap is the authored text, and the orchestrator's pasted Checks section is outside it",
      "verification": "a fixture with a long Checks section passes."
    }
  },
  "searches": [
    {
      "class": "evidence-integrity",
      "records": [
        "M-20261020-04-result-claims-against-own-counts.md"
      ]
    },
    {
      "class": "glob-classification",
      "records": []
    },
    {
      "class": "glob-filter",
      "records": []
    },
    {
      "class": "input-validation",
      "records": [
        "M-20261012-32.md"
      ]
    },
    {
      "class": "parser-gap",
      "records": [
        "M-20261019-04-parser-gap.md"
      ]
    }
  ],
  "task": "dotfiles-T133-task-generator-plan-check-a06-checker"
}
---

# Acceptance record: dotfiles-T133-task-generator-plan-check-a06-checker

- 2026-10-20T07:55Z: reset of dotfiles-T133-task-generator-plan-check-a05-checker (D-024-39: the canonical path pipeline re-plan needs a measured cap of 440 source lines; the a05 text's amendments and worker rounds are spent), text written whole by the review profile (`a06-checker-prompt.md`), 237 lines (self cap 260), Checks normalised; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 4a49ed9263e025e84f3ec5a51df553cfc83ab71192a4de016770e42a1f80491b before the Checks paste. C-80 round 1 running. Continues PR #440 from 06ffefbc with a012's uncommitted pipeline draft as the round's content. The a05 findings history is in the a05 record; its rows and re-plan lines are carried below (M-20261019-06).

## Lineage rows carried from dotfiles-T133-task-generator-plan-check-a05-checker

text-security:1368f71:1	excluded-command-trusts-sandbox-context
text-security:1368f71:2	excluded-command-trusts-sandbox-context
text-security:1368f71:3	sources
text-security:1368f71:4	hash-binding
text-security:1368f71:5	glob-matches-its-negation
text-security:cd37b74:0	correct
worker:d0ad49f:1	glob-filter
worker:24d7f55:1	unmasked-evidence
audit:9da0ed3:1	evidence-integrity
audit:9da0ed3:2	threat-row-stale
audit:9da0ed3:3	replan-not-patch
audit:9da0ed3:4	dispatch-wiring
audit:9da0ed3:5	spec-gap
audit:9da0ed3:6	glob-classification
audit:9da0ed3:7	glob-intersection
audit:9da0ed3:8	substring-selection
audit:9da0ed3:9	glob-filter
audit:9da0ed3:10	parser-gap
audit:9da0ed3:11	parser-gap
audit:9da0ed3:12	parser-gap
audit:9da0ed3:13	parser-gap
audit:9da0ed3:14	regex-gap
audit:9da0ed3:15	records-form
audit:8a09b93:1	spec-gap
audit:8a09b93:2	glob-classification
audit:8a09b93:3	glob-filter
audit:8a09b93:4	glob-filter
audit:8a09b93:5	glob-classification
audit:8a09b93:6	glob-filter
audit:8a09b93:7	parser-gap
audit:8a09b93:8	parser-gap
audit:8a09b93:9	test-coverage
audit:8a09b93:10	selector-grammar
audit:8a09b93:11	evidence-integrity
audit:8a09b93:12	records-form
audit:7a201ea:1	uv-caller-state-interpreter
audit:7a201ea:2	unlanded-mechanism-stated-as-present
audit:7a201ea:3	checker-exit-unchecked
audit:7a201ea:4	tool-environment
audit:7a201ea:5	happy-path-closing-test
audit:7a201ea:6	glob-classification
audit:7a201ea:7	glob-filter
audit:7a201ea:8	spec-without-input-grammar
audit:7a201ea:9	glob-filter
audit:7a201ea:10	input-validation
audit:7a201ea:11	input-validation
audit:7a201ea:12	happy-path-closing-test
audit:7a201ea:13	acceptance-dispositions
audit:7a201ea:14	replan-skipped
audit:7a201ea:15	evidence-dropped
security:cedc7f5:1	input-validation
security:cedc7f5:2	input-validation
security:cedc7f5:3	count-grammar
security:06ffefb:1	input-validation
security:06ffefb:2	input-validation
worker:06ffefb:1	cap-without-room
re-plan: text-defect (amendments 1 and 2 of this text; the python-pin text had the same cap collision) — specification: a text's line cap is the authored text, and the orchestrator's pasted Checks section is outside it; design: the task template states the cap that way and the checker (this slice, C16 sibling) counts lines up to the Checks heading; implementation: this slice adds the rule to task-consistency-check.py (one more check, within the caps) or records it as the a06 owner row if the caps do not allow; verification: a fixture with a long Checks section passes.
re-plan: glob-filter (rows audit:9da0ed3:9, audit:8a09b93:3-4, audit:8a09b93:6, audit:7a201ea:7, audit:7a201ea:9 of the a04 lineage; worker:d0ad49f:1) — specification: an allowed_files pathspec is validated for magic (`:(…)`, leading `:`, escapes) after normalisation, never before, and a path whose directory prefix is a symlink outside the worktree is refused before the full-match filter; symlinked directories are never followed; design: validation order fixed as normalise -> magic check -> symlink-prefix confinement -> full-match filter (a012's proposal, no scope or cap change); implementation: a012's repair in the a05 draft with one regression fixture per defect (magic after normalisation; escaping symlink prefix); verification: a012's independent review, the task-level audit of the final head and the security review (security: true).
re-plan: glob-filter (rows across audit:fa71134, audit:7a201ea; classes glob-classification x3, glob-filter x4, parser-gap x6 in this lineage) — specification: the checker's path semantics (git pathspec vs glob, root files, directory + child, `./` spellings, escaping scopes) are stated as one grammar in the text; design: one path normaliser shared by every check, tested on the grammar's cases; implementation: the a05-checker slice; verification: one fixture per grammar case, red at 7a201eab, plus the audit of the slice's head.
re-plan: input-validation (rows security:cedc7f5:1-2, security:06ffefb:1-2) — specification: every path the checker judges goes through one pipeline: the enumerated path is kept for reporting, its real target is resolved for confinement and applicability, and Unicode normalisation applies only to the comparison of names, never to the path that is confined or resolved; design: a single function returns (enumerated, resolved, normalised-for-matching) for every file and directory, and C12, C16, the fixture exemption and the symlink rules consume that triple instead of normalising or resolving in place; implementation: worker fix round 2 on PR #440 (a012), source cap 400 unchanged; verification: one red-then-green test per finding plus one invariant test, the security-profile review of the new head, the task-level audit.
re-plan: glob-classification (rows audit:9da0ed3:6, audit:8a09b93 and audit:7a201ea of the a04/a05 lineage, carried; four rows) — specification: every path the checker classifies (an `allowed_files` entry, a threat-table control, an applied directory, a walked file) goes through one canonical pipeline, `normalise_name` then `path_entry`, and is classified by its one NFC-folded key, never by a substring or by the glob library's own semantics (a06 text item 1, D-024 reset of a05); design: classification is a pure function of the key and the declared rows, so a glob, its negation and a directory scope resolve through the same key table; implementation: the a06 round on PR #440 (task-consistency-check.py +443 lines at b8bf8066, round 2 pending); verification: `tests/unit/test_task_consistency_c11_c15.py` holds one red-then-green test per carried row class, read on the Linux CI jobs by the orchestrator, not on the worker's macOS alone.
re-plan: parser-gap (rows audit:9da0ed3:10-13 and the a05 carried rows; six rows) — specification: the front matter, the Check sentence's caps (backticked paths, the numstat command in its own sentence, C-107) and the metadata grammar are parsed by one parser each, with the grammar written once in the checker and quoted in the task text; design: a parser refuses what it cannot parse (exit 1 with the line) instead of skipping it, so a gap surfaces as a finding, never as a silent pass; implementation: the a06 round on PR #440 (the same checker change); verification: one fixture per former gap in `tests/unit/test_task_consistency_c11_c15.py`, red before the pipeline and green after, plus the regime-ci fixture grammar of #441 on main.
re-plan: evidence-integrity (rows audit:9da0ed3:1, audit:7a201ea:15 (`evidence-dropped`, same cause) and worker:b8bf806:1; three rows of the lineage) — specification: a RESULT's claims are checked mechanically before the orchestrator judges them: the validation's full-suite comparison names every candidate-minus-base failure, and the head's CI has concluded green as read by the orchestrator; design: the worker's validation.md carries a `Base:`/`Candidate:` line pair and a named extra set, and the orchestrator runs `result-evidence-check.sh <task> <head40> <pr>` on every RESULT before reading its report (C-113); implementation: `.agents/worklog/orchestrator-glue/result-evidence-check.sh` (written 09:56Z; promotion into scripts/orchestrator/ as a task after the pre-send-check pattern); verification: the glue refuses b8bf8066 (`extra=6`, `0 test names`) and accepts the round-2 head only when its extra set is empty or named and its CI runs are all green.

## Rows of the a06 round (CI of b8bf8066 as read by the orchestrator; worker evidence)

ci:b8bf806:1	environment-contract
ci:b8bf806:2	platform-dependent-detection

exec
/bin/zsh -lc "sed -n '416,496p' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md" in ~/Workspace/dotfiles
 succeeded in 31ms:
worker:b8bf806:1	evidence-integrity
security:b8bf806:1	approval-binding
- 2026-10-20T08:01Z: C-80 round 1 (`…-text-security-4a49ed9.md`) `Verdict: incorrect`, one P2 (line 133): NFC-based row matching can credit one threat row to two distinct Linux files (`scripts/café.py` and `scripts/cafe<U+0301>.py`) under `scripts/**`; preserving original paths for filesystem operations does not bind the coverage decision to each file; require identity-aware row matching or collision rejection with a two-file regression before closing the pipeline-identity row. Amendment 1 by the review profile; budget 2 of 3 next.
text-security:4a49ed9:1	input-validation
- 2026-10-20T08:05Z: amendment 1 written whole by the review profile (`a06-checker-r2-prompt.md`) and installed: identity-aware matching through the pipeline triple, a named `path collision` refusal when two distinct files normalise to one key, the two-file regression as the pipeline-identity row's selector; Checks normalised; sha256 4a49ed92… -> 73ac9333b6afcdd437ca1d6cc75ca252517c9a13c5c5bad5938b77eab1caf254. C-80 round 2 next (budget 2 of 3).
- 2026-10-20T08:09Z: C-80 round 2 (`…-text-security-73ac933.md`) `Verdict: correct`; Checks pasted; final sha256 90ca0ae9563df4b352dfb26c6b6aa60132386e15ce9ff50bcf998a43097a12e6; AGMSG-TASK round 1 (reset_of a05-checker) dispatched to a012 (worker-g, wJ:p9) via dispatch.sh (`a06-checker-dispatch.txt`); read_at filled by fill-dispatch.py. The text (final bytes) joins the next records PR so regime-ci verifies the a06 copy.
text-security:73ac933:0	correct
- 2026-10-20T08:11Z: records PR #443 (`records/sync-dispatched-texts-27`, head 40b61c66) carries this text at its dispatched bytes (90ca0ae9…) and the pre-send-check text (ebe84d21…); merged by the orchestrator under D-024-40 once CI is green, so regime-ci verifies the a06 copy on #440.
- 2026-10-20T08:21:55Z: records PR #443 merged by the orchestrator (D-024-40, `--match-head-commit 40b61c66`) -> main 1f97c525; the a06 text is on main.
- 2026-10-20T08:12:36Z: a012 PONG `alive`: a06 TASK read and started; the a06 copy (90ca0ae9…) added; the a05 artifacts restored byte-identical to 06ffefbc; the held draft is this round's content.
- 2026-10-20T08:28:13Z/08:30:55Z: a012 PONGs `blocked`: its independent review of the pipeline draft (source 438/440, tests 698/700; hashes 5c09a95a…/2979c99f…) found [P1] checker:440 a trailing-slash directory scope (`scripts/`) loses its directory intent in the comparison key, so descendants are excluded before confinement (a real escaping symlink passes under `scripts/` and fails under `scripts/**`); [P2] checker:387 the C10 extraction regex excludes combining marks, so a raw NFD path is not captured before the shared resolution (NFC passes, NFD escapes). Disposition (2026-10-20T08:32Z, PING `a06-checker-disposition-1.txt`): both are implementation defects of the prescribed pipeline, repaired within this round with one regression each (equivalent directory scopes on an escaping descendant; NFD/NFC C10 paths); caps retained; if the repair exceeds 440 source lines the orchestrator amends the cap with its attribution (text amendment, C-80, records PR under D-024-40) rather than resetting again.
worker:5c09a95:1	input-validation
worker:5c09a95:2	input-validation
- 2026-10-20T08:37:40Z: a012 PONG `blocked` (cap stop as instructed): with both regressions red first (`test_path_grammar_rejects_escaping_scopes` comparing `scripts/*.py`, `scripts/` and `scripts/**` on the escaping descendant; new `test_c10_confines_original_unicode_script_paths` with raw NFD and NFC paths), the repaired source measures 442 changed lines against 440 and tests 700/700. Disposition (2026-10-20T08:39Z): cap amendment 1 of the a06 text by the orchestrator with the attribution (source 450 = 396 at 06ffefbc + 24 pipeline + 22 for the two review repairs, headroom to the next ten; tests 720), C-80 round, records PR (D-024-40), amendment dispatch; no reset.
worker:5c09a95:3	cap-without-room
- 2026-10-20T08:42Z: cap amendment 1 (orchestrator edit of three sentences: 450/720 with the attribution 396 + 24 + 22 = 442): C-80 round 3 (`…-text-security-b9e04cb.md`) `Verdict: correct`; dispatched to a012 as task_sha256 b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af (previous 90ca0ae9563df4b3…; `a06-checker-amend1.txt`); the text joins records PR sync-28.
text-security:b9e04cb:0	correct
- 2026-10-20T08:49:12Z: a012 PONG `blocked`: the two pipeline repairs are independently verified (source 98c0904f/1779440f; 27 new + 10 legacy methods green on 3.15 and 3.12), but its independent review found a P2 the R4 lint correction introduced (checker:476: the applied-directory classifier runs the metadata name normaliser on filesystem names, so an extensionless backslash filename under scripts/** loses its applied prefix and escapes C12); source 444/450, tests 700/720; the amended task copy (b9e04cb9…) in place. Disposition (2026-10-20T08:50Z, PING `a06-checker-disposition-2.txt`): repair within this round as proposed (applied-directory ancestry from the resolved comparison key's PurePosixPath parents, no metadata grammar), one real-CLI regression, lint again, then independent review, gate, commit, PONG the head.
worker:1779440:1	input-validation
- 2026-10-20T09:15:34Z/09:20:18Z: a012 PONGs `working`: full make measured (base 1267 tests 150 fail 128 err; candidate 1295 tests 156 fail 128 err, the only six added failures the RegimeCiTest subcases owned by #441, now merged); clean selected-tree `make validate-agent-assets` exit 0; frozen source 42183ecc / tests 55c31abd; a C3 observation shown pre-existing (byte-identical at 60a6fb2b); all local proofs and the worker gate complete; commit and PONG of the head expected next.
- 2026-10-20T09:23:57Z: a012 PONG `working`: the a06 round committed locally as head b45caa2b (3 code files + 161 retained a05 + 192 a06 artifacts; the a05 copy byte-identical to 06ffefbc), post-commit verified, awaiting transport. Transport at 2026-10-20T09:34Z failed as a non-fast-forward: the remote head is 762a2541, the orchestrator's `gh pr update-branch` merge of 08:38Z (main b8213131 into 06ffefbc); PING `a06-checker-merge-remote.txt` asks a012 to merge it locally (the same step a013 took on #437) and PONG the new head. Correction C-111: no update-branch of a Codex-seat PR while its worker is mid-round; update-branch only when the chain starts.
- 2026-10-20T09:36:35Z: a012 PONG `blocked`: the local merge of 762a2541 done (head b8bf8066, parents b45caa2b and 762a2541); it asks how the canonical copy and the base's 440 cap resolve. Transported by the orchestrator at 2026-10-20T09:38Z (fast-forward); disposition (PING `a06-checker-transport-done.txt`): the copy stays at the dispatched amended bytes b9e04cb9; regime stays red until records PR #444 (the amended text) merges first; RESULT after the orchestrator reads CI.
- 2026-10-20T09:37Z: head b8bf8066 transported to PR #440 by the orchestrator over HTTPS (D-024-36, `${h}:refs/heads/<branch>`); PING to a012: the a06 copy stays at the dispatched amended bytes b9e04cb9, regime-ci stays red until records PR #444 merges, RESULT after CI as read by the orchestrator.
- 2026-10-20T09:44:40Z: records PR #444 merged by the orchestrator (D-024-40: the copy on its head 661783cc hashes to b9e04cb9… = AGMSG-TASK 2805; sweep `records-sync-28-pr-feedback.json` 5 items, no threads, Codex code and security reviews finding-free; `--match-head-commit 661783cc`) -> main 230b3676. #440's regime run 39402133772 re-run: regime.yml checks out the base tip at run time, so no update-branch is needed for the regime; the ruleset's up-to-date rule still needs one, taken after a012's RESULT (C-111).
- 2026-10-20T09:42:16Z: a012 RESULT round 1 `status=ready_for_review` for head b8bf8066 (task_copy b9e04cb9… = the dispatched amended bytes; branch tools/task-generator-plan-check-a05-checker), sent before the head's Unit-test run ended (09:45Z) although the transport PING asked for the RESULT after CI as read by the orchestrator.
- 2026-10-20T09:45Z-09:50Z: CI of b8bf8066 as read by the orchestrator (Unit-test run 39402138504): `FAILED (failures=7)` of 1296 tests on all three Linux jobs (ubuntu-24.04 client and server, ubuntu-26.04 client); macos-14 client success is no evidence (unit tests are skipped for a Python-only diff). Six failures are `tests/unit/test_regime_ci.py` RegimeCiTest cases reading `checker: no verdict (exit 1): refused: UV_CACHE_DIR must be set to an absolute path`; the seventh is the new `test_canonical_path_pipeline_rejects_normalised_collisions` (`0 != 1 : t-a01.md: OK` inside `finding("C12", prefix=…)`). Snippet install, Agent assets and regime (re-run after #444) are green.
- 2026-10-20T09:51Z: diagnosis from the diff (3 code files: task-consistency-check.py +443, test_task_checkers.py, test_task_consistency_c11_c15.py +655): (R1) `scripts/orchestrator/task-consistency-check.py:37-39` exits at import when `UV_CACHE_DIR` is unset or relative, so every caller that sets none (regime-ci.py's checker launch on main, the regime workflow after a merge, the pre-send glue) gets no verdict; the text's line 117 (`retain … the absolute-cache requirement`) was implemented as a caller obligation while line 47 authorizes no caller edit (C-112). (R2) `confined()` lines 73-79 and `path_entry()` lines 83-89 compute the C12 key only after an `exists()`/`samefile()` probe of the real filesystem, normalisation-insensitive on APFS only, so on Linux the non-existent spelling is dropped before the comparison at line 449. (R3) `validation.md:36` reports base 150 vs candidate 156 failures and calls every failure inherited; the six extra are R1.
- 2026-10-20T09:53:51Z: ACCEPTANCE `status=revise round=1 previous_head=b8bf8066` (2827, `440-revise-1.txt`, read 09:53:57Z): R1 proper state = no import-time refusal, `launch()` uses a set absolute `UV_CACHE_DIR` or a private absolute temporary cache (design 5.14 item 9), one red-then-green test; R2 proper state = C12 compares NFC-folded keys of walked entries and declared rows without probing the alternate spelling; R3 = round 2 names the candidate-minus-base failure set; protocol while the Codex seat has no network: local commit, PONG `working head=<sha40>`, orchestrator transport and `ci=green|red:<names>` PING, RESULT only after `ci=green`; a security-review addendum PING for b8bf8066 follows (review started 09:54Z) and the RESULT waits for it; round 2 is the last worker round.
- 2026-10-20T09:56Z: mechanism (M-20261020-04, C-113): `.agents/worklog/orchestrator-glue/result-evidence-check.sh <task> <head40> [<pr>]` refuses a RESULT whose validation.md shows more candidate failures+errors than the base without each extra test named, and a head whose CI runs are not all green; run on b8bf8066: `refuse: candidate adds 6 failure(s)/error(s) over the base; 0 test names appear` (rc 1).
- 2026-10-20T09:54Z-10:00Z: security review of b8bf8066 (`security-review.sh`, base b8213131; `…-security-b8bf806.md` + `.last.md`): `Verdict: incorrect`, one P1 (high confidence) at `task-consistency-check.py:355`: C6/C15 fetch the normalised comparison key (`path_entry()` turns `cafe\u0301.md` into `caf\u00e9.md`; `main_entry()` normalises at line 176) instead of the original design pathname, so a different canonical file can supply the approval and invariants (reproduced read-only with a modeled API; an ASCII negative control produced C6/C15); the threat rows at text lines 32, 33, 39 and 61 stay unproven. Row `security:b8bf806:1 approval-binding`.
- 2026-10-20T10:01Z: addendum PING (2829, `440-security-addendum-1.txt`) to a012: R4 = the P1 above, proper state original spelling for requests and reads, normalisation only for comparisons, one red-then-green test; round 2 is R1+R2+R3+R4; no further addendum; RESULT after the `ci=green` PING.
- 2026-10-20T12:09:47Z: a012 RESULT round 2 `status=ready_for_review` for head 2cb58482 (task_copy b9e04cb9…; validation: exact 278-vs-278 full-suite comparison, candidate-minus-base []; 48/48 mutants killed on 3.15 and 3.12; evidence precheck ok; CI all green as read by the orchestrator). ACCEPTANCE `status=pending-integration round=2` (2835) at 12:10:58Z.
- 2026-10-20T12:19Z-12:38Z: chain on 2cb58482 (CI green; sweep; sandbox-scan 0): local review (`…-local-review-21f52c7.md`) 1 P1 + 2 P2: [P1] task-consistency-check.py:182 the new `gh api` requests (canonical main, design bytes for C6/C15, C8/C9 lookups) run in regime CI through regime-ci.py's minimal environment without `GH_TOKEN`/`GITHUB_TOKEN`; a fresh runner has no gh login, so after this checker lands every task text that references a design gets `no verdict` in the regime check (main's checker makes no API call today; the regime run on 2cb58482 passed because it executed the base's checker); [P2] :476-480 Claude instruction shims are not classified as applied files; [P2] :348-350 overlapping directory scopes need a separate row. The two P2 are advisory rows under dotfiles-T133-task-generator-plan-check-followup-a01 (recorded by the chain). The P1 is a caller-side dependency, not a defect of the changeset: the fix is the regime workflow passing `GH_TOKEN: ${{ github.token }}` and regime-ci.py forwarding it into the checker's environment (the checker already forwards both tokens when present, line 149; `test_gh_child_preserves_parent_tokens`). Disposition as for PR #411's `--premises-sha` dependency: #440 waits for `dotfiles-T133-regime-ci-token-a01` (text authored now, Claude seat), then takes the new base, and its chain (audit, record, gate) runs on that head. Worker rounds stay spent; no third round.

local:21f52c7:1	caller-dependency
local-finding: 21f52c7:1 not-applicable:sequencing dependency on dotfiles-T133-regime-ci-token-a01 (the regime workflow and regime-ci.py supply the token to the checker; #440 merges after it lands and is update-branched); evidence=git show 2cb584823ccf5f22069ea925b252d8cefb020844:scripts/orchestrator/task-consistency-check.py | sed -n 149p


## Owned by dotfiles-T133-task-generator-plan-check-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:21f52c7:2	advisory-p2
local-finding: 21f52c7:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Classify Claude instruction shims as applied files — scripts/orchestrator/task-consistency-check.py:476-480); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (a792f57b99ca5c605c4188cd23464191dbba26cda750cf2d50ae193375c33b8a)
local:21f52c7:3	advisory-p2
local-finding: 21f52c7:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Require a separate row for overlapping directory scopes — scripts/orchestrator/task-consistency-check.py:348-350); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (a792f57b99ca5c605c4188cd23464191dbba26cda750cf2d50ae193375c33b8a)
local:21f52c7:4	advisory-p2
local-finding: 21f52c7:4 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (R08-F1 of dotfiles-T133-inv6-reset-anchors-review-a01: the a06 text omits the a05 predecessor obligation 'text-defect checker / long-Checks prevention' or an explicit owner disposition; the a05->a06 reset anchor is re-reviewed as one item after this row)

- 2026-10-20T15:00Z: reset-anchor review R08-F1 (a012, `dotfiles-T133-inv6-reset-anchors-review-a01`): the a06 text omits the a05 predecessor obligation 'text-defect checker / long-Checks prevention' or an explicit owner disposition. Disposition: owned by dotfiles-T133-task-generator-plan-check-followup-a01 (row `local:21f52c7:4 advisory-p2`); the a05->a06 reset anchor is re-reviewed as one item after this row.

local:c439b63:2	advisory-p2
local-finding: c439b63:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (a792f57b99ca5c605c4188cd23464191dbba26cda750cf2d50ae193375c33b8a)
local:c439b63:3	advisory-p2
local-finding: c439b63:3 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-followup-a01.md (a792f57b99ca5c605c4188cd23464191dbba26cda750cf2d50ae193375c33b8a)

- 2026-10-21T07:50Z: chain on c439b63c (update-branch of fefa1dcc after boundary 27; PR patch-id 3deeac540b9be86c unchanged since 2cb58482): CI 7 required green; local review `…-local-review-c439b63.md` 1 P1 + 2 P2 (the P2 rows above); the chain stopped at local-advisory (exit 11, plan 020 step 4.2: the PR's one round is over, the P1 goes to the operator). Manual continuation under the interim exemption: sweep 8/8 with `440-extra.tsv` (gaps 0), receipt and record block regenerated for c439b63. The P1 and the two P2 of the round-2 security review `…-security-2cb5848.md.last.md` (never dispositioned until now) are dispositioned below as advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01; D-024-57 records the judgement and its default; the audit and the security review of c439b63c follow through the operator's codex route.

local:c439b63:1	advisory-p2
local-finding: c439b63:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225: `main_texts` decodes every canonical blob strictly, so a C8 traversal that reaches home/.key.txt.age aborts with UnicodeDecodeError; the abort is fail-closed (non-zero exit, no false acceptance), so the orchestrator grades it P2 robustness, not P1); evidence=sed -n 225p scripts/orchestrator/task-consistency-check.py at c439b63c prints `yield main_bytes(root, name).decode()` and the reviewer's read-only reproduction is in the local review file
security:2cb5848:1	input-validation
security-finding: 2cb5848:1 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (task-consistency-check.py:476 C12 classifies only the resolved target, so an unnamed applied symlink to a non-applied target passes a wildcard scope without a concrete threat row; the checker is a pre-dispatch consistency check, the runtime boundary is the worker sandbox, and the orchestrator reads every threat table by hand until the owner task lands); evidence=.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md finding 1
security:2cb5848:2	input-validation
security-finding: 2cb5848:2 not-applicable:advisory P2 owned by dotfiles-T133-task-generator-plan-check-followup-a01 (task-consistency-check.py:251 the missing-literal shortcut returns before examining directory symlinks, so a missing file beneath an internal directory alias bypasses the internal-alias rejection; same compensating controls as row 1); evidence=.orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md finding 2

## Round 2 final head c439b63c: task-level audit 2026-10-21T08:07Z (operator-run `orch-audit.sh`, `…-audit-c439b63.md.last.md`)

**Verdict: incorrect**: one implementation P1, three implementation P2, five orchestration P2. Per D-024-57 an audit P1 resets the lineage: D-024-58, reset to `dotfiles-T133-task-generator-plan-check-a07-checker` by another context, no third round; a012 holds (ACCEPTANCE 2983). The security review of c439b63c is not run (no merge of this head).

audit:c439b63:1	invariants-validation
audit:c439b63:2	probe-status
audit:c439b63:3	scope-rows
audit:c439b63:4	instruction-shim-classification
audit:c439b63:5	sweep-disposition-wording
audit:c439b63:6	counters-evidence
audit:c439b63:7	cap-measurement
audit:c439b63:8	design-conflict
audit:c439b63:9	checks-omission

Row 1 (P1): task-consistency-check.py:496, C15 accepts arbitrary `invariants` when `design_review.design` is omitted, bypassing canonical assignment and byte-equality validation (a07 item). Row 2: :312 the `grep -c` probe always returns status 0 (same defect as local:c439b63:2; a07). Row 3: :348 C4 accepts one `scripts/orchestrator/` row for both `scripts/` and `scripts/orchestrator/` scopes (same class as local:21f52c7:3; a07). Row 4: :476 C12 does not classify `CLAUDE.md` as applied instructions (same class as local:21f52c7:2; a07). Row 5 (orchestration): the GitGuardian issue comment of #440 was dispositioned by the generic issue-comment template; the next sweep carries a specific row (the fixture digest and a commit id are refutable), as 442-extra.tsv already does for #442. Row 6 (orchestration): the revise at line 416 lacked a counters snapshot; snapshot taken 2026-10-21T08:07Z (C-126): a05-checker TASKs=3 revises=2 questions=2 blocked-PONGs=10 (S2, silenced by the a05 design-reset record); a06-checker TASKs=2 (the cap amendment resend) revises=1 RESULTs=2 questions=0 blocked-PONGs=6. Row 7 (orchestration): the auditor's 517/1505 was measured from a base other than the merge-base; the C-123 measurement is `git diff --numstat e00de4e0 c439b63c` = 446 outside tests/ (task-consistency-check.py 419+27) and 709 under tests/ (35+22, 652+0), within 450/720; not-applicable, evidence pasted here. Row 8 (orchestration, real): the R1 revise directed an unset-cache fallback (checker line 138) while frozen design 5.14 item 9 requires refusal when UV_CACHE_DIR is absent; a07 restores the refusal and the record names this conflict as the orchestrator's error. Row 9 (orchestration, real): the dispatched Checks block omitted the prerequisite API observations the text's line 107 requires; a07's Checks are complete before its anchor review.

audit-finding: c439b63:7 not-applicable:measured from the merge-base per C-123, 446/709 within 450/720; evidence=git diff --numstat e00de4e0e4158de19e2c8921e572461e7e9e4ca0 c439b63c65285ec8180dc3e21394c87ef21115b4


**Analyzing design constraints and test behavior**
**Reviewing missing control elements**
codex
The canonical-read tests verify API arguments and receipt comparisons using a fake `gh`; they don’t establish that the retained launch path selects a trusted `gh` executable. I also found that restoring mandatory `UV_CACHE_DIR` revives a caller failure documented in the acceptance record, so I’m checking whether the task provides a sequencing dependency for that repair.
exec
/bin/zsh -lc "rg -n 'UV_CACHE|subprocess|task-consistency' scripts/regime-ci.py scripts/orchestrator/regime-ci.py .github/workflows/regime.yml; sed -n '95,125p' scripts/orchestrator/dispatch.sh; sed -n '195,245p' scripts/orchestrator/dispatch.sh; git show c439b63c:.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report.md | head -100; git show c439b63c:.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation.md | head -115" in ~/Workspace/dotfiles
 succeeded in 95ms:
rg: scripts/regime-ci.py: No such file or directory (os error 2)
scripts/orchestrator/regime-ci.py:6:`task.md` copy at the head (of a reset_of lineage, only the latest copy) is checked: the base's task-consistency checker
scripts/orchestrator/regime-ci.py:21:import subprocess
scripts/orchestrator/regime-ci.py:32:CHECKER = "scripts/orchestrator/task-consistency-check.py"
scripts/orchestrator/regime-ci.py:44:    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
scripts/orchestrator/regime-ci.py:165:        run = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
[[ ${line} =~ ^AGMSG-(TASK|ACCEPTANCE|PING)[[:blank:]]+v1[[:blank:]] ]] || {
    echo "dispatch: not an AGMSG-TASK, AGMSG-ACCEPTANCE or AGMSG-PING v1 line" >&2
    exit 2
}
# One allowlisted environment for git and uv: no inherited GIT_DIR, GIT_WORK_TREE or other GIT_*, VIRTUAL_ENV, UV_* or
# PYTHON* variable chooses the root, the interpreter or the code they run (audit:ef74eae:1, C-57).
# HOME is the script owner's passwd home and the uv cache sits under it, never inherited values (4300738707).
owner="$(stat -c %U -- "${BASH_SOURCE[0]}" 2> /dev/null || stat -f %Su -- "${BASH_SOURCE[0]}")" || owner=
[[ ${owner} =~ ^[A-Za-z0-9._][A-Za-z0-9._-]*$ ]] || {
    echo "dispatch: cannot tell the owner of ${BASH_SOURCE[0]}" >&2
    exit 1
}
home=
eval "home=~${owner}" # the name is checked above; ~name is its passwd home
[[ ${home} == /* ]] || {
    echo "dispatch: no passwd home for ${owner}" >&2
    exit 1
}
clean=(env -i PATH="${PATH}" HOME="${home}" UV_CACHE_DIR="${home}/.cache/uv")
for v in LANG LC_ALL; do
    [[ -z ${!v:-} ]] || clean+=("${v}=${!v}")
done
while IFS= read -r v; do
    [[ ${v} != AGMSG_* ]] || clean+=("${v}=${!v}")
done < <(compgen -e)
root="$("${clean[@]}" git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"

read -ra tokens <<< "${line}"
for t in "${tokens[@]:2}"; do
    [[ ${t} == *=* ]] || {
        echo "dispatch: ${t} is not a <key>=<value> token" >&2
    got="$(shasum -a 256 "${path}")" && got=${got%% *}
    [[ ${got} == "${want}" ]] || {
        echo "dispatch: ${field} mismatch: the line has ${want}, ${path} hashes to ${got}" >&2
        exit 1
    }
done
if [[ ${tokens[0]} == AGMSG-TASK ]]; then
    tf="$(value_of task_file)" && [[ ${tf} == /* ]] || tf="${root}/${tf}"
    # Offline only: PyYAML comes from the pinned cache the validator recipes warm, and a cold cache stops the send,
    # never a fetch. --no-project: a pyproject.toml in the caller's directory is never discovered, synced or built.
    # The interpreter is named, python3 as mise answers it under env -i at the root, else python3 on PATH, and uv
    # runs under env -i with an allowlist, so no VIRTUAL_ENV, CONDA_PREFIX, UV_* or PYTHON* variable reaches it
    # (local:9df6b0c:1, C-57, the Bot's P1 4300102967).
    py="$(cd -- "${root}" && { env -i PATH="${PATH}" HOME="${home}" mise which python3 2> /dev/null || command -v python3; })" || py=
    [[ ${py} == /* ]] || {
        echo "dispatch: no python3 interpreter to pin for uv" >&2
        exit 1
    }
    uvy=(uv run --no-config --no-project --offline --python "${py}" --with pyyaml)
    here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
    # Run from the trusted root, so a caller's .python-version or virtual environment picks no interpreter (4299651928).
    uvr() { (cd -- "${root}" && "${clean[@]}" "${uvy[@]}" "$@"); }
    uvr python -I -c 'import yaml' > /dev/null 2>&1 || {
        echo "dispatch: PyYAML is not in the uv cache ${home}/.cache/uv; run make validate-agent-assets to warm it" >&2
        exit 2
    }
    read -r -d '' brief << 'PY' || true
import sys, yaml
def unique(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    if len(keys) != len(set(keys)):
        raise yaml.YAMLError("duplicate key")
    return loader.construct_mapping(node, deep)
class Loader(yaml.SafeLoader):
    pass
Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique)
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
end = lines.index("---", 1) if lines[0] == "---" else None
front = yaml.load("\n".join(lines[1:end]), Loader) if end else None
sys.exit(0 if isinstance(front, dict) and front.get("kind") == "review" else 1)
PY
    # Fail-closed: only a parsed front matter whose kind is review skips the checker.
    if ! uvr python -I -c "${brief}" "${tf}" > /dev/null 2>&1; then
        out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" "${tf}" 2>&1)" || {
            echo "dispatch: ${tf} fails the task-consistency check" >&2
            printf '%s\n' "${out}" >&2
            exit 1
        }
    fi
fi
[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}"
# Final worker round2

Status: R1/R2/R4 implemented and independently verified; R3 reporting corrected. Complete local checker/control proofs pass. Exact-final full Make comparison is complete: candidate1296/150fail/128error/4skip versus base1267/150fail/128error/3skip, both actual exit2; all278 failure/error tuple occurrences match by exact name and multiplicity, candidate-minus-base=[] and base-minus-candidate=[]. This is not a green full suite. Selected-tree make validate-agent-assets completed with actual exit0; canonical privacy exits0 across285 selected a06 artifacts,0secret/home-path matches, valid JSON and modes0644. No RESULT or merge approval before root's explicit ci=green.

[memory:decision] Continue PR440, branch tools/task-generator-plan-check-a05-checker, from b8bf806655496b7a897aea25e1b43319095fac23. Task copy remains byte-identical amended b9e04cb9. Root2827 and the complete security addendum define this last worker repair batch; no caller, regime fixture or canonical task edit.

R1: cache absence now reaches a verdict. Launch honors a supplied absolute UV_CACHE_DIR or uses its own absolute private TemporaryDirectory, then cleans it; a supplied relative value refuses. Executable binding, isolated child environment and token forwarding remain.

R2: C12 comparison keys retain enumerated spelling independent of an alternate filename's existence. Applied-file classification now uses the original operand's confined resolved target. The platform-neutral model forces the NFC alternate absent/non-file, exercising distinct/same-target collisions and the one-file wrong-row control.

R4 / security:b8bf806:1: C6/C15 fetch original canonical design spelling; API validation no longer replaces it with NFC, and recursive reads retain raw child names. Tests reject an NFD design using another NFC file's receipt/hash with omitted invariants, reject a missing NFD design despite existing NFC, and accept correct NFD receipt/hash/invariants. The fake API percent-decodes request paths and keeps raw Unicode file keys.

R3: the previous six candidate-extra failures are our R1, not #441. That attribution is withdrawn in validation.md, with each original tuple named. The premature prior RESULT is preserved as result-before-final-revision.txt, not current readiness. This round commits locally and PONGs; root transports, returns ci=green or ci=red names, and RESULT waits for ci=green. Security addendum was received whole and is part of this batch.

Final bindings: revision1-final-bindings.json, sourcef43de893/testbe102aab/legacy20eff6f4. Complete fixed60 production419add27del=446/450. All tests652new+35legacyadd22del+6upstreamadd5del=720/720. No inherited exclusion or cap amendment. Existing helpers, rows and subprocess defaults remove29 fixture lines; independent reversal preserves104 assertion-call AST multiplicities, and raw-API/cache positive controls were added.

Each native315/312:29 new+10legacy tests pass, one disclosed native Unicode alias subtest skip; unchanged5RegimeCi methods covering6 former failure subcases pass without error/skip; mutations=48 killed=48 survived=0. All7 historical groups fail by assertion with zero errors/skips as required, driver exits0. Independent16-method runs each runtime pass on exact final bytes. Worker Crit-data gate exits0 after saved/read final review evidence.

All original interpreter/canonical/token/C14/path/C16 defenses remain. No new helper/dependency/config/workflow/deployment. Retained a05 files remain unchanged from06ffefbc; owner2817's25 upstream paths remain byte-identical to762a2541. Foreign untracked paths and timestamp worklogs are not committed.

Root owns final-head GitHub/Linux CI, recordsPR444/canonical publication, Bot/security/task audit, feedback dispositions, acceptance and integration. Local fake API/filesystem proofs confer no live GitHub or native Linux authority. Parent execution, caller-supplied shared caches, credentials and same-UID replacement remain residuals. No network/push/escalation/Bats/browser/graph update/merge-to-main. cost:n/a.

Complete selected fixed-base inventory:474 paths, recorded in full-diff-inventory.json and complete numstat/name lists in measure.md. Original task copies remain byte-identical; required reports/review/revise evidence are tracked. Earlier command-writer syntax/fence and unmasked-metadata attempts are process-only and disclosed in revision1-final-artifact-commands.json; no source/test change followed frozen validation.
# Exact final worker-round2 validation

Source/test bindings: revision1-final-bindings.json. Final sourcef43de893ab5f7d3d68bac6be5cf8c04c6e33d4303bd38e6eab56dc2726880800, new testbe102aab7c88dc74f3be5019005992f53485b0a8ed3addcb8abb4decb338dbe1; legacy20eff6f4 remains unchanged. All results below are actual process exits, with full expanded commands and verbatim output in the named artifacts. Root security addendum was received; RESULT still requires explicit final-head ci=green.

## Complete checker and unchanged caller proofs

revision1-final-module-commands.json and revision1-final-modules-{new,legacy}{315,312}.log: each native3.15.0/3.12.15 passes29 new+10legacy tests, all four actual exits0. Only the native Unicode two-file subcase skips because this host observed NFC/NFD aliasing. Modeled absent-alternate, distinct/same-target collision, wrong-row, one-file and overlap cases execute; no native Linux claim.

revision1-final-regime-commands.json and revision1-final-regime315/312.log: unchanged5RegimeCi methods covering6 prior CI failure subcases pass on both runtimes, actual0,0failures/errors/skips. test_regime_ci.py is byte-identical to the imported upstream file.

## Red before repair and historical controls

Initial R1/R2 reds use frozen42183ecc: revision1-red-commands.json and logs show2tests/2assertfail/0error/0skip on each runtime, driver exits0. R4 reds use dd44ae34 with cache/type fixes only: revision1-final-r4-red-commands.json and logs show2tests/2assertfail/0error/0skip on each runtime, driver exits0. Final R4 greens use exactf43/be10: both2methods pass with0error/skip and exits0, including correct NFD receipt/hash/invariant and raw directory-child controls.

The final tests were also rerun against all historical source snapshots; every named method fails behaviorally with no import/error/skip. Complete executed argv/env/code is in revision1-final-historical315/312-command.json; full output in revision1-final-historical315/312.log; captured JSON in revision1-final-historical-red315/312.json. Drivers actually exit0. Their reused old JSON basename was copied to these revision files after completion, and the old historical basename was restored byte-identical fromb8; the command records disclose that capture step.

| Source group, each runtime | Tests | Assertion failures | Errors | Skips |
| --- | --- | --- | --- | --- |
| historical16 | 16 | 18 | 0 | 0 |
| security-cedc7f5 | 3 | 3 | 0 | 0 |
| security-06ffefb | 4 | 4 | 0 | 0 |
| review-5c09a95a | 2 | 2 | 0 | 0 |
| review-1779440f | 1 | 1 | 0 | 0 |
| revision1-R1-R2 | 2 | 2 | 0 | 0 |
| revision1-R4 | 2 | 2 | 0 | 0 |

## Mutation sensitivity

revision1-final-mutations315/312-command.json contains the exact48 cases and execution code; logs and JSON retain each id/selector/mutant SHA/outcome. Each runtime: mutations=48 killed=48 survived=0, actual driverexit0. Every kill is an assertion failure, one selected test, no error/skip. Controls retain the prior40 and add cache absence/private cleanup/relative refusal/supplied absolute honor, resolved classification, original design/request/child spelling. Mutants and runners exist only inTMP; command records are data.

Expected FAILED footers in red/mutation logs are negative child observations, never claimed as passing suites. revision1-final-observations.json consolidates actual exits/results.

## Corrected R3 historical delta

Owner2827 reported actual GitHub Unit-test run39402138504:7failures of1296 on all3Linux jobs. Macos14 skips unit tests for the Python-only diff, so its success is no unit-test evidence. Six are R1; the seventh is R2. No worker GitHub read is claimed.

Prior local base1267/150fail/128error/3skip and candidate1295/156fail/128error/4skip both exited2. The278 base failure/error tuples retain exact multiplicity, but the6 added tuples below are our checker R1. Prior attribution to #441 was wrong and is withdrawn:
- test_regime_ci_accepts_a_base_that_moved_past_the_merge_base (test_regime_ci.RegimeCiTest.test_regime_ci_accepts_a_base_that_moved_past_the_merge_base); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage) (reset_of=True, predecessor_copy_kept=False); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage) (reset_of=True, predecessor_copy_kept=True); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (test_regime_ci.RegimeCiTest.test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier) (expected=0, phrase=None); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (test_regime_ci.RegimeCiTest.test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config (test_regime_ci.RegimeCiTest.test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config); multiplicity=1; cause=R1 import-time cache refusal.

The old report/validation remain explicitly historical. The dd44/test57b full candidate started before R4 was interrupted as obsolete; revision1-full-unit-exit.json marks it incomplete. It is not a final suite or comparison proof.

## Final candidate-minus-base comparison

COMPLETE with actual observed make exit2. revision1-final-full-suite-snapshot.json binds clean snapshot689cd97a61f002bb72f09f8e040039c5b7bd06b6 to finalf43/be10 bytes and exact argv/environment. revision1-final-full-unit-candidate.log/exits:1296 tests in1090.406s,150failures,128errors,4skips. Unchanged fixed60 baseline full-unit-base.log/full-unit-commands.json:1267 tests in842.479s,150failures,128errors,3skips, actual exit2. Same validated native315/offline environment, private cache paths differ. Additional skip is the disclosed native Unicode alias subcase.

Exact candidate-minus-base test-name/multiplicity tuples: `[]` (zero added occurrences).
Exact base-minus-candidate test-name/multiplicity tuples: `[]` (zero removed occurrences).

revision1-final-full-unit-comparison.json preserves all278 baseline and278 candidate failure/error tuple occurrences, unique tuple counts and both Counter differences. Parser uses only unittest70-equals/FAIL-or-ERROR/70-hyphens headers, retains repeated subcases, and asserts header counts match footer failure/error totals. It does not count bare fixture ERROR diagnostics. revision1-final-artifact-commands.json records the exact executed parser code/argv and actual exit0. This is an exact local baseline comparison, not a green full suite, native Linux run or final-head GitHub CI. The previous6 added failures were our R1 and are gone after the repair; the prior inherited attribution remains withdrawn.

## Format, lint, review and gate

Changed Python Ruff format check exits0. Production-only CI-style R4 lint exits0 in revision1-final-production-r4.log;5 inherited warnings in unchanged regime-ci.py remain outside scope. Full make format on the exact final snapshot exits2 at inherited shfmt differences; entire output is byte-identical to unchanged baseline, recorded in revision1-final-format-command.json/log. No lint baseline or assertion is weakened.

Read independent final MD/JSON, exact commands, both16-test runtime logs and consolidation proof. Each runtime exit0 with one disclosed native alias subtest skip; source/test/task hashes unchanged. All104 assertion-call AST multiplicities survive reversal of29 fixture-consolidation lines. Original intermediate consolidation record is not misrepresented as final-byte equivalence; later raw-API/cache controls are separately reviewed.

worker-review-evidence.json and worker-review-receipt.md bind the final resolved R1/R2/security:b8bf806:1 records. revision1-worker-gate-commands.json: unreviewed gate exits2 requesting review, saved/read Crit-data reviewed gate exits0. Independent process review is not final-head CI/task audit/acceptance.

Selected-tree make validate-agent-assets completed with actual exit0, log revision1-assets.log ending agent asset validation ok, metadata revision1-assets-command.json/result.json. It uses a clean selected tree with exact final source/test bytes; final data-only additions receive a canonical privacy scan. Final canonical privacy verification exits0:285 selected a06 artifacts,0secret matches,0home-path matches, all JSON parses and all artifact modes0644. revision1-final-artifact-privacy.json binds the final source/test/task and canonical validator hash. Initial newly written command metadata needed a further canonical mask; the attempt is disclosed in revision1-final-artifact-commands.json. Original task copies were scanned without rewriting. No local Bats, browser Crit, network, push or escalation. Task copy staysb9e; root owns canonical publication/recordsPR444 and applicable final-head CI/Bot/audits/feedback/acceptance/integration. RESULT requires explicit rootci=green.

**Reviewing test environment assumptions**
**Verifying sandbox enforcement claims**
exec
/bin/zsh -lc "rg -n 'excludedCommands|gh|sandbox|network_access|worker.*exclu' home/dot_agents/agent-config.yaml home/dot_config/claude/settings.json.tmpl home/dot_claude/modify_private_settings.json home/dot_codex/config.toml.tmpl .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '135,171p' scripts/orchestrator/regime-ci.py; rg -n 'UV_CACHE|env|GH_TOKEN|GITHUB_TOKEN' .github/workflows/regime.yml; cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-4a49ed9.md.last.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-cedc7f5.md.last.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-06ffefb.md.last.md" in ~/Workspace/dotfiles
 exited 2 in 73ms:
rg: home/dot_config/claude/settings.json.tmpl: No such file or directory (os error 2)
rg: home/dot_codex/config.toml.tmpl: No such file or directory (os error 2)
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:3:task_id: dotfiles-T133-worker-sandbox-exclusions-followup-a01
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:10:  - .orchestration/dotfiles-T133-worker-sandbox-exclusions-followup-a01/**
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:11:after: [dotfiles-T133-worker-sandbox-exclusions-a02]
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:17:  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-worker-sandbox-exclusions-followup-a01/task.md)
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:19:  - control: the branch evidence records under .orchestration/dotfiles-T133-worker-sandbox-exclusions-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:20:    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:32:    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:34:    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:40:# AGMSG-TASK dotfiles-T133-worker-sandbox-exclusions-followup-a01 — the worker sandbox exclusions lineage's owner task (advisory P2 of the worker-sandbox-exclusions PR)
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:42:Written 2026-10-20 by the orchestrator seat before the first advisory disposition of the worker-sandbox-exclusions PR (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01` in `.orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a02.md` (plan 020 step 1.2); it is dispatched after the worker-sandbox-exclusions PR merges, to a seat the orchestrator names, and only when that section holds at least one row (C-102).
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:46:Each owned row (any advisory P2 of the local review or the task-level audit of the worker-sandbox-exclusions PR's final head, and any Bot P2 the orchestrator records under this owner; rows are read from the record at dispatch; a records-only row is realised by the record it names, with no test) gets its fix and, where the row names a test or code, one red-then-green test in `tests/unit/test_generate_agent_configs.py`, named in report.md against the row id. Nothing outside the owned rows; any other file joins `allowed_files` only by an amendment that names the row needing it.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:50:The a02 text removes the exclusions on the evidence of a macOS Claude seat (messages 2827 and 2830 sent from sandboxed Bash) and records the Linux runtime as unmeasured. This owner measures it: a GitHub Actions job on `ubuntu-24.04` that installs the rendered Claude settings, starts the herdr server socket (or a unix-socket stand-in at the allowlisted path) and runs `scripts/orchestrator/dispatch.sh` inside the Claude sandbox against it, recording exit code and output; the job is advisory (no required context) and its result is pasted into the acceptance record. If Linux denies the socket, the owner proposes the Linux-only exclusion list as a design item for 5.14 item 10 instead of silently restoring it. One test asserts the job's workflow file names the allowlisted socket path from the manifest.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md:54:The Check and Completion clauses of `.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md` apply as written, with `dotfiles-T133-worker-sandbox-exclusions-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-sandbox-exclusions-followup-a01/task.md>` in the RESULT. Design 5.14 applies by reference (D-024-30).
home/dot_agents/agent-config.yaml:12:# - Keep Codex writable roots for shared agmsg state under codex.sandbox_workspace_write.
home/dot_agents/agent-config.yaml:13:#   The Claude sandbox allowWrite list is rendered from the same entries.
home/dot_agents/agent-config.yaml:34:    claude: { model: claude-opus-5-5, effort: xhigh, advisor: fable }
home/dot_agents/agent-config.yaml:37:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml:42:    claude: { model: claude-fable-5-1, effort: xhigh }
home/dot_agents/agent-config.yaml:43:    codex: { model: gpt-6.1-sol, model_reasoning_effort: xhigh }
home/dot_agents/agent-config.yaml:45:    claude: { model: claude-fable-5-1, effort: xhigh, advisor: fable }
home/dot_agents/agent-config.yaml:48:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml:52:    claude: { model: claude-fable-5, effort: high }
home/dot_agents/agent-config.yaml:56:      model_reasoning_effort: high
home/dot_agents/agent-config.yaml:60:    # at xhigh reasoning effort (operator pin 2026-10-09, T115).
home/dot_agents/agent-config.yaml:61:    claude: { model: claude-fable-5-1, effort: high }
home/dot_agents/agent-config.yaml:64:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml:65:      sandbox_mode: read-only
home/dot_agents/agent-config.yaml:96:  sandbox_mode: workspace-write
home/dot_agents/agent-config.yaml:114:  sandbox_workspace_write:
home/dot_agents/agent-config.yaml:115:    network_access: false
home/dot_agents/agent-config.yaml:223:      - Bash(gh release:*)
home/dot_agents/agent-config.yaml:230:      - Bash(gh pr merge:*)
home/dot_agents/agent-config.yaml:231:      - Bash(gh pr create:*)
home/dot_agents/agent-config.yaml:232:      - Bash(gh pr comment:*)
home/dot_agents/agent-config.yaml:233:      - Bash(gh pr review:*)
home/dot_agents/agent-config.yaml:234:      - Bash(gh pr close:*)
home/dot_agents/agent-config.yaml:235:      - Bash(gh pr edit:*)
home/dot_agents/agent-config.yaml:236:      - Bash(gh pr update-branch:*)
home/dot_agents/agent-config.yaml:237:      - Bash(gh issue:*)
home/dot_agents/agent-config.yaml:238:      - Bash(gh api -X POST:*)
home/dot_agents/agent-config.yaml:239:      - Bash(gh api --method POST:*)
home/dot_agents/agent-config.yaml:240:      - Bash(gh api -XPOST:*)
home/dot_agents/agent-config.yaml:241:      - Bash(gh api --method=POST:*)
home/dot_agents/agent-config.yaml:242:      - Bash(gh api -X PATCH:*)
home/dot_agents/agent-config.yaml:243:      - Bash(gh api --method PATCH:*)
home/dot_agents/agent-config.yaml:244:      - Bash(gh api -XPATCH:*)
home/dot_agents/agent-config.yaml:245:      - Bash(gh api --method=PATCH:*)
home/dot_agents/agent-config.yaml:246:      - Bash(gh api -X PUT:*)
home/dot_agents/agent-config.yaml:247:      - Bash(gh api --method PUT:*)
home/dot_agents/agent-config.yaml:248:      - Bash(gh api -XPUT:*)
home/dot_agents/agent-config.yaml:249:      - Bash(gh api --method=PUT:*)
home/dot_agents/agent-config.yaml:250:      - Bash(gh api -X DELETE:*)
home/dot_agents/agent-config.yaml:251:      - Bash(gh api --method DELETE:*)
home/dot_agents/agent-config.yaml:252:      - Bash(gh api -XDELETE:*)
home/dot_agents/agent-config.yaml:253:      - Bash(gh api --method=DELETE:*)
home/dot_agents/agent-config.yaml:254:      - Bash(gh api -f:*)
home/dot_agents/agent-config.yaml:255:      - Bash(gh api -F:*)
home/dot_agents/agent-config.yaml:256:      - Bash(gh api --raw-field:*)
home/dot_agents/agent-config.yaml:257:      - Bash(gh api --field:*)
home/dot_agents/agent-config.yaml:258:      - Bash(gh api -f*)
home/dot_agents/agent-config.yaml:259:      - Bash(gh api -F*)
home/dot_agents/agent-config.yaml:260:      - Bash(gh api --raw-field=*)
home/dot_agents/agent-config.yaml:261:      - Bash(gh api --field=*)
home/dot_agents/agent-config.yaml:267:  # Claude Code Bash sandbox, the counterpart of codex.sandbox_workspace_write:
home/dot_agents/agent-config.yaml:270:  # codex.sandbox_workspace_write.writable_roots so both agents share one agmsg
home/dot_agents/agent-config.yaml:271:  # writable-roots list; ~/.claude is sandbox-protected, so it is not listed.
home/dot_agents/agent-config.yaml:276:  sandbox:
home/dot_agents/agent-config.yaml:278:    # Two-stage rollout: warn and run unsandboxed while bwrap/socat are missing;
home/dot_agents/agent-config.yaml:282:    allowUnsandboxedCommands: true
home/dot_agents/agent-config.yaml:283:    # T39 recorded Herdr PermissionDenied on 2026-10-01; T130 added $HOME/.config/herdr/herdr.sock to allowUnixSockets; the orchestrator sent sandboxed Bash messages 2827 and 2830 on 2026-10-20.
home/dot_agents/agent-config.yaml:284:    excludedCommands: []
home/dot_agents/agent-config.yaml:287:      # Rendered into sandbox.filesystem.allowWrite after the Codex writable
home/dot_agents/agent-config.yaml:317:      # auto-approved sandbox into an escape (T44 r2, operator 2026-10-01).
home/dot_agents/agent-config.yaml:386:# pins here only, through generate-agent-configs.py --set-asset. `pin: unknown`
home/dot_agents/agent-config.yaml:394:    attestation: when-gh-authenticated
home/dot_agents/agent-config.yaml:396:    note: the newest cooled-down release installs only when gpg and gpgv (SHASUMS256.asc checked against the release key with gpg_fingerprint, fetched from keys.openpgp.org as mise documents) or an authenticated gh (the release attestation) can verify it before it runs; otherwise the fallback release does, and mise self-update moves it forward afterwards.
home/dot_agents/agent-config.yaml:404:      reason: a host without gpg and without an authenticated gh (a fresh macOS) can check neither the release key's signature nor the release attestation before mise runs, and SHASUMS256.txt comes from the same release; so it bootstraps this reviewed release, SHASUMS256.txt kept as a second check.
home/dot_agents/agent-config.yaml:470:    attestation: when-gh-authenticated
home/dot_agents/agent-config.yaml:471:    note: chezmoi signs its checksums with cosign only, which a fresh host cannot run; the newest cooled-down release installs only when an authenticated gh can check its release attestation before it runs, otherwise the fallback release does, and mise's own chezmoi takes over after the bootstrap.
home/dot_agents/agent-config.yaml:479:      reason: setup.sh runs before gh is installed or logged in, so a fresh host cannot check chezmoi's release attestation before chezmoi runs, and its cosign signature needs cosign; it bootstraps this reviewed release, the release's checksums file kept as a second check.
home/dot_agents/agent-config.yaml:544:    note: PyPI read 2026-10-17T10:33Z; eight platform wheels, no sdist or universal wheel; these four cover Mac and glibc Linux on amd64/arm64.
home/dot_agents/agent-config.yaml:616:      behind that tag (lightweight tag, c487be2), and sha256 is the digest of
home/dot_agents/agent-config.yaml:658:  gh-extensions:
home/dot_agents/agent-config.yaml:659:    source: gh-extension
home/dot_agents/agent-config.yaml:660:    upstream: https://github.com/seachicken/gh-poi
home/dot_agents/agent-config.yaml:663:    installer: install/common/gh_extensions.sh
home/dot_agents/agent-config.yaml:664:    note: install/common/gh_extensions.sh installs seachicken/gh-poi unpinned
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:3:task_id: dotfiles-T133-worker-sandbox-exclusions-a02
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:4:reset_of: [dotfiles-T133-worker-sandbox-exclusions-a01]
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:13:  - .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/**
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:16:  - control: the predecessor copy .orchestration/dotfiles-T133-worker-sandbox-exclusions-a01/task.md (reset_of)
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:17:    disposition: "residual: the a01 worker committed nothing (implementation_commits=0 in its blocked PONG), so no a01 copy exists on any branch; the a02 copy at .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md is the only task copy of the lineage and regime-ci verifies the latest copy of a reset_of lineage against the text on main"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:19:    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_sandbox_exclusions_render_empty_for_all_os"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:21:    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_sandbox_exclusions_are_empty_for_all_os"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:22:  - control: the PR edits scripts/validate-agent-assets.py (the validator rejects a non-empty rendered excludedCommands list)
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:23:    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_sandbox_validator_requires_empty_exclusions"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:28:  - control: the PR edits .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/**
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:30:  - control: the task copy (.orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md)
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:32:  - control: the evidence records (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:33:    disposition: "residual: command outputs and sandbox message ids are recorded without secrets or literal home paths and independently checked at acceptance"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:41:    disposition: "residual: tooling and Git retain tool, configuration and inherited environment inputs; the worker sandbox confines execution and the task-level audit from main checks inputs and effects"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:55:    disposition: "residual: Check isolates the unit-test processes only; other repository tooling stays in the worker sandbox and is checked by the task-level audit from main"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:63:    disposition: "residual: sandbox.md separates Claude macOS sends 2827 and 2830, the Codex probe denial, rendering-only CI, unmeasured Linux Claude sandbox runtime owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01, and unapplied live seats"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:70:  - control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:71:    disposition: "residual: empty-list tests check configuration; Claude sandboxed sends and the Codex sandbox denial record runtime evidence; Codex networking is a separate task, Linux runtime remains unmeasured, live seats retain the exclusion until apply, and permgate remains operator-owned"
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:75:      /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I -c 'from pathlib import Path; m=Path("home/dot_agents/agent-config.yaml").read_text(); t=Path("home/.chezmoitemplates/claude-settings-managed.json").read_text(); a=m.split("    excludedCommands:",1)[1].split("    linux_excluded_commands:",1)[0]; b=m.split("    linux_excluded_commands:",1)[1].split("    filesystem:",1)[0]; print("shared="+str(a.count("\n      - "))+" linux_additions="+str(b.count("\n      - "))+" rendered_sites="+str(t.count("\"excludedCommands\""))+" herdr_socket="+str(".config/herdr/herdr.sock" in m))'
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:80:      /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I -c 'import ast; from pathlib import Path; p=Path("tests/unit/test_generate_agent_configs.py"); t=p.read_text(); c=next(n for n in ast.parse(t).body if isinstance(n, ast.ClassDef)); v=Path("scripts/validate-agent-assets.py").read_text(); print(str(p)+" class="+c.name+" unittest.main="+str(t.rstrip().endswith("unittest.main()"))+" validator_linux_exact="+str("Linux excludedCommands must match the exact seat-tool list" in v))'
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:85:# AGMSG-TASK dotfiles-T133-worker-sandbox-exclusions-a02 — empty every rendered sandbox exclusion list
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:87:Design 5.14 of .orchestration/plans/024-design-quality.md is frozen by D-024-29 and applies by reference under D-024-30; rely on items 0–10, implementing item 10's exclusion-list change here. Worker: Codex security profile, because the affected execution boundary is Claude's; this seat has no network and the orchestrator transports its committed head. Generation, lint and Makefile recipes are the repository's own tooling run inside the worker's sandbox (design 5.14 items 2, 7, 9 by reference, D-024-30).
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:92:Set both `claude.sandbox.excludedCommands: []` and `linux_excluded_commands: []`; retain both keys, removing every pattern including the Linux additions. Replace the exclusion-history comments with one English sentence recording T39's 2026-10-01 Herdr PermissionDenied, T130's addition of `$HOME/.config/herdr/herdr.sock` to allowUnixSockets, and the orchestrator's sandboxed Bash messages 2827 and 2830 on 2026-10-20.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:93:Regenerate through `uv run --no-config --no-project --offline --python "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" --with pyyaml python -I scripts/generate-agent-configs.py`; both OS branches of the managed template must retain `"excludedCommands": []`. Do not hand-edit generated output or change the generator.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:94:Replace the validator's old list policy with an empty-list rule for both OS variants: reject every non-empty list and malformed non-list, retaining the existing missing-key default. Preserve diagnostics exercised by unchanged validator tests (`macOS.*gh` and `Linux.*excludedCommands`) without exceptions to the empty-list rule.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:98:In GenerateAgentConfigsTest add the three selectors named above: render the real manifest for darwin/linux and assert empty lists; render both committed template branches and assert empty lists; import the real validator by file path and exercise empty acceptance plus non-empty and malformed refusals on both OS variants. Include agmsg-dispatch, gh, git push, herdr-agents, actas-claim and an arbitrary pattern. Update existing exclusion expectations in this module; keep `unittest.main()` and use existing fixture helpers.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:100:Every new behavior must have an assertion-based red result before implementation and green afterwards, with selectors and both outcomes in report.md; missing executables, imports or dependencies do not count as red. Keep fixture tool invocations runnable under the prescribed clean PATH through absolute installed tool paths, without widening PATH or adding dependencies.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:102:The orchestrator pastes its own macOS Claude-sandbox measurement into the acceptance record: messages 2827 and 2830 of 2026-10-20, sent from sandboxed Bash, with exact commands, exit statuses, redacted outputs and message ids.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:103:From sandboxed Bash run `agmsg-dispatch "$TEAM" "$WORKER" "$ORCHESTRATOR" "$ORCHESTRATOR_PANE" 'AGMSG-PONG v1 task_id=dotfiles-T133-worker-sandbox-exclusions-a02 status=working reason=sandbox-dispatch-probe'`, binding recipients from the dispatch envelope. In validation.md record the exact command, sandbox/runtime identity (`network_access=false`, no Unix-socket allowlist), exit code, verbatim redacted output and any message id actually returned. The prior Codex-sandbox measurement was Herdr-socket `PermissionDenied: Operation not permitted`; record this worker's measured result without requiring successful dispatch or a delivered PONG, and never retry outside the sandbox.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:104:This probe records the Codex half of design 5.14 item 10; the manifest's `sandbox_workspace_write.network_access = true` is a separate task. No CI step launches a Linux Claude sandbox, so `agmsg-dispatch` runtime behavior there remains unmeasured by this task, a residual owned by follow-up task `dotfiles-T133-worker-sandbox-exclusions-followup-a01`.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:108:Worker Playbook step 4 applies: every command runs inside the sandbox; record the expected Codex probe refusal in sandbox.md as measured state; for any other refusal record it in sandbox.md and send `AGMSG-PONG v1 status=blocked`; never retry outside.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:120:Start a fresh branch with `git switch -c security/worker-sandbox-exclusions-a02 --no-track origin/main`. Save .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md byte-identical to the dispatched text; in that directory write report.md (changes, named red/green outcomes, residuals, cost), validation.md (commands/output, exit codes, Codex-sandbox probe result, actual message ids, cap totals), sandbox.md, learning.md and autoskill.md (used or not-used). Maintain Codex seat plan/todo worklogs with at most one active todo per owner; do not commit plan/todo/learn. Include a cost: line with observed figures or n/a.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:121:Commit locally, then send `AGMSG-PONG v1 status=working head=<40-hex>` with artifact paths. The orchestrator transports that exact head to github.com/mryfmo/dotfiles, creates the English PR, verifies exact-head Actions and the Worker Playbook step 15 Bot wait, then sends a PING binding head, PR URL and `ci=green` or failed checks. Fix in-scope failures through another committed head and transport cycle; the worker performs no network operation or merge.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:122:Only after the orchestrator's matching-head `ci=green` PING send `AGMSG-RESULT v1 task_id=dotfiles-T133-worker-sandbox-exclusions-a02 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` and artifact paths.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:124:Out of scope: permgate (operator-owned), Codex networking, other permission changes and live apply; Linux sandbox runtime measurement remains with `dotfiles-T133-worker-sandbox-exclusions-followup-a01`. The change reaches live seats only at the next `make update` after P1-14 a05 merges; until then worker seats retain the exclusion and task-level audits keep recording the existing P1.
.orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md:127:Amendment 1 (`previous_sha256: 6f95aef556842405912d7a929d19b95ba95efaa8c2b0e61c72d1ae925e5cc7fc`): the Codex sandbox denies writes under `~/.cache/uv` (measured by a013 at 14:29Z: `Operation not permitted`), so every uv invocation of this task uses a fresh private cache seeded from the read-only default cache: once per session run `UV_CACHE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/uv-cache-wse-a02.XXXXXX")"; case "$UV_CACHE_DIR" in /*) ;; *) echo refused: UV_CACHE_DIR not absolute; exit 1;; esac; chmod 0700 "$UV_CACHE_DIR"; cp -R "$HOME/.cache/uv/." "$UV_CACHE_DIR/"; export UV_CACHE_DIR` and paste the commands, `ls -ld "$UV_CACHE_DIR"`, `du -sh "$UV_CACHE_DIR"` and the exit codes into validation.md (mktemp creates a new directory with a random suffix and mode 0700, so no pre-existing path or symlink is reused); the exported variable then reaches every prescribed `uv run` and every `make` target that invokes uv (Makefile line 189) in the same shell; a copy that fails or a cache without `pyyaml` is reported as `AGMSG-PONG v1 status=blocked`, never worked around online. Interference by another process of the same UID with the copied entries remains the residual of design 5.14 item 9 that the a01 and a06 lineages record (no host isolation claimed).

 succeeded in 78ms:
            found.append(
                f"precheck.json head {bound[:12]} differs from the head outside .orchestration/{t}/: {', '.join(other)}"
            )
    if token(result_text, "precheck") != sha256(data):
        found.append(
            f"precheck.json sha256 {sha256(data)} is not result.txt's precheck={token(result_text, 'precheck')}"
        )
    return found


def policy(root, base, head, t):
    """Return (the policy bytes, its front matter or None, whether the base's dispatched text is the policy)."""
    dispatched = show(root, base, f".orchestration/tasks/{t}.md")
    data = show(root, head, f".orchestration/{t}/task.md") if dispatched is None else dispatched
    return data, front(data), dispatched is not None


def redact(text):
    """Mask the GH_TOKEN/GITHUB_TOKEN values and token-like literals in checker output (security review of a8c03fae)."""
    for value in filter(None, map(os.environ.get, ("GH_TOKEN", "GITHUB_TOKEN"))):
        text = text.replace(value, "[redacted]")
    return TOKEN_LIKE.sub("[redacted]", text)


def checker(root, data):
    """Return the base checker's violations on the base's dispatched bytes: it hands the text's literals to git (C8 to
    C10) and opens its design path (C6), so a pull request's own text never reaches it (worker review P0 of bcbd6949)."""
    with tempfile.TemporaryDirectory() as scratch:
        cmd = [*CHECKER_RUN, "--root", root, str(Path(scratch, "task.md"))]
        Path(cmd[-1]).write_bytes(data)
        run = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
    out = run.stdout.splitlines()  # the file is task.md, so C1 compares task_id with `task`; task-id checks <t>
    # only the checker's own verdict line with its exit code counts; a crash also exits 1, with no verdict line
    if (out[:1], run.returncode) not in ((["task.md: OK"], 0), (["task.md: FAIL"], 1)):
        return [("checker", f"no verdict (exit {run.returncode}): {redact(run.stdout + run.stderr).strip()[-300:]}")]
    lines = [redact(ln).strip() for ln in out[1:] if ln.strip()]
    return [("checker", ln) for ln in lines if not re.fullmatch(r"C1 task_id .* != file task", ln)]
34:        env:
41:        env:
45:          GH_TOKEN: ${{ github.token }}
- [P2] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md:133 NFC-based row matching can credit one threat row to two distinct Linux files, `scripts/caf\u00e9.py` and `scripts/cafe\u0301.py`, under `scripts/**`; preserving original paths for filesystem operations does not bind the coverage decision to each file. Require identity-aware row matching or collision rejection, with a two-file regression before closing the pipeline-identity row.

An in-memory probe of the inherited matching logic confirmed this collision. Reviewed all 39 threat rows and the cited acceptance/review history; the declared parent-execution, cache and same-UID residuals are not additional findings.

📝 まとめ: Pre-dispatch review completed with one P2 design finding for orchestrator disposition; no files changed.

Not checked: future implementation, native filesystem behavior or Linux deployment; declared execution and credential risks remain.
Verdict: incorrectReviewed [PR #440](https://github.com/mryfmo/dotfiles/pull/440), exact range `60a6fb2…cedc7f5`. Found three P2 issues:

1. **P2 · High confidence · `scripts/orchestrator/task-consistency-check.py:420`** — NFC normalization changes the filename before confinement checking: on Linux, an escaping `tests/fixtures/cafe\u0301.py` symlink is checked as the distinct `café.py` path and can receive the fixture exemption. Resolve the original enumerated path; normalize only comparison values.

2. **P2 · High confidence · `scripts/orchestrator/task-consistency-check.py:440`** — An internal directory symlink such as `tests/fixtures/alias → scripts/` passes confinement but escapes coverage because traversal skips directory links and this condition checks only files. Reject such aliases or explicitly validate their coverage without silently skipping them.

3. **P2 · High confidence · `scripts/orchestrator/task-consistency-check.py:469`** — Eleven valid item rows plus another row naming both `5.14 item 0` and `5.14 item 1` pass C16: the combined row contributes nothing to either count. Reject multi-item rows and count every occurrence when detecting duplicates.

The first two undermine the threat table’s fixture/evidence symlink control and path-normalization assurances; the third leaves the C16 control incomplete. The other closed controls—interpreter-selection order, token forwarding, canonical-main reads, and canonical receipt/hash binding—match the inspected implementation. Shell-free probes, safe YAML loading, and fixed repository/host arguments showed no additional injection or deserialization defect. Declared parent-startup, shared-cache, same-UID, and shared-credential risks remain residuals.

Focused, read-only checks of AST-extracted functions reproduced all three gaps; filesystem conditions were modeled. Source/test hashes matched the latest evidence, and the recorded scanner alert matched a synthetic-token digest.

📝 まとめ: 指定差分と threat_table のセキュリティレビューを完了し、P2 を3件報告しました。修正と受け入れ判断は orchestrator に委ねます。

Not checked: full test execution or live CI (`gh` could not connect); no files changed. Declared execution/cache/credential risks remain.
Verdict: incorrectReviewed [PR #440](https://github.com/mryfmo/dotfiles/pull/440), head `06ffefbc633fe37bcef107385ea96810b2a9a0c5`, against the specified base. Two findings:

- **P2 · High confidence · `scripts/orchestrator/task-consistency-check.py:246`** — Directory pruning compares raw filesystem names against NFC-normalized scopes, so a decomposed-Unicode directory is skipped entirely, allowing unnamed applied files or escaping symlinks to evade C12. An in-memory probe confirmed that `scripts/cafe\u0301/*.py` enumerates nothing although its normalized descendant matches. Normalize directory names for matching while retaining original paths for confinement.
- **P2 · High confidence · `scripts/orchestrator/task-consistency-check.py:465`** — C16 determines applicability from lexical scope alone, so a literal file symlink into `scripts/orchestrator/` passes without any 5.14 rows. A modeled `tests/fixtures/audit-alias.py` pointing to the checker returned no findings; naming the target directly produced all expected C16 failures. Include resolved targets when determining applicability.

The threat table’s C16 closure is therefore unsupported, and its symlink controls miss subtrees excluded by Unicode pruning. Interpreter-selection, token-forwarding, canonical-design, and receipt/hash controls hold within their stated boundaries on inspection. Remaining rows describe process controls or explicitly retained parent-execution, shared-cache, credential, and same-UID risks; this review does not establish those controls’ operational enforcement.

No additional injection or unsafe-deserialization issue was identified. Evidence hashes match the reviewed files; targeted credential scanning found no matching secrets. Recorded test results remain evidence claims, not independently rerun results.

📝 まとめ: Read-only security review completed with two P2 findings; acceptance remains with the orchestrator.

Not run: filesystem-writing test suites or live CI verification (`gh` network access failed). Known parent/cache and same-UID risks remain.
Verdict: incorrect
**Evaluating residual risk and control scope**
**Reviewing test scope and matching issues**
exec
/bin/zsh -lc "git show c439b63c:scripts/orchestrator/task-consistency-check.py | nl -ba | sed -n '245,330p'; git show c439b63c:scripts/orchestrator/task-consistency-check.py | nl -ba | sed -n '345,570p'; git show c439b63c:tests/unit/test_task_consistency_c11_c15.py | sed -n '386,419p;459,525p'; sed -n '276,323p' home/dot_agents/agent-config.yaml; sed -n '25,65p' .github/workflows/regime.yml" in ~/Workspace/dotfiles
 succeeded in 111ms:
   245	        return j < len(names) and fnmatch.fnmatchcase(names[j], parts[i]) and step(i + 1, j + 1)
   246	
   247	    return step(0, 0)
   248	
   249	
   250	def files(root, pattern, fold=os.path.normcase):
   251	    if not re.search(r"[*?\[]", pattern) and not (root / pattern).exists() and not (root / pattern).is_symlink():
   252	        yield root / pattern
   253	        return
   254	
   255	    def unreadable(error):
   256	        raise error
   257	
   258	    for folder, dirs, names in os.walk(root, followlinks=False, onerror=unreadable):
   259	        base = pathlib.Path(folder)
   260	        links = [n for n in dirs if (base / n).is_symlink()]
   261	        dirs[:] = [n for n in dirs if fold(n) != ".git" and n not in links]
   262	        dirs[:] = [n for n in dirs if match(path_entry(root, base / n, fold)[2], pattern, True, fold)]
   263	        for name in [*names, *links]:
   264	            if fold(name) != fold(".git"):
   265	                yield base / name
   266	
   267	
   268	def tokens(control):
   269	    return [
   270	        token.strip(chr(96)) for token in re.findall(r"[^\s\"'(),;]+", control) if normalise_name(token.strip(chr(96)))
   271	    ]
   272	
   273	
   274	def hits(control, allowed, root, fold=os.path.normcase):
   275	    prefixes = {a: re.split(r"[*?\[]", a, maxsplit=1)[0].rstrip("/") for a in allowed}
   276	    found = set()
   277	    for raw in tokens(control):
   278	        _, target, token = path_entry(root, raw, fold)
   279	        choices = [
   280	            a
   281	            for a, p in prefixes.items()
   282	            if token in (fold(a), fold(p))
   283	            or match(token, a, fold=fold)
   284	            and ("/" in normalise_name(token) or target is not None and target.exists())
   285	        ]
   286	        if choices:
   287	            found.add(max(choices, key=lambda a: (a == token, len(prefixes[a]))))
   288	    return found
   289	
   290	
   291	def rerun(cmd, root):
   292	    try:
   293	        words = shlex.split(cmd)
   294	        syntax = shlex.shlex(cmd, posix=False, punctuation_chars=";&|<>$()" + chr(96))
   295	        syntax.whitespace_split = True
   296	        if any(re.fullmatch(r"[;&|<>$()\x60]+", token) for token in syntax):
   297	            words = []
   298	    except ValueError:
   299	        words = []
   300	    op = words[:2]
   301	    ref = words[2] if len(words) == 3 and op == ["git", "rev-parse"] else ""
   302	    if ref and not ref.startswith("-") and not re.search(r"[\s;$\x60|&<>]", ref):
   303	        run = git(root, "rev-parse", "--verify", "--end-of-options", ref)
   304	        return run.stdout, run.returncode, run.stderr
   305	    if (len(words) == 3 and op in (["test", "-e"], ["test", "-f"])) or (len(words) == 4 and op == ["grep", "-c"]):
   306	        _, path, _ = path_entry(root, words[-1])
   307	        if path is not None:
   308	            if words[0] == "test":
   309	                return "", int(not (path.exists() if words[1] == "-e" else path.is_file())), ""
   310	            if path.is_file():
   311	                with path.open("rb") as stream:
   312	                    return str(sum(words[2].encode() in line.removesuffix(b"\n") for line in stream)) + "\n", 0, ""
   313	    return None, 1, "C14 unsupported or unconfined probe: " + cmd
   314	
   315	
   316	def check(p, root, premises_sha=None):
   317	    alias = root.with_name(root.name.swapcase())
   318	    fold = str.casefold if alias.exists() and alias.samefile(root) else os.path.normcase
   319	    fm = front(text := (data := p.read_bytes()).decode())
   320	    tid = fm.get("task_id")
   321	    suffix = tid.rsplit("-", 1)[-1]
   322	    fails = []
   323	    if tid != p.stem:
   324	        fails.append(f"C1 task_id {tid} != file {p.stem}")
   325	    allowed = []
   326	    for a in fm.get("allowed_files") or []:
   327	        if name := normalise_name(a):
   328	            allowed.append(name)
   329	        else:
   330	            fails.append(f"C12 confinement: {a}")
   345	            fails.append(f"C3 no threat_table row names {rid} task.md")
   346	    for a in allowed:
   347	        # a row's control names the entry only at a path boundary: scripts/foo.py.bak does not name scripts/foo.py
   348	        named = re.compile(re.escape(fold(a).split("*")[0].rstrip("/")) + r"(?=$|[ /\"'(),*?\[])")
   349	        if rows and not named.search(" ".join(key for _, _, key in row_paths)):
   350	            fails.append(f"C4 allowed path has no threat_table row naming it: {a}")
   351	    dr = fm.get("design_review") or {}
   352	    design = dr.get("design")
   353	    _, design_target, _ = path_entry(root, design)
   354	    if dr.get("design") and design_target is None:
   355	        fails.append("C6 design path is outside the checkout")
   356	        shown = None
   357	    else:
   358	        shown = main_bytes(root, design) if design else None
   359	    dfm = front(shown.decode()) if shown is not None and shown.startswith(b"---\n") else {}
   360	    dfm = dfm if isinstance(dfm, dict) else {}
   361	    if dr.get("receipt") or "design_sha256" in dr:
   362	        cur = (dfm.get("design_review") or {}).get("receipt")
   363	        if shown is None or not cur or dr.get("receipt") != cur:
   364	            fails.append("C6 design_review.receipt has no matching canonical design receipt")
   365	        if "design_sha256" in dr:
   366	            if shown is None or dr["design_sha256"] != hashlib.sha256(shown).hexdigest():
   367	                fails.append("C6 design_sha256 does not match canonical design bytes")
   368	        else:
   369	            print("warning: C6 design_sha256 absent; legacy receipt comparison", file=sys.stderr)
   370	    for r in rows:
   371	        m = re.search(r"names the (a\d\d) file's hash", r.get("disposition") or "")
   372	        if m and m.group(1) != suffix:
   373	            fails.append(f"C5 residual binds the {m.group(1)} hash, the task is {suffix}: {r.get('control')[:60]}")
   374	    for name in C7_NAMES:
   375	        if rows and name not in controls.lower():
   376	            fails.append(f"C7 threat_table has no row named for: {name}")
   377	    for r in rows:
   378	        if (r.get("control") or "").lstrip('"').startswith(NONPATH):
   379	            continue  # a non-path control may describe several files
   380	        hit = hits(r.get("control") or "", allowed, root, fold)
   381	        if len(hit) > 1:
   382	            fails.append(f"C7b one row names {len(hit)} allowed_files entries ({', '.join(hit)}); one row per entry")
   383	    body = text.split("\n---\n", 1)[1] if "\n---\n" in text else ""
   384	    if fm.get("kind") == "code":
   385	        for var in sorted(set(re.findall(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)*_EVIDENCE\b", body))):
   386	            # an input a script on origin/main already reads is not an added input
   387	            added = not main_contains(root, var, ("Makefile", "scripts", "home"))
   388	            if added and rows and var not in controls:
   389	                fails.append(f"C8 the task adds input {var} but no threat row controls it")
   390	    sentences = re.findall(r'"([^"]{20,})"', body) if fm.get("kind") == "docs" else []
   391	    for sent in sentences:  # C10
   392	        for scr in set(re.findall(r"scripts/[^\s\"'`,;()]+\.(?:sh|py)", sent)):
   393	            if path_entry(root, scr)[1] is None:
   394	                fails.append(f"C10 rule sentence names {scr}, a path outside the checkout")
   395	                continue
   396	            if main_entry(root, scr) is None:
   397	                continue
   398	            m = re.search(r"\b(once|until)\b", sent, re.IGNORECASE)
   399	            if m and scr in sent[m.start() :]:
   400	                continue  # the script is named inside its own landing clause
   401	            test = f"tests/unit/test_{pathlib.Path(scr).stem.replace('-', '_')}.py"
   402	            for lit in set(re.findall(r"`([^`]*(?:=|\[[^\]]+\])[^`]*)`", sent)):
   403	                if not main_contains(root, lit, (scr, test), literal=True):
   404	                    why = f"which neither the script nor {test} carries on origin/main"
   405	                    fails.append(f'C10 rule sentence names {scr} beside the literal `{lit}`, {why}: "{sent[:60]}…"')
   406	    for sent in sentences:  # C9
   407	        if re.search(r"\b(once|until)\b", sent):
   408	            continue
   409	        for n in set(re.findall(C9_NAMES, sent)):
   410	            probe = n.replace("task-consistency-check ", f"{CHECKER}#").split("#")[0]
   411	            if probe.startswith("scripts/"):
   412	                ok = main_entry(root, probe) is not None
   413	            elif probe.endswith("_EVIDENCE"):
   414	                ok = main_contains(root, probe, ("Makefile", "scripts"))
   415	            else:
   416	                ok = probe == "classes:" and main_contains(root, "^classes:", (".orchestration/learning/mistakes",))
   417	            if not ok:
   418	                why = "it is not on origin/main and the sentence has no landing condition"
   419	                fails.append(f'C9 rule sentence names {n} as present but {why}: "{sent[:70]}…"')
   420	    for r in rows:  # C13, then C11 on the form it found
   421	        d = str(r.get("disposition") or "")
   422	        form = next((f for f in FORMS if d.startswith(f)), None)
   423	        if form is None:
   424	            fails.append(f"C13 disposition is not closed:, residual: or out-of-scope: and a space: {d[:60]}")
   425	            continue
   426	        load = d[len(form) :]
   427	        selector = re.fullmatch(r"([^:]+)::(?:[A-Za-z_]\w*::)?[A-Za-z_]\w*", load)
   428	        _, target, path = path_entry(root, selector[1] if selector else None)
   429	        if form == "closed: " and not (path and normalise_name(path).startswith("tests/") and target is not None):
   430	            fails.append(f"C11 closed: payload is not tests/<path>::<identifier>: {load[:60]}")
   431	        tid_ok = re.fullmatch(r"[A-Za-z0-9][\w.-]*", load)
   432	        owner = path_entry(root, f".orchestration/tasks/{load}.md")[1] if tid_ok else None
   433	        if form == "out-of-scope: " and not (owner is not None and owner.is_file()):
   434	            fails.append(f"C11 out-of-scope: {load[:60]} is not a task under .orchestration/tasks/")
   435	        if form == "residual: " and len(load) < 20:
   436	            fails.append(f"C11 residual: payload is shorter than 20 characters: {load}")
   437	    resolved_names, entries, seen, collisions = [], {}, {}, set()
   438	    for raw in fm.get("allowed_files") or []:
   439	        _, _, a = path_entry(root, raw, fold)
   440	        if a is None:
   441	            continue
   442	        for file in files(root, raw, fold):
   443	            entry = path_entry(root, file, fold)
   444	            name = entry[2]
   445	            if not (match(name, a, fold=fold) or file.is_symlink() and match(name, a, partial=True, fold=fold)):
   446	                continue
   447	            entries[file] = raw, entry
   448	            prior = seen.setdefault(name, file)
   449	            if prior.parts != file.parts:
   450	                collisions.add(name)
   451	                fails.append(
   452	                    f"C12 path collision: {prior.relative_to(root)} and {file.relative_to(root)} normalise to the same key"
   453	                )
   454	    for file, (raw, (_, target, name)) in entries.items():
   455	        _, scope_target, a = path_entry(root, raw, fold)
   456	        if target is None:
   457	            fails.append(f"C12 confinement: {file.relative_to(root)}")
   458	            continue
   459	        resolved = path_entry(root, target, fold)[2]
   460	        resolved_names.append(resolved)
   461	        exempt = any(
   462	            file.relative_to(root).as_posix().startswith(e)
   463	            and resolved.startswith(fold(e))
   464	            and confined(root / e, target) is not None
   465	            for e in ("tests/fixtures/", own_dir)
   466	        )
   467	        named = name not in collisions and (
   468	            not re.search(r"[*?\[]", raw)
   469	            and scope_target is not None
   470	            and confined(scope_target, target) is not None
   471	            or any(
   472	                key == name and other is not None and other.exists() and target.samefile(other)
   473	                for _, other, key in row_paths
   474	            )
   475	        )
   476	        applied = resolved in map(fold, ("AGENTS.md", "Makefile")) or resolved.endswith(APPLIED)
   477	        applied = applied or any(
   478	            pathlib.PurePosixPath(d) in pathlib.PurePosixPath(resolved).parents for d in APPLIED_DIRS
   479	        )
   480	        applied = applied or match(resolved, ".claude/skills/*/SKILL.md", fold=fold)
   481	        if file.is_symlink() and file.is_dir() or target.is_file() and applied and not exempt and not named:
   482	            fails.append(f"C12 the scope {a} matches unsafe or unnamed {file.relative_to(root)}")
   483	    premises = fm.get("premises") or []
   484	    # Only the caller's dispatched-byte digest authorizes C14; branch bytes supply no authority.
   485	    if premises and hashlib.sha256(data).hexdigest() != premises_sha:
   486	        print(f"{p.name}: warning: {UNTRUSTED}", file=sys.stderr)
   487	        premises = []
   488	    for pre in premises:  # C14
   489	        cmd, want = str(pre.get("command") or ""), str(pre.get("output") if pre.get("output") is not None else "")
   490	        got, code, err = rerun(cmd, root)
   491	        # Runs of whitespace collapse (BSD wc pads its counts; YAML's |- drops the final newline).
   492	        if got is None or code or " ".join(got.split()) != " ".join(want.split()):
   493	            fails.append(err if got is None else f"C14 premise output differs from its rerun: {cmd}")
   494	    mine = fm.get("invariants") if isinstance(fm.get("invariants"), dict) else {}
   495	    present = shown is not None
   496	    if design and not present:
   497	        fails.append(f"C15 design {design} is not on canonical main")
   498	    elif present:  # the design's assignment fixes the ids; a design task compares its own definitions
   499	        canon, assigned = dfm.get("invariants") or {}, dfm.get("implementing_tasks")
   500	        ids = (assigned.get(tid) or []) if isinstance(assigned, dict) and fm.get("kind") != "design" else None
   501	        if ids is not None:
   502	            fails += [f"C15 invariant {k} that {design} assigns to {tid} is missing" for k in ids if k not in mine]
   503	            fails += [f"C15 invariant {k} is not one {design} assigns to {tid}" for k in mine if k not in ids]
   504	        bad = [k for k, v in mine.items() if (ids is None or k in ids) and canon.get(k) != v]
   505	        fails += [f"C15 invariant {k} is not byte-equal to {design} on origin/main" for k in bad]
   506	    if fm.get("security") is True and (
   507	        any(match("scripts/orchestrator", a, partial=True, fold=fold) for a in allowed)
   508	        or any(fold(n).startswith(fold("scripts/orchestrator/")) for n in resolved_names)
   509	    ):
   510	        if not re.search(r"5\.14[^\n]*(?:reference|参照)", body, re.IGNORECASE):
   511	            fails.append("C16 design 5.14 must apply by reference")
   512	        item_rows = [re.findall(r"5\.14\s+item\s+(\d+)", r.get("control") or "", re.IGNORECASE) for r in rows]
   513	        for i in range(11):
   514	            count = sum(items.count(str(i)) for items in item_rows)
   515	            if count != 1 or any(len(items) > 1 for items in item_rows):
   516	                fails.append(f"C16 item {i}: count {count}; exactly one occurrence and one item per row required")
   517	    return fails
   518	
   519	
   520	def main():
   521	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   522	    parser.add_argument("--root", type=pathlib.Path, help="the repository (default: the first file's git toplevel)")
   523	    parser.add_argument("--premises-sha", metavar="sha256", help="the dispatched file's sha256; C14 runs only for it")
   524	    parser.add_argument("tasks", nargs="+", type=pathlib.Path, metavar="task.md")
   525	    args = parser.parse_args()
   526	    if args.root is None:
   527	        start = args.tasks[0].parent.resolve()
   528	        args.root = next(p for p in (start, *start.parents) if (p / ".git").exists())
   529	    top = git(args.root, "rev-parse", "--show-toplevel")
   530	    if top.returncode:
   531	        parser.error(f"{args.tasks[0]} is not in a git checkout; pass --root")
   532	    args.root = pathlib.Path(top.stdout.strip())
   533	    rc = 0
   534	    for p in args.tasks:
   535	        fails = check(p, args.root, args.premises_sha)
   536	        print(f"{p.name}: {'FAIL' if fails else 'OK'}", *fails, sep="\n  ")
   537	        rc |= bool(fails)
   538	    return rc
   539	
   540	
   541	if __name__ == "__main__":
   542	    sys.exit(main())
    def test_canonical_path_pipeline_rejects_normalised_collisions(self):
        nfc, nfd = "scripts/caf\u00e9.py", "scripts/cafe\u0301.py"
        first = self.put(nfd, "applied\n")
        rows = [dict(control=n, disposition=RESIDUAL) for n in ("scripts/tool.py", nfd)]
        self.task(allowed=["scripts/**"], extra=rows)
        self.assertEqual(self.check()[0], 0)
        self.task(allowed=["scripts/**", nfd], extra=rows)
        self.assertEqual(self.check()[0], 0)
        targets = [self.put(f"tests/fixtures/target-{i}.py", "fixture\n") for i in range(2)]
        for destinations in (targets, [targets[0]] * 2):
            prefix = (
                "import os,pathlib,unicodedata;_walk=os.walk;_resolve=pathlib.Path.resolve;_exists=pathlib.Path.exists;_is_file=pathlib.Path.is_file\n"
                f"mapping={dict(zip([str(self.repo / n) for n in (nfc, nfd)], map(str, destinations)))!r}\n"
                "def resolve(p,*a,**k):\n return pathlib.Path(mapping[str(p)]) if str(p) in mapping else _resolve(p,*a,**k)\n"
                f"def walk(*a,**k):\n for folder,dirs,names in _walk(*a,**k):\n  if folder=={str(self.repo / 'scripts')!r}:names=[n for n in names if unicodedata.normalize('NFC',n)!={Path(nfc).name!r}]+{[Path(nfc).name, Path(nfd).name]!r}\n  yield folder,dirs,names\n"
                f"os.walk=walk;pathlib.Path.resolve=resolve;pathlib.Path.exists=lambda p:False if str(p)=={str(self.repo / nfc)!r} else _exists(p);pathlib.Path.is_file=lambda p:False if str(p)=={str(self.repo / nfc)!r} else _is_file(p)"
            )
            self.assertIn("path collision:", self.finding("C12", prefix=prefix))
            if destinations is targets:
                one = prefix.replace(repr([Path(nfc).name, Path(nfd).name]), repr([Path(nfc).name]))
                self.assertNotIn("path collision:", self.finding("C12", prefix=one))
        second = self.put(nfc, "different applied file\n")
        distinct = not first.samefile(second)
        print(f"native-NFC-NFD-distinct={distinct}", flush=True)
        with self.subTest("native two-file collision"):
            if not distinct:
                self.skipTest("observed NFC/NFD samefile alias; modeled collision and one-file control ran")
            out = self.finding("C12")
            self.assertIn("path collision:", out)
            for name in (nfc, nfd):
                self.assertIn(name, out)

    def test_c10_confines_original_unicode_script_paths(self):
        outside = self.put(self.temp / "outside.py", "outside\n")
    def test_security_c12_resolves_original_unicode_path(self):
        benign = self.put("tests/fixtures/ordinary.py", "fixture\n")
        outside = self.put(self.temp / "outside.py", "outside\n")
        (self.repo / "tests/fixtures/cafe\u0301.py").symlink_to(outside)
        nfc = self.repo / "tests/fixtures/caf\u00e9.py"
        self.task(allowed=["tests/fixtures/**"])
        # Model distinct Unicode spellings even on normalization-insensitive hosts.
        prefix = (
            "import pathlib,os,unicodedata;_resolve=pathlib.Path.resolve;_walk=os.walk\n"
            f"def resolve(p,*a,**k):\n return pathlib.Path({str(benign)!r}) if str(p)=={str(nfc)!r} else _resolve(p,*a,**k)\n"
            "def walk(*a,**k):\n for folder,dirs,names in _walk(*a,**k):\n  yield folder,dirs,[unicodedata.normalize('NFD',n) for n in names]\n"
            "pathlib.Path.resolve=resolve;os.walk=walk"
        )
        self.assertIn("confin", self.finding("C12", prefix=prefix))

    def test_security_c12_rejects_internal_directory_alias(self):
        self.put("tests/fixtures/data.txt", "fixture\n")
        alias = self.repo / "tests/fixtures/alias"
        alias.symlink_to(self.repo / "scripts", target_is_directory=True)
        for scope in ("tests/fixtures/**", "tests/fixtures/alias"):
            self.task(allowed=[scope])
            self.assertIn("alias", self.finding("C12"))
        row = dict(control="tests/fixtures/alias", disposition=RESIDUAL)
        self.task(allowed=["tests/fixtures/**"], extra=[row])
        self.finding("C12")
        alias.unlink()
        self.task(allowed=["tests/fixtures/**"])
        self.assertEqual(self.check()[0], 0)

    def test_security_c16_rejects_multi_item_rows(self):
        self.put("scripts/orchestrator/tool.py", "fixture\n")
        items = [dict(control=f"5.14 item {i}: reference", disposition=RESIDUAL) for i in range(11)]
        concrete = dict(control="scripts/orchestrator/tool.py", disposition=RESIDUAL)
        allowed = ["scripts/orchestrator/*.py"]
        for pair, trim in (((0, 1), 0), ((0, 0), 0), ((11, 12), 0), ((0, 1), 2)):
            combined = dict(control=" and ".join(f"5.14 item {i}" for i in pair), disposition=items[0]["disposition"])
            self.task(allowed=allowed, extra=[concrete, *items[trim:], combined], security=True, body=REFERENCE)
            out = self.finding("C16")
            if pair == (0, 0):
                self.assertIn("item 0: count 3", out)

    def test_exempt_case_alias_to_applied_file_is_finding(self):
        self.put("Tests/Fixtures/agent.py", "applied\n")
        self.task(allowed=["tests/fixtures/**"])
        prefix = "import os;os.path.normcase=lambda value:os.fspath(value).casefold()"
        self.assertIn("agent.py", self.finding("C12", prefix=prefix))
        alias = self.repo.with_name(self.repo.name.swapcase())
        native = alias.exists() and alias.samefile(self.repo)
        print(f"native-case-insensitive={native}", flush=True)
        if native:
            self.assertIn("agent.py", self.finding("C12"))

    def test_c12_classifies_backslash_filenames_from_resolved_ancestry(self):
        weird = self.put("scripts/evil\\name", "applied\n")
        self.put("scripts/named", "named applied control\n")
        rows = [dict(control=n, disposition=RESIDUAL) for n in ("scripts/tool.py", "scripts/named")]
        self.task(allowed=["scripts/**"], extra=rows)
        self.assertIn("scripts/evil\\name", self.finding("C12"))
        weird.unlink()
        self.assertEqual(self.check()[0], 0)

    def test_c12_covers_applied_skill_instructions(self):
        self.put(".claude/skills/example/SKILL.md", "instructions\n")
        self.task(allowed=[".claude/skills/**"])
        self.assertIn("SKILL.md", self.finding("C12"))

    def test_c16_requires_reference_and_all_item_rows(self):
  sandbox:
    enabled: true
    # Two-stage rollout: warn and run unsandboxed while bwrap/socat are missing;
    # flip to true only after live E2E.
    failIfUnavailable: false
    autoAllowBashIfSandboxed: true
    allowUnsandboxedCommands: true
    # T39 recorded Herdr PermissionDenied on 2026-10-01; T130 added $HOME/.config/herdr/herdr.sock to allowUnixSockets; the orchestrator sent sandboxed Bash messages 2827 and 2830 on 2026-10-20.
    excludedCommands: []
    linux_excluded_commands: []
    filesystem:
      # Rendered into sandbox.filesystem.allowWrite after the Codex writable
      # roots. ~/.cache/uv: every `uv run` target (make unit-test,
      # validate-agent-assets, render-check) needs the uv cache writable; a
      # filesystem relaxation limited to that directory (T39 live E2E leg 1).
      extra_allow_write:
        - ~/.cache/uv
        - ~/.local/state/mise
        - ~/.local/share/uv
      darwin_extra_allow_write:
        - ~/Library/Caches/mise
    network:
      allowedDomains:
        - github.com
        - api.github.com
        - uploads.github.com
        - objects.githubusercontent.com
        - codeload.github.com
        - pypi.org
        - files.pythonhosted.org
      # macOS certificate validation; the generator omits Mach services on Linux.
      allowMachLookup:
        - com.apple.trustd.agent
      # macOS only: Claude Code ignores this list on Linux and WSL2, where the
      # seccomp filter can't inspect socket paths. The Claude messaging socket
      # (CLAUDE_CODE_MESSAGING_SOCKET, a per-process path set at runtime) cannot
      # be listed without a glob, so it is not.
      allowUnixSockets:
        - ~/.config/herdr/herdr.sock
      # The allow-all Unix socket switch is deliberately not set: with a
      # docker-group user or a reachable `systemd --user` bus it turns the
      # auto-approved sandbox into an escape (T44 r2, operator 2026-10-01).
  hooks:
    enforce_uv_hook: ~/.claude/hooks/enforce-uv.sh
    format_edited_files_hook: ~/.claude/hooks/format-edited-files.py
    project_map_reload_hook: ~/.claude/hooks/project-map-reload.sh
    permission_request:
      command: ~/.local/bin/common/permgate claude
          fetch-depth: 0
          # The base branch's tip at run time: the event's recorded base sha can lag the branch (on PR #420 it was the
          # head's fork point, from before this verifier; ci:39185982423:1). The pull request cannot move this branch.
          ref: refs/heads/${{ github.base_ref }}
          persist-credentials: false
      - uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
        with:
          enable-cache: false
      - name: Fetch the pull request's head as data
        env:
          PR_NUMBER: ${{ github.event.pull_request.number }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
        run: |
          git fetch --no-tags origin "refs/pull/${PR_NUMBER}/head:refs/regime/pr-head"
          test "$(git rev-parse refs/regime/pr-head)" = "${HEAD_SHA}"
      - name: Check the pull request with the base's verifier
        env:
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          # the checker's gh api reads (canonical-main SHA, design bytes, C8/C9) need authentication on a fresh
          # runner; the job's contents: read token can only read this repository's contents (P1-17)
          GH_TOKEN: ${{ github.token }}
        run: uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "$(git rev-parse HEAD)" --head "${HEAD_SHA}"

**Summarizing review findings**
**Evaluating executable path handling**
exec
/bin/zsh -lc "rg -n '("'^##|binding|sandbox|residual|GIT_|closed|API|PATH|mise)'"' .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md | tail -60; git show c439b63c:.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md | tail -34; git diff -- .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md; shasum -a 256 .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md" in ~/Workspace/dotfiles
 succeeded in 89ms:
181:      "class": "excluded-command-trusts-sandbox-context",
185:      "class": "excluded-command-trusts-sandbox-context",
193:      "class": "hash-binding",
260:- 2026-10-20T01:10:03Z: C-80 round 1 (`…-text-security-1368f71.md`) `Verdict: incorrect`: P1 the unchanged dispatch parent preserves PATH and runs PATH-selected mise/uv before the checker (the sanitised execution boundary cannot be established by the checker itself); P1 the shared ~/.cache/uv is selected by the unchanged dispatch (item 9 private cache); P1 the dispatch prerequisite trusts local origin/main and git cat-file (read it through the fixed repository API at the authenticated sha); P2 C6 compares design_review.receipt against the mutable local design (validate against the canonical bytes; forged-local-receipt regression); P2 exemptions classified lexically can alias an applied file through an in-repository symlink or a case alias (resolved-target classification, negative fixtures). Disposition: the same pattern as the P1-6 slice re-plan: the checker slice claims no execution-boundary closure (rows for items 2 and 9 residual with their owners: trusted-entrypoint-binding-a01 and loop-limits-a01 for dispatch.sh, ci-efficiency-followup-a04 for the resolver and private cache) and fixes the three text-level findings; amendment 1 via the review profile; C-92 budget 1 of 3.
261:text-security:1368f71:1	excluded-command-trusts-sandbox-context
262:text-security:1368f71:2	excluded-command-trusts-sandbox-context
264:text-security:1368f71:4	hash-binding
266:- 2026-10-20T01:20:28Z: amendment 1 (`redesign/p112-a05-checker-r2.md`) installed: 249 lines, 4 files, checker OK; no execution-boundary claim (items 2 and 9 residual with the owners loop-limits-a01, trusted-entrypoint-binding-a01, ci-efficiency-followup-a04); the dispatch prerequisite read through the fixed repository API at the authenticated sha; C6 against the canonical bytes; resolved-target exemption classification. C-80 round 2 running (budget 2 of 3 when it returns).
267:- 2026-10-20T01:24:51Z: C-80 round 2 (`…-text-security-cd37b74.md`) `Verdict: correct` (33 threat rows; C6/C15 bound to one canonical snapshot; resolved-target exemptions; parent execution and shared cache deferred to named owners). Text ready for a Codex seat (a012 holding); dispatch prerequisite: boundary #435 merged (design 5.14 on main), checked through the repository API.
269:- 2026-10-20T03:20:29Z: dispatch prerequisite met (design 5.14 on main via the API after #435); dispatched to a012 (worker-g); text sha256 9081e41f464c6a1ce202ebcae25799b1d9b3e86e689074dd7acc5b0bcfb780ac.
270:- 2026-10-20T03:25:52Z: a012 PONG `working`: branch tools/task-generator-plan-check-a05-checker from 60a6fb2b (the known packed-refs warning, no repair); task copy 9081e41f…; prerequisite #435 verified through the API (pinned design sha256 30864249…); the a04 audit and re-plan read; plan: 16 fixtures red against 7a201eab before the production fixes; caps 400/700; the old branch untouched; loop-limits held.
278:- 2026-10-20T04:21:43Z/04:27:28Z: a012 PONG `blocked`: its repair breaks `tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier` (the module's fixtures write bare `disposition: residual`, which the a05 C13 grammar rejects; full-suite comparison: 6 new failures, all in RegimeCiTest); the file is outside allowed_files and amendments are spent. Disposition (PING `a05-checker-fixture-disposition.txt`, 04:30Z): C13 stays; the fixture migration is the test-only task `dotfiles-T133-regime-ci-fixture-grammar-a01` (a009); a012 pushes, runs CI and sends RESULT stating the one out-of-scope red; the chain update-branches #417 after that task merges.
286:- 2026-10-20T06:09:05Z: a012 PONG `blocked`: the runtime rebuild recreated the parent-bin directory but `uv … python install 3.12.15` cannot download (restricted network: DNS error to github.com); the text requires the 3.12 floor and the current interpreter. Disposition (2026-10-20T06:16Z): the orchestrator installed the 3.12 floor on the host with the tool manager (`mise install python@3.12` -> `$HOME/.local/share/mise/installs/python/3.12.15/bin/python3.12`, Python 3.12.15, sha256 prefix 3274dde21f976765, the same python-build-standalone archive the worker's uv named; machine-hygiene exemption, no repository file changed: `git status` of tracked files unchanged); PING `a05-checker-python312-disposition.txt`: bind it by absolute path, rerun the proofs, commit, push, CI, RESULT.
287:- 2026-10-20T06:31:07Z: a012 PONG `blocked`: all work committed (head cedc7f5f: the R4 correction; source 397/400, tests 562; 29 modules green on 3.12 and 3.15 with the host's 3.12.15; 24/24 mutants; selected-tree assets clean) but `git push` fails inside its sandbox (`Could not resolve host: github.com`). Root cause: the rendered Codex manifest sets `sandbox_workspace_write.network_access = false` (agent-config.yaml:115 -> ~/.codex/standard.config.toml:26, unchanged since 10-18), contrary to design 5.14 item 10; the pushes of 05:05-05:09Z succeeded before the Codex app-server daemon restarted at ~05:21Z, after which the setting is enforced. Interim (2026-10-20T06:34Z, D-024-36): the orchestrator transported the committed head (`git push https://github.com/mryfmo/dotfiles.git cedc7f5f…:refs/heads/tools/task-generator-plan-check-a05-checker`, declared interim-integration exemption, no commit authored); PING `a05-checker-push-transport.txt` asks for the RESULT on cedc7f5f.
290:## Lineage rows carried from dotfiles-T133-task-generator-plan-check-a04
335:- 2026-10-20T06:43:12Z: security-profile review of cedc7f5f (`…-security-cedc7f5.md`) `Verdict: incorrect`, three P2 on scripts/orchestrator/task-consistency-check.py: (1) :420 NFC normalisation changes the filename before the confinement check (an escaping `cafe<U+0301>.py` symlink is checked as `café.py` and can receive the fixture exemption); (2) :440 an internal directory symlink (`tests/fixtures/alias -> scripts/`) passes confinement but escapes coverage (traversal skips directory links; the condition checks files only); (3) :469 a row naming two design items passes C16 while contributing to neither count. The other closed controls match; the GitGuardian digest matched the synthetic token. CI on cedc7f5f (run 39381147120): only the six RegimeCiTest reds remain per Linux job (the R4 lint is green). ACCEPTANCE `status=revise round=1` (2026-10-20T06:45Z, `a05-checker-revise1.txt`): one red-then-green test per finding; commit locally and PONG the head (the orchestrator transports it, D-024-36); worker fix round 1 of 2.
All production changes are in the one allowed checker. The cap attribution (amendment 1, 2026-10-20T08:4xZ) is a05's 396 changed source lines at 06ffefbc, plus the pipeline draft's measured +24 = 420, plus the two independent-review repairs measured by the worker at +22 (directory intent kept in the comparison keys; the original C10 path extracted before resolution) = 442, with headroom to 450; the test cap 720 covers the measured 700 plus the two regressions those repairs add; no further cap increase is authorized.

Count additions plus deletions for both source and tests, as regime-ci does. The held draft's tests measured 704 changed lines before and 700 after the repairs the worker made; the two review regressions fit within 720, so no control is dropped to make room.
Paste the complete numstat, `git diff --name-only 60a6fb2b...<head40>`, per-file arithmetic and both totals in measure.md and RESULT. Do not hide runtime code in artifacts, remove defenses or change a lint baseline to fit.

The whole authored file, including its empty Checks block, is at most 260 lines and has exactly four allowed_files entries. The worker never edits the orchestrator's Checks content; a populated dispatch block is separately identified as appended metadata, never silently excluded from a claimed count.

Run the checker on dispatched bytes and record C14's warning without `--premises-sha`; authorized fixtures use their supplied trusted digest. Never invent dispatch authority from branch bytes or add shell support for authoring probes.

## Completion and evidence

Worker Playbook step 4 applies with this host's measured facts: Codex seats run without network since the daemon restart (D-024-36), so the worker commits locally, PONGs the full head, and the orchestrator transports it to PR #440 and reads CI for the worker; every other command runs inside the sandbox, and any refused command is reported as `AGMSG-PONG v1 status=blocked` with exact command, exit, output and boundary.

Do not retry a refusal through another tool, broader permission or sandbox escape. An orchestrator transport or CI read is not worker permission to leave the sandbox. Record unavailable live API validation honestly and retain local fake-API controls.

Commit report.md, validation.md, sandbox.md, learning.md, autoskill.md (status or not-used), measure.md, the byte-identical task.md and worker review evidence under this task's directory before RESULT. Verify with `git ls-files` that no required evidence remains untracked; this overrides generic untracked-artifact handoff. Codex plan/todo/learn worklogs remain uncommitted.

Use agent-side Crit data and a worker receipt in the allowed directory, with resolved records and the receipt's review_surface/reviewer/review_source/review_outcome binding; no browser, publication or human review request. Run `make require-crit-review` with the required evidence. Retain INV-6/S1 lineage accounting; repeated finding classes require a recorded re-plan, not private patch rounds.

The orchestrator transports every new committed head, checks final-head CI and performs Worker Playbook's bounded Bot procedure for the worker, returning exact observations. Fresh applicable CI follows an evidence-only push too. Keep the existing PR's English title/body current through the orchestrator; the worker never merges or edits canonical acceptance, decision or plan records.

Send `AGMSG-RESULT v1 status=ready_for_review` only after required checks pass. Include full head/base, branch, PR #440, task-copy SHA256, changed-file inventory, retained predecessor directory, final numstat/totals, selectors, historical and new red/green counts, mutation outcomes, CI/Bot observations, proposed feedback dispositions and every artifact path. Report `cost:` with observed figures or `n/a`.

After final-head CI and the required security review, the orchestrator follows Orchestrator Playbook step 10: complete feedback sweep, dispositions, task audit, acceptance record and gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE`. Neither a05 review nor previous CI approves this head.

Deferred checks and changes: generator, plan checker, workflows, dispatch/resolver implementation, deployment and local Bats.
Residual risk: unchanged parent execution, shared cache, credentials and same-UID interference remain; checker fixtures establish no host isolation.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T08:39Z before send 2 (amendment 1, the cap) to a012: the measured repair (source 442, tests 700; a012 PONG 08:37:40Z) exceeded 440, so the cap is 450 source / 720 tests with the attribution stated in the Check (396 + 24 + 22 = 442); nothing else changed; previous_sha256 90ca0ae9563df4b352dfb26c6b6aa60132386e15ce9ff50bcf998a43097a12e6; C-80 verdict and pre-send results follow in the AGMSG-TASK note
PR #440 continues on tools/task-generator-plan-check-a05-checker from head 06ffefbc with your uncommitted pipeline draft as this round's content (source cap 450 = 396 + 24 pipeline + 22 review repairs = 442 with headroom; tests 720); the Codex seats have no network (D-024-36): commit locally, PONG the head, the orchestrator transports it and reads CI; the six RegimeCiTest reds stay until #441 merges; task SHA256 in the AGMSG-TASK line, computed over these final bytes
```
922292d32c9505b79beb3e9637b3b13635e6c5ca322e6b6c58235022f9dcfbb2  .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md

**Assessing safe test execution**
**Analyzing interpreter and executable handling**
**Summarizing final review points**
**Assessing risk control gaps**
codex
The eight requested fixes address the cited checker findings, and the inherited Git child environment removes `GIT_*` overrides. Two issues remain: the canonical-read closure lacks a trusted `gh` binding, and the cache refusal has no repair dependency for callers that omit the variable. The `Checks` section is also still empty, so these bytes cannot serve as the final populated review anchor required by the task.
**Verifying environment and cache setup**
exec
/bin/zsh -lc "sed -n '20,65p' scripts/orchestrator/regime-ci.py; rg -n 'UV_CACHE|CHECKER_RUN|env|checker' tests/unit/test_regime_ci.py | head -65; sed -n '1,120p' tests/unit/test_regime_ci.py; sed -n '160,200p' Makefile; rg -n 'CHECKER_RUN|UV_CACHE' scripts/orchestrator/regime-ci.py" in ~/Workspace/dotfiles
 succeeded in 91ms:
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("regime-ci: needs pyyaml: run with uv run --no-project --with pyyaml")
    sys.exit(2)

CHECKER = "scripts/orchestrator/task-consistency-check.py"
# --no-config: a uv.toml or pyproject.toml the pull request adds cannot steer this run
CHECKER_RUN = ["uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I", CHECKER]
RUNS = (CHECKER, "scripts/orchestrator/regime-ci.py", ".github/workflows/regime.yml")
TOKEN_LIKE = re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}")


class GitError(Exception):
    pass


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)


def listed(root, *args):
    """Return the NUL-separated output of a git listing command, or raise GitError: no listing passes by being empty."""
    out = git(root, *args, "-z")
    if out.returncode:
        raise GitError(f"git {' '.join(args)} failed: {out.stderr.decode(errors='replace').strip()[:200]}")
    return [item for item in out.stdout.decode().split("\0") if item]


def show(root, head, path):
    """Return the bytes of path at head, or None when head has no such file."""
    out = git(root, "show", f"{head}:{path}")
    return out.stdout if out.returncode == 0 else None


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def token(text, name):
36:        "workflow and interpreter or environment inputs",
49:SKIPPED = f"regime-ci: warning: {T}: checker skipped: the copy is unverifiable, and the base's checker reads only the base's text"
55:        env = {k: v for k, v in os.environ.items() if k != "GITHUB_HEAD_REF"}
56:        self.env = env | GIT_ENV | {"GITHUB_HEAD_REF": "tools/t1"}
61:            cmd, cwd=self.repo, env=self.env, check=True, capture_output=True, text=True
75:        """A base commit (the checker, the dispatched text), then a code commit and an evidence commit on a branch.
78:        `task_copy` as result.txt's token, `checker` as the base's checker, `base` as more base files, `branch` as the
86:        base = {CHECKER: more.get("checker") or (ROOT / CHECKER).read_text(), "README": "base\n"} | more.get("base", {})
89:        self.git("update-ref", "refs/remotes/origin/main", "HEAD")  # the checker's C8 to C10 probe origin/main
116:    def regime(self, head=None, **env):
119:            cmd, cwd=self.repo, env=self.env | env, capture_output=True, text=True, timeout=120, check=False
123:        # Bot P1 4308651010 and 4308651011 (a02 items 5, 6): the head rewrites the verifier and the checker into programs
125:        # verifier and checker still decide, the checkout stays at the base, and no head program runs.
148:    def test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker(self):
149:        # Worker review P0 of bcbd6949: the checker's C10 passes a backticked literal of the text to `git grep`, so a
150:        # literal that is a git option runs a command; the base's checker reads only the base's dispatched text.
162:                    self.assertIn(f"regime-ci: warning: {T}: checker skipped: the copy is unverifiable", result.stdout)
257:        self.assertEqual(({"HEAD_SHA": head} | token, head), (verify["env"], fetch["env"]["HEAD_SHA"]))
305:            "checker": (
309:            "checker exit": (
310:                {"checker": 'print("task.md: OK")\nraise SystemExit(1)\n'},
313:            "checker crash": ({"copy": crash, "dispatched": crash}, "no verdict (exit 1)"),
324:    def test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config(self):
325:        # --no-config: a .python-version (or uv.toml) in the checkout cannot steer the checker's uv run
343:        self.git("switch", "-q", "pr")  # a checkout at the head would run the head's verifier and checker
347:            env=self.env,
364:        # The checker's C1 compares task_id with the file name, `task` for every copy; regime-ci checks the directory.
427:    def record_checker(self, rc=0):
428:        # a fake base checker that records its argv and environment in the fixture repository's .git, then answers `rc`
432:            "(root / '.git' / 'checker.json').write_text(json.dumps({'argv': sys.argv, 'env': dict(os.environ)}))\n"
437:        # P1-17: the checker inherits regime-ci's environment, so GH_TOKEN reaches it exactly when regime-ci holds it
438:        self.env = {k: v for k, v in self.env.items() if k not in ("GH_TOKEN", "GITHUB_TOKEN")} | {"PROBE_KEPT": "1"}
439:        self.build(checker=self.record_checker())
445:                env = json.loads((self.repo / ".git" / "checker.json").read_text())["env"]
446:                self.assertEqual(given, {k: env[k] for k in names if k in env})
447:                self.assertEqual("1", env.get("PROBE_KEPT"))  # inheritance, not an allowlist
453:                self.build(checker=self.record_checker(rc))
455:                record = json.loads((self.repo / ".git" / "checker.json").read_text())
457:                self.assertEqual(tokens, {k: record["env"].get(k) for k in tokens})  # present in the child
461:    def test_regime_ci_redacts_tokens_in_checker_diagnostics(self):
462:        # security review of a8c03fae: a checker that echoes a token must not leak it through regime-ci's diagnostic
463:        secret, literal = "gho_fixture_secret_token_value", "ghp_" + "Z" * 36  # an env value and a token-like literal
467:                self.build(checker=echo + f"sys.exit({rc})\n")
479:        self.assertEqual(["${{ github.token }}"], [s.get("env", {}).get("GH_TOKEN") for s in verify])
"""Exercise regime-ci.py on temporary repositories (a base with the dispatched text, a head with its copy) and regime.yml."""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = "scripts/orchestrator/task-consistency-check.py"
VERIFIER = "scripts/orchestrator/regime-ci.py"
UV = [
    shutil.which("uv") or "uv",
    "run",
    "--no-config",
    "--no-project",
    "--with",
    "pyyaml",
    "python",
    "-I",
]  # as regime.yml
T = "t1-a01"
RESIDUAL = '"residual: the fixture row is test data for this control"'
ROWS = "".join(
    f"  - control: {name}\n    disposition: {RESIDUAL}\n"
    for name in (
        "the PR edits src/tool.sh",
        "the PR edits tests/unit/test_tool.py",
        f"the evidence under .orchestration/{T}/",
        "task metadata",
        "metadata separators",
        "in-process effects",
        "workflow and interpreter or environment inputs",
        "new or renamed scripts",
        "orchestrator effect merge",
        "orchestrator effect update-branch",
        "orchestrator effect forced worker removal",
    )
)
TASK = (
    f"---\nformat: 2\ntask_id: {T}\nkind: code\nsecurity: false\nallowed_files:\n  - src/tool.sh\n"
    f"  - tests/unit/test_tool.py\n  - .orchestration/{T}/**\nthreat_table:\n{ROWS}premises: []\n---\n\n# {T}\n\n"
    "## Check\n\nat most 3 changed lines outside `tests/` and `.orchestration/`, 2 under `tests/`.\n"
)
CODE = {"src/tool.sh": "a\nb\nc\n", "tests/unit/test_tool.py": "x = 1\ny = 2\n"}
SKIPPED = f"regime-ci: warning: {T}: checker skipped: the copy is unverifiable, and the base's checker reads only the base's text"
GIT_ENV = {f"GIT_{role}_{k}": v for role in ("AUTHOR", "COMMITTER") for k, v in (("NAME", "t"), ("EMAIL", "t@t"))}


class RegimeCiTest(unittest.TestCase):
    def setUp(self):
        env = {k: v for k, v in os.environ.items() if k != "GITHUB_HEAD_REF"}
        self.env = env | GIT_ENV | {"GITHUB_HEAD_REF": "tools/t1"}

    def git(self, *args):
        cmd = ["git", "-c", "commit.gpgsign=false", *args]
        return subprocess.run(
            cmd, cwd=self.repo, env=self.env, check=True, capture_output=True, text=True
        ).stdout.strip()

    def commit(self, files, message):
        for rel, text in files.items():  # None deletes the file
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).unlink() if text is None else (self.repo / rel).write_text(text)
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD")

    def build(
        self, copy=TASK, dispatched=TASK, code=None, precheck_head=None, precheck_token=None, evidence=True, **more
    ):
        """A base commit (the checker, the dispatched text), then a code commit and an evidence commit on a branch.

        more: `late` files committed after the code commit precheck.json names, `precheck_doc` as precheck.json's text,
        `task_copy` as result.txt's token, `checker` as the base's checker, `base` as more base files, `branch` as the
        head branch; precheck_head "side" names a commit on another branch. The base also holds the verifier, the
        checkout returns to the base, and the base's verifier runs against the head commit (a02).
        """
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name).resolve()
        self.git("init", "-q", "-b", "main")
        base = {CHECKER: more.get("checker") or (ROOT / CHECKER).read_text(), "README": "base\n"} | more.get("base", {})
        base |= {VERIFIER: (ROOT / VERIFIER).read_text()}
        self.commit(base | ({f".orchestration/tasks/{T}.md": dispatched} if dispatched else {}), "base")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")  # the checker's C8 to C10 probe origin/main
        if precheck_head == "side":
            precheck_head = self.commit({"side.txt": "side\n"}, "side")
            self.git("reset", "-q", "--hard", "HEAD~1")
        self.git("switch", "-q", "-c", more.get("branch", "pr"))
        code_head = self.commit(CODE if code is None else code, "code")
        if "late" in more:
            self.commit(more["late"], "a change after the precheck")
        if evidence:
            pre = more.get("precheck_doc") or json.dumps({"head": precheck_head or code_head})
            token = precheck_token or hashlib.sha256(pre.encode()).hexdigest()
            copy_token = more.get("task_copy") or hashlib.sha256(copy.encode()).hexdigest()
            result = f"AGMSG-RESULT v1 task_id={T} precheck={token} task_copy={copy_token}\n"
            files = {f".orchestration/{T}/task.md": copy}
            if precheck_head != "absent":
                files |= {f".orchestration/{T}/precheck.json": pre, f".orchestration/{T}/result.txt": result}
            self.commit(files, "evidence")
        self.head = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        return self.regime()

    def head_commit(self, files, message):
        """Commit on the head branch and return the checkout to the base."""
        self.git("switch", "-q", "pr")
        self.head = self.commit(files, message)
        self.git("switch", "-q", "main")

    def regime(self, head=None, **env):
        cmd = [*UV, str(self.repo / VERIFIER), "--base", "main", "--head", head or self.head, "--root", str(self.repo)]
        return subprocess.run(
            cmd, cwd=self.repo, env=self.env | env, capture_output=True, text=True, timeout=120, check=False
        )
	@if [ -f home/dot_local/bin/common/executable_herdr-agents ]; then \
		bash home/dot_local/bin/common/executable_herdr-agents --bootstrap-agmsg "$(CURDIR)"; \
	else \
		echo "Herdr agents source helper not found; skipping agmsg bootstrap."; \
	fi

.PHONY: watch
watch:
	DOTFILES_DEBUG=1 watchexec -- chezmoi apply --verbose

.PHONY: reset
reset:
	chezmoi state delete-bucket --bucket=scriptState

.PHONY: reset-config
reset-config:
	chezmoi init --data=false

.PHONY: format
format:
	shfmt --indent 4 --space-redirects --diff .
	git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check
	git ls-files -z '*.md' | xargs -0 prettier --check

.PHONY: unit-test
unit-test:
	uv run python -m unittest discover -s tests/unit -v

# The index form fails inside the Claude sandbox even while the uv cache holds PyYAML, so a probe picks the cache first.
UV_PYYAML = $(if $(shell uv run --offline --with pyyaml python -c 'import yaml' 2> /dev/null && echo y),uv run --offline --with pyyaml,uv run --with pyyaml)

.PHONY: validate-agent-assets
validate-agent-assets:
	$(UV_PYYAML) scripts/validate-agent-assets.py

.PHONY: check-regime-boundary
check-regime-boundary:
	./scripts/check-regime-boundary.sh

.PHONY: codex-hook-trust
# Re-apply only the managed Codex config files so their modify scripts re-hash the trusted hooks;
34:CHECKER_RUN = ["uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I", CHECKER]
163:        cmd = [*CHECKER_RUN, "--root", root, str(Path(scratch, "task.md"))]

**Assessing test environment risks**
**Finalizing audit report format**
codex
- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:36` The canonical-main closure assumes a genuine `gh`: retained executable selection accepts a PATH-selected regular executable outside the checkout/shim exclusions, while the named tests deliberately supply fake API responses; fixed host/repository arguments cannot authenticate those responses or protect forwarded tokens without trusted executable provenance.

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:103` Restoring mandatory `UV_CACHE_DIR` revives the documented failure for callers that omit it, including regime-ci invocations; caller/workflow changes are excluded and no repair prerequisite is named, so supplied-cache fixtures cannot establish deployable compatibility.

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:134` `Checks` is empty despite lines 120–121 requiring prerequisite API observations and completely populated bytes before the anchor review; approving this digest cannot approve the subsequently populated dispatch text.

📝 まとめ: Reviewed all 51 threat rows and cited context; no files changed. Findings remain input for the orchestrator.

Not checked: future implementation or live deployment; declared parent-execution, shared-cache and same-UID risks remain.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
134,610
- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:36` The canonical-main closure assumes a genuine `gh`: retained executable selection accepts a PATH-selected regular executable outside the checkout/shim exclusions, while the named tests deliberately supply fake API responses; fixed host/repository arguments cannot authenticate those responses or protect forwarded tokens without trusted executable provenance.

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:103` Restoring mandatory `UV_CACHE_DIR` revives the documented failure for callers that omit it, including regime-ci invocations; caller/workflow changes are excluded and no repair prerequisite is named, so supplied-cache fixtures cannot establish deployable compatibility.

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:134` `Checks` is empty despite lines 120–121 requiring prerequisite API observations and completely populated bytes before the anchor review; approving this digest cannot approve the subsequently populated dispatch text.

📝 まとめ: Reviewed all 51 threat rows and cited context; no files changed. Findings remain input for the orchestrator.

Not checked: future implementation or live deployment; declared parent-execution, shared-cache and same-UID risks remain.
Verdict: incorrect
