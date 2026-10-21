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
session id: 01a159b2-3a72-7ce2-8c25-c7c11afa45f3
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
タスク本文と参照先の acceptance・review を読み、各 threat row の対策が実際の実行対象を拘束できるか確認します。agmsg-orchestration と Ponytail の手順を参照し、読み取り専用で進めます。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 13ms:
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
/bin/zsh -lc 'git status --short
nl -ba .orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md' in ~/Workspace/dotfiles
 succeeded in 12ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/acceptance/dotfiles-T133-loop-limits-a01.md
 M .orchestration/acceptance/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
 M .orchestration/acceptance/dotfiles-T133-result-precheck-a01.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-design-quality.md
 M .orchestration/plans/024-progress.tsv
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a06.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-34cc889.log
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-crit.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-review-receipt.md
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a04-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a05-pr-feedback.json
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
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a06.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a02.md
?? .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a02.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md
?? .orchestration/acceptance/dotfiles-T133-result-evidence-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/
?? .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/
?? .orchestration/dotfiles-T133-worker-write-boundary-a01-redesign-review-a01/
?? .orchestration/dotfiles-T133-worker-write-boundary-a02-redesign-review-a01/
?? .orchestration/learning/mistakes/M-20261020-01-amendment-note-reproduces-refused-string.md
?? .orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md
?? .orchestration/learning/mistakes/M-20261020-03-dispatch-after-failed-script.md
?? .orchestration/learning/mistakes/M-20261020-04-result-claims-against-own-counts.md
?? .orchestration/learning/mistakes/M-20261020-05-ledger-ids-collide-across-kinds.md
?? .orchestration/learning/mistakes/M-20261020-06-new-task-id-collided-with-a-lineage.md
?? .orchestration/learning/mistakes/M-20261020-07-chain-under-a-superseded-task-id.md
?? .orchestration/learning/mistakes/M-20261020-08-dispatch-after-refused-pre-send.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a02.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a02.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-af86233.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-local-review-af86233.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-chain-a644a7d.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-chain-dbc8b67.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-chain-fea3843.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-crit.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-local-review-a644a7d.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-local-review-dbc8b67.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-review-receipt.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-23f5144.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-23f5144.md.last.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-audit-6434c27.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-audit-6434c27.md.last.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-audit-7eab146.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-audit-7eab146.md.last.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-chain-222b616.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-chain-6434c27.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-chain-7eab146.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-crit.json
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-local-review-222b616.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-local-review-6434c27.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-local-review-7eab146.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-review-receipt.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-chain-09e2e95.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-chain-11584e1.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-chain-9ce253f.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-chain-d067910.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-local-review-09e2e95.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-local-review-d067910.md
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
?? .orchestration/validation/dotfiles-T133-python-pin-a02-audit-1327740.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-audit-1327740.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-chain-1327740.log
?? .orchestration/validation/dotfiles-T133-python-pin-a02-crit.json
?? .orchestration/validation/dotfiles-T133-python-pin-a02-local-review-1327740.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-python-pin-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-security-1327740.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-security-1327740.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-d899b84.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-d899b84.md.last.md
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
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-07cdcee.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-07cdcee.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-3accc7b.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-3accc7b.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-c14b967.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-c14b967.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-chain-07cdcee.log
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-chain-3accc7b.log
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-chain-c14b967.log
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-crit.json
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-local-review-07cdcee.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-local-review-3accc7b.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-local-review-c14b967.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-2c8c05a.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-eaf8c47.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-eaf8c47.md.last.md
?? .orchestration/validation/dotfiles-T133-result-evidence-check-a01-text-security-72882ac.md
?? .orchestration/validation/dotfiles-T133-result-evidence-check-a01-text-security-72882ac.md.last.md
?? .orchestration/validation/dotfiles-T133-result-evidence-check-a01-text-security-99c37ca.md
?? .orchestration/validation/dotfiles-T133-result-evidence-check-a01-text-security-99c37ca.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-7a201ea.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-e68fb33.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-local-review-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-06ffefb.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-06ffefb.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-cedc7f5.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-cedc7f5.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-21f52c7.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-2cb5848.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-21f52c7.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-b8bf806.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-b8bf806.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-4a49ed9.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-4a49ed9.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-73ac933.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-73ac933.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-b9e04cb.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-b9e04cb.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-a561e64.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-a561e64.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-25dd01e.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-9545e59.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-a2f4744.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-a561e64.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-b3c5076.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-a561e64.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-b3c5076.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a01-text-security-2116a65.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a01-text-security-2116a65.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a01-text-security-232c174.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a01-text-security-232c174.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-6f95aef.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-6f95aef.md.last.md
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
?? .orchestration/validation/records-sync-28-pr-feedback.json
?? .orchestration/validation/records-sync-29-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-regime-ci-token-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - .github/workflows/regime.yml
     8	  - scripts/orchestrator/regime-ci.py
     9	  - tests/unit/test_regime_ci.py
    10	  - .orchestration/dotfiles-T133-regime-ci-token-a01/**
    11	after: []
    12	threat_table:
    13	  - {control: ".github/workflows/regime.yml", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_the_regime_workflow_runs_base_code_only"}
    14	  - {control: "scripts/orchestrator/regime-ci.py", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_forwards_only_parent_tokens"}
    15	  - {control: "tests/unit/test_regime_ci.py", disposition: "residual: Final-head CI and the independent task audit compare fixture assertions with production behavior; tests supply no approval authority."}
    16	  - {control: ".orchestration/dotfiles-T133-regime-ci-token-a01/**", disposition: "residual: These untrusted artifacts contain only this task's copy and evidence; no executable helper or credential is stored here."}
    17	  - {control: "the task copy .orchestration/dotfiles-T133-regime-ci-token-a01/task.md", disposition: "residual: The orchestrator compares every byte and SHA256 with the dispatched text before acceptance."}
    18	  - {control: "the evidence records under .orchestration/dotfiles-T133-regime-ci-token-a01/**", disposition: "residual: The audit compares reported commands, red/green outcomes, cap totals and CI with the final head; token values are excluded from evidence."}
    19	  - {control: "task metadata (kind, security, allowed_files, after, threat_table, premises)", disposition: "residual: The consistency checker validates the front matter before dispatch and acceptance; whole-file comparison detects changed metadata."}
    20	  - {control: "metadata separators", disposition: "residual: YAML parsing and the dispatched whole-file digest cover separators in the task copy; evidence remains untrusted data."}
    21	  - {control: "in-process effects", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_keeps_tokens_out_of_argv_and_output"}
    22	  - {control: "workflow and interpreter or environment inputs: checker-child environment only", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_forwards_only_parent_tokens"}
    23	  - {control: "regime-ci CHECKER_RUN executable selection of uv and python", disposition: "residual: Executable selection, including PATH and virtual-environment discovery, is outside this task and owned by dotfiles-T133-regime-ci-token-followup-a01."}
    24	  - {control: "GH_TOKEN and GITHUB_TOKEN authority", disposition: "residual: The workflow's GITHUB_TOKEN under permissions: contents: read can read public repository contents only. A token supplied by any other caller carries that caller's authority; this task neither widens nor narrows it. The checker forwards, never mints, tokens."}
    25	  - {control: "new or renamed scripts", disposition: "residual: No script is added or renamed; retain the existing verifier, checker command and isolated interpreter setup."}
    26	  - {control: "orchestrator effect merge", disposition: "residual: Only the orchestrator integrates under Playbook step 10, binding the merge to the audited full head after the gate; the worker never merges."}
    27	  - {control: "orchestrator effect update-branch", disposition: "residual: A changed head requires fresh applicable CI, feedback and audit evidence under Playbook step 10 before integration."}
    28	  - {control: "orchestrator effect forced worker removal", disposition: "residual: None planned; removal refuses dirty state without force, and the orchestrator records any discarded state in acceptance."}
    29	  - {control: "5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: This token handoff establishes neither same-UID isolation nor separation of worker and orchestrator GitHub credentials."}
    30	  - {control: "5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: This Claude seat uses its deployed sandbox; this slice changes no host boundary or managed settings and proves no deployment isolation."}
    31	  - {control: "5.14 item 2: 無害化した環境を最初に", disposition: "residual: Tests close only the checker-child allowlist; existing parent execution and PATH selection remain unchanged and are not claimed sanitized."}
    32	  - {control: "5.14 item 3: 信頼パスの境界検査", disposition: "residual: Existing base-checkout and trusted-path checks remain unchanged; this task adds no protection against concurrent same-UID replacement."}
    33	  - {control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: regime-ci's git reads inherit GIT_DIR; dotfiles-T133-regime-ci-token-followup-a01 owns binding those reads to the checker execution tree."}
    34	  - {control: "5.14 item 5: 出力と予約の同一性", disposition: "residual: Evidence and RESULT identify the full head; this change adds no lock, reservation or physical execution slot."}
    35	  - {control: "5.14 item 6: 正直な残余", disposition: "residual: Report fixture observations separately from hosted-runner evidence; parent startup, shared caches and same-UID access remain residual risks."}
    36	  - {control: "5.14 item 7: 検証", disposition: "residual: Named red/green tests cover this handoff; retain existing security regressions and disclose unexecuted checks without claiming full contract closure."}
    37	  - {control: "5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: The unchanged checker owns canonical-main API reads; token availability supplies authentication, never approval authority from local records."}
    38	  - {control: "5.14 item 9: 私設キャッシュ", disposition: "residual: Preserve existing UV_CACHE_DIR handling and no-config isolated execution; this task neither provisions nor authenticates a private cache."}
    39	  - {control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Claude worker seats run inside their sandbox except the manifest's remaining excludedCommands: agmsg-dispatch *; on Linux also gh *, herdr-agents * and actas-claim.sh *. dotfiles-T133-worker-sandbox-exclusions-a02 owns their removal under design 5.14 item 10. This task's git, uv, python and ruff commands are not excluded and run inside the sandbox; the deployed settings keep `failIfUnavailable: false`, so a missing sandbox dependency would run them unsandboxed, a residual of the Claude settings owned by design 5.14 item 10's lineage; a refusal is reported as AGMSG-PONG v1 status=blocked."}
    40	premises:
    41	  - claim: The reviewed checker head resolves locally; this identifies the review input, not canonical GitHub authority.
    42	    command: |-
    43	      git rev-parse 2cb58482
    44	    output: |-
    45	      2cb584823ccf5f22069ea925b252d8cefb020844
    46	  - claim: The current workflow already declares read-only contents permission.
    47	    command: |-
    48	      grep -c 'contents: read' .github/workflows/regime.yml
    49	    output: |-
    50	      1
    51	  - claim: The existing uv-configuration regression test is present.
    52	    command: |-
    53	      grep -c test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config tests/unit/test_regime_ci.py
    54	    output: |-
    55	      1
    56	---
    57	
    58	# AGMSG-TASK dotfiles-T133-regime-ci-token-a01 — authenticate the regime checker's read-only API requests
    59	
    60	Amendment 1 addresses C-80 round 1 (`text-security:c32513e:1-5`); previous_sha256: c32513e5cbf65661a7a5d2f385dd814f6735d9ddaa1495b03da47db2f9c71335.
    61	
    62	Operator premise: PR #440, head 2cb58482, lineage dotfiles-T133-task-generator-plan-check-a06-checker, is merging next; its checker forwards parent GH_TOKEN/GITHUB_TOKEN only to gh api, including canonical-main SHA, C6/C15 design bytes and C8/C9 lookups. A fresh hosted runner has no gh login: missing authentication exits 4 and regime-ci reports no verdict. The local review found this P1 caller defect outside #440's allowed_files; fix it before regime becomes a required check.
    63	
    64	Design 5.14 (.orchestration/plans/024-design-quality.md), frozen by D-024-29, applies by reference under D-024-30; rely on items 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 and 10.
    65	
    66	## Item 1
    67	
    68	Add `GH_TOKEN: ${{ github.token }}` to the regime-ci step's env in .github/workflows/regime.yml; retain `permissions: {contents: read}` and base-only execution. This workflow edit is authorized because the workflow is this task's subject; do not activate a ruleset or widen permissions.
    69	
    70	In scripts/orchestrator/regime-ci.py extend the checker's minimal environment (HOME, PATH, LANG, UV_CACHE_DIR) with GH_TOKEN and GITHUB_TOKEN only when each key exists in regime-ci's own environment, preserving its value. Keep every other inherited variable out; do not copy the whole parent environment, synthesize credentials, put tokens in argv or print them. Keep the checker and its launch arguments unchanged.
    71	
    72	In tests/unit/test_regime_ci.py add RegimeCiTest.test_regime_ci_forwards_only_parent_tokens: clear both ambient token keys, exercise neither, each alone and both with synthetic values, and assert the exact child environment, including exclusion of unrelated parent variables. Add RegimeCiTest.test_regime_ci_keeps_tokens_out_of_argv_and_output to assert neither synthetic token occurs in captured subprocess argv or regime-ci stdout/stderr, covering normal verdict and no-verdict diagnostics. Both new methods assert expected token presence in the child, so dropping credentials cannot satisfy secrecy assertions. Use existing fixtures and targeted subprocess capture or a fake checker; no live API or login. These environment and secrecy tests close only “GH_TOKEN reaches the checker's environment exactly when regime-ci's environment holds it, and never appears in argv or output”; CHECKER_RUN executable selection remains with the follow-up named in the threat table.
    73	
    74	Update test_the_regime_workflow_runs_base_code_only's exact env assertion for the new token entry while retaining its permissions and base-only checks. Keep test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config green and unittest.main() at the module end. Write and run tests before implementation: every new behavior must be red before its production change and green after; name each outcome in report.md and distinguish existing passing regressions.
    75	
    76	## Check
    77	
    78	Measured deployment for Worker Playbook step 4: Claude worker seats run inside their sandbox except the commands the manifest's excludedCommands still lists: `agmsg-dispatch *`, and on Linux `gh *`, `herdr-agents *`, `actas-claim.sh *`. Design 5.14 item 10's own task, dotfiles-T133-worker-sandbox-exclusions-a02, removes these exclusions. This task's git, uv, python and ruff commands are not excluded and run inside the sandbox. Record a refusal in sandbox.md and send `AGMSG-PONG v1 status=blocked` with the command and boundary; never retry outside.
    79	
    80	Resolve uv once with `UV_DIR="$(dirname "$(env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv)")"` and paste the command and its output into report.md. The result is the absolute, non-shim directory that holds the uv binary mise installed (on this host `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/`); do not assume a `bin` subdirectory and read no pin file: the version is whatever mise resolves for this checkout, and the pasted path is the evidence.
    81	
    82	Run before implementation and after: `/usr/bin/env -i PATH="$UV_DIR:/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py`, substituting the pinned version and using that same resolved absolute uv directory for both runs.
    83	
    84	Run `ruff check --config ruff.toml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py` and `ruff format --config ruff.toml --check scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py`. Paste commands, exit statuses and verbatim output without credential values into validation.md. Caps: at most 25 changed lines outside `tests/` and `.orchestration/`, and at most 60 under `tests/`.
    85	
    86	Measure summed additions plus deletions with `git diff --numstat <base40>...<head40>`; base40 is pasted at dispatch and head40 comes from RESULT. This whole task text, including the orchestrator's Checks block, stays at or under 125 lines.
    87	
    88	Do not run Bats locally. After the final push verify GitHub Actions for the exact final head with `gh pr checks <pr> --repo mryfmo/dotfiles --watch`, fix in-scope failures and repeat before RESULT; follow Worker Playbook step 15 for the bounded Bot wait and findings. Before completion run `make require-crit-review`; if required, follow AGENTS.md's crit-data evidence and receipt procedure with worker evidence under this task's allowed directory, without a browser review.
    89	
    90	## Completion
    91	
    92	Fetch current origin/main inside the sandbox and create a fresh branch with `git switch -c ci/regime-ci-token-a01 --no-track origin/main`. Save .orchestration/dotfiles-T133-regime-ci-token-a01/task.md byte-identical to the dispatched text. Under that directory commit report.md (implementation, named red/green outcomes, residuals, cost), validation.md (commands/output and both cap totals), sandbox.md, learning.md and autoskill.md (used or not-used); do not commit plan/todo/learn worklogs. Add no runtime helpers or changes outside allowed_files.
    93	
    94	Push with `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u https://github.com/mryfmo/dotfiles.git <branch>` and open with `gh pr create --repo mryfmo/dotfiles` using an English title and body.
    95	
    96	After final-head checks pass, send `AGMSG-RESULT v1 task_id=dotfiles-T133-regime-ci-token-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with artifact paths; no worker merge. Report skipped checks and remaining risks, including unchanged parent startup and cache behavior.
    97	
    98	## Checks (pasted by the orchestrator before each send)
    99	
   100	```
   101	```
   102	
   103	Author verification: Implementation, tests and live sandbox behavior were not checked for this text-only amendment; executable selection, GIT_DIR inheritance and sandbox exclusions remain with their named follow-ups.
**Reviewing existing evidence and diffs**
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md.last.md .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '5\\.14|D-024-(21|29|30)' .orchestration/plans/024-design-quality.md .orchestration/decisions.tsv
cat .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-21f52c7.md .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-2c8c05a.md .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md.last.md .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-eaf8c47.md.last.md
nl -ba scripts/orchestrator/regime-ci.py
cat .github/workflows/regime.yml' in ~/Workspace/dotfiles
 succeeded in 84ms:
# Acceptance record: dotfiles-T133-regime-ci-token-a01

Lineage: the regime workflow passes `GH_TOKEN: ${{ github.token }}` and regime-ci.py forwards it into the checker's minimal environment, so the a06 checker's new `gh api` requests (PR #440, head 2cb58482/21f52c79) get a verdict in CI. Caller-side dependency found by the local review of #440 (local:21f52c7:1); #440 waits for this lineage. Security: true (a CI workflow).

- 2026-10-20T13:27Z-13:36Z: text written whole by the review profile from the orchestrator's brief (`regime-ci-token-a01-prompt.md`); installed, 95 lines, self cap 110; pre-send OK (checker OK, secret-pattern 0, no literal home path, id free), sha256 c32513e5cbf65661a7a5d2f385dd814f6735d9ddaa1495b03da47db2f9c71335. C-80 round 1 started 13:37Z.

## Owned by dotfiles-T133-regime-ci-token-followup-a01

(no advisory rows yet; written 2026-10-20T14:17Z before the regime-ci-token PR's first advisory disposition, C-51; the owner text carries the lineage's residual rows as items)

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:38](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:38) — “Every command inside its sandbox” is not enforced: the manifest still excludes Linux `gh *` and `agmsg-dispatch *`, and the exclusions-removal acceptance records deployment as pending; excluded commands run outside immediately, so “stop on refusal” never activates. [Sandbox semantics](https://code.claude.com/docs/en/sandboxing#run-commands-outside-the-sandbox-with-excludedcommands).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:22](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:22) — The environment-dictionary test cannot close executable selection: unchanged `CHECKER_RUN` resolves `uv` through this host’s mise-first PATH and does not pin Python, so credentials reach the selected launcher/interpreter before checker validation; `--no-project` still permits discovery of a local or parent virtual environment. [uv semantics](https://docs.astral.sh/uv/reference/cli/#uv-run--no-project).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:32](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:32) — Retained “base-only execution” is not bound on this host: regime-ci’s Git reads inherit `GIT_DIR`, while execution opens the checker beneath `root`; a read-only probe returned this repository’s HEAD from `/tmp`, demonstrating that the HEAD decision need not identify the executed filesystem tree, even without a symlink race. [Git environment semantics](https://git-scm.com/docs/git#Documentation/git.txt-GITDIR).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:23](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:23) — Workflow `contents: read` constrains its generated token, not arbitrary parent `GH_TOKEN`/`GITHUB_TOKEN` values preserved by line 67; a local write-capable credential retains that authority, so this residual does not establish the claimed absence of write or merge authority. [Token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token#modifying-the-permissions-for-the-github_token).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:77](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:77) — The prescribed clean PATH omits uv, which existing fixtures launch by name; invoking the named workflow test under that environment reproduced `FileNotFoundError: 'uv'`, preventing the required green validation independently of implementation correctness.

📝 まとめ: Reviewed the text, every threat row, and related records without modifying files; full suites and live Linux sandbox behavior were not tested, and the execution-binding risks above remain unresolved.
Verdict: incorrect---
format: 2
task_id: dotfiles-T133-regime-ci-token-followup-a01
kind: code
security: false
allowed_files:
  - scripts/orchestrator/regime-ci.py
  - tests/unit/test_regime_ci.py
  - .orchestration/dotfiles-T133-regime-ci-token-followup-a01/**
after: [dotfiles-T133-regime-ci-token-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/regime-ci.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_regime_ci.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-regime-ci-token-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T133-regime-ci-token-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
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

# AGMSG-TASK dotfiles-T133-regime-ci-token-followup-a01 — the regime CI token lineage's owner task (advisory P2 of the regime-ci-token PR)

Written 2026-10-20 by the orchestrator seat before the first advisory disposition of the regime-ci-token PR (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T133-regime-ci-token-followup-a01` in `.orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md` (plan 020 step 1.2); it is dispatched after the regime-ci-token PR merges, to a seat the orchestrator names, and only when that section holds at least one row (C-102).

## Item 1

Each owned row (any advisory P2 of the local review or the task-level audit of the regime-ci-token PR's final head, and any Bot P2 the orchestrator records under this owner; rows are read from the record at dispatch; a records-only row is realised by the record it names, with no test) gets its fix and, where the row names a test or code, one red-then-green test in `tests/unit/test_regime_ci.py`, named in report.md against the row id. Nothing outside the owned rows; any other file joins `allowed_files` only by an amendment that names the row needing it.

## Item 2

The residual rows of `dotfiles-T133-regime-ci-token-a01` that name this owner: (a) regime-ci.py's `CHECKER_RUN` resolves `uv` and the interpreter through PATH; the owner binds them to the mise install directories named in the manifest, with a test that a PATH holding a decoy `uv` first is not used; (b) regime-ci.py's git reads inherit `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`; the owner clears them for every git child (`env -u`), with a test that a hostile `GIT_DIR` does not redirect the base read. Each row gets one red-then-green test in `tests/unit/test_regime_ci.py`.

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md` apply as written, with `dotfiles-T133-regime-ci-token-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-regime-ci-token-followup-a01/task.md>` in the RESULT. Design 5.14 applies by reference (D-024-30).

## Checks (pasted by the orchestrator before each send)

```
```

 succeeded in 149ms:
.orchestration/plans/024-design-quality.md:95:### 5.14 残余（凍結後の計測事実、D-024-29）
.orchestration/plans/024-design-quality.md:103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
.orchestration/plans/024-design-quality.md:113:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
.orchestration/decisions.tsv:64:D-024-18	2026-10-19T02:5xZ	every security: true orchestrator-side task text applies design section 5.14 (trusted-host execution contract: the write-boundary premise, sanitized environment first, trusted-path boundary checks, execute-what-you-verified, 40-hex identities and inode-bound locks, honest residuals, four shared red-then-green tests) by reference, with one threat row per item	the C-80 reviews of three texts on 2026-10-19 (permission-guard-gate-a05, dispositions-a02, audit-pool-a01: 19 P1 in total) found the same unstated premise and the same gaps in each; a design-tier contract replaces per-text rewording (M-20261019-03 class)	default under the autonomy directive, reported 2026-10-19 12:0x JST; scope=design	applied-from-a05-and-the-a02-texts
.orchestration/decisions.tsv:65:D-024-19	2026-10-19T03:0xZ	permission decision rows are read from the committed ledger (git show origin/main:.orchestration/decisions.tsv after fetch), never from the working copy; a working-copy row is a proposal until the records PR carrying it merges, and that PR approval is the operator's operation (design 5.14 item 8)	the second C-80 review of the a05 text: a Claude worker seat's file tools run outside the Seatbelt sandbox and the rendered policy has no path deny, so a same-UID forged row in the working-copy ledger was possible; the committed ledger moves forgery behind a protected-branch merge	default under the autonomy directive, reported 2026-10-19 12:0x JST; the consequence is one records PR (boundary 24) before the a05 merge, approved by the operator through the live hook; scope=design,permission	applied-from-a05
.orchestration/decisions.tsv:66:D-024-20	2026-10-19T03:1xZ	P1-15 (the worker write boundary: deny rules for the Claude file tools on every trusted path outside the seat worktree, hooks and MCP locked, per-seat caches, the gh wrapper of D-024-17) is implemented before and as the dispatch prerequisite (after:) of every orchestrator-side security: true task (P1-14 a05, P1-10 a02, audit-pool-a02, P1-6); the orchestrator review worktree moves out of .claude/worktrees/ (design 5.14 item 3)	the C-80 reviews of 2026-10-19 (a05 twice, dispositions-a02 twice, audit-pool-a01) all reduce to the unstated Claude-seat boundary; hardening texts dispatched before it carry false closed rows	default under the autonomy directive, reported 2026-10-19 12:1x JST; scope=design	applied
.orchestration/decisions.tsv:67:D-024-21	2026-10-19T04:0xZ	threat model and mechanism of the worker boundary: the host is not a security boundary between seats sharing one OS user; the hard boundary is GitHub (protected main, required checks, the orchestrator identity merge); approvals and gate evidence of record are read from GitHub at a sha through the API inside the sandbox; Claude worker seats run under their own CLAUDE_CONFIG_DIR (~/.claude-worker: no excluded commands, no Herdr socket, Edit denies on trusted paths with symlink coverage, failIfUnavailable true, minimal trusted hooks with onFailure block); host-local controls target accidental and injected damage and the texts say so (design 5.14 items 0, 1, 8)	three C-80 reviews of the P1-15 text (03:24Z, 03:42Z, 03:58Z) found host-level escapes no in-process check closes (symlink swap race, writable object database, hook descendants through shims, Herdr socket RPC, hook timeout fail-open); the documentation confirms per-directory settings and credentials (one operator login for the worker directory), onFailure block (>= 2.1.295; installed 2.1.300), and symlink-aware file-tool deny rules	default under the autonomy directive, reported 2026-10-19 13:0x JST; the worker-directory login is an operator step at the P1-15 deployment; scope=design,permission	applied-to-the-P1-15-text
.orchestration/decisions.tsv:71:D-024-17a	2026-10-19T06:0xZ	amendment of D-024-17: the wrapper design is dropped (design 5.14 item 10): worker seats run no command outside the sandbox at all (gh inside the sandbox, Codex network inside its sandbox, the permgate codex rule stops approving escapes)	the probe of 03:45Z (gh works inside the sandbox) and the C-80 reviews that showed the wrapper cannot close LD_PRELOAD or argv passthrough	recorded; scope=design	supersedes-the-wrapper-wording
.orchestration/decisions.tsv:75:D-024-27	2026-10-19T21:39Z	An owner task's owned rows are hash-bound in its task text: the text quotes the rows verbatim from the lineage record's `## Owned by <owner>` section (C-88) and the premise `the Owned-by section is on origin/main at dispatch` is replaced by `the quoted rows equal the record's rows at dispatch` (orchestrator-checked, the text sha in the TASK line); dispatch of an owner task no longer waits for the records boundary PR.	18 owner texts carried the on-main premise and every one waited for #429 (the operator's approval) while two Claude seats sat idle on 2026-10-20 05:00-06:40 JST; the rows are scope, not permission approvals, so design 5.14 item 8 (approvals from the committed ledger) does not apply to them; a hash-bound text is the regime's trusted carrier of scope.	plan 024 P1-9 orchestrator load; C-51 owner-first; design 5.14 item 8 scope	applied from 06:40 JST: chain-glue-finish-followup-a01 first; chain-github-scripts-followup-a03 after #432 merges (shared baseline file)
.orchestration/decisions.tsv:77:D-024-29	2026-10-19T21:39Z	Design 5.14 is frozen (plan 006 A1: three review rounds, then freeze with a residual list): items 0-10 are the contract; a text review finding that needs a new design sentence is recorded in the design's residual list and as an owner row, not as an amendment of the item and of the text under review, unless it names a P0/P1 that is exploitable in the proposed implementation.	items 1, 2, 3, 8 and 9 were amended five times on 10-19/20 (one per review round of P1-15 and P1-12), each amendment re-opening the texts that quote the item (C-88) and costing a review round each; the texts chased a moving design.	plan 006 A1; M-20261019-05; C-92	applied from 06:40 JST; the residual list is a new subsection `5.14 残余` in 024-design-quality.md (written at the next design edit)
.orchestration/decisions.tsv:78:D-024-30	2026-10-19T23:16Z	A task text applies design 5.14 by reference: it names the items it relies on (`design: 5.14 items 2, 3, 8, 9`) and carries one threat row per item 0-10 in the item's own words, never a restated or paraphrased copy of the item; C-88 is narrowed to the exact contract sentences a test asserts; the task-consistency check gains a rule (C16) that a security: true orchestrator-side text names 5.14 and has the per-item rows (owner: the P1-12 follow-up after a04 frees task-consistency-check.py).	restated design text drifted in every reset text and re-opened a review round at each design amendment (P1-15: 23 review rounds; P1-12: 4); by-reference texts stay within proposal 1's caps and a mechanical check replaces the reviewer's paraphrase comparison; the operator's direction of 2026-10-19T22:59Z (relayed by a011) asks for the same.	plan 006 A1; D-024-29; M-20261019-05; proposal 1	applied from 08:15 JST to new texts (trusted-exec-contract-tests-a01 first); existing correct texts are not rewritten
.orchestration/decisions.tsv:79:D-024-31	2026-10-20T00:11Z	D-024-28 (an asks-only first slice of P1-14 a05) is withdrawn: the operator's approval D-024-14 binds the three ask-rule removals together with the synchronous hook installation (one digest), so a slice that removes the asks alone is not the approved change and would need its own permission approval from the committed ledger; `make update` therefore stays coupled to the a05 merge, and the idle Claude seats are relieved by converting a seat to Codex (operator step) and by security:false work.	C-80 review 1293d6b of the slice text (2026-10-20T00:04Z): two P1 (replacement control deferred; approval digest covers removals plus hook) that no text amendment can close without a new operator permission approval.	design 5.14 item 8 (approvals from the committed ledger); D-024-13/14; D-024-28; C-80 1293d6b	applied 09:08 JST; the a05 remainder is split later along non-permission lines (proposal 1)
.orchestration/decisions.tsv:81:D-024-33	2026-10-20T03:07Z	Records boundary PR #435 (head 8f7b97690df6060a73959a06fc6622a2beaf5029) is approved by the operator's written instruction in the orchestrator session at 2026-10-20 12:0x JST ("承認するので作業を継続"); the orchestrator merges it with gh pr merge --squash --match-head-commit 8f7b9769… right after PR #431 merges (or at once if #431 fails or resets), so the P1-15 chain and audit already running at edd824ea are not invalidated by a base move.	design 5.14 item 8 makes the operator's approval the authority of the recorded decisions (D-024-25..32); GitHub's ruleset 24397953 has no approval rule (rules: deletion, non_fast_forward, required_status_checks), so the written instruction is the operative approval; sequencing after #431 saves one CI run and one re-audit on the critical path.	design 5.14 item 8; ruleset 24397953; the 11:55 JST report	applied; merge pending #431
.orchestration/decisions.tsv:82:D-024-34	2026-10-20T04:12Z	The files the worker's loader consumes at start and the regime need not preserve are launcher-generated at every start: the global state file `CLAUDE_CONFIG_DIR/.claude.json` is written from the declared shape (empty `mcpServers`, `projects` with exactly the validated identities and Boolean trust, `hasCompletedOnboarding: true`) plus identity fields carried from the previous file after screening (`oauthAccount` string members, `userID`); native persisted state (`numStartups`, onboarding, tips and changelog caches, per-project history, allowedTools, cost counters) is neither screened nor preserved; refusal with a named message stays for declared-structure violations (non-empty top-level `mcpServers`, undeclared project keys, non-Boolean trust flags, undeclared object or array members), as evidence of tampering. `CLAUDE_ENV_FILE` (amendment 1) belongs to the same family. A loader that requires another preserved field blocks and retasks (the text's rule), never widens silently.	a010's probe of the installed loader (2.1.300, sha256 475517ca…; reproduced by the orchestrator at 04:10Z) shows the loader itself writes fields outside any exact schema, so the allowlist re-plan's closed schema (D-024-29/30 lineage, a02 -> a03) refuses the worker's own state at the next start; a per-version native-field table would block every loader update until re-probed; generating the file realises design 5.14 item 1 (refuse any executable payload it did not write) by writing the whole file. Second re-plan of the input-inventory family (rows text-security:f7af699:1, worker:5067ed0:1 after the allowlist re-plan).	design 5.14 item 1; D-024-29; D-024-30; a03 record rows; M-20261019-05	applied 13:12 JST as a03 amendment 2 (review-profile text, C-80 round 3); the operator may redirect it once per class (the 13:15 JST report)
.orchestration/decisions.tsv:83:D-024-35	2026-10-20T04:29Z	The launcher-generated global state file (D-024-34) carries no per-project inventory: `projects` is regenerated empty at every start and the workspace trust of the anchor is established by the launcher's existing acceptance of the trust dialog during spawn's readiness wait (`herdr-agents --add-worker`, SKILL 'Regime activation'), not by pre-generated project keys; sibling worker worktrees that share `CLAUDE_CONFIG_DIR` therefore never reject each other's keys. Refusal with a named message stays for a non-empty top-level `mcpServers` (tamper evidence). A loader needing another preserved field still blocks and retasks.	C-80 round 3 of a03 (efa211d, P2): all Claude workers share `.claude-worker/.claude.json` while S11 accepted only the anchor and the current worktree's keys, so worker B's start would reject worker A's key; enumerating sibling worktrees is the fourth inventory of the family to be found incomplete (2ae9e2c, ebbb71b, c0f50fa1, f7af699, 5067ed0, efa211d), so the inventory is removed rather than extended. Third re-plan of the input-inventory family; the operator may redirect it once per class.	D-024-34; design 5.14 item 1; a03 record rows; SKILL (trust-dialog acceptance)	applied 13:29 JST as a03 amendment 3 (review-profile text, C-80 round 4 under a new re-plan line, C-92)
.orchestration/decisions.tsv:84:D-024-36	2026-10-20T06:34Z	While the Codex seats' sandbox has no network (the rendered manifest's `network_access: false`, enforced since the Codex app-server restart of ~05:21Z), the orchestrator transports a Codex worker's committed head to its PR branch (`git push <url> <sha>:refs/heads/<branch>` over HTTPS from the main checkout, a declared interim-integration exemption; the worker's commits are unchanged and its RESULT names the head), reads CI for the worker, and the chain update-branches as today; Codex workers need no GitHub read (the orchestrator pastes CI state). The manifest value is a design 5.14 item 10 contradiction and gets its own text (Codex-boundary source: a Claude seat) after #431 frees agent-config.yaml; no manual edit of the rendered config (chezmoi-managed; make update deferred to P1-14).	a012 blocked at push (06:31Z) with everything committed; a010 and a013 will hit the same wall; the alternative (edit ~/.codex/standard.config.toml by hand or run make update) is forbidden by the operator's standing orders; transporting bytes the worker committed changes no authorship and keeps the regime's RESULT->chain flow.	design 5.14 item 10; agent-config.yaml:115; a05-checker record 06:31Z; agmsg-orchestration rule (interim manual integration exemption)	applied 2026-10-20 15:34 JST; ends when the manifest task lands and the seats are re-seated
.orchestration/decisions.tsv:85:D-024-37	2026-10-20T06:43Z	New `security: true` mechanism texts are held until the trusted-execution contract (`tests/unit/trusted_exec_contract.py`, PR #436) and the P1-15 launcher (PR #431) are on main; a held text then names those controls by reference (C-88) instead of restating the contract, and takes one C-80 round. Held now: dotfiles-T133-record-json-sync-a01 (two rounds: 1 P1 + 9 P2, all of the trusted-execution family) and dotfiles-T133-records-sync-pr-a01 (round 1: 2 P1 + 2 P2 of the same family; amendment 1 installed, review deferred).	the two texts cost three review rounds in 40 minutes and every finding re-derived the contract the two in-flight PRs land (git configuration isolation, resolved-root binding, replace refs, the agmsg-dispatch exclusion); continuing is the whack-a-mole the operator forbade, while the seats they were meant for (a011, a009) have no other dispatchable text until #438 merges.	C-88; D-024-29/30; M-20261019-05 (text review rounds unbounded); the record-json-sync record	applied 15:43 JST; the Claude seats' idle time until #438 is the operator's approval, not a text gap
.orchestration/decisions.tsv:86:D-024-38	2026-10-20T07:34Z	Records PR #438 (head 041a906b3fc36be5aa7bc18630542127d6efce8c, ten dispatched task texts) is approved by the operator's written instruction in the orchestrator session at 2026-10-20 16:3x JST ("#438は承認したので、そちらで作業を承認したうえですすめること"); merged by the orchestrator with `gh pr merge --squash --match-head-commit 041a906b…` at 07:31:17Z as main f7ed01427a43567b9c1857d2f62953add8b97c92; the dependents (#436, #432, #439, #437, #441) take the new base with `gh pr update-branch` and run their chains; the operator's sentence also delegates the ordinary acceptances of those PRs to the orchestrator's judgement, as the regime already does.	design 5.14 item 8 makes the operator's approval the authority for records PRs (D-024-33); seven PRs were regime-red on the records gap for 4 h 13 min (12:18-16:31 JST).	design 5.14 item 8; D-024-33; the 16:27 JST report	applied 2026-10-20 16:34 JST
.orchestration/decisions.tsv:88:D-024-40	2026-10-20T08:11Z	A records PR that carries only dispatched task texts (each byte-identical to the `task_sha256` of its latest `AGMSG-TASK` message, verifiable from the agmsg store) and no decision, plan, design or rule change is merged by the orchestrator under the final-integration exemption once CI is green, with `--match-head-commit`; a records PR that carries decisions.tsv, plans, design or rule text keeps the operator's written approval (design 5.14 item 8, D-024-33). First application: PR #443 (the a06-checker and pre-send-check texts).	design 5.14 item 8 binds the operator's approval to decision lines read from the committed ledger; a dispatched text is already the orchestrator's act of record on the bus, and regime-ci needs it on main before the worker's PR can pass, so every reset or amendment otherwise waits hours for an approval that adds no information (#438: 4 h 13 min for seven PRs); the operator's instruction of 16:3x JST ("そちらで作業を承認したうえですすめること") delegates the ordinary acceptances to the orchestrator.	design 5.14 item 8; D-024-33; D-024-38; M-20261020-02	applied 17:11 JST; the operator may redirect it (the next report names it)
.orchestration/decisions.tsv:89:D-024-41	2026-10-20T09:22Z	The chain-review-scripts a07 lineage (PR #439) resets to dotfiles-T128-chain-review-scripts-followup-a08 (another context): INV-6 S2 was reached by two amendments, one of them the orchestrator's erroneous resend 2710 (M-20261020-03), and the audit's P1 (review content read from the worker-writable shared object store; design 5.14 item 8) needs a new item: local-review.sh reads the head from a private bare clone fetched from GitHub at the 40-hex sha and runs the review there. The implementation at a644a7d9 stands; the pre-written a08 owner text becomes a09.	the audit of a644a7d9 (09:21Z); C-61 (a third worker round is not available after S2); design 5.14 item 8	INV-6 S2; C-61; design 5.14 item 8; the a07 record	applied 18:22 JST
.orchestration/decisions.tsv:93:D-024-45	2026-10-20T11:45Z	Design 5.14 item 10 (every worker command inside the sandbox) contradicts the seat configuration that runs `agmsg-dispatch` through excludedCommands outside the sandbox (audit:7eab146:1, audit:6434c27:1; the a008 seat's sandbox.md:18). The design is frozen (D-024-29), so the choice is the operator's: default = record a control-plane exemption for `agmsg-dispatch` in 5.14 item 10 by a design-amendment task (the bus is the regime's control plane, not a repository mutation; the herdr socket is already in the sandbox allowlist, so the alternative, running it inside, is tested first by a Claude seat); until decided, the finding is recorded as it stands on every affected lineage and never dispositioned fixed. Placed in the project map's decisions panel with that default.	claude-deep-dot
.orchestration/decisions.tsv:94:D-024-46	2026-10-20T12:20Z	D-024-43 and D-024-45 are revoked after the operator's question of 21:0x JST. (1) result-evidence-check-a01 was a lineage outside plan 024 that overlapped P1-5's result-precheck.sh and took C-80 reviews that C-80 reserves for security: true texts; the lineage is withdrawn (record kept), its two checks (the validation's base/candidate comparison and the head's CI as read by the orchestrator) become items of P1-5's follow-up owner `dotfiles-T133-result-precheck-followup-a01`, and the glue `result-evidence-check.sh` stays orchestrator-side. (2) Design 5.14 item 10 already orders the worker seats' excludedCommands emptied (024-design-quality.md:116); it was never assigned a Phase 1 task, so the `agmsg-dispatch *` exclusion of agent-config.yaml:285 (based on the T39 measurement that the T130 socket allowlist superseded; this seat sent messages 2827 and 2830 from sandboxed Bash) is implemented by a task routed to a Codex seat (Claude boundary), with permgate untouched (operator step per the design) and the Linux behaviour measured in CI as the task's residual. No design change is needed and no operator decision is pending.	claude-deep-dot
.orchestration/decisions.tsv:95:D-024-47	2026-10-20T14:22Z	The operator's written instruction of 23:2x JST ("承認するので、そちらで実施"): (1) the plan-amendment records PR (backlog table: #387/#432 to stop + hold with the a06 reset after Phase 1, #417 close, #378 merge, #396 and #404 continue; Phase 1 rows P1-16 design 5.14 item 10 implementation and P1-17 regime CI token; the transport procedure of D-024-36 as a Playbook item) is approved in advance and the orchestrator merges it under the final-integration exemption once CI is green, with --match-head-commit; (2) after P1-14 a05 merges, the orchestrator runs `make update` and re-seats the Codex workers itself as the default procedure, reporting any permission refusal (the remove-worker classifier) at that moment instead of asking beforehand.	operator (moriya-fumio-thd)
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a06-checker round=1 reset_of=dotfiles-T133-task-generator-plan-check-a05-checker repo=~/Workspace/dotfiles/.claude/worktrees/worker-g task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md task_sha256=90ca0ae9563df4b352dfb26c6b6aa60132386e15ce9ff50bcf998a43097a12e6 deadline=none done_signal=AGMSG-RESULT note=a012:reset-a06(D-024-39:measured-cap-440/700-for-the-canonical-path-pipeline-re-plan;your-uncommitted-draft-is-this-round's-content,plus-amendment-1's-identity-aware-matching-and-path-collision-refusal-with-the-two-file-regression;C-80-73ac933-correct;PR-440-continues-from-06ffefbc;add-the-a06-task-copy-and-records,keep-the-a05-copy;commit-locally-and-PONG-the-head-for-transport;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)"
  ],
  "format": 1,
  "head": null,
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
  "pr": null,
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
  "searches": [],
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
---
format: 2
task_id: dotfiles-T133-worker-sandbox-exclusions-a02
reset_of: [dotfiles-T133-worker-sandbox-exclusions-a01]
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - scripts/validate-agent-assets.py
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/**
after: []
threat_table:
  - control: the predecessor copy .orchestration/dotfiles-T133-worker-sandbox-exclusions-a01/task.md (reset_of)
    disposition: "residual: the a01 worker committed nothing (implementation_commits=0 in its blocked PONG), so no a01 copy exists on any branch; the a02 copy at .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md is the only task copy of the lineage and regime-ci verifies the latest copy of a reset_of lineage against the text on main"
  - control: the PR edits home/dot_agents/agent-config.yaml
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_sandbox_exclusions_render_empty_for_all_os"
  - control: the PR edits home/.chezmoitemplates/claude-settings-managed.json
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_sandbox_exclusions_are_empty_for_all_os"
  - control: the PR edits scripts/validate-agent-assets.py (the validator rejects a non-empty rendered excludedCommands list)
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_sandbox_validator_requires_empty_exclusions"
  - control: the PR edits tests/unit/test_generate_agent_configs.py
    disposition: "residual: real manifest rendering and validator mutations exercise the production paths; final-head CI and the independent audit check the assertions"
  - control: the PR edits tests/unit/test_claude_settings_merge.py
    disposition: "residual: the existing per-OS merge regression checks the committed template red then green; final-head CI and the task-level audit from main check its assertions"
  - control: the PR edits .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/**
    disposition: "residual: this directory contains task data and evidence only; the audit compares claims with commands, message ids and the final head"
  - control: the task copy (.orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md)
    disposition: "residual: the orchestrator compares the whole-file SHA256 and bytes with the dispatched text before acceptance"
  - control: the evidence records (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: command outputs and sandbox message ids are recorded without secrets or literal home paths and independently checked at acceptance"
  - control: task metadata (reset_of, kind, security, allowed_files, after, threat_table, premises)
    disposition: "residual: the consistency checker checks the dispatched front matter and acceptance compares the byte-identical task copy"
  - control: metadata separators
    disposition: "residual: YAML boundaries remain intact and the whole-file digest covers metadata, body and the final Checks block"
  - control: in-process effects
    disposition: "residual: importing PR-controlled generator or validator code can have unrelated effects; the task-level audit from main checks those effects"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: tooling and Git retain tool, configuration and inherited environment inputs; the worker sandbox confines execution and the task-level audit from main checks inputs and effects"
  - control: new or renamed scripts
    disposition: "residual: none are authorized; final-head path review checks that the change uses the existing generator, validator and test module"
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator follows Orchestrator Playbook step 10 and merges only the audited head after the gate and required checks"
  - control: orchestrator effect update-branch
    disposition: "residual: a changed head requires fresh exact-head CI, feedback sweep and audit before the step 10 gate"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none is planned; normal removal refuses a dirty tree and any forced removal records discarded state in acceptance"
  - control: "design 5.14 item 0: 脅威モデル（D-024-21）"
    disposition: "residual: host controls limit accidents and prompt injection; same-UID credentials remain shared and detection in the next record PR is not prevention"
  - control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）"
    disposition: "residual: Codex authors this Claude-boundary change; other Claude write-boundary work remains with P1-15 and is not established by empty exclusions"
  - control: "design 5.14 item 2: 無害化した環境を最初に"
    disposition: "residual: Check isolates the unit-test processes only; other repository tooling stays in the worker sandbox and is checked by the task-level audit from main"
  - control: "design 5.14 item 3: 信頼パスの境界検査"
    disposition: "residual: no trusted-path resolver changes; final-head scope review detects accidental path changes but cannot prevent same-UID substitution"
  - control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す"
    disposition: "residual: task-copy bytes and the transported full head are compared at acceptance; local evidence remains susceptible to same-UID mutation"
  - control: "design 5.14 item 5: 出力と予約の同一性"
    disposition: "residual: transport and CI messages bind the full 40-hex head; no lock or physical-slot mechanism is changed"
  - control: "design 5.14 item 6: 正直な残余"
    disposition: "residual: sandbox.md separates Claude macOS sends 2827 and 2830, the Codex probe denial, rendering-only CI, unmeasured Linux Claude sandbox runtime owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01, and unapplied live seats"
  - control: "design 5.14 item 7: 検証"
    disposition: "residual: render and validator regressions are red then green and CI checks both rendered OS variants; this task adds no trusted-execution mechanism"
  - control: "design 5.14 item 8: 承認はコミット済み台帳から読む"
    disposition: "residual: this task changes no approval reader; permission approval and final-head evidence remain subject to the orchestrator's existing integration procedure"
  - control: "design 5.14 item 9: 私設キャッシュ"
    disposition: "residual: use the launcher's worker cache and pinned interpreter; no shared cache becomes a new orchestrator execution source"
  - control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）"
    disposition: "residual: empty-list tests check configuration; Claude sandboxed sends and the Codex sandbox denial record runtime evidence; Codex networking is a separate task, Linux runtime remains unmeasured, live seats retain the exclusion until apply, and permgate remains operator-owned"
premises:
  - claim: "The shared list has one entry, Linux adds three, both rendered branches contain exclusions, and T130's Herdr socket allowlist is present."
    command: |-
      /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I -c 'from pathlib import Path; m=Path("home/dot_agents/agent-config.yaml").read_text(); t=Path("home/.chezmoitemplates/claude-settings-managed.json").read_text(); a=m.split("    excludedCommands:",1)[1].split("    linux_excluded_commands:",1)[0]; b=m.split("    linux_excluded_commands:",1)[1].split("    filesystem:",1)[0]; print("shared="+str(a.count("\n      - "))+" linux_additions="+str(b.count("\n      - "))+" rendered_sites="+str(t.count("\"excludedCommands\""))+" herdr_socket="+str(".config/herdr/herdr.sock" in m))'
    output: |-
      shared=1 linux_additions=3 rendered_sites=2 herdr_socket=True
  - claim: "The existing rendering module ends with unittest.main(), and the validator still requires the old exact Linux seat-tool list."
    command: |-
      /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I -c 'import ast; from pathlib import Path; p=Path("tests/unit/test_generate_agent_configs.py"); t=p.read_text(); c=next(n for n in ast.parse(t).body if isinstance(n, ast.ClassDef)); v=Path("scripts/validate-agent-assets.py").read_text(); print(str(p)+" class="+c.name+" unittest.main="+str(t.rstrip().endswith("unittest.main()"))+" validator_linux_exact="+str("Linux excludedCommands must match the exact seat-tool list" in v))'
    output: |-
      tests/unit/test_generate_agent_configs.py class=GenerateAgentConfigsTest unittest.main=True validator_linux_exact=True
---

# AGMSG-TASK dotfiles-T133-worker-sandbox-exclusions-a02 — empty every rendered sandbox exclusion list

Design 5.14 of .orchestration/plans/024-design-quality.md is frozen by D-024-29 and applies by reference under D-024-30; rely on items 0–10, implementing item 10's exclusion-list change here. Worker: Codex security profile, because the affected execution boundary is Claude's; this seat has no network and the orchestrator transports its committed head. Generation, lint and Makefile recipes are the repository's own tooling run inside the worker's sandbox (design 5.14 items 2, 7, 9 by reference, D-024-30).

## Item 1

INV-6 / plan 006 S2 reset: a01 took two amendments before implementation; this whole replacement is authored by another review-profile context.
Set both `claude.sandbox.excludedCommands: []` and `linux_excluded_commands: []`; retain both keys, removing every pattern including the Linux additions. Replace the exclusion-history comments with one English sentence recording T39's 2026-10-01 Herdr PermissionDenied, T130's addition of `$HOME/.config/herdr/herdr.sock` to allowUnixSockets, and the orchestrator's sandboxed Bash messages 2827 and 2830 on 2026-10-20.
Regenerate through `uv run --no-config --no-project --offline --python "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" --with pyyaml python -I scripts/generate-agent-configs.py`; both OS branches of the managed template must retain `"excludedCommands": []`. Do not hand-edit generated output or change the generator.
Replace the validator's old list policy with an empty-list rule for both OS variants: reject every non-empty list and malformed non-list, retaining the existing missing-key default. Preserve diagnostics exercised by unchanged validator tests (`macOS.*gh` and `Linux.*excludedCommands`) without exceptions to the empty-list rule.

## Item 2

In GenerateAgentConfigsTest add the three selectors named above: render the real manifest for darwin/linux and assert empty lists; render both committed template branches and assert empty lists; import the real validator by file path and exercise empty acceptance plus non-empty and malformed refusals on both OS variants. Include agmsg-dispatch, gh, git push, herdr-agents, actas-claim and an arbitrary pattern. Update existing exclusion expectations in this module; keep `unittest.main()` and use existing fixture helpers.
Update `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging`: change the old exclusion-list assertion near line 591 to `[]` for Darwin and Linux; it must fail on the committed template before regeneration and pass after regeneration, preserving the other merge and idempotence assertions.
Every new behavior must have an assertion-based red result before implementation and green afterwards, with selectors and both outcomes in report.md; missing executables, imports or dependencies do not count as red. Keep fixture tool invocations runnable under the prescribed clean PATH through absolute installed tool paths, without widening PATH or adding dependencies.

The orchestrator pastes its own macOS Claude-sandbox measurement into the acceptance record: messages 2827 and 2830 of 2026-10-20, sent from sandboxed Bash, with exact commands, exit statuses, redacted outputs and message ids.
From sandboxed Bash run `agmsg-dispatch "$TEAM" "$WORKER" "$ORCHESTRATOR" "$ORCHESTRATOR_PANE" 'AGMSG-PONG v1 task_id=dotfiles-T133-worker-sandbox-exclusions-a02 status=working reason=sandbox-dispatch-probe'`, binding recipients from the dispatch envelope. In validation.md record the exact command, sandbox/runtime identity (`network_access=false`, no Unix-socket allowlist), exit code, verbatim redacted output and any message id actually returned. The prior Codex-sandbox measurement was Herdr-socket `PermissionDenied: Operation not permitted`; record this worker's measured result without requiring successful dispatch or a delivered PONG, and never retry outside the sandbox.
This probe records the Codex half of design 5.14 item 10; the manifest's `sandbox_workspace_write.network_access = true` is a separate task. No CI step launches a Linux Claude sandbox, so `agmsg-dispatch` runtime behavior there remains unmeasured by this task, a residual owned by follow-up task `dotfiles-T133-worker-sandbox-exclusions-followup-a01`.

## Check

Worker Playbook step 4 applies: every command runs inside the sandbox; record the expected Codex probe refusal in sandbox.md as measured state; for any other refusal record it in sandbox.md and send `AGMSG-PONG v1 status=blocked`; never retry outside.
Run before implementation and after, recording commands, exit statuses and verbatim redacted outputs:
`/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_generate_agent_configs.py`
`/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_claude_settings_merge.py ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging`
Run `make render-check`, `make validate-agent-assets`, `ruff check --config ruff.toml scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py tests/unit/test_claude_settings_merge.py` and `ruff format --config ruff.toml --check scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py tests/unit/test_claude_settings_merge.py`; no Bats locally.

Caps: at most 60 changed lines outside `tests/` and `.orchestration/`, and at most 120 under `tests/`.
Measure summed additions plus deletions with `git diff --numstat <base40>...<head40>`; base40 is pasted at dispatch and head40 comes from RESULT.
Before completion run `make require-crit-review` and follow AGENTS.md's agent-side crit-data procedure if required, saving -worker- evidence and receipt in the allowed task directory; no browser review. The whole task file, including the orchestrator's Checks paste, stays at or under **140 lines**; author lines stay at or under **132 lines**.

## Completion

Start a fresh branch with `git switch -c security/worker-sandbox-exclusions-a02 --no-track origin/main`. Save .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md byte-identical to the dispatched text; in that directory write report.md (changes, named red/green outcomes, residuals, cost), validation.md (commands/output, exit codes, Codex-sandbox probe result, actual message ids, cap totals), sandbox.md, learning.md and autoskill.md (used or not-used). Maintain Codex seat plan/todo worklogs with at most one active todo per owner; do not commit plan/todo/learn. Include a cost: line with observed figures or n/a.
Commit locally, then send `AGMSG-PONG v1 status=working head=<40-hex>` with artifact paths. The orchestrator transports that exact head to github.com/mryfmo/dotfiles, creates the English PR, verifies exact-head Actions and the Worker Playbook step 15 Bot wait, then sends a PING binding head, PR URL and `ci=green` or failed checks. Fix in-scope failures through another committed head and transport cycle; the worker performs no network operation or merge.
Only after the orchestrator's matching-head `ci=green` PING send `AGMSG-RESULT v1 task_id=dotfiles-T133-worker-sandbox-exclusions-a02 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` and artifact paths.

Out of scope: permgate (operator-owned), Codex networking, other permission changes and live apply; Linux sandbox runtime measurement remains with `dotfiles-T133-worker-sandbox-exclusions-followup-a01`. The change reaches live seats only at the next `make update` after P1-14 a05 merges; until then worker seats retain the exclusion and task-level audits keep recording the existing P1.

## Checks (pasted by the orchestrator before each send)
 succeeded in 160ms:
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
session id: 01a159b2-3a72-7ce2-8c25-c7c11afa45f3
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
タスク本文と参照先の acceptance・review を読み、各 threat row の対策が実際の実行対象を拘束できるか確認します。agmsg-orchestration と Ponytail の手順を参照し、読み取り専用で進めます。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 13ms:
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
/bin/zsh -lc 'git status --short
nl -ba .orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md' in ~/Workspace/dotfiles
 succeeded in 12ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/acceptance/dotfiles-T133-loop-limits-a01.md
 M .orchestration/acceptance/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
 M .orchestration/acceptance/dotfiles-T133-result-precheck-a01.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-design-quality.md
 M .orchestration/plans/024-progress.tsv
 M .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a06.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-34cc889.log
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-crit.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-pr-feedback.json
 M .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-review-receipt.md
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a04-pr-feedback.json
 M .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a05-pr-feedback.json
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
?? .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a06.md
?? .orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-followup-a04.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a02.md
?? .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a02.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md
?? .orchestration/acceptance/dotfiles-T133-result-evidence-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a02.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
?? .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a02/
?? .orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/
?? .orchestration/dotfiles-T133-ci-efficiency-a01/task.md
?? .orchestration/dotfiles-T133-result-precheck-a01/
?? .orchestration/dotfiles-T133-result-precheck-a02/
?? .orchestration/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01/
?? .orchestration/dotfiles-T133-verdict-audit-pool-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a01/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-a02/
?? .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a01/
?? .orchestration/dotfiles-T133-worker-write-boundary-a01-redesign-review-a01/
?? .orchestration/dotfiles-T133-worker-write-boundary-a02-redesign-review-a01/
?? .orchestration/learning/mistakes/M-20261020-01-amendment-note-reproduces-refused-string.md
?? .orchestration/learning/mistakes/M-20261020-02-boundary-carried-pre-dispatch-snapshots.md
?? .orchestration/learning/mistakes/M-20261020-03-dispatch-after-failed-script.md
?? .orchestration/learning/mistakes/M-20261020-04-result-claims-against-own-counts.md
?? .orchestration/learning/mistakes/M-20261020-05-ledger-ids-collide-across-kinds.md
?? .orchestration/learning/mistakes/M-20261020-06-new-task-id-collided-with-a-lineage.md
?? .orchestration/learning/mistakes/M-20261020-07-chain-under-a-superseded-task-id.md
?? .orchestration/learning/mistakes/M-20261020-08-dispatch-after-refused-pre-send.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-a02.md
?? .orchestration/tasks/dotfiles-T133-pre-send-check-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-python-pin-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/tasks/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md
?? .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a02.md
?? .orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md
?? .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02-redesign-review-a01.md
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-34cc889.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-audit-af86233.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-chain-af86233.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a06-local-review-af86233.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-chain-a644a7d.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-chain-dbc8b67.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-chain-fea3843.log
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-crit.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-local-review-a644a7d.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-local-review-dbc8b67.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-review-receipt.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-23f5144.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-23f5144.md.last.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-audit-6434c27.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-audit-6434c27.md.last.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-audit-7eab146.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-audit-7eab146.md.last.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-chain-222b616.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-chain-6434c27.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-chain-7eab146.log
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-crit.json
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-local-review-222b616.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-local-review-6434c27.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-local-review-7eab146.md
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-normalised-comparison-lint-followup-a04-review-receipt.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md
?? .orchestration/validation/dotfiles-T133-permission-guard-gate-a05-slice1-text-security-1293d6b.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-chain-09e2e95.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-chain-11584e1.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-chain-9ce253f.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-chain-d067910.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-local-review-09e2e95.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a01-local-review-d067910.md
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
?? .orchestration/validation/dotfiles-T133-python-pin-a02-audit-1327740.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-audit-1327740.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-chain-1327740.log
?? .orchestration/validation/dotfiles-T133-python-pin-a02-crit.json
?? .orchestration/validation/dotfiles-T133-python-pin-a02-local-review-1327740.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-python-pin-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-security-1327740.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-security-1327740.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-68fd5f2.md.last.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md
?? .orchestration/validation/dotfiles-T133-python-pin-a02-text-security-906e395.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-4e3ec93.md.last.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-d899b84.md
?? .orchestration/validation/dotfiles-T133-record-json-sync-a01-text-security-d899b84.md.last.md
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
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-07cdcee.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-07cdcee.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-3accc7b.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-3accc7b.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-c14b967.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-audit-c14b967.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-chain-07cdcee.log
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-chain-3accc7b.log
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-chain-c14b967.log
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-crit.json
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-local-review-07cdcee.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-local-review-3accc7b.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-local-review-c14b967.md
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-regime-ci-fixture-grammar-a02-review-receipt.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-2c8c05a.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-eaf8c47.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-eaf8c47.md.last.md
?? .orchestration/validation/dotfiles-T133-result-evidence-check-a01-text-security-72882ac.md
?? .orchestration/validation/dotfiles-T133-result-evidence-check-a01-text-security-72882ac.md.last.md
?? .orchestration/validation/dotfiles-T133-result-evidence-check-a01-text-security-99c37ca.md
?? .orchestration/validation/dotfiles-T133-result-evidence-check-a01-text-security-99c37ca.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-7a201ea.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-chain-e68fb33.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-crit.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-local-review-7a201ea.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-review-receipt.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-06ffefb.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-06ffefb.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-cedc7f5.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-security-cedc7f5.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-cd37b74.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-21f52c7.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-chain-2cb5848.log
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-21f52c7.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-b8bf806.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-b8bf806.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-4a49ed9.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-4a49ed9.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-73ac933.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-73ac933.md.last.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-b9e04cb.md
?? .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-text-security-b9e04cb.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-9545e59.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-a561e64.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-audit-a561e64.md.last.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-25dd01e.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-9545e59.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-a2f4744.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-a561e64.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-chain-b3c5076.log
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-crit.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-9545e59.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-a561e64.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-local-review-b3c5076.md
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-trusted-exec-contract-tests-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a01-text-security-2116a65.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a01-text-security-2116a65.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a01-text-security-232c174.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a01-text-security-232c174.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-6f95aef.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-6f95aef.md.last.md
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
?? .orchestration/validation/records-sync-28-pr-feedback.json
?? .orchestration/validation/records-sync-29-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-regime-ci-token-a01
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - .github/workflows/regime.yml
     8	  - scripts/orchestrator/regime-ci.py
     9	  - tests/unit/test_regime_ci.py
    10	  - .orchestration/dotfiles-T133-regime-ci-token-a01/**
    11	after: []
    12	threat_table:
    13	  - {control: ".github/workflows/regime.yml", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_the_regime_workflow_runs_base_code_only"}
    14	  - {control: "scripts/orchestrator/regime-ci.py", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_forwards_only_parent_tokens"}
    15	  - {control: "tests/unit/test_regime_ci.py", disposition: "residual: Final-head CI and the independent task audit compare fixture assertions with production behavior; tests supply no approval authority."}
    16	  - {control: ".orchestration/dotfiles-T133-regime-ci-token-a01/**", disposition: "residual: These untrusted artifacts contain only this task's copy and evidence; no executable helper or credential is stored here."}
    17	  - {control: "the task copy .orchestration/dotfiles-T133-regime-ci-token-a01/task.md", disposition: "residual: The orchestrator compares every byte and SHA256 with the dispatched text before acceptance."}
    18	  - {control: "the evidence records under .orchestration/dotfiles-T133-regime-ci-token-a01/**", disposition: "residual: The audit compares reported commands, red/green outcomes, cap totals and CI with the final head; token values are excluded from evidence."}
    19	  - {control: "task metadata (kind, security, allowed_files, after, threat_table, premises)", disposition: "residual: The consistency checker validates the front matter before dispatch and acceptance; whole-file comparison detects changed metadata."}
    20	  - {control: "metadata separators", disposition: "residual: YAML parsing and the dispatched whole-file digest cover separators in the task copy; evidence remains untrusted data."}
    21	  - {control: "in-process effects", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_keeps_tokens_out_of_argv_and_output"}
    22	  - {control: "workflow and interpreter or environment inputs: checker-child environment only", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_forwards_only_parent_tokens"}
    23	  - {control: "regime-ci CHECKER_RUN executable selection of uv and python", disposition: "residual: Executable selection, including PATH and virtual-environment discovery, is outside this task and owned by dotfiles-T133-regime-ci-token-followup-a01."}
    24	  - {control: "GH_TOKEN and GITHUB_TOKEN authority", disposition: "residual: The workflow's GITHUB_TOKEN under permissions: contents: read can read public repository contents only. A token supplied by any other caller carries that caller's authority; this task neither widens nor narrows it. The checker forwards, never mints, tokens."}
    25	  - {control: "new or renamed scripts", disposition: "residual: No script is added or renamed; retain the existing verifier, checker command and isolated interpreter setup."}
    26	  - {control: "orchestrator effect merge", disposition: "residual: Only the orchestrator integrates under Playbook step 10, binding the merge to the audited full head after the gate; the worker never merges."}
    27	  - {control: "orchestrator effect update-branch", disposition: "residual: A changed head requires fresh applicable CI, feedback and audit evidence under Playbook step 10 before integration."}
    28	  - {control: "orchestrator effect forced worker removal", disposition: "residual: None planned; removal refuses dirty state without force, and the orchestrator records any discarded state in acceptance."}
    29	  - {control: "5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: This token handoff establishes neither same-UID isolation nor separation of worker and orchestrator GitHub credentials."}
    30	  - {control: "5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: This Claude seat uses its deployed sandbox; this slice changes no host boundary or managed settings and proves no deployment isolation."}
    31	  - {control: "5.14 item 2: 無害化した環境を最初に", disposition: "residual: Tests close only the checker-child allowlist; existing parent execution and PATH selection remain unchanged and are not claimed sanitized."}
    32	  - {control: "5.14 item 3: 信頼パスの境界検査", disposition: "residual: Existing base-checkout and trusted-path checks remain unchanged; this task adds no protection against concurrent same-UID replacement."}
    33	  - {control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: regime-ci's git reads inherit GIT_DIR; dotfiles-T133-regime-ci-token-followup-a01 owns binding those reads to the checker execution tree."}
    34	  - {control: "5.14 item 5: 出力と予約の同一性", disposition: "residual: Evidence and RESULT identify the full head; this change adds no lock, reservation or physical execution slot."}
    35	  - {control: "5.14 item 6: 正直な残余", disposition: "residual: Report fixture observations separately from hosted-runner evidence; parent startup, shared caches and same-UID access remain residual risks."}
    36	  - {control: "5.14 item 7: 検証", disposition: "residual: Named red/green tests cover this handoff; retain existing security regressions and disclose unexecuted checks without claiming full contract closure."}
    37	  - {control: "5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: The unchanged checker owns canonical-main API reads; token availability supplies authentication, never approval authority from local records."}
    38	  - {control: "5.14 item 9: 私設キャッシュ", disposition: "residual: Preserve existing UV_CACHE_DIR handling and no-config isolated execution; this task neither provisions nor authenticates a private cache."}
    39	  - {control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Claude worker seats run inside their sandbox except the manifest's remaining excludedCommands: agmsg-dispatch *; on Linux also gh *, herdr-agents * and actas-claim.sh *. dotfiles-T133-worker-sandbox-exclusions-a02 owns their removal under design 5.14 item 10. This task's git, uv, python and ruff commands are not excluded and run inside the sandbox; the deployed settings keep `failIfUnavailable: false`, so a missing sandbox dependency would run them unsandboxed, a residual of the Claude settings owned by design 5.14 item 10's lineage; a refusal is reported as AGMSG-PONG v1 status=blocked."}
    40	premises:
    41	  - claim: The reviewed checker head resolves locally; this identifies the review input, not canonical GitHub authority.
    42	    command: |-
    43	      git rev-parse 2cb58482
    44	    output: |-
    45	      2cb584823ccf5f22069ea925b252d8cefb020844
    46	  - claim: The current workflow already declares read-only contents permission.
    47	    command: |-
    48	      grep -c 'contents: read' .github/workflows/regime.yml
    49	    output: |-
    50	      1
    51	  - claim: The existing uv-configuration regression test is present.
    52	    command: |-
    53	      grep -c test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config tests/unit/test_regime_ci.py
    54	    output: |-
    55	      1
    56	---
    57	
    58	# AGMSG-TASK dotfiles-T133-regime-ci-token-a01 — authenticate the regime checker's read-only API requests
    59	
    60	Amendment 1 addresses C-80 round 1 (`text-security:c32513e:1-5`); previous_sha256: c32513e5cbf65661a7a5d2f385dd814f6735d9ddaa1495b03da47db2f9c71335.
    61	
    62	Operator premise: PR #440, head 2cb58482, lineage dotfiles-T133-task-generator-plan-check-a06-checker, is merging next; its checker forwards parent GH_TOKEN/GITHUB_TOKEN only to gh api, including canonical-main SHA, C6/C15 design bytes and C8/C9 lookups. A fresh hosted runner has no gh login: missing authentication exits 4 and regime-ci reports no verdict. The local review found this P1 caller defect outside #440's allowed_files; fix it before regime becomes a required check.
    63	
    64	Design 5.14 (.orchestration/plans/024-design-quality.md), frozen by D-024-29, applies by reference under D-024-30; rely on items 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 and 10.
    65	
    66	## Item 1
    67	
    68	Add `GH_TOKEN: ${{ github.token }}` to the regime-ci step's env in .github/workflows/regime.yml; retain `permissions: {contents: read}` and base-only execution. This workflow edit is authorized because the workflow is this task's subject; do not activate a ruleset or widen permissions.
    69	
    70	In scripts/orchestrator/regime-ci.py extend the checker's minimal environment (HOME, PATH, LANG, UV_CACHE_DIR) with GH_TOKEN and GITHUB_TOKEN only when each key exists in regime-ci's own environment, preserving its value. Keep every other inherited variable out; do not copy the whole parent environment, synthesize credentials, put tokens in argv or print them. Keep the checker and its launch arguments unchanged.
    71	
    72	In tests/unit/test_regime_ci.py add RegimeCiTest.test_regime_ci_forwards_only_parent_tokens: clear both ambient token keys, exercise neither, each alone and both with synthetic values, and assert the exact child environment, including exclusion of unrelated parent variables. Add RegimeCiTest.test_regime_ci_keeps_tokens_out_of_argv_and_output to assert neither synthetic token occurs in captured subprocess argv or regime-ci stdout/stderr, covering normal verdict and no-verdict diagnostics. Both new methods assert expected token presence in the child, so dropping credentials cannot satisfy secrecy assertions. Use existing fixtures and targeted subprocess capture or a fake checker; no live API or login. These environment and secrecy tests close only “GH_TOKEN reaches the checker's environment exactly when regime-ci's environment holds it, and never appears in argv or output”; CHECKER_RUN executable selection remains with the follow-up named in the threat table.
    73	
    74	Update test_the_regime_workflow_runs_base_code_only's exact env assertion for the new token entry while retaining its permissions and base-only checks. Keep test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config green and unittest.main() at the module end. Write and run tests before implementation: every new behavior must be red before its production change and green after; name each outcome in report.md and distinguish existing passing regressions.
    75	
    76	## Check
    77	
    78	Measured deployment for Worker Playbook step 4: Claude worker seats run inside their sandbox except the commands the manifest's excludedCommands still lists: `agmsg-dispatch *`, and on Linux `gh *`, `herdr-agents *`, `actas-claim.sh *`. Design 5.14 item 10's own task, dotfiles-T133-worker-sandbox-exclusions-a02, removes these exclusions. This task's git, uv, python and ruff commands are not excluded and run inside the sandbox. Record a refusal in sandbox.md and send `AGMSG-PONG v1 status=blocked` with the command and boundary; never retry outside.
    79	
    80	Resolve uv once with `UV_DIR="$(dirname "$(env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv)")"` and paste the command and its output into report.md. The result is the absolute, non-shim directory that holds the uv binary mise installed (on this host `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/`); do not assume a `bin` subdirectory and read no pin file: the version is whatever mise resolves for this checkout, and the pasted path is the evidence.
    81	
    82	Run before implementation and after: `/usr/bin/env -i PATH="$UV_DIR:/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py`, substituting the pinned version and using that same resolved absolute uv directory for both runs.
    83	
    84	Run `ruff check --config ruff.toml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py` and `ruff format --config ruff.toml --check scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py`. Paste commands, exit statuses and verbatim output without credential values into validation.md. Caps: at most 25 changed lines outside `tests/` and `.orchestration/`, and at most 60 under `tests/`.
    85	
    86	Measure summed additions plus deletions with `git diff --numstat <base40>...<head40>`; base40 is pasted at dispatch and head40 comes from RESULT. This whole task text, including the orchestrator's Checks block, stays at or under 125 lines.
    87	
    88	Do not run Bats locally. After the final push verify GitHub Actions for the exact final head with `gh pr checks <pr> --repo mryfmo/dotfiles --watch`, fix in-scope failures and repeat before RESULT; follow Worker Playbook step 15 for the bounded Bot wait and findings. Before completion run `make require-crit-review`; if required, follow AGENTS.md's crit-data evidence and receipt procedure with worker evidence under this task's allowed directory, without a browser review.
    89	
    90	## Completion
    91	
    92	Fetch current origin/main inside the sandbox and create a fresh branch with `git switch -c ci/regime-ci-token-a01 --no-track origin/main`. Save .orchestration/dotfiles-T133-regime-ci-token-a01/task.md byte-identical to the dispatched text. Under that directory commit report.md (implementation, named red/green outcomes, residuals, cost), validation.md (commands/output and both cap totals), sandbox.md, learning.md and autoskill.md (used or not-used); do not commit plan/todo/learn worklogs. Add no runtime helpers or changes outside allowed_files.
    93	
    94	Push with `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u https://github.com/mryfmo/dotfiles.git <branch>` and open with `gh pr create --repo mryfmo/dotfiles` using an English title and body.
    95	
    96	After final-head checks pass, send `AGMSG-RESULT v1 task_id=dotfiles-T133-regime-ci-token-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with artifact paths; no worker merge. Report skipped checks and remaining risks, including unchanged parent startup and cache behavior.
    97	
    98	## Checks (pasted by the orchestrator before each send)
    99	
   100	```
   101	```
   102	
   103	Author verification: Implementation, tests and live sandbox behavior were not checked for this text-only amendment; executable selection, GIT_DIR inheritance and sandbox exclusions remain with their named follow-ups.
**Reviewing existing evidence and diffs**
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md.last.md .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '5\\.14|D-024-(21|29|30)' .orchestration/plans/024-design-quality.md .orchestration/decisions.tsv
cat .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-local-review-21f52c7.md .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a02.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-2c8c05a.md .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md.last.md .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-eaf8c47.md.last.md
nl -ba scripts/orchestrator/regime-ci.py
cat .github/workflows/regime.yml' in ~/Workspace/dotfiles
 succeeded in 84ms:
# Acceptance record: dotfiles-T133-regime-ci-token-a01

Lineage: the regime workflow passes `GH_TOKEN: ${{ github.token }}` and regime-ci.py forwards it into the checker's minimal environment, so the a06 checker's new `gh api` requests (PR #440, head 2cb58482/21f52c79) get a verdict in CI. Caller-side dependency found by the local review of #440 (local:21f52c7:1); #440 waits for this lineage. Security: true (a CI workflow).

- 2026-10-20T13:27Z-13:36Z: text written whole by the review profile from the orchestrator's brief (`regime-ci-token-a01-prompt.md`); installed, 95 lines, self cap 110; pre-send OK (checker OK, secret-pattern 0, no literal home path, id free), sha256 c32513e5cbf65661a7a5d2f385dd814f6735d9ddaa1495b03da47db2f9c71335. C-80 round 1 started 13:37Z.

## Owned by dotfiles-T133-regime-ci-token-followup-a01

(no advisory rows yet; written 2026-10-20T14:17Z before the regime-ci-token PR's first advisory disposition, C-51; the owner text carries the lineage's residual rows as items)

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:38](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:38) — “Every command inside its sandbox” is not enforced: the manifest still excludes Linux `gh *` and `agmsg-dispatch *`, and the exclusions-removal acceptance records deployment as pending; excluded commands run outside immediately, so “stop on refusal” never activates. [Sandbox semantics](https://code.claude.com/docs/en/sandboxing#run-commands-outside-the-sandbox-with-excludedcommands).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:22](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:22) — The environment-dictionary test cannot close executable selection: unchanged `CHECKER_RUN` resolves `uv` through this host’s mise-first PATH and does not pin Python, so credentials reach the selected launcher/interpreter before checker validation; `--no-project` still permits discovery of a local or parent virtual environment. [uv semantics](https://docs.astral.sh/uv/reference/cli/#uv-run--no-project).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:32](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:32) — Retained “base-only execution” is not bound on this host: regime-ci’s Git reads inherit `GIT_DIR`, while execution opens the checker beneath `root`; a read-only probe returned this repository’s HEAD from `/tmp`, demonstrating that the HEAD decision need not identify the executed filesystem tree, even without a symlink race. [Git environment semantics](https://git-scm.com/docs/git#Documentation/git.txt-GITDIR).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:23](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:23) — Workflow `contents: read` constrains its generated token, not arbitrary parent `GH_TOKEN`/`GITHUB_TOKEN` values preserved by line 67; a local write-capable credential retains that authority, so this residual does not establish the claimed absence of write or merge authority. [Token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token#modifying-the-permissions-for-the-github_token).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:77](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:77) — The prescribed clean PATH omits uv, which existing fixtures launch by name; invoking the named workflow test under that environment reproduced `FileNotFoundError: 'uv'`, preventing the required green validation independently of implementation correctness.

📝 まとめ: Reviewed the text, every threat row, and related records without modifying files; full suites and live Linux sandbox behavior were not tested, and the execution-binding risks above remain unresolved.
Verdict: incorrect---
format: 2
task_id: dotfiles-T133-regime-ci-token-followup-a01
kind: code
security: false
allowed_files:
  - scripts/orchestrator/regime-ci.py
  - tests/unit/test_regime_ci.py
  - .orchestration/dotfiles-T133-regime-ci-token-followup-a01/**
after: [dotfiles-T133-regime-ci-token-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/regime-ci.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_regime_ci.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-regime-ci-token-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T133-regime-ci-token-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
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

# AGMSG-TASK dotfiles-T133-regime-ci-token-followup-a01 — the regime CI token lineage's owner task (advisory P2 of the regime-ci-token PR)

Written 2026-10-20 by the orchestrator seat before the first advisory disposition of the regime-ci-token PR (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T133-regime-ci-token-followup-a01` in `.orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md` (plan 020 step 1.2); it is dispatched after the regime-ci-token PR merges, to a seat the orchestrator names, and only when that section holds at least one row (C-102).

## Item 1

Each owned row (any advisory P2 of the local review or the task-level audit of the regime-ci-token PR's final head, and any Bot P2 the orchestrator records under this owner; rows are read from the record at dispatch; a records-only row is realised by the record it names, with no test) gets its fix and, where the row names a test or code, one red-then-green test in `tests/unit/test_regime_ci.py`, named in report.md against the row id. Nothing outside the owned rows; any other file joins `allowed_files` only by an amendment that names the row needing it.

## Item 2

The residual rows of `dotfiles-T133-regime-ci-token-a01` that name this owner: (a) regime-ci.py's `CHECKER_RUN` resolves `uv` and the interpreter through PATH; the owner binds them to the mise install directories named in the manifest, with a test that a PATH holding a decoy `uv` first is not used; (b) regime-ci.py's git reads inherit `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`; the owner clears them for every git child (`env -u`), with a test that a hostile `GIT_DIR` does not redirect the base read. Each row gets one red-then-green test in `tests/unit/test_regime_ci.py`.

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md` apply as written, with `dotfiles-T133-regime-ci-token-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-regime-ci-token-followup-a01/task.md>` in the RESULT. Design 5.14 applies by reference (D-024-30).

## Checks (pasted by the orchestrator before each send)

```
```

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:80](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:80) — Required validation cannot run as specified: neither named pin file exists, and installed uv resides under `<version>/uv-aarch64-apple-darwin/`, not `<version>/bin`; line 82 therefore cannot provide the required executable. Specify the actual pin source and verified installation directory before dispatch.

📝 まとめ: Reviewed the threat rows and related records without edits. Implementation tests and live Linux sandbox behavior were not exercised; the explicitly deferred execution-binding risks remain.
Verdict: incorrect- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:23](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:23) — This row and line 33 defer executable selection and `GIT_DIR` binding to followup-a01, but that task already merged as #425 and its explicitly bounded owned rows contain neither fix; the named owner therefore supplies no mitigation for credentials reaching a PATH-selected executable or Git validation identifying a different execution tree.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:78](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:78) — “Not excluded” does not establish sandbox confinement: deployed settings retain `failIfUnavailable: false`, so missing sandbox dependencies permit unsandboxed execution without a refusal; the prescribed stop-on-refusal control cannot enforce this claim. [Documented fallback behavior](https://code.claude.com/docs/en/sandboxing#get-started).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:80](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:80) — The required validation setup cannot run as specified: this host has mise at `~/.local/bin/mise`, neither named pin file exists, and installed uv resides under `<version>/uv-aarch64-apple-darwin/`, not `<version>/bin`; consequently the required red/green execution remains blocked independently of implementation.

📝 まとめ: Reviewed every threat row and cited records without edits. Implementation tests and live Linux sandbox behavior were not exercised; the execution-binding and confinement gaps above remain.
Verdict: incorrect     1	"""Check a pull request against its task copies with the base's verifier: the regime CI job (plan 024 P1-11, T133 a02).
     2	
     3	`uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base <ref> --head <sha>
     4	[--root <base checkout>]` runs from the base checkout and reads the head only through `git show`: it never checks out,
     5	imports or executes head content. Each task whose `.orchestration/<t>/` the diff `<base>...<head>` touches and that has a
     6	`task.md` copy at the head (of a reset_of lineage, only the latest copy) is checked: the base's task-consistency checker
     7	on the base's dispatched text, the copy against the dispatched `.orchestration/tasks/<t>.md` at the base, whose text is the policy
     8	(allowed_files, caps, reset_of), precheck.json's binding, allowed_files and the caps. Without dispatched text at the base
     9	the copy is unverifiable, a warning until REGIME_REQUIRE_DISPATCHED=1 makes it a violation; result.txt and precheck.json
    10	are the pull request's own claims. It prints one `regime-ci: <t>: <rule>: <detail>` line per violation and
    11	`regime-ci: warning: ...` lines, and exits 1 on any violation, 2 when git cannot list the diff, else 0 after
    12	`regime-ci: ok <n> task(s)`. A diff without a task copy passes as `no target (records-only)` only when every changed path
    13	is under `.orchestration/`; no branch name grants anything.
    14	"""
    15	
    16	import argparse
    17	import hashlib
    18	import json
    19	import os
    20	import re
    21	import subprocess
    22	import sys
    23	import tempfile
    24	from pathlib import Path
    25	
    26	try:
    27	    import yaml
    28	except ImportError:
    29	    print("regime-ci: needs pyyaml: run with uv run --no-project --with pyyaml")
    30	    sys.exit(2)
    31	
    32	CHECKER = "scripts/orchestrator/task-consistency-check.py"
    33	# --no-config: a uv.toml or pyproject.toml the pull request adds cannot steer this run
    34	CHECKER_RUN = ["uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I", CHECKER]
    35	RUNS = (CHECKER, "scripts/orchestrator/regime-ci.py", ".github/workflows/regime.yml")
    36	
    37	
    38	class GitError(Exception):
    39	    pass
    40	
    41	
    42	def git(root, *args):
    43	    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
    44	
    45	
    46	def listed(root, *args):
    47	    """Return the NUL-separated output of a git listing command, or raise GitError: no listing passes by being empty."""
    48	    out = git(root, *args, "-z")
    49	    if out.returncode:
    50	        raise GitError(f"git {' '.join(args)} failed: {out.stderr.decode(errors='replace').strip()[:200]}")
    51	    return [item for item in out.stdout.decode().split("\0") if item]
    52	
    53	
    54	def show(root, head, path):
    55	    """Return the bytes of path at head, or None when head has no such file."""
    56	    out = git(root, "show", f"{head}:{path}")
    57	    return out.stdout if out.returncode == 0 else None
    58	
    59	
    60	def sha256(data):
    61	    return hashlib.sha256(data).hexdigest()
    62	
    63	
    64	def token(text, name):
    65	    m = re.search(rf"(?:^|\s){name}=(\S+)", text)
    66	    return m.group(1) if m else None
    67	
    68	
    69	def allowed(path, entry):
    70	    """Match an allowed_files entry: `<dir>/**` takes its prefix, `*` and `?` stay within one path segment."""
    71	    if entry.endswith("/**"):
    72	        return path.startswith(entry[:-2])
    73	    rx = "".join("[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c) for c in entry)
    74	    return re.fullmatch(rx, path) is not None
    75	
    76	
    77	def caps(text, numstat):
    78	    """Return (violations, warnings) for the `## Check` sentence's caps against the numstat rows."""
    79	    check = text.split("\n## Check", 1)[1].split("\n## ", 1)[0] if "\n## Check" in text else ""
    80	    outside = re.search(r"at most (\d+) changed lines(?: \([^)]*\))? outside ([^(\n]*)", check)
    81	    tests = re.search(r"(\d+)\s+(?:added\s+|changed\s+)?(?:lines\s+)?under\s+`?tests/", check)
    82	    missing = [
    83	        f"no {n} cap in the copy's ## Check section" for n, m in (("outside", outside), ("tests/", tests)) if not m
    84	    ]
    85	    excluded = ["tests/", ".orchestration/"]
    86	    if outside:
    87	        excluded = re.findall(r"`([^`]+)`", re.split(r",\s*(?:and\s+)?\d", outside.group(2))[0]) or excluded
    88	
    89	    def counted(path, prefixes):
    90	        return any(path == p or (p.endswith("/") and path.startswith(p)) for p in prefixes)
    91	
    92	    out_lines = sum(a + d for a, d, p in numstat if not counted(p, excluded))
    93	    test_lines = sum(a + d for a, d, p in numstat if counted(p, ["tests/"]))
    94	    found = []
    95	    if outside and out_lines > int(outside.group(1)):
    96	        found.append(f"{out_lines} changed lines outside {', '.join(excluded)} exceed {outside.group(1)}")
    97	    if tests and test_lines > int(tests.group(1)):
    98	        found.append(f"{test_lines} changed lines under tests/ exceed {tests.group(1)}")
    99	    return found, missing
   100	
   101	
   102	def front(data):
   103	    """Return a copy's front matter mapping, or None when it is unreadable or not a mapping."""
   104	    try:
   105	        fm = yaml.safe_load(data.decode().split("\n---\n", 1)[0].lstrip("-\n"))
   106	    except (UnicodeDecodeError, yaml.YAMLError):
   107	        return None
   108	    return fm if isinstance(fm, dict) else None
   109	
   110	
   111	def precheck(root, head, t, result_text, exempt=()):
   112	    """Return the violations of precheck.json's binding, or None when the task carries no precheck.json."""
   113	    data = show(root, head, f".orchestration/{t}/precheck.json")
   114	    if data is None:
   115	        return None
   116	    try:
   117	        doc = json.loads(data)
   118	    except ValueError as error:
   119	        return [f"precheck.json is not JSON: {error}"]
   120	    found = []
   121	    bound = doc.get("head") if isinstance(doc, dict) else None
   122	    if not isinstance(bound, str) or not re.fullmatch(r"[0-9a-f]{40}", bound):
   123	        found.append(f"precheck.json head {bound!r} is not a 40-hex commit id")
   124	    elif bound != head:
   125	        # precheck.json cannot name the commit that adds it: it names the code commit, and the head may add only
   126	        # this task's evidence on top (the evidence-only ancestor rule of verdict.sh condition 1)
   127	        if git(root, "merge-base", "--is-ancestor", bound, head).returncode:
   128	            found.append(f"precheck.json head {bound} is neither the head {head} nor its ancestor")
   129	        elif other := [
   130	            p
   131	            for p in listed(root, "diff", "--name-only", "--no-renames", bound, head)
   132	            if not p.startswith((f".orchestration/{t}/", *exempt))
   133	        ]:
   134	            found.append(
   135	                f"precheck.json head {bound[:12]} differs from the head outside .orchestration/{t}/: {', '.join(other)}"
   136	            )
   137	    if token(result_text, "precheck") != sha256(data):
   138	        found.append(
   139	            f"precheck.json sha256 {sha256(data)} is not result.txt's precheck={token(result_text, 'precheck')}"
   140	        )
   141	    return found
   142	
   143	
   144	def policy(root, base, head, t):
   145	    """Return (the policy bytes, its front matter or None, whether the base's dispatched text is the policy)."""
   146	    dispatched = show(root, base, f".orchestration/tasks/{t}.md")
   147	    data = show(root, head, f".orchestration/{t}/task.md") if dispatched is None else dispatched
   148	    return data, front(data), dispatched is not None
   149	
   150	
   151	def checker(root, data):
   152	    """Return the base checker's violations on the base's dispatched bytes: it hands the text's literals to git (C8 to
   153	    C10) and opens its design path (C6), so a pull request's own text never reaches it (worker review P0 of bcbd6949)."""
   154	    with tempfile.TemporaryDirectory() as scratch:
   155	        cmd = [*CHECKER_RUN, "--root", root, str(Path(scratch, "task.md"))]
   156	        Path(cmd[-1]).write_bytes(data)
   157	        run = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
   158	    out = run.stdout.splitlines()  # the file is task.md, so C1 compares task_id with `task`; task-id checks <t>
   159	    # only the checker's own verdict line with its exit code counts; a crash also exits 1, with no verdict line
   160	    if (out[:1], run.returncode) not in ((["task.md: OK"], 0), (["task.md: FAIL"], 1)):
   161	        return [("checker", f"no verdict (exit {run.returncode}): {(run.stdout + run.stderr).strip()[-300:]}")]
   162	    lines = [ln.strip() for ln in out[1:] if ln.strip()]
   163	    return [("checker", ln) for ln in lines if not re.fullmatch(r"C1 task_id .* != file task", ln)]
   164	
   165	
   166	def check_task(root, base, head, t, changed, numstat):
   167	    """Return (violations, warnings) for one task, each violation a (rule, detail) pair."""
   168	    copy_path = f".orchestration/{t}/task.md"
   169	    copy = show(root, head, copy_path)
   170	    if (fm := front(copy)) is None:
   171	        return [("front-matter", f"{copy_path} is unreadable or has no front matter mapping")], []
   172	    data, rules, dispatched = policy(root, base, head, t)
   173	    if rules is None:
   174	        return [("front-matter", f"the base's .orchestration/tasks/{t}.md has no front matter mapping")], []
   175	    found, warnings = [], []
   176	    if fm.get("task_id") != t:
   177	        found.append(("task-id", f"the copy's task_id {fm.get('task_id')!r} is not its directory {t}"))
   178	    result = show(root, head, f".orchestration/{t}/result.txt")
   179	    result_text = result.decode(errors="replace") if result is not None else ""
   180	    if dispatched:
   181	        if data != copy:
   182	            found.append(("task-copy", f"{copy_path} differs from the base's dispatched .orchestration/tasks/{t}.md"))
   183	    else:  # the copy's own policy is provisional: a head file or a result.txt token is a claim, never authentication
   184	        unverifiable = "task copy unverifiable (no dispatched text at base)"
   185	        found += [("task-copy", unverifiable)] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else []
   186	        warnings += [] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else [unverifiable]
   187	        warnings.append("checker skipped: the copy is unverifiable, and the base's checker reads only the base's text")
   188	        if result is not None and token(result_text, "task_copy") != sha256(copy):
   189	            found.append(
   190	                ("task-copy", f"sha256 {sha256(copy)} is not result.txt's task_copy={token(result_text, 'task_copy')}")
   191	            )
   192	    found += checker(root, data) if dispatched else []
   193	    exempt = tuple(f".orchestration/{p}/" for p in rules.get("reset_of") or [] if isinstance(p, str))
   194	    bound = precheck(root, head, t, result_text, exempt)
   195	    if bound is None:
   196	        warnings.append("precheck absent")
   197	    found += [("precheck", detail) for detail in bound or []]
   198	    entries = [a for a in rules.get("allowed_files") or [] if isinstance(a, str)]
   199	    found += [
   200	        ("allowed-files", f"{p} is outside allowed_files")
   201	        for p in changed
   202	        if not p.startswith(exempt) and not any(allowed(p, a) for a in entries)
   203	    ]
   204	    exceeded, cap_warnings = caps(data.decode(errors="replace"), numstat)
   205	    found += [("caps", detail) for detail in exceeded]
   206	    return found, warnings + cap_warnings
   207	
   208	
   209	def main(argv=None):
   210	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   211	    parser.add_argument("--base", required=True, help="the base ref, such as origin/main")
   212	    parser.add_argument("--head", required=True, help="the pull request's head commit")
   213	    parser.add_argument("--root", help="the base checkout (default: the current git toplevel)")
   214	    args = parser.parse_args(argv)
   215	    root = args.root or git(".", "rev-parse", "--show-toplevel").stdout.decode().strip() or "."
   216	    shas = [
   217	        git(root, "rev-parse", "--verify", "--quiet", f"{r}^{{commit}}").stdout.decode().strip()
   218	        for r in (args.base, args.head)
   219	    ]
   220	    if not all(shas):
   221	        print(f"regime-ci: cannot resolve --base {args.base} or --head {args.head} in {root}")
   222	        return 2
   223	    base, head = shas
   224	    at = git(root, "rev-parse", "HEAD").stdout.decode().strip()  # the verifier and the checker must be the base's
   225	    if at != base:
   226	        print(
   227	            f"regime-ci: checkout: {root} is at {at[:12]}, not the base {base[:12]}, so the code run would not be the base's"
   228	        )
   229	        return 1
   230	    try:
   231	        changed = listed(root, "diff", "--name-only", "--no-renames", f"{base}...{head}")
   232	        numstat = []
   233	        for row in listed(root, "diff", "--numstat", "--no-renames", f"{base}...{head}"):
   234	            added, deleted, path = row.split("\t", 2)  # a path may hold a tab; a binary file counts 0 lines
   235	            numstat.append((int(added) if added.isdigit() else 0, int(deleted) if deleted.isdigit() else 0, path))
   236	    except GitError as error:
   237	        print(f"regime-ci: {error}")
   238	        return 2
   239	    for path in sorted(set(changed) & set(RUNS)):
   240	        print(
   241	            f"regime-ci: warning: the diff changes {path}; this run executed the base's version, the audit reads the change"
   242	        )
   243	    dirs = sorted({m.group(1) for p in changed if (m := re.match(r"\.orchestration/([^/]+)/", p))})
   244	    targets = [t for t in dirs if show(root, head, f".orchestration/{t}/task.md") is not None]
   245	    if not targets:
   246	        stray = [p for p in changed if not p.startswith(".orchestration/")]
   247	        if not stray:  # content alone decides: a branch name is the pull request's own claim
   248	            print("regime-ci: no target (records-only)")
   249	            return 0
   250	        print(
   251	            f"regime-ci: no target: {len(stray)} changed path(s) outside .orchestration/ and no task copy, first {stray[0]}"
   252	        )
   253	        return 1
   254	    # Amendment 1: a later copy whose reset_of names an earlier one is the lineage's only target, when both verify
   255	    policies = {t: policy(root, base, head, t) for t in targets}
   256	    exact = {t: policies[t][2] and show(root, head, f".orchestration/{t}/task.md") == policies[t][0] for t in targets}
   257	    later = {
   258	        p: t
   259	        for t, (_, rules, _) in policies.items()
   260	        for p in (rules or {}).get("reset_of") or []
   261	        if p in policies and p != t and exact[t] and exact[p]  # both head copies equal their base texts
   262	    }
   263	    for p, t in sorted(later.items()):
   264	        print(f"regime-ci: warning: {p}: predecessor copy .orchestration/{p}/task.md (reset_of of {t})")
   265	    targets = [t for t in targets if t not in later]
   266	    failed = False
   267	    for t in targets:
   268	        try:
   269	            found, warnings = check_task(root, base, head, t, changed, numstat)
   270	        except GitError as error:
   271	            found, warnings = [("git", str(error))], []
   272	        for detail in warnings:
   273	            print(f"regime-ci: warning: {t}: {detail}")
   274	        for rule, detail in found:
   275	            print(f"regime-ci: {t}: {rule}: {detail}")
   276	        failed |= bool(found)
   277	    if not failed:
   278	        print(f"regime-ci: ok {len(targets)} task(s)")
   279	    return int(failed)
   280	
   281	
   282	if __name__ == "__main__":
   283	    sys.exit(main())
name: regime

# The regime job (plan 024 P1-11, redesigned in T133 regime-ci a02): a pull request that carries a task copy is checked
# by the base's scripts/orchestrator/regime-ci.py against the base's dispatched policy. pull_request_target runs this
# workflow as it is on the base; the pull request's head is fetched as data and is never checked out or executed.
# It is an optional check until the operator adds `regime` to the ruleset's required contexts.
on:
  pull_request_target:
    types: [opened, synchronize, reopened, ready_for_review]

concurrency:
  group: regime-pr-${{ github.event.pull_request.number }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  regime:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
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
        run: uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "$(git rev-parse HEAD)" --head "${HEAD_SHA}"

**Filtering recent logs only**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md.last.md .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-eaf8c47.md.last.md
nl -ba scripts/orchestrator/regime-ci.py' in ~/Workspace/dotfiles
 succeeded in 0ms:
- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:80](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:80) — Required validation cannot run as specified: neither named pin file exists, and installed uv resides under `<version>/uv-aarch64-apple-darwin/`, not `<version>/bin`; line 82 therefore cannot provide the required executable. Specify the actual pin source and verified installation directory before dispatch.

📝 まとめ: Reviewed the threat rows and related records without edits. Implementation tests and live Linux sandbox behavior were not exercised; the explicitly deferred execution-binding risks remain.
Verdict: incorrect- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:23](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:23) — This row and line 33 defer executable selection and `GIT_DIR` binding to followup-a01, but that task already merged as #425 and its explicitly bounded owned rows contain neither fix; the named owner therefore supplies no mitigation for credentials reaching a PATH-selected executable or Git validation identifying a different execution tree.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:78](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:78) — “Not excluded” does not establish sandbox confinement: deployed settings retain `failIfUnavailable: false`, so missing sandbox dependencies permit unsandboxed execution without a refusal; the prescribed stop-on-refusal control cannot enforce this claim. [Documented fallback behavior](https://code.claude.com/docs/en/sandboxing#get-started).

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:80](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md:80) — The required validation setup cannot run as specified: this host has mise at `~/.local/bin/mise`, neither named pin file exists, and installed uv resides under `<version>/uv-aarch64-apple-darwin/`, not `<version>/bin`; consequently the required red/green execution remains blocked independently of implementation.

📝 まとめ: Reviewed every threat row and cited records without edits. Implementation tests and live Linux sandbox behavior were not exercised; the execution-binding and confinement gaps above remain.
Verdict: incorrect     1	"""Check a pull request against its task copies with the base's verifier: the regime CI job (plan 024 P1-11, T133 a02).
     2	
     3	`uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base <ref> --head <sha>
     4	[--root <base checkout>]` runs from the base checkout and reads the head only through `git show`: it never checks out,
     5	imports or executes head content. Each task whose `.orchestration/<t>/` the diff `<base>...<head>` touches and that has a
     6	`task.md` copy at the head (of a reset_of lineage, only the latest copy) is checked: the base's task-consistency checker
     7	on the base's dispatched text, the copy against the dispatched `.orchestration/tasks/<t>.md` at the base, whose text is the policy
     8	(allowed_files, caps, reset_of), precheck.json's binding, allowed_files and the caps. Without dispatched text at the base
     9	the copy is unverifiable, a warning until REGIME_REQUIRE_DISPATCHED=1 makes it a violation; result.txt and precheck.json
    10	are the pull request's own claims. It prints one `regime-ci: <t>: <rule>: <detail>` line per violation and
    11	`regime-ci: warning: ...` lines, and exits 1 on any violation, 2 when git cannot list the diff, else 0 after
    12	`regime-ci: ok <n> task(s)`. A diff without a task copy passes as `no target (records-only)` only when every changed path
    13	is under `.orchestration/`; no branch name grants anything.
    14	"""
    15	
    16	import argparse
    17	import hashlib
    18	import json
    19	import os
    20	import re
    21	import subprocess
    22	import sys
    23	import tempfile
    24	from pathlib import Path
    25	
    26	try:
    27	    import yaml
    28	except ImportError:
    29	    print("regime-ci: needs pyyaml: run with uv run --no-project --with pyyaml")
    30	    sys.exit(2)
    31	
    32	CHECKER = "scripts/orchestrator/task-consistency-check.py"
    33	# --no-config: a uv.toml or pyproject.toml the pull request adds cannot steer this run
    34	CHECKER_RUN = ["uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I", CHECKER]
    35	RUNS = (CHECKER, "scripts/orchestrator/regime-ci.py", ".github/workflows/regime.yml")
    36	
    37	
    38	class GitError(Exception):
    39	    pass
    40	
    41	
    42	def git(root, *args):
    43	    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
    44	
    45	
    46	def listed(root, *args):
    47	    """Return the NUL-separated output of a git listing command, or raise GitError: no listing passes by being empty."""
    48	    out = git(root, *args, "-z")
    49	    if out.returncode:
    50	        raise GitError(f"git {' '.join(args)} failed: {out.stderr.decode(errors='replace').strip()[:200]}")
    51	    return [item for item in out.stdout.decode().split("\0") if item]
    52	
    53	
    54	def show(root, head, path):
    55	    """Return the bytes of path at head, or None when head has no such file."""
    56	    out = git(root, "show", f"{head}:{path}")
    57	    return out.stdout if out.returncode == 0 else None
    58	
    59	
    60	def sha256(data):
    61	    return hashlib.sha256(data).hexdigest()
    62	
    63	
    64	def token(text, name):
    65	    m = re.search(rf"(?:^|\s){name}=(\S+)", text)
    66	    return m.group(1) if m else None
    67	
    68	
    69	def allowed(path, entry):
    70	    """Match an allowed_files entry: `<dir>/**` takes its prefix, `*` and `?` stay within one path segment."""
    71	    if entry.endswith("/**"):
    72	        return path.startswith(entry[:-2])
    73	    rx = "".join("[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c) for c in entry)
    74	    return re.fullmatch(rx, path) is not None
    75	
    76	
    77	def caps(text, numstat):
    78	    """Return (violations, warnings) for the `## Check` sentence's caps against the numstat rows."""
    79	    check = text.split("\n## Check", 1)[1].split("\n## ", 1)[0] if "\n## Check" in text else ""
    80	    outside = re.search(r"at most (\d+) changed lines(?: \([^)]*\))? outside ([^(\n]*)", check)
    81	    tests = re.search(r"(\d+)\s+(?:added\s+|changed\s+)?(?:lines\s+)?under\s+`?tests/", check)
    82	    missing = [
    83	        f"no {n} cap in the copy's ## Check section" for n, m in (("outside", outside), ("tests/", tests)) if not m
    84	    ]
    85	    excluded = ["tests/", ".orchestration/"]
    86	    if outside:
    87	        excluded = re.findall(r"`([^`]+)`", re.split(r",\s*(?:and\s+)?\d", outside.group(2))[0]) or excluded
    88	
    89	    def counted(path, prefixes):
    90	        return any(path == p or (p.endswith("/") and path.startswith(p)) for p in prefixes)
    91	
    92	    out_lines = sum(a + d for a, d, p in numstat if not counted(p, excluded))
    93	    test_lines = sum(a + d for a, d, p in numstat if counted(p, ["tests/"]))
    94	    found = []
    95	    if outside and out_lines > int(outside.group(1)):
    96	        found.append(f"{out_lines} changed lines outside {', '.join(excluded)} exceed {outside.group(1)}")
    97	    if tests and test_lines > int(tests.group(1)):
    98	        found.append(f"{test_lines} changed lines under tests/ exceed {tests.group(1)}")
    99	    return found, missing
   100	
   101	
   102	def front(data):
   103	    """Return a copy's front matter mapping, or None when it is unreadable or not a mapping."""
   104	    try:
   105	        fm = yaml.safe_load(data.decode().split("\n---\n", 1)[0].lstrip("-\n"))
   106	    except (UnicodeDecodeError, yaml.YAMLError):
   107	        return None
   108	    return fm if isinstance(fm, dict) else None
   109	
   110	
   111	def precheck(root, head, t, result_text, exempt=()):
   112	    """Return the violations of precheck.json's binding, or None when the task carries no precheck.json."""
   113	    data = show(root, head, f".orchestration/{t}/precheck.json")
   114	    if data is None:
   115	        return None
   116	    try:
   117	        doc = json.loads(data)
   118	    except ValueError as error:
   119	        return [f"precheck.json is not JSON: {error}"]
   120	    found = []
   121	    bound = doc.get("head") if isinstance(doc, dict) else None
   122	    if not isinstance(bound, str) or not re.fullmatch(r"[0-9a-f]{40}", bound):
   123	        found.append(f"precheck.json head {bound!r} is not a 40-hex commit id")
   124	    elif bound != head:
   125	        # precheck.json cannot name the commit that adds it: it names the code commit, and the head may add only
   126	        # this task's evidence on top (the evidence-only ancestor rule of verdict.sh condition 1)
   127	        if git(root, "merge-base", "--is-ancestor", bound, head).returncode:
   128	            found.append(f"precheck.json head {bound} is neither the head {head} nor its ancestor")
   129	        elif other := [
   130	            p
   131	            for p in listed(root, "diff", "--name-only", "--no-renames", bound, head)
   132	            if not p.startswith((f".orchestration/{t}/", *exempt))
   133	        ]:
   134	            found.append(
   135	                f"precheck.json head {bound[:12]} differs from the head outside .orchestration/{t}/: {', '.join(other)}"
   136	            )
   137	    if token(result_text, "precheck") != sha256(data):
   138	        found.append(
   139	            f"precheck.json sha256 {sha256(data)} is not result.txt's precheck={token(result_text, 'precheck')}"
   140	        )
   141	    return found
   142	
   143	
   144	def policy(root, base, head, t):
   145	    """Return (the policy bytes, its front matter or None, whether the base's dispatched text is the policy)."""
   146	    dispatched = show(root, base, f".orchestration/tasks/{t}.md")
   147	    data = show(root, head, f".orchestration/{t}/task.md") if dispatched is None else dispatched
   148	    return data, front(data), dispatched is not None
   149	
   150	
   151	def checker(root, data):
   152	    """Return the base checker's violations on the base's dispatched bytes: it hands the text's literals to git (C8 to
   153	    C10) and opens its design path (C6), so a pull request's own text never reaches it (worker review P0 of bcbd6949)."""
   154	    with tempfile.TemporaryDirectory() as scratch:
   155	        cmd = [*CHECKER_RUN, "--root", root, str(Path(scratch, "task.md"))]
   156	        Path(cmd[-1]).write_bytes(data)
   157	        run = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
   158	    out = run.stdout.splitlines()  # the file is task.md, so C1 compares task_id with `task`; task-id checks <t>
   159	    # only the checker's own verdict line with its exit code counts; a crash also exits 1, with no verdict line
   160	    if (out[:1], run.returncode) not in ((["task.md: OK"], 0), (["task.md: FAIL"], 1)):
   161	        return [("checker", f"no verdict (exit {run.returncode}): {(run.stdout + run.stderr).strip()[-300:]}")]
   162	    lines = [ln.strip() for ln in out[1:] if ln.strip()]
   163	    return [("checker", ln) for ln in lines if not re.fullmatch(r"C1 task_id .* != file task", ln)]
   164	
   165	
   166	def check_task(root, base, head, t, changed, numstat):
   167	    """Return (violations, warnings) for one task, each violation a (rule, detail) pair."""
   168	    copy_path = f".orchestration/{t}/task.md"
   169	    copy = show(root, head, copy_path)
   170	    if (fm := front(copy)) is None:
   171	        return [("front-matter", f"{copy_path} is unreadable or has no front matter mapping")], []
   172	    data, rules, dispatched = policy(root, base, head, t)
   173	    if rules is None:
   174	        return [("front-matter", f"the base's .orchestration/tasks/{t}.md has no front matter mapping")], []
   175	    found, warnings = [], []
   176	    if fm.get("task_id") != t:
   177	        found.append(("task-id", f"the copy's task_id {fm.get('task_id')!r} is not its directory {t}"))
   178	    result = show(root, head, f".orchestration/{t}/result.txt")
   179	    result_text = result.decode(errors="replace") if result is not None else ""
   180	    if dispatched:
   181	        if data != copy:
   182	            found.append(("task-copy", f"{copy_path} differs from the base's dispatched .orchestration/tasks/{t}.md"))
   183	    else:  # the copy's own policy is provisional: a head file or a result.txt token is a claim, never authentication
   184	        unverifiable = "task copy unverifiable (no dispatched text at base)"
   185	        found += [("task-copy", unverifiable)] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else []
   186	        warnings += [] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else [unverifiable]
   187	        warnings.append("checker skipped: the copy is unverifiable, and the base's checker reads only the base's text")
   188	        if result is not None and token(result_text, "task_copy") != sha256(copy):
   189	            found.append(
   190	                ("task-copy", f"sha256 {sha256(copy)} is not result.txt's task_copy={token(result_text, 'task_copy')}")
   191	            )
   192	    found += checker(root, data) if dispatched else []
   193	    exempt = tuple(f".orchestration/{p}/" for p in rules.get("reset_of") or [] if isinstance(p, str))
   194	    bound = precheck(root, head, t, result_text, exempt)
   195	    if bound is None:
   196	        warnings.append("precheck absent")
   197	    found += [("precheck", detail) for detail in bound or []]
   198	    entries = [a for a in rules.get("allowed_files") or [] if isinstance(a, str)]
   199	    found += [
   200	        ("allowed-files", f"{p} is outside allowed_files")
   201	        for p in changed
   202	        if not p.startswith(exempt) and not any(allowed(p, a) for a in entries)
   203	    ]
   204	    exceeded, cap_warnings = caps(data.decode(errors="replace"), numstat)
   205	    found += [("caps", detail) for detail in exceeded]
   206	    return found, warnings + cap_warnings
   207	
   208	
   209	def main(argv=None):
   210	    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   211	    parser.add_argument("--base", required=True, help="the base ref, such as origin/main")
   212	    parser.add_argument("--head", required=True, help="the pull request's head commit")
   213	    parser.add_argument("--root", help="the base checkout (default: the current git toplevel)")
   214	    args = parser.parse_args(argv)
   215	    root = args.root or git(".", "rev-parse", "--show-toplevel").stdout.decode().strip() or "."
   216	    shas = [
   217	        git(root, "rev-parse", "--verify", "--quiet", f"{r}^{{commit}}").stdout.decode().strip()
   218	        for r in (args.base, args.head)
   219	    ]
   220	    if not all(shas):
   221	        print(f"regime-ci: cannot resolve --base {args.base} or --head {args.head} in {root}")
   222	        return 2
   223	    base, head = shas
   224	    at = git(root, "rev-parse", "HEAD").stdout.decode().strip()  # the verifier and the checker must be the base's
   225	    if at != base:
   226	        print(
   227	            f"regime-ci: checkout: {root} is at {at[:12]}, not the base {base[:12]}, so the code run would not be the base's"
   228	        )
   229	        return 1
   230	    try:
   231	        changed = listed(root, "diff", "--name-only", "--no-renames", f"{base}...{head}")
   232	        numstat = []
   233	        for row in listed(root, "diff", "--numstat", "--no-renames", f"{base}...{head}"):
   234	            added, deleted, path = row.split("\t", 2)  # a path may hold a tab; a binary file counts 0 lines
   235	            numstat.append((int(added) if added.isdigit() else 0, int(deleted) if deleted.isdigit() else 0, path))
   236	    except GitError as error:
   237	        print(f"regime-ci: {error}")
   238	        return 2
   239	    for path in sorted(set(changed) & set(RUNS)):
   240	        print(
   241	            f"regime-ci: warning: the diff changes {path}; this run executed the base's version, the audit reads the change"
   242	        )
   243	    dirs = sorted({m.group(1) for p in changed if (m := re.match(r"\.orchestration/([^/]+)/", p))})
   244	    targets = [t for t in dirs if show(root, head, f".orchestration/{t}/task.md") is not None]
   245	    if not targets:
   246	        stray = [p for p in changed if not p.startswith(".orchestration/")]
   247	        if not stray:  # content alone decides: a branch name is the pull request's own claim
   248	            print("regime-ci: no target (records-only)")
   249	            return 0
   250	        print(
   251	            f"regime-ci: no target: {len(stray)} changed path(s) outside .orchestration/ and no task copy, first {stray[0]}"
   252	        )
   253	        return 1
   254	    # Amendment 1: a later copy whose reset_of names an earlier one is the lineage's only target, when both verify
   255	    policies = {t: policy(root, base, head, t) for t in targets}
   256	    exact = {t: policies[t][2] and show(root, head, f".orchestration/{t}/task.md") == policies[t][0] for t in targets}
   257	    later = {
   258	        p: t
   259	        for t, (_, rules, _) in policies.items()
   260	        for p in (rules or {}).get("reset_of") or []
   261	        if p in policies and p != t and exact[t] and exact[p]  # both head copies equal their base texts
   262	    }
   263	    for p, t in sorted(later.items()):
   264	        print(f"regime-ci: warning: {p}: predecessor copy .orchestration/{p}/task.md (reset_of of {t})")
   265	    targets = [t for t in targets if t not in later]
   266	    failed = False
   267	    for t in targets:
   268	        try:
   269	            found, warnings = check_task(root, base, head, t, changed, numstat)
   270	        except GitError as error:
   271	            found, warnings = [("git", str(error))], []
   272	        for detail in warnings:
   273	            print(f"regime-ci: warning: {t}: {detail}")
   274	        for rule, detail in found:
   275	            print(f"regime-ci: {t}: {rule}: {detail}")
   276	        failed |= bool(found)
   277	    if not failed:
   278	        print(f"regime-ci: ok {len(targets)} task(s)")
   279	    return int(failed)
   280	
   281	
   282	if __name__ == "__main__":
   283	    sys.exit(main())

**Checking git references**
codex
前回の指摘を受け、実行ファイルの選択・GIT_DIR の継承・sandbox の例外は残余リスクとして明記されています。現在は、修正後の文章に残る「closed」の範囲と、参照先の対策・テストで裏付けられる範囲を照合しています。
exec
/bin/zsh -lc "cat .github/workflows/regime.yml
rg -n 'test_the_regime|test_regime_ci_runs|environment|env=|minimal|token' tests/unit/test_regime_ci.py
rg -n '"'^### 5'"\\.14|"'^### 5'"\\.15|D-024-(21|29|30)' .orchestration/plans/024-design-quality.md .orchestration/decisions.tsv
cat .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md" in ~/Workspace/dotfiles
 succeeded in 21ms:
name: regime

# The regime job (plan 024 P1-11, redesigned in T133 regime-ci a02): a pull request that carries a task copy is checked
# by the base's scripts/orchestrator/regime-ci.py against the base's dispatched policy. pull_request_target runs this
# workflow as it is on the base; the pull request's head is fetched as data and is never checked out or executed.
# It is an optional check until the operator adds `regime` to the ruleset's required contexts.
on:
  pull_request_target:
    types: [opened, synchronize, reopened, ready_for_review]

concurrency:
  group: regime-pr-${{ github.event.pull_request.number }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  regime:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
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
        run: uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "$(git rev-parse HEAD)" --head "${HEAD_SHA}"
36:        "workflow and interpreter or environment inputs",
61:            cmd, cwd=self.repo, env=self.env, check=True, capture_output=True, text=True
73:        self, copy=TASK, dispatched=TASK, code=None, precheck_head=None, precheck_token=None, evidence=True, **more
78:        `task_copy` as result.txt's token, `checker` as the base's checker, `base` as more base files, `branch` as the
99:            token = precheck_token or hashlib.sha256(pre.encode()).hexdigest()
100:            copy_token = more.get("task_copy") or hashlib.sha256(copy.encode()).hexdigest()
101:            result = f"AGMSG-RESULT v1 task_id={T} precheck={token} task_copy={copy_token}\n"
119:            cmd, cwd=self.repo, env=self.env | env, capture_output=True, text=True, timeout=120, check=False
124:        # that pass and leave markers, and forges a dispatched text with a matching result token; the base's policy,
208:        # result.txt token, a dispatched file of its own); a warning until REGIME_REQUIRE_DISPATCHED=1, then a violation.
225:    def test_the_regime_workflow_runs_base_code_only(self):
296:            "precheck sha": ({"precheck_token": "0" * 64}, "is not result.txt's precheck=" + "0" * 64),
323:    def test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config(self):
329:        # a02 item 6: result.txt's token is a consistency check among the pull request's own records, not authentication
346:            env=self.env,
381:                token, copy = hashlib.sha256(pre.encode()).hexdigest(), hashlib.sha256(text.encode()).hexdigest()
383:                evidence[f".orchestration/{later}/result.txt"] = f"AGMSG-RESULT v1 precheck={token} task_copy={copy}\n"
.orchestration/plans/024-design-quality.md:95:### 5.14 残余（凍結後の計測事実、D-024-29）
.orchestration/plans/024-design-quality.md:113:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
.orchestration/decisions.tsv:67:D-024-21	2026-10-19T04:0xZ	threat model and mechanism of the worker boundary: the host is not a security boundary between seats sharing one OS user; the hard boundary is GitHub (protected main, required checks, the orchestrator identity merge); approvals and gate evidence of record are read from GitHub at a sha through the API inside the sandbox; Claude worker seats run under their own CLAUDE_CONFIG_DIR (~/.claude-worker: no excluded commands, no Herdr socket, Edit denies on trusted paths with symlink coverage, failIfUnavailable true, minimal trusted hooks with onFailure block); host-local controls target accidental and injected damage and the texts say so (design 5.14 items 0, 1, 8)	three C-80 reviews of the P1-15 text (03:24Z, 03:42Z, 03:58Z) found host-level escapes no in-process check closes (symlink swap race, writable object database, hook descendants through shims, Herdr socket RPC, hook timeout fail-open); the documentation confirms per-directory settings and credentials (one operator login for the worker directory), onFailure block (>= 2.1.295; installed 2.1.300), and symlink-aware file-tool deny rules	default under the autonomy directive, reported 2026-10-19 13:0x JST; the worker-directory login is an operator step at the P1-15 deployment; scope=design,permission	applied-to-the-P1-15-text
.orchestration/decisions.tsv:77:D-024-29	2026-10-19T21:39Z	Design 5.14 is frozen (plan 006 A1: three review rounds, then freeze with a residual list): items 0-10 are the contract; a text review finding that needs a new design sentence is recorded in the design's residual list and as an owner row, not as an amendment of the item and of the text under review, unless it names a P0/P1 that is exploitable in the proposed implementation.	items 1, 2, 3, 8 and 9 were amended five times on 10-19/20 (one per review round of P1-15 and P1-12), each amendment re-opening the texts that quote the item (C-88) and costing a review round each; the texts chased a moving design.	plan 006 A1; M-20261019-05; C-92	applied from 06:40 JST; the residual list is a new subsection `5.14 残余` in 024-design-quality.md (written at the next design edit)
.orchestration/decisions.tsv:78:D-024-30	2026-10-19T23:16Z	A task text applies design 5.14 by reference: it names the items it relies on (`design: 5.14 items 2, 3, 8, 9`) and carries one threat row per item 0-10 in the item's own words, never a restated or paraphrased copy of the item; C-88 is narrowed to the exact contract sentences a test asserts; the task-consistency check gains a rule (C16) that a security: true orchestrator-side text names 5.14 and has the per-item rows (owner: the P1-12 follow-up after a04 frees task-consistency-check.py).	restated design text drifted in every reset text and re-opened a review round at each design amendment (P1-15: 23 review rounds; P1-12: 4); by-reference texts stay within proposal 1's caps and a mechanical check replaces the reviewer's paraphrase comparison; the operator's direction of 2026-10-19T22:59Z (relayed by a011) asks for the same.	plan 006 A1; D-024-29; M-20261019-05; proposal 1	applied from 08:15 JST to new texts (trusted-exec-contract-tests-a01 first); existing correct texts are not rewritten
.orchestration/decisions.tsv:82:D-024-34	2026-10-20T04:12Z	The files the worker's loader consumes at start and the regime need not preserve are launcher-generated at every start: the global state file `CLAUDE_CONFIG_DIR/.claude.json` is written from the declared shape (empty `mcpServers`, `projects` with exactly the validated identities and Boolean trust, `hasCompletedOnboarding: true`) plus identity fields carried from the previous file after screening (`oauthAccount` string members, `userID`); native persisted state (`numStartups`, onboarding, tips and changelog caches, per-project history, allowedTools, cost counters) is neither screened nor preserved; refusal with a named message stays for declared-structure violations (non-empty top-level `mcpServers`, undeclared project keys, non-Boolean trust flags, undeclared object or array members), as evidence of tampering. `CLAUDE_ENV_FILE` (amendment 1) belongs to the same family. A loader that requires another preserved field blocks and retasks (the text's rule), never widens silently.	a010's probe of the installed loader (2.1.300, sha256 475517ca…; reproduced by the orchestrator at 04:10Z) shows the loader itself writes fields outside any exact schema, so the allowlist re-plan's closed schema (D-024-29/30 lineage, a02 -> a03) refuses the worker's own state at the next start; a per-version native-field table would block every loader update until re-probed; generating the file realises design 5.14 item 1 (refuse any executable payload it did not write) by writing the whole file. Second re-plan of the input-inventory family (rows text-security:f7af699:1, worker:5067ed0:1 after the allowlist re-plan).	design 5.14 item 1; D-024-29; D-024-30; a03 record rows; M-20261019-05	applied 13:12 JST as a03 amendment 2 (review-profile text, C-80 round 3); the operator may redirect it once per class (the 13:15 JST report)
.orchestration/decisions.tsv:85:D-024-37	2026-10-20T06:43Z	New `security: true` mechanism texts are held until the trusted-execution contract (`tests/unit/trusted_exec_contract.py`, PR #436) and the P1-15 launcher (PR #431) are on main; a held text then names those controls by reference (C-88) instead of restating the contract, and takes one C-80 round. Held now: dotfiles-T133-record-json-sync-a01 (two rounds: 1 P1 + 9 P2, all of the trusted-execution family) and dotfiles-T133-records-sync-pr-a01 (round 1: 2 P1 + 2 P2 of the same family; amendment 1 installed, review deferred).	the two texts cost three review rounds in 40 minutes and every finding re-derived the contract the two in-flight PRs land (git configuration isolation, resolved-root binding, replace refs, the agmsg-dispatch exclusion); continuing is the whack-a-mole the operator forbade, while the seats they were meant for (a011, a009) have no other dispatchable text until #438 merges.	C-88; D-024-29/30; M-20261019-05 (text review rounds unbounded); the record-json-sync record	applied 15:43 JST; the Claude seats' idle time until #438 is the operator's approval, not a text gap
.orchestration/decisions.tsv:93:D-024-45	2026-10-20T11:45Z	Design 5.14 item 10 (every worker command inside the sandbox) contradicts the seat configuration that runs `agmsg-dispatch` through excludedCommands outside the sandbox (audit:7eab146:1, audit:6434c27:1; the a008 seat's sandbox.md:18). The design is frozen (D-024-29), so the choice is the operator's: default = record a control-plane exemption for `agmsg-dispatch` in 5.14 item 10 by a design-amendment task (the bus is the regime's control plane, not a repository mutation; the herdr socket is already in the sandbox allowlist, so the alternative, running it inside, is tested first by a Claude seat); until decided, the finding is recorded as it stands on every affected lineage and never dispositioned fixed. Placed in the project map's decisions panel with that default.	claude-deep-dot
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-task-generator-plan-check-a06-checker round=1 reset_of=dotfiles-T133-task-generator-plan-check-a05-checker repo=~/Workspace/dotfiles/.claude/worktrees/worker-g task_file=.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md task_sha256=90ca0ae9563df4b352dfb26c6b6aa60132386e15ce9ff50bcf998a43097a12e6 deadline=none done_signal=AGMSG-RESULT note=a012:reset-a06(D-024-39:measured-cap-440/700-for-the-canonical-path-pipeline-re-plan;your-uncommitted-draft-is-this-round's-content,plus-amendment-1's-identity-aware-matching-and-path-collision-refusal-with-the-two-file-regression;C-80-73ac933-correct;PR-440-continues-from-06ffefbc;add-the-a06-task-copy-and-records,keep-the-a05-copy;commit-locally-and-PONG-the-head-for-transport;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0)"
  ],
  "format": 1,
  "head": null,
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
  "pr": null,
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
  "searches": [],
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

**Assessing output secrecy risks**
**Reviewing residual token handling**
exec
/bin/zsh -lc "sed -n '95,145p' .orchestration/plans/024-design-quality.md
sed -n '220,262p' tests/unit/test_regime_ci.py
sed -n '310,330p' tests/unit/test_regime_ci.py
git show 2cb584823ccf5f22069ea925b252d8cefb020844:scripts/orchestrator/regime-ci.py | sed -n '145,178p'
git show 2cb584823ccf5f22069ea925b252d8cefb020844:scripts/orchestrator/task-consistency-check.py | sed -n '1,208p'" in ~/Workspace/dotfiles
 succeeded in 80ms:
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
                self.assertEqual(1, flagged.returncode, flagged.stdout)
                self.assertIn(
                    f"regime-ci: {T}: task-copy: task copy unverifiable (no dispatched text at base)", flagged.stdout
                )

    def test_the_regime_workflow_runs_base_code_only(self):
        # Bot P1 4308651010 (a02 items 1, 5): pull_request_target runs the base's workflow and verifier; the head is a
        # fetched ref read as data, never checked out or executed.
        read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1])), default=str))"
        cmd = [*UV, "-c", read, str(ROOT / ".github/workflows/regime.yml")]
        doc = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
        types = ["opened", "synchronize", "reopened", "ready_for_review"]
        self.assertEqual({"pull_request_target": {"types": types}}, doc.get("on", doc.get("true")))
        self.assertEqual(({"contents": "read"}, ["regime"]), (doc["permissions"], list(doc["jobs"])))
        job = doc["jobs"]["regime"]
        self.assertEqual(("ubuntu-24.04", 10, None), (job["runs-on"], job["timeout-minutes"], job.get("permissions")))
        group = doc["concurrency"]
        self.assertEqual(
            ("regime-pr-${{ github.event.pull_request.number }}", True), (group["group"], group["cancel-in-progress"])
        )
        steps = job["steps"]
        pins = [
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7",
        ]
        self.assertEqual(pins, [s["uses"] for s in steps if "uses" in s])
        base = "refs/heads/${{ github.base_ref }}"  # the tip at run time, never a stale base sha (ci:39185982423:1)
        self.assertEqual({"fetch-depth": 0, "ref": base, "persist-credentials": False}, steps[0]["with"])
        self.assertEqual({"enable-cache": False}, steps[1]["with"])
        runs = [s for s in steps if "run" in s]
        fetch, verify = runs
        self.assertIn('git fetch --no-tags origin "refs/pull/${PR_NUMBER}/head:refs/regime/pr-head"', fetch["run"])
        self.assertIn('test "$(git rev-parse refs/regime/pr-head)" = "${HEAD_SHA}"', fetch["run"])
        line = 'uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "$(git rev-parse HEAD)" --head "${HEAD_SHA}"'
        self.assertEqual(line, verify["run"])
        head = "${{ github.event.pull_request.head.sha }}"
        self.assertEqual(({"HEAD_SHA": head}, head), (verify["env"], fetch["env"]["HEAD_SHA"]))
        for step in steps:  # no step checks out, switches to or runs anything from the head
            self.assertNotIn("${{", step.get("run", ""))
            self.assertNotRegex(step.get("run", ""), r"git (checkout|switch|worktree|reset)|pr-head:|\./")
            given = json.dumps(step.get("with", {})).replace("refs/heads/", "")  # the base branch's namespace only
            self.assertNotRegex(given, r"head|merge_commit_sha|event\.after|pull/")
            self.assertFalse(step.get("uses", "x").startswith("./"))
                "no verdict (exit 1): task.md: OK",
            ),
            "checker crash": ({"copy": crash, "dispatched": crash}, "no verdict (exit 1)"),
        }
        for case, (change, phrase) in breaks.items():
            with self.subTest(case=case):
                result = self.build(**change)
                found = [ln for ln in result.stdout.splitlines() if ln.startswith(f"regime-ci: {T}: ")]
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(1, len(found), result.stdout)
                self.assertTrue(found[0].startswith(f"regime-ci: {T}: {case.split()[0]}: "), found)
                self.assertIn(phrase, found[0])

    def test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config(self):
        # --no-config: a .python-version (or uv.toml) in the checkout cannot steer the checker's uv run
        result = self.build(base={".python-version": "3.99\n"})
        self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)

    def test_regime_ci_checks_the_copy_against_result_txt_without_dispatched_text(self):
        # a02 item 6: result.txt's token is a consistency check among the pull request's own records, not authentication
        unverifiable = f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at base)"
    """Return (the policy bytes, its front matter or None, whether the base's dispatched text is the policy)."""
    dispatched = show(root, base, f".orchestration/tasks/{t}.md")
    data = show(root, head, f".orchestration/{t}/task.md") if dispatched is None else dispatched
    return data, front(data), dispatched is not None


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
        return [("checker", f"no verdict (exit {run.returncode}): {(run.stdout + run.stderr).strip()[-300:]}")]
    lines = [ln.strip() for ln in out[1:] if ln.strip()]
    return [("checker", ln) for ln in lines if not re.fullmatch(r"C1 task_id .* != file task", ln)]


def check_task(root, base, head, t, changed, numstat):
    """Return (violations, warnings) for one task, each violation a (rule, detail) pair."""
    copy_path = f".orchestration/{t}/task.md"
    copy = show(root, head, copy_path)
    if (fm := front(copy)) is None:
        return [("front-matter", f"{copy_path} is unreadable or has no front matter mapping")], []
    data, rules, dispatched = policy(root, base, head, t)
    if rules is None:
        return [("front-matter", f"the base's .orchestration/tasks/{t}.md has no front matter mapping")], []
    found, warnings = [], []
    if fm.get("task_id") != t:
        found.append(("task-id", f"the copy's task_id {fm.get('task_id')!r} is not its directory {t}"))
    result = show(root, head, f".orchestration/{t}/result.txt")
"""Read-only cross-field check of a format-2 task file, before dispatch and at acceptance (plan 007 T704).

`uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py [--root <repo>] <task.md>...`
reads canonical GitHub design/baseline bytes (C6, C8 to C10) under --root (default: the first file's git
toplevel), prints `<file name>: OK` or `: FAIL` with one `  C<n> ...` line per finding, and exits 1 when any file fails.
C1 task_id equals the file name.
C2 allowed_files covers .orchestration/<task_id>/** and names no other task's .orchestration/<id>/ directory.
C3 when reset_of is non-empty, a threat_table row names every reset_of id's task.md and the task's own.
C4 every allowed_files entry (its path before any glob) is named in a row's control, followed by its end, a space, / " ' ( ) , or a glob.
C5 no residual binds a predecessor's hash ("names the <aNN> file's hash") instead of the task's own.
C6 design_review.receipt is the design file's current design_review.receipt.
C7 one row per non-path control name and per orchestrator effect name (the SKILL row unit).
C7b no row other than a non-path control names two allowed_files entries (one row per entry).
C8 (code tasks) every *_EVIDENCE input the body names and origin/main does not read yet has a threat row.
C9 (docs tasks) a quoted rule sentence naming a script, *_EVIDENCE, a check id or classes: finds it on origin/main or says once/until.
C10 (docs tasks) a quoted rule sentence naming a script on origin/main has no `=` or `[...]` literal absent from the script and its test.
"""

import argparse
import base64
import fnmatch
import hashlib
import json
import os
import pathlib
import pwd
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from functools import cache
from urllib.parse import quote

CACHE = os.environ.get("UV_CACHE_DIR")

try:
    import yaml
except ImportError:
    print("needs pyyaml: run with uv run --no-project --with pyyaml")
    sys.exit(2)

ROW_UNIT = "task metadata|metadata separators|in-process effects|workflow and interpreter or environment inputs|new or renamed scripts|orchestrator effect merge|orchestrator effect update-branch|orchestrator effect forced worker removal"
C7_NAMES = ROW_UNIT.split("|")
NONPATH = ("in-process effects", "task metadata", "metadata separators", "workflow and interpreter")
NONPATH += ("new or renamed scripts", "orchestrator effect")
C9_NAMES = r"(scripts/[\w./-]+|\b[A-Z][A-Z_]{3,}_EVIDENCE\b|task-consistency-check C\d|\bC\d\b of the task-consistency check|\bclasses:)"
CHECKER = "scripts/orchestrator/task-consistency-check.py"  # where `task-consistency-check C<n>` lands
TRUST_ROOT = pathlib.Path(__file__).resolve().parents[2]
HOST_HOME = pathlib.Path(pwd.getpwuid(os.getuid()).pw_dir)
FORMS = ("closed: ", "residual: ", "out-of-scope: ")
APPLIED = (".sh", ".py", ".yaml", ".yml", ".json", ".toml")
APPLIED_DIRS = ("home/", "scripts/", ".githooks/", ".github/")
UNTRUSTED = "C14: not run (no trusted sha)"  # a warning: the file is not the text --premises-sha names (revise 1)


def normalise_name(value):
    if not isinstance(value, str):
        return None
    parts = value.split("/")
    if not value or pathlib.PurePosixPath(value).is_absolute() or "\0" in value or ".." in parts or "\\" in value:
        return None
    name = "/".join(p for p in parts if p not in ("", "."))
    if not name or name[0] in ":!":
        return None
    return unicodedata.normalize("NFC", name) + ("/" if value.endswith(("/", "/.")) else "")


def confined(root, rel):
    if not root.exists():
        return None
    path = (root / rel).resolve()
    return next(
        ((path, path.relative_to(p)) for p in (path, *path.parents) if p.exists() and os.path.samefile(p, root)), None
    )


def path_entry(root, value, fold=os.path.normcase):
    raw = root / value if isinstance(value, pathlib.Path) or normalise_name(value) else None
    found = confined(root, raw) if raw is not None else None
    key = fold(unicodedata.normalize("NFC", raw.relative_to(root).as_posix())) if raw is not None else None
    if key and str(value).endswith(("/", "/.")):
        key += "/"
    return raw, found[0] if found else None, key


def front(text):
    return yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))


def trusted(path):
    raw = pathlib.Path(path)
    path = raw.resolve()
    if not raw.is_absolute() or "shims" in raw.parts or "shims" in path.parts:
        sys.exit("refused: absolute non-shim trusted path required")
    manifest = TRUST_ROOT / "home/dot_agents/agent-config.yaml"
    worker = (yaml.safe_load(manifest.read_text()) or {}).get("worker_worktree") if manifest.is_file() else None
    if ".claude/worktrees" in os.path.normpath(path).casefold() or (
        worker and confined(TRUST_ROOT / worker, path) is not None
    ):
        sys.exit("refused: worker-root trusted path")
    if not path.is_file() or not os.access(path, os.X_OK):
        sys.exit("refused: trusted executable must be an absolute regular executable file")
    return path


resolver = TRUST_ROOT / "scripts/orchestrator/trusted-interpreter.sh"
if resolver.exists() or resolver.is_symlink():
    command = ["/bin/bash", "--noprofile", "--norc", "-p", str(trusted(resolver))]
    env = {"PATH": "/usr/bin:/bin", "HOME": str(HOST_HOME), "LANG": "C.UTF-8"}
    result = subprocess.run(command, env=env, capture_output=True, text=True, check=False)
    if result.returncode:
        sys.exit("refused: interpreter resolver failed: " + result.stderr)
    selected = result.stdout.strip()
elif "TRUSTED_PYTHON" in os.environ:
    selected = os.environ["TRUSTED_PYTHON"]
else:
    selected = os.path.realpath(sys.executable)
    print("warning: interpreter fallback to real sys.executable", file=sys.stderr)
PYTHON = trusted(selected)


@cache
def executable(name):
    supplied = os.environ.get("TRUSTED_BIN_DIR")
    path = pathlib.Path(supplied) / name if supplied is not None else shutil.which(name)
    if not path or (supplied and (not os.path.isabs(supplied) or not path.is_symlink())):
        sys.exit("refused: trusted executable binding missing: " + name)
    return trusted(path)


def launch(root, binary, *args):
    binary = trusted(binary)
    if confined(pathlib.Path(root).resolve(), binary) is not None:
        sys.exit("refused: checkout executable binding")
    if CACHE is not None:
        if not os.path.isabs(CACHE):
            sys.exit("refused: UV_CACHE_DIR must be an absolute path")
        os.makedirs(CACHE, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=CACHE, prefix="checker-") as directory:
        env = {"HOME": str(HOST_HOME), "PATH": directory, "LANG": "C.UTF-8", "UV_CACHE_DIR": CACHE or directory}
        env.update(
            v.split("=", 1)
            for v in "GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 GIT_NO_REPLACE_OBJECTS=1".split()
        )
        if args and args[0] == "api":
            env.update({k: os.environ[k] for k in ("GH_TOKEN", "GITHUB_TOKEN") if k in os.environ})
        return subprocess.run(
            [str(binary), *map(str, args)], cwd=root, env=env, capture_output=True, text=True, check=False
        )


def git(cwd, *args):
    root = pathlib.Path(cwd).resolve()
    if (root / ".gitmodules").exists() or (root / ".gitmodules").is_symlink():
        sys.exit("refused: .gitmodules")
    flags = ["-C", str(root), f"--git-dir={root / '.git'}", f"--work-tree={root}"]
    for setting in "core.hooksPath=/dev/null core.fsmonitor=false submodule.recurse=false protocol.allow=never protocol.https.allow=always".split():
        flags += ["-c", setting]
    binary = executable("git")
    config = launch(root, binary, *flags, "config", "--show-origin", "--get-regexp", r"^filter\.|^core\.worktree$")
    if config.returncode not in (0, 1) or config.stdout:
        sys.exit("refused: Git configuration: " + config.stdout + config.stderr)
    top = launch(root, binary, *flags, "rev-parse", "--show-toplevel")
    if top.returncode or not os.path.samefile(top.stdout.strip(), root):
        sys.exit("refused: Git toplevel mismatch")
    return launch(root, binary, *flags, *args)


@cache
def main_entry(root, name=None):
    if name is None:
        endpoint, args = "git/ref/heads/main", ("--jq", ".object.sha")
    else:
        if not normalise_name(name):
            sys.exit("refused: canonical path")
        name = pathlib.PurePosixPath(name).as_posix()
        endpoint, args = f"contents/{quote(name.rstrip('/'), safe='/')}?ref={main_entry(root)}", ()
    endpoint = "repos/mryfmo/dotfiles/" + endpoint
    result = launch(root, executable("gh"), "api", endpoint, "--hostname", "github.com", *args)
    print("api-input-sha256 " + hashlib.sha256((result.stdout + result.stderr).encode()).hexdigest(), file=sys.stderr)
    if name is None:
        sha = result.stdout.removesuffix("\n")
        if result.returncode or not re.fullmatch(r"[0-9a-f]{40}", sha):
            sys.exit("refused: canonical main SHA unavailable")
        print("canonical-main " + sha, file=sys.stderr)
        return sha
    if result.returncode:
        if "HTTP 404" in result.stderr:
            return None
        sys.exit("refused: canonical contents unavailable")
    try:
        entry = json.loads(result.stdout)
        if not isinstance(entry, (dict, list)):
            raise ValueError()
        return entry
    except ValueError:
        sys.exit("refused: invalid canonical contents response")


@cache
def main_bytes(root, name):
    entry = main_entry(root, name)
    if entry is None:
        return None
    try:

**Reviewing environment setup concerns**
web search: 
web search: https://docs.astral.sh/uv/reference/cli/#uv-run--no-project
**Evaluating test environment assumptions**
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-worker-sandbox-exclusions-a02.md
cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a06-checker-security-2cb5848.md.last.md
ls -ld "$HOME/.local/bin/mise" "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3"
shasum -a 256 .orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md
sed -n '"'1,125p' tests/unit/test_regime_ci.py" in ~/Workspace/dotfiles
 succeeded in 39ms:
# Acceptance record: dotfiles-T133-worker-sandbox-exclusions-a02

Lineage: reset of dotfiles-T133-worker-sandbox-exclusions-a01 (INV-6 S2, two amendments before implementation, both orchestrator brief defects). Design 5.14 item 10's Claude half: empty the worker seats' excludedCommands (`agmsg-dispatch *` and the three Linux entries), regenerate the rendered Claude settings, make the validator expect the empty list, update the two tests that assert the old lists. Evidence carried by the orchestrator: this seat sent agmsg messages 2827 and 2830 on 2026-10-20 from sandboxed Bash (Claude sandbox, herdr socket allowlisted since T130); the Codex seat a013 measured `PermissionDenied` on the same socket from its sandbox (13:39Z), the Codex half's open point.

- 2026-10-20T14:03Z-14:11Z: text written whole by the review profile from the orchestrator's brief (`worker-sandbox-exclusions-a02-prompt.md`), installed, two checker fixes by the orchestrator (`reset_of` as a list; the predecessor-copy threat row C3 requires of a reset), 125 lines, self cap 140; pre-send OK, sha256 6f95aef556842405912d7a929d19b95ba95efaa8c2b0e61c72d1ae925e5cc7fc. C-80 round 1 started 14:11Z.

## Owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01

(no advisory rows yet; written 2026-10-20T14:17Z before the worker-sandbox-exclusions PR's first advisory disposition, C-51; the owner text carries the lineage's residual rows as items)
- 2026-10-20T14:21Z: C-80 round 1 one P2 (the owner text `dotfiles-T133-worker-sandbox-exclusions-followup-a01` did not exist) -> owner text written with the Linux runtime check as its item 2; round 2 `Verdict: correct` (`…-text-security-6f95aef.md.last.md`). Dispatched to a013 (TASK 2863, read 14:22:00Z) through send-task.sh at the reviewed bytes 6f95aef5…; the author omitted the fenced block under `## Checks`, so no checks were pasted (the dispatched bytes are the reviewed bytes; the pre-send output is in this record instead: checker OK, secret-pattern 0, 125 lines of 140).

Two findings in head `2cb584823ccf5f22069ea925b252d8cefb020844`:

- **P2 · High confidence — `scripts/orchestrator/task-consistency-check.py:476`:** C12 classifies only the resolved target, allowing an unnamed applied symlink such as `scripts/run → tests/fixtures/payload.txt` through a wildcard scope without a concrete threat row, although invoking the link can execute its target.
- **P2 · High confidence — `scripts/orchestrator/task-consistency-check.py:251`:** The missing-literal shortcut returns before examining directory symlinks, so `scripts/link/new.py`, with `link` pointing elsewhere inside the repository, bypasses the claimed rejection of internal directory aliases.

Both reproduced with the checked-in functions and in-memory filesystem models, without writes. The first returned no findings for a `.txt` target; changing its target to an applied `.py` file correctly produced C12. The second returned no findings for a missing file beneath an internal directory alias. These gaps undermine the threat table’s path-identity/classification controls and its **closed** “internal directory aliases” row. Classification should consider both the enumerated applied path and its confined target; prefix validation must precede the missing-file shortcut.

The remaining controls revealed no additional findings: C14 uses digest authorization and fixed operations without shell execution; YAML uses safe loading; canonical reads bind repository, host and validated commit; credentials travel through child environments. Unicode/collision and C16 controls were inspected. Parent execution, shared caches and same-UID interference remain disclosed residual risks.

Source/test hashes and the task-copy hash match their evidence records. No files were changed.

Not rerun: full suites, native filesystem fixtures or live CI; GitHub connectivity failed. The two demonstrated path-validation bypasses remain unresolved.
Verdict: incorrect-rwxr-xr-x@ 1 a0004262  staff  129658128 Oct 20 14:06 ~/.local/bin/mise
lrwxr-xr-x@ 1 a0004262  staff         10 Oct 10 06:24 ~/.local/share/mise/installs/python/3.15.0/bin/python3 -> python3.15
2c8c05a5d60867ccb9351b3359d64544f66785866e779a0199721158bdc0b4f2  .orchestration/tasks/dotfiles-T133-regime-ci-token-a01.md
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

    def test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier(self):
        # Bot P1 4308651010 and 4308651011 (a02 items 5, 6): the head rewrites the verifier and the checker into programs
        # that pass and leave markers, and forges a dispatched text with a matching result token; the base's policy,
        # verifier and checker still decide, the checkout stays at the base, and no head program runs.

**Analyzing environment and security risks**
**Finalizing review summary and verdict**
codex
No findings in the reviewed text (`SHA256: 2c8c05a5d60867ccb9351b3359d64544f66785866e779a0199721158bdc0b4f2`).

The threat table covers every allowed-file entry and required non-path control. The named tests now claim only token forwarding, output/argv secrecy, and workflow configuration. Executable selection and Git execution-tree binding are explicitly deferred, and the referenced follow-up now specifies both fixes. Same-UID interference, symlink replacement, shared caches, and sandbox exceptions remain disclosed limitations; this text does not establish host isolation. That distinction is consistent with the documented [uv environment discovery](https://docs.astral.sh/uv/reference/cli/#uv-run--no-project) and [sandbox exclusions](https://code.claude.com/docs/en/sandboxing).

📝 まとめ: Reviewed every threat row and related acceptance/review records without edits; implementation tests and live Linux sandbox behavior were not exercised, and the declared execution-binding risks remain.
Verdict: correct
hook: Stop
hook: Stop Completed
tokens used
83,885
No findings in the reviewed text (`SHA256: 2c8c05a5d60867ccb9351b3359d64544f66785866e779a0199721158bdc0b4f2`).

The threat table covers every allowed-file entry and required non-path control. The named tests now claim only token forwarding, output/argv secrecy, and workflow configuration. Executable selection and Git execution-tree binding are explicitly deferred, and the referenced follow-up now specifies both fixes. Same-UID interference, symlink replacement, shared caches, and sandbox exceptions remain disclosed limitations; this text does not establish host isolation. That distinction is consistent with the documented [uv environment discovery](https://docs.astral.sh/uv/reference/cli/#uv-run--no-project) and [sandbox exclusions](https://code.claude.com/docs/en/sandboxing).

📝 まとめ: Reviewed every threat row and related acceptance/review records without edits; implementation tests and live Linux sandbox behavior were not exercised, and the declared execution-binding risks remain.
Verdict: correct
