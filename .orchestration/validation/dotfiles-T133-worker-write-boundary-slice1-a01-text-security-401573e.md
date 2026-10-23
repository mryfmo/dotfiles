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
session id: 01a16113-38d1-7490-9eed-b06e5cdf8c1a
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
読み取り専用でタスク本文と参照先を確認し、判断した内容が実際の実行対象に結び付く設計かを検証します。agmsg-orchestration と Ponytail のレビュー手順を確認します。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md' in ~/Workspace/dotfiles
 succeeded in 148ms:
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

 succeeded in 180ms:
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

 succeeded in 256ms:
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a01.md
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a02.md
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a03.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/plans/024-replan-20261021-v2.md
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-a03.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a02.md
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
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-a02.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md
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
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-2b58663.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-local-review-2b58663.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c761dc8.md
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
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-local-review-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-review-receipt.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-worker-write-boundary-slice1-a01
     4	kind: code
     5	security: true
     6	previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9
     7	worker: a010
     8	worker_kind: codex
     9	worker_profile: security
    10	max_turns: 40
    11	allowed_files:
    12	  - home/dot_agents/agent-config.yaml
    13	  - scripts/generate-agent-configs.py
    14	  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    15	  - home/dot_claude/modify_private_settings.json
    16	  - tests/unit/test_generate_agent_configs.py
    17	  - tests/unit/test_claude_settings_merge.py
    18	  - .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**
    19	after: [dotfiles-T133-trusted-entrypoint-pins-a01, dotfiles-T133-worker-sandbox-exclusions-a02]
    20	reset_of: [dotfiles-T133-worker-write-boundary-a03]
    21	retained_predecessor_directories: [.orchestration/dotfiles-T133-worker-write-boundary-a03/]
    22	threat_table:
    23	  - {control: home/dot_agents/agent-config.yaml, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_closed_startup_contract_is_exhaustive checks declarations; dotfiles-T133-worker-write-boundary-slice2-a01 owns their startup enforcement."}
    24	  - {control: scripts/generate-agent-configs.py, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks deterministic policy; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns descendant execution binding."}
    25	  - {control: home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks routing; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns guard/interpreter/payload binding."}
    26	  - {control: tracked-hook activation (.claude/settings.json), disposition: "out-of-scope: dotfiles-T133-worker-write-boundary-slice5-a01"}
    27	  - {control: home/dot_claude/modify_private_settings.json, disposition: "residual: tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_canonical_hook_migration checks exact replacement; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns attachment/delivery descendants."}
    28	  - {control: tests/unit/test_generate_agent_configs.py, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_existing_orchestrator_outputs_are_unchanged pins the post-prerequisite baseline; final-head review checks fixture sensitivity, not live enforcement."}
    29	  - {control: tests/unit/test_claude_settings_merge.py, disposition: "residual: tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_exact_managed_hook_classification distinguishes owned/custom forms; independent final-head review checks assertions."}
    30	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; records bind actual producers, commands and full heads; orchestrator audits claims against diff and CI."}
    31	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-a03/task.md, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; retain predecessor copy, failing draft/probes and counters unchanged, without deletion or writes."}
    32	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/task.md, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; TASK and RESULT externally bind the complete dispatched slice1 bytes by SHA256."}
    33	  - {control: task metadata, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator checks reset lineage, seven paths, dependencies, budgets, counters and anchored bytes before dispatch/acceptance."}
    34	  - {control: metadata separators, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; complete-file hashing includes both format-2 delimiters and body; records confer no execution authority."}
    35	  - {control: evidence records, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; separate inherited/failing observations from new final-head results and preserve actual producer/seat provenance."}
    36	  - {control: in-process effects, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; generation and fake-process fixtures use repository/temporary files; deployment, authentication and administrative effects are forbidden."}
    37	  - {control: workflow and interpreter or environment inputs, disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed operations and declared role inputs mitigate injection but do not bind the complete reached tool chain."}
    38	  - {control: new or renamed scripts, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; only the named guard is introduced; artifact globs permit records, not executable glue, wrappers, resolvers or sidecars."}
    39	  - {control: "<absolute-home>/.agents/permgate-policy.yaml", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks static protection; dotfiles-T133-trusted-entrypoint-binding-a01 owns PermissionRequest isolation."}
    40	  - {control: "<absolute-home>/.local/lib/python*/site-packages", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks directory/descendant denies; dotfiles-T133-trusted-entrypoint-binding-a01 owns planted-startup execution tests."}
    41	  - {control: "<absolute-home>/Library/Python/*/lib/python/site-packages", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks macOS directory/descendant denies; dotfiles-T133-trusted-entrypoint-binding-a01 owns startup isolation."}
    42	  - {control: "<absolute-home>/.claude/hooks/orchestrator-only.sh", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks protection; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns installed-guard binding."}
    43	  - {control: formatter and project-map configuration selection, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks worker/outside-input suppression; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns formatter/map execution and availability."}
    44	  - {control: hook failure policy, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks supported synthetic onFailure block; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 retains reached-execution risk; async/timeouts are not enforcement."}
    45	  - {control: agmsg store driver and plugin selection, disposition: "residual: owner dotfiles-T133-agmsg-hardening-a01; static plugin/trusted-plugin denies reduce exposure; writable-store driver traversal and plugin sourcing remain unclosed."}
    46	  - {control: "5.14 item 0", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; fixed routing/static protection reduce accidental and injected damage; same-UID processes and shared credentials defeat seat-isolation claims."}
    47	  - {control: "5.14 item 1", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; this slice tests declared write policy only; startup enforcement, reloads, races and live enforcement are not closed."}
    48	  - {control: "5.14 item 2", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed guarded operations mitigate injection; PermissionRequest remains with dotfiles-T133-trusted-entrypoint-binding-a01."}
    49	  - {control: "5.14 item 3", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks canonical launch/tool paths; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns descendant identity binding."}
    50	  - {control: "5.14 item 4", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed dispatch limits candidate-selected execution without proving snapshots, last-use hashes or complete executable identity."}
    51	  - {control: "5.14 item 5", disposition: "out-of-scope: dotfiles-T133-audit-pool-a02"}
    52	  - {control: "5.14 item 6", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; report shared capabilities, races, reloads, hook limitations and pending deployment without relabelling them closed."}
    53	  - {control: "5.14 item 7", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations covers this slice; dotfiles-T133-worker-write-boundary-slice2-a01 owns launch regressions; binding remains separately owned."}
    54	  - {control: "5.14 item 8", disposition: "out-of-scope: dotfiles-T133-permission-guard-gate-a05"}
    55	  - {control: "5.14 item 9", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; static shared-cache protection is declared here; private-cache/interpreter delivery and actual startup checks land there."}
    56	  - {control: "5.14 item 10", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice4-a01; Worker Playbook alignment lands there; this worker follows the sandbox boundary now; operator Codex-policy deployment remains separate."}
    57	  - {control: orchestrator effect merge, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator alone integrates through Playbook step 10 with fresh evidence and a pinned final head; shared credentials remain residual."}
    58	  - {control: orchestrator effect update-branch, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator updates the base and refreshes CI, feedback, review, audit/security and cap evidence for the moved head."}
    59	  - {control: orchestrator effect forced worker removal, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; none authorized; preserve dirty work and existing removal refusals."}
    60	---
    61	
    62	# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice1-a01
    63	
    64	## Design
    65	
    66	[memory:decision] Establish the complete declared startup contract, rendered executable guard template and exact migration foundation. Implement no launcher screen and switch no tracked hook reference in this slice.
    67	Worker a010 is a Codex security seat authoring the Claude boundary. Create tools/worker-write-boundary-slice1-a01 fresh from authenticated origin/main; extract only this slice's changes. Preserve tools/worker-write-boundary-a01, PR #431 history, its WIP/draft and unrelated work; orchestrator owns replacement-PR bookkeeping.
    68	Before dispatch, the orchestrator verifies that dotfiles-T133-worker-sandbox-exclusions-a02 (PR #448) and dotfiles-T133-trusted-entrypoint-pins-a01 are merged in that main; `after:` names both (shared files: agent-config.yaml and the two test modules with #448, tests/unit/test_generate_agent_configs.py with pins). Their post-prerequisite main, never authoring-day main or a historical implementation head, binds every baseline-preservation statement and fixture.
    69	That baseline has empty worker excludedCommands on Darwin and Linux, a validator rejecting any non-empty list, and mise declarations uv 0.13.1, python 3.15.0, node 26.12.0. Pin declarations do not establish installed-host deployment; this slice changes none of those pins.
    70	This is the sole reset carrier for a03. Retain a01/a02 artifacts, a03 failing draft/probes and every lineage counter; retained predecessors are read-only, outside allowed writes. Never create a purported dispatched a04 copy.
    71	Read a04's Closed startup schema, Implementation and retained controls, Regression fixtures, Change budget and premises; a02/a03 acceptance, a03 blocked PONG/runtime evidence and both c0f50fa1 reviews; .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md and .agents/worklog/orchestrator-glue/a04-allocation-r1.md.
    72	Preserve original finding IDs/classes, advisory-owner history and counters in a crosswalk; do not reinterpret repeated renderings as independent findings or failing green-new.log as green evidence. The a04 scope is allocated across five slices after separating provisioning from activation; it is not copied wholesale.
    73	Apply .orchestration/plans/024-design-quality.md section 5.14 items 0-10 by reference, including its residual list; do not restate or amend the contract. D-024-26/29/30/34/35 and the allocation govern this slice.
    74	Future screening/regeneration/launch requirements below are declarations for dotfiles-T133-worker-write-boundary-slice2-a01, not implementation or runtime-enforcement claims here.
    75	
    76	## Ownership and activation order
    77	
    78	Preserve slice1 design 1's rounds 1-3 and design 2's rounds 1-2, all findings/receipts and lineage counters, including text-security-3844d93's post-prerequisite baseline finding. C-80 has at most two rounds per authorized design; this text silently resets none. Exhausted rounds require the orchestrator's recorded split/re-plan before another review.
    79	Before dispatch, orchestrator (Claude seat, sandboxed Bash) verifies canonical scoped owner records and implementing-task mappings for slices2-5, descendants-followup-a01, binding-a01, agmsg-hardening-a01, audit-pool-a02 and permission-guard-gate-a05; save their full IDs, scope hashes and dependency checks in the external receipt. Missing ownership blocks dispatch.
    80	Slice2 owns launch enforcement and worker/admin output registration; slice3 owns orchestrator output/exclusion/validator activation; slice4 owns update reconciliation, staging, documentation and deployment reconciliation. Slice5 alone owns tracked-hook activation after deployment stage A actually provisions the guard.
    81	Orchestrator corrects stale stub/allocation claims that slice1 supplies guarded tracked settings or provisions the installed guard; those records are outside worker writes. Deployment-stage-A evidence must establish actual guard installation before slice5; a rendered template or green CI is insufficient.
    82	
    83	## Host facts and evidence producers
    84	
    85	Inherited host facts from BRIEF-TEMPLATE-NOTES.md, supplied by orchestrator (Claude seat, sandboxed Bash), are retained verbatim:
    86	mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
    87	Replay producer: worker (Codex security seat, a010). Run env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv and env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which python3; paste actual stdout/status and resolved regular-file identity, never substitute a guessed uv layout or pin file.
    88	Declare the absolute non-shim mise launch interpreter from that evidence, including bootstrap/home lookup/preflight roles. The inherited a04 probe resolved python3.15 under the same 3.15.0 install; selection here does not implement a resolver or complete binding.
    89	Inherited a04 runtime evidence was produced by worker (Codex review-profile authoring seat): system Python added CPATH/LIBRARY_PATH/MANPATH/SDKROOT plus __CF_USER_TEXT_ENCODING; mise Python added only __CF_USER_TEXT_ENCODING to HOME/LANG/PATH/TERM. Retain the original commands, names, statuses and source hashes as history.
    90	Inherited spawn/loader evidence producer: worker (Codex review-profile authoring seat), as recorded in a04. Spawn evidence records export AGMSG_SPAWNED=1 at upstream spawn.sh line 527, SHA256 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731. Historical loader is 2.1.300, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3; no fresh installed-version claim is made.
    91	Every evidence item names actual producer/seat kind, command, status, time, tested full identity and path. New code/tests/renders/lint/numstat/report and CI collection: worker (Codex security seat, a010); CI execution: GitHub Actions runners; transport, dispatch/acceptance checks and CI verification: orchestrator (Claude seat, sandboxed Bash). Preserve each independent context's actual kind.
    92	C-80 and final security evidence producers: independent worker (Codex security seat); pre-push/local review and task-audit producers: independent worker (Codex review seat). Record each actual context identity, command/status and tested full head; a requested review is not evidence of a completed review.
    93	A Codex seat must not probe the Herdr socket: PermissionDenied was measured 2026-10-20T13:39Z by worker (Codex seat, a013). Use fake CLIs/processes; no socket probe, live seat or private credential inspection.
    94	
    95	## Exhaustive manifest contract
    96	
    97	Declare one renderer-owned schema and static inventory in agent-config.yaml; candidate settings, Git objects and upstream schemas never extend acceptance. Declare source-specific optional/required fields, types, exact values and role subsets, not just key names.
    98	Objects reject unknown nested keys, duplicate JSON keys, wrong types, Boolean/integer substitutions, unsupported forms, missing references and unreadable inputs. S11's discarded partition is the sole semantic-screening exception; syntax/duplicate-key/readability checks still apply.
    99	Settings keys only: permissions, sandbox, hooks, env, enableAllProjectMcpServers, enabledMcpjsonServers, disabledMcpjsonServers, enabledPlugins, syncClaudeAiPlugins, syncClaudeAiSkills, extraKnownMarketplaces, disableSkillShellExecution.
   100	permissions: only defaultMode=auto where applicable, additionalDirectories=[], and exact source-specific renderer-declared deny/native-denial fragments; no caller allow/ask or alternate mode.
   101	sandbox: only enabled, failIfUnavailable, autoAllowBashIfSandboxed, allowUnsandboxedCommands, excludedCommands, filesystem, network, enableWeakerNestedSandbox, enableWeakerNetworkIsolation, allowAppleEvents. Every present Boolean/list equals its source's declared canonical fragment.
   102	filesystem: only allowWrite and disabled. network: only allowedDomains, allowUnixSockets, allowAllUnixSockets, allowLocalBinding. Pin all leaf/list values from worker/admin policy before merging; no broadened lower-scope arrays.
   103	hooks: exact source/event/matcher/operation forms; groups only matcher/hooks; handlers only type/command/timeout/async/statusMessage/onFailure with exact declared values. Validate type first: only command; HTTP/MCP-tool/prompt/agent/unknown/missing/null/non-string types have no worker form.
   104	MCP approvals: enableAllProjectMcpServers=false, enabledMcpjsonServers=[], disabledMcpjsonServers=[]; never exempt definitions. enabledPlugins maps only declared/inventoried identities to false, both sync fields=false, extraKnownMarketplaces={}, disableSkillShellExecution=true.
   105	Settings env has exactly GH_TELEMETRY="false", DO_NOT_TRACK="1", CHECKPOINT_DISABLE="1", AWS_EC2_METADATA_DISABLED="true"; no other AWS exception, credential/provider string or arbitrary value.
   106	Absent/empty objects pass only where their source permits; canonical partial administrative objects may omit declared fields, never add keys/values. Helpers, status-line commands, wrappers, alternate executables and authentication refresh/export keys have no worker form. Orchestrator PermissionRequest is not a worker exception.
   107	
   108	## S01-S23, roots and component values
   109	
   110	Use user=<validated-home>/.claude-worker, anchor=<validated-home>/Workspace/dotfiles, managed-root=/Library/Application Support/ClaudeCode on Darwin or /etc/claude-code on Linux.
   111	S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 anchor/.claude/settings.local.json; S05 managed-root/managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery.
   112	S08 worktree/.mcp.json; S09 anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json; S12 every skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json.
   113	S16 every default hooks/hooks.json and referenced hook file; S17 each marketplace-root/.claude-plugin/marketplace.json; S18 every default/referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every default/referenced legacy command Markdown file; S22 every subagent Markdown file; S23 every default/referenced plugin LSP file.
   114	Declare independent reads of every matching file, including ignored/untracked, disabled and shadowed inputs; executable environment-file contents join this read set. Unenumerable managed delivery or caller-selected sources require named refusal, without discovery helpers.
   115	Bind anchor to validated passwd home and actual main checkout; worker roots are registered linked worktrees beneath anchor/.claude/worktrees with the same Git common directory. Declare symlink/case-alias handling and containment; foreign roots refuse before side effects for both kinds/routes.
   116	Configuration roots: dedicated user directory, anchor/worktree .claude, applicable nested/additional-directory .claude, platform managed root and registry-contained plugin roots. No account-synced, inline, seed, alternate cache or caller-selected root.
   117	Skills roots exactly Enterprise managed-root/.claude/skills, Personal user/skills, Project project/.claude/skills, Nested subdir/.claude/skills, applicable Additional directory add-dir/.claude/skills, Plugin plugin/skills. Read Markdown and bundled descriptors; managed commands/agents start at actual managed-root.
   118	S08-S10/S18-S19 objects permit only absent/empty mcpServers/managedMcpServers. S14 and S23 permit only {}; S16 only absent/empty hooks; approval/disable state cannot authorize servers or handlers.
   119	S12/S15 fields: name/version/description/author/homepage/repository/license/keywords and hooks/mcpServers/lspServers/commands/agents/skills. Descriptive fields are strings, keywords is a string list; author only string name/email/url. Each explicit component is one scalar contained regular-file reference; no arrays/objects/URLs/inline content/directories; defaults expand independently.
   120	S13 only version=2 and plugins: IDs map to record lists with scope/installPath/version/installedAt/lastUpdated/gitCommitSha/projectPath; scope=user|project|local, descriptive members strings, commit 40 hex, paths contained/project-bound; read every descriptor and disable every ID.
   121	S17 only name/owner/metadata/plugins: string name, owner string name/email, metadata string description/version, plugins absent or []. S20-S22 restricted frontmatter only name/description/argument-hint, Boolean disable-model-invocation/user-invocable, declared allowed-tools/model; no unknown/nested executable forms or dynamic shell expansion, including fenced forms.
   122	S11 must be an object; retained mcpServers only {}; oauthAccount only optional string members accountUuid/emailAddress/organizationUuid/displayName/fullName/organizationRole/workspaceRole; userID only ^[0-9a-f]{64}$. Unknown identity members/wrong types/nonempty or malformed retained MCP refuse unchanged.
   123	Declare discard of every other S11 top-level field and the entire projects value without recursive semantic screening: counters, history, allowedTools, caches and prior onboarding are never forwarded. After complete preflight, atomically regenerate exactly mcpServers={}, projects={}, hasCompletedOnboarding=true plus screened identity; never merge old state. Trust uses existing spawn-readiness acceptance.
   124	
   125	## Role environments and same-start runtime files
   126	
   127	Declare child-specific name/value maps for launcher/bootstrap, preparation, spawn-launched worker and guard/delivery/attachment; do not grant every role the union or inherit arbitrary caller names. Existing profile/control-plane selectors are consumed through manifest interfaces, not forwarded settings.
   128	Base HOME/PATH/LANG/TERM authorities follow a04: validated home, prescribed child PATH, C.UTF-8, declared terminal (hooks dumb); TMPDIR is canonical parent-supplied temp. CLAUDE_CONFIG_DIR=user, CLAUDE_PROJECT_DIR=canonical launch identity; CLAUDE_ENV_FILE is parent-bound runtime file.
   129	UV_CACHE_DIR=worktree/.uv-cache; UV_PYTHON_INSTALL_DIR=its python child. Regime names: AGMSG_RESOLVE_PROJECT="0"; AGMSG_STORAGE_PATH=validated selection (unset default supported); AGMSG_CC_MONITOR_KEEP_ALIVE="1" where required; AGMSG_AGENT_PID=numeric runtime identity.
   130	AGMSG_SPAWNED is regime-declared exactly "1", required for spawn-launched roles only. Darwin's optional platform-injected __CF_USER_TEXT_ENCODING full-matches 0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+; Linux presence refuses. CPATH/LIBRARY_PATH/MANPATH/SDKROOT remain undeclared, not silently removed.
   131	HERDR_ENV/HERDR_PANE_ID/HERDR_WORKSPACE_ID/HERDR_AGENTS_LAYOUT/HERDR_SOCKET_PATH carry validated attachment/control-plane identities, managed layout and configured canonical socket; CLAUDE_CODE_SESSION_ID/CLAUDE_PID carry required runtime identities. CLICOLOR_FORCE/FORCE_COLOR only launcher-written "1" where used; CHEZMOI_SOURCE_DIR/CHEZMOI_HOME_DIR preparation-only.
   132	Declare exact per-role presence, ID syntax and values from a04 and post-prerequisite canonical constructors, plus the four fixed env pairs. Preserve canonical attachment's optional/unset fields; no unrelated role gains them. Worker argv only manifest profile --model/--effort/--advisor, including --advisor fable.
   133	Unknown proposed names/values and caller-added settings/MCP/plugin/agent/add-dir arguments refuse. Explicit negatives include CLAUDE_CODE_USE_BEDROCK, AWS_CONFIG_FILE, AWS_SHARED_CREDENTIALS_FILE, AWS_PROFILE; all undeclared CLAUDE_CODE_USE_*, AWS_*, ANTHROPIC_*, *_API_KEY, *_TOKEN, *_PROFILE and BASH_ENV/ENV/NODE_OPTIONS/NODE_PATH/PYTHON*/LD_*/DYLD_* remain prohibited. Add no AWS parser.
   134	Declare CLAUDE_ENV_FILE acceptance only when absent, empty or byte-identical to canonical launcher contents for this start; inspect without executing/sourcing, reject unreadable/nonregular/foreign contents unchanged. After all checks, launcher writes existing runtime file, records variable+canonical-path+start-bound SHA256 and verifies before forwarding; prior-start/candidate digests never authorize it. No sidecar.
   135	Declare a04's exact zero-based hooks.<event>[<group>].hooks[<handler>] noncanonical hook handler refusal, S11 mcpServers: noncanonical global state, and source/key-only diagnostics; never print payloads/secret values. Runtime-name, executable-file and S11 A-then-B/shared-directory launch regressions belong to slice2; do not add a launcher/preflight implementation here.
   136	
   137	## Guard, renders and complete migration foundation
   138	
   139	Add pure worker/admin render functions and test them now. Register/render only the executable .tmpl guard now; worker/admin output registration and files land with their consumer in slice2. Leave .claude/settings.json byte-identical; slice5 owns its tracked command switch after stage A.
   140	Preserve byte-for-byte the orchestrator template/generated output, sandbox/exclusions, PermissionRequest command/recognition and registered outputs relative to post-prerequisite main, except registering the new guard. Both platforms' worker exclusions stay empty and the validator rejects non-empty lists; preserve no old Linux or gh exclusion. Slice3 owns subsequent orchestrator activation/alignment; slice5 owns tracked-hook activation. No Codex/shared writable-root policy changes.
   141	Worker render: auto, sandbox startup failure, no unsandboxed request, empty exclusions/no Herdr socket, four existing agmsg stores as narrow grants, explicit MCP/sync disables and false plugin IDs including discovered @skills-dir identities.
   142	Admin render: enabled sandbox/failIfUnavailable, filesystem enforcement; disabled unsandboxed/weaker-isolation/Apple Events/all-socket/local-binding switches; exact single Herdr socket and ordered exclusions agmsg-dispatch *, herdr-agents *, <home>/.agents/skills/agmsg/scripts/actas-claim.sh *. These remain shared capabilities, not worker escape authority.
   143	Static trusted_paths derive from consumed inputs, never Git tree/index: anchored source/control paths, tracked/main-local settings, .orchestration, .agents/worklog/** and .agents/worklog/uv-cache/**, worker .claude directory+descendants and .mcp.json; ordinary worktree/cache writes remain available.
   144	Protect installed manifest/profiles/permgate policy, skill scripts/SKILL files, agmsg plugin code and db/trusted-plugins, .claude/.claude-worker and guard, wrappers/application code, config/state/tool installations/shared uv caches; both user-site directory and descendant patterns protect .pth/usercustomize.py/sitecustomize.py. No blanket .agents/** or .local/** deny: db/teams/run/ext-tools remain writable except trusted-plugins.
   145	Guard accepts only manifest-fixed operations/argv. Canonical anchor identity alone permits project payloads; worker/sibling/unrelated/missing identities suppress them. Only fixed worker delivery runs for canonical workers; never trust writable run/proj.<pid>.project over explicit identity. Formatter/map additionally suppress worker/outside-anchor tool paths.
   146	Preserve stdin bytes, argv boundaries, child status, fixed payload paths and event/matcher/async/timeout markers; test supported onFailure=block through synthetic canonical hooks. Preserve absolute tool calls and attachment re-exports; caller cwd/tool input never selects a payload.
   147	Finish exact legacy/canonical classification, attachment construction and SessionStart/PostToolUse/PreToolUse migration now using synthetic canonical guarded baselines. Preserve production merge output for post-prerequisite main until slice3 activation; synthetic canonical-baseline selection must not depend on installed tools or add a rollout switch.
   148	Recognize only complete owned forms with canonical project/guard/prefix/operation/argument binding; reject near-matches as custom, never basename/substring ownership. Retain supported old-home legacy forms and stale ccgate/permgate handling without broadening PermissionRequest.
   149	Preserve custom/mixed hooks and ordering, quoted/escaped literal tilde distinctions, wrapper/chained/foreign commands; replace stale owned entries once, including enforce-uv PreToolUse; construct exactly one guarded attachment with declared identities and retain byte-idempotence. Slice3 must consume this merge implementation unchanged.
   150	Complete guard/delivery/formatter/map binding, interpreters/configuration/availability and replacement races: dotfiles-T133-trusted-entrypoint-descendants-followup-a01. Legacy PermissionRequest structural validation/isolation: dotfiles-T133-trusted-entrypoint-binding-a01. Store driver/plugin sourcing: dotfiles-T133-agmsg-hardening-a01.
   151	
   152	## Check
   153	
   154	Prerequisite check: orchestrator (Claude seat, sandboxed Bash) records authenticated merged heads for dotfiles-T133-worker-sandbox-exclusions-a02 (PR #448) and dotfiles-T133-trusted-entrypoint-pins-a01, verifies empty worker exclusions on both platforms, non-empty-list validator refusal and exact uv 0.13.1/python 3.15.0/node 26.12.0 declarations; compare all preservation fixtures to that post-prerequisite main.
   155	Write regressions before implementation using existing temporary-HOME/render/merge/fake-process builders; put new coverage only in the two allowed modules. No new dependency, helper script or runtime validator; synthetic payloads record markers and never run real services.
   156	GenerateAgentConfigsTest::test_closed_startup_contract_is_exhaustive pins all keys/nested values, S01-S23, roots/components, role maps, interpreter and identity/discard contracts against an independent expected inventory, not the candidate manifest alone.
   157	GenerateAgentConfigsTest::test_worker_admin_policy_renders covers Darwin/Linux, exact static inventory, policy/guard/user-site directory+descendant denies, writable stores/trusted-plugin exception, ordinary worktree/cache allowance, spaces/symlink/case aliases and explicit plugin disables.
   158	GenerateAgentConfigsTest::test_existing_orchestrator_outputs_are_unchanged pins post-prerequisite production output, .claude/settings.json bytes/references and expected_outputs membership; pure worker/admin renders succeed without installed guard/tools/admin policy and without registering their output files.
   159	GenerateAgentConfigsTest::test_guard_routes_fixed_operations invokes the rendered template through synthetic canonical hook commands: anchored positive; worker/sibling/unrelated/missing identities; outside/worker tool inputs; aliases/spaces; known/unknown operations, invalid extra args, fixed argv/stdin/status and absent hostile BASH_ENV markers.
   160	ClaudeSettingsMergeTest::test_exact_managed_hook_classification and test_canonical_hook_migration cover custom/mixed forms, ordering, escaped tilde, complete canonical binding, stale legacy replacement, PreToolUse and repeated byte-idempotence against synthetic canonical baselines.
   161	ClaudeSettingsMergeTest::test_guarded_attachment_construction covers one absolute guarded attachment, declared identity/store re-exports, spaces, absent optional fields and absent BASH_ENV markers using fakes; preserve post-prerequisite production-baseline expectations and synthetic legacy migration coverage.
   162	E1 requires complete modules, not selected tests: uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_validate_agent_assets tests.unit.test_herdr_agents tests.unit.test_agmsg_orchestration_docs -v.
   163	Run make render-check, make validate-agent-assets and changed-file repository lint/format checks, including rendered-guard shellcheck/shfmt and Python checks. Shell comments are English shdoc. No local Bats; required Bats/all required CI come from GitHub Actions before RESULT.
   164	The final diff has at most 650 changed lines outside tests/, .orchestration/, home/.chezmoitemplates/claude-settings-managed.json, home/.chezmoitemplates/claude-worker-settings.json and home/.chezmoitemplates/claude-managed-settings.json, and 650 under tests/.
   165	Measure with git diff --numstat <authenticated-merge-base> <head>.
   166	Changed means additions plus deletions; exclusions grant no write permission. Orchestrator supplies authenticated full merge-base/head evidence at dispatch; local origin/main alone is not authentication. For a records-only round after update-branch use its dispatch branch head, not an older code head.
   167	Preserve complete git diff --numstat 51ba5801 c0f50fa1 output; separate already-merged base rows, retained extraction and new work, reconcile per-control source/test attribution against a04 1591/2528, count shared controls once. Report actual per-file/totals; 650/650 is a ceiling, not a measured result.
   168	This complete task text stays at most 200 lines including Checks, with at most eight allowed_files entries and at most 193 lines before Checks. A measured overrun or missing prerequisite produces blocked PONG for re-tasking; never hide code in artifacts, weaken coverage, raise caps or edit outside the seven entries.
   169	
   170	## Artifacts, review and completion
   171	
   172	Worker (Codex security seat, a010) writes task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md, result.txt, budget/crosswalk and -worker- Crit-data JSON/receipt beneath this task's directory in its own worktree; RESULT states that location. No canonical task/acceptance/decision/design/other-task edits.
   173	Keep uncommitted seat plan/todo worklogs within that allowed directory using Codex seat worklog fields/sections; update them, allow one active todo per owner and commit no plan/todo/learn worklogs. Durable facts use CompactionDB markers; orchestrator owns main-checkout consolidation/copying/masking.
   174	Paste complete executed outputs/statuses and claimed identifiers, red/green tested identities and selectors, historical evidence sources, generated/installed paths, declared source/role inventories, budget attribution, CI URLs/full heads and feedback dispositions. Missing dependencies/fixtures are not red evidence.
   175	Every command obeys Worker Playbook step 4 and design 5.14 item 10 by reference. A boundary denial yields AGMSG-PONG v1 status=blocked with exact command/status/output/boundary; do not retry through escalation, another tool or socket access.
   176	Allow at most one independent pre-push review and two correction rounds, carrying a01/a02/a03 counters separately. Surviving P0/P1 stops integration; no private third round. Post no @codex review; observe automatic final-head review within the existing bounded window and record bot:none if absent.
   177	Use agent-side Crit data/receipt only, read the saved JSON, resolve each addressed record or record justified review-scope approval, then pass make require-crit-review with the required receipt. No browser/human review request or publish; account for any hook-started review server.
   178	Orchestrator (Claude seat, sandboxed Bash) verifies owner prerequisites, fills Checks before C-80, runs consistency C1-C10/C7b and verifies each C11 obligation, then selector existence/coverage at acceptance. C-80 has at most two rounds per authorized design; a second incorrect verdict stops for split/re-task. Verify remaining budget against every preserved round before requesting review; no private third round.
   179	Anchor the complete reviewed task bytes after Checks is filled; keep the SHA256 in external TASK/review receipt/RESULT. Dispatch/copy those exact bytes without repasting or post-review mutation; any edit requires a new anchor/review within the limit.
   180	Required CI and fresh final-head local review, task audit and independent security evidence precede integration. Orchestrator collects/dispositions feedback and follows Playbook step 10 in order; any moved head refreshes required evidence. Worker grants no acceptance, resolves no GitHub thread and merges nothing.
   181	RESULT names full head/base/branch/new PR, task-copy digest, changed files, all artifact/evidence producers/paths, E1/lint/CI/review outcomes, caps/attribution, open findings/counters and cost or n/a. Preserved PR #431 is history, not this slice's delivery PR.
   182	Report visible impact: this slice declares/tests worker/admin policy, startup contracts and guard/migration foundations; tracked hooks, orchestrator output/exclusions and PermissionRequest remain unchanged relative to post-prerequisite main. Same-UID/shared credentials, shared admin exceptions/socket, sourcing, reloads, races and descendant binding remain residual.
   183	
   184	## Out of scope
   185	
   186	No session loses its stop gate from this slice because the tracked commands do not change. dotfiles-T133-worker-write-boundary-slice5-a01 owns switching .claude/settings.json only after stage A provisions <home>/.claude/hooks/orchestrator-only.sh; this slice neither installs that file nor activates its tracked references.
   187	No deployment, make update/application, login/keyring change, system installation, restart, permission-policy deployment, live socket/worker probe or live-dependent release. Later slices own screening/output registration, orchestrator activation, update/staging/docs/ignore and deployment reconciliation.
   188	
   189	Amendment 1 (`previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9`): the Codex sandbox denies the Herdr socket, so `agmsg-dispatch` cannot carry this seat's messages (your PONG attempt for PING 2984 exited 1: `PermissionDenied`, `pane not found or unavailable: wJ:p1`). The named route for every PONG and the RESULT of this task is the pane-less path of Orchestrator Playbook step 6, run from sandboxed Bash: write the single line to a file under `.orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/` and send it with `~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-standard-dot-a010 claude-deep-dot --body-file <that file>` (a013 delivered its PONGs this way on 2026-10-21T05:59Z). This route is the named route, not 'another tool' under the boundary-denial sentence above, and the orchestrator reads the bus at each milestone. First reply `AGMSG-PONG v1 task_id=dotfiles-T133-worker-write-boundary-slice1-a01 status=alive` by that route, then start round 1 as written; the unsent `blocked-pong.txt` and `liveness-2998.txt` stay as evidence.
   190	
   191	## Checks
   192	
   193	```text
   194	prerequisites merged in canonical main 7da0cdfab9de9fbea673b82379acd4e317115065 (gh api --hostname github.com repos/mryfmo/dotfiles/branches/main --jq .commit.sha, 2026-10-22T00:46Z, exit 0; git merge-base --is-ancestor 4eafd890454e495fdb1d429734c5835e46c87652 7da0cdfa exit 0): dotfiles-T133-worker-sandbox-exclusions-a02 = PR #448 merge e042663b2d6efd9205f7d388bf881c01d3880642; dotfiles-T133-trusted-entrypoint-pins-a01 = PR #449 merge 4eafd890454e495fdb1d429734c5835e46c87652; the dispatch branch starts fresh from that main, so merge-base = that SHA
   195	post-prerequisite baseline at that main: agent-config.yaml worker 284:    excludedCommands: [] 285:    linux_excluded_commands: []; validate-agent-assets.py line 344 fails any non-empty worker excludedCommands; home/dot_mise/config.toml node = "26.12.0" python = "3.15.0" uv = "0.13.1"
   196	observed 2026-10-21T09:17Z and re-observed host-bound 2026-10-22T00:46Z (amendment 1) by the orchestrator (Claude seat, sandboxed Bash); C1-C10/C7b via pre-send.sh on these bytes exit 0 (see the anchor review record); every value is pasted command output
   197	```

exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md | sed -n '1,115p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-worker-write-boundary-slice1-a01
     4	kind: code
     5	security: true
     6	previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9
     7	worker: a010
     8	worker_kind: codex
     9	worker_profile: security
    10	max_turns: 40
    11	allowed_files:
    12	  - home/dot_agents/agent-config.yaml
    13	  - scripts/generate-agent-configs.py
    14	  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    15	  - home/dot_claude/modify_private_settings.json
    16	  - tests/unit/test_generate_agent_configs.py
    17	  - tests/unit/test_claude_settings_merge.py
    18	  - .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**
    19	after: [dotfiles-T133-trusted-entrypoint-pins-a01, dotfiles-T133-worker-sandbox-exclusions-a02]
    20	reset_of: [dotfiles-T133-worker-write-boundary-a03]
    21	retained_predecessor_directories: [.orchestration/dotfiles-T133-worker-write-boundary-a03/]
    22	threat_table:
    23	  - {control: home/dot_agents/agent-config.yaml, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_closed_startup_contract_is_exhaustive checks declarations; dotfiles-T133-worker-write-boundary-slice2-a01 owns their startup enforcement."}
    24	  - {control: scripts/generate-agent-configs.py, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks deterministic policy; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns descendant execution binding."}
    25	  - {control: home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks routing; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns guard/interpreter/payload binding."}
    26	  - {control: tracked-hook activation (.claude/settings.json), disposition: "out-of-scope: dotfiles-T133-worker-write-boundary-slice5-a01"}
    27	  - {control: home/dot_claude/modify_private_settings.json, disposition: "residual: tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_canonical_hook_migration checks exact replacement; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns attachment/delivery descendants."}
    28	  - {control: tests/unit/test_generate_agent_configs.py, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_existing_orchestrator_outputs_are_unchanged pins the post-prerequisite baseline; final-head review checks fixture sensitivity, not live enforcement."}
    29	  - {control: tests/unit/test_claude_settings_merge.py, disposition: "residual: tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_exact_managed_hook_classification distinguishes owned/custom forms; independent final-head review checks assertions."}
    30	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; records bind actual producers, commands and full heads; orchestrator audits claims against diff and CI."}
    31	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-a03/task.md, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; retain predecessor copy, failing draft/probes and counters unchanged, without deletion or writes."}
    32	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/task.md, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; TASK and RESULT externally bind the complete dispatched slice1 bytes by SHA256."}
    33	  - {control: task metadata, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator checks reset lineage, seven paths, dependencies, budgets, counters and anchored bytes before dispatch/acceptance."}
    34	  - {control: metadata separators, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; complete-file hashing includes both format-2 delimiters and body; records confer no execution authority."}
    35	  - {control: evidence records, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; separate inherited/failing observations from new final-head results and preserve actual producer/seat provenance."}
    36	  - {control: in-process effects, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; generation and fake-process fixtures use repository/temporary files; deployment, authentication and administrative effects are forbidden."}
    37	  - {control: workflow and interpreter or environment inputs, disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed operations and declared role inputs mitigate injection but do not bind the complete reached tool chain."}
    38	  - {control: new or renamed scripts, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; only the named guard is introduced; artifact globs permit records, not executable glue, wrappers, resolvers or sidecars."}
    39	  - {control: "<absolute-home>/.agents/permgate-policy.yaml", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks static protection; dotfiles-T133-trusted-entrypoint-binding-a01 owns PermissionRequest isolation."}
    40	  - {control: "<absolute-home>/.local/lib/python*/site-packages", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks directory/descendant denies; dotfiles-T133-trusted-entrypoint-binding-a01 owns planted-startup execution tests."}
    41	  - {control: "<absolute-home>/Library/Python/*/lib/python/site-packages", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks macOS directory/descendant denies; dotfiles-T133-trusted-entrypoint-binding-a01 owns startup isolation."}
    42	  - {control: "<absolute-home>/.claude/hooks/orchestrator-only.sh", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks protection; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns installed-guard binding."}
    43	  - {control: formatter and project-map configuration selection, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks worker/outside-input suppression; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns formatter/map execution and availability."}
    44	  - {control: hook failure policy, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks supported synthetic onFailure block; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 retains reached-execution risk; async/timeouts are not enforcement."}
    45	  - {control: agmsg store driver and plugin selection, disposition: "residual: owner dotfiles-T133-agmsg-hardening-a01; static plugin/trusted-plugin denies reduce exposure; writable-store driver traversal and plugin sourcing remain unclosed."}
    46	  - {control: "5.14 item 0", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; fixed routing/static protection reduce accidental and injected damage; same-UID processes and shared credentials defeat seat-isolation claims."}
    47	  - {control: "5.14 item 1", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; this slice tests declared write policy only; startup enforcement, reloads, races and live enforcement are not closed."}
    48	  - {control: "5.14 item 2", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed guarded operations mitigate injection; PermissionRequest remains with dotfiles-T133-trusted-entrypoint-binding-a01."}
    49	  - {control: "5.14 item 3", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks canonical launch/tool paths; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns descendant identity binding."}
    50	  - {control: "5.14 item 4", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed dispatch limits candidate-selected execution without proving snapshots, last-use hashes or complete executable identity."}
    51	  - {control: "5.14 item 5", disposition: "out-of-scope: dotfiles-T133-audit-pool-a02"}
    52	  - {control: "5.14 item 6", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; report shared capabilities, races, reloads, hook limitations and pending deployment without relabelling them closed."}
    53	  - {control: "5.14 item 7", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations covers this slice; dotfiles-T133-worker-write-boundary-slice2-a01 owns launch regressions; binding remains separately owned."}
    54	  - {control: "5.14 item 8", disposition: "out-of-scope: dotfiles-T133-permission-guard-gate-a05"}
    55	  - {control: "5.14 item 9", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; static shared-cache protection is declared here; private-cache/interpreter delivery and actual startup checks land there."}
    56	  - {control: "5.14 item 10", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice4-a01; Worker Playbook alignment lands there; this worker follows the sandbox boundary now; operator Codex-policy deployment remains separate."}
    57	  - {control: orchestrator effect merge, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator alone integrates through Playbook step 10 with fresh evidence and a pinned final head; shared credentials remain residual."}
    58	  - {control: orchestrator effect update-branch, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator updates the base and refreshes CI, feedback, review, audit/security and cap evidence for the moved head."}
    59	  - {control: orchestrator effect forced worker removal, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; none authorized; preserve dirty work and existing removal refusals."}
    60	---
    61	
    62	# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice1-a01
    63	
    64	## Design
    65	
    66	[memory:decision] Establish the complete declared startup contract, rendered executable guard template and exact migration foundation. Implement no launcher screen and switch no tracked hook reference in this slice.
    67	Worker a010 is a Codex security seat authoring the Claude boundary. Create tools/worker-write-boundary-slice1-a01 fresh from authenticated origin/main; extract only this slice's changes. Preserve tools/worker-write-boundary-a01, PR #431 history, its WIP/draft and unrelated work; orchestrator owns replacement-PR bookkeeping.
    68	Before dispatch, the orchestrator verifies that dotfiles-T133-worker-sandbox-exclusions-a02 (PR #448) and dotfiles-T133-trusted-entrypoint-pins-a01 are merged in that main; `after:` names both (shared files: agent-config.yaml and the two test modules with #448, tests/unit/test_generate_agent_configs.py with pins). Their post-prerequisite main, never authoring-day main or a historical implementation head, binds every baseline-preservation statement and fixture.
    69	That baseline has empty worker excludedCommands on Darwin and Linux, a validator rejecting any non-empty list, and mise declarations uv 0.13.1, python 3.15.0, node 26.12.0. Pin declarations do not establish installed-host deployment; this slice changes none of those pins.
    70	This is the sole reset carrier for a03. Retain a01/a02 artifacts, a03 failing draft/probes and every lineage counter; retained predecessors are read-only, outside allowed writes. Never create a purported dispatched a04 copy.
    71	Read a04's Closed startup schema, Implementation and retained controls, Regression fixtures, Change budget and premises; a02/a03 acceptance, a03 blocked PONG/runtime evidence and both c0f50fa1 reviews; .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md and .agents/worklog/orchestrator-glue/a04-allocation-r1.md.
    72	Preserve original finding IDs/classes, advisory-owner history and counters in a crosswalk; do not reinterpret repeated renderings as independent findings or failing green-new.log as green evidence. The a04 scope is allocated across five slices after separating provisioning from activation; it is not copied wholesale.
    73	Apply .orchestration/plans/024-design-quality.md section 5.14 items 0-10 by reference, including its residual list; do not restate or amend the contract. D-024-26/29/30/34/35 and the allocation govern this slice.
    74	Future screening/regeneration/launch requirements below are declarations for dotfiles-T133-worker-write-boundary-slice2-a01, not implementation or runtime-enforcement claims here.
    75	
    76	## Ownership and activation order
    77	
    78	Preserve slice1 design 1's rounds 1-3 and design 2's rounds 1-2, all findings/receipts and lineage counters, including text-security-3844d93's post-prerequisite baseline finding. C-80 has at most two rounds per authorized design; this text silently resets none. Exhausted rounds require the orchestrator's recorded split/re-plan before another review.
    79	Before dispatch, orchestrator (Claude seat, sandboxed Bash) verifies canonical scoped owner records and implementing-task mappings for slices2-5, descendants-followup-a01, binding-a01, agmsg-hardening-a01, audit-pool-a02 and permission-guard-gate-a05; save their full IDs, scope hashes and dependency checks in the external receipt. Missing ownership blocks dispatch.
    80	Slice2 owns launch enforcement and worker/admin output registration; slice3 owns orchestrator output/exclusion/validator activation; slice4 owns update reconciliation, staging, documentation and deployment reconciliation. Slice5 alone owns tracked-hook activation after deployment stage A actually provisions the guard.
    81	Orchestrator corrects stale stub/allocation claims that slice1 supplies guarded tracked settings or provisions the installed guard; those records are outside worker writes. Deployment-stage-A evidence must establish actual guard installation before slice5; a rendered template or green CI is insufficient.
    82	
    83	## Host facts and evidence producers
    84	
    85	Inherited host facts from BRIEF-TEMPLATE-NOTES.md, supplied by orchestrator (Claude seat, sandboxed Bash), are retained verbatim:
    86	mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
    87	Replay producer: worker (Codex security seat, a010). Run env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv and env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which python3; paste actual stdout/status and resolved regular-file identity, never substitute a guessed uv layout or pin file.
    88	Declare the absolute non-shim mise launch interpreter from that evidence, including bootstrap/home lookup/preflight roles. The inherited a04 probe resolved python3.15 under the same 3.15.0 install; selection here does not implement a resolver or complete binding.
    89	Inherited a04 runtime evidence was produced by worker (Codex review-profile authoring seat): system Python added CPATH/LIBRARY_PATH/MANPATH/SDKROOT plus __CF_USER_TEXT_ENCODING; mise Python added only __CF_USER_TEXT_ENCODING to HOME/LANG/PATH/TERM. Retain the original commands, names, statuses and source hashes as history.
    90	Inherited spawn/loader evidence producer: worker (Codex review-profile authoring seat), as recorded in a04. Spawn evidence records export AGMSG_SPAWNED=1 at upstream spawn.sh line 527, SHA256 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731. Historical loader is 2.1.300, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3; no fresh installed-version claim is made.
    91	Every evidence item names actual producer/seat kind, command, status, time, tested full identity and path. New code/tests/renders/lint/numstat/report and CI collection: worker (Codex security seat, a010); CI execution: GitHub Actions runners; transport, dispatch/acceptance checks and CI verification: orchestrator (Claude seat, sandboxed Bash). Preserve each independent context's actual kind.
    92	C-80 and final security evidence producers: independent worker (Codex security seat); pre-push/local review and task-audit producers: independent worker (Codex review seat). Record each actual context identity, command/status and tested full head; a requested review is not evidence of a completed review.
    93	A Codex seat must not probe the Herdr socket: PermissionDenied was measured 2026-10-20T13:39Z by worker (Codex seat, a013). Use fake CLIs/processes; no socket probe, live seat or private credential inspection.
    94	
    95	## Exhaustive manifest contract
    96	
    97	Declare one renderer-owned schema and static inventory in agent-config.yaml; candidate settings, Git objects and upstream schemas never extend acceptance. Declare source-specific optional/required fields, types, exact values and role subsets, not just key names.
    98	Objects reject unknown nested keys, duplicate JSON keys, wrong types, Boolean/integer substitutions, unsupported forms, missing references and unreadable inputs. S11's discarded partition is the sole semantic-screening exception; syntax/duplicate-key/readability checks still apply.
    99	Settings keys only: permissions, sandbox, hooks, env, enableAllProjectMcpServers, enabledMcpjsonServers, disabledMcpjsonServers, enabledPlugins, syncClaudeAiPlugins, syncClaudeAiSkills, extraKnownMarketplaces, disableSkillShellExecution.
   100	permissions: only defaultMode=auto where applicable, additionalDirectories=[], and exact source-specific renderer-declared deny/native-denial fragments; no caller allow/ask or alternate mode.
   101	sandbox: only enabled, failIfUnavailable, autoAllowBashIfSandboxed, allowUnsandboxedCommands, excludedCommands, filesystem, network, enableWeakerNestedSandbox, enableWeakerNetworkIsolation, allowAppleEvents. Every present Boolean/list equals its source's declared canonical fragment.
   102	filesystem: only allowWrite and disabled. network: only allowedDomains, allowUnixSockets, allowAllUnixSockets, allowLocalBinding. Pin all leaf/list values from worker/admin policy before merging; no broadened lower-scope arrays.
   103	hooks: exact source/event/matcher/operation forms; groups only matcher/hooks; handlers only type/command/timeout/async/statusMessage/onFailure with exact declared values. Validate type first: only command; HTTP/MCP-tool/prompt/agent/unknown/missing/null/non-string types have no worker form.
   104	MCP approvals: enableAllProjectMcpServers=false, enabledMcpjsonServers=[], disabledMcpjsonServers=[]; never exempt definitions. enabledPlugins maps only declared/inventoried identities to false, both sync fields=false, extraKnownMarketplaces={}, disableSkillShellExecution=true.
   105	Settings env has exactly GH_TELEMETRY="false", DO_NOT_TRACK="1", CHECKPOINT_DISABLE="1", AWS_EC2_METADATA_DISABLED="true"; no other AWS exception, credential/provider string or arbitrary value.
   106	Absent/empty objects pass only where their source permits; canonical partial administrative objects may omit declared fields, never add keys/values. Helpers, status-line commands, wrappers, alternate executables and authentication refresh/export keys have no worker form. Orchestrator PermissionRequest is not a worker exception.
   107	
   108	## S01-S23, roots and component values
   109	
   110	Use user=<validated-home>/.claude-worker, anchor=<validated-home>/Workspace/dotfiles, managed-root=/Library/Application Support/ClaudeCode on Darwin or /etc/claude-code on Linux.
   111	S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 anchor/.claude/settings.local.json; S05 managed-root/managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery.
   112	S08 worktree/.mcp.json; S09 anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json; S12 every skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json.
   113	S16 every default hooks/hooks.json and referenced hook file; S17 each marketplace-root/.claude-plugin/marketplace.json; S18 every default/referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every default/referenced legacy command Markdown file; S22 every subagent Markdown file; S23 every default/referenced plugin LSP file.
   114	Declare independent reads of every matching file, including ignored/untracked, disabled and shadowed inputs; executable environment-file contents join this read set. Unenumerable managed delivery or caller-selected sources require named refusal, without discovery helpers.
   115	Bind anchor to validated passwd home and actual main checkout; worker roots are registered linked worktrees beneath anchor/.claude/worktrees with the same Git common directory. Declare symlink/case-alias handling and containment; foreign roots refuse before side effects for both kinds/routes.

exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|"'^##|task-level audit'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md; git status --short" in ~/Workspace/dotfiles
 succeeded in 40ms:
10:## Architecture
17:## Regime activation and progress
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
29:## Parallel workers
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
67:- Only acceptance decisions and final merge stay orchestrator-side. Seats and scripts handle integration, adversarial RESULT review, review-profile work, gate and records through `verdict.sh`, `audit-pool.sh`, `result-precheck.sh`, `acceptance-front-matter.py` and `dispatch.sh --next`. Pending each mechanism, Delegation's interim exemption permits manual orchestrator execution. Every code-changing RESULT gets one task-level audit of its final head; findings are input, never approval (the "Task-level audit" bullet).
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
95:## Message Contract v1
152:## `.orchestration` Workspace Layout
165:## Orchestrator Playbook
178:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
181:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
182:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
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
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a02.md
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a03.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/plans/024-replan-20261021-v2.md
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-a03.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a02.md
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
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-a02.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md
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
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-2b58663.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-local-review-2b58663.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c761dc8.md
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
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-local-review-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-review-receipt.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json

**Ensuring complete output and quick graphing**
exec
/bin/zsh -lc "sed -n '225,258p' ~/.agents/skills/agmsg-orchestration/SKILL.md; sed -n '104,124p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md; cat .ua/meta.json; git rev-parse HEAD" in ~/Workspace/dotfiles
 succeeded in 38ms:
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

MCP approvals: enableAllProjectMcpServers=false, enabledMcpjsonServers=[], disabledMcpjsonServers=[]; never exempt definitions. enabledPlugins maps only declared/inventoried identities to false, both sync fields=false, extraKnownMarketplaces={}, disableSkillShellExecution=true.
Settings env has exactly GH_TELEMETRY="false", DO_NOT_TRACK="1", CHECKPOINT_DISABLE="1", AWS_EC2_METADATA_DISABLED="true"; no other AWS exception, credential/provider string or arbitrary value.
Absent/empty objects pass only where their source permits; canonical partial administrative objects may omit declared fields, never add keys/values. Helpers, status-line commands, wrappers, alternate executables and authentication refresh/export keys have no worker form. Orchestrator PermissionRequest is not a worker exception.

## S01-S23, roots and component values

Use user=<validated-home>/.claude-worker, anchor=<validated-home>/Workspace/dotfiles, managed-root=/Library/Application Support/ClaudeCode on Darwin or /etc/claude-code on Linux.
S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 anchor/.claude/settings.local.json; S05 managed-root/managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery.
S08 worktree/.mcp.json; S09 anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json; S12 every skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json.
S16 every default hooks/hooks.json and referenced hook file; S17 each marketplace-root/.claude-plugin/marketplace.json; S18 every default/referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every default/referenced legacy command Markdown file; S22 every subagent Markdown file; S23 every default/referenced plugin LSP file.
Declare independent reads of every matching file, including ignored/untracked, disabled and shadowed inputs; executable environment-file contents join this read set. Unenumerable managed delivery or caller-selected sources require named refusal, without discovery helpers.
Bind anchor to validated passwd home and actual main checkout; worker roots are registered linked worktrees beneath anchor/.claude/worktrees with the same Git common directory. Declare symlink/case-alias handling and containment; foreign roots refuse before side effects for both kinds/routes.
Configuration roots: dedicated user directory, anchor/worktree .claude, applicable nested/additional-directory .claude, platform managed root and registry-contained plugin roots. No account-synced, inline, seed, alternate cache or caller-selected root.
Skills roots exactly Enterprise managed-root/.claude/skills, Personal user/skills, Project project/.claude/skills, Nested subdir/.claude/skills, applicable Additional directory add-dir/.claude/skills, Plugin plugin/skills. Read Markdown and bundled descriptors; managed commands/agents start at actual managed-root.
S08-S10/S18-S19 objects permit only absent/empty mcpServers/managedMcpServers. S14 and S23 permit only {}; S16 only absent/empty hooks; approval/disable state cannot authorize servers or handlers.
S12/S15 fields: name/version/description/author/homepage/repository/license/keywords and hooks/mcpServers/lspServers/commands/agents/skills. Descriptive fields are strings, keywords is a string list; author only string name/email/url. Each explicit component is one scalar contained regular-file reference; no arrays/objects/URLs/inline content/directories; defaults expand independently.
S13 only version=2 and plugins: IDs map to record lists with scope/installPath/version/installedAt/lastUpdated/gitCommitSha/projectPath; scope=user|project|local, descriptive members strings, commit 40 hex, paths contained/project-bound; read every descriptor and disable every ID.
S17 only name/owner/metadata/plugins: string name, owner string name/email, metadata string description/version, plugins absent or []. S20-S22 restricted frontmatter only name/description/argument-hint, Boolean disable-model-invocation/user-invocable, declared allowed-tools/model; no unknown/nested executable forms or dynamic shell expansion, including fenced forms.
S11 must be an object; retained mcpServers only {}; oauthAccount only optional string members accountUuid/emailAddress/organizationUuid/displayName/fullName/organizationRole/workspaceRole; userID only ^[0-9a-f]{64}$. Unknown identity members/wrong types/nonempty or malformed retained MCP refuse unchanged.
Declare discard of every other S11 top-level field and the entire projects value without recursive semantic screening: counters, history, allowedTools, caches and prior onboarding are never forwarded. After complete preflight, atomically regenerate exactly mcpServers={}, projects={}, hasCompletedOnboarding=true plus screened identity; never merge old state. Trust uses existing spawn-readiness acceptance.

{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
7da0cdfab9de9fbea673b82379acd4e317115065

exec
/bin/zsh -lc 'git diff -- .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md; cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md' in ~/Workspace/dotfiles
 succeeded in 5ms:
diff --git a/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md b/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
index 108c14d2..2f0ffc7a 100644
--- a/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
+++ b/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
@@ -3,6 +3,7 @@ format: 2
 task_id: dotfiles-T133-worker-write-boundary-slice1-a01
 kind: code
 security: true
+previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9
 worker: a010
 worker_kind: codex
 worker_profile: security
@@ -185,10 +186,12 @@ Report visible impact: this slice declares/tests worker/admin policy, startup co
 No session loses its stop gate from this slice because the tracked commands do not change. dotfiles-T133-worker-write-boundary-slice5-a01 owns switching .claude/settings.json only after stage A provisions <home>/.claude/hooks/orchestrator-only.sh; this slice neither installs that file nor activates its tracked references.
 No deployment, make update/application, login/keyring change, system installation, restart, permission-policy deployment, live socket/worker probe or live-dependent release. Later slices own screening/output registration, orchestrator activation, update/staging/docs/ignore and deployment reconciliation.
 
+Amendment 1 (`previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9`): the Codex sandbox denies the Herdr socket, so `agmsg-dispatch` cannot carry this seat's messages (your PONG attempt for PING 2984 exited 1: `PermissionDenied`, `pane not found or unavailable: wJ:p1`). The named route for every PONG and the RESULT of this task is the pane-less path of Orchestrator Playbook step 6, run from sandboxed Bash: write the single line to a file under `.orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/` and send it with `~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-standard-dot-a010 claude-deep-dot --body-file <that file>` (a013 delivered its PONGs this way on 2026-10-21T05:59Z). This route is the named route, not 'another tool' under the boundary-denial sentence above, and the orchestrator reads the bus at each milestone. First reply `AGMSG-PONG v1 task_id=dotfiles-T133-worker-write-boundary-slice1-a01 status=alive` by that route, then start round 1 as written; the unsent `blocked-pong.txt` and `liveness-2998.txt` stay as evidence.
+
 ## Checks
 
 ```text
-prerequisites merged in canonical main 4eafd890454e495fdb1d429734c5835e46c87652 (gh api repos/mryfmo/dotfiles/branches/main): dotfiles-T133-worker-sandbox-exclusions-a02 = PR #448 merge e042663b2d6efd9205f7d388bf881c01d3880642; dotfiles-T133-trusted-entrypoint-pins-a01 = PR #449 merge 4eafd890454e495fdb1d429734c5835e46c87652; the dispatch branch starts fresh from that main, so merge-base = that SHA
+prerequisites merged in canonical main 7da0cdfab9de9fbea673b82379acd4e317115065 (gh api --hostname github.com repos/mryfmo/dotfiles/branches/main --jq .commit.sha, 2026-10-22T00:46Z, exit 0; git merge-base --is-ancestor 4eafd890454e495fdb1d429734c5835e46c87652 7da0cdfa exit 0): dotfiles-T133-worker-sandbox-exclusions-a02 = PR #448 merge e042663b2d6efd9205f7d388bf881c01d3880642; dotfiles-T133-trusted-entrypoint-pins-a01 = PR #449 merge 4eafd890454e495fdb1d429734c5835e46c87652; the dispatch branch starts fresh from that main, so merge-base = that SHA
 post-prerequisite baseline at that main: agent-config.yaml worker 284:    excludedCommands: [] 285:    linux_excluded_commands: []; validate-agent-assets.py line 344 fails any non-empty worker excludedCommands; home/dot_mise/config.toml node = "26.12.0" python = "3.15.0" uv = "0.13.1"
-observed 2026-10-21T09:17Z by the orchestrator (Claude seat, sandboxed Bash); C1-C10/C7b via pre-send.sh on these bytes exit 0 (see the anchor review record); every value is pasted command output
+observed 2026-10-21T09:17Z and re-observed host-bound 2026-10-22T00:46Z (amendment 1) by the orchestrator (Claude seat, sandboxed Bash); C1-C10/C7b via pre-send.sh on these bytes exit 0 (see the anchor review record); every value is pasted command output
 ```
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a02 round=1 reset_of=dotfiles-T133-worker-write-boundary-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md task_sha256=6d36b24e7601d49f34672f755ec15df375bb7a89cc1b78d51e69f79c8c51881c deadline=none done_signal=AGMSG-RESULT note=a010:reset-text(D-024-26-write-boundary-alone;previous_sha256=999ba3c7454a6191f92c407c10653801e02923d253129322894f8f5f8ee0c3b1;start-a-fresh-branch-from-origin/main-and-leave-tools/worker-write-boundary-a01-untouched;C-80-correct-at-ac9ce14-after-4-rounds;the-Checks-block-at-the-end-carries-the-counters;security:true)",
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a02 round=1 reset_of=dotfiles-T133-worker-write-boundary-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md task_sha256=e96dcac923bf2ba8d926e4618895f959be9c4f01ca29424a7f9251fd8eb5491d deadline=none done_signal=AGMSG-RESULT note=a010:amendment-1(previous_sha256=6d36b24e7601d49f34672f755ec15df375bb7a89cc1b78d51e69f79c8c51881c;the-source-cap-amended-once-to-the-measured-1041-from-your-budget-attribution.json;the-test-cap-1609-stands;two-sentences-of-the-Change-budget-and-the-Checks-block-changed,nothing-else);update-the-task-copy-to-this-text-byte-identical-and-push-on-PR-431;then-RESULT-after-the-Bot-window;no-further-cap-change",
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a02 round=1 reset_of=dotfiles-T133-worker-write-boundary-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md task_sha256=eeccf4e20d5753ce49401b3ea5f30834129798857e6a42de6cc66a5a723cb241 deadline=none done_signal=AGMSG-RESULT note=a010:amendment-1b-clerical-alignment(previous_sha256=e96dcac923bf2ba8d926e4618895f959be9c4f01ca29424a7f9251fd8eb5491d;the-Check-cap-sentence-regime-ci.py-reads-now-says-1041-like-the-Change-budget;no-second-cap-increase;my-C-89-miss:the-consumer-sentence-was-not-enumerated);update-the-task-copy-to-this-text-byte-identical,commit,push-on-PR-431,RESULT-after-CI-and-the-Bot-window",
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a02 round=1 reset_of=dotfiles-T133-worker-write-boundary-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md task_sha256=ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50 deadline=none done_signal=AGMSG-RESULT note=a010:amendment-2-measured(previous_sha256=eeccf4e20d5753ce49401b3ea5f30834129798857e6a42de6cc66a5a723cb241;caps-1111/1768-from-your-revise2-budget-attribution.json,mapped-to-the-four-local-review-rows;Change-budget-and-both-Check-sentences-changed-together;nothing-else);update-the-task-copy-to-this-text-byte-identical-in-the-same-last-round,push,RESULT-after-CI-and-the-Bot-window;no-code-change"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 431,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-worker-write-boundary-a02"
}
---

# Acceptance record: dotfiles-T133-worker-write-boundary-a02

Reset of P1-15's a01 (PR #431, branch tools/worker-write-boundary-a01, from ea3c4fb8) after the final-head security review found a P1 (startup validates only the legacy worktree-local hooks; an existing worktree's tracked `.claude/settings.json` or a legacy apiKeyHelper would run unguarded) at the C-61 cap; the a01 record holds the decision. The a02 text (review profile, prompt `p115-a02r-redesign-prompt.md`) adds the startup validation of every executable configuration entrypoint in the tracked, legacy and user settings and the Worker Playbook step 4 consistency; the a01 implementation stays. Seat: a010 (Codex, worker-e), holding. Advisory owner: dotfiles-T133-worker-write-boundary-followup-a01.

- 2026-10-19T19:58Z: text installed (after the host pause 13:03Z to 19:55Z); checker OK; C-80 first review started.
- 2026-10-19T20:00:56Z: C-80 first review of the a02 text (`…-text-security-2ae9e2c.md`): `Verdict: incorrect` on one P1: the startup screening omits the worktree's `.mcp.json` (project MCP servers execute after trust when `enableAllProjectMcpServers` is true). Round 2 by the review-profile context (prompt `p115-a02r2-redesign-prompt.md`): `.mcp.json` screened, auto-approval off in the worker settings, a malicious-server fixture.
text-security:2ae9e2c:1	input-inventory
- 2026-10-19T20:11Z: round-2 text (`p115-a02r2.md`: `.mcp.json` screened before the start, project MCP auto-approval off in the worker settings, a malicious-server fixture) installed; checker OK; C-80 round 2 next.
- 2026-10-19T20:14:37Z: C-80 round 2 of the a02 text (`…-text-security-ebbb71b.md`): `Verdict: incorrect`: P1 project skills-directory plugins (`.claude/skills/<name>/.claude-plugin/plugin.json`) can load bundled hooks after trust; P1 the configuration directory's global state `.claude.json` holds user-scoped and project-local MCP servers; P2 the quoted ledger contract still reads the sha from `origin` (the amended 5.14 item 8 binds it through the repository API). Class table: 2ae9e2c:1 (.mcp.json), ebbb71b:1 (skills plugins), ebbb71b:2 (.claude.json) = three rows of input-inventory: INV-6 S1. Root cause: the text added executable-configuration sources one review at a time instead of enumerating the documented loading list of the installed Claude Code version. Design 5.14 item 1 amended (the inventory is the documented loading list, enumerated once).
text-security:ebbb71b:1	input-inventory
text-security:ebbb71b:2	input-inventory
text-security:ebbb71b:3	repository-binding
re-plan: input-inventory (rows text-security:2ae9e2c:1, text-security:ebbb71b:1, text-security:ebbb71b:2) — specification: the a02 text named the screened sources piecemeal; design: 5.14 item 1 now defines the inventory as the documented loading list of the installed Claude Code version (settings files of every scope, project .mcp.json, the configuration directory global state .claude.json, plugins and skills directories, hook commands, apiKeyHelper, statusLine, MCP server commands), screened or disabled before workspace trust; implementation: the round-3 text enumerates that list from the documentation into premises and screens every entry in one procedure; verification: one fixture per source class (a planted payload in each) asserting refusal before any command runs, and the quotation of item 8 refreshed.
- 2026-10-19T20:3xZ: round-3 text (`p115-a02r3.md`, the whole re-plan: the documented loading list enumerated once, 22 files, 79 threat rows, 1115 lines against proposal 1's 250-line/10-file caps; not split: past its first review and the launcher slice depends on the settings slice, so a split would serialise two PR cycles on the critical path; S1 on the first fix round splits it) installed with `$HOME`-relative paths; checker next; C-80 round 3 (fresh budget after the re-plan line)
- 2026-10-19T20:36:33Z: C-80 round 3 of the a02 text (`…-text-security-b2a186e.md`, the first review after the re-plan line): `Verdict: incorrect`: P1 the inventory K01 screens hook commands only, so a `type: "http"` hook handler (no command field; POSTs tool input and interpolated credentials to its URL after startup) passes unscreened — the fourth input-inventory finding of the lineage and the first after the re-plan: the re-plan enumerated the documented sources once but kept the field-level unit ("hook commands") inside the hooks source; P2 the deferred ledger's two `gh api` calls bind owner/repo but not the host (`GH_HOST` selects the API host), so `--hostname github.com` and a hostile-host test are required. Disposition: design 5.14 item 1 amended (a hook handler of any documented type is an executable input; a worker refuses every handler type but `command`), item 8 amended (`--hostname github.com` on every gh call that decides); amendment 1 after the re-plan via the review profile (`p115-a02r4-redesign-prompt.md`, whole text with the full findings history, never a delta); C-80 budget after the re-plan: 1 of 3 consumed.
text-security:b2a186e:1	input-inventory
text-security:b2a186e:2	repository-binding
- 2026-10-19T20:5xZ: amendment 1 after the re-plan (`p115-a02r4.md`) installed with `$HOME`-relative paths: 1111 lines (r3 1115), 22 files, 81 threat rows (handler-type unit, host binding), `"http"` fixture, `--hostname github.com` ×4, quoted enumerations with fetched_at ×7; checker OK; C-80 round 4 running (budget after the re-plan: 2 of 3 consumed when it returns).
- 2026-10-19T20:55:28Z: C-80 round 4 (`…-text-security-ac9ce14.md`) `Verdict: correct` (handler-type checks cover the documented non-command hook types; 81 residual rows; plugin-loading page re-fetch failed in the review, noted); text dispatched to a010 (worker-e) with the counters pasted: sha256 6d36b24e7601d49f34672f755ec15df375bb7a89cc1b78d51e69f79c8c51881c, previous_sha256 999ba3c7… (the a01 text); TASK line in the JSON dispatch list.
text-security:ac9ce14:0	correct
- 2026-10-19T20:58:20Z: a010 PONG `status=blocked`: my dispatch note said `start a fresh branch from origin/main and leave tools/worker-write-boundary-a01 untouched` while the hashed text (lines 451 and 1052) says continue that branch and PR #431 from ea3c4fb8; a010 performed no write and asked for the binding. 21:04:12Z: PING interpretation (message 2568, read 21:04:20Z): the text binds; the note is withdrawn; recorded as the orchestrator's mistake (a dispatch note carries no instruction the text does not; C-96). 21:06:20Z: a010 PONG `status=working`: branch tools/worker-write-boundary-a01, PR 431, base 51ba5801, head ea3c4fb8, task_copy 6d36b24e…; first startup regression RED on ea3c4fb8 (the unguarded SessionStart returns 0 instead of refusing; a Git signing environment error kept separately, the clean rerun is the valid red); Claude 2.1.300 matches; loader and source enumeration under way; worker_fix_rounds=0.
- 2026-10-19T22:05:34Z: a010 PONG `working`: its single independent pre-push review complete with 2 P1 (S01: `env.HOME` can select a foreign guard; S20/S21: fenced dynamic commands bypass the inline regex); review-1 fix-1 begins with red regressions; 499-test draft green (not the final byte proof); source 1038 lines (over the 961 cap by 77), tests 1552 of 1609 before the review corrections; complete final attribution to follow; no push yet; no second independent review. The cap amendment waits for the final numstat (PING 21:30).
- 2026-10-19T23:13:33Z: a010 PONG `working`: review-1 fix-1 complete (both P1 with valid red/green); 501 required tests green at unchanged bytes; rendered guard shellcheck/shfmt and Python correctness green; source frozen at 1041 (over 961 by 80), tests 1579 of 1609; per-file and per-control attribution in budget-attribution.json; candidate-assets scan running; pre-push gate green; no commit yet; final numstat and RESULT after push, CI and the Bot window; no third review, no binding work.
- 2026-10-19T23:26:52Z: a010 PONG `working`: pushed to PR #431, head 80869efc3df23cd7ced7fd8d89a3ead3ae3de8fc; all 501 required tests green; the single pre-push review's 2 P1 addressed in one round (worker_fix_rounds=1); source 1041 against the 961 cap (overage 80, per-file and per-control attribution saved; no cap edited); tests 1579 of 1609; Bot 15-minute window and CI watch started; candidate-assets scan still running; RESULT to follow. The cap amendment (one, to the measured final numstat) is prepared at the RESULT.
- 2026-10-19T23:36:17Z: a010 PONG `blocked` (boundary: reviewed source budget): all 501 tests and the exact candidate-assets scan green at the committed bytes; CI 10 pass 1 fail: the regime job's only exit-1 cause is `1041 source lines exceed 961` (log read through the fixed-host API, saved as raw/regime-job-original.txt); per-file and per-control attribution final (budget-attribution.json); no local cap edit or suppression; asks for the reviewed, measured budget amendment with previous_sha256; the Bot window still running; the RESULT follows the window. The orchestrator amends the Change budget once to the measured figures now (amendment 1 of the a02 text).
- 2026-10-19T23:40:53Z: amendment 1 of the a02 text: the source cap amended once to the measured 1041 (per-file numstat at 80869efc; the 240-line screening estimate measured 361 in the worker settings policy; the launcher shrank 26), the test cap 1609 unchanged; two sentences and the Checks block changed; sha256 6d36b24e7601 -> e96dcac923bf; the C-80 verdict ac9ce14 covers the unchanged body; checker re-run; TASK line (amendment 1) sent to a010.
- 2026-10-19T23:47:45Z: a010 PONG `blocked`: amendment 1 changed the Change budget to 1041 but the `## Check` sentence regime-ci.py reads (`caps()` at regime-ci.py:77-99, first match in the Check section) still said 961; a010 did not commit the e96d copy (proof raw/amendment-check-cap-conflict.log). My C-89 miss (the consumer of the cap was not enumerated at the amendment). Amendment 1b at 2026-10-19T23:57:25Z: the Check sentence aligned to 1041, no new authorisation; sha256 e96dcac923bf -> eeccf4e20d57; re-dispatched.
- 2026-10-20T00:01:29Z: a010 PONG `working`: amendment 1b verified byte-for-byte (text sha256 eeccf4e2…); the exact copy committed and pushed, head aded8e4b1dcc0e15971e7af11a2086ef0cd1126e on PR #431; the regime cap function green on the actual 1041 source / 1579 test lines; code unchanged since 80869efc; RESULT after CI and the Bot window.
- 2026-10-20T00:24:59Z: a010 RESULT `status=ready_for_review`: PR #431 head aded8e4b1dcc0e15971e7af11a2086ef0cd1126e, task_copy eeccf4e2… (= amendment 1b), source 1041/1041, tests 1579/1609, worker_fix_rounds 1, independent review rounds 1, Bot none in the final 901 s window; all 501 required tests plus 59 amended-docs tests green; 21 source digests bound to HEAD; feedback 8 items proposed (1 fixed, 7 not-applicable; the orchestrator dispositions); operator-steps.md lists the deployment steps (make update; make install-managed-settings + the printed sudo install; login with CLAUDE_CONFIG_DIR=~/.claude-worker; the separate Codex permgate escape-denial change; restarts). Measured by the orchestrator 2026-10-20T00:26:27Z: 11 checks pass including regime and the ubuntu-26.04 canary, merge state CLEAN, 2 Codex Bot review comments. ACCEPTANCE pending-integration sent; chain after #417's, then security-review.sh, audit, gate, merge; deployment waits the a05 coupling (D-024-31).


## Owned by dotfiles-T133-worker-write-boundary-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:79ea98a:3	advisory-p2
local-finding: 79ea98a:3 not-applicable:advisory P2 owned by dotfiles-T133-worker-write-boundary-followup-a01 (- [P2] Migrate the legacy PreToolUse handler when adding the guard — home/.chezmoitemplates/claude-settings-managed.json); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md (69aae3928ab04247cb888bab165f9e14d09bcf03680d23a26c11a4cb1bf66e0a)
local:79ea98a:4	advisory-p2
local-finding: 79ea98a:4 not-applicable:advisory P2 owned by dotfiles-T133-worker-write-boundary-followup-a01 (- [P2] Screen existing main-local hooks before replacing them — home/dot_claude-worker/modify_private_settings.json:391-); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md (69aae3928ab04247cb888bab165f9e14d09bcf03680d23a26c11a4cb1bf66e0a)
- 2026-10-20T01:15:34Z: the chain on #431: base moved (ba318e53), update-branched to 79ea98a3; sandbox-scan clean; local review (`…-local-review-79ea98a.md`, codex review --base main) 4 findings: P1 herdr-agents:486-488 the new launch-option allowlist rejects the manifest-generated `--advisor fable` (default Claude worker seating fails); P1 the attachment hook under the clean prefix calls `herdr` by bare name with PATH=/usr/bin:/bin and HERDR_AGENTS_LAYOUT dropped (127: no attachment, no seat claim); P2 bootstrap replaces the whole hooks object (local PermissionRequest/Stop handlers deleted); P2 merge_hooks appends the guarded PreToolUse beside the legacy enforce-uv.sh. The chain refused (rc 11: a P0/P1 local finding). Revise round 1 (the second and last worker round under C-61) sent 2026-10-20T01:19:32Z with four selectors; design 5.14 item 2 stands (fixed PATH; absolute paths anchored to the passwd home for herdr and every mise-installed tool; the allowed environment names include what the attachment needs).
local:79ea98a:1	tool-environment
local:79ea98a:2	tool-environment
local:79ea98a:3	partial-fix
local:79ea98a:4	partial-fix
- 2026-10-20T01:23:40Z: a010 PONG `blocked` at the revise preflight: `git merge --ff-only 79ea98a3` exits 128 (`You have not concluded your cherry-pick (CHERRY_PICK_HEAD exists)`); evidence revise-blocked.md. Measured by the orchestrator: .git/worktrees/worker-e/CHERRY_PICK_HEAD dated 2026-10-19 20:37 JST names 7c3a6394 (`feat(agents): bind isolated Claude permission hooks`, an a01-era cherry-pick of this lineage by the same seat) with AUTO_MERGE beside it: the seat's own leftover. PING 2026-10-20T01:26:58Z: authorised `git cherry-pick --quit` (clears the sequencer state, touches neither tree nor index), record it in sandbox.md, confirm a clean status at aded8e4b, then the fast-forward and the round.
- 2026-10-20T01:28:26Z: a010 PONG `blocked`: `git cherry-pick --quit` exited 0 but could not write the shared `.git/packed-refs.lock` (Operation not permitted x3, the Codex sandbox) and CHERRY_PICK_HEAD remained; evidence raw/revise2-quit.json, revise2-clean.json, revise2-ff.json. Orchestrator action 2026-10-20T01:29:11Z (worktree hygiene; the metadata lives in the shared .git under the main checkout): `git -C .claude/worktrees/worker-e cherry-pick --quit` exit 0; CHERRY_PICK_HEAD and AUTO_MERGE gone; HEAD aded8e4b and the tracked tree untouched. PING 2026-10-20T01:29:45Z: proceed with the fast-forward and the round. Mechanism note: a Codex seat cannot clear its own sequencer state because the worktree's git metadata lives outside its writable roots; the P1-15 text's private worker caches do not cover `.git/worktrees/<seat>/`.
- 2026-10-20T01:57:11Z: a010 PONG `working` (last round, final validation): all four selectors red at 79ea98a3 and green on the revised source; no control dropped; fixed PATH kept, Herdr/jq/Node/npm/Codex called by passwd-home-anchored installed paths; measured source 1111 (cap 1041, +70: herdr-agents +36, orchestrator settings +21, worker settings policy +13) and tests 1768 (cap 1609, +159), attribution revise2-budget-attribution.json. Amendment 2 at 2026-10-20T01:58:30Z (measured; each amendment maps to accepted review findings, rows local:79ea98a:1-4): caps 1111/1768 in the Change budget and both Check sentences (C-99); sha256 eeccf4e20d57 -> ae1088a7fdef; dispatched for the copy update inside the same last round.
- 2026-10-20T02:18:32Z: a010 PONG `question` (last round, task copy ae1088a7… = amendment 2): final modules 348 run, 347 pass, 1 fail: tests/unit/test_herdr_agents.py:5906-5909 (`test_repeated_worker_start_replaces_stale_managed_hooks`) writes the current project's main-local settings but binds the legacy check-inbox argv to HOME/Workspace/dotfiles instead of the settings' project; the round's new P2 screen correctly refuses the foreign-project binding; the old bootstrap overwrite had concealed the fixture mismatch. Proposal: a one-line fixture change (local-project branch uses self.workdir.resolve()), no production change. Answer 2026-10-20T02:19:24Z: yes, inside this directed last round (the round's own screen exposed it; a red test cannot ship); rerun 348 + the four selectors; record in revise.yaml.
- 2026-10-20T02:36:11Z: a010 PONG `working`: head edd824ea pushed on PR #431 (task copy ae1088a7 = amendment 2); the authorised one-line fixture alignment recorded in revise.yaml; full 348 + 157 release modules all 505 green; the four selectors red at 79ea98a3 and green; worker_fix_rounds 2 (the last); RESULT after CI and the Bot window.
- 2026-10-20T02:53:43Z: a010 RESULT round 2 (final) `status=ready_for_review`: head edd824ea2d5b3a4b22da3d4263f96ead53fab49e (previous 79ea98a3), base ba318e53, task_copy ae1088a7 (= amendment 2), 22 changed files (7 in this round), source 1111/1111, tests 1768/1768, 505 local tests, CI 11 pass, Bot none after 901 s, feedback 8 items proposed (1 fixed, 7 n/a), open P0/P1 none, worker_fix_rounds 2, one independent pre-push review; operator steps in operator-steps.md (sudo managed-settings install, worker login, make update after a05, restarts); deployment not performed. ACCEPTANCE pending-integration sent 2026-10-20T02:55:36Z; chain on edd824ea running; then security-review.sh, audit, gate, merge.

local:c0f50fa:3	advisory-p2
local-finding: c0f50fa:3 not-applicable:advisory P2 owned by dotfiles-T133-worker-write-boundary-followup-a01 (- [P2] Include parent-directory creation in the installation command — Makefile:213-213); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md (69aae3928ab04247cb888bab165f9e14d09bcf03680d23a26c11a4cb1bf66e0a)
local:c0f50fa:4	advisory-p2
local-finding: c0f50fa:4 not-applicable:advisory P2 owned by dotfiles-T133-worker-write-boundary-followup-a01 (- [P2] Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md (69aae3928ab04247cb888bab165f9e14d09bcf03680d23a26c11a4cb1bf66e0a)
- 2026-10-20T03:14:31Z: security-profile review of the chain's update-branch head c0f50fa1 (`…-security-c0f50fa.md`) `Verdict: incorrect`: P1 the startup inventory accepts the AWS credential-chain selectors (CLAUDE_CODE_USE_BEDROCK, AWS_CONFIG_FILE, AWS_SHARED_CREDENTIALS_FILE, AWS_PROFILE), so settings can select a worker-controlled `credential_process` that executes through authentication, outside the Bash sandbox (K02 defeated); P1 S04 screens the fixed dotfiles anchor's local settings although `herdr-agents --add-worker … <DIR>` accepts other repositories, so a hook in `<DIR>/.claude/settings.local.json` stays executable (pass the validated main root into screening or refuse other roots); P2 object-form plugin command mappings (`{"source": …}`, inline `content`) pass recursive screening without Markdown inspection. The review's masker step failed (`ModuleNotFoundError: tomllib`: the unsandboxed uv resolved Python 3.10; the glue now binds the mise interpreter) and the review file is unmasked (the boundary masks it). Rows input-inventory (the family's 4th, 5th and 6th finding after the re-plan of 20:3xZ). C-61: both worker rounds are spent, so the lineage resets to a03 (the operator's standing order: no third round on a mechanism PR) once the running chain's audit of c0f50fa1 returns, with its findings folded in; the re-plan changes the approach from "screen the documented list of executable keys" to "allowlist the settings, sources and roots a worker start accepts and refuse everything else" (design 5.14 item 1's "refusing any payload it did not write", generalised; recorded in the residual list, D-024-29). #435 merges now (D-024-33: the P1-15 chain no longer needs its base).
security:c0f50fa:1	input-inventory
security:c0f50fa:2	input-inventory
security:c0f50fa:3	input-inventory
- 2026-10-20T03:17Z: the chain on the update-branch head c0f50fa1 (base 118daafa): local review 4 findings (the review file lists each twice; rows 1-4: P1 Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243; P1 Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206; P2 Include parent-directory creation in the installation command — Makefile:213-213; P2 Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633; P1 Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206; P1 Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243; P2 Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633; P2 Include parent-directory creation in the installation command — Makefile:213-213; P1 Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206; P1 Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243; P2 Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633; P2 Include parent-directory creation in the installation command — Makefile:213-213); the chain refused (rc 11) before the audit. With the security review's two P1 and no worker round left, a02 is withdrawn and the lineage resets to a03 (continue PR #431 from c0f50fa1; the allowlist re-plan; design by reference to shorten the text); the a03 text is being authored by the review profile. #435 merged at 03:18:08Z (main 60a6fb2b) per D-024-33; the main checkout fast-forwarded.
local:c0f50fa:1	tool-environment
local:c0f50fa:2	tool-environment
local:c0f50fa:3	partial-fix
local:c0f50fa:4	partial-fix

---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a03 round=1 reset_of=dotfiles-T133-worker-write-boundary-a02 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md task_sha256=5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669 deadline=none done_signal=AGMSG-RESULT note=a010:reset-a03(reset_of=a02,withdrawn-at-edd824ea-by-the-security-review-of-c0f50fa1;the-text-continues-PR-431-on-tools/worker-write-boundary-a01-from-c0f50fa1;allowlist-re-plan;design-5.14-by-reference;C-80:f7af699-incorrect->amendment-1(CLAUDE_ENV_FILE-contents),9bd6198-correct;pre-send-on-these-bytes:task-consistency-check-OK,C11-6/6,SECRET_PATTERN-0,home-paths-0,624-lines;counters-and-history-in-the-Checks-block)",
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a03 round=1 reset_of=dotfiles-T133-worker-write-boundary-a02 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md task_sha256=49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b deadline=none done_signal=AGMSG-RESULT note=a010:amendments-2-4(previous_sha256=5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669;answers-your-blocked-PONG-2694:D-024-34-the-global-state-file-is-launcher-generated-at-every-start,D-024-35-with-no-per-project-inventory(projects-regenerated-empty,trust-via-the-launcher's-dialog-acceptance),the-enterprise-skills-root-is-<managed-root>/.claude/skills;C-80:49161bc-correct;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0;update-the-task-copy-byte-identical-and-start-the-implementation-per-the-text)"
  ],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "input-inventory",
      "id": "audit:f7af699:1"
    },
    {
      "class": "input-inventory",
      "id": "audit:5067ed0:1"
    },
    {
      "class": "input-inventory",
      "id": "audit:efa211d:1"
    },
    {
      "class": "input-inventory",
      "id": "audit:be969e3:1"
    }
  ],
  "pr": null,
  "replans": {
    "input-inventory": {
      "design": "an inventory the family has now failed to complete six times is removed, not extended (the refusal for a non-empty top-level `mcpServers` stays as tamper evidence)",
      "implementation": "amendment 3 written whole by the review profile (`p115-a03-r4-prompt.md`) with an A-then-B sequential-start fixture on the shared directory, red on c0f50fa1 and green after",
      "specification": "the generated global state file declares no per-project inventory at all: `projects` is regenerated empty and the anchor's workspace trust comes from the launcher's existing trust-dialog acceptance (D-024-35)",
      "verification": "C-80 round 4 (the first round after this line)."
    }
  },
  "searches": [],
  "task": "dotfiles-T133-worker-write-boundary-a03"
}
---

# Acceptance record: dotfiles-T133-worker-write-boundary-a03

Plan 024 P1-15 reset a03 (reset_of a02; PR #431 continued from c0f50fa1; seat a010). Re-plan: allowlist (accept only the declared keys, environment names, sources, roots and value forms; refuse everything else), after the sixth input-inventory finding (security review c0f50fa1: AWS credential-chain selectors, other-repository roots, object-form plugin commands) and the local review of c0f50fa1 (2 P1 + 2 P2). Design 5.14 by reference (D-024-30): 609 lines (a02: 1112), 22 files, 85 threat rows; checker OK after install.

- 2026-10-20T03:31:52Z: text authored by the review profile (`p115-a03-redesign-prompt.md` -> `redesign/p115-a03.md`), installed with `$HOME`-relative paths; C-80 round 1 running.
- 2026-10-20T03:34Z: C-80 round 1 (`…-text-security-f7af699.md`) `Verdict: incorrect`, one P1: `CLAUDE_ENV_FILE` selects shell code executed before each Bash command; the allowlist binds only its pathname, not its contents, so pre-existing contents can execute commands or restore refused variables; require empty or launcher-generated trusted contents before forwarding, with a planted-content regression. Amendment 1 via the review profile at 2026-10-20T03:35:17Z (budget 1 of 3).
text-security:f7af699:1	input-inventory
- 2026-10-20T03:43:14Z: amendment 1 written whole by the review profile (`p115-a03-r2-prompt.md` -> `redesign/p115-a03-r2.md`) and installed: `CLAUDE_ENV_FILE` named as the only admitted variable selecting a file whose contents execute (read-only probe of the documented environment variables); preflight accepts its file only when absent, empty or byte-identical to the launcher-generated contents of this start, inspected without sourcing; one closed row with the selector `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` and one planted-content regression (red on c0f50fa1, green after). 35 changed lines against round 1; 622 lines; pre-send.sh: checker OK, SECRET_PATTERN 0 matches, no literal home path; sha256 f7af699… -> 9bd6198f1abec37ac618757c140b21fa799b987dbf4317c6a66ac16a9cefde24. C-80 round 2 running (budget 2 of 3).
- 2026-10-20T03:48:43Z: C-80 round 2 (`…-text-security-9bd6198.md`) `Verdict: correct` (budget 2 of 3 used; the CLAUDE_ENV_FILE P1 closed by amendment 1).
text-security:9bd6198:0	correct
- 2026-10-20T04:00Z: Checks block pasted (checker OK; C11 6/6 selectors; SECRET_PATTERN 0; home paths 0; C-80 history; counters tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0); final 624 lines, sha256 5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669; AGMSG-TASK round 1 dispatched to a010 (worker-e, wJ:p5) via dispatch.sh (`p115-a03-dispatch.txt`); read_at filled by fill-dispatch.py.
- 2026-10-20T04:00:43Z: a010 PONG `blocked` (message 2694) at preparation, before any edit: its read-only probe of the installed loader (Claude Code 2.1.300, loader sha256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3; `raw/loader-state-probe.json`) shows the loader itself persists `numStartups` at every start and `hasCompletedOnboarding` at onboarding into the global state file, while S11 admits only `mcpServers` and `projects`; the exact schema would refuse the worker's own native state at the next ordinary start. The text's rule (block and retask, never widen silently) was followed. Disposition: owner amendment 2 (D-024-34): the global state file becomes launcher-generated at every start (declared shape plus screened identity fields), refusing only declared-structure violations; see the re-plan line below.
worker:5067ed0:1	input-inventory
re-plan: input-inventory (rows text-security:2ae9e2c:1, text-security:ebbb71b:1-2, text-security:b2a186e:1, security:c0f50fa:1-3 of the a02 lineage; the a03 reset) — specification: a worker start accepts only the settings keys, environment names, configuration sources, roots and value forms the manifest and the renderer declare, and refuses the start with a named message for anything else (allowlist, not a screened list of executable keys); design: 5.14 item 1 generalised to every input (the residual-list entry of 2026-10-20; design frozen, D-024-29, applied by reference, D-024-30); implementation: the a03 reset text (allowlist schema, one fixture per allowlist class, the three c0f50fa1 findings as regressions); verification: C-80 rounds f7af699 (incorrect, 1 P1) and 9bd6198 (correct).
re-plan: input-inventory (rows text-security:f7af699:1, worker:5067ed0:1, after the allowlist re-plan) — specification: every file the worker's loader consumes at start that the regime need not preserve is launcher-generated at each start, so pre-existing contents never reach the loader; design: D-024-34 (the global state file written from the declared shape plus screened identity fields; refusal only for declared-structure violations; `CLAUDE_ENV_FILE` in the same family); implementation: amendment 2 written whole by the review profile (`p115-a03-r3-prompt.md`), fixtures red on c0f50fa1 and green after (regenerated state, planted `mcpServers`, non-string `oauthAccount` member); verification: C-80 round 3 (the last of the budget; a further round needs a new re-plan line, C-92).
- 2026-10-20T04:23Z: amendment 2 written whole by the review profile (`p115-a03-r3-prompt.md` -> `redesign/p115-a03-r3.md`, D-024-34) and installed: the global state file is launcher-generated at every start (declared shape plus screened identity fields; refusal only for declared-structure violations), the S11 row closed with the selector `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_global_state_with_screened_identity`, a premise carrying the orchestrator's loader probe (sha256 475517ca…, 2.1.300, grep counts 12/15 unquoted, 1/0 quoted), three fixtures red on c0f50fa1; 57 changed lines against the dispatched text; 649 lines; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 5067ed07… -> efa211d1fa4e8fc90512fc88acf6e8cad1127d10a74defafe5adab2e2817faf5. C-80 round 3 running (the last of the budget; C-92).
- 2026-10-20T04:29Z: C-80 round 3 (`…-text-security-efa211d.md`) `Verdict: incorrect`, one P2 (line 431): all Claude workers share `.claude-worker/.claude.json`, but S11 accepts only the anchor's and the current worktree's project keys, so after worker A generates valid state, worker B's start rejects A's key even sequentially; the same-worktree restart fixture misses it. Budget 3 of 3 used; a 4th round needs a new re-plan line (C-92).
text-security:efa211d:1	input-inventory
re-plan: input-inventory (row text-security:efa211d:1, after the launcher-generated-files re-plan) — specification: the generated global state file declares no per-project inventory at all: `projects` is regenerated empty and the anchor's workspace trust comes from the launcher's existing trust-dialog acceptance (D-024-35); design: an inventory the family has now failed to complete six times is removed, not extended (the refusal for a non-empty top-level `mcpServers` stays as tamper evidence); implementation: amendment 3 written whole by the review profile (`p115-a03-r4-prompt.md`) with an A-then-B sequential-start fixture on the shared directory, red on c0f50fa1 and green after; verification: C-80 round 4 (the first round after this line).
- 2026-10-20T04:41Z: amendment 3 written whole by the review profile (`p115-a03-r4-prompt.md` -> `redesign/p115-a03-r4.md`, D-024-35) and installed: the generated state file carries no per-project inventory (`projects: {}` regenerated; trust via the launcher's existing dialog acceptance), rows for the project-key inventory removed, an A-then-B sequential-start fixture on the shared directory; 39 changed lines against amendment 2; 650 lines; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 efa211d1… -> be969e32246c9a1a55e61654d28be9111328fde0e7730a300465bb2e43b0c47e. C-80 round 4 running (the first round after re-plan 3).
- 2026-10-20T04:49Z: C-80 round 4 (`…-text-security-be969e3.md`, the first after re-plan 3) `Verdict: incorrect`, one P1 (line 425): the design screens `<managed-root>/skills` and excludes `<managed-root>/.claude/skills`, which the pinned loader 2.1.300 consumes (documented loading locations), so managed skill content escapes preflight and fixture 502 tests the wrong directory. Disposition: amendment 4 after the orchestrator's read-only probe of the loader's skill-directory strings (pasted in the prompt); maps to the row below. Rounds after re-plan 3: 1 of 3 (C-92).
text-security:be969e3:1	input-inventory
- 2026-10-20T04:58Z: amendment 4 written whole by the review profile (`p115-a03-r5-prompt.md` -> `redesign/p115-a03-r5.md`) and installed: the enterprise skills root is `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), the admitted skills roots are the documented six, fixture 502 plants Markdown and bundled plugin payloads there through the temporary managed-root fixture, the row's premise quotes the documented table and the loader probe (C-87); 22 changed lines against amendment 3; 654 lines; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 be969e32… -> 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b. C-80 round 5 running (the second after re-plan 3).
- 2026-10-20T05:02Z: C-80 round 5 (`…-text-security-49161bc.md`) `Verdict: correct` (rounds after re-plan 3: 2 of 3). Checks block re-pasted (amendment history, C-80 history, counters); final sha256 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b; AGMSG-TASK (amendments 2-4, previous_sha256 5067ed07cf353371…) dispatched to a010 (worker-e, wJ:p5) via dispatch.sh (`p115-a03-amend-dispatch.txt`); read_at filled by fill-dispatch.py. The text at this sha joins the records PR so regime-ci verifies the a03 copy against main.
text-security:49161bc:0	correct
- 2026-10-20T05:03Z: correction to the previous line: the Checks re-paste did not happen (the paste script asserted on the block's shape: the amendment-4 text carries prose between the heading and the fence) and the shell continued despite `set -e`, so TASK 2740 (read by a010 at 05:02:26Z) carries sha256 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b, exactly the bytes C-80 round 5 reviewed (`Verdict: correct`); the Checks block inside them is the review's reproduction of the send-1 paste, and the amendment summary travelled in the TASK note. No resend: the dispatched bytes are the reviewed bytes. Mechanism (M-20261020-03 amended): orchestrator edit-and-dispatch commands verify each step positively (`grep -q` of the pasted marker, `|| exit 1` on every step) instead of relying on `set -e`, which this harness shell did not honour for the failed `uv run` step.
- 2026-10-20T05:08:10Z: a010 PONG `working` (2744): amendments 2-4 verified; the new state-provider, root-component, env-file and schema regressions are red at c0f50fa1; the managed-skills selector (amendment 4) is already green in all four Darwin/Linux Markdown/plugin cases because c0 already inventories `<managed-root>/.claude/skills` (the review's P1 was a text-inventory error, not an implementation gap); a010 asks to disposition that required red as retained baseline coverage. Disposition (2026-10-20T06:01Z, PING `p115-a03-2744-disposition.txt`): accepted; no artificial failing fixture; the selector stays as the row's test, report.md states the finding's nature with the four cases pasted; red-then-green applies to the rows whose control is new.
- 2026-10-21T01:50Z: R1-1 (re-plan v2, J2 default): the a04 reset text (653 lines, undispatched, C-80 round 1 P2) is withdrawn as a single text and replaced by four slices `dotfiles-T133-worker-write-boundary-slice{1,2,3,4}-a01` per the review-profile allocation draft `.agents/worklog/orchestrator-glue/a04-allocation-r1.md` (22 paths, 90 threat rows and the retained findings assigned; table saved as `.orchestration/plans/024-allocation.tsv`). Decisions taken by default: slice ids S1-S4 with serial shared-file scopes; slice 1 is the sole reset_of a03 carrier (allowed_files 8, after []); provisional caps 650 source / 650 tests for slice 1, reconciled against a04's 1591/2528 at RESULT, no silent increase; owner `dotfiles-T133-trusted-entrypoint-descendants-followup-a01` created now (J1) and named by the slices for guard/delivery/formatter/map binding; four slice namespaces, predecessor evidence retained unchanged, no purported dispatched a04 copy; the foreign-root refusal identifier uses slice 2's dispatched id; dependency edges: network -> S1, launcher consumers -> S2, settings prerequisites -> S3, audit/verdict documentation -> S4 (independent pins/resolver/a05 edges kept). Slice 1 text authoring starts through author-loop.sh (brief `brief-wwb-slice1.md`, C-80 <= 2).
- 2026-10-21T02:43Z: slice 1 text (author-loop, 190 lines, 8 paths) took three C-80 rounds: rounds 1-2 one P2 on absent owner files (slice2/slice4/agmsg-hardening stubs created, bytes unchanged, review re-run), round 3 a new P2 (`…-text-security-f4246e9.md`): switching the tracked hooks in `.claude/settings.json` to a guard that stage A has not yet installed removes the stop gate from sessions loading the tracked settings. S-R5: no fourth round on this design; re-slice: `.claude/settings.json` and the tracked-hook switch move to a new slice 5 (`dotfiles-T133-worker-write-boundary-slice5-a01`, after slice 4 and deployment stage A), slice 1 keeps 7 paths and renders the guard template only. Brief v2 (`brief-wwb-slice1-v2.md`); author-loop restarts for the re-sliced design (the round count is per design, S-R5).


**Checking budget and task scope**
codex
この slice は実行時の隔離を完成させるものではなく、宣言・レンダー・固定ルーティングの土台として記述されています。保留されたリスクを区別したうえで、参照先の所有タスクと過去の指摘を照合し、残余リスクとされた制御が実際に何を軽減するかを確認しています。
exec
/bin/zsh -lc "jq -r '.nodes[] | select((.filePath // \"\") | test(\"generate-agent-configs|herdr-agents|modify_private_settings\")) | [.filePath,.summary] | @tsv' .ua/knowledge-graph.json | head -20; git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- home scripts; rg --files --hidden .orchestration/validation .orchestration/dotfiles-T133-worker-write-boundary-a03 .orchestration/acceptance | rg '(c0f50fa|worker-write-boundary-slice1|worker-write-boundary-a03)'" in ~/Workspace/dotfiles
 succeeded in 99ms:
home/dot_claude/modify_private_settings.json	chezmoi modify_ script (Python despite the .json name) that merges the rendered managed Claude settings baseline with Claude-owned runtime state in ~/.claude/settings.json, replacing managed permission and SessionStart hooks in place and appending the herdr-agents --attach hook.
home/dot_claude/modify_private_settings.json	Parses stdin text into a dict, returning None for blank, invalid, or non-object JSON so apply falls back to the baseline.
home/dot_claude/modify_private_settings.json	Predicate identifying managed permission hooks whose command is exactly ccgate/permgate followed by 'claude'.
home/dot_claude/modify_private_settings.json	Predicate identifying SessionStart hooks that invoke herdr-agent-state.sh or herdr-agents regardless of rendered home path.
home/dot_claude/modify_private_settings.json	Replaces managed hook entries in place to preserve ordering, keeps unmanaged hooks of mixed entries, and appends remaining managed entries.
home/dot_claude/modify_private_settings.json	Merges per-event hook maps, using managed-entry replacement for predicate-tracked events and additive dedup for other lists.
home/dot_claude/modify_private_settings.json	Top-level settings merge keeping runtime keys (enabledPlugins) from current state, taking managed values otherwise, and delegating hooks to merge_hooks.
home/dot_claude/modify_private_settings.json	Renders the managed baseline template, appends the herdr-agents attach SessionStart hook, merges with stdin state, and writes the result (unchanged text when equal).
home/dot_local/bin/common/executable_herdr-agents	Large Bash launcher that builds, attaches, repairs, and restarts the Claude Code orchestrator and Codex/Claude worker panes in Herdr, seats worker worktrees and agmsg identities, claims the orchestrator seat, runs the visible read-only audit tab with secret masking and verdict gating, and installs the pre-push main-push guard.
home/dot_local/bin/common/executable_herdr-agents	Prints the herdr-agents usage text covering full, attach, restart-worker, audit, add/remove-worker, and bootstrap modes.
home/dot_local/bin/common/executable_herdr-agents	Resolves the worker model profile from the environment, deprecated alias, or manifest-generated model-profiles.env, defaulting to standard.
home/dot_local/bin/common/executable_herdr-agents	Resolves the worker kind (codex or claude) from the environment or model-profiles.env, defaulting to codex.
home/dot_local/bin/common/executable_herdr-agents	Reads and validates the manifest worker worktree path, requiring a single segment under .claude/worktrees/.
home/dot_local/bin/common/executable_herdr-agents	Prints the absolute worker worktree, creating it detached at origin/main when missing and refusing paths that are not worktrees of the repository.
home/dot_local/bin/common/executable_herdr-agents	Finds or registers the agmsg worker identity seated at a worktree, deriving team and suffix from the orchestrator identity and joining with AGMSG_RESOLVE_PROJECT=0.
home/dot_local/bin/common/executable_herdr-agents	Points agmsg delivery hooks at the worker worktree when missing, using turn delivery for codex and both for claude-code.
home/dot_local/bin/common/executable_herdr-agents	Builds the Codex -c writable_roots override granting a linked worktree's git objects, refs, logs, and worktree metadata while keeping config and hooks read-only.
home/dot_local/bin/common/executable_herdr-agents	Prints the agmsg spawn options YAML carrying the worker profile launch arguments and Codex worktree writable roots.
home/dot_local/bin/common/executable_herdr-agents	Despawns a worker seat graceful-first, retrying with --force when the seat needs it.
home/dot_local/bin/common/executable_herdr-agents	Prints the absolute path of an existing worktree of the repository or exits 2.
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
rg: .orchestration/dotfiles-T133-worker-write-boundary-a03: No such file or directory (os error 2)
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03-design-reset.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0f87501.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-3844d93.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0e9bf3f.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0b96f40.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-401573e.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0e9bf3f.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0b96f40.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-3844d93.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-c0f50fa.log
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0f87501.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md.last.md

exec
/bin/zsh -lc 'cat .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md .agents/worklog/orchestrator-glue/a04-allocation-r1.md' in ~/Workspace/dotfiles
 succeeded in 3ms:
# Notes every review-profile brief carries (orchestrator glue, 2026-10-20)

1. Host facts measured before authoring, pasted verbatim: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`. A text names a resolve command and asks the worker to paste its output, never a guessed path (re-plan validation-setup of regime-ci-token-a01).
2. Every evidence item names its producer and seat kind: `orchestrator (Claude seat, sandboxed Bash)` or `worker (<kind> seat)`. A Codex seat cannot probe the herdr socket from its sandbox (PermissionDenied measured 2026-10-20T13:39Z, a013); never ask it to (M-20261020-06/08 class).
3. The self cap leaves room for the orchestrator's Checks block (about 7 lines) when the text keeps a fenced block under `## Checks`; a reset text anchored by a review is dispatched at the anchored bytes with no paste.
4. No restatement of the trusted-execution contract: design 5.14 items by reference; environment and executable rows the tool cannot close are `residual` with an owner (re-plan contract-restatement of regime-ci-token-a01). Texts for security: false tools get no C-80 (D-024-46).
5. Caps in the C-107 sentence form; the numstat command in its own sentence; measurement base pasted at dispatch (the branch head at dispatch for a records-only round after an update-branch, not an older code head).
6. Baseline statements bind to the post-prerequisite state: a text that names `after:` prerequisites describes main as it will be after they merge (their post-merge effects stated in the brief), never as it is on the authoring day (slice 1 of P1-15, 2026-10-21: an old Linux exclusion policy was preserved against a prerequisite that empties it).

1. `024-allocation.tsv`

```tsv
item	kind	slice	reason	intermediate_condition
home/dot_agents/agent-config.yaml	path	1	Declare closed startup policy and static inventory; orchestrator activation revisits this path in slice 3	E1; preserve existing orchestrator output until E3
home/.chezmoitemplates/claude-settings-managed.json	path	3	Activate guarded orchestrator hooks and symmetric exclusions together with validator changes	E3
home/.chezmoitemplates/claude-worker-settings.json	path	2	Register and commit worker output with its preparation consumer	E2
home/.chezmoitemplates/claude-managed-settings.json	path	2	Register administrative output; privileged staging remains slice 4	E2; no installation claim
home/dot_claude/modify_private_settings.json	path	1	Add exact legacy/canonical classification and preserve custom hooks before new forms become effective	E1; activate new baseline in E3
home/dot_claude-worker/modify_private_settings.json	path	2	Own common source screening, prepared-result validation, migration and regeneration	E2
home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl	path	1	Install fixed-operation guard before tracked settings reference it	E1
.claude/settings.json	path	1	Guard all tracked events atomically with guard creation	E1
scripts/generate-agent-configs.py	path	1	Own schema/render functions and guard output; output registration and orchestrator activation recur in slices 2/3	E1/E2/E3; every registered output committed
scripts/validate-agent-assets.py	path	3	Change exact exclusion policy with the orchestrator output it validates	E3
Makefile	path	4	Own nonprivileged staging, printed parent creation and post-Herdr reconciliation	E4
home/dot_local/bin/common/executable_herdr-agents	path	2	Own route screening, anchor refusal, launch environment and interpreter consumption	E2
home/dot_agents/skills/agmsg-orchestration/SKILL.md	path	4	Make the entire Worker Playbook consistently sandbox-only	E4
.gitignore	path	4	Add only .uv-cache/ and verify publication protection	E4
tests/unit/test_generate_agent_configs.py	path	1	Own schema/static-inventory/guard tests; revisit production-output expectations in slice 3	E1/E3
tests/unit/test_validate_agent_assets.py	path	3	Move ordered exclusion fixtures with validator and policy	E3
tests/unit/test_claude_settings_merge.py	path	1	Own exact classification/custom-hook tests; revisit effective baseline in 3 and fake update in 4	E1/E3/E4
tests/unit/test_herdr_agents.py	path	2	Own launcher/source/runtime regressions; add documentation/ignore assertions in slice 4	E2/E4
tests/unit/test_agmsg_orchestration_docs.py	path	4	Own exact sandbox sentence and fixed-host ledger-template contract	E4
tests/unit/test_claude_worker_settings.py	path	2	Own worker preparation/render/deny/delivery integration	E2
tests/unit/test_claude_managed_settings.py	path	4	Own administrative content plus printed-installation target integration	E4
.orchestration/dotfiles-T133-worker-write-boundary-a04/**	path	4	Replace proposed a04 artifact namespace with four actual slice namespaces; final lineage rollup belongs here	Each slice writes its own dispatched copy/evidence; never fabricate an a04 dispatch
home/dot_agents/agent-config.yaml	threat	1	Closed declarations and static inventory; preserve deferred binding ownership	E1
home/.chezmoitemplates/claude-settings-managed.json	threat	3	Guarded baseline; legacy PermissionRequest remains with dotfiles-T133-trusted-entrypoint-binding-a01	E3; other descendant binding belongs to new owner D
home/.chezmoitemplates/claude-worker-settings.json	threat	2	Canonical worker policy and explicit disables accompany preparation	E2
home/.chezmoitemplates/claude-managed-settings.json	threat	2	Canonical administrative content only	E2; installation deferred to E4/operator
home/dot_claude/modify_private_settings.json	threat	1	Exact owned-form classification, ordering and idempotence	E1; no descendant identity claim
home/dot_claude-worker/modify_private_settings.json	threat	2	One source-aware screening policy before mutation	E2
home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl	threat	1	Fixed dispatch and identity routing; descendant binding belongs to D	E1
.claude/settings.json	threat	1	Portable guarded commands and supported failure policy	E1
scripts/generate-agent-configs.py	threat	1	Deterministic declared policy; no candidate-learned schema or installation discovery	E1/E2/E3
scripts/validate-agent-assets.py	threat	3	Preserve all existing checks while moving exact exclusion expectations	E3
Makefile	threat	4	Print privileged commands only; reconcile after installer	E4
home/dot_local/bin/common/executable_herdr-agents	threat	2	All worker routes screen before trust or mutation	E2
home/dot_agents/skills/agmsg-orchestration/SKILL.md	threat	4	No worker escape exceptions; orchestrator exemptions remain distinct	E4
.gitignore	threat	4	Ignore private cache without weakening worklog/cache denies	E4
tests/unit/test_generate_agent_configs.py	threat	1	Both-platform declaration/render correspondence and guard coverage	E1/E3
tests/unit/test_validate_agent_assets.py	threat	3	Exact exclusions, malformed variants and legacy permission composition	E3
tests/unit/test_claude_settings_merge.py	threat	1	Classification and preservation first; effective baseline/update cases later	E1/E3/E4
tests/unit/test_herdr_agents.py	threat	2	Temporary roots and fake processes cover complete startup routes	E2/E4
tests/unit/test_agmsg_orchestration_docs.py	threat	4	Read actual slice-4 dispatched copy; implement no ledger consumer	E4
tests/unit/test_claude_worker_settings.py	threat	2	Configured policy, protected bytes and delivery; complete binding remains residual	E2
tests/unit/test_claude_managed_settings.py	threat	4	Content and printed commands; no administrative execution	E4
.orchestration/dotfiles-T133-worker-write-boundary-a04/**	threat	4	Allocate equivalent evidence controls to every actual slice artifact root	Replicate row in all four texts
<absolute-home>/.claude-worker/settings.json	threat	2	S01 checked before regeneration including every environment entry	E2
<worktree>/.claude/settings.json	threat	2	S02 screens old tracked files without rewriting them	E2; guarded current file already exists from E1
<worktree>/.claude/settings.local.json	threat	2	S03 screening precedes exact legacy migration	E2
<validated-anchor>/.claude/settings.local.json	threat	2	S04 independent main-local screening plus anchor binding	E2
/Library/Application Support/ClaudeCode/managed-settings.json	threat	2	Darwin S05 source-specific screening in temporary managed root	E2
/etc/claude-code/managed-settings.json	threat	2	Linux S05 receives equivalent screening	E2
<managed-root>/managed-settings.d/<name>.json	threat	2	S06 independently checks canonical partial fragments	E2
<absolute-home>/.claude-worker/remote-settings.json	threat	2	S07 independently checks cache and refuses unenumerable delivery	E2
<worktree>/.mcp.json	threat	2	S08 absent/empty only regardless of approval or Git tracking	E2
<validated-anchor>/.mcp.json	threat	2	S09 independently screens inherited main definition	E2
<loaded-ancestor>/.mcp.json	threat	2	S10 independently screens applicable ancestors	E2
<absolute-home>/.claude-worker/.claude.json	threat	2	S11 regenerates empty shared project state every start	E2; cross-worktree fixture
S11 carried identity-field screening	threat	2	Fixed string-only identity members and exact userID shape	E2
<skills-root>/<name>/.claude-plugin/plugin.json	threat	2	S12 covers all six roots including actual enterprise root and disabled plugins	E2
<plugins-root>/installed_plugins.json	threat	2	S13 closed registry records and contained project-bound roots	E2
<plugins-root>/known_marketplaces.json	threat	2	S14 accepts only empty registry	E2
<plugin-root>/.claude-plugin/plugin.json	threat	2	S15 closed metadata and scalar inspected-file references	E2
<plugin-hook-file>	threat	2	S16 default and selected files inspected independently	E2
<marketplace-root>/.claude-plugin/marketplace.json	threat	2	S17 descriptive metadata and absent/empty plugin list only	E2
<plugin-mcp-file>	threat	2	S18 default and selected MCP definitions independently empty	E2
<managed-root>/managed-mcp.json	threat	2	S19 independent empty-server check	E2
<skills-root>/<name>/SKILL.md	threat	2	S20 restricted frontmatter and dynamic-command refusal	E2
<commands-root>/<name>.md	threat	2	S21 inspect default/selected Markdown; reject object/inline/directory forms	E2
<agents-root>/<name>.md	threat	2	S22 restricted metadata without subagent execution	E2
<plugin-lsp-file>	threat	2	S23 empty configuration only	E2
pre-start refusal of unknown settings keys	threat	2	Per-source top-level/nested unknown-key regressions	E2
pre-start refusal of undeclared provider selectors	threat	2	Settings and launch inputs; exact AWS exception only	E2
pre-start refusal of foreign repository roots	threat	2	Both worker kinds and every route refuse before side effects	E2
pre-start refusal of object-form plugin components	threat	2	Disabled-plugin object/source/inline cases refuse	E2
pre-start refusal of non-command hook handlers	threat	2	Inspect type before command; indexed refusal across sources	E2
pre-start refusal of untrusted executable environment-file contents	threat	2	No sourcing; same-start canonical bytes/hash only	E2
manifest-selected non-shim launch interpreter	threat	2	Consume slice-1 declaration on bootstrap/home/preflight routes	E2; no shim/PATH fallback
Darwin platform-injected launch environment	threat	2	Exact optional encoding shape; Linux presence refuses	E2
regime-declared launch environment	threat	2	AGMSG_SPAWNED=1 only for declared roles; retain existing authorities	E2
plugin activation and additional executable components	threat	2	Explicit disables supplement complete source screening	E2
non-file managed delivery and launch overrides	threat	2	Named refusal without discovery helpers	E2
lower-scope sandbox array merging	threat	2	Check each source before merging lists	E2
actual enterprise skills root	threat	2	Managed-root/.claude/skills on both platforms	E2; retain historical green baseline
<absolute-home>/.agents/permgate-policy.yaml	threat	1	Static directory/file protection; execution isolation remains separately owned	E1; deny integration E2
<absolute-home>/.local/lib/python*/site-packages	threat	1	Retain directory and descendant deny patterns	E1; planted-startup binding remains deferred
<absolute-home>/Library/Python/*/lib/python/site-packages	threat	1	Retain macOS directory and descendant patterns	E1; planted-startup binding remains deferred
<absolute-home>/.claude/hooks/orchestrator-only.sh	threat	1	Protect consumed installed guard; descendant execution belongs to D	E1
formatter and project-map configuration selection	threat	1	Reject worker/outside-anchor inputs; complete tool-chain binding belongs to D	E1
.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md	threat	1	Reset carrier retains a03 copy and evidence unchanged	E1; no predecessor deletion
.orchestration/dotfiles-T133-worker-write-boundary-a04/task.md	threat	1	Replace proposed copy with actual slice-1 copy and corresponding per-slice copies	No fake a04 dispatch; every actual copy matches its TASK hash
evidence records	threat	4	Final lineage reconciliation; each earlier slice supplies its own final-head evidence	Replicate in every slice
task metadata	threat	1	Carrier establishes reset lineage; each successor checks its own scope/dependencies	Replicate in every slice
metadata separators	threat	1	Whole-file digest covers format-2 metadata and body	Replicate in every slice
in-process effects	threat	1	Repository generation and temporary fixtures only	Replicate in every slice; no deployment
workflow and interpreter or environment inputs	threat	2	Role-specific startup validation; full downstream binding remains deferred	E2; D owns guard/delivery/formatter/map descendants
new or renamed scripts	threat	1	Existing renderer/preparation/guard surfaces only; no new helper or sidecar	Replicate in every slice
5.14 item 0: 脅威モデル	threat	4	Consolidate honest same-UID/shared-credential residuals	Replicate residual in every slice
5.14 item 1: 書き込み境界	threat	2	Consume declared write policy and complete closed startup screen	E2; no race/reload closure
5.14 item 2: 無害化した環境を最初に	threat	2	Clean role-specific launch inputs; legacy PermissionRequest stays deferred	E2; D owns downstream families
5.14 item 3: 信頼パスの境界検査	threat	2	Canonical anchor/component containment; guard routing already in E1	E2; downstream executable binding remains with D
5.14 item 4: 検証したものを実行し、検証した内容を渡す	threat	1	Fixed guard dispatch only; snapshot/last-use and descendant guarantees remain with consumers	E1; D for the four descendant families
5.14 item 5: 出力と予約の同一性	threat	none	dotfiles-T133-audit-pool-a02 owns pool reservations; consumers own their full-head outputs	Do not add reservation machinery or claim closure here
5.14 item 6: 正直な残余	threat	4	Consolidate residual/deployment reporting without relabelling deferred findings	Replicate in every slice
5.14 item 7: 検証	threat	2	Complete S01-S23 and startup regressions; other slices retain their focused checks	E1-E4; shared helper ownership stays with P1-6
5.14 item 8: 承認はコミット済み台帳から読む	threat	4	Fixed-host template contract only; permission-guard-gate-a05/P1-6 own consumption	E4; no approval consumer
5.14 item 9: 私設キャッシュ	threat	2	Private cache delivery and protected shared-cache inventory	E2; publication ignore E4; resolver/deployment remain separate
5.14 item 10: worker は sandbox 外でコマンドを実行しない	threat	4	Exact Worker Playbook rule and removal of contradictory exemptions	E4; operator Codex deployment remains separate
canonical GitHub API host binding	threat	4	Test both exact templates under hostile GH_HOST	E4; consumer enforcement deferred
hook failure policy	threat	1	Supported tracked/guarded entries retain onFailure block	E1/E2/E3; no timeout/background enforcement claim
agmsg store driver and plugin selection	threat	none	dotfiles-T133-agmsg-hardening-a01 owns driver validation and plugin authorization	Retain static denies and explicit sourcing residual
orchestrator effect merge	threat	4	Final-head evidence and pinned integration are orchestrator authority	Replicate in every slice
orchestrator effect update-branch	threat	4	Every moved head requires fresh required evidence	Replicate in every slice
orchestrator effect forced worker removal	threat	4	None planned; preserve dirty-worktree protections	Replicate in every slice
a01 template-suffix finding f1b862c	finding	1	Guard must remain an executable chezmoi template	E1
text-security:f589c7c:1	finding	2	Inspect legacy local hooks before exact owned migration	E2
a01 validator/exclusion and composition blockers	finding	3	Update every policy-sensitive validator check and fixture together	E3
text-security:772cde0:1	finding	1	Protect permgate policy and interpreter startup inputs	E1; deny integration E2
text-security:f810c30:1	finding	none	dotfiles-T133-trusted-entrypoint-binding-a01 owns PermissionRequest interpreter binding	Legacy command bytes unchanged
text-security:772cde0:2	finding	none	dotfiles-T133-trusted-entrypoint-binding-a01 owns isolated PermissionRequest execution	Static user-site denies do not close execution
text-security:e5c055e:1	finding	none	dotfiles-T133-trusted-entrypoint-binding-a01 owns bound deployment checker execution	No new effective-settings checker
text-security:e5c055e:2	finding	none	dotfiles-T133-trusted-entrypoint-binding-a01 owns non-shim binding-test discovery	Startup interpreter selection in E2 is narrower
text-security:5204254:1	finding	none	dotfiles-T133-trusted-entrypoint-pins-a01 and dotfiles-T133-trusted-entrypoint-binding-a01 own measured layouts	No guessed uv layout
text-security:5204254:2	finding	none	dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns formatter descendant chain	Node availability is not established here
a01 independent pre-push missing/non-executable delivery tool	finding	2	Boundary preparation must not disappear when delivery tool is unavailable	E2
Bot 4313733345 defaultMode omission	finding	2	Worker rendered/prepared policy retains defaultMode auto	E2
security:a286915 sandbox-rule contradiction	finding	4	Settle contradictory Worker Playbook exemptions explicitly	E4
security:ea3c4fb:1	finding	2	Screen old tracked settings before startup; never normalize them to pass	E2; current guarded file supplied by E1
text-security:2ae9e2c:1	finding	2	Project MCP independently screened regardless of approval	E2
text-security:ebbb71b:1	finding	2	Skills-directory plugins remain inventoried when disabled	E2
text-security:ebbb71b:2	finding	2	Global MCP empty; projects discarded and regenerated empty	E2
text-security:ebbb71b:3	finding	4	Canonical main comes from fixed repository API	E4 template contract
text-security:b2a186e:1	finding	2	Handler type checked before command, including command-free HTTP	E2
text-security:b2a186e:2	finding	4	Both deciding API templates explicitly bind github.com	E4
a02 independent pre-push env.HOME	finding	2	Candidate settings environment cannot select a foreign guard	E2
a02 independent pre-push fenced dynamic commands	finding	2	Inspect dynamic commands throughout Markdown including fences	E2
local:79ea98a:1	finding	2	Keep manifest-generated --advisor fable accepted	E2
local:79ea98a:2	finding	2	Keep absolute tool calls and attachment identity environment	E1 guard plus E2 attachment
local:79ea98a:3	finding	1	Preserve custom hooks and exact legacy managed migration	E1
local:79ea98a:4	finding	1	Retain legacy PreToolUse migration; historical main-local screening obligation also belongs to E2	E1/E2; preserve original advisory history
security:c0f50fa:1	finding	2	Refuse AWS/provider credential-chain selectors in settings and launch inputs	E2; c0f50fa1 red
security:c0f50fa:2	finding	2	Refuse foreign repositories before any worker-route side effect	E2; c0f50fa1 red
security:c0f50fa:3	finding	2	Refuse object/inline plugin component forms	E2; c0f50fa1 red
local:c0f50fa:1	finding	2	Use actual enterprise skills root	E2; accepted retained-green baseline
local:c0f50fa:2	finding	2	Reject sandbox list extensions before merging	E2; c0f50fa1 red
local:c0f50fa:3	finding	4	Print privileged parent creation before install	E4; c0f50fa1 red
local:c0f50fa:4	finding	4	Reconcile after fake Herdr installer and prove repeated-update idempotence	E4; c0f50fa1 red
text-security:f7af699:1	finding	2	Screen executable environment-file contents and bind same-start generated bytes	E2
worker:5067ed0:1	finding	2	Discard native counters/state and regenerate S11 after complete preflight	E2
text-security:efa211d:1	finding	2	Sequential sibling starts share config directory; projects always regenerated empty	E2; A-then-B fixture
text-security:be969e3:1	finding	2	Plant Markdown and bundled-plugin fixtures under managed-root/.claude/skills	E2; no manufactured red result
a03 runtime-blocked PONG	finding	2	Use declared non-shim interpreter and explicit platform/regime name classes	E2; preserve failing draft/probe evidence
text-security:d562c68:1	finding	none	dotfiles-T133-trusted-entrypoint-descendants-followup-a01 must own all four excluded descendant families	Owner text/design mapping before dispatch; binding-dependent deployment waits for owner
text-security:08e6ac7:2	finding	none	dotfiles-T133-agmsg-hardening-a01 owns store-driver traversal	Retain residual; static denies are mitigation
text-security:5cbbc03:2	finding	none	dotfiles-T133-agmsg-hardening-a01 owns trusted-plugin sourcing	Retain residual; ordinary stores remain writable
```

2. Slice definitions and intermediate conditions

Keep **four slices**, with reassignment from the provisional grouping. The TSV identifies the primary accountable slice; explicitly listed shared paths are revisited sequentially. Each actual task needs threat rows for **all its own allowed files**, including revisited paths and its evidence directory.

Use task IDs `dotfiles-T133-worker-write-boundary-slice{1,2,3,4}-a01`. Below, `S1`–`S4` abbreviate those IDs and `D` means `dotfiles-T133-trusted-entrypoint-descendants-followup-a01`.

Every merge requires `make render-check`, `make validate-agent-assets`, applicable formatting/lint, required GitHub CI, and fresh final-head review/audit/security evidence. Local Bats remain prohibited. These are proposed conditions, not observed passing results.

**Slice 1 — schema, guard, tracked settings and migration foundation**

`after: []`; **the sole `reset_of: [dotfiles-T133-worker-write-boundary-a03]` carrier**.

Allowed files, **8**:

```text
home/dot_agents/agent-config.yaml
scripts/generate-agent-configs.py
home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
.claude/settings.json
home/dot_claude/modify_private_settings.json
tests/unit/test_generate_agent_configs.py
tests/unit/test_claude_settings_merge.py
.orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**
```

**E1:** Both make targets and the complete `tests.unit.test_generate_agent_configs`, `tests.unit.test_claude_settings_merge`, `tests.unit.test_validate_agent_assets`, `tests.unit.test_herdr_agents`, and `tests.unit.test_agmsg_orchestration_docs` modules pass.

Declare the complete startup schema, source inventory, interpreter/environment authorities and static denies. Add/test pure worker/admin render functions, but **register their output files in slice 2**. Register/render the guard now and change tracked commands atomically with it. Extend orchestrator merge classification using synthetic canonical forms while preserving custom hooks and existing effective baseline.

Keep the existing orchestrator generated template, sandbox/exclusion policy and PermissionRequest command unchanged. Thus the existing validator’s Linux four-entry expectation remains valid until slice 3. No launcher enforcement is claimed yet.

**Slice 2 — startup screening and worker/admin outputs**

`after: [dotfiles-T133-worker-write-boundary-slice1-a01]`; no reset.

Allowed files, **8**:

```text
scripts/generate-agent-configs.py
home/.chezmoitemplates/claude-worker-settings.json
home/.chezmoitemplates/claude-managed-settings.json
home/dot_claude-worker/modify_private_settings.json
home/dot_local/bin/common/executable_herdr-agents
tests/unit/test_herdr_agents.py
tests/unit/test_claude_worker_settings.py
.orchestration/dotfiles-T133-worker-write-boundary-slice2-a01/**
```

**E2:** Both make targets and all five E1 modules plus complete `tests.unit.test_claude_worker_settings` pass.

Register both new generated outputs in the same change as their preparation consumer. Implement the single preflight, S01–S23, executable-file contents, S11 regeneration, all launch routes, narrow interpreter consumption and runtime-name classes. The guard and guarded current tracked settings already exist.

Existing unguarded main-local settings must refuse unchanged; accepting those installations waits for slice 3/application. Administrative content is generated but has no installation target yet. Extract launcher changes selectively from the saved draft: defer documentation/ignore assertions until slice 4. No live dependents are released.

**Slice 3 — effective orchestrator settings and validator alignment**

`after: [dotfiles-T133-worker-write-boundary-slice2-a01]`; no reset.

Allowed files, **8**:

```text
home/dot_agents/agent-config.yaml
scripts/generate-agent-configs.py
home/.chezmoitemplates/claude-settings-managed.json
home/dot_claude/modify_private_settings.json
scripts/validate-agent-assets.py
tests/unit/test_generate_agent_configs.py
tests/unit/test_validate_agent_assets.py
tests/unit/test_claude_settings_merge.py
.orchestration/dotfiles-T133-worker-write-boundary-slice3-a01/**
```

This list has **9**, so one reassignment is necessary: **do not reopen `home/dot_claude/modify_private_settings.json` here**. Slice 1 must finish its complete exact classifier, PreToolUse migration and attachment construction against synthetic canonical fixtures. Slice 3 consumes that implementation unchanged. The resulting allowlist has **8**.

**E3:** Both make targets and all six E2 modules pass.

Activate the orchestrator baseline, guarded hooks, startup failure and exact ordered three exclusions on both platforms. Change manifest, generated output, validator and their literal expectations together. Preserve every existing validator check and legacy PermissionRequest bytes/recognition.

Slice 1’s migration must already handle these forms without deleting custom hooks or keeping stale managed duplicates. `make update` reconciliation after Herdr remains explicitly incomplete until slice 4; no deployment occurs between these merges.

**Slice 4 — update/staging, documentation, ignore and lineage completion**

`after: [dotfiles-T133-worker-write-boundary-slice3-a01]`; no reset.

Allowed files, **8**:

```text
Makefile
home/dot_agents/skills/agmsg-orchestration/SKILL.md
.gitignore
tests/unit/test_claude_managed_settings.py
tests/unit/test_claude_settings_merge.py
tests/unit/test_herdr_agents.py
tests/unit/test_agmsg_orchestration_docs.py
.orchestration/dotfiles-T133-worker-write-boundary-slice4-a01/**
```

**E4:** Both make targets and **all seven complete a04 Check modules** pass, using the two original unittest command groups with the actual slice-4 task copy substituted in documentation fixtures.

Finish printed mkdir/install ordering, fake-update reconciliation, sandbox-only documentation, hostile-host template tests and `.uv-cache/` ignoring. During earlier slices, cache artifacts must remain outside staged changes; the ignore regression becomes mandatory here.

Every slice owns its own byte-identical dispatched copy, report and final-head evidence. Slice 4 reconciles lineage and pending deployment; it does not retrospectively supply missing earlier evidence. Preserve a01/a02/a03 history, the failing draft and counters. R1-2’s fresh branches replace a04’s obsolete instruction to continue PR #431; preserve that branch/draft and close #431 only through orchestrator bookkeeping.

3. J1: descendant-binding owner

Create **`dotfiles-T133-trusted-entrypoint-descendants-followup-a01`**, assigned to a011, `after: [dotfiles-T133-trusted-entrypoint-binding-a01]`, and register it in the design’s implementing-task map before using it as an out-of-scope owner.

Its four families are:

| Family | Execution and input binding it must own |
| --- | --- |
| Guard | Installed guard, its interpreter and fixed project payload chain: ContextDB hooks, stop gate, state/attachment operations and their consumed inputs. |
| Delivery | Fixed agmsg delivery operations, session-start/session-end/check-inbox/identities and reached descendants, executable identities and configuration inputs. Store-driver/plugin authorization remains the agmsg-hardening owner. |
| Formatter | Formatter script and Ruff/Prettier/Node chain, configuration selection, executable availability and rejection tests. |
| Map | Project-map reload and terminal-browser/runtime descendants, selected inputs/configuration and rejection tests. |

Correct the descendant portions of **slice 1** rows for the guard source/installed guard, formatter/map selection, orchestrator merge script, renderer, tracked hooks and design items 2–4; **slice 2** rows for worker delivery, preparation, reached execution/environment inputs and associated tests; **slice 3**’s orchestrator-template row; and **slice 4**’s consolidated residual/deployment text.

Keep those rows residual for their implemented routing/screening portions and name D for deferred binding. Do not transfer the unchanged legacy PermissionRequest, its structural validator or isolated execution away from binding-a01. Version pins remain pins-a01.

Full-binding dependents wait for D. Phase-A deployment retains the plan’s explicit existing-binding allowance, records all four residual families and compensating controls, and does **not** acquire a circular dependency on D.

4. Slice-1 brief for `author-loop.sh`

```markdown
task_id: dotfiles-T133-worker-write-boundary-slice1-a01
purpose: Establish the complete declared startup contract, fixed guard, guarded tracked settings and exact migration foundation; implement no launcher screen yet.
kind: code; security: true; worker: a010, Codex security seat.
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
  - .claude/settings.json
  - home/dot_claude/modify_private_settings.json
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**
after: []
reset_of: [dotfiles-T133-worker-write-boundary-a03]
retained_predecessor_directories: [.orchestration/dotfiles-T133-worker-write-boundary-a03/]
Preserve a01/a02 artifacts, a03 failing draft/probes and all counters; no predecessor deletion or writes.
Use a fresh origin/main branch; preserve tools/worker-write-boundary-a01 and PR #431 history.
Read a04 Closed startup schema/Regression fixtures and BRIEF-TEMPLATE-NOTES.md; retain measured host facts and name every evidence producer/seat.
Declare exhaustive settings/nested values, S01-S23, roots/components, four settings-env pairs, role environments, measured non-shim Python and identity fields.
Test pure worker/admin renders; register those output files only in slice 2. Preserve current orchestrator output/exclusions/PermissionRequest until slice 3.
Render guard now; change tracked hooks with it; finish exact legacy/canonical classification, attachment construction and PreToolUse migration now.
Carry render fixtures: both platforms, static inventory, policy/guard/user-site directory+descendant denies, writable stores, spaces/aliases and deployment-independent rendering.
Carry guard fixtures: anchored positive, worker/sibling/unrelated/missing identities, outside/worker tool inputs, fixed argv/stdin/status and absent BASH_ENV markers.
Carry merge fixtures: custom/mixed hooks, ordering, escaped tilde, stale legacy replacement, PreToolUse and idempotence using synthetic canonical forms.
Declare S11 discard/regenerate/projects-empty, executable-file same-start bytes/hash and runtime-name contracts; their actual launch regressions belong to slice 2.
Threat headings: eight allowed paths; predecessor/current copies; metadata/separators/evidence; effects/environment/scripts; 5.14 items 0-10; merge/update-branch/forced-removal.
Name descendants-followup-a01 for guard/delivery/formatter/map binding; binding-a01 retains PermissionRequest; agmsg-hardening-a01 retains store sourcing.
Proposed cap: at most 650 changed source lines outside tests/, .orchestration/ and the three a04 generated-template exclusions, and 650 under tests/.
Measure with git diff --numstat <authenticated-merge-base> <head>; preserve 51ba5801..c0f50fa1 comparison and reconcile shared-control attribution.
Require E1 complete modules, render-check, validate-agent-assets, changed-file lint, CI and final-head evidence; no local Bats, live deployment or socket probe.
Author at most 193 lines before an approximately seven-line Checks block; final text <=200 lines, <=8 paths, C-80 <=2; anchor reviewed bytes without repasting.
```

5. Decisions needed before dispatch

- **Confirm the four IDs and serial shared-file scopes.** Default: use S1–S4 above; finalize slice 3 with the eight-entry list excluding the already-completed orchestrator modify script.
- **Confirm slice-1 caps after extraction measurement.** Default: provisional **650 source / 650 tests**; reconcile against a04’s aggregate **1591 / 2528**, counting shared controls once. Stop on measured overrun; do not silently increase budgets.
- **Create/register D and amend owner references before C-80.** Default: J1’s new owner, a011, after binding; retain Phase-A residual allowance.
- **Confirm artifact/lineage migration.** Default: four actual slice namespaces, only S1 resets a03, retain predecessor evidence unchanged; never create a purported dispatched a04 copy.
- **Resolve historical finding-label discrepancies.** Default: preserve original advisory records/owner history and carry all observed custom-hook, PreToolUse and main-local-screening obligations; add an explicit crosswalk rather than rewriting history.
- **Choose the foreign-root refusal identifier.** Default: replace a04’s task identifier with S2’s actual dispatched ID and update its exact-message fixture together.
- **Fix all aggregate dependency edges before dispatch.** Default: network→S1; launcher consumers→S2; settings prerequisites→S3; audit/verdict documentation prerequisites→S4, preserving independent pins/resolver/a05 dependencies and deployment gates.

📝 まとめ: a04 の22パス・90脅威行と引継ぎ所見を4スライスへ配分し、J1の所有者とslice 1 briefを整理しました。dispatch前に上記の既定値と証跡・予算配分をorchestratorが確定してください。
Not checked: implementation, tests, CI or live enforcement; no files written. Intermediate green conditions and caps require implementation-time verification.
**Preferring concise responses**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-{3844d93,0b96f40,0e9bf3f,0f87501,4e8b427,e39dc8f,f4246e9}.md.last.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-401573e.md' in ~/Workspace/dotfiles
 succeeded in 14ms:
Reviewed [PR #431](https://github.com/mryfmo/dotfiles/pull/431) at `c0f50fa1383416240ad28959dbc4635afa777175`. Found three gaps in the claimed startup controls.

1. **P1 · High confidence — AWS credential-process selectors bypass screening.**  
   `home/dot_claude-worker/modify_private_settings.json:194` accepts `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE`, allowing settings to select a worker-controlled `credential_process`. The complete preflight accepted this combination in an in-memory probe. Claude uses the AWS credential chain, whose process provider executes the configured command; that execution happens through authentication rather than the sandboxed Bash tool. This defeats K02’s executable-source screening claim. Reject these selectors or inspect their referenced configuration before trust. [Claude authentication](https://code.claude.com/docs/en/amazon-bedrock), [AWS process provider](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/Package/-aws-sdk-credential-providers/)

2. **P1 · High confidence — S04 inspects the wrong main checkout for other repositories.**  
   `home/dot_claude-worker/modify_private_settings.json:254` always screens the fixed dotfiles anchor’s local settings, although `herdr-agents --add-worker … [DIR]` accepts other repositories. A hook in `<DIR>/.claude/settings.local.json` was absent from the inventory and passed the complete preflight. Claude worktrees load their own main checkout’s local settings, so that hook remains executable after launch. Pass the validated repository main root into screening, or refuse unsupported roots. [Worktree settings location](https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository)

3. **P2 · High confidence — Object-form plugin commands escape content inspection.**  
   `home/dot_claude-worker/modify_private_settings.json:292` follows only string/list component references; documented `commands` mappings containing `source` or inline `content` pass recursive screening without Markdown inspection. Both `{"source":"./extra/payload.md"}` and inline dynamic-shell content passed the complete preflight; the referenced file was missing from S21. Plugin disabling mitigates immediate execution, but S15/S21 explicitly promise payload refusal even for disabled plugins. Inspect these forms or reject them. [Plugin command mappings](https://code.claude.com/docs/en/plugins/manifest-reference#commands)

The probes executed the reviewed screening functions with virtual filesystem inputs; no payloads or live workers ran. `git diff --check` passed, and no files were changed.

📝 まとめ: 指定差分と threat_table の監査を完了し、P1 を2件、P2 を1件報告しました。受け入れ判断は orchestrator に委ねます。

Not checked: live enforcement and test-suite execution; GitHub CI was unavailable because `gh` could not connect. Runtime consequences above follow the documented loading behavior.

Verdict: incorrect---
task: dotfiles-T133-worker-write-boundary-a02
head: c0f50fa1383416240ad28959dbc4635afa777175
pr: 431
base: 118daafa4610549d3bc280800cf8b1d36fb851dc
started: 2026-10-20T03:08:09Z
finished: 2026-10-20T03:17:57Z
findings: 4
engine: codex review --base main (profile review, read-only)
---

- [P1] Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243
- [P1] Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206
- [P2] Include parent-directory creation in the installation command — Makefile:213-213
- [P2] Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633

```text
The startup boundary accepts sandbox-widening project settings and misses managed skill inputs. The patch also introduces update and installation regressions; validation was limited to read-only probes and static checks.

Full review comments:

- [P1] Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206
  A worktree settings file containing `sandbox.excludedCommands: ["*"]` or `sandbox.filesystem.allowWrite: ["/"]` passes the complete preflight and remains unchanged. Claude merges these array settings across scopes, so generating empty worker exclusions does not remove the escape or broad write grant, even with the administrative policy installed. Reject noncanonical sandbox extensions before launching; the claimed restricted-write control does not mitigate this input ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243
  Enterprise skills reside under `<managed-root>/skills`, not `<managed-root>/.claude/skills`. Consequently, an existing `/etc/claude-code/skills/p/SKILL.md` or macOS equivalent—and its bundled plugin hooks—is never screened or added to the discovered plugin disables. Use `managed` as the loading root and test the real paths; the current fixtures repeat the incorrect directory, leaving the S12/S20 controls ineffective ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633
  During `make update`, `scripts/update-agent-assets.sh` still runs `herdr integration install claude` after chezmoi applies this guarded command. Herdr recognizes its own literal hook command, so replacing it here causes the installer to append the original unguarded SessionStart hook again. There is no subsequent Claude-settings reconciliation, leaving duplicate execution and managed-settings drift reported by `make doctor`. Update the installation sequence to preserve the guarded entry.

- [P2] Include parent-directory creation in the installation command — Makefile:213-213
  On a fresh CLI installation, `/etc/claude-code` or `/Library/Application Support/ClaudeCode` may not exist. The printed `sudo install -m 0644 ...` command does not create parent directories, so following it fails and leaves the administrative policy undeployed. Print a privileged directory-creation command before the file installation while keeping this target itself nonprivileged.
The startup boundary accepts sandbox-widening project settings and misses managed skill inputs. The patch also introduces update and installation regressions; validation was limited to read-only probes and static checks.

Full review comments:

- [P1] Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206
  A worktree settings file containing `sandbox.excludedCommands: ["*"]` or `sandbox.filesystem.allowWrite: ["/"]` passes the complete preflight and remains unchanged. Claude merges these array settings across scopes, so generating empty worker exclusions does not remove the escape or broad write grant, even with the administrative policy installed. Reject noncanonical sandbox extensions before launching; the claimed restricted-write control does not mitigate this input ([AGENTS.md:78](AGENTS.md#L78)).

- [P1] Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243
  Enterprise skills reside under `<managed-root>/skills`, not `<managed-root>/.claude/skills`. Consequently, an existing `/etc/claude-code/skills/p/SKILL.md` or macOS equivalent—and its bundled plugin hooks—is never screened or added to the discovered plugin disables. Use `managed` as the loading root and test the real paths; the current fixtures repeat the incorrect directory, leaving the S12/S20 controls ineffective ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633
  During `make update`, `scripts/update-agent-assets.sh` still runs `herdr integration install claude` after chezmoi applies this guarded command. Herdr recognizes its own literal hook command, so replacing it here causes the installer to append the original unguarded SessionStart hook again. There is no subsequent Claude-settings reconciliation, leaving duplicate execution and managed-settings drift reported by `make doctor`. Update the installation sequence to preserve the guarded entry.

- [P2] Include parent-directory creation in the installation command — Makefile:213-213
  On a fresh CLI installation, `/etc/claude-code` or `/Library/Application Support/ClaudeCode` may not exist. The printed `sudo install -m 0644 ...` command does not create parent directories, so following it fails and leaves the administrative policy undeployed. Print a privileged directory-creation command before the file installation while keeping this target itself nonprivileged.
```
[P2] High confidence .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:137 — The required predecessor `worker-sandbox-exclusions-a02` empties both platforms’ exclusions and makes the validator reject nonempty lists, but this line requires preserving the old Linux four-entry policy, including `gh *`; retaining that policy would restore unsandboxed execution or fail the prerequisite’s validation. Bind baseline-preservation requirements and fixtures to the post-prerequisite empty-list policy.

Checked all 37 threat rows and seven allowed-file entries against the cited history and owner scopes. No additional findings: execution binding, inherited-environment handling, replacement races and same-user isolation remain explicitly residual.

📝 まとめ: Read-only design review completed; one prerequisite/baseline conflict requires orchestrator disposition.

Not checked: implementation, tests, CI or live enforcement; no files changed. Deferred execution-binding and shared-credential risks remain.
Verdict: incorrect[P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:168](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:168) — Required owners `worker-write-boundary-slice2-a01`, `worker-write-boundary-slice4-a01` and `agmsg-hardening-a01` have no task files in this checkout; their assigned startup-enforcement, sandbox-workflow and store-sourcing obligations therefore lack reviewable scopes, so the stated pre-dispatch ownership check cannot pass.

Checked all 37 threat rows and cited acceptance/review context. All eight allowed paths and required non-path controls have rows; none claims `closed`. No additional finding beyond the explicitly retained execution-binding residuals.

📝 まとめ: Completed the read-only design review; one P2 is submitted for orchestrator disposition.

Not checked: implementation, tests, CI or live enforcement; no files changed. Same-user, shared-credential and deferred execution-binding risks remain.
Verdict: incorrectNo findings in the revised design.

Checked all **37 threat rows**, all **7 allowed-file entries**, and the cited acceptance records, reviews and owner scopes. No row claims `closed`. Declaration, rendering and routing tests support the limited claims made; complete executable binding, inherited-environment handling, replacement races and same-user isolation remain explicitly residual.

The earlier activation gap is addressed: tracked hooks stay unchanged until slice5, which requires actual guard provisioning. This verdict covers the design; the required pre-dispatch Checks and ownership receipt still need completion.

📝 まとめ: Completed the read-only pre-dispatch security review; no additional findings for orchestrator disposition.

Not checked: implementation, tests, CI or live enforcement; no files changed. Deferred execution-binding and shared-credential risks remain.
Verdict: correctNo findings against the stated design. Checked all **37 threat rows**, seven allowed-file entries, cited acceptance/review history and deferred-owner scopes. No row claims `closed`.

The tests support declaration, rendering, routing and migration claims. Complete execution binding—including shim resolution, inherited `GIT_*`, symlink/case aliases, same-user replacement, Linux sandbox escapes and ledger consumption—remains explicitly deferred or residual. The prior activation-order and prerequisite-baseline conflicts are addressed.

Reviewed SHA256: `0f8750104f1b9fa28dfe470a0d31166aa740f22e7dfd83e4f1a8ea7a571611b8`.

📝 まとめ: Read-only design review completed without additional findings; pre-dispatch Checks, prerequisite verification and ownership receipts remain required.

Not checked: implementation, tests, CI or live enforcement; no files changed. Deferred execution-binding and shared-credential risks remain.
Verdict: correct[P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:194](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:194) — The prerequisite check labels its result “canonical main,” but the recorded `gh api repos/mryfmo/dotfiles/branches/main` invocation omits `--hostname github.com`; inherited `GH_HOST` can select another server, so this evidence does not establish the required repository authority. Repeat and record the host-bound check before treating prerequisites as authenticated. [GitHub CLI documentation](https://cli.github.com/manual/gh_help_environment)

Reviewed all 37 threat rows and seven allowed-file entries against the cited acceptance records, reviews and owner scopes. No additional findings: there are no `closed` rows, and shim/descendant binding, inherited-environment handling, replacement races and same-user isolation are explicitly deferred without claiming runtime closure.

Reviewed task SHA256: `4e8b427175e9ddd432044636f109e81d49dba9629ead824eb8516239afaffaaa`.

📝 まとめ: Read-only design review completed; one prerequisite-evidence finding is submitted for orchestrator disposition.

Not checked: implementation, tests, CI or live enforcement; no files changed. Deferred execution-binding and shared-credential risks remain.
Verdict: incorrectNo findings against the stated scope. Checked all **37 threat rows**, seven allowed-file entries, cited acceptance records, both c0f50fa1 reviews and deferred-owner scopes. No row claims `closed`.

The named tests support declaration, rendering, routing and migration checks. Complete execution binding—mise shims, inherited `GIT_*`, symlink/case aliases, replacement races and ledger consumption—remains explicitly residual or separately owned. Same-user processes and shared credentials remain bypass risks. The text addresses the earlier Linux `gh *` exclusion conflict and premature tracked-hook activation.

Reviewed SHA256: `e39dc8fbf4143509c53438d070648a6b03ba211c4af9da1def7534a7167c4bdc`.

📝 まとめ: Read-only design review completed without findings; prerequisite verification, ownership receipts and completed Checks remain required before dispatch.

Not checked: implementation, tests, CI or live enforcement; no files changed. This verdict establishes no runtime isolation guarantee.
Verdict: correct[P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:143](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md:143) — Switching tracked hooks alongside a rendered `.tmpl` does not install their target: `~/.claude/hooks/orchestrator-only.sh` is absent on this host, while line 187 prohibits application; sessions loading these settings therefore lose the stop gate, and `onFailure: block` cannot protect `Stop`—require guard provisioning before activating tracked references. [Hook failure semantics](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)

Checked all 37 threat rows and cited acceptance/review context. All eight allowed paths and required non-path controls have rows; none claims `closed`. Explicitly retained shim, same-user, Git-environment, alias, ledger and descendant-binding risks were not re-reported as new findings.

📝 まとめ: Completed the read-only design review; one P2 finding is submitted for orchestrator disposition.

Not checked: implementation, tests, CI or live enforcement; no files changed. Deferred execution-binding risks remain.
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
session id: 01a16113-38d1-7490-9eed-b06e5cdf8c1a
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
読み取り専用でタスク本文と参照先を確認し、判断した内容が実際の実行対象に結び付く設計かを検証します。agmsg-orchestration と Ponytail のレビュー手順を確認します。
exec
/bin/zsh -lc 'cat ~/.agents/skills/agmsg-orchestration/SKILL.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md' in ~/Workspace/dotfiles
 succeeded in 148ms:
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

 succeeded in 180ms:
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

 succeeded in 256ms:
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a01.md
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a02.md
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a03.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/plans/024-replan-20261021-v2.md
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-a03.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a02.md
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
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-a02.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md
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
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-2b58663.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-local-review-2b58663.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c761dc8.md
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
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-local-review-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-review-receipt.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-worker-write-boundary-slice1-a01
     4	kind: code
     5	security: true
     6	previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9
     7	worker: a010
     8	worker_kind: codex
     9	worker_profile: security
    10	max_turns: 40
    11	allowed_files:
    12	  - home/dot_agents/agent-config.yaml
    13	  - scripts/generate-agent-configs.py
    14	  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    15	  - home/dot_claude/modify_private_settings.json
    16	  - tests/unit/test_generate_agent_configs.py
    17	  - tests/unit/test_claude_settings_merge.py
    18	  - .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**
    19	after: [dotfiles-T133-trusted-entrypoint-pins-a01, dotfiles-T133-worker-sandbox-exclusions-a02]
    20	reset_of: [dotfiles-T133-worker-write-boundary-a03]
    21	retained_predecessor_directories: [.orchestration/dotfiles-T133-worker-write-boundary-a03/]
    22	threat_table:
    23	  - {control: home/dot_agents/agent-config.yaml, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_closed_startup_contract_is_exhaustive checks declarations; dotfiles-T133-worker-write-boundary-slice2-a01 owns their startup enforcement."}
    24	  - {control: scripts/generate-agent-configs.py, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks deterministic policy; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns descendant execution binding."}
    25	  - {control: home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks routing; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns guard/interpreter/payload binding."}
    26	  - {control: tracked-hook activation (.claude/settings.json), disposition: "out-of-scope: dotfiles-T133-worker-write-boundary-slice5-a01"}
    27	  - {control: home/dot_claude/modify_private_settings.json, disposition: "residual: tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_canonical_hook_migration checks exact replacement; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns attachment/delivery descendants."}
    28	  - {control: tests/unit/test_generate_agent_configs.py, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_existing_orchestrator_outputs_are_unchanged pins the post-prerequisite baseline; final-head review checks fixture sensitivity, not live enforcement."}
    29	  - {control: tests/unit/test_claude_settings_merge.py, disposition: "residual: tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_exact_managed_hook_classification distinguishes owned/custom forms; independent final-head review checks assertions."}
    30	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; records bind actual producers, commands and full heads; orchestrator audits claims against diff and CI."}
    31	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-a03/task.md, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; retain predecessor copy, failing draft/probes and counters unchanged, without deletion or writes."}
    32	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/task.md, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; TASK and RESULT externally bind the complete dispatched slice1 bytes by SHA256."}
    33	  - {control: task metadata, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator checks reset lineage, seven paths, dependencies, budgets, counters and anchored bytes before dispatch/acceptance."}
    34	  - {control: metadata separators, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; complete-file hashing includes both format-2 delimiters and body; records confer no execution authority."}
    35	  - {control: evidence records, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; separate inherited/failing observations from new final-head results and preserve actual producer/seat provenance."}
    36	  - {control: in-process effects, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; generation and fake-process fixtures use repository/temporary files; deployment, authentication and administrative effects are forbidden."}
    37	  - {control: workflow and interpreter or environment inputs, disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed operations and declared role inputs mitigate injection but do not bind the complete reached tool chain."}
    38	  - {control: new or renamed scripts, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; only the named guard is introduced; artifact globs permit records, not executable glue, wrappers, resolvers or sidecars."}
    39	  - {control: "<absolute-home>/.agents/permgate-policy.yaml", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks static protection; dotfiles-T133-trusted-entrypoint-binding-a01 owns PermissionRequest isolation."}
    40	  - {control: "<absolute-home>/.local/lib/python*/site-packages", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks directory/descendant denies; dotfiles-T133-trusted-entrypoint-binding-a01 owns planted-startup execution tests."}
    41	  - {control: "<absolute-home>/Library/Python/*/lib/python/site-packages", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks macOS directory/descendant denies; dotfiles-T133-trusted-entrypoint-binding-a01 owns startup isolation."}
    42	  - {control: "<absolute-home>/.claude/hooks/orchestrator-only.sh", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks protection; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns installed-guard binding."}
    43	  - {control: formatter and project-map configuration selection, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks worker/outside-input suppression; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns formatter/map execution and availability."}
    44	  - {control: hook failure policy, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks supported synthetic onFailure block; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 retains reached-execution risk; async/timeouts are not enforcement."}
    45	  - {control: agmsg store driver and plugin selection, disposition: "residual: owner dotfiles-T133-agmsg-hardening-a01; static plugin/trusted-plugin denies reduce exposure; writable-store driver traversal and plugin sourcing remain unclosed."}
    46	  - {control: "5.14 item 0", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; fixed routing/static protection reduce accidental and injected damage; same-UID processes and shared credentials defeat seat-isolation claims."}
    47	  - {control: "5.14 item 1", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; this slice tests declared write policy only; startup enforcement, reloads, races and live enforcement are not closed."}
    48	  - {control: "5.14 item 2", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed guarded operations mitigate injection; PermissionRequest remains with dotfiles-T133-trusted-entrypoint-binding-a01."}
    49	  - {control: "5.14 item 3", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks canonical launch/tool paths; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns descendant identity binding."}
    50	  - {control: "5.14 item 4", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed dispatch limits candidate-selected execution without proving snapshots, last-use hashes or complete executable identity."}
    51	  - {control: "5.14 item 5", disposition: "out-of-scope: dotfiles-T133-audit-pool-a02"}
    52	  - {control: "5.14 item 6", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; report shared capabilities, races, reloads, hook limitations and pending deployment without relabelling them closed."}
    53	  - {control: "5.14 item 7", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations covers this slice; dotfiles-T133-worker-write-boundary-slice2-a01 owns launch regressions; binding remains separately owned."}
    54	  - {control: "5.14 item 8", disposition: "out-of-scope: dotfiles-T133-permission-guard-gate-a05"}
    55	  - {control: "5.14 item 9", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; static shared-cache protection is declared here; private-cache/interpreter delivery and actual startup checks land there."}
    56	  - {control: "5.14 item 10", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice4-a01; Worker Playbook alignment lands there; this worker follows the sandbox boundary now; operator Codex-policy deployment remains separate."}
    57	  - {control: orchestrator effect merge, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator alone integrates through Playbook step 10 with fresh evidence and a pinned final head; shared credentials remain residual."}
    58	  - {control: orchestrator effect update-branch, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator updates the base and refreshes CI, feedback, review, audit/security and cap evidence for the moved head."}
    59	  - {control: orchestrator effect forced worker removal, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; none authorized; preserve dirty work and existing removal refusals."}
    60	---
    61	
    62	# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice1-a01
    63	
    64	## Design
    65	
    66	[memory:decision] Establish the complete declared startup contract, rendered executable guard template and exact migration foundation. Implement no launcher screen and switch no tracked hook reference in this slice.
    67	Worker a010 is a Codex security seat authoring the Claude boundary. Create tools/worker-write-boundary-slice1-a01 fresh from authenticated origin/main; extract only this slice's changes. Preserve tools/worker-write-boundary-a01, PR #431 history, its WIP/draft and unrelated work; orchestrator owns replacement-PR bookkeeping.
    68	Before dispatch, the orchestrator verifies that dotfiles-T133-worker-sandbox-exclusions-a02 (PR #448) and dotfiles-T133-trusted-entrypoint-pins-a01 are merged in that main; `after:` names both (shared files: agent-config.yaml and the two test modules with #448, tests/unit/test_generate_agent_configs.py with pins). Their post-prerequisite main, never authoring-day main or a historical implementation head, binds every baseline-preservation statement and fixture.
    69	That baseline has empty worker excludedCommands on Darwin and Linux, a validator rejecting any non-empty list, and mise declarations uv 0.13.1, python 3.15.0, node 26.12.0. Pin declarations do not establish installed-host deployment; this slice changes none of those pins.
    70	This is the sole reset carrier for a03. Retain a01/a02 artifacts, a03 failing draft/probes and every lineage counter; retained predecessors are read-only, outside allowed writes. Never create a purported dispatched a04 copy.
    71	Read a04's Closed startup schema, Implementation and retained controls, Regression fixtures, Change budget and premises; a02/a03 acceptance, a03 blocked PONG/runtime evidence and both c0f50fa1 reviews; .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md and .agents/worklog/orchestrator-glue/a04-allocation-r1.md.
    72	Preserve original finding IDs/classes, advisory-owner history and counters in a crosswalk; do not reinterpret repeated renderings as independent findings or failing green-new.log as green evidence. The a04 scope is allocated across five slices after separating provisioning from activation; it is not copied wholesale.
    73	Apply .orchestration/plans/024-design-quality.md section 5.14 items 0-10 by reference, including its residual list; do not restate or amend the contract. D-024-26/29/30/34/35 and the allocation govern this slice.
    74	Future screening/regeneration/launch requirements below are declarations for dotfiles-T133-worker-write-boundary-slice2-a01, not implementation or runtime-enforcement claims here.
    75	
    76	## Ownership and activation order
    77	
    78	Preserve slice1 design 1's rounds 1-3 and design 2's rounds 1-2, all findings/receipts and lineage counters, including text-security-3844d93's post-prerequisite baseline finding. C-80 has at most two rounds per authorized design; this text silently resets none. Exhausted rounds require the orchestrator's recorded split/re-plan before another review.
    79	Before dispatch, orchestrator (Claude seat, sandboxed Bash) verifies canonical scoped owner records and implementing-task mappings for slices2-5, descendants-followup-a01, binding-a01, agmsg-hardening-a01, audit-pool-a02 and permission-guard-gate-a05; save their full IDs, scope hashes and dependency checks in the external receipt. Missing ownership blocks dispatch.
    80	Slice2 owns launch enforcement and worker/admin output registration; slice3 owns orchestrator output/exclusion/validator activation; slice4 owns update reconciliation, staging, documentation and deployment reconciliation. Slice5 alone owns tracked-hook activation after deployment stage A actually provisions the guard.
    81	Orchestrator corrects stale stub/allocation claims that slice1 supplies guarded tracked settings or provisions the installed guard; those records are outside worker writes. Deployment-stage-A evidence must establish actual guard installation before slice5; a rendered template or green CI is insufficient.
    82	
    83	## Host facts and evidence producers
    84	
    85	Inherited host facts from BRIEF-TEMPLATE-NOTES.md, supplied by orchestrator (Claude seat, sandboxed Bash), are retained verbatim:
    86	mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
    87	Replay producer: worker (Codex security seat, a010). Run env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv and env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which python3; paste actual stdout/status and resolved regular-file identity, never substitute a guessed uv layout or pin file.
    88	Declare the absolute non-shim mise launch interpreter from that evidence, including bootstrap/home lookup/preflight roles. The inherited a04 probe resolved python3.15 under the same 3.15.0 install; selection here does not implement a resolver or complete binding.
    89	Inherited a04 runtime evidence was produced by worker (Codex review-profile authoring seat): system Python added CPATH/LIBRARY_PATH/MANPATH/SDKROOT plus __CF_USER_TEXT_ENCODING; mise Python added only __CF_USER_TEXT_ENCODING to HOME/LANG/PATH/TERM. Retain the original commands, names, statuses and source hashes as history.
    90	Inherited spawn/loader evidence producer: worker (Codex review-profile authoring seat), as recorded in a04. Spawn evidence records export AGMSG_SPAWNED=1 at upstream spawn.sh line 527, SHA256 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731. Historical loader is 2.1.300, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3; no fresh installed-version claim is made.
    91	Every evidence item names actual producer/seat kind, command, status, time, tested full identity and path. New code/tests/renders/lint/numstat/report and CI collection: worker (Codex security seat, a010); CI execution: GitHub Actions runners; transport, dispatch/acceptance checks and CI verification: orchestrator (Claude seat, sandboxed Bash). Preserve each independent context's actual kind.
    92	C-80 and final security evidence producers: independent worker (Codex security seat); pre-push/local review and task-audit producers: independent worker (Codex review seat). Record each actual context identity, command/status and tested full head; a requested review is not evidence of a completed review.
    93	A Codex seat must not probe the Herdr socket: PermissionDenied was measured 2026-10-20T13:39Z by worker (Codex seat, a013). Use fake CLIs/processes; no socket probe, live seat or private credential inspection.
    94	
    95	## Exhaustive manifest contract
    96	
    97	Declare one renderer-owned schema and static inventory in agent-config.yaml; candidate settings, Git objects and upstream schemas never extend acceptance. Declare source-specific optional/required fields, types, exact values and role subsets, not just key names.
    98	Objects reject unknown nested keys, duplicate JSON keys, wrong types, Boolean/integer substitutions, unsupported forms, missing references and unreadable inputs. S11's discarded partition is the sole semantic-screening exception; syntax/duplicate-key/readability checks still apply.
    99	Settings keys only: permissions, sandbox, hooks, env, enableAllProjectMcpServers, enabledMcpjsonServers, disabledMcpjsonServers, enabledPlugins, syncClaudeAiPlugins, syncClaudeAiSkills, extraKnownMarketplaces, disableSkillShellExecution.
   100	permissions: only defaultMode=auto where applicable, additionalDirectories=[], and exact source-specific renderer-declared deny/native-denial fragments; no caller allow/ask or alternate mode.
   101	sandbox: only enabled, failIfUnavailable, autoAllowBashIfSandboxed, allowUnsandboxedCommands, excludedCommands, filesystem, network, enableWeakerNestedSandbox, enableWeakerNetworkIsolation, allowAppleEvents. Every present Boolean/list equals its source's declared canonical fragment.
   102	filesystem: only allowWrite and disabled. network: only allowedDomains, allowUnixSockets, allowAllUnixSockets, allowLocalBinding. Pin all leaf/list values from worker/admin policy before merging; no broadened lower-scope arrays.
   103	hooks: exact source/event/matcher/operation forms; groups only matcher/hooks; handlers only type/command/timeout/async/statusMessage/onFailure with exact declared values. Validate type first: only command; HTTP/MCP-tool/prompt/agent/unknown/missing/null/non-string types have no worker form.
   104	MCP approvals: enableAllProjectMcpServers=false, enabledMcpjsonServers=[], disabledMcpjsonServers=[]; never exempt definitions. enabledPlugins maps only declared/inventoried identities to false, both sync fields=false, extraKnownMarketplaces={}, disableSkillShellExecution=true.
   105	Settings env has exactly GH_TELEMETRY="false", DO_NOT_TRACK="1", CHECKPOINT_DISABLE="1", AWS_EC2_METADATA_DISABLED="true"; no other AWS exception, credential/provider string or arbitrary value.
   106	Absent/empty objects pass only where their source permits; canonical partial administrative objects may omit declared fields, never add keys/values. Helpers, status-line commands, wrappers, alternate executables and authentication refresh/export keys have no worker form. Orchestrator PermissionRequest is not a worker exception.
   107	
   108	## S01-S23, roots and component values
   109	
   110	Use user=<validated-home>/.claude-worker, anchor=<validated-home>/Workspace/dotfiles, managed-root=/Library/Application Support/ClaudeCode on Darwin or /etc/claude-code on Linux.
   111	S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 anchor/.claude/settings.local.json; S05 managed-root/managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery.
   112	S08 worktree/.mcp.json; S09 anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json; S12 every skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json.
   113	S16 every default hooks/hooks.json and referenced hook file; S17 each marketplace-root/.claude-plugin/marketplace.json; S18 every default/referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every default/referenced legacy command Markdown file; S22 every subagent Markdown file; S23 every default/referenced plugin LSP file.
   114	Declare independent reads of every matching file, including ignored/untracked, disabled and shadowed inputs; executable environment-file contents join this read set. Unenumerable managed delivery or caller-selected sources require named refusal, without discovery helpers.
   115	Bind anchor to validated passwd home and actual main checkout; worker roots are registered linked worktrees beneath anchor/.claude/worktrees with the same Git common directory. Declare symlink/case-alias handling and containment; foreign roots refuse before side effects for both kinds/routes.
   116	Configuration roots: dedicated user directory, anchor/worktree .claude, applicable nested/additional-directory .claude, platform managed root and registry-contained plugin roots. No account-synced, inline, seed, alternate cache or caller-selected root.
   117	Skills roots exactly Enterprise managed-root/.claude/skills, Personal user/skills, Project project/.claude/skills, Nested subdir/.claude/skills, applicable Additional directory add-dir/.claude/skills, Plugin plugin/skills. Read Markdown and bundled descriptors; managed commands/agents start at actual managed-root.
   118	S08-S10/S18-S19 objects permit only absent/empty mcpServers/managedMcpServers. S14 and S23 permit only {}; S16 only absent/empty hooks; approval/disable state cannot authorize servers or handlers.
   119	S12/S15 fields: name/version/description/author/homepage/repository/license/keywords and hooks/mcpServers/lspServers/commands/agents/skills. Descriptive fields are strings, keywords is a string list; author only string name/email/url. Each explicit component is one scalar contained regular-file reference; no arrays/objects/URLs/inline content/directories; defaults expand independently.
   120	S13 only version=2 and plugins: IDs map to record lists with scope/installPath/version/installedAt/lastUpdated/gitCommitSha/projectPath; scope=user|project|local, descriptive members strings, commit 40 hex, paths contained/project-bound; read every descriptor and disable every ID.
   121	S17 only name/owner/metadata/plugins: string name, owner string name/email, metadata string description/version, plugins absent or []. S20-S22 restricted frontmatter only name/description/argument-hint, Boolean disable-model-invocation/user-invocable, declared allowed-tools/model; no unknown/nested executable forms or dynamic shell expansion, including fenced forms.
   122	S11 must be an object; retained mcpServers only {}; oauthAccount only optional string members accountUuid/emailAddress/organizationUuid/displayName/fullName/organizationRole/workspaceRole; userID only ^[0-9a-f]{64}$. Unknown identity members/wrong types/nonempty or malformed retained MCP refuse unchanged.
   123	Declare discard of every other S11 top-level field and the entire projects value without recursive semantic screening: counters, history, allowedTools, caches and prior onboarding are never forwarded. After complete preflight, atomically regenerate exactly mcpServers={}, projects={}, hasCompletedOnboarding=true plus screened identity; never merge old state. Trust uses existing spawn-readiness acceptance.
   124	
   125	## Role environments and same-start runtime files
   126	
   127	Declare child-specific name/value maps for launcher/bootstrap, preparation, spawn-launched worker and guard/delivery/attachment; do not grant every role the union or inherit arbitrary caller names. Existing profile/control-plane selectors are consumed through manifest interfaces, not forwarded settings.
   128	Base HOME/PATH/LANG/TERM authorities follow a04: validated home, prescribed child PATH, C.UTF-8, declared terminal (hooks dumb); TMPDIR is canonical parent-supplied temp. CLAUDE_CONFIG_DIR=user, CLAUDE_PROJECT_DIR=canonical launch identity; CLAUDE_ENV_FILE is parent-bound runtime file.
   129	UV_CACHE_DIR=worktree/.uv-cache; UV_PYTHON_INSTALL_DIR=its python child. Regime names: AGMSG_RESOLVE_PROJECT="0"; AGMSG_STORAGE_PATH=validated selection (unset default supported); AGMSG_CC_MONITOR_KEEP_ALIVE="1" where required; AGMSG_AGENT_PID=numeric runtime identity.
   130	AGMSG_SPAWNED is regime-declared exactly "1", required for spawn-launched roles only. Darwin's optional platform-injected __CF_USER_TEXT_ENCODING full-matches 0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+; Linux presence refuses. CPATH/LIBRARY_PATH/MANPATH/SDKROOT remain undeclared, not silently removed.
   131	HERDR_ENV/HERDR_PANE_ID/HERDR_WORKSPACE_ID/HERDR_AGENTS_LAYOUT/HERDR_SOCKET_PATH carry validated attachment/control-plane identities, managed layout and configured canonical socket; CLAUDE_CODE_SESSION_ID/CLAUDE_PID carry required runtime identities. CLICOLOR_FORCE/FORCE_COLOR only launcher-written "1" where used; CHEZMOI_SOURCE_DIR/CHEZMOI_HOME_DIR preparation-only.
   132	Declare exact per-role presence, ID syntax and values from a04 and post-prerequisite canonical constructors, plus the four fixed env pairs. Preserve canonical attachment's optional/unset fields; no unrelated role gains them. Worker argv only manifest profile --model/--effort/--advisor, including --advisor fable.
   133	Unknown proposed names/values and caller-added settings/MCP/plugin/agent/add-dir arguments refuse. Explicit negatives include CLAUDE_CODE_USE_BEDROCK, AWS_CONFIG_FILE, AWS_SHARED_CREDENTIALS_FILE, AWS_PROFILE; all undeclared CLAUDE_CODE_USE_*, AWS_*, ANTHROPIC_*, *_API_KEY, *_TOKEN, *_PROFILE and BASH_ENV/ENV/NODE_OPTIONS/NODE_PATH/PYTHON*/LD_*/DYLD_* remain prohibited. Add no AWS parser.
   134	Declare CLAUDE_ENV_FILE acceptance only when absent, empty or byte-identical to canonical launcher contents for this start; inspect without executing/sourcing, reject unreadable/nonregular/foreign contents unchanged. After all checks, launcher writes existing runtime file, records variable+canonical-path+start-bound SHA256 and verifies before forwarding; prior-start/candidate digests never authorize it. No sidecar.
   135	Declare a04's exact zero-based hooks.<event>[<group>].hooks[<handler>] noncanonical hook handler refusal, S11 mcpServers: noncanonical global state, and source/key-only diagnostics; never print payloads/secret values. Runtime-name, executable-file and S11 A-then-B/shared-directory launch regressions belong to slice2; do not add a launcher/preflight implementation here.
   136	
   137	## Guard, renders and complete migration foundation
   138	
   139	Add pure worker/admin render functions and test them now. Register/render only the executable .tmpl guard now; worker/admin output registration and files land with their consumer in slice2. Leave .claude/settings.json byte-identical; slice5 owns its tracked command switch after stage A.
   140	Preserve byte-for-byte the orchestrator template/generated output, sandbox/exclusions, PermissionRequest command/recognition and registered outputs relative to post-prerequisite main, except registering the new guard. Both platforms' worker exclusions stay empty and the validator rejects non-empty lists; preserve no old Linux or gh exclusion. Slice3 owns subsequent orchestrator activation/alignment; slice5 owns tracked-hook activation. No Codex/shared writable-root policy changes.
   141	Worker render: auto, sandbox startup failure, no unsandboxed request, empty exclusions/no Herdr socket, four existing agmsg stores as narrow grants, explicit MCP/sync disables and false plugin IDs including discovered @skills-dir identities.
   142	Admin render: enabled sandbox/failIfUnavailable, filesystem enforcement; disabled unsandboxed/weaker-isolation/Apple Events/all-socket/local-binding switches; exact single Herdr socket and ordered exclusions agmsg-dispatch *, herdr-agents *, <home>/.agents/skills/agmsg/scripts/actas-claim.sh *. These remain shared capabilities, not worker escape authority.
   143	Static trusted_paths derive from consumed inputs, never Git tree/index: anchored source/control paths, tracked/main-local settings, .orchestration, .agents/worklog/** and .agents/worklog/uv-cache/**, worker .claude directory+descendants and .mcp.json; ordinary worktree/cache writes remain available.
   144	Protect installed manifest/profiles/permgate policy, skill scripts/SKILL files, agmsg plugin code and db/trusted-plugins, .claude/.claude-worker and guard, wrappers/application code, config/state/tool installations/shared uv caches; both user-site directory and descendant patterns protect .pth/usercustomize.py/sitecustomize.py. No blanket .agents/** or .local/** deny: db/teams/run/ext-tools remain writable except trusted-plugins.
   145	Guard accepts only manifest-fixed operations/argv. Canonical anchor identity alone permits project payloads; worker/sibling/unrelated/missing identities suppress them. Only fixed worker delivery runs for canonical workers; never trust writable run/proj.<pid>.project over explicit identity. Formatter/map additionally suppress worker/outside-anchor tool paths.
   146	Preserve stdin bytes, argv boundaries, child status, fixed payload paths and event/matcher/async/timeout markers; test supported onFailure=block through synthetic canonical hooks. Preserve absolute tool calls and attachment re-exports; caller cwd/tool input never selects a payload.
   147	Finish exact legacy/canonical classification, attachment construction and SessionStart/PostToolUse/PreToolUse migration now using synthetic canonical guarded baselines. Preserve production merge output for post-prerequisite main until slice3 activation; synthetic canonical-baseline selection must not depend on installed tools or add a rollout switch.
   148	Recognize only complete owned forms with canonical project/guard/prefix/operation/argument binding; reject near-matches as custom, never basename/substring ownership. Retain supported old-home legacy forms and stale ccgate/permgate handling without broadening PermissionRequest.
   149	Preserve custom/mixed hooks and ordering, quoted/escaped literal tilde distinctions, wrapper/chained/foreign commands; replace stale owned entries once, including enforce-uv PreToolUse; construct exactly one guarded attachment with declared identities and retain byte-idempotence. Slice3 must consume this merge implementation unchanged.
   150	Complete guard/delivery/formatter/map binding, interpreters/configuration/availability and replacement races: dotfiles-T133-trusted-entrypoint-descendants-followup-a01. Legacy PermissionRequest structural validation/isolation: dotfiles-T133-trusted-entrypoint-binding-a01. Store driver/plugin sourcing: dotfiles-T133-agmsg-hardening-a01.
   151	
   152	## Check
   153	
   154	Prerequisite check: orchestrator (Claude seat, sandboxed Bash) records authenticated merged heads for dotfiles-T133-worker-sandbox-exclusions-a02 (PR #448) and dotfiles-T133-trusted-entrypoint-pins-a01, verifies empty worker exclusions on both platforms, non-empty-list validator refusal and exact uv 0.13.1/python 3.15.0/node 26.12.0 declarations; compare all preservation fixtures to that post-prerequisite main.
   155	Write regressions before implementation using existing temporary-HOME/render/merge/fake-process builders; put new coverage only in the two allowed modules. No new dependency, helper script or runtime validator; synthetic payloads record markers and never run real services.
   156	GenerateAgentConfigsTest::test_closed_startup_contract_is_exhaustive pins all keys/nested values, S01-S23, roots/components, role maps, interpreter and identity/discard contracts against an independent expected inventory, not the candidate manifest alone.
   157	GenerateAgentConfigsTest::test_worker_admin_policy_renders covers Darwin/Linux, exact static inventory, policy/guard/user-site directory+descendant denies, writable stores/trusted-plugin exception, ordinary worktree/cache allowance, spaces/symlink/case aliases and explicit plugin disables.
   158	GenerateAgentConfigsTest::test_existing_orchestrator_outputs_are_unchanged pins post-prerequisite production output, .claude/settings.json bytes/references and expected_outputs membership; pure worker/admin renders succeed without installed guard/tools/admin policy and without registering their output files.
   159	GenerateAgentConfigsTest::test_guard_routes_fixed_operations invokes the rendered template through synthetic canonical hook commands: anchored positive; worker/sibling/unrelated/missing identities; outside/worker tool inputs; aliases/spaces; known/unknown operations, invalid extra args, fixed argv/stdin/status and absent hostile BASH_ENV markers.
   160	ClaudeSettingsMergeTest::test_exact_managed_hook_classification and test_canonical_hook_migration cover custom/mixed forms, ordering, escaped tilde, complete canonical binding, stale legacy replacement, PreToolUse and repeated byte-idempotence against synthetic canonical baselines.
   161	ClaudeSettingsMergeTest::test_guarded_attachment_construction covers one absolute guarded attachment, declared identity/store re-exports, spaces, absent optional fields and absent BASH_ENV markers using fakes; preserve post-prerequisite production-baseline expectations and synthetic legacy migration coverage.
   162	E1 requires complete modules, not selected tests: uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_validate_agent_assets tests.unit.test_herdr_agents tests.unit.test_agmsg_orchestration_docs -v.
   163	Run make render-check, make validate-agent-assets and changed-file repository lint/format checks, including rendered-guard shellcheck/shfmt and Python checks. Shell comments are English shdoc. No local Bats; required Bats/all required CI come from GitHub Actions before RESULT.
   164	The final diff has at most 650 changed lines outside tests/, .orchestration/, home/.chezmoitemplates/claude-settings-managed.json, home/.chezmoitemplates/claude-worker-settings.json and home/.chezmoitemplates/claude-managed-settings.json, and 650 under tests/.
   165	Measure with git diff --numstat <authenticated-merge-base> <head>.
   166	Changed means additions plus deletions; exclusions grant no write permission. Orchestrator supplies authenticated full merge-base/head evidence at dispatch; local origin/main alone is not authentication. For a records-only round after update-branch use its dispatch branch head, not an older code head.
   167	Preserve complete git diff --numstat 51ba5801 c0f50fa1 output; separate already-merged base rows, retained extraction and new work, reconcile per-control source/test attribution against a04 1591/2528, count shared controls once. Report actual per-file/totals; 650/650 is a ceiling, not a measured result.
   168	This complete task text stays at most 200 lines including Checks, with at most eight allowed_files entries and at most 193 lines before Checks. A measured overrun or missing prerequisite produces blocked PONG for re-tasking; never hide code in artifacts, weaken coverage, raise caps or edit outside the seven entries.
   169	
   170	## Artifacts, review and completion
   171	
   172	Worker (Codex security seat, a010) writes task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md, result.txt, budget/crosswalk and -worker- Crit-data JSON/receipt beneath this task's directory in its own worktree; RESULT states that location. No canonical task/acceptance/decision/design/other-task edits.
   173	Keep uncommitted seat plan/todo worklogs within that allowed directory using Codex seat worklog fields/sections; update them, allow one active todo per owner and commit no plan/todo/learn worklogs. Durable facts use CompactionDB markers; orchestrator owns main-checkout consolidation/copying/masking.
   174	Paste complete executed outputs/statuses and claimed identifiers, red/green tested identities and selectors, historical evidence sources, generated/installed paths, declared source/role inventories, budget attribution, CI URLs/full heads and feedback dispositions. Missing dependencies/fixtures are not red evidence.
   175	Every command obeys Worker Playbook step 4 and design 5.14 item 10 by reference. A boundary denial yields AGMSG-PONG v1 status=blocked with exact command/status/output/boundary; do not retry through escalation, another tool or socket access.
   176	Allow at most one independent pre-push review and two correction rounds, carrying a01/a02/a03 counters separately. Surviving P0/P1 stops integration; no private third round. Post no @codex review; observe automatic final-head review within the existing bounded window and record bot:none if absent.
   177	Use agent-side Crit data/receipt only, read the saved JSON, resolve each addressed record or record justified review-scope approval, then pass make require-crit-review with the required receipt. No browser/human review request or publish; account for any hook-started review server.
   178	Orchestrator (Claude seat, sandboxed Bash) verifies owner prerequisites, fills Checks before C-80, runs consistency C1-C10/C7b and verifies each C11 obligation, then selector existence/coverage at acceptance. C-80 has at most two rounds per authorized design; a second incorrect verdict stops for split/re-task. Verify remaining budget against every preserved round before requesting review; no private third round.
   179	Anchor the complete reviewed task bytes after Checks is filled; keep the SHA256 in external TASK/review receipt/RESULT. Dispatch/copy those exact bytes without repasting or post-review mutation; any edit requires a new anchor/review within the limit.
   180	Required CI and fresh final-head local review, task audit and independent security evidence precede integration. Orchestrator collects/dispositions feedback and follows Playbook step 10 in order; any moved head refreshes required evidence. Worker grants no acceptance, resolves no GitHub thread and merges nothing.
   181	RESULT names full head/base/branch/new PR, task-copy digest, changed files, all artifact/evidence producers/paths, E1/lint/CI/review outcomes, caps/attribution, open findings/counters and cost or n/a. Preserved PR #431 is history, not this slice's delivery PR.
   182	Report visible impact: this slice declares/tests worker/admin policy, startup contracts and guard/migration foundations; tracked hooks, orchestrator output/exclusions and PermissionRequest remain unchanged relative to post-prerequisite main. Same-UID/shared credentials, shared admin exceptions/socket, sourcing, reloads, races and descendant binding remain residual.
   183	
   184	## Out of scope
   185	
   186	No session loses its stop gate from this slice because the tracked commands do not change. dotfiles-T133-worker-write-boundary-slice5-a01 owns switching .claude/settings.json only after stage A provisions <home>/.claude/hooks/orchestrator-only.sh; this slice neither installs that file nor activates its tracked references.
   187	No deployment, make update/application, login/keyring change, system installation, restart, permission-policy deployment, live socket/worker probe or live-dependent release. Later slices own screening/output registration, orchestrator activation, update/staging/docs/ignore and deployment reconciliation.
   188	
   189	Amendment 1 (`previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9`): the Codex sandbox denies the Herdr socket, so `agmsg-dispatch` cannot carry this seat's messages (your PONG attempt for PING 2984 exited 1: `PermissionDenied`, `pane not found or unavailable: wJ:p1`). The named route for every PONG and the RESULT of this task is the pane-less path of Orchestrator Playbook step 6, run from sandboxed Bash: write the single line to a file under `.orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/` and send it with `~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-standard-dot-a010 claude-deep-dot --body-file <that file>` (a013 delivered its PONGs this way on 2026-10-21T05:59Z). This route is the named route, not 'another tool' under the boundary-denial sentence above, and the orchestrator reads the bus at each milestone. First reply `AGMSG-PONG v1 task_id=dotfiles-T133-worker-write-boundary-slice1-a01 status=alive` by that route, then start round 1 as written; the unsent `blocked-pong.txt` and `liveness-2998.txt` stay as evidence.
   190	
   191	## Checks
   192	
   193	```text
   194	prerequisites merged in canonical main 7da0cdfab9de9fbea673b82379acd4e317115065 (gh api --hostname github.com repos/mryfmo/dotfiles/branches/main --jq .commit.sha, 2026-10-22T00:46Z, exit 0; git merge-base --is-ancestor 4eafd890454e495fdb1d429734c5835e46c87652 7da0cdfa exit 0): dotfiles-T133-worker-sandbox-exclusions-a02 = PR #448 merge e042663b2d6efd9205f7d388bf881c01d3880642; dotfiles-T133-trusted-entrypoint-pins-a01 = PR #449 merge 4eafd890454e495fdb1d429734c5835e46c87652; the dispatch branch starts fresh from that main, so merge-base = that SHA
   195	post-prerequisite baseline at that main: agent-config.yaml worker 284:    excludedCommands: [] 285:    linux_excluded_commands: []; validate-agent-assets.py line 344 fails any non-empty worker excludedCommands; home/dot_mise/config.toml node = "26.12.0" python = "3.15.0" uv = "0.13.1"
   196	observed 2026-10-21T09:17Z and re-observed host-bound 2026-10-22T00:46Z (amendment 1) by the orchestrator (Claude seat, sandboxed Bash); C1-C10/C7b via pre-send.sh on these bytes exit 0 (see the anchor review record); every value is pasted command output
   197	```

exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md | sed -n '1,115p'" in ~/Workspace/dotfiles
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-worker-write-boundary-slice1-a01
     4	kind: code
     5	security: true
     6	previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9
     7	worker: a010
     8	worker_kind: codex
     9	worker_profile: security
    10	max_turns: 40
    11	allowed_files:
    12	  - home/dot_agents/agent-config.yaml
    13	  - scripts/generate-agent-configs.py
    14	  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    15	  - home/dot_claude/modify_private_settings.json
    16	  - tests/unit/test_generate_agent_configs.py
    17	  - tests/unit/test_claude_settings_merge.py
    18	  - .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**
    19	after: [dotfiles-T133-trusted-entrypoint-pins-a01, dotfiles-T133-worker-sandbox-exclusions-a02]
    20	reset_of: [dotfiles-T133-worker-write-boundary-a03]
    21	retained_predecessor_directories: [.orchestration/dotfiles-T133-worker-write-boundary-a03/]
    22	threat_table:
    23	  - {control: home/dot_agents/agent-config.yaml, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_closed_startup_contract_is_exhaustive checks declarations; dotfiles-T133-worker-write-boundary-slice2-a01 owns their startup enforcement."}
    24	  - {control: scripts/generate-agent-configs.py, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks deterministic policy; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns descendant execution binding."}
    25	  - {control: home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks routing; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns guard/interpreter/payload binding."}
    26	  - {control: tracked-hook activation (.claude/settings.json), disposition: "out-of-scope: dotfiles-T133-worker-write-boundary-slice5-a01"}
    27	  - {control: home/dot_claude/modify_private_settings.json, disposition: "residual: tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_canonical_hook_migration checks exact replacement; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns attachment/delivery descendants."}
    28	  - {control: tests/unit/test_generate_agent_configs.py, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_existing_orchestrator_outputs_are_unchanged pins the post-prerequisite baseline; final-head review checks fixture sensitivity, not live enforcement."}
    29	  - {control: tests/unit/test_claude_settings_merge.py, disposition: "residual: tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_exact_managed_hook_classification distinguishes owned/custom forms; independent final-head review checks assertions."}
    30	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; records bind actual producers, commands and full heads; orchestrator audits claims against diff and CI."}
    31	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-a03/task.md, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; retain predecessor copy, failing draft/probes and counters unchanged, without deletion or writes."}
    32	  - {control: .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/task.md, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; TASK and RESULT externally bind the complete dispatched slice1 bytes by SHA256."}
    33	  - {control: task metadata, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator checks reset lineage, seven paths, dependencies, budgets, counters and anchored bytes before dispatch/acceptance."}
    34	  - {control: metadata separators, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; complete-file hashing includes both format-2 delimiters and body; records confer no execution authority."}
    35	  - {control: evidence records, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; separate inherited/failing observations from new final-head results and preserve actual producer/seat provenance."}
    36	  - {control: in-process effects, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; generation and fake-process fixtures use repository/temporary files; deployment, authentication and administrative effects are forbidden."}
    37	  - {control: workflow and interpreter or environment inputs, disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed operations and declared role inputs mitigate injection but do not bind the complete reached tool chain."}
    38	  - {control: new or renamed scripts, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; only the named guard is introduced; artifact globs permit records, not executable glue, wrappers, resolvers or sidecars."}
    39	  - {control: "<absolute-home>/.agents/permgate-policy.yaml", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks static protection; dotfiles-T133-trusted-entrypoint-binding-a01 owns PermissionRequest isolation."}
    40	  - {control: "<absolute-home>/.local/lib/python*/site-packages", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks directory/descendant denies; dotfiles-T133-trusted-entrypoint-binding-a01 owns planted-startup execution tests."}
    41	  - {control: "<absolute-home>/Library/Python/*/lib/python/site-packages", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks macOS directory/descendant denies; dotfiles-T133-trusted-entrypoint-binding-a01 owns startup isolation."}
    42	  - {control: "<absolute-home>/.claude/hooks/orchestrator-only.sh", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_admin_policy_renders checks protection; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns installed-guard binding."}
    43	  - {control: formatter and project-map configuration selection, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks worker/outside-input suppression; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns formatter/map execution and availability."}
    44	  - {control: hook failure policy, disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks supported synthetic onFailure block; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 retains reached-execution risk; async/timeouts are not enforcement."}
    45	  - {control: agmsg store driver and plugin selection, disposition: "residual: owner dotfiles-T133-agmsg-hardening-a01; static plugin/trusted-plugin denies reduce exposure; writable-store driver traversal and plugin sourcing remain unclosed."}
    46	  - {control: "5.14 item 0", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; fixed routing/static protection reduce accidental and injected damage; same-UID processes and shared credentials defeat seat-isolation claims."}
    47	  - {control: "5.14 item 1", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; this slice tests declared write policy only; startup enforcement, reloads, races and live enforcement are not closed."}
    48	  - {control: "5.14 item 2", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed guarded operations mitigate injection; PermissionRequest remains with dotfiles-T133-trusted-entrypoint-binding-a01."}
    49	  - {control: "5.14 item 3", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations checks canonical launch/tool paths; dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns descendant identity binding."}
    50	  - {control: "5.14 item 4", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-descendants-followup-a01; fixed dispatch limits candidate-selected execution without proving snapshots, last-use hashes or complete executable identity."}
    51	  - {control: "5.14 item 5", disposition: "out-of-scope: dotfiles-T133-audit-pool-a02"}
    52	  - {control: "5.14 item 6", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; report shared capabilities, races, reloads, hook limitations and pending deployment without relabelling them closed."}
    53	  - {control: "5.14 item 7", disposition: "residual: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_guard_routes_fixed_operations covers this slice; dotfiles-T133-worker-write-boundary-slice2-a01 owns launch regressions; binding remains separately owned."}
    54	  - {control: "5.14 item 8", disposition: "out-of-scope: dotfiles-T133-permission-guard-gate-a05"}
    55	  - {control: "5.14 item 9", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; static shared-cache protection is declared here; private-cache/interpreter delivery and actual startup checks land there."}
    56	  - {control: "5.14 item 10", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice4-a01; Worker Playbook alignment lands there; this worker follows the sandbox boundary now; operator Codex-policy deployment remains separate."}
    57	  - {control: orchestrator effect merge, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator alone integrates through Playbook step 10 with fresh evidence and a pinned final head; shared credentials remain residual."}
    58	  - {control: orchestrator effect update-branch, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; orchestrator updates the base and refreshes CI, feedback, review, audit/security and cap evidence for the moved head."}
    59	  - {control: orchestrator effect forced worker removal, disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice1-a01; none authorized; preserve dirty work and existing removal refusals."}
    60	---
    61	
    62	# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice1-a01
    63	
    64	## Design
    65	
    66	[memory:decision] Establish the complete declared startup contract, rendered executable guard template and exact migration foundation. Implement no launcher screen and switch no tracked hook reference in this slice.
    67	Worker a010 is a Codex security seat authoring the Claude boundary. Create tools/worker-write-boundary-slice1-a01 fresh from authenticated origin/main; extract only this slice's changes. Preserve tools/worker-write-boundary-a01, PR #431 history, its WIP/draft and unrelated work; orchestrator owns replacement-PR bookkeeping.
    68	Before dispatch, the orchestrator verifies that dotfiles-T133-worker-sandbox-exclusions-a02 (PR #448) and dotfiles-T133-trusted-entrypoint-pins-a01 are merged in that main; `after:` names both (shared files: agent-config.yaml and the two test modules with #448, tests/unit/test_generate_agent_configs.py with pins). Their post-prerequisite main, never authoring-day main or a historical implementation head, binds every baseline-preservation statement and fixture.
    69	That baseline has empty worker excludedCommands on Darwin and Linux, a validator rejecting any non-empty list, and mise declarations uv 0.13.1, python 3.15.0, node 26.12.0. Pin declarations do not establish installed-host deployment; this slice changes none of those pins.
    70	This is the sole reset carrier for a03. Retain a01/a02 artifacts, a03 failing draft/probes and every lineage counter; retained predecessors are read-only, outside allowed writes. Never create a purported dispatched a04 copy.
    71	Read a04's Closed startup schema, Implementation and retained controls, Regression fixtures, Change budget and premises; a02/a03 acceptance, a03 blocked PONG/runtime evidence and both c0f50fa1 reviews; .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md and .agents/worklog/orchestrator-glue/a04-allocation-r1.md.
    72	Preserve original finding IDs/classes, advisory-owner history and counters in a crosswalk; do not reinterpret repeated renderings as independent findings or failing green-new.log as green evidence. The a04 scope is allocated across five slices after separating provisioning from activation; it is not copied wholesale.
    73	Apply .orchestration/plans/024-design-quality.md section 5.14 items 0-10 by reference, including its residual list; do not restate or amend the contract. D-024-26/29/30/34/35 and the allocation govern this slice.
    74	Future screening/regeneration/launch requirements below are declarations for dotfiles-T133-worker-write-boundary-slice2-a01, not implementation or runtime-enforcement claims here.
    75	
    76	## Ownership and activation order
    77	
    78	Preserve slice1 design 1's rounds 1-3 and design 2's rounds 1-2, all findings/receipts and lineage counters, including text-security-3844d93's post-prerequisite baseline finding. C-80 has at most two rounds per authorized design; this text silently resets none. Exhausted rounds require the orchestrator's recorded split/re-plan before another review.
    79	Before dispatch, orchestrator (Claude seat, sandboxed Bash) verifies canonical scoped owner records and implementing-task mappings for slices2-5, descendants-followup-a01, binding-a01, agmsg-hardening-a01, audit-pool-a02 and permission-guard-gate-a05; save their full IDs, scope hashes and dependency checks in the external receipt. Missing ownership blocks dispatch.
    80	Slice2 owns launch enforcement and worker/admin output registration; slice3 owns orchestrator output/exclusion/validator activation; slice4 owns update reconciliation, staging, documentation and deployment reconciliation. Slice5 alone owns tracked-hook activation after deployment stage A actually provisions the guard.
    81	Orchestrator corrects stale stub/allocation claims that slice1 supplies guarded tracked settings or provisions the installed guard; those records are outside worker writes. Deployment-stage-A evidence must establish actual guard installation before slice5; a rendered template or green CI is insufficient.
    82	
    83	## Host facts and evidence producers
    84	
    85	Inherited host facts from BRIEF-TEMPLATE-NOTES.md, supplied by orchestrator (Claude seat, sandboxed Bash), are retained verbatim:
    86	mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`.
    87	Replay producer: worker (Codex security seat, a010). Run env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv and env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which python3; paste actual stdout/status and resolved regular-file identity, never substitute a guessed uv layout or pin file.
    88	Declare the absolute non-shim mise launch interpreter from that evidence, including bootstrap/home lookup/preflight roles. The inherited a04 probe resolved python3.15 under the same 3.15.0 install; selection here does not implement a resolver or complete binding.
    89	Inherited a04 runtime evidence was produced by worker (Codex review-profile authoring seat): system Python added CPATH/LIBRARY_PATH/MANPATH/SDKROOT plus __CF_USER_TEXT_ENCODING; mise Python added only __CF_USER_TEXT_ENCODING to HOME/LANG/PATH/TERM. Retain the original commands, names, statuses and source hashes as history.
    90	Inherited spawn/loader evidence producer: worker (Codex review-profile authoring seat), as recorded in a04. Spawn evidence records export AGMSG_SPAWNED=1 at upstream spawn.sh line 527, SHA256 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731. Historical loader is 2.1.300, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3; no fresh installed-version claim is made.
    91	Every evidence item names actual producer/seat kind, command, status, time, tested full identity and path. New code/tests/renders/lint/numstat/report and CI collection: worker (Codex security seat, a010); CI execution: GitHub Actions runners; transport, dispatch/acceptance checks and CI verification: orchestrator (Claude seat, sandboxed Bash). Preserve each independent context's actual kind.
    92	C-80 and final security evidence producers: independent worker (Codex security seat); pre-push/local review and task-audit producers: independent worker (Codex review seat). Record each actual context identity, command/status and tested full head; a requested review is not evidence of a completed review.
    93	A Codex seat must not probe the Herdr socket: PermissionDenied was measured 2026-10-20T13:39Z by worker (Codex seat, a013). Use fake CLIs/processes; no socket probe, live seat or private credential inspection.
    94	
    95	## Exhaustive manifest contract
    96	
    97	Declare one renderer-owned schema and static inventory in agent-config.yaml; candidate settings, Git objects and upstream schemas never extend acceptance. Declare source-specific optional/required fields, types, exact values and role subsets, not just key names.
    98	Objects reject unknown nested keys, duplicate JSON keys, wrong types, Boolean/integer substitutions, unsupported forms, missing references and unreadable inputs. S11's discarded partition is the sole semantic-screening exception; syntax/duplicate-key/readability checks still apply.
    99	Settings keys only: permissions, sandbox, hooks, env, enableAllProjectMcpServers, enabledMcpjsonServers, disabledMcpjsonServers, enabledPlugins, syncClaudeAiPlugins, syncClaudeAiSkills, extraKnownMarketplaces, disableSkillShellExecution.
   100	permissions: only defaultMode=auto where applicable, additionalDirectories=[], and exact source-specific renderer-declared deny/native-denial fragments; no caller allow/ask or alternate mode.
   101	sandbox: only enabled, failIfUnavailable, autoAllowBashIfSandboxed, allowUnsandboxedCommands, excludedCommands, filesystem, network, enableWeakerNestedSandbox, enableWeakerNetworkIsolation, allowAppleEvents. Every present Boolean/list equals its source's declared canonical fragment.
   102	filesystem: only allowWrite and disabled. network: only allowedDomains, allowUnixSockets, allowAllUnixSockets, allowLocalBinding. Pin all leaf/list values from worker/admin policy before merging; no broadened lower-scope arrays.
   103	hooks: exact source/event/matcher/operation forms; groups only matcher/hooks; handlers only type/command/timeout/async/statusMessage/onFailure with exact declared values. Validate type first: only command; HTTP/MCP-tool/prompt/agent/unknown/missing/null/non-string types have no worker form.
   104	MCP approvals: enableAllProjectMcpServers=false, enabledMcpjsonServers=[], disabledMcpjsonServers=[]; never exempt definitions. enabledPlugins maps only declared/inventoried identities to false, both sync fields=false, extraKnownMarketplaces={}, disableSkillShellExecution=true.
   105	Settings env has exactly GH_TELEMETRY="false", DO_NOT_TRACK="1", CHECKPOINT_DISABLE="1", AWS_EC2_METADATA_DISABLED="true"; no other AWS exception, credential/provider string or arbitrary value.
   106	Absent/empty objects pass only where their source permits; canonical partial administrative objects may omit declared fields, never add keys/values. Helpers, status-line commands, wrappers, alternate executables and authentication refresh/export keys have no worker form. Orchestrator PermissionRequest is not a worker exception.
   107	
   108	## S01-S23, roots and component values
   109	
   110	Use user=<validated-home>/.claude-worker, anchor=<validated-home>/Workspace/dotfiles, managed-root=/Library/Application Support/ClaudeCode on Darwin or /etc/claude-code on Linux.
   111	S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 anchor/.claude/settings.local.json; S05 managed-root/managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery.
   112	S08 worktree/.mcp.json; S09 anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json; S12 every skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json.
   113	S16 every default hooks/hooks.json and referenced hook file; S17 each marketplace-root/.claude-plugin/marketplace.json; S18 every default/referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every default/referenced legacy command Markdown file; S22 every subagent Markdown file; S23 every default/referenced plugin LSP file.
   114	Declare independent reads of every matching file, including ignored/untracked, disabled and shadowed inputs; executable environment-file contents join this read set. Unenumerable managed delivery or caller-selected sources require named refusal, without discovery helpers.
   115	Bind anchor to validated passwd home and actual main checkout; worker roots are registered linked worktrees beneath anchor/.claude/worktrees with the same Git common directory. Declare symlink/case-alias handling and containment; foreign roots refuse before side effects for both kinds/routes.

exec
/bin/zsh -lc "rg -n 'Codex seat worklogs|"'^##|task-level audit'"' ~/.agents/skills/agmsg-orchestration/SKILL.md; cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md; git status --short" in ~/Workspace/dotfiles
 succeeded in 40ms:
10:## Architecture
17:## Regime activation and progress
21:- A Claude session started in the repository root outside Herdr (a plain shell, mosh/ssh, or `claude -p`) is a pane-less orchestrator: nothing seats a worker automatically, and the SessionStart `herdr-agents --attach` hook prints a summary line naming that state, the on-demand commands, and any seated worker, followed in a regime repository by the `agmsg-orchestration:` directive line. Bring the regime up on demand: claim the seat outside the sandbox with the composite instance id, `actas-claim.sh <repo> claude-code <name> <session_id>.<claude pid>` (a claim from sandboxed Bash writes the bare session id and turn delivery then skips silently; see the seat-lock bullet below); seat the worker with `herdr-agents --add-worker <worktree>` (it derives `HERDR_SOCKET_PATH` from the default Herdr server socket `~/.config/herdr/herdr.sock`, the path the Claude sandbox allowlists, before creating anything, accepts a claude worker's workspace-trust dialog during spawn's readiness wait, and takes `--ready-timeout <seconds>`); confirm the worker's placement from its `run/spawn.*` placement record itself (the `herdr:<socket>:<pane>` row that upstream `agmsg_spawn_path` resolves) and the `linkage=` line `--add-worker` prints, never from `team.sh <team> --json`, which observes Codex members by reading their pane; treat the `linkage=` line `--add-worker` prints as the `AGMSG-PING` evidence, and on `pong=no` or `linkage=unreached` wake again with `agmsg-dispatch <team> <orchestrator> <worker> <pane> 'AGMSG-PING v1 task_id=<id> reason=<reason>'` and verify the PING's `read_at` (`poke.sh` only for a viewed workspace); and dispatch no AGMSG-TASK before its `AGMSG-PONG` arrives. Without a managed workspace the auditor runs headless, in the form the task-level audit bullet below names. A pane-less session uses turn delivery when the Monitor cannot run; see "Identity, delivery, and storage" for the platform limits.
29:## Parallel workers
33:- Delegate all repository-mutating work — file edits, builds, test runs, and git state changes — to seated workers, with at most one seated worker per git worktree and sequential assignments within one worktree. Add worktrees for parallelism; never use parallel `codex exec` or per-task Codex spawning, except that the read-only, non-interactive task-level audit the orchestrator runs during acceptance (the task-level audit bullet below) is not worker spawning and is permitted; it is identity-less. agmsg/herdr control-plane commands (`delivery.sh`, `watch.sh`, `actas-claim.sh`, `send.sh`, `join.sh`, and herdr agent/pane commands) are orchestrator-side exemptions.
43:  - Some steps stay sequential. The single audit tab serializes audits; the task-level audit of T67 reduces them to one per task. The orchestrator-side gate (`make require-crit-review`) and merges also run one at a time.
46:## Identity, delivery, and storage
59:## Live verification
64:## Review and integration invariants
67:- Only acceptance decisions and final merge stay orchestrator-side. Seats and scripts handle integration, adversarial RESULT review, review-profile work, gate and records through `verdict.sh`, `audit-pool.sh`, `result-precheck.sh`, `acceptance-front-matter.py` and `dispatch.sh --next`. Pending each mechanism, Delegation's interim exemption permits manual orchestrator execution. Every code-changing RESULT gets one task-level audit of its final head; findings are input, never approval (the "Task-level audit" bullet).
72:- Before every acceptance action (revise, accept, merge) the orchestrator runs `scripts/regime-counters.sh <task id>` and pastes its output into the acceptance record. S2 is decided from INV-6's counts: each component the script prints is read from its output, and for each component it prints as `unknown` the record pastes the command and output that read the source INV-6 names for that component, or, while that source has no entry for the task, says so and pastes the reading of the interim record the orchestrator used in its place. S1 (plan 006: the same finding class three times on one artifact, from any reviewer) is decided from the record's finding-class table, which gives a class to every finding the PR-feedback sweep lists, whatever its disposition, and to every task-level audit finding; three rows of one class stop the artifact. Read that table over non-advisory rows only: list advisory P2 rows with their classes (`advisory-p2` and the `local:<sha7>:<n>` rows `local-advisory.sh` writes), exclude them from S1's three-rows count, and name the excluded rows in the record. The gate's S6 check still sees every ledger row, so an advisory class at three rows gets its `searches` entry from `acceptance-front-matter.py` like any other. INV-6's message and head counts and the S2 lines (`revises`, `amendments`, `questions`, `bot_p1_heads`) take no ledger rows; `scripts/regime-counters.sh` prints them unchanged.
95:## Message Contract v1
152:## `.orchestration` Workspace Layout
165:## Orchestrator Playbook
178:       - A P2 finding of the Codex Bot, local review or task-level audit is advisory: disposition it `not-applicable:advisory P2 owned by <lineage>-followup-a0<n>` and record an `<id><TAB><class>` row under `## Owned by <owner>` in the lineage's acceptance record, with the orchestrator writing the owner task file before the row.
181:    2. Run the task-level audit of that head in the pair or headless form of the task-level audit bullet. It exits nonzero for every verdict other than `correct`. An exit with `Audit verdict: incorrect` is not a failed step: continue to step 3 and disposition its findings. A `blocked` or missing verdict means re-running the audit.
182:    3. Write the acceptance record, summarising the dispositions, with every audit finding dispositioned as the task-level audit bullet says: for an `incorrect` verdict the record's JSON `audit_findings`, which the gate reads through `ACCEPTANCE_EVIDENCE`.
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
 M .orchestration/acceptance/dotfiles-T128-chain-glue-finish-a02.md
 M .orchestration/acceptance/dotfiles-T133-pre-send-check-a03.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-progress.tsv
 M .orchestration/plans/024-replan-20261021-v2.md
 M .orchestration/tasks/dotfiles-T133-audit-pool-a02.md
 M .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md
 M .orchestration/tasks/dotfiles-T133-codex-worker-network-a01.md
 M .orchestration/tasks/dotfiles-T133-gh-binding-a01.md
 M .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-a03.md
 M .orchestration/tasks/dotfiles-T133-pre-send-check-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md
 M .orchestration/tasks/dotfiles-T133-regime-ci-token-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-result-precheck-a04.md
 M .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md
 M .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md
 M .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-crit.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-pr-feedback.json
 M .orchestration/validation/dotfiles-T133-pre-send-check-a02-review-receipt.md
?? .orchestration/acceptance/dotfiles-T133-install-ppa-resilience-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a02.md
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
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-a02.md
?? .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-followup-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01-review-a01.md
?? .orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md
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
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-chain-2b58663.log
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-local-review-2b58663.md
?? .orchestration/validation/dotfiles-T128-chain-glue-finish-a02-pr-feedback.json
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-39b60bd.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-bff1eef.md.last.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md
?? .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a08-text-security-cbc39be.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md.last.md
?? .orchestration/validation/dotfiles-T133-gh-binding-a02-text-security-c761dc8.md
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
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-crit.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-local-review-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-review-receipt.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json

**Ensuring complete output and quick graphing**
exec
/bin/zsh -lc "sed -n '225,258p' ~/.agents/skills/agmsg-orchestration/SKILL.md; sed -n '104,124p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md; cat .ua/meta.json; git rev-parse HEAD" in ~/Workspace/dotfiles
 succeeded in 38ms:
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

MCP approvals: enableAllProjectMcpServers=false, enabledMcpjsonServers=[], disabledMcpjsonServers=[]; never exempt definitions. enabledPlugins maps only declared/inventoried identities to false, both sync fields=false, extraKnownMarketplaces={}, disableSkillShellExecution=true.
Settings env has exactly GH_TELEMETRY="false", DO_NOT_TRACK="1", CHECKPOINT_DISABLE="1", AWS_EC2_METADATA_DISABLED="true"; no other AWS exception, credential/provider string or arbitrary value.
Absent/empty objects pass only where their source permits; canonical partial administrative objects may omit declared fields, never add keys/values. Helpers, status-line commands, wrappers, alternate executables and authentication refresh/export keys have no worker form. Orchestrator PermissionRequest is not a worker exception.

## S01-S23, roots and component values

Use user=<validated-home>/.claude-worker, anchor=<validated-home>/Workspace/dotfiles, managed-root=/Library/Application Support/ClaudeCode on Darwin or /etc/claude-code on Linux.
S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 anchor/.claude/settings.local.json; S05 managed-root/managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery.
S08 worktree/.mcp.json; S09 anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json; S12 every skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json.
S16 every default hooks/hooks.json and referenced hook file; S17 each marketplace-root/.claude-plugin/marketplace.json; S18 every default/referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every default/referenced legacy command Markdown file; S22 every subagent Markdown file; S23 every default/referenced plugin LSP file.
Declare independent reads of every matching file, including ignored/untracked, disabled and shadowed inputs; executable environment-file contents join this read set. Unenumerable managed delivery or caller-selected sources require named refusal, without discovery helpers.
Bind anchor to validated passwd home and actual main checkout; worker roots are registered linked worktrees beneath anchor/.claude/worktrees with the same Git common directory. Declare symlink/case-alias handling and containment; foreign roots refuse before side effects for both kinds/routes.
Configuration roots: dedicated user directory, anchor/worktree .claude, applicable nested/additional-directory .claude, platform managed root and registry-contained plugin roots. No account-synced, inline, seed, alternate cache or caller-selected root.
Skills roots exactly Enterprise managed-root/.claude/skills, Personal user/skills, Project project/.claude/skills, Nested subdir/.claude/skills, applicable Additional directory add-dir/.claude/skills, Plugin plugin/skills. Read Markdown and bundled descriptors; managed commands/agents start at actual managed-root.
S08-S10/S18-S19 objects permit only absent/empty mcpServers/managedMcpServers. S14 and S23 permit only {}; S16 only absent/empty hooks; approval/disable state cannot authorize servers or handlers.
S12/S15 fields: name/version/description/author/homepage/repository/license/keywords and hooks/mcpServers/lspServers/commands/agents/skills. Descriptive fields are strings, keywords is a string list; author only string name/email/url. Each explicit component is one scalar contained regular-file reference; no arrays/objects/URLs/inline content/directories; defaults expand independently.
S13 only version=2 and plugins: IDs map to record lists with scope/installPath/version/installedAt/lastUpdated/gitCommitSha/projectPath; scope=user|project|local, descriptive members strings, commit 40 hex, paths contained/project-bound; read every descriptor and disable every ID.
S17 only name/owner/metadata/plugins: string name, owner string name/email, metadata string description/version, plugins absent or []. S20-S22 restricted frontmatter only name/description/argument-hint, Boolean disable-model-invocation/user-invocable, declared allowed-tools/model; no unknown/nested executable forms or dynamic shell expansion, including fenced forms.
S11 must be an object; retained mcpServers only {}; oauthAccount only optional string members accountUuid/emailAddress/organizationUuid/displayName/fullName/organizationRole/workspaceRole; userID only ^[0-9a-f]{64}$. Unknown identity members/wrong types/nonempty or malformed retained MCP refuse unchanged.
Declare discard of every other S11 top-level field and the entire projects value without recursive semantic screening: counters, history, allowedTools, caches and prior onboarding are never forwarded. After complete preflight, atomically regenerate exactly mcpServers={}, projects={}, hasCompletedOnboarding=true plus screened identity; never merge old state. Trust uses existing spawn-readiness acceptance.

{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}
7da0cdfab9de9fbea673b82379acd4e317115065

exec
/bin/zsh -lc 'git diff -- .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md; cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md' in ~/Workspace/dotfiles
 succeeded in 5ms:
diff --git a/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md b/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
index 108c14d2..2f0ffc7a 100644
--- a/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
+++ b/.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md
@@ -3,6 +3,7 @@ format: 2
 task_id: dotfiles-T133-worker-write-boundary-slice1-a01
 kind: code
 security: true
+previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9
 worker: a010
 worker_kind: codex
 worker_profile: security
@@ -185,10 +186,12 @@ Report visible impact: this slice declares/tests worker/admin policy, startup co
 No session loses its stop gate from this slice because the tracked commands do not change. dotfiles-T133-worker-write-boundary-slice5-a01 owns switching .claude/settings.json only after stage A provisions <home>/.claude/hooks/orchestrator-only.sh; this slice neither installs that file nor activates its tracked references.
 No deployment, make update/application, login/keyring change, system installation, restart, permission-policy deployment, live socket/worker probe or live-dependent release. Later slices own screening/output registration, orchestrator activation, update/staging/docs/ignore and deployment reconciliation.
 
+Amendment 1 (`previous_sha256: 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9`): the Codex sandbox denies the Herdr socket, so `agmsg-dispatch` cannot carry this seat's messages (your PONG attempt for PING 2984 exited 1: `PermissionDenied`, `pane not found or unavailable: wJ:p1`). The named route for every PONG and the RESULT of this task is the pane-less path of Orchestrator Playbook step 6, run from sandboxed Bash: write the single line to a file under `.orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/` and send it with `~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-standard-dot-a010 claude-deep-dot --body-file <that file>` (a013 delivered its PONGs this way on 2026-10-21T05:59Z). This route is the named route, not 'another tool' under the boundary-denial sentence above, and the orchestrator reads the bus at each milestone. First reply `AGMSG-PONG v1 task_id=dotfiles-T133-worker-write-boundary-slice1-a01 status=alive` by that route, then start round 1 as written; the unsent `blocked-pong.txt` and `liveness-2998.txt` stay as evidence.
+
 ## Checks
 
 ```text
-prerequisites merged in canonical main 4eafd890454e495fdb1d429734c5835e46c87652 (gh api repos/mryfmo/dotfiles/branches/main): dotfiles-T133-worker-sandbox-exclusions-a02 = PR #448 merge e042663b2d6efd9205f7d388bf881c01d3880642; dotfiles-T133-trusted-entrypoint-pins-a01 = PR #449 merge 4eafd890454e495fdb1d429734c5835e46c87652; the dispatch branch starts fresh from that main, so merge-base = that SHA
+prerequisites merged in canonical main 7da0cdfab9de9fbea673b82379acd4e317115065 (gh api --hostname github.com repos/mryfmo/dotfiles/branches/main --jq .commit.sha, 2026-10-22T00:46Z, exit 0; git merge-base --is-ancestor 4eafd890454e495fdb1d429734c5835e46c87652 7da0cdfa exit 0): dotfiles-T133-worker-sandbox-exclusions-a02 = PR #448 merge e042663b2d6efd9205f7d388bf881c01d3880642; dotfiles-T133-trusted-entrypoint-pins-a01 = PR #449 merge 4eafd890454e495fdb1d429734c5835e46c87652; the dispatch branch starts fresh from that main, so merge-base = that SHA
 post-prerequisite baseline at that main: agent-config.yaml worker 284:    excludedCommands: [] 285:    linux_excluded_commands: []; validate-agent-assets.py line 344 fails any non-empty worker excludedCommands; home/dot_mise/config.toml node = "26.12.0" python = "3.15.0" uv = "0.13.1"
-observed 2026-10-21T09:17Z by the orchestrator (Claude seat, sandboxed Bash); C1-C10/C7b via pre-send.sh on these bytes exit 0 (see the anchor review record); every value is pasted command output
+observed 2026-10-21T09:17Z and re-observed host-bound 2026-10-22T00:46Z (amendment 1) by the orchestrator (Claude seat, sandboxed Bash); C1-C10/C7b via pre-send.sh on these bytes exit 0 (see the anchor review record); every value is pasted command output
 ```
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a02 round=1 reset_of=dotfiles-T133-worker-write-boundary-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md task_sha256=6d36b24e7601d49f34672f755ec15df375bb7a89cc1b78d51e69f79c8c51881c deadline=none done_signal=AGMSG-RESULT note=a010:reset-text(D-024-26-write-boundary-alone;previous_sha256=999ba3c7454a6191f92c407c10653801e02923d253129322894f8f5f8ee0c3b1;start-a-fresh-branch-from-origin/main-and-leave-tools/worker-write-boundary-a01-untouched;C-80-correct-at-ac9ce14-after-4-rounds;the-Checks-block-at-the-end-carries-the-counters;security:true)",
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a02 round=1 reset_of=dotfiles-T133-worker-write-boundary-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md task_sha256=e96dcac923bf2ba8d926e4618895f959be9c4f01ca29424a7f9251fd8eb5491d deadline=none done_signal=AGMSG-RESULT note=a010:amendment-1(previous_sha256=6d36b24e7601d49f34672f755ec15df375bb7a89cc1b78d51e69f79c8c51881c;the-source-cap-amended-once-to-the-measured-1041-from-your-budget-attribution.json;the-test-cap-1609-stands;two-sentences-of-the-Change-budget-and-the-Checks-block-changed,nothing-else);update-the-task-copy-to-this-text-byte-identical-and-push-on-PR-431;then-RESULT-after-the-Bot-window;no-further-cap-change",
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a02 round=1 reset_of=dotfiles-T133-worker-write-boundary-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md task_sha256=eeccf4e20d5753ce49401b3ea5f30834129798857e6a42de6cc66a5a723cb241 deadline=none done_signal=AGMSG-RESULT note=a010:amendment-1b-clerical-alignment(previous_sha256=e96dcac923bf2ba8d926e4618895f959be9c4f01ca29424a7f9251fd8eb5491d;the-Check-cap-sentence-regime-ci.py-reads-now-says-1041-like-the-Change-budget;no-second-cap-increase;my-C-89-miss:the-consumer-sentence-was-not-enumerated);update-the-task-copy-to-this-text-byte-identical,commit,push-on-PR-431,RESULT-after-CI-and-the-Bot-window",
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a02 round=1 reset_of=dotfiles-T133-worker-write-boundary-a01 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md task_sha256=ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50 deadline=none done_signal=AGMSG-RESULT note=a010:amendment-2-measured(previous_sha256=eeccf4e20d5753ce49401b3ea5f30834129798857e6a42de6cc66a5a723cb241;caps-1111/1768-from-your-revise2-budget-attribution.json,mapped-to-the-four-local-review-rows;Change-budget-and-both-Check-sentences-changed-together;nothing-else);update-the-task-copy-to-this-text-byte-identical-in-the-same-last-round,push,RESULT-after-CI-and-the-Bot-window;no-code-change"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 431,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-worker-write-boundary-a02"
}
---

# Acceptance record: dotfiles-T133-worker-write-boundary-a02

Reset of P1-15's a01 (PR #431, branch tools/worker-write-boundary-a01, from ea3c4fb8) after the final-head security review found a P1 (startup validates only the legacy worktree-local hooks; an existing worktree's tracked `.claude/settings.json` or a legacy apiKeyHelper would run unguarded) at the C-61 cap; the a01 record holds the decision. The a02 text (review profile, prompt `p115-a02r-redesign-prompt.md`) adds the startup validation of every executable configuration entrypoint in the tracked, legacy and user settings and the Worker Playbook step 4 consistency; the a01 implementation stays. Seat: a010 (Codex, worker-e), holding. Advisory owner: dotfiles-T133-worker-write-boundary-followup-a01.

- 2026-10-19T19:58Z: text installed (after the host pause 13:03Z to 19:55Z); checker OK; C-80 first review started.
- 2026-10-19T20:00:56Z: C-80 first review of the a02 text (`…-text-security-2ae9e2c.md`): `Verdict: incorrect` on one P1: the startup screening omits the worktree's `.mcp.json` (project MCP servers execute after trust when `enableAllProjectMcpServers` is true). Round 2 by the review-profile context (prompt `p115-a02r2-redesign-prompt.md`): `.mcp.json` screened, auto-approval off in the worker settings, a malicious-server fixture.
text-security:2ae9e2c:1	input-inventory
- 2026-10-19T20:11Z: round-2 text (`p115-a02r2.md`: `.mcp.json` screened before the start, project MCP auto-approval off in the worker settings, a malicious-server fixture) installed; checker OK; C-80 round 2 next.
- 2026-10-19T20:14:37Z: C-80 round 2 of the a02 text (`…-text-security-ebbb71b.md`): `Verdict: incorrect`: P1 project skills-directory plugins (`.claude/skills/<name>/.claude-plugin/plugin.json`) can load bundled hooks after trust; P1 the configuration directory's global state `.claude.json` holds user-scoped and project-local MCP servers; P2 the quoted ledger contract still reads the sha from `origin` (the amended 5.14 item 8 binds it through the repository API). Class table: 2ae9e2c:1 (.mcp.json), ebbb71b:1 (skills plugins), ebbb71b:2 (.claude.json) = three rows of input-inventory: INV-6 S1. Root cause: the text added executable-configuration sources one review at a time instead of enumerating the documented loading list of the installed Claude Code version. Design 5.14 item 1 amended (the inventory is the documented loading list, enumerated once).
text-security:ebbb71b:1	input-inventory
text-security:ebbb71b:2	input-inventory
text-security:ebbb71b:3	repository-binding
re-plan: input-inventory (rows text-security:2ae9e2c:1, text-security:ebbb71b:1, text-security:ebbb71b:2) — specification: the a02 text named the screened sources piecemeal; design: 5.14 item 1 now defines the inventory as the documented loading list of the installed Claude Code version (settings files of every scope, project .mcp.json, the configuration directory global state .claude.json, plugins and skills directories, hook commands, apiKeyHelper, statusLine, MCP server commands), screened or disabled before workspace trust; implementation: the round-3 text enumerates that list from the documentation into premises and screens every entry in one procedure; verification: one fixture per source class (a planted payload in each) asserting refusal before any command runs, and the quotation of item 8 refreshed.
- 2026-10-19T20:3xZ: round-3 text (`p115-a02r3.md`, the whole re-plan: the documented loading list enumerated once, 22 files, 79 threat rows, 1115 lines against proposal 1's 250-line/10-file caps; not split: past its first review and the launcher slice depends on the settings slice, so a split would serialise two PR cycles on the critical path; S1 on the first fix round splits it) installed with `$HOME`-relative paths; checker next; C-80 round 3 (fresh budget after the re-plan line)
- 2026-10-19T20:36:33Z: C-80 round 3 of the a02 text (`…-text-security-b2a186e.md`, the first review after the re-plan line): `Verdict: incorrect`: P1 the inventory K01 screens hook commands only, so a `type: "http"` hook handler (no command field; POSTs tool input and interpolated credentials to its URL after startup) passes unscreened — the fourth input-inventory finding of the lineage and the first after the re-plan: the re-plan enumerated the documented sources once but kept the field-level unit ("hook commands") inside the hooks source; P2 the deferred ledger's two `gh api` calls bind owner/repo but not the host (`GH_HOST` selects the API host), so `--hostname github.com` and a hostile-host test are required. Disposition: design 5.14 item 1 amended (a hook handler of any documented type is an executable input; a worker refuses every handler type but `command`), item 8 amended (`--hostname github.com` on every gh call that decides); amendment 1 after the re-plan via the review profile (`p115-a02r4-redesign-prompt.md`, whole text with the full findings history, never a delta); C-80 budget after the re-plan: 1 of 3 consumed.
text-security:b2a186e:1	input-inventory
text-security:b2a186e:2	repository-binding
- 2026-10-19T20:5xZ: amendment 1 after the re-plan (`p115-a02r4.md`) installed with `$HOME`-relative paths: 1111 lines (r3 1115), 22 files, 81 threat rows (handler-type unit, host binding), `"http"` fixture, `--hostname github.com` ×4, quoted enumerations with fetched_at ×7; checker OK; C-80 round 4 running (budget after the re-plan: 2 of 3 consumed when it returns).
- 2026-10-19T20:55:28Z: C-80 round 4 (`…-text-security-ac9ce14.md`) `Verdict: correct` (handler-type checks cover the documented non-command hook types; 81 residual rows; plugin-loading page re-fetch failed in the review, noted); text dispatched to a010 (worker-e) with the counters pasted: sha256 6d36b24e7601d49f34672f755ec15df375bb7a89cc1b78d51e69f79c8c51881c, previous_sha256 999ba3c7… (the a01 text); TASK line in the JSON dispatch list.
text-security:ac9ce14:0	correct
- 2026-10-19T20:58:20Z: a010 PONG `status=blocked`: my dispatch note said `start a fresh branch from origin/main and leave tools/worker-write-boundary-a01 untouched` while the hashed text (lines 451 and 1052) says continue that branch and PR #431 from ea3c4fb8; a010 performed no write and asked for the binding. 21:04:12Z: PING interpretation (message 2568, read 21:04:20Z): the text binds; the note is withdrawn; recorded as the orchestrator's mistake (a dispatch note carries no instruction the text does not; C-96). 21:06:20Z: a010 PONG `status=working`: branch tools/worker-write-boundary-a01, PR 431, base 51ba5801, head ea3c4fb8, task_copy 6d36b24e…; first startup regression RED on ea3c4fb8 (the unguarded SessionStart returns 0 instead of refusing; a Git signing environment error kept separately, the clean rerun is the valid red); Claude 2.1.300 matches; loader and source enumeration under way; worker_fix_rounds=0.
- 2026-10-19T22:05:34Z: a010 PONG `working`: its single independent pre-push review complete with 2 P1 (S01: `env.HOME` can select a foreign guard; S20/S21: fenced dynamic commands bypass the inline regex); review-1 fix-1 begins with red regressions; 499-test draft green (not the final byte proof); source 1038 lines (over the 961 cap by 77), tests 1552 of 1609 before the review corrections; complete final attribution to follow; no push yet; no second independent review. The cap amendment waits for the final numstat (PING 21:30).
- 2026-10-19T23:13:33Z: a010 PONG `working`: review-1 fix-1 complete (both P1 with valid red/green); 501 required tests green at unchanged bytes; rendered guard shellcheck/shfmt and Python correctness green; source frozen at 1041 (over 961 by 80), tests 1579 of 1609; per-file and per-control attribution in budget-attribution.json; candidate-assets scan running; pre-push gate green; no commit yet; final numstat and RESULT after push, CI and the Bot window; no third review, no binding work.
- 2026-10-19T23:26:52Z: a010 PONG `working`: pushed to PR #431, head 80869efc3df23cd7ced7fd8d89a3ead3ae3de8fc; all 501 required tests green; the single pre-push review's 2 P1 addressed in one round (worker_fix_rounds=1); source 1041 against the 961 cap (overage 80, per-file and per-control attribution saved; no cap edited); tests 1579 of 1609; Bot 15-minute window and CI watch started; candidate-assets scan still running; RESULT to follow. The cap amendment (one, to the measured final numstat) is prepared at the RESULT.
- 2026-10-19T23:36:17Z: a010 PONG `blocked` (boundary: reviewed source budget): all 501 tests and the exact candidate-assets scan green at the committed bytes; CI 10 pass 1 fail: the regime job's only exit-1 cause is `1041 source lines exceed 961` (log read through the fixed-host API, saved as raw/regime-job-original.txt); per-file and per-control attribution final (budget-attribution.json); no local cap edit or suppression; asks for the reviewed, measured budget amendment with previous_sha256; the Bot window still running; the RESULT follows the window. The orchestrator amends the Change budget once to the measured figures now (amendment 1 of the a02 text).
- 2026-10-19T23:40:53Z: amendment 1 of the a02 text: the source cap amended once to the measured 1041 (per-file numstat at 80869efc; the 240-line screening estimate measured 361 in the worker settings policy; the launcher shrank 26), the test cap 1609 unchanged; two sentences and the Checks block changed; sha256 6d36b24e7601 -> e96dcac923bf; the C-80 verdict ac9ce14 covers the unchanged body; checker re-run; TASK line (amendment 1) sent to a010.
- 2026-10-19T23:47:45Z: a010 PONG `blocked`: amendment 1 changed the Change budget to 1041 but the `## Check` sentence regime-ci.py reads (`caps()` at regime-ci.py:77-99, first match in the Check section) still said 961; a010 did not commit the e96d copy (proof raw/amendment-check-cap-conflict.log). My C-89 miss (the consumer of the cap was not enumerated at the amendment). Amendment 1b at 2026-10-19T23:57:25Z: the Check sentence aligned to 1041, no new authorisation; sha256 e96dcac923bf -> eeccf4e20d57; re-dispatched.
- 2026-10-20T00:01:29Z: a010 PONG `working`: amendment 1b verified byte-for-byte (text sha256 eeccf4e2…); the exact copy committed and pushed, head aded8e4b1dcc0e15971e7af11a2086ef0cd1126e on PR #431; the regime cap function green on the actual 1041 source / 1579 test lines; code unchanged since 80869efc; RESULT after CI and the Bot window.
- 2026-10-20T00:24:59Z: a010 RESULT `status=ready_for_review`: PR #431 head aded8e4b1dcc0e15971e7af11a2086ef0cd1126e, task_copy eeccf4e2… (= amendment 1b), source 1041/1041, tests 1579/1609, worker_fix_rounds 1, independent review rounds 1, Bot none in the final 901 s window; all 501 required tests plus 59 amended-docs tests green; 21 source digests bound to HEAD; feedback 8 items proposed (1 fixed, 7 not-applicable; the orchestrator dispositions); operator-steps.md lists the deployment steps (make update; make install-managed-settings + the printed sudo install; login with CLAUDE_CONFIG_DIR=~/.claude-worker; the separate Codex permgate escape-denial change; restarts). Measured by the orchestrator 2026-10-20T00:26:27Z: 11 checks pass including regime and the ubuntu-26.04 canary, merge state CLEAN, 2 Codex Bot review comments. ACCEPTANCE pending-integration sent; chain after #417's, then security-review.sh, audit, gate, merge; deployment waits the a05 coupling (D-024-31).


## Owned by dotfiles-T133-worker-write-boundary-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:79ea98a:3	advisory-p2
local-finding: 79ea98a:3 not-applicable:advisory P2 owned by dotfiles-T133-worker-write-boundary-followup-a01 (- [P2] Migrate the legacy PreToolUse handler when adding the guard — home/.chezmoitemplates/claude-settings-managed.json); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md (69aae3928ab04247cb888bab165f9e14d09bcf03680d23a26c11a4cb1bf66e0a)
local:79ea98a:4	advisory-p2
local-finding: 79ea98a:4 not-applicable:advisory P2 owned by dotfiles-T133-worker-write-boundary-followup-a01 (- [P2] Screen existing main-local hooks before replacing them — home/dot_claude-worker/modify_private_settings.json:391-); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md (69aae3928ab04247cb888bab165f9e14d09bcf03680d23a26c11a4cb1bf66e0a)
- 2026-10-20T01:15:34Z: the chain on #431: base moved (ba318e53), update-branched to 79ea98a3; sandbox-scan clean; local review (`…-local-review-79ea98a.md`, codex review --base main) 4 findings: P1 herdr-agents:486-488 the new launch-option allowlist rejects the manifest-generated `--advisor fable` (default Claude worker seating fails); P1 the attachment hook under the clean prefix calls `herdr` by bare name with PATH=/usr/bin:/bin and HERDR_AGENTS_LAYOUT dropped (127: no attachment, no seat claim); P2 bootstrap replaces the whole hooks object (local PermissionRequest/Stop handlers deleted); P2 merge_hooks appends the guarded PreToolUse beside the legacy enforce-uv.sh. The chain refused (rc 11: a P0/P1 local finding). Revise round 1 (the second and last worker round under C-61) sent 2026-10-20T01:19:32Z with four selectors; design 5.14 item 2 stands (fixed PATH; absolute paths anchored to the passwd home for herdr and every mise-installed tool; the allowed environment names include what the attachment needs).
local:79ea98a:1	tool-environment
local:79ea98a:2	tool-environment
local:79ea98a:3	partial-fix
local:79ea98a:4	partial-fix
- 2026-10-20T01:23:40Z: a010 PONG `blocked` at the revise preflight: `git merge --ff-only 79ea98a3` exits 128 (`You have not concluded your cherry-pick (CHERRY_PICK_HEAD exists)`); evidence revise-blocked.md. Measured by the orchestrator: .git/worktrees/worker-e/CHERRY_PICK_HEAD dated 2026-10-19 20:37 JST names 7c3a6394 (`feat(agents): bind isolated Claude permission hooks`, an a01-era cherry-pick of this lineage by the same seat) with AUTO_MERGE beside it: the seat's own leftover. PING 2026-10-20T01:26:58Z: authorised `git cherry-pick --quit` (clears the sequencer state, touches neither tree nor index), record it in sandbox.md, confirm a clean status at aded8e4b, then the fast-forward and the round.
- 2026-10-20T01:28:26Z: a010 PONG `blocked`: `git cherry-pick --quit` exited 0 but could not write the shared `.git/packed-refs.lock` (Operation not permitted x3, the Codex sandbox) and CHERRY_PICK_HEAD remained; evidence raw/revise2-quit.json, revise2-clean.json, revise2-ff.json. Orchestrator action 2026-10-20T01:29:11Z (worktree hygiene; the metadata lives in the shared .git under the main checkout): `git -C .claude/worktrees/worker-e cherry-pick --quit` exit 0; CHERRY_PICK_HEAD and AUTO_MERGE gone; HEAD aded8e4b and the tracked tree untouched. PING 2026-10-20T01:29:45Z: proceed with the fast-forward and the round. Mechanism note: a Codex seat cannot clear its own sequencer state because the worktree's git metadata lives outside its writable roots; the P1-15 text's private worker caches do not cover `.git/worktrees/<seat>/`.
- 2026-10-20T01:57:11Z: a010 PONG `working` (last round, final validation): all four selectors red at 79ea98a3 and green on the revised source; no control dropped; fixed PATH kept, Herdr/jq/Node/npm/Codex called by passwd-home-anchored installed paths; measured source 1111 (cap 1041, +70: herdr-agents +36, orchestrator settings +21, worker settings policy +13) and tests 1768 (cap 1609, +159), attribution revise2-budget-attribution.json. Amendment 2 at 2026-10-20T01:58:30Z (measured; each amendment maps to accepted review findings, rows local:79ea98a:1-4): caps 1111/1768 in the Change budget and both Check sentences (C-99); sha256 eeccf4e20d57 -> ae1088a7fdef; dispatched for the copy update inside the same last round.
- 2026-10-20T02:18:32Z: a010 PONG `question` (last round, task copy ae1088a7… = amendment 2): final modules 348 run, 347 pass, 1 fail: tests/unit/test_herdr_agents.py:5906-5909 (`test_repeated_worker_start_replaces_stale_managed_hooks`) writes the current project's main-local settings but binds the legacy check-inbox argv to HOME/Workspace/dotfiles instead of the settings' project; the round's new P2 screen correctly refuses the foreign-project binding; the old bootstrap overwrite had concealed the fixture mismatch. Proposal: a one-line fixture change (local-project branch uses self.workdir.resolve()), no production change. Answer 2026-10-20T02:19:24Z: yes, inside this directed last round (the round's own screen exposed it; a red test cannot ship); rerun 348 + the four selectors; record in revise.yaml.
- 2026-10-20T02:36:11Z: a010 PONG `working`: head edd824ea pushed on PR #431 (task copy ae1088a7 = amendment 2); the authorised one-line fixture alignment recorded in revise.yaml; full 348 + 157 release modules all 505 green; the four selectors red at 79ea98a3 and green; worker_fix_rounds 2 (the last); RESULT after CI and the Bot window.
- 2026-10-20T02:53:43Z: a010 RESULT round 2 (final) `status=ready_for_review`: head edd824ea2d5b3a4b22da3d4263f96ead53fab49e (previous 79ea98a3), base ba318e53, task_copy ae1088a7 (= amendment 2), 22 changed files (7 in this round), source 1111/1111, tests 1768/1768, 505 local tests, CI 11 pass, Bot none after 901 s, feedback 8 items proposed (1 fixed, 7 n/a), open P0/P1 none, worker_fix_rounds 2, one independent pre-push review; operator steps in operator-steps.md (sudo managed-settings install, worker login, make update after a05, restarts); deployment not performed. ACCEPTANCE pending-integration sent 2026-10-20T02:55:36Z; chain on edd824ea running; then security-review.sh, audit, gate, merge.

local:c0f50fa:3	advisory-p2
local-finding: c0f50fa:3 not-applicable:advisory P2 owned by dotfiles-T133-worker-write-boundary-followup-a01 (- [P2] Include parent-directory creation in the installation command — Makefile:213-213); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md (69aae3928ab04247cb888bab165f9e14d09bcf03680d23a26c11a4cb1bf66e0a)
local:c0f50fa:4	advisory-p2
local-finding: c0f50fa:4 not-applicable:advisory P2 owned by dotfiles-T133-worker-write-boundary-followup-a01 (- [P2] Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-followup-a01.md (69aae3928ab04247cb888bab165f9e14d09bcf03680d23a26c11a4cb1bf66e0a)
- 2026-10-20T03:14:31Z: security-profile review of the chain's update-branch head c0f50fa1 (`…-security-c0f50fa.md`) `Verdict: incorrect`: P1 the startup inventory accepts the AWS credential-chain selectors (CLAUDE_CODE_USE_BEDROCK, AWS_CONFIG_FILE, AWS_SHARED_CREDENTIALS_FILE, AWS_PROFILE), so settings can select a worker-controlled `credential_process` that executes through authentication, outside the Bash sandbox (K02 defeated); P1 S04 screens the fixed dotfiles anchor's local settings although `herdr-agents --add-worker … <DIR>` accepts other repositories, so a hook in `<DIR>/.claude/settings.local.json` stays executable (pass the validated main root into screening or refuse other roots); P2 object-form plugin command mappings (`{"source": …}`, inline `content`) pass recursive screening without Markdown inspection. The review's masker step failed (`ModuleNotFoundError: tomllib`: the unsandboxed uv resolved Python 3.10; the glue now binds the mise interpreter) and the review file is unmasked (the boundary masks it). Rows input-inventory (the family's 4th, 5th and 6th finding after the re-plan of 20:3xZ). C-61: both worker rounds are spent, so the lineage resets to a03 (the operator's standing order: no third round on a mechanism PR) once the running chain's audit of c0f50fa1 returns, with its findings folded in; the re-plan changes the approach from "screen the documented list of executable keys" to "allowlist the settings, sources and roots a worker start accepts and refuse everything else" (design 5.14 item 1's "refusing any payload it did not write", generalised; recorded in the residual list, D-024-29). #435 merges now (D-024-33: the P1-15 chain no longer needs its base).
security:c0f50fa:1	input-inventory
security:c0f50fa:2	input-inventory
security:c0f50fa:3	input-inventory
- 2026-10-20T03:17Z: the chain on the update-branch head c0f50fa1 (base 118daafa): local review 4 findings (the review file lists each twice; rows 1-4: P1 Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243; P1 Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206; P2 Include parent-directory creation in the installation command — Makefile:213-213; P2 Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633; P1 Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206; P1 Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243; P2 Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633; P2 Include parent-directory creation in the installation command — Makefile:213-213; P1 Reject project settings that widen the worker sandbox — home/dot_claude-worker/modify_private_settings.json:205-206; P1 Inventory the actual managed skill directory — home/dot_claude-worker/modify_private_settings.json:241-243; P2 Reconcile Claude settings after Herdr installs its hook — scripts/generate-agent-configs.py:629-633; P2 Include parent-directory creation in the installation command — Makefile:213-213); the chain refused (rc 11) before the audit. With the security review's two P1 and no worker round left, a02 is withdrawn and the lineage resets to a03 (continue PR #431 from c0f50fa1; the allowlist re-plan; design by reference to shorten the text); the a03 text is being authored by the review profile. #435 merged at 03:18:08Z (main 60a6fb2b) per D-024-33; the main checkout fast-forwarded.
local:c0f50fa:1	tool-environment
local:c0f50fa:2	tool-environment
local:c0f50fa:3	partial-fix
local:c0f50fa:4	partial-fix

---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a03 round=1 reset_of=dotfiles-T133-worker-write-boundary-a02 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md task_sha256=5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669 deadline=none done_signal=AGMSG-RESULT note=a010:reset-a03(reset_of=a02,withdrawn-at-edd824ea-by-the-security-review-of-c0f50fa1;the-text-continues-PR-431-on-tools/worker-write-boundary-a01-from-c0f50fa1;allowlist-re-plan;design-5.14-by-reference;C-80:f7af699-incorrect->amendment-1(CLAUDE_ENV_FILE-contents),9bd6198-correct;pre-send-on-these-bytes:task-consistency-check-OK,C11-6/6,SECRET_PATTERN-0,home-paths-0,624-lines;counters-and-history-in-the-Checks-block)",
    "AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a03 round=1 reset_of=dotfiles-T133-worker-write-boundary-a02 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md task_sha256=49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b deadline=none done_signal=AGMSG-RESULT note=a010:amendments-2-4(previous_sha256=5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669;answers-your-blocked-PONG-2694:D-024-34-the-global-state-file-is-launcher-generated-at-every-start,D-024-35-with-no-per-project-inventory(projects-regenerated-empty,trust-via-the-launcher's-dialog-acceptance),the-enterprise-skills-root-is-<managed-root>/.claude/skills;C-80:49161bc-correct;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0;update-the-task-copy-byte-identical-and-start-the-implementation-per-the-text)"
  ],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "input-inventory",
      "id": "audit:f7af699:1"
    },
    {
      "class": "input-inventory",
      "id": "audit:5067ed0:1"
    },
    {
      "class": "input-inventory",
      "id": "audit:efa211d:1"
    },
    {
      "class": "input-inventory",
      "id": "audit:be969e3:1"
    }
  ],
  "pr": null,
  "replans": {
    "input-inventory": {
      "design": "an inventory the family has now failed to complete six times is removed, not extended (the refusal for a non-empty top-level `mcpServers` stays as tamper evidence)",
      "implementation": "amendment 3 written whole by the review profile (`p115-a03-r4-prompt.md`) with an A-then-B sequential-start fixture on the shared directory, red on c0f50fa1 and green after",
      "specification": "the generated global state file declares no per-project inventory at all: `projects` is regenerated empty and the anchor's workspace trust comes from the launcher's existing trust-dialog acceptance (D-024-35)",
      "verification": "C-80 round 4 (the first round after this line)."
    }
  },
  "searches": [],
  "task": "dotfiles-T133-worker-write-boundary-a03"
}
---

# Acceptance record: dotfiles-T133-worker-write-boundary-a03

Plan 024 P1-15 reset a03 (reset_of a02; PR #431 continued from c0f50fa1; seat a010). Re-plan: allowlist (accept only the declared keys, environment names, sources, roots and value forms; refuse everything else), after the sixth input-inventory finding (security review c0f50fa1: AWS credential-chain selectors, other-repository roots, object-form plugin commands) and the local review of c0f50fa1 (2 P1 + 2 P2). Design 5.14 by reference (D-024-30): 609 lines (a02: 1112), 22 files, 85 threat rows; checker OK after install.

- 2026-10-20T03:31:52Z: text authored by the review profile (`p115-a03-redesign-prompt.md` -> `redesign/p115-a03.md`), installed with `$HOME`-relative paths; C-80 round 1 running.
- 2026-10-20T03:34Z: C-80 round 1 (`…-text-security-f7af699.md`) `Verdict: incorrect`, one P1: `CLAUDE_ENV_FILE` selects shell code executed before each Bash command; the allowlist binds only its pathname, not its contents, so pre-existing contents can execute commands or restore refused variables; require empty or launcher-generated trusted contents before forwarding, with a planted-content regression. Amendment 1 via the review profile at 2026-10-20T03:35:17Z (budget 1 of 3).
text-security:f7af699:1	input-inventory
- 2026-10-20T03:43:14Z: amendment 1 written whole by the review profile (`p115-a03-r2-prompt.md` -> `redesign/p115-a03-r2.md`) and installed: `CLAUDE_ENV_FILE` named as the only admitted variable selecting a file whose contents execute (read-only probe of the documented environment variables); preflight accepts its file only when absent, empty or byte-identical to the launcher-generated contents of this start, inspected without sourcing; one closed row with the selector `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` and one planted-content regression (red on c0f50fa1, green after). 35 changed lines against round 1; 622 lines; pre-send.sh: checker OK, SECRET_PATTERN 0 matches, no literal home path; sha256 f7af699… -> 9bd6198f1abec37ac618757c140b21fa799b987dbf4317c6a66ac16a9cefde24. C-80 round 2 running (budget 2 of 3).
- 2026-10-20T03:48:43Z: C-80 round 2 (`…-text-security-9bd6198.md`) `Verdict: correct` (budget 2 of 3 used; the CLAUDE_ENV_FILE P1 closed by amendment 1).
text-security:9bd6198:0	correct
- 2026-10-20T04:00Z: Checks block pasted (checker OK; C11 6/6 selectors; SECRET_PATTERN 0; home paths 0; C-80 history; counters tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0); final 624 lines, sha256 5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669; AGMSG-TASK round 1 dispatched to a010 (worker-e, wJ:p5) via dispatch.sh (`p115-a03-dispatch.txt`); read_at filled by fill-dispatch.py.
- 2026-10-20T04:00:43Z: a010 PONG `blocked` (message 2694) at preparation, before any edit: its read-only probe of the installed loader (Claude Code 2.1.300, loader sha256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3; `raw/loader-state-probe.json`) shows the loader itself persists `numStartups` at every start and `hasCompletedOnboarding` at onboarding into the global state file, while S11 admits only `mcpServers` and `projects`; the exact schema would refuse the worker's own native state at the next ordinary start. The text's rule (block and retask, never widen silently) was followed. Disposition: owner amendment 2 (D-024-34): the global state file becomes launcher-generated at every start (declared shape plus screened identity fields), refusing only declared-structure violations; see the re-plan line below.
worker:5067ed0:1	input-inventory
re-plan: input-inventory (rows text-security:2ae9e2c:1, text-security:ebbb71b:1-2, text-security:b2a186e:1, security:c0f50fa:1-3 of the a02 lineage; the a03 reset) — specification: a worker start accepts only the settings keys, environment names, configuration sources, roots and value forms the manifest and the renderer declare, and refuses the start with a named message for anything else (allowlist, not a screened list of executable keys); design: 5.14 item 1 generalised to every input (the residual-list entry of 2026-10-20; design frozen, D-024-29, applied by reference, D-024-30); implementation: the a03 reset text (allowlist schema, one fixture per allowlist class, the three c0f50fa1 findings as regressions); verification: C-80 rounds f7af699 (incorrect, 1 P1) and 9bd6198 (correct).
re-plan: input-inventory (rows text-security:f7af699:1, worker:5067ed0:1, after the allowlist re-plan) — specification: every file the worker's loader consumes at start that the regime need not preserve is launcher-generated at each start, so pre-existing contents never reach the loader; design: D-024-34 (the global state file written from the declared shape plus screened identity fields; refusal only for declared-structure violations; `CLAUDE_ENV_FILE` in the same family); implementation: amendment 2 written whole by the review profile (`p115-a03-r3-prompt.md`), fixtures red on c0f50fa1 and green after (regenerated state, planted `mcpServers`, non-string `oauthAccount` member); verification: C-80 round 3 (the last of the budget; a further round needs a new re-plan line, C-92).
- 2026-10-20T04:23Z: amendment 2 written whole by the review profile (`p115-a03-r3-prompt.md` -> `redesign/p115-a03-r3.md`, D-024-34) and installed: the global state file is launcher-generated at every start (declared shape plus screened identity fields; refusal only for declared-structure violations), the S11 row closed with the selector `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_global_state_with_screened_identity`, a premise carrying the orchestrator's loader probe (sha256 475517ca…, 2.1.300, grep counts 12/15 unquoted, 1/0 quoted), three fixtures red on c0f50fa1; 57 changed lines against the dispatched text; 649 lines; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 5067ed07… -> efa211d1fa4e8fc90512fc88acf6e8cad1127d10a74defafe5adab2e2817faf5. C-80 round 3 running (the last of the budget; C-92).
- 2026-10-20T04:29Z: C-80 round 3 (`…-text-security-efa211d.md`) `Verdict: incorrect`, one P2 (line 431): all Claude workers share `.claude-worker/.claude.json`, but S11 accepts only the anchor's and the current worktree's project keys, so after worker A generates valid state, worker B's start rejects A's key even sequentially; the same-worktree restart fixture misses it. Budget 3 of 3 used; a 4th round needs a new re-plan line (C-92).
text-security:efa211d:1	input-inventory
re-plan: input-inventory (row text-security:efa211d:1, after the launcher-generated-files re-plan) — specification: the generated global state file declares no per-project inventory at all: `projects` is regenerated empty and the anchor's workspace trust comes from the launcher's existing trust-dialog acceptance (D-024-35); design: an inventory the family has now failed to complete six times is removed, not extended (the refusal for a non-empty top-level `mcpServers` stays as tamper evidence); implementation: amendment 3 written whole by the review profile (`p115-a03-r4-prompt.md`) with an A-then-B sequential-start fixture on the shared directory, red on c0f50fa1 and green after; verification: C-80 round 4 (the first round after this line).
- 2026-10-20T04:41Z: amendment 3 written whole by the review profile (`p115-a03-r4-prompt.md` -> `redesign/p115-a03-r4.md`, D-024-35) and installed: the generated state file carries no per-project inventory (`projects: {}` regenerated; trust via the launcher's existing dialog acceptance), rows for the project-key inventory removed, an A-then-B sequential-start fixture on the shared directory; 39 changed lines against amendment 2; 650 lines; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 efa211d1… -> be969e32246c9a1a55e61654d28be9111328fde0e7730a300465bb2e43b0c47e. C-80 round 4 running (the first round after re-plan 3).
- 2026-10-20T04:49Z: C-80 round 4 (`…-text-security-be969e3.md`, the first after re-plan 3) `Verdict: incorrect`, one P1 (line 425): the design screens `<managed-root>/skills` and excludes `<managed-root>/.claude/skills`, which the pinned loader 2.1.300 consumes (documented loading locations), so managed skill content escapes preflight and fixture 502 tests the wrong directory. Disposition: amendment 4 after the orchestrator's read-only probe of the loader's skill-directory strings (pasted in the prompt); maps to the row below. Rounds after re-plan 3: 1 of 3 (C-92).
text-security:be969e3:1	input-inventory
- 2026-10-20T04:58Z: amendment 4 written whole by the review profile (`p115-a03-r5-prompt.md` -> `redesign/p115-a03-r5.md`) and installed: the enterprise skills root is `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), the admitted skills roots are the documented six, fixture 502 plants Markdown and bundled plugin payloads there through the temporary managed-root fixture, the row's premise quotes the documented table and the loader probe (C-87); 22 changed lines against amendment 3; 654 lines; pre-send.sh: checker OK, SECRET_PATTERN 0, home paths 0; sha256 be969e32… -> 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b. C-80 round 5 running (the second after re-plan 3).
- 2026-10-20T05:02Z: C-80 round 5 (`…-text-security-49161bc.md`) `Verdict: correct` (rounds after re-plan 3: 2 of 3). Checks block re-pasted (amendment history, C-80 history, counters); final sha256 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b; AGMSG-TASK (amendments 2-4, previous_sha256 5067ed07cf353371…) dispatched to a010 (worker-e, wJ:p5) via dispatch.sh (`p115-a03-amend-dispatch.txt`); read_at filled by fill-dispatch.py. The text at this sha joins the records PR so regime-ci verifies the a03 copy against main.
text-security:49161bc:0	correct
- 2026-10-20T05:03Z: correction to the previous line: the Checks re-paste did not happen (the paste script asserted on the block's shape: the amendment-4 text carries prose between the heading and the fence) and the shell continued despite `set -e`, so TASK 2740 (read by a010 at 05:02:26Z) carries sha256 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b, exactly the bytes C-80 round 5 reviewed (`Verdict: correct`); the Checks block inside them is the review's reproduction of the send-1 paste, and the amendment summary travelled in the TASK note. No resend: the dispatched bytes are the reviewed bytes. Mechanism (M-20261020-03 amended): orchestrator edit-and-dispatch commands verify each step positively (`grep -q` of the pasted marker, `|| exit 1` on every step) instead of relying on `set -e`, which this harness shell did not honour for the failed `uv run` step.
- 2026-10-20T05:08:10Z: a010 PONG `working` (2744): amendments 2-4 verified; the new state-provider, root-component, env-file and schema regressions are red at c0f50fa1; the managed-skills selector (amendment 4) is already green in all four Darwin/Linux Markdown/plugin cases because c0 already inventories `<managed-root>/.claude/skills` (the review's P1 was a text-inventory error, not an implementation gap); a010 asks to disposition that required red as retained baseline coverage. Disposition (2026-10-20T06:01Z, PING `p115-a03-2744-disposition.txt`): accepted; no artificial failing fixture; the selector stays as the row's test, report.md states the finding's nature with the four cases pasted; red-then-green applies to the rows whose control is new.
- 2026-10-21T01:50Z: R1-1 (re-plan v2, J2 default): the a04 reset text (653 lines, undispatched, C-80 round 1 P2) is withdrawn as a single text and replaced by four slices `dotfiles-T133-worker-write-boundary-slice{1,2,3,4}-a01` per the review-profile allocation draft `.agents/worklog/orchestrator-glue/a04-allocation-r1.md` (22 paths, 90 threat rows and the retained findings assigned; table saved as `.orchestration/plans/024-allocation.tsv`). Decisions taken by default: slice ids S1-S4 with serial shared-file scopes; slice 1 is the sole reset_of a03 carrier (allowed_files 8, after []); provisional caps 650 source / 650 tests for slice 1, reconciled against a04's 1591/2528 at RESULT, no silent increase; owner `dotfiles-T133-trusted-entrypoint-descendants-followup-a01` created now (J1) and named by the slices for guard/delivery/formatter/map binding; four slice namespaces, predecessor evidence retained unchanged, no purported dispatched a04 copy; the foreign-root refusal identifier uses slice 2's dispatched id; dependency edges: network -> S1, launcher consumers -> S2, settings prerequisites -> S3, audit/verdict documentation -> S4 (independent pins/resolver/a05 edges kept). Slice 1 text authoring starts through author-loop.sh (brief `brief-wwb-slice1.md`, C-80 <= 2).
- 2026-10-21T02:43Z: slice 1 text (author-loop, 190 lines, 8 paths) took three C-80 rounds: rounds 1-2 one P2 on absent owner files (slice2/slice4/agmsg-hardening stubs created, bytes unchanged, review re-run), round 3 a new P2 (`…-text-security-f4246e9.md`): switching the tracked hooks in `.claude/settings.json` to a guard that stage A has not yet installed removes the stop gate from sessions loading the tracked settings. S-R5: no fourth round on this design; re-slice: `.claude/settings.json` and the tracked-hook switch move to a new slice 5 (`dotfiles-T133-worker-write-boundary-slice5-a01`, after slice 4 and deployment stage A), slice 1 keeps 7 paths and renders the guard template only. Brief v2 (`brief-wwb-slice1-v2.md`); author-loop restarts for the re-sliced design (the round count is per design, S-R5).


**Checking budget and task scope**
codex
この slice は実行時の隔離を完成させるものではなく、宣言・レンダー・固定ルーティングの土台として記述されています。保留されたリスクを区別したうえで、参照先の所有タスクと過去の指摘を照合し、残余リスクとされた制御が実際に何を軽減するかを確認しています。
exec
/bin/zsh -lc "jq -r '.nodes[] | select((.filePath // \"\") | test(\"generate-agent-configs|herdr-agents|modify_private_settings\")) | [.filePath,.summary] | @tsv' .ua/knowledge-graph.json | head -20; git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- home scripts; rg --files --hidden .orchestration/validation .orchestration/dotfiles-T133-worker-write-boundary-a03 .orchestration/acceptance | rg '(c0f50fa|worker-write-boundary-slice1|worker-write-boundary-a03)'" in ~/Workspace/dotfiles
 succeeded in 99ms:
home/dot_claude/modify_private_settings.json	chezmoi modify_ script (Python despite the .json name) that merges the rendered managed Claude settings baseline with Claude-owned runtime state in ~/.claude/settings.json, replacing managed permission and SessionStart hooks in place and appending the herdr-agents --attach hook.
home/dot_claude/modify_private_settings.json	Parses stdin text into a dict, returning None for blank, invalid, or non-object JSON so apply falls back to the baseline.
home/dot_claude/modify_private_settings.json	Predicate identifying managed permission hooks whose command is exactly ccgate/permgate followed by 'claude'.
home/dot_claude/modify_private_settings.json	Predicate identifying SessionStart hooks that invoke herdr-agent-state.sh or herdr-agents regardless of rendered home path.
home/dot_claude/modify_private_settings.json	Replaces managed hook entries in place to preserve ordering, keeps unmanaged hooks of mixed entries, and appends remaining managed entries.
home/dot_claude/modify_private_settings.json	Merges per-event hook maps, using managed-entry replacement for predicate-tracked events and additive dedup for other lists.
home/dot_claude/modify_private_settings.json	Top-level settings merge keeping runtime keys (enabledPlugins) from current state, taking managed values otherwise, and delegating hooks to merge_hooks.
home/dot_claude/modify_private_settings.json	Renders the managed baseline template, appends the herdr-agents attach SessionStart hook, merges with stdin state, and writes the result (unchanged text when equal).
home/dot_local/bin/common/executable_herdr-agents	Large Bash launcher that builds, attaches, repairs, and restarts the Claude Code orchestrator and Codex/Claude worker panes in Herdr, seats worker worktrees and agmsg identities, claims the orchestrator seat, runs the visible read-only audit tab with secret masking and verdict gating, and installs the pre-push main-push guard.
home/dot_local/bin/common/executable_herdr-agents	Prints the herdr-agents usage text covering full, attach, restart-worker, audit, add/remove-worker, and bootstrap modes.
home/dot_local/bin/common/executable_herdr-agents	Resolves the worker model profile from the environment, deprecated alias, or manifest-generated model-profiles.env, defaulting to standard.
home/dot_local/bin/common/executable_herdr-agents	Resolves the worker kind (codex or claude) from the environment or model-profiles.env, defaulting to codex.
home/dot_local/bin/common/executable_herdr-agents	Reads and validates the manifest worker worktree path, requiring a single segment under .claude/worktrees/.
home/dot_local/bin/common/executable_herdr-agents	Prints the absolute worker worktree, creating it detached at origin/main when missing and refusing paths that are not worktrees of the repository.
home/dot_local/bin/common/executable_herdr-agents	Finds or registers the agmsg worker identity seated at a worktree, deriving team and suffix from the orchestrator identity and joining with AGMSG_RESOLVE_PROJECT=0.
home/dot_local/bin/common/executable_herdr-agents	Points agmsg delivery hooks at the worker worktree when missing, using turn delivery for codex and both for claude-code.
home/dot_local/bin/common/executable_herdr-agents	Builds the Codex -c writable_roots override granting a linked worktree's git objects, refs, logs, and worktree metadata while keeping config and hooks read-only.
home/dot_local/bin/common/executable_herdr-agents	Prints the agmsg spawn options YAML carrying the worker profile launch arguments and Codex worktree writable roots.
home/dot_local/bin/common/executable_herdr-agents	Despawns a worker seat graceful-first, retrying with --force when the seat needs it.
home/dot_local/bin/common/executable_herdr-agents	Prints the absolute path of an existing worktree of the repository or exits 2.
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
rg: .orchestration/dotfiles-T133-worker-write-boundary-a03: No such file or directory (os error 2)
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03-design-reset.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0f87501.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-3844d93.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0e9bf3f.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0b96f40.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-401573e.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0e9bf3f.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0b96f40.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-3844d93.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a02-chain-c0f50fa.log
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-4e8b427.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-0f87501.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-9bd6198.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md.last.md

exec
/bin/zsh -lc 'cat .agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md .agents/worklog/orchestrator-glue/a04-allocation-r1.md' in ~/Workspace/dotfiles
 succeeded in 3ms:
# Notes every review-profile brief carries (orchestrator glue, 2026-10-20)

1. Host facts measured before authoring, pasted verbatim: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`. A text names a resolve command and asks the worker to paste its output, never a guessed path (re-plan validation-setup of regime-ci-token-a01).
2. Every evidence item names its producer and seat kind: `orchestrator (Claude seat, sandboxed Bash)` or `worker (<kind> seat)`. A Codex seat cannot probe the herdr socket from its sandbox (PermissionDenied measured 2026-10-20T13:39Z, a013); never ask it to (M-20261020-06/08 class).
3. The self cap leaves room for the orchestrator's Checks block (about 7 lines) when the text keeps a fenced block under `## Checks`; a reset text anchored by a review is dispatched at the anchored bytes with no paste.
4. No restatement of the trusted-execution contract: design 5.14 items by reference; environment and executable rows the tool cannot close are `residual` with an owner (re-plan contract-restatement of regime-ci-token-a01). Texts for security: false tools get no C-80 (D-024-46).
5. Caps in the C-107 sentence form; the numstat command in its own sentence; measurement base pasted at dispatch (the branch head at dispatch for a records-only round after an update-branch, not an older code head).
6. Baseline statements bind to the post-prerequisite state: a text that names `after:` prerequisites describes main as it will be after they merge (their post-merge effects stated in the brief), never as it is on the authoring day (slice 1 of P1-15, 2026-10-21: an old Linux exclusion policy was preserved against a prerequisite that empties it).

1. `024-allocation.tsv`

```tsv
item	kind	slice	reason	intermediate_condition
home/dot_agents/agent-config.yaml	path	1	Declare closed startup policy and static inventory; orchestrator activation revisits this path in slice 3	E1; preserve existing orchestrator output until E3
home/.chezmoitemplates/claude-settings-managed.json	path	3	Activate guarded orchestrator hooks and symmetric exclusions together with validator changes	E3
home/.chezmoitemplates/claude-worker-settings.json	path	2	Register and commit worker output with its preparation consumer	E2
home/.chezmoitemplates/claude-managed-settings.json	path	2	Register administrative output; privileged staging remains slice 4	E2; no installation claim
home/dot_claude/modify_private_settings.json	path	1	Add exact legacy/canonical classification and preserve custom hooks before new forms become effective	E1; activate new baseline in E3
home/dot_claude-worker/modify_private_settings.json	path	2	Own common source screening, prepared-result validation, migration and regeneration	E2
home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl	path	1	Install fixed-operation guard before tracked settings reference it	E1
.claude/settings.json	path	1	Guard all tracked events atomically with guard creation	E1
scripts/generate-agent-configs.py	path	1	Own schema/render functions and guard output; output registration and orchestrator activation recur in slices 2/3	E1/E2/E3; every registered output committed
scripts/validate-agent-assets.py	path	3	Change exact exclusion policy with the orchestrator output it validates	E3
Makefile	path	4	Own nonprivileged staging, printed parent creation and post-Herdr reconciliation	E4
home/dot_local/bin/common/executable_herdr-agents	path	2	Own route screening, anchor refusal, launch environment and interpreter consumption	E2
home/dot_agents/skills/agmsg-orchestration/SKILL.md	path	4	Make the entire Worker Playbook consistently sandbox-only	E4
.gitignore	path	4	Add only .uv-cache/ and verify publication protection	E4
tests/unit/test_generate_agent_configs.py	path	1	Own schema/static-inventory/guard tests; revisit production-output expectations in slice 3	E1/E3
tests/unit/test_validate_agent_assets.py	path	3	Move ordered exclusion fixtures with validator and policy	E3
tests/unit/test_claude_settings_merge.py	path	1	Own exact classification/custom-hook tests; revisit effective baseline in 3 and fake update in 4	E1/E3/E4
tests/unit/test_herdr_agents.py	path	2	Own launcher/source/runtime regressions; add documentation/ignore assertions in slice 4	E2/E4
tests/unit/test_agmsg_orchestration_docs.py	path	4	Own exact sandbox sentence and fixed-host ledger-template contract	E4
tests/unit/test_claude_worker_settings.py	path	2	Own worker preparation/render/deny/delivery integration	E2
tests/unit/test_claude_managed_settings.py	path	4	Own administrative content plus printed-installation target integration	E4
.orchestration/dotfiles-T133-worker-write-boundary-a04/**	path	4	Replace proposed a04 artifact namespace with four actual slice namespaces; final lineage rollup belongs here	Each slice writes its own dispatched copy/evidence; never fabricate an a04 dispatch
home/dot_agents/agent-config.yaml	threat	1	Closed declarations and static inventory; preserve deferred binding ownership	E1
home/.chezmoitemplates/claude-settings-managed.json	threat	3	Guarded baseline; legacy PermissionRequest remains with dotfiles-T133-trusted-entrypoint-binding-a01	E3; other descendant binding belongs to new owner D
home/.chezmoitemplates/claude-worker-settings.json	threat	2	Canonical worker policy and explicit disables accompany preparation	E2
home/.chezmoitemplates/claude-managed-settings.json	threat	2	Canonical administrative content only	E2; installation deferred to E4/operator
home/dot_claude/modify_private_settings.json	threat	1	Exact owned-form classification, ordering and idempotence	E1; no descendant identity claim
home/dot_claude-worker/modify_private_settings.json	threat	2	One source-aware screening policy before mutation	E2
home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl	threat	1	Fixed dispatch and identity routing; descendant binding belongs to D	E1
.claude/settings.json	threat	1	Portable guarded commands and supported failure policy	E1
scripts/generate-agent-configs.py	threat	1	Deterministic declared policy; no candidate-learned schema or installation discovery	E1/E2/E3
scripts/validate-agent-assets.py	threat	3	Preserve all existing checks while moving exact exclusion expectations	E3
Makefile	threat	4	Print privileged commands only; reconcile after installer	E4
home/dot_local/bin/common/executable_herdr-agents	threat	2	All worker routes screen before trust or mutation	E2
home/dot_agents/skills/agmsg-orchestration/SKILL.md	threat	4	No worker escape exceptions; orchestrator exemptions remain distinct	E4
.gitignore	threat	4	Ignore private cache without weakening worklog/cache denies	E4
tests/unit/test_generate_agent_configs.py	threat	1	Both-platform declaration/render correspondence and guard coverage	E1/E3
tests/unit/test_validate_agent_assets.py	threat	3	Exact exclusions, malformed variants and legacy permission composition	E3
tests/unit/test_claude_settings_merge.py	threat	1	Classification and preservation first; effective baseline/update cases later	E1/E3/E4
tests/unit/test_herdr_agents.py	threat	2	Temporary roots and fake processes cover complete startup routes	E2/E4
tests/unit/test_agmsg_orchestration_docs.py	threat	4	Read actual slice-4 dispatched copy; implement no ledger consumer	E4
tests/unit/test_claude_worker_settings.py	threat	2	Configured policy, protected bytes and delivery; complete binding remains residual	E2
tests/unit/test_claude_managed_settings.py	threat	4	Content and printed commands; no administrative execution	E4
.orchestration/dotfiles-T133-worker-write-boundary-a04/**	threat	4	Allocate equivalent evidence controls to every actual slice artifact root	Replicate row in all four texts
<absolute-home>/.claude-worker/settings.json	threat	2	S01 checked before regeneration including every environment entry	E2
<worktree>/.claude/settings.json	threat	2	S02 screens old tracked files without rewriting them	E2; guarded current file already exists from E1
<worktree>/.claude/settings.local.json	threat	2	S03 screening precedes exact legacy migration	E2
<validated-anchor>/.claude/settings.local.json	threat	2	S04 independent main-local screening plus anchor binding	E2
/Library/Application Support/ClaudeCode/managed-settings.json	threat	2	Darwin S05 source-specific screening in temporary managed root	E2
/etc/claude-code/managed-settings.json	threat	2	Linux S05 receives equivalent screening	E2
<managed-root>/managed-settings.d/<name>.json	threat	2	S06 independently checks canonical partial fragments	E2
<absolute-home>/.claude-worker/remote-settings.json	threat	2	S07 independently checks cache and refuses unenumerable delivery	E2
<worktree>/.mcp.json	threat	2	S08 absent/empty only regardless of approval or Git tracking	E2
<validated-anchor>/.mcp.json	threat	2	S09 independently screens inherited main definition	E2
<loaded-ancestor>/.mcp.json	threat	2	S10 independently screens applicable ancestors	E2
<absolute-home>/.claude-worker/.claude.json	threat	2	S11 regenerates empty shared project state every start	E2; cross-worktree fixture
S11 carried identity-field screening	threat	2	Fixed string-only identity members and exact userID shape	E2
<skills-root>/<name>/.claude-plugin/plugin.json	threat	2	S12 covers all six roots including actual enterprise root and disabled plugins	E2
<plugins-root>/installed_plugins.json	threat	2	S13 closed registry records and contained project-bound roots	E2
<plugins-root>/known_marketplaces.json	threat	2	S14 accepts only empty registry	E2
<plugin-root>/.claude-plugin/plugin.json	threat	2	S15 closed metadata and scalar inspected-file references	E2
<plugin-hook-file>	threat	2	S16 default and selected files inspected independently	E2
<marketplace-root>/.claude-plugin/marketplace.json	threat	2	S17 descriptive metadata and absent/empty plugin list only	E2
<plugin-mcp-file>	threat	2	S18 default and selected MCP definitions independently empty	E2
<managed-root>/managed-mcp.json	threat	2	S19 independent empty-server check	E2
<skills-root>/<name>/SKILL.md	threat	2	S20 restricted frontmatter and dynamic-command refusal	E2
<commands-root>/<name>.md	threat	2	S21 inspect default/selected Markdown; reject object/inline/directory forms	E2
<agents-root>/<name>.md	threat	2	S22 restricted metadata without subagent execution	E2
<plugin-lsp-file>	threat	2	S23 empty configuration only	E2
pre-start refusal of unknown settings keys	threat	2	Per-source top-level/nested unknown-key regressions	E2
pre-start refusal of undeclared provider selectors	threat	2	Settings and launch inputs; exact AWS exception only	E2
pre-start refusal of foreign repository roots	threat	2	Both worker kinds and every route refuse before side effects	E2
pre-start refusal of object-form plugin components	threat	2	Disabled-plugin object/source/inline cases refuse	E2
pre-start refusal of non-command hook handlers	threat	2	Inspect type before command; indexed refusal across sources	E2
pre-start refusal of untrusted executable environment-file contents	threat	2	No sourcing; same-start canonical bytes/hash only	E2
manifest-selected non-shim launch interpreter	threat	2	Consume slice-1 declaration on bootstrap/home/preflight routes	E2; no shim/PATH fallback
Darwin platform-injected launch environment	threat	2	Exact optional encoding shape; Linux presence refuses	E2
regime-declared launch environment	threat	2	AGMSG_SPAWNED=1 only for declared roles; retain existing authorities	E2
plugin activation and additional executable components	threat	2	Explicit disables supplement complete source screening	E2
non-file managed delivery and launch overrides	threat	2	Named refusal without discovery helpers	E2
lower-scope sandbox array merging	threat	2	Check each source before merging lists	E2
actual enterprise skills root	threat	2	Managed-root/.claude/skills on both platforms	E2; retain historical green baseline
<absolute-home>/.agents/permgate-policy.yaml	threat	1	Static directory/file protection; execution isolation remains separately owned	E1; deny integration E2
<absolute-home>/.local/lib/python*/site-packages	threat	1	Retain directory and descendant deny patterns	E1; planted-startup binding remains deferred
<absolute-home>/Library/Python/*/lib/python/site-packages	threat	1	Retain macOS directory and descendant patterns	E1; planted-startup binding remains deferred
<absolute-home>/.claude/hooks/orchestrator-only.sh	threat	1	Protect consumed installed guard; descendant execution belongs to D	E1
formatter and project-map configuration selection	threat	1	Reject worker/outside-anchor inputs; complete tool-chain binding belongs to D	E1
.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md	threat	1	Reset carrier retains a03 copy and evidence unchanged	E1; no predecessor deletion
.orchestration/dotfiles-T133-worker-write-boundary-a04/task.md	threat	1	Replace proposed copy with actual slice-1 copy and corresponding per-slice copies	No fake a04 dispatch; every actual copy matches its TASK hash
evidence records	threat	4	Final lineage reconciliation; each earlier slice supplies its own final-head evidence	Replicate in every slice
task metadata	threat	1	Carrier establishes reset lineage; each successor checks its own scope/dependencies	Replicate in every slice
metadata separators	threat	1	Whole-file digest covers format-2 metadata and body	Replicate in every slice
in-process effects	threat	1	Repository generation and temporary fixtures only	Replicate in every slice; no deployment
workflow and interpreter or environment inputs	threat	2	Role-specific startup validation; full downstream binding remains deferred	E2; D owns guard/delivery/formatter/map descendants
new or renamed scripts	threat	1	Existing renderer/preparation/guard surfaces only; no new helper or sidecar	Replicate in every slice
5.14 item 0: 脅威モデル	threat	4	Consolidate honest same-UID/shared-credential residuals	Replicate residual in every slice
5.14 item 1: 書き込み境界	threat	2	Consume declared write policy and complete closed startup screen	E2; no race/reload closure
5.14 item 2: 無害化した環境を最初に	threat	2	Clean role-specific launch inputs; legacy PermissionRequest stays deferred	E2; D owns downstream families
5.14 item 3: 信頼パスの境界検査	threat	2	Canonical anchor/component containment; guard routing already in E1	E2; downstream executable binding remains with D
5.14 item 4: 検証したものを実行し、検証した内容を渡す	threat	1	Fixed guard dispatch only; snapshot/last-use and descendant guarantees remain with consumers	E1; D for the four descendant families
5.14 item 5: 出力と予約の同一性	threat	none	dotfiles-T133-audit-pool-a02 owns pool reservations; consumers own their full-head outputs	Do not add reservation machinery or claim closure here
5.14 item 6: 正直な残余	threat	4	Consolidate residual/deployment reporting without relabelling deferred findings	Replicate in every slice
5.14 item 7: 検証	threat	2	Complete S01-S23 and startup regressions; other slices retain their focused checks	E1-E4; shared helper ownership stays with P1-6
5.14 item 8: 承認はコミット済み台帳から読む	threat	4	Fixed-host template contract only; permission-guard-gate-a05/P1-6 own consumption	E4; no approval consumer
5.14 item 9: 私設キャッシュ	threat	2	Private cache delivery and protected shared-cache inventory	E2; publication ignore E4; resolver/deployment remain separate
5.14 item 10: worker は sandbox 外でコマンドを実行しない	threat	4	Exact Worker Playbook rule and removal of contradictory exemptions	E4; operator Codex deployment remains separate
canonical GitHub API host binding	threat	4	Test both exact templates under hostile GH_HOST	E4; consumer enforcement deferred
hook failure policy	threat	1	Supported tracked/guarded entries retain onFailure block	E1/E2/E3; no timeout/background enforcement claim
agmsg store driver and plugin selection	threat	none	dotfiles-T133-agmsg-hardening-a01 owns driver validation and plugin authorization	Retain static denies and explicit sourcing residual
orchestrator effect merge	threat	4	Final-head evidence and pinned integration are orchestrator authority	Replicate in every slice
orchestrator effect update-branch	threat	4	Every moved head requires fresh required evidence	Replicate in every slice
orchestrator effect forced worker removal	threat	4	None planned; preserve dirty-worktree protections	Replicate in every slice
a01 template-suffix finding f1b862c	finding	1	Guard must remain an executable chezmoi template	E1
text-security:f589c7c:1	finding	2	Inspect legacy local hooks before exact owned migration	E2
a01 validator/exclusion and composition blockers	finding	3	Update every policy-sensitive validator check and fixture together	E3
text-security:772cde0:1	finding	1	Protect permgate policy and interpreter startup inputs	E1; deny integration E2
text-security:f810c30:1	finding	none	dotfiles-T133-trusted-entrypoint-binding-a01 owns PermissionRequest interpreter binding	Legacy command bytes unchanged
text-security:772cde0:2	finding	none	dotfiles-T133-trusted-entrypoint-binding-a01 owns isolated PermissionRequest execution	Static user-site denies do not close execution
text-security:e5c055e:1	finding	none	dotfiles-T133-trusted-entrypoint-binding-a01 owns bound deployment checker execution	No new effective-settings checker
text-security:e5c055e:2	finding	none	dotfiles-T133-trusted-entrypoint-binding-a01 owns non-shim binding-test discovery	Startup interpreter selection in E2 is narrower
text-security:5204254:1	finding	none	dotfiles-T133-trusted-entrypoint-pins-a01 and dotfiles-T133-trusted-entrypoint-binding-a01 own measured layouts	No guessed uv layout
text-security:5204254:2	finding	none	dotfiles-T133-trusted-entrypoint-descendants-followup-a01 owns formatter descendant chain	Node availability is not established here
a01 independent pre-push missing/non-executable delivery tool	finding	2	Boundary preparation must not disappear when delivery tool is unavailable	E2
Bot 4313733345 defaultMode omission	finding	2	Worker rendered/prepared policy retains defaultMode auto	E2
security:a286915 sandbox-rule contradiction	finding	4	Settle contradictory Worker Playbook exemptions explicitly	E4
security:ea3c4fb:1	finding	2	Screen old tracked settings before startup; never normalize them to pass	E2; current guarded file supplied by E1
text-security:2ae9e2c:1	finding	2	Project MCP independently screened regardless of approval	E2
text-security:ebbb71b:1	finding	2	Skills-directory plugins remain inventoried when disabled	E2
text-security:ebbb71b:2	finding	2	Global MCP empty; projects discarded and regenerated empty	E2
text-security:ebbb71b:3	finding	4	Canonical main comes from fixed repository API	E4 template contract
text-security:b2a186e:1	finding	2	Handler type checked before command, including command-free HTTP	E2
text-security:b2a186e:2	finding	4	Both deciding API templates explicitly bind github.com	E4
a02 independent pre-push env.HOME	finding	2	Candidate settings environment cannot select a foreign guard	E2
a02 independent pre-push fenced dynamic commands	finding	2	Inspect dynamic commands throughout Markdown including fences	E2
local:79ea98a:1	finding	2	Keep manifest-generated --advisor fable accepted	E2
local:79ea98a:2	finding	2	Keep absolute tool calls and attachment identity environment	E1 guard plus E2 attachment
local:79ea98a:3	finding	1	Preserve custom hooks and exact legacy managed migration	E1
local:79ea98a:4	finding	1	Retain legacy PreToolUse migration; historical main-local screening obligation also belongs to E2	E1/E2; preserve original advisory history
security:c0f50fa:1	finding	2	Refuse AWS/provider credential-chain selectors in settings and launch inputs	E2; c0f50fa1 red
security:c0f50fa:2	finding	2	Refuse foreign repositories before any worker-route side effect	E2; c0f50fa1 red
security:c0f50fa:3	finding	2	Refuse object/inline plugin component forms	E2; c0f50fa1 red
local:c0f50fa:1	finding	2	Use actual enterprise skills root	E2; accepted retained-green baseline
local:c0f50fa:2	finding	2	Reject sandbox list extensions before merging	E2; c0f50fa1 red
local:c0f50fa:3	finding	4	Print privileged parent creation before install	E4; c0f50fa1 red
local:c0f50fa:4	finding	4	Reconcile after fake Herdr installer and prove repeated-update idempotence	E4; c0f50fa1 red
text-security:f7af699:1	finding	2	Screen executable environment-file contents and bind same-start generated bytes	E2
worker:5067ed0:1	finding	2	Discard native counters/state and regenerate S11 after complete preflight	E2
text-security:efa211d:1	finding	2	Sequential sibling starts share config directory; projects always regenerated empty	E2; A-then-B fixture
text-security:be969e3:1	finding	2	Plant Markdown and bundled-plugin fixtures under managed-root/.claude/skills	E2; no manufactured red result
a03 runtime-blocked PONG	finding	2	Use declared non-shim interpreter and explicit platform/regime name classes	E2; preserve failing draft/probe evidence
text-security:d562c68:1	finding	none	dotfiles-T133-trusted-entrypoint-descendants-followup-a01 must own all four excluded descendant families	Owner text/design mapping before dispatch; binding-dependent deployment waits for owner
text-security:08e6ac7:2	finding	none	dotfiles-T133-agmsg-hardening-a01 owns store-driver traversal	Retain residual; static denies are mitigation
text-security:5cbbc03:2	finding	none	dotfiles-T133-agmsg-hardening-a01 owns trusted-plugin sourcing	Retain residual; ordinary stores remain writable
```

2. Slice definitions and intermediate conditions

Keep **four slices**, with reassignment from the provisional grouping. The TSV identifies the primary accountable slice; explicitly listed shared paths are revisited sequentially. Each actual task needs threat rows for **all its own allowed files**, including revisited paths and its evidence directory.

Use task IDs `dotfiles-T133-worker-write-boundary-slice{1,2,3,4}-a01`. Below, `S1`–`S4` abbreviate those IDs and `D` means `dotfiles-T133-trusted-entrypoint-descendants-followup-a01`.

Every merge requires `make render-check`, `make validate-agent-assets`, applicable formatting/lint, required GitHub CI, and fresh final-head review/audit/security evidence. Local Bats remain prohibited. These are proposed conditions, not observed passing results.

**Slice 1 — schema, guard, tracked settings and migration foundation**

`after: []`; **the sole `reset_of: [dotfiles-T133-worker-write-boundary-a03]` carrier**.

Allowed files, **8**:

```text
home/dot_agents/agent-config.yaml
scripts/generate-agent-configs.py
home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
.claude/settings.json
home/dot_claude/modify_private_settings.json
tests/unit/test_generate_agent_configs.py
tests/unit/test_claude_settings_merge.py
.orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**
```

**E1:** Both make targets and the complete `tests.unit.test_generate_agent_configs`, `tests.unit.test_claude_settings_merge`, `tests.unit.test_validate_agent_assets`, `tests.unit.test_herdr_agents`, and `tests.unit.test_agmsg_orchestration_docs` modules pass.

Declare the complete startup schema, source inventory, interpreter/environment authorities and static denies. Add/test pure worker/admin render functions, but **register their output files in slice 2**. Register/render the guard now and change tracked commands atomically with it. Extend orchestrator merge classification using synthetic canonical forms while preserving custom hooks and existing effective baseline.

Keep the existing orchestrator generated template, sandbox/exclusion policy and PermissionRequest command unchanged. Thus the existing validator’s Linux four-entry expectation remains valid until slice 3. No launcher enforcement is claimed yet.

**Slice 2 — startup screening and worker/admin outputs**

`after: [dotfiles-T133-worker-write-boundary-slice1-a01]`; no reset.

Allowed files, **8**:

```text
scripts/generate-agent-configs.py
home/.chezmoitemplates/claude-worker-settings.json
home/.chezmoitemplates/claude-managed-settings.json
home/dot_claude-worker/modify_private_settings.json
home/dot_local/bin/common/executable_herdr-agents
tests/unit/test_herdr_agents.py
tests/unit/test_claude_worker_settings.py
.orchestration/dotfiles-T133-worker-write-boundary-slice2-a01/**
```

**E2:** Both make targets and all five E1 modules plus complete `tests.unit.test_claude_worker_settings` pass.

Register both new generated outputs in the same change as their preparation consumer. Implement the single preflight, S01–S23, executable-file contents, S11 regeneration, all launch routes, narrow interpreter consumption and runtime-name classes. The guard and guarded current tracked settings already exist.

Existing unguarded main-local settings must refuse unchanged; accepting those installations waits for slice 3/application. Administrative content is generated but has no installation target yet. Extract launcher changes selectively from the saved draft: defer documentation/ignore assertions until slice 4. No live dependents are released.

**Slice 3 — effective orchestrator settings and validator alignment**

`after: [dotfiles-T133-worker-write-boundary-slice2-a01]`; no reset.

Allowed files, **8**:

```text
home/dot_agents/agent-config.yaml
scripts/generate-agent-configs.py
home/.chezmoitemplates/claude-settings-managed.json
home/dot_claude/modify_private_settings.json
scripts/validate-agent-assets.py
tests/unit/test_generate_agent_configs.py
tests/unit/test_validate_agent_assets.py
tests/unit/test_claude_settings_merge.py
.orchestration/dotfiles-T133-worker-write-boundary-slice3-a01/**
```

This list has **9**, so one reassignment is necessary: **do not reopen `home/dot_claude/modify_private_settings.json` here**. Slice 1 must finish its complete exact classifier, PreToolUse migration and attachment construction against synthetic canonical fixtures. Slice 3 consumes that implementation unchanged. The resulting allowlist has **8**.

**E3:** Both make targets and all six E2 modules pass.

Activate the orchestrator baseline, guarded hooks, startup failure and exact ordered three exclusions on both platforms. Change manifest, generated output, validator and their literal expectations together. Preserve every existing validator check and legacy PermissionRequest bytes/recognition.

Slice 1’s migration must already handle these forms without deleting custom hooks or keeping stale managed duplicates. `make update` reconciliation after Herdr remains explicitly incomplete until slice 4; no deployment occurs between these merges.

**Slice 4 — update/staging, documentation, ignore and lineage completion**

`after: [dotfiles-T133-worker-write-boundary-slice3-a01]`; no reset.

Allowed files, **8**:

```text
Makefile
home/dot_agents/skills/agmsg-orchestration/SKILL.md
.gitignore
tests/unit/test_claude_managed_settings.py
tests/unit/test_claude_settings_merge.py
tests/unit/test_herdr_agents.py
tests/unit/test_agmsg_orchestration_docs.py
.orchestration/dotfiles-T133-worker-write-boundary-slice4-a01/**
```

**E4:** Both make targets and **all seven complete a04 Check modules** pass, using the two original unittest command groups with the actual slice-4 task copy substituted in documentation fixtures.

Finish printed mkdir/install ordering, fake-update reconciliation, sandbox-only documentation, hostile-host template tests and `.uv-cache/` ignoring. During earlier slices, cache artifacts must remain outside staged changes; the ignore regression becomes mandatory here.

Every slice owns its own byte-identical dispatched copy, report and final-head evidence. Slice 4 reconciles lineage and pending deployment; it does not retrospectively supply missing earlier evidence. Preserve a01/a02/a03 history, the failing draft and counters. R1-2’s fresh branches replace a04’s obsolete instruction to continue PR #431; preserve that branch/draft and close #431 only through orchestrator bookkeeping.

3. J1: descendant-binding owner

Create **`dotfiles-T133-trusted-entrypoint-descendants-followup-a01`**, assigned to a011, `after: [dotfiles-T133-trusted-entrypoint-binding-a01]`, and register it in the design’s implementing-task map before using it as an out-of-scope owner.

Its four families are:

| Family | Execution and input binding it must own |
| --- | --- |
| Guard | Installed guard, its interpreter and fixed project payload chain: ContextDB hooks, stop gate, state/attachment operations and their consumed inputs. |
| Delivery | Fixed agmsg delivery operations, session-start/session-end/check-inbox/identities and reached descendants, executable identities and configuration inputs. Store-driver/plugin authorization remains the agmsg-hardening owner. |
| Formatter | Formatter script and Ruff/Prettier/Node chain, configuration selection, executable availability and rejection tests. |
| Map | Project-map reload and terminal-browser/runtime descendants, selected inputs/configuration and rejection tests. |

Correct the descendant portions of **slice 1** rows for the guard source/installed guard, formatter/map selection, orchestrator merge script, renderer, tracked hooks and design items 2–4; **slice 2** rows for worker delivery, preparation, reached execution/environment inputs and associated tests; **slice 3**’s orchestrator-template row; and **slice 4**’s consolidated residual/deployment text.

Keep those rows residual for their implemented routing/screening portions and name D for deferred binding. Do not transfer the unchanged legacy PermissionRequest, its structural validator or isolated execution away from binding-a01. Version pins remain pins-a01.

Full-binding dependents wait for D. Phase-A deployment retains the plan’s explicit existing-binding allowance, records all four residual families and compensating controls, and does **not** acquire a circular dependency on D.

4. Slice-1 brief for `author-loop.sh`

```markdown
task_id: dotfiles-T133-worker-write-boundary-slice1-a01
purpose: Establish the complete declared startup contract, fixed guard, guarded tracked settings and exact migration foundation; implement no launcher screen yet.
kind: code; security: true; worker: a010, Codex security seat.
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
  - .claude/settings.json
  - home/dot_claude/modify_private_settings.json
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice1-a01/**
after: []
reset_of: [dotfiles-T133-worker-write-boundary-a03]
retained_predecessor_directories: [.orchestration/dotfiles-T133-worker-write-boundary-a03/]
Preserve a01/a02 artifacts, a03 failing draft/probes and all counters; no predecessor deletion or writes.
Use a fresh origin/main branch; preserve tools/worker-write-boundary-a01 and PR #431 history.
Read a04 Closed startup schema/Regression fixtures and BRIEF-TEMPLATE-NOTES.md; retain measured host facts and name every evidence producer/seat.
Declare exhaustive settings/nested values, S01-S23, roots/components, four settings-env pairs, role environments, measured non-shim Python and identity fields.
Test pure worker/admin renders; register those output files only in slice 2. Preserve current orchestrator output/exclusions/PermissionRequest until slice 3.
Render guard now; change tracked hooks with it; finish exact legacy/canonical classification, attachment construction and PreToolUse migration now.
Carry render fixtures: both platforms, static inventory, policy/guard/user-site directory+descendant denies, writable stores, spaces/aliases and deployment-independent rendering.
Carry guard fixtures: anchored positive, worker/sibling/unrelated/missing identities, outside/worker tool inputs, fixed argv/stdin/status and absent BASH_ENV markers.
Carry merge fixtures: custom/mixed hooks, ordering, escaped tilde, stale legacy replacement, PreToolUse and idempotence using synthetic canonical forms.
Declare S11 discard/regenerate/projects-empty, executable-file same-start bytes/hash and runtime-name contracts; their actual launch regressions belong to slice 2.
Threat headings: eight allowed paths; predecessor/current copies; metadata/separators/evidence; effects/environment/scripts; 5.14 items 0-10; merge/update-branch/forced-removal.
Name descendants-followup-a01 for guard/delivery/formatter/map binding; binding-a01 retains PermissionRequest; agmsg-hardening-a01 retains store sourcing.
Proposed cap: at most 650 changed source lines outside tests/, .orchestration/ and the three a04 generated-template exclusions, and 650 under tests/.
Measure with git diff --numstat <authenticated-merge-base> <head>; preserve 51ba5801..c0f50fa1 comparison and reconcile shared-control attribution.
Require E1 complete modules, render-check, validate-agent-assets, changed-file lint, CI and final-head evidence; no local Bats, live deployment or socket probe.
Author at most 193 lines before an approximately seven-line Checks block; final text <=200 lines, <=8 paths, C-80 <=2; anchor reviewed bytes without repasting.
```

5. Decisions needed before dispatch

- **Confirm the four IDs and serial shared-file scopes.** Default: use S1–S4 above; finalize slice 3 with the eight-entry list excluding the already-completed orchestrator modify script.
- **Confirm slice-1 caps after extraction measurement.** Default: provisional **650 source / 650 tests**; reconcile against a04’s aggregate **1591 / 2528**, counting shared controls once. Stop on measured overrun; do not silently increase budgets.
- **Create/register D and amend owner references before C-80.** Default: J1’s new owner, a011, after binding; retain Phase-A residual allowance.
- **Confirm artifact/lineage migration.** Default: four actual slice namespaces, only S1 resets a03, retain predecessor evidence unchanged; never create a purported dispatched a04 copy.
- **Resolve historical finding-label discrepancies.** Default: preserve original advisory records/owner history and carry all observed custom-hook, PreToolUse and main-local-screening obligations; add an explicit crosswalk rather than rewriting history.
- **Choose the foreign-root refusal identifier.** Default: replace a04’s task identifier with S2’s actual dispatched ID and update its exact-message fixture together.
- **Fix all aggregate dependency edges before dispatch.** Default: network→S1; launcher consumers→S2; settings prerequisites→S3; audit/verdict documentation prerequisites→S4, preserving independent pins/resolver/a05 dependencies and deployment gates.

📝 まとめ: a04 の22パス・90脅威行と引継ぎ所見を4スライスへ配分し、J1の所有者とslice 1 briefを整理しました。dispatch前に上記の既定値と証跡・予算配分をorchestratorが確定してください。
Not checked: implementation, tests, CI or live enforcement; no files written. Intermediate green conditions and caps require implementation-time verification.
**Preferring concise responses**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-{3844d93,0b96f40,0e9bf3f,0f87501,4e8b427,e39dc8f,f4246e9}.md.last.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-401573e.md' in ~/Workspace/dotfiles

exec
/bin/zsh -lc "cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01.md; rg -n '"'^##|''^###|''^0'"\\.|"'^1'"\\.|"'^2'"\\.|"'^3'"\\.|"'^4'"\\.|"'^5'"\\.|"'^6'"\\.|"'^7'"\\.|"'^8'"\\.|"'^9'"\\.|"'^10'"\\.|GIT_|gh |shim|residual|slice1' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
# dotfiles-T133-worker-write-boundary-slice1-a01 — acceptance record (pre-dispatch)

Plan 024 P1-15 slice 1 (re-plan v2 R1-1/R1-2, J2): the reset carrier of `dotfiles-T133-worker-write-boundary-a03` (`reset_of`), the first of five slices that replace the withdrawn a04 single text. Seat: a010 (Codex, security profile) after `dotfiles-T133-trusted-entrypoint-pins-a01` and PR #448 merge. Owner stubs for the deferred obligations: slice2-5, `dotfiles-T133-trusted-entrypoint-descendants-followup-a01`, `dotfiles-T133-agmsg-hardening-a01`.

- 2026-10-21T01:50Z: allocation table drafted by the review-profile context (`.agents/worklog/orchestrator-glue/a04-allocation-r1.md`, saved as `.orchestration/plans/024-allocation.tsv`); brief `brief-wwb-slice1.md`; author-loop.sh (brief -> text -> pre-send -> C-80, two rounds).
- 2026-10-21T02:19Z: design 1 (190 lines, 8 paths incl. `.claude/settings.json`): C-80 round 1 (`…-text-security-0b96f40.md`) one P2 (owner files slice2/slice4/agmsg-hardening absent), round 2 (`…-f4246e9.md`) the same P2 -> owner stubs created, bytes unchanged.
- 2026-10-21T02:42Z: C-80 round 3 on the same bytes (`…-f4246e9.md`, re-run): the owner finding resolved; new P2: switching the tracked hooks in `.claude/settings.json` to the guard before deployment stage A installs it removes the stop gate from sessions loading the tracked settings. S-R5: no fourth round on design 1; re-sliced (re-plan line below): `.claude/settings.json` and the activation move to `dotfiles-T133-worker-write-boundary-slice5-a01` (after slice 4 and stage A); design 1 text set aside (`.agents/worklog/orchestrator-glue/slice1-a01-design1-withdrawn.md`).
- 2026-10-21T02:54Z: design 2 (186 lines, 7 paths, brief v2): C-80 round 1 (`…-0e9bf3f.md`) Verdict correct.
- 2026-10-21T02:56Z: `after:` set to [trusted-entrypoint-pins-a01, worker-sandbox-exclusions-a02] (shared files: tests/unit/test_generate_agent_configs.py with pins; agent-config.yaml and the two test files with #448); sha256 3844d937. The C-80 re-run on these bytes was refused by C-92 (three reviews since the newest re-plan line; this record did not exist yet); the re-plan line below records design 2 and the review of 3844d937 follows it.
- 2026-10-21T02:59Z: anchor review `dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01` dispatched to a012 (TASK 2935) on sha 3844d937.

text-security:0b96f40:1	owner-files-absent
text-security:f4246e9:1	owner-files-absent
text-security:f4246e9:2	tracked-hook-activation-before-provisioning
text-security:0e9bf3f:0	correct

re-plan: tracked-hook-activation-before-provisioning (rows text-security:f4246e9:2; the class that forced the re-slice of design 1) — specification: no slice switches a tracked hook command to a guard path before deployment stage A has installed that guard on the host, so no session that loads the tracked settings loses its stop gate between merges; design: slice 1 renders the guard template and the migration logic only and leaves `.claude/settings.json` untouched; a new slice 5 (`dotfiles-T133-worker-write-boundary-slice5-a01`, after slice 4 and stage A) switches the tracked references with a test that the deployment inventory lists the installed guard; implementation: design 2 of slice 1 (186 lines, 7 paths, sha 3844d937) and the slice5 owner stub; verification: the C-80 of design 2 reports no activation-order finding and the anchor review of another context accepts the redesign bytes.
- 2026-10-21T03:09Z: C-80 of 3844d937 (`…-text-security-3844d93.md`): one P2 at line 137: the text preserves the old Linux four-entry exclusion policy (incl. `gh *`) while its new prerequisite `worker-sandbox-exclusions-a02` empties both platforms and makes the validator reject non-empty lists. Cause: the allocation brief described the baseline as today's main, not the post-prerequisite state; the `after:` edge added at 02:56Z made the conflict visible. Anchor review on 3844d937 withdrawn (PING to a012). Re-plan line below; brief v3; author-loop round on design 2 with the baseline rule.

text-security:3844d93:1	prerequisite-baseline-conflict

re-plan: prerequisite-baseline-conflict (rows text-security:3844d93:1; a baseline statement contradicted the task's own prerequisite) — specification: every baseline-preservation statement and fixture in a slice text binds to the state of main after the slice's `after:` prerequisites have merged, never to the main of the authoring day; design: the brief names each prerequisite's post-merge effect (worker-sandbox-exclusions-a02: both platforms' excludedCommands empty and the validator rejects non-empty lists; pins-a01: the pinned mise declaration) and the text's Design and Check sections cite them; implementation: brief v3 and the re-authored slice 1 text; the rule is added to BRIEF-TEMPLATE-NOTES.md for every later slice; verification: the C-80 of the re-authored text reports no prerequisite-baseline finding and the anchor review of another context accepts the bytes.
- 2026-10-21T03:10Z: anchor review a01 (a012, RESULT 03:07:48Z) rejected 3844d937 with F1 (= the C-80 finding at line 137) and F2 (line 78 says `Keep after: []` against the two edges at line 18). Both go into the brief v3 round: the prose must state the two prerequisites and their post-merge effects, no `after: []` sentence. The next anchor review is `…-redesign-review-a02` on the new sha.
- 2026-10-21T03:33Z: design 2 round 2 (brief v3: baseline bound to the post-prerequisite state; 189 lines, 7 paths): C-80 `…-text-security-0f87501.md` correct; `after:` set to [pins-a01, worker-sandbox-exclusions-a02] and the `Keep after: []` sentence replaced (anchor F2); C-80 of the final bytes e39dc8fb (`…-text-security-e39dc8f.md`) correct. Anchor review a02 dispatched to a012 on e39dc8fb.

text-security:0f87501:0	correct
text-security:e39dc8f:0	correct
- 2026-10-21T09:19Z: prerequisites met (PR #448 e042663b and PR #449 4eafd890 merged; canonical main 4eafd890); Checks pasted (6 lines), bytes now 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9 (194 lines, pre-send OK); re-anchor review `dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a03` sent to a011 (D-024-59); liveness PING to a010 (2984). Dispatch line: preconditions=met:this record, overlap_ok=431,420,406.
- 2026-10-21T09:28Z: re-anchor accepted (a011 RESULT 2987, sha 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9); dispatched to codex-standard-dot-a010 (worker-e, wJ:p5) as bus 2989 (read 09:28:18Z), round 1, fresh branch tools/worker-write-boundary-slice1-a01 from main 4eafd890, preconditions=met (this record), overlap_ok=431,420,406 (own lineage branch; parked permission-guard a03 branch; phase-2 draft). Counters before the send (C-126): a03 TASKs=2 RESULTs=0 questions=0 (S2 silenced by the a03 design-reset record); slice1 all 0. a010 had read PING 2984 without a PONG; the TASK asks for the PONG first.

5:5.8 **多重並列時のボトルネック（スケールの天井）と対処。** 第 1 段階は今ある直列点を外すが、席を 4 → 6 → それ以上に増やすと別の天井に当たる。各天井を数で示し、対処と計測を plan に固定する。
9:| S1 | orchestrator の受け入れ判定と最終マージが 1 席の直列 | P1-4〜P1-6 の後、1 RESULT の受け入れは verdict ファイル確認 + 記録生成 + `gh pr merge` で約 2〜5 分 → 12〜20 件/時。6 席が同時に RESULT を出すと最大 30 分待ち | 受け入れは RESULT 到着順で 1 件ずつ、判定に要る情報は P1-5 の precheck 証跡と review verdict に集約して読む量を固定。第 2 段階 H3 で review verdict を両ベンダーの席が返す。受け入れ権限は orchestrator に残す（rules） | 受け入れ待ち時間の分布を bus 履歴から出す（RESULT → ACCEPTANCE の時刻差） |
11:| S3 | GitHub-hosted runner の同時実行 20 ジョブ / macOS 5 ジョブ（Free〜Team 共通） | PR 1 本 = validate 1 + test 3（うち macOS 1）+ public-bootstrap 3（うち macOS 1）+ private-bootstrap 3（うち macOS 1）= 10 ジョブ・macOS 3。同時に走るのは PR 2 本分。F5 後は 7 ジョブ・macOS 1〜2 → PR 3〜5 本分 | F5（concurrency、private-bootstrap を PR から外す、in-job skip）。それでも天井は PR 3〜5 本の同時 CI。それ以上はキュー。self-hosted runner は公開リポジトリでは GitHub docs が非推奨（fork PR が任意コードを実行）なので採らない。macOS の test も対象ファイルが OS 非依存（`scripts/*.py`、`tests/unit/**` のみ）のときは in-job skip を検討（品質への影響を F5 の item 0 で判断） | `gh run list --json` から queued 時間の中央値 |
14:| S6 | GitHub API レート制限（REST 5,000 / 時、GraphQL 5,000 pt / 時、1 トークン共有） | `gh pr checks --watch` の既定 10 秒間隔 = 360 回/時/席。6 席 + sweep + gate で 3,000 回/時に近づく | P1-4 の `integrate-seat.sh` は `--interval 30`（120 回/時/席）。sweep は最終 head のみ | `gh api rate_limit` を boundary ごとに記録 |
20:5.9 **PR 多重時の CI / Bot の最適化と品質確保（F5 の仕様。品質の後ろ盾は「main への push で全マトリクスが走り、赤なら凍結」）**
32:| Q9 | 計測 | boundary ごとに `gh run list --json` から PR 1 本の run 数、wall time 中央値、queued 中央値、main 赤の回数を記録 | 数で改善を確認 | — |
34:5.10 **追加の仕組み化（品質と効率を同時に上げる残り箇所。ユーザー問い 11:3x）**
40:| M1 | accept の緑の経路でも orchestrator（LLM）が verdict を読んで ACCEPTANCE とマージを打つ | `verdict.sh --apply`: 9 条件すべて緑なら ACCEPTANCE 行の送信と `gh pr merge --squash --match-head-commit` まで 1 コマンドで実行。`--loop` で ready な PR を順に処理（orchestrator が boundary ごとに起動。権限は orchestrator のまま、判断が機械になるだけ） | 判定条件が固定され、読み落としも「急いでマージ」もない | 緑の経路から LLM の往復（20〜60 分）が消える。LLM は hold / revise だけ見る | 採用。P1-4a に含める |
48:| M9 | CI の flake（macOS の tap、ネットワーク）を人が見分けて再実行 | 既知 flake の署名リスト（`.github/flakes.yaml`）に一致する失敗だけ `gh run rerun --failed` を 1 回。それ以外は本物として扱う | flake の扱いが明文化され、実失敗を隠さない | 手動の再実行待ちが消える | 採用。P1-3 F5 に含める |
55:5.11 **品質保証の仕組み（効率の対になる側。ユーザー指摘 11:4x「効率のみで品質確保が抜けている」）**
70:5.13 **「人の判断」の細分化（ルール化・プログラム化できるもの / AI エージェントが判断できるもの / 人にしかできないもの）**
75:| 〃 | 実態との drift: plan の PR/ブランチ/head/状態が gh と git の現在値と一致、progress.tsv の state が受け入れ記録と一致 | プログラム | `plan-check.py --drift`（boundary ごとに実行、不一致を progress に書く） | P1-12 |
82:| 〃 | 残存リスクの受容（P0/P1 を直さずに進む）、期限や範囲を変える再計画 | **人** | `D-…-residual-risk` 行。既定値なし | ユーザー |
86:| trust-boundary タスクのタスク文レビュー | 形の検査: 3 つの形の規則（test selector、sentence、owning task id）、threat_table の単位規則（allowed_files 1 行につき 1 行、非パス制御 1 つにつき 1 行、orchestrator 効果 1 つにつき 1 行）、各行の disposition が `closed`（テストあり）/ `residual`（制御あり）/ `out-of-scope`（owner 実在）、premises が実行出力、invariants の設計文と byte 一致（INV-2） | プログラム | `task-consistency-check.py` の拡張（C11〜C15） | P1-12 |
88:| 〃 | 権限・信頼境界を広げるタスク（excludedCommands、allowMachLookup、hooks で gh 書込を決める、sandbox の allowWrite） | **人** | 下の「権限の変更」に合流 | ユーザー |
89:| ruleset と権限の変更 | 検知: 権限面（`permissions.*`、`excludedCommands`、`allowMachLookup`、`allowWrite`、`allowedDomains`、gh 書込を決める hook、ruleset パラメータ）の diff を機械で抽出し、`D-… scope=permission approved_by=user diff_sha256=<…>` の決定行が無ければ validator と CI が fail | プログラム | `permission-guard.py`（validate CI。diff の sha256 と決定行を照合） | 新 P1-14 |
95:### 5.14 残余（凍結後の計測事実、D-024-29）
99:5.12 **プログラム仕様** は `024-design-programs.md` に分離（17 項目: verdict.sh、audit-pool.sh と orch-audit.sh --json、schemas、result-precheck.sh、dispositions.py、regime.yml、dispatch.sh --next、acceptance-front-matter.py、git hooks、handoff.sh、flakes、task-from-plan.py）。
103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
107:1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19). The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).
108:2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
109:3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.
110:4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
111:5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
112:6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
113:0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
114:8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder; a `gh api graphql` call binds the repository through fixed query variables (`owner: "mryfmo"`, `name: "dotfiles"` as constants in the script, passed with `-f`/`-F`) and uses only node ids obtained from a query bound by those variables (verdict a04 C-80 round 5, 2026-10-19): the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged. The sha of canonical `main` comes from the fixed repository's API (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`), never from `git ls-remote origin`, whose destination the local remote and URL-rewrite configuration control (P1-12 a04 C-80, 2026-10-19T20:01Z); the content read at that sha comes from `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>`. Every `gh api` call that decides also binds the host with `--hostname github.com` (`GH_HOST` and the hosts configuration select the API host otherwise), a subcommand binds it through the `github.com/mryfmo/dotfiles` form of `--repo`, and a test that exports a hostile `GH_HOST` shows the call still names github.com or refuses (a02 review b2a186e, 2026-10-19T20:36Z).
115:9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
116:10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
117:7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

**Avoiding log self-reference**
exec
/bin/zsh -lc "cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-slice1-a01.md; sed -n '95,118p' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
 succeeded in 1ms:
# dotfiles-T133-worker-write-boundary-slice1-a01 — acceptance record (pre-dispatch)

Plan 024 P1-15 slice 1 (re-plan v2 R1-1/R1-2, J2): the reset carrier of `dotfiles-T133-worker-write-boundary-a03` (`reset_of`), the first of five slices that replace the withdrawn a04 single text. Seat: a010 (Codex, security profile) after `dotfiles-T133-trusted-entrypoint-pins-a01` and PR #448 merge. Owner stubs for the deferred obligations: slice2-5, `dotfiles-T133-trusted-entrypoint-descendants-followup-a01`, `dotfiles-T133-agmsg-hardening-a01`.

- 2026-10-21T01:50Z: allocation table drafted by the review-profile context (`.agents/worklog/orchestrator-glue/a04-allocation-r1.md`, saved as `.orchestration/plans/024-allocation.tsv`); brief `brief-wwb-slice1.md`; author-loop.sh (brief -> text -> pre-send -> C-80, two rounds).
- 2026-10-21T02:19Z: design 1 (190 lines, 8 paths incl. `.claude/settings.json`): C-80 round 1 (`…-text-security-0b96f40.md`) one P2 (owner files slice2/slice4/agmsg-hardening absent), round 2 (`…-f4246e9.md`) the same P2 -> owner stubs created, bytes unchanged.
- 2026-10-21T02:42Z: C-80 round 3 on the same bytes (`…-f4246e9.md`, re-run): the owner finding resolved; new P2: switching the tracked hooks in `.claude/settings.json` to the guard before deployment stage A installs it removes the stop gate from sessions loading the tracked settings. S-R5: no fourth round on design 1; re-sliced (re-plan line below): `.claude/settings.json` and the activation move to `dotfiles-T133-worker-write-boundary-slice5-a01` (after slice 4 and stage A); design 1 text set aside (`.agents/worklog/orchestrator-glue/slice1-a01-design1-withdrawn.md`).
- 2026-10-21T02:54Z: design 2 (186 lines, 7 paths, brief v2): C-80 round 1 (`…-0e9bf3f.md`) Verdict correct.
- 2026-10-21T02:56Z: `after:` set to [trusted-entrypoint-pins-a01, worker-sandbox-exclusions-a02] (shared files: tests/unit/test_generate_agent_configs.py with pins; agent-config.yaml and the two test files with #448); sha256 3844d937. The C-80 re-run on these bytes was refused by C-92 (three reviews since the newest re-plan line; this record did not exist yet); the re-plan line below records design 2 and the review of 3844d937 follows it.
- 2026-10-21T02:59Z: anchor review `dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a01` dispatched to a012 (TASK 2935) on sha 3844d937.

text-security:0b96f40:1	owner-files-absent
text-security:f4246e9:1	owner-files-absent
text-security:f4246e9:2	tracked-hook-activation-before-provisioning
text-security:0e9bf3f:0	correct

re-plan: tracked-hook-activation-before-provisioning (rows text-security:f4246e9:2; the class that forced the re-slice of design 1) — specification: no slice switches a tracked hook command to a guard path before deployment stage A has installed that guard on the host, so no session that loads the tracked settings loses its stop gate between merges; design: slice 1 renders the guard template and the migration logic only and leaves `.claude/settings.json` untouched; a new slice 5 (`dotfiles-T133-worker-write-boundary-slice5-a01`, after slice 4 and stage A) switches the tracked references with a test that the deployment inventory lists the installed guard; implementation: design 2 of slice 1 (186 lines, 7 paths, sha 3844d937) and the slice5 owner stub; verification: the C-80 of design 2 reports no activation-order finding and the anchor review of another context accepts the redesign bytes.
- 2026-10-21T03:09Z: C-80 of 3844d937 (`…-text-security-3844d93.md`): one P2 at line 137: the text preserves the old Linux four-entry exclusion policy (incl. `gh *`) while its new prerequisite `worker-sandbox-exclusions-a02` empties both platforms and makes the validator reject non-empty lists. Cause: the allocation brief described the baseline as today's main, not the post-prerequisite state; the `after:` edge added at 02:56Z made the conflict visible. Anchor review on 3844d937 withdrawn (PING to a012). Re-plan line below; brief v3; author-loop round on design 2 with the baseline rule.

text-security:3844d93:1	prerequisite-baseline-conflict

re-plan: prerequisite-baseline-conflict (rows text-security:3844d93:1; a baseline statement contradicted the task's own prerequisite) — specification: every baseline-preservation statement and fixture in a slice text binds to the state of main after the slice's `after:` prerequisites have merged, never to the main of the authoring day; design: the brief names each prerequisite's post-merge effect (worker-sandbox-exclusions-a02: both platforms' excludedCommands empty and the validator rejects non-empty lists; pins-a01: the pinned mise declaration) and the text's Design and Check sections cite them; implementation: brief v3 and the re-authored slice 1 text; the rule is added to BRIEF-TEMPLATE-NOTES.md for every later slice; verification: the C-80 of the re-authored text reports no prerequisite-baseline finding and the anchor review of another context accepts the bytes.
- 2026-10-21T03:10Z: anchor review a01 (a012, RESULT 03:07:48Z) rejected 3844d937 with F1 (= the C-80 finding at line 137) and F2 (line 78 says `Keep after: []` against the two edges at line 18). Both go into the brief v3 round: the prose must state the two prerequisites and their post-merge effects, no `after: []` sentence. The next anchor review is `…-redesign-review-a02` on the new sha.
- 2026-10-21T03:33Z: design 2 round 2 (brief v3: baseline bound to the post-prerequisite state; 189 lines, 7 paths): C-80 `…-text-security-0f87501.md` correct; `after:` set to [pins-a01, worker-sandbox-exclusions-a02] and the `Keep after: []` sentence replaced (anchor F2); C-80 of the final bytes e39dc8fb (`…-text-security-e39dc8f.md`) correct. Anchor review a02 dispatched to a012 on e39dc8fb.

text-security:0f87501:0	correct
text-security:e39dc8f:0	correct
- 2026-10-21T09:19Z: prerequisites met (PR #448 e042663b and PR #449 4eafd890 merged; canonical main 4eafd890); Checks pasted (6 lines), bytes now 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9 (194 lines, pre-send OK); re-anchor review `dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a03` sent to a011 (D-024-59); liveness PING to a010 (2984). Dispatch line: preconditions=met:this record, overlap_ok=431,420,406.
- 2026-10-21T09:28Z: re-anchor accepted (a011 RESULT 2987, sha 527f7f9460b694bedb177c81a0713932322cebe28c6ef1b71290fd36468224e9); dispatched to codex-standard-dot-a010 (worker-e, wJ:p5) as bus 2989 (read 09:28:18Z), round 1, fresh branch tools/worker-write-boundary-slice1-a01 from main 4eafd890, preconditions=met (this record), overlap_ok=431,420,406 (own lineage branch; parked permission-guard a03 branch; phase-2 draft). Counters before the send (C-126): a03 TASKs=2 RESULTs=0 questions=0 (S2 silenced by the a03 design-reset record); slice1 all 0. a010 had read PING 2984 without a PONG; the TASK asks for the PONG first.

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

exec
/bin/zsh -lc 'for f in .orchestration/tasks/dotfiles-T133-{trusted-entrypoint-descendants-followup-a01,trusted-entrypoint-binding-a01,agmsg-hardening-a01,worker-write-boundary-slice2-a01,worker-write-boundary-slice3-a01,worker-write-boundary-slice4-a01,worker-write-boundary-slice5-a01,audit-pool-a02,permission-guard-gate-a05}.md; do echo "$f"; sed -n '"'1,85p' \""'$f"; done' in ~/Workspace/dotfiles
 succeeded in 64ms:
.orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md
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
.orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md
---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-binding-a01
kind: code
security: true
allowed_files: ["home/dot_agents/agent-config.yaml","home/.chezmoitemplates/claude-settings-managed.json","home/dot_claude*/modify_private_settings.json","scripts/generate-agent-configs.py","scripts/validate-agent-assets.py","Makefile","tests/unit/test_claude_managed_settings.py","tests/unit/test_validate_agent_assets.py","tests/unit/test_generate_agent_configs.py","scripts/orchestrator/trusted-launch.sh",".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**"]
after: [dotfiles-T133-worker-write-boundary-slice2-a01, dotfiles-T133-ci-efficiency-followup-a04]
rendered_forms: [claude-settings-managed.json, permgate claude]
out_of_scope:
  - {"path":"home/dot_mise/config.toml","reason":"dotfiles-T133-trusted-entrypoint-pins-a01 pins the real declaration before this task is sent; it is read-only here."}
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
  - {"control":"tests/unit/test_generate_agent_configs.py","disposition":"closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_hooks_use_installed_permgate_paths asserts the executable leaf and the permission-request operand from args; the pins refactor rsplit form raises ValueError on the env+args command (pins audit:28dde0f:1)"}
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
.orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md
---
format: 2
task_id: dotfiles-T133-agmsg-hardening-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - home/dot_agents/skills/agmsg/scripts/storage.sh
  - home/dot_agents/skills/agmsg/scripts/drivers/**
  - tests/unit/test_agmsg_hardening.py
  - .orchestration/dotfiles-T133-agmsg-hardening-a01/**
after: [dotfiles-T133-worker-write-boundary-slice4-a01]
owner_of:
  - dotfiles-T133-worker-write-boundary-a01
  - dotfiles-T133-worker-write-boundary-slice1-a01
---

# AGMSG-TASK dotfiles-T133-agmsg-hardening-a01 — owner of agmsg store-driver validation and plugin authorization (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51). The a01 record of the worker-write-boundary lineage already carries a section `## Owned by dotfiles-T133-agmsg-hardening-a01 (a task to be written; upstream agmsg)` with the rows text-security:5cbbc03:2 (store-plugin trust: `storage.sh:208-228` selects and sources a writable, store-selected driver) and its widening; a04 line 594 and slice 1's row "agmsg store driver and plugin selection" name this task. The dispatch text is authored later from an upstream-agmsg brief; this stub is never dispatched. The agmsg scripts live under the user's skills directory, so the final allowed_files follow the upstream layout at dispatch time.

## Scope

Validate the store driver name against a closed allowlist before `storage.sh` sources it; authorize plugins only from a trusted, non-writable location; refuse a writable store-selected driver path; one rejection test per route. The static plugin and trusted-plugin denies that P1-15 renders reduce the exposure meanwhile and are recorded as the compensating control.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice2-a01.md
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
.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice3-a01.md
---
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice3-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - home/.chezmoitemplates/claude-settings-managed.json
  - scripts/validate-agent-assets.py
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_validate_agent_assets.py
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice3-a01/**
after: [dotfiles-T133-worker-write-boundary-slice2-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice3-a01 — P1-15 slice 3: the effective orchestrator settings and validator alignment (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51). The dispatch text is authored by `author-loop.sh` from the allocation brief (slice 3) after slice 2 merges; this stub is never dispatched. `home/dot_claude/modify_private_settings.json` is not reopened here: slice 1 finishes its exact classifier, PreToolUse migration and attachment construction, and this slice consumes that implementation unchanged (the allocation table's reassignment that keeps this list at eight entries).

## Scope (from the allocation table)

Activate the orchestrator baseline, the guarded hooks, the startup-failure policy and the exact ordered three exclusions on both platforms. Change the manifest, the generated output, the validator and their literal expectations together. Preserve every existing validator check and the legacy PermissionRequest bytes and recognition. `make update` reconciliation after Herdr stays explicitly incomplete until slice 4; no deployment occurs between these merges.

## Intermediate condition after merge (E3)

`make render-check`, `make validate-agent-assets` and all six E2 modules pass; required GitHub CI green; final-head review, audit and security evidence fresh.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice4-a01.md
---
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice4-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - Makefile
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - .gitignore
  - tests/unit/test_claude_managed_settings.py
  - tests/unit/test_claude_settings_merge.py
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_agmsg_orchestration_docs.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice4-a01/**
after: [dotfiles-T133-worker-write-boundary-slice3-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice4-a01 — P1-15 slice 4: update and staging, documentation, ignore rules and lineage completion (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51). The dispatch text is authored by `author-loop.sh` from the allocation brief (slice 4) after slice 3 merges; this stub is never dispatched.

## Scope (from the allocation table)

Finish the printed mkdir/install ordering, the fake-update reconciliation, the sandbox-only documentation, the hostile-host template tests and the `.uv-cache/` ignore rule. During the earlier slices cache artifacts stay outside staged changes; the ignore regression becomes mandatory here. Reconcile the lineage and the pending deployment; do not retrospectively supply missing earlier evidence. Preserve the a01/a02/a03 history, the failing a03 draft and the counters. The fresh slice branches replace a04's instruction to continue PR #431; that branch and draft are preserved and #431 is closed only through orchestrator bookkeeping.

## Obligations owned for slice 1

The sandbox-only workflow documentation, the deployment residual and the consolidated residual text that slice 1 defers, and the hostile-host template regressions.

## Intermediate condition after merge (E4)

`make render-check`, `make validate-agent-assets` and all seven complete a04 Check modules pass with the two original unittest command groups, the slice-4 task copy substituted in documentation fixtures; required GitHub CI green; final-head review, audit and security evidence fresh.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice5-a01.md
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
.orchestration/tasks/dotfiles-T133-audit-pool-a02.md
---
format: 2
task_id: dotfiles-T133-audit-pool-a02
kind: code
security: true
allowed_files:
  - scripts/orchestrator/audit-pool.sh
  - scripts/orchestrator/orch-audit.sh
  - .schemas/classes.yaml
  - tests/unit/test_audit_pool.py
  - .orchestration/dotfiles-T133-audit-pool-a02/**
  - tests/unit/trusted_exec_contract.py
after: [dotfiles-T133-worker-write-boundary-slice4-a01]
reset_of: [dotfiles-T133-audit-pool-a01]
threat_table:
  - control: "scripts/orchestrator/audit-pool.sh (trusted execution, frozen requests, queue ownership, physical-slot locks, full-head identities, validated outputs and bounded retries)"
    disposition: "residual: tests/unit/test_audit_pool.py exercises the ten C-80 findings and concurrent subprocess outcomes; the host write boundary mitigates same-user replacement, and killed-pool reservations remain held until explicit trusted cleanup."
  - control: "scripts/orchestrator/orch-audit.sh (verified executable realpaths, pinned Git operations, frozen evidence, differential accounting, extraction and masking)"
    disposition: "residual: tests/unit/test_audit_pool.py::test_orch_audit_executes_only_the_realpaths_verified_against_origin_main and the retained differential and masking regressions exercise consumption boundaries; processes outside every seat sandbox remain a host-level residual."
  - control: ".schemas/classes.yaml (complete controlled vocabulary from JSON and prose ledgers, remedy sentences and blast_radius globs)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_classes_file_holds_every_ledger_class_of_the_records_and_each_has_remedy_and_blast_radius"
  - control: "tests/unit/test_audit_pool.py (retained behavior cases, source-pinned schema shape, complete vocabulary fixture and red-then-green regressions)"
    disposition: "residual: temporary trusted-host fixtures and fake services exercise executable selection, filesystem identity, queue concurrency and evidence binding without live audits or retry delays."
  - control: ".orchestration/dotfiles-T133-audit-pool-a02/** (this reset task's branch artifacts)"
    disposition: "residual: artifacts identify source commits, tested heads, executable realpaths, snapshot hashes, all ten C-80 dispositions and final-head results; inherited evidence never substitutes for this task's validation."
  - control: "tests/unit/trusted_exec_contract.py (shared trusted-host contract fixture helper, created here if absent)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_audit_pool_never_executes_a_shim_first_on_path; tests/unit/test_audit_pool.py::test_audit_pool_ignores_planted_git_environment_and_config; tests/unit/test_audit_pool.py::test_audit_pool_refuses_trusted_paths_under_a_worker_root; tests/unit/test_audit_pool.py::test_audit_pool_never_consumes_a_file_swapped_after_verification"
  - control: "the task-file copies (.orchestration/dotfiles-T133-audit-pool-a02/task.md and .orchestration/dotfiles-T133-audit-pool-a01/task.md)"
    disposition: "residual: the a02 copy is byte-identical to the dispatched text and its own SHA256 is bound by TASK and RESULT; a01 never started or pushed, so the worker creates no a01 copy and deletes no predecessor material."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-audit-pool-a02/ (report.md, validation.md, sandbox.md, learning.md and revise.yaml)"
    disposition: "residual: records distinguish source history, actual red and green executions, refused commands, inherited failures, complete changed-line counts and final-head review evidence."
  - control: task metadata
    disposition: "residual: the orchestrator checks task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; dispatch also requires the exact a02 text to pass C-80."
  - control: metadata separators
    disposition: "residual: the first document separators bound the YAML front matter and byte comparison covers the complete dispatched task copy."
  - control: in-process effects
    disposition: "residual: selection consumes frozen request values under the queue and physical-slot locks; publication and cleanup require unchanged path, inode and content identities."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: sanitized startup, verified absolute executables, Python isolation and pinned Git configuration prevent inherited discovery inputs from selecting code; no workflow or seat-policy change is authorized."
  - control: new or renamed scripts
    disposition: "residual: the pool is the only new production executable, the existing audit wrapper is modified and the shared helper is test-only; the final inventory contains no undeclared production helper."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only after the integration gate with gh pr merge --squash --match-head-commit <audited head>; no local merge or push to main is authorized."
  - control: orchestrator effect update-branch
    disposition: "residual: an updated head receives the required fresh CI, feedback sweep, task-level audit and security review before the integration gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state in acceptance."
  - control: "5.14 item 1 (write boundary, premise 6)"
    disposition: "residual: the unchanged manifest-rendered seat sandbox supplies the write boundary and make render-check supplies rendered-deny evidence before dispatch; D-024-17 owns absolute binding of unsandboxed gh, and this task changes no sandbox policy."
  - control: "5.14 item 2 (sanitized environment first)"
    disposition: "residual: the pool enters env -i before interpreter startup, discovery or child execution and uses verified absolute binaries and pinned Git configuration; tests/unit/test_audit_pool.py::test_audit_pool_never_executes_a_shim_first_on_path and tests/unit/test_audit_pool.py::test_audit_pool_ignores_planted_git_environment_and_config exercise this control."
  - control: "5.14 item 3 (trusted-path boundary checks)"
    disposition: "residual: all trusted paths are realpath-resolved and rejected under worker roots, with case-insensitive identity comparison where required; tests/unit/test_audit_pool.py::test_audit_pool_refuses_trusted_paths_under_a_worker_root exercises direct and symlinked paths."
  - control: "5.14 item 4 (execute verified realpaths and consume verified contents)"
    disposition: "residual: verified executable realpaths are used directly, consumed files have unique 0600 trusted snapshots, recorded SHA256 values are checked before reuse and shadow rows bind compared outputs; tests/unit/test_audit_pool.py::test_audit_pool_never_consumes_a_file_swapped_after_verification exercises replacement between verification and consumption."
  - control: "5.14 item 5 (output and reservation identity)"
    disposition: "residual: full 40-hex heads name requests and outputs, each physical slot has one persistent inode-bound lock created with O_EXCL, and overlapping queues are refused; tests/unit/test_audit_pool.py::test_pool_detects_replaced_lock_inodes_and_frozen_request_changes, tests/unit/test_audit_pool.py::test_pool_refuses_queues_sharing_a_physical_slot_range and tests/unit/test_audit_pool.py::test_pool_uses_full_heads_and_refuses_case_alias_output_collisions exercise these controls."
  - control: "5.14 item 6 (honest residual)"
    disposition: "residual: the final section states the host-boundary residual in one line; fixture success does not claim protection against an unsandboxed same-UID writer or completion of D-024-17."
  - control: "5.14 item 7 (shared verification)"
    disposition: "closed: tests/unit/test_audit_pool.py::test_audit_pool_never_executes_a_shim_first_on_path; tests/unit/test_audit_pool.py::test_audit_pool_ignores_planted_git_environment_and_config; tests/unit/test_audit_pool.py::test_audit_pool_refuses_trusted_paths_under_a_worker_root; tests/unit/test_audit_pool.py::test_audit_pool_never_consumes_a_file_swapped_after_verification"
premises:
  - claim: the a02 branch holds the three implementation and vocabulary files inherited by this sibling
    command: git ls-tree --name-only b8998de162afc72d53d07679b8f0a194fcc480ff scripts/orchestrator/audit-pool.sh scripts/orchestrator/orch-audit.sh .schemas/classes.yaml | wc -l
    output: |-
      3
  - claim: audit-pool.sh and classes.yaml are absent from a clean origin/main checkout before cherry-picking
    command: git ls-files scripts/orchestrator/audit-pool.sh .schemas/classes.yaml | wc -l
    output: |-
      0
  - claim: orch-audit.sh is already tracked on origin/main
    command: git ls-files scripts/orchestrator/orch-audit.sh | wc -l
    output: |-
      1
  - claim: |-
      すべての worker 席は manifest から描画した sandbox の下で動き、書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。
    command: make render-check
    output: |-
      (pasted at dispatch)
---

# AGMSG-TASK dotfiles-T133-audit-pool-a02 — C-80 reset of dotfiles-T133-audit-pool-a01 under D-024-18 (plan 024 P1-4a; seat=a008, worker-f; tools/audit-pool-a02 from origin/main; one PR)

This task resets the audit-pool half split from PR #410. The a01 text failed C-80 with six P1 and four P2 in `.orchestration/validation/dotfiles-T133-audit-pool-a01-text-security.md.last.md`. Every finding is an implementation requirement and regression below.

.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md
---
format: 2
task_id: dotfiles-T133-permission-guard-gate-a05
kind: code
security: true
allowed_files:
  - scripts/permission-guard.py
  - scripts/orchestrator/ruleset-request.sh
  - scripts/orchestrator/ruleset-verify.sh
  - home/dot_claude/hooks/executable_gh-merge-gate.sh
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - scripts/generate-agent-configs.py
  - scripts/validate-agent-assets.py
  - scripts/check-agent-runtime.py
  - home/dot_config/git/config.tmpl
  - tests/unit/test_gh_merge_gate.py
  - tests/unit/test_permission_guard.py
  - tests/unit/test_ruleset_scripts.py
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_validate_agent_assets.py
  - tests/unit/test_check_agent_runtime.py
  - .orchestration/dotfiles-T133-permission-guard-gate-a05/**
  - scripts/orchestrator/integrate-merge.sh
  - scripts/orchestrator/finish-pr.sh
  - scripts/orchestrator/orch-gate.sh
  - tests/unit/test_orch_gate_path.py
  - tests/unit/test_integrate_merge.py
  - tests/unit/test_claude_settings_merge.py
after: [dotfiles-T133-worker-write-boundary-a02]
reset_of: [dotfiles-T133-permission-guard-gate-a04]
threat_table:
  - control: "scripts/permission-guard.py (canonical permission-surface comparison and exact diff SHA256 approval only from git show origin/main:.orchestration/decisions.tsv after fetch in the verified anchored checkout, under D-024-19; working-copy rows and candidate revisions supply no approval authority)"
    disposition: "closed: tests/unit/test_permission_guard.py::PermissionGuardTest::test_guard_reads_the_committed_ledger_never_the_working_copy_or_the_pr_tree"
  - control: "scripts/orchestrator/ruleset-request.sh (expected ruleset 24397953, duplicate-preserving live comparison, unchanged CLI and GET-only access)"
    disposition: "closed: tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_ruleset_comparison_preserves_duplicate_rule_types"
  - control: "scripts/orchestrator/ruleset-verify.sh (comparison result and optional updates of an explicitly selected existing progress ledger only on equality)"
    disposition: "closed: tests/unit/test_ruleset_scripts.py::RulesetScriptsTest::test_progress_is_optional_and_missing_file_is_print_only"
  - control: "home/dot_claude/hooks/executable_gh-merge-gate.sh (only the tracked anchored entrypoint can receive allow; direct gh merge, create and update-branch text always asks)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::GhMergeGateTest::test_gate_asks_for_every_gh_text_form"
  - control: "home/dot_agents/agent-config.yaml (the deployed checkout anchor, synchronous hook source and removal of exactly the three ask rules approved by D-024-14)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask"
  - control: "home/.chezmoitemplates/claude-settings-managed.json (the generated synchronous Bash PreToolUse hook and retained permission rules)"
    disposition: "residual: the existing generator renders this file from the manifest, and make render-check rejects any byte drift."
  - control: "scripts/generate-agent-configs.py (one synchronous Bash PreToolUse command entry rendered from gh_merge_gate_hook)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask"
  - control: "scripts/validate-agent-assets.py (every retained gh write ask rule and the exact synchronous deployed hook entry)"
    disposition: "closed: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_gate_validator_requires_every_retained_ask_rule_and_the_exact_synchronous_hook_entry"
  - control: "scripts/check-agent-runtime.py (the deployed hook's content and executable status)"
    disposition: "closed: tests/unit/test_check_agent_runtime.py::CheckAgentRuntimeTest::test_runtime_check_compares_the_deployed_gh_merge_gate_hook_with_the_source"
  - control: "home/dot_config/git/config.tmpl (removal of the GitHub HTTPS-to-SSH pushinsteadof block)"
    disposition: "residual: the removed block contains no credential, the existing gh credential helper remains, and the operator verifies deployment after make update."
  - control: "tests/unit/test_gh_merge_gate.py (entrypoint identity, exact argv, sanitized checks, trusted tools, gh-text asks, JSON decisions and no-decision cases)"
    disposition: "residual: temporary repositories and synthetic deployed manifests exercise decisions without executing submitted payload text or changing GitHub."
  - control: "tests/unit/test_permission_guard.py (revision fixtures, permission digests, committed origin/main ledgers in temporary anchored checkouts named by deployed manifest fixtures, and forged working-copy and PR-tree rows)"
    disposition: "residual: fixture approvals are committed at origin/main in temporary anchored repositories; uncommitted and PR-tree rows exercise refusal, no external ledger override is used, and the live decision ledger and credentials remain untouched."
  - control: "tests/unit/test_ruleset_scripts.py (GET-only argv capture, duplicate occurrences and optional temporary progress ledgers)"
    disposition: "residual: fake GitHub responses and temporary ledgers preserve the live ruleset and progress records while the audit checks the assertions."
  - control: "tests/unit/test_generate_agent_configs.py (the manifest anchor, rendered synchronous hook and complete retained ask set)"
    disposition: "residual: fixture renders cover supported darwin and linux configurations, and the final-head audit checks the assertions."
  - control: "tests/unit/test_validate_agent_assets.py (independent removal of retained rules and substitution of fake, duplicate or async hook entries)"
    disposition: "residual: fixture settings exercise validation failures without changing deployed settings."
  - control: "tests/unit/test_check_agent_runtime.py (missing, matching, stale and non-executable deployed-hook fixtures)"
    disposition: "residual: a temporary HOME supplies all deployment fixtures, leaving the live runtime untouched."
  - control: ".orchestration/dotfiles-T133-permission-guard-gate-a05/** (this reset's branch artifacts)"
    disposition: "residual: new evidence stays in this directory, separates inherited observations from final-head results and is checked against the diff and CI."
  - control: "scripts/orchestrator/integrate-merge.sh (trusted execution of the gate, final-head security guard, committed-ledger approval, PR checks, pinned squash merge and anchored fast-forward; worker-root trusted paths refuse, and premise 6 retains its Claude-seat residual)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_integrate_merge_binds_gh_and_git_to_the_trusted_root"
  - control: "scripts/orchestrator/finish-pr.sh (tracked finishing glue and publication of validated PR-body bytes through a write-once anchored snapshot rehashed immediately before gh; premise 6 retains its Claude-seat residual)"
    disposition: "closed: tests/unit/test_integrate_merge.py::IntegrateMergeTest::test_finish_pr_passes_a_body_snapshot_never_the_caller_path"
  - control: "tests/unit/test_integrate_merge.py (trusted execution, head mismatch, gate and security refusals, safe fast-forward, publication controls and source- and snapshot-swap fixtures)"
    disposition: "residual: fake binaries capture writes and synthetic files exercise swaps, metadata aliases and evidence failures without merging or publishing anything."
  - control: "scripts/orchestrator/orch-gate.sh (first-action env -i, trusted absolute binaries, explicit Git -C and fixed Git configuration before discovery and across the lines 87-89 environment rebuild; the gate and validator inherit the reconstructed controls)"
    disposition: "closed: tests/unit/test_orch_gate_path.py::OrchGatePathTest::test_orch_gate_sanitizes_the_environment_before_git_discovery"
  - control: "tests/unit/test_orch_gate_path.py (planted environment and Git configuration, discovery ordering, private PATH and validator inheritance through the rebuilt environment)"
    disposition: "residual: temporary repositories and fake binaries capture discovery and descendant environments without changing the live checkout or GitHub."
  - control: "tests/unit/test_claude_settings_merge.py (darwin and linux Bash sandbox renders, seat worktree and scratch/cache allowances, and Bash write denial for trusted paths)"
    disposition: "residual: fixture renders assert only the Bash sandbox policy; Claude file tools, hooks and MCP processes remain outside that sandbox, and the rendered permission policy has no path deny until P1-15 under D-024-17."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-permission-guard-gate-a05/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-permission-guard-gate-a04/task.md)"
    disposition: "residual: the first push deletes the a04 copy and adds the byte-identical dispatched a05 copy; TASK and RESULT carry the a05 copy's SHA256, which the orchestrator verifies at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-permission-guard-gate-a05/ (report.md, validation.md, sandbox.md, learning.md and dry-probe transcripts)"
    disposition: "residual: records retain tested identities and verbatim outputs, distinguish historical evidence from new closure and list refused commands for the audit."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance, and whole-file byte comparison protects the dispatched metadata."
  - control: metadata separators

**Splitting large output**
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T133-trusted-entrypoint-descendants-followup-a01.md .orchestration/tasks/dotfiles-T133-agmsg-hardening-a01.md .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice{2,3,4,5}-a01.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
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
---
format: 2
task_id: dotfiles-T133-agmsg-hardening-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - home/dot_agents/skills/agmsg/scripts/storage.sh
  - home/dot_agents/skills/agmsg/scripts/drivers/**
  - tests/unit/test_agmsg_hardening.py
  - .orchestration/dotfiles-T133-agmsg-hardening-a01/**
after: [dotfiles-T133-worker-write-boundary-slice4-a01]
owner_of:
  - dotfiles-T133-worker-write-boundary-a01
  - dotfiles-T133-worker-write-boundary-slice1-a01
---

# AGMSG-TASK dotfiles-T133-agmsg-hardening-a01 — owner of agmsg store-driver validation and plugin authorization (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51). The a01 record of the worker-write-boundary lineage already carries a section `## Owned by dotfiles-T133-agmsg-hardening-a01 (a task to be written; upstream agmsg)` with the rows text-security:5cbbc03:2 (store-plugin trust: `storage.sh:208-228` selects and sources a writable, store-selected driver) and its widening; a04 line 594 and slice 1's row "agmsg store driver and plugin selection" name this task. The dispatch text is authored later from an upstream-agmsg brief; this stub is never dispatched. The agmsg scripts live under the user's skills directory, so the final allowed_files follow the upstream layout at dispatch time.

## Scope

Validate the store driver name against a closed allowlist before `storage.sh` sources it; authorize plugins only from a trusted, non-writable location; refuse a writable store-selected driver path; one rejection test per route. The static plugin and trusted-plugin denies that P1-15 renders reduce the exposure meanwhile and are recorded as the compensating control.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
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
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice3-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - home/.chezmoitemplates/claude-settings-managed.json
  - scripts/validate-agent-assets.py
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_validate_agent_assets.py
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice3-a01/**
after: [dotfiles-T133-worker-write-boundary-slice2-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice3-a01 — P1-15 slice 3: the effective orchestrator settings and validator alignment (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51). The dispatch text is authored by `author-loop.sh` from the allocation brief (slice 3) after slice 2 merges; this stub is never dispatched. `home/dot_claude/modify_private_settings.json` is not reopened here: slice 1 finishes its exact classifier, PreToolUse migration and attachment construction, and this slice consumes that implementation unchanged (the allocation table's reassignment that keeps this list at eight entries).

## Scope (from the allocation table)

Activate the orchestrator baseline, the guarded hooks, the startup-failure policy and the exact ordered three exclusions on both platforms. Change the manifest, the generated output, the validator and their literal expectations together. Preserve every existing validator check and the legacy PermissionRequest bytes and recognition. `make update` reconciliation after Herdr stays explicitly incomplete until slice 4; no deployment occurs between these merges.

## Intermediate condition after merge (E3)

`make render-check`, `make validate-agent-assets` and all six E2 modules pass; required GitHub CI green; final-head review, audit and security evidence fresh.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
---
format: 2
task_id: dotfiles-T133-worker-write-boundary-slice4-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - Makefile
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - .gitignore
  - tests/unit/test_claude_managed_settings.py
  - tests/unit/test_claude_settings_merge.py
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_agmsg_orchestration_docs.py
  - .orchestration/dotfiles-T133-worker-write-boundary-slice4-a01/**
after: [dotfiles-T133-worker-write-boundary-slice3-a01]
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-slice4-a01 — P1-15 slice 4: update and staging, documentation, ignore rules and lineage completion (owner stub)

Owner stub written 2026-10-21 by the orchestrator seat (C-51). The dispatch text is authored by `author-loop.sh` from the allocation brief (slice 4) after slice 3 merges; this stub is never dispatched.

## Scope (from the allocation table)

Finish the printed mkdir/install ordering, the fake-update reconciliation, the sandbox-only documentation, the hostile-host template tests and the `.uv-cache/` ignore rule. During the earlier slices cache artifacts stay outside staged changes; the ignore regression becomes mandatory here. Reconcile the lineage and the pending deployment; do not retrospectively supply missing earlier evidence. Preserve the a01/a02/a03 history, the failing a03 draft and the counters. The fresh slice branches replace a04's instruction to continue PR #431; that branch and draft are preserved and #431 is closed only through orchestrator bookkeeping.

## Obligations owned for slice 1

The sandbox-only workflow documentation, the deployment residual and the consolidated residual text that slice 1 defers, and the hostile-host template regressions.

## Intermediate condition after merge (E4)

`make render-check`, `make validate-agent-assets` and all seven complete a04 Check modules pass with the two original unittest command groups, the slice-4 task copy substituted in documentation fixtures; required GitHub CI green; final-head review, audit and security evidence fresh.

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

exec
/bin/zsh -lc "rg -n '"'^##|''^###|GIT_|PATH|shim|residual|preflight|closed|snapshot'"' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md; rg --files --hidden .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03 | head -35; rg -n 'scope|PermissionRequest|interpreter|site|shim|residual' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md | head -25" in ~/Workspace/dotfiles
 succeeded in 22ms:
35:    disposition: "residual: the manifest declares the static protected inputs and closed worker-start schema; render tests check their correspondence without establishing same-UID isolation or complete executable binding."
37:    disposition: "residual: the orchestrator baseline retains guarded non-PermissionRequest hooks and the unchanged legacy PermissionRequest command; its execution binding belongs to dotfiles-T133-trusted-entrypoint-binding-a01."
39:    disposition: "residual: dedicated policy retains narrow write grants, static denies, canonical delivery, MCP approval disables and explicit plugin disables; higher-scope inputs also undergo independent screening."
41:    disposition: "residual: the administrative template declares sandbox requirements and the exact shared exceptions; content fixtures do not establish operator installation or live enforcement."
43:    disposition: "residual: exact managed-hook classification replaces owned legacy forms while preserving custom hooks and ordering; repeated merge fixtures check idempotence without proving descendant executable identity."
45:    disposition: "residual: one source-aware closed-schema policy checks existing and prepared inputs before mutation; fixtures establish refusal at startup while later reloads and same-UID replacement remain possible."
47:    disposition: "residual: fixed operations and canonical launch identity suppress worker project payloads; complete interpreter, formatter and descendant binding remains with dotfiles-T133-trusted-entrypoint-binding-a01."
49:    disposition: "residual: every tracked command retains the clean prefix, installed guard, fixed operation and failure policy; portable render fixtures do not establish runtime timeout enforcement."
51:    disposition: "residual: deterministic generation publishes manifest-owned policy without learning accepted keys or executable forms from candidate configuration; generation remains independent of deployment tool availability."
53:    disposition: "residual: existing schema, exclusion, hook and asset checks remain, including legacy PermissionRequest recognition; no new bound-PermissionRequest or deployment checker is introduced."
55:    disposition: "residual: staging prints privileged parent creation and file installation without executing either, and update-tree reconciles Claude settings after the Herdr installer; temporary fixtures check both sequences."
57:    disposition: "residual: all worker-start routes validate the repository anchor and all Claude routes run the same preflight before trust or mutation; no live seat or atomic consumption guarantee is claimed."
59:    disposition: "residual: the Worker Playbook has one sandbox-only command rule and no worker exemptions; documentation fixtures distinguish the retained orchestrator operations."
61:    disposition: "residual: .uv-cache remains ignored without removing either worklog/cache deny pattern; the temporary-checkout ignore fixture checks accidental-publication protection."
63:    disposition: "residual: both-platform fixtures check separate policies, static inventory, closed-schema rendering and canonical commands without claiming live enforcement."
65:    disposition: "residual: retained fixtures cover exact ordered exclusions, malformed variants and legacy permission-hook composition; formatting remains a CI concern."
67:    disposition: "residual: migration and fake-update fixtures check custom-hook preservation, guarded replacement, installer ordering and idempotence without running a live update."
69:    disposition: "residual: temporary roots and fake processes exercise source coverage, input refusals, launch routes and cache delivery without starting workers, plugins or authentication helpers."
71:    disposition: "residual: fixtures read this task's dispatched copy and test the exact sandbox sentence and fixed-host ledger templates without introducing a ledger consumer."
73:    disposition: "residual: render, merge, deny and guard fixtures verify configured policy and unchanged protected bytes without executing a bound PermissionRequest hook."
75:    disposition: "residual: administrative-content and printed-command fixtures use temporary destinations and sudo markers; actual administrative installation remains an operator step."
77:    disposition: "residual: evidence separates inherited observations, new regressions and final-head results, and records pending deployment without credentials or literal operator home paths."
79:    disposition: "residual: S01 is checked before regeneration under the closed settings schema, including every environment entry; a later same-UID replacement remains outside the startup guarantee."
81:    disposition: "residual: S02 includes old tracked settings and is checked without rewriting it; a refusal requires an authorized guarded commit rather than launcher normalization."
83:    disposition: "residual: S03 is inspected before exact legacy migration, so migration cannot conceal helpers, unknown keys or sandbox extensions."
85:    disposition: "residual: S04 is the validated repository's main-local source, independently screened because linked workers consume it; other repository roots refuse before preparation."
87:    disposition: "residual: the Darwin S05 file is screened with the administrative schema through a temporary managed-root fixture; the worker never mutates the system file."
89:    disposition: "residual: the Linux S05 file receives the same administrative schema and source-specific exceptions without claiming live installation."
91:    disposition: "residual: S06 checks each drop-in independently before merging, admitting only canonical administrative fragments and refusing unknown keys or broadened lists."
93:    disposition: "residual: S07 checks an existing cache independently; additional managed delivery that cannot be enumerated before launch produces a named refusal."
95:    disposition: "residual: S08 admits only absent or empty server definitions regardless of trust or approval state, including ignored and untracked files."
97:    disposition: "residual: S09 is checked independently of nearer worktree definitions, so an absent or empty worktree file cannot conceal an inherited server."
99:    disposition: "residual: S10 checks each applicable ancestor file independently without using Git tracking or precedence as an exclusion."
101:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees"
103:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member"
105:    disposition: "residual: S12 includes enterprise skills at <managed-root>/.claude/skills and the other five admitted skills roots, even when the plugin is disabled."
107:    disposition: "residual: S13 accepts only the declared registry shape and contained roots whose descriptors are read; an install record cannot add an unchecked root."
109:    disposition: "residual: S14 permits the declared empty registry only; refresh sources and executable header helpers have no canonical worker form."
111:    disposition: "residual: S15 admits declared descriptive metadata and scalar file references only; every selected file is inspected even for a disabled plugin."
113:    disposition: "residual: S16 covers default and explicitly referenced hook files separately; plugin-owned executable handlers have no canonical worker operation."
115:    disposition: "residual: S17 admits descriptive metadata and an absent or empty plugin list only; command sources and additional plugin selections refuse."
117:    disposition: "residual: S18 checks default and referenced MCP files independently, admitting no nonempty worker server definitions."
119:    disposition: "residual: S19 applies the same empty-server rule independently of managed-settings precedence or administrative ownership."
121:    disposition: "residual: S20 inspects admitted Markdown files and frontmatter without invoking them; unknown frontmatter and inline or fenced dynamic commands refuse."
123:    disposition: "residual: S21 reads every default or scalar-referenced command file; object mappings, inline content and directory references do not bypass Markdown inspection."
125:    disposition: "residual: S22 inspects declared subagent metadata and refuses executable frontmatter without starting a subagent."
127:    disposition: "residual: S23 admits empty LSP configuration only; language-server commands and arguments have no canonical worker operation."
129:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys"
131:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors"
133:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root"
135:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components"
137:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch"
139:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents"
140:  - control: manifest-selected non-shim launch interpreter
141:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names"
143:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment"
145:    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment"
147:    disposition: "residual: explicit false entries supplement screening; higher-scope enables, sync, dependencies, workflows, monitors and undeclared components refuse before launch."
149:    disposition: "residual: unenumerable MDM, server delivery, host settings and caller-selected sources refuse without running a helper to discover their content."
151:    disposition: "residual: source-specific canonical fragments reject extra exclusions, write roots and socket grants before Claude can merge arrays; live enforcement and later changes remain unverified."
153:    disposition: "residual: inventory starts at <managed-root>/.claude/skills, and temporary managed-root fixtures plant both Markdown and bundled plugin payloads there on both platforms."
155:    disposition: "residual: explicit static Edit denies protect the policy input and fixtures assert unchanged bytes; legacy hook environment and execution binding remain deferred."
157:    disposition: "residual: directory-target and descendant denies retain protection for .pth, usercustomize.py and sitecustomize.py without claiming isolated interpreter startup."
159:    disposition: "residual: macOS user-site directory and descendant patterns remain in the static inventory; planted-startup execution belongs to the binding task."
161:    disposition: "residual: the installed guard is an explicitly protected consumed input; routing fixtures do not close concurrent same-UID path swaps."
163:    disposition: "residual: worker and outside-anchor input paths suppress tool execution; formatter availability and complete tool-chain binding remain deferred."
165:    disposition: "residual: retain the predecessor task copy and all a03 evidence unchanged in the declared retained predecessor directory; neither deletion nor new predecessor writes is authorized."
167:    disposition: "residual: the a04 copy is byte-identical to the complete dispatched a04 text and bound by SHA256 in TASK and RESULT."
169:    disposition: "residual: report, validation, sandbox, learning, autoskill and review records preserve commands and identities while distinguishing proposals from acceptance authority."
171:    disposition: "residual: the orchestrator checks reset lineage, scope, counters, finding classes, dispatched bytes and final-head evidence without treating worker proposals as approval."
173:    disposition: "residual: format-2 separators delimit the metadata, and the task-copy digest covers the entire front matter and body."
175:    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no deployment, login, administrative installation or restart."
177:    disposition: "residual: trusted parents supply clean environments and the manifest-named absolute non-shim mise Python runs isolated; role-specific runtime-name screening does not establish complete executable binding."
179:    disposition: "residual: policy stays in the existing renderer, preparation script and guard; no new wrapper, state helper, interpreter resolver or executable-link manager is introduced."
181:    disposition: "residual: host controls reduce accidental and injected damage; shared credentials and same-UID processes prevent a seat-isolation claim."
183:    disposition: "residual: retained write policy and the closed startup schema implement this task's scope; later reloads and consumption races remain outside its guarantee."
185:    disposition: "residual: trusted-parent clean prefixes, fixed operations and declared environment inputs remain mandatory; the legacy orchestrator PermissionRequest and complete executable binding retain their separate owner."
187:    disposition: "residual: canonical root and component containment checks precede startup, including aliases; executable realpath binding remains with the binding task."
189:    disposition: "residual: fixed dispatch avoids candidate-selected execution, while snapshots, last-use digests and complete executable identity remain with their consuming mechanisms."
191:    disposition: "residual: this task introduces no reservation protocol; consuming orchestrator mechanisms retain ownership of full-head outputs and inode-bound locks."
193:    disposition: "residual: the report retains shared credentials, administrative exceptions, socket access, agmsg sourcing, races, reloads and hook-event limitations."
195:    disposition: "residual: retained source-class fixtures and new allowlist regressions supply final-head evidence; shared trusted-execution helper adoption remains with P1-6."
197:    disposition: "residual: fixed-host ledger templates and hostile-host fixtures preserve the contract; P1-14 a05 and P1-6 own actual approval consumption."
199:    disposition: "residual: private worker caches and orchestrator-cache denies remain; exact interpreter declarations, resolver consumption and deployment binding remain separately owned."
201:    disposition: "residual: the Worker Playbook permits no worker escape, while shared administrative capabilities and the operator's Codex permgate deployment remain explicit residuals."
203:    disposition: "residual: both ledger templates explicitly bind github.com and mryfmo/dotfiles; contract tests establish argv binding rather than enforcement by deferred consumers."
205:    disposition: "residual: supported rendered entries retain onFailure block, but background hooks, excluded events and runtime timeout behavior establish no enforcement responsibility."
207:    disposition: "residual: plugin-code and trusted-plugin denies reduce one route; writable store-selected sourcing remains owned by dotfiles-T133-agmsg-hardening-a01."
209:    disposition: "residual: only the orchestrator integrates with final-head evidence and a pinned merge; shared credentials still permit API routes outside the native prefix denials."
211:    disposition: "residual: an update moves the head and requires fresh CI, feedback, local review, audit and security evidence before integration."
213:    disposition: "residual: none is planned; existing dirty-worktree protections remain and any operator-authorized discarded state must be recorded."
231:      runtime-contract-probe.json supplies the exact name lists below. Read-only repetition at 2026-10-20T14:57:54Z produced the same names, exit statuses and spawn digest, without a live worker or private settings. The manifest currently lacks the non-shim interpreter declaration; a04 must add it within its existing launcher policy, not discover it through PATH.
234:      supplied_environment_names: [HOME, LANG, PATH, TERM]
239:          observed_names: [CPATH, HOME, LANG, LIBRARY_PATH, MANPATH, PATH, SDKROOT, TERM, __CF_USER_TEXT_ENCODING]
240:          unlisted_names: [CPATH, LIBRARY_PATH, MANPATH, SDKROOT, __CF_USER_TEXT_ENCODING]
244:          observed_names: [HOME, LANG, PATH, TERM, __CF_USER_TEXT_ENCODING]
260:      D-024-26 retains the write boundary and transfers executable binding. D-024-29 freezes design 5.14; D-024-30 applies it by reference. The 2026-10-20 residual-list entry in this text records the allowlist generalisation without reopening the frozen items.
286:      The single source inventory is S01-S23 below plus executable environment-file contents admitted by the launch-input schema. Each parameter denotes every actual matching file, inspected independently before merging. User means the dedicated configuration directory; managed-root is the platform directory containing managed-settings.json. S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json; S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery; S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration; S12 each skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json; S16 every default hooks/hooks.json and explicitly referenced plugin hook file; S17 every admitted marketplace-root/.claude-plugin/marketplace.json; S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file; S22 every applicable subagent Markdown file; S23 every default or referenced plugin LSP file. Non-file managed delivery and caller-selected inputs must fit the same closed schema and read set or cause a named refusal.
297:## Goal and reset
301:Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Retain every a03 item and fix, with only the runtime/interpreter decision specified here.
307:## History
309:a01 and a02 each exhausted their two worker rounds, and a03 reset the lineage to a closed startup schema while continuing PR #431. Its amendments bound executable environment-file contents, regenerated S11 with screened identity and empty shared project state, and corrected the enterprise skills inventory; those controls and their finding history remain. The worker blocked on shim/platform-added runtime names and upstream `AGMSG_SPAWNED=1`, preserving its uncommitted draft and failing evidence. INV-6's three counted a03 amendments trigger plan 006 S2, so another context authors a04 to resolve only that runtime-name/interpreter contract instead of extending a03.
311:## Design and finding history
313:Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 by reference, including its residual list. D-024-29 keeps items 0-10 frozen; D-024-30 narrows C-88 to exact contract sentences asserted by tests.
321:**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a04:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.
354:## Closed startup schema
360:### Settings and values
384:### Environment and launch arguments
388:The launch-input schema classifies names by source: existing parent/runtime declarations, `regime-declared`, and `platform-injected`. The latter two classes below are closed enumerations, not prefixes. They do not extend settings `env`, configuration-file keys or CLI arguments.
390:The launcher and its startup/preflight Python children use only the manifest-named absolute mise-installed non-shim interpreter, observed here as `<validated-home>/.local/share/mise/installs/python/3.15.0/bin/python3.15`. Add that narrow declaration to the existing manifest-owned launcher policy and consume it through the existing renderer; never route through `/usr/bin/python3`, a mise shim, PATH lookup or an interpreter-discovery fallback. Cover startup bootstrap/home lookup as well as preparation. This selects the interpreter for this boundary without returning the deferred complete binding work to scope.
396:| `HOME`, `PATH`, `LANG`, `TERM` | Validated passwd home; prescribed system-only child PATH; `C.UTF-8`; declared terminal value. Hook children retain `TERM=dumb`. |
401:| `regime-declared`: `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE`, `AGMSG_AGENT_PID` | Retain a03's exact authorities: `0`, validated launcher store selection, declared monitor value and numeric runtime process identifier; unset default-store selection remains supported. |
404:| `HERDR_ENV`, `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_AGENTS_LAYOUT`, `HERDR_SOCKET_PATH` | Validated control-plane identity, `managed` layout and canonical configured socket; these grant no worker sandbox exception. |
410:The read-only amendment-1 probe of the [documented environment variables](https://code.claude.com/docs/en/env-vars) identifies `CLAUDE_ENV_FILE` as the only name admitted above that selects a file whose contents execute: Claude runs its shell contents before Bash commands. No other admitted name has that documented role; `CLAUDE_CODE_SHELL` and `CLAUDE_CODE_SHELL_PREFIX` remain undeclared. Include the named file's contents in the preflight read set alongside S01-S23.
412:For every admitted executable-content file variable, preflight accepts its named file only when absent, empty, or byte-identical to canonical contents generated by the launcher for this start. Inspect without sourcing or executing it; unreadable/nonregular files and any other contents refuse before trust, migration, regeneration, hooks or worker commands with `worker startup refused: <file>: <variable>: noncanonical executable environment file contents`. Preserve refused bytes; never overwrite a planted file to make it pass. After all preflight checks pass, the launcher itself writes the canonical runtime-file contents, records SHA256 bound to the variable, canonical file and this start in existing startup state/evidence, and verifies those bytes before forwarding. Candidate-supplied or prior-start digests cannot authorize contents. Reuse the existing runtime file and startup state; add no sidecar, helper or generated configuration output. Later replacement races and reloads retain their existing residual owners.
418:No shell/interpreter startup or loader override is declared: `BASH_ENV`, `ENV`, `NODE_OPTIONS`, `NODE_PATH`, `PYTHON*`, `LD_*`, `DYLD_*`, shell wrappers and alternate configuration/cache roots refuse as worker inputs. Do not print their values.
422:A clean-parent probe runs through the interpreter named by the rendered manifest, imports the same modules as the predecessor probe, and asserts `CPATH`, `LIBRARY_PATH`, `MANPATH` and `SDKROOT` are absent. They remain undeclared and refuse if encountered; do not delete them to conceal an unexpected injection. Test the observed child environment as well as the parent's proposed names, with child-role-specific declarations.
426:### Sources, roots and component forms
439:| S11 global state | At every start, after all preflight checks pass and before any loader/worker command, write the existing `CLAUDE_CONFIG_DIR/.claude.json` from scratch: `mcpServers: {}`, `projects: {}` and `hasCompletedOnboarding: true`, plus screened identity fields below. The generated file carries no per-project inventory or pre-generated workspace trust. Never merge the previous file into this output. |
451:For S11, every other pre-existing top-level field, including the entire `projects` value and all its contents, `numStartups`, prior onboarding state, tips/changelog caches, project `history`, `allowedTools` and cost counters, is neither screened nor preserved; only syntax/duplicate-key/readability checks apply to the whole input. Discarded objects and arrays are never recursively screened or forwarded. Generate onboarding anew and `projects: {}`, preserve only screened identity values, and reuse the existing atomic writer after the complete preflight; the loader regenerates native state. The anchor's workspace trust is established by the launcher's existing acceptance of the workspace-trust dialog during spawn's readiness wait (`herdr-agents --add-worker` for a Claude worker, documented in the SKILL's 'Regime activation and progress' section). All Claude workers share `CLAUDE_CONFIG_DIR` at `$HOME/.claude-worker`; discarding the prior `projects` value lets sequential sibling starts succeed. A loader requiring another preserved field blocks and retasks rather than widening silently.
455:## Implementation and retained controls
457:1. Keep one preflight over S01-S23, admitted executable environment-file contents and the closed schema. Every Claude route calls it before workspace trust, migration, normalization, regeneration or execution. Enumerate through the filesystem, including ignored/untracked inputs; neither Git tracking nor a nearer definition removes a source. Inspect implicit and selected components separately without executing helpers, installing packages, fetching plugins or starting servers.
463:4. Retain dedicated `CLAUDE_CONFIG_DIR`, both private cache variables on every actual worker route, `AGMSG_RESOLVE_PROJECT=0`, validated `AGMSG_STORAGE_PATH`, canonical attachment identity and `onFailure: "block"` where supported. A writable `run/proj.<pid>.project` cannot replace the explicit project identity. Preserve the a02 absolute Herdr/jq/Node/npm/Codex calls and attachment environment; fixed PATH must not regress attachment or default seating.
473:9. Keep the orchestrator managed PermissionRequest command's existing literal bytes unchanged, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.
475:10. Apply design 5.14 by reference for trusted-parent execution, Python isolation and Git inspection. Consume the manifest-named non-shim interpreter specified above on every launcher startup/preflight Python route; add no resolver, helper, private executable directory, PATH fallback or broader version-pin work. Do not execute arbitrary task-body shell strings as probes.
491:## Regression fixtures
520:| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names` | Execute the predecessor's name-only probe through the absolute non-shim interpreter read from the rendered manifest, with only HOME/PATH/LANG/TERM supplied. Assert CPATH, LIBRARY_PATH, MANPATH and SDKROOT are absent; Darwin permits only the declared platform addition. Route fixtures prove bootstrap, home lookup and preflight use that interpreter without invoking the system shim or PATH fallback. Preserve command/status/name-only JSON. |
530:C11: every `closed` row names one exact `tests/<path>.py::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.
532:## Change budget
576:The source cap remains **1591 = 1111 + 480**; the test cap remains **2528 = 1768 + 760**, including a03 amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. The a04 non-shim interpreter, platform-injected and regime-declared controls fit the existing environment/provider and fixture-alignment increments; no cap increases. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.
582:## Out of scope
584:D-024-26 still assigns exact host-probed uv/Python/Node version declarations and mise pins beyond a04's narrow launch-interpreter selection, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.
586:Keep `home/dot_mise/config.toml`, the installed state-helper source, Codex boundary sources and updater scripts outside scope. No binding-only code returns through shared files. Add no write-boundary Python hook, gh wrapper, credential-directory substitute, installation discovery or PATH fallback.
594:`dotfiles-T133-agmsg-hardening-a01` owns store driver-name validation and plugin authorization. Shared administrative exceptions/socket access, external host processes, same-UID races, later configuration reloads and hook-event limitations remain residuals. Dedicated login state is not imported from the orchestrator or used to discover executable acceptance rules.
598:## Check
614:Retain existing guard, descendant system-PATH/BASH_ENV, migration, custom-hook, native-denial and cache tests. Record the installed Claude version, actual source read sets, documentation observations and any unsupported-version/source refusal without logging credentials. A version mismatch is a blocked PONG requiring re-tasking.
620:## Artifacts, completion and deployment
638:Report user-visible changes: this repository's workers alone are supported; unknown settings or environment inputs refuse; launcher startup uses the manifest-named non-shim mise interpreter, Darwin's optional encoding variable has only the declared shape, and upstream AGMSG_SPAWNED is exactly 1; every start regenerates global state with `projects: {}`, preserves only screened identity and resets native counters/caches/project history/allowedTools; workspace trust uses the launcher's existing spawn-readiness dialog acceptance; alternate providers/authentication selectors refuse; object/inline components refuse; lower-scope sandbox extensions refuse; actual enterprise skills are inspected. Refusal preserves original bytes and names the source without exposing values.
646:The operator logs in with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`, applies the separately prepared deterministic Codex permgate escape-denial change and restarts affected sessions. Inspect installed administrative content, dedicated directory, static denies, stores/caches, all startup sources, closed-schema refusals, MCP/plugin disables, PermissionRequest exception and sandbox startup. Check lower-scope conflicting arrays and report shared capabilities without exposing credentials.
652:## Checks (pasted by the orchestrator before each send)
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/blocked-pong.txt
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/loader-state-probe.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/wip-mask.log
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/blocked-transport.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/red-update-install.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/bus-test-2882-history.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-blocked-preparation.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/red-startup.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-publication.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/red-startup.log
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/bus-test-2882.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/preparation.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/red-update-install.log
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/owner-hold-2697.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/wip-preparation.json
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/bus-test.txt
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/run_check.py
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/autoskill.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/task-send1-5067.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/wip-commit.txt
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/probe_runtime_contract.py
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/implement_policy.py
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/render_selected.py
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/learning.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/probe_loader_state.py
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/worklog/20261020_035552_plan.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/worklog/20261020_035552_todo.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/validation.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/report.md
.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/sandbox.md
9:out_of_scope:
16:  - {"path":"scripts/orchestrator/trusted-interpreter.sh","reason":"The a04 resolver remains read-only for its existing consumers. This re-plan's launcher validates the exact Python declared by its parent-selected manifest; it must not impose the resolver's production-only pin on fixture execution."}
18:  - {"path":"home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","reason":"Complete guard, delivery and formatter/map descendant binding is outside this split; retain its named deployment residuals."}
20:  - {"control":"home/dot_agents/agent-config.yaml","disposition":"residual: Declare exact home-relative uv, Python and node identities and compare their production versions with the read-only mise declaration; deterministic rendering supplies the launcher manifest, while protected inputs still share the OS uid."}
21:  - {"control":"home/.chezmoitemplates/claude-settings-managed.json","disposition":"residual: Render the PermissionRequest exec-form clean prefix with an exact absolute --manifest operand and retain onFailure block; no outer shell starts, but the hook host and first executable's loader environment remain outside launcher validation."}
22:  - {"control":"home/dot_claude/modify_private_settings.json","disposition":"residual: Classify the legacy form separately and compare the bound command string and ordered args array, including --manifest, exactly with the rendered canonical exec form; preserve raw quoting distinctions, custom hooks and idempotence."}
23:  - {"control":"home/dot_claude-worker/modify_private_settings.json","disposition":"residual: Apply the same native expansion and exact bound command/args comparison to this consumer without importing live orchestrator settings or adding an event the surface lacks."}
24:  - {"control":"scripts/generate-agent-configs.py","disposition":"residual: Render exact relative declarations, the launcher manifest data and exec-form command/args without filesystem discovery; ordinary generation and render-check require no installed tools or deployed manifest."}
25:  - {"control":"scripts/validate-agent-assets.py","disposition":"residual: Validate exact rendered command/args and expose the opt-in effective-settings identity check; checker and yaml-importing children consume the same parent-selected manifest, verified uv/Python and private cache without substituting production pins into fixtures."}
26:  - {"control":"Makefile","disposition":"residual: Expose concrete manifest preparation, trusted seed and deployment-check commands and give the formatter the pinned node directory; unrelated inherited recipes remain outside this boundary."}
27:  - {"control":"scripts/orchestrator/trusted-launch.sh","disposition":"residual: Before any declared binary executes, validate the absolute parent-selected manifest and optional fixture root, parse declarations as data, require canonical regular executable paths and compare exact versions; fixture and production inputs use these same checks, while concurrent same-UID replacement remains possible."}
28:  - {"control":"tests/unit/test_claude_managed_settings.py","disposition":"residual: Exercise exact exec-form rendering, migration, a real fixture-manifest uv/Python/permgate execution and the separate pinned-installation case; fixture execution proves the shared launcher path, not production installation or administrative protection."}
29:  - {"control":"tests/unit/test_validate_agent_assets.py","disposition":"residual: Exercise manifest containment, shim, symlink, worker-root and version refusals, quote-preserving comparisons and the clean online seed; recording fake uv cases prove argv and refusal behavior only."}
31:  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**","disposition":"residual: Only task copies, reports, manifest test data and review or validation evidence are authorized; no executable helper or alternative hook may hide under this wildcard."}
32:  - {"control":"task copy .orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/task.md","disposition":"residual: Compare the complete dispatched file byte-for-byte and verify its SHA-256; preserve predecessor copies and the three-review history."}
33:  - {"control":"task metadata","disposition":"residual: Verify identity, both after dependencies, the pin prerequisite and exactly ten allowed_files entries before dispatch and acceptance; the modify-script glob has only its two named consumers."}
34:  - {"control":"metadata separators","disposition":"residual: Parse front matter as data with duplicate keys refused and compare the whole task copy, including both separate task texts and their separators."}
35:  - {"control":"in-process effects","disposition":"residual: Fixture execution writes temporary data and markers only; the effective-settings check is read-only and the worker performs no live deployment."}
36:  - {"control":"workflow and interpreter or environment inputs","disposition":"residual: The trusted parent names the manifest and any fixture root under the clean prefix; launcher discovery, environment overrides and production-only fixture gates are forbidden."}
37:  - {"control":"new or renamed scripts","disposition":"residual: Only the named launcher is added; manifest parsing and exact-path validation stay there, and no second resolver, wrapper executable or artifact-directory runtime helper is introduced."}
38:  - {"control":"orchestrator effect manifest provisioning","disposition":"residual: The operator materializes deterministic production manifest data under the protected repository root before enabling the changed hook; fixture manifests cannot become effective production bindings."}
39:  - {"control":"orchestrator effect merge","disposition":"residual: Only the orchestrator merges the reviewed final head after Playbook step 10; shared credentials remain a bypass risk."}
40:  - {"control":"orchestrator effect update-branch","disposition":"residual: Only the orchestrator updates the branch and refreshes evidence after any head change."}
41:  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; only the orchestrator may remove a worker and must record any discarded state."}
42:  - {"control":"design 5.14 item 0 same-UID model","disposition":"residual: These controls limit accidents and prompt injection; shared credentials and unrestricted same-UID processes remain outside prevention."}

**Reviewing documentation sections**
codex
37 行の threat_table に `closed` の主張はなく、7 件の allowed_files と各非パス制御に対応する行があります。過去の「Linux の `gh *` 除外を残す」「guard 配置前に tracked hook を切り替える」という矛盾は修正されています。今回の追記では GitHub ホストの明示も入り、残る実行先束縛のリスクが既存の保留範囲に収まるかを最終確認しています。
exec
/bin/zsh -lc "rg -n '"'^##|''^###'"' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md; cat .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-blocked-preparation.json" in ~/Workspace/dotfiles
 succeeded in 6ms:
297:## Goal and reset
307:## History
311:## Design and finding history
354:## Closed startup schema
360:### Settings and values
384:### Environment and launch arguments
426:### Sources, roots and component forms
455:## Implementation and retained controls
491:## Regression fixtures
532:## Change budget
582:## Out of scope
598:## Check
620:## Artifacts, completion and deployment
652:## Checks (pasted by the orchestrator before each send)
AGMSG-PONG v1 task_id=dotfiles-T133-worker-write-boundary-a03 status=blocked task_copy=49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b head=c0f50fa1383416240ad28959dbc4635afa777175 worker_fix_rounds=0 independent_pre_push_reviews=0 boundary=undeclared-required-runtime-environment-names command=/usr/bin/python3_-I_.orchestration/dotfiles-T133-worker-write-boundary-a03/probe_runtime_contract.py command_exit=0 test_exit=1 reason=clean-parent-supplies-only-HOME/PATH/LANG/TERM-but-/usr/bin/python3-child-adds-CPATH/LIBRARY_PATH/MANPATH/SDKROOT/__CF_USER_TEXT_ENCODING-and-mise3.15-adds-__CF_USER_TEXT_ENCODING;none-are-in-the-declared-launch-schema;upstream-spawn.sh:527-also-always-exports-AGMSG_SPAWNED=1-before-the-worker-CLI-and-that-name-is-undeclared;task-requires-block-and-retask-for-new-runtime-names note=public-scripts-and-synthetic-name-only-probes-no-live-worker-or-credentials;the-draft-strict-screen-currently-refuses-these-names;green-new.log-is-an-explicit-failing-draft-not-release-evidence;do-not-treat-as-RESULT;source/test-draft-retained-uncommitted;no-local-wildcard-or-allowlist-widening;owner2751-managed-skills-green-baseline-disposition-recorded evidence=.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json,.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log report=.orchestration/dotfiles-T133-worker-write-boundary-a03/report.md next_action=owner-bind-runtime-name-and-child-role-contract-in-reviewed-task-or-provide-an-allowed-clean-boot-route-without-undeclared-variables
{
  "python_probes": [
    {
      "command": [
        "/usr/bin/python3",
        "-I",
        "-c",
        "import os,json,pathlib,platform,pwd,tempfile,subprocess;print(json.dumps(sorted(os.environ)))"
      ],
      "supplied_environment_names": [
        "HOME",
        "LANG",
        "PATH",
        "TERM"
      ],
      "exit": 0,
      "stdout": "[\"CPATH\", \"HOME\", \"LANG\", \"LIBRARY_PATH\", \"MANPATH\", \"PATH\", \"SDKROOT\", \"TERM\", \"__CF_USER_TEXT_ENCODING\"]\n",
      "stderr": "python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead\n",
      "unlisted_names": [
        "CPATH",
        "LIBRARY_PATH",
        "MANPATH",
        "SDKROOT",
        "__CF_USER_TEXT_ENCODING"
      ]
    },
    {
      "command": [
        "~/.local/share/mise/installs/python/3.15.0/bin/python3.15",
        "-I",
        "-c",
        "import os,json,pathlib,platform,pwd,tempfile,subprocess;print(json.dumps(sorted(os.environ)))"
      ],
      "supplied_environment_names": [
        "HOME",
        "LANG",
        "PATH",
        "TERM"
      ],
      "exit": 0,
      "stdout": "[\"HOME\", \"LANG\", \"PATH\", \"TERM\", \"__CF_USER_TEXT_ENCODING\"]\n",
      "stderr": "",
      "unlisted_names": [
        "__CF_USER_TEXT_ENCODING"
      ]
    }
  ],
  "upstream_spawn_sha256": "57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731",
  "upstream_spawn_read_only": true,
  "upstream_lines": [
    {
      "line": 527,
      "text": "  echo 'export AGMSG_SPAWNED=1'"
    },
    {
      "line": 585,
      "text": "      printf '%s%s' \"$MSYS_GUARD\" \"$CLI_BIN\""
    },
    {
      "line": 796,
      "text": "  new_id=\"$(terminal_spawn \"$NAME\" \"$PROJECT\" \"$target\" \"$BOOT\")\" || rc=$?"
    },
    {
      "line": 873,
      "text": "  _id=\"$(terminal_spawn \"$NAME\" \"$PROJECT\" \"$target\" \"$BOOT\")\" \\"
    }
  ],
  "schema_has_AGMSG_SPAWNED": false,
  "live_worker": false,
  "private_settings_read": false
}
{
  "status": "partial-unreviewed-draft-not-release",
  "head": "c0f50fa1383416240ad28959dbc4635afa777175",
  "comparison_base": "118daafa4610549d3bc280800cf8b1d36fb851dc",
  "historical_base": "51ba580149fcace54a912358e7e87c5b07cd8760",
  "source_total": 1339,
  "test_total": 1992,
  "source_cap": 1591,
  "test_cap": 2528,
  "source_rows": [
    {
      "path": ".claude/settings.json",
      "additions": 32,
      "deletions": 64,
      "changed": 96
    },
    {
      "path": ".gitignore",
      "additions": 1,
      "deletions": 0,
      "changed": 1
    },
    {
      "path": "Makefile",
      "additions": 7,
      "deletions": 0,
      "changed": 7
    },
    {
      "path": "home/dot_agents/agent-config.yaml",
      "additions": 77,
      "deletions": 10,
      "changed": 87
    },
    {
      "path": "home/dot_agents/skills/agmsg-orchestration/SKILL.md",
      "additions": 6,
      "deletions": 4,
      "changed": 10
    },
    {
      "path": "home/dot_claude-worker/modify_private_settings.json",
      "additions": 595,
      "deletions": 0,
      "changed": 595
    },
    {
      "path": "home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl",
      "additions": 65,
      "deletions": 0,
      "changed": 65
    },
    {
      "path": "home/dot_claude/modify_private_settings.json",
      "additions": 89,
      "deletions": 31,
      "changed": 120
    },
    {
      "path": "home/dot_local/bin/common/executable_herdr-agents",
      "additions": 121,
      "deletions": 37,
      "changed": 158
    },
    {
      "path": "scripts/generate-agent-configs.py",
      "additions": 190,
      "deletions": 1,
      "changed": 191
    },
    {
      "path": "scripts/validate-agent-assets.py",
      "additions": 2,
      "deletions": 7,
      "changed": 9
    }
  ],
  "test_rows": [
    {
      "path": "tests/unit/test_agmsg_orchestration_docs.py",
      "additions": 96,
      "deletions": 8,
      "changed": 104
    },
    {
      "path": "tests/unit/test_claude_managed_settings.py",
      "additions": 99,
      "deletions": 0,
      "changed": 99
    },
    {
      "path": "tests/unit/test_claude_settings_merge.py",
      "additions": 248,
      "deletions": 10,
      "changed": 258
    },
    {
      "path": "tests/unit/test_claude_worker_settings.py",
      "additions": 310,
      "deletions": 0,
      "changed": 310
    },
    {
      "path": "tests/unit/test_generate_agent_configs.py",
      "additions": 92,
      "deletions": 11,
      "changed": 103
    },
    {
      "path": "tests/unit/test_herdr_agents.py",
      "additions": 1079,
      "deletions": 24,
      "changed": 1103
    },
    {
      "path": "tests/unit/test_validate_agent_assets.py",
      "additions": 12,
      "deletions": 3,
      "changed": 15
    }
  ],
  "generated_exclusions": [
    "home/.chezmoitemplates/claude-worker-settings.json",
    "home/.chezmoitemplates/claude-managed-settings.json",
    "home/.chezmoitemplates/claude-settings-managed.json"
  ],
  "current_measurement": {
    "label": "current_numstat",
    "command": "/usr/bin/env -i GIT_NO_LAZY_FETCH=1 GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null /opt/homebrew/bin/git --git-dir='~/Workspace/dotfiles/.claude/worktrees/worker-e/.git' --work-tree='~/Workspace/dotfiles/.claude/worktrees/worker-e' -C '~/Workspace/dotfiles/.claude/worktrees/worker-e' -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always -c submodule.recurse=false -c core.attributesFile=/dev/null -c core.sshCommand=false --no-pager diff --no-ext-diff --no-textconv --ignore-submodules=all --numstat 118daafa4610549d3bc280800cf8b1d36fb851dc",
    "chunk_id": "aa34c5",
    "wall_time_seconds": 0.251032791,
    "exit_code": 0,
    "original_token_count": 257,
    "output": "32\t64\t.claude/settings.json\n1\t0\t.gitignore\n1115\t0\t.orchestration/dotfiles-T133-worker-write-boundary-a02/task.md\n7\t0\tMakefile\n25\t0\thome/.chezmoitemplates/claude-managed-settings.json\n19\t12\thome/.chezmoitemplates/claude-settings-managed.json\n168\t0\thome/.chezmoitemplates/claude-worker-settings.json\n77\t10\thome/dot_agents/agent-config.yaml\n6\t4\thome/dot_agents/skills/agmsg-orchestration/SKILL.md\n595\t0\thome/dot_claude-worker/modify_private_settings.json\n65\t0\thome/dot_claude/hooks/executable_orchestrator-only.sh.tmpl\n89\t31\thome/dot_claude/modify_private_settings.json\n121\t37\thome/dot_local/bin/common/executable_herdr-agents\n190\t1\tscripts/generate-agent-configs.py\n2\t7\tscripts/validate-agent-assets.py\n96\t8\ttests/unit/test_agmsg_orchestration_docs.py\n99\t0\ttests/unit/test_claude_managed_settings.py\n248\t10\ttests/unit/test_claude_settings_merge.py\n310\t0\ttests/unit/test_claude_worker_settings.py\n92\t11\ttests/unit/test_generate_agent_configs.py\n1079\t24\ttests/unit/test_herdr_agents.py\n12\t3\ttests/unit/test_validate_agent_assets.py\n"
  },
  "historical_measurement": {
    "label": "historical_numstat",
    "command": "/usr/bin/env -i GIT_NO_LAZY_FETCH=1 GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null /opt/homebrew/bin/git --git-dir='~/Workspace/dotfiles/.claude/worktrees/worker-e/.git' --work-tree='~/Workspace/dotfiles/.claude/worktrees/worker-e' -C '~/Workspace/dotfiles/.claude/worktrees/worker-e' -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always -c submodule.recurse=false -c core.attributesFile=/dev/null -c core.sshCommand=false --no-pager diff --no-ext-diff --no-textconv --ignore-submodules=all --numstat 51ba580149fcace54a912358e7e87c5b07cd8760",
    "chunk_id": "eb6609",
    "wall_time_seconds": 0.274602708,
    "exit_code": 0,
    "original_token_count": 1052,
    "output": "32\t64\t.claude/settings.json\n1\t0\t.gitignore\n4\t0\t.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/autoskill.md\n4\t0\t.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/learning.md\n79\t0\t.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/report.md\n15\t0\t.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/revise.yaml\n28\t0\t.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/sandbox.md\n94\t0\t.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/task.md\n2534\t0\t.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/validation.md\n3\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a05/autoskill.md\n5\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a05/learning.md\n38\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a05/report.md\n22\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a05/sandbox.md\n71\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a05/task.md\n155\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a05/validation.md\n28\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/a05-gh-calls.md\n9\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/learning.md\n63\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/report.md\n11\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/revise.yaml\n15\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/sandbox.md\n57\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/task.md\n158\t0\t.orchestration/dotfiles-T128-chain-review-scripts-followup-a06/validation.md\n30\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/dotfiles-T129-assets-omp-hcom-followup-a04-worker-crit.json\n21\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/dotfiles-T129-assets-omp-hcom-followup-a04-worker-review-receipt.md\n10\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/learning.md\n52\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/report.md\n12\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/revise.yaml\n27\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/sandbox.md\n63\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/task.md\n288\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a04/validation.md\n37\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a05/dotfiles-T129-assets-omp-hcom-followup-a05-worker-crit.json\n17\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a05/dotfiles-T129-assets-omp-hcom-followup-a05-worker-review-receipt.md\n13\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a05/learning.md\n46\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a05/report.md\n28\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a05/sandbox.md\n57\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a05/task.md\n295\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-followup-a05/validation.md\n1115\t0\t.orchestration/dotfiles-T133-worker-write-boundary-a02/task.md\n7\t0\tMakefile\n25\t0\thome/.chezmoitemplates/claude-managed-settings.json\n19\t12\thome/.chezmoitemplates/claude-settings-managed.json\n168\t0\thome/.chezmoitemplates/claude-worker-settings.json\n77\t10\thome/dot_agents/agent-config.yaml\n6\t4\thome/dot_agents/skills/agmsg-orchestration/SKILL.md\n595\t0\thome/dot_claude-worker/modify_private_settings.json\n65\t0\thome/dot_claude/hooks/executable_orchestrator-only.sh.tmpl\n89\t31\thome/dot_claude/modify_private_settings.json\n121\t37\thome/dot_local/bin/common/executable_herdr-agents\n190\t1\tscripts/generate-agent-configs.py\n1\t0\tscripts/lint-comparisons-baseline.tsv\n3\t1\tscripts/orchestrator/local-advisory.sh\n12\t2\tscripts/orchestrator/resolve-threads.sh\n2\t7\tscripts/validate-agent-assets.py\n96\t8\ttests/unit/test_agmsg_orchestration_docs.py\n47\t2\ttests/unit/test_chain_github_scripts.py\n23\t0\ttests/unit/test_chain_review_scripts.py\n99\t0\ttests/unit/test_claude_managed_settings.py\n248\t10\ttests/unit/test_claude_settings_merge.py\n310\t0\ttests/unit/test_claude_worker_settings.py\n92\t11\ttests/unit/test_generate_agent_configs.py\n1079\t24\ttests/unit/test_herdr_agents.py\n21\t4\ttests/unit/test_update_agent_assets.py\n12\t3\ttests/unit/test_validate_agent_assets.py\n"
  },
  "tracked_status": {
    "label": "status",
    "command": "/usr/bin/env -i GIT_NO_LAZY_FETCH=1 GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null /opt/homebrew/bin/git --git-dir='~/Workspace/dotfiles/.claude/worktrees/worker-e/.git' --work-tree='~/Workspace/dotfiles/.claude/worktrees/worker-e' -C '~/Workspace/dotfiles/.claude/worktrees/worker-e' -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always -c submodule.recurse=false -c core.attributesFile=/dev/null -c core.sshCommand=false status --short --untracked-files=no",
    "chunk_id": "d49588",
    "wall_time_seconds": 0.174297708,
    "exit_code": 0,
    "original_token_count": 80,
    "output": " M Makefile\n M home/dot_agents/agent-config.yaml\n M home/dot_claude-worker/modify_private_settings.json\n M home/dot_local/bin/common/executable_herdr-agents\n M scripts/generate-agent-configs.py\n M tests/unit/test_claude_managed_settings.py\n M tests/unit/test_claude_settings_merge.py\n M tests/unit/test_herdr_agents.py\n"
  },
  "dispatch_command": "~/.local/bin/common/agmsg-dispatch dotfiles-conformance codex-standard-dot-a010 claude-deep-dot wJ:p1 'AGMSG-PONG v1 task_id=dotfiles-T133-worker-write-boundary-a03 status=blocked task_copy=49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b head=c0f50fa1383416240ad28959dbc4635afa777175 worker_fix_rounds=0 independent_pre_push_reviews=0 boundary=undeclared-required-runtime-environment-names command=/usr/bin/python3_-I_.orchestration/dotfiles-T133-worker-write-boundary-a03/probe_runtime_contract.py command_exit=0 test_exit=1 reason=clean-parent-supplies-only-HOME/PATH/LANG/TERM-but-/usr/bin/python3-child-adds-CPATH/LIBRARY_PATH/MANPATH/SDKROOT/__CF_USER_TEXT_ENCODING-and-mise3.15-adds-__CF_USER_TEXT_ENCODING;none-are-in-the-declared-launch-schema;upstream-spawn.sh:527-also-always-exports-AGMSG_SPAWNED=1-before-the-worker-CLI-and-that-name-is-undeclared;task-requires-block-and-retask-for-new-runtime-names note=public-scripts-and-synthetic-name-only-probes-no-live-worker-or-credentials;the-draft-strict-screen-currently-refuses-these-names;green-new.log-is-an-explicit-failing-draft-not-release-evidence;do-not-treat-as-RESULT;source/test-draft-retained-uncommitted;no-local-wildcard-or-allowlist-widening;owner2751-managed-skills-green-baseline-disposition-recorded evidence=.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json,.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log report=.orchestration/dotfiles-T133-worker-write-boundary-a03/report.md next_action=owner-bind-runtime-name-and-child-role-contract-in-reviewed-task-or-provide-an-allowed-clean-boot-route-without-undeclared-variables'",
  "dispatch": {
    "chunk_id": "e5ca48",
    "wall_time_seconds": 0,
    "exit_code": 1,
    "original_token_count": 34,
    "output": "Error: Os { code: 1, kind: PermissionDenied, message: \"Operation not permitted\" }\nagmsg-dispatch: pane not found or unavailable: wJ:p1\n"
  },
  "history_after_failure": {
    "label": "history",
    "command": "~/.agents/skills/agmsg/scripts/history.sh dotfiles-conformance codex-standard-dot-a010 5",
    "chunk_id": "12eef3",
    "wall_time_seconds": 0.811223917,
    "exit_code": 0,
    "original_token_count": 1262,
    "output": "  ○ [2026-10-20T04:00:43Z] codex-standard-dot-a010 → claude-deep-dot: AGMSG-PONG v1 task_id=dotfiles-T133-worker-write-boundary-a03 status=blocked head=c0f50fa1383416240ad28959dbc4635afa777175 task_copy=5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669 worker_fix_rounds=0 independent_pre_push_reviews=0 boundary=exhaustive-S11-versus-required-native-loader-state command=/usr/bin/python3_-I_.orchestration/dotfiles-T133-worker-write-boundary-a03/probe_loader_state.py command_exit=0 installed_claude=2.1.300 loader_sha256=475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3 reason=task-S11-allows-only-mcpServers/projects-but-public-installed-loader-defaults-numStartups(offset197319096),global-config-writer(offset197329984),and-startup-increment(offset213585566)-persist-numStartups;onboarding-also-writes-hasCompletedOnboarding;exact-schema-would-refuse-native-state-on-next-ordinary-start;per-task-if-loader-requires-another-state-field-block-and-retask-not-silently-widen note=static-binary-read-only-inference-no-private-settings-or-auth-inspection-no-live-session;specified-c0f50fa1-fast-forward-exit0-with-packed-refs-warning-preserved;tracked-tree-clean;no-production-test-edit-push-or-predecessor-deletion report=.orchestration/dotfiles-T133-worker-write-boundary-a03/report.md validation=.orchestration/dotfiles-T133-worker-write-boundary-a03/validation.md sandbox=.orchestration/dotfiles-T133-worker-write-boundary-a03/sandbox.md evidence=.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/loader-state-probe.json exact_preparation=.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/preparation.json next_action=owner-amend-native-global-state-field-and-value-contract-or-change-runtime-requirement\n  ○ [2026-10-20T04:11:06Z] claude-deep-dot → codex-standard-dot-a010: AGMSG-PING v1 task_id=dotfiles-T133-worker-write-boundary-a03 reason=hold:your-blocked-PONG-2694-is-read;the-orchestrator-reproduced-the-loader-probe(sha256-475517ca…,2.1.300);owner-amendment-2-in-preparation(D-024-34:launcher-generated-global-state-file,refusal-only-for-declared-structure-violations);an-AGMSG-TASK-amendment-with-a-new-task_sha256-follows-after-its-C-80-review;no-action-until-then\n  ○ [2026-10-20T05:02:21Z] claude-deep-dot → codex-standard-dot-a010: AGMSG-TASK v1 task_id=dotfiles-T133-worker-write-boundary-a03 round=1 reset_of=dotfiles-T133-worker-write-boundary-a02 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md task_sha256=49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b deadline=none done_signal=AGMSG-RESULT note=a010:amendments-2-4(previous_sha256=5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669;answers-your-blocked-PONG-2694:D-024-34-the-global-state-file-is-launcher-generated-at-every-start,D-024-35-with-no-per-project-inventory(projects-regenerated-empty,trust-via-the-launcher's-dialog-acceptance),the-enterprise-skills-root-is-<managed-root>/.claude/skills;C-80:49161bc-correct;pre-send:checker-OK,SECRET_PATTERN-0,home-paths-0;update-the-task-copy-byte-identical-and-start-the-implementation-per-the-text)\n  ○ [2026-10-20T05:08:10Z] codex-standard-dot-a010 → claude-deep-dot: AGMSG-PONG v1 task_id=dotfiles-T133-worker-write-boundary-a03 status=working head=c0f50fa1383416240ad28959dbc4635afa777175 task_copy=49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b worker_fix_rounds=0 independent_pre_push_reviews=0 stage=tests-first-red-complete note=amendments2-4-full-diff-and-SHA-verified;new-state-provider-root-component-env-file-and-schema-regressions-are-valid-assertion-RED-at-immutable-c0-production;printed-parent-and-post-Herdr-update-both-RED;managed-skills-selector-is-already-GREEN-in-all4-Darwin/Linux-Markdown/plugin-cases-because-c0-already-inventories-managed/.claude/skills-correctly;no-artificial-failing-fixture-will-be-added;please-disposition-that-required-RED-as-retained-baseline-coverage-under-amendment4;continuing-independent-authorized-closed-schema-implementation evidence=.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/red-startup.log,.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/red-update-install.log\n  ○ [2026-10-20T06:01:34Z] claude-deep-dot → codex-standard-dot-a010: AGMSG-PING v1 task_id=dotfiles-T133-worker-write-boundary-a03 reason=owner-disposition-for-your-PONG-2744(managed-skills-selector-already-green-at-c0f50fa1):accepted-as-retained-baseline-coverage-under-amendment-4;no-artificial-failing-fixture;the-selector-named-in-the-row-stays-as-the-row's-test(green-at-c0,green-after),report.md-states-that-the-amendment-4-finding-was-a-text-inventory-error(the-text-said-managed-root/skills)while-c0-already-inventories-managed-root/.claude/skills,with-the-four-Darwin/Linux-Markdown/plugin-cases-pasted;the-red-then-green-requirement-applies-to-the-rows-whose-control-is-new(state-provider,root-component,env-file,schema);recorded-in-the-acceptance-record;continue\n"
  },
  "pong_observed_in_history": false,
  "worker_fix_rounds": 0,
  "independent_pre_push_reviews": 0
}

exec
/bin/zsh -lc "sed -n '275,480p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
    sources: ["https://code.claude.com/docs/en/skills", ".orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md"]
  - claim: "Worker a010 blocked before any edit (PONG 2694, 2026-10-20T04:00:43Z): the loader persists numStartups at start and hasCompletedOnboarding at onboarding; the orchestrator reproduced the installed-loader probe below, not a live worker start."
    sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md]
    probe: {executed_by: review-profile-author, executed_at: "2026-10-20T14:57:54Z", loader: "$HOME/.local/share/mise/installs/npm-anthropic-ai-claude-code/2.1.300/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe", format_observed: Mach-O arm64}
    executed_commands:
      - {command: 'shasum -a 256 <loader>', output: '475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3  <loader>'}
      - {command: '<loader> --version', output: '2.1.300 (Claude Code)'}
      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o numStartups <loader>', output: '12'}
      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o hasCompletedOnboarding <loader>', output: '15'}
    quoted_string_probes: [{command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"numStartups"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasCompletedOnboarding"'' <loader>', output: '0'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasTrustDialogAccepted"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"oauthAccount"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"mcpServers"'' <loader>', output: '29'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"enabledMcpjsonServers"'' <loader>', output: '5'}]
  - claim: >-
      The single source inventory is S01-S23 below plus executable environment-file contents admitted by the launch-input schema. Each parameter denotes every actual matching file, inspected independently before merging. User means the dedicated configuration directory; managed-root is the platform directory containing managed-settings.json. S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json; S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery; S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration; S12 each skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json; S16 every default hooks/hooks.json and explicitly referenced plugin hook file; S17 every admitted marketplace-root/.claude-plugin/marketplace.json; S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file; S22 every applicable subagent Markdown file; S23 every default or referenced plugin LSP file. Non-file managed delivery and caller-selected inputs must fit the same closed schema and read set or cause a named refusal.
    sources:
      - https://code.claude.com/docs/en/settings
      - https://code.claude.com/docs/en/managed-settings
      - https://code.claude.com/docs/en/server-managed-settings
      - https://code.claude.com/docs/en/plugins/manifest-reference
      - https://code.claude.com/docs/en/skills
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-a04 — plan 024 P1-15; worker startup screen; seat a010

## Goal and reset

[memory:decision] Reset a03 under INV-6 and plan 006 S2 through this separate review-profile authoring context. Worker a010 is Codex, security profile, in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`; this task changes Claude's boundary and preserves Codex policy. Continue `tools/worker-write-boundary-a01` and PR #431 from `c0f50fa1383416240ad28959dbc4635afa777175`, keeping the uncommitted a03 draft and all predecessor evidence; open no second PR.

Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Retain every a03 item and fix, with only the runtime/interpreter decision specified here.

[memory:failure] a01 and a02 each spent two worker rounds; a03's blocked PONG reports zero worker correction rounds and zero independent pre-push reviews, while its amendment history remains counted. This reset supplies a04 at most two worker correction rounds in total, including pre-push corrections, and at most one independent pre-push review; it erases no predecessor counters or findings.

The retained draft is not approved, and its `raw/green-new.log` is explicitly failing. The c0f50fa1 local chain stopped before its task-level audit. Obtain new final-head audit and security evidence; do not describe either as inherited.

## History

a01 and a02 each exhausted their two worker rounds, and a03 reset the lineage to a closed startup schema while continuing PR #431. Its amendments bound executable environment-file contents, regenerated S11 with screened identity and empty shared project state, and corrected the enterprise skills inventory; those controls and their finding history remain. The worker blocked on shim/platform-added runtime names and upstream `AGMSG_SPAWNED=1`, preserving its uncommitted draft and failing evidence. INV-6's three counted a03 amendments trigger plan 006 S2, so another context authors a04 to resolve only that runtime-name/interpreter contract instead of extending a03.

## Design and finding history

Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 by reference, including its residual list. D-024-29 keeps items 0-10 frozen; D-024-30 narrows C-88 to exact contract sentences asserted by tests.

Item 1 applies to dedicated worker settings, static input-derived write protection and refusal before startup.
Item 2 applies to trusted-parent execution, clean environments and fixed command selection.
Item 3 applies to canonical anchor, worktree and component identities before consumption.
Item 8 applies to committed approval authority through explicitly host-bound repository API calls.
Item 9 applies to private caches and the trusted parent's interpreter/cache inputs.

**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a04:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.

Read the full a02 and a03 acceptance records, a03 task, blocked PONG and both runtime evidence files, and both c0f50fa1 reviews named in `premises:`. Retain the following history and finding classes in the a04 report and acceptance lineage:

| Finding | Class | Required treatment |
| --- | --- | --- |
| `text-security:2ae9e2c:1` | input-inventory | Project `.mcp.json` remains independently screened. |
| `text-security:ebbb71b:1` | input-inventory | Skills-directory plugins remain inventoried even when disabled. |
| `text-security:ebbb71b:2` | input-inventory | Dedicated global state regenerates `mcpServers: {}` and `projects: {}`; native project entries are discarded. |
| `text-security:ebbb71b:3` | repository-binding | Canonical main comes from the fixed repository API. |
| `text-security:b2a186e:1` | input-inventory | Inspect handler type before command; non-command types refuse. |
| `text-security:b2a186e:2` | repository-binding | Both ledger calls bind `--hostname github.com`. |
| `text-security:ac9ce14:0` | correct | Historical text approval only; it does not approve a04. |
| a02 independent pre-push review | input-inventory | Retain fixes for `env.HOME` guard selection and fenced dynamic commands. |
| `local:79ea98a:1` | tool-environment | Retain manifest-generated `--advisor fable` acceptance. |
| `local:79ea98a:2` | tool-environment | Retain absolute tool paths and attachment identity environment. |
| `local:79ea98a:3-4` | partial-fix | Retain custom-hook preservation and legacy PreToolUse migration. |
| `security:c0f50fa:1` | input-inventory | Refuse undeclared credential-chain/provider selectors. |
| `security:c0f50fa:2` | input-inventory | Refuse worker starts for repositories other than the validated anchor. |
| `security:c0f50fa:3` | input-inventory | Refuse object and inline plugin/command components. |
| `local:c0f50fa:1` | tool-environment | Inventory enterprise skills under the actual managed root. |
| `local:c0f50fa:2` | tool-environment | Reject lower-scope sandbox extensions before array merging. |
| `local:c0f50fa:3-4` | partial-fix | Fix printed parent creation and post-installer reconciliation here. |
| `text-security:f7af699:1` | input-inventory | Admit executable environment-file contents only when absent, empty or launcher-generated for this start. |
| `worker:5067ed0:1`, `text-security:efa211d:1` | input-inventory | Regenerate S11 at every start with `projects: {}` and screened identity; discard native persisted state, including every project's state, and use the launcher's existing spawn-readiness trust-dialog acceptance. |
| `text-security:be969e3:1` | input-inventory | Inventory enterprise skills and plant both Markdown and bundled plugin fixtures under `<managed-root>/.claude/skills`, following the C-87 documented table and pinned-loader probe. |

S1 first triggered on the three source omissions in 2ae9e2c/ebbb71b. The re-plan enumerated S01-S23, but subsequent findings still exploited open field/value acceptance; the c0f50fa1 security findings bring that post-re-plan family to its sixth finding. This reset changes the approach rather than adding three more denylist entries.

Preserve the advisory-owner history and owner `dotfiles-T133-worker-write-boundary-followup-a01` exactly as history. The two c0f50fa1 P2 fixes are retained from a03 by this text; the orchestrator reconciles their owner rows and updates dependent task references. The worker edits no canonical acceptance or owner task.

Retain D-024-26's transferred binding findings, including `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. Do not relabel them as fixed.

## Closed startup schema

Declare this schema in `home/dot_agents/agent-config.yaml` and expose it through the existing renderer/preparation code. Candidate files, Git objects and installed upstream schemas never define their own acceptance policy. Add no new helper, generated output file or dependency.

The schema below is exhaustive for data forwarded to the loader. Objects reject unknown keys at every level, including nested objects and records that would otherwise be preserved; S11 fields designated for discard are not screened or preserved. Reject duplicate JSON keys, wrong types, Boolean/integer substitutions, unreadable inputs and unsupported forms. Missing optional fields may pass; a present field must match its declared source-specific form.

### Settings and values

The only settings keys are `permissions`, `sandbox`, `hooks`, `env`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `enabledPlugins`, `syncClaudeAiPlugins`, `syncClaudeAiSkills`, `extraKnownMarketplaces` and `disableSkillShellExecution`.

| Node | Accepted shape and values |
| --- | --- |
| `permissions` | Only `defaultMode`, `deny`, `additionalDirectories`; `defaultMode` is `auto` where applicable; `additionalDirectories` is `[]`; `deny` is a renderer-declared worker/native-denial fragment for that source. No caller-added allow/ask rule or alternate permission mode. |
| `sandbox` | Only the keys emitted by the worker or administrative renderer: `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands`, `excludedCommands`, `filesystem`, `network`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `allowAppleEvents`. |
| `sandbox.filesystem` | Only `allowWrite`, `disabled`; exact source-specific canonical values. Worker write grants are the four declared agmsg stores; ordinary worktree/cache writes remain provided by the worktree boundary. |
| `sandbox.network` | Only `allowedDomains`, `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`; exact source-specific canonical values. |
| Sandbox lists and Booleans | Every present leaf/list equals the canonical worker fragment in S01-S04 or administrative fragment in S05-S07. Worker exclusions are empty; additional write roots/sockets are refused. Only administrative sources may contain the exact shared three exclusions and single Herdr socket. |
| `hooks` | Only source/event/matcher/operation combinations generated by the trusted renderer or delivery constructor. Groups have only `matcher`, `hooks`; handlers have only renderer-declared `type`, `command`, `timeout`, `async`, `statusMessage`, `onFailure`, with exact canonical values. |
| Handler type | Only the string `command`; validate it before reading `command`. HTTP, MCP-tool, prompt, agent, unknown, missing, null and non-string types refuse. |
| MCP approval fields | `enableAllProjectMcpServers: false`; `enabledMcpjsonServers: []`; `disabledMcpjsonServers: []` when present. Approval state never exempts a server definition. |
| Plugin fields | `enabledPlugins` maps only manifest-known or inventoried plugin identities to `false`; both sync fields are `false`; `extraKnownMarketplaces` is `{}`. |
| Skill execution | `disableSkillShellExecution`, when present, is `true`. |
| `env` | Only the four exact name/value pairs in the next subsection; arbitrary strings, maps and provider credentials are not preserved. |

Absent or empty settings objects pass where the source permits them. Administrative drop-ins/cache may contain canonical partial objects; partial means omitted declared fields, never new fields or alternate values. Validate each list before merging so an empty generated worker list cannot conceal a broader lower-scope array.

There is no canonical worker setting for helpers, status-line commands, wrappers, alternate sandbox executables, policy helpers or authentication refresh/export commands. Their keys refuse as undeclared, including misplaced forms. The orchestrator managed PermissionRequest exception is not a worker-start exception.

The old instruction to preserve unrelated non-executable state now applies only to fields admitted by this schema. Unknown settings refuse without deletion or normalization; S11 alone discards pre-existing fields outside its declared structures and carried identity, without screening or forwarding them.

### Environment and launch arguments

Settings `env` admits exactly `GH_TELEMETRY="false"`, `DO_NOT_TRACK="1"`, `CHECKPOINT_DISABLE="1"` and `AWS_EC2_METADATA_DISABLED="true"`, as declared by the manifest. The last name is the sole declared `AWS_*` exception and cannot select credentials or a provider.

The launch-input schema classifies names by source: existing parent/runtime declarations, `regime-declared`, and `platform-injected`. The latter two classes below are closed enumerations, not prefixes. They do not extend settings `env`, configuration-file keys or CLI arguments.

The launcher and its startup/preflight Python children use only the manifest-named absolute mise-installed non-shim interpreter, observed here as `<validated-home>/.local/share/mise/installs/python/3.15.0/bin/python3.15`. Add that narrow declaration to the existing manifest-owned launcher policy and consume it through the existing renderer; never route through `/usr/bin/python3`, a mise shim, PATH lookup or an interpreter-discovery fallback. Cover startup bootstrap/home lookup as well as preparation. This selects the interpreter for this boundary without returning the deferred complete binding work to scope.

The launch-input schema admits only these names, with source-specific values supplied or checked by the trusted parent:

| Names | Value authority |
| --- | --- |
| `HOME`, `PATH`, `LANG`, `TERM` | Validated passwd home; prescribed system-only child PATH; `C.UTF-8`; declared terminal value. Hook children retain `TERM=dumb`. |
| `TMPDIR` | Canonical trusted temporary directory supplied by the parent, not a candidate configuration root. |
| `CLAUDE_CONFIG_DIR` | Exactly the dedicated worker directory under the validated home. |
| `CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` | Parent-bound canonical project identity and runtime shell file; `CLAUDE_ENV_FILE` additionally requires the executable-content control below. |
| `UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR` | Exactly `<canonical-worktree>/.uv-cache` and its `python` child. |
| `regime-declared`: `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE`, `AGMSG_AGENT_PID` | Retain a03's exact authorities: `0`, validated launcher store selection, declared monitor value and numeric runtime process identifier; unset default-store selection remains supported. |
| `regime-declared`: `AGMSG_SPAWNED` | Exactly the string `1`, set by upstream `spawn.sh` on the launch surface before the worker CLI; require it on spawn-launched roles and do not synthesize it for unrelated child roles. |
| `platform-injected`: `__CF_USER_TEXT_ENCODING` | Darwin only; present or absent allowed. A present string must full-match `0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+`. The regime validates the shape and otherwise never reads or uses it. Linux presence refuses. |
| `HERDR_ENV`, `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_AGENTS_LAYOUT`, `HERDR_SOCKET_PATH` | Validated control-plane identity, `managed` layout and canonical configured socket; these grant no worker sandbox exception. |
| `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID` | Parent/runtime session identifier and numeric process identifiers where required by canonical attachment/delivery. |
| `CLICOLOR_FORCE`, `FORCE_COLOR` | Launcher-written `1` only where the launch route uses them. |
| `GH_TELEMETRY`, `DO_NOT_TRACK`, `CHECKPOINT_DISABLE`, `AWS_EC2_METADATA_DISABLED` | The four fixed values above. |
| `CHEZMOI_SOURCE_DIR`, `CHEZMOI_HOME_DIR` | Preparation-only trusted source/home bindings; not caller-selected worker configuration or executable roots. |

The read-only amendment-1 probe of the [documented environment variables](https://code.claude.com/docs/en/env-vars) identifies `CLAUDE_ENV_FILE` as the only name admitted above that selects a file whose contents execute: Claude runs its shell contents before Bash commands. No other admitted name has that documented role; `CLAUDE_CODE_SHELL` and `CLAUDE_CODE_SHELL_PREFIX` remain undeclared. Include the named file's contents in the preflight read set alongside S01-S23.

For every admitted executable-content file variable, preflight accepts its named file only when absent, empty, or byte-identical to canonical contents generated by the launcher for this start. Inspect without sourcing or executing it; unreadable/nonregular files and any other contents refuse before trust, migration, regeneration, hooks or worker commands with `worker startup refused: <file>: <variable>: noncanonical executable environment file contents`. Preserve refused bytes; never overwrite a planted file to make it pass. After all preflight checks pass, the launcher itself writes the canonical runtime-file contents, records SHA256 bound to the variable, canonical file and this start in existing startup state/evidence, and verifies those bytes before forwarding. Candidate-supplied or prior-start digests cannot authorize contents. Reuse the existing runtime file and startup state; add no sidecar, helper or generated configuration output. Later replacement races and reloads retain their existing residual owners.

Validate proposed worker configuration inputs before forwarding them. A clean child environment contains only the names declared for that child role; do not inherit the caller environment wholesale. Unknown proposed environment names refuse rather than becoming an unchecked pass-through. Existing profile/control-plane variables used to select a worker are consumed through their existing manifest-owned interfaces, not forwarded as arbitrary worker settings.

Every `CLAUDE_CODE_USE_*`, `AWS_*`, `ANTHROPIC_*`, `*_API_KEY`, `*_TOKEN` and `*_PROFILE` name refuses unless explicitly declared above with its exact allowed value. In particular refuse `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE` in settings and launch inputs before any credential lookup or helper execution. Add no AWS configuration parser.

No shell/interpreter startup or loader override is declared: `BASH_ENV`, `ENV`, `NODE_OPTIONS`, `NODE_PATH`, `PYTHON*`, `LD_*`, `DYLD_*`, shell wrappers and alternate configuration/cache roots refuse as worker inputs. Do not print their values.

Preserve the manifest-generated Claude argument interface: only `--model`, `--effort`, `--advisor` with their declared profile values, including `--advisor fable`. Caller-added settings, MCP, plugin, agent and additional-directory arguments refuse. Keep existing Codex arguments and network/shared-Git policy unchanged.

A clean-parent probe runs through the interpreter named by the rendered manifest, imports the same modules as the predecessor probe, and asserts `CPATH`, `LIBRARY_PATH`, `MANPATH` and `SDKROOT` are absent. They remain undeclared and refuse if encountered; do not delete them to conceal an unexpected injection. Test the observed child environment as well as the parent's proposed names, with child-role-specific declarations.

Any other new name, source, required state field or interpreter mismatch still blocks and re-tasks. Send a blocked PONG naming the boundary, exact command and status, with probe JSON containing the supplied/observed name lists, undeclared names and interpreter identity under the a04 evidence directory. Preserve the predecessor JSON unchanged. No wildcard, prefix-wide acceptance, candidate-learned schema, suppression or default-as-authorization is allowed; print no environment values.

### Sources, roots and component forms

The sole repository anchor is the manifest declaration resolving to `$HOME/Workspace/dotfiles`. Bind its identity to the validated passwd home and actual main checkout, resolving symlinks and filesystem case aliases. Worker roots must be registered linked worktrees beneath that anchor's declared `.claude/worktrees/` root with the same Git common directory.

Every worker launch route, for either worker kind, refuses another repository before worktree creation, identity registration, hook writes, workspace trust or spawn. The refusal names this task: `worker startup refused: dotfiles-T133-worker-write-boundary-a04: unsupported repository root`. Do not fix the foreign-root finding by inspecting the fixed anchor while launching elsewhere.

Admitted configuration roots are the dedicated worker directory, the validated anchor/worktree `.claude` directories, applicable nested worktree and additional-directory `.claude` directories, the platform managed root and contained plugin roots discovered through the declared registry. Inherited MCP files are the independently enumerated ancestor read set. No account-synced, inline, seed, alternate cache or caller-selected root is admitted; caller-added additional-directory arguments remain refused.

The admitted skills roots are exactly Enterprise `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), Personal `<absolute-home>/.claude-worker/skills` under the dedicated configuration directory, Project `<project>/.claude/skills`, Nested `<subdir>/.claude/skills`, Additional directory `<add-dir>/.claude/skills` under an applicable `--add-dir` directory, and Plugin `<plugin>/skills`. Inspect both `<skills-root>/<name>/SKILL.md` and bundled `<skills-root>/<name>/.claude-plugin/plugin.json`. Managed command/agent locations likewise start at the actual managed root. Resolve every selected path and refuse containment escapes, unsupported aliases, missing references or unreadable files.

| Source form | Closed acceptance |
| --- | --- |
| S08-S10, S18-S19 | Objects containing only absent or empty `mcpServers`/`managedMcpServers` maps. No server, including remote-only definitions, is canonical here. |
| S11 global state | At every start, after all preflight checks pass and before any loader/worker command, write the existing `CLAUDE_CONFIG_DIR/.claude.json` from scratch: `mcpServers: {}`, `projects: {}` and `hasCompletedOnboarding: true`, plus screened identity fields below. The generated file carries no per-project inventory or pre-generated workspace trust. Never merge the previous file into this output. |
| S11 pre-existing structures and identity | The existing file must be a JSON object. Missing optional retained fields pass and generated fields are written anew. Present top-level `mcpServers` must be `{}`. Carry optional `oauthAccount` only as an object with string-only members from this documented fixed set: `accountUuid`, `emailAddress`, `organizationUuid`, `displayName`, `fullName`, `organizationRole`, `workspaceRole`; declare the same set in the manifest and fixtures. Carry optional `userID` only as a string matching `^[0-9a-f]{64}$`, the installed loader's hex form. Undeclared identity members, non-string `oauthAccount` members, invalid identity values and a nonempty or malformed top-level MCP map refuse with `worker startup refused: <state-file>: <offending-key>: <named reason>` before any command or mutation, preserving refused bytes. Nonempty top-level servers use the exact reason `noncanonical global state` as tamper evidence. |
| S12/S15 plugin descriptor | Only `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and the component keys `hooks`, `mcpServers`, `lspServers`, `commands`, `agents`, `skills`. Descriptive fields are strings, keywords are strings, and author has only string `name`, `email`, `url`. |
| Component references | Each present component is one scalar string referencing a regular file within its admitted root. The screening reads that file under its source schema before accepting it. Arrays, objects, inline content, URLs and explicit directory references refuse. Default component directories are independently expanded into inspected files. |
| S13 installed registry | Only `version: 2` and `plugins`; plugin IDs map to record lists with only `scope`, `installPath`, `version`, `installedAt`, `lastUpdated`, `gitCommitSha`, `projectPath`. Scope is user/project/local; paths are contained and project-bound; descriptive fields are strings and a present commit is 40 hex. Every referenced descriptor is read and every discovered ID is disabled. |
| S14 marketplace registry | Only `{}`; no refresh source or executable header helper is canonical. |
| S16 hook file | Only an absent/empty `hooks` object; plugin-owned handlers have no canonical worker operation. |
| S17 marketplace descriptor | Only descriptive `name`, `owner`, `metadata`, `plugins`; owner has string name/email, metadata has string description/version, and plugins is absent or `[]`. Additional plugin selections refuse. |
| S20-S22 Markdown | Plain text with the existing restricted frontmatter grammar: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model. Booleans are Boolean, model/tool selections are manifest-declared values, and unknown/nested executable forms refuse. Dynamic shell expansion, including fenced forms, refuses everywhere. |
| S23 LSP | Only `{}`; command/args definitions are not canonical. |
| Non-file managed inputs | Enumerated canonical administrative data only; otherwise refuse with the managed source name before executing any helper or starting Claude. |

For S11, every other pre-existing top-level field, including the entire `projects` value and all its contents, `numStartups`, prior onboarding state, tips/changelog caches, project `history`, `allowedTools` and cost counters, is neither screened nor preserved; only syntax/duplicate-key/readability checks apply to the whole input. Discarded objects and arrays are never recursively screened or forwarded. Generate onboarding anew and `projects: {}`, preserve only screened identity values, and reuse the existing atomic writer after the complete preflight; the loader regenerates native state. The anchor's workspace trust is established by the launcher's existing acceptance of the workspace-trust dialog during spawn's readiness wait (`herdr-agents --add-worker` for a Claude worker, documented in the SKILL's 'Regime activation and progress' section). All Claude workers share `CLAUDE_CONFIG_DIR` at `$HOME/.claude-worker`; discarding the prior `projects` value lets sequential sibling starts succeed. A loader requiring another preserved field blocks and retasks rather than widening silently.

These restrictions also apply to disabled plugins and shadowed sources. Do not recursively ignore an unknown object because it lacks a familiar executable key. A plugin `commands` mapping containing `{"source": ...}` or inline `content` refuses at the selecting file/key.

## Implementation and retained controls

1. Keep one preflight over S01-S23, admitted executable environment-file contents and the closed schema. Every Claude route calls it before workspace trust, migration, normalization, regeneration or execution. Enumerate through the filesystem, including ignored/untracked inputs; neither Git tracking nor a nearer definition removes a source. Inspect implicit and selected components separately without executing helpers, installing packages, fetching plugins or starting servers.

2. Refusals identify the actual source and key/class without printing payloads, environment values, URLs with credentials or authentication material. Preserve the handler message `worker startup refused: <source-file>: hooks.<event>[<group-index>].hooks[<handler-index>]: noncanonical hook handler`, with zero-based indices. Other refusals use `worker startup refused: <source>: <key>: <named reason>`. Unknown settings, selectors, roots, components and source forms each receive a named reason.

3. Retain exact recognized legacy-delivery classification, including canonical project binding. First screen every source; only after complete success migrate recognized owned entries, validate the prepared result under the same schema, then write. Unknown content outside S11's discard partition refuses without changing any pre-existing bytes; successful S11 regeneration intentionally replaces discarded state only after every source passes. Never rewrite tracked settings or create a local file merely for migration. Keep repeated preparation and delivery-tool-unavailable behavior.

4. Retain dedicated `CLAUDE_CONFIG_DIR`, both private cache variables on every actual worker route, `AGMSG_RESOLVE_PROJECT=0`, validated `AGMSG_STORAGE_PATH`, canonical attachment identity and `onFailure: "block"` where supported. A writable `run/proj.<pid>.project` cannot replace the explicit project identity. Preserve the a02 absolute Herdr/jq/Node/npm/Codex calls and attachment environment; fixed PATH must not regress attachment or default seating.

5. Keep static `trusted_paths` derived from trusted executable inputs, not Git trees/indexes. Preserve anchored source/control paths, tracked/main-local settings, `.orchestration`, both `.agents/worklog/**` and `.agents/worklog/uv-cache/**`, worktree `.claude` directory/descendant targets and `.mcp.json`. Ordinary worktree source and private cache writes remain available.

6. Retain explicit protection of `<absolute-home>/.agents/agent-config.yaml`, model profiles, permgate policy, skill scripts/SKILL files, agmsg plugin code and `db/trusted-plugins`, `<absolute-home>/.claude/**`, `<absolute-home>/.claude-worker/**`, installed guard, local wrappers/application code, configuration/state/tool installations and shared uv caches. Keep directory and descendant user-site protection for `.pth`, `usercustomize.py` and `sitecustomize.py` on both platforms. Add no blanket `<absolute-home>/.agents/**` or `<absolute-home>/.local/**` deny: agmsg `db`, `teams`, `run`, `ext-tools` stay writable except `db/trusted-plugins`.

7. Retain separate orchestrator, worker and administrative renders. Worker policy keeps `defaultMode: auto`, sandbox startup failure, disabled unsandboxed requests, empty user exclusions, restricted writes, no user Herdr socket, explicit MCP auto-approval disables, account sync off and false plugin entries including discovered `@skills-dir` identities. Empty maps alone do not disable plugins or replace screening.

8. Administrative settings retain enabled sandboxing, `failIfUnavailable: true`, disabled unsandboxed requests, filesystem enforcement, disabled weaker isolation/Apple Events/all-socket/local-binding switches, exactly the Herdr socket, and exactly these ordered exclusions: `agmsg-dispatch *`, `herdr-agents *`, `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These shared capabilities remain available to every Claude seat and authorize no worker escape. Lower-scope canonical validation rejects extra exclusions, writes or sockets before array merging.

9. Keep the orchestrator managed PermissionRequest command's existing literal bytes unchanged, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.

10. Apply design 5.14 by reference for trusted-parent execution, Python isolation and Git inspection. Consume the manifest-named non-shim interpreter specified above on every launcher startup/preflight Python route; add no resolver, helper, private executable directory, PATH fallback or broader version-pin work. Do not execute arbitrary task-body shell strings as probes.

11. Preserve guard routing, fixed payload paths, argument boundaries, stdin and child status. Canonical worker/sibling/unrelated/missing launch identities execute no orchestrator project payload. Only fixed installed worker-delivery operations run for workers. Formatter/map operations also reject worker/outside-anchor tool inputs. Keep tracked settings portable and all existing event/validator markers.

12. Preserve managed SessionStart/PostToolUse/PreToolUse migration, custom-hook ordering, mixed entries, escaped-tilde distinctions, stale replacement and idempotence. For `make update`, reconcile the managed Claude settings after `scripts/update-agent-assets.sh` runs Herdr's installer, using the allowed Makefile/merge/renderer surfaces. Do not edit the updater script or import its unguarded hook as canonical. Verify one effective guarded hook and no managed-settings drift after repeated fake updates.


**Reviewing audit data and requirements**
**Verifying hash and avoiding mutations**
exec
/bin/zsh -lc "sed -n '491,597p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md; sed -n '354,384p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md; /usr/bin/shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md" in ~/Workspace/dotfiles
 succeeded in 9ms:
## Regression fixtures

Write the new tests before implementation. Use the existing temporary-HOME, managed-root, linked-worktree and fake-launcher builders. Tests execute no payload, credential helper, HTTP endpoint, server, plugin, subagent or live worker.

Each refusal fixture asserts the source/key or named root message, unchanged existing bytes, no migration/regeneration, no trust acceptance, no spawn and absent execution/request markers. Positive absent/canonical controls and repeated starts remain covered.

| Selector | Required coverage |
| --- | --- |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees` | Red on c0f50fa1, green after: sequentially start registered linked-worktree workers A then B on one shared `CLAUDE_CONFIG_DIR`. A's start leaves the regenerated file; simulated loader writes then add A's project entry with a `history` list. B's start succeeds and, before its first command, leaves exactly the regenerated file with `projects: {}` and screened identity. Replace any planted-project-key refusal and same-worktree restart fixture with this cross-worktree sequence. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_global_state_with_screened_identity` | Red on c0f50fa1, green after: pre-existing S11 has `numStartups: 5`, `hasCompletedOnboarding: true`, `projects[anchor].history` as a list and synthetic valid `oauthAccount`/hex `userID`. A fake worker start succeeds; before its first command the file equals exactly `mcpServers: {}`, `projects: {}`, `hasCompletedOnboarding: true` plus unchanged screened identity. Cover absent state/identity; all discarded fields and project contents disappear without semantic screening. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonempty_global_mcp_servers` | Red on c0f50fa1, green after: pre-existing S11 has nonempty top-level `mcpServers`; assert exactly `worker startup refused: <state-file>: mcpServers: noncanonical global state` before any command, preserving all bytes and absent mutation/trust/spawn/execution markers. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member` | Red on c0f50fa1, green after: a documented `oauthAccount` member contains an object; refuse with the file and exact member key named before any command and preserve all bytes. Also cover arrays, other non-string values, undeclared identity members, invalid `userID` and malformed retained structures; canonical string-only identities pass. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` | Red on c0f50fa1, green after: a pre-existing forwarded `CLAUDE_ENV_FILE` contains a planted command marker and exports restoring refused environment variables. Refuse with the variable and file named before any hook/worker command runs, without sourcing the file; assert unchanged bytes, no migration/regeneration/trust/spawn and absent command markers. In this one fixture retain absent, empty and same-start launcher-generated positive controls with recorded SHA256, and show that a prior-start digest cannot authorize foreign contents. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_aws_credential_chain_selectors` | Red on c0f50fa1: the four reported selectors select a synthetic worker-owned AWS configuration containing `credential_process`; preparation refuses without running or trusting it. Test settings and launch inputs. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root` | Red on c0f50fa1: another repository with main-local payload refuses with this task's name before any side effect, for both kinds and all worker routes; the validated anchor/control passes. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components` | Red on c0f50fa1: object `source` mappings and inline `content`, including dynamic Markdown, refuse even with the plugin disabled. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys` | One fixture per settings source, unknown top-level and nested keys, including a harmless-looking future key; candidate data cannot extend the allowlist. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors` | Every prohibited name family, settings/launch placement, exact fixed-value AWS exception, unknown ordinary environment names and noncanonical declared values. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_requires_string_component_references` | Scalar file control; object, list, directory, missing file, outside-root reference and unreadable component negatives. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch` | Command-free HTTP separately in S01-S07 on both platforms; other documented/unknown/missing/malformed types; other hook-bearing sources; exact indexed refusal. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_managed_skills_use_actual_managed_root` | Retained green baseline on c0f50fa1, accepted by owner PING 2751; do not manufacture a red result: using the same temporary managed-root fixture as S05/S06 for both Darwin and Linux, plant a Markdown skill at `<managed-root>/.claude/skills/<name>/SKILL.md` and a bundled plugin payload at `<managed-root>/.claude/skills/<name>/.claude-plugin/plugin.json` with hooks; metadata-only control produces explicit disable. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_project_sandbox_extensions_are_refused_before_launch` | Red on c0f50fa1: `excludedCommands: ["*"]`, `filesystem.allowWrite: ["/"]`, extra sockets and nested unknowns in project/local scopes; canonical administrative controls remain accepted. |
| `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_creates_managed_parent_in_printed_commands` | Red on c0f50fa1: missing parent, both platforms, quoting, mkdir-before-install, staged JSON and absent executed-sudo marker. |
| `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_update_reconciles_settings_after_herdr_install` | Red on c0f50fa1: fake Herdr installer re-appends its literal hook, then update reconciliation restores one guarded entry; repeated update preserves custom hooks and produces no managed drift. |

The runtime-name regressions below are required within the unchanged environment and fixture-alignment budgets:

| Selector | Required coverage |
| --- | --- |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names` | Execute the predecessor's name-only probe through the absolute non-shim interpreter read from the rendered manifest, with only HOME/PATH/LANG/TERM supplied. Assert CPATH, LIBRARY_PATH, MANPATH and SDKROOT are absent; Darwin permits only the declared platform addition. Route fixtures prove bootstrap, home lookup and preflight use that interpreter without invoking the system shim or PATH fallback. Preserve command/status/name-only JSON. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment` | Darwin absent and correctly shaped present controls pass; malformed shapes, wrong types, trailing content and Linux presence refuse before mutation/trust/spawn. The value never selects behavior, a path or an executable and never appears in evidence. An unrelated injected name blocks with probe JSON. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment` | Fake upstream spawn exports exactly AGMSG_SPAWNED=1 before CLI entry; accept it only for the declared child role. Wrong values and undeclared AGMSG names refuse; all four previously declared AGMSG names retain their authority and optionality. Settings env remains limited to its four original pairs. |

The five allowlist classes each have an explicit fixture: unknown key, undeclared provider selector, foreign root, object-form component and non-command handler. Parameterization may share builders but must name every subcase in validation. Do not replace the three required c0f50fa1-red regressions with tests of a new validator alone.

Retain all a02 regressions: old tracked settings, alternate executable fields, inherited project MCP, dedicated global state, skills-directory plugins, per-source S01-S23 coverage, sandbox-only documentation, hostile-GH_HOST templates, private caches, native denials, migration and guarded delivery. The fixture-case source inventory equals the production source inventory; each case plants its payload in the source it claims to exercise.

Retain a02's red/green evidence for `env.HOME`, fenced dynamic commands and the four 79ea98a3 fixes as historical evidence. Do not claim those tests newly fail on c0f50fa1. Update the documentation template test to read the a04 task copy. Update inherited S11 sentinel-preservation/unknown-field-refusal expectations to the discard-and-regenerate contract with `projects: {}`; retain the top-level MCP tamper refusal, and do not keep the old blanket `oauthAccount` refusal or project-entry refusals.

C11: every `closed` row names one exact `tests/<path>.py::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.

## Change budget

Changed lines mean additions plus deletions. The starting measurement is `git diff --numstat 51ba5801 c0f50fa1`, not the obsolete a01 estimate. Preserve its complete output and account separately for base-branch changes already merged into c0f50fa1. The author repeated this immutable comparison when preparing a04.

For this task's allowed paths, excluding `.orchestration/`, tests and the three regenerated Claude settings templates, that command measures:

| Source | Changed lines |
| --- | ---: |
| `.claude/settings.json` | 96 |
| `.gitignore` | 1 |
| `Makefile` | 6 |
| `home/dot_agents/agent-config.yaml` | 60 |
| `home/dot_agents/skills/agmsg-orchestration/SKILL.md` | 10 |
| `home/dot_claude-worker/modify_private_settings.json` | 437 |
| `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` | 65 |
| `home/dot_claude/modify_private_settings.json` | 120 |
| `home/dot_local/bin/common/executable_herdr-agents` | 126 |
| `scripts/generate-agent-configs.py` | 181 |
| `scripts/validate-agent-assets.py` | 9 |
| **Measured starting source total** | **1111** |

The seven allowed test modules measure respectively 103, 15, 206, 935, 104, 310 and 95 changed lines in `allowed_files` order: **1768**. The full historical-base output additionally contains already-merged unrelated source/test rows; list them rather than charging them as new a04 work or editing them.

Amendment 1's read-only sizing counts 24 lines in c0f50fa1's `present`/`read_json`/`write` analogues plus 16 estimated declaration/digest/route lines, and the 42-line non-command-handler fixture plus 18 estimated content/control lines: **40 source / 60 test**. This measured analogue-based estimate is not a measured implementation result.

Amendment 2's read-only AST sizing of c0f50fa1 measures `present` 8 + `read_json` 10 + `write` 6 = 24 source analogue lines, plus 56 estimated declaration/project/identity/regeneration lines: **80 source**; the global-state fixture 20 + refusal helper 36 = 56 test analogue lines, plus 64 estimated generation/identity/restart subcases: **120 test**. These are sizing analogues reused without duplication, not measured implementation results. Amendment 3 retains the **80 source** ceiling, removes project-inventory work and replaces the restart subcases with the A-then-B shared-directory sequence: the same 56 test analogue lines plus 104 estimated generation/identity/sequential-start subcase lines give **160 test**, an additional **40 test** over amendment 2. This revised estimate is not a measured implementation result.

Authorize these incremental ceilings, attributed to accepted findings. These increments are estimates pending implementation measurement, not claimed measured results:

| Control/finding | Additional source | Additional tests |
| --- | ---: | ---: |
| Closed settings/nested-value schema and sandbox extensions; S1, `local:c0f50fa:2` | 180 | 140 |
| Environment/provider allowlist and credential-chain refusal; `security:c0f50fa:1` | 70 | 100 |
| Validated repository root; `security:c0f50fa:2` | 25 | 60 |
| Scalar inspected-file components; `security:c0f50fa:3` | 35 | 70 |
| Actual enterprise skills root; `local:c0f50fa:1`, `text-security:be969e3:1` | 10 | 40 |
| Handler-class/schema consistency; `text-security:b2a186e:1` | 10 | 30 |
| Printed privileged parent creation; `local:c0f50fa:3` | 10 | 25 |
| Post-Herdr reconciliation; `local:c0f50fa:4` | 10 | 45 |
| Existing render/docs fixture alignment with the accepted re-plan | 10 | 30 |
| Executable environment-file contents and launcher-written SHA256; `text-security:f7af699:1` | 40 | 60 |
| Launcher-generated S11, screened identity and empty shared project state; D-024-34/D-024-35, `worker:5067ed0:1` and `text-security:efa211d:1` with `text-security:f7af699:1` as the shared family | 80 | 160 |
| **Increment ceiling** | **480** | **760** |

The source cap remains **1591 = 1111 + 480**; the test cap remains **2528 = 1768 + 760**, including a03 amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. The a04 non-shim interpreter, platform-injected and regime-declared controls fit the existing environment/provider and fixture-alignment increments; no cap increases. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.

RESULT records final per-file numstat, historical-base and final PR merge-base identities, actual source/test totals and per-control attribution. Preserve both the complete historical comparison and the current PR comparison so merged base changes are visible.

Every later amendment maps to accepted review findings and carries `previous_sha256`; the worker raises no cap. Amend Change budget, the operative C-107 Check cap sentence and the Checks block together. A measured overrun produces a blocked PONG rather than suppression or an unreviewed text edit.

## Out of scope

D-024-26 still assigns exact host-probed uv/Python/Node version declarations and mise pins beyond a04's narrow launch-interpreter selection, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.

Keep `home/dot_mise/config.toml`, the installed state-helper source, Codex boundary sources and updater scripts outside scope. No binding-only code returns through shared files. Add no write-boundary Python hook, gh wrapper, credential-directory substitute, installation discovery or PATH fallback.

P1-14 a05 and P1-6 own approval/evidence consumption. The exact operative ledger templates tested from this task copy are `gh api --hostname github.com repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha` and `gh api --hostname github.com 'repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref=<sha40>'`. Validate the returned full 40-hex SHA and use the identical SHA in the content request. Every deciding API call binds `--hostname github.com`; every deciding subcommand binds `--repo github.com/mryfmo/dotfiles`. Refuse if the host cannot be bound, without an unbound retry or local fallback.

Retain `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host`: extract those two templates, substitute only the validated SHA, exercise argv without shell evaluation, export hostile `GH_HOST`, check exact hostname/repository/SHA binding and test an isolated no-gh refusal. This is a contract test, not a ledger consumer or authentication test. Local remotes, URL rewrites, refs, objects and working-copy rows establish no approval authority.

The host is not a security boundary between same-UID seats. `GH_CONFIG_DIR` does not separate macOS Keychain credentials. Native merge denials remain `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`; shared credentials permit other API routes. P1-11 owns next-records-PR detection, not main-push detection or prevention. Separate-user/host prevention remains the operator's future P1-16 decision.

`dotfiles-T133-agmsg-hardening-a01` owns store driver-name validation and plugin authorization. Shared administrative exceptions/socket access, external host processes, same-UID races, later configuration reloads and hook-event limitations remain residuals. Dedicated login state is not imported from the orchestrator or used to discover executable acceptance rules.

Perform no live settings application, authentication/keyring/ruleset mutation, global/administrative installation, permission-policy deployment, restart or merge. Edit no canonical task, acceptance record, decision ledger, design or another task's evidence.

## Closed startup schema

Declare this schema in `home/dot_agents/agent-config.yaml` and expose it through the existing renderer/preparation code. Candidate files, Git objects and installed upstream schemas never define their own acceptance policy. Add no new helper, generated output file or dependency.

The schema below is exhaustive for data forwarded to the loader. Objects reject unknown keys at every level, including nested objects and records that would otherwise be preserved; S11 fields designated for discard are not screened or preserved. Reject duplicate JSON keys, wrong types, Boolean/integer substitutions, unreadable inputs and unsupported forms. Missing optional fields may pass; a present field must match its declared source-specific form.

### Settings and values

The only settings keys are `permissions`, `sandbox`, `hooks`, `env`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `enabledPlugins`, `syncClaudeAiPlugins`, `syncClaudeAiSkills`, `extraKnownMarketplaces` and `disableSkillShellExecution`.

| Node | Accepted shape and values |
| --- | --- |
| `permissions` | Only `defaultMode`, `deny`, `additionalDirectories`; `defaultMode` is `auto` where applicable; `additionalDirectories` is `[]`; `deny` is a renderer-declared worker/native-denial fragment for that source. No caller-added allow/ask rule or alternate permission mode. |
| `sandbox` | Only the keys emitted by the worker or administrative renderer: `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands`, `excludedCommands`, `filesystem`, `network`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `allowAppleEvents`. |
| `sandbox.filesystem` | Only `allowWrite`, `disabled`; exact source-specific canonical values. Worker write grants are the four declared agmsg stores; ordinary worktree/cache writes remain provided by the worktree boundary. |
| `sandbox.network` | Only `allowedDomains`, `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`; exact source-specific canonical values. |
| Sandbox lists and Booleans | Every present leaf/list equals the canonical worker fragment in S01-S04 or administrative fragment in S05-S07. Worker exclusions are empty; additional write roots/sockets are refused. Only administrative sources may contain the exact shared three exclusions and single Herdr socket. |
| `hooks` | Only source/event/matcher/operation combinations generated by the trusted renderer or delivery constructor. Groups have only `matcher`, `hooks`; handlers have only renderer-declared `type`, `command`, `timeout`, `async`, `statusMessage`, `onFailure`, with exact canonical values. |
| Handler type | Only the string `command`; validate it before reading `command`. HTTP, MCP-tool, prompt, agent, unknown, missing, null and non-string types refuse. |
| MCP approval fields | `enableAllProjectMcpServers: false`; `enabledMcpjsonServers: []`; `disabledMcpjsonServers: []` when present. Approval state never exempts a server definition. |
| Plugin fields | `enabledPlugins` maps only manifest-known or inventoried plugin identities to `false`; both sync fields are `false`; `extraKnownMarketplaces` is `{}`. |
| Skill execution | `disableSkillShellExecution`, when present, is `true`. |
| `env` | Only the four exact name/value pairs in the next subsection; arbitrary strings, maps and provider credentials are not preserved. |

Absent or empty settings objects pass where the source permits them. Administrative drop-ins/cache may contain canonical partial objects; partial means omitted declared fields, never new fields or alternate values. Validate each list before merging so an empty generated worker list cannot conceal a broader lower-scope array.

There is no canonical worker setting for helpers, status-line commands, wrappers, alternate sandbox executables, policy helpers or authentication refresh/export commands. Their keys refuse as undeclared, including misplaced forms. The orchestrator managed PermissionRequest exception is not a worker-start exception.

The old instruction to preserve unrelated non-executable state now applies only to fields admitted by this schema. Unknown settings refuse without deletion or normalization; S11 alone discards pre-existing fields outside its declared structures and carried identity, without screening or forwarding them.

### Environment and launch arguments
401573e9740264bea716a1dd479c5d740d83b5a2fb9982ebf57f00f025102764  .orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md

**Confirming no new findings**
codex
No findings against the stated design. Checked all 37 threat rows, seven allowed-file entries, cited acceptance/review history and deferred-owner scopes. No row claims `closed`.

The named tests support declaration, rendering, routing and migration checks. Complete execution binding—including mise shims, inherited `GIT_*`, symlink/case aliases, replacement races and ledger consumption—remains explicitly residual or separately owned. The earlier Linux exclusion, premature hook activation and GitHub-host evidence issues are addressed.

Reviewed SHA256: `401573e9740264bea716a1dd479c5d740d83b5a2fb9982ebf57f00f025102764`.

📝 まとめ: Read-only pre-dispatch security review completed without additional findings; acceptance remains with the orchestrator.

Not checked: implementation, tests, CI or live enforcement; no files changed. Same-user and shared-credential bypass risks remain.
Verdict: correct
hook: Stop
hook: Stop Completed
tokens used
116,772
No findings against the stated design. Checked all 37 threat rows, seven allowed-file entries, cited acceptance/review history and deferred-owner scopes. No row claims `closed`.

The named tests support declaration, rendering, routing and migration checks. Complete execution binding—including mise shims, inherited `GIT_*`, symlink/case aliases, replacement races and ledger consumption—remains explicitly residual or separately owned. The earlier Linux exclusion, premature hook activation and GitHub-host evidence issues are addressed.

Reviewed SHA256: `401573e9740264bea716a1dd479c5d740d83b5a2fb9982ebf57f00f025102764`.

📝 まとめ: Read-only pre-dispatch security review completed without additional findings; acceptance remains with the orchestrator.

Not checked: implementation, tests, CI or live enforcement; no files changed. Same-user and shared-credential bypass risks remain.
Verdict: correct
