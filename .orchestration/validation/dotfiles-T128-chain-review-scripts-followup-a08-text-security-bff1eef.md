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
session id: 01a15cc3-d29c-7a42-833a-fb693a59caf3
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
指定のタスク本文と参照先の記録を読み、判断に使った対象と実際に実行される対象が一致する設計かを確認します。読み取り専用で進め、agmsg-orchestration と Ponytail のレビュー手順を参照します。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 3ms:
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
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md' in ~/Workspace/dotfiles
 succeeded in 9ms:
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md
 M .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a02.md
 M .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a02.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
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
 M .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-pins-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01.md
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
?? .orchestration/learning/mistakes/M-20261021-02-boundary-carried-unmasked-records.md
?? .orchestration/learning/mistakes/M-20261021-03-dispatch-without-the-disjointness-check.md
?? .orchestration/learning/mistakes/M-20261021-04-requirement-waived-in-a-dispatch-note.md
?? .orchestration/plans/024-allocation.tsv
?? .orchestration/plans/024-replan-20261021-v2.md
?? .orchestration/plans/024-replan-20261021.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-pins-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/024-replan-20261021-review-r1.md
?? .orchestration/validation/024-replan-20261021-v2-review-r2.md
?? .orchestration/validation/024-replan-20261021-v2-review-r3.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md.last.md
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
     3	task_id: dotfiles-T128-chain-review-scripts-followup-a08
     4	reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]
     5	kind: code
     6	security: true
     7	allowed_files:
     8	  - scripts/orchestrator/local-advisory.sh
     9	  - scripts/orchestrator/local-review.sh
    10	  - tests/unit/test_chain_review_scripts.py
    11	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**
    12	after: []
    13	retained_predecessor_directories:
    14	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
    15	threat_table:
    16	  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "residual: Item 1 has no owned rows; this file remains unchanged and the audit compares the final diff; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    17	  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    18	  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: fixtures and stub gh/git/codex run in temporary directories; the audit checks their content assertions and inherited regressions; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    19	  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: these records are untrusted evidence; the orchestrator compares them with the dispatched text, diff and final-head CI; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    20	  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: byte-identical to the dispatched file and dispatch SHA-256; the orchestrator compares both at acceptance; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    21	  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: unchanged on the branch at SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36; the orchestrator compares it at acceptance; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    22	  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: report, validation, sandbox, learning and autoskill records identify commands, statuses and provenance; every sandbox refusal is recorded; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    23	  - {control: "review-cache provenance and reuse", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
    24	  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: task-consistency checks run before dispatch and acceptance; the whole-file comparison detects changed worker metadata; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    25	  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    26	  - {control: "in-process effects", disposition: "residual: the script creates a private temporary repository and invokes the bound reviewer; tests use fixtures and never fetch live GitHub content; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    27	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: no workflow or interpreter file changes; Item 3 isolates Git/gh inputs and preserves the inherited binary/interpreter binding and Codex environment overrides; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    28	  - {control: "new or renamed scripts", disposition: "residual: none authorized; any new or renamed script is an undeclared change that fails audit; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    29	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: same-UID processes and shared credentials remain outside host isolation; host controls reduce accidents and prompt injection, with missing acceptance detected at the next records PR rather than prevented; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    30	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: private storage uses the declared sandbox boundary; Claude file-tool protection remains incomplete until P1-15, so no unrestricted same-UID protection is claimed; owner: dotfiles-T133-worker-write-boundary-a04."}
    31	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Item 3 uses clean Git/gh children and propagates Git isolation to reviewer children; the trusted-parent contract applies by reference, without a self-reexec repair; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    32	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: the private temporary root and bound tools are checked under this item; worker-root and symlink aliases are refused, while unrestricted same-UID replacement remains possible; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    33	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: the same resolved tools and verified private-clone commits are consumed without rediscovery; unrestricted same-UID replacement between checks remains possible; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    34	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: Item 3 revalidates full head/base/tree cache identity after fresh private fetch; each private root is unique and no slot reservation is introduced; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    35	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: this table distinguishes the private-object-source fix from inherited host, credential, executable and reservation limitations; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    36	  - {control: "design 5.14 item 7: 検証", disposition: "residual: Item 3 adds content-source and refusal red/green tests and retains the existing execution-boundary tests; it does not claim the whole trusted-execution contract is closed; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    37	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    38	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: review objects use a fresh private store without alternates and review artifacts use orchestrator-private storage; inherited executable provenance remains a host-control residual; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    39	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: all Codex worker commands remain sandboxed under Worker Playbook step 4; a denial produces a blocked PONG without escalation; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    40	  - {control: "orchestrator effect merge", disposition: "residual: only gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker never merges or pushes main; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    41	  - {control: "orchestrator effect update-branch", disposition: "residual: an updated head invalidates earlier CI, sweep and audit evidence; repeat them on the new head before the gate; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    42	  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; dirty-worktree removal requires explicit force and an acceptance record of discarded state; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    43	premises:
    44	  - claim: "worker (Codex seat, review-profile authoring context): the local continuation commit resolves to the head named by D-024-41; this probe does not authenticate its content."
    45	    command: |-
    46	      git rev-parse --verify 'a644a7d9^{commit}'
    47	    output: |-
    48	      a644a7d965399b9463e9b32721287440a7efa233
    49	  - claim: "worker (Codex seat, review-profile authoring context): the predecessor task copy at the continuation head has the dispatched a07 SHA-256."
    50	    command: |-
    51	      git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256
    52	    output: |-
    53	      b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -
    54	---
    55	
    56	# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content
    57	
    58	This text is the independent-context reset after INV-6 S2 (two amendments, including the erroneous resend; D-024-41), and the a07 findings history is in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md`.
    59	Continue PR #439 on `tools/chain-review-scripts-followup-a07` from `a644a7d965399b9463e9b32721287440a7efa233`, worker a013 (Codex, worker-h), retaining the inherited implementation (code head `f5aaaf7e`) except for Item 3; create no branch or PR.
    60	Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen (D-024-29) and applies by reference (D-024-30): `design: 5.14 items 2, 3, 4, 7, 8, 9`; items 0–10 have individual threat rows.
    61	Read the whole a07 task, its acceptance record and `.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md` before editing.
    62	
    63	## Item 1
    64	
    65	Vacuous as in a07: `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` in the a06 acceptance record has no rows; do not change `local-advisory.sh` or import the a09 owner's advisory rows.
    66	
    67	## Item 2
    68	
    69	Keep the implemented canonical-main binding: resolve gh before checkout and read `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; require successful exit and exactly 40 ASCII hexadecimal characters, with a named refusal otherwise.
    70	Neither local `main` nor `origin/main` selects the base; pass that exact SHA to `codex review --base`, with the commit check moved into Item 3's private store.
    71	Keep `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` both exported and passed through `-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"'` and `-c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'` so Codex-spawned Git receives them.
    72	Preserve the inherited binary/interpreter pinning, failed-review refusal, full-head equality, finding/output handling and red/green evidence, with cache trust and location revised by Item 3; do not undo implemented fixes to reproduce inherited reds.
    73	
    74	## Item 3
    75	
    76	Close audit `audit:a644a7d:1`: `local-review.sh` never reads review content from the shared object store; checking object existence/type there or suppressing replacements/grafts does not authenticate overwritten objects.
    77	On every invocation, before any cache read, create a fresh mode-0700 private directory under `${TMPDIR:-/tmp}`, check its path under design 5.14 item 3, and create a bare repository there with `git init --bare <dir>`, followed by `git --git-dir=<dir> fetch https://github.com/mryfmo/dotfiles.git <head40> <base40>`.
    78	Use that explicit HTTPS URL, never a remote name, URL rewriting, local transport, alternates, `--reference`, `--shared`, copied objects or the shared `.git` as an object source; apply design 5.14 items 2, 4 and 9 to Git and its reviewer-spawned children, retaining Item 2's overrides.
    79	Apply design 5.14 items 2, 3, 4 and 9 to Git, gh and reviewer bindings before checkout; use fresh `GH_CONFIG_DIR` and read the token once with the bound gh's `auth token --hostname github.com`, as in `.orchestration/tasks/dotfiles-T133-python-pin-a02.md` Commands (e)/(e'); run Item 2's isolated canonical-main lookup on every invocation before any cache read.
    80	Never print or persist the token or pass it to Codex; the canonical-main lookup and explicit-URL private fetch cannot be skipped by any cached artifact.
    81	Verify both exact full SHAs in the private repository have object type `commit`, check out that head into its own worktree, and verify its HEAD; run `codex review --base <base40>` there when Item 3's cache check requires review, never in the former shared review worktree.
    82	Before any cache read, recompute the verified private-clone head SHA, canonical-main SHA and head tree hash (`git --git-dir=<dir> rev-parse <head40>^{tree}`); the first two must equal the requested head and Item 2's canonical-main result.
    83	Store reusable artifacts only as `<anchored-checkout>/.agents/worklog/local-review/<task>-local-review-<head40>.md` under design 5.14 items 1, 3 and 9, outside every worker-writable path; legacy artifacts in the shared store cannot authorize reuse.
    84	A cache hit may skip only the model call, and only if a private artifact records full `head:`, `base:` (canonical main) and `tree:` values exactly equal to all three freshly recomputed values; preserve finding counts and exit behavior.
    85	Absent, legacy, malformed, untrusted-location or mismatched artifacts require a new review and a rewritten private artifact after success; full-head equality or `findings: 0` alone never permits reuse.
    86	On fetch failure emit `local-review: private fetch failed`; on a missing/non-commit/mismatched SHA emit `local-review: private commit check failed`; both exit 2, invoke no reviewer, write no review artifact and never fall back to the shared store.
    87	Remove only this invocation's private repository/worktree on completion or refusal; preserve the inherited failed-review transcript behavior.
    88	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects`: stub gh/git, plant an overwritten object in the shared store with forged content, supply different canonical content through the explicit-URL private fetch, and have the reviewer stub read content from its actual cwd; assert canonical content, isolated Git/gh inputs and private object provenance, not merely argv or a directory name.
    89	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_refuses_a_failed_private_fetch_or_commit_check`, with subcases for fetch failure and each missing/non-commit/mismatched head or base SHA, including a matching private cache; assert the named refusal, no reviewer call, no artifact creation or rewrite and no shared fallback.
    90	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache`: plant a shared artifact with matching `head:` and `findings: 0`, including a variant with matching `base:`/`tree:`; assert fresh canonical-main lookup/private fetch precede any cache read, the reviewer runs in the canonical private checkout and rewrites the artifact privately.
    91	In that test, verify a valid private head/base/tree cache skips only the model after fresh lookup/fetch, and a changed head, canonical main, tree or missing metadata reruns review; failed lookup/fetch cannot return cached success.
    92	Record each new test red against `a644a7d9` on its security assertion, not a bootstrap failure, and green after Item 3; adapt inherited worktree fixtures to private-clone behavior and keep all other regression assertions.
    93	
    94	## Check and Completion
    95	
    96	Host facts: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
    97	Before validation, run that uv resolve command and paste its actual output; record the bound interpreter's realpath/version under design 5.14 items 2, 4 and 9, never guess an uv operand.
    98	Run `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v`, `bash -n scripts/orchestrator/local-review.sh`, `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh` and the repository's applicable lint checks; paste exact commands, resolved operands, exit statuses and complete outputs in `validation.md`; never run Bats locally.
    99	The whole PR is at most 120 changed lines outside `tests/` and `.orchestration/`, and at most 400 under `tests/`, counting additions plus deletions and attributing the inherited 26 outside-test lines and 69 test lines separately from Item 3.
   100	Run `git --git-dir=<private-bare> diff --numstat <base40>...<head40>` in the authenticated private repository with resolved full SHAs and record its complete output.
   101	The orchestrator records the resolved measurement base at dispatch; attribute inherited and Item 3 additions plus deletions separately against that base and the final head.
   102	Keep this complete task text at or under 140 lines; no workflow, permission, dependency, launcher, knowledge-graph or predecessor-artifact changes are authorized.
   103	Worker Playbook step 4 applies: every a013 command, including gh, Git and agmsg delivery, stays sandboxed; push without `-u` over HTTPS (`git push https://github.com/mryfmo/dotfiles.git tools/chain-review-scripts-followup-a07`); any denial sends a blocked PONG with exact command, status and boundary, without escalation or substitute tools.
   104	Do not probe the herdr socket from this Codex seat; host placement and delivery verification belong to the orchestrator.
   105	Copy this text byte-identically to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md`; keep the a07 task copy and evidence unchanged, and keep plan/todo/learn uncommitted with at most one active todo per owner.
   106	Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker crit-data evidence with a `-worker-` infix under `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/`; record inherited/new evidence provenance and `cost:`; never open a browser review or request human review.
   107	Every evidence item names its producer and seat kind: `worker (Codex seat, a013)` or `orchestrator (Claude seat, sandboxed Bash)`; authoring probes identify their separate Codex review-profile producer, and inherited evidence retains its original producer.
   108	Keep evidence artifacts untracked at the same relative paths in worker-h for orchestrator transfer when main-checkout paths are inaccessible; record exact commands, operands, statuses, complete output and every sandbox refusal without secrets.
   109	After the final push verify GitHub Actions and wait for the Bot under the Worker Playbook; fix P0/P1 within INV-6 and the one Bot fix round, otherwise report surviving findings for the operator; the orchestrator dispositions and resolves threads.
   110	RESULT names PR, full head/base, branch, changed files, test selectors, red/green commits, caps and artifact paths, plus `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md>`.
   111	The orchestrator records counters before acceptance actions, carries the a07 history, and performs the final-head sweep, audit, acceptance and gate in Orchestrator Playbook step 10 order; any head update repeats the required evidence; advisory ownership remains `dotfiles-T128-chain-review-scripts-followup-a09`.
   112	
   113	## Checks
   114	

**Separating clean budget outputs**
exec
/bin/zsh -lc "sed -n '/## Codex seat worklogs/,/"'^## /p'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 60ms:
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
/bin/zsh -lc 'git status --short; git rev-parse HEAD; nl -ba .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md | head -56; cat .ua/meta.json' in ~/Workspace/dotfiles
 succeeded in 42ms:
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md
 M .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a02.md
 M .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a02.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
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
 M .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-pins-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01.md
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
?? .orchestration/learning/mistakes/M-20261021-02-boundary-carried-unmasked-records.md
?? .orchestration/learning/mistakes/M-20261021-03-dispatch-without-the-disjointness-check.md
?? .orchestration/learning/mistakes/M-20261021-04-requirement-waived-in-a-dispatch-note.md
?? .orchestration/plans/024-allocation.tsv
?? .orchestration/plans/024-replan-20261021-v2.md
?? .orchestration/plans/024-replan-20261021.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-pins-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/024-replan-20261021-review-r1.md
?? .orchestration/validation/024-replan-20261021-v2-review-r2.md
?? .orchestration/validation/024-replan-20261021-v2-review-r3.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md.last.md
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
e042663b2d6efd9205f7d388bf881c01d3880642
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-chain-review-scripts-followup-a08
     4	reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]
     5	kind: code
     6	security: true
     7	allowed_files:
     8	  - scripts/orchestrator/local-advisory.sh
     9	  - scripts/orchestrator/local-review.sh
    10	  - tests/unit/test_chain_review_scripts.py
    11	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**
    12	after: []
    13	retained_predecessor_directories:
    14	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
    15	threat_table:
    16	  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "residual: Item 1 has no owned rows; this file remains unchanged and the audit compares the final diff; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    17	  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    18	  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: fixtures and stub gh/git/codex run in temporary directories; the audit checks their content assertions and inherited regressions; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    19	  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: these records are untrusted evidence; the orchestrator compares them with the dispatched text, diff and final-head CI; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    20	  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: byte-identical to the dispatched file and dispatch SHA-256; the orchestrator compares both at acceptance; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    21	  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: unchanged on the branch at SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36; the orchestrator compares it at acceptance; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    22	  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: report, validation, sandbox, learning and autoskill records identify commands, statuses and provenance; every sandbox refusal is recorded; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    23	  - {control: "review-cache provenance and reuse", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
    24	  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: task-consistency checks run before dispatch and acceptance; the whole-file comparison detects changed worker metadata; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    25	  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    26	  - {control: "in-process effects", disposition: "residual: the script creates a private temporary repository and invokes the bound reviewer; tests use fixtures and never fetch live GitHub content; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    27	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: no workflow or interpreter file changes; Item 3 isolates Git/gh inputs and preserves the inherited binary/interpreter binding and Codex environment overrides; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    28	  - {control: "new or renamed scripts", disposition: "residual: none authorized; any new or renamed script is an undeclared change that fails audit; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    29	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: same-UID processes and shared credentials remain outside host isolation; host controls reduce accidents and prompt injection, with missing acceptance detected at the next records PR rather than prevented; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    30	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: private storage uses the declared sandbox boundary; Claude file-tool protection remains incomplete until P1-15, so no unrestricted same-UID protection is claimed; owner: dotfiles-T133-worker-write-boundary-a04."}
    31	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Item 3 uses clean Git/gh children and propagates Git isolation to reviewer children; the trusted-parent contract applies by reference, without a self-reexec repair; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    32	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: the private temporary root and bound tools are checked under this item; worker-root and symlink aliases are refused, while unrestricted same-UID replacement remains possible; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    33	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: the same resolved tools and verified private-clone commits are consumed without rediscovery; unrestricted same-UID replacement between checks remains possible; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    34	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: Item 3 revalidates full head/base/tree cache identity after fresh private fetch; each private root is unique and no slot reservation is introduced; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    35	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: this table distinguishes the private-object-source fix from inherited host, credential, executable and reservation limitations; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    36	  - {control: "design 5.14 item 7: 検証", disposition: "residual: Item 3 adds content-source and refusal red/green tests and retains the existing execution-boundary tests; it does not claim the whole trusted-execution contract is closed; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    37	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    38	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: review objects use a fresh private store without alternates and review artifacts use orchestrator-private storage; inherited executable provenance remains a host-control residual; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    39	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: all Codex worker commands remain sandboxed under Worker Playbook step 4; a denial produces a blocked PONG without escalation; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    40	  - {control: "orchestrator effect merge", disposition: "residual: only gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker never merges or pushes main; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    41	  - {control: "orchestrator effect update-branch", disposition: "residual: an updated head invalidates earlier CI, sweep and audit evidence; repeat them on the new head before the gate; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    42	  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; dirty-worktree removal requires explicit force and an acceptance record of discarded state; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    43	premises:
    44	  - claim: "worker (Codex seat, review-profile authoring context): the local continuation commit resolves to the head named by D-024-41; this probe does not authenticate its content."
    45	    command: |-
    46	      git rev-parse --verify 'a644a7d9^{commit}'
    47	    output: |-
    48	      a644a7d965399b9463e9b32721287440a7efa233
    49	  - claim: "worker (Codex seat, review-profile authoring context): the predecessor task copy at the continuation head has the dispatched a07 SHA-256."
    50	    command: |-
    51	      git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256
    52	    output: |-
    53	      b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -
    54	---
    55	
    56	# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

**Clarifying scope without graph**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md; cat .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '"'^### 5.14|''^### 5.15|D-024-(21|29|30|41)|trusted|Commands|'"\\(e' .orchestration/plans/024-design-quality.md .orchestration/tasks/dotfiles-T133-python-pin-a02.md; nl -ba scripts/orchestrator/local-review.sh" in ~/Workspace/dotfiles
 exited 1 in 99ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a07 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md task_sha256=ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75 deadline=none done_signal=AGMSG-RESULT note=a011:owner-follow-up-a07(predecessor-a06-merged-as-PR-434-at-118daafa;security-false;pre-send-on-these-bytes:task-consistency-check-OK,SECRET_PATTERN-0,home-paths-0;your-PR-436-stays-on-its-branch-for-its-pending-acceptance,this-task-starts-on-its-own-branch-as-the-text-says)",
    "AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a07 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md task_sha256=ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75 deadline=none done_signal=AGMSG-RESULT note=a011:amendment-1(previous_sha256=ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75;PR-402->434-in-three-sentences,nothing-else;the-section-'Owned-by-…-a07'-now-exists-in-the-a06-record-with-zero-rows:Item-1-is-vacuous,Item-2-carries-the-task;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)",
    "AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a07 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md task_sha256=b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 deadline=none done_signal=AGMSG-RESULT note=a011:amendment-1-resent(message-2710-carried-the-unamended-sha256-ae03f009…-by-an-orchestrator-script-error:disregard-it;previous_sha256=ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75;PR-402->434-in-four-places,nothing-else;the-section-'Owned-by-…-a07'-exists-in-the-a06-record-with-zero-rows:Item-1-is-vacuous,Item-2-carries-the-task;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-chain-review-scripts-followup-a07 status=pending-integration round=1 pr=439 head=6a38e12dd1d4fc40d7e14757d7c2b02080fb7cbe reason=RESULT-of-04:59:48Z-read:item-2-implemented(canonical-main-base-via-gh-api,4-named-refusals,replace-ref-and-graft-sub-tests,19-OK,caps-26/200-and-69/1000),item-1-vacuous-as-the-record-section-says;your-decision_for_you-is-accepted:the-regime-failure-is-the-records-gap(main-holds-the-pre-amendment-a07-text-ae03f009);the-amended-text-b91cc496-joins-records-PR-438;after-its-merge-the-orchestrator-marks-439-ready,update-branches-it,and-runs-the-chain(sweep,audit,gate);no-worker-action;the-draft-stays-as-is"
  ],
  "format": 1,
  "head": "a644a7d965399b9463e9b32721287440a7efa233",
  "ledger": [
    {
      "class": "review-binary-shim",
      "id": "audit:b6ce4ff:1"
    },
    {
      "class": "task-arg-traversal",
      "id": "audit:b6ce4ff:2"
    },
    {
      "class": "sed-path-interpolation",
      "id": "audit:b6ce4ff:3"
    },
    {
      "class": "test-order-unproven",
      "id": "audit:b6ce4ff:4"
    },
    {
      "class": "owner-not-on-main",
      "id": "audit:b6ce4ff:5"
    },
    {
      "class": "sandbox-record-incomplete",
      "id": "audit:b6ce4ff:6"
    },
    {
      "class": "report-base-sha",
      "id": "audit:b6ce4ff:7"
    },
    {
      "class": "review-binary-shim",
      "id": "audit:c45f9b5:1"
    },
    {
      "class": "advisory-policy-reading",
      "id": "audit:c45f9b5:2"
    },
    {
      "class": "env-s-quoting",
      "id": "audit:2e3ff49:1"
    },
    {
      "class": "missing-owner-task",
      "id": "audit:2e3ff49:2"
    },
    {
      "class": "advisory-deferral-objection",
      "id": "audit:ba451c6:2"
    },
    {
      "class": "sandbox-count-understated",
      "id": "audit:ba451c6:3"
    },
    {
      "class": "evidence-command-unlanded-owner",
      "id": "audit:40f3be4:3"
    },
    {
      "class": "filename-suffix-parse",
      "id": "audit:000c5c6:1"
    },
    {
      "class": "consumer-half",
      "id": "audit:d3e8acf:2"
    },
    {
      "class": "consumer-half",
      "id": "audit:d3e8acf:1"
    },
    {
      "class": "evidence-reconciliation",
      "id": "audit:c646472:1"
    },
    {
      "class": "sweep-disposition-key",
      "id": "audit:c646472:2"
    },
    {
      "class": "text-defect",
      "id": "audit:b9f562e:1"
    },
    {
      "class": "evidence",
      "id": "audit:b9f562e:2"
    },
    {
      "class": "text-defect",
      "id": "audit:34cc889:1"
    },
    {
      "class": "counter-misread",
      "id": "audit:34cc889:2"
    },
    {
      "class": "counter-misread",
      "id": "audit:af86233:1"
    },
    {
      "class": "advisory-p2",
      "id": "audit:ba451c6:1"
    },
    {
      "class": "advisory-p2",
      "id": "audit:40f3be4:1"
    },
    {
      "class": "advisory-p2",
      "id": "audit:40f3be4:2"
    },
    {
      "class": "missing-owner-task",
      "id": "audit:ae03f00:1"
    },
    {
      "class": "worker-sandbox-discipline",
      "id": "audit:dbc8b67:1"
    },
    {
      "class": "sources",
      "id": "audit:a644a7d:1"
    },
    {
      "class": "replan-skipped",
      "id": "audit:a644a7d:2"
    }
  ],
  "pr": 439,
  "replans": {},
  "searches": [
    {
      "class": "advisory-p2",
      "records": []
    }
  ],
  "task": "dotfiles-T128-chain-review-scripts-followup-a07"
}
---

# Acceptance record: dotfiles-T128-chain-review-scripts-followup-a07

- 2026-10-20T04:14Z: owner follow-up text (security: false; predecessor a06 merged as PR #434 at 118daafa; code files disjoint from every in-flight task); pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; Checks block pasted; AGMSG-TASK round 1 dispatched to a011 (Claude, worker-d, wJ:p4) via dispatch.sh (`t128-a07-dispatch.txt`, task_sha256 ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75); read_at filled by fill-dispatch.py.
- 2026-10-20T04:24Z: amendment 1 before any worker edit: the text named PR #402 (the a05 PR; its advisory row was a06's) where the owner pattern means #434, and read its rows from a `## Owned by …-a07` section the a06 record lacked (the same defect a009 found on the T129 a06 owner text, C-102); the section is written with zero rows (the #434 audits' P2s were orchestration findings fixed in the record), so Item 1 is vacuous and Item 2 carries the task; dispatched to a011 as task_sha256 ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75 (`t128-a07-amend1.txt`).
owner-text:ae03f00:1	missing-owner-task
- 2026-10-20T04:31Z: correction: the 04:22:08Z send (2710) carried the unamended sha256 ae03f009… because the orchestrator's amendment script asserted three occurrences of `PR #402` where the text had four and stopped before writing (the dispatch step did not check the script's exit); the text is now amended in four places and resent as task_sha256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 (`t128-a07-amend1b.txt`), superseding 2710. Mechanism: the dispatch glue stops on any failed step (`set -e` in the amendment commands; M-20261020-03).
- 2026-10-20T04:59:48Z: a011 RESULT round 1 `status=ready_for_review`: PR #439 (draft) head 6a38e12d (code head c82e10a8, base 60a6fb2b, branch tools/chain-review-scripts-followup-a07), task_copy b91cc496 (amendment 1). Item 1 vacuous (the record section). Item 2: local-review.sh resolves gh as codex does (absolute, no shim), reads canonical main with `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha` before any checkout, refuses (exit 2, named) unless 40-hex and a local commit, passes it to `codex review --base`, exports GIT_NO_REPLACE_OBJECTS=1 and GIT_GRAFT_FILE=/dev/null before any git call; test `test_local_review_takes_its_base_from_canonical_main_never_a_local_ref` (planted local main/origin-main, 4 refusals, replace-ref and graft sub-tests) red at 6a4190f1/06cc0fe1, green at c82e10a8; 19 tests OK; caps 26/200 outside tests, 69/1000 under tests; 10 mutations each red; worker review round 1 on 60a6fb2b..fb264487: 1 P2 (replace ref steers the base; fixed) + 3 P3 (fixed/row/declared outside allowed_files: chain-integrate.sh:133 stale comment). CI on 6a38e12d: all pass except `regime` (run 39370972331: the task copy differs from main's pre-amendment a07 text ae03f009). Bot: none after 928 s. INV-6: amendments 1, questions 0, worker-side fix rounds 1.
- 2026-10-20T05:01Z: ACCEPTANCE `status=pending-integration round=1` (`t128-a07-acc-pending.txt`): the regime failure is the records gap; the amended text (b91cc496) joins records PR #438; after its merge the orchestrator marks #439 ready (`gh pr ready`), update-branches it and runs the chain. The worker's P3 on chain-integrate.sh:133 (stale comment, outside allowed_files) is an advisory row for the next owner text.

## Owned by dotfiles-T128-chain-review-scripts-followup-a09

- `chain:6434c27:1` ineffective-guard: at 2026-10-20T08:46Z `chain-integrate.sh`'s `gh pr checks --required --watch` on PR #432 head 6434c27c exited with `required checks failed` while no check had failed (four pending, three shown as `pending 0`); with the `chain:cd47e1b:1` row this is the second time the watch misreads a transient check-run state; the chain should decide from the check-runs API's conclusions with a bounded re-read.
- `chain:cd47e1b:1` ineffective-guard: `chain-integrate.sh` waits on `gh pr checks <pr> --required --watch`, which keys on check-run *status*; on 2026-10-20 (PR #441, head cd47e1b0) a required check run stayed `in_progress` with `conclusion=success` for 40+ minutes and the chain hung until the job was re-run. The chain decides from conclusions (as the ruleset does), with a bounded watch that re-reads the check-runs API and names the stuck run; one test with a fake gh returning in_progress+success.
- `worker:6a38e12:1` stale-line-number (a011's P3, 2026-10-20T04:59Z): `chain-integrate.sh:133` carries a stale comment; fix the comment.
- 2026-10-20T07:31:17Z: #438 merged as main f7ed0142 (the amended a07 text is on main); `gh pr ready 439` and `gh pr update-branch 439` next, then CI, chain.

## Lineage rows carried from dotfiles-T128-chain-review-scripts-followup-a06

audit:b6ce4ff:1	review-binary-shim
audit:b6ce4ff:2	task-arg-traversal
audit:b6ce4ff:3	sed-path-interpolation
audit:b6ce4ff:4	test-order-unproven
audit:b6ce4ff:5	owner-not-on-main
audit:b6ce4ff:6	sandbox-record-incomplete
audit:b6ce4ff:7	report-base-sha
audit:c45f9b5:1	review-binary-shim
audit:c45f9b5:2	advisory-policy-reading
audit:2e3ff49:1	env-s-quoting
audit:2e3ff49:2	missing-owner-task
audit:ba451c6:2	advisory-deferral-objection
audit:ba451c6:3	sandbox-count-understated
audit:40f3be4:3	evidence-command-unlanded-owner
audit:000c5c6:1	filename-suffix-parse
audit:d3e8acf:2	consumer-half
audit:d3e8acf:1	consumer-half
audit:c646472:1	evidence-reconciliation
audit:c646472:2	sweep-disposition-key
audit:b9f562e:1	text-defect
audit:b9f562e:2	evidence
audit:34cc889:1	text-defect
audit:34cc889:2	counter-misread
audit:af86233:1	counter-misread

- 2026-10-20T07:47Z: lineage rows carried before the chain (M-20261019-06): 24 audit rows from dotfiles-T128-chain-review-scripts-followup-a06.
- 2026-10-20T08:09:40Z: the chain on dbc8b67d stopped (rc=11) at the local review: one P1 (`…-local-review-dbc8b67.md`): local-review.sh:36 exports `GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null`, but Codex's checked-in `shell_environment_policy.inherit = "core"` drops exported variables from the reviewer's spawned commands, so a planted replacement is ignored by the wrapper's checkout yet honoured by the reviewer's `git diff` (an empty diff, a false clean review); the Bash-only stub bypasses that boundary. ACCEPTANCE `status=revise round=1` (`t128-a07-revise1.txt`): pass both through `shell_environment_policy.set` overrides and test the filtering boundary with a stub that records its config overrides and a spawned command's environment; worker fix round 1 of 2. The local review also recorded the finding as advisory under `## Owned by …-a08`; the revise supersedes that row for this finding.
local:dbc8b67:1	worker-sandbox-discipline
- 2026-10-20T08:48:46Z: a011 RESULT round 1 (revise 1) `status=ready_for_review`: PR #439 head fea3843d (code head f5aaaf7e; previous dbc8b67d; task copy b91cc496 unchanged): local-review.sh passes `-c shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"` and `-c shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"` to codex before the review subcommand (TOML-quoted); red test 5a983079, fix f2778f36, acyclic attack fixtures f5aaaf7e; `revise.yaml` with previous_head and the selector (INV-3). ACCEPTANCE `status=pending-integration round=1` (2026-10-20T08:49Z, `t128-a07-acc-pending2.txt`). The chain had already update-branched #439 to main b8213131 and runs on the new head.
- 2026-10-20T08:51Z: the chain had update-branched #439 to a644a7d9 and was waiting for its CI (four jobs pending); the orchestrator stopped that wait to run the already-clean #432 first (the review worktree is one), and re-runs the #439 chain afterwards.

## Lineage rows carried from dotfiles-T128-chain-review-scripts-followup-a06

audit:ba451c6:1	advisory-p2
audit:40f3be4:1	advisory-p2
audit:40f3be4:2	advisory-p2
- 2026-10-20T09:21:07Z: the chain on a644a7d9 (sweep 0 gaps; ledger 27): task-level audit `…-audit-a644a7d.md` `Verdict: incorrect`, two P1: (1) specification: item 2 authenticates main's sha, but the review content still comes from the worker-writable shared object store (design 5.14 item 8 requires GitHub content or a private clone; local-review.sh:123 checks object existence and type only; disabling replacements and grafts does not authenticate overwritten objects); (2) orchestration: three TASK messages (2699, the erroneous resend 2710, the corrected 2716) make amendments = 2, INV-6's S2, with no handling. Counters (2026-10-20T09:22Z): `task=dotfiles-T128-chain-review-scripts-followup-a07 tasks=3 amendments=2 questions=0 results=2 withdrawn=0 revises=1 first_result_head=6a38e12dd1d4fc40d7e14757d7c2b02080fb7cbe bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-20T04:13:45Z..2026-10-20T08:48:46Z (4:35) source=live S2: amendments 2 >= 2 source=live detail: pr=invalid authors=claude-deep-dot tasks=01a15783-e8a8-7f5f-83ff-`. Decision (D-024-41): the lineage resets to `dotfiles-T128-chain-review-scripts-followup-a08` by another context, continuing PR #439 from a644a7d9 with the implementation unchanged and one new item (the review reads the head from a private clone no worker can write); the pre-written a08 owner text is renamed a09 (its `## Owned by` section here too); a011 holds (PING `t128-a07-hold-reset.txt`). The erroneous resend that cost the amendment is M-20261020-03.
audit:a644a7d:1	sources
audit:a644a7d:2	replan-skipped

[P1] high specification .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md:18 The control authenticates main’s SHA but leaves review content in the worker-writable shared object store. Design §5.14 item 8 requires GitHub content or a private clone. `local-review.sh:123` checks only object existence/type; disabling replacements and grafts does not authenticate overwritten objects. The report acknowledges this gap at line 96, but the task supplies neither mitigation nor an owning prerequisite.

[P1] high orchestration .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md:140 The record reports one amendment despite recording three TASK messages at lines 5–7. INV-6 counts every TASK after the first, including the erroneous resend: amendments therefore equal two, reaching the reset threshold. Subsequent revise/integration actions proceed without recorded S2 handling, counter output, or a reset/waiver.

The task declares no numbered invariant set; its inherited Completion clause references INV-6.

INV-6: violated .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md:140

Orchestration findings: 1

The task hash matches. Shell syntax, Python parsing, scope and caps pass. The script/tests match the validated code head; the supplied final-head feedback lists ten successful checks and dispositions for all five items.

📝 まとめ: [PR #439](https://github.com/mryfmo/dotfiles/pull/439) の指定 head を読み取り専用で監査し、仕様と運用に各1件の指摘を確認しました。ファイルは変更していません。

Not checked: live CI (`gh` and web access failed), real Codex execution, or test reruns requiring writes. The existing checkout was dirty; source inspection used the specified commit objects. The shared-store trust gap remains.
Verdict: incorrectcat: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md: No such file or directory

 succeeded in 146ms:
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
session id: 01a15cc3-d29c-7a42-833a-fb693a59caf3
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
指定のタスク本文と参照先の記録を読み、判断に使った対象と実際に実行される対象が一致する設計かを確認します。読み取り専用で進め、agmsg-orchestration と Ponytail のレビュー手順を参照します。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 3ms:
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
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md' in ~/Workspace/dotfiles
 succeeded in 9ms:
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md
 M .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a02.md
 M .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a02.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
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
 M .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-pins-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01.md
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
?? .orchestration/learning/mistakes/M-20261021-02-boundary-carried-unmasked-records.md
?? .orchestration/learning/mistakes/M-20261021-03-dispatch-without-the-disjointness-check.md
?? .orchestration/learning/mistakes/M-20261021-04-requirement-waived-in-a-dispatch-note.md
?? .orchestration/plans/024-allocation.tsv
?? .orchestration/plans/024-replan-20261021-v2.md
?? .orchestration/plans/024-replan-20261021.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-pins-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/024-replan-20261021-review-r1.md
?? .orchestration/validation/024-replan-20261021-v2-review-r2.md
?? .orchestration/validation/024-replan-20261021-v2-review-r3.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md.last.md
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
     3	task_id: dotfiles-T128-chain-review-scripts-followup-a08
     4	reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]
     5	kind: code
     6	security: true
     7	allowed_files:
     8	  - scripts/orchestrator/local-advisory.sh
     9	  - scripts/orchestrator/local-review.sh
    10	  - tests/unit/test_chain_review_scripts.py
    11	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**
    12	after: []
    13	retained_predecessor_directories:
    14	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
    15	threat_table:
    16	  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "residual: Item 1 has no owned rows; this file remains unchanged and the audit compares the final diff; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    17	  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    18	  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: fixtures and stub gh/git/codex run in temporary directories; the audit checks their content assertions and inherited regressions; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    19	  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: these records are untrusted evidence; the orchestrator compares them with the dispatched text, diff and final-head CI; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    20	  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: byte-identical to the dispatched file and dispatch SHA-256; the orchestrator compares both at acceptance; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    21	  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: unchanged on the branch at SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36; the orchestrator compares it at acceptance; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    22	  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: report, validation, sandbox, learning and autoskill records identify commands, statuses and provenance; every sandbox refusal is recorded; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    23	  - {control: "review-cache provenance and reuse", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
    24	  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: task-consistency checks run before dispatch and acceptance; the whole-file comparison detects changed worker metadata; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    25	  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    26	  - {control: "in-process effects", disposition: "residual: the script creates a private temporary repository and invokes the bound reviewer; tests use fixtures and never fetch live GitHub content; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    27	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: no workflow or interpreter file changes; Item 3 isolates Git/gh inputs and preserves the inherited binary/interpreter binding and Codex environment overrides; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    28	  - {control: "new or renamed scripts", disposition: "residual: none authorized; any new or renamed script is an undeclared change that fails audit; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    29	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: same-UID processes and shared credentials remain outside host isolation; host controls reduce accidents and prompt injection, with missing acceptance detected at the next records PR rather than prevented; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    30	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: private storage uses the declared sandbox boundary; Claude file-tool protection remains incomplete until P1-15, so no unrestricted same-UID protection is claimed; owner: dotfiles-T133-worker-write-boundary-a04."}
    31	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Item 3 uses clean Git/gh children and propagates Git isolation to reviewer children; the trusted-parent contract applies by reference, without a self-reexec repair; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    32	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: the private temporary root and bound tools are checked under this item; worker-root and symlink aliases are refused, while unrestricted same-UID replacement remains possible; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    33	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: the same resolved tools and verified private-clone commits are consumed without rediscovery; unrestricted same-UID replacement between checks remains possible; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    34	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: Item 3 revalidates full head/base/tree cache identity after fresh private fetch; each private root is unique and no slot reservation is introduced; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    35	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: this table distinguishes the private-object-source fix from inherited host, credential, executable and reservation limitations; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    36	  - {control: "design 5.14 item 7: 検証", disposition: "residual: Item 3 adds content-source and refusal red/green tests and retains the existing execution-boundary tests; it does not claim the whole trusted-execution contract is closed; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    37	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    38	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: review objects use a fresh private store without alternates and review artifacts use orchestrator-private storage; inherited executable provenance remains a host-control residual; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    39	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: all Codex worker commands remain sandboxed under Worker Playbook step 4; a denial produces a blocked PONG without escalation; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    40	  - {control: "orchestrator effect merge", disposition: "residual: only gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker never merges or pushes main; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    41	  - {control: "orchestrator effect update-branch", disposition: "residual: an updated head invalidates earlier CI, sweep and audit evidence; repeat them on the new head before the gate; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    42	  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; dirty-worktree removal requires explicit force and an acceptance record of discarded state; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    43	premises:
    44	  - claim: "worker (Codex seat, review-profile authoring context): the local continuation commit resolves to the head named by D-024-41; this probe does not authenticate its content."
    45	    command: |-
    46	      git rev-parse --verify 'a644a7d9^{commit}'
    47	    output: |-
    48	      a644a7d965399b9463e9b32721287440a7efa233
    49	  - claim: "worker (Codex seat, review-profile authoring context): the predecessor task copy at the continuation head has the dispatched a07 SHA-256."
    50	    command: |-
    51	      git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256
    52	    output: |-
    53	      b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -
    54	---
    55	
    56	# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content
    57	
    58	This text is the independent-context reset after INV-6 S2 (two amendments, including the erroneous resend; D-024-41), and the a07 findings history is in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md`.
    59	Continue PR #439 on `tools/chain-review-scripts-followup-a07` from `a644a7d965399b9463e9b32721287440a7efa233`, worker a013 (Codex, worker-h), retaining the inherited implementation (code head `f5aaaf7e`) except for Item 3; create no branch or PR.
    60	Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen (D-024-29) and applies by reference (D-024-30): `design: 5.14 items 2, 3, 4, 7, 8, 9`; items 0–10 have individual threat rows.
    61	Read the whole a07 task, its acceptance record and `.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md` before editing.
    62	
    63	## Item 1
    64	
    65	Vacuous as in a07: `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` in the a06 acceptance record has no rows; do not change `local-advisory.sh` or import the a09 owner's advisory rows.
    66	
    67	## Item 2
    68	
    69	Keep the implemented canonical-main binding: resolve gh before checkout and read `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; require successful exit and exactly 40 ASCII hexadecimal characters, with a named refusal otherwise.
    70	Neither local `main` nor `origin/main` selects the base; pass that exact SHA to `codex review --base`, with the commit check moved into Item 3's private store.
    71	Keep `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` both exported and passed through `-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"'` and `-c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'` so Codex-spawned Git receives them.
    72	Preserve the inherited binary/interpreter pinning, failed-review refusal, full-head equality, finding/output handling and red/green evidence, with cache trust and location revised by Item 3; do not undo implemented fixes to reproduce inherited reds.
    73	
    74	## Item 3
    75	
    76	Close audit `audit:a644a7d:1`: `local-review.sh` never reads review content from the shared object store; checking object existence/type there or suppressing replacements/grafts does not authenticate overwritten objects.
    77	On every invocation, before any cache read, create a fresh mode-0700 private directory under `${TMPDIR:-/tmp}`, check its path under design 5.14 item 3, and create a bare repository there with `git init --bare <dir>`, followed by `git --git-dir=<dir> fetch https://github.com/mryfmo/dotfiles.git <head40> <base40>`.
    78	Use that explicit HTTPS URL, never a remote name, URL rewriting, local transport, alternates, `--reference`, `--shared`, copied objects or the shared `.git` as an object source; apply design 5.14 items 2, 4 and 9 to Git and its reviewer-spawned children, retaining Item 2's overrides.
    79	Apply design 5.14 items 2, 3, 4 and 9 to Git, gh and reviewer bindings before checkout; use fresh `GH_CONFIG_DIR` and read the token once with the bound gh's `auth token --hostname github.com`, as in `.orchestration/tasks/dotfiles-T133-python-pin-a02.md` Commands (e)/(e'); run Item 2's isolated canonical-main lookup on every invocation before any cache read.
    80	Never print or persist the token or pass it to Codex; the canonical-main lookup and explicit-URL private fetch cannot be skipped by any cached artifact.
    81	Verify both exact full SHAs in the private repository have object type `commit`, check out that head into its own worktree, and verify its HEAD; run `codex review --base <base40>` there when Item 3's cache check requires review, never in the former shared review worktree.
    82	Before any cache read, recompute the verified private-clone head SHA, canonical-main SHA and head tree hash (`git --git-dir=<dir> rev-parse <head40>^{tree}`); the first two must equal the requested head and Item 2's canonical-main result.
    83	Store reusable artifacts only as `<anchored-checkout>/.agents/worklog/local-review/<task>-local-review-<head40>.md` under design 5.14 items 1, 3 and 9, outside every worker-writable path; legacy artifacts in the shared store cannot authorize reuse.
    84	A cache hit may skip only the model call, and only if a private artifact records full `head:`, `base:` (canonical main) and `tree:` values exactly equal to all three freshly recomputed values; preserve finding counts and exit behavior.
    85	Absent, legacy, malformed, untrusted-location or mismatched artifacts require a new review and a rewritten private artifact after success; full-head equality or `findings: 0` alone never permits reuse.
    86	On fetch failure emit `local-review: private fetch failed`; on a missing/non-commit/mismatched SHA emit `local-review: private commit check failed`; both exit 2, invoke no reviewer, write no review artifact and never fall back to the shared store.
    87	Remove only this invocation's private repository/worktree on completion or refusal; preserve the inherited failed-review transcript behavior.
    88	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects`: stub gh/git, plant an overwritten object in the shared store with forged content, supply different canonical content through the explicit-URL private fetch, and have the reviewer stub read content from its actual cwd; assert canonical content, isolated Git/gh inputs and private object provenance, not merely argv or a directory name.
    89	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_refuses_a_failed_private_fetch_or_commit_check`, with subcases for fetch failure and each missing/non-commit/mismatched head or base SHA, including a matching private cache; assert the named refusal, no reviewer call, no artifact creation or rewrite and no shared fallback.
    90	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache`: plant a shared artifact with matching `head:` and `findings: 0`, including a variant with matching `base:`/`tree:`; assert fresh canonical-main lookup/private fetch precede any cache read, the reviewer runs in the canonical private checkout and rewrites the artifact privately.
    91	In that test, verify a valid private head/base/tree cache skips only the model after fresh lookup/fetch, and a changed head, canonical main, tree or missing metadata reruns review; failed lookup/fetch cannot return cached success.
    92	Record each new test red against `a644a7d9` on its security assertion, not a bootstrap failure, and green after Item 3; adapt inherited worktree fixtures to private-clone behavior and keep all other regression assertions.
    93	
    94	## Check and Completion
    95	
    96	Host facts: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
    97	Before validation, run that uv resolve command and paste its actual output; record the bound interpreter's realpath/version under design 5.14 items 2, 4 and 9, never guess an uv operand.
    98	Run `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v`, `bash -n scripts/orchestrator/local-review.sh`, `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh` and the repository's applicable lint checks; paste exact commands, resolved operands, exit statuses and complete outputs in `validation.md`; never run Bats locally.
    99	The whole PR is at most 120 changed lines outside `tests/` and `.orchestration/`, and at most 400 under `tests/`, counting additions plus deletions and attributing the inherited 26 outside-test lines and 69 test lines separately from Item 3.
   100	Run `git --git-dir=<private-bare> diff --numstat <base40>...<head40>` in the authenticated private repository with resolved full SHAs and record its complete output.
   101	The orchestrator records the resolved measurement base at dispatch; attribute inherited and Item 3 additions plus deletions separately against that base and the final head.
   102	Keep this complete task text at or under 140 lines; no workflow, permission, dependency, launcher, knowledge-graph or predecessor-artifact changes are authorized.
   103	Worker Playbook step 4 applies: every a013 command, including gh, Git and agmsg delivery, stays sandboxed; push without `-u` over HTTPS (`git push https://github.com/mryfmo/dotfiles.git tools/chain-review-scripts-followup-a07`); any denial sends a blocked PONG with exact command, status and boundary, without escalation or substitute tools.
   104	Do not probe the herdr socket from this Codex seat; host placement and delivery verification belong to the orchestrator.
   105	Copy this text byte-identically to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md`; keep the a07 task copy and evidence unchanged, and keep plan/todo/learn uncommitted with at most one active todo per owner.
   106	Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker crit-data evidence with a `-worker-` infix under `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/`; record inherited/new evidence provenance and `cost:`; never open a browser review or request human review.
   107	Every evidence item names its producer and seat kind: `worker (Codex seat, a013)` or `orchestrator (Claude seat, sandboxed Bash)`; authoring probes identify their separate Codex review-profile producer, and inherited evidence retains its original producer.
   108	Keep evidence artifacts untracked at the same relative paths in worker-h for orchestrator transfer when main-checkout paths are inaccessible; record exact commands, operands, statuses, complete output and every sandbox refusal without secrets.
   109	After the final push verify GitHub Actions and wait for the Bot under the Worker Playbook; fix P0/P1 within INV-6 and the one Bot fix round, otherwise report surviving findings for the operator; the orchestrator dispositions and resolves threads.
   110	RESULT names PR, full head/base, branch, changed files, test selectors, red/green commits, caps and artifact paths, plus `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md>`.
   111	The orchestrator records counters before acceptance actions, carries the a07 history, and performs the final-head sweep, audit, acceptance and gate in Orchestrator Playbook step 10 order; any head update repeats the required evidence; advisory ownership remains `dotfiles-T128-chain-review-scripts-followup-a09`.
   112	
   113	## Checks
   114	

**Separating clean budget outputs**
exec
/bin/zsh -lc "sed -n '/## Codex seat worklogs/,/"'^## /p'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 60ms:
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
/bin/zsh -lc 'git status --short; git rev-parse HEAD; nl -ba .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md | head -56; cat .ua/meta.json' in ~/Workspace/dotfiles
 succeeded in 42ms:
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md
 M .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a02.md
 M .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a02.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
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
 M .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-pins-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01.md
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
?? .orchestration/learning/mistakes/M-20261021-02-boundary-carried-unmasked-records.md
?? .orchestration/learning/mistakes/M-20261021-03-dispatch-without-the-disjointness-check.md
?? .orchestration/learning/mistakes/M-20261021-04-requirement-waived-in-a-dispatch-note.md
?? .orchestration/plans/024-allocation.tsv
?? .orchestration/plans/024-replan-20261021-v2.md
?? .orchestration/plans/024-replan-20261021.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-entrypoint-pins-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/024-replan-20261021-review-r1.md
?? .orchestration/validation/024-replan-20261021-v2-review-r2.md
?? .orchestration/validation/024-replan-20261021-v2-review-r3.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md.last.md
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
e042663b2d6efd9205f7d388bf881c01d3880642
     1	---
     2	format: 2
     3	task_id: dotfiles-T128-chain-review-scripts-followup-a08
     4	reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]
     5	kind: code
     6	security: true
     7	allowed_files:
     8	  - scripts/orchestrator/local-advisory.sh
     9	  - scripts/orchestrator/local-review.sh
    10	  - tests/unit/test_chain_review_scripts.py
    11	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**
    12	after: []
    13	retained_predecessor_directories:
    14	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
    15	threat_table:
    16	  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "residual: Item 1 has no owned rows; this file remains unchanged and the audit compares the final diff; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    17	  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    18	  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: fixtures and stub gh/git/codex run in temporary directories; the audit checks their content assertions and inherited regressions; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    19	  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: these records are untrusted evidence; the orchestrator compares them with the dispatched text, diff and final-head CI; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    20	  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: byte-identical to the dispatched file and dispatch SHA-256; the orchestrator compares both at acceptance; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    21	  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: unchanged on the branch at SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36; the orchestrator compares it at acceptance; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    22	  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: report, validation, sandbox, learning and autoskill records identify commands, statuses and provenance; every sandbox refusal is recorded; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    23	  - {control: "review-cache provenance and reuse", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
    24	  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: task-consistency checks run before dispatch and acceptance; the whole-file comparison detects changed worker metadata; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    25	  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    26	  - {control: "in-process effects", disposition: "residual: the script creates a private temporary repository and invokes the bound reviewer; tests use fixtures and never fetch live GitHub content; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    27	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: no workflow or interpreter file changes; Item 3 isolates Git/gh inputs and preserves the inherited binary/interpreter binding and Codex environment overrides; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    28	  - {control: "new or renamed scripts", disposition: "residual: none authorized; any new or renamed script is an undeclared change that fails audit; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    29	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: same-UID processes and shared credentials remain outside host isolation; host controls reduce accidents and prompt injection, with missing acceptance detected at the next records PR rather than prevented; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    30	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: private storage uses the declared sandbox boundary; Claude file-tool protection remains incomplete until P1-15, so no unrestricted same-UID protection is claimed; owner: dotfiles-T133-worker-write-boundary-a04."}
    31	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Item 3 uses clean Git/gh children and propagates Git isolation to reviewer children; the trusted-parent contract applies by reference, without a self-reexec repair; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    32	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: the private temporary root and bound tools are checked under this item; worker-root and symlink aliases are refused, while unrestricted same-UID replacement remains possible; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    33	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: the same resolved tools and verified private-clone commits are consumed without rediscovery; unrestricted same-UID replacement between checks remains possible; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    34	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: Item 3 revalidates full head/base/tree cache identity after fresh private fetch; each private root is unique and no slot reservation is introduced; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    35	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: this table distinguishes the private-object-source fix from inherited host, credential, executable and reservation limitations; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    36	  - {control: "design 5.14 item 7: 検証", disposition: "residual: Item 3 adds content-source and refusal red/green tests and retains the existing execution-boundary tests; it does not claim the whole trusted-execution contract is closed; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    37	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    38	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: review objects use a fresh private store without alternates and review artifacts use orchestrator-private storage; inherited executable provenance remains a host-control residual; owner: dotfiles-T133-trusted-entrypoint-binding-a01."}
    39	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: all Codex worker commands remain sandboxed under Worker Playbook step 4; a denial produces a blocked PONG without escalation; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    40	  - {control: "orchestrator effect merge", disposition: "residual: only gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker never merges or pushes main; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    41	  - {control: "orchestrator effect update-branch", disposition: "residual: an updated head invalidates earlier CI, sweep and audit evidence; repeat them on the new head before the gate; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    42	  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; dirty-worktree removal requires explicit force and an acceptance record of discarded state; owner: dotfiles-T128-chain-review-scripts-followup-a08."}
    43	premises:
    44	  - claim: "worker (Codex seat, review-profile authoring context): the local continuation commit resolves to the head named by D-024-41; this probe does not authenticate its content."
    45	    command: |-
    46	      git rev-parse --verify 'a644a7d9^{commit}'
    47	    output: |-
    48	      a644a7d965399b9463e9b32721287440a7efa233
    49	  - claim: "worker (Codex seat, review-profile authoring context): the predecessor task copy at the continuation head has the dispatched a07 SHA-256."
    50	    command: |-
    51	      git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256
    52	    output: |-
    53	      b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -
    54	---
    55	
    56	# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

**Clarifying scope without graph**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md; cat .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '"'^### 5.14|''^### 5.15|D-024-(21|29|30|41)|trusted|Commands|'"\\(e' .orchestration/plans/024-design-quality.md .orchestration/tasks/dotfiles-T133-python-pin-a02.md; nl -ba scripts/orchestrator/local-review.sh" in ~/Workspace/dotfiles
 exited 1 in 99ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a07 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md task_sha256=ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75 deadline=none done_signal=AGMSG-RESULT note=a011:owner-follow-up-a07(predecessor-a06-merged-as-PR-434-at-118daafa;security-false;pre-send-on-these-bytes:task-consistency-check-OK,SECRET_PATTERN-0,home-paths-0;your-PR-436-stays-on-its-branch-for-its-pending-acceptance,this-task-starts-on-its-own-branch-as-the-text-says)",
    "AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a07 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md task_sha256=ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75 deadline=none done_signal=AGMSG-RESULT note=a011:amendment-1(previous_sha256=ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75;PR-402->434-in-three-sentences,nothing-else;the-section-'Owned-by-…-a07'-now-exists-in-the-a06-record-with-zero-rows:Item-1-is-vacuous,Item-2-carries-the-task;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)",
    "AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a07 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md task_sha256=b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 deadline=none done_signal=AGMSG-RESULT note=a011:amendment-1-resent(message-2710-carried-the-unamended-sha256-ae03f009…-by-an-orchestrator-script-error:disregard-it;previous_sha256=ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75;PR-402->434-in-four-places,nothing-else;the-section-'Owned-by-…-a07'-exists-in-the-a06-record-with-zero-rows:Item-1-is-vacuous,Item-2-carries-the-task;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-chain-review-scripts-followup-a07 status=pending-integration round=1 pr=439 head=6a38e12dd1d4fc40d7e14757d7c2b02080fb7cbe reason=RESULT-of-04:59:48Z-read:item-2-implemented(canonical-main-base-via-gh-api,4-named-refusals,replace-ref-and-graft-sub-tests,19-OK,caps-26/200-and-69/1000),item-1-vacuous-as-the-record-section-says;your-decision_for_you-is-accepted:the-regime-failure-is-the-records-gap(main-holds-the-pre-amendment-a07-text-ae03f009);the-amended-text-b91cc496-joins-records-PR-438;after-its-merge-the-orchestrator-marks-439-ready,update-branches-it,and-runs-the-chain(sweep,audit,gate);no-worker-action;the-draft-stays-as-is"
  ],
  "format": 1,
  "head": "a644a7d965399b9463e9b32721287440a7efa233",
  "ledger": [
    {
      "class": "review-binary-shim",
      "id": "audit:b6ce4ff:1"
    },
    {
      "class": "task-arg-traversal",
      "id": "audit:b6ce4ff:2"
    },
    {
      "class": "sed-path-interpolation",
      "id": "audit:b6ce4ff:3"
    },
    {
      "class": "test-order-unproven",
      "id": "audit:b6ce4ff:4"
    },
    {
      "class": "owner-not-on-main",
      "id": "audit:b6ce4ff:5"
    },
    {
      "class": "sandbox-record-incomplete",
      "id": "audit:b6ce4ff:6"
    },
    {
      "class": "report-base-sha",
      "id": "audit:b6ce4ff:7"
    },
    {
      "class": "review-binary-shim",
      "id": "audit:c45f9b5:1"
    },
    {
      "class": "advisory-policy-reading",
      "id": "audit:c45f9b5:2"
    },
    {
      "class": "env-s-quoting",
      "id": "audit:2e3ff49:1"
    },
    {
      "class": "missing-owner-task",
      "id": "audit:2e3ff49:2"
    },
    {
      "class": "advisory-deferral-objection",
      "id": "audit:ba451c6:2"
    },
    {
      "class": "sandbox-count-understated",
      "id": "audit:ba451c6:3"
    },
    {
      "class": "evidence-command-unlanded-owner",
      "id": "audit:40f3be4:3"
    },
    {
      "class": "filename-suffix-parse",
      "id": "audit:000c5c6:1"
    },
    {
      "class": "consumer-half",
      "id": "audit:d3e8acf:2"
    },
    {
      "class": "consumer-half",
      "id": "audit:d3e8acf:1"
    },
    {
      "class": "evidence-reconciliation",
      "id": "audit:c646472:1"
    },
    {
      "class": "sweep-disposition-key",
      "id": "audit:c646472:2"
    },
    {
      "class": "text-defect",
      "id": "audit:b9f562e:1"
    },
    {
      "class": "evidence",
      "id": "audit:b9f562e:2"
    },
    {
      "class": "text-defect",
      "id": "audit:34cc889:1"
    },
    {
      "class": "counter-misread",
      "id": "audit:34cc889:2"
    },
    {
      "class": "counter-misread",
      "id": "audit:af86233:1"
    },
    {
      "class": "advisory-p2",
      "id": "audit:ba451c6:1"
    },
    {
      "class": "advisory-p2",
      "id": "audit:40f3be4:1"
    },
    {
      "class": "advisory-p2",
      "id": "audit:40f3be4:2"
    },
    {
      "class": "missing-owner-task",
      "id": "audit:ae03f00:1"
    },
    {
      "class": "worker-sandbox-discipline",
      "id": "audit:dbc8b67:1"
    },
    {
      "class": "sources",
      "id": "audit:a644a7d:1"
    },
    {
      "class": "replan-skipped",
      "id": "audit:a644a7d:2"
    }
  ],
  "pr": 439,
  "replans": {},
  "searches": [
    {
      "class": "advisory-p2",
      "records": []
    }
  ],
  "task": "dotfiles-T128-chain-review-scripts-followup-a07"
}
---

# Acceptance record: dotfiles-T128-chain-review-scripts-followup-a07

- 2026-10-20T04:14Z: owner follow-up text (security: false; predecessor a06 merged as PR #434 at 118daafa; code files disjoint from every in-flight task); pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; Checks block pasted; AGMSG-TASK round 1 dispatched to a011 (Claude, worker-d, wJ:p4) via dispatch.sh (`t128-a07-dispatch.txt`, task_sha256 ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75); read_at filled by fill-dispatch.py.
- 2026-10-20T04:24Z: amendment 1 before any worker edit: the text named PR #402 (the a05 PR; its advisory row was a06's) where the owner pattern means #434, and read its rows from a `## Owned by …-a07` section the a06 record lacked (the same defect a009 found on the T129 a06 owner text, C-102); the section is written with zero rows (the #434 audits' P2s were orchestration findings fixed in the record), so Item 1 is vacuous and Item 2 carries the task; dispatched to a011 as task_sha256 ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75 (`t128-a07-amend1.txt`).
owner-text:ae03f00:1	missing-owner-task
- 2026-10-20T04:31Z: correction: the 04:22:08Z send (2710) carried the unamended sha256 ae03f009… because the orchestrator's amendment script asserted three occurrences of `PR #402` where the text had four and stopped before writing (the dispatch step did not check the script's exit); the text is now amended in four places and resent as task_sha256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 (`t128-a07-amend1b.txt`), superseding 2710. Mechanism: the dispatch glue stops on any failed step (`set -e` in the amendment commands; M-20261020-03).
- 2026-10-20T04:59:48Z: a011 RESULT round 1 `status=ready_for_review`: PR #439 (draft) head 6a38e12d (code head c82e10a8, base 60a6fb2b, branch tools/chain-review-scripts-followup-a07), task_copy b91cc496 (amendment 1). Item 1 vacuous (the record section). Item 2: local-review.sh resolves gh as codex does (absolute, no shim), reads canonical main with `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha` before any checkout, refuses (exit 2, named) unless 40-hex and a local commit, passes it to `codex review --base`, exports GIT_NO_REPLACE_OBJECTS=1 and GIT_GRAFT_FILE=/dev/null before any git call; test `test_local_review_takes_its_base_from_canonical_main_never_a_local_ref` (planted local main/origin-main, 4 refusals, replace-ref and graft sub-tests) red at 6a4190f1/06cc0fe1, green at c82e10a8; 19 tests OK; caps 26/200 outside tests, 69/1000 under tests; 10 mutations each red; worker review round 1 on 60a6fb2b..fb264487: 1 P2 (replace ref steers the base; fixed) + 3 P3 (fixed/row/declared outside allowed_files: chain-integrate.sh:133 stale comment). CI on 6a38e12d: all pass except `regime` (run 39370972331: the task copy differs from main's pre-amendment a07 text ae03f009). Bot: none after 928 s. INV-6: amendments 1, questions 0, worker-side fix rounds 1.
- 2026-10-20T05:01Z: ACCEPTANCE `status=pending-integration round=1` (`t128-a07-acc-pending.txt`): the regime failure is the records gap; the amended text (b91cc496) joins records PR #438; after its merge the orchestrator marks #439 ready (`gh pr ready`), update-branches it and runs the chain. The worker's P3 on chain-integrate.sh:133 (stale comment, outside allowed_files) is an advisory row for the next owner text.

## Owned by dotfiles-T128-chain-review-scripts-followup-a09

- `chain:6434c27:1` ineffective-guard: at 2026-10-20T08:46Z `chain-integrate.sh`'s `gh pr checks --required --watch` on PR #432 head 6434c27c exited with `required checks failed` while no check had failed (four pending, three shown as `pending 0`); with the `chain:cd47e1b:1` row this is the second time the watch misreads a transient check-run state; the chain should decide from the check-runs API's conclusions with a bounded re-read.
- `chain:cd47e1b:1` ineffective-guard: `chain-integrate.sh` waits on `gh pr checks <pr> --required --watch`, which keys on check-run *status*; on 2026-10-20 (PR #441, head cd47e1b0) a required check run stayed `in_progress` with `conclusion=success` for 40+ minutes and the chain hung until the job was re-run. The chain decides from conclusions (as the ruleset does), with a bounded watch that re-reads the check-runs API and names the stuck run; one test with a fake gh returning in_progress+success.
- `worker:6a38e12:1` stale-line-number (a011's P3, 2026-10-20T04:59Z): `chain-integrate.sh:133` carries a stale comment; fix the comment.
- 2026-10-20T07:31:17Z: #438 merged as main f7ed0142 (the amended a07 text is on main); `gh pr ready 439` and `gh pr update-branch 439` next, then CI, chain.

## Lineage rows carried from dotfiles-T128-chain-review-scripts-followup-a06

audit:b6ce4ff:1	review-binary-shim
audit:b6ce4ff:2	task-arg-traversal
audit:b6ce4ff:3	sed-path-interpolation
audit:b6ce4ff:4	test-order-unproven
audit:b6ce4ff:5	owner-not-on-main
audit:b6ce4ff:6	sandbox-record-incomplete
audit:b6ce4ff:7	report-base-sha
audit:c45f9b5:1	review-binary-shim
audit:c45f9b5:2	advisory-policy-reading
audit:2e3ff49:1	env-s-quoting
audit:2e3ff49:2	missing-owner-task
audit:ba451c6:2	advisory-deferral-objection
audit:ba451c6:3	sandbox-count-understated
audit:40f3be4:3	evidence-command-unlanded-owner
audit:000c5c6:1	filename-suffix-parse
audit:d3e8acf:2	consumer-half
audit:d3e8acf:1	consumer-half
audit:c646472:1	evidence-reconciliation
audit:c646472:2	sweep-disposition-key
audit:b9f562e:1	text-defect
audit:b9f562e:2	evidence
audit:34cc889:1	text-defect
audit:34cc889:2	counter-misread
audit:af86233:1	counter-misread

- 2026-10-20T07:47Z: lineage rows carried before the chain (M-20261019-06): 24 audit rows from dotfiles-T128-chain-review-scripts-followup-a06.
- 2026-10-20T08:09:40Z: the chain on dbc8b67d stopped (rc=11) at the local review: one P1 (`…-local-review-dbc8b67.md`): local-review.sh:36 exports `GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null`, but Codex's checked-in `shell_environment_policy.inherit = "core"` drops exported variables from the reviewer's spawned commands, so a planted replacement is ignored by the wrapper's checkout yet honoured by the reviewer's `git diff` (an empty diff, a false clean review); the Bash-only stub bypasses that boundary. ACCEPTANCE `status=revise round=1` (`t128-a07-revise1.txt`): pass both through `shell_environment_policy.set` overrides and test the filtering boundary with a stub that records its config overrides and a spawned command's environment; worker fix round 1 of 2. The local review also recorded the finding as advisory under `## Owned by …-a08`; the revise supersedes that row for this finding.
local:dbc8b67:1	worker-sandbox-discipline
- 2026-10-20T08:48:46Z: a011 RESULT round 1 (revise 1) `status=ready_for_review`: PR #439 head fea3843d (code head f5aaaf7e; previous dbc8b67d; task copy b91cc496 unchanged): local-review.sh passes `-c shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"` and `-c shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"` to codex before the review subcommand (TOML-quoted); red test 5a983079, fix f2778f36, acyclic attack fixtures f5aaaf7e; `revise.yaml` with previous_head and the selector (INV-3). ACCEPTANCE `status=pending-integration round=1` (2026-10-20T08:49Z, `t128-a07-acc-pending2.txt`). The chain had already update-branched #439 to main b8213131 and runs on the new head.
- 2026-10-20T08:51Z: the chain had update-branched #439 to a644a7d9 and was waiting for its CI (four jobs pending); the orchestrator stopped that wait to run the already-clean #432 first (the review worktree is one), and re-runs the #439 chain afterwards.

## Lineage rows carried from dotfiles-T128-chain-review-scripts-followup-a06

audit:ba451c6:1	advisory-p2
audit:40f3be4:1	advisory-p2
audit:40f3be4:2	advisory-p2
- 2026-10-20T09:21:07Z: the chain on a644a7d9 (sweep 0 gaps; ledger 27): task-level audit `…-audit-a644a7d.md` `Verdict: incorrect`, two P1: (1) specification: item 2 authenticates main's sha, but the review content still comes from the worker-writable shared object store (design 5.14 item 8 requires GitHub content or a private clone; local-review.sh:123 checks object existence and type only; disabling replacements and grafts does not authenticate overwritten objects); (2) orchestration: three TASK messages (2699, the erroneous resend 2710, the corrected 2716) make amendments = 2, INV-6's S2, with no handling. Counters (2026-10-20T09:22Z): `task=dotfiles-T128-chain-review-scripts-followup-a07 tasks=3 amendments=2 questions=0 results=2 withdrawn=0 revises=1 first_result_head=6a38e12dd1d4fc40d7e14757d7c2b02080fb7cbe bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-20T04:13:45Z..2026-10-20T08:48:46Z (4:35) source=live S2: amendments 2 >= 2 source=live detail: pr=invalid authors=claude-deep-dot tasks=01a15783-e8a8-7f5f-83ff-`. Decision (D-024-41): the lineage resets to `dotfiles-T128-chain-review-scripts-followup-a08` by another context, continuing PR #439 from a644a7d9 with the implementation unchanged and one new item (the review reads the head from a private clone no worker can write); the pre-written a08 owner text is renamed a09 (its `## Owned by` section here too); a011 holds (PING `t128-a07-hold-reset.txt`). The erroneous resend that cost the amendment is M-20261020-03.
audit:a644a7d:1	sources
audit:a644a7d:2	replan-skipped

[P1] high specification .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md:18 The control authenticates main’s SHA but leaves review content in the worker-writable shared object store. Design §5.14 item 8 requires GitHub content or a private clone. `local-review.sh:123` checks only object existence/type; disabling replacements and grafts does not authenticate overwritten objects. The report acknowledges this gap at line 96, but the task supplies neither mitigation nor an owning prerequisite.

[P1] high orchestration .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md:140 The record reports one amendment despite recording three TASK messages at lines 5–7. INV-6 counts every TASK after the first, including the erroneous resend: amendments therefore equal two, reaching the reset threshold. Subsequent revise/integration actions proceed without recorded S2 handling, counter output, or a reset/waiver.

The task declares no numbered invariant set; its inherited Completion clause references INV-6.

INV-6: violated .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md:140

Orchestration findings: 1

The task hash matches. Shell syntax, Python parsing, scope and caps pass. The script/tests match the validated code head; the supplied final-head feedback lists ten successful checks and dispositions for all five items.

📝 まとめ: [PR #439](https://github.com/mryfmo/dotfiles/pull/439) の指定 head を読み取り専用で監査し、仕様と運用に各1件の指摘を確認しました。ファイルは変更していません。

Not checked: live CI (`gh` and web access failed), real Codex execution, or test reruns requiring writes. The existing checkout was dirty; source inspection used the specified commit objects. The shared-store trust gap remains.
Verdict: incorrectcat: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md: No such file or directory

---
{
  "audit_findings": [
    {
      "evidence": "bash scripts/regime-counters.sh dotfiles-T128-chain-review-scripts-followup-a06 | head -1",
      "n": "1",
      "reason": "fixed in this record before the gate: the counters re-measured with scripts/regime-counters.sh (task=dotfiles-T128-chain-review-scripts-followup-a06 tasks=2 amendments=1 questions=0 results=3 withdrawn=0 revises=2 first_result_head=2db7830bd7fa78e55aa9bdcc46c76201f0a21c3e bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-19T20:15:40Z..2026-10-20T01:01:45Z (4:46) source=live), the unknown Bot and audit counts resolved (0 Bot P1 heads: the Bot is at its usage limit; 3 audits), and the S2 decision recorded: two record-correction revises of a records-only PR, no design to redesign, integrate at af862335 with the owner a07 carrying the lineage"
    }
  ],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a06 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md task_sha256=e21ef5bef826e9d5c195d8145c26810c2fa438cf1c4a86b16ba7477d23d14749 deadline=none done_signal=AGMSG-RESULT note=a011:owner-task-of-a-merged-lineage;the-owned-row-is-in-the-predecessor-acceptance-record-Owned-by-section(an-evidence-record-correction;one-red-then-green-test-where-a-row-names-one);fresh-branch-from-origin/main-1eac64a8;security:false;files-disjoint-from-every-in-flight-task;the-task-copy-is-this-text-byte-identical",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-chain-review-scripts-followup-a06 status=pending-integration round=1 pr=434 head=2db7830bd7fa78e55aa9bdcc46c76201f0a21c3e reason=records-only-PR-read(a05-gh-calls.md-one-row-per-call-from-GitHub-timeline-and-regime-records;no-code);12-checks-pass-on-2db7830b;the-orchestrator-marks-the-PR-ready-and-runs-the-chain-after-#433;your-connector-notice-is-noted-as-an-operator-check;hold-the-seat",
    "AGMSG-TASK v1 task_id=dotfiles-T128-chain-review-scripts-followup-a06 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md task_sha256=7a8b997187a987c66bd8595146c478a170b419d38a775177d834b4100ace0c00 deadline=none done_signal=AGMSG-RESULT note=a011:amendment-1(previous_sha256=e21ef5bef826e9d5c195d8145c26810c2fa438cf1c4a86b16ba7477d23d14749;item-1-now-says-a-records-only-row-is-realised-by-the-record-it-names,no-test;audit-34cc889-finding-1);switch-to-tools/chain-review-scripts-followup-a06,update-the-task-copy-to-this-text-byte-identical,push-on-PR-434,RESULT-with-the-new-head;then-return-to-the-helper-task;C-61:second-and-last-round"
  ],
  "format": 1,
  "head": "af86233544ea2bf807c198c85d6f07580e0bed9c",
  "ledger": [
    {
      "class": "review-binary-shim",
      "id": "audit:b6ce4ff:1"
    },
    {
      "class": "task-arg-traversal",
      "id": "audit:b6ce4ff:2"
    },
    {
      "class": "sed-path-interpolation",
      "id": "audit:b6ce4ff:3"
    },
    {
      "class": "test-order-unproven",
      "id": "audit:b6ce4ff:4"
    },
    {
      "class": "owner-not-on-main",
      "id": "audit:b6ce4ff:5"
    },
    {
      "class": "sandbox-record-incomplete",
      "id": "audit:b6ce4ff:6"
    },
    {
      "class": "report-base-sha",
      "id": "audit:b6ce4ff:7"
    },
    {
      "class": "review-binary-shim",
      "id": "audit:c45f9b5:1"
    },
    {
      "class": "advisory-policy-reading",
      "id": "audit:c45f9b5:2"
    },
    {
      "class": "env-s-quoting",
      "id": "audit:2e3ff49:1"
    },
    {
      "class": "missing-owner-task",
      "id": "audit:2e3ff49:2"
    },
    {
      "class": "advisory-p2",
      "id": "audit:ba451c6:1"
    },
    {
      "class": "advisory-deferral-objection",
      "id": "audit:ba451c6:2"
    },
    {
      "class": "sandbox-count-understated",
      "id": "audit:ba451c6:3"
    },
    {
      "class": "advisory-p2",
      "id": "audit:40f3be4:1"
    },
    {
      "class": "advisory-p2",
      "id": "audit:40f3be4:2"
    },
    {
      "class": "evidence-command-unlanded-owner",
      "id": "audit:40f3be4:3"
    },
    {
      "class": "filename-suffix-parse",
      "id": "audit:000c5c6:1"
    },
    {
      "class": "consumer-half",
      "id": "audit:d3e8acf:2"
    },
    {
      "class": "consumer-half",
      "id": "audit:d3e8acf:1"
    },
    {
      "class": "evidence-reconciliation",
      "id": "audit:c646472:1"
    },
    {
      "class": "sweep-disposition-key",
      "id": "audit:c646472:2"
    },
    {
      "class": "text-defect",
      "id": "audit:b9f562e:1"
    },
    {
      "class": "evidence",
      "id": "audit:b9f562e:2"
    },
    {
      "class": "text-defect",
      "id": "audit:34cc889:1"
    },
    {
      "class": "counter-misread",
      "id": "audit:34cc889:2"
    },
    {
      "class": "counter-misread",
      "id": "audit:af86233:1"
    }
  ],
  "pr": 434,
  "replans": {},
  "searches": [
    {
      "class": "advisory-p2",
      "records": []
    }
  ],
  "task": "dotfiles-T128-chain-review-scripts-followup-a06"
}
---

# Acceptance record: dotfiles-T128-chain-review-scripts-followup-a06

Owner task of a merged lineage; its owned rows are read from the predecessor acceptance record at dispatch. security: false; dispatched under D-024-25 to keep the seats on disjoint work.

- 2026-10-19T20:1xZ: dispatched to claude-standard-dot-a011 (worker-d; sha e21ef5bef826e9d5c195d8145c26810c2fa438cf1c4a86b16ba7477d23d14749); counters pasted; no C-80 (security: false).
- 2026-10-19T21:09:08Z: a011 RESULT round 1 `status=ready_for_review`: PR #434 (draft) head 2db7830bd7fa78e55aa9bdcc46c76201f0a21c3e, base 1eac64a8, branch tools/chain-review-scripts-followup-a06, task_copy e21ef5be…; records only (a05-gh-calls.md: one row per gh call with seat, UTC time, outcome and evidence from the GitHub timeline and the regime records; the a05 report and record describe two seats, not a contradiction; a05 sandbox.md unchanged by C2); 0 changed lines outside .orchestration; 12 checks pass on 2db7830b; no Bot review after 905 s; two issue comments (CodeRabbit auto-summary; the Codex connector's `create a Codex account and connect` notice instead of a review, flagged for the operator). Adversarial read: the row's realisation matches the owned row; not_read: the whole bus history (C-53) — the creator seat rests on the a05 acceptance record, acceptable for a records row. ACCEPTANCE pending-integration sent 2026-10-19T21:14:13Z; the orchestrator marks the PR ready and chains it after #433; owner a07 text written (C-51).
- 2026-10-19T21:27:32Z: a011 PONG `status=alive`: the whole bus history read (2535 rows) finished after the RESULT and confirms a05-gh-calls.md rows 3 (message 2039, 23:47:01Z: the orchestrator opened PR #402 as a draft) and 4 (message 2070, 04:22:16Z: gh pr ready 405 and 402); one seat the record omits made no gh call (a009's a05 continuation TASK at 23:47:01Z, held by the 08:51 JST STOP, PONG no work since: message 2058). No revision: a seat without a gh call has no row. PING sent: hold; the chain runs after the #433 merge.
- 2026-10-20T06:3xJST: lineage audit rows carried before the chain (interim P1-6 procedure, M-20261019-06): 22 prose rows added, JSON ledger 22.
audit:b6ce4ff:1	review-binary-shim
audit:b6ce4ff:2	task-arg-traversal
audit:b6ce4ff:3	sed-path-interpolation
audit:b6ce4ff:4	test-order-unproven
audit:b6ce4ff:5	owner-not-on-main
audit:b6ce4ff:6	sandbox-record-incomplete
audit:b6ce4ff:7	report-base-sha
audit:c45f9b5:1	review-binary-shim
audit:c45f9b5:2	advisory-policy-reading
audit:2e3ff49:1	env-s-quoting
audit:2e3ff49:2	missing-owner-task
audit:ba451c6:1	advisory-p2
audit:ba451c6:2	advisory-deferral-objection
audit:ba451c6:3	sandbox-count-understated
audit:40f3be4:1	advisory-p2
audit:40f3be4:2	advisory-p2
audit:40f3be4:3	evidence-command-unlanded-owner
audit:000c5c6:1	filename-suffix-parse
audit:d3e8acf:2	consumer-half
audit:d3e8acf:1	consumer-half
audit:c646472:1	evidence-reconciliation
audit:c646472:2	sweep-disposition-key
- 2026-10-19T21:41:14Z: the chain on the update-branch head b9f562ec (local review clean, sweep 0 gaps, 22 lineage rows carried beforehand): task-level audit `…-audit-b9f562e.md` `Verdict: incorrect`: P2 orchestration (the hashed text's item 1 asks a red-then-green test per owned row while the dispatch note 2552 limited it to rows naming a test, and report.md:36 leans on that note: the second C-96 instance tonight; the text stands, the note was the orchestrator's); P3 evidence (a05-gh-calls.md:4 and report.md:34 name a05 sandbox.md lines 12-18 as superseded while the planned gh commands sit at 19-21). Disposition: revise round 1 to a011 at 2026-10-19T21:42:34Z (C-61 round 1 of 2): the range from a pasted grep -n, report.md:36 restated without the note; the template sentence for future owner texts (a07 and the prep template) reads 'one red-then-green test where the row names one; a records-only row is realised by the record it names'.
- 2026-10-19T22:46:13Z: a011 RESULT `round=revise-1`: head 34cc8894d029630910fe1c75e2f5a32d57f18b8b (fast-forward from b9f562ec, one records-only commit with revise.yaml): check 1 the superseded range is now a05 sandbox.md lines 19-21 from a pasted grep -n (line 18 the blocked-PONG dispatch row, line 22 the planned RESULT row); check 2 report.md states the realisation without the dispatch note; check 3 no other change (git diff --name-only b9f562ec 34cc8894: a05-gh-calls.md, report.md, revise.yaml, validation.md s7); 12 checks pass on 34cc8894; no Bot after 927 s; C-61 round 1 of 2. ACCEPTANCE pending-integration sent 2026-10-19T22:59:31Z; chain running.
- 2026-10-19T22:59:17Z: a011 PONG `alive` relaying a direction the operator typed into a011's pane (paraphrase): proceed per the convergence proposal with maximum parallel seats; (1) bring P1-6 forward (class hand-typed-chain, 18 of 83 records); (2) new task texts apply design 5.14 by reference, never restated per task, enforced by the P1-12 checker; keep P1-15 first; suggestions: a011 can take a P1-6 slice or the 5.14 item-7 shared test helper tests/unit/trusted_exec_contract.py now; the by-reference rule as a task-consistency-check C-rule. Recorded as relayed (an agent message carries no operator authority by itself); it coincides with the corrective measures already decided (P1-6 slice 1 authored; D-024-29) and is applied as the default: D-024-30 (5.14 by reference), the helper task text for a011, the checker rule as a P1-12 follow-up row. 23:01:15Z: the #434 chain on 34cc8894 stopped at pr-feedback (`gh api graphql … dial tcp 20.27.177.116:443: i/o timeout`, a GitHub API timeout from this host); re-run.
- 2026-10-19T23:18:43Z: the chain on 34cc8894 refused at the audit precheck (GAP audit:b9f562e:2): the two rows of this PR's own earlier audit were missing as prose rows; added (text-defect: the hashed text's item 1 against the dispatch note; evidence: the superseded line range). Re-run.
audit:b9f562e:1	text-defect
audit:b9f562e:2	evidence
- 2026-10-19T23:51:26Z: the chain on 34cc8894 audited (`…-audit-34cc889.md`, written although its run reported the masker failure) `Verdict: incorrect`: P2 the hashed text's item 1 still asks a test per row (report and revise.yaml reinterpret it; the fix is a hashed amendment); P2 the revise was sent without a fresh regime-counters.sh output (typed counts). Measured now: `task=dotfiles-T128-chain-review-scripts-followup-a06 tasks=1 amendments=0 questions=0 results=2 withdrawn=0 revises=1 first_result_head=2db7830bd7fa78e55aa9bdcc46c76201f0a21c3e bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-19T20:15:40Z..2026-10-19T22:46:13Z (2:30) source=live`. Amendment 1 of the a06 text (item 1: a records-only row is realised by the record it names) sha256 e21ef5bef826 -> 7a8b997187a9; TASK amendment to a011 (the copy update is the worker's second and last round); the next chain re-runs on the new head. The chain re-run of 23:4xZ failed at its prepare step (network); the review worktree is clean.
audit:34cc889:1	text-defect
audit:34cc889:2	counter-misread
- 2026-10-20T01:01:45Z: a011 RESULT `round=amendment-1`: head af86233544ea2bf807c198c85d6f07580e0bed9c (fast-forward from 34cc8894, one commit: the task copy only, byte-identical to the amended text 7a8b9971…); the second and last worker round. ACCEPTANCE pending-integration at 2026-10-20T01:06:24Z; chain after #431's (the review worktree is serial).
- 2026-10-20T01:29Z: the chain on af862335 (sweep 0 gaps, ledger 26/19): task-level audit `…-audit-af86233.md` `Verdict: incorrect`, one P2 orchestration: the final-head decision lacked refreshed counters (line 165 said revises=1 while RESULTs 2572, 2592, 2635 make revises=2: the S2 threshold). Measured now (2026-10-20T01:32:44Z) with scripts/regime-counters.sh: `task=dotfiles-T128-chain-review-scripts-followup-a06 tasks=2 amendments=1 questions=0 results=3 withdrawn=0 revises=2 first_result_head=2db7830bd7fa78e55aa9bdcc46c76201f0a21c3e bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-19T20:15:40Z..2026-10-20T01:01:45Z (4:46) source=live`; the unknowns resolved: Bot P1 heads after the RESULT 0 (the Codex Bot is at its usage limit and posted nothing on any head of this PR), audits 3 (b9f562e, 34cc889, af86233). S2 decision: both revises were record corrections of a records-only PR (the superseded line range; the task copy after the hashed text amendment), the lineage has no design to redesign, so the decision is to integrate at af862335 and let the owner a07 carry the lineage (its text already holds the local-review base-ref item); recorded here before the gate.
audit:af86233:1	counter-misread
- 2026-10-20T01:34:26Z: gate passed and PR #434 merged with --match-head-commit at af862335 (the merge glue's fast-forward followed); ACCEPTANCE `status=accepted` to a011 next; the owner a07 text (with the local-review base-ref item) carries the lineage.

## Owned by dotfiles-T128-chain-review-scripts-followup-a07

No advisory rows: the three task-level audits of PR #434 (b9f562e, af86233, 34cc889) found orchestration P2s fixed in this record, and the a05 lineage's advisory row (`## Owned by …-a06` in the a05 record, audit:c646472:1) was realised by a06 itself (#434). The a07 text's Item 1 is therefore vacuous and its Item 2 (local-review.sh takes its base from canonical main as design 5.14 item 8 reads it) carries the task. Written 2026-10-20T04:22Z after a009's identical question on the T129 a06 owner text (C-102).


 succeeded in 153ms:
.orchestration/plans/024-design-quality.md:88:| 〃 | 権限・信頼境界を広げるタスク（excludedCommands、allowMachLookup、hooks で gh 書込を決める、sandbox の allowWrite） | **人** | 下の「権限の変更」に合流 | ユーザー |
.orchestration/plans/024-design-quality.md:89:| ruleset と権限の変更 | 検知: 権限面（`permissions.*`、`excludedCommands`、`allowMachLookup`、`allowWrite`、`allowedDomains`、gh 書込を決める hook、ruleset パラメータ）の diff を機械で抽出し、`D-… scope=permission approved_by=user diff_sha256=<…>` の決定行が無ければ validator と CI が fail | プログラム | `permission-guard.py`（validate CI。diff の sha256 と決定行を照合） | 新 P1-14 |
.orchestration/plans/024-design-quality.md:95:### 5.14 残余（凍結後の計測事実、D-024-29）
.orchestration/plans/024-design-quality.md:103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
.orchestration/plans/024-design-quality.md:107:1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19). The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).
.orchestration/plans/024-design-quality.md:108:2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
.orchestration/plans/024-design-quality.md:109:3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.
.orchestration/plans/024-design-quality.md:113:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
.orchestration/plans/024-design-quality.md:115:9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
.orchestration/plans/024-design-quality.md:117:7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:16:  - {control: ".orchestration/dotfiles-T133-python-pin-a02/**", disposition: "residual: these are untrusted records; the orchestrator compares the dispatched text, final diff, evidence and CI before acceptance."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:18:  - {control: "workflow and interpreter or environment inputs", disposition: "residual: Commands bind the parent environment, interpreter and gh; dotfiles-T133-ci-efficiency-followup-a04 owns the deployed resolver, and CI retains its current interpreter setup."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:19:  - {control: "new or renamed scripts", disposition: "residual: no new or renamed script is authorized; Commands (d) executes only the inherited intended test module."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:21:  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input to review."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:22:  - {control: "in-process effects", disposition: "residual: Commands (d) executes only the intended repository test file, using standard-library imports and TOML data; it does not discover packages or run the supply-chain test's PATH-resolved chezmoi launch."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:23:  - {control: "evidence records under .orchestration/dotfiles-T133-python-pin-a02/", disposition: "residual: records identify Commands sections, operands, exit statuses and output; the orchestrator compares them with the final changeset and CI."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:27:  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: shared credentials and unrestricted same-UID replacement remain possible; host checks reduce accidents and prompt injection, and missing acceptance evidence is detected at the next records PR rather than prevented."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:28:  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: only a sandboxed Codex seat executes this task; it does not deploy or write trusted host inputs, and no unrestricted same-UID boundary is claimed."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:29:  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Commands establish the clean parent before bootstrap and use Commands (b) for validation children; deployed enforcement remains with dotfiles-T133-ci-efficiency-followup-a04."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:30:  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: Commands (c) records the declared executable's realpath; deployed worker-root, symlink and case-alias rejection remains with dotfiles-T133-ci-efficiency-followup-a04."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:31:  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Commands (c) and (d) use the same fixed PY binding without rediscovery; same-UID replacement between probe and execution remains possible."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:32:  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: Commands (f) evidence records full base and head SHAs; no reservation or lock is introduced, and acceptance verifies the final head."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:34:  - {control: "design 5.14 item 7: 検証", disposition: "residual: Commands (d) supplies declaration red/green evidence; the four execution-contract fixture tests remain the responsibility of dotfiles-T133-ci-efficiency-followup-a04."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:35:  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: Commands (e) binds the base and Commands (f) obtains cap evidence from github.com's fixed repository API at full 40-hex SHAs; acceptance verifies the final head against GitHub content."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:36:  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: Commands (c) and (d) use the installed interpreter directly without uv or provisioning; authenticating deployed executable inputs remains with dotfiles-T133-ci-efficiency-followup-a04."}
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:42:  - claim: "Commands (a), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:49:      rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:54:  - claim: "Commands (b), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:59:  - claim: "Commands (c), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:68:  - claim: "Commands (e), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:81:  - claim: "Commands (g), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:96:Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen under D-024-29 and applies by reference under D-024-30; items 0–10 have individual threat rows.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:97:[memory:decision] Declare `python = "3.15.0"` in `home/dot_mise/config.toml` as the exact Python binding for the trusted parent and the resolver owned by `dotfiles-T133-ci-efficiency-followup-a04`.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:100:## Commands
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:102:Definitions occur only here; premises quote the executed probes. Start Commands (parent) from the trusted launcher; execute the lettered sections inside that parent from the verified checkout root. Stop at any failed prerequisite.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:112:rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:122:# (e) Bind gh, print and check the binding, then obtain the canonical base.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:127:# (e') Isolate gh's persistent configuration (hosts.yml api_host can redirect requests): a fresh config dir and the keyring token read once by the bound gh.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:141:Commands (a) is the only home source; (b) removes inherited tool, loader, Python and `GIT_*` configuration. Only the prescribed authenticated gh calls receive the parent's token.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:147:2. Verify the inherited config is `python = "3.15.0"`, immediately preceded by `# Held: the trusted interpreter resolver binds to this exact Python version.` Python stops tracking `latest`; deployment remains an operator action.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:149:4. Preserve the predecessor's Commands (d) assertion-based red on the actual `latest` declaration, exactly one test, with source/head provenance; do not undo the implementation to repeat it. Run Commands (d) green directly; record complete stdout/stderr and exit statuses in `validation.md`, distinguishing inherited red evidence from this execution.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:154:The orchestrator executed the successful read-only Commands (a), (b), (c), (e) binding/version and (g) probes sequentially inside Commands (parent) before this dispatch at 2026-10-20T04:31:20Z; `premises` contains their exact commands and outputs.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:155:Commands (d), (e') and (f)/(f') were not run in that probe: test execution, token read and PR compare belong to the worker/RESULT. The probed checkout's `latest` output is the source baseline, not the continued PR's implementation.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:156:Before worker validation, repeat (a), (b), (c), (e)'s binding/version probe and (g); require version `3.15.0`, its realpath inside the anchored Python install root, and executable non-shim gh. A missing executable or version mismatch produces `python-pin: refused: installed-version-mismatch` and a blocked PONG; `after: []` adds no task dependency.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:160:The worker runs Commands (e) and (e') at dispatch and records its authenticated canonical `<base40>`; record the initial and final `<head40>` verified against GitHub, each exactly 40 ASCII hexadecimal characters.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:161:Run Commands (f) and (f') at RESULT with that dispatch base and final RESULT head; use PR 437, record both full SHAs, resolved operands, exit statuses and complete TSV output, and never substitute mutable local refs.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:162:Sum Commands (f)'s per-file additions plus deletions outside `tests/` and `.orchestration/` for at most **6 changed lines**, and additions under `tests/` for at most **40 added lines**, including the inherited policy adjustment; measure the whole PR through the GitHub compare API.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:163:This whole text must remain at or under **190 lines**. Commands (d) performs no discovery or repository-package imports; require `Ran 1 test` and green. Other tests run in CI; do not run Bats locally. After pushing, verify final-head GitHub Actions and report any failure without changing implementation.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:167:Worker Playbook step 4 applies: every command, including gh and git writes, stays inside the sandbox and allowlist. A denial sends `AGMSG-PONG v1 task_id=dotfiles-T133-python-pin-a02 status=blocked` with the Commands section, resolved operands, failure and crossed boundary; never escalate or bypass through another tool.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:168:All gh operations retain the Commands (e) binding and clean environment and explicitly identify github.com/mryfmo/dotfiles; continue the existing English PR under the Worker Playbook.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:170:Under that directory, write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence; record Commands references, base/head, PR, changed files, caps, red/green provenance, task-copy SHA-256 and `cost:`.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:171:Send `AGMSG-RESULT v1` with all five artifact paths and Commands (f)/(f') evidence; inaccessible main-checkout artifact paths use the same relative paths in the worker worktree.
.orchestration/tasks/dotfiles-T133-python-pin-a02.md:181:C-80 round 1 of this text: 68fd5f2 `Verdict: correct`; the probes in premises were executed read-only by the orchestrator at 2026-10-20T04:31:20Z (Commands (a),(b),(c),(e),(g)); PR #437 continues on task/dotfiles-T133-python-pin-a01 from head e9819d45 (implementation 09c81cc3 unchanged); the a01 copy stays as the predecessor copy
     1	#!/usr/bin/env bash
     2	# @file local-review.sh
     3	# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
     4	# @description
     5	#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
     6	#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` whose `head:` is
     7	#   this head is reused and re-reported; one that records another head is refused. Otherwise the clean review
     8	#   worktree (`$ORCH_REVIEW_WORKTREE`, else `.claude/worktrees/orchestrator-review`), a path with its own `.git`
     9	#   entry, is checked out detached at the head and left there, and the review binary runs in it as `--profile review
    10	#   -s read-only review --base main`. The binary is `$CODEX_BIN`, else codex as `mise which` answers it under `env
    11	#   -i` in the root, else `command -v`; it is resolved before the checkout, and a path under a `shims` directory is
    12	#   refused. When its first line is an env shebang (`#!/usr/bin/env NAME` or `env -S NAME ARG…`), NAME is resolved the
    13	#   same way and runs with the `-S` form's ARG words, then the binary, so no interpreter comes from PATH in the PR
    14	#   worktree. A `-S` string holding a quote, a backslash, a `$` or a word starting with `#` is refused, since env -S
    15	#   splits those differently. When the
    16	#   binary fails, no file is written. Otherwise the file gets the front matter, the unique `-
    17	#   [P0-3]` findings of the transcript's final message, and that message with the worktree prefix stripped; the
    18	#   findings are printed, then `local-review: <n> findings (<file>)`.
    19	# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
    20	# @arg $2 string The PR head commit, a local one, 40 hex characters.
    21	# @arg $3 int PR number.
    22	# @exitcode 0 No finding.
    23	# @exitcode 2 A precondition failed: a malformed task id or head, a review file of another head, the head is not a
    24	#   local commit, the review worktree is not a worktree root or not clean, no review binary outside a shims
    25	#   directory, or an env -S shebang the script does not split.
    26	# @exitcode 3 One or more findings.
    27	# @exitcode 4 The review binary failed; no file is written, and its transcript stays in `$TMPDIR`.
    28	# @example
    29	#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
    30	set -euo pipefail
    31	task=$1 head=$2 pr=$3
    32	# Both name the review file, so a / in either would write outside the validation directory (the audit of b6ce4ff).
    33	[[ $task =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && $head =~ ^[0-9a-f]{40}$ ]] || {
    34	    echo "local-review: usage: local-review.sh <task> <40-hex head> <pr>"
    35	    exit 2
    36	}
    37	R="$(git rev-parse --show-toplevel)"
    38	cd -- "$R"
    39	W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
    40	out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
    41	if [ -s "$out" ]; then
    42	    # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again. The name keeps
    43	    # seven characters of the head, so the recorded head must be this one (PR #357 thread 4270918140).
    44	    [ "$(sed -n 's/^head: //p' "$out" | head -1)" = "$head" ] || {
    45	        echo "local-review: $out records another head; not reused"
    46	        exit 2
    47	    }
    48	    findings=$(/usr/bin/grep -E '^- \[P[0-3]\]' "$out" | sort -u || true)
    49	    n=$(sed -n 's/^findings: //p' "$out" | head -1)
    50	    printf '%s\n' "$findings"
    51	    echo "local-review: $n findings (existing $out)"
    52	    [ "${n:-0}" = 0 ] || exit 3
    53	    exit 0
    54	fi
    55	git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
    56	    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
    57	    exit 2
    58	}
    59	# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
    60	[ -e "$W/.git" ] || {
    61	    echo "local-review: $W is not a worktree root"
    62	    exit 2
    63	}
    64	[ -z "$(git -C "$W" status --porcelain)" ] || {
    65	    echo "local-review: $W is not clean"
    66	    exit 2
    67	}
    68	# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
    69	# binary from the PR head. A mise shim would pick its binary from the PR worktree it runs in, so a name comes from
    70	# mise which under env -i, as orch-gate.sh resolves gh, and a shims path is refused (the audit of b6ce4ff). Sets
    71	# found; a refusal exits here, before the checkout.
    72	resolve() { # <name> <what> [<found by command -v alone>]
    73	    if [ -n "${3:-}" ]; then
    74	        found=$(command -v "$1") || found=
    75	    else
    76	        found=$(env -i PATH="$PATH" HOME="$HOME" mise which "$1" 2> /dev/null || command -v "$1") || found=
    77	    fi
    78	    [ -n "$found" ] || {
    79	        echo "local-review: no $2 $1"
    80	        exit 2
    81	    }
    82	    [[ $found == /* ]] || found=$R/$found
    83	    [[ $found != */shims/* ]] || {
    84	        echo "local-review: the $2 $found is under a shims directory; refused"
    85	        exit 2
    86	    }
    87	}
    88	resolve "${CODEX_BIN:-codex}" "review binary" "${CODEX_BIN:-}"
    89	run=("$found")
    90	# An env shebang would find its interpreter on PATH at exec time, in the PR worktree (the audit of c45f9b5).
    91	first=
    92	IFS= read -r first < "${run[0]}" || true
    93	if [[ $first =~ ^\#![[:space:]]*[^[:space:]]*/env[[:space:]]+(-S[[:space:]]+)?([^[:space:]-][^[:space:]]*)(.*)$ ]]; then
    94	    interpreter=${BASH_REMATCH[2]} split=${BASH_REMATCH[1]} rest=${BASH_REMATCH[3]}
    95	    # env -S splits the rest of the line into the interpreter's own arguments (the local review of 850fc54e).
    96	    words=()
    97	    if [ -n "$split" ]; then
    98	        # env -S quotes, escapes, expands and comments where read -a does not: refuse, never split wrongly (audit:2e3ff49:1).
    99	        if [[ $interpreter$rest == *[\"\'\\\$]* || " $interpreter$rest" =~ [[:space:]]# ]]; then
   100	            echo "local-review: the review binary's env -S shebang holds a quote, an escape, an expansion or a comment the script does not split; refused"
   101	            exit 2
   102	        fi
   103	        read -r -a words <<< "$rest"
   104	    fi
   105	    resolve "$interpreter" "review binary's interpreter"
   106	    run=("$found" ${words[@]+"${words[@]}"} "${run[0]}")
   107	fi
   108	git -C "$W" checkout -q --detach "$head"
   109	base=$(git -C "$W" merge-base main HEAD)
   110	t0=$(date -u +%FT%TZ)
   111	tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
   112	rc=0
   113	(cd "$W" && "${run[@]}" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || rc=$?
   114	if [ "$rc" != 0 ]; then
   115	    # A failed review is no sample: no file, so the next run reviews again (PR #357 thread 4270918132).
   116	    echo "local-review: codex exited $rc; no review file written (transcript $tmp)"
   117	    exit 4
   118	fi
   119	final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp")
   120	# Stripped as a literal, so no character of the worktree path acts as sed syntax (the audit of b6ce4ff); the pattern
   121	# is a quoted variable, which bash 3.2 also reads literally.
   122	prefix="$W/"
   123	final=${final//"$prefix"/}
   124	findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
   125	n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
   126	{
   127	    printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base main (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n"
   128	    printf '%s\n\n' "$findings"
   129	    echo '```text'
   130	    printf '%s\n' "$final" | cut -c1-2000
   131	    echo '```'
   132	} > "$out"
   133	rm -f "$tmp"
   134	printf '%s\n' "$findings"
   135	echo "local-review: $n findings ($out)"
   136	[ "$n" = 0 ] || exit 3

**Managing output length**
exec
/bin/zsh -lc "sed -n '95,138p' .orchestration/plans/024-design-quality.md; cat .orchestration/tasks/dotfiles-T133-python-pin-a02.md" in ~/Workspace/dotfiles
 succeeded in 31ms:
### 5.14 残余（凍結後の計測事実、D-024-29）

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
---
format: 2
task_id: dotfiles-T133-python-pin-a02
reset_of: [dotfiles-T133-python-pin-a01]
kind: code
security: true
allowed_files:
  - home/dot_mise/config.toml
  - tests/unit/test_mise_config.py
  - tests/unit/test_supply_chain_policy.py
  - .orchestration/dotfiles-T133-python-pin-a02/**
after: []
threat_table:
  - {control: "home/dot_mise/config.toml", disposition: "closed: tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version"}
  - {control: "tests/unit/test_mise_config.py", disposition: "closed: tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version"}
  - {control: ".orchestration/dotfiles-T133-python-pin-a02/**", disposition: "residual: these are untrusted records; the orchestrator compares the dispatched text, final diff, evidence and CI before acceptance."}
  - {control: "operator post-merge deployment: make update + mise install", disposition: "residual: the operator deploys after merge and records commands, output and installed version in the acceptance record; the worker never writes the host installation."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: Commands bind the parent environment, interpreter and gh; dotfiles-T133-ci-efficiency-followup-a04 owns the deployed resolver, and CI retains its current interpreter setup."}
  - {control: "new or renamed scripts", disposition: "residual: no new or renamed script is authorized; Commands (d) executes only the inherited intended test module."}
  - {control: "task metadata: kind, allowed_files, threat_table and premises", disposition: "residual: the task-consistency check validates metadata before dispatch and acceptance; whole-file comparison detects changes to the worker copy."}
  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input to review."}
  - {control: "in-process effects", disposition: "residual: Commands (d) executes only the intended repository test file, using standard-library imports and TOML data; it does not discover packages or run the supply-chain test's PATH-resolved chezmoi launch."}
  - {control: "evidence records under .orchestration/dotfiles-T133-python-pin-a02/", disposition: "residual: records identify Commands sections, operands, exit statuses and output; the orchestrator compares them with the final changeset and CI."}
  - {control: "tests/unit/test_supply_chain_policy.py", disposition: "closed: tests/unit/test_supply_chain_policy.py::SupplyChainPolicyTest::test_mise_tools_track_latest_behind_the_cooldown"}
  - {control: "task copy: .orchestration/dotfiles-T133-python-pin-a02/task.md", disposition: "residual: the copy must match the dispatched text byte-for-byte and its dispatch SHA-256; the orchestrator compares both before acceptance."}
  - {control: "predecessor copy: .orchestration/dotfiles-T133-python-pin-a01/task.md", disposition: "residual: unchanged on the branch at its a01 dispatched bytes (SHA-256 30185a5a…); regime-ci checks only the latest copy of a reset_of lineage, and the orchestrator compares the predecessor copy with the a01 dispatch at acceptance."}
  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: shared credentials and unrestricted same-UID replacement remain possible; host checks reduce accidents and prompt injection, and missing acceptance evidence is detected at the next records PR rather than prevented."}
  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: only a sandboxed Codex seat executes this task; it does not deploy or write trusted host inputs, and no unrestricted same-UID boundary is claimed."}
  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Commands establish the clean parent before bootstrap and use Commands (b) for validation children; deployed enforcement remains with dotfiles-T133-ci-efficiency-followup-a04."}
  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: Commands (c) records the declared executable's realpath; deployed worker-root, symlink and case-alias rejection remains with dotfiles-T133-ci-efficiency-followup-a04."}
  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Commands (c) and (d) use the same fixed PY binding without rediscovery; same-UID replacement between probe and execution remains possible."}
  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: Commands (f) evidence records full base and head SHAs; no reservation or lock is introduced, and acceptance verifies the final head."}
  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: the declaration test checks syntax, not executable provenance, deployment or protection against unrestricted same-UID replacement."}
  - {control: "design 5.14 item 7: 検証", disposition: "residual: Commands (d) supplies declaration red/green evidence; the four execution-contract fixture tests remain the responsibility of dotfiles-T133-ci-efficiency-followup-a04."}
  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: Commands (e) binds the base and Commands (f) obtains cap evidence from github.com's fixed repository API at full 40-hex SHAs; acceptance verifies the final head against GitHub content."}
  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: Commands (c) and (d) use the installed interpreter directly without uv or provisioning; authenticating deployed executable inputs remains with dotfiles-T133-ci-efficiency-followup-a04."}
  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: every worker command stays sandboxed; a denial produces a blocked PONG without escalation or a substitute tool."}
  - {control: "orchestrator effect merge", disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"}
  - {control: "orchestrator effect update-branch", disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"}
premises:
  - claim: "Commands (a), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      case "$(/usr/bin/uname -s)" in
        Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
        Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
        *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
      esac
      rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
      case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
    output: |-
      exit=0 home=$HOME
      absolute: yes
  - claim: "Commands (b), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" LANG=C.UTF-8)
    output: |-
      P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME=$HOME LANG=C.UTF-8)
  - claim: "Commands (c), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
      [ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python-pin: refused: missing-executable' >&2; exit 1; }
      "${P[@]}" "$PY" -I -c 'import sys, os; print(os.path.realpath(sys.executable), sys.version.split()[0])'
    output: |-
      exists+executable: yes
      $HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15 3.15.0
      exit=0
  - claim: "Commands (e), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
      printf '%s\n' "$GH"
      case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
      [ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
      "${P[@]}" "$GH" --version
    output: |-
      GH=$HOME/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh
      shim-check: ok
      executable: yes
      gh version 2.102.0 (2026-09-30)
      exit=0
  - claim: "Commands (g), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      "${P[@]}" /usr/bin/grep -n -E 'python.*latest|latest.*python|held = |if name not in held:|self.assertEqual\("latest", version, name\)' home/dot_mise/config.toml tests/unit/test_supply_chain_policy.py scripts/validate-agent-assets.py
    output: |-
      home/dot_mise/config.toml:5:python = "latest"
      tests/unit/test_supply_chain_policy.py:374:        held = {"fd": "fd = ", "npm:pnpm": '"npm:pnpm" = ', "http:bats": '[tools."http:bats"]'}
      tests/unit/test_supply_chain_policy.py:381:            if name not in held:
      tests/unit/test_supply_chain_policy.py:382:                self.assertEqual("latest", version, name)
      exit=0
---

# AGMSG-TASK dotfiles-T133-python-pin-a02 — reset the exact Python declaration

This text is the independent-context reset after INV-6 S2 (tasks=3 amendments=2 questions=1 results=5 revises=4, including round=0 blocked-RESULT closures); the a01 findings history is in `.orchestration/acceptance/dotfiles-T133-python-pin-a01.md`.
Plan 024; continue PR #437 on `task/dotfiles-T133-python-pin-a01` from `e9819d458b93bfba08352832be6b47f95780aeb8`, worker a013 (Codex, worker-h); do not create a branch or PR.
Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen under D-024-29 and applies by reference under D-024-30; items 0–10 have individual threat rows.
[memory:decision] Declare `python = "3.15.0"` in `home/dot_mise/config.toml` as the exact Python binding for the trusted parent and the resolver owned by `dotfiles-T133-ci-efficiency-followup-a04`.
The declaration grammar is the mise `[tools]` key `python` with an exact ASCII-digit `MAJOR.MINOR.PATCH` string, without whitespace, a prefix, `latest` or a range.

## Commands

Definitions occur only here; premises quote the executed probes. Start Commands (parent) from the trusted launcher; execute the lettered sections inside that parent from the verified checkout root. Stop at any failed prerequisite.
```bash
# (parent) Clear inherited inputs before starting the shell; never print the token.
/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /bin/bash --noprofile --norc -p -o pipefail
# (a) Anchor home to the real user's account record.
case "$(/usr/bin/uname -s)" in
  Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
  Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
  *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
esac
rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
# (b) The clean child prefix.
P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" LANG=C.UTF-8)
# (c) Bind and probe the exact interpreter.
PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
[ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python-pin: refused: missing-executable' >&2; exit 1; }
"${P[@]}" "$PY" -I -c 'import sys, os; print(os.path.realpath(sys.executable), sys.version.split()[0])'
# (d) Execute the intended file directly, for both red and green.
"${P[@]}" "$PY" -I tests/unit/test_mise_config.py
# (e) Bind gh, print and check the binding, then obtain the canonical base.
GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
printf '%s\n' "$GH"
case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
[ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
# (e') Isolate gh's persistent configuration (hosts.yml api_host can redirect requests): a fresh config dir and the keyring token read once by the bound gh.
GH_AUTH=$("${P[@]}" "$GH" auth token --hostname github.com); [ -n "$GH_AUTH" ] || { printf '%s\n' 'gh: refused: no-token' >&2; exit 1; }
GHC=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX")
"${P[@]}" "$GH" --version
"${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha
# (f) Substitute the recorded full SHAs before execution; never execute placeholders.
"${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --hostname github.com --paginate --jq '.files[] | "\(.additions)\t\(.deletions)\t\(.filename)"'
# (f') Completeness of (f): refuse a list of 300 files (GitHub's cap) or one that differs from the PR's changedFiles; <pr> is this task's PR, so (f') runs at RESULT, not at dispatch.
n=$("${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --hostname github.com --jq '.files | length'); c=$("${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" pr view <pr> --repo github.com/mryfmo/dotfiles --json changedFiles --jq .changedFiles)
[ "$n" -lt 300 ] && [ "$n" = "$c" ] || { printf '%s\n' "compare: refused: files=$n changedFiles=$c" >&2; exit 1; }
# (g) Read-only declaration and existing-policy probe.
"${P[@]}" /usr/bin/grep -n -E 'python.*latest|latest.*python|held = |if name not in held:|self.assertEqual\("latest", version, name\)' home/dot_mise/config.toml tests/unit/test_supply_chain_policy.py scripts/validate-agent-assets.py
```

Commands (a) is the only home source; (b) removes inherited tool, loader, Python and `GIT_*` configuration. Only the prescribed authenticated gh calls receive the parent's token.
Never substitute an interpreter, enlarge the gh candidate list, invoke a shim, provision a tool or repair a failed command through another invocation. Normalize home prefixes to `$HOME` only in stored output.

## Work

1. Continue the named head with implementation unchanged, including the inherited supply-chain Python exception; add only the new task copy and evidence under `.orchestration/dotfiles-T133-python-pin-a02/`. Preserve `.orchestration/dotfiles-T133-python-pin-a01/` as the predecessor copy.
2. Verify the inherited config is `python = "3.15.0"`, immediately preceded by `# Held: the trusted interpreter resolver binds to this exact Python version.` Python stops tracking `latest`; deployment remains an operator action.
3. Verify the single standard-library test `tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version` reads the real TOML relative to `__file__` using `pathlib` and `tomllib`, assigns the declaration to `value` without stripping, and asserts `re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', value, re.ASCII)`; the same expression rejects `"3.15.0\n"`, `"３.15.0"`, `"latest"` and `"3.15"`. The module ends with `if __name__ == "__main__": unittest.main()`.
4. Preserve the predecessor's Commands (d) assertion-based red on the actual `latest` declaration, exactly one test, with source/head provenance; do not undo the implementation to repeat it. Run Commands (d) green directly; record complete stdout/stderr and exit statuses in `validation.md`, distinguishing inherited red evidence from this execution.
5. No resolver, caller, workflow, dependency, host-installation, knowledge-graph or predecessor-artifact changes are authorized; newly discovered implementation work requires re-tasking.

## Check — prerequisites

The orchestrator executed the successful read-only Commands (a), (b), (c), (e) binding/version and (g) probes sequentially inside Commands (parent) before this dispatch at 2026-10-20T04:31:20Z; `premises` contains their exact commands and outputs.
Commands (d), (e') and (f)/(f') were not run in that probe: test execution, token read and PR compare belong to the worker/RESULT. The probed checkout's `latest` output is the source baseline, not the continued PR's implementation.
Before worker validation, repeat (a), (b), (c), (e)'s binding/version probe and (g); require version `3.15.0`, its realpath inside the anchored Python install root, and executable non-shim gh. A missing executable or version mismatch produces `python-pin: refused: installed-version-mismatch` and a blocked PONG; `after: []` adds no task dependency.

## Check — caps and final head

The worker runs Commands (e) and (e') at dispatch and records its authenticated canonical `<base40>`; record the initial and final `<head40>` verified against GitHub, each exactly 40 ASCII hexadecimal characters.
Run Commands (f) and (f') at RESULT with that dispatch base and final RESULT head; use PR 437, record both full SHAs, resolved operands, exit statuses and complete TSV output, and never substitute mutable local refs.
Sum Commands (f)'s per-file additions plus deletions outside `tests/` and `.orchestration/` for at most **6 changed lines**, and additions under `tests/` for at most **40 added lines**, including the inherited policy adjustment; measure the whole PR through the GitHub compare API.
This whole text must remain at or under **190 lines**. Commands (d) performs no discovery or repository-package imports; require `Ran 1 test` and green. Other tests run in CI; do not run Bats locally. After pushing, verify final-head GitHub Actions and report any failure without changing implementation.

## Completion and boundaries

Worker Playbook step 4 applies: every command, including gh and git writes, stays inside the sandbox and allowlist. A denial sends `AGMSG-PONG v1 task_id=dotfiles-T133-python-pin-a02 status=blocked` with the Commands section, resolved operands, failure and crossed boundary; never escalate or bypass through another tool.
All gh operations retain the Commands (e) binding and clean environment and explicitly identify github.com/mryfmo/dotfiles; continue the existing English PR under the Worker Playbook.
Copy this text byte-identically to `.orchestration/dotfiles-T133-python-pin-a02/task.md`; the orchestrator compares the whole copy and dispatch SHA-256 at acceptance. Keep plan/todo/learn uncommitted and at most one active todo per owner.
Under that directory, write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence; record Commands references, base/head, PR, changed files, caps, red/green provenance, task-copy SHA-256 and `cost:`.
Send `AGMSG-RESULT v1` with all five artifact paths and Commands (f)/(f') evidence; inaccessible main-checkout artifact paths use the same relative paths in the worker worktree.
Pass the repository review gate with local review data; never open a browser review or request human review. The orchestrator performs final-head security review and integration under Orchestrator Playbook step 10; the worker never merges.
After merge, the operator runs `make update` and `mise install`, recording commands, output and installed-version evidence in acceptance; deployment is not a dispatch prerequisite.
Not performed by this authoring context: worker tests, CI or deployment. Executable provenance and unrestricted same-UID replacement remain residual risks.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T05:03Z before send 2 (amendment 1) to a013 (Codex, worker-h): `tests/unit/test_supply_chain_policy.py` added to allowed_files with its closed row (a01 admitted it through its probe rule; the reset omitted it, which regime-ci on head 7f7665b9 reported); task-consistency-check.py OK; SECRET_PATTERN 0; bash -n OK; literal home paths 0; 181 lines (self cap 190); previous_sha256 b9752ec2b910b56079c959b9fa41a4b5a93da0dc6be2eff289486132faa12138
C-80: 68fd5f2 correct (round 1); 906e395 correct (round 2, this amendment); the probes in premises were executed read-only by the orchestrator at 2026-10-20T04:31:20Z
C-80 round 1 of this text: 68fd5f2 `Verdict: correct`; the probes in premises were executed read-only by the orchestrator at 2026-10-20T04:31:20Z (Commands (a),(b),(c),(e),(g)); PR #437 continues on task/dotfiles-T133-python-pin-a01 from head e9819d45 (implementation 09c81cc3 unchanged); the a01 copy stays as the predecessor copy
this text's counters at paste: task=dotfiles-T133-python-pin-a02 tasks=1 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-20T04:49:46Z..none (-) source=live; task SHA256 in the AGMSG-TASK line, computed over these final bytes
```
**Assessing progress and focus**
codex
本文は共有 Git オブジェクトからの読み取りを解消する方針ですが、`closed` とされた項目には、私設ディレクトリの保護や継承した実行体の束縛に依存するものがあります。参照された設計契約と a07 の実装を照合し、その前提が今回のタスクで成立するかを確認しています。
exec
/bin/zsh -lc "sed -n '117,129p' .orchestration/plans/024-design-quality.md; git show a644a7d9:scripts/orchestrator/local-review.sh; git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md" in ~/Workspace/dotfiles
 succeeded in 60ms:
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
#!/usr/bin/env bash
# @file local-review.sh
# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
# @description
#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` whose `head:` is
#   this head is reused and re-reported; one that records another head is refused. Otherwise the clean review
#   worktree (`$ORCH_REVIEW_WORKTREE`, else `.claude/worktrees/orchestrator-review`), a path with its own `.git`
#   entry, is checked out detached at the head and left there, and the review binary runs in it as `--profile review
#   -s read-only review --base <sha>`. The sha is canonical main as `gh api repos/mryfmo/dotfiles/git/ref/heads/main`
#   reports it (design 5.14 item 8), read before the checkout with gh resolved as codex is; the local main and
#   origin/main refs are never the base. Neither git here nor the git codex spawns reads a replace ref or graft:
#   the script exports `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` and passes both to codex as
#   `-c shell_environment_policy.set.…` overrides. The binary is `$CODEX_BIN`, else codex as `mise which` answers it
#   under `env -i` in the root, else `command -v`; it is resolved before the checkout, and a path under a `shims` directory is
#   refused. When its first line is an env shebang (`#!/usr/bin/env NAME` or `env -S NAME ARG…`), NAME is resolved the
#   same way and runs with the `-S` form's ARG words, then the binary, so no interpreter comes from PATH in the PR
#   worktree. A `-S` string holding a quote, a backslash, a `$` or a word starting with `#` is refused, since env -S
#   splits those differently. When the
#   binary fails, no file is written. Otherwise the file gets the front matter, the unique `-
#   [P0-3]` findings of the transcript's final message, and that message with the worktree prefix stripped; the
#   findings are printed, then `local-review: <n> findings (<file>)`.
# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
# @arg $2 string The PR head commit, a local one, 40 hex characters.
# @arg $3 int PR number.
# @exitcode 0 No finding.
# @exitcode 2 A precondition failed: a malformed task id or head, a review file of another head, the head is not a
#   local commit, the review worktree is not a worktree root or not clean, no review binary outside a shims
#   directory, an env -S shebang the script does not split, no gh outside a shims directory, or canonical main
#   unread or not a local commit.
# @exitcode 3 One or more findings.
# @exitcode 4 The review binary failed; no file is written, and its transcript stays in `$TMPDIR`.
# @example
#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
set -euo pipefail
# A seat can write refs/replace/ and info/grafts in the shared .git, and either would change what the base and the
# head hold or which commit is their merge base (design 5.14 item 8), so git and the review binary read neither.
export GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null
task=$1 head=$2 pr=$3
# Both name the review file, so a / in either would write outside the validation directory (the audit of b6ce4ff).
[[ $task =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && $head =~ ^[0-9a-f]{40}$ ]] || {
    echo "local-review: usage: local-review.sh <task> <40-hex head> <pr>"
    exit 2
}
R="$(git rev-parse --show-toplevel)"
cd -- "$R"
W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
if [ -s "$out" ]; then
    # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again. The name keeps
    # seven characters of the head, so the recorded head must be this one (PR #357 thread 4270918140).
    [ "$(sed -n 's/^head: //p' "$out" | head -1)" = "$head" ] || {
        echo "local-review: $out records another head; not reused"
        exit 2
    }
    findings=$(/usr/bin/grep -E '^- \[P[0-3]\]' "$out" | sort -u || true)
    n=$(sed -n 's/^findings: //p' "$out" | head -1)
    printf '%s\n' "$findings"
    echo "local-review: $n findings (existing $out)"
    [ "${n:-0}" = 0 ] || exit 3
    exit 0
fi
git -C "$R" cat-file -e "$head^{commit}" 2> /dev/null || {
    echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
    exit 2
}
# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
[ -e "$W/.git" ] || {
    echo "local-review: $W is not a worktree root"
    exit 2
}
[ -z "$(git -C "$W" status --porcelain)" ] || {
    echo "local-review: $W is not clean"
    exit 2
}
# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
# binary from the PR head. A mise shim would pick its binary from the PR worktree it runs in, so a name comes from
# mise which under env -i, as orch-gate.sh resolves gh, and a shims path is refused (the audit of b6ce4ff). Sets
# found; a refusal exits here, before the checkout.
resolve() { # <name> <what> [<found by command -v alone>]
    if [ -n "${3:-}" ]; then
        found=$(command -v "$1") || found=
    else
        found=$(env -i PATH="$PATH" HOME="$HOME" mise which "$1" 2> /dev/null || command -v "$1") || found=
    fi
    [ -n "$found" ] || {
        echo "local-review: no $2 $1"
        exit 2
    }
    [[ $found == /* ]] || found=$R/$found
    [[ $found != */shims/* ]] || {
        echo "local-review: the $2 $found is under a shims directory; refused"
        exit 2
    }
}
resolve "${CODEX_BIN:-codex}" "review binary" "${CODEX_BIN:-}"
run=("$found")
# An env shebang would find its interpreter on PATH at exec time, in the PR worktree (the audit of c45f9b5).
first=
IFS= read -r first < "${run[0]}" || true
if [[ $first =~ ^\#![[:space:]]*[^[:space:]]*/env[[:space:]]+(-S[[:space:]]+)?([^[:space:]-][^[:space:]]*)(.*)$ ]]; then
    interpreter=${BASH_REMATCH[2]} split=${BASH_REMATCH[1]} rest=${BASH_REMATCH[3]}
    # env -S splits the rest of the line into the interpreter's own arguments (the local review of 850fc54e).
    words=()
    if [ -n "$split" ]; then
        # env -S quotes, escapes, expands and comments where read -a does not: refuse, never split wrongly (audit:2e3ff49:1).
        if [[ $interpreter$rest == *[\"\'\\\$]* || " $interpreter$rest" =~ [[:space:]]# ]]; then
            echo "local-review: the review binary's env -S shebang holds a quote, an escape, an expansion or a comment the script does not split; refused"
            exit 2
        fi
        read -r -a words <<< "$rest"
    fi
    resolve "$interpreter" "review binary's interpreter"
    run=("$found" ${words[@]+"${words[@]}"} "${run[0]}")
fi
# A worker seat can move the local main and origin/main refs in the shared .git, so the base is what GitHub reports.
resolve gh "GitHub CLI"
base=$("$found" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha < /dev/null) || base=
[[ $base =~ ^[0-9a-f]{40}$ ]] || {
    echo "local-review: canonical main could not be read with gh api; no review base"
    exit 2
}
git -C "$R" cat-file -e "$base^{commit}" 2> /dev/null || {
    echo "local-review: canonical main $base is not a local commit (fetch origin main first)"
    exit 2
}
git -C "$W" checkout -q --detach "$head"
t0=$(date -u +%FT%TZ)
tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
rc=0
# Codex's inherit=core policy drops exported variables from the commands it spawns, so its own git gets the two values
# as set overrides (the local review of dbc8b67); TOML strings, as the set table holds.
policy=(-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"' -c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"')
(cd "$W" && "${run[@]}" --profile review -s read-only "${policy[@]}" review --base "$base" < /dev/null > "$tmp" 2>&1) || rc=$?
if [ "$rc" != 0 ]; then
    # A failed review is no sample: no file, so the next run reviews again (PR #357 thread 4270918132).
    echo "local-review: codex exited $rc; no review file written (transcript $tmp)"
    exit 4
fi
final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp")
# Stripped as a literal, so no character of the worktree path acts as sed syntax (the audit of b6ce4ff); the pattern
# is a quoted variable, which bash 3.2 also reads literally.
prefix="$W/"
final=${final//"$prefix"/}
findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
{
    printf -- '---\ntask: %s\nhead: %s\npr: %s\nbase: %s\nstarted: %s\nfinished: %s\nfindings: %s\nengine: codex review --base %s (profile review, read-only)\n---\n\n' "$task" "$head" "$pr" "$base" "$t0" "$(date -u +%FT%TZ)" "$n" "$base"
    printf '%s\n\n' "$findings"
    echo '```text'
    printf '%s\n' "$final" | cut -c1-2000
    echo '```'
} > "$out"
rm -f "$tmp"
printf '%s\n' "$findings"
echo "local-review: $n findings ($out)"
[ "$n" = 0 ] || exit 3
---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a07
kind: code
security: false
allowed_files:
  - scripts/orchestrator/local-advisory.sh
  - scripts/orchestrator/local-review.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/**
after: [dotfiles-T128-chain-review-scripts-followup-a06]
threat_table:
  - control: the PR edits scripts/orchestrator/local-advisory.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_chain_review_scripts.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: scripts/orchestrator/local-review.sh
    disposition: "residual: Item 2 binds the review base to the 40-hex sha of canonical main read from `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com` (design 5.14 item 8), never the local `main` or `origin/main` ref a worker seat can move; one test runs the script with a stub gh and a planted local main ref and shows the base sha comes from the stub"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the owned scripts on fixtures in temporary directories; nothing live changes"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the owned scripts run as today"
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

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a07 — the chain-review-scripts lineage's sixth owner task (advisory P2 of PR #434)

Written 2026-10-20 by the orchestrator seat before the first advisory disposition of PR #434 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md` (plan 020 step 1.2); it is dispatched after PR #434 merges, to a seat the orchestrator names.

## Item 1

Each owned row (any advisory P2 of the local review or the task-level audit of PR #434's final head, and any Bot P2 the orchestrator records under this owner; rows are read from the record at dispatch; a records-only row is realised by the record it names, with no test) gets its fix and, where the row names a test or code, one red-then-green test in `tests/unit/test_chain_review_scripts.py`, named in report.md against the row id. Nothing outside the owned rows; any other file joins `allowed_files` only by an amendment that names the row needing it.

## Item 2

`scripts/orchestrator/local-review.sh` takes its review base from canonical main as design 5.14 item 8 reads it (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`), passes that 40-hex sha to `codex review --base`, and refuses with a named message when the call fails; the local `main` and `origin/main` refs are never the base, because a worker seat can move them in the shared `.git`. One test in `tests/unit/test_chain_review_scripts.py` runs the script with a stub `gh` and a planted local `main` ref and shows the base sha comes from the stub: red before the change, green after. Found by the P1-6 slice-1 text review (`…-text-security-6cbe954.md`, 2026-10-19T21:59Z).

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md` apply as written, with `dotfiles-T128-chain-review-scripts-followup-a07` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T04:29Z before send 2 (amendment 1) to a011 (Claude, worker-d): PR number #402 -> #434 in four places (the lineage template named the predecessor's PR; #402 was a05, whose advisory row a06 realised); `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` written in the a06 record with zero rows, so Item 1 is vacuous and Item 2 carries the task; the message of 04:22:08Z (2710) carried the unamended sha256 ae03f009… by an orchestrator script error and is superseded by this send; task-consistency-check.py OK; SECRET_PATTERN 0; home paths 0; previous_sha256 ae03f0097a5f8b9b58cb6f6a709e4c664569992bd46b38577b2a071166523a75
predecessor dotfiles-T128-chain-review-scripts-followup-a06 merged as PR #434 at 118daafa (in origin/main 60a6fb2b); security: false (no C-80); allowed code files disjoint from every in-flight task (loop-limits, a05-checker, lint a04, P1-15 a03, python-pin)
counters: tasks=0 amendments=0 questions=0 results=0; task SHA256 in the AGMSG-TASK line, computed over these final bytes; the read marker is recorded in the acceptance record
```

**Noticing missing design lines**
exec
/bin/zsh -lc "sed -n '115,116p' .orchestration/plans/024-design-quality.md; nl -ba .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md | head -115; nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md | head -100; git show a644a7d9:tests/unit/test_chain_review_scripts.py | rg -n 'def test_|GIT_|shims|symlink|cache|PATH'" in ~/Workspace/dotfiles
 succeeded in 95ms:
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-trusted-entrypoint-binding-a01
     4	kind: code
     5	security: true
     6	allowed_files: ["home/dot_agents/agent-config.yaml","home/.chezmoitemplates/claude-settings-managed.json","home/dot_claude*/modify_private_settings.json","scripts/generate-agent-configs.py","scripts/validate-agent-assets.py","Makefile","tests/unit/test_claude_managed_settings.py","tests/unit/test_validate_agent_assets.py","scripts/orchestrator/trusted-launch.sh",".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**"]
     7	after: [dotfiles-T133-worker-write-boundary-slice2-a01, dotfiles-T133-ci-efficiency-followup-a04]
     8	rendered_forms: [claude-settings-managed.json, permgate claude]
     9	out_of_scope:
    10	  - {"path":"home/dot_mise/config.toml","reason":"dotfiles-T133-trusted-entrypoint-pins-a01 pins the real declaration before this task is sent; it is read-only here."}
    11	  - {"path":"tests/unit/test_generate_agent_configs.py","reason":"dotfiles-T133-trusted-entrypoint-pins-a01 removes the installed-template legacy literal pin without relaxing synthetic legacy migration cases."}
    12	  - {"path":"tests/unit/test_claude_settings_merge.py","reason":"Existing legacy/custom/idempotence cases remain valid through the modify script's native expansion; run this real module unchanged."}
    13	  - {"path":"tests/unit/test_statusline_tools.py","reason":"Its native renderer must continue to parse the template without deployment installations; run unchanged."}
    14	  - {"path":"tests/unit/test_herdr_agents.py","reason":"The synthetic SessionStart-only template is unaffected; retain its tests."}
    15	  - {"path":"tests/install/common/lifecycle.bats","reason":"Legacy migration fixture data is retained; Bats runs only in GitHub Actions."}
    16	  - {"path":"tests/fixtures/gate-evidence/pr-feedback-right.json","reason":"Historical feedback fixture text is data and is not rewritten."}
    17	  - {"path":"scripts/orchestrator/trusted-interpreter.sh","reason":"The a04 resolver remains read-only for its existing consumers. This re-plan's launcher validates the exact Python declared by its parent-selected manifest; it must not impose the resolver's production-only pin on fixture execution."}
    18	  - {"path":"home/dot_local/bin/common/executable_permgate","reason":"Unchanged dependency-free script, executed through explicit isolated Python rather than its shebang."}
    19	  - {"path":"home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","reason":"Complete guard, delivery and formatter/map descendant binding is outside this split; retain its named deployment residuals."}
    20	threat_table:
    21	  - {"control":"home/dot_agents/agent-config.yaml","disposition":"residual: Declare exact home-relative uv, Python and node identities and compare their production versions with the read-only mise declaration; deterministic rendering supplies the launcher manifest, while protected inputs still share the OS uid."}
    22	  - {"control":"home/.chezmoitemplates/claude-settings-managed.json","disposition":"residual: Render the PermissionRequest exec-form clean prefix with an exact absolute --manifest operand and retain onFailure block; no outer shell starts, but the hook host and first executable's loader environment remain outside launcher validation."}
    23	  - {"control":"home/dot_claude/modify_private_settings.json","disposition":"residual: Classify the legacy form separately and compare the bound command string and ordered args array, including --manifest, exactly with the rendered canonical exec form; preserve raw quoting distinctions, custom hooks and idempotence."}
    24	  - {"control":"home/dot_claude-worker/modify_private_settings.json","disposition":"residual: Apply the same native expansion and exact bound command/args comparison to this consumer without importing live orchestrator settings or adding an event the surface lacks."}
    25	  - {"control":"scripts/generate-agent-configs.py","disposition":"residual: Render exact relative declarations, the launcher manifest data and exec-form command/args without filesystem discovery; ordinary generation and render-check require no installed tools or deployed manifest."}
    26	  - {"control":"scripts/validate-agent-assets.py","disposition":"residual: Validate exact rendered command/args and expose the opt-in effective-settings identity check; checker and yaml-importing children consume the same parent-selected manifest, verified uv/Python and private cache without substituting production pins into fixtures."}
    27	  - {"control":"Makefile","disposition":"residual: Expose concrete manifest preparation, trusted seed and deployment-check commands and give the formatter the pinned node directory; unrelated inherited recipes remain outside this boundary."}
    28	  - {"control":"scripts/orchestrator/trusted-launch.sh","disposition":"residual: Before any declared binary executes, validate the absolute parent-selected manifest and optional fixture root, parse declarations as data, require canonical regular executable paths and compare exact versions; fixture and production inputs use these same checks, while concurrent same-UID replacement remains possible."}
    29	  - {"control":"tests/unit/test_claude_managed_settings.py","disposition":"residual: Exercise exact exec-form rendering, migration, a real fixture-manifest uv/Python/permgate execution and the separate pinned-installation case; fixture execution proves the shared launcher path, not production installation or administrative protection."}
    30	  - {"control":"tests/unit/test_validate_agent_assets.py","disposition":"residual: Exercise manifest containment, shim, symlink, worker-root and version refusals, quote-preserving comparisons and the clean online seed; recording fake uv cases prove argv and refusal behavior only."}
    31	  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**","disposition":"residual: Only task copies, reports, manifest test data and review or validation evidence are authorized; no executable helper or alternative hook may hide under this wildcard."}
    32	  - {"control":"task copy .orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/task.md","disposition":"residual: Compare the complete dispatched file byte-for-byte and verify its SHA-256; preserve predecessor copies and the three-review history."}
    33	  - {"control":"task metadata","disposition":"residual: Verify identity, both after dependencies, the pin prerequisite and exactly ten allowed_files entries before dispatch and acceptance; the modify-script glob has only its two named consumers."}
    34	  - {"control":"metadata separators","disposition":"residual: Parse front matter as data with duplicate keys refused and compare the whole task copy, including both separate task texts and their separators."}
    35	  - {"control":"in-process effects","disposition":"residual: Fixture execution writes temporary data and markers only; the effective-settings check is read-only and the worker performs no live deployment."}
    36	  - {"control":"workflow and interpreter or environment inputs","disposition":"residual: The trusted parent names the manifest and any fixture root under the clean prefix; launcher discovery, environment overrides and production-only fixture gates are forbidden."}
    37	  - {"control":"new or renamed scripts","disposition":"residual: Only the named launcher is added; manifest parsing and exact-path validation stay there, and no second resolver, wrapper executable or artifact-directory runtime helper is introduced."}
    38	  - {"control":"orchestrator effect manifest provisioning","disposition":"residual: The operator materializes deterministic production manifest data under the protected repository root before enabling the changed hook; fixture manifests cannot become effective production bindings."}
    39	  - {"control":"orchestrator effect merge","disposition":"residual: Only the orchestrator merges the reviewed final head after Playbook step 10; shared credentials remain a bypass risk."}
    40	  - {"control":"orchestrator effect update-branch","disposition":"residual: Only the orchestrator updates the branch and refreshes evidence after any head change."}
    41	  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; only the orchestrator may remove a worker and must record any discarded state."}
    42	  - {"control":"design 5.14 item 0 same-UID model","disposition":"residual: These controls limit accidents and prompt injection; shared credentials and unrestricted same-UID processes remain outside prevention."}
    43	  - {"control":"design 5.14 item 1 executable inputs","disposition":"residual: Retain P1-15 protection of policy, user-site locations, settings, rendered manifest and installed tools; executable binding alone does not protect mutable inputs."}
    44	  - {"control":"design 5.14 item 2 trusted parent","disposition":"residual: Exec form starts /usr/bin/env -i with literal argv before the privileged launcher validates entry state and the selected manifest; the hook host and loader starting /usr/bin/env still require host-supplied clean execution or the P1-16 OS user boundary."}
    45	  - {"control":"design 5.14 item 3 resolved boundaries","disposition":"residual: Apply canonical path, regular-file, shim, worker-root and temporary-root checks to the supplied manifest and its declarations; the explicitly named fixture root is a scoped test allowance, not a production setting."}
    46	  - {"control":"design 5.14 item 4 verified executable","disposition":"residual: Execute only the checked declared realpaths without rediscovery and record the selected manifest identity; unrestricted same-UID replacement after validation remains possible."}
    47	  - {"control":"design 5.14 item 5 output identity","disposition":"residual: Record full base/head identities, task-copy hash and manifest hashes; no new reservation or slot lock is introduced."}
    48	  - {"control":"design 5.14 item 6 honest residuals","disposition":"residual: Report declaration checks, real fixture execution, the named pinned-installation skip, CI and operator-host deployment separately; no fixture or skip substitutes for production evidence."}
    49	  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the eight named regressions and scoped hostile-input cases, recording Class::test selectors without claiming system-wide closure or treating an earlier refusal as coverage of a later check."}
    50	  - {"control":"design 5.14 item 8 authenticated evidence","disposition":"residual: A parent-selected manifest supplies executable declarations, not permission or merge approval; integration evidence and live agmsg hardening retain their separate owners."}
    51	  - {"control":"design 5.14 item 9 isolation and cache","disposition":"residual: Bound Python children use -I and isolated offline uv with an absolute parent-supplied private cache; the explicit online seed uses the same manifest, clean parent and verified uv/Python, retaining --no-config --no-project --isolated --with pyyaml --python and -I while omitting only --offline."}
    52	  - {"control":"design 5.14 item 10 sandbox","disposition":"residual: Every worker command stays inside the sandbox; denial produces blocked evidence without escalation or an alternative execution surface."}
    53	premises:
    54	  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/uv/\" | paste -sd '|' -","output":"0|0.12|0.12.17|0.12.18|0.12.19|0.12.20|0.13|0.13.0|0.13.1|global|latest"}
    55	  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/uv/0.13.1/\" | paste -sd '|' -","output":"uv-aarch64-apple-darwin"}
    56	  - {"command":"realpath \"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv"}
    57	  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/python/\" | paste -sd '|' -","output":"3|3.15|3.15.0|global|latest"}
    58	  - {"command":"realpath \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15"}
    59	  - {"command":"head -1 \"$HOME/.local/share/mise/installs/npm-prettier/3.9.10/bin/prettier\"","output":"#!/usr/bin/env node"}
    60	  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/node/\" | paste -sd '|' -","output":"26|26.12|26.12.0|global|latest"}
    61	  - {"command":"realpath \"$HOME/.local/share/mise/installs/node/26.12.0/bin/node\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/node/26.12.0/bin/node"}
    62	  - {"command":"grep -nE '^(uv|python|node) = ' home/dot_mise/config.toml | paste -sd '|' -","output":"3:node = \"latest\"|5:python = \"latest\"|17:uv = \"latest\""}
    63	  - {"command":"ls -1 .mise.toml mise.toml 2>&1 | paste -sd '|' -","output":"ls: .mise.toml: No such file or directory|mise.toml"}
    64	  - {"command":"cat mise.toml | paste -sd '|' -","output":"[tools]"}
    65	  - {"command":"grep -n '\"command\": \".*permgate claude\"' home/.chezmoitemplates/claude-settings-managed.json","output":"207:            \"command\": \"~/.local/bin/common/permgate claude\","}
    66	  - {"command":"head -1 home/dot_local/bin/common/executable_permgate","output":"#!/usr/bin/env -S uv run --no-cache --script"}
    67	  - {"command":"grep -cE '^# ///|^# dependencies[[:space:]]*=' home/dot_local/bin/common/executable_permgate","output":"0"}
    68	  - {"command":"sed -n '179,182p' Makefile | paste -sd '|' -","output":"format:| shfmt --indent 4 --space-redirects --diff .| git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check| git ls-files -z '*.md' | xargs -0 prettier --check"}
    69	  - {"command":"grep -cE '(^|[[:space:]])(export[[:space:]]+)?PATH[[:space:]:?+]*=' Makefile","output":"0"}
    70	  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_agents/agent-config.yaml home/.chezmoitemplates/claude-settings-managed.json home/dot_claude/modify_private_settings.json home/dot_claude-worker/modify_private_settings.json scripts/generate-agent-configs.py scripts/validate-agent-assets.py Makefile tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":"Makefile|home/.chezmoitemplates/claude-settings-managed.json|home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/generate-agent-configs.py|scripts/validate-agent-assets.py|tests/unit/test_validate_agent_assets.py"}
    71	  - {"command":"grep -nE '^  - (home/dot_claude-worker/modify_private_settings.json|tests/unit/test_claude_managed_settings.py)$' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | paste -sd '|' -","output":"12:  - home/dot_claude-worker/modify_private_settings.json|27:  - tests/unit/test_claude_managed_settings.py"}
    72	  - {"command":"grep -nE '^def (render_claude_settings|render_template_text|validate_claude_settings|validate_model_profile_assets|validate_generated_agent_configs|main|render_managed_template|is_managed_permission_hook)\\(' scripts/generate-agent-configs.py scripts/validate-agent-assets.py home/dot_claude/modify_private_settings.json | paste -sd '|' -","output":"scripts/generate-agent-configs.py:400:def render_claude_settings(manifest: dict[str, Any]) -> str:|scripts/generate-agent-configs.py:1401:def main() -> None:|scripts/validate-agent-assets.py:88:def render_template_text(path: Path, os_name: str = \"darwin\") -> str:|scripts/validate-agent-assets.py:374:def validate_claude_settings(manifest: dict[str, Any], os_name: str = \"darwin\") -> None:|scripts/validate-agent-assets.py:1187:def validate_model_profile_assets(manifest: dict[str, Any]) -> None:|scripts/validate-agent-assets.py:1294:def validate_generated_agent_configs() -> None:|scripts/validate-agent-assets.py:1660:def main() -> None:|home/dot_claude/modify_private_settings.json:48:def render_managed_template(text: str) -> str:|home/dot_claude/modify_private_settings.json:68:def is_managed_permission_hook(hook: Any) -> bool:|home/dot_claude/modify_private_settings.json:196:def main() -> int:"}
    73	  - {"command":"sed -n '400,487p' scripts/generate-agent-configs.py | wc -l | xargs","output":"88"}
    74	  - {"command":"sed -n '88,100p;374,406p;1187,1265p;1294,1304p;1660,1685p' scripts/validate-agent-assets.py | wc -l | xargs","output":"162"}
    75	  - {"command":"sed -n '48,55p;68,79p' home/dot_claude/modify_private_settings.json | wc -l | xargs","output":"20"}
    76	  - {"command":"wc -l .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | xargs","output":"63 .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json 95 .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py 1781 tests/unit/test_validate_agent_assets.py 79 home/dot_mise/config.toml 2350 tests/unit/test_generate_agent_configs.py 4368 total"}
    77	  - {"command":"ls tests/unit/test_task_consistency_c11_c15.py 2>&1 | paste -sd '|' -","output":"ls: tests/unit/test_task_consistency_c11_c15.py: No such file or directory"}
    78	  - {"command":"sed -n '63,66p' .claude/worktrees/worker-g/tests/unit/test_task_consistency_c11_c15.py | paste -sd '|' -","output":"CASES = {|    \"C11\": (|        '\"closed: tests/unit/test_tool.py::test_tool_prints_findings\"',|        '\"closed: tests/unit/test_tool.py::two words\"',"}
    79	  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\" --version","output":"uv 0.13.1 (62faed335 2026-10-13 aarch64-apple-darwin)"}
    80	  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B --version","output":"Python 3.15.0"}
    81	  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/node/26.12.0/bin/node\" --version","output":"v26.12.0"}
    82	  - {"command":"rg -l 'claude-settings-managed|is_managed_permission_hook|permgate claude' home scripts tests .github Makefile --glob '!*.md' --glob '!*.lock' | sort | paste -sd '|' -","output":"home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/validate-agent-assets.py|tests/fixtures/gate-evidence/pr-feedback-right.json|tests/install/common/lifecycle.bats|tests/unit/test_claude_settings_merge.py|tests/unit/test_generate_agent_configs.py|tests/unit/test_herdr_agents.py|tests/unit/test_statusline_tools.py|tests/unit/test_validate_agent_assets.py"}
    83	  - {"command":"grep -nE '^class (ClaudeManagedSettingsTest|ValidateAgentAssetsTest)' .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":".claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py:12:class ClaudeManagedSettingsTest(unittest.TestCase):|tests/unit/test_validate_agent_assets.py:84:class ValidateAgentAssetsTest(unittest.TestCase):"}
    84	  - {"command":"sed -n '117p' .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md | cut -d . -f 1-2","output":"On success print exactly one absolute interpreter realpath and exit 0. On every refusal print exactly one line `trusted-interpreter: refused: <code>` to stderr, print no interpreter on stdout, and exit 2"}
    85	  - {"command":"printf '%s\\n' \"$PATH\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/shims:$HOME/.local/bin:$HOME/.local/bin/common:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$HOME/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:$HOME/.local/share/mise/installs/node/lts/bin:/usr/bin:/bin:/usr/sbin:/sbin"}
    86	  - {"command":"grep -nE '^    import yaml|PyYAML is required' scripts/validate-agent-assets.py | paste -sd '|' -","output":"22:    import yaml|81:        fail(\"PyYAML is required\")|175:        fail(\"PyYAML is required to validate skill frontmatter\")"}
    87	  - {"command":"sed -n '340,346p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | paste -sd '|' -","output":"   Its managed PermissionRequest command remains exactly:||   ```text|   ~/.local/bin/common/permgate claude|   ```||   Do not add an env prefix, guard selector, absolute uv/Python invocation or new command-form validator for this hook. Keep its existing timeout and add the task's common `onFailure: \"block\"` entry policy. The unchanged command's shebang, interpreter discovery and inherited environment are explicit residuals owned by the binding task."}
    88	  - {"command":"head -1 .claude/worktrees/worker-e/home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","output":"#!/bin/bash"}
    89	  - {"command":"test ! -e scripts/orchestrator/trusted-launch.sh","output":"","exit_status":0}
    90	  - {"command":"python3 -I -B -c 'from pathlib import Path; roots=(Path(\"home\"),Path(\".claude/worktrees/worker-e/home\")); print(\"|\".join(str(p) for root in roots for p in sorted(root.glob(\"dot_claude*/modify_private_settings.json\"))))'","output":"home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json"}
    91	  - {"command":"python3 -I -B -c 'import os,pwd,stat; from pathlib import Path; h=Path(pwd.getpwuid(os.getuid()).pw_dir); u=h/\".local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\"; r=u.resolve(strict=True); print(\"home_matches_passwd=\"+str(Path.home()==h)); print(\"uv_regular=\"+str(stat.S_ISREG(u.lstat().st_mode))); print(\"uv_symlink=\"+str(u.is_symlink())); print(\"uv_under_passwd_install_root=\"+str(r.is_relative_to(h/\".local/share/mise/installs\"))); print(\"uv_declared_equals_realpath=\"+str(u==r)); print(\"trusted_launch_exists=\"+str(Path(\"scripts/orchestrator/trusted-launch.sh\").exists()))'","output":"home_matches_passwd=True\nuv_regular=True\nuv_symlink=False\nuv_under_passwd_install_root=True\nuv_declared_equals_realpath=True\ntrusted_launch_exists=False"}
    92	  - {"command":"rg -n '^    import yaml|PyYAML is required' scripts/generate-agent-configs.py | paste -sd '|' -","output":"14:    import yaml|34:        fail(\"PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py\")"}
    93	  - {"command":"sed -n '1294,1298p' scripts/validate-agent-assets.py | paste -sd '|' -","output":"def validate_generated_agent_configs() -> None:|    result = subprocess.run(|        [sys.executable, str(ROOT / \"scripts/generate-agent-configs.py\"), \"--check\"],|        cwd=ROOT,|        text=True,"}
    94	  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B scripts/generate-agent-configs.py --check","output":"ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py","exit_status":1}
    95	  - {"command":"claude --version","output":"2.1.300 (Claude Code)","exit_status":0}
    96	  - {"command":"python3 -I -B -c 'from pathlib import Path; b=(Path.home()/\".local/share/mise/installs/npm-anthropic-ai-claude-code/latest/bin/claude\").read_bytes(); s=b\"Command hooks require `command`. For exec form (no shell)\"; i=b.find(s); print(b[i:b.index(b\"\\0\",i)].decode() if i>=0 else \"missing exec-form help\")'","output":"Command hooks require `command`. For exec form (no shell), set `command` to the executable and `args` to its arguments: {\"type\": \"command\", \"command\": \"echo\", \"args\": [\"hi\"]}. For shell form, set `command` to the full shell string: {\"type\": \"command\", \"command\": \"echo hi\"}.","exit_status":0}
    97	  - {"command":"web.open https://code.claude.com/docs/en/hooks#exec-form-and-shell-form","output":"Command hook args present selects direct executable spawn without a shell; args omitted selects shell form (sh -c on macOS/Linux). command is the executable path and args is its argument vector. Documented path placeholders include ${CLAUDE_PROJECT_DIR} and are substituted as plain strings."}
    98	---
    99	
   100	# AGMSG-TASK dotfiles-T133-trusted-entrypoint-binding-a01 — bind trusted entrypoints to a parent-selected manifest
   101	
   102	Worker: a Codex seat (worktree named at dispatch)
   103	
   104	Use the security profile for this Claude-boundary change. D-024-26 split this family from P1-15. Read the last 60 lines of .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md and .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-{f810c30,772cde0,e5c055e,5204254}.md.last.md: shebang discovery, Python startup injection, the checker's own execution, shim discovery, the real uv layout and Prettier's node must be handled together.
   105	
   106	Read the complete binding acceptance record and these three pre-dispatch reviews:
   107	
   108	- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-faae5f4.md.last.md
   109	- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-8f5ac8d.md.last.md
   110	- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-e3ae7cd.md.last.md
   111	
   112	This is the C-92 fixture-vs-binding re-plan recorded by the acceptance record's `re-plan:` line, not a fourth repair under the predecessor design. Preserve the earlier findings and their dispositions. The new design retains round 3's exec-form hook, quote-preserving comparisons and bound online seed, and replaces its contradictory positive-fixture requirement.
   113	
   114	The launcher validates the manifest its trusted parent explicitly names. Production passes the rendered production manifest; tests pass a fixture manifest declaring the runner's real tools. Both use the same manifest parser, exact-path checks, containment checks, version comparisons and command construction. A fixture cannot bypass a check, and a production-only resolver or hard-coded installation gate must not run before the fixture's declared interpreter.
   115	
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-worker-write-boundary-a04
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - home/dot_agents/agent-config.yaml
     8	  - home/.chezmoitemplates/claude-settings-managed.json
     9	  - home/.chezmoitemplates/claude-worker-settings.json
    10	  - home/.chezmoitemplates/claude-managed-settings.json
    11	  - home/dot_claude/modify_private_settings.json
    12	  - home/dot_claude-worker/modify_private_settings.json
    13	  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    14	  - .claude/settings.json
    15	  - scripts/generate-agent-configs.py
    16	  - scripts/validate-agent-assets.py
    17	  - Makefile
    18	  - home/dot_local/bin/common/executable_herdr-agents
    19	  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
    20	  - .gitignore
    21	  - tests/unit/test_generate_agent_configs.py
    22	  - tests/unit/test_validate_agent_assets.py
    23	  - tests/unit/test_claude_settings_merge.py
    24	  - tests/unit/test_herdr_agents.py
    25	  - tests/unit/test_agmsg_orchestration_docs.py
    26	  - tests/unit/test_claude_worker_settings.py
    27	  - tests/unit/test_claude_managed_settings.py
    28	  - .orchestration/dotfiles-T133-worker-write-boundary-a04/**
    29	after: []
    30	reset_of: [dotfiles-T133-worker-write-boundary-a03]
    31	retained_predecessor_directories:
    32	  - .orchestration/dotfiles-T133-worker-write-boundary-a03/
    33	threat_table:
    34	  - control: home/dot_agents/agent-config.yaml
    35	    disposition: "residual: the manifest declares the static protected inputs and closed worker-start schema; render tests check their correspondence without establishing same-UID isolation or complete executable binding."
    36	  - control: home/.chezmoitemplates/claude-settings-managed.json
    37	    disposition: "residual: the orchestrator baseline retains guarded non-PermissionRequest hooks and the unchanged legacy PermissionRequest command; its execution binding belongs to dotfiles-T133-trusted-entrypoint-binding-a01."
    38	  - control: home/.chezmoitemplates/claude-worker-settings.json
    39	    disposition: "residual: dedicated policy retains narrow write grants, static denies, canonical delivery, MCP approval disables and explicit plugin disables; higher-scope inputs also undergo independent screening."
    40	  - control: home/.chezmoitemplates/claude-managed-settings.json
    41	    disposition: "residual: the administrative template declares sandbox requirements and the exact shared exceptions; content fixtures do not establish operator installation or live enforcement."
    42	  - control: home/dot_claude/modify_private_settings.json
    43	    disposition: "residual: exact managed-hook classification replaces owned legacy forms while preserving custom hooks and ordering; repeated merge fixtures check idempotence without proving descendant executable identity."
    44	  - control: home/dot_claude-worker/modify_private_settings.json
    45	    disposition: "residual: one source-aware closed-schema policy checks existing and prepared inputs before mutation; fixtures establish refusal at startup while later reloads and same-UID replacement remain possible."
    46	  - control: home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    47	    disposition: "residual: fixed operations and canonical launch identity suppress worker project payloads; complete interpreter, formatter and descendant binding remains with dotfiles-T133-trusted-entrypoint-binding-a01."
    48	  - control: .claude/settings.json
    49	    disposition: "residual: every tracked command retains the clean prefix, installed guard, fixed operation and failure policy; portable render fixtures do not establish runtime timeout enforcement."
    50	  - control: scripts/generate-agent-configs.py
    51	    disposition: "residual: deterministic generation publishes manifest-owned policy without learning accepted keys or executable forms from candidate configuration; generation remains independent of deployment tool availability."
    52	  - control: scripts/validate-agent-assets.py
    53	    disposition: "residual: existing schema, exclusion, hook and asset checks remain, including legacy PermissionRequest recognition; no new bound-PermissionRequest or deployment checker is introduced."
    54	  - control: Makefile
    55	    disposition: "residual: staging prints privileged parent creation and file installation without executing either, and update-tree reconciles Claude settings after the Herdr installer; temporary fixtures check both sequences."
    56	  - control: home/dot_local/bin/common/executable_herdr-agents
    57	    disposition: "residual: all worker-start routes validate the repository anchor and all Claude routes run the same preflight before trust or mutation; no live seat or atomic consumption guarantee is claimed."
    58	  - control: home/dot_agents/skills/agmsg-orchestration/SKILL.md
    59	    disposition: "residual: the Worker Playbook has one sandbox-only command rule and no worker exemptions; documentation fixtures distinguish the retained orchestrator operations."
    60	  - control: .gitignore
    61	    disposition: "residual: .uv-cache remains ignored without removing either worklog/cache deny pattern; the temporary-checkout ignore fixture checks accidental-publication protection."
    62	  - control: tests/unit/test_generate_agent_configs.py
    63	    disposition: "residual: both-platform fixtures check separate policies, static inventory, closed-schema rendering and canonical commands without claiming live enforcement."
    64	  - control: tests/unit/test_validate_agent_assets.py
    65	    disposition: "residual: retained fixtures cover exact ordered exclusions, malformed variants and legacy permission-hook composition; formatting remains a CI concern."
    66	  - control: tests/unit/test_claude_settings_merge.py
    67	    disposition: "residual: migration and fake-update fixtures check custom-hook preservation, guarded replacement, installer ordering and idempotence without running a live update."
    68	  - control: tests/unit/test_herdr_agents.py
    69	    disposition: "residual: temporary roots and fake processes exercise source coverage, input refusals, launch routes and cache delivery without starting workers, plugins or authentication helpers."
    70	  - control: tests/unit/test_agmsg_orchestration_docs.py
    71	    disposition: "residual: fixtures read this task's dispatched copy and test the exact sandbox sentence and fixed-host ledger templates without introducing a ledger consumer."
    72	  - control: tests/unit/test_claude_worker_settings.py
    73	    disposition: "residual: render, merge, deny and guard fixtures verify configured policy and unchanged protected bytes without executing a bound PermissionRequest hook."
    74	  - control: tests/unit/test_claude_managed_settings.py
    75	    disposition: "residual: administrative-content and printed-command fixtures use temporary destinations and sudo markers; actual administrative installation remains an operator step."
    76	  - control: .orchestration/dotfiles-T133-worker-write-boundary-a04/**
    77	    disposition: "residual: evidence separates inherited observations, new regressions and final-head results, and records pending deployment without credentials or literal operator home paths."
    78	  - control: <absolute-home>/.claude-worker/settings.json
    79	    disposition: "residual: S01 is checked before regeneration under the closed settings schema, including every environment entry; a later same-UID replacement remains outside the startup guarantee."
    80	  - control: <worktree>/.claude/settings.json
    81	    disposition: "residual: S02 includes old tracked settings and is checked without rewriting it; a refusal requires an authorized guarded commit rather than launcher normalization."
    82	  - control: <worktree>/.claude/settings.local.json
    83	    disposition: "residual: S03 is inspected before exact legacy migration, so migration cannot conceal helpers, unknown keys or sandbox extensions."
    84	  - control: <validated-anchor>/.claude/settings.local.json
    85	    disposition: "residual: S04 is the validated repository's main-local source, independently screened because linked workers consume it; other repository roots refuse before preparation."
    86	  - control: /Library/Application Support/ClaudeCode/managed-settings.json
    87	    disposition: "residual: the Darwin S05 file is screened with the administrative schema through a temporary managed-root fixture; the worker never mutates the system file."
    88	  - control: /etc/claude-code/managed-settings.json
    89	    disposition: "residual: the Linux S05 file receives the same administrative schema and source-specific exceptions without claiming live installation."
    90	  - control: <managed-root>/managed-settings.d/<name>.json
    91	    disposition: "residual: S06 checks each drop-in independently before merging, admitting only canonical administrative fragments and refusing unknown keys or broadened lists."
    92	  - control: <absolute-home>/.claude-worker/remote-settings.json
    93	    disposition: "residual: S07 checks an existing cache independently; additional managed delivery that cannot be enumerated before launch produces a named refusal."
    94	  - control: <worktree>/.mcp.json
    95	    disposition: "residual: S08 admits only absent or empty server definitions regardless of trust or approval state, including ignored and untracked files."
    96	  - control: <validated-anchor>/.mcp.json
    97	    disposition: "residual: S09 is checked independently of nearer worktree definitions, so an absent or empty worktree file cannot conceal an inherited server."
    98	  - control: <loaded-ancestor>/.mcp.json
    99	    disposition: "residual: S10 checks each applicable ancestor file independently without using Git tracking or precedence as an exclusion."
   100	  - control: <absolute-home>/.claude-worker/.claude.json
5:working directory, the HEAD there, PATH and its stdin to `<calls>/<name>.log`, prints `<calls>/transcript` and exits with
18:GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
22:    '"$(pwd -P)" "$(git rev-parse HEAD)" "$PATH" "$(cat)"; }} >> "$CALLS/{name}.log"\n'
26:    '-c shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1" '
27:    '-c shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'
45:        self.env = {**os.environ, **GIT_ENV, "CALLS": str(self.calls), "TMPDIR": str(self.temp)}
53:            env={**os.environ, **GIT_ENV},
71:        """A mise stub first on PATH; it runs under env -i, so it carries the calls directory itself."""
79:        """A gh stub first on PATH: it logs its argv, prints answer as `gh api --jq .object.sha` would, and exits status."""
88:        """A clean review worktree at main, a head commit made in it, codex stubbed and mise failing on PATH."""
100:        path = f"{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
101:        return review, head, {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
122:    def test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file(self):
136:        path = f"./bin{os.pathsep}{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
137:        env = {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
195:    def test_local_review_writes_no_file_when_the_review_binary_fails(self):
210:    def test_local_review_reuses_only_a_file_that_records_this_head(self):
227:    def test_local_review_resolves_codex_through_mise_and_refuses_a_shim(self):
233:        self.mise(f'printf "%s\\n" "{self.temp}/mise/shims/$2"\n')
235:            "is under a shims directory; refused", self.run_tool("local-review.sh", "t-a", head, 9, code=2, env=env)
246:    def test_local_review_takes_its_base_from_canonical_main_never_a_local_ref(self):
296:    def test_local_review_passes_no_replace_and_no_graft_to_the_commands_codex_spawns(self):
306:            'env -i PATH=/usr/bin:/bin "${kept[@]}" /usr/bin/env | /usr/bin/grep "^GIT_" | sort >> "$CALLS/spawned.log"\n'
313:        self.assertEqual(["GIT_GRAFT_FILE=/dev/null", "GIT_NO_REPLACE_OBJECTS=1"], self.log("spawned").splitlines())
315:    def test_local_review_resolves_the_review_binary_before_the_checkout(self):
328:    def test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory(self):
345:    def test_local_review_strips_a_worktree_path_holding_sed_syntax_literally(self):
354:    def test_local_review_pins_the_review_binary_interpreter(self):
356:        # answers in the root, never one PATH finds in the PR worktree.
369:            # mise knows the installed tools only, so gh falls back to the stub on PATH.
380:        with self.subTest("an interpreter under a shims directory is refused before the checkout"):
381:            self.mise(f'[[ $2 == codex ]] && printf "%s\\n" "{binary}" || printf "%s\\n" "{self.temp}/mise/shims/$2"\n')
384:            self.assertIn("is under a shims directory; refused", stdout)
389:    def test_local_review_keeps_env_S_shebang_arguments(self):
410:    def test_local_review_refuses_a_quoted_env_S_shebang(self):
438:    def test_local_advisory_records_p2_rows_and_stops_on_p0_p1(self):
488:    def test_local_advisory_refuses_a_malformed_owner_id(self):
497:    def test_local_advisory_matches_the_owner_heading_literally(self):
511:    def test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file(self):
526:    def test_local_advisory_classes_a_repeat_by_the_earlier_row(self):
565:    def test_local_advisory_matches_an_earlier_review_id_literally(self):
585:    def test_local_advisory_reads_the_whole_suffix_after_the_task_prefix(self):
608:    def test_sandbox_scan_prints_the_unsandboxed_mutation_calls(self):

**Reviewing defect fixes and contract issues**
exec
/bin/zsh -lc "rg -n 'local-review|PATH|GIT_|excludedCommands|gh' scripts/orchestrator/chain-integrate.sh .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md | head -65; cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md | head -65; rg -n 'local-review|chain-integrate|git|gh|codex' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md" in ~/Workspace/dotfiles
 succeeded in 76ms:
scripts/orchestrator/chain-integrate.sh:34:log='' lines=() && export NO_COLOR=1 && unset CLICOLOR_FORCE GH_FORCE_TTY # no ANSI from gh, as pr-feedback.py's gh_env
scripts/orchestrator/chain-integrate.sh:64:# Resolved before any fetch or checkout and run by absolute path, as local-review.sh resolves codex: a mise shim
scripts/orchestrator/chain-integrate.sh:66:pick() { env -i PATH="${PATH}" HOME="${HOME}" mise which "$1" 2> /dev/null || command -v "$1" || true; }
scripts/orchestrator/chain-integrate.sh:67:gh=$(pick gh) git=$(pick git) uv=$(pick uv) shasum=$(pick shasum) date=$(pick date)
scripts/orchestrator/chain-integrate.sh:68:for found in "${gh}" "${git}" "${uv}" "${shasum}" "${date}"; do
scripts/orchestrator/chain-integrate.sh:75:for s in scripts/orchestrator/{sandbox-scan.sh,local-review.sh,local-advisory.sh,fill_sweep.py,acceptance-front-matter.py,orch-audit.sh} scripts/pr-feedback.py; do
scripts/orchestrator/chain-integrate.sh:88:pre "${gh}" pr view "${pr}" --json isDraft --jq .isDraft
scripts/orchestrator/chain-integrate.sh:102:    step fetch 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid
scripts/orchestrator/chain-integrate.sh:110:        step checks any "${gh}" pr checks "${pr}" --required --watch
scripts/orchestrator/chain-integrate.sh:115:        while step bot 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/reviews" --paginate --jq "${q}"; do
scripts/orchestrator/chain-integrate.sh:127:    step base 0 "${gh}" pr update-branch "${pr}"
scripts/orchestrator/chain-integrate.sh:129:    while step base 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid && [ "${out}" = "${head}" ]; do
scripts/orchestrator/chain-integrate.sh:133:    fresh  # a moved base may have left the main checkout's main behind, which local-review.sh diffs against
scripts/orchestrator/chain-integrate.sh:143:step local-review 0,3 "${main}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
scripts/orchestrator/chain-integrate.sh:145:[[ ! ${out} =~ local-review:\ ([0-9]+)\ findings ]] || findings=${BASH_REMATCH[1]}
scripts/orchestrator/chain-integrate.sh:153:step fill-sweep 0 "${gh}" api user --jq .login
scripts/orchestrator/chain-integrate.sh:156:step fill-sweep 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/comments" --paginate --jq '.[]'
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md:49:- 2026-10-20T03:43:14Z: amendment 1 written whole by the review profile (`p115-a03-r2-prompt.md` -> `redesign/p115-a03-r2.md`) and installed: `CLAUDE_ENV_FILE` named as the only admitted variable selecting a file whose contents execute (read-only probe of the documented environment variables); preflight accepts its file only when absent, empty or byte-identical to the launcher-generated contents of this start, inspected without sourcing; one closed row with the selector `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` and one planted-content regression (red on c0f50fa1, green after). 35 changed lines against round 1; 622 lines; pre-send.sh: checker OK, SECRET_PATTERN 0 matches, no literal home path; sha256 f7af699… -> 9bd6198f1abec37ac618757c140b21fa799b987dbf4317c6a66ac16a9cefde24. C-80 round 2 running (budget 2 of 3).
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md:62:- 2026-10-20T04:49Z: C-80 round 4 (`…-text-security-be969e3.md`, the first after re-plan 3) `Verdict: incorrect`, one P1 (line 425): the design screens `<managed-root>/skills` and excludes `<managed-root>/.claude/skills`, which the pinned loader 2.1.300 consumes (documented loading locations), so managed skill content escapes preflight and fixture 502 tests the wrong directory. Disposition: amendment 4 after the orchestrator's read-only probe of the loader's skill-directory strings (pasted in the prompt); maps to the row below. Rounds after re-plan 3: 1 of 3 (C-92).
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md:64:- 2026-10-20T04:58Z: amendment 4 written whole by the review profile (`p115-a03-r5-prompt.md` -> `redesign/p115-a03-r5.md`) and installed: the enterprise skills root is `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), the admitted skills roots are the documented six, fixture 502 plants Markdown and bundled plugin payloads there through the temporary managed-root fixture, the row's premise quotes the documented table and the loader probe (C-87); 22 changed lines against amendment 3; 654 lines; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 be969e32… -> 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b. C-80 round 5 running (the second after re-plan 3).
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md:69:- 2026-10-21T01:50Z: R1-1 (re-plan v2, J2 default): the a04 reset text (653 lines, undispatched, C-80 round 1 P2) is withdrawn as a single text and replaced by four slices `dotfiles-T133-worker-write-boundary-slice{1,2,3,4}-a01` per the review-profile allocation draft `.agents/worklog/orchestrator-glue/a04-allocation-r1.md` (22 paths, 90 threat rows and the retained findings assigned; table saved as `.orchestration/plans/024-allocation.tsv`). Decisions taken by default: slice ids S1-S4 with serial shared-file scopes; slice 1 is the sole reset_of a03 carrier (allowed_files 8, after []); provisional caps 650 source / 650 tests for slice 1, reconciled against a04's 1591/2528 at RESULT, no silent increase; owner `dotfiles-T133-trusted-entrypoint-descendants-followup-a01` created now (J1) and named by the slices for guard/delivery/formatter/map binding; four slice namespaces, predecessor evidence retained unchanged, no purported dispatched a04 copy; the foreign-root refusal identifier uses slice 2's dispatched id; dependency edges: network -> S1, launcher consumers -> S2, settings prerequisites -> S3, audit/verdict documentation -> S4 (independent pins/resolver/a05 edges kept). Slice 1 text authoring starts through author-loop.sh (brief `brief-wwb-slice1.md`, C-80 <= 2).
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
session id: 01a15cc3-d29c-7a42-833a-fb693a59caf3
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
指定のタスク本文と参照先の記録を読み、判断に使った対象と実際に実行される対象が一致する設計かを確認します。読み取り専用で進め、agmsg-orchestration と Ponytail のレビュー手順を参照します。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 3ms:
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
12:  - {"path":"tests/unit/test_claude_settings_merge.py","reason":"Existing legacy/custom/idempotence cases remain valid through the modify script's native expansion; run this real module unchanged."}
16:  - {"path":"tests/fixtures/gate-evidence/pr-feedback-right.json","reason":"Historical feedback fixture text is data and is not rewritten."}
18:  - {"path":"home/dot_local/bin/common/executable_permgate","reason":"Unchanged dependency-free script, executed through explicit isolated Python rather than its shebang."}
49:  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the eight named regressions and scoped hostile-input cases, recording Class::test selectors without claiming system-wide closure or treating an earlier refusal as coverage of a later check."}
68:  - {"command":"sed -n '179,182p' Makefile | paste -sd '|' -","output":"format:| shfmt --indent 4 --space-redirects --diff .| git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check| git ls-files -z '*.md' | xargs -0 prettier --check"}
70:  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_agents/agent-config.yaml home/.chezmoitemplates/claude-settings-managed.json home/dot_claude/modify_private_settings.json home/dot_claude-worker/modify_private_settings.json scripts/generate-agent-configs.py scripts/validate-agent-assets.py Makefile tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":"Makefile|home/.chezmoitemplates/claude-settings-managed.json|home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/generate-agent-configs.py|scripts/validate-agent-assets.py|tests/unit/test_validate_agent_assets.py"}
82:  - {"command":"rg -l 'claude-settings-managed|is_managed_permission_hook|permgate claude' home scripts tests .github Makefile --glob '!*.md' --glob '!*.lock' | sort | paste -sd '|' -","output":"home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/validate-agent-assets.py|tests/fixtures/gate-evidence/pr-feedback-right.json|tests/install/common/lifecycle.bats|tests/unit/test_claude_settings_merge.py|tests/unit/test_generate_agent_configs.py|tests/unit/test_herdr_agents.py|tests/unit/test_statusline_tools.py|tests/unit/test_validate_agent_assets.py"}
85:  - {"command":"printf '%s\\n' \"$PATH\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/shims:$HOME/.local/bin:$HOME/.local/bin/common:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$HOME/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:$HOME/.local/share/mise/installs/node/lts/bin:/usr/bin:/bin:/usr/sbin:/sbin"}
116:These are two separate task files. This primary task has exactly ten allowed_files entries: eight exact implementation/test paths, one modify-script glob and one evidence wildcard. The glob authorizes only home/dot_claude/modify_private_settings.json and home/dot_claude-worker/modify_private_settings.json, each with its own threat row. An additional match requires a reviewed split. The second file below owns mise pins and the generator assertion; do not combine their front matter or dispatch this task before that prerequisite is accepted.
122:The seven existing concrete allowlist paths were on origin/main at the recorded probe. P1-15 creates the worker modify script and ClaudeManagedSettingsTest module. Add scripts/orchestrator/trusted-launch.sh as the only new executable source. Recheck these paths and measurements on the actual dispatch baseline; refresh changed premises through a reviewed, hashed amendment before dispatch, never only in the Checks paste.
126:The root C11 test file was absent at the recorded probe, and the inspected worker-g copy accepted tests/<path>::<identifier> rather than a Class::test payload. The orchestrator must obtain and read the accepted checker/test revision before dispatch, check C1–C10, C7b and C11, and manually re-probe premises. Never execute arbitrary premise shell strings through an unchecked checker.
136:> A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
172:Refusals exit 2, emit exactly one stderr line `trusted-launch: refused: <code>`, and produce no operation output. Use dirty-environment, script-path, home-mismatch, cache-path, manifest-path, manifest-shape, fixture-root, uv-path, python-path, node-path, version-mismatch or invocation for the corresponding failed check. Version probes may run only after path checks; capture their output for validation rather than leaking it into hook stdout. Preserve underlying operation exit status after successful validation. A negative test must reach and assert its intended reason, rather than passing through an earlier refusal.
213:Retain round 3's bound online-seed decision. The operator's deployment sequence is: make update and deterministic production-manifest preparation, explicit private-cache seed through the trusted parent, then the isolated offline deployment check. The worker does not perform live deployment.
225:The checker and its yaml-importing generator child use that same manifest and cache through the parent. Never substitute the resolver's base Python or sys.executable directly for the uv-provided PyYAML environment.
235:The harness renders a fixture manifest with exact declarations and versions for those real tools, then supplies that manifest through --manifest and the test's canonical temporary directory through --fixture-root. HOME remains the real uid's passwd home.
239:The launcher sees only the declared fixture paths, validates them through the production code path and compares their actual versions with the fixture pins. Do not pass a runner's external absolute sys.executable as an unchecked exception, redirect production HOME, disable a check, or force the fixture through the production-only mise resolver.
255:Add or extend these eight regressions in the real existing classes, recording the full selectors and running their unittest dotted equivalents red before implementation and green afterward:
283:In a separate non-skippable seed subcase, place an argument-recording fake uv as a regular executable at the fixture's declared canonical path. Its --version response matches the fixture pin. Execute the actual seed launch through the parent with shell=False and --manifest/--fixture-root. Assert the complete /usr/bin/env -i … /bin/bash --noprofile --norc -p prefix, verified absolute uv/Python operands and the recorded argv:
291:Also seed a fixture private cache explicitly through the same parent and isolated seed argv with real bound uv/Python, then prove the generator child's exact offline --with pyyaml argv, shared cache and successful yaml import. An isolated base-Python-only child must not satisfy this assertion. Sandbox or network denial is reported as blocked, without an outside-sandbox retry.
313:Run make unit-test, make format, make validate-agent-assets and make render-check, the eight named regressions, and unchanged tests.unit.test_claude_settings_merge, tests.unit.test_generate_agent_configs, tests.unit.test_statusline_tools and tests.unit.test_herdr_agents. Do not run Bats locally.
317:Measure git diff --numstat origin/main...HEAD: at most 630 changed lines outside tests/ and .orchestration/, and at most 980 under tests/. Include any production configuration placed elsewhere in the production total.
341:> Wait for final-head CI and the bounded automatic Bot-review window. Record `bot: none` if the window expires. **Do not post `@codex review`**, at the ten-minute mark or after a fix. The orchestrator replies to and resolves GitHub review threads.
343:> Every `gh` command and every `git` write is an individual command **inside the sandbox**, including pushes and authenticated fetches. No compound write commands, outside-sandbox retries, excluded-command workaround, permission escalation or alternate tool to bypass a denial. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-ci-efficiency-followup-a04 status=blocked` naming the exact command, failure and crossed boundary; preserve the evidence and wait.
390:  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | paste -sd '|' -","output":"home/dot_mise/config.toml|tests/unit/test_generate_agent_configs.py"}
404:In GenerateAgentConfigsTest add test_trusted_entrypoint_mise_versions_are_exact, red before the config change and green afterward. Refactor test_managed_hooks_use_installed_permgate_paths to compare the complete rendered PermissionRequest command with the real manifest declaration rendered through the existing template helper; retain exactly one managed entry, permgate executable-leaf/claude-argument checks and the Codex assertion. Keep synthetic legacy-command fixtures. The primary task adds strict bound-sequence and parent-selected-manifest validation.
406:Measured declaration: 79 lines; touched existing test: 6 lines at 1417–1422 in a 2350-line module. Source allowance is 3 additions+3 deletions+1 reason comment+1 margin=8 lines; fixture/assertion work 60+margin 20=80 test lines. Enforce these separate caps with git diff --numstat origin/main...HEAD; evidence is excluded, executable source is not.

**Reviewing git environment constraints**
**Checking system tool availability**
exec
/bin/zsh -lc "rg -n -C 3 'excludedCommands|allowWrite|/tmp|TMPDIR|gh|sandbox' home/.chezmoitemplates/claude-worker-settings.json home/.chezmoitemplates/claude-settings-managed.json home/dot_agents/agent-config.yaml | head -190; nl -ba scripts/orchestrator/chain-integrate.sh | sed -n '27,84p'; git show a644a7d9:tests/unit/test_chain_review_scripts.py | sed -n '227,245p;296,327p;354,389p'" in ~/Workspace/dotfiles
 succeeded in 80ms:
rg: home/.chezmoitemplates/claude-worker-settings.json: No such file or directory (os error 2)
home/.chezmoitemplates/claude-settings-managed.json-1-{
home/.chezmoitemplates/claude-settings-managed.json-2-  "$schema": "https://json.schemastore.org/claude-code-settings.json",
home/.chezmoitemplates/claude-settings-managed.json-3-  "model": "claude-fable-5-1",
home/.chezmoitemplates/claude-settings-managed.json:4:  "effortLevel": "xhigh",
home/.chezmoitemplates/claude-settings-managed.json-5-  "advisorModel": "fable",
home/.chezmoitemplates/claude-settings-managed.json-6-  "alwaysThinkingEnabled": true,
home/.chezmoitemplates/claude-settings-managed.json-7-  "autoUpdates": false,
--
home/.chezmoitemplates/claude-settings-managed.json-22-      "Bash(wget * | sh)",
home/.chezmoitemplates/claude-settings-managed.json-23-      "Read(secrets/**)",
home/.chezmoitemplates/claude-settings-managed.json-24-      "Read(config/credentials.json)",
home/.chezmoitemplates/claude-settings-managed.json:25:      "Bash(gh release:*)",
home/.chezmoitemplates/claude-settings-managed.json-26-      "Bash(npm publish:*)",
home/.chezmoitemplates/claude-settings-managed.json-27-      "Bash(uv publish:*)",
home/.chezmoitemplates/claude-settings-managed.json-28-      "Bash(terraform apply:*)",
--
home/.chezmoitemplates/claude-settings-managed.json-30-    ],
home/.chezmoitemplates/claude-settings-managed.json-31-    "defaultMode": "auto",
home/.chezmoitemplates/claude-settings-managed.json-32-    "ask": [
home/.chezmoitemplates/claude-settings-managed.json:33:      "Bash(gh pr merge:*)",
home/.chezmoitemplates/claude-settings-managed.json:34:      "Bash(gh pr create:*)",
home/.chezmoitemplates/claude-settings-managed.json:35:      "Bash(gh pr comment:*)",
home/.chezmoitemplates/claude-settings-managed.json:36:      "Bash(gh pr review:*)",
home/.chezmoitemplates/claude-settings-managed.json:37:      "Bash(gh pr close:*)",
home/.chezmoitemplates/claude-settings-managed.json:38:      "Bash(gh pr edit:*)",
home/.chezmoitemplates/claude-settings-managed.json:39:      "Bash(gh pr update-branch:*)",
home/.chezmoitemplates/claude-settings-managed.json:40:      "Bash(gh issue:*)",
home/.chezmoitemplates/claude-settings-managed.json:41:      "Bash(gh api -X POST:*)",
home/.chezmoitemplates/claude-settings-managed.json:42:      "Bash(gh api --method POST:*)",
home/.chezmoitemplates/claude-settings-managed.json:43:      "Bash(gh api -XPOST:*)",
home/.chezmoitemplates/claude-settings-managed.json:44:      "Bash(gh api --method=POST:*)",
home/.chezmoitemplates/claude-settings-managed.json:45:      "Bash(gh api -X PATCH:*)",
home/.chezmoitemplates/claude-settings-managed.json:46:      "Bash(gh api --method PATCH:*)",
home/.chezmoitemplates/claude-settings-managed.json:47:      "Bash(gh api -XPATCH:*)",
home/.chezmoitemplates/claude-settings-managed.json:48:      "Bash(gh api --method=PATCH:*)",
home/.chezmoitemplates/claude-settings-managed.json:49:      "Bash(gh api -X PUT:*)",
home/.chezmoitemplates/claude-settings-managed.json:50:      "Bash(gh api --method PUT:*)",
home/.chezmoitemplates/claude-settings-managed.json:51:      "Bash(gh api -XPUT:*)",
home/.chezmoitemplates/claude-settings-managed.json:52:      "Bash(gh api --method=PUT:*)",
home/.chezmoitemplates/claude-settings-managed.json:53:      "Bash(gh api -X DELETE:*)",
home/.chezmoitemplates/claude-settings-managed.json:54:      "Bash(gh api --method DELETE:*)",
home/.chezmoitemplates/claude-settings-managed.json:55:      "Bash(gh api -XDELETE:*)",
home/.chezmoitemplates/claude-settings-managed.json:56:      "Bash(gh api --method=DELETE:*)",
home/.chezmoitemplates/claude-settings-managed.json:57:      "Bash(gh api -f:*)",
home/.chezmoitemplates/claude-settings-managed.json:58:      "Bash(gh api -F:*)",
home/.chezmoitemplates/claude-settings-managed.json:59:      "Bash(gh api --raw-field:*)",
home/.chezmoitemplates/claude-settings-managed.json:60:      "Bash(gh api --field:*)",
home/.chezmoitemplates/claude-settings-managed.json:61:      "Bash(gh api -f*)",
home/.chezmoitemplates/claude-settings-managed.json:62:      "Bash(gh api -F*)",
home/.chezmoitemplates/claude-settings-managed.json:63:      "Bash(gh api --raw-field=*)",
home/.chezmoitemplates/claude-settings-managed.json:64:      "Bash(gh api --field=*)"
home/.chezmoitemplates/claude-settings-managed.json-65-    ]
home/.chezmoitemplates/claude-settings-managed.json-66-  },
home/.chezmoitemplates/claude-settings-managed.json:67:  "sandbox": {{ if eq .chezmoi.os "darwin" }}
home/.chezmoitemplates/claude-settings-managed.json-68-{
home/.chezmoitemplates/claude-settings-managed.json-69-  "enabled": true,
home/.chezmoitemplates/claude-settings-managed.json-70-  "failIfUnavailable": false,
home/.chezmoitemplates/claude-settings-managed.json-71-  "autoAllowBashIfSandboxed": true,
home/.chezmoitemplates/claude-settings-managed.json:72:  "allowUnsandboxedCommands": true,
home/.chezmoitemplates/claude-settings-managed.json:73:  "excludedCommands": [],
home/.chezmoitemplates/claude-settings-managed.json-74-  "filesystem": {
home/.chezmoitemplates/claude-settings-managed.json:75:    "allowWrite": [
home/.chezmoitemplates/claude-settings-managed.json-76-      "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",
home/.chezmoitemplates/claude-settings-managed.json-77-      "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",
home/.chezmoitemplates/claude-settings-managed.json-78-      "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",
--
home/.chezmoitemplates/claude-settings-managed.json-106-  "enabled": true,
home/.chezmoitemplates/claude-settings-managed.json-107-  "failIfUnavailable": false,
home/.chezmoitemplates/claude-settings-managed.json-108-  "autoAllowBashIfSandboxed": true,
home/.chezmoitemplates/claude-settings-managed.json:109:  "allowUnsandboxedCommands": true,
home/.chezmoitemplates/claude-settings-managed.json:110:  "excludedCommands": [],
home/.chezmoitemplates/claude-settings-managed.json-111-  "filesystem": {
home/.chezmoitemplates/claude-settings-managed.json:112:    "allowWrite": [
home/.chezmoitemplates/claude-settings-managed.json-113-      "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",
home/.chezmoitemplates/claude-settings-managed.json-114-      "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",
home/.chezmoitemplates/claude-settings-managed.json-115-      "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",
--
home/dot_agents/agent-config.yaml-9-# - Keep MCP servers disabled by default; enable only after checking scope and credentials.
home/dot_agents/agent-config.yaml-10-# - Store credentials as environment-variable references or inherited environment only.
home/dot_agents/agent-config.yaml-11-# - Use current maintained MCP servers; deprecated packages are rejected by validation.
home/dot_agents/agent-config.yaml:12:# - Keep Codex writable roots for shared agmsg state under codex.sandbox_workspace_write.
home/dot_agents/agent-config.yaml:13:#   The Claude sandbox allowWrite list is rendered from the same entries.
home/dot_agents/agent-config.yaml-14-# - Let upstream install.sh own ~/.agents/skills/agmsg; never vendor it (assets.agmsg).
home/dot_agents/agent-config.yaml-15-
home/dot_agents/agent-config.yaml-16-schema_version: 1
--
home/dot_agents/agent-config.yaml-31-    claude: { model: haiku, effort: low }
home/dot_agents/agent-config.yaml-32-    codex: { model: gpt-5.6-luna, model_reasoning_effort: low }
home/dot_agents/agent-config.yaml-33-  standard:
home/dot_agents/agent-config.yaml:34:    claude: { model: claude-opus-5-5, effort: xhigh, advisor: fable }
home/dot_agents/agent-config.yaml-35-    codex:
home/dot_agents/agent-config.yaml-36-      model: gpt-6.1-sol
home/dot_agents/agent-config.yaml:37:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml-38-      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
home/dot_agents/agent-config.yaml-39-  review:
home/dot_agents/agent-config.yaml-40-    # Review independence rests on a fresh context, not a stronger model (operator decision 2026-10-13, plan 007 T717);
home/dot_agents/agent-config.yaml-41-    # INV-7: the Claude review profile is the same model and effort as deep.
home/dot_agents/agent-config.yaml:42:    claude: { model: claude-fable-5-1, effort: xhigh }
home/dot_agents/agent-config.yaml:43:    codex: { model: gpt-6.1-sol, model_reasoning_effort: xhigh }
home/dot_agents/agent-config.yaml-44-  deep:
home/dot_agents/agent-config.yaml:45:    claude: { model: claude-fable-5-1, effort: xhigh, advisor: fable }
home/dot_agents/agent-config.yaml-46-    codex:
home/dot_agents/agent-config.yaml-47-      model: gpt-6.1-sol
home/dot_agents/agent-config.yaml:48:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml-49-      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
home/dot_agents/agent-config.yaml-50-  security:
home/dot_agents/agent-config.yaml-51-    # Security-audit tier: specialist model for auditing pending changes.
home/dot_agents/agent-config.yaml:52:    claude: { model: claude-fable-5, effort: high }
home/dot_agents/agent-config.yaml-53-    codex:
home/dot_agents/agent-config.yaml-54-      # gpt-daybreak-blue-latest requires API-key auth (rejected under ChatGPT login).
home/dot_agents/agent-config.yaml-55-      model: gpt-6-astra
home/dot_agents/agent-config.yaml:56:      model_reasoning_effort: high
home/dot_agents/agent-config.yaml-57-      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
home/dot_agents/agent-config.yaml-58-  audit:
home/dot_agents/agent-config.yaml-59-    # Auditor tier (監査役): cross-vendor read-only audit of worker changesets
home/dot_agents/agent-config.yaml:60:    # at xhigh reasoning effort (operator pin 2026-10-09, T115).
home/dot_agents/agent-config.yaml:61:    claude: { model: claude-fable-5-1, effort: high }
home/dot_agents/agent-config.yaml-62-    codex:
home/dot_agents/agent-config.yaml-63-      model: gpt-6-astra
home/dot_agents/agent-config.yaml:64:      model_reasoning_effort: xhigh
home/dot_agents/agent-config.yaml:65:      sandbox_mode: read-only
home/dot_agents/agent-config.yaml-66-      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
home/dot_agents/agent-config.yaml-67-interactive_profile: deep
home/dot_agents/agent-config.yaml-68-# Worker pane agent for herdr-agents: codex or claude. Renders into
--
home/dot_agents/agent-config.yaml-93-  model_verbosity: low
home/dot_agents/agent-config.yaml-94-  personality: pragmatic
home/dot_agents/agent-config.yaml-95-  approval_policy: on-request
home/dot_agents/agent-config.yaml:96:  sandbox_mode: workspace-write
home/dot_agents/agent-config.yaml-97-  web_search: cached
home/dot_agents/agent-config.yaml-98-  check_for_update_on_startup: false
home/dot_agents/agent-config.yaml-99-  project_doc_max_bytes: 65536
--
home/dot_agents/agent-config.yaml-111-      - git-branch
home/dot_agents/agent-config.yaml-112-    model_availability_nux:
home/dot_agents/agent-config.yaml-113-      gpt-5.6-sol: 2
home/dot_agents/agent-config.yaml:114:  sandbox_workspace_write:
home/dot_agents/agent-config.yaml-115-    network_access: false
home/dot_agents/agent-config.yaml-116-    writable_roots:
home/dot_agents/agent-config.yaml-117-      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db'
--
home/dot_agents/agent-config.yaml-220-      - Bash(wget * | sh)
home/dot_agents/agent-config.yaml-221-      - Read(secrets/**)
home/dot_agents/agent-config.yaml-222-      - Read(config/credentials.json)
home/dot_agents/agent-config.yaml:223:      - Bash(gh release:*)
home/dot_agents/agent-config.yaml-224-      - Bash(npm publish:*)
home/dot_agents/agent-config.yaml-225-      - Bash(uv publish:*)
home/dot_agents/agent-config.yaml-226-      - Bash(terraform apply:*)
home/dot_agents/agent-config.yaml-227-      - Bash(kubectl apply:*)
home/dot_agents/agent-config.yaml-228-    # shortcut: flags after the API path escape prefix rules; the integration gate remains authoritative.
home/dot_agents/agent-config.yaml-229-    ask:
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
home/dot_agents/agent-config.yaml-262-  env:
home/dot_agents/agent-config.yaml-263-    GH_TELEMETRY: "false"
home/dot_agents/agent-config.yaml-264-    DO_NOT_TRACK: "1"
home/dot_agents/agent-config.yaml-265-    CHECKPOINT_DISABLE: "1"
home/dot_agents/agent-config.yaml-266-    AWS_EC2_METADATA_DISABLED: "true"
home/dot_agents/agent-config.yaml:267:  # Claude Code Bash sandbox, the counterpart of codex.sandbox_workspace_write:
home/dot_agents/agent-config.yaml:268:  # commands may write only the working directory, the session TMPDIR, and
    27	# @exitcode 13 The base moved three times.
    28	# @exitcode 14 The sweep has gaps.
    29	# @exitcode 15 The owner task file is absent.
    30	# @exitcode 16 A sandbox-scan hit not yet judged (`CHAIN_SCAN_JUDGED=<sha7>` after the judgement).
    31	# @example
    32	#   scripts/orchestrator/chain-integrate.sh dotfiles-T128-x-a01 370 "$PWD" "$PWD/.claude/worktrees/orchestrator-review" dotfiles-T128-x-followup-a01
    33	set -euo pipefail
    34	log='' lines=() && export NO_COLOR=1 && unset CLICOLOR_FORCE GH_FORCE_TTY # no ANSI from gh, as pr-feedback.py's gh_env
    35	say() { lines+=("$1") && { [ -z "${log}" ] || printf '%s\n' "$1" >> "${log}"; }; }
    36	refuse() { echo "chain-integrate: $2" >&2 && { [ -z "${log}" ] || say "chain-integrate: $2"; } && exit "$1"; } # <exit> <message>
    37	# <command…>: a precondition read; sets out, and a failure is exit 1
    38	pre() { out=$("$@") || { echo "step prepare failed rc=$?" >&2 && exit 1; }; }
    39	step() { # <name> <accepted statuses, comma-separated, or any> <command…>: sets out and rc; any other status is exit 1
    40	    local name=$1 ok=",$2," shown
    41	    shift 2
    42	    rc=0
    43	    out=$("$@") || rc=$?
    44	    shown="${1##*/} ${*:2}"
    45	    shown=${shown//"${main}"\//}
    46	    say "$("${date}" -u +%FT%TZ) ${name} rc=${rc}: ${shown//"${main}"/.}"
    47	    echo "${name} rc=${rc}"
    48	    [ -z "${out}" ] || printf '%s\n' "${out}"
    49	    [[ ${ok} == ,any, || ${ok} == *",${rc},"* ]] || {
    50	        echo "step ${name} failed rc=${rc}" >&2
    51	        say "step ${name} failed rc=${rc}"
    52	        exit 1
    53	    }
    54	}
    55	(($# == 5 || $# == 6)) || refuse 10 "invalid argument: chain-integrate.sh <task> <pr> <main> <review> <owner> [<extra tsv>]"
    56	task=$1 pr=$2 owner=$5 extra=${6:-}
    57	# Both ids become path segments under .orchestration/ and record content; the leading class excludes . and ..
    58	for v in "${task}" "${owner}"; do
    59	    [[ ${v} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || refuse 10 "invalid argument: ${v}"
    60	done
    61	[[ ${pr} =~ ^[0-9]+$ ]] || refuse 10 "invalid argument: ${pr}"
    62	main=$(cd -- "$3" 2> /dev/null && pwd -P) || refuse 10 "invalid argument: $3"
    63	cd -- "${main}"
    64	# Resolved before any fetch or checkout and run by absolute path, as local-review.sh resolves codex: a mise shim
    65	# would pick its binary by the directory it runs in.
    66	pick() { env -i PATH="${PATH}" HOME="${HOME}" mise which "$1" 2> /dev/null || command -v "$1" || true; }
    67	gh=$(pick gh) git=$(pick git) uv=$(pick uv) shasum=$(pick shasum) date=$(pick date)
    68	for found in "${gh}" "${git}" "${uv}" "${shasum}" "${date}"; do
    69	    [[ ${found} == /* && ${found} != */shims/* ]] || refuse 10 "no binary outside a shims directory: ${found:-none}"
    70	done
    71	[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || refuse 10 "main checkout is not on main"
    72	fresh() { pre "${git}" -C "${main}" fetch -q origin main && pre "${git}" -C "${main}" rev-parse HEAD origin/main && { [ "${out%%$'\n'*}" = "${out##*$'\n'}" ] || refuse 10 "main checkout is not origin/main: run scripts/orchestrator/ff-main.sh"; }; }
    73	fresh
    74	# They run with the orchestrator's credentials, so each must be HEAD's own copy (PR #372 thread 4291474880).
    75	for s in scripts/orchestrator/{sandbox-scan.sh,local-review.sh,local-advisory.sh,fill_sweep.py,acceptance-front-matter.py,orch-audit.sh} scripts/pr-feedback.py; do
    76	    "${git}" -C "${main}" ls-files --error-unmatch -- "${s}" > /dev/null 2>&1 || refuse 10 "${s} is not tracked in the main checkout"
    77	done
    78	"${git}" -C "${main}" diff --quiet HEAD -- scripts || refuse 10 "scripts/ in the main checkout differs from HEAD"
    79	pre "${git}" -C "${main}" rev-parse --show-toplevel
    80	canonical=${out}/.claude/worktrees/orchestrator-review
    81	review=$(cd -- "$4" 2> /dev/null && pwd -P) || review=$4
    82	[ "${review}" = "${canonical}" ] || refuse 10 "review worktree is not the canonical one: ${canonical}"
    83	[ -e "${review}/.git" ] || refuse 10 "review worktree is not a worktree root"
    84	pre "${git}" -C "${review}" status --porcelain
    def test_local_review_resolves_codex_through_mise_and_refuses_a_shim(self):
        # audit:b6ce4ff:1 (operator decision A's P1): codex is what mise which answers under env -i, never a shim.
        review, head, env = self.review_head()
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        self.stub(self.temp / "installs/codex", "installed")
        env["MISE_CONFIG_FILE"] = str(self.temp / "payload.toml")
        self.mise(f'printf "%s\\n" "{self.temp}/mise/shims/$2"\n')
        self.assertIn(
            "is under a shims directory; refused", self.run_tool("local-review.sh", "t-a", head, 9, code=2, env=env)
        )
        self.assertEqual(self.git("rev-parse", "main"), self.git("rev-parse", "HEAD", cwd=review))
        # mise knows codex only, so the stub's own env-shebang interpreter (bash) falls back to command -v.
        self.mise(f'[[ $2 == codex ]] && printf "%s\\n" "{self.temp}/installs/$2"\n')
        self.run_tool("local-review.sh", "t-a", head, 9, env=env)
        self.assertEqual(1, self.log("installed").count(ARGV))
        self.assertEqual("", self.log("codex"))
        asked = [f"argv: which {name} MISE_CONFIG_FILE=unset" for name in ("codex", "codex", "bash", "gh")]
        self.assertEqual(asked, self.log("mise").splitlines())

    def test_local_review_passes_no_replace_and_no_graft_to_the_commands_codex_spawns(self):
        # Local review of dbc8b67: Codex's shell_environment_policy.inherit=core drops exported variables from the
        # commands it spawns, so the two values reach them only as shell_environment_policy.set overrides.
        _, head, env = self.review_head()
        codex = self.temp / "bin/policy-codex"
        codex.write_text(
            '#!/bin/bash\nkept=()\nfor a in "$@"; do\n    case $a in shell_environment_policy.set.*)\n'
            '        echo "override: $a" >> "$CALLS/policy.log"\n        kv=${a#shell_environment_policy.set.}\n'
            '        v=${kv#*=}; v=${v#\\"}; kept+=("${kv%%=*}=${v%\\"}") ;;\n    esac\ndone\n'
            "# inherit=core: the spawned command starts from an empty environment plus the set overrides.\n"
            'env -i PATH=/usr/bin:/bin "${kept[@]}" /usr/bin/env | /usr/bin/grep "^GIT_" | sort >> "$CALLS/spawned.log"\n'
            'printf "codex\\nNo findings.\\n"\n'
        )
        codex.chmod(0o755)
        self.run_tool("local-review.sh", "t-a", head, 9, env={**env, "CODEX_BIN": str(codex)})
        overrides = [f"override: {o.removeprefix('-c ')}" for o in POLICY.split(" -c ")]
        self.assertEqual(overrides, self.log("policy").splitlines())
        self.assertEqual(["GIT_GRAFT_FILE=/dev/null", "GIT_NO_REPLACE_OBJECTS=1"], self.log("spawned").splitlines())

    def test_local_review_resolves_the_review_binary_before_the_checkout(self):
        # audit:b6ce4ff:4: mise answers while the review worktree is still where the run found it, not at the head.
        review, head, env = self.review_head()
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        self.stub(self.temp / "installs/codex", "installed")
        self.mise(
            f'[[ $2 == codex ]] || exit 1\ngit -C "{review}" rev-parse HEAD > "{self.calls}/mise-head"\n'
            f'printf "%s\\n" "{self.temp}/installs/$2"\n'
        )
        self.run_tool("local-review.sh", "t-a", head, 9, env=env)
        self.assertEqual(self.git("rev-parse", "main"), (self.calls / "mise-head").read_text().strip())
        self.assertIn(f"head: {head}\n", self.log("installed"))

    def test_local_review_pins_the_review_binary_interpreter(self):
        # The audit of c45f9b5: a binary whose first line is an env shebang runs under the interpreter mise which
        # answers in the root, never one PATH finds in the PR worktree.
        review, head, env = self.review_head()
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        binary = self.temp / "installs/codex"
        self.stub(binary, "codex")
        binary.write_text(binary.read_text().replace("#!/usr/bin/env bash\n", "#!/usr/bin/env -S interp --flag\n"))
        interp = self.temp / "installs/interp"
        interp.write_text(
            f'#!/bin/bash\nprintf "%s\\n" "$*" > "{self.calls}/interp.argv"\nshift\nexec /bin/bash "$@"\n'
        )
        interp.chmod(0o755)
        out = self.repo / f".orchestration/validation/t-a-local-review-{head[:7]}.md"
        with self.subTest("the interpreter mise answers runs the binary"):
            # mise knows the installed tools only, so gh falls back to the stub on PATH.
            self.mise(f'[ -e "{self.temp}/installs/$2" ] && printf "%s\\n" "{self.temp}/installs/$2"\n')
            self.run_tool("local-review.sh", "t-a", head, 9, env=env)
            self.assertEqual(
                f"--flag {binary} {ARGV.removeprefix('argv: ')}{self.git('rev-parse', 'main')}\n",
                (self.calls / "interp.argv").read_text(),
            )
            self.assertEqual(1, self.log("codex").count(ARGV))
        out.unlink()
        (self.calls / "interp.argv").unlink()
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        with self.subTest("an interpreter under a shims directory is refused before the checkout"):
            self.mise(f'[[ $2 == codex ]] && printf "%s\\n" "{binary}" || printf "%s\\n" "{self.temp}/mise/shims/$2"\n')
            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=2, env=env)
            self.assertIn("review binary's interpreter", stdout)
            self.assertIn("is under a shims directory; refused", stdout)
            self.assertEqual(self.git("rev-parse", "main"), self.git("rev-parse", "HEAD", cwd=review))
            self.assertFalse(out.exists())
            self.assertFalse((self.calls / "interp.argv").exists())

    def test_local_review_keeps_env_S_shebang_arguments(self):

**Reviewing citation and auditing requirements**
exec
/bin/zsh -lc "nl -ba scripts/orchestrator/chain-integrate.sh | sed -n '136,194p'; nl -ba scripts/orchestrator/local-advisory.sh | sed -n '1,125p'; sed -n '675,690p' home/dot_agents/agent-config.yaml; rg -n 'exclude_tmp|TMPDIR|writable_roots|sandbox_workspace_write' home/dot_agents/agent-config.yaml" in ~/Workspace/dotfiles
 succeeded in 74ms:
   136	# C-29: the scan reports and exits 0, so the chain is the stop its reader used to be.
   137	step sandbox-scan 0 "${main}/scripts/orchestrator/sandbox-scan.sh" "${task}"
   138	[ -z "${out}" ] || say "${out}"
   139	if [[ ${out} == *"sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"* ]]; then
   140	    [ "${CHAIN_SCAN_JUDGED:-}" = "${sha7}" ] || refuse 16 "sandbox scan hit: judge it, then re-run with CHAIN_SCAN_JUDGED=${sha7}"
   141	    say "sandbox scan: judged by the orchestrator"
   142	fi
   143	step local-review 0,3 "${main}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
   144	findings=0
   145	[[ ! ${out} =~ local-review:\ ([0-9]+)\ findings ]] || findings=${BASH_REMATCH[1]}
   146	if ((rc == 3)); then
   147	    [ -f "${main}/.orchestration/tasks/${owner}.md" ] || refuse 15 "write the owner task ${owner} first"
   148	    step local-advisory 0,3 "${main}/scripts/orchestrator/local-advisory.sh" "${task}" "${head}" "${owner}"
   149	    ((rc == 0)) || refuse 11 "a P0/P1 local finding: the one round or the operator"
   150	fi
   151	sweep=${v}/${task}-pr-feedback.json comments=${v}/${task}-pr-comments.json
   152	step pr-feedback 0 "${uv}" run --no-project python -I "${main}/scripts/pr-feedback.py" "${pr}" --json "${sweep}"
   153	step fill-sweep 0 "${gh}" api user --jq .login
   154	login=${out}
   155	# One compact object per line, joined into one array, so a second page does not end the JSON after the first.
   156	step fill-sweep 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/comments" --paginate --jq '.[]'
   157	printf '[%s]\n' "${out//$'\n'/,}" > "${comments}"
   158	step fill-sweep 0,1 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/fill_sweep.py" "${sweep}" "${comments}" ${extra:+"${extra}"} --orchestrator-login "${login}"
   159	rm -f -- "${comments}"
   160	gaps=unknown
   161	[[ ! ${out} =~ gaps\ ([0-9]+) ]] || gaps=${BASH_REMATCH[1]}
   162	((rc == 0)) || refuse 14 "sweep gaps: ${gaps}"
   163	now=$("${date}" -u +%FT%TZ)
   164	body="orchestrator integration review of PR #${pr} at ${head}: local review ${findings} finding(s), each with its line in the acceptance record; sweep complete"
   165	printf '[{"id": "%s", "scope": "review", "resolved": true, "author": "claude-code", "head": "%s", "pr": "%s", "reviewed_at": "%s", "body": "%s"}]\n' \
   166	    "${task}-pr${pr}-review-1" "${head}" "${pr}" "${now}" "${body}" > "${v}/${task}-crit.json"
   167	say "${now} receipt rc=0: printf > .orchestration/validation/${task}-crit.json"
   168	printf 'review_surface: crit-data\nreviewer: claude-code\nreview_source: %s\nreview_outcome: approved\nhead: %s\npr: %s\nreviewed_at: %s\nnote: %s\n' \
   169	    ".orchestration/validation/${task}-crit.json" "${head}" "${pr}" "${now}" \
   170	    "${body} (chain-integrate.sh; the task-level audit of this head is recorded separately in .orchestration/validation/${task}-audit-${sha7}.md)" \
   171	    > "${v}/${task}-review-receipt.md"
   172	say "${now} receipt rc=0: printf > .orchestration/validation/${task}-review-receipt.md"
   173	# The gate's LEDGER_ID: a thread id of ten or more digits or audit:<sha7>:<n>; local: rows stay in the prose.
   174	tsv=${v}/${task}-ledger-${sha7}.tsv
   175	step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
   176	printf '%s\n' "${out}" > "${tsv}"
   177	step record 0 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/acceptance-front-matter.py" "${task}" "${sweep}" "${review}" --ledger "${tsv}"
   178	rm -f -- "${tsv}"
   179	# C-61 (plan 023 F1): an update-branch-only head, a merge of main into the audited head whose PR patch is unchanged,
   180	# inherits that head's audit under its own names; the first line names the head the audit ran on, whose ids it keeps.
   181	# --verbatim keeps whitespace in the id, so a whitespace-only change is a new patch (PR #390 thread 4302490292).
   182	patch() { "${git}" -C "${main}" diff-tree -p "$("${git}" -C "${main}" merge-base origin/main "$1")" "$1" | "${git}" -C "${main}" patch-id --verbatim; }
   183	parent=$("${git}" -C "${main}" rev-parse -q --verify "${head}^1" || true) old='' new=''
   184	from=${v}/${task}-audit-${parent:0:7}
   185	if [[ -n ${parent} && -f ${from}.md && -f ${from}.md.last.md ]] && "${git}" -C "${main}" merge-base --is-ancestor "${head}^2" origin/main 2> /dev/null; then
   186	    old=$(patch "${parent}") || old='' # computed outside the condition, so a failure is an empty id and a fresh audit
   187	    new=$(patch "${head}") || new=''
   188	    # patch-id ignores hunk positions, so the head must also be the tree a clean merge of its parents writes: a
   189	    # conflict (merge-tree exits 1) or any edit made in the merge gets a fresh audit (re-plan R1).
   190	    tree=$("${git}" -C "${main}" merge-tree --write-tree "${head}^1" "${head}^2") || tree=''
   191	    [[ -n ${tree} && ${tree} == "$("${git}" -C "${main}" rev-parse "${head}^{tree}")" ]] || old=''
   192	    # The receipt names its head by 7 characters only: the parent's chain log must name the parent's full sha in its
   193	    # verdict line, so a commit ground to the same prefix never loads another head's audit (PR #413 thread 4306231809).
   194	    /usr/bin/awk -v t="${task}" -v p="${parent}" '$1 == "chain-integrate:" && $2 == t && $3 == p { f = 1 } END { exit !f }' \
     1	#!/usr/bin/env bash
     2	# @file local-advisory.sh
     3	# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
     4	# @description
     5	#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
     6	#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
     7	#   other appends the row `local:<sha7>:<n><TAB><class>` under the heading `## Owned by <owner>` of
     8	#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
     9	#   not-applicable:advisory P2 owned by <owner> (…); evidence=shasum -a 256 .orchestration/tasks/<owner>.md
    10	#   (<sha256>)` line, each only when the record lacks it. A review with findings needs the owner task file. The
    11	#   class is `advisory-p2`, unless the finding's `path:line[-line]` token (backticks ignored) matches a finding of
    12	#   the task's earlier local review files (`<task>-local-review-<sha7>.md` only) whose `local:` row in the record,
    13	#   matched by its exact id, has another class: then the last such row's class, and the line's parenthesis names it
    14	#   as `repeat of local:<sha7>:<n>` (C-50).
    15	# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
    16	# @arg $2 string The reviewed head, 40 hex characters.
    17	# @arg $3 string The task id that owns the advisory findings, in the task id's form.
    18	# @exitcode 0 No P0/P1 finding.
    19	# @exitcode 2 No local review file, a malformed task id, head or owner task id, or (for a review with findings) no
    20	#   owner task file: `write the owner task <owner> first`.
    21	# @exitcode 3 A P0/P1 finding.
    22	# @example
    23	#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
    24	set -euo pipefail
    25	task=$1 head=$2 owner=$3
    26	# Both name the files read and appended, so a / in either would reach outside .orchestration (the audit of b6ce4ff).
    27	# The owner is written into the record verbatim, so it takes the task id's form too.
    28	id='^[A-Za-z0-9][A-Za-z0-9._-]*$'
    29	[[ $task =~ $id && $head =~ ^[0-9a-f]{40}$ && $owner =~ $id ]] || {
    30	    echo "usage: local-advisory.sh <task> <40-hex head> <owner task>"
    31	    exit 2
    32	}
    33	cd "$(git rev-parse --show-toplevel)"
    34	h7=${head:0:7}
    35	LR=".orchestration/validation/$task-local-review-$h7.md"
    36	A=".orchestration/acceptance/$task.md"
    37	[ -s "$LR" ] || {
    38	    echo "no local review file $LR"
    39	    exit 2
    40	}
    41	n=$(sed -n 's/^findings: //p' "$LR" | head -1)
    42	[ "${n:-0}" != "0" ] || {
    43	    echo "local review of $h7: no findings"
    44	    exit 0
    45	}
    46	# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
    47	O=".orchestration/tasks/$owner.md"
    48	[ -f "$O" ] || {
    49	    echo "write the owner task $owner first"
    50	    exit 2
    51	}
    52	sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
    53	# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
    54	# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
    55	# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
    56	token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
    57	earlier=""
    58	for f in .orchestration/validation/"$task"-local-review-*.md; do
    59	    [[ -f $f && $f != "$LR" ]] || continue
    60	    # The exact prefix is stripped, so the whole rest of the name must be the head: a name with a second
    61	    # `-local-review-` cannot pass as its last part (the audit of 000c5c6, finding 1).
    62	    e=${f%.md} && e=${e#.orchestration/validation/"$task"-local-review-} && k=0
    63	    # Only a seven-hex suffix names a reviewed head; any other file is skipped (the audit of d3e8acf, finding 1).
    64	    [[ $e =~ ^[0-9a-f]{7}$ ]] || continue
    65	    while IFS= read -r l; do
    66	        k=$((k + 1))
    67	        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
    68	    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
    69	done
    70	# A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
    71	awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
    72	i=0 stop=0
    73	while IFS= read -r line; do
    74	    i=$((i + 1))
    75	    case "$line" in
    76	    *"[P0]"* | *"[P1]"*)
    77	        echo "STOP: local finding $i of $h7 is P0/P1: $line"
    78	        stop=1
    79	        ;;
    80	    *)
    81	        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
    82	        class=advisory-p2 repeat=""
    83	        t=$(token "$line") || t=""
    84	        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
    85	        if [[ -n $t && -n $ids ]]; then
    86	            # A row's id is its first tab-separated field, compared as text, never as a pattern.
    87	            row=$(awk -F'\t' -v ids="${ids%|}" 'BEGIN { n = split(ids, a, "|"); for (j = 1; j <= n; j++) s[a[j]] = 1 } NF > 1 && ($1 in s) && $0 !~ /\tadvisory-p2$/' "$A" | tail -1 || true)
    88	            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
    89	        fi
    90	        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
    91	        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
    92	        ;;
    93	    esac
    94	done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
    95	echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
    96	[ "$stop" = 0 ] || exit 3
12:# - Keep Codex writable roots for shared agmsg state under codex.sandbox_workspace_write.
114:  sandbox_workspace_write:
116:    writable_roots:
267:  # Claude Code Bash sandbox, the counterpart of codex.sandbox_workspace_write:
268:  # commands may write only the working directory, the session TMPDIR, and
270:  # codex.sandbox_workspace_write.writable_roots so both agents share one agmsg

**Analyzing repository environment inconsistencies**
**Reviewing Git configuration isolation challenges**

I’m examining the need for strict Git environment isolation using config flags and environment variables, noting contradictions between test expectations and practical overrides, plus issues with Python environment inheritance and sandboxing risks.
**Checking temporary write settings**
codex
判定に影響する具体的な不整合が見つかりました。レビュー成果物を私設パスへ移しても、変更を禁止された `local-advisory.sh` は旧パスを読み続けるため、P0/P1 の停止判断に別の成果物を使えます。また、同一 UID に対する一時領域・キャッシュの保護と、呼び出し元での環境無害化には、今回の依存関係に含まれない前提が残っています。
exec
/bin/zsh -lc "sed -n '108,132p' home/dot_agents/agent-config.yaml; sed -n '263,296p' home/dot_agents/agent-config.yaml; git show a644a7d9:scripts/orchestrator/local-advisory.sh | sed -n '33,45p'; sed -n '1,85p' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md; rg -n 'threat.table|non-path|one per' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 80ms:
      - total-output-tokens
      - five-hour-limit
      - weekly-limit
      - git-branch
    model_availability_nux:
      gpt-5.6-sol: 2
  sandbox_workspace_write:
    network_access: false
    writable_roots:
      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db'
      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams'
      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run'
      - '{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools'
  shell_environment_policy:
    inherit: core
    set:
      PATH: '{{ .chezmoi.homeDir }}/.local/share/mise/installs/node/lts/bin:{{ .chezmoi.homeDir }}/.local/share/mise/shims:{{ .chezmoi.homeDir }}/.local/bin:{{ .chezmoi.homeDir }}/.local/bin/common:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
  features:
    plugins: true
    hooks: true
    plugin_hooks: true
  plugins:
    superpowers@openai-curated:
      enabled: true
    crit@mryfmo-personal-plugins:
    GH_TELEMETRY: "false"
    DO_NOT_TRACK: "1"
    CHECKPOINT_DISABLE: "1"
    AWS_EC2_METADATA_DISABLED: "true"
  # Claude Code Bash sandbox, the counterpart of codex.sandbox_workspace_write:
  # commands may write only the working directory, the session TMPDIR, and
  # filesystem.allowWrite. The generator renders allowWrite from
  # codex.sandbox_workspace_write.writable_roots so both agents share one agmsg
  # writable-roots list; ~/.claude is sandbox-protected, so it is not listed.
  # bubblewrap and socat come from the installers that the operator runs with
  # `make update` outside Claude sessions; on Ubuntu 24.04+ the bwrap-userns
  # AppArmor profile (install/ubuntu/common/apparmor_userns.sh) lets bwrap
  # create user namespaces.
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
cd "$(git rev-parse --show-toplevel)"
h7=${head:0:7}
LR=".orchestration/validation/$task-local-review-$h7.md"
A=".orchestration/acceptance/$task.md"
[ -s "$LR" ] || {
    echo "no local review file $LR"
    exit 2
}
n=$(sed -n 's/^findings: //p' "$LR" | head -1)
[ "${n:-0}" != "0" ] || {
    echo "local review of $h7: no findings"
    exit 0
}
---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-descendants-followup-a01
kind: code
security: true
allowed_files:
  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
  - home/dot_claude/hooks/executable_project-map-reload.sh
  - home/dot_agents/skills/agmsg/scripts/**
  - scripts/format-staged.sh
  - tests/unit/test_trusted_descendants.py
  - .orchestration/dotfiles-T133-trusted-entrypoint-descendants-followup-a01/**
after: [dotfiles-T133-trusted-entrypoint-binding-a01]
owner_of:
  - dotfiles-T133-worker-write-boundary-slice1-a01
  - dotfiles-T133-worker-write-boundary-slice2-a01
  - dotfiles-T133-worker-write-boundary-slice3-a01
  - dotfiles-T133-worker-write-boundary-slice4-a01
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-descendants-followup-a01 — owner of the descendant execution binding (guard, delivery, formatter, map)

Written 2026-10-21 by the orchestrator seat before the first owner disposition of the P1-15 slices (C-51: the owner task exists before the first advisory row), per re-plan v2 J1 and the allocation draft `.agents/worklog/orchestrator-glue/a04-allocation-r1.md` section 3. `dotfiles-T133-trusted-entrypoint-binding-a01` excludes this work at its line 19 ("Complete guard, delivery and formatter/map descendant binding is outside this split"), so a04's Out of scope and the slice texts name this task instead.

## Scope

Bind the execution of the four descendant families to their declared interpreters, inputs and configuration, with a rejection test per family, after binding-a01 has landed the trusted entrypoint:

1. **Guard**: the installed orchestrator-only guard, its interpreter and the fixed project payload chain (ContextDB hooks, the stop gate, state and attachment operations) and the inputs they consume.
2. **Delivery**: the fixed agmsg delivery operations (session-start, session-end, check-inbox, identities) and the descendants they reach, their executable identities and configuration inputs. Store-driver and plugin authorization stay with the agmsg-hardening owner.
3. **Formatter**: the formatter script and the Ruff/Prettier/Node chain, its configuration selection, executable availability and rejection tests.
4. **Map**: the project-map reload hook and the terminal-browser/runtime descendants, their selected inputs and configuration, and rejection tests.

Out of scope: the legacy PermissionRequest command, its structural validator and isolated execution (binding-a01); version pins (pins-a01); the slices' own routing and screening (their residual rows stay residual for the implemented portion and name this task for the deferred binding).

## Owned rows

The slice records' rows that name this task as owner are read from `## Owned by dotfiles-T133-trusted-entrypoint-descendants-followup-a01` in `.orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice{1,2,3,4}-a01.md`. Deployment that needs complete binding (new guard/delivery/formatter/map descendant execution) waits for this task; the Phase-A deployment of P1-15 keeps the recorded existing-binding allowance and its compensating controls.

## Check and Completion

Dispatched only after binding-a01 merges; the dispatch amendment fixes allowed_files to the files the four families actually execute (listed above as the expected set), adds one threat row per allowed_files entry and per family, and names the rejection test selectors. RESULT lists each family's binding, its test and the deployment check that releases the dependents.

## Checks (pasted by the orchestrator before each send)

```text
(empty until dispatch)
```
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.

**Analyzing Git PATH binding issues**
**Summarizing design and security findings**

I’m organizing key findings about potential security gaps and contract enforcement issues in the review design, focusing on specific code lines for stale consumers, temp usage, cache paths, parent prerequisites, and resolver test violations. I’m careful to limit speculation and plan to provide a concise set of roughly five strong, security-focused points followed by a clear final verdict with risk notes and summary.
**Analyzing temporary directory permissions**
**Summarizing permission and resolver conflicts**

I'm reviewing unresolved permission and resolver test conflicts, weighing findings about consumer, tmp, cache, and inherited resolver behaviors. The complexity arises from balancing path preservation with test bindings and design inconsistencies; I’m deciding which key points to include and how concise the final summary should be while maintaining clarity.
codex
[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:65 Keeping `local-advisory.sh` unchanged disconnects enforcement from the reviewed artifact: it still reads `.orchestration/validation/<task>-local-review-<sha7>.md`, whereas Item 3 writes a private full-head filename; when the new review returns P1 findings, a planted legacy `findings: 0` makes the advisory consumer return success and lets `chain-integrate.sh` continue.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:77 A mode-0700 directory under `${TMPDIR:-/tmp}` does not establish a worker-inaccessible object store: same-UID workers with access to that temporary root can modify it, and item 3’s worker-root/symlink/case checks do not exclude shared scratch space; replacement after fetch can therefore change the content consumed by the reviewer, while the named stub test establishes no write boundary.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:23 Cache provenance cannot be `closed` while line 30 acknowledges unenforced Claude file-tool protection and `after: []` imposes no deployment prerequisite: a worker can forge an anchored-cache artifact containing the publicly computable head/base/tree and `findings: 0`; fresh canonical lookup and fetch validate those identifiers, not who produced the review.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:31 Referencing a trusted-parent contract does not supply a trusted caller: `chain-integrate.sh:143` directly executes the script with inherited environment, and neither this task nor the named binding owner authorizes changing that caller; `BASH_ENV` or Linux loader injection can execute before child sanitization, including before an unsandboxed gh invocation, so clean Git/gh children cannot compensate for the missing entry boundary.

[P2] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:92 Preserving every inherited regression conflicts with the required executable binding: the inherited tests explicitly require PATH-selected `mise which` calls and interpreter fallback, while design §5.14 item 9 prohibits both; they also require exactly two Codex environment overrides despite the configured reviewer PATH containing mise shims, so these assertions must be revised to verify the actual descendant Git binding.

📝 まとめ: タスク本文と参照記録を読み取り専用で審査し、実行・成果物の結び付けと保護前提に5件の指摘を確認しました。
Not checked: implementation, live sandbox enforcement, or test execution; the stated controls do not yet establish the claimed boundaries.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
94,046
[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:65 Keeping `local-advisory.sh` unchanged disconnects enforcement from the reviewed artifact: it still reads `.orchestration/validation/<task>-local-review-<sha7>.md`, whereas Item 3 writes a private full-head filename; when the new review returns P1 findings, a planted legacy `findings: 0` makes the advisory consumer return success and lets `chain-integrate.sh` continue.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:77 A mode-0700 directory under `${TMPDIR:-/tmp}` does not establish a worker-inaccessible object store: same-UID workers with access to that temporary root can modify it, and item 3’s worker-root/symlink/case checks do not exclude shared scratch space; replacement after fetch can therefore change the content consumed by the reviewer, while the named stub test establishes no write boundary.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:23 Cache provenance cannot be `closed` while line 30 acknowledges unenforced Claude file-tool protection and `after: []` imposes no deployment prerequisite: a worker can forge an anchored-cache artifact containing the publicly computable head/base/tree and `findings: 0`; fresh canonical lookup and fetch validate those identifiers, not who produced the review.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:31 Referencing a trusted-parent contract does not supply a trusted caller: `chain-integrate.sh:143` directly executes the script with inherited environment, and neither this task nor the named binding owner authorizes changing that caller; `BASH_ENV` or Linux loader injection can execute before child sanitization, including before an unsandboxed gh invocation, so clean Git/gh children cannot compensate for the missing entry boundary.

[P2] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:92 Preserving every inherited regression conflicts with the required executable binding: the inherited tests explicitly require PATH-selected `mise which` calls and interpreter fallback, while design §5.14 item 9 prohibits both; they also require exactly two Codex environment overrides despite the configured reviewer PATH containing mise shims, so these assertions must be revised to verify the actual descendant Git binding.

📝 まとめ: タスク本文と参照記録を読み取り専用で審査し、実行・成果物の結び付けと保護前提に5件の指摘を確認しました。
Not checked: implementation, live sandbox enforcement, or test execution; the stated controls do not yet establish the claimed boundaries.
Verdict: incorrect
