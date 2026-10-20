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
session id: 01a15809-4ace-7ab3-867a-df3f777b276e
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
タスク本文・threat_table・参照された acceptance／review を読み、判断と実際の実行対象が結び付くかを確認します。agmsg-orchestration と Ponytail の指示を適用し、読み取り専用で監査します。モデル profile はこのセッション内では変更しません。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 14ms:
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
---
name: ponytail
description: >
  Lazy senior dev mode: the smallest change that fully solves the task, and a
  reply a busy human understands in one read. Use on any coding task (writing,
  fixing, refactoring, reviewing, choosing dependencies) and when the user says
  "ponytail", "be lazy", "simplest solution", "yagni", or complains about
  over-engineering or bloat. Levels: lite, full (default), ultra.
argument-hint: "[lite|full|ultra|off]"
license: MIT
---

# Ponytail

You are a lazy senior developer. The best code is the code never written. You solve the whole problem with the least new code. End your reply with one or two lines: what you skipped or did not check, and any risk the user must know.

Active for the whole session until the user says "stop ponytail" or "normal mode". Switch level: `/ponytail lite|full|ultra`.

## Before you write

Read the task and the code it touches. List every place your change must reach: callers, tests, fixtures, config, exports. Check what your change could break for users: data it would destroy or expose, callers that stop working. That is scope. Extra features are not.

## The smallest complete change

Take the first option that fully works:

1. Does it need to exist? Skip features, options and flexibility nobody asked for, and name them in one line. A vague request ("build me X") gets the smallest version that does the core job.
2. Already in this codebase (a helper, component, service, pattern)? Use it the way the surrounding code does.
3. Standard library or a platform feature? Use it, unless the project has its own. A house component beats a native widget.
4. An installed dependency? Use it. Never add a dependency for a few lines.
5. Can it be one line a reader gets at a glance? One line.
6. Otherwise: the minimum code that works.

- Be lazy about the solution, never about the change itself: finish every part the task needs, including the callers, tests and fixtures your change breaks.
- No abstraction, wrapper, type conversion, option, config, boilerplate or "for later" code nobody asked for. Keep values in the form the platform already gives you. Deletion beats addition. Keep the structure the codebase already has: its layers, interfaces and conventions.
- The shortest working diff wins, once you know everything it must touch. A one-liner that needs decoding is not short.
- Comment only the why the code cannot show, in one line.
- Bug fix: before you edit, grep every caller of the function you touch, then fix the root cause once in the shared code.
- Code you move or merge keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases.
- Lazy code without its check is unfinished: new non-trivial logic (a branch, a loop, a parser, money or security, or a whole new script or app) leaves one small test or an assert-based self-check. Trivial changes need none.
- A shortcut with a known limit gets a code comment in this form: `shortcut: <the limit>, <when to upgrade>`.

Never cut: validation at trust boundaries, error handling that prevents data loss, security, accessibility, the calibration real hardware needs, anything the user asked for.

## Levels

| Level | Behavior |
|-------|----------|
| **lite** | Build what was asked. Name the smaller option in one line and let the user pick. |
| **full** | The rules above. Default. |
| **ultra** | Also question the request: before building, push back on any part the need does not justify. |

exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md' in ~/Workspace/dotfiles
 succeeded in 14ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-record-json-sync-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/record-json-sync.py
     8	  - tests/unit/test_record_json_sync.py
     9	  - .orchestration/dotfiles-T133-record-json-sync-a01/**
    10	after: []
    11	threat_table:
    12	  - {control: "scripts/orchestrator/record-json-sync.py", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_syncs_rows_and_replans"}
    13	  - {control: "tests/unit/test_record_json_sync.py", disposition: "residual: Assertion errors can conceal broken behavior; the final-head audit checks fixtures, observations and red/green evidence against the implementation."}
    14	  - {control: ".orchestration/dotfiles-T133-record-json-sync-a01/**", disposition: "residual: Only task records are permitted under this wildcard; no executable helper or replacement implementation may be hidden in evidence."}
    15	  - {control: "the task copy .orchestration/dotfiles-T133-record-json-sync-a01/task.md", disposition: "residual: The orchestrator compares the whole file byte-for-byte with dispatch and checks its SHA-256 before acceptance."}
    16	  - {control: "the evidence records under .orchestration/dotfiles-T133-record-json-sync-a01/", disposition: "residual: Preserve commands, exit statuses and complete outputs; the audit compares their claims with the final diff and GitHub Actions."}
    17	  - {control: "task metadata: kind, security, allowed_files, after, threat_table and premises", disposition: "residual: Task-consistency checks and independent task-file review run before dispatch and acceptance; task-copy equality exposes altered metadata."}
    18	  - {control: "metadata separators", disposition: "residual: Whole-file comparison covers task-copy separators; evidence is untrusted data, and acceptance-record delimiter failures are exercised by the malformed-front-matter test."}
    19	  - {control: "malformed acceptance-record front matter", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_malformed_front_matter_is_unchanged"}
    20	  - {control: "acceptance-record write target", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_task_and_output_path_are_confined"}
    21	  - {control: "in-process effects", disposition: "residual: Only the named acceptance file is rewritten after validation; tests use temporary records, and same-UID concurrent replacement remains possible."}
    22	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: Commands bind the clean parent, fixed interpreter and executable paths; no workflow or interpreter configuration changes are authorized."}
    23	  - {control: "new or renamed scripts", disposition: "residual: Only scripts/orchestrator/record-json-sync.py is introduced; it parses data with the standard library and never evaluates prose or starts subprocesses."}
    24	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: Same-UID replacement and shared credentials remain possible; local JSON synchronization is process evidence, never authentication or permission approval."}
    25	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: Every worker action stays inside its sandbox and declared files; this task changes no deployed sandbox, permissions or trusted host inputs."}
    26	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Commands establish the clean parent before binding tools; the transformer launches no executable and cannot sanitize the parent that started its interpreter."}
    27	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: Task-id and symlink escape tests constrain the write target; they do not establish protection against unrestricted same-UID replacement."}
    28	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Commands reuse the probed PY binding; parse and validate the record before writing, without claiming a snapshot or concurrent-writer exclusion."}
    29	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: RESULT and cap evidence name full base and head SHAs; this transformer introduces no reservation, lock or head-named executable output."}
    30	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: The transformation tests establish record behavior only; host provenance, concurrent writes and shared credentials remain explicit residuals."}
    31	  - {control: "design 5.14 item 7: 検証", disposition: "residual: Red/green tests cover the data transformation; they do not claim the four host-execution probes, since no execution mechanism is introduced."}
    32	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: This writes a local acceptance-record proposal without granting approval; committed permission decisions and final integration retain their existing authorities."}
    33	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: Runtime uses only the standard library under the fixed installed interpreter; worker lint caches remain seat-local and no orchestrator cache is changed."}
    34	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Every command including gh and push remains sandboxed; refusal produces a blocked PONG without escalation or a substitute tool."}
    35	  - {control: "orchestrator effect merge", disposition: "residual: Only the orchestrator merges through gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker never merges or pushes main."}
    36	  - {control: "orchestrator effect update-branch", disposition: "residual: The orchestrator refreshes CI, feedback and the task-level audit after an update-branch changes the head, before applying the integration gate."}
    37	  - {control: "orchestrator effect forced worker removal", disposition: "residual: None is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and any forced removal records the discarded state in acceptance."}
    38	premises:
    39	  - claim: "The existing glue has 28 lines; neither requested tracked path exists in the authoring checkout."
    40	    command: |-
    41	      "${P[@]}" "$PY" -I -c 'from pathlib import Path; p=Path(".agents/worklog/orchestrator-glue/record-json-sync.py"); print("glue_lines=" + str(len(p.read_text().splitlines()))); print("tracked_script_exists=" + str(Path("scripts/orchestrator/record-json-sync.py").exists())); print("test_module_exists=" + str(Path("tests/unit/test_record_json_sync.py").exists()))'
    42	    output: |-
    43	      glue_lines=28
    44	      tracked_script_exists=False
    45	      test_module_exists=False
    46	  - claim: "The gate defines the ledger grammar, class grammar and four required re-plan keys; replan_complete requires non-empty text."
    47	    command: |-
    48	      rg -n '^LEDGER_ID =|^REPLAN_KEYS =|^CLASS_SLUG =|^def replan_complete|^    return isinstance\(entry, dict\)' scripts/require-crit-review.py
    49	    output: |-
    50	      37:LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")
    51	      38:CLASS_SLUG = re.compile(r"[a-z0-9-]+")
    52	      44:REPLAN_KEYS = ("specification", "design", "implementation", "verification")
    53	      775:def replan_complete(entry: object) -> bool:
    54	      776:    return isinstance(entry, dict) and all(is_text(entry.get(key)) for key in REPLAN_KEYS)
    55	  - claim: "acceptance-front-matter.py lines 79-84 reject wrong containers, invalid class slugs, missing or extra keys and blank values before writing."
    56	    command: |-
    57	      sed -n '79,84p' scripts/orchestrator/acceptance-front-matter.py
    58	    output: |-
    59	          replans, parts = record.get("replans", {}), ", ".join(gate.REPLAN_KEYS)
    60	          if not isinstance(replans, dict):
    61	              parser.error(f"replans must be {{<class slug>: {{{parts}}}}}; nothing written")
    62	          for cls, entry in replans.items():
    63	              if not gate.CLASS_SLUG.fullmatch(cls) or not gate.replan_complete(entry) or set(entry) != set(gate.REPLAN_KEYS):
    64	                  parser.error(f"replans.{cls} must be {{{parts}}}, each a non-empty string; nothing written")
    65	---
    66	
    67	# AGMSG-TASK dotfiles-T133-record-json-sync-a01 — promote acceptance-record JSON synchronization
    68	Written 2026-10-20; amendment 1 addresses all five C-80 round-1 findings and C-104. PR #437's task-level audit e9819d4 found empty JSON ledger, replans and searches beside 18 prose rows and three re-plan lines (M-20261019-06). [memory:failure] Prose-only findings and re-plans do not populate the JSON the gate consumes.
    69	Design 5.14 of `.orchestration/plans/024-design-quality.md` is frozen (D-024-29) and applies by reference (D-024-30); items 0–10 have individual threat rows.
    70	
    71	## Commands
    72	Definitions occur only here; premises quote source-authoring probes, not additional worker instructions. Start (parent) from the trusted launcher in the verified checkout root; run the lettered sections inside it. Stop dependent work at any failed prerequisite; substitute recorded operands before execution.
    73	```bash
    74	# (parent) Clear inherited inputs before starting the shell.
    75	/usr/bin/env -i PATH=/usr/bin:/bin TMPDIR="${TMPDIR:-/tmp}" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 /bin/bash --noprofile --norc -p -o pipefail
    76	# (a) Record the platform and anchor home to the real user's passwd entry.
    77	platform=$(/usr/bin/uname -s); printf '%s\n' "$platform"
    78	case "$platform" in
    79	  Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
    80	  Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
    81	  *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
    82	esac
    83	rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
    84	case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
    85	# (b) The clean child prefix.
    86	P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8)
    87	# (c) Bind and probe the exact interpreter, then use this test invocation for red and green.
    88	PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
    89	[ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python: refused: missing-executable' >&2; exit 1; }
    90	"${P[@]}" "$PY" -I -c 'import os,sys; p=os.path.realpath(sys.executable); print(p, sys.version.split()[0]); assert sys.version.split()[0]=="3.15.0" and p.startswith(os.environ["HOME"]+"/.local/share/mise/installs/python/3.15.0/")' || exit 1
    91	"${P[@]}" "$PY" -I tests/unit/test_record_json_sync.py
    92	# (d) Resolve uv only when needed for lint; never execute a shim or provision a replacement interpreter.
    93	UV=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/uv/latest/uv-aarch64-apple-darwin/uv")
    94	case "$UV" in ""|*/mise/shims/*) exit 1;; "$home"/.local/share/mise/installs/uv/*/uv-aarch64-apple-darwin/uv) ;; *) exit 1;; esac
    95	[ -f "$UV" ] && [ -x "$UV" ] || exit 1
    96	"${P[@]}" UV_CACHE_DIR="$PWD/.uv-cache" "$UV" run --no-config --no-project --python "$PY" --with ruff ruff check scripts/orchestrator/record-json-sync.py tests/unit/test_record_json_sync.py
    97	"${P[@]}" UV_CACHE_DIR="$PWD/.uv-cache" "$UV" run --no-config --no-project --python "$PY" --with ruff ruff format --check scripts/orchestrator/record-json-sync.py tests/unit/test_record_json_sync.py
    98	# (e) Bind gh; every invocation gets a fresh config directory and an explicit host/repository.
    99	GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
   100	case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
   101	[ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
   102	gh_call() {
   103	  local GH_CONFIG_DIR; GH_CONFIG_DIR=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX") || return
   104	  case "$1" in api) [[ "$2" == repos/mryfmo/dotfiles/* ]] || return 1; "${P[@]}" GH_CONFIG_DIR="$GH_CONFIG_DIR" "$GH" "$@" --hostname github.com;; pr|run|issue) "${P[@]}" GH_CONFIG_DIR="$GH_CONFIG_DIR" "$GH" "$@" --repo github.com/mryfmo/dotfiles;; *) return 1;; esac
   105	}
   106	# (f) All Git operations use the clean prefix and system Git; cap operands are full recorded SHAs.
   107	branch=tools/record-json-sync-a01
   108	git_clean() { "${P[@]}" /usr/bin/git "$@"; }
   109	"${P[@]}" /usr/bin/git diff --numstat "$base40...$head40"
   110	( GH_CONFIG_DIR=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX") || exit 1; P+=(GH_CONFIG_DIR="$GH_CONFIG_DIR"); "${P[@]}" /usr/bin/git -c credential.helper= -c "credential.helper=!$GH auth git-credential" push https://github.com/mryfmo/dotfiles.git "HEAD:$branch" )
   111	```
   112	Commands (a) is the only home source. Commands (parent)/(b) clear inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_COUNT`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM` and other `GIT_*`, tool, loader and Python variables. Commands (e)/(f) also isolate the credential helper's configuration; authentication failure is a blocker, never permission to restore inherited configuration, rediscover tools or leave the sandbox.
   113	
   114	## Item 1
   115	The author read the 28-line `.agents/worklog/orchestrator-glue/record-json-sync.py`; promote its behavior below using only the standard library, without depending on that untracked file in the worker checkout. Read `scripts/orchestrator/orch-gate.sh`, `scripts/require-crit-review.py` and `scripts/orchestrator/acceptance-front-matter.py` and enumerate consumers before editing. Run from the checkout root with exactly one task-id argument; read `.orchestration/acceptance/<task>.md`. Reject task-id traversal and symlink escapes before writing.
   116	Require an opening whole-line `---` JSON block and closing separator. Parse with `json.loads(..., object_pairs_hook=<a hook that raises on a duplicate key>)`; reject duplicate keys at any depth. Missing separators, invalid JSON, duplicate keys, non-object front matter or malformed ledger/replans containers exit 1 with stderr and leave the entire file byte-identical. Validate before opening for writing. Serialize UTF-8 with indent 2, sorted keys and ensure_ascii=False, preserving every unrelated key and every byte of prose after the closing separator.
   117	The exact gate definition at `scripts/require-crit-review.py:37` is `LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")`. Copy only complete prose lines `<id><TAB><class>` whose entire id matches that grammar and whose entire class matches `[a-z0-9-]+`: numeric review-thread ids of ten or more digits, or `audit:` plus exactly seven lowercase hex digits plus `:` plus digits. No ranges, longer audit SHAs, trailing text or near-matches enter JSON.
   118	Initialize an absent ledger to []; validate existing rows against the gate's `{id, class}` contract, preserving valid existing entries, order and values. Append eligible prose rows in order only when their text-form id is absent; suppress repeated prose ids, including matches to existing numeric JSON ids.
   119	C-104: all other rows (`text-security:`, `worker:`, `ci:`, `orchestrator-text:` and others) remain prose only, where the gate's S1 class table reads them. The glue's first version copied every row; the #441 chain's record step refused it with `ledger row 0 must be {id: <thread id or audit:<sha7>:<n>>, class: …}`.
   120	Copy complete lines `re-plan: <class> (<rows>) — specification: …; design: …; implementation: …; verification: …` into `replans[<class>]`. Use exactly `"specification"`, `"design"`, `"implementation"`, `"verification"`, each a non-empty stripped string; no rows or extra key. Initialize absent replans to {}, preserve other classes, and let the last complete line for a class win. Missing/blank parts emit stderr naming the class and missing parts, contribute no entry and never overwrite an existing valid entry; other valid rows/lines still synchronize. Success, including skipped incomplete lines, exits 0; repeated runs are byte-identical.
   121	The gate consumes the record's replans object. [memory:decision] Synchronize only ledger/replans; searches remains unchanged for acceptance-front-matter.py's existing recomputation. Do not change consumers, gates, original glue, live acceptance records, hooks, permissions, workflows, dependencies or graph data.
   122	
   123	## Item 2
   124	Write `tests/unit/test_record_json_sync.py` first with unittest and temporary checkout-shaped records, ending with `if __name__ == "__main__": unittest.main()`. Invoke the real script as `[sys.executable, "-I", <absolute script>, <task>]`; no source-string assertions or mocked transformation.
   125	Use `RecordJsonSyncTest` methods `test_syncs_rows_and_replans`, `test_missing_part_warns_and_is_skipped`, `test_existing_ids_are_kept_and_second_run_is_identical`, `test_last_complete_replan_wins`, `test_malformed_front_matter_is_unchanged`, `test_task_and_output_path_are_confined`, `test_acceptance_front_matter_accepts_replans` and `test_prose_is_byte_identical`.
   126	Fixtures cover a mixed prose table with audit, numeric-thread and excluded kinds, proving only audit/thread rows are copied; 7/40-hex and single/range forms; digit-bearing class slugs; malformed near-matches; existing JSON ids; unrelated JSON including searches; extra prose separators; Unicode; mixed LF/CRLF prose preserved byte-for-byte. Malformed-front-matter subcases include a duplicate `ledger` key and a nested duplicate key, each refused with exit 1 and the whole file unchanged. Missing-part subcases cover every required key and a valid entry followed by an incomplete line.
   127	The compatibility test runs the actual acceptance-front-matter.py CLI and actual gate module in a temporary Git repository with a matching-head sweep and valid audit/thread ledger fixtures; assert exit 0 and preservation of the four-key replans object. Do not copy validation logic into the test or claim excluded prose ids are valid JSON ledger ids.
   128	Exercise every new behavior red before production implementation and green afterward using Commands (c); report each selector and observed assertion failure. A skip or setup/import failure is not behavioral red.
   129	
   130	## Check
   131	Worker Playbook step 4 applies with design 5.14 item 10's measured facts: this host is Darwin, where the manifest's Claude seats run gh inside the sandbox (measured 2026-10-19T03:45Z). The current manifest's Linux-only exclusion does not apply here and is being removed by P1-15 under the D-024-17 revision. Record Commands (a)'s platform and every resolved command in sandbox.md. Every command, including fixtures, lint, Git, gh and messaging, stays sandboxed; any refusal stops dependent work and produces `AGMSG-PONG v1 task_id=dotfiles-T133-record-json-sync-a01 status=blocked` with the exact command and boundary, never an outside-sandbox retry or substitute tool.
   132	Run Commands (c) before and after implementation and Commands (d) afterward; paste complete stdout/stderr and exit statuses into validation.md. Python children retain isolation. No shell file is authorized; shell scripts require English shdoc @file, @brief, @description, @arg and @exitcode comments plus shellcheck and shfmt.
   133	Caps: at most 70 changed lines outside tests/ and .orchestration/, and at most 180 under tests/, using Commands (f)'s numstat; base40 is pasted at dispatch and head40 comes from RESULT, both full 40-hex SHAs. Count additions plus deletions and paste the numstat and both totals. Keep this whole task at or under 150 lines. Do not run Bats locally; use Commands (e) to verify final-head GitHub Actions and fix in-scope failures before RESULT.
   134	
   135	## Completion
   136	Use Commands (f) to start the named fresh branch from origin/main without tracking/config writes. Keep `.orchestration/dotfiles-T133-record-json-sync-a01/task.md` byte-identical to dispatch. In that directory write report.md (selectors, red/green, scope, limitations and cost), validation.md, sandbox.md, learning.md, autoskill.md and result.txt; records are data only. Keep plan/todo/learn worklogs uncommitted and at most one active todo per owner.
   137	Complete worker agent-side review and the required repository review gate, retaining Commands (b–f)'s bindings, with repo-local resolved JSON evidence and receipt under the allowed artifact directory; never open a browser review or publish Crit. Use Commands (f) for commit/push and Commands (e) for a draft PR with an English title/body and the Worker Playbook's ready/CI/Bot sequence.
   138	Commit/push all task changes and evidence, record final-head green CI, then send `AGMSG-RESULT v1 task_id=dotfiles-T133-record-json-sync-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with artifact paths. Report unrun checks; same-UID replacement and shared credentials remain residual risks.
   139	
   140	## Checks (pasted by the orchestrator before each send)
   141	
   142	```
   143	```

**Reviewing context references and skills**
exec
/bin/zsh -lc "git status --short; git rev-parse HEAD; if [ -f .ua/meta.json ]; then cat .ua/meta.json; fi; if [ -f .ua/knowledge-graph.json ]; then /usr/bin/python3 -I -c 'import json; g=json.load(open(\".ua/knowledge-graph.json\")); print(\"\\n\".join(str({k:n.get(k) for k in (\"filePath\",\"summary\")}) for n in g.get(\"nodes\",[]) if any(s in str(n.get(\"filePath\",\"\")) for s in (\"024-design-quality\", \"acceptance-front-matter\", \"require-crit-review\", \"record-json-sync\"))))'; fi; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 172ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a02.md
 M .orchestration/acceptance/dotfiles-T133-loop-limits-a01.md
 M .orchestration/acceptance/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-design-quality.md
 M .orchestration/plans/024-progress.tsv
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md
 M .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a06.md
 M .orchestration/tasks/dotfiles-T133-loop-limits-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-34cc889.log
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-crit.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-review-receipt.md
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a04-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a05-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-74f72c2.md
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-9ef8e5b.md
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-9ef8e5b.md.last.md
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-fb3c323.md
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-fb3c323.md.last.md
 M .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-6cbe954.md
 M .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-a26cc07.md
 M .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-cf4f0ca.md
 M .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-text-security-545281d.md
 M .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-text-security-a9ea1b0.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-1cc2a02.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-8f5ac8d.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-8f5ac8d.md.last.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-e3ae7cd.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-e3ae7cd.md.last.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-2ae9e2c.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-ac9ce14.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-b2a186e.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-ebbb71b.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-ebbb71b.md.last.md
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a06.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a02.md
?? .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/
?? .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/
?? .orchestration/learning/mistakes/M-20261020-01-amendment-note-reproduces-refused-string.md
?? .orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md
?? .orchestration/learning/mistakes/M-20261020-03-dispatch-after-failed-script.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a02.md
?? .orchestration/tasks/dotfiles-T133-python-pin-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-af86233.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-local-review-af86233.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-audit-e9819d4.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-audit-e9819d4.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-chain-09c81cc.log
?? .orchestration/validation/dotfiles-T133-python-pin-a01-chain-e9819d4.log
?? .orchestration/validation/dotfiles-T133-python-pin-a01-crit.json
?? .orchestration/validation/dotfiles-T133-python-pin-a01-local-review-e9819d4.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-python-pin-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-security-09c81cc.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-security-09c81cc.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-0ec4bb9.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-0ec4bb9.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-7771c92.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-7771c92.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9c5500f.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9c5500f.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9f757da.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9f757da.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-ad56c1a.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-b657a89.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-b657a89.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-c8021a7.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-c8021a7.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e4316e1.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e4316e1.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e74aec4.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e74aec4.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-ed75bc6.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-ed75bc6.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-d899b84.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md.last.md
?? .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md
?? .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-audit-cd47e1b.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-audit-cd47e1b.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-crit.json
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-local-review-cd47e1b.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-7a201ea.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-e68fb33.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-local-review-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-25dd01e.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-9545e59.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-a2f4744.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-b3c5076.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-b3c5076.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-79ea98a.log
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-aded8e4.log
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-c0f50fa.log
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-edd824e.log
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-79ea98a.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md.last.md
60a6fb2b324d0381c4a6e539b37c650105154a7e
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
{'filePath': 'scripts/require-crit-review.py', 'summary': "Integration guard that requires native agent or Crit review evidence for meaningful diffs and, for PR integration, re-collects GitHub feedback from the authenticated base's pr-feedback.py and requires a root-cause disposition for every item."}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Skips worklogs and the PR feedback evidence file itself when sizing a diff.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Rejects PR feedback evidence outside .orchestration/validation/ or without the -pr-feedback.json suffix.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Lists unstaged, staged, untracked, and optionally base...HEAD changed paths, excluding ignored files.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Sums added and removed line counts across working, staged, and base...HEAD diffs via git numstat.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Classifies a path as high risk (policy/config file, agent lifecycle prefix, or risky token) and returns the reason.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Aggregates reasons that make review mandatory: high-risk paths, many files, or large line counts.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Validates the review receipt file and its required fields, dispatching to agent or Crit evidence checks.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Checks agent reviewer receipts require the crit-data surface, an allowed outcome, and valid Crit JSON evidence.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Validates repo-local Crit JSON evidence: inside the repo, a list of well-formed resolved records with at least one review/line/file scope.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Checks the filled pr-feedback JSON: correct head, valid fixed:<commit> or not-applicable:<reason> dispositions, failure reasons long enough, and fixed commits in range.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': "Binds the evidence's base to the PR's GitHub base and local repository before running any collector, rejecting stale or rewritten bases."}
{'filePath': 'scripts/require-crit-review.py', 'summary': "Re-runs the GitHub base's pr-feedback.py and requires every currently collected item to be present in the evidence."}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'CLI entry that decides whether review is required, validates base, review receipts, and PR feedback evidence, and exits non-zero on any error.'}
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
/bin/zsh -lc "git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- scripts home tests; rg -n '5\\.14|D-024-29|D-024-30|P1-15' .orchestration/plans/024-design-quality.md; cat .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md.last.md .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-d899b84.md; rg -n 'C-80|C-104|M-20261019-06|437|441' .orchestration/learning/corrections-inventory.tsv .orchestration/acceptance/dotfiles-T133-python-pin-a01.md .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md" in ~/Workspace/dotfiles
 succeeded in 104ms:
home/.chezmoiexternal.yaml.tmpl
home/.chezmoiremove
home/.chezmoiscripts/common/run_after_03-install-sheldon.sh.tmpl
home/.chezmoiscripts/common/run_before_00-refuse-dirty-source.sh.tmpl
home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl
home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl
home/.chezmoiscripts/ubuntu/run_after_04-install-aws-cli.sh.tmpl
home/.chezmoiscripts/ubuntu/run_after_05-client-install-zed.sh.tmpl
home/.chezmoiscripts/ubuntu/run_after_10-install-starship.sh.tmpl
home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl
home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl
home/.chezmoitemplates/claude-settings-managed.json
home/.chezmoitemplates/codex-config-managed.toml
home/dot_agents/README.md
home/dot_agents/agent-config.yaml
home/dot_agents/model-profiles.env
home/dot_agents/permgate-policy.yaml
home/dot_agents/skills/agmsg-orchestration/SKILL.md
home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py
home/dot_agents/skills/gh-first-workflow/SKILL.md
home/dot_agents/skills/project-map/SKILL.md
home/dot_agents/skills/project-map/agents/openai.yaml
home/dot_bash/client/bashrc
home/dot_claude/agents/project-map.md
home/dot_claude/commands/commit.md
home/dot_claude/hooks/executable_enforce-uv.sh
home/dot_claude/hooks/executable_format-edited-files.py
home/dot_claude/hooks/executable_project-map-reload.sh
home/dot_claude/modify_private_settings.json
home/dot_claude/private_mcp.json.tmpl
home/dot_claude/rules/symlink_project-map.md.tmpl
home/dot_claude/skills/project-map/agents/symlink_openai.yaml.tmpl
home/dot_claude/skills/project-map/symlink_SKILL.md.tmpl
home/dot_codex/modify_private_adh.config.toml
home/dot_codex/modify_private_audit.config.toml
home/dot_codex/modify_private_config.toml
home/dot_codex/modify_private_deep.config.toml
home/dot_codex/modify_private_express.config.toml
home/dot_codex/modify_private_review.config.toml
home/dot_codex/modify_private_security.config.toml
home/dot_codex/modify_private_standard.config.toml
home/dot_codex/rules/default.rules
home/dot_config/alias/client.sh
home/dot_config/alias/server.sh
home/dot_config/claude/rules/agmsg-orchestration.md
home/dot_config/claude/rules/compactiondb.md
home/dot_config/claude/rules/crit-review.md
home/dot_config/claude/rules/latex.md
home/dot_config/claude/rules/model-selection.md
home/dot_config/claude/rules/ponytail.md
home/dot_config/claude/rules/pr-integration.md
home/dot_config/claude/rules/project-map.md
home/dot_config/claude/rules/understand-anything.md
home/dot_config/codex/AGENTS.md
home/dot_config/git/ignore
home/dot_config/gwq/config.toml
home/dot_config/mise/mise.lock.tmpl
home/dot_config/sheldon/plugin_sources/client/common.toml
home/dot_config/sheldon/plugin_sources/common.toml
home/dot_config/sheldon/plugin_sources/server.toml
home/dot_config/tango.yml
home/dot_local/bin/common/executable_agent-fanout
home/dot_local/bin/common/executable_codex-orchestrate
home/dot_local/bin/common/executable_contextdb-codex-notify
home/dot_local/bin/common/executable_dev
home/dot_local/bin/common/executable_herdr-agents
home/dot_local/bin/common/executable_herdr-session
home/dot_local/bin/common/executable_permgate
home/dot_local/bin/common/executable_remove-agent-asset
home/dot_local/bin/common/executable_setup-python-env
home/dot_local/bin/server/cache.sh
home/dot_local/bin/server/history.sh
home/dot_mise/config.toml
home/dot_mise/mise.lock
home/dot_npmrc
home/dot_zshrc
scripts/agent-stop-gate.sh
scripts/check-agent-runtime.py
scripts/check-regime-boundary.sh
scripts/check-sleep.sh
scripts/check-statusline-tools.py
scripts/check-tools.sh
scripts/generate-agent-configs.py
scripts/gh-auth.sh
scripts/lib/github-release.sh
scripts/lib/installer-pins.sh
scripts/lint-comparisons-baseline.tsv
scripts/lint-comparisons.py
scripts/orchestrator/acceptance-front-matter.py
scripts/orchestrator/boundary.sh
scripts/orchestrator/bus-read.sh
scripts/orchestrator/chain-integrate.sh
scripts/orchestrator/ci-rerun.sh
scripts/orchestrator/codex-review.sh
scripts/orchestrator/design-keydiff.py
scripts/orchestrator/dispatch.sh
scripts/orchestrator/ff-main.sh
scripts/orchestrator/fill_sweep.py
scripts/orchestrator/ledger-check.py
scripts/orchestrator/local-advisory.sh
scripts/orchestrator/local-review.sh
scripts/orchestrator/orch-audit.sh
scripts/orchestrator/orch-gate.sh
scripts/orchestrator/pr-cost.sh
scripts/orchestrator/regime-ci.py
scripts/orchestrator/replay.sh
scripts/orchestrator/resolve-threads.sh
scripts/orchestrator/sandbox-scan.sh
scripts/orchestrator/task-consistency-check.py
scripts/orchestrator/three-repeat.sh
scripts/pr-feedback.py
scripts/regime-counters.sh
scripts/require-crit-review.py
scripts/run_unit_test.sh
scripts/update-agent-assets.sh
scripts/upgrade-tools.sh
scripts/usage-report.py
scripts/validate-agent-assets.py
tests/files/common.bats
tests/files/macos.bats
tests/files/ubuntu.bats
tests/fixtures/gate-evidence/.prettierrc
tests/fixtures/gate-evidence/acceptance-dispatch-key.md
tests/fixtures/gate-evidence/acceptance-duplicate-key.md
tests/fixtures/gate-evidence/acceptance-finding-quotes-grammar.md
tests/fixtures/gate-evidence/acceptance-ledger-incomplete.md
tests/fixtures/gate-evidence/acceptance-ledger-review-body.md
tests/fixtures/gate-evidence/acceptance-nan.md
tests/fixtures/gate-evidence/acceptance-s6-missing.md
tests/fixtures/gate-evidence/acceptance-s6-present.md
tests/fixtures/gate-evidence/acceptance-stale-head.md
tests/fixtures/gate-evidence/acceptance-wrong-pr.md
tests/fixtures/gate-evidence/pr-feedback-right.json
tests/fixtures/gate-evidence/pr-feedback-wrong.json
tests/fixtures/lessons/dotfiles-T128-process-rules-a05-audit-4af8939.md.last.txt
tests/fixtures/lessons/dotfiles-T128-process-rules-a05-pr-feedback.json
tests/fixtures/lessons/dotfiles-T128-process-rules-a05.record.txt
tests/fixtures/lessons/historical-front-matter.txt
tests/fixtures/regime-counters/dotfiles-T118-rolling-tools-single-update-a01.tsv
tests/fixtures/regime-counters/dotfiles-T119-rolling-release-assets-a01.tsv
tests/fixtures/regime-counters/dotfiles-T124-wave1-task-validator-a01.tsv
tests/fixtures/regime-counters/dotfiles-T128-v0-main-tests-a01.tsv
tests/fixtures/regime-counters/pr-313.json
tests/fixtures/regime-counters/pr-317.json
tests/fixtures/regime/code-review-orchestration.md
tests/fixtures/regime/invariants.md
tests/fixtures/regime/message-contract.md
tests/fixtures/regime/orchestrator-step-6.md
tests/fixtures/regime/orchestrator-step-7.md
tests/fixtures/regime/worker-step-15.md
tests/install/common/check_tools.bats
tests/install/common/lifecycle.bats
tests/install/common/mise.bats
tests/install/common/setup.bats
tests/install/macos/common/brew.bats
tests/install/ubuntu/client/zed.bats
tests/install/ubuntu/server/sheldon.bats
tests/unit/test_agent_session_staleness.py
tests/unit/test_agent_stop_gate.py
tests/unit/test_agmsg_dispatch.py
tests/unit/test_agmsg_orchestration_docs.py
tests/unit/test_apparmor_userns.py
tests/unit/test_asset_manifest.py
tests/unit/test_aws_cli_acquisition.py
tests/unit/test_chain_github_scripts.py
tests/unit/test_chain_glue.py
tests/unit/test_chain_review_scripts.py
tests/unit/test_check_agent_runtime.py
tests/unit/test_check_regime_boundary.py
tests/unit/test_check_sleep.py
tests/unit/test_chezmoiremove_agmsg.py
tests/unit/test_ci_rerun.py
tests/unit/test_claude_settings_merge.py
tests/unit/test_codex_config_merge.py
tests/unit/test_codex_execpolicy.py
tests/unit/test_codex_orchestrate.py
tests/unit/test_contextdb_codex_notify.py
tests/unit/test_enforce_uv.py
tests/unit/test_files_fixture.py
tests/unit/test_format_edited_files_hook.py
tests/unit/test_generate_agent_configs.py
tests/unit/test_gh_auth.py
tests/unit/test_github_release.py
tests/unit/test_gitignore_sandbox_placeholders.py
tests/unit/test_herdr_agents.py
tests/unit/test_lint_comparisons.py
tests/unit/test_makefile_offline.py
tests/unit/test_orch_gate_path.py
tests/unit/test_orchestrator_tools.py
tests/unit/test_permgate.py
tests/unit/test_pr_feedback.py
tests/unit/test_regime_ci.py
tests/unit/test_regime_counters.py
tests/unit/test_release_asset_pins.py
tests/unit/test_remove_agent_asset.py
tests/unit/test_require_crit_review.py
tests/unit/test_runtime_health.py
tests/unit/test_statusline_tools.py
tests/unit/test_supply_chain_policy.py
tests/unit/test_task_checkers.py
tests/unit/test_ua_symbol_coverage.py
tests/unit/test_update_agent_assets.py
tests/unit/test_update_agent_assets_ua_core.py
tests/unit/test_upgrade_tools.py
tests/unit/test_usage_review.py
tests/unit/test_validate_agent_assets.py
tests/unit/test_workflow_orchestration_skip.py
tests/unit/test_workflow_security.py
95:### 5.14 残余（凍結後の計測事実、D-024-29）
103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
107:1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19). The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).
115:9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-record-json-sync-a01"
}
---

# Acceptance record: dotfiles-T133-record-json-sync-a01

- 2026-10-20T06:24Z: text written whole by the review profile from the orchestrator's brief (`dotfiles-T133-record-json-sync-a01-prompt.md`; security: true; promotes the glue record-json-sync.py (prose rows and re-plan lines into the JSON ledger and replans; audit e9819d4 P2, M-20261019-06) into scripts/orchestrator/record-json-sync.py with tests); trailing authoring commentary stripped by the orchestrator; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 4e3ec939… before the Checks paste. C-80 round 1 running; dispatch to an idle Claude seat after a correct verdict (files disjoint from every in-flight task).
- 2026-10-20T06:28Z: C-80 round 1 (`…-text-security-4e3ec93.md`) `Verdict: incorrect`: [P1] line 34: sandbox-only execution asserted while the current manifest excludes `gh *` on Linux for Claude seats (so a command could run outside without the promised refusal); [P2] line 88: the interpreter is selected through inherited `$HOME` and `dirname "$(command -v uv)"` restores the mise shim directory; [P2] line 94: `GIT_CONFIG_GLOBAL=/dev/null` leaves `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_COUNT` effective (a probe showed injected rewrite configuration survives); [P2] line 94: bare `gh` through the shim and `--repo mryfmo/dotfiles` without host binding; [P2] line 74: duplicate JSON keys collapse silently under default parsing. Amendment 1 by the review profile applies the python-pin a02 Commands pattern (passwd home, clean prefix, interpreter and gh by realpath, `GIT_*` unset, `--repo github.com/mryfmo/dotfiles`, fresh `GH_CONFIG_DIR`) and duplicate-key rejection; budget 2 of 3 next.
text-security:4e3ec93:1	excluded-command-trusts-sandbox-context
text-security:4e3ec93:2	tool-environment
text-security:4e3ec93:3	tool-environment
text-security:4e3ec93:4	repository-binding
text-security:4e3ec93:5	input-validation
- 2026-10-20T06:39Z: amendment 1 written whole by the review profile (`record-json-sync-a01-r2-prompt.md`, corrected for C-104 before the run) and installed: one `## Commands` block (platform, passwd home, clean prefix with the proxy variables, interpreter/uv/gh by realpath, GIT_* cleared by env -i), the Darwin statement in the Worker Playbook sentence, duplicate-key rejection, the exact `LEDGER_ID` shape quoted from scripts/require-crit-review.py:37; Checks section normalised; pre-send.sh: checker OK, SECRET_PATTERN 0, bash -n OK, home paths 0; 143 lines (self cap 150); sha256 4e3ec939… -> d899b844365703dcc8a33fccca822fad9c739d5d948a28efdd17919691f439ad. C-80 round 2 running (budget 2 of 3).

[P1] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:34](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:34) — Sandbox-only execution is asserted without a dispatch prerequisite or Codex-only restriction; the manifest defaults to Claude and excludes `gh *` on Linux, so commands can run outside the sandbox without triggering the promised refusal/PONG.

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:88](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:88) — The supposedly fixed interpreter is selected through inherited `$HOME`, while `dirname "$(command -v uv)"` restores this host’s mise-shim directory to PATH; `env -i` and `-I` do not authenticate either executable location, leaving the parent-binding mitigation incomplete.

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:94](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:94) — Clearing only `GIT_CONFIG_GLOBAL` leaves inherited `GIT_DIR`, `GIT_WORK_TREE` and `GIT_CONFIG_COUNT` effective, permitting repository substitution or URL rewriting; a read-only probe confirmed that injected rewrite configuration survives this exact credential-helper prefix. [Git configuration](https://git-scm.com/docs/git-config).

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:94](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:94) — Both the credential helper and PR creation rediscover bare `gh` through this host’s mise shim, and `--repo mryfmo/dotfiles` leaves the host unbound; checkout configuration and inherited `GH_HOST` can therefore change execution or destination despite the reviewed command text. [Mise](https://mise.jdx.dev/dev-tools/shims.html), [gh environment](https://cli.github.com/manual/gh_help_environment).

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:74](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:74) — The malformed-input contract and fixtures omit duplicate JSON keys: default parsing silently collapses duplicate `ledger` fields, potentially deleting findings and converting a record the existing gate rejects into an accepted object; require duplicate-key rejection with byte-identical preservation. [Python JSON behavior](https://docs.python.org/3/library/json.html#repeated-names-within-an-object).

All allowed-file entries have threat rows. Static symlink confinement is required; unrestricted concurrent replacement and shared credentials are explicitly residual, without a claim of host isolation.

📝 まとめ: Completed the read-only design review and checked the cited acceptance/audit context; five findings are submitted for orchestrator disposition.
Not checked: implementation, CI or deployed Linux enforcement; no files changed, and the execution-binding gaps remain unverified.
Verdict: incorrectReading additional input from stdin...
OpenAI Codex v0.163.0
--------
workdir: ~/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a15809-4ace-7ab3-867a-df3f777b276e
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
タスク本文・threat_table・参照された acceptance／review を読み、判断と実際の実行対象が結び付くかを確認します。agmsg-orchestration と Ponytail の指示を適用し、読み取り専用で監査します。モデル profile はこのセッション内では変更しません。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 14ms:
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
---
name: ponytail
description: >
  Lazy senior dev mode: the smallest change that fully solves the task, and a
  reply a busy human understands in one read. Use on any coding task (writing,
  fixing, refactoring, reviewing, choosing dependencies) and when the user says
  "ponytail", "be lazy", "simplest solution", "yagni", or complains about
  over-engineering or bloat. Levels: lite, full (default), ultra.
argument-hint: "[lite|full|ultra|off]"
license: MIT
---

# Ponytail

You are a lazy senior developer. The best code is the code never written. You solve the whole problem with the least new code. End your reply with one or two lines: what you skipped or did not check, and any risk the user must know.

Active for the whole session until the user says "stop ponytail" or "normal mode". Switch level: `/ponytail lite|full|ultra`.

## Before you write

Read the task and the code it touches. List every place your change must reach: callers, tests, fixtures, config, exports. Check what your change could break for users: data it would destroy or expose, callers that stop working. That is scope. Extra features are not.

## The smallest complete change

Take the first option that fully works:

1. Does it need to exist? Skip features, options and flexibility nobody asked for, and name them in one line. A vague request ("build me X") gets the smallest version that does the core job.
2. Already in this codebase (a helper, component, service, pattern)? Use it the way the surrounding code does.
3. Standard library or a platform feature? Use it, unless the project has its own. A house component beats a native widget.
4. An installed dependency? Use it. Never add a dependency for a few lines.
5. Can it be one line a reader gets at a glance? One line.
6. Otherwise: the minimum code that works.

- Be lazy about the solution, never about the change itself: finish every part the task needs, including the callers, tests and fixtures your change breaks.
- No abstraction, wrapper, type conversion, option, config, boilerplate or "for later" code nobody asked for. Keep values in the form the platform already gives you. Deletion beats addition. Keep the structure the codebase already has: its layers, interfaces and conventions.
- The shortest working diff wins, once you know everything it must touch. A one-liner that needs decoding is not short.
- Comment only the why the code cannot show, in one line.
- Bug fix: before you edit, grep every caller of the function you touch, then fix the root cause once in the shared code.
- Code you move or merge keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases.
- Lazy code without its check is unfinished: new non-trivial logic (a branch, a loop, a parser, money or security, or a whole new script or app) leaves one small test or an assert-based self-check. Trivial changes need none.
- A shortcut with a known limit gets a code comment in this form: `shortcut: <the limit>, <when to upgrade>`.

Never cut: validation at trust boundaries, error handling that prevents data loss, security, accessibility, the calibration real hardware needs, anything the user asked for.

## Levels

| Level | Behavior |
|-------|----------|
| **lite** | Build what was asked. Name the smaller option in one line and let the user pick. |
| **full** | The rules above. Default. |
| **ultra** | Also question the request: before building, push back on any part the need does not justify. |

exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md' in ~/Workspace/dotfiles
 succeeded in 14ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-record-json-sync-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/record-json-sync.py
     8	  - tests/unit/test_record_json_sync.py
     9	  - .orchestration/dotfiles-T133-record-json-sync-a01/**
    10	after: []
    11	threat_table:
    12	  - {control: "scripts/orchestrator/record-json-sync.py", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_syncs_rows_and_replans"}
    13	  - {control: "tests/unit/test_record_json_sync.py", disposition: "residual: Assertion errors can conceal broken behavior; the final-head audit checks fixtures, observations and red/green evidence against the implementation."}
    14	  - {control: ".orchestration/dotfiles-T133-record-json-sync-a01/**", disposition: "residual: Only task records are permitted under this wildcard; no executable helper or replacement implementation may be hidden in evidence."}
    15	  - {control: "the task copy .orchestration/dotfiles-T133-record-json-sync-a01/task.md", disposition: "residual: The orchestrator compares the whole file byte-for-byte with dispatch and checks its SHA-256 before acceptance."}
    16	  - {control: "the evidence records under .orchestration/dotfiles-T133-record-json-sync-a01/", disposition: "residual: Preserve commands, exit statuses and complete outputs; the audit compares their claims with the final diff and GitHub Actions."}
    17	  - {control: "task metadata: kind, security, allowed_files, after, threat_table and premises", disposition: "residual: Task-consistency checks and independent task-file review run before dispatch and acceptance; task-copy equality exposes altered metadata."}
    18	  - {control: "metadata separators", disposition: "residual: Whole-file comparison covers task-copy separators; evidence is untrusted data, and acceptance-record delimiter failures are exercised by the malformed-front-matter test."}
    19	  - {control: "malformed acceptance-record front matter", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_malformed_front_matter_is_unchanged"}
    20	  - {control: "acceptance-record write target", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_task_and_output_path_are_confined"}
    21	  - {control: "in-process effects", disposition: "residual: Only the named acceptance file is rewritten after validation; tests use temporary records, and same-UID concurrent replacement remains possible."}
    22	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: Commands bind the clean parent, fixed interpreter and executable paths; no workflow or interpreter configuration changes are authorized."}
    23	  - {control: "new or renamed scripts", disposition: "residual: Only scripts/orchestrator/record-json-sync.py is introduced; it parses data with the standard library and never evaluates prose or starts subprocesses."}
    24	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: Same-UID replacement and shared credentials remain possible; local JSON synchronization is process evidence, never authentication or permission approval."}
    25	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: Every worker action stays inside its sandbox and declared files; this task changes no deployed sandbox, permissions or trusted host inputs."}
    26	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Commands establish the clean parent before binding tools; the transformer launches no executable and cannot sanitize the parent that started its interpreter."}
    27	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: Task-id and symlink escape tests constrain the write target; they do not establish protection against unrestricted same-UID replacement."}
    28	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Commands reuse the probed PY binding; parse and validate the record before writing, without claiming a snapshot or concurrent-writer exclusion."}
    29	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: RESULT and cap evidence name full base and head SHAs; this transformer introduces no reservation, lock or head-named executable output."}
    30	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: The transformation tests establish record behavior only; host provenance, concurrent writes and shared credentials remain explicit residuals."}
    31	  - {control: "design 5.14 item 7: 検証", disposition: "residual: Red/green tests cover the data transformation; they do not claim the four host-execution probes, since no execution mechanism is introduced."}
    32	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: This writes a local acceptance-record proposal without granting approval; committed permission decisions and final integration retain their existing authorities."}
    33	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: Runtime uses only the standard library under the fixed installed interpreter; worker lint caches remain seat-local and no orchestrator cache is changed."}
    34	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Every command including gh and push remains sandboxed; refusal produces a blocked PONG without escalation or a substitute tool."}
    35	  - {control: "orchestrator effect merge", disposition: "residual: Only the orchestrator merges through gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker never merges or pushes main."}
    36	  - {control: "orchestrator effect update-branch", disposition: "residual: The orchestrator refreshes CI, feedback and the task-level audit after an update-branch changes the head, before applying the integration gate."}
    37	  - {control: "orchestrator effect forced worker removal", disposition: "residual: None is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and any forced removal records the discarded state in acceptance."}
    38	premises:
    39	  - claim: "The existing glue has 28 lines; neither requested tracked path exists in the authoring checkout."
    40	    command: |-
    41	      "${P[@]}" "$PY" -I -c 'from pathlib import Path; p=Path(".agents/worklog/orchestrator-glue/record-json-sync.py"); print("glue_lines=" + str(len(p.read_text().splitlines()))); print("tracked_script_exists=" + str(Path("scripts/orchestrator/record-json-sync.py").exists())); print("test_module_exists=" + str(Path("tests/unit/test_record_json_sync.py").exists()))'
    42	    output: |-
    43	      glue_lines=28
    44	      tracked_script_exists=False
    45	      test_module_exists=False
    46	  - claim: "The gate defines the ledger grammar, class grammar and four required re-plan keys; replan_complete requires non-empty text."
    47	    command: |-
    48	      rg -n '^LEDGER_ID =|^REPLAN_KEYS =|^CLASS_SLUG =|^def replan_complete|^    return isinstance\(entry, dict\)' scripts/require-crit-review.py
    49	    output: |-
    50	      37:LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")
    51	      38:CLASS_SLUG = re.compile(r"[a-z0-9-]+")
    52	      44:REPLAN_KEYS = ("specification", "design", "implementation", "verification")
    53	      775:def replan_complete(entry: object) -> bool:
    54	      776:    return isinstance(entry, dict) and all(is_text(entry.get(key)) for key in REPLAN_KEYS)
    55	  - claim: "acceptance-front-matter.py lines 79-84 reject wrong containers, invalid class slugs, missing or extra keys and blank values before writing."
    56	    command: |-
    57	      sed -n '79,84p' scripts/orchestrator/acceptance-front-matter.py
    58	    output: |-
    59	          replans, parts = record.get("replans", {}), ", ".join(gate.REPLAN_KEYS)
    60	          if not isinstance(replans, dict):
    61	              parser.error(f"replans must be {{<class slug>: {{{parts}}}}}; nothing written")
    62	          for cls, entry in replans.items():
    63	              if not gate.CLASS_SLUG.fullmatch(cls) or not gate.replan_complete(entry) or set(entry) != set(gate.REPLAN_KEYS):
    64	                  parser.error(f"replans.{cls} must be {{{parts}}}, each a non-empty string; nothing written")
    65	---
    66	
    67	# AGMSG-TASK dotfiles-T133-record-json-sync-a01 — promote acceptance-record JSON synchronization
    68	Written 2026-10-20; amendment 1 addresses all five C-80 round-1 findings and C-104. PR #437's task-level audit e9819d4 found empty JSON ledger, replans and searches beside 18 prose rows and three re-plan lines (M-20261019-06). [memory:failure] Prose-only findings and re-plans do not populate the JSON the gate consumes.
    69	Design 5.14 of `.orchestration/plans/024-design-quality.md` is frozen (D-024-29) and applies by reference (D-024-30); items 0–10 have individual threat rows.
    70	
    71	## Commands
    72	Definitions occur only here; premises quote source-authoring probes, not additional worker instructions. Start (parent) from the trusted launcher in the verified checkout root; run the lettered sections inside it. Stop dependent work at any failed prerequisite; substitute recorded operands before execution.
    73	```bash
    74	# (parent) Clear inherited inputs before starting the shell.
    75	/usr/bin/env -i PATH=/usr/bin:/bin TMPDIR="${TMPDIR:-/tmp}" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 /bin/bash --noprofile --norc -p -o pipefail
    76	# (a) Record the platform and anchor home to the real user's passwd entry.
    77	platform=$(/usr/bin/uname -s); printf '%s\n' "$platform"
    78	case "$platform" in
    79	  Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
    80	  Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
    81	  *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
    82	esac
    83	rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
    84	case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
    85	# (b) The clean child prefix.
    86	P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8)
    87	# (c) Bind and probe the exact interpreter, then use this test invocation for red and green.
    88	PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
    89	[ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python: refused: missing-executable' >&2; exit 1; }
    90	"${P[@]}" "$PY" -I -c 'import os,sys; p=os.path.realpath(sys.executable); print(p, sys.version.split()[0]); assert sys.version.split()[0]=="3.15.0" and p.startswith(os.environ["HOME"]+"/.local/share/mise/installs/python/3.15.0/")' || exit 1
    91	"${P[@]}" "$PY" -I tests/unit/test_record_json_sync.py
    92	# (d) Resolve uv only when needed for lint; never execute a shim or provision a replacement interpreter.
    93	UV=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/uv/latest/uv-aarch64-apple-darwin/uv")
    94	case "$UV" in ""|*/mise/shims/*) exit 1;; "$home"/.local/share/mise/installs/uv/*/uv-aarch64-apple-darwin/uv) ;; *) exit 1;; esac
    95	[ -f "$UV" ] && [ -x "$UV" ] || exit 1
    96	"${P[@]}" UV_CACHE_DIR="$PWD/.uv-cache" "$UV" run --no-config --no-project --python "$PY" --with ruff ruff check scripts/orchestrator/record-json-sync.py tests/unit/test_record_json_sync.py
    97	"${P[@]}" UV_CACHE_DIR="$PWD/.uv-cache" "$UV" run --no-config --no-project --python "$PY" --with ruff ruff format --check scripts/orchestrator/record-json-sync.py tests/unit/test_record_json_sync.py
    98	# (e) Bind gh; every invocation gets a fresh config directory and an explicit host/repository.
    99	GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
   100	case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
   101	[ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
   102	gh_call() {
   103	  local GH_CONFIG_DIR; GH_CONFIG_DIR=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX") || return
   104	  case "$1" in api) [[ "$2" == repos/mryfmo/dotfiles/* ]] || return 1; "${P[@]}" GH_CONFIG_DIR="$GH_CONFIG_DIR" "$GH" "$@" --hostname github.com;; pr|run|issue) "${P[@]}" GH_CONFIG_DIR="$GH_CONFIG_DIR" "$GH" "$@" --repo github.com/mryfmo/dotfiles;; *) return 1;; esac
   105	}
   106	# (f) All Git operations use the clean prefix and system Git; cap operands are full recorded SHAs.
   107	branch=tools/record-json-sync-a01
   108	git_clean() { "${P[@]}" /usr/bin/git "$@"; }
   109	"${P[@]}" /usr/bin/git diff --numstat "$base40...$head40"
   110	( GH_CONFIG_DIR=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX") || exit 1; P+=(GH_CONFIG_DIR="$GH_CONFIG_DIR"); "${P[@]}" /usr/bin/git -c credential.helper= -c "credential.helper=!$GH auth git-credential" push https://github.com/mryfmo/dotfiles.git "HEAD:$branch" )
   111	```
   112	Commands (a) is the only home source. Commands (parent)/(b) clear inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_COUNT`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM` and other `GIT_*`, tool, loader and Python variables. Commands (e)/(f) also isolate the credential helper's configuration; authentication failure is a blocker, never permission to restore inherited configuration, rediscover tools or leave the sandbox.
   113	
   114	## Item 1
   115	The author read the 28-line `.agents/worklog/orchestrator-glue/record-json-sync.py`; promote its behavior below using only the standard library, without depending on that untracked file in the worker checkout. Read `scripts/orchestrator/orch-gate.sh`, `scripts/require-crit-review.py` and `scripts/orchestrator/acceptance-front-matter.py` and enumerate consumers before editing. Run from the checkout root with exactly one task-id argument; read `.orchestration/acceptance/<task>.md`. Reject task-id traversal and symlink escapes before writing.
   116	Require an opening whole-line `---` JSON block and closing separator. Parse with `json.loads(..., object_pairs_hook=<a hook that raises on a duplicate key>)`; reject duplicate keys at any depth. Missing separators, invalid JSON, duplicate keys, non-object front matter or malformed ledger/replans containers exit 1 with stderr and leave the entire file byte-identical. Validate before opening for writing. Serialize UTF-8 with indent 2, sorted keys and ensure_ascii=False, preserving every unrelated key and every byte of prose after the closing separator.
   117	The exact gate definition at `scripts/require-crit-review.py:37` is `LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")`. Copy only complete prose lines `<id><TAB><class>` whose entire id matches that grammar and whose entire class matches `[a-z0-9-]+`: numeric review-thread ids of ten or more digits, or `audit:` plus exactly seven lowercase hex digits plus `:` plus digits. No ranges, longer audit SHAs, trailing text or near-matches enter JSON.
   118	Initialize an absent ledger to []; validate existing rows against the gate's `{id, class}` contract, preserving valid existing entries, order and values. Append eligible prose rows in order only when their text-form id is absent; suppress repeated prose ids, including matches to existing numeric JSON ids.
   119	C-104: all other rows (`text-security:`, `worker:`, `ci:`, `orchestrator-text:` and others) remain prose only, where the gate's S1 class table reads them. The glue's first version copied every row; the #441 chain's record step refused it with `ledger row 0 must be {id: <thread id or audit:<sha7>:<n>>, class: …}`.
   120	Copy complete lines `re-plan: <class> (<rows>) — specification: …; design: …; implementation: …; verification: …` into `replans[<class>]`. Use exactly `"specification"`, `"design"`, `"implementation"`, `"verification"`, each a non-empty stripped string; no rows or extra key. Initialize absent replans to {}, preserve other classes, and let the last complete line for a class win. Missing/blank parts emit stderr naming the class and missing parts, contribute no entry and never overwrite an existing valid entry; other valid rows/lines still synchronize. Success, including skipped incomplete lines, exits 0; repeated runs are byte-identical.
   121	The gate consumes the record's replans object. [memory:decision] Synchronize only ledger/replans; searches remains unchanged for acceptance-front-matter.py's existing recomputation. Do not change consumers, gates, original glue, live acceptance records, hooks, permissions, workflows, dependencies or graph data.
   122	
   123	## Item 2
   124	Write `tests/unit/test_record_json_sync.py` first with unittest and temporary checkout-shaped records, ending with `if __name__ == "__main__": unittest.main()`. Invoke the real script as `[sys.executable, "-I", <absolute script>, <task>]`; no source-string assertions or mocked transformation.
   125	Use `RecordJsonSyncTest` methods `test_syncs_rows_and_replans`, `test_missing_part_warns_and_is_skipped`, `test_existing_ids_are_kept_and_second_run_is_identical`, `test_last_complete_replan_wins`, `test_malformed_front_matter_is_unchanged`, `test_task_and_output_path_are_confined`, `test_acceptance_front_matter_accepts_replans` and `test_prose_is_byte_identical`.
   126	Fixtures cover a mixed prose table with audit, numeric-thread and excluded kinds, proving only audit/thread rows are copied; 7/40-hex and single/range forms; digit-bearing class slugs; malformed near-matches; existing JSON ids; unrelated JSON including searches; extra prose separators; Unicode; mixed LF/CRLF prose preserved byte-for-byte. Malformed-front-matter subcases include a duplicate `ledger` key and a nested duplicate key, each refused with exit 1 and the whole file unchanged. Missing-part subcases cover every required key and a valid entry followed by an incomplete line.
   127	The compatibility test runs the actual acceptance-front-matter.py CLI and actual gate module in a temporary Git repository with a matching-head sweep and valid audit/thread ledger fixtures; assert exit 0 and preservation of the four-key replans object. Do not copy validation logic into the test or claim excluded prose ids are valid JSON ledger ids.
   128	Exercise every new behavior red before production implementation and green afterward using Commands (c); report each selector and observed assertion failure. A skip or setup/import failure is not behavioral red.
   129	
   130	## Check
   131	Worker Playbook step 4 applies with design 5.14 item 10's measured facts: this host is Darwin, where the manifest's Claude seats run gh inside the sandbox (measured 2026-10-19T03:45Z). The current manifest's Linux-only exclusion does not apply here and is being removed by P1-15 under the D-024-17 revision. Record Commands (a)'s platform and every resolved command in sandbox.md. Every command, including fixtures, lint, Git, gh and messaging, stays sandboxed; any refusal stops dependent work and produces `AGMSG-PONG v1 task_id=dotfiles-T133-record-json-sync-a01 status=blocked` with the exact command and boundary, never an outside-sandbox retry or substitute tool.
   132	Run Commands (c) before and after implementation and Commands (d) afterward; paste complete stdout/stderr and exit statuses into validation.md. Python children retain isolation. No shell file is authorized; shell scripts require English shdoc @file, @brief, @description, @arg and @exitcode comments plus shellcheck and shfmt.
   133	Caps: at most 70 changed lines outside tests/ and .orchestration/, and at most 180 under tests/, using Commands (f)'s numstat; base40 is pasted at dispatch and head40 comes from RESULT, both full 40-hex SHAs. Count additions plus deletions and paste the numstat and both totals. Keep this whole task at or under 150 lines. Do not run Bats locally; use Commands (e) to verify final-head GitHub Actions and fix in-scope failures before RESULT.
   134	
   135	## Completion
   136	Use Commands (f) to start the named fresh branch from origin/main without tracking/config writes. Keep `.orchestration/dotfiles-T133-record-json-sync-a01/task.md` byte-identical to dispatch. In that directory write report.md (selectors, red/green, scope, limitations and cost), validation.md, sandbox.md, learning.md, autoskill.md and result.txt; records are data only. Keep plan/todo/learn worklogs uncommitted and at most one active todo per owner.
   137	Complete worker agent-side review and the required repository review gate, retaining Commands (b–f)'s bindings, with repo-local resolved JSON evidence and receipt under the allowed artifact directory; never open a browser review or publish Crit. Use Commands (f) for commit/push and Commands (e) for a draft PR with an English title/body and the Worker Playbook's ready/CI/Bot sequence.
   138	Commit/push all task changes and evidence, record final-head green CI, then send `AGMSG-RESULT v1 task_id=dotfiles-T133-record-json-sync-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with artifact paths. Report unrun checks; same-UID replacement and shared credentials remain residual risks.
   139	
   140	## Checks (pasted by the orchestrator before each send)
   141	
   142	```
   143	```

**Reviewing context references and skills**
exec
/bin/zsh -lc "git status --short; git rev-parse HEAD; if [ -f .ua/meta.json ]; then cat .ua/meta.json; fi; if [ -f .ua/knowledge-graph.json ]; then /usr/bin/python3 -I -c 'import json; g=json.load(open(\".ua/knowledge-graph.json\")); print(\"\\n\".join(str({k:n.get(k) for k in (\"filePath\",\"summary\")}) for n in g.get(\"nodes\",[]) if any(s in str(n.get(\"filePath\",\"\")) for s in (\"024-design-quality\", \"acceptance-front-matter\", \"require-crit-review\", \"record-json-sync\"))))'; fi; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 172ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a02.md
 M .orchestration/acceptance/dotfiles-T133-loop-limits-a01.md
 M .orchestration/acceptance/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-design-quality.md
 M .orchestration/plans/024-progress.tsv
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md
 M .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a06.md
 M .orchestration/tasks/dotfiles-T133-loop-limits-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-34cc889.log
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-crit.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-review-receipt.md
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a04-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a05-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-74f72c2.md
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-9ef8e5b.md
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-9ef8e5b.md.last.md
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-fb3c323.md
 M .orchestration/validation/dotfiles-T133-loop-limits-a01-text-security-fb3c323.md.last.md
 M .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-6cbe954.md
 M .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-a26cc07.md
 M .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-cf4f0ca.md
 M .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-text-security-545281d.md
 M .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-text-security-a9ea1b0.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-1cc2a02.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-8f5ac8d.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-8f5ac8d.md.last.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-e3ae7cd.md
 M .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-e3ae7cd.md.last.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-2ae9e2c.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-ac9ce14.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-b2a186e.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-ebbb71b.md
 M .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-ebbb71b.md.last.md
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a06.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a02.md
?? .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/
?? .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/
?? .orchestration/learning/mistakes/M-20261020-01-amendment-note-reproduces-refused-string.md
?? .orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md
?? .orchestration/learning/mistakes/M-20261020-03-dispatch-after-failed-script.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-a02.md
?? .orchestration/tasks/dotfiles-T133-python-pin-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-af86233.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-local-review-af86233.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-audit-e9819d4.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-audit-e9819d4.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-chain-09c81cc.log
?? .orchestration/validation/dotfiles-T133-python-pin-a01-chain-e9819d4.log
?? .orchestration/validation/dotfiles-T133-python-pin-a01-crit.json
?? .orchestration/validation/dotfiles-T133-python-pin-a01-local-review-e9819d4.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-python-pin-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-security-09c81cc.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-security-09c81cc.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-0ec4bb9.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-0ec4bb9.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-7771c92.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-7771c92.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9c5500f.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9c5500f.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9f757da.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-9f757da.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-ad56c1a.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-b657a89.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-b657a89.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-c8021a7.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-c8021a7.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e4316e1.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e4316e1.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e74aec4.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-e74aec4.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-ed75bc6.md
?? .orchestration/validation/dotfiles-T133-python-pin-a01-text-security-ed75bc6.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-d899b84.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md
?? .orchestration/validation/dotfiles-T133-record-ledger-carry-a01-text-security-f3bfcc6.md.last.md
?? .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md
?? .orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-audit-cd47e1b.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-audit-cd47e1b.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-crit.json
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-local-review-cd47e1b.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-7a201ea.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-e68fb33.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-local-review-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-25dd01e.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-9545e59.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-a2f4744.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-b3c5076.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-b3c5076.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-79ea98a.log
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-aded8e4.log
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-c0f50fa.log
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-edd824e.log
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-79ea98a.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md.last.md
60a6fb2b324d0381c4a6e539b37c650105154a7e
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
{'filePath': 'scripts/require-crit-review.py', 'summary': "Integration guard that requires native agent or Crit review evidence for meaningful diffs and, for PR integration, re-collects GitHub feedback from the authenticated base's pr-feedback.py and requires a root-cause disposition for every item."}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Skips worklogs and the PR feedback evidence file itself when sizing a diff.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Rejects PR feedback evidence outside .orchestration/validation/ or without the -pr-feedback.json suffix.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Lists unstaged, staged, untracked, and optionally base...HEAD changed paths, excluding ignored files.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Sums added and removed line counts across working, staged, and base...HEAD diffs via git numstat.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Classifies a path as high risk (policy/config file, agent lifecycle prefix, or risky token) and returns the reason.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Aggregates reasons that make review mandatory: high-risk paths, many files, or large line counts.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Validates the review receipt file and its required fields, dispatching to agent or Crit evidence checks.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Checks agent reviewer receipts require the crit-data surface, an allowed outcome, and valid Crit JSON evidence.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Validates repo-local Crit JSON evidence: inside the repo, a list of well-formed resolved records with at least one review/line/file scope.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'Checks the filled pr-feedback JSON: correct head, valid fixed:<commit> or not-applicable:<reason> dispositions, failure reasons long enough, and fixed commits in range.'}
{'filePath': 'scripts/require-crit-review.py', 'summary': "Binds the evidence's base to the PR's GitHub base and local repository before running any collector, rejecting stale or rewritten bases."}
{'filePath': 'scripts/require-crit-review.py', 'summary': "Re-runs the GitHub base's pr-feedback.py and requires every currently collected item to be present in the evidence."}
{'filePath': 'scripts/require-crit-review.py', 'summary': 'CLI entry that decides whether review is required, validates base, review receipts, and PR feedback evidence, and exits non-zero on any error.'}
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
/bin/zsh -lc "git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- scripts home tests; rg -n '5\\.14|D-024-29|D-024-30|P1-15' .orchestration/plans/024-design-quality.md; cat .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md.last.md .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-d899b84.md; rg -n 'C-80|C-104|M-20261019-06|437|441' .orchestration/learning/corrections-inventory.tsv .orchestration/acceptance/dotfiles-T133-python-pin-a01.md .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md" in ~/Workspace/dotfiles
.orchestration/learning/corrections-inventory.tsv:75:C-80	text-only	code	pending	procedure:the security-profile review of a security: true task text and threat table runs before dispatch and its findings join the class table (M-20261019-03); tool:security-review.sh --text <task.md> (glue)
.orchestration/learning/corrections-inventory.tsv:80:C-85	text-only	code	pending	procedure:integration chains serialize on the one canonical review worktree today (chain-integrate.sh refuses any other path: "review worktree is not the canonical one", probed 2026-10-19T04:53Z with three extra worktrees); the security reviews, the C-80 text reviews and the redesigns run in parallel; the per-PR review worktree that lets chains run concurrently is a P1-6 item (after P1-15 under D-024-20); merges stay serialized through the gate (operator instruction 2026-10-19 13:5x: maximize parallel work without quality loss)
.orchestration/learning/corrections-inventory.tsv:83:C-88	text-only	code	pending	procedure:a dispatched text that relies on a design section not yet on main quotes the relied-on sentences verbatim inline, so the reviewed bytes (and the TASK/RESULT sha256) carry the contract; the path is context only; C-86's path-naming alone is insufficient (the a07 C-80 of 2026-10-19T07:30Z: changing the referenced design changes the effective instructions without changing the reviewed bytes); tool:task-consistency-check C20 requires a quotation block for every cited uncommitted section (P1-12 owner)
.orchestration/learning/corrections-inventory.tsv:87:C-92	text-only	code	pending	procedure:a task text's pre-dispatch (C-80) review is capped at 3 rounds; at the third incorrect verdict the text is re-planned as a whole by another context that receives every finding so far (never a delta prompt) or the task is split, with a re-plan: line and a default decision in the map (plan 006 A1 '3 rounds then freeze'; M-20261019-05: 19 rounds on the P1-15 text); tool:text-security-review.sh refuses a fourth review of one task id without a re-plan: line newer than the third verdict (orchestrator glue, now)
.orchestration/learning/corrections-inventory.tsv:99:C-104	records	record	pending	procedure:the JSON `ledger` of an acceptance record holds only `audit:<sha7>:<n>` rows and numeric review-thread ids (acceptance-front-matter.py's shape); text-security, worker, ci and orchestrator-text rows are prose rows the gate's S1 class table reads; a tool that syncs prose into JSON filters by that shape (record-json-sync glue fixed 2026-10-20T06:3xZ after the #441 chain's record step refused `orchestrator-text:2fc20d2:1`); the record-json-sync task text states the shape and tests the filter.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:12:    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-python-pin-a01 status=pending-integration round=1 pr=437 head=09c81cc3cc759dd08bb8b76935c99a34c8f19442 reason=RESULT-of-04:03:43Z-read;CI-all-green-at-09c81cc3;security-review-of-09c81cc3:Verdict-correct;the-integration-chain-update-branched-the-PR-to-e9819d45(merge-of-main-60a6fb2b,patch-unchanged)and-runs-sweep,local-review,task-level-audit,gate;no-worker-action-until-the-audit-result;no-finding-on-the-implementation-so-far"
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:17:  "pr": 437,
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:23:      "verification": "C-80 round 1 after this line."
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:29:      "verification": "CI `validate` on the next head of PR #437."
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:35:      "verification": "C-80 round 4 with the budget reset by this line, then the worker's pasted outputs of exactly those commands."
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:47:- 2026-10-20T01:11:32Z: C-80 round 1 running (security: true); dispatch to a012 (holding since the loop-limits prerequisites) when correct.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:48:- 2026-10-20T01:14Z: C-80 round 1 (`…-text-security-7771c92.md`) `Verdict: incorrect`, six P2: the version decision probes `latest/bin/python3` while validation runs `3.15.0/bin/python3` (bind both to one realpath); bare `uv` resolves through the mise shim and inherits HOME/Python startup inputs in the validation command; the in-process row ignores that unittest imports repository modules and test_supply_chain_policy.py:394 launches PATH-resolved chezmoi; the cap evidence uses inherited GIT_* and mutable refs (bind base/head by sha); the regex accepts a trailing newline and Unicode digits (ASCII fullmatch); no per-item rows for 5.14 items 0-10 (D-024-30). Amendment 1 via the review profile; budget 1 of 3.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:55:- 2026-10-20T01:28:06Z: amendment 1 (`redesign/python-pin-r2.md`) installed: 150 lines, 4 files, 27 threat rows (one per 5.14 item 0-10, the per-file rows, the standard rows); the exact interpreter bound by realpath; ASCII fullmatch with negatives; bound base/head cap evidence; checker OK; C-80 round 2 running.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:56:- 2026-10-20T01:27Z: C-80 round 2 (`…-text-security-e4316e1.md`) `Verdict: incorrect`, two P2: the premises' probes ran `~/.local/.../python3` with the inherited HOME outside the clean prefix of the validation command; the base lookup invoked bare `gh` (the mise shim). Amendment 2 at 2026-10-20T01:40:32Z (`redesign/python-pin-r3.md`): one clean prefix and the passwd-anchored home for every probe and command (no `~`), gh by its verified realpath with GH_TOKEN passed explicitly; 164 lines; checker OK; C-80 round 3 running (the last of the C-92 budget: a fourth review needs a re-plan line).
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:59:- 2026-10-20T01:42Z: C-80 round 3 (`…-text-security-9f757da.md`) `Verdict: incorrect`, one P2: `unittest discover -p test_mise_config.py` imports subpackage initialisers whatever the pattern (an untracked tests/unit/<pkg>/__init__.py would execute with `Ran 1 test` unchanged); execute the test file directly under `-I`. Fourth finding of the tool-environment family on this text (7771c92:2, e4316e1:1, e4316e1:2, 9f757da:1) and the third review: S1 and the C-92 cap both fire. Re-examination: the text wrote its commands ad hoc in several places (prerequisite probes, validation, cap evidence, the test invocation), so each review found another leaky invocation; the whole fix is one command block defined once.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:61:re-plan: tool-environment (rows text-security:7771c92:2, text-security:e4316e1:1, text-security:e4316e1:2, text-security:9f757da:1) — specification: every command the text prescribes runs in the trusted-parent form with one interpreter, no PATH resolution and no implicit import (no discovery, no shim, no `~`); design: a single `## Commands` block defines the clean prefix, the anchored home, the exact interpreter path, the direct test-file execution (`python -I tests/unit/test_mise_config.py`) and the bound gh realpath once, and every premise, check and evidence line references that block instead of restating a command; implementation: amendment 3 of the text by the review profile; verification: C-80 round 4 with the budget reset by this line, then the worker's pasted outputs of exactly those commands.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:62:- 2026-10-20T01:54:26Z: re-planned text (`redesign/python-pin-r4.md`) installed: 167 lines + the standard rows the review profile dropped (orchestrator effects, task metadata, in-process effects, workflow inputs) = checker OK; one `## Commands` block (anchored home, clean prefix, exact interpreter, direct test-file execution, bound gh realpath, bound cap evidence) referenced everywhere; no `~`. C-80 round 1 after the re-plan running.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:63:- 2026-10-20T02:00Z: C-80 round 1 after the re-plan (`…-text-security-e74aec4.md`) `Verdict: incorrect`, two P2, both facts the orchestrator's prompt prescribed without probing (C-87 by the orchestrator): mise installs gh under `installs/github-cli-cli/` (not `github-cli/`), so Commands (e) always refuses; `git -c include.path=` is invalid (exit 128 `relative config includes must come from files`). Amendment 1 after the re-plan with the probed values (2026-10-20T02:01:18Z): the gh realpath from the host, and the cap evidence read from the GitHub API compare endpoint (design 5.14 item 8) instead of local git; budget 1 of 3.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:66:- 2026-10-20T02:32:13Z: C-80 round 2 after the re-plan (`…-text-security-c8021a7.md`) `Verdict: correct` (commands remove inherited inputs, avoid shims, bind GitHub evidence to the repository and full shas; residuals explicit). Dispatch next: the orchestrator runs the text's Commands probes fresh (C-100) and pastes them into the Checks block; a012 takes it (loop-limits stays held on its prerequisites).
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:68:- 2026-10-20T02:33:41Z: the dispatch probes run fresh (C-100): inside the Claude sandbox `dscl . -read … NFSHomeDirectory` fails (`Operation failed with error: eServerError`; the helper task measured exit 70 in the Codex sandbox) while `/usr/bin/id -P | cut -d: -f9` and Python's `pwd.getpwuid` return the passwd home; outside the sandbox dscl works. Measured amendment: Commands (a) uses `id -P` (same directory service through libc); recorded in design 5.14's residual list (D-024-29: no item change). Probe outputs pasted into the Checks block: interpreter realpath …/python/3.15.0/bin/python3 (3.15.0), gh realpath …/github-cli-cli/2.102.0/bin/gh (2.102.0), main 118daafa, declaration python = "latest". Text sha256 c8021a71… -> 9c5500f0…; checker OK; C-80 round 3 after the re-plan running (the last of the budget).
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:69:- 2026-10-20T02:37Z: C-80 round 3 after the re-plan (`…-text-security-9c5500f.md`) `Verdict: incorrect`, one P2: GitHub's compare endpoint caps `.files` at 300 whatever `--paginate` says, and the task directory is unbounded, so a truncated list could hide changes from the cap evidence; reject truncated results or establish completeness independently. The budget after the first re-plan is spent. Re-examination: four rounds on this text found nine findings of one family — commands and facts written from memory instead of executed (dscl, the gh install path, `-c include.path=`, the compare cap): fragile-premise. The re-plan: no command enters the text unexecuted.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:71:re-plan: fragile-premise (rows text-security:7771c92:1-6, text-security:e74aec4:1-2, text-security:9c5500f:1) — specification: every command the text prescribes has been executed by the orchestrator at authoring time on this host, under the clean prefix, and its pasted output stands beside it; a command that cannot be executed before dispatch is not written; design: the `## Commands` block carries, for each command, the execution timestamp and output (C-87 applied to the text itself), and the cap evidence command refuses a compare list of 300 files or one whose length differs from the PR's `changedFiles`; implementation: the amendment with the executed compare probe; verification: C-80 round 1 after this line.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:72:- 2026-10-20T02:38:42Z: amendment after re-plan 2: the compare completeness check (fewer than 300 files and equal to the PR's changedFiles) added to Commands (f) with its executed output (`ba318e53...118daafa`: files 7, total_commits 1, truncated false; PR #434 changedFiles 7); text sha256 9c5500f0… -> ed75bc62…, 188 lines, checker OK; C-80 round 1 after re-plan 2 running.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:73:- 2026-10-20T02:41Z: C-80 round 1 after re-plan 2 (`…-text-security-ed75bc6.md`) `Verdict: incorrect`, two P2 caused by the orchestrator's direct edit: the completeness requirement was prose inside the executable Bash block (`bash -n` exit 2), and dispatch required the PR's changedFiles that exists only after dispatch (circular). Fixed at 2026-10-20T02:42:13Z: an executable (f') line inside the block (refuse 300 files or a count that differs from changedFiles), the prose with the executed output below the block, (f)/(f') run at RESULT only; `bash -n` of the block verified; budget after re-plan 2: 1 of 3 used.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:76:- 2026-10-20T02:45Z: C-80 round 2 after re-plan 2 (`…-text-security-0ec4bb9.md`) `Verdict: incorrect`, one P2: gh's persistent configuration (hosts.yml api_host) can redirect requests despite --hostname, and the unqualified --repo can select another configured host. Fixed at 2026-10-20T02:47:12Z: Commands (e') isolates gh's configuration (a fresh GH_CONFIG_DIR and the keyring token read once by the bound gh; every gh call carries both; --repo github.com/mryfmo/dotfiles); executed on this host inside and outside the sandbox: token read (40 chars), main sha 118daafa, PR #434 changedFiles 7; `bash -n` of the block OK; C-80 round 3 after re-plan 2 running (the last of the budget).
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:78:- 2026-10-20T02:47:53Z: the configuration-isolation replace had also rewritten the trusted-parent launch line (undefined $GHC/$TOKEN at that point); the launch line restored without a token (the token is read inside by (e')); a review started on the intermediate bytes was stopped before it wrote anything (not consumed); text sha256 ad56c1a6… -> b657a897…; `bash -n` OK; checker OK; C-80 round 3 after re-plan 2 running on the corrected text.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:79:- 2026-10-20T02:52:55Z: C-80 round 3 after re-plan 2 (`…-text-security-b657a89.md`) `Verdict: incorrect` on one P2: the text (198 lines) exceeded its own 185-line sentence; "No additional security findings". Disposition by the orchestrator: the self-cap sentence set to 210 (proposal 1 allows 250), 199 lines; the review budget is spent and the finding is mechanical, so no further review; the task-level audit of the PR checks the contract. Dispatched to a013 (worker-h, the sixth seat, added by the orchestrator at 02:51Z); text sha256 59f91f5580892ddd58f10b538eb611e790200edf6d41ead1e63bd753e5d68fbd.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:84:- 2026-10-20T03:23:40Z: a013 PONG `alive`: the HTTPS push form succeeded inside the sandbox; PR #437 opened at head 4045295b (dispatch base 118daafa; main now 60a6fb2b); CI and the Bot window running; no worker update-branch or merge.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:85:- 2026-10-20T03:27:36Z: a013 PONG `blocked`: CI validate failed on #437 (run 39364020428, job 118436537807); the bound gh could not read the log (`creating cache entry: open $HOME/.cache/gh/run-log-…zip: operation not permitted`: the gh run-log cache lives under the home cache dir outside the Codex writable roots: C-94's remedy is XDG_CACHE_HOME under the worktree); Commands (f)/(f') pass (4 files, code 3/6, tests 19/40); the orchestrator reads the log.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:86:- 2026-10-20T03:31:08Z: the #437 validate job failed: `possible committed secret in .orchestration/dotfiles-T133-python-pin-a01/task.md` (SECRET_PATTERN matches `<redacted:secret-pattern>` at Commands lines 132/134/136, found by running the validator's pattern over the text); amendment: variable GH_AUTH and `GH_TOKEN=$GH_AUTH` (clean against the pattern); sha256 59f91f558089 -> 8e544c8a77ca; re-dispatched for the copy update; a013 told the C-94 remedy for gh run logs (XDG_CACHE_HOME under the worktree). Mechanism note: the pre-dispatch checker should run the validator's secret scan on the text (owner: the P1-12 a05-checker lineage, C16 sibling).
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:89:re-plan: text-defect (rows text-security:ed75bc6:1-2, text-security:b657a89:1, ci:32f400c:1) — specification: the task text passes, as one file, every machine check CI and the regime apply to it before any send: the consistency checker, the validator's SECRET_PATTERN over every line, no literal home path, its own line cap and `bash -n` over every fenced bash block; design: one pre-send command runs them all on the final bytes and prints the sha256 the dispatch line carries (`.agents/worklog/orchestrator-glue/pre-send.sh`; tracked home `dispatch.sh --next` in the loop-limits lineage); implementation: the line-199 note rewritten as a description, pre-send output `OK / secret-pattern: 0 match(es) / bash -n block 1: rc=0 / lines: 199`, sha256 8e544c8a… -> 30185a5a…; verification: CI `validate` on the next head of PR #437.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:91:- 2026-10-20T04:03:43Z: a013 RESULT `ready_for_review` for PR #437 head 09c81cc3 (base 60a6fb2b, task_sha256 30185a5a…); CI all green at 04:01Z (validate 2m14s, regime 14s, GitGuardian pass); the chain (`chain-integrate.sh … 437 … dotfiles-T133-python-pin-followup-a01`) and the security-profile review of 09c81cc3 started 04:08Z.
.orchestration/acceptance/dotfiles-T133-python-pin-a01.md:92:- 2026-10-20T04:24:57Z: the chain on the update-branch head e9819d45 (base check moved the PR: `gh pr update-branch`; CI green; local review 0 findings; sweep 9 items 0 gaps): task-level audit `…-audit-e9819d4.md` `Verdict: incorrect`: [P1] orchestration: INV-6 S2 exceeded on this lineage with no reset (measured 2026-10-20T04:39Z with scripts/regime-counters.sh: `tasks=3 amendments=2 questions=1 results=5 withdrawn=0 revises=4 first_result_head=none`; `S2: revises 4 >= 2`, `S2: amendments 2 >= 2`; the round=0 closures of blocked RESULTs count as revises); [P2] records: the JSON ledger, replans and searches were empty while the prose held 18 rows and three re-plan lines; [P2] specification: the dispatched text's Check (line 161-162) forbids dispatch until the failed Commands (a) probe is replaced while `premises` (line 76-81) still carries that failed `dscl` probe. Dispositions: P1 -> the lineage resets to `dotfiles-T133-python-pin-a02` written by the review profile (`python-pin-a02-prompt.md`), carrying the implementation at 09c81cc3 unchanged on PR #437 (a013 holds, PING `python-pin-hold.txt`); P2 records -> fixed in this record by `record-json-sync.py` (ledger 18 rows, replans 3) before any gate; P2 text -> fixed in the a02 text (premises carry only the probes executed read-only at 04:31:20Z: `id -P` home, python 3.15.0 realpath, gh 2.102.0 realpath, policy grep). No finding on the implementation.
.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md:143:- 2026-10-19T20:1xZ: dispatched to claude-standard-dot-a011 (worker-d; sha e21ef5bef826e9d5c195d8145c26810c2fa438cf1c4a86b16ba7477d23d14749); counters pasted; no C-80 (security: false).
.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md:146:- 2026-10-20T06:3xJST: lineage audit rows carried before the chain (interim P1-6 procedure, M-20261019-06): 22 prose rows added, JSON ledger 22.

**Optimizing audit log reads**
codex
改訂版は継承 `GIT_*` の除去と直接の shim 実行を避けています。次に、Git の設定経由の実行、実体パスの検証、承認ファイルの書き込み境界を、過去の指摘と照合します。読み取り専用のため worklog／証跡ファイルは作成しません。
exec
/bin/zsh -lc "cat .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md.last.md; sed -n '95,119p' .orchestration/plans/024-design-quality.md; cat .orchestration/validation/dotfiles-T133-python-pin-a01-audit-e9819d4.md.last.md; rg -n 'M-20261019-06' .orchestration/learning/mistakes; nl -ba scripts/orchestrator/acceptance-front-matter.py | head -130" in ~/Workspace/dotfiles
 succeeded in 96ms:
---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-record-json-sync-a01"
}
---

# Acceptance record: dotfiles-T133-record-json-sync-a01

- 2026-10-20T06:24Z: text written whole by the review profile from the orchestrator's brief (`dotfiles-T133-record-json-sync-a01-prompt.md`; security: true; promotes the glue record-json-sync.py (prose rows and re-plan lines into the JSON ledger and replans; audit e9819d4 P2, M-20261019-06) into scripts/orchestrator/record-json-sync.py with tests); trailing authoring commentary stripped by the orchestrator; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 4e3ec939… before the Checks paste. C-80 round 1 running; dispatch to an idle Claude seat after a correct verdict (files disjoint from every in-flight task).
- 2026-10-20T06:28Z: C-80 round 1 (`…-text-security-4e3ec93.md`) `Verdict: incorrect`: [P1] line 34: sandbox-only execution asserted while the current manifest excludes `gh *` on Linux for Claude seats (so a command could run outside without the promised refusal); [P2] line 88: the interpreter is selected through inherited `$HOME` and `dirname "$(command -v uv)"` restores the mise shim directory; [P2] line 94: `GIT_CONFIG_GLOBAL=/dev/null` leaves `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_COUNT` effective (a probe showed injected rewrite configuration survives); [P2] line 94: bare `gh` through the shim and `--repo mryfmo/dotfiles` without host binding; [P2] line 74: duplicate JSON keys collapse silently under default parsing. Amendment 1 by the review profile applies the python-pin a02 Commands pattern (passwd home, clean prefix, interpreter and gh by realpath, `GIT_*` unset, `--repo github.com/mryfmo/dotfiles`, fresh `GH_CONFIG_DIR`) and duplicate-key rejection; budget 2 of 3 next.
text-security:4e3ec93:1	excluded-command-trusts-sandbox-context
text-security:4e3ec93:2	tool-environment
text-security:4e3ec93:3	tool-environment
text-security:4e3ec93:4	repository-binding
text-security:4e3ec93:5	input-validation
- 2026-10-20T06:39Z: amendment 1 written whole by the review profile (`record-json-sync-a01-r2-prompt.md`, corrected for C-104 before the run) and installed: one `## Commands` block (platform, passwd home, clean prefix with the proxy variables, interpreter/uv/gh by realpath, GIT_* cleared by env -i), the Darwin statement in the Worker Playbook sentence, duplicate-key rejection, the exact `LEDGER_ID` shape quoted from scripts/require-crit-review.py:37; Checks section normalised; pre-send.sh: checker OK, SECRET_PATTERN 0, bash -n OK, home paths 0; 143 lines (self cap 150); sha256 4e3ec939… -> d899b844365703dcc8a33fccca822fad9c739d5d948a28efdd17919691f439ad. C-80 round 2 running (budget 2 of 3).

[P1] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:34](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:34) — Sandbox-only execution is asserted without a dispatch prerequisite or Codex-only restriction; the manifest defaults to Claude and excludes `gh *` on Linux, so commands can run outside the sandbox without triggering the promised refusal/PONG.

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:88](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:88) — The supposedly fixed interpreter is selected through inherited `$HOME`, while `dirname "$(command -v uv)"` restores this host’s mise-shim directory to PATH; `env -i` and `-I` do not authenticate either executable location, leaving the parent-binding mitigation incomplete.

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:94](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:94) — Clearing only `GIT_CONFIG_GLOBAL` leaves inherited `GIT_DIR`, `GIT_WORK_TREE` and `GIT_CONFIG_COUNT` effective, permitting repository substitution or URL rewriting; a read-only probe confirmed that injected rewrite configuration survives this exact credential-helper prefix. [Git configuration](https://git-scm.com/docs/git-config).

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:94](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:94) — Both the credential helper and PR creation rediscover bare `gh` through this host’s mise shim, and `--repo mryfmo/dotfiles` leaves the host unbound; checkout configuration and inherited `GH_HOST` can therefore change execution or destination despite the reviewed command text. [Mise](https://mise.jdx.dev/dev-tools/shims.html), [gh environment](https://cli.github.com/manual/gh_help_environment).

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:74](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:74) — The malformed-input contract and fixtures omit duplicate JSON keys: default parsing silently collapses duplicate `ledger` fields, potentially deleting findings and converting a record the existing gate rejects into an accepted object; require duplicate-key rejection with byte-identical preservation. [Python JSON behavior](https://docs.python.org/3/library/json.html#repeated-names-within-an-object).

All allowed-file entries have threat rows. Static symlink confinement is required; unrestricted concurrent replacement and shared credentials are explicitly residual, without a claim of host isolation.

📝 まとめ: Completed the read-only design review and checked the cited acceptance/audit context; five findings are submitted for orchestrator disposition.
Not checked: implementation, CI or deployed Linux enforcement; no files changed, and the execution-binding gaps remain unverified.
Verdict: incorrect### 5.14 残余（凍結後の計測事実、D-024-29）

- 2026-10-20: 項目 2 の「passwd home を dscl/getent で読む」は、両席の sandbox 内で `dscl` が失敗する（Claude sandbox: `Operation failed with error: eServerError`、Codex sandbox: exit 70、helper task RESULT）ため、同じディレクトリサービスを libc 経由で読む `/usr/bin/id -P | cut -d: -f9`（macOS）/ `getent passwd "$(id -un)" | cut -d: -f6`（Linux）/ Python の `pwd.getpwuid(os.getuid()).pw_dir` を passwd home の読み方とする。項目の意図（HOME は passwd のもの、継承値ではない）は不変。

5.12 **プログラム仕様** は `024-design-programs.md` に分離（17 項目: verdict.sh、audit-pool.sh と orch-audit.sh --json、schemas、result-precheck.sh、dispositions.py、regime.yml、dispatch.sh --next、acceptance-front-matter.py、git hooks、handoff.sh、flakes、task-from-plan.py）。

結論: 第 1 段階で消えるのは今の直列点（S1 の一部、S2、S8 の一部）。残る天井は S3（hosted runner）、S4/S5（モデルと監査の枠）、S7（hot spot）で、これらは席数の上限 D10（4 → 6）の根拠になる。6 を超える並列は、S3 と S5 の実測が出るまで plan に入れない。

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
The implementation matches the requested pin and tests; three defects remain in the orchestrator’s artifacts.

[P1] high orchestration .orchestration/acceptance/dotfiles-T133-python-pin-a01.md:9 The record documents at least five RESULTs and three TASK dispatches, exceeding INV-6’s two-revise/two-amendment thresholds, but contains no counter snapshot or required independent design reset; marking continuations `round=0` does not exclude blocked RESULTs from those counts.

[P2] high orchestration .orchestration/acceptance/dotfiles-T133-python-pin-a01.md:15 The machine-readable `ledger`, `replans`, and `searches` are empty despite repeated findings and three prose replans; the gate reads these JSON fields, so it cannot enforce S1/S6 against the recorded history.

[P2] high specification .orchestration/dotfiles-T133-python-pin-a01/task.md:162 The dispatched specification still prohibits dispatch until its failed prerequisite evidence is replaced, while `premises` retains that failure; appended successful probes do not reconcile this contradictory completion condition.

The task declares no numbered invariants; these audit labels enumerate its explicit obligations:

INV-1: holds home/dot_mise/config.toml:5 — exact `3.15.0` pin and required reason.
INV-2: holds tests/unit/test_mise_config.py:8 — one test, ASCII fullmatch, four required negatives; recorded red/green matches the implementation.
INV-3: holds tests/unit/test_supply_chain_policy.py:375 — Python exception preserves other tools’ policy.
INV-4: holds .orchestration/dotfiles-T133-python-pin-a01/task.md:174 — four allowed paths, 3/6 code lines, 19/40 test additions, 200/210 task lines.
INV-5: holds .orchestration/dotfiles-T133-python-pin-a01/task.md:181 — dispatched copy and SHA-256 match.
INV-6: violated .orchestration/acceptance/dotfiles-T133-python-pin-a01.md:9 — regime reset thresholds were not handled.
INV-7: violated .orchestration/dotfiles-T133-python-pin-a01/task.md:162 — prerequisite evidence remains contradictory.

[PR #437](https://github.com/mryfmo/dotfiles/pull/437)’s final-head CI passed. Design §5.14’s declaration requirement is satisfied; executable provenance and deployment remain explicitly residual.

Orchestration findings: 3

📝 まとめ: Read-only audit completed; implementation checks passed, with three artifact findings requiring disposition.
Not rerun: full tests, Bats, or deployment. Runtime provenance remains unverified; nothing was modified.
Verdict: incorrect.orchestration/learning/mistakes/M-20261019-06-record-automation-gaps-recur.md:2:id: M-20261019-06
     1	"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]
     2	
     3	Write or update the JSON block of `.orchestration/acceptance/<task>.md` in this checkout (plan 007 T718, a05 item 1;
     4	plan 013 A′, C-24, C-26): the object between the record's first two `---` lines that the gate reads. `head` is
     5	`git -C <pr-worktree> rev-parse HEAD` and must equal the sweep JSON's `head_sha`; `pr` is the sweep JSON's own `pr`.
     6	`ledger` keeps every row the record has and adds each `--ledger` row (`id<TAB>class`) whose id is new; a row whose
     7	id is present is printed as kept-ledger-row. `searches` is recomputed by the gate's rule: each class with three or
     8	more rows, with the sorted basenames of the mistake records naming it. `audit_findings` come from
     9	`--audit-dispositions` (`n<TAB>reason<TAB>evidence`), required when the audit summary orch-audit.sh writes beside
    10	its receipt (`.orchestration/validation/<task>-audit-<sha7>.md.last.md`) ends in `Verdict: incorrect`, refused
    11	otherwise; the record is written before the audit (the audit reads it) and again after an incorrect one. A record
    12	that starts with a `---` block is read with the gate module's reader (duplicate keys refused) and keeps its text
    13	after the block and its `dispatch` list; a prose record gets the block prepended. `replans`, the C-59 re-plans
    14	(`{<class slug>: {specification, design, implementation, verification}}`, each a non-empty string), is kept as found
    15	and written `{}` when absent; another shape exits 2 naming the key. The gate module's field checks run on the new
    16	block, and any refusal exits 1 before anything is written.
    17	"""
    18	
    19	import argparse
    20	import collections
    21	import importlib.util
    22	import json
    23	import re
    24	import subprocess
    25	import sys
    26	from pathlib import Path
    27	
    28	
    29	def refuse(message):
    30	    sys.exit(f"acceptance-front-matter: {message}; nothing written")
    31	
    32	
    33	def git(*args):
    34	    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()
    35	
    36	
    37	def rows(path, width):
    38	    """The `width`-field rows of a TSV file, blank and `#` lines skipped."""
    39	    lines = Path(path).read_text().splitlines() if path else []
    40	    found = [line.split("\t") for line in lines if line.strip() and not line.startswith("#")]
    41	    for fields in found:
    42	        if len(fields) != width:
    43	            refuse(f"{path}: a row needs {width} tab-separated fields: {fields!r}")
    44	    return found
    45	
    46	
    47	def main():
    48	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    49	    parser.add_argument("task")
    50	    parser.add_argument("sweep")
    51	    parser.add_argument("pr_worktree")
    52	    parser.add_argument("--ledger")
    53	    parser.add_argument("--audit-dispositions")
    54	    args = parser.parse_args()
    55	    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.task):
    56	        parser.error(f"not a task id: {args.task!r}")
    57	    root = Path(git("-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"))
    58	    spec = importlib.util.spec_from_file_location("require_crit_review", root / "scripts/require-crit-review.py")
    59	    gate = importlib.util.module_from_spec(spec)
    60	    spec.loader.exec_module(gate)
    61	
    62	    try:
    63	        sweep = json.loads(Path(args.sweep).read_text(), object_pairs_hook=gate.refuse_duplicate_keys)
    64	    except ValueError as error:
    65	        refuse(f"{args.sweep}: {error}")
    66	    head = git("-C", args.pr_worktree, "rev-parse", "HEAD")
    67	    if sweep.get("head_sha") != head:
    68	        refuse(f"the sweep was collected for head {sweep.get('head_sha')!r}, not {args.pr_worktree}'s HEAD {head}")
    69	
    70	    path = root / ".orchestration/acceptance" / f"{args.task}.md"
    71	    text = path.read_text() if path.is_file() else ""
    72	    record, rest = {}, text
    73	    if text.split("\n")[0] == "---":
    74	        record, error = gate.read_acceptance_record(path)
    75	        if error:
    76	            refuse(error)
    77	        lines = text.split("\n")
    78	        rest = "\n".join(lines[lines.index("---", 1) + 1 :])
    79	    replans, parts = record.get("replans", {}), ", ".join(gate.REPLAN_KEYS)
    80	    if not isinstance(replans, dict):
    81	        parser.error(f"replans must be {{<class slug>: {{{parts}}}}}; nothing written")
    82	    for cls, entry in replans.items():
    83	        if not gate.CLASS_SLUG.fullmatch(cls) or not gate.replan_complete(entry) or set(entry) != set(gate.REPLAN_KEYS):
    84	            parser.error(f"replans.{cls} must be {{{parts}}}, each a non-empty string; nothing written")
    85	
    86	    ledger = list(record.get("ledger", []))
    87	    present = {str(row.get("id")) for row in ledger if isinstance(row, dict)}
    88	    for row_id, cls in rows(args.ledger, 2):
    89	        if row_id in present:
    90	            print("kept-ledger-row", row_id)
    91	        else:
    92	            ledger.append({"id": row_id, "class": cls})
    93	            present.add(row_id)
    94	
    95	    summary = root / f".orchestration/validation/{args.task}-audit-{head[:7]}.md.last.md"
    96	    audit = summary.read_text() if summary.is_file() else ""
    97	    # The gate's verdict rule: the summary's last non-blank line.
    98	    last = [line for line in audit.splitlines() if line.strip()][-1:]
    99	    verdict = (match := gate.AUDIT_VERDICT.fullmatch(last[0]) if last else None) and match.group(1)
   100	    incorrect = verdict == "incorrect"
   101	    if incorrect != (args.audit_dispositions is not None):
   102	        refuse(
   103	            f"--audit-dispositions is {'required' if incorrect else 'refused'}: {summary.name} {verdict or 'missing'}"
   104	        )
   105	    findings = [
   106	        {"n": n, "reason": reason, "evidence": evidence} for n, reason, evidence in rows(args.audit_dispositions, 3)
   107	    ]
   108	
   109	    classes = collections.Counter(
   110	        row["class"] for row in ledger if isinstance(row, dict) and isinstance(row.get("class"), str)
   111	    )
   112	    searches = []
   113	    for cls in sorted(c for c, count in classes.items() if count >= gate.S6_CLASS_LIMIT):
   114	        found = gate.mistake_records(root, cls)
   115	        if isinstance(found, str):
   116	            refuse(found)
   117	        searches.append({"class": cls, "records": sorted(found)})
   118	
   119	    block = {**record, "format": gate.RECORD_FORMAT, "task": args.task, "head": head, "pr": sweep.get("pr")}
   120	    block.update(ledger=ledger, searches=searches, audit_findings=findings, replans=replans)
   121	    errors = gate.record_field_errors(block, args.task, head, sweep.get("pr"))
   122	    if not errors and incorrect:
   123	        errors = gate.audit_findings_errors(block, len(gate.AUDIT_FINDING.findall(audit)))
   124	    if errors:
   125	        refuse("; ".join(errors))
   126	    path.parent.mkdir(parents=True, exist_ok=True)
   127	    path.write_text("---\n" + json.dumps(block, indent=2, sort_keys=True, ensure_ascii=False) + "\n---\n" + rest)
   128	    print("written", path.relative_to(root), "head", head[:7], "pr", block["pr"], "ledger", len(ledger))
   129	
   130	

**Reviewing git config and test symlink issues**
**Assessing validation, serialization, and auth issues**

I'm analyzing missing validation for task identities, focusing on case-insensitive file rewrites without data loss and ensuring proper canonical protection within the repo. I’m refining serialization to handle NaN values correctly and reviewing security controls around file and row closures in scripts. There’s a conflict with existing row design needing caution during replans. Lastly, I’m investigating GitHub config and authentication—confirming that without a GH_TOKEN, certain tasks can’t complete due to dropped token provisioning, so I’m checking official docs carefully.
web search: 
exec
/bin/zsh -lc "sed -n '109,110p' .orchestration/plans/024-design-quality.md; cat .orchestration/learning/mistakes/M-20261019-06-record-automation-gaps-recur.md; rg -n 'excludedCommands|gh \\*|linux|worker_kind' home/dot_agents/agent-config.yaml | head -45; rg -n 'D-024-(29|30)' .orchestration/decisions.tsv; sed -n '1,65p' scripts/orchestrator/orch-gate.sh; sed -n '1,55p' .agents/worklog/orchestrator-glue/record-json-sync.py; /usr/bin/env -i PATH=/usr/bin:/bin HOME=/nonexistent /usr/bin/git -c url.https://example.invalid/.insteadOf=https://github.com/ -c remote.review.url=https://github.com/mryfmo/dotfiles.git remote get-url review" in ~/Workspace/dotfiles
 exited 2 in 109ms:
3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
---
id: M-20261019-06
date: 2026-10-19
classes: [dispatch-record-markers, ledger-row-missing, ledger-completeness]
severity: P2
---

# The two record-automation gaps of P1-6 recurred across five PRs in one night

**What happened.** On 2026-10-19/20 the integration chain refused five PRs at its audit precheck for missing lineage ledger rows (#402, #411, #430, #375 twice, #433), each time because the orchestrator had carried the predecessor audits' `audit:<sha7>:<n>` rows into the JSON block but not as the prose rows `ledger-check.py` reads, or not at all; and three task-level audits of the assets lineage (725b25b:4, 4e743a1:1, 9bff92b:1) found the record's `dispatch` array empty although the TASK and ACCEPTANCE lines had `read_at` timestamps on the bus. Each time the orchestrator repaired the record by hand from the lineage records or messages.db and re-ran the chain (about 10 minutes per refusal).

**What the rules say.** Plan 024 P1-6 (record automation and `dispatch.sh --next`) owns both: the record is generated from the RESULT and the bus, and the chain carries lineage rows itself. The gate reads prose rows for ledger-check and the JSON block for the ledger; both must be written together. C-87/C-89: every figure is pasted command output, consumers enumerated before dispatch.

**Why the rules did not fire.** P1-6 was sequenced after the mechanisms it depends on (dispatch.sh is in loop-limits-a01's allowed_files; acceptance-front-matter.py too), so no task text existed and the orchestrator kept doing the two steps by hand, each time one record later than the chain needed them. The S1 count for `dispatch-record-markers` reached three only at 9bff92b because the class slug stayed stable (C-93 worked); the ledger-carry gap had no class row at all because the chain's refusal is not an audit finding.

**Mechanism.** (1) Interim glue, in use from this record on: `fill-dispatch.py <task>` fills the dispatch array from messages.db, and a lineage-row carry (prose and JSON) runs before every chain, both in `.agents/worklog/orchestrator-glue/`. (2) P1-6's first slice, written after loop-limits-a01 merges: dispatch.sh appends the sent line to the record at send time; chain-integrate.sh (or acceptance-front-matter.py) carries every lineage audit row into both the prose rows and the JSON ledger before the precheck, and ledger-check.py reads the JSON ledger as well. (3) The chain's refusal rc=3 is recorded as a ledger-completeness row in the record it refused, so the class count is visible.
71:worker_kind: claude
285:    excludedCommands:
293:    linux_excluded_commands:
294:      - gh *
413:        linux-x64: 04147c68e946902f5226dfdcd54d19907aed3cf54d95b2f27d2b9c778bb26f9e
414:        linux-arm64: e79866e32624b346f6854d93ca8a24294516cd7c0b48ce0e80af508fb7c3d8b8
425:        MISE_FALLBACK_LINUX_X64_SHA256: fallback.sha256.linux-x64
426:        MISE_FALLBACK_LINUX_ARM64_SHA256: fallback.sha256.linux-arm64
440:      linux-x86_64: b7c232b0e8249d8e55a40beb79c5c43a7d370f3f9408bd215deb0170daeaadf3
441:      linux-aarch64: dc30189378d2f2e287384e8a692d3f95ad1df64cf0e8c36aa9201516028aed6b
449:        STARSHIP_X86_64_SHA256: sha256.linux-x86_64
450:        STARSHIP_AARCH64_SHA256: sha256.linux-aarch64
488:        linux-amd64: b597729b687af4488a848240134cb633de8ca0f04e0d26d48f400ee2ac338ffa
489:        linux-arm64: abcb840401d3c1f2356e0f53f5d52aa10d10f572654d9626db9ad0ca4dc03355
499:        CHEZMOI_FALLBACK_LINUX_AMD64_SHA256: fallback.sha256.linux-amd64
500:        CHEZMOI_FALLBACK_LINUX_ARM64_SHA256: fallback.sha256.linux-arm64
548:      linux-amd64: 38b4424fb335cd6faa70010823682e53a4a2e29e31a36a977874a13f11ad0992
549:      linux-arm64: 278202e8eedce8a838785be8153b26b36fee0662640fc838fc7048da01aaba81
553:      linux-amd64: https://files.pythonhosted.org/packages/21/fb/0a48f19a1c39b4ff59412f1fe34130c14acbc55da69097018d729191c6d2/hcom-0.7.30-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
554:      linux-arm64: https://files.pythonhosted.org/packages/f0/23/e746ce90643a1286ed3c6410c66eaae7134fbd2267d002814e6a932a2b60/hcom-0.7.30-py3-none-manylinux_2_28_aarch64.whl
561:      constants: {HCOM_PIN_VERSION: pin, HCOM_DARWIN_ARM64_SHA256: sha256.darwin-arm64, HCOM_DARWIN_AMD64_SHA256: sha256.darwin-amd64, HCOM_LINUX_AMD64_SHA256: sha256.linux-amd64, HCOM_LINUX_ARM64_SHA256: sha256.linux-arm64}
568:      linux-amd64: fecd40eea356020cd605dfca6a4be6ab3c9635134ca5e28ee99e6286ab62c31d
569:      linux-arm64: 92311ddf4862179c655087d4703e7f2e3f4b4aacb0549c22e5dae999c0fb2b6e
579:        CRIT_LINUX_AMD64_SHA256: sha256.linux-amd64
580:        CRIT_LINUX_ARM64_SHA256: sha256.linux-arm64
77:D-024-29	2026-10-19T21:39Z	Design 5.14 is frozen (plan 006 A1: three review rounds, then freeze with a residual list): items 0-10 are the contract; a text review finding that needs a new design sentence is recorded in the design's residual list and as an owner row, not as an amendment of the item and of the text under review, unless it names a P0/P1 that is exploitable in the proposed implementation.	items 1, 2, 3, 8 and 9 were amended five times on 10-19/20 (one per review round of P1-15 and P1-12), each amendment re-opening the texts that quote the item (C-88) and costing a review round each; the texts chased a moving design.	plan 006 A1; M-20261019-05; C-92	applied from 06:40 JST; the residual list is a new subsection `5.14 残余` in 024-design-quality.md (written at the next design edit)
78:D-024-30	2026-10-19T23:16Z	A task text applies design 5.14 by reference: it names the items it relies on (`design: 5.14 items 2, 3, 8, 9`) and carries one threat row per item 0-10 in the item's own words, never a restated or paraphrased copy of the item; C-88 is narrowed to the exact contract sentences a test asserts; the task-consistency check gains a rule (C16) that a security: true orchestrator-side text names 5.14 and has the per-item rows (owner: the P1-12 follow-up after a04 frees task-consistency-check.py).	restated design text drifted in every reset text and re-opened a review round at each design amendment (P1-15: 23 review rounds; P1-12: 4); by-reference texts stay within proposal 1's caps and a mechanical check replaces the reviewer's paraphrase comparison; the operator's direction of 2026-10-19T22:59Z (relayed by a011) asks for the same.	plan 006 A1; D-024-29; M-20261019-05; proposal 1	applied from 08:15 JST to new texts (trusted-exec-contract-tests-a01 first); existing correct texts are not rewritten
82:D-024-34	2026-10-20T04:12Z	The files the worker's loader consumes at start and the regime need not preserve are launcher-generated at every start: the global state file `CLAUDE_CONFIG_DIR/.claude.json` is written from the declared shape (empty `mcpServers`, `projects` with exactly the validated identities and Boolean trust, `hasCompletedOnboarding: true`) plus identity fields carried from the previous file after screening (`oauthAccount` string members, `userID`); native persisted state (`numStartups`, onboarding, tips and changelog caches, per-project history, allowedTools, cost counters) is neither screened nor preserved; refusal with a named message stays for declared-structure violations (non-empty top-level `mcpServers`, undeclared project keys, non-Boolean trust flags, undeclared object or array members), as evidence of tampering. `CLAUDE_ENV_FILE` (amendment 1) belongs to the same family. A loader that requires another preserved field blocks and retasks (the text's rule), never widens silently.	a010's probe of the installed loader (2.1.300, sha256 475517ca…; reproduced by the orchestrator at 04:10Z) shows the loader itself writes fields outside any exact schema, so the allowlist re-plan's closed schema (D-024-29/30 lineage, a02 -> a03) refuses the worker's own state at the next start; a per-version native-field table would block every loader update until re-probed; generating the file realises design 5.14 item 1 (refuse any executable payload it did not write) by writing the whole file. Second re-plan of the input-inventory family (rows text-security:f7af699:1, worker:5067ed0:1 after the allowlist re-plan).	design 5.14 item 1; D-024-29; D-024-30; a03 record rows; M-20261019-05	applied 13:12 JST as a03 amendment 2 (review-profile text, C-80 round 3); the operator may redirect it once per class (the 13:15 JST report)
#!/usr/bin/env bash
# @file orch-gate.sh
# @brief Run the integration gate on a PR checkout's head from the review worktree, with the task's evidence copied in.
# @description
#   Plan 007 T718, the parameterised form of the orchestrator's gate wrapper. The head is always `git -C
#   <pr-worktree> rev-parse HEAD`. From the checkout this script lives in, it requires the task's sweep JSON (whose
#   `pr` must be <pr>), the audit of this head and its `.last.md`, the review receipt, the crit JSON and the
#   acceptance record, all under `.orchestration/`, before it checks the clean review worktree
#   `.claude/worktrees/orchestrator-review` out at the head; a head that tracks a symlink under `.orchestration`
#   is refused, so no copy follows a link out of the worktree. It copies them in and runs, with the review worktree
#   as its working tree, the gate `make require-crit-review` runs, but this checkout's copy: the head's Makefile
#   and gate are PR-controlled (PR #350 thread 4265190252), so `scripts/require-crit-review.py` and the validator
#   it loads must equal origin/main's here. The interpreter is `uv python find` in this checkout, resolved before
#   the review worktree is entered and run directly, so no uv reads the head's `.python-version` or `uv.toml`
#   (uv runs an executable a `.python-version` names; the audit of f48593d6). The gate runs under `env -i` with
#   HOME as this shell has it, a PATH of one private directory of links to `gh` and `git` as this checkout resolves
#   them (`mise which` under `env -i`, else `command -v`; a path under a `shims` directory or none is refused), its
#   inputs AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE, PR_FEEDBACK_EVIDENCE, REVIEW_EVIDENCE and AGENT_REVIEWED=1, and
#   PYTHONSAFEPATH=1, as `-I -P <gate> --base origin/main`: nothing else of this shell or of the head reaches the
#   gate or the collector and gh it starts (the audits of a06c874e and 6847aa9f). A trap set before the private
#   directory is made removes it whatever fails or the gate says, and once the head's checkout has started restores
#   the review worktree to origin/main; a refusal before that leaves the review worktree as it was (the audit of
#   a235637).
# @arg $1 string Task id.
# @arg $2 path The PR's checkout (its HEAD is the gated head).
# @arg $3 int PR number.
# @exitcode 0 The gate passed.
# @exitcode 2 Usage error, or a refused precondition.
# @exitcode * Otherwise the gate's own status.
# @example
#   scripts/orchestrator/orch-gate.sh dotfiles-T128-orchestrator-tools-a05 .claude/worktrees/worker-c 350
set -euo pipefail

usage() {
    echo "usage: orch-gate.sh <task> <pr-worktree> <pr>" >&2
    exit 2
}
refuse() {
    echo "orch-gate: $1; refused" >&2
    exit 2
}
(($# == 3)) || usage
task=$1 pr=$3
[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && ${pr} =~ ^[0-9]+$ ]] || usage
head="$(git -C "$2" rev-parse HEAD)"
root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
review="${root}/.claude/worktrees/orchestrator-review"
v=.orchestration/validation
sweep="${v}/${task}-pr-feedback.json" audit="${v}/${task}-audit-${head:0:7}.md"
record=".orchestration/acceptance/${task}.md" receipt="${v}/${task}-review-receipt.md"
evidence=("${sweep}" "${audit}" "${audit}.last.md" "${receipt}" "${v}/${task}-crit.json" "${record}")
cd -- "${root}"
git diff --quiet origin/main -- scripts/require-crit-review.py scripts/validate-agent-assets.py ||
    refuse "the gate here differs from origin/main's"
for f in "${evidence[@]}"; do
    [[ -f ${f} ]] || refuse "${f} is missing"
done
[[ $(jq -r .pr "${sweep}") == "${pr}" ]] || refuse "${sweep} is not the sweep of PR ${pr}"
[[ -z $(git ls-tree -r "${head}" -- .orchestration | awk '$1 == "120000"') ]] ||
    refuse "${head:0:7} tracks a symlink under .orchestration (PR #350 thread 4265190259)"
python="$(uv python find)" || refuse "uv found no interpreter in ${root}"
[[ -z $(git -C "${review}" status --porcelain --untracked-files=all) ]] || refuse "the review worktree is not clean"
trap '[[ -z ${bin:-} ]] || rm -rf -- "${bin}"
[[ -z ${moved:-} ]] || { git -C "${review}" clean -fdq -- .orchestration; git -C "${review}" checkout -qf --detach origin/main; }' EXIT
bin="$(mktemp -d "${TMPDIR:-/tmp}/orch-gate.XXXXXX")"
"""record-json-sync.py <task>: copy a record's prose rows (`<id>\t<class>`) into the JSON front matter's `ledger`
and its `re-plan: <class> (…) — specification: …; design: …; implementation: …; verification: …` lines into
`replans`, so the gate reads what the prose says (audit e9819d4 P2, M-20261019-06). Idempotent; prose unchanged."""
import json, pathlib, re, sys
task = sys.argv[1]; p = pathlib.Path(f'.orchestration/acceptance/{task}.md'); text = p.read_text()
head, fm, body = text.split('---\n', 2); assert head == '', 'front matter must start the file'
rec = json.loads(fm)
rows = [(i, c) for i, c in re.findall(r'^([a-z-]+:[0-9a-f]{7,}:[0-9-]+|[0-9]+)\t([a-z-]+)\s*$', body, re.M) if re.fullmatch(r'\d{10,}|audit:[0-9a-f]{7}:\d+', i)]  # scripts/require-crit-review.py LEDGER_ID  # the JSON ledger takes audit rows and thread ids only (acceptance-front-matter.py); other prose rows stay prose
have = {e.get('id') for e in rec.get('ledger', [])}
added = 0
for rid, cls in rows:
    if rid not in have:
        rec.setdefault('ledger', []).append({'class': cls, 'id': rid}); have.add(rid); added += 1
keys = ('specification', 'design', 'implementation', 'verification')
replans = rec.get('replans') or {}
for m in re.finditer(r'^re-plan: ([a-z-]+) \((.*?)\) — (.*)$', body, re.M):
    cls, rest = m.group(1), m.group(3)
    parts = {}
    for k in keys:
        mm = re.search(rf'(?:^|; ){k}: (.*?)(?=; (?:specification|design|implementation|verification): |$)', rest)
        if mm: parts[k] = mm.group(1).strip()
    if set(parts) == set(keys) and all(parts.values()):
        replans[cls] = parts  # the last line for a class wins
    else:
        print(f'warning: re-plan line for {cls} lacks a part: {sorted(set(keys) - set(parts))}', file=sys.stderr)
rec['replans'] = replans
p.write_text('---\n' + json.dumps(rec, indent=2, sort_keys=True, ensure_ascii=False) + '\n---\n' + body)
print(f'{task}: ledger +{added} (now {len(rec.get("ledger", []))}), replans {sorted(replans)}')
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
error: No such remote 'review'

web search: https://git-scm.com/docs/git-config
**Troubleshooting git remote issues**
**Analyzing Python environment and git object discrepancies**

I'm piecing together suspicious Python shim behaviors involving symbolic links and sandbox proxy settings, alongside git local object replacements that complicate verification and auditing processes. There’s a tricky overlap between residual evidence and validation that I want to separate into clear findings.
web search: 
exec
/bin/zsh -lc "/usr/bin/env -i PATH=/usr/bin:/bin HOME=/nonexistent GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null /usr/bin/git -c url.https://example.invalid/.insteadOf=https://github.com/ ls-remote --get-url https://github.com/mryfmo/dotfiles.git; sed -n '277,299p' home/dot_agents/agent-config.yaml; rg -n 'NaN|parse_constant|ledger row|row.get\\(\"id\"|LEDGER_ID' scripts/require-crit-review.py | head -25; /usr/bin/shasum -a 256 .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md" in ~/Workspace/dotfiles
 succeeded in 53ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
https://example.invalid/mryfmo/dotfiles.git
    enabled: true
    # Two-stage rollout: warn and run unsandboxed while bwrap/socat are missing;
    # flip to true only after live E2E.
    failIfUnavailable: false
    autoAllowBashIfSandboxed: true
    allowUnsandboxedCommands: true
    # Patterns need a trailing wildcard for arguments; every chained command must match.
    # Exclusion retains the normal permission flow (sandboxing docs, T130).
    excludedCommands:
      # agmsg-dispatch: inserts one agmsg row and sends a herdr wake. From
      # sandboxed Bash the herdr socket is PermissionDenied (T39 leg 1);
      # outside the sandbox it delivered msgs 545-577 with read_at within
      # seconds (T49 E2E, 2026-10-01).
      - agmsg-dispatch *
    # Linux blocks gh's keyring and herdr-agents -> actas-claim.sh socket calls;
    # child-script patterns cannot match the parent, but the absolute pattern covers direct calls.
    linux_excluded_commands:
      - gh *
      - herdr-agents *
      - "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *"
    filesystem:
      # Rendered into sandbox.filesystem.allowWrite after the Codex writable
      # roots. ~/.cache/uv: every `uv run` target (make unit-test,
37:LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")
745:    """json.loads accepts NaN and Infinity by default; a record field never needs one."""
757:        data = json.loads(block, object_pairs_hook=refuse_duplicate_keys, parse_constant=refuse_non_finite)
821:                or not LEDGER_ID.fullmatch(str(row["id"]))
826:                    f"ledger row {index} must be {{id: <thread id or audit:<sha7>:<n>>, class: <[a-z0-9-] slug>}}: {row!r}"
d899b844365703dcc8a33fccca822fad9c739d5d948a28efdd17919691f439ad  .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md

web search: 'insteadOf'
**Analyzing messaging sandbox conflicts**
**Checking readlink compatibility**
codex
具体的な不整合が見つかりました。Git は環境変数を消しても設定ファイルを読み、固定した HTTPS URL も書き換えられます。また Darwin でも `agmsg-dispatch` は sandbox 除外に残っており、「messaging を含む全コマンドが sandbox 内」という記述と衝突します。既に明記された同一 UID の競合リスクとは分けて報告します。
web search: 
exec
/bin/zsh -lc "/usr/bin/python3 -I -c 'import json,pathlib; p=pathlib.Path(\"~/.claude/settings.json\"); d=json.loads(p.read_text()); s=d.get(\"sandbox\",{}); print(json.dumps({k:s.get(k) for k in (\"enabled\",\"failIfUnavailable\",\"allowUnsandboxedCommands\",\"excludedCommands\")},indent=2))'; sed -n '730,767p' scripts/require-crit-review.py; sed -n '808,830p' scripts/require-crit-review.py; rg -n '441|C-104|record-json-sync|ledger row 0' .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log" in ~/Workspace/dotfiles
 succeeded in 265ms:
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
{
  "enabled": true,
  "failIfUnavailable": false,
  "allowUnsandboxedCommands": true,
  "excludedCommands": [
    "agmsg-dispatch *"
  ]
}
        )
    return errors


def refuse_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    """json.loads keeps the last of two equal keys; the record's reader refuses them instead."""
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise ValueError(f"acceptance record: duplicate key {key}")
        seen.add(key)
    return dict(pairs)


def refuse_non_finite(name: str) -> object:
    """json.loads accepts NaN and Infinity by default; a record field never needs one."""
    raise ValueError("acceptance record: non-finite number")


def read_acceptance_record(path: Path) -> tuple[dict | None, str | None]:
    """Load the record's JSON block between its first two --- lines with the standard library only."""
    # Both delimiters are whole lines that are exactly `---`: `---junk` closes nothing.
    lines = path.read_text().split("\n")
    if lines[0] != "---" or "---" not in lines[1:]:
        return None, "acceptance record must start with a JSON block between two lines that are exactly ---"
    block = "\n".join(lines[1 : lines.index("---", 1)])
    try:
        data = json.loads(block, object_pairs_hook=refuse_duplicate_keys, parse_constant=refuse_non_finite)
    except json.JSONDecodeError as error:
        return None, f"acceptance record: the block between the first two --- lines is not JSON: {error}"
    except ValueError as error:
        return None, str(error)
    if not isinstance(data, dict):
        return None, "acceptance record: the block must be one JSON object"
    return data, None


def is_int(value: object) -> bool:
    if not is_int(record.get("format")) or record["format"] != RECORD_FORMAT:
        errors.append(f"format must be {RECORD_FORMAT}")
    ledger = record.get("ledger")
    if not isinstance(ledger, list):
        errors.append("ledger must be a list of {id, class} rows")
    else:
        for index, row in enumerate(ledger):
            # A thread id may be a JSON number or a string; the id is its text either way.
            if (
                not isinstance(row, dict)
                or set(row) != {"id", "class"}
                or not isinstance(row["id"], (int, str))
                or isinstance(row["id"], bool)
                or not LEDGER_ID.fullmatch(str(row["id"]))
                or not isinstance(row["class"], str)
                or not CLASS_SLUG.fullmatch(row["class"])
            ):
                errors.append(
                    f"ledger row {index} must be {{id: <thread id or audit:<sha7>:<n>>, class: <[a-z0-9-] slug>}}: {row!r}"
                )
    searches = record.get("searches")
    if not isinstance(searches, list):
        errors.append("searches must be a list of {class, records} entries")
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:8:    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-regime-ci-fixture-grammar-a01 status=pending-integration round=1 pr=441 head=e51fee5b29ad97e4f2c5ed20ba3bffcc1ffd9c38 reason=RESULT-of-05:39:29Z-read:five-rows-on-one-module-constant,module-16/16-before-and-after,caps-0/11-of-12,CI-11/11;no-finding-on-the-change;one-records-step-before-the-chain,already-asked-in-PING-2748:the-task-copy-must-equal-the-amendment-2-text(509e4c54…);push-it-and-re-send-the-RESULT-with-the-new-head;then-sweep,audit,gate,merge-ahead-of-#440"
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:13:  "pr": 441,
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:26:- 2026-10-20T05:39:29Z: a009 RESULT round 1 `status=ready_for_review`: PR #441 head e51fee5b (code head 15bc046e, base 60a6fb2b), five rows read the module constant `RESIDUAL` (276 an f-string, still removing exactly the ROWS src/tool.sh row); module 16/16 OK before (60a6fb2b) and after (15bc046e), with the proxy variables; caps 0 outside, 11/12 under tests; CI 11/11 pass; Codex Bot unavailable (usage limits at 05:10Z); self-review 1 round (2 P3 resolved); INV-6 amendments 1, questions 2, revises 0. Gap found at 2026-10-20T05:42Z: the task copy on the branch (sha256 c2bfda03…) is the amendment-1 text; the latest dispatched text is amendment 2 (2732, 04:53:03Z, 509e4c54…, unread on the bus: a009's session restarted). PING `regime-ci-fixture-copy-ping.txt`: update the copy to 509e4c54 byte-identical, push, re-send the RESULT; the chain starts on that head.
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:30:(no advisory rows yet; written 2026-10-20T05:43Z before PR #441's first advisory disposition, C-51)
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:31:- 2026-10-20T05:43Z: the copy on #441 (c2bfda03…) equals the amendment-1 dispatch (2727), not amendment 2 (2732, 509e4c54…, read by a009 at 05:10:06Z but not applied across its session restart). PING 2748 (read 05:42:15Z) asks for the copy update and a re-sent RESULT.
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:32:- 2026-10-20T06:02Z: a009 pushed the amendment-2 task copy (head cd47e1b0; the copy's sha256 at that head read from GitHub is 509e4c54…, equal to the dispatched text); CI CLEAN; the re-sent RESULT is pending. The chain started on cd47e1b0 (`chain-integrate.sh … 441 … dotfiles-T133-regime-ci-fixture-grammar-followup-a01`; owner text written 14:43 JST; JSON ledger synced: 1 row).
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:34:- 2026-10-20T06:27Z: the chain's required-checks watch (`gh pr checks 441 --required --watch`, started 06:02Z) hung for 23 minutes on the check run `public-bootstrap (ubuntu-24.04, server)` (id 118475370308), which GitHub reported as `status=in_progress` with `conclusion=success` and `completed_at=05:43:21Z` (a status-propagation glitch; the ruleset and mergeStateStatus CLEAN read the conclusion). Measured with `gh run view 39376387419 --json jobs` and the commits/…/check-runs API. Remedy: `gh run rerun 39376387419 --job 118475370308` (a CI re-run of a passing job; no repository change) produced check run 118487841730 `completed/success` at 06:26:36Z and the watch ended; the chain continues on cd47e1b0. Mechanism: the chain should decide from check-run conclusions (as the ruleset does) with a bounded watch, not from `gh pr checks --watch` status alone; recorded as an advisory row for the chain-review a08 owner text (chain-integrate.sh is in its allowed_files).
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:35:- 2026-10-20T06:28:09Z: the chain (local review 0 findings; sweep 6 items 0 gaps) stopped at the record step: `acceptance-front-matter.py` refuses the JSON ledger row `orchestrator-text:2fc20d2:1` (the JSON ledger takes `audit:<sha7>:<n>` rows and numeric thread ids only); the orchestrator's `record-json-sync.py` glue had copied every prose row. Fix (2026-10-20T06:29Z): the glue copies only audit and thread rows (the other prose rows stay prose, which S1 reads); the six JSON ledgers it had filled are repaired; the chain restarts on cd47e1b0. Correction C-104.
.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:36:- 2026-10-20T06:35:39Z: the chain on cd47e1b0 (sweep 6 items 0 gaps; local review 0 findings): task-level audit `…-audit-cd47e1b.md` `Verdict: incorrect`: [P2] orchestration: the record said amendments=1 while three TASK dispatches (2722, 2727, 2732) make amendments=2, INV-6's S2 threshold, and the re-sent RESULT makes revises=1; measured 2026-10-20T06:36Z with scripts/regime-counters.sh: `task=dotfiles-T133-regime-ci-fixture-grammar-a01 tasks=3 amendments=2 questions=2 results=2 withdrawn=0 revises=1 first_result_head=e51fee5b29ad97e4f2c5ed20ba3bffcc1ffd9c38 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-20T04:34:08Z..2026-10-20T06:06:15Z (1:32) source=live S2: amendments 2 >= 2 source=live S2: questions 2 >= 2 source=live `; [P2] conformance: sandbox.md:31 places the RESULT send in `excludedCommands`, contradicting the text's sandbox-only sentence (the agmsg delivery send of a Claude worker runs through the documented exclusion until P1-15 lands); [P3] the text mandates `git push -u` although the shared git configuration is read-only (the push landed, the upstream write was refused). Dispositions: P2#1 -> the lineage resets to `dotfiles-T133-regime-ci-fixture-grammar-a02` written by the review profile (S2 reached by two orchestrator-text amendments), continuing PR #441 with the implementation 15bc046e unchanged; P2#2 -> the a02 text names the agmsg send as the one documented exclusion (Worker Playbook step 4) owned by P1-15, so the claim matches the facts; P3 -> fixed in a02 (push without `-u`). No finding on the code change.
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:1:2026-10-20T06:02:49Z fetch rc=0: git -C . fetch -q origin +pull/441/head:refs/remotes/pr/441
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:2:2026-10-20T06:02:50Z fetch rc=0: git -C .claude/worktrees/orchestrator-review fetch -q origin +pull/441/head
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:5:2026-10-20T06:02:50Z fetch rc=0: gh pr view 441 --json headRefOid --jq .headRefOid
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:7:2026-10-20T06:26:44Z checks rc=0: gh pr checks 441 --required --watch
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:8:2026-10-20T06:26:44Z bot rc=0: gh api repos/{owner}/{repo}/pulls/441/reviews --paginate --jq [.[] | select(.user.login == "chatgpt-codex-connector[bot]" and .commit_id == "cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2")] | length
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:13:2026-10-20T06:28:03Z local-review rc=0: local-review.sh dotfiles-T133-regime-ci-fixture-grammar-a01 cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2 441
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:14:2026-10-20T06:28:08Z pr-feedback rc=0: uv run --no-project python -I scripts/pr-feedback.py 441 --json .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-pr-feedback.json
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:16:2026-10-20T06:28:09Z fill-sweep rc=0: gh api repos/{owner}/{repo}/pulls/441/comments --paginate --jq .[]
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:23:2026-10-20T06:30:17Z fetch rc=0: git -C . fetch -q origin +pull/441/head:refs/remotes/pr/441
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:24:2026-10-20T06:30:17Z fetch rc=0: git -C .claude/worktrees/orchestrator-review fetch -q origin +pull/441/head
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:27:2026-10-20T06:30:18Z fetch rc=0: gh pr view 441 --json headRefOid --jq .headRefOid
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:29:2026-10-20T06:30:19Z checks rc=0: gh pr checks 441 --required --watch
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:30:2026-10-20T06:30:20Z bot rc=0: gh api repos/{owner}/{repo}/pulls/441/reviews --paginate --jq [.[] | select(.user.login == "chatgpt-codex-connector[bot]" and .commit_id == "cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2")] | length
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:35:2026-10-20T06:30:20Z local-review rc=0: local-review.sh dotfiles-T133-regime-ci-fixture-grammar-a01 cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2 441
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:36:2026-10-20T06:30:25Z pr-feedback rc=0: uv run --no-project python -I scripts/pr-feedback.py 441 --json .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-pr-feedback.json
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:38:2026-10-20T06:30:26Z fill-sweep rc=0: gh api repos/{owner}/{repo}/pulls/441/comments --paginate --jq .[]
.orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-chain-cd47e1b.log:44:2026-10-20T06:35:38Z audit rc=0: orch-audit.sh dotfiles-T133-regime-ci-fixture-grammar-a01 .claude/worktrees/orchestrator-review 441

web search: 
**Assessing fallback context and host provenance**
**Analyzing path validation and symlink handling**

I’m checking how path bindings handle symlinks and fixed roots, noting that GitHub’s resolution correctly binds symlinks but lacks strict allowlist enforcement, which is flagged as a high-priority concern. I see that case-insensitive comparisons might create loopholes, though strict case-sensitive checks avoid those. Python’s prefix checks don’t reveal vulnerabilities. Input validation for malformed JSON covers most cases but misses some, leading to potential minor validation issues flagged as lower priority. Overall, I’m preparing concise findings without headings, emphasizing key concerns and their impact.
exec
/bin/zsh -lc "cat .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a01-audit-cd47e1b.md.last.md; /usr/bin/python3 -I -c 'import json; pairs=lambda xs: dict(xs); s=\"{\\\"ledger\\\": [], \\\"replans\\\": {}, \\\"extra\\\": NaN}\"; r=json.loads(s,object_pairs_hook=pairs); print(\"parse_with_object_pairs_hook=accepted\"); print(json.dumps(r,ensure_ascii=False,sort_keys=True)); print(\"finite_check_present=False\")'; /usr/bin/env -i PATH=/usr/bin:/bin /bin/bash --noprofile --norc -p -c 'GH=/tmp/worker-owned/gh; case \""'$GH" in ""|*/mise/shims/*) printf "refused'"\\n\";; *) printf \"path_guard=accepted:%s\\n\" \""'$GH";; esac'"'" in ~/Workspace/dotfiles
 succeeded in 154ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-regime-ci-fixture-grammar-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md task_sha256=2fc20d2392dc7f45df100f314258ecf0ddd9e9f0310e9b2a2f8bac286ce5081d deadline=none done_signal=AGMSG-RESULT note=a009:test-only-fixture-migration(unblocks-a012's-PR-417:the-a05-checker's-C13-grammar-rejects-the-module's-bare-residual-rows;five-rows,no-test-logic-change;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0;fresh-branch-from-origin/main-60a6fb2b)",
    "AGMSG-TASK v1 task_id=dotfiles-T133-regime-ci-fixture-grammar-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md task_sha256=c2bfda037d2012e3703f12b7eedc2e976f79f5259ec5e47798248d544a69cc2b deadline=none done_signal=AGMSG-RESULT note=a009:amendment-1(previous_sha256=2fc20d2392dc7f45df100f314258ecf0ddd9e9f0310e9b2a2f8bac286ce5081d;answers-your-04:40:30Z-question:(a)yes,the-Check-command-now-keeps-uv's-dir-on-PATH-and-TMPDIR-set,as-you-measured;(b)the-one-module-constant-is-allowed,cap-12-stays;the-src/tool.sh-row-is-attributed-to-line-27's-ROWS;nothing-else-changed;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)",
    "AGMSG-TASK v1 task_id=dotfiles-T133-regime-ci-fixture-grammar-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md task_sha256=509e4c5430069deb70e35779ea1e36ff49bb7779c1a7615b1e627453242173d6 deadline=none done_signal=AGMSG-RESULT note=a009:amendment-2(previous_sha256=c2bfda037d2012e3703f12b7eedc2e976f79f5259ec5e47798248d544a69cc2b;answers-your-04:48:12Z-addendum:the-Check-command-passes-HTTPS_PROXY/HTTP_PROXY/NO_PROXY-through,as-you-measured;the-orchestrator-ran-that-exact-form-on-unmodified-main:16-tests-OK-in-50.8s;nothing-else-changed;your-default-(a)+the-constant-is-exactly-this-text;proceed)",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-regime-ci-fixture-grammar-a01 status=pending-integration round=1 pr=441 head=e51fee5b29ad97e4f2c5ed20ba3bffcc1ffd9c38 reason=RESULT-of-05:39:29Z-read:five-rows-on-one-module-constant,module-16/16-before-and-after,caps-0/11-of-12,CI-11/11;no-finding-on-the-change;one-records-step-before-the-chain,already-asked-in-PING-2748:the-task-copy-must-equal-the-amendment-2-text(509e4c54…);push-it-and-re-send-the-RESULT-with-the-new-head;then-sweep,audit,gate,merge-ahead-of-#440"
  ],
  "format": 1,
  "head": "cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2",
  "ledger": [],
  "pr": 441,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-regime-ci-fixture-grammar-a01"
}
---

# Acceptance record: dotfiles-T133-regime-ci-fixture-grammar-a01

- 2026-10-20T04:34Z: test-only task written by the orchestrator after a012 blocked on `tests/unit/test_regime_ci.py` (outside #417's allowed_files; amendments spent): the five bare `disposition: residual` fixture rows migrate to the `residual: <sentence>` grammar the a05 checker requires (C13) and main's checker also accepts; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; Checks pasted; AGMSG-TASK round 1 dispatched to a009 (Claude, worker-c, wJ:p2) via dispatch.sh (`regime-ci-fixture-dispatch.txt`, task_sha256 2fc20d2392dc7f45df100f314258ecf0ddd9e9f0310e9b2a2f8bac286ce5081d); read_at filled by fill-dispatch.py. After its merge the chain update-branches #417.
- 2026-10-20T04:49Z: a009 PONG `question` (04:40:30Z, nothing committed): the Check command as written fails on unmodified main inside the sandbox (22 errors: `uv` not on the `env -i` PATH; then 21 `git init` exit 128 with TMPDIR unset), while PATH with uv's directory and TMPDIR set gives 16/16 OK; ruff-format splits the inline sentences past the 12-line cap (16 lines) while one module constant measures 11; the `src/tool.sh` row removed at line 276 is written by line 27's ROWS, not line 127. The orchestrator's command had been written without execution (C-100 instance: the orchestrator's own run of the module in its seat gave 21 failures and 1 error in 240 s under the same form, an environment difference not investigated further; a009's measured form is the authority). Amendment 1: Check command with uv's directory and TMPDIR, the one constant allowed, the attribution fixed; task_sha256 2fc20d2392dc7f45… -> c2bfda037d2012e3703f12b7eedc2e976f79f5259ec5e47798248d544a69cc2b (`regime-ci-fixture-amend1.txt`).
orchestrator-text:2fc20d2:1	check-command-unverified-in-seat
- 2026-10-20T04:55Z: a009 addendum (04:48:12Z): the corrected command also needs the sandbox proxy variables (env -i strips HTTPS_PROXY/HTTP_PROXY/NO_PROXY; the module's `uv run --with pyyaml` then fails with a DNS error to pypi.org: 21 failures + 1 error, the same shape the orchestrator's own run had shown). The orchestrator ran the form with the three variables passed through on unmodified main in its sandbox at 04:51:17Z: `Ran 16 tests in 50.784s / OK`. Amendment 2: the Check command passes them through; task_sha256 c2bfda037d2012e3… -> 509e4c5430069deb70e35779ea1e36ff49bb7779c1a7615b1e627453242173d6 (`regime-ci-fixture-amend2.txt`).
- 2026-10-20T05:39:29Z: a009 RESULT round 1 `status=ready_for_review`: PR #441 head e51fee5b (code head 15bc046e, base 60a6fb2b), five rows read the module constant `RESIDUAL` (276 an f-string, still removing exactly the ROWS src/tool.sh row); module 16/16 OK before (60a6fb2b) and after (15bc046e), with the proxy variables; caps 0 outside, 11/12 under tests; CI 11/11 pass; Codex Bot unavailable (usage limits at 05:10Z); self-review 1 round (2 P3 resolved); INV-6 amendments 1, questions 2, revises 0. Gap found at 2026-10-20T05:42Z: the task copy on the branch (sha256 c2bfda03…) is the amendment-1 text; the latest dispatched text is amendment 2 (2732, 04:53:03Z, 509e4c54…, unread on the bus: a009's session restarted). PING `regime-ci-fixture-copy-ping.txt`: update the copy to 509e4c54 byte-identical, push, re-send the RESULT; the chain starts on that head.

## Owned by dotfiles-T133-regime-ci-fixture-grammar-followup-a01

(no advisory rows yet; written 2026-10-20T05:43Z before PR #441's first advisory disposition, C-51)
- 2026-10-20T05:43Z: the copy on #441 (c2bfda03…) equals the amendment-1 dispatch (2727), not amendment 2 (2732, 509e4c54…, read by a009 at 05:10:06Z but not applied across its session restart). PING 2748 (read 05:42:15Z) asks for the copy update and a re-sent RESULT.
- 2026-10-20T06:02Z: a009 pushed the amendment-2 task copy (head cd47e1b0; the copy's sha256 at that head read from GitHub is 509e4c54…, equal to the dispatched text); CI CLEAN; the re-sent RESULT is pending. The chain started on cd47e1b0 (`chain-integrate.sh … 441 … dotfiles-T133-regime-ci-fixture-grammar-followup-a01`; owner text written 14:43 JST; JSON ledger synced: 1 row).
- 2026-10-20T06:06:15Z: a009 RESULT re-sent for head cd47e1b0 (code head 15bc046e unchanged, task_copy 509e4c54… = amendment 2; CI all success, CLEAN). ACCEPTANCE `status=pending-integration round=1` for cd47e1b0 (2026-10-20T06:07Z, `regime-ci-fixture-acc-pending2.txt`).
- 2026-10-20T06:27Z: the chain's required-checks watch (`gh pr checks 441 --required --watch`, started 06:02Z) hung for 23 minutes on the check run `public-bootstrap (ubuntu-24.04, server)` (id 118475370308), which GitHub reported as `status=in_progress` with `conclusion=success` and `completed_at=05:43:21Z` (a status-propagation glitch; the ruleset and mergeStateStatus CLEAN read the conclusion). Measured with `gh run view 39376387419 --json jobs` and the commits/…/check-runs API. Remedy: `gh run rerun 39376387419 --job 118475370308` (a CI re-run of a passing job; no repository change) produced check run 118487841730 `completed/success` at 06:26:36Z and the watch ended; the chain continues on cd47e1b0. Mechanism: the chain should decide from check-run conclusions (as the ruleset does) with a bounded watch, not from `gh pr checks --watch` status alone; recorded as an advisory row for the chain-review a08 owner text (chain-integrate.sh is in its allowed_files).
- 2026-10-20T06:28:09Z: the chain (local review 0 findings; sweep 6 items 0 gaps) stopped at the record step: `acceptance-front-matter.py` refuses the JSON ledger row `orchestrator-text:2fc20d2:1` (the JSON ledger takes `audit:<sha7>:<n>` rows and numeric thread ids only); the orchestrator's `record-json-sync.py` glue had copied every prose row. Fix (2026-10-20T06:29Z): the glue copies only audit and thread rows (the other prose rows stay prose, which S1 reads); the six JSON ledgers it had filled are repaired; the chain restarts on cd47e1b0. Correction C-104.
- 2026-10-20T06:35:39Z: the chain on cd47e1b0 (sweep 6 items 0 gaps; local review 0 findings): task-level audit `…-audit-cd47e1b.md` `Verdict: incorrect`: [P2] orchestration: the record said amendments=1 while three TASK dispatches (2722, 2727, 2732) make amendments=2, INV-6's S2 threshold, and the re-sent RESULT makes revises=1; measured 2026-10-20T06:36Z with scripts/regime-counters.sh: `task=dotfiles-T133-regime-ci-fixture-grammar-a01 tasks=3 amendments=2 questions=2 results=2 withdrawn=0 revises=1 first_result_head=e51fee5b29ad97e4f2c5ed20ba3bffcc1ffd9c38 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-20T04:34:08Z..2026-10-20T06:06:15Z (1:32) source=live S2: amendments 2 >= 2 source=live S2: questions 2 >= 2 source=live `; [P2] conformance: sandbox.md:31 places the RESULT send in `excludedCommands`, contradicting the text's sandbox-only sentence (the agmsg delivery send of a Claude worker runs through the documented exclusion until P1-15 lands); [P3] the text mandates `git push -u` although the shared git configuration is read-only (the push landed, the upstream write was refused). Dispositions: P2#1 -> the lineage resets to `dotfiles-T133-regime-ci-fixture-grammar-a02` written by the review profile (S2 reached by two orchestrator-text amendments), continuing PR #441 with the implementation 15bc046e unchanged; P2#2 -> the a02 text names the agmsg send as the one documented exclusion (Worker Playbook step 4) owned by P1-15, so the claim matches the facts; P3 -> fixed in a02 (push without `-u`). No finding on the code change.
audit:cd47e1b:1	replan-skipped
audit:cd47e1b:2	excluded-command-trusts-sandbox-context
audit:cd47e1b:3	tool-environment

[P2] high orchestration `.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:26` reports amendments=1, but the three recorded TASK dispatches establish amendments=2, reaching INV-6’s S2 threshold; the later RESULT also changes revises to 1. Correct the counter evidence and record the required reset or waiver before merge.

[P2] high conformance `.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/sandbox.md:31` places RESULT dispatch in `excludedCommands`, contradicting task.md:59 and design 5.14 item 10’s requirement that every worker command execute inside the sandbox; the claim that everything remained sandboxed is therefore unsupported.

[P3] high orchestration `.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md:59` mandates `git push -u` despite the shared Git configuration being read-only; sandbox.md:23 confirms the resulting upstream-configuration refusal. Prescribe an explicit branch push without `-u`.

The fixture implementation checks out: all five replacements, unchanged test logic, preserved `no_row` matching, 11/12 changed-line cap, and amendment-2 task-copy equality. Final-head [CI logs](https://github.com/mryfmo/dotfiles/actions/runs/39376387421/job/118475369929) confirm all 16 module tests and 1,267 Python tests passed.

INV-6: holds `.orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md:33` — integration remains pending; reaching S2 requires reset/waiver before the merge backstop permits integration.

Orchestration findings: 2

📝 まとめ: Read-only audit completed; three process/conformance findings remain.

Not rerun locally: test suites or PR #417 integration. No files changed; sandbox compliance remains unresolved.
Verdict: incorrectpython3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
parse_with_object_pairs_hook=accepted
{"extra": NaN, "ledger": [], "replans": {}}
finite_check_present=False
path_guard=accepted:/tmp/worker-owned/gh

**Finalizing findings with verification**
exec
/bin/zsh -lc "rg -n 'threat.table|non-path|pre-dispatch' ~/.agents/skills/agmsg-orchestration/SKILL.md; /usr/bin/shasum -a 256 .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md; test "'! -e scripts/orchestrator/record-json-sync.py && test ! -e tests/unit/test_record_json_sync.py && printf '"'implementation-and-test-absent\\n'" in ~/Workspace/dotfiles
 succeeded in 0ms:
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
d899b844365703dcc8a33fccca822fad9c739d5d948a28efdd17919691f439ad  .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
implementation-and-test-absent

**Assessing Git reference and object risks**
**Reviewing sandbox Git config and parsing behavior**

I'm analyzing whether the sandbox's local Git config is writable and how the JSON parser handles invalid constants like NaN. I note that the environment likely trusts user-level write permissions but avoids overstating severity beyond P2 except in specific sandbox cases. The parser's design doesn't reject invalid constants, so tests can't guarantee strict enforcement, aligning with the specifications. I’m preparing to close commentary with a concise English summary and Japanese per instructions, focusing on clear verdict lines about risks and conditions for the user.
codex
[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:108](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:108) — Clearing inherited `GIT_*` leaves system/global/repository configuration active: hooks can execute unchecked code and `url.*.insteadOf` can redirect the explicit push URL; a read-only probe confirmed URL rewriting survives the clean environment. [Git configuration](https://git-scm.com/docs/git-config).

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:100](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:100) — The resolved `GH` path is checked only for executability and a case-sensitive shim substring; an installation symlink pointing into a worker directory passes before any race, so the claimed trusted executable binding lacks resolved-root validation.

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:109](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:109) — Full SHA operands do not authenticate cap evidence from the shared object store: worker-writable `refs/replace` can substitute the objects Git compares; use the fixed repository’s remote content or a protected object store as §5.14 requires. [Git replacement behavior](https://git-scm.com/docs/git-replace).

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:131](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:131) — Darwin does not satisfy the sandbox-only messaging claim: deployed settings still exclude `agmsg-dispatch *`, which the Worker Playbook requires for delivery; the cited #441 acceptance/audit already records this contradiction, and no deployment prerequisite closes it.

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:116](~/Workspace/dotfiles-T133-record-json-sync-a01.md:116) — The prescribed parser and malformed-input fixtures omit non-finite-number rejection: `{"ledger":[],"replans":{},"extra":NaN}` passes `object_pairs_hook` parsing and serialization although the actual gate rejects it, leaving the malformed-front-matter row’s closure unsupported. [Python JSON behavior](https://docs.python.org/3/library/json.html#infinite-and-nan-number-values).

All required file, non-path-control, and orchestrator-effect rows are present. Explicitly acknowledged concurrent replacement and shared-credential residuals are not counted again.

📝 まとめ: Completed the read-only pre-dispatch review and cited-record checks; five findings remain for orchestrator disposition.
Not checked: implementation/tests, which do not yet exist, or live Linux enforcement. No files changed; execution-binding gaps remain.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
108,545
[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:108](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:108) — Clearing inherited `GIT_*` leaves system/global/repository configuration active: hooks can execute unchecked code and `url.*.insteadOf` can redirect the explicit push URL; a read-only probe confirmed URL rewriting survives the clean environment. [Git configuration](https://git-scm.com/docs/git-config).

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:100](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:100) — The resolved `GH` path is checked only for executability and a case-sensitive shim substring; an installation symlink pointing into a worker directory passes before any race, so the claimed trusted executable binding lacks resolved-root validation.

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:109](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:109) — Full SHA operands do not authenticate cap evidence from the shared object store: worker-writable `refs/replace` can substitute the objects Git compares; use the fixed repository’s remote content or a protected object store as §5.14 requires. [Git replacement behavior](https://git-scm.com/docs/git-replace).

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:131](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:131) — Darwin does not satisfy the sandbox-only messaging claim: deployed settings still exclude `agmsg-dispatch *`, which the Worker Playbook requires for delivery; the cited #441 acceptance/audit already records this contradiction, and no deployment prerequisite closes it.

[P2] high [.orchestration/tasks/dotfiles-T133-record-json-sync-a01.md:116](~/Workspace/dotfiles-T133-record-json-sync-a01.md:116) — The prescribed parser and malformed-input fixtures omit non-finite-number rejection: `{"ledger":[],"replans":{},"extra":NaN}` passes `object_pairs_hook` parsing and serialization although the actual gate rejects it, leaving the malformed-front-matter row’s closure unsupported. [Python JSON behavior](https://docs.python.org/3/library/json.html#infinite-and-nan-number-values).

All required file, non-path-control, and orchestrator-effect rows are present. Explicitly acknowledged concurrent replacement and shared-credential residuals are not counted again.

📝 まとめ: Completed the read-only pre-dispatch review and cited-record checks; five findings remain for orchestrator disposition.
Not checked: implementation/tests, which do not yet exist, or live Linux enforcement. No files changed; execution-binding gaps remain.
Verdict: incorrect
