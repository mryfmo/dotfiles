Reading additional input from stdin...
OpenAI Codex v0.163.0
--------
workdir: /Users/a0004262/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a16103-29c3-7ae2-96bc-08d2c710e0f1
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-gh-binding-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both /Users/a0004262/.codex/hooks.json and /Users/a0004262/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
対象タスクと参照先の記録を読み、設計上の検証結果が実際の実行対象に結び付くかを確認します。agmsg-orchestration と Ponytail のレビュー手順を使い、ファイルは変更しません。
exec
/bin/zsh -lc 'cat /Users/a0004262/.agents/skills/agmsg-orchestration/SKILL.md' in /Users/a0004262/Workspace/dotfiles
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

exec
/bin/zsh -lc 'cat /Users/a0004262/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in /Users/a0004262/Workspace/dotfiles
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
/bin/zsh -lc 'cat /Users/a0004262/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in /Users/a0004262/Workspace/dotfiles
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

exec
/bin/zsh -lc 'git status --short; nl -ba .orchestration/tasks/dotfiles-T133-gh-binding-a01.md' in /Users/a0004262/Workspace/dotfiles
 succeeded in 191ms:
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
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-1d72f16.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-gh-binding-a01
     4	kind: code
     5	security: true
     6	dispatch_status: blocked-pre-anchor
     7	design_review: {design: .orchestration/plans/024-design-quality.md}
     8	requires_decision: [D-024-69]
     9	after: []
    10	allowed_files:
    11	  - home/dot_mise/config.toml
    12	  - home/dot_agents/agent-config.yaml
    13	  - scripts/validate-agent-assets.py
    14	  - scripts/orchestrator/chain-integrate.sh
    15	  - scripts/orchestrator/orch-gate.sh
    16	  - scripts/orchestrator/local-review.sh
    17	  - tests/unit/test_*.py
    18	  - .orchestration/dotfiles-T133-gh-binding-a01/**
    19	threat_table:
    20	  - {control: "home/dot_mise/config.toml", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_exact_pin"}
    21	  - {control: "home/dot_agents/agent-config.yaml", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
    22	  - {control: "scripts/validate-agent-assets.py", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
    23	  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_chain_integrate_authenticated_decoy"}
    24	  - {control: "scripts/orchestrator/orch-gate.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_orch_gate_authenticated_decoy"}
    25	  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_local_review_authenticated_decoy"}
    26	  - {control: "tests/unit/test_*.py", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence-integrity automation; limit edits to Item 6's four modules and independently inspect assertions and red/green logs."}
    27	  - {control: ".orchestration/dotfiles-T133-gh-binding-a01/** including task.md", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence automation; compare anchored bytes, task-copy digest and literal full head against the independently audited PR."}
    28	  - {control: "pin", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_exact_pin"}
    29	  - {control: "declaration", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
    30	  - {control: "consumer binding", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_consumer_binding_matrix"}
    31	  - {control: "minimal environment", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_gh_environment_is_minimal"}
    32	  - {control: "gh configuration inputs", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_protected_gh_configuration"}
    33	  - {control: "trusted parent before first instruction", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns automatic parent binding; authenticated use stays disabled until the orchestrator measures a clean, absolutely bound parent and private namespace for every non-gh process in the route."}
    34	  - {control: "task metadata", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns dispatch automation; reviewed inventory and populated Checks must match the complete anchored task before dispatch."}
    35	  - {control: "metadata separators", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns byte-integrity automation; compare all front matter, separators and Checks, with no paste after anchor."}
    36	  - {control: "in-process effects", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_git_environment_cannot_redirect_fixture_writes"}
    37	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns uv/Python/Node, permgate and launcher binding; unchanged resolvers run only inside Item 3's measured parent namespace, otherwise authenticated use is blocked."}
    38	  - {control: "new or renamed scripts; future gh routes", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns adoption by absent chain-finish and future checker gh routes; create no consumer here and require their own positive authenticated fixtures before claiming closure."}
    39	  - {control: "remaining git/date/mise executable provenance", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns permanent remaining-tool binding; today's resolver algorithms remain, constrained by the measured parent namespace and token-free discovery, with no authenticated fallback."}
    40	  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns integration follow-through; only the orchestrator integrates the exact audited head through Playbook step 10."}
    41	  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence refresh; rerun CI, feedback, audit, acceptance and gate for every changed head."}
    42	  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns teardown records; none is planned and no dirty state may be discarded without separate authorization."}
    43	  - {control: "orchestrator effect owner-stub amendment", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns every residual assigned here; the orchestrator expands its existing stub before anchor, outside worker scope."}
    44	  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns measurement automation; gh-free private-clone evidence and trusted-parent observations must precede a fresh review of the complete populated bytes."}
    45	  - {control: "orchestrator effect installation and deployment", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns deployment follow-through; separately verify the pinned install, protected configuration and real authenticated consumer probes before enabling acceptance reads."}
    46	  - {control: "design 5.14 item 0", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns the unchanged item 0 residual; this task establishes no same-UID or credential-separation boundary."}
    47	  - {control: "design 5.14 item 1", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns host protection evidence; item 1 must cover the declaration, binary, configuration source and parent namespace before authenticated use."}
    48	  - {control: "design 5.14 item 2", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns permanent item 2 integration; the measured trusted-parent compensating control is mandatory now."}
    49	  - {control: "design 5.14 item 3", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns wider item 3 integration; apply it to this task's gh inputs without certifying other runtime boundaries."}
    50	  - {control: "design 5.14 item 4", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns wider item 4 integration; checked gh identity is consumed directly and same-UID replacement remains item 0's residual."}
    51	  - {control: "design 5.14 item 5", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns unchanged item 5 obligations; retain full head identities and introduce no lock or reservation changes."}
    52	  - {control: "design 5.14 item 6", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns deployment verification; distinguish fixture success, CI and observed host execution under item 6."}
    53	  - {control: "design 5.14 item 7", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns wider item 7 coverage; independently check behavioral assertions and never count setup failure or absent routes as closure."}
    54	  - {control: "design 5.14 item 8", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns future canonical-reader adoption; apply item 8 to active gh routes and do not certify the current local-object checkers."}
    55	  - {control: "design 5.14 item 9", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns permanent item 9 integration; measured isolated runtimes and the parent's absolute UV_CACHE_DIR remain mandatory."}
    56	  - {control: "design 5.14 item 10", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns denial records; item 10 applies and any denied command stops work with a blocked PONG."}
    57	premises: []
    58	---
    59	
    60	# AGMSG-TASK dotfiles-T133-gh-binding-a01 — bind gh on the measured host
    61	
    62	D-024-69 supersedes the 2026-10-21 owner stub and pulls this remedy ahead of slices 2-5; pins-a01 merged as #449, after remains empty, and later tool declarations use sibling entries. TASK names worker a012, a Codex seat.
    63	Seven refused C-80 rounds: a07-checker 922292d/0edbd8c/fd8c003/c6cebe4/a3125e1; regime-ci-followup-a02 a232baf/a18a67d. Unbound gh can forge canonical main, design, merge state and PR data and read forwarded credentials.
    64	Design 5.14 items 0-10 apply by reference, particularly 2-4/9; do not restate their trusted-execution contract.
    65	R1 references below identify original lines of .orchestration/tasks/dotfiles-T133-gh-binding-a01.md: 39→Item 3; 76→Item 4; 38/80→Item 6; 105→Item 0; 110→Anchor.
    66	
    67	## Items
    68	
    69	0. Reviewed baseline amendment for R1:105: local HEAD and origin/main are 7da0cdfab9de9fbea673b82379acd4e317115065; chain-finish.sh is absent, and regime-ci.py/task-consistency-check.py currently use Git, not gh lookups. These are local observations, not authenticated canonical facts.
    70	   Implement the three present shell routes, including their actual gh descendants; do not invent a finish script or add canonical-network behavior to either checker. Future gh adoption belongs to dotfiles-T133-gh-binding-followup-a01 and requires positive authenticated fixtures in those owners.
    71	   This explicit inventory amendment requires C-80 approval with gh-free canonical confirmation before dispatch. If the canonical baseline differs, reauthor and review the whole inventory and threat table; never silently widen scope or claim six routes were closed.
    72	1. Pin "github:cli/cli" = "2.102.0" in home/dot_mise/config.toml, with one adjacent English reason comment following pins-a01; extend the exact-version assertion and retain unrelated pins.
    73	2. Add trusted_tools.gh with version "2.102.0" and path "~/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh" to agent-config.yaml; later uv/Python/Node bindings extend sibling entries.
    74	   validate-agent-assets.py checks version equals the mise pin, the spelling is normalized and home-anchored, expansion is absolute under the real user's trusted home, and neither spelling nor resolved path is under shims. Refuse missing/malformed declarations, traversal, forged HOME and mismatched identities; one refusal test per rule.
    75	   Runtime reads the protected deployed ~/.agents/agent-config.yaml as data using existing parsing facilities under the measured isolated interpreter; never source/eval it or read a PR/worker copy. Chezmoi already deploys this plain source file; no generated artifact is needed, so leave generate-agent-configs.py and its tests unchanged.
    76	3. Replace gh discovery in chain-integrate.sh and orch-gate.sh, and bind local-review.sh's descendant namespace to the declaration. Cover pr-feedback/gate collectors and review descendants without editing their sources or adding wrappers.
    77	   Require the declared version-specific absolute realpath, regular executable, existence, non-shim/trusted-root checks and matching reported version; consume that checked target without rediscovery. Missing/mismatching identity emits exactly "refused: gh binding", exits nonzero and performs no canonical operation; no PATH/mise/latest fallback for gh.
    78	   gh api uses --hostname github.com and fixed repos/mryfmo/dotfiles endpoints; other subcommands use --repo github.com/mryfmo/dotfiles or a full fixed-host URL under item 8. Do not add the unsupported --hostname flag to gh pr; version probes make no network call.
    79	   R1:39: before any script, loader, resolver or parser runs with credentials, the orchestrator supplies and measures the trusted parent required by items 2/9, binding Bash, mise, git, uv, Python, Node and every other non-gh executable the selected route can execute.
    80	   Keep today's non-gh resolver algorithms, but constrain their execution and outputs to that preverified private namespace; discovery receives no tokens. A PATH- or mise-selected unchecked parent is forbidden. No self-reexec, sentinel or child cleanup counts as pre-exec evidence; without this compensating control authenticated operation stays blocked.
    81	4. R1:76: launch every bound gh, including identity probes, with a constructed allowlist and protected GH_CONFIG_DIR=/var/empty on this host; verify its resolved directory and ancestors are protected, it is empty and contains no symlink/config payload. Missing/unsafe configuration refuses, without default-home fallback or directory creation.
    82	   Only the call's explicitly supplied token is inherited, normalized to GH_TOKEN; never fetch credentials implicitly from home config/keychain. Supply required nonsecret constants explicitly, including trusted HOME/PATH, absolute UV_CACHE_DIR, fixed configuration, disabled prompts/update notices and plain output; probes get no token.
    83	   Reject ambient GH_HOST/GH_CONFIG_DIR/XDG_CONFIG_HOME, proxies, loader/startup variables and Git configuration overrides. Apply items 2/9 to the parent and descendants too; every env -i contract carries UV_CACHE_DIR. Record the complete allowed-name set without token values.
    84	   Test planted home/XDG gh config with http_unix_socket, aliases and alternate hosts; neither transport nor child execution may change. Test refusal of unsafe configuration and a positive authenticated operation using the controlled source. Sources: [gh config](https://cli.github.com/manual/gh_config), [configuration discovery](https://cli.github.com/manual/gh_help_environment).
    85	5. No workflow/regime.yml, launcher, permission, dependency, unrelated resolver algorithm or acceptance-semantic change. No new/renamed executable or executable evidence. Future checkers and missing consumers remain explicitly owned, never represented as implemented here.
    86	6. The test wildcard authorizes only test_supply_chain_policy.py, test_chain_glue.py, test_regime_ci.py and test_task_checkers.py; reuse trusted_exec_contract.py without modifying it and preserve existing assertions.
    87	   R1:38: fix reused chain/regime/checker fixture Git helpers before any init/add/commit/reset/fetch: construct fresh environments, explicit fixture roots and neutralized configuration; do not merge os.environ. Plant GIT_DIR/GIT_WORK_TREE/GIT_CONFIG_* and hostile local includes/hooks; a second disposable repository's refs/index/bytes and external markers must stay unchanged. See [Git environment](https://git-scm.com/docs/git).
    88	   R1:80: each active route needs a successful authenticated-operation fixture through the declared target, with a synthetic credential, expected fixed host/repository, response consumption and descendant coverage; separately test missing/version/path refusals. Identity refusal can never satisfy a success or decoy assertion.
    89	   Put an executable gh decoy on the lookup path and a hostile mise answer; prove neither is executed or receives the synthetic credential. The trusted-parent fixture binds non-gh tools but must not prebind gh and thereby mask the production defect.
    90	   Implement every closed selector above; the policy test uses separate subtests per refusal rule, and the consumer/environment/configuration matrices cover all three active routes. Absent future routes are not passing matrix entries.
    91	   Write fixtures first; for each behavioral case record red against origin/main production bytes and green at the fix commit, with selector, full baseline/red-fixture/fix SHAs, exact commands, stdout/stderr and exit status. Red must reach its intended assertion, not import/setup/missing-tool failure; inventory-only requirements use diff evidence, not fabricated red tests.
    92	
    93	## Check
    94	
    95	The final diff has at most 350 changed lines outside `tests/` and `.orchestration/`, and at most 700 under `tests/`.
    96	Measure with git diff --numstat <merge-base40> <head40>.
    97	Caps are PR-wide additions plus deletions from git merge-base <authenticated-main40> <head40> (C-123), not round deltas. Record dispatch measurement_base40, final full SHAs, every numstat row and both totals; recount after update-branch. Expected width is about 200/400; headroom covers parent/configuration fixtures and one Bot fix round. The a07 rewrite's 446/709 grants no exemption; an overrun blocks.
    98	Run uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_supply_chain_policy tests.unit.test_chain_glue tests.unit.test_regime_ci tests.unit.test_task_checkers -v with measured absolute uv/Python, item 9 isolation and a temporary absolute UV_CACHE_DIR; record the expanded invocation.
    99	Run bash -n, shellcheck and shfmt --indent 4 --space-redirects --diff on all three changed shells; run ruff check --config ruff.toml and ruff format --check --config ruff.toml on changed Python. Run make validate-agent-assets and the existing review gate. Never run Bats locally.
   100	Host resolution probe: /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" UV_CACHE_DIR="$UV_CACHE_DIR" "$HOME/.local/bin/mise" which uv; repeat with python and paste actual outputs, never guess a uv/bin path. These discovery observations alone do not establish trusted-parent deployment.
   101	
   102	## Execution and evidence
   103	
   104	Worker Playbook step 4 applies: every command sandboxed; any denial sends AGMSG-PONG v1 task_id=dotfiles-T133-gh-binding-a01 status=blocked with exact command, exit status and boundary, then holds. Never escalate, probe Herdr sockets or retry through another surface.
   105	Create tools/gh-binding-a01 from origin/main with git switch -c tools/gh-binding-a01 --no-track origin/main. Push HTTPS with git push https://github.com/mryfmo/dotfiles.git tools/gh-binding-a01, never -u or shared config changes; open one draft PR. Follow step 15's CI/Bot wait, at most one worker Bot fix round; surviving P0/P1 stops for the operator. Worker never merges.
   106	Under .orchestration/dotfiles-T133-gh-binding-a01/ write task.md byte-identical to the complete anchored dispatch, report.md, validation.md with verbatim command stdout/stderr and real exit statuses, sandbox.md, learning.md, autoskill.md and result.txt; keep artifacts non-executable and secret-free.
   107	Every evidence item names its producer/seat: worker (Codex seat), orchestrator (Claude seat, sandboxed Bash), or author (Codex review-profile seat, sandboxed exec) for the observations below. report.md maps rows/selectors, scope, counts, red/green pairs and limitations; sandbox.md records denials, learning.md triage, autoskill.md actual use/not-used, cost n/a unless measured.
   108	Write AGMSG-RESULT v1 before sending: task_id, status, pr, literal head=<full40>, authenticated_main=<full40>, merge_base=<full40>, source_cap=350, test_cap=700, source_changed/test_changed, every red/green SHA pair, task_copy=<repo-local task.md>, task_copy_sha256 and artifact paths. ready_for_review requires passing CI.
   109	Keep plan/todo/learn updated and uncommitted, one active todo per owner. Use agent-side Crit data/evidence only; no browser or publication. Satisfy make require-crit-review and its receipt before RESULT. The orchestrator alone follows Playbook step 10's feedback, audit, acceptance, gate and integration order.
   110	
   111	## Anchor
   112	
   113	R1:110: the observed Checks below explicitly block anchoring; no canonical clone or trusted-parent deployment was measured in this read-only authoring context. They are not an approval or substituted canonical evidence.
   114	Before C-80/anchor, the orchestrator expands the gh-binding-followup-a01 owner stub for every assigned residual and the three future consumers; confirms Item 0's amended inventory; obtains main40/design digest from a fresh private HTTPS bare clone of the fixed repository, gh-free and independent of the shared object store.
   115	Record exact sanitized producer commands/outputs and item 2/9 parent/namespace protection evidence separately; paste their observed identifiers and the host pin/version lines into the five payload lines below. Change dispatch_status only after all observations exist, then review and anchor the entire resulting bytes; any later paste invalidates that anchor.
   116	Installation is separate from code/CI: the orchestrator records the declared pinned install and protected config, then positive real consumer probes under the measured parent before enabling authenticated acceptance reads. a07/regime-ci future routes remain unclosed until their own adoption evidence exists.
   117	
   118	## Checks
   119	

exec
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-gh-binding-a01.md' in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc 'cat /Users/a0004262/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail-review/SKILL.md' in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n -A 42 -B 3 'Codex seat worklogs' /Users/a0004262/.agents/skills/agmsg-orchestration/SKILL.md; git status --short; cat .ua/meta.json" in /Users/a0004262/Workspace/dotfiles
 succeeded in 136ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-gh-binding-a01
     4	kind: code
     5	security: true
     6	dispatch_status: blocked-pre-anchor
     7	design_review: {design: .orchestration/plans/024-design-quality.md}
     8	requires_decision: [D-024-69]
     9	after: []
    10	allowed_files:
    11	  - home/dot_mise/config.toml
    12	  - home/dot_agents/agent-config.yaml
    13	  - scripts/validate-agent-assets.py
    14	  - scripts/orchestrator/chain-integrate.sh
    15	  - scripts/orchestrator/orch-gate.sh
    16	  - scripts/orchestrator/local-review.sh
    17	  - tests/unit/test_*.py
    18	  - .orchestration/dotfiles-T133-gh-binding-a01/**
    19	threat_table:
    20	  - {control: "home/dot_mise/config.toml", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_exact_pin"}
    21	  - {control: "home/dot_agents/agent-config.yaml", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
    22	  - {control: "scripts/validate-agent-assets.py", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
    23	  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_chain_integrate_authenticated_decoy"}
    24	  - {control: "scripts/orchestrator/orch-gate.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_orch_gate_authenticated_decoy"}
    25	  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_local_review_authenticated_decoy"}
    26	  - {control: "tests/unit/test_*.py", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence-integrity automation; limit edits to Item 6's four modules and independently inspect assertions and red/green logs."}
    27	  - {control: ".orchestration/dotfiles-T133-gh-binding-a01/** including task.md", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence automation; compare anchored bytes, task-copy digest and literal full head against the independently audited PR."}
    28	  - {control: "pin", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_exact_pin"}
    29	  - {control: "declaration", disposition: "closed: tests/unit/test_supply_chain_policy.py::GhBindingPolicyTest::test_gh_declaration_policy"}
    30	  - {control: "consumer binding", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_consumer_binding_matrix"}
    31	  - {control: "minimal environment", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_gh_environment_is_minimal"}
    32	  - {control: "gh configuration inputs", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_protected_gh_configuration"}
    33	  - {control: "trusted parent before first instruction", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns automatic parent binding; authenticated use stays disabled until the orchestrator measures a clean, absolutely bound parent and private namespace for every non-gh process in the route."}
    34	  - {control: "task metadata", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns dispatch automation; reviewed inventory and populated Checks must match the complete anchored task before dispatch."}
    35	  - {control: "metadata separators", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns byte-integrity automation; compare all front matter, separators and Checks, with no paste after anchor."}
    36	  - {control: "in-process effects", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_git_environment_cannot_redirect_fixture_writes"}
    37	  - {control: "workflow and interpreter or environment inputs", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns uv/Python/Node, permgate and launcher binding; unchanged resolvers run only inside Item 3's measured parent namespace, otherwise authenticated use is blocked."}
    38	  - {control: "new or renamed scripts; future gh routes", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns adoption by absent chain-finish and future checker gh routes; create no consumer here and require their own positive authenticated fixtures before claiming closure."}
    39	  - {control: "remaining git/date/mise executable provenance", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns permanent remaining-tool binding; today's resolver algorithms remain, constrained by the measured parent namespace and token-free discovery, with no authenticated fallback."}
    40	  - {control: "orchestrator effect merge", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns integration follow-through; only the orchestrator integrates the exact audited head through Playbook step 10."}
    41	  - {control: "orchestrator effect update-branch", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns evidence refresh; rerun CI, feedback, audit, acceptance and gate for every changed head."}
    42	  - {control: "orchestrator effect forced worker removal", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns teardown records; none is planned and no dirty state may be discarded without separate authorization."}
    43	  - {control: "orchestrator effect owner-stub amendment", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns every residual assigned here; the orchestrator expands its existing stub before anchor, outside worker scope."}
    44	  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns measurement automation; gh-free private-clone evidence and trusted-parent observations must precede a fresh review of the complete populated bytes."}
    45	  - {control: "orchestrator effect installation and deployment", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns deployment follow-through; separately verify the pinned install, protected configuration and real authenticated consumer probes before enabling acceptance reads."}
    46	  - {control: "design 5.14 item 0", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns the unchanged item 0 residual; this task establishes no same-UID or credential-separation boundary."}
    47	  - {control: "design 5.14 item 1", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns host protection evidence; item 1 must cover the declaration, binary, configuration source and parent namespace before authenticated use."}
    48	  - {control: "design 5.14 item 2", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns permanent item 2 integration; the measured trusted-parent compensating control is mandatory now."}
    49	  - {control: "design 5.14 item 3", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns wider item 3 integration; apply it to this task's gh inputs without certifying other runtime boundaries."}
    50	  - {control: "design 5.14 item 4", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns wider item 4 integration; checked gh identity is consumed directly and same-UID replacement remains item 0's residual."}
    51	  - {control: "design 5.14 item 5", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns unchanged item 5 obligations; retain full head identities and introduce no lock or reservation changes."}
    52	  - {control: "design 5.14 item 6", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns deployment verification; distinguish fixture success, CI and observed host execution under item 6."}
    53	  - {control: "design 5.14 item 7", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns wider item 7 coverage; independently check behavioral assertions and never count setup failure or absent routes as closure."}
    54	  - {control: "design 5.14 item 8", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns future canonical-reader adoption; apply item 8 to active gh routes and do not certify the current local-object checkers."}
    55	  - {control: "design 5.14 item 9", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns permanent item 9 integration; measured isolated runtimes and the parent's absolute UV_CACHE_DIR remain mandatory."}
    56	  - {control: "design 5.14 item 10", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns denial records; item 10 applies and any denied command stops work with a blocked PONG."}
    57	premises: []
    58	---
    59	
    60	# AGMSG-TASK dotfiles-T133-gh-binding-a01 — bind gh on the measured host
    61	
    62	D-024-69 supersedes the 2026-10-21 owner stub and pulls this remedy ahead of slices 2-5; pins-a01 merged as #449, after remains empty, and later tool declarations use sibling entries. TASK names worker a012, a Codex seat.
    63	Seven refused C-80 rounds: a07-checker 922292d/0edbd8c/fd8c003/c6cebe4/a3125e1; regime-ci-followup-a02 a232baf/a18a67d. Unbound gh can forge canonical main, design, merge state and PR data and read forwarded credentials.
    64	Design 5.14 items 0-10 apply by reference, particularly 2-4/9; do not restate their trusted-execution contract.
    65	R1 references below identify original lines of .orchestration/tasks/dotfiles-T133-gh-binding-a01.md: 39→Item 3; 76→Item 4; 38/80→Item 6; 105→Item 0; 110→Anchor.
    66	
    67	## Items
    68	
    69	0. Reviewed baseline amendment for R1:105: local HEAD and origin/main are 7da0cdfab9de9fbea673b82379acd4e317115065; chain-finish.sh is absent, and regime-ci.py/task-consistency-check.py currently use Git, not gh lookups. These are local observations, not authenticated canonical facts.
    70	   Implement the three present shell routes, including their actual gh descendants; do not invent a finish script or add canonical-network behavior to either checker. Future gh adoption belongs to dotfiles-T133-gh-binding-followup-a01 and requires positive authenticated fixtures in those owners.
    71	   This explicit inventory amendment requires C-80 approval with gh-free canonical confirmation before dispatch. If the canonical baseline differs, reauthor and review the whole inventory and threat table; never silently widen scope or claim six routes were closed.
    72	1. Pin "github:cli/cli" = "2.102.0" in home/dot_mise/config.toml, with one adjacent English reason comment following pins-a01; extend the exact-version assertion and retain unrelated pins.
    73	2. Add trusted_tools.gh with version "2.102.0" and path "~/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh" to agent-config.yaml; later uv/Python/Node bindings extend sibling entries.
    74	   validate-agent-assets.py checks version equals the mise pin, the spelling is normalized and home-anchored, expansion is absolute under the real user's trusted home, and neither spelling nor resolved path is under shims. Refuse missing/malformed declarations, traversal, forged HOME and mismatched identities; one refusal test per rule.
    75	   Runtime reads the protected deployed ~/.agents/agent-config.yaml as data using existing parsing facilities under the measured isolated interpreter; never source/eval it or read a PR/worker copy. Chezmoi already deploys this plain source file; no generated artifact is needed, so leave generate-agent-configs.py and its tests unchanged.
    76	3. Replace gh discovery in chain-integrate.sh and orch-gate.sh, and bind local-review.sh's descendant namespace to the declaration. Cover pr-feedback/gate collectors and review descendants without editing their sources or adding wrappers.
    77	   Require the declared version-specific absolute realpath, regular executable, existence, non-shim/trusted-root checks and matching reported version; consume that checked target without rediscovery. Missing/mismatching identity emits exactly "refused: gh binding", exits nonzero and performs no canonical operation; no PATH/mise/latest fallback for gh.
    78	   gh api uses --hostname github.com and fixed repos/mryfmo/dotfiles endpoints; other subcommands use --repo github.com/mryfmo/dotfiles or a full fixed-host URL under item 8. Do not add the unsupported --hostname flag to gh pr; version probes make no network call.
    79	   R1:39: before any script, loader, resolver or parser runs with credentials, the orchestrator supplies and measures the trusted parent required by items 2/9, binding Bash, mise, git, uv, Python, Node and every other non-gh executable the selected route can execute.
    80	   Keep today's non-gh resolver algorithms, but constrain their execution and outputs to that preverified private namespace; discovery receives no tokens. A PATH- or mise-selected unchecked parent is forbidden. No self-reexec, sentinel or child cleanup counts as pre-exec evidence; without this compensating control authenticated operation stays blocked.
    81	4. R1:76: launch every bound gh, including identity probes, with a constructed allowlist and protected GH_CONFIG_DIR=/var/empty on this host; verify its resolved directory and ancestors are protected, it is empty and contains no symlink/config payload. Missing/unsafe configuration refuses, without default-home fallback or directory creation.
    82	   Only the call's explicitly supplied token is inherited, normalized to GH_TOKEN; never fetch credentials implicitly from home config/keychain. Supply required nonsecret constants explicitly, including trusted HOME/PATH, absolute UV_CACHE_DIR, fixed configuration, disabled prompts/update notices and plain output; probes get no token.
    83	   Reject ambient GH_HOST/GH_CONFIG_DIR/XDG_CONFIG_HOME, proxies, loader/startup variables and Git configuration overrides. Apply items 2/9 to the parent and descendants too; every env -i contract carries UV_CACHE_DIR. Record the complete allowed-name set without token values.
    84	   Test planted home/XDG gh config with http_unix_socket, aliases and alternate hosts; neither transport nor child execution may change. Test refusal of unsafe configuration and a positive authenticated operation using the controlled source. Sources: [gh config](https://cli.github.com/manual/gh_config), [configuration discovery](https://cli.github.com/manual/gh_help_environment).
    85	5. No workflow/regime.yml, launcher, permission, dependency, unrelated resolver algorithm or acceptance-semantic change. No new/renamed executable or executable evidence. Future checkers and missing consumers remain explicitly owned, never represented as implemented here.
    86	6. The test wildcard authorizes only test_supply_chain_policy.py, test_chain_glue.py, test_regime_ci.py and test_task_checkers.py; reuse trusted_exec_contract.py without modifying it and preserve existing assertions.
    87	   R1:38: fix reused chain/regime/checker fixture Git helpers before any init/add/commit/reset/fetch: construct fresh environments, explicit fixture roots and neutralized configuration; do not merge os.environ. Plant GIT_DIR/GIT_WORK_TREE/GIT_CONFIG_* and hostile local includes/hooks; a second disposable repository's refs/index/bytes and external markers must stay unchanged. See [Git environment](https://git-scm.com/docs/git).
    88	   R1:80: each active route needs a successful authenticated-operation fixture through the declared target, with a synthetic credential, expected fixed host/repository, response consumption and descendant coverage; separately test missing/version/path refusals. Identity refusal can never satisfy a success or decoy assertion.
    89	   Put an executable gh decoy on the lookup path and a hostile mise answer; prove neither is executed or receives the synthetic credential. The trusted-parent fixture binds non-gh tools but must not prebind gh and thereby mask the production defect.
    90	   Implement every closed selector above; the policy test uses separate subtests per refusal rule, and the consumer/environment/configuration matrices cover all three active routes. Absent future routes are not passing matrix entries.
    91	   Write fixtures first; for each behavioral case record red against origin/main production bytes and green at the fix commit, with selector, full baseline/red-fixture/fix SHAs, exact commands, stdout/stderr and exit status. Red must reach its intended assertion, not import/setup/missing-tool failure; inventory-only requirements use diff evidence, not fabricated red tests.
    92	
    93	## Check
    94	
    95	The final diff has at most 350 changed lines outside `tests/` and `.orchestration/`, and at most 700 under `tests/`.
    96	Measure with git diff --numstat <merge-base40> <head40>.
    97	Caps are PR-wide additions plus deletions from git merge-base <authenticated-main40> <head40> (C-123), not round deltas. Record dispatch measurement_base40, final full SHAs, every numstat row and both totals; recount after update-branch. Expected width is about 200/400; headroom covers parent/configuration fixtures and one Bot fix round. The a07 rewrite's 446/709 grants no exemption; an overrun blocks.
    98	Run uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_supply_chain_policy tests.unit.test_chain_glue tests.unit.test_regime_ci tests.unit.test_task_checkers -v with measured absolute uv/Python, item 9 isolation and a temporary absolute UV_CACHE_DIR; record the expanded invocation.
    99	Run bash -n, shellcheck and shfmt --indent 4 --space-redirects --diff on all three changed shells; run ruff check --config ruff.toml and ruff format --check --config ruff.toml on changed Python. Run make validate-agent-assets and the existing review gate. Never run Bats locally.
   100	Host resolution probe: /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" UV_CACHE_DIR="$UV_CACHE_DIR" "$HOME/.local/bin/mise" which uv; repeat with python and paste actual outputs, never guess a uv/bin path. These discovery observations alone do not establish trusted-parent deployment.
   101	
   102	## Execution and evidence
   103	
   104	Worker Playbook step 4 applies: every command sandboxed; any denial sends AGMSG-PONG v1 task_id=dotfiles-T133-gh-binding-a01 status=blocked with exact command, exit status and boundary, then holds. Never escalate, probe Herdr sockets or retry through another surface.
   105	Create tools/gh-binding-a01 from origin/main with git switch -c tools/gh-binding-a01 --no-track origin/main. Push HTTPS with git push https://github.com/mryfmo/dotfiles.git tools/gh-binding-a01, never -u or shared config changes; open one draft PR. Follow step 15's CI/Bot wait, at most one worker Bot fix round; surviving P0/P1 stops for the operator. Worker never merges.
   106	Under .orchestration/dotfiles-T133-gh-binding-a01/ write task.md byte-identical to the complete anchored dispatch, report.md, validation.md with verbatim command stdout/stderr and real exit statuses, sandbox.md, learning.md, autoskill.md and result.txt; keep artifacts non-executable and secret-free.
   107	Every evidence item names its producer/seat: worker (Codex seat), orchestrator (Claude seat, sandboxed Bash), or author (Codex review-profile seat, sandboxed exec) for the observations below. report.md maps rows/selectors, scope, counts, red/green pairs and limitations; sandbox.md records denials, learning.md triage, autoskill.md actual use/not-used, cost n/a unless measured.
   108	Write AGMSG-RESULT v1 before sending: task_id, status, pr, literal head=<full40>, authenticated_main=<full40>, merge_base=<full40>, source_cap=350, test_cap=700, source_changed/test_changed, every red/green SHA pair, task_copy=<repo-local task.md>, task_copy_sha256 and artifact paths. ready_for_review requires passing CI.
   109	Keep plan/todo/learn updated and uncommitted, one active todo per owner. Use agent-side Crit data/evidence only; no browser or publication. Satisfy make require-crit-review and its receipt before RESULT. The orchestrator alone follows Playbook step 10's feedback, audit, acceptance, gate and integration order.
   110	
   111	## Anchor
   112	
   113	R1:110: the observed Checks below explicitly block anchoring; no canonical clone or trusted-parent deployment was measured in this read-only authoring context. They are not an approval or substituted canonical evidence.
   114	Before C-80/anchor, the orchestrator expands the gh-binding-followup-a01 owner stub for every assigned residual and the three future consumers; confirms Item 0's amended inventory; obtains main40/design digest from a fresh private HTTPS bare clone of the fixed repository, gh-free and independent of the shared object store.
   115	Record exact sanitized producer commands/outputs and item 2/9 parent/namespace protection evidence separately; paste their observed identifiers and the host pin/version lines into the five payload lines below. Change dispatch_status only after all observations exist, then review and anchor the entire resulting bytes; any later paste invalidates that anchor.
   116	Installation is separate from code/CI: the orchestrator records the declared pinned install and protected config, then positive real consumer probes under the measured parent before enabling authenticated acceptance reads. a07/regime-ci future routes remain unclosed until their own adoption evidence exists.
   117	
   118	## Checks
   119	

 succeeded in 163ms:
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

 succeeded in 243ms:
222-    - Fix P0/P1 findings, inline or review-body, in at most one worker-side fix round before RESULT, then request `@codex review` and restart the wait from the push. A P0/P1 surviving that round is not fixed again: send `AGMSG-RESULT … bot_rounds=2` with each listed as `open:<thread id>` (`open:review-<review id>` for a review-body finding); this stops the PR for the operator's decision, and the next bullet's `fixed:`/`not-applicable:` rule does not override it.
223-    - Apart from those surviving P0/P1 items, the RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>` under Orchestrator Playbook step 10. The worker resolves no thread.
224-
225:## Codex seat worklogs
226-
227-Project layouts vary by language. Set up this worklog structure only when it
228-does not already exist, and use timestamped filenames in `YYYYMMDD_HHMMSS`
229-form:
230-
231-- `.agents/worklog/codex/plan/<timestamp>_plan.md` stores the plan and design
232-  written before implementation. Ask the user questions when needed, and
233-  update the plan when questions, learning, or completed tasks change it. It
234-  must contain `Goal`, `Scope`, `Assumptions`, `Design`, `Tests`, and
235-  `Open Questions`.
236-- `.agents/worklog/codex/todo/<timestamp>_todo.md` derives its tasks from the
237-  plan. Move completed items from `TODO` to `Done`; when `TODO` is empty, set
238-  its status to `done` and rename it to `<timestamp>_done.md`. It must contain
239-  `TODO` and `Done`.
240-- `.agents/worklog/codex/learn/<timestamp>_learn.md` records only reusable,
241-  validated knowledge that speeds a future decision. State what was learned
242-  and where it applies, update the plan's `Assumptions`, `Design`, or `Tests`
243-  when relevant. A learn file must contain `Date`, `Learnings`, and
244-  `Plan Updates`.
245-
246-Every plan, todo, and learn file starts with YAML frontmatter containing
247-`type` (`plan`, `todo`, or `learn`), `id` (`YYYYMMDD_HHMMSS`), `owner` (for
248-example, `codex-a`), and ISO8601 `created_at` and `updated_at`. Additionally:
249-
250-- todo requires `status`, `workstream`, and `related_plan`; status is one of
251-  `active`, `blocked`, `done`, or `superseded`;
252-- plan requires `status`, one of `draft`, `active`, `done`, or `superseded`;
253-- learn requires `validated` (`true` or `false`) and `apply_to` (plan/tests),
254-  and may be created only when reusable and validated.
255-
256-Optional frontmatter keys are `depends_on` (todo ID array), `blocked_reason`
257-for blocked work, `evidence` (path array), and `tags`.
258-
259-## Pitfalls
260-
261-- Do not start work from the agmsg message alone; read `task_file` first.
262-- Do not edit outside `allowed_files`, even for convenient cleanup.
263-- Do not perform forbidden actions such as dependency changes, gate changes, product changes, promotion decisions, image builds, or LLM calls when listed.
264-- Do not collapse candidate, promoted, rejected, and merged skill registry states into one directory.
265-- Do not put secrets, raw logs with credentials, or unredacted AutoSkill inputs in artifacts.
266-- Do not wake workers with `pane send-text` + `send-keys Enter`; use `agmsg-dispatch`, `poke.sh --body-file`, or `send.sh --body-file` as step 6 selects, and verify `read_at` in messages.db.
267-- Do not treat `AGMSG-ACCEPTANCE status=revise` as a new task unless it changes the task file or explicitly provides a next action.
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
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-1d72f16.md.last.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-audit-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-1d72f16.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-chain-7888241.log
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-local-review-1d72f16.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a02-security-7888241.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md
?? .orchestration/validation/dotfiles-T133-pre-send-check-a03-audit-a30a43b.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-e39dc8f.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-slice1-a01-text-security-f4246e9.md.last.md
?? .orchestration/validation/records-sync-30-pr-comments.json
?? .orchestration/validation/records-sync-30-pr-feedback.json
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

**Optimizing output and querying**
exec
/bin/zsh -lc "git rev-parse HEAD; git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- scripts home tests; /usr/bin/python3 -c 'import json; g=json.load(open(\".ua/knowledge-graph.json\")); print(\"\\n\".join(str({k:n.get(k) for k in (\"filePath\",\"summary\")}) for n in g.get(\"nodes\",[]) if any(s in n.get(\"filePath\", \"\") for s in (\"chain-integrate\", \"orch-gate\", \"local-review\", \"pr-feedback\", \"trusted_exec\"))))'" in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n '5\\.14|D-024-69' .orchestration/plans/024-design-quality.md .orchestration/decisions.tsv; sed -n '1,180p' .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md; cat .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md; cat .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md" in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-pins-a01.md; cat .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a02.md; cat .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a18a67d.md.last.md; cat .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-a3125e1.md.last.md' in /Users/a0004262/Workspace/dotfiles
 succeeded in 205ms:
.orchestration/plans/024-design-quality.md:95:### 5.14 残余（凍結後の計測事実、D-024-29）
.orchestration/plans/024-design-quality.md:103:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
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
.orchestration/decisions.tsv:86:D-024-38	2026-10-20T07:34Z	Records PR #438 (head 041a906b3fc36be5aa7bc18630542127d6efce8c, ten dispatched task texts) is approved by the operator's written instruction in the orchestrator session at 2026-10-20 16:3x JST ("#438は承認したので、そちらで作業を承認したうえですすめること"); merged by the orchestrator with `gh pr merge --squash --match-head-commit 041a906b…` at 07:31:17Z as main f7ed01427a43567b9c1857d2f62953add8b97c92; the dependents (#436, #432, #439, #437, #441) take the new base with `gh pr update-branch` and run their chains; the operator's sentence also delegates the ordinary acceptances of those PRs to the orchestrator's judgement, as the regime already does.	design 5.14 item 8 makes the operator's approval the authority for records PRs (D-024-33); seven PRs were regime-red on the records gap for 4 h 13 min (12:18-16:31 JST).	design 5.14 item 8; D-024-33; the 16:27 JST report	applied 2026-10-20 16:34 JST
.orchestration/decisions.tsv:88:D-024-40	2026-10-20T08:11Z	A records PR that carries only dispatched task texts (each byte-identical to the `task_sha256` of its latest `AGMSG-TASK` message, verifiable from the agmsg store) and no decision, plan, design or rule change is merged by the orchestrator under the final-integration exemption once CI is green, with `--match-head-commit`; a records PR that carries decisions.tsv, plans, design or rule text keeps the operator's written approval (design 5.14 item 8, D-024-33). First application: PR #443 (the a06-checker and pre-send-check texts).	design 5.14 item 8 binds the operator's approval to decision lines read from the committed ledger; a dispatched text is already the orchestrator's act of record on the bus, and regime-ci needs it on main before the worker's PR can pass, so every reset or amendment otherwise waits hours for an approval that adds no information (#438: 4 h 13 min for seven PRs); the operator's instruction of 16:3x JST ("そちらで作業を承認したうえですすめること") delegates the ordinary acceptances to the orchestrator.	design 5.14 item 8; D-024-33; D-024-38; M-20261020-02	applied 17:11 JST; the operator may redirect it (the next report names it)
.orchestration/decisions.tsv:89:D-024-41	2026-10-20T09:22Z	The chain-review-scripts a07 lineage (PR #439) resets to dotfiles-T128-chain-review-scripts-followup-a08 (another context): INV-6 S2 was reached by two amendments, one of them the orchestrator's erroneous resend 2710 (M-20261020-03), and the audit's P1 (review content read from the worker-writable shared object store; design 5.14 item 8) needs a new item: local-review.sh reads the head from a private bare clone fetched from GitHub at the 40-hex sha and runs the review there. The implementation at a644a7d9 stands; the pre-written a08 owner text becomes a09.	the audit of a644a7d9 (09:21Z); C-61 (a third worker round is not available after S2); design 5.14 item 8	INV-6 S2; C-61; design 5.14 item 8; the a07 record	applied 18:22 JST
.orchestration/decisions.tsv:93:D-024-45	2026-10-20T11:45Z	Design 5.14 item 10 (every worker command inside the sandbox) contradicts the seat configuration that runs `agmsg-dispatch` through excludedCommands outside the sandbox (audit:7eab146:1, audit:6434c27:1; the a008 seat's sandbox.md:18). The design is frozen (D-024-29), so the choice is the operator's: default = record a control-plane exemption for `agmsg-dispatch` in 5.14 item 10 by a design-amendment task (the bus is the regime's control plane, not a repository mutation; the herdr socket is already in the sandbox allowlist, so the alternative, running it inside, is tested first by a Claude seat); until decided, the finding is recorded as it stands on every affected lineage and never dispositioned fixed. Placed in the project map's decisions panel with that default.	recorded in the what column (row written in the 4-column form id/when/what/decider; converted to the 6-column header 2026-10-21T00:1x JST)	claude-deep-dot	revoked by D-024-46
.orchestration/decisions.tsv:94:D-024-46	2026-10-20T12:20Z	D-024-43 and D-024-45 are revoked after the operator's question of 21:0x JST. (1) result-evidence-check-a01 was a lineage outside plan 024 that overlapped P1-5's result-precheck.sh and took C-80 reviews that C-80 reserves for security: true texts; the lineage is withdrawn (record kept), its two checks (the validation's base/candidate comparison and the head's CI as read by the orchestrator) become items of P1-5's follow-up owner `dotfiles-T133-result-precheck-followup-a01`, and the glue `result-evidence-check.sh` stays orchestrator-side. (2) Design 5.14 item 10 already orders the worker seats' excludedCommands emptied (024-design-quality.md:116); it was never assigned a Phase 1 task, so the `agmsg-dispatch *` exclusion of agent-config.yaml:285 (based on the T39 measurement that the T130 socket allowlist superseded; this seat sent messages 2827 and 2830 from sandboxed Bash) is implemented by a task routed to a Codex seat (Claude boundary), with permgate untouched (operator step per the design) and the Linux behaviour measured in CI as the task's residual. No design change is needed and no operator decision is pending.	recorded in the what column (row written in the 4-column form id/when/what/decider; converted to the 6-column header 2026-10-21T00:1x JST)	claude-deep-dot	applied
.orchestration/decisions.tsv:95:D-024-47	2026-10-20T14:22Z	The operator's written instruction of 23:2x JST ("承認するので、そちらで実施"): (1) the plan-amendment records PR (backlog table: #387/#432 to stop + hold with the a06 reset after Phase 1, #417 close, #378 merge, #396 and #404 continue; Phase 1 rows P1-16 design 5.14 item 10 implementation and P1-17 regime CI token; the transport procedure of D-024-36 as a Playbook item) is approved in advance and the orchestrator merges it under the final-integration exemption once CI is green, with --match-head-commit; (2) after P1-14 a05 merges, the orchestrator runs `make update` and re-seats the Codex workers itself as the default procedure, reporting any permission refusal (the remove-worker classifier) at that moment instead of asking beforehand.	recorded in the what column (row written in the 4-column form id/when/what/decider; converted to the 6-column header 2026-10-21T00:1x JST)	operator (moriya-fumio-thd)	in progress: boundary-26 records PR assembled 2026-10-20T15:1xZ; make update and the Codex re-seat follow the P1-14 a05 merge
.orchestration/decisions.tsv:102:D-024-54	2026-10-21T06:12Z	a08 (dotfiles-T128-chain-review-scripts-followup-a08, dispatched to codex-standard-dot-a013 as TASK 2972): the operator chose option A at 15:1x JST: keep a08 held at a013 (ACCEPTANCE 2975 status=hold) until the P1-15 deployment (stage A/B, slices 1-5 merged and installed) exists and the orchestrator records the deployed design 5.14 items 1-4/9 protection that a08 line 63 requires; the text is unchanged, so no further C-80; a013 takes no other task meanwhile (none is dispatchable)	a08 line 63-65/87 hold the task and PR behind that evidence; the dispatch against the text's own precondition was the orchestrator's mistake (M-20261021-06); amending the text (option B) would need a new re-plan line and a C-80 round after the codex route returns, and withdrawing (option C) adds steps without freeing useful capacity	PONG 2974 (a013, status=blocked reason=pre-dispatch-deployment-evidence-unverified); canonical clone at 60a6fb2b; send-task.sh precondition guard probed REFUSED on line 63	a08 held; release follows the P1-15 deployment record; a013 idle
.orchestration/decisions.tsv:106:D-024-58	2026-10-21T08:07Z	PR #440 (task-generator-plan-check a06-checker, a012) round 2 head c439b63c: the task-level audit is incorrect with an implementation P1 (C15 accepts arbitrary invariants when design_review.design is omitted) and three implementation P2; per D-024-57 the lineage resets to dotfiles-T133-task-generator-plan-check-a07-checker by another context: the a07 text continues PR #440's branch from c439b63c and fixes the P1, the three audit P2, the local decode abort, the two round-2 security symlink P2 and the UV_CACHE_DIR refusal of design 5.14 item 9 (the R1 revise had wrongly directed a fallback), with one red-then-green fixture each; caps measured from the merge-base at RESULT; Checks complete before the anchor review; a Codex seat other than a012 implements; executed as the recommended default under the operator's 15:1x JST standing instruction	D-024-57 fixed the consequence in advance; the mechanism-PR two-round limit forbids a third round; the orchestration rows 8 and 9 are the orchestrator's own errors and are corrected in the a07 text rather than by a worker	audit …-audit-c439b63.md.last.md; measurement git diff --numstat e00de4e0 c439b63c = 446/709; counters snapshot in the record; security review …-security-2cb5848.md.last.md (2 P2)	a012 hold sent (2983); a07 brief written; author-loop is the next operator line after the pins chain
.orchestration/decisions.tsv:113:D-024-65	2026-10-21T21:30Z	a07-checker (reset of a06, PR #440): after five C-80 rounds (922292d, 0edbd8c, fd8c003, c6cebe4, a3125e1), all incorrect on the executable-provenance class (gh, then bare git, then GIT_* sanitisation, then the checker's forwarded credentials), the operator chose option A at 06:3x JST: hold the a07 text until the trusted-entrypoint binding is deployed on the host (dotfiles-T133-trusted-entrypoint-binding-a01 and dotfiles-T133-gh-binding-a01, design 5.14 items 2-4/9); #440 stays open with its audit P1 (C15) unfixed and main keeps the pre-a06 checker; #411 waits behind #440 (D-024-62); the C-80 resumes on the a07 bytes after the binding; options B (operator waiver of the surviving P1) and C (pull the binding ahead of slices 2-5) were declined	no text can bind an executable; the reviewer's requirement is a host property (bound gh/git/uv/python) that only the binding tasks establish, exactly the wall a08 declared at its line 63; the regime's rule forbids dispatching a text with a surviving P1	five .last.md verdicts; the a07 record's re-plan line executable-provenance (3 reviews consumed under it incl. this one); C-92	a07 held (undispatched); ledger 440/411 -> held-behind-binding; the binding tasks' order unchanged (R2-15b)
.orchestration/decisions.tsv:114:D-024-66	2026-10-21T22:12Z	PR #442 (pre-send a03, a009) round-1 head a30a43ba: the task-level audit is incorrect with nine P2 and no P1; round 2 (the last) runs with amendment 1 of the a03 text (UV_CACHE_DIR private cache with refusal when absent per design 5.14 item 9; one red-then-green fixture per implementation row; verbatim evidence incl. CI watch and Bot wait); the sandbox-exception row is owned by worker-sandbox-exclusions-followup-a01 and the record-placement row is fixed by the orchestrator; the private-cache class reached three rows across a06/a07/a03 -> re-plan line private-cache-contract and a pre-send.sh guard; executed as the recommended default under the 15:1x JST standing instruction (the operator asked for fewer confirmations; this is the per-class re-plan the feedback rule names, reported here instead of asked)	no P1 remains, the lineage has its second round available, and the five parser edge cases are exactly what a round is for; the private-cache omission was the orchestrator's brief error three times	audit …-audit-a30a43b.md.last.md; pre-send.sh private-cache guard probed refused on the dispatched a03 bytes; local review 4 advisory rows	amendment 1 written and sent as ACCEPTANCE revise round=2 to a009; after its RESULT: CI, chain (local review cached by head? no: new head -> fresh), gate, merge
.orchestration/decisions.tsv:117:D-024-69	2026-10-21T22:58Z	gh binding pulled forward (operator 07:5x JST: use the essential remedy, not an expedient): dotfiles-T133-gh-binding-a01 (pin github-cli in home/dot_mise/config.toml, declare the absolute gh path beside uv/Python/Node in agent-config.yaml, make the orchestrator scripts' resolver and the checker's executable() use the declared path with --hostname github.com, one refusal test per route) is authored now (author-loop, C-80), anchored and dispatched to the free Codex seat a012 ahead of slices 2-5 and of trusted-entrypoint-binding-a01; a07 (D-024-65) and regime-ci-followup-a02 resume their C-80 after it merges; options B (keep the order) and C (a CI-side waiver) were declined by the operator's instruction	seven C-80 rounds across a07 and regime-ci-followup-a02 refused the same executable-provenance class; only a host binding of gh closes it; the operator ruled for the essential means	text-security verdicts 922292d/0edbd8c/fd8c003/c6cebe4/a3125e1 (a07) and a232baf/a18a67d (regime-ci-followup-a02); gh is mise-managed at github-cli-cli/latest, unpinned	brief next; dispatch to a012 after the anchor review
- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:39` — Deferring parent/interpreter binding supplies no compensating control: retained mise/PATH-selected processes execute before the proposed `gh` checks and can replace their decisions or capture credentials; cleaning only the child environment cannot establish the claimed consumer binding, especially outside Linux’s sandbox.

- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:76` — The environment allowlist omits a control and test for `gh`’s configuration-file inputs: default home configuration can select `http_unix_socket`, changing the actual transport despite a pinned executable and explicit hostname; require a protected, controlled configuration source. [GitHub CLI configuration](https://cli.github.com/manual/gh_config), [configuration discovery](https://cli.github.com/manual/gh_help_environment).

- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:38` — The named child-environment test cannot close in-process effects: the reused chain/regime fixtures inherit `GIT_*` into Git writes, allowing `GIT_DIR`/`GIT_WORK_TREE` to redirect operations outside their temporary repositories and `GIT_CONFIG_*` to inject configuration. [Git environment](https://git-scm.com/docs/git), [configuration overrides](https://git-scm.com/docs/git-config).

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:80` — Allowing an identity refusal to satisfy each decoy test does not prove successful consumer binding; require a positive authenticated-operation fixture per route, alongside refusal cases, to prevent an always-refusing implementation from satisfying the binding evidence.

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:105` — The stated baseline is inaccurate: `chain-finish.sh` is absent from this checkout and local `origin/main`, and neither Python checker contains the claimed `gh` lookup; with creation forbidden and `after: []`, the six-route implementation requires the reviewed amendment this line prescribes.

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:110` — `Checks` is empty despite requiring populated measurements before C-80; these bytes provide no observed canonical-source, installation or interpreter-binding evidence, and approval cannot cover a later paste.

📝 まとめ: Reviewed all 37 threat rows and cited acceptance/review history; findings remain input for the orchestrator. No files changed.

Not checked: future implementation, CI or live Linux/race behavior; same-user replacement and credential-sharing risks remain.
Verdict: incorrect---
format: 2
task_id: dotfiles-T133-gh-binding-followup-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/validate-agent-assets.py
  - .orchestration/dotfiles-T133-gh-binding-followup-a01/**
after: [dotfiles-T133-gh-binding-a01]
---

# AGMSG-TASK dotfiles-T133-gh-binding-followup-a01 — owner of the gh-binding-a01 residual rows (owner stub)

Owner stub written 2026-10-21T22:59Z by the orchestrator seat (C-51); never dispatched as a stub.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
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
```

## Orchestrator note (2026-10-21T08:31Z): the pins test moves with the command form

The pins PR (#449, head 28dde0f5) refactored `test_managed_hooks_use_installed_permgate_paths` to split the rendered PermissionRequest command with `rsplit(" ", 1)` and assert the permgate executable leaf and the `claude` argument; that assertion encodes the pre-binding shell form and raises ValueError on this task's `command: "/usr/bin/env"` plus `args` form (audit:28dde0f:1 of the pins lineage). `tests/unit/test_generate_agent_configs.py` is therefore in this task's allowed_files: the worker updates that test together with the command form, asserting the executable leaf and the `permission-request` operand from `args` instead of a split string, and keeps the exact-pins test green. Its former out_of_scope row read: "dotfiles-T133-trusted-entrypoint-pins-a01 removes the installed-template legacy literal pin without relaxing synthetic legacy migration cases"; that constraint still holds (the synthetic legacy migration cases stay unrelaxed), only the ownership of the file moved here.

 succeeded in 273ms:
---
{
  "format": 1,
  "task": "dotfiles-T133-trusted-entrypoint-pins-a01",
  "head": "28dde0f5933abee4355892401a13be9c05054326",
  "pr": 449,
  "ledger": [
    {
      "id": "audit:28dde0f:1",
      "class": "successor-scope"
    },
    {
      "id": "audit:28dde0f:2",
      "class": "checks-omission"
    }
  ],
  "searches": [],
  "audit_findings": [
    {
      "n": "1",
      "reason": "the pins assertion encodes the pre-binding shell form correctly; the successor binding task's allowed_files now include tests/unit/test_generate_agent_configs.py and its note moves the assertion with the command form",
      "evidence": "awk '/^allowed_files:/' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md | grep -c test_generate_agent_configs"
    },
    {
      "n": "2",
      "reason": "orchestration finding corrected in this record: the pre-dispatch checks the text requires were run post hoc with pasted output (pre-send OK, premise re-probe at e042663b, origin/main and 28dde0f5), the wrong \"no premises\" statement is withdrawn, and send-task.sh refuses an empty Checks block from now on",
      "evidence": "bash .agents/worklog/orchestrator-glue/pre-send.sh .orchestration/tasks/dotfiles-T133-trusted-entrypoint-pins-a01.md"
    }
  ]
}
---

# Acceptance record: dotfiles-T133-trusted-entrypoint-pins-a01

The separate pins task extracted from `dotfiles-T133-trusted-entrypoint-binding-a01` lines 398-417 (re-plan v2 R2-15a, r2 finding 11): pin uv 0.13.1, python 3.15.0, node 26.12.0 in `home/dot_mise/config.toml`; pins -> resolver -> binding. Seat: codex-standard-dot-a012 (worker-g).

- 2026-10-21T02:00Z: text authored by author-loop.sh from `brief-pins-a01.md` (99 lines, 3 allowed_files); C-80 round 1 (`…-text-security-0908b8f.md`) correct.
- 2026-10-21T02:04Z: dispatched (TASK 2926, sha 0908b8f4); paste-checks.sh failed on this text (no premise block), so the Checks block stayed empty. Held at 02:09Z over the allowed-file overlap with PR #448 (M-20261021-03); worktree collision reconciled (02:40Z); resumed 03:59Z after #448 merged.
- 2026-10-21T04:12Z: PONG 2953 status=blocked: the independent pre-push review found a P1: `tests/unit/test_supply_chain_policy.py:374-387` holds a map of pinnable tools and requires every other tool to be `latest` and a reason comment above each held line; node and uv are not in the map, so the pins fail that test, and the file is outside the text's three allowed_files. The text omitted the test (orchestrator brief defect). Amendment 1 (brief v2): allowed_files + that test, held entries for node and uv, reason comments, caps 16/48.

text-security:0908b8f:0	correct
worker:e042663:1	brief-omitted-consumer-test
- 2026-10-21T04:27Z: amendment 1 authored by author-loop.sh from `brief-pins-a01-v2.md` (109 lines, 4 allowed_files incl. tests/unit/test_supply_chain_policy.py; held entries for node and uv; reason comments; caps 16/48); C-80 round 2 (`…-text-security-70feed4.md`) correct; sent to a012 as amendment 1 at 2026-10-21T04:28Z (TASK 2955; send-task.sh refused the first line for the missing previous_task_sha256 token, C-121, and accepted it with the token 0908b8f4).

text-security:70feed4:0	correct
- 2026-10-21T08:14Z: defect sweep S1: this text was dispatched (amendment 1, sha 70feed416161304c90552bc8f7c169868a5b00e35857947a4855c9710ba92dbc) with an empty `## Checks (pasted by the orchestrator before each send)` block; the text defines no premise block for the paste (paste-checks.sh found none), so the heading is a template remainder, not an omitted measurement. Recorded here before the audit so the row, if raised, is dispositioned as an orchestrator text-shape defect: the dispatch facts were origin/main e042663b at dispatch (TASK line), the held-map conflict on tests/unit/test_supply_chain_policy.py resolved by amendment 1, and the worker's RESULT 2962 head 1f17d05f (update-branched to 28dde0f5 on 2026-10-21 08:06Z). send-task.sh now refuses an empty Checks block without `checks=none`.

## Final head 28dde0f5 (update-branch of 1f17d05f after boundary 27; PR patch unchanged): chain 2026-10-21T08:32Z

Chain (operator-run): CI 7 required green, GitGuardian "No secrets detected", local review 0 findings, sweep 5/5 (gaps 0), record block written. Task-level audit `…-audit-28dde0f.md.last.md`: **Verdict: incorrect**, one specification P1 and one orchestration P2; both dispositioned below (neither changes the PR's bytes), the security review of 28dde0f5 follows, then gate and merge.

audit:28dde0f:1	successor-scope
audit:28dde0f:2	checks-omission

Row 1 (P1, specification, task line 58): the refactored `test_managed_hooks_use_installed_permgate_paths` (tests/unit/test_generate_agent_configs.py:1476) splits the rendered PermissionRequest command with `rsplit(" ", 1)`, which encodes the pre-binding shell form; the binding task's `command: "/usr/bin/env"` plus `args` form (binding text line 181) would raise ValueError, and the binding text excluded this test file. The pins assertion is correct for the state the PR creates; the defect is the successor's scope. Fixed outside the PR: the undispatched binding text now lists `tests/unit/test_generate_agent_configs.py` in allowed_files, its exclusion row is amended, and an orchestrator note tells the worker to move the assertion to the `args` form together with the command (binding text sha ebc62361… before this note's final hash; re-hashed at dispatch).
Row 2 (P2, orchestration, this record's S1 note): the orchestrator's earlier statement that the text "defines no premise block" was wrong; the text has a `premises` entry (line 33 area: `rg -n '^(uv|python|node) = ' home/dot_mise/config.toml`) and line 96 requires C1-C10, C7b, C11 and the regime-copy checks before dispatch and acceptance, re-probing premises manually. Those checks were not run before the amendment-1 send (the omission is the orchestrator's); run post hoc 2026-10-21T08:32Z: `pre-send.sh` on the dispatched bytes -> `OK`, `secret-pattern: 0 match(es)`, `lines: 109`, sha 70feed41…; premise re-probe at the dispatch base e042663b and at origin/main e00de4e0: `3:node = "latest"`, `6:python = "3.15.0"`, `18:uv = "latest"`; at the head 28dde0f5: `4:node = "26.12.0"`, `7:python = "3.15.0"`, `20:uv = "0.13.1"`. send-task.sh now refuses an empty Checks block (C-130/S1).

audit-finding: 28dde0f:1 not-applicable:the pins assertion encodes the pre-binding shell form correctly; the successor binding task's allowed_files now include tests/unit/test_generate_agent_configs.py and its note moves the assertion with the command form; evidence=awk '/^allowed_files:/' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md | grep -c test_generate_agent_configs
audit-finding: 28dde0f:2 not-applicable:orchestration finding corrected in this record: the pre-dispatch checks the text requires were run post hoc with pasted output (pre-send OK, premise re-probe at e042663b, origin/main and 28dde0f5), the wrong "no premises" statement is withdrawn, and send-task.sh refuses an empty Checks block from now on; evidence=bash .agents/worklog/orchestrator-glue/pre-send.sh .orchestration/tasks/dotfiles-T133-trusted-entrypoint-pins-a01.md
- 2026-10-21T08:34Z: binding text after the row-1 fix: allowed_files + threat row for tests/unit/test_generate_agent_configs.py, the out_of_scope row removed (its constraint kept in the note), task-consistency-check OK, sha d9b396b076fe4eed95d13ca02e05b6b1272ddfc9551b0df034467fccc0840bd4 (undispatched; re-hashed at dispatch). The binding file still carries an appended pins draft after its own text (a second `format: 2` block from the joint authoring); it is dropped when the binding text is authored for dispatch (sweep S6).
- 2026-10-21T09:14Z: security review of 28dde0f5 `…-security-28dde0f.md.last.md` Verdict correct (25 threat rows checked, no findings). Counters before the gate (C-126, sqlite): TASKs|2 ACCEPT-amend|0 ACCEPT-revise|0 RESULTs|1 PONG-question|0 (amendment 1 = TASKs 2; S2 not reached). finish-pr.sh runs the sweep, the record block, the gate and the merge bound to 28dde0f5.
- 2026-10-21T09:47Z: owner declaration for the records boundary: the residual rows of this lineage named above are owned by dotfiles-T133-trusted-entrypoint-descendants-followup-a01 (owner stub under .orchestration/tasks/).

# Acceptance: dotfiles-T133-regime-ci-followup-a02

Dispatch text of the owner stub (2026-10-19) authored by author-loop on 2026-10-21T22:54Z from `brief-regime-ci-followup-a02.md` (D-024-67: fix the regime verifier's three gaps and set UV_CACHE_DIR for its step; essential remedy for the regime refusals of 2026-10-21). Security: true.

- Round 1 `…-text-security-a232baf.md`: Verdict incorrect, six findings. Round 2 `…-text-security-a18a67d.md`: Verdict incorrect, six findings; the loop stopped (exit 7). Round 2: P1 the bindings cover uv/Python/Git but not gh, whose responses authenticate the verifier's reads (the executable-provenance wall, as a07); P1 merge-driver configuration uncontrolled in the patch-id recomputation (fixable: isolated git config and a hostile-driver regression); P1 empty Checks (pasted before review, as every text); P2 the workflow row's closed claim too broad; P2 cache-refusal ownership circular between a07 and this task (fix: this task takes the checker file into allowed_files and owns the restoration); P2 the followup-a03 owner stub missing (created 2026-10-21T22:54Z).

text-security:a232baf:1	executable-provenance
text-security:a18a67d:1	executable-provenance
text-security:a18a67d:2	merge-driver-isolation
text-security:a18a67d:3	checks-omission
text-security:a18a67d:4	closed-claim-scope
text-security:a18a67d:5	ownership-circular
text-security:a18a67d:6	owner-stub-missing

Decision pending (2026-10-21T22:54Z): the gh-provenance P1 is the same wall that holds a07 (D-024-65); two lineages now wait on the gh binding, so the orchestrator escalates whether to pull `dotfiles-T133-gh-binding-a01` (and the trusted-entrypoint binding) ahead of slices 2-5.
- 2026-10-21T22:58Z: D-024-69: the operator ruled for the essential remedy; gh-binding-a01 goes first; this text's C-80 resumes after that binding merges (its fixable findings 2-6 are folded into the amendment then).

- [P1] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:84` — The explicit bindings cover uv/Python/Git but omit `gh`, whose responses authenticate Item 5; `gh-binding-a01.md:20–24` says canonical reads remain non-authoritative until that binding lands, so require a bound authentication transport and an actual-consumer substitution probe.

- [P1] medium `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:66` — Merge recomputation leaves merge-driver configuration uncontrolled: local `merge.default`/`merge.*.driver` can select executable commands and manufacture a successful merge result despite the referenced hook/diff protections; require isolated merge configuration and a hostile-driver regression. [Git documentation](https://git-scm.com/docs/gitattributes#_defining_a_custom_merge_driver)

- [P1] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:98` — The required pre-review measurements are absent: the file ends at an empty `Checks` heading, leaving launch bindings, descendant results and authenticated gate-source identity unestablished; this version cannot satisfy its own approval/dispatch conditions.

- [P2] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:18` — The whole workflow is marked `closed` by a test specified only to inspect `UV_CACHE_DIR`; that assertion cannot establish protected-base execution, head-as-data handling or credential protections, so narrow the claim or name coverage for the workflow’s actual execution boundary.

- [P2] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:74` — Cache-refusal ownership is circular: this task excludes the checker and assigns refusal to a07, while `a07-checker.md:56,77,90` explicitly preserves the fallback and assigns restoration here; neither task authorizes the promised control.

- [P2] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:38` — The required `dotfiles-T133-regime-ci-followup-a03.md` owner stub does not exist, so the residual ownership asserted throughout the table has not met its stated pre-anchor prerequisite.

📝 まとめ: Read-only design review completed; six findings are input for the orchestrator’s decision.

Not checked: implementation, live Linux execution or CI; runtime enforcement remains unverified.
Verdict: incorrect- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:117` The replacement authority path invokes bare `git` without binding its executable; PATH/mise substitution can forge clone, prerequisite and measurement results, reproducing the rejected `gh` provenance defect.
- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:135` The clone prefix does not remove inherited `GIT_*`, and subsequent commands omit even that prefix: a read-only probe confirmed `GIT_CONFIG_COUNT` can rewrite the fixed GitHub URL despite both stated options; `GIT_DIR` can likewise redirect subsequent repository reads.
- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:35` Calling checker output “non-authoritative” does not mitigate executing substituted `gh` with forwarded credentials; no binding prerequisite or credential suppression prevents disclosure, and Linux execution outside the sandbox cannot rely on sandbox containment.
- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:117` A fresh “private” clone establishes initial separation from shared objects, but the specified `<dir>` has no demonstrated worker-write exclusion or consumption-time identity binding; same-UID replacement can still alter objects or refs subsequently treated as authoritative.
- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:137` Counting two “5.14” occurrences does not perform the inherited exact design-publication assertion; Checks also omits that assertion’s command and exit, so its claimed prerequisite success does not satisfy line 119.

📝 まとめ: Reviewed the threat rows and cited acceptance/review context; five findings remain for orchestrator disposition. No files changed.

Not checked: future implementation or live Linux/race behavior; executable, credential and object-store binding remain unresolved.
Verdict: incorrect
 succeeded in 315ms:
7da0cdfab9de9fbea673b82379acd4e317115065
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
tests/unit/test_mise_config.py
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
tests/unit/test_trusted_exec_contract.py
tests/unit/test_ua_symbol_coverage.py
tests/unit/test_update_agent_assets.py
tests/unit/test_update_agent_assets_ua_core.py
tests/unit/test_upgrade_tools.py
tests/unit/test_usage_review.py
tests/unit/test_validate_agent_assets.py
tests/unit/test_workflow_orchestration_skip.py
tests/unit/test_workflow_security.py
tests/unit/trusted_exec_contract.py
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
python3: error: couldn't create cache file '/tmp/xcrun_db-qAKMgZco' (errno=Operation not permitted)
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
python3: error: couldn't create cache file '/tmp/xcrun_db-suNCOlwR' (errno=Operation not permitted)
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Collector that gathers every piece of GitHub feedback on a PR head (issue comments, reviews, inline comments with thread state, non-passing checks, annotations, commit statuses) into one JSON document with empty dispositions for the PR integration gate.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Exits with guidance when `gh auth status` reports the GitHub CLI is not authenticated.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Builds one normalized feedback item (source, actor, bot flag, level, body, url, path/line, thread state) with an empty disposition.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Queries review threads over GraphQL and maps each review comment id to its resolved and outdated state.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Fetches all PR feedback sources for the head commit via REST/GraphQL and assembles the item list with repo, PR, head and base metadata.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'CLI entry that resolves the repo, requires gh auth, collects feedback, and writes JSON to stdout or a file.'}

**Reducing tool chunk size**
codex
今回の文面は、従来の指摘に対して親プロセスの事前検証と認証利用の停止条件を追加しています。次に、その条件が既存の子プロセスの起動方法や同一ユーザーによる書き換えに対して有効かを確認します。
exec
/bin/zsh -lc "sed -n '95,150p' .orchestration/plans/024-design-quality.md; cat .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-3bf2a79.md.last.md; cat .orchestration/tasks/dotfiles-T133-gh-binding-followup-a01.md; rg -n '"'^D-024-69'"\\b' .orchestration/decisions.tsv" in /Users/a0004262/Workspace/dotfiles
 succeeded in 41ms:
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
- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:39` — Deferring parent/interpreter binding supplies no compensating control: retained mise/PATH-selected processes execute before the proposed `gh` checks and can replace their decisions or capture credentials; cleaning only the child environment cannot establish the claimed consumer binding, especially outside Linux’s sandbox.

- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:76` — The environment allowlist omits a control and test for `gh`’s configuration-file inputs: default home configuration can select `http_unix_socket`, changing the actual transport despite a pinned executable and explicit hostname; require a protected, controlled configuration source. [GitHub CLI configuration](https://cli.github.com/manual/gh_config), [configuration discovery](https://cli.github.com/manual/gh_help_environment).

- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:38` — The named child-environment test cannot close in-process effects: the reused chain/regime fixtures inherit `GIT_*` into Git writes, allowing `GIT_DIR`/`GIT_WORK_TREE` to redirect operations outside their temporary repositories and `GIT_CONFIG_*` to inject configuration. [Git environment](https://git-scm.com/docs/git), [configuration overrides](https://git-scm.com/docs/git-config).

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:80` — Allowing an identity refusal to satisfy each decoy test does not prove successful consumer binding; require a positive authenticated-operation fixture per route, alongside refusal cases, to prevent an always-refusing implementation from satisfying the binding evidence.

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:105` — The stated baseline is inaccurate: `chain-finish.sh` is absent from this checkout and local `origin/main`, and neither Python checker contains the claimed `gh` lookup; with creation forbidden and `after: []`, the six-route implementation requires the reviewed amendment this line prescribes.

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:110` — `Checks` is empty despite requiring populated measurements before C-80; these bytes provide no observed canonical-source, installation or interpreter-binding evidence, and approval cannot cover a later paste.

📝 まとめ: Reviewed all 37 threat rows and cited acceptance/review history; findings remain input for the orchestrator. No files changed.

Not checked: future implementation, CI or live Linux/race behavior; same-user replacement and credential-sharing risks remain.
Verdict: incorrect---
format: 2
task_id: dotfiles-T133-gh-binding-followup-a01
kind: code
security: true
dispatch_status: draft-owner-stub
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/validate-agent-assets.py
  - .orchestration/dotfiles-T133-gh-binding-followup-a01/**
after: [dotfiles-T133-gh-binding-a01]
---

# AGMSG-TASK dotfiles-T133-gh-binding-followup-a01 — owner of the gh-binding-a01 residual rows (owner stub)

Owner stub written 2026-10-21T22:59Z by the orchestrator seat (C-51); never dispatched as a stub.

## Checks (pasted by the orchestrator before each send)

```text
(empty until the dispatch text is authored)
```
117:D-024-69	2026-10-21T22:58Z	gh binding pulled forward (operator 07:5x JST: use the essential remedy, not an expedient): dotfiles-T133-gh-binding-a01 (pin github-cli in home/dot_mise/config.toml, declare the absolute gh path beside uv/Python/Node in agent-config.yaml, make the orchestrator scripts' resolver and the checker's executable() use the declared path with --hostname github.com, one refusal test per route) is authored now (author-loop, C-80), anchored and dispatched to the free Codex seat a012 ahead of slices 2-5 and of trusted-entrypoint-binding-a01; a07 (D-024-65) and regime-ci-followup-a02 resume their C-80 after it merges; options B (keep the order) and C (a CI-side waiver) were declined by the operator's instruction	seven C-80 rounds across a07 and regime-ci-followup-a02 refused the same executable-provenance class; only a host binding of gh closes it; the operator ruled for the essential means	text-security verdicts 922292d/0edbd8c/fd8c003/c6cebe4/a3125e1 (a07) and a232baf/a18a67d (regime-ci-followup-a02); gh is mise-managed at github-cli-cli/latest, unpinned	brief next; dispatch to a012 after the anchor review

**Checking token and time budget**
exec
/bin/zsh -lc "rg -n '"'^[- ]*'"\\[P|"'^Verdict:|''^##|gh-binding|gh |a3125e1|a18a67d'"' .orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-{922292d,0edbd8c,fd8c003,c6cebe4}.md.last.md .orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md; rg --files .orchestration/acceptance | rg '(a07-checker|gh-binding)'" in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba scripts/orchestrator/local-review.sh | head -240; rg -n 'gh|gh_env|subprocess|GIT_|PATH|repo' scripts/pr-feedback.py scripts/orchestrator/gate-collect.py tests/unit/trusted_exec_contract.py" in /Users/a0004262/Workspace/dotfiles
exec
/bin/zsh -lc 'nl -ba scripts/orchestrator/chain-integrate.sh | head -220; nl -ba scripts/orchestrator/orch-gate.sh | head -190' in /Users/a0004262/Workspace/dotfiles
 succeeded in 169ms:
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
     1	#!/usr/bin/env bash
     2	# @file orch-gate.sh
     3	# @brief Run the integration gate on a PR checkout's head from the review worktree, with the task's evidence copied in.
     4	# @description
     5	#   Plan 007 T718, the parameterised form of the orchestrator's gate wrapper. The head is always `git -C
     6	#   <pr-worktree> rev-parse HEAD`. From the checkout this script lives in, it requires the task's sweep JSON (whose
     7	#   `pr` must be <pr>), the audit of this head and its `.last.md`, the review receipt, the crit JSON and the
     8	#   acceptance record, all under `.orchestration/`, before it checks the clean review worktree
     9	#   `.claude/worktrees/orchestrator-review` out at the head; a head that tracks a symlink under `.orchestration`
    10	#   is refused, so no copy follows a link out of the worktree. It copies them in and runs, with the review worktree
    11	#   as its working tree, the gate `make require-crit-review` runs, but this checkout's copy: the head's Makefile
    12	#   and gate are PR-controlled (PR #350 thread 4265190252), so `scripts/require-crit-review.py` and the validator
    13	#   it loads must equal origin/main's here. The interpreter is `uv python find` in this checkout, resolved before
    14	#   the review worktree is entered and run directly, so no uv reads the head's `.python-version` or `uv.toml`
    15	#   (uv runs an executable a `.python-version` names; the audit of f48593d6). The gate runs under `env -i` with
    16	#   HOME as this shell has it, a PATH of one private directory of links to `gh` and `git` as this checkout resolves
    17	#   them (`mise which` under `env -i`, else `command -v`; a path under a `shims` directory or none is refused), its
    18	#   inputs AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE, PR_FEEDBACK_EVIDENCE, REVIEW_EVIDENCE and AGENT_REVIEWED=1, and
    19	#   PYTHONSAFEPATH=1, as `-I -P <gate> --base origin/main`: nothing else of this shell or of the head reaches the
    20	#   gate or the collector and gh it starts (the audits of a06c874e and 6847aa9f). A trap set before the private
    21	#   directory is made removes it whatever fails or the gate says, and once the head's checkout has started restores
    22	#   the review worktree to origin/main; a refusal before that leaves the review worktree as it was (the audit of
    23	#   a235637).
    24	# @arg $1 string Task id.
    25	# @arg $2 path The PR's checkout (its HEAD is the gated head).
    26	# @arg $3 int PR number.
    27	# @exitcode 0 The gate passed.
    28	# @exitcode 2 Usage error, or a refused precondition.
    29	# @exitcode * Otherwise the gate's own status.
    30	# @example
    31	#   scripts/orchestrator/orch-gate.sh dotfiles-T128-orchestrator-tools-a05 .claude/worktrees/worker-c 350
    32	set -euo pipefail
    33	
    34	usage() {
    35	    echo "usage: orch-gate.sh <task> <pr-worktree> <pr>" >&2
    36	    exit 2
    37	}
    38	refuse() {
    39	    echo "orch-gate: $1; refused" >&2
    40	    exit 2
    41	}
    42	(($# == 3)) || usage
    43	task=$1 pr=$3
    44	[[ ${task} =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ && ${pr} =~ ^[0-9]+$ ]] || usage
    45	head="$(git -C "$2" rev-parse HEAD)"
    46	root="$(git -C "$(dirname -- "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
    47	review="${root}/.claude/worktrees/orchestrator-review"
    48	v=.orchestration/validation
    49	sweep="${v}/${task}-pr-feedback.json" audit="${v}/${task}-audit-${head:0:7}.md"
    50	record=".orchestration/acceptance/${task}.md" receipt="${v}/${task}-review-receipt.md"
    51	evidence=("${sweep}" "${audit}" "${audit}.last.md" "${receipt}" "${v}/${task}-crit.json" "${record}")
    52	cd -- "${root}"
    53	git diff --quiet origin/main -- scripts/require-crit-review.py scripts/validate-agent-assets.py ||
    54	    refuse "the gate here differs from origin/main's"
    55	for f in "${evidence[@]}"; do
    56	    [[ -f ${f} ]] || refuse "${f} is missing"
    57	done
    58	[[ $(jq -r .pr "${sweep}") == "${pr}" ]] || refuse "${sweep} is not the sweep of PR ${pr}"
    59	[[ -z $(git ls-tree -r "${head}" -- .orchestration | awk '$1 == "120000"') ]] ||
    60	    refuse "${head:0:7} tracks a symlink under .orchestration (PR #350 thread 4265190259)"
    61	python="$(uv python find)" || refuse "uv found no interpreter in ${root}"
    62	[[ -z $(git -C "${review}" status --porcelain --untracked-files=all) ]] || refuse "the review worktree is not clean"
    63	trap '[[ -z ${bin:-} ]] || rm -rf -- "${bin}"
    64	[[ -z ${moved:-} ]] || { git -C "${review}" clean -fdq -- .orchestration; git -C "${review}" checkout -qf --detach origin/main; }' EXIT
    65	bin="$(mktemp -d "${TMPDIR:-/tmp}/orch-gate.XXXXXX")"
    66	# The gate's PATH is these links alone: through the caller's PATH, gh resolved to a mise shim, which picks the binary
    67	# from the review worktree's mise.toml (the audit of 6847aa9f). gh and git are what the gate and its collector run.
    68	# mise resolves under env -i, so no MISE_CONFIG_FILE or MISE_TRUSTED_CONFIG_PATHS of this shell picks the binary
    69	# (PR #355 thread 4267889542).
    70	for name in gh git; do
    71	    found="$(env -i PATH="${PATH}" HOME="${HOME}" mise which "${name}" 2> /dev/null || command -v "${name}")" || found=
    72	    [[ ${found} == /* && ${found} != */shims/* ]] || refuse "no binary for ${name} outside a shims directory ('${found}')"
    73	    ln -s -- "${found}" "${bin}/${name}"
    74	done
    75	moved=1
    76	git -C "${review}" checkout -q --detach "${head}"
    77	for f in "${evidence[@]}"; do
    78	    mkdir -p "${review}/$(dirname -- "${f}")"
    79	    cp -- "${f}" "${review}/${f}"
    80	done
    81	rc=0
    82	(
    83	    # errexit is off left of ||, so a failed cd exits here instead of gating another tree.
    84	    cd -- "${review}" || exit 2
    85	    # Built, not filtered: CRIT_REVIEW=off, CRIT_REVIEWED=1 (thread 4265190267) or a PYTHONPATH that loads the head's
    86	    # sitecustomize.py into the collector (the audit of a06c874e) cannot come along.
    87	    env -i PATH="${bin}" HOME="${HOME}" AUDIT_EVIDENCE="${audit}" ACCEPTANCE_EVIDENCE="${record}" \
    88	        PR_FEEDBACK_EVIDENCE="${sweep}" REVIEW_EVIDENCE="${receipt}" AGENT_REVIEWED=1 PYTHONSAFEPATH=1 \
    89	        "${python}" -I -P "${root}/scripts/require-crit-review.py" --base origin/main
    90	) || rc=$?
    91	echo "orch-gate: ${task} at ${head:0:7} for PR ${pr}: gate rc=${rc}"
    92	exit "${rc}"

 exited 2 in 226ms:
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
rg: scripts/orchestrator/gate-collect.py: No such file or directory (os error 2)
scripts/pr-feedback.py:4:Usage: pr-feedback.py <pr-number> [--repo owner/name] [--json <out>]
scripts/pr-feedback.py:11:checks the filled file through PR_FEEDBACK_EVIDENCE. Passing check runs are
scripts/pr-feedback.py:21:import subprocess
scripts/pr-feedback.py:31:  repository(owner: $owner, name: $name) {
scripts/pr-feedback.py:66:def gh_env() -> dict[str, str]:
scripts/pr-feedback.py:67:    """Environment for gh that never colours output, even under CLICOLOR_FORCE panes."""
scripts/pr-feedback.py:73:def gh(args: list[str]) -> str:
scripts/pr-feedback.py:74:    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False, env=gh_env())
scripts/pr-feedback.py:76:        sys.exit(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
scripts/pr-feedback.py:80:def gh_fetch(path: str, paginate: bool = False) -> Any:
scripts/pr-feedback.py:83:        return json.loads(gh(["api", "--paginate", "--slurp", path]))
scripts/pr-feedback.py:84:    return json.loads(gh(["api", path]))
scripts/pr-feedback.py:87:def gh_graphql(query: str, variables: dict[str, Any]) -> Any:
scripts/pr-feedback.py:92:    return json.loads(gh(args))
scripts/pr-feedback.py:96:    result = subprocess.run(
scripts/pr-feedback.py:97:        ["gh", "auth", "status"],
scripts/pr-feedback.py:101:        env=gh_env(),
scripts/pr-feedback.py:104:        print("pr-feedback: gh is not authenticated; run `gh auth login`", file=sys.stderr)
scripts/pr-feedback.py:109:    """Merge `gh api --paginate --slurp` pages into one list."""
scripts/pr-feedback.py:147:def thread_states(repo: str, number: int, graphql: GraphQL) -> dict[int, dict[str, bool]]:
scripts/pr-feedback.py:149:    owner, name = repo.split("/", 1)
scripts/pr-feedback.py:157:        threads = data["data"]["repository"]["pullRequest"]["reviewThreads"]
scripts/pr-feedback.py:176:def collect(repo: str, number: int, fetch: Fetch = gh_fetch, graphql: GraphQL = gh_graphql) -> dict[str, Any]:
scripts/pr-feedback.py:177:    pull = fetch(f"repos/{repo}/pulls/{number}", False)
scripts/pr-feedback.py:181:    for comment in flatten(fetch(f"repos/{repo}/issues/{number}/comments", True)):
scripts/pr-feedback.py:191:    for review in flatten(fetch(f"repos/{repo}/pulls/{number}/reviews", True)):
scripts/pr-feedback.py:202:    states = thread_states(repo, number, graphql)
scripts/pr-feedback.py:203:    for comment in flatten(fetch(f"repos/{repo}/pulls/{number}/comments", True)):
scripts/pr-feedback.py:219:    for run in flatten(fetch(f"repos/{repo}/commits/{sha}/check-runs", True), "check_runs"):
scripts/pr-feedback.py:236:            for annotation in flatten(fetch(f"repos/{repo}/check-runs/{run['id']}/annotations", True)):
scripts/pr-feedback.py:253:    for status in flatten(fetch(f"repos/{repo}/commits/{sha}/statuses", True)):
scripts/pr-feedback.py:268:        "repo": repo,
scripts/pr-feedback.py:282:    parser.add_argument("--repo", help="owner/name; defaults to the current repository")
scripts/pr-feedback.py:287:    repo = args.repo or gh(["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]).strip()
scripts/pr-feedback.py:288:    document = collect(repo, args.pr)
scripts/pr-feedback.py:297:        f"pr-feedback: {repo}#{args.pr} head {document['head_sha'][:7]}: {len(document['items'])} items ({summary})",
tests/unit/trusted_exec_contract.py:10:import subprocess
tests/unit/trusted_exec_contract.py:15:SHIMS = ("uv", "python3", "gh", "git", "bash")
tests/unit/trusted_exec_contract.py:16:ALLOWED = ("PATH", "HOME", "LANG")
tests/unit/trusted_exec_contract.py:17:SAFE_PATH = "/usr/bin:/bin"
tests/unit/trusted_exec_contract.py:20:QUIET = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
tests/unit/trusted_exec_contract.py:21:HOSTILE_GIT_ENV = ("GIT_DIR", "GIT_WORK_TREE", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CEILING_DIRECTORIES")
tests/unit/trusted_exec_contract.py:22:HOSTILE_GIT_ENV += ("GIT_ALTERNATE_OBJECT_DIRECTORIES",)
tests/unit/trusted_exec_contract.py:31:    """Failing shims of SHIMS first on PATH, each recording its name and argv as JSON through an absolute python."""
tests/unit/trusted_exec_contract.py:42:        self.env["PATH"] = os.pathsep.join(filter(None, (str(self.bin), self.env.get("PATH", ""))))
tests/unit/trusted_exec_contract.py:53:    """A legitimate and an attacker repository; attack(kind) yields the environment to offer a consumer."""
tests/unit/trusted_exec_contract.py:57:        self.hook_marker, self._env = base / "attacker-hook-ran", {"PATH": SAFE_PATH, "HOME": str(base)}
tests/unit/trusted_exec_contract.py:58:        for repo, text in ((self.legit, LEGIT), (self.attacker, ATTACKER)):
tests/unit/trusted_exec_contract.py:59:            repo.mkdir()
tests/unit/trusted_exec_contract.py:60:            self._git(repo, "init", "-q")
tests/unit/trusted_exec_contract.py:61:            (repo / "probe.txt").write_text(text)
tests/unit/trusted_exec_contract.py:62:            self._git(repo, "add", "probe.txt")  # an index, so status consults core.fsmonitor
tests/unit/trusted_exec_contract.py:69:    def _git(self, repo, *args):
tests/unit/trusted_exec_contract.py:70:        subprocess.run(["/usr/bin/git", "-C", str(repo), *args], env=self._env | QUIET, check=True, capture_output=True)
tests/unit/trusted_exec_contract.py:74:        """Kind environment exports hostile GIT_*; the local-* kinds plant one key in the fixture's own config."""
tests/unit/trusted_exec_contract.py:79:            yield self._env | {name: str(value) for name, value in zip(HOSTILE_GIT_ENV, values, strict=True)}
tests/unit/trusted_exec_contract.py:183:    """The observed names are exactly PATH, HOME, LANG and the consumer's declared names, with PATH=/usr/bin:/bin."""
tests/unit/trusted_exec_contract.py:184:    want, got, path = set(ALLOWED) | set(declared), set(observed), observed.get("PATH")
tests/unit/trusted_exec_contract.py:187:    found += [f"PATH is {path!r}, not {SAFE_PATH!r}"] if path != SAFE_PATH else []
tests/unit/trusted_exec_contract.py:192:def repository_root():
tests/unit/trusted_exec_contract.py:193:    """The checkout this module lives in, from its own path; no Git command or GIT_* variable is consulted."""
tests/unit/trusted_exec_contract.py:198:    return subprocess.run(argv, env={}, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL).stdout
tests/unit/trusted_exec_contract.py:202:    """The real UID's home from its passwd entry (pwd.getpwuid), never HOME or PATH. dscl (macOS) or getent (Linux)
tests/unit/trusted_exec_contract.py:209:    except (OSError, subprocess.CalledProcessError):
tests/unit/trusted_exec_contract.py:222:    """Run a regular file inside the repository root under env -i and bash -p, each argument one argument."""
tests/unit/trusted_exec_contract.py:225:    root, real = repository_root().resolve(), Path(script).resolve()
tests/unit/trusted_exec_contract.py:230:    argv = ["/usr/bin/env", "-i", f"PATH={SAFE_PATH}", f"HOME={passwd_home()}", "LANG=C.UTF-8"]
tests/unit/trusted_exec_contract.py:232:    return subprocess.run(argv, env={}, capture_output=True, text=True, check=False, stdin=subprocess.DEVNULL)

 succeeded in 246ms:
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md.last.md:1:- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:36` Withholding authenticity claims does not mitigate executable substitution: retained PATH selection can execute an attacker-controlled `gh`, forward tokens, and accept forged canonical design/receipt responses; authoritative use needs a trusted-executable prerequisite or must remain non-authoritative until that prerequisite lands.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md.last.md:2:- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:120` The acceptance measurement uses mutable local `origin/main` and shared Git objects; a same-user writer can change the merge-base and measured diff despite sanitized `GIT_*`, so the budget decision needs an authenticated canonical base and verified changeset.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md.last.md:3:- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:135` `Checks` remains empty although lines 122–123 require observed prerequisites before either review; this digest lacks the prerequisite evidence, and approval cannot carry over to subsequently populated dispatch bytes.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-0edbd8c.md.last.md:8:Verdict: incorrect
.orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md:1:- [P1] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:99` — Recording `mise which uv` does not bind subsequent bare `uv` execution, its Python, or checker descendants; this host resolves uv through mise shims, while `after: []` permits dispatch before the binding prerequisites land.
.orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md:3:- [P1] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:24` — Temporary repositories do not isolate inherited `GIT_DIR`, `GIT_WORK_TREE`, or `GIT_CONFIG_*`: the retained test harness forwards them into Git, including commits and resets, so commands can target another writable repository despite their temporary cwd; sandboxing does not close this redirection.
.orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md:5:- [P1] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:66` — Equal `patch-id --verbatim` values do not establish unchanged behavior: moving an identical hunk between repeated blocks preserves the ID, including when introduced through a merge resolution; the named test needs this negative case and a check that binds the resulting tree to the permitted merge. [Git documentation](https://git-scm.com/docs/git-patch-id)
.orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md:7:- [P1] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:85` — A matching acceptance JSON head plus “gate passed” evidence can be fabricated together in the records PR; recorded/unrecorded fixtures cannot close this authentication gap without an independently authenticated gate result bound to the repository, exact head, and trusted preceding boundary.
.orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md:9:- [P1] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:42` — Fixture byte equality provides no compensating control against replacement between validation and consumption: the bootstrap still names checkout files, while no required test binds the executed checker and consumed evidence to the validated snapshot under symlink, case-alias, or same-user replacement.
.orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md:11:- [P2] high `.orchestration/tasks/dotfiles-T133-regime-ci-followup-a02.md:60` — Blob equality omits Git entry modes: identical bytes can change from a regular evidence file into a symlink or executable while satisfying the stated comparison; the closed retained-directory row needs type/mode checks and corresponding negative fixtures.
.orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md:15:Not checked: implementation, live Linux gh execution, or CI; runtime enforcement remains unverified.
.orchestration/validation/dotfiles-T133-regime-ci-followup-a02-text-security-a232baf.md.last.md:16:Verdict: incorrect
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md.last.md:1:- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:117` “Non-authoritative” `gh` output still selects the cap-measurement base and establishes dispatch prerequisites: a substituted executable can report the candidate head as canonical main, satisfying ancestry and producing a zero diff even in an authentic private clone; the residual also leaves forwarded credentials exposed, without requiring the binding prerequisite before use.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md.last.md:2:- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:135` The prerequisite command uses `--repo mryfmo/dotfiles` without fixing its host, so inherited `GH_HOST` can select another server even with genuine `gh`; use `--repo github.com/mryfmo/dotfiles` or a fixed-host API request. [GitHub CLI environment documentation](https://cli.github.com/manual/gh_help_environment).
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md.last.md:3:- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:137` Checks asserts successful design publication but omits the exact contents-API/assertion commands and individual stage exits required by line 119; line 138 supplies only a pre-paste pre-send exit, so these reviewed bytes do not contain the prerequisite evidence required before review and dispatch.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-c6cebe4.md.last.md:8:Verdict: incorrect
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md.last.md:1:- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:36` Moving authority to the orchestrator’s bare `gh` does not authenticate its executable: PATH/mise substitution can forge acceptance reads, while “non-authoritative” checker execution still exposes forwarded credentials; sandbox labels do not close either risk, and the named binding-owner text specifies uv/Python/Node/permgate binding, not `gh`.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md.last.md:2:- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:117` The authoritative API command omits `--hostname github.com`; inherited `GH_HOST` can redirect the fixed repository endpoint even with a genuine executable, so the stated command does not establish the canonical-main source required by design item 8.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md.last.md:3:- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:117` Authenticating the main SHA does not authenticate the shared local objects consumed by `git merge-base` and `git diff --numstat`; same-user object substitution can change ancestry and measured counts even after inherited `GIT_*` sanitization, so acceptance needs authenticated changeset bytes or a worker-inaccessible clone.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-fd8c003.md.last.md:8:Verdict: incorrect
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md.last.md:1:- [P1] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:36` The canonical-main closure assumes a genuine `gh`: retained executable selection accepts a PATH-selected regular executable outside the checkout/shim exclusions, while the named tests deliberately supply fake API responses; fixed host/repository arguments cannot authenticate those responses or protect forwarded tokens without trusted executable provenance.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md.last.md:3:- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:103` Restoring mandatory `UV_CACHE_DIR` revives the documented failure for callers that omit it, including regime-ci invocations; caller/workflow changes are excluded and no repair prerequisite is named, so supplied-cache fixtures cannot establish deployable compatibility.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md.last.md:5:- [P2] High confidence `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a07-checker.md:134` `Checks` is empty despite lines 120–121 requiring prerequisite API observations and completely populated bytes before the anchor review; approving this digest cannot approve the subsequently populated dispatch text.
.orchestration/validation/dotfiles-T133-task-generator-plan-check-a07-checker-text-security-922292d.md.last.md:10:Verdict: incorrect
.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a07-checker.md

**Handling tool output truncation**
exec
/bin/zsh -lc "cat scripts/orchestrator/orch-gate.sh; sed -n '30,110p' scripts/orchestrator/local-review.sh; sed -n '60,107p' scripts/pr-feedback.py; sed -n '280,295p' scripts/pr-feedback.py" in /Users/a0004262/Workspace/dotfiles
 succeeded in 39ms:
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
# The gate's PATH is these links alone: through the caller's PATH, gh resolved to a mise shim, which picks the binary
# from the review worktree's mise.toml (the audit of 6847aa9f). gh and git are what the gate and its collector run.
# mise resolves under env -i, so no MISE_CONFIG_FILE or MISE_TRUSTED_CONFIG_PATHS of this shell picks the binary
# (PR #355 thread 4267889542).
for name in gh git; do
    found="$(env -i PATH="${PATH}" HOME="${HOME}" mise which "${name}" 2> /dev/null || command -v "${name}")" || found=
    [[ ${found} == /* && ${found} != */shims/* ]] || refuse "no binary for ${name} outside a shims directory ('${found}')"
    ln -s -- "${found}" "${bin}/${name}"
done
moved=1
git -C "${review}" checkout -q --detach "${head}"
for f in "${evidence[@]}"; do
    mkdir -p "${review}/$(dirname -- "${f}")"
    cp -- "${f}" "${review}/${f}"
done
rc=0
(
    # errexit is off left of ||, so a failed cd exits here instead of gating another tree.
    cd -- "${review}" || exit 2
    # Built, not filtered: CRIT_REVIEW=off, CRIT_REVIEWED=1 (thread 4265190267) or a PYTHONPATH that loads the head's
    # sitecustomize.py into the collector (the audit of a06c874e) cannot come along.
    env -i PATH="${bin}" HOME="${HOME}" AUDIT_EVIDENCE="${audit}" ACCEPTANCE_EVIDENCE="${record}" \
        PR_FEEDBACK_EVIDENCE="${sweep}" REVIEW_EVIDENCE="${receipt}" AGENT_REVIEWED=1 PYTHONSAFEPATH=1 \
        "${python}" -I -P "${root}/scripts/require-crit-review.py" --base origin/main
) || rc=$?
echo "orch-gate: ${task} at ${head:0:7} for PR ${pr}: gate rc=${rc}"
exit "${rc}"
set -euo pipefail
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
git -C "$W" checkout -q --detach "$head"
base=$(git -C "$W" merge-base main HEAD)
t0=$(date -u +%FT%TZ)
"""

Fetch = Callable[[str, bool], Any]
GraphQL = Callable[[str, dict[str, Any]], Any]


def gh_env() -> dict[str, str]:
    """Environment for gh that never colours output, even under CLICOLOR_FORCE panes."""
    env = {key: value for key, value in os.environ.items() if key not in {"CLICOLOR_FORCE", "GH_FORCE_TTY"}}
    env["NO_COLOR"] = "1"
    return env


def gh(args: list[str]) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False, env=gh_env())
    if result.returncode != 0:
        sys.exit(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return result.stdout


def gh_fetch(path: str, paginate: bool = False) -> Any:
    """Return the JSON for a REST path; paginated responses become a list of pages."""
    if paginate:
        return json.loads(gh(["api", "--paginate", "--slurp", path]))
    return json.loads(gh(["api", path]))


def gh_graphql(query: str, variables: dict[str, Any]) -> Any:
    args = ["api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is not None:
            args.extend(["-F" if type(value) is int else "-f", f"{key}={value}"])
    return json.loads(gh(args))


def require_auth() -> None:
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
        check=False,
        env=gh_env(),
    )
    if result.returncode != 0:
        print("pr-feedback: gh is not authenticated; run `gh auth login`", file=sys.stderr)
        raise SystemExit(2)


    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pr", type=int, help="pull request number")
    parser.add_argument("--repo", help="owner/name; defaults to the current repository")
    parser.add_argument("--json", type=Path, help="write the document here instead of stdout")
    args = parser.parse_args(argv)

    require_auth()
    repo = args.repo or gh(["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]).strip()
    document = collect(repo, args.pr)
    text = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    if args.json:
        args.json.write_text(text)
    else:
        sys.stdout.write(text)
    counts = Counter(f"{entry['source']}:{entry['level']}" for entry in document["items"])
    summary = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))

**Analyzing specification constraints**
**Evaluating namespace trust limitations**
exec
/bin/zsh -lc "sed -n '110,112p' .orchestration/plans/024-design-quality.md; cat .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a07-checker.md; rg -n 'gh|pr-feedback|subprocess|PATH|env=' scripts/require-crit-review.py; sed -n '1,160p' tests/unit/test_chain_glue.py" in /Users/a0004262/Workspace/dotfiles
 succeeded in 46ms:
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
# Acceptance: dotfiles-T133-task-generator-plan-check-a07-checker

Reset of `dotfiles-T133-task-generator-plan-check-a06-checker` (PR #440, round-2 head c439b63c; D-024-57, D-024-58): the audit of c439b63c found an implementation P1 (C15 accepts arbitrary invariants when design_review.design is omitted) and three implementation P2; the mechanism-PR two-round limit forbade a third round. a07 continues PR #440's branch `tools/task-generator-plan-check-a05-checker` from c439b63c and fixes the P1, the audit P2 rows, the local-review decode abort and the two round-2 security symlink P2, with one red-then-green fixture each. The UV_CACHE_DIR refusal of design 5.14 item 9 is not in a07: the a06 R1 fallback stays as a recorded design exception owned by `dotfiles-T133-regime-ci-followup-a02` (restored together with the caller change).

## Authoring (author-loop from `brief-a07-checker.md`, then orchestrator edits)

- Round 1 `…-text-security-922292d.md` and round 2 `…-text-security-0edbd8c.md`: Verdict incorrect; the loop stopped at its two-round limit (exit 7). Recurring P1: the checker's canonical reads trust a PATH-selected gh. Round-2 P2: the measurement base used mutable local origin/main.
- Orchestrator edits (2026-10-21T09:30Z): gh-provenance rows re-owned, fix 7 removed (owner regime-ci-followup-a02), measurement base bound to the canonical main SHA read by the orchestrator's own gh; Checks pasted (observed #435 MERGED 60a6fb2b, canonical main e00de4e0, decoded design digest a027b021…, stage exits).
- Round 3 `…-text-security-fd8c003.md`: Verdict incorrect. P1: moving authority to the orchestrator's bare gh does not authenticate the executable, and the named binding owner binds uv/Python/Node/permgate, not gh. P2: the canonical-main command lacked `--hostname github.com`. P2: shared local git objects are not authenticated for merge-base/numstat.

text-security:922292d:1	executable-provenance
text-security:922292d:2	design-conflict
text-security:0edbd8c:1	executable-provenance
text-security:0edbd8c:2	cap-measurement-base
text-security:fd8c003:1	executable-provenance
text-security:fd8c003:2	canonical-host-binding
text-security:fd8c003:3	measurement-object-trust

re-plan: executable-provenance (rows text-security:922292d:1, text-security:0edbd8c:1, text-security:fd8c003:1 of this text and local:21f52c7:1 of the a06 round-2 head; four rounds in which canonical reads through an unbound gh were taken as authoritative) — specification: no gh read of this regime is authoritative until gh is pinned and bound by absolute path with `--hostname github.com`; the checker's reads are pre-dispatch hygiene, the orchestrator's reads are recorded as non-authoritative evidence, and the record says so; design: the gh binding is owned by `dotfiles-T133-gh-binding-a01` (owner stub written 2026-10-21T09:30Z, after the binding task; pin github-cli in mise, declare the absolute gh path in agent-config.yaml, bind every canonical read), while uv/Python/Node/permgate stay with `dotfiles-T133-trusted-entrypoint-binding-a01`; the cap measurement runs in a fresh private HTTPS bare clone (generalisation owned by `dotfiles-T128-chain-review-scripts-followup-a09`); implementation: the a07 text edit of 2026-10-21T09:30Z (bytes 45b58f323a0eaf62878c2009d6af78351f5c71476386e924082d396574ec4c0d; rows 35-38 and items 2/8 re-owned, `--hostname github.com`, private-clone measurement), no checker code change for this class; verification: C-80 round 4 of these bytes under this line (the first review after it; C-92 allows three), then the anchor review by another context, then dispatch to a Codex seat other than a012.

## Counters (INV-6)

a06 lineage: TASKs=2 (cap amendment resend) revises=1 RESULTs=2 questions=0 blocked-PONGs=6 (snapshot 08:02Z). a07: not dispatched; amendments=0.
- 2026-10-21T09:41Z: Checks re-pasted with the observed values after the pins merge (canonical main 4eafd890454e495fdb1d429734c5835e46c87652, merge-base with c439b63c unchanged, design digest equal, --hostname github.com in the command); bytes c6cebe47312094927a3a607149d8dc8c5d2bcbbfebed3a7d96f63a22da979779; round 4 runs on these bytes.
- 2026-10-21T09:47Z: owner declaration for the records boundary: the residual rows of this lineage named above are owned by dotfiles-T133-gh-binding-a01 (owner stub under .orchestration/tasks/).
- 2026-10-21T21:24Z: C-80 round 4 (`…-text-security-c6cebe4.md`, run by the orchestrator unsandboxed: the classifier approved the call this time): Verdict incorrect. P1: non-authoritative gh output still selected the measurement base and the prerequisites, so a substituted gh could pass the candidate head off as main. P2: `--repo mryfmo/dotfiles` without a fixed host. P2: Checks lacked the exact commands and stage exits of line 119. Edit: the measurement and every prerequisite now come from a fresh private bare clone fetched anonymously over HTTPS with git only (no gh anywhere in the measurement path; #435's merge state is its merge commit's ancestry of refs/heads/main; the design digest is `git show` of that ref); Checks rebuilt with each command and exit; bytes a3125e128a240b1800372977cc3f52bc97cd702e3a5f7f48e46fa1e813b77e65; round 5 is the third and last review under the re-plan line.

text-security:c6cebe4:1	executable-provenance
text-security:c6cebe4:2	canonical-host-binding
text-security:c6cebe4:3	checks-omission
- 2026-10-21T21:28Z: C-80 round 5 (`…-text-security-a3125e1.md`, orchestrator-run): Verdict incorrect, three P1 and two P2. The executable-provenance class moved from gh to bare git (PATH/mise substitution can forge the clone and the measurement), to unsanitised GIT_* (GIT_CONFIG_COUNT rewrites the fixed URL, GIT_DIR redirects reads), and to the checker's forwarded credentials ("non-authoritative" does not stop disclosure); P2: the private clone directory has no worker-write exclusion or consumption-time identity binding; P2: the design-publication assertion is counted, not performed. Five rounds, five incorrect verdicts, one class: no text can close it before a trusted-executable binding exists on the host (design 5.14 items 2-4/9: dotfiles-T133-trusted-entrypoint-binding-a01 and dotfiles-T133-gh-binding-a01), which is the same wall a08 declared at its line 63. STOP (feedback: re-plan, not a patch): the a07 authoring stops here; the decision (hold behind the binding, or an explicit operator waiver of the surviving P1 for dispatch) is escalated with materials.

text-security:a3125e1:1	executable-provenance
text-security:a3125e1:2	environment-sanitisation
text-security:a3125e1:3	executable-provenance
text-security:a3125e1:4	measurement-object-trust
text-security:a3125e1:5	checks-omission
- 2026-10-21T21:30Z: D-024-65 (operator option A): a07 held, undispatched, until the trusted-entrypoint binding is deployed; the C-80 resumes then on these bytes (a3125e1…) or an amended text; #440 open, #411 waits.

12:import subprocess
57:# runs that did not finish, so a work-in-progress run cannot be waved through.
138:def run_git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
139:    return subprocess.run(
144:        stdout=subprocess.PIPE,
145:        stderr=subprocess.PIPE,
197:        relative.parts[:2] != (".orchestration", "validation") or not relative.name.endswith("-pr-feedback.json")
200:        return "evidence must live under .orchestration/validation/ and end with -pr-feedback.json"
253:        and not any(high_risk_reason(path) for path in paths)
257:def high_risk_reason(path: str) -> str | None:
272:        reason = high_risk_reason(path)
412:    """Check the filled pr-feedback.py JSON: every item needs a root-cause disposition."""
416:            return [f"{PR_FEEDBACK_ENV} must point to the filled scripts/pr-feedback.py JSON for PR integration"]
432:        return [f"{PR_FEEDBACK_ENV} must be a pr-feedback.py document with an items list"]
437:            f"{PR_FEEDBACK_ENV} was collected for head {data.get('head_sha')!r}, not the current HEAD {head}; rerun scripts/pr-feedback.py"
521:    failure = f"could not verify PR #{pr} base on GitHub; fetch the base and rerun scripts/pr-feedback.py"
523:        repository = subprocess.run(
524:            ["gh", "repo", "view", "--json", "nameWithOwner"],
526:            env=env,
537:                f"{PR_FEEDBACK_ENV} does not match the local GitHub repository {repo}; rerun scripts/pr-feedback.py"
539:        result = subprocess.run(
540:            ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "headRefOid,baseRefName,baseRefOid"],
542:            env=env,
566:            f"{PR_FEEDBACK_ENV} does not match the GitHub base {github_ref} ({github_base}); rerun scripts/pr-feedback.py"
593:    base SHA's scripts/pr-feedback.py (the PR under review cannot swap it) for the
609:        collector = root / "scripts/pr-feedback.py"
610:        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
612:            collector = Path(temporary) / "pr-feedback.py"
614:        result = subprocess.run(
619:            stdout=subprocess.PIPE,
620:            stderr=subprocess.PIPE,
624:            return [f"could not re-collect PR #{pr} feedback with scripts/pr-feedback.py: {detail[0]}"]
634:            f"{PR_FEEDBACK_ENV} lacks {sum(missing.values())} current feedback item(s) for PR #{pr}, e.g. {sample[0]}:{sample[2]} {sample[1]}; rerun scripts/pr-feedback.py and disposition them"
655:        return f"{AUDIT_ENV} audits task {match.group('task')!r}, not {task!r} named by {PR_FEEDBACK_ENV} (<task>-pr-feedback.json)"
960:    The same match as `grep -rl 'classes:.*<class>'`, without a subprocess; the gate reads its result, never
1021:        print("PR feedback evidence is incomplete; run scripts/pr-feedback.py and disposition every item.")
1033:    # pr_feedback_errors already validated PR_FEEDBACK_EVIDENCE's location and -pr-feedback.json suffix.
1035:    task = Path(feedback).name.removesuffix("-pr-feedback.json") if feedback else None
"""Exercise chain-integrate.sh (plan 022 T7) against a temporary origin, main checkout and review worktree.

git is the real one: a bare origin holds `main` and `refs/pull/7/head`, the main checkout and the review worktree are
clones of it, the review worktree at the canonical `<main>/.claude/worktrees/orchestrator-review`. The repository
scripts the chain calls are stubs in the main checkout's `scripts/`: each appends `argv:`, `cwd:` and `path:` lines
(and the content of a `.tsv` or comments argument) to `<calls>/<name>.log`, prints `<calls>/<name>.out` and exits with
`<calls>/<name>.status` (0 when absent). `gh`, `uv`, `codex` and `mise` (failing, so `command -v` resolves) are stubs
first on PATH; `gh` answers from files the case writes and its `update-branch` merges `main` into the pull ref.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parents[2] / "scripts/orchestrator/chain-integrate.sh"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
TASK, OWNER = "dotfiles-T128-x-a01", "dotfiles-T128-x-followup-a01"
STUB = (
    "#!/usr/bin/env bash\n"
    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\npath: %s\\nreview: %s\\n" "$(pwd -P)" "$PATH" "${{ORCH_REVIEW_WORKTREE:-}}"\n'
    '  for a; do case $a in *.tsv | *-pr-comments.json) cat -- "$a" ;; esac; done; }} >> "$CALLS/{name}.log"\n'
    '[ ! -x "$CALLS/{name}-hook" ] || "$CALLS/{name}-hook"\n'
    'cat "$CALLS/{name}.out" 2> /dev/null || true\n'
    'exit "$(cat "$CALLS/{name}.status" 2> /dev/null || echo 0)"\n'
)
GH = """#!/usr/bin/env bash
{ printf "argv:"; printf " %s" "$@"; printf "\\n"; } >> "$CALLS/gh.log"
# gh colours its output when forced (a Herdr pane's CLICOLOR_FORCE=1, or GH_FORCE_TTY) unless NO_COLOR is set.
paint() { if [ -z "${NO_COLOR:-}" ] && { [ "${CLICOLOR_FORCE:-0}" != 0 ] || [ -n "${GH_FORCE_TTY:-}" ]; }; then sed $'s/.*/\\e[32m&\\e[0m/'; else cat; fi; }
jq=; prev=; for a; do [ "$prev" != --jq ] || jq=$a; prev=$a; done
case "$1 $2" in
"pr view") if [[ " $* " == *" isDraft "* ]]; then cat "$CALLS/draft" 2> /dev/null || echo false; else cat "$CALLS/head"; fi | paint ;;
"pr checks")
    [ ! -x "$CALLS/checks-hook" ] || "$CALLS/checks-hook"
    exit "$(cat "$CALLS/checks-status" 2> /dev/null || echo 0)" ;;
"pr update-branch")
    git -C "$SEED" fetch -q origin +refs/pull/7/head:refs/remotes/pr/7 main
    git -C "$SEED" checkout -q --detach pr/7
    git -C "$SEED" -c commit.gpgsign=false merge -q --no-edit origin/main
    git -C "$SEED" push -q origin HEAD:refs/pull/7/head
    git -C "$SEED" rev-parse HEAD > "$CALLS/head"
    [ ! -x "$CALLS/update-hook" ] || "$CALLS/update-hook" ;;
"api user") paint < "$CALLS/login" ;;
"api "*)
    case $2 in *reviews) f=$CALLS/reviews.json ;; *) f=$CALLS/comments.json ;; esac
    if [ -n "$jq" ]; then JQ -rc "$jq" "$f"; else cat "$f"; fi | paint ;;
esac
"""
UV = """#!/usr/bin/env bash
{ printf "argv:"; printf " %s" "$@"; printf "\\n"; } >> "$CALLS/uv.log"
shift 4
exec "$@"
"""
SCRIPTS = {
    "orchestrator/sandbox-scan.sh": "sandbox-scan",
    "orchestrator/local-review.sh": "local-review",
    "orchestrator/local-advisory.sh": "local-advisory",
    "orchestrator/fill_sweep.py": "fill_sweep",
    "orchestrator/acceptance-front-matter.py": "acceptance-front-matter",
    "orchestrator/orch-audit.sh": "orch-audit",
    "pr-feedback.py": "pr-feedback",
}
SCAN_HIT = "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
STEPS = [
    "fetch",
    "base",
    "checks",
    "bot",
    "sandbox-scan",
    "local-review",
    "local-advisory",
    "pr-feedback",
    "fill-sweep",
    "receipt",
    "record",
    "audit",
]


class ChainIntegrateTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.calls, bin_dir = self.temp / "calls", self.temp / "bin"
        self.calls.mkdir()
        bin_dir.mkdir()
        (self.temp / "home").mkdir()
        origin, self.seed = self.temp / "origin.git", self.temp / "seed"
        self.git("init", "-q", "--bare", "-b", "main", str(origin), cwd=self.temp)
        self.git("clone", "-q", str(origin), str(self.seed), cwd=self.temp)
        # The stubs are tracked on main, so the main checkout's copies are HEAD's (PR #372 thread 4291474880).
        for rel, name in SCRIPTS.items():
            self.executable(self.seed / "scripts" / rel, STUB.format(name=name))
        self.git("add", "scripts", cwd=self.seed)
        self.commit(self.seed, "a.txt")
        self.git("push", "-q", "origin", "HEAD:main", cwd=self.seed)
        self.commit(self.seed, "b.txt")
        self.git("push", "-q", "origin", "HEAD:refs/pull/7/head", cwd=self.seed)
        self.head = self.git("rev-parse", "HEAD", cwd=self.seed)
        self.git("checkout", "-q", "main", cwd=self.seed)
        self.main = self.temp / "main"
        self.git("clone", "-q", str(origin), str(self.main), cwd=self.temp)
        self.review = self.main / ".claude/worktrees/orchestrator-review"
        self.git("clone", "-q", str(origin), str(self.review), cwd=self.temp)
        self.v = self.main / ".orchestration/validation"
        self.v.mkdir(parents=True)
        rows = "# Acceptance\n\n4280648512\tclass-a\naudit:abcdef1:2\tclass-b\nlocal:abcdef1:1\tadvisory-p2\n123456789\tshort-id\n"
        self.write(f".orchestration/acceptance/{TASK}.md", rows)
        self.write(f".orchestration/tasks/{OWNER}.md", "owner\n")
        self.executable(bin_dir / "gh", GH.replace("JQ", shutil.which("jq") or "jq"))
        self.executable(bin_dir / "uv", UV)
        self.executable(bin_dir / "codex", STUB.format(name="codex"))
        self.executable(bin_dir / "mise", "#!/bin/sh\nexit 1\n")
        bot = {"user": {"login": "chatgpt-codex-connector[bot]"}, "commit_id": self.head}
        (self.calls / "head").write_text(self.head + "\n")
        (self.calls / "reviews.json").write_text(json.dumps([bot]))
        (self.calls / "comments.json").write_text(json.dumps([{"id": 1, "body": "a"}, {"id": 2, "body": "b,\nc"}]))
        (self.calls / "login").write_text("orch\n")
        (self.calls / "orch-audit.out").write_text("audit written\nVerdict: correct\n")
        self.env = {
            **GIT_ENV,
            "CALLS": str(self.calls),
            "SEED": str(self.seed),
            "HOME": str(self.temp / "home"),
            "TMPDIR": str(self.temp),
            "PATH": f"{bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin",
            "CHAIN_POLL_SECONDS": "0",
            "CHAIN_BOT_WAIT": "0",
        }

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=cwd or self.main,
            env={**os.environ, **GIT_ENV},
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def commit(self, repo, name, text=None):
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text or f"{name}\n")
        if text:
            (repo / name).chmod(0o755)
        self.git("add", name, cwd=repo)
        self.git("commit", "-q", "-m", name, cwd=repo)

    def write(self, rel, text):
        path = self.main / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def executable(self, path, text):

**Gathering necessary documentation**
web search: 
web search: https://cli.github.com/manual/gh_help_environment
**Checking for YAML parser support**
exec
/bin/zsh -lc "head -40 home/dot_agents/agent-config.yaml; head -65 scripts/validate-agent-assets.py; sed -n '510,553p' scripts/require-crit-review.py; sed -n '590,626p' scripts/require-crit-review.py; rg -n 'def |env=|subprocess' tests/unit/test_supply_chain_policy.py | head -55; rg -n 'yaml|read_text|agent-config' scripts/validate-agent-assets.py | head -35; sed -n '1,120p' .orchestration/validation/dotfiles-T133-gh-binding-a01-text-security-6486b79.md" in /Users/a0004262/Workspace/dotfiles
 succeeded in 82ms:
# Canonical AI-agent configuration managed by chezmoi.
#
# This file is the single source of truth for Codex and Claude Code.
# Agent-native files are generated from this manifest by scripts/generate-agent-configs.py.
#
# Best-practice rules encoded here:
# - Define one shared capability catalog and render native adapters for every agent.
# - Keep shared skills in ~/.agents/skills and expose the same skill set to every agent.
# - Keep MCP servers disabled by default; enable only after checking scope and credentials.
# - Store credentials as environment-variable references or inherited environment only.
# - Use current maintained MCP servers; deprecated packages are rejected by validation.
# - Keep Codex writable roots for shared agmsg state under codex.sandbox_workspace_write.
#   The Claude sandbox allowWrite list is rendered from the same entries.
# - Let upstream install.sh own ~/.agents/skills/agmsg; never vendor it (assets.agmsg).

schema_version: 1

target_agents:
  - codex
  - claude

skills:
  canonical_dir: ~/.agents/skills

# Model IDs and efforts live only in this map. Profiles render into Claude
# settings, per-profile Codex config files (~/.codex/<name>.config.toml), and
# ~/.agents/model-profiles.env for launchers. Keep main-session models fixed
# within a session; switching models mid-session invalidates the prompt cache.
model_profiles:
  express:
    claude: { model: haiku, effort: low }
    codex: { model: gpt-5.6-luna, model_reasoning_effort: low }
  standard:
    claude: { model: claude-opus-5-5, effort: xhigh, advisor: fable }
    codex:
      model: gpt-6.1-sol
      model_reasoning_effort: xhigh
      notify: ['{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify']
  review:
    # Review independence rests on a fresh context, not a stronger model (operator decision 2026-10-13, plan 007 T717);
#!/usr/bin/env python3
"""Validate Codex, Claude Code, MCP, plugin, and skill assets."""

from __future__ import annotations

import configparser
import fnmatch
import json
import os
import posixpath
import re
import subprocess
import sys
from collections.abc import Iterable
from functools import cache
from pathlib import Path
from typing import Any

import tomllib

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs PyYAML for this script.
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SECRET_PATTERN = re.compile(
    r"""(?ix)
    (
        # A key prefix starts after a non-word character or the start, or right
        # after an escape sequence (a backslash and 1-9 letters or digits: \n,
        # \u000a, \U0000000A, \x0a); the zero-width lookbehinds keep the escape
        # out of the match, so --mask-secrets leaves it intact.
        (?:(?<![A-Za-z0-9_])|(?<=\\[A-Za-z0-9])|(?<=\\[A-Za-z0-9]{2})|(?<=\\[A-Za-z0-9]{3})|(?<=\\[A-Za-z0-9]{4})|(?<=\\[A-Za-z0-9]{5})|(?<=\\[A-Za-z0-9]{6})|(?<=\\[A-Za-z0-9]{7})|(?<=\\[A-Za-z0-9]{8})|(?<=\\[A-Za-z0-9]{9}))
        (?:ghp_[A-Za-z0-9_]{20,} | github_pat_[A-Za-z0-9_]{20,}
           # An sk- key body holds a run of 20+ hyphen-free key characters within
           # its first 64 characters (an sk-proj- key right after proj-); a
           # hyphenated slug such as ...-sk-boundary-a01-review-receipt never
           # does. The bound keeps a long hyphenated run from rescanning (O(n^2)).
           | sk-(?=[A-Za-z0-9_-]{0,64}[A-Za-z0-9_]{20})[A-Za-z0-9_-]{20,})
        | api[_-]?key\s*[:=]\s*["'][^"']+["']
        | password\s*=\s*["'][^"']+["']
        | secret\s*[:=]\s*["'][^"']+["']
        | token\s*[:=]\s*["'][^"']+["']
    )
    """,
)
DEPRECATED_MCP_PACKAGES = {
    "@modelcontextprotocol/server-github": "Use the official ghcr.io/github/github-mcp-server container instead.",
}
REQUIRED_AGMSG_WRITABLE_ROOTS = {
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db",
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/teams",
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/run",
    "{{ .chezmoi.homeDir }}/.agents/skills/agmsg/ext-tools",
}
SYNC_TIMEOUT_BUDGET_S = 30  # PLAN H3 pins the per-source, per-event synchronous budget.
HOOK_COMPOSITION_SOURCES = {
    "claude": (Path("home/.chezmoitemplates/claude-settings-managed.json"), "json"),
    "codex": (Path("home/.chezmoitemplates/codex-config-managed.toml"), "toml"),
    "compactiondb": (
        Path("vendor/compactiondb/.claude/settings.fragment.json"),
        "json",
    ),
}
                available[key] -= 1
                break
        else:
            missing[feedback_key(item)] += 1
    return missing


def pr_base_errors(root: Path, evidence: dict, pr: int, head: str, base: str) -> list[str]:
    """Bind the base before executing a collector, independently of PR-owned JSON/code."""
    env = {key: value for key, value in os.environ.items() if key not in {"CLICOLOR_FORCE", "GH_FORCE_TTY", "GH_REPO"}}
    env["NO_COLOR"] = "1"
    failure = f"could not verify PR #{pr} base on GitHub; fetch the base and rerun scripts/pr-feedback.py"
    try:
        repository = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner"],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        repo_data = json.loads(repository.stdout) if repository.returncode == 0 else None
        repo = repo_data.get("nameWithOwner") if isinstance(repo_data, dict) else None
        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            return [failure]
        if evidence.get("repo") != repo:
            return [
                f"{PR_FEEDBACK_ENV} does not match the local GitHub repository {repo}; rerun scripts/pr-feedback.py"
            ]
        result = subprocess.run(
            ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "headRefOid,baseRefName,baseRefOid"],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        metadata = json.loads(result.stdout) if result.returncode == 0 else None
    except (OSError, json.JSONDecodeError):
        return [failure]
    if not isinstance(metadata, dict):
        return [failure]
    github_base = metadata.get("baseRefOid")
    github_ref = metadata.get("baseRefName")
    """Re-collect the PR's feedback and require every current item in the evidence.

    A hand-written or stale document cannot pass: the guard runs the GitHub
    base SHA's scripts/pr-feedback.py (the PR under review cannot swap it) for the
    evidence's PR, requires the PR head on GitHub to be this HEAD, and requires
    each collected item (as a multiset) to be present. A bot review is not
    required; when one exists it is collected and must be dispositioned like any
    other item.
    """
    pr = evidence.get("pr")
    if not isinstance(pr, int) or isinstance(pr, bool) or pr <= 0:
        return [f"{PR_FEEDBACK_ENV} must name its pull request number in `pr`"]
    errors = pr_base_errors(root, evidence, pr, head, base)
    if errors:
        return errors
    with tempfile.TemporaryDirectory() as temporary:
        collected_path = Path(temporary) / "collected.json"
        # An advanced local base may contain untrusted code despite a safe merge-base.
        # Execute only the GitHub-authenticated base's collector, including bootstrap.
        collector = root / "scripts/pr-feedback.py"
        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
        if base_collector.returncode == 0:
            collector = Path(temporary) / "pr-feedback.py"
            collector.write_text(base_collector.stdout)
        result = subprocess.run(
            [sys.executable, str(collector), str(pr), "--repo", evidence["repo"], "--json", str(collected_path)],
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0 or not collected_path.is_file():
            detail = (result.stderr or result.stdout).strip().splitlines()[-1:] or ["no output"]
            return [f"could not re-collect PR #{pr} feedback with scripts/pr-feedback.py: {detail[0]}"]
        collected = json.loads(collected_path.read_text())
    if collected.get("head_sha") != head:
5:import subprocess
17:    def test_installer_cleanup_survives_mock_function_returns(self):
100:                result = subprocess.run(
108:                    env={**os.environ, "HOME": str(home), "TMPDIR": str(temp)},
117:    def test_installer_cleanup_preserves_failure_status(self):
135:                result = subprocess.run(
143:                    env={**os.environ, "HOME": str(root / "home"), "TMPDIR": str(root / "tmp")},
149:    def run_with_tmpdir(self, script, relative, home, **env):
163:        return subprocess.run(
165:            env={**os.environ, "HOME": str(home), "TMPDIR": str(tmp), "PATH": f"{shim}:{os.environ['PATH']}", **env},
171:    def test_a_failed_download_keeps_a_working_tool_and_a_failed_check_never_does(self):
256:    def test_every_apply_installers_skip_when_current_and_keep_the_tool_offline(self):
290:                result = subprocess.run(
292:                    env={**os.environ, "HOME": str(home), "NEWEST": newest, "LOOKUP_FAIL": lookup_fail},
309:    def test_mise_main_preserves_install_failure(self):
312:            result = subprocess.run(
327:    def test_executable_downloads_are_verified_and_not_piped_to_shell(self):
342:    def test_binary_installers_replace_from_same_directory_stages(self):
354:    def test_mise_tools_track_latest_behind_the_cooldown(self):
397:            result = subprocess.run(
412:    def test_lifecycle_runs_the_upgrade_through_make_update_without_locked_installs(self):
428:    def test_mise_apply_replaces_live_symlinks_with_independent_copies(self):
444:            subprocess.run(
466:    def test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts(self):
480:    def test_mise_config_backends_and_http_tools(self):
517:    def test_rolling_installers_resolve_through_the_release_helper(self):
559:    def test_sheldon_uses_locked_crates_io_source(self):
571:    def test_sheldon_git_sources_have_revisions(self):
578:    def test_externals_use_fixed_urls_and_checksums(self):
588:    def test_externals_render_without_network_discovery(self):
595:        result = subprocess.run(
607:            env=env,
618:    def test_external_checksum_failure_preserves_destination(self):
637:            result = subprocess.run(
663:    def test_renovate_owns_dependency_update_notifications(self):
689:    def test_setup_ci_rejects_and_preserves_local_drift(self):
22:    import yaml
24:    yaml = None
79:def load_yaml(path: Path) -> dict[str, Any]:
80:    if yaml is None:
82:    data = yaml.safe_load(path.read_text()) or {}
89:    text = path.read_text()
168:    text = path.read_text()
174:    if yaml is None:
176:    data = yaml.safe_load(text[4:end]) or {}
201:        openai_yaml = skill_dir / "agents/openai.yaml"
202:        if openai_yaml.exists():
203:            parsed = load_yaml(openai_yaml)
205:                fail(f"{openai_yaml} must be a mapping")
219:        if not symlink.exists() or symlink.read_text() != expected_target:
229:    manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
232:    for number, line in enumerate(manifest_path.read_text().splitlines(), start=1):
256:    marketplace = json.loads(marketplace_path.read_text())
272:            manifest = json.loads(manifest_path.read_text())
392:    if not crit_rule.exists() or "/crit" not in crit_rule.read_text():
421:    """The parsed [[hooks.<Event>]] matcher group that generate-agent-configs.py renders for one hook."""
675:        for line in (removal_file.read_text().splitlines() if removal_file.exists() else [])
690:        fail("agent-config.yaml must declare third-party assets under assets:")
798:        for match in LITERAL_VERSION_ASSIGNMENT.finditer(path.read_text()):
804:    manifest_path = ROOT / "home/dot_agents/agent-config.yaml"
805:    manifest = load_yaml(manifest_path)
848:    readme = (ROOT / "README.md").read_text()
850:    readme_worker = f"`worker_kind` in `home/dot_agents/agent-config.yaml` (currently `{worker_kind}`;"
857:        f"`orchestrator_kind` in `home/dot_agents/agent-config.yaml` (currently `{orchestrator_kind}`;"
928:    text = path.read_text()
971:    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
984:    codex_agents = (ROOT / "home/dot_config/codex/AGENTS.md").read_text()
997:    guard_text = guard_path.read_text()
1014:    readme = (ROOT / "README.md").read_text()
1028:    updater = (ROOT / "scripts/update-agent-assets.sh").read_text()
1044:        fail("home/dot_agents/agent-config.yaml must enable the Ponytail Codex plugin")
Reading additional input from stdin...
OpenAI Codex v0.163.0
--------
workdir: /Users/a0004262/Workspace/dotfiles
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: concise
session id: 01a16103-29c3-7ae2-96bc-08d2c710e0f1
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-gh-binding-a01.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both /Users/a0004262/.codex/hooks.json and /Users/a0004262/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
対象タスクと参照先の記録を読み、設計上の検証結果が実際の実行対象に結び付くかを確認します。agmsg-orchestration と Ponytail のレビュー手順を使い、ファイルは変更しません。
exec
/bin/zsh -lc 'cat /Users/a0004262/.agents/skills/agmsg-orchestration/SKILL.md' in /Users/a0004262/Workspace/dotfiles
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

**Analyzing audit and binding issues**
**Evaluating executable binding and script scope**
codex
既存の gate は、子プロセス内でローカル Git 設定から対象リポジトリを選び直しています。`gh` の実行ファイルだけを固定しても残る経路です。子ソースの編集・wrapper 追加を禁じた今回の範囲で、固定リポジトリの要件を満たせるかを詰めています。
exec
/bin/zsh -lc "sed -n '596,626p' scripts/require-crit-review.py; rg -n 'git|subprocess|os.environ|run\\(' tests/unit/test_generate_agent_configs.py | head -65; rg -n 'os.environ|subprocess|def git|def run_git' tests/unit/test_supply_chain_policy.py tests/unit/test_regime_ci.py tests/unit/test_task_checkers.py; rg -n 'trusted-root|trusted_tools|symlink|case|swap|in-process|private|snapshot' .orchestration/tasks/dotfiles-T133-gh-binding-a01.md; ls -ld /var /var/empty /private /private/var /private/var/empty; command -v gh mise uv python3" in /Users/a0004262/Workspace/dotfiles
 succeeded in 68ms:
    required; when one exists it is collected and must be dispositioned like any
    other item.
    """
    pr = evidence.get("pr")
    if not isinstance(pr, int) or isinstance(pr, bool) or pr <= 0:
        return [f"{PR_FEEDBACK_ENV} must name its pull request number in `pr`"]
    errors = pr_base_errors(root, evidence, pr, head, base)
    if errors:
        return errors
    with tempfile.TemporaryDirectory() as temporary:
        collected_path = Path(temporary) / "collected.json"
        # An advanced local base may contain untrusted code despite a safe merge-base.
        # Execute only the GitHub-authenticated base's collector, including bootstrap.
        collector = root / "scripts/pr-feedback.py"
        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
        if base_collector.returncode == 0:
            collector = Path(temporary) / "pr-feedback.py"
            collector.write_text(base_collector.stdout)
        result = subprocess.run(
            [sys.executable, str(collector), str(pr), "--repo", evidence["repo"], "--json", str(collected_path)],
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0 or not collected_path.is_file():
            detail = (result.stderr or result.stdout).strip().splitlines()[-1:] or ["no output"]
            return [f"could not re-collect PR #{pr} feedback with scripts/pr-feedback.py: {detail[0]}"]
        collected = json.loads(collected_path.read_text())
    if collected.get("head_sha") != head:
12:import subprocess
169:    result = subprocess.run(
534:        def parse_digits_as_int(text: str) -> dict:
540:        stderr = self.run_set_asset_with_parser(parse_digits_as_int)
614:        result = subprocess.run(
618:            stdout=subprocess.PIPE,
619:            stderr=subprocess.PIPE,
621:                **os.environ,
651:        result = subprocess.run(
655:            stdout=subprocess.PIPE,
656:            stderr=subprocess.PIPE,
657:            env={**os.environ, "HOME": str(home)},
685:                    "network": {"allowedDomains": ["github.com"], "allowUnixSockets": []},
752:                        "github.com",
753:                        "api.github.com",
754:                        "uploads.github.com",
755:                        "objects.githubusercontent.com",
756:                        "codeload.github.com",
808:        patterns = ["agmsg-dispatch *", "gh *", "git push *", "herdr-agents *", "actas-claim.sh *", "arbitrary *"]
850:            result = subprocess.run(
854:                stdout=subprocess.PIPE,
855:                stderr=subprocess.PIPE,
898:        result = subprocess.run(
902:            stdout=subprocess.PIPE,
903:            stderr=subprocess.PIPE,
904:            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
933:        result = subprocess.run(
937:            stdout=subprocess.PIPE,
938:            stderr=subprocess.PIPE,
939:            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
1022:    def run_profile(self, manifest: dict, home: Path, current: str) -> subprocess.CompletedProcess:
1024:        return subprocess.run(
1029:            env={**os.environ, "HOME": str(home)},
1293:        result = subprocess.run(
1298:            env={**os.environ, "HOME": str(home)},
1317:        result = subprocess.run(
1325:            stdout=subprocess.PIPE,
1326:            stderr=subprocess.PIPE,
1327:            env={**os.environ, "HOME": str(home)},
1346:        result = subprocess.run(
1350:            stdout=subprocess.PIPE,
1351:            stderr=subprocess.PIPE,
1352:            env={**os.environ, "HOME": str(home)},
1373:        result = subprocess.run(
1377:            stdout=subprocess.PIPE,
1378:            stderr=subprocess.PIPE,
1379:            env={**os.environ, "HOME": str(home)},
1520:    def test_model_profiles_env_selects_no_github_store(self) -> None:
1838:                    result = subprocess.run(
1844:                            **os.environ,
1879:                "with open(os.environ['BROWSER_CALLS'], 'a') as out:\n"
1882:                "    print(os.environ['BROWSER_LISTING'])\n"
1886:                "    sys.exit(int(os.environ['OPEN_EXIT']))\n"
1893:                "with open(os.environ['AGENT_CALLS'], 'a') as out:\n"
1935:                    result = subprocess.run(
1941:                            **os.environ,
1995:                "with open(os.environ['BROWSER_CALLS'], 'a') as out:\n"
1998:                "    print(os.environ['BROWSER_LISTING'])\n"
2005:                "with open(os.environ['AGENT_CALLS'], 'a') as out:\n"
2011:            result = subprocess.run(
2018:                    **os.environ,
2187:                    result = subprocess.run(
2251:            browser.write_text(f"#!{sys.executable}\nimport os\nprint(os.environ['BROWSER_LISTING'])\n")
2258:                "with open(os.environ['AGENT_CALLS'], 'a') as out:\n"
2261:                "    Path(os.environ['PIN_STATE']).write_text(str('--pin-tab' in sys.argv))\n"
tests/unit/test_supply_chain_policy.py:5:import subprocess
tests/unit/test_supply_chain_policy.py:100:                result = subprocess.run(
tests/unit/test_supply_chain_policy.py:108:                    env={**os.environ, "HOME": str(home), "TMPDIR": str(temp)},
tests/unit/test_supply_chain_policy.py:135:                result = subprocess.run(
tests/unit/test_supply_chain_policy.py:143:                    env={**os.environ, "HOME": str(root / "home"), "TMPDIR": str(root / "tmp")},
tests/unit/test_supply_chain_policy.py:163:        return subprocess.run(
tests/unit/test_supply_chain_policy.py:165:            env={**os.environ, "HOME": str(home), "TMPDIR": str(tmp), "PATH": f"{shim}:{os.environ['PATH']}", **env},
tests/unit/test_supply_chain_policy.py:290:                result = subprocess.run(
tests/unit/test_supply_chain_policy.py:292:                    env={**os.environ, "HOME": str(home), "NEWEST": newest, "LOOKUP_FAIL": lookup_fail},
tests/unit/test_supply_chain_policy.py:312:            result = subprocess.run(
tests/unit/test_supply_chain_policy.py:397:            result = subprocess.run(
tests/unit/test_supply_chain_policy.py:444:            subprocess.run(
tests/unit/test_supply_chain_policy.py:589:        env = os.environ.copy()
tests/unit/test_supply_chain_policy.py:595:        result = subprocess.run(
tests/unit/test_supply_chain_policy.py:637:            result = subprocess.run(
tests/unit/test_task_checkers.py:1:"""Run scripts/orchestrator/task-consistency-check.py and ledger-check.py as subprocesses (plan 007 T704).
tests/unit/test_task_checkers.py:5:`found`; the subprocess pattern of tests/unit/test_orchestrator_tools.py. tests/fixtures/lessons/ holds copies from
tests/unit/test_task_checkers.py:13:import subprocess
tests/unit/test_task_checkers.py:41:        result = subprocess.run(
tests/unit/test_task_checkers.py:46:            env={**os.environ, "STUB_BIN": str(self.temp / "bin"), "STUB_CAT_FILE": cat_file, "STUB_GREP": grep},
tests/unit/test_regime_ci.py:7:import subprocess
tests/unit/test_regime_ci.py:55:        env = {k: v for k, v in os.environ.items() if k != "GITHUB_HEAD_REF"}
tests/unit/test_regime_ci.py:58:    def git(self, *args):
tests/unit/test_regime_ci.py:60:        return subprocess.run(
tests/unit/test_regime_ci.py:118:        return subprocess.run(
tests/unit/test_regime_ci.py:230:        doc = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
tests/unit/test_regime_ci.py:344:        result = subprocess.run(
tests/unit/test_regime_ci.py:432:            "(root / '.git' / 'checker.json').write_text(json.dumps({'argv': sys.argv, 'env': dict(os.environ)}))\n"
tests/unit/test_regime_ci.py:477:        doc = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
33:  - {control: "trusted parent before first instruction", disposition: "residual: dotfiles-T133-trusted-entrypoint-binding-a01 owns automatic parent binding; authenticated use stays disabled until the orchestrator measures a clean, absolutely bound parent and private namespace for every non-gh process in the route."}
36:  - {control: "in-process effects", disposition: "closed: tests/unit/test_chain_glue.py::GhBindingTest::test_git_environment_cannot_redirect_fixture_writes"}
44:  - {control: "orchestrator effect canonical measurements", disposition: "residual: dotfiles-T133-gh-binding-followup-a01 owns measurement automation; gh-free private-clone evidence and trusted-parent observations must precede a fresh review of the complete populated bytes."}
73:2. Add trusted_tools.gh with version "2.102.0" and path "~/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh" to agent-config.yaml; later uv/Python/Node bindings extend sibling entries.
77:   Require the declared version-specific absolute realpath, regular executable, existence, non-shim/trusted-root checks and matching reported version; consume that checked target without rediscovery. Missing/mismatching identity emits exactly "refused: gh binding", exits nonzero and performs no canonical operation; no PATH/mise/latest fallback for gh.
80:   Keep today's non-gh resolver algorithms, but constrain their execution and outputs to that preverified private namespace; discovery receives no tokens. A PATH- or mise-selected unchecked parent is forbidden. No self-reexec, sentinel or child cleanup counts as pre-exec evidence; without this compensating control authenticated operation stays blocked.
81:4. R1:76: launch every bound gh, including identity probes, with a constructed allowlist and protected GH_CONFIG_DIR=/var/empty on this host; verify its resolved directory and ancestors are protected, it is empty and contains no symlink/config payload. Missing/unsafe configuration refuses, without default-home fallback or directory creation.
91:   Write fixtures first; for each behavioral case record red against origin/main production bytes and green at the fix commit, with selector, full baseline/red-fixture/fix SHAs, exact commands, stdout/stderr and exit status. Red must reach its intended assertion, not import/setup/missing-tool failure; inventory-only requirements use diff evidence, not fabricated red tests.
114:Before C-80/anchor, the orchestrator expands the gh-binding-followup-a01 owner stub for every assigned residual and the three future consumers; confirms Item 0's amended inventory; obtains main40/design digest from a fresh private HTTPS bare clone of the fixed repository, gh-free and independent of the shared object store.
drwxr-xr-x   6 root  wheel   192 Oct 22 08:28 /private
drwxr-xr-x  35 root  wheel  1120 Sep 30 14:56 /private/var
drwxr-xr-x   2 root  sys      64 Sep 24 16:10 /private/var/empty
lrwxr-xr-x@  1 root  wheel    11 Sep 24 16:10 /var -> private/var
drwxr-xr-x   2 root  sys      64 Sep 24 16:10 /var/empty
/Users/a0004262/.local/share/mise/shims/gh
/Users/a0004262/.local/bin/mise
/Users/a0004262/.local/share/mise/shims/uv
/Users/a0004262/.local/share/mise/shims/python3

**Verifying test coverage and token handling**
**Analyzing Git environment isolation limits**
exec
/bin/zsh -lc "nl -ba scripts/require-crit-review.py | sed -n '517,550p;596,623p'; rg -n 'trusted|private|git_environment|test_.*swap|test_.*case' tests/unit/trusted_exec_contract.py | head -45; git diff --numstat -- .orchestration/tasks/dotfiles-T133-gh-binding-a01.md; /usr/bin/shasum -a 256 .orchestration/tasks/dotfiles-T133-gh-binding-a01.md" in /Users/a0004262/Workspace/dotfiles
 succeeded in 73ms:
   517	def pr_base_errors(root: Path, evidence: dict, pr: int, head: str, base: str) -> list[str]:
   518	    """Bind the base before executing a collector, independently of PR-owned JSON/code."""
   519	    env = {key: value for key, value in os.environ.items() if key not in {"CLICOLOR_FORCE", "GH_FORCE_TTY", "GH_REPO"}}
   520	    env["NO_COLOR"] = "1"
   521	    failure = f"could not verify PR #{pr} base on GitHub; fetch the base and rerun scripts/pr-feedback.py"
   522	    try:
   523	        repository = subprocess.run(
   524	            ["gh", "repo", "view", "--json", "nameWithOwner"],
   525	            cwd=root,
   526	            env=env,
   527	            capture_output=True,
   528	            text=True,
   529	            check=False,
   530	        )
   531	        repo_data = json.loads(repository.stdout) if repository.returncode == 0 else None
   532	        repo = repo_data.get("nameWithOwner") if isinstance(repo_data, dict) else None
   533	        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
   534	            return [failure]
   535	        if evidence.get("repo") != repo:
   536	            return [
   537	                f"{PR_FEEDBACK_ENV} does not match the local GitHub repository {repo}; rerun scripts/pr-feedback.py"
   538	            ]
   539	        result = subprocess.run(
   540	            ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "headRefOid,baseRefName,baseRefOid"],
   541	            cwd=root,
   542	            env=env,
   543	            capture_output=True,
   544	            text=True,
   545	            check=False,
   546	        )
   547	        metadata = json.loads(result.stdout) if result.returncode == 0 else None
   548	    except (OSError, json.JSONDecodeError):
   549	        return [failure]
   550	    if not isinstance(metadata, dict):
   596	    required; when one exists it is collected and must be dispositioned like any
   597	    other item.
   598	    """
   599	    pr = evidence.get("pr")
   600	    if not isinstance(pr, int) or isinstance(pr, bool) or pr <= 0:
   601	        return [f"{PR_FEEDBACK_ENV} must name its pull request number in `pr`"]
   602	    errors = pr_base_errors(root, evidence, pr, head, base)
   603	    if errors:
   604	        return errors
   605	    with tempfile.TemporaryDirectory() as temporary:
   606	        collected_path = Path(temporary) / "collected.json"
   607	        # An advanced local base may contain untrusted code despite a safe merge-base.
   608	        # Execute only the GitHub-authenticated base's collector, including bootstrap.
   609	        collector = root / "scripts/pr-feedback.py"
   610	        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
   611	        if base_collector.returncode == 0:
   612	            collector = Path(temporary) / "pr-feedback.py"
   613	            collector.write_text(base_collector.stdout)
   614	        result = subprocess.run(
   615	            [sys.executable, str(collector), str(pr), "--repo", evidence["repo"], "--json", str(collected_path)],
   616	            cwd=root,
   617	            check=False,
   618	            text=True,
   619	            stdout=subprocess.PIPE,
   620	            stderr=subprocess.PIPE,
   621	        )
   622	        if result.returncode != 0 or not collected_path.is_file():
   623	            detail = (result.stderr or result.stdout).strip().splitlines()[-1:] or ["no output"]
1:"""Shared probes of design-quality 5.14 item 7: one attack each in a temporary fixture, and the trusted parent."""
27:    """run_under_trusted_parent refused the script before running anything."""
164:    base = Path(tempfile.mkdtemp(prefix="trusted-exec-")).resolve()
221:def run_under_trusted_parent(script, *args):
100	15	.orchestration/tasks/dotfiles-T133-gh-binding-a01.md
6486b79dfb7e3dbf62b680d7dce6b2af9f5698294f35659e886f4673f9aff2b6  .orchestration/tasks/dotfiles-T133-gh-binding-a01.md

web search: 
web search: 'GH_REPO'
**Analyzing risk in code validation and policy checks**
**Reviewing verification and authentication nuances**
**Analyzing environment variable handling**
**Evaluating security profile and gate bindings**
**Assessing security scope and test coverage**
**Summarizing security findings and tests**

I’m wrapping up with two main security issues—one around fixed destination enforcement and another about Python inheritance of isolation flags—and outlining test gaps and requirements to justify conclusions with repository evidence and clear summaries.
web search: 
web search: https://docs.python.org/3/using/cmdline.html#cmdoption-I
exec
/bin/zsh -lc "sed -n '76,90p' .orchestration/tasks/dotfiles-T133-gh-binding-a01.md; sed -n '1,105p' /Users/a0004262/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md" in /Users/a0004262/Workspace/dotfiles
 succeeded in 12ms:
3. Replace gh discovery in chain-integrate.sh and orch-gate.sh, and bind local-review.sh's descendant namespace to the declaration. Cover pr-feedback/gate collectors and review descendants without editing their sources or adding wrappers.
   Require the declared version-specific absolute realpath, regular executable, existence, non-shim/trusted-root checks and matching reported version; consume that checked target without rediscovery. Missing/mismatching identity emits exactly "refused: gh binding", exits nonzero and performs no canonical operation; no PATH/mise/latest fallback for gh.
   gh api uses --hostname github.com and fixed repos/mryfmo/dotfiles endpoints; other subcommands use --repo github.com/mryfmo/dotfiles or a full fixed-host URL under item 8. Do not add the unsupported --hostname flag to gh pr; version probes make no network call.
   R1:39: before any script, loader, resolver or parser runs with credentials, the orchestrator supplies and measures the trusted parent required by items 2/9, binding Bash, mise, git, uv, Python, Node and every other non-gh executable the selected route can execute.
   Keep today's non-gh resolver algorithms, but constrain their execution and outputs to that preverified private namespace; discovery receives no tokens. A PATH- or mise-selected unchecked parent is forbidden. No self-reexec, sentinel or child cleanup counts as pre-exec evidence; without this compensating control authenticated operation stays blocked.
4. R1:76: launch every bound gh, including identity probes, with a constructed allowlist and protected GH_CONFIG_DIR=/var/empty on this host; verify its resolved directory and ancestors are protected, it is empty and contains no symlink/config payload. Missing/unsafe configuration refuses, without default-home fallback or directory creation.
   Only the call's explicitly supplied token is inherited, normalized to GH_TOKEN; never fetch credentials implicitly from home config/keychain. Supply required nonsecret constants explicitly, including trusted HOME/PATH, absolute UV_CACHE_DIR, fixed configuration, disabled prompts/update notices and plain output; probes get no token.
   Reject ambient GH_HOST/GH_CONFIG_DIR/XDG_CONFIG_HOME, proxies, loader/startup variables and Git configuration overrides. Apply items 2/9 to the parent and descendants too; every env -i contract carries UV_CACHE_DIR. Record the complete allowed-name set without token values.
   Test planted home/XDG gh config with http_unix_socket, aliases and alternate hosts; neither transport nor child execution may change. Test refusal of unsafe configuration and a positive authenticated operation using the controlled source. Sources: [gh config](https://cli.github.com/manual/gh_config), [configuration discovery](https://cli.github.com/manual/gh_help_environment).
5. No workflow/regime.yml, launcher, permission, dependency, unrelated resolver algorithm or acceptance-semantic change. No new/renamed executable or executable evidence. Future checkers and missing consumers remain explicitly owned, never represented as implemented here.
6. The test wildcard authorizes only test_supply_chain_policy.py, test_chain_glue.py, test_regime_ci.py and test_task_checkers.py; reuse trusted_exec_contract.py without modifying it and preserve existing assertions.
   R1:38: fix reused chain/regime/checker fixture Git helpers before any init/add/commit/reset/fetch: construct fresh environments, explicit fixture roots and neutralized configuration; do not merge os.environ. Plant GIT_DIR/GIT_WORK_TREE/GIT_CONFIG_* and hostile local includes/hooks; a second disposable repository's refs/index/bytes and external markers must stay unchanged. See [Git environment](https://git-scm.com/docs/git).
   R1:80: each active route needs a successful authenticated-operation fixture through the declared target, with a synthetic credential, expected fixed host/repository, response consumption and descendant coverage; separately test missing/version/path refusals. Identity refusal can never satisfy a success or decoy assertion.
   Put an executable gh decoy on the lookup path and a hostile mise answer; prove neither is executed or receives the synthetic credential. The trusted-parent fixture binds non-gh tools but must not prebind gh and thereby mask the production defect.
   Implement every closed selector above; the policy test uses separate subtests per refusal rule, and the consumer/environment/configuration matrices cover all three active routes. Absent future routes are not passing matrix entries.
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

**Finalizing report summary**

I’m wrapping up with a concise 280-word summary covering two main findings around control decisions and validated execution. I’m including clickable, relative file paths per developer preference, noting no duplicate states and highlighting risks like “same-user residual remains.” I’ll also mention gate priorities, test matrix limits, and immutable repo constraints as key points.
**Confirming final review status**
codex
- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:76` — Forbidding descendant edits and wrappers prevents the promised fixed-repository binding: `scripts/require-crit-review.py:519` removes `GH_REPO`, then discovers the repository from local Git context and passes that result to `gh pr view`; `scripts/pr-feedback.py:84` also omits `--hostname`. A pinned executable does not bind these decisions to `github.com/mryfmo/dotfiles`; authorize the descendant changes and test hostile repository configuration through the real gate. [GitHub CLI environment](https://cli.github.com/manual/gh_help_environment)

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:83` — Applying item 9 to every descendant conflicts with the excluded gate’s collector launch at `scripts/require-crit-review.py:615`, which starts `[sys.executable, collector, …]` without `-I`; the parent’s isolation flags do not propagate, and `PYTHONSAFEPATH` alone does not disable user-site startup code. Authorize this launch change and require a real-descendant startup-hook test before claiming the isolation contract is satisfied. [Python isolation options](https://docs.python.org/3/using/cmdline.html#cmdoption-I)

📝 まとめ: Reviewed all 37 threat rows, existing consumer paths, and cited acceptance/review history. Two findings remain for orchestrator disposition; no files changed.

Not checked: future implementation, CI, or live Linux/race behavior; same-user replacement and credential separation remain acknowledged residual risks.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
110,607
- [P1] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:76` — Forbidding descendant edits and wrappers prevents the promised fixed-repository binding: `scripts/require-crit-review.py:519` removes `GH_REPO`, then discovers the repository from local Git context and passes that result to `gh pr view`; `scripts/pr-feedback.py:84` also omits `--hostname`. A pinned executable does not bind these decisions to `github.com/mryfmo/dotfiles`; authorize the descendant changes and test hostile repository configuration through the real gate. [GitHub CLI environment](https://cli.github.com/manual/gh_help_environment)

- [P2] High confidence `.orchestration/tasks/dotfiles-T133-gh-binding-a01.md:83` — Applying item 9 to every descendant conflicts with the excluded gate’s collector launch at `scripts/require-crit-review.py:615`, which starts `[sys.executable, collector, …]` without `-I`; the parent’s isolation flags do not propagate, and `PYTHONSAFEPATH` alone does not disable user-site startup code. Authorize this launch change and require a real-descendant startup-hook test before claiming the isolation contract is satisfied. [Python isolation options](https://docs.python.org/3/using/cmdline.html#cmdoption-I)

📝 まとめ: Reviewed all 37 threat rows, existing consumer paths, and cited acceptance/review history. Two findings remain for orchestrator disposition; no files changed.

Not checked: future implementation, CI, or live Linux/race behavior; same-user replacement and credential separation remain acknowledged residual risks.
Verdict: incorrect
