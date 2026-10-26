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
session id: 01a15b35-df48-7b40-8d55-77ddfacbbf2a
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
対象タスクと参照先の acceptance・review 記録を読み、各 threat row の制御が実際の実行まで拘束できるか確認します。agmsg-orchestration と Ponytail の手順を参照し、読み取り専用でレビューします。
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
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
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
   101	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees"
   102	  - control: S11 carried identity-field screening
   103	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member"
   104	  - control: <skills-root>/<name>/.claude-plugin/plugin.json
   105	    disposition: "residual: S12 includes enterprise skills at <managed-root>/.claude/skills and the other five admitted skills roots, even when the plugin is disabled."
   106	  - control: <plugins-root>/installed_plugins.json
   107	    disposition: "residual: S13 accepts only the declared registry shape and contained roots whose descriptors are read; an install record cannot add an unchecked root."
   108	  - control: <plugins-root>/known_marketplaces.json
   109	    disposition: "residual: S14 permits the declared empty registry only; refresh sources and executable header helpers have no canonical worker form."
   110	  - control: <plugin-root>/.claude-plugin/plugin.json
   111	    disposition: "residual: S15 admits declared descriptive metadata and scalar file references only; every selected file is inspected even for a disabled plugin."
   112	  - control: <plugin-hook-file>
   113	    disposition: "residual: S16 covers default and explicitly referenced hook files separately; plugin-owned executable handlers have no canonical worker operation."
   114	  - control: <marketplace-root>/.claude-plugin/marketplace.json
   115	    disposition: "residual: S17 admits descriptive metadata and an absent or empty plugin list only; command sources and additional plugin selections refuse."
   116	  - control: <plugin-mcp-file>
   117	    disposition: "residual: S18 checks default and referenced MCP files independently, admitting no nonempty worker server definitions."
   118	  - control: <managed-root>/managed-mcp.json
   119	    disposition: "residual: S19 applies the same empty-server rule independently of managed-settings precedence or administrative ownership."
   120	  - control: <skills-root>/<name>/SKILL.md
   121	    disposition: "residual: S20 inspects admitted Markdown files and frontmatter without invoking them; unknown frontmatter and inline or fenced dynamic commands refuse."
   122	  - control: <commands-root>/<name>.md
   123	    disposition: "residual: S21 reads every default or scalar-referenced command file; object mappings, inline content and directory references do not bypass Markdown inspection."
   124	  - control: <agents-root>/<name>.md
   125	    disposition: "residual: S22 inspects declared subagent metadata and refuses executable frontmatter without starting a subagent."
   126	  - control: <plugin-lsp-file>
   127	    disposition: "residual: S23 admits empty LSP configuration only; language-server commands and arguments have no canonical worker operation."
   128	  - control: pre-start refusal of unknown settings keys
   129	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys"
   130	  - control: pre-start refusal of undeclared provider selectors
   131	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors"
   132	  - control: pre-start refusal of foreign repository roots
   133	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root"
   134	  - control: pre-start refusal of object-form plugin components
   135	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components"
   136	  - control: pre-start refusal of non-command hook handlers
   137	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch"
   138	  - control: pre-start refusal of untrusted executable environment-file contents
   139	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents"
   140	  - control: manifest-selected non-shim launch interpreter
   141	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names"
   142	  - control: Darwin platform-injected launch environment
   143	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment"
   144	  - control: regime-declared launch environment
   145	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment"
   146	  - control: plugin activation and additional executable components
   147	    disposition: "residual: explicit false entries supplement screening; higher-scope enables, sync, dependencies, workflows, monitors and undeclared components refuse before launch."
   148	  - control: non-file managed delivery and launch overrides
   149	    disposition: "residual: unenumerable MDM, server delivery, host settings and caller-selected sources refuse without running a helper to discover their content."
   150	  - control: lower-scope sandbox array merging
   151	    disposition: "residual: source-specific canonical fragments reject extra exclusions, write roots and socket grants before Claude can merge arrays; live enforcement and later changes remain unverified."
   152	  - control: actual enterprise skills root
   153	    disposition: "residual: inventory starts at <managed-root>/.claude/skills, and temporary managed-root fixtures plant both Markdown and bundled plugin payloads there on both platforms."
   154	  - control: <absolute-home>/.agents/permgate-policy.yaml
   155	    disposition: "residual: explicit static Edit denies protect the policy input and fixtures assert unchanged bytes; legacy hook environment and execution binding remain deferred."
   156	  - control: <absolute-home>/.local/lib/python*/site-packages
   157	    disposition: "residual: directory-target and descendant denies retain protection for .pth, usercustomize.py and sitecustomize.py without claiming isolated interpreter startup."
   158	  - control: <absolute-home>/Library/Python/*/lib/python/site-packages
   159	    disposition: "residual: macOS user-site directory and descendant patterns remain in the static inventory; planted-startup execution belongs to the binding task."
   160	  - control: <absolute-home>/.claude/hooks/orchestrator-only.sh
   161	    disposition: "residual: the installed guard is an explicitly protected consumed input; routing fixtures do not close concurrent same-UID path swaps."
   162	  - control: formatter and project-map configuration selection
   163	    disposition: "residual: worker and outside-anchor input paths suppress tool execution; formatter availability and complete tool-chain binding remain deferred."
   164	  - control: .orchestration/dotfiles-T133-worker-write-boundary-a03/task.md
   165	    disposition: "residual: retain the predecessor task copy and all a03 evidence unchanged in the declared retained predecessor directory; neither deletion nor new predecessor writes is authorized."
   166	  - control: .orchestration/dotfiles-T133-worker-write-boundary-a04/task.md
   167	    disposition: "residual: the a04 copy is byte-identical to the complete dispatched a04 text and bound by SHA256 in TASK and RESULT."
   168	  - control: evidence records
   169	    disposition: "residual: report, validation, sandbox, learning, autoskill and review records preserve commands and identities while distinguishing proposals from acceptance authority."
   170	  - control: task metadata
   171	    disposition: "residual: the orchestrator checks reset lineage, scope, counters, finding classes, dispatched bytes and final-head evidence without treating worker proposals as approval."
   172	  - control: metadata separators
   173	    disposition: "residual: format-2 separators delimit the metadata, and the task-copy digest covers the entire front matter and body."
   174	  - control: in-process effects
   175	    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no deployment, login, administrative installation or restart."
   176	  - control: workflow and interpreter or environment inputs
   177	    disposition: "residual: trusted parents supply clean environments and the manifest-named absolute non-shim mise Python runs isolated; role-specific runtime-name screening does not establish complete executable binding."
   178	  - control: new or renamed scripts
   179	    disposition: "residual: policy stays in the existing renderer, preparation script and guard; no new wrapper, state helper, interpreter resolver or executable-link manager is introduced."
   180	  - control: "5.14 item 0: 脅威モデル"
   181	    disposition: "residual: host controls reduce accidental and injected damage; shared credentials and same-UID processes prevent a seat-isolation claim."
   182	  - control: "5.14 item 1: 書き込み境界"
   183	    disposition: "residual: retained write policy and the closed startup schema implement this task's scope; later reloads and consumption races remain outside its guarantee."
   184	  - control: "5.14 item 2: 無害化した環境を最初に"
   185	    disposition: "residual: trusted-parent clean prefixes, fixed operations and declared environment inputs remain mandatory; the legacy orchestrator PermissionRequest and complete executable binding retain their separate owner."
   186	  - control: "5.14 item 3: 信頼パスの境界検査"
   187	    disposition: "residual: canonical root and component containment checks precede startup, including aliases; executable realpath binding remains with the binding task."
   188	  - control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す"
   189	    disposition: "residual: fixed dispatch avoids candidate-selected execution, while snapshots, last-use digests and complete executable identity remain with their consuming mechanisms."
   190	  - control: "5.14 item 5: 出力と予約の同一性"
   191	    disposition: "residual: this task introduces no reservation protocol; consuming orchestrator mechanisms retain ownership of full-head outputs and inode-bound locks."
   192	  - control: "5.14 item 6: 正直な残余"
   193	    disposition: "residual: the report retains shared credentials, administrative exceptions, socket access, agmsg sourcing, races, reloads and hook-event limitations."
   194	  - control: "5.14 item 7: 検証"
   195	    disposition: "residual: retained source-class fixtures and new allowlist regressions supply final-head evidence; shared trusted-execution helper adoption remains with P1-6."
   196	  - control: "5.14 item 8: 承認はコミット済み台帳から読む"
   197	    disposition: "residual: fixed-host ledger templates and hostile-host fixtures preserve the contract; P1-14 a05 and P1-6 own actual approval consumption."
   198	  - control: "5.14 item 9: 私設キャッシュ"
   199	    disposition: "residual: private worker caches and orchestrator-cache denies remain; exact interpreter declarations, resolver consumption and deployment binding remain separately owned."
   200	  - control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない"
   201	    disposition: "residual: the Worker Playbook permits no worker escape, while shared administrative capabilities and the operator's Codex permgate deployment remain explicit residuals."
   202	  - control: canonical GitHub API host binding
   203	    disposition: "residual: both ledger templates explicitly bind github.com and mryfmo/dotfiles; contract tests establish argv binding rather than enforcement by deferred consumers."
   204	  - control: hook failure policy
   205	    disposition: "residual: supported rendered entries retain onFailure block, but background hooks, excluded events and runtime timeout behavior establish no enforcement responsibility."
   206	  - control: agmsg store driver and plugin selection
   207	    disposition: "residual: plugin-code and trusted-plugin denies reduce one route; writable store-selected sourcing remains owned by dotfiles-T133-agmsg-hardening-a01."
   208	  - control: orchestrator effect merge
   209	    disposition: "residual: only the orchestrator integrates with final-head evidence and a pinned merge; shared credentials still permit API routes outside the native prefix denials."
   210	  - control: orchestrator effect update-branch
   211	    disposition: "residual: an update moves the head and requires fresh CI, feedback, local review, audit and security evidence before integration."
   212	  - control: orchestrator effect forced worker removal
   213	    disposition: "residual: none is planned; existing dirty-worktree protections remain and any operator-authorized discarded state must be recorded."
   214	premises:
   215	  - claim: >-
   216	      INV-6 carries three a03 amendments; plan 006 S2 requires design by another authoring context. This review-profile context supplies a04, reset_of a03, rather than another a03 amendment. Read-only rechecks on 2026-10-20 confirmed worker-e remains at c0f50fa1383416240ad28959dbc4635afa777175 on tools/worker-write-boundary-a01. Keep PR #431 and the uncommitted a03 implementation/test draft. The canonical a03 text and retained worker task copy both hash to 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b.
   217	    sources:
   218	      - .orchestration/plans/006-regime-v3-execution.md
   219	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
   220	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
   221	    executed_commands:
   222	      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" rev-parse HEAD', output: 'c0f50fa1383416240ad28959dbc4635afa777175'}
   223	      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" symbolic-ref --short HEAD', output: 'tools/worker-write-boundary-a01'}
   224	      - {command: 'shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md', output: 'both files: 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b'}
   225	  - claim: >-
   226	      The blocked PONG reports probe exit 0, test exit 1, zero worker correction rounds and zero independent pre-push reviews. Its green-new.log is a failing uncommitted draft: 15 tests, 45 failures, including undeclared runtime names, noncanonical TMPDIR and unreconciled fake-update hooks; it is not a RESULT or final green evidence. Retain it without relabeling.
   227	    sources:
   228	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
   229	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log
   230	  - claim: >-
   231	      runtime-contract-probe.json supplies the exact name lists below. Read-only repetition at 2026-10-20T14:57:54Z produced the same names, exit statuses and spawn digest, without a live worker or private settings. The manifest currently lacks the non-shim interpreter declaration; a04 must add it within its existing launcher policy, not discover it through PATH.
   232	    sources: [.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json]
   233	    repeated_probe:
   234	      supplied_environment_names: [HOME, LANG, PATH, TERM]
   235	      child_code: 'import os,json,pathlib,platform,pwd,tempfile,subprocess;print(json.dumps(sorted(os.environ)))'
   236	      interpreters:
   237	        - command: '/usr/bin/python3 -I -c <child_code>'
   238	          exit: 0
   239	          observed_names: [CPATH, HOME, LANG, LIBRARY_PATH, MANPATH, PATH, SDKROOT, TERM, __CF_USER_TEXT_ENCODING]
   240	          unlisted_names: [CPATH, LIBRARY_PATH, MANPATH, SDKROOT, __CF_USER_TEXT_ENCODING]
   241	          stderr: "python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead"
   242	        - command: '"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" -I -c <child_code>'
   243	          exit: 0
   244	          observed_names: [HOME, LANG, PATH, TERM, __CF_USER_TEXT_ENCODING]
   245	          unlisted_names: [__CF_USER_TEXT_ENCODING]
   246	          stderr: ""
   247	      upstream_spawn_sha256: 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731
   248	      upstream_spawn_line: 527
   249	      upstream_spawn_text: "  echo 'export AGMSG_SPAWNED=1'"
   250	      schema_has_AGMSG_SPAWNED: false
   251	      live_worker: false
   252	      private_settings_read: false
   253	  - claim: >-
   254	      The complete c0f50fa1 security review found AWS credential-chain selectors, a foreign-repository main-local inventory gap and object-form plugin command mappings. The local review found the incorrect enterprise skills root, lower-scope sandbox extensions, missing privileged parent creation and post-Herdr settings drift. The local chain stopped before a task-level audit; none exists for c0f50fa1. Repeated renderings in the local report are four findings, not additional independent findings.
   255	    sources:
   256	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
   257	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
   258	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
   259	  - claim: >-
   260	      D-024-26 retains the write boundary and transfers executable binding. D-024-29 freezes design 5.14; D-024-30 applies it by reference. The 2026-10-20 residual-list entry in this text records the allowlist generalisation without reopening the frozen items.
   261	    sources:
   262	      - .orchestration/decisions.tsv
   263	      - $HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md
   264	  - claim: >-
   265	      The inherited read-only version observation is Claude Code 2.1.300. Documentation enumerations fetched at 2026-10-19T20:41:53Z were: settings scopes User, Shared project, Project local, Managed; precedence Managed settings, Command line, Project local settings, Shared project settings, User settings; MCP scopes Local, Project, User; hook types command, http, mcp_tool, prompt, agent; plugin origins @<marketplace>, @inline, @skills-dir, @synced; plugin enablement sources --add-dir, user, project, local, flag, managed; skills roots Enterprise, Personal, Project, Nested, Additional directory, Plugin; account-synced roots remain undeclared. Recheck the installed version and loader before changing implementation.
   266	    fetched_at: "2026-10-19T20:41:53Z"
   267	    sources:
   268	      - https://code.claude.com/docs/en/settings
   269	      - https://code.claude.com/docs/en/hooks
   270	      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
   271	      - https://code.claude.com/docs/en/plugins/loading
   272	      - https://code.claude.com/docs/en/skills
   273	  - claim: >-
   274	      C-87 inherited observation: the orchestrator observed the documented ["Where skills live" table](https://code.claude.com/docs/en/skills) at 2026-10-20T04:47:57Z and the read-only loader probe at 2026-10-20T04:50Z. The Enterprise row says "`.claude/skills/<skill-name>/SKILL.md` in the managed settings directory", with Linux example `/etc/claude-code/.claude/skills/<skill-name>/`. The pinned 2.1.300 loader, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3, contains `/.claude/skills/` (11 occurrences), `.claude/skills/` (8), `/etc/claude-code` (6) and `/Library/Application Support/ClaudeCode` (3); the historical supplied probe excerpt is `LC_ALL=C /usr/bin/grep -a -o -E '…(\.claude/skills|/skills"|skills/)…' <loader> | sort | uniq -c`. These observations bind the enterprise inventory and fixture to `<managed-root>/.claude/skills`.
   275	    sources: ["https://code.claude.com/docs/en/skills", ".orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md"]
   276	  - claim: "Worker a010 blocked before any edit (PONG 2694, 2026-10-20T04:00:43Z): the loader persists numStartups at start and hasCompletedOnboarding at onboarding; the orchestrator reproduced the installed-loader probe below, not a live worker start."
   277	    sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md]
   278	    probe: {executed_by: review-profile-author, executed_at: "2026-10-20T14:57:54Z", loader: "$HOME/.local/share/mise/installs/npm-anthropic-ai-claude-code/2.1.300/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe", format_observed: Mach-O arm64}
   279	    executed_commands:
   280	      - {command: 'shasum -a 256 <loader>', output: '475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3  <loader>'}
   281	      - {command: '<loader> --version', output: '2.1.300 (Claude Code)'}
   282	      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o numStartups <loader>', output: '12'}
   283	      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o hasCompletedOnboarding <loader>', output: '15'}
   284	    quoted_string_probes: [{command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"numStartups"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasCompletedOnboarding"'' <loader>', output: '0'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasTrustDialogAccepted"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"oauthAccount"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"mcpServers"'' <loader>', output: '29'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"enabledMcpjsonServers"'' <loader>', output: '5'}]
   285	  - claim: >-
   286	      The single source inventory is S01-S23 below plus executable environment-file contents admitted by the launch-input schema. Each parameter denotes every actual matching file, inspected independently before merging. User means the dedicated configuration directory; managed-root is the platform directory containing managed-settings.json. S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json; S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery; S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration; S12 each skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json; S16 every default hooks/hooks.json and explicitly referenced plugin hook file; S17 every admitted marketplace-root/.claude-plugin/marketplace.json; S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file; S22 every applicable subagent Markdown file; S23 every default or referenced plugin LSP file. Non-file managed delivery and caller-selected inputs must fit the same closed schema and read set or cause a named refusal.
   287	    sources:
   288	      - https://code.claude.com/docs/en/settings
   289	      - https://code.claude.com/docs/en/managed-settings
   290	      - https://code.claude.com/docs/en/server-managed-settings
   291	      - https://code.claude.com/docs/en/plugins/manifest-reference
   292	      - https://code.claude.com/docs/en/skills
   293	---
   294	
   295	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a04 — plan 024 P1-15; worker startup screen; seat a010
   296	
   297	## Goal and reset
   298	
   299	[memory:decision] Reset a03 under INV-6 and plan 006 S2 through this separate review-profile authoring context. Worker a010 is Codex, security profile, in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`; this task changes Claude's boundary and preserves Codex policy. Continue `tools/worker-write-boundary-a01` and PR #431 from `c0f50fa1383416240ad28959dbc4635afa777175`, keeping the uncommitted a03 draft and all predecessor evidence; open no second PR.
   300	
   301	Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Retain every a03 item and fix, with only the runtime/interpreter decision specified here.
   302	
   303	[memory:failure] a01 and a02 each spent two worker rounds; a03's blocked PONG reports zero worker correction rounds and zero independent pre-push reviews, while its amendment history remains counted. This reset supplies a04 at most two worker correction rounds in total, including pre-push corrections, and at most one independent pre-push review; it erases no predecessor counters or findings.
   304	
   305	The retained draft is not approved, and its `raw/green-new.log` is explicitly failing. The c0f50fa1 local chain stopped before its task-level audit. Obtain new final-head audit and security evidence; do not describe either as inherited.
   306	
   307	## History
   308	
   309	a01 and a02 each exhausted their two worker rounds, and a03 reset the lineage to a closed startup schema while continuing PR #431. Its amendments bound executable environment-file contents, regenerated S11 with screened identity and empty shared project state, and corrected the enterprise skills inventory; those controls and their finding history remain. The worker blocked on shim/platform-added runtime names and upstream `AGMSG_SPAWNED=1`, preserving its uncommitted draft and failing evidence. INV-6's three counted a03 amendments trigger plan 006 S2, so another context authors a04 to resolve only that runtime-name/interpreter contract instead of extending a03.
   310	
   311	## Design and finding history
   312	
   313	Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 by reference, including its residual list. D-024-29 keeps items 0-10 frozen; D-024-30 narrows C-88 to exact contract sentences asserted by tests.
   314	
   315	Item 1 applies to dedicated worker settings, static input-derived write protection and refusal before startup.
   316	Item 2 applies to trusted-parent execution, clean environments and fixed command selection.
   317	Item 3 applies to canonical anchor, worktree and component identities before consumption.
   318	Item 8 applies to committed approval authority through explicitly host-bound repository API calls.
   319	Item 9 applies to private caches and the trusted parent's interpreter/cache inputs.
   320	
   321	**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a04:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.
   322	
   323	Read the full a02 and a03 acceptance records, a03 task, blocked PONG and both runtime evidence files, and both c0f50fa1 reviews named in `premises:`. Retain the following history and finding classes in the a04 report and acceptance lineage:
   324	
   325	| Finding | Class | Required treatment |
   326	| --- | --- | --- |
   327	| `text-security:2ae9e2c:1` | input-inventory | Project `.mcp.json` remains independently screened. |
   328	| `text-security:ebbb71b:1` | input-inventory | Skills-directory plugins remain inventoried even when disabled. |
   329	| `text-security:ebbb71b:2` | input-inventory | Dedicated global state regenerates `mcpServers: {}` and `projects: {}`; native project entries are discarded. |
   330	| `text-security:ebbb71b:3` | repository-binding | Canonical main comes from the fixed repository API. |
   331	| `text-security:b2a186e:1` | input-inventory | Inspect handler type before command; non-command types refuse. |
   332	| `text-security:b2a186e:2` | repository-binding | Both ledger calls bind `--hostname github.com`. |
   333	| `text-security:ac9ce14:0` | correct | Historical text approval only; it does not approve a04. |
   334	| a02 independent pre-push review | input-inventory | Retain fixes for `env.HOME` guard selection and fenced dynamic commands. |
   335	| `local:79ea98a:1` | tool-environment | Retain manifest-generated `--advisor fable` acceptance. |
   336	| `local:79ea98a:2` | tool-environment | Retain absolute tool paths and attachment identity environment. |
   337	| `local:79ea98a:3-4` | partial-fix | Retain custom-hook preservation and legacy PreToolUse migration. |
   338	| `security:c0f50fa:1` | input-inventory | Refuse undeclared credential-chain/provider selectors. |
   339	| `security:c0f50fa:2` | input-inventory | Refuse worker starts for repositories other than the validated anchor. |
   340	| `security:c0f50fa:3` | input-inventory | Refuse object and inline plugin/command components. |
   341	| `local:c0f50fa:1` | tool-environment | Inventory enterprise skills under the actual managed root. |
   342	| `local:c0f50fa:2` | tool-environment | Reject lower-scope sandbox extensions before array merging. |
   343	| `local:c0f50fa:3-4` | partial-fix | Fix printed parent creation and post-installer reconciliation here. |
   344	| `text-security:f7af699:1` | input-inventory | Admit executable environment-file contents only when absent, empty or launcher-generated for this start. |
   345	| `worker:5067ed0:1`, `text-security:efa211d:1` | input-inventory | Regenerate S11 at every start with `projects: {}` and screened identity; discard native persisted state, including every project's state, and use the launcher's existing spawn-readiness trust-dialog acceptance. |
   346	| `text-security:be969e3:1` | input-inventory | Inventory enterprise skills and plant both Markdown and bundled plugin fixtures under `<managed-root>/.claude/skills`, following the C-87 documented table and pinned-loader probe. |
   347	
   348	S1 first triggered on the three source omissions in 2ae9e2c/ebbb71b. The re-plan enumerated S01-S23, but subsequent findings still exploited open field/value acceptance; the c0f50fa1 security findings bring that post-re-plan family to its sixth finding. This reset changes the approach rather than adding three more denylist entries.
   349	
   350	Preserve the advisory-owner history and owner `dotfiles-T133-worker-write-boundary-followup-a01` exactly as history. The two c0f50fa1 P2 fixes are retained from a03 by this text; the orchestrator reconciles their owner rows and updates dependent task references. The worker edits no canonical acceptance or owner task.
   351	
   352	Retain D-024-26's transferred binding findings, including `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. Do not relabel them as fixed.
   353	
   354	## Closed startup schema
   355	
   356	Declare this schema in `home/dot_agents/agent-config.yaml` and expose it through the existing renderer/preparation code. Candidate files, Git objects and installed upstream schemas never define their own acceptance policy. Add no new helper, generated output file or dependency.
   357	
   358	The schema below is exhaustive for data forwarded to the loader. Objects reject unknown keys at every level, including nested objects and records that would otherwise be preserved; S11 fields designated for discard are not screened or preserved. Reject duplicate JSON keys, wrong types, Boolean/integer substitutions, unreadable inputs and unsupported forms. Missing optional fields may pass; a present field must match its declared source-specific form.
   359	
   360	### Settings and values
   361	
   362	The only settings keys are `permissions`, `sandbox`, `hooks`, `env`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `enabledPlugins`, `syncClaudeAiPlugins`, `syncClaudeAiSkills`, `extraKnownMarketplaces` and `disableSkillShellExecution`.
   363	
   364	| Node | Accepted shape and values |
   365	| --- | --- |
   366	| `permissions` | Only `defaultMode`, `deny`, `additionalDirectories`; `defaultMode` is `auto` where applicable; `additionalDirectories` is `[]`; `deny` is a renderer-declared worker/native-denial fragment for that source. No caller-added allow/ask rule or alternate permission mode. |
   367	| `sandbox` | Only the keys emitted by the worker or administrative renderer: `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands`, `excludedCommands`, `filesystem`, `network`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `allowAppleEvents`. |
   368	| `sandbox.filesystem` | Only `allowWrite`, `disabled`; exact source-specific canonical values. Worker write grants are the four declared agmsg stores; ordinary worktree/cache writes remain provided by the worktree boundary. |
   369	| `sandbox.network` | Only `allowedDomains`, `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`; exact source-specific canonical values. |
   370	| Sandbox lists and Booleans | Every present leaf/list equals the canonical worker fragment in S01-S04 or administrative fragment in S05-S07. Worker exclusions are empty; additional write roots/sockets are refused. Only administrative sources may contain the exact shared three exclusions and single Herdr socket. |
   371	| `hooks` | Only source/event/matcher/operation combinations generated by the trusted renderer or delivery constructor. Groups have only `matcher`, `hooks`; handlers have only renderer-declared `type`, `command`, `timeout`, `async`, `statusMessage`, `onFailure`, with exact canonical values. |
   372	| Handler type | Only the string `command`; validate it before reading `command`. HTTP, MCP-tool, prompt, agent, unknown, missing, null and non-string types refuse. |
   373	| MCP approval fields | `enableAllProjectMcpServers: false`; `enabledMcpjsonServers: []`; `disabledMcpjsonServers: []` when present. Approval state never exempts a server definition. |
   374	| Plugin fields | `enabledPlugins` maps only manifest-known or inventoried plugin identities to `false`; both sync fields are `false`; `extraKnownMarketplaces` is `{}`. |
   375	| Skill execution | `disableSkillShellExecution`, when present, is `true`. |
   376	| `env` | Only the four exact name/value pairs in the next subsection; arbitrary strings, maps and provider credentials are not preserved. |
   377	
   378	Absent or empty settings objects pass where the source permits them. Administrative drop-ins/cache may contain canonical partial objects; partial means omitted declared fields, never new fields or alternate values. Validate each list before merging so an empty generated worker list cannot conceal a broader lower-scope array.
   379	
   380	There is no canonical worker setting for helpers, status-line commands, wrappers, alternate sandbox executables, policy helpers or authentication refresh/export commands. Their keys refuse as undeclared, including misplaced forms. The orchestrator managed PermissionRequest exception is not a worker-start exception.
   381	
   382	The old instruction to preserve unrelated non-executable state now applies only to fields admitted by this schema. Unknown settings refuse without deletion or normalization; S11 alone discards pre-existing fields outside its declared structures and carried identity, without screening or forwarding them.
   383	
   384	### Environment and launch arguments
   385	
   386	Settings `env` admits exactly `GH_TELEMETRY="false"`, `DO_NOT_TRACK="1"`, `CHECKPOINT_DISABLE="1"` and `AWS_EC2_METADATA_DISABLED="true"`, as declared by the manifest. The last name is the sole declared `AWS_*` exception and cannot select credentials or a provider.
   387	
   388	The launch-input schema classifies names by source: existing parent/runtime declarations, `regime-declared`, and `platform-injected`. The latter two classes below are closed enumerations, not prefixes. They do not extend settings `env`, configuration-file keys or CLI arguments.
   389	
   390	The launcher and its startup/preflight Python children use only the manifest-named absolute mise-installed non-shim interpreter, observed here as `<validated-home>/.local/share/mise/installs/python/3.15.0/bin/python3.15`. Add that narrow declaration to the existing manifest-owned launcher policy and consume it through the existing renderer; never route through `/usr/bin/python3`, a mise shim, PATH lookup or an interpreter-discovery fallback. Cover startup bootstrap/home lookup as well as preparation. This selects the interpreter for this boundary without returning the deferred complete binding work to scope.
   391	
   392	The launch-input schema admits only these names, with source-specific values supplied or checked by the trusted parent:
   393	
   394	| Names | Value authority |
   395	| --- | --- |
   396	| `HOME`, `PATH`, `LANG`, `TERM` | Validated passwd home; prescribed system-only child PATH; `C.UTF-8`; declared terminal value. Hook children retain `TERM=dumb`. |
   397	| `TMPDIR` | Canonical trusted temporary directory supplied by the parent, not a candidate configuration root. |
   398	| `CLAUDE_CONFIG_DIR` | Exactly the dedicated worker directory under the validated home. |
   399	| `CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` | Parent-bound canonical project identity and runtime shell file; `CLAUDE_ENV_FILE` additionally requires the executable-content control below. |
   400	| `UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR` | Exactly `<canonical-worktree>/.uv-cache` and its `python` child. |
   401	| `regime-declared`: `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE`, `AGMSG_AGENT_PID` | Retain a03's exact authorities: `0`, validated launcher store selection, declared monitor value and numeric runtime process identifier; unset default-store selection remains supported. |
   402	| `regime-declared`: `AGMSG_SPAWNED` | Exactly the string `1`, set by upstream `spawn.sh` on the launch surface before the worker CLI; require it on spawn-launched roles and do not synthesize it for unrelated child roles. |
   403	| `platform-injected`: `__CF_USER_TEXT_ENCODING` | Darwin only; present or absent allowed. A present string must full-match `0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+`. The regime validates the shape and otherwise never reads or uses it. Linux presence refuses. |
   404	| `HERDR_ENV`, `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_AGENTS_LAYOUT`, `HERDR_SOCKET_PATH` | Validated control-plane identity, `managed` layout and canonical configured socket; these grant no worker sandbox exception. |
   405	| `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID` | Parent/runtime session identifier and numeric process identifiers where required by canonical attachment/delivery. |
   406	| `CLICOLOR_FORCE`, `FORCE_COLOR` | Launcher-written `1` only where the launch route uses them. |
   407	| `GH_TELEMETRY`, `DO_NOT_TRACK`, `CHECKPOINT_DISABLE`, `AWS_EC2_METADATA_DISABLED` | The four fixed values above. |
   408	| `CHEZMOI_SOURCE_DIR`, `CHEZMOI_HOME_DIR` | Preparation-only trusted source/home bindings; not caller-selected worker configuration or executable roots. |
   409	
   410	The read-only amendment-1 probe of the [documented environment variables](https://code.claude.com/docs/en/env-vars) identifies `CLAUDE_ENV_FILE` as the only name admitted above that selects a file whose contents execute: Claude runs its shell contents before Bash commands. No other admitted name has that documented role; `CLAUDE_CODE_SHELL` and `CLAUDE_CODE_SHELL_PREFIX` remain undeclared. Include the named file's contents in the preflight read set alongside S01-S23.
   411	
   412	For every admitted executable-content file variable, preflight accepts its named file only when absent, empty, or byte-identical to canonical contents generated by the launcher for this start. Inspect without sourcing or executing it; unreadable/nonregular files and any other contents refuse before trust, migration, regeneration, hooks or worker commands with `worker startup refused: <file>: <variable>: noncanonical executable environment file contents`. Preserve refused bytes; never overwrite a planted file to make it pass. After all preflight checks pass, the launcher itself writes the canonical runtime-file contents, records SHA256 bound to the variable, canonical file and this start in existing startup state/evidence, and verifies those bytes before forwarding. Candidate-supplied or prior-start digests cannot authorize contents. Reuse the existing runtime file and startup state; add no sidecar, helper or generated configuration output. Later replacement races and reloads retain their existing residual owners.
   413	
   414	Validate proposed worker configuration inputs before forwarding them. A clean child environment contains only the names declared for that child role; do not inherit the caller environment wholesale. Unknown proposed environment names refuse rather than becoming an unchecked pass-through. Existing profile/control-plane variables used to select a worker are consumed through their existing manifest-owned interfaces, not forwarded as arbitrary worker settings.
   415	
   416	Every `CLAUDE_CODE_USE_*`, `AWS_*`, `ANTHROPIC_*`, `*_API_KEY`, `*_TOKEN` and `*_PROFILE` name refuses unless explicitly declared above with its exact allowed value. In particular refuse `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE` in settings and launch inputs before any credential lookup or helper execution. Add no AWS configuration parser.
   417	
   418	No shell/interpreter startup or loader override is declared: `BASH_ENV`, `ENV`, `NODE_OPTIONS`, `NODE_PATH`, `PYTHON*`, `LD_*`, `DYLD_*`, shell wrappers and alternate configuration/cache roots refuse as worker inputs. Do not print their values.
   419	
   420	Preserve the manifest-generated Claude argument interface: only `--model`, `--effort`, `--advisor` with their declared profile values, including `--advisor fable`. Caller-added settings, MCP, plugin, agent and additional-directory arguments refuse. Keep existing Codex arguments and network/shared-Git policy unchanged.
   421	
   422	A clean-parent probe runs through the interpreter named by the rendered manifest, imports the same modules as the predecessor probe, and asserts `CPATH`, `LIBRARY_PATH`, `MANPATH` and `SDKROOT` are absent. They remain undeclared and refuse if encountered; do not delete them to conceal an unexpected injection. Test the observed child environment as well as the parent's proposed names, with child-role-specific declarations.
   423	
   424	Any other new name, source, required state field or interpreter mismatch still blocks and re-tasks. Send a blocked PONG naming the boundary, exact command and status, with probe JSON containing the supplied/observed name lists, undeclared names and interpreter identity under the a04 evidence directory. Preserve the predecessor JSON unchanged. No wildcard, prefix-wide acceptance, candidate-learned schema, suppression or default-as-authorization is allowed; print no environment values.
   425	
   426	### Sources, roots and component forms
   427	
   428	The sole repository anchor is the manifest declaration resolving to `$HOME/Workspace/dotfiles`. Bind its identity to the validated passwd home and actual main checkout, resolving symlinks and filesystem case aliases. Worker roots must be registered linked worktrees beneath that anchor's declared `.claude/worktrees/` root with the same Git common directory.
   429	
   430	Every worker launch route, for either worker kind, refuses another repository before worktree creation, identity registration, hook writes, workspace trust or spawn. The refusal names this task: `worker startup refused: dotfiles-T133-worker-write-boundary-a04: unsupported repository root`. Do not fix the foreign-root finding by inspecting the fixed anchor while launching elsewhere.
   431	
   432	Admitted configuration roots are the dedicated worker directory, the validated anchor/worktree `.claude` directories, applicable nested worktree and additional-directory `.claude` directories, the platform managed root and contained plugin roots discovered through the declared registry. Inherited MCP files are the independently enumerated ancestor read set. No account-synced, inline, seed, alternate cache or caller-selected root is admitted; caller-added additional-directory arguments remain refused.
   433	
   434	The admitted skills roots are exactly Enterprise `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), Personal `<absolute-home>/.claude-worker/skills` under the dedicated configuration directory, Project `<project>/.claude/skills`, Nested `<subdir>/.claude/skills`, Additional directory `<add-dir>/.claude/skills` under an applicable `--add-dir` directory, and Plugin `<plugin>/skills`. Inspect both `<skills-root>/<name>/SKILL.md` and bundled `<skills-root>/<name>/.claude-plugin/plugin.json`. Managed command/agent locations likewise start at the actual managed root. Resolve every selected path and refuse containment escapes, unsupported aliases, missing references or unreadable files.
   435	
   436	| Source form | Closed acceptance |
   437	| --- | --- |
   438	| S08-S10, S18-S19 | Objects containing only absent or empty `mcpServers`/`managedMcpServers` maps. No server, including remote-only definitions, is canonical here. |
   439	| S11 global state | At every start, after all preflight checks pass and before any loader/worker command, write the existing `CLAUDE_CONFIG_DIR/.claude.json` from scratch: `mcpServers: {}`, `projects: {}` and `hasCompletedOnboarding: true`, plus screened identity fields below. The generated file carries no per-project inventory or pre-generated workspace trust. Never merge the previous file into this output. |
   440	| S11 pre-existing structures and identity | The existing file must be a JSON object. Missing optional retained fields pass and generated fields are written anew. Present top-level `mcpServers` must be `{}`. Carry optional `oauthAccount` only as an object with string-only members from this documented fixed set: `accountUuid`, `emailAddress`, `organizationUuid`, `displayName`, `fullName`, `organizationRole`, `workspaceRole`; declare the same set in the manifest and fixtures. Carry optional `userID` only as a string matching `^[0-9a-f]{64}$`, the installed loader's hex form. Undeclared identity members, non-string `oauthAccount` members, invalid identity values and a nonempty or malformed top-level MCP map refuse with `worker startup refused: <state-file>: <offending-key>: <named reason>` before any command or mutation, preserving refused bytes. Nonempty top-level servers use the exact reason `noncanonical global state` as tamper evidence. |
   441	| S12/S15 plugin descriptor | Only `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and the component keys `hooks`, `mcpServers`, `lspServers`, `commands`, `agents`, `skills`. Descriptive fields are strings, keywords are strings, and author has only string `name`, `email`, `url`. |
   442	| Component references | Each present component is one scalar string referencing a regular file within its admitted root. The screening reads that file under its source schema before accepting it. Arrays, objects, inline content, URLs and explicit directory references refuse. Default component directories are independently expanded into inspected files. |
   443	| S13 installed registry | Only `version: 2` and `plugins`; plugin IDs map to record lists with only `scope`, `installPath`, `version`, `installedAt`, `lastUpdated`, `gitCommitSha`, `projectPath`. Scope is user/project/local; paths are contained and project-bound; descriptive fields are strings and a present commit is 40 hex. Every referenced descriptor is read and every discovered ID is disabled. |
   444	| S14 marketplace registry | Only `{}`; no refresh source or executable header helper is canonical. |
   445	| S16 hook file | Only an absent/empty `hooks` object; plugin-owned handlers have no canonical worker operation. |
   446	| S17 marketplace descriptor | Only descriptive `name`, `owner`, `metadata`, `plugins`; owner has string name/email, metadata has string description/version, and plugins is absent or `[]`. Additional plugin selections refuse. |
   447	| S20-S22 Markdown | Plain text with the existing restricted frontmatter grammar: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model. Booleans are Boolean, model/tool selections are manifest-declared values, and unknown/nested executable forms refuse. Dynamic shell expansion, including fenced forms, refuses everywhere. |
   448	| S23 LSP | Only `{}`; command/args definitions are not canonical. |
   449	| Non-file managed inputs | Enumerated canonical administrative data only; otherwise refuse with the managed source name before executing any helper or starting Claude. |
   450	
   451	For S11, every other pre-existing top-level field, including the entire `projects` value and all its contents, `numStartups`, prior onboarding state, tips/changelog caches, project `history`, `allowedTools` and cost counters, is neither screened nor preserved; only syntax/duplicate-key/readability checks apply to the whole input. Discarded objects and arrays are never recursively screened or forwarded. Generate onboarding anew and `projects: {}`, preserve only screened identity values, and reuse the existing atomic writer after the complete preflight; the loader regenerates native state. The anchor's workspace trust is established by the launcher's existing acceptance of the workspace-trust dialog during spawn's readiness wait (`herdr-agents --add-worker` for a Claude worker, documented in the SKILL's 'Regime activation and progress' section). All Claude workers share `CLAUDE_CONFIG_DIR` at `$HOME/.claude-worker`; discarding the prior `projects` value lets sequential sibling starts succeed. A loader requiring another preserved field blocks and retasks rather than widening silently.
   452	
   453	These restrictions also apply to disabled plugins and shadowed sources. Do not recursively ignore an unknown object because it lacks a familiar executable key. A plugin `commands` mapping containing `{"source": ...}` or inline `content` refuses at the selecting file/key.
   454	
   455	## Implementation and retained controls
   456	
   457	1. Keep one preflight over S01-S23, admitted executable environment-file contents and the closed schema. Every Claude route calls it before workspace trust, migration, normalization, regeneration or execution. Enumerate through the filesystem, including ignored/untracked inputs; neither Git tracking nor a nearer definition removes a source. Inspect implicit and selected components separately without executing helpers, installing packages, fetching plugins or starting servers.
   458	
   459	2. Refusals identify the actual source and key/class without printing payloads, environment values, URLs with credentials or authentication material. Preserve the handler message `worker startup refused: <source-file>: hooks.<event>[<group-index>].hooks[<handler-index>]: noncanonical hook handler`, with zero-based indices. Other refusals use `worker startup refused: <source>: <key>: <named reason>`. Unknown settings, selectors, roots, components and source forms each receive a named reason.
   460	
   461	3. Retain exact recognized legacy-delivery classification, including canonical project binding. First screen every source; only after complete success migrate recognized owned entries, validate the prepared result under the same schema, then write. Unknown content outside S11's discard partition refuses without changing any pre-existing bytes; successful S11 regeneration intentionally replaces discarded state only after every source passes. Never rewrite tracked settings or create a local file merely for migration. Keep repeated preparation and delivery-tool-unavailable behavior.
   462	
   463	4. Retain dedicated `CLAUDE_CONFIG_DIR`, both private cache variables on every actual worker route, `AGMSG_RESOLVE_PROJECT=0`, validated `AGMSG_STORAGE_PATH`, canonical attachment identity and `onFailure: "block"` where supported. A writable `run/proj.<pid>.project` cannot replace the explicit project identity. Preserve the a02 absolute Herdr/jq/Node/npm/Codex calls and attachment environment; fixed PATH must not regress attachment or default seating.
   464	
   465	5. Keep static `trusted_paths` derived from trusted executable inputs, not Git trees/indexes. Preserve anchored source/control paths, tracked/main-local settings, `.orchestration`, both `.agents/worklog/**` and `.agents/worklog/uv-cache/**`, worktree `.claude` directory/descendant targets and `.mcp.json`. Ordinary worktree source and private cache writes remain available.
   466	
   467	6. Retain explicit protection of `<absolute-home>/.agents/agent-config.yaml`, model profiles, permgate policy, skill scripts/SKILL files, agmsg plugin code and `db/trusted-plugins`, `<absolute-home>/.claude/**`, `<absolute-home>/.claude-worker/**`, installed guard, local wrappers/application code, configuration/state/tool installations and shared uv caches. Keep directory and descendant user-site protection for `.pth`, `usercustomize.py` and `sitecustomize.py` on both platforms. Add no blanket `<absolute-home>/.agents/**` or `<absolute-home>/.local/**` deny: agmsg `db`, `teams`, `run`, `ext-tools` stay writable except `db/trusted-plugins`.
   468	
   469	7. Retain separate orchestrator, worker and administrative renders. Worker policy keeps `defaultMode: auto`, sandbox startup failure, disabled unsandboxed requests, empty user exclusions, restricted writes, no user Herdr socket, explicit MCP auto-approval disables, account sync off and false plugin entries including discovered `@skills-dir` identities. Empty maps alone do not disable plugins or replace screening.
   470	
   471	8. Administrative settings retain enabled sandboxing, `failIfUnavailable: true`, disabled unsandboxed requests, filesystem enforcement, disabled weaker isolation/Apple Events/all-socket/local-binding switches, exactly the Herdr socket, and exactly these ordered exclusions: `agmsg-dispatch *`, `herdr-agents *`, `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These shared capabilities remain available to every Claude seat and authorize no worker escape. Lower-scope canonical validation rejects extra exclusions, writes or sockets before array merging.
   472	
   473	9. Keep the orchestrator managed PermissionRequest command's existing literal bytes unchanged, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.
   474	
   475	10. Apply design 5.14 by reference for trusted-parent execution, Python isolation and Git inspection. Consume the manifest-named non-shim interpreter specified above on every launcher startup/preflight Python route; add no resolver, helper, private executable directory, PATH fallback or broader version-pin work. Do not execute arbitrary task-body shell strings as probes.
   476	
   477	11. Preserve guard routing, fixed payload paths, argument boundaries, stdin and child status. Canonical worker/sibling/unrelated/missing launch identities execute no orchestrator project payload. Only fixed installed worker-delivery operations run for workers. Formatter/map operations also reject worker/outside-anchor tool inputs. Keep tracked settings portable and all existing event/validator markers.
   478	
   479	12. Preserve managed SessionStart/PostToolUse/PreToolUse migration, custom-hook ordering, mixed entries, escaped-tilde distinctions, stale replacement and idempotence. For `make update`, reconcile the managed Claude settings after `scripts/update-agent-assets.sh` runs Herdr's installer, using the allowed Makefile/merge/renderer surfaces. Do not edit the updater script or import its unguarded hook as canonical. Verify one effective guarded hook and no managed-settings drift after repeated fake updates.
   480	
   481	13. `install-managed-settings` still stages `<absolute-home>/.claude/managed-settings.rendered.json` nonprivileged. Print a quoted privileged `mkdir -p` for the detected administrative parent before the existing quoted `sudo install -m 0644` command. Cover both platform destinations and homes containing spaces. Execute neither privileged command; do not install, log in or restart.
   482	
   483	14. Keep all existing validator checks, exact three-entry exclusion fixtures on both platforms, legacy PermissionRequest validity, duplicate-hook checks, ordering/timeouts, freshness, portability and secret/home-path scanning. Add no bound-PermissionRequest mode. `.gitignore` retains `.uv-cache/` as this task's only addition.
   484	
   485	15. Worker Playbook step 4 retains this exact test-asserted sentence:
   486	
   487	> Complete every worker command, including gh, git push and authenticated git fetch, inside the sandbox and allowlist without forbidden actions or escalation; anything that cannot complete there is `AGMSG-PONG v1 status=blocked` naming the exact command and boundary.
   488	
   489	The entire Worker Playbook, including steps 2, 5 and 11, authorizes no exception. Evidence-sync writes/masking, CompactionDB consolidation and agmsg-dispatch control-plane exemptions remain orchestrator-only. Workers write required relative evidence in their own worktree; the orchestrator copies it before acceptance. Preserve merged documentation changes and run the complete documentation module.
   490	
   491	## Regression fixtures
   492	
   493	Write the new tests before implementation. Use the existing temporary-HOME, managed-root, linked-worktree and fake-launcher builders. Tests execute no payload, credential helper, HTTP endpoint, server, plugin, subagent or live worker.
   494	
   495	Each refusal fixture asserts the source/key or named root message, unchanged existing bytes, no migration/regeneration, no trust acceptance, no spawn and absent execution/request markers. Positive absent/canonical controls and repeated starts remain covered.
   496	
   497	| Selector | Required coverage |
   498	| --- | --- |
   499	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees` | Red on c0f50fa1, green after: sequentially start registered linked-worktree workers A then B on one shared `CLAUDE_CONFIG_DIR`. A's start leaves the regenerated file; simulated loader writes then add A's project entry with a `history` list. B's start succeeds and, before its first command, leaves exactly the regenerated file with `projects: {}` and screened identity. Replace any planted-project-key refusal and same-worktree restart fixture with this cross-worktree sequence. |
   500	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_global_state_with_screened_identity` | Red on c0f50fa1, green after: pre-existing S11 has `numStartups: 5`, `hasCompletedOnboarding: true`, `projects[anchor].history` as a list and synthetic valid `oauthAccount`/hex `userID`. A fake worker start succeeds; before its first command the file equals exactly `mcpServers: {}`, `projects: {}`, `hasCompletedOnboarding: true` plus unchanged screened identity. Cover absent state/identity; all discarded fields and project contents disappear without semantic screening. |
   501	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonempty_global_mcp_servers` | Red on c0f50fa1, green after: pre-existing S11 has nonempty top-level `mcpServers`; assert exactly `worker startup refused: <state-file>: mcpServers: noncanonical global state` before any command, preserving all bytes and absent mutation/trust/spawn/execution markers. |
   502	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member` | Red on c0f50fa1, green after: a documented `oauthAccount` member contains an object; refuse with the file and exact member key named before any command and preserve all bytes. Also cover arrays, other non-string values, undeclared identity members, invalid `userID` and malformed retained structures; canonical string-only identities pass. |
   503	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` | Red on c0f50fa1, green after: a pre-existing forwarded `CLAUDE_ENV_FILE` contains a planted command marker and exports restoring refused environment variables. Refuse with the variable and file named before any hook/worker command runs, without sourcing the file; assert unchanged bytes, no migration/regeneration/trust/spawn and absent command markers. In this one fixture retain absent, empty and same-start launcher-generated positive controls with recorded SHA256, and show that a prior-start digest cannot authorize foreign contents. |
   504	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_aws_credential_chain_selectors` | Red on c0f50fa1: the four reported selectors select a synthetic worker-owned AWS configuration containing `credential_process`; preparation refuses without running or trusting it. Test settings and launch inputs. |
   505	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root` | Red on c0f50fa1: another repository with main-local payload refuses with this task's name before any side effect, for both kinds and all worker routes; the validated anchor/control passes. |
   506	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components` | Red on c0f50fa1: object `source` mappings and inline `content`, including dynamic Markdown, refuse even with the plugin disabled. |
   507	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys` | One fixture per settings source, unknown top-level and nested keys, including a harmless-looking future key; candidate data cannot extend the allowlist. |
   508	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors` | Every prohibited name family, settings/launch placement, exact fixed-value AWS exception, unknown ordinary environment names and noncanonical declared values. |
   509	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_requires_string_component_references` | Scalar file control; object, list, directory, missing file, outside-root reference and unreadable component negatives. |
   510	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch` | Command-free HTTP separately in S01-S07 on both platforms; other documented/unknown/missing/malformed types; other hook-bearing sources; exact indexed refusal. |
   511	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_managed_skills_use_actual_managed_root` | Retained green baseline on c0f50fa1, accepted by owner PING 2751; do not manufacture a red result: using the same temporary managed-root fixture as S05/S06 for both Darwin and Linux, plant a Markdown skill at `<managed-root>/.claude/skills/<name>/SKILL.md` and a bundled plugin payload at `<managed-root>/.claude/skills/<name>/.claude-plugin/plugin.json` with hooks; metadata-only control produces explicit disable. |
   512	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_project_sandbox_extensions_are_refused_before_launch` | Red on c0f50fa1: `excludedCommands: ["*"]`, `filesystem.allowWrite: ["/"]`, extra sockets and nested unknowns in project/local scopes; canonical administrative controls remain accepted. |
   513	| `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_creates_managed_parent_in_printed_commands` | Red on c0f50fa1: missing parent, both platforms, quoting, mkdir-before-install, staged JSON and absent executed-sudo marker. |
   514	| `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_update_reconciles_settings_after_herdr_install` | Red on c0f50fa1: fake Herdr installer re-appends its literal hook, then update reconciliation restores one guarded entry; repeated update preserves custom hooks and produces no managed drift. |
   515	
   516	The runtime-name regressions below are required within the unchanged environment and fixture-alignment budgets:
   517	
   518	| Selector | Required coverage |
   519	| --- | --- |
   520	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names` | Execute the predecessor's name-only probe through the absolute non-shim interpreter read from the rendered manifest, with only HOME/PATH/LANG/TERM supplied. Assert CPATH, LIBRARY_PATH, MANPATH and SDKROOT are absent; Darwin permits only the declared platform addition. Route fixtures prove bootstrap, home lookup and preflight use that interpreter without invoking the system shim or PATH fallback. Preserve command/status/name-only JSON. |
   521	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment` | Darwin absent and correctly shaped present controls pass; malformed shapes, wrong types, trailing content and Linux presence refuse before mutation/trust/spawn. The value never selects behavior, a path or an executable and never appears in evidence. An unrelated injected name blocks with probe JSON. |
   522	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment` | Fake upstream spawn exports exactly AGMSG_SPAWNED=1 before CLI entry; accept it only for the declared child role. Wrong values and undeclared AGMSG names refuse; all four previously declared AGMSG names retain their authority and optionality. Settings env remains limited to its four original pairs. |
   523	
   524	The five allowlist classes each have an explicit fixture: unknown key, undeclared provider selector, foreign root, object-form component and non-command handler. Parameterization may share builders but must name every subcase in validation. Do not replace the three required c0f50fa1-red regressions with tests of a new validator alone.
   525	
   526	Retain all a02 regressions: old tracked settings, alternate executable fields, inherited project MCP, dedicated global state, skills-directory plugins, per-source S01-S23 coverage, sandbox-only documentation, hostile-GH_HOST templates, private caches, native denials, migration and guarded delivery. The fixture-case source inventory equals the production source inventory; each case plants its payload in the source it claims to exercise.
   527	
   528	Retain a02's red/green evidence for `env.HOME`, fenced dynamic commands and the four 79ea98a3 fixes as historical evidence. Do not claim those tests newly fail on c0f50fa1. Update the documentation template test to read the a04 task copy. Update inherited S11 sentinel-preservation/unknown-field-refusal expectations to the discard-and-regenerate contract with `projects: {}`; retain the top-level MCP tamper refusal, and do not keep the old blanket `oauthAccount` refusal or project-entry refusals.
   529	
   530	C11: every `closed` row names one exact `tests/<path>.py::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.
   531	
   532	## Change budget
   533	
   534	Changed lines mean additions plus deletions. The starting measurement is `git diff --numstat 51ba5801 c0f50fa1`, not the obsolete a01 estimate. Preserve its complete output and account separately for base-branch changes already merged into c0f50fa1. The author repeated this immutable comparison when preparing a04.
   535	
   536	For this task's allowed paths, excluding `.orchestration/`, tests and the three regenerated Claude settings templates, that command measures:
   537	
   538	| Source | Changed lines |
   539	| --- | ---: |
   540	| `.claude/settings.json` | 96 |
   541	| `.gitignore` | 1 |
   542	| `Makefile` | 6 |
   543	| `home/dot_agents/agent-config.yaml` | 60 |
   544	| `home/dot_agents/skills/agmsg-orchestration/SKILL.md` | 10 |
   545	| `home/dot_claude-worker/modify_private_settings.json` | 437 |
   546	| `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` | 65 |
   547	| `home/dot_claude/modify_private_settings.json` | 120 |
   548	| `home/dot_local/bin/common/executable_herdr-agents` | 126 |
   549	| `scripts/generate-agent-configs.py` | 181 |
   550	| `scripts/validate-agent-assets.py` | 9 |
   551	| **Measured starting source total** | **1111** |
   552	
   553	The seven allowed test modules measure respectively 103, 15, 206, 935, 104, 310 and 95 changed lines in `allowed_files` order: **1768**. The full historical-base output additionally contains already-merged unrelated source/test rows; list them rather than charging them as new a04 work or editing them.
   554	
   555	Amendment 1's read-only sizing counts 24 lines in c0f50fa1's `present`/`read_json`/`write` analogues plus 16 estimated declaration/digest/route lines, and the 42-line non-command-handler fixture plus 18 estimated content/control lines: **40 source / 60 test**. This measured analogue-based estimate is not a measured implementation result.
   556	
   557	Amendment 2's read-only AST sizing of c0f50fa1 measures `present` 8 + `read_json` 10 + `write` 6 = 24 source analogue lines, plus 56 estimated declaration/project/identity/regeneration lines: **80 source**; the global-state fixture 20 + refusal helper 36 = 56 test analogue lines, plus 64 estimated generation/identity/restart subcases: **120 test**. These are sizing analogues reused without duplication, not measured implementation results. Amendment 3 retains the **80 source** ceiling, removes project-inventory work and replaces the restart subcases with the A-then-B shared-directory sequence: the same 56 test analogue lines plus 104 estimated generation/identity/sequential-start subcase lines give **160 test**, an additional **40 test** over amendment 2. This revised estimate is not a measured implementation result.
   558	
   559	Authorize these incremental ceilings, attributed to accepted findings. These increments are estimates pending implementation measurement, not claimed measured results:
   560	
   561	| Control/finding | Additional source | Additional tests |
   562	| --- | ---: | ---: |
   563	| Closed settings/nested-value schema and sandbox extensions; S1, `local:c0f50fa:2` | 180 | 140 |
   564	| Environment/provider allowlist and credential-chain refusal; `security:c0f50fa:1` | 70 | 100 |
   565	| Validated repository root; `security:c0f50fa:2` | 25 | 60 |
   566	| Scalar inspected-file components; `security:c0f50fa:3` | 35 | 70 |
   567	| Actual enterprise skills root; `local:c0f50fa:1`, `text-security:be969e3:1` | 10 | 40 |
   568	| Handler-class/schema consistency; `text-security:b2a186e:1` | 10 | 30 |
   569	| Printed privileged parent creation; `local:c0f50fa:3` | 10 | 25 |
   570	| Post-Herdr reconciliation; `local:c0f50fa:4` | 10 | 45 |
   571	| Existing render/docs fixture alignment with the accepted re-plan | 10 | 30 |
   572	| Executable environment-file contents and launcher-written SHA256; `text-security:f7af699:1` | 40 | 60 |
   573	| Launcher-generated S11, screened identity and empty shared project state; D-024-34/D-024-35, `worker:5067ed0:1` and `text-security:efa211d:1` with `text-security:f7af699:1` as the shared family | 80 | 160 |
   574	| **Increment ceiling** | **480** | **760** |
   575	
   576	The source cap remains **1591 = 1111 + 480**; the test cap remains **2528 = 1768 + 760**, including a03 amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. The a04 non-shim interpreter, platform-injected and regime-declared controls fit the existing environment/provider and fixture-alignment increments; no cap increases. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.
   577	
   578	RESULT records final per-file numstat, historical-base and final PR merge-base identities, actual source/test totals and per-control attribution. Preserve both the complete historical comparison and the current PR comparison so merged base changes are visible.
   579	
   580	Every later amendment maps to accepted review findings and carries `previous_sha256`; the worker raises no cap. Amend Change budget, the operative C-107 Check cap sentence and the Checks block together. A measured overrun produces a blocked PONG rather than suppression or an unreviewed text edit.
   581	
   582	## Out of scope
   583	
   584	D-024-26 still assigns exact host-probed uv/Python/Node version declarations and mise pins beyond a04's narrow launch-interpreter selection, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.
   585	
   586	Keep `home/dot_mise/config.toml`, the installed state-helper source, Codex boundary sources and updater scripts outside scope. No binding-only code returns through shared files. Add no write-boundary Python hook, gh wrapper, credential-directory substitute, installation discovery or PATH fallback.
   587	
   588	P1-14 a05 and P1-6 own approval/evidence consumption. The exact operative ledger templates tested from this task copy are `gh api --hostname github.com repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha` and `gh api --hostname github.com 'repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref=<sha40>'`. Validate the returned full 40-hex SHA and use the identical SHA in the content request. Every deciding API call binds `--hostname github.com`; every deciding subcommand binds `--repo github.com/mryfmo/dotfiles`. Refuse if the host cannot be bound, without an unbound retry or local fallback.
   589	
   590	Retain `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host`: extract those two templates, substitute only the validated SHA, exercise argv without shell evaluation, export hostile `GH_HOST`, check exact hostname/repository/SHA binding and test an isolated no-gh refusal. This is a contract test, not a ledger consumer or authentication test. Local remotes, URL rewrites, refs, objects and working-copy rows establish no approval authority.
   591	
   592	The host is not a security boundary between same-UID seats. `GH_CONFIG_DIR` does not separate macOS Keychain credentials. Native merge denials remain `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`; shared credentials permit other API routes. P1-11 owns next-records-PR detection, not main-push detection or prevention. Separate-user/host prevention remains the operator's future P1-16 decision.
   593	
   594	`dotfiles-T133-agmsg-hardening-a01` owns store driver-name validation and plugin authorization. Shared administrative exceptions/socket access, external host processes, same-UID races, later configuration reloads and hook-event limitations remain residuals. Dedicated login state is not imported from the orchestrator or used to discover executable acceptance rules.
   595	
   596	Perform no live settings application, authentication/keyring/ruleset mutation, global/administrative installation, permission-policy deployment, restart or merge. Edit no canonical task, acceptance record, decision ledger, design or another task's evidence.
   597	
   598	## Check
   599	
   600	`make render-check` and `make validate-agent-assets` pass. Run repository formatting/lint on changed files, including shellcheck/shfmt on the launcher and rendered guard; shell comments use English shdoc-compatible annotations.
   601	
   602	Run `uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` and `uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs -v` inside the worker sandbox with its private cache. Preserve complete outputs, statuses and tested identities.
   603	
   604	The final diff has at most 1591 changed lines outside `tests/`, `.orchestration/`, `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`, and 2528 under `tests/`.
   605	
   606	Measure the current PR diff against its authenticated merge-base; preserve the historical-base measurement and reconciliation described in Change budget. No unrelated base change becomes an authorized edit.
   607	
   608	Validation includes amendment 3's four c0f50fa1-red/after-green S11 fixtures, including sequential A-then-B starts on the shared configuration directory, the three c0f50fa1-red security regressions, all four local-review cases (enterprise skills retain accepted green baseline coverage), all three runtime-name/interpreter fixtures, every allowlist class, complete S01-S23 case coverage and final green module output. Malformed/unknown retained nested inputs, disabled plugin payloads and shadowed files refuse before mutation; S11 discarded fields are never forwarded. Positive controls retain default seating, canonical delivery, attachment, repeated preparation and ordinary worktree writes.
   609	
   610	Both platform renders retain the exact static deny inventory, directory/descendant coverage, narrow writable stores, private caches, MCP/plugin disables and administrative policy. Sandbox-extension fixtures prove startup refusal, rather than merely showing unchanged administrative JSON.
   611	
   612	Printed-installation evidence includes parent creation before file installation on both platforms with no privileged execution. Fake-update evidence covers Herdr's literal append followed by reconciliation and a second idempotent update.
   613	
   614	Retain existing guard, descendant system-PATH/BASH_ENV, migration, custom-hook, native-denial and cache tests. Record the installed Claude version, actual source read sets, documentation observations and any unsupported-version/source refusal without logging credentials. A version mismatch is a blocked PONG requiring re-tasking.
   615	
   616	Retain the inherited formatting reproduction at historical base `205fe85c` for the 12 out-of-scope shell files; do not repair them here. Run no local Bats tests. Required Bats results and all required checks come from GitHub Actions before RESULT.
   617	
   618	The orchestrator runs the task-consistency checker before dispatch and acceptance against this complete a04 file, using the trusted parent/interpreter/cache contract. C1-C10 and C7b pass, including both C3 task-copy rows; check C11 selectors individually. A separate C-80 security-profile context reviews this reset text before dispatch. These are prerequisites, not results claimed by this draft.
   619	
   620	## Artifacts, completion and deployment
   621	
   622	On the first a04 push, add `.orchestration/dotfiles-T133-worker-write-boundary-a04/task.md` byte-identical to the complete dispatched text. Retain `.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md` and all existing a03 evidence unchanged in `retained_predecessor_directories`; the predecessor is not an allowed write directory. Keep all other a01/a02 artifacts and implementation history as found; the a03 predecessor-deletion instruction does not carry forward.
   623	
   624	Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, operator steps, budget attribution and worker review evidence under the a04 artifact directory. Evidence lives in the worker's own worktree; RESULT says so. Use the `-worker-` review-evidence infix. Record durable decisions/failures with CompactionDB markers; the orchestrator owns main-checkout consolidation.
   625	
   626	Continue PR #431 on the existing branch from the specified head. Discard no unrelated work. The orchestrator owns base updates and dependent `after:` changes; this task retains `after: []`. Every moved final head receives fresh required evidence.
   627	
   628	Every worker command completes inside its sandbox and allowlist. Each gh/git write is an individual command without shell chaining. A boundary failure produces the exact blocked PONG; no permission-gate, tool or shell alternative bypasses it. Do not clear shared Git metadata outside the worker boundary.
   629	
   630	Allow at most one independent pre-push review and two total correction rounds, including that review's corrections. Preserve a01/a02/a03 counters separately. Surviving P0/P1 findings are `open:<id>` or `open:review-<review id>` in RESULT and stop integration for the operator's decision; do not start a private third round.
   631	
   632	Post no `@codex review` comment. Observe automatic final-head reviews within the bounded 15-minute window and record absence as `bot: none`. Required GitHub Actions pass before RESULT. Propose a disposition for every feedback item; the worker resolves no review thread and grants no acceptance.
   633	
   634	Follow repository agent-side Crit-data/receipt rules without a browser or human review request. Record resolved evidence, including a justified review-scope approval when finding-free; never use `AGENT_REVIEWED=1` without reading the evidence. Report any Plan Mode server for orchestrator cleanup.
   635	
   636	RESULT names final full head/base/branch, PR, changed files, task-copy SHA256, exact selectors, red/green identities, final numstat/attribution, schema/source/handler/root inventories, installed-version observations, inherited binding-removal inventory, scripts/installed paths, settings destinations, printed installation commands, feedback/dispositions, open findings, counters and all evidence paths. Distinguish historical claims from new final-head results.
   637	
   638	Report user-visible changes: this repository's workers alone are supported; unknown settings or environment inputs refuse; launcher startup uses the manifest-named non-shim mise interpreter, Darwin's optional encoding variable has only the declared shape, and upstream AGMSG_SPAWNED is exactly 1; every start regenerates global state with `projects: {}`, preserves only screened identity and resets native counters/caches/project history/allowedTools; workspace trust uses the launcher's existing spawn-readiness dialog acceptance; alternate providers/authentication selectors refuse; object/inline components refuse; lower-scope sandbox extensions refuse; actual enterprise skills are inspected. Refusal preserves original bytes and names the source without exposing values.
   639	
   640	Retain user-visible effects of dedicated worker login, static denies also affecting Bash writes, writable agmsg stores except trusted-plugin authorization, private caches, no worker sandbox escape, shared administrative exceptions/socket access, guarded project hooks and unchanged legacy orchestrator PermissionRequest. Formatter availability and complete executable binding remain deferred.
   641	
   642	The orchestrator obtains separate local review, task-level audit and security-profile review of the final implementation head. Final feedback collection, dispositions, acceptance and integration follow Orchestrator Playbook step 10 in order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the review receipt; merge is pinned to the reviewed final head. The worker writes no approval row.
   643	
   644	Operator deployment remains post-merge and coupled to the approved P1-14 a05 change under D-024-31: `make update`, then `make install-managed-settings`, inspect staged content, then execute the printed privileged parent-creation and platform-specific file-installation commands. Record administrative installation separately from chezmoi application.
   645	
   646	The operator logs in with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`, applies the separately prepared deterministic Codex permgate escape-denial change and restarts affected sessions. Inspect installed administrative content, dedicated directory, static denies, stores/caches, all startup sources, closed-schema refusals, MCP/plugin disables, PermissionRequest exception and sandbox startup. Check lower-scope conflicting arrays and report shared capabilities without exposing credentials.
   647	
   648	Merge alone establishes no deployment readiness. Record application, administrative installation, login, startup checks and the Codex permgate change before releasing live dependents; mechanisms requiring executable binding also wait for that owner.
   649	
   650	Not performed in task authoring: implementation, worker tests, local Bats, deployment, login or restarts. Final-head correctness and live enforcement remain unverified.
   651	
   652	## Checks (pasted by the orchestrator before each send)
   653	

exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; cat .ua/meta.json' in ~/Workspace/dotfiles
 succeeded in 22ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/acceptance/dotfiles-T133-loop-limits-a01.md
 M .orchestration/acceptance/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
 M .orchestration/acceptance/dotfiles-T133-result-precheck-a01.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-checklists.md
 M .orchestration/plans/024-design-quality.md
 M .orchestration/plans/024-omp-cutover-and-corrective-order.md
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
?? .orchestration/acceptance/dotfiles-T133-ci-efficiency-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-inv6-reset-anchors-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a02.md
?? .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a02.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md
?? .orchestration/acceptance/dotfiles-T133-result-evidence-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-result-precheck-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-result-precheck-a03-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a03-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a02.md
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
?? .orchestration/dotfiles-T133-inv6-reset-anchors-review-a01/
?? .orchestration/dotfiles-T133-pre-send-check-a01-redesign-review-a01/
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
?? .orchestration/learning/mistakes/M-20261020-09-typed-sha-and-mute-seat.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-inv6-reset-anchors-review-a01.md
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
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
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
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-2c8c05a.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-cef7ebe.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-cef7ebe.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d4798eb.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d4798eb.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-9313f2c.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-9313f2c.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-b858147.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-b858147.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-c8d2f6b.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-c8d2f6b.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md
?? .orchestration/validation/records-sync-28-pr-feedback.json
?? .orchestration/validation/records-sync-29-pr-feedback.json
f7f3806749815ba9dfd90e7ff9ee390ca6079014
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

exec
/bin/zsh -lc "sed -n '180,345p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md | nl -ba -v180" in ~/Workspace/dotfiles
 succeeded in 27ms:
   180	  - control: "5.14 item 0: 脅威モデル"
   181	    disposition: "residual: host controls reduce accidental and injected damage; shared credentials and same-UID processes prevent a seat-isolation claim."
   182	  - control: "5.14 item 1: 書き込み境界"
   183	    disposition: "residual: retained write policy and the closed startup schema implement this task's scope; later reloads and consumption races remain outside its guarantee."
   184	  - control: "5.14 item 2: 無害化した環境を最初に"
   185	    disposition: "residual: trusted-parent clean prefixes, fixed operations and declared environment inputs remain mandatory; the legacy orchestrator PermissionRequest and complete executable binding retain their separate owner."
   186	  - control: "5.14 item 3: 信頼パスの境界検査"
   187	    disposition: "residual: canonical root and component containment checks precede startup, including aliases; executable realpath binding remains with the binding task."
   188	  - control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す"
   189	    disposition: "residual: fixed dispatch avoids candidate-selected execution, while snapshots, last-use digests and complete executable identity remain with their consuming mechanisms."
   190	  - control: "5.14 item 5: 出力と予約の同一性"
   191	    disposition: "residual: this task introduces no reservation protocol; consuming orchestrator mechanisms retain ownership of full-head outputs and inode-bound locks."
   192	  - control: "5.14 item 6: 正直な残余"
   193	    disposition: "residual: the report retains shared credentials, administrative exceptions, socket access, agmsg sourcing, races, reloads and hook-event limitations."
   194	  - control: "5.14 item 7: 検証"
   195	    disposition: "residual: retained source-class fixtures and new allowlist regressions supply final-head evidence; shared trusted-execution helper adoption remains with P1-6."
   196	  - control: "5.14 item 8: 承認はコミット済み台帳から読む"
   197	    disposition: "residual: fixed-host ledger templates and hostile-host fixtures preserve the contract; P1-14 a05 and P1-6 own actual approval consumption."
   198	  - control: "5.14 item 9: 私設キャッシュ"
   199	    disposition: "residual: private worker caches and orchestrator-cache denies remain; exact interpreter declarations, resolver consumption and deployment binding remain separately owned."
   200	  - control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない"
   201	    disposition: "residual: the Worker Playbook permits no worker escape, while shared administrative capabilities and the operator's Codex permgate deployment remain explicit residuals."
   202	  - control: canonical GitHub API host binding
   203	    disposition: "residual: both ledger templates explicitly bind github.com and mryfmo/dotfiles; contract tests establish argv binding rather than enforcement by deferred consumers."
   204	  - control: hook failure policy
   205	    disposition: "residual: supported rendered entries retain onFailure block, but background hooks, excluded events and runtime timeout behavior establish no enforcement responsibility."
   206	  - control: agmsg store driver and plugin selection
   207	    disposition: "residual: plugin-code and trusted-plugin denies reduce one route; writable store-selected sourcing remains owned by dotfiles-T133-agmsg-hardening-a01."
   208	  - control: orchestrator effect merge
   209	    disposition: "residual: only the orchestrator integrates with final-head evidence and a pinned merge; shared credentials still permit API routes outside the native prefix denials."
   210	  - control: orchestrator effect update-branch
   211	    disposition: "residual: an update moves the head and requires fresh CI, feedback, local review, audit and security evidence before integration."
   212	  - control: orchestrator effect forced worker removal
   213	    disposition: "residual: none is planned; existing dirty-worktree protections remain and any operator-authorized discarded state must be recorded."
   214	premises:
   215	  - claim: >-
   216	      INV-6 carries three a03 amendments; plan 006 S2 requires design by another authoring context. This review-profile context supplies a04, reset_of a03, rather than another a03 amendment. Read-only rechecks on 2026-10-20 confirmed worker-e remains at c0f50fa1383416240ad28959dbc4635afa777175 on tools/worker-write-boundary-a01. Keep PR #431 and the uncommitted a03 implementation/test draft. The canonical a03 text and retained worker task copy both hash to 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b.
   217	    sources:
   218	      - .orchestration/plans/006-regime-v3-execution.md
   219	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
   220	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
   221	    executed_commands:
   222	      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" rev-parse HEAD', output: 'c0f50fa1383416240ad28959dbc4635afa777175'}
   223	      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" symbolic-ref --short HEAD', output: 'tools/worker-write-boundary-a01'}
   224	      - {command: 'shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md', output: 'both files: 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b'}
   225	  - claim: >-
   226	      The blocked PONG reports probe exit 0, test exit 1, zero worker correction rounds and zero independent pre-push reviews. Its green-new.log is a failing uncommitted draft: 15 tests, 45 failures, including undeclared runtime names, noncanonical TMPDIR and unreconciled fake-update hooks; it is not a RESULT or final green evidence. Retain it without relabeling.
   227	    sources:
   228	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
   229	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log
   230	  - claim: >-
   231	      runtime-contract-probe.json supplies the exact name lists below. Read-only repetition at 2026-10-20T14:57:54Z produced the same names, exit statuses and spawn digest, without a live worker or private settings. The manifest currently lacks the non-shim interpreter declaration; a04 must add it within its existing launcher policy, not discover it through PATH.
   232	    sources: [.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json]
   233	    repeated_probe:
   234	      supplied_environment_names: [HOME, LANG, PATH, TERM]
   235	      child_code: 'import os,json,pathlib,platform,pwd,tempfile,subprocess;print(json.dumps(sorted(os.environ)))'
   236	      interpreters:
   237	        - command: '/usr/bin/python3 -I -c <child_code>'
   238	          exit: 0
   239	          observed_names: [CPATH, HOME, LANG, LIBRARY_PATH, MANPATH, PATH, SDKROOT, TERM, __CF_USER_TEXT_ENCODING]
   240	          unlisted_names: [CPATH, LIBRARY_PATH, MANPATH, SDKROOT, __CF_USER_TEXT_ENCODING]
   241	          stderr: "python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead"
   242	        - command: '"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" -I -c <child_code>'
   243	          exit: 0
   244	          observed_names: [HOME, LANG, PATH, TERM, __CF_USER_TEXT_ENCODING]
   245	          unlisted_names: [__CF_USER_TEXT_ENCODING]
   246	          stderr: ""
   247	      upstream_spawn_sha256: 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731
   248	      upstream_spawn_line: 527
   249	      upstream_spawn_text: "  echo 'export AGMSG_SPAWNED=1'"
   250	      schema_has_AGMSG_SPAWNED: false
   251	      live_worker: false
   252	      private_settings_read: false
   253	  - claim: >-
   254	      The complete c0f50fa1 security review found AWS credential-chain selectors, a foreign-repository main-local inventory gap and object-form plugin command mappings. The local review found the incorrect enterprise skills root, lower-scope sandbox extensions, missing privileged parent creation and post-Herdr settings drift. The local chain stopped before a task-level audit; none exists for c0f50fa1. Repeated renderings in the local report are four findings, not additional independent findings.
   255	    sources:
   256	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
   257	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
   258	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
   259	  - claim: >-
   260	      D-024-26 retains the write boundary and transfers executable binding. D-024-29 freezes design 5.14; D-024-30 applies it by reference. The 2026-10-20 residual-list entry in this text records the allowlist generalisation without reopening the frozen items.
   261	    sources:
   262	      - .orchestration/decisions.tsv
   263	      - $HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md
   264	  - claim: >-
   265	      The inherited read-only version observation is Claude Code 2.1.300. Documentation enumerations fetched at 2026-10-19T20:41:53Z were: settings scopes User, Shared project, Project local, Managed; precedence Managed settings, Command line, Project local settings, Shared project settings, User settings; MCP scopes Local, Project, User; hook types command, http, mcp_tool, prompt, agent; plugin origins @<marketplace>, @inline, @skills-dir, @synced; plugin enablement sources --add-dir, user, project, local, flag, managed; skills roots Enterprise, Personal, Project, Nested, Additional directory, Plugin; account-synced roots remain undeclared. Recheck the installed version and loader before changing implementation.
   266	    fetched_at: "2026-10-19T20:41:53Z"
   267	    sources:
   268	      - https://code.claude.com/docs/en/settings
   269	      - https://code.claude.com/docs/en/hooks
   270	      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
   271	      - https://code.claude.com/docs/en/plugins/loading
   272	      - https://code.claude.com/docs/en/skills
   273	  - claim: >-
   274	      C-87 inherited observation: the orchestrator observed the documented ["Where skills live" table](https://code.claude.com/docs/en/skills) at 2026-10-20T04:47:57Z and the read-only loader probe at 2026-10-20T04:50Z. The Enterprise row says "`.claude/skills/<skill-name>/SKILL.md` in the managed settings directory", with Linux example `/etc/claude-code/.claude/skills/<skill-name>/`. The pinned 2.1.300 loader, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3, contains `/.claude/skills/` (11 occurrences), `.claude/skills/` (8), `/etc/claude-code` (6) and `/Library/Application Support/ClaudeCode` (3); the historical supplied probe excerpt is `LC_ALL=C /usr/bin/grep -a -o -E '…(\.claude/skills|/skills"|skills/)…' <loader> | sort | uniq -c`. These observations bind the enterprise inventory and fixture to `<managed-root>/.claude/skills`.
   275	    sources: ["https://code.claude.com/docs/en/skills", ".orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md"]
   276	  - claim: "Worker a010 blocked before any edit (PONG 2694, 2026-10-20T04:00:43Z): the loader persists numStartups at start and hasCompletedOnboarding at onboarding; the orchestrator reproduced the installed-loader probe below, not a live worker start."
   277	    sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md]
   278	    probe: {executed_by: review-profile-author, executed_at: "2026-10-20T14:57:54Z", loader: "$HOME/.local/share/mise/installs/npm-anthropic-ai-claude-code/2.1.300/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe", format_observed: Mach-O arm64}
   279	    executed_commands:
   280	      - {command: 'shasum -a 256 <loader>', output: '475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3  <loader>'}
   281	      - {command: '<loader> --version', output: '2.1.300 (Claude Code)'}
   282	      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o numStartups <loader>', output: '12'}
   283	      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o hasCompletedOnboarding <loader>', output: '15'}
   284	    quoted_string_probes: [{command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"numStartups"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasCompletedOnboarding"'' <loader>', output: '0'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasTrustDialogAccepted"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"oauthAccount"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"mcpServers"'' <loader>', output: '29'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"enabledMcpjsonServers"'' <loader>', output: '5'}]
   285	  - claim: >-
   286	      The single source inventory is S01-S23 below plus executable environment-file contents admitted by the launch-input schema. Each parameter denotes every actual matching file, inspected independently before merging. User means the dedicated configuration directory; managed-root is the platform directory containing managed-settings.json. S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json; S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery; S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration; S12 each skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json; S16 every default hooks/hooks.json and explicitly referenced plugin hook file; S17 every admitted marketplace-root/.claude-plugin/marketplace.json; S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file; S22 every applicable subagent Markdown file; S23 every default or referenced plugin LSP file. Non-file managed delivery and caller-selected inputs must fit the same closed schema and read set or cause a named refusal.
   287	    sources:
   288	      - https://code.claude.com/docs/en/settings
   289	      - https://code.claude.com/docs/en/managed-settings
   290	      - https://code.claude.com/docs/en/server-managed-settings
   291	      - https://code.claude.com/docs/en/plugins/manifest-reference
   292	      - https://code.claude.com/docs/en/skills
   293	---
   294	
   295	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a04 — plan 024 P1-15; worker startup screen; seat a010
   296	
   297	## Goal and reset
   298	
   299	[memory:decision] Reset a03 under INV-6 and plan 006 S2 through this separate review-profile authoring context. Worker a010 is Codex, security profile, in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`; this task changes Claude's boundary and preserves Codex policy. Continue `tools/worker-write-boundary-a01` and PR #431 from `c0f50fa1383416240ad28959dbc4635afa777175`, keeping the uncommitted a03 draft and all predecessor evidence; open no second PR.
   300	
   301	Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Retain every a03 item and fix, with only the runtime/interpreter decision specified here.
   302	
   303	[memory:failure] a01 and a02 each spent two worker rounds; a03's blocked PONG reports zero worker correction rounds and zero independent pre-push reviews, while its amendment history remains counted. This reset supplies a04 at most two worker correction rounds in total, including pre-push corrections, and at most one independent pre-push review; it erases no predecessor counters or findings.
   304	
   305	The retained draft is not approved, and its `raw/green-new.log` is explicitly failing. The c0f50fa1 local chain stopped before its task-level audit. Obtain new final-head audit and security evidence; do not describe either as inherited.
   306	
   307	## History
   308	
   309	a01 and a02 each exhausted their two worker rounds, and a03 reset the lineage to a closed startup schema while continuing PR #431. Its amendments bound executable environment-file contents, regenerated S11 with screened identity and empty shared project state, and corrected the enterprise skills inventory; those controls and their finding history remain. The worker blocked on shim/platform-added runtime names and upstream `AGMSG_SPAWNED=1`, preserving its uncommitted draft and failing evidence. INV-6's three counted a03 amendments trigger plan 006 S2, so another context authors a04 to resolve only that runtime-name/interpreter contract instead of extending a03.
   310	
   311	## Design and finding history
   312	
   313	Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 by reference, including its residual list. D-024-29 keeps items 0-10 frozen; D-024-30 narrows C-88 to exact contract sentences asserted by tests.
   314	
   315	Item 1 applies to dedicated worker settings, static input-derived write protection and refusal before startup.
   316	Item 2 applies to trusted-parent execution, clean environments and fixed command selection.
   317	Item 3 applies to canonical anchor, worktree and component identities before consumption.
   318	Item 8 applies to committed approval authority through explicitly host-bound repository API calls.
   319	Item 9 applies to private caches and the trusted parent's interpreter/cache inputs.
   320	
   321	**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a04:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.
   322	
   323	Read the full a02 and a03 acceptance records, a03 task, blocked PONG and both runtime evidence files, and both c0f50fa1 reviews named in `premises:`. Retain the following history and finding classes in the a04 report and acceptance lineage:
   324	
   325	| Finding | Class | Required treatment |
   326	| --- | --- | --- |
   327	| `text-security:2ae9e2c:1` | input-inventory | Project `.mcp.json` remains independently screened. |
   328	| `text-security:ebbb71b:1` | input-inventory | Skills-directory plugins remain inventoried even when disabled. |
   329	| `text-security:ebbb71b:2` | input-inventory | Dedicated global state regenerates `mcpServers: {}` and `projects: {}`; native project entries are discarded. |
   330	| `text-security:ebbb71b:3` | repository-binding | Canonical main comes from the fixed repository API. |
   331	| `text-security:b2a186e:1` | input-inventory | Inspect handler type before command; non-command types refuse. |
   332	| `text-security:b2a186e:2` | repository-binding | Both ledger calls bind `--hostname github.com`. |
   333	| `text-security:ac9ce14:0` | correct | Historical text approval only; it does not approve a04. |
   334	| a02 independent pre-push review | input-inventory | Retain fixes for `env.HOME` guard selection and fenced dynamic commands. |
   335	| `local:79ea98a:1` | tool-environment | Retain manifest-generated `--advisor fable` acceptance. |
   336	| `local:79ea98a:2` | tool-environment | Retain absolute tool paths and attachment identity environment. |
   337	| `local:79ea98a:3-4` | partial-fix | Retain custom-hook preservation and legacy PreToolUse migration. |
   338	| `security:c0f50fa:1` | input-inventory | Refuse undeclared credential-chain/provider selectors. |
   339	| `security:c0f50fa:2` | input-inventory | Refuse worker starts for repositories other than the validated anchor. |
   340	| `security:c0f50fa:3` | input-inventory | Refuse object and inline plugin/command components. |
   341	| `local:c0f50fa:1` | tool-environment | Inventory enterprise skills under the actual managed root. |
   342	| `local:c0f50fa:2` | tool-environment | Reject lower-scope sandbox extensions before array merging. |
   343	| `local:c0f50fa:3-4` | partial-fix | Fix printed parent creation and post-installer reconciliation here. |
   344	| `text-security:f7af699:1` | input-inventory | Admit executable environment-file contents only when absent, empty or launcher-generated for this start. |
   345	| `worker:5067ed0:1`, `text-security:efa211d:1` | input-inventory | Regenerate S11 at every start with `projects: {}` and screened identity; discard native persisted state, including every project's state, and use the launcher's existing spawn-readiness trust-dialog acceptance. |

exec
/bin/zsh -lc "sed -n '346,505p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md | nl -ba -v346" in ~/Workspace/dotfiles
 succeeded in 22ms:
   346	| `text-security:be969e3:1` | input-inventory | Inventory enterprise skills and plant both Markdown and bundled plugin fixtures under `<managed-root>/.claude/skills`, following the C-87 documented table and pinned-loader probe. |
   347	
   348	S1 first triggered on the three source omissions in 2ae9e2c/ebbb71b. The re-plan enumerated S01-S23, but subsequent findings still exploited open field/value acceptance; the c0f50fa1 security findings bring that post-re-plan family to its sixth finding. This reset changes the approach rather than adding three more denylist entries.
   349	
   350	Preserve the advisory-owner history and owner `dotfiles-T133-worker-write-boundary-followup-a01` exactly as history. The two c0f50fa1 P2 fixes are retained from a03 by this text; the orchestrator reconciles their owner rows and updates dependent task references. The worker edits no canonical acceptance or owner task.
   351	
   352	Retain D-024-26's transferred binding findings, including `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. Do not relabel them as fixed.
   353	
   354	## Closed startup schema
   355	
   356	Declare this schema in `home/dot_agents/agent-config.yaml` and expose it through the existing renderer/preparation code. Candidate files, Git objects and installed upstream schemas never define their own acceptance policy. Add no new helper, generated output file or dependency.
   357	
   358	The schema below is exhaustive for data forwarded to the loader. Objects reject unknown keys at every level, including nested objects and records that would otherwise be preserved; S11 fields designated for discard are not screened or preserved. Reject duplicate JSON keys, wrong types, Boolean/integer substitutions, unreadable inputs and unsupported forms. Missing optional fields may pass; a present field must match its declared source-specific form.
   359	
   360	### Settings and values
   361	
   362	The only settings keys are `permissions`, `sandbox`, `hooks`, `env`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `enabledPlugins`, `syncClaudeAiPlugins`, `syncClaudeAiSkills`, `extraKnownMarketplaces` and `disableSkillShellExecution`.
   363	
   364	| Node | Accepted shape and values |
   365	| --- | --- |
   366	| `permissions` | Only `defaultMode`, `deny`, `additionalDirectories`; `defaultMode` is `auto` where applicable; `additionalDirectories` is `[]`; `deny` is a renderer-declared worker/native-denial fragment for that source. No caller-added allow/ask rule or alternate permission mode. |
   367	| `sandbox` | Only the keys emitted by the worker or administrative renderer: `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands`, `excludedCommands`, `filesystem`, `network`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `allowAppleEvents`. |
   368	| `sandbox.filesystem` | Only `allowWrite`, `disabled`; exact source-specific canonical values. Worker write grants are the four declared agmsg stores; ordinary worktree/cache writes remain provided by the worktree boundary. |
   369	| `sandbox.network` | Only `allowedDomains`, `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`; exact source-specific canonical values. |
   370	| Sandbox lists and Booleans | Every present leaf/list equals the canonical worker fragment in S01-S04 or administrative fragment in S05-S07. Worker exclusions are empty; additional write roots/sockets are refused. Only administrative sources may contain the exact shared three exclusions and single Herdr socket. |
   371	| `hooks` | Only source/event/matcher/operation combinations generated by the trusted renderer or delivery constructor. Groups have only `matcher`, `hooks`; handlers have only renderer-declared `type`, `command`, `timeout`, `async`, `statusMessage`, `onFailure`, with exact canonical values. |
   372	| Handler type | Only the string `command`; validate it before reading `command`. HTTP, MCP-tool, prompt, agent, unknown, missing, null and non-string types refuse. |
   373	| MCP approval fields | `enableAllProjectMcpServers: false`; `enabledMcpjsonServers: []`; `disabledMcpjsonServers: []` when present. Approval state never exempts a server definition. |
   374	| Plugin fields | `enabledPlugins` maps only manifest-known or inventoried plugin identities to `false`; both sync fields are `false`; `extraKnownMarketplaces` is `{}`. |
   375	| Skill execution | `disableSkillShellExecution`, when present, is `true`. |
   376	| `env` | Only the four exact name/value pairs in the next subsection; arbitrary strings, maps and provider credentials are not preserved. |
   377	
   378	Absent or empty settings objects pass where the source permits them. Administrative drop-ins/cache may contain canonical partial objects; partial means omitted declared fields, never new fields or alternate values. Validate each list before merging so an empty generated worker list cannot conceal a broader lower-scope array.
   379	
   380	There is no canonical worker setting for helpers, status-line commands, wrappers, alternate sandbox executables, policy helpers or authentication refresh/export commands. Their keys refuse as undeclared, including misplaced forms. The orchestrator managed PermissionRequest exception is not a worker-start exception.
   381	
   382	The old instruction to preserve unrelated non-executable state now applies only to fields admitted by this schema. Unknown settings refuse without deletion or normalization; S11 alone discards pre-existing fields outside its declared structures and carried identity, without screening or forwarding them.
   383	
   384	### Environment and launch arguments
   385	
   386	Settings `env` admits exactly `GH_TELEMETRY="false"`, `DO_NOT_TRACK="1"`, `CHECKPOINT_DISABLE="1"` and `AWS_EC2_METADATA_DISABLED="true"`, as declared by the manifest. The last name is the sole declared `AWS_*` exception and cannot select credentials or a provider.
   387	
   388	The launch-input schema classifies names by source: existing parent/runtime declarations, `regime-declared`, and `platform-injected`. The latter two classes below are closed enumerations, not prefixes. They do not extend settings `env`, configuration-file keys or CLI arguments.
   389	
   390	The launcher and its startup/preflight Python children use only the manifest-named absolute mise-installed non-shim interpreter, observed here as `<validated-home>/.local/share/mise/installs/python/3.15.0/bin/python3.15`. Add that narrow declaration to the existing manifest-owned launcher policy and consume it through the existing renderer; never route through `/usr/bin/python3`, a mise shim, PATH lookup or an interpreter-discovery fallback. Cover startup bootstrap/home lookup as well as preparation. This selects the interpreter for this boundary without returning the deferred complete binding work to scope.
   391	
   392	The launch-input schema admits only these names, with source-specific values supplied or checked by the trusted parent:
   393	
   394	| Names | Value authority |
   395	| --- | --- |
   396	| `HOME`, `PATH`, `LANG`, `TERM` | Validated passwd home; prescribed system-only child PATH; `C.UTF-8`; declared terminal value. Hook children retain `TERM=dumb`. |
   397	| `TMPDIR` | Canonical trusted temporary directory supplied by the parent, not a candidate configuration root. |
   398	| `CLAUDE_CONFIG_DIR` | Exactly the dedicated worker directory under the validated home. |
   399	| `CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` | Parent-bound canonical project identity and runtime shell file; `CLAUDE_ENV_FILE` additionally requires the executable-content control below. |
   400	| `UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR` | Exactly `<canonical-worktree>/.uv-cache` and its `python` child. |
   401	| `regime-declared`: `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE`, `AGMSG_AGENT_PID` | Retain a03's exact authorities: `0`, validated launcher store selection, declared monitor value and numeric runtime process identifier; unset default-store selection remains supported. |
   402	| `regime-declared`: `AGMSG_SPAWNED` | Exactly the string `1`, set by upstream `spawn.sh` on the launch surface before the worker CLI; require it on spawn-launched roles and do not synthesize it for unrelated child roles. |
   403	| `platform-injected`: `__CF_USER_TEXT_ENCODING` | Darwin only; present or absent allowed. A present string must full-match `0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+`. The regime validates the shape and otherwise never reads or uses it. Linux presence refuses. |
   404	| `HERDR_ENV`, `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_AGENTS_LAYOUT`, `HERDR_SOCKET_PATH` | Validated control-plane identity, `managed` layout and canonical configured socket; these grant no worker sandbox exception. |
   405	| `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID` | Parent/runtime session identifier and numeric process identifiers where required by canonical attachment/delivery. |
   406	| `CLICOLOR_FORCE`, `FORCE_COLOR` | Launcher-written `1` only where the launch route uses them. |
   407	| `GH_TELEMETRY`, `DO_NOT_TRACK`, `CHECKPOINT_DISABLE`, `AWS_EC2_METADATA_DISABLED` | The four fixed values above. |
   408	| `CHEZMOI_SOURCE_DIR`, `CHEZMOI_HOME_DIR` | Preparation-only trusted source/home bindings; not caller-selected worker configuration or executable roots. |
   409	
   410	The read-only amendment-1 probe of the [documented environment variables](https://code.claude.com/docs/en/env-vars) identifies `CLAUDE_ENV_FILE` as the only name admitted above that selects a file whose contents execute: Claude runs its shell contents before Bash commands. No other admitted name has that documented role; `CLAUDE_CODE_SHELL` and `CLAUDE_CODE_SHELL_PREFIX` remain undeclared. Include the named file's contents in the preflight read set alongside S01-S23.
   411	
   412	For every admitted executable-content file variable, preflight accepts its named file only when absent, empty, or byte-identical to canonical contents generated by the launcher for this start. Inspect without sourcing or executing it; unreadable/nonregular files and any other contents refuse before trust, migration, regeneration, hooks or worker commands with `worker startup refused: <file>: <variable>: noncanonical executable environment file contents`. Preserve refused bytes; never overwrite a planted file to make it pass. After all preflight checks pass, the launcher itself writes the canonical runtime-file contents, records SHA256 bound to the variable, canonical file and this start in existing startup state/evidence, and verifies those bytes before forwarding. Candidate-supplied or prior-start digests cannot authorize contents. Reuse the existing runtime file and startup state; add no sidecar, helper or generated configuration output. Later replacement races and reloads retain their existing residual owners.
   413	
   414	Validate proposed worker configuration inputs before forwarding them. A clean child environment contains only the names declared for that child role; do not inherit the caller environment wholesale. Unknown proposed environment names refuse rather than becoming an unchecked pass-through. Existing profile/control-plane variables used to select a worker are consumed through their existing manifest-owned interfaces, not forwarded as arbitrary worker settings.
   415	
   416	Every `CLAUDE_CODE_USE_*`, `AWS_*`, `ANTHROPIC_*`, `*_API_KEY`, `*_TOKEN` and `*_PROFILE` name refuses unless explicitly declared above with its exact allowed value. In particular refuse `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE` in settings and launch inputs before any credential lookup or helper execution. Add no AWS configuration parser.
   417	
   418	No shell/interpreter startup or loader override is declared: `BASH_ENV`, `ENV`, `NODE_OPTIONS`, `NODE_PATH`, `PYTHON*`, `LD_*`, `DYLD_*`, shell wrappers and alternate configuration/cache roots refuse as worker inputs. Do not print their values.
   419	
   420	Preserve the manifest-generated Claude argument interface: only `--model`, `--effort`, `--advisor` with their declared profile values, including `--advisor fable`. Caller-added settings, MCP, plugin, agent and additional-directory arguments refuse. Keep existing Codex arguments and network/shared-Git policy unchanged.
   421	
   422	A clean-parent probe runs through the interpreter named by the rendered manifest, imports the same modules as the predecessor probe, and asserts `CPATH`, `LIBRARY_PATH`, `MANPATH` and `SDKROOT` are absent. They remain undeclared and refuse if encountered; do not delete them to conceal an unexpected injection. Test the observed child environment as well as the parent's proposed names, with child-role-specific declarations.
   423	
   424	Any other new name, source, required state field or interpreter mismatch still blocks and re-tasks. Send a blocked PONG naming the boundary, exact command and status, with probe JSON containing the supplied/observed name lists, undeclared names and interpreter identity under the a04 evidence directory. Preserve the predecessor JSON unchanged. No wildcard, prefix-wide acceptance, candidate-learned schema, suppression or default-as-authorization is allowed; print no environment values.
   425	
   426	### Sources, roots and component forms
   427	
   428	The sole repository anchor is the manifest declaration resolving to `$HOME/Workspace/dotfiles`. Bind its identity to the validated passwd home and actual main checkout, resolving symlinks and filesystem case aliases. Worker roots must be registered linked worktrees beneath that anchor's declared `.claude/worktrees/` root with the same Git common directory.
   429	
   430	Every worker launch route, for either worker kind, refuses another repository before worktree creation, identity registration, hook writes, workspace trust or spawn. The refusal names this task: `worker startup refused: dotfiles-T133-worker-write-boundary-a04: unsupported repository root`. Do not fix the foreign-root finding by inspecting the fixed anchor while launching elsewhere.
   431	
   432	Admitted configuration roots are the dedicated worker directory, the validated anchor/worktree `.claude` directories, applicable nested worktree and additional-directory `.claude` directories, the platform managed root and contained plugin roots discovered through the declared registry. Inherited MCP files are the independently enumerated ancestor read set. No account-synced, inline, seed, alternate cache or caller-selected root is admitted; caller-added additional-directory arguments remain refused.
   433	
   434	The admitted skills roots are exactly Enterprise `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), Personal `<absolute-home>/.claude-worker/skills` under the dedicated configuration directory, Project `<project>/.claude/skills`, Nested `<subdir>/.claude/skills`, Additional directory `<add-dir>/.claude/skills` under an applicable `--add-dir` directory, and Plugin `<plugin>/skills`. Inspect both `<skills-root>/<name>/SKILL.md` and bundled `<skills-root>/<name>/.claude-plugin/plugin.json`. Managed command/agent locations likewise start at the actual managed root. Resolve every selected path and refuse containment escapes, unsupported aliases, missing references or unreadable files.
   435	
   436	| Source form | Closed acceptance |
   437	| --- | --- |
   438	| S08-S10, S18-S19 | Objects containing only absent or empty `mcpServers`/`managedMcpServers` maps. No server, including remote-only definitions, is canonical here. |
   439	| S11 global state | At every start, after all preflight checks pass and before any loader/worker command, write the existing `CLAUDE_CONFIG_DIR/.claude.json` from scratch: `mcpServers: {}`, `projects: {}` and `hasCompletedOnboarding: true`, plus screened identity fields below. The generated file carries no per-project inventory or pre-generated workspace trust. Never merge the previous file into this output. |
   440	| S11 pre-existing structures and identity | The existing file must be a JSON object. Missing optional retained fields pass and generated fields are written anew. Present top-level `mcpServers` must be `{}`. Carry optional `oauthAccount` only as an object with string-only members from this documented fixed set: `accountUuid`, `emailAddress`, `organizationUuid`, `displayName`, `fullName`, `organizationRole`, `workspaceRole`; declare the same set in the manifest and fixtures. Carry optional `userID` only as a string matching `^[0-9a-f]{64}$`, the installed loader's hex form. Undeclared identity members, non-string `oauthAccount` members, invalid identity values and a nonempty or malformed top-level MCP map refuse with `worker startup refused: <state-file>: <offending-key>: <named reason>` before any command or mutation, preserving refused bytes. Nonempty top-level servers use the exact reason `noncanonical global state` as tamper evidence. |
   441	| S12/S15 plugin descriptor | Only `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and the component keys `hooks`, `mcpServers`, `lspServers`, `commands`, `agents`, `skills`. Descriptive fields are strings, keywords are strings, and author has only string `name`, `email`, `url`. |
   442	| Component references | Each present component is one scalar string referencing a regular file within its admitted root. The screening reads that file under its source schema before accepting it. Arrays, objects, inline content, URLs and explicit directory references refuse. Default component directories are independently expanded into inspected files. |
   443	| S13 installed registry | Only `version: 2` and `plugins`; plugin IDs map to record lists with only `scope`, `installPath`, `version`, `installedAt`, `lastUpdated`, `gitCommitSha`, `projectPath`. Scope is user/project/local; paths are contained and project-bound; descriptive fields are strings and a present commit is 40 hex. Every referenced descriptor is read and every discovered ID is disabled. |
   444	| S14 marketplace registry | Only `{}`; no refresh source or executable header helper is canonical. |
   445	| S16 hook file | Only an absent/empty `hooks` object; plugin-owned handlers have no canonical worker operation. |
   446	| S17 marketplace descriptor | Only descriptive `name`, `owner`, `metadata`, `plugins`; owner has string name/email, metadata has string description/version, and plugins is absent or `[]`. Additional plugin selections refuse. |
   447	| S20-S22 Markdown | Plain text with the existing restricted frontmatter grammar: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model. Booleans are Boolean, model/tool selections are manifest-declared values, and unknown/nested executable forms refuse. Dynamic shell expansion, including fenced forms, refuses everywhere. |
   448	| S23 LSP | Only `{}`; command/args definitions are not canonical. |
   449	| Non-file managed inputs | Enumerated canonical administrative data only; otherwise refuse with the managed source name before executing any helper or starting Claude. |
   450	
   451	For S11, every other pre-existing top-level field, including the entire `projects` value and all its contents, `numStartups`, prior onboarding state, tips/changelog caches, project `history`, `allowedTools` and cost counters, is neither screened nor preserved; only syntax/duplicate-key/readability checks apply to the whole input. Discarded objects and arrays are never recursively screened or forwarded. Generate onboarding anew and `projects: {}`, preserve only screened identity values, and reuse the existing atomic writer after the complete preflight; the loader regenerates native state. The anchor's workspace trust is established by the launcher's existing acceptance of the workspace-trust dialog during spawn's readiness wait (`herdr-agents --add-worker` for a Claude worker, documented in the SKILL's 'Regime activation and progress' section). All Claude workers share `CLAUDE_CONFIG_DIR` at `$HOME/.claude-worker`; discarding the prior `projects` value lets sequential sibling starts succeed. A loader requiring another preserved field blocks and retasks rather than widening silently.
   452	
   453	These restrictions also apply to disabled plugins and shadowed sources. Do not recursively ignore an unknown object because it lacks a familiar executable key. A plugin `commands` mapping containing `{"source": ...}` or inline `content` refuses at the selecting file/key.
   454	
   455	## Implementation and retained controls
   456	
   457	1. Keep one preflight over S01-S23, admitted executable environment-file contents and the closed schema. Every Claude route calls it before workspace trust, migration, normalization, regeneration or execution. Enumerate through the filesystem, including ignored/untracked inputs; neither Git tracking nor a nearer definition removes a source. Inspect implicit and selected components separately without executing helpers, installing packages, fetching plugins or starting servers.
   458	
   459	2. Refusals identify the actual source and key/class without printing payloads, environment values, URLs with credentials or authentication material. Preserve the handler message `worker startup refused: <source-file>: hooks.<event>[<group-index>].hooks[<handler-index>]: noncanonical hook handler`, with zero-based indices. Other refusals use `worker startup refused: <source>: <key>: <named reason>`. Unknown settings, selectors, roots, components and source forms each receive a named reason.
   460	
   461	3. Retain exact recognized legacy-delivery classification, including canonical project binding. First screen every source; only after complete success migrate recognized owned entries, validate the prepared result under the same schema, then write. Unknown content outside S11's discard partition refuses without changing any pre-existing bytes; successful S11 regeneration intentionally replaces discarded state only after every source passes. Never rewrite tracked settings or create a local file merely for migration. Keep repeated preparation and delivery-tool-unavailable behavior.
   462	
   463	4. Retain dedicated `CLAUDE_CONFIG_DIR`, both private cache variables on every actual worker route, `AGMSG_RESOLVE_PROJECT=0`, validated `AGMSG_STORAGE_PATH`, canonical attachment identity and `onFailure: "block"` where supported. A writable `run/proj.<pid>.project` cannot replace the explicit project identity. Preserve the a02 absolute Herdr/jq/Node/npm/Codex calls and attachment environment; fixed PATH must not regress attachment or default seating.
   464	
   465	5. Keep static `trusted_paths` derived from trusted executable inputs, not Git trees/indexes. Preserve anchored source/control paths, tracked/main-local settings, `.orchestration`, both `.agents/worklog/**` and `.agents/worklog/uv-cache/**`, worktree `.claude` directory/descendant targets and `.mcp.json`. Ordinary worktree source and private cache writes remain available.
   466	
   467	6. Retain explicit protection of `<absolute-home>/.agents/agent-config.yaml`, model profiles, permgate policy, skill scripts/SKILL files, agmsg plugin code and `db/trusted-plugins`, `<absolute-home>/.claude/**`, `<absolute-home>/.claude-worker/**`, installed guard, local wrappers/application code, configuration/state/tool installations and shared uv caches. Keep directory and descendant user-site protection for `.pth`, `usercustomize.py` and `sitecustomize.py` on both platforms. Add no blanket `<absolute-home>/.agents/**` or `<absolute-home>/.local/**` deny: agmsg `db`, `teams`, `run`, `ext-tools` stay writable except `db/trusted-plugins`.
   468	
   469	7. Retain separate orchestrator, worker and administrative renders. Worker policy keeps `defaultMode: auto`, sandbox startup failure, disabled unsandboxed requests, empty user exclusions, restricted writes, no user Herdr socket, explicit MCP auto-approval disables, account sync off and false plugin entries including discovered `@skills-dir` identities. Empty maps alone do not disable plugins or replace screening.
   470	
   471	8. Administrative settings retain enabled sandboxing, `failIfUnavailable: true`, disabled unsandboxed requests, filesystem enforcement, disabled weaker isolation/Apple Events/all-socket/local-binding switches, exactly the Herdr socket, and exactly these ordered exclusions: `agmsg-dispatch *`, `herdr-agents *`, `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These shared capabilities remain available to every Claude seat and authorize no worker escape. Lower-scope canonical validation rejects extra exclusions, writes or sockets before array merging.
   472	
   473	9. Keep the orchestrator managed PermissionRequest command's existing literal bytes unchanged, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.
   474	
   475	10. Apply design 5.14 by reference for trusted-parent execution, Python isolation and Git inspection. Consume the manifest-named non-shim interpreter specified above on every launcher startup/preflight Python route; add no resolver, helper, private executable directory, PATH fallback or broader version-pin work. Do not execute arbitrary task-body shell strings as probes.
   476	
   477	11. Preserve guard routing, fixed payload paths, argument boundaries, stdin and child status. Canonical worker/sibling/unrelated/missing launch identities execute no orchestrator project payload. Only fixed installed worker-delivery operations run for workers. Formatter/map operations also reject worker/outside-anchor tool inputs. Keep tracked settings portable and all existing event/validator markers.
   478	
   479	12. Preserve managed SessionStart/PostToolUse/PreToolUse migration, custom-hook ordering, mixed entries, escaped-tilde distinctions, stale replacement and idempotence. For `make update`, reconcile the managed Claude settings after `scripts/update-agent-assets.sh` runs Herdr's installer, using the allowed Makefile/merge/renderer surfaces. Do not edit the updater script or import its unguarded hook as canonical. Verify one effective guarded hook and no managed-settings drift after repeated fake updates.
   480	
   481	13. `install-managed-settings` still stages `<absolute-home>/.claude/managed-settings.rendered.json` nonprivileged. Print a quoted privileged `mkdir -p` for the detected administrative parent before the existing quoted `sudo install -m 0644` command. Cover both platform destinations and homes containing spaces. Execute neither privileged command; do not install, log in or restart.
   482	
   483	14. Keep all existing validator checks, exact three-entry exclusion fixtures on both platforms, legacy PermissionRequest validity, duplicate-hook checks, ordering/timeouts, freshness, portability and secret/home-path scanning. Add no bound-PermissionRequest mode. `.gitignore` retains `.uv-cache/` as this task's only addition.
   484	
   485	15. Worker Playbook step 4 retains this exact test-asserted sentence:
   486	
   487	> Complete every worker command, including gh, git push and authenticated git fetch, inside the sandbox and allowlist without forbidden actions or escalation; anything that cannot complete there is `AGMSG-PONG v1 status=blocked` naming the exact command and boundary.
   488	
   489	The entire Worker Playbook, including steps 2, 5 and 11, authorizes no exception. Evidence-sync writes/masking, CompactionDB consolidation and agmsg-dispatch control-plane exemptions remain orchestrator-only. Workers write required relative evidence in their own worktree; the orchestrator copies it before acceptance. Preserve merged documentation changes and run the complete documentation module.
   490	
   491	## Regression fixtures
   492	
   493	Write the new tests before implementation. Use the existing temporary-HOME, managed-root, linked-worktree and fake-launcher builders. Tests execute no payload, credential helper, HTTP endpoint, server, plugin, subagent or live worker.
   494	
   495	Each refusal fixture asserts the source/key or named root message, unchanged existing bytes, no migration/regeneration, no trust acceptance, no spawn and absent execution/request markers. Positive absent/canonical controls and repeated starts remain covered.
   496	
   497	| Selector | Required coverage |
   498	| --- | --- |
   499	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees` | Red on c0f50fa1, green after: sequentially start registered linked-worktree workers A then B on one shared `CLAUDE_CONFIG_DIR`. A's start leaves the regenerated file; simulated loader writes then add A's project entry with a `history` list. B's start succeeds and, before its first command, leaves exactly the regenerated file with `projects: {}` and screened identity. Replace any planted-project-key refusal and same-worktree restart fixture with this cross-worktree sequence. |
   500	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_global_state_with_screened_identity` | Red on c0f50fa1, green after: pre-existing S11 has `numStartups: 5`, `hasCompletedOnboarding: true`, `projects[anchor].history` as a list and synthetic valid `oauthAccount`/hex `userID`. A fake worker start succeeds; before its first command the file equals exactly `mcpServers: {}`, `projects: {}`, `hasCompletedOnboarding: true` plus unchanged screened identity. Cover absent state/identity; all discarded fields and project contents disappear without semantic screening. |
   501	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonempty_global_mcp_servers` | Red on c0f50fa1, green after: pre-existing S11 has nonempty top-level `mcpServers`; assert exactly `worker startup refused: <state-file>: mcpServers: noncanonical global state` before any command, preserving all bytes and absent mutation/trust/spawn/execution markers. |
   502	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member` | Red on c0f50fa1, green after: a documented `oauthAccount` member contains an object; refuse with the file and exact member key named before any command and preserve all bytes. Also cover arrays, other non-string values, undeclared identity members, invalid `userID` and malformed retained structures; canonical string-only identities pass. |
   503	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` | Red on c0f50fa1, green after: a pre-existing forwarded `CLAUDE_ENV_FILE` contains a planted command marker and exports restoring refused environment variables. Refuse with the variable and file named before any hook/worker command runs, without sourcing the file; assert unchanged bytes, no migration/regeneration/trust/spawn and absent command markers. In this one fixture retain absent, empty and same-start launcher-generated positive controls with recorded SHA256, and show that a prior-start digest cannot authorize foreign contents. |
   504	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_aws_credential_chain_selectors` | Red on c0f50fa1: the four reported selectors select a synthetic worker-owned AWS configuration containing `credential_process`; preparation refuses without running or trusting it. Test settings and launch inputs. |
   505	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root` | Red on c0f50fa1: another repository with main-local payload refuses with this task's name before any side effect, for both kinds and all worker routes; the validated anchor/control passes. |

**Reviewing references and planning design**
codex
この案は、起動時の入力検査と、後続タスクが担う実行ファイルの束縛を分けています。その境界を踏まえ、`closed` とした行のテスト範囲、および残余リスクとして明記された箇所に実効性のある制御が残るかを確認しています。
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '506,597p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md | nl -ba -v506" in ~/Workspace/dotfiles
 succeeded in 108ms:
   506	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components` | Red on c0f50fa1: object `source` mappings and inline `content`, including dynamic Markdown, refuse even with the plugin disabled. |
   507	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys` | One fixture per settings source, unknown top-level and nested keys, including a harmless-looking future key; candidate data cannot extend the allowlist. |
   508	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors` | Every prohibited name family, settings/launch placement, exact fixed-value AWS exception, unknown ordinary environment names and noncanonical declared values. |
   509	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_requires_string_component_references` | Scalar file control; object, list, directory, missing file, outside-root reference and unreadable component negatives. |
   510	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch` | Command-free HTTP separately in S01-S07 on both platforms; other documented/unknown/missing/malformed types; other hook-bearing sources; exact indexed refusal. |
   511	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_managed_skills_use_actual_managed_root` | Retained green baseline on c0f50fa1, accepted by owner PING 2751; do not manufacture a red result: using the same temporary managed-root fixture as S05/S06 for both Darwin and Linux, plant a Markdown skill at `<managed-root>/.claude/skills/<name>/SKILL.md` and a bundled plugin payload at `<managed-root>/.claude/skills/<name>/.claude-plugin/plugin.json` with hooks; metadata-only control produces explicit disable. |
   512	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_project_sandbox_extensions_are_refused_before_launch` | Red on c0f50fa1: `excludedCommands: ["*"]`, `filesystem.allowWrite: ["/"]`, extra sockets and nested unknowns in project/local scopes; canonical administrative controls remain accepted. |
   513	| `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_creates_managed_parent_in_printed_commands` | Red on c0f50fa1: missing parent, both platforms, quoting, mkdir-before-install, staged JSON and absent executed-sudo marker. |
   514	| `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_update_reconciles_settings_after_herdr_install` | Red on c0f50fa1: fake Herdr installer re-appends its literal hook, then update reconciliation restores one guarded entry; repeated update preserves custom hooks and produces no managed drift. |
   515	
   516	The runtime-name regressions below are required within the unchanged environment and fixture-alignment budgets:
   517	
   518	| Selector | Required coverage |
   519	| --- | --- |
   520	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names` | Execute the predecessor's name-only probe through the absolute non-shim interpreter read from the rendered manifest, with only HOME/PATH/LANG/TERM supplied. Assert CPATH, LIBRARY_PATH, MANPATH and SDKROOT are absent; Darwin permits only the declared platform addition. Route fixtures prove bootstrap, home lookup and preflight use that interpreter without invoking the system shim or PATH fallback. Preserve command/status/name-only JSON. |
   521	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment` | Darwin absent and correctly shaped present controls pass; malformed shapes, wrong types, trailing content and Linux presence refuse before mutation/trust/spawn. The value never selects behavior, a path or an executable and never appears in evidence. An unrelated injected name blocks with probe JSON. |
   522	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment` | Fake upstream spawn exports exactly AGMSG_SPAWNED=1 before CLI entry; accept it only for the declared child role. Wrong values and undeclared AGMSG names refuse; all four previously declared AGMSG names retain their authority and optionality. Settings env remains limited to its four original pairs. |
   523	
   524	The five allowlist classes each have an explicit fixture: unknown key, undeclared provider selector, foreign root, object-form component and non-command handler. Parameterization may share builders but must name every subcase in validation. Do not replace the three required c0f50fa1-red regressions with tests of a new validator alone.
   525	
   526	Retain all a02 regressions: old tracked settings, alternate executable fields, inherited project MCP, dedicated global state, skills-directory plugins, per-source S01-S23 coverage, sandbox-only documentation, hostile-GH_HOST templates, private caches, native denials, migration and guarded delivery. The fixture-case source inventory equals the production source inventory; each case plants its payload in the source it claims to exercise.
   527	
   528	Retain a02's red/green evidence for `env.HOME`, fenced dynamic commands and the four 79ea98a3 fixes as historical evidence. Do not claim those tests newly fail on c0f50fa1. Update the documentation template test to read the a04 task copy. Update inherited S11 sentinel-preservation/unknown-field-refusal expectations to the discard-and-regenerate contract with `projects: {}`; retain the top-level MCP tamper refusal, and do not keep the old blanket `oauthAccount` refusal or project-entry refusals.
   529	
   530	C11: every `closed` row names one exact `tests/<path>.py::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.
   531	
   532	## Change budget
   533	
   534	Changed lines mean additions plus deletions. The starting measurement is `git diff --numstat 51ba5801 c0f50fa1`, not the obsolete a01 estimate. Preserve its complete output and account separately for base-branch changes already merged into c0f50fa1. The author repeated this immutable comparison when preparing a04.
   535	
   536	For this task's allowed paths, excluding `.orchestration/`, tests and the three regenerated Claude settings templates, that command measures:
   537	
   538	| Source | Changed lines |
   539	| --- | ---: |
   540	| `.claude/settings.json` | 96 |
   541	| `.gitignore` | 1 |
   542	| `Makefile` | 6 |
   543	| `home/dot_agents/agent-config.yaml` | 60 |
   544	| `home/dot_agents/skills/agmsg-orchestration/SKILL.md` | 10 |
   545	| `home/dot_claude-worker/modify_private_settings.json` | 437 |
   546	| `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` | 65 |
   547	| `home/dot_claude/modify_private_settings.json` | 120 |
   548	| `home/dot_local/bin/common/executable_herdr-agents` | 126 |
   549	| `scripts/generate-agent-configs.py` | 181 |
   550	| `scripts/validate-agent-assets.py` | 9 |
   551	| **Measured starting source total** | **1111** |
   552	
   553	The seven allowed test modules measure respectively 103, 15, 206, 935, 104, 310 and 95 changed lines in `allowed_files` order: **1768**. The full historical-base output additionally contains already-merged unrelated source/test rows; list them rather than charging them as new a04 work or editing them.
   554	
   555	Amendment 1's read-only sizing counts 24 lines in c0f50fa1's `present`/`read_json`/`write` analogues plus 16 estimated declaration/digest/route lines, and the 42-line non-command-handler fixture plus 18 estimated content/control lines: **40 source / 60 test**. This measured analogue-based estimate is not a measured implementation result.
   556	
   557	Amendment 2's read-only AST sizing of c0f50fa1 measures `present` 8 + `read_json` 10 + `write` 6 = 24 source analogue lines, plus 56 estimated declaration/project/identity/regeneration lines: **80 source**; the global-state fixture 20 + refusal helper 36 = 56 test analogue lines, plus 64 estimated generation/identity/restart subcases: **120 test**. These are sizing analogues reused without duplication, not measured implementation results. Amendment 3 retains the **80 source** ceiling, removes project-inventory work and replaces the restart subcases with the A-then-B shared-directory sequence: the same 56 test analogue lines plus 104 estimated generation/identity/sequential-start subcase lines give **160 test**, an additional **40 test** over amendment 2. This revised estimate is not a measured implementation result.
   558	
   559	Authorize these incremental ceilings, attributed to accepted findings. These increments are estimates pending implementation measurement, not claimed measured results:
   560	
   561	| Control/finding | Additional source | Additional tests |
   562	| --- | ---: | ---: |
   563	| Closed settings/nested-value schema and sandbox extensions; S1, `local:c0f50fa:2` | 180 | 140 |
   564	| Environment/provider allowlist and credential-chain refusal; `security:c0f50fa:1` | 70 | 100 |
   565	| Validated repository root; `security:c0f50fa:2` | 25 | 60 |
   566	| Scalar inspected-file components; `security:c0f50fa:3` | 35 | 70 |
   567	| Actual enterprise skills root; `local:c0f50fa:1`, `text-security:be969e3:1` | 10 | 40 |
   568	| Handler-class/schema consistency; `text-security:b2a186e:1` | 10 | 30 |
   569	| Printed privileged parent creation; `local:c0f50fa:3` | 10 | 25 |
   570	| Post-Herdr reconciliation; `local:c0f50fa:4` | 10 | 45 |
   571	| Existing render/docs fixture alignment with the accepted re-plan | 10 | 30 |
   572	| Executable environment-file contents and launcher-written SHA256; `text-security:f7af699:1` | 40 | 60 |
   573	| Launcher-generated S11, screened identity and empty shared project state; D-024-34/D-024-35, `worker:5067ed0:1` and `text-security:efa211d:1` with `text-security:f7af699:1` as the shared family | 80 | 160 |
   574	| **Increment ceiling** | **480** | **760** |
   575	
   576	The source cap remains **1591 = 1111 + 480**; the test cap remains **2528 = 1768 + 760**, including a03 amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. The a04 non-shim interpreter, platform-injected and regime-declared controls fit the existing environment/provider and fixture-alignment increments; no cap increases. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.
   577	
   578	RESULT records final per-file numstat, historical-base and final PR merge-base identities, actual source/test totals and per-control attribution. Preserve both the complete historical comparison and the current PR comparison so merged base changes are visible.
   579	
   580	Every later amendment maps to accepted review findings and carries `previous_sha256`; the worker raises no cap. Amend Change budget, the operative C-107 Check cap sentence and the Checks block together. A measured overrun produces a blocked PONG rather than suppression or an unreviewed text edit.
   581	
   582	## Out of scope
   583	
   584	D-024-26 still assigns exact host-probed uv/Python/Node version declarations and mise pins beyond a04's narrow launch-interpreter selection, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.
   585	
   586	Keep `home/dot_mise/config.toml`, the installed state-helper source, Codex boundary sources and updater scripts outside scope. No binding-only code returns through shared files. Add no write-boundary Python hook, gh wrapper, credential-directory substitute, installation discovery or PATH fallback.
   587	
   588	P1-14 a05 and P1-6 own approval/evidence consumption. The exact operative ledger templates tested from this task copy are `gh api --hostname github.com repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha` and `gh api --hostname github.com 'repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref=<sha40>'`. Validate the returned full 40-hex SHA and use the identical SHA in the content request. Every deciding API call binds `--hostname github.com`; every deciding subcommand binds `--repo github.com/mryfmo/dotfiles`. Refuse if the host cannot be bound, without an unbound retry or local fallback.
   589	
   590	Retain `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host`: extract those two templates, substitute only the validated SHA, exercise argv without shell evaluation, export hostile `GH_HOST`, check exact hostname/repository/SHA binding and test an isolated no-gh refusal. This is a contract test, not a ledger consumer or authentication test. Local remotes, URL rewrites, refs, objects and working-copy rows establish no approval authority.
   591	
   592	The host is not a security boundary between same-UID seats. `GH_CONFIG_DIR` does not separate macOS Keychain credentials. Native merge denials remain `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`; shared credentials permit other API routes. P1-11 owns next-records-PR detection, not main-push detection or prevention. Separate-user/host prevention remains the operator's future P1-16 decision.
   593	
   594	`dotfiles-T133-agmsg-hardening-a01` owns store driver-name validation and plugin authorization. Shared administrative exceptions/socket access, external host processes, same-UID races, later configuration reloads and hook-event limitations remain residuals. Dedicated login state is not imported from the orchestrator or used to discover executable acceptance rules.
   595	
   596	Perform no live settings application, authentication/keyring/ruleset mutation, global/administrative installation, permission-policy deployment, restart or merge. Edit no canonical task, acceptance record, decision ledger, design or another task's evidence.
   597	

 succeeded in 148ms:
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


 succeeded in 166ms:
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
session id: 01a15b35-df48-7b40-8d55-77ddfacbbf2a
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
対象タスクと参照先の acceptance・review 記録を読み、各 threat row の制御が実際の実行まで拘束できるか確認します。agmsg-orchestration と Ponytail の手順を参照し、読み取り専用でレビューします。
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
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
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
   101	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees"
   102	  - control: S11 carried identity-field screening
   103	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member"
   104	  - control: <skills-root>/<name>/.claude-plugin/plugin.json
   105	    disposition: "residual: S12 includes enterprise skills at <managed-root>/.claude/skills and the other five admitted skills roots, even when the plugin is disabled."
   106	  - control: <plugins-root>/installed_plugins.json
   107	    disposition: "residual: S13 accepts only the declared registry shape and contained roots whose descriptors are read; an install record cannot add an unchecked root."
   108	  - control: <plugins-root>/known_marketplaces.json
   109	    disposition: "residual: S14 permits the declared empty registry only; refresh sources and executable header helpers have no canonical worker form."
   110	  - control: <plugin-root>/.claude-plugin/plugin.json
   111	    disposition: "residual: S15 admits declared descriptive metadata and scalar file references only; every selected file is inspected even for a disabled plugin."
   112	  - control: <plugin-hook-file>
   113	    disposition: "residual: S16 covers default and explicitly referenced hook files separately; plugin-owned executable handlers have no canonical worker operation."
   114	  - control: <marketplace-root>/.claude-plugin/marketplace.json
   115	    disposition: "residual: S17 admits descriptive metadata and an absent or empty plugin list only; command sources and additional plugin selections refuse."
   116	  - control: <plugin-mcp-file>
   117	    disposition: "residual: S18 checks default and referenced MCP files independently, admitting no nonempty worker server definitions."
   118	  - control: <managed-root>/managed-mcp.json
   119	    disposition: "residual: S19 applies the same empty-server rule independently of managed-settings precedence or administrative ownership."
   120	  - control: <skills-root>/<name>/SKILL.md
   121	    disposition: "residual: S20 inspects admitted Markdown files and frontmatter without invoking them; unknown frontmatter and inline or fenced dynamic commands refuse."
   122	  - control: <commands-root>/<name>.md
   123	    disposition: "residual: S21 reads every default or scalar-referenced command file; object mappings, inline content and directory references do not bypass Markdown inspection."
   124	  - control: <agents-root>/<name>.md
   125	    disposition: "residual: S22 inspects declared subagent metadata and refuses executable frontmatter without starting a subagent."
   126	  - control: <plugin-lsp-file>
   127	    disposition: "residual: S23 admits empty LSP configuration only; language-server commands and arguments have no canonical worker operation."
   128	  - control: pre-start refusal of unknown settings keys
   129	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys"
   130	  - control: pre-start refusal of undeclared provider selectors
   131	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors"
   132	  - control: pre-start refusal of foreign repository roots
   133	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root"
   134	  - control: pre-start refusal of object-form plugin components
   135	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components"
   136	  - control: pre-start refusal of non-command hook handlers
   137	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch"
   138	  - control: pre-start refusal of untrusted executable environment-file contents
   139	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents"
   140	  - control: manifest-selected non-shim launch interpreter
   141	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names"
   142	  - control: Darwin platform-injected launch environment
   143	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment"
   144	  - control: regime-declared launch environment
   145	    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment"
   146	  - control: plugin activation and additional executable components
   147	    disposition: "residual: explicit false entries supplement screening; higher-scope enables, sync, dependencies, workflows, monitors and undeclared components refuse before launch."
   148	  - control: non-file managed delivery and launch overrides
   149	    disposition: "residual: unenumerable MDM, server delivery, host settings and caller-selected sources refuse without running a helper to discover their content."
   150	  - control: lower-scope sandbox array merging
   151	    disposition: "residual: source-specific canonical fragments reject extra exclusions, write roots and socket grants before Claude can merge arrays; live enforcement and later changes remain unverified."
   152	  - control: actual enterprise skills root
   153	    disposition: "residual: inventory starts at <managed-root>/.claude/skills, and temporary managed-root fixtures plant both Markdown and bundled plugin payloads there on both platforms."
   154	  - control: <absolute-home>/.agents/permgate-policy.yaml
   155	    disposition: "residual: explicit static Edit denies protect the policy input and fixtures assert unchanged bytes; legacy hook environment and execution binding remain deferred."
   156	  - control: <absolute-home>/.local/lib/python*/site-packages
   157	    disposition: "residual: directory-target and descendant denies retain protection for .pth, usercustomize.py and sitecustomize.py without claiming isolated interpreter startup."
   158	  - control: <absolute-home>/Library/Python/*/lib/python/site-packages
   159	    disposition: "residual: macOS user-site directory and descendant patterns remain in the static inventory; planted-startup execution belongs to the binding task."
   160	  - control: <absolute-home>/.claude/hooks/orchestrator-only.sh
   161	    disposition: "residual: the installed guard is an explicitly protected consumed input; routing fixtures do not close concurrent same-UID path swaps."
   162	  - control: formatter and project-map configuration selection
   163	    disposition: "residual: worker and outside-anchor input paths suppress tool execution; formatter availability and complete tool-chain binding remain deferred."
   164	  - control: .orchestration/dotfiles-T133-worker-write-boundary-a03/task.md
   165	    disposition: "residual: retain the predecessor task copy and all a03 evidence unchanged in the declared retained predecessor directory; neither deletion nor new predecessor writes is authorized."
   166	  - control: .orchestration/dotfiles-T133-worker-write-boundary-a04/task.md
   167	    disposition: "residual: the a04 copy is byte-identical to the complete dispatched a04 text and bound by SHA256 in TASK and RESULT."
   168	  - control: evidence records
   169	    disposition: "residual: report, validation, sandbox, learning, autoskill and review records preserve commands and identities while distinguishing proposals from acceptance authority."
   170	  - control: task metadata
   171	    disposition: "residual: the orchestrator checks reset lineage, scope, counters, finding classes, dispatched bytes and final-head evidence without treating worker proposals as approval."
   172	  - control: metadata separators
   173	    disposition: "residual: format-2 separators delimit the metadata, and the task-copy digest covers the entire front matter and body."
   174	  - control: in-process effects
   175	    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no deployment, login, administrative installation or restart."
   176	  - control: workflow and interpreter or environment inputs
   177	    disposition: "residual: trusted parents supply clean environments and the manifest-named absolute non-shim mise Python runs isolated; role-specific runtime-name screening does not establish complete executable binding."
   178	  - control: new or renamed scripts
   179	    disposition: "residual: policy stays in the existing renderer, preparation script and guard; no new wrapper, state helper, interpreter resolver or executable-link manager is introduced."
   180	  - control: "5.14 item 0: 脅威モデル"
   181	    disposition: "residual: host controls reduce accidental and injected damage; shared credentials and same-UID processes prevent a seat-isolation claim."
   182	  - control: "5.14 item 1: 書き込み境界"
   183	    disposition: "residual: retained write policy and the closed startup schema implement this task's scope; later reloads and consumption races remain outside its guarantee."
   184	  - control: "5.14 item 2: 無害化した環境を最初に"
   185	    disposition: "residual: trusted-parent clean prefixes, fixed operations and declared environment inputs remain mandatory; the legacy orchestrator PermissionRequest and complete executable binding retain their separate owner."
   186	  - control: "5.14 item 3: 信頼パスの境界検査"
   187	    disposition: "residual: canonical root and component containment checks precede startup, including aliases; executable realpath binding remains with the binding task."
   188	  - control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す"
   189	    disposition: "residual: fixed dispatch avoids candidate-selected execution, while snapshots, last-use digests and complete executable identity remain with their consuming mechanisms."
   190	  - control: "5.14 item 5: 出力と予約の同一性"
   191	    disposition: "residual: this task introduces no reservation protocol; consuming orchestrator mechanisms retain ownership of full-head outputs and inode-bound locks."
   192	  - control: "5.14 item 6: 正直な残余"
   193	    disposition: "residual: the report retains shared credentials, administrative exceptions, socket access, agmsg sourcing, races, reloads and hook-event limitations."
   194	  - control: "5.14 item 7: 検証"
   195	    disposition: "residual: retained source-class fixtures and new allowlist regressions supply final-head evidence; shared trusted-execution helper adoption remains with P1-6."
   196	  - control: "5.14 item 8: 承認はコミット済み台帳から読む"
   197	    disposition: "residual: fixed-host ledger templates and hostile-host fixtures preserve the contract; P1-14 a05 and P1-6 own actual approval consumption."
   198	  - control: "5.14 item 9: 私設キャッシュ"
   199	    disposition: "residual: private worker caches and orchestrator-cache denies remain; exact interpreter declarations, resolver consumption and deployment binding remain separately owned."
   200	  - control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない"
   201	    disposition: "residual: the Worker Playbook permits no worker escape, while shared administrative capabilities and the operator's Codex permgate deployment remain explicit residuals."
   202	  - control: canonical GitHub API host binding
   203	    disposition: "residual: both ledger templates explicitly bind github.com and mryfmo/dotfiles; contract tests establish argv binding rather than enforcement by deferred consumers."
   204	  - control: hook failure policy
   205	    disposition: "residual: supported rendered entries retain onFailure block, but background hooks, excluded events and runtime timeout behavior establish no enforcement responsibility."
   206	  - control: agmsg store driver and plugin selection
   207	    disposition: "residual: plugin-code and trusted-plugin denies reduce one route; writable store-selected sourcing remains owned by dotfiles-T133-agmsg-hardening-a01."
   208	  - control: orchestrator effect merge
   209	    disposition: "residual: only the orchestrator integrates with final-head evidence and a pinned merge; shared credentials still permit API routes outside the native prefix denials."
   210	  - control: orchestrator effect update-branch
   211	    disposition: "residual: an update moves the head and requires fresh CI, feedback, local review, audit and security evidence before integration."
   212	  - control: orchestrator effect forced worker removal
   213	    disposition: "residual: none is planned; existing dirty-worktree protections remain and any operator-authorized discarded state must be recorded."
   214	premises:
   215	  - claim: >-
   216	      INV-6 carries three a03 amendments; plan 006 S2 requires design by another authoring context. This review-profile context supplies a04, reset_of a03, rather than another a03 amendment. Read-only rechecks on 2026-10-20 confirmed worker-e remains at c0f50fa1383416240ad28959dbc4635afa777175 on tools/worker-write-boundary-a01. Keep PR #431 and the uncommitted a03 implementation/test draft. The canonical a03 text and retained worker task copy both hash to 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b.
   217	    sources:
   218	      - .orchestration/plans/006-regime-v3-execution.md
   219	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
   220	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
   221	    executed_commands:
   222	      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" rev-parse HEAD', output: 'c0f50fa1383416240ad28959dbc4635afa777175'}
   223	      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" symbolic-ref --short HEAD', output: 'tools/worker-write-boundary-a01'}
   224	      - {command: 'shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md', output: 'both files: 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b'}
   225	  - claim: >-
   226	      The blocked PONG reports probe exit 0, test exit 1, zero worker correction rounds and zero independent pre-push reviews. Its green-new.log is a failing uncommitted draft: 15 tests, 45 failures, including undeclared runtime names, noncanonical TMPDIR and unreconciled fake-update hooks; it is not a RESULT or final green evidence. Retain it without relabeling.
   227	    sources:
   228	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
   229	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log
   230	  - claim: >-
   231	      runtime-contract-probe.json supplies the exact name lists below. Read-only repetition at 2026-10-20T14:57:54Z produced the same names, exit statuses and spawn digest, without a live worker or private settings. The manifest currently lacks the non-shim interpreter declaration; a04 must add it within its existing launcher policy, not discover it through PATH.
   232	    sources: [.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json]
   233	    repeated_probe:
   234	      supplied_environment_names: [HOME, LANG, PATH, TERM]
   235	      child_code: 'import os,json,pathlib,platform,pwd,tempfile,subprocess;print(json.dumps(sorted(os.environ)))'
   236	      interpreters:
   237	        - command: '/usr/bin/python3 -I -c <child_code>'
   238	          exit: 0
   239	          observed_names: [CPATH, HOME, LANG, LIBRARY_PATH, MANPATH, PATH, SDKROOT, TERM, __CF_USER_TEXT_ENCODING]
   240	          unlisted_names: [CPATH, LIBRARY_PATH, MANPATH, SDKROOT, __CF_USER_TEXT_ENCODING]
   241	          stderr: "python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead"
   242	        - command: '"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" -I -c <child_code>'
   243	          exit: 0
   244	          observed_names: [HOME, LANG, PATH, TERM, __CF_USER_TEXT_ENCODING]
   245	          unlisted_names: [__CF_USER_TEXT_ENCODING]
   246	          stderr: ""
   247	      upstream_spawn_sha256: 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731
   248	      upstream_spawn_line: 527
   249	      upstream_spawn_text: "  echo 'export AGMSG_SPAWNED=1'"
   250	      schema_has_AGMSG_SPAWNED: false
   251	      live_worker: false
   252	      private_settings_read: false
   253	  - claim: >-
   254	      The complete c0f50fa1 security review found AWS credential-chain selectors, a foreign-repository main-local inventory gap and object-form plugin command mappings. The local review found the incorrect enterprise skills root, lower-scope sandbox extensions, missing privileged parent creation and post-Herdr settings drift. The local chain stopped before a task-level audit; none exists for c0f50fa1. Repeated renderings in the local report are four findings, not additional independent findings.
   255	    sources:
   256	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
   257	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
   258	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
   259	  - claim: >-
   260	      D-024-26 retains the write boundary and transfers executable binding. D-024-29 freezes design 5.14; D-024-30 applies it by reference. The 2026-10-20 residual-list entry in this text records the allowlist generalisation without reopening the frozen items.
   261	    sources:
   262	      - .orchestration/decisions.tsv
   263	      - $HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md
   264	  - claim: >-
   265	      The inherited read-only version observation is Claude Code 2.1.300. Documentation enumerations fetched at 2026-10-19T20:41:53Z were: settings scopes User, Shared project, Project local, Managed; precedence Managed settings, Command line, Project local settings, Shared project settings, User settings; MCP scopes Local, Project, User; hook types command, http, mcp_tool, prompt, agent; plugin origins @<marketplace>, @inline, @skills-dir, @synced; plugin enablement sources --add-dir, user, project, local, flag, managed; skills roots Enterprise, Personal, Project, Nested, Additional directory, Plugin; account-synced roots remain undeclared. Recheck the installed version and loader before changing implementation.
   266	    fetched_at: "2026-10-19T20:41:53Z"
   267	    sources:
   268	      - https://code.claude.com/docs/en/settings
   269	      - https://code.claude.com/docs/en/hooks
   270	      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
   271	      - https://code.claude.com/docs/en/plugins/loading
   272	      - https://code.claude.com/docs/en/skills
   273	  - claim: >-
   274	      C-87 inherited observation: the orchestrator observed the documented ["Where skills live" table](https://code.claude.com/docs/en/skills) at 2026-10-20T04:47:57Z and the read-only loader probe at 2026-10-20T04:50Z. The Enterprise row says "`.claude/skills/<skill-name>/SKILL.md` in the managed settings directory", with Linux example `/etc/claude-code/.claude/skills/<skill-name>/`. The pinned 2.1.300 loader, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3, contains `/.claude/skills/` (11 occurrences), `.claude/skills/` (8), `/etc/claude-code` (6) and `/Library/Application Support/ClaudeCode` (3); the historical supplied probe excerpt is `LC_ALL=C /usr/bin/grep -a -o -E '…(\.claude/skills|/skills"|skills/)…' <loader> | sort | uniq -c`. These observations bind the enterprise inventory and fixture to `<managed-root>/.claude/skills`.
   275	    sources: ["https://code.claude.com/docs/en/skills", ".orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md"]
   276	  - claim: "Worker a010 blocked before any edit (PONG 2694, 2026-10-20T04:00:43Z): the loader persists numStartups at start and hasCompletedOnboarding at onboarding; the orchestrator reproduced the installed-loader probe below, not a live worker start."
   277	    sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md]
   278	    probe: {executed_by: review-profile-author, executed_at: "2026-10-20T14:57:54Z", loader: "$HOME/.local/share/mise/installs/npm-anthropic-ai-claude-code/2.1.300/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe", format_observed: Mach-O arm64}
   279	    executed_commands:
   280	      - {command: 'shasum -a 256 <loader>', output: '475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3  <loader>'}
   281	      - {command: '<loader> --version', output: '2.1.300 (Claude Code)'}
   282	      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o numStartups <loader>', output: '12'}
   283	      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o hasCompletedOnboarding <loader>', output: '15'}
   284	    quoted_string_probes: [{command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"numStartups"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasCompletedOnboarding"'' <loader>', output: '0'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasTrustDialogAccepted"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"oauthAccount"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"mcpServers"'' <loader>', output: '29'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"enabledMcpjsonServers"'' <loader>', output: '5'}]
   285	  - claim: >-
   286	      The single source inventory is S01-S23 below plus executable environment-file contents admitted by the launch-input schema. Each parameter denotes every actual matching file, inspected independently before merging. User means the dedicated configuration directory; managed-root is the platform directory containing managed-settings.json. S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json; S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery; S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration; S12 each skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json; S16 every default hooks/hooks.json and explicitly referenced plugin hook file; S17 every admitted marketplace-root/.claude-plugin/marketplace.json; S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file; S22 every applicable subagent Markdown file; S23 every default or referenced plugin LSP file. Non-file managed delivery and caller-selected inputs must fit the same closed schema and read set or cause a named refusal.
   287	    sources:
   288	      - https://code.claude.com/docs/en/settings
   289	      - https://code.claude.com/docs/en/managed-settings
   290	      - https://code.claude.com/docs/en/server-managed-settings
   291	      - https://code.claude.com/docs/en/plugins/manifest-reference
   292	      - https://code.claude.com/docs/en/skills
   293	---
   294	
   295	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a04 — plan 024 P1-15; worker startup screen; seat a010
   296	
   297	## Goal and reset
   298	
   299	[memory:decision] Reset a03 under INV-6 and plan 006 S2 through this separate review-profile authoring context. Worker a010 is Codex, security profile, in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`; this task changes Claude's boundary and preserves Codex policy. Continue `tools/worker-write-boundary-a01` and PR #431 from `c0f50fa1383416240ad28959dbc4635afa777175`, keeping the uncommitted a03 draft and all predecessor evidence; open no second PR.
   300	
   301	Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Retain every a03 item and fix, with only the runtime/interpreter decision specified here.
   302	
   303	[memory:failure] a01 and a02 each spent two worker rounds; a03's blocked PONG reports zero worker correction rounds and zero independent pre-push reviews, while its amendment history remains counted. This reset supplies a04 at most two worker correction rounds in total, including pre-push corrections, and at most one independent pre-push review; it erases no predecessor counters or findings.
   304	
   305	The retained draft is not approved, and its `raw/green-new.log` is explicitly failing. The c0f50fa1 local chain stopped before its task-level audit. Obtain new final-head audit and security evidence; do not describe either as inherited.
   306	
   307	## History
   308	
   309	a01 and a02 each exhausted their two worker rounds, and a03 reset the lineage to a closed startup schema while continuing PR #431. Its amendments bound executable environment-file contents, regenerated S11 with screened identity and empty shared project state, and corrected the enterprise skills inventory; those controls and their finding history remain. The worker blocked on shim/platform-added runtime names and upstream `AGMSG_SPAWNED=1`, preserving its uncommitted draft and failing evidence. INV-6's three counted a03 amendments trigger plan 006 S2, so another context authors a04 to resolve only that runtime-name/interpreter contract instead of extending a03.
   310	
   311	## Design and finding history
   312	
   313	Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 by reference, including its residual list. D-024-29 keeps items 0-10 frozen; D-024-30 narrows C-88 to exact contract sentences asserted by tests.
   314	
   315	Item 1 applies to dedicated worker settings, static input-derived write protection and refusal before startup.
   316	Item 2 applies to trusted-parent execution, clean environments and fixed command selection.
   317	Item 3 applies to canonical anchor, worktree and component identities before consumption.
   318	Item 8 applies to committed approval authority through explicitly host-bound repository API calls.
   319	Item 9 applies to private caches and the trusted parent's interpreter/cache inputs.
   320	
   321	**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a04:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.
   322	
   323	Read the full a02 and a03 acceptance records, a03 task, blocked PONG and both runtime evidence files, and both c0f50fa1 reviews named in `premises:`. Retain the following history and finding classes in the a04 report and acceptance lineage:
   324	
   325	| Finding | Class | Required treatment |
   326	| --- | --- | --- |
   327	| `text-security:2ae9e2c:1` | input-inventory | Project `.mcp.json` remains independently screened. |
   328	| `text-security:ebbb71b:1` | input-inventory | Skills-directory plugins remain inventoried even when disabled. |
   329	| `text-security:ebbb71b:2` | input-inventory | Dedicated global state regenerates `mcpServers: {}` and `projects: {}`; native project entries are discarded. |
   330	| `text-security:ebbb71b:3` | repository-binding | Canonical main comes from the fixed repository API. |
   331	| `text-security:b2a186e:1` | input-inventory | Inspect handler type before command; non-command types refuse. |
   332	| `text-security:b2a186e:2` | repository-binding | Both ledger calls bind `--hostname github.com`. |
   333	| `text-security:ac9ce14:0` | correct | Historical text approval only; it does not approve a04. |
   334	| a02 independent pre-push review | input-inventory | Retain fixes for `env.HOME` guard selection and fenced dynamic commands. |
   335	| `local:79ea98a:1` | tool-environment | Retain manifest-generated `--advisor fable` acceptance. |
   336	| `local:79ea98a:2` | tool-environment | Retain absolute tool paths and attachment identity environment. |
   337	| `local:79ea98a:3-4` | partial-fix | Retain custom-hook preservation and legacy PreToolUse migration. |
   338	| `security:c0f50fa:1` | input-inventory | Refuse undeclared credential-chain/provider selectors. |
   339	| `security:c0f50fa:2` | input-inventory | Refuse worker starts for repositories other than the validated anchor. |
   340	| `security:c0f50fa:3` | input-inventory | Refuse object and inline plugin/command components. |
   341	| `local:c0f50fa:1` | tool-environment | Inventory enterprise skills under the actual managed root. |
   342	| `local:c0f50fa:2` | tool-environment | Reject lower-scope sandbox extensions before array merging. |
   343	| `local:c0f50fa:3-4` | partial-fix | Fix printed parent creation and post-installer reconciliation here. |
   344	| `text-security:f7af699:1` | input-inventory | Admit executable environment-file contents only when absent, empty or launcher-generated for this start. |
   345	| `worker:5067ed0:1`, `text-security:efa211d:1` | input-inventory | Regenerate S11 at every start with `projects: {}` and screened identity; discard native persisted state, including every project's state, and use the launcher's existing spawn-readiness trust-dialog acceptance. |
   346	| `text-security:be969e3:1` | input-inventory | Inventory enterprise skills and plant both Markdown and bundled plugin fixtures under `<managed-root>/.claude/skills`, following the C-87 documented table and pinned-loader probe. |
   347	
   348	S1 first triggered on the three source omissions in 2ae9e2c/ebbb71b. The re-plan enumerated S01-S23, but subsequent findings still exploited open field/value acceptance; the c0f50fa1 security findings bring that post-re-plan family to its sixth finding. This reset changes the approach rather than adding three more denylist entries.
   349	
   350	Preserve the advisory-owner history and owner `dotfiles-T133-worker-write-boundary-followup-a01` exactly as history. The two c0f50fa1 P2 fixes are retained from a03 by this text; the orchestrator reconciles their owner rows and updates dependent task references. The worker edits no canonical acceptance or owner task.
   351	
   352	Retain D-024-26's transferred binding findings, including `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. Do not relabel them as fixed.
   353	
   354	## Closed startup schema
   355	
   356	Declare this schema in `home/dot_agents/agent-config.yaml` and expose it through the existing renderer/preparation code. Candidate files, Git objects and installed upstream schemas never define their own acceptance policy. Add no new helper, generated output file or dependency.
   357	
   358	The schema below is exhaustive for data forwarded to the loader. Objects reject unknown keys at every level, including nested objects and records that would otherwise be preserved; S11 fields designated for discard are not screened or preserved. Reject duplicate JSON keys, wrong types, Boolean/integer substitutions, unreadable inputs and unsupported forms. Missing optional fields may pass; a present field must match its declared source-specific form.
   359	
   360	### Settings and values
   361	
   362	The only settings keys are `permissions`, `sandbox`, `hooks`, `env`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `enabledPlugins`, `syncClaudeAiPlugins`, `syncClaudeAiSkills`, `extraKnownMarketplaces` and `disableSkillShellExecution`.
   363	
   364	| Node | Accepted shape and values |
   365	| --- | --- |
   366	| `permissions` | Only `defaultMode`, `deny`, `additionalDirectories`; `defaultMode` is `auto` where applicable; `additionalDirectories` is `[]`; `deny` is a renderer-declared worker/native-denial fragment for that source. No caller-added allow/ask rule or alternate permission mode. |
   367	| `sandbox` | Only the keys emitted by the worker or administrative renderer: `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands`, `excludedCommands`, `filesystem`, `network`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `allowAppleEvents`. |
   368	| `sandbox.filesystem` | Only `allowWrite`, `disabled`; exact source-specific canonical values. Worker write grants are the four declared agmsg stores; ordinary worktree/cache writes remain provided by the worktree boundary. |
   369	| `sandbox.network` | Only `allowedDomains`, `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`; exact source-specific canonical values. |
   370	| Sandbox lists and Booleans | Every present leaf/list equals the canonical worker fragment in S01-S04 or administrative fragment in S05-S07. Worker exclusions are empty; additional write roots/sockets are refused. Only administrative sources may contain the exact shared three exclusions and single Herdr socket. |
   371	| `hooks` | Only source/event/matcher/operation combinations generated by the trusted renderer or delivery constructor. Groups have only `matcher`, `hooks`; handlers have only renderer-declared `type`, `command`, `timeout`, `async`, `statusMessage`, `onFailure`, with exact canonical values. |
   372	| Handler type | Only the string `command`; validate it before reading `command`. HTTP, MCP-tool, prompt, agent, unknown, missing, null and non-string types refuse. |
   373	| MCP approval fields | `enableAllProjectMcpServers: false`; `enabledMcpjsonServers: []`; `disabledMcpjsonServers: []` when present. Approval state never exempts a server definition. |
   374	| Plugin fields | `enabledPlugins` maps only manifest-known or inventoried plugin identities to `false`; both sync fields are `false`; `extraKnownMarketplaces` is `{}`. |
   375	| Skill execution | `disableSkillShellExecution`, when present, is `true`. |
   376	| `env` | Only the four exact name/value pairs in the next subsection; arbitrary strings, maps and provider credentials are not preserved. |
   377	
   378	Absent or empty settings objects pass where the source permits them. Administrative drop-ins/cache may contain canonical partial objects; partial means omitted declared fields, never new fields or alternate values. Validate each list before merging so an empty generated worker list cannot conceal a broader lower-scope array.
   379	
   380	There is no canonical worker setting for helpers, status-line commands, wrappers, alternate sandbox executables, policy helpers or authentication refresh/export commands. Their keys refuse as undeclared, including misplaced forms. The orchestrator managed PermissionRequest exception is not a worker-start exception.
   381	
   382	The old instruction to preserve unrelated non-executable state now applies only to fields admitted by this schema. Unknown settings refuse without deletion or normalization; S11 alone discards pre-existing fields outside its declared structures and carried identity, without screening or forwarding them.
   383	
   384	### Environment and launch arguments
   385	
   386	Settings `env` admits exactly `GH_TELEMETRY="false"`, `DO_NOT_TRACK="1"`, `CHECKPOINT_DISABLE="1"` and `AWS_EC2_METADATA_DISABLED="true"`, as declared by the manifest. The last name is the sole declared `AWS_*` exception and cannot select credentials or a provider.
   387	
   388	The launch-input schema classifies names by source: existing parent/runtime declarations, `regime-declared`, and `platform-injected`. The latter two classes below are closed enumerations, not prefixes. They do not extend settings `env`, configuration-file keys or CLI arguments.
   389	
   390	The launcher and its startup/preflight Python children use only the manifest-named absolute mise-installed non-shim interpreter, observed here as `<validated-home>/.local/share/mise/installs/python/3.15.0/bin/python3.15`. Add that narrow declaration to the existing manifest-owned launcher policy and consume it through the existing renderer; never route through `/usr/bin/python3`, a mise shim, PATH lookup or an interpreter-discovery fallback. Cover startup bootstrap/home lookup as well as preparation. This selects the interpreter for this boundary without returning the deferred complete binding work to scope.
   391	
   392	The launch-input schema admits only these names, with source-specific values supplied or checked by the trusted parent:
   393	
   394	| Names | Value authority |
   395	| --- | --- |
   396	| `HOME`, `PATH`, `LANG`, `TERM` | Validated passwd home; prescribed system-only child PATH; `C.UTF-8`; declared terminal value. Hook children retain `TERM=dumb`. |
   397	| `TMPDIR` | Canonical trusted temporary directory supplied by the parent, not a candidate configuration root. |
   398	| `CLAUDE_CONFIG_DIR` | Exactly the dedicated worker directory under the validated home. |
   399	| `CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` | Parent-bound canonical project identity and runtime shell file; `CLAUDE_ENV_FILE` additionally requires the executable-content control below. |
   400	| `UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR` | Exactly `<canonical-worktree>/.uv-cache` and its `python` child. |
   401	| `regime-declared`: `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE`, `AGMSG_AGENT_PID` | Retain a03's exact authorities: `0`, validated launcher store selection, declared monitor value and numeric runtime process identifier; unset default-store selection remains supported. |
   402	| `regime-declared`: `AGMSG_SPAWNED` | Exactly the string `1`, set by upstream `spawn.sh` on the launch surface before the worker CLI; require it on spawn-launched roles and do not synthesize it for unrelated child roles. |
   403	| `platform-injected`: `__CF_USER_TEXT_ENCODING` | Darwin only; present or absent allowed. A present string must full-match `0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+`. The regime validates the shape and otherwise never reads or uses it. Linux presence refuses. |
   404	| `HERDR_ENV`, `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_AGENTS_LAYOUT`, `HERDR_SOCKET_PATH` | Validated control-plane identity, `managed` layout and canonical configured socket; these grant no worker sandbox exception. |
   405	| `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID` | Parent/runtime session identifier and numeric process identifiers where required by canonical attachment/delivery. |
   406	| `CLICOLOR_FORCE`, `FORCE_COLOR` | Launcher-written `1` only where the launch route uses them. |
   407	| `GH_TELEMETRY`, `DO_NOT_TRACK`, `CHECKPOINT_DISABLE`, `AWS_EC2_METADATA_DISABLED` | The four fixed values above. |
   408	| `CHEZMOI_SOURCE_DIR`, `CHEZMOI_HOME_DIR` | Preparation-only trusted source/home bindings; not caller-selected worker configuration or executable roots. |
   409	
   410	The read-only amendment-1 probe of the [documented environment variables](https://code.claude.com/docs/en/env-vars) identifies `CLAUDE_ENV_FILE` as the only name admitted above that selects a file whose contents execute: Claude runs its shell contents before Bash commands. No other admitted name has that documented role; `CLAUDE_CODE_SHELL` and `CLAUDE_CODE_SHELL_PREFIX` remain undeclared. Include the named file's contents in the preflight read set alongside S01-S23.
   411	
   412	For every admitted executable-content file variable, preflight accepts its named file only when absent, empty, or byte-identical to canonical contents generated by the launcher for this start. Inspect without sourcing or executing it; unreadable/nonregular files and any other contents refuse before trust, migration, regeneration, hooks or worker commands with `worker startup refused: <file>: <variable>: noncanonical executable environment file contents`. Preserve refused bytes; never overwrite a planted file to make it pass. After all preflight checks pass, the launcher itself writes the canonical runtime-file contents, records SHA256 bound to the variable, canonical file and this start in existing startup state/evidence, and verifies those bytes before forwarding. Candidate-supplied or prior-start digests cannot authorize contents. Reuse the existing runtime file and startup state; add no sidecar, helper or generated configuration output. Later replacement races and reloads retain their existing residual owners.
   413	
   414	Validate proposed worker configuration inputs before forwarding them. A clean child environment contains only the names declared for that child role; do not inherit the caller environment wholesale. Unknown proposed environment names refuse rather than becoming an unchecked pass-through. Existing profile/control-plane variables used to select a worker are consumed through their existing manifest-owned interfaces, not forwarded as arbitrary worker settings.
   415	
   416	Every `CLAUDE_CODE_USE_*`, `AWS_*`, `ANTHROPIC_*`, `*_API_KEY`, `*_TOKEN` and `*_PROFILE` name refuses unless explicitly declared above with its exact allowed value. In particular refuse `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE` in settings and launch inputs before any credential lookup or helper execution. Add no AWS configuration parser.
   417	
   418	No shell/interpreter startup or loader override is declared: `BASH_ENV`, `ENV`, `NODE_OPTIONS`, `NODE_PATH`, `PYTHON*`, `LD_*`, `DYLD_*`, shell wrappers and alternate configuration/cache roots refuse as worker inputs. Do not print their values.
   419	
   420	Preserve the manifest-generated Claude argument interface: only `--model`, `--effort`, `--advisor` with their declared profile values, including `--advisor fable`. Caller-added settings, MCP, plugin, agent and additional-directory arguments refuse. Keep existing Codex arguments and network/shared-Git policy unchanged.
   421	
   422	A clean-parent probe runs through the interpreter named by the rendered manifest, imports the same modules as the predecessor probe, and asserts `CPATH`, `LIBRARY_PATH`, `MANPATH` and `SDKROOT` are absent. They remain undeclared and refuse if encountered; do not delete them to conceal an unexpected injection. Test the observed child environment as well as the parent's proposed names, with child-role-specific declarations.
   423	
   424	Any other new name, source, required state field or interpreter mismatch still blocks and re-tasks. Send a blocked PONG naming the boundary, exact command and status, with probe JSON containing the supplied/observed name lists, undeclared names and interpreter identity under the a04 evidence directory. Preserve the predecessor JSON unchanged. No wildcard, prefix-wide acceptance, candidate-learned schema, suppression or default-as-authorization is allowed; print no environment values.
   425	
   426	### Sources, roots and component forms
   427	
   428	The sole repository anchor is the manifest declaration resolving to `$HOME/Workspace/dotfiles`. Bind its identity to the validated passwd home and actual main checkout, resolving symlinks and filesystem case aliases. Worker roots must be registered linked worktrees beneath that anchor's declared `.claude/worktrees/` root with the same Git common directory.
   429	
   430	Every worker launch route, for either worker kind, refuses another repository before worktree creation, identity registration, hook writes, workspace trust or spawn. The refusal names this task: `worker startup refused: dotfiles-T133-worker-write-boundary-a04: unsupported repository root`. Do not fix the foreign-root finding by inspecting the fixed anchor while launching elsewhere.
   431	
   432	Admitted configuration roots are the dedicated worker directory, the validated anchor/worktree `.claude` directories, applicable nested worktree and additional-directory `.claude` directories, the platform managed root and contained plugin roots discovered through the declared registry. Inherited MCP files are the independently enumerated ancestor read set. No account-synced, inline, seed, alternate cache or caller-selected root is admitted; caller-added additional-directory arguments remain refused.
   433	
   434	The admitted skills roots are exactly Enterprise `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), Personal `<absolute-home>/.claude-worker/skills` under the dedicated configuration directory, Project `<project>/.claude/skills`, Nested `<subdir>/.claude/skills`, Additional directory `<add-dir>/.claude/skills` under an applicable `--add-dir` directory, and Plugin `<plugin>/skills`. Inspect both `<skills-root>/<name>/SKILL.md` and bundled `<skills-root>/<name>/.claude-plugin/plugin.json`. Managed command/agent locations likewise start at the actual managed root. Resolve every selected path and refuse containment escapes, unsupported aliases, missing references or unreadable files.
   435	
   436	| Source form | Closed acceptance |
   437	| --- | --- |
   438	| S08-S10, S18-S19 | Objects containing only absent or empty `mcpServers`/`managedMcpServers` maps. No server, including remote-only definitions, is canonical here. |
   439	| S11 global state | At every start, after all preflight checks pass and before any loader/worker command, write the existing `CLAUDE_CONFIG_DIR/.claude.json` from scratch: `mcpServers: {}`, `projects: {}` and `hasCompletedOnboarding: true`, plus screened identity fields below. The generated file carries no per-project inventory or pre-generated workspace trust. Never merge the previous file into this output. |
   440	| S11 pre-existing structures and identity | The existing file must be a JSON object. Missing optional retained fields pass and generated fields are written anew. Present top-level `mcpServers` must be `{}`. Carry optional `oauthAccount` only as an object with string-only members from this documented fixed set: `accountUuid`, `emailAddress`, `organizationUuid`, `displayName`, `fullName`, `organizationRole`, `workspaceRole`; declare the same set in the manifest and fixtures. Carry optional `userID` only as a string matching `^[0-9a-f]{64}$`, the installed loader's hex form. Undeclared identity members, non-string `oauthAccount` members, invalid identity values and a nonempty or malformed top-level MCP map refuse with `worker startup refused: <state-file>: <offending-key>: <named reason>` before any command or mutation, preserving refused bytes. Nonempty top-level servers use the exact reason `noncanonical global state` as tamper evidence. |
   441	| S12/S15 plugin descriptor | Only `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and the component keys `hooks`, `mcpServers`, `lspServers`, `commands`, `agents`, `skills`. Descriptive fields are strings, keywords are strings, and author has only string `name`, `email`, `url`. |
   442	| Component references | Each present component is one scalar string referencing a regular file within its admitted root. The screening reads that file under its source schema before accepting it. Arrays, objects, inline content, URLs and explicit directory references refuse. Default component directories are independently expanded into inspected files. |
   443	| S13 installed registry | Only `version: 2` and `plugins`; plugin IDs map to record lists with only `scope`, `installPath`, `version`, `installedAt`, `lastUpdated`, `gitCommitSha`, `projectPath`. Scope is user/project/local; paths are contained and project-bound; descriptive fields are strings and a present commit is 40 hex. Every referenced descriptor is read and every discovered ID is disabled. |
   444	| S14 marketplace registry | Only `{}`; no refresh source or executable header helper is canonical. |
   445	| S16 hook file | Only an absent/empty `hooks` object; plugin-owned handlers have no canonical worker operation. |
   446	| S17 marketplace descriptor | Only descriptive `name`, `owner`, `metadata`, `plugins`; owner has string name/email, metadata has string description/version, and plugins is absent or `[]`. Additional plugin selections refuse. |
   447	| S20-S22 Markdown | Plain text with the existing restricted frontmatter grammar: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model. Booleans are Boolean, model/tool selections are manifest-declared values, and unknown/nested executable forms refuse. Dynamic shell expansion, including fenced forms, refuses everywhere. |
   448	| S23 LSP | Only `{}`; command/args definitions are not canonical. |
   449	| Non-file managed inputs | Enumerated canonical administrative data only; otherwise refuse with the managed source name before executing any helper or starting Claude. |
   450	
   451	For S11, every other pre-existing top-level field, including the entire `projects` value and all its contents, `numStartups`, prior onboarding state, tips/changelog caches, project `history`, `allowedTools` and cost counters, is neither screened nor preserved; only syntax/duplicate-key/readability checks apply to the whole input. Discarded objects and arrays are never recursively screened or forwarded. Generate onboarding anew and `projects: {}`, preserve only screened identity values, and reuse the existing atomic writer after the complete preflight; the loader regenerates native state. The anchor's workspace trust is established by the launcher's existing acceptance of the workspace-trust dialog during spawn's readiness wait (`herdr-agents --add-worker` for a Claude worker, documented in the SKILL's 'Regime activation and progress' section). All Claude workers share `CLAUDE_CONFIG_DIR` at `$HOME/.claude-worker`; discarding the prior `projects` value lets sequential sibling starts succeed. A loader requiring another preserved field blocks and retasks rather than widening silently.
   452	
   453	These restrictions also apply to disabled plugins and shadowed sources. Do not recursively ignore an unknown object because it lacks a familiar executable key. A plugin `commands` mapping containing `{"source": ...}` or inline `content` refuses at the selecting file/key.
   454	
   455	## Implementation and retained controls
   456	
   457	1. Keep one preflight over S01-S23, admitted executable environment-file contents and the closed schema. Every Claude route calls it before workspace trust, migration, normalization, regeneration or execution. Enumerate through the filesystem, including ignored/untracked inputs; neither Git tracking nor a nearer definition removes a source. Inspect implicit and selected components separately without executing helpers, installing packages, fetching plugins or starting servers.
   458	
   459	2. Refusals identify the actual source and key/class without printing payloads, environment values, URLs with credentials or authentication material. Preserve the handler message `worker startup refused: <source-file>: hooks.<event>[<group-index>].hooks[<handler-index>]: noncanonical hook handler`, with zero-based indices. Other refusals use `worker startup refused: <source>: <key>: <named reason>`. Unknown settings, selectors, roots, components and source forms each receive a named reason.
   460	
   461	3. Retain exact recognized legacy-delivery classification, including canonical project binding. First screen every source; only after complete success migrate recognized owned entries, validate the prepared result under the same schema, then write. Unknown content outside S11's discard partition refuses without changing any pre-existing bytes; successful S11 regeneration intentionally replaces discarded state only after every source passes. Never rewrite tracked settings or create a local file merely for migration. Keep repeated preparation and delivery-tool-unavailable behavior.
   462	
   463	4. Retain dedicated `CLAUDE_CONFIG_DIR`, both private cache variables on every actual worker route, `AGMSG_RESOLVE_PROJECT=0`, validated `AGMSG_STORAGE_PATH`, canonical attachment identity and `onFailure: "block"` where supported. A writable `run/proj.<pid>.project` cannot replace the explicit project identity. Preserve the a02 absolute Herdr/jq/Node/npm/Codex calls and attachment environment; fixed PATH must not regress attachment or default seating.
   464	
   465	5. Keep static `trusted_paths` derived from trusted executable inputs, not Git trees/indexes. Preserve anchored source/control paths, tracked/main-local settings, `.orchestration`, both `.agents/worklog/**` and `.agents/worklog/uv-cache/**`, worktree `.claude` directory/descendant targets and `.mcp.json`. Ordinary worktree source and private cache writes remain available.
   466	
   467	6. Retain explicit protection of `<absolute-home>/.agents/agent-config.yaml`, model profiles, permgate policy, skill scripts/SKILL files, agmsg plugin code and `db/trusted-plugins`, `<absolute-home>/.claude/**`, `<absolute-home>/.claude-worker/**`, installed guard, local wrappers/application code, configuration/state/tool installations and shared uv caches. Keep directory and descendant user-site protection for `.pth`, `usercustomize.py` and `sitecustomize.py` on both platforms. Add no blanket `<absolute-home>/.agents/**` or `<absolute-home>/.local/**` deny: agmsg `db`, `teams`, `run`, `ext-tools` stay writable except `db/trusted-plugins`.
   468	
   469	7. Retain separate orchestrator, worker and administrative renders. Worker policy keeps `defaultMode: auto`, sandbox startup failure, disabled unsandboxed requests, empty user exclusions, restricted writes, no user Herdr socket, explicit MCP auto-approval disables, account sync off and false plugin entries including discovered `@skills-dir` identities. Empty maps alone do not disable plugins or replace screening.
   470	
   471	8. Administrative settings retain enabled sandboxing, `failIfUnavailable: true`, disabled unsandboxed requests, filesystem enforcement, disabled weaker isolation/Apple Events/all-socket/local-binding switches, exactly the Herdr socket, and exactly these ordered exclusions: `agmsg-dispatch *`, `herdr-agents *`, `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These shared capabilities remain available to every Claude seat and authorize no worker escape. Lower-scope canonical validation rejects extra exclusions, writes or sockets before array merging.
   472	
   473	9. Keep the orchestrator managed PermissionRequest command's existing literal bytes unchanged, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.
   474	
   475	10. Apply design 5.14 by reference for trusted-parent execution, Python isolation and Git inspection. Consume the manifest-named non-shim interpreter specified above on every launcher startup/preflight Python route; add no resolver, helper, private executable directory, PATH fallback or broader version-pin work. Do not execute arbitrary task-body shell strings as probes.
   476	
   477	11. Preserve guard routing, fixed payload paths, argument boundaries, stdin and child status. Canonical worker/sibling/unrelated/missing launch identities execute no orchestrator project payload. Only fixed installed worker-delivery operations run for workers. Formatter/map operations also reject worker/outside-anchor tool inputs. Keep tracked settings portable and all existing event/validator markers.
   478	
   479	12. Preserve managed SessionStart/PostToolUse/PreToolUse migration, custom-hook ordering, mixed entries, escaped-tilde distinctions, stale replacement and idempotence. For `make update`, reconcile the managed Claude settings after `scripts/update-agent-assets.sh` runs Herdr's installer, using the allowed Makefile/merge/renderer surfaces. Do not edit the updater script or import its unguarded hook as canonical. Verify one effective guarded hook and no managed-settings drift after repeated fake updates.
   480	
   481	13. `install-managed-settings` still stages `<absolute-home>/.claude/managed-settings.rendered.json` nonprivileged. Print a quoted privileged `mkdir -p` for the detected administrative parent before the existing quoted `sudo install -m 0644` command. Cover both platform destinations and homes containing spaces. Execute neither privileged command; do not install, log in or restart.
   482	
   483	14. Keep all existing validator checks, exact three-entry exclusion fixtures on both platforms, legacy PermissionRequest validity, duplicate-hook checks, ordering/timeouts, freshness, portability and secret/home-path scanning. Add no bound-PermissionRequest mode. `.gitignore` retains `.uv-cache/` as this task's only addition.
   484	
   485	15. Worker Playbook step 4 retains this exact test-asserted sentence:
   486	
   487	> Complete every worker command, including gh, git push and authenticated git fetch, inside the sandbox and allowlist without forbidden actions or escalation; anything that cannot complete there is `AGMSG-PONG v1 status=blocked` naming the exact command and boundary.
   488	
   489	The entire Worker Playbook, including steps 2, 5 and 11, authorizes no exception. Evidence-sync writes/masking, CompactionDB consolidation and agmsg-dispatch control-plane exemptions remain orchestrator-only. Workers write required relative evidence in their own worktree; the orchestrator copies it before acceptance. Preserve merged documentation changes and run the complete documentation module.
   490	
   491	## Regression fixtures
   492	
   493	Write the new tests before implementation. Use the existing temporary-HOME, managed-root, linked-worktree and fake-launcher builders. Tests execute no payload, credential helper, HTTP endpoint, server, plugin, subagent or live worker.
   494	
   495	Each refusal fixture asserts the source/key or named root message, unchanged existing bytes, no migration/regeneration, no trust acceptance, no spawn and absent execution/request markers. Positive absent/canonical controls and repeated starts remain covered.
   496	
   497	| Selector | Required coverage |
   498	| --- | --- |
   499	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees` | Red on c0f50fa1, green after: sequentially start registered linked-worktree workers A then B on one shared `CLAUDE_CONFIG_DIR`. A's start leaves the regenerated file; simulated loader writes then add A's project entry with a `history` list. B's start succeeds and, before its first command, leaves exactly the regenerated file with `projects: {}` and screened identity. Replace any planted-project-key refusal and same-worktree restart fixture with this cross-worktree sequence. |
   500	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_global_state_with_screened_identity` | Red on c0f50fa1, green after: pre-existing S11 has `numStartups: 5`, `hasCompletedOnboarding: true`, `projects[anchor].history` as a list and synthetic valid `oauthAccount`/hex `userID`. A fake worker start succeeds; before its first command the file equals exactly `mcpServers: {}`, `projects: {}`, `hasCompletedOnboarding: true` plus unchanged screened identity. Cover absent state/identity; all discarded fields and project contents disappear without semantic screening. |
   501	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonempty_global_mcp_servers` | Red on c0f50fa1, green after: pre-existing S11 has nonempty top-level `mcpServers`; assert exactly `worker startup refused: <state-file>: mcpServers: noncanonical global state` before any command, preserving all bytes and absent mutation/trust/spawn/execution markers. |
   502	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member` | Red on c0f50fa1, green after: a documented `oauthAccount` member contains an object; refuse with the file and exact member key named before any command and preserve all bytes. Also cover arrays, other non-string values, undeclared identity members, invalid `userID` and malformed retained structures; canonical string-only identities pass. |
   503	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` | Red on c0f50fa1, green after: a pre-existing forwarded `CLAUDE_ENV_FILE` contains a planted command marker and exports restoring refused environment variables. Refuse with the variable and file named before any hook/worker command runs, without sourcing the file; assert unchanged bytes, no migration/regeneration/trust/spawn and absent command markers. In this one fixture retain absent, empty and same-start launcher-generated positive controls with recorded SHA256, and show that a prior-start digest cannot authorize foreign contents. |
   504	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_aws_credential_chain_selectors` | Red on c0f50fa1: the four reported selectors select a synthetic worker-owned AWS configuration containing `credential_process`; preparation refuses without running or trusting it. Test settings and launch inputs. |
   505	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root` | Red on c0f50fa1: another repository with main-local payload refuses with this task's name before any side effect, for both kinds and all worker routes; the validated anchor/control passes. |
   506	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components` | Red on c0f50fa1: object `source` mappings and inline `content`, including dynamic Markdown, refuse even with the plugin disabled. |
   507	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys` | One fixture per settings source, unknown top-level and nested keys, including a harmless-looking future key; candidate data cannot extend the allowlist. |
   508	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors` | Every prohibited name family, settings/launch placement, exact fixed-value AWS exception, unknown ordinary environment names and noncanonical declared values. |
   509	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_requires_string_component_references` | Scalar file control; object, list, directory, missing file, outside-root reference and unreadable component negatives. |
   510	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch` | Command-free HTTP separately in S01-S07 on both platforms; other documented/unknown/missing/malformed types; other hook-bearing sources; exact indexed refusal. |
   511	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_managed_skills_use_actual_managed_root` | Retained green baseline on c0f50fa1, accepted by owner PING 2751; do not manufacture a red result: using the same temporary managed-root fixture as S05/S06 for both Darwin and Linux, plant a Markdown skill at `<managed-root>/.claude/skills/<name>/SKILL.md` and a bundled plugin payload at `<managed-root>/.claude/skills/<name>/.claude-plugin/plugin.json` with hooks; metadata-only control produces explicit disable. |
   512	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_project_sandbox_extensions_are_refused_before_launch` | Red on c0f50fa1: `excludedCommands: ["*"]`, `filesystem.allowWrite: ["/"]`, extra sockets and nested unknowns in project/local scopes; canonical administrative controls remain accepted. |
   513	| `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_creates_managed_parent_in_printed_commands` | Red on c0f50fa1: missing parent, both platforms, quoting, mkdir-before-install, staged JSON and absent executed-sudo marker. |
   514	| `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_update_reconciles_settings_after_herdr_install` | Red on c0f50fa1: fake Herdr installer re-appends its literal hook, then update reconciliation restores one guarded entry; repeated update preserves custom hooks and produces no managed drift. |
   515	
   516	The runtime-name regressions below are required within the unchanged environment and fixture-alignment budgets:
   517	
   518	| Selector | Required coverage |
   519	| --- | --- |
   520	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names` | Execute the predecessor's name-only probe through the absolute non-shim interpreter read from the rendered manifest, with only HOME/PATH/LANG/TERM supplied. Assert CPATH, LIBRARY_PATH, MANPATH and SDKROOT are absent; Darwin permits only the declared platform addition. Route fixtures prove bootstrap, home lookup and preflight use that interpreter without invoking the system shim or PATH fallback. Preserve command/status/name-only JSON. |
   521	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment` | Darwin absent and correctly shaped present controls pass; malformed shapes, wrong types, trailing content and Linux presence refuse before mutation/trust/spawn. The value never selects behavior, a path or an executable and never appears in evidence. An unrelated injected name blocks with probe JSON. |
   522	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment` | Fake upstream spawn exports exactly AGMSG_SPAWNED=1 before CLI entry; accept it only for the declared child role. Wrong values and undeclared AGMSG names refuse; all four previously declared AGMSG names retain their authority and optionality. Settings env remains limited to its four original pairs. |
   523	
   524	The five allowlist classes each have an explicit fixture: unknown key, undeclared provider selector, foreign root, object-form component and non-command handler. Parameterization may share builders but must name every subcase in validation. Do not replace the three required c0f50fa1-red regressions with tests of a new validator alone.
   525	
   526	Retain all a02 regressions: old tracked settings, alternate executable fields, inherited project MCP, dedicated global state, skills-directory plugins, per-source S01-S23 coverage, sandbox-only documentation, hostile-GH_HOST templates, private caches, native denials, migration and guarded delivery. The fixture-case source inventory equals the production source inventory; each case plants its payload in the source it claims to exercise.
   527	
   528	Retain a02's red/green evidence for `env.HOME`, fenced dynamic commands and the four 79ea98a3 fixes as historical evidence. Do not claim those tests newly fail on c0f50fa1. Update the documentation template test to read the a04 task copy. Update inherited S11 sentinel-preservation/unknown-field-refusal expectations to the discard-and-regenerate contract with `projects: {}`; retain the top-level MCP tamper refusal, and do not keep the old blanket `oauthAccount` refusal or project-entry refusals.
   529	
   530	C11: every `closed` row names one exact `tests/<path>.py::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.
   531	
   532	## Change budget
   533	
   534	Changed lines mean additions plus deletions. The starting measurement is `git diff --numstat 51ba5801 c0f50fa1`, not the obsolete a01 estimate. Preserve its complete output and account separately for base-branch changes already merged into c0f50fa1. The author repeated this immutable comparison when preparing a04.
   535	
   536	For this task's allowed paths, excluding `.orchestration/`, tests and the three regenerated Claude settings templates, that command measures:
   537	
   538	| Source | Changed lines |
   539	| --- | ---: |
   540	| `.claude/settings.json` | 96 |
   541	| `.gitignore` | 1 |
   542	| `Makefile` | 6 |
   543	| `home/dot_agents/agent-config.yaml` | 60 |
   544	| `home/dot_agents/skills/agmsg-orchestration/SKILL.md` | 10 |
   545	| `home/dot_claude-worker/modify_private_settings.json` | 437 |
   546	| `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` | 65 |
   547	| `home/dot_claude/modify_private_settings.json` | 120 |
   548	| `home/dot_local/bin/common/executable_herdr-agents` | 126 |
   549	| `scripts/generate-agent-configs.py` | 181 |
   550	| `scripts/validate-agent-assets.py` | 9 |
   551	| **Measured starting source total** | **1111** |
   552	
   553	The seven allowed test modules measure respectively 103, 15, 206, 935, 104, 310 and 95 changed lines in `allowed_files` order: **1768**. The full historical-base output additionally contains already-merged unrelated source/test rows; list them rather than charging them as new a04 work or editing them.
   554	
   555	Amendment 1's read-only sizing counts 24 lines in c0f50fa1's `present`/`read_json`/`write` analogues plus 16 estimated declaration/digest/route lines, and the 42-line non-command-handler fixture plus 18 estimated content/control lines: **40 source / 60 test**. This measured analogue-based estimate is not a measured implementation result.
   556	
   557	Amendment 2's read-only AST sizing of c0f50fa1 measures `present` 8 + `read_json` 10 + `write` 6 = 24 source analogue lines, plus 56 estimated declaration/project/identity/regeneration lines: **80 source**; the global-state fixture 20 + refusal helper 36 = 56 test analogue lines, plus 64 estimated generation/identity/restart subcases: **120 test**. These are sizing analogues reused without duplication, not measured implementation results. Amendment 3 retains the **80 source** ceiling, removes project-inventory work and replaces the restart subcases with the A-then-B shared-directory sequence: the same 56 test analogue lines plus 104 estimated generation/identity/sequential-start subcase lines give **160 test**, an additional **40 test** over amendment 2. This revised estimate is not a measured implementation result.
   558	
   559	Authorize these incremental ceilings, attributed to accepted findings. These increments are estimates pending implementation measurement, not claimed measured results:
   560	
   561	| Control/finding | Additional source | Additional tests |
   562	| --- | ---: | ---: |
   563	| Closed settings/nested-value schema and sandbox extensions; S1, `local:c0f50fa:2` | 180 | 140 |
   564	| Environment/provider allowlist and credential-chain refusal; `security:c0f50fa:1` | 70 | 100 |
   565	| Validated repository root; `security:c0f50fa:2` | 25 | 60 |
   566	| Scalar inspected-file components; `security:c0f50fa:3` | 35 | 70 |
   567	| Actual enterprise skills root; `local:c0f50fa:1`, `text-security:be969e3:1` | 10 | 40 |
   568	| Handler-class/schema consistency; `text-security:b2a186e:1` | 10 | 30 |
   569	| Printed privileged parent creation; `local:c0f50fa:3` | 10 | 25 |
   570	| Post-Herdr reconciliation; `local:c0f50fa:4` | 10 | 45 |
   571	| Existing render/docs fixture alignment with the accepted re-plan | 10 | 30 |
   572	| Executable environment-file contents and launcher-written SHA256; `text-security:f7af699:1` | 40 | 60 |
   573	| Launcher-generated S11, screened identity and empty shared project state; D-024-34/D-024-35, `worker:5067ed0:1` and `text-security:efa211d:1` with `text-security:f7af699:1` as the shared family | 80 | 160 |
   574	| **Increment ceiling** | **480** | **760** |
   575	
   576	The source cap remains **1591 = 1111 + 480**; the test cap remains **2528 = 1768 + 760**, including a03 amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. The a04 non-shim interpreter, platform-injected and regime-declared controls fit the existing environment/provider and fixture-alignment increments; no cap increases. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.
   577	
   578	RESULT records final per-file numstat, historical-base and final PR merge-base identities, actual source/test totals and per-control attribution. Preserve both the complete historical comparison and the current PR comparison so merged base changes are visible.
   579	
   580	Every later amendment maps to accepted review findings and carries `previous_sha256`; the worker raises no cap. Amend Change budget, the operative C-107 Check cap sentence and the Checks block together. A measured overrun produces a blocked PONG rather than suppression or an unreviewed text edit.
   581	
   582	## Out of scope
   583	
   584	D-024-26 still assigns exact host-probed uv/Python/Node version declarations and mise pins beyond a04's narrow launch-interpreter selection, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.
   585	
   586	Keep `home/dot_mise/config.toml`, the installed state-helper source, Codex boundary sources and updater scripts outside scope. No binding-only code returns through shared files. Add no write-boundary Python hook, gh wrapper, credential-directory substitute, installation discovery or PATH fallback.
   587	
   588	P1-14 a05 and P1-6 own approval/evidence consumption. The exact operative ledger templates tested from this task copy are `gh api --hostname github.com repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha` and `gh api --hostname github.com 'repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref=<sha40>'`. Validate the returned full 40-hex SHA and use the identical SHA in the content request. Every deciding API call binds `--hostname github.com`; every deciding subcommand binds `--repo github.com/mryfmo/dotfiles`. Refuse if the host cannot be bound, without an unbound retry or local fallback.
   589	
   590	Retain `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host`: extract those two templates, substitute only the validated SHA, exercise argv without shell evaluation, export hostile `GH_HOST`, check exact hostname/repository/SHA binding and test an isolated no-gh refusal. This is a contract test, not a ledger consumer or authentication test. Local remotes, URL rewrites, refs, objects and working-copy rows establish no approval authority.
   591	
   592	The host is not a security boundary between same-UID seats. `GH_CONFIG_DIR` does not separate macOS Keychain credentials. Native merge denials remain `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`; shared credentials permit other API routes. P1-11 owns next-records-PR detection, not main-push detection or prevention. Separate-user/host prevention remains the operator's future P1-16 decision.
   593	
   594	`dotfiles-T133-agmsg-hardening-a01` owns store driver-name validation and plugin authorization. Shared administrative exceptions/socket access, external host processes, same-UID races, later configuration reloads and hook-event limitations remain residuals. Dedicated login state is not imported from the orchestrator or used to discover executable acceptance rules.
   595	
   596	Perform no live settings application, authentication/keyring/ruleset mutation, global/administrative installation, permission-policy deployment, restart or merge. Edit no canonical task, acceptance record, decision ledger, design or another task's evidence.
   597	
   598	## Check
   599	
   600	`make render-check` and `make validate-agent-assets` pass. Run repository formatting/lint on changed files, including shellcheck/shfmt on the launcher and rendered guard; shell comments use English shdoc-compatible annotations.
   601	
   602	Run `uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` and `uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs -v` inside the worker sandbox with its private cache. Preserve complete outputs, statuses and tested identities.
   603	
   604	The final diff has at most 1591 changed lines outside `tests/`, `.orchestration/`, `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`, and 2528 under `tests/`.
   605	
   606	Measure the current PR diff against its authenticated merge-base; preserve the historical-base measurement and reconciliation described in Change budget. No unrelated base change becomes an authorized edit.
   607	
   608	Validation includes amendment 3's four c0f50fa1-red/after-green S11 fixtures, including sequential A-then-B starts on the shared configuration directory, the three c0f50fa1-red security regressions, all four local-review cases (enterprise skills retain accepted green baseline coverage), all three runtime-name/interpreter fixtures, every allowlist class, complete S01-S23 case coverage and final green module output. Malformed/unknown retained nested inputs, disabled plugin payloads and shadowed files refuse before mutation; S11 discarded fields are never forwarded. Positive controls retain default seating, canonical delivery, attachment, repeated preparation and ordinary worktree writes.
   609	
   610	Both platform renders retain the exact static deny inventory, directory/descendant coverage, narrow writable stores, private caches, MCP/plugin disables and administrative policy. Sandbox-extension fixtures prove startup refusal, rather than merely showing unchanged administrative JSON.
   611	
   612	Printed-installation evidence includes parent creation before file installation on both platforms with no privileged execution. Fake-update evidence covers Herdr's literal append followed by reconciliation and a second idempotent update.
   613	
   614	Retain existing guard, descendant system-PATH/BASH_ENV, migration, custom-hook, native-denial and cache tests. Record the installed Claude version, actual source read sets, documentation observations and any unsupported-version/source refusal without logging credentials. A version mismatch is a blocked PONG requiring re-tasking.
   615	
   616	Retain the inherited formatting reproduction at historical base `205fe85c` for the 12 out-of-scope shell files; do not repair them here. Run no local Bats tests. Required Bats results and all required checks come from GitHub Actions before RESULT.
   617	
   618	The orchestrator runs the task-consistency checker before dispatch and acceptance against this complete a04 file, using the trusted parent/interpreter/cache contract. C1-C10 and C7b pass, including both C3 task-copy rows; check C11 selectors individually. A separate C-80 security-profile context reviews this reset text before dispatch. These are prerequisites, not results claimed by this draft.
   619	
   620	## Artifacts, completion and deployment
   621	
   622	On the first a04 push, add `.orchestration/dotfiles-T133-worker-write-boundary-a04/task.md` byte-identical to the complete dispatched text. Retain `.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md` and all existing a03 evidence unchanged in `retained_predecessor_directories`; the predecessor is not an allowed write directory. Keep all other a01/a02 artifacts and implementation history as found; the a03 predecessor-deletion instruction does not carry forward.
   623	
   624	Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, operator steps, budget attribution and worker review evidence under the a04 artifact directory. Evidence lives in the worker's own worktree; RESULT says so. Use the `-worker-` review-evidence infix. Record durable decisions/failures with CompactionDB markers; the orchestrator owns main-checkout consolidation.
   625	
   626	Continue PR #431 on the existing branch from the specified head. Discard no unrelated work. The orchestrator owns base updates and dependent `after:` changes; this task retains `after: []`. Every moved final head receives fresh required evidence.
   627	
   628	Every worker command completes inside its sandbox and allowlist. Each gh/git write is an individual command without shell chaining. A boundary failure produces the exact blocked PONG; no permission-gate, tool or shell alternative bypasses it. Do not clear shared Git metadata outside the worker boundary.
   629	
   630	Allow at most one independent pre-push review and two total correction rounds, including that review's corrections. Preserve a01/a02/a03 counters separately. Surviving P0/P1 findings are `open:<id>` or `open:review-<review id>` in RESULT and stop integration for the operator's decision; do not start a private third round.
   631	
   632	Post no `@codex review` comment. Observe automatic final-head reviews within the bounded 15-minute window and record absence as `bot: none`. Required GitHub Actions pass before RESULT. Propose a disposition for every feedback item; the worker resolves no review thread and grants no acceptance.
   633	
   634	Follow repository agent-side Crit-data/receipt rules without a browser or human review request. Record resolved evidence, including a justified review-scope approval when finding-free; never use `AGENT_REVIEWED=1` without reading the evidence. Report any Plan Mode server for orchestrator cleanup.
   635	
   636	RESULT names final full head/base/branch, PR, changed files, task-copy SHA256, exact selectors, red/green identities, final numstat/attribution, schema/source/handler/root inventories, installed-version observations, inherited binding-removal inventory, scripts/installed paths, settings destinations, printed installation commands, feedback/dispositions, open findings, counters and all evidence paths. Distinguish historical claims from new final-head results.
   637	
   638	Report user-visible changes: this repository's workers alone are supported; unknown settings or environment inputs refuse; launcher startup uses the manifest-named non-shim mise interpreter, Darwin's optional encoding variable has only the declared shape, and upstream AGMSG_SPAWNED is exactly 1; every start regenerates global state with `projects: {}`, preserves only screened identity and resets native counters/caches/project history/allowedTools; workspace trust uses the launcher's existing spawn-readiness dialog acceptance; alternate providers/authentication selectors refuse; object/inline components refuse; lower-scope sandbox extensions refuse; actual enterprise skills are inspected. Refusal preserves original bytes and names the source without exposing values.
   639	
   640	Retain user-visible effects of dedicated worker login, static denies also affecting Bash writes, writable agmsg stores except trusted-plugin authorization, private caches, no worker sandbox escape, shared administrative exceptions/socket access, guarded project hooks and unchanged legacy orchestrator PermissionRequest. Formatter availability and complete executable binding remain deferred.
   641	
   642	The orchestrator obtains separate local review, task-level audit and security-profile review of the final implementation head. Final feedback collection, dispositions, acceptance and integration follow Orchestrator Playbook step 10 in order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the review receipt; merge is pinned to the reviewed final head. The worker writes no approval row.
   643	
   644	Operator deployment remains post-merge and coupled to the approved P1-14 a05 change under D-024-31: `make update`, then `make install-managed-settings`, inspect staged content, then execute the printed privileged parent-creation and platform-specific file-installation commands. Record administrative installation separately from chezmoi application.
   645	
   646	The operator logs in with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`, applies the separately prepared deterministic Codex permgate escape-denial change and restarts affected sessions. Inspect installed administrative content, dedicated directory, static denies, stores/caches, all startup sources, closed-schema refusals, MCP/plugin disables, PermissionRequest exception and sandbox startup. Check lower-scope conflicting arrays and report shared capabilities without exposing credentials.
   647	
   648	Merge alone establishes no deployment readiness. Record application, administrative installation, login, startup checks and the Codex permgate change before releasing live dependents; mechanisms requiring executable binding also wait for that owner.
   649	
   650	Not performed in task authoring: implementation, worker tests, local Bats, deployment, login or restarts. Final-head correctness and live enforcement remain unverified.
   651	
   652	## Checks (pasted by the orchestrator before each send)
   653	

exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; cat .ua/meta.json' in ~/Workspace/dotfiles
 succeeded in 22ms:
 M .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md
 M .orchestration/acceptance/dotfiles-T133-loop-limits-a01.md
 M .orchestration/acceptance/dotfiles-T133-record-ledger-carry-a01.md
 M .orchestration/acceptance/dotfiles-T133-regime-ci-followup-a01.md
 M .orchestration/acceptance/dotfiles-T133-result-precheck-a01.md
 M .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md
 M .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
 M .orchestration/decisions.tsv
 M .orchestration/learning/corrections-inventory.tsv
 M .orchestration/plans/024-checklists.md
 M .orchestration/plans/024-design-quality.md
 M .orchestration/plans/024-omp-cutover-and-corrective-order.md
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
?? .orchestration/acceptance/dotfiles-T133-ci-efficiency-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-inv6-reset-anchors-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-permission-guard-gate-a05-slice1.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-pre-send-check-a02.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a01.md
?? .orchestration/acceptance/dotfiles-T133-python-pin-a02.md
?? .orchestration/acceptance/dotfiles-T133-record-json-sync-a01.md
?? .orchestration/acceptance/dotfiles-T133-records-sync-pr-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a01.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-fixture-grammar-a02.md
?? .orchestration/acceptance/dotfiles-T133-regime-ci-token-a01.md
?? .orchestration/acceptance/dotfiles-T133-result-evidence-check-a01.md
?? .orchestration/acceptance/dotfiles-T133-result-precheck-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-result-precheck-a03-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a03-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a05-checker.md
?? .orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a06-checker.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01-design-reset.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a01.md
?? .orchestration/acceptance/dotfiles-T133-trusted-exec-contract-tests-a02.md
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
?? .orchestration/dotfiles-T133-inv6-reset-anchors-review-a01/
?? .orchestration/dotfiles-T133-pre-send-check-a01-redesign-review-a01/
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
?? .orchestration/learning/mistakes/M-20261020-09-typed-sha-and-mute-seat.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md
?? .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a09.md
?? .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a05.md
?? .orchestration/tasks/dotfiles-T133-inv6-reset-anchors-review-a01.md
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
?? .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
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
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-2c8c05a.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-c32513e.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-cef7ebe.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-cef7ebe.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d44acec.md.last.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d4798eb.md
?? .orchestration/validation/dotfiles-T133-regime-ci-token-a01-text-security-d4798eb.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-9313f2c.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-9313f2c.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-b858147.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-b858147.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-c8d2f6b.md
?? .orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-text-security-c8d2f6b.md.last.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md
?? .orchestration/validation/records-sync-28-pr-feedback.json
?? .orchestration/validation/records-sync-29-pr-feedback.json
f7f3806749815ba9dfd90e7ff9ee390ca6079014
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

exec
/bin/zsh -lc "sed -n '180,345p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md | nl -ba -v180" in ~/Workspace/dotfiles
 succeeded in 27ms:
   180	  - control: "5.14 item 0: 脅威モデル"
   181	    disposition: "residual: host controls reduce accidental and injected damage; shared credentials and same-UID processes prevent a seat-isolation claim."
   182	  - control: "5.14 item 1: 書き込み境界"
   183	    disposition: "residual: retained write policy and the closed startup schema implement this task's scope; later reloads and consumption races remain outside its guarantee."
   184	  - control: "5.14 item 2: 無害化した環境を最初に"
   185	    disposition: "residual: trusted-parent clean prefixes, fixed operations and declared environment inputs remain mandatory; the legacy orchestrator PermissionRequest and complete executable binding retain their separate owner."
   186	  - control: "5.14 item 3: 信頼パスの境界検査"
   187	    disposition: "residual: canonical root and component containment checks precede startup, including aliases; executable realpath binding remains with the binding task."
   188	  - control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す"
   189	    disposition: "residual: fixed dispatch avoids candidate-selected execution, while snapshots, last-use digests and complete executable identity remain with their consuming mechanisms."
   190	  - control: "5.14 item 5: 出力と予約の同一性"
   191	    disposition: "residual: this task introduces no reservation protocol; consuming orchestrator mechanisms retain ownership of full-head outputs and inode-bound locks."
   192	  - control: "5.14 item 6: 正直な残余"
   193	    disposition: "residual: the report retains shared credentials, administrative exceptions, socket access, agmsg sourcing, races, reloads and hook-event limitations."
   194	  - control: "5.14 item 7: 検証"
   195	    disposition: "residual: retained source-class fixtures and new allowlist regressions supply final-head evidence; shared trusted-execution helper adoption remains with P1-6."
   196	  - control: "5.14 item 8: 承認はコミット済み台帳から読む"
   197	    disposition: "residual: fixed-host ledger templates and hostile-host fixtures preserve the contract; P1-14 a05 and P1-6 own actual approval consumption."
   198	  - control: "5.14 item 9: 私設キャッシュ"
   199	    disposition: "residual: private worker caches and orchestrator-cache denies remain; exact interpreter declarations, resolver consumption and deployment binding remain separately owned."
   200	  - control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない"
   201	    disposition: "residual: the Worker Playbook permits no worker escape, while shared administrative capabilities and the operator's Codex permgate deployment remain explicit residuals."
   202	  - control: canonical GitHub API host binding
   203	    disposition: "residual: both ledger templates explicitly bind github.com and mryfmo/dotfiles; contract tests establish argv binding rather than enforcement by deferred consumers."
   204	  - control: hook failure policy
   205	    disposition: "residual: supported rendered entries retain onFailure block, but background hooks, excluded events and runtime timeout behavior establish no enforcement responsibility."
   206	  - control: agmsg store driver and plugin selection
   207	    disposition: "residual: plugin-code and trusted-plugin denies reduce one route; writable store-selected sourcing remains owned by dotfiles-T133-agmsg-hardening-a01."
   208	  - control: orchestrator effect merge
   209	    disposition: "residual: only the orchestrator integrates with final-head evidence and a pinned merge; shared credentials still permit API routes outside the native prefix denials."
   210	  - control: orchestrator effect update-branch
   211	    disposition: "residual: an update moves the head and requires fresh CI, feedback, local review, audit and security evidence before integration."
   212	  - control: orchestrator effect forced worker removal
   213	    disposition: "residual: none is planned; existing dirty-worktree protections remain and any operator-authorized discarded state must be recorded."
   214	premises:
   215	  - claim: >-
   216	      INV-6 carries three a03 amendments; plan 006 S2 requires design by another authoring context. This review-profile context supplies a04, reset_of a03, rather than another a03 amendment. Read-only rechecks on 2026-10-20 confirmed worker-e remains at c0f50fa1383416240ad28959dbc4635afa777175 on tools/worker-write-boundary-a01. Keep PR #431 and the uncommitted a03 implementation/test draft. The canonical a03 text and retained worker task copy both hash to 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b.
   217	    sources:
   218	      - .orchestration/plans/006-regime-v3-execution.md
   219	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
   220	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
   221	    executed_commands:
   222	      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" rev-parse HEAD', output: 'c0f50fa1383416240ad28959dbc4635afa777175'}
   223	      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" symbolic-ref --short HEAD', output: 'tools/worker-write-boundary-a01'}
   224	      - {command: 'shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md', output: 'both files: 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b'}
   225	  - claim: >-
   226	      The blocked PONG reports probe exit 0, test exit 1, zero worker correction rounds and zero independent pre-push reviews. Its green-new.log is a failing uncommitted draft: 15 tests, 45 failures, including undeclared runtime names, noncanonical TMPDIR and unreconciled fake-update hooks; it is not a RESULT or final green evidence. Retain it without relabeling.
   227	    sources:
   228	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
   229	      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log
   230	  - claim: >-
   231	      runtime-contract-probe.json supplies the exact name lists below. Read-only repetition at 2026-10-20T14:57:54Z produced the same names, exit statuses and spawn digest, without a live worker or private settings. The manifest currently lacks the non-shim interpreter declaration; a04 must add it within its existing launcher policy, not discover it through PATH.
   232	    sources: [.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json]
   233	    repeated_probe:
   234	      supplied_environment_names: [HOME, LANG, PATH, TERM]
   235	      child_code: 'import os,json,pathlib,platform,pwd,tempfile,subprocess;print(json.dumps(sorted(os.environ)))'
   236	      interpreters:
   237	        - command: '/usr/bin/python3 -I -c <child_code>'
   238	          exit: 0
   239	          observed_names: [CPATH, HOME, LANG, LIBRARY_PATH, MANPATH, PATH, SDKROOT, TERM, __CF_USER_TEXT_ENCODING]
   240	          unlisted_names: [CPATH, LIBRARY_PATH, MANPATH, SDKROOT, __CF_USER_TEXT_ENCODING]
   241	          stderr: "python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead"
   242	        - command: '"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" -I -c <child_code>'
   243	          exit: 0
   244	          observed_names: [HOME, LANG, PATH, TERM, __CF_USER_TEXT_ENCODING]
   245	          unlisted_names: [__CF_USER_TEXT_ENCODING]
   246	          stderr: ""
   247	      upstream_spawn_sha256: 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731
   248	      upstream_spawn_line: 527
   249	      upstream_spawn_text: "  echo 'export AGMSG_SPAWNED=1'"
   250	      schema_has_AGMSG_SPAWNED: false
   251	      live_worker: false
   252	      private_settings_read: false
   253	  - claim: >-
   254	      The complete c0f50fa1 security review found AWS credential-chain selectors, a foreign-repository main-local inventory gap and object-form plugin command mappings. The local review found the incorrect enterprise skills root, lower-scope sandbox extensions, missing privileged parent creation and post-Herdr settings drift. The local chain stopped before a task-level audit; none exists for c0f50fa1. Repeated renderings in the local report are four findings, not additional independent findings.
   255	    sources:
   256	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
   257	      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
   258	      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
   259	  - claim: >-
   260	      D-024-26 retains the write boundary and transfers executable binding. D-024-29 freezes design 5.14; D-024-30 applies it by reference. The 2026-10-20 residual-list entry in this text records the allowlist generalisation without reopening the frozen items.
   261	    sources:
   262	      - .orchestration/decisions.tsv
   263	      - $HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md
   264	  - claim: >-
   265	      The inherited read-only version observation is Claude Code 2.1.300. Documentation enumerations fetched at 2026-10-19T20:41:53Z were: settings scopes User, Shared project, Project local, Managed; precedence Managed settings, Command line, Project local settings, Shared project settings, User settings; MCP scopes Local, Project, User; hook types command, http, mcp_tool, prompt, agent; plugin origins @<marketplace>, @inline, @skills-dir, @synced; plugin enablement sources --add-dir, user, project, local, flag, managed; skills roots Enterprise, Personal, Project, Nested, Additional directory, Plugin; account-synced roots remain undeclared. Recheck the installed version and loader before changing implementation.
   266	    fetched_at: "2026-10-19T20:41:53Z"
   267	    sources:
   268	      - https://code.claude.com/docs/en/settings
   269	      - https://code.claude.com/docs/en/hooks
   270	      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
   271	      - https://code.claude.com/docs/en/plugins/loading
   272	      - https://code.claude.com/docs/en/skills
   273	  - claim: >-
   274	      C-87 inherited observation: the orchestrator observed the documented ["Where skills live" table](https://code.claude.com/docs/en/skills) at 2026-10-20T04:47:57Z and the read-only loader probe at 2026-10-20T04:50Z. The Enterprise row says "`.claude/skills/<skill-name>/SKILL.md` in the managed settings directory", with Linux example `/etc/claude-code/.claude/skills/<skill-name>/`. The pinned 2.1.300 loader, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3, contains `/.claude/skills/` (11 occurrences), `.claude/skills/` (8), `/etc/claude-code` (6) and `/Library/Application Support/ClaudeCode` (3); the historical supplied probe excerpt is `LC_ALL=C /usr/bin/grep -a -o -E '…(\.claude/skills|/skills"|skills/)…' <loader> | sort | uniq -c`. These observations bind the enterprise inventory and fixture to `<managed-root>/.claude/skills`.
   275	    sources: ["https://code.claude.com/docs/en/skills", ".orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md"]
   276	  - claim: "Worker a010 blocked before any edit (PONG 2694, 2026-10-20T04:00:43Z): the loader persists numStartups at start and hasCompletedOnboarding at onboarding; the orchestrator reproduced the installed-loader probe below, not a live worker start."
   277	    sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md]
   278	    probe: {executed_by: review-profile-author, executed_at: "2026-10-20T14:57:54Z", loader: "$HOME/.local/share/mise/installs/npm-anthropic-ai-claude-code/2.1.300/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe", format_observed: Mach-O arm64}
   279	    executed_commands:
   280	      - {command: 'shasum -a 256 <loader>', output: '475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3  <loader>'}
   281	      - {command: '<loader> --version', output: '2.1.300 (Claude Code)'}
   282	      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o numStartups <loader>', output: '12'}
   283	      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o hasCompletedOnboarding <loader>', output: '15'}
   284	    quoted_string_probes: [{command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"numStartups"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasCompletedOnboarding"'' <loader>', output: '0'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasTrustDialogAccepted"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"oauthAccount"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"mcpServers"'' <loader>', output: '29'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"enabledMcpjsonServers"'' <loader>', output: '5'}]
   285	  - claim: >-
   286	      The single source inventory is S01-S23 below plus executable environment-file contents admitted by the launch-input schema. Each parameter denotes every actual matching file, inspected independently before merging. User means the dedicated configuration directory; managed-root is the platform directory containing managed-settings.json. S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json; S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery; S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration; S12 each skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json; S16 every default hooks/hooks.json and explicitly referenced plugin hook file; S17 every admitted marketplace-root/.claude-plugin/marketplace.json; S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file; S22 every applicable subagent Markdown file; S23 every default or referenced plugin LSP file. Non-file managed delivery and caller-selected inputs must fit the same closed schema and read set or cause a named refusal.
   287	    sources:
   288	      - https://code.claude.com/docs/en/settings
   289	      - https://code.claude.com/docs/en/managed-settings
   290	      - https://code.claude.com/docs/en/server-managed-settings
   291	      - https://code.claude.com/docs/en/plugins/manifest-reference
   292	      - https://code.claude.com/docs/en/skills
   293	---
   294	
   295	# AGMSG-TASK dotfiles-T133-worker-write-boundary-a04 — plan 024 P1-15; worker startup screen; seat a010
   296	
   297	## Goal and reset
   298	
   299	[memory:decision] Reset a03 under INV-6 and plan 006 S2 through this separate review-profile authoring context. Worker a010 is Codex, security profile, in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`; this task changes Claude's boundary and preserves Codex policy. Continue `tools/worker-write-boundary-a01` and PR #431 from `c0f50fa1383416240ad28959dbc4635afa777175`, keeping the uncommitted a03 draft and all predecessor evidence; open no second PR.
   300	
   301	Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Retain every a03 item and fix, with only the runtime/interpreter decision specified here.
   302	
   303	[memory:failure] a01 and a02 each spent two worker rounds; a03's blocked PONG reports zero worker correction rounds and zero independent pre-push reviews, while its amendment history remains counted. This reset supplies a04 at most two worker correction rounds in total, including pre-push corrections, and at most one independent pre-push review; it erases no predecessor counters or findings.
   304	
   305	The retained draft is not approved, and its `raw/green-new.log` is explicitly failing. The c0f50fa1 local chain stopped before its task-level audit. Obtain new final-head audit and security evidence; do not describe either as inherited.
   306	
   307	## History
   308	
   309	a01 and a02 each exhausted their two worker rounds, and a03 reset the lineage to a closed startup schema while continuing PR #431. Its amendments bound executable environment-file contents, regenerated S11 with screened identity and empty shared project state, and corrected the enterprise skills inventory; those controls and their finding history remain. The worker blocked on shim/platform-added runtime names and upstream `AGMSG_SPAWNED=1`, preserving its uncommitted draft and failing evidence. INV-6's three counted a03 amendments trigger plan 006 S2, so another context authors a04 to resolve only that runtime-name/interpreter contract instead of extending a03.
   310	
   311	## Design and finding history
   312	
   313	Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 by reference, including its residual list. D-024-29 keeps items 0-10 frozen; D-024-30 narrows C-88 to exact contract sentences asserted by tests.
   314	
   315	Item 1 applies to dedicated worker settings, static input-derived write protection and refusal before startup.
   316	Item 2 applies to trusted-parent execution, clean environments and fixed command selection.
   317	Item 3 applies to canonical anchor, worktree and component identities before consumption.
   318	Item 8 applies to committed approval authority through explicitly host-bound repository API calls.
   319	Item 9 applies to private caches and the trusted parent's interpreter/cache inputs.
   320	
   321	**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a04:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.
   322	
   323	Read the full a02 and a03 acceptance records, a03 task, blocked PONG and both runtime evidence files, and both c0f50fa1 reviews named in `premises:`. Retain the following history and finding classes in the a04 report and acceptance lineage:
   324	
   325	| Finding | Class | Required treatment |
   326	| --- | --- | --- |
   327	| `text-security:2ae9e2c:1` | input-inventory | Project `.mcp.json` remains independently screened. |
   328	| `text-security:ebbb71b:1` | input-inventory | Skills-directory plugins remain inventoried even when disabled. |
   329	| `text-security:ebbb71b:2` | input-inventory | Dedicated global state regenerates `mcpServers: {}` and `projects: {}`; native project entries are discarded. |
   330	| `text-security:ebbb71b:3` | repository-binding | Canonical main comes from the fixed repository API. |
   331	| `text-security:b2a186e:1` | input-inventory | Inspect handler type before command; non-command types refuse. |
   332	| `text-security:b2a186e:2` | repository-binding | Both ledger calls bind `--hostname github.com`. |
   333	| `text-security:ac9ce14:0` | correct | Historical text approval only; it does not approve a04. |
   334	| a02 independent pre-push review | input-inventory | Retain fixes for `env.HOME` guard selection and fenced dynamic commands. |
   335	| `local:79ea98a:1` | tool-environment | Retain manifest-generated `--advisor fable` acceptance. |
   336	| `local:79ea98a:2` | tool-environment | Retain absolute tool paths and attachment identity environment. |
   337	| `local:79ea98a:3-4` | partial-fix | Retain custom-hook preservation and legacy PreToolUse migration. |
   338	| `security:c0f50fa:1` | input-inventory | Refuse undeclared credential-chain/provider selectors. |
   339	| `security:c0f50fa:2` | input-inventory | Refuse worker starts for repositories other than the validated anchor. |
   340	| `security:c0f50fa:3` | input-inventory | Refuse object and inline plugin/command components. |
   341	| `local:c0f50fa:1` | tool-environment | Inventory enterprise skills under the actual managed root. |
   342	| `local:c0f50fa:2` | tool-environment | Reject lower-scope sandbox extensions before array merging. |
   343	| `local:c0f50fa:3-4` | partial-fix | Fix printed parent creation and post-installer reconciliation here. |
   344	| `text-security:f7af699:1` | input-inventory | Admit executable environment-file contents only when absent, empty or launcher-generated for this start. |
   345	| `worker:5067ed0:1`, `text-security:efa211d:1` | input-inventory | Regenerate S11 at every start with `projects: {}` and screened identity; discard native persisted state, including every project's state, and use the launcher's existing spawn-readiness trust-dialog acceptance. |

exec
/bin/zsh -lc "sed -n '346,505p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md | nl -ba -v346" in ~/Workspace/dotfiles
 succeeded in 22ms:
   346	| `text-security:be969e3:1` | input-inventory | Inventory enterprise skills and plant both Markdown and bundled plugin fixtures under `<managed-root>/.claude/skills`, following the C-87 documented table and pinned-loader probe. |
   347	
   348	S1 first triggered on the three source omissions in 2ae9e2c/ebbb71b. The re-plan enumerated S01-S23, but subsequent findings still exploited open field/value acceptance; the c0f50fa1 security findings bring that post-re-plan family to its sixth finding. This reset changes the approach rather than adding three more denylist entries.
   349	
   350	Preserve the advisory-owner history and owner `dotfiles-T133-worker-write-boundary-followup-a01` exactly as history. The two c0f50fa1 P2 fixes are retained from a03 by this text; the orchestrator reconciles their owner rows and updates dependent task references. The worker edits no canonical acceptance or owner task.
   351	
   352	Retain D-024-26's transferred binding findings, including `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. Do not relabel them as fixed.
   353	
   354	## Closed startup schema
   355	
   356	Declare this schema in `home/dot_agents/agent-config.yaml` and expose it through the existing renderer/preparation code. Candidate files, Git objects and installed upstream schemas never define their own acceptance policy. Add no new helper, generated output file or dependency.
   357	
   358	The schema below is exhaustive for data forwarded to the loader. Objects reject unknown keys at every level, including nested objects and records that would otherwise be preserved; S11 fields designated for discard are not screened or preserved. Reject duplicate JSON keys, wrong types, Boolean/integer substitutions, unreadable inputs and unsupported forms. Missing optional fields may pass; a present field must match its declared source-specific form.
   359	
   360	### Settings and values
   361	
   362	The only settings keys are `permissions`, `sandbox`, `hooks`, `env`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `enabledPlugins`, `syncClaudeAiPlugins`, `syncClaudeAiSkills`, `extraKnownMarketplaces` and `disableSkillShellExecution`.
   363	
   364	| Node | Accepted shape and values |
   365	| --- | --- |
   366	| `permissions` | Only `defaultMode`, `deny`, `additionalDirectories`; `defaultMode` is `auto` where applicable; `additionalDirectories` is `[]`; `deny` is a renderer-declared worker/native-denial fragment for that source. No caller-added allow/ask rule or alternate permission mode. |
   367	| `sandbox` | Only the keys emitted by the worker or administrative renderer: `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands`, `excludedCommands`, `filesystem`, `network`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `allowAppleEvents`. |
   368	| `sandbox.filesystem` | Only `allowWrite`, `disabled`; exact source-specific canonical values. Worker write grants are the four declared agmsg stores; ordinary worktree/cache writes remain provided by the worktree boundary. |
   369	| `sandbox.network` | Only `allowedDomains`, `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`; exact source-specific canonical values. |
   370	| Sandbox lists and Booleans | Every present leaf/list equals the canonical worker fragment in S01-S04 or administrative fragment in S05-S07. Worker exclusions are empty; additional write roots/sockets are refused. Only administrative sources may contain the exact shared three exclusions and single Herdr socket. |
   371	| `hooks` | Only source/event/matcher/operation combinations generated by the trusted renderer or delivery constructor. Groups have only `matcher`, `hooks`; handlers have only renderer-declared `type`, `command`, `timeout`, `async`, `statusMessage`, `onFailure`, with exact canonical values. |
   372	| Handler type | Only the string `command`; validate it before reading `command`. HTTP, MCP-tool, prompt, agent, unknown, missing, null and non-string types refuse. |
   373	| MCP approval fields | `enableAllProjectMcpServers: false`; `enabledMcpjsonServers: []`; `disabledMcpjsonServers: []` when present. Approval state never exempts a server definition. |
   374	| Plugin fields | `enabledPlugins` maps only manifest-known or inventoried plugin identities to `false`; both sync fields are `false`; `extraKnownMarketplaces` is `{}`. |
   375	| Skill execution | `disableSkillShellExecution`, when present, is `true`. |
   376	| `env` | Only the four exact name/value pairs in the next subsection; arbitrary strings, maps and provider credentials are not preserved. |
   377	
   378	Absent or empty settings objects pass where the source permits them. Administrative drop-ins/cache may contain canonical partial objects; partial means omitted declared fields, never new fields or alternate values. Validate each list before merging so an empty generated worker list cannot conceal a broader lower-scope array.
   379	
   380	There is no canonical worker setting for helpers, status-line commands, wrappers, alternate sandbox executables, policy helpers or authentication refresh/export commands. Their keys refuse as undeclared, including misplaced forms. The orchestrator managed PermissionRequest exception is not a worker-start exception.
   381	
   382	The old instruction to preserve unrelated non-executable state now applies only to fields admitted by this schema. Unknown settings refuse without deletion or normalization; S11 alone discards pre-existing fields outside its declared structures and carried identity, without screening or forwarding them.
   383	
   384	### Environment and launch arguments
   385	
   386	Settings `env` admits exactly `GH_TELEMETRY="false"`, `DO_NOT_TRACK="1"`, `CHECKPOINT_DISABLE="1"` and `AWS_EC2_METADATA_DISABLED="true"`, as declared by the manifest. The last name is the sole declared `AWS_*` exception and cannot select credentials or a provider.
   387	
   388	The launch-input schema classifies names by source: existing parent/runtime declarations, `regime-declared`, and `platform-injected`. The latter two classes below are closed enumerations, not prefixes. They do not extend settings `env`, configuration-file keys or CLI arguments.
   389	
   390	The launcher and its startup/preflight Python children use only the manifest-named absolute mise-installed non-shim interpreter, observed here as `<validated-home>/.local/share/mise/installs/python/3.15.0/bin/python3.15`. Add that narrow declaration to the existing manifest-owned launcher policy and consume it through the existing renderer; never route through `/usr/bin/python3`, a mise shim, PATH lookup or an interpreter-discovery fallback. Cover startup bootstrap/home lookup as well as preparation. This selects the interpreter for this boundary without returning the deferred complete binding work to scope.
   391	
   392	The launch-input schema admits only these names, with source-specific values supplied or checked by the trusted parent:
   393	
   394	| Names | Value authority |
   395	| --- | --- |
   396	| `HOME`, `PATH`, `LANG`, `TERM` | Validated passwd home; prescribed system-only child PATH; `C.UTF-8`; declared terminal value. Hook children retain `TERM=dumb`. |
   397	| `TMPDIR` | Canonical trusted temporary directory supplied by the parent, not a candidate configuration root. |
   398	| `CLAUDE_CONFIG_DIR` | Exactly the dedicated worker directory under the validated home. |
   399	| `CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` | Parent-bound canonical project identity and runtime shell file; `CLAUDE_ENV_FILE` additionally requires the executable-content control below. |
   400	| `UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR` | Exactly `<canonical-worktree>/.uv-cache` and its `python` child. |
   401	| `regime-declared`: `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE`, `AGMSG_AGENT_PID` | Retain a03's exact authorities: `0`, validated launcher store selection, declared monitor value and numeric runtime process identifier; unset default-store selection remains supported. |
   402	| `regime-declared`: `AGMSG_SPAWNED` | Exactly the string `1`, set by upstream `spawn.sh` on the launch surface before the worker CLI; require it on spawn-launched roles and do not synthesize it for unrelated child roles. |
   403	| `platform-injected`: `__CF_USER_TEXT_ENCODING` | Darwin only; present or absent allowed. A present string must full-match `0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+`. The regime validates the shape and otherwise never reads or uses it. Linux presence refuses. |
   404	| `HERDR_ENV`, `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_AGENTS_LAYOUT`, `HERDR_SOCKET_PATH` | Validated control-plane identity, `managed` layout and canonical configured socket; these grant no worker sandbox exception. |
   405	| `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID` | Parent/runtime session identifier and numeric process identifiers where required by canonical attachment/delivery. |
   406	| `CLICOLOR_FORCE`, `FORCE_COLOR` | Launcher-written `1` only where the launch route uses them. |
   407	| `GH_TELEMETRY`, `DO_NOT_TRACK`, `CHECKPOINT_DISABLE`, `AWS_EC2_METADATA_DISABLED` | The four fixed values above. |
   408	| `CHEZMOI_SOURCE_DIR`, `CHEZMOI_HOME_DIR` | Preparation-only trusted source/home bindings; not caller-selected worker configuration or executable roots. |
   409	
   410	The read-only amendment-1 probe of the [documented environment variables](https://code.claude.com/docs/en/env-vars) identifies `CLAUDE_ENV_FILE` as the only name admitted above that selects a file whose contents execute: Claude runs its shell contents before Bash commands. No other admitted name has that documented role; `CLAUDE_CODE_SHELL` and `CLAUDE_CODE_SHELL_PREFIX` remain undeclared. Include the named file's contents in the preflight read set alongside S01-S23.
   411	
   412	For every admitted executable-content file variable, preflight accepts its named file only when absent, empty, or byte-identical to canonical contents generated by the launcher for this start. Inspect without sourcing or executing it; unreadable/nonregular files and any other contents refuse before trust, migration, regeneration, hooks or worker commands with `worker startup refused: <file>: <variable>: noncanonical executable environment file contents`. Preserve refused bytes; never overwrite a planted file to make it pass. After all preflight checks pass, the launcher itself writes the canonical runtime-file contents, records SHA256 bound to the variable, canonical file and this start in existing startup state/evidence, and verifies those bytes before forwarding. Candidate-supplied or prior-start digests cannot authorize contents. Reuse the existing runtime file and startup state; add no sidecar, helper or generated configuration output. Later replacement races and reloads retain their existing residual owners.
   413	
   414	Validate proposed worker configuration inputs before forwarding them. A clean child environment contains only the names declared for that child role; do not inherit the caller environment wholesale. Unknown proposed environment names refuse rather than becoming an unchecked pass-through. Existing profile/control-plane variables used to select a worker are consumed through their existing manifest-owned interfaces, not forwarded as arbitrary worker settings.
   415	
   416	Every `CLAUDE_CODE_USE_*`, `AWS_*`, `ANTHROPIC_*`, `*_API_KEY`, `*_TOKEN` and `*_PROFILE` name refuses unless explicitly declared above with its exact allowed value. In particular refuse `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE` in settings and launch inputs before any credential lookup or helper execution. Add no AWS configuration parser.
   417	
   418	No shell/interpreter startup or loader override is declared: `BASH_ENV`, `ENV`, `NODE_OPTIONS`, `NODE_PATH`, `PYTHON*`, `LD_*`, `DYLD_*`, shell wrappers and alternate configuration/cache roots refuse as worker inputs. Do not print their values.
   419	
   420	Preserve the manifest-generated Claude argument interface: only `--model`, `--effort`, `--advisor` with their declared profile values, including `--advisor fable`. Caller-added settings, MCP, plugin, agent and additional-directory arguments refuse. Keep existing Codex arguments and network/shared-Git policy unchanged.
   421	
   422	A clean-parent probe runs through the interpreter named by the rendered manifest, imports the same modules as the predecessor probe, and asserts `CPATH`, `LIBRARY_PATH`, `MANPATH` and `SDKROOT` are absent. They remain undeclared and refuse if encountered; do not delete them to conceal an unexpected injection. Test the observed child environment as well as the parent's proposed names, with child-role-specific declarations.
   423	
   424	Any other new name, source, required state field or interpreter mismatch still blocks and re-tasks. Send a blocked PONG naming the boundary, exact command and status, with probe JSON containing the supplied/observed name lists, undeclared names and interpreter identity under the a04 evidence directory. Preserve the predecessor JSON unchanged. No wildcard, prefix-wide acceptance, candidate-learned schema, suppression or default-as-authorization is allowed; print no environment values.
   425	
   426	### Sources, roots and component forms
   427	
   428	The sole repository anchor is the manifest declaration resolving to `$HOME/Workspace/dotfiles`. Bind its identity to the validated passwd home and actual main checkout, resolving symlinks and filesystem case aliases. Worker roots must be registered linked worktrees beneath that anchor's declared `.claude/worktrees/` root with the same Git common directory.
   429	
   430	Every worker launch route, for either worker kind, refuses another repository before worktree creation, identity registration, hook writes, workspace trust or spawn. The refusal names this task: `worker startup refused: dotfiles-T133-worker-write-boundary-a04: unsupported repository root`. Do not fix the foreign-root finding by inspecting the fixed anchor while launching elsewhere.
   431	
   432	Admitted configuration roots are the dedicated worker directory, the validated anchor/worktree `.claude` directories, applicable nested worktree and additional-directory `.claude` directories, the platform managed root and contained plugin roots discovered through the declared registry. Inherited MCP files are the independently enumerated ancestor read set. No account-synced, inline, seed, alternate cache or caller-selected root is admitted; caller-added additional-directory arguments remain refused.
   433	
   434	The admitted skills roots are exactly Enterprise `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), Personal `<absolute-home>/.claude-worker/skills` under the dedicated configuration directory, Project `<project>/.claude/skills`, Nested `<subdir>/.claude/skills`, Additional directory `<add-dir>/.claude/skills` under an applicable `--add-dir` directory, and Plugin `<plugin>/skills`. Inspect both `<skills-root>/<name>/SKILL.md` and bundled `<skills-root>/<name>/.claude-plugin/plugin.json`. Managed command/agent locations likewise start at the actual managed root. Resolve every selected path and refuse containment escapes, unsupported aliases, missing references or unreadable files.
   435	
   436	| Source form | Closed acceptance |
   437	| --- | --- |
   438	| S08-S10, S18-S19 | Objects containing only absent or empty `mcpServers`/`managedMcpServers` maps. No server, including remote-only definitions, is canonical here. |
   439	| S11 global state | At every start, after all preflight checks pass and before any loader/worker command, write the existing `CLAUDE_CONFIG_DIR/.claude.json` from scratch: `mcpServers: {}`, `projects: {}` and `hasCompletedOnboarding: true`, plus screened identity fields below. The generated file carries no per-project inventory or pre-generated workspace trust. Never merge the previous file into this output. |
   440	| S11 pre-existing structures and identity | The existing file must be a JSON object. Missing optional retained fields pass and generated fields are written anew. Present top-level `mcpServers` must be `{}`. Carry optional `oauthAccount` only as an object with string-only members from this documented fixed set: `accountUuid`, `emailAddress`, `organizationUuid`, `displayName`, `fullName`, `organizationRole`, `workspaceRole`; declare the same set in the manifest and fixtures. Carry optional `userID` only as a string matching `^[0-9a-f]{64}$`, the installed loader's hex form. Undeclared identity members, non-string `oauthAccount` members, invalid identity values and a nonempty or malformed top-level MCP map refuse with `worker startup refused: <state-file>: <offending-key>: <named reason>` before any command or mutation, preserving refused bytes. Nonempty top-level servers use the exact reason `noncanonical global state` as tamper evidence. |
   441	| S12/S15 plugin descriptor | Only `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and the component keys `hooks`, `mcpServers`, `lspServers`, `commands`, `agents`, `skills`. Descriptive fields are strings, keywords are strings, and author has only string `name`, `email`, `url`. |
   442	| Component references | Each present component is one scalar string referencing a regular file within its admitted root. The screening reads that file under its source schema before accepting it. Arrays, objects, inline content, URLs and explicit directory references refuse. Default component directories are independently expanded into inspected files. |
   443	| S13 installed registry | Only `version: 2` and `plugins`; plugin IDs map to record lists with only `scope`, `installPath`, `version`, `installedAt`, `lastUpdated`, `gitCommitSha`, `projectPath`. Scope is user/project/local; paths are contained and project-bound; descriptive fields are strings and a present commit is 40 hex. Every referenced descriptor is read and every discovered ID is disabled. |
   444	| S14 marketplace registry | Only `{}`; no refresh source or executable header helper is canonical. |
   445	| S16 hook file | Only an absent/empty `hooks` object; plugin-owned handlers have no canonical worker operation. |
   446	| S17 marketplace descriptor | Only descriptive `name`, `owner`, `metadata`, `plugins`; owner has string name/email, metadata has string description/version, and plugins is absent or `[]`. Additional plugin selections refuse. |
   447	| S20-S22 Markdown | Plain text with the existing restricted frontmatter grammar: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model. Booleans are Boolean, model/tool selections are manifest-declared values, and unknown/nested executable forms refuse. Dynamic shell expansion, including fenced forms, refuses everywhere. |
   448	| S23 LSP | Only `{}`; command/args definitions are not canonical. |
   449	| Non-file managed inputs | Enumerated canonical administrative data only; otherwise refuse with the managed source name before executing any helper or starting Claude. |
   450	
   451	For S11, every other pre-existing top-level field, including the entire `projects` value and all its contents, `numStartups`, prior onboarding state, tips/changelog caches, project `history`, `allowedTools` and cost counters, is neither screened nor preserved; only syntax/duplicate-key/readability checks apply to the whole input. Discarded objects and arrays are never recursively screened or forwarded. Generate onboarding anew and `projects: {}`, preserve only screened identity values, and reuse the existing atomic writer after the complete preflight; the loader regenerates native state. The anchor's workspace trust is established by the launcher's existing acceptance of the workspace-trust dialog during spawn's readiness wait (`herdr-agents --add-worker` for a Claude worker, documented in the SKILL's 'Regime activation and progress' section). All Claude workers share `CLAUDE_CONFIG_DIR` at `$HOME/.claude-worker`; discarding the prior `projects` value lets sequential sibling starts succeed. A loader requiring another preserved field blocks and retasks rather than widening silently.
   452	
   453	These restrictions also apply to disabled plugins and shadowed sources. Do not recursively ignore an unknown object because it lacks a familiar executable key. A plugin `commands` mapping containing `{"source": ...}` or inline `content` refuses at the selecting file/key.
   454	
   455	## Implementation and retained controls
   456	
   457	1. Keep one preflight over S01-S23, admitted executable environment-file contents and the closed schema. Every Claude route calls it before workspace trust, migration, normalization, regeneration or execution. Enumerate through the filesystem, including ignored/untracked inputs; neither Git tracking nor a nearer definition removes a source. Inspect implicit and selected components separately without executing helpers, installing packages, fetching plugins or starting servers.
   458	
   459	2. Refusals identify the actual source and key/class without printing payloads, environment values, URLs with credentials or authentication material. Preserve the handler message `worker startup refused: <source-file>: hooks.<event>[<group-index>].hooks[<handler-index>]: noncanonical hook handler`, with zero-based indices. Other refusals use `worker startup refused: <source>: <key>: <named reason>`. Unknown settings, selectors, roots, components and source forms each receive a named reason.
   460	
   461	3. Retain exact recognized legacy-delivery classification, including canonical project binding. First screen every source; only after complete success migrate recognized owned entries, validate the prepared result under the same schema, then write. Unknown content outside S11's discard partition refuses without changing any pre-existing bytes; successful S11 regeneration intentionally replaces discarded state only after every source passes. Never rewrite tracked settings or create a local file merely for migration. Keep repeated preparation and delivery-tool-unavailable behavior.
   462	
   463	4. Retain dedicated `CLAUDE_CONFIG_DIR`, both private cache variables on every actual worker route, `AGMSG_RESOLVE_PROJECT=0`, validated `AGMSG_STORAGE_PATH`, canonical attachment identity and `onFailure: "block"` where supported. A writable `run/proj.<pid>.project` cannot replace the explicit project identity. Preserve the a02 absolute Herdr/jq/Node/npm/Codex calls and attachment environment; fixed PATH must not regress attachment or default seating.
   464	
   465	5. Keep static `trusted_paths` derived from trusted executable inputs, not Git trees/indexes. Preserve anchored source/control paths, tracked/main-local settings, `.orchestration`, both `.agents/worklog/**` and `.agents/worklog/uv-cache/**`, worktree `.claude` directory/descendant targets and `.mcp.json`. Ordinary worktree source and private cache writes remain available.
   466	
   467	6. Retain explicit protection of `<absolute-home>/.agents/agent-config.yaml`, model profiles, permgate policy, skill scripts/SKILL files, agmsg plugin code and `db/trusted-plugins`, `<absolute-home>/.claude/**`, `<absolute-home>/.claude-worker/**`, installed guard, local wrappers/application code, configuration/state/tool installations and shared uv caches. Keep directory and descendant user-site protection for `.pth`, `usercustomize.py` and `sitecustomize.py` on both platforms. Add no blanket `<absolute-home>/.agents/**` or `<absolute-home>/.local/**` deny: agmsg `db`, `teams`, `run`, `ext-tools` stay writable except `db/trusted-plugins`.
   468	
   469	7. Retain separate orchestrator, worker and administrative renders. Worker policy keeps `defaultMode: auto`, sandbox startup failure, disabled unsandboxed requests, empty user exclusions, restricted writes, no user Herdr socket, explicit MCP auto-approval disables, account sync off and false plugin entries including discovered `@skills-dir` identities. Empty maps alone do not disable plugins or replace screening.
   470	
   471	8. Administrative settings retain enabled sandboxing, `failIfUnavailable: true`, disabled unsandboxed requests, filesystem enforcement, disabled weaker isolation/Apple Events/all-socket/local-binding switches, exactly the Herdr socket, and exactly these ordered exclusions: `agmsg-dispatch *`, `herdr-agents *`, `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These shared capabilities remain available to every Claude seat and authorize no worker escape. Lower-scope canonical validation rejects extra exclusions, writes or sockets before array merging.
   472	
   473	9. Keep the orchestrator managed PermissionRequest command's existing literal bytes unchanged, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.
   474	
   475	10. Apply design 5.14 by reference for trusted-parent execution, Python isolation and Git inspection. Consume the manifest-named non-shim interpreter specified above on every launcher startup/preflight Python route; add no resolver, helper, private executable directory, PATH fallback or broader version-pin work. Do not execute arbitrary task-body shell strings as probes.
   476	
   477	11. Preserve guard routing, fixed payload paths, argument boundaries, stdin and child status. Canonical worker/sibling/unrelated/missing launch identities execute no orchestrator project payload. Only fixed installed worker-delivery operations run for workers. Formatter/map operations also reject worker/outside-anchor tool inputs. Keep tracked settings portable and all existing event/validator markers.
   478	
   479	12. Preserve managed SessionStart/PostToolUse/PreToolUse migration, custom-hook ordering, mixed entries, escaped-tilde distinctions, stale replacement and idempotence. For `make update`, reconcile the managed Claude settings after `scripts/update-agent-assets.sh` runs Herdr's installer, using the allowed Makefile/merge/renderer surfaces. Do not edit the updater script or import its unguarded hook as canonical. Verify one effective guarded hook and no managed-settings drift after repeated fake updates.
   480	
   481	13. `install-managed-settings` still stages `<absolute-home>/.claude/managed-settings.rendered.json` nonprivileged. Print a quoted privileged `mkdir -p` for the detected administrative parent before the existing quoted `sudo install -m 0644` command. Cover both platform destinations and homes containing spaces. Execute neither privileged command; do not install, log in or restart.
   482	
   483	14. Keep all existing validator checks, exact three-entry exclusion fixtures on both platforms, legacy PermissionRequest validity, duplicate-hook checks, ordering/timeouts, freshness, portability and secret/home-path scanning. Add no bound-PermissionRequest mode. `.gitignore` retains `.uv-cache/` as this task's only addition.
   484	
   485	15. Worker Playbook step 4 retains this exact test-asserted sentence:
   486	
   487	> Complete every worker command, including gh, git push and authenticated git fetch, inside the sandbox and allowlist without forbidden actions or escalation; anything that cannot complete there is `AGMSG-PONG v1 status=blocked` naming the exact command and boundary.
   488	
   489	The entire Worker Playbook, including steps 2, 5 and 11, authorizes no exception. Evidence-sync writes/masking, CompactionDB consolidation and agmsg-dispatch control-plane exemptions remain orchestrator-only. Workers write required relative evidence in their own worktree; the orchestrator copies it before acceptance. Preserve merged documentation changes and run the complete documentation module.
   490	
   491	## Regression fixtures
   492	
   493	Write the new tests before implementation. Use the existing temporary-HOME, managed-root, linked-worktree and fake-launcher builders. Tests execute no payload, credential helper, HTTP endpoint, server, plugin, subagent or live worker.
   494	
   495	Each refusal fixture asserts the source/key or named root message, unchanged existing bytes, no migration/regeneration, no trust acceptance, no spawn and absent execution/request markers. Positive absent/canonical controls and repeated starts remain covered.
   496	
   497	| Selector | Required coverage |
   498	| --- | --- |
   499	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees` | Red on c0f50fa1, green after: sequentially start registered linked-worktree workers A then B on one shared `CLAUDE_CONFIG_DIR`. A's start leaves the regenerated file; simulated loader writes then add A's project entry with a `history` list. B's start succeeds and, before its first command, leaves exactly the regenerated file with `projects: {}` and screened identity. Replace any planted-project-key refusal and same-worktree restart fixture with this cross-worktree sequence. |
   500	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_global_state_with_screened_identity` | Red on c0f50fa1, green after: pre-existing S11 has `numStartups: 5`, `hasCompletedOnboarding: true`, `projects[anchor].history` as a list and synthetic valid `oauthAccount`/hex `userID`. A fake worker start succeeds; before its first command the file equals exactly `mcpServers: {}`, `projects: {}`, `hasCompletedOnboarding: true` plus unchanged screened identity. Cover absent state/identity; all discarded fields and project contents disappear without semantic screening. |
   501	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonempty_global_mcp_servers` | Red on c0f50fa1, green after: pre-existing S11 has nonempty top-level `mcpServers`; assert exactly `worker startup refused: <state-file>: mcpServers: noncanonical global state` before any command, preserving all bytes and absent mutation/trust/spawn/execution markers. |
   502	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member` | Red on c0f50fa1, green after: a documented `oauthAccount` member contains an object; refuse with the file and exact member key named before any command and preserve all bytes. Also cover arrays, other non-string values, undeclared identity members, invalid `userID` and malformed retained structures; canonical string-only identities pass. |
   503	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` | Red on c0f50fa1, green after: a pre-existing forwarded `CLAUDE_ENV_FILE` contains a planted command marker and exports restoring refused environment variables. Refuse with the variable and file named before any hook/worker command runs, without sourcing the file; assert unchanged bytes, no migration/regeneration/trust/spawn and absent command markers. In this one fixture retain absent, empty and same-start launcher-generated positive controls with recorded SHA256, and show that a prior-start digest cannot authorize foreign contents. |
   504	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_aws_credential_chain_selectors` | Red on c0f50fa1: the four reported selectors select a synthetic worker-owned AWS configuration containing `credential_process`; preparation refuses without running or trusting it. Test settings and launch inputs. |
   505	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root` | Red on c0f50fa1: another repository with main-local payload refuses with this task's name before any side effect, for both kinds and all worker routes; the validated anchor/control passes. |

**Reviewing references and planning design**
codex
この案は、起動時の入力検査と、後続タスクが担う実行ファイルの束縛を分けています。その境界を踏まえ、`closed` とした行のテスト範囲、および残余リスクとして明記された箇所に実効性のある制御が残るかを確認しています。
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '506,597p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md | nl -ba -v506" in ~/Workspace/dotfiles
 succeeded in 108ms:
   506	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components` | Red on c0f50fa1: object `source` mappings and inline `content`, including dynamic Markdown, refuse even with the plugin disabled. |
   507	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys` | One fixture per settings source, unknown top-level and nested keys, including a harmless-looking future key; candidate data cannot extend the allowlist. |
   508	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors` | Every prohibited name family, settings/launch placement, exact fixed-value AWS exception, unknown ordinary environment names and noncanonical declared values. |
   509	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_requires_string_component_references` | Scalar file control; object, list, directory, missing file, outside-root reference and unreadable component negatives. |
   510	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch` | Command-free HTTP separately in S01-S07 on both platforms; other documented/unknown/missing/malformed types; other hook-bearing sources; exact indexed refusal. |
   511	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_managed_skills_use_actual_managed_root` | Retained green baseline on c0f50fa1, accepted by owner PING 2751; do not manufacture a red result: using the same temporary managed-root fixture as S05/S06 for both Darwin and Linux, plant a Markdown skill at `<managed-root>/.claude/skills/<name>/SKILL.md` and a bundled plugin payload at `<managed-root>/.claude/skills/<name>/.claude-plugin/plugin.json` with hooks; metadata-only control produces explicit disable. |
   512	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_project_sandbox_extensions_are_refused_before_launch` | Red on c0f50fa1: `excludedCommands: ["*"]`, `filesystem.allowWrite: ["/"]`, extra sockets and nested unknowns in project/local scopes; canonical administrative controls remain accepted. |
   513	| `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_creates_managed_parent_in_printed_commands` | Red on c0f50fa1: missing parent, both platforms, quoting, mkdir-before-install, staged JSON and absent executed-sudo marker. |
   514	| `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_update_reconciles_settings_after_herdr_install` | Red on c0f50fa1: fake Herdr installer re-appends its literal hook, then update reconciliation restores one guarded entry; repeated update preserves custom hooks and produces no managed drift. |
   515	
   516	The runtime-name regressions below are required within the unchanged environment and fixture-alignment budgets:
   517	
   518	| Selector | Required coverage |
   519	| --- | --- |
   520	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names` | Execute the predecessor's name-only probe through the absolute non-shim interpreter read from the rendered manifest, with only HOME/PATH/LANG/TERM supplied. Assert CPATH, LIBRARY_PATH, MANPATH and SDKROOT are absent; Darwin permits only the declared platform addition. Route fixtures prove bootstrap, home lookup and preflight use that interpreter without invoking the system shim or PATH fallback. Preserve command/status/name-only JSON. |
   521	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment` | Darwin absent and correctly shaped present controls pass; malformed shapes, wrong types, trailing content and Linux presence refuse before mutation/trust/spawn. The value never selects behavior, a path or an executable and never appears in evidence. An unrelated injected name blocks with probe JSON. |
   522	| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment` | Fake upstream spawn exports exactly AGMSG_SPAWNED=1 before CLI entry; accept it only for the declared child role. Wrong values and undeclared AGMSG names refuse; all four previously declared AGMSG names retain their authority and optionality. Settings env remains limited to its four original pairs. |
   523	
   524	The five allowlist classes each have an explicit fixture: unknown key, undeclared provider selector, foreign root, object-form component and non-command handler. Parameterization may share builders but must name every subcase in validation. Do not replace the three required c0f50fa1-red regressions with tests of a new validator alone.
   525	
   526	Retain all a02 regressions: old tracked settings, alternate executable fields, inherited project MCP, dedicated global state, skills-directory plugins, per-source S01-S23 coverage, sandbox-only documentation, hostile-GH_HOST templates, private caches, native denials, migration and guarded delivery. The fixture-case source inventory equals the production source inventory; each case plants its payload in the source it claims to exercise.
   527	
   528	Retain a02's red/green evidence for `env.HOME`, fenced dynamic commands and the four 79ea98a3 fixes as historical evidence. Do not claim those tests newly fail on c0f50fa1. Update the documentation template test to read the a04 task copy. Update inherited S11 sentinel-preservation/unknown-field-refusal expectations to the discard-and-regenerate contract with `projects: {}`; retain the top-level MCP tamper refusal, and do not keep the old blanket `oauthAccount` refusal or project-entry refusals.
   529	
   530	C11: every `closed` row names one exact `tests/<path>.py::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.
   531	
   532	## Change budget
   533	
   534	Changed lines mean additions plus deletions. The starting measurement is `git diff --numstat 51ba5801 c0f50fa1`, not the obsolete a01 estimate. Preserve its complete output and account separately for base-branch changes already merged into c0f50fa1. The author repeated this immutable comparison when preparing a04.
   535	
   536	For this task's allowed paths, excluding `.orchestration/`, tests and the three regenerated Claude settings templates, that command measures:
   537	
   538	| Source | Changed lines |
   539	| --- | ---: |
   540	| `.claude/settings.json` | 96 |
   541	| `.gitignore` | 1 |
   542	| `Makefile` | 6 |
   543	| `home/dot_agents/agent-config.yaml` | 60 |
   544	| `home/dot_agents/skills/agmsg-orchestration/SKILL.md` | 10 |
   545	| `home/dot_claude-worker/modify_private_settings.json` | 437 |
   546	| `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` | 65 |
   547	| `home/dot_claude/modify_private_settings.json` | 120 |
   548	| `home/dot_local/bin/common/executable_herdr-agents` | 126 |
   549	| `scripts/generate-agent-configs.py` | 181 |
   550	| `scripts/validate-agent-assets.py` | 9 |
   551	| **Measured starting source total** | **1111** |
   552	
   553	The seven allowed test modules measure respectively 103, 15, 206, 935, 104, 310 and 95 changed lines in `allowed_files` order: **1768**. The full historical-base output additionally contains already-merged unrelated source/test rows; list them rather than charging them as new a04 work or editing them.
   554	
   555	Amendment 1's read-only sizing counts 24 lines in c0f50fa1's `present`/`read_json`/`write` analogues plus 16 estimated declaration/digest/route lines, and the 42-line non-command-handler fixture plus 18 estimated content/control lines: **40 source / 60 test**. This measured analogue-based estimate is not a measured implementation result.
   556	
   557	Amendment 2's read-only AST sizing of c0f50fa1 measures `present` 8 + `read_json` 10 + `write` 6 = 24 source analogue lines, plus 56 estimated declaration/project/identity/regeneration lines: **80 source**; the global-state fixture 20 + refusal helper 36 = 56 test analogue lines, plus 64 estimated generation/identity/restart subcases: **120 test**. These are sizing analogues reused without duplication, not measured implementation results. Amendment 3 retains the **80 source** ceiling, removes project-inventory work and replaces the restart subcases with the A-then-B shared-directory sequence: the same 56 test analogue lines plus 104 estimated generation/identity/sequential-start subcase lines give **160 test**, an additional **40 test** over amendment 2. This revised estimate is not a measured implementation result.
   558	
   559	Authorize these incremental ceilings, attributed to accepted findings. These increments are estimates pending implementation measurement, not claimed measured results:
   560	
   561	| Control/finding | Additional source | Additional tests |
   562	| --- | ---: | ---: |
   563	| Closed settings/nested-value schema and sandbox extensions; S1, `local:c0f50fa:2` | 180 | 140 |
   564	| Environment/provider allowlist and credential-chain refusal; `security:c0f50fa:1` | 70 | 100 |
   565	| Validated repository root; `security:c0f50fa:2` | 25 | 60 |
   566	| Scalar inspected-file components; `security:c0f50fa:3` | 35 | 70 |
   567	| Actual enterprise skills root; `local:c0f50fa:1`, `text-security:be969e3:1` | 10 | 40 |
   568	| Handler-class/schema consistency; `text-security:b2a186e:1` | 10 | 30 |
   569	| Printed privileged parent creation; `local:c0f50fa:3` | 10 | 25 |
   570	| Post-Herdr reconciliation; `local:c0f50fa:4` | 10 | 45 |
   571	| Existing render/docs fixture alignment with the accepted re-plan | 10 | 30 |
   572	| Executable environment-file contents and launcher-written SHA256; `text-security:f7af699:1` | 40 | 60 |
   573	| Launcher-generated S11, screened identity and empty shared project state; D-024-34/D-024-35, `worker:5067ed0:1` and `text-security:efa211d:1` with `text-security:f7af699:1` as the shared family | 80 | 160 |
   574	| **Increment ceiling** | **480** | **760** |
   575	
   576	The source cap remains **1591 = 1111 + 480**; the test cap remains **2528 = 1768 + 760**, including a03 amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. The a04 non-shim interpreter, platform-injected and regime-declared controls fit the existing environment/provider and fixture-alignment increments; no cap increases. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.
   577	
   578	RESULT records final per-file numstat, historical-base and final PR merge-base identities, actual source/test totals and per-control attribution. Preserve both the complete historical comparison and the current PR comparison so merged base changes are visible.
   579	
   580	Every later amendment maps to accepted review findings and carries `previous_sha256`; the worker raises no cap. Amend Change budget, the operative C-107 Check cap sentence and the Checks block together. A measured overrun produces a blocked PONG rather than suppression or an unreviewed text edit.
   581	
   582	## Out of scope
   583	
   584	D-024-26 still assigns exact host-probed uv/Python/Node version declarations and mise pins beyond a04's narrow launch-interpreter selection, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.
   585	
   586	Keep `home/dot_mise/config.toml`, the installed state-helper source, Codex boundary sources and updater scripts outside scope. No binding-only code returns through shared files. Add no write-boundary Python hook, gh wrapper, credential-directory substitute, installation discovery or PATH fallback.
   587	
   588	P1-14 a05 and P1-6 own approval/evidence consumption. The exact operative ledger templates tested from this task copy are `gh api --hostname github.com repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha` and `gh api --hostname github.com 'repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref=<sha40>'`. Validate the returned full 40-hex SHA and use the identical SHA in the content request. Every deciding API call binds `--hostname github.com`; every deciding subcommand binds `--repo github.com/mryfmo/dotfiles`. Refuse if the host cannot be bound, without an unbound retry or local fallback.
   589	
   590	Retain `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host`: extract those two templates, substitute only the validated SHA, exercise argv without shell evaluation, export hostile `GH_HOST`, check exact hostname/repository/SHA binding and test an isolated no-gh refusal. This is a contract test, not a ledger consumer or authentication test. Local remotes, URL rewrites, refs, objects and working-copy rows establish no approval authority.
   591	
   592	The host is not a security boundary between same-UID seats. `GH_CONFIG_DIR` does not separate macOS Keychain credentials. Native merge denials remain `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`; shared credentials permit other API routes. P1-11 owns next-records-PR detection, not main-push detection or prevention. Separate-user/host prevention remains the operator's future P1-16 decision.
   593	
   594	`dotfiles-T133-agmsg-hardening-a01` owns store driver-name validation and plugin authorization. Shared administrative exceptions/socket access, external host processes, same-UID races, later configuration reloads and hook-event limitations remain residuals. Dedicated login state is not imported from the orchestrator or used to discover executable acceptance rules.
   595	
   596	Perform no live settings application, authentication/keyring/ruleset mutation, global/administrative installation, permission-policy deployment, restart or merge. Edit no canonical task, acceptance record, decision ledger, design or another task's evidence.
   597	

 succeeded in 148ms:
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



**Managing large transcript review**
exec
/bin/zsh -lc "wc -l .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md; tail -n 55 .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md; tail -n 18 .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md; rg -n '"'^### 5.14|''^### 5.15|D-024-(26|29|30|31|34|35)'"' .orchestration/plans/024-design-quality.md .orchestration/decisions.tsv" in ~/Workspace/dotfiles
 succeeded in 222ms:
      82 .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
      48 .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
    4152 .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md
    4282 total
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



**Managing large transcript review**
exec
/bin/zsh -lc "wc -l .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md; tail -n 55 .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md; tail -n 18 .orchestration/validation/dotfiles-T133-worker-write-boundary-a04-text-security-d562c68.md; rg -n '"'^### 5.14|''^### 5.15|D-024-(26|29|30|31|34|35)'"' .orchestration/plans/024-design-quality.md .orchestration/decisions.tsv" in ~/Workspace/dotfiles
.orchestration/plans/024-design-quality.md:95:### 5.14 残余（凍結後の計測事実、D-024-29）
.orchestration/decisions.tsv:74:D-024-26	2026-10-19T11:2xZ	P1-15 (worker-write-boundary-a01) ships the write boundary alone: the executable-binding work (exact installation layouts probed on the host for uv, Python and node, the bound PermissionRequest hook through the rendered absolute uv and isolated Python, the deploy-time effective-settings check, the formatter PATH) splits into dotfiles-T133-trusted-entrypoint-binding-a01 (after P1-15 and ci-efficiency-followup-a04, whose trusted interpreter resolver it consumes); until it lands the PermissionRequest hook keeps its current form behind the managed deny rules	recorded in the what column (row written in the 4-column form id/when/what/basis; converted to the 6-column header 2026-10-21T00:1x JST)	the fourth executable-binding finding of the P1-15 text review (5204254) after the re-plan line of 20:1x JST; M-20261019-05; the operator's standing order that a third finding of one class re-plans rather than patches	not recorded at conversion
.orchestration/decisions.tsv:77:D-024-29	2026-10-19T21:39Z	Design 5.14 is frozen (plan 006 A1: three review rounds, then freeze with a residual list): items 0-10 are the contract; a text review finding that needs a new design sentence is recorded in the design's residual list and as an owner row, not as an amendment of the item and of the text under review, unless it names a P0/P1 that is exploitable in the proposed implementation.	items 1, 2, 3, 8 and 9 were amended five times on 10-19/20 (one per review round of P1-15 and P1-12), each amendment re-opening the texts that quote the item (C-88) and costing a review round each; the texts chased a moving design.	plan 006 A1; M-20261019-05; C-92	applied from 06:40 JST; the residual list is a new subsection `5.14 残余` in 024-design-quality.md (written at the next design edit)
.orchestration/decisions.tsv:78:D-024-30	2026-10-19T23:16Z	A task text applies design 5.14 by reference: it names the items it relies on (`design: 5.14 items 2, 3, 8, 9`) and carries one threat row per item 0-10 in the item's own words, never a restated or paraphrased copy of the item; C-88 is narrowed to the exact contract sentences a test asserts; the task-consistency check gains a rule (C16) that a security: true orchestrator-side text names 5.14 and has the per-item rows (owner: the P1-12 follow-up after a04 frees task-consistency-check.py).	restated design text drifted in every reset text and re-opened a review round at each design amendment (P1-15: 23 review rounds; P1-12: 4); by-reference texts stay within proposal 1's caps and a mechanical check replaces the reviewer's paraphrase comparison; the operator's direction of 2026-10-19T22:59Z (relayed by a011) asks for the same.	plan 006 A1; D-024-29; M-20261019-05; proposal 1	applied from 08:15 JST to new texts (trusted-exec-contract-tests-a01 first); existing correct texts are not rewritten
.orchestration/decisions.tsv:79:D-024-31	2026-10-20T00:11Z	D-024-28 (an asks-only first slice of P1-14 a05) is withdrawn: the operator's approval D-024-14 binds the three ask-rule removals together with the synchronous hook installation (one digest), so a slice that removes the asks alone is not the approved change and would need its own permission approval from the committed ledger; `make update` therefore stays coupled to the a05 merge, and the idle Claude seats are relieved by converting a seat to Codex (operator step) and by security:false work.	C-80 review 1293d6b of the slice text (2026-10-20T00:04Z): two P1 (replacement control deferred; approval digest covers removals plus hook) that no text amendment can close without a new operator permission approval.	design 5.14 item 8 (approvals from the committed ledger); D-024-13/14; D-024-28; C-80 1293d6b	applied 09:08 JST; the a05 remainder is split later along non-permission lines (proposal 1)
.orchestration/decisions.tsv:82:D-024-34	2026-10-20T04:12Z	The files the worker's loader consumes at start and the regime need not preserve are launcher-generated at every start: the global state file `CLAUDE_CONFIG_DIR/.claude.json` is written from the declared shape (empty `mcpServers`, `projects` with exactly the validated identities and Boolean trust, `hasCompletedOnboarding: true`) plus identity fields carried from the previous file after screening (`oauthAccount` string members, `userID`); native persisted state (`numStartups`, onboarding, tips and changelog caches, per-project history, allowedTools, cost counters) is neither screened nor preserved; refusal with a named message stays for declared-structure violations (non-empty top-level `mcpServers`, undeclared project keys, non-Boolean trust flags, undeclared object or array members), as evidence of tampering. `CLAUDE_ENV_FILE` (amendment 1) belongs to the same family. A loader that requires another preserved field blocks and retasks (the text's rule), never widens silently.	a010's probe of the installed loader (2.1.300, sha256 475517ca…; reproduced by the orchestrator at 04:10Z) shows the loader itself writes fields outside any exact schema, so the allowlist re-plan's closed schema (D-024-29/30 lineage, a02 -> a03) refuses the worker's own state at the next start; a per-version native-field table would block every loader update until re-probed; generating the file realises design 5.14 item 1 (refuse any executable payload it did not write) by writing the whole file. Second re-plan of the input-inventory family (rows text-security:f7af699:1, worker:5067ed0:1 after the allowlist re-plan).	design 5.14 item 1; D-024-29; D-024-30; a03 record rows; M-20261019-05	applied 13:12 JST as a03 amendment 2 (review-profile text, C-80 round 3); the operator may redirect it once per class (the 13:15 JST report)
.orchestration/decisions.tsv:83:D-024-35	2026-10-20T04:29Z	The launcher-generated global state file (D-024-34) carries no per-project inventory: `projects` is regenerated empty at every start and the workspace trust of the anchor is established by the launcher's existing acceptance of the trust dialog during spawn's readiness wait (`herdr-agents --add-worker`, SKILL 'Regime activation'), not by pre-generated project keys; sibling worker worktrees that share `CLAUDE_CONFIG_DIR` therefore never reject each other's keys. Refusal with a named message stays for a non-empty top-level `mcpServers` (tamper evidence). A loader needing another preserved field still blocks and retasks.	C-80 round 3 of a03 (efa211d, P2): all Claude workers share `.claude-worker/.claude.json` while S11 accepted only the anchor and the current worktree's keys, so worker B's start would reject worker A's key; enumerating sibling worktrees is the fourth inventory of the family to be found incomplete (2ae9e2c, ebbb71b, c0f50fa1, f7af699, 5067ed0, efa211d), so the inventory is removed rather than extended. Third re-plan of the input-inventory family; the operator may redirect it once per class.	D-024-34; design 5.14 item 1; a03 record rows; SKILL (trust-dialog acceptance)	applied 13:29 JST as a03 amendment 3 (review-profile text, C-80 round 4 under a new re-plan line, C-92)
.orchestration/decisions.tsv:85:D-024-37	2026-10-20T06:43Z	New `security: true` mechanism texts are held until the trusted-execution contract (`tests/unit/trusted_exec_contract.py`, PR #436) and the P1-15 launcher (PR #431) are on main; a held text then names those controls by reference (C-88) instead of restating the contract, and takes one C-80 round. Held now: dotfiles-T133-record-json-sync-a01 (two rounds: 1 P1 + 9 P2, all of the trusted-execution family) and dotfiles-T133-records-sync-pr-a01 (round 1: 2 P1 + 2 P2 of the same family; amendment 1 installed, review deferred).	the two texts cost three review rounds in 40 minutes and every finding re-derived the contract the two in-flight PRs land (git configuration isolation, resolved-root binding, replace refs, the agmsg-dispatch exclusion); continuing is the whack-a-mole the operator forbade, while the seats they were meant for (a011, a009) have no other dispatchable text until #438 merges.	C-88; D-024-29/30; M-20261019-05 (text review rounds unbounded); the record-json-sync record	applied 15:43 JST; the Claude seats' idle time until #438 is the operator's approval, not a text gap
.orchestration/decisions.tsv:93:D-024-45	2026-10-20T11:45Z	Design 5.14 item 10 (every worker command inside the sandbox) contradicts the seat configuration that runs `agmsg-dispatch` through excludedCommands outside the sandbox (audit:7eab146:1, audit:6434c27:1; the a008 seat's sandbox.md:18). The design is frozen (D-024-29), so the choice is the operator's: default = record a control-plane exemption for `agmsg-dispatch` in 5.14 item 10 by a design-amendment task (the bus is the regime's control plane, not a repository mutation; the herdr socket is already in the sandbox allowlist, so the alternative, running it inside, is tested first by a Claude seat); until decided, the finding is recorded as it stands on every affected lineage and never dispositioned fixed. Placed in the project map's decisions panel with that default.	recorded in the what column (row written in the 4-column form id/when/what/decider; converted to the 6-column header 2026-10-21T00:1x JST)	claude-deep-dot	revoked by D-024-46

**Analyzing audit log behavior**
exec
/bin/zsh -lc "sed -n '55,130p' .orchestration/plans/024-design-quality.md; sed -n '30,82p' .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "cat .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json; sed -n '1,65p' .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log; diff -u .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md" in ~/Workspace/dotfiles
 succeeded in 62ms:
5.11 **品質保証の仕組み（効率の対になる側。ユーザー指摘 11:4x「効率のみで品質確保が抜けている」）**

効率側の仕組みは、それ自体がマージを決める trust-boundary のコードになる。したがって品質保証は「人のレビューを残す」ではなく、次の 6 つを機械として入れる。

| # | 品質の仕組み | 具体 | 位置 |
| --- | --- | --- | --- |
| Q-A 仕組み自体が trust-boundary | P1-3、P1-4a、P1-4、P1-5、P1-6、P1-7、P1-10〜P1-14 のタスクはすべて `security: true`、threat_table 必須、task-level audit に加えて `codex --profile security exec` の 2 本目を受ける。allowed_files 外への変更は audit が fail | todo の各行、AGENTS.md Audit 節 |
| Q-B fail-closed | verdict は入力が 1 つでも欠ける・読めない・schema に合わないとき `hold`（exit 20）。audit-pool は schema 不合格の JSON を捨てて request を blocked に。precheck は 1 検査でも失敗したら RESULT を送らせない（dispatch.sh が `precheck=` 無し・不一致を拒否）。dispositions は空の not-applicable を拒否。CI regime は証跡不一致で赤。「黙って通る」経路を作らない | 5.12 の各仕様 |
| Q-C shadow mode による校正 | verdict.sh は最初の 2 波は `--apply` なしで走らせ、orchestrator の手判定と並べて `.orchestration/validation/verdict-shadow.tsv`（列 pr、head、machine、human、agree、at。machine 列は `verdict.sh --shadow` が、human 列は orchestrator が各受け入れ直後に書く）に記録。不一致 0 を連続 4 件確認してから `--apply` を有効化。audit の差分監査も同じく、初回は全差分監査と並走して所見の差分が 0 であることを 2 件確認してから有効化 | P1-4a の完了条件、DoD-P1-j |
| Q-D 品質指標を gate に | 連続 2 波ごとに計測し、閾値を超えたらマージ凍結と根本原因の記録（plan 第 7 節 STOP に追加済み）: main の push CI 赤 ≤ 1 回/2 波（かつ根本原因が記録されている）、マージ後 24 時間以内の hotfix PR（escaped defect）= 0、監査 P0/P1 のマージ後検出 = 0、revise 率 ≤ 20%、disposition の not-applicable 比率 ≤ 30%（高ければ Bot の所見を軽視している兆候として review） | 024-checklists.md P1-j、P1-k、progress.tsv の列 |
| Q-E 証跡の不変性 | 証跡ファイル名に head sha を含め（`audit-<head>.json`、`verdict-<head>.json`、`precheck.json` の `head`）、受け入れ記録に各ファイルの sha256 を書く。gate は記録の sha256 と実ファイルを照合。後から書き換えた証跡は照合で落ちる | 5.12、`orch-gate.sh` |
| Q-F 仕組みの回帰テスト | 新規スクリプトは `tests/unit/test_<name>.py` に赤→緑の fixture を持ち、既存の regime テスト（test_dispatch、test_regime_counters、test_check_regime_boundary、test_agmsg_orchestration_docs）が緑のまま。`make unit-test` と `render-check` は precheck と CI の両方で走る | 各タスクの Validation |

人の判断として残すもの（機械化しない）: 5.13 の細分化の結果、「方向と価値の決定」「P0/P1 の残存リスクの受容」「権限・信頼境界を広げる変更の承認」「トークンに権限が無い管理者操作と資格情報の投入」の 4 つに縮む。

5.13 **「人の判断」の細分化（ルール化・プログラム化できるもの / AI エージェントが判断できるもの / 人にしかできないもの）**

| 判断項目 | 細分化 | 分類 | 具体（ルールとプログラム） | 位置 |
| --- | --- | --- | --- | --- |
| plan と設計の是非 | 形式の整合: 各 todo 行に完了条件がある、同時実行行の allowed_files が互いに素、各 P1 行がボトルネック id に対応、DoD が「コマンド + 期待出力」で書かれている、各決定に既定値と期限がある、相互参照（PR 番号、ブランチ、タスク id、節番号）が実在する | プログラム | `plan-check.py`（task-consistency-check と同型。plan 群 5 文書を読み、違反 1 行 1 件で exit 1）。`validate` CI に追加 | P1-12 に含める |
| 〃 | 実態との drift: plan の PR/ブランチ/head/状態が gh と git の現在値と一致、progress.tsv の state が受け入れ記録と一致 | プログラム | `plan-check.py --drift`（boundary ごとに実行、不一致を progress に書く） | P1-12 |
| 〃 | 方向の不変条件: 禁止事項（Anthropic OAuth、main への直接 push、`--admin`、人の ask を増やす設定）が plan と diff に無い | プログラム | `plan-check.py --invariants`（禁止パターンの grep と validator 連携） | P1-12 |
| 〃 | 起案、再計画（S1 後）、見積もりの更新、進行中作業の分類（規則表に従う） | AI | 第 3 節の分類規則（Claude/Codex 専用 → E 後に不要、ハーネス非依存 → 継続）と plan 第 8 節のモデルを AI が適用し、plan-check を通してから提示 | orchestrator |
| 〃 | 方向と価値の決定（どのハーネスか、どのベンダーか、費用上限、品質閾値の変更、範囲の増減） | **人** | decisions.tsv に `scope=direction` の行として記録。既定値なし | ユーザー |
| hold（S1 / INV-6 / P0） | 検知と凍結: 同一クラス 3 回、revise 2 回、P0 の出現で artifact を止め、`re-plan:` 行の雛形と `search:` 行を出す | プログラム（既存を拡張） | `three-repeat.sh` + counters + verdict の hold。凍結は `dispatch.sh` が hold 中の task への TASK/revise 送信を拒否 | P1-4a |
| 〃 | クラス別の是正手順（playbook）: `.orchestration/learning/classes.yaml` の各 class に `remedy:`（例: `string-form-comparison` → 正規化関数経由に置換、`ps-output-parsing` → 起動時 JSON 記録との照合、`records-form` → 記録生成の自動化）と `blast_radius:`（許される変更範囲） | プログラム + AI | `hold-playbook.sh <task> <class>`: remedy を再計画の骨格に展開し、変更範囲が task の allowed_files 内なら AI が再計画を書いて再 dispatch（決定不要）。範囲外なら決定パネル行を生成 | 新 P1-13 |
| 〃 | P0（セキュリティ）の即時対応: 修正 forward か revert かの選択 | AI（規則） | 規則: main に入っていれば revert PR を即時、未マージなら hold。例外なし | P1-4a の verdict |
| 〃 | 残存リスクの受容（P0/P1 を直さずに進む）、期限や範囲を変える再計画 | **人** | `D-…-residual-risk` 行。既定値なし | ユーザー |
| not-applicable の refutation | 形の検査: refutation は 3 形式のどれか。(i) `test:<selector>` が所見の前提を再現しない（実行して pass を貼る）、(ii) `source:{url, fetched_at, quote}` が所見と矛盾（quote が取得ページに実在することをハッシュで確認）、(iii) `diff:<range>` で該当経路が到達不能（静的）。所見の file:line が実在、空文・一般論は拒否 | プログラム | `dispositions.py --require-refutation` の 3 形式検査 + 再現コマンドの実行と出力の貼り付け | P1-10 |
| 〃 | 妥当性の判断（P2/P3）: 2 モデルの独立判定の一致 | AI（合議） | `audit-pool.sh --second-opinion <finding>`: audit profile と security profile（または別ベンダー）に refutation を渡し、両方が「所見は成立しない」なら受理。不一致は hold | P1-10 + P1-4a |
| 〃 | 妥当性の判断（P0/P1）で 2 モデルが不一致、または根拠がコマンドで検証できない外部事実（契約条項、業務意図） | **人** | 残存リスクの受容と同じ決定行 | ユーザー |
| trust-boundary タスクのタスク文レビュー | 形の検査: 3 つの形の規則（test selector、sentence、owning task id）、threat_table の単位規則（allowed_files 1 行につき 1 行、非パス制御 1 つにつき 1 行、orchestrator 効果 1 つにつき 1 行）、各行の disposition が `closed`（テストあり）/ `residual`（制御あり）/ `out-of-scope`（owner 実在）、premises が実行出力、invariants の設計文と byte 一致（INV-2） | プログラム | `task-consistency-check.py` の拡張（C11〜C15） | P1-12 |
| 〃 | 内容のレビュー（threat の見落とし、制御の妥当性） | AI（独立モデル、1 ラウンド固定） | 既存の headless review（Codex review profile）を `security: true` のタスクだけに限定。停止条件は SKILL の既定 | 既存 |
| 〃 | 権限・信頼境界を広げるタスク（excludedCommands、allowMachLookup、hooks で gh 書込を決める、sandbox の allowWrite） | **人** | 下の「権限の変更」に合流 | ユーザー |
| ruleset と権限の変更 | 検知: 権限面（`permissions.*`、`excludedCommands`、`allowMachLookup`、`allowWrite`、`allowedDomains`、gh 書込を決める hook、ruleset パラメータ）の diff を機械で抽出し、`D-… scope=permission approved_by=user diff_sha256=<…>` の決定行が無ければ validator と CI が fail | プログラム | `permission-guard.py`（validate CI。diff の sha256 と決定行を照合） | 新 P1-14 |
| 〃 | 提案: 最小の広げ方と threat_table、現在値との diff、適用後の検証 | AI | `ruleset-request.sh`（望む ruleset JSON と現在値の diff を出す）、`ruleset-verify.sh`（適用後に一致を確認し progress に書く） | P1-14 |
| 〃 | 承認そのもの。トークンに権限が無い管理者操作（ruleset のトグル）、資格情報の投入（OAuth ログイン、API キー、relay トークン） | **人** | 構造上の制約（権限・資格情報は人が保持）。plan の「ユーザーが必要なこと」欄に時機付きで明記 | ユーザー |

結論: 5 項目のうち機械とAI で吸収できる部分を除くと、人に残るのは (a) 方向と価値の決定、(b) P0/P1 の残存リスクの受容、(c) 権限・信頼境界を広げる変更の承認、(d) トークンに権限が無い管理者操作と資格情報の投入、の 4 つ。(c)(d) は能力ではなく権限の所在による。新規タスクは P1-13（hold playbook）と P1-14（permission guard と ruleset 補助）の 2 本。

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


 exited 1 in 105ms:
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
test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) ... 
  test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) (old=None) ... FAIL
  test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) (old={}) ... FAIL
  test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) (old={'oauthAccount': {'accountUuid': 'synthetic', 'emailAddress': 'test@example.invalid'}, 'userID': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'numStartups': 5, 'hasCompletedOnboarding': False, 'projects': {'/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/herdr-agents-test-cocab53r/home/Workspace/dotfiles': {'history': ['discard'], 'allowedTools': ['*']}}, 'futureState': {'command': 'payload-value'}}) ... FAIL
test_worker_start_regenerates_shared_global_state_across_worktrees (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_shared_global_state_across_worktrees) ... FAIL
test_worker_start_refuses_nonempty_global_mcp_servers (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_nonempty_global_mcp_servers) ... FAIL
test_worker_start_refuses_nonstring_oauth_account_member (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_nonstring_oauth_account_member) ... FAIL
test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) ... 
  test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) (name='CLAUDE_CODE_USE_BEDROCK') ... FAIL
  test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) (name='AWS_CONFIG_FILE') ... FAIL
  test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) (name='AWS_SHARED_CREDENTIALS_FILE') ... FAIL
  test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) (name='AWS_PROFILE') ... FAIL
test_worker_start_refuses_undeclared_provider_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_undeclared_provider_selectors) ... FAIL
test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) ... 
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S01', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S01', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S01', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S01', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S02', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S02', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S02', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S02', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S03', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S03', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S03', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S03', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S04', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S04', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S04', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S04', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S05', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S05', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S05', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S05', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S06', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S06', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S06', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S06', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S07', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S07', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S07', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S07', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
test_project_sandbox_extensions_are_refused_before_launch (tests.unit.test_herdr_agents.HerdrAgentsTest.test_project_sandbox_extensions_are_refused_before_launch) ... FAIL
test_worker_start_refuses_object_plugin_command_components (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_object_plugin_command_components) ... FAIL
test_worker_start_requires_string_component_references (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_requires_string_component_references) ... FAIL
test_managed_skills_use_actual_managed_root (tests.unit.test_herdr_agents.HerdrAgentsTest.test_managed_skills_use_actual_managed_root) ... FAIL
test_worker_start_refuses_foreign_repository_root (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_foreign_repository_root) ... ok
test_worker_start_refuses_planted_claude_env_file_contents (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_planted_claude_env_file_contents) ... FAIL
test_install_target_creates_managed_parent_in_printed_commands (tests.unit.test_claude_managed_settings.ClaudeManagedSettingsTest.test_install_target_creates_managed_parent_in_printed_commands) ... ok
test_update_reconciles_settings_after_herdr_install (tests.unit.test_claude_settings_merge.ClaudeSettingsMergeTest.test_update_reconciles_settings_after_herdr_install) ... FAIL

======================================================================
FAIL: test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) (old=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_herdr_agents.py", line 5470, in test_worker_start_regenerates_global_state_with_screened_identity
    self.assertEqual(result.returncode, 0, result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : worker startup refused: launch environment: __CF_USER_TEXT_ENCODING: undeclared environment input


======================================================================
FAIL: test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) (old={})
----------------------------------------------------------------------
Traceback (most recent call last):
--- .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md	2026-10-20 16:34:09
+++ .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md	2026-10-21 00:12:59
@@ -1,6 +1,6 @@
 ---
 format: 2
-task_id: dotfiles-T133-worker-write-boundary-a03
+task_id: dotfiles-T133-worker-write-boundary-a04
 kind: code
 security: true
 allowed_files:
@@ -25,9 +25,11 @@
   - tests/unit/test_agmsg_orchestration_docs.py
   - tests/unit/test_claude_worker_settings.py
   - tests/unit/test_claude_managed_settings.py
-  - .orchestration/dotfiles-T133-worker-write-boundary-a03/**
+  - .orchestration/dotfiles-T133-worker-write-boundary-a04/**
 after: []
-reset_of: [dotfiles-T133-worker-write-boundary-a02]
+reset_of: [dotfiles-T133-worker-write-boundary-a03]
+retained_predecessor_directories:
+  - .orchestration/dotfiles-T133-worker-write-boundary-a03/
 threat_table:
   - control: home/dot_agents/agent-config.yaml
     disposition: "residual: the manifest declares the static protected inputs and closed worker-start schema; render tests check their correspondence without establishing same-UID isolation or complete executable binding."
@@ -71,7 +73,7 @@
     disposition: "residual: render, merge, deny and guard fixtures verify configured policy and unchanged protected bytes without executing a bound PermissionRequest hook."
   - control: tests/unit/test_claude_managed_settings.py
     disposition: "residual: administrative-content and printed-command fixtures use temporary destinations and sudo markers; actual administrative installation remains an operator step."
-  - control: .orchestration/dotfiles-T133-worker-write-boundary-a03/**
+  - control: .orchestration/dotfiles-T133-worker-write-boundary-a04/**
     disposition: "residual: evidence separates inherited observations, new regressions and final-head results, and records pending deployment without credentials or literal operator home paths."
   - control: <absolute-home>/.claude-worker/settings.json
     disposition: "residual: S01 is checked before regeneration under the closed settings schema, including every environment entry; a later same-UID replacement remains outside the startup guarantee."
@@ -135,6 +137,12 @@
     disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch"
   - control: pre-start refusal of untrusted executable environment-file contents
     disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents"
+  - control: manifest-selected non-shim launch interpreter
+    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names"
+  - control: Darwin platform-injected launch environment
+    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment"
+  - control: regime-declared launch environment
+    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment"
   - control: plugin activation and additional executable components
     disposition: "residual: explicit false entries supplement screening; higher-scope enables, sync, dependencies, workflows, monitors and undeclared components refuse before launch."
   - control: non-file managed delivery and launch overrides
@@ -143,20 +151,20 @@
     disposition: "residual: source-specific canonical fragments reject extra exclusions, write roots and socket grants before Claude can merge arrays; live enforcement and later changes remain unverified."
   - control: actual enterprise skills root
     disposition: "residual: inventory starts at <managed-root>/.claude/skills, and temporary managed-root fixtures plant both Markdown and bundled plugin payloads there on both platforms."
-  - control: ~/.agents/permgate-policy.yaml
+  - control: <absolute-home>/.agents/permgate-policy.yaml
     disposition: "residual: explicit static Edit denies protect the policy input and fixtures assert unchanged bytes; legacy hook environment and execution binding remain deferred."
-  - control: ~/.local/lib/python*/site-packages
+  - control: <absolute-home>/.local/lib/python*/site-packages
     disposition: "residual: directory-target and descendant denies retain protection for .pth, usercustomize.py and sitecustomize.py without claiming isolated interpreter startup."
-  - control: ~/Library/Python/*/lib/python/site-packages
+  - control: <absolute-home>/Library/Python/*/lib/python/site-packages
     disposition: "residual: macOS user-site directory and descendant patterns remain in the static inventory; planted-startup execution belongs to the binding task."
-  - control: ~/.claude/hooks/orchestrator-only.sh
+  - control: <absolute-home>/.claude/hooks/orchestrator-only.sh
     disposition: "residual: the installed guard is an explicitly protected consumed input; routing fixtures do not close concurrent same-UID path swaps."
   - control: formatter and project-map configuration selection
     disposition: "residual: worker and outside-anchor input paths suppress tool execution; formatter availability and complete tool-chain binding remain deferred."
-  - control: .orchestration/dotfiles-T133-worker-write-boundary-a02/task.md
-    disposition: "residual: C3 authorizes deletion of this predecessor copy on the first a03 push only; all other predecessor artifacts and canonical history remain untouched."
   - control: .orchestration/dotfiles-T133-worker-write-boundary-a03/task.md
-    disposition: "residual: the replacement copy is byte-identical to the dispatched a03 text and bound by SHA256 in TASK and RESULT."
+    disposition: "residual: retain the predecessor task copy and all a03 evidence unchanged in the declared retained predecessor directory; neither deletion nor new predecessor writes is authorized."
+  - control: .orchestration/dotfiles-T133-worker-write-boundary-a04/task.md
+    disposition: "residual: the a04 copy is byte-identical to the complete dispatched a04 text and bound by SHA256 in TASK and RESULT."
   - control: evidence records
     disposition: "residual: report, validation, sandbox, learning, autoskill and review records preserve commands and identities while distinguishing proposals from acceptance authority."
   - control: task metadata
@@ -166,7 +174,7 @@
   - control: in-process effects
     disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no deployment, login, administrative installation or restart."
   - control: workflow and interpreter or environment inputs
-    disposition: "residual: trusted parents supply clean environments before child execution and Python runs isolated; this task does not restore deferred version declarations or complete executable binding."
+    disposition: "residual: trusted parents supply clean environments and the manifest-named absolute non-shim mise Python runs isolated; role-specific runtime-name screening does not establish complete executable binding."
   - control: new or renamed scripts
     disposition: "residual: policy stays in the existing renderer, preparation script and guard; no new wrapper, state helper, interpreter resolver or executable-link manager is introduced."
   - control: "5.14 item 0: 脅威モデル"
@@ -205,45 +213,56 @@
     disposition: "residual: none is planned; existing dirty-worktree protections remain and any operator-authorized discarded state must be recorded."
 premises:
   - claim: >-
-      This is the C-61 reset of a02 after both worker rounds were spent.
-      Continue PR 431 on tools/worker-write-boundary-a01 from
-      c0f50fa1383416240ad28959dbc4635afa777175, retaining its implementation.
-      The preceding dispatched task and committed copy have SHA256
-      ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50.
-    sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md]
+      INV-6 carries three a03 amendments; plan 006 S2 requires design by another authoring context. This review-profile context supplies a04, reset_of a03, rather than another a03 amendment. Read-only rechecks on 2026-10-20 confirmed worker-e remains at c0f50fa1383416240ad28959dbc4635afa777175 on tools/worker-write-boundary-a01. Keep PR #431 and the uncommitted a03 implementation/test draft. The canonical a03 text and retained worker task copy both hash to 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b.
+    sources:
+      - .orchestration/plans/006-regime-v3-execution.md
+      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md
+      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
+    executed_commands:
+      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" rev-parse HEAD', output: 'c0f50fa1383416240ad28959dbc4635afa777175'}
+      - {command: 'git -C "$HOME/Workspace/dotfiles/.claude/worktrees/worker-e" symbolic-ref --short HEAD', output: 'tools/worker-write-boundary-a01'}
+      - {command: 'shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md', output: 'both files: 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b'}
   - claim: >-
-      The complete c0f50fa1 security review found AWS credential-chain
-      selectors, a foreign-repository main-local inventory gap and
-      object-form plugin command mappings. The local review found the
-      incorrect enterprise skills root, lower-scope sandbox extensions,
-      missing privileged parent creation and post-Herdr settings drift.
-      The local chain stopped before a task-level audit; none exists for
-      c0f50fa1. Repeated renderings in the local report are four findings,
-      not additional independent findings.
+      The blocked PONG reports probe exit 0, test exit 1, zero worker correction rounds and zero independent pre-push reviews. Its green-new.log is a failing uncommitted draft: 15 tests, 45 failures, including undeclared runtime names, noncanonical TMPDIR and unreconciled fake-update hooks; it is not a RESULT or final green evidence. Retain it without relabeling.
     sources:
+      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt
+      - .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log
+  - claim: >-
+      runtime-contract-probe.json supplies the exact name lists below. Read-only repetition at 2026-10-20T14:57:54Z produced the same names, exit statuses and spawn digest, without a live worker or private settings. The manifest currently lacks the non-shim interpreter declaration; a04 must add it within its existing launcher policy, not discover it through PATH.
+    sources: [.claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json]
+    repeated_probe:
+      supplied_environment_names: [HOME, LANG, PATH, TERM]
+      child_code: 'import os,json,pathlib,platform,pwd,tempfile,subprocess;print(json.dumps(sorted(os.environ)))'
+      interpreters:
+        - command: '/usr/bin/python3 -I -c <child_code>'
+          exit: 0
+          observed_names: [CPATH, HOME, LANG, LIBRARY_PATH, MANPATH, PATH, SDKROOT, TERM, __CF_USER_TEXT_ENCODING]
+          unlisted_names: [CPATH, LIBRARY_PATH, MANPATH, SDKROOT, __CF_USER_TEXT_ENCODING]
+          stderr: "python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead"
+        - command: '"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15" -I -c <child_code>'
+          exit: 0
+          observed_names: [HOME, LANG, PATH, TERM, __CF_USER_TEXT_ENCODING]
+          unlisted_names: [__CF_USER_TEXT_ENCODING]
+          stderr: ""
+      upstream_spawn_sha256: 57ae782bd8a4776ce516d5fd45ba069f7cb50271e985cc2341842376246a3731
+      upstream_spawn_line: 527
+      upstream_spawn_text: "  echo 'export AGMSG_SPAWNED=1'"
+      schema_has_AGMSG_SPAWNED: false
+      live_worker: false
+      private_settings_read: false
+  - claim: >-
+      The complete c0f50fa1 security review found AWS credential-chain selectors, a foreign-repository main-local inventory gap and object-form plugin command mappings. The local review found the incorrect enterprise skills root, lower-scope sandbox extensions, missing privileged parent creation and post-Herdr settings drift. The local chain stopped before a task-level audit; none exists for c0f50fa1. Repeated renderings in the local report are four findings, not additional independent findings.
+    sources:
       - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
       - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
       - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
   - claim: >-
-      D-024-26 retains the write boundary and transfers executable binding.
-      D-024-29 freezes design 5.14; D-024-30 applies it by reference.
-      The 2026-10-20 residual-list entry in this text records the allowlist
-      generalisation without reopening the frozen items.
+      D-024-26 retains the write boundary and transfers executable binding. D-024-29 freezes design 5.14; D-024-30 applies it by reference. The 2026-10-20 residual-list entry in this text records the allowlist generalisation without reopening the frozen items.
     sources:
       - .orchestration/decisions.tsv
       - $HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md
   - claim: >-
-      The inherited read-only version observation is Claude Code 2.1.300.
-      Documentation enumerations fetched at 2026-10-19T20:41:53Z were:
-      settings scopes User, Shared project, Project local, Managed;
-      precedence Managed settings, Command line, Project local settings,
-      Shared project settings, User settings; MCP scopes Local, Project,
-      User; hook types command, http, mcp_tool, prompt, agent; plugin
-      origins @<marketplace>, @inline, @skills-dir, @synced; plugin
-      enablement sources --add-dir, user, project, local, flag, managed;
-      skills roots Enterprise, Personal, Project, Nested, Additional
-      directory, Plugin; account-synced roots remain undeclared. Recheck the installed version
-      and loader before changing implementation.
+      The inherited read-only version observation is Claude Code 2.1.300. Documentation enumerations fetched at 2026-10-19T20:41:53Z were: settings scopes User, Shared project, Project local, Managed; precedence Managed settings, Command line, Project local settings, Shared project settings, User settings; MCP scopes Local, Project, User; hook types command, http, mcp_tool, prompt, agent; plugin origins @<marketplace>, @inline, @skills-dir, @synced; plugin enablement sources --add-dir, user, project, local, flag, managed; skills roots Enterprise, Personal, Project, Nested, Additional directory, Plugin; account-synced roots remain undeclared. Recheck the installed version and loader before changing implementation.
     fetched_at: "2026-10-19T20:41:53Z"
     sources:
       - https://code.claude.com/docs/en/settings
@@ -252,11 +271,11 @@
       - https://code.claude.com/docs/en/plugins/loading
       - https://code.claude.com/docs/en/skills
   - claim: >-
-      C-87: the orchestrator observed the documented ["Where skills live" table](https://code.claude.com/docs/en/skills) at 2026-10-20T04:47:57Z and the read-only loader probe at 2026-10-20T04:50Z. The Enterprise row says "`.claude/skills/<skill-name>/SKILL.md` in the managed settings directory", with Linux example `/etc/claude-code/.claude/skills/<skill-name>/`. The pinned 2.1.300 loader, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3, contains `/.claude/skills/` (11 occurrences), `.claude/skills/` (8), `/etc/claude-code` (6) and `/Library/Application Support/ClaudeCode` (3); the supplied probe excerpt is `LC_ALL=C /usr/bin/grep -a -o -E '…(\.claude/skills|/skills"|skills/)…' <loader> | sort | uniq -c`. These observations bind the enterprise inventory and fixture to `<managed-root>/.claude/skills`.
-    sources: [https://code.claude.com/docs/en/skills, .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md]
+      C-87 inherited observation: the orchestrator observed the documented ["Where skills live" table](https://code.claude.com/docs/en/skills) at 2026-10-20T04:47:57Z and the read-only loader probe at 2026-10-20T04:50Z. The Enterprise row says "`.claude/skills/<skill-name>/SKILL.md` in the managed settings directory", with Linux example `/etc/claude-code/.claude/skills/<skill-name>/`. The pinned 2.1.300 loader, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3, contains `/.claude/skills/` (11 occurrences), `.claude/skills/` (8), `/etc/claude-code` (6) and `/Library/Application Support/ClaudeCode` (3); the historical supplied probe excerpt is `LC_ALL=C /usr/bin/grep -a -o -E '…(\.claude/skills|/skills"|skills/)…' <loader> | sort | uniq -c`. These observations bind the enterprise inventory and fixture to `<managed-root>/.claude/skills`.
+    sources: ["https://code.claude.com/docs/en/skills", ".orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md"]
   - claim: "Worker a010 blocked before any edit (PONG 2694, 2026-10-20T04:00:43Z): the loader persists numStartups at start and hasCompletedOnboarding at onboarding; the orchestrator reproduced the installed-loader probe below, not a live worker start."
     sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md]
-    probe: {executed_by: orchestrator, executed_at: "2026-10-20T04:10Z", loader: "$HOME/.local/share/mise/installs/npm-anthropic-ai-claude-code/2.1.300/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe", format_observed: Mach-O arm64}
+    probe: {executed_by: review-profile-author, executed_at: "2026-10-20T14:57:54Z", loader: "$HOME/.local/share/mise/installs/npm-anthropic-ai-claude-code/2.1.300/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe", format_observed: Mach-O arm64}
     executed_commands:
       - {command: 'shasum -a 256 <loader>', output: '475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3  <loader>'}
       - {command: '<loader> --version', output: '2.1.300 (Claude Code)'}
@@ -264,29 +283,7 @@
       - {command: 'LC_ALL=C /usr/bin/grep -c -a -o hasCompletedOnboarding <loader>', output: '15'}
     quoted_string_probes: [{command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"numStartups"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasCompletedOnboarding"'' <loader>', output: '0'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasTrustDialogAccepted"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"oauthAccount"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"mcpServers"'' <loader>', output: '29'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"enabledMcpjsonServers"'' <loader>', output: '5'}]
   - claim: >-
-      The single source inventory is S01-S23 below plus executable
-      environment-file contents admitted by the launch-input schema. Each parameter denotes
-      every actual matching file, inspected independently before merging.
-      User means the dedicated configuration directory; managed-root is
-      the platform directory containing managed-settings.json.
-      S01 user/settings.json; S02 worktree/.claude/settings.json;
-      S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json;
-      S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json;
-      S07 user/remote-settings.json plus independently enumerated non-file managed delivery;
-      S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json;
-      S10 every other loaded ancestor .mcp.json;
-      S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration;
-      S12 each skills-root/<name>/.claude-plugin/plugin.json;
-      S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json;
-      S15 each admitted plugin-root/.claude-plugin/plugin.json;
-      S16 every default hooks/hooks.json and explicitly referenced plugin hook file;
-      S17 every admitted marketplace-root/.claude-plugin/marketplace.json;
-      S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json;
-      S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file;
-      S22 every applicable subagent Markdown file;
-      S23 every default or referenced plugin LSP file.
-      Non-file managed delivery and caller-selected inputs must fit the
-      same closed schema and read set or cause a named refusal.
+      The single source inventory is S01-S23 below plus executable environment-file contents admitted by the launch-input schema. Each parameter denotes every actual matching file, inspected independently before merging. User means the dedicated configuration directory; managed-root is the platform directory containing managed-settings.json. S01 user/settings.json; S02 worktree/.claude/settings.json; S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json; S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json; S07 user/remote-settings.json plus independently enumerated non-file managed delivery; S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json; S10 every other loaded ancestor .mcp.json; S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration; S12 each skills-root/<name>/.claude-plugin/plugin.json; S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json; S15 each admitted plugin-root/.claude-plugin/plugin.json; S16 every default hooks/hooks.json and explicitly referenced plugin hook file; S17 every admitted marketplace-root/.claude-plugin/marketplace.json; S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json; S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file; S22 every applicable subagent Markdown file; S23 every default or referenced plugin LSP file. Non-file managed delivery and caller-selected inputs must fit the same closed schema and read set or cause a named refusal.
     sources:
       - https://code.claude.com/docs/en/settings
       - https://code.claude.com/docs/en/managed-settings
@@ -295,21 +292,21 @@
       - https://code.claude.com/docs/en/skills
 ---
 
-# AGMSG-TASK dotfiles-T133-worker-write-boundary-a03 — plan 024 P1-15; seat a010
+# AGMSG-TASK dotfiles-T133-worker-write-boundary-a04 — plan 024 P1-15; worker startup screen; seat a010
 
 ## Goal and reset
 
-[memory:decision] Reset a02 after C-61 exhausted its two worker rounds. Worker a010 is Codex in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`. Continue `tools/worker-write-boundary-a01` and PR #431 from `c0f50fa1383416240ad28959dbc4635afa777175`; keep the a02 implementation and open no second PR.
+[memory:decision] Reset a03 under INV-6 and plan 006 S2 through this separate review-profile authoring context. Worker a010 is Codex, security profile, in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`; this task changes Claude's boundary and preserves Codex policy. Continue `tools/worker-write-boundary-a01` and PR #431 from `c0f50fa1383416240ad28959dbc4635afa777175`, keeping the uncommitted a03 draft and all predecessor evidence; open no second PR.
 
-Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Fix the four local-review findings within the same authorized files.
+Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Retain every a03 item and fix, with only the runtime/interpreter decision specified here.
 
-[memory:failure] a01 spent two rounds and a02 spent two rounds. Neither a new task name nor a clean historical test result closes their findings. This explicit reset supplies a03's fresh budget: at most two worker correction rounds in total, including pre-push corrections, and at most one independent pre-push review.
+[memory:failure] a01 and a02 each spent two worker rounds; a03's blocked PONG reports zero worker correction rounds and zero independent pre-push reviews, while its amendment history remains counted. This reset supplies a04 at most two worker correction rounds in total, including pre-push corrections, and at most one independent pre-push review; it erases no predecessor counters or findings.
 
-The current implementation is the starting point, not an approved result. The c0f50fa1 local chain stopped before its task-level audit. Obtain new final-head audit and security evidence; do not describe either as inherited.
+The retained draft is not approved, and its `raw/green-new.log` is explicitly failing. The c0f50fa1 local chain stopped before its task-level audit. Obtain new final-head audit and security evidence; do not describe either as inherited.
 
-Amendment 1 accepts `text-security:f7af699:1`, the sole P1 at line 374 in `.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md.last.md`, and adds only the executable environment-file contents control and its evidence/budget consequences. `previous_sha256: f7af699666211dd95cc3d3addfbbbecee9359b91c7916b1e2e54e47577e2d6d4`. This is task-text amendment 1, not a worker correction round.
+## History
 
-Amendment 2 implements D-024-34, the second input-inventory re-plan after the allowlist, mapping accepted rows `worker:5067ed0:1 input-inventory` and `text-security:f7af699:1 input-inventory` to launcher-generated files. `previous_sha256: 5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669`. The worker blocked before any edit; this is task-text amendment 2, not a worker correction round. It changes S11, identity screening, three fixtures and their budget consequences; the `CLAUDE_ENV_FILE` control rows and fixture remain unchanged. Amendment 3 implements D-024-35, the third input-inventory re-plan, mapping accepted row `text-security:efa211d:1 input-inventory` from C-80 round 3's sole P2 at line 431 in `.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md.last.md`; `previous_sha256: efa211d1fa4e8fc90512fc88acf6e8cad1127d10a74defafe5adab2e2817faf5`. It removes S11's per-project inventory, regenerates `projects: {}` and relies on the existing spawn-readiness trust-dialog acceptance; an A-then-B shared-directory fixture replaces the same-worktree restart fixture. This is task-text amendment 3, not a worker correction round; identity screening, top-level MCP tamper refusal and the `CLAUDE_ENV_FILE` control remain. Amendment 4 accepts `text-security:be969e3:1 input-inventory`, C-80 round 4's sole P1 at line 425 in `.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md`; `previous_sha256: be969e32246c9a1a55e61654d28be9111328fde0e7730a300465bb2e43b0c47e`. It corrects only the enterprise skills root to `<managed-root>/.claude/skills`, the corresponding S12 inventory and fixture, and their C-87 premise; the admitted skills roots are the documented six. This is task-text amendment 4, not a worker correction round; scope, implementation budgets and all other controls remain unchanged.
+a01 and a02 each exhausted their two worker rounds, and a03 reset the lineage to a closed startup schema while continuing PR #431. Its amendments bound executable environment-file contents, regenerated S11 with screened identity and empty shared project state, and corrected the enterprise skills inventory; those controls and their finding history remain. The worker blocked on shim/platform-added runtime names and upstream `AGMSG_SPAWNED=1`, preserving its uncommitted draft and failing evidence. INV-6's three counted a03 amendments trigger plan 006 S2, so another context authors a04 to resolve only that runtime-name/interpreter contract instead of extending a03.
 
 ## Design and finding history
 
@@ -321,9 +318,9 @@
 Item 8 applies to committed approval authority through explicitly host-bound repository API calls.
 Item 9 applies to private caches and the trusted parent's interpreter/cache inputs.
 
-**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a03:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.
+**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a04:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.
 
-Read the full a02 acceptance record and both c0f50fa1 reviews named in `premises:`. Retain the following history and finding classes in the a03 report and acceptance lineage:
+Read the full a02 and a03 acceptance records, a03 task, blocked PONG and both runtime evidence files, and both c0f50fa1 reviews named in `premises:`. Retain the following history and finding classes in the a04 report and acceptance lineage:
 
 | Finding | Class | Required treatment |
 | --- | --- | --- |
@@ -333,7 +330,7 @@
 | `text-security:ebbb71b:3` | repository-binding | Canonical main comes from the fixed repository API. |
 | `text-security:b2a186e:1` | input-inventory | Inspect handler type before command; non-command types refuse. |
 | `text-security:b2a186e:2` | repository-binding | Both ledger calls bind `--hostname github.com`. |
-| `text-security:ac9ce14:0` | correct | Historical text approval only; it does not approve a03. |
+| `text-security:ac9ce14:0` | correct | Historical text approval only; it does not approve a04. |
 | a02 independent pre-push review | input-inventory | Retain fixes for `env.HOME` guard selection and fenced dynamic commands. |
 | `local:79ea98a:1` | tool-environment | Retain manifest-generated `--advisor fable` acceptance. |
 | `local:79ea98a:2` | tool-environment | Retain absolute tool paths and attachment identity environment. |
@@ -350,7 +347,7 @@
 
 S1 first triggered on the three source omissions in 2ae9e2c/ebbb71b. The re-plan enumerated S01-S23, but subsequent findings still exploited open field/value acceptance; the c0f50fa1 security findings bring that post-re-plan family to its sixth finding. This reset changes the approach rather than adding three more denylist entries.
 
-Preserve the advisory-owner history exactly as history. The two c0f50fa1 P2 fixes are explicitly brought into a03 by this text; the orchestrator reconciles their owner rows and updates dependent task references. The worker edits no canonical acceptance or owner task.
+Preserve the advisory-owner history and owner `dotfiles-T133-worker-write-boundary-followup-a01` exactly as history. The two c0f50fa1 P2 fixes are retained from a03 by this text; the orchestrator reconciles their owner rows and updates dependent task references. The worker edits no canonical acceptance or owner task.
 
 Retain D-024-26's transferred binding findings, including `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. Do not relabel them as fixed.
 
@@ -388,6 +385,10 @@
 
 Settings `env` admits exactly `GH_TELEMETRY="false"`, `DO_NOT_TRACK="1"`, `CHECKPOINT_DISABLE="1"` and `AWS_EC2_METADATA_DISABLED="true"`, as declared by the manifest. The last name is the sole declared `AWS_*` exception and cannot select credentials or a provider.
 
+The launch-input schema classifies names by source: existing parent/runtime declarations, `regime-declared`, and `platform-injected`. The latter two classes below are closed enumerations, not prefixes. They do not extend settings `env`, configuration-file keys or CLI arguments.
+
+The launcher and its startup/preflight Python children use only the manifest-named absolute mise-installed non-shim interpreter, observed here as `<validated-home>/.local/share/mise/installs/python/3.15.0/bin/python3.15`. Add that narrow declaration to the existing manifest-owned launcher policy and consume it through the existing renderer; never route through `/usr/bin/python3`, a mise shim, PATH lookup or an interpreter-discovery fallback. Cover startup bootstrap/home lookup as well as preparation. This selects the interpreter for this boundary without returning the deferred complete binding work to scope.
+
 The launch-input schema admits only these names, with source-specific values supplied or checked by the trusted parent:
 
 | Names | Value authority |
@@ -397,9 +398,11 @@
 | `CLAUDE_CONFIG_DIR` | Exactly the dedicated worker directory under the validated home. |
 | `CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` | Parent-bound canonical project identity and runtime shell file; `CLAUDE_ENV_FILE` additionally requires the executable-content control below. |
 | `UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR` | Exactly `<canonical-worktree>/.uv-cache` and its `python` child. |
-| `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE` | `0`, the validated launcher store selection, and the declared monitor value; unset default-store selection remains supported. |
+| `regime-declared`: `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE`, `AGMSG_AGENT_PID` | Retain a03's exact authorities: `0`, validated launcher store selection, declared monitor value and numeric runtime process identifier; unset default-store selection remains supported. |
+| `regime-declared`: `AGMSG_SPAWNED` | Exactly the string `1`, set by upstream `spawn.sh` on the launch surface before the worker CLI; require it on spawn-launched roles and do not synthesize it for unrelated child roles. |
+| `platform-injected`: `__CF_USER_TEXT_ENCODING` | Darwin only; present or absent allowed. A present string must full-match `0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+:0x[0-9A-Fa-f]+`. The regime validates the shape and otherwise never reads or uses it. Linux presence refuses. |
 | `HERDR_ENV`, `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_AGENTS_LAYOUT`, `HERDR_SOCKET_PATH` | Validated control-plane identity, `managed` layout and canonical configured socket; these grant no worker sandbox exception. |
-| `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID`, `AGMSG_AGENT_PID` | Parent/runtime session identifier and numeric process identifiers where required by canonical attachment/delivery. |
+| `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID` | Parent/runtime session identifier and numeric process identifiers where required by canonical attachment/delivery. |
 | `CLICOLOR_FORCE`, `FORCE_COLOR` | Launcher-written `1` only where the launch route uses them. |
 | `GH_TELEMETRY`, `DO_NOT_TRACK`, `CHECKPOINT_DISABLE`, `AWS_EC2_METADATA_DISABLED` | The four fixed values above. |
 | `CHEZMOI_SOURCE_DIR`, `CHEZMOI_HOME_DIR` | Preparation-only trusted source/home bindings; not caller-selected worker configuration or executable roots. |
@@ -416,13 +419,15 @@
 
 Preserve the manifest-generated Claude argument interface: only `--model`, `--effort`, `--advisor` with their declared profile values, including `--advisor fable`. Caller-added settings, MCP, plugin, agent and additional-directory arguments refuse. Keep existing Codex arguments and network/shared-Git policy unchanged.
 
-If the installed loader or an existing launch route requires another name or preserved state field, send a blocked PONG with the exact boundary and evidence. Do not silently widen the schema, introduce wildcard name acceptance or treat a runtime default as authorization.
+A clean-parent probe runs through the interpreter named by the rendered manifest, imports the same modules as the predecessor probe, and asserts `CPATH`, `LIBRARY_PATH`, `MANPATH` and `SDKROOT` are absent. They remain undeclared and refuse if encountered; do not delete them to conceal an unexpected injection. Test the observed child environment as well as the parent's proposed names, with child-role-specific declarations.
 
+Any other new name, source, required state field or interpreter mismatch still blocks and re-tasks. Send a blocked PONG naming the boundary, exact command and status, with probe JSON containing the supplied/observed name lists, undeclared names and interpreter identity under the a04 evidence directory. Preserve the predecessor JSON unchanged. No wildcard, prefix-wide acceptance, candidate-learned schema, suppression or default-as-authorization is allowed; print no environment values.
+
 ### Sources, roots and component forms
 
 The sole repository anchor is the manifest declaration resolving to `$HOME/Workspace/dotfiles`. Bind its identity to the validated passwd home and actual main checkout, resolving symlinks and filesystem case aliases. Worker roots must be registered linked worktrees beneath that anchor's declared `.claude/worktrees/` root with the same Git common directory.
 
-Every worker launch route, for either worker kind, refuses another repository before worktree creation, identity registration, hook writes, workspace trust or spawn. The refusal names this task: `worker startup refused: dotfiles-T133-worker-write-boundary-a03: unsupported repository root`. Do not fix the foreign-root finding by inspecting the fixed anchor while launching elsewhere.
+Every worker launch route, for either worker kind, refuses another repository before worktree creation, identity registration, hook writes, workspace trust or spawn. The refusal names this task: `worker startup refused: dotfiles-T133-worker-write-boundary-a04: unsupported repository root`. Do not fix the foreign-root finding by inspecting the fixed anchor while launching elsewhere.
 
 Admitted configuration roots are the dedicated worker directory, the validated anchor/worktree `.claude` directories, applicable nested worktree and additional-directory `.claude` directories, the platform managed root and contained plugin roots discovered through the declared registry. Inherited MCP files are the independently enumerated ancestor read set. No account-synced, inline, seed, alternate cache or caller-selected root is admitted; caller-added additional-directory arguments remain refused.
 
@@ -459,21 +464,21 @@
 
 5. Keep static `trusted_paths` derived from trusted executable inputs, not Git trees/indexes. Preserve anchored source/control paths, tracked/main-local settings, `.orchestration`, both `.agents/worklog/**` and `.agents/worklog/uv-cache/**`, worktree `.claude` directory/descendant targets and `.mcp.json`. Ordinary worktree source and private cache writes remain available.
 
-6. Retain explicit protection of `~/.agents/agent-config.yaml`, model profiles, permgate policy, skill scripts/SKILL files, agmsg plugin code and `db/trusted-plugins`, `~/.claude/**`, `~/.claude-worker/**`, installed guard, local wrappers/application code, configuration/state/tool installations and shared uv caches. Keep directory and descendant user-site protection for `.pth`, `usercustomize.py` and `sitecustomize.py` on both platforms. Add no blanket `~/.agents/**` or `~/.local/**` deny: agmsg `db`, `teams`, `run`, `ext-tools` stay writable except `db/trusted-plugins`.
+6. Retain explicit protection of `<absolute-home>/.agents/agent-config.yaml`, model profiles, permgate policy, skill scripts/SKILL files, agmsg plugin code and `db/trusted-plugins`, `<absolute-home>/.claude/**`, `<absolute-home>/.claude-worker/**`, installed guard, local wrappers/application code, configuration/state/tool installations and shared uv caches. Keep directory and descendant user-site protection for `.pth`, `usercustomize.py` and `sitecustomize.py` on both platforms. Add no blanket `<absolute-home>/.agents/**` or `<absolute-home>/.local/**` deny: agmsg `db`, `teams`, `run`, `ext-tools` stay writable except `db/trusted-plugins`.
 
 7. Retain separate orchestrator, worker and administrative renders. Worker policy keeps `defaultMode: auto`, sandbox startup failure, disabled unsandboxed requests, empty user exclusions, restricted writes, no user Herdr socket, explicit MCP auto-approval disables, account sync off and false plugin entries including discovered `@skills-dir` identities. Empty maps alone do not disable plugins or replace screening.
 
 8. Administrative settings retain enabled sandboxing, `failIfUnavailable: true`, disabled unsandboxed requests, filesystem enforcement, disabled weaker isolation/Apple Events/all-socket/local-binding switches, exactly the Herdr socket, and exactly these ordered exclusions: `agmsg-dispatch *`, `herdr-agents *`, `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These shared capabilities remain available to every Claude seat and authorize no worker escape. Lower-scope canonical validation rejects extra exclusions, writes or sockets before array merging.
 
-9. Keep the orchestrator managed PermissionRequest command exactly `~/.local/bin/common/permgate claude`, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.
+9. Keep the orchestrator managed PermissionRequest command's existing literal bytes unchanged, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.
 
-10. Trusted parents supply the clean environment before child execution; do not replace this with an in-script self-reexec or caller sentinel. Preserve isolated Python and the existing absolute interpreter conventions. Add no version pins, private executable directory or PATH fallback. Git inspection follows design 5.14's sanitized environment, explicit checkout identity, disabled lazy fetch/hooks/fsmonitor/submodule recursion and disabled external diff/textconv. Do not execute arbitrary task-body shell strings as probes.
+10. Apply design 5.14 by reference for trusted-parent execution, Python isolation and Git inspection. Consume the manifest-named non-shim interpreter specified above on every launcher startup/preflight Python route; add no resolver, helper, private executable directory, PATH fallback or broader version-pin work. Do not execute arbitrary task-body shell strings as probes.
 
 11. Preserve guard routing, fixed payload paths, argument boundaries, stdin and child status. Canonical worker/sibling/unrelated/missing launch identities execute no orchestrator project payload. Only fixed installed worker-delivery operations run for workers. Formatter/map operations also reject worker/outside-anchor tool inputs. Keep tracked settings portable and all existing event/validator markers.
 
 12. Preserve managed SessionStart/PostToolUse/PreToolUse migration, custom-hook ordering, mixed entries, escaped-tilde distinctions, stale replacement and idempotence. For `make update`, reconcile the managed Claude settings after `scripts/update-agent-assets.sh` runs Herdr's installer, using the allowed Makefile/merge/renderer surfaces. Do not edit the updater script or import its unguarded hook as canonical. Verify one effective guarded hook and no managed-settings drift after repeated fake updates.
 
-13. `install-managed-settings` still stages `~/.claude/managed-settings.rendered.json` nonprivileged. Print a quoted privileged `mkdir -p` for the detected administrative parent before the existing quoted `sudo install -m 0644` command. Cover both platform destinations and homes containing spaces. Execute neither privileged command; do not install, log in or restart.
+13. `install-managed-settings` still stages `<absolute-home>/.claude/managed-settings.rendered.json` nonprivileged. Print a quoted privileged `mkdir -p` for the detected administrative parent before the existing quoted `sudo install -m 0644` command. Cover both platform destinations and homes containing spaces. Execute neither privileged command; do not install, log in or restart.
 
 14. Keep all existing validator checks, exact three-entry exclusion fixtures on both platforms, legacy PermissionRequest validity, duplicate-hook checks, ordering/timeouts, freshness, portability and secret/home-path scanning. Add no bound-PermissionRequest mode. `.gitignore` retains `.uv-cache/` as this task's only addition.
 
@@ -503,22 +508,30 @@
 | `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors` | Every prohibited name family, settings/launch placement, exact fixed-value AWS exception, unknown ordinary environment names and noncanonical declared values. |
 | `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_requires_string_component_references` | Scalar file control; object, list, directory, missing file, outside-root reference and unreadable component negatives. |
 | `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch` | Command-free HTTP separately in S01-S07 on both platforms; other documented/unknown/missing/malformed types; other hook-bearing sources; exact indexed refusal. |
-| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_managed_skills_use_actual_managed_root` | Red on c0f50fa1: using the same temporary managed-root fixture as S05/S06 for both Darwin and Linux, plant a Markdown skill at `<managed-root>/.claude/skills/<name>/SKILL.md` and a bundled plugin payload at `<managed-root>/.claude/skills/<name>/.claude-plugin/plugin.json` with hooks; metadata-only control produces explicit disable. |
+| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_managed_skills_use_actual_managed_root` | Retained green baseline on c0f50fa1, accepted by owner PING 2751; do not manufacture a red result: using the same temporary managed-root fixture as S05/S06 for both Darwin and Linux, plant a Markdown skill at `<managed-root>/.claude/skills/<name>/SKILL.md` and a bundled plugin payload at `<managed-root>/.claude/skills/<name>/.claude-plugin/plugin.json` with hooks; metadata-only control produces explicit disable. |
 | `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_project_sandbox_extensions_are_refused_before_launch` | Red on c0f50fa1: `excludedCommands: ["*"]`, `filesystem.allowWrite: ["/"]`, extra sockets and nested unknowns in project/local scopes; canonical administrative controls remain accepted. |
 | `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_creates_managed_parent_in_printed_commands` | Red on c0f50fa1: missing parent, both platforms, quoting, mkdir-before-install, staged JSON and absent executed-sudo marker. |
 | `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_update_reconciles_settings_after_herdr_install` | Red on c0f50fa1: fake Herdr installer re-appends its literal hook, then update reconciliation restores one guarded entry; repeated update preserves custom hooks and produces no managed drift. |
+
+The runtime-name regressions below are required within the unchanged environment and fixture-alignment budgets:
+
+| Selector | Required coverage |
+| --- | --- |
+| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_manifest_interpreter_probe_excludes_xcode_environment_names` | Execute the predecessor's name-only probe through the absolute non-shim interpreter read from the rendered manifest, with only HOME/PATH/LANG/TERM supplied. Assert CPATH, LIBRARY_PATH, MANPATH and SDKROOT are absent; Darwin permits only the declared platform addition. Route fixtures prove bootstrap, home lookup and preflight use that interpreter without invoking the system shim or PATH fallback. Preserve command/status/name-only JSON. |
+| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_platform_injected_environment` | Darwin absent and correctly shaped present controls pass; malformed shapes, wrong types, trailing content and Linux presence refuse before mutation/trust/spawn. The value never selects behavior, a path or an executable and never appears in evidence. An unrelated injected name blocks with probe JSON. |
+| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_validates_regime_declared_environment` | Fake upstream spawn exports exactly AGMSG_SPAWNED=1 before CLI entry; accept it only for the declared child role. Wrong values and undeclared AGMSG names refuse; all four previously declared AGMSG names retain their authority and optionality. Settings env remains limited to its four original pairs. |
 
 The five allowlist classes each have an explicit fixture: unknown key, undeclared provider selector, foreign root, object-form component and non-command handler. Parameterization may share builders but must name every subcase in validation. Do not replace the three required c0f50fa1-red regressions with tests of a new validator alone.
 
 Retain all a02 regressions: old tracked settings, alternate executable fields, inherited project MCP, dedicated global state, skills-directory plugins, per-source S01-S23 coverage, sandbox-only documentation, hostile-GH_HOST templates, private caches, native denials, migration and guarded delivery. The fixture-case source inventory equals the production source inventory; each case plants its payload in the source it claims to exercise.
 
-Retain a02's red/green evidence for `env.HOME`, fenced dynamic commands and the four 79ea98a3 fixes as historical evidence. Do not claim those tests newly fail on c0f50fa1. Update the documentation template test to read the a03 task copy. Update inherited S11 sentinel-preservation/unknown-field-refusal expectations to the discard-and-regenerate contract with `projects: {}`; retain the top-level MCP tamper refusal, and do not keep the old blanket `oauthAccount` refusal or project-entry refusals.
+Retain a02's red/green evidence for `env.HOME`, fenced dynamic commands and the four 79ea98a3 fixes as historical evidence. Do not claim those tests newly fail on c0f50fa1. Update the documentation template test to read the a04 task copy. Update inherited S11 sentinel-preservation/unknown-field-refusal expectations to the discard-and-regenerate contract with `projects: {}`; retain the top-level MCP tamper refusal, and do not keep the old blanket `oauthAccount` refusal or project-entry refusals.
 
-C11: every `closed` row names one exact `tests/<path>::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.
+C11: every `closed` row names one exact `tests/<path>.py::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.
 
 ## Change budget
 
-Changed lines mean additions plus deletions. The starting measurement is `git diff --numstat 51ba5801 c0f50fa1`, not the obsolete a01 estimate. Preserve its complete output and account separately for base-branch changes already merged into c0f50fa1.
+Changed lines mean additions plus deletions. The starting measurement is `git diff --numstat 51ba5801 c0f50fa1`, not the obsolete a01 estimate. Preserve its complete output and account separately for base-branch changes already merged into c0f50fa1. The author repeated this immutable comparison when preparing a04.
 
 For this task's allowed paths, excluding `.orchestration/`, tests and the three regenerated Claude settings templates, that command measures:
 
@@ -537,7 +550,7 @@
 | `scripts/validate-agent-assets.py` | 9 |
 | **Measured starting source total** | **1111** |
 
-The seven allowed test modules measure respectively 103, 15, 206, 935, 104, 310 and 95 changed lines in `allowed_files` order: **1768**. The full historical-base output additionally contains already-merged unrelated source/test rows; list them rather than charging them as new a03 work or editing them.
+The seven allowed test modules measure respectively 103, 15, 206, 935, 104, 310 and 95 changed lines in `allowed_files` order: **1768**. The full historical-base output additionally contains already-merged unrelated source/test rows; list them rather than charging them as new a04 work or editing them.
 
 Amendment 1's read-only sizing counts 24 lines in c0f50fa1's `present`/`read_json`/`write` analogues plus 16 estimated declaration/digest/route lines, and the 42-line non-command-handler fixture plus 18 estimated content/control lines: **40 source / 60 test**. This measured analogue-based estimate is not a measured implementation result.
 
@@ -560,15 +573,15 @@
 | Launcher-generated S11, screened identity and empty shared project state; D-024-34/D-024-35, `worker:5067ed0:1` and `text-security:efa211d:1` with `text-security:f7af699:1` as the shared family | 80 | 160 |
 | **Increment ceiling** | **480** | **760** |
 
-The source cap is **1591 = 1111 + 480**; the test cap is **2528 = 1768 + 760**, including amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.
+The source cap remains **1591 = 1111 + 480**; the test cap remains **2528 = 1768 + 760**, including a03 amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. The a04 non-shim interpreter, platform-injected and regime-declared controls fit the existing environment/provider and fixture-alignment increments; no cap increases. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.
 
 RESULT records final per-file numstat, historical-base and final PR merge-base identities, actual source/test totals and per-control attribution. Preserve both the complete historical comparison and the current PR comparison so merged base changes are visible.
 
-Every later amendment maps to accepted review findings and carries `previous_sha256`; the worker raises no cap. Amend Change budget, both operative Check cap sentences and the Checks block together. A measured overrun produces a blocked PONG rather than suppression or an unreviewed text edit.
+Every later amendment maps to accepted review findings and carries `previous_sha256`; the worker raises no cap. Amend Change budget, the operative C-107 Check cap sentence and the Checks block together. A measured overrun produces a blocked PONG rather than suppression or an unreviewed text edit.
 
 ## Out of scope
 
-D-024-26 still assigns exact host-probed uv/Python/Node declarations, mise pins, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.
+D-024-26 still assigns exact host-probed uv/Python/Node version declarations and mise pins beyond a04's narrow launch-interpreter selection, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.
 
 Keep `home/dot_mise/config.toml`, the installed state-helper source, Codex boundary sources and updater scripts outside scope. No binding-only code returns through shared files. Add no write-boundary Python hook, gh wrapper, credential-directory substitute, installation discovery or PATH fallback.
 
@@ -588,13 +601,11 @@
 
 Run `uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` and `uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs -v` inside the worker sandbox with its private cache. Preserve complete outputs, statuses and tested identities.
 
-The final diff has at most 1591 changed lines outside `tests/` and `.orchestration/`, excluding regenerated `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`.
+The final diff has at most 1591 changed lines outside `tests/`, `.orchestration/`, `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`, and 2528 under `tests/`.
 
-The final diff has at most 2528 changed lines under `tests/`.
-
 Measure the current PR diff against its authenticated merge-base; preserve the historical-base measurement and reconciliation described in Change budget. No unrelated base change becomes an authorized edit.
 
-Validation includes amendment 3's four c0f50fa1-red/after-green S11 fixtures, including sequential A-then-B starts on the shared configuration directory, the three c0f50fa1-red security regressions, all four local-review regressions, every allowlist class, complete S01-S23 case coverage and final green module output. Malformed/unknown retained nested inputs, disabled plugin payloads and shadowed files refuse before mutation; S11 discarded fields are never forwarded. Positive controls retain default seating, canonical delivery, attachment, repeated preparation and ordinary worktree writes.
+Validation includes amendment 3's four c0f50fa1-red/after-green S11 fixtures, including sequential A-then-B starts on the shared configuration directory, the three c0f50fa1-red security regressions, all four local-review cases (enterprise skills retain accepted green baseline coverage), all three runtime-name/interpreter fixtures, every allowlist class, complete S01-S23 case coverage and final green module output. Malformed/unknown retained nested inputs, disabled plugin payloads and shadowed files refuse before mutation; S11 discarded fields are never forwarded. Positive controls retain default seating, canonical delivery, attachment, repeated preparation and ordinary worktree writes.
 
 Both platform renders retain the exact static deny inventory, directory/descendant coverage, narrow writable stores, private caches, MCP/plugin disables and administrative policy. Sandbox-extension fixtures prove startup refusal, rather than merely showing unchanged administrative JSON.
 
@@ -604,19 +615,19 @@
 
 Retain the inherited formatting reproduction at historical base `205fe85c` for the 12 out-of-scope shell files; do not repair them here. Run no local Bats tests. Required Bats results and all required checks come from GitHub Actions before RESULT.
 
-The orchestrator runs the task-consistency checker before dispatch and acceptance against this complete a03 file, using the trusted parent/interpreter/cache contract. C1-C10 and C7b pass, including both C3 task-copy rows; check C11 selectors individually. A separate C-80 security-profile context reviews this reset text before dispatch. These are prerequisites, not results claimed by this draft.
+The orchestrator runs the task-consistency checker before dispatch and acceptance against this complete a04 file, using the trusted parent/interpreter/cache contract. C1-C10 and C7b pass, including both C3 task-copy rows; check C11 selectors individually. A separate C-80 security-profile context reviews this reset text before dispatch. These are prerequisites, not results claimed by this draft.
 
 ## Artifacts, completion and deployment
 
-On the first a03 push, delete `.orchestration/dotfiles-T133-worker-write-boundary-a02/task.md` and add `.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md` byte-identical to the dispatched text. This C3 deletion is the sole authorized predecessor-path exception. Keep all other a01/a02 artifacts and implementation history.
+On the first a04 push, add `.orchestration/dotfiles-T133-worker-write-boundary-a04/task.md` byte-identical to the complete dispatched text. Retain `.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md` and all existing a03 evidence unchanged in `retained_predecessor_directories`; the predecessor is not an allowed write directory. Keep all other a01/a02 artifacts and implementation history as found; the a03 predecessor-deletion instruction does not carry forward.
 
-Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, operator steps, budget attribution and worker review evidence under the a03 artifact directory. Evidence lives in the worker's own worktree; RESULT says so. Use the `-worker-` review-evidence infix. Record durable decisions/failures with CompactionDB markers; the orchestrator owns main-checkout consolidation.
+Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, operator steps, budget attribution and worker review evidence under the a04 artifact directory. Evidence lives in the worker's own worktree; RESULT says so. Use the `-worker-` review-evidence infix. Record durable decisions/failures with CompactionDB markers; the orchestrator owns main-checkout consolidation.
 
 Continue PR #431 on the existing branch from the specified head. Discard no unrelated work. The orchestrator owns base updates and dependent `after:` changes; this task retains `after: []`. Every moved final head receives fresh required evidence.
 
 Every worker command completes inside its sandbox and allowlist. Each gh/git write is an individual command without shell chaining. A boundary failure produces the exact blocked PONG; no permission-gate, tool or shell alternative bypasses it. Do not clear shared Git metadata outside the worker boundary.
 
-Allow at most one independent pre-push review and two total correction rounds, including that review's corrections. Preserve a01/a02 counters separately. Surviving P0/P1 findings are `open:<id>` or `open:review-<review id>` in RESULT and stop integration for the operator's decision; do not start a private third round.
+Allow at most one independent pre-push review and two total correction rounds, including that review's corrections. Preserve a01/a02/a03 counters separately. Surviving P0/P1 findings are `open:<id>` or `open:review-<review id>` in RESULT and stop integration for the operator's decision; do not start a private third round.
 
 Post no `@codex review` comment. Observe automatic final-head reviews within the bounded 15-minute window and record absence as `bot: none`. Required GitHub Actions pass before RESULT. Propose a disposition for every feedback item; the worker resolves no review thread and grants no acceptance.
 
@@ -624,7 +635,7 @@
 
 RESULT names final full head/base/branch, PR, changed files, task-copy SHA256, exact selectors, red/green identities, final numstat/attribution, schema/source/handler/root inventories, installed-version observations, inherited binding-removal inventory, scripts/installed paths, settings destinations, printed installation commands, feedback/dispositions, open findings, counters and all evidence paths. Distinguish historical claims from new final-head results.
 
-Report user-visible changes: this repository's workers alone are supported; unknown settings or environment inputs refuse; every start regenerates global state with `projects: {}`, preserves only screened identity and resets native counters/caches/project history/allowedTools; workspace trust uses the launcher's existing spawn-readiness dialog acceptance; alternate providers/authentication selectors refuse; object/inline components refuse; lower-scope sandbox extensions refuse; actual enterprise skills are inspected. Refusal preserves original bytes and names the source without exposing values.
+Report user-visible changes: this repository's workers alone are supported; unknown settings or environment inputs refuse; launcher startup uses the manifest-named non-shim mise interpreter, Darwin's optional encoding variable has only the declared shape, and upstream AGMSG_SPAWNED is exactly 1; every start regenerates global state with `projects: {}`, preserves only screened identity and resets native counters/caches/project history/allowedTools; workspace trust uses the launcher's existing spawn-readiness dialog acceptance; alternate providers/authentication selectors refuse; object/inline components refuse; lower-scope sandbox extensions refuse; actual enterprise skills are inspected. Refusal preserves original bytes and names the source without exposing values.
 
 Retain user-visible effects of dedicated worker login, static denies also affecting Bash writes, writable agmsg stores except trusted-plugin authorization, private caches, no worker sandbox escape, shared administrative exceptions/socket access, guarded project hooks and unchanged legacy orchestrator PermissionRequest. Formatter availability and complete executable binding remain deferred.
 
@@ -636,20 +647,7 @@
 
 Merge alone establishes no deployment readiness. Record application, administrative installation, login, startup checks and the Codex permgate change before releasing live dependents; mechanisms requiring executable binding also wait for that owner.
 
+Not performed in task authoring: implementation, worker tests, local Bats, deployment, login or restarts. Final-head correctness and live enforcement remain unverified.
+
 ## Checks (pasted by the orchestrator before each send)
 
-Amendment-3 operative caps are **1591 source / 2528 tests**, increments **480 / 760** including this control's **80 / 160**; amendment 3 adds **0 source / 40 tests** to amendment 2. C-99 cap statements updated: Change budget, both Check limits and this Checks statement. The fenced send-1 paste below is reproduced verbatim as historical evidence, including its superseded caps/counts; the orchestrator re-pastes current checker/C11/security/counter results and these limits before send 2. C-80 round 3 found the accepted P2 `text-security:efa211d:1`; round 4, the first after D-024-35's new re-plan line under C-92, found the accepted P1 `text-security:be969e3:1`, addressed by amendment 4's enterprise-root correction with no cap change. Amendment-4 validation is pending; no passing result is claimed here.
-
-```
-a03 reset text for a010 (Codex, worker-e); plan 024 P1-15; PR #431; branch tools/worker-write-boundary-a01; start c0f50fa1383416240ad28959dbc4635afa777175; reset_of a02; security true; after []
-a02 dispatched/task-copy SHA256 ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50; a01 worker rounds 2 spent; a02 worker rounds 2 spent; C-61 prohibits another a02 round
-history: 2ae9e2c incorrect; ebbb71b incorrect -> S1 documented-source re-plan; b2a186e incorrect; ac9ce14 correct; pre-push HOME/fenced-command fixes retained; 79ea98a3 four local fixes retained; c0f50fa1 security 2 P1 + 1 P2; local review four unique findings; no c0f50fa1 task-level audit
-approach: closed settings/environment/source/root/value schema; 2026-10-20 residual-list entry; D-024-29 design freeze; D-024-30 design by reference; D-024-26 binding transfer retained; D-024-31 deployment coupling retained
-measured starting task-owned source 1111 / tests 1768 from git diff --numstat 51ba5801 c0f50fa1; incremental ceilings 400 / 600 (amendment 1 adds 40 / 60 for executable environment-file contents); operative caps 1511 / 2368; final RESULT must contain measured per-file and per-control totals
-pasted 2026-10-20T03:55Z before send 1: task-consistency-check.py: `dotfiles-T133-worker-write-boundary-a03.md: OK`; C11: 6 closed rows, 0 without a `tests/<path>.py::<Class>::<test>` selector; validate-agent-assets.py SECRET_PATTERN: 0 matches; literal home paths: 0; complete text 622 lines before this paste
-C-80: f7af699 incorrect (1 P1: CLAUDE_ENV_FILE contents unbound -> amendment 1, text-security:f7af699:1 input-inventory); 9bd6198 correct (`Verdict: correct`, 86 threat rows and 22 allowed-file entries checked); budget 2 of 3 used
-acceptance counters (scripts/regime-counters.sh, 03:54Z): tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none; worker_fix_rounds 0; independent pre-push reviews 0
-task SHA256: in the AGMSG-TASK line, computed over these final bytes; delivery read marker: this message's messages.db read_at, recorded in the acceptance record; later amendments require an accepted finding mapping and previous_sha256
-```
-
-Not performed by the worker: local Bats, live enforcement, administrative installation, login, permission-policy deployment or session restarts.
\ No newline at end of file

**Limiting read size for design**
exec
/bin/zsh -lc "sed -n '110,135p' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
 succeeded in 12ms:
4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder; a `gh api graphql` call binds the repository through fixed query variables (`owner: "mryfmo"`, `name: "dotfiles"` as constants in the script, passed with `-f`/`-F`) and uses only node ids obtained from a query bound by those variables (verdict a04 C-80 round 5, 2026-10-19): the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged. The sha of canonical `main` comes from the fixed repository's API (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`), never from `git ls-remote origin`, whose destination the local remote and URL-rewrite configuration control (P1-12 a04 C-80, 2026-10-19T20:01Z); the content read at that sha comes from `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>`. Every `gh api` call that decides also binds the host with `--hostname github.com` (`GH_HOST` and the hosts configuration select the API host otherwise), a subcommand binds it through the `github.com/mryfmo/dotfiles` form of `--repo`, and a test that exports a hostile `GH_HOST` shows the call still names github.com or refuses (a02 review b2a186e, 2026-10-19T20:36Z).
9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.
10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

exec
/bin/zsh -lc "cat .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/runtime-blocked-pong.txt .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/runtime-contract-probe.json; sed -n '1,32p' .claude/worktrees/worker-e/.orchestration/dotfiles-T133-worker-write-boundary-a03/raw/green-new.log" in ~/Workspace/dotfiles
 succeeded in 0ms:
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
test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) ... 
  test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) (old=None) ... FAIL
  test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) (old={}) ... FAIL
  test_worker_start_regenerates_global_state_with_screened_identity (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_global_state_with_screened_identity) (old={'oauthAccount': {'accountUuid': 'synthetic', 'emailAddress': 'test@example.invalid'}, 'userID': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'numStartups': 5, 'hasCompletedOnboarding': False, 'projects': {'/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/herdr-agents-test-cocab53r/home/Workspace/dotfiles': {'history': ['discard'], 'allowedTools': ['*']}}, 'futureState': {'command': 'payload-value'}}) ... FAIL
test_worker_start_regenerates_shared_global_state_across_worktrees (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_regenerates_shared_global_state_across_worktrees) ... FAIL
test_worker_start_refuses_nonempty_global_mcp_servers (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_nonempty_global_mcp_servers) ... FAIL
test_worker_start_refuses_nonstring_oauth_account_member (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_nonstring_oauth_account_member) ... FAIL
test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) ... 
  test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) (name='CLAUDE_CODE_USE_BEDROCK') ... FAIL
  test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) (name='AWS_CONFIG_FILE') ... FAIL
  test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) (name='AWS_SHARED_CREDENTIALS_FILE') ... FAIL
  test_worker_start_refuses_aws_credential_chain_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_aws_credential_chain_selectors) (name='AWS_PROFILE') ... FAIL
test_worker_start_refuses_undeclared_provider_selectors (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_undeclared_provider_selectors) ... FAIL
test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) ... 
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S01', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S01', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S01', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S01', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S02', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S02', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S02', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S02', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S03', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S03', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S03', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S03', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S04', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S04', payload={'sandbox': {'futureHarmless': False}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S04', payload={'permissions': {'allow': []}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S04', payload={'sandbox': {'network': {'future': []}}}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S05', payload={'futureHarmless': False}) ... FAIL
  test_worker_start_refuses_unknown_settings_keys (tests.unit.test_herdr_agents.HerdrAgentsTest.test_worker_start_refuses_unknown_settings_keys) (source='S05', payload={'sandbox': {'futureHarmless': False}}) ... FAIL

**Evaluating design and security bindings**
**Analyzing path and symlink handling**
codex
参照記録では、前回の「managed skills の場所」の指摘は後に訂正され、現案は `<managed-root>/.claude/skills` を採用しています。今回はその指摘を繰り返さず、親プロセスの環境・Git の識別・起動後に読むファイルが、検査した対象と一致する契約になっているかを確認しています。
exec
/bin/zsh -lc "sed -n '107,109p' .orchestration/plans/024-design-quality.md; sed -n '40,65p' .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md; rg -n '"'^(after:|  - |.*gh|.*GIT_|.*shim|.*realpath|.*symlink)'"' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md" in ~/Workspace/dotfiles
 succeeded in 48ms:
1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19). The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).
2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.
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
7:after: [dotfiles-T133-worker-write-boundary-a02, dotfiles-T133-ci-efficiency-followup-a04]
10:  - {"path":"home/dot_mise/config.toml","reason":"dotfiles-T133-trusted-entrypoint-pins-a01 pins the real declaration before this task is sent; it is read-only here."}
11:  - {"path":"tests/unit/test_generate_agent_configs.py","reason":"dotfiles-T133-trusted-entrypoint-pins-a01 removes the installed-template legacy literal pin without relaxing synthetic legacy migration cases."}
12:  - {"path":"tests/unit/test_claude_settings_merge.py","reason":"Existing legacy/custom/idempotence cases remain valid through the modify script's native expansion; run this real module unchanged."}
13:  - {"path":"tests/unit/test_statusline_tools.py","reason":"Its native renderer must continue to parse the template without deployment installations; run unchanged."}
14:  - {"path":"tests/unit/test_herdr_agents.py","reason":"The synthetic SessionStart-only template is unaffected; retain its tests."}
15:  - {"path":"tests/install/common/lifecycle.bats","reason":"Legacy migration fixture data is retained; Bats runs only in GitHub Actions."}
16:  - {"path":"tests/fixtures/gate-evidence/pr-feedback-right.json","reason":"Historical feedback fixture text is data and is not rewritten."}
17:  - {"path":"scripts/orchestrator/trusted-interpreter.sh","reason":"The a04 resolver remains read-only for its existing consumers. This re-plan's launcher validates the exact Python declared by its parent-selected manifest; it must not impose the resolver's production-only pin on fixture execution."}
18:  - {"path":"home/dot_local/bin/common/executable_permgate","reason":"Unchanged dependency-free script, executed through explicit isolated Python rather than its shebang."}
19:  - {"path":"home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","reason":"Complete guard, delivery and formatter/map descendant binding is outside this split; retain its named deployment residuals."}
21:  - {"control":"home/dot_agents/agent-config.yaml","disposition":"residual: Declare exact home-relative uv, Python and node identities and compare their production versions with the read-only mise declaration; deterministic rendering supplies the launcher manifest, while protected inputs still share the OS uid."}
22:  - {"control":"home/.chezmoitemplates/claude-settings-managed.json","disposition":"residual: Render the PermissionRequest exec-form clean prefix with an exact absolute --manifest operand and retain onFailure block; no outer shell starts, but the hook host and first executable's loader environment remain outside launcher validation."}
23:  - {"control":"home/dot_claude/modify_private_settings.json","disposition":"residual: Classify the legacy form separately and compare the bound command string and ordered args array, including --manifest, exactly with the rendered canonical exec form; preserve raw quoting distinctions, custom hooks and idempotence."}
24:  - {"control":"home/dot_claude-worker/modify_private_settings.json","disposition":"residual: Apply the same native expansion and exact bound command/args comparison to this consumer without importing live orchestrator settings or adding an event the surface lacks."}
25:  - {"control":"scripts/generate-agent-configs.py","disposition":"residual: Render exact relative declarations, the launcher manifest data and exec-form command/args without filesystem discovery; ordinary generation and render-check require no installed tools or deployed manifest."}
26:  - {"control":"scripts/validate-agent-assets.py","disposition":"residual: Validate exact rendered command/args and expose the opt-in effective-settings identity check; checker and yaml-importing children consume the same parent-selected manifest, verified uv/Python and private cache without substituting production pins into fixtures."}
27:  - {"control":"Makefile","disposition":"residual: Expose concrete manifest preparation, trusted seed and deployment-check commands and give the formatter the pinned node directory; unrelated inherited recipes remain outside this boundary."}
28:  - {"control":"scripts/orchestrator/trusted-launch.sh","disposition":"residual: Before any declared binary executes, validate the absolute parent-selected manifest and optional fixture root, parse declarations as data, require canonical regular executable paths and compare exact versions; fixture and production inputs use these same checks, while concurrent same-UID replacement remains possible."}
29:  - {"control":"tests/unit/test_claude_managed_settings.py","disposition":"residual: Exercise exact exec-form rendering, migration, a real fixture-manifest uv/Python/permgate execution and the separate pinned-installation case; fixture execution proves the shared launcher path, not production installation or administrative protection."}
30:  - {"control":"tests/unit/test_validate_agent_assets.py","disposition":"residual: Exercise manifest containment, shim, symlink, worker-root and version refusals, quote-preserving comparisons and the clean online seed; recording fake uv cases prove argv and refusal behavior only."}
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
43:  - {"control":"design 5.14 item 1 executable inputs","disposition":"residual: Retain P1-15 protection of policy, user-site locations, settings, rendered manifest and installed tools; executable binding alone does not protect mutable inputs."}
44:  - {"control":"design 5.14 item 2 trusted parent","disposition":"residual: Exec form starts /usr/bin/env -i with literal argv before the privileged launcher validates entry state and the selected manifest; the hook host and loader starting /usr/bin/env still require host-supplied clean execution or the P1-16 OS user boundary."}
45:  - {"control":"design 5.14 item 3 resolved boundaries","disposition":"residual: Apply canonical path, regular-file, shim, worker-root and temporary-root checks to the supplied manifest and its declarations; the explicitly named fixture root is a scoped test allowance, not a production setting."}
46:  - {"control":"design 5.14 item 4 verified executable","disposition":"residual: Execute only the checked declared realpaths without rediscovery and record the selected manifest identity; unrestricted same-UID replacement after validation remains possible."}
47:  - {"control":"design 5.14 item 5 output identity","disposition":"residual: Record full base/head identities, task-copy hash and manifest hashes; no new reservation or slot lock is introduced."}
48:  - {"control":"design 5.14 item 6 honest residuals","disposition":"residual: Report declaration checks, real fixture execution, the named pinned-installation skip, CI and operator-host deployment separately; no fixture or skip substitutes for production evidence."}
49:  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the eight named regressions and scoped hostile-input cases, recording Class::test selectors without claiming system-wide closure or treating an earlier refusal as coverage of a later check."}
50:  - {"control":"design 5.14 item 8 authenticated evidence","disposition":"residual: A parent-selected manifest supplies executable declarations, not permission or merge approval; integration evidence and live agmsg hardening retain their separate owners."}
51:  - {"control":"design 5.14 item 9 isolation and cache","disposition":"residual: Bound Python children use -I and isolated offline uv with an absolute parent-supplied private cache; the explicit online seed uses the same manifest, clean parent and verified uv/Python, retaining --no-config --no-project --isolated --with pyyaml --python and -I while omitting only --offline."}
52:  - {"control":"design 5.14 item 10 sandbox","disposition":"residual: Every worker command stays inside the sandbox; denial produces blocked evidence without escalation or an alternative execution surface."}
54:  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/uv/\" | paste -sd '|' -","output":"0|0.12|0.12.17|0.12.18|0.12.19|0.12.20|0.13|0.13.0|0.13.1|global|latest"}
55:  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/uv/0.13.1/\" | paste -sd '|' -","output":"uv-aarch64-apple-darwin"}
56:  - {"command":"realpath \"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv"}
57:  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/python/\" | paste -sd '|' -","output":"3|3.15|3.15.0|global|latest"}
58:  - {"command":"realpath \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15"}
59:  - {"command":"head -1 \"$HOME/.local/share/mise/installs/npm-prettier/3.9.10/bin/prettier\"","output":"#!/usr/bin/env node"}
60:  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/node/\" | paste -sd '|' -","output":"26|26.12|26.12.0|global|latest"}
61:  - {"command":"realpath \"$HOME/.local/share/mise/installs/node/26.12.0/bin/node\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/node/26.12.0/bin/node"}
62:  - {"command":"grep -nE '^(uv|python|node) = ' home/dot_mise/config.toml | paste -sd '|' -","output":"3:node = \"latest\"|5:python = \"latest\"|17:uv = \"latest\""}
63:  - {"command":"ls -1 .mise.toml mise.toml 2>&1 | paste -sd '|' -","output":"ls: .mise.toml: No such file or directory|mise.toml"}
64:  - {"command":"cat mise.toml | paste -sd '|' -","output":"[tools]"}
65:  - {"command":"grep -n '\"command\": \".*permgate claude\"' home/.chezmoitemplates/claude-settings-managed.json","output":"207:            \"command\": \"~/.local/bin/common/permgate claude\","}
66:  - {"command":"head -1 home/dot_local/bin/common/executable_permgate","output":"#!/usr/bin/env -S uv run --no-cache --script"}
67:  - {"command":"grep -cE '^# ///|^# dependencies[[:space:]]*=' home/dot_local/bin/common/executable_permgate","output":"0"}
68:  - {"command":"sed -n '179,182p' Makefile | paste -sd '|' -","output":"format:| shfmt --indent 4 --space-redirects --diff .| git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check| git ls-files -z '*.md' | xargs -0 prettier --check"}
69:  - {"command":"grep -cE '(^|[[:space:]])(export[[:space:]]+)?PATH[[:space:]:?+]*=' Makefile","output":"0"}
70:  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_agents/agent-config.yaml home/.chezmoitemplates/claude-settings-managed.json home/dot_claude/modify_private_settings.json home/dot_claude-worker/modify_private_settings.json scripts/generate-agent-configs.py scripts/validate-agent-assets.py Makefile tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":"Makefile|home/.chezmoitemplates/claude-settings-managed.json|home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/generate-agent-configs.py|scripts/validate-agent-assets.py|tests/unit/test_validate_agent_assets.py"}
71:  - {"command":"grep -nE '^  - (home/dot_claude-worker/modify_private_settings.json|tests/unit/test_claude_managed_settings.py)$' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | paste -sd '|' -","output":"12:  - home/dot_claude-worker/modify_private_settings.json|27:  - tests/unit/test_claude_managed_settings.py"}
72:  - {"command":"grep -nE '^def (render_claude_settings|render_template_text|validate_claude_settings|validate_model_profile_assets|validate_generated_agent_configs|main|render_managed_template|is_managed_permission_hook)\\(' scripts/generate-agent-configs.py scripts/validate-agent-assets.py home/dot_claude/modify_private_settings.json | paste -sd '|' -","output":"scripts/generate-agent-configs.py:400:def render_claude_settings(manifest: dict[str, Any]) -> str:|scripts/generate-agent-configs.py:1401:def main() -> None:|scripts/validate-agent-assets.py:88:def render_template_text(path: Path, os_name: str = \"darwin\") -> str:|scripts/validate-agent-assets.py:374:def validate_claude_settings(manifest: dict[str, Any], os_name: str = \"darwin\") -> None:|scripts/validate-agent-assets.py:1187:def validate_model_profile_assets(manifest: dict[str, Any]) -> None:|scripts/validate-agent-assets.py:1294:def validate_generated_agent_configs() -> None:|scripts/validate-agent-assets.py:1660:def main() -> None:|home/dot_claude/modify_private_settings.json:48:def render_managed_template(text: str) -> str:|home/dot_claude/modify_private_settings.json:68:def is_managed_permission_hook(hook: Any) -> bool:|home/dot_claude/modify_private_settings.json:196:def main() -> int:"}
73:  - {"command":"sed -n '400,487p' scripts/generate-agent-configs.py | wc -l | xargs","output":"88"}
74:  - {"command":"sed -n '88,100p;374,406p;1187,1265p;1294,1304p;1660,1685p' scripts/validate-agent-assets.py | wc -l | xargs","output":"162"}
75:  - {"command":"sed -n '48,55p;68,79p' home/dot_claude/modify_private_settings.json | wc -l | xargs","output":"20"}
76:  - {"command":"wc -l .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | xargs","output":"63 .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json 95 .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py 1781 tests/unit/test_validate_agent_assets.py 79 home/dot_mise/config.toml 2350 tests/unit/test_generate_agent_configs.py 4368 total"}
77:  - {"command":"ls tests/unit/test_task_consistency_c11_c15.py 2>&1 | paste -sd '|' -","output":"ls: tests/unit/test_task_consistency_c11_c15.py: No such file or directory"}
78:  - {"command":"sed -n '63,66p' .claude/worktrees/worker-g/tests/unit/test_task_consistency_c11_c15.py | paste -sd '|' -","output":"CASES = {|    \"C11\": (|        '\"closed: tests/unit/test_tool.py::test_tool_prints_findings\"',|        '\"closed: tests/unit/test_tool.py::two words\"',"}
79:  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\" --version","output":"uv 0.13.1 (62faed335 2026-10-13 aarch64-apple-darwin)"}
80:  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B --version","output":"Python 3.15.0"}
81:  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/node/26.12.0/bin/node\" --version","output":"v26.12.0"}
82:  - {"command":"rg -l 'claude-settings-managed|is_managed_permission_hook|permgate claude' home scripts tests .github Makefile --glob '!*.md' --glob '!*.lock' | sort | paste -sd '|' -","output":"home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/validate-agent-assets.py|tests/fixtures/gate-evidence/pr-feedback-right.json|tests/install/common/lifecycle.bats|tests/unit/test_claude_settings_merge.py|tests/unit/test_generate_agent_configs.py|tests/unit/test_herdr_agents.py|tests/unit/test_statusline_tools.py|tests/unit/test_validate_agent_assets.py"}
83:  - {"command":"grep -nE '^class (ClaudeManagedSettingsTest|ValidateAgentAssetsTest)' .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":".claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py:12:class ClaudeManagedSettingsTest(unittest.TestCase):|tests/unit/test_validate_agent_assets.py:84:class ValidateAgentAssetsTest(unittest.TestCase):"}
84:  - {"command":"sed -n '117p' .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md | cut -d . -f 1-2","output":"On success print exactly one absolute interpreter realpath and exit 0. On every refusal print exactly one line `trusted-interpreter: refused: <code>` to stderr, print no interpreter on stdout, and exit 2"}
85:  - {"command":"printf '%s\\n' \"$PATH\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/shims:$HOME/.local/bin:$HOME/.local/bin/common:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$HOME/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:$HOME/.local/share/mise/installs/node/lts/bin:/usr/bin:/bin:/usr/sbin:/sbin"}
86:  - {"command":"grep -nE '^    import yaml|PyYAML is required' scripts/validate-agent-assets.py | paste -sd '|' -","output":"22:    import yaml|81:        fail(\"PyYAML is required\")|175:        fail(\"PyYAML is required to validate skill frontmatter\")"}
87:  - {"command":"sed -n '340,346p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | paste -sd '|' -","output":"   Its managed PermissionRequest command remains exactly:||   ```text|   ~/.local/bin/common/permgate claude|   ```||   Do not add an env prefix, guard selector, absolute uv/Python invocation or new command-form validator for this hook. Keep its existing timeout and add the task's common `onFailure: \"block\"` entry policy. The unchanged command's shebang, interpreter discovery and inherited environment are explicit residuals owned by the binding task."}
88:  - {"command":"head -1 .claude/worktrees/worker-e/home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","output":"#!/bin/bash"}
89:  - {"command":"test ! -e scripts/orchestrator/trusted-launch.sh","output":"","exit_status":0}
90:  - {"command":"python3 -I -B -c 'from pathlib import Path; roots=(Path(\"home\"),Path(\".claude/worktrees/worker-e/home\")); print(\"|\".join(str(p) for root in roots for p in sorted(root.glob(\"dot_claude*/modify_private_settings.json\"))))'","output":"home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json"}
91:  - {"command":"python3 -I -B -c 'import os,pwd,stat; from pathlib import Path; h=Path(pwd.getpwuid(os.getuid()).pw_dir); u=h/\".local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\"; r=u.resolve(strict=True); print(\"home_matches_passwd=\"+str(Path.home()==h)); print(\"uv_regular=\"+str(stat.S_ISREG(u.lstat().st_mode))); print(\"uv_symlink=\"+str(u.is_symlink())); print(\"uv_under_passwd_install_root=\"+str(r.is_relative_to(h/\".local/share/mise/installs\"))); print(\"uv_declared_equals_realpath=\"+str(u==r)); print(\"trusted_launch_exists=\"+str(Path(\"scripts/orchestrator/trusted-launch.sh\").exists()))'","output":"home_matches_passwd=True\nuv_regular=True\nuv_symlink=False\nuv_under_passwd_install_root=True\nuv_declared_equals_realpath=True\ntrusted_launch_exists=False"}
92:  - {"command":"rg -n '^    import yaml|PyYAML is required' scripts/generate-agent-configs.py | paste -sd '|' -","output":"14:    import yaml|34:        fail(\"PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py\")"}
93:  - {"command":"sed -n '1294,1298p' scripts/validate-agent-assets.py | paste -sd '|' -","output":"def validate_generated_agent_configs() -> None:|    result = subprocess.run(|        [sys.executable, str(ROOT / \"scripts/generate-agent-configs.py\"), \"--check\"],|        cwd=ROOT,|        text=True,"}
94:  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B scripts/generate-agent-configs.py --check","output":"ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py","exit_status":1}
95:  - {"command":"claude --version","output":"2.1.300 (Claude Code)","exit_status":0}
96:  - {"command":"python3 -I -B -c 'from pathlib import Path; b=(Path.home()/\".local/share/mise/installs/npm-anthropic-ai-claude-code/latest/bin/claude\").read_bytes(); s=b\"Command hooks require `command`. For exec form (no shell)\"; i=b.find(s); print(b[i:b.index(b\"\\0\",i)].decode() if i>=0 else \"missing exec-form help\")'","output":"Command hooks require `command`. For exec form (no shell), set `command` to the executable and `args` to its arguments: {\"type\": \"command\", \"command\": \"echo\", \"args\": [\"hi\"]}. For shell form, set `command` to the full shell string: {\"type\": \"command\", \"command\": \"echo hi\"}.","exit_status":0}
97:  - {"command":"web.open https://code.claude.com/docs/en/hooks#exec-form-and-shell-form","output":"Command hook args present selects direct executable spawn without a shell; args omitted selects shell form (sh -c on macOS/Linux). command is the executable path and args is its argument vector. Documented path placeholders include ${CLAUDE_PROJECT_DIR} and are substituted as plain strings."}
104:Use the security profile for this Claude-boundary change. D-024-26 split this family from P1-15. Read the last 60 lines of .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md and .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-{f810c30,772cde0,e5c055e,5204254}.md.last.md: shebang discovery, Python startup injection, the checker's own execution, shim discovery, the real uv layout and Prettier's node must be handled together.
116:These are two separate task files. This primary task has exactly ten allowed_files entries: eight exact implementation/test paths, one modify-script glob and one evidence wildcard. The glob authorizes only home/dot_claude/modify_private_settings.json and home/dot_claude-worker/modify_private_settings.json, each with its own threat row. An additional match requires a reviewed split. The second file below owns mise pins and the generator assertion; do not combine their front matter or dispatch this task before that prerequisite is accepted.
122:The seven existing concrete allowlist paths were on origin/main at the recorded probe. P1-15 creates the worker modify script and ClaudeManagedSettingsTest module. Add scripts/orchestrator/trusted-launch.sh as the only new executable source. Recheck these paths and measurements on the actual dispatch baseline; refresh changed premises through a reviewed, hashed amendment before dispatch, never only in the Checks paste.
126:The root C11 test file was absent at the recorded probe, and the inspected worker-g copy accepted tests/<path>::<identifier> rather than a Class::test payload. The orchestrator must obtain and read the accepted checker/test revision before dispatch, check C1–C10, C7b and C11, and manually re-probe premises. Never execute arbitrary premise shell strings through an unchecked checker.
136:> A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
144:Declare production uv 0.13.1 at .local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv, Python 3.15.0 at .local/share/mise/installs/python/3.15.0/bin/python3.15, and node 26.12.0 at .local/share/mise/installs/node/26.12.0/bin/node, relative to the real uid's passwd home. A test compares all three production versions with home/dot_mise/config.toml. No wildcard, version alias, latest, shim, traversal or missing required declaration is accepted. If accepted pins differ from these probes, stop for a re-probed amendment rather than substituting an installed version.
156:Validate the launcher entry state before reading the manifest. Retain #!/bin/bash -p, English shdoc comments, the exact accepted clean environment, the canonical non-symlinked launcher pathname under its repository root and HOME equality with the real uid's passwd home. Account explicitly for Bash-maintained environment entries. Refuse rather than repairing the environment or self-re-executing.
158:Resolve the manifest and require a regular, non-symlinked file whose canonical path is under the repository root or, when explicitly supplied, under the canonical fixture root. Reject sibling-prefix lookalikes, path traversal and symlink escapes. A fixture root must be an existing canonical directory; it does not replace passwd HOME, the launcher repository root or the launcher's own entry checks.
163:2. Require a regular executable file, reject a symlinked binary or redirected installation component, and require the declared composed pathname to equal the canonical executable pathname.
164:3. Reject a `shims` path component before and after resolution.
165:4. Reject containment under worker-writable roots, worker caches or temporary roots, including $TMPDIR. The explicitly named fixture root is the sole scoped allowance for fixture files under temporary storage; it does not waive regular-file, symlink, shim, exact-path or version checks. Explicit worker subroots within a fixture remain forbidden.
166:5. Complete identity and containment checks before executing that binary, including a --version probe. Compare the reported version exactly with that manifest's declared pin, then use only the verified absolute realpath.
172:Refusals exit 2, emit exactly one stderr line `trusted-launch: refused: <code>`, and produce no operation output. Use dirty-environment, script-path, home-mismatch, cache-path, manifest-path, manifest-shape, fixture-root, uv-path, python-path, node-path, version-mismatch or invocation for the corresponding failed check. Version probes may run only after path checks; capture their output for validation rather than leaking it into hook stdout. Preserve underlying operation exit status after successful validation. A negative test must reach and assert its intended reason, rather than passing through an earlier refusal.
192:Refuse absent args, shell-form substitutes, missing, reordered or extra args, an altered manifest operand, production --fixture-root, --script, nonisolated Python, shim paths and shell suffixes. Retain ccgate refusal, hook order, duplicate detection, synchronous timeout budgets and onFailure block.
203:- Formatter interpreter check: the same launcher validates the declared node and starts its verified realpath with the probed installed Prettier script. Makefile format PATH includes node's declared bin directory so its env-node shebang resolves.
207:Add --check-effective-settings as an opt-in mode and expose the concrete trusted launch in Makefile. Ordinary validate-agent-assets and render-check stay pure. The opt-in mode reads effective installed settings, requires their exact production wiring and manifest operand, and checks existence, regular/executable identity, canonical protected paths and exact declared versions before operation execution. It consumes checked realpaths without rediscovery. It does not silently create a manifest, provision a cache, install tools or retry online.
213:Retain round 3's bound online-seed decision. The operator's deployment sequence is: make update and deterministic production-manifest preparation, explicit private-cache seed through the trusted parent, then the isolated offline deployment check. The worker does not perform live deployment.
225:The checker and its yaml-importing generator child use that same manifest and cache through the parent. Never substitute the resolver's base Python or sys.executable directly for the uv-provided PyYAML environment.
233:The harness discovers real uv by inspecting shutil.which("uv"), rejecting a shims component before and after resolution, then searching the actual mise uv install root if needed. Prefer the pinned version's directory when present and use the newest exact installed version only as a harness fallback. Handle the probed platform subdirectory rather than assuming <version>/uv. Resolve sys.executable for real Python and reject shims. Record the discovery result, canonical identities and actual versions.
235:The harness renders a fixture manifest with exact declarations and versions for those real tools, then supplies that manifest through --manifest and the test's canonical temporary directory through --fixture-root. HOME remains the real uid's passwd home.
237:The fixture must satisfy exact relative-path composition and containment. If a discovered executable is outside the permitted home/fixture binding, materialize the real executable bytes and the Python runtime support needed for a working installation under the fixture root, using regular files rather than symlink bindings. Verify the copied executable bytes against their discovered sources and verify the staged interpreter actually runs with -I. Copy necessary runtime/stdlib files; do not replace Python with a wrapper or a fake executable. Preserve unchanged real permgate bytes under the fixture root.
239:The launcher sees only the declared fixture paths, validates them through the production code path and compares their actual versions with the fixture pins. Do not pass a runner's external absolute sys.executable as an unchecked exception, redirect production HOME, disable a check, or force the fixture through the production-only mise resolver.
251:Elsewhere, skip only this pinned-installation test with the named reason `pinned-installation-unavailable`, recording the missing exact installation paths. An existing symlinked, malformed, mismatched or otherwise invalid installation is a refusal/failure, not absence and not a skip. Record every such skip in validation.md and report.md. Obtain the real host result during operator deployment; a runner's required fixture execution remains separate.
255:Add or extend these eight regressions in the real existing classes, recording the full selectors and running their unittest dotted equivalents red before implementation and green afterward:
277:- A sibling-prefix or symlink escape outside those roots, also refused with manifest-path.
281:The binary-identity regression uses that accepted fixture-manifest path to reach the intended binary check. Cover a declaration naming a shim, a symlinked binary pointing to a marker-writing fake uv, and a path under an explicitly forbidden worker-writable root. Assert exit 2, the specific uv-path or python-path refusal and absent marker. A prior manifest, HOME or missing-installation refusal does not cover these cases. Also cover an exact-version mismatch after valid path checks.
283:In a separate non-skippable seed subcase, place an argument-recording fake uv as a regular executable at the fixture's declared canonical path. Its --version response matches the fixture pin. Execute the actual seed launch through the parent with shell=False and --manifest/--fixture-root. Assert the complete /usr/bin/env -i … /bin/bash --noprofile --norc -p prefix, verified absolute uv/Python operands and the recorded argv:
291:Also seed a fixture private cache explicitly through the same parent and isolated seed argv with real bound uv/Python, then prove the generator child's exact offline --with pyyaml argv, shared cache and successful yaml import. An isolated base-Python-only child must not satisfy this assertion. Sandbox or network denial is reported as blocked, without an outside-sandbox retry.
307:Test allowance is real execution/rendering and fixture preparation 260 + migration 100 + validator identities/refusals 220 + pin/shape checks 70 + environment/node cases 90 + pre-exec symlink case 40 + hostile quoting case 20 + yaml-child/cache case 20 + exec-form hook case 10 + online-seed prefix/argv case 30 + manifest-boundary cases 80 + separate pinned-installation case 40 = 980 changed lines.
313:Run make unit-test, make format, make validate-agent-assets and make render-check, the eight named regressions, and unchanged tests.unit.test_claude_settings_merge, tests.unit.test_generate_agent_configs, tests.unit.test_statusline_tools and tests.unit.test_herdr_agents. Do not run Bats locally.
343:> Every `gh` command and every `git` write is an individual command **inside the sandbox**, including pushes and authenticated fetches. No compound write commands, outside-sandbox retries, excluded-command workaround, permission escalation or alternate tool to bypass a denial. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-ci-efficiency-followup-a04 status=blocked` naming the exact command, failure and crossed boundary; preserve the evidence and wait.
363:after: []
365:  - {"control":"home/dot_mise/config.toml","disposition":"residual: Pin only uv, Python and node to the primary task's probed versions; this intentionally stops their latest-version tracking."}
366:  - {"control":"tests/unit/test_generate_agent_configs.py","disposition":"residual: Keep an exact source-manifest/rendered-command equality check and executable leaf/argument checks, plus explicit pin assertions; do not delete legacy fixture coverage."}
367:  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**","disposition":"residual: Only task copy and review/validation/report data are authorized; no helper or runtime code is placed here."}
368:  - {"control":"task copy .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/task.md","disposition":"residual: The orchestrator compares the full dispatched bytes and SHA-256 before accepting this prerequisite."}
369:  - {"control":"task metadata","disposition":"residual: This is an independent three-entry prerequisite task; it grants no write permission for the later binding implementation."}
370:  - {"control":"metadata separators","disposition":"residual: Parse as data with duplicate keys refused and compare the complete dispatched task copy."}
371:  - {"control":"in-process effects","disposition":"residual: Tests and fixture renders use temporary directories; no mise install, update, apply or live hook execution is authorized."}
372:  - {"control":"workflow and interpreter or environment inputs","disposition":"residual: The exact declaration is changed intentionally; trusted-entrypoint implementation remains in the primary task."}
373:  - {"control":"new or renamed scripts","disposition":"residual: None is authorized; retain existing generator and test helpers."}
374:  - {"control":"orchestrator effect merge","disposition":"residual: The orchestrator alone integrates after full final-head evidence and Playbook step 10."}
375:  - {"control":"orchestrator effect update-branch","disposition":"residual: A moved head requires refreshed checks and integration evidence under the orchestrator's control."}
376:  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; the worker cannot remove seats or discard another worktree."}
377:  - {"control":"design 5.14 item 0 same-UID model","disposition":"residual: Exact pins do not separate OS identities or shared GitHub credentials."}
378:  - {"control":"design 5.14 item 1 protected inputs","disposition":"residual: The exact declaration becomes a trusted input; worker write protection remains pending until P1-15 is accepted and deployed."}
379:  - {"control":"design 5.14 item 2 clean environment","disposition":"residual: No new production execution path is introduced; inherited check launch trust is not established by a pin."}
380:  - {"control":"design 5.14 item 3 paths","disposition":"residual: The declaration path is fixed and unchanged; installation path validation belongs to the resolver and primary task."}
381:  - {"control":"design 5.14 item 4 verified bytes","disposition":"residual: Whole-task and final-head evidence are compared; local files remain replaceable by unrestricted same-UID processes."}
382:  - {"control":"design 5.14 item 5 identity","disposition":"residual: Use full head/base and task-copy SHA-256 in evidence; no new lock or reservation is created."}
383:  - {"control":"design 5.14 item 6 honest residuals","disposition":"residual: Pin assertions prove declarations only, not installed binary identity or successful hook execution."}
384:  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the pin regression red then green and retain generator/merge consumers; general hostile-execution closure is not claimed."}
385:  - {"control":"design 5.14 item 8 approval","disposition":"residual: Pins and local evidence are proposals until integration; neither grants permission or merge authority."}
386:  - {"control":"design 5.14 item 9 isolation","disposition":"residual: This task supplies exact version input only; the accepted resolver and primary task implement isolated execution and private caches."}
387:  - {"control":"design 5.14 item 10 sandbox","disposition":"residual: All commands stay in the sandbox; denied commands produce blocked evidence without escalation."}
389:  - {"command":"grep -nE '^(uv|python|node) = ' home/dot_mise/config.toml | paste -sd '|' -","output":"3:node = \"latest\"|5:python = \"latest\"|17:uv = \"latest\""}
390:  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | paste -sd '|' -","output":"home/dot_mise/config.toml|tests/unit/test_generate_agent_configs.py"}
391:  - {"command":"wc -l .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | xargs","output":"63 .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json 95 .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py 1781 tests/unit/test_validate_agent_assets.py 79 home/dot_mise/config.toml 2350 tests/unit/test_generate_agent_configs.py 4368 total"}
392:  - {"command":"grep -nE '^    def test_managed_hooks_use_installed_permgate_paths' tests/unit/test_generate_agent_configs.py | paste -sd '|' -","output":"1417:    def test_managed_hooks_use_installed_permgate_paths(self) -> None:"}
393:  - {"command":"sed -n '1417,1422p' tests/unit/test_generate_agent_configs.py | wc -l | xargs","output":"6"}
404:In GenerateAgentConfigsTest add test_trusted_entrypoint_mise_versions_are_exact, red before the config change and green afterward. Refactor test_managed_hooks_use_installed_permgate_paths to compare the complete rendered PermissionRequest command with the real manifest declaration rendered through the existing template helper; retain exactly one managed entry, permgate executable-leaf/claude-argument checks and the Codex assertion. Keep synthetic legacy-command fixtures. The primary task adds strict bound-sequence and parent-selected-manifest validation.

web search: 
web search: https://code.claude.com/docs/en/settings
**Analyzing command sandboxing and exclusions**
**Examining Python version and test environment issues**
web search: 
web search: 'excludedCommands'
exec
/bin/zsh -lc "sed -n '30,55p' .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md" in ~/Workspace/dotfiles
 succeeded in 18ms:
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

**Analyzing environment and CLI binding issues**
**Reviewing executable binding and launcher configurations**
exec
/bin/zsh -lc "rg -n 'CLI_BIN|command -v|claude_bin|CLAUDE_BIN|claude_args|claude_binary|spawn.sh|realpath|git -C|GIT_' .claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents ~/.agents/skills/agmsg/scripts/spawn.sh" in ~/Workspace/dotfiles
 succeeded in 35ms:
~/.agents/skills/agmsg/scripts/spawn.sh:4:# spawn.sh — launch a NEW agent process and have it take an actas identity.
~/.agents/skills/agmsg/scripts/spawn.sh:6:# Given an agent-type and an actas <name>, spawn.sh:
~/.agents/skills/agmsg/scripts/spawn.sh:16:#   spawn.sh <agent-type> <name> [options]
~/.agents/skills/agmsg/scripts/spawn.sh:17:#   spawn.sh <agent-type> <name> --boot-prompt "<initial task>" [options]
~/.agents/skills/agmsg/scripts/spawn.sh:110:[ -n "$AGENT_TYPE" ] || die "Usage: spawn.sh <agent-type> <name> [options]"
~/.agents/skills/agmsg/scripts/spawn.sh:111:[ -n "$NAME" ] || die "Usage: spawn.sh <agent-type> <name> [options]"
~/.agents/skills/agmsg/scripts/spawn.sh:238:CLI_BIN="$(agmsg_type_get "$AGENT_TYPE" cli)"
~/.agents/skills/agmsg/scripts/spawn.sh:239:CLI_BIN_EXE="${CLI_BIN%% *}"
~/.agents/skills/agmsg/scripts/spawn.sh:241:if [ -n "$CLI_BIN" ]; then
~/.agents/skills/agmsg/scripts/spawn.sh:242:  command -v "$CLI_BIN_EXE" >/dev/null 2>&1 \
~/.agents/skills/agmsg/scripts/spawn.sh:243:    || die "'$CLI_BIN_EXE' not found on PATH — install the ${AGENT_TYPE} CLI first"
~/.agents/skills/agmsg/scripts/spawn.sh:244:  CLI_PATH="$(command -v "$CLI_BIN_EXE")"
~/.agents/skills/agmsg/scripts/spawn.sh:255:# where `command -v codex` resolves the REAL binary and the spawned seat starts
~/.agents/skills/agmsg/scripts/spawn.sh:272:    || die "agent type '$AGENT_TYPE' declares a launch wrapper that is missing or not executable: $SPAWN_WRAPPER — refusing to launch the bare '$CLI_BIN_EXE' in its place (bypassing the wrapper is exactly what it exists to prevent)"
~/.agents/skills/agmsg/scripts/spawn.sh:333:  NODE_BIN="${AGMSG_NODE_BIN:-$(command -v node 2>/dev/null || true)}"
~/.agents/skills/agmsg/scripts/spawn.sh:583:      case "$CLI_BIN" in *' '*) printf ' %s' "${CLI_BIN#* }" ;; esac
~/.agents/skills/agmsg/scripts/spawn.sh:585:      printf '%s%s' "$MSYS_GUARD" "$CLI_BIN"
~/.agents/skills/agmsg/scripts/spawn.sh:729:  command -v tmux >/dev/null 2>&1 \
~/.agents/skills/agmsg/scripts/spawn.sh:771:    && command -v herdr >/dev/null 2>&1
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:56:# @option --add-worker [<worktree>] Seat a worker for DIR/<worktree> via agmsg spawn.sh; the
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:62:# @option --ready-timeout <seconds> Add-worker: spawn.sh readiness wait bound (spawn.sh default 90).
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:162:spawn.sh, with the profile's launch args. HERDR_AGENTS_WORKER_KIND (default
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:171:socket ~/.config/herdr/herdr.sock (the path the Claude sandbox allowlists), a claude worker's workspace-trust dialog is accepted while spawn.sh
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:172:waits, and --ready-timeout bounds that wait (spawn.sh default 90 seconds);
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:288:        listed="$(git -C "${workdir}" worktree list --porcelain 2> /dev/null | sed -n 's/^worktree //p')"
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:293:    elif ! git -C "${workdir}" worktree add --detach "${path}" origin/main > /dev/null 2>&1; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:309:#   unless $4 is `--no-join` (spawn.sh joins it itself).
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:462:    common="$(git -C "${worktree}" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)" || return 0
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:463:    git_dir="$(git -C "${worktree}" rev-parse --path-format=absolute --git-dir 2> /dev/null)" || return 0
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:491:    if [[ "$(git -C "${worktree}" rev-parse --is-shallow-repository 2> /dev/null)" == true ]]; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:497:#   profile's launch arguments (spawn.sh splices the type section into the boot
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:547:#   despawn.sh: a graceful `ok` (which includes a member with no placement
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:557:    local despawn="${HOME}/.agents/skills/agmsg/scripts/despawn.sh"
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:577:        ! git -C "$1" worktree list --porcelain 2> /dev/null | sed -n 's/^worktree //p' | grep -Fxq -- "${path}"; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:589:    git_dir="$(git -C "$1" rev-parse --path-format=absolute --git-dir 2> /dev/null)" &&
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:590:        common_dir="$(git -C "$1" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)" &&
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:600:    common_dir="$(git -C "${dir}" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)" || return 1
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:952:    local -a claude_args=() extra_claude_args=()
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:973:        read -r -a claude_args <<< "${profile_args}"
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:976:        read -r -a extra_claude_args <<< "${HERDR_AGENTS_CLAUDE_ARGS}"
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:977:        claude_args+=(${extra_claude_args[@]+"${extra_claude_args[@]}"})
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:984:    start_agent_in_pane claude "${agent_name}" "${pane_id}" "${newly_created}" ${claude_args[@]+"${claude_args[@]}"} > /dev/null
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:985:    printf 'orchestrator_profile=%s args=%s\n' "${profile:-none}" "${claude_args[*]:-none}"
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1053:    done < <(git -C "$1" worktree list --porcelain 2> /dev/null | sed -n 's/^worktree //p')
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1136:    if ! command -v agmsg-dispatch > /dev/null 2>&1; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1192:#   spawn.sh seats it. spawn.sh places the pane before its readiness wait, and a
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1194:#   times out, so watch the workspace's new pane for as long as spawn.sh runs.
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1196:# @arg $2 json Pane ids (a JSON array) in that workspace before spawn.sh started.
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1197:# @arg $3 pid spawn.sh process id.
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1217:    # waits for spawn.sh and reports its exit code.
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1240:    if [[ -n ${seat_dir} && -x ${scripts}/identities.sh && -x ${scripts}/team.sh ]] && command -v jq > /dev/null 2>&1; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1284:    if common="$(git -C "$1" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)" &&
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1443:    common_dir="$(git -C "${workdir}" rev-parse --path-format=absolute --git-common-dir 2> /dev/null)" || return 0
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1444:    hook="$(git -C "${workdir}" rev-parse --path-format=absolute --git-path hooks 2> /dev/null)/pre-push" || return 0
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1448:    if [[ "$(git -C "${workdir}" hash-object --no-filters -- "${hook}")" == "${stub_blob}" ]]; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1605:#   workspace. despawn.sh usually closes the worker's pane, and with it the
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1637:    if ! command -v "${command_name}" > /dev/null 2>&1; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1852:        # A pane-less caller has no HERDR_SOCKET_PATH, and spawn.sh's herdr
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1889:    if [[ ! -x ${scripts}/spawn.sh ]]; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1890:        printf 'herdr-agents: agmsg spawn.sh not found (%s); install agmsg 1.5.0 with make update.\n' "${scripts}/spawn.sh" >&2
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1897:    # Bash retains this inherited flock until spawn.sh registers the identity.
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1898:    seat_git_common_dir="$(git -C "${workdir}" rev-parse --path-format=absolute --git-common-dir)"
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1913:        done < <(git -C "${workdir}" worktree list --porcelain | sed -n 's/^worktree //p')
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1933:        # spawn.sh labels the worker's tab and pane <team>:<name>.
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1954:    # spawn.sh seats the member (placement record, actas boot, readiness wait);
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1976:            "${scripts}/spawn.sh" "$(worker_agmsg_type "${seat_kind}")" "${seat_name}" \
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:1987:        printf 'herdr-agents: spawn.sh exited %s for worker %s in workspace %s; confirm linkage with AGMSG-PING before dispatching.\n' "${spawn_rc}" "${seat_name}" "${seat_workspace_id}" >&2
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2018:    if [[ ${seat_force} != true && -n "$(git -C "${seat_dir}" status --porcelain 2> /dev/null)" ]]; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2127:        if ! audit_base="$(git -C "${workdir}" merge-base origin/main "${audit_commit}" 2> /dev/null)"; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2215:    if git -C "${workdir}" ls-files --error-unmatch -- "${audit_validator_rel}" > /dev/null 2>&1 ||
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2216:        git -C "${workdir}" cat-file -e "HEAD:${audit_validator_rel}" 2> /dev/null ||
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2218:        audit_head="$(git -C "${workdir}" rev-parse HEAD 2> /dev/null || true)"
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2219:        audit_full="$(git -C "${workdir}" rev-parse --verify --quiet "${audit_commit}^{commit}" 2> /dev/null || true)"
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2222:            ! git -C "${workdir}" ls-files --error-unmatch -- "${audit_validator_rel}" > /dev/null 2>&1 ||
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2223:            ! git -C "${workdir}" diff --quiet HEAD -- "${audit_validator_rel}" 2> /dev/null; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2226:        elif ! command -v python3 > /dev/null 2>&1; then
.claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents:2372:if command -v zed > /dev/null 2>&1; then

exec
/bin/zsh -lc "rg -n 'worker.*launch|launcher|python|herdr_binary|claude|trusted_paths|mise' .claude/worktrees/worker-e/home/dot_agents/agent-config.yaml | head -n 75; sed -n '1,90p' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md" in ~/Workspace/dotfiles
 succeeded in 0ms:
20:  - claude
27:# ~/.agents/model-profiles.env for launchers. Keep main-session models fixed
31:    claude: { model: haiku, effort: low }
34:    claude: { model: claude-opus-5-5, effort: xhigh, advisor: fable }
42:    claude: { model: claude-fable-5-1, effort: xhigh }
45:    claude: { model: claude-fable-5-1, effort: xhigh, advisor: fable }
52:    claude: { model: claude-fable-5, effort: high }
61:    claude: { model: claude-fable-5-1, effort: high }
68:# Worker pane agent for herdr-agents: codex or claude. Renders into
71:worker_kind: claude
72:# Orchestrator pane agent for the herdr-agents pair: claude or codex; codex
76:orchestrator_kind: claude
85:worker_worktree: .claude/worktrees/worker-c
124:      PATH: '{{ .chezmoi.homeDir }}/.local/share/mise/installs/node/lts/bin:{{ .chezmoi.homeDir }}/.local/share/mise/shims:{{ .chezmoi.homeDir }}/.local/bin:{{ .chezmoi.homeDir }}/.local/bin/common:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
176:      ponytail@ponytail:hooks/claude-codex-hooks.json:session_start:0:0:
179:      ponytail@ponytail:hooks/claude-codex-hooks.json:user_prompt_submit:0:0:
182:      ponytail@ponytail:hooks/claude-codex-hooks.json:subagent_start:0:0:
189:claude:
218:    - superpowers@claude-plugins-official
222:  settings_path: home/.chezmoitemplates/claude-settings-managed.json
223:  worker_settings_path: home/.chezmoitemplates/claude-worker-settings.json
224:  managed_settings_path: home/.chezmoitemplates/claude-managed-settings.json
225:  worker_config_dir: "{{ .chezmoi.homeDir }}/.claude-worker"
227:  trusted_paths: [
229:    "{checkout}/.claude/contextdb", "{checkout}/.claude/contextdb/**",
230:    "{checkout}/.claude/hooks", "{checkout}/.claude/hooks/**",
231:    "{checkout}/.claude/settings.json", "{checkout}/.claude/settings.local.json",
246:    "{checkout}/mise.toml", "{checkout}/mkdocs.yml", "{checkout}/renovate.json", "{checkout}/ruff.toml",
248:    "{checkout}/.claude/worktrees/*/.claude", "{checkout}/.claude/worktrees/*/.claude/**",
249:    "{checkout}/.claude/worktrees/*/.mcp.json", "~/.agents/agent-config.yaml", "~/.agents/model-profiles.env",
254:    "~/.agents/permgate-policy.yaml", "~/.claude/hooks/orchestrator-only.sh",
255:    "~/.local/lib/python*/site-packages", "~/.local/lib/python*/site-packages/**",
256:    "~/Library/Python/*/lib/python/site-packages", "~/Library/Python/*/lib/python/site-packages/**",
257:    "~/.claude", "~/.claude/**",
258:    "~/.claude-worker", "~/.claude-worker/**",
262:    "~/.local/share/mise", "~/.local/share/mise/**",
267:  mcp_config_path: home/dot_claude/private_mcp.json.tmpl
268:  schema: https://json.schemastore.org/claude-code-settings.json
274:  plansDirectory: ./.agents/worklog/claude
285:    # independently." (code.claude.com/docs/en/permissions)
347:  # writable-roots list; ~/.claude is sandbox-protected, so it is not listed.
374:        - ~/.local/state/mise
377:        - ~/Library/Caches/mise
386:        - files.pythonhosted.org
400:    enforce_uv_hook: ~/.claude/hooks/enforce-uv.sh
401:    format_edited_files_hook: ~/.claude/hooks/format-edited-files.py
402:    project_map_reload_hook: ~/.claude/hooks/project-map-reload.sh
404:      command: ~/.local/bin/common/permgate claude
411:            command: "bash '{{ .chezmoi.homeDir }}/.claude/hooks/herdr-agent-state.sh' session"
460:# minimum_release_age in home/dot_mise/config.toml). Only a component whose
467:  mise:
469:    upstream: jdx/mise
474:    note: the newest cooled-down release installs only when gpg and gpgv (SHASUMS256.asc checked against the release key with gpg_fingerprint, fetched from keys.openpgp.org as mise documents) or an authenticated gh (the release attestation) can verify it before it runs; otherwise the fallback release does, and mise self-update moves it forward afterwards.
482:      reason: a host without gpg and without an authenticated gh (a fresh macOS) can check neither the release key's signature nor the release attestation before mise runs, and SHASUMS256.txt comes from the same release; so it bootstraps this reviewed release, SHASUMS256.txt kept as a second check.
483:    install_path: ~/.local/bin/mise
484:    installer: install/common/mise.sh
486:      file: install/common/mise.sh
549:    note: chezmoi signs its checksums with cosign only, which a fresh host cannot run; the newest cooled-down release installs only when an authenticated gh can check its release attestation before it runs, otherwise the fallback release does, and mise's own chezmoi takes over after the bootstrap.
618:      darwin-arm64: https://files.pythonhosted.org/packages/f5/ed/5e951b0e6fcadef1a2598e82b969b3eaa387a3e202f8987102d0e84cddfc/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl
619:      darwin-amd64: https://files.pythonhosted.org/packages/ba/c3/04dd3c68d87620fa347372b5e9450c3bb3518aa096abdf08169e6d2ce37f/hcom-0.7.30-py3-none-macosx_10_12_x86_64.whl
620:      linux-amd64: https://files.pythonhosted.org/packages/21/fb/0a48f19a1c39b4ff59412f1fe34130c14acbc55da69097018d729191c6d2/hcom-0.7.30-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
621:      linux-arm64: https://files.pythonhosted.org/packages/f0/23/e746ce90643a1286ed3c6410c66eaae7134fbd2267d002814e6a932a2b60/hcom-0.7.30-py3-none-manylinux_2_28_aarch64.whl
712:  claude-plugins:
713:    source: claude-plugin
719:      superpowers: {marketplace: anthropics/claude-plugins-official, pin: 6.4.1}
---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-binding-a01
kind: code
security: true
allowed_files: ["home/dot_agents/agent-config.yaml","home/.chezmoitemplates/claude-settings-managed.json","home/dot_claude*/modify_private_settings.json","scripts/generate-agent-configs.py","scripts/validate-agent-assets.py","Makefile","tests/unit/test_claude_managed_settings.py","tests/unit/test_validate_agent_assets.py","scripts/orchestrator/trusted-launch.sh",".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**"]
after: [dotfiles-T133-worker-write-boundary-a02, dotfiles-T133-ci-efficiency-followup-a04]
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

**Checking function start behavior**
exec
/bin/zsh -lc "sed -n '760,860p' .claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents; sed -n '1945,1985p' .claude/worktrees/worker-e/home/dot_local/bin/common/executable_herdr-agents; sed -n '238,265p' ~/.agents/skills/agmsg/scripts/spawn.sh; sed -n '508,593p' ~/.agents/skills/agmsg/scripts/spawn.sh" in ~/Workspace/dotfiles
 succeeded in 53ms:
    local output

    output="$(claim_orchestrator_seat "$1" "$2" --self)"
    [[ -n ${output} ]] || return 0
    printf '%s\n' "${output}"
    [[ ${output} != seat_claim=skipped* ]] || return 0
    print_stale_seats "$1"
    print_regime_directive "$1"
}

# @description Derive and validate a herdr 0.8.2 agent registration name.
# @arg $1 string Agent role prefix.
# @arg $2 string Herdr workspace id.
function agent_name_for_workspace() {
    local name

    name="$(printf '%s-%s' "$1" "$2" | tr '[:upper:]' '[:lower:]')"
    if [[ ! ${name} =~ ^[a-z][a-z0-9_-]{0,31}$ ]]; then
        printf 'Invalid Herdr agent name: %s\n' "${name}" >&2
        return 1
    fi
    printf '%s\n' "${name}"
}

# @description Succeed when the pane's last non-blank output line ends in a prompt.
#   It reads recent-unwrapped: a background tab's visible snapshot can be stale.
# @arg $1 pane_id Herdr pane id to inspect.
function pane_shows_shell_prompt() {
    herdr pane read "$1" --source recent-unwrapped --lines 50 2> /dev/null |
        sed '/^[[:space:]]*$/d' | tail -n 1 | grep -qE '[$#%❯➜>]+[[:space:]]*$'
}

# @description Wait (bounded) until the pane's shell is idle.
#   The foreground process decides: the pane's shell alone means idle. A new
#   pane also needs its prompt drawn, because a split can return before zsh
#   enables its prompt and starting an agent during that window injects
#   bracketed-paste control bytes into the line editor. Without process-info,
#   the prompt text alone decides.
# @arg $1 pane_id Herdr pane id to inspect.
# @arg $2 string Optional `prompt` to also require a drawn prompt.
function wait_for_shell_prompt() {
    local pane_id="$1"
    local require_prompt="${2:-}"
    local process_json

    for _ in {1..50}; do
        if process_json="$(herdr pane process-info --pane "${pane_id}" 2> /dev/null)"; then
            if printf '%s\n' "${process_json}" | jq -e \
                '.result.process_info as $info
                 | $info.foreground_processes as $processes
                 | ($processes | length) == 1
                   and (($info.shell_pid != null and $processes[0].pid == $info.shell_pid)
                     or (($processes[0].argv[0] // $processes[0].name // "") | test("(^|/)-?(ba|z|fi)?sh$")))' > /dev/null &&
                { [[ ${require_prompt} != prompt ]] || pane_shows_shell_prompt "${pane_id}"; }; then
                sleep 0.2
                return 0
            fi
        elif pane_shows_shell_prompt "${pane_id}"; then
            sleep 0.2
            return 0
        fi
        sleep 0.2
    done
    return 1
}

# @description Split a pane and return the id reported by herdr.
# @arg $1 pane_id Existing pane used as the split anchor.
# @arg $2 path Working directory for the new pane.
# @arg $@ option Additional pane split options.
function split_agent_pane() {
    local source_pane_id="$1"
    local workdir="$2"
    local split_json
    local pane_id
    shift 2

    if [[ -n ${FPATH:-} ]]; then
        split_json="$(herdr pane split "${source_pane_id}" --direction right --cwd "${workdir}" --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --env "FPATH=${FPATH}" "$@" --no-focus)"
    else
        split_json="$(herdr pane split "${source_pane_id}" --direction right --cwd "${workdir}" --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 "$@" --no-focus)"
    fi
    pane_id="$(printf '%s\n' "${split_json}" | json_agent_pane_id)"
    if [[ -z ${pane_id} ]]; then
        printf 'Unable to read split pane id from Herdr response: %s\n' "${split_json}" >&2
        return 1
    fi
    printf '%s\n' "${pane_id}"
}

# @description Wait for a newly registered agent to become interactive.
# @arg $1 string Herdr agent registration name.
function wait_for_agent_ready() {
    local agent_name="$1"

    for _ in {1..30}; do
        if herdr agent wait "${agent_name}" --until "idle" --until "working" --until "done" --timeout 1000 > /dev/null 2>&1; then
            return 0
        fi
        sleep 0.2
    done
        if [[ -z ${seat_workspace_id} ]]; then
            printf 'herdr-agents: unable to create Herdr workspace %q for %s.\n' "${seat_label}" "${seat_dir}" >&2
            exit 1
        fi
    fi
    seat_options="$(mktemp)"
    trap 'rm -f "${seat_options}"' EXIT
    write_spawn_options "${seat_kind}" "${seat_dir}" > "${seat_options}"
    seat_panes="$(herdr pane list --workspace "${seat_workspace_id}" | jq -c '[.result.panes[]?.pane_id]')"
    # spawn.sh seats the member (placement record, actas boot, readiness wait);
    # --window opens a tab in HERDR_WORKSPACE_ID (the managed workspace when one
    # exists, the orchestrator tab untouched), and --project opts the join
    # out of project resolution. It runs in the background so a claude worker's
    # trust dialog is accepted during the readiness wait, not after it.
    (
        export UV_CACHE_DIR="${seat_dir}/.uv-cache" UV_PYTHON_INSTALL_DIR="${seat_dir}/.uv-cache/python"
        [[ ${seat_kind} != claude ]] || export CLAUDE_CONFIG_DIR="${HOME}/.claude-worker"
        # @description Bind the new pane environment even in an existing workspace.
        # shellcheck disable=SC2329 # Invoked by the upstream spawn process.
        function herdr() {
            if [[ $1 == tab && $2 == create ]]; then
                local -a bindings=(--env "UV_CACHE_DIR=${UV_CACHE_DIR}" --env "UV_PYTHON_INSTALL_DIR=${UV_PYTHON_INSTALL_DIR}")
                [[ ${seat_kind} != claude ]] || bindings+=(--env "CLAUDE_CONFIG_DIR=${CLAUDE_CONFIG_DIR}")
                "${HOOK_TOOLS}/github-ogulcancelik-herdr/latest/herdr" "$@" "${bindings[@]}"
            else
                "${HOOK_TOOLS}/github-ogulcancelik-herdr/latest/herdr" "$@"
            fi
        }
        export seat_kind HOOK_TOOLS
        export -f herdr
        HERDR_WORKSPACE_ID="${seat_workspace_id}" AGMSG_SPAWN_OPTIONS_FILE="${seat_options}" \
            "${scripts}/spawn.sh" "$(worker_agmsg_type "${seat_kind}")" "${seat_name}" \
            --project "${seat_dir}" --team "${seat_team}" --terminal-driver herdr --window \
            ${seat_ready_timeout:+--ready-timeout "${seat_ready_timeout}"}
    ) &
    spawn_pid=$!
    [[ ${seat_kind} != claude ]] || accept_spawned_claude_trust_dialog "${seat_workspace_id}" "${seat_panes}" "${spawn_pid}"
    spawn_rc=0
    wait "${spawn_pid}" || spawn_rc=$?
    (cd / && python3 -I -c 'import fcntl; fcntl.flock(9, fcntl.LOCK_UN)')
    exec 9>&-
CLI_BIN="$(agmsg_type_get "$AGENT_TYPE" cli)"
CLI_BIN_EXE="${CLI_BIN%% *}"
CLI_PATH=""
if [ -n "$CLI_BIN" ]; then
  command -v "$CLI_BIN_EXE" >/dev/null 2>&1 \
    || die "'$CLI_BIN_EXE' not found on PATH — install the ${AGENT_TYPE} CLI first"
  CLI_PATH="$(command -v "$CLI_BIN_EXE")"
elif [ -z "$SPAWN_LAUNCHER" ]; then
  die "agent type '$AGENT_TYPE' manifest declares neither a 'cli' binary nor a 'spawn' launcher"
fi

# --- Optional launch wrapper (manifest `spawn_wrapper=`) ---
# A type may name a script, relative to its own driver directory, that the boot
# script runs INSTEAD of the bare `cli=` executable. codex needs this (#1063):
# its monitor bridge is entered through codex-shim.sh, which is installed on
# purpose as an interactive-shell FUNCTION (PR #193) — so it is not exported
# and does not exist in the non-interactive shell that runs a boot script,
# where `command -v codex` resolves the REAL binary and the spawned seat starts
# without --remote (measured 2026-09-06: the bridge then restarts every few
# seconds against a thread it cannot own, and no message is ever delivered).
# The function form stays; what spawn needs is a resolution that works from a
# non-interactive shell, so the wrapper is addressed by its bundled path —
# never through PATH or function lookup. A wrapper that is declared but
# missing or not executable is a REFUSAL: launching the bare CLI instead would
# recreate the bypass with no signal, and the symptom is a seat that looks
# spawned and never says a word. The `cli=` check above still applies, because
# the wrapper needs the real binary too.
SPAWN_WRAPPER=""
PLAIN_WITNESS="${BOOT}.plain-witness"
{
  echo '#!/usr/bin/env bash'
  printf 'cd %q || exit 1\n' "$PROJECT"
  # A plain OS-terminal spawn has no parent-side handle. The child window is the
  # first authority that can observe its emulator, controlling tty and owner
  # process. Only the plain launcher creates the request file, so tmux/herdr
  # boots do no extra work. Publish atomically before starting the CLI.
  printf 'if [ -f %q ]; then\n' "$PLAIN_WITNESS_REQUEST"
  echo '  case "${TERM_PROGRAM:-}" in iTerm.app) _agmsg_emulator=iterm ;; Apple_Terminal) _agmsg_emulator=terminal ;; *) _agmsg_emulator=unknown ;; esac'
  echo '  _agmsg_tty="$(tty 2>/dev/null || true)"'
  echo '  _agmsg_start="$(ps -o lstart= -p "$$" 2>/dev/null | sed '\''s/^ *//; s/ *$//'\'' | tr '\'' '\'' '\''_'\'')"'
  printf '  _agmsg_witness_tmp=%q.$$\n' "$PLAIN_WITNESS"
  echo '  { printf '\''%s\t%s\t%s\t%s'\'' "$_agmsg_emulator" "$_agmsg_tty" "$$" "$_agmsg_start"; echo; } > "$_agmsg_witness_tmp"'
  printf '  mv "$_agmsg_witness_tmp" %q\n' "$PLAIN_WITNESS"
  echo 'fi'
  # Mark the launched session as spawn-born (#339): the CLI inherits this, so the
  # actas flow knows the session is already named <team>-<agent> (name_arg) and
  # suppresses the "rename this session" tip meant for hand-started sessions.
  echo 'export AGMSG_SPAWNED=1'
  # Drop inherited same-type session-identity vars before exec'ing the CLI (#294).
  # An entry ending in `*` is a NAMESPACE: every exported variable whose name
  # starts with that prefix is unset, enumerated from `env` at boot time, so a
  # control variable the type's runtime adds later is cleared without anyone
  # remembering to list it (#1063: the codex shim stack keeps all of its runtime
  # controls under AGMSG_CODEX_*, and two review rounds each found one more name
  # a deny-list had missed). Names without `*` are unset literally.
  if [ -n "$SPAWN_UNSET_VARS" ]; then
    _unset_literal=""
    for _v in $SPAWN_UNSET_VARS; do
      case "$_v" in
        *\*)
          # `sed -e … -e …`, not `sed -n`: the emitted line must not contain a
          # bare ` -n `, which is also claude-code's name flag and is asserted
          # absent from a codex boot script.
          _prefix="${_v%\*}"
          printf 'for _v in $(env | sed -e '"'"'/^%s[A-Za-z0-9_]*=/!d'"'"' -e '"'"'s/=.*//'"'"'); do unset "$_v"; done\n' "$_prefix"
          ;;
        *) _unset_literal="$_unset_literal $_v" ;;
      esac
    done
    [ -n "$_unset_literal" ] && printf 'unset%s\n' "$_unset_literal"
  fi
  if [ -n "$SPAWN_AGENT" ]; then
    # Node-launcher path: pass the universal agmsg context + the actas prompt.
    # Type-specific config is the launcher's own default/env, so core stays
    # generic and names no add-on. Spawn-options tokens (if any) land before
    # --initial-input, same relative position as the direct-CLI path below.
    printf '%s%q %q \\\n' "$MSYS_GUARD" "$NODE_BIN" "$SPAWN_AGENT"
    printf '  --name %q \\\n' "$NAME"
    printf '  --team %q \\\n' "$TEAM"
    printf '  --project %q \\\n' "$PROJECT"
    for _tok in ${SPAWN_OPT_TOKENS[@]+"${SPAWN_OPT_TOKENS[@]}"}; do
      printf '  %q \\\n' "$_tok"
    done
    printf '  --initial-input %q\n' "$ACTAS_PROMPT"
  else
    # Direct-CLI launch:
    # `<cli> [<resume_arg> <uuid>] [<model_arg> <model_id>] [spawn-options...] [<name_arg> <name>] [<prompt_arg>] "/<cmd> actas <name>"`.
    # cli is emitted unquoted — it is trusted fixed-prefix manifest data (see
    # above) that may itself be several tokens (e.g. `opencode run --interactive`).
    # The resume head (#339) is emitted RIGHT AFTER the cli, before all other
    # args: mandatory for a subcommand-shaped resume (codex `resume <id>`),
    # harmless for a flag-shaped one (claude `--resume <id>`) -- see
    # agmsg_role_resume_head. model_arg is the manifest flag spelling (bare, not
    # %q-quoted); the model id and every spawn-options token are quoted. The
    # role-identity tail (name/prompt_arg + the actas prompt) is emitted by
    # agmsg_role_cli_args so its flag order matches resurrect-panes.sh.
    # MSYS_GUARD (#336) prefixes the CLI line as a command-local env assignment;
    # emitted with %s (not %q) so it stays an assignment, not a single token.
    # With a manifest spawn_wrapper, the wrapper's bundled path replaces the
    # cli's FIRST word (the executable); any fixed-prefix tokens after it are
    # kept, since the wrapper forwards its argv to the real binary.
    if [ -n "$SPAWN_WRAPPER" ]; then
      printf '%s%q' "$MSYS_GUARD" "$SPAWN_WRAPPER"
      case "$CLI_BIN" in *' '*) printf ' %s' "${CLI_BIN#* }" ;; esac
    else
      printf '%s%s' "$MSYS_GUARD" "$CLI_BIN"
    fi
    agmsg_role_resume_head "$AGENT_TYPE" "$RESUME_UUID"
    [ -n "$MODEL_ID" ] && printf ' %s %q' "$MODEL_ARG" "$MODEL_ID"
    for _tok in ${SPAWN_OPT_TOKENS[@]+"${SPAWN_OPT_TOKENS[@]}"}; do
      printf ' %q' "$_tok"
    done
    # Role-identity tail: name the session and pass the actas prompt. The actas
    # prompt runs in BOTH fresh and resume cases -- resume restores context only,

**Analyzing environment inheritance in spawn roles**
**Reviewing launcher symlink and interpreter validation**
**Finalizing audit summary**
**Assessing nested worktree and permissions**
**Analyzing ownership binding gaps**
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md | sed -n '8,61p'; rg -n 'guard|descendant|formatter|residual' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md | tail -n 18; sed -n '1,150p' .orchestration/acceptance/dotfiles-T133-trusted-entrypoint-binding-a01.md" in ~/Workspace/dotfiles
 succeeded in 110ms:
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
371:  - {"control":"in-process effects","disposition":"residual: Tests and fixture renders use temporary directories; no mise install, update, apply or live hook execution is authorized."}
372:  - {"control":"workflow and interpreter or environment inputs","disposition":"residual: The exact declaration is changed intentionally; trusted-entrypoint implementation remains in the primary task."}
373:  - {"control":"new or renamed scripts","disposition":"residual: None is authorized; retain existing generator and test helpers."}
374:  - {"control":"orchestrator effect merge","disposition":"residual: The orchestrator alone integrates after full final-head evidence and Playbook step 10."}
375:  - {"control":"orchestrator effect update-branch","disposition":"residual: A moved head requires refreshed checks and integration evidence under the orchestrator's control."}
376:  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; the worker cannot remove seats or discard another worktree."}
377:  - {"control":"design 5.14 item 0 same-UID model","disposition":"residual: Exact pins do not separate OS identities or shared GitHub credentials."}
378:  - {"control":"design 5.14 item 1 protected inputs","disposition":"residual: The exact declaration becomes a trusted input; worker write protection remains pending until P1-15 is accepted and deployed."}
379:  - {"control":"design 5.14 item 2 clean environment","disposition":"residual: No new production execution path is introduced; inherited check launch trust is not established by a pin."}
380:  - {"control":"design 5.14 item 3 paths","disposition":"residual: The declaration path is fixed and unchanged; installation path validation belongs to the resolver and primary task."}
381:  - {"control":"design 5.14 item 4 verified bytes","disposition":"residual: Whole-task and final-head evidence are compared; local files remain replaceable by unrestricted same-UID processes."}
382:  - {"control":"design 5.14 item 5 identity","disposition":"residual: Use full head/base and task-copy SHA-256 in evidence; no new lock or reservation is created."}
383:  - {"control":"design 5.14 item 6 honest residuals","disposition":"residual: Pin assertions prove declarations only, not installed binary identity or successful hook execution."}
384:  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the pin regression red then green and retain generator/merge consumers; general hostile-execution closure is not claimed."}
385:  - {"control":"design 5.14 item 8 approval","disposition":"residual: Pins and local evidence are proposals until integration; neither grants permission or merge authority."}
386:  - {"control":"design 5.14 item 9 isolation","disposition":"residual: This task supplies exact version input only; the accepted resolver and primary task implement isolated execution and private caches."}
387:  - {"control":"design 5.14 item 10 sandbox","disposition":"residual: All commands stay in the sandbox; denied commands produce blocked evidence without escalation."}
417:Risk: the primary binding work and same-UID/shared-credential residuals remain.
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
  "task": "dotfiles-T133-trusted-entrypoint-binding-a01"
}
---

# Acceptance record: dotfiles-T133-trusted-entrypoint-binding-a01

The executable-binding family split out of plan 024 P1-15 by D-024-26: exact probed declarations for uv, Python and node, the bound PermissionRequest hook through the rendered absolute uv and isolated Python, the deploy-time effective-settings check, the formatter PATH; after: P1-15 and ci-efficiency-followup-a04 (the trusted interpreter resolver). Text designed by the review-profile context with probed premises (`.agents/worklog/orchestrator-glue/redesign/binding-a01.md`, prompt `binding-a01-design-prompt.md`); security: true; a Codex seat (D-024-25).

- 2026-10-19T12:02Z: design installed (`binding-a01.md`, 247 lines; premises probed; after: P1-15 and ci-efficiency-followup-a04); checker OK; C-80 first review started.
- 2026-10-19T12:06:42Z: C-80 first review (newest `…-text-security-*.md`): `Verdict: incorrect`: P1 uv's identity and containment are checked inside the checker uv launches (the parent must verify the uv binary before any exec); P2 shlex token equality loses quoting (compare the raw command against the rendered canonical form); P2 the generator probe under the base Python has no PyYAML (run it through the bound uv with the seeded private cache). Round 2 by the review-profile context (prompt `binding-a01r2-redesign-prompt.md`).
text-security:binding-r1:1	executable-binding
text-security:binding-r1:2	quoting-preservation
text-security:binding-r1:3	dependency-environment
- 2026-10-19T12:17Z: round-2 text (`binding-a01r2.md`) installed: the parent verifies the uv binary before any exec, quote-preserving command comparison, the generator probe through the bound uv with the seeded cache; checker OK; C-80 round 2 started.
- 2026-10-19T12:35:39Z: C-80 second review (newest `…-text-security-*.md`): `Verdict: incorrect`: P1 the shell-form hook starts an outer shell before `env -i`, so inherited loader inputs run before the privileged parent validates anything (the hook form itself must be the trusted parent: exec form, or the managed hook command is the launcher program with no outer shell); P1 the mandatory online cache seed bypasses the bound parent (no env clearing, no `--isolated`, no verified `--python`, no `-I`). Round 3 to be written with both; the task is after P1-15 and the resolver, so it is not on the critical path.
text-security:binding-r2:1	executable-binding
text-security:binding-r2:2	executable-binding
- 2026-10-19T19:57Z: host pause 13:03Z to 19:55Z (the sandboxed send queued at 13:02 executed at 19:55); the binding text's third review (12:59Z, `…-text-security-*.md`): `Verdict: incorrect` on one P2: the positive fixture admits `sys.executable` and fallback uv installations that the pinned launcher rejects, so CI with setup-uv and no pinned mise Python cannot pass while skipping is forbidden. Three reviews consumed: C-92 re-plan.
re-plan: fixture-vs-binding (rows text-security:binding-r1:1, text-security:binding-r2:1, text-security:binding-r2:2, text-security:binding-r3:1) — specification: the text demanded one hook execution test that is both pinned-binding-faithful and runnable on runners without the pinned installation; design: the launcher trusts the manifest its parent names (a `--manifest <path>` argument under the trusted prefix), so a test passes a fixture manifest bound to the runner's real uv and python and the launcher applies every check (shape, regular file, no shims, no worker-writable roots) to those paths — not a bypass, the same code path with a different trusted input; the production manifest is the rendered one; implementation: the round-4 text states the manifest argument, the fixture manifest test on runners, and the pinned-installation test on the host only (named skip elsewhere, recorded); verification: both tests plus the launcher refusing a manifest outside the repository or the test fixture root.
text-security:binding-r3:1	fixture-vs-binding
- 2026-10-19T20:10Z: re-planned text (`binding-a01r4.md`, 417 lines: the launcher trusts the manifest its parent names with `--manifest`/`--fixture-root`, fixture manifests on runners, the pinned case on the host) installed; checker OK; C-80 (first after the re-plan) started.
- 2026-10-19T20:13:07Z: C-80 (first after the re-plan; the manifest-trusting launcher): `Verdict: correct`. The text waits for its prerequisites (P1-15 and ci-efficiency-followup-a04); a Codex seat takes it then (D-024-25).
- 2026-10-19T21:33:05Z: `after:` retargeted from the withdrawn dotfiles-T133-worker-write-boundary-a01 (PR #431 reset) to its reset successor dotfiles-T133-worker-write-boundary-a02; one line, same length, body unchanged (sha256 1cc2a02b0876… -> 2ed7e01d8239…; the C-80 verdict on the body stands); checker OK. Found by the project-map pass at 06:30 JST.

**Analyzing ownership and execution gaps**
**Summarizing interpreter closure and documentation approach**

I’m focusing on reporting a key limitation involving interpreter closure and binary binding without relying on external sources, prioritizing verified local documentation and internal findings to keep the scope clear and concise.
codex
引き継ぎ先に一つ不一致があります。a04 は guard・delivery・formatter/map の完全な実行束縛を `trusted-entrypoint-binding-a01` に割り当てていますが、そのタスクは同じ範囲を明示的に対象外としています。既知の同一 UID リスクを再指摘するものではなく、待機先の完了では解消しない実行経路が残るという指摘です。
exec
/bin/zsh -lc "sed -n '55,82p' .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md; cat .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-49161bc.md.last.md; sed -n '306,329p' .orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md" in ~/Workspace/dotfiles
 succeeded in 35ms:
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

[P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md:374](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md:374) — `CLAUDE_ENV_FILE` selects shell code executed before each Bash command, but the design binds only its pathname and omits its contents from S01–S23, threat coverage and refusal tests; pre-existing contents can execute commands or restore rejected environment variables. Require empty or explicitly trusted generated contents before forwarding, with a planted-content regression. This admission-time omission is separate from deferred replacement races. [Documented behavior](https://code.claude.com/docs/en/env-vars).

Checked all 85 threat rows, including five closed claims; all 22 allowed-file entries have rows. No additional findings beyond the disclosed residuals. Independent review corroborated the finding.

📝 まとめ: Completed the read-only design and cited-context review; disposition remains with the orchestrator.

Not checked: implementation, CI or live enforcement. No files changed; this finding does not establish a sandbox escape.
Verdict: incorrect[P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md:431](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md:431) — All Claude workers share `.claude-worker/.claude.json`, but S11 accepts only the anchor and current worktree’s project keys: after worker A generates valid state, starting worker B rejects A’s key before regeneration—even sequentially; distinguish validated sibling-worktree state from foreign roots and add an A→B startup fixture, since the named same-worktree restart test misses this regression.

Checked all **87 threat rows**, including **8 closed claims**, and all **22 allowed-file entries**, alongside the cited acceptance records and reviews. No additional actionable finding beyond the explicitly deferred execution-binding risks. The executable-content check addresses the documented behavior of [`CLAUDE_ENV_FILE`](https://code.claude.com/docs/en/env-vars).

Reviewed SHA256: `efa211d1fa4e8fc90512fc88acf6e8cad1127d10a74defafe5adab2e2817faf5`.

📝 まとめ: Completed the read-only design review; one P2 finding is submitted for orchestrator disposition.

Not checked: implementation, CI or live enforcement. No files changed; complete executable binding and same-UID isolation remain unestablished.
Verdict: incorrect[P1] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md:425](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md:425) — The design screens `<managed-root>/skills` and explicitly excludes `<managed-root>/.claude/skills`, but the exact pinned Claude 2.1.300 loader consumes the latter; enterprise skill content therefore escapes preflight, while fixture502 tests the wrong directory. Correct the inventory and fixture to match actual consumption. [Official loading locations](https://code.claude.com/docs/en/skills#where-skills-live).

Static inspection confirmed the loader’s SHA256 matches the task’s recorded `475517ca…2d3`; it constructs `join(UA(), ".claude", "skills")`, with `UA()` returning the platform managed directory. Independent review corroborated this finding.

Checked all 87 threat rows, eight closed claims and 22 allowed-file entries, plus cited acceptance records and reviews. No additional findings beyond explicitly deferred risks.

Reviewed task SHA256: `be969e32246c9a1a55e61654d28be9111328fde0e7730a300465bb2e43b0c47e`.

📝 まとめ: Completed the read-only design review; one P1 finding is submitted for orchestrator disposition.

Not checked: implementation, CI or live enforcement. No files changed; complete executable binding and same-UID isolation remain unestablished.
Verdict: incorrectNo new actionable findings in the [task text](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md).

Checked all **87 threat rows**, including **8 closed claims**, and all **22 allowed-file entries**, alongside the cited acceptance records and reviews. The proposed fixtures support their narrowly scoped startup claims. Independent review reached the same conclusion.

The design requires canonical symlink/case identities, sanitized Git inspection and clean child environments. Linux `gh` failure requires blocking rather than sandbox escape. Complete executable binding, same-user replacement races and ledger consumption remain explicitly deferred. The corrected enterprise skills root matches the [official documentation](https://code.claude.com/docs/en/skills#choose-where-skills-load).

Reviewed SHA256: `49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b`.

📝 まとめ: Completed the read-only design review; acceptance remains with the orchestrator.

Not checked: implementation, CI or live enforcement. No files changed; deferred execution-binding risks remain.
Verdict: correct
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

**Preparing counting commands**
exec
/bin/zsh -lc "shasum -a 256 .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md; awk '/"'^threat_table:/{t=1;next}/''^premises:/{t=0} t && /''^  - control:/{n++} t && /disposition: "closed:/{c++} END {print "threat_rows=" n, "closed_rows=" c}'"' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md" in ~/Workspace/dotfiles
 succeeded in 46ms:
d562c68bb40e2dcbf7a18e9958dfe4d5f6c82f04c42ef1bb4946f90d0ba32d99  .orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md
threat_rows=90 closed_rows=11

codex
[P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md:584](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md:584) — Complete guard, delivery and formatter/map execution binding is assigned to `trusted-entrypoint-binding-a01`, but that owner explicitly excludes it at [line 19](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md:19); completing the named dependency therefore cannot close these decision-not-bound-to-execution paths—identify an actual owner and bind dependent deployment to its completion.

Checked all 90 threat rows, 11 closed claims and 22 allowed-file entries, plus cited acceptance/review context. No additional findings beyond explicitly retained residuals.

📝 まとめ: Completed the read-only design review; one P2 finding is submitted for orchestrator disposition.

Not checked: implementation, CI or live enforcement. No files changed; deferred execution-binding risks remain.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
132,084
[P2] High confidence [.orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md:584](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-worker-write-boundary-a04.md:584) — Complete guard, delivery and formatter/map execution binding is assigned to `trusted-entrypoint-binding-a01`, but that owner explicitly excludes it at [line 19](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-trusted-entrypoint-binding-a01.md:19); completing the named dependency therefore cannot close these decision-not-bound-to-execution paths—identify an actual owner and bind dependent deployment to its completion.

Checked all 90 threat rows, 11 closed claims and 22 allowed-file entries, plus cited acceptance/review context. No additional findings beyond explicitly retained residuals.

📝 まとめ: Completed the read-only design review; one P2 finding is submitted for orchestrator disposition.

Not checked: implementation, CI or live enforcement. No files changed; deferred execution-binding risks remain.
Verdict: incorrect
