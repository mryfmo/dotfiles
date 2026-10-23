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
session id: 01a15cd0-1ab2-7c01-b820-8e59d99a8360
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
実装前の設計として、task 本文・threat_table・参照された acceptance/review を読み、判断した対象と実行対象が一致するかを確認します。agmsg-orchestration と Ponytail のレビュー手順を参照し、読み取り専用で進めます。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 2ms:
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
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
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
/bin/zsh -lc 'git status --short; git rev-parse HEAD; cat .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md' in ~/Workspace/dotfiles
 succeeded in 17ms:
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
 M .orchestration/tasks/dotfiles-T133-pre-send-check-a02.md
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
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-chain-08b8add.log
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
---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a08
reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]
kind: code
security: true
allowed_files:
  - scripts/orchestrator/local-advisory.sh
  - scripts/orchestrator/local-review.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**
  - scripts/orchestrator/chain-integrate.sh
  - tests/unit/test_chain_glue.py
after: []
retained_predecessor_directories:
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
threat_table:
  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success"}
  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; temporary fixtures assert consumed content, refusals and descendant bindings; audit checks sensitivity and retained behavioral regressions."}
  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; records are untrusted evidence compared with dispatched bytes, diff and final-head CI; no runtime helpers."}
  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1"}
  - {control: "tests/unit/test_chain_glue.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fixtures exercise the actual caller and consumer; audit compares assertions with execution and stop behavior."}
  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; compare whole-file bytes and dispatch SHA-256 at acceptance."}
  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; preserve SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 and compare at acceptance."}
  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; report, validation, sandbox, learning and autoskill records identify producers, commands, statuses, provenance and every refusal."}
  - {control: "review-cache identity and shared-artifact rejection", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
  - {control: "review-cache producer authenticity", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; head/base/tree are public identifiers, not producer authentication; production reuse is held until deployed write protection is evidenced."}
  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; consistency checks before dispatch/acceptance and whole-file comparison detect changed metadata."}
  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; parse front matter as data and compare complete bytes; evidence confers no execution authority."}
  - {control: "in-process effects", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; private repositories and bound reviewers run under verified host prerequisites; fixtures never fetch live GitHub content."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; this task binds the actual chain review call sites; complete host executable/input provisioning remains separately deployed."}
  - {control: "new or renamed scripts", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none authorized; audit rejects undeclared helpers, wrappers or renames."}
  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; shared credentials and unrestricted same-UID processes remain outside prevention; missing acceptance is detected at the next records PR."}
  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; protected storage requires deployed Bash and file-tool boundaries for every active worker kind; mode 0700 alone proves none."}
  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed caller establishes child entry boundaries; orchestrator must supply the clean outer parent before chain shell/loader startup."}
  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; reject shared scratch, worker roots and aliases for production objects/artifacts; live boundary evidence remains mandatory."}
  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; use the same verified bindings/content without rediscovery; unrestricted same-UID replacement remains possible."}
  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fresh lookup/fetch precede full head/base/tree cache comparison; unique invocation roots introduce no reservation."}
  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; functional cache tests do not authenticate producers or prove live deployment, credentials, executable protection or reservations."}
  - {control: "design 5.14 item 7: 検証", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; security-assertion red/green evidence covers source, cache, consumer and entry behavior, not the whole host contract."}
  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; fresh protected object stores and protected artifacts avoid shared caches; host executable/input provenance remains a deployment residual."}
  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; every Codex worker command remains sandboxed; denial produces blocked evidence without escalation."}
  - {control: "orchestrator effect trusted-parent launch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; invoke the anchored chain under design 5.14 item 2 before its first executable; no direct inherited-environment launch or self-reexec."}
  - {control: "orchestrator effect production release", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice5-a01; verify installed protection and activation before dispatch/live use; merge, after: [] and fixture success do not release dependents."}
  - {control: "orchestrator effect cache commissioning", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; after verified deployment, commission empty protected storage and quarantine prior artifacts; only reviews produced after commissioning may authorize reuse."}
  - {control: "orchestrator effect merge", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; only gh pr merge --squash --match-head-commit <audited head> after Playbook step 10; worker never merges or pushes main."}
  - {control: "orchestrator effect update-branch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed head invalidates earlier CI, sweep, audit and security evidence; repeat before the gate."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none planned; explicit force and acceptance recording of discarded state are required for dirty removal."}
premises:
  - {claim: "worker (Codex seat, review-profile authoring context): local continuation identity only; this does not authenticate content.", command: "git rev-parse --verify 'a644a7d9^{commit}'", output: "a644a7d965399b9463e9b32721287440a7efa233"}
  - {claim: "worker (Codex seat, review-profile authoring context): predecessor copy matches dispatched a07 bytes.", command: "git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256", output: "b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -"}
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content

Independent-context reset after INV-6 S2 (two amendments including the erroneous resend; D-024-41); preserve a07 history in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md`.
Continue PR #439, branch `tools/chain-review-scripts-followup-a07`, from `a644a7d965399b9463e9b32721287440a7efa233` with worker a013 (Codex, worker-h); create no branch or PR.
Retain inherited code head `f5aaaf7e` except the corrections below; the two additional allowed paths authorize only C-80's actual caller/consumer binding and its regression, never a09's CI-wait or stale-comment rows.
Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen (D-024-29), applies by reference (D-024-30), and its items 0–10 have individual threat rows; do not restate its contract.
Read the whole a07 task, its acceptance, `.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md` and `.agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md`.
Before dispatch, the orchestrator records deployed design 5.14 items 1–4/9 protection for every active worker kind, installed bindings and the clean outer chain launch; otherwise keep this task and PR held.
P1-15's slice2 startup/administrative outputs and slice5 activation require actual deployment evidence; neither merge nor `after: []` establishes readiness. No worker deploys settings or invents an enforcement sentinel.
After protection is verified, the trusted orchestrator commissions empty protected review storage, quarantines pre-existing artifacts and records that boundary/creation order; pre-deployment artifacts cannot become trusted by matching public identifiers.

## Item 1

The a06 record's `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` still has no rows; import none from a09.
C-80 requires `local-advisory.sh` to consume the exact protected artifact produced by Item 3, with full head/base/tree identity, rather than the legacy shared `.orchestration/validation/<task>-local-review-<sha7>.md`.
Have `chain-integrate.sh` hand that completed invocation's exact protected path and identities to the advisory consumer; validate containment, metadata and finding/count consistency before using it, and refuse missing, malformed or mismatched evidence with exit 2.
Never default a missing count to zero or fall back to shared artifacts; retain P0/P1 exit 3, chain exit 11 and existing P2/P3 ownership/repeat semantics, reading prior review content only from protected full-head artifacts.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success`: a private P1 plus planted legacy zero must stop; missing/mismatched private evidence must refuse; retain positive advisory cases.

## Item 2

On every `local-review.sh` invocation, before any cache read, use the bound gh for `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; require successful exit and exactly 40 ASCII hexadecimal characters, otherwise a named exit-2 refusal.
Neither local `main` nor `origin/main` selects the base; pass that exact SHA to `codex review --base`, with commit checks in Item 3's private store.
Keep `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` exported and passed through `-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"'` and `-c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'`.
Preserve failed-review refusal, full-head equality, finding/output behavior and inherited red/green provenance; revise unsafe executable-resolution expectations and cache trust/location as required below, without undoing implemented fixes to reproduce old reds.

## Item 3

Close `audit:a644a7d:1`: review content never comes from worker-writable shared objects; existence/type checks and replacement/graft suppression do not authenticate overwritten objects.
Use `<anchored-checkout>/.agents/worklog/local-review/` as the protected production storage parent; create each invocation's fresh mode-0700 object/worktree directory there, never under `${TMPDIR:-/tmp}` or other shared scratch.
Apply design 5.14 items 1/3 to the actual resolved parent, object store, worktree and artifact paths; reject worker-writable roots and symlink/case aliases. Mode 0700 is hygiene, not a same-UID write boundary.
Before production use, the orchestrator supplies installed-policy and actual denied-write evidence for Bash and file tools of each active worker kind against this parent; absent protection keeps review/reuse/integration held, not silently downgraded.
Create a fresh bare repository with `git init --bare <dir>`, then `git --git-dir=<dir> fetch https://github.com/mryfmo/dotfiles.git <head40> <base40>` on every invocation before any cache read.
Use only that explicit HTTPS source; prohibit remote-name/URL rewriting, local transport, alternates, `--reference`, `--shared`, copied objects and the shared `.git` as object sources; apply design 5.14 items 2/4/9 to all Git children.
Bind Git, gh, reviewer and required interpreters before checkout under design 5.14 items 2/3/4/9; execute those bindings and apply the same isolation and verified Git-only resolution to reviewer descendants, retaining Item 2's overrides.
Use fresh protected `GH_CONFIG_DIR` and read the token once with the bound gh's `auth token --hostname github.com` as in `.orchestration/tasks/dotfiles-T133-python-pin-a02.md` Commands (e)/(e'); isolate the fixed-host canonical-main request.
Never print/persist the token or pass it to Codex; canonical-main lookup and private fetch cannot be skipped by cached success.
Verify both exact full SHAs have type `commit` in the private repository, check out that exact head into its own worktree and verify HEAD; recompute head, canonical-main base and `git --git-dir=<dir> rev-parse <head40>^{tree}` there.
Store the artifact only at `<anchored-checkout>/.agents/worklog/local-review/<task>-local-review-<head40>.md`; shared/legacy artifacts, including ones with matching public head/base/tree, are never authoritative.
After fresh lookup/fetch/verification, a structurally valid protected artifact may skip only the model call when its single full `head:`, `base:` and `tree:` fields equal all three recomputed values and findings/counts agree.
Absent, legacy, malformed, duplicate-field, untrusted-location or mismatched artifacts require review in that private worktree and atomic replacement of the protected artifact after successful review; identifiers alone do not authenticate its producer.
On fetch failure emit `local-review: private fetch failed`; on missing/non-commit/mismatched head or base emit `local-review: private commit check failed`; exit 2, call no reviewer, create/rewrite no artifact and never fall back.
Remove only this invocation's private repository/worktree on completion/refusal; preserve failed-review transcripts and inherited exit-4 behavior without retaining reusable success for the failed invocation.
Change `chain-integrate.sh`'s actual review/advisory exec sites to establish design 5.14 item 2 before either child's shell/loader starts, using anchored script bindings; satisfy its own entry requirements under the orchestrator-controlled outer parent, with no self-reexec repair.
Add `tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1`: execute the actual changed caller/consumer path from the trusted fixture parent with hostile inherited startup/loader inputs; assert no payload/decoy execution, exact private handoff, exit 11 on private P1 despite legacy zero and no downstream sweep/audit.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects`: stub gh/git, plant forged shared-object content, serve different canonical content through explicit-URL private fetch, and make the reviewer read its actual cwd; assert consumed canonical content, isolated inputs and object provenance.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_refuses_a_failed_private_fetch_or_commit_check`: cover fetch failure and each missing/non-commit/mismatched head/base, with a matching private cache planted; assert named refusal, no reviewer, no artifact creation/rewrite and no fallback.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache`: plant matching shared head/findings-zero artifacts, also matching base/tree; assert fresh lookup/fetch, canonical-cwd review and protected rewrite.
That cache test proves lookup/fetch precede any cache read, valid protected head/base/tree skips only the model, changed/missing/duplicate metadata or inconsistent counts reruns it, and failed lookup/fetch cannot return cached success; it proves identity/rejection, not producer authenticity.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_rejects_shared_scratch_and_worker_private_roots` for shared TMPDIR, worker roots and aliases; fixtures prove path refusals only, never live worker write isolation.
Revise inherited tests that demand PATH-selected `mise which`, `command -v`/interpreter fallback or exactly two Codex overrides: assert design 5.14 items 4/9 bindings and an actually spawned Git's resolved executable/environment after Codex-policy filtering, including a shim/decoy attack.
Record each new regression red against `a644a7d9` on its security assertion, then green; separately disclose bootstrap-only fixture adaptations. Retain traversal, literal-path, shebang-argument/refusal, owner/repeat, output and failure regressions with safe fixtures.

## Check and Completion

Host facts: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
Run that uv resolve command as a host observation and paste actual output; bind validation operands under design 5.14 items 2/4/9, record interpreter realpath/version, and never guess an uv path or use the observation as production runtime discovery.
Run the bound uv/Python equivalents of `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` and `uv run python -m unittest tests/unit/test_chain_glue.py -v` under design 5.14 items 2/9; record complete actual argv/output/status.
Run `bash -n` on all three changed shell scripts, `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/chain-integrate.sh` and applicable repository lint; comments use English shdoc; never run Bats locally.
The whole PR has at most 120 changed lines outside `tests/` and `.orchestration/`, and 400 under `tests/`, counting additions plus deletions; attribute inherited 26 outside-test lines and 69 test lines separately from this reset's corrections, including caller edits.
Run `git --git-dir=<private-bare> diff --numstat <base40>...<head40>` in the authenticated private repository using resolved full SHAs and record complete output before cleanup.
The orchestrator pastes the resolved measurement base at dispatch; attribute inherited/new changes against that base and final head, including a branch-head base for any records-only round after update-branch; an overrun blocks, never raises caps.
Keep the complete dispatched text at or under 140 lines, reserving seven for Checks; no workflow, permission, dependency, launcher, knowledge-graph, predecessor-artifact or a09-owned changes are authorized.
Worker Playbook step 4 applies: every a013 command, including gh, Git and agmsg delivery, stays sandboxed; push without `-u` over HTTPS with `git push https://github.com/mryfmo/dotfiles.git tools/chain-review-scripts-followup-a07`; every denial records command/status/boundary and sends blocked PONG without escalation/substitution.
Do not probe the herdr socket; placement/delivery verification and host-deployment evidence belong to the orchestrator. Keep plan/todo/learn uncommitted and at most one active todo per owner.
Copy these complete dispatched bytes to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md`; keep the retained a07 task copy/evidence unchanged; no executable helper may be hidden in the artifact wildcard.
Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and `-worker-` crit-data/receipt evidence under the a08 directory; follow repository review gates without browser/human review, record provenance and `cost:`.
Each evidence item names `worker (Codex seat, a013)` or `orchestrator (Claude seat, sandboxed Bash)`; identify separate authoring/inherited producers honestly and include exact commands, operands, statuses, complete outputs and refusals without secrets.
Keep evidence untracked at the same relative paths in worker-h when main-checkout paths are inaccessible; RESULT identifies their location for orchestrator transfer.
This text's C-80 round 2 addresses supplied round 1; at most two C-80 text-review rounds total, no private third round. Keep INV-6/a07 counters and the one worker Bot fix-round limit; surviving P0/P1 goes to the operator.
After final push verify GitHub Actions and wait for final-head Bot feedback under the Worker Playbook; the worker proposes dispositions and resolves no threads.
RESULT names PR, full head/base, branch, changed files, selectors, red/green commits, caps/attribution, artifact paths and `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md>`.
The orchestrator records counters before acceptance, carries a07 history, then performs final-head sweep, task audit, security review, acceptance and gate in Playbook step 10 order; changed heads repeat required evidence; advisory ownership remains `dotfiles-T128-chain-review-scripts-followup-a09`.
Not performed by this authoring context: implementation edits, worker tests, live fetch, CI or deployment.
Shared credentials and unrestricted same-UID interference remain residual; fixture results cannot authorize production cache reuse or integration before the declared deployment prerequisites.

## Checks (pasted by the orchestrator before each send)


exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|task-level audit|threat.table' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; cat .ua/meta.json; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 60ms:
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
    12	  - scripts/orchestrator/chain-integrate.sh
    13	  - tests/unit/test_chain_glue.py
    14	after: []
    15	retained_predecessor_directories:
    16	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
    17	threat_table:
    18	  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success"}
    19	  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    20	  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; temporary fixtures assert consumed content, refusals and descendant bindings; audit checks sensitivity and retained behavioral regressions."}
    21	  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; records are untrusted evidence compared with dispatched bytes, diff and final-head CI; no runtime helpers."}
    22	  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1"}
    23	  - {control: "tests/unit/test_chain_glue.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fixtures exercise the actual caller and consumer; audit compares assertions with execution and stop behavior."}
    24	  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; compare whole-file bytes and dispatch SHA-256 at acceptance."}
    25	  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; preserve SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 and compare at acceptance."}
    26	  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; report, validation, sandbox, learning and autoskill records identify producers, commands, statuses, provenance and every refusal."}
    27	  - {control: "review-cache identity and shared-artifact rejection", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
    28	  - {control: "review-cache producer authenticity", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; head/base/tree are public identifiers, not producer authentication; production reuse is held until deployed write protection is evidenced."}
    29	  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; consistency checks before dispatch/acceptance and whole-file comparison detect changed metadata."}
    30	  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; parse front matter as data and compare complete bytes; evidence confers no execution authority."}
    31	  - {control: "in-process effects", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; private repositories and bound reviewers run under verified host prerequisites; fixtures never fetch live GitHub content."}
    32	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; this task binds the actual chain review call sites; complete host executable/input provisioning remains separately deployed."}
    33	  - {control: "new or renamed scripts", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none authorized; audit rejects undeclared helpers, wrappers or renames."}
    34	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; shared credentials and unrestricted same-UID processes remain outside prevention; missing acceptance is detected at the next records PR."}
    35	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; protected storage requires deployed Bash and file-tool boundaries for every active worker kind; mode 0700 alone proves none."}
    36	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed caller establishes child entry boundaries; orchestrator must supply the clean outer parent before chain shell/loader startup."}
    37	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; reject shared scratch, worker roots and aliases for production objects/artifacts; live boundary evidence remains mandatory."}
    38	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; use the same verified bindings/content without rediscovery; unrestricted same-UID replacement remains possible."}
    39	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fresh lookup/fetch precede full head/base/tree cache comparison; unique invocation roots introduce no reservation."}
    40	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; functional cache tests do not authenticate producers or prove live deployment, credentials, executable protection or reservations."}
    41	  - {control: "design 5.14 item 7: 検証", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; security-assertion red/green evidence covers source, cache, consumer and entry behavior, not the whole host contract."}
    42	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    43	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; fresh protected object stores and protected artifacts avoid shared caches; host executable/input provenance remains a deployment residual."}
    44	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; every Codex worker command remains sandboxed; denial produces blocked evidence without escalation."}
    45	  - {control: "orchestrator effect trusted-parent launch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; invoke the anchored chain under design 5.14 item 2 before its first executable; no direct inherited-environment launch or self-reexec."}
    46	  - {control: "orchestrator effect production release", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice5-a01; verify installed protection and activation before dispatch/live use; merge, after: [] and fixture success do not release dependents."}
    47	  - {control: "orchestrator effect cache commissioning", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; after verified deployment, commission empty protected storage and quarantine prior artifacts; only reviews produced after commissioning may authorize reuse."}
    48	  - {control: "orchestrator effect merge", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; only gh pr merge --squash --match-head-commit <audited head> after Playbook step 10; worker never merges or pushes main."}
    49	  - {control: "orchestrator effect update-branch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed head invalidates earlier CI, sweep, audit and security evidence; repeat before the gate."}
    50	  - {control: "orchestrator effect forced worker removal", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none planned; explicit force and acceptance recording of discarded state are required for dirty removal."}
    51	premises:
    52	  - {claim: "worker (Codex seat, review-profile authoring context): local continuation identity only; this does not authenticate content.", command: "git rev-parse --verify 'a644a7d9^{commit}'", output: "a644a7d965399b9463e9b32721287440a7efa233"}
    53	  - {claim: "worker (Codex seat, review-profile authoring context): predecessor copy matches dispatched a07 bytes.", command: "git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256", output: "b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -"}
    54	---
    55	
    56	# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content
    57	
    58	Independent-context reset after INV-6 S2 (two amendments including the erroneous resend; D-024-41); preserve a07 history in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md`.
    59	Continue PR #439, branch `tools/chain-review-scripts-followup-a07`, from `a644a7d965399b9463e9b32721287440a7efa233` with worker a013 (Codex, worker-h); create no branch or PR.
    60	Retain inherited code head `f5aaaf7e` except the corrections below; the two additional allowed paths authorize only C-80's actual caller/consumer binding and its regression, never a09's CI-wait or stale-comment rows.
    61	Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen (D-024-29), applies by reference (D-024-30), and its items 0–10 have individual threat rows; do not restate its contract.
    62	Read the whole a07 task, its acceptance, `.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md` and `.agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md`.
    63	Before dispatch, the orchestrator records deployed design 5.14 items 1–4/9 protection for every active worker kind, installed bindings and the clean outer chain launch; otherwise keep this task and PR held.
    64	P1-15's slice2 startup/administrative outputs and slice5 activation require actual deployment evidence; neither merge nor `after: []` establishes readiness. No worker deploys settings or invents an enforcement sentinel.
    65	After protection is verified, the trusted orchestrator commissions empty protected review storage, quarantines pre-existing artifacts and records that boundary/creation order; pre-deployment artifacts cannot become trusted by matching public identifiers.
    66	
    67	## Item 1
    68	
    69	The a06 record's `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` still has no rows; import none from a09.
    70	C-80 requires `local-advisory.sh` to consume the exact protected artifact produced by Item 3, with full head/base/tree identity, rather than the legacy shared `.orchestration/validation/<task>-local-review-<sha7>.md`.
    71	Have `chain-integrate.sh` hand that completed invocation's exact protected path and identities to the advisory consumer; validate containment, metadata and finding/count consistency before using it, and refuse missing, malformed or mismatched evidence with exit 2.
    72	Never default a missing count to zero or fall back to shared artifacts; retain P0/P1 exit 3, chain exit 11 and existing P2/P3 ownership/repeat semantics, reading prior review content only from protected full-head artifacts.
    73	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success`: a private P1 plus planted legacy zero must stop; missing/mismatched private evidence must refuse; retain positive advisory cases.
    74	
    75	## Item 2
    76	
    77	On every `local-review.sh` invocation, before any cache read, use the bound gh for `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; require successful exit and exactly 40 ASCII hexadecimal characters, otherwise a named exit-2 refusal.
    78	Neither local `main` nor `origin/main` selects the base; pass that exact SHA to `codex review --base`, with commit checks in Item 3's private store.
    79	Keep `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` exported and passed through `-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"'` and `-c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'`.
    80	Preserve failed-review refusal, full-head equality, finding/output behavior and inherited red/green provenance; revise unsafe executable-resolution expectations and cache trust/location as required below, without undoing implemented fixes to reproduce old reds.
    81	
    82	## Item 3
    83	
    84	Close `audit:a644a7d:1`: review content never comes from worker-writable shared objects; existence/type checks and replacement/graft suppression do not authenticate overwritten objects.
    85	Use `<anchored-checkout>/.agents/worklog/local-review/` as the protected production storage parent; create each invocation's fresh mode-0700 object/worktree directory there, never under `${TMPDIR:-/tmp}` or other shared scratch.
    86	Apply design 5.14 items 1/3 to the actual resolved parent, object store, worktree and artifact paths; reject worker-writable roots and symlink/case aliases. Mode 0700 is hygiene, not a same-UID write boundary.
    87	Before production use, the orchestrator supplies installed-policy and actual denied-write evidence for Bash and file tools of each active worker kind against this parent; absent protection keeps review/reuse/integration held, not silently downgraded.
    88	Create a fresh bare repository with `git init --bare <dir>`, then `git --git-dir=<dir> fetch https://github.com/mryfmo/dotfiles.git <head40> <base40>` on every invocation before any cache read.
    89	Use only that explicit HTTPS source; prohibit remote-name/URL rewriting, local transport, alternates, `--reference`, `--shared`, copied objects and the shared `.git` as object sources; apply design 5.14 items 2/4/9 to all Git children.
    90	Bind Git, gh, reviewer and required interpreters before checkout under design 5.14 items 2/3/4/9; execute those bindings and apply the same isolation and verified Git-only resolution to reviewer descendants, retaining Item 2's overrides.
    91	Use fresh protected `GH_CONFIG_DIR` and read the token once with the bound gh's `auth token --hostname github.com` as in `.orchestration/tasks/dotfiles-T133-python-pin-a02.md` Commands (e)/(e'); isolate the fixed-host canonical-main request.
    92	Never print/persist the token or pass it to Codex; canonical-main lookup and private fetch cannot be skipped by cached success.
    93	Verify both exact full SHAs have type `commit` in the private repository, check out that exact head into its own worktree and verify HEAD; recompute head, canonical-main base and `git --git-dir=<dir> rev-parse <head40>^{tree}` there.
    94	Store the artifact only at `<anchored-checkout>/.agents/worklog/local-review/<task>-local-review-<head40>.md`; shared/legacy artifacts, including ones with matching public head/base/tree, are never authoritative.
    95	After fresh lookup/fetch/verification, a structurally valid protected artifact may skip only the model call when its single full `head:`, `base:` and `tree:` fields equal all three recomputed values and findings/counts agree.
    96	Absent, legacy, malformed, duplicate-field, untrusted-location or mismatched artifacts require review in that private worktree and atomic replacement of the protected artifact after successful review; identifiers alone do not authenticate its producer.
    97	On fetch failure emit `local-review: private fetch failed`; on missing/non-commit/mismatched head or base emit `local-review: private commit check failed`; exit 2, call no reviewer, create/rewrite no artifact and never fall back.
    98	Remove only this invocation's private repository/worktree on completion/refusal; preserve failed-review transcripts and inherited exit-4 behavior without retaining reusable success for the failed invocation.
    99	Change `chain-integrate.sh`'s actual review/advisory exec sites to establish design 5.14 item 2 before either child's shell/loader starts, using anchored script bindings; satisfy its own entry requirements under the orchestrator-controlled outer parent, with no self-reexec repair.
   100	Add `tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1`: execute the actual changed caller/consumer path from the trusted fixture parent with hostile inherited startup/loader inputs; assert no payload/decoy execution, exact private handoff, exit 11 on private P1 despite legacy zero and no downstream sweep/audit.
   101	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects`: stub gh/git, plant forged shared-object content, serve different canonical content through explicit-URL private fetch, and make the reviewer read its actual cwd; assert consumed canonical content, isolated inputs and object provenance.
   102	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_refuses_a_failed_private_fetch_or_commit_check`: cover fetch failure and each missing/non-commit/mismatched head/base, with a matching private cache planted; assert named refusal, no reviewer, no artifact creation/rewrite and no fallback.
   103	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache`: plant matching shared head/findings-zero artifacts, also matching base/tree; assert fresh lookup/fetch, canonical-cwd review and protected rewrite.
   104	That cache test proves lookup/fetch precede any cache read, valid protected head/base/tree skips only the model, changed/missing/duplicate metadata or inconsistent counts reruns it, and failed lookup/fetch cannot return cached success; it proves identity/rejection, not producer authenticity.
   105	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_rejects_shared_scratch_and_worker_private_roots` for shared TMPDIR, worker roots and aliases; fixtures prove path refusals only, never live worker write isolation.
   106	Revise inherited tests that demand PATH-selected `mise which`, `command -v`/interpreter fallback or exactly two Codex overrides: assert design 5.14 items 4/9 bindings and an actually spawned Git's resolved executable/environment after Codex-policy filtering, including a shim/decoy attack.
   107	Record each new regression red against `a644a7d9` on its security assertion, then green; separately disclose bootstrap-only fixture adaptations. Retain traversal, literal-path, shebang-argument/refusal, owner/repeat, output and failure regressions with safe fixtures.
   108	
   109	## Check and Completion
   110	
   111	Host facts: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
   112	Run that uv resolve command as a host observation and paste actual output; bind validation operands under design 5.14 items 2/4/9, record interpreter realpath/version, and never guess an uv path or use the observation as production runtime discovery.
   113	Run the bound uv/Python equivalents of `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` and `uv run python -m unittest tests/unit/test_chain_glue.py -v` under design 5.14 items 2/9; record complete actual argv/output/status.
   114	Run `bash -n` on all three changed shell scripts, `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/chain-integrate.sh` and applicable repository lint; comments use English shdoc; never run Bats locally.
   115	The whole PR has at most 120 changed lines outside `tests/` and `.orchestration/`, and 400 under `tests/`, counting additions plus deletions; attribute inherited 26 outside-test lines and 69 test lines separately from this reset's corrections, including caller edits.
   116	Run `git --git-dir=<private-bare> diff --numstat <base40>...<head40>` in the authenticated private repository using resolved full SHAs and record complete output before cleanup.
   117	The orchestrator pastes the resolved measurement base at dispatch; attribute inherited/new changes against that base and final head, including a branch-head base for any records-only round after update-branch; an overrun blocks, never raises caps.
   118	Keep the complete dispatched text at or under 140 lines, reserving seven for Checks; no workflow, permission, dependency, launcher, knowledge-graph, predecessor-artifact or a09-owned changes are authorized.
   119	Worker Playbook step 4 applies: every a013 command, including gh, Git and agmsg delivery, stays sandboxed; push without `-u` over HTTPS with `git push https://github.com/mryfmo/dotfiles.git tools/chain-review-scripts-followup-a07`; every denial records command/status/boundary and sends blocked PONG without escalation/substitution.
   120	Do not probe the herdr socket; placement/delivery verification and host-deployment evidence belong to the orchestrator. Keep plan/todo/learn uncommitted and at most one active todo per owner.
   121	Copy these complete dispatched bytes to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md`; keep the retained a07 task copy/evidence unchanged; no executable helper may be hidden in the artifact wildcard.
   122	Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and `-worker-` crit-data/receipt evidence under the a08 directory; follow repository review gates without browser/human review, record provenance and `cost:`.
   123	Each evidence item names `worker (Codex seat, a013)` or `orchestrator (Claude seat, sandboxed Bash)`; identify separate authoring/inherited producers honestly and include exact commands, operands, statuses, complete outputs and refusals without secrets.
   124	Keep evidence untracked at the same relative paths in worker-h when main-checkout paths are inaccessible; RESULT identifies their location for orchestrator transfer.
   125	This text's C-80 round 2 addresses supplied round 1; at most two C-80 text-review rounds total, no private third round. Keep INV-6/a07 counters and the one worker Bot fix-round limit; surviving P0/P1 goes to the operator.
   126	After final push verify GitHub Actions and wait for final-head Bot feedback under the Worker Playbook; the worker proposes dispositions and resolves no threads.
   127	RESULT names PR, full head/base, branch, changed files, selectors, red/green commits, caps/attribution, artifact paths and `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md>`.
   128	The orchestrator records counters before acceptance, carries a07 history, then performs final-head sweep, task audit, security review, acceptance and gate in Playbook step 10 order; changed heads repeat required evidence; advisory ownership remains `dotfiles-T128-chain-review-scripts-followup-a09`.
   129	Not performed by this authoring context: implementation edits, worker tests, live fetch, CI or deployment.
   130	Shared credentials and unrestricted same-UID interference remain residual; fixture results cannot authorize production cache reuse or integration before the declared deployment prerequisites.
   131	
   132	## Checks (pasted by the orchestrator before each send)
   133	

 succeeded in 109ms:
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
67:- Only acceptance decisions and final merge stay orchestrator-side. Seats and scripts handle integration, adversarial RESULT review, review-profile work, gate and records through `verdict.sh`, `audit-pool.sh`, `result-precheck.sh`, `acceptance-front-matter.py` and `dispatch.sh --next`. Pending each mechanism, Delegation's interim exemption permits manual orchestrator execution. Every code-changing RESULT gets one task-level audit of its final head; findings are input, never approval (the "Task-level audit" bullet).
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
178:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
181:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
182:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
225:## Codex seat worklogs
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

 succeeded in 164ms:
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
 M .orchestration/tasks/dotfiles-T133-pre-send-check-a02.md
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
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-chain-08b8add.log
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
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
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

**Requesting plain text output**
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md; cat .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '225,263p' ~/.agents/skills/agmsg-orchestration/SKILL.md; rg -n '5\\.14|5\\.15' .orchestration/plans/024-design-quality.md; cat .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md; cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md; cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md; rg -n '"'^##|'"\\(e\\)|\\(e.\\)' .orchestration/tasks/dotfiles-T133-python-pin-a02.md" in ~/Workspace/dotfiles
 succeeded in 113ms:
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
# Notes every review-profile brief carries (orchestrator glue, 2026-10-20)

1. Host facts measured before authoring, pasted verbatim: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`. A text names a resolve command and asks the worker to paste its output, never a guessed path (re-plan validation-setup of regime-ci-token-a01).
2. Every evidence item names its producer and seat kind: `orchestrator (Claude seat, sandboxed Bash)` or `worker (<kind> seat)`. A Codex seat cannot probe the herdr socket from its sandbox (PermissionDenied measured 2026-10-20T13:39Z, a013); never ask it to (M-20261020-06/08 class).
3. The self cap leaves room for the orchestrator's Checks block (about 7 lines) when the text keeps a fenced block under `## Checks`; a reset text anchored by a review is dispatched at the anchored bytes with no paste.
4. No restatement of the trusted-execution contract: design 5.14 items by reference; environment and executable rows the tool cannot close are `residual` with an owner (re-plan contract-restatement of regime-ci-token-a01). Texts for security: false tools get no C-80 (D-024-46).
5. Caps in the C-107 sentence form; the numstat command in its own sentence; measurement base pasted at dispatch (the branch head at dispatch for a records-only round after an update-branch, not an older code head).
6. Baseline statements bind to the post-prerequisite state: a text that names `after:` prerequisites describes main as it will be after they merge (their post-merge effects stated in the brief), never as it is on the authoring day (slice 1 of P1-15, 2026-10-21: an old Linux exclusion policy was preserved against a prerequisite that empties it).


 succeeded in 171ms:
[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:65 Keeping `local-advisory.sh` unchanged disconnects enforcement from the reviewed artifact: it still reads `.orchestration/validation/<task>-local-review-<sha7>.md`, whereas Item 3 writes a private full-head filename; when the new review returns P1 findings, a planted legacy `findings: 0` makes the advisory consumer return success and lets `chain-integrate.sh` continue.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:77 A mode-0700 directory under `${TMPDIR:-/tmp}` does not establish a worker-inaccessible object store: same-UID workers with access to that temporary root can modify it, and item 3’s worker-root/symlink/case checks do not exclude shared scratch space; replacement after fetch can therefore change the content consumed by the reviewer, while the named stub test establishes no write boundary.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:23 Cache provenance cannot be `closed` while line 30 acknowledges unenforced Claude file-tool protection and `after: []` imposes no deployment prerequisite: a worker can forge an anchored-cache artifact containing the publicly computable head/base/tree and `findings: 0`; fresh canonical lookup and fetch validate those identifiers, not who produced the review.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:31 Referencing a trusted-parent contract does not supply a trusted caller: `chain-integrate.sh:143` directly executes the script with inherited environment, and neither this task nor the named binding owner authorizes changing that caller; `BASH_ENV` or Linux loader injection can execute before child sanitization, including before an unsandboxed gh invocation, so clean Git/gh children cannot compensate for the missing entry boundary.

[P2] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:92 Preserving every inherited regression conflicts with the required executable binding: the inherited tests explicitly require PATH-selected `mise which` calls and interpreter fallback, while design §5.14 item 9 prohibits both; they also require exactly two Codex environment overrides despite the configured reviewer PATH containing mise shims, so these assertions must be revised to verify the actual descendant Git binding.

📝 まとめ: タスク本文と参照記録を読み取り専用で審査し、実行・成果物の結び付けと保護前提に5件の指摘を確認しました。
Not checked: implementation, live sandbox enforcement, or test execution; the stated controls do not yet establish the claimed boundaries.
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
session id: 01a15cd0-1ab2-7c01-b820-8e59d99a8360
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
実装前の設計として、task 本文・threat_table・参照された acceptance/review を読み、判断した対象と実行対象が一致するかを確認します。agmsg-orchestration と Ponytail のレビュー手順を参照し、読み取り専用で進めます。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 2ms:
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
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
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
/bin/zsh -lc 'git status --short; git rev-parse HEAD; cat .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md' in ~/Workspace/dotfiles
 succeeded in 17ms:
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
 M .orchestration/tasks/dotfiles-T133-pre-send-check-a02.md
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
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-chain-08b8add.log
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
---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a08
reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]
kind: code
security: true
allowed_files:
  - scripts/orchestrator/local-advisory.sh
  - scripts/orchestrator/local-review.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**
  - scripts/orchestrator/chain-integrate.sh
  - tests/unit/test_chain_glue.py
after: []
retained_predecessor_directories:
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
threat_table:
  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success"}
  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; temporary fixtures assert consumed content, refusals and descendant bindings; audit checks sensitivity and retained behavioral regressions."}
  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; records are untrusted evidence compared with dispatched bytes, diff and final-head CI; no runtime helpers."}
  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1"}
  - {control: "tests/unit/test_chain_glue.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fixtures exercise the actual caller and consumer; audit compares assertions with execution and stop behavior."}
  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; compare whole-file bytes and dispatch SHA-256 at acceptance."}
  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; preserve SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 and compare at acceptance."}
  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; report, validation, sandbox, learning and autoskill records identify producers, commands, statuses, provenance and every refusal."}
  - {control: "review-cache identity and shared-artifact rejection", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
  - {control: "review-cache producer authenticity", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; head/base/tree are public identifiers, not producer authentication; production reuse is held until deployed write protection is evidenced."}
  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; consistency checks before dispatch/acceptance and whole-file comparison detect changed metadata."}
  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; parse front matter as data and compare complete bytes; evidence confers no execution authority."}
  - {control: "in-process effects", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; private repositories and bound reviewers run under verified host prerequisites; fixtures never fetch live GitHub content."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; this task binds the actual chain review call sites; complete host executable/input provisioning remains separately deployed."}
  - {control: "new or renamed scripts", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none authorized; audit rejects undeclared helpers, wrappers or renames."}
  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; shared credentials and unrestricted same-UID processes remain outside prevention; missing acceptance is detected at the next records PR."}
  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; protected storage requires deployed Bash and file-tool boundaries for every active worker kind; mode 0700 alone proves none."}
  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed caller establishes child entry boundaries; orchestrator must supply the clean outer parent before chain shell/loader startup."}
  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; reject shared scratch, worker roots and aliases for production objects/artifacts; live boundary evidence remains mandatory."}
  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; use the same verified bindings/content without rediscovery; unrestricted same-UID replacement remains possible."}
  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fresh lookup/fetch precede full head/base/tree cache comparison; unique invocation roots introduce no reservation."}
  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; functional cache tests do not authenticate producers or prove live deployment, credentials, executable protection or reservations."}
  - {control: "design 5.14 item 7: 検証", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; security-assertion red/green evidence covers source, cache, consumer and entry behavior, not the whole host contract."}
  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; fresh protected object stores and protected artifacts avoid shared caches; host executable/input provenance remains a deployment residual."}
  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; every Codex worker command remains sandboxed; denial produces blocked evidence without escalation."}
  - {control: "orchestrator effect trusted-parent launch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; invoke the anchored chain under design 5.14 item 2 before its first executable; no direct inherited-environment launch or self-reexec."}
  - {control: "orchestrator effect production release", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice5-a01; verify installed protection and activation before dispatch/live use; merge, after: [] and fixture success do not release dependents."}
  - {control: "orchestrator effect cache commissioning", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; after verified deployment, commission empty protected storage and quarantine prior artifacts; only reviews produced after commissioning may authorize reuse."}
  - {control: "orchestrator effect merge", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; only gh pr merge --squash --match-head-commit <audited head> after Playbook step 10; worker never merges or pushes main."}
  - {control: "orchestrator effect update-branch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed head invalidates earlier CI, sweep, audit and security evidence; repeat before the gate."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none planned; explicit force and acceptance recording of discarded state are required for dirty removal."}
premises:
  - {claim: "worker (Codex seat, review-profile authoring context): local continuation identity only; this does not authenticate content.", command: "git rev-parse --verify 'a644a7d9^{commit}'", output: "a644a7d965399b9463e9b32721287440a7efa233"}
  - {claim: "worker (Codex seat, review-profile authoring context): predecessor copy matches dispatched a07 bytes.", command: "git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256", output: "b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -"}
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content

Independent-context reset after INV-6 S2 (two amendments including the erroneous resend; D-024-41); preserve a07 history in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md`.
Continue PR #439, branch `tools/chain-review-scripts-followup-a07`, from `a644a7d965399b9463e9b32721287440a7efa233` with worker a013 (Codex, worker-h); create no branch or PR.
Retain inherited code head `f5aaaf7e` except the corrections below; the two additional allowed paths authorize only C-80's actual caller/consumer binding and its regression, never a09's CI-wait or stale-comment rows.
Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen (D-024-29), applies by reference (D-024-30), and its items 0–10 have individual threat rows; do not restate its contract.
Read the whole a07 task, its acceptance, `.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md` and `.agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md`.
Before dispatch, the orchestrator records deployed design 5.14 items 1–4/9 protection for every active worker kind, installed bindings and the clean outer chain launch; otherwise keep this task and PR held.
P1-15's slice2 startup/administrative outputs and slice5 activation require actual deployment evidence; neither merge nor `after: []` establishes readiness. No worker deploys settings or invents an enforcement sentinel.
After protection is verified, the trusted orchestrator commissions empty protected review storage, quarantines pre-existing artifacts and records that boundary/creation order; pre-deployment artifacts cannot become trusted by matching public identifiers.

## Item 1

The a06 record's `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` still has no rows; import none from a09.
C-80 requires `local-advisory.sh` to consume the exact protected artifact produced by Item 3, with full head/base/tree identity, rather than the legacy shared `.orchestration/validation/<task>-local-review-<sha7>.md`.
Have `chain-integrate.sh` hand that completed invocation's exact protected path and identities to the advisory consumer; validate containment, metadata and finding/count consistency before using it, and refuse missing, malformed or mismatched evidence with exit 2.
Never default a missing count to zero or fall back to shared artifacts; retain P0/P1 exit 3, chain exit 11 and existing P2/P3 ownership/repeat semantics, reading prior review content only from protected full-head artifacts.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success`: a private P1 plus planted legacy zero must stop; missing/mismatched private evidence must refuse; retain positive advisory cases.

## Item 2

On every `local-review.sh` invocation, before any cache read, use the bound gh for `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; require successful exit and exactly 40 ASCII hexadecimal characters, otherwise a named exit-2 refusal.
Neither local `main` nor `origin/main` selects the base; pass that exact SHA to `codex review --base`, with commit checks in Item 3's private store.
Keep `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` exported and passed through `-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"'` and `-c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'`.
Preserve failed-review refusal, full-head equality, finding/output behavior and inherited red/green provenance; revise unsafe executable-resolution expectations and cache trust/location as required below, without undoing implemented fixes to reproduce old reds.

## Item 3

Close `audit:a644a7d:1`: review content never comes from worker-writable shared objects; existence/type checks and replacement/graft suppression do not authenticate overwritten objects.
Use `<anchored-checkout>/.agents/worklog/local-review/` as the protected production storage parent; create each invocation's fresh mode-0700 object/worktree directory there, never under `${TMPDIR:-/tmp}` or other shared scratch.
Apply design 5.14 items 1/3 to the actual resolved parent, object store, worktree and artifact paths; reject worker-writable roots and symlink/case aliases. Mode 0700 is hygiene, not a same-UID write boundary.
Before production use, the orchestrator supplies installed-policy and actual denied-write evidence for Bash and file tools of each active worker kind against this parent; absent protection keeps review/reuse/integration held, not silently downgraded.
Create a fresh bare repository with `git init --bare <dir>`, then `git --git-dir=<dir> fetch https://github.com/mryfmo/dotfiles.git <head40> <base40>` on every invocation before any cache read.
Use only that explicit HTTPS source; prohibit remote-name/URL rewriting, local transport, alternates, `--reference`, `--shared`, copied objects and the shared `.git` as object sources; apply design 5.14 items 2/4/9 to all Git children.
Bind Git, gh, reviewer and required interpreters before checkout under design 5.14 items 2/3/4/9; execute those bindings and apply the same isolation and verified Git-only resolution to reviewer descendants, retaining Item 2's overrides.
Use fresh protected `GH_CONFIG_DIR` and read the token once with the bound gh's `auth token --hostname github.com` as in `.orchestration/tasks/dotfiles-T133-python-pin-a02.md` Commands (e)/(e'); isolate the fixed-host canonical-main request.
Never print/persist the token or pass it to Codex; canonical-main lookup and private fetch cannot be skipped by cached success.
Verify both exact full SHAs have type `commit` in the private repository, check out that exact head into its own worktree and verify HEAD; recompute head, canonical-main base and `git --git-dir=<dir> rev-parse <head40>^{tree}` there.
Store the artifact only at `<anchored-checkout>/.agents/worklog/local-review/<task>-local-review-<head40>.md`; shared/legacy artifacts, including ones with matching public head/base/tree, are never authoritative.
After fresh lookup/fetch/verification, a structurally valid protected artifact may skip only the model call when its single full `head:`, `base:` and `tree:` fields equal all three recomputed values and findings/counts agree.
Absent, legacy, malformed, duplicate-field, untrusted-location or mismatched artifacts require review in that private worktree and atomic replacement of the protected artifact after successful review; identifiers alone do not authenticate its producer.
On fetch failure emit `local-review: private fetch failed`; on missing/non-commit/mismatched head or base emit `local-review: private commit check failed`; exit 2, call no reviewer, create/rewrite no artifact and never fall back.
Remove only this invocation's private repository/worktree on completion/refusal; preserve failed-review transcripts and inherited exit-4 behavior without retaining reusable success for the failed invocation.
Change `chain-integrate.sh`'s actual review/advisory exec sites to establish design 5.14 item 2 before either child's shell/loader starts, using anchored script bindings; satisfy its own entry requirements under the orchestrator-controlled outer parent, with no self-reexec repair.
Add `tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1`: execute the actual changed caller/consumer path from the trusted fixture parent with hostile inherited startup/loader inputs; assert no payload/decoy execution, exact private handoff, exit 11 on private P1 despite legacy zero and no downstream sweep/audit.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects`: stub gh/git, plant forged shared-object content, serve different canonical content through explicit-URL private fetch, and make the reviewer read its actual cwd; assert consumed canonical content, isolated inputs and object provenance.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_refuses_a_failed_private_fetch_or_commit_check`: cover fetch failure and each missing/non-commit/mismatched head/base, with a matching private cache planted; assert named refusal, no reviewer, no artifact creation/rewrite and no fallback.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache`: plant matching shared head/findings-zero artifacts, also matching base/tree; assert fresh lookup/fetch, canonical-cwd review and protected rewrite.
That cache test proves lookup/fetch precede any cache read, valid protected head/base/tree skips only the model, changed/missing/duplicate metadata or inconsistent counts reruns it, and failed lookup/fetch cannot return cached success; it proves identity/rejection, not producer authenticity.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_rejects_shared_scratch_and_worker_private_roots` for shared TMPDIR, worker roots and aliases; fixtures prove path refusals only, never live worker write isolation.
Revise inherited tests that demand PATH-selected `mise which`, `command -v`/interpreter fallback or exactly two Codex overrides: assert design 5.14 items 4/9 bindings and an actually spawned Git's resolved executable/environment after Codex-policy filtering, including a shim/decoy attack.
Record each new regression red against `a644a7d9` on its security assertion, then green; separately disclose bootstrap-only fixture adaptations. Retain traversal, literal-path, shebang-argument/refusal, owner/repeat, output and failure regressions with safe fixtures.

## Check and Completion

Host facts: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
Run that uv resolve command as a host observation and paste actual output; bind validation operands under design 5.14 items 2/4/9, record interpreter realpath/version, and never guess an uv path or use the observation as production runtime discovery.
Run the bound uv/Python equivalents of `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` and `uv run python -m unittest tests/unit/test_chain_glue.py -v` under design 5.14 items 2/9; record complete actual argv/output/status.
Run `bash -n` on all three changed shell scripts, `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/chain-integrate.sh` and applicable repository lint; comments use English shdoc; never run Bats locally.
The whole PR has at most 120 changed lines outside `tests/` and `.orchestration/`, and 400 under `tests/`, counting additions plus deletions; attribute inherited 26 outside-test lines and 69 test lines separately from this reset's corrections, including caller edits.
Run `git --git-dir=<private-bare> diff --numstat <base40>...<head40>` in the authenticated private repository using resolved full SHAs and record complete output before cleanup.
The orchestrator pastes the resolved measurement base at dispatch; attribute inherited/new changes against that base and final head, including a branch-head base for any records-only round after update-branch; an overrun blocks, never raises caps.
Keep the complete dispatched text at or under 140 lines, reserving seven for Checks; no workflow, permission, dependency, launcher, knowledge-graph, predecessor-artifact or a09-owned changes are authorized.
Worker Playbook step 4 applies: every a013 command, including gh, Git and agmsg delivery, stays sandboxed; push without `-u` over HTTPS with `git push https://github.com/mryfmo/dotfiles.git tools/chain-review-scripts-followup-a07`; every denial records command/status/boundary and sends blocked PONG without escalation/substitution.
Do not probe the herdr socket; placement/delivery verification and host-deployment evidence belong to the orchestrator. Keep plan/todo/learn uncommitted and at most one active todo per owner.
Copy these complete dispatched bytes to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md`; keep the retained a07 task copy/evidence unchanged; no executable helper may be hidden in the artifact wildcard.
Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and `-worker-` crit-data/receipt evidence under the a08 directory; follow repository review gates without browser/human review, record provenance and `cost:`.
Each evidence item names `worker (Codex seat, a013)` or `orchestrator (Claude seat, sandboxed Bash)`; identify separate authoring/inherited producers honestly and include exact commands, operands, statuses, complete outputs and refusals without secrets.
Keep evidence untracked at the same relative paths in worker-h when main-checkout paths are inaccessible; RESULT identifies their location for orchestrator transfer.
This text's C-80 round 2 addresses supplied round 1; at most two C-80 text-review rounds total, no private third round. Keep INV-6/a07 counters and the one worker Bot fix-round limit; surviving P0/P1 goes to the operator.
After final push verify GitHub Actions and wait for final-head Bot feedback under the Worker Playbook; the worker proposes dispositions and resolves no threads.
RESULT names PR, full head/base, branch, changed files, selectors, red/green commits, caps/attribution, artifact paths and `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md>`.
The orchestrator records counters before acceptance, carries a07 history, then performs final-head sweep, task audit, security review, acceptance and gate in Playbook step 10 order; changed heads repeat required evidence; advisory ownership remains `dotfiles-T128-chain-review-scripts-followup-a09`.
Not performed by this authoring context: implementation edits, worker tests, live fetch, CI or deployment.
Shared credentials and unrestricted same-UID interference remain residual; fixture results cannot authorize production cache reuse or integration before the declared deployment prerequisites.

## Checks (pasted by the orchestrator before each send)


exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|task-level audit|threat.table' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; cat .ua/meta.json; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 60ms:
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
    12	  - scripts/orchestrator/chain-integrate.sh
    13	  - tests/unit/test_chain_glue.py
    14	after: []
    15	retained_predecessor_directories:
    16	  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
    17	threat_table:
    18	  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success"}
    19	  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    20	  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; temporary fixtures assert consumed content, refusals and descendant bindings; audit checks sensitivity and retained behavioral regressions."}
    21	  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; records are untrusted evidence compared with dispatched bytes, diff and final-head CI; no runtime helpers."}
    22	  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1"}
    23	  - {control: "tests/unit/test_chain_glue.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fixtures exercise the actual caller and consumer; audit compares assertions with execution and stop behavior."}
    24	  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; compare whole-file bytes and dispatch SHA-256 at acceptance."}
    25	  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; preserve SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 and compare at acceptance."}
    26	  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; report, validation, sandbox, learning and autoskill records identify producers, commands, statuses, provenance and every refusal."}
    27	  - {control: "review-cache identity and shared-artifact rejection", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
    28	  - {control: "review-cache producer authenticity", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; head/base/tree are public identifiers, not producer authentication; production reuse is held until deployed write protection is evidenced."}
    29	  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; consistency checks before dispatch/acceptance and whole-file comparison detect changed metadata."}
    30	  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; parse front matter as data and compare complete bytes; evidence confers no execution authority."}
    31	  - {control: "in-process effects", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; private repositories and bound reviewers run under verified host prerequisites; fixtures never fetch live GitHub content."}
    32	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; this task binds the actual chain review call sites; complete host executable/input provisioning remains separately deployed."}
    33	  - {control: "new or renamed scripts", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none authorized; audit rejects undeclared helpers, wrappers or renames."}
    34	  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; shared credentials and unrestricted same-UID processes remain outside prevention; missing acceptance is detected at the next records PR."}
    35	  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; protected storage requires deployed Bash and file-tool boundaries for every active worker kind; mode 0700 alone proves none."}
    36	  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed caller establishes child entry boundaries; orchestrator must supply the clean outer parent before chain shell/loader startup."}
    37	  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; reject shared scratch, worker roots and aliases for production objects/artifacts; live boundary evidence remains mandatory."}
    38	  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; use the same verified bindings/content without rediscovery; unrestricted same-UID replacement remains possible."}
    39	  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fresh lookup/fetch precede full head/base/tree cache comparison; unique invocation roots introduce no reservation."}
    40	  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; functional cache tests do not authenticate producers or prove live deployment, credentials, executable protection or reservations."}
    41	  - {control: "design 5.14 item 7: 検証", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; security-assertion red/green evidence covers source, cache, consumer and entry behavior, not the whole host contract."}
    42	  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
    43	  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; fresh protected object stores and protected artifacts avoid shared caches; host executable/input provenance remains a deployment residual."}
    44	  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; every Codex worker command remains sandboxed; denial produces blocked evidence without escalation."}
    45	  - {control: "orchestrator effect trusted-parent launch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; invoke the anchored chain under design 5.14 item 2 before its first executable; no direct inherited-environment launch or self-reexec."}
    46	  - {control: "orchestrator effect production release", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice5-a01; verify installed protection and activation before dispatch/live use; merge, after: [] and fixture success do not release dependents."}
    47	  - {control: "orchestrator effect cache commissioning", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; after verified deployment, commission empty protected storage and quarantine prior artifacts; only reviews produced after commissioning may authorize reuse."}
    48	  - {control: "orchestrator effect merge", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; only gh pr merge --squash --match-head-commit <audited head> after Playbook step 10; worker never merges or pushes main."}
    49	  - {control: "orchestrator effect update-branch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed head invalidates earlier CI, sweep, audit and security evidence; repeat before the gate."}
    50	  - {control: "orchestrator effect forced worker removal", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none planned; explicit force and acceptance recording of discarded state are required for dirty removal."}
    51	premises:
    52	  - {claim: "worker (Codex seat, review-profile authoring context): local continuation identity only; this does not authenticate content.", command: "git rev-parse --verify 'a644a7d9^{commit}'", output: "a644a7d965399b9463e9b32721287440a7efa233"}
    53	  - {claim: "worker (Codex seat, review-profile authoring context): predecessor copy matches dispatched a07 bytes.", command: "git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256", output: "b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -"}
    54	---
    55	
    56	# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content
    57	
    58	Independent-context reset after INV-6 S2 (two amendments including the erroneous resend; D-024-41); preserve a07 history in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md`.
    59	Continue PR #439, branch `tools/chain-review-scripts-followup-a07`, from `a644a7d965399b9463e9b32721287440a7efa233` with worker a013 (Codex, worker-h); create no branch or PR.
    60	Retain inherited code head `f5aaaf7e` except the corrections below; the two additional allowed paths authorize only C-80's actual caller/consumer binding and its regression, never a09's CI-wait or stale-comment rows.
    61	Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen (D-024-29), applies by reference (D-024-30), and its items 0–10 have individual threat rows; do not restate its contract.
    62	Read the whole a07 task, its acceptance, `.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md` and `.agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md`.
    63	Before dispatch, the orchestrator records deployed design 5.14 items 1–4/9 protection for every active worker kind, installed bindings and the clean outer chain launch; otherwise keep this task and PR held.
    64	P1-15's slice2 startup/administrative outputs and slice5 activation require actual deployment evidence; neither merge nor `after: []` establishes readiness. No worker deploys settings or invents an enforcement sentinel.
    65	After protection is verified, the trusted orchestrator commissions empty protected review storage, quarantines pre-existing artifacts and records that boundary/creation order; pre-deployment artifacts cannot become trusted by matching public identifiers.
    66	
    67	## Item 1
    68	
    69	The a06 record's `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` still has no rows; import none from a09.
    70	C-80 requires `local-advisory.sh` to consume the exact protected artifact produced by Item 3, with full head/base/tree identity, rather than the legacy shared `.orchestration/validation/<task>-local-review-<sha7>.md`.
    71	Have `chain-integrate.sh` hand that completed invocation's exact protected path and identities to the advisory consumer; validate containment, metadata and finding/count consistency before using it, and refuse missing, malformed or mismatched evidence with exit 2.
    72	Never default a missing count to zero or fall back to shared artifacts; retain P0/P1 exit 3, chain exit 11 and existing P2/P3 ownership/repeat semantics, reading prior review content only from protected full-head artifacts.
    73	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success`: a private P1 plus planted legacy zero must stop; missing/mismatched private evidence must refuse; retain positive advisory cases.
    74	
    75	## Item 2
    76	
    77	On every `local-review.sh` invocation, before any cache read, use the bound gh for `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; require successful exit and exactly 40 ASCII hexadecimal characters, otherwise a named exit-2 refusal.
    78	Neither local `main` nor `origin/main` selects the base; pass that exact SHA to `codex review --base`, with commit checks in Item 3's private store.
    79	Keep `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` exported and passed through `-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"'` and `-c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'`.
    80	Preserve failed-review refusal, full-head equality, finding/output behavior and inherited red/green provenance; revise unsafe executable-resolution expectations and cache trust/location as required below, without undoing implemented fixes to reproduce old reds.
    81	
    82	## Item 3
    83	
    84	Close `audit:a644a7d:1`: review content never comes from worker-writable shared objects; existence/type checks and replacement/graft suppression do not authenticate overwritten objects.
    85	Use `<anchored-checkout>/.agents/worklog/local-review/` as the protected production storage parent; create each invocation's fresh mode-0700 object/worktree directory there, never under `${TMPDIR:-/tmp}` or other shared scratch.
    86	Apply design 5.14 items 1/3 to the actual resolved parent, object store, worktree and artifact paths; reject worker-writable roots and symlink/case aliases. Mode 0700 is hygiene, not a same-UID write boundary.
    87	Before production use, the orchestrator supplies installed-policy and actual denied-write evidence for Bash and file tools of each active worker kind against this parent; absent protection keeps review/reuse/integration held, not silently downgraded.
    88	Create a fresh bare repository with `git init --bare <dir>`, then `git --git-dir=<dir> fetch https://github.com/mryfmo/dotfiles.git <head40> <base40>` on every invocation before any cache read.
    89	Use only that explicit HTTPS source; prohibit remote-name/URL rewriting, local transport, alternates, `--reference`, `--shared`, copied objects and the shared `.git` as object sources; apply design 5.14 items 2/4/9 to all Git children.
    90	Bind Git, gh, reviewer and required interpreters before checkout under design 5.14 items 2/3/4/9; execute those bindings and apply the same isolation and verified Git-only resolution to reviewer descendants, retaining Item 2's overrides.
    91	Use fresh protected `GH_CONFIG_DIR` and read the token once with the bound gh's `auth token --hostname github.com` as in `.orchestration/tasks/dotfiles-T133-python-pin-a02.md` Commands (e)/(e'); isolate the fixed-host canonical-main request.
    92	Never print/persist the token or pass it to Codex; canonical-main lookup and private fetch cannot be skipped by cached success.
    93	Verify both exact full SHAs have type `commit` in the private repository, check out that exact head into its own worktree and verify HEAD; recompute head, canonical-main base and `git --git-dir=<dir> rev-parse <head40>^{tree}` there.
    94	Store the artifact only at `<anchored-checkout>/.agents/worklog/local-review/<task>-local-review-<head40>.md`; shared/legacy artifacts, including ones with matching public head/base/tree, are never authoritative.
    95	After fresh lookup/fetch/verification, a structurally valid protected artifact may skip only the model call when its single full `head:`, `base:` and `tree:` fields equal all three recomputed values and findings/counts agree.
    96	Absent, legacy, malformed, duplicate-field, untrusted-location or mismatched artifacts require review in that private worktree and atomic replacement of the protected artifact after successful review; identifiers alone do not authenticate its producer.
    97	On fetch failure emit `local-review: private fetch failed`; on missing/non-commit/mismatched head or base emit `local-review: private commit check failed`; exit 2, call no reviewer, create/rewrite no artifact and never fall back.
    98	Remove only this invocation's private repository/worktree on completion/refusal; preserve failed-review transcripts and inherited exit-4 behavior without retaining reusable success for the failed invocation.
    99	Change `chain-integrate.sh`'s actual review/advisory exec sites to establish design 5.14 item 2 before either child's shell/loader starts, using anchored script bindings; satisfy its own entry requirements under the orchestrator-controlled outer parent, with no self-reexec repair.
   100	Add `tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1`: execute the actual changed caller/consumer path from the trusted fixture parent with hostile inherited startup/loader inputs; assert no payload/decoy execution, exact private handoff, exit 11 on private P1 despite legacy zero and no downstream sweep/audit.
   101	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects`: stub gh/git, plant forged shared-object content, serve different canonical content through explicit-URL private fetch, and make the reviewer read its actual cwd; assert consumed canonical content, isolated inputs and object provenance.
   102	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_refuses_a_failed_private_fetch_or_commit_check`: cover fetch failure and each missing/non-commit/mismatched head/base, with a matching private cache planted; assert named refusal, no reviewer, no artifact creation/rewrite and no fallback.
   103	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache`: plant matching shared head/findings-zero artifacts, also matching base/tree; assert fresh lookup/fetch, canonical-cwd review and protected rewrite.
   104	That cache test proves lookup/fetch precede any cache read, valid protected head/base/tree skips only the model, changed/missing/duplicate metadata or inconsistent counts reruns it, and failed lookup/fetch cannot return cached success; it proves identity/rejection, not producer authenticity.
   105	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_rejects_shared_scratch_and_worker_private_roots` for shared TMPDIR, worker roots and aliases; fixtures prove path refusals only, never live worker write isolation.
   106	Revise inherited tests that demand PATH-selected `mise which`, `command -v`/interpreter fallback or exactly two Codex overrides: assert design 5.14 items 4/9 bindings and an actually spawned Git's resolved executable/environment after Codex-policy filtering, including a shim/decoy attack.
   107	Record each new regression red against `a644a7d9` on its security assertion, then green; separately disclose bootstrap-only fixture adaptations. Retain traversal, literal-path, shebang-argument/refusal, owner/repeat, output and failure regressions with safe fixtures.
   108	
   109	## Check and Completion
   110	
   111	Host facts: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
   112	Run that uv resolve command as a host observation and paste actual output; bind validation operands under design 5.14 items 2/4/9, record interpreter realpath/version, and never guess an uv path or use the observation as production runtime discovery.
   113	Run the bound uv/Python equivalents of `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` and `uv run python -m unittest tests/unit/test_chain_glue.py -v` under design 5.14 items 2/9; record complete actual argv/output/status.
   114	Run `bash -n` on all three changed shell scripts, `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/chain-integrate.sh` and applicable repository lint; comments use English shdoc; never run Bats locally.
   115	The whole PR has at most 120 changed lines outside `tests/` and `.orchestration/`, and 400 under `tests/`, counting additions plus deletions; attribute inherited 26 outside-test lines and 69 test lines separately from this reset's corrections, including caller edits.
   116	Run `git --git-dir=<private-bare> diff --numstat <base40>...<head40>` in the authenticated private repository using resolved full SHAs and record complete output before cleanup.
   117	The orchestrator pastes the resolved measurement base at dispatch; attribute inherited/new changes against that base and final head, including a branch-head base for any records-only round after update-branch; an overrun blocks, never raises caps.
   118	Keep the complete dispatched text at or under 140 lines, reserving seven for Checks; no workflow, permission, dependency, launcher, knowledge-graph, predecessor-artifact or a09-owned changes are authorized.
   119	Worker Playbook step 4 applies: every a013 command, including gh, Git and agmsg delivery, stays sandboxed; push without `-u` over HTTPS with `git push https://github.com/mryfmo/dotfiles.git tools/chain-review-scripts-followup-a07`; every denial records command/status/boundary and sends blocked PONG without escalation/substitution.
   120	Do not probe the herdr socket; placement/delivery verification and host-deployment evidence belong to the orchestrator. Keep plan/todo/learn uncommitted and at most one active todo per owner.
   121	Copy these complete dispatched bytes to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md`; keep the retained a07 task copy/evidence unchanged; no executable helper may be hidden in the artifact wildcard.
   122	Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and `-worker-` crit-data/receipt evidence under the a08 directory; follow repository review gates without browser/human review, record provenance and `cost:`.
   123	Each evidence item names `worker (Codex seat, a013)` or `orchestrator (Claude seat, sandboxed Bash)`; identify separate authoring/inherited producers honestly and include exact commands, operands, statuses, complete outputs and refusals without secrets.
   124	Keep evidence untracked at the same relative paths in worker-h when main-checkout paths are inaccessible; RESULT identifies their location for orchestrator transfer.
   125	This text's C-80 round 2 addresses supplied round 1; at most two C-80 text-review rounds total, no private third round. Keep INV-6/a07 counters and the one worker Bot fix-round limit; surviving P0/P1 goes to the operator.
   126	After final push verify GitHub Actions and wait for final-head Bot feedback under the Worker Playbook; the worker proposes dispositions and resolves no threads.
   127	RESULT names PR, full head/base, branch, changed files, selectors, red/green commits, caps/attribution, artifact paths and `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md>`.
   128	The orchestrator records counters before acceptance, carries a07 history, then performs final-head sweep, task audit, security review, acceptance and gate in Playbook step 10 order; changed heads repeat required evidence; advisory ownership remains `dotfiles-T128-chain-review-scripts-followup-a09`.
   129	Not performed by this authoring context: implementation edits, worker tests, live fetch, CI or deployment.
   130	Shared credentials and unrestricted same-UID interference remain residual; fixture results cannot authorize production cache reuse or integration before the declared deployment prerequisites.
   131	
   132	## Checks (pasted by the orchestrator before each send)
   133	

 succeeded in 109ms:
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
67:- Only acceptance decisions and final merge stay orchestrator-side. Seats and scripts handle integration, adversarial RESULT review, review-profile work, gate and records through `verdict.sh`, `audit-pool.sh`, `result-precheck.sh`, `acceptance-front-matter.py` and `dispatch.sh --next`. Pending each mechanism, Delegation's interim exemption permits manual orchestrator execution. Every code-changing RESULT gets one task-level audit of its final head; findings are input, never approval (the "Task-level audit" bullet).
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
178:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
181:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
182:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
225:## Codex seat worklogs
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

 succeeded in 164ms:
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
 M .orchestration/tasks/dotfiles-T133-pre-send-check-a02.md
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
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-chain-08b8add.log
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
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
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

**Requesting plain text output**
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md; cat .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '225,263p' ~/.agents/skills/agmsg-orchestration/SKILL.md; rg -n '5\\.14|5\\.15' .orchestration/plans/024-design-quality.md; cat .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md; cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md; cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md; rg -n '"'^##|'"\\(e\\)|\\(e.\\)' .orchestration/tasks/dotfiles-T133-python-pin-a02.md" in ~/Workspace/dotfiles
 succeeded in 113ms:
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
# Notes every review-profile brief carries (orchestrator glue, 2026-10-20)

1. Host facts measured before authoring, pasted verbatim: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`. A text names a resolve command and asks the worker to paste its output, never a guessed path (re-plan validation-setup of regime-ci-token-a01).
2. Every evidence item names its producer and seat kind: `orchestrator (Claude seat, sandboxed Bash)` or `worker (<kind> seat)`. A Codex seat cannot probe the herdr socket from its sandbox (PermissionDenied measured 2026-10-20T13:39Z, a013); never ask it to (M-20261020-06/08 class).
3. The self cap leaves room for the orchestrator's Checks block (about 7 lines) when the text keeps a fenced block under `## Checks`; a reset text anchored by a review is dispatched at the anchored bytes with no paste.
4. No restatement of the trusted-execution contract: design 5.14 items by reference; environment and executable rows the tool cannot close are `residual` with an owner (re-plan contract-restatement of regime-ci-token-a01). Texts for security: false tools get no C-80 (D-024-46).
5. Caps in the C-107 sentence form; the numstat command in its own sentence; measurement base pasted at dispatch (the branch head at dispatch for a records-only round after an update-branch, not an older code head).
6. Baseline statements bind to the post-prerequisite state: a text that names `after:` prerequisites describes main as it will be after they merge (their post-merge effects stated in the brief), never as it is on the authoring day (slice 1 of P1-15, 2026-10-21: an old Linux exclusion policy was preserved against a prerequisite that empties it).


35:  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: Commands (e) binds the base and Commands (f) obtains cap evidence from github.com's fixed repository API at full 40-hex SHAs; acceptance verifies the final head against GitHub content."}
68:  - claim: "Commands (e), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
100:## Commands
122:# (e) Bind gh, print and check the binding, then obtain the canonical base.
127:# (e') Isolate gh's persistent configuration (hosts.yml api_host can redirect requests): a fresh config dir and the keyring token read once by the bound gh.
144:## Work
152:## Check — prerequisites
154:The orchestrator executed the successful read-only Commands (a), (b), (c), (e) binding/version and (g) probes sequentially inside Commands (parent) before this dispatch at 2026-10-20T04:31:20Z; `premises` contains their exact commands and outputs.
155:Commands (d), (e') and (f)/(f') were not run in that probe: test execution, token read and PR compare belong to the worker/RESULT. The probed checkout's `latest` output is the source baseline, not the continued PR's implementation.
156:Before worker validation, repeat (a), (b), (c), (e)'s binding/version probe and (g); require version `3.15.0`, its realpath inside the anchored Python install root, and executable non-shim gh. A missing executable or version mismatch produces `python-pin: refused: installed-version-mismatch` and a blocked PONG; `after: []` adds no task dependency.
158:## Check — caps and final head
160:The worker runs Commands (e) and (e') at dispatch and records its authenticated canonical `<base40>`; record the initial and final `<head40>` verified against GitHub, each exactly 40 ASCII hexadecimal characters.
165:## Completion and boundaries
168:All gh operations retain the Commands (e) binding and clean environment and explicitly identify github.com/mryfmo/dotfiles; continue the existing English PR under the Worker Playbook.
176:## Checks (pasted by the orchestrator before each send)
181:C-80 round 1 of this text: 68fd5f2 `Verdict: correct`; the probes in premises were executed read-only by the orchestrator at 2026-10-20T04:31:20Z (Commands (a),(b),(c),(e),(g)); PR #437 continues on task/dotfiles-T133-python-pin-a01 from head e9819d45 (implementation 09c81cc3 unchanged); the a01 copy stays as the predecessor copy

 succeeded in 177ms:
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
95:### 5.14 残余（凍結後の計測事実、D-024-29）
103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
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
Verdict: incorrect
**Noting current transcript status**
exec
/bin/zsh -lc "sed -n '103,210p' .orchestration/plans/024-design-quality.md; sed -n '100,143p' .orchestration/tasks/dotfiles-T133-python-pin-a02.md; cat .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
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

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:65 Keeping `local-advisory.sh` unchanged disconnects enforcement from the reviewed artifact: it still reads `.orchestration/validation/<task>-local-review-<sha7>.md`, whereas Item 3 writes a private full-head filename; when the new review returns P1 findings, a planted legacy `findings: 0` makes the advisory consumer return success and lets `chain-integrate.sh` continue.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:77 A mode-0700 directory under `${TMPDIR:-/tmp}` does not establish a worker-inaccessible object store: same-UID workers with access to that temporary root can modify it, and item 3’s worker-root/symlink/case checks do not exclude shared scratch space; replacement after fetch can therefore change the content consumed by the reviewer, while the named stub test establishes no write boundary.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:23 Cache provenance cannot be `closed` while line 30 acknowledges unenforced Claude file-tool protection and `after: []` imposes no deployment prerequisite: a worker can forge an anchored-cache artifact containing the publicly computable head/base/tree and `findings: 0`; fresh canonical lookup and fetch validate those identifiers, not who produced the review.

[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:31 Referencing a trusted-parent contract does not supply a trusted caller: `chain-integrate.sh:143` directly executes the script with inherited environment, and neither this task nor the named binding owner authorizes changing that caller; `BASH_ENV` or Linux loader injection can execute before child sanitization, including before an unsandboxed gh invocation, so clean Git/gh children cannot compensate for the missing entry boundary.

[P2] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:92 Preserving every inherited regression conflicts with the required executable binding: the inherited tests explicitly require PATH-selected `mise which` calls and interpreter fallback, while design §5.14 item 9 prohibits both; they also require exactly two Codex environment overrides despite the configured reviewer PATH containing mise shims, so these assertions must be revised to verify the actual descendant Git binding.

📝 まとめ: タスク本文と参照記録を読み取り専用で審査し、実行・成果物の結び付けと保護前提に5件の指摘を確認しました。
Not checked: implementation, live sandbox enforcement, or test execution; the stated controls do not yet establish the claimed boundaries.
Verdict: incorrect
**Reviewing ledger test sources**
codex
前回の5件について、今回の本文には private artifact の受け渡し、保護の導入待ち、実際の呼び出し箇所の修正が追加されています。残る確認点は、承認台帳を読む経路まで保護が届くかと、各 `closed` 行のテストが宣言した範囲を検証できるかです。
exec
/bin/zsh -lc 'nl -ba scripts/orchestrator/local-advisory.sh; nl -ba scripts/orchestrator/local-review.sh; nl -ba scripts/orchestrator/chain-integrate.sh' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md; cat .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md; cat .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md; cat .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md; nl -ba .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md | tail -38' in ~/Workspace/dotfiles
 succeeded in 165ms:
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
     1	#!/usr/bin/env bash
     2	# @file chain-integrate.sh
     3	# @brief Run a PR head's integration chain up to the audit from the main checkout's scripts, logging every step.
     4	# @description
     5	#   Plan 022 T7 (D7): Orchestrator Playbook step 10 up to the audit as one command. After its preconditions (the
     6	#   arguments, the binaries resolved outside shims, the main checkout on main at origin/main, the canonical clean
     7	#   review worktree, the record, a ready PR) it fetches the head into both checkouts, update-branches when the base
     8	#   moved (restarting at the fetch), waits for the required checks and the Bot (never gated), then runs the sandbox
     9	#   scan, the local review, the advisory rows, the sweep, the receipt, the record block and the audit, which an
    10	#   update-branch-only head inherits from the head it merged main into when the PR's patch-id is unchanged, a clean
    11	#   merge of its parents reproduces its tree and that head's audit ends with a verdict the gate accepts. Each command
    12	#   goes to `.orchestration/validation/<task>-chain-<sha7>.log` as `<utc> <step> rc=<n>: <command>`, repository
    13	#   paths relative; a refusal before the head is known goes to stderr only. The repository scripts run from the main
    14	#   checkout, never the head, and the script never changes directory into the review worktree.
    15	# @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
    16	# @arg $2 int PR number.
    17	# @arg $3 path The main checkout.
    18	# @arg $4 path The review worktree, `<main>/.claude/worktrees/orchestrator-review`.
    19	# @arg $5 string The task id that owns the advisory findings, in the task id's form.
    20	# @arg $6 path Optional extra dispositions TSV for fill_sweep.py.
    21	# @exitcode 0 The audit is written; the last line is `chain-integrate: <task> <head> <verdict line>`.
    22	# @exitcode 1 A step's command failed: `step <name> failed rc=<n>` on stderr and in the log.
    23	# @exitcode 10 A refused precondition (argument, main checkout, review worktree, record, draft, head mismatch, head
    24	#   already audited, update-branch head not visible).
    25	# @exitcode 11 A P0/P1 local finding.
    26	# @exitcode 12 The required checks failed.
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
    85	[ -z "${out}" ] || refuse 10 "review worktree is not clean"
    86	record=${main}/.orchestration/acceptance/${task}.md
    87	[ -f "${record}" ] || refuse 10 "no acceptance record ${record#"${main}"/}"
    88	pre "${gh}" pr view "${pr}" --json isDraft --jq .isDraft
    89	[ "${out}" = false ] || refuse 10 "draft PR: the worker marks it ready"
    90	pre "${git}" -C "${review}" fetch -q origin main
    91	# The log names repository paths only, so an extra TSV must be in the main checkout (PR #372 thread 4291474891).
    92	[ -z "${extra}" ] || extra=$(cd -- "$(dirname -- "${extra}")" 2> /dev/null && pwd -P)/${extra##*/}
    93	[[ -z ${extra} || ${extra} == "${main}"/* ]] || refuse 10 "extra dispositions TSV is not in the main checkout: $6"
    94	export ORCH_REVIEW_WORKTREE=${review}
    95	v=${main}/.orchestration/validation
    96	for attempt in 1 2 3; do
    97	    step fetch 0 "${git}" -C "${main}" fetch -q origin "+pull/${pr}/head:refs/remotes/pr/${pr}"
    98	    step fetch 0 "${git}" -C "${review}" fetch -q origin "+pull/${pr}/head"
    99	    step fetch 0 "${git}" -C "${review}" checkout -q --detach FETCH_HEAD
   100	    step fetch 0 "${git}" -C "${review}" rev-parse HEAD
   101	    head=${out}
   102	    step fetch 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid
   103	    [ "${out}" = "${head}" ] || refuse 10 "head mismatch: re-run"
   104	    sha7=${head:0:7}
   105	    # The log is named by the head, so the lines before it are written once it is known; a new head's log holds them all.
   106	    [ "${log}" = "${v}/${task}-chain-${sha7}.log" ] || { log=${v}/${task}-chain-${sha7}.log && printf '%s\n' "${lines[@]}" >> "${log}"; }
   107	    [ ! -e "${v}/${task}-audit-${sha7}.md.last.md" ] || refuse 10 "head already audited: one chain per head"
   108	    step base 0,1 "${git}" -C "${review}" merge-base --is-ancestor origin/main HEAD
   109	    if ((rc == 0)); then
   110	        step checks any "${gh}" pr checks "${pr}" --required --watch
   111	        ((rc == 0)) || refuse 12 "required checks failed"
   112	        # Plan 020 step 4: the Bot wait is never gated, so it ends present or absent and the chain goes on.
   113	        q="[.[] | select(.user.login == \"chatgpt-codex-connector[bot]\" and .commit_id == \"${head}\")] | length"
   114	        t0=$("${date}" +%s)
   115	        while step bot 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/reviews" --paginate --jq "${q}"; do
   116	            n=$((${out//$'\n'/+})) # one count per page
   117	            ((n == 0 && $("${date}" +%s) - t0 < ${CHAIN_BOT_WAIT:-900})) || break
   118	            sleep 30
   119	        done
   120	        say "bot review: $( ((n > 0)) && echo present || echo absent)"
   121	        # origin/main can move during the waits (PR #372 thread 4291474885): a moved base is updated, then the fetch.
   122	        step base 0 "${git}" -C "${review}" fetch -q origin main
   123	        step base 0,1 "${git}" -C "${review}" merge-base --is-ancestor origin/main HEAD
   124	        ((rc == 1)) || break
   125	    fi
   126	    ((attempt < 3)) || refuse 13 "base moved three times"
   127	    step base 0 "${gh}" pr update-branch "${pr}"
   128	    t0=$("${date}" +%s) # GitHub builds the merge commit asynchronously: poll the head check's query until it moves.
   129	    while step base 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid && [ "${out}" = "${head}" ]; do
   130	        (($("${date}" +%s) - t0 < ${CHAIN_POLL_MAX:-120})) || refuse 10 "update-branch head not visible"
   131	        sleep "${CHAIN_POLL_SECONDS:-5}"
   132	    done
   133	    fresh  # a moved base may have left the main checkout's main behind, which local-review.sh diffs against
   134	    log='' # the next head's log takes every line; this one ends here
   135	done
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
   195	        "${v}/${task}-chain-${parent:0:7}.log" 2> /dev/null || old=''
   196	    # Only a verdict the gate accepts is inherited (its AUDIT_VERDICT and AUDIT_FINDING): correct, or incorrect with a
   197	    # [P0-P3] line; a blocked, empty or finding-less parent result takes the fresh audit (audit:274a536:2).
   198	    last=$(/usr/bin/awk 'NF { l = $0 } END { print l }' "${from}.md.last.md")
   199	    [[ ${last} =~ ^[[:space:]]*Verdict:\ (correct|incorrect)[[:space:]]*$ ]] || old=''
   200	    [[ ${BASH_REMATCH[1]-} != incorrect ]] || /usr/bin/grep -qE '^[[:space:]]*([-*+][[:space:]]+)?\[P[0-3]\]' "${from}.md.last.md" || old=''
   201	fi
   202	if [[ -n ${old} && ${old%% *} == "${new%% *}" ]]; then
   203	    for s in .md .md.last.md; do
   204	        # A parent that inherited keeps its marker: the ids stay those of the head the audit ran on.
   205	        { [[ $(head -n 1 -- "${from}${s}") == inherited-from:* ]] || echo "inherited-from: ${parent:0:7}"; } > "${v}/${task}-audit-${sha7}${s}"
   206	        cat -- "${from}${s}" >> "${v}/${task}-audit-${sha7}${s}"
   207	    done
   208	    say "$("${date}" -u +%FT%TZ) audit rc=0: audit inherited from ${parent:0:7} ($(head -n 1 -- "${v}/${task}-audit-${sha7}.md.last.md"))"
   209	    echo "audit inherited from ${parent:0:7}"
   210	    verdict="chain-integrate: ${task} ${head} $(tail -n 1 -- "${v}/${task}-audit-${sha7}.md.last.md")"
   211	else
   212	    step audit 0 "${main}/scripts/orchestrator/orch-audit.sh" "${task}" "${review}" "${pr}"
   213	    verdict="chain-integrate: ${task} ${head} ${out##*$'\n'}"
   214	    step audit 0 "${git}" -C "${review}" checkout -q --detach "${head}" # orch-audit.sh leaves it at origin/main; the gate reads it
   215	fi
   216	say "${verdict}" && echo "${verdict}"

 succeeded in 200ms:
---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-binding-a01
kind: code
security: true
allowed_files: ["home/dot_agents/agent-config.yaml","home/.chezmoitemplates/claude-settings-managed.json","home/dot_claude*/modify_private_settings.json","scripts/generate-agent-configs.py","scripts/validate-agent-assets.py","Makefile","tests/unit/test_claude_managed_settings.py","tests/unit/test_validate_agent_assets.py","scripts/orchestrator/trusted-launch.sh",".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**"]
after: [dotfiles-T133-worker-write-boundary-slice2-a01, dotfiles-T133-ci-efficiency-followup-a04]
rendered_forms: [claude-settings-managed.json, permgate claude]
out_of_scope:
  - {"path":"home/dot_mise/config.toml","reason":"dotfiles-T133-trusted-entrypoint-pins-a01 pins the real declaration before this task is sent; it is read-only here."}
  - {"path":"tests/unit/test_generate_agent_configs.py","reason":"dotfiles-T133-trusted-entrypoint-pins-a01 removes the installed-template legacy literal pin without relaxing synthetic legacy migration cases."}
  - {"path":"tests/unit/test_claude_settings_merge.py","reason":"Existing legacy/custom/idempotence cases remain valid through the modify script's native expansion; run this real module unchanged."}
  - {"path":"tests/unit/test_statusline_tools.py","reason":"Its native renderer must continue to parse the template without deployment installations; run unchanged."}
  - {"path":"tests/unit/test_herdr_agents.py","reason":"The synthetic SessionStart-only template is unaffected; retain its tests."}
  - {"path":"tests/install/common/lifecycle.bats","reason":"Legacy migration fixture data is retained; Bats runs only in GitHub Actions."}
  - {"path":"tests/fixtures/gate-evidence/pr-feedback-right.json","reason":"Historical feedback fixture text is data and is not rewritten."}
  - {"path":"scripts/orchestrator/trusted-interpreter.sh","reason":"The a04 resolver remains read-only for its existing consumers. This re-plan's launcher validates the exact Python declared by its parent-selected manifest; it must not impose the resolver's production-only pin on fixture execution."}
  - {"path":"home/dot_local/bin/common/executable_permgate","reason":"Unchanged dependency-free script, executed through explicit isolated Python rather than its shebang."}
  - {"path":"home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","reason":"Complete guard, delivery and formatter/map descendant binding is outside this split; retain its named deployment residuals."}
threat_table:
  - {"control":"home/dot_agents/agent-config.yaml","disposition":"residual: Declare exact home-relative uv, Python and node identities and compare their production versions with the read-only mise declaration; deterministic rendering supplies the launcher manifest, while protected inputs still share the OS uid."}
  - {"control":"home/.chezmoitemplates/claude-settings-managed.json","disposition":"residual: Render the PermissionRequest exec-form clean prefix with an exact absolute --manifest operand and retain onFailure block; no outer shell starts, but the hook host and first executable's loader environment remain outside launcher validation."}
  - {"control":"home/dot_claude/modify_private_settings.json","disposition":"residual: Classify the legacy form separately and compare the bound command string and ordered args array, including --manifest, exactly with the rendered canonical exec form; preserve raw quoting distinctions, custom hooks and idempotence."}
  - {"control":"home/dot_claude-worker/modify_private_settings.json","disposition":"residual: Apply the same native expansion and exact bound command/args comparison to this consumer without importing live orchestrator settings or adding an event the surface lacks."}
  - {"control":"scripts/generate-agent-configs.py","disposition":"residual: Render exact relative declarations, the launcher manifest data and exec-form command/args without filesystem discovery; ordinary generation and render-check require no installed tools or deployed manifest."}
  - {"control":"scripts/validate-agent-assets.py","disposition":"residual: Validate exact rendered command/args and expose the opt-in effective-settings identity check; checker and yaml-importing children consume the same parent-selected manifest, verified uv/Python and private cache without substituting production pins into fixtures."}
  - {"control":"Makefile","disposition":"residual: Expose concrete manifest preparation, trusted seed and deployment-check commands and give the formatter the pinned node directory; unrelated inherited recipes remain outside this boundary."}
  - {"control":"scripts/orchestrator/trusted-launch.sh","disposition":"residual: Before any declared binary executes, validate the absolute parent-selected manifest and optional fixture root, parse declarations as data, require canonical regular executable paths and compare exact versions; fixture and production inputs use these same checks, while concurrent same-UID replacement remains possible."}
  - {"control":"tests/unit/test_claude_managed_settings.py","disposition":"residual: Exercise exact exec-form rendering, migration, a real fixture-manifest uv/Python/permgate execution and the separate pinned-installation case; fixture execution proves the shared launcher path, not production installation or administrative protection."}
  - {"control":"tests/unit/test_validate_agent_assets.py","disposition":"residual: Exercise manifest containment, shim, symlink, worker-root and version refusals, quote-preserving comparisons and the clean online seed; recording fake uv cases prove argv and refusal behavior only."}
  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**","disposition":"residual: Only task copies, reports, manifest test data and review or validation evidence are authorized; no executable helper or alternative hook may hide under this wildcard."}
  - {"control":"task copy .orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/task.md","disposition":"residual: Compare the complete dispatched file byte-for-byte and verify its SHA-256; preserve predecessor copies and the three-review history."}
  - {"control":"task metadata","disposition":"residual: Verify identity, both after dependencies, the pin prerequisite and exactly ten allowed_files entries before dispatch and acceptance; the modify-script glob has only its two named consumers."}
  - {"control":"metadata separators","disposition":"residual: Parse front matter as data with duplicate keys refused and compare the whole task copy, including both separate task texts and their separators."}
  - {"control":"in-process effects","disposition":"residual: Fixture execution writes temporary data and markers only; the effective-settings check is read-only and the worker performs no live deployment."}
  - {"control":"workflow and interpreter or environment inputs","disposition":"residual: The trusted parent names the manifest and any fixture root under the clean prefix; launcher discovery, environment overrides and production-only fixture gates are forbidden."}
  - {"control":"new or renamed scripts","disposition":"residual: Only the named launcher is added; manifest parsing and exact-path validation stay there, and no second resolver, wrapper executable or artifact-directory runtime helper is introduced."}
  - {"control":"orchestrator effect manifest provisioning","disposition":"residual: The operator materializes deterministic production manifest data under the protected repository root before enabling the changed hook; fixture manifests cannot become effective production bindings."}
  - {"control":"orchestrator effect merge","disposition":"residual: Only the orchestrator merges the reviewed final head after Playbook step 10; shared credentials remain a bypass risk."}
  - {"control":"orchestrator effect update-branch","disposition":"residual: Only the orchestrator updates the branch and refreshes evidence after any head change."}
  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; only the orchestrator may remove a worker and must record any discarded state."}
  - {"control":"design 5.14 item 0 same-UID model","disposition":"residual: These controls limit accidents and prompt injection; shared credentials and unrestricted same-UID processes remain outside prevention."}
  - {"control":"design 5.14 item 1 executable inputs","disposition":"residual: Retain P1-15 protection of policy, user-site locations, settings, rendered manifest and installed tools; executable binding alone does not protect mutable inputs."}
  - {"control":"design 5.14 item 2 trusted parent","disposition":"residual: Exec form starts /usr/bin/env -i with literal argv before the privileged launcher validates entry state and the selected manifest; the hook host and loader starting /usr/bin/env still require host-supplied clean execution or the P1-16 OS user boundary."}
  - {"control":"design 5.14 item 3 resolved boundaries","disposition":"residual: Apply canonical path, regular-file, shim, worker-root and temporary-root checks to the supplied manifest and its declarations; the explicitly named fixture root is a scoped test allowance, not a production setting."}
  - {"control":"design 5.14 item 4 verified executable","disposition":"residual: Execute only the checked declared realpaths without rediscovery and record the selected manifest identity; unrestricted same-UID replacement after validation remains possible."}
  - {"control":"design 5.14 item 5 output identity","disposition":"residual: Record full base/head identities, task-copy hash and manifest hashes; no new reservation or slot lock is introduced."}
  - {"control":"design 5.14 item 6 honest residuals","disposition":"residual: Report declaration checks, real fixture execution, the named pinned-installation skip, CI and operator-host deployment separately; no fixture or skip substitutes for production evidence."}
  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the eight named regressions and scoped hostile-input cases, recording Class::test selectors without claiming system-wide closure or treating an earlier refusal as coverage of a later check."}
  - {"control":"design 5.14 item 8 authenticated evidence","disposition":"residual: A parent-selected manifest supplies executable declarations, not permission or merge approval; integration evidence and live agmsg hardening retain their separate owners."}
  - {"control":"design 5.14 item 9 isolation and cache","disposition":"residual: Bound Python children use -I and isolated offline uv with an absolute parent-supplied private cache; the explicit online seed uses the same manifest, clean parent and verified uv/Python, retaining --no-config --no-project --isolated --with pyyaml --python and -I while omitting only --offline."}
  - {"control":"design 5.14 item 10 sandbox","disposition":"residual: Every worker command stays inside the sandbox; denial produces blocked evidence without escalation or an alternative execution surface."}
premises:
  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/uv/\" | paste -sd '|' -","output":"0|0.12|0.12.17|0.12.18|0.12.19|0.12.20|0.13|0.13.0|0.13.1|global|latest"}
  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/uv/0.13.1/\" | paste -sd '|' -","output":"uv-aarch64-apple-darwin"}
  - {"command":"realpath \"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv"}
  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/python/\" | paste -sd '|' -","output":"3|3.15|3.15.0|global|latest"}
  - {"command":"realpath \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15"}
  - {"command":"head -1 \"$HOME/.local/share/mise/installs/npm-prettier/3.9.10/bin/prettier\"","output":"#!/usr/bin/env node"}
  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/node/\" | paste -sd '|' -","output":"26|26.12|26.12.0|global|latest"}
  - {"command":"realpath \"$HOME/.local/share/mise/installs/node/26.12.0/bin/node\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/node/26.12.0/bin/node"}
  - {"command":"grep -nE '^(uv|python|node) = ' home/dot_mise/config.toml | paste -sd '|' -","output":"3:node = \"latest\"|5:python = \"latest\"|17:uv = \"latest\""}
  - {"command":"ls -1 .mise.toml mise.toml 2>&1 | paste -sd '|' -","output":"ls: .mise.toml: No such file or directory|mise.toml"}
  - {"command":"cat mise.toml | paste -sd '|' -","output":"[tools]"}
  - {"command":"grep -n '\"command\": \".*permgate claude\"' home/.chezmoitemplates/claude-settings-managed.json","output":"207:            \"command\": \"~/.local/bin/common/permgate claude\","}
  - {"command":"head -1 home/dot_local/bin/common/executable_permgate","output":"#!/usr/bin/env -S uv run --no-cache --script"}
  - {"command":"grep -cE '^# ///|^# dependencies[[:space:]]*=' home/dot_local/bin/common/executable_permgate","output":"0"}
  - {"command":"sed -n '179,182p' Makefile | paste -sd '|' -","output":"format:| shfmt --indent 4 --space-redirects --diff .| git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check| git ls-files -z '*.md' | xargs -0 prettier --check"}
  - {"command":"grep -cE '(^|[[:space:]])(export[[:space:]]+)?PATH[[:space:]:?+]*=' Makefile","output":"0"}
  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_agents/agent-config.yaml home/.chezmoitemplates/claude-settings-managed.json home/dot_claude/modify_private_settings.json home/dot_claude-worker/modify_private_settings.json scripts/generate-agent-configs.py scripts/validate-agent-assets.py Makefile tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":"Makefile|home/.chezmoitemplates/claude-settings-managed.json|home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/generate-agent-configs.py|scripts/validate-agent-assets.py|tests/unit/test_validate_agent_assets.py"}
  - {"command":"grep -nE '^  - (home/dot_claude-worker/modify_private_settings.json|tests/unit/test_claude_managed_settings.py)$' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | paste -sd '|' -","output":"12:  - home/dot_claude-worker/modify_private_settings.json|27:  - tests/unit/test_claude_managed_settings.py"}
  - {"command":"grep -nE '^def (render_claude_settings|render_template_text|validate_claude_settings|validate_model_profile_assets|validate_generated_agent_configs|main|render_managed_template|is_managed_permission_hook)\\(' scripts/generate-agent-configs.py scripts/validate-agent-assets.py home/dot_claude/modify_private_settings.json | paste -sd '|' -","output":"scripts/generate-agent-configs.py:400:def render_claude_settings(manifest: dict[str, Any]) -> str:|scripts/generate-agent-configs.py:1401:def main() -> None:|scripts/validate-agent-assets.py:88:def render_template_text(path: Path, os_name: str = \"darwin\") -> str:|scripts/validate-agent-assets.py:374:def validate_claude_settings(manifest: dict[str, Any], os_name: str = \"darwin\") -> None:|scripts/validate-agent-assets.py:1187:def validate_model_profile_assets(manifest: dict[str, Any]) -> None:|scripts/validate-agent-assets.py:1294:def validate_generated_agent_configs() -> None:|scripts/validate-agent-assets.py:1660:def main() -> None:|home/dot_claude/modify_private_settings.json:48:def render_managed_template(text: str) -> str:|home/dot_claude/modify_private_settings.json:68:def is_managed_permission_hook(hook: Any) -> bool:|home/dot_claude/modify_private_settings.json:196:def main() -> int:"}
  - {"command":"sed -n '400,487p' scripts/generate-agent-configs.py | wc -l | xargs","output":"88"}
  - {"command":"sed -n '88,100p;374,406p;1187,1265p;1294,1304p;1660,1685p' scripts/validate-agent-assets.py | wc -l | xargs","output":"162"}
  - {"command":"sed -n '48,55p;68,79p' home/dot_claude/modify_private_settings.json | wc -l | xargs","output":"20"}
  - {"command":"wc -l .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | xargs","output":"63 .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json 95 .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py 1781 tests/unit/test_validate_agent_assets.py 79 home/dot_mise/config.toml 2350 tests/unit/test_generate_agent_configs.py 4368 total"}
  - {"command":"ls tests/unit/test_task_consistency_c11_c15.py 2>&1 | paste -sd '|' -","output":"ls: tests/unit/test_task_consistency_c11_c15.py: No such file or directory"}
  - {"command":"sed -n '63,66p' .claude/worktrees/worker-g/tests/unit/test_task_consistency_c11_c15.py | paste -sd '|' -","output":"CASES = {|    \"C11\": (|        '\"closed: tests/unit/test_tool.py::test_tool_prints_findings\"',|        '\"closed: tests/unit/test_tool.py::two words\"',"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\" --version","output":"uv 0.13.1 (62faed335 2026-10-13 aarch64-apple-darwin)"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B --version","output":"Python 3.15.0"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/node/26.12.0/bin/node\" --version","output":"v26.12.0"}
  - {"command":"rg -l 'claude-settings-managed|is_managed_permission_hook|permgate claude' home scripts tests .github Makefile --glob '!*.md' --glob '!*.lock' | sort | paste -sd '|' -","output":"home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/validate-agent-assets.py|tests/fixtures/gate-evidence/pr-feedback-right.json|tests/install/common/lifecycle.bats|tests/unit/test_claude_settings_merge.py|tests/unit/test_generate_agent_configs.py|tests/unit/test_herdr_agents.py|tests/unit/test_statusline_tools.py|tests/unit/test_validate_agent_assets.py"}
  - {"command":"grep -nE '^class (ClaudeManagedSettingsTest|ValidateAgentAssetsTest)' .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":".claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py:12:class ClaudeManagedSettingsTest(unittest.TestCase):|tests/unit/test_validate_agent_assets.py:84:class ValidateAgentAssetsTest(unittest.TestCase):"}
  - {"command":"sed -n '117p' .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md | cut -d . -f 1-2","output":"On success print exactly one absolute interpreter realpath and exit 0. On every refusal print exactly one line `trusted-interpreter: refused: <code>` to stderr, print no interpreter on stdout, and exit 2"}
  - {"command":"printf '%s\\n' \"$PATH\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/shims:$HOME/.local/bin:$HOME/.local/bin/common:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$HOME/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:$HOME/.local/share/mise/installs/node/lts/bin:/usr/bin:/bin:/usr/sbin:/sbin"}
  - {"command":"grep -nE '^    import yaml|PyYAML is required' scripts/validate-agent-assets.py | paste -sd '|' -","output":"22:    import yaml|81:        fail(\"PyYAML is required\")|175:        fail(\"PyYAML is required to validate skill frontmatter\")"}
  - {"command":"sed -n '340,346p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | paste -sd '|' -","output":"   Its managed PermissionRequest command remains exactly:||   ```text|   ~/.local/bin/common/permgate claude|   ```||   Do not add an env prefix, guard selector, absolute uv/Python invocation or new command-form validator for this hook. Keep its existing timeout and add the task's common `onFailure: \"block\"` entry policy. The unchanged command's shebang, interpreter discovery and inherited environment are explicit residuals owned by the binding task."}
  - {"command":"head -1 .claude/worktrees/worker-e/home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","output":"#!/bin/bash"}
  - {"command":"test ! -e scripts/orchestrator/trusted-launch.sh","output":"","exit_status":0}
  - {"command":"python3 -I -B -c 'from pathlib import Path; roots=(Path(\"home\"),Path(\".claude/worktrees/worker-e/home\")); print(\"|\".join(str(p) for root in roots for p in sorted(root.glob(\"dot_claude*/modify_private_settings.json\"))))'","output":"home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json"}
  - {"command":"python3 -I -B -c 'import os,pwd,stat; from pathlib import Path; h=Path(pwd.getpwuid(os.getuid()).pw_dir); u=h/\".local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\"; r=u.resolve(strict=True); print(\"home_matches_passwd=\"+str(Path.home()==h)); print(\"uv_regular=\"+str(stat.S_ISREG(u.lstat().st_mode))); print(\"uv_symlink=\"+str(u.is_symlink())); print(\"uv_under_passwd_install_root=\"+str(r.is_relative_to(h/\".local/share/mise/installs\"))); print(\"uv_declared_equals_realpath=\"+str(u==r)); print(\"trusted_launch_exists=\"+str(Path(\"scripts/orchestrator/trusted-launch.sh\").exists()))'","output":"home_matches_passwd=True\nuv_regular=True\nuv_symlink=False\nuv_under_passwd_install_root=True\nuv_declared_equals_realpath=True\ntrusted_launch_exists=False"}
  - {"command":"rg -n '^    import yaml|PyYAML is required' scripts/generate-agent-configs.py | paste -sd '|' -","output":"14:    import yaml|34:        fail(\"PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py\")"}
  - {"command":"sed -n '1294,1298p' scripts/validate-agent-assets.py | paste -sd '|' -","output":"def validate_generated_agent_configs() -> None:|    result = subprocess.run(|        [sys.executable, str(ROOT / \"scripts/generate-agent-configs.py\"), \"--check\"],|        cwd=ROOT,|        text=True,"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B scripts/generate-agent-configs.py --check","output":"ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py","exit_status":1}
  - {"command":"claude --version","output":"2.1.300 (Claude Code)","exit_status":0}
  - {"command":"python3 -I -B -c 'from pathlib import Path; b=(Path.home()/\".local/share/mise/installs/npm-anthropic-ai-claude-code/latest/bin/claude\").read_bytes(); s=b\"Command hooks require `command`. For exec form (no shell)\"; i=b.find(s); print(b[i:b.index(b\"\\0\",i)].decode() if i>=0 else \"missing exec-form help\")'","output":"Command hooks require `command`. For exec form (no shell), set `command` to the executable and `args` to its arguments: {\"type\": \"command\", \"command\": \"echo\", \"args\": [\"hi\"]}. For shell form, set `command` to the full shell string: {\"type\": \"command\", \"command\": \"echo hi\"}.","exit_status":0}
  - {"command":"web.open https://code.claude.com/docs/en/hooks#exec-form-and-shell-form","output":"Command hook args present selects direct executable spawn without a shell; args omitted selects shell form (sh -c on macOS/Linux). command is the executable path and args is its argument vector. Documented path placeholders include ${CLAUDE_PROJECT_DIR} and are substituted as plain strings."}
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-binding-a01 — bind trusted entrypoints to a parent-selected manifest

Worker: a Codex seat (worktree named at dispatch)

Use the security profile for this Claude-boundary change. D-024-26 split this family from P1-15. Read the last 60 lines of .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md and .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-{f810c30,772cde0,e5c055e,5204254}.md.last.md: shebang discovery, Python startup injection, the checker's own execution, shim discovery, the real uv layout and Prettier's node must be handled together.

Read the complete binding acceptance record and these three pre-dispatch reviews:

- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-faae5f4.md.last.md
- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-8f5ac8d.md.last.md
- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-e3ae7cd.md.last.md

This is the C-92 fixture-vs-binding re-plan recorded by the acceptance record's `re-plan:` line, not a fourth repair under the predecessor design. Preserve the earlier findings and their dispositions. The new design retains round 3's exec-form hook, quote-preserving comparisons and bound online seed, and replaces its contradictory positive-fixture requirement.

The launcher validates the manifest its trusted parent explicitly names. Production passes the rendered production manifest; tests pass a fixture manifest declaring the runner's real tools. Both use the same manifest parser, exact-path checks, containment checks, version comparisons and command construction. A fixture cannot bypass a check, and a production-only resolver or hard-coded installation gate must not run before the fixture's declared interpreter.

These are two separate task files. This primary task has exactly ten allowed_files entries: eight exact implementation/test paths, one modify-script glob and one evidence wildcard. The glob authorizes only home/dot_claude/modify_private_settings.json and home/dot_claude-worker/modify_private_settings.json, each with its own threat row. An additional match requires a reviewed split. The second file below owns mise pins and the generator assertion; do not combine their front matter or dispatch this task before that prerequisite is accepted.

## Dispatch prerequisites and scope

Accept dotfiles-T133-trusted-entrypoint-pins-a01 before the Python-resolver dependency is dispatched; the historical probe says latest for all three tools. Accept both after dependencies and verify P1-15's deployed protection before sending this task.

The seven existing concrete allowlist paths were on origin/main at the recorded probe. P1-15 creates the worker modify script and ClaudeManagedSettingsTest module. Add scripts/orchestrator/trusted-launch.sh as the only new executable source. Recheck these paths and measurements on the actual dispatch baseline; refresh changed premises through a reviewed, hashed amendment before dispatch, never only in the Checks paste.

The installed a04 resolver remains read-only. Its existing consumers retain its production-pinned contract. For the scoped launcher, this re-plan explicitly replaces the earlier instruction to obtain Python unconditionally from that resolver: resolve and validate the exact Python declaration in the parent-selected manifest, using the same code for production and fixtures. Do not edit the resolver, add PATH discovery to production, or make a fixture satisfy an unrelated host's mise pin.

The root C11 test file was absent at the recorded probe, and the inspected worker-g copy accepted tests/<path>::<identifier> rather than a Class::test payload. The orchestrator must obtain and read the accepted checker/test revision before dispatch, check C1–C10, C7b and C11, and manually re-probe premises. Never execute arbitrary premise shell strings through an unchecked checker.

Each threat-table file row names one file or one allowed wildcard only. This draft makes no closed claims. Any later closed row must name exactly one selector in the form tests/<path>::<Class>::<test>; a module name, free-function selector or prose reference is insufficient.

## Applicable design — C-88 verbatim quotations

`$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, section 5.14, is uncommitted design input. The relied-on sentences of items 1, 2 and 9 are quoted verbatim below. The parent-selected manifest contract is this re-plan's explicit scoped replacement for an unconditional production-pinned resolver call.

> The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19).
>
> A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
>
> One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.

## Implementation contract

### Declarations and deterministic rendering

Declare production uv 0.13.1 at .local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv, Python 3.15.0 at .local/share/mise/installs/python/3.15.0/bin/python3.15, and node 26.12.0 at .local/share/mise/installs/node/26.12.0/bin/node, relative to the real uid's passwd home. A test compares all three production versions with home/dot_mise/config.toml. No wildcard, version alias, latest, shim, traversal or missing required declaration is accepted. If accepted pins differ from these probes, stop for a re-probed amendment rather than substituting an installed version.

Rendering composes the supplied home and repository bindings with these declarations and validates shape only. It remains deterministic on a host with no installs. Use the same native expansion in both modify-script consumers and the validator renderer, with correct JSON and shell quoting, including homes and repository paths containing spaces.

Render the launcher manifest as data from the source manifest. The fixed production destination is <canonical repository root>/.agents/worklog/trusted-entrypoint-manifest, outside worker-writable roots. It is an operator-provisioned runtime data artifact, not a new tracked source file or an executable under the evidence wildcard. The operator materializes it during deployment preparation before enabling the changed hook. Tests render into their temporary fixture root. Ordinary generation and render-check compare the deterministic rendering without requiring or writing the installed production artifact.

Use one small, documented data grammar that the privileged-shell launcher can parse with fixed absolute system tools before executing any declared uv or Python. Treat every field as literal data: no source, eval, shell expansion, command substitution or declared-interpreter bootstrap. Reject malformed, duplicate, unknown or missing required fields. Declare exact relative paths and exact versions; declarations must not select arbitrary commands. The production manifest also carries the rendered worker-root inventory used by containment checks.

### Parent-selected manifest and shared checks

Every launcher invocation requires exactly one `--manifest <absolute path>` before its operation. There is no implicit manifest, environment-variable replacement or discovery fallback. The only additional root argument is one optional `--fixture-root <absolute directory>`, also supplied by the trusted parent before the operation.

Validate the launcher entry state before reading the manifest. Retain #!/bin/bash -p, English shdoc comments, the exact accepted clean environment, the canonical non-symlinked launcher pathname under its repository root and HOME equality with the real uid's passwd home. Account explicitly for Bash-maintained environment entries. Refuse rather than repairing the environment or self-re-executing.

Resolve the manifest and require a regular, non-symlinked file whose canonical path is under the repository root or, when explicitly supplied, under the canonical fixture root. Reject sibling-prefix lookalikes, path traversal and symlink escapes. A fixture root must be an existing canonical directory; it does not replace passwd HOME, the launcher repository root or the launcher's own entry checks.

Apply the same checks to every declared executable required by the selected operation:

1. Require the exact declared relative path, composed with passwd home for production or the explicitly named fixture root for fixture bindings. Do not accept an arbitrary absolute executable operand, a parent traversal or a different installation chosen by discovery.
2. Require a regular executable file, reject a symlinked binary or redirected installation component, and require the declared composed pathname to equal the canonical executable pathname.
3. Reject a `shims` path component before and after resolution.
4. Reject containment under worker-writable roots, worker caches or temporary roots, including $TMPDIR. The explicitly named fixture root is the sole scoped allowance for fixture files under temporary storage; it does not waive regular-file, symlink, shim, exact-path or version checks. Explicit worker subroots within a fixture remain forbidden.
5. Complete identity and containment checks before executing that binary, including a --version probe. Compare the reported version exactly with that manifest's declared pin, then use only the verified absolute realpath.

The production manifest pins must match the repository's mise declaration. A fixture manifest instead pins the actual versions of its real fixture tools. Comparing fixture versions with production mise pins, calling the production-only resolver first, or accepting arbitrary runner paths without the shared checks would reproduce the rejected design.

No launcher-side command -v, mise which, newest-version selection, PATH fallback, download or alternative resolver is permitted. Test-harness discovery described below is preparation of trusted fixture input, not launcher discovery.

Refusals exit 2, emit exactly one stderr line `trusted-launch: refused: <code>`, and produce no operation output. Use dirty-environment, script-path, home-mismatch, cache-path, manifest-path, manifest-shape, fixture-root, uv-path, python-path, node-path, version-mismatch or invocation for the corresponding failed check. Version probes may run only after path checks; capture their output for validation rather than leaking it into hook stdout. Preserve underlying operation exit status after successful validation. A negative test must reach and assert its intended reason, rather than passing through an earlier refusal.

### Exec-form hook and migration

The installed Claude Code probe reports 2.1.300. Its embedded hook help and the [exec-form documentation](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form) establish command plus args without an outer shell. Retain that round-3 decision.

The managed PermissionRequest hook uses the following clean prefix, with absolute rendered host bindings and the parent-selected private cache and manifest. Each args element is one argument; paths containing spaces have no embedded shell quotes. CLAUDE_PROJECT_DIR is the documented host-substituted placeholder, and CLAUDE_ENV_FILE is explicitly empty. Do not assume exec form expands arbitrary environment variables.

```json
{"command":"/usr/bin/env","args":["-i","PATH=/usr/bin:/bin","HOME=<rendered passwd-home>","LANG=C.UTF-8","TERM=dumb","CLAUDE_PROJECT_DIR=${CLAUDE_PROJECT_DIR}","CLAUDE_ENV_FILE=","UV_CACHE_DIR=<private cache>","/bin/bash","--noprofile","--norc","-p","<abs trusted launch>","--manifest","<abs rendered production manifest>","permission-request"]}
```

A fixture uses the same form, substituting its rendered manifest operand and inserting `--fixture-root`, `<abs fixture root>` immediately before permission-request. Effective production settings must match the production form exactly and must not contain --fixture-root.

This starts no sh -c, bash -c, eval, command substitution or intermediate wrapper. The launcher constructs the verified uv/Python/permgate argv. Do not fall back to shell form when exec-form support is absent: stop for a reviewed amendment.

Exec form removes the extra outer-shell startup path. The hook host's own process environment and inherited loader inputs while starting /usr/bin/env remain residual until the host supplies a clean environment at exec or the P1-16 OS user boundary exists. Neither env -i, -p nor a launcher check retroactively closes that residual.

Replace the validator's literal permgate-claude substring rule with exact equality of the command string and ordered args array against the complete rendered canonical exec form, including --manifest. Both modify scripts use that same comparison for bound-form classification. Do not join args into a shell string, compare shlex tokens, normalize strings or discard quoting from legacy comparisons.

Refuse absent args, shell-form substitutes, missing, reordered or extra args, an altered manifest operand, production --fixture-root, --script, nonisolated Python, shim paths and shell suffixes. Retain ccgate refusal, hook order, duplicate detection, synchronous timeout budgets and onFailure block.

Classify the legacy managed form separately. Replace stale managed hooks once, preserve custom hooks and converge idempotently. Retain quote-preserving raw-string distinctions for legacy shell fixtures. Keep each surface's P1-15 event inventory; do not import live orchestrator settings or add an event to a surface that lacks it. Run the existing ClaudeSettingsMergeTest legacy/custom fixtures unchanged.

### Scoped entrypoint inventory

The render regression checks exact command/args, executes the hook as [command, *args] with shell=False, and resolves the executable and interpreter operands in actual invocations under PATH=/usr/bin:/bin.

- PermissionRequest: /usr/bin/env with the literal clean-prefix args, /bin/bash --noprofile --norc -p, the canonical launcher, --manifest and optional explicitly named fixture root, then permission-request. After manifest and binary validation the parent execs `<abs uv> run --no-config --no-project --isolated --offline --python <abs python> python -I <abs permgate> claude`, preserving hook stdin, stdout and exit status.
- Deployment: the same launcher, clean prefix, production manifest and verified uv/Python perform the explicit online seed below. Subsequent checker/generator commands use isolated offline uv/Python with cached --with pyyaml and the same private cache. The checker runs validate-agent-assets.py --check-effective-settings. Its generated-config child re-enters the same parent with the same manifest and runs `<abs uv> run --no-config --no-project --isolated --offline --with pyyaml --python <abs python> python -I <abs generator> --check` from the canonical repository cwd.
- Fixture subjects: the same launcher with the explicitly named fixture manifest and root, real uv/Python and unchanged permgate bytes, together with the generator, validator and both modify scripts. Every bound Python child uses -I. A child importing yaml uses the same offline --with pyyaml pattern after explicit fixture-cache provisioning.
- Formatter interpreter check: the same launcher validates the declared node and starts its verified realpath with the probed installed Prettier script. Makefile format PATH includes node's declared bin directory so its env-node shebang resolves.

Only canonical scoped invocations are accepted. PermissionRequest accepts its selector after the required manifest arguments and constructs the fixed command internally. Other scoped operations, including the seed, must match their exact bound argv. Arbitrary executable forwarding, caller-selected executable directories and alternate executable operands are forbidden.

Add --check-effective-settings as an opt-in mode and expose the concrete trusted launch in Makefile. Ordinary validate-agent-assets and render-check stay pure. The opt-in mode reads effective installed settings, requires their exact production wiring and manifest operand, and checks existence, regular/executable identity, canonical protected paths and exact declared versions before operation execution. It consumes checked realpaths without rediscovery. It does not silently create a manifest, provision a cache, install tools or retry online.

### Private cache and explicit online seed

The trusted parent supplies an absolute UV_CACHE_DIR: protected main-checkout .agents/worklog/uv-cache for orchestrator/deploy runs, launcher-supplied <worktree>/.uv-cache for workers, and a temporary cache for tests. Parent and child refuse absent or relative caches; children do not derive defaults.

Retain round 3's bound online-seed decision. The operator's deployment sequence is: make update and deterministic production-manifest preparation, explicit private-cache seed through the trusted parent, then the isolated offline deployment check. The worker does not perform live deployment.

Use this seed command, replacing placeholders with shell-quoted absolute bound operands and using the canonical repository cwd:

```text
/usr/bin/env -i PATH=/usr/bin:/bin HOME=<rendered passwd-home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR=<canonical repository root> CLAUDE_ENV_FILE= UV_CACHE_DIR=<private cache> /bin/bash --noprofile --norc -p <abs trusted launch> --manifest <abs rendered production manifest> <abs uv> run --no-config --no-project --isolated --with pyyaml --python <abs python> python -I -c "import yaml"
```

The parent performs the same entry, manifest, cache, uv and Python checks before the seed as before every other bound operation. It compares executable operands with its verified manifest paths and execs only the exact PyYAML-import argv. Relative to the offline PyYAML form, only --offline is omitted. Retain --no-config, --no-project, --isolated, --with pyyaml, --python <verified abs python> and python -I. The [uv command reference](https://docs.astral.sh/uv/reference/cli/#uv-run) supplies the option semantics.

Record the selected manifest's canonical path and SHA-256, the complete seed command with expanded bound paths, output and actual exit status in validation.md. Carry the seed status and evidence into acceptance. Propagate the seed's exit status. A failed seed blocks later offline deployment commands; none downloads or seeds implicitly.

The checker and its yaml-importing generator child use that same manifest and cache through the parent. Never substitute the resolver's base Python or sys.executable directly for the uv-provided PyYAML environment.

Record the actual positive deployment result from the operator's host after make update and manifest preparation. CI fixture execution does not substitute for that host result.

## Fixture and regression contract

### Real fixture-manifest execution on runners

The harness discovers real uv by inspecting shutil.which("uv"), rejecting a shims component before and after resolution, then searching the actual mise uv install root if needed. Prefer the pinned version's directory when present and use the newest exact installed version only as a harness fallback. Handle the probed platform subdirectory rather than assuming <version>/uv. Resolve sys.executable for real Python and reject shims. Record the discovery result, canonical identities and actual versions.

The harness renders a fixture manifest with exact declarations and versions for those real tools, then supplies that manifest through --manifest and the test's canonical temporary directory through --fixture-root. HOME remains the real uid's passwd home.

The fixture must satisfy exact relative-path composition and containment. If a discovered executable is outside the permitted home/fixture binding, materialize the real executable bytes and the Python runtime support needed for a working installation under the fixture root, using regular files rather than symlink bindings. Verify the copied executable bytes against their discovered sources and verify the staged interpreter actually runs with -I. Copy necessary runtime/stdlib files; do not replace Python with a wrapper or a fake executable. Preserve unchanged real permgate bytes under the fixture root.

The launcher sees only the declared fixture paths, validates them through the production code path and compares their actual versions with the fixture pins. Do not pass a runner's external absolute sys.executable as an unchecked exception, redirect production HOME, disable a check, or force the fixture through the production-only mise resolver.

Execute the rendered hook as [command, *args] with shell=False and a fake PermissionRequest payload. Substitute only the documented host placeholder. Require real uv, real isolated Python and unchanged real permgate, with no wrapper or fake on the positive path. Assert the expected permgate decision, not merely process startup or argv recording.

Plant .pth and usercustomize.py markers in a fake user site and assert neither executes. Include hostile uv.toml, .venv and startup/PYTHON* inputs. Confirm the supplied clean prefix and isolated invocation prevent their consumption without changing real user-site files or installations.

This fixture execution is required on CI runners with setup-uv and their ordinary Python installation; it does not require the production mise installation. There is no fixture-execution skip for missing production pins. Failure to discover or prepare real fixture tools is a failed or blocked check with its exact reason, never green evidence.

### Separate pinned-installation case

Add a separate test of the exact production manifest bindings on a host with the pinned mise installation. It must execute the real bound hook path without substituting fixture pins or accepting a fallback version.

Elsewhere, skip only this pinned-installation test with the named reason `pinned-installation-unavailable`, recording the missing exact installation paths. An existing symlinked, malformed, mismatched or otherwise invalid installation is a refusal/failure, not absence and not a skip. Record every such skip in validation.md and report.md. Obtain the real host result during operator deployment; a runner's required fixture execution remains separate.

### Named regressions

Add or extend these eight regressions in the real existing classes, recording the full selectors and running their unittest dotted equivalents red before implementation and green afterward:

- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_trusted_entrypoint_manifest_matches_mise
- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_every_bound_entrypoint_resolves_with_system_path
- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_permission_request_uses_real_isolated_uv
- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_permission_request_uses_pinned_installation
- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_trusted_entrypoint_consumers_migrate
- tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_bound_permission_request_structure
- tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_effective_settings_checks_binary_identity
- tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_trusted_launch_validates_manifest

The manifest/mise regression checks production declarations, deterministic manifest rendering and exact version equality with the read-only mise declaration. Fixture pins are tested against their actual fixture executables, not against production versions.

The system-PATH regression checks /usr/bin/env as the hook executable, the exact clean assignments before /bin/bash --noprofile --norc -p, the canonical launcher, required manifest operand and operation. Assert shell=False, no outer-shell invocation, and exact fixture-root argument placement when testing the fixture form.

The structure and migration regressions include a hostile CLAUDE_PROJECT_DIR value containing spaces and a -- word, such as `project path -- injected`. Host substitution must preserve one args element. Both bound classifiers compare the exact command string and ordered args array; splitting the value or joining args into a shell string must fail.

Retain the round-2 quoted/unquoted legacy shell fixture pair whose shlex tokens are equal. Refuse both as the active canonical hook and preserve their raw-string distinction during legacy classification. Preserve custom hooks, stale managed-form replacement and repeated-merge idempotence.

The manifest regression exercises the actual launcher with otherwise valid fixture bindings and covers:

- A regular manifest outside both the repository and named fixture root, refused with manifest-path before any declared binary executes.
- A sibling-prefix or symlink escape outside those roots, also refused with manifest-path.
- A missing, relative or duplicated --manifest operand, malformed manifest data and an invalid fixture-root operand, with their specific refusal codes.
- A valid regular fixture manifest under the explicitly named fixture root, proving the same path accepts its declared real uv/Python without the production mise installation.

The binary-identity regression uses that accepted fixture-manifest path to reach the intended binary check. Cover a declaration naming a shim, a symlinked binary pointing to a marker-writing fake uv, and a path under an explicitly forbidden worker-writable root. Assert exit 2, the specific uv-path or python-path refusal and absent marker. A prior manifest, HOME or missing-installation refusal does not cover these cases. Also cover an exact-version mismatch after valid path checks.

In a separate non-skippable seed subcase, place an argument-recording fake uv as a regular executable at the fixture's declared canonical path. Its --version response matches the fixture pin. Execute the actual seed launch through the parent with shell=False and --manifest/--fixture-root. Assert the complete /usr/bin/env -i … /bin/bash --noprofile --norc -p prefix, verified absolute uv/Python operands and the recorded argv:

```text
run --no-config --no-project --isolated --with pyyaml --python <abs python> python -I -c "import yaml"
```

The final import is one argument. Assert absence of --offline, the exact clean environment and absolute private UV_CACHE_DIR, and seed exit-status propagation. Missing or relative caches must refuse without executing fake uv. This case uses no network and is evidence of invocation and refusal behavior only.

Also seed a fixture private cache explicitly through the same parent and isolated seed argv with real bound uv/Python, then prove the generator child's exact offline --with pyyaml argv, shared cache and successful yaml import. An isolated base-Python-only child must not satisfy this assertion. Sandbox or network denial is reported as blocked, without an outside-sandbox retry.

The fake-uv refusal and seed-recording subcases are not positive hook or deployment evidence. Structural, migration, manifest-boundary, identity and seed-recording cases never depend on the pinned-installation skip.

Exercise design item 7's hostile PATH, hostile Git environment/configuration, worker-root path and validation-to-consumption replacement cases for the scoped mechanisms, using the common helper when available. Prove no planted payload executes and state the same-UID replacement residual honestly.

No guard/delivery/state-helper descendant migration, permgate policy/source change, dependency, workflow change or worker live deployment is authorized.

## Measurement and caps

Historical touched-function spans are renderer 88, validator 13+33+79+11+26=162 and orchestrator modify 8+12=20 lines. P1-15's inspected worker modify module is 63 lines: 88+162+20+63=333 existing touched lines. The launcher has a zero-line baseline because the probed path is absent: 333+0=333. Existing target test modules total 95+1781=1876 lines.

The P1-15 files are an unmerged worker-e snapshot, not accepted-base measurements. Remeasure on the dispatch baseline and record the actual spans and file totals before implementation.

Production allowance, counted as additions plus deletions, is manifest/template 50 + renderer and manifest serialization 80 + both modify scripts 100 + validator 190 + Makefile 40 + launcher including shared manifest parsing, containment, identity and hook/seed dispatch 160 + margin 10 = 630 changed lines.

Test allowance is real execution/rendering and fixture preparation 260 + migration 100 + validator identities/refusals 220 + pin/shape checks 70 + environment/node cases 90 + pre-exec symlink case 40 + hostile quoting case 20 + yaml-child/cache case 20 + exec-form hook case 10 + online-seed prefix/argv case 30 + manifest-boundary cases 80 + separate pinned-installation case 40 = 980 changed lines.

The re-plan therefore raises the production cap from 500 to 630 and the test cap from 800 to 980 for the explicitly named manifest and fixture work. Runtime manifest data is not an executable helper. Count any tracked runtime configuration as production rather than hiding it in evidence totals. Reports and review evidence are excluded. Do not raise a cap or omit a consumer: stop for another split.

## Check

Run make unit-test, make format, make validate-agent-assets and make render-check, the eight named regressions, and unchanged tests.unit.test_claude_settings_merge, tests.unit.test_generate_agent_configs, tests.unit.test_statusline_tools and tests.unit.test_herdr_agents. Do not run Bats locally.

Record exact commands, statuses, red/green commits, discovered and staged real-tool identities, manifest hashes, fixture results, the named pinned-installation skip or host result, and baseline failures in validation.md. A failed or blocked check is not green. CI must execute the real fixture-manifest hook case without the pinned mise installation; the pinned-installation case has its separate recorded outcome.

Measure git diff --numstat origin/main...HEAD: at most 630 changed lines outside tests/ and .orchestration/, and at most 980 under tests/. Include any production configuration placed elsewhere in the production total.

The orchestrator compares the dispatched copy and TASK SHA-256 and runs the accepted base's regime-ci.py --base <base40> --head <head40> --root <base-checkout> under the trusted Python prefix. Report any unverifiable-copy warning. Check C7b row units and any C11 closed-row selectors explicitly.

Before completion run make require-crit-review with read/resolved local agent evidence and its receipt, then use Playbook step 10 at integration. Neither drafting this text nor passing a fixture authorizes deployment or merging.

## Completion

Current bindings override the historical identifiers, paths, branch/PR and deletion instructions inside the following source quotation: create tools/trusted-entrypoint-binding-a01 and one new PR from the accepted dispatch baseline; all artifacts, PONG ids and task_copy bind to dotfiles-T133-trusted-entrypoint-binding-a01, no predecessor deletion is authorized, and the orchestrator creates dotfiles-T133-trusted-entrypoint-binding-followup-a01 before advisory dispositions. Preserve the full executable-binding finding history, the C-92 fixture-vs-binding re-plan and D-024-26. The source Completion is otherwise verbatim, with the requested advisory-owner substitution.

Report the production and fixture manifest identities separately. Include the real fixture-hook outcome, pinned-installation result or named skip, each manifest/binary refusal, quote-preserving comparison evidence and bound seed evidence. The operator's later deployment result remains a distinct acceptance item; do not claim it from CI.

> Bindings for this new task: create a fresh `tools/loop-limits-a01` branch and one new PR from the dispatched baseline; predecessor head is not applicable. All current artifact paths, task-copy hashes and PONG task ids bind to `dotfiles-T133-loop-limits-a01`. Keep the first push's task copy byte-identical; no predecessor deletion is authorized. The orchestrator creates `dotfiles-T133-trusted-entrypoint-binding-followup-a01` before dispositioning advisory rows. The quotation below preserves the source Completion verbatim except for the requested advisory-owner substitution; its historical PR, branch and predecessor bindings are superseded by this paragraph.
>
> One existing PR, #424, on `tools/ci-efficiency-followup-a02`, continuing from `67e2cc98`; the predecessor’s fresh-branch requirement is superseded. Keep its implementation, tests, commits and historical evidence. In the first a04 push delete `.orchestration/dotfiles-T133-ci-efficiency-followup-a02/task.md` and add `.orchestration/dotfiles-T133-ci-efficiency-followup-a04/task.md` byte-identically to the dispatched a04 text. That single predecessor-file deletion is the reset transition authorized by C3; do not rewrite or move the predecessor’s other evidence.
>
> Write current `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence under `.orchestration/dotfiles-T133-ci-efficiency-followup-a04/`. Record the predecessor head, exact final head and base, branch, PR, changed files, row-to-test mapping, red/green commits, cap totals, evidence paths and `task_copy=<sha256 of .orchestration/dotfiles-T133-ci-efficiency-followup-a04/task.md>`. Preserve historical claims as historical; they do not approve the new head.
>
> The inherited Completion rules apply with these explicit bindings: advisory P2 and P3 belong to `dotfiles-T133-trusted-entrypoint-binding-followup-a01`, with rows recorded by the orchestrator before disposition. Do not reopen that owner’s advisory work in this task unless a narrow revise explicitly authorizes it.
>
> Every fix round counts toward INV-6, including worker-side fixes before the first RESULT; C-61 permits at most two in this task, and amendments and questions retain their own counters. A rebase repair qualifies only under D-024-24 and cannot hide a security fix. Another repeated-class finding or exhausted counter stops work for the orchestrator’s recorded re-plan; do not continue under a new label.
>
> A P0/P1 surviving the permitted worker-side fix round is sent as `open:<id>` in the RESULT, including `open:review-<id>` for a review-body finding, with the applicable round count. It stops integration for the operator’s decision; never convert it into an advisory disposition or perform another unauthorized fix round.
>
> Wait for final-head CI and the bounded automatic Bot-review window. Record `bot: none` if the window expires. **Do not post `@codex review`**, at the ten-minute mark or after a fix. The orchestrator replies to and resolves GitHub review threads.
>
> Every `gh` command and every `git` write is an individual command **inside the sandbox**, including pushes and authenticated fetches. No compound write commands, outside-sandbox retries, excluded-command workaround, permission escalation or alternate tool to bypass a denial. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-ci-efficiency-followup-a04 status=blocked` naming the exact command, failure and crossed boundary; preserve the evidence and wait.
>
> The orchestrator performs final-head review and the security-profile review, then follows Orchestrator Playbook step 10 for CI, feedback sweep, task-level audit, finding dispositions, acceptance, gate and head-bound merge. The worker does not merge or remove workers.
>
> Implementation, runtime tests and CI are not claimed checked by this task draft; dispatch remains held on the stated prerequisites. Same-UID replacement and shared-credential risks remain residual.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
Not checked: implementation, runtime tests, CI, live dispatch or operator-host deployment.
Risk: pending prerequisites, same-UID replacement, shared credentials and inherited descendant bindings remain residual.
```

---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-pins-a01
kind: code
security: true
allowed_files: ["home/dot_mise/config.toml","tests/unit/test_generate_agent_configs.py",".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**"]
after: []
threat_table:
  - {"control":"home/dot_mise/config.toml","disposition":"residual: Pin only uv, Python and node to the primary task's probed versions; this intentionally stops their latest-version tracking."}
  - {"control":"tests/unit/test_generate_agent_configs.py","disposition":"residual: Keep an exact source-manifest/rendered-command equality check and executable leaf/argument checks, plus explicit pin assertions; do not delete legacy fixture coverage."}
  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**","disposition":"residual: Only task copy and review/validation/report data are authorized; no helper or runtime code is placed here."}
  - {"control":"task copy .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/task.md","disposition":"residual: The orchestrator compares the full dispatched bytes and SHA-256 before accepting this prerequisite."}
  - {"control":"task metadata","disposition":"residual: This is an independent three-entry prerequisite task; it grants no write permission for the later binding implementation."}
  - {"control":"metadata separators","disposition":"residual: Parse as data with duplicate keys refused and compare the complete dispatched task copy."}
  - {"control":"in-process effects","disposition":"residual: Tests and fixture renders use temporary directories; no mise install, update, apply or live hook execution is authorized."}
  - {"control":"workflow and interpreter or environment inputs","disposition":"residual: The exact declaration is changed intentionally; trusted-entrypoint implementation remains in the primary task."}
  - {"control":"new or renamed scripts","disposition":"residual: None is authorized; retain existing generator and test helpers."}
  - {"control":"orchestrator effect merge","disposition":"residual: The orchestrator alone integrates after full final-head evidence and Playbook step 10."}
  - {"control":"orchestrator effect update-branch","disposition":"residual: A moved head requires refreshed checks and integration evidence under the orchestrator's control."}
  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; the worker cannot remove seats or discard another worktree."}
  - {"control":"design 5.14 item 0 same-UID model","disposition":"residual: Exact pins do not separate OS identities or shared GitHub credentials."}
  - {"control":"design 5.14 item 1 protected inputs","disposition":"residual: The exact declaration becomes a trusted input; worker write protection remains pending until P1-15 is accepted and deployed."}
  - {"control":"design 5.14 item 2 clean environment","disposition":"residual: No new production execution path is introduced; inherited check launch trust is not established by a pin."}
  - {"control":"design 5.14 item 3 paths","disposition":"residual: The declaration path is fixed and unchanged; installation path validation belongs to the resolver and primary task."}
  - {"control":"design 5.14 item 4 verified bytes","disposition":"residual: Whole-task and final-head evidence are compared; local files remain replaceable by unrestricted same-UID processes."}
  - {"control":"design 5.14 item 5 identity","disposition":"residual: Use full head/base and task-copy SHA-256 in evidence; no new lock or reservation is created."}
  - {"control":"design 5.14 item 6 honest residuals","disposition":"residual: Pin assertions prove declarations only, not installed binary identity or successful hook execution."}
  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the pin regression red then green and retain generator/merge consumers; general hostile-execution closure is not claimed."}
  - {"control":"design 5.14 item 8 approval","disposition":"residual: Pins and local evidence are proposals until integration; neither grants permission or merge authority."}
  - {"control":"design 5.14 item 9 isolation","disposition":"residual: This task supplies exact version input only; the accepted resolver and primary task implement isolated execution and private caches."}
  - {"control":"design 5.14 item 10 sandbox","disposition":"residual: All commands stay in the sandbox; denied commands produce blocked evidence without escalation."}
premises:
  - {"command":"grep -nE '^(uv|python|node) = ' home/dot_mise/config.toml | paste -sd '|' -","output":"3:node = \"latest\"|5:python = \"latest\"|17:uv = \"latest\""}
  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | paste -sd '|' -","output":"home/dot_mise/config.toml|tests/unit/test_generate_agent_configs.py"}
  - {"command":"wc -l .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | xargs","output":"63 .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json 95 .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py 1781 tests/unit/test_validate_agent_assets.py 79 home/dot_mise/config.toml 2350 tests/unit/test_generate_agent_configs.py 4368 total"}
  - {"command":"grep -nE '^    def test_managed_hooks_use_installed_permgate_paths' tests/unit/test_generate_agent_configs.py | paste -sd '|' -","output":"1417:    def test_managed_hooks_use_installed_permgate_paths(self) -> None:"}
  - {"command":"sed -n '1417,1422p' tests/unit/test_generate_agent_configs.py | wc -l | xargs","output":"6"}
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-pins-a01 — prerequisite split for exact tool pins

Worker: a Codex seat (worktree named at dispatch)

This is the second, separate task file, with exactly three allowed_files entries. Accept it before dispatching ci-efficiency-followup-a04 or the primary binding task. The primary task above contains the shared host probes and C-88 quotations; these bind the version choices here and do not authorize the primary implementation in this prerequisite.

Pin uv=0.13.1, python=3.15.0 and node=26.12.0 in home/dot_mise/config.toml, replacing only those latest values. Add one English comment explaining the trusted-entrypoint pins; preserve every other tool and setting. Do not install or apply anything.

In GenerateAgentConfigsTest add test_trusted_entrypoint_mise_versions_are_exact, red before the config change and green afterward. Refactor test_managed_hooks_use_installed_permgate_paths to compare the complete rendered PermissionRequest command with the real manifest declaration rendered through the existing template helper; retain exactly one managed entry, permgate executable-leaf/claude-argument checks and the Codex assertion. Keep synthetic legacy-command fixtures. The primary task adds strict bound-sequence and parent-selected-manifest validation.

Measured declaration: 79 lines; touched existing test: 6 lines at 1417–1422 in a 2350-line module. Source allowance is 3 additions+3 deletions+1 reason comment+1 margin=8 lines; fixture/assertion work 60+margin 20=80 test lines. Enforce these separate caps with git diff --numstat origin/main...HEAD; evidence is excluded, executable source is not.

Check: make unit-test, make format, make validate-agent-assets, make render-check, tests.unit.test_generate_agent_configs and the new pin regression. Do not run Bats locally. Use the primary task's accepted-checker and regime-copy checks for this task's own id/copy; report blocked or baseline-failing checks honestly.

Completion: create tools/trusted-entrypoint-pins-a01 and one PR; write task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence under .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/. The primary task's quoted Completion round, sandbox, CI/Bot and integration rules apply with this task's own identifiers; no predecessor deletion is authorized. Advisory owner is dotfiles-T133-trusted-entrypoint-binding-followup-a01, created before disposition. Only the orchestrator integrates; no deployment is claimed.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
Not checked: implementation, runtime tests, CI or deployment.
Risk: the primary binding work and same-UID/shared-credential residuals remain.
```---
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice2-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - scripts/generate-agent-configs.py
  - home/.chezmoitemplates/claude-worker-settings.json
  - home/.chezmoitemplates/claude-managed-settings.json
  - home/dot_claude-worker/modify_private_settings.json
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_claude_worker_settings.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice2-a01/**
after: [dotfiles-T133-worker-write-boundary-slice1-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice2-a01 — P1-15 slice 2: startup screening and the worker/admin outputs (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat so that slice 1 can name this task as the owner of the obligations it defers (C-51). The dispatch text is authored by `author-loop.sh` from the allocation brief (`.agents/worklog/orchestrator-glue/a04-allocation-r1.md`, slice 2) after slice 1 merges; this stub is never dispatched.

## Scope (from the allocation table)

Register both generated outputs (worker and admin settings) in the same change as their preparation consumer. Implement the single preflight: the S01-S23 startup-source inventory, executable-file contents, S11 discard/regenerate, every launch route, narrow interpreter consumption and the runtime-name classes. The guard and the guarded tracked settings already exist (slice 1). Existing unguarded main-local settings refuse unchanged; accepting those installations waits for slice 3 and the deployment. Administrative content is generated but has no installation target yet. Launcher changes are extracted selectively from the preserved a03 draft (`tools/worker-write-boundary-a01`); documentation and ignore assertions wait for slice 4. No live dependents are released.

## Obligations owned for slice 1

Design 5.14 item 1 (startup enforcement, configuration reloads, races and live refusal), the launch-route regressions of the S11 and executable-file contracts that slice 1 only declares, and the foreign-root refusal identifier (this task's dispatched id replaces a04's).

## Intermediate condition after merge (E2)

`make render-check`, `make validate-agent-assets`, the five E1 modules plus the complete `tests.unit.test_claude_worker_settings` pass; required GitHub CI green; final-head review, audit and security evidence fresh.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
---
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice5-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - .claude/settings.json
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice5-a01/**
after: [dotfiles-T133-worker-write-boundary-slice4-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice5-a01 — P1-15 slice 5: activate the tracked hooks on the installed guard (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51) after the third C-80 round of slice 1 (`…-text-security-f4246e9.md.last.md`): switching the tracked hook commands in `.claude/settings.json` to `~/.claude/hooks/orchestrator-only.sh` before that guard is installed removes the stop gate from every session that loads the tracked settings, and `onFailure: block` cannot protect `Stop`. Activation therefore follows provisioning: slice 1 renders the guard template and the migration logic but leaves the tracked commands unchanged; the deployment stage A (`make update`, `make install-managed-settings`, the administrative installation) provisions the guard on the host; this slice switches the tracked references afterwards, with a test that the referenced guard path exists in the rendered deployment inventory before the switch is accepted.

## Scope

`.claude/settings.json`: replace the current tracked hook commands with the fixed guard invocation (exec form, absolute `--manifest` operand, supported `onFailure` block) only for hooks whose guard target the deployment inventory lists as installed; the regression test asserts the inventory check and the unchanged behaviour of hooks without an installed guard.

## Owned for slice 1

The tracked-hook activation and its ordering after stage A (slice 1 row ".claude/settings.json" is out of slice 1's scope and names this task).

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```

 succeeded in 227ms:
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
# Notes every review-profile brief carries (orchestrator glue, 2026-10-20)

1. Host facts measured before authoring, pasted verbatim: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`. A text names a resolve command and asks the worker to paste its output, never a guessed path (re-plan validation-setup of regime-ci-token-a01).
2. Every evidence item names its producer and seat kind: `orchestrator (Claude seat, sandboxed Bash)` or `worker (<kind> seat)`. A Codex seat cannot probe the herdr socket from its sandbox (PermissionDenied measured 2026-10-20T13:39Z, a013); never ask it to (M-20261020-06/08 class).
3. The self cap leaves room for the orchestrator's Checks block (about 7 lines) when the text keeps a fenced block under `## Checks`; a reset text anchored by a review is dispatched at the anchored bytes with no paste.
4. No restatement of the trusted-execution contract: design 5.14 items by reference; environment and executable rows the tool cannot close are `residual` with an owner (re-plan contract-restatement of regime-ci-token-a01). Texts for security: false tools get no C-80 (D-024-46).
5. Caps in the C-107 sentence form; the numstat command in its own sentence; measurement base pasted at dispatch (the branch head at dispatch for a records-only round after an update-branch, not an older code head).
6. Baseline statements bind to the post-prerequisite state: a text that names `after:` prerequisites describes main as it will be after they merge (their post-merge effects stated in the brief), never as it is on the authoring day (slice 1 of P1-15, 2026-10-21: an old Linux exclusion policy was preserved against a prerequisite that empties it).

    96	Absent, legacy, malformed, duplicate-field, untrusted-location or mismatched artifacts require review in that private worktree and atomic replacement of the protected artifact after successful review; identifiers alone do not authenticate its producer.
    97	On fetch failure emit `local-review: private fetch failed`; on missing/non-commit/mismatched head or base emit `local-review: private commit check failed`; exit 2, call no reviewer, create/rewrite no artifact and never fall back.
    98	Remove only this invocation's private repository/worktree on completion/refusal; preserve failed-review transcripts and inherited exit-4 behavior without retaining reusable success for the failed invocation.
    99	Change `chain-integrate.sh`'s actual review/advisory exec sites to establish design 5.14 item 2 before either child's shell/loader starts, using anchored script bindings; satisfy its own entry requirements under the orchestrator-controlled outer parent, with no self-reexec repair.
   100	Add `tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1`: execute the actual changed caller/consumer path from the trusted fixture parent with hostile inherited startup/loader inputs; assert no payload/decoy execution, exact private handoff, exit 11 on private P1 despite legacy zero and no downstream sweep/audit.
   101	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects`: stub gh/git, plant forged shared-object content, serve different canonical content through explicit-URL private fetch, and make the reviewer read its actual cwd; assert consumed canonical content, isolated inputs and object provenance.
   102	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_refuses_a_failed_private_fetch_or_commit_check`: cover fetch failure and each missing/non-commit/mismatched head/base, with a matching private cache planted; assert named refusal, no reviewer, no artifact creation/rewrite and no fallback.
   103	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache`: plant matching shared head/findings-zero artifacts, also matching base/tree; assert fresh lookup/fetch, canonical-cwd review and protected rewrite.
   104	That cache test proves lookup/fetch precede any cache read, valid protected head/base/tree skips only the model, changed/missing/duplicate metadata or inconsistent counts reruns it, and failed lookup/fetch cannot return cached success; it proves identity/rejection, not producer authenticity.
   105	Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_rejects_shared_scratch_and_worker_private_roots` for shared TMPDIR, worker roots and aliases; fixtures prove path refusals only, never live worker write isolation.
   106	Revise inherited tests that demand PATH-selected `mise which`, `command -v`/interpreter fallback or exactly two Codex overrides: assert design 5.14 items 4/9 bindings and an actually spawned Git's resolved executable/environment after Codex-policy filtering, including a shim/decoy attack.
   107	Record each new regression red against `a644a7d9` on its security assertion, then green; separately disclose bootstrap-only fixture adaptations. Retain traversal, literal-path, shebang-argument/refusal, owner/repeat, output and failure regressions with safe fixtures.
   108	
   109	## Check and Completion
   110	
   111	Host facts: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
   112	Run that uv resolve command as a host observation and paste actual output; bind validation operands under design 5.14 items 2/4/9, record interpreter realpath/version, and never guess an uv path or use the observation as production runtime discovery.
   113	Run the bound uv/Python equivalents of `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` and `uv run python -m unittest tests/unit/test_chain_glue.py -v` under design 5.14 items 2/9; record complete actual argv/output/status.
   114	Run `bash -n` on all three changed shell scripts, `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/chain-integrate.sh` and applicable repository lint; comments use English shdoc; never run Bats locally.
   115	The whole PR has at most 120 changed lines outside `tests/` and `.orchestration/`, and 400 under `tests/`, counting additions plus deletions; attribute inherited 26 outside-test lines and 69 test lines separately from this reset's corrections, including caller edits.
   116	Run `git --git-dir=<private-bare> diff --numstat <base40>...<head40>` in the authenticated private repository using resolved full SHAs and record complete output before cleanup.
   117	The orchestrator pastes the resolved measurement base at dispatch; attribute inherited/new changes against that base and final head, including a branch-head base for any records-only round after update-branch; an overrun blocks, never raises caps.
   118	Keep the complete dispatched text at or under 140 lines, reserving seven for Checks; no workflow, permission, dependency, launcher, knowledge-graph, predecessor-artifact or a09-owned changes are authorized.
   119	Worker Playbook step 4 applies: every a013 command, including gh, Git and agmsg delivery, stays sandboxed; push without `-u` over HTTPS with `git push https://github.com/mryfmo/dotfiles.git tools/chain-review-scripts-followup-a07`; every denial records command/status/boundary and sends blocked PONG without escalation/substitution.
   120	Do not probe the herdr socket; placement/delivery verification and host-deployment evidence belong to the orchestrator. Keep plan/todo/learn uncommitted and at most one active todo per owner.
   121	Copy these complete dispatched bytes to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md`; keep the retained a07 task copy/evidence unchanged; no executable helper may be hidden in the artifact wildcard.
   122	Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and `-worker-` crit-data/receipt evidence under the a08 directory; follow repository review gates without browser/human review, record provenance and `cost:`.
   123	Each evidence item names `worker (Codex seat, a013)` or `orchestrator (Claude seat, sandboxed Bash)`; identify separate authoring/inherited producers honestly and include exact commands, operands, statuses, complete outputs and refusals without secrets.
   124	Keep evidence untracked at the same relative paths in worker-h when main-checkout paths are inaccessible; RESULT identifies their location for orchestrator transfer.
   125	This text's C-80 round 2 addresses supplied round 1; at most two C-80 text-review rounds total, no private third round. Keep INV-6/a07 counters and the one worker Bot fix-round limit; surviving P0/P1 goes to the operator.
   126	After final push verify GitHub Actions and wait for final-head Bot feedback under the Worker Playbook; the worker proposes dispositions and resolves no threads.
   127	RESULT names PR, full head/base, branch, changed files, selectors, red/green commits, caps/attribution, artifact paths and `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md>`.
   128	The orchestrator records counters before acceptance, carries a07 history, then performs final-head sweep, task audit, security review, acceptance and gate in Playbook step 10 order; changed heads repeat required evidence; advisory ownership remains `dotfiles-T128-chain-review-scripts-followup-a09`.
   129	Not performed by this authoring context: implementation edits, worker tests, live fetch, CI or deployment.
   130	Shared credentials and unrestricted same-UID interference remain residual; fixture results cannot authorize production cache reuse or integration before the declared deployment prerequisites.
   131	
   132	## Checks (pasted by the orchestrator before each send)
   133	

**Noticing token limits**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md | head -150; sed -n '56,185p' scripts/orchestrator/chain-integrate.sh" in ~/Workspace/dotfiles
 succeeded in 30ms:
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
   116	These are two separate task files. This primary task has exactly ten allowed_files entries: eight exact implementation/test paths, one modify-script glob and one evidence wildcard. The glob authorizes only home/dot_claude/modify_private_settings.json and home/dot_claude-worker/modify_private_settings.json, each with its own threat row. An additional match requires a reviewed split. The second file below owns mise pins and the generator assertion; do not combine their front matter or dispatch this task before that prerequisite is accepted.
   117	
   118	## Dispatch prerequisites and scope
   119	
   120	Accept dotfiles-T133-trusted-entrypoint-pins-a01 before the Python-resolver dependency is dispatched; the historical probe says latest for all three tools. Accept both after dependencies and verify P1-15's deployed protection before sending this task.
   121	
   122	The seven existing concrete allowlist paths were on origin/main at the recorded probe. P1-15 creates the worker modify script and ClaudeManagedSettingsTest module. Add scripts/orchestrator/trusted-launch.sh as the only new executable source. Recheck these paths and measurements on the actual dispatch baseline; refresh changed premises through a reviewed, hashed amendment before dispatch, never only in the Checks paste.
   123	
   124	The installed a04 resolver remains read-only. Its existing consumers retain its production-pinned contract. For the scoped launcher, this re-plan explicitly replaces the earlier instruction to obtain Python unconditionally from that resolver: resolve and validate the exact Python declaration in the parent-selected manifest, using the same code for production and fixtures. Do not edit the resolver, add PATH discovery to production, or make a fixture satisfy an unrelated host's mise pin.
   125	
   126	The root C11 test file was absent at the recorded probe, and the inspected worker-g copy accepted tests/<path>::<identifier> rather than a Class::test payload. The orchestrator must obtain and read the accepted checker/test revision before dispatch, check C1–C10, C7b and C11, and manually re-probe premises. Never execute arbitrary premise shell strings through an unchecked checker.
   127	
   128	Each threat-table file row names one file or one allowed wildcard only. This draft makes no closed claims. Any later closed row must name exactly one selector in the form tests/<path>::<Class>::<test>; a module name, free-function selector or prose reference is insufficient.
   129	
   130	## Applicable design — C-88 verbatim quotations
   131	
   132	`$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, section 5.14, is uncommitted design input. The relied-on sentences of items 1, 2 and 9 are quoted verbatim below. The parent-selected manifest contract is this re-plan's explicit scoped replacement for an unconditional production-pinned resolver call.
   133	
   134	> The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19).
   135	>
   136	> A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
   137	>
   138	> One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
   139	
   140	## Implementation contract
   141	
   142	### Declarations and deterministic rendering
   143	
   144	Declare production uv 0.13.1 at .local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv, Python 3.15.0 at .local/share/mise/installs/python/3.15.0/bin/python3.15, and node 26.12.0 at .local/share/mise/installs/node/26.12.0/bin/node, relative to the real uid's passwd home. A test compares all three production versions with home/dot_mise/config.toml. No wildcard, version alias, latest, shim, traversal or missing required declaration is accepted. If accepted pins differ from these probes, stop for a re-probed amendment rather than substituting an installed version.
   145	
   146	Rendering composes the supplied home and repository bindings with these declarations and validates shape only. It remains deterministic on a host with no installs. Use the same native expansion in both modify-script consumers and the validator renderer, with correct JSON and shell quoting, including homes and repository paths containing spaces.
   147	
   148	Render the launcher manifest as data from the source manifest. The fixed production destination is <canonical repository root>/.agents/worklog/trusted-entrypoint-manifest, outside worker-writable roots. It is an operator-provisioned runtime data artifact, not a new tracked source file or an executable under the evidence wildcard. The operator materializes it during deployment preparation before enabling the changed hook. Tests render into their temporary fixture root. Ordinary generation and render-check compare the deterministic rendering without requiring or writing the installed production artifact.
   149	
   150	Use one small, documented data grammar that the privileged-shell launcher can parse with fixed absolute system tools before executing any declared uv or Python. Treat every field as literal data: no source, eval, shell expansion, command substitution or declared-interpreter bootstrap. Reject malformed, duplicate, unknown or missing required fields. Declare exact relative paths and exact versions; declarations must not select arbitrary commands. The production manifest also carries the rendered worker-root inventory used by containment checks.
task=$1 pr=$2 owner=$5 extra=${6:-}
# Both ids become path segments under .orchestration/ and record content; the leading class excludes . and ..
for v in "${task}" "${owner}"; do
    [[ ${v} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || refuse 10 "invalid argument: ${v}"
done
[[ ${pr} =~ ^[0-9]+$ ]] || refuse 10 "invalid argument: ${pr}"
main=$(cd -- "$3" 2> /dev/null && pwd -P) || refuse 10 "invalid argument: $3"
cd -- "${main}"
# Resolved before any fetch or checkout and run by absolute path, as local-review.sh resolves codex: a mise shim
# would pick its binary by the directory it runs in.
pick() { env -i PATH="${PATH}" HOME="${HOME}" mise which "$1" 2> /dev/null || command -v "$1" || true; }
gh=$(pick gh) git=$(pick git) uv=$(pick uv) shasum=$(pick shasum) date=$(pick date)
for found in "${gh}" "${git}" "${uv}" "${shasum}" "${date}"; do
    [[ ${found} == /* && ${found} != */shims/* ]] || refuse 10 "no binary outside a shims directory: ${found:-none}"
done
[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || refuse 10 "main checkout is not on main"
fresh() { pre "${git}" -C "${main}" fetch -q origin main && pre "${git}" -C "${main}" rev-parse HEAD origin/main && { [ "${out%%$'\n'*}" = "${out##*$'\n'}" ] || refuse 10 "main checkout is not origin/main: run scripts/orchestrator/ff-main.sh"; }; }
fresh
# They run with the orchestrator's credentials, so each must be HEAD's own copy (PR #372 thread 4291474880).
for s in scripts/orchestrator/{sandbox-scan.sh,local-review.sh,local-advisory.sh,fill_sweep.py,acceptance-front-matter.py,orch-audit.sh} scripts/pr-feedback.py; do
    "${git}" -C "${main}" ls-files --error-unmatch -- "${s}" > /dev/null 2>&1 || refuse 10 "${s} is not tracked in the main checkout"
done
"${git}" -C "${main}" diff --quiet HEAD -- scripts || refuse 10 "scripts/ in the main checkout differs from HEAD"
pre "${git}" -C "${main}" rev-parse --show-toplevel
canonical=${out}/.claude/worktrees/orchestrator-review
review=$(cd -- "$4" 2> /dev/null && pwd -P) || review=$4
[ "${review}" = "${canonical}" ] || refuse 10 "review worktree is not the canonical one: ${canonical}"
[ -e "${review}/.git" ] || refuse 10 "review worktree is not a worktree root"
pre "${git}" -C "${review}" status --porcelain
[ -z "${out}" ] || refuse 10 "review worktree is not clean"
record=${main}/.orchestration/acceptance/${task}.md
[ -f "${record}" ] || refuse 10 "no acceptance record ${record#"${main}"/}"
pre "${gh}" pr view "${pr}" --json isDraft --jq .isDraft
[ "${out}" = false ] || refuse 10 "draft PR: the worker marks it ready"
pre "${git}" -C "${review}" fetch -q origin main
# The log names repository paths only, so an extra TSV must be in the main checkout (PR #372 thread 4291474891).
[ -z "${extra}" ] || extra=$(cd -- "$(dirname -- "${extra}")" 2> /dev/null && pwd -P)/${extra##*/}
[[ -z ${extra} || ${extra} == "${main}"/* ]] || refuse 10 "extra dispositions TSV is not in the main checkout: $6"
export ORCH_REVIEW_WORKTREE=${review}
v=${main}/.orchestration/validation
for attempt in 1 2 3; do
    step fetch 0 "${git}" -C "${main}" fetch -q origin "+pull/${pr}/head:refs/remotes/pr/${pr}"
    step fetch 0 "${git}" -C "${review}" fetch -q origin "+pull/${pr}/head"
    step fetch 0 "${git}" -C "${review}" checkout -q --detach FETCH_HEAD
    step fetch 0 "${git}" -C "${review}" rev-parse HEAD
    head=${out}
    step fetch 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid
    [ "${out}" = "${head}" ] || refuse 10 "head mismatch: re-run"
    sha7=${head:0:7}
    # The log is named by the head, so the lines before it are written once it is known; a new head's log holds them all.
    [ "${log}" = "${v}/${task}-chain-${sha7}.log" ] || { log=${v}/${task}-chain-${sha7}.log && printf '%s\n' "${lines[@]}" >> "${log}"; }
    [ ! -e "${v}/${task}-audit-${sha7}.md.last.md" ] || refuse 10 "head already audited: one chain per head"
    step base 0,1 "${git}" -C "${review}" merge-base --is-ancestor origin/main HEAD
    if ((rc == 0)); then
        step checks any "${gh}" pr checks "${pr}" --required --watch
        ((rc == 0)) || refuse 12 "required checks failed"
        # Plan 020 step 4: the Bot wait is never gated, so it ends present or absent and the chain goes on.
        q="[.[] | select(.user.login == \"chatgpt-codex-connector[bot]\" and .commit_id == \"${head}\")] | length"
        t0=$("${date}" +%s)
        while step bot 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/reviews" --paginate --jq "${q}"; do
            n=$((${out//$'\n'/+})) # one count per page
            ((n == 0 && $("${date}" +%s) - t0 < ${CHAIN_BOT_WAIT:-900})) || break
            sleep 30
        done
        say "bot review: $( ((n > 0)) && echo present || echo absent)"
        # origin/main can move during the waits (PR #372 thread 4291474885): a moved base is updated, then the fetch.
        step base 0 "${git}" -C "${review}" fetch -q origin main
        step base 0,1 "${git}" -C "${review}" merge-base --is-ancestor origin/main HEAD
        ((rc == 1)) || break
    fi
    ((attempt < 3)) || refuse 13 "base moved three times"
    step base 0 "${gh}" pr update-branch "${pr}"
    t0=$("${date}" +%s) # GitHub builds the merge commit asynchronously: poll the head check's query until it moves.
    while step base 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid && [ "${out}" = "${head}" ]; do
        (($("${date}" +%s) - t0 < ${CHAIN_POLL_MAX:-120})) || refuse 10 "update-branch head not visible"
        sleep "${CHAIN_POLL_SECONDS:-5}"
    done
    fresh  # a moved base may have left the main checkout's main behind, which local-review.sh diffs against
    log='' # the next head's log takes every line; this one ends here
done
# C-29: the scan reports and exits 0, so the chain is the stop its reader used to be.
step sandbox-scan 0 "${main}/scripts/orchestrator/sandbox-scan.sh" "${task}"
[ -z "${out}" ] || say "${out}"
if [[ ${out} == *"sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"* ]]; then
    [ "${CHAIN_SCAN_JUDGED:-}" = "${sha7}" ] || refuse 16 "sandbox scan hit: judge it, then re-run with CHAIN_SCAN_JUDGED=${sha7}"
    say "sandbox scan: judged by the orchestrator"
fi
step local-review 0,3 "${main}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
findings=0
[[ ! ${out} =~ local-review:\ ([0-9]+)\ findings ]] || findings=${BASH_REMATCH[1]}
if ((rc == 3)); then
    [ -f "${main}/.orchestration/tasks/${owner}.md" ] || refuse 15 "write the owner task ${owner} first"
    step local-advisory 0,3 "${main}/scripts/orchestrator/local-advisory.sh" "${task}" "${head}" "${owner}"
    ((rc == 0)) || refuse 11 "a P0/P1 local finding: the one round or the operator"
fi
sweep=${v}/${task}-pr-feedback.json comments=${v}/${task}-pr-comments.json
step pr-feedback 0 "${uv}" run --no-project python -I "${main}/scripts/pr-feedback.py" "${pr}" --json "${sweep}"
step fill-sweep 0 "${gh}" api user --jq .login
login=${out}
# One compact object per line, joined into one array, so a second page does not end the JSON after the first.
step fill-sweep 0 "${gh}" api "repos/{owner}/{repo}/pulls/${pr}/comments" --paginate --jq '.[]'
printf '[%s]\n' "${out//$'\n'/,}" > "${comments}"
step fill-sweep 0,1 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/fill_sweep.py" "${sweep}" "${comments}" ${extra:+"${extra}"} --orchestrator-login "${login}"
rm -f -- "${comments}"
gaps=unknown
[[ ! ${out} =~ gaps\ ([0-9]+) ]] || gaps=${BASH_REMATCH[1]}
((rc == 0)) || refuse 14 "sweep gaps: ${gaps}"
now=$("${date}" -u +%FT%TZ)
body="orchestrator integration review of PR #${pr} at ${head}: local review ${findings} finding(s), each with its line in the acceptance record; sweep complete"
printf '[{"id": "%s", "scope": "review", "resolved": true, "author": "claude-code", "head": "%s", "pr": "%s", "reviewed_at": "%s", "body": "%s"}]\n' \
    "${task}-pr${pr}-review-1" "${head}" "${pr}" "${now}" "${body}" > "${v}/${task}-crit.json"
say "${now} receipt rc=0: printf > .orchestration/validation/${task}-crit.json"
printf 'review_surface: crit-data\nreviewer: claude-code\nreview_source: %s\nreview_outcome: approved\nhead: %s\npr: %s\nreviewed_at: %s\nnote: %s\n' \
    ".orchestration/validation/${task}-crit.json" "${head}" "${pr}" "${now}" \
    "${body} (chain-integrate.sh; the task-level audit of this head is recorded separately in .orchestration/validation/${task}-audit-${sha7}.md)" \
    > "${v}/${task}-review-receipt.md"
say "${now} receipt rc=0: printf > .orchestration/validation/${task}-review-receipt.md"
# The gate's LEDGER_ID: a thread id of ten or more digits or audit:<sha7>:<n>; local: rows stay in the prose.
tsv=${v}/${task}-ledger-${sha7}.tsv
step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
printf '%s\n' "${out}" > "${tsv}"
step record 0 "${uv}" run --no-project python -I "${main}/scripts/orchestrator/acceptance-front-matter.py" "${task}" "${sweep}" "${review}" --ledger "${tsv}"
rm -f -- "${tsv}"
# C-61 (plan 023 F1): an update-branch-only head, a merge of main into the audited head whose PR patch is unchanged,
# inherits that head's audit under its own names; the first line names the head the audit ran on, whose ids it keeps.
# --verbatim keeps whitespace in the id, so a whitespace-only change is a new patch (PR #390 thread 4302490292).
patch() { "${git}" -C "${main}" diff-tree -p "$("${git}" -C "${main}" merge-base origin/main "$1")" "$1" | "${git}" -C "${main}" patch-id --verbatim; }
parent=$("${git}" -C "${main}" rev-parse -q --verify "${head}^1" || true) old='' new=''
from=${v}/${task}-audit-${parent:0:7}
if [[ -n ${parent} && -f ${from}.md && -f ${from}.md.last.md ]] && "${git}" -C "${main}" merge-base --is-ancestor "${head}^2" origin/main 2> /dev/null; then

**Analyzing Git hook security risks**
**Reviewing config isolation and trust boundaries**
exec
/bin/zsh -lc "git show a644a7d965399b9463e9b32721287440a7efa233:scripts/orchestrator/chain-integrate.sh | sed -n '55,105p'; git show a644a7d965399b9463e9b32721287440a7efa233:scripts/orchestrator/local-advisory.sh | sed -n '30,96p'; rg -n 'git|gh|codex|chain|ledger|canonical|out.of.scope|after:' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md | tail -24; rg -n 'threat.table|non-path|closed.*selector|owning task' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 35ms:
(($# == 5 || $# == 6)) || refuse 10 "invalid argument: chain-integrate.sh <task> <pr> <main> <review> <owner> [<extra tsv>]"
task=$1 pr=$2 owner=$5 extra=${6:-}
# Both ids become path segments under .orchestration/ and record content; the leading class excludes . and ..
for v in "${task}" "${owner}"; do
    [[ ${v} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || refuse 10 "invalid argument: ${v}"
done
[[ ${pr} =~ ^[0-9]+$ ]] || refuse 10 "invalid argument: ${pr}"
main=$(cd -- "$3" 2> /dev/null && pwd -P) || refuse 10 "invalid argument: $3"
cd -- "${main}"
# Resolved before any fetch or checkout and run by absolute path, as local-review.sh resolves codex: a mise shim
# would pick its binary by the directory it runs in.
pick() { env -i PATH="${PATH}" HOME="${HOME}" mise which "$1" 2> /dev/null || command -v "$1" || true; }
gh=$(pick gh) git=$(pick git) uv=$(pick uv) shasum=$(pick shasum) date=$(pick date)
for found in "${gh}" "${git}" "${uv}" "${shasum}" "${date}"; do
    [[ ${found} == /* && ${found} != */shims/* ]] || refuse 10 "no binary outside a shims directory: ${found:-none}"
done
[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || refuse 10 "main checkout is not on main"
fresh() { pre "${git}" -C "${main}" fetch -q origin main && pre "${git}" -C "${main}" rev-parse HEAD origin/main && { [ "${out%%$'\n'*}" = "${out##*$'\n'}" ] || refuse 10 "main checkout is not origin/main: run scripts/orchestrator/ff-main.sh"; }; }
fresh
# They run with the orchestrator's credentials, so each must be HEAD's own copy (PR #372 thread 4291474880).
for s in scripts/orchestrator/{sandbox-scan.sh,local-review.sh,local-advisory.sh,fill_sweep.py,acceptance-front-matter.py,orch-audit.sh} scripts/pr-feedback.py; do
    "${git}" -C "${main}" ls-files --error-unmatch -- "${s}" > /dev/null 2>&1 || refuse 10 "${s} is not tracked in the main checkout"
done
"${git}" -C "${main}" diff --quiet HEAD -- scripts || refuse 10 "scripts/ in the main checkout differs from HEAD"
pre "${git}" -C "${main}" rev-parse --show-toplevel
canonical=${out}/.claude/worktrees/orchestrator-review
review=$(cd -- "$4" 2> /dev/null && pwd -P) || review=$4
[ "${review}" = "${canonical}" ] || refuse 10 "review worktree is not the canonical one: ${canonical}"
[ -e "${review}/.git" ] || refuse 10 "review worktree is not a worktree root"
pre "${git}" -C "${review}" status --porcelain
[ -z "${out}" ] || refuse 10 "review worktree is not clean"
record=${main}/.orchestration/acceptance/${task}.md
[ -f "${record}" ] || refuse 10 "no acceptance record ${record#"${main}"/}"
pre "${gh}" pr view "${pr}" --json isDraft --jq .isDraft
[ "${out}" = false ] || refuse 10 "draft PR: the worker marks it ready"
pre "${git}" -C "${review}" fetch -q origin main
# The log names repository paths only, so an extra TSV must be in the main checkout (PR #372 thread 4291474891).
[ -z "${extra}" ] || extra=$(cd -- "$(dirname -- "${extra}")" 2> /dev/null && pwd -P)/${extra##*/}
[[ -z ${extra} || ${extra} == "${main}"/* ]] || refuse 10 "extra dispositions TSV is not in the main checkout: $6"
export ORCH_REVIEW_WORKTREE=${review}
v=${main}/.orchestration/validation
for attempt in 1 2 3; do
    step fetch 0 "${git}" -C "${main}" fetch -q origin "+pull/${pr}/head:refs/remotes/pr/${pr}"
    step fetch 0 "${git}" -C "${review}" fetch -q origin "+pull/${pr}/head"
    step fetch 0 "${git}" -C "${review}" checkout -q --detach FETCH_HEAD
    step fetch 0 "${git}" -C "${review}" rev-parse HEAD
    head=${out}
    step fetch 0 "${gh}" pr view "${pr}" --json headRefOid --jq .headRefOid
    [ "${out}" = "${head}" ] || refuse 10 "head mismatch: re-run"
    sha7=${head:0:7}
    # The log is named by the head, so the lines before it are written once it is known; a new head's log holds them all.
    echo "usage: local-advisory.sh <task> <40-hex head> <owner task>"
    exit 2
}
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
# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
O=".orchestration/tasks/$owner.md"
[ -f "$O" ] || {
    echo "write the owner task $owner first"
    exit 2
}
sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
earlier=""
for f in .orchestration/validation/"$task"-local-review-*.md; do
    [[ -f $f && $f != "$LR" ]] || continue
    # The exact prefix is stripped, so the whole rest of the name must be the head: a name with a second
    # `-local-review-` cannot pass as its last part (the audit of 000c5c6, finding 1).
    e=${f%.md} && e=${e#.orchestration/validation/"$task"-local-review-} && k=0
    # Only a seven-hex suffix names a reviewed head; any other file is skipped (the audit of d3e8acf, finding 1).
    [[ $e =~ ^[0-9a-f]{7}$ ]] || continue
    while IFS= read -r l; do
        k=$((k + 1))
        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
done
# A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
i=0 stop=0
while IFS= read -r line; do
    i=$((i + 1))
    case "$line" in
    *"[P0]"* | *"[P1]"*)
        echo "STOP: local finding $i of $h7 is P0/P1: $line"
        stop=1
        ;;
    *)
        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
        class=advisory-p2 repeat=""
        t=$(token "$line") || t=""
        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
        if [[ -n $t && -n $ids ]]; then
            # A row's id is its first tab-separated field, compared as text, never as a pattern.
            row=$(awk -F'\t' -v ids="${ids%|}" 'BEGIN { n = split(ids, a, "|"); for (j = 1; j <= n; j++) s[a[j]] = 1 } NF > 1 && ($1 in s) && $0 !~ /\tadvisory-p2$/' "$A" | tail -1 || true)
            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
        fi
        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
        ;;
    esac
done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
echo "local review of $h7: $i finding(s) recorded as advisory under 'Owned by $owner' in $A"
[ "$stop" = 0 ] || exit 3
201:- Deployment: the same launcher, clean prefix, production manifest and verified uv/Python perform the explicit online seed below. Subsequent checker/generator commands use isolated offline uv/Python with cached --with pyyaml and the same private cache. The checker runs validate-agent-assets.py --check-effective-settings. Its generated-config child re-enters the same parent with the same manifest and runs `<abs uv> run --no-config --no-project --isolated --offline --with pyyaml --python <abs python> python -I <abs generator> --check` from the canonical repository cwd.
205:Only canonical scoped invocations are accepted. PermissionRequest accepts its selector after the required manifest arguments and constructs the fixed command internally. Other scoped operations, including the seed, must match their exact bound argv. Arbitrary executable forwarding, caller-selected executable directories and alternate executable operands are forbidden.
207:Add --check-effective-settings as an opt-in mode and expose the concrete trusted launch in Makefile. Ordinary validate-agent-assets and render-check stay pure. The opt-in mode reads effective installed settings, requires their exact production wiring and manifest operand, and checks existence, regular/executable identity, canonical protected paths and exact declared versions before operation execution. It consumes checked realpaths without rediscovery. It does not silently create a manifest, provision a cache, install tools or retry online.
213:Retain round 3's bound online-seed decision. The operator's deployment sequence is: make update and deterministic production-manifest preparation, explicit private-cache seed through the trusted parent, then the isolated offline deployment check. The worker does not perform live deployment.
215:Use this seed command, replacing placeholders with shell-quoted absolute bound operands and using the canonical repository cwd:
218:/usr/bin/env -i PATH=/usr/bin:/bin HOME=<rendered passwd-home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR=<canonical repository root> CLAUDE_ENV_FILE= UV_CACHE_DIR=<private cache> /bin/bash --noprofile --norc -p <abs trusted launch> --manifest <abs rendered production manifest> <abs uv> run --no-config --no-project --isolated --with pyyaml --python <abs python> python -I -c "import yaml"
223:Record the selected manifest's canonical path and SHA-256, the complete seed command with expanded bound paths, output and actual exit status in validation.md. Carry the seed status and evidence into acceptance. Propagate the seed's exit status. A failed seed blocks later offline deployment commands; none downloads or seeds implicitly.
225:The checker and its yaml-importing generator child use that same manifest and cache through the parent. Never substitute the resolver's base Python or sys.executable directly for the uv-provided PyYAML environment.
233:The harness discovers real uv by inspecting shutil.which("uv"), rejecting a shims component before and after resolution, then searching the actual mise uv install root if needed. Prefer the pinned version's directory when present and use the newest exact installed version only as a harness fallback. Handle the probed platform subdirectory rather than assuming <version>/uv. Resolve sys.executable for real Python and reject shims. Record the discovery result, canonical identities and actual versions.
235:The harness renders a fixture manifest with exact declarations and versions for those real tools, then supplies that manifest through --manifest and the test's canonical temporary directory through --fixture-root. HOME remains the real uid's passwd home.
239:The launcher sees only the declared fixture paths, validates them through the production code path and compares their actual versions with the fixture pins. Do not pass a runner's external absolute sys.executable as an unchecked exception, redirect production HOME, disable a check, or force the fixture through the production-only mise resolver.
255:Add or extend these eight regressions in the real existing classes, recording the full selectors and running their unittest dotted equivalents red before implementation and green afterward:
268:The system-PATH regression checks /usr/bin/env as the hook executable, the exact clean assignments before /bin/bash --noprofile --norc -p, the canonical launcher, required manifest operand and operation. Assert shell=False, no outer-shell invocation, and exact fixture-root argument placement when testing the fixture form.
272:Retain the round-2 quoted/unquoted legacy shell fixture pair whose shlex tokens are equal. Refuse both as the active canonical hook and preserve their raw-string distinction during legacy classification. Preserve custom hooks, stale managed-form replacement and repeated-merge idempotence.
283:In a separate non-skippable seed subcase, place an argument-recording fake uv as a regular executable at the fixture's declared canonical path. Its --version response matches the fixture pin. Execute the actual seed launch through the parent with shell=False and --manifest/--fixture-root. Assert the complete /usr/bin/env -i … /bin/bash --noprofile --norc -p prefix, verified absolute uv/Python operands and the recorded argv:
291:Also seed a fixture private cache explicitly through the same parent and isolated seed argv with real bound uv/Python, then prove the generator child's exact offline --with pyyaml argv, shared cache and successful yaml import. An isolated base-Python-only child must not satisfy this assertion. Sandbox or network denial is reported as blocked, without an outside-sandbox retry.
313:Run make unit-test, make format, make validate-agent-assets and make render-check, the eight named regressions, and unchanged tests.unit.test_claude_settings_merge, tests.unit.test_generate_agent_configs, tests.unit.test_statusline_tools and tests.unit.test_herdr_agents. Do not run Bats locally.
317:Measure git diff --numstat origin/main...HEAD: at most 630 changed lines outside tests/ and .orchestration/, and at most 980 under tests/. Include any production configuration placed elsewhere in the production total.
341:> Wait for final-head CI and the bounded automatic Bot-review window. Record `bot: none` if the window expires. **Do not post `@codex review`**, at the ten-minute mark or after a fix. The orchestrator replies to and resolves GitHub review threads.
343:> Every `gh` command and every `git` write is an individual command **inside the sandbox**, including pushes and authenticated fetches. No compound write commands, outside-sandbox retries, excluded-command workaround, permission escalation or alternate tool to bypass a denial. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-ci-efficiency-followup-a04 status=blocked` naming the exact command, failure and crossed boundary; preserve the evidence and wait.
363:after: []
390:  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | paste -sd '|' -","output":"home/dot_mise/config.toml|tests/unit/test_generate_agent_configs.py"}
404:In GenerateAgentConfigsTest add test_trusted_entrypoint_mise_versions_are_exact, red before the config change and green afterward. Refactor test_managed_hooks_use_installed_permgate_paths to compare the complete rendered PermissionRequest command with the real manifest declaration rendered through the existing template helper; retain exactly one managed entry, permgate executable-leaf/claude-argument checks and the Codex assertion. Keep synthetic legacy-command fixtures. The primary task adds strict bound-sequence and parent-selected-manifest validation.
406:Measured declaration: 79 lines; touched existing test: 6 lines at 1417–1422 in a 2350-line module. Source allowance is 3 additions+3 deletions+1 reason comment+1 margin=8 lines; fixture/assertion work 60+margin 20=80 test lines. Enforce these separate caps with git diff --numstat origin/main...HEAD; evidence is excluded, executable source is not.
71:- A task that touches a trust boundary (anything the design tier lists, CI that decides a required check, code that executes PR-controlled input) carries a `threat_table` in its front matter: one `{control, disposition}` row per thing the PR or the orchestrator controls (the tree and its tests, task.md, workflow files, interpreter and environment files, in-process effects, new or renamed scripts, metadata separators). The row unit is one row per `allowed_files` entry, one row per listed control that is not a path (task metadata, workflow and interpreter or environment inputs, in-process effects, new or renamed scripts, metadata separators), carried by the declared test module's row where that is where the control acts, and one row per orchestrator effect from the fixed list (forced removal, merge, update-branch); under a wildcard `allowed_files` entry whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow), one row per concrete file the PR changes; a wildcard over test fixtures or other data files keeps one row; C4 and C7b of `scripts/orchestrator/task-consistency-check.py` verify the path half before dispatch, and the task-file review checks the rest. A disposition takes one of three forms: `closed: tests/<file>::<name>`, the test that closes the row; `residual: <sentence>`, the compensating control; `out-of-scope: <task id>`, the task that owns the row. The task-file review checks the three shape rules by hand: a `closed` selector names a test present in the PR tree at acceptance, an `out-of-scope` owner is a task id in the design's `implementing_tasks`, a `residual` payload is a sentence of at least 20 characters (the gate's minimum for a reason). For a `closed` row it checks the selector's form only, since the test does not exist before implementation. Substance is the reviewers': the task-file review, the Bot and the auditor judge each row against the diff. The table is the task's completion condition: a missing row is added once, counted as an amendment, never fixed finding by finding.

**Focusing on targeted data search**
exec
/bin/zsh -lc "sed -n '1,104p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md; sed -n '1,140p' .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md; sed -n '90,109p' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md" in ~/Workspace/dotfiles
 succeeded in 55ms:
---
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice2-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - scripts/generate-agent-configs.py
  - home/.chezmoitemplates/claude-worker-settings.json
  - home/.chezmoitemplates/claude-managed-settings.json
  - home/dot_claude-worker/modify_private_settings.json
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_claude_worker_settings.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice2-a01/**
after: [dotfiles-T133-worker-write-boundary-slice1-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice2-a01 — P1-15 slice 2: startup screening and the worker/admin outputs (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat so that slice 1 can name this task as the owner of the obligations it defers (C-51). The dispatch text is authored by `author-loop.sh` from the allocation brief (`.agents/worklog/orchestrator-glue/a04-allocation-r1.md`, slice 2) after slice 1 merges; this stub is never dispatched.

## Scope (from the allocation table)

Register both generated outputs (worker and admin settings) in the same change as their preparation consumer. Implement the single preflight: the S01-S23 startup-source inventory, executable-file contents, S11 discard/regenerate, every launch route, narrow interpreter consumption and the runtime-name classes. The guard and the guarded tracked settings already exist (slice 1). Existing unguarded main-local settings refuse unchanged; accepting those installations waits for slice 3 and the deployment. Administrative content is generated but has no installation target yet. Launcher changes are extracted selectively from the preserved a03 draft (`tools/worker-write-boundary-a01`); documentation and ignore assertions wait for slice 4. No live dependents are released.

## Obligations owned for slice 1

Design 5.14 item 1 (startup enforcement, configuration reloads, races and live refusal), the launch-route regressions of the S11 and executable-file contracts that slice 1 only declares, and the foreign-root refusal identifier (this task's dispatched id replaces a04's).

## Intermediate condition after merge (E2)

`make render-check`, `make validate-agent-assets`, the five E1 modules plus the complete `tests.unit.test_claude_worker_settings` pass; required GitHub CI green; final-head review, audit and security evidence fresh.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
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

  - {"command":"python3 -I -B -c 'from pathlib import Path; roots=(Path(\"home\"),Path(\".claude/worktrees/worker-e/home\")); print(\"|\".join(str(p) for root in roots for p in sorted(root.glob(\"dot_claude*/modify_private_settings.json\"))))'","output":"home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json"}
  - {"command":"python3 -I -B -c 'import os,pwd,stat; from pathlib import Path; h=Path(pwd.getpwuid(os.getuid()).pw_dir); u=h/\".local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\"; r=u.resolve(strict=True); print(\"home_matches_passwd=\"+str(Path.home()==h)); print(\"uv_regular=\"+str(stat.S_ISREG(u.lstat().st_mode))); print(\"uv_symlink=\"+str(u.is_symlink())); print(\"uv_under_passwd_install_root=\"+str(r.is_relative_to(h/\".local/share/mise/installs\"))); print(\"uv_declared_equals_realpath=\"+str(u==r)); print(\"trusted_launch_exists=\"+str(Path(\"scripts/orchestrator/trusted-launch.sh\").exists()))'","output":"home_matches_passwd=True\nuv_regular=True\nuv_symlink=False\nuv_under_passwd_install_root=True\nuv_declared_equals_realpath=True\ntrusted_launch_exists=False"}
  - {"command":"rg -n '^    import yaml|PyYAML is required' scripts/generate-agent-configs.py | paste -sd '|' -","output":"14:    import yaml|34:        fail(\"PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py\")"}
  - {"command":"sed -n '1294,1298p' scripts/validate-agent-assets.py | paste -sd '|' -","output":"def validate_generated_agent_configs() -> None:|    result = subprocess.run(|        [sys.executable, str(ROOT / \"scripts/generate-agent-configs.py\"), \"--check\"],|        cwd=ROOT,|        text=True,"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B scripts/generate-agent-configs.py --check","output":"ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py","exit_status":1}
  - {"command":"claude --version","output":"2.1.300 (Claude Code)","exit_status":0}
  - {"command":"python3 -I -B -c 'from pathlib import Path; b=(Path.home()/\".local/share/mise/installs/npm-anthropic-ai-claude-code/latest/bin/claude\").read_bytes(); s=b\"Command hooks require `command`. For exec form (no shell)\"; i=b.find(s); print(b[i:b.index(b\"\\0\",i)].decode() if i>=0 else \"missing exec-form help\")'","output":"Command hooks require `command`. For exec form (no shell), set `command` to the executable and `args` to its arguments: {\"type\": \"command\", \"command\": \"echo\", \"args\": [\"hi\"]}. For shell form, set `command` to the full shell string: {\"type\": \"command\", \"command\": \"echo hi\"}.","exit_status":0}
  - {"command":"web.open https://code.claude.com/docs/en/hooks#exec-form-and-shell-form","output":"Command hook args present selects direct executable spawn without a shell; args omitted selects shell form (sh -c on macOS/Linux). command is the executable path and args is its argument vector. Documented path placeholders include ${CLAUDE_PROJECT_DIR} and are substituted as plain strings."}
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-binding-a01 — bind trusted entrypoints to a parent-selected manifest

Worker: a Codex seat (worktree named at dispatch)

Use the security profile for this Claude-boundary change. D-024-26 split this family from P1-15. Read the last 60 lines of .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md and .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-{f810c30,772cde0,e5c055e,5204254}.md.last.md: shebang discovery, Python startup injection, the checker's own execution, shim discovery, the real uv layout and Prettier's node must be handled together.

Read the complete binding acceptance record and these three pre-dispatch reviews:

- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-faae5f4.md.last.md
- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-8f5ac8d.md.last.md

**Verifying Git template and artifact security**
**Assessing ledger ownership and task scoping**
**Analyzing Git integrity risks**
**Examining Git config vulnerabilities**
exec
/bin/zsh -lc "git show a644a7d965399b9463e9b32721287440a7efa233:scripts/orchestrator/chain-integrate.sh | nl -ba | sed -n '169,240p'; rg -n 'inherit|GIT_|PATH|shell_environment|mcp|hooks' home/dot_agents/agent-config.yaml | head -38; wc -l .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md" in ~/Workspace/dotfiles
 succeeded in 78ms:
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
   195	        "${v}/${task}-chain-${parent:0:7}.log" 2> /dev/null || old=''
   196	    # Only a verdict the gate accepts is inherited (its AUDIT_VERDICT and AUDIT_FINDING): correct, or incorrect with a
   197	    # [P0-P3] line; a blocked, empty or finding-less parent result takes the fresh audit (audit:274a536:2).
   198	    last=$(/usr/bin/awk 'NF { l = $0 } END { print l }' "${from}.md.last.md")
   199	    [[ ${last} =~ ^[[:space:]]*Verdict:\ (correct|incorrect)[[:space:]]*$ ]] || old=''
   200	    [[ ${BASH_REMATCH[1]-} != incorrect ]] || /usr/bin/grep -qE '^[[:space:]]*([-*+][[:space:]]+)?\[P[0-3]\]' "${from}.md.last.md" || old=''
   201	fi
   202	if [[ -n ${old} && ${old%% *} == "${new%% *}" ]]; then
   203	    for s in .md .md.last.md; do
   204	        # A parent that inherited keeps its marker: the ids stay those of the head the audit ran on.
   205	        { [[ $(head -n 1 -- "${from}${s}") == inherited-from:* ]] || echo "inherited-from: ${parent:0:7}"; } > "${v}/${task}-audit-${sha7}${s}"
   206	        cat -- "${from}${s}" >> "${v}/${task}-audit-${sha7}${s}"
   207	    done
   208	    say "$("${date}" -u +%FT%TZ) audit rc=0: audit inherited from ${parent:0:7} ($(head -n 1 -- "${v}/${task}-audit-${sha7}.md.last.md"))"
   209	    echo "audit inherited from ${parent:0:7}"
   210	    verdict="chain-integrate: ${task} ${head} $(tail -n 1 -- "${v}/${task}-audit-${sha7}.md.last.md")"
   211	else
   212	    step audit 0 "${main}/scripts/orchestrator/orch-audit.sh" "${task}" "${review}" "${pr}"
   213	    verdict="chain-integrate: ${task} ${head} ${out##*$'\n'}"
   214	    step audit 0 "${git}" -C "${review}" checkout -q --detach "${head}" # orch-audit.sh leaves it at origin/main; the gate reads it
   215	fi
   216	say "${verdict}" && echo "${verdict}"
10:# - Store credentials as environment-variable references or inherited environment only.
121:  shell_environment_policy:
122:    inherit: core
124:      PATH: '{{ .chezmoi.homeDir }}/.local/share/mise/installs/node/lts/bin:{{ .chezmoi.homeDir }}/.local/share/mise/shims:{{ .chezmoi.homeDir }}/.local/bin:{{ .chezmoi.homeDir }}/.local/bin/common:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
127:    hooks: true
128:    plugin_hooks: true
141:  hooks:
146:    # Compaction and session end reach CompactionDB like Claude's hooks do; the
148:    command_hooks:
161:    # The hooks this repository ships or installs, trusted by `make update`: the modify scripts hash each
173:      crit@mryfmo-personal-plugins:hooks/hooks.json:stop:0:0:
176:      ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0:
179:      ponytail@ponytail:hooks/claude-codex-hooks.json:user_prompt_submit:0:0:
182:      ponytail@ponytail:hooks/claude-codex-hooks.json:subagent_start:0:0:
191:  mcp_config_path: home/dot_claude/private_mcp.json.tmpl
318:  hooks:
319:    enforce_uv_hook: ~/.claude/hooks/enforce-uv.sh
320:    format_edited_files_hook: ~/.claude/hooks/format-edited-files.py
321:    project_map_reload_hook: ~/.claude/hooks/project-map-reload.sh
328:        hooks:
333:            command: "bash '{{ .chezmoi.homeDir }}/.claude/hooks/herdr-agent-state.sh' session"
336:        hooks:
375:mcp_servers: {}
     133 .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md

**Finalizing test coverage findings**
**Summarizing test and audit coverage issues**

I'm working through three key findings: two high-priority issues around unsafe ownership chains and audit scope complexities, plus a medium-priority test coverage gap that doesn't fully prove fixes. There’s a tricky mismatch between declared owners and actual tool bindings, especially concerning Git and reviewer provisioning—notably missing explicit manifests or version pins, which impacts deployment and trust boundaries. I’m thinking about how these gaps relate to user expectations and the intended contract scope.
codex
private review の後も、継承した chain は共有 object store から監査の再利用可否を判断し、共有 review worktree を監査へ渡します。この経路は今回許可された呼び出し箇所の修正範囲に収まるかを確認しています。また、item 8 の `closed` テストが指定する検証は PR 内容の出所までで、台帳を読む経路は含まれていません。
**Analyzing chain resolution and test coverage**
**Summarizing mitigation requirements and integration scope**

I’m clarifying the minimal mitigation as holding the live chain until all consumers are authenticated or prerequisites arrive, ensuring the P1 and P2 tasks aren’t redundant. I’m considering permission boundaries around Codex reviewer subprocesses and potential injection risks via hooks, while noting no global integration owner is named. The goal is to produce a concise, precise final summary in both Japanese and English, formatted as clear single lines referencing exact local file paths per developer preference, staying within about 320 words.
codex
[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:22 The chain’s `closed` test stops on private P1 evidence before exercising the successful path: inherited `chain-integrate.sh:182–214` still decides audit reuse from worker-writable shared objects and passes the shared worktree to `orch-audit.sh`; protecting the new review store does not authenticate those inputs, and the task neither authorizes their replacement nor names their hardening as a release prerequisite.

[P2] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:42 The named test proves private PR-content consumption, not item 8’s committed-ledger requirement: retained advisory ownership/repeat decisions read local acceptance/task files, and no specified assertion checks their authenticated committed source; test those decision inputs or narrow this `closed` claim and assign the remaining control.

📝 まとめ: Reviewed the task, threat rows and cited context; found one remaining integration trust gap and one unsupported closure claim. No files changed.

Not checked: implementation, test execution or live deployment enforcement; these findings assess the stated design.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
92,727
[P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:22 The chain’s `closed` test stops on private P1 evidence before exercising the successful path: inherited `chain-integrate.sh:182–214` still decides audit reuse from worker-writable shared objects and passes the shared worktree to `orch-audit.sh`; protecting the new review store does not authenticate those inputs, and the task neither authorizes their replacement nor names their hardening as a release prerequisite.

[P2] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:42 The named test proves private PR-content consumption, not item 8’s committed-ledger requirement: retained advisory ownership/repeat decisions read local acceptance/task files, and no specified assertion checks their authenticated committed source; test those decision inputs or narrow this `closed` claim and assign the remaining control.

📝 まとめ: Reviewed the task, threat rows and cited context; found one remaining integration trust gap and one unsupported closure claim. No files changed.

Not checked: implementation, test execution or live deployment enforcement; these findings assess the stated design.
Verdict: incorrect
