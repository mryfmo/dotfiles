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
session id: 01a15391-2296-71f1-a2c8-3f8276496b0c
--------
user
Pre-dispatch security review (read-only, security profile) of the task text .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md and its threat_table, before any implementation exists. Judge the design the text states: can the controls it names bind what actually executes on this host (mise shims first on PATH, same-user worker processes, gh outside the sandbox on Linux, symlinks and case-insensitive filesystems, inherited GIT_* environment)? Check every threat row: a closed row whose named test cannot close it, a residual row whose control does not mitigate the risk, a missing row for a file or non-path control, and any gap of the class decision-not-bound-to-execution (a decision made on text or on a validated copy while the execution resolves binaries, files or ledgers from an attacker-influenced place). Read the related acceptance records and reviews the text cites for context. Report each finding as [P0-P3] <confidence> <file:line> <one line>; findings are input for the orchestrator, who decides. End with exactly one line: Verdict: correct or Verdict: incorrect.
warning: loading hooks from both ~/.codex/hooks.json and ~/.codex/config.toml; prefer a single representation for this layer
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
🤖 I read the AGENTS.md for mryfmo/dotfiles.
タスク本文と参照先の acceptance・review 記録を読み、各 control がこのホストで実際に実行される対象を拘束できるか確認します。読み取り専用で進めます。
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
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
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
/bin/zsh -lc 'nl -ba .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
     1	---
     2	format: 2
     3	task_id: dotfiles-T133-verdict-audit-pool-a04
     4	kind: code
     5	security: true
     6	allowed_files:
     7	  - scripts/orchestrator/verdict.sh
     8	  - .schemas/verdict.json
     9	  - .schemas/audit.json
    10	  - tests/unit/test_verdict.py
    11	  - .orchestration/dotfiles-T133-verdict-audit-pool-a04/**
    12	after: [dotfiles-T133-worker-write-boundary-a01]
    13	reset_of: [dotfiles-T133-verdict-audit-pool-a03]
    14	threat_table:
    15	  - control: "scripts/orchestrator/verdict.sh (nine conditions, trusted-parent startup, fixed executable identities, contained output and explicit security metadata)"
    16	    disposition: "residual: the regression fixtures exercise the declared execution and write controls; these controls reduce accidental and prompt-injected execution but do not isolate hostile processes sharing the orchestrator's UID."
    17	  - control: ".schemas/verdict.json (the accept, revise and hold contract)"
    18	    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold"
    19	  - control: ".schemas/audit.json (the audit contract and controlled class vocabulary)"
    20	    disposition: "residual: schema rejection is exercised by the retained validator tests; the sibling owns the separate vocabulary file and its equality test."
    21	  - control: "tests/unit/test_verdict.py (retained behavior cases and the reset-design regressions)"
    22	    disposition: "residual: temporary repositories and fixed fixture executables expose arguments, marker writes and side effects; they do not establish host isolation or authenticate live GitHub state."
    23	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/** (this reset task's artifacts)"
    24	    disposition: "residual: artifacts identify their commands, tested heads and provenance; historical a03 evidence remains distinguishable from a04 final-head results."
    25	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md (dispatched task copy)"
    26	    disposition: "residual: the first push adds the byte-identical dispatched a04 text; the TASK and RESULT bind this copy's own SHA256, which the orchestrator compares independently."
    27	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md (predecessor task-copy deletion)"
    28	    disposition: "residual: the first push deletes only this predecessor copy under the explicit reset-bookkeeping exception; other a03 evidence remains unchanged."
    29	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/report.md"
    30	    disposition: "residual: the report distinguishes inherited evidence, new results and retained predecessor artifacts; a local record does not authenticate its author."
    31	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/validation.md"
    32	    disposition: "residual: validation records commands, red results, final-head results and tested heads; pasted output does not authenticate its source."
    33	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/sandbox.md"
    34	    disposition: "residual: the record identifies refused commands and the observed boundary without claiming isolation from unrestricted same-UID processes."
    35	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/learning.md"
    36	    disposition: "residual: reusable learning remains separate from executable policy and from predecessor evidence."
    37	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/autoskill.md"
    38	    disposition: "residual: the run status or not-used record grants no execution or promotion authority."
    39	  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/revise.yaml"
    40	    disposition: "residual: revision instructions and selectors remain data, bounded by this task's files, caps and round allowance."
    41	  - control: "agmsg storage route (~/.agents/skills/agmsg/scripts/lib/storage.sh; no application path exists in this task)"
    42	    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path"
    43	  - control: "application integration gate (make require-crit-review; no application path exists in this task)"
    44	    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path"
    45	  - control: task metadata
    46	    disposition: "residual: the orchestrator checks format-2 consistency before dispatch and at acceptance, validates security as an explicit boolean, and compares the complete dispatched task with its branch copy."
    47	  - control: metadata separators
    48	    disposition: "residual: the first opening and closing document separators bound safe-loaded YAML; the byte comparison also covers the body and subsequent separators."
    49	  - control: in-process effects
    50	    disposition: "residual: the Python child contains verdict and shadow writes; hold never appends a shadow row, and no application path exists in this task. --apply exits 2 with its named refusal; verdict never dispatches, calls the gate, executes agmsg code or merges."
    51	  - control: workflow and interpreter or environment inputs
    52	    disposition: "residual: a trusted parent supplies the clean environment before any exec, startup checks refuse rather than repair, and internally fixed executable paths remove the caller-bin interface; shared-UID access to installations, credentials and host state remains outside the isolation these controls provide."
    53	  - control: new or renamed scripts
    54	    disposition: "residual: verdict.sh remains the only implementation executable introduced by this PR; no pool executable, caller wrapper, dependency or production test-override interface is added."
    55	  - control: orchestrator effect merge
    56	    disposition: "residual: only the orchestrator performs the live head-matched squash merge with --repo mryfmo/dotfiles after the prescribed evidence and integration gate; verdict has no application path."
    57	  - control: orchestrator effect update-branch
    58	    disposition: "residual: an update-branch changes the head and invalidates head-bound evidence; the orchestrator repeats required CI, feedback collection, audit and security review for the resulting head."
    59	  - control: orchestrator effect forced worker removal
    60	    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state."
    61	  - control: "design 5.14 item 1 (worker write boundary)"
    62	    disposition: "residual: the worker does not change its own execution boundary; Claude write isolation is not inferred from render-check, and the orchestrator verifies the deployed boundary separately."
    63	  - control: "design 5.14 item 2 (sanitized environment before execution)"
    64	    disposition: "residual: a trusted parent supplies the clean environment, including passwd-derived HOME, before exec; the program checks allowed names, its resolved script path and HOME and exits 2 on refusal without self re-exec. Privileged mode alone cannot prevent Linux loader execution; caller integration and shared-UID host execution remain separately assessed."
    65	  - control: "design 5.14 item 3 (trusted path boundaries)"
    66	    disposition: "residual: resolved executable and destination paths are checked against the declared trusted roots; a same-UID process outside a worker sandbox can still mutate host paths."
    67	  - control: "design 5.14 item 4 (execute verified identities and consume verified contents)"
    68	    disposition: "residual: executables run by verified realpath, consumed snapshots are rehashed immediately before use, and decision-input hashes enter the verdict; snapshots do not create a boundary against unrestricted same-UID mutation."
    69	  - control: "design 5.14 item 5 (output and reservation identity)"
    70	    disposition: "residual: verdict and evidence snapshot filenames and shadow rows use the full head; each audit, security, local-review and sweep input is also matched by its full-head metadata, and this verdict task introduces no reservation lock."
    71	  - control: "design 5.14 item 6 (honest residuals)"
    72	    disposition: "residual: startup, path and snapshot controls are reported as damage reduction; neither host isolation nor independent GitHub credentials is claimed."
    73	  - control: "design 5.14 item 7 (verification)"
    74	    disposition: "residual: this task supplies concrete regression selectors and final-head evidence; the shared trusted-execution test helper remains owned by P1-6 and is reused only if available without expanding this task's edit boundary."
    75	  - control: "design 5.14 item 8 (committed approval ledger)"
    76	    disposition: "residual: verdict evaluation supplies no permission approval; every gh call names mryfmo/dotfiles explicitly, and PR data comes from GitHub at one base/head pair captured once and recorded at full SHAs, never shared refs or objects. No application path exists in this task; shared credentials remain a residual."
    77	  - control: "design 5.14 item 9 (private cache and absolute interpreter)"
    78	    disposition: "residual: the shared trusted-interpreter resolver anchors the install root to the passwd home of the real uid, never HOME, and the anchored private uv cache excludes worktrees, worker-writable caches and temporary directories; until the P1-3 resolver is available, verdict holds without a private resolver or PATH fallback."
    79	  - control: "design 5.14 item 10 (worker commands remain sandboxed)"
    80	    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; a command that cannot complete there produces a blocked PONG rather than an escape or alternate execution route."
    81	premises: []
    82	---
    83	
    84	# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a04 — INV-6 S1 re-plan of a03 (plan 024 P1-4a; PR #410)
    85	
    86	Worker: a008, Claude Code, worktree `worker-f`.
    87	
    88	This text is the independent redesign by a review-profile context other than the author of the predecessor task texts. The a03 pre-push fix round and revise 1 exhausted its C-61 allowance. The security review of `513e5d05` found caller-controlled executable selection and cached-bytecode execution; the review of `6b7e7833` found inherited `compgen` execution, acceptance of attacker-selected absolute symlink targets, uncontained output writes and an implicit non-security branch.
    89	
    90	The a03 acceptance record contains three `env-trust-bypass` rows: `security:513e5d0:1`, `security:6b7e783:1` and `security:6b7e783:2`. Its recorded `re-plan:` line establishes INV-6 S1. Another a03 patch round is not authorized. This reset changes the execution contract so a trusted parent supplies the clean environment before exec, the program verifies and refuses without self re-exec, and no caller executable directory exists.
    91	
    92	Read these records before implementation:
    93	
    94	- `.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md`
    95	- `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md`
    96	- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md`
    97	- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md`
    98	
    99	The design at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, section 5.14, applies by reference, including today's amendments to items 2, 8 and 9 and items 4 and 5. This absolute path identifies the orchestrator's uncommitted working copy under C-86. The task does not claim that section is already on `origin/main`.
   100	
   101	The sentences of section 5.14 this task relies on are quoted here verbatim (C-88: the quoted sentences are normative; the path above is context, and the design file is uncommitted at authoring time):
   102	
   103	> 2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
   104	
   105	> 4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
   106	
   107	> 5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
   108	
   109	> 8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder: the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged.
   110	
   111	> 9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record.
   112	
   113	
   114	Host controls reduce accidents and prompt-injected damage. They do not isolate unrestricted processes sharing one UID. The design's GitHub prevention boundary is also not established while worker and orchestrator credentials remain accessible to that same UID; subsequent boundary-record checks provide detection as the design states.
   115	
   116	## Branch and reset boundary
   117	
   118	Continue `tools/verdict-audit-pool-a01`, PR #410, from `6b7e7833a85528440dc397c2555bc9dd603c685a`, already update-branched onto main `3f240b12`. Keep the a03 implementation, regression coverage and evidence. Create neither another implementation branch nor another PR.
   119	
   120	The first push deletes `.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md` and adds the dispatched text byte-for-byte at `.orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md`. This single predecessor-copy deletion is the explicit reset-bookkeeping exception to `allowed_files`. Other a03 evidence remains unchanged under its original task identifier and tested heads.
   121	
   122	The orchestrator retains the a03 acceptance history, class rows, stopped status and counters. The final inventory identifies preserved a03 evidence separately from a04 additions; preservation does not authorize further worker edits in the a03 directory. The a01/a02 artifact removals already completed by a03 are not repeated or reversed.
   123	
   124	The split remains intact. The pool sibling owns `scripts/orchestrator/audit-pool.sh`, changes to `scripts/orchestrator/orch-audit.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py`. `audit-pool.sh` is absent at `6b7e7833`; the audit schema at that head is `.schemas/audit.json`. Neither fact authorizes recreating a split file or adding a `schemas/` mirror. PR #407 remains parked; its parking operation is not repeated.
   125	
   126	## Goal
   127	
   128	Produce one schema-valid verdict from nine positively checked conditions without executing inherited shell startup code, accepting caller-selected executable directories, following output symlinks or treating invalid `security` metadata as an exemption.
   129	
   130	Retain complete feedback validation, amended-cap precedence, offline operation and finding counts. This task computes and records shadow verdicts only; `--apply` is rejected as item 6 specifies.
   131	
   132	## Files
   133	
   134	1. `scripts/orchestrator/verdict.sh <pr> [--loop] [--shadow]` remains Bash with `set -Eeuo pipefail`, English shdoc documentation and `jq` for JSON. Its startup and executable selection follow the Reset design below. Each condition is `{id, ok, evidence}` and becomes true only through a positive check of parsed, validated input.
   135	
   136	   Inputs remain the PR view and checks, the acceptance record's JSON block and prose, the selected task or `--task <id>`, the audit JSON, a fresh feedback sweep, saved feedback dispositions, the task's allowed paths and caps, regime counters, the GitHub merge-base changeset and the head-specific security review. The acceptance block names the PR, task and current head and contains a ledger array. The PR is open, non-draft and based on `main`. At the start of each PR evaluation, capture `head.sha` and `base.sha` together once from `gh api repos/mryfmo/dotfiles/pulls/<pr>` as `head40` and `base40`, require both to be 40 lowercase hexadecimal characters, and bind all reads to that pair. Record both in the verdict JSON as `head` and `base`. The compare listing and file contents are read from GitHub at that captured pair; no separate current-main read replaces either value. If a second PR read is needed, compare both SHAs with the captured pair and refuse with hold, exit 20 and `verdict: PR base/head changed during evaluation` if either differs; append no shadow row and never combine reads from different pairs. This task chooses GitHub API reads, not a local clone: read the changeset through `…/compare/<base40>...<head40>` and inspected PR bytes through `…/contents/<path>?ref=<head40>`. Repository identity is fixed to `mryfmo/dotfiles` from the trusted repository declaration, not caller environment or local Git configuration. Every `gh pr`, `gh run` and `gh issue` invocation supplies `--repo mryfmo/dotfiles` or the full pull-request URL; every `gh api` invocation, including instantiated API templates in the design quotation, uses an explicit `repos/mryfmo/dotfiles/…` endpoint path, never `--repo` or a `{owner}/{repo}` placeholder. A matching head SHA in a fork is not a repository binding. Missing, incomplete, truncated or unreadable API data holds; no local-head fetch or shared-object fallback is allowed.
   137	
   138	   Condition 1 verifies that the GitHub contents response for `.orchestration/<task>/precheck.json?ref=<head40>` hashes to the record's `precheck:` value and names the head or an ancestor authenticated by GitHub compare data whose diff to the head contains only `.orchestration/<task>/` paths. The retained `PRECHECK_REQUIRED` setting is supplied explicitly as `--precheck-required 0|1`; absent or zero makes this condition's failure a warning. No environment exception is added for it.
   139	
   140	   Condition 2 requires every required check to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Every duplicate entry for a required name must also be `SUCCESS`.
   141	
   142	   Condition 3 requires an audit that validates against `.schemas/audit.json`, names the task and full head, has zero open P0/P1 findings, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit without remaining findings fails this condition.
   143	
   144	   Condition 4 requires saved and fresh feedback documents to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Diagnostic URLs do not determine the result.
   145	
   146	   Condition 5 requires every path in the base-to-head diff to match an `allowed_files` entry and additions-plus-deletions totals to remain within the effective Check caps. The comparison is `gh api repos/mryfmo/dotfiles/compare/<base40>...<head40>` using the PR API's base and head, and its full `merge_base_commit.sha` identifies the merge base. Consume the complete authenticated file list and its additions/deletions; account for both names of a rename. An unreadable merge base or incomplete changeset holds. The main checkout's `.git`, including `origin/main`, replacement refs and objects, is not an evidence source. Backticked exclusions after `outside` leave the outside count; default exclusions remain `tests/` and `.orchestration/`. Item 7 retains amendment precedence.
   147	
   148	   Condition 6 reads one orchestrator-pasted INV-6 counters block in the acceptance record, bound there to this task, PR and full head. This task chooses the pasted record rather than a live store query so verdict executes no agmsg shell code and cannot follow worker-writable `drivers.partition`. It never invokes `scripts/regime-counters.sh` or sources the agmsg storage layer. No `S1:` line is present and the parsed decimal `revises` value is below 2. A missing ledger or counters block, duplicate block, mismatched binding or unreadable count holds; an absent count is never zero.
   149	
   150	   Condition 7 requires the numeric count of open P0/P1 findings to be zero. Findings with status `new`, `still-open` or absent count as open regardless of identifier or scope.
   151	
   152	   Condition 8 first validates `security` as an explicit boolean. Only boolean `false` permits the non-security branch. Boolean `true` requires the security review's front-matter `head:` to equal the verdict's own full 40-hex head and its last non-blank line to be `Verdict: correct`. A sha7 filename is never a head match. Missing, null or non-boolean metadata holds with the named reason specified below.
   153	
   154	   Condition 9 requires at least one `sha256:<hex> <path>` line in the acceptance record's prose and verifies every such line against its file. Every inspected evidence file, including audit, security, local review and saved or fresh sweep, is named with and matched against the verdict's full 40-hex head: Markdown uses front-matter `head:`, audit and local-review JSON use `head` (on every record for a JSON list), and feedback JSON uses `head_sha`. Missing, invalid or different full-head metadata holds even when a filename or sha7 prefix matches. Hashes preserve consumed bytes; they do not authenticate a local Git object or ref.
   155	
   156	   All nine conditions passing produces `accept`. Failure of condition 6 or 7, missing or unreadable input, schema-invalid input, invalid security metadata or an internal evaluation error produces `hold`. Other failed conditions produce `revise`. The revise line remains `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies `check=` selectors.
   157	
   158	   The generated verdict is `.orchestration/validation/<task>-verdict-<head>.json`, using the full 40-character head under design 5.14 item 5. Its fields are `verdict`, `pr`, `head`, `base`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`, validated against `.schemas/verdict.json`. Audit, security, local-review and sweep inputs use full-head-named verified snapshots with the metadata bindings above. External producers are not edited; the orchestrator supplies the full-head-named evidence and required metadata before evaluation, retaining original artifacts separately. Historical verdict files remain untouched.
   159	
   160	   Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with internal error treated as hold. A destination or post-startup execution-boundary refusal holds with exit 20; the mandatory startup refusals in Reset design item 1 exit 2 with their named messages. Refusal before a usable task or head exists reports hold without inventing an output identity.
   161	
   162	   `--apply` is unsupported and exits 2 with `verdict: --apply is not supported in this shadow-only task` before input reads or tool calls other than mandatory startup verification. No application branch, dispatch, gate call, agmsg execution or merge remains. Arguments containing `--admin` or `--auto` anywhere are refused with exit 2 before input reads or tool calls other than mandatory startup verification.
   163	
   164	   Shadow evaluation is the default; `--shadow` is its explicit spelling. It writes the verdict JSON and, only for a non-hold verdict, appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`. Columns remain `pr`, `head`, `machine`, `human`, `agree` and `at`; the orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing, invokes no dispatch, gate or agmsg code, and treats no gate conclusion as binding.
   165	
   166	   `--loop` retains PR-number order, eligible open non-draft PRs on `main`, and an acceptance record naming each current head. Each recursive verdict invocation uses the sanitized program-entry contract and captures that PR's single base/head pair at its start as above. The loop computes and records shadow verdicts only; it never refreshes a checkout, dispatches, calls the gate, executes agmsg code or merges. Evaluation never uses the main checkout's shared refs or objects.
   167	
   168	2. `.schemas/verdict.json` and `.schemas/audit.json` remain JSON Schema 2020-12 documents with `additionalProperties: false` at the top level and in defined item objects.
   169	
   170	   The audit contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and optional `status`. The controlled class enum retains the vocabulary snapshot at `b8998de162afc72d53d07679b8f0a194fcc480ff`.
   171	
   172	   The existing stdlib schema validator remains available through `--validate` under the fixed isolated interpreter, without a new helper file or dependency. Required keys, types, enums, bounds, SHA patterns, additional-property restrictions and RFC 3339 timestamps with offsets remain checked. Date-only values, naive timestamps and invalid calendar dates fail. Runtime validation does not depend on the sibling's `orch-audit.sh --validate`.
   173	
   174	3. The retained interpreter-selection requirement is implemented through Reset design item 2 rather than the a03 caller-bin mechanism.
   175	
   176	   Before PR input processing, the trusted entrypoint fixes absolute executable identities and the offline PyYAML environment. Checkout `.python-version`, `.venv`, executable files, uv configuration, mise configuration and inherited tool-selection variables cannot select an interpreter or tool. Missing trusted installations or unavailable offline dependencies hold before evaluation.
   177	
   178	   The historical interpreter regression against `85a472294d0c10835bd7235e3c76d045846a6ed9` remains identified as historical. Its marker-writing interpreter cases run again against the final implementation.
   179	
   180	4. The a02 and a03 finding-count and feedback fixes remain acceptance requirements.
   181	
   182	   Conditions 3 and 7 count open P0/P1 findings numerically. Empty identifiers and records scope cannot hide a finding.
   183	
   184	   Condition 4 requires both saved and fresh `head_sha` values to equal the accepted head. Missing or invalid dispositions are counted before formatting URLs; null and empty URLs affect diagnostics only.
   185	
   186	   Complete identity and multiplicity retain the trusted helper's `feedback_key()` and `missing_feedback()` behavior. Source, URL, level, path, line, body and author participate, with only existing exact masked-body and masked-path equivalence. One saved occurrence covers one fresh occurrence.
   187	
   188	   Dispositions retain `parse_disposition()` validation and `commit_in_range()` semantics, but verdict checks commit membership through complete GitHub compare/commit data instead of calling the helper's local-Git range check. A fix commit exists within the authenticated base-to-head range. A not-applicable disposition has a non-empty reason and evidence command and satisfies existing level-specific reason requirements. Evidence commands remain data and are never executed.
   189	
   190	   Neither `scripts/require-crit-review.py` nor its validator is edited. Shadow evaluation never calls the gate or treats its conclusions as binding. Retained red evidence keeps its original head; final-head green results are new evidence.
   191	
   192	5. `tests/unit/test_verdict.py` retains the sixteen shadow behavior tests at `6b7e7833`, including schema-rule rejection, offline PyYAML refusal, numeric finding counts, feedback head binding, null diagnostic URLs, identity and multiplicity, disposition validation, amended caps and cached-bytecode refusal. Delete the three application, gate-order and post-merge checkout-refresh tests and their application-only fixtures; retain the `--admin` and `--auto` refusal controls in the no-application-path regression below.
   193	
   194	   The a03 test named `test_verdict_ignores_caller_bin_and_path_overrides` retains its coverage of hostile PATH selection while its removed executable-directory fixture is replaced by the fixed-entrypoint fixture: direct dirty invocations refuse, and trusted-parent clean invocations preserve the verdict without executing planted tools. Neither the script nor the test source retains `VERDICT_BIN` or another production executable-directory override.
   195	
   196	   Existing shadow positive and negative controls remain: empty checks, failed duplicate checks, blocked audits, incorrect audits without findings, missing ledgers and records, unavailable GitHub heads, unreadable GitHub merge bases, backticked cap exclusions and absent evidence hashes.
   197	
   198	   Fixtures use temporary repositories and fake external tools whose absolute identities are established in the fixture's trusted entrypoint before invocation. They do not reintroduce caller PATH discovery or a production test-only override. The actual Python used for valid execution satisfies the interpreter boundary. All fixture lines count toward the test cap.
   199	
   200	6. No application path exists in this task.
   201	
   202	   Remove application code, prerequisite-ledger reads, agmsg installation checks and their tests. `verdict.sh` never dispatches, calls the gate, executes agmsg code or merges, including in `--loop`. It computes and records only the shadow verdict JSON and non-hold TSV row described in item 1. Passing `--apply` exits 2 with `verdict: --apply is not supported in this shadow-only task` before input reads or tool calls other than mandatory startup verification; no verdict or shadow row is written for that usage refusal.
   203	
   204	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path` covers default, `--shadow` and `--loop` evaluation and unsupported `--apply`, including `--loop --apply`. Shadow evaluations record the schema-valid JSON with full `head` and `base` and append only the machine TSV columns for non-hold verdicts. Marker-writing gate, dispatch, history and agmsg fixtures remain untouched and no merge occurs. The `--apply` cases require the named message, exit 2, no PR or prerequisite reads and no output writes. The retained `--admin` and `--auto` controls still refuse before input reads or effect calls.
   205	
   206	7. The retained cap-parser fix remains enforced.
   207	
   208	   The last applicable cap declaration in text order governs, including its exclusions and outside limit. A later test-only amendment changes the test limit while retaining the outside limit.
   209	
   210	   `test_verdict_condition_5_honors_the_latest_amended_caps` retains the original 500 versus amended 550 case with 531 changed test lines, the actual a02 test-only wording, a later lower limit, changed exclusions and changed outside limit. Unrelated conditions stay green and evidence hashes are refreshed. Its original red head remains historical.
   211	
   212	The required check names remain `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.
   213	
   214	## Reset design
   215	
   216	1. **A trusted parent supplies the clean environment before exec; startup verifies and refuses.**
   217	
   218	   `verdict.sh` has mode 0755 and shebang `#!/bin/bash -p`. A trusted parent invokes it with `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …`, with long Bash options before `-p`. The parent supplies a clean environment before any exec, including the exec of `/usr/bin/env` itself; launching that prefix with inherited loader variables is not sanitization before the loader. Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but does not enable the loader’s secure-execution mode. On Linux, inherited `LD_PRELOAD` or `LD_AUDIT` can execute before Bash’s first statement. There is no self re-exec and no reopening of caller-controlled `$0`.
   219	
   220	   Before `set`, traps, argument processing or executable discovery, the first executable compound statement verifies privileged mode, the startup environment, the script path and HOME. A missing privileged mode refuses with exit 2 and `verdict: execute as a program`. Check environment names through absolute `/usr/bin/env` and `/usr/bin/grep`; exactly `PATH`, `HOME`, `LANG`, `PWD`, `SHLVL` and `_` are allowed, with fixed `PATH=/usr/bin:/bin` and `LANG=C.UTF-8`. An extra/missing name or wrong fixed value refuses with exit 2 and `verdict: untrusted startup environment`. A caller-set sentinel proves nothing and is not accepted.
   221	
   222	   Resolve `$0` with the fixed absolute realpath utility and require an absolute invocation path whose realpath is a regular file under the anchored repository root; otherwise exit 2 with `verdict: untrusted script path`. Resolve the real uid through absolute `/usr/bin/id -ru` and obtain its passwd home through `/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS (the user is resolved from that real uid), or `/usr/bin/getent passwd <uid>` on Linux. Missing, ambiguous or unreadable account data, or HOME unequal to that passwd home, exits 2 with `verdict: HOME does not match passwd home`. The repository root and passwd-home lookup do not derive from caller HOME, PWD or local Git configuration. Refuse instead of repairing any failed check. No `compgen`, `unset -f` loop or PATH edit serves as the startup boundary.
   223	
   224	   Every ordinary caller, including the loop child and test helpers, is the trusted parent for that exec and uses the exact clean prefix with the passwd home and absolute script path; no sentinel is exported or trusted. The retained `PRECHECK_REQUIRED` control is passed as the explicit `--precheck-required 0|1` argument when needed, defaults to 0, and is never inherited or retained as an environment name.
   225	
   226	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_program_discards_hostile_startup_environment` executes the program with exported functions named `compgen`, `[`, `test`, `exec`, `command`, `builtin` and `command_not_found_handle`, a marker-writing `BASH_ENV`, `LD_PRELOAD` and `LD_AUDIT` naming marker-library paths, a forged HOME containing a marker-writing interpreter, and a planted PATH. The fixture also supplies the other startup selectors discarded by privileged mode. The direct dirty invocation must exit 2 with `verdict: untrusted startup environment` and no marker; it must not repair or re-exec. The direct dirty cases use deliberately non-loadable library paths: a loadable constructor cannot be prevented after a dirty exec. Exercise a loadable marker library only through the already-trusted parent supplying the clean environment before every exec, and require no marker. The clean prefix must yield the unchanged clean verdict and conditions, so an incidental exit 2 cannot pass the positive control.
   227	
   228	   Separate subcases exercise each named refusal: a forged HOME with otherwise allowed names and fixed values, a symlinked `$0` resolving outside the repository, and `VERDICT_SANITIZED=1` together with `GIT_CONFIG_GLOBAL`, `GIT_DIR` and `GIT_INDEX_FILE` pointing to planted files. Require the appropriate named message, exit 2, no marker or application effect and no consumption of planted configuration, objects or index. Check the clean child’s allowed-name-only environment and passwd-derived HOME. Exercise the exact long-options-before-`-p` command.
   229	
   230	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_bash_file_invocation` invokes `bash scripts/orchestrator/verdict.sh …` in a clean fixture and requires exit 2 and the named message. This negative invocation is the sole deliberate plain non-privileged Bash verdict call in the tests.
   231	
   232	2. **Executable identities are fixed at the trusted entrypoint.**
   233	
   234	   No caller-supplied executable directory exists. Remove `VERDICT_BIN`, its environment whitelist, symlink-directory acceptance and every equivalent caller override from the script and fixtures. Do not replace them with a differently named environment variable or CLI option.
   235	
   236	   The trusted entrypoint fixes the absolute paths for Bash, uv, Python, gh, git, jq and required utilities before reading PR-controlled input. It executes verified realpaths without rediscovery. The repository's Python declaration is a read-only input; consume `scripts/orchestrator/trusted-interpreter.sh` from the authenticated trusted base when present. The P1-3 resolver alone resolves the pinned declaration to a regular executable file under the tool manager's install root, anchored to the passwd home of the real uid, never to HOME, and outside worktrees, worker-writable caches and `$TMPDIR`. A symlink spelling alone authenticates nothing. An absent resolver or invalid trusted installation holds rather than selecting another interpreter from PATH, mise, uv discovery or a checkout. No private resolver, `command -v` or `mise which` fallback is retained here. Implementation may proceed before `dotfiles-T133-ci-efficiency-followup-a04` lands by implementing and testing this unavailable-resolver hold with a trusted resolver fixture for successful cases; live execution stays on hold until that lineage supplies the resolver. This task therefore does not need the resolver at implementation time and adds no P1-3 `after:` dependency.
   237	
   238	   Design 5.14 items 2, 4 and 9 apply by reference to Git invocation, executable paths, verified snapshots and private cache use. The uv invocation is `uv run --no-config --no-project --offline --python <abs>`, with uv itself an internally fixed absolute executable and `<abs>` the validated interpreter realpath. `UV_CACHE_DIR` is the anchored private cache from the design. Worker-shared uv or mise caches supply no executable. Python children use `-I`; the a03 `-B`, `sys.dont_write_bytecode` and refusal of checkout bytecode that helper imports could consume remain enforced.
   239	
   240	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_uses_only_declared_absolute_executables` verifies fixed tool identities, refusal of hostile PATH and inherited interpreter selectors, and unchanged clean-prefix execution, including an absolute symlink to a marker-writing interpreter and a forged HOME install tree that cannot become the trusted install root.
   241	
   242	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_interpreters_in_worktrees_caches_or_tmp` covers each excluded root, a non-regular target, a forged-HOME install root and a valid regular-file control under the passwd-home-anchored install root.
   243	
   244	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_executes_verified_snapshots_and_records_input_hashes` changes a validated source or input before consumption and verifies refusal or consumption of the verified snapshot, never the substituted contents, and checks the recorded input hashes.
   245	
   246	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_without_the_shared_trusted_interpreter_resolver` verifies the interim hold and absence of interpreter discovery or application effects.
   247	
   248	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_reads_pasted_counters_without_sourcing_agmsg` plants a marker-writing agmsg driver and counter executable, supplies the valid pasted counters, and requires unchanged verdicts with no marker; missing, duplicate, mismatched and unreadable counter cases hold.
   249	
   250	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_ignores_replaced_local_objects_and_refs` serves forged PR bytes through a replaced local object and forged `origin/main`, while fixed GitHub fixtures return the authentic full-head changeset and contents. It requires the clean verdict and authenticated input hashes, no local-object evidence read, and hold on incomplete API data rather than a local fallback. Cover precheck ancestry, fix-commit membership and loop shadow evaluation through the same GitHub fixtures.
   251	
   252	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_names_the_repository_on_every_gh_call` runs with a fixed fake gh that records every argument vector and asserts `--repo mryfmo/dotfiles` on every `gh pr`/`gh run`/`gh issue` call and an endpoint path beginning with `repos/mryfmo/dotfiles/` on every `gh api` call, with no `--repo` flag or repository placeholder on API calls. It covers PR view/checks, API and feedback reads and loop shadow evaluation in PR-number order. A fork fixture containing the same head SHA cannot redirect a call.
   253	
   254	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_a_changed_pr_base_or_head` supplies one initial GitHub `base40`/`head40` pair and differing SHAs on a required second read. Separate subcases change only the base, only the head and both. Each requires the named pair-change refusal, hold with exit 20 and no shadow row; the unchanged-pair control records both full SHAs and proves every compare listing and contents request uses the captured pair.
   255	
   256	   The retained `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` and `test_verdict_never_imports_cached_bytecode` remain green. Unavailable offline PyYAML still holds with no online fallback.
   257	
   258	3. **The Python child contains persistent writes.**
   259	
   260	   Verdict JSON and shadow logging are opened through the fixed isolated Python child inside `<repo>/.orchestration/validation/`. Their resolved paths remain inside the repository and the validation directory. Symlinks, non-regular files and paths outside that boundary refuse before truncation or append. Directory-component validation and descriptor checks prevent a symlinked parent from defeating a leaf-only check.
   261	
   262	   Both opens use `O_NOFOLLOW`; shadow logging also uses `O_APPEND`. Regular-file checks apply to the opened descriptor. Shell `>` and `>>` redirections do not open these destinations. The JSON is schema-valid before it is committed to its destination. A write refusal holds and performs neither dispatch nor merge.
   263	
   264	   On `hold`, the shadow log receives nothing, whether absent or already populated. A contained hold JSON may still be written when task and head are known.
   265	
   266	   New verdict filenames use the full head; every shadow row retains the full head. No reservation or lock mechanism is introduced.
   267	
   268	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_opens_outputs_without_following_symlinks` plants a symlink separately at the JSON destination and shadow-log destination, requires refusal, and verifies each target's bytes remain unchanged. It includes escaping-parent and non-regular destination controls.
   269	
   270	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_shadow_does_not_append_on_hold` checks absent and populated logs and unchanged prior bytes. The existing successful shadow-column test remains green.
   271	
   272	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_output_names_use_the_full_head` checks the full-head JSON filename and shadow identity rather than accepting a seven-character output name.
   273	
   274	4. **Security metadata is an explicit boolean.**
   275	
   276	   Validate the parsed task's `security` value before selecting condition 8's branch. Missing, null or non-boolean values produce condition 8 failure, overall hold with exit 20, and the named reason `security must be an explicit boolean`. They never produce `not a security task`, append a shadow row, dispatch or merge.
   277	
   278	   Only boolean `false` permits the no-security-review branch. Boolean `true` retains the required head-specific review, with front-matter `head:` exactly equal to the verdict's full 40-hex head. A quoted `"false"` is a string and does not exempt the task.
   279	
   280	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_evidence_for_another_full_head_with_the_same_sha7` uses two distinct 40-hex heads sharing their first seven characters. Separate subcases substitute the audit, security report, local review and saved or fresh sweep; each mismatched or absent full-head field holds despite a matching prefix and a correct security verdict. Full-head-matched controls remain green.
   281	
   282	   Add these separate tests:
   283	
   284	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_missing`
   285	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_null`
   286	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_string`
   287	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_an_integer`
   288	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_float`
   289	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_list`
   290	   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_mapping`
   291	
   292	   Each test checks the named reason, hold and absence of application effects. The true and false positive controls remain in the retained condition tests. Unreadable or malformed YAML also holds.
   293	
   294	## Caller inventory and ownership
   295	
   296	At `6b7e7833`, executable verdict callers are the `--loop` child invocation in `scripts/orchestrator/verdict.sh` and the helpers and direct subprocess calls in `tests/unit/test_verdict.py`. Both files are in `allowed_files`. Update every ordinary call to the trusted-parent clean-prefix form with passwd-derived HOME and an absolute script path; the explicit dirty-environment and refusal tests remain the named exceptions.
   297	
   298	There is no direct verdict invocation in the PR head's CI workflows and no separate tracked shadow-runner executable. CI exercises the updated test helper. This task's concrete shadow command below is the shadow runner. Do not add an unused wrapper or workflow step.
   299	
   300	The orchestrator owns the follow-up connection in `scripts/orchestrator/chain-integrate.sh` and its local glue `.agents/worklog/orchestrator-glue/integrate-pr.sh`. Before either connects to verdict execution, the orchestrator applies the same trusted-parent clean-environment-before-exec contract with passwd-derived HOME and an absolute script path. Those files are not edited by a008. Any later direct CI or shadow caller follows that contract before use.
   301	
   302	## Measured budget
   303	
   304	The read-only command `git diff --numstat 3f240b12 6b7e7833` produced these relevant rows:
   305	
   306	```text
   307	11	0	.schemas/audit.json
   308	10	0	.schemas/verdict.json
   309	278	0	scripts/orchestrator/verdict.sh
   310	399	0	tests/unit/test_verdict.py
   311	```
   312	
   313	The implementation budget is the measured 278 script lines plus Reset design estimates of 60 for startup and callers, 95 for fixed execution and verified consumption, 90 for contained writes, 20 for explicit security metadata, 20 for pasted-counter validation, 70 for GitHub changeset reads with single-pair and explicit repository binding, and 25 for full-head evidence binding, the measured 21 schema lines and 11 lines of reserve: `278 + 60 + 95 + 90 + 20 + 20 + 70 + 25 + 21 + 11 = 690`.
   314	
   315	The test budget is the measured 399 lines plus corresponding estimates of 200, 130, 110, 60, 50, 95 and 60 (the startup estimate adds 60 for refusal, passwd-home and loader cases), 50 for every-call repository arguments, with 41 lines of reserve: `399 + 200 + 130 + 110 + 60 + 50 + 95 + 60 + 50 + 41 = 1195`. The startup and GitHub-read estimates include the no-application-path and differing-SHA regressions respectively.
   316	
   317	These are cumulative PR ceilings, not targets. Changed lines mean additions plus deletions; fixture changes count. No behavior, validation, assertion or trust-boundary control is removed to meet them.
   318	
   319	## Out of scope
   320	
   321	Pool implementation, the audit wrapper, vocabulary ownership, `dispatch.sh`, record generation, `dispositions.py`, `--second-opinion`, `hold-playbook.sh`, `integrate-seat.sh`, gate and validator changes, task-checker implementation, Makefile targets, CI changes, model configuration, worker permission configuration and live deployment remain outside this task.
   322	
   323	Application belongs to the later task `dotfiles-T133-verdict-apply-a01`, which is not written. That task owns its own prerequisites and four-distinct-PR agreement enforcement. This task has no application path and does not implement a dormant or prerequisite-gated `--apply` mode.
   324	
   325	The four findings from the `6b7e7833` security review belong to this reset, including its two P2 findings. They are not assigned to an advisory owner. The a03 no-bytecode fix remains in scope as retained behavior.
   326	
   327	## Check
   328	
   329	Write the new regressions before their implementation changes. Record each new regression's red result against `6b7e7833a85528440dc397c2555bc9dd603c685a` and green result after the fix. A red result must reach its named defect; an unrelated startup or fixture failure is not evidence. Historical a01/a02/a03 red results retain their original references and do not replace new or final-head results.
   330	
   331	The validation file contains commands, verbatim output, exit statuses and tested heads for `make unit-test`, `make render-check`, `make format`, `shellcheck scripts/orchestrator/verdict.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/verdict.sh` and `uv run python -m unittest tests.unit.test_verdict -v`. The script checks are clean and the verdict module is green. Record the executable mode and exact shebang.
   332	
   333	Run every Reset design selector, including all seven invalid-security tests, retain all sixteen inherited shadow behavior tests and run the no-application-path and differing-SHA regressions. Record the fixed executable realpaths, trusted interpreter and cache location without exposing credentials. Confirm that no executable-directory override remains in script or test source.
   334	
   335	The concrete shadow invocation, issued by the trusted parent with a clean environment before exec, is `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <repo>/scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a04`, where `<repo>` is the anchored absolute repository root and `<passwd home>` is the real uid’s passwd home. Its JSON, exit status, tested head and unchanged shadow-log state on hold appear in `.orchestration/dotfiles-T133-verdict-audit-pool-a04/validation.md`. Hold is expected before required audit and acceptance evidence exists. No live `--apply` is exercised.
   336	
   337	`git diff --numstat --no-renames origin/main...HEAD` shows at most 690 changed lines outside `tests/` and `.orchestration/`, including both JSON schemas, with `verdict.sh` limited to 669 physical lines.
   338	
   339	The cumulative test cap is 1195 under `tests/` over that same complete PR diff.
   340	
   341	Report the implementation total, test total, script length and each schema's line count separately. An inherited check failure is reproduced against the unchanged base with the same command and environment and reported as a failure, never labelled passing or repaired outside scope. Local Bats tests remain unrun; GitHub Actions supplies their required results.
   342	
   343	The orchestrator runs the format-2 task-consistency checker before dispatch and at acceptance, covering C1 to C10, C7b, the required C11 selector grammar and C18's design-by-reference requirement. It records the checker version and actual coverage; a version lacking a check is not evidence that the check passed. Every `closed` row is checked against its single concrete selector, including the class name.
   344	
   345	The orchestrator performs the C-80 security-profile review of this task text and threat table before dispatch. Findings enter the class table and receive dispositions before a send. The orchestrator also performs the complete task-copy byte comparison and SHA256 check; these are not worker self-attestations.
   346	
   347	The final inventory confirms the split remains intact, identifies preserved a03 evidence, shows the a03 task-copy deletion and a04 replacement, and accounts for every new or modified path against the declared boundary.
   348	
   349	## Completion
   350	
   351	One branch, `tools/verdict-audit-pool-a01`, continues PR #410 from the named a03 head. The first push contains the C3 task-copy replacement. The implementation, tests and historical evidence remain; no new implementation PR, branch or repeated parking operation is created.
   352	
   353	The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's branch, reset boundary and live rules taking precedence, `dotfiles-T133-verdict-audit-pool-a05` as the advisory P2 owner, `task_copy=<sha256 of .orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md>` and `parked_pr=407` in the RESULT. The orchestrator writes the advisory owner task before assigning an advisory disposition and records owned findings under its matching acceptance-record section.
   354	
   355	There is one worker-side pre-push review round at most. Every worker fix round before or after the first RESULT counts toward INV-6 under C-61, including Bot-driven fixes. A pre-push fix followed by revise 1 exhausts the two-round allowance. Predecessor counters and stopped histories remain recorded; a reset does not erase them. A third finding of one class stops further rounds until the orchestrator records the required re-plan.
   356	
   357	A P0/P1 surviving the allowed fix round is sent as `open:<id>` in the RESULT, including review-body and local/security finding identifiers. It stops the PR for the operator's decision. It is neither silently deferred nor converted to not-applicable to permit another worker round or merge. The worker resolves no review thread.
   358	
   359	The report and RESULT identify head, base, branch, changed files, every feedback disposition, retained and added test names, code and test totals, schema counts, script length, task-copy hash, review-round counts and evidence paths. They distinguish historical evidence from final-head validation. Record actual Bot review events rather than inventing a re-review count.
   360	
   361	Expected worker artifacts are `.orchestration/dotfiles-T133-verdict-audit-pool-a04/report.md`, `validation.md`, `sandbox.md`, `learning.md` and `autoskill.md`; revision instructions and selectors are also recorded in `revise.yaml`. Worker review evidence uses the required `-worker-` infix. Artifacts are written at those relative paths in `worker-f`; the RESULT states their placement, and the orchestrator copies required evidence by absolute path. Plan, todo and learn worklogs remain uncommitted.
   362	
   363	This task is `security: true`. The orchestrator performs its final-head task-level audit and separate security-profile review before the integration gate. Final-head CI, the complete feedback sweep, dispositions, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive fresh required evidence. Only the orchestrator performs `gh pr merge --repo mryfmo/dotfiles --squash --match-head-commit <audited head>` after the gate. PR #410 is integrated manually.
   364	
   365	No `@codex review` comment is posted. Observe automatic review for the bounded window, read both review bodies and inline findings, and record absence after 15 minutes as `bot: none`. Wait for the required CI checks to pass before a ready-for-review RESULT. Any new push requires checking its CI again.
   366	
   367	Every worker `gh pr`, `gh run` and `gh issue` command supplies `--repo mryfmo/dotfiles` or the full pull-request URL, and every worker `gh api` command supplies an explicit `repos/mryfmo/dotfiles/…` endpoint path with no `--repo` flag or repository placeholder; each gh command, Git write, push and fetch is an individual command inside the sandbox, without shell chaining or a wrapper combining commands. No excluded command, unsandboxed retry, API substitution or browser path bypasses a live boundary. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-verdict-audit-pool-a04 status=blocked` naming the exact command, exit status, output and boundary; preserve the available artifacts and wait for the orchestrator to re-task.
   368	
   369	Until plan 024 P1-14 lands, strings containing `gh pr merge` or `gh pr create` are written through the file-edit tool, not shell commands, heredocs or shell wrappers. This writing rule grants no execution authority.
   370	
   371	Live dispatch, merge and local Bats are not exercised. No application path exists in this task; the shared-UID residual remains as stated in the design.
   372	
   373	## Checks (pasted by the orchestrator before each send)
   374	
   375	```
   376	(pasted at dispatch)
   377	```
exec
/bin/zsh -lc "sed -n '1,145p' .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md" in ~/Workspace/dotfiles
 succeeded in 99ms:
---
format: 2
task_id: dotfiles-T133-verdict-audit-pool-a04
kind: code
security: true
allowed_files:
  - scripts/orchestrator/verdict.sh
  - .schemas/verdict.json
  - .schemas/audit.json
  - tests/unit/test_verdict.py
  - .orchestration/dotfiles-T133-verdict-audit-pool-a04/**
after: [dotfiles-T133-worker-write-boundary-a01]
reset_of: [dotfiles-T133-verdict-audit-pool-a03]
threat_table:
  - control: "scripts/orchestrator/verdict.sh (nine conditions, trusted-parent startup, fixed executable identities, contained output and explicit security metadata)"
    disposition: "residual: the regression fixtures exercise the declared execution and write controls; these controls reduce accidental and prompt-injected execution but do not isolate hostile processes sharing the orchestrator's UID."
  - control: ".schemas/verdict.json (the accept, revise and hold contract)"
    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold"
  - control: ".schemas/audit.json (the audit contract and controlled class vocabulary)"
    disposition: "residual: schema rejection is exercised by the retained validator tests; the sibling owns the separate vocabulary file and its equality test."
  - control: "tests/unit/test_verdict.py (retained behavior cases and the reset-design regressions)"
    disposition: "residual: temporary repositories and fixed fixture executables expose arguments, marker writes and side effects; they do not establish host isolation or authenticate live GitHub state."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/** (this reset task's artifacts)"
    disposition: "residual: artifacts identify their commands, tested heads and provenance; historical a03 evidence remains distinguishable from a04 final-head results."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md (dispatched task copy)"
    disposition: "residual: the first push adds the byte-identical dispatched a04 text; the TASK and RESULT bind this copy's own SHA256, which the orchestrator compares independently."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md (predecessor task-copy deletion)"
    disposition: "residual: the first push deletes only this predecessor copy under the explicit reset-bookkeeping exception; other a03 evidence remains unchanged."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/report.md"
    disposition: "residual: the report distinguishes inherited evidence, new results and retained predecessor artifacts; a local record does not authenticate its author."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/validation.md"
    disposition: "residual: validation records commands, red results, final-head results and tested heads; pasted output does not authenticate its source."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/sandbox.md"
    disposition: "residual: the record identifies refused commands and the observed boundary without claiming isolation from unrestricted same-UID processes."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/learning.md"
    disposition: "residual: reusable learning remains separate from executable policy and from predecessor evidence."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/autoskill.md"
    disposition: "residual: the run status or not-used record grants no execution or promotion authority."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/revise.yaml"
    disposition: "residual: revision instructions and selectors remain data, bounded by this task's files, caps and round allowance."
  - control: "agmsg storage route (~/.agents/skills/agmsg/scripts/lib/storage.sh; no application path exists in this task)"
    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path"
  - control: "application integration gate (make require-crit-review; no application path exists in this task)"
    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path"
  - control: task metadata
    disposition: "residual: the orchestrator checks format-2 consistency before dispatch and at acceptance, validates security as an explicit boolean, and compares the complete dispatched task with its branch copy."
  - control: metadata separators
    disposition: "residual: the first opening and closing document separators bound safe-loaded YAML; the byte comparison also covers the body and subsequent separators."
  - control: in-process effects
    disposition: "residual: the Python child contains verdict and shadow writes; hold never appends a shadow row, and no application path exists in this task. --apply exits 2 with its named refusal; verdict never dispatches, calls the gate, executes agmsg code or merges."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: a trusted parent supplies the clean environment before any exec, startup checks refuse rather than repair, and internally fixed executable paths remove the caller-bin interface; shared-UID access to installations, credentials and host state remains outside the isolation these controls provide."
  - control: new or renamed scripts
    disposition: "residual: verdict.sh remains the only implementation executable introduced by this PR; no pool executable, caller wrapper, dependency or production test-override interface is added."
  - control: orchestrator effect merge
    disposition: "residual: only the orchestrator performs the live head-matched squash merge with --repo mryfmo/dotfiles after the prescribed evidence and integration gate; verdict has no application path."
  - control: orchestrator effect update-branch
    disposition: "residual: an update-branch changes the head and invalidates head-bound evidence; the orchestrator repeats required CI, feedback collection, audit and security review for the resulting head."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state."
  - control: "design 5.14 item 1 (worker write boundary)"
    disposition: "residual: the worker does not change its own execution boundary; Claude write isolation is not inferred from render-check, and the orchestrator verifies the deployed boundary separately."
  - control: "design 5.14 item 2 (sanitized environment before execution)"
    disposition: "residual: a trusted parent supplies the clean environment, including passwd-derived HOME, before exec; the program checks allowed names, its resolved script path and HOME and exits 2 on refusal without self re-exec. Privileged mode alone cannot prevent Linux loader execution; caller integration and shared-UID host execution remain separately assessed."
  - control: "design 5.14 item 3 (trusted path boundaries)"
    disposition: "residual: resolved executable and destination paths are checked against the declared trusted roots; a same-UID process outside a worker sandbox can still mutate host paths."
  - control: "design 5.14 item 4 (execute verified identities and consume verified contents)"
    disposition: "residual: executables run by verified realpath, consumed snapshots are rehashed immediately before use, and decision-input hashes enter the verdict; snapshots do not create a boundary against unrestricted same-UID mutation."
  - control: "design 5.14 item 5 (output and reservation identity)"
    disposition: "residual: verdict and evidence snapshot filenames and shadow rows use the full head; each audit, security, local-review and sweep input is also matched by its full-head metadata, and this verdict task introduces no reservation lock."
  - control: "design 5.14 item 6 (honest residuals)"
    disposition: "residual: startup, path and snapshot controls are reported as damage reduction; neither host isolation nor independent GitHub credentials is claimed."
  - control: "design 5.14 item 7 (verification)"
    disposition: "residual: this task supplies concrete regression selectors and final-head evidence; the shared trusted-execution test helper remains owned by P1-6 and is reused only if available without expanding this task's edit boundary."
  - control: "design 5.14 item 8 (committed approval ledger)"
    disposition: "residual: verdict evaluation supplies no permission approval; every gh call names mryfmo/dotfiles explicitly, and PR data comes from GitHub at one base/head pair captured once and recorded at full SHAs, never shared refs or objects. No application path exists in this task; shared credentials remain a residual."
  - control: "design 5.14 item 9 (private cache and absolute interpreter)"
    disposition: "residual: the shared trusted-interpreter resolver anchors the install root to the passwd home of the real uid, never HOME, and the anchored private uv cache excludes worktrees, worker-writable caches and temporary directories; until the P1-3 resolver is available, verdict holds without a private resolver or PATH fallback."
  - control: "design 5.14 item 10 (worker commands remain sandboxed)"
    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; a command that cannot complete there produces a blocked PONG rather than an escape or alternate execution route."
premises: []
---

# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a04 — INV-6 S1 re-plan of a03 (plan 024 P1-4a; PR #410)

Worker: a008, Claude Code, worktree `worker-f`.

This text is the independent redesign by a review-profile context other than the author of the predecessor task texts. The a03 pre-push fix round and revise 1 exhausted its C-61 allowance. The security review of `513e5d05` found caller-controlled executable selection and cached-bytecode execution; the review of `6b7e7833` found inherited `compgen` execution, acceptance of attacker-selected absolute symlink targets, uncontained output writes and an implicit non-security branch.

The a03 acceptance record contains three `env-trust-bypass` rows: `security:513e5d0:1`, `security:6b7e783:1` and `security:6b7e783:2`. Its recorded `re-plan:` line establishes INV-6 S1. Another a03 patch round is not authorized. This reset changes the execution contract so a trusted parent supplies the clean environment before exec, the program verifies and refuses without self re-exec, and no caller executable directory exists.

Read these records before implementation:

- `.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md`
- `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md`
- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md`
- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md`

The design at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, section 5.14, applies by reference, including today's amendments to items 2, 8 and 9 and items 4 and 5. This absolute path identifies the orchestrator's uncommitted working copy under C-86. The task does not claim that section is already on `origin/main`.

The sentences of section 5.14 this task relies on are quoted here verbatim (C-88: the quoted sentences are normative; the path above is context, and the design file is uncommitted at authoring time):

> 2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.

> 4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。

> 5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。

> 8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder: the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged.

> 9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record.


Host controls reduce accidents and prompt-injected damage. They do not isolate unrestricted processes sharing one UID. The design's GitHub prevention boundary is also not established while worker and orchestrator credentials remain accessible to that same UID; subsequent boundary-record checks provide detection as the design states.

## Branch and reset boundary

Continue `tools/verdict-audit-pool-a01`, PR #410, from `6b7e7833a85528440dc397c2555bc9dd603c685a`, already update-branched onto main `3f240b12`. Keep the a03 implementation, regression coverage and evidence. Create neither another implementation branch nor another PR.

The first push deletes `.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md` and adds the dispatched text byte-for-byte at `.orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md`. This single predecessor-copy deletion is the explicit reset-bookkeeping exception to `allowed_files`. Other a03 evidence remains unchanged under its original task identifier and tested heads.

The orchestrator retains the a03 acceptance history, class rows, stopped status and counters. The final inventory identifies preserved a03 evidence separately from a04 additions; preservation does not authorize further worker edits in the a03 directory. The a01/a02 artifact removals already completed by a03 are not repeated or reversed.

The split remains intact. The pool sibling owns `scripts/orchestrator/audit-pool.sh`, changes to `scripts/orchestrator/orch-audit.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py`. `audit-pool.sh` is absent at `6b7e7833`; the audit schema at that head is `.schemas/audit.json`. Neither fact authorizes recreating a split file or adding a `schemas/` mirror. PR #407 remains parked; its parking operation is not repeated.

## Goal

Produce one schema-valid verdict from nine positively checked conditions without executing inherited shell startup code, accepting caller-selected executable directories, following output symlinks or treating invalid `security` metadata as an exemption.

Retain complete feedback validation, amended-cap precedence, offline operation and finding counts. This task computes and records shadow verdicts only; `--apply` is rejected as item 6 specifies.

## Files

1. `scripts/orchestrator/verdict.sh <pr> [--loop] [--shadow]` remains Bash with `set -Eeuo pipefail`, English shdoc documentation and `jq` for JSON. Its startup and executable selection follow the Reset design below. Each condition is `{id, ok, evidence}` and becomes true only through a positive check of parsed, validated input.

   Inputs remain the PR view and checks, the acceptance record's JSON block and prose, the selected task or `--task <id>`, the audit JSON, a fresh feedback sweep, saved feedback dispositions, the task's allowed paths and caps, regime counters, the GitHub merge-base changeset and the head-specific security review. The acceptance block names the PR, task and current head and contains a ledger array. The PR is open, non-draft and based on `main`. At the start of each PR evaluation, capture `head.sha` and `base.sha` together once from `gh api repos/mryfmo/dotfiles/pulls/<pr>` as `head40` and `base40`, require both to be 40 lowercase hexadecimal characters, and bind all reads to that pair. Record both in the verdict JSON as `head` and `base`. The compare listing and file contents are read from GitHub at that captured pair; no separate current-main read replaces either value. If a second PR read is needed, compare both SHAs with the captured pair and refuse with hold, exit 20 and `verdict: PR base/head changed during evaluation` if either differs; append no shadow row and never combine reads from different pairs. This task chooses GitHub API reads, not a local clone: read the changeset through `…/compare/<base40>...<head40>` and inspected PR bytes through `…/contents/<path>?ref=<head40>`. Repository identity is fixed to `mryfmo/dotfiles` from the trusted repository declaration, not caller environment or local Git configuration. Every `gh pr`, `gh run` and `gh issue` invocation supplies `--repo mryfmo/dotfiles` or the full pull-request URL; every `gh api` invocation, including instantiated API templates in the design quotation, uses an explicit `repos/mryfmo/dotfiles/…` endpoint path, never `--repo` or a `{owner}/{repo}` placeholder. A matching head SHA in a fork is not a repository binding. Missing, incomplete, truncated or unreadable API data holds; no local-head fetch or shared-object fallback is allowed.

   Condition 1 verifies that the GitHub contents response for `.orchestration/<task>/precheck.json?ref=<head40>` hashes to the record's `precheck:` value and names the head or an ancestor authenticated by GitHub compare data whose diff to the head contains only `.orchestration/<task>/` paths. The retained `PRECHECK_REQUIRED` setting is supplied explicitly as `--precheck-required 0|1`; absent or zero makes this condition's failure a warning. No environment exception is added for it.

   Condition 2 requires every required check to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Every duplicate entry for a required name must also be `SUCCESS`.

   Condition 3 requires an audit that validates against `.schemas/audit.json`, names the task and full head, has zero open P0/P1 findings, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit without remaining findings fails this condition.

   Condition 4 requires saved and fresh feedback documents to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Diagnostic URLs do not determine the result.


exec
/bin/zsh -lc "rg -n -A 30 -B 2 'Codex seat worklogs' ~/.agents/skills/agmsg-orchestration/SKILL.md" in ~/Workspace/dotfiles
 succeeded in 147ms:
215-    - Apart from those surviving P0/P1 items, the RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>` under Orchestrator Playbook step 10. The worker resolves no thread.
216-
217:## Codex seat worklogs
218-
219-Project layouts vary by language. Set up this worklog structure only when it
220-does not already exist, and use timestamped filenames in `YYYYMMDD_HHMMSS`
221-form:
222-
223-- `.agents/worklog/codex/plan/<timestamp>_plan.md` stores the plan and design
224-  written before implementation. Ask the user questions when needed, and
225-  update the plan when questions, learning, or completed tasks change it. It
226-  must contain `Goal`, `Scope`, `Assumptions`, `Design`, `Tests`, and
227-  `Open Questions`.
228-- `.agents/worklog/codex/todo/<timestamp>_todo.md` derives its tasks from the
229-  plan. Move completed items from `TODO` to `Done`; when `TODO` is empty, set
230-  its status to `done` and rename it to `<timestamp>_done.md`. It must contain
231-  `TODO` and `Done`.
232-- `.agents/worklog/codex/learn/<timestamp>_learn.md` records only reusable,
233-  validated knowledge that speeds a future decision. State what was learned
234-  and where it applies, update the plan's `Assumptions`, `Design`, or `Tests`
235-  when relevant. A learn file must contain `Date`, `Learnings`, and
236-  `Plan Updates`.
237-
238-Every plan, todo, and learn file starts with YAML frontmatter containing
239-`type` (`plan`, `todo`, or `learn`), `id` (`YYYYMMDD_HHMMSS`), `owner` (for
240-example, `codex-a`), and ISO8601 `created_at` and `updated_at`. Additionally:
241-
242-- todo requires `status`, `workstream`, and `related_plan`; status is one of
243-  `active`, `blocked`, `done`, or `superseded`;
244-- plan requires `status`, one of `draft`, `active`, `done`, or `superseded`;
245-- learn requires `validated` (`true` or `false`) and `apply_to` (plan/tests),
246-  and may be created only when reusable and validated.
247-

exec
/bin/zsh -lc 'cat ~/.codex/plugins/cache/ponytail/ponytail/5.3.2/skills/ponytail/SKILL.md' in ~/Workspace/dotfiles
 succeeded in 34ms:
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

**Estimating budget allocation**
codex
Ponytail と agmsg-orchestration の worklog 規則を確認しました。今回は読み取り専用なので記録ファイルは作成しません。まず、既知の same-UID residual と、それとは別に修正が必要な実行経路の穴を切り分けます。
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md | sed -n '140,257p'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'git status --short; git rev-parse HEAD; command -v crit; print -r -- "$PATH"' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'ls -l .ua/knowledge-graph.json .ua/meta.json' in ~/Workspace/dotfiles
 succeeded in 140ms:
   140	   Condition 2 requires every required check to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Every duplicate entry for a required name must also be `SUCCESS`.
   141	
   142	   Condition 3 requires an audit that validates against `.schemas/audit.json`, names the task and full head, has zero open P0/P1 findings, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit without remaining findings fails this condition.
   143	
   144	   Condition 4 requires saved and fresh feedback documents to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Diagnostic URLs do not determine the result.
   145	
   146	   Condition 5 requires every path in the base-to-head diff to match an `allowed_files` entry and additions-plus-deletions totals to remain within the effective Check caps. The comparison is `gh api repos/mryfmo/dotfiles/compare/<base40>...<head40>` using the PR API's base and head, and its full `merge_base_commit.sha` identifies the merge base. Consume the complete authenticated file list and its additions/deletions; account for both names of a rename. An unreadable merge base or incomplete changeset holds. The main checkout's `.git`, including `origin/main`, replacement refs and objects, is not an evidence source. Backticked exclusions after `outside` leave the outside count; default exclusions remain `tests/` and `.orchestration/`. Item 7 retains amendment precedence.
   147	
   148	   Condition 6 reads one orchestrator-pasted INV-6 counters block in the acceptance record, bound there to this task, PR and full head. This task chooses the pasted record rather than a live store query so verdict executes no agmsg shell code and cannot follow worker-writable `drivers.partition`. It never invokes `scripts/regime-counters.sh` or sources the agmsg storage layer. No `S1:` line is present and the parsed decimal `revises` value is below 2. A missing ledger or counters block, duplicate block, mismatched binding or unreadable count holds; an absent count is never zero.
   149	
   150	   Condition 7 requires the numeric count of open P0/P1 findings to be zero. Findings with status `new`, `still-open` or absent count as open regardless of identifier or scope.
   151	
   152	   Condition 8 first validates `security` as an explicit boolean. Only boolean `false` permits the non-security branch. Boolean `true` requires the security review's front-matter `head:` to equal the verdict's own full 40-hex head and its last non-blank line to be `Verdict: correct`. A sha7 filename is never a head match. Missing, null or non-boolean metadata holds with the named reason specified below.
   153	
   154	   Condition 9 requires at least one `sha256:<hex> <path>` line in the acceptance record's prose and verifies every such line against its file. Every inspected evidence file, including audit, security, local review and saved or fresh sweep, is named with and matched against the verdict's full 40-hex head: Markdown uses front-matter `head:`, audit and local-review JSON use `head` (on every record for a JSON list), and feedback JSON uses `head_sha`. Missing, invalid or different full-head metadata holds even when a filename or sha7 prefix matches. Hashes preserve consumed bytes; they do not authenticate a local Git object or ref.
   155	
   156	   All nine conditions passing produces `accept`. Failure of condition 6 or 7, missing or unreadable input, schema-invalid input, invalid security metadata or an internal evaluation error produces `hold`. Other failed conditions produce `revise`. The revise line remains `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies `check=` selectors.
   157	
   158	   The generated verdict is `.orchestration/validation/<task>-verdict-<head>.json`, using the full 40-character head under design 5.14 item 5. Its fields are `verdict`, `pr`, `head`, `base`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`, validated against `.schemas/verdict.json`. Audit, security, local-review and sweep inputs use full-head-named verified snapshots with the metadata bindings above. External producers are not edited; the orchestrator supplies the full-head-named evidence and required metadata before evaluation, retaining original artifacts separately. Historical verdict files remain untouched.
   159	
   160	   Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with internal error treated as hold. A destination or post-startup execution-boundary refusal holds with exit 20; the mandatory startup refusals in Reset design item 1 exit 2 with their named messages. Refusal before a usable task or head exists reports hold without inventing an output identity.
   161	
   162	   `--apply` is unsupported and exits 2 with `verdict: --apply is not supported in this shadow-only task` before input reads or tool calls other than mandatory startup verification. No application branch, dispatch, gate call, agmsg execution or merge remains. Arguments containing `--admin` or `--auto` anywhere are refused with exit 2 before input reads or tool calls other than mandatory startup verification.
   163	
   164	   Shadow evaluation is the default; `--shadow` is its explicit spelling. It writes the verdict JSON and, only for a non-hold verdict, appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`. Columns remain `pr`, `head`, `machine`, `human`, `agree` and `at`; the orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing, invokes no dispatch, gate or agmsg code, and treats no gate conclusion as binding.
   165	
   166	   `--loop` retains PR-number order, eligible open non-draft PRs on `main`, and an acceptance record naming each current head. Each recursive verdict invocation uses the sanitized program-entry contract and captures that PR's single base/head pair at its start as above. The loop computes and records shadow verdicts only; it never refreshes a checkout, dispatches, calls the gate, executes agmsg code or merges. Evaluation never uses the main checkout's shared refs or objects.
   167	
   168	2. `.schemas/verdict.json` and `.schemas/audit.json` remain JSON Schema 2020-12 documents with `additionalProperties: false` at the top level and in defined item objects.
   169	
   170	   The audit contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and optional `status`. The controlled class enum retains the vocabulary snapshot at `b8998de162afc72d53d07679b8f0a194fcc480ff`.
   171	
   172	   The existing stdlib schema validator remains available through `--validate` under the fixed isolated interpreter, without a new helper file or dependency. Required keys, types, enums, bounds, SHA patterns, additional-property restrictions and RFC 3339 timestamps with offsets remain checked. Date-only values, naive timestamps and invalid calendar dates fail. Runtime validation does not depend on the sibling's `orch-audit.sh --validate`.
   173	
   174	3. The retained interpreter-selection requirement is implemented through Reset design item 2 rather than the a03 caller-bin mechanism.
   175	
   176	   Before PR input processing, the trusted entrypoint fixes absolute executable identities and the offline PyYAML environment. Checkout `.python-version`, `.venv`, executable files, uv configuration, mise configuration and inherited tool-selection variables cannot select an interpreter or tool. Missing trusted installations or unavailable offline dependencies hold before evaluation.
   177	
   178	   The historical interpreter regression against `85a472294d0c10835bd7235e3c76d045846a6ed9` remains identified as historical. Its marker-writing interpreter cases run again against the final implementation.
   179	
   180	4. The a02 and a03 finding-count and feedback fixes remain acceptance requirements.
   181	
   182	   Conditions 3 and 7 count open P0/P1 findings numerically. Empty identifiers and records scope cannot hide a finding.
   183	
   184	   Condition 4 requires both saved and fresh `head_sha` values to equal the accepted head. Missing or invalid dispositions are counted before formatting URLs; null and empty URLs affect diagnostics only.
   185	
   186	   Complete identity and multiplicity retain the trusted helper's `feedback_key()` and `missing_feedback()` behavior. Source, URL, level, path, line, body and author participate, with only existing exact masked-body and masked-path equivalence. One saved occurrence covers one fresh occurrence.
   187	
   188	   Dispositions retain `parse_disposition()` validation and `commit_in_range()` semantics, but verdict checks commit membership through complete GitHub compare/commit data instead of calling the helper's local-Git range check. A fix commit exists within the authenticated base-to-head range. A not-applicable disposition has a non-empty reason and evidence command and satisfies existing level-specific reason requirements. Evidence commands remain data and are never executed.
   189	
   190	   Neither `scripts/require-crit-review.py` nor its validator is edited. Shadow evaluation never calls the gate or treats its conclusions as binding. Retained red evidence keeps its original head; final-head green results are new evidence.
   191	
   192	5. `tests/unit/test_verdict.py` retains the sixteen shadow behavior tests at `6b7e7833`, including schema-rule rejection, offline PyYAML refusal, numeric finding counts, feedback head binding, null diagnostic URLs, identity and multiplicity, disposition validation, amended caps and cached-bytecode refusal. Delete the three application, gate-order and post-merge checkout-refresh tests and their application-only fixtures; retain the `--admin` and `--auto` refusal controls in the no-application-path regression below.
   193	
   194	   The a03 test named `test_verdict_ignores_caller_bin_and_path_overrides` retains its coverage of hostile PATH selection while its removed executable-directory fixture is replaced by the fixed-entrypoint fixture: direct dirty invocations refuse, and trusted-parent clean invocations preserve the verdict without executing planted tools. Neither the script nor the test source retains `VERDICT_BIN` or another production executable-directory override.
   195	
   196	   Existing shadow positive and negative controls remain: empty checks, failed duplicate checks, blocked audits, incorrect audits without findings, missing ledgers and records, unavailable GitHub heads, unreadable GitHub merge bases, backticked cap exclusions and absent evidence hashes.
   197	
   198	   Fixtures use temporary repositories and fake external tools whose absolute identities are established in the fixture's trusted entrypoint before invocation. They do not reintroduce caller PATH discovery or a production test-only override. The actual Python used for valid execution satisfies the interpreter boundary. All fixture lines count toward the test cap.
   199	
   200	6. No application path exists in this task.
   201	
   202	   Remove application code, prerequisite-ledger reads, agmsg installation checks and their tests. `verdict.sh` never dispatches, calls the gate, executes agmsg code or merges, including in `--loop`. It computes and records only the shadow verdict JSON and non-hold TSV row described in item 1. Passing `--apply` exits 2 with `verdict: --apply is not supported in this shadow-only task` before input reads or tool calls other than mandatory startup verification; no verdict or shadow row is written for that usage refusal.
   203	
   204	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path` covers default, `--shadow` and `--loop` evaluation and unsupported `--apply`, including `--loop --apply`. Shadow evaluations record the schema-valid JSON with full `head` and `base` and append only the machine TSV columns for non-hold verdicts. Marker-writing gate, dispatch, history and agmsg fixtures remain untouched and no merge occurs. The `--apply` cases require the named message, exit 2, no PR or prerequisite reads and no output writes. The retained `--admin` and `--auto` controls still refuse before input reads or effect calls.
   205	
   206	7. The retained cap-parser fix remains enforced.
   207	
   208	   The last applicable cap declaration in text order governs, including its exclusions and outside limit. A later test-only amendment changes the test limit while retaining the outside limit.
   209	
   210	   `test_verdict_condition_5_honors_the_latest_amended_caps` retains the original 500 versus amended 550 case with 531 changed test lines, the actual a02 test-only wording, a later lower limit, changed exclusions and changed outside limit. Unrelated conditions stay green and evidence hashes are refreshed. Its original red head remains historical.
   211	
   212	The required check names remain `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.
   213	
   214	## Reset design
   215	
   216	1. **A trusted parent supplies the clean environment before exec; startup verifies and refuses.**
   217	
   218	   `verdict.sh` has mode 0755 and shebang `#!/bin/bash -p`. A trusted parent invokes it with `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …`, with long Bash options before `-p`. The parent supplies a clean environment before any exec, including the exec of `/usr/bin/env` itself; launching that prefix with inherited loader variables is not sanitization before the loader. Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but does not enable the loader’s secure-execution mode. On Linux, inherited `LD_PRELOAD` or `LD_AUDIT` can execute before Bash’s first statement. There is no self re-exec and no reopening of caller-controlled `$0`.
   219	
   220	   Before `set`, traps, argument processing or executable discovery, the first executable compound statement verifies privileged mode, the startup environment, the script path and HOME. A missing privileged mode refuses with exit 2 and `verdict: execute as a program`. Check environment names through absolute `/usr/bin/env` and `/usr/bin/grep`; exactly `PATH`, `HOME`, `LANG`, `PWD`, `SHLVL` and `_` are allowed, with fixed `PATH=/usr/bin:/bin` and `LANG=C.UTF-8`. An extra/missing name or wrong fixed value refuses with exit 2 and `verdict: untrusted startup environment`. A caller-set sentinel proves nothing and is not accepted.
   221	
   222	   Resolve `$0` with the fixed absolute realpath utility and require an absolute invocation path whose realpath is a regular file under the anchored repository root; otherwise exit 2 with `verdict: untrusted script path`. Resolve the real uid through absolute `/usr/bin/id -ru` and obtain its passwd home through `/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS (the user is resolved from that real uid), or `/usr/bin/getent passwd <uid>` on Linux. Missing, ambiguous or unreadable account data, or HOME unequal to that passwd home, exits 2 with `verdict: HOME does not match passwd home`. The repository root and passwd-home lookup do not derive from caller HOME, PWD or local Git configuration. Refuse instead of repairing any failed check. No `compgen`, `unset -f` loop or PATH edit serves as the startup boundary.
   223	
   224	   Every ordinary caller, including the loop child and test helpers, is the trusted parent for that exec and uses the exact clean prefix with the passwd home and absolute script path; no sentinel is exported or trusted. The retained `PRECHECK_REQUIRED` control is passed as the explicit `--precheck-required 0|1` argument when needed, defaults to 0, and is never inherited or retained as an environment name.
   225	
   226	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_program_discards_hostile_startup_environment` executes the program with exported functions named `compgen`, `[`, `test`, `exec`, `command`, `builtin` and `command_not_found_handle`, a marker-writing `BASH_ENV`, `LD_PRELOAD` and `LD_AUDIT` naming marker-library paths, a forged HOME containing a marker-writing interpreter, and a planted PATH. The fixture also supplies the other startup selectors discarded by privileged mode. The direct dirty invocation must exit 2 with `verdict: untrusted startup environment` and no marker; it must not repair or re-exec. The direct dirty cases use deliberately non-loadable library paths: a loadable constructor cannot be prevented after a dirty exec. Exercise a loadable marker library only through the already-trusted parent supplying the clean environment before every exec, and require no marker. The clean prefix must yield the unchanged clean verdict and conditions, so an incidental exit 2 cannot pass the positive control.
   227	
   228	   Separate subcases exercise each named refusal: a forged HOME with otherwise allowed names and fixed values, a symlinked `$0` resolving outside the repository, and `VERDICT_SANITIZED=1` together with `GIT_CONFIG_GLOBAL`, `GIT_DIR` and `GIT_INDEX_FILE` pointing to planted files. Require the appropriate named message, exit 2, no marker or application effect and no consumption of planted configuration, objects or index. Check the clean child’s allowed-name-only environment and passwd-derived HOME. Exercise the exact long-options-before-`-p` command.
   229	
   230	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_bash_file_invocation` invokes `bash scripts/orchestrator/verdict.sh …` in a clean fixture and requires exit 2 and the named message. This negative invocation is the sole deliberate plain non-privileged Bash verdict call in the tests.
   231	
   232	2. **Executable identities are fixed at the trusted entrypoint.**
   233	
   234	   No caller-supplied executable directory exists. Remove `VERDICT_BIN`, its environment whitelist, symlink-directory acceptance and every equivalent caller override from the script and fixtures. Do not replace them with a differently named environment variable or CLI option.
   235	
   236	   The trusted entrypoint fixes the absolute paths for Bash, uv, Python, gh, git, jq and required utilities before reading PR-controlled input. It executes verified realpaths without rediscovery. The repository's Python declaration is a read-only input; consume `scripts/orchestrator/trusted-interpreter.sh` from the authenticated trusted base when present. The P1-3 resolver alone resolves the pinned declaration to a regular executable file under the tool manager's install root, anchored to the passwd home of the real uid, never to HOME, and outside worktrees, worker-writable caches and `$TMPDIR`. A symlink spelling alone authenticates nothing. An absent resolver or invalid trusted installation holds rather than selecting another interpreter from PATH, mise, uv discovery or a checkout. No private resolver, `command -v` or `mise which` fallback is retained here. Implementation may proceed before `dotfiles-T133-ci-efficiency-followup-a04` lands by implementing and testing this unavailable-resolver hold with a trusted resolver fixture for successful cases; live execution stays on hold until that lineage supplies the resolver. This task therefore does not need the resolver at implementation time and adds no P1-3 `after:` dependency.
   237	
   238	   Design 5.14 items 2, 4 and 9 apply by reference to Git invocation, executable paths, verified snapshots and private cache use. The uv invocation is `uv run --no-config --no-project --offline --python <abs>`, with uv itself an internally fixed absolute executable and `<abs>` the validated interpreter realpath. `UV_CACHE_DIR` is the anchored private cache from the design. Worker-shared uv or mise caches supply no executable. Python children use `-I`; the a03 `-B`, `sys.dont_write_bytecode` and refusal of checkout bytecode that helper imports could consume remain enforced.
   239	
   240	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_uses_only_declared_absolute_executables` verifies fixed tool identities, refusal of hostile PATH and inherited interpreter selectors, and unchanged clean-prefix execution, including an absolute symlink to a marker-writing interpreter and a forged HOME install tree that cannot become the trusted install root.
   241	
   242	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_interpreters_in_worktrees_caches_or_tmp` covers each excluded root, a non-regular target, a forged-HOME install root and a valid regular-file control under the passwd-home-anchored install root.
   243	
   244	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_executes_verified_snapshots_and_records_input_hashes` changes a validated source or input before consumption and verifies refusal or consumption of the verified snapshot, never the substituted contents, and checks the recorded input hashes.
   245	
   246	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_without_the_shared_trusted_interpreter_resolver` verifies the interim hold and absence of interpreter discovery or application effects.
   247	
   248	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_reads_pasted_counters_without_sourcing_agmsg` plants a marker-writing agmsg driver and counter executable, supplies the valid pasted counters, and requires unchanged verdicts with no marker; missing, duplicate, mismatched and unreadable counter cases hold.
   249	
   250	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_ignores_replaced_local_objects_and_refs` serves forged PR bytes through a replaced local object and forged `origin/main`, while fixed GitHub fixtures return the authentic full-head changeset and contents. It requires the clean verdict and authenticated input hashes, no local-object evidence read, and hold on incomplete API data rather than a local fallback. Cover precheck ancestry, fix-commit membership and loop shadow evaluation through the same GitHub fixtures.
   251	
   252	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_names_the_repository_on_every_gh_call` runs with a fixed fake gh that records every argument vector and asserts `--repo mryfmo/dotfiles` on every `gh pr`/`gh run`/`gh issue` call and an endpoint path beginning with `repos/mryfmo/dotfiles/` on every `gh api` call, with no `--repo` flag or repository placeholder on API calls. It covers PR view/checks, API and feedback reads and loop shadow evaluation in PR-number order. A fork fixture containing the same head SHA cannot redirect a call.
   253	
   254	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_a_changed_pr_base_or_head` supplies one initial GitHub `base40`/`head40` pair and differing SHAs on a required second read. Separate subcases change only the base, only the head and both. Each requires the named pair-change refusal, hold with exit 20 and no shadow row; the unchanged-pair control records both full SHAs and proves every compare listing and contents request uses the captured pair.
   255	
   256	   The retained `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` and `test_verdict_never_imports_cached_bytecode` remain green. Unavailable offline PyYAML still holds with no online fallback.
   257	

 succeeded in 241ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-verdict-audit-pool-a03 round=1 reset_of=dotfiles-T133-verdict-audit-pool-a02 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md task_sha256=2f0493944badef8294dc691e87fba7ab6cc84ed2d6e135454a34b1219f724c42 deadline=none done_signal=AGMSG-RESULT note=a008:the-verdict-half-of-the-P1-4a-split(verdict.sh,the-two-JSON-schemas,test_verdict.py)"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 410,
  "searches": [],
  "task": "dotfiles-T133-verdict-audit-pool-a03"
}
---

# Acceptance record: dotfiles-T133-verdict-audit-pool-a03

The verdict half of the P1-4a split (the a02 record holds the S2 decision): `verdict.sh`, `.schemas/verdict.json`, `.schemas/audit.json` and `tests/unit/test_verdict.py` stay on PR #410's branch from b8998de1; the pool files move to `dotfiles-T133-audit-pool-a01` (a009). Redesigned by a review-profile context (`.agents/worklog/orchestrator-glue/redesign/vap-a03.md`, file A). Seat: a008 (worker-f, Claude), fetching the branch, after its F1 owner RESULT. Owner of advisory P2: `dotfiles-T133-verdict-audit-pool-followup-a01` (its after now names both split tasks).

- 2026-10-19T00:4xZ: `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a008 (the line above; the full note is in the bus history). In-flight file check (C-78): verdict.sh, the two schemas and test_verdict.py appear in no other in-flight task (the pool task owns the other four files).
- 2026-10-19T02:53:51Z: RESULT round 1 from a008: PR #410 head 1bf64c949a1d5cdde918448f2c64f2fd470007a4 (code head 8b0b5bb4, previous b8998de1) on 3e41e36a, branch `tools/verdict-audit-pool-a01`; `task_copy=2f049394…` (the dispatched sha); the split commit 0e16d7eb (the a02 copy deleted, the a03 copy added, audit-pool.sh/classes.yaml/test_audit_pool.py removed, orch-audit.sh = origin/main); inventory outside .orchestration: verdict.sh, .schemas/verdict.json, .schemas/audit.json, test_verdict.py; item 6: `--apply` holds (exit 20) unless the trusted orch-gate.sh exits 0 (`test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure`); item 7: caps from the last declaration (`test_verdict_condition_5_honors_the_latest_amended_caps`); red at b8998de1, green 17/17 at 8b0b5bb4; the checker moved into verdict.sh `--validate` with a 35-case equivalence (0 disagreements); worker review 1 round (P2 fixed, 10/10 mutants killed); caps 298/300 and 393/400; shellcheck/shfmt clean; make format and make unit-test inherited failures (same at base); shadow hold exit 20; CI 7 required pass; the optional regime check fails on the stale base (the P1-11 defect, #425); Bot none; a01/a02 record directories (17 files) left for the orchestrator's reset bookkeeping. `status=pending-integration` sent 02:5xZ; chain after #425.
- 2026-10-19T02:58:31Z: C-80 review of the audit-pool-a01 text (`.orchestration/validation/dotfiles-T133-audit-pool-a01-text-security.md`): `Verdict: incorrect`, six P1 and four P2 (mise-shim resolution; GIT_* inheritance; tracked-and-unchanged checks before execution through mutable paths; previous evidence not frozen; symlink redirects of worktree and output paths; the queue lock replaceable; the shadow TSV rows not bound to outputs; shared physical slots across queues; 7-char head names collide; the closure test reads only the JSON ledger). The third text with the same class in one morning → design section 5.14 (D-024-18) written; a01 is withdrawn from a009's queue before it started, and a02 (the a01 text with 5.14 applied and the ten findings as items) is redesigned for a008.
- 2026-10-19T03:08:50Z: the audit-pool-a02 text (review profile, prompt `pool-a02-redesign-prompt.md`; design 5.14 applied by reference with one row per item; the ten C-80 findings as items) installed as `.orchestration/tasks/dotfiles-T133-audit-pool-a02.md`; checker OK; its C-80 review started 03:09Z; dispatch to a008 on `Verdict: correct`.
- 2026-10-19T03:13:23Z: C-80 review of the audit-pool-a02 text: `Verdict: incorrect`, three P1 and one P2: the write boundary is not established before P1-15 (render-check verifies equality, not isolation); D-024-17 pending; git repository-local configuration and .gitattributes (external diff, textconv, filters) still influence the audited diff; rows for 5.14 items 8-10 missing. By D-024-20 the text is sequenced `after: [dotfiles-T133-worker-write-boundary-a01]`; design 5.14 item 2 gains `--no-ext-diff --no-textconv -c core.attributesFile=/dev/null -c core.sshCommand=false`, item 7 requires one row per item 1-10; the text's next revision (rows 8-10, the git flags, P1-15 as a merged control) is batched with the a05 and dispositions-a02 revisions once the P1-15 text passes C-80.
- 2026-10-19T05:34Z: the security review of the update-branch head 513e5d05 (`…-security-513e5d0.md`): two P1 (verdict.sh:36 a caller VERDICT_BIN/PATH bypasses env -i; :168 the dynamic import can execute scripts/__pycache__ bytecode the guard excludes) and one P2 (17 predecessor artifacts of the a01/a02 directories remain in the PR tree). Counters (`--pr 410`): tasks=1 amendments=0 results=1 revises=0. Decision: revise 1 to a008 05:35Z (trusted-root resolution only, python -I -B with a __pycache__ refusal, the predecessor directories deleted from the branch); C-61: the pre-push round plus this one is the cap.
- 2026-10-19T06:29:47Z: a008 RESULT revise 1: head 934457c9 (code head 7c24617e; 3-case VERDICT_BIN/PATH test, no cached bytecode, red at 513e5d05 then 19/19, 5/5 mutants). Update-branched onto main 3f240b12 at 06:46Z → 6b7e7833 (CI 7/7 required green by 07:1xZ).
- 2026-10-19T06:59Z: the security review of 6b7e7833 (`…-security-6b7e783.md`): `Verdict: incorrect`: P1 verdict.sh:33 `compgen` runs before the inherited functions are removed, so an exported function named compgen executes before sanitization (probe confirmed); P1 :40 a caller-supplied VERDICT_BIN whose entries are absolute symlinks passes as trusted without authenticating the targets; P2 :271 the shadow log follows an unchecked symlink and appends on `hold`, and the JSON redirection at :268 has no destination containment; P2 :231 a missing, null or malformed `security` value selects 'not a security task' instead of holding. Class table: the 05:34Z rows security:513e5d0:1 env-trust-bypass (VERDICT_BIN/PATH), :2 interpreter-input-trust (__pycache__); today's :1 and :2 are env-trust-bypass again → 3 rows of one class: INV-6 S1. Counters (`--pr 410`): results=2 revises=1 (revise 1 was the C-61 cap). Root cause: the a03 design sanitizes the environment from inside a bash process that already started under the untrusted environment (functions, BASH_ENV, PATH, a caller-chosen bin dir), so every statement before the cleanup, and the cleanup itself, runs under attacker-controlled names; patches moved the gap (05:34Z PATH → 06:59Z compgen and symlinks). Proper state (design 5.14 item 2, amended today): sanitization happens before the first statement, by the invocation (`#!/bin/bash -p` executed as a program, then a self re-exec under `/usr/bin/env -i` with a fixed PATH), no caller-supplied executable directory at all, writes opened with O_NOFOLLOW inside the repository, `security` validated as an explicit boolean. Decision: re-plan; the lineage resets as verdict-audit-pool-a04 on the same branch from 6b7e7833 (redesign by the review-profile context, prompt `v-a04-redesign-prompt.md`); a008 holds (PING 07:2xZ, no fix). Dispatch of a04 follows D-024-20 (see the decision text pasted in the a04 record).
security:513e5d0:1	env-trust-bypass
security:513e5d0:2	interpreter-input-trust
security:6b7e783:1	env-trust-bypass
security:6b7e783:2	env-trust-bypass
security:6b7e783:3	write-containment
security:6b7e783:4	default-deny-gap
re-plan: env-trust-bypass (3 rows: security:513e5d0:1, security:6b7e783:1, security:6b7e783:2) — specification: the a03 text let the script sanitize itself and accept a caller bin dir; design: 5.14 item 2 gains the program-execution rule (bash -p, env -i re-exec, no caller executable directory); implementation: a04 reset on the same branch; verification: one test executes the program under exported functions named compgen, [, test, exec and command_not_found_handle plus BASH_ENV and a planted PATH and asserts none ran.
- 2026-10-19T07:24:23Z: a008 `status=holding`: PING read; no fix, no push; the #410 branch left at 934457c9 in worker-f (the remote head is the update-branch 6b7e7833); waiting for the reviewed a04 TASK.

 succeeded in 361ms:
Found four issues in [PR #410](https://github.com/mryfmo/dotfiles/pull/410), at head `6b7e7833a85528440dc397c2555bc9dd603c685a`.

1. **P1 · high confidence · `scripts/orchestrator/verdict.sh:33`** — The cleanup invokes `compgen` before removing inherited functions, so an exported function named `compgen` executes with the operator’s authority before sanitization. A read-only probe confirmed execution.

2. **P1 · high confidence · `scripts/orchestrator/verdict.sh:40`** — A caller-supplied `VERDICT_BIN` containing absolute symlinks, together with the permitted environment and matching `PATH`, passes as trusted without authenticating the targets; a symlink to an attacker’s interpreter is accepted. The regression tests cover a copied executable and an environment forcing reconstruction, but omit this clean-environment/symlink combination.

3. **P2 · high confidence · `scripts/orchestrator/verdict.sh:271`** — Shadow logging follows an unchecked `.orchestration/validation/verdict-shadow.tsv` symlink and appends even when the verdict is `hold`, allowing a PR-controlled link to corrupt an operator-writable file outside the repository. The JSON output redirection at line 268 likewise lacks destination containment checks.

4. **P2 · high confidence · `scripts/orchestrator/verdict.sh:231`** — Missing, null, or malformed `security` values select “not a security task,” bypassing the security-review requirement instead of holding; isolated probes confirmed missing and null values pass condition 8. Only an explicitly validated boolean `false` should permit this exemption.

The threat-table assessment, using its rows in declaration order:

| Rows / controls | Assessment |
|---|---|
| 1 — verdict implementation; 4 — regression fixtures | Incomplete: the cases above remain uncovered. |
| 2 — verdict schema; 3 — audit schema | No additional defect found; in-memory positive and rejection probes passed. |
| 5 — branch artifacts; 7 — evidence records; 12 — file inventory | Inventory stays within the declared scope; no embedded secrets found. Historical results are identified, but live CI could not be independently verified. |
| 6 — replacement task copy | Its SHA-256 matches the report; the external dispatched original was unavailable for comparison. |
| 8 — metadata; 9 — separators | YAML uses `safe_load` and bounded front matter; metadata validation does not prevent finding 4 in the evaluator. |
| 10 — in-process effects | Gate-before-dispatch/merge ordering holds, but artifact writes have finding 3. |
| 11 — workflow/interpreter/environment inputs | **Not closed:** findings 1 and 2 defeat the claimed execution boundary. |
| 13 — merge | Gate failure prevents dispatch and merge; merge arguments retain the head match. The current gate’s incompatible positional interface normally holds application, as documented. |
| 14 — update-branch; 15 — forced removal | Procedural controls outside this implementation; their execution was not verified. |

Bash syntax, shellcheck, shfmt, and isolated schema probes passed. No additional command-injection, unsafe-deserialization, or embedded-secret issue was identified.

📝 まとめ: Read-only security review completed with four findings; acceptance remains with the orchestrator.
Not run: full tests, Bats, or live application; GitHub access failed. The execution-boundary and file-write risks above remain unresolved.
Verdict: incorrect
 succeeded in 456ms:
-rw-r--r--@ 1 a0004262  staff  1041907 Oct  8 09:08 .ua/knowledge-graph.json
-rw-r--r--@ 1 a0004262  staff      156 Oct  8 09:08 .ua/meta.json

 succeeded in 651ms:
Reviewed [PR #410](https://github.com/mryfmo/dotfiles/pull/410) at `513e5d0532ec3c21484ab215ef77fea440329749` against the specified base. Found two execution-boundary vulnerabilities and one scope violation.

1. **P1 — High confidence — `scripts/orchestrator/verdict.sh:36`:** Caller-supplied `VERDICT_BIN` and matching `PATH` bypass `env -i`, allowing inherited shell functions and tool-selection variables to execute with the operator’s authority.  
   A read-only probe supplied those variables and an exported `git` function; the function executed. Rebuild the execution environment unconditionally rather than trusting an inherited re-entry marker. The threat table’s “workflow and interpreter or environment inputs” closure is therefore unsupported.

2. **P1 — High confidence — `scripts/orchestrator/verdict.sh:168`:** The dynamic import can execute attacker-supplied bytecode from ignored `scripts/__pycache__`, which the application guard at line 114 excludes from inspection.  
   An in-memory loader probe confirmed that valid cached bytecode executes under `-I -B`; `-B` prevents cache writes, not reads. This permits code execution before the integration gate, despite unchanged tracked helper sources. Load the verified source without consulting checkout caches, including the validator imported by that helper.

3. **P2 — High confidence — `.orchestration/dotfiles-T133-verdict-audit-pool-a01/task.md:1`:** The cumulative diff retains 17 predecessor artifacts outside a03’s `allowed_files`, contradicting the required final inventory in a03 `task.md:70`.  
   The worker report acknowledges these files, but their removal remains unfinished at the reviewed head.

The threat-table assessment is:

| Control row | Assessment |
|---|---|
| Verdict implementation | Execution isolation fails findings 1–2. |
| Verdict schema | Output-validation coverage is present; no additional issue identified. |
| Audit schema | Constraint rejection tests and controlled enum are present. |
| Tests | Fake-tool fixtures cover gate ordering but miss both execution vulnerabilities. |
| a03 artifact directory | Its files remain within the declared directory. |
| Replacement task copy | Replacement is present and a02 copy absent; dispatched-byte authenticity was not independently verified. |
| Branch evidence records | Historical results are labelled; final inventory remains incomplete. |
| Task metadata | External consistency checks remain an acceptance dependency. |
| Metadata separators | Parsing stops at the first closing separator; YAML uses `safe_load`. |
| In-process effects | Dispatch/merge fail closed on gate failure, but findings 1–2 execute earlier. |
| Workflow/interpreter/environment | Claimed closure fails finding 1. |
| New or renamed scripts | Implementation inventory matches; predecessor records violate the overall inventory. |
| Merge effect | Gate precedes dispatch and head-matched merge. |
| Update-branch effect | Fresh evidence is an external orchestration requirement, not verified here. |
| Forced worker removal | No removal implementation is introduced. |

No additional shell interpolation, unsafe YAML construction, or task-ID traversal issue was identified. The changed-file scan found no credential-pattern or home-directory-path matches.

📝 まとめ: Completed the read-only security review; two P1 findings and one P2 finding remain for orchestrator disposition.

Not checked: full tests, live application, or live CI—GitHub access failed. The execution risks above remain unresolved; no files were changed.
Verdict: incorrect
 succeeded in 670ms:
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
?? .orchestration/acceptance/dotfiles-T133-hold-playbook-a02.md
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
?? .orchestration/tasks/dotfiles-T133-hold-playbook-a02.md
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
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-05b8851.md
?? .orchestration/validation/dotfiles-T129-anthropic-auth-route-check-followup-a07-text-security-05b8851.md.last.md
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
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-audit-725b25b.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-audit-725b25b.md.last.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-chain-1b3e0ee.log
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-chain-725b25b.log
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-crit.json
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-local-review-725b25b.md
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-pr-feedback.json
?? .orchestration/validation/dotfiles-T129-assets-omp-hcom-followup-a03-review-receipt.md
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
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-82ced8f.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-82ced8f.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-9fc8dc4.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-9fc8dc4.md.last.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-cedac25.md
?? .orchestration/validation/dotfiles-T133-ci-efficiency-followup-a04-text-security-cedac25.md.last.md
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
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-audit-c206774.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-audit-c206774.md.last.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-chain-9f5eaee.log
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-chain-c206774.log
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-crit.json
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-local-review-9f5eaee.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-local-review-c206774.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-pr-feedback.json
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-review-receipt.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-security-c206774.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a01-security-c206774.md.last.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a02-text-security-2eb1d0b.md
?? .orchestration/validation/dotfiles-T133-hold-playbook-a02-text-security-2eb1d0b.md.last.md
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
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-0ade510.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-0ade510.md.last.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-12b9ebf.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-12b9ebf.md.last.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-6748694.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-6748694.md.last.md
?? .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-a6baa1c.md
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
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-772cde0.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-772cde0.md.last.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8520998.md
?? .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8520998.md.last.md
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
~/.local/bin/crit
~/.local/share/mise/shims:~/.local/bin:~/.local/bin/common:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:~/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:~/.local/share/mise/installs/node/lts/bin:/usr/bin:/bin:/usr/sbin:/sbin

**Adjusting output truncation**
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md .orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md | sed -n '232,257p'" in ~/Workspace/dotfiles
 succeeded in 119ms:
---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-verdict-audit-pool-a03 round=1 reset_of=dotfiles-T133-verdict-audit-pool-a02 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md task_sha256=2f0493944badef8294dc691e87fba7ab6cc84ed2d6e135454a34b1219f724c42 deadline=none done_signal=AGMSG-RESULT note=a008:the-verdict-half-of-the-P1-4a-split(verdict.sh,the-two-JSON-schemas,test_verdict.py)"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 410,
  "searches": [],
  "task": "dotfiles-T133-verdict-audit-pool-a03"
}
---

# Acceptance record: dotfiles-T133-verdict-audit-pool-a03

The verdict half of the P1-4a split (the a02 record holds the S2 decision): `verdict.sh`, `.schemas/verdict.json`, `.schemas/audit.json` and `tests/unit/test_verdict.py` stay on PR #410's branch from b8998de1; the pool files move to `dotfiles-T133-audit-pool-a01` (a009). Redesigned by a review-profile context (`.agents/worklog/orchestrator-glue/redesign/vap-a03.md`, file A). Seat: a008 (worker-f, Claude), fetching the branch, after its F1 owner RESULT. Owner of advisory P2: `dotfiles-T133-verdict-audit-pool-followup-a01` (its after now names both split tasks).

- 2026-10-19T00:4xZ: `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a008 (the line above; the full note is in the bus history). In-flight file check (C-78): verdict.sh, the two schemas and test_verdict.py appear in no other in-flight task (the pool task owns the other four files).
- 2026-10-19T02:53:51Z: RESULT round 1 from a008: PR #410 head 1bf64c949a1d5cdde918448f2c64f2fd470007a4 (code head 8b0b5bb4, previous b8998de1) on 3e41e36a, branch `tools/verdict-audit-pool-a01`; `task_copy=2f049394…` (the dispatched sha); the split commit 0e16d7eb (the a02 copy deleted, the a03 copy added, audit-pool.sh/classes.yaml/test_audit_pool.py removed, orch-audit.sh = origin/main); inventory outside .orchestration: verdict.sh, .schemas/verdict.json, .schemas/audit.json, test_verdict.py; item 6: `--apply` holds (exit 20) unless the trusted orch-gate.sh exits 0 (`test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure`); item 7: caps from the last declaration (`test_verdict_condition_5_honors_the_latest_amended_caps`); red at b8998de1, green 17/17 at 8b0b5bb4; the checker moved into verdict.sh `--validate` with a 35-case equivalence (0 disagreements); worker review 1 round (P2 fixed, 10/10 mutants killed); caps 298/300 and 393/400; shellcheck/shfmt clean; make format and make unit-test inherited failures (same at base); shadow hold exit 20; CI 7 required pass; the optional regime check fails on the stale base (the P1-11 defect, #425); Bot none; a01/a02 record directories (17 files) left for the orchestrator's reset bookkeeping. `status=pending-integration` sent 02:5xZ; chain after #425.
- 2026-10-19T02:58:31Z: C-80 review of the audit-pool-a01 text (`.orchestration/validation/dotfiles-T133-audit-pool-a01-text-security.md`): `Verdict: incorrect`, six P1 and four P2 (mise-shim resolution; GIT_* inheritance; tracked-and-unchanged checks before execution through mutable paths; previous evidence not frozen; symlink redirects of worktree and output paths; the queue lock replaceable; the shadow TSV rows not bound to outputs; shared physical slots across queues; 7-char head names collide; the closure test reads only the JSON ledger). The third text with the same class in one morning → design section 5.14 (D-024-18) written; a01 is withdrawn from a009's queue before it started, and a02 (the a01 text with 5.14 applied and the ten findings as items) is redesigned for a008.
- 2026-10-19T03:08:50Z: the audit-pool-a02 text (review profile, prompt `pool-a02-redesign-prompt.md`; design 5.14 applied by reference with one row per item; the ten C-80 findings as items) installed as `.orchestration/tasks/dotfiles-T133-audit-pool-a02.md`; checker OK; its C-80 review started 03:09Z; dispatch to a008 on `Verdict: correct`.
- 2026-10-19T03:13:23Z: C-80 review of the audit-pool-a02 text: `Verdict: incorrect`, three P1 and one P2: the write boundary is not established before P1-15 (render-check verifies equality, not isolation); D-024-17 pending; git repository-local configuration and .gitattributes (external diff, textconv, filters) still influence the audited diff; rows for 5.14 items 8-10 missing. By D-024-20 the text is sequenced `after: [dotfiles-T133-worker-write-boundary-a01]`; design 5.14 item 2 gains `--no-ext-diff --no-textconv -c core.attributesFile=/dev/null -c core.sshCommand=false`, item 7 requires one row per item 1-10; the text's next revision (rows 8-10, the git flags, P1-15 as a merged control) is batched with the a05 and dispositions-a02 revisions once the P1-15 text passes C-80.
- 2026-10-19T05:34Z: the security review of the update-branch head 513e5d05 (`…-security-513e5d0.md`): two P1 (verdict.sh:36 a caller VERDICT_BIN/PATH bypasses env -i; :168 the dynamic import can execute scripts/__pycache__ bytecode the guard excludes) and one P2 (17 predecessor artifacts of the a01/a02 directories remain in the PR tree). Counters (`--pr 410`): tasks=1 amendments=0 results=1 revises=0. Decision: revise 1 to a008 05:35Z (trusted-root resolution only, python -I -B with a __pycache__ refusal, the predecessor directories deleted from the branch); C-61: the pre-push round plus this one is the cap.
- 2026-10-19T06:29:47Z: a008 RESULT revise 1: head 934457c9 (code head 7c24617e; 3-case VERDICT_BIN/PATH test, no cached bytecode, red at 513e5d05 then 19/19, 5/5 mutants). Update-branched onto main 3f240b12 at 06:46Z → 6b7e7833 (CI 7/7 required green by 07:1xZ).
- 2026-10-19T06:59Z: the security review of 6b7e7833 (`…-security-6b7e783.md`): `Verdict: incorrect`: P1 verdict.sh:33 `compgen` runs before the inherited functions are removed, so an exported function named compgen executes before sanitization (probe confirmed); P1 :40 a caller-supplied VERDICT_BIN whose entries are absolute symlinks passes as trusted without authenticating the targets; P2 :271 the shadow log follows an unchecked symlink and appends on `hold`, and the JSON redirection at :268 has no destination containment; P2 :231 a missing, null or malformed `security` value selects 'not a security task' instead of holding. Class table: the 05:34Z rows security:513e5d0:1 env-trust-bypass (VERDICT_BIN/PATH), :2 interpreter-input-trust (__pycache__); today's :1 and :2 are env-trust-bypass again → 3 rows of one class: INV-6 S1. Counters (`--pr 410`): results=2 revises=1 (revise 1 was the C-61 cap). Root cause: the a03 design sanitizes the environment from inside a bash process that already started under the untrusted environment (functions, BASH_ENV, PATH, a caller-chosen bin dir), so every statement before the cleanup, and the cleanup itself, runs under attacker-controlled names; patches moved the gap (05:34Z PATH → 06:59Z compgen and symlinks). Proper state (design 5.14 item 2, amended today): sanitization happens before the first statement, by the invocation (`#!/bin/bash -p` executed as a program, then a self re-exec under `/usr/bin/env -i` with a fixed PATH), no caller-supplied executable directory at all, writes opened with O_NOFOLLOW inside the repository, `security` validated as an explicit boolean. Decision: re-plan; the lineage resets as verdict-audit-pool-a04 on the same branch from 6b7e7833 (redesign by the review-profile context, prompt `v-a04-redesign-prompt.md`); a008 holds (PING 07:2xZ, no fix). Dispatch of a04 follows D-024-20 (see the decision text pasted in the a04 record).
security:513e5d0:1	env-trust-bypass
security:513e5d0:2	interpreter-input-trust
security:6b7e783:1	env-trust-bypass
security:6b7e783:2	env-trust-bypass
security:6b7e783:3	write-containment
security:6b7e783:4	default-deny-gap
re-plan: env-trust-bypass (3 rows: security:513e5d0:1, security:6b7e783:1, security:6b7e783:2) — specification: the a03 text let the script sanitize itself and accept a caller bin dir; design: 5.14 item 2 gains the program-execution rule (bash -p, env -i re-exec, no caller executable directory); implementation: a04 reset on the same branch; verification: one test executes the program under exported functions named compgen, [, test, exec and command_not_found_handle plus BASH_ENV and a planted PATH and asserts none ran.
- 2026-10-19T07:24:23Z: a008 `status=holding`: PING read; no fix, no push; the #410 branch left at 934457c9 in worker-f (the remote head is the update-branch 6b7e7833); waiting for the reviewed a04 TASK.

 succeeded in 150ms:
Reviewed [PR #410](https://github.com/mryfmo/dotfiles/pull/410) at `513e5d0532ec3c21484ab215ef77fea440329749` against the specified base. Found two execution-boundary vulnerabilities and one scope violation.

1. **P1 — High confidence — `scripts/orchestrator/verdict.sh:36`:** Caller-supplied `VERDICT_BIN` and matching `PATH` bypass `env -i`, allowing inherited shell functions and tool-selection variables to execute with the operator’s authority.  
   A read-only probe supplied those variables and an exported `git` function; the function executed. Rebuild the execution environment unconditionally rather than trusting an inherited re-entry marker. The threat table’s “workflow and interpreter or environment inputs” closure is therefore unsupported.

2. **P1 — High confidence — `scripts/orchestrator/verdict.sh:168`:** The dynamic import can execute attacker-supplied bytecode from ignored `scripts/__pycache__`, which the application guard at line 114 excludes from inspection.  
   An in-memory loader probe confirmed that valid cached bytecode executes under `-I -B`; `-B` prevents cache writes, not reads. This permits code execution before the integration gate, despite unchanged tracked helper sources. Load the verified source without consulting checkout caches, including the validator imported by that helper.

3. **P2 — High confidence — `.orchestration/dotfiles-T133-verdict-audit-pool-a01/task.md:1`:** The cumulative diff retains 17 predecessor artifacts outside a03’s `allowed_files`, contradicting the required final inventory in a03 `task.md:70`.  
   The worker report acknowledges these files, but their removal remains unfinished at the reviewed head.

The threat-table assessment is:

| Control row | Assessment |
|---|---|
| Verdict implementation | Execution isolation fails findings 1–2. |
| Verdict schema | Output-validation coverage is present; no additional issue identified. |
| Audit schema | Constraint rejection tests and controlled enum are present. |
| Tests | Fake-tool fixtures cover gate ordering but miss both execution vulnerabilities. |
| a03 artifact directory | Its files remain within the declared directory. |
| Replacement task copy | Replacement is present and a02 copy absent; dispatched-byte authenticity was not independently verified. |
| Branch evidence records | Historical results are labelled; final inventory remains incomplete. |
| Task metadata | External consistency checks remain an acceptance dependency. |
| Metadata separators | Parsing stops at the first closing separator; YAML uses `safe_load`. |
| In-process effects | Dispatch/merge fail closed on gate failure, but findings 1–2 execute earlier. |
| Workflow/interpreter/environment | Claimed closure fails finding 1. |
| New or renamed scripts | Implementation inventory matches; predecessor records violate the overall inventory. |
| Merge effect | Gate precedes dispatch and head-matched merge. |
| Update-branch effect | Fresh evidence is an external orchestration requirement, not verified here. |
| Forced worker removal | No removal implementation is introduced. |

No additional shell interpolation, unsafe YAML construction, or task-ID traversal issue was identified. The changed-file scan found no credential-pattern or home-directory-path matches.

📝 まとめ: Completed the read-only security review; two P1 findings and one P2 finding remain for orchestrator disposition.

Not checked: full tests, live application, or live CI—GitHub access failed. The execution risks above remain unresolved; no files were changed.
Verdict: incorrectFound four issues in [PR #410](https://github.com/mryfmo/dotfiles/pull/410), at head `6b7e7833a85528440dc397c2555bc9dd603c685a`.

1. **P1 · high confidence · `scripts/orchestrator/verdict.sh:33`** — The cleanup invokes `compgen` before removing inherited functions, so an exported function named `compgen` executes with the operator’s authority before sanitization. A read-only probe confirmed execution.

2. **P1 · high confidence · `scripts/orchestrator/verdict.sh:40`** — A caller-supplied `VERDICT_BIN` containing absolute symlinks, together with the permitted environment and matching `PATH`, passes as trusted without authenticating the targets; a symlink to an attacker’s interpreter is accepted. The regression tests cover a copied executable and an environment forcing reconstruction, but omit this clean-environment/symlink combination.

3. **P2 · high confidence · `scripts/orchestrator/verdict.sh:271`** — Shadow logging follows an unchecked `.orchestration/validation/verdict-shadow.tsv` symlink and appends even when the verdict is `hold`, allowing a PR-controlled link to corrupt an operator-writable file outside the repository. The JSON output redirection at line 268 likewise lacks destination containment checks.

4. **P2 · high confidence · `scripts/orchestrator/verdict.sh:231`** — Missing, null, or malformed `security` values select “not a security task,” bypassing the security-review requirement instead of holding; isolated probes confirmed missing and null values pass condition 8. Only an explicitly validated boolean `false` should permit this exemption.

The threat-table assessment, using its rows in declaration order:

| Rows / controls | Assessment |
|---|---|
| 1 — verdict implementation; 4 — regression fixtures | Incomplete: the cases above remain uncovered. |
| 2 — verdict schema; 3 — audit schema | No additional defect found; in-memory positive and rejection probes passed. |
| 5 — branch artifacts; 7 — evidence records; 12 — file inventory | Inventory stays within the declared scope; no embedded secrets found. Historical results are identified, but live CI could not be independently verified. |
| 6 — replacement task copy | Its SHA-256 matches the report; the external dispatched original was unavailable for comparison. |
| 8 — metadata; 9 — separators | YAML uses `safe_load` and bounded front matter; metadata validation does not prevent finding 4 in the evaluator. |
| 10 — in-process effects | Gate-before-dispatch/merge ordering holds, but artifact writes have finding 3. |
| 11 — workflow/interpreter/environment inputs | **Not closed:** findings 1 and 2 defeat the claimed execution boundary. |
| 13 — merge | Gate failure prevents dispatch and merge; merge arguments retain the head match. The current gate’s incompatible positional interface normally holds application, as documented. |
| 14 — update-branch; 15 — forced removal | Procedural controls outside this implementation; their execution was not verified. |

Bash syntax, shellcheck, shfmt, and isolated schema probes passed. No additional command-injection, unsafe-deserialization, or embedded-secret issue was identified.

📝 まとめ: Read-only security review completed with four findings; acceptance remains with the orchestrator.
Not run: full tests, Bats, or live application; GitHub access failed. The execution-boundary and file-write risks above remain unresolved.
Verdict: incorrect
 succeeded in 169ms:
   232	2. **Executable identities are fixed at the trusted entrypoint.**
   233	
   234	   No caller-supplied executable directory exists. Remove `VERDICT_BIN`, its environment whitelist, symlink-directory acceptance and every equivalent caller override from the script and fixtures. Do not replace them with a differently named environment variable or CLI option.
   235	
   236	   The trusted entrypoint fixes the absolute paths for Bash, uv, Python, gh, git, jq and required utilities before reading PR-controlled input. It executes verified realpaths without rediscovery. The repository's Python declaration is a read-only input; consume `scripts/orchestrator/trusted-interpreter.sh` from the authenticated trusted base when present. The P1-3 resolver alone resolves the pinned declaration to a regular executable file under the tool manager's install root, anchored to the passwd home of the real uid, never to HOME, and outside worktrees, worker-writable caches and `$TMPDIR`. A symlink spelling alone authenticates nothing. An absent resolver or invalid trusted installation holds rather than selecting another interpreter from PATH, mise, uv discovery or a checkout. No private resolver, `command -v` or `mise which` fallback is retained here. Implementation may proceed before `dotfiles-T133-ci-efficiency-followup-a04` lands by implementing and testing this unavailable-resolver hold with a trusted resolver fixture for successful cases; live execution stays on hold until that lineage supplies the resolver. This task therefore does not need the resolver at implementation time and adds no P1-3 `after:` dependency.
   237	
   238	   Design 5.14 items 2, 4 and 9 apply by reference to Git invocation, executable paths, verified snapshots and private cache use. The uv invocation is `uv run --no-config --no-project --offline --python <abs>`, with uv itself an internally fixed absolute executable and `<abs>` the validated interpreter realpath. `UV_CACHE_DIR` is the anchored private cache from the design. Worker-shared uv or mise caches supply no executable. Python children use `-I`; the a03 `-B`, `sys.dont_write_bytecode` and refusal of checkout bytecode that helper imports could consume remain enforced.
   239	
   240	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_uses_only_declared_absolute_executables` verifies fixed tool identities, refusal of hostile PATH and inherited interpreter selectors, and unchanged clean-prefix execution, including an absolute symlink to a marker-writing interpreter and a forged HOME install tree that cannot become the trusted install root.
   241	
   242	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_interpreters_in_worktrees_caches_or_tmp` covers each excluded root, a non-regular target, a forged-HOME install root and a valid regular-file control under the passwd-home-anchored install root.
   243	
   244	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_executes_verified_snapshots_and_records_input_hashes` changes a validated source or input before consumption and verifies refusal or consumption of the verified snapshot, never the substituted contents, and checks the recorded input hashes.
   245	
   246	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_without_the_shared_trusted_interpreter_resolver` verifies the interim hold and absence of interpreter discovery or application effects.
   247	
   248	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_reads_pasted_counters_without_sourcing_agmsg` plants a marker-writing agmsg driver and counter executable, supplies the valid pasted counters, and requires unchanged verdicts with no marker; missing, duplicate, mismatched and unreadable counter cases hold.
   249	
   250	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_ignores_replaced_local_objects_and_refs` serves forged PR bytes through a replaced local object and forged `origin/main`, while fixed GitHub fixtures return the authentic full-head changeset and contents. It requires the clean verdict and authenticated input hashes, no local-object evidence read, and hold on incomplete API data rather than a local fallback. Cover precheck ancestry, fix-commit membership and loop shadow evaluation through the same GitHub fixtures.
   251	
   252	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_names_the_repository_on_every_gh_call` runs with a fixed fake gh that records every argument vector and asserts `--repo mryfmo/dotfiles` on every `gh pr`/`gh run`/`gh issue` call and an endpoint path beginning with `repos/mryfmo/dotfiles/` on every `gh api` call, with no `--repo` flag or repository placeholder on API calls. It covers PR view/checks, API and feedback reads and loop shadow evaluation in PR-number order. A fork fixture containing the same head SHA cannot redirect a call.
   253	
   254	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_a_changed_pr_base_or_head` supplies one initial GitHub `base40`/`head40` pair and differing SHAs on a required second read. Separate subcases change only the base, only the head and both. Each requires the named pair-change refusal, hold with exit 20 and no shadow row; the unchanged-pair control records both full SHAs and proves every compare listing and contents request uses the captured pair.
   255	
   256	   The retained `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` and `test_verdict_never_imports_cached_bytecode` remain green. Unavailable offline PyYAML still holds with no online fallback.
   257	

**Reviewing acceptance and prior text**
exec
/bin/zsh -lc 'cat .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'crit status --json' in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a04.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n -A 45 '"'^### 5.14|''^## 5.14'"' .orchestration/plans/024-design-quality.md" in ~/Workspace/dotfiles
 succeeded in 97ms:
---
format: 2
task_id: dotfiles-T133-verdict-audit-pool-a03
kind: code
security: true
allowed_files:
  - scripts/orchestrator/verdict.sh
  - .schemas/verdict.json
  - .schemas/audit.json
  - tests/unit/test_verdict.py
  - .orchestration/dotfiles-T133-verdict-audit-pool-a03/**
after: []
reset_of: [dotfiles-T133-verdict-audit-pool-a02]
threat_table:
  - control: "scripts/orchestrator/verdict.sh (the nine conditions, pinned execution context, schema validation, complete feedback matching, amended caps and gated application)"
    disposition: "residual: the retained verdict cases and the two new red-then-green regressions exercise evaluation and application; the final-head task-level audit and separate security review assess their combined coverage."
  - control: ".schemas/verdict.json (the accept, revise and hold record)"
    disposition: "closed: tests/unit/test_verdict.py::test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold"
  - control: ".schemas/audit.json (the audit contract, controlled class enum and JSON Schema 2020-12 constraints)"
    disposition: "residual: the verdict fixtures exercise schema rejection and audit interpretation; the class enum retains the inherited contract, and the sibling task owns the vocabulary file and its equality test."
  - control: "tests/unit/test_verdict.py (the retained verdict cases, split fixtures and two new regressions)"
    disposition: "residual: temporary repositories and fake external tools record arguments and effects; unrelated conditions remain green and changed evidence hashes are refreshed so each regression demonstrates its named defect."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a03/** (this reset task's branch artifacts)"
    disposition: "residual: artifacts remain within this task's directory, identify their tested heads and commands, and distinguish inherited evidence from final-head results."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md)"
    disposition: "residual: the worker deletes the a02 copy in the first push and adds the byte-identical a03 copy; the a03 copy's own SHA256 appears in the TASK and RESULT and is checked at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-verdict-audit-pool-a03/ (report.md, validation.md, sandbox.md, learning.md and revise.yaml)"
    disposition: "residual: records identify the split, retained fixes, historical red results, new regressions, refused commands, final inventory and final-head validation without rewriting predecessor history."
  - control: task metadata
    disposition: "residual: the orchestrator checks the dispatched front matter with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; byte identity covers subsequent metadata changes."
  - control: metadata separators
    disposition: "residual: the first document separators bound the YAML front matter and the dispatched-file byte comparison covers the complete task copy."
  - control: in-process effects
    disposition: "residual: evaluation writes temporary files and validation artifacts; application requires accept, four distinct agreeing shadow PRs and a successful trusted integration gate before dispatch or merge."
  - control: workflow and interpreter or environment inputs
    disposition: "closed: tests/unit/test_verdict.py::test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout"
  - control: new or renamed scripts
    disposition: "residual: this PR adds only the declared verdict executable and two JSON schema data files; the sibling implementation files leave its cumulative diff, and the final inventory is checked against allowed_files."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only with gh pr merge --squash --match-head-commit <audited head> after the integration gate; this task authorizes fixture application only and its own PR is integrated manually."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, so required CI, the feedback sweep, task-level audit and security review bind the resulting final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records the discarded uncommitted state in the acceptance record."
premises:
  - claim: orch-audit.sh takes the audited head from a PR worktree positional today, so item 3 adds --head as the alternative the pool needs
    command: "/usr/bin/grep -c 'usage: orch-audit.sh <task> <pr-worktree> <pr>' scripts/orchestrator/orch-audit.sh"
    output: |-
      1
  - claim: pr-feedback.py writes its document with --json <out>, the form verdict.sh calls for the final head's sweep
    command: uv run --no-project python scripts/pr-feedback.py --help | /usr/bin/grep -c -- '--json JSON'
    output: |-
      2
  - claim: regime-counters.sh has the --history-only mode verdict.sh reads for condition 6
    command: /usr/bin/grep -c -- '--history-only) history_only=true' scripts/regime-counters.sh
    output: |-
      1
  - claim: none of the new files exists on origin/main
    command: git ls-files .schemas scripts/orchestrator/verdict.sh scripts/orchestrator/audit-pool.sh | wc -l
    output: |-
      0
---

# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a03 — INV-6 reset of dotfiles-T133-verdict-audit-pool-a02 with the verdict and audit-pool split (PR #410; plan 024 P1-4a)

This text is the independent redesign by a review-profile context other than the author of a02. Plan 006 INV-6 S2 stopped a02 with amendments 1, questions 1 and revises 1. Its revise-1 head `b8998de162afc72d53d07679b8f0a194fcc480ff` received two further P1 and three P2. Seven local-review P1 across three heads establish that the combined three-script, three-schema surface requires a split.

PR #410 continues on `tools/verdict-audit-pool-a01` from `b8998de162afc72d53d07679b8f0a194fcc480ff`. The worker's first push deletes `.orchestration/dotfiles-T133-verdict-audit-pool-a02/task.md`, adds the dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md`, removes `scripts/orchestrator/audit-pool.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py` from the branch, and restores `scripts/orchestrator/orch-audit.sh` to `origin/main`. These named deletions and restoration are the explicit split bookkeeping exception to the worker's edit boundary. Subsequent implementation edits remain within `allowed_files`.

The orchestrator preserves historical branch evidence with its original task identifiers and tested heads, and removes predecessor artifacts from the cumulative PR diff as reset bookkeeping. The final cumulative inventory contains only this task's allowed files. The a01 and a02 acceptance histories retain their stopped status and original counters.

The sibling `dotfiles-T133-audit-pool-a01` owns the pool, audit wrapper, class vocabulary and pool tests on its own branch and PR. This task creates no implementation branch or PR. PR C stage 1 remains parked as draft PR #407 at `dfa9001b858431751faeab3b779b71eb0da01c2f`, and the completed parking step is not repeated.

The four premises preserve a02's write-time observations verbatim. Their references to the former combined items remain historical. The design is `.orchestration/plans/024-design-programs.md` items (1) and (3), with the nine conditions in `.orchestration/plans/024-design-mechanism.md`. Programs items (2) and (16) remain outside this task.

## Goal

The orchestrator obtains one schema-valid verdict from nine positively checked acceptance conditions. `--apply` reaches neither acceptance dispatch nor merge without a successful integration gate for the accepted task, head and PR. Later cap amendments govern condition 5.

The verdict implementation, both JSON schemas and the verdict tests form one independently reviewable PR. The retained interpreter, finding-count, feedback and loop-refresh fixes remain enforced.

## Files

1. `scripts/orchestrator/verdict.sh <pr> [--apply] [--loop] [--shadow]` remains Bash with `set -Eeuo pipefail`, English shdoc documentation and `jq` for JSON. Every condition is `{id, ok, evidence}` and becomes true only through a positive check of parsed, validated input.

   Inputs are `gh pr view <pr> --json headRefOid,isDraft,baseRefName,state,number`, `gh pr checks <pr> --json name,state`, the acceptance record whose JSON block names the PR, task and current head and contains a ledger array, its prose `precheck: <sha256>`, the selected task or `--task <id>`, `.orchestration/validation/<task>-audit-<sha7>.json`, a fresh `scripts/pr-feedback.py <pr> --json <mktemp>` sweep, the saved `.orchestration/validation/<task>-pr-feedback.json` dispositions, the task's `allowed_files`, `security` and Check caps, regime counters, the merge-base diff and numstat, and the required head-specific security review. The PR is open, non-draft and based on `main`. A missing head is fetched from `pull/<pr>/head` and must resolve locally before evaluation continues.

   Condition 1 verifies that `git show <head>:.orchestration/<task>/precheck.json` hashes to the record's `precheck:` value and names the head or an ancestor whose diff to the head contains only `.orchestration/<task>/` paths. Unset or zero `PRECHECK_REQUIRED` makes failure of this condition a warning.

   Condition 2 requires every required check to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Every duplicate entry for a required name must also be `SUCCESS`.

   Condition 3 requires an audit that validates against `.schemas/audit.json`, names this task and head, has zero open P0/P1 findings, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit without remaining findings fails this condition.

   Condition 4 requires both saved and fresh feedback documents to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Diagnostic URLs do not determine the result.

   Condition 5 requires every path in `git diff --name-only <base> <head>` to match an `allowed_files` entry and additions-plus-deletions totals from `git diff --numstat --no-renames <base> <head>` to remain within the effective Check caps. The base is `git merge-base origin/main <head>`. An unreadable base or diff holds. Backticked exclusions after `outside` leave the outside count. Default exclusions are `tests/` and `.orchestration/`. Item 7 defines amendment precedence.

   Condition 6 runs `scripts/regime-counters.sh <task> --pr <pr>` with its ledger source. No `S1:` line is present and the parsed `revises` value is below 2. A missing ledger, failed command or unreadable count holds.

   Condition 7 requires the numeric count of open P0/P1 findings to be zero. Findings with status `new`, `still-open` or absent count as open regardless of identifier or scope.

   Condition 8 requires `.orchestration/validation/<task>-security-<sha7>.md.last.md` to end with the last non-blank line `Verdict: correct` when the task's `security` is true. Unreadable front matter cannot select the non-security path.

   Condition 9 requires at least one `sha256:<hex> <path>` line in the acceptance record's prose and verifies every such line against its file.

   All nine conditions passing produces `accept`. Failure of condition 6 or 7, missing or unreadable input, schema-invalid input or an internal evaluation error produces `hold`. Other failed conditions produce `revise`. The revise line remains `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies `check=` selectors.

   The output is `.orchestration/validation/<task>-verdict-<sha7>.json`, validated against `.schemas/verdict.json`, with `verdict`, `pr`, `head`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`. Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with an internal error treated as hold. Refusal before a usable task or head exists reports hold without inventing an output identity.

   `--apply` requires the pinned execution context, tracked scripts, schemas and task files equal to `origin/main`, and no untracked executable helper substituted in those code directories. The last four rows of `.orchestration/validation/verdict-shadow.tsv` must agree between machine and human and represent four distinct PRs. Four rows for one PR do not unlock application. Item 6 adds the integration gate before either application effect.

   After accept and a successful gate, application writes `AGMSG-ACCEPTANCE v1 task_id=<task> status=accepted reason=verdict-<sha7> next_action=merge` to a temporary file, sends it through `scripts/orchestrator/dispatch.sh <team> <from> <to> <pane> <file> <record>`, and invokes `gh pr merge <pr> --squash --match-head-commit <head>`. Team, sender, recipient and placement come from `--team`, `--from`, `--to` and `--pane`. Arguments containing `--admin` or `--auto` anywhere are refused with exit 2 before any read or tool invocation.

   `--shadow` writes the verdict JSON and appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`, with columns `pr`, `head`, `machine`, `human`, `agree` and `at`. The orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing.

   `--loop` processes eligible open, non-draft PRs on `main` in PR-number order when an acceptance record exists and names the PR's current head. It retains the pinned context, fetches origin between PRs, and with `--apply` fast-forwards the trusted checkout to `origin/main` after each child. Failure to fast-forward holds with exit 20. Fetching alone does not satisfy the retained refresh requirement.

2. `.schemas/verdict.json` and `.schemas/audit.json` remain JSON Schema 2020-12 documents with `additionalProperties: false` at the top level and in defined item objects. Their fields retain the inherited verdict and audit contracts.

   The audit record contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and optional `status`. The controlled class enum retains the vocabulary snapshot at `b8998de162afc72d53d07679b8f0a194fcc480ff`. Its absence as a separate classes file in this branch does not loosen that enum.

   Schema validation remains available inside this task's verdict implementation under its pinned isolated interpreter. The split removes the runtime dependency on the sibling's new `orch-audit.sh --validate` mode. The existing stdlib schema-checking behavior is retained without a new helper file or dependency. Required keys, types, enums, bounds, SHA patterns, additional-property restrictions and RFC 3339 date-times with an offset remain checked. Date-only values, naive timestamps and invalid calendar dates fail.

   The sibling owns `.schemas/classes.yaml` and its equality test against this audit contract. This task changes neither the vocabulary file nor the pool implementation.

3. The interpreter-selection fix remains enforced. Before reading any PR checkout, the script resolves `uv`, Python, `gh`, `git`, `jq`, Bash and required shell utilities to absolute executables through the trusted-root, private-PATH pattern established by `scripts/orchestrator/orch-gate.sh`. Shim refusal remains enforced and the environment is explicitly constructed.

   Python runs through the pinned absolute interpreter with isolation. The offline PyYAML environment is resolved and pinned before PR input processing. Subsequent helpers, schema checks, the feedback collector, task-front-matter reading and the gate invocation retain the same tool and interpreter boundary. Checkout `.python-version`, `.venv`, executable files, uv configuration, mise configuration and inherited tool-selection variables cannot select another interpreter or tool. Missing trusted tools or unavailable offline dependencies hold before dispatch or merge.

   `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` retains its planted marker-writing interpreter and checkout-local and inherited-selector cases. Its historical red evidence against `85a472294d0c10835bd7235e3c76d045846a6ed9` remains identified as historical. The final-head green result proves that pinned evaluation works and the planted interpreter never writes its marker.

4. The remaining a02 fixes remain plain acceptance requirements.

   Conditions 3 and 7 count open P0/P1 findings numerically. Empty identifiers cannot hide a finding and records scope cannot exempt it. `test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty` retains P0, P1, `new`, `still-open` and fixed controls, with refreshed audit hashes.

   Condition 4 requires the saved and fresh `head_sha` values to equal the accepted head. `test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head` retains stale and missing-head cases for both documents.

   Condition 4 counts missing or invalid dispositions before formatting URLs. Null and empty URLs affect diagnostics only. `test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url` retains its rejected status and valid-disposition control.

   Complete feedback identity and multiplicity use the trusted root's existing `feedback_key()` and `missing_feedback()` behavior from `scripts/require-crit-review.py`. Source, URL, level, path, line, body and author participate in identity, with only the existing exact masked-body and masked-path equivalence accepted. Each saved occurrence covers at most one fresh occurrence. `test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity` retains shared-URL annotations, duplicate fresh identities with too few saved occurrences, and one valid saved occurrence per fresh occurrence.

   Disposition validation reuses `parse_disposition()` and `commit_in_range()` from the trusted root's existing `scripts/require-crit-review.py` without modifying it. A fix commit exists inside the authenticated base-to-head range. A not-applicable disposition has a non-empty reason and evidence command and satisfies existing level-specific reason requirements. Evidence commands remain data and are never executed. `test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators` retains empty and whitespace-only reasons, missing or repeated evidence delimiters, unknown commits, base commits, commits outside the head's ancestry, short failure reasons and valid positive controls.

   The historical red results for these retained fixes remain tied to their original heads. Their green results run again on the final implementation.

5. `tests/unit/test_verdict.py` retains every existing behavior case and these test names:

   `test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds`, `test_verdict_holds_on_a_missing_or_schema_failing_input`, `test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto`, `test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold`, `test_verdict_condition_1_is_a_warning_under_precheck_required_0`, `test_verdict_shadow_appends_the_machine_column_only` and `test_verdict_reads_the_record_front_matter_offline_and_holds_when_pyyaml_is_unavailable` remain present.

   `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout`, `test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty`, `test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head`, `test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url`, `test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity`, `test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators` and `test_verdict_loop_refreshes_the_trusted_checkout_after_a_merge` remain present.

   The green fixture accepts. Breaking conditions 1 to 5, 8 and 9 revises, while conditions 6 and 7 hold. Existing cases retain empty checks, failed duplicate check entries, blocked audits, incorrect audits without findings, missing ledgers and records, unavailable heads, unreadable merge bases, backticked cap exclusions, absent evidence hashes and refusal from a PR-code checkout.

   Apply fixtures retain early forbidden-flag refusal, four-distinct-PR enforcement and dispatch-before-merge ordering with `--match-head-commit`. Offline front-matter fixtures retain the cached-PyYAML green path and unavailable-offline-PyYAML hold with exit 20 and no online fallback.

   Fixtures use temporary repositories and fake tools. Their schema checks run without the sibling implementation. Red fixtures supply the inherited validation entry point as a test double where necessary so a new regression reaches its named defect. Refactoring retains every behavior case and assertion, and fixture lines count against the test cap.

6. The b8998de P1 in the application path is fixed. After accept and the shadow unlock, `--apply` runs the trusted `scripts/orchestrator/orch-gate.sh <task> <head> <pr>` and requires its zero exit before any dispatch or merge. Missing, refused or nonzero gate execution produces hold with exit 20, leaves no accepted application result and performs neither side effect. Application does not substitute its nine-condition result for the gate's receipt, audit-disposition and integration checks.

   `test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure` is written first. All nine conditions and the four-distinct-PR shadow requirement pass. A fake gate records the exact task, full head and PR and returns failure. The inherited implementation incorrectly dispatches and merges, giving the red result against `b8998de162afc72d53d07679b8f0a194fcc480ff`. The fixed implementation holds and calls neither tool. Missing and refused gate cases also hold. A zero-exit control proves the exact order gate, dispatch, merge and retains the head-matched merge arguments.

   The current gate wrapper takes a PR-worktree path in its second position. This task changes no gate interface. Refusal of the specified head form remains hold until that form is supported by the trusted wrapper. No alternate gate or direct-merge fallback bypasses the refusal.

7. The b8998de P2 in the cap parser is fixed. The parser honors the latest amendment's cap sentence, using the last applicable `at most <n>` declaration in text order instead of the first historical declaration. The effective sentence supplies its exclusions and test limit. A later test-only amendment replaces the test limit while retaining the outside limit.

   `test_verdict_condition_5_honors_the_latest_amended_caps` is written first. An otherwise green fixture contains an original 500-line test cap and a later amendment allowing 550, with 531 changed test lines. The inherited implementation applies 500 and fails condition 5, giving the red result against `b8998de162afc72d53d07679b8f0a194fcc480ff`. The fixed implementation accepts under 550. Subcases retain the actual a02 test-only amendment wording, verify a later lower limit refuses acceptance, and verify that amended exclusions and outside limits come from the effective cap sentence. Unrelated conditions remain green and evidence hashes remain current.

The seven required check names are `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.

## Out of scope

The sibling owns `audit-pool.sh`, changes to `orch-audit.sh`, `classes.yaml` and `test_audit_pool.py`. `dispatch.sh`, the record generator, `dispositions.py`, `--second-opinion`, `hold-playbook.sh`, `integrate-seat.sh`, gate and validator changes, Makefile targets, CI changes and live deployment remain outside this task. The two b8998de findings assigned above are fixed here rather than assigned to an advisory owner.

## Check

The validation file contains commands, verbatim output, exit statuses and tested heads for `make unit-test`, `make render-check`, `make format`, `shellcheck scripts/orchestrator/verdict.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/verdict.sh` and `uv run python -m unittest tests.unit.test_verdict -v`. The script checks are clean and the verdict module is green.

The concrete shadow invocation is `scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a03`. Its JSON, exit status and tested head appear in `.orchestration/dotfiles-T133-verdict-audit-pool-a03/validation.md`. Hold is expected before the required audit and acceptance evidence exist. This task exercises no live `--apply`.

Each new regression has its own red result against `b8998de162afc72d53d07679b8f0a194fcc480ff` and green result after the fix. Retained tests run on the final implementation. Historical a01 and a02 results keep their original references and do not substitute for final-head validation.

`git diff --numstat origin/main...HEAD` shows at most 300 changed lines outside `tests/` and `.orchestration/`, and 400 under `tests/`. Changed lines are additions plus deletions over the complete PR diff. `verdict.sh` is the sole implementation script and is at most 300 lines on its own. The two JSON schemas remain in the outside total and their line counts are also reported separately. Meeting a cap removes no required behavior, validation, regression case or trust-boundary control.

An inherited check failure is reproduced against the unchanged base with the same command and environment and reported as a failure with that evidence. It is never labelled passing or repaired outside the edit boundary. Local Bats tests remain unrun and GitHub Actions supplies their required results.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task-copy byte comparison and SHA256 cover this a03 text. The final inventory confirms the sibling files and predecessor branch artifacts have left PR #410.

## Completion

One branch, `tools/verdict-audit-pool-a01`, continues PR #410 with the split verdict scope. The first push contains the replacement a03 copy and the specified split removals. No second implementation PR or branch is created for this task and no parking operation is repeated.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with the live rules below, `dotfiles-T133-verdict-audit-pool-followup-a01` as the owner of advisory P2, `task_copy=<sha256 of .orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md>` and `parked_pr=407` in the RESULT. The orchestrator writes the owner task before assigning an advisory disposition. The two b8998de findings in items 6 and 7 belong to this reset.

There is at most one worker-side pre-push review round. Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. Predecessor rounds and stopped histories remain recorded. A surviving P0/P1 stops the PR for the operator's decision under the inherited Completion rule.

The report and RESULT identify head, base, branch, changed files, every feedback disposition, test names, code and test totals, schema counts, task-copy hash and evidence paths. They distinguish retained fixes, the split, historical evidence and final-head results. A Codex seat writes evidence at the same relative paths in its own worktree and states that placement in the RESULT. Worker review evidence uses the required `-worker-` infix and the orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. The orchestrator runs its own final-head task-level audit and separate security-profile review before the gate. Final-head CI, the feedback sweep, finding dispositions, acceptance record, integration gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive fresh required evidence. The orchestrator merges with `gh pr merge --squash --match-head-commit <audited head>` after the gate. Four-distinct-PR shadow enforcement remains in code and this PR is integrated manually.

No `@codex review` comment is posted. Automatic review is observed for the bounded window and absence after 15 minutes is recorded as `bot: none`. Commands matching a live ask rule are not issued and no API or browser path bypasses that rule. Each `gh` command, Git write and `git fetch` runs individually without shell chaining or a wrapper combining commands. Refused commands retain their command, exit status and output while independent authorized work continues.

Until plan 024 P1-14 lands, every string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool. Shell commands, heredocs and shell wrappers do not write those strings. This writing rule supplies no authorization to execute a command refused by the live permission boundary.

Live dispatch, merge and local Bats are not exercised. A trusted gate that rejects the head argument keeps live application on hold.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-verdict-audit-pool-a03.md: OK
premises: copied from a02 verbatim
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md
```

 succeeded in 160ms:
---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 410,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-verdict-audit-pool-a04"
}
---

# Acceptance record: dotfiles-T133-verdict-audit-pool-a04

Reset of the verdict lineage's a03 (PR #410, branch tools/verdict-audit-pool-a01, from 6b7e7833) after the security review of the update-branch head found two P1 of the class env-trust-bypass (three rows: INV-6 S1) at the C-61 cap; the a03 record holds the class table and the re-plan line. Text designed by the review-profile context (`.agents/worklog/orchestrator-glue/redesign/v-a04.md`, prompt `v-a04-redesign-prompt.md`): program execution with `bash -p` and an env -i re-exec, no caller-supplied executable directory, O_NOFOLLOW writes inside the repository, `security` as an explicit boolean; `after: [dotfiles-T133-worker-write-boundary-a01]` (D-024-20); the sentences of design 5.14 items 2, 4, 5 and 9 quoted inline (C-88). Seat: a008 (Claude, worker-f), holding. Advisory owner: dotfiles-T133-verdict-audit-pool-a05 (written when the first row appears).

- 2026-10-19T07:36Z: text installed (333 lines + the quotations); `task-consistency-check.py: OK`.
- 2026-10-19T07:41Z: C-80 first review (`…-text-security-*.md`, see the validation directory): `Verdict: incorrect`: P1 a caller-set VERDICT_SANITIZED=1 skips the env -i re-exec and `bash -p` keeps GIT_* (fixed binaries consume attacker-selected git configuration and object stores); P1 the retained counter sources agmsg storage code whose drivers.partition selects a sourced file through worker-writable team configuration (no row, no compensating control); P1 equality to local origin/main and the merge-base trust the shared refs/objects Codex workers can write (the evaluated changeset can differ from the PR); P2 condition 8 names the security report by sha7; P2 `/bin/bash -p --noprofile --norc` exits 2 (long options must precede -p). Root causes: a sentinel is caller-controlled (the check must be of the environment itself); the design let the verdict read PR content from the shared object db and run agmsg shell code. Design 5.14 amended (item 2: option order and the clean-environment check instead of a sentinel; item 8: PR content read from GitHub at the 40-hex head or from a private clone; item 9: one trusted interpreter resolver). Decision: round 2 by the review-profile context (prompt `v-a04r2-redesign-prompt.md`).
text-security:v-a04-r1:1	sentinel-skippable
text-security:v-a04-r1:2	store-plugin-trust
text-security:v-a04-r1:3	shared-objectdb-trust
text-security:v-a04-r1:4	sha7-collision
text-security:v-a04-r1:5	bash-option-order
- 2026-10-19T08:3xZ: the a04 text's design citation is a literal home path (the validator's home-path scan refuses it in a committed task copy); the round-2 text is installed with the `$HOME`-relative form (C-86 amended).
- 2026-10-19T08:29Z: round-2 text (redesign `v-a04r2.md`, 368 lines) installed: the clean-environment check replaces the sentinel, `/bin/bash --noprofile --norc -p` order, counters read from the agmsg SQLite store read-only (no agmsg shell code sourced; the storage route named with its owner), PR content from GitHub at the 40-hex head, full-head evidence names, the 5.14 items 2/8/9 quotations refreshed; the design citation `$HOME`-relative; checker OK; C-80 round 2 started.
- 2026-10-19T08:33:20Z: C-80 second review (`…-text-security-*.md`, newest): `Verdict: incorrect`: P1 HOME preserved by the sanitization selects the resolver's install root (executable selection through an environment variable); P1 LD_PRELOAD/LD_AUDIT run before the first statement on Linux (bash -p does not enable the loader's secure mode); P1 the no-sourcing control fails during application: `dispatch.sh` calls `history.sh`, which sources the agmsg storage and partition drivers; P2 the retained gate (`make require-crit-review`) independently runs `uv python find`, rediscovers tools and rereads shared refs, so application needs a compliant-gate prerequisite; P1 `gh pr merge` without `--repo` lets the local configuration select another repository (a fork can hold the same head). Design 5.14 amended: item 2 (trusted parent, verify-and-refuse, passwd home) and item 9 (install root anchored to the passwd home) earlier today; item 8 now (`--repo` on every gh call; `--apply` prerequisites named, shadow-only until merged). The orchestrator's merge glue gains `--repo mryfmo/dotfiles` on its gh pr calls (08:3xZ). Decision: round 3 by the review-profile context (prompt `v-a04r3-redesign-prompt.md`).
text-security:v-a04-r2:1	home-anchored-trust
text-security:v-a04-r2:2	loader-env-before-exec
text-security:v-a04-r2:3	store-plugin-trust
text-security:v-a04-r2:4	gate-prerequisite
text-security:v-a04-r2:5	repository-binding
- 2026-10-19T09:19Z: round-3 text (`v-a04r3.md`, 384 lines) installed: trusted parent supplies the environment and the program verifies and refuses (allowed names, `$0` realpath, HOME = passwd home), install root anchored to the passwd home, `--repo mryfmo/dotfiles` on every gh call (11 occurrences) with a fake-gh argument test, `--apply` gated on the recorded merges of agmsg-hardening-a01 and dispositions-a02 (shadow-only until then), 5.14 items 2/4/5/8/9 quotations refreshed; checker OK; C-80 round 3 started.
- 2026-10-19T09:24:08Z: C-80 third review (`…-text-security-*.md`, newest): `Verdict: incorrect`: P1 the gate prerequisite named dispositions-a02, whose text still authenticates through `git show origin/main` and excludes require-crit-review.py (the claim was not owned); P1 the agmsg merge record does not authenticate the installed agmsg code dispatch executes (bind the installed version and the storage.sh sha256); P2 `gh api` has no `--repo` flag (installed gh 2.102.0) — the repository binds through the explicit `repos/mryfmo/dotfiles/…` endpoint (design 5.14 item 8 reworded). Decision: round 4 by the review-profile context (prompt `v-a04r4-redesign-prompt.md`): the gate prerequisite becomes the to-be-written `dotfiles-T133-gate-hardening-a01`; installation binding for agmsg; endpoint-bound gh api calls.
text-security:v-a04-r3:1	gate-prerequisite
text-security:v-a04-r3:2	installation-binding
text-security:v-a04-r3:3	repository-binding
- 2026-10-19T09:36Z: round-4 text (`v-a04r4.md`, 388 lines) installed: the `--apply` gate prerequisite is the to-be-written dotfiles-T133-gate-hardening-a01 (dispositions-a02 does not own it), the agmsg prerequisite binds the installed version file and the storage.sh sha256 pinned in the hardening record, `gh api` calls bind the repository through `repos/mryfmo/dotfiles/…` endpoints (9) and `gh pr`/`gh run` through `--repo`; checker OK; C-80 round 4 started.
- 2026-10-19T09:39:00Z: C-80 fourth review (newest `…-text-security-*.md`): `Verdict: incorrect`: P1 the installation pins (VERSION, storage.sh) do not cover the agmsg execution chain dispatch runs; P1 prerequisites authenticated at main40 while the tree is authenticated at a separately captured base40. Both attack the `--apply` mode that this task only gates. Re-plan (YAGNI; P1-4a is shadow until four agreements): `--apply` is removed from a04 (refused with a named message); application is a later task (`dotfiles-T133-verdict-apply-a01`, not written) with its own prerequisites; the evaluated tree binds to one head40/base40 pair captured once. Round 5 by the review-profile context (prompt `v-a04r5-redesign-prompt.md`).
text-security:v-a04-r4:1	installation-binding
text-security:v-a04-r4:2	prerequisite-tree-binding
re-plan: apply-mode-trust (rows text-security:v-a04-r2:3, v-a04-r3:2, v-a04-r4:1, v-a04-r4:2) — specification: a04 gated --apply behind prerequisites instead of not shipping it; design: shadow-only verdict (plan 024 P1-4a), application deferred to verdict-apply-a01; implementation: --apply removed from the text and the script; verification: --apply refuses with a named message; no agmsg code path exists.
- 2026-10-19T09:49Z: round-5 text (`v-a04r5.md`, 376 lines) installed: shadow-only (`--apply` refused with a named message; application deferred to verdict-apply-a01, not written; no agmsg code path, no gate call), the evaluated tree bound to one head40/base40 pair captured once; checker OK; C-80 round 5 started.

 succeeded in 198ms:
99:## 5.14 信頼ホスト実行契約（trusted-host execution contract、D-024-18）
100-
101-orchestrator 側の仕組み（merge gate、integrate-merge、orch-gate、dispositions、audit-pool、verdict、chain）は、同じホスト上で同じ UID の worker プロセスと共存する。2026-10-19 の C-80 審査（a05、dispositions-a02、audit-pool-a01 の 3 文、計 19 件の P1）は、どの文も同じ前提を書かず同じ穴を持つことを示した。以後、`security: true` の orchestrator 側タスク文は本節を参照で適用し、本節の各項目に対応する threat 行を持つ。文ごとに言い換えない。
102-
103-1. **書き込み境界（前提 6、ランタイム別に正直に）** Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。chezmoi は user ではこのファイルを書けないので、描画した内容を操作者が `sudo` で一度配置する（操作者手順）。worker 設定は worktree 自身の `.claude/**` と `.mcp.json` への Edit deny（`//<anchored>/.claude/worktrees/*/.claude/**`）を持つ（Bash 側は sandbox 既定の settings/hooks の denyWithinAllow）。agmsg store（全席が書く）から配送 hook が driver や plugin を source する上流の経路（storage.sh の `drivers.partition` traversal、`db/trusted-plugins` と `plugins/partition/shared.sh` による差し替え承認）は別タスク（agmsg hardening）の行で、worker 設定は `~/.agents/skills/agmsg/plugins/**` と `~/.agents/skills/agmsg/db/trusted-plugins` への書き込みを deny し（Edit deny は sandbox の deny にも合流する）、hook 側は store 由来の設定値を検証するまで残余と書く。managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。公式文書：linked worktree の session は **main checkout の `.claude/settings.local.json` を読む**ので、worker 向けの hook を worktree の settings.local.json に書いても読まれず、逆に orchestrator の local hooks が worker session でも走る。したがって orchestrator 側の local hooks も guard 経由にし、worker 側の hook は worker config dir の settings に置く。Edit deny の一覧は `git ls-tree` ではなく描画時の静的一覧（manifest に列挙、`.agents/worklog/**` と `.agents/worklog/uv-cache/**` を含む）とし、`~/.agents/**` の全面 deny は agmsg store の書き込みと矛盾するので、`~/.agents/agent-config.yaml`、`~/.agents/skills/**/scripts/**`、`~/.agents/model-profiles.env` などストア以外を列挙する。公式文書で確認した事実（2026-10-19）：`Edit(path)` の deny は Write/MultiEdit/NotebookEdit にも効き、deny → ask → allow の順で最初の一致が決まる；ただし Read/Edit の deny は **Bash sandbox の設定にも合流する**（"Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration"）ので、ユーザー設定（全席共有）に `.orchestration/**` の Edit deny を書くと orchestrator の Bash による記録書き込みも止まる。hook は起動時に固定されず、設定ファイルの編集は file watcher が即座に反映する。`sandbox.failIfUnavailable` の既定は fail-open（依存が無ければ sandbox 無しで実行）。したがって Claude 席の境界は Edit deny 規則ではなく、**ユーザーレベルの PreToolUse hook**（`~/.claude/hooks/worker-write-boundary`、chezmoi が描画、`/bin/sh` または絶対パスの `python3 -I`）で作る：cwd の realpath が `<anchored>/.claude/worktrees/` 配下の session では、Write/Edit/MultiEdit/NotebookEdit の対象が cwd の外、または `<cwd>/.claude/**`・`<cwd>/.mcp.json` のとき `permissionDecision: deny` を返す。Bash 側は sandbox の既定 `denyWithinAllow`（settings、hooks）と `allowWrite`（自席 worktree）が担う。`failIfUnavailable: true` を全席に置く。 Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。Claude 席は Seatbelt sandbox が Bash を限るだけで、Write/Edit/MultiEdit/NotebookEdit、hook、MCP プロセスは sandbox 外で動き、permission policy（permgate の決定論ポリシー）が path で拒否しない限り anchored checkout や `~/.agents` にも書ける（2026-10-19 時点、描画済み設定にその deny は無い）。したがって前提 6 は「Codex 席は成立、Claude 席は P1-15 が描画設定に Edit の path deny を入れるまで残余」と書く。P1-15 以前に「worker は信頼ルートに書けない」と書く文は誤りで、C-80 が拒否する。P1-15 が入るまで、承認の出所は項目 8 の「コミット済み台帳」で守る。書き込みは自席の worktree（`.claude/worktrees/<name>`）、scratch、列挙されたツールキャッシュに限る。anchored checkout（`.claude/worktrees/` 以外）、`~/.agents/agent-config.yaml`、`~/.claude/hooks`、信頼ルートのバイナリ、orchestrator の証跡・スナップショット・lock は worker から書けない。render テストが描画後の deny を検証する。残余は「どの席 sandbox にも属さない同一 UID プロセス」と、Worker Playbook step 4 が sandbox 外に出す少数のコマンド（gh）。後者は D-024-17（P1-15）で絶対パスの実行体に束縛する。 The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19).
104-2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
105-3. **信頼パスの境界検査** 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。 A validator or scanner enumerates its inputs by walking the filesystem under fixed roots (every regular file, ignored or untracked included), never by asking git which files exist: `git ls-files` trusts the index and the working-tree `.gitignore` rules, which a same-UID writer edits without a commit (a07 C-80 rounds 1 to 3, 2026-10-19); git is consulted only to confirm the root (`--show-toplevel` equality with a real `.git` directory) and never as an exclusion authority.
106-4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。
107-5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。
108-6. **正直な残余** 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。
109-0. **脅威モデル（D-024-21）** 席は同じ OS ユーザで動き、ホストは席間の信頼境界ではない（同一 UID のプロセスは symlink 差し替え、共有 `.git` の object 差し替え、hook の子プロセス、Herdr socket 経由の host 実行で、ホスト内のどの検査も迂回できる）。regime の硬い境界は GitHub（保護された main、必須チェック、orchestrator の identity によるマージ）。ただしこの境界は **worker 席が orchestrator の GitHub 資格情報を共有しない**ときだけ成立する（D-024-22：worker 席は専用の GitHub identity（別アカウントまたは App のトークン）で `gh` に login し、ruleset の bypass 一覧に入らない。orchestrator の keychain トークンを worker の config dir に持ち込まない。identity が分かれるまで「GitHub が境界」は未成立と書く）。**同一 macOS ユーザでは資格情報は分離できない**（gh は keychain の項目を host/user で引き、同じ UID の gh は orchestrator のトークンを読める。`GH_CONFIG_DIR` は設定を分けるだけ）。防止には worker 席を別の OS ユーザ（または別ホスト）で動かすしかなく、それは D-024-23 の将来項目（P1-16、操作者の判断）。それまで GitHub 境界は **検知**で守る：記録は boundary の記録 PR まで main に無いので、検知は次の記録 PR の regime ジョブで行う（`.orchestration/acceptance/**` に触れる PR で、前回 boundary 以降の main の各マージ commit に、gate 通過の証跡を持つ受け入れ記録が対応することを検査し、無ければその PR を失敗させる；P1-11 owner a02 の行 `ci:detection:1`）。main push 時点の検知は記録が無いので不可能であり、文は「次の記録 PR で検知、防止ではない」と書く。悪意ある worker に耐えるべき入力（承認台帳、gate が読む証跡 of record）は GitHub から sha 指定で API 経由（sandbox 内）に読み、ローカルファイルやローカル object database からは読まない。ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。
110-8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder: the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged.
111-9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19).
112-10. **worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）** 2026-10-19T03:45Z の実測で `gh api` は Claude sandbox の中から成功した（sandbox の proxy は CONNECT 型で TLS を終端しない；keychain のトークンも読めた）。worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。Codex 席は `sandbox_workspace_write.network_access = true` で同じ状態にし、permgate の codex ポリシーは sandbox 外への escape を承認しない（permgate の変更は操作者の手順）。wrapper 方式（絶対パス、env -i、固定 GH_CONFIG_DIR）は LD_PRELOAD と引数転送（`gh repo clone -- --config`）を閉じられないので採らない。
113-7. **検証** threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。共通テスト補助 `tests/unit/trusted_exec_contract.py`（P1-6 で作る）を使い、仕組みごとに 4 つの red→green テストを持つ：PATH 先頭の shim が実行されない、植え付けた GIT_* と git 設定が効かない、worker ルート配下の信頼パスが拒否される、検証後に差し替えたファイルが消費側に届かない。

 succeeded in 266ms:
{
  "branch": "main",
  "daemon": {
    "running": false
  },
  "review_file": "~/.crit/reviews/c06a520c1f9b/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}

**Confirming no delegation needed**
exec
/bin/zsh -lc 'cat .orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a04.md' in ~/Workspace/dotfiles
 succeeded in 0ms:
---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 410,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-verdict-audit-pool-a04"
}
---

# Acceptance record: dotfiles-T133-verdict-audit-pool-a04

Reset of the verdict lineage's a03 (PR #410, branch tools/verdict-audit-pool-a01, from 6b7e7833) after the security review of the update-branch head found two P1 of the class env-trust-bypass (three rows: INV-6 S1) at the C-61 cap; the a03 record holds the class table and the re-plan line. Text designed by the review-profile context (`.agents/worklog/orchestrator-glue/redesign/v-a04.md`, prompt `v-a04-redesign-prompt.md`): program execution with `bash -p` and an env -i re-exec, no caller-supplied executable directory, O_NOFOLLOW writes inside the repository, `security` as an explicit boolean; `after: [dotfiles-T133-worker-write-boundary-a01]` (D-024-20); the sentences of design 5.14 items 2, 4, 5 and 9 quoted inline (C-88). Seat: a008 (Claude, worker-f), holding. Advisory owner: dotfiles-T133-verdict-audit-pool-a05 (written when the first row appears).

- 2026-10-19T07:36Z: text installed (333 lines + the quotations); `task-consistency-check.py: OK`.
- 2026-10-19T07:41Z: C-80 first review (`…-text-security-*.md`, see the validation directory): `Verdict: incorrect`: P1 a caller-set VERDICT_SANITIZED=1 skips the env -i re-exec and `bash -p` keeps GIT_* (fixed binaries consume attacker-selected git configuration and object stores); P1 the retained counter sources agmsg storage code whose drivers.partition selects a sourced file through worker-writable team configuration (no row, no compensating control); P1 equality to local origin/main and the merge-base trust the shared refs/objects Codex workers can write (the evaluated changeset can differ from the PR); P2 condition 8 names the security report by sha7; P2 `/bin/bash -p --noprofile --norc` exits 2 (long options must precede -p). Root causes: a sentinel is caller-controlled (the check must be of the environment itself); the design let the verdict read PR content from the shared object db and run agmsg shell code. Design 5.14 amended (item 2: option order and the clean-environment check instead of a sentinel; item 8: PR content read from GitHub at the 40-hex head or from a private clone; item 9: one trusted interpreter resolver). Decision: round 2 by the review-profile context (prompt `v-a04r2-redesign-prompt.md`).
text-security:v-a04-r1:1	sentinel-skippable
text-security:v-a04-r1:2	store-plugin-trust
text-security:v-a04-r1:3	shared-objectdb-trust
text-security:v-a04-r1:4	sha7-collision
text-security:v-a04-r1:5	bash-option-order
- 2026-10-19T08:3xZ: the a04 text's design citation is a literal home path (the validator's home-path scan refuses it in a committed task copy); the round-2 text is installed with the `$HOME`-relative form (C-86 amended).
- 2026-10-19T08:29Z: round-2 text (redesign `v-a04r2.md`, 368 lines) installed: the clean-environment check replaces the sentinel, `/bin/bash --noprofile --norc -p` order, counters read from the agmsg SQLite store read-only (no agmsg shell code sourced; the storage route named with its owner), PR content from GitHub at the 40-hex head, full-head evidence names, the 5.14 items 2/8/9 quotations refreshed; the design citation `$HOME`-relative; checker OK; C-80 round 2 started.
- 2026-10-19T08:33:20Z: C-80 second review (`…-text-security-*.md`, newest): `Verdict: incorrect`: P1 HOME preserved by the sanitization selects the resolver's install root (executable selection through an environment variable); P1 LD_PRELOAD/LD_AUDIT run before the first statement on Linux (bash -p does not enable the loader's secure mode); P1 the no-sourcing control fails during application: `dispatch.sh` calls `history.sh`, which sources the agmsg storage and partition drivers; P2 the retained gate (`make require-crit-review`) independently runs `uv python find`, rediscovers tools and rereads shared refs, so application needs a compliant-gate prerequisite; P1 `gh pr merge` without `--repo` lets the local configuration select another repository (a fork can hold the same head). Design 5.14 amended: item 2 (trusted parent, verify-and-refuse, passwd home) and item 9 (install root anchored to the passwd home) earlier today; item 8 now (`--repo` on every gh call; `--apply` prerequisites named, shadow-only until merged). The orchestrator's merge glue gains `--repo mryfmo/dotfiles` on its gh pr calls (08:3xZ). Decision: round 3 by the review-profile context (prompt `v-a04r3-redesign-prompt.md`).
text-security:v-a04-r2:1	home-anchored-trust
text-security:v-a04-r2:2	loader-env-before-exec
text-security:v-a04-r2:3	store-plugin-trust
text-security:v-a04-r2:4	gate-prerequisite
text-security:v-a04-r2:5	repository-binding
- 2026-10-19T09:19Z: round-3 text (`v-a04r3.md`, 384 lines) installed: trusted parent supplies the environment and the program verifies and refuses (allowed names, `$0` realpath, HOME = passwd home), install root anchored to the passwd home, `--repo mryfmo/dotfiles` on every gh call (11 occurrences) with a fake-gh argument test, `--apply` gated on the recorded merges of agmsg-hardening-a01 and dispositions-a02 (shadow-only until then), 5.14 items 2/4/5/8/9 quotations refreshed; checker OK; C-80 round 3 started.
- 2026-10-19T09:24:08Z: C-80 third review (`…-text-security-*.md`, newest): `Verdict: incorrect`: P1 the gate prerequisite named dispositions-a02, whose text still authenticates through `git show origin/main` and excludes require-crit-review.py (the claim was not owned); P1 the agmsg merge record does not authenticate the installed agmsg code dispatch executes (bind the installed version and the storage.sh sha256); P2 `gh api` has no `--repo` flag (installed gh 2.102.0) — the repository binds through the explicit `repos/mryfmo/dotfiles/…` endpoint (design 5.14 item 8 reworded). Decision: round 4 by the review-profile context (prompt `v-a04r4-redesign-prompt.md`): the gate prerequisite becomes the to-be-written `dotfiles-T133-gate-hardening-a01`; installation binding for agmsg; endpoint-bound gh api calls.
text-security:v-a04-r3:1	gate-prerequisite
text-security:v-a04-r3:2	installation-binding
text-security:v-a04-r3:3	repository-binding
- 2026-10-19T09:36Z: round-4 text (`v-a04r4.md`, 388 lines) installed: the `--apply` gate prerequisite is the to-be-written dotfiles-T133-gate-hardening-a01 (dispositions-a02 does not own it), the agmsg prerequisite binds the installed version file and the storage.sh sha256 pinned in the hardening record, `gh api` calls bind the repository through `repos/mryfmo/dotfiles/…` endpoints (9) and `gh pr`/`gh run` through `--repo`; checker OK; C-80 round 4 started.
- 2026-10-19T09:39:00Z: C-80 fourth review (newest `…-text-security-*.md`): `Verdict: incorrect`: P1 the installation pins (VERSION, storage.sh) do not cover the agmsg execution chain dispatch runs; P1 prerequisites authenticated at main40 while the tree is authenticated at a separately captured base40. Both attack the `--apply` mode that this task only gates. Re-plan (YAGNI; P1-4a is shadow until four agreements): `--apply` is removed from a04 (refused with a named message); application is a later task (`dotfiles-T133-verdict-apply-a01`, not written) with its own prerequisites; the evaluated tree binds to one head40/base40 pair captured once. Round 5 by the review-profile context (prompt `v-a04r5-redesign-prompt.md`).
text-security:v-a04-r4:1	installation-binding
text-security:v-a04-r4:2	prerequisite-tree-binding
re-plan: apply-mode-trust (rows text-security:v-a04-r2:3, v-a04-r3:2, v-a04-r4:1, v-a04-r4:2) — specification: a04 gated --apply behind prerequisites instead of not shipping it; design: shadow-only verdict (plan 024 P1-4a), application deferred to verdict-apply-a01; implementation: --apply removed from the text and the script; verification: --apply refuses with a named message; no agmsg code path exists.
- 2026-10-19T09:49Z: round-5 text (`v-a04r5.md`, 376 lines) installed: shadow-only (`--apply` refused with a named message; application deferred to verdict-apply-a01, not written; no agmsg code path, no gate call), the evaluated tree bound to one head40/base40 pair captured once; checker OK; C-80 round 5 started.

exec
/bin/zsh -lc "sed -n '105,155p' .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md" in ~/Workspace/dotfiles
 succeeded in 0ms:

   All nine conditions passing produces `accept`. Failure of condition 6 or 7, missing or unreadable input, schema-invalid input or an internal evaluation error produces `hold`. Other failed conditions produce `revise`. The revise line remains `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies `check=` selectors.

   The output is `.orchestration/validation/<task>-verdict-<sha7>.json`, validated against `.schemas/verdict.json`, with `verdict`, `pr`, `head`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`. Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with an internal error treated as hold. Refusal before a usable task or head exists reports hold without inventing an output identity.

   `--apply` requires the pinned execution context, tracked scripts, schemas and task files equal to `origin/main`, and no untracked executable helper substituted in those code directories. The last four rows of `.orchestration/validation/verdict-shadow.tsv` must agree between machine and human and represent four distinct PRs. Four rows for one PR do not unlock application. Item 6 adds the integration gate before either application effect.

   After accept and a successful gate, application writes `AGMSG-ACCEPTANCE v1 task_id=<task> status=accepted reason=verdict-<sha7> next_action=merge` to a temporary file, sends it through `scripts/orchestrator/dispatch.sh <team> <from> <to> <pane> <file> <record>`, and invokes `gh pr merge <pr> --squash --match-head-commit <head>`. Team, sender, recipient and placement come from `--team`, `--from`, `--to` and `--pane`. Arguments containing `--admin` or `--auto` anywhere are refused with exit 2 before any read or tool invocation.

   `--shadow` writes the verdict JSON and appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`, with columns `pr`, `head`, `machine`, `human`, `agree` and `at`. The orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing.

   `--loop` processes eligible open, non-draft PRs on `main` in PR-number order when an acceptance record exists and names the PR's current head. It retains the pinned context, fetches origin between PRs, and with `--apply` fast-forwards the trusted checkout to `origin/main` after each child. Failure to fast-forward holds with exit 20. Fetching alone does not satisfy the retained refresh requirement.

2. `.schemas/verdict.json` and `.schemas/audit.json` remain JSON Schema 2020-12 documents with `additionalProperties: false` at the top level and in defined item objects. Their fields retain the inherited verdict and audit contracts.

   The audit record contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and optional `status`. The controlled class enum retains the vocabulary snapshot at `b8998de162afc72d53d07679b8f0a194fcc480ff`. Its absence as a separate classes file in this branch does not loosen that enum.

   Schema validation remains available inside this task's verdict implementation under its pinned isolated interpreter. The split removes the runtime dependency on the sibling's new `orch-audit.sh --validate` mode. The existing stdlib schema-checking behavior is retained without a new helper file or dependency. Required keys, types, enums, bounds, SHA patterns, additional-property restrictions and RFC 3339 date-times with an offset remain checked. Date-only values, naive timestamps and invalid calendar dates fail.

   The sibling owns `.schemas/classes.yaml` and its equality test against this audit contract. This task changes neither the vocabulary file nor the pool implementation.

3. The interpreter-selection fix remains enforced. Before reading any PR checkout, the script resolves `uv`, Python, `gh`, `git`, `jq`, Bash and required shell utilities to absolute executables through the trusted-root, private-PATH pattern established by `scripts/orchestrator/orch-gate.sh`. Shim refusal remains enforced and the environment is explicitly constructed.

   Python runs through the pinned absolute interpreter with isolation. The offline PyYAML environment is resolved and pinned before PR input processing. Subsequent helpers, schema checks, the feedback collector, task-front-matter reading and the gate invocation retain the same tool and interpreter boundary. Checkout `.python-version`, `.venv`, executable files, uv configuration, mise configuration and inherited tool-selection variables cannot select another interpreter or tool. Missing trusted tools or unavailable offline dependencies hold before dispatch or merge.

   `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` retains its planted marker-writing interpreter and checkout-local and inherited-selector cases. Its historical red evidence against `85a472294d0c10835bd7235e3c76d045846a6ed9` remains identified as historical. The final-head green result proves that pinned evaluation works and the planted interpreter never writes its marker.

4. The remaining a02 fixes remain plain acceptance requirements.

   Conditions 3 and 7 count open P0/P1 findings numerically. Empty identifiers cannot hide a finding and records scope cannot exempt it. `test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty` retains P0, P1, `new`, `still-open` and fixed controls, with refreshed audit hashes.

   Condition 4 requires the saved and fresh `head_sha` values to equal the accepted head. `test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head` retains stale and missing-head cases for both documents.

   Condition 4 counts missing or invalid dispositions before formatting URLs. Null and empty URLs affect diagnostics only. `test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url` retains its rejected status and valid-disposition control.

   Complete feedback identity and multiplicity use the trusted root's existing `feedback_key()` and `missing_feedback()` behavior from `scripts/require-crit-review.py`. Source, URL, level, path, line, body and author participate in identity, with only the existing exact masked-body and masked-path equivalence accepted. Each saved occurrence covers at most one fresh occurrence. `test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity` retains shared-URL annotations, duplicate fresh identities with too few saved occurrences, and one valid saved occurrence per fresh occurrence.

   Disposition validation reuses `parse_disposition()` and `commit_in_range()` from the trusted root's existing `scripts/require-crit-review.py` without modifying it. A fix commit exists inside the authenticated base-to-head range. A not-applicable disposition has a non-empty reason and evidence command and satisfies existing level-specific reason requirements. Evidence commands remain data and are never executed. `test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators` retains empty and whitespace-only reasons, missing or repeated evidence delimiters, unknown commits, base commits, commits outside the head's ancestry, short failure reasons and valid positive controls.

   The historical red results for these retained fixes remain tied to their original heads. Their green results run again on the final implementation.

5. `tests/unit/test_verdict.py` retains every existing behavior case and these test names:

   `test_verdict_accepts_only_when_all_nine_conditions_hold_and_each_broken_condition_revises_or_holds`, `test_verdict_holds_on_a_missing_or_schema_failing_input`, `test_verdict_apply_calls_nothing_unless_accept_and_refuses_admin_and_auto`, `test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold`, `test_verdict_condition_1_is_a_warning_under_precheck_required_0`, `test_verdict_shadow_appends_the_machine_column_only` and `test_verdict_reads_the_record_front_matter_offline_and_holds_when_pyyaml_is_unavailable` remain present.

   `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout`, `test_verdict_counts_open_p0_p1_findings_even_when_the_id_is_empty`, `test_verdict_condition_4_requires_saved_and_fresh_heads_to_equal_the_accepted_head`, `test_verdict_condition_4_rejects_an_undispositioned_status_with_a_null_url`, `test_verdict_condition_4_preserves_complete_item_identity_and_multiplicity`, `test_verdict_condition_4_uses_the_existing_disposition_and_commit_validators` and `test_verdict_loop_refreshes_the_trusted_checkout_after_a_merge` remain present.

   The green fixture accepts. Breaking conditions 1 to 5, 8 and 9 revises, while conditions 6 and 7 hold. Existing cases retain empty checks, failed duplicate check entries, blocked audits, incorrect audits without findings, missing ledgers and records, unavailable heads, unreadable merge bases, backticked cap exclusions, absent evidence hashes and refusal from a PR-code checkout.

   Apply fixtures retain early forbidden-flag refusal, four-distinct-PR enforcement and dispatch-before-merge ordering with `--match-head-commit`. Offline front-matter fixtures retain the cached-PyYAML green path and unavailable-offline-PyYAML hold with exit 20 and no online fallback.


exec
/bin/zsh -lc 'cat .ua/meta.json' in ~/Workspace/dotfiles
 succeeded in 0ms:
{
  "lastAnalyzedAt": "2026-10-02T14:12:51Z",
  "gitCommitHash": "940a3a2b07adfd14140a0acff96784ef53a0a509",
  "version": "1.0.0",
  "analyzedFiles": 368
}

**Evaluating symlink and path security**
**Reviewing sandbox and helper execution rules**
codex
過去の指摘に対して、今回の本文は `--apply` の削除、GitHub の base/head 固定、起動前の環境除去を明記しています。残る確認点は、固定した実行体・検証済み snapshot が、既存ヘルパーの子プロセスや import 先まで届く設計になっているかです。
exec
/bin/zsh -lc 'git diff --name-only 940a3a2b07adfd14140a0acff96784ef53a0a509..HEAD -- scripts home/dot_agents/agent-config.yaml' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "/usr/bin/python3 -I -B -c 'import json; g=json.load(open(\".ua/knowledge-graph.json\")); print(\"\\n\".join(str({k:n.get(k) for k in (\"filePath\",\"summary\")}) for n in g.get(\"nodes\",[]) if any(s in str(n.get(\"filePath\",\"\")) for s in (\"pr-feedback\", \"require-crit\", \"orchestrator\", \"agent-config\"))))'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'subprocess|Popen|sys.executable|importlib|__file__|gh_env|run_git|\\[\"gh\"|\\[\"git\"' scripts/pr-feedback.py scripts/require-crit-review.py scripts/validate-orchestration.py" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'cat .orchestration/validation/dotfiles-T133-verdict-audit-pool-a04-text-security-{0ade510,12b9ebf,6748694,b9bf09a}.md.last.md' in ~/Workspace/dotfiles
 exited 2 in 103ms:
rg: scripts/validate-orchestration.py: No such file or directory (os error 2)
scripts/pr-feedback.py:21:import subprocess
scripts/pr-feedback.py:66:def gh_env() -> dict[str, str]:
scripts/pr-feedback.py:74:    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False, env=gh_env())
scripts/pr-feedback.py:96:    result = subprocess.run(
scripts/pr-feedback.py:97:        ["gh", "auth", "status"],
scripts/pr-feedback.py:101:        env=gh_env(),
scripts/require-crit-review.py:8:import importlib.util
scripts/require-crit-review.py:12:import subprocess
scripts/require-crit-review.py:138:def run_git(args: list[str], root: Path | None = None) -> subprocess.CompletedProcess[str]:
scripts/require-crit-review.py:139:    return subprocess.run(
scripts/require-crit-review.py:140:        ["git", *args],
scripts/require-crit-review.py:144:        stdout=subprocess.PIPE,
scripts/require-crit-review.py:145:        stderr=subprocess.PIPE,
scripts/require-crit-review.py:150:    result = run_git(["rev-parse", "--show-toplevel"])
scripts/require-crit-review.py:214:        result = run_git(command, root)
scripts/require-crit-review.py:226:        result = run_git(command, root)
scripts/require-crit-review.py:236:    untracked = run_git(["ls-files", "--others", "--exclude-standard"], root)
scripts/require-crit-review.py:392:        run_git(["merge-base", "--is-ancestor", commit, head], root).returncode == 0
scripts/require-crit-review.py:393:        and run_git(["merge-base", "--is-ancestor", commit, base], root).returncode != 0
scripts/require-crit-review.py:454:        if commit and run_git(["cat-file", "-e", f"{commit}^{{commit}}"], root).returncode != 0:
scripts/require-crit-review.py:475:    spec = importlib.util.spec_from_file_location(
scripts/require-crit-review.py:476:        "validate_agent_assets", Path(__file__).resolve().with_name("validate-agent-assets.py")
scripts/require-crit-review.py:479:    module = importlib.util.module_from_spec(spec)
scripts/require-crit-review.py:523:        repository = subprocess.run(
scripts/require-crit-review.py:524:            ["gh", "repo", "view", "--json", "nameWithOwner"],
scripts/require-crit-review.py:539:        result = subprocess.run(
scripts/require-crit-review.py:540:            ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "headRefOid,baseRefName,baseRefOid"],
scripts/require-crit-review.py:559:        or run_git(["cat-file", "-e", f"{github_base}^{{commit}}"], root).returncode != 0
scripts/require-crit-review.py:569:    resolved = run_git(["rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}"], root)
scripts/require-crit-review.py:574:        if run_git(["merge-base", "--is-ancestor", base_sha, github_base], root).returncode == 0:
scripts/require-crit-review.py:575:            first_parents = run_git(["rev-list", "--first-parent", head], root)
scripts/require-crit-review.py:579:        if run_git(["merge-base", "--is-ancestor", github_base, base_sha], root).returncode == 0:
scripts/require-crit-review.py:580:            actual = run_git(["merge-base", base_sha, head], root)
scripts/require-crit-review.py:581:            expected = run_git(["merge-base", github_base, head], root)
scripts/require-crit-review.py:610:        base_collector = run_git(["show", f"{evidence['base_sha']}:scripts/pr-feedback.py"], root)
scripts/require-crit-review.py:614:        result = subprocess.run(
scripts/require-crit-review.py:615:            [sys.executable, str(collector), str(pr), "--repo", evidence["repo"], "--json", str(collected_path)],
scripts/require-crit-review.py:619:            stdout=subprocess.PIPE,
scripts/require-crit-review.py:620:            stderr=subprocess.PIPE,
scripts/require-crit-review.py:960:    The same match as `grep -rl 'classes:.*<class>'`, without a subprocess; the gate reads its result, never
scripts/require-crit-review.py:995:    verify = run_git(["rev-parse", "--verify", "--quiet", "--end-of-options", f"{base}^{{commit}}"], root)
scripts/require-crit-review.py:1018:    head = run_git(["rev-parse", "HEAD"], root).stdout.strip() if args.base else None
scripts/require-crit-review.py:1039:    current_head = head or run_git(["rev-parse", "HEAD"], root).stdout.strip()

 succeeded in 180ms:
home/dot_agents/agent-config.yaml
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

 succeeded in 203ms:
- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:210](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:210) — Matching `VERSION` and `storage.sh` does not authenticate executed `history.sh`, `driver-registry.sh` or loaded drivers; a mixed installation passes the prescribed test while executing unverified code, so installation pins must cover the execution chain.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:208](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:208) — Prerequisites are authenticated at `main40`, but execution is authenticated against the separately captured `base40` at line 162; if main advances between reads, merged-hardening records can unlock an older gate, requiring an explicit binding between prerequisite commits and the executed tree plus a regression for differing SHAs.

📝 まとめ: Reviewed every threat row and cited context; two execution-binding findings remain for orchestrator disposition.

Not checked: implementation tests or live deployment; no files changed. The prerequisite checks do not yet bind all executed code.
Verdict: incorrect- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:44](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:44) — The delegated gate control is not owned as claimed: `dispositions-a02` still authenticates through `git show origin/main` and excludes `require-crit-review.py` from its edit boundary; its merge therefore cannot establish the promised descendant-execution and evidence binding.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:208](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:208) — An authenticated agmsg merge record does not authenticate the installed `~/.agents/skills/agmsg/scripts/history.sh` and storage code that dispatch executes; without deployment/version binding, the prerequisite can pass while the old worker-influenced driver-sourcing route remains installed.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:264](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:264) — The fake-gh test requires unsupported `--repo` arguments on API calls: installed gh 2.102.0 rejects the prescribed command with `unknown flag: --repo`, preventing evaluation; API calls must bind repository identity through explicit endpoints rather than this flag. [CLI documentation](https://cli.github.com/manual/gh_api)

📝 まとめ: Reviewed every threat row and cited context; three findings remain for orchestrator disposition.

Not run: implementation tests or live application; no files changed. The prerequisite-to-execution gaps remain unresolved.
Verdict: incorrect- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:206](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:206) — Caller-set `VERDICT_SANITIZED=1` skips `env -i`; `bash -p` preserves `GIT_*`, so fixed binaries still consume attacker-selected Git configuration and object stores; read-only probes confirmed both survive the proposed sentinel check. [Bash semantics](https://www.gnu.org/s/bash/manual/html_node/The-Set-Builtin.html)

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:130](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:130) — The retained counter sources agmsg storage code, whose `drivers.partition` selects a sourced file through worker-writable team configuration; pinning the counter and its interpreter does not bind that descendant execution, and this known route lacks a threat row or compensating control.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:144](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:144) — Equality to local `origin/main` and the merge-base calculation still trust shared refs/objects that sandboxed Codex workers can write; snapshot hashes preserve the selected bytes without authenticating them against GitHub, allowing the evaluated changeset to differ from the actual PR.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:134](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:134) — Condition 8 checks only the security report’s final verdict while retaining its sha7 filename; a different head sharing that prefix can reuse an earlier approval because no full-head content check is required, and full-head output names do not mitigate this input collision.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:206](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:206) — The prescribed `/bin/bash -p --noprofile --norc` re-exec exits 2 on this host before evaluation; Bash requires long options before `-p`, so the hostile-startup regression cannot produce the required clean-equivalent verdict through this branch. [Invocation rules](https://www.gnu.org/software/bash/manual/html_node/Invoking-Bash.html)

📝 まとめ: Reviewed every declared threat row and the cited context; five findings remain for orchestrator disposition.
Not run: implementation tests, live CI or deployment checks; no files changed. The execution and evidence-binding risks above remain unresolved.
Verdict: incorrect- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:222](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:222) — Sanitization preserves attacker-supplied `HOME`, while the required resolver derives its trusted installation root from `$HOME/.local/share/mise/installs`; validating a candidate against that caller-selected root recreates executable selection through an environment variable.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:220](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:220) — On Linux, inherited `LD_PRELOAD`/`LD_AUDIT` can execute before Bash’s first statement—or before `/usr/bin/env` clears the environment—because `bash -p` does not enable the loader’s secure-execution mode; the startup regression omits this route. [Loader semantics](https://man7.org/linux/man-pages/man8/ld.so.8.html)

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:42](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:42) — The “no agmsg shell sourcing” compensating control covers counters but fails during application: retained `dispatch.sh` invokes `history.sh`, which sources storage and partition drivers; verifying dispatch’s bytes does not bind this worker-influenced descendant execution, and application has no agmsg-hardening prerequisite.

- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:202](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:202) — The retained gate independently runs `uv python find`, rediscovers tools, and rereads shared refs and live evidence; snapshotting its script and testing a fake gate’s exit/order cannot establish the promised execution/input binding, so application needs an explicit compliant-gate prerequisite beyond the acknowledged argument-mismatch hold.

- [P1] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:162](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:162) — Reads use a fixed repository, but the prescribed merge command omits `--repo` or a qualified PR URL, allowing local repository configuration to select another repository; matching the head SHA does not bind repository identity because forks can contain the same commit. [Merge options](https://cli.github.com/manual/gh_pr_merge)

📝 まとめ: Reviewed every threat row and the cited acceptance/review context; five findings remain for orchestrator disposition.

Not run: implementation tests, live application or deployment checks; no files changed. The execution-binding risks above remain unresolved.
Verdict: incorrect
 succeeded in 253ms:
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
python3: error: couldn't create cache file '/tmp/xcrun_db-uRk6iNKC' (errno=Operation not permitted)
python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
python3: error: couldn't create cache file '/tmp/xcrun_db-0MdET1dJ' (errno=Operation not permitted)
{'filePath': 'home/dot_agents/agent-config.yaml', 'summary': 'Canonical hand-edited manifest for Codex and Claude Code: model profiles (express/standard/review/deep/security/audit/adh), herdr-agents worker kind/profile/worktree, Codex and Claude settings, sandboxes, permissions, hooks, plugins, disabled-by-default MCP servers, and pinned install assets. All agent-native config files are rendered from it.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Generator that renders agent-native configuration (Codex config.toml, Claude settings/sandbox/MCP, plugin marketplace, model-profile TOML and modify scripts, profiles env, express-explorer agent, asset pin constants) from home/dot_agents/agent-config.yaml, with --check and --set-asset modes.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Parses the agent manifest YAML with PyYAML, failing clearly when PyYAML is missing or the document is not a mapping.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Serializes Python scalars, lists, and tables into TOML literal syntax.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Validates the model_profiles mapping (required express/standard profiles, claude/codex fields) and returns it.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Rewrites one scalar under assets.<name> in the manifest text while preserving comments and layout.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Rewrites each asset\'s NAME="..." pin assignment in its render target file (e.g. installer-pins.sh), enforcing plain pin values and exactly one assignment.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Renders the managed Codex config.toml: models, sandbox and writable roots, features, hooks, MCP servers, plugins, and projects.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Renders the Claude sandbox settings block, reusing the Codex agmsg writable roots for allowWrite.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Renders the managed Claude Code settings JSON: hooks, permissions, sandbox, env, plugins, statusline, and model defaults.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Builds one Claude MCP server entry for stdio or HTTP transports from the manifest definition.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Renders the local Codex plugin marketplace JSON from manifest plugin entries.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Renders one managed Codex plugin manifest, failing when required plugin keys are missing.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Produces chezmoi symlink_ outputs mirroring every shared skill file into home/dot_claude/skills.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Renders a per-profile Codex TOML (model, reasoning effort, notify) launched via `codex --profile <name>`.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Generates a chezmoi modify_ Python script that merges the managed profile keys into an existing ~/.codex/<profile>.config.toml without clobbering user keys.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Renders the model-profiles.env shell fragment (interactive profile, worker kind/profile/worktree, per-profile CLI args) for agent launchers.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Renders the express-explorer Claude subagent definition pinned to the express profile model.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Collects every generated output path and rendered content derived from the manifest.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'Deletes generated files and empty directories under home/dot_claude/skills that are no longer expected.'}
{'filePath': 'scripts/generate-agent-configs.py', 'summary': 'CLI entry handling --set-asset pin rewrites, --check drift verification, stale output removal, and writing all generated files.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Collector that gathers every piece of GitHub feedback on a PR head (issue comments, reviews, inline comments with thread state, non-passing checks, annotations, commit statuses) into one JSON document with empty dispositions for the PR integration gate.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Exits with guidance when `gh auth status` reports the GitHub CLI is not authenticated.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Builds one normalized feedback item (source, actor, bot flag, level, body, url, path/line, thread state) with an empty disposition.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Queries review threads over GraphQL and maps each review comment id to its resolved and outdated state.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'Fetches all PR feedback sources for the head commit via REST/GraphQL and assembles the item list with repo, PR, head and base metadata.'}
{'filePath': 'scripts/pr-feedback.py', 'summary': 'CLI entry that resolves the repo, requires gh auth, collects feedback, and writes JSON to stdout or a file.'}
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

**Evaluating design constraints and schema checks**
**Analyzing environment variable validation**
exec
/bin/zsh -lc 'wc -l .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md' in ~/Workspace/dotfiles
exec
/bin/zsh -lc "rg -n 'case|symlink|gh|Linux|sandbox|mise|P1-3|trusted-interpreter|interpreter|install root' .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '465,510p' scripts/require-crit-review.py; sed -n '1,80p' scripts/validate-agent-assets.py" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '55,115p' scripts/pr-feedback.py; sed -n '125,175p' scripts/pr-feedback.py; sed -n '200,245p' scripts/pr-feedback.py; sed -n '330,385p' scripts/pr-feedback.py" in ~/Workspace/dotfiles
 succeeded in 153ms:
        if item.get("level") in STRICT_REASON_LEVELS and not commit and len(reason) < FAILURE_REASON_MIN_CHARS:
            errors.append(
                f"{label} is {item.get('level')}-level; not-applicable needs a reason of at least {FAILURE_REASON_MIN_CHARS} characters"
            )
    return errors


@cache
def validator():
    """Load the validator that ships next to this guard, for its secret masker."""
    spec = importlib.util.spec_from_file_location(
        "validate_agent_assets", Path(__file__).resolve().with_name("validate-agent-assets.py")
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def feedback_key(item: dict, masked: bool = False) -> tuple:
    """Identify a feedback item; `masked` takes its body and path as `--mask-secrets` saves them.

    A saved body or path may be verbatim or exactly that masked form, because
    masking (`validate-agent-assets.py --mask-secrets`, which masks the string
    values of a JSON file) is the repository's documented way to keep evidence
    scannable, and the url still identifies the item. Source, url, level, line
    and author stay byte-exact; the author decides which items the acceptance
    record's ledger must cover, so it is matched against the live collection too.
    """
    key = {field: item.get(field) for field in ("source", "url", "level", "path", "line", "body", "author")}
    if masked:
        # Only the body and a key-shaped file path may be masked; the rest is exact.
        for field in ("path", "body"):
            if isinstance(key[field], str):
                key[field] = validator().mask_secret_matches(key[field])[0]
    return tuple(key.values())


def missing_feedback(collected: list, saved: list) -> Counter:
    """Count collected items with no saved item, verbatim or masked, left to match."""
    available = Counter(feedback_key(item) for item in saved if isinstance(item, dict))
    missing: Counter = Counter()
    for item in collected:
        for key in dict.fromkeys((feedback_key(item), feedback_key(item, masked=True))):
            if available[key]:
                available[key] -= 1
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
# PLAN H3 pins the current relative SessionStart order across managed sources.
SESSIONSTART_EXPECTED_COMMAND_SUBSTRINGS = {
    "claude": ("herdr-agent-state.sh",),
    "codex": (),
    "compactiondb": ("contextdb_hook.py", "contextdb_recover.py"),
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:

 succeeded in 191ms:
     120 .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md

 succeeded in 211ms:
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:11:  - scripts/orchestrator/trusted-interpreter.sh
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:12:  - tests/unit/test_trusted_interpreter.py
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:16:  - control: scripts/orchestrator/ci-rerun.sh interpreter selection and invocation
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:17:    disposition: "closed: tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:24:  - control: scripts/orchestrator/trusted-interpreter.sh fixed declaration parser and read-only real-installation resolution
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:25:    disposition: "residual: tests/unit/test_trusted_interpreter.py::TrustedInterpreterTest::test_pinned_interpreter_ignores_checkout_path_without_mise is the positive case; its red state is the refusal path (before the implementation the resolver does not exist, so the test fails by absence); a named missing-installation skip is not positive coverage; install-symlink and install-not-regular cannot be exercised in CI or by the worker (implemented, refuses by code, verified by reading); temporary refusal fixtures and read-only real-installation checks do not establish host directory protection"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:26:  - control: tests/unit/test_trusted_interpreter.py read-only real-installation and temporary hostile-input fixtures
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:27:    disposition: "residual: the positive case reads the real repository and real passwd-home installation read-only and records a named skip when the pinned installation is absent; negative declaration fixtures execute temporary repository copies with the real passwd-home installation read-only and assert their specific refusal codes without bypassing the passwd-home anchor; their results cannot establish host directory protection"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:35:    disposition: "residual: fixtures use fake GitHub executables and temporary ledgers; production retains the existing reservation, ledger append and gh run rerun --failed effect, which is not exercised against GitHub during unit tests"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:36:  - control: workflow and interpreter or environment inputs
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:39:    disposition: "residual: scripts/orchestrator/trusted-interpreter.sh is the one new executable script; no other new or renamed script is authorized"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:41:    disposition: "residual: only the orchestrator merges PR #424 after the integration gate, using gh pr merge --squash --match-head-commit with the audited head; local controls do not prevent a same-UID credential holder from bypassing this procedure"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:47:    disposition: "residual: D-024-20 requires the worker-write-boundary dependency before dispatch and verification of the deployed boundary; same-UID processes outside a seat sandbox remain outside that protection"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:50:  - control: design 5.14 item 3 interpreter path boundaries
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:51:    disposition: "residual: interpreter checks requiring a mutated installation under the real passwd home cannot be exercised in CI or by the worker (implemented, refuses by code, verified by reading); tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_refuses_unsafe_flake_registry_destination, tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_refuses_unsafe_ledger_destination and tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_refuses_unsafe_reservation_destination cover this consumer's resolved destinations only after an accepted baseline whose repository copy is executed as the program; declaration-file and anchored uv-cache destination validation and path boundaries in other scripts remain unimplemented by this task, so the row remains residual rather than claiming full item-3 closure"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:62:  - control: design 5.14 item 9 private cache and shared interpreter resolver
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:64:  - control: design 5.14 item 10 commands remain inside the sandbox
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:65:    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; an unavailable operation produces a blocked PONG rather than an outside-sandbox retry"
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:68:premises: []
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:71:# AGMSG-TASK dotfiles-T133-ci-efficiency-followup-a04 — replace the interpreter-selection class with one trusted resolver
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:73:Plan 024 P1-3. Worker: `claude-standard-dot-a011`, Claude Code, `.claude/worktrees/worker-d`. Continue branch `tools/ci-efficiency-followup-a02` and [PR #424](https://github.com/mryfmo/dotfiles/pull/424) from head `67e2cc98`; do not create another branch or PR.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:75:[memory:failure] The predecessor reached the C-61 round cap with its worker-side fix round and revise 1, and INV-6 S2 with two amendment dispatches. Its rebase repair and update-branches do not erase those counts. The security review of `44cb8353` found the owned `interpreter-selection` class again: `command -v python3` accepts an activated checkout’s absolute `.venv/bin/python3`, which then executes through uv and directly with operator authority.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:79:Read the predecessor task and acceptance record, `.orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-security-44cb835.md.last.md`, and `.orchestration/validation/dotfiles-T133-ci-efficiency-followup-a02-local-review-7329f0e.md`. The latter’s pre-pin cleanup-command P1 stays covered. Preserve the predecessor implementation, tests and historical evidence except for the explicitly replaced interpreter-selection mechanism and task copy.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:83:The inspected repository does **not** contain `.mise.toml`, `.tool-versions` or `.python-version`. Its root `mise.toml` contains only `[tools]`; its actual managed declaration, `home/dot_mise/config.toml`, says `python = "latest"`, which is not an exact pin. Do not describe any of these as an existing pinned Python declaration.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:85:Before dispatch, the orchestrator must resolve that missing prerequisite through an authorized change and bind this text to the actual trusted declaration and its exact grammar. No declaration file is writable under this task’s `allowed_files`; the worker must not add a pin, select the newest installation, or substitute an installed version. Until resolved, this task is held.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:89:D-024-20 also requires `dotfiles-T133-worker-write-boundary-a01` to be accepted and its deployed protection verified before dispatch. The pinned declaration, interpreter installation and anchored private cache must be outside worker-writable roots.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:91:Every caller of either program, including the chain glue, CI steps and tests, must supply the trusted-parent clean prefix specified below. Caller changes outside `allowed_files` are an orchestrator-owned dispatch prerequisite to land through a separate authorized change; this task does not authorize editing those callers.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:97:Item 2: “A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.” “Python は `-I`。” “PATH 探索で実行するものは無い。”
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:101:Item 9: “orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。” “`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。” “One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19).”
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:103:## Item 1 — one trusted interpreter resolver
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:105:Add executable `scripts/orchestrator/trusted-interpreter.sh`, with English shdoc comments and `#!/bin/bash -p`. Every caller executes it as a program through a trusted parent supplying `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …`; do not source it or use an unqualified `bash <file>` invocation. The parent itself must already be trusted and clean before starting `/usr/bin/env`; clearing the environment after a loader has consumed it is too late. There is no self re-exec.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:107:Before traps, tool discovery or declaration reads, verify the actual environment's exact allowed names through `/usr/bin/env` and `/usr/bin/grep`, the fixed PATH and LANG values, the script's absolute realpath and the passwd-home match. Account explicitly for Bash's own maintained environment entries so the clean prefix succeeds; allow no sanitization sentinel or production test exemption. Require `$0` to be the bound absolute canonical script pathname and its realpath to be a regular file under the trusted repository root, outside worker roots; refuse a symlinked `$0`, including a worker-owned symlink to the trusted script, without reopening it. Any invalid environment, script path or HOME exits 2 with a named `trusted-interpreter:` diagnostic and no stdout, instead of repairing or re-executing.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:109:Read only the repository’s exact Python declaration established by the dispatch prerequisite, anchored to the trusted script/repository location rather than the caller’s cwd. Parse its fixed grammar as data with trusted absolute tools, without `source`, `eval`, shell interpolation of declaration content, or an interpreter selected from that content. Refuse missing, duplicate, malformed, non-exact or metacharacter-bearing declarations; `latest` is invalid.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:111:Obtain the real uid through `/usr/bin/id -ru`. On macOS obtain its user name through `/usr/bin/id -run` and its passwd home through `/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory`; on Linux use `/usr/bin/getent passwd <uid>`. Refuse a missing, ambiguous or malformed passwd result, or any disagreement between that passwd home and HOME, with exit 2 and a named `trusted-interpreter:` diagnostic before selecting a candidate. Derive the installation root only as `<passwd home>/.local/share/mise/installs`, never from the HOME variable, and construct only `<install root>/python/<version>/bin/python3`. Resolve and validate the candidate before printing it. Require an executable regular file after `realpath`, within the expected protected installation, outside the worktree, manifest worker roots, worker-writable caches and `$TMPDIR`. Check resolved path boundaries, including filesystem case behavior where applicable. Refuse a symlinked installation rather than accepting a redirected install directory.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:113:On success print exactly one absolute interpreter realpath and exit 0. On every refusal print exactly one line `trusted-interpreter: refused: <code>` to stderr, print no interpreter on stdout, and exit 2. The codes are `dirty-environment`, `script-path`, `home-mismatch`, `declaration-missing`, `declaration-malformed`, `declaration-duplicate`, `install-missing`, `install-not-regular`, `install-symlink`, `install-outside-root` and `version-mismatch`. Invalid entry environment uses `dirty-environment`; a noncanonical or symlinked script path uses `script-path`; invalid passwd data or HOME disagreement uses `home-mismatch`. An absent declaration uses `declaration-missing`, duplicates use `declaration-duplicate`, and malformed, non-exact or metacharacter-bearing declarations use `declaration-malformed`. An absent candidate uses `install-missing`, a non-executable or non-regular candidate uses `install-not-regular`, a symlinked installation uses `install-symlink`, a forbidden resolved path uses `install-outside-root`, and a resolved installation version differing from the pin uses `version-mismatch`. Every negative test asserts its specific reason code as well as exit 2 and no interpreter stdout; an earlier refusal is not coverage of a later check. There is no `command -v`, `mise which`, PATH search, version-alias selection, download or fallback. Do not execute a candidate to discover whether it is trustworthy.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:119:Apply the same trusted-parent clean prefix, privileged program entry, exact environment verification, canonical `$0` realpath check and real-uid passwd-home match to `scripts/orchestrator/ci-rerun.sh`. Refuse any entry failure with exit 2 and exactly one `ci-rerun: refused: <code>` line before tool setup or effects: `dirty-environment` for invalid environment names or values, `script-path` for a noncanonical or symlinked script path, and `home-mismatch` for invalid passwd data or HOME disagreement. Do not repair the environment or self re-exec. Invoke the resolver by its bound absolute realpath through the same clean prefix, supplying HOME from the verified passwd home, and consume its single validated result; propagate refusal without trying another interpreter.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:127:Before reading or writing the flake registry, ledger or reservation state, resolve `.github/flakes.yaml`, `.orchestration/validation/ci-reruns.tsv` and the reservation parent `.orchestration/validation/ci-reruns.lock.d` with `realpath`. Require the registry and ledger to be regular files and the reservation parent to be a directory under the confirmed repository root, outside manifest worker roots, worker-writable caches and `$TMPDIR`. Refuse symlinks in the destination or any path component below that root, and, on a case-insensitive filesystem, a destination differing from its declared pathname only by case. Use only the validated canonical destinations for subsequent reads and effects. Apply the same checks to an existing per-run reservation directory before inspecting its claim and to a newly claimed directory before using it. Missing output objects may be created only at the existing effect point after validating their existing parent chain and resolving the intended destination; resolve and type-check each newly created object before appending ledger data or using a claim. Preserve atomic per-run creation and never replace an existing object during validation. Any destination-validation failure exits 2 with exactly one `ci-rerun: refused: <code>` line before registry parsing, ledger access or a rerun, leaving redirected targets unchanged. Destination codes are `destination-outside-root` for a resolved path outside the confirmed repository or in a forbidden root, `destination-symlink` for an otherwise contained path with a symlink in the destination or its parent chain, `destination-case-alias` for an otherwise contained case alias, `destination-not-regular` for an invalid registry or ledger file type, and `destination-not-directory` for an invalid reservation directory type. Check containment before symlink, case-alias and type checks so an outside-root mutation has its own distinguishable code.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:129:Run the YAML-loading Python only through `uv run --no-config --no-project --offline --python "<abs>"`, retaining `--with pyyaml`, with `python -I` as the command. Run the reservation Python directly as `"<abs>" -I …`. Both use the resolver’s realpath, never a Python link in a temporary directory, another lookup, or an inherited virtual environment.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:139:Write the failing regressions before the fix and paste red and green output. Every negative security case asserts its specific refusal code, not just exit 2 or an empty marker. Declaration-mutating negative cases (missing, malformed, duplicate, non-exact and metacharacter-bearing declarations, and the exact declaration used for a missing installation) execute the canonical resolver in a temporary copy of the repository tree through the trusted-parent clean prefix. Mutate only that copy's declaration; keep the real uid's passwd-home installation read-only and retain the real passwd-home lookup and install-root anchor. Add `tests/unit/test_trusted_interpreter.py` with class `TrustedInterpreterTest` and these tests:
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:141:- `test_pinned_interpreter_ignores_checkout_path_without_mise`: prepend a temporary checkout’s marker-writing `.venv/bin/python3` to PATH with mise unavailable; direct dirty entry exits 2 with `trusted-interpreter: refused: dirty-environment` and no marker. Its positive clean-prefix case invokes the canonical resolver in the real repository, reads that repository’s pinned declaration and the tool-manager-installed interpreter beneath the real uid’s passwd-home install root read-only, and expects exactly one absolute realpath and exit 0. Assert that the printed path is an executable regular file under that install root, then execute it as `"<abs>" -I -c 'import sys; print(sys.version_info[:2])'` and compare the output with the pinned version’s major/minor pair. Assert the resolver exists before considering a skip: its red state is the refusal path, failing by absence before implementation. If the pinned installation is absent, skip only this positive case with the named reason `pinned-installation-unavailable`, including the pin and expected install root, and record the skip in `report.md` and `validation.md`; do not skip dirty-entry or other negative cases. An existing installation that fails validation or version matching is a test failure, not a skip; the marker remains absent in every case.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:142:- `test_missing_install_is_refused`: in the temporary repository copy, declare an exact version whose installation under the real passwd-home root is confirmed absent without creating or modifying it; assert exit 2, `trusted-interpreter: refused: install-missing` and no stdout.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:143:- `test_shell_metacharacter_in_declaration_is_refused`: a copied declaration containing a shell metacharacter exits 2 with `trusted-interpreter: refused: declaration-malformed`, no interpreter stdout and no marker, without executing it.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:144:- `test_duplicate_malformed_nonexact_or_metacharacter_declarations_are_refused`: through the clean prefix in the temporary repository copy, cover duplicate declarations with `trusted-interpreter: refused: declaration-duplicate`; malformed grammar, non-exact versions including `latest`, prefix or suffix lookalikes, and metacharacter-bearing values each assert `trusted-interpreter: refused: declaration-malformed`. Every case exits 2 with no interpreter stdout and no marker.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:145:- `test_missing_or_nonexact_declaration_is_refused`: in the temporary repository copy, an absent declaration asserts `trusted-interpreter: refused: declaration-missing` and `latest` asserts `trusted-interpreter: refused: declaration-malformed`, both with exit 2, no interpreter stdout and no selection of an installed version.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:146:- `test_program_entry_refuses_dirty_environment_or_symlinked_script`: invoke the program with exported functions, `BASH_ENV`/`ENV`, `LD_PRELOAD` and `LD_AUDIT` naming a marker-library path, planted PATH, a forged sanitization sentinel and a symlinked `$0`; dirty-entry cases assert `trusted-interpreter: refused: dirty-environment` and the symlinked-script case asserts `trusted-interpreter: refused: script-path`, each with exit 2, no interpreter stdout and no marker. The trusted-parent clean-prefix success assertion uses the read-only positive case above, with the real repository’s canonical script path and no marker. For direct dirty-entry refusal tests use a non-loadable marker-library path; a loadable library can execute before the script, so test its absence only with the trusted parent's pre-exec clean environment, never as a shell-entry guarantee.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:147:- `test_forged_home_is_refused`: set HOME to a forged directory containing a marker-writing interpreter at the expected mise layout, retaining an otherwise allowed environment; assert exit 2 with `trusted-interpreter: refused: home-mismatch`, no interpreter stdout and no marker before that interpreter can execute. The clean-prefix success assertion with the real uid's passwd home is the read-only positive case above.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:149:`install-symlink` and `install-not-regular` cannot be exercised in CI or by the worker (implemented, refuses by code, verified by reading). Their threat-table row remains `residual`, not `closed`. Do not manufacture symlinked, non-regular, forbidden-root or case-aliased installed candidates under the real passwd home, redirect its install root, or count an earlier refusal as runtime coverage of these checks.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:151:Extend `tests/unit/test_ci_rerun.py::CiRerunTest::test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment`, currently at line 273, with the marker-writing **`python3`** in `.venv/bin` **prepended to PATH**, with mise unavailable. Assert dirty entry exits 2 with `ci-rerun: refused: dirty-environment` and no marker or rerun; then, in a CI-provisioned successful consumer fixture as specified below, use the trusted-parent clean prefix and assert the marker is absent and that the real pinned installation permits exactly one rerun with the pinned interpreter. Also cover safe refusal in a temporary repository copy declaring an exact version whose real passwd-home installation is confirmed absent, asserting the propagated `trusted-interpreter: refused: install-missing` code without modifying that installation.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:153:Retain and adapt `test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path` and `test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin`; their assertions must exercise the new trusted-path contract rather than preserve acceptance of arbitrary PATH wrappers or the removed shims mechanism. Add `test_ci_rerun_executes_as_a_sanitized_program` for exported functions, `BASH_ENV`/`ENV`, `LD_PRELOAD` and `LD_AUDIT` naming a marker-library path, planted PATH, the forged-sentinel case, forged HOME and a worker-owned symlinked `$0`; assert `ci-rerun: refused: dirty-environment` for hostile environment inputs, `ci-rerun: refused: home-mismatch` for forged HOME and `ci-rerun: refused: script-path` for symlinked `$0`, each with exit 2, no marker and no rerun. Apply the same non-loadable-path limitation to direct dirty-loader refusal cases; with a loadable marker library, only the trusted-parent clean-prefix case asserts no marker. Clean-prefix execution in a CI-provisioned successful consumer fixture with the canonical script path and real passwd home must still use the pinned interpreter for both Python invocation sites and permit the expected rerun.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:155:Add these tests to `tests/unit/test_ci_rerun.py::CiRerunTest`. Each destination test starts from an accepted baseline: a temporary copy of the repository tree whose own `scripts/orchestrator/ci-rerun.sh` is executed as the program through the trusted-parent clean prefix. The copy must be the program's confirmed repository root, with its registry, ledger and reservation paths accepted; make one positive assertion of exit 0 and the expected fixture-only behavior first. The CI runner provisions these temporary copies outside the forbidden worker/cache/tmp roots, using the real pinned installation read-only; the sandboxed worker records blocked local evidence when that baseline is unavailable. Executing the original script against paths in another temporary tree is not an accepted baseline.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:157:For each independent negative invocation, restore the accepted baseline state and apply exactly one mutation: an otherwise in-root symlink at the destination or a parent (including a symlinked ledger and a symlinked reservation parent), a case-aliased in-root pathname (including the registry on a case-insensitive filesystem), or a parent redirected to a path outside the copy, including worker-writable cache and temporary destinations. Assert exactly `ci-rerun: refused: destination-symlink`, `ci-rerun: refused: destination-case-alias` or `ci-rerun: refused: destination-outside-root`, respectively, as well as exit 2, no registry parsing, no ledger append or reservation change, no rerun and an untouched target compared with its state immediately before the mutation. Keep symlink and case-alias subcases otherwise contained so an earlier containment refusal cannot satisfy them. Report an explicit skip for the case-alias subcase on a case-sensitive filesystem; do not claim that subcase ran.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:159:- `test_ci_rerun_refuses_unsafe_flake_registry_destination`: exercise all destination-refusal subcases for `.github/flakes.yaml`.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:160:- `test_ci_rerun_refuses_unsafe_ledger_destination`: exercise all destination-refusal subcases for `.orchestration/validation/ci-reruns.tsv`, including a redirected ledger parent.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:161:- `test_ci_rerun_refuses_unsafe_reservation_destination`: exercise all destination-refusal subcases for `.orchestration/validation/ci-reruns.lock.d` and an existing per-run reservation, including a redirected reservation parent.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:162:- `test_ci_rerun_refuses_git_environment_inputs`: start with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` and `GIT_CONFIG_GLOBAL` pointing at planted locations in the outer environment, run through the trusted-parent clean prefix and assert that no `GIT_*` name survives at program entry, the confirmed root is the trusted fixture repository and the planted locations remain unused and unchanged. In separate subcases deliberately introduce each of those four names, plus another `GIT_*` name, after the prefix; the program must refuse at entry with exit 2 and `ci-rerun: refused: dirty-environment` before Git, registry reads, ledger or reservation access or any rerun.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:163:- `test_ci_rerun_refuses_repository_local_core_worktree`: set `core.worktree` in the fixture repository's local configuration to a planted worktree, invoke the consumer through the trusted-parent clean prefix with no `GIT_*` names and assert exit 2 at root confirmation with `ci-rerun: refused: repository-root`, before registry reads, ledger or reservation access or any rerun; the planted worktree remains unchanged.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:165:The positive resolver case reads the real repository and real installation read-only; it does not copy or rewrite the declaration, provision an installation, or create a repository outside the worker boundary. Every executable negative case, including forged HOME, malformed declaration, dirty environment, planted PATH and redirected destinations, uses temporary fixtures; declaration mutations use repository copies, and destination mutations require the accepted copied-repository baseline above. No negative case modifies the real passwd-home installation; symlinked and non-regular installation checks remain residual and are verified by reading. The passwd-home lookup always remains anchored to the real uid: do not substitute an account database, intercept that lookup, redirect the install root, or add a test seam that bypasses it.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:167:The inspected unit-test workflow `.github/workflows/test.yaml`, job `test`, has the existing mise setup step `Setup mise for statusline smoke` using `jdx/mise-action`, followed by `Install statusline tools` and later `Run Python unit tests`. The setup currently has `install: false`, and the listed tool-install commands do not install Python. Before dispatch, the orchestrator must arrange through a separate authorized prerequisite that this existing mise setup provisions the repository’s exact pinned Python under the runner’s real passwd-home mise install root before the Python tests. This task does not authorize workflow edits or worker writes beneath that root. CI runs the positive resolver case against its real checkout outside forbidden roots and its actual mise installation; it must record a passing case, not a missing-installation skip, for acceptance.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:169:Successful consumer fixture repositories outside worker/cache/tmp roots are created and exercised by the CI runner, using the same real pinned installation read-only; the sandboxed worker must not provision them or modify the real repository, installation or protected cache. Copy the resolver beside the consumer only in fixture repositories, supply fixture declarations there, and execute both scripts as programs through the trusted-parent clean prefix except for the explicit refusal cases. Obtain the successful consumer assertions’ red/green evidence in CI; record any locally unavailable fixture as blocked local evidence rather than claiming a pass or weakening the write boundary. Adapt fake-gh fixture data delivery to the clean environment; do not add production environment exemptions, executable-directory parameters or test-only resolver bypasses. Keep every existing behavioral assertion and keep all fixture calls off live GitHub.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:177:Test budget: the retained a02 test delta is `67 + 1 = 68` changed lines, plus about `130` for resolver tests including parser, forged-HOME, dirty-entry and reason-code cases, `110` for consumer regressions and clean-prefix fixture migration, and `90` for the three destination tests and two hostile-Git regressions, giving `68 + 130 + 110 + 90 = 398`, with `22` lines of allowance and a resulting cap of **420 changed lines under `tests/`**.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:183:Retain the predecessor’s checks: `make unit-test`, `make format`, ShellCheck and repository-style `shfmt -i 4 -sr -d` on the changed shell scripts, and the workflow-orchestration, workflow-security and ci-rerun unit modules. Add the trusted-interpreter module, the new startup and hostile-PATH cases, and the changed-file comparison lint. Do not run bats locally.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:187:After pushing, paste `gh run list --branch tools/ci-efficiency-followup-a02 --json name,event,conclusion` and final-head required-check evidence, showing the seven required contexts and no pull-request private-bootstrap run.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:203:Write current `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence under `.orchestration/dotfiles-T133-ci-efficiency-followup-a04/`. Record the predecessor head, exact final head and base, branch, PR, changed files, row-to-test mapping, red/green commits, cap totals, evidence paths and `task_copy=<sha256 of .orchestration/dotfiles-T133-ci-efficiency-followup-a04/task.md>`. Preserve historical claims as historical; they do not approve the new head.
.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md:213:Every `gh` command and every `git` write is an individual command **inside the sandbox**, including pushes and authenticated fetches. No compound write commands, outside-sandbox retries, excluded-command workaround, permission escalation or alternate tool to bypass a denial. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-ci-efficiency-followup-a04 status=blocked` naming the exact command, failure and crossed boundary; preserve the evidence and wait.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:34:  - control: "home/dot_agents/agent-config.yaml (trusted checkout and interpreter bindings, static trusted_paths inventory, distinct worker policy, managed sandbox policy and worker caches)"
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:37:    disposition: "residual: the user baseline preserves orchestrator functions within the managed sandbox policy; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the specified changes and retained settings; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision executes the rendered PermissionRequest under the system-only PATH and checks every rendered hook entrypoint."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:40:  - control: "home/.chezmoitemplates/claude-managed-settings.json (admin-required sandbox enforcement, fixed rendered control-plane exclusions and Herdr socket allowance)"
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:41:    disposition: "residual: operator installation establishes the documented enforcement scope against project and local sandbox relaxation; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox asserts the rendered keys; shared control-plane capabilities and same-UID host access remain residual."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:54:  - control: "scripts/validate-agent-assets.py (consolidated item 16: exact platform-symmetric excludedCommands at base lines 349-355; native per-host binding expansion in render_template_text before structural sanitized Claude PermissionRequest wiring at base lines 1193-1200; enumeration and preservation of the other managed Claude settings, hook-composition and sandbox checks)"
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:55:    disposition: "residual: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form covers the two exclusion fixtures; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_render_template_text_expands_native_bindings checks expansion from the same binding source as both modify scripts before JSON parsing and the structural check; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate covers shlex parsing, the exact clean prefix, absolute uv and Python bindings, the fixed offline/no-cache uv arguments, the installed permgate script and sole claude argument, malformed or additional words and retained ccgate refusal; the Codex wiring check remains unchanged, and rendered-content validation does not establish live enforcement."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:60:  - control: "home/dot_local/bin/common/executable_herdr-agent-state.sh (repository-owned Herdr state helper with an explicitly supplied absolute Python interpreter)"
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:61:    disposition: "residual: binding the helper and its Python child reduces shim execution; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters checks executed identities with planted shims."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:63:    disposition: "residual: the sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks its replacement; shared managed control-plane capabilities remain available and are not represented as per-seat isolation."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:66:  - control: "tests/unit/test_generate_agent_configs.py (separate platform policies, static inventory, interpreter bindings, tracked hook coverage and item 16's literal-form PermissionRequest assertions)"
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:68:  - control: "tests/unit/test_validate_agent_assets.py (consolidated item 16: the macOS gh-exclusion and Linux extra-exclusion fixtures, valid_claude_sandbox's exact required exclusions, the literal-form hook fixture, native-binding rendering and the structural PermissionRequest cases)"
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:69:    disposition: "residual: tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_accepts_manifest_symmetric_settings, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_rejects_each_broken_rule, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_requires_extra_codex_writable_roots, tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs and tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs exercise the corrected shared sandbox fixture; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_hook_composition_requires_permgate_first and tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate cover the hook contract; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_render_template_text_expands_native_bindings checks native expansion before the structural check and render/runtime test without claiming live enforcement."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:77:    disposition: "residual: fixtures verify the selected documented enforcement keys and staging behavior; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision checks every rendered hook entrypoint and executes the real dependency-free permgate through bound uv/Python under PATH=/usr/bin:/bin, without simulating proof of Claude runtime enforcement or performing sudo installation."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:83:    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, outputs, statuses and tested revisions without credentials or unmasked home-directory paths."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:90:  - control: workflow and interpreter or environment inputs
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:91:    disposition: "residual: absolute interpreters, Python -I, sanitized Git, fixed hook PATH and trusted executable bindings reduce environment injection; the host, native loader and same-UID processes remain outside this task's security guarantee."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:93:    disposition: "residual: the worker settings modify script, orchestrator-only guard and repository-owned Herdr state helper have named source and installed paths; RESULT inventories their interpreter and descendant bindings without introducing a worker-write-boundary hook or gh wrapper."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:95:    disposition: "residual: host controls reduce accidental and injected damage without isolating seats sharing one OS user; prevention of worker-initiated merges requires a separate OS user or host under D-024-23's future P1-16, which the operator decides; the GitHub boundary is detection, not prevention, through P1-11's regime check in the next records PR for missing acceptance or gate evidence; shared managed control-plane exclusions and the Herdr socket remain residual."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:97:    disposition: "residual: dedicated configuration, static symlink-aware Edit denies including worktree configuration and orchestrator worklogs and caches, narrow writable agmsg stores, managed sandbox enforcement and failIfUnavailable true reduce damage; documented path checks do not establish atomic immunity to concurrent path swaps."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:101:    disposition: "residual: canonical anchor and interpreter checks reduce worker-selected trusted paths and account for symlink components and filesystem case aliases; other consuming-helper checks remain with their owning hardening tasks."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:107:    disposition: "residual: guarded tracked and main-local project hooks and minimal worker user hooks reduce host execution routes; shared managed Herdr socket access, control-plane exclusions, approved external processes and same-UID processes outside every seat sandbox remain residual."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:111:    disposition: "residual: the regime reads the ledger through the GitHub contents API at the SHA returned by git ls-remote origin refs/heads/main; P1-14 a05 implements that read, and local refs, files and object traversal provide no approval authority; the GitHub boundary is detection, not prevention."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:113:    disposition: "residual: per-seat worker caches, restricted worker write allowances and explicit denies on the orchestrator worklog and uv-cache reduce cache poisoning; consuming hardening tasks use the protected orchestrator cache with --offline and execute no worker, shared uv or mise cache content."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:114:  - control: "5.14 item 10: no worker command outside the sandbox"
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:115:    disposition: "residual: empty worker user exclusions and disabled unsandboxed requests reduce escape routes; the worker rule forbids using shared managed control-plane exceptions, whose availability and Herdr socket access remain residual; the deterministic Codex permgate rule and live deployment remain operator steps."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:119:    disposition: "residual: every seat writes the store, and installed storage.sh resolves drivers.partition as a driver path and sources it during unsandboxed delivery; it also uses db/trusted-plugins to authorize plugins/partition/shared.sh for sourcing; fixed PATH does not stop these routes; worker denies on plugins/** and db/trusted-plugins reduce the plugin route; dotfiles-T133-agmsg-hardening-a01 owns upstream basename validation, plugin authorization hardening and their adversarial red-then-green tests; this task introduces no store-derived sourcing beyond the installed scripts' current behavior."
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:126:premises:
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:128:      The historical a05 premises carried by the preceding text describe its recorded observations. They do not require this worker to rebuild PR 400, edit the approval ledger or implement P1-14 a05.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:133:      D-024-21 establishes the host threat model and dedicated Claude worker configuration. D-024-23 supersedes D-024-22's credential-separation claim because gh Keychain access is shared by seats running as the same macOS user. Prevention requires a separate OS user or host; the current GitHub boundary is detection, not prevention.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:145:      The current launcher constructs worker profile options separately from the pane environment. The dedicated Claude configuration directory and private cache variables reach the actual worker process on every launch route. This task adds no gh configuration directory or credential-separation mechanism.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:158:      Managed sandbox.enabled true, failIfUnavailable true and allowUnsandboxedCommands false establish the documented admin-required enforcement scope. Project and local settings cannot supply sandbox relaxations in that scope. User settings and shared managed exceptions remain distinct from project and local settings.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:160:      - https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:175:This is the amendment-5 text of the task dispatched at 2026-10-19T05:42Z (the ninth-round text that passed its pre-dispatch security review). Amendment 1 folds in two interpretation notes the worker needed (the inherited make format clause; the portable tracked `.claude/settings.json` with host-specific paths only in the rendered guard) and removes the Codex worker profile item (a Codex seat edits no Codex-boundary source; it becomes the separate Claude-seat task dotfiles-T133-codex-worker-network-a01). Everything else is the dispatched text in meaning; the branch, the eight green tests and the fixtures stay; the worker swaps the task copy to this text at its next push.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:177:The host is not a security boundary between seats sharing one OS user. gh keys Keychain credentials by host and user, so a worker running as the same macOS user can read the orchestrator's token regardless of `GH_CONFIG_DIR`. Prevention of a worker-initiated merge requires a separate OS user or host under D-024-23's future P1-16, which the operator decides whether to pursue. Until then the GitHub boundary is detection, not prevention. The regime detects missing acceptance or gate-passage evidence in the next records PR, not at main-push time, because the records reach main only with that boundary PR. On a PR touching `.orchestration/acceptance/**`, the regime job checks every main merge commit since the previous boundary for its corresponding acceptance record with gate-passage evidence and fails the PR when one is missing. P1-11 owns implementation of that check; this task states section 5.14 item 0's detection rule. Approvals and gate evidence of record are read from GitHub at a SHA through its API inside the sandbox. Host-local controls reduce accidental and injected damage without establishing isolation from a malicious same-UID process.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:179:This task implements section 5.14 items 1, 9 and 10 through a dedicated Claude worker configuration directory, static Edit deny rules on trusted paths and worktree configuration, managed sandbox enforcement, guarded project hooks, hook interpreter and PATH bindings, private worker caches and the rule that worker commands run inside their sandbox. Every Claude seat has `sandbox.failIfUnavailable: true`.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:181:The administrative managed policy is shared by every Claude seat. Its Herdr socket allowance and three control-plane exclusions remain available to workers as well as the orchestrator. Empty arrays in worker user settings do not subtract these managed entries. Their availability is a residual under item 0, and the worker execution rule supplies no authorization to use them outside the sandbox.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:185:The design source is `.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:189:> 5.14 item 1: Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。 worker 設定：除外コマンド無し、Herdr socket 無し、sandbox の allowWrite は自席 worktree と agmsg store と席別キャッシュだけ、`failIfUnavailable: true`、信頼パス（anchored checkout の `.claude/worktrees/` 以外、`~/.agents`、`~/.claude*`、`~/.local`、`~/.config`）への Edit deny（公式文書：file tool の permission 検査は要求パスと symlink 解決後のパスの両方に deny を適用し、symlink そのものへの書き込みは拒否する）、sandbox の強制範囲はユーザー設定ではなく **managed settings**（`/Library/Application Support/ClaudeCode/managed-settings.json`、公式文書 "Repository settings under an admin-required sandbox"：project/local 設定は sandbox を無効化したり除外・socket を足したりできない）に置く。 hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。 `failIfUnavailable: true` を全席に置く。
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:193:> 5.14 item 9: orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。 `UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:195:> 5.14 item 10: worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:197:D-024-21, D-024-23 and the amended items 0, 1 and 8 govern this revision. D-024-22's proposed gh credential separation is superseded. The acceptance record preserves documentation facts and earlier proposals as history.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:199:The third C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-ecc7ab5.md.last.md`. Its five P1 findings remain recorded. The retained mechanisms are documented symlink-aware deny rules, approval reads outside the local object database, hook interpreter bindings and runtime hook failure policy.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:203:The fifth C-80 text review is `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-08e6ac7.md.last.md`. Its three P1 findings remain recorded. This revision removes the gh credential-separation mechanism, records the upstream agmsg store-driver residual and moves sandbox enforcement into administrative managed settings.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:205:The file-tool rule is the documented sentence, “Deny rules: apply when either the requested path or the file it resolves to matches.” Edit and Write refuse a requested file that is itself a symlink. Directory symlinks are subject to resolved-target permission checks, and the tools check the resolved location again when opening the approved file. These documented checks reduce redirection risk without establishing an atomic host security boundary against concurrent same-UID changes. [Claude permission reference](https://code.claude.com/docs/en/permissions#symlinks)
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:207:The 2026-10-19T03:45:06Z sandbox probe ran `gh api repos/mryfmo/dotfiles --jq .name` and returned `dotfiles`. The recorded sandbox proxy used CONNECT without TLS interception, and gh read the Keychain token. This historical observation confirms neither credential separation nor final-head deployment readiness.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:209:The documentation facts recorded at 03:2xZ establish that Edit denies also affect the Bash sandbox, hooks reload during a session and an unavailable sandbox is fail-open by default. D-024-21's 04:0xZ decision establishes the dedicated Claude configuration mechanism, directory-specific Claude credentials, symlink coverage and `onFailure: "block"` support. These Claude credentials do not separate gh Keychain access.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:217:   The manifest names `orchestrator_checkout` as the anchored primary checkout and supplies trusted deployment bindings for the guard, hook scripts and absolute interpreters. Both user-settings renders use the same `claude.execution` bindings: resolve Python from `claude.execution.tool_paths.python3`, the trusted source behind `claude.execution.python`, and add the missing `claude.execution.tool_paths.uv` binding for the installed uv binary. Render their resolved absolute executable files, not PATH lookups or a private link whose creation depends on an earlier hook. These bindings resolve outside worker worktrees and executable caches. Worker cwd, tool input, worktree configuration and inherited command variables do not select them. The manifest also supplies the trusted bindings from which the render resolves the absolute directories holding `ruff`, `prettier` and `terminal-browser`, without using mise shims.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:225:   The home-path denies are `~/.agents/agent-config.yaml`, `~/.agents/model-profiles.env`, `~/.agents/skills/**/scripts/**`, `~/.agents/skills/**/SKILL.md`, `~/.agents/skills/agmsg/plugins/**`, `~/.agents/skills/agmsg/db/trusted-plugins`, `~/.claude/**`, `~/.claude-worker/**`, `~/.local/bin/**`, `~/.local/share/**`, `~/.local/state/**`, `~/.local/share/mise/**`, `~/.config/**`, `~/.cache/uv/**` and `~/.local/share/uv/**`. No blanket deny on `~/.agents/**` or `~/.local/**` replaces this list.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:227:   The agmsg store paths `~/.agents/skills/agmsg/db`, `~/.agents/skills/agmsg/teams`, `~/.agents/skills/agmsg/run` and `~/.agents/skills/agmsg/ext-tools` remain writable. Deny patterns cover neither these directory targets nor their descendants except the file `~/.agents/skills/agmsg/db/trusted-plugins`. Edit denies merge into the sandbox configuration, so Bash writes to that file and `~/.agents/skills/agmsg/plugins/**` are refused too. Their influence on installed delivery-script driver and plugin selection remains the separately owned agmsg residual.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:229:   The orchestrator retains its existing permissions, cache allowances and hook functions within the administrative managed policy. Its user baseline receives `failIfUnavailable: true`, `onFailure: "block"` on its hooks and the interpreter and PATH bindings below. Its exclusion entries match the three control-plane entries specified below; the former Linux `gh *` exclusion is removed.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:231:   The worker user policy contains no excluded commands and sets `allowUnsandboxedCommands: false`. It contains no Herdr socket allowance and no allow-all Unix socket switch. Its sandbox is enabled and has `failIfUnavailable: true`. Shared managed entries remain effective despite these empty worker arrays.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:233:   Worker `sandbox.filesystem.allowWrite` contains only the existing agmsg store paths and per-seat cache paths. The worktree is the project root and supplies its ordinary project write root. Shared uv and mise write allowances are not copied into worker settings.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:235:   Existing model selections, Codex worker profile values, Codex sandbox and approval arguments and Codex shared Git grants retain their meaning and remain unchanged. The deterministic Codex permgate rule that stops approving sandbox escapes is an operator step.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:243:   Edit denies cover Write, MultiEdit and NotebookEdit through Claude's permission system. Requested-path and resolved-target matching supply the documented symlink coverage. The generator creates no `executable_worker-write-boundary.py` or replacement PreToolUse path validator.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:263:   In `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest`, add `test_modify_private_settings_renders_native_bindings_before_merging` using the actual generated native binding expressions, temporary homes and executable paths containing spaces; `test_permission_merge_upgrades_legacy_permgate_to_bound_hook` for the legacy-to-bound upgrade; `test_permission_merge_replaces_previous_bound_hook_idempotently` for old-to-new absolute uv/Python bindings and byte-identical re-merge; and `test_permission_merge_does_not_classify_foreign_hook_as_managed` for foreign-script and malformed or extended bound commands. Extend `test_permission_merge_preserves_unrelated_current_hooks` and `test_permission_merge_preserves_custom_hook_in_mixed_entry` to retain custom hooks through these upgrades, and retain `test_managed_permgate_replaces_stale_current_ccgate_hook`. Record red-then-green evidence for each named selector.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:267:   The orchestrator retains its current user policy content apart from `failIfUnavailable: true`, `onFailure: "block"`, the required interpreter and PATH bindings and alignment of exclusions with the three control-plane entries. Worker-specific Edit denies and restricted worker cache allowances do not enter this baseline. Administrative sandbox requirements apply to the orchestrator as well as workers.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:269:   Every generated hook entry carries `onFailure: "block"`. Every generated command hook starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` before its trusted installed entrypoint, except that this chezmoi template renders PermissionRequest HOME as `HOME="{{ .chezmoi.homeDir }}"`. The prefix re-exports HOME before any HOME-relative entrypoint path. Host-specific interpreter, private-link-directory, anchored-checkout and tool-directory bindings remain in the per-host rendered user settings and guard. The formatter and project-map hooks run through the installed orchestrator-only guard and receive the role-specific pinned PATH specified below. Merge evidence identifies hooks appended by the existing modify script and distinguishes them from generated baseline entries. The report accounts for the effective deployed hook set without equating baseline coverage with coverage of runtime-added entries.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:273:   Every other rendered hook command, including SessionStart, Stop, delivery and guard invocations, likewise uses absolute bound entrypoints and interpreters and never relies on PATH to select uv, python3, bash or a tool; upstream agmsg env-bash descendants retain the fixed system-PATH binding in item 11.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:279:   It renders the static trusted-path Edit denies, the worktree `.claude` and `.mcp.json` Edit denies, retained native merge denials, empty user `excludedCommands`, `allowUnsandboxedCommands: false`, restricted `allowWrite`, no user Herdr socket allowance and `failIfUnavailable: true` for both Darwin and Linux.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:283:   Every worker hook entry carries `onFailure: "block"`. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}" AGMSG_RESOLVE_PROJECT=0` before the selected absolute shell interpreter and absolute installed agmsg script path. The prefix also re-exports `AGMSG_STORAGE_PATH` when it is set in the launcher environment. Project resolution from a writable `run/proj.<pid>.project` marker remains disabled, so delivery retains the explicit worker path. Descendants inherit this PATH.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:289:5. `home/.chezmoitemplates/claude-managed-settings.json` supplies the administrative sandbox policy.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:291:   The rendered policy sets `sandbox.enabled: true`, `sandbox.failIfUnavailable: true` and `sandbox.allowUnsandboxedCommands: false`. The last setting makes sandboxing admin-required. Project and local files cannot add sandbox exclusions, socket allowances or other documented relaxations in this scope. Managed Boolean values prevail over lower scopes. User settings remain a separate trusted scope, and arrays such as exclusions have no general managed-only lock. [Repository settings under an admin-required sandbox](https://code.claude.com/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox)
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:293:   The rendered policy sets `sandbox.filesystem.disabled: false`, `sandbox.enableWeakerNestedSandbox: false`, `sandbox.enableWeakerNetworkIsolation: false`, `sandbox.network.allowAllUnixSockets: false`, `sandbox.network.allowLocalBinding: false` and `sandbox.allowAppleEvents: false`.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:295:   The rendered `sandbox.excludedCommands` list contains exactly `agmsg-dispatch *`, `herdr-agents *` and `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These are the orchestrator's three control-plane entries. It contains no `gh *`, `git push *` or authenticated-fetch exemption.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:297:   The rendered `sandbox.network.allowUnixSockets` list contains exactly the trusted home expansion of `~/.config/herdr/herdr.sock`. This allowance is shared by every seat under managed settings. Per-seat removal is unavailable in that scope, and the worker baseline's empty list does not revoke it.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:299:   Shared control-plane exclusions are also available in worker sessions. The worker execution rule forbids using them to leave the sandbox. The text treats their availability and the socket's host-execution capability as item 0 residuals rather than enforced per-seat separation.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:301:   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox` asserts the rendered content, exact exclusion and socket lists, trusted home expansion and every required Boolean value.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:303:   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings` supplies project and local fixtures that disable sandboxing, disable startup failure, enable unsandboxed retries, add exclusions and sockets, enable weaker isolation and widen filesystem writes. The trusted managed render remains unchanged. The test verifies configuration scope and content without presenting a simulated settings merger as runtime enforcement.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:309:   The target selects `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux and prints the exact command `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` with the actual staging path and detected destination substituted and shell quoting preserved. The printed command is ready for the operator to run.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:313:   `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo` covers both macOS and Linux, uses a temporary home, verifies the staged JSON and exact printed command with the detected destination, includes a home path containing spaces and asserts that a planted sudo marker remains absent.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:319:   Worker permissions, sandbox policy and hooks managed by this renderer replace stale managed values. Permissive old user exclusions, socket allowances, hook commands and shared cache allowances do not survive as additive worker user policy. The script does not read or copy `~/.claude/settings.json`.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:321:   Rendering handles empty and malformed input through the repository's existing baseline behavior and is idempotent. It neither reads credentials nor initiates authentication.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:327:   Chezmoi renders the installed guard per host. Its rendered absolute shebang selects the trusted shell interpreter. The host-specific absolute interpreter paths, private executable-link directory, anchored checkout and tool directories are bound inside this rendered guard and the rendered user settings. The tracked project settings contain none of these paths.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:329:   The guard compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Equality executes the fixed operation supplied by the caller through the guard's trusted interpreter and anchored-script bindings, subject to the formatter and project-map tool-input check below. Every other launch root exits 0 without executing it. `CLAUDE_PROJECT_DIR` supplies launch identity and never selects an executable.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:335:   The guard preserves argument boundaries, stdin and child exit status. It performs no eval, PATH interpreter lookup or worktree-relative script selection. Its portable caller starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`. The prefix re-exports `HOME` from the launcher environment as `HOME="$HOME"` before any path that uses it and explicitly re-exports the launch identity and the few variables Claude Code documents for hooks. No interpreter or anchored script path is supplied by the tracked settings.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:337:   The pinned PATH differs by role. Worker-session hooks use `/usr/bin:/bin`. For the orchestrator's formatter and project-map hooks, which the guard runs only in orchestrator sessions, the guard itself sets PATH to a rendered list of absolute tool directories of the trusted root before executing the guarded command. Those directories hold `ruff`, `prettier` and `terminal-browser` and are resolved by the render from the manifest without using mise shims. The formatter and project-map scripts remain outside `allowed_files` and unchanged.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:339:   `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads` plants worker Stop, contextdb and formatter payloads. Worker and unrelated-root invocations leave all markers absent. The positive-path case runs the complete rendered command in a subprocess with a fake `CLAUDE_PROJECT_DIR` equal to the anchored checkout and asserts that the guarded script executed while preserving its arguments and status. A second case runs the complete rendered command with a worktree `CLAUDE_PROJECT_DIR` and asserts that the guarded script did not execute. A planted `BASH_ENV` in the outer environment remains unexecuted in both cases. Formatter and project-map reload cases keep `CLAUDE_PROJECT_DIR` anchored and supply hook tool input for an outside file and a worker-repository file under `.claude/worktrees/`; both exit 0 with command and planted configuration markers absent. Matching anchored-file inputs run both commands normally. The guard tests execute the portable HOME-relative hook command against separately rendered per-host guards, assert the `HOME="$HOME"` re-export and verify that interpreter and anchor selection occurs only inside the rendered guard. Changing `CLAUDE_PROJECT_DIR` never changes the selected executable.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:341:9. `.claude/settings.json` retains its tracked project hooks and rewrites every command through the installed orchestrator-only guard.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:343:   This tracked file is not a chezmoi template and remains portable across hosts. Every command starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier with its arguments. The shell running the hook expands `$HOME`, and the clean environment re-exports the launcher's HOME before any path that uses it. The file names no interpreter, anchor path, private links directory or host-specific tool directory.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:345:   Host-specific absolute bindings live only inside the per-host rendered guard and rendered user settings, including the orchestrator user template's bound PermissionRequest invocation. The guard binds the selected operation to its absolute interpreter and anchored script path. Contextdb commands do not invoke bare `python3` or select `.claude/hooks` from a worker checkout. The Stop gate does not invoke bare `bash` or a worker checkout's `scripts/agent-stop-gate.sh`. `CLAUDE_PROJECT_DIR` never selects an executable.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:349:   `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure` traverses every event, matcher and command entry. It rejects unguarded commands, missing failure policy, missing `/usr/bin/env -i` prefixes with the specified HOME re-export, interpreter or anchor paths in the tracked file and worker-selected executable paths. Render fixtures use distinct homes and anchors and assert that the tracked commands stay identical while the guard and worker settings receive their own host bindings.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:353:    Every Claude worker pane starts with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`. This value reaches the actual worker process through the pane command and environment construction. Setting it only in the parent spawn process does not satisfy this requirement.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:355:    Managed-workspace and standalone-worker routes receive the same binding. Repeated starts do not inherit a conflicting caller Claude configuration directory. This task introduces no worker gh configuration directory, gh templates or credential-separation claim.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:361:    Before every Claude worker start, the launcher also migrates the legacy worktree-local file. Claude Code loads the worktree's own `.claude/settings.local.json` alongside the main checkout's local settings, so a previously generated delivery entry there would stay effective with its unsanitized environment and PATH-resolved interpreter. The launcher removes every managed delivery hook entry it previously wrote from `<worktree>/.claude/settings.local.json`, keeps that file's unrelated entries, and refuses to start the worker while a command hook it did not write remains there, naming the entry. The effective hook set is asserted across the three files Claude Code loads for a linked worktree (worker user settings, the main checkout's local settings, the legacy worktree-local file) with a fixture holding a previously generated unsanitized entry: `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks` is red at the base and green on the final head.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:365:    The launcher also regenerates its managed hooks in the main checkout's `.claude/settings.local.json`. Every local agmsg delivery and orchestrator attachment command that it writes runs through the installed orchestrator-only guard. The existing permissions object and unrelated non-hook settings remain stored. Their effective sandbox interpretation follows the administrative managed policy.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:367:    Every command hook in both `~/.claude-worker/settings.json` and the main checkout's `.claude/settings.local.json` starts with `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"`. Worker user settings contain their per-host rendered absolute interpreter and script bindings. Main-local commands invoke `"$HOME/.claude/hooks/orchestrator-only.sh"` with fixed operation identifiers, leaving host-specific executable bindings inside the rendered guard. The prefix removes inherited `BASH_ENV` before Bash starts and explicitly re-exports the launch identity and documented hook variables. Agmsg delivery prefixes additionally re-export `AGMSG_RESOLVE_PROJECT=0` and `AGMSG_STORAGE_PATH` when the latter is set in the launcher environment, so the clean environment does not re-enable project resolution from the writable `run/proj.<pid>.project` marker. Every entry carries `onFailure: "block"`. Main-local hooks loaded by a worker session execute no guarded payload.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:369:    Worker settings retain existing native merge denials. They add no user excluded commands, Herdr socket allowance, unsandboxed requests or orchestrator hooks. Shared managed exclusions and socket access remain effective.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:371:    Codex launches retain their existing `--sandbox workspace-write` and `--ask-for-approval never` arguments unchanged. This task changes no Codex worker profile or network-policy source and adds no network-policy test.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:377:    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_launch_adds_no_unsandboxed_route` checks that worker launch construction adds no outside-sandbox command route, worker user exclusions or socket allowances and retains native merge denials. It separately records the shared managed exceptions and does not claim that empty user arrays remove them.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:381:    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_settings_hook_has_system_path_prefix` exhaustively traverses both settings files after initial preparation and repeated starts. It asserts the literal `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix on every command hook, checks the split between absolute bindings in rendered worker settings and HOME-relative main-local guard calls, and asserts that a planted `BASH_ENV` in the hook's inherited environment does not run. The planted-`BASH_ENV` case is red against the current PATH-only form. The test also asserts `AGMSG_RESOLVE_PROJECT=0` in every agmsg delivery prefix and preservation of `AGMSG_STORAGE_PATH` when set in the launcher environment. It invokes the delivery resolver through the rendered prefix with an explicit worker path and a conflicting writable `run/proj.<pid>.project` marker and asserts that the resolver retains the explicit worker path.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:385:    The currently installed `~/.claude/hooks/herdr-agent-state.sh` is generated by Herdr and is not a tracked source in this repository. Its bare `python3` descendant is not retained as a trusted worker hook. The repository-owned helper preserves the required state-reporting function and receives its absolute Python interpreter through the rendered invocation.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:387:    Every hook command reaches a selected absolute interpreter and absolute script path through trusted installed bindings. The tracked settings name only the HOME-relative guard and fixed operation identifiers. Host-specific interpreter and anchor bindings reside inside the per-host rendered guard or rendered user settings. Repository-owned shell descendants use absolute shebangs or explicit absolute shell invocations. Direct Python descendants use the selected absolute interpreter with `-I`; PermissionRequest uses the bound uv/Python invocation in item 3.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:393:    The inventory records source ownership, installed path, caller, entrypoint interpreter and inherited PATH for each reached script. Binding only the first command does not establish descendant coverage.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:395:    The inventory separately records the current `storage.sh` route from writable team configuration to driver sourcing. A `drivers.partition` value such as `../../../db/payload` can select a planted driver file during unsandboxed delivery. Fixed PATH does not mitigate that selection. The upstream fix belongs to `dotfiles-T133-agmsg-hardening-a01` as recorded in the acceptance record's ownership section.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:399:    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters` executes the fixture hook routes with planted Python and Bash shims. It includes a directly executed descendant with an `/usr/bin/env bash` shebang, checks descendant markers and records actual interpreter identities and inherited PATH. Capturing launcher command strings alone does not satisfy this test. Its result does not close the store-driver residual.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:401:12. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the Worker Playbook step 4 sentence that lists outside-sandbox worker commands.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:403:    The replacement sentence is: “Every worker command, including gh, git push and authenticated git fetch, runs inside the worker's sandbox; no worker command runs outside it.”
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:405:    This sentence governs worker execution. Historical TLS, keyring, artifact-writing and delivery exceptions elsewhere in the playbook provide no authorization to leave the sandbox. Shared managed control-plane exceptions provide no worker authorization either. An unavailable operation produces a blocked PONG with its exact command and boundary.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:407:    `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox` checks the replacement and removal of the former three-command exception sentence.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:411:    Section 5.14 item 9 fixes trusted orchestrator consumers to `UV_CACHE_DIR=<anchored-checkout>/.agents/worklog/uv-cache`, places managed Python installations beneath that cache and uses `--offline`. Those consumers execute no dependency content from worker caches, shared uv caches or mise caches. Their owning hardening tasks implement the consumer changes.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:415:    This task's hooks use standard-library Python and absolute shell interpreters; PermissionRequest alone invokes the existing dependency-free permgate through the absolute uv/Python binding with `--offline --no-cache` specified in item 3. The existing `.agents/worklog/` ignore covers the orchestrator cache.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:423:    Managed settings tests cover the exact rendered policy, conflicting project and local sandbox relaxations, shared control-plane exclusions, shared Herdr socket access and staging without privileged execution. They distinguish worker user settings from the effective shared policy.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:425:    Path fixtures cover symlink components and filesystem case aliases. They verify inventory and configuration identities without presenting a simulated permission matcher as proof of Claude runtime enforcement.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:427:    Hook tests cover every generated and tracked entry's failure policy, worker user settings, guarded main-local settings, the `/usr/bin/env -i` prefix with explicit hook-variable re-exports, complete rendered-command positive and worktree-negative cases, role-specific pinned PATH bindings, suppression of a planted inherited `BASH_ENV` and actual descendant execution. They distinguish synchronous policy hooks from background delivery and post-action events.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:429:    `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_hooks_bind_executables_and_permgate_returns_decision` renders the complete orchestrator and worker user hook sets and the guard in a temporary HOME, reusing the tracked and launcher-generated hook fixtures for SessionStart, Stop and delivery. For every command hook, expand only the fixture's known HOME and hook-variable bindings, parse with `shlex`, and assert that the first word is an absolute path to an existing executable file; for `/usr/bin/env -i`, also assert the first word after all environment assignments is such a file. Check the guard's rendered shebang, interpreter and fixed-operation executable bindings too, so no bare uv, python3, bash or tool survives. In the same test, install the unchanged real permgate source and a minimal deterministic fixture policy beneath that temporary HOME, then execute the rendered PermissionRequest command with the actual bound uv and Python binaries, outer `PATH=/usr/bin:/bin` and a fake PermissionRequest payload matching the fixture policy. Assert exit 0, parse stdout and assert `hookSpecificOutput.hookEventName == "PermissionRequest"` and the expected `hookSpecificOutput.decision.behavior`; empty stdout, exit 127 or `env: uv: No such file or directory` fails. A fake uv or permgate that merely prints a decision does not satisfy this test. Record red-then-green evidence for this selector.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:435:15. `.orchestration/dotfiles-T133-worker-write-boundary-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:439:16. `scripts/validate-agent-assets.py` is the consolidated validator scope for every existing check affected by this task's rendered Claude settings, hooks, sandbox and exclusions, with their corresponding fixtures and assertions.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:443:    The Linux and macOS `excludedCommands` checks at base lines 349-355 become one exact ordered-list check on both platforms: `agmsg-dispatch *`, `herdr-agents *`, `{{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *`. The last entry becomes `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *` after chezmoi expansion. Neither platform permits `gh *` or an additional, missing, reordered or substituted exclusion. The existing non-empty-string list validation remains. This follows the normative design sentences quoted above from `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 (C-86, C-88); the path is context only.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:445:    The Claude managed-user-settings hook-wiring check in `validate_model_profile_assets` at base lines 1193-1200 becomes structural. Inspect command hooks under `hooks.PermissionRequest`, not serialized text from other events, and parse the command with `shlex` without executing it. Require exactly the sanitized prefix from item 3 with HOME equal to the absolute home rendered from `{{ .chezmoi.homeDir }}`, followed in order by an absolute uv path whose basename is `uv`, `run`, `--no-config`, `--no-project`, `--offline`, `--no-cache`, `--python`, an absolute Python path matching the trusted rendered interpreter binding, `--script`, the absolute installed permgate path whose basename is `permgate`, and `claude`, with no further words. The uv and permgate paths also match their trusted rendered bindings. Compare parsed words so quoting of a bound path containing spaces is preserved; do not require a literal `permgate claude` substring. Missing or malformed commands, an incomplete or altered prefix, an extra environment assignment, relative or substituted executable paths, missing, reordered or additional uv flags, a different script or argument, a direct shebang-based permgate call, a guard selector, and trailing words or shell operations fail. The generated PermissionRequest command and its assertions conform to this bound-interpreter contract; the worker's current `orchestrator-only.sh permgate` selector does not satisfy it. Parsed tokens establish command structure; the render/runtime test in item 14 establishes that the executable binding actually runs under the sanitized PATH. The existing refusal of `ccgate` anywhere in the Claude hooks remains. The Codex PermissionRequest and `permgate codex` check at base lines 1189-1190, and its ccgate refusal, are unchanged because this task changes no Codex hook design.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:447:    The complete inventory of the surrounding checks is retained: `validate_claude_settings` still checks the schema, interactive model and effort, absence of the redundant model suffix and legacy type checker, the `format-edited-files.py` operation marker (still present in the guarded command), permission-allow list shape, sandbox policy, disabled unmanaged plugins and the Crit rule. `validate_claude_sandbox` still requires enabled and auto-allow booleans, a Boolean `failIfUnavailable` (the render tests separately require true), all agmsg and Codex writable roots, valid extra write paths, allowed hostname and telemetry restrictions, the platform Mach-service allowlist, no allow-all Unix sockets and valid socket paths; only its exclusion policy changes. `validate_hook_composition` retains duplicate-command rejection, permgate-first ordering, synchronous timeout budgets and the SessionStart `herdr-agent-state.sh` marker and order. These markers remain in the rendered commands, so none is deleted or weakened to accommodate the prefix. Generated-output freshness, manifest home-path checks, tracked project-settings portability, permgate policy and profile-asset checks and the orchestration home-path/secret scan remain unchanged. New worker-user and administrative-managed-policy outputs retain their exact content checks in the already named render tests; the orchestrator user sandbox validator is not applied to worker empty exclusions.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:449:    In `tests/unit/test_validate_agent_assets.py`, the two already authorized cases in `ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form` remain in scope: macOS gh exclusion and Linux extra exclusion. The shared `ValidateAgentAssetsTest::valid_claude_sandbox` fixture gains the exact three-entry exclusions above. Its callers `test_claude_sandbox_accepts_manifest_symmetric_settings`, `test_claude_sandbox_rejects_each_broken_rule`, `test_claude_sandbox_requires_extra_codex_writable_roots`, `test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs` and `test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs` retain their checks and reach the rule each intends to test. The literal-form fixture in `test_hook_composition_requires_permgate_first` follows the sanitized hook while retaining its ordering failure. Add `ValidateAgentAssetsTest::test_claude_permission_request_requires_sanitized_permgate` with valid quoted-path cases and negative cases for the structural contract and retained ccgate refusal. Keep red-then-green evidence and run `uv run python -m unittest tests.unit.test_validate_agent_assets -v` to green on the final head.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:453:The worker's before-amendment-4 measurements are 674 changed source lines, guard included, and 905 changed test lines (2026-10-19T08:21:22Z evidence at local head 55c125a1 on main 69dccca9); re-measuring that worker diff, including its pending validator/exclusion edits, gives the same totals. For amendments 4 and 5, estimate additional changed source lines as 45 for the generator/manifest uv/Python binding and native hook render, 45 for the structural PermissionRequest validator, 60 for the orchestrator modify script's native-binding renderer and managed-hook classifier, 25 for the identical renderer in the worker modify script and 25 for native expansion in the validator: `674 + 45 + 45 + 60 + 25 + 25 = 874`. Estimate additional changed test lines as 10 for `valid_claude_sandbox`, 90 for the hook-execution render test in item 14, 50 for the structural validator cases, 25 for the native-binding validator render fixture, 20 for the existing literal-form fixture/assertion adjustments and 90 for the native-binding merge fixture, legacy-to-bound upgrade, binding-upgrade/idempotence, custom-hook and foreign-hook merge fixtures in item 3: `905 + 10 + 90 + 50 + 25 + 20 + 90 = 1190`. The source cap therefore rises from 700 to 874 and the test cap from 950 to 1190, only to these estimated sums. All increments and totals count additions plus deletions, with the same generated-template exclusions as below. These are allocation estimates, not final-head measurements; the worker records final per-file numstat and both measured totals and does not raise either cap further without a measured sum requiring it.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:455:The guard source is `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl`: chezmoi renders the guard from its .tmpl source with the per-host absolute interpreter, anchored-checkout and tool-directory paths at apply time (a plain `executable_` source would be copied without expansion), and the render test renders the template with the test host values and asserts the paths it contains.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:461:The enumerated Codex consumers `home/.chezmoitemplates/codex-config-managed.toml`, `home/dot_codex/modify_private_config.toml` and `tests/unit/test_codex_config_merge.py` are unchanged: their PermissionRequest wiring, rendering and stale-ccgate migration use the separate `permgate codex` contract. `tests/unit/test_permgate.py` invokes the unchanged permgate source directly through Python and tests its payload, decision and policy contracts; it has no literal Claude managed-hook command-form assertion and is unaffected. `tests/unit/test_statusline_tools.py` calls the orchestrator's `render_managed_template` to read `statusLine.command`; its assertions concern the unchanged `ccusage statusline` and `ccstatusline` commands, not the PermissionRequest form, so it is unaffected and remains unchanged. `tests/fixtures/gate-evidence/pr-feedback-right.json` is historical PR-feedback disposition data mentioning the managed template; it asserts no managed-hook command form and is unaffected and unchanged. The enumerated `tests/unit/test_herdr_agents.py` and `tests/unit/test_agmsg_orchestration_docs.py` remain limited to their already authorized launcher and Worker Playbook changes: their template/PermissionRequest mentions add no literal-form assertion to this amendment. All consumers of the changed managed Claude hook form are consolidated in items 3 and 16; the existing in-scope manifest, generator, worker modify script and named generator, validator and merge tests follow that contract.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:463:The Codex worker profile change `sandbox_workspace_write.network_access=true` belongs to the separate task `dotfiles-T133-codex-worker-network-a01` for a Claude seat. This task contains no implementation, threat row or test for that change. This Codex seat edits no Codex-boundary source. The operator step for the deterministic Codex permgate policy remains named below.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:465:The worker-write-boundary Python hook, its hook entries and `tests/unit/test_worker_write_boundary.py` are dropped. The gh-trusted wrapper remains dropped. The worker gh configuration directory, its templates and the dedicated-identity implementation are removed from this task.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:469:The permission guard and merge gate remain P1-14 a05's work. P1-14 a05 and P1-6 implement the regime rule that approvals and gate evidence of record come from GitHub at a SHA through its API inside the sandbox. The GitHub boundary is detection, not prevention.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:471:For the committed approval ledger, the regime obtains the commit SHA returned by `git ls-remote origin refs/heads/main` and reads `gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. The consuming implementation reads the API response's file content at that exact SHA. It does not fall back to local files, local refs or local object traversal.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:477:Permgate code and deterministic policy remain the operator's responsibility. The worker prepares the operator step that stops the Codex permgate policy from approving sandbox escapes. The worker performs no live policy edit or escape probe.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:479:The operator logs into Claude once with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker` selected. The Claude Keychain entry is keyed to that directory. This Claude login does not authenticate or isolate gh.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:481:Administrative installation of `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux is the operator's step. The worker implements rendering, staging and the printed installation command without running sudo or installing live managed settings.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:483:The documented file-tool checks reduce symlink redirection risk. A same-UID process can race filesystem changes, alter host-local state or execute outside a seat sandbox. The remaining interval between permission checks and path consumption is a residual under section 5.14 item 0. This text makes no claim that the worker could already write every redirected target directly.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:485:The managed Herdr socket allowance stays available to every seat. Per-seat socket removal is unavailable in that shared scope. Shared control-plane exclusions, socket RPC, hooks, approved MCP processes and other processes outside every seat sandbox retain their stated host trust. The configuration is not represented as same-UID adversarial isolation.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:491:In `scripts/validate-agent-assets.py`, the consolidated policy-check changes enumerated in item 16 are in scope; unrelated validator behavior remains out of scope. In `tests/unit/test_validate_agent_assets.py`, the two exclusion cases, `valid_claude_sandbox`, the native-binding render fixture, the named hook fixture and structural-hook cases in item 16 are in scope; unrelated tests remain out of scope. The named literal-form assertions and fixtures in the already allowed generator and merge test modules are included as item 16 specifies.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:511:Managed render evidence asserts sandbox enablement, startup failure, disabled unsandboxed retries, the required anti-weakening Boolean values, exactly the three rendered control-plane exclusions and exactly the Herdr socket allowance. Conflicting project and local fixtures leave that render unchanged. The evidence names the documented enforcement scope without claiming live runtime verification.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:513:Staging evidence shows the home-directory output and exact printed `sudo install -m 0644` command with the detected administrative destination on both macOS and Linux. The temporary-HOME test proves that the target executes no sudo command.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:515:Hook evidence inventories every generated and tracked entry, its `onFailure` value, `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix (with template-rendered absolute HOME for PermissionRequest), installed script, absolute entrypoint interpreter and reached descendants. It includes the new render/runtime selector's actual exit status and parsed permgate decision under `PATH=/usr/bin:/bin`, plus first-word and post-env-assignment executable checks for every rendered hook command. It states the portable tracked-command and per-host-rendered-binding split, verifies HOME re-export before HOME-relative paths and shows that tracked commands name no interpreter or anchor path. It includes worker user settings and main-checkout local settings. Render evidence shows that `ruff`, `prettier` and `terminal-browser` resolve under the guard's rendered orchestrator tool PATH on the rendering host and that no PATH entry is a shims directory. Merged-settings evidence identifies runtime-added entries separately. No report claims complete effective failure-policy coverage from template inspection alone.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:517:Launch evidence shows both cache variables reaching the actual worker process on every route. Claude processes additionally receive the dedicated Claude configuration directory. Repeated-start evidence shows replacement of stale managed hooks, retained native merge denials and the unchanged Codex sandbox and approval arguments.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:521:Guard markers also show that worker project scripts, contextdb hooks, Stop gates and formatter payloads do not execute through tracked hooks. Descendant markers show that planted PATH interpreters do not execute on the tested hook routes, including an upstream-style `/usr/bin/env bash` descendant.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:523:The report separately identifies the writable agmsg store's current driver-selection route and `dotfiles-T133-agmsg-hardening-a01` ownership. Hook interpreter tests do not claim to close that residual.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:535:One implementation PR continues the existing branch `tools/worker-write-boundary-a01`, created from clean base `205fe85c`, on the Codex seat a010. The eight green tests, fixtures and evidence stay. The first push deletes the predecessor copy `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md` and adds the byte-identical dispatched a02 task at `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md`. This predecessor-copy deletion is the sole authorized edit to the predecessor's artifact directory.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:543:Every gh write and every git write runs as a separate command without shell chaining. Every worker command remains inside its sandbox. An operation that cannot complete there produces a blocked PONG with the exact command and boundary.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:547:`AGMSG-RESULT v1` names the final head, base, branch, changed files, new deployable scripts, source and installed paths, trusted anchor, interpreter and descendant inventory, hook PATH bindings, user and administrative settings destinations, staging path and printed installation command, Bot findings and proposed dispositions, open P0/P1 findings, exact test selectors, measured caps, task-copy SHA256 and evidence paths. It distinguishes historical observations from final-head results and names all pending operator steps.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:549:The report states the user-visible effects. Claude workers use `~/.claude-worker` and require its own Claude login. Worker trusted-path and worktree-configuration Edit denies also affect Bash sandbox writes. Agmsg store paths remain writable except `~/.agents/skills/agmsg/db/trusted-plugins`, and worker denies also cover `~/.agents/skills/agmsg/plugins/**`. Worker user settings add no excluded commands or Herdr socket allowance, while shared managed settings retain the three control-plane exclusions and Herdr socket for every seat. Tracked and main-local orchestrator project hooks are no-ops in worker sessions. Worker caches are private. Every Claude seat fails when its sandbox is unavailable.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:551:Administrative managed settings require sandboxing for the orchestrator as well as workers and disable unsandboxed retries. The former Linux gh exemption is removed. The orchestrator retains its existing functions within those requirements and the specified hook failure, guarding and interpreter/PATH-binding changes.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:553:The report states that no gh credential separation is established. Shared credentials permit worker-initiated API merges despite native command denials. The GitHub boundary is detection, not prevention, with the required next-records-PR regime check owned by P1-11.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:559:The permission-surface change receives the required operator-backed approval through the repository's existing process. The worker writes no approval row and treats no candidate-tree decision as authority.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:561:Live deployment is the operator's post-merge `make update`. The operator runs `make install-managed-settings`, inspects the rendered staging file and executes its printed `sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"` command with `/Library/Application Support/ClaudeCode/managed-settings.json` detected on macOS and `/etc/claude-code/managed-settings.json` detected on Linux. Administrative installation is recorded separately from staging and ordinary chezmoi application.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:565:The operator applies the prepared deterministic Codex permgate rule that stops approving sandbox escapes and restarts affected sessions.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:567:The deployment record checks effective settings after `make update` and administrative installation, including hooks added by merge scripts or integration installers. It verifies the installed managed-settings content, admin-required sandbox scope, worker directory, both platform policy outputs, static deny inventory, worktree-configuration denies, writable agmsg stores, worker-user and main-local hook placement, hook PATH and interpreter descendants, failure-policy coverage and sandbox startup without exposing credentials.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:569:The effective-settings check includes conflicting project and local sandbox relaxations and confirms that they do not weaken the administrative policy. It also records the shared control-plane exclusions and Herdr socket as available capabilities. It makes no claim that worker user arrays subtract those entries.
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md:576:amendment 4 (consolidated; amendment 3 was not dispatched), 2026-10-19T09:2xZ; task-consistency-check.py: OK; C-80 text security review of this text: .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-8520998.md.last.md Verdict: correct (amendment 3 f810c30: one P1, the permgate hook interpreter binding, fixed here)

 succeeded in 226ms:
        nodes { databaseId }
      }
    }
  }
}
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


def flatten(pages: Any, key: str | None = None) -> list[Any]:
    """Merge `gh api --paginate --slurp` pages into one list."""
    merged: list[Any] = []
    for page in pages:
        merged.extend(page[key] if key else page)
    return merged


    actor: dict[str, Any] | None,
    level: str,
    body: str | None,
    url: str | None,
    path: str | None = None,
    line: int | None = None,
    **extra: Any,
) -> dict[str, Any]:
    return {
        "source": source,
        "author": (actor or {}).get("login") or (actor or {}).get("slug") or "",
        "bot": is_bot(actor),
        "level": level,
        "path": path,
        "line": line,
        "body": body or "",
        "url": url,
        **extra,
        "disposition": "",
    }


def thread_states(repo: str, number: int, graphql: GraphQL) -> dict[int, dict[str, bool]]:
    """Map each review comment id to its thread's resolved and outdated state."""
    owner, name = repo.split("/", 1)
    states: dict[int, dict[str, bool]] = {}
    cursor = None
    while True:
        data = graphql(
            THREADS_QUERY,
            {"owner": owner, "name": name, "number": number, "cursor": cursor},
        )
        threads = data["data"]["repository"]["pullRequest"]["reviewThreads"]
        for thread in threads["nodes"]:
            state = {"resolved": thread["isResolved"], "outdated": thread["isOutdated"]}
            comments = thread["comments"]
            while True:
                for comment in comments["nodes"]:
                    states[comment["databaseId"]] = state
                if not comments["pageInfo"]["hasNextPage"]:
                    break
                page = graphql(
                    THREAD_COMMENTS_QUERY,
                    {"id": thread["id"], "cursor": comments["pageInfo"]["endCursor"]},
                )
                comments = page["data"]["node"]["comments"]
        if not threads["pageInfo"]["hasNextPage"]:
            return states
        cursor = threads["pageInfo"]["endCursor"]


            )
        )
    states = thread_states(repo, number, graphql)
    for comment in flatten(fetch(f"repos/{repo}/pulls/{number}/comments", True)):
        state = states.get(comment["id"], {"resolved": False, "outdated": False})
        items.append(
            item(
                "review_comment",
                comment["user"],
                "comment",
                comment["body"],
                comment["html_url"],
                comment["path"],
                comment.get("line") or comment.get("original_line"),
                **state,
            )
        )

    checks = []
    for run in flatten(fetch(f"repos/{repo}/commits/{sha}/check-runs", True), "check_runs"):
        conclusion = run.get("conclusion") or run.get("status")
        checks.append({"name": run["name"], "conclusion": conclusion, "url": run["html_url"]})
        output = run.get("output") or {}
        if conclusion not in PASSING_CONCLUSIONS:
            summary = " ".join(part for part in (output.get("title"), output.get("summary")) if part)
            items.append(
                item(
                    "check_run",
                    run.get("app"),
                    conclusion,
                    f"{run['name']}: {summary}".strip(),
                    run["html_url"],
                    check=run["name"],
                )
            )
        if output.get("annotations_count"):
            for annotation in flatten(fetch(f"repos/{repo}/check-runs/{run['id']}/annotations", True)):
                message = " ".join(part for part in (annotation.get("title"), annotation["message"]) if part)
                items.append(
                    item(
                        "annotation",
                        run.get("app"),
                        annotation["annotation_level"],
                        message,
                        run["html_url"],
                        annotation.get("path"),

**Analyzing GraphQL endpoint issues**
web search: 
web search: site.cli.github.com/manual/gh_api GraphQL graphql endpoint ...
exec
/bin/zsh -lc "sed -n '90,120p' .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md; nl -ba scripts/pr-feedback.py | sed -n '18,55p'; nl -ba scripts/pr-feedback.py | sed -n '80,95p'" in ~/Workspace/dotfiles
 succeeded in 14ms:
Fixing any baseline hit (the four of premise 3 are rows for their lineages' owners: PR #379's for the hook's two, PR #375's for resolve-threads.sh, the chain-review a04 owner for local-advisory.sh; the rest get owner tasks the orchestrator writes at acceptance from the RESULT's per-file list); a Makefile or workflow change (none is needed: premises 1 and 2); the omp hooks (PR B).

## Check

`uv run python -m unittest tests/unit/test_lint_comparisons.py -v` green and `uv run --no-project python -I scripts/lint-comparisons.py` (exit 0, no output) pasted in the validation file, with `ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/`, outside `.orchestration/` and excluding `scripts/lint-comparisons-baseline.tsv` (plan 021 step 7.2; the baseline is data, one row per hit on main, excluded by decision D-cap-F2 of Amendment 2), and 1000 added lines under `tests/` (INV-2); the script `scripts/lint-comparisons.py` alone is at most 200 lines.

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round, before or after the first RESULT, counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T129-normalised-comparison-lint-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T129-normalised-comparison-lint-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T129-normalised-comparison-lint-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-17T10:10:10Z)

The Codex half's round 1 (two P1, four P2): the make target and workflow step that did not exist are gone, the lint is the third test of item 3 under `make unit-test` (premises 1 and 2 added); the four hits in in-flight files are a content-hashed baseline whose stale row fails (item 2, premise 3 added, Makefile and test.yaml removed from allowed_files, the environment row true again); item 1 is the rule table with one fixture per row and the test iterates it; R4 reads Python from the `ast`; the fixtures the finding named (`[ = ]`, `case`, jq `==`/`startswith`/`test`, `cd -P`, `urllib.parse`, `canonical_path`, `normalise_*`) are in the table.

## Amendment 1 (round 2, 2026-10-17T10:48:37Z)

a005's question 1 (PONG 10:44Z): the lint as specified printed 87 hits (R1 22, R2 1, R3 6, R4 54, R6 4), the four baseline lines among them, the other 83 in files no in-flight task owns. Read from the list: the substring token rule matched `profile_hash` (`file`), `EXCLUDED_DIR_NAMES` (`dir`) and the like, which are not path operands, so the token rule becomes a segment match (item 1; decided by the orchestrator by default, no operator round); the hits that remain are real string-form comparisons (herdr-agents's `[[ ${git_dir} == "${common}/worktrees/"* ]]`, its jq `test("(^|/)-?(ba|z|fi)?sh$")` on a process name), so the baseline carries every remaining hit, not only the four, and the RESULT lists them per rule and per file for the orchestrator to assign owners (item 2, Out of scope). The rule table, the tests and the caps are unchanged; the stale-row test is the mechanism that empties the baseline.

## Amendment 2 (round 2, 2026-10-17T11:03:15Z)

a005's PONG of 11:01Z: `scripts/lint-comparisons.py` is 211 lines and the baseline 73 rows, 284 changed lines outside `tests/` and `.orchestration/`, over the Check's 200. Decision D-cap-F2 (the orchestrator, by default): the baseline TSV is data, one row per hit on origin/main, and leaves the 200 count; the script is code and must come down to at most 200 lines on its own (the per-rule messages, duplicated `--list-rules` text or helper indirection are the usual 11 lines; no rule, test or behaviour leaves). The Check sentence carries both.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-normalised-comparison-lint-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md
```
    18	import datetime
    19	import json
    20	import os
    21	import subprocess
    22	import sys
    23	from collections import Counter
    24	from collections.abc import Callable
    25	from pathlib import Path
    26	from typing import Any
    27	
    28	PASSING_CONCLUSIONS = {"success", "neutral", "skipped"}
    29	THREADS_QUERY = """
    30	query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
    31	  repository(owner: $owner, name: $name) {
    32	    pullRequest(number: $number) {
    33	      reviewThreads(first: 100, after: $cursor) {
    34	        pageInfo { hasNextPage endCursor }
    35	        nodes {
    36	          id
    37	          isResolved
    38	          isOutdated
    39	          comments(first: 100) {
    40	            pageInfo { hasNextPage endCursor }
    41	            nodes { databaseId }
    42	          }
    43	        }
    44	      }
    45	    }
    46	  }
    47	}
    48	"""
    49	THREAD_COMMENTS_QUERY = """
    50	query($id: ID!, $cursor: String) {
    51	  node(id: $id) {
    52	    ... on PullRequestReviewThread {
    53	      comments(first: 100, after: $cursor) {
    54	        pageInfo { hasNextPage endCursor }
    55	        nodes { databaseId }
    80	def gh_fetch(path: str, paginate: bool = False) -> Any:
    81	    """Return the JSON for a REST path; paginated responses become a list of pages."""
    82	    if paginate:
    83	        return json.loads(gh(["api", "--paginate", "--slurp", path]))
    84	    return json.loads(gh(["api", path]))
    85	
    86	
    87	def gh_graphql(query: str, variables: dict[str, Any]) -> Any:
    88	    args = ["api", "graphql", "-f", f"query={query}"]
    89	    for key, value in variables.items():
    90	        if value is not None:
    91	            args.extend(["-F" if type(value) is int else "-f", f"{key}={value}"])
    92	    return json.loads(gh(args))
    93	
    94	
    95	def require_auth() -> None:

**Assessing security helper and snapshot checks**
**Analyzing row completeness and rename handling**
**Analyzing repository host and security constraints**
**Preparing final security summary**
codex
1 点、仕様の矛盾を確認しました。全 `gh api` 呼び出しに `repos/mryfmo/dotfiles/…` を要求していますが、保持対象の feedback collector は review thread の解決状態を `gh api graphql` で取得します。この経路の repository binding と、それを検証するテスト条件が必要です。
exec
/bin/zsh -lc "rg -n 'closed:|out-of-scope:' .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "sed -n '155,215p' .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md" in ~/Workspace/dotfiles
exec
/bin/zsh -lc "nl -ba .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md | sed -n '70,82p;246,255p;360,371p'" in ~/Workspace/dotfiles
exec
/bin/zsh -lc 'shasum -a 256 .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md' in ~/Workspace/dotfiles
 succeeded in 106ms:
    70	    disposition: "residual: verdict and evidence snapshot filenames and shadow rows use the full head; each audit, security, local-review and sweep input is also matched by its full-head metadata, and this verdict task introduces no reservation lock."
    71	  - control: "design 5.14 item 6 (honest residuals)"
    72	    disposition: "residual: startup, path and snapshot controls are reported as damage reduction; neither host isolation nor independent GitHub credentials is claimed."
    73	  - control: "design 5.14 item 7 (verification)"
    74	    disposition: "residual: this task supplies concrete regression selectors and final-head evidence; the shared trusted-execution test helper remains owned by P1-6 and is reused only if available without expanding this task's edit boundary."
    75	  - control: "design 5.14 item 8 (committed approval ledger)"
    76	    disposition: "residual: verdict evaluation supplies no permission approval; every gh call names mryfmo/dotfiles explicitly, and PR data comes from GitHub at one base/head pair captured once and recorded at full SHAs, never shared refs or objects. No application path exists in this task; shared credentials remain a residual."
    77	  - control: "design 5.14 item 9 (private cache and absolute interpreter)"
    78	    disposition: "residual: the shared trusted-interpreter resolver anchors the install root to the passwd home of the real uid, never HOME, and the anchored private uv cache excludes worktrees, worker-writable caches and temporary directories; until the P1-3 resolver is available, verdict holds without a private resolver or PATH fallback."
    79	  - control: "design 5.14 item 10 (worker commands remain sandboxed)"
    80	    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; a command that cannot complete there produces a blocked PONG rather than an escape or alternate execution route."
    81	premises: []
    82	---
   246	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_without_the_shared_trusted_interpreter_resolver` verifies the interim hold and absence of interpreter discovery or application effects.
   247	
   248	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_reads_pasted_counters_without_sourcing_agmsg` plants a marker-writing agmsg driver and counter executable, supplies the valid pasted counters, and requires unchanged verdicts with no marker; missing, duplicate, mismatched and unreadable counter cases hold.
   249	
   250	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_ignores_replaced_local_objects_and_refs` serves forged PR bytes through a replaced local object and forged `origin/main`, while fixed GitHub fixtures return the authentic full-head changeset and contents. It requires the clean verdict and authenticated input hashes, no local-object evidence read, and hold on incomplete API data rather than a local fallback. Cover precheck ancestry, fix-commit membership and loop shadow evaluation through the same GitHub fixtures.
   251	
   252	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_names_the_repository_on_every_gh_call` runs with a fixed fake gh that records every argument vector and asserts `--repo mryfmo/dotfiles` on every `gh pr`/`gh run`/`gh issue` call and an endpoint path beginning with `repos/mryfmo/dotfiles/` on every `gh api` call, with no `--repo` flag or repository placeholder on API calls. It covers PR view/checks, API and feedback reads and loop shadow evaluation in PR-number order. A fork fixture containing the same head SHA cannot redirect a call.
   253	
   254	   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_a_changed_pr_base_or_head` supplies one initial GitHub `base40`/`head40` pair and differing SHAs on a required second read. Separate subcases change only the base, only the head and both. Each requires the named pair-change refusal, hold with exit 20 and no shadow row; the unchanged-pair control records both full SHAs and proves every compare listing and contents request uses the captured pair.
   255	
   360	
   361	Expected worker artifacts are `.orchestration/dotfiles-T133-verdict-audit-pool-a04/report.md`, `validation.md`, `sandbox.md`, `learning.md` and `autoskill.md`; revision instructions and selectors are also recorded in `revise.yaml`. Worker review evidence uses the required `-worker-` infix. Artifacts are written at those relative paths in `worker-f`; the RESULT states their placement, and the orchestrator copies required evidence by absolute path. Plan, todo and learn worklogs remain uncommitted.
   362	
   363	This task is `security: true`. The orchestrator performs its final-head task-level audit and separate security-profile review before the integration gate. Final-head CI, the complete feedback sweep, dispositions, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive fresh required evidence. Only the orchestrator performs `gh pr merge --repo mryfmo/dotfiles --squash --match-head-commit <audited head>` after the gate. PR #410 is integrated manually.
   364	
   365	No `@codex review` comment is posted. Observe automatic review for the bounded window, read both review bodies and inline findings, and record absence after 15 minutes as `bot: none`. Wait for the required CI checks to pass before a ready-for-review RESULT. Any new push requires checking its CI again.
   366	
   367	Every worker `gh pr`, `gh run` and `gh issue` command supplies `--repo mryfmo/dotfiles` or the full pull-request URL, and every worker `gh api` command supplies an explicit `repos/mryfmo/dotfiles/…` endpoint path with no `--repo` flag or repository placeholder; each gh command, Git write, push and fetch is an individual command inside the sandbox, without shell chaining or a wrapper combining commands. No excluded command, unsandboxed retry, API substitution or browser path bypasses a live boundary. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-verdict-audit-pool-a04 status=blocked` naming the exact command, exit status, output and boundary; preserve the available artifacts and wait for the orchestrator to re-task.
   368	
   369	Until plan 024 P1-14 lands, strings containing `gh pr merge` or `gh pr create` are written through the file-edit tool, not shell commands, heredocs or shell wrappers. This writing rule grants no execution authority.
   370	
   371	Live dispatch, merge and local Bats are not exercised. No application path exists in this task; the shared-UID residual remains as stated in the design.

 succeeded in 179ms:
a6baa1c4cd5fc5e7fb2ac2918e4590f156faf53507a44965111710f61d9bcb86  .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md

 succeeded in 182ms:
18:    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold"
42:    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path"
44:    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path"

 succeeded in 202ms:

   Fixtures use temporary repositories and fake tools. Their schema checks run without the sibling implementation. Red fixtures supply the inherited validation entry point as a test double where necessary so a new regression reaches its named defect. Refactoring retains every behavior case and assertion, and fixture lines count against the test cap.

6. The b8998de P1 in the application path is fixed. After accept and the shadow unlock, `--apply` runs the trusted `scripts/orchestrator/orch-gate.sh <task> <head> <pr>` and requires its zero exit before any dispatch or merge. Missing, refused or nonzero gate execution produces hold with exit 20, leaves no accepted application result and performs neither side effect. Application does not substitute its nine-condition result for the gate's receipt, audit-disposition and integration checks.

   `test_verdict_apply_runs_the_integration_gate_before_dispatch_or_merge_and_holds_on_failure` is written first. All nine conditions and the four-distinct-PR shadow requirement pass. A fake gate records the exact task, full head and PR and returns failure. The inherited implementation incorrectly dispatches and merges, giving the red result against `b8998de162afc72d53d07679b8f0a194fcc480ff`. The fixed implementation holds and calls neither tool. Missing and refused gate cases also hold. A zero-exit control proves the exact order gate, dispatch, merge and retains the head-matched merge arguments.

   The current gate wrapper takes a PR-worktree path in its second position. This task changes no gate interface. Refusal of the specified head form remains hold until that form is supported by the trusted wrapper. No alternate gate or direct-merge fallback bypasses the refusal.

7. The b8998de P2 in the cap parser is fixed. The parser honors the latest amendment's cap sentence, using the last applicable `at most <n>` declaration in text order instead of the first historical declaration. The effective sentence supplies its exclusions and test limit. A later test-only amendment replaces the test limit while retaining the outside limit.

   `test_verdict_condition_5_honors_the_latest_amended_caps` is written first. An otherwise green fixture contains an original 500-line test cap and a later amendment allowing 550, with 531 changed test lines. The inherited implementation applies 500 and fails condition 5, giving the red result against `b8998de162afc72d53d07679b8f0a194fcc480ff`. The fixed implementation accepts under 550. Subcases retain the actual a02 test-only amendment wording, verify a later lower limit refuses acceptance, and verify that amended exclusions and outside limits come from the effective cap sentence. Unrelated conditions remain green and evidence hashes remain current.

The seven required check names are `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.

## Out of scope

The sibling owns `audit-pool.sh`, changes to `orch-audit.sh`, `classes.yaml` and `test_audit_pool.py`. `dispatch.sh`, the record generator, `dispositions.py`, `--second-opinion`, `hold-playbook.sh`, `integrate-seat.sh`, gate and validator changes, Makefile targets, CI changes and live deployment remain outside this task. The two b8998de findings assigned above are fixed here rather than assigned to an advisory owner.

## Check

The validation file contains commands, verbatim output, exit statuses and tested heads for `make unit-test`, `make render-check`, `make format`, `shellcheck scripts/orchestrator/verdict.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/verdict.sh` and `uv run python -m unittest tests.unit.test_verdict -v`. The script checks are clean and the verdict module is green.

The concrete shadow invocation is `scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a03`. Its JSON, exit status and tested head appear in `.orchestration/dotfiles-T133-verdict-audit-pool-a03/validation.md`. Hold is expected before the required audit and acceptance evidence exist. This task exercises no live `--apply`.

Each new regression has its own red result against `b8998de162afc72d53d07679b8f0a194fcc480ff` and green result after the fix. Retained tests run on the final implementation. Historical a01 and a02 results keep their original references and do not substitute for final-head validation.

`git diff --numstat origin/main...HEAD` shows at most 300 changed lines outside `tests/` and `.orchestration/`, and 400 under `tests/`. Changed lines are additions plus deletions over the complete PR diff. `verdict.sh` is the sole implementation script and is at most 300 lines on its own. The two JSON schemas remain in the outside total and their line counts are also reported separately. Meeting a cap removes no required behavior, validation, regression case or trust-boundary control.

An inherited check failure is reproduced against the unchanged base with the same command and environment and reported as a failure with that evidence. It is never labelled passing or repaired outside the edit boundary. Local Bats tests remain unrun and GitHub Actions supplies their required results.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task-copy byte comparison and SHA256 cover this a03 text. The final inventory confirms the sibling files and predecessor branch artifacts have left PR #410.

## Completion

One branch, `tools/verdict-audit-pool-a01`, continues PR #410 with the split verdict scope. The first push contains the replacement a03 copy and the specified split removals. No second implementation PR or branch is created for this task and no parking operation is repeated.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with the live rules below, `dotfiles-T133-verdict-audit-pool-followup-a01` as the owner of advisory P2, `task_copy=<sha256 of .orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md>` and `parked_pr=407` in the RESULT. The orchestrator writes the owner task before assigning an advisory disposition. The two b8998de findings in items 6 and 7 belong to this reset.

There is at most one worker-side pre-push review round. Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. Predecessor rounds and stopped histories remain recorded. A surviving P0/P1 stops the PR for the operator's decision under the inherited Completion rule.

The report and RESULT identify head, base, branch, changed files, every feedback disposition, test names, code and test totals, schema counts, task-copy hash and evidence paths. They distinguish retained fixes, the split, historical evidence and final-head results. A Codex seat writes evidence at the same relative paths in its own worktree and states that placement in the RESULT. Worker review evidence uses the required `-worker-` infix and the orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. The orchestrator runs its own final-head task-level audit and separate security-profile review before the gate. Final-head CI, the feedback sweep, finding dispositions, acceptance record, integration gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive fresh required evidence. The orchestrator merges with `gh pr merge --squash --match-head-commit <audited head>` after the gate. Four-distinct-PR shadow enforcement remains in code and this PR is integrated manually.

No `@codex review` comment is posted. Automatic review is observed for the bounded window and absence after 15 minutes is recorded as `bot: none`. Commands matching a live ask rule are not issued and no API or browser path bypasses that rule. Each `gh` command, Git write and `git fetch` runs individually without shell chaining or a wrapper combining commands. Refused commands retain their command, exit status and output while independent authorized work continues.

Until plan 024 P1-14 lands, every string containing the words `gh pr merge` or `gh pr create` is written with the file-edit tool. Shell commands, heredocs and shell wrappers do not write those strings. This writing rule supplies no authorization to execute a command refused by the live permission boundary.

Live dispatch, merge and local Bats are not exercised. A trusted gate that rejects the head argument keeps live application on hold.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-verdict-audit-pool-a03.md: OK
premises: copied from a02 verbatim
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md
```

codex
- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:252](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:252) — Requiring `repos/mryfmo/dotfiles/…` on **every** `gh api` call excludes the retained feedback collector’s `gh api graphql` calls for review-thread resolution state; the prescribed test therefore rejects complete feedback collection. Define and test GraphQL repository binding through fixed owner/name variables and repository-bound thread IDs. [CLI documentation](https://cli.github.com/manual/gh_api)

📝 まとめ: Reviewed every threat row and the cited acceptance/review history; one specification defect remains for orchestrator disposition.

Not checked: implementation tests or deployed isolation; no files changed. The acknowledged same-UID and shared-credential risks remain.
Verdict: incorrect
hook: Stop
hook: Stop Completed
tokens used
88,827
- [P2] High confidence [.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:252](~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a04.md:252) — Requiring `repos/mryfmo/dotfiles/…` on **every** `gh api` call excludes the retained feedback collector’s `gh api graphql` calls for review-thread resolution state; the prescribed test therefore rejects complete feedback collection. Define and test GraphQL repository binding through fixed owner/name variables and repository-bound thread IDs. [CLI documentation](https://cli.github.com/manual/gh_api)

📝 まとめ: Reviewed every threat row and the cited acceptance/review history; one specification defect remains for orchestrator disposition.

Not checked: implementation tests or deployed isolation; no files changed. The acknowledged same-UID and shared-credential risks remain.
Verdict: incorrect
