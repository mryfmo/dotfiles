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
session id: 01a1621f-9ae6-7881-82b0-d46bc169bed2
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
指定されたタスク本文と参照証跡を読み、各制御が実際の実行対象に結び付くかを確認します。関連スキルのレビュー手順を使い、読み取り専用で進めます。

exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
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
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a01.md
 M .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a01.md
 M .orchestration/acceptance/dotfiles-T129-pstack-asset-a01.md
 M .orchestration/acceptance/dotfiles-T133-gh-binding-a02-review-a01.md
 M .orchestration/acceptance/dotfiles-T133-gh-binding-a02.md
 M .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
 M .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/plans/024-replan-20261021-v2.md
 M .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md
 M .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md
 M .orchestration/tasks/dotfiles-T129-pstack-asset-review-a01.md
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a02.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-crit.json
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-review-receipt.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02.md
?? .orchestration/acceptance/dotfiles-T129-pstack-asset-review-a01.md
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
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T129-pstack-asset-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-codex-network-policy-a01.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-herdr-agents-eperm-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
?? .orchestration/tasks/dotfiles-T133-orchestrator-inbox-loop-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-followup-a03.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-audit-b801369.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-2b58663.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-b801369.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-crit.json
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-local-review-2b58663.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-05000f4.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-5f9caa3.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-5f9caa3.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-d61a0f2.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-d61a0f2.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-0ecdc07.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-2adb147.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-2adb147.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-3c1d54a.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-63d69cc.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-728f0ff.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-728f0ff.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-86513b2.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-86513b2.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-b700fe8.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c0a7dae.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c761dc8.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md.last.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-44134e3.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-e6b645f.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-e6b645f.md.last.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-059a40c.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-44134e3.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-e6b645f.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-local-review-059a40c.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-local-review-e6b645f.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-1d72f16.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-chain-128a208.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-chain-a30a43b.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-local-review-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-pr-comments.json
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md
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
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-audit-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-audit-28dde0f.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-chain-28dde0f.log
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-local-review-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-1f17d05.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-28dde0f.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-401573e.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T129-hcom-dispatch-bus-a02
     4	kind: code
     5	security: true
     6	previous_sha256: 4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c
     7	reset_of: [dotfiles-T129-hcom-dispatch-bus-a01]
     8	dispatch_status: blocked-pre-anchor
     9	design_review: {design: .orchestration/plans/024-design-quality.md}
    10	after: [dotfiles-T133-gh-binding-a02]
    11	allowed_files:
    12	  - home/dot_local/bin/common/executable_hcom-dispatch
    13	  - scripts/orchestrator/bus-history.sh
    14	  - scripts/orchestrator/dispatch.sh
    15	  - scripts/orchestrator/bus-read.sh
    16	  - scripts/regime-counters.sh
    17	  - tests/unit/test_*.py
    18	  - scripts/update-agent-assets.sh
    19	  - scripts/lint-comparisons-baseline.tsv
    20	  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a02/**
    21	  - home/dot_agents/agent-config.yaml
    22	threat_table:
    23	  - {control: "home/dot_local/bin/common/executable_hcom-dispatch", disposition: "closed: tests/unit/test_hcom_dispatch.py::HcomDispatchTest::test_transport_matrix"}
    24	  - {control: "scripts/orchestrator/bus-history.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_history_matrix"}
    25	  - {control: "scripts/orchestrator/dispatch.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_dispatch_matrix"}
    26	  - {control: "scripts/orchestrator/bus-read.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_bus_read_matrix"}
    27	  - {control: "scripts/regime-counters.sh", disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_hcom_counter_matrix"}
    28	  - {control: "tests/unit/test_*.py (test_hcom_dispatch.py)", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; independent audit checks send argv and receipt assertions."}
    29	  - {control: "scripts/update-agent-assets.sh (amendment 2: one new target, update_hcom_private, installs the verified hcom wheel the receipt names into the anchored checkout's private tool directory with UV_TOOL_DIR and UV_TOOL_BIN_DIR under <checkout>/.agents/worklog/uv-tools; nothing else in the updater changes)", disposition: "closed: tests/unit/test_hcom_dispatch.py::test_update_hcom_private_installs_the_verified_wheel_into_the_private_tool_dir_leaves_the_public_entry_unchanged_and_refuses_a_drifted_wheel"}
    30	  - {control: "scripts/lint-comparisons-baseline.tsv (amendment 3: stale-row removal only; the five R1 rows of scripts/orchestrator/dispatch.sh at lines 109, 190, 202, 209 and 334 fall away with the lines the constraints rewrite; no row is added, every new hit is fixed in the allowed sources)", disposition: "closed: tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline (the existing lint test, run by make unit-test on the final head)"}
    31	  - {control: "tests/unit/test_orchestrator_tools.py", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; audit checks real reader/dispatcher assertions and red/green logs."}
    32	  - {control: "tests/unit/test_regime_counters.py", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; audit checks counts and preserved seam cases."}
    33	  - {control: ".orchestration/dotfiles-T129-hcom-dispatch-bus-a02/** including task.md", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence automation; independently compare anchored bytes, full heads and verbatim validation."}
    34	  - {control: "home/dot_agents/agent-config.yaml", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_production_store_declaration"}
    35	  - {control: "private namespace", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_namespace_matrix"}
    36	  - {control: "store identity", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hostile_hcom_store_refused"}
    37	  - {control: "consumed-bytes binding", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_consumed_bytes_matrix"}
    38	  - {control: "history format", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_marker_roundtrip"}
    39	  - {control: "history framing", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_history_forged_row_refused"}
    40	  - {control: "receipt identity", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_concurrent_identical_send_receipts"}
    41	  - {control: "status key", disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_status_revise_matrix"}
    42	  - {control: "bound gh calls", disposition: "residual: dotfiles-T133-gh-binding-a02 owns executable/configuration/host binding; dispatcher argv stubs establish only invocation shape, never that boundary."}
    43	  - {control: "task metadata including dotfiles-T129-hcom-dispatch-bus-a01/task.md and dotfiles-T129-hcom-dispatch-bus-a02/task.md", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns metadata automation; check complete reset bytes and format-2 consistency, never reuse a01 approval."}
    44	  - {control: "metadata separators", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence automation; bind the whole text including front matter, separators and Checks."}
    45	  - {control: "bus rows and routing identities", disposition: "closed: tests/unit/test_hcom_dispatch.py::HcomDispatchTest::test_identity_and_payload_matrix"}
    46	  - {control: "in-process effects", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_fixture_route_isolation"}
    47	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployment evidence; require measured design 5.14 items 1/2/9 before operational use."}
    48	  - {control: "new or renamed scripts", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_migration_item_matrix"}
    49	  - {control: "design 5.14 item 0", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns unchanged item 0 obligations; this task establishes no same-UID or credential-separation boundary."}
    50	  - {control: "design 5.14 item 1", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns protection measurements for the deployed manifest, tools, namespace, snapshots and evidence."}
    51	  - {control: "design 5.14 item 2", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_namespace_matrix"}
    52	  - {control: "design 5.14 item 3", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_trusted_path_matrix"}
    53	  - {control: "design 5.14 item 4", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_consumed_bytes_matrix"}
    54	  - {control: "design 5.14 item 5", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns unchanged lock/reservation obligations; retain full head identities and existing locking."}
    55	  - {control: "design 5.14 item 6", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployment verification; distinguish assertions, CI and observed host execution."}
    56	  - {control: "design 5.14 item 7", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_contract_attack_matrix"}
    57	  - {control: "design 5.14 item 8", disposition: "residual: dotfiles-T133-gh-binding-a02 owns bound gh authority; add no approval reader and certify no local-object boundary."}
    58	  - {control: "design 5.14 item 9", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_cache_matrix"}
    59	  - {control: "design 5.14 item 10", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns denial records; apply Worker Playbook step 4 without escalation."}
    60	  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns integration records; only the orchestrator integrates the audited full head through Playbook step 10."}
    61	  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence refresh; repeat CI, sweep, audit, acceptance and gate after any head change."}
    62	  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns teardown records; none is planned and dirty state cannot be discarded implicitly."}
    63	  - {control: "orchestrator effect owner-stub creation", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns all assigned residuals; create its task stub before anchor, outside worker scope."}
    64	  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns Checks provenance; populate post-prerequisite observations before review/anchor."}
    65	  - {control: "orchestrator effect PR 407 closure", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns continuity records; record closure of 407 in RESULT if replaced."}
    66	  - {control: "orchestrator effect deployment", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployed store declaration and real-host verification; fixtures never enable an unmeasured route."}
    67	premises: []
    68	---
    69	
    70	# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a02 — plan 023 PR C, stage 1
    71	
    72	Reset a01 (2026-10-18); retain items 0–7 and deferred work, with binding remedies for C-80 24d8b8d (2026-10-22T04:44Z: five P1/two P2) and a02 round 1 (framing, receipt identity, undeclared production store). Plan 024 phase 2 starts here (D-024-79/D-024-81). Worker: Claude seat a009 (worker-c).
    73	Design 5.14 items 0–10 in .orchestration/plans/024-design-quality.md apply by reference. Closed rows cover their named assertions; broader host/environment/executable risks remain with the residual owners. This is accident/prompt-injection mitigation under item 0.
    74	Baseline means main after dotfiles-T133-gh-binding-a02 merges, including its bound gh and fixed host/repository. The audit-inherit-replan-json lineage is already on main as b22a5580 (#423); #390 is superseded.
    75	Historical host facts supplied by orchestrator (Claude seat, sandboxed Bash), 2026-10-22T04:44Z, main d06d94fd: manifest-pinned hcom 0.7.30 and omp exist at their declared install targets; upstream hcom 0.7.31 is not adopted. Dispatch sends at 245/350 and reads history at 46–59/347; bus-read reads at 49; counters read_history is at 94 and revise rule at 11; replay reads no bus; hcom-dispatch is absent. Reobserve post-prerequisite.
    76	The test wildcard expands only to test_hcom_dispatch.py (new), test_orchestrator_tools.py and test_regime_counters.py; the three executable modules have separate threat rows. The evidence wildcard is non-executable. Manifest authority is limited to the store declaration in constraint 2; preserve profiles, tools, pins and unrelated fields.
    77	
    78	## Items
    79	
    80	0. Before code, paste actual hcom version and top-level/send/list/events-or-history help, sender-selection/tag-scope facts, default directory, SQLite basename/schema, id/time/from/to/body/receipt columns and PRAGMA user_version into report.md. Verify the one-send form, returned stable message ID and deadline/receipt behavior; no guessed flags/schema. Choose a read command only if it reads the entire tag with every needed field/receipt without writes; otherwise use schema-guarded sqlite3 -readonly. Missing facts/tool/unique send identity means blocked PONG. test_migration_item_matrix includes a behavioral item-0 subfixture grounded in these observations.
    81	1. Add bus-history.sh <team> [--limit <n>]: chronological marker rows "<marker> [<at>] <from> → <to>: <body>", marker ● unread or ○ read from hcom receipts, at UTC ISO-8601. The old TSV output is withdrawn; an internal --json view retains actual message IDs and fields, with --message-id <id> selecting exactly one row in that view (missing/duplicate ID refuses). Validate IDs against item 0's grammar and bind query values, never interpolate SQL. Apply constraint 6 before emitting any output; unreadable/foreign store or unknown schema exits 1 with one stderr line, never initializes/writes/marks read. test_hcom_history_matrix covers populated/empty/bounded histories, both markers, schema refusal and unchanged store bytes.
    82	2. Add hcom-dispatch <team> <from> <to> <pane> <words…>, preserving agmsg-dispatch's argument form/space joining and deadline. Validate its existing strict identity grammar without sourcing agmsg; body is one argument after --, one send only. Capture that send's stable hcom ID and confirm only its receipt through the reader's exact-ID view; emit one machine receipt {id, read_at} for dispatch's recorder. Missing/ambiguous ID never falls back to sender/body matching or resends. Unconfirmed sends nudge once through bound herdr pane run "<pane>" "hcom: new message for <to>" and return the existing nonzero unconfirmed status. test_transport_matrix covers argv, leading dash, tabs/quotes, confirmation/no nudge and timeout/one nudge; test_identity_and_payload_matrix covers hostile inputs. Both new scripts have English shdoc headers/args/exitcodes.
    83	3. Replace both dispatch send sites and history windows with hcom-dispatch and bus-history. BUS_HISTORY is a repository-relative constant resolved against the checkout, never an environment override; remove AGMSG_SCRIPTS selection. Keep existing refusals, bounded windows and byte-identical outgoing line. Supersede only the old last-matching-row identity heuristic: record read/unread from the exact returned message ID; verify receipt shape and matching team/from/to/body through the reader's exact-ID view before recording; preserve the sender's nonzero timeout status after recording an unread receipt. test_hcom_dispatch_matrix and test_hcom_marker_roundtrip cover the actual subprocess route; test_concurrent_identical_send_receipts interleaves identical messages, reads only the other ID and proves this dispatch stays unread.
    84	4. For AGMSG-ACCEPTANCE v1 status=revise require previous_head= exactly once (40 lowercase hex), check= exactly once (nonempty), task_sha256= and a record argument. Before send run bound regime-counters.sh <task_id> --team <team> --history-only; failure refuses with stderr. Append stdout to the record JSON counters list as "<task_id> <ISO time> <lines joined by '; '>", preserving sort_keys/indent=2 and creating the list when absent. Named subfixtures cover every missing/duplicate/malformed field, absent record, failed counter and successful append. Other acceptance statuses skip only these revise-specific checks; verdict= never selects them.
    85	5. Switch bus-read's source to the same constant reader; preserve jq classification unchanged and rerun all five existing test_bus_read_* fixtures. test_hcom_bus_read_matrix and test_hcom_marker_roundtrip prove open-task classification and both markers from actual reader output.
    86	6. Switch counters' read_history to that reader; remove storage.sh sourcing. Use its internal --json view, retaining actual hcom IDs while adapting into the existing count input; preserve --history-file's TSV fixture contract and 20 existing seam cases, existing detail/count output and inherited audit/re-plan schema/deduplication. revises=max(RESULTs−1, this task's ACCEPTANCE status=revise count, 0); update the header only in meaning. Fixtures: 2 RESULTs/3 revises → 3 and 4 RESULTs/1 revise → 3; unrelated tasks/tabs and verdict-only revise do not inflate counts.
    87	7. Leave replay.sh (no bus read), agent-stop-gate.sh (stage-2 hook), SKILL/rules (PR E), agmsg-dispatch and .chezmoiremove (PR E) untouched; report each reason. test_migration_item_matrix names one behavioral subfixture per item 0–7, including operation with the agmsg store absent and item-7 migration/scope checks.
    88	
    89	## Binding constraints
    90	
    91	1. Resolve every executable/child under design 5.14 items 2/3/9, including hcom/sqlite3/jq/herdr/uv/Python and utilities; declared absolute tools/private namespace or realpath-bound checkout siblings only. Refuse inherited executable selection, mise shims and PATH lookup. Every env -i contract carries absolute private UV_CACHE_DIR; missing/relative cache refuses. test_private_namespace_matrix attacks all routes with PATH decoys, BUS_HISTORY/AGMSG_SCRIPTS overrides and startup payloads; test_private_cache_matrix covers cache refusals and hostile .venv/uv.toml/user-site inputs.
    92	2. Authorize assets.hcom.store_relative_path: .hcom in home/dot_agents/agent-config.yaml, verified as item 0's default or block for reauthoring. Production reads the protected deployed .agents/agent-config.yaml under passwd home, never a worker checkout/fixture declaration or inherited HOME/HCOM_DIR. Require a normalized home-relative directory, no traversal/absolute override, and the measured SQLite basename within it; both directory and database realpaths must remain in that declared location. Refuse nonempty inherited HCOM_DIR, unknown schema and absent/malformed declaration; never set HCOM_DIR or initialize a store. test_production_store_declaration consumes the actual source declaration and covers its deployed read/missing/malformed/escape cases; test_hostile_hcom_store_refused supplies a schema-compatible fabricated store via HCOM_DIR and proves refusal/no rows/both stores unchanged.
    93	3. Every task-copy/record consumer applies design 5.14 item 4 to bytes it actually reads: verify against TASK/ACCEPTANCE digests, then parse/use that same buffer, protected snapshot or held FD; missing/mismatch refuses. Pass checked content and explicit expected digest to checker/recorder/counter children without editing an out-of-scope consumer; inability to preserve binding blocks/replans. test_consumed_bytes_matrix replaces/restores a task copy after an earlier hash and proves consumer refusal, not acceptance-time detection alone.
    94	4. A record requires matching record_file= and record_sha256= on the bound line. Dispatch's record argument and counters' record path open once under canonical <checkout>/.orchestration/acceptance/, with no symlinked parent or escaping case alias; preserve opened identity through validation/read/write. Compare inode before/after validation and immediately before the locked atomic update; never reopen an unchecked pathname. Verify each consumed record buffer against its input digest before mutation; subsequent controlled writes produce the next explicit digest/identity. test_consumed_bytes_matrix covers symlinked parent, swapped inode, wrong digest and safe update; test_hcom_counter_matrix independently covers record consumption.
    95	5. Add no gh calls to the five scripts; existing counters PR reads adopt T133's bound gh, fixed github.com host and mryfmo/dotfiles repository (design 5.14 items 2/8/9). The named merge/update operations use the same binding. Dispatcher argv-stub tests establish only invocation shape; claim no executable/credential/Linux escape/authenticated-network boundary from them. Unmet prerequisite/deployment evidence blocks operational use.
    96	6. Before rendering any marker row, validate header fields and reject NUL and every body line separator recognized by downstream splitlines, including CR/LF, VT/FF, FS/GS/RS, NEL and Unicode line/paragraph separators; preserve ordinary tabs/quotes. Buffer validation so failure emits no partial history; readers refuse the failed read. test_history_forged_row_refused plants one hcom message containing a forged marker/ACCEPTANCE row, exercises bus-history plus all three consumers, and asserts refusal, no fabricated event/count, no send and no record mutation. test_hcom_marker_roundtrip proves valid marker compatibility; only ID selection in item 3 supersedes the old sent-row algorithm.
    97	7. test_status_revise_matrix and dispatch subfixtures use AGMSG-ACCEPTANCE v1 status=revise previous_head=… check=… task_sha256=…; preserve amendment digest validation. Receipt-identity fixtures cover send/query IDs missing/malformed/ambiguous and injection attempts, duplicate payloads with opposite receipts and a valid exact-ID match; store-declaration/framing fixtures separately close all three round-1 findings.
    98	
    99	## Deferred — stage 2 and PR E
   100	
   101	Stage 2 seats hcom omp --tag <team> --dir <worktree> instead of spawn.sh, with MODEL_PROFILE_<NAME>_OMP_MODEL and a verified omp model flag; writes <run-dir>/<seat>.launch.json {argv,pid,started_at}; --attach shows live arguments; check-regime-boundary.sh seat_pane_state/check-agent-runtime.py compare live process/record; dispatch refuses mismatched live seats (C-60:1); worker hcom hook requires re-plan: on S1 revise; remove-worker/--stale use hcom's member list. Report item-0 changes to member command/hook surface.
   102	Sources remain PR #383's branch-only seat-args.sh and seat-liveness/seat-launch-args owner records; VERIFY intended owned rows with the plan author. Serialize stage-2 seating with integration-seat-result-gate-cap-a01 and runtime checks with pstack-asset-a01. Orchestrator assigns a distinct stage-2 owner, never this reset's a02 ID. PR E owns SKILL/rules migration and agmsg-dispatch/Stop-hook/.chezmoiremove removal; the sole manifest exception here is constraint 2.
   103	
   104	## Validation and caps
   105	
   106	Fixtures first: one red-at-origin/main behavioral assertion and green-at-fix pair per constraint, round-1 remedy and item 0–7, with individually named matrix subtests. For absent new files, exercise the corresponding existing production route at baseline; missing command/import/setup failure is not red evidence. Record full baseline/red-fixture/fix SHAs, selectors, exact commands, stdout/stderr and real statuses; facts/scope checks accompany item-0/7 behavioral assertions.
   107	Reuse tests/unit/trusted_exec_contract.py unchanged: test_contract_attack_matrix covers shim nonexecution, hostile GIT_*/repository configuration, worker-root refusal and post-validation replacement; test_trusted_path_matrix covers realpath/parent/case handling. Use isolated fixture roots populated from production declarations, never environment override seams or live stores/sockets/panes/PRs; test_fixture_route_isolation proves isolation.
   108	Run uv run python -m unittest tests.unit.test_hcom_dispatch tests.unit.test_orchestrator_tools tests.unit.test_regime_counters -v through measured absolute uv/Python and design 5.14 item 9 isolation; paste the expanded invocation. Run make unit-test once on final head, bash -n/shellcheck on all five changed scripts, make format and make render-check; verify scope/status. Never run Bats locally.
   109	Resolve validation uv with /usr/bin/env -i PATH=/usr/bin:/bin HOME="<passwd-home>" UV_CACHE_DIR="<absolute-private-cache>" "<passwd-home>/.local/bin/mise" which uv; repeat for python and paste outputs. Host notes report Python 3.15.0 and uv's version/target directory without bin; never guess paths or treat discovery as runtime provenance.
   110	The final diff has at most 900 changed lines outside tests/ and .orchestration/, and at most 2200 under tests/.
   111	Measure with git diff --numstat <merge-base40> <head40>.
   112	Caps count PR-wide additions plus deletions from merge-base with authenticated main, never round deltas; expected 650/1500 leaves 250/700 headroom. Paste dispatch measurement_base40 (current branch head for a records-only round after update-branch), final authenticated main/head/merge-base40, every numstat row/totals; recount after update-branch. Do not silently raise caps.
   113	Explain every agmsg hit in the five scripts: only historical argument-form/PR-E documentation may remain, never store reads/sourcing. Unverified flags/schema, direct store writes, receipt mutation by history reads, test live sends, resend retries, workflow/permission changes and edits outside allowed_files are forbidden.
   114	
   115	## Execution, evidence and completion
   116	
   117	Worker Playbook step 4 applies: denial means blocked PONG with exact command/exit/boundary and hold, no escalation or alternate-surface retry. Claude a009 sends PONG/RESULT through existing agmsg-dispatch on macOS when already socket-allowlisted, or send.sh --body-file on its named route; this task changes no permission or its own reporting bus before merge.
   118	Continue tools/hcom-dispatch-bus-a01/draft PR #407, updated to post-prerequisite origin/main, carrying its two item-0 files' evidence into authorized a02 artifacts; or use a fresh branch/PR and close #407 with closure in RESULT. The entire PR diff must fit allowed_files; if old artifact paths prevent that within scope, use the fresh-branch route. Textual conflicts are blocked PONG for orchestrator integration, never worker hand merge. Push without shared Git-config changes.
   119	A replacement draft uses explicit --base main/--head/--title/--body-file/--draft and English text. Follow Worker Playbook step 15's ready/CI/Bot wait and one worker fix round; worker never merges. Apply normalised-comparison-lint-a01's Completion clause with advisory owner dotfiles-T129-hcom-dispatch-bus-a02-followup-a01, preserving INV-6 and surviving-P0/P1 stops.
   120	Under the allowed evidence directory write byte-identical task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and result.txt. Every item names producer/seat: worker (Claude seat a009), orchestrator (Claude seat, sandboxed Bash), or author (Codex review-profile seat). Paste verbatim outputs/statuses, selector/finding mappings, schema/send-ID/receipt/declaration facts, agmsg-hit table, denials and limits; learning/AutoSkill record actual triage/use; cost is observed or n/a. Keep plan/todo/learn uncommitted, one active todo per owner.
   121	RESULT names PR/#407 disposition, branch, full head/main/merge-base/measurement_base40, files, source_cap=900/test_cap=2200 and measured totals, every red/green pair, task_copy=<sha256 of .orchestration/dotfiles-T129-hcom-dispatch-bus-a02/task.md>, artifact paths, Bot findings/dispositions and deferred-stage facts. Pass agent-side review evidence and make require-crit-review before RESULT; no browser Crit/publication. Orchestrator alone follows Playbook step 10's final-head sweep/audit/acceptance/gate/merge order.
   122	Before review/anchor, orchestrator creates dotfiles-T129-hcom-dispatch-bus-a02-followup-a01's owner stub, confirms T133 merged, checks post-prerequisite inventory and measures design 5.14 items 1/2/9 deployment prerequisites. Store declaration deployment is verified after the code merges and before operational migration; absent declaration always refuses.
   123	Replace the pending Checks payload with .agents/worklog/orchestrator-glue/checks-paste.sh's hcom selector dotfiles-T129-hcom-dispatch-bus-a01, which selects probes only. Require exact masked commands/outputs/real statuses, canonical-main/design identity, executable provenance and absolute private UV_CACHE_DIR in every env -i contract; incomplete evidence blocks anchor/dispatch. Inventory differences require reauthoring.
   124	C-80 reviews the complete populated text, then anchor/dispatch those exact bytes with no later paste. Reserve up to 34 Checks payload lines within 180 total lines; amendments carry status=revise and new task_sha256 and repeat consumer verification.
   125	
   126	Amendment 1 (orchestrator, pre-anchor; `previous_sha256` above): design 5.14 item 9 excludes executables read from the shared uv directories, and this host's `~/.local/bin/hcom` resolves into `~/.local/share/uv/tools/hcom/bin/hcom` (PR A installed it with `uv tool install --force <verified wheel>`, receipt `update_hcom` in `~/.agents/.installed-manifest.json`, wheel `~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`). Constraint 1 therefore binds hcom by that absolute uv-tools path and, before every invocation, compares the sha256 of the resolved entry and of the wheel the receipt names with the values the Checks block records, refusing on mismatch (`refused: hcom binding`); no PATH or `~/.local/bin` lookup; one fixture plants a different file at the resolved path and asserts the refusal. The Checks block below is generated by `checks-paste.sh` (every line a command with its output and exit status, the design digest in two stages through a private file, the executable digests and item 1 observations shared with every task).
   127	
   128	Amendment 2 (orchestrator, pre-anchor; `previous_sha256` above; supersedes amendment 1's execution path): design 5.14 item 9 forbids executing from the shared uv directories, and a hash taken before an invocation from such a directory does not close replacement between the check and the run. The bus scripts therefore execute hcom only from the anchored checkout's private tool directory, `<checkout>/.agents/worklog/uv-tools/hcom/bin/hcom` (gitignored, under the main checkout, outside the Bash sandbox write roots of both seat kinds as rendered on canonical main, the Codex `writable_roots` and the Claude `allowWrite` lists recorded in the Checks; a Claude seat's unsandboxed file tools and every same-UID process remain design 5.14 item 0's residual, owned by dotfiles-T129-hcom-dispatch-bus-a02-followup-a01, so the run-time control is the digest check at every invocation, not the directory), installed by one new updater target `update_hcom_private` that verifies the receipt's wheel sha256 (`~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`) and runs `uv tool install --force <wheel>` with both `UV_TOOL_DIR` and `UV_TOOL_BIN_DIR` set under that directory (uv publishes the entry in `UV_TOOL_BIN_DIR`; without it the install would replace the public `~/.local/bin/hcom`), and the fixture asserts that the public entry's sha256 is unchanged by the install; the scripts refuse (`refused: hcom binding`) when the path is absent, is not a regular file, or when its sha256 differs from the value the install recorded beside it; the fixture plants a drifted wheel and a replaced entry and asserts both refusals. `~/.local/bin/hcom` and `~/.local/share/uv/tools` are never executed by these scripts. The generated Checks print every command with shell quoting (`%q`), so a recorded `sh -c` replays as run, and record the worker write boundaries as members: the rendered arrays at canonical main and the deployed settings of this host (the Claude `allowWrite`, `allowUnixSockets` and `excludedCommands` lists; the Codex `writable_roots` and `network_access`). The denial itself is measured by the worker, not pasted by the orchestrator: item 0's first command attempts to create a file under `<checkout>/.agents/worklog/uv-tools/` from inside its sandbox and records the refusal verbatim in sandbox.md; a success there is an `AGMSG-PONG v1 status=blocked`, because the protection premise would have failed.
   129	
   130	Amendment 3 (orchestrator, pre-anchor; `previous_sha256` above): the comparison-lint baseline at canonical main holds five R1 rows for `scripts/orchestrator/dispatch.sh` (lines 109, 190, 202, 209, 334; the Checks list them), and the lint exits 1 on a stale row of a changed file, so `scripts/lint-comparisons-baseline.tsv` joins allowed_files for stale-row removal only, closed by the existing lint test; new hits are fixed in the sources. The length rule reads 180 lines including the generated Checks block (34 payload lines). Nothing else changes.
   131	
   132	## Checks (pasted by the orchestrator before each send)
   133	
   134	```text
   135	observed 2026-10-22T05:39Z by the orchestrator (sandboxed Bash); every executable below is absolute and every command runs under the enumerated environment printed with it
   136	canonical main: clone (gh-free): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home /Library/Developer/CommandLineTools/usr/bin/git -c http.proxyAuthMethod=basic -c credential.http://localhost:49680.helper= clone -q --bare https://github.com/mryfmo/dotfiles.git <private>/dotfiles.git ` -> `` (exit 0)
   137	canonical main: ref: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git rev-parse refs/heads/main ` -> `d06d94fd8eedcd0770c1c80c2b1596ec36109ef8` (exit 0)
   138	canonical main: remote: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git config --get remote.origin.url ` -> `https://github.com/mryfmo/dotfiles.git` (exit 0)
   139	canonical main: config origins: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git config --list --show-origin ` -> `file:<private>/dotfiles.git/config	core.repositoryformatversion=0 file:<private>/dotfiles.git/config	core.filemode=true file:<private>/dotfiles.git/config	core.bare=true file:<private>/dotfiles.git/config	core.ignorecase=true file:<private>/dotfiles.git/config	core.precomposeunicode=true file:<private>/dotfiles.git/config	remote.origin.url=https://github.com/mryfmo/dotfiles.git` (exit 0)
   140	design file (canonical main): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c exec\ /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:.orchestration/plans/024-design-quality.md\ \>\ <private>/design.md ` -> `` (exit 0)
   141	design digest: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 <private>/design.md ` -> `a027b0210981ca4c4d4e832dc849af6a03cd71c408801f74d098c3b778dd9dbe  <private>/design.md` (exit 0)
   142	hcom version: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 ~/.local/bin/hcom --version ` -> `→ hcom v0.7.31 available — run `hcom update` hcom 0.7.30` (exit 0)
   143	hcom realpath: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/readlink -f ~/.local/bin/hcom ` -> `~/.local/share/uv/tools/hcom/bin/hcom` (exit 0)
   144	hcom entry digest: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 ~/.local/share/uv/tools/hcom/bin/hcom ` -> `7cd012d9a4d369de313ca4935cccda1ada6c8ffcd5e42ffa7eaeecdff7fc580e  ~/.local/share/uv/tools/hcom/bin/hcom` (exit 0)
   145	hcom install receipt (PR A): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n -E -B2 -A8 hcom ~/.agents/.installed-manifest.json ` -> `224-      "source_version": "18.11.3" 225-    }, 226:    "update_hcom": { 227-      "installed_at": "2026-10-20T05:02:45Z", 228-      "kind": "installer", 229-      "paths": [ 230:        "~/.local/bin/hcom", 231:        "~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl" 232-      ], 233-      "commands": [ 234:        "uv tool install --force <verified-hcom-wheel>" 235-      ], 236-      "source_version": "0.7.30" 237-    } 238-  } 239-}` (exit 0)
   146	hcom verified wheel digest (PR A): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 ~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl ` -> `764b6469ce4fe470094d2fb821285ea5e7e002726c68c634752663abe2410ea4  ~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl` (exit 0)
   147	omp path: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -la ~/.local/bin/omp ` -> `lrwxr-xr-x@ 1 <user>  staff  57 Oct 18 08:01 ~/.local/bin/omp -> ../lib/node_modules/@oh-my-pi/pi-coding-agent/dist/cli.js` (exit 0)
   148	premise 1: agmsg-dispatch in dispatch.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c agmsg-dispatch ~/Workspace/dotfiles/scripts/orchestrator/dispatch.sh ` -> `4` (exit 0)
   149	premise 2a: history.sh in bus-read.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c history.sh ~/Workspace/dotfiles/scripts/orchestrator/bus-read.sh ` -> `2` (exit 0)
   150	premise 2b: storage.sh in regime-counters.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c storage.sh ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `1` (exit 0)
   151	premise 3: bus reads in replay.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c -e history.sh -e storage.sh -e sqlite3 ~/Workspace/dotfiles/scripts/orchestrator/replay.sh ` -> `0` (exit 1)
   152	premise 4: hcom-dispatch absent: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls ~/Workspace/dotfiles/home/dot_local/bin/common/executable_hcom-dispatch ` -> `ls: ~/Workspace/dotfiles/home/dot_local/bin/common/executable_hcom-dispatch: No such file or directory` (exit 1)
   153	premise 5: revises rule: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n revises\ =\ AGMSG-RESULTs\ -\ 1 ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `11:#   1; revises = AGMSG-RESULTs - 1, whatever their status; questions = PONGs of` (exit 0)
   154	anchor: dispatch.sh call sites: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n agmsg-dispatch\ \"\$\{team\}\" ~/Workspace/dotfiles/scripts/orchestrator/dispatch.sh ` -> `245:[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" 350:agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?` (exit 0)
   155	anchor: bus-read.sh history read: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n history.sh ~/Workspace/dotfiles/scripts/orchestrator/bus-read.sh ` -> `5:#   Plan 007 T718 (C-23). Reads the history through agmsg's `history.sh <team> 49:history="$("${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}")" || {` (exit 0)
   156	anchor: regime-counters.sh read_history: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n read_history\(\) ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `94:read_history() {` (exit 0)
   157	after: audit-inherit-replan-json lineage on main: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /Library/Developer/CommandLineTools/usr/bin/git -C ~/Workspace/dotfiles log -1 --format=%h%x20%s b22a5580 ` -> `b22a5580 fix(orchestrator): the F1 lineage's owned rows: the gate's re-plan schema in the counters, no inherited unusable audit, one count per audit id (T129 audit-inherit replan-json followup a02) (#423)` (exit 0)
   158	executable digests: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 /Library/Developer/CommandLineTools/usr/bin/git /usr/bin/shasum /usr/bin/env /bin/ls /usr/bin/sed /usr/bin/readlink /usr/bin/grep /usr/bin/cut /usr/bin/tr /bin/date ~/.local/bin/mise ~/.local/share/mise/installs/github-cli-cli/latest/bin/gh ` -> `a73bf622a2e470d5d57a4b1d5aef1e8680e67278018d4858a2f93825b7d595c7  /Library/Developer/CommandLineTools/usr/bin/git 0812595f981a26f813d98dc380af14d4af427626c9339eda29eb849ae13de1e3  /usr/bin/shasum 2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0  /usr/bin/env 13f44bfe1c4af602da4465c834dbe7b16a5441ccbd843178b36116ee23422bfb  /bin/ls bb1cb46089269d91ba83ef291364e6e7121e7b27f12037629fe8daaf5238a559  /usr/bin/sed 2dc55748b64cf63d2452300bcf2cd3fc337425e76c76f8c484212026840d5a3c  /usr/bin/readlink afc3903988afaa5be7a19d595e66a95ead29cbb5102ff4dd2e4522089871f64a  /usr/bin/grep 71d96107b74d43fa54e2e2dbdb0148bf209f38a7ab29f6962bf9cd9df7c3c0a0  /usr/bin/cut 188d384d918a49fab8263deaa423e33068c99e9a4a5cb23fb971d2ed5b6e4d16  /usr/bin/tr 931edbfcbd847f3c1ccb504325a502db313ce20db27634744a7416c3c4b812f0  /bin/date 005b32b9c22ca9cb63ff9d35c74b3abe69c433e9ca655fea288ba3dcbe7e4918  ~/.local/bin/mise 8a4258433c81106343144857750316241759d06dcf16265cf3c4864a8f2f2ad6  ~/.local/share/mise/installs/github-cli-cli/latest/bin/gh` (exit 0)
   159	git version: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /Library/Developer/CommandLineTools/usr/bin/git --version ` -> `git version 2.54.0 (Apple Git-157)` (exit 0)
   160	git code signature: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/codesign -dv /Library/Developer/CommandLineTools/usr/bin/git ` -> `Executable=/Library/Developer/CommandLineTools/usr/bin/git Identifier=com.apple.git Format=Mach-O thin (arm64) CodeDirectory v=20400 size=29809 flags=0x2000(library-validation) hashes=926+2 location=embedded Signature size=4442 Signed Time=Sep 2, 2026 at 12:44:16 Info.plist entries=2 TeamIdentifier=59GAB85EFG Sealed Resources=none Internal requirements count=1 size=64` (exit 0)
   161	worker write roots (codex, rendered at canonical main, members): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:home/.chezmoitemplates/codex-config-managed.toml\ \|\ /usr/bin/sed\ -n\ \'/writable_roots/\,/\]/p\;/network_access/p\' ` -> `network_access = false writable_roots = ["{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db", "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams", "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run", "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools"]  [shell_environment_policy]` (exit 0)
   162	worker write roots (claude, rendered at canonical main, members): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:home/.chezmoitemplates/claude-settings-managed.json\ \|\ /usr/bin/sed\ -n\ \'/allowWrite/\,/\]/p\;/allowUnixSockets/\,/\]/p\;/excludedCommands/p\' ` -> `  "excludedCommands": [],     "allowWrite": [       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools",       "~/.cache/uv",       "~/.local/state/mise",       "~/.local/share/uv",       "~/Library/Caches/mise"     ]     "allowUnixSockets": [       "~/.config/herdr/herdr.sock"     ]   "excludedCommands": [],     "allowWrite": [       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools",       "~/.cache/uv",       "~/.local/state/mise",       "~/.local/share/uv"     ]     "allowUnixSockets": [       "~/.config/herdr/herdr.sock"     ]` (exit 0)
   163	effective claude sandbox on this host (deployed settings): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/sh -c /usr/bin/sed\ -n\ \'/allowWrite/\,/\]/p\;/allowUnixSockets/\,/\]/p\;/excludedCommands/p\'\ ~/.claude/settings.json ` -> `    "excludedCommands": [],       "allowWrite": [         "~/.agents/skills/agmsg/db",         "~/.agents/skills/agmsg/teams",         "~/.agents/skills/agmsg/run",         "~/.agents/skills/agmsg/ext-tools",         "~/.cache/uv",         "~/.local/state/mise",         "~/.local/share/uv",         "~/Library/Caches/mise"       ]       "allowUnixSockets": [         "~/.config/herdr/herdr.sock"       ]` (exit 0)
   164	effective codex sandbox on this host (deployed config and the launch-time roots herdr-agents adds): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/sh -c /usr/bin/sed\ -n\ \'/writable_roots/\,/\]/p\;/network_access/p\'\ ~/.codex/config.toml\;\ /usr/bin/grep\ -n\ writable_roots\ ~/Workspace/dotfiles/home/dot_local/bin/common/executable_herdr-agents ` -> `network_access = false writable_roots = ["~/.agents/skills/agmsg/db", "~/.agents/skills/agmsg/teams", "~/.agents/skills/agmsg/run", "~/.agents/skills/agmsg/ext-tools"]  [shell_environment_policy] 403:#   when the file exists but cannot be parsed, or its writable_roots is not a 408:# @stdout `sandbox_workspace_write.writable_roots=[...]`, or nothing. 409:function codex_worktree_writable_roots() { 427:    roots = tomllib.load(handle).get("sandbox_workspace_write", {}).get("writable_roots", []) 433:        printf 'herdr-agents: cannot read sandbox_workspace_write.writable_roots in %s as a list of strings (python3 3.11+ tomllib); the codex worker in %s gets no git metadata roots.\n' "${config}" "${worktree}" >&2 438:        if all(.[]; type == "string" and (contains("#") | not)) then "sandbox_workspace_write.writable_roots=" + tojson else error("unsupported") end' \ 454:#   codex_worktree_writable_roots) for a codex worker when a worktree is given. 489:        roots="$(codex_worktree_writable_roots "$2")"` (exit 0)
   165	private tool dir of the anchored checkout: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -ld ~/Workspace/dotfiles/.agents/worklog/uv-tools ~/Workspace/dotfiles/.agents/worklog ` -> `ls: ~/Workspace/dotfiles/.agents/worklog/uv-tools: No such file or directory drwxr-xr-x@ 7 <user>  staff  224 Oct 22 12:02 ~/Workspace/dotfiles/.agents/worklog` (exit 1)
   166	lint baseline rows naming the task's scripts (canonical main): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:scripts/lint-comparisons-baseline.tsv\ \|\ /usr/bin/grep\ -E\ \'\(executable_hcom-dispatch\|bus-history.sh\|dispatch.sh\|bus-read.sh\|regime-counters.sh\|update-agent-assets.sh\|agent-config.yaml\)\'\ \|\|\ true ` -> `scripts/orchestrator/dispatch.sh	R1	0aa21332a34f2b0fcc6d3e611138e68be68a5c96888545888202ad9d891eed4f scripts/orchestrator/dispatch.sh	R1	4dc66da0312fcc5ec625b21280b5780d6a5d991a13195a0cae35de72535665d6 scripts/orchestrator/dispatch.sh	R1	7da677eb3c35e65932431b5c74e602850bfee03f910d10100529d9bfcda4c370 scripts/orchestrator/dispatch.sh	R1	e36790337b32324fb95aca31583a592972e4628860426a8fe9a078f31557eac3 scripts/orchestrator/dispatch.sh	R1	f210c0c83e72ff3ea95a71f3075be49726b76ee318ad9c6c618de4b0d98be7e1` (exit 0)
   167	item 1 manifest: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -la ~/.agents/agent-config.yaml ` -> `-rw-r--r--@ 1 <user>  staff  32378 Oct 22 08:08 ~/.agents/agent-config.yaml` (exit 0)
   168	item 1 directory: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -ld ~/.agents ` -> `drwxr-xr-x  11 <user>  staff  352 Oct 22 08:20 ~/.agents` (exit 0)
   169	```

**Reducing output size**
exec
/bin/zsh -lc "sed -n '1,115p' .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
---
format: 2
task_id: dotfiles-T129-hcom-dispatch-bus-a02
kind: code
security: true
previous_sha256: 4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c
reset_of: [dotfiles-T129-hcom-dispatch-bus-a01]
dispatch_status: blocked-pre-anchor
design_review: {design: .orchestration/plans/024-design-quality.md}
after: [dotfiles-T133-gh-binding-a02]
allowed_files:
  - home/dot_local/bin/common/executable_hcom-dispatch
  - scripts/orchestrator/bus-history.sh
  - scripts/orchestrator/dispatch.sh
  - scripts/orchestrator/bus-read.sh
  - scripts/regime-counters.sh
  - tests/unit/test_*.py
  - scripts/update-agent-assets.sh
  - scripts/lint-comparisons-baseline.tsv
  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a02/**
  - home/dot_agents/agent-config.yaml
threat_table:
  - {control: "home/dot_local/bin/common/executable_hcom-dispatch", disposition: "closed: tests/unit/test_hcom_dispatch.py::HcomDispatchTest::test_transport_matrix"}
  - {control: "scripts/orchestrator/bus-history.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_history_matrix"}
  - {control: "scripts/orchestrator/dispatch.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_dispatch_matrix"}
  - {control: "scripts/orchestrator/bus-read.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_bus_read_matrix"}
  - {control: "scripts/regime-counters.sh", disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_hcom_counter_matrix"}
  - {control: "tests/unit/test_*.py (test_hcom_dispatch.py)", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; independent audit checks send argv and receipt assertions."}
  - {control: "scripts/update-agent-assets.sh (amendment 2: one new target, update_hcom_private, installs the verified hcom wheel the receipt names into the anchored checkout's private tool directory with UV_TOOL_DIR and UV_TOOL_BIN_DIR under <checkout>/.agents/worklog/uv-tools; nothing else in the updater changes)", disposition: "closed: tests/unit/test_hcom_dispatch.py::test_update_hcom_private_installs_the_verified_wheel_into_the_private_tool_dir_leaves_the_public_entry_unchanged_and_refuses_a_drifted_wheel"}
  - {control: "scripts/lint-comparisons-baseline.tsv (amendment 3: stale-row removal only; the five R1 rows of scripts/orchestrator/dispatch.sh at lines 109, 190, 202, 209 and 334 fall away with the lines the constraints rewrite; no row is added, every new hit is fixed in the allowed sources)", disposition: "closed: tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline (the existing lint test, run by make unit-test on the final head)"}
  - {control: "tests/unit/test_orchestrator_tools.py", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; audit checks real reader/dispatcher assertions and red/green logs."}
  - {control: "tests/unit/test_regime_counters.py", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; audit checks counts and preserved seam cases."}
  - {control: ".orchestration/dotfiles-T129-hcom-dispatch-bus-a02/** including task.md", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence automation; independently compare anchored bytes, full heads and verbatim validation."}
  - {control: "home/dot_agents/agent-config.yaml", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_production_store_declaration"}
  - {control: "private namespace", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_namespace_matrix"}
  - {control: "store identity", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hostile_hcom_store_refused"}
  - {control: "consumed-bytes binding", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_consumed_bytes_matrix"}
  - {control: "history format", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_marker_roundtrip"}
  - {control: "history framing", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_history_forged_row_refused"}
  - {control: "receipt identity", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_concurrent_identical_send_receipts"}
  - {control: "status key", disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_status_revise_matrix"}
  - {control: "bound gh calls", disposition: "residual: dotfiles-T133-gh-binding-a02 owns executable/configuration/host binding; dispatcher argv stubs establish only invocation shape, never that boundary."}
  - {control: "task metadata including dotfiles-T129-hcom-dispatch-bus-a01/task.md and dotfiles-T129-hcom-dispatch-bus-a02/task.md", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns metadata automation; check complete reset bytes and format-2 consistency, never reuse a01 approval."}
  - {control: "metadata separators", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence automation; bind the whole text including front matter, separators and Checks."}
  - {control: "bus rows and routing identities", disposition: "closed: tests/unit/test_hcom_dispatch.py::HcomDispatchTest::test_identity_and_payload_matrix"}
  - {control: "in-process effects", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_fixture_route_isolation"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployment evidence; require measured design 5.14 items 1/2/9 before operational use."}
  - {control: "new or renamed scripts", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_migration_item_matrix"}
  - {control: "design 5.14 item 0", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns unchanged item 0 obligations; this task establishes no same-UID or credential-separation boundary."}
  - {control: "design 5.14 item 1", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns protection measurements for the deployed manifest, tools, namespace, snapshots and evidence."}
  - {control: "design 5.14 item 2", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_namespace_matrix"}
  - {control: "design 5.14 item 3", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_trusted_path_matrix"}
  - {control: "design 5.14 item 4", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_consumed_bytes_matrix"}
  - {control: "design 5.14 item 5", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns unchanged lock/reservation obligations; retain full head identities and existing locking."}
  - {control: "design 5.14 item 6", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployment verification; distinguish assertions, CI and observed host execution."}
  - {control: "design 5.14 item 7", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_contract_attack_matrix"}
  - {control: "design 5.14 item 8", disposition: "residual: dotfiles-T133-gh-binding-a02 owns bound gh authority; add no approval reader and certify no local-object boundary."}
  - {control: "design 5.14 item 9", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_cache_matrix"}
  - {control: "design 5.14 item 10", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns denial records; apply Worker Playbook step 4 without escalation."}
  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns integration records; only the orchestrator integrates the audited full head through Playbook step 10."}
  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence refresh; repeat CI, sweep, audit, acceptance and gate after any head change."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns teardown records; none is planned and dirty state cannot be discarded implicitly."}
  - {control: "orchestrator effect owner-stub creation", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns all assigned residuals; create its task stub before anchor, outside worker scope."}
  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns Checks provenance; populate post-prerequisite observations before review/anchor."}
  - {control: "orchestrator effect PR 407 closure", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns continuity records; record closure of 407 in RESULT if replaced."}
  - {control: "orchestrator effect deployment", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployed store declaration and real-host verification; fixtures never enable an unmeasured route."}
premises: []
---

# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a02 — plan 023 PR C, stage 1

Reset a01 (2026-10-18); retain items 0–7 and deferred work, with binding remedies for C-80 24d8b8d (2026-10-22T04:44Z: five P1/two P2) and a02 round 1 (framing, receipt identity, undeclared production store). Plan 024 phase 2 starts here (D-024-79/D-024-81). Worker: Claude seat a009 (worker-c).
Design 5.14 items 0–10 in .orchestration/plans/024-design-quality.md apply by reference. Closed rows cover their named assertions; broader host/environment/executable risks remain with the residual owners. This is accident/prompt-injection mitigation under item 0.
Baseline means main after dotfiles-T133-gh-binding-a02 merges, including its bound gh and fixed host/repository. The audit-inherit-replan-json lineage is already on main as b22a5580 (#423); #390 is superseded.
Historical host facts supplied by orchestrator (Claude seat, sandboxed Bash), 2026-10-22T04:44Z, main d06d94fd: manifest-pinned hcom 0.7.30 and omp exist at their declared install targets; upstream hcom 0.7.31 is not adopted. Dispatch sends at 245/350 and reads history at 46–59/347; bus-read reads at 49; counters read_history is at 94 and revise rule at 11; replay reads no bus; hcom-dispatch is absent. Reobserve post-prerequisite.
The test wildcard expands only to test_hcom_dispatch.py (new), test_orchestrator_tools.py and test_regime_counters.py; the three executable modules have separate threat rows. The evidence wildcard is non-executable. Manifest authority is limited to the store declaration in constraint 2; preserve profiles, tools, pins and unrelated fields.

## Items

0. Before code, paste actual hcom version and top-level/send/list/events-or-history help, sender-selection/tag-scope facts, default directory, SQLite basename/schema, id/time/from/to/body/receipt columns and PRAGMA user_version into report.md. Verify the one-send form, returned stable message ID and deadline/receipt behavior; no guessed flags/schema. Choose a read command only if it reads the entire tag with every needed field/receipt without writes; otherwise use schema-guarded sqlite3 -readonly. Missing facts/tool/unique send identity means blocked PONG. test_migration_item_matrix includes a behavioral item-0 subfixture grounded in these observations.
1. Add bus-history.sh <team> [--limit <n>]: chronological marker rows "<marker> [<at>] <from> → <to>: <body>", marker ● unread or ○ read from hcom receipts, at UTC ISO-8601. The old TSV output is withdrawn; an internal --json view retains actual message IDs and fields, with --message-id <id> selecting exactly one row in that view (missing/duplicate ID refuses). Validate IDs against item 0's grammar and bind query values, never interpolate SQL. Apply constraint 6 before emitting any output; unreadable/foreign store or unknown schema exits 1 with one stderr line, never initializes/writes/marks read. test_hcom_history_matrix covers populated/empty/bounded histories, both markers, schema refusal and unchanged store bytes.
2. Add hcom-dispatch <team> <from> <to> <pane> <words…>, preserving agmsg-dispatch's argument form/space joining and deadline. Validate its existing strict identity grammar without sourcing agmsg; body is one argument after --, one send only. Capture that send's stable hcom ID and confirm only its receipt through the reader's exact-ID view; emit one machine receipt {id, read_at} for dispatch's recorder. Missing/ambiguous ID never falls back to sender/body matching or resends. Unconfirmed sends nudge once through bound herdr pane run "<pane>" "hcom: new message for <to>" and return the existing nonzero unconfirmed status. test_transport_matrix covers argv, leading dash, tabs/quotes, confirmation/no nudge and timeout/one nudge; test_identity_and_payload_matrix covers hostile inputs. Both new scripts have English shdoc headers/args/exitcodes.
3. Replace both dispatch send sites and history windows with hcom-dispatch and bus-history. BUS_HISTORY is a repository-relative constant resolved against the checkout, never an environment override; remove AGMSG_SCRIPTS selection. Keep existing refusals, bounded windows and byte-identical outgoing line. Supersede only the old last-matching-row identity heuristic: record read/unread from the exact returned message ID; verify receipt shape and matching team/from/to/body through the reader's exact-ID view before recording; preserve the sender's nonzero timeout status after recording an unread receipt. test_hcom_dispatch_matrix and test_hcom_marker_roundtrip cover the actual subprocess route; test_concurrent_identical_send_receipts interleaves identical messages, reads only the other ID and proves this dispatch stays unread.
4. For AGMSG-ACCEPTANCE v1 status=revise require previous_head= exactly once (40 lowercase hex), check= exactly once (nonempty), task_sha256= and a record argument. Before send run bound regime-counters.sh <task_id> --team <team> --history-only; failure refuses with stderr. Append stdout to the record JSON counters list as "<task_id> <ISO time> <lines joined by '; '>", preserving sort_keys/indent=2 and creating the list when absent. Named subfixtures cover every missing/duplicate/malformed field, absent record, failed counter and successful append. Other acceptance statuses skip only these revise-specific checks; verdict= never selects them.
5. Switch bus-read's source to the same constant reader; preserve jq classification unchanged and rerun all five existing test_bus_read_* fixtures. test_hcom_bus_read_matrix and test_hcom_marker_roundtrip prove open-task classification and both markers from actual reader output.
6. Switch counters' read_history to that reader; remove storage.sh sourcing. Use its internal --json view, retaining actual hcom IDs while adapting into the existing count input; preserve --history-file's TSV fixture contract and 20 existing seam cases, existing detail/count output and inherited audit/re-plan schema/deduplication. revises=max(RESULTs−1, this task's ACCEPTANCE status=revise count, 0); update the header only in meaning. Fixtures: 2 RESULTs/3 revises → 3 and 4 RESULTs/1 revise → 3; unrelated tasks/tabs and verdict-only revise do not inflate counts.
7. Leave replay.sh (no bus read), agent-stop-gate.sh (stage-2 hook), SKILL/rules (PR E), agmsg-dispatch and .chezmoiremove (PR E) untouched; report each reason. test_migration_item_matrix names one behavioral subfixture per item 0–7, including operation with the agmsg store absent and item-7 migration/scope checks.

## Binding constraints

1. Resolve every executable/child under design 5.14 items 2/3/9, including hcom/sqlite3/jq/herdr/uv/Python and utilities; declared absolute tools/private namespace or realpath-bound checkout siblings only. Refuse inherited executable selection, mise shims and PATH lookup. Every env -i contract carries absolute private UV_CACHE_DIR; missing/relative cache refuses. test_private_namespace_matrix attacks all routes with PATH decoys, BUS_HISTORY/AGMSG_SCRIPTS overrides and startup payloads; test_private_cache_matrix covers cache refusals and hostile .venv/uv.toml/user-site inputs.
2. Authorize assets.hcom.store_relative_path: .hcom in home/dot_agents/agent-config.yaml, verified as item 0's default or block for reauthoring. Production reads the protected deployed .agents/agent-config.yaml under passwd home, never a worker checkout/fixture declaration or inherited HOME/HCOM_DIR. Require a normalized home-relative directory, no traversal/absolute override, and the measured SQLite basename within it; both directory and database realpaths must remain in that declared location. Refuse nonempty inherited HCOM_DIR, unknown schema and absent/malformed declaration; never set HCOM_DIR or initialize a store. test_production_store_declaration consumes the actual source declaration and covers its deployed read/missing/malformed/escape cases; test_hostile_hcom_store_refused supplies a schema-compatible fabricated store via HCOM_DIR and proves refusal/no rows/both stores unchanged.
3. Every task-copy/record consumer applies design 5.14 item 4 to bytes it actually reads: verify against TASK/ACCEPTANCE digests, then parse/use that same buffer, protected snapshot or held FD; missing/mismatch refuses. Pass checked content and explicit expected digest to checker/recorder/counter children without editing an out-of-scope consumer; inability to preserve binding blocks/replans. test_consumed_bytes_matrix replaces/restores a task copy after an earlier hash and proves consumer refusal, not acceptance-time detection alone.
4. A record requires matching record_file= and record_sha256= on the bound line. Dispatch's record argument and counters' record path open once under canonical <checkout>/.orchestration/acceptance/, with no symlinked parent or escaping case alias; preserve opened identity through validation/read/write. Compare inode before/after validation and immediately before the locked atomic update; never reopen an unchecked pathname. Verify each consumed record buffer against its input digest before mutation; subsequent controlled writes produce the next explicit digest/identity. test_consumed_bytes_matrix covers symlinked parent, swapped inode, wrong digest and safe update; test_hcom_counter_matrix independently covers record consumption.
5. Add no gh calls to the five scripts; existing counters PR reads adopt T133's bound gh, fixed github.com host and mryfmo/dotfiles repository (design 5.14 items 2/8/9). The named merge/update operations use the same binding. Dispatcher argv-stub tests establish only invocation shape; claim no executable/credential/Linux escape/authenticated-network boundary from them. Unmet prerequisite/deployment evidence blocks operational use.
6. Before rendering any marker row, validate header fields and reject NUL and every body line separator recognized by downstream splitlines, including CR/LF, VT/FF, FS/GS/RS, NEL and Unicode line/paragraph separators; preserve ordinary tabs/quotes. Buffer validation so failure emits no partial history; readers refuse the failed read. test_history_forged_row_refused plants one hcom message containing a forged marker/ACCEPTANCE row, exercises bus-history plus all three consumers, and asserts refusal, no fabricated event/count, no send and no record mutation. test_hcom_marker_roundtrip proves valid marker compatibility; only ID selection in item 3 supersedes the old sent-row algorithm.
7. test_status_revise_matrix and dispatch subfixtures use AGMSG-ACCEPTANCE v1 status=revise previous_head=… check=… task_sha256=…; preserve amendment digest validation. Receipt-identity fixtures cover send/query IDs missing/malformed/ambiguous and injection attempts, duplicate payloads with opposite receipts and a valid exact-ID match; store-declaration/framing fixtures separately close all three round-1 findings.

## Deferred — stage 2 and PR E

Stage 2 seats hcom omp --tag <team> --dir <worktree> instead of spawn.sh, with MODEL_PROFILE_<NAME>_OMP_MODEL and a verified omp model flag; writes <run-dir>/<seat>.launch.json {argv,pid,started_at}; --attach shows live arguments; check-regime-boundary.sh seat_pane_state/check-agent-runtime.py compare live process/record; dispatch refuses mismatched live seats (C-60:1); worker hcom hook requires re-plan: on S1 revise; remove-worker/--stale use hcom's member list. Report item-0 changes to member command/hook surface.
Sources remain PR #383's branch-only seat-args.sh and seat-liveness/seat-launch-args owner records; VERIFY intended owned rows with the plan author. Serialize stage-2 seating with integration-seat-result-gate-cap-a01 and runtime checks with pstack-asset-a01. Orchestrator assigns a distinct stage-2 owner, never this reset's a02 ID. PR E owns SKILL/rules migration and agmsg-dispatch/Stop-hook/.chezmoiremove removal; the sole manifest exception here is constraint 2.

## Validation and caps

Fixtures first: one red-at-origin/main behavioral assertion and green-at-fix pair per constraint, round-1 remedy and item 0–7, with individually named matrix subtests. For absent new files, exercise the corresponding existing production route at baseline; missing command/import/setup failure is not red evidence. Record full baseline/red-fixture/fix SHAs, selectors, exact commands, stdout/stderr and real statuses; facts/scope checks accompany item-0/7 behavioral assertions.
Reuse tests/unit/trusted_exec_contract.py unchanged: test_contract_attack_matrix covers shim nonexecution, hostile GIT_*/repository configuration, worker-root refusal and post-validation replacement; test_trusted_path_matrix covers realpath/parent/case handling. Use isolated fixture roots populated from production declarations, never environment override seams or live stores/sockets/panes/PRs; test_fixture_route_isolation proves isolation.
Run uv run python -m unittest tests.unit.test_hcom_dispatch tests.unit.test_orchestrator_tools tests.unit.test_regime_counters -v through measured absolute uv/Python and design 5.14 item 9 isolation; paste the expanded invocation. Run make unit-test once on final head, bash -n/shellcheck on all five changed scripts, make format and make render-check; verify scope/status. Never run Bats locally.
Resolve validation uv with /usr/bin/env -i PATH=/usr/bin:/bin HOME="<passwd-home>" UV_CACHE_DIR="<absolute-private-cache>" "<passwd-home>/.local/bin/mise" which uv; repeat for python and paste outputs. Host notes report Python 3.15.0 and uv's version/target directory without bin; never guess paths or treat discovery as runtime provenance.
The final diff has at most 900 changed lines outside tests/ and .orchestration/, and at most 2200 under tests/.
Measure with git diff --numstat <merge-base40> <head40>.
Caps count PR-wide additions plus deletions from merge-base with authenticated main, never round deltas; expected 650/1500 leaves 250/700 headroom. Paste dispatch measurement_base40 (current branch head for a records-only round after update-branch), final authenticated main/head/merge-base40, every numstat row/totals; recount after update-branch. Do not silently raise caps.
Explain every agmsg hit in the five scripts: only historical argument-form/PR-E documentation may remain, never store reads/sourcing. Unverified flags/schema, direct store writes, receipt mutation by history reads, test live sends, resend retries, workflow/permission changes and edits outside allowed_files are forbidden.

## Execution, evidence and completion

exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|"'^##|''^###'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md; git status --short" in ~/Workspace/dotfiles
 succeeded in 30ms:
10:## Architecture
17:## Regime activation and progress
29:## Parallel workers
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
95:## Message Contract v1
152:## `.orchestration` Workspace Layout
165:## Orchestrator Playbook
195:## Worker Playbook
225:## Codex seat worklogs
259:## Pitfalls
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
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a01.md
 M .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a01.md
 M .orchestration/acceptance/dotfiles-T129-pstack-asset-a01.md
 M .orchestration/acceptance/dotfiles-T133-gh-binding-a02-review-a01.md
 M .orchestration/acceptance/dotfiles-T133-gh-binding-a02.md
 M .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
 M .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/plans/024-replan-20261021-v2.md
 M .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md
 M .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md
 M .orchestration/tasks/dotfiles-T129-pstack-asset-review-a01.md
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a02.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-crit.json
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-review-receipt.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02.md
?? .orchestration/acceptance/dotfiles-T129-pstack-asset-review-a01.md
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
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T129-pstack-asset-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-codex-network-policy-a01.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-herdr-agents-eperm-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
?? .orchestration/tasks/dotfiles-T133-orchestrator-inbox-loop-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-followup-a03.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-audit-b801369.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-2b58663.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-b801369.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-crit.json
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-local-review-2b58663.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-05000f4.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-5f9caa3.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-5f9caa3.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-d61a0f2.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-d61a0f2.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-0ecdc07.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-2adb147.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-2adb147.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-3c1d54a.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-63d69cc.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-728f0ff.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-728f0ff.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-86513b2.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-86513b2.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-b700fe8.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c0a7dae.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c761dc8.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md.last.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-44134e3.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-e6b645f.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-e6b645f.md.last.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-059a40c.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-44134e3.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-e6b645f.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-local-review-059a40c.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-local-review-e6b645f.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-1d72f16.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-chain-128a208.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-chain-a30a43b.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-local-review-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-pr-comments.json
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md
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
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-audit-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-audit-28dde0f.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-chain-28dde0f.log
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-local-review-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-1f17d05.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-28dde0f.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-401573e.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json

**Preparing flat string output**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md | sed -n '100,132p'; rg -n 'Codex seat worklogs|"'^##|''^###'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02.md .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md" in ~/Workspace/dotfiles
 succeeded in 16ms:
   100	
   101	Stage 2 seats hcom omp --tag <team> --dir <worktree> instead of spawn.sh, with MODEL_PROFILE_<NAME>_OMP_MODEL and a verified omp model flag; writes <run-dir>/<seat>.launch.json {argv,pid,started_at}; --attach shows live arguments; check-regime-boundary.sh seat_pane_state/check-agent-runtime.py compare live process/record; dispatch refuses mismatched live seats (C-60:1); worker hcom hook requires re-plan: on S1 revise; remove-worker/--stale use hcom's member list. Report item-0 changes to member command/hook surface.
   102	Sources remain PR #383's branch-only seat-args.sh and seat-liveness/seat-launch-args owner records; VERIFY intended owned rows with the plan author. Serialize stage-2 seating with integration-seat-result-gate-cap-a01 and runtime checks with pstack-asset-a01. Orchestrator assigns a distinct stage-2 owner, never this reset's a02 ID. PR E owns SKILL/rules migration and agmsg-dispatch/Stop-hook/.chezmoiremove removal; the sole manifest exception here is constraint 2.
   103	
   104	## Validation and caps
   105	
   106	Fixtures first: one red-at-origin/main behavioral assertion and green-at-fix pair per constraint, round-1 remedy and item 0–7, with individually named matrix subtests. For absent new files, exercise the corresponding existing production route at baseline; missing command/import/setup failure is not red evidence. Record full baseline/red-fixture/fix SHAs, selectors, exact commands, stdout/stderr and real statuses; facts/scope checks accompany item-0/7 behavioral assertions.
   107	Reuse tests/unit/trusted_exec_contract.py unchanged: test_contract_attack_matrix covers shim nonexecution, hostile GIT_*/repository configuration, worker-root refusal and post-validation replacement; test_trusted_path_matrix covers realpath/parent/case handling. Use isolated fixture roots populated from production declarations, never environment override seams or live stores/sockets/panes/PRs; test_fixture_route_isolation proves isolation.
   108	Run uv run python -m unittest tests.unit.test_hcom_dispatch tests.unit.test_orchestrator_tools tests.unit.test_regime_counters -v through measured absolute uv/Python and design 5.14 item 9 isolation; paste the expanded invocation. Run make unit-test once on final head, bash -n/shellcheck on all five changed scripts, make format and make render-check; verify scope/status. Never run Bats locally.
   109	Resolve validation uv with /usr/bin/env -i PATH=/usr/bin:/bin HOME="<passwd-home>" UV_CACHE_DIR="<absolute-private-cache>" "<passwd-home>/.local/bin/mise" which uv; repeat for python and paste outputs. Host notes report Python 3.15.0 and uv's version/target directory without bin; never guess paths or treat discovery as runtime provenance.
   110	The final diff has at most 900 changed lines outside tests/ and .orchestration/, and at most 2200 under tests/.
   111	Measure with git diff --numstat <merge-base40> <head40>.
   112	Caps count PR-wide additions plus deletions from merge-base with authenticated main, never round deltas; expected 650/1500 leaves 250/700 headroom. Paste dispatch measurement_base40 (current branch head for a records-only round after update-branch), final authenticated main/head/merge-base40, every numstat row/totals; recount after update-branch. Do not silently raise caps.
   113	Explain every agmsg hit in the five scripts: only historical argument-form/PR-E documentation may remain, never store reads/sourcing. Unverified flags/schema, direct store writes, receipt mutation by history reads, test live sends, resend retries, workflow/permission changes and edits outside allowed_files are forbidden.
   114	
   115	## Execution, evidence and completion
   116	
   117	Worker Playbook step 4 applies: denial means blocked PONG with exact command/exit/boundary and hold, no escalation or alternate-surface retry. Claude a009 sends PONG/RESULT through existing agmsg-dispatch on macOS when already socket-allowlisted, or send.sh --body-file on its named route; this task changes no permission or its own reporting bus before merge.
   118	Continue tools/hcom-dispatch-bus-a01/draft PR #407, updated to post-prerequisite origin/main, carrying its two item-0 files' evidence into authorized a02 artifacts; or use a fresh branch/PR and close #407 with closure in RESULT. The entire PR diff must fit allowed_files; if old artifact paths prevent that within scope, use the fresh-branch route. Textual conflicts are blocked PONG for orchestrator integration, never worker hand merge. Push without shared Git-config changes.
   119	A replacement draft uses explicit --base main/--head/--title/--body-file/--draft and English text. Follow Worker Playbook step 15's ready/CI/Bot wait and one worker fix round; worker never merges. Apply normalised-comparison-lint-a01's Completion clause with advisory owner dotfiles-T129-hcom-dispatch-bus-a02-followup-a01, preserving INV-6 and surviving-P0/P1 stops.
   120	Under the allowed evidence directory write byte-identical task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and result.txt. Every item names producer/seat: worker (Claude seat a009), orchestrator (Claude seat, sandboxed Bash), or author (Codex review-profile seat). Paste verbatim outputs/statuses, selector/finding mappings, schema/send-ID/receipt/declaration facts, agmsg-hit table, denials and limits; learning/AutoSkill record actual triage/use; cost is observed or n/a. Keep plan/todo/learn uncommitted, one active todo per owner.
   121	RESULT names PR/#407 disposition, branch, full head/main/merge-base/measurement_base40, files, source_cap=900/test_cap=2200 and measured totals, every red/green pair, task_copy=<sha256 of .orchestration/dotfiles-T129-hcom-dispatch-bus-a02/task.md>, artifact paths, Bot findings/dispositions and deferred-stage facts. Pass agent-side review evidence and make require-crit-review before RESULT; no browser Crit/publication. Orchestrator alone follows Playbook step 10's final-head sweep/audit/acceptance/gate/merge order.
   122	Before review/anchor, orchestrator creates dotfiles-T129-hcom-dispatch-bus-a02-followup-a01's owner stub, confirms T133 merged, checks post-prerequisite inventory and measures design 5.14 items 1/2/9 deployment prerequisites. Store declaration deployment is verified after the code merges and before operational migration; absent declaration always refuses.
   123	Replace the pending Checks payload with .agents/worklog/orchestrator-glue/checks-paste.sh's hcom selector dotfiles-T129-hcom-dispatch-bus-a01, which selects probes only. Require exact masked commands/outputs/real statuses, canonical-main/design identity, executable provenance and absolute private UV_CACHE_DIR in every env -i contract; incomplete evidence blocks anchor/dispatch. Inventory differences require reauthoring.
   124	C-80 reviews the complete populated text, then anchor/dispatch those exact bytes with no later paste. Reserve up to 34 Checks payload lines within 180 total lines; amendments carry status=revise and new task_sha256 and repeat consumer verification.
   125	
   126	Amendment 1 (orchestrator, pre-anchor; `previous_sha256` above): design 5.14 item 9 excludes executables read from the shared uv directories, and this host's `~/.local/bin/hcom` resolves into `~/.local/share/uv/tools/hcom/bin/hcom` (PR A installed it with `uv tool install --force <verified wheel>`, receipt `update_hcom` in `~/.agents/.installed-manifest.json`, wheel `~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`). Constraint 1 therefore binds hcom by that absolute uv-tools path and, before every invocation, compares the sha256 of the resolved entry and of the wheel the receipt names with the values the Checks block records, refusing on mismatch (`refused: hcom binding`); no PATH or `~/.local/bin` lookup; one fixture plants a different file at the resolved path and asserts the refusal. The Checks block below is generated by `checks-paste.sh` (every line a command with its output and exit status, the design digest in two stages through a private file, the executable digests and item 1 observations shared with every task).
   127	
   128	Amendment 2 (orchestrator, pre-anchor; `previous_sha256` above; supersedes amendment 1's execution path): design 5.14 item 9 forbids executing from the shared uv directories, and a hash taken before an invocation from such a directory does not close replacement between the check and the run. The bus scripts therefore execute hcom only from the anchored checkout's private tool directory, `<checkout>/.agents/worklog/uv-tools/hcom/bin/hcom` (gitignored, under the main checkout, outside the Bash sandbox write roots of both seat kinds as rendered on canonical main, the Codex `writable_roots` and the Claude `allowWrite` lists recorded in the Checks; a Claude seat's unsandboxed file tools and every same-UID process remain design 5.14 item 0's residual, owned by dotfiles-T129-hcom-dispatch-bus-a02-followup-a01, so the run-time control is the digest check at every invocation, not the directory), installed by one new updater target `update_hcom_private` that verifies the receipt's wheel sha256 (`~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`) and runs `uv tool install --force <wheel>` with both `UV_TOOL_DIR` and `UV_TOOL_BIN_DIR` set under that directory (uv publishes the entry in `UV_TOOL_BIN_DIR`; without it the install would replace the public `~/.local/bin/hcom`), and the fixture asserts that the public entry's sha256 is unchanged by the install; the scripts refuse (`refused: hcom binding`) when the path is absent, is not a regular file, or when its sha256 differs from the value the install recorded beside it; the fixture plants a drifted wheel and a replaced entry and asserts both refusals. `~/.local/bin/hcom` and `~/.local/share/uv/tools` are never executed by these scripts. The generated Checks print every command with shell quoting (`%q`), so a recorded `sh -c` replays as run, and record the worker write boundaries as members: the rendered arrays at canonical main and the deployed settings of this host (the Claude `allowWrite`, `allowUnixSockets` and `excludedCommands` lists; the Codex `writable_roots` and `network_access`). The denial itself is measured by the worker, not pasted by the orchestrator: item 0's first command attempts to create a file under `<checkout>/.agents/worklog/uv-tools/` from inside its sandbox and records the refusal verbatim in sandbox.md; a success there is an `AGMSG-PONG v1 status=blocked`, because the protection premise would have failed.
   129	
   130	Amendment 3 (orchestrator, pre-anchor; `previous_sha256` above): the comparison-lint baseline at canonical main holds five R1 rows for `scripts/orchestrator/dispatch.sh` (lines 109, 190, 202, 209, 334; the Checks list them), and the lint exits 1 on a stale row of a changed file, so `scripts/lint-comparisons-baseline.tsv` joins allowed_files for stale-row removal only, closed by the existing lint test; new hits are fixed in the sources. The length rule reads 180 lines including the generated Checks block (34 payload lines). Nothing else changes.
   131	
   132	## Checks (pasted by the orchestrator before each send)
10:## Architecture
17:## Regime activation and progress
29:## Parallel workers
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
95:## Message Contract v1
152:## `.orchestration` Workspace Layout
165:## Orchestrator Playbook
195:## Worker Playbook
225:## Codex seat worklogs
259:## Pitfalls
# Acceptance: dotfiles-T129-hcom-dispatch-bus-a02

Reset of dotfiles-T129-hcom-dispatch-bus-a01 (plan 023 PR C stage 1; D-024-79/81). Brief .agents/worklog/orchestrator-glue/brief-hcom-dispatch-bus-a02.md (a01's items 0-7 plus the seven C-80 findings of 24d8b8d as binding constraints; after: gh-binding a02). Worker: the Claude seat a009. Security: true.

text-security:17775c1:1	bus-row-framing
text-security:17775c1:2	sent-row-identity
text-security:17775c1:3	store-location-declaration
- 2026-10-22T05:00Z: author-loop round 1 produced 120 lines; pre-send refused C3 (no row named the a02 task.md), the orchestrator added the task-copy row; C-80 of 17775c16 Verdict incorrect: P1 the marker format needs reader-side framing against embedded newlines, P2 sent-row identification by message id, P2 the store location needs an authoritative declaration; author-loop round 2 running with the findings fed back.

## Counters (INV-6)

amendments=0 revises=0 questions=0 at dispatch (not yet dispatched).
text-security:d61a0f2:0	correct
- 2026-10-22T05:13Z: author-loop round 2 (the three findings fed back) `Verdict: correct` at d61a0f2b (122 lines, unpopulated); Checks generated by checks-paste.sh (premises, line anchors, hcom/omp, after lineage; every line with its exit) and pasted; pre-send OK at 5f9caa3b9c7d738e0bb158298f776045fe2641900514f91606f317115b84d525; C-80 on the populated bytes next, then the anchor (a011); the dispatch to a009 waits for the gh-binding a02 merge (after:).
text-security:5f9caa3:1	checks-paste-provenance
text-security:5f9caa3:2	generated-digest-pipeline
- 2026-10-22T05:19Z: C-80 of the populated text (5f9caa3b) Verdict incorrect, two P2: the hcom case of the generator lacked the executable provenance and item 1/2/9 lines (they lived only in the gh-binding case) and hcom resolves into uv's tools directory, which item 9 excludes; the design-digest pipeline reported one status and lost quoting. Fixed in the mechanism: the provenance tail is shared by every task, the digest is two stages through a private file, the hcom case records realpath, entry digest, receipt and wheel digest; amendment 1 (pre-anchor) binds hcom by its absolute uv-tools path with a digest check against the receipt's wheel. Pre-send OK at 7c44fcaf6ad7a851f3b9e5a339880f79fbff629d82cc60a20cfd0ff2e99c4de0.
search: checks-paste-provenance -> none
re-plan: checks-paste-provenance (rows text-security:5f9caa3:1-2 of this lineage; the per-task command list omitted the shared provenance block) — specification: every generated Checks block carries, after the task's own lines, the executable digests, the git identity and the item 1 observations, and every multi-stage measurement is one command per stage with its own status; design: checks-paste.sh prints that tail after the per-task case for every task, so a new task cannot omit it; implementation: done in this round (the shared tail, the two-stage digest); verification: the next C-80 of this text and the first C-80 of every later text see the tail; a further refusal of this class stops the generator for redesign.
text-security:7c44fca:1	item9-execution-path
text-security:7c44fca:2	deployment-evidence
text-security:7c44fca:3	generated-command-quoting
- 2026-10-22T05:24Z: C-80 of 7c44fcaf Verdict incorrect (P1 execution from the shared uv directory with a check-then-run gap; P2 the Checks show modes, not the worker write boundaries; P2 the printed sh -c loses its argument boundary). Amendment 2 (pre-anchor): hcom executes only from the anchored checkout's private UV_TOOL_DIR, installed from the verified wheel by a new updater target (scripts/update-agent-assets.sh joins allowed_files with a closed row), refusals on absence or digest drift; the generator prints commands with %q and records the rendered Codex writable_roots and Claude allowWrite lines from canonical main. Pre-send OK at 7c44fcaf6ad7a851f3b9e5a339880f79fbff629d82cc60a20cfd0ff2e99c4de0; C-80 next (the second since this lineage's re-plan line).
- 2026-10-22T05:25Z: correction of the previous line: its first write of amendment 2 failed on an anchor mismatch and left the text at 7c44fcaf; the amendment is now applied and the pre-send sha is 2db29fc2af0ba7de58ca712bc24d03c9965a5918fce7d3fdac12d71be899bf70.
text-security:2db29fc:1	deployment-evidence
text-security:2db29fc:2	tool-install-publication
- 2026-10-22T05:28Z: C-80 of 2db29fc2 incorrect on two P2: the write-boundary probes had landed in the generator's gh branch (now in the shared tail, present in this block), and UV_TOOL_DIR alone lets uv publish the entry over the public ~/.local/bin/hcom (now UV_TOOL_BIN_DIR too, the fixture asserts the public entry unchanged, uv docs); the protection statement names the same-UID file-tool residual (item 0) with its owner. Pre-send OK at 4a0347ca9056aa69e0d7197c72ec305befae44677b8c570349f5e44a2981f8a5; C-80 next (the third since this lineage's re-plan line).
text-security:4a0347c:1	deployment-evidence
- 2026-10-22T05:31Z: C-80 of 4a0347ca incorrect on one P2: the write-boundary lines printed template keys only. Generator: the rendered arrays' members at canonical main and the deployed settings of this host (Claude allowWrite/allowUnixSockets/excludedCommands, Codex writable_roots/network_access); the text makes the denial a worker measurement at task start (item 0, sandbox.md) rather than an orchestrator paste. Pre-send OK at a22cf33a2a2353ae833c15cb60086275f36292cfcea3f29e1f2cff5dbf8c5c3f.
search: deployment-evidence -> none
re-plan: deployment-evidence (rows text-security:2db29fc:1, text-security:4a0347c:1 of this lineage; two reviews refused the orchestrator's write-boundary evidence, first absent then keys without members) — specification: a protection claim in a text is backed by the effective configuration members (rendered at canonical main and deployed on the host) in the Checks, and by a denial the seat itself measures at task start in sandbox.md, never by file modes or key names; design: checks-paste.sh prints the member lists for both seat kinds in its shared tail, and every text whose constraints rest on a seat boundary carries the task-start denial probe; implementation: done in this round for this text and the generator; verification: the next C-80 and the worker's sandbox.md at RESULT; a further refusal of this class stops the lineage for the operator.
text-security:4de6705:0	correct
- 2026-10-22T05:35Z: C-80 of 4de67056 (effective boundary members, worker-side denial probe) `Verdict: correct`; follow-up owner stub created; anchor review TASK dotfiles-T129-hcom-dispatch-bus-a02-review-a01 sent to a011; dispatch to a009 waits for the gh-binding a02 merge (after:).
anchor:a011:r1:1	touch-point-coverage
anchor:a011:r1:2	length-rule-mismatch
- 2026-10-22T05:39Z: anchor round 1 reject: the lint baseline is a touch point (five dispatch.sh R1 rows), the third row of class touch-point-coverage across the gh-binding and hcom lineages, so the mechanism now prints the baseline rows naming the task's scripts in every generated Checks block (checks-paste.sh shared tail); amendment 3 adds the baseline for stale-row removal only (closed by the existing lint test) and sets the length rule to 180; pre-send OK at e22742007ecfb5333e386e0141cc78e0490850739c8e3f36a89a5b11eb0dfbfe; C-80 next.
---
{
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T129-hcom-dispatch-bus-a02-review-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md task_sha256=852b32e2554751f44ffa0ec8f270c658a3e2e7d91dca1d4f7cb89355bd3fd111 design_file=.orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md design_sha256=4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c allowed_files=see-task-file forbidden_actions=edit;dispatch;network-write expected_result_file=.orchestration/dotfiles-T129-hcom-dispatch-bus-a02-review-a01/review.md done_signal=AGMSG-RESULT max_turns=20 note=anchor-review-of-the-hcom-dispatch-bus-a02-text(plan-023-PR-C-stage-1;C-80-correct-at-4de6705);read-only;reply-by-agmsg-dispatch-to-wW:p1 read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T129-hcom-dispatch-bus-a02-review-a01 status=hold round=1 pr=none verdict=reject reason=round-1-RESULT-received(item-4:the-lint-baseline's-five-dispatch.sh-rows;P2:the-length-sentence);amendment-3-written(baseline-for-stale-row-removal-only-closed-by-the-existing-lint-test,length-rule-180)-and-in-C-80;round-2-follows-a-correct-verdict next_action=hold:no-worker-action-until-the-round-2-ACCEPTANCE read_at=read"
  ]
}
---
# Acceptance: dotfiles-T129-hcom-dispatch-bus-a02-review-a01

Anchor review of the hcom-dispatch bus a02 text by a011 (worker-d). Design sha 4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c after C-80 correct at 4de6705.

## Counters (INV-6)

amendments=0 revises=0 questions=0 at dispatch.
- 2026-10-22T05:35Z: review TASK dispatched to a011 (task sha 852b32e2554751f44ffa0ec8f270c658a3e2e7d91dca1d4f7cb89355bd3fd111; design sha 4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c) (hand line).
- 2026-10-22T05:39Z: round 1 RESULT (a011, 05:38:15Z) reject on item 4 (the lint baseline's five R1 rows for dispatch.sh) and a P2 on the length sentence; hold sent; amendment 3 at e22742007ecfb5333e386e0141cc78e0490850739c8e3f36a89a5b11eb0dfbfe in C-80; round 2 after a correct verdict (hand line).

**Assessing information needs**
exec
/bin/zsh -lc "sed -n '225,258p' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md; cat .ua/meta.json; git rev-parse HEAD; nl -ba .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md | sed -n '89,100p'; cat .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01.md" in ~/Workspace/dotfiles
 succeeded in 66ms:
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
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
d06d94fd8eedcd0770c1c80c2b1596ec36109ef8
    89	## Binding constraints
    90	
    91	1. Resolve every executable/child under design 5.14 items 2/3/9, including hcom/sqlite3/jq/herdr/uv/Python and utilities; declared absolute tools/private namespace or realpath-bound checkout siblings only. Refuse inherited executable selection, mise shims and PATH lookup. Every env -i contract carries absolute private UV_CACHE_DIR; missing/relative cache refuses. test_private_namespace_matrix attacks all routes with PATH decoys, BUS_HISTORY/AGMSG_SCRIPTS overrides and startup payloads; test_private_cache_matrix covers cache refusals and hostile .venv/uv.toml/user-site inputs.
    92	2. Authorize assets.hcom.store_relative_path: .hcom in home/dot_agents/agent-config.yaml, verified as item 0's default or block for reauthoring. Production reads the protected deployed .agents/agent-config.yaml under passwd home, never a worker checkout/fixture declaration or inherited HOME/HCOM_DIR. Require a normalized home-relative directory, no traversal/absolute override, and the measured SQLite basename within it; both directory and database realpaths must remain in that declared location. Refuse nonempty inherited HCOM_DIR, unknown schema and absent/malformed declaration; never set HCOM_DIR or initialize a store. test_production_store_declaration consumes the actual source declaration and covers its deployed read/missing/malformed/escape cases; test_hostile_hcom_store_refused supplies a schema-compatible fabricated store via HCOM_DIR and proves refusal/no rows/both stores unchanged.
    93	3. Every task-copy/record consumer applies design 5.14 item 4 to bytes it actually reads: verify against TASK/ACCEPTANCE digests, then parse/use that same buffer, protected snapshot or held FD; missing/mismatch refuses. Pass checked content and explicit expected digest to checker/recorder/counter children without editing an out-of-scope consumer; inability to preserve binding blocks/replans. test_consumed_bytes_matrix replaces/restores a task copy after an earlier hash and proves consumer refusal, not acceptance-time detection alone.
    94	4. A record requires matching record_file= and record_sha256= on the bound line. Dispatch's record argument and counters' record path open once under canonical <checkout>/.orchestration/acceptance/, with no symlinked parent or escaping case alias; preserve opened identity through validation/read/write. Compare inode before/after validation and immediately before the locked atomic update; never reopen an unchecked pathname. Verify each consumed record buffer against its input digest before mutation; subsequent controlled writes produce the next explicit digest/identity. test_consumed_bytes_matrix covers symlinked parent, swapped inode, wrong digest and safe update; test_hcom_counter_matrix independently covers record consumption.
    95	5. Add no gh calls to the five scripts; existing counters PR reads adopt T133's bound gh, fixed github.com host and mryfmo/dotfiles repository (design 5.14 items 2/8/9). The named merge/update operations use the same binding. Dispatcher argv-stub tests establish only invocation shape; claim no executable/credential/Linux escape/authenticated-network boundary from them. Unmet prerequisite/deployment evidence blocks operational use.
    96	6. Before rendering any marker row, validate header fields and reject NUL and every body line separator recognized by downstream splitlines, including CR/LF, VT/FF, FS/GS/RS, NEL and Unicode line/paragraph separators; preserve ordinary tabs/quotes. Buffer validation so failure emits no partial history; readers refuse the failed read. test_history_forged_row_refused plants one hcom message containing a forged marker/ACCEPTANCE row, exercises bus-history plus all three consumers, and asserts refusal, no fabricated event/count, no send and no record mutation. test_hcom_marker_roundtrip proves valid marker compatibility; only ID selection in item 3 supersedes the old sent-row algorithm.
    97	7. test_status_revise_matrix and dispatch subfixtures use AGMSG-ACCEPTANCE v1 status=revise previous_head=… check=… task_sha256=…; preserve amendment digest validation. Receipt-identity fixtures cover send/query IDs missing/malformed/ambiguous and injection attempts, duplicate payloads with opposite receipts and a valid exact-ID match; store-declaration/framing fixtures separately close all three round-1 findings.
    98	
    99	## Deferred — stage 2 and PR E
   100	
---
format: 2
task_id: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - scripts/orchestrator/bus-history.sh
  - scripts/orchestrator/dispatch.sh
  - tests/unit/test_hcom_dispatch.py
  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01/**
after: [dotfiles-T129-hcom-dispatch-bus-a02]
---

# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 — owner of the hcom-dispatch bus a02 residual rows (owner stub)

Owner stub written 2026-10-22T05:35Z by the orchestrator seat (plan 023 PR C stage 1, D-024-79/81). Owns the residual rows of the a02 threat table (fixture-integrity and metadata automation, the same-UID file-tool residual of design 5.14 item 0 for the private tool directory, the deferred launcher half listed in a01). Never dispatched as a stub; authored after a02 merges from the advisory rows of its acceptance record.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```

exec
/bin/zsh -lc "rg -n '5.14|item 0|same.UID|namespace|GIT_|case.insens|trusted_exec' .orchestration/plans/024-design-quality.md; cat .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md.last.md .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md.last.md .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-05000f4.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
11:| S3 | GitHub-hosted runner の同時実行 20 ジョブ / macOS 5 ジョブ（Free〜Team 共通） | PR 1 本 = validate 1 + test 3（うち macOS 1）+ public-bootstrap 3（うち macOS 1）+ private-bootstrap 3（うち macOS 1）= 10 ジョブ・macOS 3。同時に走るのは PR 2 本分。F5 後は 7 ジョブ・macOS 1〜2 → PR 3〜5 本分 | F5（concurrency、private-bootstrap を PR から外す、in-job skip）。それでも天井は PR 3〜5 本の同時 CI。それ以上はキュー。self-hosted runner は公開リポジトリでは GitHub docs が非推奨（fork PR が任意コードを実行）なので採らない。macOS の test も対象ファイルが OS 非依存（`scripts/*.py`、`tests/unit/**` のみ）のときは in-job skip を検討（品質への影響を F5 の item 0 で判断） | `gh run list --json` から queued 時間の中央値 |
27:| Q4 | キャッシュ | F5 の item 0 で各 job の所要を step ごとに計測し、uv / pip / mise / Homebrew の取得が 1 分超なら `actions/cache` を入れる（効果が無ければ入れない） | 取得物は pin とハッシュで検証済み（PR A）なので cache は再現性を変えない | — |
95:### 5.14 残余（凍結後の計測事実、D-024-29）
103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
108:2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
109:3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.
117:7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:102 `BUS_HISTORY` selects an executable from inherited environment state without trusted-path validation; together with the PATH-resolved commands retained by row 48, an injected override or mise shim can execute code and fabricate the history used for dispatch decisions—the sanitized Checks commands do not constrain this runtime path.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:22 Read-only access and a schema guard do not authenticate history: attacker-selected `HCOM_DIR` can point to a schema-compatible fabricated store, supplying false senders, receipts and counts; no store-identity control or corresponding hostile-store test is specified.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:36 Acceptance-time byte comparison does not bind execution-time input: a same-user writer can replace the task pathname after hashing and restore it before acceptance; the design requires neither protected snapshot consumption nor consumer-side verification of the consumed bytes.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:103 The new counters write retains record handling that accepts independently supplied writable paths without canonical containment or stable file identity; symlinked parents, case aliases and replacement between validation and write can redirect acceptance evidence.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:52 `--match-head-commit` binds only the commit, not the executable, repository or host: inherited `GIT_*`, repository configuration and host configuration can redirect plain `gh` operations, while the text supplies no enforced execution prerequisite for Linux’s unsandboxed gh path; argv-stub tests cannot establish that boundary.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:100 The required TSV history is incompatible with the unchanged marker-format parsers required by items 3 and 5: `bus-read.sh` reports `open: none`, and dispatch cannot identify and record the sent row; the five-field contract also omits the required read marker.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:103 The new refusals and revise count select `verdict=revise`, but the cited acceptance records and existing protocol use `status=revise`, so ordinary revision directives bypass the required previous-head, test-selector and counters checks.

Not checked: implementation, live Linux execution or adversarial races; same-user isolation remains a declared residual, and these controls do not establish it.
Verdict: incorrectNo P0–P3 findings in the stated design’s 43 threat rows. Reviewed task SHA-256 `4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c`.

The requirements cover executable selection, inherited Git/startup environments, symlink/case handling, consumed-byte binding and receipt identity. Amendment 2 explicitly retains same-UID replacement as a residual; its digest check does not establish isolation. gh execution remains conditional on T133 and deployment evidence.

This does not authorize dispatch: prerequisite completion, residual-owner creation and required protection measurements remain outstanding conditions.

📝 まとめ: Reviewed the task, threat table and cited acceptance/review context without changing files.

Not checked: implementation, CI or live Linux/race execution; same-UID replacement and credential separation remain declared residual risks.
Verdict: correctReading additional input from stdin...
OpenAI Codex v0.163.0
--------
workdir: ~/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a1621f-9ae6-7881-82b0-d46bc169bed2
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
指定されたタスク本文と参照証跡を読み、各制御が実際の実行対象に結び付くかを確認します。関連スキルのレビュー手順を使い、読み取り専用で進めます。

exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in ~/Workspace/dotfiles
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
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a01.md
 M .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a01.md
 M .orchestration/acceptance/dotfiles-T129-pstack-asset-a01.md
 M .orchestration/acceptance/dotfiles-T133-gh-binding-a02-review-a01.md
 M .orchestration/acceptance/dotfiles-T133-gh-binding-a02.md
 M .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
 M .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/plans/024-replan-20261021-v2.md
 M .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md
 M .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md
 M .orchestration/tasks/dotfiles-T129-pstack-asset-review-a01.md
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a02.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-crit.json
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-review-receipt.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02.md
?? .orchestration/acceptance/dotfiles-T129-pstack-asset-review-a01.md
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
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T129-pstack-asset-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-codex-network-policy-a01.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-herdr-agents-eperm-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
?? .orchestration/tasks/dotfiles-T133-orchestrator-inbox-loop-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-followup-a03.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-audit-b801369.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-2b58663.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-b801369.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-crit.json
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-local-review-2b58663.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-05000f4.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-5f9caa3.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-5f9caa3.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-d61a0f2.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-d61a0f2.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-0ecdc07.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-2adb147.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-2adb147.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-3c1d54a.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-63d69cc.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-728f0ff.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-728f0ff.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-86513b2.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-86513b2.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-b700fe8.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c0a7dae.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c761dc8.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md.last.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-44134e3.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-e6b645f.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-e6b645f.md.last.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-059a40c.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-44134e3.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-e6b645f.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-local-review-059a40c.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-local-review-e6b645f.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-1d72f16.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-chain-128a208.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-chain-a30a43b.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-local-review-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-pr-comments.json
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md
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
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-audit-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-audit-28dde0f.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-chain-28dde0f.log
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-local-review-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-1f17d05.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-28dde0f.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-401573e.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T129-hcom-dispatch-bus-a02
     4	kind: code
     5	security: true
     6	previous_sha256: 4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c
     7	reset_of: [dotfiles-T129-hcom-dispatch-bus-a01]
     8	dispatch_status: blocked-pre-anchor
     9	design_review: {design: .orchestration/plans/024-design-quality.md}
    10	after: [dotfiles-T133-gh-binding-a02]
    11	allowed_files:
    12	  - home/dot_local/bin/common/executable_hcom-dispatch
    13	  - scripts/orchestrator/bus-history.sh
    14	  - scripts/orchestrator/dispatch.sh
    15	  - scripts/orchestrator/bus-read.sh
    16	  - scripts/regime-counters.sh
    17	  - tests/unit/test_*.py
    18	  - scripts/update-agent-assets.sh
    19	  - scripts/lint-comparisons-baseline.tsv
    20	  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a02/**
    21	  - home/dot_agents/agent-config.yaml
    22	threat_table:
    23	  - {control: "home/dot_local/bin/common/executable_hcom-dispatch", disposition: "closed: tests/unit/test_hcom_dispatch.py::HcomDispatchTest::test_transport_matrix"}
    24	  - {control: "scripts/orchestrator/bus-history.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_history_matrix"}
    25	  - {control: "scripts/orchestrator/dispatch.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_dispatch_matrix"}
    26	  - {control: "scripts/orchestrator/bus-read.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_bus_read_matrix"}
    27	  - {control: "scripts/regime-counters.sh", disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_hcom_counter_matrix"}
    28	  - {control: "tests/unit/test_*.py (test_hcom_dispatch.py)", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; independent audit checks send argv and receipt assertions."}
    29	  - {control: "scripts/update-agent-assets.sh (amendment 2: one new target, update_hcom_private, installs the verified hcom wheel the receipt names into the anchored checkout's private tool directory with UV_TOOL_DIR and UV_TOOL_BIN_DIR under <checkout>/.agents/worklog/uv-tools; nothing else in the updater changes)", disposition: "closed: tests/unit/test_hcom_dispatch.py::test_update_hcom_private_installs_the_verified_wheel_into_the_private_tool_dir_leaves_the_public_entry_unchanged_and_refuses_a_drifted_wheel"}
    30	  - {control: "scripts/lint-comparisons-baseline.tsv (amendment 3: stale-row removal only; the five R1 rows of scripts/orchestrator/dispatch.sh at lines 109, 190, 202, 209 and 334 fall away with the lines the constraints rewrite; no row is added, every new hit is fixed in the allowed sources)", disposition: "closed: tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline (the existing lint test, run by make unit-test on the final head)"}
    31	  - {control: "tests/unit/test_orchestrator_tools.py", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; audit checks real reader/dispatcher assertions and red/green logs."}
    32	  - {control: "tests/unit/test_regime_counters.py", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; audit checks counts and preserved seam cases."}
    33	  - {control: ".orchestration/dotfiles-T129-hcom-dispatch-bus-a02/** including task.md", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence automation; independently compare anchored bytes, full heads and verbatim validation."}
    34	  - {control: "home/dot_agents/agent-config.yaml", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_production_store_declaration"}
    35	  - {control: "private namespace", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_namespace_matrix"}
    36	  - {control: "store identity", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hostile_hcom_store_refused"}
    37	  - {control: "consumed-bytes binding", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_consumed_bytes_matrix"}
    38	  - {control: "history format", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_marker_roundtrip"}
    39	  - {control: "history framing", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_history_forged_row_refused"}
    40	  - {control: "receipt identity", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_concurrent_identical_send_receipts"}
    41	  - {control: "status key", disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_status_revise_matrix"}
    42	  - {control: "bound gh calls", disposition: "residual: dotfiles-T133-gh-binding-a02 owns executable/configuration/host binding; dispatcher argv stubs establish only invocation shape, never that boundary."}
    43	  - {control: "task metadata including dotfiles-T129-hcom-dispatch-bus-a01/task.md and dotfiles-T129-hcom-dispatch-bus-a02/task.md", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns metadata automation; check complete reset bytes and format-2 consistency, never reuse a01 approval."}
    44	  - {control: "metadata separators", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence automation; bind the whole text including front matter, separators and Checks."}
    45	  - {control: "bus rows and routing identities", disposition: "closed: tests/unit/test_hcom_dispatch.py::HcomDispatchTest::test_identity_and_payload_matrix"}
    46	  - {control: "in-process effects", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_fixture_route_isolation"}
    47	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployment evidence; require measured design 5.14 items 1/2/9 before operational use."}
    48	  - {control: "new or renamed scripts", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_migration_item_matrix"}
    49	  - {control: "design 5.14 item 0", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns unchanged item 0 obligations; this task establishes no same-UID or credential-separation boundary."}
    50	  - {control: "design 5.14 item 1", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns protection measurements for the deployed manifest, tools, namespace, snapshots and evidence."}
    51	  - {control: "design 5.14 item 2", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_namespace_matrix"}
    52	  - {control: "design 5.14 item 3", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_trusted_path_matrix"}
    53	  - {control: "design 5.14 item 4", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_consumed_bytes_matrix"}
    54	  - {control: "design 5.14 item 5", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns unchanged lock/reservation obligations; retain full head identities and existing locking."}
    55	  - {control: "design 5.14 item 6", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployment verification; distinguish assertions, CI and observed host execution."}
    56	  - {control: "design 5.14 item 7", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_contract_attack_matrix"}
    57	  - {control: "design 5.14 item 8", disposition: "residual: dotfiles-T133-gh-binding-a02 owns bound gh authority; add no approval reader and certify no local-object boundary."}
    58	  - {control: "design 5.14 item 9", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_cache_matrix"}
    59	  - {control: "design 5.14 item 10", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns denial records; apply Worker Playbook step 4 without escalation."}
    60	  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns integration records; only the orchestrator integrates the audited full head through Playbook step 10."}
    61	  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence refresh; repeat CI, sweep, audit, acceptance and gate after any head change."}
    62	  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns teardown records; none is planned and dirty state cannot be discarded implicitly."}
    63	  - {control: "orchestrator effect owner-stub creation", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns all assigned residuals; create its task stub before anchor, outside worker scope."}
    64	  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns Checks provenance; populate post-prerequisite observations before review/anchor."}
    65	  - {control: "orchestrator effect PR 407 closure", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns continuity records; record closure of 407 in RESULT if replaced."}
    66	  - {control: "orchestrator effect deployment", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployed store declaration and real-host verification; fixtures never enable an unmeasured route."}
    67	premises: []
    68	---
    69	
    70	# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a02 — plan 023 PR C, stage 1
    71	
    72	Reset a01 (2026-10-18); retain items 0–7 and deferred work, with binding remedies for C-80 24d8b8d (2026-10-22T04:44Z: five P1/two P2) and a02 round 1 (framing, receipt identity, undeclared production store). Plan 024 phase 2 starts here (D-024-79/D-024-81). Worker: Claude seat a009 (worker-c).
    73	Design 5.14 items 0–10 in .orchestration/plans/024-design-quality.md apply by reference. Closed rows cover their named assertions; broader host/environment/executable risks remain with the residual owners. This is accident/prompt-injection mitigation under item 0.
    74	Baseline means main after dotfiles-T133-gh-binding-a02 merges, including its bound gh and fixed host/repository. The audit-inherit-replan-json lineage is already on main as b22a5580 (#423); #390 is superseded.
    75	Historical host facts supplied by orchestrator (Claude seat, sandboxed Bash), 2026-10-22T04:44Z, main d06d94fd: manifest-pinned hcom 0.7.30 and omp exist at their declared install targets; upstream hcom 0.7.31 is not adopted. Dispatch sends at 245/350 and reads history at 46–59/347; bus-read reads at 49; counters read_history is at 94 and revise rule at 11; replay reads no bus; hcom-dispatch is absent. Reobserve post-prerequisite.
    76	The test wildcard expands only to test_hcom_dispatch.py (new), test_orchestrator_tools.py and test_regime_counters.py; the three executable modules have separate threat rows. The evidence wildcard is non-executable. Manifest authority is limited to the store declaration in constraint 2; preserve profiles, tools, pins and unrelated fields.
    77	
    78	## Items
    79	
    80	0. Before code, paste actual hcom version and top-level/send/list/events-or-history help, sender-selection/tag-scope facts, default directory, SQLite basename/schema, id/time/from/to/body/receipt columns and PRAGMA user_version into report.md. Verify the one-send form, returned stable message ID and deadline/receipt behavior; no guessed flags/schema. Choose a read command only if it reads the entire tag with every needed field/receipt without writes; otherwise use schema-guarded sqlite3 -readonly. Missing facts/tool/unique send identity means blocked PONG. test_migration_item_matrix includes a behavioral item-0 subfixture grounded in these observations.
    81	1. Add bus-history.sh <team> [--limit <n>]: chronological marker rows "<marker> [<at>] <from> → <to>: <body>", marker ● unread or ○ read from hcom receipts, at UTC ISO-8601. The old TSV output is withdrawn; an internal --json view retains actual message IDs and fields, with --message-id <id> selecting exactly one row in that view (missing/duplicate ID refuses). Validate IDs against item 0's grammar and bind query values, never interpolate SQL. Apply constraint 6 before emitting any output; unreadable/foreign store or unknown schema exits 1 with one stderr line, never initializes/writes/marks read. test_hcom_history_matrix covers populated/empty/bounded histories, both markers, schema refusal and unchanged store bytes.
    82	2. Add hcom-dispatch <team> <from> <to> <pane> <words…>, preserving agmsg-dispatch's argument form/space joining and deadline. Validate its existing strict identity grammar without sourcing agmsg; body is one argument after --, one send only. Capture that send's stable hcom ID and confirm only its receipt through the reader's exact-ID view; emit one machine receipt {id, read_at} for dispatch's recorder. Missing/ambiguous ID never falls back to sender/body matching or resends. Unconfirmed sends nudge once through bound herdr pane run "<pane>" "hcom: new message for <to>" and return the existing nonzero unconfirmed status. test_transport_matrix covers argv, leading dash, tabs/quotes, confirmation/no nudge and timeout/one nudge; test_identity_and_payload_matrix covers hostile inputs. Both new scripts have English shdoc headers/args/exitcodes.
    83	3. Replace both dispatch send sites and history windows with hcom-dispatch and bus-history. BUS_HISTORY is a repository-relative constant resolved against the checkout, never an environment override; remove AGMSG_SCRIPTS selection. Keep existing refusals, bounded windows and byte-identical outgoing line. Supersede only the old last-matching-row identity heuristic: record read/unread from the exact returned message ID; verify receipt shape and matching team/from/to/body through the reader's exact-ID view before recording; preserve the sender's nonzero timeout status after recording an unread receipt. test_hcom_dispatch_matrix and test_hcom_marker_roundtrip cover the actual subprocess route; test_concurrent_identical_send_receipts interleaves identical messages, reads only the other ID and proves this dispatch stays unread.
    84	4. For AGMSG-ACCEPTANCE v1 status=revise require previous_head= exactly once (40 lowercase hex), check= exactly once (nonempty), task_sha256= and a record argument. Before send run bound regime-counters.sh <task_id> --team <team> --history-only; failure refuses with stderr. Append stdout to the record JSON counters list as "<task_id> <ISO time> <lines joined by '; '>", preserving sort_keys/indent=2 and creating the list when absent. Named subfixtures cover every missing/duplicate/malformed field, absent record, failed counter and successful append. Other acceptance statuses skip only these revise-specific checks; verdict= never selects them.
    85	5. Switch bus-read's source to the same constant reader; preserve jq classification unchanged and rerun all five existing test_bus_read_* fixtures. test_hcom_bus_read_matrix and test_hcom_marker_roundtrip prove open-task classification and both markers from actual reader output.
    86	6. Switch counters' read_history to that reader; remove storage.sh sourcing. Use its internal --json view, retaining actual hcom IDs while adapting into the existing count input; preserve --history-file's TSV fixture contract and 20 existing seam cases, existing detail/count output and inherited audit/re-plan schema/deduplication. revises=max(RESULTs−1, this task's ACCEPTANCE status=revise count, 0); update the header only in meaning. Fixtures: 2 RESULTs/3 revises → 3 and 4 RESULTs/1 revise → 3; unrelated tasks/tabs and verdict-only revise do not inflate counts.
    87	7. Leave replay.sh (no bus read), agent-stop-gate.sh (stage-2 hook), SKILL/rules (PR E), agmsg-dispatch and .chezmoiremove (PR E) untouched; report each reason. test_migration_item_matrix names one behavioral subfixture per item 0–7, including operation with the agmsg store absent and item-7 migration/scope checks.
    88	
    89	## Binding constraints
    90	
    91	1. Resolve every executable/child under design 5.14 items 2/3/9, including hcom/sqlite3/jq/herdr/uv/Python and utilities; declared absolute tools/private namespace or realpath-bound checkout siblings only. Refuse inherited executable selection, mise shims and PATH lookup. Every env -i contract carries absolute private UV_CACHE_DIR; missing/relative cache refuses. test_private_namespace_matrix attacks all routes with PATH decoys, BUS_HISTORY/AGMSG_SCRIPTS overrides and startup payloads; test_private_cache_matrix covers cache refusals and hostile .venv/uv.toml/user-site inputs.
    92	2. Authorize assets.hcom.store_relative_path: .hcom in home/dot_agents/agent-config.yaml, verified as item 0's default or block for reauthoring. Production reads the protected deployed .agents/agent-config.yaml under passwd home, never a worker checkout/fixture declaration or inherited HOME/HCOM_DIR. Require a normalized home-relative directory, no traversal/absolute override, and the measured SQLite basename within it; both directory and database realpaths must remain in that declared location. Refuse nonempty inherited HCOM_DIR, unknown schema and absent/malformed declaration; never set HCOM_DIR or initialize a store. test_production_store_declaration consumes the actual source declaration and covers its deployed read/missing/malformed/escape cases; test_hostile_hcom_store_refused supplies a schema-compatible fabricated store via HCOM_DIR and proves refusal/no rows/both stores unchanged.
    93	3. Every task-copy/record consumer applies design 5.14 item 4 to bytes it actually reads: verify against TASK/ACCEPTANCE digests, then parse/use that same buffer, protected snapshot or held FD; missing/mismatch refuses. Pass checked content and explicit expected digest to checker/recorder/counter children without editing an out-of-scope consumer; inability to preserve binding blocks/replans. test_consumed_bytes_matrix replaces/restores a task copy after an earlier hash and proves consumer refusal, not acceptance-time detection alone.
    94	4. A record requires matching record_file= and record_sha256= on the bound line. Dispatch's record argument and counters' record path open once under canonical <checkout>/.orchestration/acceptance/, with no symlinked parent or escaping case alias; preserve opened identity through validation/read/write. Compare inode before/after validation and immediately before the locked atomic update; never reopen an unchecked pathname. Verify each consumed record buffer against its input digest before mutation; subsequent controlled writes produce the next explicit digest/identity. test_consumed_bytes_matrix covers symlinked parent, swapped inode, wrong digest and safe update; test_hcom_counter_matrix independently covers record consumption.
    95	5. Add no gh calls to the five scripts; existing counters PR reads adopt T133's bound gh, fixed github.com host and mryfmo/dotfiles repository (design 5.14 items 2/8/9). The named merge/update operations use the same binding. Dispatcher argv-stub tests establish only invocation shape; claim no executable/credential/Linux escape/authenticated-network boundary from them. Unmet prerequisite/deployment evidence blocks operational use.
    96	6. Before rendering any marker row, validate header fields and reject NUL and every body line separator recognized by downstream splitlines, including CR/LF, VT/FF, FS/GS/RS, NEL and Unicode line/paragraph separators; preserve ordinary tabs/quotes. Buffer validation so failure emits no partial history; readers refuse the failed read. test_history_forged_row_refused plants one hcom message containing a forged marker/ACCEPTANCE row, exercises bus-history plus all three consumers, and asserts refusal, no fabricated event/count, no send and no record mutation. test_hcom_marker_roundtrip proves valid marker compatibility; only ID selection in item 3 supersedes the old sent-row algorithm.
    97	7. test_status_revise_matrix and dispatch subfixtures use AGMSG-ACCEPTANCE v1 status=revise previous_head=… check=… task_sha256=…; preserve amendment digest validation. Receipt-identity fixtures cover send/query IDs missing/malformed/ambiguous and injection attempts, duplicate payloads with opposite receipts and a valid exact-ID match; store-declaration/framing fixtures separately close all three round-1 findings.
    98	
    99	## Deferred — stage 2 and PR E
   100	
   101	Stage 2 seats hcom omp --tag <team> --dir <worktree> instead of spawn.sh, with MODEL_PROFILE_<NAME>_OMP_MODEL and a verified omp model flag; writes <run-dir>/<seat>.launch.json {argv,pid,started_at}; --attach shows live arguments; check-regime-boundary.sh seat_pane_state/check-agent-runtime.py compare live process/record; dispatch refuses mismatched live seats (C-60:1); worker hcom hook requires re-plan: on S1 revise; remove-worker/--stale use hcom's member list. Report item-0 changes to member command/hook surface.
   102	Sources remain PR #383's branch-only seat-args.sh and seat-liveness/seat-launch-args owner records; VERIFY intended owned rows with the plan author. Serialize stage-2 seating with integration-seat-result-gate-cap-a01 and runtime checks with pstack-asset-a01. Orchestrator assigns a distinct stage-2 owner, never this reset's a02 ID. PR E owns SKILL/rules migration and agmsg-dispatch/Stop-hook/.chezmoiremove removal; the sole manifest exception here is constraint 2.
   103	
   104	## Validation and caps
   105	
   106	Fixtures first: one red-at-origin/main behavioral assertion and green-at-fix pair per constraint, round-1 remedy and item 0–7, with individually named matrix subtests. For absent new files, exercise the corresponding existing production route at baseline; missing command/import/setup failure is not red evidence. Record full baseline/red-fixture/fix SHAs, selectors, exact commands, stdout/stderr and real statuses; facts/scope checks accompany item-0/7 behavioral assertions.
   107	Reuse tests/unit/trusted_exec_contract.py unchanged: test_contract_attack_matrix covers shim nonexecution, hostile GIT_*/repository configuration, worker-root refusal and post-validation replacement; test_trusted_path_matrix covers realpath/parent/case handling. Use isolated fixture roots populated from production declarations, never environment override seams or live stores/sockets/panes/PRs; test_fixture_route_isolation proves isolation.
   108	Run uv run python -m unittest tests.unit.test_hcom_dispatch tests.unit.test_orchestrator_tools tests.unit.test_regime_counters -v through measured absolute uv/Python and design 5.14 item 9 isolation; paste the expanded invocation. Run make unit-test once on final head, bash -n/shellcheck on all five changed scripts, make format and make render-check; verify scope/status. Never run Bats locally.
   109	Resolve validation uv with /usr/bin/env -i PATH=/usr/bin:/bin HOME="<passwd-home>" UV_CACHE_DIR="<absolute-private-cache>" "<passwd-home>/.local/bin/mise" which uv; repeat for python and paste outputs. Host notes report Python 3.15.0 and uv's version/target directory without bin; never guess paths or treat discovery as runtime provenance.
   110	The final diff has at most 900 changed lines outside tests/ and .orchestration/, and at most 2200 under tests/.
   111	Measure with git diff --numstat <merge-base40> <head40>.
   112	Caps count PR-wide additions plus deletions from merge-base with authenticated main, never round deltas; expected 650/1500 leaves 250/700 headroom. Paste dispatch measurement_base40 (current branch head for a records-only round after update-branch), final authenticated main/head/merge-base40, every numstat row/totals; recount after update-branch. Do not silently raise caps.
   113	Explain every agmsg hit in the five scripts: only historical argument-form/PR-E documentation may remain, never store reads/sourcing. Unverified flags/schema, direct store writes, receipt mutation by history reads, test live sends, resend retries, workflow/permission changes and edits outside allowed_files are forbidden.
   114	
   115	## Execution, evidence and completion
   116	
   117	Worker Playbook step 4 applies: denial means blocked PONG with exact command/exit/boundary and hold, no escalation or alternate-surface retry. Claude a009 sends PONG/RESULT through existing agmsg-dispatch on macOS when already socket-allowlisted, or send.sh --body-file on its named route; this task changes no permission or its own reporting bus before merge.
   118	Continue tools/hcom-dispatch-bus-a01/draft PR #407, updated to post-prerequisite origin/main, carrying its two item-0 files' evidence into authorized a02 artifacts; or use a fresh branch/PR and close #407 with closure in RESULT. The entire PR diff must fit allowed_files; if old artifact paths prevent that within scope, use the fresh-branch route. Textual conflicts are blocked PONG for orchestrator integration, never worker hand merge. Push without shared Git-config changes.
   119	A replacement draft uses explicit --base main/--head/--title/--body-file/--draft and English text. Follow Worker Playbook step 15's ready/CI/Bot wait and one worker fix round; worker never merges. Apply normalised-comparison-lint-a01's Completion clause with advisory owner dotfiles-T129-hcom-dispatch-bus-a02-followup-a01, preserving INV-6 and surviving-P0/P1 stops.
   120	Under the allowed evidence directory write byte-identical task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and result.txt. Every item names producer/seat: worker (Claude seat a009), orchestrator (Claude seat, sandboxed Bash), or author (Codex review-profile seat). Paste verbatim outputs/statuses, selector/finding mappings, schema/send-ID/receipt/declaration facts, agmsg-hit table, denials and limits; learning/AutoSkill record actual triage/use; cost is observed or n/a. Keep plan/todo/learn uncommitted, one active todo per owner.
   121	RESULT names PR/#407 disposition, branch, full head/main/merge-base/measurement_base40, files, source_cap=900/test_cap=2200 and measured totals, every red/green pair, task_copy=<sha256 of .orchestration/dotfiles-T129-hcom-dispatch-bus-a02/task.md>, artifact paths, Bot findings/dispositions and deferred-stage facts. Pass agent-side review evidence and make require-crit-review before RESULT; no browser Crit/publication. Orchestrator alone follows Playbook step 10's final-head sweep/audit/acceptance/gate/merge order.
   122	Before review/anchor, orchestrator creates dotfiles-T129-hcom-dispatch-bus-a02-followup-a01's owner stub, confirms T133 merged, checks post-prerequisite inventory and measures design 5.14 items 1/2/9 deployment prerequisites. Store declaration deployment is verified after the code merges and before operational migration; absent declaration always refuses.
   123	Replace the pending Checks payload with .agents/worklog/orchestrator-glue/checks-paste.sh's hcom selector dotfiles-T129-hcom-dispatch-bus-a01, which selects probes only. Require exact masked commands/outputs/real statuses, canonical-main/design identity, executable provenance and absolute private UV_CACHE_DIR in every env -i contract; incomplete evidence blocks anchor/dispatch. Inventory differences require reauthoring.
   124	C-80 reviews the complete populated text, then anchor/dispatch those exact bytes with no later paste. Reserve up to 34 Checks payload lines within 180 total lines; amendments carry status=revise and new task_sha256 and repeat consumer verification.
   125	
   126	Amendment 1 (orchestrator, pre-anchor; `previous_sha256` above): design 5.14 item 9 excludes executables read from the shared uv directories, and this host's `~/.local/bin/hcom` resolves into `~/.local/share/uv/tools/hcom/bin/hcom` (PR A installed it with `uv tool install --force <verified wheel>`, receipt `update_hcom` in `~/.agents/.installed-manifest.json`, wheel `~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`). Constraint 1 therefore binds hcom by that absolute uv-tools path and, before every invocation, compares the sha256 of the resolved entry and of the wheel the receipt names with the values the Checks block records, refusing on mismatch (`refused: hcom binding`); no PATH or `~/.local/bin` lookup; one fixture plants a different file at the resolved path and asserts the refusal. The Checks block below is generated by `checks-paste.sh` (every line a command with its output and exit status, the design digest in two stages through a private file, the executable digests and item 1 observations shared with every task).
   127	
   128	Amendment 2 (orchestrator, pre-anchor; `previous_sha256` above; supersedes amendment 1's execution path): design 5.14 item 9 forbids executing from the shared uv directories, and a hash taken before an invocation from such a directory does not close replacement between the check and the run. The bus scripts therefore execute hcom only from the anchored checkout's private tool directory, `<checkout>/.agents/worklog/uv-tools/hcom/bin/hcom` (gitignored, under the main checkout, outside the Bash sandbox write roots of both seat kinds as rendered on canonical main, the Codex `writable_roots` and the Claude `allowWrite` lists recorded in the Checks; a Claude seat's unsandboxed file tools and every same-UID process remain design 5.14 item 0's residual, owned by dotfiles-T129-hcom-dispatch-bus-a02-followup-a01, so the run-time control is the digest check at every invocation, not the directory), installed by one new updater target `update_hcom_private` that verifies the receipt's wheel sha256 (`~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`) and runs `uv tool install --force <wheel>` with both `UV_TOOL_DIR` and `UV_TOOL_BIN_DIR` set under that directory (uv publishes the entry in `UV_TOOL_BIN_DIR`; without it the install would replace the public `~/.local/bin/hcom`), and the fixture asserts that the public entry's sha256 is unchanged by the install; the scripts refuse (`refused: hcom binding`) when the path is absent, is not a regular file, or when its sha256 differs from the value the install recorded beside it; the fixture plants a drifted wheel and a replaced entry and asserts both refusals. `~/.local/bin/hcom` and `~/.local/share/uv/tools` are never executed by these scripts. The generated Checks print every command with shell quoting (`%q`), so a recorded `sh -c` replays as run, and record the worker write boundaries as members: the rendered arrays at canonical main and the deployed settings of this host (the Claude `allowWrite`, `allowUnixSockets` and `excludedCommands` lists; the Codex `writable_roots` and `network_access`). The denial itself is measured by the worker, not pasted by the orchestrator: item 0's first command attempts to create a file under `<checkout>/.agents/worklog/uv-tools/` from inside its sandbox and records the refusal verbatim in sandbox.md; a success there is an `AGMSG-PONG v1 status=blocked`, because the protection premise would have failed.
   129	
   130	Amendment 3 (orchestrator, pre-anchor; `previous_sha256` above): the comparison-lint baseline at canonical main holds five R1 rows for `scripts/orchestrator/dispatch.sh` (lines 109, 190, 202, 209, 334; the Checks list them), and the lint exits 1 on a stale row of a changed file, so `scripts/lint-comparisons-baseline.tsv` joins allowed_files for stale-row removal only, closed by the existing lint test; new hits are fixed in the sources. The length rule reads 180 lines including the generated Checks block (34 payload lines). Nothing else changes.
   131	
   132	## Checks (pasted by the orchestrator before each send)
   133	
   134	```text
   135	observed 2026-10-22T05:39Z by the orchestrator (sandboxed Bash); every executable below is absolute and every command runs under the enumerated environment printed with it
   136	canonical main: clone (gh-free): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home /Library/Developer/CommandLineTools/usr/bin/git -c http.proxyAuthMethod=basic -c credential.http://localhost:49680.helper= clone -q --bare https://github.com/mryfmo/dotfiles.git <private>/dotfiles.git ` -> `` (exit 0)
   137	canonical main: ref: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git rev-parse refs/heads/main ` -> `d06d94fd8eedcd0770c1c80c2b1596ec36109ef8` (exit 0)
   138	canonical main: remote: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git config --get remote.origin.url ` -> `https://github.com/mryfmo/dotfiles.git` (exit 0)
   139	canonical main: config origins: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git config --list --show-origin ` -> `file:<private>/dotfiles.git/config	core.repositoryformatversion=0 file:<private>/dotfiles.git/config	core.filemode=true file:<private>/dotfiles.git/config	core.bare=true file:<private>/dotfiles.git/config	core.ignorecase=true file:<private>/dotfiles.git/config	core.precomposeunicode=true file:<private>/dotfiles.git/config	remote.origin.url=https://github.com/mryfmo/dotfiles.git` (exit 0)
   140	design file (canonical main): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c exec\ /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:.orchestration/plans/024-design-quality.md\ \>\ <private>/design.md ` -> `` (exit 0)
   141	design digest: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 <private>/design.md ` -> `a027b0210981ca4c4d4e832dc849af6a03cd71c408801f74d098c3b778dd9dbe  <private>/design.md` (exit 0)
   142	hcom version: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 ~/.local/bin/hcom --version ` -> `→ hcom v0.7.31 available — run `hcom update` hcom 0.7.30` (exit 0)
   143	hcom realpath: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/readlink -f ~/.local/bin/hcom ` -> `~/.local/share/uv/tools/hcom/bin/hcom` (exit 0)
   144	hcom entry digest: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 ~/.local/share/uv/tools/hcom/bin/hcom ` -> `7cd012d9a4d369de313ca4935cccda1ada6c8ffcd5e42ffa7eaeecdff7fc580e  ~/.local/share/uv/tools/hcom/bin/hcom` (exit 0)
   145	hcom install receipt (PR A): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n -E -B2 -A8 hcom ~/.agents/.installed-manifest.json ` -> `224-      "source_version": "18.11.3" 225-    }, 226:    "update_hcom": { 227-      "installed_at": "2026-10-20T05:02:45Z", 228-      "kind": "installer", 229-      "paths": [ 230:        "~/.local/bin/hcom", 231:        "~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl" 232-      ], 233-      "commands": [ 234:        "uv tool install --force <verified-hcom-wheel>" 235-      ], 236-      "source_version": "0.7.30" 237-    } 238-  } 239-}` (exit 0)
   146	hcom verified wheel digest (PR A): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 ~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl ` -> `764b6469ce4fe470094d2fb821285ea5e7e002726c68c634752663abe2410ea4  ~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl` (exit 0)
   147	omp path: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -la ~/.local/bin/omp ` -> `lrwxr-xr-x@ 1 <user>  staff  57 Oct 18 08:01 ~/.local/bin/omp -> ../lib/node_modules/@oh-my-pi/pi-coding-agent/dist/cli.js` (exit 0)
   148	premise 1: agmsg-dispatch in dispatch.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c agmsg-dispatch ~/Workspace/dotfiles/scripts/orchestrator/dispatch.sh ` -> `4` (exit 0)
   149	premise 2a: history.sh in bus-read.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c history.sh ~/Workspace/dotfiles/scripts/orchestrator/bus-read.sh ` -> `2` (exit 0)
   150	premise 2b: storage.sh in regime-counters.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c storage.sh ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `1` (exit 0)
   151	premise 3: bus reads in replay.sh: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -c -e history.sh -e storage.sh -e sqlite3 ~/Workspace/dotfiles/scripts/orchestrator/replay.sh ` -> `0` (exit 1)
   152	premise 4: hcom-dispatch absent: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls ~/Workspace/dotfiles/home/dot_local/bin/common/executable_hcom-dispatch ` -> `ls: ~/Workspace/dotfiles/home/dot_local/bin/common/executable_hcom-dispatch: No such file or directory` (exit 1)
   153	premise 5: revises rule: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n revises\ =\ AGMSG-RESULTs\ -\ 1 ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `11:#   1; revises = AGMSG-RESULTs - 1, whatever their status; questions = PONGs of` (exit 0)
   154	anchor: dispatch.sh call sites: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n agmsg-dispatch\ \"\$\{team\}\" ~/Workspace/dotfiles/scripts/orchestrator/dispatch.sh ` -> `245:[[ -n ${record} ]] || exec agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" 350:agmsg-dispatch "${team}" "${from}" "${to}" "${pane}" "${line}" || rc=$?` (exit 0)
   155	anchor: bus-read.sh history read: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n history.sh ~/Workspace/dotfiles/scripts/orchestrator/bus-read.sh ` -> `5:#   Plan 007 T718 (C-23). Reads the history through agmsg's `history.sh <team> 49:history="$("${AGMSG_SCRIPTS:-${HOME}/.agents/skills/agmsg/scripts}/history.sh" "${team}" "" "${limit}")" || {` (exit 0)
   156	anchor: regime-counters.sh read_history: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/grep -n read_history\(\) ~/Workspace/dotfiles/scripts/regime-counters.sh ` -> `94:read_history() {` (exit 0)
   157	after: audit-inherit-replan-json lineage on main: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /Library/Developer/CommandLineTools/usr/bin/git -C ~/Workspace/dotfiles log -1 --format=%h%x20%s b22a5580 ` -> `b22a5580 fix(orchestrator): the F1 lineage's owned rows: the gate's re-plan schema in the counters, no inherited unusable audit, one count per audit id (T129 audit-inherit replan-json followup a02) (#423)` (exit 0)
   158	executable digests: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/shasum -a 256 /Library/Developer/CommandLineTools/usr/bin/git /usr/bin/shasum /usr/bin/env /bin/ls /usr/bin/sed /usr/bin/readlink /usr/bin/grep /usr/bin/cut /usr/bin/tr /bin/date ~/.local/bin/mise ~/.local/share/mise/installs/github-cli-cli/latest/bin/gh ` -> `a73bf622a2e470d5d57a4b1d5aef1e8680e67278018d4858a2f93825b7d595c7  /Library/Developer/CommandLineTools/usr/bin/git 0812595f981a26f813d98dc380af14d4af427626c9339eda29eb849ae13de1e3  /usr/bin/shasum 2b2a1145527f00e8369fda0d2ffc523b520201bb08dbaf4b0bded837f7652ce0  /usr/bin/env 13f44bfe1c4af602da4465c834dbe7b16a5441ccbd843178b36116ee23422bfb  /bin/ls bb1cb46089269d91ba83ef291364e6e7121e7b27f12037629fe8daaf5238a559  /usr/bin/sed 2dc55748b64cf63d2452300bcf2cd3fc337425e76c76f8c484212026840d5a3c  /usr/bin/readlink afc3903988afaa5be7a19d595e66a95ead29cbb5102ff4dd2e4522089871f64a  /usr/bin/grep 71d96107b74d43fa54e2e2dbdb0148bf209f38a7ab29f6962bf9cd9df7c3c0a0  /usr/bin/cut 188d384d918a49fab8263deaa423e33068c99e9a4a5cb23fb971d2ed5b6e4d16  /usr/bin/tr 931edbfcbd847f3c1ccb504325a502db313ce20db27634744a7416c3c4b812f0  /bin/date 005b32b9c22ca9cb63ff9d35c74b3abe69c433e9ca655fea288ba3dcbe7e4918  ~/.local/bin/mise 8a4258433c81106343144857750316241759d06dcf16265cf3c4864a8f2f2ad6  ~/.local/share/mise/installs/github-cli-cli/latest/bin/gh` (exit 0)
   159	git version: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /Library/Developer/CommandLineTools/usr/bin/git --version ` -> `git version 2.54.0 (Apple Git-157)` (exit 0)
   160	git code signature: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /usr/bin/codesign -dv /Library/Developer/CommandLineTools/usr/bin/git ` -> `Executable=/Library/Developer/CommandLineTools/usr/bin/git Identifier=com.apple.git Format=Mach-O thin (arm64) CodeDirectory v=20400 size=29809 flags=0x2000(library-validation) hashes=926+2 location=embedded Signature size=4442 Signed Time=Sep 2, 2026 at 12:44:16 Info.plist entries=2 TeamIdentifier=59GAB85EFG Sealed Resources=none Internal requirements count=1 size=64` (exit 0)
   161	worker write roots (codex, rendered at canonical main, members): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:home/.chezmoitemplates/codex-config-managed.toml\ \|\ /usr/bin/sed\ -n\ \'/writable_roots/\,/\]/p\;/network_access/p\' ` -> `network_access = false writable_roots = ["{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db", "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams", "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run", "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools"]  [shell_environment_policy]` (exit 0)
   162	worker write roots (claude, rendered at canonical main, members): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:home/.chezmoitemplates/claude-settings-managed.json\ \|\ /usr/bin/sed\ -n\ \'/allowWrite/\,/\]/p\;/allowUnixSockets/\,/\]/p\;/excludedCommands/p\' ` -> `  "excludedCommands": [],     "allowWrite": [       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools",       "~/.cache/uv",       "~/.local/state/mise",       "~/.local/share/uv",       "~/Library/Caches/mise"     ]     "allowUnixSockets": [       "~/.config/herdr/herdr.sock"     ]   "excludedCommands": [],     "allowWrite": [       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",       "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools",       "~/.cache/uv",       "~/.local/state/mise",       "~/.local/share/uv"     ]     "allowUnixSockets": [       "~/.config/herdr/herdr.sock"     ]` (exit 0)
   163	effective claude sandbox on this host (deployed settings): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/sh -c /usr/bin/sed\ -n\ \'/allowWrite/\,/\]/p\;/allowUnixSockets/\,/\]/p\;/excludedCommands/p\'\ ~/.claude/settings.json ` -> `    "excludedCommands": [],       "allowWrite": [         "~/.agents/skills/agmsg/db",         "~/.agents/skills/agmsg/teams",         "~/.agents/skills/agmsg/run",         "~/.agents/skills/agmsg/ext-tools",         "~/.cache/uv",         "~/.local/state/mise",         "~/.local/share/uv",         "~/Library/Caches/mise"       ]       "allowUnixSockets": [         "~/.config/herdr/herdr.sock"       ]` (exit 0)
   164	effective codex sandbox on this host (deployed config and the launch-time roots herdr-agents adds): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/sh -c /usr/bin/sed\ -n\ \'/writable_roots/\,/\]/p\;/network_access/p\'\ ~/.codex/config.toml\;\ /usr/bin/grep\ -n\ writable_roots\ ~/Workspace/dotfiles/home/dot_local/bin/common/executable_herdr-agents ` -> `network_access = false writable_roots = ["~/.agents/skills/agmsg/db", "~/.agents/skills/agmsg/teams", "~/.agents/skills/agmsg/run", "~/.agents/skills/agmsg/ext-tools"]  [shell_environment_policy] 403:#   when the file exists but cannot be parsed, or its writable_roots is not a 408:# @stdout `sandbox_workspace_write.writable_roots=[...]`, or nothing. 409:function codex_worktree_writable_roots() { 427:    roots = tomllib.load(handle).get("sandbox_workspace_write", {}).get("writable_roots", []) 433:        printf 'herdr-agents: cannot read sandbox_workspace_write.writable_roots in %s as a list of strings (python3 3.11+ tomllib); the codex worker in %s gets no git metadata roots.\n' "${config}" "${worktree}" >&2 438:        if all(.[]; type == "string" and (contains("#") | not)) then "sandbox_workspace_write.writable_roots=" + tojson else error("unsupported") end' \ 454:#   codex_worktree_writable_roots) for a codex worker when a worktree is given. 489:        roots="$(codex_worktree_writable_roots "$2")"` (exit 0)
   165	private tool dir of the anchored checkout: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -ld ~/Workspace/dotfiles/.agents/worklog/uv-tools ~/Workspace/dotfiles/.agents/worklog ` -> `ls: ~/Workspace/dotfiles/.agents/worklog/uv-tools: No such file or directory drwxr-xr-x@ 7 <user>  staff  224 Oct 22 12:02 ~/Workspace/dotfiles/.agents/worklog` (exit 1)
   166	lint baseline rows naming the task's scripts (canonical main): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:scripts/lint-comparisons-baseline.tsv\ \|\ /usr/bin/grep\ -E\ \'\(executable_hcom-dispatch\|bus-history.sh\|dispatch.sh\|bus-read.sh\|regime-counters.sh\|update-agent-assets.sh\|agent-config.yaml\)\'\ \|\|\ true ` -> `scripts/orchestrator/dispatch.sh	R1	0aa21332a34f2b0fcc6d3e611138e68be68a5c96888545888202ad9d891eed4f scripts/orchestrator/dispatch.sh	R1	4dc66da0312fcc5ec625b21280b5780d6a5d991a13195a0cae35de72535665d6 scripts/orchestrator/dispatch.sh	R1	7da677eb3c35e65932431b5c74e602850bfee03f910d10100529d9bfcda4c370 scripts/orchestrator/dispatch.sh	R1	e36790337b32324fb95aca31583a592972e4628860426a8fe9a078f31557eac3 scripts/orchestrator/dispatch.sh	R1	f210c0c83e72ff3ea95a71f3075be49726b76ee318ad9c6c618de4b0d98be7e1` (exit 0)
   167	item 1 manifest: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -la ~/.agents/agent-config.yaml ` -> `-rw-r--r--@ 1 <user>  staff  32378 Oct 22 08:08 ~/.agents/agent-config.yaml` (exit 0)
   168	item 1 directory: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 /bin/ls -ld ~/.agents ` -> `drwxr-xr-x  11 <user>  staff  352 Oct 22 08:20 ~/.agents` (exit 0)
   169	```

**Reducing output size**
exec
/bin/zsh -lc "sed -n '1,115p' .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
---
format: 2
task_id: dotfiles-T129-hcom-dispatch-bus-a02
kind: code
security: true
previous_sha256: 4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c
reset_of: [dotfiles-T129-hcom-dispatch-bus-a01]
dispatch_status: blocked-pre-anchor
design_review: {design: .orchestration/plans/024-design-quality.md}
after: [dotfiles-T133-gh-binding-a02]
allowed_files:
  - home/dot_local/bin/common/executable_hcom-dispatch
  - scripts/orchestrator/bus-history.sh
  - scripts/orchestrator/dispatch.sh
  - scripts/orchestrator/bus-read.sh
  - scripts/regime-counters.sh
  - tests/unit/test_*.py
  - scripts/update-agent-assets.sh
  - scripts/lint-comparisons-baseline.tsv
  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a02/**
  - home/dot_agents/agent-config.yaml
threat_table:
  - {control: "home/dot_local/bin/common/executable_hcom-dispatch", disposition: "closed: tests/unit/test_hcom_dispatch.py::HcomDispatchTest::test_transport_matrix"}
  - {control: "scripts/orchestrator/bus-history.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_history_matrix"}
  - {control: "scripts/orchestrator/dispatch.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_dispatch_matrix"}
  - {control: "scripts/orchestrator/bus-read.sh", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_bus_read_matrix"}
  - {control: "scripts/regime-counters.sh", disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_hcom_counter_matrix"}
  - {control: "tests/unit/test_*.py (test_hcom_dispatch.py)", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; independent audit checks send argv and receipt assertions."}
  - {control: "scripts/update-agent-assets.sh (amendment 2: one new target, update_hcom_private, installs the verified hcom wheel the receipt names into the anchored checkout's private tool directory with UV_TOOL_DIR and UV_TOOL_BIN_DIR under <checkout>/.agents/worklog/uv-tools; nothing else in the updater changes)", disposition: "closed: tests/unit/test_hcom_dispatch.py::test_update_hcom_private_installs_the_verified_wheel_into_the_private_tool_dir_leaves_the_public_entry_unchanged_and_refuses_a_drifted_wheel"}
  - {control: "scripts/lint-comparisons-baseline.tsv (amendment 3: stale-row removal only; the five R1 rows of scripts/orchestrator/dispatch.sh at lines 109, 190, 202, 209 and 334 fall away with the lines the constraints rewrite; no row is added, every new hit is fixed in the allowed sources)", disposition: "closed: tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline (the existing lint test, run by make unit-test on the final head)"}
  - {control: "tests/unit/test_orchestrator_tools.py", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; audit checks real reader/dispatcher assertions and red/green logs."}
  - {control: "tests/unit/test_regime_counters.py", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns fixture-integrity automation; audit checks counts and preserved seam cases."}
  - {control: ".orchestration/dotfiles-T129-hcom-dispatch-bus-a02/** including task.md", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence automation; independently compare anchored bytes, full heads and verbatim validation."}
  - {control: "home/dot_agents/agent-config.yaml", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_production_store_declaration"}
  - {control: "private namespace", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_namespace_matrix"}
  - {control: "store identity", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hostile_hcom_store_refused"}
  - {control: "consumed-bytes binding", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_consumed_bytes_matrix"}
  - {control: "history format", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_hcom_marker_roundtrip"}
  - {control: "history framing", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_history_forged_row_refused"}
  - {control: "receipt identity", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_concurrent_identical_send_receipts"}
  - {control: "status key", disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_status_revise_matrix"}
  - {control: "bound gh calls", disposition: "residual: dotfiles-T133-gh-binding-a02 owns executable/configuration/host binding; dispatcher argv stubs establish only invocation shape, never that boundary."}
  - {control: "task metadata including dotfiles-T129-hcom-dispatch-bus-a01/task.md and dotfiles-T129-hcom-dispatch-bus-a02/task.md", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns metadata automation; check complete reset bytes and format-2 consistency, never reuse a01 approval."}
  - {control: "metadata separators", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence automation; bind the whole text including front matter, separators and Checks."}
  - {control: "bus rows and routing identities", disposition: "closed: tests/unit/test_hcom_dispatch.py::HcomDispatchTest::test_identity_and_payload_matrix"}
  - {control: "in-process effects", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_fixture_route_isolation"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployment evidence; require measured design 5.14 items 1/2/9 before operational use."}
  - {control: "new or renamed scripts", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_migration_item_matrix"}
  - {control: "design 5.14 item 0", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns unchanged item 0 obligations; this task establishes no same-UID or credential-separation boundary."}
  - {control: "design 5.14 item 1", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns protection measurements for the deployed manifest, tools, namespace, snapshots and evidence."}
  - {control: "design 5.14 item 2", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_namespace_matrix"}
  - {control: "design 5.14 item 3", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_trusted_path_matrix"}
  - {control: "design 5.14 item 4", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_consumed_bytes_matrix"}
  - {control: "design 5.14 item 5", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns unchanged lock/reservation obligations; retain full head identities and existing locking."}
  - {control: "design 5.14 item 6", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployment verification; distinguish assertions, CI and observed host execution."}
  - {control: "design 5.14 item 7", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_contract_attack_matrix"}
  - {control: "design 5.14 item 8", disposition: "residual: dotfiles-T133-gh-binding-a02 owns bound gh authority; add no approval reader and certify no local-object boundary."}
  - {control: "design 5.14 item 9", disposition: "closed: tests/unit/test_orchestrator_tools.py::OrchestratorToolsTest::test_private_cache_matrix"}
  - {control: "design 5.14 item 10", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns denial records; apply Worker Playbook step 4 without escalation."}
  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns integration records; only the orchestrator integrates the audited full head through Playbook step 10."}
  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns evidence refresh; repeat CI, sweep, audit, acceptance and gate after any head change."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns teardown records; none is planned and dirty state cannot be discarded implicitly."}
  - {control: "orchestrator effect owner-stub creation", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns all assigned residuals; create its task stub before anchor, outside worker scope."}
  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns Checks provenance; populate post-prerequisite observations before review/anchor."}
  - {control: "orchestrator effect PR 407 closure", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns continuity records; record closure of 407 in RESULT if replaced."}
  - {control: "orchestrator effect deployment", disposition: "residual: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 owns deployed store declaration and real-host verification; fixtures never enable an unmeasured route."}
premises: []
---

# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a02 — plan 023 PR C, stage 1

Reset a01 (2026-10-18); retain items 0–7 and deferred work, with binding remedies for C-80 24d8b8d (2026-10-22T04:44Z: five P1/two P2) and a02 round 1 (framing, receipt identity, undeclared production store). Plan 024 phase 2 starts here (D-024-79/D-024-81). Worker: Claude seat a009 (worker-c).
Design 5.14 items 0–10 in .orchestration/plans/024-design-quality.md apply by reference. Closed rows cover their named assertions; broader host/environment/executable risks remain with the residual owners. This is accident/prompt-injection mitigation under item 0.
Baseline means main after dotfiles-T133-gh-binding-a02 merges, including its bound gh and fixed host/repository. The audit-inherit-replan-json lineage is already on main as b22a5580 (#423); #390 is superseded.
Historical host facts supplied by orchestrator (Claude seat, sandboxed Bash), 2026-10-22T04:44Z, main d06d94fd: manifest-pinned hcom 0.7.30 and omp exist at their declared install targets; upstream hcom 0.7.31 is not adopted. Dispatch sends at 245/350 and reads history at 46–59/347; bus-read reads at 49; counters read_history is at 94 and revise rule at 11; replay reads no bus; hcom-dispatch is absent. Reobserve post-prerequisite.
The test wildcard expands only to test_hcom_dispatch.py (new), test_orchestrator_tools.py and test_regime_counters.py; the three executable modules have separate threat rows. The evidence wildcard is non-executable. Manifest authority is limited to the store declaration in constraint 2; preserve profiles, tools, pins and unrelated fields.

## Items

0. Before code, paste actual hcom version and top-level/send/list/events-or-history help, sender-selection/tag-scope facts, default directory, SQLite basename/schema, id/time/from/to/body/receipt columns and PRAGMA user_version into report.md. Verify the one-send form, returned stable message ID and deadline/receipt behavior; no guessed flags/schema. Choose a read command only if it reads the entire tag with every needed field/receipt without writes; otherwise use schema-guarded sqlite3 -readonly. Missing facts/tool/unique send identity means blocked PONG. test_migration_item_matrix includes a behavioral item-0 subfixture grounded in these observations.
1. Add bus-history.sh <team> [--limit <n>]: chronological marker rows "<marker> [<at>] <from> → <to>: <body>", marker ● unread or ○ read from hcom receipts, at UTC ISO-8601. The old TSV output is withdrawn; an internal --json view retains actual message IDs and fields, with --message-id <id> selecting exactly one row in that view (missing/duplicate ID refuses). Validate IDs against item 0's grammar and bind query values, never interpolate SQL. Apply constraint 6 before emitting any output; unreadable/foreign store or unknown schema exits 1 with one stderr line, never initializes/writes/marks read. test_hcom_history_matrix covers populated/empty/bounded histories, both markers, schema refusal and unchanged store bytes.
2. Add hcom-dispatch <team> <from> <to> <pane> <words…>, preserving agmsg-dispatch's argument form/space joining and deadline. Validate its existing strict identity grammar without sourcing agmsg; body is one argument after --, one send only. Capture that send's stable hcom ID and confirm only its receipt through the reader's exact-ID view; emit one machine receipt {id, read_at} for dispatch's recorder. Missing/ambiguous ID never falls back to sender/body matching or resends. Unconfirmed sends nudge once through bound herdr pane run "<pane>" "hcom: new message for <to>" and return the existing nonzero unconfirmed status. test_transport_matrix covers argv, leading dash, tabs/quotes, confirmation/no nudge and timeout/one nudge; test_identity_and_payload_matrix covers hostile inputs. Both new scripts have English shdoc headers/args/exitcodes.
3. Replace both dispatch send sites and history windows with hcom-dispatch and bus-history. BUS_HISTORY is a repository-relative constant resolved against the checkout, never an environment override; remove AGMSG_SCRIPTS selection. Keep existing refusals, bounded windows and byte-identical outgoing line. Supersede only the old last-matching-row identity heuristic: record read/unread from the exact returned message ID; verify receipt shape and matching team/from/to/body through the reader's exact-ID view before recording; preserve the sender's nonzero timeout status after recording an unread receipt. test_hcom_dispatch_matrix and test_hcom_marker_roundtrip cover the actual subprocess route; test_concurrent_identical_send_receipts interleaves identical messages, reads only the other ID and proves this dispatch stays unread.
4. For AGMSG-ACCEPTANCE v1 status=revise require previous_head= exactly once (40 lowercase hex), check= exactly once (nonempty), task_sha256= and a record argument. Before send run bound regime-counters.sh <task_id> --team <team> --history-only; failure refuses with stderr. Append stdout to the record JSON counters list as "<task_id> <ISO time> <lines joined by '; '>", preserving sort_keys/indent=2 and creating the list when absent. Named subfixtures cover every missing/duplicate/malformed field, absent record, failed counter and successful append. Other acceptance statuses skip only these revise-specific checks; verdict= never selects them.
5. Switch bus-read's source to the same constant reader; preserve jq classification unchanged and rerun all five existing test_bus_read_* fixtures. test_hcom_bus_read_matrix and test_hcom_marker_roundtrip prove open-task classification and both markers from actual reader output.
6. Switch counters' read_history to that reader; remove storage.sh sourcing. Use its internal --json view, retaining actual hcom IDs while adapting into the existing count input; preserve --history-file's TSV fixture contract and 20 existing seam cases, existing detail/count output and inherited audit/re-plan schema/deduplication. revises=max(RESULTs−1, this task's ACCEPTANCE status=revise count, 0); update the header only in meaning. Fixtures: 2 RESULTs/3 revises → 3 and 4 RESULTs/1 revise → 3; unrelated tasks/tabs and verdict-only revise do not inflate counts.
7. Leave replay.sh (no bus read), agent-stop-gate.sh (stage-2 hook), SKILL/rules (PR E), agmsg-dispatch and .chezmoiremove (PR E) untouched; report each reason. test_migration_item_matrix names one behavioral subfixture per item 0–7, including operation with the agmsg store absent and item-7 migration/scope checks.

## Binding constraints

1. Resolve every executable/child under design 5.14 items 2/3/9, including hcom/sqlite3/jq/herdr/uv/Python and utilities; declared absolute tools/private namespace or realpath-bound checkout siblings only. Refuse inherited executable selection, mise shims and PATH lookup. Every env -i contract carries absolute private UV_CACHE_DIR; missing/relative cache refuses. test_private_namespace_matrix attacks all routes with PATH decoys, BUS_HISTORY/AGMSG_SCRIPTS overrides and startup payloads; test_private_cache_matrix covers cache refusals and hostile .venv/uv.toml/user-site inputs.
2. Authorize assets.hcom.store_relative_path: .hcom in home/dot_agents/agent-config.yaml, verified as item 0's default or block for reauthoring. Production reads the protected deployed .agents/agent-config.yaml under passwd home, never a worker checkout/fixture declaration or inherited HOME/HCOM_DIR. Require a normalized home-relative directory, no traversal/absolute override, and the measured SQLite basename within it; both directory and database realpaths must remain in that declared location. Refuse nonempty inherited HCOM_DIR, unknown schema and absent/malformed declaration; never set HCOM_DIR or initialize a store. test_production_store_declaration consumes the actual source declaration and covers its deployed read/missing/malformed/escape cases; test_hostile_hcom_store_refused supplies a schema-compatible fabricated store via HCOM_DIR and proves refusal/no rows/both stores unchanged.
3. Every task-copy/record consumer applies design 5.14 item 4 to bytes it actually reads: verify against TASK/ACCEPTANCE digests, then parse/use that same buffer, protected snapshot or held FD; missing/mismatch refuses. Pass checked content and explicit expected digest to checker/recorder/counter children without editing an out-of-scope consumer; inability to preserve binding blocks/replans. test_consumed_bytes_matrix replaces/restores a task copy after an earlier hash and proves consumer refusal, not acceptance-time detection alone.
4. A record requires matching record_file= and record_sha256= on the bound line. Dispatch's record argument and counters' record path open once under canonical <checkout>/.orchestration/acceptance/, with no symlinked parent or escaping case alias; preserve opened identity through validation/read/write. Compare inode before/after validation and immediately before the locked atomic update; never reopen an unchecked pathname. Verify each consumed record buffer against its input digest before mutation; subsequent controlled writes produce the next explicit digest/identity. test_consumed_bytes_matrix covers symlinked parent, swapped inode, wrong digest and safe update; test_hcom_counter_matrix independently covers record consumption.
5. Add no gh calls to the five scripts; existing counters PR reads adopt T133's bound gh, fixed github.com host and mryfmo/dotfiles repository (design 5.14 items 2/8/9). The named merge/update operations use the same binding. Dispatcher argv-stub tests establish only invocation shape; claim no executable/credential/Linux escape/authenticated-network boundary from them. Unmet prerequisite/deployment evidence blocks operational use.
6. Before rendering any marker row, validate header fields and reject NUL and every body line separator recognized by downstream splitlines, including CR/LF, VT/FF, FS/GS/RS, NEL and Unicode line/paragraph separators; preserve ordinary tabs/quotes. Buffer validation so failure emits no partial history; readers refuse the failed read. test_history_forged_row_refused plants one hcom message containing a forged marker/ACCEPTANCE row, exercises bus-history plus all three consumers, and asserts refusal, no fabricated event/count, no send and no record mutation. test_hcom_marker_roundtrip proves valid marker compatibility; only ID selection in item 3 supersedes the old sent-row algorithm.
7. test_status_revise_matrix and dispatch subfixtures use AGMSG-ACCEPTANCE v1 status=revise previous_head=… check=… task_sha256=…; preserve amendment digest validation. Receipt-identity fixtures cover send/query IDs missing/malformed/ambiguous and injection attempts, duplicate payloads with opposite receipts and a valid exact-ID match; store-declaration/framing fixtures separately close all three round-1 findings.

## Deferred — stage 2 and PR E

Stage 2 seats hcom omp --tag <team> --dir <worktree> instead of spawn.sh, with MODEL_PROFILE_<NAME>_OMP_MODEL and a verified omp model flag; writes <run-dir>/<seat>.launch.json {argv,pid,started_at}; --attach shows live arguments; check-regime-boundary.sh seat_pane_state/check-agent-runtime.py compare live process/record; dispatch refuses mismatched live seats (C-60:1); worker hcom hook requires re-plan: on S1 revise; remove-worker/--stale use hcom's member list. Report item-0 changes to member command/hook surface.
Sources remain PR #383's branch-only seat-args.sh and seat-liveness/seat-launch-args owner records; VERIFY intended owned rows with the plan author. Serialize stage-2 seating with integration-seat-result-gate-cap-a01 and runtime checks with pstack-asset-a01. Orchestrator assigns a distinct stage-2 owner, never this reset's a02 ID. PR E owns SKILL/rules migration and agmsg-dispatch/Stop-hook/.chezmoiremove removal; the sole manifest exception here is constraint 2.

## Validation and caps

Fixtures first: one red-at-origin/main behavioral assertion and green-at-fix pair per constraint, round-1 remedy and item 0–7, with individually named matrix subtests. For absent new files, exercise the corresponding existing production route at baseline; missing command/import/setup failure is not red evidence. Record full baseline/red-fixture/fix SHAs, selectors, exact commands, stdout/stderr and real statuses; facts/scope checks accompany item-0/7 behavioral assertions.
Reuse tests/unit/trusted_exec_contract.py unchanged: test_contract_attack_matrix covers shim nonexecution, hostile GIT_*/repository configuration, worker-root refusal and post-validation replacement; test_trusted_path_matrix covers realpath/parent/case handling. Use isolated fixture roots populated from production declarations, never environment override seams or live stores/sockets/panes/PRs; test_fixture_route_isolation proves isolation.
Run uv run python -m unittest tests.unit.test_hcom_dispatch tests.unit.test_orchestrator_tools tests.unit.test_regime_counters -v through measured absolute uv/Python and design 5.14 item 9 isolation; paste the expanded invocation. Run make unit-test once on final head, bash -n/shellcheck on all five changed scripts, make format and make render-check; verify scope/status. Never run Bats locally.
Resolve validation uv with /usr/bin/env -i PATH=/usr/bin:/bin HOME="<passwd-home>" UV_CACHE_DIR="<absolute-private-cache>" "<passwd-home>/.local/bin/mise" which uv; repeat for python and paste outputs. Host notes report Python 3.15.0 and uv's version/target directory without bin; never guess paths or treat discovery as runtime provenance.
The final diff has at most 900 changed lines outside tests/ and .orchestration/, and at most 2200 under tests/.
Measure with git diff --numstat <merge-base40> <head40>.
Caps count PR-wide additions plus deletions from merge-base with authenticated main, never round deltas; expected 650/1500 leaves 250/700 headroom. Paste dispatch measurement_base40 (current branch head for a records-only round after update-branch), final authenticated main/head/merge-base40, every numstat row/totals; recount after update-branch. Do not silently raise caps.
Explain every agmsg hit in the five scripts: only historical argument-form/PR-E documentation may remain, never store reads/sourcing. Unverified flags/schema, direct store writes, receipt mutation by history reads, test live sends, resend retries, workflow/permission changes and edits outside allowed_files are forbidden.

## Execution, evidence and completion

exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|"'^##|''^###'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md; git status --short" in ~/Workspace/dotfiles
 succeeded in 30ms:
10:## Architecture
17:## Regime activation and progress
29:## Parallel workers
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
95:## Message Contract v1
152:## `.orchestration` Workspace Layout
165:## Orchestrator Playbook
195:## Worker Playbook
225:## Codex seat worklogs
259:## Pitfalls
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
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a01.md
 M .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a01.md
 M .orchestration/acceptance/dotfiles-T129-pstack-asset-a01.md
 M .orchestration/acceptance/dotfiles-T133-gh-binding-a02-review-a01.md
 M .orchestration/acceptance/dotfiles-T133-gh-binding-a02.md
 M .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
 M .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/plans/024-replan-20261021-v2.md
 M .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md
 M .orchestration/tasks/dotfiles-T129-pstack-asset-a01.md
 M .orchestration/tasks/dotfiles-T129-pstack-asset-review-a01.md
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a02.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-crit.json
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-review-receipt.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md
?? .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02.md
?? .orchestration/acceptance/dotfiles-T129-pstack-asset-review-a01.md
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
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md
?? .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T129-pstack-asset-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-codex-network-policy-a01.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-herdr-agents-eperm-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
?? .orchestration/tasks/dotfiles-T133-orchestrator-inbox-loop-a01.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-followup-a03.md
?? .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-audit-b801369.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-2b58663.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-b801369.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-crit.json
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-local-review-2b58663.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a01-text-security-24d8b8d.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-05000f4.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4de6705.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-5f9caa3.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-5f9caa3.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md.last.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-d61a0f2.md
?? .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-d61a0f2.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-0ecdc07.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-2adb147.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-2adb147.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-3c1d54a.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-63d69cc.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-728f0ff.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-728f0ff.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-86513b2.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-86513b2.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-b700fe8.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c0a7dae.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c761dc8.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md.last.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-44134e3.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-e6b645f.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-e6b645f.md.last.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-059a40c.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-44134e3.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-chain-e6b645f.log
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-local-review-059a40c.md
?? .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-local-review-e6b645f.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-1d72f16.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-chain-128a208.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-chain-a30a43b.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-local-review-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-pr-comments.json
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md
?? .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md
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
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-audit-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-audit-28dde0f.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-chain-28dde0f.log
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-local-review-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-1f17d05.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-28dde0f.md
?? .orchestration/validation/dotfiles-T133-trusted-entrypoint-pins-a01-security-28dde0f.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-401573e.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json

**Preparing flat string output**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md | sed -n '100,132p'; rg -n 'Codex seat worklogs|"'^##|''^###'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02.md .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md" in ~/Workspace/dotfiles
 succeeded in 16ms:
   100	
   101	Stage 2 seats hcom omp --tag <team> --dir <worktree> instead of spawn.sh, with MODEL_PROFILE_<NAME>_OMP_MODEL and a verified omp model flag; writes <run-dir>/<seat>.launch.json {argv,pid,started_at}; --attach shows live arguments; check-regime-boundary.sh seat_pane_state/check-agent-runtime.py compare live process/record; dispatch refuses mismatched live seats (C-60:1); worker hcom hook requires re-plan: on S1 revise; remove-worker/--stale use hcom's member list. Report item-0 changes to member command/hook surface.
   102	Sources remain PR #383's branch-only seat-args.sh and seat-liveness/seat-launch-args owner records; VERIFY intended owned rows with the plan author. Serialize stage-2 seating with integration-seat-result-gate-cap-a01 and runtime checks with pstack-asset-a01. Orchestrator assigns a distinct stage-2 owner, never this reset's a02 ID. PR E owns SKILL/rules migration and agmsg-dispatch/Stop-hook/.chezmoiremove removal; the sole manifest exception here is constraint 2.
   103	
   104	## Validation and caps
   105	
   106	Fixtures first: one red-at-origin/main behavioral assertion and green-at-fix pair per constraint, round-1 remedy and item 0–7, with individually named matrix subtests. For absent new files, exercise the corresponding existing production route at baseline; missing command/import/setup failure is not red evidence. Record full baseline/red-fixture/fix SHAs, selectors, exact commands, stdout/stderr and real statuses; facts/scope checks accompany item-0/7 behavioral assertions.
   107	Reuse tests/unit/trusted_exec_contract.py unchanged: test_contract_attack_matrix covers shim nonexecution, hostile GIT_*/repository configuration, worker-root refusal and post-validation replacement; test_trusted_path_matrix covers realpath/parent/case handling. Use isolated fixture roots populated from production declarations, never environment override seams or live stores/sockets/panes/PRs; test_fixture_route_isolation proves isolation.
   108	Run uv run python -m unittest tests.unit.test_hcom_dispatch tests.unit.test_orchestrator_tools tests.unit.test_regime_counters -v through measured absolute uv/Python and design 5.14 item 9 isolation; paste the expanded invocation. Run make unit-test once on final head, bash -n/shellcheck on all five changed scripts, make format and make render-check; verify scope/status. Never run Bats locally.
   109	Resolve validation uv with /usr/bin/env -i PATH=/usr/bin:/bin HOME="<passwd-home>" UV_CACHE_DIR="<absolute-private-cache>" "<passwd-home>/.local/bin/mise" which uv; repeat for python and paste outputs. Host notes report Python 3.15.0 and uv's version/target directory without bin; never guess paths or treat discovery as runtime provenance.
   110	The final diff has at most 900 changed lines outside tests/ and .orchestration/, and at most 2200 under tests/.
   111	Measure with git diff --numstat <merge-base40> <head40>.
   112	Caps count PR-wide additions plus deletions from merge-base with authenticated main, never round deltas; expected 650/1500 leaves 250/700 headroom. Paste dispatch measurement_base40 (current branch head for a records-only round after update-branch), final authenticated main/head/merge-base40, every numstat row/totals; recount after update-branch. Do not silently raise caps.
   113	Explain every agmsg hit in the five scripts: only historical argument-form/PR-E documentation may remain, never store reads/sourcing. Unverified flags/schema, direct store writes, receipt mutation by history reads, test live sends, resend retries, workflow/permission changes and edits outside allowed_files are forbidden.
   114	
   115	## Execution, evidence and completion
   116	
   117	Worker Playbook step 4 applies: denial means blocked PONG with exact command/exit/boundary and hold, no escalation or alternate-surface retry. Claude a009 sends PONG/RESULT through existing agmsg-dispatch on macOS when already socket-allowlisted, or send.sh --body-file on its named route; this task changes no permission or its own reporting bus before merge.
   118	Continue tools/hcom-dispatch-bus-a01/draft PR #407, updated to post-prerequisite origin/main, carrying its two item-0 files' evidence into authorized a02 artifacts; or use a fresh branch/PR and close #407 with closure in RESULT. The entire PR diff must fit allowed_files; if old artifact paths prevent that within scope, use the fresh-branch route. Textual conflicts are blocked PONG for orchestrator integration, never worker hand merge. Push without shared Git-config changes.
   119	A replacement draft uses explicit --base main/--head/--title/--body-file/--draft and English text. Follow Worker Playbook step 15's ready/CI/Bot wait and one worker fix round; worker never merges. Apply normalised-comparison-lint-a01's Completion clause with advisory owner dotfiles-T129-hcom-dispatch-bus-a02-followup-a01, preserving INV-6 and surviving-P0/P1 stops.
   120	Under the allowed evidence directory write byte-identical task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and result.txt. Every item names producer/seat: worker (Claude seat a009), orchestrator (Claude seat, sandboxed Bash), or author (Codex review-profile seat). Paste verbatim outputs/statuses, selector/finding mappings, schema/send-ID/receipt/declaration facts, agmsg-hit table, denials and limits; learning/AutoSkill record actual triage/use; cost is observed or n/a. Keep plan/todo/learn uncommitted, one active todo per owner.
   121	RESULT names PR/#407 disposition, branch, full head/main/merge-base/measurement_base40, files, source_cap=900/test_cap=2200 and measured totals, every red/green pair, task_copy=<sha256 of .orchestration/dotfiles-T129-hcom-dispatch-bus-a02/task.md>, artifact paths, Bot findings/dispositions and deferred-stage facts. Pass agent-side review evidence and make require-crit-review before RESULT; no browser Crit/publication. Orchestrator alone follows Playbook step 10's final-head sweep/audit/acceptance/gate/merge order.
   122	Before review/anchor, orchestrator creates dotfiles-T129-hcom-dispatch-bus-a02-followup-a01's owner stub, confirms T133 merged, checks post-prerequisite inventory and measures design 5.14 items 1/2/9 deployment prerequisites. Store declaration deployment is verified after the code merges and before operational migration; absent declaration always refuses.
   123	Replace the pending Checks payload with .agents/worklog/orchestrator-glue/checks-paste.sh's hcom selector dotfiles-T129-hcom-dispatch-bus-a01, which selects probes only. Require exact masked commands/outputs/real statuses, canonical-main/design identity, executable provenance and absolute private UV_CACHE_DIR in every env -i contract; incomplete evidence blocks anchor/dispatch. Inventory differences require reauthoring.
   124	C-80 reviews the complete populated text, then anchor/dispatch those exact bytes with no later paste. Reserve up to 34 Checks payload lines within 180 total lines; amendments carry status=revise and new task_sha256 and repeat consumer verification.
   125	
   126	Amendment 1 (orchestrator, pre-anchor; `previous_sha256` above): design 5.14 item 9 excludes executables read from the shared uv directories, and this host's `~/.local/bin/hcom` resolves into `~/.local/share/uv/tools/hcom/bin/hcom` (PR A installed it with `uv tool install --force <verified wheel>`, receipt `update_hcom` in `~/.agents/.installed-manifest.json`, wheel `~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`). Constraint 1 therefore binds hcom by that absolute uv-tools path and, before every invocation, compares the sha256 of the resolved entry and of the wheel the receipt names with the values the Checks block records, refusing on mismatch (`refused: hcom binding`); no PATH or `~/.local/bin` lookup; one fixture plants a different file at the resolved path and asserts the refusal. The Checks block below is generated by `checks-paste.sh` (every line a command with its output and exit status, the design digest in two stages through a private file, the executable digests and item 1 observations shared with every task).
   127	
   128	Amendment 2 (orchestrator, pre-anchor; `previous_sha256` above; supersedes amendment 1's execution path): design 5.14 item 9 forbids executing from the shared uv directories, and a hash taken before an invocation from such a directory does not close replacement between the check and the run. The bus scripts therefore execute hcom only from the anchored checkout's private tool directory, `<checkout>/.agents/worklog/uv-tools/hcom/bin/hcom` (gitignored, under the main checkout, outside the Bash sandbox write roots of both seat kinds as rendered on canonical main, the Codex `writable_roots` and the Claude `allowWrite` lists recorded in the Checks; a Claude seat's unsandboxed file tools and every same-UID process remain design 5.14 item 0's residual, owned by dotfiles-T129-hcom-dispatch-bus-a02-followup-a01, so the run-time control is the digest check at every invocation, not the directory), installed by one new updater target `update_hcom_private` that verifies the receipt's wheel sha256 (`~/.local/share/agent-assets/hcom/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl`) and runs `uv tool install --force <wheel>` with both `UV_TOOL_DIR` and `UV_TOOL_BIN_DIR` set under that directory (uv publishes the entry in `UV_TOOL_BIN_DIR`; without it the install would replace the public `~/.local/bin/hcom`), and the fixture asserts that the public entry's sha256 is unchanged by the install; the scripts refuse (`refused: hcom binding`) when the path is absent, is not a regular file, or when its sha256 differs from the value the install recorded beside it; the fixture plants a drifted wheel and a replaced entry and asserts both refusals. `~/.local/bin/hcom` and `~/.local/share/uv/tools` are never executed by these scripts. The generated Checks print every command with shell quoting (`%q`), so a recorded `sh -c` replays as run, and record the worker write boundaries as members: the rendered arrays at canonical main and the deployed settings of this host (the Claude `allowWrite`, `allowUnixSockets` and `excludedCommands` lists; the Codex `writable_roots` and `network_access`). The denial itself is measured by the worker, not pasted by the orchestrator: item 0's first command attempts to create a file under `<checkout>/.agents/worklog/uv-tools/` from inside its sandbox and records the refusal verbatim in sandbox.md; a success there is an `AGMSG-PONG v1 status=blocked`, because the protection premise would have failed.
   129	
   130	Amendment 3 (orchestrator, pre-anchor; `previous_sha256` above): the comparison-lint baseline at canonical main holds five R1 rows for `scripts/orchestrator/dispatch.sh` (lines 109, 190, 202, 209, 334; the Checks list them), and the lint exits 1 on a stale row of a changed file, so `scripts/lint-comparisons-baseline.tsv` joins allowed_files for stale-row removal only, closed by the existing lint test; new hits are fixed in the sources. The length rule reads 180 lines including the generated Checks block (34 payload lines). Nothing else changes.
   131	
   132	## Checks (pasted by the orchestrator before each send)
10:## Architecture
17:## Regime activation and progress
29:## Parallel workers
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
95:## Message Contract v1
152:## `.orchestration` Workspace Layout
165:## Orchestrator Playbook
195:## Worker Playbook
225:## Codex seat worklogs
259:## Pitfalls
# Acceptance: dotfiles-T129-hcom-dispatch-bus-a02

Reset of dotfiles-T129-hcom-dispatch-bus-a01 (plan 023 PR C stage 1; D-024-79/81). Brief .agents/worklog/orchestrator-glue/brief-hcom-dispatch-bus-a02.md (a01's items 0-7 plus the seven C-80 findings of 24d8b8d as binding constraints; after: gh-binding a02). Worker: the Claude seat a009. Security: true.

text-security:17775c1:1	bus-row-framing
text-security:17775c1:2	sent-row-identity
text-security:17775c1:3	store-location-declaration
- 2026-10-22T05:00Z: author-loop round 1 produced 120 lines; pre-send refused C3 (no row named the a02 task.md), the orchestrator added the task-copy row; C-80 of 17775c16 Verdict incorrect: P1 the marker format needs reader-side framing against embedded newlines, P2 sent-row identification by message id, P2 the store location needs an authoritative declaration; author-loop round 2 running with the findings fed back.

## Counters (INV-6)

amendments=0 revises=0 questions=0 at dispatch (not yet dispatched).
text-security:d61a0f2:0	correct
- 2026-10-22T05:13Z: author-loop round 2 (the three findings fed back) `Verdict: correct` at d61a0f2b (122 lines, unpopulated); Checks generated by checks-paste.sh (premises, line anchors, hcom/omp, after lineage; every line with its exit) and pasted; pre-send OK at 5f9caa3b9c7d738e0bb158298f776045fe2641900514f91606f317115b84d525; C-80 on the populated bytes next, then the anchor (a011); the dispatch to a009 waits for the gh-binding a02 merge (after:).
text-security:5f9caa3:1	checks-paste-provenance
text-security:5f9caa3:2	generated-digest-pipeline
- 2026-10-22T05:19Z: C-80 of the populated text (5f9caa3b) Verdict incorrect, two P2: the hcom case of the generator lacked the executable provenance and item 1/2/9 lines (they lived only in the gh-binding case) and hcom resolves into uv's tools directory, which item 9 excludes; the design-digest pipeline reported one status and lost quoting. Fixed in the mechanism: the provenance tail is shared by every task, the digest is two stages through a private file, the hcom case records realpath, entry digest, receipt and wheel digest; amendment 1 (pre-anchor) binds hcom by its absolute uv-tools path with a digest check against the receipt's wheel. Pre-send OK at 7c44fcaf6ad7a851f3b9e5a339880f79fbff629d82cc60a20cfd0ff2e99c4de0.
search: checks-paste-provenance -> none
re-plan: checks-paste-provenance (rows text-security:5f9caa3:1-2 of this lineage; the per-task command list omitted the shared provenance block) — specification: every generated Checks block carries, after the task's own lines, the executable digests, the git identity and the item 1 observations, and every multi-stage measurement is one command per stage with its own status; design: checks-paste.sh prints that tail after the per-task case for every task, so a new task cannot omit it; implementation: done in this round (the shared tail, the two-stage digest); verification: the next C-80 of this text and the first C-80 of every later text see the tail; a further refusal of this class stops the generator for redesign.
text-security:7c44fca:1	item9-execution-path
text-security:7c44fca:2	deployment-evidence
text-security:7c44fca:3	generated-command-quoting
- 2026-10-22T05:24Z: C-80 of 7c44fcaf Verdict incorrect (P1 execution from the shared uv directory with a check-then-run gap; P2 the Checks show modes, not the worker write boundaries; P2 the printed sh -c loses its argument boundary). Amendment 2 (pre-anchor): hcom executes only from the anchored checkout's private UV_TOOL_DIR, installed from the verified wheel by a new updater target (scripts/update-agent-assets.sh joins allowed_files with a closed row), refusals on absence or digest drift; the generator prints commands with %q and records the rendered Codex writable_roots and Claude allowWrite lines from canonical main. Pre-send OK at 7c44fcaf6ad7a851f3b9e5a339880f79fbff629d82cc60a20cfd0ff2e99c4de0; C-80 next (the second since this lineage's re-plan line).
- 2026-10-22T05:25Z: correction of the previous line: its first write of amendment 2 failed on an anchor mismatch and left the text at 7c44fcaf; the amendment is now applied and the pre-send sha is 2db29fc2af0ba7de58ca712bc24d03c9965a5918fce7d3fdac12d71be899bf70.
text-security:2db29fc:1	deployment-evidence
text-security:2db29fc:2	tool-install-publication
- 2026-10-22T05:28Z: C-80 of 2db29fc2 incorrect on two P2: the write-boundary probes had landed in the generator's gh branch (now in the shared tail, present in this block), and UV_TOOL_DIR alone lets uv publish the entry over the public ~/.local/bin/hcom (now UV_TOOL_BIN_DIR too, the fixture asserts the public entry unchanged, uv docs); the protection statement names the same-UID file-tool residual (item 0) with its owner. Pre-send OK at 4a0347ca9056aa69e0d7197c72ec305befae44677b8c570349f5e44a2981f8a5; C-80 next (the third since this lineage's re-plan line).
text-security:4a0347c:1	deployment-evidence
- 2026-10-22T05:31Z: C-80 of 4a0347ca incorrect on one P2: the write-boundary lines printed template keys only. Generator: the rendered arrays' members at canonical main and the deployed settings of this host (Claude allowWrite/allowUnixSockets/excludedCommands, Codex writable_roots/network_access); the text makes the denial a worker measurement at task start (item 0, sandbox.md) rather than an orchestrator paste. Pre-send OK at a22cf33a2a2353ae833c15cb60086275f36292cfcea3f29e1f2cff5dbf8c5c3f.
search: deployment-evidence -> none
re-plan: deployment-evidence (rows text-security:2db29fc:1, text-security:4a0347c:1 of this lineage; two reviews refused the orchestrator's write-boundary evidence, first absent then keys without members) — specification: a protection claim in a text is backed by the effective configuration members (rendered at canonical main and deployed on the host) in the Checks, and by a denial the seat itself measures at task start in sandbox.md, never by file modes or key names; design: checks-paste.sh prints the member lists for both seat kinds in its shared tail, and every text whose constraints rest on a seat boundary carries the task-start denial probe; implementation: done in this round for this text and the generator; verification: the next C-80 and the worker's sandbox.md at RESULT; a further refusal of this class stops the lineage for the operator.
text-security:4de6705:0	correct
- 2026-10-22T05:35Z: C-80 of 4de67056 (effective boundary members, worker-side denial probe) `Verdict: correct`; follow-up owner stub created; anchor review TASK dotfiles-T129-hcom-dispatch-bus-a02-review-a01 sent to a011; dispatch to a009 waits for the gh-binding a02 merge (after:).
anchor:a011:r1:1	touch-point-coverage
anchor:a011:r1:2	length-rule-mismatch
- 2026-10-22T05:39Z: anchor round 1 reject: the lint baseline is a touch point (five dispatch.sh R1 rows), the third row of class touch-point-coverage across the gh-binding and hcom lineages, so the mechanism now prints the baseline rows naming the task's scripts in every generated Checks block (checks-paste.sh shared tail); amendment 3 adds the baseline for stale-row removal only (closed by the existing lint test) and sets the length rule to 180; pre-send OK at e22742007ecfb5333e386e0141cc78e0490850739c8e3f36a89a5b11eb0dfbfe; C-80 next.
---
{
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T129-hcom-dispatch-bus-a02-review-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-review-a01.md task_sha256=852b32e2554751f44ffa0ec8f270c658a3e2e7d91dca1d4f7cb89355bd3fd111 design_file=.orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md design_sha256=4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c allowed_files=see-task-file forbidden_actions=edit;dispatch;network-write expected_result_file=.orchestration/dotfiles-T129-hcom-dispatch-bus-a02-review-a01/review.md done_signal=AGMSG-RESULT max_turns=20 note=anchor-review-of-the-hcom-dispatch-bus-a02-text(plan-023-PR-C-stage-1;C-80-correct-at-4de6705);read-only;reply-by-agmsg-dispatch-to-wW:p1 read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T129-hcom-dispatch-bus-a02-review-a01 status=hold round=1 pr=none verdict=reject reason=round-1-RESULT-received(item-4:the-lint-baseline's-five-dispatch.sh-rows;P2:the-length-sentence);amendment-3-written(baseline-for-stale-row-removal-only-closed-by-the-existing-lint-test,length-rule-180)-and-in-C-80;round-2-follows-a-correct-verdict next_action=hold:no-worker-action-until-the-round-2-ACCEPTANCE read_at=read"
  ]
}
---
# Acceptance: dotfiles-T129-hcom-dispatch-bus-a02-review-a01

Anchor review of the hcom-dispatch bus a02 text by a011 (worker-d). Design sha 4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c after C-80 correct at 4de6705.

## Counters (INV-6)

amendments=0 revises=0 questions=0 at dispatch.
- 2026-10-22T05:35Z: review TASK dispatched to a011 (task sha 852b32e2554751f44ffa0ec8f270c658a3e2e7d91dca1d4f7cb89355bd3fd111; design sha 4de67056f4dff9c88cdbaf8603298bd4d93721766d90b6a5a0095684c7fa0d5c) (hand line).
- 2026-10-22T05:39Z: round 1 RESULT (a011, 05:38:15Z) reject on item 4 (the lint baseline's five R1 rows for dispatch.sh) and a P2 on the length sentence; hold sent; amendment 3 at e22742007ecfb5333e386e0141cc78e0490850739c8e3f36a89a5b11eb0dfbfe in C-80; round 2 after a correct verdict (hand line).

**Assessing information needs**
exec
/bin/zsh -lc "sed -n '225,258p' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md; cat .ua/meta.json; git rev-parse HEAD; nl -ba .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md | sed -n '89,100p'; cat .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01.md" in ~/Workspace/dotfiles
 succeeded in 66ms:
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
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
d06d94fd8eedcd0770c1c80c2b1596ec36109ef8
    89	## Binding constraints
    90	
    91	1. Resolve every executable/child under design 5.14 items 2/3/9, including hcom/sqlite3/jq/herdr/uv/Python and utilities; declared absolute tools/private namespace or realpath-bound checkout siblings only. Refuse inherited executable selection, mise shims and PATH lookup. Every env -i contract carries absolute private UV_CACHE_DIR; missing/relative cache refuses. test_private_namespace_matrix attacks all routes with PATH decoys, BUS_HISTORY/AGMSG_SCRIPTS overrides and startup payloads; test_private_cache_matrix covers cache refusals and hostile .venv/uv.toml/user-site inputs.
    92	2. Authorize assets.hcom.store_relative_path: .hcom in home/dot_agents/agent-config.yaml, verified as item 0's default or block for reauthoring. Production reads the protected deployed .agents/agent-config.yaml under passwd home, never a worker checkout/fixture declaration or inherited HOME/HCOM_DIR. Require a normalized home-relative directory, no traversal/absolute override, and the measured SQLite basename within it; both directory and database realpaths must remain in that declared location. Refuse nonempty inherited HCOM_DIR, unknown schema and absent/malformed declaration; never set HCOM_DIR or initialize a store. test_production_store_declaration consumes the actual source declaration and covers its deployed read/missing/malformed/escape cases; test_hostile_hcom_store_refused supplies a schema-compatible fabricated store via HCOM_DIR and proves refusal/no rows/both stores unchanged.
    93	3. Every task-copy/record consumer applies design 5.14 item 4 to bytes it actually reads: verify against TASK/ACCEPTANCE digests, then parse/use that same buffer, protected snapshot or held FD; missing/mismatch refuses. Pass checked content and explicit expected digest to checker/recorder/counter children without editing an out-of-scope consumer; inability to preserve binding blocks/replans. test_consumed_bytes_matrix replaces/restores a task copy after an earlier hash and proves consumer refusal, not acceptance-time detection alone.
    94	4. A record requires matching record_file= and record_sha256= on the bound line. Dispatch's record argument and counters' record path open once under canonical <checkout>/.orchestration/acceptance/, with no symlinked parent or escaping case alias; preserve opened identity through validation/read/write. Compare inode before/after validation and immediately before the locked atomic update; never reopen an unchecked pathname. Verify each consumed record buffer against its input digest before mutation; subsequent controlled writes produce the next explicit digest/identity. test_consumed_bytes_matrix covers symlinked parent, swapped inode, wrong digest and safe update; test_hcom_counter_matrix independently covers record consumption.
    95	5. Add no gh calls to the five scripts; existing counters PR reads adopt T133's bound gh, fixed github.com host and mryfmo/dotfiles repository (design 5.14 items 2/8/9). The named merge/update operations use the same binding. Dispatcher argv-stub tests establish only invocation shape; claim no executable/credential/Linux escape/authenticated-network boundary from them. Unmet prerequisite/deployment evidence blocks operational use.
    96	6. Before rendering any marker row, validate header fields and reject NUL and every body line separator recognized by downstream splitlines, including CR/LF, VT/FF, FS/GS/RS, NEL and Unicode line/paragraph separators; preserve ordinary tabs/quotes. Buffer validation so failure emits no partial history; readers refuse the failed read. test_history_forged_row_refused plants one hcom message containing a forged marker/ACCEPTANCE row, exercises bus-history plus all three consumers, and asserts refusal, no fabricated event/count, no send and no record mutation. test_hcom_marker_roundtrip proves valid marker compatibility; only ID selection in item 3 supersedes the old sent-row algorithm.
    97	7. test_status_revise_matrix and dispatch subfixtures use AGMSG-ACCEPTANCE v1 status=revise previous_head=… check=… task_sha256=…; preserve amendment digest validation. Receipt-identity fixtures cover send/query IDs missing/malformed/ambiguous and injection attempts, duplicate payloads with opposite receipts and a valid exact-ID match; store-declaration/framing fixtures separately close all three round-1 findings.
    98	
    99	## Deferred — stage 2 and PR E
   100	
---
format: 2
task_id: dotfiles-T129-hcom-dispatch-bus-a02-followup-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - scripts/orchestrator/bus-history.sh
  - scripts/orchestrator/dispatch.sh
  - tests/unit/test_hcom_dispatch.py
  - .orchestration/dotfiles-T129-hcom-dispatch-bus-a02-followup-a01/**
after: [dotfiles-T129-hcom-dispatch-bus-a02]
---

# AGMSG-TASK dotfiles-T129-hcom-dispatch-bus-a02-followup-a01 — owner of the hcom-dispatch bus a02 residual rows (owner stub)

Owner stub written 2026-10-22T05:35Z by the orchestrator seat (plan 023 PR C stage 1, D-024-79/81). Owns the residual rows of the a02 threat table (fixture-integrity and metadata automation, the same-UID file-tool residual of design 5.14 item 0 for the private tool directory, the deferred launcher half listed in a01). Never dispatched as a stub; authored after a02 merges from the advisory rows of its acceptance record.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```


**Avoiding self-logs and filtering context**
codex
本文は PATH・Git 環境・レコード差し替えの対策を要求し、同一 UID の隔離と gh の境界は残余リスク／前提条件として分けています。追加された private hcom インストールが、検証した wheel と実行時の Python・モジュールまで結び付けられるかを確認しています。

exec
/bin/zsh -lc "sed -n '103,125p' .orchestration/plans/024-design-quality.md; cat .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md.last.md .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md.last.md .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md.last.md .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md.last.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "cat .orchestration/acceptance/dotfiles-T133-gh-binding-a02.md .orchestration/acceptance/dotfiles-T133-gh-binding-a02-review-a01.md; sed -n '1,130p' .orchestration/tasks/dotfiles-T133-gh-binding-a02.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "/usr/bin/python3 -I -c 'import json; d=json.load(open(\".ua/knowledge-graph.json\")); print(type(d).__name__); nodes=d.get(\"nodes\",[]); print(\"\\n\".join(str({k:n.get(k) for k in (\"summary\",\"filePath\")}) for n in nodes if any(s in str(n.get(\"filePath\",\"\")) for s in (\"update-agent-assets\",\"trusted_exec_contract\",\"regime-counters\",\"orchestrator/dispatch\"))))'; git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD | head -25; sed -n '1,160p' tests/unit/trusted_exec_contract.py; rg -n 'update_hcom|UV_TOOL|hcom' scripts/update-agent-assets.sh" in ~/Workspace/dotfiles
 succeeded in 144ms:
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
[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:73 The marker format specifies no escaping or rejection of embedded newlines: one worker message can contain a forged acceptance row that the unchanged parsers treat as a separate event; the named history/payload tests need a reader-side framing attack.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:75 Preserving sent-row identification retains selection of the last matching sender/recipient/body rather than the sent message’s ID; two concurrent identical messages can record `read` while this send remains unread, which the prescribed roundtrip fixture does not test.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:84 The required manifest-bound store location has no declaration in `agent-config.yaml`, and neither this task nor T133 authorizes adding it; fixture-only declarations cannot establish the production binding—specify its authoritative location and authorize any required declaration with a threat row.

📝 まとめ: Reviewed all 40 threat rows and cited context; found three design gaps, with parser and receipt-selection behavior confirmed by in-memory probes. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-user isolation and deployment protections remain unverified residuals.
Verdict: incorrect[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:122 Amendment 1 still executes hcom from the shared uv directory forbidden by design item 9: hashing before invocation leaves replacement between verification and execution possible, while the prescribed fixture replaces the file before verification; consume a verified, protected executable and test that handoff before marking this boundary closed.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:153 The Checks show owner-writable filesystem modes, not worker write denial or protection of the executable namespace, snapshots and cache; they do not supply the item 1/2/9 deployment measurements required before review/anchor.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:132 The generated command still loses the argument boundary around `sh -c`’s command string: replaying the printed `sh -c exec …` does not execute the recorded Git command, so separate exit statuses have not resolved the previous evidence-reproducibility finding.

The installed hcom currently matches the executable inside the pinned wheel; the first finding concerns the subsequent execution handoff.

📝 まとめ: Reviewed all 42 threat rows and cited acceptance/review context; three findings remain for orchestrator disposition. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-UID isolation and credential separation remain declared residual risks.
Verdict: incorrect[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:126 The claimed worker write-boundary measurements are absent from Checks: the generator puts those probes in its non-hcom branch; filesystem modes—and even allowWrite lists alone—cannot establish protection against Claude’s unsandboxed file tools, so the private executable and adjacent digest remain unproven until actual denial controls are measured.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:28 Setting only `UV_TOOL_DIR` leaves executable publication at `~/.local/bin`; the prescribed `uv tool install --force` therefore replaces the existing public hcom entry, an unmodelled effect the named private-install/drift test need not detect—bind `UV_TOOL_BIN_DIR` privately and assert the public entry remains unchanged. [uv documentation](https://docs.astral.sh/uv/reference/cli/#uv-tool-install)

📝 まとめ: Reviewed all 43 threat rows and referenced acceptance/review context; two findings remain for orchestrator disposition. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-UID isolation and credential separation remain declared residual risks.
Verdict: incorrect[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:158 The claimed worker write-boundary measurement prints only unrendered template keys, omitting allowWrite/socket members and effective seat settings; it cannot establish amendment 2’s private-directory protection—record effective per-seat boundaries and denial evidence before anchoring.

📝 まとめ: Reviewed all 43 threat rows and cited acceptance/review history; one deployment-evidence finding remains. No files changed.

Not checked: future implementation, CI or live Linux/race execution; same-UID replacement and credential separation remain declared residual risks.
Verdict: incorrect
 succeeded in 182ms:
---
{
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-gh-binding-a02 round=1 reset_of=dotfiles-T133-gh-binding-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-g task_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md task_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 preconditions=met:.orchestration/acceptance/dotfiles-T133-gh-binding-a02.md overlap_ok=378,395,396,404,406,410,411,412,419,420,424,426,431,432,439,440 deadline=none done_signal=AGMSG-RESULT note=a012:gh-binding-a02(reset-of-a01;anchored-by-review-a01-round-3-after-C-80-correct;bytes-must-not-change);origin/main=7b21659eb2e86198bde458136d9e31b3e836cdb0;fresh-branch-tools/gh-binding-a02-from-that-main;security:true;Worker-Playbook-step-4:every-command-sandboxed,HTTPS-push-without--u;report-route-per-line-109:send.sh-dotfiles-conformance-codex-standard-dot-a012-claude-deep-dot---body-file-<file>(never-agmsg-dispatch);reply-AGMSG-PONG-v1-status=alive-by-that-route-first read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02 status=hold round=1 pr=none reason=blocked-PONG-received(packed-refs.lock-denials-with-exit-0-on-the-branch-creation);the-orchestrator-verified-tools/gh-binding-a02-as-the-worktree-HEAD:keep-it;the-denial-is-the-T64-read-only-common-dir-working-as-designed,so-amendment-1-of-the-text-makes-an-exit-0-denial-on-.git/packed-refs.lock-or-.git/config.lock-measured-state-recorded-in-sandbox.md(every-other-denial-stays-blocked);amendment-1-is-in-C-80-and-the-anchor-review-now,then-an-ACCEPTANCE-revise-carries-its-task_sha256 next_action=hold:do-not-retry;resume-only-on-the-ACCEPTANCE-that-names-the-amended-task_sha256 read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02 status=revise pr=none round=1 amendment=1 task_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md previous_task_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 task_sha256=2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 reason=amendment-1(anchored-by-a011-round-4,C-80-correct):an-exit-0-Operation-not-permitted-on-.git/packed-refs.lock-or-.git/config.lock-with-the-effect-present-is-measured-state-recorded-in-sandbox.md,never-retried-outside;every-other-denial-stays-blocked;the-branch-tools/gh-binding-a02-you-created-at-03:05Z-is-kept(verified-as-the-worktree-HEAD);refresh-the-task-copy-to-these-bytes next_action=resume-round-1-on-the-kept-branch:record-the-03:05Z-denial-in-sandbox.md-as-measured-state,then-Items-0-7-as-written;reply-AGMSG-PONG-v1-status=alive-by-send.sh-first read_at=read",
    "AGMSG-PING v1 task_id=dotfiles-T133-gh-binding-a02 reason=answer-to-your-question-(no-rule-sentence-changes,the-text's-item-4-constants-rule-applies):(1)the-gate-keeps-executing-the-authenticated-base's-collector-(require-crit-review.py:608-615)-and-never-refuses-it-for-lacking-the-binding-flags,otherwise-a02-could-not-pass-its-own-gate;(2)for-a-selected-collector-older-than-the-binding-the-gate-supplies-the-missing-pieces-as-explicit-constants-of-the-constructed-environment:the-executable-through-item-2's-private-PATH-link-gh->the-declared-path(no-wrapper,a-link-in-the-private-namespace),the-host-as-GH_HOST=github.com(gh-help-environment:GH_HOST-sets-the-hostname-for-commands-that-would-otherwise-assume-github.com),the-repository-already-pinned-by-the---repo-argument-the-gate-passes;ambient-GH_HOST/GH_REPO/GH_CONFIG_DIR-are-dropped-first(the-text's-reject-ambient-rule)-and-the-constants-are-recorded-in-the-allowed-name-set;(3)one-fixture:a-selected-collector-predating-the-binding-runs-with-those-constants,a-decoy-gh-on-the-inherited-PATH-is-never-executed,and-a-planted-ambient-GH_HOST-does-not-reach-the-child;(4)after-a02-merges-the-base-collector-carries---hostname-and-the-constants-remain-as-defence-in-depth;continue-round-1;reply-AGMSG-PONG-v1-status=alive-by-send.sh read_at=unread",
    "AGMSG-PING v1 task_id=dotfiles-T133-gh-binding-a02 reason=answer-to-your-second-question(no-rule-sentence-changes):your-push,PR-creation-and-CI-are-Worker-Playbook-step-2/4-operations-from-inside-the-Codex-sandbox(T64:sandbox_workspace_write.network_access=true,HTTPS-git-push-origin-<branch>-without--u,gh-pr-create---draft),and-that-sandbox-path-IS-the-authorized-transport-route(design-5.14-item-10);row-38's-'authenticated-use-is-blocked-until-the-orchestrator-measures-items-2/9'-scopes-the-consumers-this-task-binds(the-orchestrator's-acceptance-time-gh-reads-and-the-gate's-collector),not-your-transport;no-parent-measurement-or-deployed-config-evidence-is-a-precondition-of-your-push;for-your-own-commands-keep-constructing-env--i-with-absolute-executables-and-UV_CACHE_DIR-as-you-do;proceed:tests,lint,review,push,draft-PR,gh-pr-ready,CI,Bot-wait,RESULT;reply-AGMSG-PONG-v1-status=alive-by-send.sh read_at=read",
    "AGMSG-PING v1 task_id=dotfiles-T133-gh-binding-a02 reason=answer-to-your-blocked-PONG/RESULT(no-rule-sentence-changes):(1)the-denied-write-is-gh's-optional-run-log-cache(~/.cache/gh),outside-your-writable-roots;gh-honours-XDG_CACHE_HOME(gh-help-environment),so-supply-it-as-an-explicit-nonsecret-constant-of-your-env--i-contract(item-4),pointing-at-a-private-directory-under-your-worktree-or-TMPDIR,and-re-run-the-read-inside-the-sandbox:this-is-a-constructed-constant,not-a-cache-relocation-outside-the-boundary-and-not-a-retry-outside;(2)the-regime-context-is-not-a-required-check-and-its-failure-on-this-PR-is-the-known-task-copy-class(main-does-not-carry-the-a02-text-yet,D-024-64/67):record-it,do-not-hold-on-it;(3)finish-round-1:gh-pr-ready-456,CI-on-the-final-head,the-Bot-wait-of-step-15,then-AGMSG-RESULT-status=ready_for_review-by-send.sh;the-orchestrator-copies-your-artifacts-from-worker-g-into-the-main-checkout-at-that-RESULT read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02 status=revise pr=456 previous_head=2804b176adc394109dd1f7df86e23cdb87f6b2f5 round=1 text=unchanged reason=your-blocked-RESULT-of-05:02:46Z-is-answered-by-the-PING-of-05:0xZ(XDG_CACHE_HOME-as-an-explicit-constant;the-regime-context-is-not-required);this-line-records-the-continuation-of-round-1-for-the-bus:the-text-is-unchanged,no-new-check=;finish-gh-pr-ready,CI-on-the-final-head(test-ubuntu-26.04-client-is-red-at-2804b176:fix-it-within-round-1),the-Bot-wait,then-RESULT-ready_for_review next_action=continue-round-1 read_at=unread",
    "AGMSG-PING v1 task_id=dotfiles-T133-gh-binding-a02 reason=answer-to-your-third-question:yes,amendment-2-is-written(Item-6-authorizes-test_orch_gate_path.py,test_orchestrator_tools.py,test_chain_review_scripts.py,test_validate_agent_assets.py-and-test_agmsg_orchestration_docs.py-for-fixture-adoption-only,no-assertion-weakened;test-cap-1000,source-cap-350;a-per-module-line-in-report.md)and-is-in-C-80-then-the-anchor;you-receive-it-as-an-ACCEPTANCE-status=revise-with-the-new-task_sha256;until-then-continue-the-independent-fixes-and-do-not-edit-the-five-legacy-modules read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02 status=revise pr=456 previous_head=2804b176adc394109dd1f7df86e23cdb87f6b2f5 round=1 amendment=3 task_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md previous_task_sha256=2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 task_sha256=e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 reason=amendments-2-and-3(anchored-by-a011-round-6,C-80-correct):amendment-2:Item-0's-inventory-sentence-authorizes-test_orch_gate_path.py,test_orchestrator_tools.py,test_chain_review_scripts.py,test_validate_agent_assets.py-and-test_agmsg_orchestration_docs.py-for-fixture-adoption-only(a-fixture-adopts-the-bound-gh-and-the-declaration;no-assertion-weakened,deleted-or-re-targeted),test-cap-1000,source-cap-350,one-line-per-legacy-module-in-report.md;amendment-3:scripts/lint-comparisons-baseline.tsv-is-allowed-for-stale-row-removal-only(the-orch-gate.sh-R1-row),new-R1/R4-hits-fixed-in-the-sources,closed-by-LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline;refresh-the-task-copy-to-these-bytes next_action=continue-round-1:adopt-the-fixtures,remove-the-stale-baseline-row,fix-the-lint-hits-in-the-sources,push,CI-green-on-the-final-head,Bot-wait,AGMSG-RESULT-ready_for_review-by-send.sh read_at=read"
  ]
}
---
# Acceptance: dotfiles-T133-gh-binding-a02

Reset of `dotfiles-T133-gh-binding-a01` under S-R5 (D-024-69: the essential remedy for the executable-provenance wall of the a07 and regime-ci-followup lineages). The a01 text stopped after two C-80 rounds (3bf2a79: 3 P1 + 3 P2; 6486b79: 1 P1 + 1 P2, the gate's gh descendants `scripts/require-crit-review.py:519/615` and `scripts/pr-feedback.py:84`); brief `.agents/worklog/orchestrator-glue/brief-gh-binding-a02.md` widened the scope to those descendants (design items 6 and 7) and author-loop produced the a02 text. Security: true. Worker: the Codex seat a012 at worker-g (not seated while the Claude seat a014 occupies worker-g; operator step).

text-security:c761dc8:0	correct
text-security:0ecdc07:1	checks-paste-provenance
text-security:0ecdc07:2	checks-paste-provenance
text-security:c0a7dae:0	correct
anchor:a011:r1:1	checks-paste-provenance
anchor:a011:r1:2	checks-paste-provenance
text-security:b700fe8:1	checks-paste-provenance
text-security:b700fe8:2	evidence-abbreviation

- 2026-10-22T00:5xZ: author-loop round 1: pre-send OK, C-80 `Verdict: correct` on the unpopulated text (c761dc8e, 124 lines).
- 2026-10-22T01:02Z: Checks pasted (gh-free bare clone, mise pin, installed gh, interpreter bindings, items 1 and 2); owner stub `dotfiles-T133-gh-binding-followup-a01` expanded (19 residual rows, three future routes, `after: [dotfiles-T133-gh-binding-a02]`); C-80 of 0ecdc07c `Verdict: incorrect`, two P1: the canonical measurement ran bare `git`/`shasum` without a measured executable namespace, and without a constructed environment (GIT_CONFIG_*, GIT_DIR).
- 2026-10-22T01:14Z: re-measured with `/Library/Developer/CommandLineTools/usr/bin/git` (Apple Git-157, codesign com.apple.git, sha256 recorded) and `/usr/bin/shasum` under `/usr/bin/env -i` with the enumerated proxy variables, `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_DIR=<private clone>`: main 7da0cdfab9de9fbea673b82379acd4e317115065, design digest a027b0210981ca4c4d4e832dc849af6a03cd71c408801f74d098c3b778dd9dbe (both equal to the unbound read); C-80 of c0a7dae7 `Verdict: correct`.
- 2026-10-22T01:24Z: anchor review `dotfiles-T133-gh-binding-a02-review-a01` (a011) `verdict=reject`, two findings on the paste: Checks line 128 described UV_CACHE_DIR as a `mktemp -d` cache (contradicts design 5.14 item 9: parent-supplied absolute cache, refused when absent; mktemp for tests only), and lines 127-130 held claims without their commands. Lines 127-130 rewritten with each command and its output and the item-9 wording (sha 5d62e48e18f41ab5f12cc62b03f6ed855425ffa8324f97689cdb46e200111811, pre-send OK). The next C-80 was refused by C-92: three reviews since the newest re-plan line.
search: checks-paste-provenance -> none
re-plan: checks-paste-provenance (rows text-security:0ecdc07:1-2, anchor:a011:r1:1-2; three reviews of one text in which the orchestrator's own Checks paste, not the task design, was refused: an unbound measurement, then claims without commands and a cache sentence contradicting item 9) — specification: a Checks line is a pasted command and its output under an enumerated environment with absolute executables and their digests, never a paraphrase; the paste is produced by one glue script from a fixed command list, so a review judges the list once; design: `checks-paste.sh <task>` in the orchestrator glue prints the block from the list the text names (canonical main and design digest by bound git in a private clone, the mise pin line, the installed tool version by absolute path, the declared bindings, the item 1 and 2 observations) and the text's `## Anchor` names that list; implementation: written by the orchestrator before the next C-80 of this text, the block replaced by its output, no hand-written Checks line; verification: the fourth C-80 reviews the generated block; a fifth refusal of this class stops the lineage for the operator's judgement.
counters (`scripts/regime-counters.sh dotfiles-T133-gh-binding-a02`, 01:52Z): task=dotfiles-T133-gh-binding-a02 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=none..none (-) source=live / detail: pr=none authors=- tasks=- results=- questions=- withdrawn=- bot_heads=- source=live
- 2026-10-22T01:47Z (host clock, `date -u`): the times typed in this record's 2026-10-22 lines before this one were the orchestrator's estimates and run 7 to 27 minutes ahead of the writes (the project-map agent compared them with file mtimes); the bus rows and file mtimes are authoritative, and every later line takes its time from `date -u`.
- 2026-10-22T02:25Z: operator answered J-G (recommended default): the Checks block is generated by `.agents/worklog/orchestrator-glue/checks-paste.sh` (absolute executables, one enumerated environment, digests of every executable, no prose; proxy values and the user name masked) and pasted in place of the hand-written block; pre-send OK at sha b700fe8bfddc561e6fb548485dd965066285ddeb0bd884ee1a5aef5e8bd0c709 (139 lines); C-80 round 4 of this lineage running on these bytes; anchor round 2 (a011) follows a correct verdict.
- 2026-10-22T02:33Z: C-80 round 4 (b700fe8, the first generated block) `Verdict: incorrect`: P1 the generator forwarded the inherited GIT_CONFIG_PARAMETERS under the label "proxy auth method only" (a git config vector); P2 the canonical stages were abbreviated. Generator rewritten: no inherited git configuration (the proxy auth method travels as explicit `-c http.proxyAuthMethod=basic` and the proxy host credential helper as `-c credential.http://localhost:<port>.helper=`), a full bare clone with GIT_NO_LAZY_FETCH=1 (a blobless clone made `git show` fetch lazily and the digest came out as the empty-input sha, caught before the paste), every stage printed as its full command with its exit status, every proxy occurrence masked (the single-occurrence sed had left a second copy unmasked in one line, also caught before the paste). Regenerated block: canonical main 7b21659e (main moved with the #442 merge), design digest a027b021…, 4 stages exit 0, scan clean; pre-send OK at sha 63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a (143 lines); C-80 round 5 of this lineage running on these bytes (the second since the re-plan line; the re-plan's own stop is the next refusal of the class).
text-security:63d69cc:0	correct
anchor:a011:r2:1	checks-paste-provenance
anchor:a011:r2:2	advisory-p3-exit-status
- 2026-10-22T02:35Z: C-80 round 5 of the lineage (63d69cc0, the corrected generated block) `Verdict: correct`; anchor round 2 sent to a011 (amendment 1 of the review task, design sha 63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a; bus row after 2026-10-22T02:35Z, hand line).
- 2026-10-22T02:55Z: anchor round 2 (a011, RESULT 3045 at 02:37:14Z) `verdict=reject`: the generated block's closing "executables:" line held values without their commands (shasum, git --version, codesign); P3 advisory: only the canonical lines printed an exit status; observation: the mise pin was read from the working file, not the clone. This is the fifth refusal of class checks-paste-provenance (rows text-security:0ecdc07:1-2, anchor:a011:r1:1-2, text-security:b700fe8:1, anchor:a011:r2:1): the re-plan line's stop applies and the lineage waits for the operator. Prepared meanwhile, no review run: the generator prints every host line through one `stage` (command, output, exit status), the executable digests as one `shasum` command, `git --version` and `codesign -dv` as commands, the mise pin from the private clone (`git show refs/heads/main:home/dot_mise/config.toml | sed -n 43p`); the text names the Codex seat's report route (`send.sh … --body-file`, Playbook step 6; the gap the map agent found at line 109, the same as slice1's); regenerated block 21 lines (canonical main 7b21659e, design digest a027b021…, 19 lines with exit status: 18 exit 0 and the trusted_tools grep exit 1 = 0 matches), pre-send OK at sha 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 (145 lines). Default put to the operator: C-80 round 6 on these bytes, then anchor round 3, then dispatch to a012 (seated at wW:p7 at 02:49Z, linkage pending).
text-security:3c1d54a:0	correct
- 2026-10-22T02:59Z: C-80 round 6 of the lineage (3c1d54a9, the fully generated block plus the Codex route sentence) `Verdict: correct`; the operator's "推奨案で実施" covered the run after the fifth refusal (the structural cause, a hand-written line, was removed from the generator); anchor round 3 sent to a011 (design sha 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9; hand line).
anchor:a011:r3:0	accept
anchor:a011:r3:1	advisory-p3-exit-status
- 2026-10-22T03:01Z: anchor round 3 (a011, RESULT at 03:00:34Z) accept at 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9, findings 0, P3 advisory (the design-digest and mise-pin pipeline lines carry no exit status; recorded, no change: the anchored bytes stay frozen, as does the informational front-matter field dispatch_status: blocked-pre-anchor, which the checker does not read). counters before the dispatch (`scripts/regime-counters.sh dotfiles-T133-gh-binding-a02`, 2026-10-22T03:01Z): task=dotfiles-T133-gh-binding-a02 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=none..none (-) source=live. Dispatch to codex-standard-dot-a012 (worker-g, wW:p7, alive 02:53Z) follows as round 1; overlap_ok lists the 16 open PRs whose files fall under the task's globs (none in flight as a worker task; #378 held; #454 shares no file).
dispatch: [2026-10-22T03:02Z] claude-deep-dot → codex-standard-dot-a012: AGMSG-TASK v1 task_id=dotfiles-T133-gh-binding-a02 round=1 task_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 (bus row at 03:0xZ; hand line, see the history row for the read marker)
- 2026-10-22T03:37Z: a012 PONG status=blocked (03:05:50Z): `git switch -c tools/gh-binding-a02 --no-track origin/main` exited 0 and created the branch (verified: worker-g HEAD), then printed two `Unable to create .git/packed-refs.lock: Operation not permitted` lines; the shared common dir is read-only for Codex seats by design (T64), so this is the boundary working as designed, not a defect; a probe from the orchestrator checkout shows branch creation touching no packed-refs lock there (the Claude sandbox denies .git/config.lock instead, also with exit 0), so the trigger is seat-specific and the amendment names the class, not a cause. Amendment 1 (previous_sha256 3c1d54a9…): an exit-0 denial on .git/packed-refs.lock or .git/config.lock is measured state recorded in sandbox.md; every other denial stays blocked; pre-send OK at sha 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 (148 lines); C-80 running; anchor round 4 (a011) follows; hold ACCEPTANCE sent to a012 (hand line).
text-security:2adb147:0	correct
- 2026-10-22T03:38Z: C-80 of amendment 1 (2adb1477) `Verdict: correct`; anchor round 4 sent to a011 (hand line).
anchor:a011:r4:0	accept
- 2026-10-22T03:40Z: anchor round 4 (a011, 03:39:52Z) accept at 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7, findings 0 (diff against the round-3 bytes: previous_sha256 and the Amendment 1 paragraph only; the exception is design 5.14 item 1 working as designed). a012 acknowledged the hold (PONG 03:38:52Z, branch preserved). counters before the send (`scripts/regime-counters.sh dotfiles-T133-gh-binding-a02`, 2026-10-22T03:40Z): task=dotfiles-T133-gh-binding-a02 tasks=1 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-22T03:02:12Z..none (-) source=live. ACCEPTANCE status=revise round=1 amendment=1 sent to a012 with task_sha256 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 (hand line).
- 2026-10-22T04:27Z: a012 PONG status=question (04:25:02Z; INV-6 questions=1): the gate executes the authenticated base's collector (require-crit-review.py:608-615), whose bytes at 7b21659e call bare gh without --hostname, and the selected bytes must stay unchanged; may the gate refuse such a collector until a02 is on main, or is an older-base contract authorized? Answer sent as a PING at 2026-10-22T04:27Z (no rule sentence changes; the text's item-4 constants rule applies): never refuse the base collector; supply the executable through item 2's private PATH link gh -> the declared path, the host as the explicit constant GH_HOST=github.com (gh help environment: '`GH_HOST`: specify the GitHub hostname for commands where a hostname has not been provided, or cannot be inferred from the context of a local Git repository. If this host was previously '), the repository by the --repo argument the gate already passes; drop ambient GH_HOST/GH_REPO/GH_CONFIG_DIR first; one fixture (older selected collector + decoy gh + planted ambient GH_HOST); after the merge the constants stay as defence in depth. The worker meanwhile fixes its independent-review findings (equality, token-free discovery, manifest ambiguity).
- 2026-10-22T04:45Z: a012 PONG status=question (04:44:30Z; INV-6 questions=2, S2's questions count reached: judged at the next acceptance action): before its HTTPS push, PR and CI it asked for the measured items 2/9 parent namespace and deployed gh/config evidence, or an authorized transport route. Answer sent as a PING at 2026-10-22T04:45Z (no rule sentence changes): the push, PR creation and CI are Worker Playbook step 2/4 operations from inside the Codex sandbox (T64 network_access, HTTPS push without -u, gh pr create --draft), which is the authorized transport (design 5.14 item 10); row 38's 'authenticated use is blocked' scopes the consumers this task binds (the orchestrator's acceptance-time reads and the gate's collector), not the worker's transport; no parent measurement precedes the push. Both questions of this lineage come from the same over-reach of the residual rows into the worker's own transport; the rows are the design's residuals and stay as written.
- 2026-10-22T05:04Z: a012 PONG status=blocked (05:00:20Z) and RESULT status=blocked (05:02:46Z): PR #456 opened as a draft at 2804b176 (source 321/350, tests 698/700, baseline red 16 tests, implementation green 166, portable routes 14); the block is gh's run-log cache write under ~/.cache/gh denied by the Codex writable roots while reading the regime job log, held per the boundary rule. Answer sent as a PING at 2026-10-22T05:04Z: XDG_CACHE_HOME as an explicit constant of the env -i contract (gh honours it; item 4's nonsecret constants) to a private directory, re-run inside the sandbox; the regime failure is the D-024-64 class, not a hold; finish ready/CI/Bot/RESULT; the orchestrator copies the worktree artifacts at the ready RESULT.
- 2026-10-22T05:08Z: a012 resumed (PONG 05:05:07Z, transport cache under its private TMPDIR, gh pr ready next); the blocked RESULT is answered on the bus by an ACCEPTANCE status=revise round=1 text=unchanged (continuation, no new check=); CI at 2804b176: regime red (known class) and test (ubuntu-26.04, client) red, to be fixed within round 1.
- 2026-10-22T05:15Z: a012 PONG status=question (05:14:24Z; INV-6 questions=3): CI on 2804b176 fails in the fixtures of three legacy test modules that exercise the bound scripts and are outside Item 6's four modules. Orchestrator text defect (the task-file review's touch-point grep covered gh calls, not the tests that exercise the changed scripts): amendment 2 authorizes the five legacy modules for fixture adoption only (the three named plus test_validate_agent_assets.py and test_agmsg_orchestration_docs.py, found by grep on main), test cap 1000; pre-send OK at 86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c; C-80 and anchor next; answer PING sent. S2 note: questions=3 and amendments=2 after this; both counts are judged at the acceptance action with this explanation.
search: touch-point-coverage -> none
re-plan: touch-point-coverage (rows: the a02 text's Item 6 listed four test modules while five legacy modules exercise the scripts the task binds, found by CI at 2804b176 and by grep on main; the task-file review's item 4 enumerated gh call sites only) — specification: a task's allowed test set is every test module that references a changed script or module by name (grep over tests/unit for each basename in allowed_files), stated in the text before dispatch, never discovered by CI; design: the task-file review's item 4 names that enumeration explicitly, and pre-send gains the same check as a mechanism (owner: dotfiles-T133-pre-send-check-followup-a01: refuse a text whose test allowance omits a module that references a changed script); implementation: amendment 2 of this text widens Item 6 to the nine modules with fixture-adoption-only for the five legacy ones and raises the test cap to 1000; verification: CI of the next head green on the five modules, the anchor review item 4 run with the enumeration, and no further test-scope amendment on this lineage.
text-security:86513b2:0	correct
- 2026-10-22T05:19Z: C-80 of amendment 2 (86513b29) `Verdict: correct` after the touch-point-coverage re-plan line (C-92); anchor round 5 sent to a011 (hand line).
anchor:a011:r5:1	touch-point-coverage
- 2026-10-22T05:23Z: anchor round 5 (a011, 05:22:14Z) reject on item 4: scripts/lint-comparisons-baseline.tsv is a touch point (a stale row for orch-gate.sh R1 fails the lint on a changed file; new R1/R4 hits in orch-gate.sh and pr-feedback.py are fixed in the sources); P3 wording (row 29 four modules; Item 6 versus Item 0). Amendment 3: the baseline joins allowed_files for stale-row removal only with a closed threat row, wording fixed; pre-send OK at 728f0ffe540d8eddc2261eeb89de3cdf11066a9660e900f9527c2f8833421eca; C-80 then anchor round 6; the touch-point-coverage class gains its second row (the task-file review's grep must also cover the lint baseline for every changed script).
text-security:728f0ff:1	selector-existence
- 2026-10-22T05:26Z: C-80 of amendment 3 (728f0ffe) incorrect on one P2: the baseline row named a test that does not exist; the row now closes through the existing LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline; pre-send OK at e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1; C-80 again (the third since the touch-point-coverage re-plan line).
text-security:e9ce1c3:0	correct
- 2026-10-22T05:29Z: C-80 of amendment 3 with the existing selector (e9ce1c3b) `Verdict: correct`; anchor round 6 sent to a011; on accept, amendments 2 and 3 go to a012 as one ACCEPTANCE revise (task_sha256 e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1) (hand line).
anchor:a011:r6:0	accept
- 2026-10-22T05:32Z: anchor round 6 (a011) accept at e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1; counters before the send (`scripts/regime-counters.sh dotfiles-T133-gh-binding-a02`, 2026-10-22T05:32Z): task=dotfiles-T133-gh-binding-a02 tasks=1 amendments=0 questions=3 results=1 withdrawn=0 revises=0 first_result_head=2804b176adc394109dd1f7df86e23cdb87f6b2f5 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-22T03:02:12Z..2026-1 / S2: questions 3 >= 2 source=live; ACCEPTANCE status=revise round=1 amendment=3 (amendments 2 and 3) sent to a012 with task_sha256 e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 (hand line). Counter note: the lineage shows questions=3 and the bus revise rows of the two continuation lines; the first amendment and both continuations were orchestrator-side corrections or confirmations, not worker rounds, which the acceptance record states when S2 is read.
---
{
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02-review-a01.md task_sha256=0b954cc99b76901d0c79119bffdbb078ec0bb718906338de809287352019a302 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=c0a7dae7d7e10974669ebd2e21b79907a5b5c5e84016d308b9d4fa8bce73c3df allowed_files=see-task-file forbidden_actions=edit;dispatch;network-write expected_result_file=.orchestration/dotfiles-T133-gh-binding-a02-review-a01/review.md done_signal=AGMSG-RESULT max_turns=20 note=anchor-review-of-the-gh-binding-a02-text(reset-of-a01;C-80-correct-at-c0a7dae7-after-the-bound-Checks-paste);read-only;reply-by-agmsg-dispatch-to-wW:p1 read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=2 amendment=1 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a previous_design_sha256=c0a7dae7d7e10974669ebd2e21b79907a5b5c5e84016d308b9d4fa8bce73c3df reason=your-round-1-findings-answered:the-Checks-block-is-now-generated-by-.agents/worklog/orchestrator-glue/checks-paste.sh(every-line-a-full-command-under-one-enumerated-environment-with-its-exit-status,absolute-executables-with-digests,no-prose,no-inherited-git-configuration);line-128's-cache-sentence-removed,item-9-stays-the-source-in-the-body;canonical-main-is-7b21659e-after-the-#442-merge;C-80-Verdict-correct-at-this-sha(…-text-security-63d69cc.md.last.md) next_action=review-round-2:compute-the-hash,judge-items-1-7-of-your-task(item-3-now-reads:every-Checks-line-is-a-command-and-its-output),RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=hold round=2 pr=none verdict=reject reason=RESULT-3045-received(reject:the-executables-line-held-values-without-commands;P3-exit-status-advisory);fixed-in-the-generator-and-regenerated-at-sha-3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9;fifth-refusal-of-class-checks-paste-provenance:the-lineage-waits-for-the-operator-before-C-80-round-6-and-your-round-3 next_action=hold:no-worker-action-until-the-round-3-ACCEPTANCE read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=3 amendment=2 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 previous_design_sha256=63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a reason=your-round-2-finding-answered:every-Checks-line-is-now-one-command-with-its-output-and-exit-status(the-executable-digests-are-one-shasum-command,git---version-and-codesign--dv-are-commands,the-mise-pin-is-read-from-the-private-clone);line-109-names-the-Codex-seat's-report-route(send.sh---body-file,Playbook-step-6);C-80-Verdict-correct-at-this-sha(…-text-security-3c1d54a.md.last.md) next_action=review-round-3:compute-the-hash,judge-items-1-7,RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=accepted round=3 pr=none verdict=accept design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 reason=round-3-accept,findings=0(P3-advisory:two-pipeline-lines-without-exit,recorded);the-gh-binding-a02-TASK-goes-to-a012-on-these-bytes next_action=none:the-seat-is-free read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=4 amendment=3 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 previous_design_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 reason=amendment-1-of-the-design-text-after-the-seat's-first-command:an-exit-0-Operation-not-permitted-on-.git/packed-refs.lock-or-.git/config.lock(the-T64-read-only-common-dir)-is-measured-state-recorded-in-sandbox.md,every-other-denial-stays-blocked;previous_sha256-added-to-the-front-matter;Checks-block-unchanged;C-80-Verdict-correct-at-this-sha(…-text-security-2adb147.md.last.md) next_action=review-round-4:compute-the-hash,judge-items-1-7(item-2:the-amendment-contradicts-no-design-item;item-5:no-threat-row-changes),RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=accepted round=4 pr=none verdict=accept design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 reason=round-4-accept,findings=0;amendment-1-goes-to-a012-as-an-ACCEPTANCE-revise next_action=none:the-seat-is-free read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=5 amendment=4 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c previous_design_sha256=2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 reason=amendment-2-of-the-design-text:Item-6-authorizes-test_orch_gate_path.py,test_orchestrator_tools.py,test_chain_review_scripts.py,test_validate_agent_assets.py-and-test_agmsg_orchestration_docs.py-for-fixture-adoption-only(CI-at-2804b176-failed-in-their-fixtures;found-by-grep-on-main:they-exercise-the-bound-scripts),test-cap-1000,source-cap-350,one-report-line-per-legacy-module;Checks-and-threat-rows-unchanged-except-the-test-row-wording;C-80-Verdict-correct-at-this-sha(…-text-security-86513b2.md.last.md) next_action=review-round-5:compute-the-hash,judge-items-1-7(item-4:the-touch-point-grep-now-covers-the-test-modules-that-reference-each-changed-script),RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=hold round=5 pr=none verdict=reject reason=round-5-RESULT-received(item-4:scripts/lint-comparisons-baseline.tsv-is-a-touch-point;P3-wording);amendment-3-written-at-728f0ffe(baseline-for-stale-row-removal-only-with-a-closed-row,wording)-and-in-C-80;round-6-follows-a-correct-verdict next_action=hold:no-worker-action-until-the-round-6-ACCEPTANCE read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=6 amendment=5 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 previous_design_sha256=86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c reason=amendment-3-of-the-design-text-answers-your-round-5:scripts/lint-comparisons-baseline.tsv-joins-allowed_files-for-stale-row-removal-only-with-a-row-closed-by-the-existing-LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline(new-R1/R4-hits-are-fixed-in-the-sources);row-29-says-nine-modules;the-authorization-sentence-is-Item-0's;C-80-Verdict-correct-at-this-sha(…-text-security-e9ce1c3.md.last.md) next_action=review-round-6:compute-the-hash,judge-items-1-7(item-4:the-touch-point-grep-covers-tests-and-the-lint-baseline-for-every-changed-script),RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=accepted round=6 pr=none verdict=accept design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 reason=amendments-2-and-3-accepted-at-round-6;they-go-to-a012-as-one-ACCEPTANCE-revise next_action=none:the-seat-is-free read_at=read"
  ]
}
---
# Acceptance: dotfiles-T133-gh-binding-a02-review-a01

Anchor review of the gh-binding a02 text (reset of a01 under S-R5; D-024-69). Design file `.orchestration/tasks/dotfiles-T133-gh-binding-a02.md` at `c0a7dae7d7e10974669ebd2e21b79907a5b5c5e84016d308b9d4fa8bce73c3df` (C-80 rounds: c761dc8 correct unpopulated; 0ecdc07 incorrect, two P1 on the unbound canonical measurement; c0a7dae correct after the bound-executable re-measurement). Review seat a011 (worker-d, wW:p4).

## Counters (INV-6)

amendments=0 revises=0 questions=0 at dispatch.
- 2026-10-22T01:24Z: round 1 RESULT (a011) `verdict=reject`, findings=2 (Checks line 128 against design 5.14 item 9; lines 127-130 claims without commands); both fixed in the text at 5d62e48e; round 2 waits for the C-92 re-plan of the a02 lineage and its next C-80.
dispatch: [2026-10-22T01:29:09Z] claude-deep-dot → claude-standard-dot-a011: AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=hold round=1 (bus row ○ read; recorded by hand because the dispatch.sh run that sent it was stopped during its slow post-send bus read)
- 2026-10-22T02:35Z: round 2 (amendment 1) sent: design sha 63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a after C-80 correct (hand line).
- 2026-10-22T02:56Z: round 2 RESULT (a011) reject (executables line without commands; P3 exit status); hold sent; round 3 after the operator's answer on the lineage stop (hand line).
- 2026-10-22T02:59Z: round 3 (amendment 2) sent: design sha 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 after C-80 correct (hand line).
- 2026-10-22T03:01Z: round 3 RESULT (a011) accept at 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9, findings 0, advisory P3 (two pipeline lines print no exit); ACCEPTANCE accepted sent (hand line).
- 2026-10-22T03:38Z: round 4 (amendment 3 of this review task = amendment 1 of the design text) sent at design sha 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 (hand line).
- 2026-10-22T03:40Z: round 4 RESULT (a011) accept at 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7, findings 0; ACCEPTANCE accepted sent (hand line).
- 2026-10-22T05:19Z: round 5 (amendment 2 of the design text) sent at design sha 86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c (hand line).
- 2026-10-22T05:25Z: round 5 RESULT (a011) reject (item 4: the lint baseline; P3 wording); hold sent; round 6 after the C-80 of amendment 3 (hand line).
- 2026-10-22T05:29Z: round 6 (amendment 3 of the design text) sent at design sha e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 (hand line).
- 2026-10-22T05:32Z: round 6 RESULT (a011, 05:30:44Z) accept at e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1; ACCEPTANCE accepted sent (hand line).
---
format: 2
task_id: dotfiles-T133-gh-binding-a02
kind: code
security: true
previous_sha256: 728f0ffe540d8eddc2261eeb89de3cdf11066a9660e900f9527c2f8833421eca
dispatch_status: blocked-pre-anchor
design_review: {design: .orchestration/plans/024-design-quality.md}
requires_decision: [D-024-69]
after: []
allowed_files:
  - home/dot_mise/config.toml
  - home/dot_agents/agent-config.yaml
  - scripts/validate-agent-assets.py
  - scripts/orchestrator/*.sh
  - scripts/require-crit-review.py
  - scripts/pr-feedback.py
  - tests/unit/test_*.py
  - scripts/lint-comparisons-baseline.tsv
  - .orchestration/dotfiles-T133-gh-binding-a02/**
threat_table:
  - {control: "home/dot_mise/config.toml", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_exact_pin"}
  - {control: "home/dot_agents/agent-config.yaml", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
  - {control: "scripts/validate-agent-assets.py", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_chain_integrate_authenticated_decoy"}
  - {control: "scripts/orchestrator/orch-gate.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_orch_gate_authenticated_decoy"}
  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_local_review_authenticated_decoy"}
  - {control: "scripts/require-crit-review.py", disposition: "closed: tests/unit/test_require_crit_review.py::GhBindingTest::test_gate_hostile_repository"}
  - {control: "scripts/pr-feedback.py", disposition: "closed: tests/unit/test_pr_feedback.py::GhBindingTest::test_collector_hostile_repository"}
  - {control: "tests/unit/test_*.py", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence-integrity automation; independently inspect the four authorized modules and their behavioral red/green logs."}
  - {control: "scripts/lint-comparisons-baseline.tsv (amendment 3: stale-row removal only; no row is added, every new R1/R4 hit is fixed in the allowed sources)", disposition: "closed: tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline (the existing lint test, run by make unit-test on the final head; it fails on a stale row of a changed file and on an unbaselined hit)"}
  - {control: ".orchestration/dotfiles-T133-gh-binding-a02/** including task.md", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence automation; compare anchored bytes, task-copy digest and literal full head against the independently audited PR."}
  - {control: "pin", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_exact_pin"}
  - {control: "declaration", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
  - {control: "consumer binding", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_consumer_binding_matrix"}
  - {control: "minimal environment", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_gh_environment_is_minimal"}
  - {control: "gh configuration inputs", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_protected_gh_configuration"}
  - {control: "fixed repository and host in gate descendants", disposition: "closed: tests/unit/test_require_crit_review.py::GhBindingTest::test_gate_hostile_repository"}
  - {control: "collector interpreter startup", disposition: "closed: tests/unit/test_require_crit_review.py::GhBindingTest::test_collector_ignores_startup_hooks"}
  - {control: "trusted parent before first instruction", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns automatic parent binding; authenticated use is blocked until the orchestrator measures design 5.14 items 2/9 for every non-gh process in the route."}
  - {control: "task metadata", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns dispatch automation; compare the reviewed inventory and populated Checks with the complete anchored task before dispatch."}
  - {control: "metadata separators", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns byte-integrity automation; compare front matter, separators and Checks, with no paste after anchor."}
  - {control: "in-process effects", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_git_environment_cannot_redirect_fixture_writes"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns uv/Python/Node, permgate and launcher binding; unchanged resolvers require the measured design 5.14 items 2/9 parent, otherwise authenticated use is blocked."}
  - {control: "new or renamed scripts; future gh routes", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns absent chain-finish and future checker adoption; add no consumer here and require their own positive authenticated fixtures."}
  - {control: "remaining git/date/mise executable provenance", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns remaining-tool binding; retain today's resolver algorithms only under the measured parent, with token-free discovery."}
  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns integration follow-through; only the orchestrator integrates the exact audited head through Playbook step 10."}
  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence refresh; repeat CI, feedback, audit, acceptance and gate for each changed head."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns teardown records; none is planned and dirty state requires separate authorization before discard."}
  - {control: "orchestrator effect owner-stub amendment", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns all assigned residuals; the orchestrator creates or expands its owner stub before anchor, outside worker scope."}
  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns measurement automation; gh-free private-clone and trusted-parent evidence precedes review of the complete populated bytes."}
  - {control: "orchestrator effect installation and deployment", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns deployment verification; observe the pinned install, protected configuration and positive real consumer probes before enabling acceptance reads."}
  - {control: "design 5.14 item 0", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns unchanged item 0 obligations; this task establishes no same-UID or credential-separation boundary."}
  - {control: "design 5.14 item 1", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns host protection evidence; item 1 must cover declaration, binary, configuration source and parent namespace before authenticated use."}
  - {control: "design 5.14 item 2", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns permanent item 2 integration; measured parent evidence is mandatory now."}
  - {control: "design 5.14 item 3", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns wider item 3 integration; apply it to gh inputs without certifying other runtime boundaries."}
  - {control: "design 5.14 item 4", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns wider item 4 integration; consume checked gh directly, with replacement risk retained under item 0."}
  - {control: "design 5.14 item 5", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns unchanged item 5 obligations; retain full head identities and change no locks or reservations."}
  - {control: "design 5.14 item 6", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns deployment verification; distinguish fixture success, CI and observed host execution."}
  - {control: "design 5.14 item 7", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns wider coverage; inspect behavioral assertions and never count setup failure or absent routes as closure."}
  - {control: "design 5.14 item 8", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns future canonical-reader adoption; bind active gh routes without certifying local-object checkers."}
  - {control: "design 5.14 item 9", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns permanent item 9 integration; measured isolated runtimes and absolute UV_CACHE_DIR remain mandatory."}
  - {control: "design 5.14 item 10", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns denial records; apply item 10 and stop with a blocked PONG on any denial."}
premises: []
---

# AGMSG-TASK dotfiles-T133-gh-binding-a02 — bind gh and its gate descendants

D-024-69 advances this remedy ahead of slices 2-5. This S-R5 reset supersedes the 2026-10-21 owner stub and a01 round-2 text; TASK names Codex worker a012. pins-a01 merged as #449; after is empty and later binding adds sibling declarations.
Seven C-80 refusals share the unbound-gh P1: a07-checker 922292d/0edbd8c/fd8c003/c6cebe4/a3125e1; regime-ci-followup-a02 a232baf/a18a67d. A substitute can forge main, design, merge state and PR data and read forwarded credentials.
a01 rounds 3bf2a79 (3 P1, 3 P2) and 6486b79 (1 P1, 1 P2) are superseded; Items 6/7 authorize and test the refused descendant changes while retaining the other round-2 requirements.
Design 5.14 items 0-10 apply by reference, particularly 2-4/8/9; this text does not redefine that contract.

## Items

0. Inventory: local HEAD/origin/main observed at 7da0cdfab9de9fbea673b82379acd4e317115065; chain-finish.sh is absent and regime-ci.py/task-consistency-check.py currently use Git, not gh. These are local observations, pending gh-free canonical confirmation before C-80/anchor.
   Implement the three present shell routes and their real gate/collector descendants. Do not invent chain-finish or add canonical-network behavior to the checkers; dotfiles-T133-gh-binding-followup-a01 owns all three future routes and their positive authenticated decoy fixtures.
   The shell wildcard authorizes only chain-integrate.sh, orch-gate.sh and local-review.sh; the test wildcard authorizes test_supply_chain_policy.py, test_chain_glue.py, test_require_crit_review.py and test_pr_feedback.py for new fixtures, and, for fixture adoption only (a fixture adopts the bound gh and the declaration; no assertion is weakened, deleted or re-targeted), test_orch_gate_path.py, test_orchestrator_tools.py, test_chain_review_scripts.py, test_validate_agent_assets.py and test_agmsg_orchestration_docs.py, the modules that exercise the scripts this task changes (amendment 2). If canonical inventory differs, reauthor/review the whole inventory and threat table before dispatch.
1. Pin `"github:cli/cli" = "2.102.0"` in home/dot_mise/config.toml with one adjacent English reason comment following pins-a01; retain unrelated pins. Installed target: `~/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh`.
2. Declare trusted_tools.gh with version "2.102.0" and that home-relative absolute target in agent-config.yaml; later uv/Python/Node entries are siblings.
   validate-agent-assets.py checks pin equality, normalized home-anchored spelling, absolute expansion under the real user's home, and no shims component in spelling or resolved path. Refuse missing/malformed declarations, traversal, forged HOME and mismatched identities; give every rule a separate refusal subtest.
   Runtime reads protected deployed ~/.agents/agent-config.yaml as data with existing parsing facilities under design 5.14 items 2/9, never source/eval or a worker/PR copy. Chezmoi deploys this plain source; create no rendered artifact and leave generator/rendering tests unchanged.
3. Replace gh discovery in chain-integrate.sh/orch-gate.sh; bind local-review.sh's descendant namespace and both authorized Python consumers to the declaration. No PATH, mise-which, latest, wrapper or caller-selected executable override may supply gh.
   Require the version-specific absolute realpath, regular executable, existence, non-shim/trusted-root checks and matching reported version; consume that checked target under design 5.14 items 3/4. Missing/mismatching identity emits exactly `refused: gh binding`, exits nonzero and performs no canonical operation or fallback.
   Every repository REST read names literal repos/mryfmo/dotfiles endpoints and --hostname github.com; GraphQL fixes owner=mryfmo/name=dotfiles and accepts node IDs only from those bound queries. gh pr uses --repo github.com/mryfmo/dotfiles, never unsupported --hostname; account/auth probes bind the host and version probes make no network call.
   Preserve today's uv/git/date/mise and other non-gh resolver algorithms only within the orchestrator's measured design 5.14 items 2/9 parent/namespace, established before the first credential-bearing process. Discovery is token-free; without that evidence authenticated operation remains blocked.
4. Construct minimal environments for every bound gh, including token-free identity probes; use protected GH_CONFIG_DIR=/var/empty, verify the resolved directory and ancestors are protected and the directory itself is empty with no symlink/config payloads, and refuse unsafe/missing configuration without creation or fallback.
   Normalize only the call's explicitly supplied token to GH_TOKEN; no implicit home/keychain credentials. Supply trusted HOME/PATH, absolute UV_CACHE_DIR, fixed configuration, disabled prompts/update notices and plain output explicitly; record allowed names without values. Every env -i contract includes UV_CACHE_DIR.
   Exclude ambient GH_HOST/GH_REPO/GH_CONFIG_DIR/XDG_CONFIG_HOME, proxies, loader/startup variables and Git overrides. Test planted home/XDG config with http_unix_socket, aliases and alternate hosts, unsafe-config refusal and a positive controlled authenticated operation.
5. No workflow/regime.yml, launcher, permission, dependency, unrelated resolver-algorithm or acceptance-semantic change; regime-ci-followup-a02 owns the workflow. Add/rename no executable and keep evidence non-executable; other runtime binding remains dotfiles-T133-trusted-entrypoint-binding-a01's scope.
6. Edit scripts/require-crit-review.py and scripts/pr-feedback.py: the gate's pr_base_errors must use the bound gh and --repo github.com/mryfmo/dotfiles, never discover authority from local Git context after removing GH_REPO. The collector uses the same declared target and host/repository binding for REST, GraphQL and auth calls.
   Reject conflicting CLI/evidence repositories; hostile remote, GH_REPO and GH_HOST cannot redirect authority. Preserve authenticated-base collector selection and all feedback checks; never execute a PR collector in place of that selected source.
   Test the real gate path through PR view and collector launch, and separately the real collector, with a foreign remote plus hostile GH_REPO/GH_HOST. Require successful fixed-host/repository responses, consumed results and observed descendant argv/environment; mocking subprocess launch or pre-sanitizing away the attack does not close the row.
7. Replace the gate's bare sys.executable collector launch with the gate's measured absolute Python plus -I and design 5.14 item 9's constructed environment, including absolute UV_CACHE_DIR. PYTHONSAFEPATH alone is insufficient; preserve the selected collector bytes and subprocess failure propagation.
   A real-descendant test launches the gate and its selected real collector with planted user-site .pth/sitecustomize.py/usercustomize.py and PYTHONSTARTUP markers; prove the same hook can execute without isolation, then assert no marker and a successful collected response with production isolation.

## Check

The final diff has at most 350 changed lines outside `tests/` and `.orchestration/`, and at most 1000 under `tests/` (amendment 2: the fixture adoption in the five legacy modules).
Measure with `git diff --numstat <merge-base40> <head40>`.
Caps are PR-wide additions plus deletions from git merge-base <authenticated-main40> <head40> (C-123), never round deltas; record dispatch measurement_base40, final main/head/merge-base SHAs, every numstat row and both totals, and recount after update-branch. Expected width is about 200/400; 350/700 includes fixtures and one Bot fix round, with no exemption from a07's 446/709 rewrite.
Write fixtures first and implement every closed selector. Each active shell route and both Python consumers needs a positive authenticated operation, synthetic credential, fixed host/repository and consumed response through declared gh; separately test missing/version/path refusals. Matrices cover all five consumers, including review/gate descendants; absent checkers/chain-finish are not passing entries.
Plant executable PATH gh and hostile mise answers without prebinding gh in the trusted-parent fixture; assert neither executes nor receives the synthetic credential. Minimal-environment/configuration matrices observe every consumer's actual child environment.
Reuse trusted_exec_contract.py without modification. Before fixture Git init/add/commit/reset/fetch, construct fresh environments and explicit roots, never os.environ merges; test hostile GIT_DIR/GIT_WORK_TREE/GIT_CONFIG_* and local includes/hooks, preserving a second repository's refs/index/bytes and external markers.
For each behavioral requirement in Items 1-4/6/7, record red at origin/main production bytes and green at the fix commit: selector, full baseline/red-fixture/fix SHAs, exact commands, stdout/stderr and real status. Red reaches the intended assertion, never missing API/import/setup/tool failure. Items 0/5 use inventory/diff evidence; no fabricated red or closure for future consumers.
Run `uv run python -m unittest tests.unit.test_supply_chain_policy tests.unit.test_chain_glue tests.unit.test_require_crit_review tests.unit.test_pr_feedback -v` through measured absolute uv/Python with item 9 isolation and temporary absolute UV_CACHE_DIR; record the expanded invocation.
Run bash -n, shellcheck and shfmt --indent 4 --space-redirects --diff on the three changed shells; ruff check --config ruff.toml and ruff format --check --config ruff.toml on changed Python; make validate-agent-assets and the review gate. Never run Bats locally.
Resolve observations with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" UV_CACHE_DIR="$UV_CACHE_DIR" "$HOME/.local/bin/mise" which uv`, repeat for python, and paste actual outputs; uv's installed path has no assumed bin component. Discovery is not trusted-parent deployment evidence.

## Execution and evidence

Worker Playbook step 4 applies: every command sandboxed; any denial sends AGMSG-PONG v1 task_id=dotfiles-T133-gh-binding-a02 status=blocked with exact command, exit status and boundary, then holds. Never escalate, probe Herdr sockets or retry through another surface. The named report route of this Codex seat is the pane-less path of Orchestrator Playbook step 6: write each PONG and the RESULT as one line to a file under `.orchestration/dotfiles-T133-gh-binding-a02/` and send it from sandboxed Bash with `~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-standard-dot-a012 claude-deep-dot --body-file <that file>` (the Codex sandbox denies the Herdr socket, D-024-73, so `agmsg-dispatch` is not a route for this seat); the orchestrator reads the bus at each milestone. This route is the named route, not "another surface".
Create fresh branch with `git switch -c tools/gh-binding-a02 --no-track origin/main`; push `git push https://github.com/mryfmo/dotfiles.git tools/gh-binding-a02`, never -u or shared-config changes; open one draft PR. Follow step 15's ready/CI/Bot wait, with at most one worker Bot fix round; surviving P0/P1 stops for the operator. Worker never merges.
Under .orchestration/dotfiles-T133-gh-binding-a02/ write task.md byte-identical to the complete anchored dispatch, report.md, validation.md with verbatim stdout/stderr and real exit statuses, sandbox.md, learning.md, autoskill.md and result.txt; normalize home paths and retain no secrets.
Each evidence item names producer/seat: worker (Codex seat), orchestrator (Claude seat, sandboxed Bash), or author (Codex review-profile seat, sandboxed exec). report.md maps all rows/selectors, scope, counts, red/green pairs and limitations; sandbox.md records denials, learning.md triage, autoskill.md actual use/not-used, and cost is n/a unless measured.
Write AGMSG-RESULT v1 before sending: task_id, status, PR, literal head=<full40>, authenticated_main=<full40>, merge_base=<full40>, measurement_base40, source_cap=350, test_cap=1000, source_changed/test_changed, every red/green SHA pair, task_copy=<repo-local task.md>, task_copy_sha256 and artifact paths. ready_for_review requires passing CI; include Bot findings and dispositions per step 15.
Keep plan/todo/learn updated and uncommitted, one active todo per owner. Use agent-side Crit data/evidence only, no browser/publication; pass make require-crit-review with its receipt before RESULT. The orchestrator alone follows Playbook step 10's feedback, audit, acceptance, gate and integration order.

## Anchor

Authoring is read-only: canonical clone and trusted-parent deployment are unmeasured here; incomplete Checks block anchor/dispatch. Host observations supplied by orchestrator, sandboxed Bash, 2026-10-22 07:5x JST: config.toml:43 declares "github:cli/cli" = "latest"; installed ~/.local/share/mise/installs/github-cli-cli/latest/bin/gh reports 2.102.0 (2026-09-30).
Before C-80/anchor the orchestrator creates/expands dotfiles-T133-gh-binding-followup-a01's owner stub for every assigned residual and three future routes, updates its a02 dependency, and confirms Item 0 against canonical main; all owner-stub edits are outside worker scope.
Obtain main40 and design digest gh-free from a fresh private HTTPS bare clone of https://github.com/mryfmo/dotfiles.git with an independent object store. Record exact sanitized producer commands/outputs and design 5.14 items 1/2/9 protection/parent observations, then paste the five payload lines below before review.
Change dispatch_status only after evidence exists; C-80 reviews and anchors the whole populated text, with no later paste. Inventory differences require reauthoring, not extra files or invented passing fixtures.
Installation/deployment is separate from code/CI: observe the version-specific declared install, protected manifest/config and positive real consumer probes under the measured parent before enabling authenticated acceptance reads. Future checker adoption stays unclosed.
Amendment 1 (`previous_sha256: 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9`): the seat's first command, the branch creation of 2026-10-22T03:05Z, exited 0 and created `tools/gh-binding-a02`, but git printed two `Unable to create .git/packed-refs.lock: Operation not permitted` lines, because the shared common dir is read-only for a Codex seat by design (T64 writable roots: objects, refs, logs and the seat's worktrees entry; the common dir itself, config, hooks, info, HEAD and packed-refs stay read-only). Under this text a denial of exactly that kind, an `Operation not permitted` on `.git/packed-refs.lock` or `.git/config.lock` from a git command whose exit status is 0 and whose stated effect is present, is the boundary working as designed: record the command, its exit status and the stderr lines in sandbox.md as measured state and continue; never retry it outside the sandbox. Every other denial, including one of these paths with a non-zero exit, stays an `AGMSG-PONG v1 status=blocked` and a hold, as line 109 says. The branch created at 03:05Z is kept; the orchestrator verified it as the worktree's HEAD.

Amendment 2 (`previous_sha256: 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7`): CI on 2804b176 (1342 tests, 55 failures, 4 errors) showed that the fixtures of test_orch_gate_path.py, test_orchestrator_tools.py and test_chain_review_scripts.py assume an ambient PATH gh and the old call recorder, because they exercise orch-gate.sh, local-review.sh and the gate this task binds; test_validate_agent_assets.py and test_agmsg_orchestration_docs.py exercise the validator and the scripts' text the same way. Item 0 (the inventory sentence at line 76) therefore authorizes those five modules for fixture adoption only, the test cap becomes 1000 (source cap unchanged at 350), and the worker's RESULT lists, per legacy module, the fixtures adopted and asserts that no assertion changed meaning (one line per module in report.md). Nothing else changes.

Amendment 3 (`previous_sha256: 86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c`): CI at 2804b176 fails `test_lint_comparisons` on new R1/R4 hits (orch-gate.sh:77, pr-feedback.py:77/147/170) and on a stale baseline row (`scripts/orchestrator/orch-gate.sh R1`): the lint exits 1 on a stale row in a changed file. The new hits are fixed in the allowed sources (no baseline row is added); `scripts/lint-comparisons-baseline.tsv` joins allowed_files for stale-row removal only, with its threat row above, closed by the existing `LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline` (no new test in that module). The test-row wording now says nine modules, and amendment 2's authorization sentence is Item 0's inventory sentence (line 76), not Item 6. Nothing else changes.

 succeeded in 308ms:
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
python3: error: couldn't create cache file '/tmp/xcrun_db-PiTX3z9P' (errno=Operation not permitted)
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
python3: error: couldn't create cache file '/tmp/xcrun_db-JZa4fkfY' (errno=Operation not permitted)
dict
{'summary': 'Converges shared AI-agent assets: Claude Code and Codex marketplaces/plugins (Superpowers, Crit, Ponytail, Understand-Anything), gh extensions, pinned Crit/tode/terminal-browser/agmsg releases with checksum verification, the vendored CompactionDB tree, and Herdr integrations.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Resolves the dotfiles repository source root from the wrapper export or the script path, validating the vendored CompactionDB tree.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Prints a section heading.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Returns success when a command is available on PATH.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Removes node-global claude/codex CLIs that would shadow the dedicated mise-managed tools.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Reinstalls a broken mise-managed npm agent CLI (claude or codex).', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs configured GitHub CLI extensions when gh authentication is ready.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': "Returns success when a command's output contains a fixed string.", 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Prints the local root path of a configured Codex plugin marketplace.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': "Returns success when a Git checkout's origin URL matches the expected source.", 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Returns success when a configured Codex marketplace exists with a matching Git origin.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Ensures the official Claude Code plugin marketplace is configured.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Downloads a pinned Crit release binary, verifies its SHA256 and version, and installs it atomically via a staging file.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Selects the platform-specific pinned Crit artifact and installs it when the binary is missing or at the wrong version.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Ensures the Crit Claude Code plugin marketplace is configured.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Ensures the Ponytail Claude Code plugin marketplace is configured.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Ensures the Understand-Anything Claude Code plugin marketplace is configured.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Returns success when the Claude Code Crit plugin is already enabled.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Returns success when the Claude Code Ponytail plugin is already enabled.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Returns success when the Claude Code Understand-Anything plugin is already enabled.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or refreshes the Herdr agent integrations.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates the Claude Code Superpowers plugin.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates the Claude Code Crit plugin after ensuring its marketplace.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates the Claude Code Ponytail plugin.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates the Claude Code Understand-Anything plugin.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs the Codex Superpowers plugin from the OpenAI-curated catalog.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Ensures the Ponytail Codex plugin marketplace is configured with the expected source.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates the Codex Ponytail plugin from its marketplace.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates the Codex Crit plugin and its plan-review hook.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Builds Understand-Anything packages/core in a plugin tree when its dist output is missing or stale.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Provisions Codex Understand-Anything runtime files by building and copying from the matching Claude release artifact.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates Codex Understand-Anything skills via the vendor installer and provisions its runtime.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Returns success when zenbu-labs installers publish a build for the current platform.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Downloads an upstream installer script, verifies its pinned SHA256, and runs it.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates the terminal-code (tode) CLI at the pinned version.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or updates the terminal-browser CLI at the pinned version, including its skill symlinks.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Syncs the vendored CompactionDB tree without deleting project runtime state.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Prints sha256 lines using sha256sum or shasum on macOS.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Prints a sorted sha256 manifest of files under given paths of the agmsg skill directory, failing rather than emitting a short manifest.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Downloads and checksum-verifies the pinned agmsg tarball, backs up live state, runs upstream install.sh (with --update when installed), and verifies teams/ and messages.db were untouched and VERSION matches the pin.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Installs or refreshes the pinned upstream agmsg skill in place via install_pinned_agmsg.', 'filePath': 'scripts/update-agent-assets.sh'}
{'summary': 'Entry point that converges all managed agent CLIs, plugins, pinned tools, CompactionDB, agmsg, and Herdr integrations in order.', 'filePath': 'scripts/update-agent-assets.sh'}
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
"""Shared probes of design-quality 5.14 item 7: one attack each in a temporary fixture, and the trusted parent."""

import contextlib
import functools
import hashlib
import json
import os
import pwd
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SHIMS = ("uv", "python3", "gh", "git", "bash")
ALLOWED = ("PATH", "HOME", "LANG")
SAFE_PATH = "/usr/bin:/bin"
LEGIT, ATTACKER = "legitimate\n", "attacker\n"
BASELINE_NS, NFS = 10**18, "NFSHomeDirectory:"  # a fixed past mtime (2001): a write at any later clock tick moves it
QUIET = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
HOSTILE_GIT_ENV = ("GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CEILING_DIRECTORIES")
HOSTILE_GIT_ENV += ("GIT_ALTERNATE_OBJECT_DIRECTORIES",)
SHIM = "#!{python} -I\nimport json, sys\nwith open({record!r}, 'a') as f:\n    f.write(json.dumps({{'name': {name!r}, 'argv': sys.argv}}) + '\\n')\nsys.exit(97)\n"


class TrustedExecRefused(ValueError):
    """run_under_trusted_parent refused the script before running anything."""


class ShimProbe:
    """Failing shims of SHIMS first on PATH, each recording its name and argv as JSON through an absolute python."""

    def __init__(self, base, env=None):
        if any(c.isspace() for c in sys.executable):
            raise RuntimeError(f"{sys.executable}: a shim interpreter path must hold no whitespace")
        self.base, self.bin, self.record = base, base / "bin", base / "shim-runs.jsonl"
        self.bin.mkdir()
        for name in SHIMS:
            (self.bin / name).write_text(SHIM.format(python=sys.executable, record=str(self.record), name=name))
            (self.bin / name).chmod(0o755)
        self.env = dict(os.environ if env is None else env)
        self.env["PATH"] = os.pathsep.join(filter(None, (str(self.bin), self.env.get("PATH", ""))))

    def records(self):
        return [json.loads(line) for line in (self.record.read_text() if self.record.exists() else "").splitlines()]

    def assert_none_ran(self):
        if runs := self.records():
            raise AssertionError("shim ran: " + "; ".join(f"{r['name']} {r['argv']!r}" for r in runs))


class HostileGit:
    """A legitimate and an attacker repository; attack(kind) yields the environment to offer a consumer."""

    def __init__(self, base):
        self.base, self.legit, self.attacker = base, base / "legit", base / "attacker"
        self.hook_marker, self._env = base / "attacker-hook-ran", {"PATH": SAFE_PATH, "HOME": str(base)}
        for repo, text in ((self.legit, LEGIT), (self.attacker, ATTACKER)):
            repo.mkdir()
            self._git(repo, "init", "-q")
            (repo / "probe.txt").write_text(text)
            self._git(repo, "add", "probe.txt")  # an index, so status consults core.fsmonitor
        hook = self.attacker / "hook"
        hook.write_text(f'#!/bin/sh\necho ran >> "{self.hook_marker}"\nexit 1\n')
        hook.chmod(0o755)
        self.config = self.attacker / "attacker.gitconfig"  # included, it makes git run the attacker's program
        self.config.write_text(f"[core]\n\tfsmonitor = {hook}\n")

    def _git(self, repo, *args):
        subprocess.run(["/usr/bin/git", "-C", str(repo), *args], env=self._env | QUIET, check=True, capture_output=True)

    @contextlib.contextmanager
    def attack(self, kind):
        """Kind environment exports hostile GIT_*; the local-* kinds plant one key in the fixture's own config."""
        self.hook_marker.unlink(missing_ok=True)
        if kind == "environment":
            git_dir = self.attacker / ".git"
            values = (git_dir, self.attacker, self.config, self.config, self.legit, git_dir / "objects")
            yield self._env | {name: str(value) for name, value in zip(HOSTILE_GIT_ENV, values, strict=True)}
            return
        pairs = {"local-worktree": ("core.worktree", self.attacker), "local-include": ("include.path", self.config)}
        key, value = pairs[kind]
        self._git(self.legit, "config", key, str(value))
        try:
            yield dict(self._env)
        finally:
            self._git(self.legit, "config", "--unset", key)

    def assert_unaffected(self, root, content):
        """The consumer's confirmed root and what it read there are legitimate, and no attacker program ran."""
        real, found = os.path.realpath(root), []
        if real != str(self.legit):
            found.append(f"attacker root {root}" if real == str(self.attacker) else f"wrong root {root!r}")
        if content != LEGIT:
            found.append("attacker content" if content == ATTACKER else f"wrong content {content!r}")
        found += ["attacker hook ran"] if self.hook_marker.exists() else []
        if found:
            raise AssertionError("hostile git: " + "; ".join(found))


class WorkerRoot:
    """An input, an output and a new output under a worker root. A read shows as the input's access time leaving 0; a
    filesystem where a read leaves it at 0 (measured on a scratch file) refuses the probe instead of passing vacuously."""

    def __init__(self, base):
        self.base, seat = base, base / "root" / ".claude" / "worktrees" / "probe-seat"
        seat.mkdir(parents=True)
        self.input, self.output, self.new_output = seat / "ledger.tsv", seat / "out.txt", seat / "new" / "out.txt"
        check = base / "atime-check"
        for path in (check, self.input, self.output):
            path.write_text(LEGIT)
            os.utime(path, ns=(0, BASELINE_NS))
        if check.read_text() and os.stat(check).st_atime_ns == 0:
            raise RuntimeError(f"a read leaves the access time at 0 under {base}, so reads are not observable here")
        self._identity = {path: (os.lstat(path).st_ino, os.lstat(path).st_mode) for path in (self.input, self.output)}

    def assert_untouched(self):
        """Nothing read the input, wrote, replaced or removed either file, or created the new output's directory. The
        content is compared too, since a write in place can keep the inode, the size and a coarse clock's mtime."""
        found = []
        for path, identity in self._identity.items():
            if not os.path.lexists(path):
                found.append(f"removed {path}")
                continue
            st = os.lstat(path)
            found += [f"read {path}"] if path == self.input and st.st_atime_ns else []
            content = path.read_bytes() if (st.st_ino, st.st_mode) == identity else b""  # the same regular file only
            os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False)  # puts this read's access back
            if ((st.st_ino, st.st_mode), st.st_mtime_ns, content) != (identity, BASELINE_NS, LEGIT.encode()):
                found.append(f"wrote {path}")
        found += [f"created {self.new_output}"] if self.new_output.parent.exists() else []
        if found:
            raise AssertionError("worker root: " + "; ".join(found))


class SwappedFile:
    """A checked file, swap() linking its name (or its stat-measured case alias) to attacker content mid-consumption."""

    def __init__(self, base):
        self.base, self.path, self.attacker = base, base / "Checked.tsv", base / "attacker.tsv"
        self.path.write_text(LEGIT)
        self.attacker.write_text(ATTACKER)
        self.expected_sha = hashlib.sha256(LEGIT.encode()).hexdigest()
        flipped = self.path.with_name(self.path.name.swapcase())
        same = flipped.exists() and os.path.samefile(flipped, self.path)
        self.alias = flipped if same else None
        self.alias_reason = "" if same else f"case-sensitive filesystem under {base}: {flipped.name} does not resolve"

    def swap(self, via_alias=False):
        if (target := self.alias if via_alias else self.path) is None:
            raise RuntimeError(self.alias_reason)
        os.symlink(self.attacker, self.base / ".swap")
        os.replace(self.base / ".swap", target)

    def assert_not_consumed(self, data):
        if not os.path.islink(self.path):  # only swap() makes the checked name a link
            raise AssertionError("never swapped: the consumer did not reach the barrier, so the probe proves nothing")
        if data != LEGIT.encode():
            raise AssertionError("attacker content consumed" if data == ATTACKER.encode() else f"unexpected {data!r}")

82:HCOM_DARWIN_ARM64_URL="https://files.pythonhosted.org/packages/f5/ed/5e951b0e6fcadef1a2598e82b969b3eaa387a3e202f8987102d0e84cddfc/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl"
83:HCOM_DARWIN_AMD64_URL="https://files.pythonhosted.org/packages/ba/c3/04dd3c68d87620fa347372b5e9450c3bb3518aa096abdf08169e6d2ce37f/hcom-0.7.30-py3-none-macosx_10_12_x86_64.whl"
84:HCOM_LINUX_AMD64_URL="https://files.pythonhosted.org/packages/21/fb/0a48f19a1c39b4ff59412f1fe34130c14acbc55da69097018d729191c6d2/hcom-0.7.30-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
85:HCOM_LINUX_ARM64_URL="https://files.pythonhosted.org/packages/f0/23/e746ce90643a1286ed3c6410c66eaae7134fbd2267d002814e6a932a2b60/hcom-0.7.30-py3-none-manylinux_2_28_aarch64.whl"
993:# @description Verify the pinned platform wheel before uv installs hcom, and keep it where uv's receipt points.
996:function update_hcom() (
1004:        printf 'Skipping hcom: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
1009:        printf 'Skipping hcom: uv command not found.\n'
1012:    section "hcom"
1013:    # uv's receipt records the wheel's path as hcom's source and `uv tool upgrade` re-reads it, so the verified wheel
1015:    wheel_dir="${HOME}/.local/share/agent-assets/hcom"
1016:    installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
1019:        printf 'hcom %s is already installed.\n' "${installed}"
1028:        printf 'hcom checksum mismatch: expected %s, got %s.\n' "${expected}" "${actual}" >&2
1038:    installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
1040:        printf 'hcom version mismatch: expected %s, got %s.\n' "${HCOM_PIN_VERSION}" "${installed}" >&2
1043:    manifest_record "update_hcom" installer "${HCOM_PIN_VERSION}" "${HOME}/.local/bin/hcom" "${wheel}" -- "uv tool install --force <verified-hcom-wheel>"
1253:    update_hcom

**Improving tool output formatting**
exec
/bin/zsh -lc "sed -n '119,122p' .orchestration/plans/024-design-quality.md; /usr/bin/file ~/.local/share/uv/tools/hcom/bin/hcom; /bin/ls -l ~/.local/share/uv/tools/hcom/bin/python*; /usr/bin/head -c 800 ~/.local/share/uv/tools/hcom/bin/hcom; /usr/bin/shasum -a 256 .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md" in ~/Workspace/dotfiles
 succeeded in 24ms:
~/.local/share/uv/tools/hcom/bin/hcom: Mach-O 64-bit executable arm64
lrwxr-xr-x@ 1 a0004262  staff  85 Oct 20 14:02 ~/.local/share/uv/tools/hcom/bin/python -> ~/.local/share/uv/python/cpython-3.10-macos-aarch64-none/bin/python3.10
lrwxr-xr-x@ 1 a0004262  staff   6 Oct 20 14:02 ~/.local/share/uv/tools/hcom/bin/python3 -> python
lrwxr-xr-x@ 1 a0004262  staff   6 Oct 20 14:02 ~/.local/share/uv/tools/hcom/bin/python3.10 -> python
����            �	  � �        H   __PAGEZERO                                                        �  __TEXT                  ��              ��                  __text          __TEXT           
     �|�      
               �            __stubs         __TEXT          ؆�    �      ؆�             �           __stub_helper   __TEXT          ���           ���              �            __const         __TEXT           ��    Ā      ��                            __gcc_except_tab__TEXT          � �    �4     � �                            __cstring       __TEXT          DU�    P�     DU�                           __unwind_info   __TEXT          �#�    @�     �#�                            __eh_frame      __TEXT          ز�    ��     ز�            05000f451d9fc1ed38d962e9e863724793dea281330b2c21fd578af5bca35ee6  .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md

exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-17775c1.md.last.md .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-7c44fca.md.last.md .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-2db29fc.md.last.md .orchestration/validation/dotfiles-T129-hcom-dispatch-bus-a02-text-security-4a0347c.md.last.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:73 The marker format specifies no escaping or rejection of embedded newlines: one worker message can contain a forged acceptance row that the unchanged parsers treat as a separate event; the named history/payload tests need a reader-side framing attack.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:75 Preserving sent-row identification retains selection of the last matching sender/recipient/body rather than the sent message’s ID; two concurrent identical messages can record `read` while this send remains unread, which the prescribed roundtrip fixture does not test.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:84 The required manifest-bound store location has no declaration in `agent-config.yaml`, and neither this task nor T133 authorizes adding it; fixture-only declarations cannot establish the production binding—specify its authoritative location and authorize any required declaration with a threat row.

📝 まとめ: Reviewed all 40 threat rows and cited context; found three design gaps, with parser and receipt-selection behavior confirmed by in-memory probes. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-user isolation and deployment protections remain unverified residuals.
Verdict: incorrect[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:122 Amendment 1 still executes hcom from the shared uv directory forbidden by design item 9: hashing before invocation leaves replacement between verification and execution possible, while the prescribed fixture replaces the file before verification; consume a verified, protected executable and test that handoff before marking this boundary closed.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:153 The Checks show owner-writable filesystem modes, not worker write denial or protection of the executable namespace, snapshots and cache; they do not supply the item 1/2/9 deployment measurements required before review/anchor.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:132 The generated command still loses the argument boundary around `sh -c`’s command string: replaying the printed `sh -c exec …` does not execute the recorded Git command, so separate exit statuses have not resolved the previous evidence-reproducibility finding.

The installed hcom currently matches the executable inside the pinned wheel; the first finding concerns the subsequent execution handoff.

📝 まとめ: Reviewed all 42 threat rows and cited acceptance/review context; three findings remain for orchestrator disposition. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-UID isolation and credential separation remain declared residual risks.
Verdict: incorrect[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:126 The claimed worker write-boundary measurements are absent from Checks: the generator puts those probes in its non-hcom branch; filesystem modes—and even allowWrite lists alone—cannot establish protection against Claude’s unsandboxed file tools, so the private executable and adjacent digest remain unproven until actual denial controls are measured.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:28 Setting only `UV_TOOL_DIR` leaves executable publication at `~/.local/bin`; the prescribed `uv tool install --force` therefore replaces the existing public hcom entry, an unmodelled effect the named private-install/drift test need not detect—bind `UV_TOOL_BIN_DIR` privately and assert the public entry remains unchanged. [uv documentation](https://docs.astral.sh/uv/reference/cli/#uv-tool-install)

📝 まとめ: Reviewed all 43 threat rows and referenced acceptance/review context; two findings remain for orchestrator disposition. No files changed.

Not checked: implementation, CI or live Linux/race execution; same-UID isolation and credential separation remain declared residual risks.
Verdict: incorrect[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md:158 The claimed worker write-boundary measurement prints only unrendered template keys, omitting allowWrite/socket members and effective seat settings; it cannot establish amendment 2’s private-directory protection—record effective per-seat boundaries and denial evidence before anchoring.

📝 まとめ: Reviewed all 43 threat rows and cited acceptance/review history; one deployment-evidence finding remains. No files changed.

Not checked: future implementation, CI or live Linux/race execution; same-UID replacement and credential separation remain declared residual risks.
Verdict: incorrect
**Reviewing code changes and testing approach**
exec
/bin/zsh -lc "tail -3 .orchestration/plans/024-design-quality.md; cat .orchestration/acceptance/dotfiles-T133-gh-binding-a02-review-a01.md; tail -32 .orchestration/acceptance/dotfiles-T133-gh-binding-a02.md; sed -n '65,110p' .orchestration/tasks/dotfiles-T133-gh-binding-a02.md; sed -n '1,85p' .orchestration/acceptance/dotfiles-T129-hcom-dispatch-bus-a01.md" in ~/Workspace/dotfiles
 succeeded in 23ms:
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。
---
{
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02-review-a01.md task_sha256=0b954cc99b76901d0c79119bffdbb078ec0bb718906338de809287352019a302 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=c0a7dae7d7e10974669ebd2e21b79907a5b5c5e84016d308b9d4fa8bce73c3df allowed_files=see-task-file forbidden_actions=edit;dispatch;network-write expected_result_file=.orchestration/dotfiles-T133-gh-binding-a02-review-a01/review.md done_signal=AGMSG-RESULT max_turns=20 note=anchor-review-of-the-gh-binding-a02-text(reset-of-a01;C-80-correct-at-c0a7dae7-after-the-bound-Checks-paste);read-only;reply-by-agmsg-dispatch-to-wW:p1 read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=2 amendment=1 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a previous_design_sha256=c0a7dae7d7e10974669ebd2e21b79907a5b5c5e84016d308b9d4fa8bce73c3df reason=your-round-1-findings-answered:the-Checks-block-is-now-generated-by-.agents/worklog/orchestrator-glue/checks-paste.sh(every-line-a-full-command-under-one-enumerated-environment-with-its-exit-status,absolute-executables-with-digests,no-prose,no-inherited-git-configuration);line-128's-cache-sentence-removed,item-9-stays-the-source-in-the-body;canonical-main-is-7b21659e-after-the-#442-merge;C-80-Verdict-correct-at-this-sha(…-text-security-63d69cc.md.last.md) next_action=review-round-2:compute-the-hash,judge-items-1-7-of-your-task(item-3-now-reads:every-Checks-line-is-a-command-and-its-output),RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=hold round=2 pr=none verdict=reject reason=RESULT-3045-received(reject:the-executables-line-held-values-without-commands;P3-exit-status-advisory);fixed-in-the-generator-and-regenerated-at-sha-3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9;fifth-refusal-of-class-checks-paste-provenance:the-lineage-waits-for-the-operator-before-C-80-round-6-and-your-round-3 next_action=hold:no-worker-action-until-the-round-3-ACCEPTANCE read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=3 amendment=2 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 previous_design_sha256=63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a reason=your-round-2-finding-answered:every-Checks-line-is-now-one-command-with-its-output-and-exit-status(the-executable-digests-are-one-shasum-command,git---version-and-codesign--dv-are-commands,the-mise-pin-is-read-from-the-private-clone);line-109-names-the-Codex-seat's-report-route(send.sh---body-file,Playbook-step-6);C-80-Verdict-correct-at-this-sha(…-text-security-3c1d54a.md.last.md) next_action=review-round-3:compute-the-hash,judge-items-1-7,RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=accepted round=3 pr=none verdict=accept design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 reason=round-3-accept,findings=0(P3-advisory:two-pipeline-lines-without-exit,recorded);the-gh-binding-a02-TASK-goes-to-a012-on-these-bytes next_action=none:the-seat-is-free read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=4 amendment=3 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 previous_design_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 reason=amendment-1-of-the-design-text-after-the-seat's-first-command:an-exit-0-Operation-not-permitted-on-.git/packed-refs.lock-or-.git/config.lock(the-T64-read-only-common-dir)-is-measured-state-recorded-in-sandbox.md,every-other-denial-stays-blocked;previous_sha256-added-to-the-front-matter;Checks-block-unchanged;C-80-Verdict-correct-at-this-sha(…-text-security-2adb147.md.last.md) next_action=review-round-4:compute-the-hash,judge-items-1-7(item-2:the-amendment-contradicts-no-design-item;item-5:no-threat-row-changes),RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=accepted round=4 pr=none verdict=accept design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 reason=round-4-accept,findings=0;amendment-1-goes-to-a012-as-an-ACCEPTANCE-revise next_action=none:the-seat-is-free read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=5 amendment=4 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c previous_design_sha256=2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 reason=amendment-2-of-the-design-text:Item-6-authorizes-test_orch_gate_path.py,test_orchestrator_tools.py,test_chain_review_scripts.py,test_validate_agent_assets.py-and-test_agmsg_orchestration_docs.py-for-fixture-adoption-only(CI-at-2804b176-failed-in-their-fixtures;found-by-grep-on-main:they-exercise-the-bound-scripts),test-cap-1000,source-cap-350,one-report-line-per-legacy-module;Checks-and-threat-rows-unchanged-except-the-test-row-wording;C-80-Verdict-correct-at-this-sha(…-text-security-86513b2.md.last.md) next_action=review-round-5:compute-the-hash,judge-items-1-7(item-4:the-touch-point-grep-now-covers-the-test-modules-that-reference-each-changed-script),RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=hold round=5 pr=none verdict=reject reason=round-5-RESULT-received(item-4:scripts/lint-comparisons-baseline.tsv-is-a-touch-point;P3-wording);amendment-3-written-at-728f0ffe(baseline-for-stale-row-removal-only-with-a-closed-row,wording)-and-in-C-80;round-6-follows-a-correct-verdict next_action=hold:no-worker-action-until-the-round-6-ACCEPTANCE read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=revise pr=none round=6 amendment=5 design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 previous_design_sha256=86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c reason=amendment-3-of-the-design-text-answers-your-round-5:scripts/lint-comparisons-baseline.tsv-joins-allowed_files-for-stale-row-removal-only-with-a-row-closed-by-the-existing-LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline(new-R1/R4-hits-are-fixed-in-the-sources);row-29-says-nine-modules;the-authorization-sentence-is-Item-0's;C-80-Verdict-correct-at-this-sha(…-text-security-e9ce1c3.md.last.md) next_action=review-round-6:compute-the-hash,judge-items-1-7(item-4:the-touch-point-grep-covers-tests-and-the-lint-baseline-for-every-changed-script),RESULT-with-verdict=accept|reject read_at=read",
    "AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=accepted round=6 pr=none verdict=accept design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 reason=amendments-2-and-3-accepted-at-round-6;they-go-to-a012-as-one-ACCEPTANCE-revise next_action=none:the-seat-is-free read_at=read"
  ]
}
---
# Acceptance: dotfiles-T133-gh-binding-a02-review-a01

Anchor review of the gh-binding a02 text (reset of a01 under S-R5; D-024-69). Design file `.orchestration/tasks/dotfiles-T133-gh-binding-a02.md` at `c0a7dae7d7e10974669ebd2e21b79907a5b5c5e84016d308b9d4fa8bce73c3df` (C-80 rounds: c761dc8 correct unpopulated; 0ecdc07 incorrect, two P1 on the unbound canonical measurement; c0a7dae correct after the bound-executable re-measurement). Review seat a011 (worker-d, wW:p4).

## Counters (INV-6)

amendments=0 revises=0 questions=0 at dispatch.
- 2026-10-22T01:24Z: round 1 RESULT (a011) `verdict=reject`, findings=2 (Checks line 128 against design 5.14 item 9; lines 127-130 claims without commands); both fixed in the text at 5d62e48e; round 2 waits for the C-92 re-plan of the a02 lineage and its next C-80.
dispatch: [2026-10-22T01:29:09Z] claude-deep-dot → claude-standard-dot-a011: AGMSG-ACCEPTANCE v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=hold round=1 (bus row ○ read; recorded by hand because the dispatch.sh run that sent it was stopped during its slow post-send bus read)
- 2026-10-22T02:35Z: round 2 (amendment 1) sent: design sha 63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a after C-80 correct (hand line).
- 2026-10-22T02:56Z: round 2 RESULT (a011) reject (executables line without commands; P3 exit status); hold sent; round 3 after the operator's answer on the lineage stop (hand line).
- 2026-10-22T02:59Z: round 3 (amendment 2) sent: design sha 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 after C-80 correct (hand line).
- 2026-10-22T03:01Z: round 3 RESULT (a011) accept at 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9, findings 0, advisory P3 (two pipeline lines print no exit); ACCEPTANCE accepted sent (hand line).
- 2026-10-22T03:38Z: round 4 (amendment 3 of this review task = amendment 1 of the design text) sent at design sha 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 (hand line).
- 2026-10-22T03:40Z: round 4 RESULT (a011) accept at 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7, findings 0; ACCEPTANCE accepted sent (hand line).
- 2026-10-22T05:19Z: round 5 (amendment 2 of the design text) sent at design sha 86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c (hand line).
- 2026-10-22T05:25Z: round 5 RESULT (a011) reject (item 4: the lint baseline; P3 wording); hold sent; round 6 after the C-80 of amendment 3 (hand line).
- 2026-10-22T05:29Z: round 6 (amendment 3 of the design text) sent at design sha e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 (hand line).
- 2026-10-22T05:32Z: round 6 RESULT (a011, 05:30:44Z) accept at e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1; ACCEPTANCE accepted sent (hand line).
anchor:a011:r2:1	checks-paste-provenance
anchor:a011:r2:2	advisory-p3-exit-status
- 2026-10-22T02:35Z: C-80 round 5 of the lineage (63d69cc0, the corrected generated block) `Verdict: correct`; anchor round 2 sent to a011 (amendment 1 of the review task, design sha 63d69cc0438e90a1e25678b46006012835842ec4f6cc21934c512c75cb57b21a; bus row after 2026-10-22T02:35Z, hand line).
- 2026-10-22T02:55Z: anchor round 2 (a011, RESULT 3045 at 02:37:14Z) `verdict=reject`: the generated block's closing "executables:" line held values without their commands (shasum, git --version, codesign); P3 advisory: only the canonical lines printed an exit status; observation: the mise pin was read from the working file, not the clone. This is the fifth refusal of class checks-paste-provenance (rows text-security:0ecdc07:1-2, anchor:a011:r1:1-2, text-security:b700fe8:1, anchor:a011:r2:1): the re-plan line's stop applies and the lineage waits for the operator. Prepared meanwhile, no review run: the generator prints every host line through one `stage` (command, output, exit status), the executable digests as one `shasum` command, `git --version` and `codesign -dv` as commands, the mise pin from the private clone (`git show refs/heads/main:home/dot_mise/config.toml | sed -n 43p`); the text names the Codex seat's report route (`send.sh … --body-file`, Playbook step 6; the gap the map agent found at line 109, the same as slice1's); regenerated block 21 lines (canonical main 7b21659e, design digest a027b021…, 19 lines with exit status: 18 exit 0 and the trusted_tools grep exit 1 = 0 matches), pre-send OK at sha 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 (145 lines). Default put to the operator: C-80 round 6 on these bytes, then anchor round 3, then dispatch to a012 (seated at wW:p7 at 02:49Z, linkage pending).
text-security:3c1d54a:0	correct
- 2026-10-22T02:59Z: C-80 round 6 of the lineage (3c1d54a9, the fully generated block plus the Codex route sentence) `Verdict: correct`; the operator's "推奨案で実施" covered the run after the fifth refusal (the structural cause, a hand-written line, was removed from the generator); anchor round 3 sent to a011 (design sha 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9; hand line).
anchor:a011:r3:0	accept
anchor:a011:r3:1	advisory-p3-exit-status
- 2026-10-22T03:01Z: anchor round 3 (a011, RESULT at 03:00:34Z) accept at 3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9, findings 0, P3 advisory (the design-digest and mise-pin pipeline lines carry no exit status; recorded, no change: the anchored bytes stay frozen, as does the informational front-matter field dispatch_status: blocked-pre-anchor, which the checker does not read). counters before the dispatch (`scripts/regime-counters.sh dotfiles-T133-gh-binding-a02`, 2026-10-22T03:01Z): task=dotfiles-T133-gh-binding-a02 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=none..none (-) source=live. Dispatch to codex-standard-dot-a012 (worker-g, wW:p7, alive 02:53Z) follows as round 1; overlap_ok lists the 16 open PRs whose files fall under the task's globs (none in flight as a worker task; #378 held; #454 shares no file).
dispatch: [2026-10-22T03:02Z] claude-deep-dot → codex-standard-dot-a012: AGMSG-TASK v1 task_id=dotfiles-T133-gh-binding-a02 round=1 task_sha256=3c1d54a9191af00478de29a1d69f251719fed4f692f0cb50a9d1adbf65ba36c9 (bus row at 03:0xZ; hand line, see the history row for the read marker)
- 2026-10-22T03:37Z: a012 PONG status=blocked (03:05:50Z): `git switch -c tools/gh-binding-a02 --no-track origin/main` exited 0 and created the branch (verified: worker-g HEAD), then printed two `Unable to create .git/packed-refs.lock: Operation not permitted` lines; the shared common dir is read-only for Codex seats by design (T64), so this is the boundary working as designed, not a defect; a probe from the orchestrator checkout shows branch creation touching no packed-refs lock there (the Claude sandbox denies .git/config.lock instead, also with exit 0), so the trigger is seat-specific and the amendment names the class, not a cause. Amendment 1 (previous_sha256 3c1d54a9…): an exit-0 denial on .git/packed-refs.lock or .git/config.lock is measured state recorded in sandbox.md; every other denial stays blocked; pre-send OK at sha 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 (148 lines); C-80 running; anchor round 4 (a011) follows; hold ACCEPTANCE sent to a012 (hand line).
text-security:2adb147:0	correct
- 2026-10-22T03:38Z: C-80 of amendment 1 (2adb1477) `Verdict: correct`; anchor round 4 sent to a011 (hand line).
anchor:a011:r4:0	accept
- 2026-10-22T03:40Z: anchor round 4 (a011, 03:39:52Z) accept at 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7, findings 0 (diff against the round-3 bytes: previous_sha256 and the Amendment 1 paragraph only; the exception is design 5.14 item 1 working as designed). a012 acknowledged the hold (PONG 03:38:52Z, branch preserved). counters before the send (`scripts/regime-counters.sh dotfiles-T133-gh-binding-a02`, 2026-10-22T03:40Z): task=dotfiles-T133-gh-binding-a02 tasks=1 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-22T03:02:12Z..none (-) source=live. ACCEPTANCE status=revise round=1 amendment=1 sent to a012 with task_sha256 2adb14773dc6ec1563b0ddb518edf27e4b23d6eb8c9a817c9f243cbc1faf82f7 (hand line).
- 2026-10-22T04:27Z: a012 PONG status=question (04:25:02Z; INV-6 questions=1): the gate executes the authenticated base's collector (require-crit-review.py:608-615), whose bytes at 7b21659e call bare gh without --hostname, and the selected bytes must stay unchanged; may the gate refuse such a collector until a02 is on main, or is an older-base contract authorized? Answer sent as a PING at 2026-10-22T04:27Z (no rule sentence changes; the text's item-4 constants rule applies): never refuse the base collector; supply the executable through item 2's private PATH link gh -> the declared path, the host as the explicit constant GH_HOST=github.com (gh help environment: '`GH_HOST`: specify the GitHub hostname for commands where a hostname has not been provided, or cannot be inferred from the context of a local Git repository. If this host was previously '), the repository by the --repo argument the gate already passes; drop ambient GH_HOST/GH_REPO/GH_CONFIG_DIR first; one fixture (older selected collector + decoy gh + planted ambient GH_HOST); after the merge the constants stay as defence in depth. The worker meanwhile fixes its independent-review findings (equality, token-free discovery, manifest ambiguity).
- 2026-10-22T04:45Z: a012 PONG status=question (04:44:30Z; INV-6 questions=2, S2's questions count reached: judged at the next acceptance action): before its HTTPS push, PR and CI it asked for the measured items 2/9 parent namespace and deployed gh/config evidence, or an authorized transport route. Answer sent as a PING at 2026-10-22T04:45Z (no rule sentence changes): the push, PR creation and CI are Worker Playbook step 2/4 operations from inside the Codex sandbox (T64 network_access, HTTPS push without -u, gh pr create --draft), which is the authorized transport (design 5.14 item 10); row 38's 'authenticated use is blocked' scopes the consumers this task binds (the orchestrator's acceptance-time reads and the gate's collector), not the worker's transport; no parent measurement precedes the push. Both questions of this lineage come from the same over-reach of the residual rows into the worker's own transport; the rows are the design's residuals and stay as written.
- 2026-10-22T05:04Z: a012 PONG status=blocked (05:00:20Z) and RESULT status=blocked (05:02:46Z): PR #456 opened as a draft at 2804b176 (source 321/350, tests 698/700, baseline red 16 tests, implementation green 166, portable routes 14); the block is gh's run-log cache write under ~/.cache/gh denied by the Codex writable roots while reading the regime job log, held per the boundary rule. Answer sent as a PING at 2026-10-22T05:04Z: XDG_CACHE_HOME as an explicit constant of the env -i contract (gh honours it; item 4's nonsecret constants) to a private directory, re-run inside the sandbox; the regime failure is the D-024-64 class, not a hold; finish ready/CI/Bot/RESULT; the orchestrator copies the worktree artifacts at the ready RESULT.
- 2026-10-22T05:08Z: a012 resumed (PONG 05:05:07Z, transport cache under its private TMPDIR, gh pr ready next); the blocked RESULT is answered on the bus by an ACCEPTANCE status=revise round=1 text=unchanged (continuation, no new check=); CI at 2804b176: regime red (known class) and test (ubuntu-26.04, client) red, to be fixed within round 1.
- 2026-10-22T05:15Z: a012 PONG status=question (05:14:24Z; INV-6 questions=3): CI on 2804b176 fails in the fixtures of three legacy test modules that exercise the bound scripts and are outside Item 6's four modules. Orchestrator text defect (the task-file review's touch-point grep covered gh calls, not the tests that exercise the changed scripts): amendment 2 authorizes the five legacy modules for fixture adoption only (the three named plus test_validate_agent_assets.py and test_agmsg_orchestration_docs.py, found by grep on main), test cap 1000; pre-send OK at 86513b290ea19e044c8d7c06cd8dfb9afbc90fc1a4b5c173154e49d08b8b4f9c; C-80 and anchor next; answer PING sent. S2 note: questions=3 and amendments=2 after this; both counts are judged at the acceptance action with this explanation.
search: touch-point-coverage -> none
re-plan: touch-point-coverage (rows: the a02 text's Item 6 listed four test modules while five legacy modules exercise the scripts the task binds, found by CI at 2804b176 and by grep on main; the task-file review's item 4 enumerated gh call sites only) — specification: a task's allowed test set is every test module that references a changed script or module by name (grep over tests/unit for each basename in allowed_files), stated in the text before dispatch, never discovered by CI; design: the task-file review's item 4 names that enumeration explicitly, and pre-send gains the same check as a mechanism (owner: dotfiles-T133-pre-send-check-followup-a01: refuse a text whose test allowance omits a module that references a changed script); implementation: amendment 2 of this text widens Item 6 to the nine modules with fixture-adoption-only for the five legacy ones and raises the test cap to 1000; verification: CI of the next head green on the five modules, the anchor review item 4 run with the enumeration, and no further test-scope amendment on this lineage.
text-security:86513b2:0	correct
- 2026-10-22T05:19Z: C-80 of amendment 2 (86513b29) `Verdict: correct` after the touch-point-coverage re-plan line (C-92); anchor round 5 sent to a011 (hand line).
anchor:a011:r5:1	touch-point-coverage
- 2026-10-22T05:23Z: anchor round 5 (a011, 05:22:14Z) reject on item 4: scripts/lint-comparisons-baseline.tsv is a touch point (a stale row for orch-gate.sh R1 fails the lint on a changed file; new R1/R4 hits in orch-gate.sh and pr-feedback.py are fixed in the sources); P3 wording (row 29 four modules; Item 6 versus Item 0). Amendment 3: the baseline joins allowed_files for stale-row removal only with a closed threat row, wording fixed; pre-send OK at 728f0ffe540d8eddc2261eeb89de3cdf11066a9660e900f9527c2f8833421eca; C-80 then anchor round 6; the touch-point-coverage class gains its second row (the task-file review's grep must also cover the lint baseline for every changed script).
text-security:728f0ff:1	selector-existence
- 2026-10-22T05:26Z: C-80 of amendment 3 (728f0ffe) incorrect on one P2: the baseline row named a test that does not exist; the row now closes through the existing LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline; pre-send OK at e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1; C-80 again (the third since the touch-point-coverage re-plan line).
text-security:e9ce1c3:0	correct
- 2026-10-22T05:29Z: C-80 of amendment 3 with the existing selector (e9ce1c3b) `Verdict: correct`; anchor round 6 sent to a011; on accept, amendments 2 and 3 go to a012 as one ACCEPTANCE revise (task_sha256 e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1) (hand line).
anchor:a011:r6:0	accept
- 2026-10-22T05:32Z: anchor round 6 (a011) accept at e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1; counters before the send (`scripts/regime-counters.sh dotfiles-T133-gh-binding-a02`, 2026-10-22T05:32Z): task=dotfiles-T133-gh-binding-a02 tasks=1 amendments=0 questions=3 results=1 withdrawn=0 revises=0 first_result_head=2804b176adc394109dd1f7df86e23cdb87f6b2f5 bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-22T03:02:12Z..2026-1 / S2: questions 3 >= 2 source=live; ACCEPTANCE status=revise round=1 amendment=3 (amendments 2 and 3) sent to a012 with task_sha256 e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1 (hand line). Counter note: the lineage shows questions=3 and the bus revise rows of the two continuation lines; the first amendment and both continuations were orchestrator-side corrections or confirmations, not worker rounds, which the acceptance record states when S2 is read.
---

# AGMSG-TASK dotfiles-T133-gh-binding-a02 — bind gh and its gate descendants

D-024-69 advances this remedy ahead of slices 2-5. This S-R5 reset supersedes the 2026-10-21 owner stub and a01 round-2 text; TASK names Codex worker a012. pins-a01 merged as #449; after is empty and later binding adds sibling declarations.
Seven C-80 refusals share the unbound-gh P1: a07-checker 922292d/0edbd8c/fd8c003/c6cebe4/a3125e1; regime-ci-followup-a02 a232baf/a18a67d. A substitute can forge main, design, merge state and PR data and read forwarded credentials.
a01 rounds 3bf2a79 (3 P1, 3 P2) and 6486b79 (1 P1, 1 P2) are superseded; Items 6/7 authorize and test the refused descendant changes while retaining the other round-2 requirements.
Design 5.14 items 0-10 apply by reference, particularly 2-4/8/9; this text does not redefine that contract.

## Items

0. Inventory: local HEAD/origin/main observed at 7da0cdfab9de9fbea673b82379acd4e317115065; chain-finish.sh is absent and regime-ci.py/task-consistency-check.py currently use Git, not gh. These are local observations, pending gh-free canonical confirmation before C-80/anchor.
   Implement the three present shell routes and their real gate/collector descendants. Do not invent chain-finish or add canonical-network behavior to the checkers; dotfiles-T133-gh-binding-followup-a01 owns all three future routes and their positive authenticated decoy fixtures.
   The shell wildcard authorizes only chain-integrate.sh, orch-gate.sh and local-review.sh; the test wildcard authorizes test_supply_chain_policy.py, test_chain_glue.py, test_require_crit_review.py and test_pr_feedback.py for new fixtures, and, for fixture adoption only (a fixture adopts the bound gh and the declaration; no assertion is weakened, deleted or re-targeted), test_orch_gate_path.py, test_orchestrator_tools.py, test_chain_review_scripts.py, test_validate_agent_assets.py and test_agmsg_orchestration_docs.py, the modules that exercise the scripts this task changes (amendment 2). If canonical inventory differs, reauthor/review the whole inventory and threat table before dispatch.
1. Pin `"github:cli/cli" = "2.102.0"` in home/dot_mise/config.toml with one adjacent English reason comment following pins-a01; retain unrelated pins. Installed target: `~/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh`.
2. Declare trusted_tools.gh with version "2.102.0" and that home-relative absolute target in agent-config.yaml; later uv/Python/Node entries are siblings.
   validate-agent-assets.py checks pin equality, normalized home-anchored spelling, absolute expansion under the real user's home, and no shims component in spelling or resolved path. Refuse missing/malformed declarations, traversal, forged HOME and mismatched identities; give every rule a separate refusal subtest.
   Runtime reads protected deployed ~/.agents/agent-config.yaml as data with existing parsing facilities under design 5.14 items 2/9, never source/eval or a worker/PR copy. Chezmoi deploys this plain source; create no rendered artifact and leave generator/rendering tests unchanged.
3. Replace gh discovery in chain-integrate.sh/orch-gate.sh; bind local-review.sh's descendant namespace and both authorized Python consumers to the declaration. No PATH, mise-which, latest, wrapper or caller-selected executable override may supply gh.
   Require the version-specific absolute realpath, regular executable, existence, non-shim/trusted-root checks and matching reported version; consume that checked target under design 5.14 items 3/4. Missing/mismatching identity emits exactly `refused: gh binding`, exits nonzero and performs no canonical operation or fallback.
   Every repository REST read names literal repos/mryfmo/dotfiles endpoints and --hostname github.com; GraphQL fixes owner=mryfmo/name=dotfiles and accepts node IDs only from those bound queries. gh pr uses --repo github.com/mryfmo/dotfiles, never unsupported --hostname; account/auth probes bind the host and version probes make no network call.
   Preserve today's uv/git/date/mise and other non-gh resolver algorithms only within the orchestrator's measured design 5.14 items 2/9 parent/namespace, established before the first credential-bearing process. Discovery is token-free; without that evidence authenticated operation remains blocked.
4. Construct minimal environments for every bound gh, including token-free identity probes; use protected GH_CONFIG_DIR=/var/empty, verify the resolved directory and ancestors are protected and the directory itself is empty with no symlink/config payloads, and refuse unsafe/missing configuration without creation or fallback.
   Normalize only the call's explicitly supplied token to GH_TOKEN; no implicit home/keychain credentials. Supply trusted HOME/PATH, absolute UV_CACHE_DIR, fixed configuration, disabled prompts/update notices and plain output explicitly; record allowed names without values. Every env -i contract includes UV_CACHE_DIR.
   Exclude ambient GH_HOST/GH_REPO/GH_CONFIG_DIR/XDG_CONFIG_HOME, proxies, loader/startup variables and Git overrides. Test planted home/XDG config with http_unix_socket, aliases and alternate hosts, unsafe-config refusal and a positive controlled authenticated operation.
5. No workflow/regime.yml, launcher, permission, dependency, unrelated resolver-algorithm or acceptance-semantic change; regime-ci-followup-a02 owns the workflow. Add/rename no executable and keep evidence non-executable; other runtime binding remains dotfiles-T133-trusted-entrypoint-binding-a01's scope.
6. Edit scripts/require-crit-review.py and scripts/pr-feedback.py: the gate's pr_base_errors must use the bound gh and --repo github.com/mryfmo/dotfiles, never discover authority from local Git context after removing GH_REPO. The collector uses the same declared target and host/repository binding for REST, GraphQL and auth calls.
   Reject conflicting CLI/evidence repositories; hostile remote, GH_REPO and GH_HOST cannot redirect authority. Preserve authenticated-base collector selection and all feedback checks; never execute a PR collector in place of that selected source.
   Test the real gate path through PR view and collector launch, and separately the real collector, with a foreign remote plus hostile GH_REPO/GH_HOST. Require successful fixed-host/repository responses, consumed results and observed descendant argv/environment; mocking subprocess launch or pre-sanitizing away the attack does not close the row.
7. Replace the gate's bare sys.executable collector launch with the gate's measured absolute Python plus -I and design 5.14 item 9's constructed environment, including absolute UV_CACHE_DIR. PYTHONSAFEPATH alone is insufficient; preserve the selected collector bytes and subprocess failure propagation.
   A real-descendant test launches the gate and its selected real collector with planted user-site .pth/sitecustomize.py/usercustomize.py and PYTHONSTARTUP markers; prove the same hook can execute without isolation, then assert no marker and a successful collected response with production isolation.

## Check

The final diff has at most 350 changed lines outside `tests/` and `.orchestration/`, and at most 1000 under `tests/` (amendment 2: the fixture adoption in the five legacy modules).
Measure with `git diff --numstat <merge-base40> <head40>`.
Caps are PR-wide additions plus deletions from git merge-base <authenticated-main40> <head40> (C-123), never round deltas; record dispatch measurement_base40, final main/head/merge-base SHAs, every numstat row and both totals, and recount after update-branch. Expected width is about 200/400; 350/700 includes fixtures and one Bot fix round, with no exemption from a07's 446/709 rewrite.
Write fixtures first and implement every closed selector. Each active shell route and both Python consumers needs a positive authenticated operation, synthetic credential, fixed host/repository and consumed response through declared gh; separately test missing/version/path refusals. Matrices cover all five consumers, including review/gate descendants; absent checkers/chain-finish are not passing entries.
Plant executable PATH gh and hostile mise answers without prebinding gh in the trusted-parent fixture; assert neither executes nor receives the synthetic credential. Minimal-environment/configuration matrices observe every consumer's actual child environment.
Reuse trusted_exec_contract.py without modification. Before fixture Git init/add/commit/reset/fetch, construct fresh environments and explicit roots, never os.environ merges; test hostile GIT_DIR/GIT_WORK_TREE/GIT_CONFIG_* and local includes/hooks, preserving a second repository's refs/index/bytes and external markers.
For each behavioral requirement in Items 1-4/6/7, record red at origin/main production bytes and green at the fix commit: selector, full baseline/red-fixture/fix SHAs, exact commands, stdout/stderr and real status. Red reaches the intended assertion, never missing API/import/setup/tool failure. Items 0/5 use inventory/diff evidence; no fabricated red or closure for future consumers.
Run `uv run python -m unittest tests.unit.test_supply_chain_policy tests.unit.test_chain_glue tests.unit.test_require_crit_review tests.unit.test_pr_feedback -v` through measured absolute uv/Python with item 9 isolation and temporary absolute UV_CACHE_DIR; record the expanded invocation.
Run bash -n, shellcheck and shfmt --indent 4 --space-redirects --diff on the three changed shells; ruff check --config ruff.toml and ruff format --check --config ruff.toml on changed Python; make validate-agent-assets and the review gate. Never run Bats locally.
Resolve observations with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" UV_CACHE_DIR="$UV_CACHE_DIR" "$HOME/.local/bin/mise" which uv`, repeat for python, and paste actual outputs; uv's installed path has no assumed bin component. Discovery is not trusted-parent deployment evidence.

## Execution and evidence
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T129-hcom-dispatch-bus-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md task_sha256=1fed50618ef0815e290115b6e9f85820dcb66376011a9e28fb1f20a194924631 deadline=none done_signal=AGMSG-RESULT note=a008:plan-023-PR-C-stage-1,main-based(fresh-branch-from-origin/main;your-lint-follow-up-branch-stays-pushed-for-its-stacked-PR-after-387-merges);hcom-0.7.30-is-installed-at-~/.local/bin/hcom(item-0-facts-first);rebase-after-390-merges-before-the-RESULT;under-the-morning-merge-gate-policy-you-open-your-own-draft-PR-with-the-plain-create-form-and-mark-it-ready-when-CI-is-green(no-other-gh-write:comment,review,edit-still-prompt);a-task-file-review-round-follows-your-start,its-findings-arrive-as-amendment-1 read_at=read",
    "AGMSG-PING v1 task_id=dotfiles-T129-hcom-dispatch-bus-a01 reason=STOP:the-user-s-instruction-of-08:51-JST(relayed-by-the-operator):stop-all-work-now;keep-what-you-changed-on-your-branch-or-in-your-files(a-local-commit-is-fine;no-push,no-PR-create,no-gh-write,no-further-edit);reply-PONG-status=alive-with-your-state(branch,head-or-uncommitted-files,what-was-in-progress);then-wait-for-a-new-TASK-or-PING;the-orchestrator-is-re-planning-and-nothing-runs-until-the-user-agrees read_at=unread"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "searches": [],
  "task": "dotfiles-T129-hcom-dispatch-bus-a01"
}
---
# Acceptance record: dotfiles-T129-hcom-dispatch-bus-a01

Plan 023 PR C stage 1 (hcom-dispatch and the bus readers), dispatched 2026-10-17T23:4xZ to a008 (worker-f) on the operator's instruction of 08:4x JST; task sha256 1fed5061… (presend: checker OK, six premises OK, masked 0). Starts from origin/main now; rebases after #390 merges (its worker finished; D-D-overlap-394 reading). A task-file review round runs after the dispatch; its findings travel as amendment 1.

- record created before the first dispatch (Orchestrator Playbook step 6).
- 2026-10-18T04:25Z parked under plan 024 0b: a008 pushed `tools/hcom-dispatch-bus-a01` at dfa9001b and opened draft PR #407; PONG `parked-draft-pr-407-head-dfa9001b…` received 04:25:27Z. Resumes in phase 2 D-W0 after amendment 1.

## Reset to a02 (2026-10-22T04:44Z, D-024-81)

text-security:24d8b8d:1	env-selected-executable
text-security:24d8b8d:2	store-identity
text-security:24d8b8d:3	consumed-bytes-binding
text-security:24d8b8d:4	record-path-containment
text-security:24d8b8d:5	gh-host-binding
text-security:24d8b8d:6	history-format-contract
text-security:24d8b8d:7	protocol-key-mismatch
- 2026-10-22T04:44Z: resumed from the 2026-10-18 parking: amendment 1 re-anchored the text to main d06d94fd (premises and line anchors re-verified, after: satisfied by #423, generated Checks); C-80 of 24d8b8d Verdict incorrect, five P1 and two P2 (the text predates design 5.14 items 2 and 9: env-selected BUS_HISTORY, unauthenticated HCOM_DIR store, byte comparison not bound at execution, record path containment, gh host binding; TSV history incompatible with the marker parsers; verdict= instead of status=). Reset as dotfiles-T129-hcom-dispatch-bus-a02 with brief .agents/worklog/orchestrator-glue/brief-hcom-dispatch-bus-a02.md (after: gh-binding a02); author-loop next; PR #407 continues under a02.

**Reviewing lint baseline tests and task constraints**
**Examining unittest module structure and platform constraints**
exec
/bin/zsh -lc "rg -n 'class LintComparisonsTest|def test_the_changed_files_are_clean_against_the_baseline' tests/unit/test_lint_comparisons.py; sed -n '1,110p' tests/unit/test_lint_comparisons.py; sed -n '133,140p' .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md; cat .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-e9ce1c3.md.last.md; rg -c '"'^  - '"\\{control:' .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md; sed -n '1,75p' ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 44ms:
104:class LintComparisonsTest(unittest.TestCase):
322:    def test_the_changed_files_are_clean_against_the_baseline(self):
"""Exercise scripts/lint-comparisons.py (C-61 rule 6; plan 023 PR F2): the rule table on fixture files in a temporary
directory, the content-hashed baseline and its changed-file severity, and the files this checkout changes against the
committed baseline.

The lint runs as a subprocess (`python3 -I`), so nothing of it is imported here.
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINT = ROOT / "scripts/lint-comparisons.py"
# plan 024 5.14 item 2: env -i, a system git by its absolute path, an explicit -C, no system or global config
GIT_ENV = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
GIT_C = ("core.hooksPath=/dev/null", "core.fsmonitor=false", "protocol.allow=never", "protocol.https.allow=always")
GIT_C += ("core.attributesFile=/dev/null", "core.sshCommand=false")
SHELL_NORMALISERS = {
    "realpath": '[[ "$(realpath "$path")" == */x ]]\n',
    "pwd -P": '[[ "$(cd "$dir" && pwd -P)" == */x ]]\n',
    "cd -P": '[[ "$(cd -P "$dir" && pwd)" == */x ]]\n',
    "readlink -f": '[[ "$(readlink -f "$path")" == */x ]]\n',
    "python3 -I -c os.path.realpath": '[[ "$(python3 -I -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$path")" == */x ]]\n',
    "python3 -I -c os.path.normpath": '[[ "$(python3 -I -c "import os, sys; print(os.path.normpath(sys.argv[1]))" "$path")" == */x ]]\n',
    "python3 -I -c urllib.parse": '[[ "$(python3 -I -c "import sys, urllib.parse; print(urllib.parse.unquote(sys.argv[1]))" "$url")" == */x ]]\n',
    "canonical_path": '[[ "$(canonical_path "$path")" == */x ]]\n',
    "normalise_*": '[[ "$(normalise_path "$path")" == */x ]]\n',
    "normalize_*": '[[ "$(normalize_path "$path")" == */x ]]\n',
}
# rule id -> (fixture file name, the refused fixture of the rule table, one accepted form per normaliser of its row)
TABLE = {
    "R0": (
        "r0.sh",
        "[[ $a == $b ]] # lint-comparisons: allow\n",
        {"a reason": "[[ $path == /x ]] # lint-comparisons: allow the fixture\n"},
    ),
    "R1": ("r1.sh", "[[ $path == */x ]]\n", SHELL_NORMALISERS),
    "R2": (
        "r2.sh",
        'case "$url" in file://*) ;; esac\n',
        {
            name: form.replace("[[ ", "case ").replace('" == */x ]]', '/x" in /*) ;; esac')
            for name, form in SHELL_NORMALISERS.items()
        },
    ),
    "R3": (
        "r3.sh",
        "jq -r 'select(.url | endswith(\"/index.html\"))'\n",
        {
            "def canonical_path": "jq -r 'def canonical_path: ascii_downcase; select((.url | canonical_path) == ($p | canonical_path))'\n",
            "def normalise_*": "jq -r 'def normalise_url: ascii_downcase; select((.url | normalise_url) == ($p | normalise_url))'\n",
            "def normalize_*": "jq -r 'def normalize_url: ascii_downcase; select((.url | normalize_url) == ($p | normalize_url))'\n",
        },
    ),
    "R4": (
        "r4.py",
        'if path == "/x":\n    pass\n',
        {
            "os.path.realpath": 'if os.path.realpath(path) == "/x":\n    pass\n',
            "os.path.normpath": 'if os.path.normpath(path) == "/x":\n    pass\n',
            "os.path.abspath": 'if os.path.abspath(path) == "/x":\n    pass\n',
            "Path(...).resolve": 'if Path(path).resolve() == Path("/x"):\n    pass\n',
            "pathlib.Path(...).resolve": 'if pathlib.Path(path).resolve() == Path("/x"):\n    pass\n',
            "urllib.parse.urlsplit": 'if urllib.parse.urlsplit(url).path == "/x":\n    pass\n',
            "urlparse": 'if urlparse(url).path == "/x":\n    pass\n',
            "unquote": 'if unquote(url) == "/x":\n    pass\n',
            "canonical_path": 'if canonical_path(path) == "/x":\n    pass\n',
            "normalise_*": 'if normalise_path(path) == "/x":\n    pass\n',
            "normalize_*": 'if normalize_path(path) == "/x":\n    pass\n',
            "os.path.samefile": 'if os.path.samefile(path, "/x"):\n    pass\n',
        },
    ),
    "R5": (
        "r5.sh",
        "ps -axo pid,command | grep claude\n",
        {"ps -o <fields>= -p <pid>": 'ps -o args= -p "$pid"\n', "pgrep -x <name>": "pgrep -x omp\n"},
    ),
    "R6": (
        "r6.sh",
        'grep -E "^(${ids})\\t"\n',
        {"grep -F": 'grep -F "${ids}"\n', "escape_regex": 'grep -E "^($(escape_regex "$ids"))\\t"\n'},
    ),
}
PYTHON_R6 = ("r6.py", 're.search(f"^{name}$", text)\n', {"re.escape": 're.search(f"^{re.escape(name)}$", text)\n'})
# forms beyond the table's fixtures that the lint also refuses: the test word not first on its line, a jq program inside
# a double-quoted substitution, ps inside a substitution or after if, a jq normaliser applied to one side only
MORE_REFUSED = {
    "R1": ('if [[ "$path" == */x ]]; then :; fi\n', 'x=1 && [ "$1" = "$2/" ]\n'),
    "R2": ('while :; do case "$url" in file://*) ;; esac; done\n',),
    "R3": (
        'x="$(printf %s "$j" | jq -r \'select(.url == $u)\')"\n',
        "jq -r 'def canonical_path: .; select((.url | canonical_path) == $path)'\n",
    ),
    "R5": ("x=$(ps -axo pid,command | grep claude)\n", "if ps -axo pid,command | grep -q claude; then :; fi\n"),
}


class LintComparisonsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()

    def lint(self, *args, cwd=None):

```text
observed 2026-10-22T05:39Z by the orchestrator (sandboxed Bash); every executable below is absolute and every command runs under the enumerated environment printed with it
canonical main: clone (gh-free): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home /Library/Developer/CommandLineTools/usr/bin/git -c http.proxyAuthMethod=basic -c credential.http://localhost:49680.helper= clone -q --bare https://github.com/mryfmo/dotfiles.git <private>/dotfiles.git ` -> `` (exit 0)
canonical main: ref: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git rev-parse refs/heads/main ` -> `d06d94fd8eedcd0770c1c80c2b1596ec36109ef8` (exit 0)
canonical main: remote: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git config --get remote.origin.url ` -> `https://github.com/mryfmo/dotfiles.git` (exit 0)
canonical main: config origins: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /Library/Developer/CommandLineTools/usr/bin/git config --list --show-origin ` -> `file:<private>/dotfiles.git/config	core.repositoryformatversion=0 file:<private>/dotfiles.git/config	core.filemode=true file:<private>/dotfiles.git/config	core.bare=true file:<private>/dotfiles.git/config	core.ignorecase=true file:<private>/dotfiles.git/config	core.precomposeunicode=true file:<private>/dotfiles.git/config	remote.origin.url=https://github.com/mryfmo/dotfiles.git` (exit 0)
design file (canonical main): `/usr/bin/env -i PATH=/usr/bin:/bin HOME=~ TMPDIR=/tmp/claude-501 UV_CACHE_DIR=<private>/uv-cache HTTPS_PROXY=<sandbox proxy> https_proxy=<sandbox proxy> NO_PROXY=<local ranges> GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 HOME=<private>/home GIT_DIR=<private>/dotfiles.git /bin/sh -c exec\ /Library/Developer/CommandLineTools/usr/bin/git\ show\ refs/heads/main:.orchestration/plans/024-design-quality.md\ \>\ <private>/design.md ` -> `` (exit 0)
No P0–P3 findings in task SHA-256 `e9ce1c3b2b165111b944b346b1891aa2dac246a2b952737b0638160f77eb25c1`.

Reviewed all 42 threat rows, the incorporated execution contract, cited acceptance records and reviews. The corrected lint selector exists. The design requires executable and consumed-byte binding, resolved-path/case-alias checks, isolated descendants and sanitized Git environments. Authenticated use remains conditional on measured parent and deployment protections.

📝 まとめ: Completed the read-only design review and independent cross-check; no files changed.

Not checked: implementation, CI or live Linux execution; same-UID replacement and credential separation remain declared residual risks.
Verdict: correct44
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


**Completing final verification**
**Finalizing security review summary**
codex
No P0–P3 findings across the 44 threat rows in task SHA-256 `05000f451d9fc1ed38d962e9e863724793dea281330b2c21fd578af5bca35ee6`.

The stated controls cover executable selection, inherited Git environments, symlink/case handling, consumed-byte binding and receipt identity. The added lint selector exists. Operational use remains conditional on T133 and deployment measurements; same-UID isolation is explicitly unclaimed.

📝 まとめ: Completed the read-only design review against the cited acceptance records and reviews; no files changed.

Not checked: implementation, CI or live Linux/race execution; same-UID replacement and credential separation remain declared residual risks.
Verdict: correct
hook: Stop
hook: Stop Completed
tokens used
79,367
No P0–P3 findings across the 44 threat rows in task SHA-256 `05000f451d9fc1ed38d962e9e863724793dea281330b2c21fd578af5bca35ee6`.

The stated controls cover executable selection, inherited Git environments, symlink/case handling, consumed-byte binding and receipt identity. The added lint selector exists. Operational use remains conditional on T133 and deployment measurements; same-UID isolation is explicitly unclaimed.

📝 まとめ: Completed the read-only design review against the cited acceptance records and reviews; no files changed.

Not checked: implementation, CI or live Linux/race execution; same-UID replacement and credential separation remain declared residual risks.
Verdict: correct
